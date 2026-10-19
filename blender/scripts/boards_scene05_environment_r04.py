"""Existing-image evidence assembly only; explicit resampling, no art generation."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageCms,ImageChops,ImageStat
import json,hashlib
R=Path(__file__).resolve().parents[2];P=R/'blender/renders/scene05_environment_r04';profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def board(name,files,labels,width=800):
 height=round(width*9/16);b=Image.new('RGB',(width*len(files),height+36),'#242729');d=ImageDraw.Draw(b)
 for i,(file,label) in enumerate(zip(files,labels)):
  im=Image.open(P/file).convert('RGB').resize((width,height),Image.Resampling.LANCZOS);b.paste(im,(i*width,36));d.text((i*width+9,12),label,fill='white')
 b.save(P/name,icc_profile=profile)
board('baseline_and_r04.png',['baseline_saved_settings.png','establishing.png'],['r03 actual SAVED settings - preserved baseline','r04 reference_inspired - refinement prototype'])
if (P/'r03_fixed_new_camera.png').exists():board('fixed_camera_before_after.png',['r03_fixed_new_camera.png','establishing.png'],['r03 through NEW r04 camera; original r03 light','r04 SAME camera; designed geometry/material/light changes'])
board('craft_kit_neutral_dusk.png',['kit_neutral.png','kit_dusk.png'],['Native craft samples - neutral','Same samples - dusk'])
board('material_contribution_AB.png',['material_A_flat_families.png','material_B_native_craft.png'],['A: flat family shading; geometry/fibers retained','B: native shader detail - SAME lights/camera/seed'],960)
board('existing_height_contribution_AB.png',['material_B_native_craft.png','existing_height_map_trial.png'],['A: delivered native shader','B: EXISTING packed height on bark only; render-only'],960)
metrics={}
for key,a,b in [('native_shader','material_A_flat_families.png','material_B_native_craft.png'),('existing_height','material_B_native_craft.png','existing_height_map_trial.png')]:
 ia=Image.open(P/a).convert('RGB');ib=Image.open(P/b).convert('RGB');assert ia.size==ib.size;diff=ImageChops.difference(ia,ib);diff.save(P/(key+'_difference.png'),icc_profile=profile);metrics[key]={'A_sha256':sha(P/a),'B_sha256':sha(P/b),'mean_display_channel_absolute_difference':ImageStat.Stat(diff).mean,'warning':'Encoded pixel differences prove a render changed; not a felt score or approval.'}
 # Same-coordinate 1:1 detail crops, not rescaled for a flattering comparison.
 box=(150,360,950,620);ca=ia.crop(box);cb=ib.crop(box);out=Image.new('RGB',(ca.width*2,ca.height+28),'#242729');out.paste(ca,(0,28));out.paste(cb,(ca.width,28));d=ImageDraw.Draw(out);d.text((8,7),'A - same pixel crop',fill='white');d.text((ca.width+8,7),'B - same pixel crop',fill='white');out.save(P/(key+'_detail_AB.png'),icc_profile=profile)
b=Image.new('RGB',(1440,600),'#242729');d=ImageDraw.Draw(b)
for i,name in enumerate(['establishing','medium_actor_clean','root_contact_detail','envelope_left','envelope_right','neutral_material_diagnostic']):
 im=Image.open(P/(name+'.png')).convert('RGB').resize((480,270),Image.Resampling.LANCZOS);x=(i%3)*480;y=(i//3)*300;b.paste(im,(x,y+30));d.text((x+7,y+10),name,fill='white')
b.save(P/'review_views.png',icc_profile=profile)
board('proxy_test_labeled.png',['medium_scale_contact_proxies.png'],['DIAGNOSTIC PROXIES ONLY: rest volume, Milo .25 ratio, route + paw/nose markers'],1280)
(P/'comparison_metrics.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
