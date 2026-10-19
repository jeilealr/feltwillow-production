"""Remove residual beige cap stains, confirmed by the exposed final diagnostic."""
import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r03';OUT=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r03.blend'
bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False);bpy.context.scene.frame_set(1)
o=bpy.data.objects['Leo_surface'];me=o.data;uv=me.uv_layers.active.data;im=me.materials[0].node_tree.nodes['Image Texture'].image;pixels=np.array(im.pixels[:]).reshape((im.size[1],im.size[0],4))
def colors(uvs):
 a=np.asarray(uvs);x=np.clip((a[:,0]*im.size[0]).astype(int),0,im.size[0]-1);y=np.clip((a[:,1]*im.size[1]).astype(int),0,im.size[1]-1);return pixels[y,x,:3]
caps=[48508,48510,48511];patches=[]
for idx in caps:
 p=me.polygons[idx];center=p.center.copy();candidates=[]
 for q in me.polygons:
  d=(q.center-center).length
  if q.index in caps or d>.035:continue
  u=np.array([uv[i].uv[:] for i in q.loop_indices]);col=colors(u).mean(axis=0)
  if np.ptp(u,axis=0).max()<.015 and col[0]>.90 and col[1]>.78 and col[2]>.62:candidates.append((d,q.index,u.mean(axis=0),col))
 _,neighbor,anchor,col=min(candidates,key=lambda x:x[0])
 for li in p.loop_indices:
  co=me.vertices[me.loops[li].vertex_index].co-center;uv[li].uv=anchor+np.array([co.x,co.z])*.04
 patches.append({'face':idx,'cream_neighbor_face':neighbor,'new_uv_anchor':anchor.tolist(),'anchor_image_buffer_rgb':col.tolist()})
w=bpy.data.objects['Leo_attached_wool_r02'];wm=w.data;data=np.empty(len(wm.vertices)*3,dtype=np.float32);wm.vertices.foreach_get('co',data);roots=data.reshape(-1,30,3)[:,:3,:].mean(axis=1);centers=np.array([me.polygons[i].center[:] for i in caps]);dist=np.linalg.norm(roots[:,None,:]-centers[None,:,:],axis=2);near=np.where(dist.min(axis=1)<.012)[0]
for k in near:
 anchor=patches[dist[k].argmin()]['new_uv_anchor'];start=int(k)*9*3*4
 for li in range(start,start+9*3*4):wm.uv_layers.active.data[li].uv=anchor
me.update();wm.update();prior.neutral();prior.camera('front_three_quarter');bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
p=P/'operations.json';r=json.loads(p.read_text())
for old,new in zip(r['uv_repairs'],patches):old.update(new)
r['residual_color_repair']='Final exposed diagnostic found beige staining: restrict anchors to nearby bright cream rather than former shaded whisker roots';r['locally_recolored_strands']=len(near);r['candidate_sha256']=hashlib.sha256(OUT.read_bytes()).hexdigest();p.write_text(json.dumps(r,indent=2))
# Expose the repaired skin immediately, before the expensive full review.
for ob in bpy.data.objects:
 if ob.name.startswith('Leo_whisker_') or ob.name=='Leo_attached_wool_r02':ob.hide_render=True
s=bpy.context.scene;c=s.camera;c.location=(1.8,-5,1.16);target=Vector((.13,-.92,.88));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.34;s.render.resolution_x=800;s.render.resolution_y=800;s.cycles.samples=32;s.cycles.seed=18102606;s.render.filepath=str(P/'muzzle_color_verified.png');bpy.ops.render.render(write_still=True)
print('FINAL_COLOR_REPAIR',r['candidate_sha256'],patches,flush=True)
