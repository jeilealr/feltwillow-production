"""Record owner selection, compose existing portrait pixels, propose one clean plate.

No provider calls. Immutable generation receipts and source PNGs are preserved.
"""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

from PIL import Image, ImageFilter, ImageOps

D = Path(__file__).resolve().parent
R = D.parents[4]
S = R / 'stories/lion_and_mouse_v7'
C = S / 'review/character_performance_consistency_r001/s06_s07_pose_continuation_r002'


def read(p):
    return json.loads(p.read_text())


def write(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ref(p, **extra):
    return dict(path=str(p.relative_to(R)), sha256=digest(p), **extra)


def main():
    assert sys.prefix == '/Users/lealroja/miniconda3/envs/feltwillow'
    assert not (D / 'OPERATION.json').exists(), 'Preparation already completed'
    lib = read(S / 'character_performance_library.json')
    plan = read(S / 'audio_visual_plan.json')
    execution = read(C / 'EXECUTION.json')
    acceptance = D / 'owner_acceptance'
    acceptance.mkdir()
    selection = {'decisions': {}, 'joint_decisions': {},
                 'scope': 'Five depicted performance candidates selected; scene approval and measured anatomy remain separate.'}
    statement = 'They passed. we can create now the actual scenes wit hthe background now the we have the poses'
    for row in execution['outputs']:
        assert digest(R / row['path']) == row['sha256']
        joint = len(row['actors']) == 2
        group = lib['joint_performance_requirements'] if joint else lib['assets']
        asset = group[row['requirement_id']]
        decision = dict(revision=asset['revision'], variant=row['variant'], sha256=row['sha256'],
                        canonical_sha256=({a: v['sha256'] for a, v in asset['canonical'].items()} if joint else asset['canonical']['sha256']),
                        reviewer='project_owner', statement=statement, image_revision=row['image_revision'],
                        scope='joint_performance_use_only' if joint else 'performance_use_only')
        decision['requirement_id' if joint else 'asset_id'] = row['requirement_id']
        selection['joint_decisions' if joint else 'decisions'][row['requirement_id'] + ':' + row['variant']] = decision
    ledger = acceptance / 'OWNER_SELECTION.json'
    write(ledger, selection)
    changes = []
    for row in execution['outputs']:
        joint = len(row['actors']) == 2
        group = lib['joint_performance_requirements'] if joint else lib['assets']
        variant = group[row['requirement_id']]['variants'][row['variant']]
        decision = copy.deepcopy(selection['joint_decisions' if joint else 'decisions'][row['requirement_id'] + ':' + row['variant']])
        decision['record'] = ref(ledger)
        side = R / row['sidecar']['path']
        shutil.copy2(side, acceptance / side.name)
        old = digest(side)
        data = read(side)
        data.update(status='owner_selected_for_performance', owner_decision=decision)
        write(side, data)
        variant.update(status=data['status'], owner_decision=decision)
        variant['file']['sidecar']['sha256'] = digest(side)
        row['sidecar']['sha256'] = digest(side)
        changes.append(dict(path=str(side.relative_to(R)), before_sha256=old, after_sha256=digest(side),
                            reason='Owner review overlay; original sidecar archived; PNG and immutable generation receipt unchanged'))
    execution['review_status'] = 'five continuation performances selected by owner'
    execution.setdefault('review_changes', []).extend(changes)
    write(C / 'EXECUTION.json', execution)
    write(acceptance / 'REVIEW_CHANGES.json', changes)
    write(S / 'character_performance_library.json', lib)

    plate_ref = plan['continuity_groups']['great_tree_block']['background_reference']
    source = R / plate_ref['path']
    assert digest(source) == plate_ref['sha256']
    # This foliage crop ends above the sleeping lion. No old actor enters portraits.
    crop = (780, 0, 1672, 285)
    with Image.open(source) as original:
        background = ImageOps.fit(original.convert('RGB').crop(crop), (1672, 941),
                                  method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(22))
    background_path = D / 'S07_foliage_blurred_background.png'
    background.save(background_path)
    write(D / 'LOCAL_COMPOSITION_AUTHORIZATION.json', {
        'statement': statement, 'scope': 'Actual scenes from selected performance layers and established location; local Pillow compositing authorized in prior session',
        'paid_requests_authorized_by_this_record': 0,
        'method': 'Uniform whole-image actor scale, alpha composite over actor-free blurred source crop; no facial/body redraw or recoloring'})
    portraits = [
        ('S07-L001', 'Leo', 'leo.s07.dialogue.portrait.3q', 'default', 'annoyed_leo'),
        ('S07-L002', 'Leo', 'leo.expression.mildly_annoyed.s07.3q', 'questioning', 'questioning_leo'),
        ('S07-L003', 'Milo', 'milo.portrait.base.3q_left', 'default', 'apologetic_milo'),
        ('S07-L004', 'Milo', 'milo.expression.anxious_sincere.3q_left', 'default', 'anxious_milo'),
        ('S07-L005', 'Milo', 'milo.expression.sincere.3q_left', 'default', 'sincere_milo'),
    ]
    outputs = []
    receipt_dir = D / 'receipts'
    receipt_dir.mkdir()
    for n, (lid, actor, aid, name, subject) in enumerate(portraits, 1):
        line = next(l for l in plan['lines'] if l['line_id'] == lid)
        beat = line['beats'][0]
        image = beat['image_sequence']['images'][0]
        variant = lib['assets'][aid]['variants'][name]
        f = variant['file']
        assert variant['status'] == 'owner_selected_for_performance'
        assert digest(R / f['path']) == f['sha256']
        scale = 0.65 if actor == 'Leo' else 0.72
        # Same scale and origin within each portrait family, including the
        # one-pixel wider anxious Milo canvas. Never independently fit each face.
        origin = (464, 48) if actor == 'Leo' else (351, 100)
        with Image.open(R / f['path']) as im:
            im.load()
            layer = im.convert('RGBA').resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
        canvas = background.convert('RGBA')
        canvas.alpha_composite(layer, origin)
        out = R / 'character/characters/lion_and_mouse_v7/interactions/scene_compositions' / (image['id'] + '_single_' + subject + '_portrait_r001_candidate.png')
        assert not out.exists()
        canvas.convert('RGB').save(out)
        receipt = receipt_dir / f'{n:03d}.json'
        recipe = {
            'method': 'local Pillow alpha composite; no generative calls', 'endpoint': None, 'actual_cost': 0,
            'inputs': [ref(R / f['path'], role='owner_selected_performance', asset_id=aid, variant=name),
                       ref(source, role='location_source_foliage_only'), ref(background_path, role='blurred_actor_free_background')],
            'background_crop_native_pixels': list(crop), 'background_output_dimensions': [1672, 941],
            'background_fit': 'Pillow ImageOps.fit centered; LANCZOS; GaussianBlur radius 22',
            'actor_uniform_scale': scale, 'actor_origin_pixels': list(origin), 'resampling': 'LANCZOS',
            'preserve': 'original character color, body, face and alpha; no mirroring, head/body resizing or lighting recolor',
            'portrait_family': actor + '_s07_dialogue', 'owner_performance_decision': variant['owner_decision'],
        }
        write(receipt, recipe)
        side = out.with_suffix('.json')
        data = dict(image_id=image['id'], line_id=lid, beat_id=beat['id'], image_revision='r001', role='single',
                    path=str(out.relative_to(R)), sha256=digest(out), dimensions=[1672, 941], audio=line['audio'],
                    location_view=image['location_view'], world_state_ref=image['state'],
                    status='candidate_pending_owner_scene_review', owner_approval=None,
                    creation=dict(recipe, receipt=ref(receipt)),
                    technical_review='Exact selected actor raster reused at uniform family scale. Scene lighting, framing and alpha integration need owner review; projected anatomy is not newly measured. Original expression geometry differences retained.')
        write(side, data)
        outputs.append(dict(data, sidecar=ref(side), receipt=ref(receipt)))
    write(D / 'LOCAL_SCENES.json', {'outputs': outputs, 'provider_calls': 0, 'actual_cost': 0})

    clean = D / 'S06-L001-B01_location_great_tree_clean_plate_r001_candidate.png'
    prompt = (
        'Edit the supplied 1672x941 felt woodland scene into a character-free clean background plate for a locked camera sequence. '
        'Remove ONLY the sleeping lion, including all mane, ears, face, torso, legs, paws, tail and lion-caused contact shadows. '
        'Reconstruct the mossy grass, small ground vegetation and earth that were hidden beneath his silhouette, connecting naturally to the visible surroundings. '
        'There is no mouse in this source; add no mouse or other animal. Keep the same great tree, roots, sunset sky and sun, valley, stream, rocks, background foliage, '
        'horizon, camera framing and 1672x941 canvas. Preserve all visible scene pixels away from the old lion and its immediate shadow area. '
        'No scene redesign, new paths, zoom, crop, lens change, new props, text, symbols or watermark. '
        'Opaque background image, no transparent holes. This is environmental reconstruction only; no replacement characters. One output only.'
    )
    operation = {
        'schema': 'feltwillow.scene-generation-proposal.v1', 'status': 'prepared_pending_concrete_owner_approval',
        'endpoint': 'image_gen.imagegen', 'request_count': 1, 'outputs_per_request': 1, 'automatic_retries': 0,
        'pricing': 'Built-in model, current per-image pricing, seed and actual charge are not exposed; unknown, not assumed free',
        'estimated_total_cost': None,
        'purpose': 'Reconstruct old-Leo area once; then use one protected plate and exact owner-selected pair layers for connected S06 scenes',
        'requests': [{'sequence': 1, 'output': str(clean.relative_to(R)), 'inputs': [ref(source, role='edit_target_exact_background_camera')],
                      'tool_arguments': {'prompt': prompt, 'referenced_image_paths': [str(source)], 'transparent_background': False}}],
        'post_generation_gate': 'Inspect reconstruction, preserve raw output and receipt, create an explicit old-actor/shadow repair mask, restore exact source pixels outside that mask and review it. No whole-scene generative substitution or duplicate sleeping Leo.',
        'not_in_this_paid_operation': 'No character regeneration, new performance phases, audio, video, retries or publication',
    }
    write(D / 'OPERATION.json', operation)
    missing = []
    pair = lib['joint_performance_requirements']['milo_leo.s06.great_tree']
    for name, v in pair['variants'].items():
        if v.get('file') is None:
            missing.append(dict(variant=name, image_ids=v['image_ids'], status='not generated; needs exact selected pose references in subsequent concrete scene-edit operation'))
    write(D / 'S06_REALIZATION_PLAN.json', {
        'selected_pair_anchors': [dict(variant=n, file=v['file']) for n, v in pair['variants'].items() if v.get('file')],
        'missing_phases': missing, 'background': plate_ref,
        'staging': 'Register Leo resting trunk/hips/ground support against S05. One uniform pair transform for selected anchors; Milo screen-right. Body shape and apparent height may change with pose. Review paw-foot overlap in full scene.',
        'continuity_repair': 'S05 last transition matches same-location S06 entry; S06 L003/L004/L005 begin with exact previous endpoint before their declared reaction event, then end on new reaction. World states/events, narration and WAV bytes unchanged.',
        'scope': 'S07 five actual local portrait scenes saved. S06 waits for clean plate; seven phases still missing. Do not claim full S06 coverage.'})
    (D / 'REVIEW.md').write_text(
        '# S06/S07 scene production\n\nFive approved continuation performances are now exact-hash selected. Five S07 portrait scene candidates are locally composed from selected layers over one blurred, actor-free foliage crop of S05. No character redraw or paid calls.\n\n'
        'S06 needs one clean-background repair before placing the three selected joint anchors. Seven additional motion/reaction phases remain ungenerated; they need subsequent exact-reference scene operations after anchor review.\n\n'
        'Concrete next paid operation: **1 request, image_gen.imagegen, transparent_background=false, one output, no retries, cost unknown**. Remove sleeping Leo and reconstruct only the hidden ground. Exact input path/hash and full prompt/settings are in [OPERATION.json](OPERATION.json). Its SHA256 is `' + digest(D / 'OPERATION.json') + '`.\n\n'
        'The raw generated plate will be preserved. A recorded repair mask will restore original background pixels outside old Leo/shadow regions; exact background continuity is verified afterward, not assumed from prompting. Existing selected S01–S05 PNGs remain unchanged. No full suite or Git publication.\n')
    print('Five local S07 scenes saved; one clean-plate request prepared, not submitted.')


if __name__ == '__main__':
    main()
