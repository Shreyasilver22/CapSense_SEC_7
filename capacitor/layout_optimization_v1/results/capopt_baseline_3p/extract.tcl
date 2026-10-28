crashbackups stop
drc off
gds read {../../layouts/capopt_baseline_3p.gds}
load capopt_baseline_3p
select top cell
extract all
ext2spice default
ext2spice format ngspice
ext2spice scale off
ext2spice cthresh 0
ext2spice subcircuits top on
ext2spice -y 6 -o capopt_baseline_3p.native.spice
save capopt_baseline_3p
quit -noprompt
