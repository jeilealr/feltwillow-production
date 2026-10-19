"""Actual bounded audit and final r04 review, no source edits."""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'blender/scripts'))
import leo_r02_review as audit
import leo_tripo_canonical_pass as prior
P=ROOT/'blender/renders/leo_tripo_canonical_r04';OUT=ROOT/'blender/assets/characters/leo/leo_canonical_tripo_candidate_r04.blend'
audit.P=P;audit.OUT=OUT;audit.audit()
prior.neutral();s=bpy.context.scene;s.cycles.seed=18102606;records=[]
for name,view,frame,size,samples in [('portrait','portrait',1,896,40),('full_body','front_three_quarter',1,768,32),('head_left','portrait',9,768,32),('head_right','portrait',25,768,32)]:
 prior.camera(view);s.frame_set(frame);s.render.resolution_x=size;s.render.resolution_y=size;s.cycles.samples=samples;s.render.filepath=str(P/(name+'.png'));bpy.ops.render.render(write_still=True)
 records.append({'path':name+'.png','sha256':hashlib.sha256((P/(name+'.png')).read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'frame':frame,'size':[size,size],'samples':samples,'camera':[list(r) for r in s.camera.matrix_world],'ortho_scale':s.camera.data.ortho_scale,'engine':'Cycles CPU','color':'Standard / None / exposure 0 / gamma 1'})
(P/'render_manifest.json').write_text(json.dumps(records,indent=2));print('R04_REVIEW_COMPLETE',flush=True)
