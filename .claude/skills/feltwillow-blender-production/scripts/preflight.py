#!/usr/bin/env python3
"""Read-only advisory manifest checks. No Blender, network or paid calls."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from fw_contracts import load_json, digest, validate_asset, validate_job, validate_chain

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='mode',required=True)
    for name in ('asset','job','chain','fingerprint'):
        s=sub.add_parser(name)
        s.add_argument('manifest',type=Path)
        if name in ('asset','job'):
            s.add_argument('--root',type=Path,required=True)
        if name=='asset':
            s.add_argument('--require-approved',action='store_true')
        if name=='job':
            s.add_argument('--ledger',type=Path,required=True)
        if name=='fingerprint':
            s.add_argument('--exclude',choices=('review','approval'),required=True)
    args=p.parse_args()
    try:
        doc=load_json(args.manifest)
        if args.mode=='fingerprint':
            print(digest(doc,(args.exclude,)));return 0
        if args.mode=='asset':
            errors=validate_asset(doc,args.root,args.require_approved)
        elif args.mode=='job':
            errors=validate_job(doc,load_json(args.ledger),args.root)
        else:
            errors=validate_chain(doc)
        print(json.dumps({'mode':args.mode,'metadata_valid':not errors,'errors':errors,
                          'scope':'Advisory only: not visual approval, rights certification or a spending enforcement gateway.'},indent=2))
        return 1 if errors else 0
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps({'metadata_valid':False,'input_error':str(exc)}));return 2

if __name__=='__main__':
    raise SystemExit(main())
