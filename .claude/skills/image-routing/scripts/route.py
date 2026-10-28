"""Offline routing of explicitly classified operations; no model/provider execution."""
import argparse
import json

ARTISTIC = {'generate', 'artistic_edit', 'appearance_change', 'visual_assessment'}
TECHNICAL = {'code', 'metadata', 'hash', 'compositing_software', 'diagnostics', 'contact_sheet', 'html_review', 'tests'}

def route(operation, gpt_image_capability=False):
    if operation in ARTISTIC:
        return 'gpt' if gpt_image_capability else 'handoff_to_gpt'
    if operation in TECHNICAL:
        return 'coding_model'
    raise ValueError('Unknown operation: classify it explicitly before routing')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=sorted(ARTISTIC | TECHNICAL))
    parser.add_argument('--gpt-image-capability', action='store_true')
    args = parser.parse_args()
    print(json.dumps({'route': route(args.operation, args.gpt_image_capability), 'owner_approval_inferred': False}))
