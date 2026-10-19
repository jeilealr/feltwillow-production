#!/usr/bin/env python3
"""V7 composition uses reviewed anatomical calibration and one master transform.

Original PNG primitives and executed method are preserved in the migration
snapshot. Legacy bbox normalization is deliberately unavailable for new pairs.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from production.paired_images import compose_master, calibrated_transform
from production.paired_composition import compose_recipe


def composite(*args, **kwargs):
    raise ValueError('Uncalibrated pose-box composition retired. Use production/keyframe.py --paired-recipe RECIPE.json --out NEW.png')


if __name__ == '__main__':
    raise SystemExit('Use production/keyframe.py --paired-recipe RECIPE.json --out NEW.png; see docs/paired-image-workflow.md')
