#!/usr/bin/env python3
"""Candidate-only illumination repair: preserve original texture and geometry.

The model supplies smooth lighting guidance; none of its geometry is imported.
Unlike the earlier finishing pass, there is no frozen oval of facial lighting.
"""
import hashlib,json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[4];HOME=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 if (HOME/'lighting_receipt.json').exists() and json.loads((HOME/'lighting_receipt.json').read_text()).get('active_selection_changed'):
  raise SystemExit('Repair is adopted; preserve the exact recipe and start a new revision for further edits.')
 source=ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes/s04_p02_r13_candidate.png'
 raw=HOME/'s04_p02_lighting_generated_r01.png'
 layer=ROOT/'character/characters/lion_and_mouse_v6/interactions/sources/perceptual_world_fixes/milo_atlas_crouch_r01.png'
 original=np.array(Image.open(source).convert('RGB'));h,w=original.shape[:2]
 generated=np.array(Image.open(raw).convert('RGB').resize((w,h),Image.Resampling.LANCZOS)).astype('float32')
 alpha=np.array(Image.open(layer).convert('RGBA'))[:,:,3].astype('float32')/255
 yy,xx=np.nonzero(alpha>.5);alpha=alpha[yy.min():yy.max()+1,xx.min():xx.max()+1]
 x,y,bw,bh=724,491,471,265;mask=np.zeros((h,w),np.float32);mask[y:y+bh,x:x+bw]=cv2.resize(alpha,(bw,bh),interpolation=cv2.INTER_AREA)
 # Smooth model lighting relative to selected pixels; preserve source features,
 # expression and wool detail. A single field spans the entire character.
 sigma=16
 a=cv2.GaussianBlur(original.astype('float32'),(0,0),sigma)
 b=cv2.GaussianBlur(generated,(0,0),sigma)
 gain=np.clip((b+12)/(a+12),.80,1.12)
 support=np.rint(mask*255).astype('uint8');mask=support.astype('float32')/255
 result=np.rint(np.clip(original*(1-mask[:,:,None])+original*gain*mask[:,:,None],0,255)).astype('uint8')
 diff=np.any(result!=original,axis=2);assert not np.any(diff&(support==0))
 output=HOME/'s04_p02_lighting_repair_r01_candidate.png';Image.fromarray(result).save(output);Image.fromarray(support).save(HOME/'lighting_edit_mask.png')
 pair=Image.new('RGB',(1500,680),'#242424');draw=ImageDraw.Draw(pair)
 for i,(name,image) in enumerate([('Current r13 — face protection mismatch',original),('Repair — continuous illumination',result)]):
  crop=Image.fromarray(image).crop((700,460,1230,790));crop.thumbnail((730,520));pair.paste(crop,(i*750+10,60));draw.text((i*750+12,20),name,fill='white')
 pair.save(HOME/'lighting_detail_comparison.jpg',quality=96)
 receipt={'schema':'feltwillow.lighting-repair-candidate.v1','status':'prepared_pending_owner_review_not_adopted','source_path':str(source.relative_to(ROOT)),'source_sha256':sha(source),'raw_path':str(raw.relative_to(ROOT)),'raw_sha256':sha(raw),'raw_normalization':'LANCZOS to existing 1920x1080 canvas; no registration warp','layer_path':str(layer.relative_to(ROOT)),'layer_sha256':sha(layer),'layer_box_xywh':[x,y,bw,bh],'mode':'smooth RGB illumination gain applied to original pixels across whole actor, including face','gaussian_sigma_px':sigma,'gain_bounds':[.80,1.12],'regularizer':12,'frozen_face_ellipse':False,'output_path':str(output.relative_to(ROOT)),'output_sha256':sha(output),'mask_sha256':sha(HOME/'lighting_edit_mask.png'),'changed_pixels':int(diff.sum()),'changed_outside_original_actor_alpha':0,'expression_or_geometry_imported_from_model':False,'active_selection_changed':False,'technical_approval_inferred':False}
 (HOME/'lighting_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt))
if __name__=='__main__':run()
