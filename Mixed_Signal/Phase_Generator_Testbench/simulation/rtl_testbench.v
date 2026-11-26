`timescale 1ns/1ps
module rtl_testbench;
reg clk=0,rst=1; wire p,t,q,pb,tb,qb,sv;
integer k;
capsense_phase_gen dut(clk,rst,p,t,q,pb,tb,qb,sv);
always #500 clk=~clk;
initial begin
$dumpfile("rtl_phases.vcd"); $dumpvars(0,rtl_testbench);
#1 rst=0; #1;
if ({p,t,q,pb,tb,qb,sv} !== 7'b0001110) $fatal(1,"reset");
#1999 rst=1;
for(k=0;k<300;k=k+1) begin
 @(posedge clk); #1;
 if (p !== ((k%100)<=40) || t !== ((k%100)>=45 && (k%100)<=89) || q !== ((k%100)>=46 && (k%100)<=89) || sv !== ((k%100)==80)) $fatal(1,"phase timing");
 if (pb !== ~p || tb !== ~t || qb !== ~q) $fatal(1,"complements");
end
$display("PASS: reset, 300 clock edges, all seven outputs");$finish;
end
endmodule
