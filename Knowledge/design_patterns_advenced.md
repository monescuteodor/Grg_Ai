# Design Patterns Reference


---

# CHAPTER 1: CREATIONAL PATTERNS


## Singleton

```python
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = "connected"
        return cls._instance

db1 = Database()
db2 = Database()
assert db1 is db2  # Same instance!
```

```javascript
class Database {
    constructor() {
        if (Database.instance) return Database.instance;
        this.connection = 'connected';
        Database.instance = this;
    }
}
const db1 = new Database();
const db2 = new Database();
console.log(db1 === db2);  // true
```


## Factory

```python
class Animal:
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Woof!"

class Cat(Animal):
    def speak(self): return "Meow!"

def create_animal(animal_type):
    animals = {"dog": Dog, "cat": Cat}
    return animals.get(animal_type, Animal)()

pet = create_animal("dog")
print(pet.speak())  # "Woof!"
```


## Builder

```python
class QueryBuilder:
    def __init__(self):
        self._parts = []
    def select(self, fields):
        self._parts.append(f"SELECT {fields}")
        return self
    def from_table(self, table):
        self._parts.append(f"FROM {table}")
        return self
    def where(self, cond):
        self._parts.append(f"WHERE {cond}")
        return self
    def build(self):
        return " ".join(self._parts)

query = QueryBuilder().select("*").from_table("users").where("age > 18").build()
# "SELECT * FROM users WHERE age > 18"
```


---

# CHAPTER 2: BEHAVIORAL PATTERNS


## Observer

```python
class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event, *args):
        for cb in self._listeners.get(event, []):
            cb(*args)

emitter = EventEmitter()
emitter.on("login", lambda user: print(f"{user} logged in"))
emitter.on("login", lambda user: log_to_db(user))
emitter.emit("login", "Alice")
```

```javascript
class EventEmitter {
    constructor() { this.events = {}; }
    on(event, fn) { (this.events[event] ??= []).push(fn); }
    emit(event, ...args) { (this.events[event] || []).forEach(fn => fn(...args)); }
    off(event, fn) { this.events[event] = (this.events[event] || []).filter(f => f !== fn); }
}

const bus = new EventEmitter();
bus.on('click', (x, y) => console.log(`Clicked ${x},${y}`));
bus.emit('click', 100, 200);
```


## Strategy

```python
def sort_by_name(users): return sorted(users, key=lambda u: u['name'])
def sort_by_age(users): return sorted(users, key=lambda u: u['age'])
def sort_by_score(users): return sorted(users, key=lambda u: u['score'], reverse=True)

def display_users(users, strategy=sort_by_name):
    for user in strategy(users):
        print(user['name'], user['age'])

users = [{'name': 'Bob', 'age': 30, 'score': 85}, {'name': 'Alice', 'age': 25, 'score': 92}]
display_users(users, sort_by_score)
```


---

# CHAPTER 3: STRUCTURAL PATTERNS


## Decorator (Wrapper)

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.time()-start:.3f}s")
        return result
    return wrapper

def retry(max_tries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_tries):
                try: return func(*args, **kwargs)
                except Exception as e:
                    if i == max_tries - 1: raise
        return wrapper
    return decorator

@timer
@retry(max_tries=3)
def fetch_data(url):
    pass
```


## Middleware (Chain)

```javascript
class Pipeline {
    constructor() { this.middlewares = []; }
    use(fn) { this.middlewares.push(fn); return this; }
    execute(context) {
        let index = 0;
        const next = () => {
            if (index < this.middlewares.length) {
                this.middlewares[index++](context, next);
            }
        };
        next();
    }
}

const pipeline = new Pipeline();
pipeline.use((ctx, next) => { ctx.startTime = Date.now(); next(); });
pipeline.use((ctx, next) => { console.log('Processing:', ctx.data); next(); });
pipeline.use((ctx, next) => { ctx.result = ctx.data.toUpperCase(); next(); });

const ctx = { data: 'hello' };
pipeline.execute(ctx);
console.log(ctx.result);  // "HELLO"
```