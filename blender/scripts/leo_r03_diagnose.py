import bpy,sys,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r03'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r02.blend'),use_scripts=False)
prior.neutral();s=bpy.context.scene;s.frame_set(1);o=bpy.data.objects['Leo_surface'];me=o.data
local=[];uv=me.uv_layers.active.data
for p in me.polygons:
 c=p.center
 if .09<c.x<.19 and c.y<-.86 and .79<c.z<.92:
  local.append({'face':p.index,'center':list(c),'vertices':list(p.vertices),'uv':[list(uv[i].uv) for i in p.loop_indices]})
(P/'muzzle_local_faces.json').write_text(json.dumps(local,indent=2))
mat=o.data.materials[0]
(P/'material_nodes.json').write_text(json.dumps([{'name':n.name,'type':n.type,'label':n.label,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None} for n in mat.node_tree.nodes],indent=2))
for ob in bpy.data.objects:
 if ob.name.startswith('Leo_whisker_') or ob.name=='Leo_attached_wool_r02':ob.hide_render=True
c=s.camera;c.location=(1.8,-5,1.16);target=Vector((.13,-.92,.88));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.34
s.render.resolution_x=800;s.render.resolution_y=800;s.cycles.samples=32
s.render.filepath=str(P/'muzzle_before_color.png');bpy.ops.render.render(write_still=True)
clay=bpy.data.materials.new('diagnostic_clay');clay.use_nodes=True;clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5,.5,.5,1);clay.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.9
o.data.materials[0]=clay;s.render.filepath=str(P/'muzzle_before_clay.png');bpy.ops.render.render(write_still=True)
