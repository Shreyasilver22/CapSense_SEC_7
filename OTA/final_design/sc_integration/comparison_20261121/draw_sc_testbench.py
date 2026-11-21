"""Draw the SCL08 SCB10H integration circuit used in the RX/TX-slew test."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

OUT = Path(__file__).resolve().parent
fig = plt.figure(figsize=(16.4,8.2), facecolor='white')
ax = fig.add_axes([.044,.105,.917,.75], xlim=(0,22.25), ylim=(.05,10.71), aspect='equal')
ax.axis('off')
ink='#1c2d3c'
blue='#136876'
muted='#506171'
light='#d7e1e7'

def line(*points, color=ink, width=1.65):
    x,y=zip(*points)
    ax.plot(x,y,color=color,lw=width,solid_capstyle='round',zorder=2)

def text(x,y,s,*,size=11,ha='center',va='center',color=ink,weight='normal'):
    ax.text(x,y,s,fontsize=size,ha=ha,va=va,color=color,fontweight=weight,zorder=4)

def dot(x,y,filled=True):
    ax.add_patch(Circle((x,y),.052,ec=ink,fc=ink if filled else 'white',lw=1.15,zorder=5))

def transform(x,y,u,v,axis,sign):
    return (x+u,y+v) if axis=='h' else (x-v,y+sign*u)

def switch(x,y,*,axis='h',sign=1):
    p=lambda a,b:transform(x,y,a,b,axis,sign)
    line(p(-.50,0),p(-.27,0))
    line(p(.26,0),p(.50,0))
    line(p(-.23,.025),p(.14,.265))
    dot(*p(-.27,0),False)
    dot(*p(.26,0),False)

def capacitor(x,y,*,axis='h',sign=1,color=ink,width=.28):
    p=lambda a,b:transform(x,y,a,b,axis,sign)
    line(p(-.50,0),p(-.12,0),color=color)
    line(p(.12,0),p(.50,0),color=color)
    line(p(-.12,-width),p(-.12,width),color=color)
    line(p(.12,-width),p(.12,width),color=color)

def resistor(x,y,*,axis='h',sign=1,color=ink):
    p=lambda a,b:transform(x,y,a,b,axis,sign)
    line(p(-.61,0),p(-.40,0),p(-.33,.13),p(-.22,-.13),p(-.11,.13),
         p(0,-.13),p(.11,.13),p(.22,-.13),p(.33,.13),p(.40,0),p(.61,0),color=color)

def ground(x,y,sign):
    p=lambda a,b:(x+b,y+a*sign)
    line(p(0,0),p(.16,0))
    for a,b in ((.16,.205),(.26,.137),(.36,.069)):
        line(p(a,-b),p(a,b),width=1.3)

def rail(x,y):
    line((x-.22,y),(x+.22,y),width=1.5)

def circuit_branch(y,d,s):
    idx=s.upper()
    tx,rx,su,ou,ho=2.55,5.95,8.50,13.67,17.48
    text(.30,y+.43,r'$+5\ \mathrm{V}$',size=11)
    dot(.30,y,False)
    line((.30,y),(.86,y))
    switch(1.36,y)
    text(1.36,y+.62,r'$\phi_{\mathrm{CHG}}$',size=10,color=muted)
    line((1.86,y),(3.81,y))
    dot(tx,y)
    text(tx,y-.37*d,r'$\mathrm{TX}_{'+s+'}$',size=11)
    switch(tx,y+.72*d,axis='v',sign=d)
    line((tx,y),(tx,y+.22*d))
    line((tx,y+1.22*d),(tx,y+1.39*d))
    text(tx-.30,y+.76*d,r'$\phi_{\mathrm{DIS}}$',size=10,ha='right',color=muted)
    resistor(tx,y+2*d,axis='v',sign=d,color=blue)
    text(tx+.31,y+2*d,r'$15\ \mathrm{k\Omega}$',ha='left',color=blue,size=11,weight='bold')
    ground(tx,y+2.61*d,d)
    capacitor(4.31,y,color=blue)
    cap_label=r'$C_P$' if s=='p' else r'$C_N=10\ \mathrm{pF}$'
    text(4.31,y+.61,cap_label,size=12,color=blue,weight='bold')
    text(4.31,y-.57,'SCB10H sensor' if s=='p' else 'Reference capacitor',size=10,color=muted)
    line((4.81,y),(6.58,y))
    dot(rx,y)
    text(rx,y-.38*d,r'$\mathrm{RX}_{'+s+'}$',size=11)
    line((rx,y),(rx,y+.56*d))
    switch(rx,y+1.06*d,axis='v',sign=d)
    line((rx,y+1.56*d),(rx,y+1.96*d))
    rail(rx,y+1.96*d)
    text(rx,y+2.27*d,r'$V_{\mathrm{PRE}}$',size=11)
    text(rx+.30,y+1.13*d,r'$\phi_{\mathrm{RST}}$',size=10,ha='left',color=muted)
    switch(7.08,y)
    text(7.08,y+.54,r'$\phi_{\mathrm{XFER}}$',size=10,color=muted)
    line((7.58,y),(9.28,y))
    dot(su,y)
    text(su-.10,y-.40*d,r'$\mathrm{SUM}_{'+s+'}$',size=11)
    line((12.92,y),(14.83,y))
    dot(ou,y)
    text(ou+.30,y-.42*d,r'$V_{\mathrm{O'+idx+'}}$',size=11,ha='left')
    wire_y=y+1.43*d
    reset_y=y+2.27*d
    line((su,y),(su,reset_y),(10.54,reset_y))
    line((ou,y),(ou,reset_y),(11.54,reset_y))
    dot(su,wire_y)
    dot(ou,wire_y)
    line((su,wire_y),(10.54,wire_y))
    capacitor(11.04,wire_y,color=blue,width=.205)
    line((11.54,wire_y),(ou,wire_y))
    text(11.04,wire_y-.37*d,r'$C_{\mathrm{F'+idx+'}}$'+'  PMOS bank',size=10.4,color=blue)
    switch(11.04,reset_y)
    text(11.04,reset_y+.50*d,r'$\phi_{\mathrm{RST}}$',size=10,color=muted)
    line((ou,y),(ou,y-.21*d))
    capacitor(ou,y-.71*d,axis='v',sign=-d,width=.23)
    ground(ou,y-1.21*d,-d)
    text(ou+.33,y-.91*d,r'$5\ \mathrm{pF}$',ha='left',size=10,color=muted)
    switch(15.33,y)
    text(15.33,y+.58,r'$\phi_{\mathrm{TRACK}}$',size=10,color=muted)
    line((15.83,y),(18.91,y))
    dot(ho,y)
    text(ho+.30,y-.38*d,r'$V_{\mathrm{H'+idx+'}}$',ha='left',size=11)
    switch(ho,y+.83*d,axis='v',sign=d)
    line((ho,y),(ho,y+.33*d))
    line((ho,y+1.33*d),(ho,y+1.76*d))
    rail(ho,y+1.76*d)
    text(ho,y+2.06*d,r'$V_{\mathrm{PRE}}$',size=11)
    text(ho+.30,y+.90*d,r'$\phi_{\mathrm{PRE}}$',size=10,ha='left',color=muted)
    line((ho,y),(ho,y-.21*d))
    capacitor(ho,y-.71*d,axis='v',sign=-d,width=.23)
    ground(ho,y-1.21*d,-d)
    text(ho-.33,y-.75*d,r'$10\ \mathrm{pF}$',ha='right',size=10,color=muted)
    resistor(19.52,y)
    line((20.13,y),(21.79,y))
    dot(21.79,y,False)
    text(19.52,y+.43,r'$5\ \Omega$',size=10,color=muted)
    text(21.72,y+.45,r'$\mathrm{PIN}'+idx+'$',size=11,ha='right',weight='bold')

y_p,y_n=7.32,3.35
ax.add_patch(FancyBboxPatch((9.28,2.99),3.64,4.69,boxstyle='round,pad=0,rounding_size=.08',
                            edgecolor=ink,facecolor='#f3f7f8',lw=1.7,zorder=1))
circuit_branch(y_p,1,'p')
circuit_branch(y_n,-1,'n')
text(9.57,y_p,'−',size=16)
text(9.57,y_n,'+',size=15)
text(12.60,y_p,'+',size=15)
text(12.60,y_n,'−',size=16)
text(11.10,5.91,'Fully differential OTA',size=12,weight='bold')
text(11.10,5.39,'Telescopic + CMFB',size=11)
text(11.10,4.78,'Output CM target  2.5 V',size=10,color=muted)
text(11.10,4.34,'5 V supply',size=10,color=muted)
text(20.35,5.62,'ADC-facing output',size=11,weight='bold')
text(20.35,5.12,r'$\Delta V = V_{\mathrm{PINP}} - V_{\mathrm{PINN}}$',size=11,color=blue)

fig.lines.append(plt.Line2D([.046,.954],[.109,.109],transform=fig.transFigure,
                            color=light,lw=1.15))
fig.text(.046,.952,'SCB10H differential switched-capacitor testbench',color=ink,
         fontsize=25,fontweight='bold',ha='left',va='top')
fig.text(.046,.884,'Single 10 kHz clock  •  SCL08 transmission gates  •  Controlled TX discharge',
         color=muted,fontsize=13,ha='left',va='top')
fig.text(.046,.081,
         r'$V_{\mathrm{PRE}}$ is the buffered 2.5 V precharge reference.  '
         r'Each $C_{\mathrm{F}}$ bank uses 121 PMOS units at $W/L=20/10\ \mathrm{\mu m/\mu m}$.',
         color=ink,fontsize=10.5,ha='left',va='center')
fig.text(.046,.045,'One clock generates all labeled phases. Bench pad and board shunt loads are omitted from the drawing.',
         color=muted,fontsize=10.5,ha='left',va='center')
fig.savefig(OUT/'scb10h_sc_testbench.png',dpi=180)

