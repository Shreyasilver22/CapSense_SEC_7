import json,concurrent.futures
import sweep as w, sc_simulate as s
R=w.R
def wrapper(src):
 ren={'ip':'INP','im':'INN','op':'OUTP','om':'OUTM','vdd':'VDD','0':'VSS','bn':'IREF','vcm':'VCM','nb':'VBN','pb':'VBP'}
 out=['.subckt ota_telescopic_layout INP INN OUTP OUTM VDD VSS IREF VCM VBN VBP']
 for line in src.splitlines():
  a=line.split()
  if not a or not a[0].startswith(('M','X','C')):continue
  n=4 if a[0].startswith('M') else 2;a[1:n+1]=[ren.get(x,x.upper()) for x in a[1:n+1]];out.append(' '.join(a))
 out+=['MREF IREF IREF VSS VSS N W=20u L=3.2u AD=90p AS=90p PD=49u PS=49u','.ends ota_telescopic_layout'];return '\n'.join(out)+'\n'
if __name__=='__main__':
 rr=json.loads((R/'finalists.json').read_text());chosen=[rr[0],rr[1]]
 for r in [100,150]:
  z=[x for x in rr if x['pars']['R_kohm']==r and x['pars']['follower_m']==2*x['pars']['bias_m']]
  if z:chosen.append(z[0])
 chosen += [next(x for x in rr if x['pars'].get('controller_scale')==.5)]
 chosen=list({x['candidate']:x for x in chosen}.values());(R/'SC_trial_candidates.json').write_text(json.dumps(chosen,indent=2))
 for x in chosen:(R/'models'/(x['candidate']+'.spice')).write_text(wrapper(w.source(x['pars'],True)))
 jobs=[dict(arch=x['candidate'],switch='ideal') for x in chosen]
 jobs += [dict(arch=chosen[0]['candidate'],switch='tg')]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda j:s.run(**j),jobs))
 s.save('SC_trials',rows)
