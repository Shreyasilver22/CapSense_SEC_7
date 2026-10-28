crashbackups stop
drc off
gds read {../../layouts/capopt_slotted_4p.gds}
load capopt_slotted_4p
select top cell
extract all
ext2spice default
ext2spice format ngspice
ext2spice scale off
ext2spice cthresh 0
ext2spice subcircuits top on
ext2spice -y 6 -o capopt_slotted_4p.native.spice
save capopt_slotted_4p
quit -noprompt
