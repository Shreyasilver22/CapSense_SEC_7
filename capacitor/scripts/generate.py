import pya,os,sys,json
from pathlib import Path
root=Path(os.environ['CAP_PROJECT_ROOT']);sys.path.insert(0,str(root/'scripts'))
from common import requests
seen=set();geometry=[]
for r in requests():
 name=r['cell']
 if name in seen:continue
 seen.add(name);n,nx,ny=r['units'],r['columns'],r['rows']
 layout=pya.Layout();layout.dbu=.001;m1=layout.layer(8,0);m2=layout.layer(10,0);t1=layout.layer(8,7);t2=layout.layer(10,7);cell=layout.create_cell(name)
 def rect(layer,x1,y1,x2,y2):cell.shapes(layer).insert(pya.Box(round(x1*1000),round(y1*1000),round(x2*1000),round(y2*1000)))
 for col in range(nx):
  used=[row for row in range(ny) if row*nx+col<n];assert used
  x=40*col
  for row in used:
   y=28*row;rect(m1,x,y,x+20,y+20);rect(m1,x-6,y+8,x,y+12);rect(m2,x,y,x+20,y+20);rect(m2,x+20,y+8,x+26,y+12)
  if n>1:
   rect(m1,x-6,-8,x-2,used[-1]*28+12)
   rect(m2,x+22,8,x+26,(ny-1)*28+28)
 if n>1:
  if nx>1:rect(m1,-6,-8,(nx-1)*40-2,-4)
  rect(m2,22,(ny-1)*28+24,(nx-1)*40+26,(ny-1)*28+28)
 bot=(-4,-6) if n>1 else (-4,10);top=(24,(ny-1)*28+26) if n>1 else (24,10)
 cell.shapes(t1).insert(pya.Text('BOT',pya.Trans(int(bot[0]*1000),int(bot[1]*1000))));cell.shapes(t2).insert(pya.Text('TOP',pya.Trans(int(top[0]*1000),int(top[1]*1000))))
 regions=[]
 for layer in [m1,m2]:
  reg=pya.Region(cell.begin_shapes_rec(layer));reg.merge();assert reg.count()==1,(name,layer);regions.append(reg)
 overlap=(regions[0]&regions[1]).area()*1e-6;assert abs(overlap-n*400)<1e-6,(name,overlap)
 layout.write(str(root/'layouts'/(name+'.gds')));b=cell.bbox();geometry.append(dict(cell=name,units=n,columns=nx,rows=ny,width_um=b.width()*.001,height_um=b.height()*.001,overlap_um2=overlap,footprint_um2=b.area()*1e-6))
(root/'results/geometry.json').write_text(json.dumps(geometry,indent=2));print('Generated',len(geometry),'connected, via-free cells with verified plate-overlap area')
