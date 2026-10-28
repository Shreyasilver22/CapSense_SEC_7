crashbackups stop
drc off
gds read {../../layouts/scl08_cap_n660.gds}
load scl08_cap_n660
select top cell
extract all
ext2spice default
ext2spice format ngspice
ext2spice scale off
ext2spice cthresh 0
ext2spice subcircuits top on
ext2spice -y 6 -o scl08_cap_n660.native.spice
save scl08_cap_n660
quit -noprompt
