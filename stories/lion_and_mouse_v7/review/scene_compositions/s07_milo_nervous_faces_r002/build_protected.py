"""Restore original scene outside explicit face masks; preserve generated raws."""
import copy,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
D=Path(__file__).resolve().parent;R=D.parents[4];S=R/'stories/lion_and_mouse_v7';F=D.parent/'s06_s07_background_scenes_r001'
def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(R)),'sha256':sha(p)}
def main():
 e=read(D/'EXECUTION.json');op=read(D/'OPERATION.json');assert e['completed']==3;assert sha(D/'OPERATION.json')==read(D/'AUTHORIZATION.json')['operation_sha256'];assert not (D/'PROTECTED_SCENES.json').exists()
 previous=read(F/'LOCAL_SCENES.json');registry=read(S/'scene_composition_candidates_s06_s07.json');outputs=[];checks=[]
 # Mask is inside the face: ears, skull silhouette, neck/chest and background
 # remain the existing source pixels. No head registration warp is applied.
 polygon=[(613,395),(670,356),(750,360),(820,385),(915,420),(959,470),(970,580),(965,671),(878,722),(755,723),(635,686),(581,634),(580,535)]
 for i,q in enumerate(op['requests']):
  raw=R/q['output'];source=R/q['inputs'][0]['path'];assert sha(source)==q['inputs'][0]['sha256'];raw_row=next(o for o in e['outputs'] if o['image_id']==q['image_id']);assert sha(raw)==raw_row['sha256']
  with Image.open(source) as im:base=im.convert('RGB')
  with Image.open(raw) as im:im.load();generated=im.convert('RGB')
  raw_dimensions=list(generated.size)
  assert base.size==(1672,941) and generated.size in {(1672,941),(1671,941)},'Unexpected dimensions: review before compositing'
  # The L004 raw is one pixel narrower. Place native pixels at (0,0) on
  # source-sized canvas; the untouched rightmost source column is outside
  # the face. Do not stretch or register the head to conceal this difference.
  if generated.size!=base.size:
   native_canvas=base.copy();native_canvas.paste(generated,(0,0));generated=native_canvas
  mask=Image.new('L',base.size);ImageDraw.Draw(mask).polygon(polygon,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(4));mp=D/(q['image_id']+'_face_mask.png');mask.save(mp)
  result=Image.composite(generated,base,mask);support=np.asarray(mask)>0;diff=np.any(np.asarray(base)!=np.asarray(result),axis=2);assert not (diff&~support).any()
  out=R/q['protected_scene_output'];assert not out.exists();result.save(out)
  recipe={'method':'local Pillow face-mask restoration after authorized imagegen edit','raw_generated':ref(raw),'generation_receipt':raw_row['receipt'],'source_scene':ref(source),'mask':ref(mp),'mask_polygon':polygon,'mask_feather_radius':4,'raw_dimensions':raw_dimensions,'input_and_output_dimensions':[1672,941],'raw_native_pixel_origin':[0,0],'registration':'none; no rescaling or warp; any missing right-edge column comes from source outside face mask','changed_pixels_outside_face_mask':0,'local_provider_calls':0,'actual_generation_cost':None,'protection':'Original background, body, ears and skull silhouette retained outside face mask; within-mask gaze/eye and facial anatomy need visual review'}
  rp=D/'receipts'/f'{i+1:03d}_protected_composition.json';write(rp,recipe)
  old=next(o for o in previous['outputs'] if o['image_id']==q['image_id']);row=copy.deepcopy(old);row.update(path=str(out.relative_to(R)),sha256=sha(out),image_revision='r002',status='candidate_pending_owner_scene_review',owner_approval=None,creation=dict(recipe,receipt=ref(rp)),technical_review='More nervous facial acting, closed mouth and upward-left gaze. Original scene restored outside recorded face mask, including body, ears and background. Within-mask eye/cheek/face geometry and emotion need owner review; no numerical anatomy pass.');row.pop('sidecar',None);row.pop('receipt',None)
  side=out.with_suffix('.json');write(side,row);row.update(sidecar=ref(side),receipt=ref(rp));outputs.append(row)
  checks.append({'image_id':q['image_id'],'image_sha256':row['sha256'],'dimensions':[1672,941],'changed_pixels_outside_face_mask':0,'changed_pixels_inside_face_mask':int(diff.sum()),'ear_body_background':'source bytes unchanged outside mask','owner_approval':None})
  for n,o in enumerate(previous['outputs']):
   if o['image_id']==row['image_id']:
    previous.setdefault('superseded_face_candidates',[]).append(o);previous['outputs'][n]=row;break
  for n,o in enumerate(registry['images']):
   if o['image_id']==row['image_id']:
    registry.setdefault('superseded_candidates',[]).append(o);new=copy.deepcopy(o);new.update({k:row[k] for k in ['path','sha256','sidecar','receipt','status']});new.update(owner_approval=None,review_notes=[row['technical_review']]);registry['images'][n]=new;break
 write(D/'PROTECTED_SCENES.json',{'outputs':outputs,'provider_calls':0,'actual_cost':0,'generation_requests_in_separate_execution':3});write(D/'COMPOSITION_VALIDATION.json',{'outputs':checks,'raw_outputs_preserved':True,'no_head_body_rescaling':True,'automatic_retries':0,'actual_generation_cost':None,'full_suite':'not run per owner cadence'});write(F/'LOCAL_SCENES.json',previous);write(S/'scene_composition_candidates_s06_s07.json',registry)
 print('Saved three protected nervous-face candidates; original scene pixels exact outside face masks.')
if __name__=='__main__':main()
