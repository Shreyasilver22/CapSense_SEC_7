crashbackups stop
drc off
gds read ../layout/ota_boosted_layout.gds
load ota_boosted_layout
select top cell
extract all
ext2spice default
ext2spice format ngspice
ext2spice scale off
ext2spice cthresh 0
ext2spice resistor tee on
ext2spice subcircuits top on
ext2spice -o ota_C_raw.spice
puts "Extraction feedback count: [feedback count]"
for {set i 1} {$i <= [feedback count]} {incr i} {feedback find $i; feedback why}
quit -noprompt
