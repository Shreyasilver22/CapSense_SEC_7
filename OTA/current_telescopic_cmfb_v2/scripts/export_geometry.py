import pya,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];ly=pya.Layout();ly.read(str(R/'layout/ota_telescopic_layout.gds'));c=ly.top_cell();data=[]
for li in ly.layer_indexes():
 info=ly.get_info(li)
 if info.datatype!=0:continue
 for sh in c.shapes(li).each():
  if sh.is_box():
   b=sh.box;data.append([info.layer,b.left*ly.dbu,b.bottom*ly.dbu,b.right*ly.dbu,b.top*ly.dbu])
(R/'verification/geometry.json').write_text(json.dumps(data))
