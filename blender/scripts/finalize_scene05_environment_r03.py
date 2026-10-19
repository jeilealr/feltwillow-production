"""Correct full-resolution bark regression without rebuilding the library."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];A=R/'blender';P=A/'renders/scene05_environment_r03';E=A/'assets/environments/great_tree/great_tree_environment_r03.blend'
bpy.ops.wm.open_mainfile(filepath=str(E),use_scripts=False)
assert not bpy.context.scene.get('r03_full_resolution_bark_repair',False),'Already applied'
o=bpy.data.objects['OAK_MAIN'];base=bpy.data.objects['ANCHOR_OAK_BASE'].location.copy();inv=o.matrix_world.inverted()
for v in o.data.vertices:
 p=o.matrix_world@v.co
 if 3.1<=p.z<3.8:
  t=(p.z-3.1)/.7;t=t*t*(3-2*t);p.x=base.x+(p.x-base.x)*(1+.4*(1-t));v.co=inv@p
bpy.data.objects['R03_surface_following_bark_folds'].hide_render=True
bpy.data.objects['ROOT_APPROACH_A'].data.splines[0].bezier_points[-1].co=bpy.data.objects['ANCHOR_ROOT_APPROACH_TIP'].location+Vector((0,0,.018))
bpy.data.objects['ROOT_APPROACH_A']['r03_tip']='original safe contact-root endpoint restored; extended tip failed route clearance'
bpy.context.scene['r03_full_resolution_bark_repair']=True
bpy.ops.wm.save_as_mainfile(filepath=str(E),compress=True)
inventory=json.loads((P/'build_inventory.json').read_text());inventory['environment_sha256']=hashlib.sha256(E.read_bytes()).hexdigest();inventory['full_resolution_bark_repair']='Hidden lifted ribbon layer; continuous upper width taper; restored safe approach-root endpoint';(P/'build_inventory.json').write_text(json.dumps(inventory,indent=2))
