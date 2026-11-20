// ============================================================================
// Proyecto: Open Photonic GPU (OPGPU-TX-v1)
// Módulo: opgpu_odd_controller.v
// Licencia: CC0 1.0 Universal (Dominio Público / Prior Art)
// Descripción: Controlador de Autodescubrimiento Óptico (ODD 32-bit) y
//              conmutación automática a modo prueba (Cross-Loopback).
// ============================================================================

module opgpu_odd_controller (
    input  wire        clk_100mhz,       // Reloj base de control
    input  wire        rst_n,            // Reset activo en bajo
    input  wire        reprobe_trigger,  // Señal para re-escanear fibra

    // Interfaz hacia Front-End Óptico (QSFP28 / Bloque D)
    output reg         tx_pilot_en,      // Habilita pulso piloto de interrogación
    output reg         opt_sw_loopback,  // 0: Modo Normal (Externo) | 1: Cross-Loopback
    input  wire        rx_signal_detect, // Detector de potencia óptica recibida
    input  wire [31:0] rx_odd_raw_frame, // Trama de 32 bits decodificada del eco ODD
    input  wire        rx_odd_valid,     // Pulso de trama ODD recibida correctamente

    // Registros de Estado hacia Bus PCIe / CXL (Bloque A)
    output reg  [1:0]  system_mode,      // 00: INIT, 01: NORMAL_OPGPU, 10: LOOPBACK_TEST, 11: FAULT
    output reg  [31:0] odd_descriptor,   // Descriptor ODD activo (ARCH, LOGIC, SHEETS, dB, FLAGS)
    output reg  [7:0]  laser_bias_dac    // Ajuste de potencia láser según atenuación del módulo
);

    // Definición de Estados
    localparam ST_IDLE         = 3'd0;
    localparam ST_SEND_PING    = 3'd1;
    localparam ST_WAIT_ECHO    = 3'd2;
    localparam ST_CONFIG_NORM  = 3'd3;
    localparam ST_CONFIG_LOOP  = 3'd4;
    localparam ST_ACTIVE       = 3'd5;

    reg [2:0]  state;
    reg [19:0] timeout_cnt; // Contador para ventana de espera (10 ms @ 100 MHz = 1,000,000 ciclos)

    // Extracción de campos del Descriptor ODD (Bits 23:16 = LINK_BUDGET_DB)
    wire [7:0] expected_loss_db = rx_odd_raw_frame[23:16];

    always @(posedge clk_100mhz or negedge rst_n) begin
        if (!rst_n) begin
            state           <= ST_IDLE;
            tx_pilot_en     <= 1'b0;
            opt_sw_loopback <= 1'b0;
            system_mode     <= 2'b00;
            odd_descriptor  <= 32'h0000_0000;
            laser_bias_dac  <= 8'h20; // Potencia mínima segura por defecto
            timeout_cnt     <= 20'd0;
        end else begin
            case (state)
                ST_IDLE: begin
                    system_mode     <= 2'b00;
                    opt_sw_loopback <= 1'b0; // Abre camino hacia el puerto externo
                    timeout_cnt     <= 20'd0;
                    state           <= ST_SEND_PING;
                end

                ST_SEND_PING: begin
                    tx_pilot_en <= 1'b1; // Emite pulso óptico de interrogación ODD
                    state       <= ST_WAIT_ECHO;
                end

                ST_WAIT_ECHO: begin
                    tx_pilot_en <= 1'b0;
                    timeout_cnt <= timeout_cnt + 1'b1;

                    if (rx_odd_valid && (rx_odd_raw_frame[3:0] != 4'h0)) begin
                        // Caso 3: Tanque remoto detectado con firma espectral/temporal válida
                        odd_descriptor <= rx_odd_raw_frame;
                        state          <= ST_CONFIG_NORM;
                    end else if (timeout_cnt >= 20'd1_000_000) begin
                        // Caso 1: Timeout (10 ms sin retorno externo) -> Activar prueba cruzada
                        state          <= ST_CONFIG_LOOP;
                    end
                end

                ST_CONFIG_NORM: begin
                    opt_sw_loopback <= 1'b0; // Mantiene enlace hacia fibra externa
                    system_mode     <= 2'b01; // MODO NORMAL OPGPU
                    // Ajusta ganancia del láser proporcional a la pérdida reportada por el módulo
                    laser_bias_dac  <= 8'h40 + expected_loss_db;
                    state           <= ST_ACTIVE;
                end

                ST_CONFIG_LOOP: begin
                    opt_sw_loopback <= 1'b1; // Conmuta matriz interna: TX1->RX2 y TX2->RX1
                    system_mode     <= 2'b10; // MODO PRUEBA (CROSS-LOOPBACK)
                    // Descriptor virtual emulado: 1 Lámina, Membranas, 12 dB atenuación interna
                    odd_descriptor  <= 32'h07_30_01_11;
                    laser_bias_dac  <= 8'h50; // Calibrado para el atenuador interno de 12 dB
                    state           <= ST_ACTIVE;
                end

                ST_ACTIVE: begin
                    if (reprobe_trigger) begin
                        state <= ST_IDLE;
                    end else if (!rx_signal_detect && (system_mode == 2'b01)) begin
                        // Protección de seguridad: si se desconecta la fibra en caliente, corta láser
                        laser_bias_dac <= 8'h10;
                        system_mode    <= 2'b11; // FAULT / LINK_LOSS
                    end
                end

                default: state <= ST_IDLE;
            endcase
        end
    end
endmodule
