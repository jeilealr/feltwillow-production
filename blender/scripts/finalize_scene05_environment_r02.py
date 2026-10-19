"""Make the linked shot open cleanly; viewport-only change, no scene geometry edits."""
import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'blender/renders/scene05_environment_r02';SHOT=ROOT/'blender/scenes/lion_and_mouse_v6/s05_environment_r02.blend'
bpy.ops.wm.open_mainfile(filepath=str(SHOT),use_scripts=False)
bpy.data.collections['S05_PROXIES_DIAGNOSTIC_ONLY'].hide_viewport=True
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.shading.type='MATERIAL';a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=str(SHOT),compress=True)
p=P/'scene_build.json';r=json.loads(p.read_text());r['sha256']=hashlib.sha256(SHOT.read_bytes()).hexdigest();r['proxies_hidden_in_default_viewport']=True;p.write_text(json.dumps(r,indent=2))
print('IMAGE_PORTABILITY',json.dumps([{'name':im.name,'source':im.source,'filepath':im.filepath,'packed':bool(im.packed_file),'packed_files':len(im.packed_files),'has_data':im.has_data,'library':im.library.filepath if im.library else None} for im in bpy.data.images]),flush=True)
