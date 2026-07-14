# Monitoring and Observability Complete Reference


---

# CHAPTER 1: THE THREE PILLARS


## Remarks

Observability answers: "What is my system doing and WHY?" Monitoring answers: "Is my system working?" You need both. The three pillars are logs, metrics, and traces. Together they let you detect problems, diagnose root causes, and prevent incidents.


## Logs

```python
# STRUCTURED LOGGING (machine-parseable, searchable)
import logging
import json
from datetime import datetime

logger = logging.getLogger("myapp")

def log_structured(level, event, **kwargs):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "event": event,
        **kwargs,
    }
    logger.log(getattr(logging, level.upper()), json.dumps(entry))

# Usage
log_structured("info", "request_start", 
    method="GET", path="/api/users", request_id="req-abc123")

log_structured("error", "database_timeout",
    query="SELECT * FROM users", duration_ms=5000, request_id="req-abc123")

# Output (JSON lines → parseable by any log tool):
# {"timestamp":"2026-06-10T14:30:00Z","level":"info","event":"request_start","method":"GET","path":"/api/users","request_id":"req-abc123"}

# LOG LEVELS (use correctly!):
# DEBUG:    variable values, flow details (dev only, never in prod)
# INFO:     normal operations (request start/end, job completed)
# WARNING:  unexpected but handled (retry succeeded, fallback used)
# ERROR:    operation failed (request error, timeout)
# CRITICAL: system failure (database down, out of memory)

# WHAT TO LOG:
#   ✅ Request start/end with duration and status
#   ✅ External calls (DB, API) with duration
#   ✅ Errors with full context (user_id, request_id, input)
#   ✅ Business events (order created, payment processed)
#
# WHAT NOT TO LOG:
#   ❌ Passwords, tokens, credit cards, PII
#   ❌ Every iteration of a loop
#   ❌ Success for trivially common operations

# REQUEST ID (correlate across services)
import uuid

class RequestMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, request):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        # Attach to all logs in this request
        log_structured("info", "request_start",
            request_id=request_id, method=request.method, path=request.path)
        
        response = await self.app(request)
        
        log_structured("info", "request_end",
            request_id=request_id, status=response.status_code)
        
        response.headers["X-Request-ID"] = request_id
        return response
```


## Metrics

```python
# RED Method (for services):
# Rate:     requests per second
# Errors:   error rate (%)
# Duration: response time (p50, p95, p99)

# USE Method (for resources):
# Utilization: CPU %, memory %, disk %
# Saturation:  queue length, thread pool usage
# Errors:      hardware errors, OOM events

# Prometheus metrics (Python)
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Counter: only goes UP (total requests, total errors)
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests',
    ['method', 'path', 'status']
)

# Histogram: distribution (response times)
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'path'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Gauge: goes UP and DOWN (current connections, queue size)
ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

# Usage in request handler
async def handle_request(request):
    ACTIVE_CONNECTIONS.inc()
    
    with REQUEST_DURATION.labels(
        method=request.method, path=request.path
    ).time():
        response = await process(request)
    
    REQUEST_COUNT.labels(
        method=request.method, 
        path=request.path,
        status=response.status_code
    ).inc()
    
    ACTIVE_CONNECTIONS.dec()
    return response

# Expose metrics endpoint
start_http_server(9090)  # Prometheus scrapes this
```


## Health Checks

```python
@app.get("/health")
async def health_check():
    checks = {}
    
    # Database
    try:
        await db.execute("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
    
    # Redis
    try:
        await redis.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"
    
    # Disk space
    import shutil
    disk = shutil.disk_usage("/")
    free_pct = disk.free / disk.total * 100
    checks["disk"] = f"ok ({free_pct:.0f}% free)"
    
    # Overall status
    all_ok = all(v == "ok" or v.startswith("ok") for v in checks.values())
    status_code = 200 if all_ok else 503
    
    return JSONResponse({
        "status": "healthy" if all_ok else "degraded",
        "checks": checks,
        "uptime_seconds": time.time() - START_TIME,
    }, status_code=status_code)

# Health endpoint should:
# ✅ Check all critical dependencies
# ✅ Return 200 (healthy) or 503 (unhealthy)
# ✅ Be fast (<1 second)
# ✅ Not require authentication
# ❌ Not do heavy computation
```


---

# CHAPTER 2: ALERTING


## Alert Rules

```yaml
# Prometheus alerting rules example

groups:
  - name: application
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 5% for 5 minutes"

      # Slow responses
      - alert: SlowResponses
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p99 response time above 2 seconds"

      # Service down
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is not responding"
```

```
GOOD ALERTS:
  ✅ Actionable (someone needs to DO something)
  ✅ Urgent (can't wait until morning)
  ✅ Clear (what's wrong, what to check)
  ✅ Low false-positive rate (<5%)

BAD ALERTS:
  ❌ "CPU at 70%" — so what? Is anything broken?
  ❌ "1 error occurred" — 1 error in 1M requests is normal
  ❌ Alerting on every metric — alert fatigue → ignore all alerts

ALERT ON SYMPTOMS, NOT CAUSES:
  ❌ "Database CPU high" — might not affect users
  ✅ "API error rate > 5%" — users ARE affected
  ✅ "Response time p99 > 2s" — users ARE experiencing slowness
```


---

# CHAPTER 3: COMMON PITFALLS

```
PITFALL 1: No request ID correlation
  Can't trace a request across services.
  Fix: generate request ID at entry, pass through all services.

PITFALL 2: Logging sensitive data
  Passwords, tokens, credit cards in logs.
  Fix: scrub sensitive fields before logging.

PITFALL 3: Alert fatigue
  100 alerts per day → team ignores all of them.
  Fix: fewer, better alerts. Alert on symptoms, not causes.

PITFALL 4: No log retention policy
  Logs grow forever → disk full → service crashes.
  Fix: log rotation, max file size, ship to central system with retention.

PITFALL 5: Only monitoring averages
  Average response time 50ms. But p99 = 10 seconds!
  Fix: track percentiles (p50, p95, p99).

PITFALL 6: No baseline
  "Is 200ms response time good or bad?" — don't know without baseline.
  Fix: establish baselines during normal operation, alert on deviations.
```