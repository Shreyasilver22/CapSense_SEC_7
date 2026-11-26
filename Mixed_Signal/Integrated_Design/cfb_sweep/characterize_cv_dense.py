from pathlib import Path
import subprocess,re,json
R=Path(__file__).resolve().parent
sizes=json.loads((R/'specified_sizes.json').read_text());model='/home/shreyas/open_source_scl_cp8d/open_pdks/scl_cp8d/libs.tech/ngpsice/model/hspice/models49/mos/tntp49_5v';rows=[]
for item in sizes:
 cf=item['target_pF'];s=f'''Five-finger PMOS C-V
.include {model}
VB b 0 2.5
VG g 0 DC 0 AC 1
MC b g b b P W=20u L={item['L_um']}u M=5 AD=90p AS=90p PD=49u PS=49u
.options klu
.control
set numdgt=12
'''
 for k in range(201):
  gate=k*.025
  s+=f'alter VG={gate:.12g}\nac lin 1 100k 100k\nlet c=-imag(i(VG))/(2*pi*100k)\necho CV_POINT {gate-2.5:.12g} $&c\n'
 s+='quit\n.endc\n.end\n';p=R/f'dense_cv_{cf}.cir';p.write_text(s)
 with (R/f'dense_cv_{cf}_console.log').open('w') as f:subprocess.run(['nice','-n','10','ngspice','-b','-o',f'dense_cv_{cf}.log',p.name],cwd=R,stdout=f,stderr=f,check=True)
 for bias,c in re.findall(r'^CV_POINT\s+([\deE.+-]+)\s+([\deE.+-]+)',(R/f'dense_cv_{cf}.log').read_text(),re.M):rows.append({**item,'gate_minus_sum_V':float(bias),'capacitance_pF':float(c)*1e12})
(R/'dense_capacitance_cv.json').write_text(json.dumps(rows,indent=2));print('C-V points:',len(rows));assert len(rows)==603
