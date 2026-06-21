# Docker and Kubernetes Advanced Complete Reference


---

# CHAPTER 1: DOCKER ADVANCED


## Remarks

Docker basics (images, containers, Dockerfiles) are covered in `devops_basics.md`. This reference covers advanced patterns for production-grade containerization and orchestration: multi-stage builds, networking internals, storage drivers, security hardening, Kubernetes operators, Helm charts, service mesh, and production debugging.


## Multi-Stage Builds

```dockerfile
# MULTI-STAGE: separate build environment from runtime
# Result: tiny production image (no compilers, no dev deps)

# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false    # Install ALL deps (including devDependencies)
COPY . .
RUN npm run build                # Compile TypeScript, bundle, etc.
RUN npm prune --production       # Remove devDependencies

# Stage 2: Production (only runtime)
FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]

# Result:
#   builder stage: ~500 MB (Node + TypeScript + all deps)
#   production:    ~80 MB (Node + runtime deps + compiled code)


# PYTHON MULTI-STAGE
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --user --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "server.py"]


# GO MULTI-STAGE (extreme: final image has NO OS)
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /server .

FROM scratch                     # EMPTY image — no OS!
COPY --from=builder /server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
ENTRYPOINT ["/server"]
# Final image: ~10-15 MB (just the binary + TLS certs)
```


## Docker Networking

```bash
# NETWORK TYPES:
# bridge (default): isolated network, containers communicate via IP
# host:             container shares host's network (no isolation)
# none:             no networking
# overlay:          multi-host (Swarm/K8s)
# macvlan:          container gets own MAC address on physical network

# Create custom network (recommended over default bridge)
docker network create --driver bridge app-network

# Run containers on same network (can use container names as hostnames!)
docker run -d --name db --network app-network postgres:16
docker run -d --name api --network app-network -e DB_HOST=db myapp
# api can reach postgres at hostname "db" — Docker DNS handles it

# Inspect network
docker network inspect app-network

# Port mapping
docker run -p 8080:3000 myapp     # Host 8080 → container 3000
docker run -p 127.0.0.1:8080:3000 myapp  # Only localhost (more secure)

# DNS resolution between containers
docker exec api ping db           # Resolves "db" to container IP
docker exec api nslookup db       # Shows DNS resolution
```


## Docker Volumes and Storage

```bash
# VOLUME TYPES:
# Named volume:  managed by Docker, persists after container removal
# Bind mount:    map host directory into container
# tmpfs:         in-memory (RAM), no persistence

# Named volume (RECOMMENDED for databases)
docker volume create pgdata
docker run -v pgdata:/var/lib/postgresql/data postgres:16
# Data persists even after container removed
# docker volume inspect pgdata → shows mount point on host

# Bind mount (development — live code reload)
docker run -v $(pwd)/src:/app/src -v $(pwd)/package.json:/app/package.json myapp
# Changes on host instantly reflected in container

# tmpfs (sensitive data that shouldn't persist)
docker run --tmpfs /tmp:size=100m myapp
# /tmp lives in RAM, disappears when container stops

# Read-only filesystem (security)
docker run --read-only --tmpfs /tmp --tmpfs /var/run myapp
# Container can't write anywhere except /tmp and /var/run

# Volume backup
docker run --rm -v pgdata:/source -v $(pwd):/backup alpine \
    tar czf /backup/pgdata-backup.tar.gz -C /source .

# Volume restore
docker run --rm -v pgdata:/target -v $(pwd):/backup alpine \
    tar xzf /backup/pgdata-backup.tar.gz -C /target
```


## Docker Security

```dockerfile
# 1. Non-root user (CRITICAL)
RUN addgroup -S app && adduser -S app -G app
USER app
# Never run as root in production!

# 2. Minimal base image
FROM node:20-alpine             # Alpine: ~5 MB base
# NOT FROM node:20              # Debian: ~350 MB base
# NOT FROM ubuntu:22.04         # Ubuntu: ~77 MB base

# 3. No secrets in image
# BAD:
ENV DB_PASSWORD=secret          # Visible in docker inspect!
COPY .env /app/.env             # Baked into image layers!

# GOOD: pass at runtime
docker run -e DB_PASSWORD=secret myapp
docker run --env-file .env myapp
# Or use Docker secrets / K8s secrets

# 4. Pin versions
FROM node:20.11.1-alpine3.19   # Exact version, reproducible

# 5. Scan for vulnerabilities
# docker scout cves myimage:latest
# trivy image myimage:latest
# snyk container test myimage:latest

# 6. Drop capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp
# Remove ALL Linux capabilities, add back only what's needed

# 7. Read-only root filesystem
docker run --read-only --tmpfs /tmp myapp
```


## Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.9'

services:
  api:
    image: myapp:${VERSION:-latest}
    restart: unless-stopped
    ports:
      - "127.0.0.1:3000:3000"     # Only localhost
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --maxmemory 128mb --maxmemory-policy allkeys-lru
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s

volumes:
  pgdata:
    driver: local

secrets:
  db_password:
    file: ./secrets/db_password.txt
```


---

# CHAPTER 2: KUBERNETES ADVANCED


## K8s Architecture Recap

```
CONTROL PLANE:
  API Server:         entry point for all K8s operations
  etcd:               distributed KV store (cluster state)
  Scheduler:          assigns pods to nodes
  Controller Manager: runs controllers (replication, node, endpoints)

WORKER NODES:
  kubelet:            agent on each node, manages pods
  kube-proxy:         network proxy, service routing
  Container Runtime:  containerd/CRI-O (runs containers)

OBJECTS:
  Pod:                smallest unit (1+ containers)
  Deployment:         manages ReplicaSets (rolling updates)
  Service:            stable network endpoint for pods
  Ingress:            HTTP routing (domain → service)
  ConfigMap:          non-sensitive configuration
  Secret:             sensitive configuration (base64 encoded)
  PersistentVolume:   storage
  StatefulSet:        for stateful apps (databases)
  DaemonSet:          one pod per node (monitoring, logging)
  Job/CronJob:        batch/scheduled tasks
  Namespace:          logical cluster subdivision
```


## Advanced Deployments

```yaml
# Rolling update with canary-like safety
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1           # Create 1 extra pod during update
      maxUnavailable: 0     # Never reduce below desired count
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
        version: v2.1.0
    spec:
      containers:
        - name: api
          image: myapp:2.1.0
          ports:
            - containerPort: 3000
          resources:
            requests:
              cpu: 100m        # 0.1 CPU core guaranteed
              memory: 128Mi    # 128 MB guaranteed
            limits:
              cpu: 500m        # Max 0.5 CPU core
              memory: 512Mi    # Max 512 MB (OOM-killed if exceeded)
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
          env:
            - name: DB_HOST
              valueFrom:
                configMapKeyRef:
                  name: api-config
                  key: db_host
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: db_password
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: api
                topologyKey: kubernetes.io/hostname
      # Anti-affinity: spread pods across different nodes
```


## Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70    # Scale up when CPU > 70%
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60    # Wait 60s before scaling up more
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60             # Add max 2 pods per minute
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5 min before scaling down
      policies:
        - type: Percent
          value: 25
          periodSeconds: 60             # Remove max 25% per minute
```


## Helm Charts

```bash
# Helm = package manager for Kubernetes
# Chart = packaged K8s manifests with templating

# Install
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search
helm search repo postgresql
helm search hub redis

# Install chart
helm install my-db bitnami/postgresql \
    --namespace database \
    --create-namespace \
    --set auth.postgresPassword=secret \
    --set primary.persistence.size=20Gi

# Install with values file
helm install my-db bitnami/postgresql -f values-prod.yaml

# Upgrade
helm upgrade my-db bitnami/postgresql --set image.tag=16.2

# Rollback
helm rollback my-db 1    # Rollback to revision 1

# List releases
helm list -A             # All namespaces

# Uninstall
helm uninstall my-db -n database
```

```yaml
# values-prod.yaml
auth:
  postgresPassword: ""   # Use existingSecret instead
  existingSecret: pg-credentials
primary:
  persistence:
    size: 50Gi
    storageClass: fast-ssd
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 2
      memory: 4Gi
metrics:
  enabled: true
  serviceMonitor:
    enabled: true        # For Prometheus
```


## K8s Debugging

```bash
# Pod status
kubectl get pods -o wide                  # With node and IP
kubectl get pods --show-labels            # With labels
kubectl get pods -w                       # Watch (live updates)

# Pod details (events show WHY pod is failing)
kubectl describe pod POD_NAME

# Logs
kubectl logs POD_NAME                     # Current logs
kubectl logs POD_NAME --previous          # Previous container (after crash)
kubectl logs POD_NAME -f                  # Follow (stream)
kubectl logs -l app=api --all-containers  # All pods with label

# Shell into pod
kubectl exec -it POD_NAME -- /bin/sh
kubectl exec -it POD_NAME -c CONTAINER -- bash   # Specific container

# Run debug container (when pod has no shell)
kubectl debug POD_NAME -it --image=busybox --target=api

# Port forward (access service locally)
kubectl port-forward svc/api 8080:3000    # localhost:8080 → service:3000
kubectl port-forward pod/POD_NAME 5432:5432  # Direct to pod

# Resource usage
kubectl top pods                          # CPU and memory per pod
kubectl top nodes                         # CPU and memory per node

# Events (cluster-wide)
kubectl get events --sort-by=.lastTimestamp

# Common issues:
# CrashLoopBackOff: container crashes → restarts → crashes → ...
#   Check: kubectl logs POD --previous
# ImagePullBackOff: can't pull image
#   Check: image name, registry auth, network
# Pending: no node can schedule pod
#   Check: resources (not enough CPU/memory), node selectors, taints
# OOMKilled: exceeded memory limit
#   Check: increase limits or fix memory leak
```


---

# CHAPTER 3: COMMON PITFALLS


## Docker and Kubernetes Pitfalls

```
PITFALL 1: Running as root in containers
  Fix: USER directive in Dockerfile. Never run as root.

PITFALL 2: Using :latest tag in production
  "latest" can change unexpectedly → different code deployed.
  Fix: pin exact version tags (myapp:2.1.0-sha-abc123).

PITFALL 3: No health checks
  K8s doesn't know if app is healthy → sends traffic to broken pods.
  Fix: readinessProbe (traffic routing) + livenessProbe (restart).

PITFALL 4: No resource limits
  One pod consumes all node resources → other pods starve.
  Fix: always set requests AND limits for CPU and memory.

PITFALL 5: Secrets in environment variables
  Visible via kubectl describe, docker inspect, /proc/environ.
  Fix: mount secrets as files, use external secret managers (Vault).

PITFALL 6: No log rotation
  Container logs fill disk → node dies.
  Fix: Docker json-file driver with max-size. Ship logs to central system.

PITFALL 7: Single replica in production
  Pod crashes → downtime until restart.
  Fix: minimum 2 replicas + PodDisruptionBudget.

PITFALL 8: Not using namespaces
  Everything in default namespace → hard to manage, no isolation.
  Fix: separate namespaces per team/environment.

PITFALL 9: Ignoring pod anti-affinity
  All replicas on same node → node fails → total outage.
  Fix: podAntiAffinity to spread across nodes.

PITFALL 10: No rollback strategy
  Bad deployment → scramble to fix.
  Fix: kubectl rollout undo, Helm rollback, blue-green deployments.

PITFALL 11: Storing state in containers
  Container restarts → data lost.
  Fix: PersistentVolumes for databases, external storage for files.

PITFALL 12: Over-provisioning resources
  Each pod requests 4 CPU + 8 GB → 3 pods need massive node.
  Fix: profile actual usage, set realistic requests.

PITFALL 13: No network policies
  Any pod can talk to any pod → lateral movement risk.
  Fix: NetworkPolicy to restrict pod-to-pod communication.

PITFALL 14: Manual kubectl in production
  kubectl apply from laptop → no audit trail, no review.
  Fix: GitOps (ArgoCD, FluxCD). All changes via git PR.

PITFALL 15: Not monitoring
  Cluster looks fine until it isn't.
  Fix: Prometheus + Grafana for metrics, Loki for logs, alerts on key SLIs.
```