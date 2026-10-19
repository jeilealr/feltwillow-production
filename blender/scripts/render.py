"""Render saved assets; --target leo|s05|benchmark|rig, --samples N, --size N."""
import bpy
import sys
import json
import time
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
AREA=ROOT/'blender'
sys.path.insert(0,str(AREA/'scripts'))
from poses import apply_pose


def arg(key,default):
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    return args[args.index(key)+1] if key in args else default

TARGET=arg('--target','leo');SAMPLES=int(arg('--samples','24'));SIZE=int(arg('--size','640'))
records=[]


def render(name,folder,engine='CYCLES'):
    s=bpy.context.scene;s.render.engine=engine
    if engine=='CYCLES':s.cycles.samples=SAMPLES;s.cycles.use_denoising=True
    s.render.resolution_x=SIZE;s.render.resolution_y=SIZE if TARGET in {'leo','rig','benchmark'} else round(SIZE*9/16)
    path=AREA/folder/(name+'.png');path.parent.mkdir(parents=True,exist_ok=True)
    s.render.filepath=str(path);start=time.perf_counter();bpy.ops.render.render(write_still=True)
    rec={'image':str(path.relative_to(ROOT)),'engine':engine,'samples':SAMPLES if engine=='CYCLES' else None,
         'resolution':[s.render.resolution_x,s.render.resolution_y],'seconds':round(time.perf_counter()-start,3),
         'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'blender':bpy.app.version_string,
         'camera':s.camera.name,'status':'prototype_needs_visual_review',
         'input_blend':str(Path(bpy.data.filepath).relative_to(ROOT)),
         'input_blend_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
         'authority_sha256':hashlib.sha256((AREA/'config/authority.json').read_bytes()).hexdigest(),
         'rig_pose':bpy.data.objects['Leo_RIG'].get('active_pose','neutral'),
         'linked_library_sha256':{l.filepath:hashlib.sha256(Path(bpy.path.abspath(l.filepath)).read_bytes()).hexdigest() for l in bpy.data.libraries}}
    records.append(rec)
    # Write after each completed image to retain actual timing after interruption.
    (AREA/f'renders/{TARGET}_manifest.json').write_text(json.dumps(records,indent=2)+'\n')


if TARGET in {'leo','benchmark','rig'}:
    bpy.ops.wm.open_mainfile(filepath=str(AREA/'assets/characters/leo/leo_canonical_candidate.blend'))
    c=bpy.context.scene.camera
    from mathutils import Vector
    views={'front':((0,-8,1.8),(0,.1,.72),2.6),
           'left':((-8,0,2),(0,.25,.72),3.1),
           'right':((8,0,2),(0,.25,.72),3.1),
           'rear':((0,8,1.8),(0,.15,.72),2.6),
           'front_three_quarter':((2.5,-4,1.7),(0,.1,.72),2.65),
           'rear_three_quarter':((-3,4,1.8),(0,.15,.72),2.65),
           'elevated_three_quarter':((2.8,-4,3),(0,.1,.7),2.8),
           'portrait':((0,-4,1.08),(0,-.55,1.04),1.1)}
    if TARGET=='leo':
        for name,(loc,target,ortho) in views.items():
            c.location=loc;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=ortho
            render(name,'renders/reference/leo')
    elif TARGET=='benchmark':
        render('cycles','renders/diagnostic/engine_comparison')
        render('eevee','renders/diagnostic/engine_comparison','BLENDER_EEVEE')
    else:
        rig=bpy.data.objects['Leo_RIG']
        for pose in ['neutral','walk','lie','struggle','head_turn']:
            apply_pose(rig,pose);bpy.context.view_layer.update();render(pose,'renders/diagnostic/rig')
elif TARGET=='s05':
    bpy.ops.wm.open_mainfile(filepath=str(AREA/'scenes/lion_and_mouse_v6/s05.blend'))
    render('s05_p01_wide','renders/reference/s05')
    leo=bpy.data.collections['LEO_CANDIDATE']
    leo.hide_render=True
    render('environment_wide','renders/reference/s05')
    leo.hide_render=False
    for name in ['CAM_s05_medium_two_s05_p04','CAM_s05_close_two_s05_p03','CAM_s05_owner_s05x_p04_camera_s05x_p04']:
        bpy.context.scene.camera=bpy.data.objects[name]
        render(name.removeprefix('CAM_'),'renders/reference/s05')
else:raise ValueError(TARGET)
