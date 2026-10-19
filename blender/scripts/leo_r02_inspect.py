"""Inspect source whisker artifact and local topology; no source writes."""
import bpy,bmesh,json,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r02';P.mkdir(parents=True,exist_ok=True)
after='--r02' in sys.argv
source=prior.OUT.with_name('leo_canonical_tripo_candidate_r02.blend') if after else prior.OUT
bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False);prior.neutral()
o=bpy.data.objects['Leo_surface'];m=o.data;bm=bmesh.new();bm.from_mesh(m)
issues=[{'a':list(e.verts[0].co),'b':list(e.verts[1].co),'faces':len(e.link_faces)} for e in bm.edges if not e.is_manifold]
faceverts=[{'id':v.index,'co':list(v.co),'normal':list(v.normal),'edges':len(v.link_edges)} for v in bm.verts if abs(v.co.x)<.4 and v.co.y<-.65 and .80<v.co.z<1.05]
bm.free();(P/('refined_local_geometry.json' if after else 'source_local_geometry.json')).write_text(json.dumps({'problem_edges':issues,'face_vertices':faceverts},indent=2)+'\n')
for ob in bpy.data.objects:
 if ob.name=='Leo_attached_short_wool' or ob.name.startswith('Leo_whisker_'):ob.hide_render=True
c=bpy.context.scene.camera;c.location=(-1.8,-5,1.13);target=Vector((0,-.78,.97));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.72
s=bpy.context.scene;s.render.resolution_x=1000;s.render.resolution_y=800;s.cycles.samples=32;s.render.filepath=str(P/('imported_whiskers_after.png' if after else 'imported_whiskers_before.png'));bpy.ops.render.render(write_still=True)
mat=o.data.materials[0];clay=bpy.data.materials.new('Whisker_geometry_clay');clay.use_nodes=True
clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5,.5,.5,1);clay.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9
o.data.materials[0]=clay;s.render.filepath=str(P/('imported_whiskers_after_clay.png' if after else 'imported_whiskers_clay.png'));bpy.ops.render.render(write_still=True)
if after:
 o.data.materials[0]=mat;prior.camera('rear');s.render.resolution_x=768;s.render.resolution_y=768;s.render.filepath=str(P/'rear_refinement_preview.png');bpy.ops.render.render(write_still=True)
print('WHISKER_INSPECTION',len(faceverts),'face vertices',len(issues),'problem edges',flush=True)
