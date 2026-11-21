"""Check series resistance on the RX transfer path under the same 10 kHz clocks."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import product
import re

import sweep_sensitivity as s


@dataclass(frozen=True)
class SlewCase(s.Case):
    rx_kohm:int=15

    @property
    def name(self):
        return super().name+f'_rxr{self.rx_kohm}k'


make_base = s.make_files


def make_slew(c):
    work,deck = make_base(c)
    net=deck.read_text()
    for suffix,branch in (('P','p'),('N','n')):
        pattern=rf'(?im)^XXFER{suffix} rx{branch} '
        net,count=re.subn(pattern,f'XXFER{suffix} rxlimited{branch} ',net)
        if count!=1:
            raise ValueError('RX transfer instance not identified')
    length=2.4*c.rx_kohm*1000/28
    res='\n'.join(f'XRXLIM{side} rx{side} rxlimited{side} RPP W=2.4u L={length:.8g}u' for side in 'pn')
    net=net.replace('.include "',res+'\n.include "',1)
    deck.write_text(net)
    return work,deck


def evaluate(c):
    r=s.run(c)
    r['rx_series_nom_kohm']=c.rx_kohm
    return r


def main():
    s.make_files=make_slew
    tests=[SlewCase(20,60,p,corner=c,rx_kohm=r)
           for c,p,r in [('typ',p,r) for p,r in product((7.82,10.5,11.79),(15,30))]
            + [(c,p,15) for c,p in product(('cold','hot'),(7.82,11.79))]
            + [('typ',p,15) for p in (7.32,14.50)]]
    with ThreadPoolExecutor(4) as pool:
        rows=list(pool.map(evaluate,tests))
    s.write_csv('rx_slew_points.csv',rows)
    for r in rows:
        if r['status']=='ok':
            print(r['corner'],r['cp_pF'],r['rx_series_nom_kohm'],
                  'diff',round(r['diff_sample_mV'],3),
                  'tail',round(r['tail_min_switch_mV'],1),
                  'slack',round(r['settle_slack_us'],2),flush=True)

if __name__=='__main__':
    main()

