import pya,os,json,math
from pathlib import Path
R=Path(os.environ['CAP_OPT_ROOT']);cfg=json.loads((R/'config.json').read_text());records=[]
for t in cfg['targets']:
 for style in ['baseline','compact','slotted']:
  name=f"capopt_{style}_{t['token']}";lay=pya.Layout();lay.dbu=.001;m1=lay.layer(8,0);m2=lay.layer(10,0);tx1=lay.layer(8,7);tx2=lay.layer(10,7);cell=lay.create_cell(name)
  def box(layer,x1,y1,x2,y2):
   assert x2>x1 and y2>y1
   cell.shapes(layer).insert(pya.Box(round(x1*1000),round(y1*1000),round(x2*1000),round(y2*1000)))
  if style in ['baseline','compact']:
   if style=='baseline':n=t['baseline_units'];px,py,stub,rail,end,ylow,yhigh=40,28,6,4,26,8,12;mutual_unit=11.384e-15
   else:n=int(t['target_F']/11.338e-15+.5);px,py,stub,rail,end,ylow,yhigh=32,23,5,3,25,8.5,11.5;mutual_unit=11.338e-15
   nx=max(1,math.ceil(math.sqrt(n*py/px)));ny=math.ceil(n/nx);bottom_bus_low=-8 if style=='baseline' else -6;bottom_bus_high=bottom_bus_low+rail;top_bus_high=(ny-1)*py+(28 if style=='baseline' else 26);top_bus_low=top_bus_high-rail
   for col in range(nx):
    used=[row for row in range(ny) if row*nx+col<n];x=col*px
    for row in used:
     y=row*py;box(m1,x,y,x+20,y+20);box(m1,x-stub,y+ylow,x,y+yhigh);box(m2,x,y,x+20,y+20);box(m2,x+20,y+ylow,x+end,y+yhigh)
    box(m1,x-stub,bottom_bus_low,x-stub+rail,used[-1]*py+yhigh);box(m2,x+end-rail,ylow,x+end,top_bus_high)
   if nx>1:box(m1,-stub,bottom_bus_low,(nx-1)*px-stub+rail,bottom_bus_high)
   box(m2,end-rail,top_bus_low,(nx-1)*px+end,top_bus_high)
   bot=(-stub+rail/2,bottom_bus_low+rail/2);top=(end-rail/2,top_bus_low+rail/2)
   route_length=top_bus_high-bottom_bus_low+(nx-1)*px;route_squares=route_length/rail
   details=dict(units=n,columns=nx,rows=ny,pitch_x_um=px,pitch_y_um=py,rail_um=rail,estimated_mutual_F=n*mutual_unit)
  else:
   ny=cfg['strip_rows'][t['token']];height=ny*20+(ny-1)*2
   # Two corresponding 20um-wide strips per row, 2um slots, separate 3um side spines.
   # Estimate overlap plus left-edge coupling only to seed dimensions; extraction is decisive.
   length=round((t['target_F']*1e15-.92*ny)/(.028*20*ny),2)
   if 'strip_length_um' in cfg and t['token'] in cfg['strip_length_um']:length=cfg['strip_length_um'][t['token']]
   for row in range(ny):
    y=row*22;box(m1,-5,y,length,y+20);box(m2,0,y,length+5,y+20)
   box(m1,-5,0,-2,height);box(m2,length+2,0,length+5,height)
   bot=(-3.5,10);top=(length+3.5,10);route_length=height+length;route_squares=height/3+length/20
   details=dict(rows=ny,strip_length_um=length,strip_width_um=20,slot_width_um=2,rail_um=3,estimated_mutual_F=(.028*20*ny*length+.92*ny)*1e-15)
  cell.shapes(tx1).insert(pya.Text('BOT',pya.Trans(round(bot[0]*1000),round(bot[1]*1000))));cell.shapes(tx2).insert(pya.Text('TOP',pya.Trans(round(top[0]*1000),round(top[1]*1000))))
  regions=[]
  for layer,minwidth in [(m1,1700),(m2,2000)]:
   region=pya.Region(cell.begin_shapes_rec(layer));region.merge();assert region.count()==1,(name,'disconnected metal')
   assert region.width_check(minwidth).count()==0,(name,'width')
   assert region.notch_check(1200 if layer==m1 else 1400).count()==0,(name,'notch')
   assert region.sized(-12500).is_empty(),(name,'solid metal exceeds 25um in both directions')
   regions.append(region)
  overlap=(regions[0]&regions[1]).area()*1e-6;b=cell.bbox();lay.write(str(R/'layouts'/(name+'.gds')))
  # Store polygon outlines for scientific layout visualization without proprietary layer files.
  outlines=[]
  for rgn in regions:outlines.append([[[pt.x*.001,pt.y*.001] for pt in poly.each_point_hull()] for poly in rgn.each()])
  records.append(dict(name=name,style=style,token=t['token'],target_F=t['target_F'],width_um=b.width()*.001,height_um=b.height()*.001,area_um2=b.area()*1e-6,overlap_um2=overlap,M1_area_um2=regions[0].area()*1e-6,M2_area_um2=regions[1].area()*1e-6,route_length_proxy_um=route_length,route_squares_proxy=route_squares,M1_route_R_proxy_ohm=.05*route_squares,M2_route_R_proxy_ohm=.03*route_squares,polygons=outlines,**details))
(R/'results/geometry.json').write_text(json.dumps(records,indent=2));print('Generated',len(records),'layouts; connectivity, widths, notches and 25um solid-region checks passed')
