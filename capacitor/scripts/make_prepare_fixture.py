from common import ROOT as R
p=R/'results/prepare_workflow';p.mkdir(exist_ok=True)
s=(R/'examples/value_demo.sch').read_text().replace('name=XC0 value=2.5p','name=XC0 value=4p')
(p/'request_4p.sch').write_text(s)
print(p/'request_4p.sch')
