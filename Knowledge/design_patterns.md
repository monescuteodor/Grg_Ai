# Design Patterns and Software Architecture Complete Reference

## SOLID Principles

The foundation of good object-oriented design:

S — Single Responsibility Principle (SRP): a class should have only one reason to change. One class = one job. Split classes that do too much.

O — Open/Closed Principle (OCP): open for extension, closed for modification. Add new behavior by adding code (subclasses, strategy objects), not by editing existing code.

L — Liskov Substitution Principle (LSP): subclasses must be substitutable for their base class without breaking the program. Overriding methods must not weaken preconditions or strengthen postconditions.

I — Interface Segregation Principle (ISP): many specific interfaces are better than one general-purpose interface. Clients should not be forced to implement methods they do not use.

D — Dependency Inversion Principle (DIP): high-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces). Abstractions should not depend on details.

DRY — Don't Repeat Yourself: every piece of knowledge should have a single representation. Duplication leads to inconsistency.
YAGNI — You Aren't Gonna Need It: don't add functionality until it's needed.
KISS — Keep It Simple, Stupid: simple is better than complex.

## Creational Patterns

Creational patterns deal with object creation, making it more flexible and decoupled.

### Singleton
Ensures only one instance of a class exists; provides global access point.
Use when: logging, configuration, thread pools, caches, device drivers.
Implementation: private constructor, static getInstance() method that creates instance only once.
Thread-safe variants: synchronized method, double-checked locking, enum-based, initialization-on-demand holder.
Warning: can make code hard to test (global state). Prefer dependency injection.

```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Factory Method
Define an interface for creating objects, let subclasses decide which class to instantiate.
Use when: you don't know ahead of time which class you need to instantiate; subclasses should control what they create.
Creator class has abstract factoryMethod(); each ConcreteCreator implements it differently.

### Abstract Factory
Create families of related objects without specifying their concrete classes.
Use when: system must be independent of how its products are created; you need families of related objects.
Example: UI toolkit — WindowsFactory creates WindowsButton + WindowsCheckbox; MacFactory creates MacButton + MacCheckbox.

### Builder
Separate the construction of a complex object from its representation.
Use when: constructing complex objects step by step; same construction process should create different representations; avoid telescoping constructors.
Director orchestrates the building; Builder defines steps; ConcreteBuilder implements steps.

```python
class QueryBuilder:
    def __init__(self): self._query = {}
    def select(self, cols): self._query['select'] = cols; return self
    def from_table(self, t): self._query['from'] = t; return self
    def where(self, cond): self._query['where'] = cond; return self
    def build(self): return self._query
# Usage: query = QueryBuilder().select('*').from_table('users').where('id=1').build()
```

### Prototype
Clone existing objects without coupling to their specific classes.
Use when: object creation is expensive; you need copies of complex objects.
Shallow copy vs Deep copy. Each object implements a clone() method.

## Structural Patterns

Structural patterns deal with object composition, creating relationships between objects.

### Adapter
Convert the interface of a class into another interface clients expect. Makes incompatible interfaces work together.
Use when: integrating legacy code or third-party libraries with incompatible interfaces.
Object adapter (composition): adapter wraps adaptee, delegates calls.
Class adapter (multiple inheritance): adapter inherits from both target and adaptee.

### Decorator
Attach additional responsibilities to an object dynamically. Flexible alternative to subclassing.
Use when: you want to add behavior to individual objects without affecting others; subclassing would lead to class explosion.
Wraps the original object, calls it, adds behavior before/after. Stackable.
Example: Java I/O streams — BufferedReader(FileReader(file)).

```python
class LoggingDecorator:
    def __init__(self, service):
        self._service = service
    def operation(self):
        print("Logging: before")
        result = self._service.operation()
        print("Logging: after")
        return result
```

### Facade
Provide a simplified interface to a complex subsystem.
Use when: you want to provide a simple interface to a complex body of code; you want to reduce dependencies on internal components.
Client talks only to the facade; facade delegates to subsystem classes.
Example: home theater system — one Facade.watchMovie() replaces calling projector, dvd player, sound system, lights separately.

### Proxy
Provide a surrogate or placeholder for another object. Control access to it.
Types:
- Virtual proxy: delays expensive object creation until needed (lazy initialization).
- Protection proxy: controls access rights.
- Remote proxy: represents an object in a different address space (RPC, REST client).
- Caching proxy: caches results of expensive operations.
- Logging proxy: records calls to the real object.

### Composite
Compose objects into tree structures to represent part-whole hierarchies. Treat individual objects and compositions uniformly.
Use when: you want clients to ignore the difference between compositions and individual objects.
Example: file system — File and Directory both implement Component. Directory holds a list of Components.

### Bridge
Decouple an abstraction from its implementation so both can vary independently.
Use when: you want to avoid permanent binding between abstraction and implementation; both should be extensible via subclassing.
Abstraction holds reference to an Implementor. Different combinations without class explosion.

### Flyweight
Use sharing to support large numbers of fine-grained objects efficiently.
Use when: you have a very large number of objects consuming too much memory; objects have shared intrinsic state and external extrinsic state.
Example: text editor — share Character objects for each letter of the alphabet; position is extrinsic.

## Behavioral Patterns

Behavioral patterns deal with communication and responsibility between objects.

### Observer (Event / Publish-Subscribe)
Define a one-to-many dependency so when one object changes state, all dependents are notified.
Use when: changes to one object require updating others; you don't know how many objects need to change.
Subject maintains list of Observers; calls update() on each when state changes.
Event-driven systems, MVC (Model notifies View), React state, Redux, DOM events.

```python
class EventEmitter:
    def __init__(self): self._handlers = {}
    def on(self, event, fn): self._handlers.setdefault(event, []).append(fn)
    def emit(self, event, *args):
        for fn in self._handlers.get(event, []): fn(*args)
```

### Strategy
Define a family of algorithms, encapsulate each, make them interchangeable.
Use when: you want to switch algorithms at runtime; you have related classes that differ only in behavior; you want to eliminate conditionals.
Context holds a reference to a Strategy interface; delegates the algorithm to it.
Example: sorting strategy, payment strategy (CreditCard/PayPal/Bitcoin), compression strategy.

### Command
Encapsulate a request as an object. Supports undo/redo, queuing, logging.
Use when: parameterize objects with operations; queue or log requests; implement undoable operations.
Command has execute() and undo(). Invoker calls execute(). Receiver does the actual work.
Example: text editor (each keystroke is a Command object stored in a history stack).

### Template Method
Define the skeleton of an algorithm in a base class; defer some steps to subclasses.
Use when: you have invariant parts of an algorithm and variant parts; avoid code duplication.
Base class defines the template with abstract methods; subclasses override only the variant steps.

### Iterator
Provide a way to sequentially access elements without exposing the underlying representation.
Use when: you want a standard way to traverse different collection types.
Python: __iter__ and __next__; Java: Iterator<T>; C++: begin()/end().

### State
Allow an object to alter its behavior when its internal state changes.
Use when: an object's behavior depends on state and must change at runtime; large conditional statements based on state.
Context delegates behavior to current State object. State transitions happen inside State or Context.
Example: vending machine, traffic light, order processing (PENDING → PROCESSING → SHIPPED → DELIVERED).

### Chain of Responsibility
Pass request along a chain of handlers; each decides to process or pass along.
Use when: more than one object can handle a request; the set of handlers should be specifiable dynamically.
Example: middleware pipeline in web frameworks, exception handling, event bubbling in DOM.

### Mediator
Define an object that encapsulates how a set of objects interact. Promotes loose coupling.
Use when: many objects communicate in complex ways, resulting in tight coupling.
Objects communicate through the mediator instead of directly. Air traffic control is classic example.

### Memento
Capture and externalize an object's internal state so it can be restored later, without violating encapsulation.
Use when: you need to implement undo/redo; snapshots of an object's state.
Originator creates Mementos. Caretaker stores and retrieves them.

### Visitor
Add new operations to objects without changing their classes.
Use when: you want to perform many distinct and unrelated operations on an object structure.
Visitor implements an operation for each concrete element type. Elements accept a Visitor.
Example: AST (Abstract Syntax Tree) traversal — different visitors for type checking, code generation, pretty-printing.

## Architectural Patterns

### MVC — Model-View-Controller
Model: data and business logic. View: UI, presentation. Controller: handles input, updates model.
Used in: web frameworks (Rails, Django, Spring MVC), desktop GUIs.
Flow: User → Controller → Model → View (notifies) → User.

### MVP — Model-View-Presenter
Like MVC but Presenter handles all presentation logic; View is passive (dumb).
View interface lets Presenter be tested without UI. Used in: Android (older), WinForms.

### MVVM — Model-View-ViewModel
ViewModel exposes data streams/bindings that the View observes automatically.
View has no logic. Used in: WPF, Angular, React + MobX, SwiftUI, Flutter.

### Repository Pattern
Abstract data access behind an interface. Business logic doesn't know if data comes from SQL, MongoDB, or a file.
IUserRepository with findById(), save(), delete(). Concrete: SqlUserRepository, MongoUserRepository.
Enables easy testing (swap with in-memory fake repository).

### Service Layer
Define an application's boundary with a layer of services. Each service encapsulates a use case.
Controller → Service → Repository → Database.
Services are transaction boundaries and orchestrate business logic.

### CQRS — Command Query Responsibility Segregation
Separate read (Query) and write (Command) operations. Different models for reading and writing.
Commands: change state, no return value. Queries: return data, no side effects.
Scales reads and writes independently. Often paired with Event Sourcing.

### Event Sourcing
Store state as a sequence of events instead of current state. Reconstruct current state by replaying events.
Benefits: full audit log, time travel, easy event-driven integration.
Example: bank account stores DEPOSIT, WITHDRAW events, not just the balance.

### Hexagonal Architecture (Ports and Adapters)
Core application logic in the center. Ports (interfaces) connect core to the outside world. Adapters implement ports.
Separates domain from infrastructure (database, UI, APIs). Highly testable.

### Microservices vs Monolith
Monolith: single deployable unit. Simpler to develop, deploy, debug. Scales as one unit.
Microservices: separate services for each business capability. Independent deployment, scaling, technology choices. Complex operations.
When to use microservices: large teams, services with very different scaling needs, need for independent deployments.

## Clean Code Principles

Naming: use intention-revealing names. Avoid abbreviations. Use nouns for classes, verbs for methods.
Functions: small (do one thing), no side effects, descriptive names, few parameters (≤3).
Comments: explain WHY not WHAT. Good code is self-documenting. Avoid commented-out code.
Error handling: use exceptions not error codes. Don't return null — return empty collections or Optional. Fail fast.
Classes: small, single purpose. High cohesion (methods use the same instance variables).
Formatting: consistent indentation, small files, blank lines between logical sections.
Tests: FIRST — Fast, Independent, Repeatable, Self-validating, Timely.

Code smells (things to refactor):
- Long method: extract into smaller methods.
- Large class: split into multiple classes.
- Long parameter list: introduce parameter object or builder.
- Duplicate code: extract to shared method or class.
- Dead code: delete it.
- Feature envy: method uses another class's data more than its own — move it.
- Data clumps: groups of data that always appear together — create a class.
- Primitive obsession: overuse of primitives — create value objects.
- Switch statements: replace with polymorphism.
- Speculative generality: code for hypothetical future needs — YAGNI.

## Dependency Injection and IoC

Inversion of Control (IoC): don't create dependencies yourself, receive them from outside.
Dependency Injection: pass dependencies (services) into an object rather than having it create them.

Types:
- Constructor injection: dependencies passed via constructor (preferred).
- Setter injection: dependencies set via setters after construction.
- Interface injection: component implements interface that allows injector to push dependencies.

Benefits: loose coupling, easier testing (inject mocks), easier to swap implementations.

IoC Containers: frameworks that manage object creation and wiring.
Examples: Spring (Java), .NET Core DI, Angular DI, Dagger (Android).

```python
# Without DI — tightly coupled
class OrderService:
    def __init__(self): self.repo = MySQLOrderRepository()  # hard-coded

# With DI — loosely coupled
class OrderService:
    def __init__(self, repo: OrderRepository): self.repo = repo  # injected
```

## Testing Patterns

Unit test: test a single unit (class/function) in isolation. Mock all dependencies.
Integration test: test interaction between components (e.g., service + real database).
End-to-end (E2E) test: test full user flows through the entire system.

Test pyramid: many unit tests, fewer integration tests, few E2E tests. Inversely proportional to cost.

AAA pattern (Arrange-Act-Assert):
Arrange: set up test data and dependencies.
Act: call the function/method being tested.
Assert: verify the output or behavior.

Test doubles:
- Mock: pre-programmed with expectations; verifies interactions.
- Stub: returns hardcoded responses to calls.
- Fake: working implementation (e.g., in-memory database).
- Spy: real object but records calls.
- Dummy: passed but never used; satisfies parameter requirements.

TDD — Test Driven Development: Red → Green → Refactor.
Write a failing test → write minimum code to pass → refactor.

BDD — Behavior Driven Development: describe behavior in plain language.
Given (context) → When (action) → Then (outcome). Tools: Cucumber, Jasmine, RSpec.

## API Design

REST (Representational State Transfer) principles:
- Stateless: each request contains all needed information.
- Uniform interface: consistent resource naming and HTTP methods.
- Client-server separation.
- Cacheable responses.
- Layered system.

HTTP methods: GET (read), POST (create), PUT (full update), PATCH (partial update), DELETE (remove).
Status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable Entity, 500 Internal Server Error.

REST URL conventions:
- Collections: GET /users, POST /users
- Items: GET /users/{id}, PUT /users/{id}, DELETE /users/{id}
- Nested: GET /users/{id}/orders
- Filtering: GET /users?role=admin&active=true
- Pagination: GET /users?page=2&limit=20
- Versioning: /api/v1/users or via Accept header

GraphQL: query language for APIs. Client requests exactly the data it needs.
- Query: read data. Mutation: write data. Subscription: real-time updates.
- Single endpoint. No over-fetching or under-fetching.

gRPC: high-performance RPC framework using Protocol Buffers (binary serialization).
- Strongly typed. Code generation. HTTP/2. Bi-directional streaming. Best for microservices.

WebSockets: full-duplex communication over a persistent connection. For real-time apps (chat, live updates, gaming).
