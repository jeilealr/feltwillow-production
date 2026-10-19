"""Resolve reviewed pose calibrations and layer placement before common crop."""
from pathlib import Path

try:
    from .paired_images import (load_story, verify, compose_master, digest,
                                atomic_json, endpoint_spec)
except ImportError:
    from paired_images import (load_story, verify, compose_master, digest,
                               atomic_json, endpoint_spec)


def compose_recipe(root, recipe, output):
    from PIL import Image
    folder, plan, chars, locs = load_story(root, recipe['story'])
    endpoint = plan['endpoints'][recipe['endpoint_id']]
    setup = locs['setups'][endpoint['setup_id']]
    if setup['status'] != 'owner_approved':
        raise ValueError('setup needs foundation calibration/support/axis review')
    if Path(output).exists() or Path(output).with_suffix('.json').exists():
        raise ValueError('composition output exists; use a new immutable candidate path')
    layers = []
    source_records = []
    for layer in recipe['layers']:
        calibration = chars['pose_calibrations'][layer['calibration_id']]
        source = verify(root, calibration['source'], approved=True)
        if digest(source) != calibration['source']['sha256']:
            raise ValueError('calibration source changed')
        image = Image.open(source).convert('RGBA')
        if len(image.getextrema()[3]) != 2 or image.getextrema()[3][0] == 255:
            raise ValueError('reviewed RGBA matte required; do not infer a new matte')
        layers.append({'image': image, 'calibration': calibration, 'placement': layer['placement']})
        source_records.append({'calibration_id': layer['calibration_id'], 'source': calibration['source'],
                               'placement': layer['placement']})
    with Image.open(verify(root, setup['plate'])) as plate:
        image = compose_master(plate, layers, setup)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    receipt = {'schema': 'paired_composition_v1', 'endpoint_id': recipe['endpoint_id'],
        'spec_sha256': endpoint_spec(plan, chars, locs, recipe['endpoint_id']),
        'setup_id': endpoint['setup_id'], 'plate': setup['plate'], 'sources': source_records,
        'crop_rect_norm': setup['crop_rect_norm'], 'output_size': setup['output_size'],
        'image_sha256': digest(output), 'status': 'candidate_requires_pixel_and_visual_review'}
    atomic_json(output.with_suffix('.json'), receipt)
    return receipt
