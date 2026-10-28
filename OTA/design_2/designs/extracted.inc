** sch_path: OTA/design_2/designs/ota_extracted_cc.sch
.subckt ota_extracted_cc inp inn out vdd vss iref
*.ipin inp
*.ipin inn
*.opin out
*.iopin vdd
*.iopin vss
*.iopin iref
M3 n1 n1 vdd vdd P w=10u l=3.2u m=1
M4 n2 n1 vdd vdd P w=10u l=3.2u m=1
M1 n1 inn tail vss N w=7.5u l=2.4u m=1
M2 n2 inp tail vss N w=7.5u l=2.4u m=1
M5 tail iref vss vss N w=20u l=3.2u m=1
M6 out n2 vdd vdd P w=112u l=3.2u m=1
M7 out iref vss vss N w=160u l=3.2u m=1
M8 iref iref vss vss N w=20u l=3.2u m=1
XCC n2 out vss scl08_cap_8p
.ends
