"""Explicit display resampling and matched-coordinate comparison evidence."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageCms
import json,hashlib,sys
R=Path(__file__).resolve().parents[2];P=R/'blender/renders/scene05_environment_r03';W,H=960,540
sys.path.insert(0,str(R/'.claude/skills/feltwillow-blender-production/scripts'))
from scene_match import compare
profile=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
source=R/'character/locations/lion_and_mouse_v6/great_tree/tree_dusk_r02.png'
im=Image.open(source).convert('RGB');sw,sh=im.size;wanted=sw*9/16;trim=(sh-wanted)/2;box=(0,trim,sw,sh-trim)
ref=im.resize((W,H),Image.Resampling.LANCZOS,box=box)
ref.save(P/'reference_display_960.png',icc_profile=profile)
base=Image.open(R/'blender/renders/scene05_environment_r02/environment_wide.png').convert('RGB')
cur=Image.open(P/'environment_wide.png').convert('RGB').resize((W,H),Image.Resampling.LANCZOS);cur.save(P/'candidate_display_960.png',icc_profile=profile)
base.save(P/'baseline_display_960.png',icc_profile=profile)
points=[
 ('sun_center',[.075,.350],[.075,.345]),
 ('trunk_left_at_030',[.582,.300],[.607,.300]),
 ('trunk_right_at_030',[.790,.300],[.792,.300]),
 ('trunk_left_at_045',[.551,.450],[.575,.450]),
 ('right_rock_crest',[.952,.552],[.952,.519]),
 ('left_stone_crest',[.253,.641],[.267,.623]),
 ('approach_root_fine_tip',[.586,.866],[.490,.860]),
 ('stream_visible_center',[.149,.537],[.149,.500]),
 ('path_left_edge_at_082',[.575,.820],[.580,.820]),
 ('canopy_low_cluster_near_center',[.365,.240],[.500,.255]),
]
landmarks={'schema':'feltwillow.scene-match-landmarks.v1','coordinate_system':'normalized_top_left_pixel_centers','reference_sha256':sha(P/'reference_display_960.png'),'render_sha256':sha(P/'candidate_display_960.png'),'points':[{'id':name,'reference_xy':a,'render_xy':b,'uncertainty':'Agent visual estimate, typically +/-0.015 normalized; crown cluster identity +/-0.04; not surveyed, not a solved camera, not an aesthetic score'} for name,a,b in points]}
(P/'landmarks.json').write_text(json.dumps(landmarks,indent=2))
compare(P/'reference_display_960.png',P/'candidate_display_960.png',P/'comparison_final',landmarks=P/'landmarks.json',assume_srgb=True)
compare(P/'reference_display_960.png',P/'baseline_display_960.png',P/'comparison_baseline',assume_srgb=True)
board=Image.new('RGB',(W*3,H+42),'#202225');d=ImageDraw.Draw(board)
for i,(label,image) in enumerate([('APPROVED DUSK GEOGRAPHY',ref),('R02 BASELINE - actual Cycles render',base),('R03 REFINEMENT PROTOTYPE - needs revision',cur)]):
 board.paste(image,(i*W,42));d.text((i*W+12,14),label,fill='white')
board.save(P/'before_after_board.png',icc_profile=profile)
for name,box in [('tree_roots',(490,100,850,365)),('path_rock_stream',(0,270,960,540))]:
 parts=[x.crop(box) for x in [ref,base,cur]];cw,ch=parts[0].size;b=Image.new('RGB',(cw*3,ch+28),'#202225');d=ImageDraw.Draw(b)
 for i,(lab,part) in enumerate(zip(['Approved','r02','r03 prototype'],parts)):b.paste(part,(i*cw,28));d.text((i*cw+5,7),lab,fill='white')
 b.save(P/(name+'_matched_crops.png'),icc_profile=profile)
meta={'source':str(source.relative_to(R)),'source_sha256':sha(source),'source_size':[sw,sh],'explicit_source_crop_px':[0,trim,sw,sh-trim],'display_size':[W,H],'method':'center trim 0.25 source pixel top/bottom to exact 16:9; Lanczos resize; candidate downsample from 1920x1080; no landmark warping or color matching','srgb':'explicit sRGB assumption for untagged owner source and Blender Standard PNGs','approval':'needs_revision; diagnostics do not grant owner acceptance'}
(P/'comparison_preparation.json').write_text(json.dumps(meta,indent=2))
print('Comparison board, overlays, differences and two matched-coordinate crops written.')
