# Design Patterns GoF Complete Reference


---

# CHAPTER 1: CREATIONAL PATTERNS


## Remarks

The Gang of Four (GoF) — Gamma, Helm, Johnson, Vlissides — published "Design Patterns: Elements of Reusable Object-Oriented Software" in 1994. It catalogs 23 patterns divided into Creational (object creation), Structural (object composition), and Behavioral (object interaction). These patterns are language-agnostic solutions to recurring design problems. Modern languages have made some patterns trivial (Iterator, Observer via events) and others less relevant (Singleton is often an anti-pattern now). Focus on understanding WHEN to use each, not memorizing implementations.


## Singleton

```python
# Ensure only ONE instance of a class exists.
# WARNING: often an anti-pattern (global state, hard to test).
# Modern alternative: dependency injection.

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.connection = create_connection()
            self._initialized = True

# Better: module-level instance (Python modules are singletons)
# db.py
_db = None

def get_db():
    global _db
    if _db is None:
        _db = Database()
    return _db

# Best: just use dependency injection and create one instance
```


## Factory Method

```python
# Define interface for creating objects.
# Let subclasses decide which class to instantiate.

from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str): pass

class EmailNotification(Notification):
    def send(self, message):
        print(f"Email: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS: {message}")

class PushNotification(Notification):
    def send(self, message):
        print(f"Push: {message}")

# Factory method
class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        factories = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification,
        }
        cls = factories.get(channel)
        if not cls:
            raise ValueError(f"Unknown channel: {channel}")
        return cls()

# Usage
notifier = NotificationFactory.create("email")
notifier.send("Hello!")
```


## Abstract Factory

```python
# Create families of related objects without specifying concrete classes.

class Button(ABC):
    @abstractmethod
    def render(self): pass

class Checkbox(ABC):
    @abstractmethod
    def render(self): pass

# Light theme family
class LightButton(Button):
    def render(self): return "<button class='light'>Click</button>"

class LightCheckbox(Checkbox):
    def render(self): return "<input type='checkbox' class='light'/>"

# Dark theme family
class DarkButton(Button):
    def render(self): return "<button class='dark'>Click</button>"

class DarkCheckbox(Checkbox):
    def render(self): return "<input type='checkbox' class='dark'/>"

# Abstract factory
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: pass
    @abstractmethod
    def create_checkbox(self) -> Checkbox: pass

class LightThemeFactory(UIFactory):
    def create_button(self): return LightButton()
    def create_checkbox(self): return LightCheckbox()

class DarkThemeFactory(UIFactory):
    def create_button(self): return DarkButton()
    def create_checkbox(self): return DarkCheckbox()

# Client code doesn't know which theme it's using
def render_ui(factory: UIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    return button.render() + checkbox.render()
```


## Builder

```python
# Construct complex objects step by step.
# Separate construction from representation.

class QueryBuilder:
    def __init__(self):
        self._select = "*"
        self._from = ""
        self._where = []
        self._order_by = None
        self._limit = None

    def select(self, fields: str) -> "QueryBuilder":
        self._select = fields
        return self

    def from_table(self, table: str) -> "QueryBuilder":
        self._from = table
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._where.append(condition)
        return self

    def order_by(self, field: str, direction: str = "ASC") -> "QueryBuilder":
        self._order_by = f"{field} {direction}"
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._limit = n
        return self

    def build(self) -> str:
        query = f"SELECT {self._select} FROM {self._from}"
        if self._where:
            query += " WHERE " + " AND ".join(self._where)
        if self._order_by:
            query += f" ORDER BY {self._order_by}"
        if self._limit:
            query += f" LIMIT {self._limit}"
        return query

# Fluent API (method chaining)
sql = (QueryBuilder()
    .select("name, email")
    .from_table("users")
    .where("active = true")
    .where("age > 18")
    .order_by("name")
    .limit(10)
    .build())
# "SELECT name, email FROM users WHERE active = true AND age > 18 ORDER BY name ASC LIMIT 10"
```


## Prototype

```python
# Create objects by cloning an existing instance.
# Useful when construction is expensive.

import copy

class Config:
    def __init__(self):
        self.settings = {}
        self.plugins = []
        self.loaded_at = None

    def clone(self) -> "Config":
        return copy.deepcopy(self)

# Base config (expensive to create)
base_config = Config()
base_config.settings = load_from_file()   # Slow operation
base_config.plugins = discover_plugins()   # Slow operation

# Clone for each environment (fast!)
dev_config = base_config.clone()
dev_config.settings["debug"] = True

prod_config = base_config.clone()
prod_config.settings["debug"] = False
```


---

# CHAPTER 2: STRUCTURAL PATTERNS


## Adapter

```python
# Convert interface of one class to interface client expects.
# Makes incompatible interfaces work together.

# Legacy system returns XML
class LegacyPaymentGateway:
    def process_xml(self, xml_data: str) -> str:
        return "<response><status>OK</status></response>"

# Modern code expects JSON
class PaymentAdapter:
    def __init__(self, legacy: LegacyPaymentGateway):
        self.legacy = legacy

    def charge(self, amount: float, currency: str) -> dict:
        xml = f"<payment><amount>{amount}</amount><currency>{currency}</currency></payment>"
        xml_response = self.legacy.process_xml(xml)
        return {"status": "ok", "amount": amount}

# Client uses modern interface
adapter = PaymentAdapter(LegacyPaymentGateway())
result = adapter.charge(99.99, "USD")
```


## Decorator

```python
# Add behavior dynamically without modifying original class.
# Like wrapping a gift — each layer adds something.

class DataSource(ABC):
    @abstractmethod
    def write(self, data: str): pass
    @abstractmethod
    def read(self) -> str: pass

class FileDataSource(DataSource):
    def __init__(self, filename):
        self.filename = filename
    def write(self, data):
        with open(self.filename, 'w') as f: f.write(data)
    def read(self):
        with open(self.filename) as f: return f.read()

class EncryptionDecorator(DataSource):
    def __init__(self, source: DataSource):
        self.source = source
    def write(self, data):
        encrypted = self._encrypt(data)
        self.source.write(encrypted)
    def read(self):
        return self._decrypt(self.source.read())

class CompressionDecorator(DataSource):
    def __init__(self, source: DataSource):
        self.source = source
    def write(self, data):
        compressed = self._compress(data)
        self.source.write(compressed)
    def read(self):
        return self._decompress(self.source.read())

# Stack decorators (compression → encryption → file)
source = CompressionDecorator(
    EncryptionDecorator(
        FileDataSource("data.txt")
    )
)
source.write("sensitive data")   # Compressed → encrypted → written to file
```


## Facade

```python
# Simplified interface to a complex subsystem.

class VideoConverter:
    """Hides complexity of video conversion pipeline."""
    def convert(self, input_path: str, output_path: str, format: str):
        file = VideoFile(input_path)
        codec = CodecFactory.detect(file)
        buffer = BitrateReader.read(file, codec)
        result = BitrateReader.convert(buffer, codec)
        AudioMixer.fix(result)
        Encoder.encode(result, format, output_path)

# Client: one simple call instead of 6 complex steps
converter = VideoConverter()
converter.convert("input.mp4", "output.avi", "avi")
```


## Proxy

```python
# Control access to another object.

class DatabaseProxy:
    """Adds caching, logging, and access control to database."""
    def __init__(self, real_db: Database, user: User):
        self.real_db = real_db
        self.user = user
        self.cache = {}

    def query(self, sql: str):
        # Access control
        if not self.user.has_permission("read"):
            raise PermissionError("Not authorized")

        # Caching
        if sql in self.cache:
            return self.cache[sql]

        # Logging
        log.info(f"Query by {self.user.name}: {sql}")

        # Delegate to real database
        result = self.real_db.query(sql)
        self.cache[sql] = result
        return result

# Types of proxy:
#   Virtual:    lazy initialization (create heavy object only when needed)
#   Protection: access control (check permissions)
#   Caching:    cache results
#   Logging:    log all access
#   Remote:     represent remote object locally (RPC)
```


## Composite

```python
# Treat individual objects and compositions uniformly.
# Tree structures where leaves and branches share interface.

class FileSystemComponent(ABC):
    @abstractmethod
    def get_size(self) -> int: pass
    @abstractmethod
    def display(self, indent: int = 0): pass

class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def get_size(self): return self.size
    def display(self, indent=0):
        print(" " * indent + f"📄 {self.name} ({self.size}B)")

class Directory(FileSystemComponent):
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def get_size(self):
        return sum(child.get_size() for child in self.children)

    def display(self, indent=0):
        print(" " * indent + f"📁 {self.name} ({self.get_size()}B)")
        for child in self.children:
            child.display(indent + 2)

# Usage
root = Directory("src")
root.add(File("main.py", 1024))
root.add(File("utils.py", 512))
tests = Directory("tests")
tests.add(File("test_main.py", 768))
root.add(tests)
root.display()
root.get_size()   # 2304 (works for both files and directories)
```


## Bridge, Flyweight

```python
# BRIDGE: decouple abstraction from implementation.
# Two independent hierarchies that can vary independently.

class Renderer(ABC):
    @abstractmethod
    def render_circle(self, x, y, radius): pass

class SVGRenderer(Renderer):
    def render_circle(self, x, y, r):
        return f'<circle cx="{x}" cy="{y}" r="{r}"/>'

class CanvasRenderer(Renderer):
    def render_circle(self, x, y, r):
        return f'ctx.arc({x}, {y}, {r}, 0, 2*Math.PI)'

class Shape(ABC):
    def __init__(self, renderer: Renderer):
        self.renderer = renderer

class Circle(Shape):
    def __init__(self, renderer, x, y, radius):
        super().__init__(renderer)
        self.x, self.y, self.radius = x, y, radius

    def draw(self):
        return self.renderer.render_circle(self.x, self.y, self.radius)

# Shape × Renderer: don't need SVGCircle, CanvasCircle, SVGSquare, etc.
circle = Circle(SVGRenderer(), 10, 20, 5)


# FLYWEIGHT: share common state between many objects to save memory.
# Example: text editor — each character has font, size, color.
# Instead of storing per-char: share Font objects via flyweight pool.

class Font:
    _cache = {}

    @classmethod
    def get(cls, name, size, bold=False):
        key = (name, size, bold)
        if key not in cls._cache:
            cls._cache[key] = cls(name, size, bold)
        return cls._cache[key]

    def __init__(self, name, size, bold):
        self.name = name
        self.size = size
        self.bold = bold

# 1M characters, but only ~20 unique Font objects in memory
```


---

# CHAPTER 3: BEHAVIORAL PATTERNS


## Observer

```python
# When one object changes, notify all dependents automatically.
# Also called: Event, Listener, Pub/Sub.

class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)
        return self

    def off(self, event, callback):
        self._listeners.get(event, []).remove(callback)

    def emit(self, event, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)

class Store(EventEmitter):
    def __init__(self):
        super().__init__()
        self._items = []

    def add(self, item):
        self._items.append(item)
        self.emit("item_added", item)

    def remove(self, item):
        self._items.remove(item)
        self.emit("item_removed", item)

store = Store()
store.on("item_added", lambda item: print(f"Added: {item}"))
store.on("item_added", lambda item: update_ui(item))
store.on("item_added", lambda item: sync_to_server(item))
store.add("Widget")   # All three listeners fire
```


## Strategy

```python
# Define family of algorithms, make them interchangeable.
# Already covered in clean_code.md — brief recap.

class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data: bytes) -> bytes: pass

class GzipCompression(CompressionStrategy):
    def compress(self, data): return gzip.compress(data)

class Brotli(CompressionStrategy):
    def compress(self, data): return brotli.compress(data)

class NoCompression(CompressionStrategy):
    def compress(self, data): return data

class FileUploader:
    def __init__(self, compression: CompressionStrategy):
        self.compression = compression

    def upload(self, data: bytes):
        compressed = self.compression.compress(data)
        send_to_server(compressed)

# Swap algorithm at runtime
uploader = FileUploader(GzipCompression())
uploader = FileUploader(Brotli())
```


## Command

```python
# Encapsulate a request as an object.
# Enables: undo/redo, queuing, logging, macros.

class Command(ABC):
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def undo(self): pass

class InsertTextCommand(Command):
    def __init__(self, editor, text, position):
        self.editor = editor
        self.text = text
        self.position = position

    def execute(self):
        self.editor.insert(self.position, self.text)

    def undo(self):
        self.editor.delete(self.position, len(self.text))

class DeleteTextCommand(Command):
    def __init__(self, editor, position, length):
        self.editor = editor
        self.position = position
        self.length = length
        self.deleted_text = None

    def execute(self):
        self.deleted_text = self.editor.get_text(self.position, self.length)
        self.editor.delete(self.position, self.length)

    def undo(self):
        self.editor.insert(self.position, self.deleted_text)

# Command history for undo/redo
class CommandHistory:
    def __init__(self):
        self.history = []
        self.redo_stack = []

    def execute(self, command: Command):
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()

    def undo(self):
        if self.history:
            cmd = self.history.pop()
            cmd.undo()
            self.redo_stack.append(cmd)

    def redo(self):
        if self.redo_stack:
            cmd = self.redo_stack.pop()
            cmd.execute()
            self.history.append(cmd)
```


## Iterator

```python
# Access elements sequentially without exposing internal structure.
# Python has this built-in with __iter__ and __next__.

class Range:
    def __init__(self, start, end, step=1):
        self.start = start
        self.end = end
        self.step = step

    def __iter__(self):
        current = self.start
        while current < self.end:
            yield current
            current += self.step

for num in Range(0, 10, 2):
    print(num)   # 0, 2, 4, 6, 8

# Generators are iterators (lazy evaluation)
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Take first 10
from itertools import islice
list(islice(fibonacci(), 10))   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```


## State

```python
# Object behaves differently depending on internal state.
# State transitions are explicit and encapsulated.

class OrderState(ABC):
    @abstractmethod
    def pay(self, order): pass
    @abstractmethod
    def ship(self, order): pass
    @abstractmethod
    def cancel(self, order): pass

class DraftState(OrderState):
    def pay(self, order):
        order.state = PaidState()
        print("Order paid!")
    def ship(self, order):
        raise ValueError("Can't ship unpaid order")
    def cancel(self, order):
        order.state = CancelledState()
        print("Order cancelled")

class PaidState(OrderState):
    def pay(self, order):
        raise ValueError("Already paid")
    def ship(self, order):
        order.state = ShippedState()
        print("Order shipped!")
    def cancel(self, order):
        order.state = CancelledState()
        print("Order cancelled, refund issued")

class ShippedState(OrderState):
    def pay(self, order): raise ValueError("Already paid")
    def ship(self, order): raise ValueError("Already shipped")
    def cancel(self, order): raise ValueError("Can't cancel shipped order")

class Order:
    def __init__(self):
        self.state = DraftState()
    def pay(self): self.state.pay(self)
    def ship(self): self.state.ship(self)
    def cancel(self): self.state.cancel(self)

order = Order()
order.pay()      # "Order paid!"
order.ship()     # "Order shipped!"
order.cancel()   # ValueError: Can't cancel shipped order
```


## Template Method, Chain of Responsibility, Mediator, Memento, Visitor

```python
# TEMPLATE METHOD: define skeleton, subclasses fill in steps.
class DataMiner(ABC):
    def mine(self, path):        # Template method (fixed structure)
        data = self.extract(path)
        parsed = self.parse(data)
        analyzed = self.analyze(parsed)
        self.report(analyzed)

    @abstractmethod
    def extract(self, path): pass
    @abstractmethod
    def parse(self, data): pass

    def analyze(self, data):    # Default implementation
        return {"count": len(data)}

    def report(self, analysis):  # Default implementation
        print(analysis)

class CSVMiner(DataMiner):
    def extract(self, path): return open(path).read()
    def parse(self, data): return data.split('\n')

class PDFMiner(DataMiner):
    def extract(self, path): return extract_pdf_text(path)
    def parse(self, data): return data.split('\n\n')


# CHAIN OF RESPONSIBILITY: pass request along chain of handlers.
class Handler(ABC):
    def __init__(self, next_handler=None):
        self.next = next_handler
    def handle(self, request):
        if self.can_handle(request):
            return self.process(request)
        if self.next:
            return self.next.handle(request)
        raise ValueError("No handler found")
    @abstractmethod
    def can_handle(self, request) -> bool: pass
    @abstractmethod
    def process(self, request): pass

class AuthHandler(Handler):
    def can_handle(self, req): return not req.get("authenticated")
    def process(self, req): raise PermissionError("Not authenticated")

class RateLimitHandler(Handler):
    def can_handle(self, req): return req.get("rate_exceeded")
    def process(self, req): raise ValueError("Rate limit exceeded")

class BusinessHandler(Handler):
    def can_handle(self, req): return True
    def process(self, req): return {"result": "processed"}

# Build chain: auth → rate limit → business logic
chain = AuthHandler(RateLimitHandler(BusinessHandler()))
chain.handle({"authenticated": True, "rate_exceeded": False})


# MEDIATOR: centralized communication between components.
# Instead of A→B, A→C, B→C (mesh), all go through Mediator.
# Example: chat room mediates between users.
# Example: Redux store mediates between React components.


# MEMENTO: capture and restore object state (undo).
# Already shown in Command pattern with history.
# Save state snapshots, restore when needed.


# VISITOR: add operations to objects without modifying them.
class NodeVisitor(ABC):
    @abstractmethod
    def visit_number(self, node): pass
    @abstractmethod
    def visit_string(self, node): pass

class PrintVisitor(NodeVisitor):
    def visit_number(self, node): print(f"Number: {node.value}")
    def visit_string(self, node): print(f"String: '{node.value}'")

class NumberNode:
    def __init__(self, value): self.value = value
    def accept(self, visitor): visitor.visit_number(self)

class StringNode:
    def __init__(self, value): self.value = value
    def accept(self, visitor): visitor.visit_string(self)
```


---

# CHAPTER 4: WHEN TO USE WHICH


## Pattern Selection Guide

```
CREATING OBJECTS:
  "I need one instance"              → Singleton (or just DI)
  "I need to create family of objects" → Abstract Factory
  "I need to create one of many types" → Factory Method
  "Construction is complex/step-by-step" → Builder
  "Cloning is cheaper than creating" → Prototype

COMPOSING OBJECTS:
  "Wrap existing class to add behavior"  → Decorator
  "Make incompatible interfaces work"    → Adapter
  "Simplify complex subsystem"           → Facade
  "Control access to object"             → Proxy
  "Treat single/group uniformly (tree)"  → Composite
  "Decouple abstraction from impl"       → Bridge
  "Share common state to save memory"    → Flyweight

MANAGING BEHAVIOR:
  "React to state changes (events)"      → Observer
  "Swap algorithm at runtime"            → Strategy
  "Undo/redo, queue commands"            → Command
  "Access collection without exposing"   → Iterator
  "Behavior changes based on state"      → State
  "Define skeleton, subclasses fill in"  → Template Method
  "Pass request through handler chain"   → Chain of Responsibility
  "Centralize communication"             → Mediator
  "Save/restore state snapshots"         → Memento
  "Add operations without modifying"     → Visitor

MODERN ALTERNATIVES:
  Singleton → dependency injection container
  Observer → built-in events, RxJS, signals
  Iterator → generators, for-of, streams
  Strategy → first-class functions (pass function, not class)
  Template Method → composition over inheritance
  Command → closures with undo state
  State → discriminated unions + switch (TypeScript)
```


## Common Pitfalls

```
PITFALL 1: Pattern-itis
  Using patterns everywhere, even when unnecessary.
  Fix: YAGNI. Use a pattern when it solves a REAL problem.

PITFALL 2: Wrong pattern choice
  Using Singleton when you need Factory. Using Decorator when Proxy fits.
  Fix: understand the PROBLEM each pattern solves, not just the structure.

PITFALL 3: Over-abstraction
  AbstractFactoryProviderBuilderStrategy for a simple config.
  Fix: start concrete, refactor to patterns when complexity demands it.

PITFALL 4: Ignoring language features
  Writing Strategy pattern in Python when a function parameter suffices.
  Fix: first-class functions, closures, and decorators replace many patterns.

PITFALL 5: Singleton as global state
  Everything accesses Singleton.getInstance() → coupled, untestable.
  Fix: dependency injection. Pass dependencies explicitly.
```