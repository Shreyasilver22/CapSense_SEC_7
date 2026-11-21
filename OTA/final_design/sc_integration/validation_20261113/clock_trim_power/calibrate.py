"""Use comparator transition traces to update the physical trim-tap positions."""
from pathlib import Path
import argparse
import json

import numpy as np

from build import DEFAULT,EDGES
from check import SETTINGS,measure

TARGETS = (40.85,43.,45.35,65.19,70.09,80.05,90.01)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('work',type=Path)
    p.add_argument('output',type=Path)
    p.add_argument('--previous',type=Path)
    args=p.parse_args()
    previous=DEFAULT if args.previous is None else {int(k):v for k,v in json.loads(args.previous.read_text()).items()}
    profiles=dict(previous)
    for code, setting in SETTINGS.items():
        p=args.work/f'clock{code}'/'trace.dat'
        if not p.is_file():
            continue
        a=np.loadtxt(p,skiprows=1)
        t=a[:,0]*1e6-100
        if t[-1]<102.9:
            continue
        vdd=setting[1]
        r=measure(a,setting,True)
        samples=a[:,8]/vdd
        corrected=[]
        # Convert the previous endpoint settings back to actual internal tap fractions.
        ref=np.array(previous[3])
        hi,lo=previous[code][0],previous[code][-1]
        physical=lo+(ref-ref[-1])*(hi-lo)/(ref[0]-ref[-1])
        for edge,fraction,target in zip(EDGES,physical,TARGETS):
            old=r[f'q{edge}_us']
            if edge==43 and old<r['reset_off_us']:
                old=r['rx_on_us']
            if np.isfinite(old):
                shift=np.interp(target,t,samples)-np.interp(old,t,samples)
                f=fraction+shift
            else:
                offset=(-.001 if edge in (43,46,70) else .004)
                f=np.interp(target,t,samples)+offset
            corrected.append(round(f*2000)/2000)
        if code==3 and np.any(np.diff(corrected)>=0):
            raise ValueError(f'Nonmonotonic calibration taps for code {code}')
        print(code,[round(r[f'q{x}_us'],3) for x in EDGES],corrected)
        profiles[code]=corrected
    args.output.write_text(json.dumps(profiles,indent=2)+'\n')


if __name__=='__main__':
    main()
