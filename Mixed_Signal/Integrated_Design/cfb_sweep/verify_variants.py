from pathlib import Path
import subprocess,re,json,hashlib
R=Path(__file__).resolve().parent;P=R.parent;reports=[]
for cf,length in [(40,202.7),(50,253.375),(60,304.05)]:
 src=P/f'schematic/capsense_cfb_{cf}pf.sch';dest=P/'simulation/cap_controls_check'/f'capsense_cfb_{cf}pf.spice'
 p=subprocess.run(['xschem-800nm','-x','-q','--tcl','set USER_CONF_DIR /tmp','-s','-n','-o',str(dest.parent),'-N',dest.name,str(src)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=True)
 assert 'Symbol not found' not in p.stdout and 'Unmatched' not in p.stdout
 text=dest.read_text();assert f'CFB_L={length:g}u' in text
 assert len(re.findall(r'^X\w+ .* Transmission_v1_26_[hv]$',text,re.M))==12
 assert len(re.findall(r'^MCF[PN] ',text,re.M))==2
 assert 'CSP txp rxp {CS}' in text and 'CSN txn rxn {CS}' in text
 assert 'W={CFB_W} L={CFB_L} M={CFB_M}' in text
 assert 'CMEMP 0 sensp {CP}' in text and 'CMEMN 0 sensn {CN}' in text
 reports.append({'cfb_label_pF':cf,'L_um':length,'W_um':20,'parallel_fingers':5,'netlist':str(dest),'status':'pass'})
(P/'simulation/cap_controls_check/schematic_variants_verified.json').write_text(json.dumps(reports,indent=2));print('PASS: all three Xschem variants, twelve hierarchical TGs each, two direct PMOS feedback devices with editable dimensions and CS.')
