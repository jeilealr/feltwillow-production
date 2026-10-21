"""Local CPU regressions for semantic planning; no provider or GPU calls."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
import wave

from production import audio_visual_plan as av
from production import paired_images

ROOT=Path(__file__).resolve().parents[1]
STORY='lion_and_mouse_v7'


class AudioVisualPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder,cls.plan,cls.chars,cls.locs=av.load(ROOT,STORY)

    def line(self,lid,plan=None):
        return next(l for l in (plan or self.plan)['lines'] if l['line_id']==lid)

    def check(self,plan=None,locs=None):
        return av.validate(plan or self.plan,self.chars,locs or self.locs)

    def test_scene_composition_receipts_and_audio_links(self):
        manifest=json.loads((self.folder/'scene_composition_candidates.json').read_text())
        self.assertEqual(manifest['submitted_requests'],24)
        self.assertEqual(manifest['automatic_retries'],0)
        images=manifest['images']
        self.assertEqual(len(images),24)
        self.assertEqual(len({i['line_id'] for i in images}),18)
        for image in images:
            self.assertEqual(image['audio_sha256'],self.line(image['line_id'])['audio']['sha256'])
            self.assertTrue(Path(image['path']).name.startswith(image['image_id']))
            self.assertEqual(image['status'],'candidate_pending_owner_review')
            self.assertIsNone(image['owner_approval'])
            self.assertEqual(av.digest(ROOT/image['sidecar']['path']),image['sidecar']['sha256'])
            if (ROOT/image['path']).exists():
                self.assertEqual(av.digest(ROOT/image['path']),image['sha256'])

    def test_derived_index_keeps_preview_scope_separate(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);(folder/'derived').mkdir()
            source=self.folder/'scene_composition_candidates.json'
            (folder/source.name).write_text(source.read_text())
            av.derive(folder,self.plan,self.chars,self.locs)
            index=json.loads((folder/'derived/audio_image_index.json').read_text())
            previews=[i for i in index['associations'] if i.get('scope')=='representative_scene_composition_only']
            self.assertEqual(len(previews),24)
            self.assertEqual(av.summary(self.plan,self.locs)['approved_scene_images'],0)

    def test_planning_with_only_placeholders_is_valid(self):
        self.assertEqual(self.check(),[])
        self.assertEqual(av.summary(self.plan,self.locs)['generated_images'],0)
        for line in self.plan['lines']:
            for beat in line['beats']:
                self.assertTrue(all(i['status']=='planned' for i in beat['image_sequence']['images']))

    def test_local_current_audio_exact_coverage(self):
        audio_root=ROOT/self.plan['audio_source']['root']
        if not list((audio_root/'lines').glob('*.wav')):
            self.skipTest('ignored local WAVs not restored; synthetic audio cases still run')
        actual,errors=av.inventory_audio(ROOT,self.plan['audio_source']['root'],set(self.plan['script_line_order']))
        self.assertEqual(errors,[])
        current=[l['line_id'] for l in self.plan['lines'] if l['audio']['status']=='available_in_r001']
        self.assertEqual(len(current),len(set(current)))
        self.assertEqual(set(current),set(actual))
        self.assertEqual(av.validate(self.plan,self.chars,self.locs,ROOT),[])
        # Recorded future lines have exact audio provenance but no invented visual beats.
        self.assertEqual(len(current),161)
        self.assertEqual({i[:3] for i in current},{f'S{i:02d}' for i in range(1,17)})

    def test_future_audio_honesty(self):
        backlog=[l for l in self.plan['lines'] if int(l['audio_scene'][1:])>=13]
        self.assertEqual(len(backlog),63)
        self.assertTrue(all(l['text'] and not l['beats'] and l['audio']['duration_seconds']>0 and l['planning_status']=='pending_visual_authoring' for l in backlog))
        for field,value in [('duration_seconds',None),('sha256',None)]:
            plan=copy.deepcopy(self.plan);self.line('S13-L001',plan)['audio'][field]=value
            self.assertTrue(self.check(plan))
        # Missing future audio still cannot masquerade as a timed recording.
        plan=copy.deepcopy(self.plan);line=self.line('S13-L001',plan)
        line['audio']={'status':'not_available_in_r001','revision':'r001','wav':None,'metadata':None,'duration_seconds':None,'sha256':None,'metadata_sha256':None}
        line['planning_status']='pending_audio_visual_authoring'
        self.assertEqual(self.check(plan),[])
        line['audio']['duration_seconds']=5
        self.assertTrue(self.check(plan))

    def test_duplicate_missing_unknown_line_rejected(self):
        for mutate in [lambda p:p['lines'].pop(0),lambda p:p['lines'].append(copy.deepcopy(p['lines'][0])),lambda p:p['lines'][0].update(line_id='S99-L001')]:
            plan=copy.deepcopy(self.plan);mutate(plan)
            self.assertTrue(self.check(plan))

    def test_one_to_many_and_owner_scene_one(self):
        line=self.line('S01-L002');self.assertEqual(len(line['beats']),3)
        for token,beat in zip(['berry bush','hollow log','winding path'],line['beats']):
            self.assertIn(token,beat['semantic_span'])
            self.assertEqual(beat['location_family'],'peaceful_forest')
        line=self.line('S01-L004')
        self.assertEqual(len(line['beats']),3)
        for token,beat in zip(['seeds','berries','acorn'],line['beats']):self.assertIn(token,beat['semantic_span'])
        self.assertEqual(line['beats'][-1]['image_sequence']['mode'],'multi_key')
        self.assertTrue(all(b['location_family']=='peaceful_forest' for l in self.plan['lines'] if l['audio_scene']=='S01' for b in l['beats']))

    def test_portraits_and_route_decision(self):
        for lid in ['S02-L003','S03-L009']:
            b=self.line(lid)['beats'][0]
            self.assertEqual(b['shot_type'],'portrait');self.assertEqual(b['transition_in'],'portrait_cut')
            self.assertIn('blur',str(self.locs['views'][b['location_view']]).lower())
        beats=[self.line(f'S03-L00{i}')['beats'][0] for i in range(1,9)]
        self.assertEqual(len({b['continuity_group'] for b in beats}),1)
        self.assertIsNotNone(beats[0]['continuity_group'])
        self.assertNotEqual(beats[-1]['continuity_group'],self.line('S03-L009')['beats'][0]['continuity_group'])

    def test_sleeping_details_and_four_phase_landing(self):
        for i in range(1,5):
            b=self.line(f'S05-L00{i}')['beats'][0]
            self.assertFalse(self.plan['world_states'][b['state_out']]['actors']['Leo']['awake'])
            self.assertEqual(b['shot_type'],'establishing' if i==1 else 'detail')
            if i>1:self.assertEqual(b['transition_in'],'detail_cut')
        seq=self.line('S05-L009')['beats'][0]['image_sequence']
        self.assertEqual(seq['mode'],'multi_key');self.assertEqual(len(seq['images']),4)
        poses=[self.plan['world_states'][i['state']]['actors']['Milo']['pose'] for i in seq['images']]
        self.assertEqual(poses,['support_lost','tumbling','rolling','landed_surprised'])

    def test_all_sequence_contracts_and_role_rejection(self):
        modes={b['image_sequence']['mode'] for l in self.plan['lines'] for b in l['beats']}
        self.assertEqual(modes,av.MODES)
        for mode in modes:
            plan=copy.deepcopy(self.plan)
            b=next(b for l in plan['lines'] for b in l['beats'] if b['image_sequence']['mode']==mode)
            b['image_sequence']['images'][0]['role']='invalid'
            self.assertTrue(self.check(plan),mode)
        plan=copy.deepcopy(self.plan);b=self.line('S05-L009',plan)['beats'][0]
        b['image_sequence']['images']=b['image_sequence']['images'][:2]
        self.assertTrue(self.check(plan))

    def test_no_equal_window_requirement_or_fake_alignment(self):
        for b in self.line('S01-L004')['beats']:
            self.assertEqual(b['timing']['status'],'pending_alignment')
            self.assertIsNone(b['timing']['start_seconds']);self.assertIsNone(b['timing']['end_seconds'])
        plan=copy.deepcopy(self.plan);self.line('S01-L004',plan)['beats'][0]['timing']['start_seconds']=0
        self.assertTrue(self.check(plan))
        plan=copy.deepcopy(self.plan)
        for b in self.line('S01-L004',plan)['beats']:
            b['timing'].update(status='reviewed_alignment',start_seconds=0,end_seconds=1,evidence='fixture-reviewed')
        self.assertTrue(any('gap/overlap' in e for e in self.check(plan)))

    def test_cuts_do_not_implicitly_share_and_continuity_needs_group(self):
        b=self.line('S01-L002')['beats'][0]
        self.assertIsNone(b['continuity_group']);self.assertEqual(b['transition_in'],'cut')
        self.assertFalse(any(i.get('reuse_of') for i in b['image_sequence']['images']))
        plan=copy.deepcopy(self.plan);a=self.line('S01-L001',plan)['beats'][-1];b=self.line('S01-L002',plan)['beats'][0]
        a['transition_out']=b['transition_in']='shared_boundary'
        self.assertTrue(any('explicit common group' in e or 'independent scene' in e for e in self.check(plan)))
        plan=copy.deepcopy(self.plan);b=self.line('S11-L002',plan)['beats'][0]
        b['image_sequence']['images'][0]['reuse_of']=None
        self.assertTrue(any('explicitly reuse' in e for e in self.check(plan)))

    def test_world_persists_offscreen_and_events_are_causal(self):
        for l in self.plan['lines']:
            if l['audio_scene']=='S12':
                for b in l['beats']:
                    self.assertIn('Leo',b['offscreen_cast'])
                    self.assertEqual(self.plan['world_states'][b['state_out']]['props']['net']['phase'],'settled')
        plan=copy.deepcopy(self.plan);b=self.line('S12-L004',plan)['beats'][0];b['state_in']=plan['initial_world_state']
        self.assertTrue(any('cut reset' in e for e in self.check(plan)))
        plan=copy.deepcopy(self.plan)
        e=next(e for e in plan['world_events'].values() if e['kind']=='trigger_press')
        e['kind']='arbitrary_reset'
        self.assertTrue(self.check(plan))
        plan=copy.deepcopy(self.plan);b=self.line('S10-L004',plan)['beats'][0]
        plan['world_states'][b['state_out']]['actors']['Leo']['paw']='airborne'
        self.assertTrue(self.check(plan))

    def test_location_families_views_and_immutable_masters(self):
        self.assertGreater(sum(v['family_id']=='stream_bank' for v in self.locs['views'].values()),3)
        old=av.read(self.folder/'history/pre_audio_line_visual_2026-10-19/location_library.json')
        for master in old['locations']:
            v=self.locs['views'][master['id']]
            self.assertEqual(v['source'],dict(path=master['path'],sha256=master['sha256']))
        plan=copy.deepcopy(self.plan);self.line('S01-L002',plan)['beats'][0]['location_family']='invented'
        self.assertTrue(self.check(plan))

    def test_narrator_and_dialogue_pipeline_separate(self):
        plan=copy.deepcopy(self.plan);self.line('S01-L001',plan)['beats'][0]['dialogue']['mouth_driver']='Milo'
        self.assertTrue(any('narration' in e for e in self.check(plan)))
        plan=copy.deepcopy(self.plan);self.line('S02-L003',plan)['beats'][0]['dialogue']['mode']='narrator_voiceover'
        self.assertTrue(self.check(plan))
        plan=copy.deepcopy(self.plan);self.line('S02-L003',plan)['beats'][0]['dialogue']['boundary_mouth']='open'
        self.assertTrue(self.check(plan))

    def test_causal_prerequisites_for_net_and_future_rope_release(self):
        state=copy.deepcopy(self.plan['world_states'][self.plan['initial_world_state']])
        event=dict(kind='net_drop', changes=[dict(path='props.net.phase', before='suspended', after='falling')])
        with self.assertRaisesRegex(ValueError,'causal prerequisite'):
            av.apply_event(state,event,self.plan['state_rules'])
        state['props']['trigger']['phase']='pressed'
        self.assertEqual(av.apply_event(state,event,self.plan['state_rules'])['props']['net']['phase'],'falling')
        state['props']['net']['phase']='settled'
        event=dict(kind='net_open',changes=[dict(path='props.net.phase',before='settled',after='opened')])
        with self.assertRaisesRegex(ValueError,'causal prerequisite'):
            av.apply_event(state,event,self.plan['state_rules'])
        state['props']['rope']['phase']='parted'
        self.assertEqual(av.apply_event(state,event,self.plan['state_rules'])['props']['net']['phase'],'opened')

    def test_ids_cast_provenance_and_view_status_are_checked(self):
        for key,value in [('id','S01-L002-B09'),('cast',['Unknown']),('transition_in','cut or pose change; pending')]:
            plan=copy.deepcopy(self.plan);self.line('S01-L002',plan)['beats'][0][key]=value
            self.assertTrue(self.check(plan))
        locs=copy.deepcopy(self.locs)
        view=next(v for v in locs['views'].values() if v['status']=='planned')
        view['approval']={'status':'approved'}
        self.assertTrue(self.check(locs=locs))
        plan=copy.deepcopy(self.plan);self.line('S01-L001',plan)['audio']['duration_seconds']=0
        self.assertTrue(self.check(plan))

    def test_owner_normal_shots_before_first_background_lock(self):
        for lid in ['S03-L001','S03-L002','S03-L003','S03-L004','S03-L005']:
            self.assertEqual(self.line(lid)['beats'][0]['image_sequence']['mode'],'pair')
        a=self.line('S03-L004')['beats'][0];b=self.line('S03-L005')['beats'][0]
        self.assertEqual(a['transition_out'],'cut')
        self.assertEqual(b['transition_in'],'cut')
        self.assertEqual(a['location_view'],b['location_view'])
        self.assertEqual(b['continuity_group'],'fork_decision')
        self.assertFalse(b['image_sequence']['images'][0].get('reuse_of'))
        for lid in ['S01-L003','S02-L002']:
            b=self.line(lid)['beats'][0]
            self.assertIsNone(b['continuity_group'])
            self.assertFalse(any(i.get('reuse_of') for i in b['image_sequence']['images']))

    def test_owner_acorn_has_contact_before_release(self):
        beats=self.line('S02-L004')['beats']
        self.assertEqual([b['image_sequence']['mode'] for b in beats],['pair','multi_key'])
        images=beats[1]['image_sequence']['images']
        key=self.plan['world_states'][images[1]['state']]['props']['acorn']
        end=self.plan['world_states'][images[2]['state']]['props']['acorn']
        self.assertEqual(key['owner'],'Milo')
        self.assertEqual(key['anchor'],'Milo_paws_at_stream_stone')
        self.assertEqual(end['owner'],'stone')

    def test_owner_rear_paw_and_scene_six_contract(self):
        trip=self.line('S05-L008')['beats'][0]
        state=self.plan['world_states'][trip['state_out']]
        self.assertEqual(state['actors']['Milo']['anchor'],'leo_rear_paw')
        self.assertEqual(state['actors']['Leo']['trip_obstacle_limb'],'rear_paw')
        self.assertEqual(state['actors']['Leo']['later_blocking_limb'],'front_paw')
        for line in self.plan['lines']:
            if line['audio_scene']=='S06':
                for b in line['beats']:
                    self.assertEqual(b['continuity_group'],'great_tree_block')
                    self.assertEqual(b['staging_continuity']['contract'],'great_tree_rear_paw_to_face_s05_s06')

    def test_prepared_pilot_is_bounded_unapproved_and_hash_bound(self):
        operation=av.read(self.folder/'review/NEXT_LOCATION_VIEW_OPERATION.json')
        self.assertEqual(operation['request_count'],3)
        self.assertEqual(operation['automatic_retries'],0)
        self.assertIsNone(operation['estimated_total_cost'])
        self.assertEqual(operation['status'],'prepared_pending_explicit_owner_batch_approval')
        self.assertEqual(operation['bindings']['audio_visual_plan_sha256'],av.digest(self.folder/'history/before_independent_opening_2026-10-19/audio_visual_plan.json'))
        receipt=av.read(self.folder/'review/location_views/pilot_r001/operation.json')
        self.assertEqual(receipt['proposal_sha256'],av.digest(self.folder/'review/NEXT_LOCATION_VIEW_OPERATION.json'))
        self.assertEqual(receipt['operation']['bindings'],operation['bindings'])
        self.assertEqual(receipt['submitted_request_count'],3)
        # Registering generated candidates changes the live library after preflight.
        self.assertEqual(receipt['status'],'completed_three_of_three_owner_approved')
        for request in operation['requests']:
            self.assertIn('No characters',request['arguments']['prompt'])
            for source in request['inputs']:
                self.assertEqual(av.digest(ROOT/source['path']),source['sha256'])

    def test_audio_linked_filename_contract(self):
        self.assertEqual(av.image_filename('S01-L002-B01','berry_world'),
            'S01-L002-B01_location_berry_world_r001_candidate.png')
        self.assertEqual(av.image_filename('S01-L002-B03','path',2,image_id='S01-L002-B03-I02',role='end'),
            'S01-L002-B03-I02_end_path_r002_candidate.png')
        for args,kwargs in [(('arbitrary','path'),{}),(('S01-L002-B01','Bad Subject'),{}),
                (('S01-L002-B01','path',0),{}),(('S01-L002-B01','path'),{'role':'start'}),
                (('S01-L002-B01','path'),{'image_id':'S01-L003-B01-I01','role':'start'})]:
            with self.assertRaises(ValueError):av.image_filename(*args,**kwargs)

    def test_generated_locations_keep_audio_links_and_candidate_scope(self):
        self.assertEqual(av.candidate_errors(self.plan,self.locs),[])
        candidates=[c for v in self.locs['views'].values() for c in v.get('candidates',[])]
        pilot=[c for c in candidates if c['primary_beat_id'].startswith('S01-L002-')]
        self.assertEqual(len(pilot),3)
        for c in pilot:
            self.assertEqual(c['audio_links'][0]['line_id'],'S01-L002')
            self.assertEqual(c['audio_links'][0]['wav'],self.line('S01-L002')['audio']['wav'])
            self.assertEqual(c['status'],'owner_approved')
            self.assertEqual(c['owner_approval']['image_sha256'],c['sha256'])
        for mutate in [lambda c:c.update(path='unrelated.png'),
                lambda c:c['audio_links'][0].update(wav='other.wav'),
                lambda c:c.update(primary_beat_id='S99-L001-B01'),
                lambda c:c['sidecar'].update(path='unrelated.json'),
                lambda c:c.update(owner_approval={'approved':True})]:
            locs=copy.deepcopy(self.locs)
            c=next(c for v in locs['views'].values() for c in v.get('candidates',[]))
            mutate(c)
            self.assertTrue(av.candidate_errors(self.plan,locs))

    def test_candidate_sidecar_bytes_are_hash_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);locs=copy.deepcopy(self.locs)
            for view in locs['views'].values():
                for c in view.get('candidates',[]):
                    view.update(status='planned',source=None,approval=None)
                    c.update(status='candidate_pending_owner_review',owner_approval=None)
                    im=root/c['path'];im.parent.mkdir(parents=True,exist_ok=True);im.write_bytes(b'fixture image')
                    c['sha256']=av.digest(im)
                    side=root/c['sidecar']['path']
                    av.write(side,dict(audio_links=c['audio_links'],primary_beat_id=c['primary_beat_id'],image=dict(path=c['path'],sha256=c['sha256']),status=c['status'],owner_approval=None))
                    c['sidecar']['sha256']=av.digest(side)
            self.assertEqual(av.candidate_errors(self.plan,locs,root),[])
            side.write_text('{}')
            self.assertTrue(av.candidate_errors(self.plan,locs,root))

    def test_owner_location_approval_is_scoped_and_hash_bound(self):
        decision=av.read(self.folder/'location_view_acceptance.json')
        self.assertEqual(len(decision['views']),3)
        for vid,entry in decision['views'].items():
            view=self.locs['views'][vid]
            self.assertEqual(view['status'],'owner_approved_view')
            self.assertEqual(entry['owner_statement'],'yes they passed')
            self.assertEqual(entry['scope'],'location_view_only')
            self.assertEqual(view['source'],dict(path=entry['path'],sha256=entry['sha256']))
        self.assertEqual(av.summary(self.plan,self.locs)['owner_approved_location_views'],3)
        locs=copy.deepcopy(self.locs)
        view=next(v for v in locs['views'].values() if v['status']=='owner_approved_view')
        view['candidates'][0]['owner_approval']['image_sha256']='0'*64
        self.assertTrue(av.candidate_errors(self.plan,locs))

    def test_cut_sequence_secondary_view_is_in_audio_image_index(self):
        locs=copy.deepcopy(self.locs)
        view_id='peaceful_forest__seed_world_second_shot__afternoon'
        bid='S01-L004-B01';audio=self.line('S01-L004')['audio']
        locs['views'][view_id]['candidates']=[dict(primary_beat_id=bid,subject='seed_world_second_shot',
            image_revision=1,status='candidate_pending_owner_review',owner_approval=None,
            path=av.image_filename(bid,'seed_world_second_shot'),sha256='fixture',
            sidecar=dict(path='fixture.json',sha256='fixture'),
            audio_links=[dict(line_id='S01-L004',audio_revision='r001',
                **{k:audio[k] for k in ['wav','metadata','sha256','metadata_sha256']})])]
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);av.derive(folder,self.plan,self.chars,locs)
            rows=av.read(folder/'derived/audio_image_index.json')['associations']
            self.assertEqual(len([r for r in rows if r['location_view']==view_id]),1)
            row=next(r for r in rows if r['location_view']==view_id)
            self.assertEqual(row['line_id'],'S01-L004')
            self.assertEqual(row['beat_id'],bid)

    def test_independent_places_and_first_exact_background(self):
        for line in self.plan['lines']:
            if line['audio_scene'] in ['S01','S02'] and line['line_id'] not in ['S02-L001','S02-L004']:
                for b in line['beats']:
                    self.assertEqual(b['background_continuity'],'independent_scene')
                    v=self.locs['views'][b['location_view']]
                    self.assertEqual(v['reference_usage'],'style_and_material_only')
                    self.assertFalse(v['inherit_reference_geography'])
        group=self.plan['continuity_groups']['fork_decision']
        self.assertEqual(group['background_policy'],'exact_same_background')
        beats=[self.line(f'S03-L{i:03d}')['beats'][0] for i in range(1,9)]
        self.assertEqual(len({b['location_view'] for b in beats}),1)
        self.assertTrue(all(b['background_continuity']=='locked_background' for b in beats))
        self.assertEqual(self.plan['location_continuity_policy']['first_exact_background_line'],'S02-L001')
        plan=copy.deepcopy(self.plan);self.line('S03-L007',plan)['beats'][0]['location_view']='fork__decision_long_path__sunset'
        self.assertTrue(any('locked background' in e for e in self.check(plan)))

    def test_opening_compositions_cover_lines_without_stream_master(self):
        folder=self.folder/'review/scene_compositions/s01_s03_r001'
        operation=av.read(folder/'OPERATION.json')
        self.assertEqual(operation['request_count'],24)
        self.assertEqual(len({r['audio_line'] for r in operation['requests']}),18)
        self.assertEqual(operation['bindings']['audio_visual_plan_sha256'],av.digest(self.folder/'review/character_performance_consistency_r001/before_audio_visual_plan.json'))
        self.assertEqual(operation['bindings']['location_library_sha256'],av.digest(self.folder/'review/character_performance_consistency_r001/before_location_library.json'))
        locked=[]
        for req in operation['requests']:
            if req['background_continuity']=='independent_scene':
                self.assertFalse(any('/stream_bank/' in ref['path'] for ref in req['inputs']))
            if req['background_continuity']=='locked_background':
                locked.append(next(ref['sha256'] for ref in req['inputs'] if ref['role'].startswith('exact shared fork')))
        self.assertEqual(len(locked),3);self.assertEqual(len(set(locked)),1)

    def test_old_background_operation_is_superseded_assets_preserved(self):
        folder=self.folder/'review/location_views/remaining_81_r001'
        queue=av.read(folder/'QUEUE.json')
        self.assertTrue(queue['generation_hold'])
        self.assertEqual(queue['status'],'superseded_by_independent_opening_direction')
        preserved=av.read(self.folder/'derived/previous_image_assets.json')['images']
        self.assertEqual(len(preserved),9)
        self.assertEqual(len([r for r in preserved if r['status']=='owner_approved']),3)

    def test_runtime_candidates_are_derived_untimed_and_not_generated(self):
        intervals=av.future_intervals(self.plan)
        self.assertTrue(intervals)
        self.assertIsNone(intervals[0]['start_seconds'])
        self.assertEqual(len([i for i in intervals if i['beat_id']=='S05-L009-B01']),3)
        with self.assertRaisesRegex(ValueError,'Historical paired tool refuses'):paired_images.load_story(ROOT,STORY)


class AudioByteInventoryTests(unittest.TestCase):
    def fixture(self,root,lid='S01-L001'):
        directory=root/'audio/lines';directory.mkdir(parents=True)
        wav=directory/f'{lid}.wav'
        with wave.open(str(wav),'wb') as out:
            out.setparams((1,2,24000,0,'NONE','not compressed'));out.writeframes(b'\0\0'*12345)
        meta=dict(id=lid,scene=1,text='Exact test words.',speaker='NARRATOR',style='gentle',seconds=12345/24000,sha256=av.digest(wav))
        av.write(directory/f'{lid}.json',meta)
        return directory,meta

    def test_actual_sample_count_not_historical_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);directory,meta=self.fixture(root)
            actual,errors=av.inventory_audio(root,'audio',{'S01-L001'})
            self.assertEqual(errors,[]);self.assertEqual(actual['S01-L001']['sample_count'],12345)
            self.assertEqual(actual['S01-L001']['duration_seconds'],12345/24000)
            meta['seconds']=7;av.write(directory/'S01-L001.json',meta)
            self.assertTrue(av.inventory_audio(root,'audio',{'S01-L001'})[1])

    def test_hash_unpaired_unknown_and_missing_future(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);directory,meta=self.fixture(root)
            actual,errors=av.inventory_audio(root,'audio',{'S01-L001','S13-L001'})
            self.assertNotIn('S13-L001',actual);self.assertEqual(errors,[])
            meta['sha256']='0'*64;av.write(directory/'S01-L001.json',meta)
            self.assertTrue(av.inventory_audio(root,'audio',{'S01-L001'})[1])
            (directory/'S01-L001.json').unlink()
            self.assertIn('incomplete',str(av.inventory_audio(root,'audio',{'S01-L001'})[1]))
            self.assertIn('unknown',str(av.inventory_audio(root,'audio',set())[1]))


if __name__=='__main__':unittest.main()
