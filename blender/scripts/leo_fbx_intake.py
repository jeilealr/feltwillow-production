"""Read-only geometry intake from owner-provided FBX; preserve raw bytes/maps."""
import bpy, json, hashlib, shutil, sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
AREA=ROOT/'blender'
SOURCE=ROOT.parent/'model.fbx'
RAW=AREA/'assets/characters/leo/imports/tripo_owner_model'
RAW.mkdir(parents=True,exist_ok=True)
DEST=RAW/'model.fbx'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if DEST.exists() and sha(DEST)!=sha(SOURCE):raise RuntimeError('Existing raw import differs')
if not DEST.exists():shutil.copy2(SOURCE,DEST)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(DEST),use_anim=False)
bpy.context.view_layer.update()
sys.path.insert(0,str(ROOT/'.claude/skills/feltwillow-blender-production/scripts'))
from blender_inspect import inventory
report=inventory(bpy)
report['source']={'path':'../model.fbx','sha256':sha(SOURCE),'raw_copy':str(DEST.relative_to(ROOT)),
 'provider':'Tripo per owner context; exact endpoint/version unverified','request_id':None,'seed':None,
 'generation_prompt':None,'cost':None,'license_receipt':'not supplied; no publication authorization inferred'}
report['bounds']={o.name:{'min':[min((o.matrix_world@Vector(c))[j] for c in o.bound_box) for j in range(3)],
 'max':[max((o.matrix_world@Vector(c))[j] for c in o.bound_box) for j in range(3)]} for o in bpy.data.objects if o.type=='MESH'}
report['material_nodes']={m.name:[{'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None} for n in m.node_tree.nodes] for m in bpy.data.materials if m.use_nodes}
for im in bpy.data.images:
    if im.has_data:
        # Preserve embedded textures as explicit local provenance files as well.
        if im.packed_file:
            p=RAW/(Path(im.filepath).name or im.name+'.png')
            if not p.exists():p.write_bytes(im.packed_file.data)
        im.pack()
report['packed_image_names']=[im.name for im in bpy.data.images if im.packed_file]
(AREA/'docs/leo_tripo_input_inventory.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(RAW/'leo_import_untouched.blend'),compress=True)
print(json.dumps({'bounds':report['bounds'],'objects':len(report['objects']),'materials':report['material_nodes'],'images':report['images']},indent=2))
