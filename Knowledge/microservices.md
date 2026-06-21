# Microservices Architecture Complete Reference


---

# CHAPTER 1: MICROSERVICES FUNDAMENTALS


## Remarks

Microservices is an architectural style where an application is composed of small, independent services communicating over a network. Each service owns its domain, has its own database, and can be deployed independently. Term popularized by Netflix, Amazon, and Martin Fowler's writings around 2014.

Key principles: **Single Responsibility** (one business capability per service), **Decentralized data** (each service has own DB), **Independent deployment** (no big-bang releases), **Failure isolation** (one service down ≠ system down), **Polyglot** (different languages/tech per service), **Smart endpoints, dumb pipes** (logic in services, not in middleware).

Used by: Netflix (700+ services), Amazon, Uber, Spotify, Airbnb, eBay, LinkedIn.

Tools: **Kubernetes** (orchestration), **Docker** (containers), **Service mesh** (Istio, Linkerd), **API gateways** (Kong, Envoy), **Observability** (Jaeger, Prometheus, ELK stack), **Message brokers** (Kafka, RabbitMQ).


## When to Use Microservices (and When NOT to)

```
USE MICROSERVICES WHEN:
  ✅ >100 developers working on the codebase
  ✅ Different parts have very different scale requirements
  ✅ Need independent deployment cycles
  ✅ Different services need different tech stacks
  ✅ Clear domain boundaries (DDD bounded contexts)
  ✅ Have DevOps maturity (CI/CD, monitoring, IaC)
  ✅ Can afford operational complexity

DO NOT USE MICROSERVICES WHEN:
  ❌ Startup with <10 devs
  ❌ Unclear domain (still figuring out the product)
  ❌ Don't have DevOps team / mature CI/CD
  ❌ Need ACID transactions across many entities
  ❌ Low traffic / simple CRUD app

THE MONOLITH-FIRST APPROACH (Martin Fowler):
  Start with a well-structured monolith.
  Split into services only when seams become obvious.
  Premature microservices = disaster.

REAL TRADE-OFFS:
                    Monolith          Microservices
  Development:      Easy              Hard
  Deployment:       Big bang          Independent
  Scaling:          All together      Per-service
  Tech diversity:   One stack         Per-service
  Observability:    Stdout, logs      Complex (tracing!)
  Failure modes:    Process crash     Cascading network failures
  Team size:        1-50              100+
  Latency:          In-process        Network hops
  Consistency:      ACID transactions Eventual / sagas
```


## Domain-Driven Design Foundation

```
BOUNDED CONTEXT:
  An explicit boundary where a particular model applies.
  Within the boundary, terms have specific meaning.
  
  E-commerce example:
    "Customer" in Sales context     = someone who places orders
    "Customer" in Marketing context = someone who clicks ads
    "Customer" in Support context   = someone with open tickets
  
  Each context = potential microservice boundary.

UBIQUITOUS LANGUAGE:
  Same terms used by developers and domain experts within a context.
  No translation tax.

CONTEXT MAP:
  Diagram showing how bounded contexts interact.
  Patterns: customer-supplier, conformist, anti-corruption layer.

AGGREGATES:
  Cluster of objects treated as one unit.
  Has a "root" - all access goes through it.
  Transaction boundary.
  
  Example: Order is aggregate root, LineItems are inside.
    Don't modify LineItem directly; go through Order.
    Order is responsible for invariants (total = sum of items).

EVENTS:
  Past-tense facts about what happened.
  OrderPlaced, PaymentFailed, ShipmentDelivered.
  Domain events drive integration between services.
```


---

# CHAPTER 2: SERVICE BOUNDARIES AND DESIGN


## Decomposition Strategies

```
DECOMPOSE BY BUSINESS CAPABILITY:
  - Order service
  - Payment service
  - Inventory service
  - User service
  - Notification service
  
  Each owns a business function. Easy for product to understand.

DECOMPOSE BY SUBDOMAIN (DDD):
  Core domains:     Differentiate the business (build in-house)
  Supporting:       Necessary but not differentiating (build or buy)
  Generic:          Off-the-shelf (auth, billing - use SaaS)

DECOMPOSE BY VERB/USE-CASE:
  - CheckoutService (one specific flow)
  - SearchService
  Less common, leads to too many services.

ANTI-PATTERN: Decompose by technical layer
  - "FrontendService", "BackendService", "DatabaseService"
  This is N-tier, not microservices. Defeats the purpose.

SIZE GUIDELINES (rules of thumb):
  - "Two-pizza team" (Amazon): 6-10 people own it
  - Small enough to rewrite in 2-4 weeks
  - One service = one bounded context
  - Big enough to be worth its operational cost
  
"Nano-services" (1 function per service) is an ANTI-PATTERN.
Coordination overhead > benefits.
```


## Service Contracts

```
INPUT (the API):
  - REST API:     GET /orders/{id}
  - gRPC:         orderService.GetOrder(OrderRequest)
  - GraphQL:      query { order(id: 123) { ... } }
  - Events:       Subscribe to "OrderPlaced" topic

OUTPUT (the data):
  Schemas published, versioned, treated as contracts.

VERSIONING:
  URL versioning:    /v1/orders, /v2/orders
  Header versioning: Accept: application/vnd.myapp.v2+json
  Query param:       /orders?version=2

BACKWARD COMPATIBILITY:
  ✅ Add new fields (clients ignore unknown)
  ✅ Add new endpoints
  ✅ Add new optional parameters
  ❌ Remove fields (breaks old clients)
  ❌ Rename fields
  ❌ Change types
  ❌ Make optional → required

DEPRECATION PROCESS:
  1. Add v2 endpoint
  2. Announce deprecation of v1 (with date)
  3. Add deprecation warnings in v1 responses
  4. Monitor v1 usage
  5. Remove v1 after grace period
```


### Example: Service Contract with OpenAPI

```yaml
# orders-api.yaml
openapi: 3.0.0
info:
  title: Orders Service API
  version: 2.1.0
  description: |
    REST API for managing orders.
    Breaking changes will increment major version.

paths:
  /orders:
    post:
      summary: Create a new order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: Order created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          description: Invalid input
        '422':
          description: Business validation failed

components:
  schemas:
    CreateOrderRequest:
      type: object
      required: [userId, items]
      properties:
        userId:
          type: string
          format: uuid
        items:
          type: array
          minItems: 1
          items:
            $ref: '#/components/schemas/OrderItem'

    Order:
      type: object
      required: [id, userId, status, totalAmount, createdAt]
      properties:
        id:
          type: string
          format: uuid
        status:
          type: string
          enum: [pending, paid, shipped, delivered, cancelled]
        totalAmount:
          type: number
          format: decimal
```


---

# CHAPTER 3: INTER-SERVICE COMMUNICATION


## Synchronous vs Asynchronous

```
SYNCHRONOUS (request-response):
  Service A calls Service B and waits for response.
  
  Pros:
    - Simple mental model
    - Immediate feedback
    - Strong consistency for the call
  
  Cons:
    - Tight coupling (B must be up)
    - Cascading failures
    - Latency adds up across hops
    - Doesn't scale well
  
  Protocols: HTTP/REST, gRPC, GraphQL

ASYNCHRONOUS (event-driven):
  Service A publishes event. B consumes when ready.
  
  Pros:
    - Loose coupling
    - Resilient (queue buffers when B is down)
    - Better for spikes
    - Easy to add new subscribers
  
  Cons:
    - Eventual consistency
    - Harder to debug (no direct callstack)
    - Complex error handling
  
  Protocols: Kafka, RabbitMQ, AWS SNS/SQS, NATS

WHEN TO USE WHICH:
  Sync: User-facing actions needing immediate response
        (Get user profile, create payment intent)
  
  Async: Side effects, notifications, audit logs, analytics
         (Send welcome email, update recommendations)
```


## REST Communication Best Practices

```python
# httpx-based async client (Python)
import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class UserServiceClient:
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            headers={"User-Agent": "OrderService/1.0"}
        )

    async def get_user(self, user_id: str) -> Optional[dict]:
        try:
            response = await self._client.get(f"/users/{user_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            logger.warning(f"Timeout fetching user {user_id}")
            raise UpstreamUnavailable("user-service timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} from user-service")
            raise

    async def close(self):
        await self._client.aclose()


# Centralized client factory
class ServiceClients:
    def __init__(self, settings):
        self.users = UserServiceClient(settings.USER_SERVICE_URL)
        self.orders = OrderServiceClient(settings.ORDER_SERVICE_URL)
        self.payments = PaymentServiceClient(settings.PAYMENT_SERVICE_URL)
```


## gRPC Communication

```protobuf
// user.proto
syntax = "proto3";
package user;

service UserService {
    rpc GetUser(GetUserRequest) returns (User);
    rpc CreateUser(CreateUserRequest) returns (User);
    rpc StreamUsers(StreamUsersRequest) returns (stream User);
}

message User {
    string id = 1;
    string name = 2;
    string email = 3;
    int64 created_at = 4;
}

message GetUserRequest {
    string user_id = 1;
}

message CreateUserRequest {
    string name = 1;
    string email = 2;
}
```

```python
# Python gRPC server
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserServiceImpl(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = db.find_user(request.user_id)
        if not user:
            context.abort(grpc.StatusCode.NOT_FOUND, "User not found")
        return user_pb2.User(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=int(user.created_at.timestamp())
        )

    def StreamUsers(self, request, context):
        for user in db.iter_users():
            yield user_pb2.User(id=user.id, name=user.name, ...)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


# Python gRPC client
async def get_user(user_id: str):
    async with grpc.aio.insecure_channel('user-service:50051') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        try:
            response = await stub.GetUser(
                user_pb2.GetUserRequest(user_id=user_id),
                timeout=5.0
            )
            return response
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise
```


## Event-Driven with Kafka

```python
# Producer
from confluent_kafka import Producer
import json

producer = Producer({
    'bootstrap.servers': 'kafka:9092',
    'client.id': 'order-service',
    'acks': 'all',                    # Wait for all replicas
    'enable.idempotence': True,       # Exactly-once semantics
    'compression.type': 'snappy',
})

def publish_order_placed(order: dict):
    event = {
        "event_type": "OrderPlaced",
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "version": 1,
        "data": {
            "order_id": order["id"],
            "user_id": order["user_id"],
            "items": order["items"],
            "total": str(order["total"]),
        }
    }

    producer.produce(
        topic='order-events',
        key=order["id"],               # Same key → same partition (ordering)
        value=json.dumps(event).encode('utf-8'),
        callback=delivery_callback
    )
    producer.flush()

def delivery_callback(err, msg):
    if err:
        logger.error(f"Failed to deliver: {err}")
    else:
        logger.info(f"Delivered to {msg.topic()}:{msg.partition()}:{msg.offset()}")


# Consumer
from confluent_kafka import Consumer, KafkaError

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'notification-service',     # Consumer group
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,            # Manual commit for safety
    'max.poll.interval.ms': 300000,
})

consumer.subscribe(['order-events'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            logger.error(f"Consumer error: {msg.error()}")
            continue

        try:
            event = json.loads(msg.value().decode('utf-8'))

            # Idempotent handling
            if not already_processed(event["event_id"]):
                process_event(event)
                mark_processed(event["event_id"])

            consumer.commit(msg)         # Commit after success
        except Exception as e:
            logger.error(f"Failed to process: {e}")
            # Don't commit - will be redelivered
finally:
    consumer.close()
```


---

# CHAPTER 4: SERVICE DISCOVERY


## Why Service Discovery?

```
In a monolith: services call each other by function name.
In microservices: services run on different IPs that change over time.

PROBLEM: How does Service A find Service B's current address?

OPTIONS:

1. DNS-based:
   Configure DNS records.
   Service B = "user-service.internal" → DNS resolves to IP.
   Kubernetes uses this (CoreDNS).

2. Server-side discovery (load balancer):
   Service A → Load Balancer → Service B instances
   Pros: Service A doesn't know about discovery
   Cons: LB is extra hop

3. Client-side discovery (service registry):
   Service A queries registry, gets list of B instances, picks one.
   Tools: Consul, Eureka, Zookeeper
   Pros: No extra hop
   Cons: Each client must know discovery logic

4. Service mesh (sidecar):
   Sidecar proxy handles discovery transparently.
   Tools: Istio, Linkerd, Consul Connect
   Pros: Apps don't need any discovery code
   Cons: Operational complexity
```


## Kubernetes Service Discovery

```yaml
# user-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: app
        image: myapp/user-service:1.2.0
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 5
---
# Service - stable DNS name
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP   # Internal only
```

Now any pod can reach: `http://user-service` or `http://user-service.default.svc.cluster.local`

```python
# In another service - no IP, just the DNS name
async def get_user(user_id):
    async with httpx.AsyncClient() as client:
        return await client.get(f"http://user-service/users/{user_id}")
```


## Health Checks

```python
# FastAPI health endpoints
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

# Liveness - "is the process alive?"
@app.get("/health")
async def liveness():
    return {"status": "alive"}


# Readiness - "ready to serve traffic?"
@app.get("/ready")
async def readiness():
    checks = {
        "database": await check_database(),
        "redis": await check_redis(),
        "upstream_user_service": await check_upstream(),
    }

    if all(c["healthy"] for c in checks.values()):
        return {"status": "ready", "checks": checks}
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "checks": checks}
        )


async def check_database():
    try:
        await db.execute("SELECT 1")
        return {"healthy": True}
    except Exception as e:
        return {"healthy": False, "error": str(e)}


async def check_redis():
    try:
        await redis.ping()
        return {"healthy": True}
    except Exception as e:
        return {"healthy": False, "error": str(e)}
```

K8s uses these:
- **Liveness fails** → kill and restart pod
- **Readiness fails** → remove from load balancer (keep running)


---

# CHAPTER 5: DATA MANAGEMENT


## Database per Service

```
PRINCIPLE: Each service owns its data.
Other services NEVER access another service's DB directly.

Pros:
  - Schema changes don't break other services
  - Each service picks best DB for its needs
  - Failure isolation
  - Independent scaling

Cons:
  - No joins across services (must call APIs)
  - Data duplication (denormalization)
  - Distributed transactions complex
  - Reporting/analytics harder (need separate analytics DB)

VIOLATIONS THAT KILL MICROSERVICES:
  ❌ Shared database between services
  ❌ Services reaching into each other's tables
  ❌ Foreign keys across service boundaries

Better:
  ✅ Each service has its DB
  ✅ Inter-service communication via API or events
  ✅ Data warehouse / lake for analytics (ETL from each service)
```


## Distributed Transactions and Saga Pattern

```
PROBLEM:
  Multiple services need to update their DBs together.
  Example: Order requires reserving inventory + charging payment.
  If one fails, the others should undo.

WHY NOT 2-PHASE COMMIT (2PC)?
  - Synchronous blocking
  - Single coordinator = SPOF
  - Slow, doesn't scale
  - Most NoSQL DBs don't support it

SAGA PATTERN:
  Sequence of local transactions; each has a compensating action.
  If step N fails, run compensations for steps 1 to N-1.

  CHOREOGRAPHY (event-based, no central coordinator):
    Service A: writes → publishes event
    Service B: subscribes → reacts → writes → publishes event
    Service C: subscribes → reacts → ...
    
    On failure: publishes failure event → others run compensations.
    
    Pros: Decentralized, simple
    Cons: Hard to understand flow, hard to debug
    Use when: <5 services involved

  ORCHESTRATION (central coordinator):
    Orchestrator calls services in order.
    On failure, orchestrator calls compensations in reverse.
    
    Pros: Easy to understand and debug, easier monitoring
    Cons: Coordinator can become bottleneck/SPOF
    Use when: Complex flows, many steps

EXAMPLE - Order Saga (Orchestration):
  Steps:
    1. CreateOrder (Order service)
    2. ReservePayment (Payment service)
    3. ReserveInventory (Inventory service)
    4. ConfirmOrder (Order service)

  Compensations (reverse order):
    1. CancelOrder
    2. RefundPayment
    3. ReleaseInventory
    4. (nothing for ConfirmOrder)
```


### Saga Orchestrator Implementation

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Awaitable

class SagaStepStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    COMPENSATED = "compensated"

@dataclass
class SagaStep:
    name: str
    action: Callable[..., Awaitable]
    compensation: Callable[..., Awaitable]
    status: SagaStepStatus = SagaStepStatus.PENDING
    result: any = None


class OrderSagaOrchestrator:
    def __init__(self, services):
        self.services = services

    async def execute(self, order_request: dict):
        steps = [
            SagaStep(
                name="create_order",
                action=lambda: self.services.order.create(order_request),
                compensation=lambda r: self.services.order.cancel(r["order_id"])
            ),
            SagaStep(
                name="reserve_payment",
                action=lambda: self.services.payment.reserve(
                    order_request["user_id"], order_request["total"]
                ),
                compensation=lambda r: self.services.payment.refund(r["payment_id"])
            ),
            SagaStep(
                name="reserve_inventory",
                action=lambda: self.services.inventory.reserve(order_request["items"]),
                compensation=lambda r: self.services.inventory.release(r["reservation_id"])
            ),
            SagaStep(
                name="confirm_order",
                action=lambda: self.services.order.confirm(steps[0].result["order_id"]),
                compensation=lambda r: None   # No compensation needed
            ),
        ]

        completed = []
        try:
            for step in steps:
                step.result = await step.action()
                step.status = SagaStepStatus.SUCCESS
                completed.append(step)
                logger.info(f"Saga step {step.name} succeeded")

            return {"status": "success", "order_id": steps[0].result["order_id"]}

        except Exception as e:
            logger.error(f"Saga failed at step {step.name}: {e}")
            await self._compensate(completed)
            return {"status": "failed", "reason": str(e)}

    async def _compensate(self, completed_steps: list[SagaStep]):
        # Run compensations in REVERSE order
        for step in reversed(completed_steps):
            try:
                await step.compensation(step.result)
                step.status = SagaStepStatus.COMPENSATED
                logger.info(f"Compensated step {step.name}")
            except Exception as e:
                logger.error(f"FAILED to compensate {step.name}: {e}")
                # Critical: Manual intervention needed.
                # In production: persist to dead-letter / alert ops
```


## Eventual Consistency Patterns

```
OUTBOX PATTERN:
  Problem: How to atomically save state AND publish event?
  If you save to DB then publish to Kafka:
    - DB succeeds, Kafka fails → state changed but no event
    - Kafka succeeds, DB fails → event for non-existent state

  Solution:
    1. In same DB transaction: write business data + write event to "outbox" table.
    2. Separate process polls outbox table and publishes to Kafka.
    3. After publish, delete (or mark) outbox row.

  Guarantees at-least-once delivery, atomicity preserved.
```

```python
# Outbox pattern implementation
async def create_order(user_id, items):
    async with db.transaction():
        # 1. Write business data
        order = await db.execute(
            "INSERT INTO orders (user_id, total) VALUES ($1, $2) RETURNING *",
            user_id, sum(i.price for i in items)
        )

        # 2. Write event to outbox (SAME TRANSACTION)
        event = {
            "event_type": "OrderPlaced",
            "data": {"order_id": order.id, "user_id": user_id}
        }
        await db.execute(
            "INSERT INTO outbox (event_type, payload, created_at) VALUES ($1, $2, NOW())",
            "OrderPlaced", json.dumps(event)
        )

    # Transaction committed atomically
    return order


# Outbox poller (separate process)
async def poll_outbox():
    while True:
        rows = await db.fetch(
            "SELECT * FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 100"
        )

        for row in rows:
            try:
                await kafka.publish(row["event_type"], json.loads(row["payload"]))
                await db.execute(
                    "UPDATE outbox SET published_at = NOW() WHERE id = $1",
                    row["id"]
                )
            except Exception as e:
                logger.error(f"Failed to publish {row['id']}: {e}")
                # Will retry next poll

        await asyncio.sleep(1)
```


## CQRS (Command Query Responsibility Segregation)

```
PRINCIPLE: Use different models for writes (commands) and reads (queries).

WHY?
  Read patterns ≠ Write patterns.
  Reads: fast, often complex joins/aggregations, denormalized
  Writes: validation, business rules, normalized for consistency
  
  CQRS lets each optimize independently.

ARCHITECTURE:
  
  Commands ──► Command Handler ──► Write Model (normalized DB)
                                          │
                                          ▼
                                    Publish Events
                                          │
                                          ▼
                                 Update Read Models
                                  (denormalized, optimized for queries)
  
  Queries ──► Read Model (could be Elasticsearch, denormalized SQL, etc.)

USE WHEN:
  - Read/write ratio is very skewed (e.g. 100:1)
  - Complex business rules on writes
  - Need different consistency for reads vs writes
  - Reports/analytics use cases

EVENTUAL CONSISTENCY:
  Read model lags behind write model by milliseconds.
  Usually OK; problematic for "read your writes" scenarios.

DON'T USE WHEN:
  - Simple CRUD
  - Read/write patterns similar
  - Strong consistency required everywhere
```


---

# CHAPTER 6: OBSERVABILITY


## The Three Pillars

```
LOGS:        What happened (events, errors)
METRICS:     How much, how often, how fast (numbers)
TRACES:      Why slow / where failed (request flow through services)

You need ALL THREE for production microservices.
```


## Structured Logging

```python
import structlog
import logging
import sys

# Configure
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

# Use
async def create_order(user_id, items):
    log = logger.bind(user_id=user_id, item_count=len(items))
    log.info("Creating order")

    try:
        order = await orders_repo.create(user_id, items)
        log.info("Order created", order_id=order.id, total=order.total)
        return order
    except InsufficientStockError as e:
        log.warning("Insufficient stock", item_id=e.item_id)
        raise
    except Exception as e:
        log.exception("Order creation failed")
        raise

# Output (JSON):
# {"event": "Creating order", "user_id": "u123", "item_count": 3, 
#  "timestamp": "2026-06-10T10:30:00Z", "level": "info"}
```

**JSON logs are critical** — they can be parsed and indexed by log aggregators (ELK, Loki, Datadog).


## Metrics with Prometheus

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response

app = FastAPI()

# Counter - monotonically increasing
orders_created = Counter(
    'orders_created_total',
    'Total orders created',
    ['status']     # Labels for dimensions
)

# Histogram - distribution of values (for latency)
order_processing_seconds = Histogram(
    'order_processing_seconds',
    'Time spent processing orders',
    buckets=[0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

# Gauge - value that can go up and down
active_users = Gauge('active_users', 'Currently active users')


@app.post("/orders")
async def create_order(request: CreateOrderRequest):
    with order_processing_seconds.time():
        try:
            order = await orders_repo.create(request.user_id, request.items)
            orders_created.labels(status='success').inc()
            return order
        except Exception as e:
            orders_created.labels(status='error').inc()
            raise


# Expose metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

**Prometheus scrapes `/metrics` every 15s** and stores time series. Grafana visualizes.

Standard metrics every service should have:
- Request count (per endpoint, per status code)
- Request latency (p50, p95, p99)
- Error rate
- Resource usage (CPU, memory)
- Custom business metrics (orders/sec, revenue/min, etc.)


## Distributed Tracing with OpenTelemetry

```python
# pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp \
#             opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-httpx

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

# Setup
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="jaeger:4317"))
)

# Instrument frameworks (automatic)
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()

# Manual spans for business logic
tracer = trace.get_tracer(__name__)

@app.post("/orders")
async def create_order(request: CreateOrderRequest):
    with tracer.start_as_current_span("create_order") as span:
        span.set_attribute("user_id", request.user_id)
        span.set_attribute("item_count", len(request.items))

        with tracer.start_as_current_span("validate"):
            await validate_request(request)

        with tracer.start_as_current_span("check_inventory"):
            available = await inventory_client.check(request.items)
            span.set_attribute("inventory_available", available)

        with tracer.start_as_current_span("create_db"):
            order = await orders_repo.create(request)
            span.set_attribute("order_id", order.id)

        return order
```

Result in Jaeger UI: full timeline showing every service touched by a request, with timings.

**This is irreplaceable for debugging "why is this request slow?"** in microservices.


---

# CHAPTER 7: DEPLOYMENT


## Docker Containers

```dockerfile
# Multi-stage build for smaller image
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.12-slim

# Non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

COPY --chown=appuser:appuser . .

USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# Use exec form to ensure signals propagate
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
```


## Kubernetes Deployment

```yaml
# user-service.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  namespace: prod
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1           # 1 extra during update
      maxUnavailable: 0     # Never go below desired
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
        version: v2-3-1
    spec:
      containers:
      - name: app
        image: myapp/user-service:2.3.1
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-service-secrets
              key: database_url
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            cpu: 100m         # Reserved
            memory: 256Mi
          limits:
            cpu: 500m         # Max
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 5
        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["sh", "-c", "sleep 15"]   # Drain time
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 80
    targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: user-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: user-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```


## Deployment Strategies

```
ROLLING UPDATE (default in K8s):
  Replace pods one (or few) at a time.
  Old + new run simultaneously briefly.
  
  Pros: No downtime, simple
  Cons: Both versions live - schema compat needed

BLUE-GREEN:
  Run TWO complete environments (blue=v1, green=v2).
  Switch traffic from blue to green at once.
  
  Pros: Instant rollback (switch back), test green before traffic
  Cons: Doubles resources during transition

CANARY:
  Deploy v2 to a small fraction of users (5%).
  Monitor metrics. If good, gradually increase (10%, 25%, 50%, 100%).
  
  Pros: Reduce blast radius of bad deployments
  Cons: Complex routing, need good observability

FEATURE FLAGS:
  Deploy code with feature OFF.
  Enable for users gradually via config.
  
  Pros: Decouple deploy from release; A/B testing
  Cons: Code complexity, dead code accumulates
  Tools: LaunchDarkly, Unleash, Flagsmith
```


## Common Pitfalls

```
PITFALL 1: Distributed monolith
  Services so tightly coupled they MUST deploy together.
  → Define clear contracts, version APIs, use events.

PITFALL 2: Premature decomposition
  Splitting too early before understanding domain.
  → Start monolith, split when seams clear.

PITFALL 3: Shared database
  Multiple services hitting the same tables.
  → Each service owns its DB. Use API or events to communicate.

PITFALL 4: Synchronous service chains
  A → B → C → D → E. Each adds latency. Any failure cascades.
  → Use async events where possible.

PITFALL 5: Ignoring data consistency
  Just hoping eventual consistency will work out.
  → Design with sagas, outbox pattern, idempotency.

PITFALL 6: No observability
  Can't tell why something is slow or broken.
  → Logs + metrics + traces from day 1.

PITFALL 7: Ignoring idempotency
  Network retry causes duplicate orders / charges.
  → All operations idempotent (use idempotency keys).

PITFALL 8: Too small services ("nano-services")
  100 services for what should be 10. Coordination overhead exceeds benefit.
  → Bigger services unless clear reason to split.

PITFALL 9: No retry/timeout strategy
  Service calls hang forever or retry storms.
  → Timeouts, exponential backoff, circuit breakers.

PITFALL 10: Lack of testing
  Unit tests pass, but integration breaks.
  → Contract testing (Pact), integration tests, end-to-end smoke tests.

PITFALL 11: Logging PII / secrets
  Logs include passwords, tokens, credit cards.
  → Sanitize at logger level. Never log secrets.

PITFALL 12: Different time zones
  Some services log in UTC, others local time.
  → Always UTC in logs and stored timestamps. Convert at display.
```