# VHDL Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH VHDL


## Remarks

VHDL (VHSIC Hardware Description Language) is an IEEE-standard (1076) hardware description language used for digital design, simulation, and synthesis. It is strongly typed, verbose, and precise. VHDL is used extensively in defense, aerospace, and European industry. Common in FPGA/ASIC design alongside Verilog.

Tools: GHDL (open-source simulator), Xilinx Vivado, Intel Quartus, ModelSim, Sigasi (IDE).


## Hello World / Testbench

```vhdl
-- hello.vhd — simulation only
library ieee;
use ieee.std_logic_1164.all;

entity hello is
end entity hello;

architecture sim of hello is
begin
    process
    begin
        report "Hello, World!";
        report "Hello, VHDL!" severity note;
        wait;  -- stop simulation
    end process;
end architecture sim;
```

```bash
ghdl -a hello.vhd          # analyze
ghdl -e hello              # elaborate
ghdl -r hello              # run
# Output: hello.vhd:8:9:@0ms:(report note): Hello, World!
```


---

# CHAPTER 2: TYPES AND DECLARATIONS


## VHDL Type System

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity types_demo is
end entity;

architecture rtl of types_demo is

    -- Standard logic types
    signal a    : std_logic;           -- single bit: 'U','X','0','1','Z','W','L','H','-'
    signal bus8 : std_logic_vector(7 downto 0);   -- 8-bit vector
    signal bus32: std_logic_vector(31 downto 0);  -- 32-bit vector
    signal uns  : unsigned(7 downto 0);           -- unsigned arithmetic
    signal sgn  : signed(7 downto 0);             -- signed arithmetic

    -- Built-in types
    signal b    : boolean := false;
    signal i    : integer := 0;
    signal n    : natural := 0;   -- integer >= 0
    signal p    : positive := 1; -- integer > 0
    signal r    : real := 3.14;
    signal c    : character := 'A';
    signal s    : string := "hello";
    signal t    : time := 10 ns;

    -- Constrained integer
    signal age  : integer range 0 to 150 := 0;

    -- Enumeration
    type color_t is (red, green, blue, yellow);
    signal color : color_t := red;

    -- FSM state
    type state_t is (idle, fetch, decode, execute, writeback);
    signal state : state_t := idle;

    -- Array types
    type byte_array is array (natural range <>) of std_logic_vector(7 downto 0);
    type matrix_4x4 is array (0 to 3, 0 to 3) of integer;

    -- Record type
    type point_t is record
        x : integer;
        y : integer;
    end record;

    -- Constants
    constant CLK_FREQ  : integer := 100_000_000;  -- 100 MHz
    constant CLK_PERIOD: time := 10 ns;
    constant MAX_VAL   : unsigned(7 downto 0) := x"FF";

    -- Aliases
    alias clk_period : time is CLK_PERIOD;

begin
    -- Conversion examples
    -- std_logic_vector <-> unsigned <-> integer
    -- unsigned(bus8)                  -- slv to unsigned
    -- std_logic_vector(uns)           -- unsigned to slv
    -- to_integer(uns)                 -- unsigned to integer
    -- to_unsigned(42, 8)              -- integer to unsigned (8 bits)
    -- to_signed(-10, 8)               -- integer to signed (8 bits)

    process
    begin
        a <= '1';
        bus8 <= x"AB";           -- hex literal
        bus8 <= "10101011";      -- binary literal
        bus8 <= (others => '0'); -- all zeros
        uns <= to_unsigned(170, 8);
        wait;
    end process;

end architecture;
```


---

# CHAPTER 3: ENTITIES AND ARCHITECTURES


## Design Units

```vhdl
-- Entity: interface (ports)
entity adder is
    generic (
        WIDTH : natural := 8    -- parameterizable
    );
    port (
        a    : in  std_logic_vector(WIDTH-1 downto 0);
        b    : in  std_logic_vector(WIDTH-1 downto 0);
        cin  : in  std_logic;
        sum  : out std_logic_vector(WIDTH-1 downto 0);
        cout : out std_logic
    );
end entity adder;

-- Architecture: implementation
architecture rtl of adder is
    signal result : unsigned(WIDTH downto 0);
begin
    result <= ('0' & unsigned(a)) + ('0' & unsigned(b)) + ("" & cin);
    sum  <= std_logic_vector(result(WIDTH-1 downto 0));
    cout <= result(WIDTH);
end architecture rtl;

-- Multiple architectures for same entity
architecture behavioral of adder is
begin
    process(a, b, cin)
        variable sum_v : unsigned(WIDTH downto 0);
    begin
        sum_v := ('0' & unsigned(a)) + ('0' & unsigned(b)) + ("" & cin);
        sum  <= std_logic_vector(sum_v(WIDTH-1 downto 0));
        cout <= sum_v(WIDTH);
    end process;
end architecture behavioral;

-- Structural (instantiation)
entity top is
    port (
        clk  : in  std_logic;
        rst  : in  std_logic;
        data : out std_logic_vector(7 downto 0)
    );
end entity;

architecture structural of top is

    -- Component declaration (import)
    component adder
        generic (WIDTH : natural);
        port (
            a, b : in  std_logic_vector(WIDTH-1 downto 0);
            cin  : in  std_logic;
            sum  : out std_logic_vector(WIDTH-1 downto 0);
            cout : out std_logic
        );
    end component;

    signal a_s, b_s, s_s : std_logic_vector(7 downto 0);
    signal c_s : std_logic;

begin

    -- Instantiation
    u_add : adder
        generic map (WIDTH => 8)
        port map (
            a    => a_s,
            b    => b_s,
            cin  => '0',
            sum  => s_s,
            cout => c_s
        );

end architecture;
```


---

# CHAPTER 4: CONCURRENT STATEMENTS


## Concurrent Signal Assignments

```vhdl
architecture rtl of concurrent_demo is
    signal a, b, c, y : std_logic;
    signal sel : std_logic_vector(1 downto 0);
    signal data_in : std_logic_vector(7 downto 0);
    signal data_out : std_logic_vector(7 downto 0);
begin

    -- Simple concurrent assignment
    y <= a and b;
    y <= a or b or c;
    y <= not a;

    -- Conditional signal assignment (when-else)
    y <= a when sel = "00" else
         b when sel = "01" else
         c when sel = "10" else
         '0';

    -- Selected signal assignment (with-select)
    with sel select
        y <= a when "00",
             b when "01",
             c when "10",
             '0' when others;

    -- Generate statements (for loops in hardware)
    -- Replicating a unit N times
    gen_reg : for i in 0 to 7 generate
        -- create 8 instances
        data_out(i) <= data_in(i) and '1';
    end generate;

    -- Conditional generate
    gen_opt : if WIDTH > 8 generate
        -- extra logic for wide buses
    else generate
        -- narrow bus logic
    end generate;

    -- Process statement (concurrent, but sequential inside)
    proc_clk : process(a, b, c)
    begin
        if a = '1' then
            y <= b;
        else
            y <= c;
        end if;
    end process;

end architecture;
```


---

# CHAPTER 5: SEQUENTIAL LOGIC


## Process-Based Sequential Design

```vhdl
architecture rtl of seq_demo is
    signal clk, rst_n : std_logic;
    signal q          : std_logic;
    signal count      : unsigned(7 downto 0);

    -- State machine
    type state_t is (idle, run, done);
    signal state, next_state : state_t;
begin

    -- D flip-flop with synchronous reset
    ff_sync : process(clk)
    begin
        if rising_edge(clk) then
            if rst_n = '0' then
                q <= '0';
            else
                q <= d;
            end if;
        end if;
    end process;

    -- D flip-flop with asynchronous reset
    ff_async : process(clk, rst_n)
    begin
        if rst_n = '0' then
            q <= '0';
        elsif rising_edge(clk) then
            q <= d;
        end if;
    end process;

    -- 8-bit up counter
    counter : process(clk, rst_n)
    begin
        if rst_n = '0' then
            count <= (others => '0');
        elsif rising_edge(clk) then
            if en = '1' then
                count <= count + 1;
            end if;
        end if;
    end process;

    -- 2-process FSM style (most recommended)
    -- Process 1: state register
    state_reg : process(clk, rst_n)
    begin
        if rst_n = '0' then
            state <= idle;
        elsif rising_edge(clk) then
            state <= next_state;
        end if;
    end process;

    -- Process 2: next state and output logic (combinational)
    comb : process(state, start, done_flag)
    begin
        -- Default assignments (avoid latches)
        next_state <= state;
        busy       <= '0';
        result_en  <= '0';

        case state is
            when idle =>
                if start = '1' then
                    next_state <= run;
                end if;
            when run =>
                busy <= '1';
                if done_flag = '1' then
                    next_state <= done;
                end if;
            when done =>
                result_en  <= '1';
                next_state <= idle;
            when others =>
                next_state <= idle;
        end case;
    end process;

end architecture;
```


---

# CHAPTER 6: SUBPROGRAMS AND PACKAGES


## Functions, Procedures, and Packages

```vhdl
-- Package definition
package math_pkg is

    function log2_ceil(n : positive) return natural;
    function is_power_of_2(n : natural) return boolean;

    procedure swap(signal a : inout std_logic_vector;
                   signal b : inout std_logic_vector);

    constant PI : real := 3.14159265358979;

end package;

package body math_pkg is

    function log2_ceil(n : positive) return natural is
        variable r : natural := 0;
        variable v : natural := 1;
    begin
        while v < n loop
            v := v * 2;
            r := r + 1;
        end loop;
        return r;
    end function;

    function is_power_of_2(n : natural) return boolean is
    begin
        return n /= 0 and (n and (n-1)) = 0;
    end function;

    procedure swap(signal a : inout std_logic_vector;
                   signal b : inout std_logic_vector) is
        variable tmp : std_logic_vector(a'range);
    begin
        tmp := a;
        a   <= b;
        b   <= tmp;
    end procedure;

end package body;

-- Using the package
library ieee;
use ieee.std_logic_1164.all;
use work.math_pkg.all;

entity use_pkg is
end entity;

architecture rtl of use_pkg is
    constant ADDR_BITS : natural := log2_ceil(256);   -- 8
begin
    process
    begin
        report "log2(256) = " & natural'image(ADDR_BITS);
        report "is_power_of_2(64) = " & boolean'image(is_power_of_2(64));
        wait;
    end process;
end architecture;
```


---

# CHAPTER 7: SIMULATION AND TESTBENCHES


## Writing Testbenches

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_adder is
end entity;

architecture sim of tb_adder is

    constant WIDTH     : natural := 8;
    constant CLK_PERIOD: time := 10 ns;

    -- DUT signals
    signal a, b : std_logic_vector(WIDTH-1 downto 0);
    signal cin  : std_logic;
    signal sum  : std_logic_vector(WIDTH-1 downto 0);
    signal cout : std_logic;

    -- Clock and reset
    signal clk   : std_logic := '0';
    signal rst_n : std_logic := '0';

begin

    -- Clock generation
    clk <= not clk after CLK_PERIOD / 2;

    -- DUT instantiation
    u_dut : entity work.adder
        generic map (WIDTH => WIDTH)
        port map (
            a    => a,
            b    => b,
            cin  => cin,
            sum  => sum,
            cout => cout
        );

    -- Test stimulus
    stim : process

        procedure apply_test (
            a_v, b_v : in natural;
            c_v      : in std_logic;
            expected : in natural
        ) is
            variable result : unsigned(WIDTH downto 0);
        begin
            a   <= std_logic_vector(to_unsigned(a_v, WIDTH));
            b   <= std_logic_vector(to_unsigned(b_v, WIDTH));
            cin <= c_v;
            wait for CLK_PERIOD;
            result := unsigned(cout & sum);
            if result /= to_unsigned(expected, WIDTH+1) then
                report "FAIL: " & natural'image(a_v) & "+" &
                       natural'image(b_v) & " expected " &
                       natural'image(expected) & " got " &
                       natural'image(to_integer(result))
                    severity error;
            end if;
        end procedure;

    begin
        -- Reset
        rst_n <= '0';
        a <= (others => '0');
        b <= (others => '0');
        cin <= '0';
        wait for 2 * CLK_PERIOD;
        rst_n <= '1';
        wait for CLK_PERIOD;

        -- Tests
        apply_test(0, 0, '0', 0);
        apply_test(255, 1, '0', 256);
        apply_test(127, 127, '1', 255);

        report "Simulation complete" severity note;
        wait;  -- stop simulation
    end process;

end architecture;
```


---

# CHAPTER 8: NUMERIC PACKAGES AND ADVANCED


## Advanced VHDL

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;       -- preferred (std)
-- use ieee.std_logic_arith.all;    -- older, avoid
-- use ieee.std_logic_unsigned.all; -- older, avoid

-- numeric_std types and operations
-- unsigned(n downto 0)
-- signed(n downto 0)

-- Arithmetic
-- u1 + u2, u1 - u2, u1 * u2
-- Comparison: u1 < u2, u1 = u2, etc.
-- Shift: shift_left(u, n), shift_right(u, n)
-- Rotate: rotate_left(u, n), rotate_right(u, n)
-- Resize: resize(u, new_width)  -- zero/sign extend

-- Conversions
-- to_integer(u)               -- unsigned -> integer
-- to_unsigned(n, width)       -- integer -> unsigned
-- to_signed(n, width)         -- integer -> signed
-- unsigned(slv)               -- slv -> unsigned
-- signed(slv)                 -- slv -> signed
-- std_logic_vector(u)         -- unsigned/signed -> slv

-- Concatenation
-- signal result : std_logic_vector(15 downto 0);
-- result <= a & b;  -- concat 8+8 = 16 bits

-- Bit manipulation
-- bus8(7)          -- single bit
-- bus8(7 downto 4) -- slice (returns std_logic_vector)
-- bus8(7) <= '1';  -- assign single bit
-- bus8 <= (others => '0');  -- all zeros
-- bus8 <= (7 => '1', others => '0');  -- bit 7 set

-- VHDL 2008 features
-- Matching case (case?)
-- Conditional signal assignment (inline when)
-- Package instantiation
-- Enhanced port maps
-- Bit string literals: b"1010_0101"

-- Synthesis attributes (Xilinx example)
-- attribute keep : string;
-- attribute keep of sig_name : signal is "true";

-- GHDL simulation
-- ghdl -a --std=08 file.vhd   (VHDL 2008)
-- ghdl -e --std=08 entity_name
-- ghdl -r --std=08 entity_name --vcd=waves.vcd
-- gtkwave waves.vcd

-- File I/O in simulation
-- use std.textio.all;
-- file f : text open write_mode is "output.txt";
-- variable line_var : line;
-- write(line_var, string'("Hello"));
-- writeline(f, line_var);
```
