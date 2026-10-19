#!/usr/bin/env python3
"""V7 immutable paired-candidate registration entry point.

Usage: --story lion_and_mouse_v7 register ENDPOINT r001 IMAGE PROVENANCE.json
The pre-paired whole-group/bbox registration implementation is preserved in
history/pre_paired_2026-10-19/register_generated.py. It must not author new pairs.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from production.paired_images import main

if __name__ == '__main__':
    raise SystemExit(main())
