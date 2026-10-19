#!/usr/bin/env python3
"""Bound an ImageGen integration suggestion to a selected composite's actor.

No active images, production plans or approval records are modified. Dependencies:
Pillow, numpy, opencv-python. Face/prop protection is explicit, never inferred.
"""
import argparse,hashlib,json,shutil
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[4];HOME=Path(__file__).resolve().parent
STORY=ROOT/'stories/lion_and_mouse_v6'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def run(fid,generated,protected_boxes,relight_only=False):
 if json.loads((HOME/'audit.json').read_text()).get('status')=='complete':
  raise SystemExit('Completed finish receipts are immutable. Start a new scoped review; use verify_finish.py to check this adoption.')
 plan=json.loads((STORY/'keyframe_plan.json').read_text());row=next(x for x in plan['images'] if x['id']==fid)
 source_path=ROOT/row['candidate_path'];assert sha(source_path)==row['sha256']
 source=np.array(Image.open(source_path).convert('RGB'));H,W=source.shape[:2]
 receipt_path=STORY/'image_sources/compositions'/(fid+'.json')
 if receipt_path.exists() and 'output_sha256' in json.loads(receipt_path.read_text()):
  receipt=json.loads(receipt_path.read_text())
 elif any(x['id']==fid for x in json.loads((HOME/'legacy_selected_compositions.json').read_text())):
  receipt_path=HOME/'legacy_selected_compositions.json'
  legacy=next(x for x in json.loads(receipt_path.read_text()) if x['id']==fid and x['current_sha256']==row['sha256'])
  chars=[]
  for c in legacy['composition']['characters']:
   label=c['path'].split('/feltwillow-production/',1)[-1]
   bx0,by0,bx1,by1=c['bbox'];nh=round(c['h']*H);nw=round((bx1-bx0)*nh/(by1-by0))
   chars.append({'actor':'milo','still_source':{'label':label,'sha256':c['source_sha256']},'box':[round(c['x']*W-nw/2),round(c['y']*H-nh),nw,nh],'flip':c.get('flip',False),'contact_shadows':c.get('contact_shadows',[]),'source_trim_bbox':c['bbox']})
  receipt={'output_sha256':legacy['current_sha256'],'characters':chars}
 else:
  receipt_path=HOME/'manual_regions.json'
  manual=json.loads(receipt_path.read_text())['frames'][fid]
  receipt={'output_sha256':row['sha256'],'characters':[],'manual':manual}
  relight_only=True
 assert receipt['output_sha256']==row['sha256']
 aliases={x['previous_path']:x['path'] for x in json.loads((STORY/'image_sources/cleanup_manifest.json').read_text())['preserved_assets']}
 folder=HOME/'frames'/fid;folder.mkdir(parents=True,exist_ok=True)
 raw=folder/'generated.png'
 if Path(generated).resolve()!=raw.resolve():shutil.copyfile(generated,raw)
 with Image.open(raw) as im:raw_size=list(im.size);suggestion=np.asarray(im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)).astype('float32')
 edit=np.zeros((H,W),np.float32);actor_alpha=np.zeros_like(edit);other=np.zeros_like(edit);yy,xx=np.mgrid[:H,:W];layers=[]
 for actor in receipt['characters']:
  label=actor['still_source']['label'];path=ROOT/aliases.get(label,label);assert sha(path)==actor['still_source']['sha256']
  layer=np.array(Image.open(path).convert('RGBA'));alpha=layer[:,:,3].astype('float32')/255
  if actor.get('source_trim_bbox'):
   bx0,by0,bx1,by1=actor['source_trim_bbox'];trim=alpha[by0:by1,bx0:bx1]
  else:
   ys,xs=np.nonzero(alpha>.5);trim=alpha[ys.min():ys.max()+1,xs.min():xs.max()+1]
  if actor.get('flip'):trim=trim[:,::-1]
  x,y,w,h=actor['box'];placed=np.zeros((H,W),np.float32);a=cv2.resize(trim,(w,h),interpolation=cv2.INTER_AREA)
  l,t=max(0,x),max(0,y);right,bottom=min(W,x+w),min(H,y+h)
  placed[t:bottom,l:right]=a[t-y:bottom-y,l-x:right-x]
  if actor['actor']!='milo':other=np.maximum(other,placed);continue
  actor_alpha=np.maximum(actor_alpha,placed);edit=np.maximum(edit,placed)
  for contact in actor.get('contact_shadows',[]):
   cx=x+contact['u']*w;cy=y+contact['v']*h
   # Narrow immediate-contact patch; never expose entire generic shadow ellipse.
   sx=max(3,min(42,w*.08));sy=max(2,min(7,h*.012))
   patch=np.exp(-.5*(((xx-cx)/sx)**2+((yy-cy)/sy)**2)).astype('float32');patch[patch<.015]=0
   edit=np.maximum(edit,patch*(1-placed))
  layers.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),'box':actor['box'],'flip':actor.get('flip',False)})
 if receipt.get('manual'):
  spec=receipt['manual'];region=np.zeros((H,W),np.uint8)
  for polygon in spec['polygons']:cv2.fillPoly(region,[np.array(polygon,dtype='int32')],255)
  for x0,y0,x1,y1 in spec['ellipses']:cv2.ellipse(region,((x0+x1)//2,(y0+y1)//2),((x1-x0)//2,(y1-y0)//2),0,0,360,255,-1)
  rgb=source.astype('float32');blue=np.maximum(rgb[:,:,2],1)
  interior=(rgb[:,:,0]/blue<1.95)&(rgb[:,:,1]/blue<1.55)
  region=region.astype('float32')/255*interior
  # Smooth inward only: outside the inspected/chroma-restricted support stays exact.
  edit=region*cv2.GaussianBlur(region,(0,0),2)
  layers=[{'path':str(source_path.relative_to(ROOT)),'sha256':row['sha256'],'box':spec['box'],'mask_source':'manually inspected interior wool regions; see manual_regions.json'}]
 if not layers:raise ValueError('No Milo RGBA source or explicit inspected interior regions')
 # Other actors and their prop topology are immutable. Original layers include their ropes.
 edit[other>0]=0
 protect=np.zeros((H,W),np.uint8)
 for box in protected_boxes:
  x0,y0,x1,y1=box
  cv2.ellipse(protect,((x0+x1)//2,(y0+y1)//2),((x1-x0)//2,(y1-y0)//2),0,0,360,255,-1)
 # Feather OUTSIDE protected ellipses, whose feature pixels remain exactly original.
 feather=cv2.GaussianBlur(protect.astype('float32')/255,(0,0),15);feather=np.maximum(feather,protect/255)
 edit*=1-feather
 # Quantize before blending so the saved mask is the exact verification support.
 edit=np.rint(np.clip(edit,0,1)*255)/255
 if relight_only:
  # Extract a smooth, bounded light field; never import generated anatomy/background.
  sigma=20
  src_light=cv2.GaussianBlur(source.astype('float32'),(0,0),sigma)
  gen_light=cv2.GaussianBlur(suggestion,(0,0),sigma)
  gain=np.clip((gen_light+12)/(src_light+12),.85,1.12)
  suggestion=source.astype('float32')*gain
 result=np.rint(np.clip(source*(1-edit[:,:,None])+suggestion*edit[:,:,None],0,255)).astype('uint8')
 diff=np.any(result!=source,axis=2);assert not np.any(diff & (edit==0));assert not np.any(diff & (protect>0))
 Image.fromarray(result).save(folder/'finished.png');Image.fromarray(np.rint(edit*255).astype('uint8')).save(folder/'edit_mask.png');Image.fromarray(protect).save(folder/'protected_features.png')
 # Keep a compact paired detail/whole-frame overview. Original remains hash-bound source.
 pair=Image.new('RGB',(960,304),'#202020');from PIL import ImageDraw
 d=ImageDraw.Draw(pair);d.text((10,8),fid+' — original',fill='white');d.text((490,8),fid+' — focused finish',fill='white')
 pair.paste(Image.fromarray(source).resize((480,270)),(0,30));pair.paste(Image.fromarray(result).resize((480,270)),(480,30));pair.save(folder/'comparison.jpg',quality=95)
 report={'schema':'feltwillow.focused-integration-frame.v1','id':fid,'status':'candidate_pending_native_inspection','source_path':row['candidate_path'],'source_sha256':row['sha256'],'source_receipt':str(receipt_path.relative_to(ROOT)),'source_layers':layers,'raw_generated_path':str(raw.relative_to(ROOT)),'raw_sha256':sha(raw),'raw_dimensions':raw_size,'mode':'model_suggested_smooth_lighting_only' if relight_only else 'bounded_generated_material_finish','normalization':'LANCZOS to original 1920x1080; original actor alpha and explicit feathered elliptical feature protection; no image registration warp','protected_ellipse_bounds_xyxy':protected_boxes,'finished_path':str((folder/'finished.png').relative_to(ROOT)),'finished_sha256':sha(folder/'finished.png'),'edit_mask_path':str((folder/'edit_mask.png').relative_to(ROOT)),'changed_pixels':int(diff.sum()),'changed_outside_edit_support':0,'changed_protected_feature_pixels':0,'mean_channel_change_inside_edit':float(np.abs(result.astype('float32')-source)[edit>0].mean()),'active_images_modified':False,'technical_approvals_granted':False}
 dump(folder/'receipt.json',report);print(fid,report['changed_pixels'],'changed; protected geometry/background/features verified')
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--frame',required=True);ap.add_argument('--generated',type=Path,required=True);ap.add_argument('--protect',type=str,required=True,help='JSON list of exact protected ellipses x0,y0,x1,y1');ap.add_argument('--relight-only',action='store_true',help='Transfer only smooth bounded lighting, preserving original material/anatomy pixels');a=ap.parse_args();run(a.frame,a.generated,json.loads(a.protect),a.relight_only)
