"""Reopen actual linked r03; render and audit without saving mutations."""
import bpy,sys,json,time,hashlib,math,bmesh
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'blender';P=A/'renders/scene05_environment_r03'
ENV=A/'assets/environments/great_tree/great_tree_environment_r03.blend';SHOT=A/'scenes/lion_and_mouse_v6/s05_environment_r03.blend'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SHOT),use_scripts=False);s=bpy.context.scene;s.cycles.use_denoising=True;s.cycles.device='CPU';s.cycles.seed=510318
wide=bpy.data.objects['CAM_S05_GEOGRAPHY_WIDE_R02'];s.camera=wide
records=[];manifest=P/('preview_manifest.json' if '--preview' in sys.argv else 'render_manifest.json')
if manifest.exists():records=json.loads(manifest.read_text())
def render(name,cam,width=1280,samples=48):
 s.camera=bpy.data.objects[cam];s.render.resolution_x=width;s.render.resolution_y=round(width*9/16);s.render.resolution_percentage=100;s.cycles.samples=samples;s.render.filepath=str(P/(name+'.png'));s.render.image_settings.color_mode='RGB'
 start=time.perf_counter();bpy.ops.render.render(write_still=True)
 records.append({'name':name,'sha256':sha(P/(name+'.png')),'scene_sha256':sha(SHOT),'environment_sha256':sha(ENV),'camera':cam,'matrix':[list(x) for x in s.camera.matrix_world],'lens':s.camera.data.lens,'shift':[s.camera.data.shift_x,s.camera.data.shift_y],'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':samples,'seconds':round(time.perf_counter()-start,2),'engine':'Cycles CPU','color':{'view':s.view_settings.view_transform,'look':s.view_settings.look,'exposure':s.view_settings.exposure,'gamma':s.view_settings.gamma},'frame':s.frame_current});manifest.write_text(json.dumps(records,indent=2))
if '--preview' in sys.argv:render('preview_wide',wide.name,960,32);sys.exit()
if '--audit-only' not in sys.argv:
 render('environment_wide',wide.name,1920,64)
 render('interaction_crop_study','CAM_S05_P02_PROPOSED_CROP_STUDY_R02')
 render('root_contact_detail','CAM_GT_ROOT_CONTACT_DETAIL_R02')
 render('envelope_left','CAM_GT_ENVELOPE_LEFT',960,32)
 render('envelope_right','CAM_GT_ENVELOPE_RIGHT',960,32)
 # Local light data copies keep library on disk immutable.
 neutral=bpy.data.collections.new('R03_NEUTRAL_DIAGNOSTIC_LIGHTS');s.collection.children.link(neutral)
 for o in bpy.data.collections['GT_DUSK_LIGHT_R02'].objects:
  duplicate=o.copy();duplicate.data=o.data.copy();duplicate.data.color=(1,1,1);neutral.objects.link(duplicate)
 s.view_layers[0].layer_collection.children['GT_DUSK_LIGHT_R02'].exclude=True
 s.world.node_tree.nodes['Background'].inputs[0].default_value=(.4,.4,.4,1)
 render('environment_neutral_light',wide.name,1280,40)
bpy.ops.wm.open_mainfile(filepath=str(SHOT),use_scripts=False);s=bpy.context.scene;s.camera=bpy.data.objects['CAM_S05_GEOGRAPHY_WIDE_R02'];bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
def bvh(ob):
 ev=ob.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();t=BVHTree.FromPolygons([ob.matrix_world@v.co for v in me.vertices],[f.vertices for f in me.loop_triangles],all_triangles=True);ev.to_mesh_clear();return t
supports={name:bvh(bpy.data.objects[name]) for name in ['SURF_CLEARING','SURF_PATH']};root=bvh(bpy.data.objects['ROOT_APPROACH_A']);samples=[];clearances=[]
route=[bpy.data.objects['ROUTE_MILO_%02d'%i].matrix_world.translation for i in range(7)]
for a,b in zip(route,route[1:]):
 for j in range(11):
  p=a.lerp(b,j/10);hits=[]
  for name,t in supports.items():
   hit,n,_,_=t.ray_cast(Vector((p.x,p.y,2)),Vector((0,0,-1)))
   if hit is not None:hits.append((hit.z,name,n.z))
  best=max(hits) if hits else None;samples.append({'xy':[p.x,p.y],'support':best})
  _,_,_,d=root.find_nearest(p+Vector((0,0,.07)));clearances.append(d)
bm=bmesh.new();bm.from_mesh(bpy.data.objects['OAK_MAIN'].data);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
before=json.loads((P/'preserved_sources_before.json').read_text());preservation=[dict(x,unchanged=sha(ROOT/x['path'])==x['sha256']) for x in before]
checks={'all_preserved_source_hashes_unchanged':all(x['unchanged'] for x in preservation),'relative_library_resolves':all(lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists() for lib in bpy.data.libraries),'packed_image_dependencies':all(im.packed_file for im in bpy.data.images if im.source=='FILE'),'all_66_route_samples_hit_support':all(x['support'] for x in samples),'route_normals_above_099':all(x['support'] and x['support'][2]>.99 for x in samples),'route_ground_steps_below_002':max(x['support'][0] for x in samples)-min(x['support'][0] for x in samples)<.02,'root_route_clearance_over_006':min(clearances)>.06,'oak_base_mesh_closed':nonmanifold==0,'proxies_hidden':bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'].hide_render,'proxy_ratio_025':abs(bpy.data.objects['PROXY_MILO_025_NOT_CHARACTER'].dimensions.z/1.5-.25)<1e-6}
result={'checks':checks,'minimum_route_root_clearance_bu':min(clearances),'oak_base_nonmanifold_edges':nonmanifold,'route_samples':samples,'source_preservation':preservation,'libraries':[lib.filepath for lib in bpy.data.libraries],'scene_sha256':sha(SHOT),'environment_sha256':sha(ENV),'limits':'Still candidate only; anchor projections are not silhouette validation. No Leo performance, motion stability, large camera travel, or owner approval.'}
(P/'validation.json').write_text(json.dumps(result,indent=2));print('R03_AUDIT',json.dumps(checks),flush=True)
