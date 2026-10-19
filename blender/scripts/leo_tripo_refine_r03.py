"""Local r03 repair and dense, fixed-seed attached felt; no external calls."""
import bpy,sys,json,hashlib,math,time
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
import leo_tripo_refine_r02 as refine
P=ROOT/'blender/renders/leo_tripo_canonical_r03';P.mkdir(exist_ok=True,parents=True)
SOURCE=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r02.blend'
OUT=SOURCE.with_name('leo_canonical_tripo_candidate_r03.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE)=='7d60fb0c9aa96c89458152d09e5e6c88e7566507d58ff9e2a8daef0042a5768a'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);s=bpy.context.scene;s.frame_set(1)
o=bpy.data.objects['Leo_surface'];me=o.data;uv=me.uv_layers.active.data
mat=me.materials[0].copy();mat.name='Leo_Felt_r03_PATINA';me.materials[0]=mat
im=mat.node_tree.nodes['Image Texture'].image
pixels=np.array(im.pixels[:],dtype=np.float32).reshape((im.size[1],im.size[0],4))
def colors(uvs):
 a=np.asarray(uvs);x=np.clip((a[:,0]*im.size[0]).astype(int),0,im.size[0]-1);y=np.clip((a[:,1]*im.size[1]).astype(int),0,im.size[1]-1);return pixels[y,x,:3]
# Correct only the three caps whose corners crossed unrelated UV islands.
caps=[48508,48510,48511];patches=[];capverts=set()
for idx in caps:
 p=me.polygons[idx];center=p.center.copy();candidates=[]
 for q in me.polygons:
  if q.index in caps or (q.center-center).length>.035:continue
  u=np.array([uv[i].uv[:] for i in q.loop_indices]);col=colors(u).mean(axis=0)
  if np.ptp(u,axis=0).max()<.015 and col[0]>.90 and col[1]>.78 and col[2]>.62:
   candidates.append(((q.center-center).length,q.index,u.mean(axis=0),col))
 assert candidates,'No local cream UV anchor'
 _,neighbor,anchor,col=min(candidates,key=lambda x:x[0])
 old=[list(uv[i].uv) for i in p.loop_indices]
 for li in p.loop_indices:
  co=me.vertices[me.loops[li].vertex_index].co-center
  uv[li].uv=anchor+np.array([co.x,co.z])*.04
 patches.append({'face':idx,'old_uv':old,'cream_neighbor_face':neighbor,'new_uv_anchor':anchor.tolist(),'anchor_linear_rgb':col.tolist()});capverts.update(p.vertices)
# Constrained local fairing, no connectivity/vertex index changes.
adj=[set() for _ in me.vertices]
for e in me.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
centers=[me.polygons[i].center.copy() for i in caps];orig=[v.co.copy() for v in me.vertices]
ids=set(capverts)
for i in list(capverts):ids.update(adj[i])
for iteration in range(10):
 targets={}
 for i in ids:
  d=min((orig[i]-c).length for c in centers);f=max(0,1-d/.021)*.38
  if adj[i]:targets[i]=me.vertices[i].co.lerp(sum((me.vertices[j].co for j in adj[i]),Vector())/len(adj[i]),f)
 for i,p in targets.items():me.vertices[i].co=p
fairing_count=len(ids)
me.update();max_change=max((v.co-orig[v.index]).length for v in me.vertices)
# Stable coordinates track the locally corrected rest surface.
rest=me.attributes.get('felt_rest')
if rest:
 rest.data.foreach_set('vector',np.array([v.co[:] for v in me.vertices],dtype=np.float32).ravel())
# Less engraved relief; geometric loops now carry the visible surface texture.
n=mat.node_tree.nodes
bump=next(x for x in n if x.type=='BUMP' and x.label=='PATINA compressed felt height');bump.inputs['Strength'].default_value=.32;bump.inputs['Distance'].default_value=.0022
n.get('Normal Map').inputs['Strength'].default_value=.25
n.get('Principled BSDF').inputs['Sheen Weight'].default_value=.35
# Fixed seed area-uniform root sampling.
rng=np.random.default_rng(18102618);me.calc_loop_triangles();ts=list(me.loop_triangles)
tri=np.array([t.vertices[:] for t in ts]);tloops=np.array([t.loops[:] for t in ts]);area=np.array([t.area for t in ts]);acc=np.cumsum(area)
NTRY=150000;ix=np.searchsorted(acc,rng.random(NTRY)*acc[-1]);b=rng.random((NTRY,2));b[b.sum(axis=1)>1]=1-b[b.sum(axis=1)>1];bary=np.column_stack((1-b.sum(axis=1),b))
coords=np.array([v.co[:] for v in me.vertices]);norms=np.array([v.normal[:] for v in me.vertices]);triids=tri[ix];roots=(coords[triids]*bary[:,:,None]).sum(axis=1);norm=(norms[triids]*bary[:,:,None]).sum(axis=1);norm/=np.linalg.norm(norm,axis=1)[:,None]
uva=np.array([d.uv[:] for d in uv]);rootuv=(uva[tloops[ix]]*bary[:,:,None]).sum(axis=1)
col=colors(rootuv)
# Exclude eyes/nose/lip pigment on face; admit short wool on cream/gold skin.
face=(roots[:,1]<-.70)&(np.abs(roots[:,0])<.34)&(roots[:,2]>.79)&(roots[:,2]<1.28)
eye=(roots[:,1]<-.77)&(np.abs(roots[:,0])>.075)&(np.abs(roots[:,0])<.29)&(roots[:,2]>1.045)&(roots[:,2]<1.23)
nose=(roots[:,1]<-.90)&(np.abs(roots[:,0])<.105)&(roots[:,2]>.905)&(roots[:,2]<1.025)
lip=(roots[:,1]<-.90)&(np.abs(roots[:,0])<.07)&(roots[:,2]>.80)&(roots[:,2]<.85)
keep=~((face & ((col.max(axis=1)<.48)|(col[:,1]<.32)))|eye|nose|lip)
roots,norm,triids,bary,rootuv,face=[a[keep] for a in [roots,norm,triids,bary,rootuv,face]]
K=len(roots);N=10;S=3
randomdir=rng.normal(size=(K,3));tangent=np.cross(norm,randomdir);tangent/=np.linalg.norm(tangent,axis=1)[:,None];side=np.cross(norm,tangent)
length=rng.uniform(.014,.030,K);height=rng.uniform(.0010,.0038,K);radius=rng.uniform(.00016,.00025,K)
fly=rng.random(K)<.06;height[fly]*=1.8;length[fly]*=1.25
length[face]*=.55;height[face]*=.60;radius[face]*=.85
# Project each end onto the unchanged source topology, avoiding floating ends.
bvh=BVHTree.FromPolygons([Vector(p) for p in coords],tri.tolist(),all_triangles=True)
end=roots+tangent*length[:,None];endnormal=np.empty_like(norm)
for i,p in enumerate(end):
 loc,no,_,_=bvh.find_nearest(Vector(p));end[i]=loc;endnormal[i]=no
points=np.empty((K,N,3));phase=rng.uniform(0,math.tau,K);freq=rng.uniform(.65,1.05,K)
for j,t in enumerate(np.linspace(0,1,N)):
 center=roots*(1-t)+end*t
 nn=norm*(1-t)+endnormal*t;nn/=np.linalg.norm(nn,axis=1)[:,None]
 wiggle=np.sin(t*math.pi)*np.sin(phase+t*freq*math.tau)*length*.18
 points[:,j]=center+nn*(.00020+np.sin(t*math.pi)*height)[:,None]+side*wiggle[:,None]
# Thin triangular tubes; fixed dimensions and topology through animation.
dir=np.empty_like(points);dir[:,1:-1]=points[:,2:]-points[:,:-2];dir[:,0]=points[:,1]-points[:,0];dir[:,-1]=points[:,-1]-points[:,-2];dir/=np.linalg.norm(dir,axis=2)[:,:,None]
ex=np.cross(dir,norm[:,None,:]);ex/=np.linalg.norm(ex,axis=2)[:,:,None];ey=np.cross(dir,ex)
verts=np.empty((K,N,S,3),dtype=np.float32)
for k in range(S):
 angle=math.tau*k/S;verts[:,:,k]=points+(ex*math.cos(angle)+ey*math.sin(angle))*radius[:,None,None]
start=(np.arange(K,dtype=np.int32)*N*S)[:,None,None];j=(np.arange(N-1,dtype=np.int32)*S)[None,:,None];k=np.arange(S,dtype=np.int32)[None,None,:]
a=start+j+k;bb=start+j+(k+1)%S
faces=np.stack((np.broadcast_to(a,(K,N-1,S)),np.broadcast_to(bb,(K,N-1,S)),np.broadcast_to(bb+S,(K,N-1,S)),np.broadcast_to(a+S,(K,N-1,S))),axis=-1).reshape(-1,4)
old=bpy.data.objects['Leo_attached_wool_r02'];wmat=old.data.materials[0].copy();wmat.name='Leo_Wool_r03_Palette';collection=old.users_collection[0];parent=old.parent;rig=bpy.data.objects['Leo_RIG_R02'];bpy.data.objects.remove(old,do_unlink=True)
mesh=bpy.data.meshes.new('Leo_r03_dense_short_wool');mesh.vertices.add(K*N*S);mesh.vertices.foreach_set('co',verts.ravel());mesh.loops.add(len(faces)*4);mesh.loops.foreach_set('vertex_index',faces.ravel());mesh.polygons.add(len(faces));mesh.polygons.foreach_set('loop_start',np.arange(len(faces),dtype=np.int32)*4);mesh.polygons.foreach_set('loop_total',np.full(len(faces),4,dtype=np.int32));mesh.polygons.foreach_set('use_smooth',np.ones(len(faces),dtype=bool));mesh.update(calc_edges=True)
wool=bpy.data.objects.new('Leo_attached_wool_r02',mesh);collection.objects.link(wool);wool.parent=parent
layer=mesh.uv_layers.new(name='Source_palette_UV');loopstrand=faces.ravel()//(N*S);layer.data.foreach_set('uv',rootuv[loopstrand].astype(np.float32).ravel())
# Reuse source skin weights; roots retain their source triangle and barycentrics.
gnames={g.index:g.name for g in o.vertex_groups};weights=[{gnames[g.group]:g.weight for g in v.groups} for v in me.vertices]
groups={name:wool.vertex_groups.new(name=name) for name in gnames.values()}
bindings=[]
for k,(ids,bs) in enumerate(zip(triids,bary)):
 w={}
 for idx,factor in zip(ids,bs):
  for name,value in weights[idx].items():w[name]=w.get(name,0)+value*factor
 total=sum(w.values());vids=list(range(k*N*S,(k+1)*N*S))
 for name,value in w.items():
  if value/total>1e-6:groups[name].add(vids,float(value/total),'REPLACE')
 if k%max(1,K//80)==0:bindings.append({'start':k*N*S,'triangle':ids.tolist(),'bary':bs.tolist(),'rest_root':roots[k].tolist()})
mod=wool.modifiers.new('Attached source triangle skin weights','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
wn=wmat.node_tree.nodes;wl=wmat.node_tree.links;pp=wn.get('Principled BSDF');pp.inputs['Roughness'].default_value=.68;pp.inputs['Sheen Weight'].default_value=.50;pp.inputs['Specular IOR Level'].default_value=.35
# Fibers use unmodified source atlas pigment. Surface relief belongs on the felt base.
source_tex=wn.get('Image Texture');pigment=wn.new('ShaderNodeMixRGB');pigment.blend_type='MULTIPLY';pigment.label='Fiber reflectance: lift baked source shading';pigment.inputs[0].default_value=1;pigment.inputs[2].default_value=(1.8,1.8,1.8,1);wl.new(source_tex.outputs['Color'],pigment.inputs[1]);wl.new(pigment.outputs[0],pp.inputs['Base Color'])
trans=next(x for x in wn if x.type=='BSDF_TRANSLUCENT');wl.new(pigment.outputs[0],trans.inputs['Color']);mix=next(x for x in wn if x.type=='MIX_SHADER');mix.inputs[0].default_value=.25
mesh.materials.append(wmat)
(P/'groom_bindings_sample.json').write_text(json.dumps(bindings,indent=2))
prior.neutral();prior.camera('front_three_quarter');s.frame_set(1);s.cycles.seed=18102606
s['approval_status']='r03 muzzle repair / dense wool candidate; owner visual review pending';s['groom_strands']=K
for im in bpy.data.images:
 if im.has_data and not im.packed_file:im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
(P/'operations.json').write_text(json.dumps({'source_sha256':sha(SOURCE),'candidate_sha256':sha(OUT),'uv_repairs':patches,'local_smoothed_vertices':fairing_count,'local_fairing_max_change_bu':max_change,'topology':refine.stats(me),'groom_strands':K,'groom_vertices':len(mesh.vertices),'face_strands':int(face.sum()),'strand_length_bu':[.014,.030],'strand_radius_bu':[.00016,.00025],'face_length_multiplier':.55,'groom_translucency':.25,'fiber_reflectance_multiplier':1.8,'trial':2,'curve_points':10,'patina_bump_strength':.32,'patina_bump_distance_bu':.0022,'external_requests':0},indent=2))
print('R03_BUILD_COMPLETE',K,sha(OUT),flush=True)
