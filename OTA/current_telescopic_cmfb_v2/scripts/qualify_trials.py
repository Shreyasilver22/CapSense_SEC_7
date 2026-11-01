import json,concurrent.futures,itertools
import sweep as w,sc_simulate as s
from trial_sc import wrapper
R=w.R
if __name__=='__main__':
 rr=json.loads((R/'finalists.json').read_text());names=['R200_B2_F4_C6_T0.25','R200_B2_F4_C12_T0.5']
 chosen=[next(x for x in rr if x['candidate']==n) for n in names]
 jobs=[]
 for x in chosen:
  (R/'models'/(x['candidate']+'.spice')).write_text(wrapper(w.source(x['pars'],True)))
  for f,sw in itertools.product([100000,200000],['ideal','tg']):jobs.append(dict(arch=x['candidate'],fs=f,switch=sw))
  for b,sw in itertools.product([2.2,2.4],['ideal','tg']):jobs.append(dict(arch=x['candidate'],switch=sw,vdd=4.5,temp=85,mos='wnwp49_5v',vbn=b))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(lambda j:s.run(**j),jobs))
 s.save('SC_trial_qualification',rows)
 jobs=[(x['pars'],dict(vdd=v,temp=t,mos=m,vd=d,vbn=b,cl=10)) for x in chosen for v,t,m,b in itertools.product([4.5,5.5],[0,85],['bnbp49_5v','wnwp49_5v'],[2.2,2.4]) for d in [0,6.6-v,-(6.6-v)]]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:acs=list(ex.map(lambda j:w.ac(j[0],**j[1]),jobs))
 w.save('trial_corner_ac',acs)
 for x in chosen:
  for bn in [2.2,2.4]:
   r=[z for z in acs if z['candidate']==x['candidate'] and z['vbn']==bn and z['status']=='OK'];print(x['candidate'],bn,'minPM',min(z['PM_deg'] for z in r if z['PM_deg'] is not None),'maxCM',max(abs(z['CM_error_mV']) for z in r),flush=True)
