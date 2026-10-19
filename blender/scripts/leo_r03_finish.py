"""Bound final fiber reflectance after the second look-development preview."""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r03';OUT=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r03.blend'
bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False)
w=bpy.data.objects['Leo_attached_wool_r02'];m=w.data.materials[0];n=m.node_tree.nodes;l=m.node_tree.links
pigment=next(x for x in n if x.label=='Fiber reflectance: lift baked source shading')
pigment.inputs[2].default_value=(1.45,1.45,1.45,1)
gray=n.new('ShaderNodeRGBToBW');gray.label='Neutral fiber scattering component';source=n.get('Image Texture').outputs['Color'];l.new(source,gray.inputs[0])
blend=n.new('ShaderNodeMixRGB');blend.label='Restrained fiber saturation, 20 percent neutral';blend.inputs[0].default_value=.20;l.new(source,blend.inputs[1]);l.new(gray.outputs[0],blend.inputs[2]);l.new(blend.outputs[0],pigment.inputs[1])
# This corrects only the groom's highlight/reflectance approximation. Original
# body/eye/ear/mane pigment atlas and surface shader colors remain unchanged.
prior.neutral();prior.camera('front_three_quarter');bpy.context.scene.frame_set(1)
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':
   a.spaces.active.shading.type='MATERIAL';a.spaces.active.overlay.show_overlays=False;a.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
p=P/'operations.json';data=json.loads(p.read_text());data.update({'candidate_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'fiber_reflectance_multiplier':1.45,'fiber_neutral_component':.20,'final_adjustment':'Restrain overly orange second-preview fibers without changing original surface atlas'})
for patch in data['uv_repairs']:patch['anchor_image_buffer_rgb']=patch.pop('anchor_linear_rgb')
p.write_text(json.dumps(data,indent=2))
