# Ruby Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH RUBY


## Remarks

Ruby is a dynamic, interpreted, object-oriented scripting language emphasizing programmer happiness and productivity. Everything in Ruby is an object. Ruby on Rails is its most famous framework. Ruby 3.3+ is current.

Tools: MRI/CRuby (reference), JRuby, RubyGems, Bundler, IRB (REPL).


## Hello World

```ruby
# hello.rb
puts "Hello, World!"
print "Hello without newline"
p "Hello with inspect"     # shows quotes and escapes
pp [1, 2, 3]               # pretty print

printf("Hello, %s! You are %d years old.\n", "Alice", 30)
```

```bash
ruby hello.rb
irb   # interactive REPL
gem install rails
bundle exec ruby hello.rb
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Types and Variables

```ruby
# Variable types
local_var  = 42           # local variable
@instance  = "instance"   # instance variable
@@class_var = "class"     # class variable
$global    = "global"     # global variable
CONSTANT   = 3.14159      # constant

# Nil
x = nil
x.nil?          # true
x.is_a?(NilClass)

# Numbers
n   = 42
big = 10 ** 100           # Bignum (arbitrary precision)
f   = 3.14
r   = 3/4r                # Rational: (3/4)
c   = 2 + 3i              # Complex

# Strings
s = "Hello, World!"
s.length      # 13
s.size        # same
s.upcase
s.downcase
s.reverse
s.include?("World")
s.start_with?("Hello")
s.end_with?("!")
s.gsub("World", "Ruby")
s.split(", ")
s.strip
s.chars              # ["H","e","l","l","o",...]
s[0..4]              # "Hello"
s[-1]                # "!"

# String interpolation
name = "Alice"
puts "Hello, #{name}!"
puts "2 + 2 = #{2 + 2}"

# Symbols (immutable, interned)
:hello
:world
:hello.to_s    # "hello"
"hello".to_sym # :hello

# Boolean
true.class   # TrueClass
false.class  # FalseClass
nil.class    # NilClass

# Truthiness: only false and nil are falsy!
if 0          # TRUTHY in Ruby
if ""         # TRUTHY in Ruby
if nil        # falsy
if false      # falsy
```

## Collections

```ruby
# Array
arr = [1, 2, 3, 4, 5]
arr.push(6)          # arr << 6 also works
arr.pop
arr.shift            # remove first
arr.unshift(0)       # prepend
arr.first(3)         # [1, 2, 3]
arr.last(2)          # [5, 6]
arr.length; arr.size; arr.count
arr.include?(3)
arr.flatten
arr.compact          # remove nils
arr.uniq             # remove duplicates
arr.sort
arr.sort_by { |x| -x }
arr.reverse
arr.min; arr.max
arr.sum

# Hash
h = { name: "Alice", age: 30 }
h = { "name" => "Alice" }   # string keys
h[:name]            # "Alice"
h["name"]
h[:city] = "NYC"
h.delete(:age)
h.keys; h.values
h.each { |k, v| puts "#{k}: #{v}" }
h.map { |k, v| [k, v.to_s] }.to_h
h.select { |k, v| v.is_a?(String) }
h.reject { |k, v| v.nil? }
h.merge({ zip: "10001" })
h.any? { |k, v| v == 30 }
h.all? { |k, v| v }
h.fetch(:name, "default")

# Range
(1..10)          # inclusive
(1...10)         # exclusive
('a'..'z')       # character range
(1..10).to_a     # [1, 2, ..., 10]
(1..10).include?(5)
(1..10).each { |i| puts i }
(1..10).select(&:odd?)
(1..10).map { |n| n**2 }
(1..10).reduce(:+)

# Set
require 'set'
s = Set.new([1, 2, 3])
s.add(4)
s.include?(2)
s | Set[3,4,5]   # union
s & Set[2,3]     # intersection
```


---

# CHAPTER 3: CONTROL FLOW


## Control Structures

```ruby
# if/elsif/else/unless
if x > 0
  puts "positive"
elsif x == 0
  puts "zero"
else
  puts "negative"
end

# Inline if/unless
puts "positive" if x > 0
puts "not zero" unless x == 0

# Ternary
label = x > 0 ? "pos" : "non-pos"

# case/when
case day
when "Monday", "Tuesday"
  puts "Early week"
when /Sat|Sun/        # regex!
  puts "Weekend"
when 1..5             # range!
  puts "Number 1-5"
else
  puts "Other"
end

# loops
5.times { |i| puts i }
1.upto(5) { |i| puts i }
5.downto(1) { |i| puts i }

(1..10).each { |i| puts i }
[1,2,3].each { |x| puts x }
[1,2,3].each_with_index { |x, i| puts "#{i}: #{x}" }
[1,2,3].each_with_object([]) { |x, acc| acc << x*2 }

# while / until
while n > 0
  n -= 1
end

until n == 10
  n += 1
end

# loop with break
loop do
  input = gets.chomp
  break if input == "quit"
  puts input
end

# next (continue) / break / redo
[1,2,3,4,5].each do |n|
  next if n.even?
  break if n > 4
  puts n
end

# begin/end while (do-while)
begin
  n -= 1
end while n > 0
```


---

# CHAPTER 4: METHODS


## Defining Methods

```ruby
# Basic method
def greet(name)
  "Hello, #{name}!"   # implicit return (last expression)
end

# Default arguments
def connect(host, port: 8080, timeout: 30)
  "#{host}:#{port}"
end
connect("localhost", port: 3000)

# Splat (*args) and double splat (**kwargs)
def variadic(*args, **opts)
  args.each { |a| puts a }
  opts.each { |k, v| puts "#{k}=#{v}" }
end

# Block parameter
def repeat(n, &block)
  n.times { block.call }
end

# yield
def each_even(arr)
  arr.each { |x| yield x if x.even? }
end
each_even([1,2,3,4]) { |n| puts n }

# proc and lambda
square = proc { |x| x ** 2 }
double = lambda { |x| x * 2 }
add    = ->(a, b) { a + b }

square.call(5)   # 25
double.(5)       # 10
add.(3, 4)       # 7

# Method object
m = method(:puts)
m.call("hello")
[1,2,3].map(&method(:puts))

# Functional methods
nums = [1,2,3,4,5,6,7,8,9,10]
nums.map { |n| n * 2 }
nums.select { |n| n.odd? }
nums.reject { |n| n.even? }
nums.reduce(0) { |sum, n| sum + n }
nums.reduce(:+)                    # shorthand with symbol
nums.each_slice(3).to_a            # [[1,2,3],[4,5,6],[7,8,9],[10]]
nums.flat_map { |n| [n, n*n] }
nums.partition { |n| n.even? }     # [[2,4,6,8,10],[1,3,5,7,9]]
nums.group_by { |n| n % 3 }
nums.min_by { |n| (n - 5).abs }   # closest to 5
nums.sort_by { |n| -n }
nums.count { |n| n > 5 }
nums.any? { |n| n > 9 }
nums.all? { |n| n > 0 }
nums.none? { |n| n > 10 }
nums.find { |n| n > 5 }           # 6
nums.take_while { |n| n < 5 }
nums.drop_while { |n| n < 5 }
nums.zip([11,12,13])
nums.tally                         # {1=>1, 2=>1, ...}
nums.sum { |n| n * n }
nums.minmax
```


---

# CHAPTER 5: OBJECT-ORIENTED PROGRAMMING


## Classes

```ruby
class Animal
  attr_accessor :name, :sound    # generates getter+setter
  attr_reader   :id              # getter only
  attr_writer   :tag             # setter only

  @@count = 0   # class variable

  def initialize(name, sound)
    @name = name
    @sound = sound
    @id = @@count += 1
  end

  def speak
    "#{@name} says #{@sound}"
  end

  def to_s
    "Animal(#{@name})"
  end

  def inspect
    "#<Animal name=#{@name.inspect}>"
  end

  def self.count     # class method
    @@count
  end

  def self.create(name, sound)
    new(name, sound)
  end

  def <=>(other)       # comparable
    name <=> other.name
  end
  include Comparable
end

class Dog < Animal
  attr_reader :breed

  def initialize(name, breed)
    super(name, "Woof")
    @breed = breed
  end

  def speak
    super + "!"
  end

  def fetch
    "#{name} fetches!"
  end
end

# Module (mixin)
module Greetable
  def greet
    "Hello, I'm #{name}"
  end
end

class Person
  include Greetable      # mix in
  attr_reader :name
  def initialize(name) @name = name end
end

# Struct
Point = Struct.new(:x, :y) do
  def distance_to(other)
    Math.sqrt((x - other.x)**2 + (y - other.y)**2)
  end
end

p = Point.new(3, 4)
p.x; p.y; p.distance_to(Point.new(0,0))
```


---

# CHAPTER 6: MODULES AND MIXINS


## Modules

```ruby
module MathUtils
  PI = 3.14159265358979

  def self.circle_area(r)
    PI * r * r
  end

  # Mixed-in method
  def square
    self * self
  end
end

class Integer
  include MathUtils   # open class!
end

5.square   # 25 (added to all integers)

# Enumerable mixin
class NumberList
  include Enumerable
  include Comparable

  def initialize(*nums) @nums = nums end

  def each(&block) @nums.each(&block) end

  def <=>(other) @nums.sum <=> other.sum end
end

nl = NumberList.new(3, 1, 4, 1, 5)
nl.sort          # [1, 1, 3, 4, 5]
nl.min           # 1
nl.max           # 5
nl.select(&:odd?)
nl.map { |n| n * 2 }
nl.include?(4)

# Comparable mixin
class Temperature
  include Comparable
  attr_reader :degrees
  def initialize(d) @degrees = d end
  def <=>(other) degrees <=> other.degrees end
end

temps = [Temperature.new(30), Temperature.new(15), Temperature.new(25)]
temps.sort.first.degrees   # 15
```


---

# CHAPTER 7: EXCEPTIONS AND FILE I/O


## Error Handling

```ruby
# begin/rescue/ensure/raise
begin
  result = 10 / 0
rescue ZeroDivisionError => e
  puts "Math error: #{e.message}"
rescue TypeError, ArgumentError => e
  puts "Type or Arg error: #{e.message}"
rescue => e     # catch all StandardError
  puts "Error: #{e.message}"
  raise         # re-raise
else
  puts "Success: #{result}"
ensure
  puts "Always runs"
end

# raise
raise ArgumentError, "must be positive" unless x > 0
raise "Something went wrong"

# Custom exception
class AppError < StandardError
  attr_reader :code
  def initialize(msg, code = nil)
    super(msg)
    @code = code
  end
end

raise AppError.new("Not found", 404)

# File I/O
# Read
content = File.read("file.txt")
lines   = File.readlines("file.txt").map(&:chomp)

File.open("file.txt") do |f|
  f.each_line { |line| puts line }
end

# Write
File.write("out.txt", "Hello\n")
File.open("out.txt", "w") { |f| f.puts "Line 1" }
File.open("out.txt", "a") { |f| f.puts "Appended" }

# CSV
require 'csv'
CSV.foreach("data.csv", headers: true) do |row|
  puts row["name"]
end
CSV.open("out.csv", "w") do |csv|
  csv << ["name", "age"]
  csv << ["Alice", 30]
end
```


---

# CHAPTER 8: METAPROGRAMMING


## Dynamic Features

```ruby
# method_missing
class DynamicProxy
  def initialize(target) @target = target end

  def method_missing(name, *args, &block)
    if @target.respond_to?(name)
      @target.send(name, *args, &block)
    else
      super
    end
  end

  def respond_to_missing?(name, include_private = false)
    @target.respond_to?(name) || super
  end
end

# define_method
[:add, :subtract, :multiply].each do |op|
  define_method("#{op}_ten") do |n|
    case op
    when :add      then n + 10
    when :subtract then n - 10
    when :multiply then n * 10
    end
  end
end

# eval / class_eval / instance_eval
class Person; end
Person.class_eval do
  def greet; "Hello!"; end
end

# send (dynamic method call)
"hello".send(:upcase)           # "HELLO"
obj.send(:private_method)       # can call private methods

# Reflection
"hello".class                   # String
"hello".is_a?(String)           # true
"hello".respond_to?(:upcase)    # true
String.instance_methods(false)  # methods defined in String only
String.ancestors                # [String, Comparable, Object, ...]

# Proc / lambda differences
# proc: return exits method; args are flexible
# lambda: return exits lambda; args are strict

# Frozen objects
str = "hello".freeze
str << " world"   # FrozenError!
str.frozen?       # true
```
