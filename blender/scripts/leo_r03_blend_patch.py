"""Feather local muzzle pigment and suppress baked root normals, no atlas edits."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r03';OUT=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r03.blend'
bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False);s=bpy.context.scene;s.frame_set(1)
o=bpy.data.objects['Leo_surface'];m=o.data.materials[0];n=m.node_tree.nodes;l=m.node_tree.links
assert not any(x.label=='Feathered old whisker-root healing' for x in n)
coord=n.new('ShaderNodeAttribute');coord.attribute_name='felt_rest';coord.label='Local muzzle healing / stable rest space'
dists=[]
for idx in [48508,48510,48511]:
 d=n.new('ShaderNodeVectorMath');d.operation='DISTANCE';d.inputs[1].default_value=o.data.polygons[idx].center;l.new(coord.outputs['Vector'],d.inputs[0]);dists.append(d.outputs['Value'])
small=dists[0]
for socket in dists[1:]:
 d=n.new('ShaderNodeMath');d.operation='MINIMUM';l.new(small,d.inputs[0]);l.new(socket,d.inputs[1]);small=d.outputs[0]
mask=n.new('ShaderNodeMapRange');mask.interpolation_type='SMOOTHERSTEP';mask.label='Feather old-root patch over 0.010–0.032 BU';mask.inputs['From Min'].default_value=.010;mask.inputs['From Max'].default_value=.032;mask.inputs['To Min'].default_value=1;mask.inputs['To Max'].default_value=0;l.new(small,mask.inputs['Value'])
heal=n.new('ShaderNodeMixRGB');heal.label='Feathered old whisker-root healing';l.new(mask.outputs['Result'],heal.inputs[0]);l.new(n.get('Image Texture').outputs['Color'],heal.inputs[1])
def lin(v):return v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4
heal.inputs[2].default_value=tuple(lin(v) for v in (.93,.84,.71))+(1,)
base=n.get('Principled BSDF');mul=base.inputs['Base Color'].links[0].from_node;l.new(heal.outputs[0],mul.inputs[1])
# The imported normal atlas still encodes the old root scar: fade it locally,
# retaining PATINA's continuous rest-space wool relief on top.
inverse=n.new('ShaderNodeMath');inverse.operation='SUBTRACT';inverse.inputs[0].default_value=1;l.new(mask.outputs['Result'],inverse.inputs[1]);strength=n.new('ShaderNodeMath');strength.operation='MULTIPLY';strength.inputs[1].default_value=.25;l.new(inverse.outputs[0],strength.inputs[0]);l.new(strength.outputs[0],n.get('Normal Map').inputs['Strength'])
prior.neutral();prior.camera('front_three_quarter');bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
p=P/'operations.json';r=json.loads(p.read_text());r['candidate_sha256']=hashlib.sha256(OUT.read_bytes()).hexdigest();r['feathered_healing']={'centers_faces':[48508,48510,48511],'full_radius_bu':.010,'fade_radius_bu':.032,'cream_sample_srgb':[.93,.84,.71],'source_normal_strength_at_center':0,'original_image_unchanged':True};p.write_text(json.dumps(r,indent=2))
for ob in bpy.data.objects:
 if ob.name.startswith('Leo_whisker_') or ob.name=='Leo_attached_wool_r02':ob.hide_render=True
c=s.camera;c.location=(1.8,-5,1.16);target=Vector((.13,-.92,.88));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.34;s.render.resolution_x=800;s.render.resolution_y=800;s.cycles.samples=32;s.cycles.seed=18102606;s.render.filepath=str(P/'muzzle_color_verified.png');bpy.ops.render.render(write_still=True)
print('FEATHERED_HEALING',r['candidate_sha256'],flush=True)
