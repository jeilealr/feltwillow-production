"""Small eye-clearance revision; r03 source, palette, surface and rig preserved."""
import bpy,sys,json,hashlib,shutil
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r04';SRC=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r03.blend';OUT=SRC.with_name('leo_canonical_tripo_candidate_r04.blend')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SRC)=='e337d6708236f8b57da8853b59f9dcc6edc9643392ffbe52e5135cffedc21fa2'
bpy.ops.wm.open_mainfile(filepath=str(SRC),use_scripts=False);s=bpy.context.scene;s.frame_set(1);prior.neutral();s.cycles.seed=18102606
surface=bpy.data.objects['Leo_surface'];w=bpy.data.objects['Leo_attached_wool_r02'];me=w.data
verts=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',verts);points=verts.reshape(-1,30,3)
oldidx=np.empty(len(me.polygons),dtype=np.int32);me.polygons.foreach_get('material_index',oldidx);oldmask=oldidx.reshape(-1,27)[:,0]>0
# Actual eye centers from r03's orthographic front image, 768px / 2.2 BU.
# This character's tilted/asymmetric head is not symmetric about X=0.
sm=surface.data;sm.calc_loop_triangles();tree=BVHTree.FromPolygons([v.co for v in sm.vertices],[t.vertices for t in sm.loop_triangles],all_triangles=True)
eyes=[];newmask=oldmask.copy()
for name,px,pz,rx,rz in [('viewer_left',357,297,.050,.057),('viewer_right',448,310,.058,.061)]:
 x=(px-384)*2.2/768;z=.79+(384-pz)*2.2/768
 loc,normal,_,_=tree.ray_cast(Vector((x,-3,z)),Vector((0,1,0)));assert loc is not None
 ellipse=((points[:,:,0]-x)/rx)**2+((points[:,:,2]-z)/rz)**2
 clear=(ellipse<1)&(np.abs(points[:,:,1]-loc.y)<.065)
 mask=clear.any(axis=1);newmask|=mask
 eyes.append({'name':name,'surface_center':list(loc),'xz_radii':[rx,rz],'depth_half_extent':.065,'additional_strands':int((mask&~oldmask).sum())})
# Eye diagnostic camera: front view and tight face crop; no geometry changes.
def close(name):
 c=s.camera;c.location=(0,-5,1.005);target=Vector((.053,-.77,1.005));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.43
 s.render.resolution_x=1000;s.render.resolution_y=800;s.cycles.samples=40;s.render.filepath=str(P/(name+'.png'));bpy.ops.render.render(write_still=True)
close('eyes_before')
me.polygons.foreach_set('material_index',np.repeat(newmask.astype(np.int32),27));me.update()
prior.camera('front_three_quarter');s.frame_set(1);s['approval_status']='r04 final eye tidy; owner happy with r03 appearance, final local correction pending review'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
r={'source_sha256':sha(SRC),'candidate_sha256':sha(OUT),'eyes':eyes,'previous_hidden_strands':int(oldmask.sum()),'additional_hidden_strands':int((newmask&~oldmask).sum()),'visible_strands':int((~newmask).sum()),'surface_geometry_palette_rig_unchanged':True,'external_requests':0,'additional_cost_usd':0}
(P/'operations.json').write_text(json.dumps(r,indent=2));shutil.copy2(P.with_name('leo_tripo_canonical_r03')/'groom_bindings_sample.json',P/'groom_bindings_sample.json')
close('eyes_after');print('R04_EYE_TIDY',json.dumps(r),flush=True)
