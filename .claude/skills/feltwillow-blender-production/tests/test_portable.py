"""Synthetic unit tests: no real Blender models, reviews, paid calls or approvals."""
from __future__ import annotations
import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime,timezone,timedelta
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import fw_contracts as f
from ambient_motion import frame_time,stable_phase,displacement
from context_snapshot import collect
from contact_sheet import make_sheet

class PortableTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        for name in ('candidate.bin','reference.txt','evidence.txt'):
            (self.root/name).write_text('Synthetic test fixture: '+name)
        self.bind=lambda name:{'path':name,'sha256':f.sha256_file(self.root/name)}
        self.asset={'schema':'feltwillow.blender.asset.v1','asset_id':'test_bird','kind':'character',
                    'candidate':self.bind('candidate.bin'),'source_bindings':[self.bind('reference.txt')],
                    'design':{'test_fixture':True},
                    'anatomy':{'appendages':[{'id':'wing.L','kind':'wing'},{'id':'wing.R','kind':'wing'}],
                               'locomotion':['flight','perch'],
                               'neutral_measurement':{'definition':'test landmarks','value':1.0,'unit':'test_unit'}}}
        self.now=datetime(2026,10,18,12,0,tzinfo=timezone.utc)
        self.job={'schema':'feltwillow.blender.job.v1','job_id':'synthetic_test','provider':'fal',
                  'endpoint':'fal-ai/patina','inputs':[self.bind('reference.txt')],'settings':{},'requests':1,
                  'quote':{'currency':'USD','maximum_usd':'0.10','quoted_at':self.now.isoformat(),'max_age_hours':24,
                           'source_url':'https://fal.ai/models/fal-ai/patina'}}
        self.job['approval']={'decision':'approved','by':'SYNTHETIC TEST - NOT USER APPROVAL','at':self.now.isoformat(),
                              'request_sha256':f.digest(self.job,('approval',)),'max_requests':1,'max_total_usd':'0.10'}
        self.ledger={'currency':'USD','cap_usd':'1.00','entries':[]}
    def tearDown(self):self.temp.cleanup()
    def err(self,errors,text):self.assertTrue(any(text in s for s in errors),errors)
    def test_malformed_kind_returns_errors(self):
        self.asset['kind']=[]
        self.err(f.validate_asset(self.asset,self.root),'unsupported kind')
    def test_malformed_endpoint_returns_errors(self):
        self.job['endpoint']=[]
        self.err(f.validate_job(self.job,self.ledger,self.root,self.now),'allowlist')
    def test_huge_number_rejected(self):
        self.assertFalse(f.number(10**1000))
    def test_valid_asset_metadata(self):self.assertEqual(f.validate_asset(self.asset,self.root),[])
    def test_no_approval_is_not_approved(self):self.err(f.validate_asset(self.asset,self.root,True),'review')
    def test_synthetic_hash_bound_review(self):
        self.asset['review']={'decision':'approved','reviewer':'TEST ONLY','reviewed_at':self.now.isoformat(),
                             'spec_sha256':f.digest(self.asset,('review',)),'evidence':[self.bind('evidence.txt')],
                             'checks':{k:True for k in f.CHECKS['character']}}
        self.assertEqual(f.validate_asset(self.asset,self.root,True),[])
        self.asset['design']['changed']=True
        self.err(f.validate_asset(self.asset,self.root,True),'stale')
    def test_tampered_file(self):
        (self.root/'candidate.bin').write_text('changed');self.err(f.validate_asset(self.asset,self.root),'mismatch')
    def test_missing_file(self):
        (self.root/'candidate.bin').unlink();self.err(f.validate_asset(self.asset,self.root),'missing')
    def test_duplicate_appendage(self):
        self.asset['anatomy']['appendages']*=2;self.err(f.validate_asset(self.asset,self.root),'duplicate appendage')
    def test_limbless_profile_supported(self):
        self.asset['anatomy']['appendages']=[];self.asset['anatomy']['locomotion']=['slither']
        self.assertEqual(f.validate_asset(self.asset,self.root),[])
    def test_nonpositive_height_rejected(self):
        self.asset['anatomy']['neutral_measurement']['value']=0
        self.err(f.validate_asset(self.asset,self.root),'positive neutral')
    def test_boolean_not_measurement(self):
        self.asset['anatomy']['neutral_measurement']['value']=True
        self.err(f.validate_asset(self.asset,self.root),'positive neutral')
    def test_no_universal_milo_ratio(self):
        self.asset['anatomy']['neutral_measurement']['value']=12
        self.assertEqual(f.validate_asset(self.asset,self.root),[])
    def test_environment_needs_envelope(self):
        self.asset['kind']='environment';self.err(f.validate_asset(self.asset,self.root),'camera envelope')
    def test_path_traversal(self):
        for bad in ('../x','/tmp/x','a/../x','a//x','./x','a\\x'):
            with self.subTest(bad=bad),self.assertRaises(ValueError):f.safe_path(self.root,bad)
    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root/'link').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(ValueError):f.safe_path(self.root,'link/secret')
    def test_duplicate_json_key(self):
        p=self.root/'duplicate.json';p.write_text('{"x":1,"x":2}')
        with self.assertRaises(ValueError):f.load_json(p)
    def test_nonfinite_json(self):
        p=self.root/'nan.json';p.write_text('{"x":NaN}')
        with self.assertRaises(ValueError):f.load_json(p)
    def test_digest_order_independent(self):self.assertEqual(f.digest({'a':1,'b':2}),f.digest({'b':2,'a':1}))
    def test_money_rejects_unsafe_values(self):
        for value in (-1,'NaN','Infinity',True,None):
            with self.subTest(value=value),self.assertRaises(ValueError):f.money(value)
    def test_valid_synthetic_job(self):self.assertEqual(f.validate_job(self.job,self.ledger,self.root,self.now),[])
    def test_job_pending_not_approved(self):
        self.job['approval']['decision']='pending';self.err(f.validate_job(self.job,self.ledger,self.root,self.now),'approval')
    def test_settings_change_invalidates_consent(self):
        self.job['settings']['detail']='higher';self.err(f.validate_job(self.job,self.ledger,self.root,self.now),'stale')
    def test_unknown_endpoint(self):
        self.job['endpoint']='other/expensive';self.err(f.validate_job(self.job,self.ledger,self.root,self.now),'allowlist')
    def test_stale_quote(self):self.err(f.validate_job(self.job,self.ledger,self.root,self.now+timedelta(days=2)),'quote')
    def test_future_quote(self):self.err(f.validate_job(self.job,self.ledger,self.root,self.now-timedelta(days=1)),'future')
    def test_unknown_charge_stays_reserved(self):
        self.ledger['entries']=[{'job_id':'old','status':'unknown','maximum_usd':'0.95'}]
        self.assertEqual(f.ledger_used(self.ledger),Decimal('0.95'))
        self.err(f.validate_job(self.job,self.ledger,self.root,self.now),'insufficient')
    def test_settled_uses_actual(self):
        self.ledger['entries']=[{'job_id':'old','status':'settled','actual_usd':'0.20','maximum_usd':'0.95'}]
        self.assertEqual(f.ledger_used(self.ledger),Decimal('0.20'))
    def test_settled_missing_cost_rejected(self):
        self.ledger['entries']=[{'job_id':'old','status':'settled'}]
        with self.assertRaises(ValueError):f.ledger_used(self.ledger)
    def test_duplicate_submission_rejected(self):
        self.ledger['entries']=[{'job_id':self.job['job_id'],'status':'submitted','maximum_usd':'0.10'}]
        self.err(f.validate_job(self.job,self.ledger,self.root,self.now),'already recorded')
    def test_cap_not_multiplied_wrongly(self):
        self.ledger['cap_usd']='0.10'
        self.assertEqual(f.validate_job(self.job,self.ledger,self.root,self.now),[])
    def test_timestamp_needs_timezone(self):
        with self.assertRaises(ValueError):f.timestamp('2026-10-18T12:00:00')
    def test_global_frame_time(self):self.assertEqual(str(frame_time(30,30000,1001)),'1001/1000')
    def test_no_frame_reseed(self):
        t=float(frame_time(240,24));self.assertEqual(displacement('grass',t,8,.02),displacement('grass',10,8,.02))
    def test_distinct_stable_phase(self):
        self.assertEqual(stable_phase('grass',4),stable_phase('grass',4));self.assertNotEqual(stable_phase('grass',4),stable_phase('leaf',4))
    def test_periodic_and_bounded_ambient(self):
        for i in range(100):
            v=displacement('x',i/10,7,.02,2);self.assertLessEqual(abs(v),.020000001)
            self.assertAlmostEqual(v,displacement('x',i/10+7,7,.02,2),places=12)
    def test_invalid_ambient(self):
        with self.assertRaises(ValueError):displacement('x',0,0,1)
        with self.assertRaises(ValueError):displacement('x',float('nan'),2,1)
    def state(self,frame):
        h='a'*64
        return {'global_frame':frame,'environment_sha256':h,'camera_sha256':h,'lighting_sha256':h,'render_settings_sha256':h,
                'assets':{},'props':{},'actors':{},'ambient':{'preset':'test','seed':1},'velocities':{}}
    def chain(self):
        return {'schema':'feltwillow.blender.chain.v1','fps_num':24,'fps_den':1,'shots':[
            {'id':'one','start':0,'end':24,'join':'start','start_state':self.state(0),'end_state':self.state(24)},
            {'id':'two','start':24,'end':48,'join':'continuous','start_state':self.state(24),'end_state':self.state(48)}]}
    def test_valid_chain(self):self.assertEqual(f.validate_chain(self.chain()),[])
    def test_camera_change_breaks_continuity(self):
        c=self.chain();c['shots'][1]['start_state']['camera_sha256']='b'*64
        self.err(f.validate_chain(c),'boundary states differ')
    def test_ambient_reset_breaks_continuity(self):
        c=self.chain();c['shots'][1]['start_state']['ambient']['seed']=7
        self.err(f.validate_chain(c),'boundary states differ')
    def test_gap_rejected(self):
        c=self.chain();c['shots'][1]['start']=25;self.err(f.validate_chain(c),'gap or overlap')
    def test_cut_needs_reason(self):
        c=self.chain();c['shots'][1]['join']='cut';self.err(f.validate_chain(c),'cut needs')
    def test_valid_camera_cut(self):
        c=self.chain();s=c['shots'][1];s.update(join='cut',cut_reason='approved portrait');s['start_state']['camera_sha256']='b'*64
        self.assertEqual(f.validate_chain(c),[])
    def test_prop_change_requires_event(self):
        c=self.chain();s=c['shots'][1];s.update(join='cut',cut_reason='new shot');s['start_state']['props']={'net':'cut'}
        self.err(f.validate_chain(c),'explicit event')
    def test_actor_requires_velocity(self):
        c=self.chain();c['shots'][0]['start_state']['actors']={'bird':{'root_matrix':[0]*16,'pose_sha256':'a'*64}}
        self.err(f.validate_chain(c),'velocity')
    def test_context_snapshot_does_not_assume_approval(self):
        home=self.root/'stories'/'test';home.mkdir(parents=True)
        (home/'visual_bible.json').write_text(json.dumps({'characters':{},'pipeline':'keyframe_boundary_v1'}))
        (home/'keyframe_plan.json').write_text('{"images":[]}')
        d=collect(self.root,'test');self.assertEqual(d['keyframe_count'],0);self.assertFalse(d['owner_acceptance_ledger_present'])
        self.assertIn('do not establish approval',d['warning'])
    def test_invalid_story_path(self):
        with self.assertRaises(ValueError):collect(self.root,'../../home')
    def test_contact_sheet_preserves_input_and_refuses_overwrite(self):
        from PIL import Image
        img=self.root/'input.png';Image.new('RGB',(200,100),(127,127,127)).save(img)
        before=f.sha256_file(img);out=self.root/'sheet.png'
        self.assertEqual(make_sheet([img],out,columns=1,width=200),(200,200))
        self.assertEqual(f.sha256_file(img),before)
        self.assertTrue(out.with_suffix('.json').is_file())
        with self.assertRaises(ValueError):make_sheet([img],out)

if __name__=='__main__':unittest.main()
