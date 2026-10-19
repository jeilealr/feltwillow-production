"""Safe-copy material audit and original linked-shot baseline; no scene saves."""
import bpy,sys,json,time,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];P=R/'blender/renders/scene05_environment_r04';sys.path.insert(0,str(R/'.claude/skills/feltwillow-blender-production/scripts'))
import blender_material_audit as audit
bpy.ops.wm.open_mainfile(filepath=str(P/'intake_source_r03.blend'),use_scripts=False)
report=audit.inspect(bpy);(P/'r03_material_audit.json').write_text(json.dumps(report,indent=2))
inventory={'collections':[c.name for c in bpy.data.collections],'hero':{},'materials':{}}
for name in ['OAK_MAIN','ROOT_APPROACH_A','SURF_CLEARING','SURF_PATH','ROCK_RIGHT','STONE_CENTER_LEFT','ANCHOR_OAK_BASE','ANCHOR_LEO_REST_CENTER','ANCHOR_LEO_PAW_CONTACT','ANCHOR_LEO_NOSE_CONTACT']:
 o=bpy.data.objects[name];inventory['hero'][name]={'location':list(o.location),'dimensions':list(o.dimensions),'materials':[x.name for x in o.data.materials] if o.type in ['MESH','CURVE'] else []}
for m in bpy.data.materials:
 images=[{'name':n.image.name,'node':n.name} for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image] if m.node_tree else []
 if images:inventory['materials'][m.name]=images
bpy.ops.wm.open_mainfile(filepath=str(R/'blender/scenes/lion_and_mouse_v6/s05_environment_r03.blend'),use_scripts=False);s=bpy.context.scene
inventory['shot']={'camera':s.camera.name,'matrix':[list(x) for x in s.camera.matrix_world],'lens':s.camera.data.lens,'resolution':[s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage],'samples':s.cycles.samples,'color':[s.view_settings.view_transform,s.view_settings.look,s.view_settings.exposure,s.view_settings.gamma],'libraries':[x.filepath for x in bpy.data.libraries],'world':s.world.name}
inventory['route']={o.name:list(o.location) for o in bpy.data.objects if o.name.startswith('ROUTE_MILO_')}
(P/'intake_inventory.json').write_text(json.dumps(inventory,indent=2));print(json.dumps(inventory['hero']),flush=True)
s.render.filepath=str(P/'baseline_saved_settings.png');s.render.image_settings.file_format='PNG';start=time.perf_counter();bpy.ops.render.render(write_still=True);inventory['baseline_seconds']=time.perf_counter()-start;inventory['baseline_sha256']=hashlib.sha256((P/'baseline_saved_settings.png').read_bytes()).hexdigest();(P/'intake_inventory.json').write_text(json.dumps(inventory,indent=2))
