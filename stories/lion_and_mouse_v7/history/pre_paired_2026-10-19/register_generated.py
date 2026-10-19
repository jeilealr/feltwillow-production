#!/usr/bin/env python3
"""Register a built-in ImageGen transparent foreground layer as one v7 composite candidate."""
import argparse, hashlib, json, shutil, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import tools_compose
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('unit_id');p.add_argument('generated_png');a=p.parse_args()
plan_path=ROOT/'stories/lion_and_mouse_v7/visual_unit_plan.json';data=json.loads(plan_path.read_text());u=next(x for x in data['units'] if x['id']==a.unit_id)
layer=ROOT/u['character_layer'];layer.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.generated_png,layer)
zoom=u['camera_view']['zoom_factor'];cx,cy=u['camera_view']['crop_center_norm'];height=max(u['character_height_targets'].values()); center=.5;ground=u['staging'].get('ground_y_norm',.84)
params=tools_compose.composite(ROOT/u['location_plate'],layer,ROOT/u['image_path'],height,center,ground,zoom,cx,cy)
u['composite_transform']={**params,'method':'generated transparent character layer over registered location crop','background_source':u['location_plate'],'layer_source':str(layer.relative_to(ROOT)),'background_pixels_outside_character_and_contact_shadow':'source plate crop, never regenerated'}
u['status']='generated_candidate_needs_visual_review'
u['sha256']=hashlib.sha256((ROOT/u['image_path']).read_bytes()).hexdigest()
data['status']='scene candidates in progress; technical image review required; owner approval pending'
plan_path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'id':u['id'],'image':u['image_path'],'layer':u['character_layer'],'sha256':u['sha256'],'transform':params}))
