#!/usr/bin/env python3
"""Stable global-clock oscillator. Math helper, NOT a Blender animation system."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from fractions import Fraction

def frame_time(frame: int, fps_num: int, fps_den: int=1) -> Fraction:
    if any(type(x) is not int for x in (frame,fps_num,fps_den)) or frame < 0 or fps_num <= 0 or fps_den <= 0:
        raise ValueError('Use a nonnegative global frame and positive rational FPS')
    return Fraction(frame*fps_den,fps_num)

def stable_phase(asset_id: str, seed: int=0) -> float:
    if not isinstance(asset_id,str) or not asset_id or type(seed) is not int:
        raise ValueError('Stable semantic asset ID and integer seed required')
    raw=json.dumps([asset_id,seed],ensure_ascii=False,separators=(',',':')).encode()
    return int.from_bytes(hashlib.sha256(raw).digest()[:8],'big')/(2**64)*math.tau

def displacement(asset_id: str, seconds: float, period: float, amplitude: float, seed: int=0) -> float:
    if any(isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) for x in (seconds,period,amplitude)):
        raise ValueError('All numerical inputs must be finite')
    if period <= 0 or amplitude < 0:
        raise ValueError('Period must be positive and amplitude nonnegative')
    return amplitude*math.sin(math.tau*((seconds%period)/period)+stable_phase(asset_id,seed))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--id',required=True);p.add_argument('--frame',type=int,required=True)
    p.add_argument('--fps-num',type=int,default=24);p.add_argument('--fps-den',type=int,default=1)
    p.add_argument('--period',type=float,required=True);p.add_argument('--amplitude',type=float,required=True)
    p.add_argument('--seed',type=int,default=0)
    a=p.parse_args()
    try:
        t=frame_time(a.frame,a.fps_num,a.fps_den)
        v=displacement(a.id,float(t),a.period,a.amplitude,a.seed)
        print(json.dumps({'time_rational':str(t),'value':v,'units':'same as supplied amplitude','visual_calibration':'required'}))
    except ValueError as e:
        p.error(str(e))
if __name__=='__main__':
    main()
