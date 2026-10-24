"""Owner-authorized local composition; preserves source bytes and reviewed anatomy."""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

D = Path(__file__).resolve().parent
R = D.parents[4]

def read(path):
    return json.loads(path.read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    recipe_path = D / 'COMPOSITION_RECIPE.json'
    recipe = read(recipe_path)
    authorization = read(D / 'AUTHORIZATION.json')
    assert authorization['recipe_sha256'] == digest(recipe_path)
    for record in (recipe['background'], recipe['actor']):
        assert digest(R / record['path']) == record['sha256']
    out = R / recipe['output']
    side = out.with_suffix('.json')
    assert not out.exists() and not side.exists(), 'Do not overwrite a prior result'
    base = Image.open(R / recipe['background']['path']).convert('RGBA')
    actor = Image.open(R / recipe['actor']['path']).convert('RGBA')
    scale = recipe['actor']['transform']['uniform_scale']
    size = tuple(round(d * scale) for d in actor.size)
    assert list(size) == recipe['actor']['output_extent_pixels']
    resized = actor.resize(size, Image.Resampling.LANCZOS)
    layer = Image.new('RGBA', base.size)
    layer.paste(resized, tuple(recipe['actor']['transform']['translation_pixels']))
    result = Image.alpha_composite(base, layer).convert('RGB')
    result.save(out)
    with Image.open(out) as saved:
        saved.load()
        pixels = np.asarray(saved)
        assert saved.size == base.size
    protected = np.asarray(layer.getchannel('A')) == 0
    changed_protected = int(np.count_nonzero(np.any(pixels != np.asarray(base.convert('RGB')), axis=2) & protected))
    assert changed_protected == 0
    expected = np.asarray(Image.alpha_composite(base, layer).convert('RGB'))
    assert np.array_equal(pixels, expected)
    prior = read(R / 'character/characters/lion_and_mouse_v7/interactions/scene_compositions/S05-L008-B01-I02_key_first_joint_rear_paw_contact_r002_candidate.json')
    for key, hash_key in [('wav', 'sha256'), ('metadata', 'metadata_sha256')]:
        assert digest(R / prior['audio'][key]) == prior['audio'][hash_key]
    receipt = dict(prior)
    receipt.update(path=recipe['output'], sha256=digest(out), dimensions=list(base.size), mode='RGB', owner_decision=None,
                   creation={'method': recipe['method'], 'provider_calls': 0, 'actual_cost': 0,
                             'recipe': str(recipe_path.relative_to(R)), 'recipe_sha256': digest(recipe_path),
                             'authorization': str((D/'AUTHORIZATION.json').relative_to(R)),
                             'background': recipe['background'], 'actor': recipe['actor']},
                   inputs=[recipe['background'], recipe['actor']], technical_review='pending owner contact/scale/edge/lighting review',
                   production_readiness=False,
                   readiness_limitations=['Exact actor design reused through uniform whole-layer resampling; no new face or palette edits.',
                                         'No shadow synthesized; rear-paw contact, support, lighting and apparent scale require owner review.'])
    write(side, receipt)
    (D/'receipts').mkdir(exist_ok=True)
    immutable_receipt = D/'receipts/001.json'
    write(immutable_receipt, receipt)
    row = {'image_id': recipe['image_id'], 'path': recipe['output'], 'sha256': digest(out),
           'sidecar': {'path': str(side.relative_to(R)), 'sha256': digest(side)},
           'receipt': {'path': str(immutable_receipt.relative_to(R)), 'sha256': digest(immutable_receipt)},
           'dimensions': list(base.size), 'status': 'candidate_pending_owner_review'}
    write(D/'EXECUTION.json', {'method': recipe['method'], 'provider_calls': 0, 'actual_cost': 0, 'completed': 1, 'outputs': [row]})
    write(D/'COMPOSITION_VALIDATION.json', {'source_hashes': 'pass', 'png_decode': 'pass', 'uniform_scale': scale,
          'resampled_dimensions': list(size), 'protected_pixel_count': int(protected.sum()),
          'changed_pixels_outside_actor_alpha': changed_protected, 'exact_recipe_reconstruction': True,
          'anatomy_design': 'selected r004 raster reused; no independent body-part edits', 'camera': 'camera_unknown',
          'physical_contact_pass': None, 'owner_decision': None, 'full_suite': 'not run per owner cadence'})
    print(json.dumps(row, indent=2))

if __name__ == '__main__':
    main()
