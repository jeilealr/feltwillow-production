#!/usr/bin/env python3
"""Check selected active bytes and clean inventory, separately from render gates."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from production.keyframe_visual_gate import build_frame_dispositions
from production.keyframe_reference_gate import validate_active_inventory
HOME=Path(__file__).resolve().parent;STORY=HOME.parent.parent
KEYFRAMES=ROOT/'character/characters/lion_and_mouse_v6/interactions/keyframes'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    report=load(HOME/'owner_adoption.json');plan=load(STORY/'keyframe_plan.json');reviews=load(STORY/'keyframe_visual_reviews.json');acceptance=load(STORY/'owner_visual_acceptance.json');selected={f['id']:f for f in acceptance['images']}
    assert report['status']=='adopted' and len(plan['images'])==96 and report['count']==41
    assert not validate_active_inventory(plan,KEYFRAMES)
    assert reviews['frame_dispositions']==build_frame_dispositions(plan,reviews)
    for f in plan['images']:
        assert sha(ROOT/f['candidate_path'])==f['sha256']==selected[f['id']]['sha256']
        assert f['candidate_path']==selected[f['id']]['path']
        if f['id'] in reviews['images']:assert reviews['images'][f['id']]['sha256']==f['sha256']
    for f in report['frames']:
        assert not (ROOT/f['previous_path']).exists()
        assert sha(ROOT/f['archive_path'])==f['previous_sha256']
        assert sha(ROOT/f['active_path'])==sha(ROOT/f['review_artifact_path'])==f['sha256']
        assert all(v is None for v in reviews['images'][f['id']]['checks'].values())
    manifest=load(KEYFRAMES/'.review/contact_sheets/current/manifest.json')
    assert {f['id']:(f['candidate_path'],f['sha256']) for f in manifest['images']}=={f['id']:(f['candidate_path'],f['sha256']) for f in plan['images']}
    sheets=[KEYFRAMES/'.review/contact_sheets/current'/('scene%02d_keyframes.png'%i) for i in range(1,17)]
    assert all(p.exists() for p in sheets)
    links=0
    for name in ['owner_review.html','scene_continuity.html']:
        for link in re.findall(r'(?:src|href)="([^"]+)"',(HOME/name).read_text()):
            if not link.startswith('#'):assert (HOME/link).exists(),(name,link);links+=1
    for scene in load(STORY/'video_boundary_plan.json')['scenes']:
        for key in ['start_image','first_own_image','end_image']:assert (ROOT/scene[key]).exists()
        for transition in scene['internal_transitions']:
            for key in ['start_image','end_image','next_start_image']:assert (ROOT/transition[key]).exists()
    result={'status':'passed','active_images':96,'adopted_replacements':41,'retained':55,'superseded_direct_images':0,'contact_sheets':16,'review_links':links,'active_hashes_owner_ledger_and_visual_records_match':True,'archive_hashes_match':True,'render_and_authority_gates':'remain separate and pending','scene_sheet_hashes':{str(p.relative_to(ROOT)):sha(p) for p in sheets}}
    (HOME/'adoption_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: 96 unique active keyframes; 41 approved replacements; exact owner/hash records; no obsolete direct versions; 16 sheets and all review/boundary links current.')
if __name__=='__main__':main()
