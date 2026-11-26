from pathlib import Path
import os,sys,json
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'plotting_deps'));os.environ['MPLCONFIGDIR']=str(R/'mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
rows=json.loads((R/'dense_capacitance_cv.json').read_text());fig,ax=plt.subplots(1,2,figsize=(11,4.5),layout='constrained')
for cf in [40,50,60]:
 a=[r for r in rows if r['target_pF']==cf];zero=next(r['capacitance_pF'] for r in a if abs(r['gate_minus_sum_V'])<1e-12)
 x=[r['gate_minus_sum_V'] for r in a];c=[r['capacitance_pF'] for r in a]
 ax[0].plot(x,c,label=f'{cf} pF label; L={a[0]["L_um"]:g} µm')
 ax[1].plot(x,[v/zero for v in c],label=f'{cf} pF')
for a in ax:
 a.set_xlabel('V(gate) − V(source/drain/well) (V)');a.grid(alpha=.25);a.axvline(0,color='gray',ls=':',lw=1);a.legend(fontsize=8)
ax[0].set_ylabel('Small-signal capacitance (pF)');ax[1].set_ylabel('C / C at zero bias')
fig.suptitle('Five PMOS fingers per feedback capacitor, W = 20 µm each\nTypical SCL model, 27 °C; 100 kHz AC linearization; bias electrode = 2.5 V')
fig.savefig(R/'pmos_capacitance_cv.png',dpi=160);fig.savefig(R/'pmos_capacitance_cv.pdf')
