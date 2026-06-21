# TypeScript Advanced Complete Reference


---

# CHAPTER 1: TYPE SYSTEM FUNDAMENTALS


## Remarks

TypeScript is JavaScript with a static type system, developed by Microsoft. It compiles to plain JavaScript and adds zero runtime overhead — types are erased at compile time. TypeScript is now the industry standard for any JavaScript project at scale (React, Node, Angular, Vue, Deno, Bun all use it).

Key concepts: **Structural typing** (shape matters, not name), **Type inference** (compiler deduces types), **Union and Intersection types** (combine types), **Generics** (reusable typed abstractions), **Utility types** (built-in type transformers), **Conditional types** (type-level if/else), **Template literal types** (string manipulation at type level), **Type narrowing** (compiler tracks types through control flow).

Used by: every modern web/Node project. Google, Microsoft, Airbnb, Stripe, Vercel all mandate TypeScript.

Tools: **tsc** (compiler), **tsconfig.json** (config), **ts-node** (run TS directly), **tsx** (faster ts-node), **@types/** (DefinitelyTyped packages), **ESLint** with @typescript-eslint, **Zod** (runtime validation + type inference).


## Primitive and Literal Types

```typescript
// Primitives
let name: string = "Alice";
let age: number = 30;
let active: boolean = true;
let nothing: null = null;
let undef: undefined = undefined;
let big: bigint = 100n;
let sym: symbol = Symbol("id");

// Literal types (EXACT values)
let direction: "north" | "south" | "east" | "west";
direction = "north";    // OK
direction = "up";       // Error!

let httpStatus: 200 | 201 | 400 | 404 | 500;
httpStatus = 200;       // OK
httpStatus = 302;       // Error!

// const assertions (infer narrowest type)
const config = {
    port: 3000,
    host: "localhost",
} as const;
// Type: { readonly port: 3000; readonly host: "localhost"; }
// Without 'as const': { port: number; host: string; }

// Template literal types
type EventName = `on${string}`;
let handler: EventName = "onClick";   // OK
let bad: EventName = "click";         // Error! Must start with "on"

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type ApiRoute = `/${string}`;
type Endpoint = `${HttpMethod} ${ApiRoute}`;
let ep: Endpoint = "GET /users";      // OK
let bad2: Endpoint = "PATCH /users";  // Error!
```


## Object Types and Interfaces

```typescript
// Interface (preferred for objects)
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;                      // Optional
    readonly createdAt: Date;          // Cannot be reassigned
}

// Type alias (preferred for unions, tuples, complex types)
type Status = "active" | "inactive" | "banned";
type Point = { x: number; y: number };
type Callback = (data: string) => void;

// Extend interface
interface Admin extends User {
    permissions: string[];
    level: number;
}

// Intersection (&) — combine types
type AdminUser = User & {
    permissions: string[];
    level: number;
};

// Index signatures (dynamic keys)
interface Dictionary {
    [key: string]: string;
}

interface NumberMap {
    [key: string]: number;
    length: number;    // OK: number is compatible
}

// Record type (cleaner than index signature)
type Scores = Record<string, number>;
const scores: Scores = { math: 95, english: 87 };

// Nested
interface Company {
    name: string;
    address: {
        street: string;
        city: string;
        country: string;
    };
    employees: User[];
}

// Interface vs Type — when to use which?
// Interface: objects, classes, extending, declaration merging
// Type: unions, tuples, mapped types, complex type operations
```


## Arrays, Tuples, and Enums

```typescript
// Arrays
const numbers: number[] = [1, 2, 3];
const names: Array<string> = ["Alice", "Bob"];
const mixed: (string | number)[] = [1, "two", 3];

// Readonly arrays
const frozen: readonly number[] = [1, 2, 3];
const frozen2: ReadonlyArray<string> = ["a", "b"];
// frozen.push(4);   // Error!

// Tuples (fixed-length, typed positions)
type Point3D = [number, number, number];
const origin: Point3D = [0, 0, 0];

// Named tuples (documentation)
type UserTuple = [id: number, name: string, active: boolean];
const user: UserTuple = [1, "Alice", true];

// Variadic tuples
type Head<T extends any[]> = T extends [infer H, ...any[]] ? H : never;
type First = Head<[string, number, boolean]>;   // string

// Rest in tuples
type StringThenNumbers = [string, ...number[]];
const data: StringThenNumbers = ["label", 1, 2, 3, 4];

// Enums
enum Direction {
    Up = "UP",
    Down = "DOWN",
    Left = "LEFT",
    Right = "RIGHT",
}

// const enum (inlined at compile time, no runtime object)
const enum Color {
    Red = 0,
    Green = 1,
    Blue = 2,
}
const c = Color.Red;   // Compiles to: const c = 0;

// PREFER union types over enums in most cases:
type Direction2 = "UP" | "DOWN" | "LEFT" | "RIGHT";
// Simpler, no runtime code, works with JSON naturally
```


---

# CHAPTER 2: FUNCTIONS


## Function Types

```typescript
// Function declaration
function add(a: number, b: number): number {
    return a + b;
}

// Arrow function
const multiply = (a: number, b: number): number => a * b;

// Function type alias
type MathOp = (a: number, b: number) => number;
const divide: MathOp = (a, b) => a / b;

// Optional and default parameters
function greet(name: string, greeting: string = "Hello"): string {
    return `${greeting}, ${name}!`;
}

function createUser(name: string, age?: number): User {
    return { name, age: age ?? 0 };
}

// Rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((a, b) => a + b, 0);
}

// Overloads (multiple signatures)
function parse(input: string): number;
function parse(input: number): string;
function parse(input: string | number): string | number {
    if (typeof input === "string") return parseInt(input);
    return input.toString();
}

const a = parse("42");      // Type: number
const b = parse(42);        // Type: string

// void vs undefined
function logMessage(msg: string): void {
    console.log(msg);
    // return undefined; is fine too
}

// never (function never returns)
function throwError(msg: string): never {
    throw new Error(msg);
}

function infiniteLoop(): never {
    while (true) { /* ... */ }
}

// this parameter (explicit typing)
interface Button {
    label: string;
    onClick(this: Button): void;
}
```


## Generics

```typescript
// Generic function — works with ANY type, preserving type info
function identity<T>(value: T): T {
    return value;
}
const str = identity("hello");    // Type: string (inferred)
const num = identity(42);         // Type: number

// Generic with constraint
function getLength<T extends { length: number }>(item: T): number {
    return item.length;
}
getLength("hello");               // OK: string has .length
getLength([1, 2, 3]);             // OK: array has .length
getLength(42);                    // Error: number has no .length

// Multiple type parameters
function map<T, U>(arr: T[], fn: (item: T) => U): U[] {
    return arr.map(fn);
}
const lengths = map(["hi", "hello"], s => s.length);   // number[]

// Generic interfaces
interface Repository<T> {
    findById(id: string): Promise<T | null>;
    findAll(): Promise<T[]>;
    create(item: Omit<T, "id">): Promise<T>;
    update(id: string, item: Partial<T>): Promise<T>;
    delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
    async findById(id: string): Promise<User | null> {
        return db.users.findFirst({ where: { id } });
    }
    // ... implement all methods
}

// Generic classes
class Stack<T> {
    private items: T[] = [];

    push(item: T): void {
        this.items.push(item);
    }

    pop(): T | undefined {
        return this.items.pop();
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    get size(): number {
        return this.items.length;
    }
}

const numStack = new Stack<number>();
numStack.push(42);
numStack.push("hello");    // Error: string is not number

// Default type parameter
interface ApiResponse<T = unknown> {
    data: T;
    status: number;
    message: string;
}

const res: ApiResponse = { data: "anything", status: 200, message: "ok" };
const userRes: ApiResponse<User> = { data: user, status: 200, message: "ok" };

// Constraining to keys of another type
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user = { name: "Alice", age: 30 };
getProperty(user, "name");     // Type: string
getProperty(user, "age");      // Type: number
getProperty(user, "email");    // Error: "email" is not keyof User
```


---

# CHAPTER 3: ADVANCED TYPE SYSTEM


## Union and Intersection Types

```typescript
// Union: A OR B
type StringOrNumber = string | number;

function printId(id: string | number): void {
    // Must narrow before using type-specific methods
    if (typeof id === "string") {
        console.log(id.toUpperCase());     // OK: narrowed to string
    } else {
        console.log(id.toFixed(2));        // OK: narrowed to number
    }
}

// Discriminated unions (THE most powerful TS pattern)
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rectangle"; width: number; height: number }
    | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rectangle":
            return shape.width * shape.height;
        case "triangle":
            return (shape.base * shape.height) / 2;
    }
    // Exhaustiveness check: if you add new shape, TS warns
}

// Result type pattern (instead of try-catch)
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

function divide(a: number, b: number): Result<number, string> {
    if (b === 0) return { ok: false, error: "Division by zero" };
    return { ok: true, value: a / b };
}

const result = divide(10, 3);
if (result.ok) {
    console.log(result.value);     // Type: number
} else {
    console.log(result.error);     // Type: string
}

// Intersection: A AND B
type WithTimestamps = {
    createdAt: Date;
    updatedAt: Date;
};

type UserWithTimestamps = User & WithTimestamps;
// Has all User fields AND createdAt + updatedAt
```


## Type Narrowing

```typescript
// typeof guard
function process(value: string | number | boolean): string {
    if (typeof value === "string") return value.toUpperCase();
    if (typeof value === "number") return value.toFixed(2);
    return value ? "yes" : "no";   // Narrowed to boolean
}

// instanceof guard
function formatDate(date: string | Date): string {
    if (date instanceof Date) return date.toISOString();
    return new Date(date).toISOString();
}

// 'in' operator guard
interface Cat { meow(): void; whiskers: number; }
interface Dog { bark(): void; breed: string; }

function pet(animal: Cat | Dog): void {
    if ("meow" in animal) {
        animal.meow();           // Cat
    } else {
        animal.bark();           // Dog
    }
}

// Custom type guard (type predicate)
function isString(value: unknown): value is string {
    return typeof value === "string";
}

function processValue(value: unknown): void {
    if (isString(value)) {
        console.log(value.toUpperCase());   // Narrowed to string!
    }
}

// Assertion function (throws if not valid)
function assertNonNull<T>(value: T | null | undefined, msg?: string): asserts value is T {
    if (value === null || value === undefined) {
        throw new Error(msg ?? "Value is null");
    }
}

const user = getUser(id);          // User | null
assertNonNull(user, "User not found");
console.log(user.name);            // Now guaranteed non-null

// Discriminated union narrowing
type ApiResult =
    | { status: "loading" }
    | { status: "success"; data: User[] }
    | { status: "error"; message: string };

function render(result: ApiResult): string {
    switch (result.status) {
        case "loading": return "Loading...";
        case "success": return result.data.map(u => u.name).join(", ");
        case "error": return `Error: ${result.message}`;
    }
}

// Exhaustiveness with never
function exhaustive(result: ApiResult): string {
    switch (result.status) {
        case "loading": return "Loading...";
        case "success": return "Done";
        case "error": return "Failed";
        default:
            const _exhaustive: never = result;
            return _exhaustive;   // Error if new status added but not handled
    }
}
```


## Utility Types (Built-in)

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    age: number;
    role: "admin" | "user";
}

// Partial<T> — all properties optional
type UpdateUser = Partial<User>;
// { id?: number; name?: string; email?: string; ... }

// Required<T> — all properties required
type StrictUser = Required<User>;

// Readonly<T> — all properties readonly
type FrozenUser = Readonly<User>;
const frozen: FrozenUser = { id: 1, name: "Alice", ... };
// frozen.name = "Bob";   // Error!

// Pick<T, K> — select specific properties
type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string; }

// Omit<T, K> — remove specific properties
type CreateUser = Omit<User, "id">;
// { name: string; email: string; age: number; role: ... }

// Record<K, V> — object with keys K and values V
type Roles = Record<string, string[]>;
const permissions: Roles = {
    admin: ["read", "write", "delete"],
    user: ["read"],
};

type StatusCodes = Record<number, string>;
const codes: StatusCodes = { 200: "OK", 404: "Not Found" };

// Exclude<T, U> — remove types from union
type NonString = Exclude<string | number | boolean, string>;
// number | boolean

// Extract<T, U> — keep only types matching U
type OnlyString = Extract<string | number | boolean, string>;
// string

// NonNullable<T> — remove null and undefined
type SafeString = NonNullable<string | null | undefined>;
// string

// ReturnType<T> — extract return type of function
function getUser() { return { id: 1, name: "Alice" }; }
type UserReturn = ReturnType<typeof getUser>;
// { id: number; name: string; }

// Parameters<T> — extract parameter types as tuple
type GetUserParams = Parameters<typeof getUser>;
// []

function createUser(name: string, age: number): User { /* ... */ }
type CreateParams = Parameters<typeof createUser>;
// [string, number]

// Awaited<T> — unwrap Promise
type ResolvedUser = Awaited<Promise<User>>;
// User

type DeepResolved = Awaited<Promise<Promise<string>>>;
// string

// ConstructorParameters<T>
class HttpClient {
    constructor(baseUrl: string, timeout: number) {}
}
type HttpParams = ConstructorParameters<typeof HttpClient>;
// [string, number]

// InstanceType<T>
type HttpInstance = InstanceType<typeof HttpClient>;
// HttpClient
```


## Mapped Types

```typescript
// Create new types by transforming properties of existing ones

// Make all properties optional (this is how Partial<T> works)
type MyPartial<T> = {
    [K in keyof T]?: T[K];
};

// Make all properties readonly
type MyReadonly<T> = {
    readonly [K in keyof T]: T[K];
};

// Make all properties nullable
type Nullable<T> = {
    [K in keyof T]: T[K] | null;
};

// Remove readonly
type Mutable<T> = {
    -readonly [K in keyof T]: T[K];
};

// Remove optional
type Concrete<T> = {
    [K in keyof T]-?: T[K];
};

// Transform values
type Getters<T> = {
    [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;
// { getId: () => number; getName: () => string; getEmail: () => string; ... }

// Filter keys by value type
type StringKeys<T> = {
    [K in keyof T as T[K] extends string ? K : never]: T[K];
};

type UserStrings = StringKeys<User>;
// { name: string; email: string; role: "admin" | "user"; }

// Practical: Form errors (each field → string | undefined)
type FormErrors<T> = {
    [K in keyof T]?: string;
};

type UserFormErrors = FormErrors<User>;
// { id?: string; name?: string; email?: string; ... }
```


## Conditional Types

```typescript
// Type-level if/else
type IsString<T> = T extends string ? true : false;
type A = IsString<string>;        // true
type B = IsString<number>;        // false

// Extract return type (simplified ReturnType)
type GetReturn<T> = T extends (...args: any[]) => infer R ? R : never;
type R1 = GetReturn<() => string>;           // string
type R2 = GetReturn<(x: number) => boolean>; // boolean

// Extract array element type
type ElementOf<T> = T extends (infer E)[] ? E : never;
type E1 = ElementOf<string[]>;               // string
type E2 = ElementOf<(number | boolean)[]>;   // number | boolean

// Extract Promise value
type UnwrapPromise<T> = T extends Promise<infer V> ? V : T;
type P1 = UnwrapPromise<Promise<string>>;    // string
type P2 = UnwrapPromise<number>;             // number (not a Promise, unchanged)

// Distributive conditional types (over unions)
type ToArray<T> = T extends any ? T[] : never;
type Arr = ToArray<string | number>;
// string[] | number[] (distributed!)

// Non-distributive
type ToArrayND<T> = [T] extends [any] ? T[] : never;
type ArrND = ToArrayND<string | number>;
// (string | number)[] (NOT distributed)

// Recursive conditional types
type DeepReadonly<T> = {
    readonly [K in keyof T]: T[K] extends object
        ? DeepReadonly<T[K]>
        : T[K];
};

interface Config {
    server: {
        port: number;
        host: string;
        ssl: {
            enabled: boolean;
            cert: string;
        };
    };
}

type FrozenConfig = DeepReadonly<Config>;
// All nested properties are readonly
```


---

# CHAPTER 4: PATTERNS AND BEST PRACTICES


## Branded Types (Nominal Typing)

```typescript
// TypeScript is structural — same shape = same type
// Problem: UserId and PostId are both numbers, but shouldn't be interchangeable

type UserId = number & { readonly __brand: "UserId" };
type PostId = number & { readonly __brand: "PostId" };

function createUserId(id: number): UserId {
    return id as UserId;
}

function createPostId(id: number): PostId {
    return id as PostId;
}

function getUser(id: UserId): User { /* ... */ }
function getPost(id: PostId): Post { /* ... */ }

const userId = createUserId(1);
const postId = createPostId(1);

getUser(userId);    // OK
getUser(postId);    // Error! PostId is not UserId
getUser(1);         // Error! number is not UserId

// Same for strings
type Email = string & { readonly __brand: "Email" };
type Url = string & { readonly __brand: "Url" };

function validateEmail(input: string): Email {
    if (!input.includes("@")) throw new Error("Invalid email");
    return input as Email;
}
```


## Builder Pattern with Types

```typescript
// Type-safe builder that tracks which fields are set
interface QueryConfig {
    table: string;
    where?: string;
    orderBy?: string;
    limit?: number;
}

class QueryBuilder<T extends Partial<QueryConfig> = {}> {
    private config: Partial<QueryConfig> = {};

    from<Table extends string>(table: Table): QueryBuilder<T & { table: Table }> {
        this.config.table = table;
        return this as any;
    }

    where(condition: string): QueryBuilder<T & { where: string }> {
        this.config.where = condition;
        return this as any;
    }

    orderBy(field: string): QueryBuilder<T & { orderBy: string }> {
        this.config.orderBy = field;
        return this as any;
    }

    limit(n: number): QueryBuilder<T & { limit: number }> {
        this.config.limit = n;
        return this as any;
    }

    // Can only build if table is set
    build(this: QueryBuilder<{ table: string }>): string {
        let sql = `SELECT * FROM ${this.config.table}`;
        if (this.config.where) sql += ` WHERE ${this.config.where}`;
        if (this.config.orderBy) sql += ` ORDER BY ${this.config.orderBy}`;
        if (this.config.limit) sql += ` LIMIT ${this.config.limit}`;
        return sql;
    }
}

new QueryBuilder()
    .from("users")
    .where("active = true")
    .orderBy("name")
    .limit(10)
    .build();   // OK

new QueryBuilder()
    .where("active = true")
    .build();   // Error! 'table' is missing
```


## Zod — Runtime Validation + Type Inference

```typescript
import { z } from "zod";

// Define schema (runtime validation + TypeScript type in one place!)
const UserSchema = z.object({
    id: z.number().int().positive(),
    name: z.string().min(1).max(100),
    email: z.string().email(),
    age: z.number().int().min(0).max(150).optional(),
    role: z.enum(["admin", "user", "moderator"]),
    tags: z.array(z.string()).default([]),
    metadata: z.record(z.string(), z.unknown()).optional(),
});

// Extract TypeScript type FROM the schema (single source of truth!)
type User = z.infer<typeof UserSchema>;
// { id: number; name: string; email: string; age?: number; role: "admin" | "user" | "moderator"; ... }

// Validate at runtime
function createUser(input: unknown): User {
    return UserSchema.parse(input);
    // Throws ZodError if invalid
}

// Safe parse (no throw)
const result = UserSchema.safeParse(input);
if (result.success) {
    const user = result.data;    // Type: User
} else {
    console.error(result.error.issues);
}

// Compose schemas
const CreateUserSchema = UserSchema.omit({ id: true });
const UpdateUserSchema = UserSchema.partial().omit({ id: true });
const UserPreviewSchema = UserSchema.pick({ id: true, name: true });

// Transform
const ApiUserSchema = z.object({
    user_name: z.string(),
    user_email: z.string().email(),
}).transform(data => ({
    name: data.user_name,
    email: data.user_email,
}));

// Async validation
const UniqueEmailSchema = z.string().email().refine(
    async (email) => {
        const exists = await db.users.findByEmail(email);
        return !exists;
    },
    { message: "Email already taken" }
);

// In Express/Fastify middleware
function validate<T>(schema: z.ZodSchema<T>) {
    return (req: Request, res: Response, next: NextFunction) => {
        const result = schema.safeParse(req.body);
        if (!result.success) {
            return res.status(400).json({ errors: result.error.issues });
        }
        req.body = result.data;
        next();
    };
}

app.post("/users", validate(CreateUserSchema), async (req, res) => {
    const user = req.body;   // Fully typed and validated!
});
```


## Type-Safe Event Emitter

```typescript
type EventMap = {
    "user:login": { userId: string; timestamp: Date };
    "user:logout": { userId: string };
    "order:created": { orderId: string; total: number };
    "error": { message: string; code: number };
};

class TypedEventEmitter<Events extends Record<string, any>> {
    private handlers: Partial<{
        [K in keyof Events]: Array<(data: Events[K]) => void>;
    }> = {};

    on<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): void {
        if (!this.handlers[event]) this.handlers[event] = [];
        this.handlers[event]!.push(handler);
    }

    emit<K extends keyof Events>(event: K, data: Events[K]): void {
        this.handlers[event]?.forEach(h => h(data));
    }

    off<K extends keyof Events>(event: K, handler: (data: Events[K]) => void): void {
        const handlers = this.handlers[event];
        if (handlers) {
            this.handlers[event] = handlers.filter(h => h !== handler);
        }
    }
}

const emitter = new TypedEventEmitter<EventMap>();

emitter.on("user:login", (data) => {
    console.log(data.userId);      // Type: string
    console.log(data.timestamp);   // Type: Date
});

emitter.emit("user:login", {
    userId: "123",
    timestamp: new Date(),
});

emitter.emit("user:login", {
    userId: 123,          // Error! Must be string
});

emitter.on("nonexistent", () => {});   // Error! Not in EventMap
```


---

# CHAPTER 5: REACT WITH TYPESCRIPT


## Component Props

```typescript
// Props interface
interface ButtonProps {
    label: string;
    onClick: () => void;
    variant?: "primary" | "secondary" | "danger";
    disabled?: boolean;
    icon?: React.ReactNode;
    size?: "sm" | "md" | "lg";
}

function Button({ label, onClick, variant = "primary", disabled = false, icon, size = "md" }: ButtonProps) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`btn btn-${variant} btn-${size}`}
        >
            {icon && <span className="icon">{icon}</span>}
            {label}
        </button>
    );
}

// Children prop
interface CardProps {
    title: string;
    children: React.ReactNode;   // Accepts any renderable content
}

function Card({ title, children }: CardProps) {
    return (
        <div className="card">
            <h2>{title}</h2>
            <div>{children}</div>
        </div>
    );
}

// Extending HTML element props
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label: string;
    error?: string;
}

function Input({ label, error, ...rest }: InputProps) {
    return (
        <div>
            <label>{label}</label>
            <input {...rest} />
            {error && <span className="error">{error}</span>}
        </div>
    );
}
// Now accepts ALL native input props + label + error

// Polymorphic component (render as different elements)
interface BoxProps<T extends React.ElementType = "div"> {
    as?: T;
    children: React.ReactNode;
}

type PolymorphicProps<T extends React.ElementType> =
    BoxProps<T> & Omit<React.ComponentPropsWithoutRef<T>, keyof BoxProps>;

function Box<T extends React.ElementType = "div">({
    as,
    children,
    ...rest
}: PolymorphicProps<T>) {
    const Component = as || "div";
    return <Component {...rest}>{children}</Component>;
}

<Box>Default div</Box>
<Box as="section">Section element</Box>
<Box as="a" href="/about">Link element</Box>
```


## Hooks with TypeScript

```typescript
// useState
const [count, setCount] = useState(0);            // Inferred: number
const [user, setUser] = useState<User | null>(null);  // Explicit

// useRef
const inputRef = useRef<HTMLInputElement>(null);
const intervalRef = useRef<number | null>(null);

function focus() {
    inputRef.current?.focus();
}

// useReducer
type State = {
    count: number;
    error: string | null;
};

type Action =
    | { type: "increment" }
    | { type: "decrement" }
    | { type: "set"; payload: number }
    | { type: "error"; message: string };

function reducer(state: State, action: Action): State {
    switch (action.type) {
        case "increment": return { ...state, count: state.count + 1 };
        case "decrement": return { ...state, count: state.count - 1 };
        case "set": return { ...state, count: action.payload };
        case "error": return { ...state, error: action.message };
    }
}

const [state, dispatch] = useReducer(reducer, { count: 0, error: null });
dispatch({ type: "increment" });
dispatch({ type: "set", payload: 42 });
dispatch({ type: "set" });              // Error! Missing payload

// Custom hook with generics
function useLocalStorage<T>(key: string, initialValue: T) {
    const [stored, setStored] = useState<T>(() => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch {
            return initialValue;
        }
    });

    const setValue = (value: T | ((prev: T) => T)) => {
        const valueToStore = value instanceof Function ? value(stored) : value;
        setStored(valueToStore);
        localStorage.setItem(key, JSON.stringify(valueToStore));
    };

    return [stored, setValue] as const;
}

const [theme, setTheme] = useLocalStorage<"light" | "dark">("theme", "light");
// theme: "light" | "dark"
// setTheme: (value: "light" | "dark" | ((prev) => ...)) => void

// useMemo / useCallback with proper types
const filtered = useMemo<User[]>(() => {
    return users.filter(u => u.active);
}, [users]);

const handleClick = useCallback((id: string) => {
    deleteUser(id);
}, [deleteUser]);
```


## Context with TypeScript

```typescript
interface ThemeContextType {
    theme: "light" | "dark";
    toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

function useTheme(): ThemeContextType {
    const context = useContext(ThemeContext);
    if (!context) {
        throw new Error("useTheme must be used within ThemeProvider");
    }
    return context;
}

function ThemeProvider({ children }: { children: React.ReactNode }) {
    const [theme, setTheme] = useState<"light" | "dark">("light");
    const toggleTheme = useCallback(() => {
        setTheme(prev => prev === "light" ? "dark" : "light");
    }, []);

    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}

// Usage
function Header() {
    const { theme, toggleTheme } = useTheme();
    return <button onClick={toggleTheme}>Current: {theme}</button>;
}
```


---

# CHAPTER 6: TSCONFIG AND TOOLING


## Recommended tsconfig.json

```jsonc
{
    "compilerOptions": {
        // Output
        "target": "ES2022",
        "module": "ESNext",
        "moduleResolution": "bundler",
        "outDir": "dist",
        "rootDir": "src",

        // Strictness (ALWAYS enable all of these)
        "strict": true,
        "noUncheckedIndexedAccess": true,
        "noImplicitOverride": true,
        "noPropertyAccessFromIndexSignature": true,
        "noFallthroughCasesInSwitch": true,
        "forceConsistentCasingInFileNames": true,
        "exactOptionalPropertyTypes": true,

        // Interop
        "esModuleInterop": true,
        "allowSyntheticDefaultImports": true,
        "resolveJsonModule": true,
        "isolatedModules": true,

        // Declaration files
        "declaration": true,
        "declarationMap": true,
        "sourceMap": true,

        // Path aliases
        "baseUrl": ".",
        "paths": {
            "@/*": ["src/*"],
            "@/components/*": ["src/components/*"],
            "@/utils/*": ["src/utils/*"]
        },

        // Skip type checking of node_modules
        "skipLibCheck": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```


## Common Pitfalls

```typescript
// PITFALL 1: Using 'any' everywhere
function bad(data: any): any { return data.foo; }
// Defeats the purpose of TypeScript!
// FIX: Use 'unknown' + narrowing
function good(data: unknown): string | undefined {
    if (typeof data === "object" && data !== null && "foo" in data) {
        return (data as { foo: string }).foo;
    }
}

// PITFALL 2: Type assertions instead of narrowing
const user = response as User;   // DANGEROUS: no runtime check!
// FIX: Validate with Zod or type guard
const user = UserSchema.parse(response);   // Runtime check + type

// PITFALL 3: Forgetting to handle null/undefined
function getUser(id: string): User | null { /* ... */ }
const user = getUser("1");
console.log(user.name);   // Error with strict null checks (good!)
// FIX:
if (user) console.log(user.name);

// PITFALL 4: Enum vs union type
enum Status { Active, Inactive }   // Generates runtime code
type Status2 = "active" | "inactive";   // Zero runtime code, works with JSON
// PREFER union types in most cases

// PITFALL 5: Interface for everything
type Callback = (data: string) => void;   // Type alias is better here
// Interface can't represent unions, tuples, or mapped types

// PITFALL 6: Not using 'as const'
const ROUTES = {
    home: "/",
    about: "/about",
};
// Type: { home: string; about: string; } — too wide!
const ROUTES2 = {
    home: "/",
    about: "/about",
} as const;
// Type: { readonly home: "/"; readonly about: "/about"; } — exact!

// PITFALL 7: Object.keys returns string[]
const user = { name: "Alice", age: 30 };
Object.keys(user);   // string[] (not ("name" | "age")[])
// Workaround:
const keys = Object.keys(user) as Array<keyof typeof user>;
// Or use a helper:
function typedKeys<T extends object>(obj: T): Array<keyof T> {
    return Object.keys(obj) as Array<keyof T>;
}

// PITFALL 8: Forgetting return types on public APIs
// BAD: inferred return type can change accidentally
export function getConfig() {
    return { port: 3000, host: "localhost" };
}
// GOOD: explicit return type = contract
export function getConfig(): { port: number; host: string } {
    return { port: 3000, host: "localhost" };
}

// PITFALL 9: Not using discriminated unions for state
// BAD
interface State {
    loading: boolean;
    data: User[] | null;
    error: string | null;
}
// Problem: loading=false, data=null, error=null — what state is this?

// GOOD: discriminated union
type State =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: User[] }
    | { status: "error"; message: string };
// Each state is explicit and self-documenting

// PITFALL 10: Ignoring strict mode
// "strict": false in tsconfig → you're writing JavaScript with extra steps
// ALWAYS enable strict mode. Fix the errors, don't disable the checks.
```