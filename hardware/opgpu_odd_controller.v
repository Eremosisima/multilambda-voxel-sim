// ============================================================================
// Proyecto: Open Photonic GPU (OPGPU-TX-v1)
// Archivo: rtl/opgpu_odd_controller.v
// Licencia: CC0 1.0 Universal (Dominio Público / Prior Art)
// ============================================================================

module opgpu_odd_controller (
    input  wire        clk_100mhz,
    input  wire        rst_n,
    input  wire        reprobe_trigger,
    output reg         tx_pilot_en,
    output reg         opt_sw_loopback,
    input  wire        rx_signal_detect,
    input  wire [31:0] rx_odd_raw_frame,
    input  wire        rx_odd_valid,
    output reg  [1:0]  system_mode,
    output reg  [31:0] odd_descriptor,
    output reg  [7:0]  laser_bias_dac
);

    localparam ST_IDLE        = 3'd0;
    localparam ST_SEND_PING   = 3'd1;
    localparam ST_WAIT_ECHO   = 3'd2;
    localparam ST_CONFIG_NORM = 3'd3;
    localparam ST_CONFIG_LOOP = 3'd4;
    localparam ST_ACTIVE      = 3'd5;

    reg [2:0]  state;
    reg [19:0] timeout_cnt;

    wire [7:0] expected_loss_db = rx_odd_raw_frame[23:16];

    always @(posedge clk_100mhz or negedge rst_n) begin
        if (!rst_n) begin
            state           <= ST_IDLE;
            tx_pilot_en     <= 1'b0;
            opt_sw_loopback <= 1'b0;
            system_mode     <= 2'b00;
            odd_descriptor  <= 32'h0000_0000;
            laser_bias_dac  <= 8'h20;
            timeout_cnt     <= 20'd0;
        end else begin
            case (state)
                ST_IDLE: begin
                    system_mode     <= 2'b00;
                    opt_sw_loopback <= 1'b0;
                    timeout_cnt     <= 20'd0;
                    state           <= ST_SEND_PING;
                end
                ST_SEND_PING: begin
                    tx_pilot_en <= 1'b1;
                    state       <= ST_WAIT_ECHO;
                end
                ST_WAIT_ECHO: begin
                    tx_pilot_en <= 1'b0;
                    timeout_cnt <= timeout_cnt + 1'b1;
                    if (rx_odd_valid && (rx_odd_raw_frame[3:0] != 4'h0)) begin
                        odd_descriptor <= rx_odd_raw_frame;
                        state          <= ST_CONFIG_NORM;
                    end else if (timeout_cnt >= 20'd1_000_000) begin
                        state          <= ST_CONFIG_LOOP;
                    end
                end
                ST_CONFIG_NORM: begin
                    opt_sw_loopback <= 1'b0;
                    system_mode     <= 2'b01;
                    laser_bias_dac  <= 8'h40 + expected_loss_db;
                    state           <= ST_ACTIVE;
                end
                ST_CONFIG_LOOP: begin
                    opt_sw_loopback <= 1'b1;
                    system_mode     <= 2'b10;
                    odd_descriptor  <= 32'h07_30_01_11;
                    laser_bias_dac  <= 8'h50;
                    state           <= ST_ACTIVE;
                end
                ST_ACTIVE: begin
                    if (reprobe_trigger) begin
                        state <= ST_IDLE;
                    end else if (!rx_signal_detect && (system_mode == 2'b01)) begin
                        laser_bias_dac <= 8'h10;
                        system_mode    <= 2'b11;
                    end
                end
                default: state <= ST_IDLE;
            endcase
        end
    end
endmodule
