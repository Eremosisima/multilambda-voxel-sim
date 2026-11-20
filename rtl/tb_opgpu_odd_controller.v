// ============================================================================
// Proyecto: Open Photonic GPU (OPGPU-TX-v1)
// Archivo: rtl/tb_opgpu_odd_controller.v
// Licencia: CC0 1.0 Universal (Dominio Público)
// ============================================================================
`timescale 1ns / 1ps

module tb_opgpu_odd_controller;
    reg clk = 0;
    reg rst_n = 0;
    reg reprobe = 0;
    reg rx_sig = 0;
    reg [31:0] rx_frame = 0;
    reg rx_valid = 0;

    wire tx_pilot;
    wire opt_loopback;
    wire [1:0] sys_mode;
    wire [31:0] odd_desc;
    wire [7:0] laser_dac;

    opgpu_odd_controller dut (
        .clk_100mhz(clk), .rst_n(rst_n), .reprobe_trigger(reprobe),
        .tx_pilot_en(tx_pilot), .opt_sw_loopback(opt_loopback),
        .rx_signal_detect(rx_sig), .rx_odd_raw_frame(rx_frame),
        .rx_odd_valid(rx_valid), .system_mode(sys_mode),
        .odd_descriptor(odd_desc), .laser_bias_dac(laser_dac)
    );

    always #5 clk = ~clk;

    initial begin
        $display("=== INICIANDO TESTBENCH RTL (SUITE S2) ===");
        #20 rst_n = 1;
        #10_050_000;
        if (sys_mode == 2'b10 && opt_loopback == 1'b1)
            $display("[PASS] Prueba 1: Cross-Loopback activado (ODD: 0x%h)", odd_desc);
        else
            $display("[FAIL] Prueba 1: Fallo en deteccion.");

        reprobe = 1; #20; reprobe = 0;
        #100;
        rx_sig = 1;
        rx_frame = 32'h07_38_08_11;
        rx_valid = 1; #10; rx_valid = 0;
        #50;

        if (sys_mode == 2'b01 && opt_loopback == 1'b0 && odd_desc == 32'h07380811)
            $display("[PASS] Prueba 2: Tanque 8 laminas reconocido. Laser DAC: 0x%h", laser_dac);
        else
            $display("[FAIL] Prueba 2: Error lectura ODD.");
        $finish;
    end
endmodule
