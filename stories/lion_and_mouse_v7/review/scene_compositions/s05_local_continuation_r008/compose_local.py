"""Compose selected S05 pose layers against the accepted original Leo scene."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

D = Path(__file__).resolve().parent
R = D.parents[4]

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    manifest = read(D/'COMPOSITION_BATCH.json')
    bg = manifest['background']
    assert digest(R/bg['path']) == bg['sha256']
    assert not (D/'EXECUTION.json').exists(), 'Preserve existing outputs; no duplicate execution'
    base = Image.open(R/bg['path']).convert('RGBA')
    outputs, checks, observations = [], [], []
    (D/'receipts').mkdir(exist_ok=True)
    for index, job in enumerate(manifest['jobs'], 1):
        actor = job['actor']
        assert digest(R/actor['path']) == actor['sha256']
        assert digest(R/actor['sidecar']['path']) == actor['sidecar']['sha256']
        for key, hash_key in [('wav','sha256'), ('metadata','metadata_sha256')]:
            assert digest(R/job['audio'][key]) == job['audio'][hash_key]
        image = Image.open(R/actor['path']).convert('RGBA')
        size = tuple(round(d*job['scale']) for d in image.size)
        image = image.resize(size, Image.Resampling.LANCZOS)
        layer = Image.new('RGBA', base.size)
        layer.paste(image, tuple(job['translate_pixels']))
        result = Image.alpha_composite(base, layer).convert('RGB')
        path = R/job['output']
        side = path.with_suffix('.json')
        assert not path.exists() and not side.exists()
        result.save(path)
        with Image.open(path) as saved:
            saved.load()
            pixels = np.asarray(saved)
        outside = np.asarray(layer.getchannel('A')) == 0
        changed = int(np.count_nonzero(np.any(pixels != np.asarray(base.convert('RGB')), axis=2) & outside))
        assert changed == 0
        note = 'Exact selected '+job['pose_variant']+' layer, uniformly scaled 0.32; grey felt design unchanged. Original Leo/background preserved outside actor alpha. Manual path/contact, depth, occlusion and lighting need owner review; no shadow synthesized. Pose bbox varies; camera_unknown. Not an approved motion sequence.'
        receipt = {'schema':'feltwillow.scene-performance-candidate.v1', 'image_id':job['image_id'],
                   'line_id':job['line_id'], 'beat_id':job['beat_id'], 'path':job['output'],
                   'sha256':digest(path), 'dimensions':list(base.size), 'mode':'RGB',
                   'status':'candidate_pending_owner_review', 'owner_decision':None,
                   'audio':job['audio'], 'state_id':job['state_id'], 'world_state':job['world_state'],
                   'events_before':job['events_before'], 'performance':job['performance'],
                   'background_continuity':job['background_continuity'], 'continuity_group':job['continuity_group'],
                   'creation':{'method':manifest['method'], 'provider_calls':0, 'actual_cost':0,
                               'manifest':str((D/'COMPOSITION_BATCH.json').relative_to(R)),
                               'manifest_sha256':digest(D/'COMPOSITION_BATCH.json'),
                               'background':bg, 'actor':actor, 'scale':job['scale'],
                               'translate_pixels':job['translate_pixels'], 'resampling':'whole-layer Lanczos'},
                   'inputs':[bg,actor], 'technical_review':note, 'production_readiness':False}
        # Bind actual submitted layer bytes rather than leave stale planned pose hashes.
        receipt['performance']['Milo']['pose_revision']=job['pose_revision']
        receipt['performance']['Milo']['pose_sha256']=actor['sha256']
        write(side,receipt)
        receipt_path=D/'receipts'/f'{index:03d}.json'
        write(receipt_path,receipt)
        row={'image_id':job['image_id'], 'path':job['output'], 'sha256':digest(path),
             'sidecar':{'path':str(side.relative_to(R)), 'sha256':digest(side)},
             'receipt':{'path':str(receipt_path.relative_to(R)), 'sha256':digest(receipt_path)},
             'dimensions':list(base.size), 'status':'candidate_pending_owner_review'}
        outputs.append(row)
        checks.append({'image_id':job['image_id'], 'source_audio_hashes':'verified',
                       'png_decode':'pass', 'changed_pixels_outside_actor_alpha':changed,
                       'uniform_scale':job['scale'], 'resampled_dimensions':list(size), 'physical_contact_pass':None})
        observations.append({'image_id':job['image_id'], 'image_sha256':row['sha256'], 'observation':note,
                             'owner_decision':None, 'exact_background_outside_actor_alpha':True})
    write(D/'EXECUTION.json', {'completed':len(outputs), 'outputs':outputs, 'provider_calls':0, 'actual_cost':0})
    write(D/'COMPOSITION_VALIDATION.json', {'images':checks, 'full_suite':'not run per owner cadence'})
    write(D/'VISUAL_OBSERVATIONS.json', {'images':observations})
    sheet=Image.new('RGB',(1000,610),(35,39,32))
    draw=ImageDraw.Draw(sheet)
    for k,row in enumerate(outputs):
        tile=Image.open(R/row['path']).convert('RGB');tile.thumbnail((490,276))
        x=(k%2)*500;y=(k//2)*305
        sheet.paste(tile,(x,y+25));draw.text((x+6,y+6),row['image_id'],fill='white')
    sheet.save(D/'comparison.jpg',quality=94)
    print('Saved',len(outputs),'scene candidates; protected pixels unchanged in all.')

if __name__=='__main__':
    main()
