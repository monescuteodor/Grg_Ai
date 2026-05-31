# Zig Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH ZIG


## Remarks

Zig is a systems programming language focused on robustness, optimality, and maintainability. Created by Andrew Kelley in 2016. Zig has no hidden control flow, no hidden allocations, no preprocessor, and no macros. It interoperates seamlessly with C and can compile C code.

Tools: `zig` (official compiler/build tool), `zls` (Zig Language Server).


## Hello World

```zig
// hello.zig
const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, {s}!\n", .{"World"});
}
```

```bash
zig run hello.zig          # compile and run
zig build-exe hello.zig    # compile to executable
zig test hello.zig         # run tests
zig fmt hello.zig          # format file
```


---

# CHAPTER 2: TYPES AND VARIABLES


## Zig Type System

```zig
const std = @import("std");

pub fn main() !void {
    // === INTEGER TYPES ===
    const i: i32 = -42;         // signed 32-bit
    const u: u32 = 42;          // unsigned 32-bit
    const big: i64 = 1_000_000; // underscores for readability
    const byte: u8 = 255;
    const usize_val: usize = 100; // pointer-sized unsigned

    // Arbitrary bit widths
    const i3_val: i3 = -4;      // 3-bit signed (-4 to 3)
    const u7_val: u7 = 127;     // 7-bit unsigned

    // Comptime integer (arbitrary precision)
    const big_int = 12345678901234567890;

    // === FLOAT TYPES ===
    const f: f64 = 3.14;
    const f32_val: f32 = 1.5;
    const f128_val: f128 = 1.0;

    // === BOOLEAN ===
    const b: bool = true;
    const flag = false;  // type inferred

    // === OPTIONAL ===
    const maybe: ?i32 = null;
    const has_val: ?i32 = 42;
    if (has_val) |v| {
        std.debug.print("Value: {}\n", .{v});
    }

    // Unwrap optional (panic if null)
    const val = has_val.?;

    // orelse — default value
    const result = maybe orelse 0;

    // === ERROR UNION ===
    const err_union: anyerror!i32 = 42;
    const err_result = err_union catch 0;  // default on error

    // === VOID AND NULL ===
    const nothing: void = {};
    const null_ptr: ?*i32 = null;

    // === COMPTIME ===
    comptime var ct: i32 = 10;
    comptime {
        ct = ct * 2;  // evaluated at compile time
    }

    // Type reflection
    std.debug.print("Type of i: {}\n", .{@TypeOf(i)});
    std.debug.print("Size of i32: {} bytes\n", .{@sizeOf(i32)});
    std.debug.print("Bits of f64: {}\n", .{@bitSizeOf(f64)});

    _ = i; _ = u; _ = big; _ = byte; _ = usize_val;
    _ = i3_val; _ = u7_val; _ = big_int;
    _ = f; _ = f32_val; _ = f128_val;
    _ = b; _ = flag; _ = maybe; _ = val; _ = result;
    _ = err_result; _ = nothing; _ = null_ptr;
}
```


---

# CHAPTER 3: CONTROL FLOW


## Control Structures

```zig
const std = @import("std");

pub fn main() !void {
    const x: i32 = 10;

    // === IF / ELSE ===
    if (x > 0) {
        std.debug.print("positive\n", .{});
    } else if (x == 0) {
        std.debug.print("zero\n", .{});
    } else {
        std.debug.print("negative\n", .{});
    }

    // If as expression
    const sign: i32 = if (x > 0) 1 else if (x < 0) -1 else 0;

    // If with optional capture
    const maybe: ?i32 = 42;
    if (maybe) |v| {
        std.debug.print("got {}\n", .{v});
    } else {
        std.debug.print("null\n", .{});
    }

    // If with error capture
    const result: anyerror!i32 = 5;
    if (result) |v| {
        std.debug.print("ok: {}\n", .{v});
    } else |err| {
        std.debug.print("err: {}\n", .{err});
    }

    // === SWITCH ===
    const day: u8 = 3;
    switch (day) {
        1 => std.debug.print("Monday\n", .{}),
        2 => std.debug.print("Tuesday\n", .{}),
        3, 4, 5 => std.debug.print("Wed-Fri\n", .{}),
        6...7 => std.debug.print("Weekend\n", .{}),  // range
        else => std.debug.print("Invalid\n", .{}),
    }

    // Switch as expression
    const name = switch (day) {
        1 => "Monday",
        2 => "Tuesday",
        else => "Other",
    };

    // === LOOPS ===

    // While loop
    var i: u32 = 0;
    while (i < 5) : (i += 1) {
        std.debug.print("{} ", .{i});
    }
    std.debug.print("\n", .{});

    // While with continue expression
    var j: u32 = 0;
    while (j < 10) : (j += 2) {
        if (j == 6) continue;
        if (j == 8) break;
        std.debug.print("{} ", .{j});
    }

    // For loop (over slice/array)
    const arr = [_]i32{ 10, 20, 30, 40, 50 };
    for (arr) |val| {
        std.debug.print("{} ", .{val});
    }

    // For with index
    for (arr, 0..) |val, idx| {
        std.debug.print("[{}]={} ", .{ idx, val });
    }

    // Inline for (comptime)
    inline for ([_]type{ u8, u16, u32 }) |T| {
        std.debug.print("size of {}: {}\n", .{ T, @sizeOf(T) });
    }

    _ = sign; _ = name;
}
```


---

# CHAPTER 4: FUNCTIONS AND ERROR HANDLING


## Functions and Errors

```zig
const std = @import("std");

// === BASIC FUNCTION ===
fn add(a: i32, b: i32) i32 {
    return a + b;
}

// === ERROR HANDLING ===
const MathError = error{
    DivisionByZero,
    Overflow,
};

fn divide(a: f64, b: f64) MathError!f64 {
    if (b == 0.0) return MathError.DivisionByZero;
    return a / b;
}

// Combining error sets
fn parse(s: []const u8) (std.fmt.ParseIntError || MathError)!i32 {
    const n = try std.fmt.parseInt(i32, s, 10);
    if (n < 0) return MathError.Overflow;
    return n;
}

// === OPTIONALS ===
fn find(haystack: []const u8, needle: u8) ?usize {
    for (haystack, 0..) |c, i| {
        if (c == needle) return i;
    }
    return null;
}

// === COMPTIME FUNCTIONS ===
fn max(comptime T: type, a: T, b: T) T {
    return if (a > b) a else b;
}

// === VARIADIC-LIKE (using slices) ===
fn sum(nums: []const i32) i32 {
    var total: i32 = 0;
    for (nums) |n| total += n;
    return total;
}

// === FUNCTION POINTERS ===
fn apply(f: *const fn (i32) i32, x: i32) i32 {
    return f(x);
}
fn double(x: i32) i32 { return x * 2; }

pub fn main() !void {
    // Basic call
    std.debug.print("add: {}\n", .{add(3, 4)});

    // try — propagate error up
    const result = try divide(10.0, 3.0);
    std.debug.print("divide: {d:.2}\n", .{result});

    // catch — handle error
    const r2 = divide(1.0, 0.0) catch |err| blk: {
        std.debug.print("error: {}\n", .{err});
        break :blk 0.0;
    };
    _ = r2;

    // errdefer — cleanup on error
    // (see memory chapter)

    // Optional
    const pos = find("hello", 'l');
    if (pos) |p| std.debug.print("found at {}\n", .{p});

    // Comptime generic
    std.debug.print("max(3,5): {}\n", .{max(i32, 3, 5)});
    std.debug.print("max(1.5,2.5): {}\n", .{max(f64, 1.5, 2.5)});

    // Slice
    const nums = [_]i32{ 1, 2, 3, 4, 5 };
    std.debug.print("sum: {}\n", .{sum(&nums)});

    // Function pointer
    std.debug.print("apply: {}\n", .{apply(double, 7)});
}
```


---

# CHAPTER 5: STRUCTS, ENUMS, AND UNIONS


## Composite Types

```zig
const std = @import("std");

// === STRUCT ===
const Point = struct {
    x: f64,
    y: f64,

    // Method
    pub fn distance(self: Point, other: Point) f64 {
        const dx = self.x - other.x;
        const dy = self.y - other.y;
        return @sqrt(dx * dx + dy * dy);
    }

    // Static method (no self)
    pub fn origin() Point {
        return .{ .x = 0, .y = 0 };
    }
};

// Packed struct (exact memory layout)
const Flags = packed struct {
    read: bool,
    write: bool,
    execute: bool,
    _padding: u5 = 0,
};

// === ENUM ===
const Direction = enum {
    north,
    south,
    east,
    west,

    pub fn opposite(self: Direction) Direction {
        return switch (self) {
            .north => .south,
            .south => .north,
            .east => .west,
            .west => .east,
        };
    }
};

// Enum with explicit values
const Color = enum(u8) {
    red = 1,
    green = 2,
    blue = 4,
    white = 7,
};

// === TAGGED UNION ===
const Shape = union(enum) {
    circle: f64,           // radius
    rectangle: struct { w: f64, h: f64 },
    triangle: struct { base: f64, height: f64 },

    pub fn area(self: Shape) f64 {
        return switch (self) {
            .circle => |r| std.math.pi * r * r,
            .rectangle => |rect| rect.w * rect.h,
            .triangle => |tri| 0.5 * tri.base * tri.height,
        };
    }
};

pub fn main() !void {
    // Struct
    const p1 = Point{ .x = 0, .y = 0 };
    const p2 = Point{ .x = 3, .y = 4 };
    std.debug.print("distance: {}\n", .{p1.distance(p2)});
    std.debug.print("origin: {}\n", .{Point.origin()});

    // Struct init shorthand
    const p3: Point = .{ .x = 1, .y = 2 };
    _ = p3;

    // Packed struct
    const flags = Flags{ .read = true, .write = true, .execute = false };
    std.debug.print("flags size: {} byte\n", .{@sizeOf(Flags)});
    _ = flags;

    // Enum
    const dir = Direction.north;
    std.debug.print("opposite of north: {}\n", .{dir.opposite()});
    std.debug.print("color red: {}\n", .{@intFromEnum(Color.red)});

    // Tagged union
    const s1 = Shape{ .circle = 5.0 };
    const s2 = Shape{ .rectangle = .{ .w = 4.0, .h = 6.0 } };
    std.debug.print("circle area: {d:.2}\n", .{s1.area()});
    std.debug.print("rect area: {d:.2}\n", .{s2.area()});
}
```


---

# CHAPTER 6: MEMORY AND ALLOCATORS


## Memory Management

```zig
const std = @import("std");

pub fn main() !void {
    // === ALLOCATORS ===

    // General purpose (debug mode: detects leaks)
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // Arena allocator (free everything at once)
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const arena_alloc = arena.allocator();

    // Fixed buffer allocator (no heap)
    var buf: [1024]u8 = undefined;
    var fba = std.heap.FixedBufferAllocator.init(&buf);
    const fba_alloc = fba.allocator();

    // === ALLOCATE/FREE ===
    const p = try allocator.create(i32);  // alloc single item
    defer allocator.destroy(p);
    p.* = 42;
    std.debug.print("p: {}\n", .{p.*});

    // Allocate slice
    const nums = try allocator.alloc(i32, 10);
    defer allocator.free(nums);
    for (nums, 0..) |*n, i| n.* = @intCast(i * i);
    std.debug.print("nums[3]: {}\n", .{nums[3]});

    // Realloc
    const more = try allocator.realloc(nums, 20);
    defer allocator.free(more);

    // === ARRAYLISTS ===
    var list = std.ArrayList(i32).init(allocator);
    defer list.deinit();

    try list.append(1);
    try list.append(2);
    try list.append(3);
    try list.appendSlice(&[_]i32{ 4, 5, 6 });
    std.debug.print("list: {any}\n", .{list.items});

    // === HASHMAPS ===
    var map = std.StringHashMap(i32).init(allocator);
    defer map.deinit();

    try map.put("one", 1);
    try map.put("two", 2);
    try map.put("three", 3);

    if (map.get("two")) |v| {
        std.debug.print("two = {}\n", .{v});
    }

    var it = map.iterator();
    while (it.next()) |entry| {
        std.debug.print("{s}: {}\n", .{ entry.key_ptr.*, entry.value_ptr.* });
    }

    // errdefer — cleanup if function errors after allocation
    _ = arena_alloc;
    _ = fba_alloc;
}

// Defer and errdefer example
fn processFile(allocator: std.mem.Allocator, path: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();  // always runs

    const size = (try file.stat()).size;
    const buf = try allocator.alloc(u8, size);
    errdefer allocator.free(buf);  // only runs on error

    _ = try file.readAll(buf);
    return buf;
}
```


---

# CHAPTER 7: POINTERS AND SLICES


## Low-Level Memory

```zig
const std = @import("std");

pub fn main() !void {
    // === POINTERS ===
    var x: i32 = 10;
    const ptr: *i32 = &x;  // pointer to x
    ptr.* = 20;             // dereference and assign
    std.debug.print("x = {}\n", .{x});  // 20

    // Optional pointer
    var opt_ptr: ?*i32 = null;
    opt_ptr = &x;
    if (opt_ptr) |p| {
        std.debug.print("opt: {}\n", .{p.*});
    }

    // Many-item pointer (unsafe, no length)
    var arr = [_]i32{ 1, 2, 3, 4, 5 };
    const many_ptr: [*]i32 = &arr;
    std.debug.print("many_ptr[2] = {}\n", .{many_ptr[2]});

    // Const pointer (can't modify through it)
    const const_ptr: *const i32 = &x;
    std.debug.print("const: {}\n", .{const_ptr.*});

    // === SLICES ===
    // Slice = pointer + length
    const slice: []i32 = arr[1..4];  // elements 1,2,3
    std.debug.print("slice.len = {}\n", .{slice.len});
    std.debug.print("slice[0] = {}\n", .{slice[0]});

    // Sentinel-terminated slice (C strings)
    const cstr: [*:0]const u8 = "hello";
    const str_slice = std.mem.span(cstr);  // convert to []const u8
    std.debug.print("str: {s}\n", .{str_slice});

    // === STRING OPERATIONS ===
    const s1: []const u8 = "Hello";
    const s2: []const u8 = "World";
    std.debug.print("eq: {}\n", .{std.mem.eql(u8, s1, s2)});
    std.debug.print("len: {}\n", .{s1.len});

    // String formatting
    var buf: [100]u8 = undefined;
    const formatted = try std.fmt.bufPrint(&buf, "{s} {s}!", .{ s1, s2 });
    std.debug.print("{s}\n", .{formatted});

    // === COMPTIME ARRAYS ===
    const static_arr = [5]i32{ 1, 2, 3, 4, 5 };
    const static_slice: []const i32 = &static_arr;
    std.debug.print("static: {any}\n", .{static_slice});

    // @ptrCast and @alignCast (unsafe, for C interop)
    const bytes: []const u8 = "AB";
    const uint: *const u16 = @ptrCast(@alignCast(bytes.ptr));
    std.debug.print("cast: 0x{X}\n", .{uint.*});
}
```


---

# CHAPTER 8: BUILD SYSTEM AND ADVANCED


## Zig Build and Advanced Features

```zig
// build.zig — Zig's build system
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Executable
    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    // Link C library
    exe.linkLibC();
    exe.linkSystemLibrary("SDL2");

    b.installArtifact(exe);

    // Run step
    const run_cmd = b.addRunArtifact(exe);
    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);

    // Test step
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    const test_step = b.step("test", "Run tests");
    test_step.dependOn(&b.addRunArtifact(unit_tests).step);
}
```

```zig
// === COMPTIME METAPROGRAMMING ===
const std = @import("std");

// Comptime struct generation
fn Vec(comptime N: usize, comptime T: type) type {
    return struct {
        data: [N]T,

        const Self = @This();

        pub fn dot(self: Self, other: Self) T {
            var result: T = 0;
            for (self.data, other.data) |a, b| result += a * b;
            return result;
        }
    };
}

// Testing
test "basic math" {
    try std.testing.expect(1 + 1 == 2);
    try std.testing.expectEqual(@as(i32, 10), add(3, 7));
}

test "Vec dot product" {
    const V3 = Vec(3, f64);
    const v1 = V3{ .data = .{ 1, 2, 3 } };
    const v2 = V3{ .data = .{ 4, 5, 6 } };
    try std.testing.expectEqual(@as(f64, 32), v1.dot(v2));
}

fn add(a: i32, b: i32) i32 { return a + b; }

// === C INTEROP ===
const c = @cImport({
    @cInclude("stdio.h");
    @cInclude("stdlib.h");
});

pub fn c_interop() void {
    _ = c.printf("Hello from C!\n");
    const p = c.malloc(100);
    defer c.free(p);
}

// === ASYNC (pre-0.12 style) ===
// Zig async is being redesigned; use threads for concurrency:
pub fn threaded() !void {
    const handle = try std.Thread.spawn(.{}, worker, .{42});
    handle.join();
}
fn worker(id: i32) void {
    std.debug.print("worker {}\n", .{id});
}

// === CROSS COMPILATION ===
// zig build -Dtarget=aarch64-linux-musl
// zig build -Dtarget=x86_64-windows-gnu
// zig build -Dtarget=wasm32-wasi

// zig targets  -- list all supported targets
```
