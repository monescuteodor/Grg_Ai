# API Design Complete Reference


---

# CHAPTER 1: REST API FUNDAMENTALS


## Remarks

An API (Application Programming Interface) is the contract between software systems. REST (Representational State Transfer) is the dominant architectural style for web APIs, created by Roy Fielding in 2000. A well-designed API is intuitive, consistent, versioned, secure, and performant. Bad API design creates years of technical debt and frustration.

Key concepts: **Resources** (nouns, not verbs), **HTTP methods** (GET/POST/PUT/PATCH/DELETE), **Status codes** (2xx/3xx/4xx/5xx), **Versioning** (URL, header, or query), **Pagination** (cursor vs offset), **HATEOAS** (hypermedia links), **Idempotency** (safe to retry), **Rate limiting** (abuse prevention), **Content negotiation** (Accept header).

Used by: every web/mobile app backend. Stripe, GitHub, Twilio, Spotify — all have exemplary REST APIs.

Tools: **OpenAPI/Swagger** (specification), **Postman** (testing), **Insomnia** (alternative), **curl** (CLI), **httpie** (friendlier CLI), **Redocly/Stoplight** (documentation).


## HTTP Methods — When to Use Each

```
METHOD    CRUD       IDEMPOTENT?  SAFE?   BODY?    USE CASE
────────────────────────────────────────────────────────────
GET       Read       Yes          Yes     No       Fetch resource(s)
POST      Create     No           No      Yes      Create new resource
PUT       Replace    Yes          No      Yes      Full update (replace entire resource)
PATCH     Update     No*          No      Yes      Partial update (change specific fields)
DELETE    Delete     Yes          No      No**     Remove resource

HEAD      -          Yes          Yes     No       Like GET but no body (check existence)
OPTIONS   -          Yes          Yes     No       CORS preflight, discover allowed methods

IDEMPOTENT = calling N times has same effect as calling 1 time
SAFE = doesn't modify server state

* PATCH can be made idempotent but isn't inherently
** DELETE can have body but it's unusual

EXAMPLES:
  GET    /users           List all users
  GET    /users/123       Get specific user
  POST   /users           Create new user
  PUT    /users/123       Replace user 123 entirely
  PATCH  /users/123       Update specific fields of user 123
  DELETE /users/123       Delete user 123
```


## URL Design — Resources Are Nouns

```
GOOD (nouns, plural):
  GET    /users
  GET    /users/123
  GET    /users/123/posts
  GET    /users/123/posts/456
  POST   /users
  DELETE /users/123

BAD (verbs in URL):
  GET    /getUsers              ❌ verb
  POST   /createUser            ❌ verb
  GET    /getUserPosts/123      ❌ verb + mixed
  POST   /deleteUser/123        ❌ wrong method + verb

NESTED RESOURCES (relationships):
  GET    /users/123/posts              # Posts by user 123
  GET    /users/123/posts/456          # Post 456 by user 123
  POST   /users/123/posts              # Create post for user 123

  LIMIT NESTING to 2-3 levels max.
  Deeper? Use query params or flat routes:
    GET /posts?userId=123              # Alternative to deep nesting
    GET /posts/456                     # If post ID is globally unique

ACTIONS (non-CRUD operations):
  POST   /users/123/activate           # Action on resource
  POST   /users/123/reset-password
  POST   /orders/456/cancel
  POST   /reports/generate

  Use verbs for ACTIONS only, nouns for resources.

FILTERING, SORTING, SEARCHING:
  GET /users?status=active&role=admin          # Filter
  GET /users?sort=created_at&order=desc        # Sort
  GET /users?search=alice                      # Search
  GET /users?fields=id,name,email              # Sparse fieldsets
  GET /products?minPrice=10&maxPrice=100       # Range

PLURAL vs SINGULAR:
  Always plural: /users, /posts, /orders
  Exception: singleton resources: /users/123/profile (one profile per user)
```


## HTTP Status Codes

```
2xx SUCCESS:
  200 OK                  General success (GET, PUT, PATCH, DELETE)
  201 Created             Resource created (POST). Include Location header.
  202 Accepted            Request accepted, processing async (queued job)
  204 No Content          Success but no body (DELETE, PUT when no response needed)

3xx REDIRECT:
  301 Moved Permanently   Resource URL changed forever
  302 Found               Temporary redirect
  304 Not Modified        Client cache is fresh (ETag/If-None-Match)

4xx CLIENT ERROR:
  400 Bad Request         Malformed request, validation error
  401 Unauthorized        Not authenticated (missing/invalid token)
  403 Forbidden           Authenticated but not authorized for this action
  404 Not Found           Resource doesn't exist
  405 Method Not Allowed  HTTP method not supported on this endpoint
  409 Conflict            State conflict (duplicate entry, version mismatch)
  410 Gone                Resource existed but was permanently deleted
  415 Unsupported Media   Wrong Content-Type header
  422 Unprocessable       Valid syntax but semantic errors (validation)
  429 Too Many Requests   Rate limit exceeded. Include Retry-After header.

5xx SERVER ERROR:
  500 Internal Error      Bug on server (unhandled exception)
  502 Bad Gateway         Upstream server returned invalid response
  503 Service Unavailable Temporarily down (maintenance, overloaded)
  504 Gateway Timeout     Upstream server didn't respond in time

CHOOSING THE RIGHT CODE:
  ✅ Be specific (422 not 400 for validation)
  ✅ 401 vs 403: "Who are you?" vs "You can't do that"
  ✅ Never return 200 with error body
  ✅ 404 for missing resource, not for empty list (200 + [])
```


## Request and Response Design

```json
// POST /users — Create user
// Request:
{
    "name": "Alice",
    "email": "alice@example.com",
    "role": "user"
}

// Response (201 Created):
// Headers:
//   Location: /users/123
//   Content-Type: application/json
{
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com",
    "role": "user",
    "createdAt": "2026-06-10T14:30:00Z",
    "updatedAt": "2026-06-10T14:30:00Z"
}


// PATCH /users/123 — Partial update
// Request (ONLY fields to change):
{
    "name": "Alice Smith"
}

// Response (200 OK): return updated resource
{
    "id": 123,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "role": "user",
    "createdAt": "2026-06-10T14:30:00Z",
    "updatedAt": "2026-06-10T15:00:00Z"
}


// GET /users — List
// Response:
{
    "data": [
        { "id": 1, "name": "Alice", "email": "alice@example.com" },
        { "id": 2, "name": "Bob", "email": "bob@example.com" }
    ],
    "meta": {
        "total": 150,
        "page": 1,
        "perPage": 20,
        "totalPages": 8
    }
}


// DELETE /users/123
// Response: 204 No Content (no body)


// CONVENTIONS:
//   - camelCase for JSON keys (JavaScript convention)
//   - snake_case also acceptable (Python convention) — pick ONE, be consistent
//   - ISO 8601 for dates: "2026-06-10T14:30:00Z"
//   - UTC always (let client convert to local)
//   - Wrap lists in object (for future metadata): { data: [...], meta: {...} }
//   - Return created/updated resource in response
```


---

# CHAPTER 2: ERROR HANDLING


## Error Response Format

```json
// Standard error response
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "The request body contains invalid data.",
        "details": [
            {
                "field": "email",
                "message": "Must be a valid email address.",
                "value": "not-an-email"
            },
            {
                "field": "age",
                "message": "Must be a positive integer.",
                "value": -5
            }
        ],
        "requestId": "req_abc123def456"
    }
}


// Consistent structure across ALL errors:
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "User with id 999 not found.",
        "requestId": "req_789xyz"
    }
}

{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Too many requests. Retry after 30 seconds.",
        "retryAfter": 30,
        "requestId": "req_456abc"
    }
}

{
    "error": {
        "code": "UNAUTHORIZED",
        "message": "Invalid or expired access token.",
        "requestId": "req_321fed"
    }
}
```


## Error Codes (Machine-Readable)

```
Define constants, not just messages:

AUTHENTICATION:
  UNAUTHORIZED           Missing or invalid authentication
  TOKEN_EXPIRED          Auth token has expired
  INVALID_CREDENTIALS    Wrong username/password

AUTHORIZATION:
  FORBIDDEN              Authenticated but not authorized
  INSUFFICIENT_ROLE      Role doesn't have permission

VALIDATION:
  VALIDATION_ERROR       Request body failed validation
  INVALID_FORMAT         Field format is wrong (email, URL)
  MISSING_FIELD          Required field not provided
  VALUE_OUT_OF_RANGE     Number outside allowed range

RESOURCE:
  RESOURCE_NOT_FOUND     Requested resource doesn't exist
  RESOURCE_ALREADY_EXISTS Duplicate (unique constraint)
  RESOURCE_GONE          Permanently deleted

BUSINESS:
  INSUFFICIENT_BALANCE   Not enough funds
  ORDER_ALREADY_SHIPPED  Can't cancel shipped order
  LIMIT_EXCEEDED         Usage limit reached

RATE LIMITING:
  RATE_LIMIT_EXCEEDED    Too many requests

SERVER:
  INTERNAL_ERROR         Unhandled server error
  SERVICE_UNAVAILABLE    Dependency down
  DATABASE_ERROR         Database connection issue (don't expose internals!)

WHY CODES MATTER:
  - Clients can switch/match on codes (not messages!)
  - Messages can change (localization) without breaking clients
  - Codes are documented in API reference
```


### Error Handling Implementation

```python
# FastAPI error handling
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

app = FastAPI()

class ApiError(Exception):
    def __init__(self, code: str, message: str, status: int = 400, details: list = None):
        self.code = code
        self.message = message
        self.status = status
        self.details = details or []
        self.request_id = str(uuid.uuid4())[:12]

class NotFoundError(ApiError):
    def __init__(self, resource: str, id: str):
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=f"{resource} with id '{id}' not found.",
            status=404,
        )

class ValidationError(ApiError):
    def __init__(self, details: list):
        super().__init__(
            code="VALIDATION_ERROR",
            message="The request body contains invalid data.",
            status=422,
            details=details,
        )

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(
        status_code=exc.status,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
                "requestId": exc.request_id,
            }
        },
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    # Log the real error (for debugging)
    logger.exception("Unhandled error", exc_info=exc)
    # Return generic message (don't leak internals!)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred.",
                "requestId": str(uuid.uuid4())[:12],
            }
        },
    )

# Usage
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await db.users.find(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user
```


---

# CHAPTER 3: PAGINATION


## Offset-Based Pagination

```
REQUEST:
  GET /users?page=3&perPage=20

RESPONSE:
{
    "data": [ ... 20 items ... ],
    "meta": {
        "total": 150,
        "page": 3,
        "perPage": 20,
        "totalPages": 8
    }
}

SQL:
  SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;
  -- OFFSET = (page - 1) * perPage = (3-1) * 20 = 40

PROS:
  ✅ Simple to implement
  ✅ Client can jump to any page
  ✅ Total count available

CONS:
  ❌ SLOW for large offsets (DB skips N rows)
  ❌ Inconsistent with inserts/deletes (page shift)
  ❌ OFFSET 1000000 = scan 1M rows then discard

USE WHEN:
  - Small datasets (<10K records)
  - Admin panels where total/page numbers needed
  - User needs to jump to specific page
```


## Cursor-Based Pagination (Recommended)

```
REQUEST:
  GET /users?limit=20
  GET /users?limit=20&after=eyJpZCI6MTIzfQ==

RESPONSE:
{
    "data": [ ... 20 items ... ],
    "meta": {
        "hasNextPage": true,
        "hasPreviousPage": true,
        "startCursor": "eyJpZCI6MTA0fQ==",
        "endCursor": "eyJpZCI6MTIzfQ=="
    }
}

// Cursor = encoded pointer to last item (usually base64 of ID or timestamp)

SQL:
  -- First page
  SELECT * FROM users ORDER BY id LIMIT 20;

  -- Next pages (using cursor = last seen ID)
  SELECT * FROM users WHERE id > 123 ORDER BY id LIMIT 20;
  -- O(log n) with index! No offset scanning.

PROS:
  ✅ Fast at any position (O(log n))
  ✅ Consistent even with inserts/deletes
  ✅ Scales to billions of rows

CONS:
  ❌ Can't jump to page N
  ❌ No total count (expensive for large tables)
  ❌ More complex implementation

USE WHEN:
  - Large datasets
  - Infinite scroll / "load more" UIs
  - Real-time feeds (timeline, notifications)
  - APIs consumed by mobile apps
```


### Cursor Implementation

```python
import base64
import json
from fastapi import Query

def encode_cursor(data: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(cursor).encode())

@app.get("/users")
async def list_users(
    limit: int = Query(20, ge=1, le=100),
    after: str = Query(None),   # Cursor
):
    query = "SELECT * FROM users"
    params = []

    if after:
        cursor_data = decode_cursor(after)
        query += " WHERE id > $1"
        params.append(cursor_data["id"])

    query += " ORDER BY id ASC LIMIT $" + str(len(params) + 1)
    params.append(limit + 1)   # Fetch 1 extra to check hasNextPage

    rows = await db.fetch(query, *params)

    has_next = len(rows) > limit
    items = rows[:limit]

    return {
        "data": items,
        "meta": {
            "hasNextPage": has_next,
            "endCursor": encode_cursor({"id": items[-1]["id"]}) if items else None,
        }
    }


# Multi-column cursor (for sorting by non-unique field)
# Example: sort by created_at (not unique), tiebreak by id

@app.get("/posts")
async def list_posts(limit: int = 20, after: str = None):
    if after:
        cursor = decode_cursor(after)
        query = """
            SELECT * FROM posts
            WHERE (created_at, id) < ($1, $2)
            ORDER BY created_at DESC, id DESC
            LIMIT $3
        """
        rows = await db.fetch(query, cursor["created_at"], cursor["id"], limit + 1)
    else:
        query = "SELECT * FROM posts ORDER BY created_at DESC, id DESC LIMIT $1"
        rows = await db.fetch(query, limit + 1)

    has_next = len(rows) > limit
    items = rows[:limit]

    return {
        "data": items,
        "meta": {
            "hasNextPage": has_next,
            "endCursor": encode_cursor({
                "id": items[-1]["id"],
                "created_at": items[-1]["created_at"].isoformat(),
            }) if items else None,
        }
    }
```


---

# CHAPTER 4: VERSIONING


## Versioning Strategies

```
1. URL VERSIONING (most common, clearest)
   GET /v1/users
   GET /v2/users

   Pros: Obvious, easy to test, cache-friendly
   Cons: Proliferates routes, feels "un-RESTful"
   Used by: Stripe, Twitter, GitHub

2. HEADER VERSIONING
   GET /users
   Accept: application/vnd.myapi.v2+json

   Pros: Clean URLs, content negotiation
   Cons: Hidden, harder to test in browser
   Used by: GitHub (supports both)

3. QUERY PARAMETER
   GET /users?version=2

   Pros: Simple, visible
   Cons: Not standard, caching issues
   Used by: Some Google APIs

RECOMMENDATION: URL versioning (/v1/) for most APIs.
Clear, simple, no surprises.
```


## Backward Compatibility Rules

```
SAFE CHANGES (non-breaking):
  ✅ Add new endpoints
  ✅ Add new optional fields to responses
  ✅ Add new optional query parameters
  ✅ Add new enum values (if client handles unknown)
  ✅ Widen accepted input types

BREAKING CHANGES (require new version):
  ❌ Remove endpoint
  ❌ Remove response field
  ❌ Rename field
  ❌ Change type of field (string → number)
  ❌ Make optional field required
  ❌ Change URL structure
  ❌ Change error format
  ❌ Change authentication method
  ❌ Change pagination format

DEPRECATION PROCESS:
  1. Add v2 endpoint alongside v1
  2. Add Deprecation header to v1: Deprecation: true
  3. Add Sunset header: Sunset: Sat, 01 Jan 2027 00:00:00 GMT
  4. Document migration guide
  5. Email API consumers
  6. Monitor v1 usage (drop when <1% traffic)
  7. Remove v1 after sunset date

  Timeline: minimum 6-12 months for public APIs.
```


---

# CHAPTER 5: AUTHENTICATION AND SECURITY


## API Authentication Methods

```
1. API KEYS (simple, common for server-to-server)
   Header: X-API-Key: sk_live_abc123
   
   Pros: Simple, easy to rotate
   Cons: No user identity, shared secret
   Use for: Server-to-server, CLI tools, public data APIs

2. BEARER TOKEN (JWT)
   Header: Authorization: Bearer eyJhbGci...
   
   Pros: Stateless, contains user info, standard
   Cons: Can't revoke before expiry (without blacklist)
   Use for: User-facing APIs, SPAs, mobile apps

3. OAUTH 2.0 (delegated access)
   Complex flow: authorization code → access token → API calls
   
   Pros: Industry standard, scoped access, third-party
   Cons: Complex implementation
   Use for: Third-party integrations, "Login with Google"

4. BASIC AUTH (username:password)
   Header: Authorization: Basic base64(user:pass)
   
   Pros: Simple
   Cons: Credentials in every request, base64 is NOT encryption
   Use for: Internal tools, ONLY over HTTPS, NEVER for public APIs

HEADER CONVENTION:
  Standard: Authorization: Bearer <token>
  Custom:   X-API-Key: <key>
  NEVER in URL: /users?apiKey=secret (visible in logs, browser history!)
```


## Rate Limiting

```
WHY:
  - Prevent abuse (scraping, brute force)
  - Fair resource distribution
  - Protect backend from overload
  - Monetization (free tier limits)

HEADERS TO RETURN:
  X-RateLimit-Limit: 100            # Max per window
  X-RateLimit-Remaining: 43         # Remaining
  X-RateLimit-Reset: 1700000000     # Unix timestamp when window resets
  Retry-After: 30                   # Seconds to wait (on 429)

LIMITS (typical):
  Public API:    100 req/15min per IP
  Authenticated: 1000 req/15min per user
  Write ops:     30 req/min per user
  Login:         5 req/15min per IP+account

RESPONSE WHEN LIMITED:
  HTTP 429 Too Many Requests
  {
      "error": {
          "code": "RATE_LIMIT_EXCEEDED",
          "message": "Rate limit exceeded. Retry after 30 seconds.",
          "retryAfter": 30
      }
  }
```


### Rate Limiting Implementation

```python
# Token bucket with Redis
import redis
import time

r = redis.Redis()

async def check_rate_limit(
    key: str,
    limit: int = 100,
    window: int = 900   # 15 minutes
) -> tuple[bool, dict]:
    now = int(time.time())
    window_start = now - window

    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)   # Remove expired
    pipe.zcard(key)                                 # Count current
    pipe.zadd(key, {str(now): now})                # Add this request
    pipe.expire(key, window)                        # Auto-cleanup
    _, count, _, _ = pipe.execute()

    allowed = count <= limit
    headers = {
        "X-RateLimit-Limit": str(limit),
        "X-RateLimit-Remaining": str(max(0, limit - count)),
        "X-RateLimit-Reset": str(now + window),
    }

    return allowed, headers


# FastAPI middleware
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"ratelimit:{client_ip}"

        allowed, headers = await check_rate_limit(key)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests."}},
                headers={**headers, "Retry-After": "60"},
            )

        response = await call_next(request)
        for k, v in headers.items():
            response.headers[k] = v
        return response
```


## CORS (Cross-Origin Resource Sharing)

```python
# FastAPI CORS setup
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myapp.com",
        "https://staging.myapp.com",
        "http://localhost:3000",       # Dev only
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Limit"],
    max_age=600,   # Cache preflight for 10 min
)

# NEVER in production:
# allow_origins=["*"]  + allow_credentials=True
# This is a security vulnerability!

# CORS flow:
# 1. Browser sends OPTIONS preflight
# 2. Server responds with allowed origins/methods
# 3. Browser checks response
# 4. If allowed → sends actual request
# 5. If not → blocks in browser (server never sees request)
```


---

# CHAPTER 6: API DOCUMENTATION


## OpenAPI / Swagger Specification

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: User Management API
  description: RESTful API for managing users
  version: 1.0.0
  contact:
    name: API Support
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

security:
  - BearerAuth: []

paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      tags: [Users]
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - name: after
          in: query
          description: Cursor for pagination
          schema:
            type: string
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive, banned]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  meta:
                    $ref: '#/components/schemas/PaginationMeta'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      operationId: createUser
      summary: Create a new user
      tags: [Users]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          headers:
            Location:
              schema:
                type: string
              description: URL of created user
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '422':
          $ref: '#/components/responses/ValidationError'

  /users/{userId}:
    get:
      operationId: getUser
      summary: Get user by ID
      tags: [Users]
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required: [id, name, email, role, createdAt]
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        role:
          type: string
          enum: [admin, user, moderator]
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required: [name, email]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
        role:
          type: string
          enum: [admin, user, moderator]
          default: user

    PaginationMeta:
      type: object
      properties:
        hasNextPage:
          type: boolean
        endCursor:
          type: string
          nullable: true

    ApiError:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            requestId:
              type: string
            details:
              type: array
              items:
                type: object

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ApiError'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ApiError'

    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ApiError'

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```


## Auto-Generated Docs

```python
# FastAPI auto-generates OpenAPI spec and interactive docs!
from fastapi import FastAPI

app = FastAPI(
    title="User Management API",
    description="RESTful API for managing users",
    version="1.0.0",
    docs_url="/docs",         # Swagger UI at /docs
    redoc_url="/redoc",       # ReDoc at /redoc
    openapi_url="/openapi.json",
)

# Every endpoint automatically appears in docs
@app.get("/users", tags=["Users"], summary="List all users")
async def list_users(
    limit: int = Query(20, ge=1, le=100, description="Number of results"),
    after: str = Query(None, description="Cursor for pagination"),
):
    """
    List all users with cursor-based pagination.

    - **limit**: Number of results per page (1-100, default 20)
    - **after**: Cursor from previous response's `meta.endCursor`
    """
    pass

# Visit: http://localhost:8000/docs → interactive API explorer
# Visit: http://localhost:8000/redoc → clean documentation
```


---

# CHAPTER 7: IDEMPOTENCY


## Why Idempotency Matters

```
PROBLEM:
  Client sends POST /orders to create order.
  Network timeout — client doesn't know if it succeeded.
  Client retries POST /orders.
  → TWO orders created! User charged twice!

SOLUTION:
  Client sends a unique idempotency key with the request.
  Server checks: "Did I already process this key?"
  If yes → return cached response (no side effects).
  If no → process normally, cache response.

NATURALLY IDEMPOTENT:
  GET    — always (reading doesn't change state)
  PUT    — replacing with same data = same result
  DELETE — deleting twice = same result (404 on second)

NOT IDEMPOTENT:
  POST   — creating twice = two resources
  PATCH  — incrementing twice = different result
```


### Idempotency Key Implementation

```python
# Client sends: Idempotency-Key: unique-uuid-per-request
import hashlib

IDEMPOTENCY_TTL = 86400   # 24 hours

@app.post("/orders")
async def create_order(
    request: Request,
    body: CreateOrderRequest,
):
    # 1. Get idempotency key
    idempotency_key = request.headers.get("Idempotency-Key")
    if not idempotency_key:
        raise ApiError("MISSING_IDEMPOTENCY_KEY", "Idempotency-Key header required.", 400)

    cache_key = f"idempotency:{idempotency_key}"

    # 2. Check if already processed
    cached = await redis.get(cache_key)
    if cached:
        return JSONResponse(
            status_code=200,
            content=json.loads(cached),
            headers={"X-Idempotent-Replayed": "true"},
        )

    # 3. Process normally
    order = await orders_service.create(body)
    response_data = order.dict()

    # 4. Cache response
    await redis.setex(cache_key, IDEMPOTENCY_TTL, json.dumps(response_data))

    return JSONResponse(status_code=201, content=response_data)


# CLIENT USAGE:
# First attempt:
# POST /orders
# Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
# → 201 Created (order created)

# Retry (same key):
# POST /orders
# Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
# → 200 OK (cached response, no duplicate order)
# X-Idempotent-Replayed: true
```


---

# CHAPTER 8: WEBHOOKS


## Webhook Design

```
WHAT:
  Server-to-server HTTP callbacks.
  "When event X happens, POST to your URL."

INSTEAD OF POLLING:
  Polling:  Client checks every 5s: "Any updates?"  (wasteful)
  Webhook:  Server pushes to client when event occurs (efficient)

DESIGN PRINCIPLES:
  1. POST to subscriber's URL
  2. JSON body with event type + data
  3. HMAC signature for verification
  4. Retry with exponential backoff on failure
  5. Timeout: 5-30 seconds
  6. Expect 2xx response = acknowledged
```


### Webhook Payload

```json
{
    "id": "evt_abc123",
    "type": "order.completed",
    "created": "2026-06-10T14:30:00Z",
    "data": {
        "orderId": "ord_789",
        "userId": "usr_456",
        "total": 99.99,
        "currency": "USD",
        "items": [
            { "productId": "prod_1", "quantity": 2, "price": 49.99 }
        ]
    }
}
```


### Webhook Sender

```python
import hmac
import hashlib
import httpx

class WebhookSender:
    def __init__(self, secret: str):
        self.secret = secret.encode()
        self.client = httpx.AsyncClient(timeout=10.0)

    async def send(self, url: str, event: dict, max_retries: int = 5):
        payload = json.dumps(event)

        # Sign payload
        signature = hmac.new(
            self.secret,
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": f"sha256={signature}",
            "X-Webhook-ID": event["id"],
            "X-Webhook-Timestamp": event["created"],
        }

        # Retry with exponential backoff
        for attempt in range(max_retries):
            try:
                response = await self.client.post(url, content=payload, headers=headers)
                if 200 <= response.status_code < 300:
                    return True
                if response.status_code >= 400 and response.status_code < 500:
                    return False   # Client error, don't retry
            except httpx.RequestError:
                pass

            # Exponential backoff: 1s, 2s, 4s, 8s, 16s
            await asyncio.sleep(2 ** attempt)

        # All retries failed — queue for manual review
        await dead_letter_queue.add(event)
        return False
```


### Webhook Receiver (Verification)

```python
@app.post("/webhooks/orders")
async def receive_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Webhook-Signature", "")

    # Verify signature
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(401, "Invalid signature")

    # Parse and process
    event = json.loads(payload)

    # Idempotency: check if already processed
    if await is_processed(event["id"]):
        return {"status": "already_processed"}

    # Process by type
    match event["type"]:
        case "order.completed":
            await handle_order_completed(event["data"])
        case "order.cancelled":
            await handle_order_cancelled(event["data"])
        case _:
            logger.warning(f"Unknown event type: {event['type']}")

    await mark_processed(event["id"])
    return {"status": "ok"}

    # IMPORTANT: Return 200 quickly!
    # Do heavy processing async (queue).
    # Webhook sender will timeout after 10s.
```


---

# CHAPTER 9: API DESIGN CHECKLIST AND PITFALLS


## Design Checklist

```
NAMING:
  ☐ Resources are nouns, plural (/users not /getUser)
  ☐ Consistent casing (camelCase or snake_case, pick one)
  ☐ No abbreviations (use /organizations not /orgs)
  ☐ Lowercase URLs (/users/123/posts)

HTTP:
  ☐ Correct method per action (GET=read, POST=create, etc.)
  ☐ Correct status codes (specific, not just 200 or 500)
  ☐ Content-Type headers set correctly
  ☐ Accept header respected

RESPONSES:
  ☐ Consistent response envelope ({ data, meta, error })
  ☐ ISO 8601 dates in UTC
  ☐ Include resource ID in creation response
  ☐ Include Location header on 201
  ☐ Empty list = 200 + [], not 404

ERRORS:
  ☐ Consistent error format across all endpoints
  ☐ Machine-readable error codes
  ☐ Human-readable messages
  ☐ Validation errors list affected fields
  ☐ No stack traces in production responses

PAGINATION:
  ☐ Default page size set (e.g., 20)
  ☐ Maximum page size enforced (e.g., 100)
  ☐ Cursor-based for large/real-time data
  ☐ Include hasNextPage in response

SECURITY:
  ☐ HTTPS only (no HTTP)
  ☐ Authentication on all non-public endpoints
  ☐ Authorization checked per resource
  ☐ Rate limiting with proper headers
  ☐ CORS configured correctly
  ☐ Input validated and sanitized
  ☐ No sensitive data in URLs

DOCUMENTATION:
  ☐ OpenAPI spec maintained
  ☐ Interactive docs (Swagger UI)
  ☐ Examples for every endpoint
  ☐ Error codes documented
  ☐ Authentication explained
  ☐ Rate limits documented
  ☐ Changelog maintained

VERSIONING:
  ☐ Version in URL (/v1/)
  ☐ Backward compatibility rules followed
  ☐ Deprecation process defined
```


## Common Pitfalls

```
PITFALL 1: Verbs in URLs
  ❌ GET /getUsers, POST /createUser
  ✅ GET /users, POST /users

PITFALL 2: Returning 200 with error body
  ❌ 200 OK { "success": false, "error": "Not found" }
  ✅ 404 Not Found { "error": { "code": "NOT_FOUND" } }

PITFALL 3: No pagination
  ❌ GET /users returns ALL 1M users
  ✅ GET /users?limit=20&after=cursor

PITFALL 4: Breaking changes without versioning
  ❌ Rename field, remove endpoint, change type
  ✅ New version: /v2/users with migration guide

PITFALL 5: Inconsistent naming
  ❌ Mix of camelCase, snake_case, PascalCase
  ✅ Pick one convention, document it, enforce it

PITFALL 6: Exposing internal IDs/structure
  ❌ /users/1 (auto-increment, enumerable)
  ✅ /users/usr_7f3k9x (UUID or prefixed ID)

PITFALL 7: No rate limiting
  ❌ Unlimited requests → bot scrapes everything
  ✅ Rate limit per IP + per user with 429 response

PITFALL 8: Secrets in URLs
  ❌ GET /users?apiKey=sk_live_secret123
  ✅ Header: Authorization: Bearer sk_live_secret123

PITFALL 9: Not validating input
  ❌ Trust client data, insert directly to DB
  ✅ Validate types, lengths, formats server-side

PITFALL 10: Chatty APIs (N+1 at API level)
  ❌ Client calls GET /users, then GET /users/1/profile for each
  ✅ Include related data: GET /users?include=profile

PITFALL 11: No idempotency for mutations
  ❌ Retry POST /orders creates duplicate
  ✅ Idempotency-Key header prevents duplicates

PITFALL 12: Ignoring Accept/Content-Type
  ❌ Always return JSON regardless of request
  ✅ Check Accept header, return 415 for unsupported types

PITFALL 13: Timestamps without timezone
  ❌ "2026-06-10 14:30:00" (what timezone?)
  ✅ "2026-06-10T14:30:00Z" (UTC, ISO 8601)

PITFALL 14: No request ID for debugging
  ❌ Error occurs, no way to trace
  ✅ Generate X-Request-ID, include in logs and error responses

PITFALL 15: Overly nested resources
  ❌ /companies/1/departments/2/teams/3/members/4/tasks/5
  ✅ /tasks/5 or /tasks?teamId=3
```