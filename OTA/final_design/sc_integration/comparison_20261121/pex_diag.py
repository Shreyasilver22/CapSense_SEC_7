"""Determine whether explicit layout capacitance explains the boosted OTA behavior."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re

from compare import Case, ROOT, run, save

def main():
    net = (ROOT/'models/boosted_C.spice').read_text().splitlines()
    middle = {l.split()[2] for l in net if re.match(r'^XR\d+A ',l)}
    for mode in ('zero','quarter','no_poly_ground'):
        out = []
        for line in net:
            if re.match(r'^C\d+\s',line):
                _,a,b,val = line.split()[:4]
                if mode == 'zero':
                    continue
                if mode == 'no_poly_ground' and (a in ('VSS','0') and b in middle or b in ('VSS','0') and a in middle):
                    continue
                if mode == 'quarter':
                    m = re.fullmatch(r'([\d.eE+-]+)([a-zA-Z]*)',val)
                    line = line.replace(val,f'{float(m[1])/4:.12g}{m[2]}')
            out.append(line)
        (ROOT/f'models/boosted_C_{mode}.spice').write_text('\n'.join(out)+'\n')
    cases = [Case(f'boosted_C_{mode}','typ',100) for mode in ('zero','quarter','no_poly_ground')]
    cases += [Case('boosted_C','typ',100,cycles=4), Case('boosted_C','typ',100,step=30,solver='gear')]
    with ThreadPoolExecutor(4) as pool:
        rows = list(pool.map(run,cases))
    save(ROOT/'pex_diagnostics.csv',rows)

if __name__ == '__main__':
    main()

