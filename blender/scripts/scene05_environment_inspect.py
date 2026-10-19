"""Read-only existing prototype inspection, before any new modeling."""
import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'blender/renders/scene05_environment_r02'
paths=['blender/assets/environments/great_tree/great_tree_dusk_candidate.blend','blender/scenes/lion_and_mouse_v6/s05.blend','blender/assets/characters/leo/leo_canonical_tripo_candidate_r04.blend']
r={'files':[]}
for path in paths[:2]:
 p=ROOT/path;bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False)
 r['files'].append({'path':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'objects':len(bpy.data.objects),'collections':[x.name for x in bpy.data.collections],'cameras':[{'name':o.name,'location':list(o.location),'lens':o.data.lens} for o in bpy.data.objects if o.type=='CAMERA'],'libraries':[x.filepath for x in bpy.data.libraries]})
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(ROOT/paths[2]),link=False) as (src,dst):dst.objects=['Leo_surface']
o=dst.objects[0];z=[v.co.z for v in o.data.vertices];r['leo_scale']={'source':paths[2],'sha256':hashlib.sha256((ROOT/paths[2]).read_bytes()).hexdigest(),'surface_z_min':min(z),'surface_z_max':max(z),'neutral_height_bu':max(z)-min(z),'proxy_milo_height_bu':(max(z)-min(z))*.25,'unit_m_per_bu':.2,'note':'Source local coordinates have normalized identity transform; no posing or groom required for this anatomical standing height.'}
(P/'existing_asset_inventory.json').write_text(json.dumps(r,indent=2));print('EXISTING_INVENTORY',json.dumps(r['leo_scale']),flush=True)
