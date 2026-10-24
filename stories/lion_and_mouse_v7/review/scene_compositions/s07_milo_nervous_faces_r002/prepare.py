"""Record selective scene acceptance and prepare three face-only requests."""
import copy,hashlib,json,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[4];S=R/'stories/lion_and_mouse_v7';F=D.parent/'s06_s07_background_scenes_r001'
def read(p):return json.loads(p.read_text())
def write(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p,**extra):return dict(path=str(p.relative_to(R)),sha256=sha(p),**extra)
def main():
 assert not (D/'OPERATION.json').exists()
 statement='maybe 7-L003-B01-I01 · scene candidate and the other following S07-L004-B01-I01 · scene candidate and S07-L005-B01-I01 · scene candidate should show a Milo a bit more nervous? . the other iamges I think are fine'
 a=D/'owner_acceptance';a.mkdir();selected=[];changes=[]
 journals=[F/'S06_SCENES.json',F/'LOCAL_SCENES.json'];loaded=[read(p) for p in journals]
 for journal in loaded:
  for row in journal['outputs']:
   if row['image_id'][:8] in ['S07-L003','S07-L004','S07-L005']:continue
   assert sha(R/row['path'])==row['sha256'];selected.append({'image_id':row['image_id'],'path':row['path'],'sha256':row['sha256'],'image_revision':row['image_revision'],'reviewer':'project_owner','scope':'scene_depiction_only','statement':statement})
 ledger=a/'OWNER_SELECTION.json';write(ledger,{'images':selected,'count':len(selected),'scope':'Three S06 anchors and two Leo S07 portraits only. Milo S07 L003-L005 require nervous-face revisions. No missing phases, numerical anatomy or video approval inferred.'});assert len(selected)==5
 registry_path=S/'scene_composition_candidates_s06_s07.json';registry=read(registry_path)
 for path,journal in zip(journals,loaded):
  for row in journal['outputs']:
   match=next((s for s in selected if s['image_id']==row['image_id']),None)
   if not match:continue
   side=R/row['sidecar']['path'];assert sha(side)==row['sidecar']['sha256'];shutil.copy2(side,a/side.name);old=sha(side)
   decision=dict(match,record=ref(ledger));data=read(side);data.update(status='owner_selected_scene_image',owner_approval=decision);write(side,data)
   row.update(status=data['status'],owner_approval=decision,sidecar=ref(side));changes.append({'path':str(side.relative_to(R)),'before_sha256':old,'after_sha256':sha(side),'reason':'Owner review overlay; PNG and original creation receipt unchanged, prior sidecar archived'})
   for item in registry['images']:
    if item['image_id']==row['image_id'] and item['sha256']==row['sha256']:item.update(status=data['status'],owner_approval=decision,sidecar=ref(side))
  write(path,journal)
 write(registry_path,registry);write(a/'REVIEW_CHANGES.json',changes)
 milo=[row for row in loaded[1]['outputs'] if row['image_id'][:8] in ['S07-L003','S07-L004','S07-L005']]
 actions=[
  'L003: he blurts an anxious apology to the much larger lion. Lift the inner brow ends into an unmistakably worried pleading shape, slightly tense the lower eyelids and cheeks, and give the closed mouth a small worried downward crease. Remove the relaxed smile. He is frightened about having disturbed Leo, but remains child-friendly and readable, without exaggerated panic.',
  'L004: he nervously explains taking the shortcut to get home before dark. His brows and eyelids should show tense worried concentration and apprehension about Leo’s response. Increase nervous facial tension compared with the edit target, with a slightly compressed closed mouth and worried corners. No relaxed or happy smile; this is an anxious explanation, not sadness alone.',
  'L005: he makes a sincere promise while still visibly intimidated. Give him pleading raised inner brows, worried eyes and a small tightly closed uncertain mouth. Remove the reassuring happy smile. Convey nervous sincerity and concern about being believed, slightly softer than the rushed explanation but still clearly apprehensive.'
 ]
 canonical=R/'character/characters/lion_and_mouse_v7/Milo/canonical/full-body_milo_neutral_pose_r01.png'
 requests=[]
 for row,acting in zip(milo,actions):
  source=R/row['path'];assert sha(source)==row['sha256']
  prompt=('Edit only Milo’s local facial expression in reference 1, the existing 1672x941 scene. '+acting+
   ' Keep his gaze up toward screen-left to offscreen Leo. Preserve exact head pitch/yaw, skull and muzzle outline, eye size and spacing, green iris palette, nose, ears and ear placement, whiskers, neck, shoulders, visible cream chest and torso silhouette. Keep the same felt texture, intrinsic colors, lighting, whole-character scale, position, image canvas and blurred background. Facial acting comes from brows, eyelids, cheek tension and closed mouth crease only. No enlarged head or eyes, head tilt, zoom, reframing, body redraw or mirroring. Keep his mouth closed and toothless; this is a still dialogue boundary, not a baked speech shape. Reference 2 supplies canonical Milo identity and material only, not its neutral acting or frontal body pose. No tears, sweat drops, emotion icons, props, text or watermark. One opaque output only. Surrounding pixels must remain as close as possible; exact preservation will be checked and restored outside a recorded facial-edit mask after generation.')
  raw=D/(row['image_id']+'_single_nervous_face_raw_r002_candidate.png')
  final=R/'character/characters/lion_and_mouse_v7/interactions/scene_compositions'/(row['image_id']+'_single_nervous_milo_portrait_r002_candidate.png')
  assert not raw.exists() and not final.exists()
  requests.append({'sequence':len(requests)+1,'image_id':row['image_id'],'output':str(raw.relative_to(R)),'protected_scene_output':str(final.relative_to(R)),'audio':row['audio'],'state_ref':row['world_state_ref'],'inputs':[ref(source,role='edit_target_exact_scene_geometry'),ref(canonical,role='canonical_identity_material_only')],'tool_arguments':{'prompt':prompt,'referenced_image_paths':[str(source),str(canonical)],'transparent_background':False}})
 op={'schema':'feltwillow.scene-generation-proposal.v1','status':'prepared_pending_concrete_owner_approval','endpoint':'image_gen.imagegen','request_count':3,'outputs_per_request':1,'automatic_retries':0,'estimated_total_cost':None,'pricing':'Current built-in model, seed and per-image charge not exposed; total cost unknown, not assumed free','scope':'Only S07 L003-L005 Milo facial acting; five other current scene PNGs retained at selected hashes; no new S06 phases','post_generation':'Preserve raw PNG/receipt; inspect head geometry; use explicit local facial masks to restore exact original background/body/ears outside mask. Do not independently rescale head or body. Register final candidates only after hash/visual checks. New scene acting is not automatically a reusable expression asset.','requests':requests};write(D/'OPERATION.json',op)
 write(D/'OWNER_FEEDBACK.json',{'statement':statement,'selected_other_scenes':selected,'revise':[{'image_id':r['image_id'],'sha256':r['sha256'],'path':r['path']} for r in milo],'current_milo_scenes':'remain displayed as needs nervous-face revision until new bytes exist','calls_submitted':0})
 (D/'REVIEW.md').write_text('# Nervous Milo S07 portrait correction\n\nL003 worried apology, L004 tense shortcut explanation, L005 nervous sincere promise. Closed toothless mouths; gaze up-left toward Leo. Preserve the existing body/crop/head proportions and background. Five other scene depictions selected at exact hashes; source PNGs/creation receipts unchanged.\n\nConcrete proposal: **3 image_gen.imagegen requests, one opaque output each, no retries, cost unknown**. Full input paths/hashes, prompts and settings are in [OPERATION.json](OPERATION.json); SHA256 `'+sha(D/'OPERATION.json')+'`. No request submitted.\n\nRaw generated scenes are preserved. Local recorded facial masks restore original pixels outside the reviewed face area. If geometry drifts, flag it rather than independently resize the head. New expressions do not automatically replace approved reusable performance files. No S06 phase generation, audio/video, full suite or Git publication.\n')
 print('Selected five other scene depictions; three exact facial-edit requests prepared, not submitted.')
if __name__=='__main__':main()
