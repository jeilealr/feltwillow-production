"""Real CPU V7 packet/tracker/FFmpeg integration; no legacy story manifests."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import wave

import numpy as np
from PIL import Image
from production import v7_dialogue as v
from feltwillow.mouth_tracking import TrackingError
from tests.test_portrait_qa import fixture as portrait_fixture


class DialogueFixture(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.width=self.height=96;self.count=17
        self.closed=np.random.default_rng(8).integers(40,210,(96,96,3),dtype=np.uint8)
        self.opened=self.closed.copy();self.opened[48:55,44:53]=20
        self.frames=np.stack([self.closed]*self.count)
        for name,frame in [('closed.png',self.closed),('open.png',self.opened)]:Image.fromarray(frame).save(self.root/name)
        self.source=self.root/'source.mp4'
        subprocess.run([v.ffmpeg_binary(),'-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','96x96','-r','8','-i','pipe:0','-an','-c:v','libx264','-crf','0','-pix_fmt','yuv444p',str(self.source)],input=self.frames.tobytes(),capture_output=True,check=True)
        receipt=dict(run_id='synthetic',runtime_sha256='runtime',shot='piece',width=96,height=96,frames=17,fps=8,output_sha256=v.digest(self.source),native_boundaries={k:dict(path=str(self.root/'closed.png'),sha256=v.digest(self.root/'closed.png')) for k in ('first','last')})
        self.source.with_suffix('.json').write_text(json.dumps(receipt))
        self.plan=dict(story='lion_and_mouse_v7',lines=[],visual_units={'portrait':dict(status='authored',composition='portrait',mouth_policy='dialogue_lipsync',audio_line_ids=['S01-L001'],visible_cast=['Milo'],camera_and_crop_lock='same-view')})
        self.add_line('S01-L001','MOUSE','Hello friend.')
        source_hash=v.digest(self.source)
        self.takes=dict(schema='feltwillow.sequence-takes.v1',story=self.plan['story'],run_id='synthetic',runtime_sha256='runtime',takes={'piece':dict(path=str(self.source),sha256=source_hash,owner_decision='selected',full_motion_review=dict(status='pass',reviewer='synthetic',output_sha256=source_hash,whole_clip_watched=True,joins_reviewed=True))})
        _,contract=portrait_fixture();contract['source_sha256']=source_hash
        self.mapping=dict(source_piece='piece',frame_count=17,width=96,height=96,fps=8,sample_rate=24000,frame_scene_samples=[n*3000 for n in range(17)],actor='Milo',view='three_quarter',camera_and_crop_lock='same-view',boundary_mouth='closed',allowed_mouth_motion_roi=[.3,.3,.7,.65],calibration_id='mouth',portrait_contract=contract,source_review=dict(source_sha256=source_hash,status='pass',reviewer='synthetic',closed_boundaries=True,teeth_absent=True,whole_clip_watched=True,portrait_no_intrusion=True))
        self.refresh_mapping_review()
        refs={key:dict(path=path,sha256=v.digest(self.root/path)) for key,path in [('closed_base','closed.png'),('open_candidate','open.png')]}
        review=dict(reviewer='synthetic',closed_sha256=refs['closed_base']['sha256'],open_sha256=refs['open_candidate']['sha256'])
        self.calibrations={'mouth':dict(actor='Milo',purpose='speech_calibration',view='three_quarter',camera_and_crop_lock='same-view',no_teeth_design=True,**refs,mouth_roi_normalized=[.44,.48,.57,.59],owner_selection=dict(review,status='selected',scope='mouth_calibration'),anatomy_review=dict(review,status='pass'))}
        self.alignments={'S01-L001':self.alignment(self.plan['lines'][0])}

    def add_line(self,lid,speaker,text):
        wav=self.root/(lid+'.wav');meta=self.root/(lid+'.json')
        with wave.open(str(wav),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(b'\0\0'*48000)
        meta.write_text(json.dumps(dict(text=text,speaker=speaker)))
        self.plan['lines'].append(dict(line_id=lid,audio_scene='S01',speaker=speaker,text=text,audio=dict(wav=wav.name,sha256=v.digest(wav),metadata=meta.name,metadata_sha256=v.digest(meta),sample_count=48000,sample_rate_hz=24000)))

    def alignment(self,line):
        return dict(status='reviewed',reviewer='synthetic',audio_sha256=line['audio']['sha256'],metadata_sha256=line['audio']['metadata_sha256'],transcript=line['text'],speaker=line['speaker'],sample_rate=24000,words=[dict(text='Hello',start_sample=3000,end_sample=15000),dict(text='friend',start_sample=24000,end_sample=42000)])

    def refresh_mapping_review(self):
        self.mapping['review']=dict(status='reviewed',reviewer='synthetic',source_sha256=v.digest(self.source),frame_mapping_sha256=v.fingerprint(self.mapping['frame_scene_samples']),audio_sha256s={l['line_id']:l['audio']['sha256'] for l in self.plan['lines']})

    def compile(self):return v.compile_dialogue(self.plan,'portrait',self.takes,self.calibrations,self.alignments,self.mapping,self.root)

    def test_v7_compile_real_tracking_apply_and_immutable_output(self):
        packet=self.compile();out,report=v.process_frames(packet,self.frames,self.root)
        active=np.asarray(report['activation'])>0
        self.assertTrue(active.any());self.assertTrue(np.any(out[active]!=self.frames[active]))
        self.assertTrue(np.array_equal(out[~active],self.frames[~active]))
        self.assertTrue(np.array_equal(out[[0,-1]],self.frames[[0,-1]]))
        roi=v.region_mask(self.closed.shape,self.mapping['allowed_mouth_motion_roi'])
        self.assertTrue(np.array_equal(out[:,~roi],self.frames[:,~roi]))
        receipt=v.apply_packet(packet,self.root,self.root/'result',frames=self.frames)
        self.assertEqual('pending',receipt['owner_selection']);self.assertFalse(receipt['assembly_authorized'])
        self.assertEqual(receipt,v.apply_packet(packet,self.root,self.root/'result',frames=self.frames))
        self.assertFalse((self.root/'prompt_manifest.json').exists());self.assertFalse((self.root/'timing_plan.json').exists())

    def test_narrator_passes_through_without_alignment_or_calibration(self):
        line=self.plan['lines'][0];line['speaker']='NARRATOR';meta=self.root/line['audio']['metadata'];meta.write_text(json.dumps(dict(text=line['text'],speaker='NARRATOR')));line['audio']['metadata_sha256']=v.digest(meta)
        self.plan['visual_units']['portrait']['mouth_policy']='no_mouth_driver'
        self.calibrations={};self.alignments={};packet=self.compile();out,report=v.process_frames(packet,self.frames,self.root)
        self.assertEqual([],packet['cues']);self.assertTrue(np.array_equal(out,self.frames));self.assertEqual([0.]*17,report['activation'])

    def test_cross_line_gap_and_narrator_exclusion(self):
        self.add_line('S01-L002','NARRATOR','Then he waited.')
        self.plan['visual_units']['portrait']['audio_line_ids'].append('S01-L002')
        self.mapping['frame_scene_samples']=[n*6000 for n in range(17)];self.refresh_mapping_review()
        packet=self.compile();values=v.activations(packet)
        self.assertEqual(64800,packet['audio'][1]['scene_start_sample'])
        self.assertTrue(all(value==0 for n,value in enumerate(values) if self.mapping['frame_scene_samples'][n]>=48000))
        self.assertEqual('narrator_never_drives_mouth',packet['exclusions'][0]['reason'])

    def test_stale_audio_metadata_source_and_packet_rejected(self):
        packet=self.compile()
        for key in ('wav','metadata'):
            p=self.root/packet['audio'][0][key]['path'];old=p.read_bytes();p.write_bytes(old+b'changed')
            with self.assertRaises(ValueError):v.validate_packet(packet,self.root)
            p.write_bytes(old)
        bad=copy.deepcopy(packet);bad['cues'][0]['text']='wrong'
        with self.assertRaisesRegex(ValueError,'changed after'):v.validate_packet(bad,self.root)
        old=self.source.read_bytes();self.source.write_bytes(old+b'changed')
        with self.assertRaises(ValueError):v.validate_packet(packet,self.root)

    def test_calibration_view_roi_hash_and_teeth_fail(self):
        for key,value in [('view','profile'),('no_teeth_design',False),('mouth_roi_normalized',[0,0,0,1])]:
            saved=self.calibrations['mouth'][key];self.calibrations['mouth'][key]=value
            with self.assertRaises(ValueError):self.compile()
            self.calibrations['mouth'][key]=saved
        im=self.opened.copy();im[0,0]=0;Image.fromarray(im).save(self.root/'open.png')
        c=self.calibrations['mouth'];c['open_candidate']['sha256']=v.digest(self.root/'open.png')
        for name in ('owner_selection','anatomy_review'):c[name]['open_sha256']=c['open_candidate']['sha256']
        with self.assertRaisesRegex(ValueError,'outside mouth ROI'):self.compile()

    def test_open_boundary_intrusion_and_word_omission_fail(self):
        self.mapping['boundary_mouth']='open'
        with self.assertRaisesRegex(ValueError,'open dialogue boundary'):self.compile()
        self.mapping['boundary_mouth']='closed';self.mapping['source_review']['portrait_no_intrusion']=False
        with self.assertRaisesRegex(ValueError,'portrait_intrusion'):self.compile()
        self.mapping['source_review']['portrait_no_intrusion']=True;self.alignments['S01-L001']['words'].pop()
        with self.assertRaisesRegex(ValueError,'omits/reorders'):self.compile()

    def test_tracking_failure_never_falls_back(self):
        packet=self.compile();bad=self.frames.copy();bad[2]=0
        # Crop protection itself rejects before the muzzle tracker can hide a bad source.
        with self.assertRaisesRegex(ValueError,'portrait_intrusion/crop'):v.process_frames(packet,bad,self.root)
        packet['visual_unit']['composition']='body_or_interaction';packet.pop('packet_sha256');packet['packet_sha256']=v.fingerprint(packet)
        with self.assertRaises(TrackingError):v.process_frames(packet,bad,self.root)

    def test_take_without_whole_motion_or_stale_alignment_rejected(self):
        self.takes['takes']['piece']['full_motion_review']['joins_reviewed']=False
        with self.assertRaisesRegex(ValueError,'whole-motion/join'):self.compile()
        self.takes['takes']['piece']['full_motion_review']['joins_reviewed']=True
        self.alignments['S01-L001']['audio_sha256']='wrong'
        with self.assertRaisesRegex(ValueError,'stale/mismatched'):self.compile()

    def test_missing_visible_mouth_actor_cannot_silently_pass_through(self):
        self.mapping['actor']=None
        with self.assertRaisesRegex(ValueError,'explicit named mouth actor'):self.compile()

    def test_scene_offsets_reject_mixed_rate_arithmetic(self):
        self.add_line('S01-L002','MOUSE','Hello friend.')
        self.plan['lines'][1]['audio']['sample_rate_hz']=48000
        with self.assertRaisesRegex(ValueError,'mixed scene sample rates'):v.scene_offsets(self.plan,'S01')

    def test_real_cli_compile_apply_decode_path_without_legacy_files(self):
        import contextlib
        import io
        story=self.root/'stories/lion_and_mouse_v7';story.mkdir(parents=True)
        (story/'audio_visual_plan.json').write_text(json.dumps(self.plan))
        for name,value in [('takes',self.takes),('calibrations',self.calibrations),('alignments',self.alignments),('mapping',self.mapping)]:
            (self.root/(name+'.json')).write_text(json.dumps(value))
        argv=['--root',str(self.root),'compile','--story','lion_and_mouse_v7','--unit','portrait']
        for name in ('takes','calibrations','alignments','mapping'):argv.extend(['--'+name,str(self.root/(name+'.json'))])
        argv.extend(['--out',str(self.root/'packet.json')])
        with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(0,v.main(argv))
        with contextlib.redirect_stdout(io.StringIO()):self.assertEqual(0,v.main(['--root',str(self.root),'apply',str(self.root/'packet.json'),'--out',str(self.root/'cli-output')]))
        receipt=json.loads((self.root/'cli-output/dialogue_receipt.json').read_text())
        self.assertTrue(receipt['raw_boundary_frames_pixel_identical'])
        self.assertEqual('pending',receipt['post_sync_review'])
        self.assertTrue((self.root/'cli-output/dialogue.mp4').is_file())

    def test_cli_inventory_library_without_mouth_registry_is_honestly_empty(self):
        import contextlib
        import io
        story=self.root/'stories/lion_and_mouse_v7';story.mkdir(parents=True)
        (story/'audio_visual_plan.json').write_text(json.dumps(self.plan))
        (story/'character_performance_library.json').write_text(json.dumps(dict(schema='test-performance',assets={})))
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):self.assertEqual(0,v.main(['--root',str(self.root),'inventory','--story','lion_and_mouse_v7']))
        result=json.loads(stream.getvalue())
        self.assertEqual([],result['units'][0]['calibration_ids'])
        self.assertEqual('pending',result['video_review'])
