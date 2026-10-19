"""Render isolated r03 comparisons and reuse the established bounded rig audit."""
import bpy,sys,json,hashlib,time
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_r02_review as review
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r03';OUT=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r03.blend'
review.P=P;review.OUT=OUT
if '--audit' in sys.argv:review.audit();sys.exit()
bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False);prior.neutral();s=bpy.context.scene;s.frame_set(1);s.cycles.seed=18102606
manifest=P/('preview_render_manifest.json' if '--preview' in sys.argv else 'render_manifest.json');records=json.loads(manifest.read_text()) if manifest.exists() else []
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def render(name,size=896,samples=40):
 dest=P/(name+'.png');dest.parent.mkdir(exist_ok=True,parents=True)
 if '--resume' in sys.argv and any(r['path']==name+'.png' and r['candidate_sha256']==sha(OUT) and dest.exists() and r['sha256']==sha(dest) for r in records):return
 s.render.filepath=str(dest);s.render.resolution_x=size;s.render.resolution_y=size;s.cycles.samples=samples
 start=time.perf_counter();bpy.ops.render.render(write_still=True)
 records[:]=[r for r in records if r['path']!=name+'.png']
 records.append({'path':name+'.png','sha256':sha(dest),'candidate_sha256':sha(OUT),'frame':s.frame_current,'samples':samples,'size':[size,size],'engine':'Cycles CPU','color':'Standard / None / exposure 0 / gamma 1','camera':[list(row) for row in s.camera.matrix_world],'ortho_scale':s.camera.data.ortho_scale,'seconds':round(time.perf_counter()-start,2)})
 manifest.write_text(json.dumps(records,indent=2))
def close():
 c=s.camera;c.location=(1.8,-5,1.16);target=Vector((.13,-.92,.88));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.34
if '--preview' in sys.argv:
 prior.camera('portrait');render('preview_portrait',768,32)
 c=s.camera;c.location=(-3,-1.9,1.2);target=Vector((-.15,.05,.54));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.75;render('preview_body',896,40)
 close();render('preview_muzzle',800,40)
else:
 for v in ['front_three_quarter','front','right','rear','portrait']:
  prior.camera(v);render(v,768,40 if v=='portrait' else 32)
 c=s.camera;c.location=(-3,-1.9,1.2);target=Vector((-.15,.05,.54));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.75;render('body_detail',896,48)
 close();render('muzzle_final',800,40)
 for ob in bpy.data.objects:
  if ob.name.startswith('Leo_whisker_') or ob.name=='Leo_attached_wool_r02':ob.hide_render=True
 render('muzzle_after_color',800,32)
 o=bpy.data.objects['Leo_surface'];original=o.data.materials[0];clay=bpy.data.materials.new('r03_diagnostic_clay');clay.use_nodes=True;clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5,.5,.5,1);clay.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9;o.data.materials[0]=clay
 render('muzzle_after_clay',800,32);o.data.materials[0]=original
 for ob in bpy.data.objects:
  if ob.name.startswith('Leo_whisker_') or ob.name=='Leo_attached_wool_r02':ob.hide_render=False
 prior.camera('front_three_quarter');bpy.data.objects['Neutral_key'].data.color=(1,.79,.57);bpy.data.objects['Neutral_rim'].data.color=(.62,.74,1);render('story_light',768,32)
 prior.neutral();prior.camera('front_three_quarter')
 for frame in range(1,50,4):s.frame_set(frame);render('motion/frame_%03d'%frame,512,24)
 s.frame_set(1)
print('R03_RENDER_COMPLETE',len(records),flush=True)
