`timescale 1ns/1ps

module capsense_phase_gen (
    input  wire clk_1mhz, rst_n,
    output reg  phi1,
    output reg  phit,
    output reg  phi2,
    output wire phi1b,
    output wire phitb,
    output wire phi2b,
    output reg  sample_valid
);
    reg [6:0] count;
    wire [6:0] next_count;

    assign next_count = (count == 7'd99) ? 7'd0 : (count + 7'd1);

    always @(posedge clk_1mhz or negedge rst_n) begin
        if (!rst_n) begin
            // Entire clock network inactive until reset is released.
            count        <= 7'd99;
            phi1         <= 1'b0;
            phit         <= 1'b0;
            phi2         <= 1'b0;
            sample_valid <= 1'b0;
        end else begin
            count        <= next_count;
            phi1         <= (next_count <= 7'd40);
            phit         <= (next_count >= 7'd45 && next_count <= 7'd89);
            phi2         <= (next_count >= 7'd46 && next_count <= 7'd89);
            sample_valid <= (next_count == 7'd80);
        end
    end

    assign phi1b = ~phi1;
    assign phitb = ~phit;
    assign phi2b = ~phi2;
endmodule
