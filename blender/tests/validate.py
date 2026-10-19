"""Blender integration checks against actual saved files and evaluated rig."""
import bpy
import sys
import json
import hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'blender'
sys.path.insert(0,str(A/'scripts'))
from poses import apply_pose
checks=[]


def check(condition,description):
    checks.append({'check':description,'pass':bool(condition)})
    if not condition:print('FAIL:',description)


cfg=json.loads((A/'config/authority.json').read_text())
for path,sha in cfg['sources'].items():
    check((ROOT/path).exists() and hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,'source unchanged: '+path)
bpy.ops.wm.open_mainfile(filepath=str(A/'assets/characters/leo/leo_canonical_candidate.blend'))
rig=bpy.data.objects['Leo_RIG'];apply_pose(rig,'neutral');bpy.context.view_layer.update()
check(len([b for b in rig.pose.bones if b.name.startswith('CTRL_')])==4,'four independent planted paw controls')
check(all(rig.pose.bones[t+'_lower'].constraints.get('Planted_paw_IK') for t in ['front_L','front_R','hind_L','hind_R']),'four two-bone IK chains')
deps=bpy.context.evaluated_depsgraph_get()
rest={}
for tag in ['front_L','front_R','hind_L','hind_R']:
    o=bpy.data.objects['Leo_paw_'+tag];ev=o.evaluated_get(deps)
    bottom=min((ev.matrix_world@Vector(v)).z for v in ev.bound_box)
    rest[tag]=ev.matrix_world@ev.data.vertices[0].co
    check(abs(bottom)<.025,'neutral grounded paw '+tag)
# A real deformation test: move a target and verify corresponding paw follows.
ctrl=rig.pose.bones['CTRL_front_L'];ctrl.location[0]+=.08;bpy.context.view_layer.update()
ev=bpy.data.objects['Leo_paw_front_L'].evaluated_get(bpy.context.evaluated_depsgraph_get())
check(((ev.matrix_world@ev.data.vertices[0].co)-rest['front_L']).length>.045,'IK target actually moves evaluated front-left paw')
apply_pose(rig,'neutral')
# Body lowering must leave all four targets planted, with no bone stretch.
rig.pose.bones['hips'].location=rig.pose.bones['hips'].bone.matrix_local.to_3x3().inverted() @ Vector((0,0,-.10))
bpy.context.view_layer.update()
for tag in rest:
    ev=bpy.data.objects['Leo_paw_'+tag].evaluated_get(bpy.context.evaluated_depsgraph_get())
    check(((ev.matrix_world@ev.data.vertices[0].co)-rest[tag]).length<.005,'paw stays planted under body motion: '+tag)
apply_pose(rig,'neutral')
stats={'meshes':0,'vertices':0,'polygons':0,'curve_splines':0,'bones':len(rig.data.bones)}
for o in bpy.data.collections['LEO_CANDIDATE'].objects:
    if o.type=='MESH':
        stats['meshes']+=1;stats['vertices']+=len(o.data.vertices);stats['polygons']+=len(o.data.polygons)
    elif o.type=='CURVE':stats['curve_splines']+=len(o.data.splines)
check(all(p.scale==Vector((1,1,1)) for p in rig.pose.bones),'neutral rig has no anatomical scaling')
# Fibers must receive the same rest-to-pose transform as their supporting mesh.
from mathutils.bvhtree import BVHTree
attached=[]
for ob in bpy.data.collections['LEO_CANDIDATE'].objects:
    if not ob.name.endswith('_fibers'):continue
    mesh=bpy.data.objects.get(ob.name.removesuffix('_fibers'))
    if mesh is None:continue
    dep=bpy.context.evaluated_depsgraph_get();fiber=ob.evaluated_get(dep);ev=mesh.evaluated_get(dep)
    tree=BVHTree.FromObject(mesh,dep)
    start=fiber.matrix_world @ Vector(fiber.data.splines[0].points[0].co[:3])
    local=ev.matrix_world.inverted() @ start
    hit=tree.find_nearest(local)
    attached.append(hit[3]<.025)
check(attached and all(attached),'surface fibers follow evaluated neutral mesh transforms')
for name in ['walk','lie','struggle','head_turn']:
    apply_pose(rig,name);bpy.context.view_layer.update()
    check(all(all(abs(v)<100 for row in p.matrix for v in row) for p in rig.pose.bones),'finite rig evaluation: '+name)
bpy.ops.wm.open_mainfile(filepath=str(A/'scenes/lion_and_mouse_v6/s05.blend'))
check(bpy.data.objects.get('Great_oak_trunk') is not None,'linked environment resolved after reopen')
check(bpy.data.objects.get('Foreground_stumble_root') is not None,'r02 stumble root present')
check(bpy.data.objects.get('CAM_s05_wide') is not None,'representative wide camera available')
check(len([o for o in bpy.data.objects if o.type=='CAMERA'])>=7,'registered crop cameras available')
rig=bpy.data.objects['Leo_RIG'];p=bpy.data.objects['Milo_SCALE_PROXY']
check(abs(p['neutral_height']/rig['neutral_height']-.25)<1e-6,'Milo proxy / neutral Leo exactly .25')
check(p.hide_render and not p['production_asset'],'proxy clearly non-production and hidden')
check(all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries),'all linked libraries resolve')
check(all(l.filepath.startswith('//') for l in bpy.data.libraries),'library paths repository-relative')
check(bpy.context.scene.view_settings.view_transform=='Standard','deliberate Standard color management')
# Verify optical crop math against projected world points, not just camera names.
from bpy_extras.object_utils import world_to_camera_view
scene=bpy.context.scene;wide=bpy.data.objects['CAM_s05_wide']
for cam in [o for o in bpy.data.objects if o.type=='CAMERA' and o.get('source_frame')]:
    x,y,w,h=cam['crop_rect_on_plate'];errors=[]
    for point in [Vector((0,2,1)),Vector((3.5,5.2,.5)),Vector((-3,.1,.2))]:
        a=world_to_camera_view(scene,wide,point);b=world_to_camera_view(scene,cam,point)
        expect_x=(a.x-x)/w;expect_y=(a.y-(1-y-h))/h
        errors.append(max(abs(b.x-expect_x),abs(b.y-expect_y)))
    check(max(errors)<.001,'camera projection follows registered crop: '+cam['source_frame'])
# Save calibration diagnostics even when artistic fit remains poor.
landmarks={'oak_base':(3.5,5.2,0),'left_stone':(-3,2,.27),'right_rock':(5.6,1,.52),'root_tip':(-.7,-1.5,.045)}
projected={}
for name,co in landmarks.items():
    p=world_to_camera_view(scene,wide,Vector(co));projected[name]=[round(p.x,4),round(1-p.y,4)]
(A/'renders/camera_landmarks.json').write_text(json.dumps({'status':'provisional_not_approved','normalized_top_left':projected},indent=2)+'\n')
env_stats={'mesh_polygons':sum(len(o.data.polygons) for o in bpy.data.collections['GREAT_TREE_CANDIDATE'].objects if o.type=='MESH'),'curve_splines':sum(len(o.data.splines) for o in bpy.data.collections['GREAT_TREE_CANDIDATE'].objects if o.type=='CURVE'),'objects':len(bpy.data.collections['GREAT_TREE_CANDIDATE'].objects)}
result={'environment_statistics':env_stats,'checks':checks,'leo_statistics':stats,'passed':sum(c['pass'] for c in checks),'total':len(checks),'blender':bpy.app.version_string}
(A/'renders/validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not all(c['pass'] for c in checks):raise RuntimeError('Prototype structural validation failed')
