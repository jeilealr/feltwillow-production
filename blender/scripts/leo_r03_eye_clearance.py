"""Clear complete wool strands crossing eyes; preserve skin/binding indices."""
import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r03';OUT=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r03.blend'
bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False);s=bpy.context.scene;s.frame_set(1);w=bpy.data.objects['Leo_attached_wool_r02'];me=w.data
coords=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',coords);p=coords.reshape(-1,30,3)
# Test every strand vertex, not only its root: longer wool can cross a clear eye.
eye=(p[:,:,1]<-.77)&(np.abs(p[:,:,0])>.065)&(np.abs(p[:,:,0])<.34)&(p[:,:,2]>.955)&(p[:,:,2]<1.125)
remove=eye.any(axis=1)
clear=bpy.data.materials.new('Leo_r03_masked_feature_fibers');clear.use_nodes=True;n=clear.node_tree.nodes;l=clear.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');t=n.new('ShaderNodeBsdfTransparent');l.new(t.outputs[0],out.inputs['Surface']);me.materials.append(clear)
me.polygons.foreach_set('material_index',np.repeat(remove.astype(np.int32),27));me.update()
prior.neutral();prior.camera('front_three_quarter');bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
r=json.loads((P/'operations.json').read_text());r['eye_clearance']={'method':'whole-strand transparent material for any vertex crossing protected eye envelope; indices/bindings preserved','masked_strands':int(remove.sum()),'visible_strands':int((~remove).sum()),'y_max':-.77,'absolute_x':[.065,.34],'z':[.955,1.125]};r['candidate_sha256']=hashlib.sha256(OUT.read_bytes()).hexdigest();(P/'operations.json').write_text(json.dumps(r,indent=2))
c=s.camera;c.location=(1.8,-5,1.16);target=Vector((.13,-.92,.88));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.34;s.render.resolution_x=800;s.render.resolution_y=800;s.cycles.samples=32;s.cycles.seed=18102606;s.render.filepath=str(P/'eye_clearance_verified.png');bpy.ops.render.render(write_still=True)
print('EYE_CLEARANCE',r['eye_clearance'],r['candidate_sha256'],flush=True)
