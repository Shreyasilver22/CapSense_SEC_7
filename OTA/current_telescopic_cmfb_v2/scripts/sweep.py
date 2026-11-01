from pathlib import Path
import re,json,subprocess,itertools,concurrent.futures,csv
import numpy as np
R=Path(__file__).resolve().parents[1];PDK=Path('/home/berson_meshak/pdk/scl08/ngspice_models49')
def key(p):return f"R{p['R_kohm']}_B{p['bias_m']}_F{p['follower_m']}_C{p['cap_m']}_T{p.get('controller_scale',1)}"+(f"_H{p['headroom_scale']}" if p.get('headroom_scale',1)!=1 else '')+('_N' if p.get('sense_type')=='nmos' else '')+('_SB' if p.get('body_tied_sensors') else '')
def source(p,estimated=False):
 lines=[]
 for line in (R/'models/original_telescopic.spice').read_text().splitlines():
  a=line.split()
  if not a:continue
  if a[0] in ['MCS','MCR','MCT','MCP1','MCP2'] and p.get('controller_scale',1)!=1:
   w=float(re.search(r'\bW=([\d.]+)u',line,re.I)[1])*p['controller_scale']
   for par,val in [('W',w),('AD',w*4.5),('AS',w*4.5),('PD',2*(w+4.5)),('PS',2*(w+4.5))]:
    line=re.sub(r'\b'+par+r'=[\d.]+[up]',f'{par}={val:.9g}'+('p' if par in ['AD','AS'] else 'u'),line,flags=re.I)
  if a[0] in ['MSP','MSM','MSR','MSIP','MSIM','MSIR','MCM1','MCM2']:
   m=p['follower_m'] if a[0] in ['MSP','MSM','MSR'] else p['bias_m'] if a[0] in ['MSIP','MSIM','MSIR'] else p['cap_m']
   if a[0] in ['MSIP','MSIM','MSIR']:m*=p.get('headroom_scale',1)
   line=re.sub(r'\sM=[\d.]+','',line,flags=re.I)+f' M={m}'
  if a[0]=='MCBI' and p.get('headroom_scale',1)!=1:line+=f" M={p['headroom_scale']}"
  if a[0] in ['MSP','MSM','MSR'] and p.get('body_tied_sensors'):
   toks=line.split();toks[4]=toks[3];line=' '.join(toks)
  if a[0] in ['XSP','XSM']:
   total=p['R_kohm']*1000*2.4/28
   if not estimated:line=re.sub(r'L=[\d.]+u',f'L={total:.9f}u',line)
   else:
    start=a[1];end=a[2];count=20;ln=total/count
    for k in range(count):
     n1=start if k==0 else a[0]+str(k);n2=end if k==count-1 else a[0]+str(k+1);mid=a[0]+'C'+str(k)
     lines += [f'{a[0]}A{k} {n1} {mid} RPP W=2.4u L={ln/2:.9f}u',f'{a[0]}B{k} {mid} {n2} RPP W=2.4u L={ln/2:.9f}u',f'C{a[0]}{k} {mid} 0 {(ln*2.4*.093+2*(ln+2.4)*.048):.8f}f']
    continue
  if line.lower().startswith('.ends') and estimated:
   lines+=['CPAR_sense sense 0 0.1p','CPAR_pc pc 0 0.3p','CPAR_sp sp 0 0.1p','CPAR_sm sm 0 0.1p','CPAR_op op 0 0.5p','CPAR_om om 0 0.5p']
  lines.append(line)
 if p.get('sense_type')=='nmos':
  changed=[]
  def mos(n,d,g,s,b,t,w,l,m=1):return f'{n} {d} {g} {s} {b} {t} W={w:.9g}u L={l}u M={m} AD={w*4.5:.9g}p AS={w*4.5:.9g}p PD={2*(w+4.5):.9g}u PS={2*(w+4.5):.9g}u'
  scale=p.get('controller_scale',.25)
  for line in lines:
   a=line.split();nm=a[0] if a else ''
   if nm in ['MSP','MSM','MSR']:
    gate={'MSP':'op','MSM':'om','MSR':'vcm'}[nm];src={'MSP':'sp','MSM':'sm','MSR':'sr'}[nm];changed.append(mos(nm,'vdd',gate,src,'0','N',20,1.6,p['follower_m']));continue
   if nm in ['MSIP','MSIM','MSIR']:
    src={'MSIP':'sp','MSIM':'sm','MSIR':'sr'}[nm];changed.append(mos(nm,src,'bn','0','0','N',20,3.2,p['bias_m']));continue
   if nm in ['MCS','MCR','MCT','MCP1','MCP2']:continue
   if nm.lower()=='.ends':
    changed += [mos('MCS','ca','sense','ct','vdd','P',10*scale,2.4),mos('MCR','rcm','sr','ct','vdd','P',10*scale,2.4),mos('MCT','ct','cb','vdd','vdd','P',20*scale,3.2)]
    for name,d,g,t in [('MCFN1','ca','ca','N'),('MCFN2','pc','ca','N'),('MCFN3','rcm','rcm','N'),('MCFN4','pbias','rcm','N'),('MCFP1','pbias','pbias','P'),('MCFP2','pc','pbias','P')]:
     changed.append(mos(name,d,g,'0' if t=='N' else 'vdd','0' if t=='N' else 'vdd',t,20*scale,3.2))
   changed.append(line)
  lines=changed
 return '\n'.join(lines)+'\n'

def ac(p,vd=0,mos='tntp49_5v',vdd=5,temp=27,cl=5,kind='cm',model=None,tag=None,vbn=2.4,res='typ'):
 name=tag or key(p);d=R/'results'/name/f'{kind}_{vd}_{mos}_{vdd}_{temp}_{cl}_{vbn}_{res}';d.mkdir(parents=True,exist_ok=True)
 if model is None:
  text=source(p,True).replace('VN nb 0 2.4',f'VN nb 0 {vbn}')
  if kind=='cm':
   text=text.replace('MSP 0 op','MSP 0 sop').replace('MSM 0 om','MSM 0 som').replace('MSP vdd op','MSP vdd sop').replace('MSM vdd om','MSM vdd som')
   text=text.replace('.ends ota_telescopic','LCMP op sop 1e12\nLCMM om som 1e12\nCCMP sop inject 1u\nCCMM som inject 1u\nVINJECT inject 0 dc 0 ac 1\n.ends ota_telescopic')
  (d/'dut.spice').write_text(text);path=d/'dut.spice';sub='ota_telescopic';pins='inp inn op om vdd bn vcm'
 else:
  text=Path(model).read_text();ls=[]
  for line in text.splitlines():
   a=line.split()
   if kind=='cm' and a and a[0].startswith('M') and a[2] in ['OUTP','OUTM'] and re.search(r'\bw=(?:20|40)(?:\.0)?u\s+l=1\.6u',line,re.I):a[2]='SENSE_'+a[2];line=' '.join(a)
   if kind=='cm' and line.lower().startswith('.ends'):ls+=['LCMP OUTP SENSE_OUTP 1e12','LCMM OUTM SENSE_OUTM 1e12','CCMP SENSE_OUTP INJECT 1u','CCMM SENSE_OUTM INJECT 1u','VINJECT INJECT VSS dc 0 ac 1']
   ls.append(line)
  path=d/'dut.spice';path.write_text('\n'.join(ls)+'\n');sub='ota_telescopic_layout';pins='inp inn op om vdd 0 bn vcm vbn vbp'
 b=f'''CMFB revision {name}
.include "{PDK}/mos/{mos}"
.include "{PDK}/res/{res}/ppr"
.include "{path}"
.temp {temp}
.options reltol=1e-5 vntol=1e-8 abstol=1e-12
VDD vdd 0 {vdd}
IREF vdd bn 3.5u
VCM vcm 0 {vdd/2}
VBN vbn 0 {vbn}
VBP vbp vdd -2.2
XOTA {pins} {sub}
CLP op 0 {cl}p
CLM om 0 {cl}p
'''
 if model is None:b+='MREF bn bn 0 0 N W=20u L=3.2u AD=90p AS=90p PD=49u PS=49u\n'
 if kind=='cm':b+=f'VIP inp 0 1.5\nEFB inn 0 value={{1.5+v(op)-v(om)-({vd})}}\n';expr='-(v(op)+v(om))/2'
 else:b+=f'VCMD cmd 0 dc {vd} ac 1\nEIP inp 0 value={{1.5+(v(cmd)-v(fb))/2}}\nEIM inn 0 value={{1.5-(v(cmd)-v(fb))/2}}\nEOD od 0 op om 1\nLDC od fb 1e12\nCAC fb 0 1e12\n';expr='v(od)'
 b+=f'''.control
set wr_singlescale
set wr_vecnames
op
print v(op) v(om) i(vdd)
ac dec 80 {100 if kind=='cm' else .01} 1G
let gr=real({expr})
let gi=imag({expr})
wrdata ac.dat gr gi
quit
.endc
.end
'''
 (d/'tb.cir').write_text(b);rec=dict(candidate=name,pars=p,kind=kind,vd=vd,mos=mos,VDD=vdd,temp=temp,CL_pF=cl,vbn=vbn,res=res,status='FAILED')
 try:
  proc=subprocess.run(['ngspice','-b','-o','sim.log','tb.cir'],cwd=d,capture_output=True,timeout=90);a=np.loadtxt(d/'ac.dat',skiprows=1);assert proc.returncode==0
  h=a[:,1]+1j*a[:,2];g=20*np.log10(abs(h));ph=np.unwrap(np.angle(h))*180/np.pi;cross=[]
  for i in np.where(g[:-1]*g[1:]<0)[0]:
   f=-g[i]/(g[i+1]-g[i]);cross.append(dict(f_MHz=float(10**(np.log10(a[i,0])+f*np.log10(a[i+1,0]/a[i,0]))/1e6),PM_deg=float(180+ph[i]+f*(ph[i+1]-ph[i]))))
  log=(d/'sim.log').read_text();op={k:float(v) for k,v in re.findall(r'^(v\(op\)|v\(om\)|i\(vdd\))\s*=\s*([-+\d.eE]+)',log,re.M)}
  rec.update(status='OK',gain_dB=float(g[0]),PM_deg=min((x['PM_deg'] for x in cross),default=None),crossings=cross,power_uW=-vdd*op['i(vdd)']*1e6,CM_error_mV=((op['v(op)']+op['v(om)'])/2-vdd/2)*1000,op_V=op['v(op)'],om_V=op['v(om)'])
 except Exception as e:rec['error']=str(e)
 return rec
def save(name,r):
 (R/(name+'.json')).write_text(json.dumps(r,indent=2))
 with (R/(name+'.csv')).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in r for k in x)));w.writeheader();w.writerows(r)
if __name__=='__main__':
 pars=[dict(R_kohm=r,bias_m=b,follower_m=b*ratio,cap_m=c,controller_scale=t) for r,b,ratio,c,t in itertools.product([100,150,200],[2,3,4],[2,4],[6,8,12,16],[.25,.5,1])]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(lambda p:ac(p),pars))
 save('screen_center',rows);print('Center cases',len(rows),flush=True)
 good=[x for x in rows if x['status']=='OK' and x['PM_deg'] is not None and x['PM_deg']>=65]
 jobs=[(x['pars'],vd) for x in good for vd in [-1.8,1.8]]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:ends=list(ex.map(lambda j:ac(j[0],vd=j[1]),jobs))
 save('screen_signal_range',ends);print('Range cases',len(ends),flush=True)
 finalists=[]
 for x in good:
  rr=[y for y in ends if y['candidate']==x['candidate']]
  if len(rr)==2 and all(y['status']=='OK' and y.get('PM_deg',-999) is not None and y['PM_deg']>=60 and abs(y['CM_error_mV'])<20 for y in rr):finalists.append(dict(**x,worst_PM=min(y['PM_deg'] for y in [x]+rr),worst_CM_error_mV=max(abs(y['CM_error_mV']) for y in [x]+rr)))
 finalists.sort(key=lambda x:(x['power_uW'],x['pars']['cap_m'],x['worst_CM_error_mV']))
 save('finalists',finalists);print('Finalists',len(finalists),flush=True)
 for x in finalists[:12]:print(x['candidate'],x['power_uW'],x['worst_PM'],x['worst_CM_error_mV'],flush=True)
