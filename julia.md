# Julia Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH JULIA


## Remarks

Julia is a high-level, high-performance, dynamic programming language for technical computing. It combines the ease of Python with the speed of C through just-in-time compilation. Julia excels at numerical analysis, scientific computing, machine learning, and data science.

Tools: julia REPL, Pkg package manager, Pluto/Jupyter notebooks, VS Code with Julia extension.


## Hello World

```julia
# hello.jl
println("Hello, World!")
println("Hello, $(\"Julia\")!")
@printf("Hello, %s!\n", "Julia")

# REPL usage
# julia
# julia> println("Hello!")
```

```bash
julia hello.jl
julia --project=. hello.jl
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables and Types

```julia
# Variables (dynamically typed, can annotate)
x = 42
y = 3.14
s = "Hello"
b = true
c = 'A'           # Char (single quotes)

# Type annotations
x::Int64 = 42
y::Float64 = 3.14

# Multiple assignment
a, b, c = 1, 2, 3
a, b = b, a    # swap

# Constants
const MAX = 100
const PI_APPROX = 3.14159

# Integer types
n8  = Int8(127)
n16 = Int16(1000)
n32 = Int32(1_000_000)
n64 = Int64(1_000_000_000)
u8  = UInt8(255)

# Float types
f32 = Float32(3.14)
f64 = Float64(3.14159265358979)
f16 = Float16(3.14)

# BigInt and BigFloat
big_n = big"123456789012345678901234567890"
big_f = BigFloat("3.141592653589793238462643383279")

# Complex numbers
z = 3 + 4im
println(real(z), " ", imag(z))
println(abs(z))    # 5.0

# Rational numbers
r = 3//4
println(numerator(r), denominator(r))
println(r + 1//4)   # 1//1

# typeof and isa
println(typeof(42))      # Int64
println(typeof(3.14))    # Float64
println(isa(42, Integer))  # true
println(42 isa Number)     # true

# Type conversion
convert(Float64, 42)
Float64(42)
Int64(3.14)
parse(Int64, "42")
parse(Float64, "3.14")
string(42)
```


---

# CHAPTER 3: COLLECTIONS


## Arrays, Tuples, Dicts, and Sets

```julia
# Arrays (1-indexed!)
arr = [1, 2, 3, 4, 5]
mat = [1 2 3; 4 5 6; 7 8 9]    # 3x3 matrix (no commas between cols)

# Type-annotated
ints = Int64[1, 2, 3]
floats = Float64[1.0, 2.0, 3.0]

# Access (1-based)
println(arr[1])       # 1
println(arr[end])     # 5
println(arr[2:4])     # [2, 3, 4]
println(mat[2, 3])    # 6
println(mat[:, 2])    # second column

# Modify
push!(arr, 6)
pop!(arr)
pushfirst!(arr, 0)
popfirst!(arr)
insert!(arr, 2, 99)
deleteat!(arr, 2)
append!(arr, [10, 11, 12])

# Array functions
length(arr)
size(mat)         # (3, 3)
size(mat, 1)      # 3 rows
ndims(mat)        # 2
sum(arr)
prod(arr)
minimum(arr)
maximum(arr)
sort(arr)
sort(arr, rev=true)
reverse(arr)
unique([1,2,2,3,3])

# Array comprehensions
squares = [x^2 for x in 1:10]
evens   = [x for x in 1:20 if x % 2 == 0]
matrix_comp = [i*j for i in 1:3, j in 1:3]

# Vectorized operations (broadcast with .)
arr2 = [1, 2, 3, 4, 5]
arr2 .* 2        # element-wise multiply
arr2 .^ 2        # element-wise square
sqrt.(arr2)      # element-wise sqrt
arr2 .> 3        # element-wise comparison

# Tuples (immutable, value types)
t = (1, "hello", 3.14)
println(t[1])    # 1

# Named tuples
nt = (name = "Alice", age = 30)
println(nt.name)
println(nt[:age])

# Dictionaries
d = Dict("name" => "Alice", "age" => 30)
d["city"] = "NYC"
delete!(d, "age")
haskey(d, "name")   # true
get(d, "missing", "default")   # "default"
keys(d); values(d)

for (k, v) in d
    println("$k: $v")
end

# Sets
s = Set([1, 2, 3, 2, 1])
push!(s, 4)
delete!(s, 1)
in(2, s)           # true
union(s, Set([5, 6]))
intersect(s, Set([2, 3, 7]))
```


---

# CHAPTER 4: CONTROL FLOW


## Flow Control

```julia
# if/elseif/else
x = 10
if x > 0
    println("positive")
elseif x == 0
    println("zero")
else
    println("negative")
end

# Ternary
label = x > 0 ? "pos" : "non-pos"

# Short-circuit
x > 0 && println("positive")
x < 0 || println("not negative")

# for loop
for i in 1:10
    print("$i ")
end
println()

for i in 1:2:10   # step 2
    print("$i ")
end

for item in ["a", "b", "c"]
    println(item)
end

for (i, v) in enumerate([10, 20, 30])
    println("$i: $v")
end

# while loop
n = 1
while n < 100
    n *= 2
end
println(n)  # 128

# break / continue
for i in 1:10
    i == 5 && break
    i % 2 == 0 && continue
    print("$i ")
end

# Nested loop control with @label / @goto (rarely needed)
# Better: extract to function and use return

# try/catch/finally
try
    error("something went wrong")
catch e
    println("Caught: $e")
finally
    println("cleanup")
end

# try with specific exception type
try
    parse(Int, "not a number")
catch e::ArgumentError
    println("ArgumentError: ", e.msg)
end

# begin...end block
result = begin
    a = 10
    b = 20
    a + b    # last expression is the value
end
println(result)   # 30

# let block (local scope)
y = let x = 5
    x * x
end
```


---

# CHAPTER 5: FUNCTIONS


## Functions

```julia
# Basic function
function add(a, b)
    return a + b
end

# Short form
mul(a, b) = a * b
square(x) = x^2

# Anonymous functions
f = x -> x^2
g = (x, y) -> x + y

# Default arguments
function greet(name, greeting="Hello")
    println("$greeting, $name!")
end
greet("Alice")
greet("Bob", "Hi")

# Keyword arguments
function create_user(; name, age=0, city="Unknown")
    (name=name, age=age, city=city)
end
create_user(name="Alice", age=30)

# Variadic functions
function sum_all(nums...)
    sum(nums)
end
sum_all(1, 2, 3, 4, 5)

# Multiple return values
function minmax(v)
    return minimum(v), maximum(v)
end
lo, hi = minmax([3,1,4,1,5,9])

# Type annotations
function typed_add(a::Int, b::Int)::Int
    a + b
end

# Higher-order functions
function apply(f, x)
    f(x)
end
apply(sqrt, 16)   # 4.0

# map, filter, reduce
nums = 1:10
map(x -> x^2, nums)
filter(iseven, nums)
reduce(+, nums)   # sum

# do-block syntax
result = map(1:5) do x
    x^2 + 1
end

# Closures
function make_counter()
    count = 0
    function increment()
        count += 1
        count
    end
end
c = make_counter()
c(); c(); c()   # 1, 2, 3

# Function composition
double = x -> x * 2
inc    = x -> x + 1
double_then_inc = inc ∘ double   # ∘ = \circ
double_then_inc(5)   # 11

# Broadcasting (vectorize any function)
f.(1:5)         # apply f to each element
sin.(0:0.1:π)
```


---

# CHAPTER 6: TYPES AND MULTIPLE DISPATCH


## Type System

```julia
# Abstract types
abstract type Animal end
abstract type Pet <: Animal end

# Concrete structs
struct Dog <: Pet
    name::String
    breed::String
    age::Int
end

mutable struct Cat <: Pet
    name::String
    lives::Int
end

# Constructor
rex = Dog("Rex", "Labrador", 3)
whiskers = Cat("Whiskers", 9)

# Access fields
println(rex.name)
whiskers.lives -= 1   # mutable!

# Methods (multiple dispatch)
function speak(animal::Dog)
    "$(animal.name) says: Woof!"
end

function speak(animal::Cat)
    "$(animal.name) says: Meow!"
end

function speak(animal::Animal)
    "$(typeof(animal)) makes a sound"
end

println(speak(rex))
println(speak(whiskers))

# Parametric types
struct Point{T<:Number}
    x::T
    y::T
end

p1 = Point(3.0, 4.0)       # Point{Float64}
p2 = Point(3, 4)            # Point{Int64}

distance(p::Point) = sqrt(p.x^2 + p.y^2)
println(distance(p1))   # 5.0

# Type hierarchy
println(supertype(Int64))       # Signed
println(subtypes(Integer))      # [Bool, Signed, Unsigned]
println(Int64 <: Number)        # true

# Union types
function process(x::Union{Int, String})
    if x isa Int
        x * 2
    else
        uppercase(x)
    end
end

# Nothing and Missing
println(nothing)
println(ismissing(missing))

# Traits via Val
struct Celsius end
struct Fahrenheit end
convert_temp(::Type{Celsius}, t::Float64) = (t - 32) * 5/9
convert_temp(::Type{Fahrenheit}, t::Float64) = t * 9/5 + 32
```


---

# CHAPTER 7: MODULES AND PACKAGES


## Modules and Stdlib

```julia
# Defining a module
module MyMath
    export factorial, fibonacci

    function factorial(n::Int)
        n <= 1 ? 1 : n * factorial(n-1)
    end

    function fibonacci(n::Int)
        n <= 1 ? n : fibonacci(n-1) + fibonacci(n-2)
    end
end

using .MyMath
println(factorial(5))    # 120
println(fibonacci(10))   # 55

# Standard library modules
using LinearAlgebra
A = [1.0 2.0; 3.0 4.0]
println(det(A))
println(eigvals(A))
b = [1.0, 2.0]
x = A \ b    # solve Ax = b

using Statistics
data = [1.0, 2.0, 3.0, 4.0, 5.0]
println(mean(data))
println(median(data))
println(std(data))
println(var(data))
println(cor([1,2,3], [4,5,6]))

using Random
Random.seed!(42)
rand()              # uniform [0,1]
randn()             # normal(0,1)
rand(1:10)          # random int 1-10
shuffle([1,2,3,4,5])

# Pkg package manager
# import Pkg
# Pkg.add("DataFrames")
# Pkg.add("Plots")
# Pkg.status()

# Common packages
using Printf
@printf("Value: %.4f\n", π)
@sprintf("Pi ≈ %.2f", π)

# Dates
using Dates
now()
today()
Date(2024, 1, 15)
DateTime(2024, 1, 15, 12, 30, 0)
now() - DateTime(2024, 1, 1)   # Period
Dates.format(now(), "yyyy-mm-dd")
```


---

# CHAPTER 8: PERFORMANCE AND MACROS


## Metaprogramming and Performance

```julia
# Macros
macro saytime(expr)
    quote
        t = @elapsed $expr
        println("Time: $t seconds")
    end
end

@saytime sleep(0.1)

# Built-in macros
@time sum(1:1_000_000)       # time and allocations
@elapsed sum(1:1_000_000)    # time only
@allocated sum(1:1_000_000)  # allocations only
@benchmark sum($(1:1_000_000))   # BenchmarkTools

# Type stability (key for performance)
function stable(x::Float64)
    x > 0.0 ? x : -x    # always returns Float64
end

# @code_warntype to check type stability
@code_warntype stable(3.14)
@code_llvm stable(3.14)
@code_native stable(3.14)

# Avoid global variables (use const or pass as args)
# Use typed struct fields
# Use @inbounds for array access
function fast_sum(arr::Vector{Float64})
    s = 0.0
    @inbounds for x in arr
        s += x
    end
    s
end

# SIMD
function simd_sum(arr::Vector{Float64})
    s = 0.0
    @simd for x in arr
        s += x
    end
    s
end

# Parallel computing
using Base.Threads
println(Threads.nthreads())

Threads.@threads for i in 1:100
    # parallel loop body
end

# Tasks (coroutines)
function producer(ch::Channel)
    for i in 1:5
        put!(ch, i^2)
    end
    close(ch)
end

ch = Channel{Int}(5)
@async producer(ch)
for val in ch
    println(val)
end

# Metaprogramming
expr = :(1 + 2 * 3)   # expression object
eval(expr)             # 7
dump(expr)             # show AST

# Quote and unquote
x = 5
e = :($x * $x)
eval(e)   # 25

# Generated functions
@generated function my_zeros(::Val{N}) where N
    :(zeros($N))
end
my_zeros(Val(5))   # [0,0,0,0,0]
```
