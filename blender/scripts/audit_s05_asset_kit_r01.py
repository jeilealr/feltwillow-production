"""Read actual latest candidate/links/materials and sun visibility. No saves/renders."""
import bpy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=R/'blender/renders/s05_asset_kit_r01';sys.path.insert(0,str(R/'.agents/skills/feltwillow-blender-production/scripts'));import blender_material_audit as audit
E=R/'blender/assets/environments/great_tree/great_tree_environment_r04.blend';S=R/'blender/scenes/lion_and_mouse_v6/s05_environment_r04.blend'
bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);s=bpy.context.scene
def visible(col):
 result=set()
 if col.hide_render:return result
 result.update(o.name for o in col.objects if not o.hide_render)
 for child in col.children:result.update(visible(child))
 return result
active=visible(s.collection);sun=[]
for o in bpy.data.objects:
 if any(x in o.name.lower() for x in ['sunset','fixed_sun','sun_']):sun.append({'name':o.name,'type':o.type,'hide_render':o.hide_render,'render_collection_eligible':o.name in active,'viewport_visible_get':o.visible_get(),'collections':[{'name':x.name,'hide_render':x.hide_render,'hide_viewport':x.hide_viewport} for x in o.users_collection],'materials':[x.name for x in o.data.materials] if o.type in ['MESH','CURVE'] else [],'location':list(o.location)})
report=audit.inspect(bpy);report['actual_scene_libraries']=[{'path':x.filepath,'resolved':bpy.path.abspath(x.filepath),'exists':Path(bpy.path.abspath(x.filepath)).is_file()} for x in bpy.data.libraries];report['sun_inventory']=sun;report['camera']={'name':s.camera.name,'matrix':[list(x) for x in s.camera.matrix_world],'lens':s.camera.data.lens};report['current_main_materials']={name:[slot.material.name if slot.material else None for slot in s.objects[name].material_slots] for name in ['OAK_MAIN','ROOT_APPROACH_A','SURF_CLEARING','ROCK_RIGHT']};report['visible_r04_material_users']={m.name:[o.name for o in s.objects if o.name in active and any(slot.material==m for slot in o.material_slots)] for m in bpy.data.materials if m.name.startswith('R04_')}
(P/'current_material_sun_audit.json').write_text(json.dumps(report,indent=2));print('SUN_INVENTORY',json.dumps(sun),flush=True)
