# Elixir Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH ELIXIR


## Remarks

Elixir is a dynamic, functional language built on the Erlang VM (BEAM). It inherits Erlang's concurrency and fault-tolerance while adding a modern syntax, macros, and the Phoenix web framework. Used for web apps, distributed systems, and real-time applications.

Tools: iex (REPL), mix (build tool), hex (package manager), Phoenix framework.


## Hello World

```elixir
# hello.exs (script)
IO.puts("Hello, World!")
IO.puts("Hello, #{\"Elixir\"}!")

# Run:
# elixir hello.exs
# iex hello.exs

# Mix project
# mix new my_project
# cd my_project && mix run
```


---

# CHAPTER 2: TYPES AND VARIABLES


## Basic Types

```elixir
# Variables (lowercase, snake_case)
# Rebinding is OK (not truly immutable like Haskell)
name = "Alice"
age  = 30
pi   = 3.14159
flag = true

# Atoms (like symbols, lowercase or :quoted)
:ok
:error
:hello
true     # same as :true
false    # same as :false
nil      # same as :nil

# Integers
42
1_000_000     # underscores for readability
0xFF          # hex: 255
0b1010        # binary: 10
0o777         # octal: 511

# Floats
3.14
1.0e-5

# Strings (UTF-8 encoded binaries)
s = "Hello, World!"
String.length(s)           # 13
String.upcase(s)
String.downcase(s)
String.slice(s, 0, 5)      # "Hello"
String.contains?(s, "World")
String.replace(s, "World", "Elixir")
String.split(s, ", ")
String.trim("  hello  ")
String.starts_with?(s, "Hello")
String.ends_with?(s, "!")
String.to_integer("42")
String.to_float("3.14")

# String interpolation
greeting = "Hello, #{name}!"
math = "2 + 2 = #{2 + 2}"

# Charlists (Erlang strings)
chars = 'hello'    # charlist
is_list(chars)     # true
List.to_string(chars)   # "hello"

# Tuples
{:ok, 42}
{:error, "not found"}
{1, 2, 3}
t = {:ok, "result"}
elem(t, 0)          # :ok
elem(t, 1)          # "result"
put_elem(t, 1, "new")  # {:ok, "new"}
tuple_size(t)        # 2

# Pattern matching (fundamental!)
{status, value} = {:ok, 42}   # status=:ok, value=42
{:ok, n} = {:ok, 100}          # n=100
[h | t] = [1, 2, 3]           # h=1, t=[2,3]

# Pin operator ^ (don't rebind)
x = 1
{^x, y} = {1, 2}   # matches only if first = 1
```


---

# CHAPTER 3: COLLECTIONS


## Lists, Maps, and Structs

```elixir
# Lists (linked lists)
list = [1, 2, 3, 4, 5]
[h | t] = list         # head = 1, tail = [2,3,4,5]
[1 | [2, 3]]           # [1,2,3]
list ++ [6, 7]         # [1,2,3,4,5,6,7]
[0 | list]             # [0,1,2,3,4,5] (prepend)
length(list)           # 5
hd(list)               # 1
tl(list)               # [2,3,4,5]
Enum.at(list, 2)       # 3

# Keyword lists (list of {atom, value} tuples)
opts = [timeout: 5000, retries: 3]
opts[:timeout]           # 5000
Keyword.get(opts, :retries)  # 3

# Maps
m = %{name: "Alice", age: 30}     # atom keys
m2 = %{"name" => "Bob", "age" => 25}  # string keys

m.name                # "Alice" (atom key shortcut)
m[:name]              # "Alice"
Map.get(m, :name)     # "Alice"
Map.get(m, :missing, "default")
Map.put(m, :city, "NYC")
Map.delete(m, :age)
Map.has_key?(m, :name)   # true
Map.keys(m)
Map.values(m)
Map.to_list(m)
Map.from_list([{:a, 1}, {:b, 2}])
Map.merge(m, %{email: "alice@example.com"})
Map.update!(m, :age, fn age -> age + 1 end)

# Map update syntax
%{m | age: 31}         # returns new map with age=31

# Map pattern matching
%{name: name} = m      # name = "Alice"
%{name: n, age: a} = m

# Structs (compile-time enforced maps)
defmodule Person do
  defstruct [:name, age: 0, city: "Unknown"]
end

alice = %Person{name: "Alice", age: 30}
alice.name                    # "Alice"
%Person{name: n} = alice      # pattern match
%{alice | age: 31}            # update

# MapSet
s = MapSet.new([1, 2, 3, 2, 1])
MapSet.put(s, 4)
MapSet.delete(s, 1)
MapSet.member?(s, 2)    # true
MapSet.union(s, MapSet.new([3,4,5]))
MapSet.intersection(s, MapSet.new([2,3,7]))
MapSet.to_list(s)
```


---

# CHAPTER 4: ENUM AND STREAM


## Functional Collection Operations

```elixir
list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Enum — eager evaluation
Enum.map(list, fn x -> x * 2 end)          # [2,4,6,8,10,12,14,16,18,20]
Enum.filter(list, fn x -> rem(x, 2) == 0 end)  # [2,4,6,8,10]
Enum.reject(list, fn x -> rem(x, 2) == 0 end)  # [1,3,5,7,9]
Enum.reduce(list, 0, fn x, acc -> x + acc end)  # 55
Enum.sum(list)           # 55
Enum.min(list)           # 1
Enum.max(list)           # 10
Enum.sort(list)
Enum.sort(list, :desc)
Enum.sort_by(list, fn x -> -x end)
Enum.reverse(list)
Enum.count(list)         # 10
Enum.count(list, fn x -> x > 5 end)  # 5
Enum.any?(list, fn x -> x > 9 end)   # true
Enum.all?(list, fn x -> x > 0 end)   # true
Enum.find(list, fn x -> x > 5 end)   # 6
Enum.find_index(list, fn x -> x > 5 end)  # 5
Enum.take(list, 3)       # [1,2,3]
Enum.drop(list, 7)       # [8,9,10]
Enum.take_while(list, fn x -> x < 5 end)  # [1,2,3,4]
Enum.drop_while(list, fn x -> x < 5 end)  # [5,6,7,8,9,10]
Enum.zip(list, list)
Enum.zip_with(list, list, fn a, b -> a + b end)
Enum.flat_map(list, fn x -> [x, x*2] end)
Enum.chunk_every(list, 3)    # [[1,2,3],[4,5,6],[7,8,9],[10]]
Enum.group_by(list, fn x -> rem(x, 2) == 0 end)
Enum.uniq([1,2,2,3,3,4])  # [1,2,3,4]
Enum.frequencies([1,1,2,3,3])  # %{1=>2, 2=>1, 3=>2}

# Stream — lazy evaluation
Stream.map(list, fn x -> x * 2 end)
|> Stream.filter(fn x -> x > 10 end)
|> Enum.take(3)

Stream.cycle([1,2,3]) |> Enum.take(9)    # [1,2,3,1,2,3,1,2,3]
Stream.iterate(1, fn x -> x * 2 end) |> Enum.take(10)  # powers of 2
Stream.unfold(0, fn n -> {n, n+1} end) |> Enum.take(5) # [0,1,2,3,4]

# Pipe operator |>
[1,2,3,4,5]
|> Enum.map(fn x -> x * x end)
|> Enum.filter(fn x -> x > 5 end)
|> Enum.sum()   # 50

# Comprehensions
for x <- 1..5, do: x * x       # [1,4,9,16,25]
for x <- 1..5, x > 3, do: x    # [4,5]
for x <- 1..3, y <- 1..3, do: {x, y}
for x <- 1..5, into: %{}, do: {x, x*x}  # map
```


---

# CHAPTER 5: FUNCTIONS AND MODULES


## Functions

```elixir
defmodule Math do
  # Public function
  def add(a, b), do: a + b

  # Multi-line function body
  def factorial(0), do: 1
  def factorial(n) when n > 0, do: n * factorial(n - 1)

  # Default arguments
  def greet(name, greeting \\ "Hello") do
    "#{greeting}, #{name}!"
  end

  # Private function
  defp helper(x), do: x * 2

  # Guards
  def abs_val(x) when x >= 0, do: x
  def abs_val(x), do: -x

  # Multiple return values via tuple
  def minmax(list) do
    {Enum.min(list), Enum.max(list)}
  end
end

Math.add(3, 4)              # 7
Math.factorial(5)           # 120
{min, max} = Math.minmax([3,1,4,1,5,9])

# Anonymous functions
square = fn x -> x * x end
square.(5)    # 25 (note the dot!)

add = fn a, b -> a + b end
add.(3, 4)

# Shorthand (&) capture syntax
square = &(&1 * &1)
add    = &(&1 + &2)
double = &(Enum.map(&1, fn x -> x * 2 end))

Enum.map(1..5, &(&1 * 2))
Enum.filter(1..10, &(rem(&1, 2) == 0))

# Function as value / capture
add_fn = &Math.add/2
add_fn.(3, 4)   # 7

Enum.map([1,2,3], &Math.factorial/1)

# Closures
make_adder = fn n ->
  fn x -> x + n end
end
add5 = make_adder.(5)
add5.(10)   # 15

# Partial application with &
greet = fn greeting ->
  fn name -> "#{greeting}, #{name}!" end
end
hello = greet.("Hello")
hello.("Alice")   # "Hello, Alice!"
```


---

# CHAPTER 6: CONCURRENCY WITH PROCESSES


## The Actor Model

```elixir
# Spawn a process
pid = spawn(fn ->
  IO.puts("Hello from process #{inspect(self())}")
end)

# Send and receive messages
parent = self()
child = spawn(fn ->
  receive do
    {:hello, from} -> send(from, {:world, self()})
  end
end)

send(child, {:hello, parent})
receive do
  {:world, from} -> IO.puts("Got world from #{inspect(from)}")
after 1000 -> IO.puts("Timeout")
end

# Process with state (recursive loop)
defmodule Counter do
  def start(n \\ 0) do
    spawn(fn -> loop(n) end)
  end

  defp loop(n) do
    receive do
      {:increment, from} ->
        send(from, n + 1)
        loop(n + 1)
      {:get, from} ->
        send(from, n)
        loop(n)
      :stop -> :ok
    end
  end
end

pid = Counter.start()
send(pid, {:increment, self()})
receive do n -> IO.puts("Count: #{n}") end

# Task (high-level async)
task = Task.async(fn ->
  :timer.sleep(100)
  42
end)
result = Task.await(task)   # 42

# Task.async_stream (parallel processing)
[1, 2, 3, 4, 5]
|> Task.async_stream(fn n ->
  :timer.sleep(100)
  n * n
end, max_concurrency: 3)
|> Enum.map(fn {:ok, v} -> v end)  # [1,4,9,16,25]

# Agent (simple state management)
{:ok, agent} = Agent.start_link(fn -> %{count: 0} end)
Agent.update(agent, fn state -> %{state | count: state.count + 1} end)
Agent.get(agent, fn state -> state.count end)
```


---

# CHAPTER 7: OTP AND GENSERVER


## OTP Behaviors

```elixir
# GenServer
defmodule MyServer do
  use GenServer

  # Client API
  def start_link(opts \\ []) do
    GenServer.start_link(__MODULE__, %{}, opts)
  end

  def put(server, key, value) do
    GenServer.cast(server, {:put, key, value})
  end

  def get(server, key) do
    GenServer.call(server, {:get, key})
  end

  def delete(server, key) do
    GenServer.call(server, {:delete, key})
  end

  # Server callbacks
  @impl true
  def init(state), do: {:ok, state}

  @impl true
  def handle_call({:get, key}, _from, state) do
    {:reply, Map.get(state, key), state}
  end
  def handle_call({:delete, key}, _from, state) do
    {:reply, :ok, Map.delete(state, key)}
  end

  @impl true
  def handle_cast({:put, key, value}, state) do
    {:noreply, Map.put(state, key, value)}
  end

  @impl true
  def handle_info(:tick, state) do
    IO.puts("Tick!")
    {:noreply, state}
  end
end

{:ok, pid} = MyServer.start_link()
MyServer.put(pid, :name, "Alice")
MyServer.get(pid, :name)   # "Alice"

# Supervisor
defmodule MySupervisor do
  use Supervisor

  def start_link(_opts) do
    Supervisor.start_link(__MODULE__, :ok, name: __MODULE__)
  end

  @impl true
  def init(:ok) do
    children = [
      {MyServer, name: :my_server}
    ]
    Supervisor.init(children, strategy: :one_for_one)
  end
end
```


---

# CHAPTER 8: MACROS AND METAPROGRAMMING


## Macros

```elixir
# defmacro — compile-time code generation
defmodule MyMacros do
  defmacro unless(condition, do: body) do
    quote do
      if !unquote(condition), do: unquote(body)
    end
  end

  defmacro debug(expr) do
    quote do
      result = unquote(expr)
      IO.puts("#{unquote(Macro.to_string(expr))} = #{inspect(result)}")
      result
    end
  end
end

require MyMacros
MyMacros.unless false do IO.puts("executed") end
MyMacros.debug(1 + 2 * 3)   # prints: 1 + 2 * 3 = 7

# Protocols (polymorphism)
defprotocol Describable do
  def describe(x)
end

defimpl Describable, for: Integer do
  def describe(n), do: "Integer: #{n}"
end

defimpl Describable, for: BitString do
  def describe(s), do: "String: #{s}"
end

defimpl Describable, for: List do
  def describe(l), do: "List of #{length(l)} items"
end

Describable.describe(42)        # "Integer: 42"
Describable.describe("hello")   # "String: hello"
Describable.describe([1,2,3])   # "List of 3 items"

# mix tasks
# mix deps.get, mix compile, mix test, mix format
# mix phx.new my_app  (Phoenix)
# mix ecto.migrate    (database)

# Testing with ExUnit
defmodule MyTest do
  use ExUnit.Case

  test "addition" do
    assert Math.add(1, 2) == 3
  end

  test "factorial" do
    assert Math.factorial(0) == 1
    assert Math.factorial(5) == 120
  end

  test "raises error" do
    assert_raise ArithmeticError, fn -> 1 / 0 end
  end
end
```
