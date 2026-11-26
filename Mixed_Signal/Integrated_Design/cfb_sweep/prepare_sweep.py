from pathlib import Path
import shutil,re,json,subprocess
R=Path(__file__).resolve().parent;P=R.parent
sizes=[{'target_pF':c,'W_um':20,'L_um':202.7*c/40,'fingers':5,'gate_area_um2':20*202.7*c/40*5} for c in [40,50,60]]
(R/'specified_sizes.json').write_text(json.dumps(sizes,indent=2))
backup=R/'before_parameterization';backup.mkdir(exist_ok=True)
for p in [P/'simulation/analog_support.spice',P/'symbols/pmos_cfb.sym',P/'schematic/capsense_integrated_tb.sch']:
 q=backup/p.name
 if not q.exists():shutil.copy2(p,q)
p=P/'simulation/analog_support.spice';s=p.read_text();s=re.sub(r'MFB SUM OUT SUM SUM P .*', 'MFB SUM OUT SUM SUM P W=20u L={CFB_L} M=5 AD=90p AS=90p PD=49u PS=49u',s);p.write_text(s)
p=P/'symbols/pmos_cfb.sym';s=p.read_text();
if 'T {5 x 20u / CFB_L}' not in s:s+='T {5 x 20u / CFB_L} -40 24 0 0 0.16 0.16 {}\n'
p.write_text(s)
p=P/'schematic/capsense_integrated_tb.sch';s=p.read_text();s=s.replace('name=CMEMP value=11.79p','name=CMEMP value=\\{CP\\}').replace('name=CMEMN value=10p','name=CMEMN value=\\{CN\\}')
if 'name=CAP_VALUES' not in s:s+='C {/usr/share/xschem/xschem_library/devices/code_shown.sym} 1450 1600 0 0 {name=CAP_VALUES only_toplevel=false value=".param CP=11.79p CN=10p CFB_L=202.7u SIM_STOP=795u"}\n'
p.write_text(s)
for row in sizes:
 name=f'capsense_cfb_{row["target_pF"]}pf.sch';v=s.replace('CFB_L=202.7u',f'CFB_L={row["L_um"]:.9g}u').replace('SIM_STOP=795u',f'SIM_STOP={795 if row["target_pF"]==40 else 1595}u');(P/'schematic'/name).write_text(v)
# Independently measure the specified dimensions at several biases.
model='/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/mos/tntp49_5v'
cv=[]
for row in sizes:
 for bias in [-2,-1,-.5,0,.5,1,2]:
  deck=f'''Specified 5-finger PMOS capacitor characterization
.include {model}
VB b 0 2.5
VG g 0 DC {2.5+bias} AC 1
MC b g b b P W=20u L={row['L_um']}u M=5 AD=90p AS=90p PD=49u PS=49u
.options klu
.control
ac lin 1 100k 100k
let capacitance=-imag(i(VG))/(2*pi*100k)
print capacitance
quit
.endc
.end
''';tag=f'cv_{row["target_pF"]}_{bias}'.replace('.','p');(R/(tag+'.cir')).write_text(deck)
  subprocess.run(['ngspice','-b','-o',tag+'.log',tag+'.cir'],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
  log=(R/(tag+'.log')).read_text();c=float(re.search(r'capacitance\s*=\s*([\deE.+-]+)',log)[1]);cv.append({**row,'gate_minus_sum_V':bias,'capacitance_pF':c*1e12})
(R/'specified_cap_cv.json').write_text(json.dumps(cv,indent=2));print([x for x in cv if x['gate_minus_sum_V']==0])
