# JavaScript Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH JAVASCRIPT


## Remarks

JavaScript is a lightweight, interpreted, multi-paradigm language. It runs in browsers (DOM manipulation) and server-side via Node.js. ES6+ (ES2015+) introduced classes, modules, arrow functions, destructuring, promises, and async/await.

Engines: V8 (Chrome/Node), SpiderMonkey (Firefox), JavaScriptCore (Safari).


## Hello World

```javascript
// Browser
console.log("Hello, World!");
alert("Hello!");

// Node.js
console.log("Hello from Node!");
process.stdout.write("No newline");
```

```bash
node hello.js
node -e "console.log('Hello')"
```


---

# CHAPTER 2: VARIABLES AND TYPES


## Variables

```javascript
// let — block-scoped, reassignable
let x = 10;
x = 20;

// const — block-scoped, not reassignable
const PI = 3.14159;
const obj = { a: 1 };
obj.a = 2;   // OK — object itself is mutable

// var — function-scoped, hoisted (avoid)
var old = "legacy";

// Primitive types
let num    = 42;           // number
let float  = 3.14;         // number
let big    = 42n;          // bigint
let str    = "hello";      // string
let bool   = true;         // boolean
let undef;                 // undefined
let nul    = null;         // null
let sym    = Symbol("id"); // symbol

// Type coercion
typeof 42        // "number"
typeof "hello"   // "string"
typeof null      // "object" (quirk!)
typeof undefined // "undefined"

// Equality
1 == "1"    // true  (loose, coerces)
1 === "1"   // false (strict, no coercion) — prefer ===
null == undefined   // true
null === undefined  // false
```

## Strings

```javascript
const s = "Hello, World!";
s.length           // 13
s.toUpperCase()    // "HELLO, WORLD!"
s.toLowerCase()
s.includes("World")   // true
s.startsWith("Hello") // true
s.indexOf("World")    // 7
s.slice(0, 5)         // "Hello"
s.split(", ")         // ["Hello", "World!"]
s.trim()
s.replace("World", "JS")
s.padStart(20, "*")

// Template literals
const name = "Alice";
const age = 30;
console.log(`Name: ${name}, Age: ${age}`);
console.log(`${2 + 2}`);   // "4"

// Multi-line
const multi = `
  Line 1
  Line 2
`;
```


---

# CHAPTER 3: CONTROL FLOW


## Conditionals and Loops

```javascript
// if/else
if (x > 0) {
    console.log("positive");
} else if (x === 0) {
    console.log("zero");
} else {
    console.log("negative");
}

// Ternary
const label = x > 0 ? "positive" : "non-positive";

// switch
switch (day) {
    case "Mon":
    case "Tue":
        console.log("Weekday"); break;
    case "Sat":
    case "Sun":
        console.log("Weekend"); break;
    default:
        console.log("Other");
}

// for
for (let i = 0; i < 5; i++) {
    console.log(i);
}

// for...of (iterate values)
for (const item of [1, 2, 3]) {
    console.log(item);
}

// for...in (iterate keys)
for (const key in { a: 1, b: 2 }) {
    console.log(key);
}

// while / do-while
let n = 0;
while (n < 5) n++;

do {
    console.log(n);
    n--;
} while (n > 0);

// Nullish coalescing
const val = null ?? "default";   // "default"
const val2 = 0 ?? "default";    // 0 (not null/undefined)

// Optional chaining
const city = user?.address?.city;
const len  = arr?.length;
```


---

# CHAPTER 4: FUNCTIONS


## Functions

```javascript
// Function declaration (hoisted)
function add(a, b) { return a + b; }

// Function expression
const multiply = function(a, b) { return a * b; };

// Arrow function
const square = x => x * x;
const sum = (a, b) => a + b;
const doSomething = () => { console.log("done"); };

// Default parameters
function greet(name = "World") {
    return `Hello, ${name}!`;
}

// Rest parameters
function total(...nums) {
    return nums.reduce((a, b) => a + b, 0);
}

// Spread
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5];
Math.max(...arr1);

// Destructuring parameters
function display({ name, age = 0 } = {}) {
    console.log(name, age);
}

// Higher-order functions
const nums = [1, 2, 3, 4, 5];
nums.map(x => x * 2)             // [2,4,6,8,10]
nums.filter(x => x % 2 === 0)   // [2,4]
nums.reduce((acc, x) => acc + x, 0)  // 15
nums.find(x => x > 3)            // 4
nums.every(x => x > 0)           // true
nums.some(x => x > 4)            // true

// Closures
function makeCounter(start = 0) {
    let count = start;
    return {
        increment: () => ++count,
        decrement: () => --count,
        value: () => count,
    };
}

// IIFE
(function() { console.log("runs immediately"); })();
(() => { console.log("arrow IIFE"); })();
```


---

# CHAPTER 5: OBJECTS AND ARRAYS


## Objects

```javascript
// Object literal
const person = {
    name: "Alice",
    age: 30,
    greet() { return `Hi, I'm ${this.name}`; },
    get fullName() { return `${this.name} Smith`; },
    set fullName(v) { this.name = v.split(" ")[0]; },
};

// Computed property names
const key = "score";
const obj = { [key]: 100, [`${key}Bonus`]: 10 };

// Destructuring
const { name, age, city = "NYC" } = person;
const { name: firstName } = person;   // rename

// Spread / Object.assign
const extended = { ...person, email: "alice@example.com" };
const copy = Object.assign({}, person);

// Object methods
Object.keys(person)
Object.values(person)
Object.entries(person)
Object.freeze(person)    // make immutable
Object.fromEntries([["a",1],["b",2]])

// Arrays
const arr = [1, 2, 3, 4, 5];
arr.push(6)          // add to end
arr.pop()            // remove from end
arr.unshift(0)       // add to start
arr.shift()          // remove from start
arr.splice(2, 1)     // remove at index
arr.slice(1, 3)      // [2,3] (non-mutating)
arr.indexOf(3)
arr.includes(3)
arr.flat()           // flatten nested
arr.flatMap(x => [x, x*2])
arr.sort((a,b) => a-b)   // numeric sort
arr.reverse()

// Array destructuring
const [first, second, ...rest] = arr;
const [,, third] = arr;
```


---

# CHAPTER 6: CLASSES AND PROTOTYPES


## OOP in JavaScript

```javascript
class Animal {
    #name;    // private field

    constructor(name, sound) {
        this.#name = name;
        this.sound = sound;
    }

    get name() { return this.#name; }

    speak() {
        return `${this.#name} says ${this.sound}`;
    }

    static create(name, sound) {
        return new Animal(name, sound);
    }

    toString() { return `Animal(${this.#name})`; }
}

class Dog extends Animal {
    constructor(name, breed) {
        super(name, "Woof");
        this.breed = breed;
    }

    speak() {
        return super.speak() + "!";
    }

    fetch() { return `${this.name} fetches!`; }
}

// Mixins
const Serializable = (Base) => class extends Base {
    serialize() { return JSON.stringify(this); }
};

class SerializableDog extends Serializable(Dog) {}

// Symbol.iterator — make custom iterable
class Range {
    constructor(start, end) {
        this.start = start; this.end = end;
    }
    [Symbol.iterator]() {
        let current = this.start;
        const end = this.end;
        return {
            next() {
                return current <= end
                    ? { value: current++, done: false }
                    : { done: true };
            }
        };
    }
}

for (const n of new Range(1, 5)) console.log(n);
```


---

# CHAPTER 7: ASYNC PROGRAMMING


## Promises and Async/Await

```javascript
// Callbacks (old style)
setTimeout(() => console.log("after 1s"), 1000);

// Promise
const promise = new Promise((resolve, reject) => {
    setTimeout(() => resolve("success"), 1000);
});

promise
    .then(val => console.log(val))
    .catch(err => console.error(err))
    .finally(() => console.log("done"));

// Promise combinators
Promise.all([fetch("/a"), fetch("/b")])        // all must succeed
    .then(([a, b]) => console.log(a, b));

Promise.allSettled([p1, p2])                   // all results
    .then(results => results.forEach(r => console.log(r)));

Promise.race([p1, p2])                         // first to settle
    .then(v => console.log(v));

Promise.any([p1, p2])                          // first to succeed
    .then(v => console.log(v));

// async/await
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        return data;
    } catch (err) {
        console.error("Fetch failed:", err);
        throw err;
    }
}

// Parallel async
async function fetchAll(urls) {
    const results = await Promise.all(urls.map(fetchData));
    return results;
}

// Async generators
async function* paginate(url) {
    let page = 1;
    while (true) {
        const data = await fetchData(`${url}?page=${page}`);
        if (!data.length) return;
        yield data;
        page++;
    }
}
```


---

# CHAPTER 8: MODULES


## ES Modules and CommonJS

```javascript
// ES Modules (import/export)

// math.js
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export default class Calculator { /* ... */ }

// main.js
import Calculator, { PI, add } from "./math.js";
import * as math from "./math.js";

// Dynamic import
const module = await import("./math.js");

// CommonJS (Node.js)
// utils.js
module.exports = { add: (a,b) => a+b };
// or
exports.PI = 3.14159;

// main.js
const { add } = require("./utils");
const fs = require("fs");
const path = require("path");
```


---

# CHAPTER 9: ADVANCED JAVASCRIPT


## Generators, Proxy, WeakMap

```javascript
// Generator
function* range(start, end, step = 1) {
    for (let i = start; i < end; i += step) yield i;
}

for (const n of range(0, 10, 2)) console.log(n);

// Proxy
const handler = {
    get(target, key) {
        return key in target ? target[key] : `No property: ${key}`;
    },
    set(target, key, value) {
        if (typeof value !== "number") throw new TypeError("Must be number");
        target[key] = value;
        return true;
    }
};
const proxy = new Proxy({}, handler);

// Reflect
Reflect.has(obj, "key")
Reflect.ownKeys(obj)

// WeakMap / WeakSet (no memory leaks for DOM nodes)
const wm = new WeakMap();
wm.set(element, { data: "private" });

// Symbol
const id = Symbol("id");
const obj = { [id]: 123, name: "Alice" };
obj[id]   // 123

// Prototype chain
Object.getPrototypeOf(dog) === Dog.prototype  // true
dog instanceof Dog   // true
dog instanceof Animal  // true

// Error types
new Error("generic")
new TypeError("wrong type")
new RangeError("out of range")
new ReferenceError("not defined")
new SyntaxError("bad syntax")
```
