"""Force lazy file images to pack, close approach-root tips, keep linked scene portable."""
import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'blender/renders/scene05_environment_r02';ENV=ROOT/'blender/assets/environments/great_tree/great_tree_environment_r02.blend';SHOT=ROOT/'blender/scenes/lion_and_mouse_v6/s05_environment_r02.blend'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(ENV),use_scripts=False)
for im in bpy.data.images:
 if im.source=='FILE':im.pack()
bpy.data.objects['ROOT_APPROACH_A'].data.use_fill_caps=True
bpy.ops.wm.save_as_mainfile(filepath=str(ENV),compress=True)
r=json.loads((P/'build_inventory.json').read_text());r['sha256']=sha(ENV);r['packed_images']=[im.name for im in bpy.data.images if im.packed_file];r['approach_root_caps_closed']=True;(P/'build_inventory.json').write_text(json.dumps(r,indent=2))
bpy.ops.wm.open_mainfile(filepath=str(SHOT),use_scripts=False);bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'].hide_viewport=True
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=str(SHOT),compress=True)
r=json.loads((P/'scene_build.json').read_text());r['sha256']=sha(SHOT);r['library_sha256']=sha(ENV);r['proxies_hidden_in_default_viewport']=True;(P/'scene_build.json').write_text(json.dumps(r,indent=2))
print('PACKED_LINKED_IMAGES',json.dumps([{'name':im.name,'packed':bool(im.packed_file),'packed_files':len(im.packed_files)} for im in bpy.data.images if im.source=='FILE']),flush=True)
