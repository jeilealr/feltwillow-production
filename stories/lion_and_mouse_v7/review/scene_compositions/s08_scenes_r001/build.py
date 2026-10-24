"""Compose S08 candidate scenes from authorized performances and prior plates.

Candidate preview use only: no owner performance/scene approval is fabricated.
No paid calls; no body-part scaling; shared rasters explicitly retain all uses.
"""
import copy,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
D=Path(__file__).resolve().parent;R=D.parents[4];S=R/'stories/lion_and_mouse_v7';P=S/'review/character_performance_consistency_r001/s08_planning_r001';F=D.parent/'s06_s07_background_scenes_r001'
def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def main():
 assert not (D/'SCENES.json').exists()
 e=read(P/'EXECUTION.json');op=read(P/'OPERATION.json');assert e['completed']==e['requested']==7
 assert sha(P/'OPERATION.json')==read(P/'AUTHORIZATION.json')['operation_sha256']
 plan=read(S/'audio_visual_plan.json');lib=read(S/'character_performance_library.json');rows={r['requirement_id']+':'+r['variant']:r for r in e['outputs']};layers={};checks=[]
 (D/'layers').mkdir();(D/'receipts').mkdir()
 for q in op['requests']:
  raw=R/q['output'];assert sha(raw)==rows[q['requirement_id']+':'+q['variant']]['sha256']
  for f in q['inputs']:assert sha(R/f['path'])==f['sha256']
  if len(q['actors'])==2:
   with Image.open(raw) as im:im.load();assert im.mode=='RGBA';layers[q['variant']]={'path':str(raw.relative_to(R)),'sha256':sha(raw),'raw_performance':ref(raw),'method':'paired generated candidate; review anatomy and registration separately'}
   continue
  actor=q['actors'][0];name=q['requirement_id'].split('.')[3];basep=R/q['inputs'][0]['path']
  with Image.open(basep) as im:base=im.convert('RGBA')
  with Image.open(raw) as im:im.load();gen=im.convert('RGBA')
  dims=list(gen.size);assert abs(gen.width-base.width)<=1 and abs(gen.height-base.height)<=1,'Canvas drift beyond one pixel: review, never silently rescale anatomy'
  if gen.size!=base.size:
   native=base.copy();native.paste(gen,(0,0));gen=native
  if actor=='Leo':poly=[(500,385),(660,360),(820,400),(1005,445),(1030,600),(1025,750),(920,845),(800,885),(660,850),(480,760),(450,620)]
  else:poly=[(round((x-351)/.72),round((y-100)/.72)) for x,y in [(613,395),(670,356),(750,360),(820,385),(915,420),(959,470),(970,580),(965,671),(878,722),(755,723),(635,686),(581,634),(580,535)]]
  mask=Image.new('L',base.size);ImageDraw.Draw(mask).polygon(poly,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(5));mp=D/'layers'/(actor.lower()+'_'+name+'_face_mask.png');mask.save(mp)
  protected=Image.composite(gen,base,mask);diff=np.any(np.asarray(protected)!=np.asarray(base),axis=2);assert not (diff&(np.asarray(mask)==0)).any()
  out=D/'layers'/(actor.lower()+'_'+name+'_protected.png');protected.save(out)
  lr=dict(ref(out),raw_performance=ref(raw),portrait_base=ref(basep),face_mask=ref(mp),mask_polygon=poly,mask_feather_radius=5,raw_dimensions=dims,native_pixel_origin=[0,0],registration='none; no resize/warp',changed_pixels_outside_face_mask=0,method='local face-mask preservation of source portrait body and head outline')
  layers[name]=lr;checks.append(lr)
 # All selected scene geography comes from the already reconstructed S06 plate.
 platep=F/'S06-L001-B01_location_protected_clean_plate_r001_candidate.png';bgp=F/'S07_foliage_blurred_background.png';plate=Image.open(platep).convert('RGBA');portrait_bg=Image.open(bgp).convert('RGBA');assert plate.size==portrait_bg.size==(1672,941)
 # A small set of genuine acting states is reused deliberately across lines.
 # Offscreen paw release/sky gesture do not require an invented visible action.
 primary={'restrained_blocked':('S08-L001-B01-I01','start'),'gentle_clear':('S08-L016-B01-I01','single'),'thoughtful':('S08-L007-B01-I01','start'),'softened':('S08-L007-B01-I02','end'),'reassuring':('S08-L011-B01-I01','single'),'surprised_relief':('S08-L012-B01-I01','single'),'grateful':('S08-L019-B01-I01','single')}
 source_for={};uses={k:[] for k in primary}
 for l in plan['lines']:
  if l['audio_scene']!='S08':continue
  n=int(l['line_id'][-3:])
  for b in l['beats']:
   for im in b['image_sequence']['images']:
    k='restrained_blocked' if n<=6 else 'gentle_clear' if n in [16,17,18] else 'thoughtful' if n==7 and im['role']=='start' else 'softened' if n in [7,8,9,10] else 'surprised_relief' if n==12 else 'grateful' if n in [19,20,21] else 'reassuring'
    source_for[im['id']]=k;uses[k].append({'image_id':im['id'],'line_id':l['line_id'],'beat_id':b['id'],'role':im['role'],'audio':l['audio'],'world_state_ref':im['state'],'location_view':im['location_view'],'action':b['action']})
    if len(im['performance'])==1:
     actor=next(iter(im['performance']));im['performance'][actor].update(expression_id='milo.expression.s08.'+k+'.3q_left' if actor=='Milo' else 'leo.expression.s08.'+k+'.3q',expression_variant='default',expression_revision='r001',expression_sha256=layers[k]['raw_performance']['sha256'])
     im['phase_intent']=b['action']+'; closest available '+k+' acting reused; no new distinct face inferred'
 outputs=[];association_rows=[]
 for key,(iid,role) in primary.items():
  lr=layers[key];actor=Image.open(R/lr['path']).convert('RGBA');paired=key in ['restrained_blocked','gentle_clear'];base=plate.copy() if paired else portrait_bg.copy();scale=.78 if paired else .72 if key in ['surprised_relief','grateful'] else .65;xy=(220,110) if paired else (351,100) if key in ['surprised_relief','grateful'] else (464,96)
  resized=actor.resize(tuple(round(x*scale) for x in actor.size),Image.Resampling.LANCZOS);layer=Image.new('RGBA',base.size);layer.alpha_composite(resized,xy)
  shadow=Image.new('L',base.size)
  if paired:
   draw=ImageDraw.Draw(shadow);draw.ellipse((355,714,1215,793),fill=62);draw.ellipse((1215,746,1480,814),fill=52);shadow=shadow.filter(ImageFilter.GaussianBlur(13))
  sp=D/'layers'/(key+'_shadow.png');shadow.save(sp);shade=Image.new('RGBA',base.size,(35,24,13,0));shade.putalpha(shadow);result=Image.alpha_composite(Image.alpha_composite(base,shade),layer).convert('RGB')
  effect=(np.asarray(layer.getchannel('A'))>0)|(np.asarray(shadow)>0);delta=np.any(np.asarray(result)!=np.asarray(base.convert('RGB')),axis=2);assert not (delta&~effect).any();mp=D/'layers'/(key+'_effect_mask.png');Image.fromarray(effect.astype('uint8')*255).save(mp)
  out=R/'character/characters/lion_and_mouse_v7/interactions/scene_compositions'/(iid+'_'+role+'_'+key+'_r001_candidate.png');assert not out.exists();result.save(out)
  recipe={'method':'local Pillow composition of authorized performance candidates; no new provider calls','performance_layer':lr,'background':ref(platep if paired else bgp),'uniform_whole_layer_scale':scale,'origin_pixels':list(xy),'shadow':ref(sp),'effect_mask':ref(mp),'changed_pixels_outside_actor_and_shadow_mask':0,'resampling':'LANCZOS','owner_performance_approval':None,'preview_scope':'New generated performances are pending owner review; this local composition is a scene preview, not approved image readiness','acting_choice':'Narration-specific best-fit expression reused across related lines; no generic surprise','provider_calls':0,'actual_local_cost':0}
  rp=D/'receipts'/(key+'.json');write(rp,recipe);first=next(v for v in uses[key] if v['image_id']==iid)
  row=dict(first,path=str(out.relative_to(R)),sha256=sha(out),image_revision='r001',dimensions=[1672,941],status='candidate_pending_owner_scene_review',owner_approval=None,creation=dict(recipe,receipt=ref(rp)),all_audio_image_uses=uses[key],technical_review='Narration-specific acting on fixed background/crop; new performance and scene pending owner review. Shared-raster uses are holds/offscreen actions, not distinct visible motion endpoints. Anatomy, light and grounding need review.')
  side=out.with_suffix('.json');write(side,row);row.update(sidecar=ref(side),receipt=ref(rp),source_variant=key);outputs.append(row)
  for u in uses[key]:
   association_rows.append(dict(u,path=row['path'],sha256=row['sha256'],dimensions=row['dimensions'],sidecar=row['sidecar'],receipt=row['receipt'],status=row['status'],owner_approval=None,source_variant=key,audio_scene='S08',audio_wav=u['audio']['wav'],audio_sha256=u['audio']['sha256'],background_continuity='locked_background' if paired else 'same_place_new_view',primary_image_id=iid,reuses_exact_scene_pixels=u['image_id']!=iid,review_notes=[row['technical_review']]))
 association_rows.sort(key=lambda r:r['image_id'])
 write(D/'SCENES.json',{'unique_scene_files':len(outputs),'audio_lines':24,'image_associations':len(association_rows),'outputs':outputs,'associations':association_rows,'provider_calls':0,'note':'Seven unique scene depictions deliberately reused for 24 narration lines/28 image slots. Identical before/after raster at L001/L010/L024 conveys holds/offscreen changes; no visible head/paw/sky motion endpoint is claimed.'})
 write(S/'scene_composition_candidates_s08.json',{'schema':'feltwillow.scene-composition-candidates.v1','story':'lion_and_mouse_v7','images':association_rows,'scope':'Candidate previews using new pending performance layers; no approval transfer'})
 write(S/'audio_visual_plan.json',plan)
 write(D/'COMPOSITION_VALIDATION.json',{'protected_portrait_layers':checks,'scene_outputs':[{'path':o['path'],'sha256':o['sha256'],'all_uses':len(o['all_audio_image_uses'])} for o in outputs],'protected_background_outside_effect_mask':'zero changed pixels','unique_files':len(outputs),'image_slots':len(association_rows),'owner_approvals':0,'full_suite':'not run per owner cadence','motion_limitations':['L001 head-look endpoints reuse same raster','L010 front-paw release below portrait crop; identical before/after still','L024 sky gesture below crop; no generated upward-gaze endpoint'],'narration_specific_unproduced_variants':'amused, hopeful and sky_hint not generated; closest softened, grateful and reassuring depictions chosen explicitly'})
 print('Saved',len(outputs),'unique scene candidate rasters for',len(association_rows),'image associations and 24 S08 lines.')
if __name__=='__main__':main()
