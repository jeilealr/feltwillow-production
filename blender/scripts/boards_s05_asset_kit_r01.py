"""Assemble actual comparison renders; no generated art, new renders or grading."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageCms
import json
R=Path(__file__).resolve().parents[2];P=R/'blender/renders/s05_asset_kit_r01';profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
def board(light,view):
 w=640;h=360;b=Image.new('RGB',(w*3,h+66),'#242729');d=ImageDraw.Draw(b)
 for i,(stage,label) in enumerate([('prior','PRIOR: native r04 recipe'),('imported','IMPORTED: unadapted baseline'),('adapted','ADAPTED ATTEMPT: mixed / rejected components')]):
  im=Image.open(P/(stage+'_'+light+'_'+view+'.png')).convert('RGB').resize((w,h),Image.Resampling.LANCZOS);b.paste(im,(i*w,32));d.text((i*w+8,10),label,fill='white')
 d.text((8,h+45),'Maps: Poly Haven - Rico Cilliers / colormass (CC0) | Mesh bases: Kenney Nature Kit 2.1 (CC0) | fixed '+light+' setup; pending owner review',fill='white');b.save(P/('comparison_'+light+'_'+view+'.png'),icc_profile=profile)
for light in ['neutral','dusk']:
 for view in ['shot','close']:board(light,view)
# Same-coordinate original-pixel crops make relief and topology failures explicit.
for region,box in [('stump',(0,215,465,650)),('moss',(440,380,720,540)),('rock_leaf',(710,235,1280,600))]:
 images=[Image.open(P/(stage+'_neutral_shot.png')).convert('RGB').crop(box) for stage in ['prior','imported','adapted']];w,h=images[0].size;b=Image.new('RGB',(w*3,h+34),'#242729');d=ImageDraw.Draw(b)
 for i,(im,label) in enumerate(zip(images,['Prior','Imported baseline','Adapted attempt - see verdict'])):b.paste(im,(w*i,34));d.text((w*i+6,10),label,fill='white')
 b.save(P/(region+'_matched_crop.png'),icc_profile=profile)
rows=json.loads((P/'render_manifest.json').read_text());print('Existing renders assembled:',len(rows),'true render seconds:',round(sum(x['seconds'] for x in rows),2),'cumulative process maxrss bytes:',max(x['process_maxrss_bytes_macos'] for x in rows))
