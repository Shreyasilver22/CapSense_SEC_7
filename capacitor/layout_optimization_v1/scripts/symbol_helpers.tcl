set capopt_root [file dirname [file dirname [file normalize [info script]]]]
source [file join $capopt_root models catalog.tcl]
proc capopt_model {style value pins} {
 global capopt_cm_pf
 set name capopt_${style}_${value}
 if {![info exists capopt_cm_pf($name)]} {return capopt_UNPREPARED}
 if {$pins==2} {append name _gnd}
 return $name
}
proc capopt_info {style value} {
 global capopt_cm_pf
 set name capopt_${style}_${value}
 if {[info exists capopt_cm_pf($name)]} {return "Extracted: $capopt_cm_pf($name) pF"}
 return {NOT PREPARED}
}
