"""CPU-only performance registry, immutable evidence and staging contracts."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image, ImageDraw

from production import character_performance as cp
from production import audio_visual_plan as av
from production import serve_scene_review as server

ROOT=Path(__file__).resolve().parents[1]


class PerformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder,cls.plan,cls.chars,cls.locs,cls.lib=cp.load(ROOT,'lion_and_mouse_v7')

    def check(self,lib=None,plan=None,root=None,gate='planning'):
        return cp.validate(lib or self.lib,plan or self.plan,self.chars,root,gate)

    def binding(self,iid,plan=None,actor='Milo'):
        return next(i for l in (plan or self.plan)['lines'] for b in l['beats'] for i in b['image_sequence']['images'] if i['id']==iid)['performance'][actor]

    def test_planned_missing_assets_do_not_block_planning(self):
        self.assertEqual(self.check(),[])
        self.assertTrue(self.check(root=ROOT,gate='image'))
        self.assertTrue(all(v['owner_decision'] is None for a in self.lib['assets'].values() for v in a['variants'].values() if v['status'] not in cp.APPROVED))
        self.assertTrue(all(v['file'] is None for a in self.lib['assets'].values() for v in a['variants'].values() if v['status']=='planned'))

    def test_reuse_has_one_asset_and_one_off_is_allowed(self):
        ids=['S01-L001-B01-I02','S01-L002-B03-I02','S01-L003-B01-I02']
        self.assertEqual(len({self.binding(i)['pose_id'] for i in ids}),1)
        report=cp.usage_report(self.lib,self.plan)
        self.assertEqual(report['counts']['actual_generated_performance_candidates'],44)
        self.assertEqual(report['counts']['approved_performance_variants'],28)
        # The owner's later acceptance binds the exact current bytes; earlier
        # decisions remain with superseded versions, and scene readiness stays separate.
        generated=[v for a in self.lib['assets'].values() for v in a['variants'].values() if v.get('file')]
        approved=[v for v in generated if v['status']=='owner_selected_for_performance']
        pending=[v for v in generated if v['status']=='candidate_pending_owner_review']
        self.assertEqual((len(approved),len(pending)),(28,16))
        self.assertTrue(all(v['owner_decision']['sha256']==v['file']['sha256'] and v['owner_decision']['scope']=='performance_use_only' for v in approved))
        self.assertTrue(all(v['owner_decision'] is None for v in pending))
        self.assertEqual(report['counts']['actual_scene_images_approved_by_this_library'],0)
        milo_approved=[v for a in self.lib['assets'].values() if a['actor']=='Milo' for v in a['variants'].values() if v['status']=='owner_selected_for_performance']
        self.assertTrue(all(v.get('superseded_candidates') for v in milo_approved))
        one=self.lib['assets'][self.binding('S01-L002-B01-I01')['pose_id']]
        self.assertEqual(one['reuse_status'],'one_off')
        self.assertEqual(len(report['impact'][one['id']]),1)

    def test_unknown_ids_and_canonical_hash_fail_closed(self):
        for field,value in [('pose_id','made.up'),('expression_id','made.up'),('pose_variant','missing')]:
            plan=copy.deepcopy(self.plan);self.binding('S01-L001-B01-I02',plan)[field]=value
            self.assertTrue(self.check(plan=plan))
        plan=copy.deepcopy(self.plan)
        image=next(i for l in plan['lines'] for b in l['beats'] for i in b['image_sequence']['images'])
        image['performance']['OtherAnimal']=image['performance'].pop('Milo')
        self.assertTrue(self.check(plan=plan))
        lib=copy.deepcopy(self.lib);lib['assets']['milo.walk.screen_right.lightstep.3q']['canonical']['sha256']='0'*64
        self.assertTrue(any('canonical' in e for e in self.check(lib)))

    def test_measurement_and_previous_candidate_references_do_not_gain_identity_authority(self):
        walk=self.lib['assets']['milo.walk.screen_right.lightstep.3q']['variants']['contact']
        inputs=walk['creation']['inputs']
        self.assertEqual([r['role'] for r in inputs],['canonical_identity','canonical_width_annotation','previous_pose_candidate'])
        for role in ('canonical_width_annotation','previous_pose_candidate'):
            lib=copy.deepcopy(self.lib)
            refs=lib['assets']['milo.walk.screen_right.lightstep.3q']['variants']['contact']['creation']['inputs']
            next(r for r in refs if r['role']==role)['authority']='identity_anatomy_material_palette'
            self.assertTrue(any('reference role contradicts' in e for e in self.check(lib)))

    def test_pose_approval_does_not_certify_anatomy_or_prop_fit(self):
        # Use the preserved, genuinely owner-selected earlier bytes as a fixture;
        # the current replacement is pending and must never inherit that decision.
        lib=copy.deepcopy(self.lib)
        snapshot=ROOT/'stories/lion_and_mouse_v7'/cp.AUDIT/'s01_s03_revision_preflight_r001/previous_variant_012.json'
        v=json.loads(snapshot.read_text())
        lib['assets']['milo.acorn.pick_hold.3q']['variants']['hold']=v
        self.assertIn(v['status'],cp.APPROVED)
        self.assertTrue(cp.anatomy_blockers(lib,'Milo',v))
        proposal=cp.proposal(ROOT,self.folder,lib,self.plan,self.chars,self.locs,'S01-L004-B03-I02')
        self.assertTrue(any('anatomy match pending' in s for s in proposal['blockers']))
        self.assertTrue(any('acorn' in s for s in proposal['blockers']))
        self.assertEqual(self.check(lib),[])
        changed=copy.deepcopy(lib)
        changed['assets']['milo.acorn.pick_hold.3q']['variants']['hold']['anatomy_review']['image_sha256']='0'*64
        self.assertTrue(any('anatomy review' in e for e in self.check(changed)))

    def test_uniform_actor_scale_and_anatomy_evidence_required(self):
        lib=copy.deepcopy(self.lib)
        lib['anatomy_policies']['Milo']['staging_scale_policy']='resize_head_separately'
        self.assertTrue(any('independently resized' in e for e in self.check(lib)))
        lib=copy.deepcopy(self.lib)
        v=lib['assets']['milo.acorn.pick_hold.3q']['variants']['hold']
        v['anatomy_review']['status']='matched_reviewed_reference'
        self.assertTrue(any('comparable-view method' in e for e in self.check(lib)))
        v['anatomy_review']['comparison_method']='matched-view annotated comparison'
        self.assertTrue(self.check(lib))
        self.assertTrue(cp.anatomy_blockers(self.lib,'Milo',self.lib['assets']['milo.decision.stationary.3q']['variants']['long_path']))

    def test_view_head_angle_base_revision_and_closed_mouth(self):
        for field,value in [('view','profile'),('head_view','rear'),('body_facing','screen_left'),('head_orientation','left'),('mouth','open'),('visible_teeth',True)]:
            plan=copy.deepcopy(self.plan);self.binding('S02-L003-B01-I01',plan)[field]=value
            self.assertTrue(self.check(plan=plan))
        aid=self.binding('S02-L003-B01-I01')['expression_id']
        lib=copy.deepcopy(self.lib);lib['assets'][aid]['portrait_base']['revision']='r099'
        self.assertTrue(self.check(lib))
        lib=copy.deepcopy(self.lib);lib['assets'][aid]['constraints']['visible_teeth']=True
        self.assertTrue(self.check(lib))

    def test_no_narrator_mouth_and_dialogue_remains_separate(self):
        for line,beat,image,actor,binding in cp.uses(self.plan):
            self.assertEqual(binding['mouth'],'closed')
            if line['speaker']=='NARRATOR':self.assertIsNone(beat['dialogue']['mouth_driver'])
            else:self.assertEqual(beat['dialogue']['mouth_driver'],'future_reviewed_dialogue_pipeline')

    def test_independent_camera_measurements_can_differ(self):
        plan=copy.deepcopy(self.plan)
        for iid,distance,scale in [('S01-L001-B01-I02',1,0.65),('S01-L003-B01-I02',10,0.10)]:
            self.binding(iid,plan)['staging'].update(camera_status='measured',camera_distance_m=distance,lens_or_zoom='test camera',crop=[0,0,1,1],depth=distance,screen_scale=scale)
        self.assertEqual(self.check(plan=plan),[])
        # Registry itself must never encode one universal pixel height.
        lib=copy.deepcopy(self.lib);lib['assets']['milo.walk.screen_right.lightstep.3q']['pixel_height']=500
        self.assertTrue(self.check(lib))

    def test_unknown_camera_cannot_invent_distance(self):
        plan=copy.deepcopy(self.plan);self.binding('S01-L001-B01-I02',plan)['staging']['camera_distance_m']=10
        self.assertTrue(self.check(plan=plan))

    def test_fork_requires_shared_root_scale_contract(self):
        for number in [6,7,8]:
            b=self.binding(f'S03-L{number:03d}-B01-I02')
            self.assertEqual(b['staging']['contract_id'],'fork_decision.Milo')
            self.assertEqual(b['render_method'],'deterministic_layers')
        for mutate in [lambda p:self.binding('S03-L007-B01-I02',p)['staging'].update(contract_id='new_root'),lambda p:p['performance_staging_contracts']['fork_decision.Milo'].update(scale_contract='new_head_size')]:
            plan=copy.deepcopy(self.plan);mutate(plan);self.assertTrue(self.check(plan=plan))
        plan=copy.deepcopy(self.plan)
        plan['performance_staging_contracts']['fork_decision.Milo']['measurement_status']='owner_reviewed_anchor'
        self.assertTrue(any('reviewed anchor' in e for e in self.check(plan=plan)))

    def test_revision_and_hash_binding_require_explicit_update(self):
        for field,value in [('pose_revision','r999'),('expression_revision','r999'),('pose_sha256','0'*64)]:
            plan=copy.deepcopy(self.plan);self.binding('S01-L001-B01-I02',plan)[field]=value
            self.assertTrue(self.check(plan=plan))

    def test_immutable_source_mismatch_is_not_auto_repaired(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'story'
            source=root/'original.png';source.write_bytes(b'unchanged source')
            av.write(folder/cp.AUDIT/'BEFORE.json',{'files':[{'path':'original.png','sha256':av.digest(source)}]})
            self.assertEqual(cp.immutable_errors(root,folder),[])
            source.write_bytes(b'altered source')
            self.assertTrue(cp.immutable_errors(root,folder))

    def test_walk_keys_and_no_identical_stamp_cycle(self):
        walk=self.lib['assets']['milo.walk.screen_right.lightstep.3q']
        self.assertEqual(walk['gait_order'],['contact','passing_step','opposite_contact'])
        self.assertNotEqual(walk['variants']['contact']['support_contacts'],walk['variants']['opposite_contact']['support_contacts'])
        lib=copy.deepcopy(self.lib);lib['assets'][walk['id']]['gait_order']=['contact']*3
        self.assertTrue(self.check(lib))
        lib=copy.deepcopy(self.lib)
        for v in lib['assets'][walk['id']]['variants'].values():v['file']={'sha256':'a'*64}
        self.assertTrue(any('identical stamp' in e for e in self.check(lib)))

    def test_early_shortcut_commitment_rejected(self):
        plan=copy.deepcopy(self.plan);self.binding('S03-L004-B01-I02',plan)['pose_id']='milo.walk.screen_right.lightstep.3q'
        self.binding('S03-L004-B01-I02',plan)['pose_variant']='passing_step'
        self.assertTrue(any('route emphasis' in e for e in self.check(plan=plan)))

    def test_contact_support_and_state_phases(self):
        plan=copy.deepcopy(self.plan);self.binding('S05-L009-B01-I02',plan)['support']='ground'
        self.assertTrue(self.check(plan=plan))
        plan=copy.deepcopy(self.plan);self.binding('S05-L009-B01-I03',plan)['pose_variant']='support_lost'
        self.assertTrue(self.check(plan=plan))
        phases=[self.binding(f'S05-L009-B01-I{i:02d}')['trajectory_phase'] for i in range(1,5)]
        self.assertEqual(len(set(phases)),4)
        plan=copy.deepcopy(self.plan)
        self.binding('S10-L003-B01-I03',plan,'Leo')['pose_variant']='approach'
        self.assertTrue(any('phase' in e for e in self.check(plan=plan)))

    def test_sleeping_details_reuse_one_body(self):
        ids=[self.binding(f'S05-L{i:03d}-B01-I01',actor='Leo')['pose_id'] for i in range(1,5)]
        self.assertEqual(len(set(ids)),1)

    def test_variant_parent_cycles_and_fake_approval(self):
        lib=copy.deepcopy(self.lib);aid='milo.portrait.base.3q'
        lib['assets'][aid]['parents']=[dict(id=aid,revision='r001',variant='default',sha256=None,authority='portrait_geometry_only')]
        self.assertTrue(any('cycle' in e for e in self.check(lib)))
        lib=copy.deepcopy(self.lib);lib['assets'][aid]['variants']['default'].update(status='approved_for_scene_use',owner_decision=None)
        self.assertTrue(self.check(lib))
        plan=copy.deepcopy(self.plan);self.binding('S02-L003-B01-I01',plan)['binding_status']='bound_reviewed_performance'
        binding=self.binding('S02-L003-B01-I01',plan)
        binding['pose_sha256']=self.lib['assets'][binding['pose_id']]['variants'][binding['pose_variant']]['file']['sha256']
        self.assertTrue(any('pending asset' in e for e in self.check(plan=plan)))

    def test_existing_images_receipts_and_audio_semantics_unchanged(self):
        self.assertEqual(cp.immutable_errors(ROOT,self.folder),[])
        before=av.read(self.folder/cp.AUDIT/'before_audio_visual_plan.json')
        after=copy.deepcopy(self.plan)
        # Camera/location continuity is intentionally revised. Audio, stable IDs,
        # event ordering, sequence roles and causal states remain immutable.
        for key in ('script_line_order','world_events','world_states','state_rules'):
            self.assertEqual(after[key],before[key])
        def semantics(plan):
            return [(l['line_id'],l['text'],l['speaker'],l['audio'],
                [(b['id'],b['state_in'],b['state_start'],b['state_out'],b['entry_events'],b['timing'],b['image_sequence']['mode'],
                  [(im['id'],im['role'],im['state'],im['events_before']) for im in b['image_sequence']['images']]) for b in l['beats']]) for l in plan['lines']]
        # Owner's r005 correction moves the taste event from I03 to a new,
        # planned I04. Project only that explicit change back for this legacy
        # invariant; every other line/image/audio/state must remain identical.
        revised=next(l for l in after['lines'] if l['line_id']=='S01-L004')['beats'][2]
        original=next(l for l in before['lines'] if l['line_id']=='S01-L004')['beats'][2]
        self.assertEqual([i['id'] for i in revised['image_sequence']['images']],
                         [i['id'] for i in original['image_sequence']['images']]+['S01-L004-B03-I04'])
        revised['image_sequence']['images']=copy.deepcopy(original['image_sequence']['images'])
        # Newly recorded S13-S16 are now hash-bound audio with an explicit
        # visual backlog. Exact local provenance is checked by audio tests.
        for current, historical in zip(after['lines'],before['lines']):
            if int(current['audio_scene'][1:])>=13:
                self.assertEqual(current['audio']['status'],'available_in_r001')
                self.assertEqual(current['planning_status'],'pending_visual_authoring')
                self.assertEqual(current['beats'],[])
                current['audio']=copy.deepcopy(historical['audio'])
        # Owner expanded the ungenerated S05 trip to four keys. Restore only
        # that explicit sequence for the historical invariant; dedicated S04-S05
        # tests protect the new phases and preserve the exact original event.
        trip=next(l for l in after['lines'] if l['line_id']=='S05-L008')['beats'][0]
        old_trip=next(l for l in before['lines'] if l['line_id']=='S05-L008')['beats'][0]
        self.assertEqual([i['id'] for i in trip['image_sequence']['images']],
                         ['S05-L008-B01-I01','S05-L008-B01-I02','S05-L008-B01-I03','S05-L008-B01-I04'])
        trip['image_sequence']=copy.deepcopy(old_trip['image_sequence'])
        self.assertEqual(semantics(after),semantics(before))
        available=[l for l in after['lines'] if l['audio']['status']=='available_in_r001']
        self.assertEqual(len(available),98)
        self.assertTrue(all(l['audio']['duration_seconds'] is None and not l['beats'] for l in after['lines'] if int(l['audio_scene'][1:])>=13))
        old=av.read(self.folder/cp.AUDIT/'before_character_library.json')
        selected=copy.deepcopy(self.chars['characters'])
        reconciliation=av.read(self.folder/'owner_leo_canonical_reconciliation_r001.json')
        self.assertEqual(selected['Leo']['canonical']['sha256'],reconciliation['canonical']['sha256'])
        self.assertEqual(selected['Leo']['canonical']['path'],old['characters']['Leo']['canonical']['path'])
        self.assertFalse(reconciliation['image_bytes_changed'])
        selected['Leo']['canonical']=copy.deepcopy(old['characters']['Leo']['canonical'])
        self.assertEqual(old['characters'],selected)

    def test_dry_proposal_never_infers_scene_approval_or_submits(self):
        proposal=cp.proposal(ROOT,self.folder,self.lib,self.plan,self.chars,self.locs,'S01-L001-B01-I02')
        self.assertTrue(proposal['dry_run']);self.assertFalse(proposal['submission_allowed'])
        self.assertTrue(proposal['blockers']);self.assertIsNone(proposal['estimated_total_cost'])
        self.assertEqual(proposal['request_count'],1)
        self.assertEqual(proposal['ordered_references'][0]['role'],'canonical_identity')
        self.assertIsNone(proposal['sidecar_requirements']['owner_scene_approval'])
        proposal=cp.proposal(ROOT,self.folder,self.lib,self.plan,self.chars,self.locs,'S03-L006-B01-I02',1)
        self.assertTrue(any('reference limit' in e for e in proposal['blockers']))
        self.assertTrue(any('locked background' in e for e in proposal['blockers']))

    def test_derive_is_only_usage_not_copied_pose_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);(folder/'derived').mkdir()
            report=cp.derive(folder,self.lib,self.plan,self.chars)
            self.assertGreater(len(report['impact']['milo.walk.screen_right.lightstep.3q']),3)
            self.assertFalse(list(folder.rglob('*.png')))
            self.assertTrue((folder/'derived/AUDIO_PERFORMANCE_INDEX.md').exists())

    def test_extra_review_page_does_not_serve_repository(self):
        assets=server.review_assets(ROOT)
        self.assertIn('/'+server.PERFORMANCE_GALLERY.as_posix(),assets)
        self.assertNotIn('/stories/lion_and_mouse_v7/character_library.json',assets)
        self.assertEqual(sum(p.suffix=='.wav' for p in assets.values()),33)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'bad.html').write_text('<img src="../outside.png">')
            with self.assertRaises(ValueError):server.gallery_assets(root,Path('bad.html'))


class SyntheticCandidateTests(unittest.TestCase):
    """Real synthetic RGBA files and ledgers, never production assets."""
    def test_distinct_candidate_and_approval_scopes_bytes_and_sidecars(self):
        folder,plan,chars,locs,lib=cp.load(ROOT,'lion_and_mouse_v7')
        lib=copy.deepcopy(lib)
        # This fixture tests synthetic files independently of local candidate PNGs.
        lib.pop('anatomy_policies',None)
        for item in lib['assets'].values():
            for variant in item['variants'].values():
                variant.update(status='planned',file=None,creation=None,owner_decision=None)
                variant.pop('anatomy_review',None)
                # Production component reviews identify real candidate bytes;
                # they cannot describe this fixture's planned/synthetic files.
                variant.pop('component_review',None)
            for parent in item['parents']:
                parent['sha256']=None
        # Use full planning graph, but create just one pose candidate and canonical bytes.
        actor='Milo';aid='milo.walk.screen_right.lightstep.3q';asset=lib['assets'][aid];v=asset['variants']['contact']
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            canonical=root/asset['canonical']['path'];canonical.parent.mkdir(parents=True);canonical.write_bytes((ROOT/asset['canonical']['path']).read_bytes())
            path=root/'character/characters/lion_and_mouse_v7/Milo/poses/milo_walk_contact_3q_r001_candidate.png';path.parent.mkdir(parents=True)
            im=Image.new('RGBA',(20,20));ImageDraw.Draw(im).rectangle((5,5,15,19),fill=(100,100,100,255));im.save(path)
            side=path.with_suffix('.json');receipt=root/'receipt.json';receipt.write_text('{"method":"synthetic test"}')
            v['file']={'path':str(path.relative_to(root)),'sha256':av.digest(path),'dimensions':[20,20],'alpha':{'has_alpha':True,'extrema':[0,255]},'sidecar':{'path':str(side.relative_to(root)),'sha256':'0'*64}}
            creation={'method':'synthetic_test','prompt':'fixture only','settings':{},'inputs':[{**asset['canonical'],'role':'canonical_identity','authority':'identity_anatomy_material_palette'}]}
            av.write(receipt,creation)
            v['creation']={**creation,'receipt':{'path':'receipt.json','sha256':av.digest(receipt)}}
            v['status']='candidate_pending_owner_review'
            def save_side():
                av.write(side,dict(asset_id=aid,revision='r001',variant='contact',image_sha256=v['file']['sha256'],canonical=asset['canonical'],creation=v['creation'],status=v['status'],owner_decision=v['owner_decision']))
                v['file']['sidecar']['sha256']=av.digest(side)
            save_side();self.assertEqual(cp.validate(lib,plan,chars,root),[])
            self.assertEqual(cp.usage_report(lib,plan)['counts']['actual_generated_performance_candidates'],1)
            v['status']='owner_selected_for_performance';save_side()
            self.assertTrue(any('owner decision' in e for e in cp.validate(lib,plan,chars,root)))
            ledger={'asset_id':aid,'revision':'r001','variant':'contact','sha256':v['file']['sha256'],'canonical_sha256':asset['canonical']['sha256'],'reviewer':'project_owner','scope':'performance_use_only','statement':'Synthetic test selection'}
            av.write(root/'decision.json',{'decisions':{aid+':contact':ledger}})
            v['owner_decision']={**ledger,'record':{'path':'decision.json','sha256':av.digest(root/'decision.json')}}
            save_side()
            self.assertEqual(cp.validate(lib,plan,chars,root),[])
            self.assertEqual(cp.usage_report(lib,plan)['counts']['actual_scene_images_approved_by_this_library'],0)
            for mutate in [lambda candidate:candidate['file']['sidecar'].update(path='wrong.json'),
                           lambda candidate:candidate['file'].update(dimensions=[21,20]),
                           lambda candidate:candidate['file']['alpha'].update(has_alpha=False),
                           lambda candidate:candidate['owner_decision'].update(scope='scene_approval'),
                           lambda candidate:candidate['creation']['inputs'][0].update(path='../escape.png')]:
                invalid=copy.deepcopy(lib);mutate(invalid['assets'][aid]['variants']['contact'])
                self.assertTrue(cp.validate(invalid,plan,chars,root))
            path.write_bytes(b'changed');self.assertTrue(cp.validate(lib,plan,chars,root))
            v['file']['path']='../escape.png';self.assertTrue(cp.validate(lib,plan,chars,root))

    def test_synthetic_layer_root_and_protected_background(self):
        import numpy as np
        background=Image.new('RGBA',(40,30),(20,80,40,255));actor=Image.new('RGBA',(10,10));ImageDraw.Draw(actor).rectangle((3,1,7,9),fill=(120,90,60,255))
        recipe={'purpose':'synthetic_contract_test','uniform_scale':1,'translate_pixels':[12,10],'source_root_pixels':[5,9],'target_root_pixels':[17,19]}
        result,mask=cp.compose_synthetic_pilot(background,actor,recipe)
        outside=np.asarray(mask)==0
        self.assertTrue(np.array_equal(np.asarray(result)[outside],np.asarray(background)[outside]))
        self.assertFalse(np.array_equal(np.asarray(result),np.asarray(background)))
        recipe['target_root_pixels']=[18,19]
        with self.assertRaises(ValueError):cp.compose_synthetic_pilot(background,actor,recipe)
        recipe['purpose']='production'
        with self.assertRaises(ValueError):cp.compose_synthetic_pilot(background,actor,recipe)


if __name__=='__main__':unittest.main()
