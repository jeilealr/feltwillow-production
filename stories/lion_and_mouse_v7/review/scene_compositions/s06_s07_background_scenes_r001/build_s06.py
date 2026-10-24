"""Save one authorized raw plate and compose selected pair rasters locally."""
import hashlib,json,shutil
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
D=Path(__file__).resolve().parent;R=D.parents[4];S=R/'stories/lion_and_mouse_v7'
def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def main():
 op=read(D/'OPERATION.json');auth=read(D/'AUTHORIZATION.json');assert sha(D/'OPERATION.json')==auth['operation_sha256']
 q=op['requests'][0];src=R/q['inputs'][0]['path'];assert sha(src)==q['inputs'][0]['sha256']
 raw=R/q['output'];assert not raw.exists()
 tool=Path('/Users/lealroja/.codex/generated_images/01a1533f-9137-7e20-a37c-3eeb1ab8afad/exec-21e9d52c-347f-442f-865e-184206dfbb7d.png');shutil.copy2(tool,raw)
 receipt=D/'receipts/clean_plate_generation.json';write(receipt,{'endpoint':op['endpoint'],'tool_arguments':q['tool_arguments'],'operation_sha256':auth['operation_sha256'],'authorization':ref(D/'AUTHORIZATION.json'),'tool_output_path':str(tool),'inputs':q['inputs'],'actual_cost':None,'request_id':None,'seed':None,'attempt':1})
 base=Image.open(src).convert('RGB');generated=Image.open(raw).convert('RGB');assert base.size==generated.size==(1672,941)
 rawside=raw.with_suffix('.json');write(rawside,{'path':str(raw.relative_to(R)),'sha256':sha(raw),'dimensions':list(base.size),'creation_receipt':ref(receipt),'status':'candidate_pending_owner_review'})
 e=read(D/'EXECUTION.json');assert e['completed']==0;e['completed']=1;e['attempts']['0']['status']='completed_candidate_saved';e['outputs']=[dict(ref(raw),sidecar=ref(rawside),receipt=ref(receipt),dimensions=list(base.size))];write(D/'EXECUTION.json',e)
 poly=[(210,565),(315,550),(390,605),(480,575),(535,525),(635,470),(780,450),(900,470),(915,415),(975,360),(1070,310),(1195,285),(1315,295),(1400,345),(1465,415),(1515,495),(1530,610),(1515,715),(1490,790),(1330,805),(1100,805),(965,790),(820,770),(620,790),(410,795),(365,735),(275,720),(215,685)]
 mask=Image.new('L',base.size);ImageDraw.Draw(mask).polygon(poly,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(8));mp=D/'old_leo_repair_mask.png';mask.save(mp)
 protected=Image.composite(generated,base,mask);plate=D/'S06-L001-B01_location_protected_clean_plate_r001_candidate.png';protected.save(plate)
 support=np.asarray(mask)>0;changed=np.any(np.asarray(base)!=np.asarray(protected),axis=2);assert not (changed&~support).any()
 write(plate.with_suffix('.json'),{'image':ref(plate),'source':ref(src),'raw_generated':ref(raw),'mask':ref(mp),'polygon':poly,'feather_radius':8,'changed_pixels_outside_mask':0,'status':'candidate_pending_owner_review','note':'Masked generated reconstruction; original pixels restored outside declared repair support. Hidden ground is synthesized, not historically known.'})
 lib=read(S/'character_performance_library.json');plan=read(S/'audio_visual_plan.json');pair=lib['joint_performance_requirements']['milo_leo.s06.great_tree'];outputs=[];checks=[]
 jobs=[('rest_nose','S06-L001-B01-I01','start','rest_nose'),('path_arrival','S06-L001-B02-I02','end','path_arrival'),('paw_planted','S06-L002-B01-I03','end','front_paw_block')]
 for n,(phase,iid,role,subject) in enumerate(jobs,8):
  v=pair['variants'][phase];f=v['file'];assert v['status']=='owner_selected_for_performance' and sha(R/f['path'])==f['sha256']
  actor=Image.open(R/f['path']).convert('RGBA');scale=.78;xy=(220,110);actor=actor.resize(tuple(round(z*scale) for z in actor.size),Image.Resampling.LANCZOS)
  layer=Image.new('RGBA',base.size);layer.alpha_composite(actor,xy)
  # Grounding layer only: under Leo's supported trunk/paws and Milo's feet.
  # It does not fix anatomy, relative foot occlusion or scene-depth mismatch.
  shadow=Image.new('L',base.size);draw=ImageDraw.Draw(shadow)
  for bounds,opacity in [((355,714,1215,793),62),((1215,746,1480,814),52)]:draw.ellipse(bounds,fill=opacity)
  shadow=shadow.filter(ImageFilter.GaussianBlur(13));sp=D/f'{iid}_shadow.png';shadow.save(sp)
  shade=Image.new('RGBA',base.size,(35,24,13,0));shade.putalpha(shadow)
  result=Image.alpha_composite(Image.alpha_composite(protected.convert('RGBA'),shade),layer).convert('RGB')
  effect=(np.asarray(layer.getchannel('A'))>0)|(np.asarray(shadow)>0);delta=np.any(np.asarray(result)!=np.asarray(protected),axis=2);assert not (delta&~effect).any()
  effectp=D/f'{iid}_effect_mask.png';Image.fromarray(effect.astype('uint8')*255).save(effectp)
  out=R/'character/characters/lion_and_mouse_v7/interactions/scene_compositions'/f'{iid}_{role}_{subject}_r001_candidate.png';assert not out.exists();result.save(out)
  line=next(l for l in plan['lines'] if l['line_id']==iid[:8]);beat=next(b for b in line['beats'] if b['id']==iid[:12]);im=next(im for im in beat['image_sequence']['images'] if im['id']==iid)
  recipe={'method':'local Pillow composition, exact selected pair raster uniformly scaled','provider_calls':0,'actual_cost':0,'plate':ref(plate),'pair':f,'owner_decision':v['owner_decision'],'uniform_pair_scale':scale,'pair_origin_pixels':list(xy),'resampling':'LANCZOS','shadow':ref(sp),'effect_mask':ref(effectp),'actor_RGB_edits':False,'whole_pair_transform_shared_across_three_anchors':True}
  rp=D/'receipts'/f'{n:03d}.json';write(rp,recipe)
  note='Selected joint pose reused as one layer; Leo lying, Milo screen-right. Same shared transform/background, no body redraw. Grounding, light, relative anatomy and scene depth need owner review.'
  if phase=='paw_planted':note+=' Existing source paw/foot overlap retained exactly; scene approval is separate from performance selection.'
  row={'image_id':iid,'line_id':line['line_id'],'beat_id':beat['id'],'image_revision':'r001','role':role,'path':str(out.relative_to(R)),'sha256':sha(out),'dimensions':list(base.size),'audio':line['audio'],'location_view':im['location_view'],'world_state_ref':im['state'],'status':'candidate_pending_owner_scene_review','owner_approval':None,'creation':dict(recipe,receipt=ref(rp)),'technical_review':note}
  side=out.with_suffix('.json');write(side,row);row.update(sidecar=ref(side),receipt=ref(rp));outputs.append(row)
  checks.append({'image_id':iid,'changed_pixels_outside_actor_and_shadow_mask':0,'scene_contact_anatomy_pass':None})
 write(D/'S06_SCENES.json',{'outputs':outputs,'provider_calls':0,'actual_cost':0,'missing_joint_phases':7})
 write(D/'S06_COMPOSITION_VALIDATION.json',{'raw_generation_requests':1,'retries':0,'actual_generation_cost':None,'raw_dimensions':list(generated.size),'protected_background_changed_pixels_outside_mask':0,'scenes':checks,'full_suite':'not run per owner cadence'})
 reg=S/'scene_composition_candidates_s06_s07.json';registry=read(reg)
 for row in outputs:
  item={k:row[k] for k in ['image_id','line_id','beat_id','role','location_view','path','sha256','dimensions','sidecar','receipt','status']};item.update(audio_scene='S06',audio_wav=row['audio']['wav'],audio_sha256=row['audio']['sha256'],background_continuity='locked_background',owner_approval=None,review_notes=[row['technical_review']]);registry['images'].append(item)
 write(reg,registry)
 print('Saved raw repair, protected shared plate and three local S06 anchors; seven phases remain.')
if __name__=='__main__':main()
