#!/usr/bin/env python3
"""Historical paired-only utility; migrated v7 uses audio_visual_plan.py.
CPU-only v7 preflight and planned Wan input contract; never starts a render."""
import argparse
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from production.paired_images import load_story,readiness,read,verify,atomic_json,digest
from feltwillow.wan import model_id,LIGHTNING


def planned_contract(root,story):
    folder,plan,chars,locs=load_story(root,story)
    blockers=readiness(root,story,'video')
    if blockers:raise ValueError('\n'.join(blockers))
    selection=read(folder/'selection.json')['endpoints']
    pieces=[]
    for piece in plan['pieces']:
        setup=locs['setups'][piece['setup_id']]
        pair=[selection[piece[k]] for k in ['start_image','end_image']]
        for ref in pair:verify(root,ref)
        pieces.append({'id':piece['id'],'image':pair[0],'last_image':pair[1],
            'setup_id':piece['setup_id'],'output_size':setup['output_size'],
            'preprocessing':'identical feltwillow.wan.fit on image and last_image',
            'audio_intervals':piece['audio_intervals'],'handoff':piece['handoff'],
            'actual_generated_first':None,'actual_generated_last':None,
            'video_review':'pending','dialogue_review':'pending'})
    return {'schema':'feltwillow.paired-wan-inputs.v1','story':story,
        'plan_sha256':digest(folder/'shot_plan.json'),'model':model_id('i2v'),
        'lightning_recipe':LIGHTNING,'normal_recipe':'existing feltwillow.wan I2V settings; choose exact run parameters explicitly',
        'status':'planned_input_receipt_not_render_or_video_approval','pieces':pieces}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--story',required=True)
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--preflight',action='store_true')
    modes.add_argument('--export-contract',type=Path)
    args=parser.parse_args()
    try:
        if args.preflight:
            blockers=readiness(ROOT,args.story,'video')
            for b in blockers[:20]:print('BLOCKED:',b)
            print(f'{len(blockers)} blockers; no weights loaded, audio generated or renders submitted')
            return bool(blockers)
        contract=planned_contract(ROOT,args.story)
        if args.export_contract.exists():raise ValueError('contract destination exists; choose a new path')
        atomic_json(args.export_contract,contract)
    except (ValueError,KeyError,OSError) as exc:parser.exit(1,f'V7_RUNTIME_BLOCKED: {exc}\n')
    return 0

if __name__=='__main__':raise SystemExit(main())
