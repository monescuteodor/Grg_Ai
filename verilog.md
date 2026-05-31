# Verilog Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH VERILOG


## Remarks

Verilog is a hardware description language (HDL) used to model and simulate digital circuits at the register-transfer level (RTL) and gate level. It is an IEEE standard (1364-1995, 2001, 2005) and is widely used for FPGA and ASIC design. SystemVerilog (IEEE 1800) extends Verilog with OOP features for verification.

Tools: Icarus Verilog (iverilog), Verilator, Xilinx Vivado, Intel Quartus, ModelSim, GTKWave (waveform viewer).


## Hello World / Testbench

```verilog
// hello.v — simulation only (no real hardware)
module hello;
    initial begin
        $display("Hello, World!");
        $display("Hello, %s!", "Verilog");
        $finish;
    end
endmodule
```

```bash
iverilog -o hello hello.v && ./hello
# Hello, World!
# Hello, Verilog!
```


---

# CHAPTER 2: DATA TYPES AND LOGIC VALUES


## Verilog Types

```verilog
// Logic values: 0, 1, x (unknown), z (high-impedance)

// Net types (physical connections)
wire w;           // single-bit wire
wire [7:0] bus;   // 8-bit bus (7=MSB, 0=LSB)
wire [31:0] data; // 32-bit bus

// Register types (can store values)
reg r;            // single-bit register
reg [7:0] byte_val;   // 8-bit register
reg [31:0] word_val;  // 32-bit register
reg signed [15:0] s;  // signed 16-bit

// Integer types
integer i;        // 32-bit signed integer (for loops)
real r_val;       // floating point (simulation only)
time t;           // 64-bit for simulation time

// Parameters (constants)
parameter WIDTH = 8;
parameter DEPTH = 256;
localparam MAX = (1 << WIDTH) - 1;   // local parameter

// String (simulation only)
reg [8*13-1:0] str;   // "Hello, World!" needs 13 bytes

// Literals
8'b10101010    // 8-bit binary
8'hAB          // 8-bit hex
8'd170         // 8-bit decimal
8'o252         // 8-bit octal
'b1            // sized-less binary

// Special values
1'bx           // unknown
1'bz           // high-impedance
32'bx          // all bits unknown
4'b1z0x        // mixed

// Arrays
reg [7:0] memory [0:255];       // 256 bytes
reg [7:0] matrix [0:3][0:3];    // 4x4 matrix
wire [31:0] regfile [0:31];     // 32 32-bit registers

// Signed vs unsigned
reg [7:0] u = 8'd200;    // unsigned: 200
reg signed [7:0] s2 = -8'd56; // signed: -56

// $signed / $unsigned conversion
$signed(u)     // interpret as signed
$unsigned(s2)  // interpret as unsigned
```


---

# CHAPTER 3: MODULES AND INSTANTIATION


## Module Structure

```verilog
// Module definition
module adder #(
    parameter WIDTH = 8        // parameterized width
) (
    input  wire [WIDTH-1:0] a,  // input ports
    input  wire [WIDTH-1:0] b,
    input  wire              cin,
    output wire [WIDTH-1:0] sum,
    output wire              cout
);

    // Internal signals
    wire [WIDTH:0] result;

    // Continuous assignment
    assign result = {1'b0, a} + {1'b0, b} + {{WIDTH{1'b0}}, cin};
    assign sum  = result[WIDTH-1:0];
    assign cout = result[WIDTH];

endmodule

// Module instantiation
module top;
    wire [7:0] a = 8'd15;
    wire [7:0] b = 8'd27;
    wire [7:0] s;
    wire c;

    // Instantiate by name (preferred)
    adder #(.WIDTH(8)) u_adder (
        .a   (a),
        .b   (b),
        .cin (1'b0),
        .sum (s),
        .cout(c)
    );

    initial begin
        #10;
        $display("Sum = %d, Carry = %b", s, c);
        $finish;
    end
endmodule

// Common module pattern
module register #(
    parameter WIDTH = 8,
    parameter RESET_VAL = 0
) (
    input  wire             clk,
    input  wire             rst_n,     // active low reset
    input  wire             en,
    input  wire [WIDTH-1:0] d,
    output reg  [WIDTH-1:0] q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= RESET_VAL;
        else if (en)
            q <= d;
    end

endmodule
```


---

# CHAPTER 4: BEHAVIORAL MODELING


## Procedural Blocks

```verilog
// always block — synthesizable (for hardware)
module combinational (
    input  wire [3:0] a, b,
    input  wire       sel,
    output reg  [3:0] y
);

    // Combinational logic: sensitive to all inputs
    always @(*) begin    // @(*) = automatic sensitivity list
        if (sel)
            y = a;
        else
            y = b;
    end

endmodule

// Sequential logic — flip-flop
module d_ff (
    input  wire clk,
    input  wire rst_n,
    input  wire d,
    output reg  q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 1'b0;     // non-blocking assignment (use in sequential)
        else
            q <= d;
    end

endmodule

// Case statement
module decoder_4to16 (
    input  wire [3:0] sel,
    output reg  [15:0] y
);

    always @(*) begin
        y = 16'b0;    // default: all zeros
        case (sel)
            4'd0:  y = 16'h0001;
            4'd1:  y = 16'h0002;
            4'd2:  y = 16'h0004;
            // ...
            4'd15: y = 16'h8000;
            default: y = 16'hxxxx;
        endcase
    end

endmodule

// Casez (z matches anything including ?, z, 0, 1)
// Casex (x and z both match anything)
module priority_encoder (
    input  wire [7:0] in,
    output reg  [2:0] out,
    output reg        valid
);

    always @(*) begin
        valid = 1'b1;
        casez (in)
            8'b1??????? : out = 3'd7;
            8'b01?????? : out = 3'd6;
            8'b001????? : out = 3'd5;
            8'b0001???? : out = 3'd4;
            8'b00001??? : out = 3'd3;
            8'b000001?? : out = 3'd2;
            8'b0000001? : out = 3'd1;
            8'b00000001 : out = 3'd0;
            default:     begin out = 3'd0; valid = 1'b0; end
        endcase
    end

endmodule

// Initial block (simulation only, not synthesizable)
initial begin
    clk = 0;
    rst_n = 0;
    #20 rst_n = 1;
    #1000 $finish;
end

always #5 clk = ~clk;    // 10ns period clock
```


---

# CHAPTER 5: OPERATORS AND EXPRESSIONS


## Verilog Operators

```verilog
module operators_demo;
    reg [7:0] a = 8'b10101010;
    reg [7:0] b = 8'b11001100;
    reg [7:0] result;
    integer i;

    initial begin
        // Bitwise operators
        result = a & b;     // AND:  8'b10001000
        result = a | b;     // OR:   8'b11101110
        result = a ^ b;     // XOR:  8'b01100110
        result = ~a;        // NOT:  8'b01010101
        result = ~(a & b);  // NAND: 8'b01110111
        result = a ~^ b;    // XNOR: 8'b10011001

        // Shift operators
        result = a << 2;    // logical left shift
        result = a >> 2;    // logical right shift
        result = $signed(a) >>> 2;  // arithmetic right shift

        // Arithmetic
        result = a + b;
        result = a - b;
        result = a * b;     // synthesizable but expensive!
        result = a / b;     // not always synthesizable
        result = a % b;     // modulo

        // Reduction operators (reduce all bits)
        $display("&a = %b", &a);    // AND of all bits
        $display("|a = %b", |a);    // OR of all bits
        $display("^a = %b", ^a);    // XOR (parity)
        $display("~&a = %b", ~&a);  // NAND of all bits

        // Comparison
        $display("a == b: %b", a == b);
        $display("a != b: %b", a != b);
        $display("a < b: %b",  a < b);
        $display("a > b: %b",  a > b);
        $display("a <= b: %b", a <= b);
        $display("a >= b: %b", a >= b);

        // Logical (returns 0 or 1)
        $display("!a: %b", !a);
        $display("a && b: %b", a && b);
        $display("a || b: %b", a || b);

        // Conditional
        result = (a > b) ? a : b;   // max

        // Concatenation and replication
        result = {a[3:0], b[3:0]};  // concatenate lower nibbles
        result = {4{a[1:0]}};       // replicate: 4 copies of a[1:0]

        // Part select
        $display("a[7:4] = %b", a[7:4]);   // upper nibble
        $display("a[2] = %b", a[2]);        // single bit

        $finish;
    end
endmodule
```


---

# CHAPTER 6: TESTBENCH DESIGN


## Simulation and Verification

```verilog
// Testbench for adder module
`timescale 1ns / 1ps    // time unit / precision

module tb_adder;

    // Parameters
    parameter WIDTH = 8;
    parameter NUM_TESTS = 1000;

    // DUT (device under test) signals
    reg  [WIDTH-1:0] a, b;
    reg              cin;
    wire [WIDTH-1:0] sum;
    wire             cout;

    // Instantiate DUT
    adder #(.WIDTH(WIDTH)) dut (
        .a    (a),
        .b    (b),
        .cin  (cin),
        .sum  (sum),
        .cout (cout)
    );

    // Reference model
    function [WIDTH:0] ref_add;
        input [WIDTH-1:0] ra, rb;
        input             rc;
        begin
            ref_add = ra + rb + rc;
        end
    endfunction

    integer i, errors;
    reg [WIDTH:0] expected;

    // Test stimulus
    initial begin
        errors = 0;

        // Directed tests
        a = 0; b = 0; cin = 0;
        #10;
        if ({cout, sum} !== 9'b0)
            $display("FAIL: 0+0+0 = %b%b, expected 0", cout, sum);

        a = 8'hFF; b = 8'h01; cin = 0;
        #10;
        expected = ref_add(a, b, cin);
        if ({cout, sum} !== expected)
            $display("FAIL: FF+01 got %b%b, expected %b", cout, sum, expected);

        // Random tests
        for (i = 0; i < NUM_TESTS; i = i + 1) begin
            a   = $random;
            b   = $random;
            cin = $random;
            #10;
            expected = ref_add(a, b, cin);
            if ({cout, sum} !== expected) begin
                $display("FAIL at test %0d: %0d+%0d+%0d = %0d%0d, expected %0d",
                         i, a, b, cin, cout, sum, expected);
                errors = errors + 1;
            end
        end

        if (errors == 0)
            $display("PASSED all %0d tests", NUM_TESTS);
        else
            $display("FAILED %0d tests", errors);

        $finish;
    end

    // Waveform dump
    initial begin
        $dumpfile("waves.vcd");
        $dumpvars(0, tb_adder);
    end

    // Timeout watchdog
    initial begin
        #100000;
        $display("TIMEOUT!");
        $finish;
    end

endmodule
```


---

# CHAPTER 7: FINITE STATE MACHINES


## FSM Design

```verilog
// Mealy FSM — output depends on state AND input
module traffic_light (
    input  wire clk,
    input  wire rst_n,
    input  wire sensor,    // car detected
    output reg  [1:0] light // 00=red, 01=yellow, 10=green
);

    // State encoding
    localparam RED    = 2'd0;
    localparam YELLOW = 2'd1;
    localparam GREEN  = 2'd2;

    reg [1:0] state, next_state;
    reg [3:0] count;

    // State register
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= RED;
        else
            state <= next_state;
    end

    // Next state logic (combinational)
    always @(*) begin
        case (state)
            RED:    next_state = (count == 4'd10) ? GREEN  : RED;
            GREEN:  next_state = (count == 4'd8)  ? YELLOW : GREEN;
            YELLOW: next_state = (count == 4'd2)  ? RED    : YELLOW;
            default: next_state = RED;
        endcase
    end

    // Output logic
    always @(*) begin
        case (state)
            RED:    light = 2'b00;
            GREEN:  light = 2'b10;
            YELLOW: light = 2'b01;
            default: light = 2'b00;
        endcase
    end

    // Counter
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            count <= 0;
        else if (state != next_state)
            count <= 0;
        else
            count <= count + 1;
    end

endmodule
```


---

# CHAPTER 8: SYSTEM TASKS AND COMPILER DIRECTIVES


## System Tasks and Synthesis

```verilog
// System tasks (simulation)
$display("format string", args);    // print with newline
$write("format string", args);      // print without newline
$monitor("format string", args);    // print on change
$strobe("format string", args);     // print at end of timestep
$finish;                            // end simulation
$stop;                              // pause simulation
$time                               // current simulation time
$realtime                           // time as real
$random                             // pseudo-random 32-bit integer
$urandom                            // unsigned random
$urandom_range(max, min)            // random in range

// File operations
integer fid;
fid = $fopen("output.txt", "w");
$fdisplay(fid, "data: %0d", data);
$fclose(fid);

// Memory operations
$readmemh("data.hex", memory);      // load hex file into memory
$readmemb("data.bin", memory);      // load binary file
$writememh("out.hex", memory);      // write memory to hex file

// Timing checks
$setup(d, posedge clk, 2ns);
$hold(posedge clk, d, 1ns);

// Compiler directives (`define)
`define WIDTH 8
`define CLK_PERIOD 10
`ifdef DEBUG
    $display("Debug info");
`endif
`ifndef SYNTHESIS
    // simulation-only code
`endif
`include "header.v"
`timescale 1ns / 1ps

// Synthesis attributes (tool-specific)
// (* KEEP = "TRUE" *)
// (* DONT_TOUCH = "TRUE" *)
// synthesis translate_off / translate_on (Quartus)

// Commonly synthesized constructs:
// - Combinational: assign, always @(*) with if/case
// - Sequential: always @(posedge clk) with non-blocking <=
// - NOT synthesizable: initial, #delays, $display, real, time
// - Careful: integer division/modulo, dynamic bit selects

// Best practices:
// 1. Use non-blocking (<=) in clocked always blocks
// 2. Use blocking (=) in combinational always blocks
// 3. Default assignments at top of always blocks
// 4. Avoid latches: assign all outputs in all branches
// 5. One clock domain per always block
// 6. Reset all flip-flops
```
