# Clean Code and SOLID Principles Complete Reference


---

# CHAPTER 1: CLEAN CODE FUNDAMENTALS


## Remarks

Clean code is code that is easy to read, understand, and modify. The term was popularized by Robert C. Martin's book "Clean Code" (2008). Clean code is not about cleverness — it's about clarity. The best code reads like well-written prose. You spend 10x more time READING code than writing it, so optimize for readability.

Key concepts: **Naming** (intention-revealing names), **Functions** (small, single purpose), **DRY** (Don't Repeat Yourself), **KISS** (Keep It Simple), **YAGNI** (You Aren't Gonna Need It), **SOLID** (5 OOP principles), **Code smells** (indicators of bad design), **Refactoring** (improving structure without changing behavior), **Design patterns** (proven solutions to common problems).

Used by: every professional developer. Code review standards at Google, Meta, and Stripe are essentially clean code checklists.

Books: "Clean Code" by Robert Martin, "Refactoring" by Martin Fowler, "A Philosophy of Software Design" by John Ousterhout, "The Pragmatic Programmer" by Hunt/Thomas.


## Naming — The Foundation

```python
# ──── VARIABLES ────

# BAD: meaningless, abbreviated, misleading
d = 5                      # What is d?
tmp = get_data()           # Temporary what?
flag = True                # Flag for what?
lst = []                   # list of what?
data2 = process(data1)     # data1 and data2 tell nothing

# GOOD: intention-revealing, pronounceable, searchable
elapsed_days = 5
active_users = get_active_users()
is_authenticated = True
pending_orders = []
filtered_products = apply_discount(raw_products)


# ──── FUNCTIONS ────

# BAD: vague, too generic
def do_stuff(x):
    pass

def handle(data):
    pass

def process(items):
    pass

# GOOD: verb + noun, describes what it DOES
def calculate_shipping_cost(order):
    pass

def send_welcome_email(user):
    pass

def validate_credit_card(card_number):
    pass


# ──── BOOLEANS ────

# BAD
status = True
open = True
val = check(user)

# GOOD: is/has/can/should prefix (reads like English)
is_active = True
has_permission = True
can_edit = check_edit_permission(user)
should_retry = attempt_count < max_retries


# ──── CLASSES ────

# BAD: vague, suffix-itis
DataManager
UserHelper
OrderProcessor
BaseService
AbstractHandler

# GOOD: specific nouns describing what it IS
ShoppingCart
InvoiceGenerator
EmailSender
PasswordValidator
UserRepository


# ──── CONSTANTS ────

# BAD: magic numbers/strings
if retry_count > 3:
    pass

timeout = 86400

if status == "A":
    pass

# GOOD: named constants
MAX_RETRY_ATTEMPTS = 3
SECONDS_PER_DAY = 86400
STATUS_ACTIVE = "A"

if retry_count > MAX_RETRY_ATTEMPTS:
    pass


# ──── CONTEXT ────

# Avoid unnecessary prefixes in classes
class User:
    user_name = ""       # BAD: "user" prefix redundant inside User class
    user_email = ""

class User:
    name = ""            # GOOD: context is the class itself
    email = ""
```


## Functions — Small and Focused

```python
# ──── SIZE ────
# Functions should be 5-20 lines. If longer, extract.

# BAD: 50-line function doing everything
def process_order(order):
    # validate order (10 lines)
    # calculate totals (10 lines)
    # apply discounts (10 lines)
    # charge payment (10 lines)
    # send confirmation (10 lines)
    pass

# GOOD: each step is its own function
def process_order(order):
    validate_order(order)
    totals = calculate_totals(order)
    final_price = apply_discounts(totals, order.coupons)
    charge_payment(order.payment_method, final_price)
    send_order_confirmation(order)


# ──── SINGLE RESPONSIBILITY ────
# A function should do ONE thing and do it well.

# BAD: does validation AND saving AND emailing
def create_user(data):
    if not data.get("email"):
        raise ValueError("Email required")
    if not "@" in data["email"]:
        raise ValueError("Invalid email")
    user = db.insert("users", data)
    smtp.send(data["email"], "Welcome!", "...")
    return user

# GOOD: separated concerns
def create_user(data):
    validated = validate_user_data(data)
    user = save_user(validated)
    send_welcome_email(user)
    return user


# ──── ARGUMENTS ────
# Fewer arguments = better. 0-2 ideal. 3 max. More → use object.

# BAD: too many arguments
def create_user(name, email, age, role, department, manager_id, start_date):
    pass

# GOOD: use a data object
@dataclass
class CreateUserRequest:
    name: str
    email: str
    age: int
    role: str = "employee"
    department: str = ""
    manager_id: str = None
    start_date: date = None

def create_user(request: CreateUserRequest):
    pass


# ──── NO SIDE EFFECTS ────
# Functions should either return a value OR have a side effect, not both.

# BAD: modifies input AND returns something
def add_tax(items):
    for item in items:
        item.price *= 1.2    # Mutates! Caller might not expect this.
    return items

# GOOD: pure function (no mutation)
def add_tax(items):
    return [
        {**item, "price": item["price"] * 1.2}
        for item in items
    ]


# ──── AVOID FLAG ARGUMENTS ────
# Boolean argument = function does 2 things.

# BAD
def send_notification(user, is_urgent):
    if is_urgent:
        send_sms(user)
    else:
        send_email(user)

# GOOD: two clear functions
def send_urgent_notification(user):
    send_sms(user)

def send_regular_notification(user):
    send_email(user)
```


## Comments — When and When Not

```python
# ──── BAD COMMENTS (most comments) ────

# Redundant (says what code already says)
i += 1   # Increment i by 1

# Misleading
# Returns the user's age
def get_user_name(user):    # Actually returns name, not age!
    return user.name

# Commented-out code (use version control!)
# def old_function():
#     pass
# TODO: maybe use this later???

# Journal comments
# 2024-01-15: Added validation (John)
# 2024-01-16: Fixed bug in validation (Jane)
# Git blame does this better

# Closing brace comments
if condition:
    for item in items:
        if item.valid:
            process(item)
        # end if
    # end for
# end if
# → Your function is too long if you need these!


# ──── GOOD COMMENTS (rare but valuable) ────

# WHY, not WHAT (explain reasoning behind non-obvious decisions)
# We use a 30-second timeout because the payment gateway
# occasionally takes 20+ seconds under heavy load.
PAYMENT_TIMEOUT = 30

# Legal/license headers
# Copyright 2026 MyCompany. MIT License.

# Warning of consequences
# WARNING: This drops the entire database. Only use in test environment.
def reset_database():
    pass

# TODO with ticket reference
# TODO(PROJ-123): Replace with cursor pagination before launch

# Regex explanation
# Matches: user_123, admin_456 (type + underscore + digits)
USER_ID_PATTERN = re.compile(r'^[a-z]+_\d+$')

# API documentation (docstrings)
def calculate_compound_interest(
    principal: float,
    rate: float,
    years: int,
    compounds_per_year: int = 12,
) -> float:
    """
    Calculate compound interest.

    Args:
        principal: Initial investment amount
        rate: Annual interest rate (0.05 = 5%)
        years: Number of years
        compounds_per_year: Compounding frequency (default: monthly)

    Returns:
        Final amount after compound interest

    Example:
        >>> calculate_compound_interest(1000, 0.05, 10)
        1647.01
    """
    return principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
```


---

# CHAPTER 2: SOLID PRINCIPLES


## S — Single Responsibility Principle

```python
# A class should have ONE reason to change.

# BAD: User class does authentication, validation, persistence, AND formatting
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def validate(self):
        if "@" not in self.email:
            raise ValueError("Invalid email")

    def hash_password(self):
        self.password = bcrypt.hash(self.password)

    def save_to_database(self):
        db.execute("INSERT INTO users ...", self.name, self.email)

    def send_welcome_email(self):
        smtp.send(self.email, "Welcome!", "...")

    def to_json(self):
        return json.dumps({"name": self.name, "email": self.email})


# GOOD: each class has one responsibility
class User:
    """Domain entity — just holds data and business rules."""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserValidator:
    """Validates user data."""
    def validate(self, user: User) -> list[str]:
        errors = []
        if "@" not in user.email:
            errors.append("Invalid email")
        return errors

class UserRepository:
    """Handles persistence."""
    def save(self, user: User) -> User:
        return db.execute("INSERT INTO users ...", user.name, user.email)

class WelcomeEmailSender:
    """Handles email notifications."""
    def send(self, user: User):
        smtp.send(user.email, "Welcome!", f"Hi {user.name}!")

class UserSerializer:
    """Handles serialization."""
    def to_json(self, user: User) -> str:
        return json.dumps({"name": user.name, "email": user.email})
```


## O — Open/Closed Principle

```python
# Open for extension, closed for modification.
# Add new behavior WITHOUT changing existing code.

# BAD: must modify calculate_area every time a new shape is added
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    elif shape.type == "triangle":
        return 0.5 * shape.base * shape.height
    # Adding new shape? Must modify this function.

# GOOD: extend by adding new classes, not modifying existing code
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

# Adding Pentagon? Just add a new class. Nothing else changes.
class Pentagon(Shape):
    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return (5 * self.side ** 2) / (4 * (5 - 2 * 5 ** 0.5) ** 0.5)


# REAL-WORLD: Payment processors
class PaymentProcessor(ABC):
    @abstractmethod
    async def charge(self, amount: float, currency: str) -> PaymentResult:
        pass

class StripeProcessor(PaymentProcessor):
    async def charge(self, amount, currency):
        return await stripe.charges.create(amount=amount, currency=currency)

class PayPalProcessor(PaymentProcessor):
    async def charge(self, amount, currency):
        return await paypal.payments.create(amount=amount, currency=currency)

# Adding new processor doesn't change existing code
class CryptoProcessor(PaymentProcessor):
    async def charge(self, amount, currency):
        return await crypto_gateway.pay(amount, currency)
```


## L — Liskov Substitution Principle

```python
# Subtypes must be substitutable for their base types.
# If code works with Base, it must work with any Derived.

# BAD: Square violates Rectangle contract
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    @property
    def width(self):
        return self._side

    @width.setter
    def width(self, value):
        self._side = value    # Also changes height!

    @property
    def height(self):
        return self._side

    @height.setter
    def height(self, value):
        self._side = value    # Also changes width!

# Problem:
def test_area(rect: Rectangle):
    rect.width = 5
    rect.height = 4
    assert rect.area() == 20   # FAILS for Square! (area = 16)

# GOOD: don't make Square inherit Rectangle
# They're both shapes, but Rectangle IS NOT a supertype of Square
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2
```


## I — Interface Segregation Principle

```python
# Clients should not depend on interfaces they don't use.
# Many specific interfaces > one fat interface.

# BAD: one fat interface forces implementation of unused methods
class Worker(ABC):
    @abstractmethod
    def code(self): pass

    @abstractmethod
    def test(self): pass

    @abstractmethod
    def design(self): pass

    @abstractmethod
    def manage(self): pass

class Developer(Worker):
    def code(self): return "Writing code"
    def test(self): return "Writing tests"
    def design(self): raise NotImplementedError   # Doesn't design!
    def manage(self): raise NotImplementedError   # Doesn't manage!


# GOOD: segregated interfaces
class Coder(ABC):
    @abstractmethod
    def code(self): pass

class Tester(ABC):
    @abstractmethod
    def test(self): pass

class Designer(ABC):
    @abstractmethod
    def design(self): pass

class Manager(ABC):
    @abstractmethod
    def manage(self): pass

class Developer(Coder, Tester):
    def code(self): return "Writing code"
    def test(self): return "Writing tests"

class UXDesigner(Designer):
    def design(self): return "Creating mockups"

class TechLead(Coder, Manager):
    def code(self): return "Writing code"
    def manage(self): return "Leading team"
```


## D — Dependency Inversion Principle

```python
# High-level modules should not depend on low-level modules.
# Both should depend on abstractions.

# BAD: high-level OrderService directly depends on low-level MySQLDatabase
class MySQLDatabase:
    def save(self, data):
        mysql.execute("INSERT INTO ...", data)

class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()    # Tight coupling!

    def create_order(self, order):
        self.db.save(order)
        # Can't switch to PostgreSQL without changing OrderService!


# GOOD: both depend on abstraction
class Database(ABC):
    @abstractmethod
    def save(self, data): pass

    @abstractmethod
    def find(self, id): pass

class MySQLDatabase(Database):
    def save(self, data):
        mysql.execute("INSERT INTO ...", data)

    def find(self, id):
        return mysql.query("SELECT * FROM ... WHERE id = ?", id)

class PostgresDatabase(Database):
    def save(self, data):
        pg.execute("INSERT INTO ...", data)

    def find(self, id):
        return pg.query("SELECT * FROM ... WHERE id = $1", id)

class OrderService:
    def __init__(self, db: Database):        # Depends on abstraction!
        self.db = db

    def create_order(self, order):
        self.db.save(order)

# Now switch databases without touching OrderService:
service = OrderService(MySQLDatabase())      # MySQL
service = OrderService(PostgresDatabase())   # PostgreSQL
service = OrderService(InMemoryDatabase())   # Testing!
```


---

# CHAPTER 3: CODE SMELLS


## Common Code Smells

```python
# ──── SMELL 1: Long Method ────
# Function > 20 lines → extract smaller functions

# ──── SMELL 2: God Class ────
# Class does everything → split by responsibility
# Signs: 500+ lines, 20+ methods, "Manager" or "Service" in name

# ──── SMELL 3: Feature Envy ────
# Method uses more data from another class than its own
# BAD:
def calculate_bonus(employee):
    return employee.department.budget * employee.department.bonus_rate * employee.years

# GOOD: move to the class that owns the data
class Department:
    def calculate_bonus(self, employee):
        return self.budget * self.bonus_rate * employee.years


# ──── SMELL 4: Data Clumps ────
# Same group of variables always appears together
# BAD:
def create_address(street, city, state, zip_code, country):
    pass

def validate_address(street, city, state, zip_code, country):
    pass

# GOOD: group into a class
@dataclass
class Address:
    street: str
    city: str
    state: str
    zip_code: str
    country: str

def create_address(address: Address):
    pass


# ──── SMELL 5: Primitive Obsession ────
# Using primitives instead of small objects
# BAD:
email = "alice@example.com"         # Just a string, no validation
phone = "+40722123456"              # No formatting rules
money = 99.99                       # No currency info

# GOOD: value objects
class Email:
    def __init__(self, value: str):
        if "@" not in value:
            raise ValueError(f"Invalid email: {value}")
        self.value = value

class Money:
    def __init__(self, amount: Decimal, currency: str):
        self.amount = amount
        self.currency = currency

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)


# ──── SMELL 6: Switch Statements (Repeated) ────
# Same switch/if-else chain in multiple places
# BAD:
def calculate_shipping(order):
    if order.type == "standard":
        return 5.99
    elif order.type == "express":
        return 15.99
    elif order.type == "overnight":
        return 29.99

def estimate_delivery(order):
    if order.type == "standard":
        return 5  # days
    elif order.type == "express":
        return 2
    elif order.type == "overnight":
        return 1

# GOOD: polymorphism
class ShippingMethod(ABC):
    @abstractmethod
    def cost(self) -> float: pass

    @abstractmethod
    def delivery_days(self) -> int: pass

class StandardShipping(ShippingMethod):
    def cost(self): return 5.99
    def delivery_days(self): return 5

class ExpressShipping(ShippingMethod):
    def cost(self): return 15.99
    def delivery_days(self): return 2


# ──── SMELL 7: Dead Code ────
# Unreachable code, unused variables, unused imports
# Delete it. Git remembers everything.


# ──── SMELL 8: Speculative Generality ────
# Building for "future needs" that never come
# BAD: AbstractFactoryProviderBuilderManager for a simple feature
# GOOD: build for today. Refactor when actually needed. (YAGNI)


# ──── SMELL 9: Message Chains ────
# BAD:
total = order.get_customer().get_address().get_city().get_tax_rate()

# GOOD: Law of Demeter (only talk to friends)
total = order.get_tax_rate()    # Order knows how to get it


# ──── SMELL 10: Shotgun Surgery ────
# One change requires editing 10 files
# Solution: consolidate related logic into one place
```


---

# CHAPTER 4: DESIGN PATTERNS


## Strategy Pattern

```python
# Encapsulate algorithms and make them interchangeable.

from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        return result + left[i:] + right[j:]

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        return self._strategy.sort(data)

# Usage: swap algorithm without changing client code
sorter = Sorter(QuickSort())
result = sorter.sort([3, 1, 4, 1, 5])

sorter = Sorter(MergeSort())
result = sorter.sort([3, 1, 4, 1, 5])
```


## Observer Pattern

```python
# When one object changes, notify all dependents.

class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list] = {}

    def on(self, event: str, callback):
        self._listeners.setdefault(event, []).append(callback)

    def off(self, event: str, callback):
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)


class OrderService(EventEmitter):
    def create_order(self, order_data):
        order = self._save(order_data)
        self.emit("order:created", order)
        return order


# Subscribers (decoupled!)
order_service = OrderService()

order_service.on("order:created", lambda order: send_email(order))
order_service.on("order:created", lambda order: update_inventory(order))
order_service.on("order:created", lambda order: log_analytics(order))

# Adding new side effect? Just add new listener.
# No modification to OrderService needed (Open/Closed Principle!)
```


## Repository Pattern

```python
# Abstraction over data access. Domain layer doesn't know about DB.

class UserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, id: str) -> User | None: pass

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: pass

    @abstractmethod
    async def save(self, user: User) -> User: pass

    @abstractmethod
    async def delete(self, id: str) -> bool: pass

    @abstractmethod
    async def find_all(self, limit: int = 20, offset: int = 0) -> list[User]: pass


class PostgresUserRepository(UserRepository):
    def __init__(self, pool):
        self.pool = pool

    async def find_by_id(self, id: str) -> User | None:
        row = await self.pool.fetchrow(
            "SELECT * FROM users WHERE id = $1", id
        )
        return User(**row) if row else None

    async def save(self, user: User) -> User:
        row = await self.pool.fetchrow(
            "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
            user.name, user.email,
        )
        return User(**row)


class InMemoryUserRepository(UserRepository):
    """For testing!"""
    def __init__(self):
        self.users: dict[str, User] = {}

    async def find_by_id(self, id: str) -> User | None:
        return self.users.get(id)

    async def save(self, user: User) -> User:
        self.users[user.id] = user
        return user


# Service uses abstraction — doesn't know or care about DB
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, id: str) -> User:
        user = await self.repo.find_by_id(id)
        if not user:
            raise NotFoundError("User", id)
        return user

# Production:
service = UserService(PostgresUserRepository(db_pool))

# Testing:
service = UserService(InMemoryUserRepository())
```


## Factory Pattern

```python
# Encapsulate object creation logic.

class NotificationFactory:
    @staticmethod
    def create(channel: str, config: dict) -> Notification:
        match channel:
            case "email":
                return EmailNotification(config["smtp_host"], config["from"])
            case "sms":
                return SMSNotification(config["twilio_sid"], config["from_number"])
            case "push":
                return PushNotification(config["fcm_key"])
            case "slack":
                return SlackNotification(config["webhook_url"])
            case _:
                raise ValueError(f"Unknown channel: {channel}")

# Usage
notifier = NotificationFactory.create("email", email_config)
notifier.send(user, "Hello!")

# Why factory?
# - Creation logic in one place
# - Client doesn't need to know concrete classes
# - Easy to add new notification types
# - Testable (mock the factory)
```


## Decorator Pattern

```python
# Add behavior to objects dynamically without modifying them.

# Python decorators (language feature aligned with pattern)
import functools
import time
import logging

logger = logging.getLogger(__name__)

# Timing decorator
def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

# Retry decorator
def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

# Cache decorator
def cached(ttl_seconds=300):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache:
                value, timestamp = cache[args]
                if now - timestamp < ttl_seconds:
                    return value
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

# Usage (composable!)
@timed
@retry(max_attempts=3)
@cached(ttl_seconds=60)
def fetch_user(user_id: str):
    return api.get(f"/users/{user_id}")
```


---

# CHAPTER 5: REFACTORING TECHNIQUES


## Extract Method

```python
# BEFORE: long method with mixed concerns
def print_invoice(invoice):
    # Print header
    print("=" * 40)
    print(f"Invoice #{invoice.number}")
    print(f"Date: {invoice.date}")
    print(f"Customer: {invoice.customer.name}")
    print("=" * 40)

    # Print line items
    total = 0
    for item in invoice.items:
        line_total = item.quantity * item.price
        total += line_total
        print(f"  {item.name}: {item.quantity} x ${item.price} = ${line_total}")

    # Print footer
    tax = total * 0.2
    grand_total = total + tax
    print("-" * 40)
    print(f"  Subtotal: ${total}")
    print(f"  Tax (20%): ${tax}")
    print(f"  TOTAL: ${grand_total}")

# AFTER: extracted methods
def print_invoice(invoice):
    print_header(invoice)
    subtotal = print_line_items(invoice.items)
    print_footer(subtotal)

def print_header(invoice):
    print("=" * 40)
    print(f"Invoice #{invoice.number}")
    print(f"Date: {invoice.date}")
    print(f"Customer: {invoice.customer.name}")
    print("=" * 40)

def print_line_items(items) -> float:
    total = 0
    for item in items:
        line_total = item.quantity * item.price
        total += line_total
        print(f"  {item.name}: {item.quantity} x ${item.price} = ${line_total}")
    return total

def print_footer(subtotal: float):
    tax = subtotal * 0.2
    print("-" * 40)
    print(f"  Subtotal: ${subtotal}")
    print(f"  Tax (20%): ${tax}")
    print(f"  TOTAL: ${subtotal + tax}")
```


## Replace Conditional with Polymorphism

```python
# BEFORE: switch on type
def calculate_pay(employee):
    if employee.type == "hourly":
        return employee.hours * employee.rate
    elif employee.type == "salaried":
        return employee.annual_salary / 12
    elif employee.type == "contractor":
        return employee.hours * employee.rate * 1.5

# AFTER: polymorphism
class Employee(ABC):
    @abstractmethod
    def calculate_pay(self) -> float:
        pass

class HourlyEmployee(Employee):
    def __init__(self, hours: float, rate: float):
        self.hours = hours
        self.rate = rate

    def calculate_pay(self) -> float:
        return self.hours * self.rate

class SalariedEmployee(Employee):
    def __init__(self, annual_salary: float):
        self.annual_salary = annual_salary

    def calculate_pay(self) -> float:
        return self.annual_salary / 12

class Contractor(Employee):
    def __init__(self, hours: float, rate: float):
        self.hours = hours
        self.rate = rate

    def calculate_pay(self) -> float:
        return self.hours * self.rate * 1.5
```


## Guard Clauses (Early Return)

```python
# BEFORE: deeply nested
def process_payment(order):
    if order is not None:
        if order.is_valid():
            if order.has_stock():
                if order.payment_method is not None:
                    if order.total > 0:
                        charge(order)
                        return "Success"
                    else:
                        return "Invalid total"
                else:
                    return "No payment method"
            else:
                return "Out of stock"
        else:
            return "Invalid order"
    else:
        return "No order"

# AFTER: guard clauses (flat, readable)
def process_payment(order):
    if order is None:
        return "No order"
    if not order.is_valid():
        return "Invalid order"
    if not order.has_stock():
        return "Out of stock"
    if order.payment_method is None:
        return "No payment method"
    if order.total <= 0:
        return "Invalid total"

    charge(order)
    return "Success"
```


---

# CHAPTER 6: PRINCIPLES AND RULES


## DRY, KISS, YAGNI

```
DRY (Don't Repeat Yourself):
  Every piece of knowledge should have a single, authoritative source.
  
  NOT just "don't copy-paste code" — also:
    - Don't repeat business rules in multiple places
    - Don't repeat validation logic (define once, use everywhere)
    - Don't repeat constants (define once)
  
  BUT: Some duplication is OK!
    - Shared code between unrelated features → coupling risk
    - "Wrong abstraction" is worse than duplication
    - Rule of Three: duplicate twice before abstracting

KISS (Keep It Simple, Stupid):
  The simplest solution that works is usually best.
  
  BAD: Using 5 design patterns for a 20-line script
  GOOD: Simple function until complexity requires patterns
  
  "Everyone knows that debugging is twice as hard as writing code.
   Therefore, if you write code as cleverly as possible, you are, by
   definition, not smart enough to debug it." — Kernighan

YAGNI (You Aren't Gonna Need It):
  Don't build for imaginary future requirements.
  
  BAD: "Let's add plugin support in case someone wants to extend it"
  GOOD: Build what's needed now. Refactor when requirements change.
  
  Exception: architecture decisions that are expensive to change later
  (database choice, auth model, API format) → think ahead.
```


## Law of Demeter (Principle of Least Knowledge)

```python
# Each unit should only talk to its direct friends.
# "Don't talk to strangers."

# BAD: long chains → coupling to internal structure
user.get_department().get_manager().get_email()
order.get_customer().get_address().get_zip_code()

# GOOD: ask, don't reach
user.get_manager_email()
order.get_shipping_zip()

# Implementation:
class User:
    def get_manager_email(self) -> str:
        return self.department.manager.email
    # Now if department structure changes, only User changes.
    # Callers are protected from internal structure.
```


## Composition Over Inheritance

```python
# Prefer composing objects over extending through inheritance.

# BAD: deep inheritance hierarchy
class Animal:
    def eat(self): pass

class Dog(Animal):
    def bark(self): pass

class SwimmingDog(Dog):
    def swim(self): pass

class FlyingSwimmingDog(SwimmingDog):    # Absurd!
    def fly(self): pass

# GOOD: compose behaviors
class Animal:
    def __init__(self, name: str, abilities: list["Ability"] = None):
        self.name = name
        self.abilities = abilities or []

    def perform(self, action: str):
        for ability in self.abilities:
            if ability.can_do(action):
                return ability.do(action)
        raise ValueError(f"{self.name} can't {action}")

class SwimAbility:
    def can_do(self, action): return action == "swim"
    def do(self, action): return "Swimming!"

class FlyAbility:
    def can_do(self, action): return action == "fly"
    def do(self, action): return "Flying!"

class BarkAbility:
    def can_do(self, action): return action == "bark"
    def do(self, action): return "Woof!"

# Mix and match without inheritance:
dog = Animal("Rex", [SwimAbility(), BarkAbility()])
duck = Animal("Donald", [SwimAbility(), FlyAbility()])
```


---

# CHAPTER 7: COMMON PITFALLS


## Anti-Patterns and Pitfalls

```
PITFALL 1: Premature abstraction
  Abstracting before you see the pattern.
  → Wait until you have 3 concrete cases, then abstract.

PITFALL 2: Over-engineering
  Factory of factory builders with abstract strategy providers.
  → KISS. Start simple. Refactor when needed.

PITFALL 3: Clever code
  One-liners that save lines but cost understanding.
  → Write code for humans, not for the compiler.

PITFALL 4: Inconsistency
  Different naming, formatting, patterns in same codebase.
  → Establish conventions (linter, formatter, style guide).

PITFALL 5: God objects
  One class/module does everything.
  → Split by Single Responsibility.

PITFALL 6: Tight coupling
  Changing one module breaks five others.
  → Depend on abstractions, use dependency injection.

PITFALL 7: Not refactoring
  "It works, don't touch it."
  → Technical debt compounds. Refactor regularly.

PITFALL 8: Cargo cult programming
  Using patterns/tools because "everyone does" without understanding why.
  → Understand the problem before applying the solution.

PITFALL 9: Ignoring error handling
  Happy path only. Production crashes.
  → Handle errors at every boundary.

PITFALL 10: Mutable shared state
  Multiple parts modify same global variable.
  → Immutable data, pure functions, explicit state management.

PITFALL 11: Comments instead of clear code
  // Calculate the total with tax and discount applied
  result = a * b - c + d * e / f
  → Rename variables, extract functions until code reads clearly.

PITFALL 12: Reinventing the wheel
  Writing your own JSON parser, HTTP client, crypto library.
  → Use battle-tested libraries. Focus on YOUR domain.

PITFALL 13: Mixing concerns in one function
  validate + compute + save + log + notify in one method.
  → Single Responsibility: each concern gets its own function.

PITFALL 14: Not using the type system
  Everything is `any`, `object`, `dict`.
  → Types prevent bugs. Use them fully.

PITFALL 15: Optimizing before profiling
  "This loop might be slow" → rewrites in assembly.
  → Profile first. Optimize the actual bottleneck.
  "Premature optimization is the root of all evil." — Knuth
```