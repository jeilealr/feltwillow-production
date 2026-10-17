#!/usr/bin/env python3
"""Owner-authorized A/B trial; never changes active images or production plans.

Requires Pillow, numpy and opencv-python. Takes an already generated focused
edit as --generated; no model calls or credentials are handled by this script.
"""
import argparse,hashlib,json,shutil
from pathlib import Path
import cv2
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[4]
HOME=Path(__file__).resolve().parent
SOURCE=ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes/s04_p03_r12_candidate.png'
LAYER=ROOT/'character/characters/lion_and_mouse_v6/interactions/sources/perceptual_world_fixes/milo_run_r01.png'
RECEIPT=ROOT/'stories/lion_and_mouse_v6/image_sources/compositions/s04_p03.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,a):
 p=HOME/name;Image.fromarray(np.rint(np.clip(a,0,255)).astype('uint8')).save(p);return p

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--generated',type=Path,required=True);args=ap.parse_args()
 source=np.asarray(Image.open(SOURCE).convert('RGB')).astype('float32');H,W=source.shape[:2]
 receipt=json.loads(RECEIPT.read_text());assert sha(SOURCE)==receipt['output_sha256']
 rgba=np.asarray(Image.open(LAYER).convert('RGBA'));alpha=rgba[:,:,3].astype('float32')/255
 ys,xs=np.nonzero(alpha>.5);trim=alpha[ys.min():ys.max()+1,xs.min():xs.max()+1]
 x,y,w,h=receipt['characters'][0]['box'];a=np.zeros((H,W),np.float32);a[y:y+h,x:x+w]=cv2.resize(trim,(w,h),interpolation=cv2.INTER_AREA)
 yy,xx=np.mgrid[0:H,0:W];u=np.clip((xx-x)/w,0,1);v=np.clip((yy-y)/h,0,1)
 # Local luminance shaping only: preserve intrinsic pigment and all geometry.
 gain=.98-.055*u-.025*v
 softened=cv2.GaussianBlur(source,(0,0),.65)
 relit=(source*.78+softened*.22)*gain[:,:,None]
 # Reduce bright cutout boundary slightly, rather than blurring the full image.
 core=cv2.erode(a,np.ones((3,3),np.uint8));edge=np.maximum(a-core,0)
 relit-=edge[:,:,None]*4
 # Supporting sole only. The trailing foot remains airborne; no invented contacts.
 contact=np.exp(-.5*(((xx-522)/28)**2+((yy-755)/3.3)**2)).astype('float32')
 contact[contact<.008]=0
 contact*=1-a
 deterministic=source*(1-a[:,:,None])+relit*a[:,:,None]
 deterministic*=1-.15*contact[:,:,None]
 det=save('s04_p03_integration_deterministic_r01.png',deterministic)
 # Archive the actual generator output. Explicit normalization is recorded below.
 raw=HOME/'s04_p03_integration_generated_source_r01.png'
 if args.generated.resolve()!=raw.resolve():shutil.copyfile(args.generated,raw)
 with Image.open(raw) as image:
  raw_size=list(image.size);generated=np.asarray(image.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)).astype('float32')
 # Limit generated repaint to the original silhouette and a very small contact patch.
 # Preserve facial feature pixels exactly: eyes, muzzle, smile, gaze stay selected.
 face=np.maximum(0,1-(((xx-548)/83)**2+((yy-490)/62)**2))
 face=np.clip(face*5,0,1)
 edit=a*(1-face)
 foot=np.exp(-.5*(((xx-522)/42)**2+((yy-755)/7)**2)).astype('float32')
 foot[foot<.015]=0
 edit=np.maximum(edit,foot*(1-a))
 gen=source*(1-edit[:,:,None])+generated*edit[:,:,None]
 focused=save('s04_p03_integration_focused_r01.png',gen)
 mask=save('integration_edit_mask.png',edit*255)
 # Also save deterministic support to make preservation claims independently checkable.
 det_mask=save('deterministic_edit_mask.png',np.maximum(a,contact)*255)
 results={}
 for name,path,m in [('deterministic',det,np.maximum(a,contact)),('focused_generative',focused,edit)]:
  output=np.asarray(Image.open(path));base=source.astype('uint8');changed=np.any(output!=base,axis=2)
  assert not np.any(changed & (m==0)),name
  results[name]={'path':str(path.relative_to(ROOT)),'sha256':sha(path),'changed_pixel_count':int(changed.sum()),'changed_outside_edit_support':0,'mean_absolute_channel_change_inside_support':round(float(np.abs(output.astype('float32')-source)[m>0].mean()),3)}
 assert sha(SOURCE)==receipt['output_sha256']
 # Side-by-side overview and common detail crop, clearly labeled outside artwork.
 def board(detail=False):
  images=[Image.open(SOURCE),Image.open(det),Image.open(focused)];labels=['A - approved original','B - deterministic polish','C - focused generative integration']
  board=Image.new('RGB',(1440,470 if detail else 314),'#202020');draw=ImageDraw.Draw(board)
  for i,(im,label) in enumerate(zip(images,labels)):
   if detail:im=im.crop((225,280,705,800));im.thumbnail((480,420))
   else:im=im.resize((480,270),Image.Resampling.LANCZOS)
   board.paste(im,(i*480,34));draw.text((i*480+8,10),label,fill='white')
  board.save(HOME/('detail_comparison.jpg' if detail else 'comparison.jpg'),quality=95)
 board();board(True)
 report={'schema':'feltwillow.image-integration-trial.v1','status':'comparison_candidates_pending_owner_selection','frame':'s04_p03','active_images_modified':False,'source':{'path':str(SOURCE.relative_to(ROOT)),'sha256':sha(SOURCE)},'source_layer':{'path':str(LAYER.relative_to(ROOT)),'sha256':sha(LAYER)},'geometry':{'original_actor_box_xywh':[x,y,w,h],'rescaling_or_repositioning':False,'mask_method':'Replay selected RGBA alpha crop and INTER_AREA placement from original compositor receipt. All edits bounded by source alpha or local supporting-foot shadow.'},'deterministic_recipe':{'luminance_gain':'0.98 - 0.055*u - 0.025*v (within original actor alpha)','detail_softening':'22% blend with sigma=0.65 Gaussian; actor pixels only','edge_reduction':'4 intensity levels on one-pixel alpha boundary','contact_shadow':'15% peak attenuation at (522,755), sigma (28,3.3), existing support only'},'generative_recipe':{'tool':'built-in image_gen','prompt_file':'integration_prompt.txt','raw_path':str(raw.relative_to(ROOT)),'raw_sha256':sha(raw),'raw_dimensions':raw_size,'delivery_dimensions':[W,H],'normalization':'LANCZOS to original delivery canvas, then bounded blend; no global color grading or geometric warping','protected_face':'Original central eyes/muzzle/smile pixels preserved through feathered face mask','limitations':'Generated interior wool/shading can drift; preserved edit support does not prove anatomical or identity match. Raw generator changes scenery, which is excluded from the bounded candidate. No new owner/technical approval inferred.'},'results':results}
 (HOME/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(results,indent=2))
if __name__=='__main__':main()
