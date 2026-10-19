"""Paired-image CPU behavior regressions; no image generation or GPU imports."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image
from production import paired_images as p
from production import paired_review
from production.keyframe_plan import crop_for_frame
from feltwillow.version_policy import require_story_local_audio
from production.verify_audio_manifest import verify as verify_audio

ROOT=Path(__file__).resolve().parents[1]
STORY='lion_and_mouse_v7'


def setup():
    return {'crop_rect_norm':[0,0,1,1], 'output_size':[100,100],
            'support_zones':{'path':[0,0,1,1]},'allow_offscreen_support':False}


def calibration(neutral=40):
    return {'status':'owner_approved','neutral_equivalent_source_px':neutral,
            'source_support_px':[20,40], 'kind':'actor'}


def placement(x=.5,y=.8):
    return {'neutral_equivalent_plate_px':40,'support_xy_on_plate':[x,y],
            'support_surface':'path','depth_projection_scale':1}


class PairedImagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder,cls.plan,cls.chars,cls.locs=p.load_story(ROOT,STORY)

    def test_exact_import_refuses_changed_hash_and_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'source').write_bytes(b'canonical')
            ref={'path':'source','sha256':p.digest(root/'source'),'status':'owner_approved'}
            imported=p.import_canonical(root,ref,'v7/canonical')
            self.assertEqual((root/'v7/canonical').read_bytes(),b'canonical')
            self.assertEqual(imported['sha256'],ref['sha256'])
            for bad in [{**ref,'status':'candidate'},{**ref,'sha256':'0'*64}]:
                with self.assertRaises(ValueError):p.import_canonical(root,bad,'v7/bad')
            (root/'v7/canonical').write_bytes(b'changed')
            with self.assertRaises(ValueError):p.import_canonical(root,ref,'v7/canonical')

    def test_missing_source_names_exact_restore_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,'restore exact source.*123'):
                p.verify(tmp,{'path':'missing.png','sha256':'123'})

    def test_unapproved_atlas_is_not_identity_or_performance_authority(self):
        actor=self.chars['characters']['Milo']['canonical']
        plate=next(iter(self.locs['setups'].values()))
        refs=[{'role':'identity_root',**actor},{'role':'locked_plate',**plate['plate']},
              {'role':'pose',**actor,'status':'candidate'}]
        with self.assertRaisesRegex(ValueError,'unapproved'):
            p.check_references(ROOT,refs,self.chars,plate,['Milo'])

    def test_locked_camera_does_not_follow_actor(self):
        s=setup();s['crop_rect_norm']=[.25,.25,.5,.5]
        for x in [.4,.6]:
            self.assertEqual(crop_for_frame({'schema':p.SCHEMA,'actors':{'a':{'contact_xy_on_plate':[x,.8]}}},2,setup=s),[.25,.25,.5,.5])
        with self.assertRaises(ValueError):crop_for_frame({'schema':p.SCHEMA},2)

    def test_one_camera_transform_magnifies_every_world_layer(self):
        plate=Image.new('RGB',(100,100),(20,20,20))
        # Landmark is an exact patch in the master plate.
        for x in range(40,50):
            for y in range(40,50):plate.putpixel((x,y),(255,0,0))
        layer=Image.new('RGBA',(10,10),(0,255,0,255))
        cal=calibration(10);cal['source_support_px']=[0,0]
        pos=placement(.5,.5);pos['neutral_equivalent_plate_px']=10
        layers=[{'image':layer,'calibration':cal,'placement':pos}]
        wide=p.compose_master(plate,layers,setup())
        close_setup=setup();close_setup['crop_rect_norm']=[.25,.25,.5,.5]
        close=p.compose_master(plate,layers,close_setup)
        def area(im,channel):
            a=np.asarray(im);return int(((a[:,:,channel]>200)&(a[:,:,1-channel]<50)).sum())
        self.assertGreater(area(close,0),area(wide,0)*3)
        self.assertGreater(area(close,1),area(wide,1)*3)
        self.assertEqual(p.project([.5,.5],close_setup),[.5,.5])

    def test_pose_silhouette_never_sets_anatomical_scale(self):
        for visible_height in [40,30,20,12]:
            cal=calibration();cal['visible_silhouette_px']=visible_height
            self.assertEqual(p.calibrated_transform(cal,placement(),setup(),[100,100])['source_scale_in_master'],1)
        a=Image.new('RGBA',(40,40),(255,0,0,255))
        b=Image.new('RGBA',(40,20),(255,0,0,255))
        self.assertEqual(p.calibrated_transform(calibration(),placement(),setup(),[100,100])['source_scale_in_master'],1)
        self.assertNotEqual(a.height,b.height)

    def test_group_requires_each_internal_actor_scale_review(self):
        cal={**calibration(),'kind':'group','members':{'a':{'internal_scale_reviewed':True},'b':{}}}
        with self.assertRaisesRegex(ValueError,'internal actor scale'):
            p.calibrated_transform(cal,placement(),setup(),[100,100])

    def test_portrait_support_can_be_offscreen_but_not_in_water(self):
        s=setup();s.update(crop_rect_norm=[.25,.1,.5,.5],allow_offscreen_support=True)
        t=p.calibrated_transform(calibration(),placement(y=.9),s,[100,100])
        self.assertGreater(t['support_after_crop'][1],1)
        with self.assertRaises(ValueError):p.calibrated_transform(calibration(),placement(y=1.1),s,[100,100])
        s['support_zones']={'path':[0,.5,.4,1]}
        with self.assertRaisesRegex(ValueError,'walkable'):
            p.calibrated_transform(calibration(),placement(),s,[100,100])

    def test_movement_restores_vacated_plate_and_preserves_rope_holes(self):
        plate=Image.new('RGB',(100,100),(45,70,99))
        layer=Image.new('RGBA',(40,40),(255,0,0,255))
        for x in range(16,24):
            for y in range(16,24):layer.putpixel((x,y),(255,255,255,0))
        s=setup()
        first=p.compose_master(plate,[{'image':layer,'calibration':calibration(),'placement':placement(.3)}],s)
        last=p.compose_master(plate,[{'image':layer,'calibration':calibration(),'placement':placement(.8)}],s)
        self.assertEqual(last.getpixel((25,60)),plate.getpixel((25,60)))
        self.assertEqual(first.getpixel((30,60)),plate.getpixel((30,60)))
        mask=Image.new('L',(100,100),0)
        for x in range(5,100):
            for y in range(35,85):mask.putpixel((x,y),255)
        self.assertTrue(p.protected_difference(first,last,mask)['pass'])
        last.putpixel((0,0),(0,0,0))
        self.assertFalse(p.protected_difference(first,last,mask)['pass'])

    def test_invalid_crop_light_identity_scale_and_airborne_shadow_reject(self):
        a={'setup_id':'one','crop_rect_norm':[0,0,1,1],'output_size':[100,100], 'lighting':'day',
           'identity_hashes':{'a':'123'},'actors':{'a':{'pose_calibration_id':'stand','support_valid':True,
           'neutral_equivalent_plate_px':40,'depth_projection_scale':1,'support':'ground','anatomy_measurements':{'head_px':10}}}}
        self.assertEqual(paired_review.geometry_errors(a,a,[]),[])
        for key,val in [('setup_id','two'),('lighting','night'),('crop_rect_norm',[0,0,.5,.5]),('identity_hashes',{'a':'456'})]:
            b=copy.deepcopy(a);b[key]=val
            self.assertTrue(paired_review.geometry_errors(a,b,[]))
        b=copy.deepcopy(a);b['actors']['a']['neutral_equivalent_plate_px']=80
        self.assertTrue(paired_review.geometry_errors(a,b,[]))
        b=copy.deepcopy(a);b['actors']['a'].update(support='airborne',planted_contact_shadow=True)
        self.assertTrue(paired_review.geometry_errors(a,b,[]))

    def test_shared_endpoints_and_camera_cuts_preserve_state(self):
        self.assertFalse(p.validate(self.plan,self.chars,self.locs))
        for kind,field in [('shared_boundary','start_image'),('camera_cut','start_state')]:
            plan=copy.deepcopy(self.plan)
            target=next(x for x in plan['pieces'] if x['handoff']['type']==kind)
            target[field]=plan['pieces'][-1]['end_image' if field=='start_image' else 'end_state']
            self.assertTrue(p.validate(plan,self.chars,self.locs))

    def test_offscreen_trap_persists_and_release_requires_parted_rope(self):
        for piece in self.plan['pieces']:
            if piece['audio_scene']==12:
                self.assertEqual(self.plan['states'][piece['start_state']]['props']['net'],'settled')
                self.assertIn('Leo',piece['offscreen_cast'])
        plan=copy.deepcopy(self.plan)
        part=next(x for x in plan['pieces'] if x['event']=='part');part['event']='nod'
        self.assertTrue(any('causal event' in e for e in p.validate(plan,self.chars,self.locs)))
        plan=copy.deepcopy(self.plan)
        cut=next(x for x in plan['pieces'] if x['audio_scene']==12)
        plan['states'][cut['start_state']]['props']['net']='discarded'
        self.assertTrue(p.validate(plan,self.chars,self.locs))

    def test_prompt_visible_cast_portrait_and_no_teeth(self):
        for piece in self.plan['pieces']:
            packet=p.packet(self.plan,self.chars,self.locs,piece['id'],'start')
            prompt=packet['prompt']
            if piece['visible_cast']==['Milo']:
                self.assertNotIn('Leo',prompt)
            if piece['visible_cast']==['Leo']:
                self.assertNotIn('Milo',prompt)
            if self.locs['setups'][piece['setup_id']]['framing']=='portrait':
                self.assertNotIn('fully inside',prompt)
                self.assertIn('upper chest',prompt)
            if 'Milo' in piece['visible_cast']:
                self.assertIn('no visible teeth',prompt.lower().replace('never shows visible teeth','no visible teeth'))

    def test_audio_intervals_split_once_and_narrator_cannot_drive_lips(self):
        self.assertEqual(len(self.plan['audio_spans']),161)
        self.assertFalse(p.validate(self.plan,self.chars,self.locs))
        plan=copy.deepcopy(self.plan);plan['pieces'][0]['audio_intervals'][0]['start']+=.1
        self.assertTrue(any('gap or overlap' in e for e in p.validate(plan,self.chars,self.locs)))
        plan=copy.deepcopy(self.plan);plan['pieces'][0]['speaker']='NARRATOR'
        self.assertTrue(any('mouth speaker' in e for e in p.validate(plan,self.chars,self.locs)))

    def fixture(self,root):
        folder=root/'stories'/STORY;folder.mkdir(parents=True)
        for name in ['shot_plan.json','character_library.json','location_library.json','selection.json']:
            p.atomic_json(folder/name,p.read(self.folder/name))
        for c in self.chars['characters'].values():
            path=c['canonical']['path'];out=root/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((ROOT/path).read_bytes())
        piece=self.plan['pieces'][0]
        s=self.locs['setups'][piece['setup_id']]
        path=s['plate']['path'];out=root/path;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes((ROOT/path).read_bytes())
        image=root/'image.png';Image.new('RGB',tuple(s['output_size']),'red').save(image)
        packet=p.packet(self.plan,self.chars,self.locs,piece['id'],'start')
        packet.update(tool='mock_recorded_tool',request_id=None,seed=None,estimated_cost=None,actual_cost=None)
        return folder,piece,image,packet

    def test_registration_immutable_idempotent_atomic_and_scoped_invalidation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder,piece,image,provenance=self.fixture(root)
            eid=piece['start_image']
            receipt=p.register(root,STORY,eid,'r001',image,provenance)
            self.assertEqual(p.register(root,STORY,eid,'r001',image,provenance),receipt)
            Image.new('RGB',(1536,864),'blue').save(image)
            with self.assertRaisesRegex(ValueError,'immutable'):p.register(root,STORY,eid,'r001',image,provenance)
            p.register(root,STORY,eid,'r002',image,provenance)
            selection=p.read(folder/'selection.json');selection['reviews']={'affected':{'endpoint_ids':[eid],'status':'reviewed'},'unrelated':{'endpoint_ids':['other'],'status':'reviewed'}}
            p.atomic_json(folder/'selection.json',selection)
            before=p.digest(folder/'selection.json')
            with patch('production.paired_images.os.replace',side_effect=OSError('interrupted transaction')):
                with self.assertRaises(OSError):p.select(root,STORY,eid,'r001',before)
            self.assertEqual(p.digest(folder/'selection.json'),before)
            chosen=p.select(root,STORY,eid,'r001',before)
            self.assertEqual(chosen['reviews']['affected']['status'],'stale')
            self.assertEqual(chosen['reviews']['unrelated']['status'],'reviewed')
            with self.assertRaisesRegex(ValueError,'selection changed'):p.select(root,STORY,eid,'r002',before)
            before=p.digest(folder/'selection.json')
            chosen=p.select(root,STORY,eid,'r002',before)
            self.assertEqual(chosen['endpoints'][eid]['revision'],'r002')

    def test_registration_rejects_stale_start_and_changed_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder,piece,image,prov=self.fixture(root)
            end=p.packet(self.plan,self.chars,self.locs,piece['id'],'end')
            end['ordered_references']=end['ordered_references'][1:]
            end.update(tool='test',start_sha256='wrong')
            with self.assertRaisesRegex(ValueError,'stale or unselected'):
                p.register(root,STORY,piece['end_image'],'r001',image,end)
            (root/prov['ordered_references'][0]['path']).write_bytes(b'wrong plate')
            with self.assertRaisesRegex(ValueError,'hash changed'):p.register(root,STORY,piece['start_image'],'r001',image,prov)
            self.assertFalse((folder/'candidates').exists())

    def test_wan_handoff_receives_both_images_and_same_preprocess(self):
        start=Image.new('RGB',(100,100),'red');end=Image.new('RGB',(100,100),'blue')
        seen=[]
        def fit(image,width,height):seen.append((image,width,height));return image.resize((width,height))
        inputs=p.wan_inputs(start,end,setup(),width=50,height=50,preprocess=fit)
        self.assertEqual(seen,[(start,50,50),(end,50,50)])
        def mock_wan(*,image,last_image):
            self.assertEqual(image.getpixel((0,0)),(255,0,0));self.assertEqual(last_image.getpixel((0,0)),(0,0,255))
        mock_wan(image=inputs['image'],last_image=inputs['last_image'])
        self.assertIsNone(inputs['actual_generated_first_last'])
        self.assertIn('@596658',inputs['model'])

    def test_image_only_does_not_need_audio_and_video_is_blocked(self):
        self.assertEqual(p.readiness(ROOT,STORY,'source'),[])
        blockers=p.readiness(ROOT,STORY,'video')
        self.assertTrue(any('restore exact source' in b and '.wav' in b for b in blockers))
        audio=p.read(self.folder/'audio_manifest.json')
        self.assertEqual(len(verify_audio(audio,STORY,root=ROOT)),177)
        with self.assertRaises(SystemExit):require_story_local_audio(STORY,'lion_and_mouse_v6')
        require_story_local_audio(STORY,STORY)


if __name__=='__main__':unittest.main()
