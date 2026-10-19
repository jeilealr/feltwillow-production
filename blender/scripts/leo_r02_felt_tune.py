"""One visually motivated wool refinement, preview first; no provider calls."""
import bpy,sys,json,time,hashlib,shutil
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_tripo_refine_r02 as r
import leo_tripo_canonical_pass as prior
P=r.P;OUT=r.OUT
bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False);prior.neutral();bpy.context.scene.frame_set(1)
if bpy.context.scene.get('felt_refinement_applied'):raise RuntimeError('Felt refinement already applied; rebuild rig/felt baseline before replaying this step')
import numpy as np
wool=bpy.data.objects['Leo_attached_wool_r02'];me=wool.data
coords=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',coords);a=coords.reshape((-1,21,3));roots=a[:,:3,:].mean(axis=1,keepdims=True);a[:]=roots+(a-roots)*.70;me.vertices.foreach_set('co',coords);me.update()
m=wool.data.materials[0];n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');out=n.get('Material Output')
trans=n.new('ShaderNodeBsdfTranslucent');trans.label='Restrained thin wool light transmission'
if p.inputs['Base Color'].is_linked:l.new(p.inputs['Base Color'].links[0].from_socket,trans.inputs['Color'])
mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.40;l.new(p.outputs['BSDF'],mix.inputs[1]);l.new(trans.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface'])
surface=bpy.data.objects['Leo_surface'];patina=surface.data.materials[0];n=patina.node_tree.nodes;l=patina.node_tree.links
bump=next(node for node in n if node.type=='BUMP' and node.label=='PATINA compressed felt height')
bump.inputs['Strength'].default_value=.50;bump.inputs['Distance'].default_value=.004
height_socket=bump.inputs['Height'].links[0].from_socket
levels=n.new('ShaderNodeMapRange');levels.label='Felt height contrast';levels.inputs['From Min'].default_value=.25;levels.inputs['From Max'].default_value=.75;levels.inputs['To Min'].default_value=0;levels.inputs['To Max'].default_value=1;l.new(height_socket,levels.inputs['Value']);l.new(levels.outputs['Result'],bump.inputs['Height'])
# Bound fine fiber luminance around one; the character's original color atlas
# remains the pigment source. This supplies the densely interlaced meso detail
# which isolated geometric flyaways cannot provide.
tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(r.AREA/'assets/materials/leo_felt_patina_trial/extracted_texture.png'),check_existing=True);tex.image.colorspace_settings.name='sRGB';tex.image.pack();tex.projection='BOX';tex.projection_blend=.25;tex.extension='REPEAT';tex.label='PATINA fine wool structure / color-neutral modulation'
mapping=next(node for node in n if node.type=='VECT_MATH' and node.operation=='SCALE');l.new(mapping.outputs[0],tex.inputs['Vector'])
gray=n.new('ShaderNodeRGBToBW');l.new(tex.outputs['Color'],gray.inputs[0])
level=n.new('ShaderNodeMapRange');level.label='Mean-neutral wool variation, bounded +/-12 percent';level.inputs['From Min'].default_value=.3543341-.12/.65;level.inputs['From Max'].default_value=.3543341+.12/.65;level.inputs['To Min'].default_value=.88;level.inputs['To Max'].default_value=1.12;l.new(gray.outputs[0],level.inputs['Value'])
bsdf=n.get('Principled BSDF');original_color=bsdf.inputs['Base Color'].links[0].from_socket
mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;l.new(original_color,mul.inputs[1]);l.new(level.outputs['Result'],mul.inputs[2]);l.new(mul.outputs[0],bsdf.inputs['Base Color'])
if '--apply' in sys.argv:
    checkpoint=OUT.with_name('leo_tripo_r02_material_trial_01.blend')
    if not checkpoint.exists():shutil.copy2(OUT,checkpoint)
    bpy.context.scene['felt_refinement_applied']=True
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT),compress=True)
    (P/'felt_refinement.json').write_text(json.dumps({'operation':'finer shorter wool; 40% thin-fiber translucency; PATINA height relief and bounded mean-neutral fine-fiber luminance','fiber_length_and_radius_scale':.70,'groom_translucent_mix':.40,'patina_bump_strength':.50,'patina_height_distance_bu':.004,'height_levels':[.25,.75],'wool_luminance_multiplier_bounds':[.88,1.12],'source_texture_linear_luminance_mean':.3543341,'original_color_atlas_retained':True,'external_requests':0,'candidate_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2)+'\n')
    print('FELT_TUNE_APPLIED',flush=True)
else:
    s=bpy.context.scene;c=s.camera;c.location=(-3,-1.9,1.2);target=Vector((-.15,.05,.54));c.rotation_euler=(target-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.75
    s.render.resolution_x=896;s.render.resolution_y=896;s.cycles.samples=48;s.render.filepath=str(P/'felt_tune_body_preview.png');bpy.ops.render.render(write_still=True)
    if '--body-only' not in sys.argv:
        prior.camera('portrait');s.render.resolution_x=768;s.render.resolution_y=768;s.cycles.samples=40;s.render.filepath=str(P/'felt_tune_face_preview.png');bpy.ops.render.render(write_still=True)
