# Functional Programming Complete Reference


---

# CHAPTER 1: CORE PRINCIPLES


## Remarks

Functional programming (FP) is a paradigm where programs are built by composing pure functions, avoiding shared mutable state and side effects. FP originated in lambda calculus (Alonzo Church, 1930s) and is implemented in languages like Haskell, Erlang, Elixir, Clojure, OCaml, and F#. Modern languages (JavaScript, Python, Rust, Kotlin, Swift, Java) have adopted FP features heavily. Understanding FP makes you write cleaner code in ANY language.

Key concepts: **Pure functions** (same input → same output, no side effects), **Immutability** (data never changes), **First-class functions** (functions as values), **Higher-order functions** (functions that take/return functions), **Composition** (combine simple functions into complex ones), **Recursion** (loop via self-reference), **Monads** (composable computation containers), **Algebraic Data Types** (sum and product types), **Pattern matching** (destructure and dispatch).


## Pure Functions

```python
# PURE: depends ONLY on inputs, produces ONLY output
# No side effects (no mutation, no I/O, no global state)

# PURE ✅
def add(a, b):
    return a + b

def discount(price, rate):
    return price * (1 - rate)

def sort_list(lst):
    return sorted(lst)   # Returns NEW list, doesn't mutate original

# IMPURE ❌
total = 0
def add_to_total(n):
    global total
    total += n           # Side effect: modifies global state
    return total

def get_time():
    return datetime.now()  # Different result each call

def save_user(user):
    db.insert(user)        # Side effect: I/O
    return user

# WHY PURE MATTERS:
#   ✅ Testable (no setup, no mocks needed)
#   ✅ Cacheable/memoizable (same input = same output = can cache)
#   ✅ Parallelizable (no shared state = no race conditions)
#   ✅ Debuggable (predictable, reproducible)
#   ✅ Composable (output of one → input of next)

# REAL PROGRAMS NEED SIDE EFFECTS (I/O, state)
# FP strategy: push side effects to the EDGES.
# Pure core → impure shell (functional core, imperative shell)
```


## Immutability

```python
# MUTABLE (dangerous in concurrent/shared contexts)
users = [{"name": "Alice", "age": 30}]
users[0]["age"] = 31          # Mutated! Anyone holding reference sees change.
users.append({"name": "Bob"}) # Mutated!

# IMMUTABLE (safe, predictable)
from dataclasses import dataclass, replace

@dataclass(frozen=True)   # frozen = immutable
class User:
    name: str
    age: int

alice = User("Alice", 30)
# alice.age = 31            # Error! Can't mutate frozen dataclass

# Create modified copy instead
older_alice = replace(alice, age=31)
print(alice.age)       # 30 (unchanged!)
print(older_alice.age) # 31 (new object)


# Immutable collections
original = (1, 2, 3)          # Tuple (immutable list)
extended = original + (4,)     # New tuple, original unchanged

from frozenset import frozenset
s = frozenset([1, 2, 3])      # Immutable set


# JavaScript immutability patterns
# const user = { name: "Alice", age: 30 };
# const older = { ...user, age: 31 };           // Spread operator
# const users = [user1, user2];
# const more = [...users, user3];               // New array
# Object.freeze(user);                          // Shallow freeze


# WHY IMMUTABILITY:
#   ✅ No accidental mutation (bugs from shared references)
#   ✅ Thread-safe (no locks needed)
#   ✅ Easy undo/redo (keep old versions)
#   ✅ Change detection is trivial (reference equality: old !== new)
#   ✅ Enables structural sharing (efficient immutable data structures)

# STRUCTURAL SHARING:
# Persistent data structures (Clojure, Immutable.js):
# New version shares unchanged parts with old version.
# [1, 2, 3, 4] → change index 2 → [1, 2, 99, 4]
# Only index 2 is new. Indices 0, 1, 3 point to same memory.
```


---

# CHAPTER 2: HIGHER-ORDER FUNCTIONS


## Functions as Values

```python
# First-class functions: pass them around like any value

# Function as argument
def apply(fn, x):
    return fn(x)

apply(str.upper, "hello")      # "HELLO"
apply(len, [1, 2, 3])          # 3
apply(lambda x: x ** 2, 5)     # 25

# Function as return value
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
triple = multiplier(3)
double(5)    # 10
triple(5)    # 15

# Closure: inner function captures variables from outer scope
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

c = counter()
c()    # 1
c()    # 2
c()    # 3
```


## Map, Filter, Reduce

```python
# MAP: transform each element
numbers = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, numbers))        # [2, 4, 6, 8, 10]
doubled = [x * 2 for x in numbers]                     # Same (Pythonic)

names = ["alice", "bob", "charlie"]
upper = list(map(str.capitalize, names))               # ["Alice", "Bob", "Charlie"]


# FILTER: keep elements matching predicate
evens = list(filter(lambda x: x % 2 == 0, numbers))   # [2, 4]
evens = [x for x in numbers if x % 2 == 0]            # Same (Pythonic)

adults = [u for u in users if u.age >= 18]


# REDUCE: combine all elements into single value
from functools import reduce

total = reduce(lambda acc, x: acc + x, numbers, 0)    # 15
product = reduce(lambda acc, x: acc * x, numbers, 1)  # 120

# Reduce to build dict
word_count = reduce(
    lambda acc, word: {**acc, word: acc.get(word, 0) + 1},
    ["a", "b", "a", "c", "b", "a"],
    {}
)
# {"a": 3, "b": 2, "c": 1}


# CHAIN operations (functional pipeline)
result = (
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    |> filter(lambda x: x % 2 == 0)  # Python doesn't have |> yet
    |> map(lambda x: x ** 2)
    |> sum
)

# Python equivalent:
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = sum(x ** 2 for x in nums if x % 2 == 0)   # 220


# JavaScript equivalents:
# [1,2,3,4,5]
#   .filter(x => x % 2 === 0)
#   .map(x => x ** 2)
#   .reduce((sum, x) => sum + x, 0)
```


## Function Composition

```python
# Compose: combine functions into a pipeline
# f(g(x)) → compose(f, g)(x)

def compose(*fns):
    def composed(x):
        result = x
        for fn in reversed(fns):
            result = fn(result)
        return result
    return composed

def pipe(*fns):
    def piped(x):
        result = x
        for fn in fns:
            result = fn(result)
        return result
    return piped

# pipe: left-to-right (more intuitive)
process_name = pipe(
    str.strip,
    str.lower,
    lambda s: s.replace(" ", "_"),
)

process_name("  John Doe  ")   # "john_doe"


# Real-world: data processing pipeline
process_users = pipe(
    lambda users: [u for u in users if u["active"]],       # Filter active
    lambda users: [u for u in users if u["age"] >= 18],    # Filter adults
    lambda users: sorted(users, key=lambda u: u["name"]),  # Sort by name
    lambda users: [u["name"] for u in users],              # Extract names
)

result = process_users(raw_users)


# Partial application: fix some arguments, leave others
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

square(5)    # 25
cube(3)      # 27

# Partial in real code
import json
pretty_json = partial(json.dumps, indent=2, sort_keys=True)
print(pretty_json({"b": 2, "a": 1}))
```


---

# CHAPTER 3: ALGEBRAIC DATA TYPES AND PATTERN MATCHING


## Sum Types (Tagged Unions)

```python
# Sum type: value is ONE OF several variants
# Also called: tagged union, discriminated union, variant, enum

from dataclasses import dataclass
from typing import Union

# Python (approximation with dataclasses)
@dataclass
class Loading:
    pass

@dataclass
class Success:
    data: list

@dataclass
class Error:
    message: str

State = Union[Loading, Success, Error]   # Sum type

def render(state: State) -> str:
    match state:
        case Loading():
            return "Loading..."
        case Success(data=data):
            return f"Got {len(data)} items"
        case Error(message=msg):
            return f"Error: {msg}"

render(Loading())                    # "Loading..."
render(Success(data=[1, 2, 3]))     # "Got 3 items"
render(Error(message="timeout"))    # "Error: timeout"


# TypeScript (native discriminated unions)
# type State =
#   | { status: "loading" }
#   | { status: "success"; data: User[] }
#   | { status: "error"; message: string }


# Rust (native enums with data)
# enum State {
#     Loading,
#     Success(Vec<User>),
#     Error(String),
# }
# match state {
#     State::Loading => println!("Loading..."),
#     State::Success(users) => println!("Got {} users", users.len()),
#     State::Error(msg) => println!("Error: {}", msg),
# }


# Option/Maybe type (value or nothing)
from typing import Optional

def find_user(id: int) -> Optional[User]:
    user = db.get(id)
    return user   # User or None

# Rust: Option<T> = Some(T) | None
# Haskell: Maybe a = Just a | Nothing
# Forces you to handle the None case!


# Result type (success or error)
@dataclass
class Ok:
    value: any

@dataclass
class Err:
    error: str

Result = Union[Ok, Err]

def divide(a: float, b: float) -> Result:
    if b == 0:
        return Err("Division by zero")
    return Ok(a / b)

match divide(10, 3):
    case Ok(value=v):
        print(f"Result: {v}")
    case Err(error=e):
        print(f"Error: {e}")
```


## Pattern Matching

```python
# Python 3.10+ structural pattern matching

def describe(value):
    match value:
        # Literal patterns
        case 0:
            return "zero"
        case 1 | 2 | 3:
            return "small"
        
        # Type + destructuring
        case str(s) if len(s) > 10:
            return f"long string: {s[:10]}..."
        case str(s):
            return f"string: {s}"
        
        # Sequence patterns
        case []:
            return "empty list"
        case [x]:
            return f"single element: {x}"
        case [x, y]:
            return f"pair: {x}, {y}"
        case [first, *rest]:
            return f"first={first}, rest has {len(rest)} items"
        
        # Mapping patterns
        case {"type": "user", "name": name, "age": age}:
            return f"User {name}, age {age}"
        case {"type": "error", "message": msg}:
            return f"Error: {msg}"
        
        # Guard clause
        case int(n) if n > 0:
            return f"positive: {n}"
        case int(n):
            return f"non-positive: {n}"
        
        # Wildcard
        case _:
            return "unknown"

describe(0)                                    # "zero"
describe([1, 2, 3, 4])                        # "first=1, rest has 3 items"
describe({"type": "user", "name": "Alice", "age": 30})  # "User Alice, age 30"
```


---

# CHAPTER 4: MONADS AND FUNCTORS


## What Are Monads (Simplified)

```
FUNCTOR: a container you can MAP over.
  List is a functor:   [1,2,3].map(x => x*2) = [2,4,6]
  Optional is a functor: Some(5).map(x => x*2) = Some(10), None.map(...) = None
  Promise is a functor: promise.then(x => x*2)

MONAD: a functor you can FLATMAP (chain/bind) over.
  Allows sequencing operations that return wrapped values.
  
  Without monad (nested nightmare):
    getUser(id) returns Optional<User>
    getAddress(user) returns Optional<Address>
    getCity(address) returns Optional<String>
    
    result = getUser(id)
    if result is not None:
        address = getAddress(result)
        if address is not None:
            city = getCity(address)
            if city is not None:
                print(city)
    
  With monad (flat chain):
    getUser(id)
      .flatMap(getAddress)
      .flatMap(getCity)
      .map(print)
    
    If ANY step returns None → entire chain returns None.
    No nested ifs!

MONAD LAWS:
  1. Left identity:  unit(a).flatMap(f)  ==  f(a)
  2. Right identity: m.flatMap(unit)     ==  m
  3. Associativity:  m.flatMap(f).flatMap(g)  ==  m.flatMap(x => f(x).flatMap(g))
```


## Practical Monads in Python

```python
# OPTIONAL MONAD (handle None without if-checks)
class Maybe:
    def __init__(self, value):
        self._value = value

    @staticmethod
    def of(value):
        return Maybe(value)

    def map(self, fn):
        if self._value is None:
            return Maybe(None)
        return Maybe(fn(self._value))

    def flat_map(self, fn):
        if self._value is None:
            return Maybe(None)
        return fn(self._value)

    def get_or_else(self, default):
        return self._value if self._value is not None else default

    def __repr__(self):
        return f"Maybe({self._value})"

# Usage
def get_user(user_id):
    return Maybe.of({"name": "Alice", "address": {"city": "Brașov"}})

def get_address(user):
    return Maybe.of(user.get("address"))

def get_city(address):
    return Maybe.of(address.get("city"))

result = (
    get_user(123)
    .flat_map(get_address)
    .flat_map(get_city)
    .get_or_else("Unknown")
)
print(result)   # "Brașov"

# If any step returns None → final result is "Unknown"
# No nested if-checks!


# RESULT MONAD (handle errors without try-catch)
class Result:
    def __init__(self, value=None, error=None):
        self._value = value
        self._error = error
        self._is_ok = error is None

    @staticmethod
    def ok(value): return Result(value=value)

    @staticmethod
    def err(error): return Result(error=error)

    def map(self, fn):
        if not self._is_ok:
            return self
        try:
            return Result.ok(fn(self._value))
        except Exception as e:
            return Result.err(str(e))

    def flat_map(self, fn):
        if not self._is_ok:
            return self
        return fn(self._value)

    def get_or_else(self, default):
        return self._value if self._is_ok else default

# Pipeline that gracefully handles errors
def parse_int(s):
    try:
        return Result.ok(int(s))
    except ValueError:
        return Result.err(f"Not a number: {s}")

def divide_by(divisor):
    def inner(n):
        if divisor == 0:
            return Result.err("Division by zero")
        return Result.ok(n / divisor)
    return inner

result = (
    parse_int("42")
    .flat_map(divide_by(7))
    .map(lambda x: x + 1)
    .get_or_else(0)
)
print(result)   # 7.0


# PROMISE IS A MONAD (JavaScript):
# fetch('/api/user')
#   .then(res => res.json())          // flatMap
#   .then(user => fetch(`/api/posts/${user.id}`))  // flatMap
#   .then(res => res.json())          // flatMap
#   .catch(err => console.error(err)) // error handling
# 
# async/await is syntactic sugar for monadic chaining!
```


---

# CHAPTER 5: COMMON PITFALLS


## FP Pitfalls

```
PITFALL 1: FP dogmatism
  "Everything must be pure!" in an inherently impure world.
  Fix: pragmatic FP. Pure core, impure shell. Use FP where it helps.

PITFALL 2: Overusing reduce
  reduce() for everything → unreadable. Sometimes a loop is clearer.
  Fix: use reduce for actual accumulation. Use map/filter for transformations.

PITFALL 3: Deep recursion without TCO
  Python has no tail-call optimization. Deep recursion → stack overflow.
  Fix: use iteration, or explicit stack, or increase recursion limit.

PITFALL 4: Immutability performance
  Copying large objects on every change → slow.
  Fix: structural sharing (persistent data structures), or be pragmatic with mutation in hot paths.

PITFALL 5: Monad tutorial fallacy
  Trying to understand monads abstractly. Confusion guaranteed.
  Fix: use them first (Optional, Result, Promise). Understanding comes from practice.

PITFALL 6: Over-abstraction
  Pointfree style, monad transformers, applicative functors in Python.
  Fix: use FP concepts that make YOUR code clearer. Not Haskell in Python.

PITFALL 7: Ignoring readability
  compose(pipe(map(filter(reduce(...)))) — clever but unreadable.
  Fix: name intermediate variables. Split into functions. Be kind to future readers.

PITFALL 8: Not using the language's idioms
  Writing Haskell-style in Python. Writing Java-style in Clojure.
  Fix: learn the language's FP features. Python: comprehensions > map/filter.

PITFALL 9: Pure functions that aren't
  def "pure" function reads from database → actually impure.
  Fix: dependencies should be explicit parameters, not hidden I/O.

PITFALL 10: Mutation in map/filter callbacks
  [].map(x => { x.processed = true; return x; }) — mutates original!
  Fix: return new objects: .map(x => ({...x, processed: true}))
```