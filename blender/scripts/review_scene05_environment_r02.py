"""Isolated actual renders and support/camera validation for Great Tree r02."""
import bpy,bmesh,sys,json,time,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2];AREA=ROOT/'blender';P=AREA/'renders/scene05_environment_r02';ENV=AREA/'assets/environments/great_tree/great_tree_environment_r02.blend';SHOT=AREA/'scenes/lion_and_mouse_v6/s05_environment_r02.blend'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SHOT if '--proxies' in sys.argv else ENV),use_scripts=False);s=bpy.context.scene;s.cycles.seed=18102651;s.cycles.use_denoising=True;records=[]
manifest=P/('preview_render_manifest.json' if '--preview' in sys.argv else ('proxy_render_manifest.json' if '--proxies' in sys.argv else 'render_manifest.json'))
if manifest.exists():records=json.loads(manifest.read_text())
def render(name,camera,size=960,samples=40):
 s.camera=bpy.data.objects[camera];s.render.resolution_x=size;s.render.resolution_y=round(size*9/16);s.cycles.samples=samples;s.render.filepath=str(P/(name+'.png'))
 if '--resume' in sys.argv and any(r['name']==name and r['environment_sha256']==sha(ENV) and (P/(name+'.png')).exists() and r['sha256']==sha(P/(name+'.png')) for r in records):return
 start=time.perf_counter();bpy.ops.render.render(write_still=True);records[:]=[r for r in records if r['name']!=name]
 records.append({'name':name,'path':name+'.png','sha256':sha(P/(name+'.png')),'environment_sha256':sha(ENV),'scene_sha256':sha(SHOT) if '--proxies' in sys.argv else None,'camera':camera,'camera_matrix':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens,'size':[s.render.resolution_x,s.render.resolution_y],'samples':samples,'seconds':round(time.perf_counter()-start,3),'engine':'Cycles CPU','color':'Standard / None / exposure0 / gamma1'});manifest.write_text(json.dumps(records,indent=2))
if '--audit-only' in sys.argv:pass
elif '--preview' in sys.argv:render('preview_wide','CAM_S05_GEOGRAPHY_WIDE_R02',768,24);sys.exit()
if '--proxies' in sys.argv:
 c=bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'];c.hide_render=False;render('route_proxy_overlay','CAM_S05_GEOGRAPHY_WIDE_R02',960,32);render('root_proxy_detail','CAM_GT_ROOT_CONTACT_DETAIL_R02',960,32);sys.exit()
for name,cam in ([] if '--audit-only' in sys.argv else [('environment_wide','CAM_S05_GEOGRAPHY_WIDE_R02'),('interaction_crop_study','CAM_S05_P02_PROPOSED_CROP_STUDY_R02'),('root_contact_detail','CAM_GT_ROOT_CONTACT_DETAIL_R02'),('overview_diagnostic','CAM_GT_OVERVIEW_DIAGNOSTIC_R02'),('envelope_left','CAM_GT_ENVELOPE_LEFT'),('envelope_right','CAM_GT_ENVELOPE_RIGHT')]):render(name,cam,960,48 if name=='environment_wide' else 32)
# Fixed geometry under neutral light, isolate material vs sunset interpretation.
for ob in bpy.data.collections['GT_DUSK_LIGHT_R02'].objects:ob.data.color=(1,1,1)
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.4,.4,.4,1)
if '--audit-only' not in sys.argv:render('environment_neutral_light','CAM_S05_GEOGRAPHY_WIDE_R02',960,32)
# Measure actual visible support geometry and registered projections, no beauty inference.
bpy.ops.wm.open_mainfile(filepath=str(SHOT),use_scripts=False);s=bpy.context.scene;cam=bpy.data.objects['CAM_S05_GEOGRAPHY_WIDE_R02'];bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
targets={'OAK_BASE':(.69,.59),'STONE_CENTER_LEFT':(.26,.69),'ROCK_RIGHT':(.94,.67),'MOUND_LEFT':(.055,.66),'ROOT_APPROACH_START':(.03,.67),'ROOT_APPROACH_TIP':(.49,.86),'STREAM_GLIMPSE':(.14,.53)};projections={}
for name,(u,v) in targets.items():
 p=world_to_camera_view(s,cam,bpy.data.objects['ANCHOR_'+name].matrix_world.translation);projections[name]={'target_uv':[u,v],'actual_uv':[p.x,1-p.y],'pixel_error_at_1920':math.hypot((p.x-u)*1920,(1-p.y-v)*1080)}
support=[]
for name in ['SURF_CLEARING','SURF_PATH']:
 o=bpy.data.objects[name];ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();tree=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[t.vertices for t in me.loop_triangles],all_triangles=True);support.append((name,tree));ev.to_mesh_clear()
route=[bpy.data.objects['ROUTE_MILO_%02d'%i].matrix_world.translation for i in range(7)];samples=[]
for a,b in zip(route,route[1:]):
 for j in range(11):
  p=a.lerp(b,j/10);hits=[]
  for name,tree in support:
   hit,normal,_,_=tree.ray_cast(Vector((p.x,p.y,2)),Vector((0,0,-1)))
   if hit is not None:hits.append((hit.z,name,normal.z))
  best=max(hits) if hits else None;samples.append({'xy':[p.x,p.y],'height':best[0] if best else None,'surface':best[1] if best else None,'normal_z':best[2] if best else None})
# Visible approach root collision clearance for a .06 BU route-radius proxy.
root=bpy.data.objects['ROOT_APPROACH_A'];ev=root.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();tree=BVHTree.FromPolygons([root.matrix_world@v.co for v in me.vertices],[t.vertices for t in me.loop_triangles],all_triangles=True);clearances=[]
for a,b in zip(route,route[1:]):
 for j in range(11):
  p=a.lerp(b,j/10)+Vector((0,0,.07));_,_,_,distance=tree.find_nearest(p);clearances.append(distance)
ev.to_mesh_clear()
bm=bmesh.new();bm.from_mesh(bpy.data.objects['OAK_MAIN'].data);wood_nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
height=bpy.data.objects['PROXY_MILO_025_NOT_CHARACTER'].dimensions.z;checks={'main_oak_closed_manifold':wood_nonmanifold==0,'all_route_samples_hit_visible_support':all(x['height'] is not None for x in samples),'route_slope_normal_z_above_099':all(x['normal_z']>.99 for x in samples),'ground_steps_below_002_bu':max(x['height'] for x in samples)-min(x['height'] for x in samples)<.02,'milo_neutral_height_ratio_025':abs(height/1.5-.25)<1e-6,'relative_link_resolves':all(lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists() for lib in bpy.data.libraries),'landmark_anchor_projection_within_1px':all(x['pixel_error_at_1920']<1 for x in projections.values()),'root_route_clearance_over_006':min(clearances)>.06,'no_character_mesh_in_default_beauty':bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'].hide_render,'all_environment_file_images_packed':all(im.packed_file for im in bpy.data.images if im.source=='FILE')}
r={'environment_sha256':sha(ENV),'scene_sha256':sha(SHOT),'checks':checks,'landmark_projections':projections,'route_support_samples':samples,'main_oak_nonmanifold_edges':wood_nonmanifold,'minimum_route_root_clearance_bu':min(clearances),'measured_proxy_height_bu':height,'limits':'Contact corridor / simple proxies only. No Leo lying pose, paw/nose performance or complete collision qualification. Projection checks use authored anchor points, not silhouette matching.','objects':len(bpy.data.objects),'mesh_faces':sum(len(o.data.polygons) for o in bpy.data.objects if o.type=='MESH')};(P/'validation.json').write_text(json.dumps(r,indent=2));print('ENV_REVIEW_COMPLETE',json.dumps(checks),flush=True)
