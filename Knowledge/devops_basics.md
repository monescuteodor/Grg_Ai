# DevOps Basics Complete Reference


---

# CHAPTER 1: LINUX FOR DEVELOPERS


## Remarks

DevOps (Development + Operations) is the practice of unifying software development and operations, automating everything from code commit to production deployment. Originated around 2008-2010 with the rise of cloud computing. Now standard practice at every modern software company.

Key concepts: **Infrastructure as Code** (IaC), **CI/CD** (Continuous Integration/Deployment), **Containers** (Docker, OCI), **Orchestration** (Kubernetes), **Observability** (logs, metrics, traces), **GitOps** (Git as source of truth), **Site Reliability Engineering** (SRE), **Immutable infrastructure** (replace, don't patch).

Used in: every production deployment. From startups to FAANG, DevOps practices determine how fast and reliably software ships.

Tools: **Linux** (the OS of servers), **Git** (version control), **Docker** (containers), **Kubernetes** (orchestration), **Terraform** (IaC), **Ansible** (config management), **GitHub Actions / GitLab CI / Jenkins** (CI/CD), **Prometheus + Grafana** (monitoring), **AWS/GCP/Azure** (clouds).


## Essential Linux Commands

```bash
# File system navigation
pwd                        # Print working directory
ls -la                     # List with details, hidden files
cd /var/log                # Change directory
cd -                       # Previous directory
cd ~                       # Home

# File operations
cp file.txt backup.txt     # Copy
cp -r dir1/ dir2/          # Copy directory recursively
mv old.txt new.txt         # Move/rename
rm file.txt                # Delete
rm -rf dir/                # Delete recursively (DANGEROUS!)
touch file.txt             # Create empty / update timestamp
mkdir -p path/to/dir       # Create dir tree

# Viewing files
cat file.txt               # Print entire file
less file.txt              # Pager (q to quit, / to search)
head -n 20 file.txt        # First 20 lines
tail -n 50 file.txt        # Last 50 lines
tail -f /var/log/app.log   # Follow (live updates) — KEY for debugging
wc -l file.txt             # Line count
file unknown.bin           # Identify file type

# Find files
find /var/log -name "*.log"
find . -mtime -7           # Modified in last 7 days
find . -size +100M         # Bigger than 100 MB
find . -type f -delete     # DANGEROUS — delete found files

# Search inside files
grep "ERROR" app.log                # Find lines with ERROR
grep -r "TODO" src/                 # Recursive
grep -i "warning" log.txt           # Case-insensitive
grep -v "DEBUG" log.txt             # Exclude DEBUG lines
grep -E "ERROR|FATAL" log.txt       # Regex (multiple patterns)
grep -B 2 -A 5 "Exception" log.txt  # 2 lines before, 5 after
grep -c "404" access.log            # Count matches

# Permissions
chmod 755 script.sh        # rwxr-xr-x (owner: rwx, others: r-x)
chmod +x script.sh         # Add execute
chmod -R 644 docs/         # Recursive
chown user:group file      # Change owner

# Permission cheatsheet:
#   4 = read, 2 = write, 1 = execute
#   755 = rwx r-x r-x (typical for executables)
#   644 = rw- r-- r-- (typical for files)
#   600 = rw- --- --- (private, e.g. SSH keys)
#   700 = rwx --- --- (private executable)

# Process management
ps aux                     # All processes (BSD style)
ps -ef | grep node         # Find Node processes
top                        # Live process monitor
htop                       # Better top (install separately)
kill 1234                  # Send SIGTERM to PID 1234
kill -9 1234               # SIGKILL (force, last resort)
killall node               # Kill all by name

# Disk usage
df -h                      # Disk space per partition (human readable)
du -sh /var/log/*          # Size of each item in dir
du -sh * | sort -h         # Sorted by size
ncdu                       # Interactive (install separately)

# Memory
free -h                    # Total/used/free memory
cat /proc/meminfo          # Detailed

# Networking
ip addr                    # Network interfaces (newer)
ifconfig                   # Old equivalent
ss -tlnp                   # Listening TCP sockets with PIDs
netstat -tulpn             # Old equivalent
curl https://example.com   # HTTP request
curl -I https://x.com      # HEAD only (headers)
wget url                   # Download
ping example.com           # Test reachability
traceroute google.com      # Path to host
dig example.com            # DNS lookup
nslookup example.com       # Alternative DNS

# Archive / Compression
tar -czf archive.tar.gz dir/    # Create gzipped tar
tar -xzf archive.tar.gz         # Extract
tar -tzf archive.tar.gz         # List contents
zip -r archive.zip dir/         # Zip
unzip archive.zip               # Unzip

# Text processing
sed -i 's/foo/bar/g' file.txt        # Replace in place
awk '{print $1, $3}' data.txt        # Print fields 1 and 3
cut -d',' -f2 data.csv               # Field 2 from CSV
sort file.txt | uniq -c              # Count unique lines
sort -rn file.txt                    # Numeric reverse sort

# Pipes and redirects
cmd1 | cmd2                # Pipe output of cmd1 → input of cmd2
cmd > file.txt             # Redirect stdout (overwrite)
cmd >> file.txt            # Append
cmd 2> errors.txt          # Redirect stderr
cmd > out.log 2>&1         # Combine stdout + stderr
cmd1 && cmd2               # Run cmd2 only if cmd1 succeeded
cmd1 || cmd2               # Run cmd2 only if cmd1 failed
cmd1 ; cmd2                # Run both regardless
```


## Shell Scripting Essentials

```bash
#!/usr/bin/env bash
set -euo pipefail   # CRITICAL: fail fast, undefined var = error, pipe failure = error

# Variables
NAME="Alice"
echo "Hello, $NAME"
echo "Total: ${NAME}123"

# Command substitution
DATE=$(date +%Y-%m-%d)
FILES=$(ls *.txt | wc -l)

# Conditionals
if [[ -f "config.json" ]]; then
    echo "Config exists"
elif [[ "$ENV" == "prod" ]]; then
    echo "Production"
else
    echo "Other"
fi

# File tests:
#   -f file exists and is regular file
#   -d is directory
#   -e exists
#   -r readable, -w writable, -x executable
#   -s file exists and is not empty

# Loops
for FILE in *.log; do
    echo "Processing $FILE"
    gzip "$FILE"
done

for i in {1..10}; do
    echo "Iteration $i"
done

while read -r LINE; do
    echo "Line: $LINE"
done < input.txt

# Functions
function backup() {
    local SOURCE=$1
    local DEST=$2
    cp -r "$SOURCE" "$DEST"
    echo "Backed up $SOURCE → $DEST"
}

backup /etc/nginx /backup/nginx

# Error handling
deploy() {
    cp app.js /opt/app/ || { echo "Copy failed"; return 1; }
    systemctl restart app || { echo "Restart failed"; return 1; }
}

if ! deploy; then
    echo "Deployment failed, rolling back"
    rollback
    exit 1
fi

# Arguments
echo "Script: $0"
echo "First arg: $1"
echo "All args: $@"
echo "Count: $#"

# Read environment variables with defaults
PORT="${PORT:-3000}"
ENV="${NODE_ENV:-development}"
```


## SSH and Remote Servers

```bash
# Connect
ssh user@server.com
ssh -p 2222 user@server.com           # Custom port
ssh -i ~/.ssh/key.pem ec2-user@host   # Specific key

# Run command on remote
ssh user@server "ls -la /var/log"

# Copy files
scp file.txt user@server:/path/       # Local → remote
scp user@server:/path/file.txt .      # Remote → local
scp -r dir/ user@server:/path/        # Directory

# Better: rsync (resume, delta transfer)
rsync -avz dir/ user@server:/path/    # Sync local → remote
rsync -avz --delete dir/ user@server:/path/   # Delete files not in source

# SSH config (~/.ssh/config) — define shortcuts
# Then: ssh prod (instead of full command)
Host prod
    HostName prod.example.com
    User deploy
    Port 22
    IdentityFile ~/.ssh/prod_key

Host bastion
    HostName 1.2.3.4
    User admin

# Tunneling (forward local port to remote service)
ssh -L 5432:db.internal:5432 user@bastion
# Now localhost:5432 → bastion → db.internal:5432

# Generate SSH key pair
ssh-keygen -t ed25519 -C "your_email@example.com"
# Adds: ~/.ssh/id_ed25519 (private) and id_ed25519.pub (public)

# Copy public key to server
ssh-copy-id user@server.com
# Or manually: append .pub content to ~/.ssh/authorized_keys on server
```


---

# CHAPTER 2: DOCKER


## Container Concepts

```
WHAT'S A CONTAINER?
  Process running in isolation with its own:
    - Filesystem view (chroot-like)
    - Network namespace
    - Process namespace (own PID 1)
    - Resource limits (CPU, RAM via cgroups)
  
  Not a VM! Shares the host kernel.

DOCKER WORKFLOW:
  Dockerfile → docker build → Image → docker run → Container
                                ↓
                          push to registry
                                ↓
                          pull from registry on other machines

IMAGE vs CONTAINER:
  Image: read-only template (like a class)
  Container: running instance of an image (like an object)
  Multiple containers can run from same image.

LAYERS:
  Image = stack of layers (each Dockerfile instruction = layer)
  Layers are CACHED — change late, cache early layers
  Stored as content-addressable hashes
```


## Dockerfile

```dockerfile
# Use a specific version, not 'latest' (reproducibility)
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files FIRST (cached if unchanged)
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy app code (changes often = invalidates cache from this point)
COPY . .

# Build (if needed)
RUN npm run build

# Non-root user for security
RUN addgroup -S app && adduser -S app -G app
USER app

# Expose port (documentation only — doesn't actually open)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Entry point
CMD ["node", "dist/server.js"]
```

**Best practices:**
- Multi-stage builds for smaller images
- `.dockerignore` to exclude node_modules, .git, secrets
- Pin versions (`FROM node:20.5.1-alpine`, not `:latest`)
- Order matters: changes-rarely first, changes-often last
- One process per container
- Non-root user


## Multi-Stage Builds

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (small, only what's needed)
FROM node:20-alpine
WORKDIR /app

# Copy only production dependencies and build output
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY --from=builder /build/dist ./dist

USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]

# Result: production image MUCH smaller (no dev deps, no source files)
```


## Docker Commands

```bash
# Build
docker build -t myapp:1.0 .
docker build -t myapp:1.0 -f Dockerfile.prod .   # Specific Dockerfile

# Tag
docker tag myapp:1.0 registry.example.com/myapp:1.0

# Push to registry
docker push registry.example.com/myapp:1.0

# Pull
docker pull nginx:latest

# Run
docker run myapp:1.0
docker run -d --name web -p 8080:3000 myapp:1.0   # Detached, port mapping
docker run -e DB_URL=postgres://... myapp:1.0     # Env var
docker run -v /host/data:/data myapp:1.0          # Volume mount
docker run --rm myapp:1.0                          # Auto-remove on exit
docker run -it ubuntu bash                         # Interactive terminal

# List
docker ps                       # Running containers
docker ps -a                    # All containers (incl. stopped)
docker images                   # All images
docker volume ls                # Volumes
docker network ls               # Networks

# Inspect
docker logs <container>
docker logs -f <container>      # Follow logs
docker logs --tail 100 <container>
docker exec -it <container> bash   # Shell inside container
docker inspect <container>      # Full JSON details
docker stats                    # Live resource usage

# Stop / start / remove
docker stop <container>
docker start <container>
docker restart <container>
docker rm <container>           # Remove (must be stopped)
docker rm -f <container>        # Force remove (kill + remove)
docker rmi <image>              # Remove image

# Cleanup
docker system prune             # Remove stopped containers, unused images
docker system prune -a          # More aggressive (all unused images)
docker volume prune             # Remove unused volumes

# Disk usage
docker system df                # Show docker disk usage
```


## Docker Compose

```yaml
# docker-compose.yml
version: '3.9'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://postgres:password@db:5432/myapp
      REDIS_URL: redis://cache:6379
      NODE_ENV: production
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - cache_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - web
    restart: unless-stopped

volumes:
  db_data:
  cache_data:

networks:
  default:
    driver: bridge
```

```bash
# Compose commands
docker compose up                    # Start all
docker compose up -d                 # Detached
docker compose down                  # Stop and remove
docker compose down -v               # Also remove volumes (DELETE DATA)
docker compose logs -f               # Follow logs from all
docker compose logs -f web           # Specific service
docker compose ps                    # Service status
docker compose exec web bash         # Shell in service
docker compose build                 # Rebuild images
docker compose up --build            # Rebuild and start
docker compose restart web           # Restart one service
```


---

# CHAPTER 3: KUBERNETES BASICS


## Core Objects

```
POD:
  Smallest deployable unit. Wraps one or more tightly-coupled containers.
  Containers in same pod share: network, storage volumes, lifecycle.
  Usually: 1 pod = 1 main container + maybe a sidecar.

DEPLOYMENT:
  Manages replica sets (groups of identical pods).
  Handles rolling updates, scaling, rollback.

SERVICE:
  Stable network endpoint for a set of pods.
  Pods come and go (different IPs); service IP is stable.
  Types: ClusterIP (internal), NodePort, LoadBalancer (cloud), Ingress.

CONFIGMAP:
  Non-secret configuration data (env vars, config files).

SECRET:
  Sensitive data (passwords, API keys, certs).
  Base64-encoded (NOT encrypted by default — enable encryption at rest).

NAMESPACE:
  Logical isolation (like a virtual cluster).
  e.g. dev, staging, prod.

INGRESS:
  HTTP/HTTPS routing into the cluster (URL-based, host-based).
```


## Pod Manifest

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    app: myapp
    env: prod
spec:
  containers:
  - name: app
    image: myapp:1.0.0
    ports:
    - containerPort: 3000
    env:
    - name: NODE_ENV
      value: production
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: database_url
    resources:
      requests:
        cpu: 100m         # 0.1 CPU
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 512Mi
    livenessProbe:        # Restart if fails
      httpGet:
        path: /health
        port: 3000
      initialDelaySeconds: 10
      periodSeconds: 10
    readinessProbe:       # Remove from LB if fails
      httpGet:
        path: /ready
        port: 3000
      periodSeconds: 5
  restartPolicy: Always
```


## Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3                      # 3 pods
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1                  # 1 extra during update
      maxUnavailable: 0            # Never below 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: myapp-config
        - secretRef:
            name: myapp-secrets
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet: { path: /health, port: 3000 }
          periodSeconds: 10
        readinessProbe:
          httpGet: { path: /ready, port: 3000 }
          periodSeconds: 5
```


## Service

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
  - port: 80                    # Service port
    targetPort: 3000            # Container port
  type: ClusterIP               # Internal only
  # type: LoadBalancer          # External (creates cloud LB)
  # type: NodePort              # Exposes on each node's IP:port
```

Now other pods in the cluster can reach: `http://myapp` or `http://myapp.default.svc.cluster.local`.


## Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.example.com
    secretName: api-tls
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```


## ConfigMap and Secret

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  LOG_LEVEL: info
  CACHE_TTL: "300"
  FEATURE_FLAGS: "feature_a=true,feature_b=false"
---
# secret.yaml (values base64-encoded)
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  database_url: cG9zdGdyZXM6Ly91c2VyOnBhc3NAaG9zdC9kYg==
  api_key: c2VjcmV0X2tleQ==

# Generate base64:
# echo -n "my-secret-value" | base64

# BETTER: Use external secrets management (Vault, AWS Secrets Manager,
# sealed-secrets, external-secrets-operator). Don't commit secrets to Git!
```


## kubectl Commands

```bash
# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f .                  # All YAML in current dir
kubectl apply -k .                  # Kustomize

# Get resources
kubectl get pods                    # All pods (current namespace)
kubectl get pods -A                 # All namespaces
kubectl get pods -n production
kubectl get pods -l app=myapp       # Filter by label
kubectl get pods -o wide            # More columns
kubectl get pods -o yaml            # Full YAML

# Describe (detailed info)
kubectl describe pod myapp-xxx
kubectl describe deployment myapp
kubectl describe svc myapp

# Logs
kubectl logs myapp-xxx
kubectl logs -f myapp-xxx           # Follow
kubectl logs --tail 100 myapp-xxx
kubectl logs -l app=myapp           # All matching pods
kubectl logs --previous myapp-xxx   # From previous container (if restarted)

# Exec
kubectl exec -it myapp-xxx -- bash
kubectl exec myapp-xxx -- ls /

# Port forward (debug locally)
kubectl port-forward svc/myapp 8080:80
# Now localhost:8080 → service

# Scale
kubectl scale deployment myapp --replicas=10

# Update image (rolling)
kubectl set image deployment/myapp app=myapp:1.1.0
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp           # Revert
kubectl rollout undo deployment/myapp --to-revision=3

# Delete
kubectl delete pod myapp-xxx
kubectl delete deployment myapp
kubectl delete -f deployment.yaml

# Context (multiple clusters)
kubectl config get-contexts
kubectl config use-context prod-cluster

# Resource consumption (requires metrics-server)
kubectl top pods
kubectl top nodes
```


## Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70    # Scale up if avg CPU > 70%
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5min before scaling down
    scaleUp:
      stabilizationWindowSeconds: 30
```


---

# CHAPTER 4: CI/CD


## CI/CD Concepts

```
CONTINUOUS INTEGRATION (CI):
  Every commit triggers:
    - Linting
    - Unit tests
    - Integration tests
    - Build artifact (Docker image)
  Goal: catch problems within minutes of writing code.

CONTINUOUS DEPLOYMENT (CD):
  Successful CI → auto-deploy to environment.
    - Staging: usually automatic
    - Production: with approval gates, canary, or fully automated

PIPELINE STAGES (typical):
  Code Push
    → Lint (eslint, ruff)
    → Test (unit, integration)
    → Build (docker, npm)
    → Scan (security, vulns)
    → Deploy to staging
    → Smoke tests
    → Deploy to production (rolling/canary)
    → Notify (Slack, email)

PRINCIPLES:
  - Every commit goes through pipeline (no skipping)
  - Failed pipeline blocks merge
  - Fast feedback (<10 min total ideal)
  - Reproducible builds (same code → same artifact)
```


## GitHub Actions Example

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/test

      - name: Coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to K8s
        run: |
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig
          export KUBECONFIG=kubeconfig
          kubectl set image deployment/myapp app=ghcr.io/${{ github.repository }}:${{ github.sha }}
          kubectl rollout status deployment/myapp -n staging

  deploy-prod:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production       # Requires approval (configured in GitHub)
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to K8s
        run: |
          # Same as staging but prod cluster
          ...
      - name: Smoke test
        run: |
          curl --fail https://api.example.com/health
      - name: Notify Slack
        uses: rtCamp/action-slack-notify@v2
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
          SLACK_MESSAGE: 'Deployed ${{ github.sha }} to production'
```


## GitLab CI Example

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

test:
  stage: test
  image: node:20-alpine
  services:
    - postgres:16-alpine
  variables:
    POSTGRES_DB: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgres://postgres:test@postgres:5432/test
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
  script:
    - npm ci
    - npm run lint
    - npm test
  coverage: '/All files\s+\|\s+([0-9.]+)/'

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE .
    - docker push $IMAGE
  only:
    - main
    - develop

deploy_prod:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/myapp app=$IMAGE -n prod
    - kubectl rollout status deployment/myapp -n prod --timeout=5m
  environment:
    name: production
    url: https://api.example.com
  when: manual                # Requires manual click
  only:
    - main
```


## Deployment Strategies

```
ROLLING UPDATE (K8s default):
  Replace pods 1 (or N) at a time.
  Both versions live briefly.
  Pros: No downtime, simple
  Cons: Mixed-version during deploy (DB compatibility critical)

BLUE-GREEN:
  Two complete environments (blue=v1, green=v2).
  Cutover traffic instantly.
  Pros: Instant rollback, test before traffic
  Cons: 2x resources during transition

CANARY:
  Deploy v2 to 5% of users → monitor → 10% → 25% → 100%.
  Pros: Limited blast radius for bad releases
  Cons: Complex routing, need good observability

FEATURE FLAGS:
  Deploy code with feature OFF.
  Toggle on for users gradually via config.
  Pros: Decouple deploy from release, easy A/B test
  Cons: Code complexity, dead-code accumulation
  Tools: LaunchDarkly, Unleash, Flagsmith

RECOMMENDED DEFAULT:
  Rolling updates for most apps.
  Canary for high-risk changes.
  Feature flags for product experiments.
```


---

# CHAPTER 5: INFRASTRUCTURE AS CODE


## Terraform Basics

```hcl
# main.tf — provision AWS infrastructure

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Remote state (recommended for teams)
  backend "s3" {
    bucket         = "mycompany-tfstate"
    key            = "prod/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "eu-central-1"
}

# Variables
variable "environment" {
  type    = string
  default = "prod"
}

variable "instance_type" {
  type    = string
  default = "t3.medium"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

# Subnet
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${var.environment}-public-${count.index}"
  }
}

# EC2 instance
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public[0].id

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y docker
    systemctl start docker
    systemctl enable docker
  EOF

  tags = {
    Name        = "${var.environment}-web"
    Environment = var.environment
  }
}

# Output
output "web_public_ip" {
  value = aws_instance.web.public_ip
}

# Data sources (read existing resources)
data "aws_availability_zones" "available" {
  state = "available"
}
```

```bash
# Terraform workflow
terraform init        # First time / after changing providers
terraform fmt         # Format code
terraform validate    # Syntax check
terraform plan        # Preview changes
terraform apply       # Apply (asks for confirmation)
terraform apply -auto-approve
terraform destroy     # Tear down

# State management
terraform state list
terraform state show aws_instance.web
terraform import aws_instance.web i-1234567890   # Import existing

# Modules (reusable components)
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  name    = "my-vpc"
  cidr    = "10.0.0.0/16"
  ...
}
```


## Ansible Basics

```yaml
# playbook.yml — configure servers
---
- name: Configure web servers
  hosts: webservers
  become: yes              # sudo

  vars:
    app_name: myapp
    app_user: deploy
    app_dir: /opt/{{ app_name }}

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install required packages
      apt:
        name:
          - nginx
          - postgresql-client
          - curl
        state: present

    - name: Create app user
      user:
        name: "{{ app_user }}"
        system: yes
        shell: /bin/bash

    - name: Create app directory
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        mode: '0755'

    - name: Copy nginx config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
      notify:
        - Reload nginx        # Triggers handler

    - name: Enable nginx site
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link

    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: Reload nginx
      service:
        name: nginx
        state: reloaded
```

```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com

[all:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/deploy_key
```

```bash
# Run playbook
ansible-playbook -i inventory.ini playbook.yml

# Specific hosts
ansible-playbook -i inventory.ini playbook.yml --limit webservers

# Dry run
ansible-playbook -i inventory.ini playbook.yml --check

# Ad-hoc command
ansible all -i inventory.ini -m ping
ansible webservers -i inventory.ini -a "uptime"
```


---

# CHAPTER 6: OBSERVABILITY


## Logs, Metrics, Traces — The 3 Pillars

```
LOGS:        what happened (events)
METRICS:     how much/often (numbers, time series)
TRACES:      why slow / where failed (request flow across services)

Each answers different questions:
  Logs:    "What error occurred at 14:32?"
  Metrics: "What's our RPS / error rate / p99 latency?"
  Traces:  "Why is /api/checkout slow? Which service?"
```


## Prometheus Metrics

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'myapp'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: myapp
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)
        replacement: ${1}

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

# Alerting rules
rule_files:
  - 'alerts.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

```yaml
# alerts.yml
groups:
  - name: app
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          / sum(rate(http_requests_total[5m])) by (service) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency >1s on {{ $labels.service }}"

      - alert: PodMemoryUsage
        expr: |
          container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} memory >90%"
```


## PromQL Examples

```
# Total requests in last 5min
sum(rate(http_requests_total[5m]))

# By endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m]))

# p95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Memory by pod
sum(container_memory_usage_bytes{namespace="prod"}) by (pod)

# Top 5 slowest endpoints by p99
topk(5,
  histogram_quantile(0.99,
    sum(rate(http_request_duration_seconds_bucket[5m])) by (endpoint, le)
  )
)
```


## Centralized Logging

```
PATTERNS:
  ELK stack:      Elasticsearch + Logstash + Kibana (classic, heavy)
  EFK stack:      Elasticsearch + Fluentd + Kibana (lighter ingest)
  Loki:           Grafana Loki + Promtail (cheaper, integrates with Grafana)
  Datadog/New Relic/Splunk: SaaS

PRINCIPLES:
  - JSON-structured logs (not free text)
  - Include trace ID in every log line
  - Don't log secrets
  - Sample very high-volume logs (e.g. health checks)
  - Different log levels: DEBUG, INFO, WARN, ERROR, FATAL

EXAMPLE (Loki + Promtail in K8s):
```

```yaml
# promtail-config.yaml
clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - cri: {}              # Parse CRI runtime format
      - json:
          expressions:
            level:
            msg:
            trace_id:
      - labels:
          level:
    relabel_configs:
      - action: replace
        source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - action: replace
        source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
```


## Distributed Tracing (Jaeger / OpenTelemetry)

```javascript
// Node.js with OpenTelemetry
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
    traceExporter: new OTLPTraceExporter({
        url: 'http://jaeger:4317',
    }),
    instrumentations: [getNodeAutoInstrumentations()],
    serviceName: 'myapp',
});

sdk.start();

// All HTTP/DB calls now auto-traced
// In Jaeger UI: see full request timeline across services
```


---

# CHAPTER 7: BEST PRACTICES AND PITFALLS


## Twelve-Factor App Principles

```
Foundational rules for SaaS apps (twelve-factor.net):

1. CODEBASE: One codebase tracked in revision control, many deploys
2. DEPENDENCIES: Explicitly declare and isolate (package.json, requirements.txt)
3. CONFIG: Store in environment (no hardcoded secrets!)
4. BACKING SERVICES: Treat as attached resources (db = URL, swap easily)
5. BUILD, RELEASE, RUN: Strictly separate stages
6. PROCESSES: Stateless (sessions in Redis, not memory)
7. PORT BINDING: Self-contained (app exports HTTP, doesn't need Apache)
8. CONCURRENCY: Scale out via the process model
9. DISPOSABILITY: Fast startup, graceful shutdown
10. DEV/PROD PARITY: Keep development, staging, production as similar as possible
11. LOGS: Treat as event streams (stdout/stderr → external aggregator)
12. ADMIN PROCESSES: Run admin tasks (migrations, repl) as one-offs

Following these → easy to scale, deploy, debug.
```


## Common Pitfalls

```
PITFALL 1: Mutable infrastructure
  SSH-ing in to fix things by hand → drift, can't reproduce.
  → Use IaC. Rebuild from scratch if needed.

PITFALL 2: Secrets in Git
  Once in history, leaked forever.
  → Use .gitignore, pre-commit hooks, secret scanners (gitleaks).
  → If leaked: rotate the secret IMMEDIATELY.

PITFALL 3: No backups (or untested backups)
  "We have backups" — never tested. Disaster strikes — restore fails.
  → Schedule monthly restore drills.

PITFALL 4: Single point of failure
  Database, LB, single node — anything alone is a SPOF.
  → Multi-AZ, multi-region critical components.

PITFALL 5: Logging too much / too little
  Too much: storage cost, signal/noise problem.
  Too little: can't debug production.
  → Standard levels, sample high-volume, INFO for business events.

PITFALL 6: No alerting on alerts
  Alert fires but no one notices. Or every alert is fatigue.
  → PagerDuty/Opsgenie with rotation. Tune thresholds. Alert on symptoms not causes.

PITFALL 7: Manual deployments
  Different person → different procedure. Mistakes happen.
  → Automate. If not in pipeline, it shouldn't ship.

PITFALL 8: No staging environment
  Test in production = pain.
  → Mirror prod (smaller scale) for pre-release testing.

PITFALL 9: Ignoring resource limits
  Container has no CPU/memory limits → noisy neighbor problem.
  → Always set requests AND limits in K8s.

PITFALL 10: latest tag in production
  image: myapp:latest → unpredictable. What's actually running?
  → Pin specific versions/digests. Use semantic versioning.

PITFALL 11: Long-lived secrets in containers
  Static creds baked in → if leaked, valid forever.
  → Use short-lived tokens, IAM roles, secret rotation.

PITFALL 12: No documentation
  Hero culture: only one person knows. They leave. Disaster.
  → README, runbooks, architecture docs. Practice "what would the new person do?"

PITFALL 13: Premature Kubernetes
  K8s adds huge complexity. <100 containers? Use simpler tools.
  → Docker Compose on a VM, Render, Railway, Fly.io for small apps.

PITFALL 14: Not testing rollback
  Forward path tested; rollback never. When needed, it breaks too.
  → Practice rollback. Database migrations should be reversible.

PITFALL 15: Cost surprises
  Cloud spending balloons. Discover at end of month.
  → Set budgets, alerts (AWS Budgets, GCP Budgets). Tag resources. Review weekly.
```


## Recommended Reading Path for Beginners

```
1. LINUX BASICS (1 month)
   - File system, processes, permissions
   - Shell scripting
   - SSH and remote work
   - Resources: "The Linux Command Line" by William Shotts

2. DOCKER (2 weeks)
   - Containers vs VMs
   - Dockerfile best practices
   - docker-compose
   - Resource: docker.com tutorials

3. GIT (deeply, 2 weeks)
   - Branching strategies
   - Merge vs rebase
   - Conflict resolution
   - Resource: "Pro Git" book (free online)

4. CI/CD (2 weeks)
   - GitHub Actions or GitLab CI
   - Build a pipeline for a real project
   - Test, build, deploy

5. CLOUD (1 month — pick one!)
   - AWS, GCP, or Azure (depends on job market)
   - Compute, storage, networking, IAM, managed databases

6. KUBERNETES (1 month, ONLY if needed)
   - Local with minikube/kind first
   - Deploy a real app
   - Resource: "Kubernetes Up & Running" by Hightower et al.

7. IaC (2 weeks)
   - Terraform basics
   - Manage real cloud resources

8. OBSERVABILITY (2 weeks)
   - Prometheus + Grafana
   - Centralized logging
   - Tracing

TOTAL: ~6 months part-time to be functional.
       ~2 years to be senior-level DevOps.
```