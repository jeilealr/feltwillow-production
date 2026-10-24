"""Freeze the owner's current S01-S05 selections and clean active candidate folders.

Historical source bytes move into a hash-checked provenance archive. Only
regenerable caches are permanently removed. No canonical, audio or current
performance bytes are changed; no Git commands are performed.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil

from PIL import Image

D=Path(__file__).resolve().parent
R=D.parents[3]
S=R/'stories/lion_and_mouse_v7'

def read(p):
    return json.loads(p.read_text())

def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    # This script sits directly below review/, unlike scene-batch builders.
    assert (R/'production').is_dir(),R
    manifest_path=D/'CLEANUP_MANIFEST.json'
    assert not manifest_path.exists(),'Cleanup already recorded; verify rather than repeat'
    opening=read(S/'scene_image_selection.json')
    opening_hash=digest(S/'scene_image_selection.json')
    batches=['s04_s05_setup_r001','s05_owner_sequence_through_trip_r003',
             's05_local_continuation_r008','s05_leo_portrait_completion_r009',
             's05_contact_grounding_r010','s05_leo_expression_portraits_r011']
    current={}
    for batch in batches:
        for row in read(S/'review/scene_compositions'/batch/'EXECUTION.json').get('outputs',[]):
            current[row['image_id']]=row
    images=opening['images']+list(current.values())
    enriched=[]
    for row in images:
        row=dict(row)
        for f in [row,row['sidecar']]:assert digest(R/f['path'])==f['sha256']
        side=read(R/row['sidecar']['path'])
        for k,h in [('wav','sha256'),('metadata','metadata_sha256')]:
            assert digest(R/side['audio'][k])==side['audio'][h]
        with Image.open(R/row['path']) as im:im.load();dims=list(im.size)
        row.update(line_id=side['line_id'],beat_id=side['beat_id'],dimensions=dims,
                   audio=side['audio'],selection='owner_selected_scene_depiction',
                   technical_review=side.get('technical_review'),readiness_limitations=side.get('readiness_limitations',[]))
        enriched.append(row)
    enriched.sort(key=lambda r:(r['line_id'],r['image_id'] or r['beat_id']+'-I00'))
    assert len({r['path'] for r in enriched})==len(enriched)==44
    ledger={'schema':'feltwillow.scene-image-selection.v1','story':'lion_and_mouse_v7',
            'scope':['S01','S02','S03','S04','S05'],'reviewer':'project_owner',
            'owner_statement':'the yall passed. now I want to set all the images from S01 to S05 so far and delete the cadidates that in the end we didnt accept we we have a clean version of v7 so far',
            'decision':'owner_selected_scene_images','count':len(enriched),
            'counts_by_scene':dict(Counter(r['line_id'][:3] for r in enriched)),
            'coverage':'available images selected so far; not all planned keys/complete video coverage',
            'technical_review':'Owner depiction selection preserves existing anatomy/contact/crop/geometry warnings; it is not video approval or numerical certification.',
            'images':enriched}
    write(S/'scene_image_selection_s01_s05.json',ledger)
    # Keep the old exact-hash S01-S03 handoff intact for compatibility.
    assert digest(S/'scene_image_selection.json')==opening_hash
    selected={r['path'] for r in enriched}
    lib=read(S/'character_performance_library.json')
    active_performances={v['file']['path'] for a in lib['assets'].values() for v in a['variants'].values() if v.get('file')}
    moves=set()
    scene=R/'character/characters/lion_and_mouse_v7/interactions/scene_compositions'
    for p in scene.glob('*.png'):
        if str(p.relative_to(R)) not in selected:moves.add(p)
    for a in lib['assets'].values():
        for v in a['variants'].values():
            for old in v.get('superseded_candidates',[]):
                f=old.get('file') or {}
                if f.get('path') and f['path'] not in active_performances:
                    p=R/f['path']
                    if p.is_file():moves.add(p)
    # Sidecars remain immutable alongside relocated source PNGs.
    for p in list(moves):
        if p.with_suffix('.json').is_file():moves.add(p.with_suffix('.json'))
    archive=S/'history/retained_sources'
    index_path=archive/'INDEX.json'
    index=read(index_path) if index_path.exists() else {'schema':'feltwillow.retained-sources.v1','purpose':'read-only source provenance; excluded from active selection/gallery','files':{}}
    moving=[]
    for p in sorted(moves):
        logical=str(p.relative_to(R));assert logical not in selected and logical not in active_performances
        destination=archive/'files'/logical
        row={'original_path':logical,'archived_path':str(destination.relative_to(R)),
             'sha256':digest(p),'bytes':p.stat().st_size,'reason':'superseded/rejected candidate retained only for provenance or historical audit'}
        assert not destination.exists(),destination
        destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,destination)
        assert digest(destination)==row['sha256']
        index['files'][logical]={'archived_path':row['archived_path'],'sha256':row['sha256']}
        moving.append(row)
    # Publish the resolver map before deleting original physical paths.
    write(index_path,index)
    for row in moving:
        p=R/row['original_path'];assert digest(p)==row['sha256'];p.unlink()
    removed=[]
    for pattern in ['*.pyc','.DS_Store']:
        for p in (S/'review').rglob(pattern):
            removed.append({'path':str(p.relative_to(R)),'sha256':digest(p),'bytes':p.stat().st_size,'reason':'regenerable local cache'})
            p.unlink()
    reuse=read(S/'review/scene_compositions/s05_owner_sequence_through_trip_r003/IMAGE_REUSE.json')
    reuse['selection']='owner_selected_shared_scene_use';reuse['selection_scope']='same accepted L005 pixels held through L006, separate unchanged WAV'
    write(S/'selected_images/IMAGE_REUSE.json',reuse)
    wanted={r['image_id'] for r in enriched if r['image_id']}
    gaps=[]
    for line in read(S/'audio_visual_plan.json')['lines']:
        if line['audio_scene'] not in ledger['scope']:continue
        for beat in line['beats']:
            for image in beat['image_sequence']['images']:
                if image['id'] not in wanted and image['id']!='S05-L006-B01-I01':
                    gaps.append({'image_id':image['id'],'line_id':line['line_id'],'phase':image.get('phase_intent'),'status':'no owner-selected scene bytes yet'})
    write(S/'selected_images/COVERAGE_GAPS.json',{'scope':ledger['scope'],'missing_planned_keys':gaps,'count':len(gaps),'note':'Selection so far does not imply complete audio-aligned motion coverage.'})
    (S/'selected_images/SHA256SUMS').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in enriched))
    write(manifest_path,{'owner_statement':ledger['owner_statement'],'selected_unique_images':44,
         'accepted_scene_uses_including_L006_reuse':45,'opening_ledger_sha256_unchanged':opening_hash,
         'relocated_source_files':moving,'permanently_removed_cache_files':removed,
         'relocated_bytes':sum(r['bytes'] for r in moving),'deleted_cache_bytes':sum(r['bytes'] for r in removed),
         'protected':'canonical/current performance/approved scene/audio bytes and historical receipt contents unchanged',
         'scope':'active S01-S05 scene folder now selected only; superseded reusable performance versions removed from active pose directories'})
    print(json.dumps({'selected':44,'scene_uses':45,'by_scene':ledger['counts_by_scene'],'archived_source_files':len(moving),'archived_bytes':sum(r['bytes'] for r in moving),'deleted_caches':len(removed),'missing_planned_keys':len(gaps)},indent=2))

if __name__=='__main__':main()
