set cap_library_root [file dirname [file dirname [file normalize [info script]]]]
if {[file exists [file join $cap_library_root models catalog.tcl]]} {
  source [file join $cap_library_root models catalog.tcl]
}
proc cap_value_text {value} {
  global cap_actual_pf
  if {[info exists cap_actual_pf($value)]} {return "Extracted: $cap_actual_pf($value) pF"}
  return {NOT PREPARED - generate layout/model}
}

proc cap_notify {message} {
  puts $message
  if {[llength [info commands tk_messageBox]]} {tk_messageBox -message $message -type ok}
}
proc cap_prepare_current {} {
  global cap_library_root cap_pdk_root env cap_prepare_pipe cap_prepare_log
  if {[info exists cap_prepare_pipe]} {cap_notify {A capacitor build is already running.}; return}
  if {[info exists env(SCL08_CAP_PDK_ROOT)]} {set cap_pdk_root $env(SCL08_CAP_PDK_ROOT)}
  if {![info exists cap_pdk_root] || ![file isdirectory $cap_pdk_root]} {
    cap_notify {Set SCL08_CAP_PDK_ROOT to your authorized scl_cp8d directory, then restart xschem.}; return
  }
  # The launcher explicitly says Save + generate; save edited instance values before scanning.
  xschem save
  set filename [xschem get schname]
  if {![file isfile $filename]} {cap_notify {Save this schematic before generating capacitor layouts.}; return}
  set cap_prepare_log [open [file join $cap_library_root results prepare_gui.log] w]
  set command [list | python3 [file join $cap_library_root scripts prepare.py] --schematic $filename --pdk-root $cap_pdk_root 2>@1]
  if {[catch {set cap_prepare_pipe [open $command r]} error]} {
    close $cap_prepare_log; unset cap_prepare_log; cap_notify $error; return
  }
  fconfigure $cap_prepare_pipe -blocking 0 -buffering line
  fileevent $cap_prepare_pipe readable cap_prepare_progress
  puts {Generating checked capacitor layouts/models in background; see results/prepare_gui.log.}
}
proc cap_prepare_progress {} {
  global cap_prepare_pipe cap_prepare_log cap_library_root
  while {[gets $cap_prepare_pipe line]>=0} {puts $cap_prepare_log $line; flush $cap_prepare_log; puts $line}
  if {[eof $cap_prepare_pipe]} {
    fileevent $cap_prepare_pipe readable {}
    fconfigure $cap_prepare_pipe -blocking 1
    set failed [catch {close $cap_prepare_pipe} message]
    close $cap_prepare_log
    unset cap_prepare_pipe cap_prepare_log
    if {$failed} {cap_notify "Build failed: $message. See results/prepare_gui.log."; return}
    uplevel #0 [list source [file join $cap_library_root models catalog.tcl]]
    xschem redraw
    cap_notify {Capacitor models/layouts updated. Check results/catalog.csv for achieved values, then netlist and simulate again.}
  }
}
