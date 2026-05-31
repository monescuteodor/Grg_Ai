# TypeScript Complete Reference


---

# CHAPTER 1: GETTING STARTED WITH TYPESCRIPT


## Remarks

TypeScript is a strongly typed superset of JavaScript developed by Microsoft. It compiles to plain JavaScript. TypeScript adds static types, interfaces, generics, decorators, and enums to JavaScript, enabling better tooling and large-scale application development.

Tools: `tsc` (TypeScript compiler), `ts-node`, `tsx`, `esbuild`, `vite`.


## Hello World

```typescript
// hello.ts
const greeting: string = "Hello, World!";
console.log(greeting);

function greet(name: string): string {
    return `Hello, ${name}!`;
}

console.log(greet("TypeScript"));
```

```bash
npm install -g typescript
tsc hello.ts
node hello.js

# Direct execution
npx ts-node hello.ts
npx tsx hello.ts
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "sourceMap": true
  }
}
```


---

# CHAPTER 2: TYPES


## Type System

```typescript
// Primitive types
let num: number = 42;
let str: string = "hello";
let bool: boolean = true;
let nothing: null = null;
let undef: undefined = undefined;
let big: bigint = 42n;
let sym: symbol = Symbol("id");

// any — opt out of type checking (avoid)
let anything: any = 42;

// unknown — type-safe any
let val: unknown = getInput();
if (typeof val === "string") {
    val.toUpperCase();   // OK after narrowing
}

// never — unreachable code
function throwError(msg: string): never {
    throw new Error(msg);
}

// void — function with no return
function log(msg: string): void {
    console.log(msg);
}

// Arrays
let nums: number[] = [1, 2, 3];
let strs: Array<string> = ["a", "b"];
let readonly_arr: readonly number[] = [1, 2, 3];

// Tuples
let pair: [string, number] = ["Alice", 30];
let [name, age] = pair;

// Named tuple
type Point3D = [x: number, y: number, z: number];

// Union types
let id: string | number = "abc";
id = 42;   // also valid

// Intersection types
type Admin = User & { admin: true };

// Literal types
type Direction = "north" | "south" | "east" | "west";
type StatusCode = 200 | 404 | 500;

// Type aliases
type UserID = string;
type Nullable<T> = T | null;
type Callback<T> = (data: T) => void;

// Utility types
Partial<User>       // all fields optional
Required<User>      // all fields required
Readonly<User>      // all fields readonly
Pick<User, "name" | "age">
Omit<User, "password">
Record<string, number>
Exclude<"a"|"b"|"c", "a">   // "b" | "c"
Extract<"a"|"b"|"c", "a"|"b">  // "a" | "b"
NonNullable<string | null>   // string
ReturnType<typeof fn>
Parameters<typeof fn>
InstanceType<typeof MyClass>
```


---

# CHAPTER 3: INTERFACES AND TYPE ALIASES


## Defining Shapes

```typescript
// Interface
interface User {
    id: number;
    name: string;
    email?: string;   // optional
    readonly createdAt: Date;  // read-only
    greet(): string;
    update(data: Partial<User>): void;
}

// Interface extension
interface Admin extends User {
    role: "admin" | "superadmin";
    permissions: string[];
}

// Interface merging (declaration merging)
interface Window {
    myCustomProp: string;
}

// Callable interface
interface Formatter {
    (value: number, precision: number): string;
    defaultPrecision: number;
}

// Index signature
interface StringMap {
    [key: string]: string;
    length: number;   // specific known key
}

// Type alias vs Interface
// Use interface for object shapes that may be extended
// Use type for unions, intersections, mapped types

// Mapped types
type Optional<T> = { [K in keyof T]?: T[K] };
type Mutable<T> = { -readonly [K in keyof T]: T[K] };
type Stringify<T> = { [K in keyof T]: string };

// Conditional types
type IsArray<T> = T extends any[] ? true : false;
type ElementType<T> = T extends (infer E)[] ? E : never;
type Flatten<T> = T extends Array<infer Item> ? Item : T;

// Template literal types
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;  // "onClick" | "onFocus" | "onBlur"
```


---

# CHAPTER 4: FUNCTIONS


## Typed Functions

```typescript
// Function types
function add(a: number, b: number): number { return a + b; }
const multiply = (a: number, b: number): number => a * b;

// Optional and default parameters
function greet(name: string, prefix: string = "Hello"): string {
    return `${prefix}, ${name}!`;
}

// Rest parameters
function sum(...nums: number[]): number {
    return nums.reduce((a, b) => a + b, 0);
}

// Function overloads
function format(value: number): string;
function format(value: string): string;
function format(value: number | string): string {
    return typeof value === "number" ? value.toFixed(2) : value.trim();
}

// Generic functions
function identity<T>(arg: T): T { return arg; }
function first<T>(arr: T[]): T | undefined { return arr[0]; }
function zip<A, B>(a: A[], b: B[]): [A, B][] {
    return a.map((x, i) => [x, b[i]]);
}

// Constrained generics
function maxVal<T extends { valueOf(): number }>(a: T, b: T): T {
    return a.valueOf() >= b.valueOf() ? a : b;
}

// Higher-order functions
function compose<T>(...fns: Array<(x: T) => T>): (x: T) => T {
    return (x) => fns.reduceRight((acc, fn) => fn(acc), x);
}

// Predicate functions (type guards)
function isString(val: unknown): val is string {
    return typeof val === "string";
}

// Assertion functions
function assertDefined<T>(val: T): asserts val is NonNullable<T> {
    if (val == null) throw new Error("Expected defined value");
}
```


---

# CHAPTER 5: CLASSES


## TypeScript Classes

```typescript
class Animal {
    // Field declarations
    private name: string;
    protected sound: string;
    public readonly id: number;
    #privateField = 42;   // ECMAScript private

    constructor(name: string, sound: string) {
        this.name = name;
        this.sound = sound;
        this.id = Math.random();
    }

    // Parameter property shorthand
    // constructor(private name: string, public age: number) {}

    get displayName(): string { return this.name; }
    set displayName(val: string) { this.name = val; }

    speak(): string { return `${this.name} says ${this.sound}`; }

    static create(name: string): Animal {
        return new Animal(name, "...");
    }
}

class Dog extends Animal {
    constructor(name: string, public breed: string) {
        super(name, "Woof");
    }

    override speak(): string { return super.speak() + "!"; }
}

// Implementing interfaces
interface Serializable {
    serialize(): string;
    deserialize(data: string): void;
}

class Config implements Serializable {
    constructor(private data: Record<string, unknown> = {}) {}
    serialize() { return JSON.stringify(this.data); }
    deserialize(s: string) { this.data = JSON.parse(s); }
}

// Abstract class
abstract class Shape {
    abstract get area(): number;
    abstract get perimeter(): number;
    describe(): void { console.log(`Area=${this.area.toFixed(2)}`); }
}

// Generic class
class Pair<A, B> {
    constructor(public first: A, public second: B) {}
    swap(): Pair<B, A> { return new Pair(this.second, this.first); }
}
```


---

# CHAPTER 6: GENERICS AND ADVANCED TYPES


## Advanced Generics

```typescript
// Generic constraints
interface HasLength { length: number; }
function logLength<T extends HasLength>(val: T): T {
    console.log(val.length);
    return val;
}

// keyof and typeof
type Keys = keyof User;   // "id" | "name" | "email" | ...

function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const name = getProperty(user, "name");  // typed as string

// Discriminated unions
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number }
    | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":   return Math.PI * shape.radius ** 2;
        case "rect":     return shape.width * shape.height;
        case "triangle": return 0.5 * shape.base * shape.height;
    }
}

// infer in conditional types
type Unpromise<T> = T extends Promise<infer R> ? R : T;
type RetType<T> = T extends (...args: any[]) => infer R ? R : never;

// Template literal types
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```


---

# CHAPTER 7: DECORATORS AND MODULES


## Decorators and Modules

```typescript
// Decorators (experimental, enable in tsconfig)
function log(target: any, key: string, descriptor: PropertyDescriptor) {
    const original = descriptor.value;
    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${key} with`, args);
        return original.apply(this, args);
    };
    return descriptor;
}

class Service {
    @log
    process(data: string): string {
        return data.toUpperCase();
    }
}

// Class decorator
function singleton<T extends { new(...args: any[]): {} }>(ctor: T) {
    let instance: InstanceType<T>;
    return class extends ctor {
        constructor(...args: any[]) {
            if (instance) return instance;
            super(...args);
            instance = this as any;
        }
    };
}

// ES Modules
// math.ts
export const PI = 3.14159;
export function add(a: number, b: number) { return a + b; }
export default class MathHelper { /* ... */ }

// main.ts
import MathHelper, { PI, add } from "./math.js";
import type { User } from "./types.js";   // type-only import

// Re-export
export { add as default } from "./math.js";
export * from "./utils.js";
```


---

# CHAPTER 8: TYPE NARROWING AND GUARDS


## Type Safety Patterns

```typescript
// typeof narrowing
function process(val: string | number) {
    if (typeof val === "string") {
        return val.toUpperCase();
    }
    return val.toFixed(2);
}

// instanceof narrowing
function handleError(err: unknown) {
    if (err instanceof TypeError) {
        console.log("Type error:", err.message);
    } else if (err instanceof Error) {
        console.log("Error:", err.message);
    } else {
        console.log("Unknown error:", err);
    }
}

// in narrowing
interface Cat { meow(): void; }
interface Dog { bark(): void; }
function makeNoise(animal: Cat | Dog) {
    if ("meow" in animal) animal.meow();
    else animal.bark();
}

// Discriminated union exhaustiveness
function assertNever(x: never): never {
    throw new Error("Unexpected: " + x);
}

function handleShape(s: Shape) {
    switch (s.kind) {
        case "circle": return Math.PI * s.radius**2;
        case "rect":   return s.width * s.height;
        default:       return assertNever(s);  // compile error if not exhaustive
    }
}

// Nullish patterns
const x = value ?? defaultValue;
const len = str?.length ?? 0;
obj?.method?.();

// as const
const config = { host: "localhost", port: 8080 } as const;
// config.port is 8080 (literal), not number
```
