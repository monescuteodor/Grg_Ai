# Testing Patterns Complete Reference


---

# CHAPTER 1: TESTING FUNDAMENTALS


## Remarks

Testing is writing code that verifies your other code works correctly. It prevents regressions (bugs reintroduced when changing code), enables confident refactoring, serves as living documentation, and catches bugs before users do. Companies like Google, Microsoft, and Netflix mandate high test coverage as a condition for production deployment.

Key concepts: **Test Pyramid** (many unit, some integration, few E2E), **AAA pattern** (Arrange, Act, Assert), **TDD** (Test-Driven Development — test first, code second), **Mocking** (replacing real dependencies with fakes), **Code coverage** (percentage of code exercised by tests), **CI testing** (automated on every commit), **Flaky tests** (pass/fail randomly — the worst), **Contract testing** (verify API contracts between services).

Used by: every professional software project. Untested code is legacy code.

Tools: **Jest** (JS/TS), **Vitest** (faster Jest), **Pytest** (Python), **JUnit** (Java/Kotlin), **XCTest** (Swift), **React Testing Library** (component tests), **Playwright/Cypress** (E2E browser), **Detox** (E2E mobile), **Pact** (contract testing), **Istanbul/c8** (coverage).


## The Test Pyramid

```
         ┌──────────┐
         │   E2E    │     Few (slow, expensive, fragile)
         │ Browser  │     Test full user flows
         ├──────────┤
         │Integration│    Some (medium speed)
         │  Tests    │    Test components together
         ├──────────┤
         │  Unit    │     MANY (fast, cheap, reliable)
         │  Tests   │     Test individual functions/classes
         └──────────┘

IDEAL RATIO:
  70% Unit tests        (milliseconds each)
  20% Integration tests (seconds each)
  10% E2E tests         (minutes each)

UNIT TEST:
  Test one function/class in isolation.
  Mock all dependencies.
  Fast (1000s per second).
  Example: test that calculateTax(100, 0.2) returns 20.

INTEGRATION TEST:
  Test multiple components working together.
  May use real DB, real HTTP, real file system.
  Slower (seconds).
  Example: test that POST /users creates user in DB and sends email.

E2E TEST:
  Test entire application from user's perspective.
  Real browser, real server, real database.
  Slowest (minutes).
  Example: test that user can sign up, log in, create post, and log out.

ANTI-PATTERN: Ice cream cone (inverted pyramid)
  Many E2E tests, few unit tests.
  → Slow CI, flaky tests, hard to debug failures.
```


## AAA Pattern (Arrange, Act, Assert)

```javascript
// ARRANGE: set up test data and conditions
// ACT: perform the action being tested
// ASSERT: verify the result

test('calculateTotal applies discount correctly', () => {
    // Arrange
    const items = [
        { name: 'Widget', price: 100, quantity: 2 },
        { name: 'Gadget', price: 50, quantity: 1 },
    ];
    const discount = 0.1;   // 10% discount

    // Act
    const total = calculateTotal(items, discount);

    // Assert
    expect(total).toBe(225);   // (200 + 50) * 0.9 = 225
});

// ALSO KNOWN AS:
// Given-When-Then (BDD style)
// given: items and discount
// when: calculateTotal is called
// then: returns 225
```


## What to Test (and What NOT to)

```
TEST:
  ✅ Business logic (calculations, transformations, rules)
  ✅ Edge cases (empty input, null, zero, negative, max values)
  ✅ Error handling (what happens when things fail)
  ✅ Public API surface (inputs → outputs)
  ✅ State transitions (idle → loading → success/error)
  ✅ Integration points (DB queries, API calls)
  ✅ Security-critical paths (auth, permissions, validation)

DON'T TEST:
  ❌ Implementation details (private methods, internal state)
  ❌ Third-party libraries (they have their own tests)
  ❌ Trivial code (getters/setters with no logic)
  ❌ Framework boilerplate (React renders, Express routes)
  ❌ Exact UI layout (pixel-perfect tests are fragile)
  ❌ Generated code (protobuf, OpenAPI clients)

FOCUS ON BEHAVIOR, NOT IMPLEMENTATION:
  BAD: "test that _internalCache has 3 entries after 3 calls"
  GOOD: "test that third call returns cached result in <1ms"
```


---

# CHAPTER 2: UNIT TESTING


## Jest / Vitest Basics

```javascript
// math.ts
export function add(a: number, b: number): number {
    return a + b;
}

export function divide(a: number, b: number): number {
    if (b === 0) throw new Error('Division by zero');
    return a / b;
}

export function clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
}


// math.test.ts
import { describe, it, expect } from 'vitest';   // or 'jest'
import { add, divide, clamp } from './math';

describe('add', () => {
    it('adds two positive numbers', () => {
        expect(add(2, 3)).toBe(5);
    });

    it('handles negative numbers', () => {
        expect(add(-1, -2)).toBe(-3);
        expect(add(-1, 5)).toBe(4);
    });

    it('handles zero', () => {
        expect(add(0, 0)).toBe(0);
        expect(add(5, 0)).toBe(5);
    });
});

describe('divide', () => {
    it('divides correctly', () => {
        expect(divide(10, 2)).toBe(5);
        expect(divide(7, 2)).toBe(3.5);
    });

    it('throws on division by zero', () => {
        expect(() => divide(10, 0)).toThrow('Division by zero');
    });

    it('handles negative division', () => {
        expect(divide(-10, 2)).toBe(-5);
    });
});

describe('clamp', () => {
    it('returns value when within range', () => {
        expect(clamp(5, 0, 10)).toBe(5);
    });

    it('clamps to min when below', () => {
        expect(clamp(-5, 0, 10)).toBe(0);
    });

    it('clamps to max when above', () => {
        expect(clamp(15, 0, 10)).toBe(10);
    });

    it('handles edge: value equals min', () => {
        expect(clamp(0, 0, 10)).toBe(0);
    });

    it('handles edge: value equals max', () => {
        expect(clamp(10, 0, 10)).toBe(10);
    });
});
```


## Matchers

```javascript
// Equality
expect(value).toBe(5);                    // === strict
expect(object).toEqual({ a: 1 });        // Deep equality
expect(value).not.toBe(3);               // Negation

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3);
expect(value).toBeLessThan(5);
expect(0.1 + 0.2).toBeCloseTo(0.3);     // Float comparison

// Strings
expect(str).toMatch(/pattern/);
expect(str).toContain('substring');
expect(str).toHaveLength(5);

// Arrays
expect(arr).toContain(item);
expect(arr).toHaveLength(3);
expect(arr).toEqual(expect.arrayContaining([1, 2]));

// Objects
expect(obj).toHaveProperty('name');
expect(obj).toHaveProperty('address.city', 'NYC');
expect(obj).toMatchObject({ name: 'Alice' });   // Partial match
expect(obj).toEqual(expect.objectContaining({ name: 'Alice' }));

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('specific message');
expect(() => fn()).toThrow(TypeError);

// Async
await expect(asyncFn()).resolves.toBe(42);
await expect(asyncFn()).rejects.toThrow('error');

// Snapshots (careful — can become stale)
expect(component).toMatchSnapshot();
expect(data).toMatchInlineSnapshot(`
    Object {
      "name": "Alice",
      "age": 30,
    }
`);
```


## Testing Async Code

```javascript
// Promises
test('fetches user data', async () => {
    const user = await fetchUser(1);
    expect(user.name).toBe('Alice');
});

// Rejections
test('throws for invalid id', async () => {
    await expect(fetchUser(-1)).rejects.toThrow('Invalid ID');
});

// Timers
test('debounced function calls after delay', () => {
    jest.useFakeTimers();

    const fn = jest.fn();
    const debounced = debounce(fn, 500);

    debounced();
    expect(fn).not.toHaveBeenCalled();

    jest.advanceTimersByTime(499);
    expect(fn).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1);
    expect(fn).toHaveBeenCalledTimes(1);

    jest.useRealTimers();
});

// Event-based
test('emits event on save', (done) => {
    emitter.on('saved', (data) => {
        expect(data.id).toBe(1);
        done();   // Signal test completion
    });
    emitter.save({ id: 1 });
});
```


## Setup and Teardown

```javascript
describe('UserService', () => {
    let service: UserService;
    let db: TestDatabase;

    // Run ONCE before all tests in this describe
    beforeAll(async () => {
        db = await TestDatabase.create();
    });

    // Run ONCE after all tests
    afterAll(async () => {
        await db.close();
    });

    // Run before EACH test
    beforeEach(async () => {
        await db.clear();   // Clean state per test
        service = new UserService(db);
    });

    // Run after EACH test
    afterEach(() => {
        jest.restoreAllMocks();
    });

    test('creates user', async () => {
        const user = await service.create({ name: 'Alice' });
        expect(user.id).toBeDefined();
    });

    test('finds user by id', async () => {
        const created = await service.create({ name: 'Bob' });
        const found = await service.findById(created.id);
        expect(found.name).toBe('Bob');
    });
});
```


---

# CHAPTER 3: MOCKING


## Why Mock?

```
MOCKING: replace real dependency with a fake that you control.

REASONS:
  1. ISOLATION — test one thing, not its dependencies
  2. SPEED — avoid slow I/O (DB, network, file system)
  3. CONTROL — simulate errors, edge cases, specific responses
  4. DETERMINISM — no flaky tests from external services

TYPES:
  STUB:    Returns predetermined values (no verification)
  MOCK:    Records calls and can verify interactions
  SPY:     Wraps real function, records calls but still executes
  FAKE:    Working implementation but simplified (in-memory DB)
```


## Jest/Vitest Mocking

```javascript
// Mock a module
jest.mock('./emailService');
import { sendEmail } from './emailService';

test('sends welcome email on registration', async () => {
    // sendEmail is now a mock function
    (sendEmail as jest.Mock).mockResolvedValue({ sent: true });

    await registerUser({ name: 'Alice', email: 'alice@example.com' });

    expect(sendEmail).toHaveBeenCalledTimes(1);
    expect(sendEmail).toHaveBeenCalledWith(
        'alice@example.com',
        'Welcome!',
        expect.stringContaining('Alice')
    );
});


// Mock with implementation
jest.mock('./database', () => ({
    findUser: jest.fn().mockResolvedValue({ id: 1, name: 'Alice' }),
    saveUser: jest.fn().mockResolvedValue({ id: 2, name: 'Bob' }),
}));


// Spy on existing function
const consoleSpy = jest.spyOn(console, 'log');
doSomething();
expect(consoleSpy).toHaveBeenCalledWith('Expected message');
consoleSpy.mockRestore();


// Mock return values
const mock = jest.fn();
mock.mockReturnValue(42);              // Always returns 42
mock.mockReturnValueOnce(1);           // First call returns 1
mock.mockReturnValueOnce(2);           // Second call returns 2
mock.mockResolvedValue({ ok: true });  // Returns Promise.resolve(...)
mock.mockRejectedValue(new Error());   // Returns Promise.reject(...)

// Mock implementation
mock.mockImplementation((x) => x * 2);


// Verify mock calls
expect(mock).toHaveBeenCalled();
expect(mock).toHaveBeenCalledTimes(3);
expect(mock).toHaveBeenCalledWith('arg1', 'arg2');
expect(mock).toHaveBeenLastCalledWith('latest');
expect(mock).toHaveBeenNthCalledWith(1, 'first call args');

// Access call details
mock.mock.calls;                        // [[arg1, arg2], [arg3]]
mock.mock.results;                      // [{type: 'return', value: 42}]
mock.mock.calls[0][0];                  // First call, first argument


// Clear vs Reset vs Restore
mock.mockClear();     // Clear calls and results (keeps implementation)
mock.mockReset();     // Clear + remove implementation
mock.mockRestore();   // Restore original (only for spies)
```


## Dependency Injection for Testing

```typescript
// BAD: hard to test (creates its own dependencies)
class OrderService {
    private db = new Database();
    private emailer = new EmailService();
    private stripe = new StripeClient();

    async createOrder(data: OrderData) {
        const order = await this.db.orders.create(data);
        await this.emailer.send(data.email, 'Order confirmed');
        await this.stripe.charge(data.total);
        return order;
    }
}

// GOOD: dependencies injected (easy to mock)
class OrderService {
    constructor(
        private db: Database,
        private emailer: EmailService,
        private stripe: PaymentClient,
    ) {}

    async createOrder(data: OrderData) {
        const order = await this.db.orders.create(data);
        await this.emailer.send(data.email, 'Order confirmed');
        await this.stripe.charge(data.total);
        return order;
    }
}

// Test with mocks
test('createOrder creates order and sends email', async () => {
    const mockDb = {
        orders: {
            create: jest.fn().mockResolvedValue({ id: 1, ...orderData }),
        },
    };
    const mockEmailer = { send: jest.fn().mockResolvedValue(true) };
    const mockStripe = { charge: jest.fn().mockResolvedValue({ paid: true }) };

    const service = new OrderService(mockDb as any, mockEmailer as any, mockStripe as any);

    const result = await service.createOrder(orderData);

    expect(result.id).toBe(1);
    expect(mockDb.orders.create).toHaveBeenCalledWith(orderData);
    expect(mockEmailer.send).toHaveBeenCalledWith(orderData.email, 'Order confirmed');
    expect(mockStripe.charge).toHaveBeenCalledWith(orderData.total);
});

// Test error handling
test('rolls back if payment fails', async () => {
    const mockDb = {
        orders: {
            create: jest.fn().mockResolvedValue({ id: 1 }),
            delete: jest.fn().mockResolvedValue(true),
        },
    };
    const mockStripe = {
        charge: jest.fn().mockRejectedValue(new Error('Card declined')),
    };

    const service = new OrderService(mockDb as any, mockEmailer as any, mockStripe as any);

    await expect(service.createOrder(orderData)).rejects.toThrow('Card declined');
    expect(mockDb.orders.delete).toHaveBeenCalledWith(1);
});
```


## HTTP Mocking (MSW)

```typescript
// Mock Service Worker — intercepts actual HTTP requests
// Works in tests AND browser (dev mode)
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const handlers = [
    http.get('https://api.example.com/users/:id', ({ params }) => {
        return HttpResponse.json({
            id: params.id,
            name: 'Alice',
            email: 'alice@example.com',
        });
    }),

    http.post('https://api.example.com/users', async ({ request }) => {
        const body = await request.json();
        return HttpResponse.json(
            { id: '123', ...body },
            { status: 201 }
        );
    }),

    // Simulate error
    http.get('https://api.example.com/users/999', () => {
        return HttpResponse.json(
            { error: { code: 'NOT_FOUND', message: 'User not found' } },
            { status: 404 }
        );
    }),

    // Simulate network error
    http.get('https://api.example.com/health', () => {
        return HttpResponse.error();
    }),
];

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('fetches user successfully', async () => {
    const user = await apiClient.getUser('1');
    expect(user.name).toBe('Alice');
});

test('handles 404 gracefully', async () => {
    const user = await apiClient.getUser('999');
    expect(user).toBeNull();
});

// Override handler for specific test
test('handles server error', async () => {
    server.use(
        http.get('https://api.example.com/users/:id', () => {
            return HttpResponse.json({ error: 'Server error' }, { status: 500 });
        })
    );

    await expect(apiClient.getUser('1')).rejects.toThrow();
});
```


---

# CHAPTER 4: INTEGRATION TESTING


## Database Integration Tests

```typescript
// Use test database (NOT production!)
import { Pool } from 'pg';

let pool: Pool;

beforeAll(async () => {
    pool = new Pool({
        connectionString: process.env.TEST_DATABASE_URL,
    });
    // Run migrations
    await runMigrations(pool);
});

afterAll(async () => {
    await pool.end();
});

beforeEach(async () => {
    // Clean tables before each test (order matters for FK constraints)
    await pool.query('TRUNCATE orders, users CASCADE');
});

describe('UserRepository', () => {
    const repo = new UserRepository(pool);

    test('creates and retrieves user', async () => {
        // Arrange + Act
        const created = await repo.create({
            name: 'Alice',
            email: 'alice@example.com',
        });

        // Assert
        expect(created.id).toBeDefined();
        expect(created.name).toBe('Alice');

        // Verify in DB
        const found = await repo.findById(created.id);
        expect(found).toEqual(created);
    });

    test('enforces unique email', async () => {
        await repo.create({ name: 'Alice', email: 'alice@example.com' });

        await expect(
            repo.create({ name: 'Bob', email: 'alice@example.com' })
        ).rejects.toThrow(/unique/i);
    });

    test('returns null for non-existent user', async () => {
        const found = await repo.findById('nonexistent-uuid');
        expect(found).toBeNull();
    });

    test('updates user fields', async () => {
        const user = await repo.create({ name: 'Alice', email: 'a@b.com' });
        const updated = await repo.update(user.id, { name: 'Alice Smith' });

        expect(updated.name).toBe('Alice Smith');
        expect(updated.email).toBe('a@b.com');   // Unchanged
    });

    test('deletes user', async () => {
        const user = await repo.create({ name: 'Alice', email: 'a@b.com' });
        await repo.delete(user.id);

        const found = await repo.findById(user.id);
        expect(found).toBeNull();
    });
});
```


## API Integration Tests

```typescript
// Test actual HTTP endpoints with real server
import { createApp } from '../app';
import supertest from 'supertest';

let app: Express;
let request: supertest.SuperTest<supertest.Test>;

beforeAll(async () => {
    app = await createApp({
        database: testDatabaseUrl,
        redis: testRedisUrl,
    });
    request = supertest(app);
});

afterAll(async () => {
    await app.close();
});

beforeEach(async () => {
    await cleanDatabase();
});

describe('POST /api/users', () => {
    test('creates user with valid data', async () => {
        const response = await request
            .post('/api/users')
            .send({ name: 'Alice', email: 'alice@example.com' })
            .expect(201);

        expect(response.body).toMatchObject({
            id: expect.any(String),
            name: 'Alice',
            email: 'alice@example.com',
        });
        expect(response.headers.location).toMatch(/\/api\/users\/.+/);
    });

    test('returns 422 for invalid email', async () => {
        const response = await request
            .post('/api/users')
            .send({ name: 'Alice', email: 'not-email' })
            .expect(422);

        expect(response.body.error.code).toBe('VALIDATION_ERROR');
        expect(response.body.error.details[0].field).toBe('email');
    });

    test('returns 409 for duplicate email', async () => {
        await request
            .post('/api/users')
            .send({ name: 'Alice', email: 'alice@example.com' })
            .expect(201);

        await request
            .post('/api/users')
            .send({ name: 'Bob', email: 'alice@example.com' })
            .expect(409);
    });
});

describe('GET /api/users/:id', () => {
    test('returns user by id', async () => {
        const created = await request
            .post('/api/users')
            .send({ name: 'Alice', email: 'alice@example.com' });

        const response = await request
            .get(`/api/users/${created.body.id}`)
            .expect(200);

        expect(response.body.name).toBe('Alice');
    });

    test('returns 404 for non-existent user', async () => {
        await request
            .get('/api/users/nonexistent-uuid')
            .expect(404);
    });
});

describe('Authentication required', () => {
    test('returns 401 without token', async () => {
        await request
            .get('/api/users')
            .expect(401);
    });

    test('returns 401 with expired token', async () => {
        await request
            .get('/api/users')
            .set('Authorization', `Bearer ${expiredToken}`)
            .expect(401);
    });

    test('succeeds with valid token', async () => {
        await request
            .get('/api/users')
            .set('Authorization', `Bearer ${validToken}`)
            .expect(200);
    });
});
```


## Docker-Based Test Environment

```yaml
# docker-compose.test.yml
version: '3.9'
services:
  test-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: test
      POSTGRES_PASSWORD: test
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data   # RAM-based for speed!

  test-redis:
    image: redis:7-alpine
    ports:
      - "6380:6379"
```

```bash
# Run integration tests
docker compose -f docker-compose.test.yml up -d
TEST_DATABASE_URL=postgres://postgres:test@localhost:5433/test \
TEST_REDIS_URL=redis://localhost:6380 \
npm test -- --testPathPattern=integration
docker compose -f docker-compose.test.yml down
```


---

# CHAPTER 5: COMPONENT TESTING (REACT)


## React Testing Library

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter', () => {
    test('renders initial count', () => {
        render(<Counter initialCount={5} />);
        expect(screen.getByText('Count: 5')).toBeInTheDocument();
    });

    test('increments on button click', async () => {
        const user = userEvent.setup();
        render(<Counter initialCount={0} />);

        await user.click(screen.getByRole('button', { name: /increment/i }));

        expect(screen.getByText('Count: 1')).toBeInTheDocument();
    });

    test('decrements on button click', async () => {
        const user = userEvent.setup();
        render(<Counter initialCount={5} />);

        await user.click(screen.getByRole('button', { name: /decrement/i }));

        expect(screen.getByText('Count: 4')).toBeInTheDocument();
    });

    test('does not go below zero', async () => {
        const user = userEvent.setup();
        render(<Counter initialCount={0} />);

        await user.click(screen.getByRole('button', { name: /decrement/i }));

        expect(screen.getByText('Count: 0')).toBeInTheDocument();
    });
});


// Testing forms
describe('LoginForm', () => {
    test('submits with valid credentials', async () => {
        const onSubmit = jest.fn();
        const user = userEvent.setup();
        render(<LoginForm onSubmit={onSubmit} />);

        await user.type(screen.getByLabelText(/email/i), 'alice@example.com');
        await user.type(screen.getByLabelText(/password/i), 'password123');
        await user.click(screen.getByRole('button', { name: /login/i }));

        expect(onSubmit).toHaveBeenCalledWith({
            email: 'alice@example.com',
            password: 'password123',
        });
    });

    test('shows validation errors', async () => {
        const user = userEvent.setup();
        render(<LoginForm onSubmit={jest.fn()} />);

        await user.click(screen.getByRole('button', { name: /login/i }));

        expect(screen.getByText(/email is required/i)).toBeInTheDocument();
        expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });

    test('disables submit while loading', async () => {
        const onSubmit = jest.fn(() => new Promise(() => {}));   // Never resolves
        const user = userEvent.setup();
        render(<LoginForm onSubmit={onSubmit} />);

        await user.type(screen.getByLabelText(/email/i), 'a@b.com');
        await user.type(screen.getByLabelText(/password/i), 'pass');
        await user.click(screen.getByRole('button', { name: /login/i }));

        expect(screen.getByRole('button', { name: /login/i })).toBeDisabled();
    });
});


// Testing async data loading
describe('UserList', () => {
    test('shows loading then data', async () => {
        render(<UserList />);

        // Initially loading
        expect(screen.getByText(/loading/i)).toBeInTheDocument();

        // After data loads
        await waitFor(() => {
            expect(screen.getByText('Alice')).toBeInTheDocument();
            expect(screen.getByText('Bob')).toBeInTheDocument();
        });

        // Loading gone
        expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });

    test('shows error on failure', async () => {
        server.use(
            http.get('/api/users', () => HttpResponse.error())
        );

        render(<UserList />);

        await waitFor(() => {
            expect(screen.getByText(/error/i)).toBeInTheDocument();
        });
    });
});
```


## Query Priority (React Testing Library)

```
PRIORITY ORDER (use the most accessible query):

1. getByRole          BEST — accessible, semantic
   screen.getByRole('button', { name: /submit/i })
   screen.getByRole('textbox', { name: /email/i })
   screen.getByRole('heading', { level: 2 })

2. getByLabelText     Forms — what users see
   screen.getByLabelText(/email address/i)

3. getByPlaceholderText
   screen.getByPlaceholderText(/search/i)

4. getByText          Visible text
   screen.getByText(/welcome/i)

5. getByDisplayValue  Current input value
   screen.getByDisplayValue('alice@example.com')

6. getByAltText       Images
   screen.getByAltText(/profile photo/i)

7. getByTestId        LAST RESORT — implementation detail
   screen.getByTestId('custom-element')

VARIANTS:
  getBy...        — throws if not found (expect element exists)
  queryBy...      — returns null if not found (expect element doesn't exist)
  findBy...       — waits and returns Promise (async elements)
  getAllBy...      — returns array (multiple matches)
```


---

# CHAPTER 6: E2E TESTING


## Playwright

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
    testDir: './e2e',
    timeout: 30000,
    retries: 2,
    use: {
        baseURL: 'http://localhost:3000',
        screenshot: 'only-on-failure',
        trace: 'retain-on-failure',
    },
    projects: [
        { name: 'chromium', use: { browserName: 'chromium' } },
        { name: 'firefox', use: { browserName: 'firefox' } },
        { name: 'mobile', use: { ...devices['iPhone 13'] } },
    ],
    webServer: {
        command: 'npm run dev',
        port: 3000,
        reuseExistingServer: !process.env.CI,
    },
});

// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
    test('user can sign up and log in', async ({ page }) => {
        // Navigate to signup
        await page.goto('/signup');

        // Fill form
        await page.getByLabel('Name').fill('Alice');
        await page.getByLabel('Email').fill('alice@example.com');
        await page.getByLabel('Password').fill('SecurePass123!');
        await page.getByRole('button', { name: 'Sign Up' }).click();

        // Verify redirect to dashboard
        await expect(page).toHaveURL('/dashboard');
        await expect(page.getByText('Welcome, Alice')).toBeVisible();

        // Log out
        await page.getByRole('button', { name: 'Logout' }).click();
        await expect(page).toHaveURL('/login');

        // Log back in
        await page.getByLabel('Email').fill('alice@example.com');
        await page.getByLabel('Password').fill('SecurePass123!');
        await page.getByRole('button', { name: 'Log In' }).click();

        await expect(page).toHaveURL('/dashboard');
    });

    test('shows error for invalid credentials', async ({ page }) => {
        await page.goto('/login');

        await page.getByLabel('Email').fill('wrong@example.com');
        await page.getByLabel('Password').fill('wrongpassword');
        await page.getByRole('button', { name: 'Log In' }).click();

        await expect(page.getByText('Invalid credentials')).toBeVisible();
        await expect(page).toHaveURL('/login');   // No redirect
    });
});

// Visual regression
test('homepage looks correct', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
        maxDiffPixelRatio: 0.01,
    });
});

// Network interception
test('handles API failure gracefully', async ({ page }) => {
    await page.route('**/api/users', (route) =>
        route.fulfill({ status: 500, body: 'Server Error' })
    );
    await page.goto('/users');
    await expect(page.getByText('Something went wrong')).toBeVisible();
});
```


## Pytest (Python E2E)

```python
import pytest
import httpx

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client

@pytest.fixture
def auth_token(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123",
    })
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


class TestUserAPI:
    def test_create_user(self, client, auth_headers):
        response = client.post("/api/users", json={
            "name": "Alice",
            "email": "alice@test.com",
        }, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alice"
        assert "id" in data

    def test_list_users(self, client, auth_headers):
        response = client.get("/api/users", headers=auth_headers)

        assert response.status_code == 200
        assert isinstance(response.json()["data"], list)

    def test_unauthorized_without_token(self, client):
        response = client.get("/api/users")
        assert response.status_code == 401

    def test_validation_error(self, client, auth_headers):
        response = client.post("/api/users", json={
            "name": "",
            "email": "not-email",
        }, headers=auth_headers)

        assert response.status_code == 422
        errors = response.json()["error"]["details"]
        assert any(e["field"] == "email" for e in errors)
```


---

# CHAPTER 7: TEST-DRIVEN DEVELOPMENT (TDD)


## TDD Cycle: Red-Green-Refactor

```
1. RED:    Write a failing test
2. GREEN:  Write minimum code to pass
3. REFACTOR: Clean up without changing behavior

REPEAT for each small piece of functionality.

EXAMPLE: Build a password validator

ITERATION 1: Minimum length
```

```javascript
// RED: write test first
test('rejects passwords shorter than 8 chars', () => {
    expect(validatePassword('short')).toEqual({
        valid: false,
        errors: ['Password must be at least 8 characters'],
    });
});

test('accepts passwords with 8+ chars', () => {
    expect(validatePassword('longpassword')).toEqual({
        valid: true,
        errors: [],
    });
});

// GREEN: minimum code to pass
function validatePassword(password: string) {
    const errors: string[] = [];
    if (password.length < 8) {
        errors.push('Password must be at least 8 characters');
    }
    return { valid: errors.length === 0, errors };
}

// REFACTOR: looks clean already, move on.


// ITERATION 2: Require uppercase
test('rejects passwords without uppercase', () => {
    expect(validatePassword('lowercaseonly')).toEqual({
        valid: false,
        errors: ['Password must contain at least one uppercase letter'],
    });
});

// GREEN: add uppercase check
function validatePassword(password: string) {
    const errors: string[] = [];
    if (password.length < 8)
        errors.push('Password must be at least 8 characters');
    if (!/[A-Z]/.test(password))
        errors.push('Password must contain at least one uppercase letter');
    return { valid: errors.length === 0, errors };
}


// ITERATION 3: Require number
test('rejects passwords without number', () => {
    const result = validatePassword('NoNumberHere');
    expect(result.valid).toBe(false);
    expect(result.errors).toContain('Password must contain at least one number');
});

// GREEN: add number check
// ...and so on, iteration by iteration.
```


## TDD Benefits and Pitfalls

```
BENEFITS:
  ✅ Forces thinking about API design before implementation
  ✅ 100% coverage of intended behavior
  ✅ Catches bugs immediately
  ✅ Produces better design (testable = modular)
  ✅ Confidence to refactor

PITFALLS:
  ❌ Testing implementation details (brittle tests)
  ❌ Spending more time on tests than production code
  ❌ Not doing TDD for exploratory/prototype work
  ❌ Testing trivial code (getters, setters)

WHEN TO USE TDD:
  ✅ Business logic (rules, calculations)
  ✅ Library/SDK code (public API)
  ✅ Bug fixes (write test reproducing bug, then fix)
  ✅ Well-understood requirements

WHEN NOT TO USE TDD:
  ❌ Prototyping / exploring (write tests after)
  ❌ UI layout (too volatile)
  ❌ One-time scripts
  ❌ When requirements are still changing rapidly
```


---

# CHAPTER 8: CODE COVERAGE


## Coverage Metrics

```
LINE COVERAGE:     % of lines executed by tests
BRANCH COVERAGE:   % of if/else branches taken
FUNCTION COVERAGE: % of functions called
STATEMENT COVERAGE: % of statements executed

EXAMPLE:
  function grade(score: number): string {
      if (score >= 90) return 'A';        // Branch 1
      if (score >= 80) return 'B';        // Branch 2
      if (score >= 70) return 'C';        // Branch 3
      return 'F';                          // Branch 4
  }

  test('returns A for 95', () => {
      expect(grade(95)).toBe('A');
  });

  Line coverage:     ~60% (only 'A' path executed)
  Branch coverage:   25% (1 of 4 branches)
  To get 100%: test 95, 85, 75, 50

TOOLS:
  JavaScript: c8, istanbul/nyc, vitest --coverage
  Python: coverage.py, pytest-cov
  Go: go test -cover

COMMANDS:
  npx vitest --coverage                   # Vitest
  npx jest --coverage                      # Jest
  pytest --cov=myapp --cov-report=html    # Pytest
```


## Coverage Targets

```
RECOMMENDED TARGETS:
  Overall:           80%+ line coverage
  Business logic:    90%+ (critical code)
  Utilities/helpers: 95%+ (pure functions, easy to test)
  UI components:     60-80% (behavior, not layout)
  Generated code:    exclude from coverage

IMPORTANT: 100% coverage does NOT mean bug-free!
  function add(a, b) { return a - b; }   // Bug!
  test('add returns number', () => {
      expect(typeof add(1, 2)).toBe('number');
  });
  // 100% coverage, but add is broken!

COVERAGE IS A FLOOR, NOT A CEILING.
  High coverage = necessary but not sufficient.
  Quality of assertions matters more than coverage %.

ENFORCE IN CI:
  // vitest.config.ts
  export default defineConfig({
      test: {
          coverage: {
              provider: 'c8',
              reporter: ['text', 'html', 'lcov'],
              thresholds: {
                  lines: 80,
                  branches: 75,
                  functions: 80,
                  statements: 80,
              },
              exclude: [
                  'node_modules/',
                  '**/*.test.ts',
                  '**/*.d.ts',
                  'src/generated/',
              ],
          },
      },
  });
```


---

# CHAPTER 9: BEST PRACTICES AND PITFALLS


## Test Naming Convention

```
FORMAT: "should [expected behavior] when [condition]"
  OR:   "[unit] [behavior] [condition]"

GOOD:
  "calculateTotal should apply 10% discount when coupon is valid"
  "UserService creates user with hashed password"
  "Login form shows error when email is invalid"
  "API returns 404 when user does not exist"

BAD:
  "test1"
  "it works"
  "handles edge case"
  "calculateTotal test"
```


## Common Pitfalls

```
PITFALL 1: Testing implementation, not behavior
  BAD:  expect(component.state.count).toBe(1)
  GOOD: expect(screen.getByText('Count: 1')).toBeInTheDocument()
  Users see text, not state.

PITFALL 2: Flaky tests (pass sometimes, fail sometimes)
  Causes: timing, order dependency, shared state, network
  Fix: isolate tests, use fake timers, mock external services
  Rule: A flaky test is worse than no test (erodes trust in CI)

PITFALL 3: Slow test suite
  Fix: more unit tests (ms), fewer E2E (min)
  Fix: parallel execution
  Fix: run only affected tests (jest --changedSince=main)
  Target: <5 min total for CI

PITFALL 4: Tests coupled to each other
  BAD: test B depends on test A creating data
  GOOD: each test sets up its own data (beforeEach)

PITFALL 5: Too many mocks (testing mocks, not code)
  If test has 10 mocks, it's testing nothing real.
  Fix: fewer mocks, more integration tests for those cases.

PITFALL 6: Snapshot abuse
  BAD: snapshot entire component (breaks on any change)
  GOOD: snapshot only stable, meaningful output (API responses, config)
  Or: don't use snapshots at all — explicit assertions are clearer.

PITFALL 7: Not testing error paths
  Happy path only → production errors catch you off guard.
  Test: null input, network errors, auth failures, edge values.

PITFALL 8: Ignoring test maintenance
  Tests need refactoring too. Dead tests, outdated mocks.
  Review tests during code review.

PITFALL 9: Testing third-party code
  Don't test that fetch() works. Test YOUR code that uses fetch().

PITFALL 10: No CI integration
  Tests that don't run automatically are tests that get skipped.
  Every PR must pass tests before merge.

PITFALL 11: Console.log in tests
  Noisy output hides real failures.
  Mock console or use proper assertions.

PITFALL 12: God test files
  One test file with 500 tests → impossible to navigate.
  One test file per module/component. Keep focused.

PITFALL 13: Forgetting edge cases
  - Empty arrays/strings
  - null/undefined
  - Zero, negative numbers
  - Very large inputs
  - Unicode/special characters
  - Concurrent access
  - Timezone boundaries

PITFALL 14: Not testing accessibility
  Use getByRole, getByLabelText → forces accessible markup.
  If you can't query by role, your UI isn't accessible.

PITFALL 15: Treating tests as second-class code
  Tests deserve same quality as production code.
  Refactor, name well, keep DRY (but readable).
```