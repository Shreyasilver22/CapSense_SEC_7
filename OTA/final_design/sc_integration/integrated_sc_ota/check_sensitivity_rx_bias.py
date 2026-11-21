"""Compare baseline corners and test elevated RX precharge as a headroom aid."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from itertools import product
import re

import sweep_sensitivity as s


@dataclass(frozen=True)
class BiasCase(s.Case):
    rx_v:float=0

    @property
    def name(self):
        return super().name+f'_rxpre{self.rx_v:g}V'


make_base = s.make_files


def make_biased(c):
    work,deck=make_base(c)
    if not getattr(c,'rx_v',0):
        return work,deck
    text=deck.read_text()
    text,n1=re.subn(r'(?im)^(XRRESETP\s+rxp\s+)0 ',r'\1rx_reset ',text)
    text,n2=re.subn(r'(?im)^(XRRESETN\s+)0 ',r'\1rx_reset ',text)
    if (n1,n2)!=(1,1):
        raise ValueError('RX clamp instances not identified')
    text=text.replace('.include "',f'VRXBIAS rx_reset 0 {c.rx_v:g}\n.include "',1)
    deck.write_text(text)
    return work,deck


def evaluate(c):
    r=s.run(c)
    r['rx_precharge_V']=getattr(c,'rx_v',0)
    return r


def main():
    s.make_files=make_biased
    tests=[s.Case(10,m,p,corner=c)
           for m,c,p in product((121,84),('cold','hot'),s.CP_ENDS)]
    tests += [BiasCase(20,60,p,corner=c,rx_v=v)
              for c,p,v in [('typ',p,v) for p,v in product((7.82,10.5,11.79),(.5,1))]
                + [(c,p,1) for c,p in product(('cold','hot'),s.CP_ENDS)]]
    with ThreadPoolExecutor(6) as pool:
        rows=list(pool.map(evaluate,tests))
    s.write_csv('rx_bias_and_baseline_points.csv',rows)
    s.summarize([r for r in rows if r['rx_precharge_V']==0],'baseline_84_corner_summary.csv')
    for r in rows:
        if r['status']=='ok' and r['rx_precharge_V']:
            print(r['corner'],r['cp_pF'],'RXV',r['rx_precharge_V'],
                  'diff',round(r['diff_sample_mV'],2),
                  'tail at sample',round(r['tail_sample_mV'],1),
                  'tail minimum',round(r['tail_min_switch_mV'],1),
                  'slack',round(r['settle_slack_us'],2),flush=True)

if __name__=='__main__':
    main()

