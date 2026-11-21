from pathlib import Path
import pya,re,json
R=Path(__file__).resolve().parents[1]
cfg=json.loads((R/'selected.json').read_text());target_res=cfg['R_kohm']*1000
ly=pya.Layout();ly.dbu=.001;c=ly.create_cell('ota_telescopic_layout')
def box(la,x1,y1,x2,y2):c.shapes(ly.layer(la,0)).insert(pya.DBox(x1,y1,x2,y2))
def text(la,x,y,s):c.shapes(ly.layer(la,7)).insert(pya.DText(s,pya.DTrans(pya.DVector(x,y))))
def contact(x,y):box(7,x-.6,y-.6,x+.6,y+.6);box(8,x-1.1,y-1.1,x+1.1,y+1.1)
def via(x,y):
 box(9,x-.75,y-.75,x+.75,y+.75)
 for la in [8,10]:box(la,x-1.5,y-1.5,x+1.5,y+1.5)
ports=['INP','INN','OUTP','OUTM','VDD','VSS','IREF','VCM','VBN','VBP']
ren={'ip':'INP','im':'INN','op':'OUTP','om':'OUTM','vdd':'VDD','0':'VSS','bn':'IREF','vcm':'VCM','nb':'VBN','pb':'VBP'}
node=lambda s:ren.get(s,s.upper())
source=(R/'models/source_telescopic.spice').read_text();ref=['* Independent source-model reference, external cascode references and integrated bias diode.','.subckt ota_telescopic_layout '+' '.join(ports)];dev=[]
for line in source.splitlines():
 if not line.startswith('M'):continue
 a=line.split();d,g,s,b=map(node,a[1:5]);t=a[5]
 w=float(re.search(r'\bW=([\d.]+)u',line,re.I)[1]);l=float(re.search(r'\bL=([\d.]+)u',line,re.I)[1]);m=re.search(r'\bM=([\d.]+)',line,re.I);count=int(float(m[1])) if m else 1
 ref.append(f'{a[0]} {d} {g} {s} {b} {t} W={w}u L={l}u M={count}')
 for k in range(count):dev.append((a[0]+'_'+str(k),d,g,s,b,t,w,l))
dev.append(('MREF','IREF','IREF','VSS','VSS','N',20,3.2));ref+=['MREF IREF IREF VSS VSS N W=20u L=3.2u',f'RSP SP SENSE {target_res} RPP',f'RSM SM SENSE {target_res} RPP','.ends ota_telescopic_layout']
(R/'schematic/reference.cdl').write_text('\n'.join(ref)+'\n')
# Group the matched input pair adjacently; all other units remain identical W/L.
core=[d for d in dev if d[0].startswith(('MN1_','MN2_','MNC','MPC','MP1_','MP2_','MTAIL','MREF'))]
detector=[d for d in dev if d[0].startswith(('MCS_','MCR_','MCBI_','MCBN_','MCT_','MCP1_','MCP2_','MCFN','MCFP'))]
other=[d for d in dev if d not in core and d not in detector]
# Put the high-impedance detector next to the resistor banks, after the buffer/cap rows.
dev=core+other+detector
nets=ports+list(dict.fromkeys(n for d in dev for n in d[1:5] if n not in ports))
devx=5+len(nets)*5+25
rows=[dev[i:i+6] for i in range(0,len(dev),6)];placements=[];rowinfo=[];ybase=0
for row in rows:
 used=[n for n in nets if any(n in d[1:5] for d in row)];buses={n:ybase+i*4.8 for i,n in enumerate(used)};y=ybase+len(used)*4.8+9;x=devx
 for d in row:placements.append((d,x,y,buses));x+=d[-1]+34
 rowinfo.append((buses,x));ybase=y+max(d[-2] for d in row)+14
for (name,d,g,s,b,t,w,l),x,y,by in placements:
 gx=x+8;sx=gx-3;dx=gx+l+3;bx=gx+l+10
 box(2,gx-4.5,y,gx+l+4.5,y+w);box(4,gx,y-1.5,gx+l,y+w+5)
 if w<2.6:
  for xx in [sx,dx]:box(2,xx-1.4,y-.1,xx+1.4,y+w+.1)
 gc=gx+l/2;box(4,gc-1.1,y+w+2.1,gc+1.1,y+w+4.3);contact(gc,y+w+3.2);box(8,x-1.1,y+w+2.1,gc+1.1,y+w+4.3)
 # Repeated source/drain contacts reduce the unmodeled diffusion spreading resistance.
 yy=[y+w/2] if w<3 else [y+1.5+2.4*k for k in range(int((w-3)/2.4)+1)]
 for xx,n in [(sx,s),(dx,d)]:
  for cy in yy:contact(xx,cy)
  box(8,xx-1.1,by[n],xx+1.1,max(yy)+1.1);via(xx,by[n])
 for tx,ty,n in [(x,y+w+3.2,g),(bx,y+3,b)]:
  box(8,tx-1.1,by[n],tx+1.1,ty+1.1);via(tx,by[n])
 box(2,bx-1.5,y+1.5,bx+1.5,y+4.5);contact(bx,y+3)
 if t=='P':
  box(1,gx-8,y-5,bx+5,y+w+7);box(3,gx-10,y-7,bx+7,y+w+9)
  for la in [5,6]:box(la,gx-5.2,y-(.8 if w<2.6 else .7),gx+l+5.2,y+w+(.8 if w<2.6 else .7))
 else:
  for la in [5,6]:box(la,bx-2.2,y+.8,bx+2.2,y+5.2)
for by,end in rowinfo:
 for n,yy in by.items():
  tx=5+nets.index(n)*5;box(10,tx-1.5,yy-1.5,end,yy+1.5);via(tx,yy)
for n in nets:
 tx=5+nets.index(n)*5;ys=[by[n] for by,end in rowinfo if n in by];box(8,tx-1.1,min(ys)-1.5,tx+1.1,max(ys)+1.5)
 if n in ports:text(8,tx,min(ys),n)
# Two native 1 Mohm P-poly resistors. 100 series sections per bank.
# 1 nm grid snapping changes resistance by far less than deck tolerance.
ry=ybase+35;rx0=devx+10;rw=2.4;segments=40;rl=round(target_res*rw/(28*segments),3)
res_geom=[]
for bank,src in enumerate(['SP','SM']):
 rx=rx0+bank*(rl+35)
 for k in range(segments):
  yy=ry+6*k;box(4,rx-3.6,yy-rw/2,rx+rl+3.6,yy+rw/2)
  for la in [5,6]:box(la,rx-4.3,yy-1.9,rx+rl+4.3,yy+1.9)
  box(44,rx,yy-rw/2,rx+rl,yy+rw/2)
  for xx in [rx-1.8,rx+rl+1.8]:contact(xx,yy)
  box(36,rx-3.6,yy-rw/2,rx,yy+rw/2);box(36,rx+rl,yy-rw/2,rx+rl+3.6,yy+rw/2)
  if k<segments-1:
   xx=rx+rl+1.8 if k%2==0 else rx-1.8;box(8,xx-1.1,yy-1.1,xx+1.1,yy+7.1)
  res_geom.append(dict(bank=bank,segment=k,x=rx,y=yy,W_um=rw,L_um=rl))
 for net,yy,routey in [(src,ry,ry-12-6*bank),('SENSE',ry+6*(segments-1),ry+6*(segments-1)+12)]:
  xx=5+nets.index(net)*5;ys=[by[net] for by,end in rowinfo if net in by]
  box(8,xx-1.1,min(ys)-1.5,xx+1.1,routey+1.5);via(xx,routey);via(rx-8,routey)
  box(8,rx-9.1,min(routey,yy)-1.1,rx-6.9,max(routey,yy)+1.1)
  box(8,rx-9.1,yy-1.1,rx-.7,yy+1.1);box(10,xx-1.5,routey-1.5,rx-6.5,routey+1.5)
ly.write(str(R/'layout/ota_telescopic_layout.gds'))
(R/'verification/placements.json').write_text(json.dumps([dict(name=d[0],D=d[1],G=d[2],S=d[3],B=d[4],type=d[5],W_um=d[6],L_um=d[7],x=x,y=y) for d,x,y,b in placements],indent=2))
(R/'verification/resistors.json').write_text(json.dumps(res_geom,indent=2))
b=c.dbbox();summary=dict(MOS_units=len(dev),resistor_segments=len(res_geom),bbox_um=[b.left,b.bottom,b.right,b.top],area_mm2=b.width()*b.height()/1e6,ports=ports)
(R/'verification/geometry_summary.json').write_text(json.dumps(summary,indent=2));print(summary)
