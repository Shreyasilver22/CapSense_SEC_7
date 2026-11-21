"""Build a SCL08 resistor-string trim and power-reduced clock/reference candidate."""
from pathlib import Path
import argparse
import json
import re

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent/'clock_reference_scl08/blocks.spice'
EDGES = (41, 43, 46, 65, 70, 80, 90)
DEFAULT = {
    0: (.459,.447,.4356,.3606,.3384,.3022,.2644), # cold
    1: (.498,.487,.477,.406,.386,.358,.330),     # wnbp
    2: (.508,.497,.487,.415,.394,.361,.325),     # wnwp
    3: (.5244,.5127,.503,.4254,.403,.367,.329),  # typical
    4: (.540,.528,.518,.437,.415,.375,.335),     # fast nominal
    5: (.5878,.5725,.561,.4805,.4548,.4169,.3762), # hot
    6: (.547,.535,.524,.441,.419,.379,.338),     # bnwp nominal
    7: (.5244,.5127,.503,.4254,.403,.367,.329),  # spare nominal
}


def trim_string(profiles):
    reference=profiles[3]
    span=4900
    ladder=[]
    for hi,lo,top,bottom in zip(EDGES,EDGES[1:],reference,reference[1:]):
        length = span*(top-bottom)/(reference[0]-reference[-1])
        ladder.append(f'XL{hi} v{hi} v{lo} RPP W=2.4u L={length:.3f}u')
    bits=('d0','d1','d2')
    for bit in bits:
        ladder.append(f'XINV_{bit} {bit} {bit}b vdd vss inv08')
    for code in range(8):
        a,b,c=[bit if code & (1<<i) else bit+'b' for i,bit in enumerate(bits)]
        ladder += [f'XDECA{code} {a} {b} decab{code} vdd vss nand08',
                   f'XDECB{code} decab{code} deca{code} vdd vss inv08',
                   f'XDECC{code} deca{code} {c} selb{code} vdd vss nand08',
                   f'XDECD{code} selb{code} sel{code} vdd vss inv08']
        high,low=profiles[code][0],profiles[code][-1]
        total=span/(high-low)
        ladder += [
            f'XLOW{code} v90 low{code} RPP W=2.4u L={low*total:.3f}u',
            f'XHIGH{code} v41 high{code} RPP W=2.4u L={(1-high)*total:.3f}u',
            f'MLOW{code} low{code} sel{code} vss vss N W=60u L=.8u',
            f'MHIGH{code} high{code} selb{code} vdd vdd P W=100u L=.8u',
        ]
    return '\n'.join(ladder)+'\n'


def make_blocks(profiles, quiet_clock=True, lean_ref=True):
    s=SOURCE.read_text()
    s=s.replace('.subckt phase08 clk vdd vss','.subckt phase_trim08 clk d0 d1 d2 vdd vss')
    s=s.replace('.ends phase08','.ends phase_trim08')
    s=re.sub(r'(?m)^\+ f41=.*$', '+ lramp=2.2u lslew=16u lfall=14.5u ldead=50000u',s)
    s=re.sub(r'(?ms)^XL0 vss.*?(?=^XC41)',trim_string(profiles),s)
    s=s.replace('XRXG q43 n41 rx_guard_b vdd vss nand08', '''* Interlock RX with a delayed copy of the physical reset release.
XRXGDEAD s1b rx_delay RPP W=2.4u L=65000u
MRXGN rx_delay vss vss vss N W=100u L=20u
MRXGP rx_delay vdd vdd vdd P W=100u L=20u
XRXGI rx_delay reset_safe_b vdd vss inv08
XRXGB reset_safe_b reset_safe vdd vss inv08
XRXG q43 reset_safe rx_guard_b vdd vss nand08''')
    if quiet_clock:
        s=s.replace('XB1 raw yn vdd vss inv08', '''* Long-channel inverter limits crossover current when raw lingers at midrail.
MNBUF yn raw vss vss N W=5u L=12u
MPBUF yn raw vdd vdd P W=10u L=12u''')
        s=s.replace('XB2 yn y vdd vss inv08 w=12u','XB2 yn y vdd vss inv08 w=3u')
    s=s.replace('.subckt refbuf08 ref out vdd vss','.subckt refbuf08 ref out boost vdd vss')
    if lean_ref:
        s=s.replace('MT tail nb vss vss N W=60u','MT tail nb vss vss N W=24u')
        s=s.replace('MN out nb vss vss N W=180u L=2.4u', '''MN out nb vss vss N W=72u L=2.4u
* Enable extra sink current in the upper trim codes, including the hot code.
XBOOST boost boost_b vdd vss inv08
MBSWN nb_extra boost nb vss N W=5u L=.8u
MBSWP nb_extra boost_b nb vdd P W=10u L=.8u
MBOFF nb_extra boost_b vss vss N W=5u L=.8u
MBEXTRA out nb_extra vss vss N W=64u L=2.4u''')
    return s


def main():
    p=argparse.ArgumentParser()
    p.add_argument('output', type=Path)
    p.add_argument('--profiles',type=Path)
    p.add_argument('--legacy-clock',action='store_true')
    p.add_argument('--legacy-reference',action='store_true')
    a=p.parse_args()
    profiles=DEFAULT if not a.profiles else {int(k):v for k,v in json.loads(a.profiles.read_text()).items()}
    a.output.write_text(make_blocks(profiles, not a.legacy_clock, not a.legacy_reference))

if __name__=='__main__':
    main()
