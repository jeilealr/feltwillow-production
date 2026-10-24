"""Apply S08 owner framing and prepare bounded performance foundations; no calls."""
import copy,hashlib,json,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4];S=R/'stories/lion_and_mouse_v7';F=S/'review/scene_compositions/s06_s07_background_scenes_r001';N=F.parent/'s07_milo_nervous_faces_r002'
def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p,**kw):return dict(path=str(p.relative_to(R)),sha256=sha(p),**kw)
def main():
 assert not (D/'OPERATION.json').exists();A=D/'owner_acceptance';A.mkdir()
 plan=read(S/'audio_visual_plan.json');before=copy.deepcopy(plan);lib=read(S/'character_performance_library.json');loc=read(S/'location_library.json')
 write(A/'before_audio_visual_plan.json',plan)
 # Select only the three newly reviewed Milo scenes. Reusable expression files
 # retain their existing scopes; scene edits do not silently replace them.
 protected=read(N/'PROTECTED_SCENES.json');selected=[]
 statement='they passed. continuw wil S08. I can only say that close up portraits will be L007 8 - 15, 19 - 24 . we can create the portratit and for the other scenes I will leave up to you to create the poses an dkeep banckground consistency and so on based on previous scenes'
 for row in protected['outputs']:
  assert sha(R/row['path'])==row['sha256'];selected.append({k:row[k] for k in ['image_id','path','sha256','image_revision']})
  selected[-1].update(reviewer='project_owner',scope='scene_depiction_only',statement=statement)
 ledger=A/'OWNER_SELECTION.json';write(ledger,{'images':selected,'count':3,'scope':'Only three S07 nervous Milo scenes; no new S08 approval'})
 current=read(F/'LOCAL_SCENES.json');registry=read(S/'scene_composition_candidates_s06_s07.json');changes=[]
 for row,decision in zip(protected['outputs'],selected):
  side=R/row['sidecar']['path'];assert sha(side)==row['sidecar']['sha256'];shutil.copy2(side,A/side.name);old=sha(side);data=read(side);approval=dict(decision,record=ref(ledger));data.update(status='owner_selected_scene_image',owner_approval=approval);write(side,data)
  row.update(status=data['status'],owner_approval=approval,sidecar=ref(side));changes.append({'path':str(side.relative_to(R)),'before_sha256':old,'after_sha256':sha(side)})
  for collection in [current['outputs'],registry['images']]:
   for item in collection:
    if item['image_id']==row['image_id'] and item['sha256']==row['sha256']:item.update(status=data['status'],owner_approval=approval,sidecar=ref(side))
 write(N/'PROTECTED_SCENES.json',protected);write(F/'LOCAL_SCENES.json',current);write(S/'scene_composition_candidates_s06_s07.json',registry);write(A/'REVIEW_CHANGES.json',changes)
 # New S08-specific face requirements inherit selected S07 upper-body geometry.
 bases={'Leo':'leo.s07.dialogue.portrait.3q','Milo':'milo.portrait.base.3q_left'}
 roles={'Leo':['thoughtful','softened','amused','reassuring','sky_hint'],'Milo':['surprised_relief','grateful','hopeful']}
 aids={}
 for actor,names in roles.items():
  for name in names:
   aid=actor.lower()+'.expression.s08.'+name+('.3q_left' if actor=='Milo' else '.3q');aids[actor,name]=aid
   template=copy.deepcopy(lib['assets']['milo.expression.sincere.3q_left' if actor=='Milo' else 'leo.expression.thoughtful.3q']);parent=lib['assets'][bases[actor]];f=parent['variants']['default']['file']
   template.update(id=aid,label='S08 '+name+'; same selected S07 portrait geometry',family_id=actor.lower()+'.s08.portrait.expressions',parents=[{'id':bases[actor],'revision':parent['revision'],'variant':'default','sha256':f['sha256'],'authority':'portrait_geometry_only'}],portrait_base={'id':bases[actor],'revision':parent['revision']})
   v=copy.deepcopy(template['variants']['default']);v.update(status='planned',file=None,owner_decision=None,creation=None);v.pop('candidate_review',None);template['variants']={'default':v};lib['assets'][aid]=template
 portrait_lines=set(range(7,16))|set(range(19,25));milo_portraits={12,19,20,21}
 # Nine non-portrait beats share one fixed S06 setup. Portrait cuts retain
 # persistent world states and reciprocal eyelines; no invented relocation.
 shared_view='great_tree__s06_joint_locked__dusk';shared_beats=[];matrix=[]
 for line in plan['lines']:
  if line['audio_scene']!='S08':continue
  n=int(line['line_id'][-3:]);portrait=n in portrait_lines;actor='Milo' if n in milo_portraits else 'Leo'
  for b in line['beats']:
   if portrait:
    b.update(cast=[actor],offscreen_cast=['Leo' if actor=='Milo' else 'Milo'],shot_type='portrait_close_up',background_continuity='same_place_new_view',continuity_group=None,camera_intent='Same selected S07 '+actor+' head/ears-or-mane/neck/shoulders/upper chest extent; fixed family crop and reciprocal eyeline; listener offscreen in same great-tree world')
    if n==10:
     b['action']='Leo gently gives permission in portrait; blocking front paw withdraws below crop, same declared release event; route clear afterward'
    if n==24:
     b['action']='Leo encouraging portrait shifts eyes toward darkening canopy; existing sky gesture occurs below crop, escape route remains clear'
   else:
    shared_beats.append(b['id']);b.update(cast=['Leo','Milo'],offscreen_cast=[],shot_type='two_character_medium_wide',background_continuity='locked_background',location_view=shared_view,continuity_group='great_tree_kindness_s08',camera_intent='Same S06 protected background/camera; Leo lying left, Milo screen-right grounded at same depth. Reveal restraint, trembling and kindness through readable acting; no actual anger scene.')
   for im in b['image_sequence']['images']:
    if portrait:
     old=im['performance'].get(actor)
     if old is None:old=copy.deepcopy(next(iter(im['performance'].values())))
     binding=copy.deepcopy(old);binding.update(pose_id=bases[actor],pose_variant='default',pose_revision='r001',pose_sha256=lib['assets'][bases[actor]]['variants']['default']['file']['sha256'],body_facing='screen_left' if actor=='Milo' else 'screen_right',head_orientation='left' if actor=='Milo' else 'forward_right',gaze_target='Leo screen-left/up' if actor=='Milo' else 'Milo screen-right/down',support='ground')
     if actor=='Milo':emotion='surprised_relief' if n==12 else 'hopeful' if n==21 else 'grateful'
     else:emotion='thoughtful' if n==7 and im['role']=='start' else 'softened' if n in [7,8] else 'amused' if n in [9,10] else 'sky_hint' if n==24 and im['role']=='end' else 'reassuring'
     binding.update(expression_id=aids[actor,emotion],expression_variant='default',expression_revision='r001',expression_sha256=None);im['performance']={actor:binding};im.pop('joint_performance_requirement',None)
     im['phase_intent']=b['action']+'; '+emotion+' facial acting, closed toothless boundary mouth'
    else:
     im['location_view']=shared_view
     # Keep existing per-actor requirements as planned dependencies; paired
     # references supplement them without falsely approving individual sprites.
     for a,binding in im['performance'].items():
      if a=='Milo':binding.update(body_facing='screen_left',head_orientation='left',gaze_target='Leo screen-left/up')
     if 'Milo' not in im['performance']:
      donor=next(x for l in before['lines'] if l['line_id']=='S08-L003' for bb in l['beats'] for x in bb['image_sequence']['images'])['performance']['Milo'];im['performance']['Milo']=copy.deepcopy(donor);im['performance']['Milo'].update(world_state_ref=im['state'],body_facing='screen_left',head_orientation='left')
     if 'Leo' not in im['performance']:
      donor=next(x for l in before['lines'] if l['line_id']=='S08-L003' for bb in l['beats'] for x in bb['image_sequence']['images'])['performance']['Leo'];im['performance']['Leo']=copy.deepcopy(donor);im['performance']['Leo']['world_state_ref']=im['state']
    matrix.append({'line_id':line['line_id'],'text':line['text'],'speaker':line['speaker'],'audio':line['audio'],'image_id':im['id'],'role':im['role'],'world_state':im['state'],'framing':'portrait '+actor if portrait else 'locked shared setup','action':b['action'],'performance':im['performance'],'generation_status':'planned; references/keys are not completed scenes'})
 plan['continuity_groups']['great_tree_kindness_s08']={'id':'great_tree_kindness_s08','beat_ids':shared_beats,'policy':'All nine non-portrait S08 lines revisit the same setup across portrait cuts; no camera/depth/actor-root drift. Leo stays lying. Front-paw release changes at L010 offscreen in portrait. Hypothetical anger is never enacted.','background_policy':'exact_same_background','locked_location_view':shared_view,'camera_policy':'locked_camera_crop','background_reference':ref(F/'S06-L001-B01_location_protected_clean_plate_r001_candidate.png'),'screen_axis':'Leo left, Milo screen-right facing up-left','phase_rule':'blocking paw persists through L009, route clear after declared L010 release event; never reuse blocked pair after release'}
 for view in loc['views'].values():
  for bid in list(view.get('used_by_beats',[])):
   if bid.startswith('S08-'):view['used_by_beats'].remove(bid)
 for line in plan['lines']:
  if line['audio_scene']=='S08':
   for b in line['beats']:
    view=loc['views'][b['location_view']]
    if b['id'] not in view['used_by_beats']:view['used_by_beats'].append(b['id'])
 assert plan['world_states']==before['world_states'] and plan['world_events']==before['world_events']
 assert [(l['line_id'],l['text'],l['audio']) for l in plan['lines']]==[(l['line_id'],l['text'],l['audio']) for l in before['lines']]
 write(S/'audio_visual_plan.json',plan);write(S/'character_performance_library.json',lib);write(S/'location_library.json',loc);write(D/'S08_SHOT_MAP.json',{'portrait_lines':sorted(portrait_lines),'interpretation':'L007, L008-L015 and L019-L024','images':matrix,'source_audio_unchanged':True,'world_states_events_unchanged':True})
 # First bounded stage: five portrait emotions + two paired action anchors.
 requests=[]
 for actor,name,acting in [
  ('Leo','thoughtful','Quietly considering the frightened mouse. Relax the questioning frown into thoughtful restraint, eyes down-right toward Milo, closed neutral mouth; not angry and not yet smiling warmly.'),
  ('Leo','softened','His expression has just softened: release brow tension, soften eyelids, a tiny kind closed-mouth lift. Warm, safe and patient rather than questioning or stern; eyes down-right toward Milo.'),
  ('Leo','reassuring','Calm reassuring kindness and quiet encouragement toward Milo down-right. Gentle brows and soft eyes, modest closed-mouth smile, no big grin, no teeth, no patronizing or menacing face.'),
  ('Milo','surprised_relief','Surprised that Leo is letting him go: inner brows rise with uncertain relief, eyes up-left toward Leo, closed lips gently relax. Transition from fear to cautious relief, not cheerful confidence or panic.'),
  ('Milo','grateful','Small sincere grateful expression toward Leo up-left: eased brows, warm attentive eyes and tiny closed-mouth thankful smile. He remains respectful and a little overwhelmed, not exuberant or smug.')]:
  base=lib['assets'][bases[actor]]['variants']['default']['file'];canon=lib['assets'][bases[actor]]['canonical'];anno=S/'review/character_performance_consistency_r001/canonical_measurements_r001'/('milo_combined_annotated.jpg' if actor=='Milo' else 'leo_combined_annotated.jpg')
  refs=[ref(R/base['path'],role='selected_portrait_edit_base',authority='head/ears-or-mane/neck/chest geometry and crop only'),dict(canon,role='canonical_identity',authority='identity/anatomy/material/palette'),ref(anno,role='canonical_measurement_annotation',authority='same-character visible surface measurements only; never render annotations')]
  prompt='Edit ONLY local facial acting of reference 1, the owner-selected '+actor+' portrait performance. '+acting+' Preserve exactly the same head pitch/yaw, skull/muzzle, eye size and spacing, ears/'+('mane curls' if actor=='Leo' else 'whiskers and cream muzzle')+', neck, shoulders and upper chest silhouette and visible extent, canvas and crop. Change brow/eyelid/cheek tension and closed mouth crease only. No head enlargement, tilt, zoom, body reconstruction, mirroring or separate body-part scaling. Canonical reference 2 controls identity and intrinsic felt palette; annotation reference 3 controls compatible visible proportions only, not markings. Preserve intrinsic color and felt texture. Genuine transparent alpha; no forest, props, shadows, tears, symbols, text or watermark. Exactly one output. Closed toothless mouth despite dialogue; full head/ears-or-mane and upper chest with original margins. Guidance is not proof of exact geometry; surrounding pixels will be checked after generation.'
  uses=[m['image_id'] for m in matrix if any(v['expression_id']==aids[actor,name] for v in m['performance'].values())]
  requests.append({'sequence':len(requests)+1,'requirement_id':aids[actor,name],'variant':'default','actors':[actor],'output':'character/characters/lion_and_mouse_v7/'+actor+'/expressions/'+actor.lower()+'_s08_'+name+'_3q'+('_left' if actor=='Milo' else '')+'_r001_candidate.png','audio_image_uses':uses,'inputs':refs,'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(R/x['path']) for x in refs],'transparent_background':True}})
 pairbase=lib['joint_performance_requirements']['milo_leo.s06.great_tree']['variants']['paw_planted']['file'];canonicals=lib['joint_performance_requirements']['milo_leo.s06.great_tree']['canonical'];newpair={'schema':'feltwillow.joint-performance-requirements.v1','id':'milo_leo.s08.great_tree','revision':'r001','actors':['Leo','Milo'],'canonical':canonicals,'asset_root':'character/characters/lion_and_mouse_v7/interactions/performance_pairs','purpose':'S08 paired performance anchors, not separate approved actor sprites or final scenes','variants':{}}
 for phase,action,uses in [
  ('restrained_blocked','Keep the FRONT paw planted beside Milo as in reference 1, before the release. Leo looks down with thoughtful restraint, no anger or threatening mouth; Milo is tense and frightened, ears/head canonical and body slightly braced, eyes up-left. Preserve the body and screen axis. Clarify paw beside rather than covering Milo’s near foot: a visible small ground gap, do not step on or pin him. No new limb geometry unrelated to clearance.',['S08-L001-B01-I02','S08-L002-B01-I01','S08-L003-B01-I01','S08-L004-B01-I01','S08-L005-B01-I01','S08-L006-B01-I01']),
  ('gentle_clear','After the L010 release: Leo stays lying with head/chest raised, his blocking FRONT paw withdrawn nearer his own chest so the ground route ahead of Milo is visibly clear. Show gentle reassuring eyes/down-right and a small closed-mouth smile. Milo remains on the same viewer-right ground root/depth, looking up-left in surprised relief; do not make him leave, step backward, change size or switch sides. Preserve Leo trunk/hips/rear paws/tail, and preserve Milo head/ear/torso/limb ratios. No paw pressing/covering Milo.',['S08-L016-B01-I01','S08-L017-B01-I01','S08-L018-B01-I01'])]:
  refs=[ref(R/pairbase['path'],role='selected_joint_pose',authority='exact shared body projection and relative scale; only requested acting/front-paw change'),*[dict(canonicals[a],role='canonical_identity_'+a.lower(),authority='identity/anatomy/material for named actor') for a in ['Leo','Milo']],*[ref(S/'review/character_performance_consistency_r001/canonical_measurements_r001'/(a.lower()+'_combined_annotated.jpg'),role='canonical_measurement_'+a.lower(),authority='own-character visible surface baselines only') for a in ['Leo','Milo']]]
  prompt='Edit the owner-selected transparent Leo+Milo paired pose in reference 1. '+action+' Leo remains lying; never stands fully. Preserve the same pair canvas, Leo-left/Milo-right screen axis, intrinsic felt palette, grey Milo paws, cream patch, green mouse eyes, amber lion eyes, mane curls and animal-specific proportions. References 2/3 own respective canonical identities; 4/5 are their own visible measurement guides, never paint guides or apply mouse ratios to lion. No independent head/body resizing. Milo upright projected head fraction 0.39 +/-0.01 applies only at compatible upright pitch; bent/occluded views require comparison, not a fabricated pass. Both mouths closed and toothless. Keep complete characters with margins, genuine transparent alpha, no environment, ground plane, cast shadows, props, symbols, words or watermark. Exactly one output.'
  newpair['variants'][phase]={'status':'planned','file':None,'creation':None,'owner_decision':None,'image_ids':uses,'purpose':action}
  requests.append({'sequence':len(requests)+1,'requirement_id':newpair['id'],'variant':phase,'actors':['Leo','Milo'],'output':'character/characters/lion_and_mouse_v7/interactions/performance_pairs/leo_milo_s08_'+phase+'_3q_r001_candidate.png','audio_image_uses':uses,'inputs':refs,'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(R/x['path']) for x in refs],'transparent_background':True}})
 lib['joint_performance_requirements'][newpair['id']]=newpair;write(S/'character_performance_library.json',lib)
 for q in requests:
  assert len(q['inputs'])<=5 and not (R/q['output']).exists()
  for f in q['inputs']:assert sha(R/f['path'])==f['sha256']
 write(D/'OPERATION.json',{'schema':'feltwillow.performance-generation-proposal.v1','status':'prepared_pending_concrete_owner_approval','endpoint':'image_gen.imagegen','request_count':7,'outputs_per_request':1,'automatic_retries':0,'pricing':'Built-in current model/seed/price not exposed; unknown, not assumed free','estimated_total_cost':None,'scope':'Five S08 portrait-expression foundations and two paired action anchors only. Background scene production and remaining amused/hopeful/sky facial keys follow reviewed anchors; no audio/video or canonical regeneration.','requests':requests})
 (D/'REVIEW.md').write_text('# S08 performance foundations\n\nOwner close-ups interpreted as L007-L015 and L019-L024: Leo except Milo L012/L019-L021. Nine other lines use the S06 fixed shared setup, Leo lying and Milo screen-right. L010 releases the front paw below the Leo portrait crop; L024 sky gesture stays below crop with visible canopy eyeline. World events/audio unchanged. Never enact hypothetical anger.\n\nSeven concrete requests: Leo thoughtful, softened, reassuring; Milo surprised relief, grateful; paired restrained/blocked and gentle/clear. All use selected S07 portrait or S06 paired references and each character’s own canonical/measurement guide. Endpoint image_gen.imagegen, one transparent output each, no retries, total cost unknown. Full prompts/input hashes/settings in [OPERATION.json](OPERATION.json). No submissions.\n\nAfter review, retain exact scene backgrounds and family crops while composing scenes and preparing the remaining amused/hopeful/sky variants. Existing nervous Milo scene can supply trembling-face continuity but does not establish literal motion in a still. The L007 softening pair and L024 gaze pair keep distinct state endpoints. Portraits retain upper-body extent and closed toothless still mouths. Seven missing S06 phases remain separate; this S08 request does not generate them.\n')
 print('Selected three S07 faces; S08 shot map and seven concrete requests prepared, no calls.')
if __name__=='__main__':main()
