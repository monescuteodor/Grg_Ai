# Python Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH PYTHON


## Remarks

Python is a high-level, interpreted, dynamically typed language emphasizing readability. It supports procedural, object-oriented, and functional paradigms. Used widely in web development, data science, AI/ML, and automation.

Tools: CPython (reference), PyPy (JIT), pip, venv, poetry, conda.


## Hello World

```python
print("Hello, World!")
name = "Python"
print(f"Hello, {name}!")
```

```bash
python hello.py
python -m py_compile hello.py   # check syntax
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Built-in Types

```python
# Integers (arbitrary precision)
x = 42
big = 10 ** 100

# Floats
pi = 3.14159
sci = 1.5e-10

# Complex
z = 3 + 4j
print(z.real, z.imag)

# Boolean
flag = True
bool(0)       # False
bool("hi")    # True

# Strings
s = "Hello"
raw = r"C:\Users"
multi = """multi
line"""

# None
val = None

# Type conversion
int("42")         # 42
float("3.14")     # 3.14
str(100)          # "100"

# Type checking
isinstance(42, int)           # True
type(42) is int               # True
```

## Collections

```python
# List (mutable, ordered)
lst = [1, 2, 3]
lst.append(4)
lst.insert(0, 0)
lst.extend([5, 6])
lst.pop()
lst.remove(3)
lst.sort()
lst.reverse()

# Tuple (immutable)
t = (1, 2, 3)
single = (42,)

# Dict
d = {"name": "Alice", "age": 30}
d["city"] = "NYC"
d.get("missing", "default")
d.keys(); d.values(); d.items()

# Set
s = {1, 2, 3}
s.add(4)
s | {5}    # union
s & {2,3}  # intersection
s - {1}    # difference

# Comprehensions
squares = [x**2 for x in range(10)]
evens   = [x for x in range(20) if x % 2 == 0]
sq_dict = {x: x**2 for x in range(5)}
sq_set  = {x**2 for x in range(5)}
```


---

# CHAPTER 3: CONTROL FLOW


## Conditionals and Loops

```python
# if/elif/else
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# Ternary
result = "even" if x % 2 == 0 else "odd"

# for
for i in range(5):
    print(i)

for i, val in enumerate(["a", "b", "c"]):
    print(i, val)

for k, v in {"a": 1}.items():
    print(k, v)

# while
n = 10
while n > 0:
    n -= 1

# break / continue
for i in range(10):
    if i == 5: break
    if i % 2 == 0: continue
    print(i)

# match (Python 3.10+)
match command:
    case "quit": print("Exiting")
    case "help": print("Help")
    case _:      print("Unknown")
```


---

# CHAPTER 4: FUNCTIONS


## Defining Functions

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Default args
def connect(host, port=8080, timeout=30):
    return f"{host}:{port}"

# *args and **kwargs
def variadic(*args, **kwargs):
    print(args, kwargs)

# Lambda
square = lambda x: x ** 2

# Map, filter, reduce
from functools import reduce
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x*2, nums))
evens   = list(filter(lambda x: x%2==0, nums))
total   = reduce(lambda a,b: a+b, nums)

# Closures
def make_counter():
    count = [0]
    def inc():
        count[0] += 1
        return count[0]
    return inc

# Decorators
def timer(func):
    import time
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time()-t:.4f}s")
        return result
    return wrapper

@timer
def slow(): import time; time.sleep(0.1)

# Generator
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# lru_cache
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```


---

# CHAPTER 5: OBJECT-ORIENTED PROGRAMMING


## Classes

```python
class Animal:
    kingdom = "Animalia"  # class variable

    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"

    def __repr__(self):
        return f"Animal({self.name!r})"

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["sound"])

    @staticmethod
    def is_animal(obj):
        return isinstance(obj, Animal)

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Woof")
        self.breed = breed

    def speak(self):
        return super().speak() + "!"

# Dataclass
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0

    def dist(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

# Abstract base class
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r**2

# Magic methods
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, o): return Vector(self.x+o.x, self.y+o.y)
    def __mul__(self, s): return Vector(self.x*s, self.y*s)
    def __repr__(self): return f"Vector({self.x}, {self.y})"
    def __eq__(self, o): return self.x==o.x and self.y==o.y
    def __hash__(self): return hash((self.x, self.y))
```


---

# CHAPTER 6: MODULES AND STANDARD LIBRARY


## Key Modules

```python
import os, sys, json, re, math, random, datetime
from pathlib import Path
from collections import defaultdict, Counter, deque
from itertools import chain, product, combinations, islice

# os / pathlib
os.getcwd()
os.makedirs("dir", exist_ok=True)
Path("data/file.txt").read_text()
Path("out.txt").write_text("content")
list(Path(".").glob("*.py"))

# json
json.dumps({"key": "val"}, indent=2)
data = json.loads('{"x": 1}')

# re
re.findall(r"\d+", "abc 123 def 456")   # ['123','456']
re.sub(r"\s+", " ", "hello   world")
m = re.match(r"(\w+)@(\w+)", "user@host")
m.group(1)   # 'user'

# collections
dd = defaultdict(list)
dd["key"].append(1)
cnt = Counter("abracadabra")
cnt.most_common(3)
dq = deque([1,2,3], maxlen=5)
dq.appendleft(0)

# datetime
now = datetime.datetime.now()
delta = datetime.timedelta(days=7)
future = now + delta

# math
math.sqrt(16)
math.factorial(10)
math.gcd(12, 8)
math.log(100, 10)
```


---

# CHAPTER 7: FILE I/O AND EXCEPTIONS


## File Operations

```python
# Read
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
    lines = f.readlines()

# Write
with open("out.txt", "w") as f:
    f.write("Hello\n")
    f.writelines(["a\n", "b\n"])

# CSV
import csv
with open("data.csv") as f:
    for row in csv.DictReader(f):
        print(row)

# Exception handling
try:
    x = int("abc")
except ValueError as e:
    print(f"ValueError: {e}")
except (TypeError, KeyError):
    print("Type or Key error")
except Exception as e:
    raise RuntimeError("wrapped") from e
else:
    print("success")
finally:
    print("cleanup")

# Custom exception
class AppError(Exception):
    def __init__(self, msg, code=None):
        super().__init__(msg)
        self.code = code

# Context manager
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    t = time.time()
    yield
    print(f"Elapsed: {time.time()-t:.3f}s")

with timer():
    sum(range(10**6))
```


---

# CHAPTER 8: CONCURRENCY


## Threading and Async

```python
import threading, asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Threading
def worker(n):
    print(f"Worker {n}")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()

# ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as ex:
    results = list(ex.map(pow, [2]*10, range(10)))

# asyncio
async def fetch(url):
    await asyncio.sleep(0.1)
    return f"data:{url}"

async def main():
    results = await asyncio.gather(fetch("a"), fetch("b"), fetch("c"))
    print(results)

asyncio.run(main())

# async with / async for
async def producer():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i

async def consumer():
    async for item in producer():
        print(item)
```


---

# CHAPTER 9: ADVANCED PYTHON


## Metaclasses, Typing, Protocols

```python
# Type hints
from typing import List, Dict, Optional, Union, Callable, TypeVar, Protocol

T = TypeVar("T")

def first(lst: List[T]) -> Optional[T]:
    return lst[0] if lst else None

class Drawable(Protocol):
    def draw(self) -> None: ...

# __slots__
class Point:
    __slots__ = ("x", "y")
    def __init__(self, x, y): self.x, self.y = x, y

# Descriptor
class PositiveInt:
    def __set_name__(self, owner, name): self.name = name
    def __get__(self, obj, type=None): return obj.__dict__.get(self.name)
    def __set__(self, obj, val):
        if not isinstance(val, int) or val <= 0:
            raise ValueError(f"{self.name} must be positive int")
        obj.__dict__[self.name] = val

class Config:
    size = PositiveInt()

# Metaclass
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass

# Property
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self): return self._celsius

    @celsius.setter
    def celsius(self, val):
        if val < -273.15: raise ValueError("Below absolute zero")
        self._celsius = val

    @property
    def fahrenheit(self): return self._celsius * 9/5 + 32
```
