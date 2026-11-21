"""Make ngspice decks for the transistor-level clock and reference buffer."""
from pathlib import Path
import argparse
import re

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parent / 'vcm_pvt_20261115/netlists/combined_bnwp_5.5_85_12_50.cir'
PDK = Path.home() / 'pdk/scl08/ngspice_models49'
VECTORS = (
    'v(clk10k) v(phi1) v(phit) v(phi2) v(phi2b) v(pr) v(tr) v(vref_sw) v(vref) '
    'v(outp) v(outn) v(sump) v(sumn) v(holdp) v(holdn) v(txp) v(rxp) '
    'i(VBUFDD) i(VCLKDD) i(VDD) i(VDRIVE)'
)

def make_deck(*, supply, temp, model, resistor, cp, cn, physical_clock, physical_reference,
              phase_params='', bypass_units=0):
    body = FIXTURE.read_text().split('.save')[0]
    body = re.sub(r'(?m)^\.include .*?mos/.*$',f'.include "{PDK}/mos/{model}49_5v"',body)
    body = re.sub(r'(?m)^\.include .*?res/.*$',f'.include "{PDK}/res/{resistor}/ppr"',body)
    body = body.replace('VDD vdd 0 5.5',f'VDD vdd 0 {supply}')
    body = body.replace('VCLK clk10k 0 PULSE(0 5.5 ',f'VCLK clk10k 0 PULSE(0 {supply} ')
    body = body.replace('.temp 85',f'.temp {temp}')
    body = body.replace('.param CP=12p CN=12p',f'.param CP={cp}p CN={cn}p')
    body = body.replace('reltol=1e-5','reltol=1e-4')
    if physical_clock:
        body = re.sub(r'(?ms)^ENORM .*?^\.ends phases_10k\n','',
                      body[body.index('\n')+1:])
        body = re.sub(r'(?m)^(B1|B2|BT|BTR|BPR|VSTART|BSTART) .*\n','',body)
        body = re.sub(r'(?m)^(MN_drive_[pn] vdd) phi1 ',r'\1 chg ',body)
        body = re.sub(r'(?m)^(MP_drive_[pn] vdd) phi1b ',r'\1 chgb ',body)
        body += ('XCLK clk10k clk_vdd 0 phi1 phi1b phit phitb phi2 phi2b '
                 f'pr prb tr trb chg chgb phase08 {phase_params}\n')
        body = 'SCL08 physical clock and SC reference integration\n' + body
    else:
        body = re.sub(r'(?m)^ENORM (.*) [^ ]+$',r'ENORM \1 '+str(5/supply),body)
        body = re.sub(r'(?m)^(ESC\w+ .*) [^ ]+$',r'\1 '+str(supply/5),body)
        body = body.replace('VSTART start_reset 0 PWL(0 5.5 1u 5.5 2u 0)',
                            f'VSTART start_reset 0 PWL(0 {supply} 1u {supply} 2u 0)')
    body += '\n.include blocks.spice\nVCLKDD vdd clk_vdd 0\nVBUFDD vdd buf_vdd 0\n'
    if physical_reference:
        body = body.replace('RREF ref_src vref_sw 50','XREF ref_src vref_driven buf_vdd 0 refbuf08')
        body = body.replace('VREFSENSE vref_sw vref 0','VREFSENSE ref_src vref 0')
    else:
        body = body.replace('RREF ref_src vref_sw 50','RREF ref_src vref_driven 50')
    body += 'VDRIVE vref_driven vref_sw 0\n'
    if bypass_units:
        body += f'MREFBYPASS vdd vref_sw vdd vdd P W=20u L=10u M={bypass_units}\n'
    return f"""{body}
.control
set wr_singlescale
set wr_vecnames
set numdgt=10
tran 50n 300u 0 50n
wrdata trace.dat {VECTORS}
quit
.endc
.end
"""

def main():
    p=argparse.ArgumentParser()
    p.add_argument('output',type=Path)
    p.add_argument('--supply',type=float,default=5)
    p.add_argument('--temp',type=int,default=27)
    p.add_argument('--model',default='tntp')
    p.add_argument('--resistor',default='typ')
    p.add_argument('--cp',type=int,default=12)
    p.add_argument('--cn',type=int,default=7)
    p.add_argument('--physical-clock',action='store_true')
    p.add_argument('--physical-reference',action='store_true')
    p.add_argument('--phase-params',default='')
    p.add_argument('--bypass-units',type=int,default=0)
    args=vars(p.parse_args())
    output=args.pop('output')
    output.write_text(make_deck(**args))

if __name__=='__main__':
    main()
