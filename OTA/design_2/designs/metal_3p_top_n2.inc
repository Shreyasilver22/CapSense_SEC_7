* Device-group sizing; W/L fixed within each length group.
* K scales BOTH M6 and M7 W/L, preserving approximate second-stage DC balance.
* Nominal output/tail current ratio = 2*K; measured ratios are reported.
.subckt ota_tuned inp inn out vdd vss iref params: LI=3.2u LM=3.2u LO=3.2u K=1 CC=20p
M1 n1 inn tail vss N W={3.125*LI} L={LI}
M2 n2 inp tail vss N W={3.125*LI} L={LI}
M3 n1 n1 vdd vdd P W={3.125*LM} L={LM}
M4 n2 n1 vdd vdd P W={3.125*LM} L={LM}
M5 tail iref vss vss N W=20u L=3.2u
M6 out n2 vdd vdd P W={8.75*LO*K} L={LO}
M7 out iref vss vss N W={12.5*LO*K} L={LO}
M8 iref iref vss vss N W=20u L=3.2u
XCC n2 out vss scl08_cap_3p
.ends ota_tuned
