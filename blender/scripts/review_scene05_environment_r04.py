"""Actual linked-shot renders, controlled shader A/B and scoped support audit."""
import bpy,sys,json,time,hashlib,bmesh,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];A=R/'blender';P=A/'renders/scene05_environment_r04';E=A/'assets/environments/great_tree/great_tree_environment_r04.blend';S=A/'scenes/lion_and_mouse_v6/s05_environment_r04.blend'
sys.path.insert(0,str(A/'scripts'));import craft_scene05_r04 as c
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def open_shot():
 bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);s=bpy.context.scene;s.cycles.device='CPU';s.cycles.use_denoising=True;s.cycles.seed=510400;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';return s
s=open_shot();records=[]
manifest=P/('preview_render_manifest.json' if '--preview' in sys.argv else 'render_manifest.json')
if manifest.exists():records=json.loads(manifest.read_text())
def obj(name):return s.objects.get(name) or next(o for o in s.objects if o.name.startswith(name))
def render(name,cam,width=1280,samples=40,state='dusk'):
 s.camera=obj(cam);s.render.resolution_x=width;s.render.resolution_y=round(width*9/16);s.cycles.samples=samples;s.render.filepath=str(P/(name+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True)
 records.append({'name':name,'sha256':sha(P/(name+'.png')),'environment_sha256':sha(E),'shot_sha256':sha(S),'camera':s.camera.name,'matrix':[list(x) for x in s.camera.matrix_world],'lens':s.camera.data.lens,'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':samples,'seconds':round(time.perf_counter()-t,3),'frame':s.frame_current,'seed':510400,'denoising':True,'engine':'Cycles CPU','color':[s.view_settings.view_transform,s.view_settings.look,s.view_settings.exposure,s.view_settings.gamma],'lighting_state':state});manifest.write_text(json.dumps(records,indent=2))
if '--preview' in sys.argv:render('layout_preview','CAM_S05_ESTABLISHING_R04',960,28);sys.exit()
if '--audit-only' not in sys.argv:
 render('establishing','CAM_S05_ESTABLISHING_R04',1600,48)
 render('medium_actor_clean','CAM_S05_MEDIUM_ACTOR_R04',1280,40)
 render('root_contact_detail','CAM_S05_ROOT_CONTACT_R04',1280,40)
 render('envelope_left','CAM_S05_ENVELOPE_LEFT_R04',960,28)
 render('envelope_right','CAM_S05_ENVELOPE_RIGHT_R04',960,28)
 # Labeled geometric space/size tests, never character likeness or an action performance.
 proxy=bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'];proxy.hide_render=False
 render('medium_scale_contact_proxies','CAM_S05_MEDIUM_ACTOR_R04',1280,40,'dusk, labeled geometric scale/contact proxies enabled')
 proxy.hide_render=True
 # A/B on same curved root/ground camera; no geometry, light, exposure, sampling change.
 render('material_B_native_craft','CAM_S05_ROOT_CONTACT_R04',1280,40,'unchanged dusk B')
 changes=[]
 # Assign local material copies only to scene objects; source .blend never saved by review.
 copies={}
 def render_objects(col,enabled=True):
  result=set()
  if not enabled or col.hide_render:return result
  result.update(o for o in col.objects if not o.hide_render)
  for child in col.children:result.update(render_objects(child))
  return result
 for o in list(render_objects(s.collection)):
  if o.type not in ['MESH','CURVE']:continue
  for slot in o.material_slots:
   m=slot.material
   if not m or not m.name.startswith('R04_') or not m.use_nodes or not m.node_tree.nodes.get('Principled BSDF'):continue
   # Local object/data copy permits harmless overrides of linked materials.
   if o.library:
    local=o.copy();local.data=o.data.copy();s.collection.objects.link(local);o.hide_render=True;o=local
   key=m.name
   if key not in copies:
    new=m.copy();new.name=key+'_AB_FLAT';n=new.node_tree.nodes;l=new.node_tree.links;p=n.get('Principled BSDF')
    ground_mix=n.get('EARTH_TO_MATTED_GRASS')
    for field in (['Normal'] if ground_mix else ['Normal','Base Color']):
     for link in list(p.inputs[field].links):l.remove(link)
    if ground_mix:
     for field,hx in [(1,'9D7751'),(2,'66743B')]:
      for link in list(ground_mix.inputs[field].links):l.remove(link)
      ground_mix.inputs[field].default_value=(*c.rgb(hx),1)
    else:p.inputs['Base Color'].default_value=m.diffuse_color
    p.inputs['Sheen Weight'].default_value=0
    copies[key]=new;changes.append({'material':key,'disabled':['procedural color variation','bump/normal chain','sheen'],'retained':['base family color','roughness','same silhouette geometry','same fibers','same lights/camera/exposure/seed']})
   for local_slot in o.material_slots:
    if local_slot.material and local_slot.material.name==key:local_slot.material=copies[key]
 render('material_A_flat_families','CAM_S05_ROOT_CONTACT_R04',1280,40,'unchanged dusk A; shader variation/normal/sheen disabled')
 (P/'material_AB_changes.json').write_text(json.dumps({'type':'native shader contribution; not PATINA-map-only A/B','changes':changes,'fixed_geometry':True,'fixed_lighting':True,'not_saved_to_blend':True},indent=2))
 s=open_shot()
 # Diagnostic neutral rig in local collection, old dusk rig excluded rather than modified.
 original=next(col for col in s.collection.children if col.name.startswith('GT_DUSK_LIGHT_R04'));rig=c.collection('R04_NEUTRAL_REVIEW',s.collection)
 for o in original.objects:
  dup=o.copy();dup.data=o.data.copy();dup.data.color=(1,1,1);rig.objects.link(dup)
 s.view_layers[0].layer_collection.children[original.name].exclude=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.35,.35,.35,1)
 render('neutral_material_diagnostic','CAM_S05_ESTABLISHING_R04',1280,36,'neutral light colors; emission sky remains dusk')
s=open_shot();bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
def bvh(o):
 ev=o.evaluated_get(deps);me=ev.to_mesh();me.calc_loop_triangles();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in me.vertices],[x.vertices for x in me.loop_triangles],all_triangles=True);ev.to_mesh_clear();return t
ground=bvh(obj('SURF_CLEARING'));root=bvh(obj('ROOT_APPROACH_A'));oak=bvh(obj('OAK_MAIN'))
route=[obj('ROUTE_MILO_%02d'%i).matrix_world.translation for i in range(7)];samples=[];clearances=[];oakclear=[]
for a,b in zip(route,route[1:]):
 for j in range(11):
  p=a.lerp(b,j/10);hit,n,_,_=ground.ray_cast(Vector((p.x,p.y,2)),Vector((0,0,-1)));samples.append({'xy':[p.x,p.y],'hit_z':hit.z if hit is not None else None,'normal_z':n.z if n else None})
  _,_,_,d=root.find_nearest(p+Vector((0,0,.07)));clearances.append(d);_,_,_,d=oak.find_nearest(p+Vector((0,0,.18)));oakclear.append(d)
before=json.loads((P/'protected_sources.json').read_text());preserved=[dict(x,unchanged=sha(R/x['path'])==x['sha256']) for x in before]
rest=[]
for x in [-1.15,-.2,.75]:
 for y in [0,.4,.8]:
  hit,n,_,_=ground.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));rest.append({'xy':[x,y],'hit_z':hit.z if hit is not None else None})
checks={'all_protected_sources_unchanged':all(x['unchanged'] for x in preserved),'relative_library_resolves':all(lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).exists() for lib in bpy.data.libraries),'only_r04_environment_link':all(Path(bpy.path.abspath(lib.filepath)).name=='great_tree_environment_r04.blend' for lib in bpy.data.libraries),'packed_file_images':all(im.packed_file for im in bpy.data.images if im.source=='FILE'),'route_66_samples_supported':all(x['hit_z'] is not None for x in samples),'route_normals_over_099':all(x['normal_z'] and x['normal_z']>.99 for x in samples),'root_clearance_over_006':min(clearances)>.06,'hero_tree_route_clearance_over_015':min(oakclear)>.15,'nine_rest_support_samples':all(x['hit_z'] is not None for x in rest),'scale_proxy_ratio_025':abs(obj('PROXY_MILO_025').dimensions.z/1.5-.25)<1e-6,'default_proxies_hidden':bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'].hide_render,'mode_reference_inspired':s.get('design_mode')=='reference_inspired'}
bm=bmesh.new();bm.from_mesh(obj('OAK_MAIN').data);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();checks['oak_base_mesh_closed']=nonmanifold==0
result={'environment_sha256':sha(E),'shot_sha256':sha(S),'checks':checks,'minimum_approach_root_clearance_bu':min(clearances),'minimum_hero_tree_route_clearance_bu':min(oakclear),'route':samples,'rest_support':rest,'protected_sources':preserved,'libraries':[x.filepath for x in bpy.data.libraries],'limits':'Scoped static route/rest/proxy tests. No Leo rig performance, dynamic collision, mesh self-intersection proof, motion stability or owner approval.'}
(P/'validation.json').write_text(json.dumps(result,indent=2));print('R04_CHECKS',json.dumps(checks),flush=True)
sys.path.insert(0,str(R/'.claude/skills/feltwillow-blender-production/scripts'));import blender_material_audit as material_audit
(P/'r04_linked_shot_material_audit.json').write_text(json.dumps(material_audit.inspect(bpy),indent=2))
