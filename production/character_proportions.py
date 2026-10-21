"""CPU-only projected-ratio screening. No pixel segmentation or generation."""
import argparse
import json
import math
from pathlib import Path


def chain_length(points):
    """Sum joint-to-joint distances; a bent arm is not its endpoint chord."""
    if len(points)<2:raise ValueError('At least two landmarks required')
    if any(len(p)!=2 or any(not math.isfinite(v) for v in p) for p in points):
        raise ValueError('Landmarks must be finite 2D points')
    return sum(math.dist(a,b) for a,b in zip(points,points[1:]))


def ratio_screen(numerator, denominator, numerator_error, denominator_error,
                 target, tolerance, comparable, reason=''):
    """Conservative interval; tolerance is absolute ratio units, never percent."""
    if not isinstance(comparable,bool):raise ValueError('Comparability must be explicitly true or false')
    numbers=(numerator,denominator,numerator_error,denominator_error,target,tolerance)
    if any(not math.isfinite(v) for v in numbers):raise ValueError('Finite inputs required')
    if min(numerator,numerator_error,denominator_error,target,tolerance)<0 or denominator<=denominator_error:
        raise ValueError('Invalid measurement or denominator uncertainty')
    low=max(0,numerator-numerator_error)/(denominator+denominator_error)
    high=(numerator+numerator_error)/(denominator-denominator_error)
    band=(target-tolerance,target+tolerance)
    status='not_comparable'
    if comparable:
        status=('within_band' if low>=band[0] and high<=band[1] else
                'outside_band' if high<band[0] or low>band[1] else 'uncertain')
    return dict(ratio=numerator/denominator,interval=[low,high],target_band=list(band),
                status=status,reason=reason,approval=False)


def validate_profile(profile):
    errors=[]
    if profile.get('tolerance_units')!='absolute_ratio':errors.append('Tolerance units must be absolute_ratio')
    for key,row in profile.get('ratios',{}).items():
        target=row.get('target');tol=row.get('tolerance')
        if not row.get('definition') or not row.get('comparability'):errors.append(f'{key}: definition/view scope missing')
        if target is None:
            if tol is not None or row.get('calibration_status')!='pending_reference_measurement':
                errors.append(f'{key}: uncalibrated ratio cannot invent tolerance/approval')
        elif (not isinstance(target,(int,float)) or isinstance(target,bool) or not math.isfinite(target)
              or target<=0 or not isinstance(tol,(int,float)) or isinstance(tol,bool)
              or not math.isfinite(tol) or tol<=0):errors.append(f'{key}: invalid target/tolerance')
        elif row.get('calibration_status') not in {'owner_requested_design_target','calibrated_reference'}:
            errors.append(f'{key}: numerical target needs explicit origin/calibration status')
    return errors


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--story',required=True)
    p.add_argument('command',choices=['validate','derive'])
    args=p.parse_args()
    try:from . import character_performance as cp
    except ImportError:import character_performance as cp
    folder,plan,chars,locs,library=cp.load(cp.ROOT,args.story)
    profiles={actor:policy['ratio_profile'] for actor,policy in library.get('anatomy_policies',{}).items() if 'ratio_profile' in policy}
    errors=[f'{actor}: {e}' for actor,profile in profiles.items() for e in validate_profile(profile)]
    if errors:raise SystemExit('\n'.join(errors))
    result={'schema':'feltwillow.proportion-profiles-report.v1','profiles':profiles,
            'automatic_anatomy_approval':False,'source':'character_performance_library.json anatomy_policies.*.ratio_profile'}
    if args.command=='derive':
        (folder/'derived/CHARACTER_PROPORTIONS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'validation':'PASS','actors':list(profiles),'automatic_anatomy_approval':False},indent=2))


if __name__=='__main__':main()
