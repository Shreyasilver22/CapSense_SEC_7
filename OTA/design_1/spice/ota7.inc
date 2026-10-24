* Seven MOS core. External ideal VBN required; bias generator excluded.
* inp is noninverting after two stages. All dimensions explicit SI units.
.subckt ota7 inp inn out vdd vss vbn
M1 n1 inn tail vss N W=2.5u L=0.8u
M2 n2 inp tail vss N W=2.5u L=0.8u
M3 n1 n1 vdd vdd P W=2.5u L=0.8u
M4 n2 n1 vdd vdd P W=2.5u L=0.8u
M5 tail vbn vss vss N W=5u L=0.8u
M6 out n2 vdd vdd P W=7u L=0.8u
M7 out vbn vss vss N W=10u L=0.8u
Cc n2 out 5p
.ends ota7
