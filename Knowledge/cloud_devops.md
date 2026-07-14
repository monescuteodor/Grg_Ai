Cloud Architecture & DevOps Complete Reference
CHAPTER 1: GETTING STARTED WITH CLOUD & DEVOPS
Remarks
Cloud computing delivers computing services (servers, storage, databases, networking, software) over the internet. DevOps combines development and operations to shorten the systems development lifecycle. Key concepts: containers (Docker), orchestration (Kubernetes), CI/CD pipelines, Infrastructure as Code (Terraform), microservices, service mesh, observability.
Tools: Docker, Kubernetes (k8s), Terraform, Ansible, Jenkins, GitLab CI, GitHub Actions, Prometheus, Grafana, Helm, ArgoCD, AWS CLI, gcloud, az.
Hello Cloud
# hello_cloud.py
"""
First cloud program: interact with AWS S3 (requires boto3).
"""
import boto3
from botocore.exceptions import ClientError

def hello_s3(bucket_name: str, region: str = "us-east-1"):
    """Demonstrate basic S3 operations."""
    s3 = boto3.client('s3', region_name=region)
    
    # List buckets
    try:
        response = s3.list_buckets()
        print("Your S3 buckets:")
        for bucket in response['Buckets']:
            print(f"  • {bucket['Name']} (created: {bucket['CreationDate']})")
    except ClientError as e:
        print(f"Error: {e}")
    
    # Create a bucket (if doesn't exist)
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"\n✓ Created bucket: {bucket_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print(f"\n✓ Bucket already exists: {bucket_name}")
        else:
            print(f"Error creating bucket: {e}")
    
    # Upload a file
    test_content = b"Hello from Cloud Architecture!"
    try:
        s3.put_object(
            Bucket=bucket_name,
            Key='hello.txt',
            Body=test_content,
            ContentType='text/plain'
        )
        print(f"✓ Uploaded hello.txt to {bucket_name}")
    except ClientError as e:
        print(f"Upload error: {e}")
    
    # Download the file
    try:
        response = s3.get_object(Bucket=bucket_name, Key='hello.txt')
        content = response['Body'].read().decode('utf-8')
        print(f"✓ Downloaded content: {content}")
    except ClientError as e:
        print(f"Download error: {e}")

# Note: Requires AWS credentials configured
# hello_s3("my-test-bucket-12345")

DevOps Principles
# CALMS framework:
# - Culture: collaboration between dev and ops
# - Automation: CI/CD, IaC, monitoring
# - Lean: eliminate waste, fast feedback
# - Measurement: metrics, KPIs, observability
# - Sharing: knowledge, tools, practices

# Key metrics (DORA):
# 1. Deployment Frequency: how often code reaches production
# 2. Lead Time for Changes: commit to production
# 3. Mean Time to Recovery (MTTR): incident to resolution
# 4. Change Failure Rate: % of deployments causing failures

# DevOps maturity levels:
# Level 1: Manual deployments, siloed teams
# Level 2: Basic CI, some automation
# Level 3: Full CI/CD, IaC, containerization
# Level 4: Advanced observability, GitOps, service mesh
# Level 5: Self-healing systems, AIOps

print("=== DevOps Principles ===")
print("✓ Automate everything that can be automated")
print("✓ Shift left: security and testing early")
print("✓ Infrastructure as Code: version control everything")
print("✓ Continuous everything: integration, delivery, deployment")
print("✓ Monitor and measure: observability is key")
print("✓ Blameless postmortems: learn from failures")

CHAPTER 2: CONTAINERIZATION WITH DOCKER
Dockerfile Basics
# Dockerfile: instructions to build a container image
# Best practices: minimize layers, use multi-stage builds, non-root user

# Example: Python web app Dockerfile
"""
# Multi-stage build for Python Flask app
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies first (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage
FROM python:3.11-slim

# Security: run as non-root user
RUN useradd -m -u 1000 appuser
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
"""

# Example: Node.js Dockerfile
"""
FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine

RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=appuser:appgroup . .

USER appuser
EXPOSE 3000
CMD ["node", "server.js"]
"""

Docker Compose
# docker-compose.yml: multi-container applications
"""
version: '3.8'

services:
  # Web application
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    networks:
      - app-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

  # PostgreSQL database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Redis cache
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - app-network

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
"""

Docker Python SDK
import docker
import time

def docker_demo():
    """Demonstrate Docker Python SDK operations."""
    client = docker.from_env()
    
    # List running containers
    print("=== Running Containers ===")
    for container in client.containers.list():
        print(f"  {container.name}: {container.status} ({container.image.tags[0]})")
    
    # Pull an image
    print("\n=== Pulling Image ===")
    image = client.images.pull("nginx:alpine")
    print(f"  Pulled: {image.tags[0]}")
    
    # Run a container
    print("\n=== Running Container ===")
    container = client.containers.run(
        "nginx:alpine",
        detach=True,
        ports={'80/tcp': 8080},
        name="test-nginx"
    )
    print(f"  Started: {container.name} (ID: {container.short_id})")
    
    # Wait and check logs
    time.sleep(2)
    logs = container.logs().decode('utf-8')
    print(f"  Logs: {logs[:100]}...")
    
    # Stop and remove
    container.stop()
    container.remove()
    print(f"  Stopped and removed: {container.name}")
    
    # Build an image
    print("\n=== Building Image ===")
    # image, logs = client.images.build(path=".", tag="myapp:latest")
    # print(f"  Built: {image.tags[0]}")

# docker_demo()

Container Security Best Practices
# 1. Use minimal base images (alpine, distroless)
# 2. Run as non-root user
# 3. Scan images for vulnerabilities (Trivy, Snyk)
# 4. Use specific image tags (not :latest)
# 5. Implement read-only filesystems
# 6. Drop unnecessary capabilities
# 7. Use secrets management (not environment variables)
# 8. Implement network policies
# 9. Regular updates and patching
# 10. Use multi-stage builds to reduce attack surface

# Example: Secure Dockerfile
"""
FROM python:3.11-slim

# Install security tools
RUN apt-get update && apt-get install -y --no-install-recommends \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup app.py .

# Security hardening
USER appuser
EXPOSE 5000

# Read-only filesystem (set in docker run)
# --read-only --tmpfs /tmp

# Drop all capabilities (set in docker run)
# --cap-drop=ALL

# No new privileges
# --security-opt=no-new-privileges

CMD ["python", "app.py"]
"""

# Docker run with security options:
"""
docker run -d \\
  --name secure-app \\
  --read-only \\
  --tmpfs /tmp \\
  --cap-drop=ALL \\
  --cap-add=NET_BIND_SERVICE \\
  --security-opt=no-new-privileges \\
  --user 1000:1000 \\
  --memory=512m \\
  --cpus=1.0 \\
  myapp:latest
"""

CHAPTER 3: KUBERNETES (K8S) FUNDAMENTALS
Kubernetes Architecture
# Control Plane:
# - API Server: front-end for k8s API
# - etcd: distributed key-value store
# - Scheduler: assigns pods to nodes
# - Controller Manager: runs controllers
# - Cloud Controller Manager: cloud-specific logic

# Worker Nodes:
# - kubelet: agent that ensures containers run
# - kube-proxy: network proxy
# - Container Runtime: Docker, containerd, CRI-O

# Key Objects:
# - Pod: smallest deployable unit (one or more containers)
# - Deployment: manages ReplicaSets (rolling updates)
# - Service: stable network endpoint
# - ConfigMap/Secret: configuration data
# - Ingress: HTTP routing
# - PersistentVolume/Claim: storage

# Namespaces: virtual clusters (default, kube-system, kube-public)

Kubernetes Deployment YAML
"""
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: production
  labels:
    app: web-app
    version: v1.2.3
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: web-app
        version: v1.2.3
    spec:
      serviceAccountName: web-app-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: web-app
        image: myregistry.com/web-app:v1.2.3
        imagePullPolicy: Always
        ports:
        - containerPort: 5000
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: CACHE_TTL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: cache_ttl
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 15
          periodSeconds: 20
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /health
            port: 5000
          failureThreshold: 30
          periodSeconds: 10
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
          readOnly: true
        - name: tmp-volume
          mountPath: /tmp
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
      volumes:
      - name: config-volume
        configMap:
          name: app-config
      - name: tmp-volume
        emptyDir:
          sizeLimit: 100Mi
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web-app
              topologyKey: kubernetes.io/hostname
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "web-app"
        effect: "NoSchedule"
"""

Kubernetes Service and Ingress
"""
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
  namespace: production
spec:
  selector:
    app: web-app
  ports:
  - name: http
    port: 80
    targetPort: 5000
    protocol: TCP
  type: ClusterIP
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-app-service
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
"""

Kubernetes Python Client
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def k8s_demo():
    """Demonstrate Kubernetes Python client operations."""
    # Load kubeconfig
    config.load_kube_config()
    
    # Create API clients
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    
    # List pods
    print("=== Pods in default namespace ===")
    try:
        pods = v1.list_namespaced_pod(namespace="default")
        for pod in pods.items:
            print(f"  {pod.metadata.name}: {pod.status.phase}")
    except ApiException as e:
        print(f"Error: {e}")
    
    # List deployments
    print("\n=== Deployments ===")
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace="default")
        for dep in deployments.items:
            print(f"  {dep.metadata.name}: {dep.status.replicas} replicas")
    except ApiException as e:
        print(f"Error: {e}")
    
    # Create a deployment
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="test-deployment"),
        spec=client.V1DeploymentSpec(
            replicas=2,
            selector={"matchLabels": {"app": "test"}},
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels={"app": "test"}),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="test",
                            image="nginx:alpine",
                            ports=[client.V1ContainerPort(container_port=80)]
                        )
                    ]
                )
            )
        )
    )
    
    # try:
    #     apps_v1.create_namespaced_deployment(
    #         namespace="default",
    #         body=deployment
    #     )
    #     print("\n✓ Created deployment: test-deployment")
    # except ApiException as e:
    #     print(f"Error creating deployment: {e}")

# k8s_demo()

Helm Charts
# Helm: package manager for Kubernetes
# Chart structure:
# mychart/
#   Chart.yaml
#   values.yaml
#   templates/
#     deployment.yaml
#     service.yaml
#     ingress.yaml
#     _helpers.tpl

# Chart.yaml
"""
apiVersion: v2
name: web-app
description: A Helm chart for web application
type: application
version: 1.2.3
appVersion: "1.2.3"
keywords:
  - web
  - python
  - flask
maintainers:
  - name: DevOps Team
    email: devops@example.com
"""

# values.yaml
"""
replicaCount: 3

image:
  repository: myregistry.com/web-app
  pullPolicy: Always
  tag: "1.2.3"

service:
  type: ClusterIP
  port: 80
  targetPort: 5000

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - app.example.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

env:
  DATABASE_URL:
    secretKeyRef:
      name: db-credentials
      key: url
  CACHE_TTL: "3600"
"""

# Helm commands:
# helm install my-release ./mychart
# helm upgrade my-release ./mychart
# helm rollback my-release 1
# helm uninstall my-release
# helm template my-release ./mychart > output.yaml

CHAPTER 4: CI/CD PIPELINES
GitHub Actions Workflow
"""
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Code quality and testing
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black mypy
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=120
    
    - name: Format check with black
      run: black --check .
    
    - name: Type check with mypy
      run: mypy .
    
    - name: Test with pytest
      run: |
        pytest --cov=app --cov-report=xml --cov-report=html
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false

  # Security scanning
  security:
    runs-on: ubuntu-latest
    needs: test
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run Bandit security linter
      run: |
        pip install bandit
        bandit -r app/ -f json -o bandit-results.json
    
    - name: Check for secrets
      uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: ${{ github.event.repository.default_branch }}

  # Build and push Docker image
  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    permissions:
      contents: read
      packages: write
    steps:
    - uses: actions/checkout@v4
    
    - name: Log in to Container Registry
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
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  # Deploy to staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: staging
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
    
    - name: Deploy to staging
      run: |
        kubectl set image deployment/web-app \\
          web-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \\
          -n staging
        kubectl rollout status deployment/web-app -n staging --timeout=300s

  # Deploy to production
  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
    
    - name: Deploy to production
      run: |
        kubectl set image deployment/web-app \\
          web-app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \\
          -n production
        kubectl rollout status deployment/web-app -n production --timeout=300s
    
    - name: Run smoke tests
      run: |
        sleep 30
        curl -f https://app.example.com/health || exit 1
    
    - name: Notify on success
      if: success()
      run: |
        echo "✓ Production deployment successful"
        # curl -X POST ${{ secrets.SLACK_WEBHOOK }} \\
        #   -H 'Content-type: application/json' \\
        #   --data '{"text":"Production deployment successful!"}'
"""

GitLab CI/CD Pipeline
"""
# .gitlab-ci.yml
stages:
  - test
  - build
  - security
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

services:
  - docker:20.10-dind

# Test stage
unit-tests:
  stage: test
  image: python:3.11-slim
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  script:
    - pytest --cov=app --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

lint:
  stage: test
  image: python:3.11-slim
  script:
    - pip install flake8 black
    - flake8 .
    - black --check .

# Build stage
build-image:
  stage: build
  image: docker:20.10
  services:
    - docker:20.10-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - develop

# Security stage
trivy-scan:
  stage: security
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_TAG
  allow_failure: true
  only:
    - main

# Deploy stages
deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context staging
    - kubectl set image deployment/web-app web-app=$IMAGE_TAG -n staging
    - kubectl rollout status deployment/web-app -n staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl config use-context production
    - kubectl set image deployment/web-app web-app=$IMAGE_TAG -n production
    - kubectl rollout status deployment/web-app -n production
  environment:
    name: production
    url: https://app.example.com
  when: manual
  only:
    - main
"""

Jenkins Pipeline (Declarative)
"""
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'myregistry.com'
        IMAGE_NAME = 'web-app'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    pytest --cov=app
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    cobertura coberturaReportFile: 'coverage.xml'
                }
            }
        }
        
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}")
                }
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}").push()
                        docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}").push('latest')
                    }
                }
            }
        }
        
        stage('Deploy Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                    kubectl set image deployment/web-app \\
                        web-app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \\
                        -n staging
                '''
            }
        }
        
        stage('Deploy Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh '''
                    kubectl set image deployment/web-app \\
                        web-app=${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \\
                        -n production
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            slackSend(channel: '#deployments', 
                     color: 'good', 
                     message: "Build ${env.BUILD_NUMBER} successful!")
        }
        failure {
            slackSend(channel: '#deployments', 
                     color: 'danger', 
                     message: "Build ${env.BUILD_NUMBER} failed!")
        }
    }
}
"""

CHAPTER 5: INFRASTRUCTURE AS CODE (TERRAFORM)
Terraform Basics
# Terraform: declarative infrastructure provisioning
# Providers: AWS, GCP, Azure, Kubernetes, etc.
# State: tracks infrastructure state (remote backend recommended)

# main.tf - AWS infrastructure
"""
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "terraform-state-prod"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project_name
      ManagedBy   = "Terraform"
    }
  }
}
"""

# variables.tf
"""
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "web-app"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
"""

# vpc.tf
"""
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.project_name}-public-${count.index + 1}"
    Type = "Public"
  }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {
    Name = "${var.project_name}-private-${count.index + 1}"
    Type = "Private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

data "aws_availability_zones" "available" {
  state = "available"
}
"""

# eks.tf - Kubernetes cluster
"""
resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.28"
  
  vpc_config {
    subnet_ids              = aws_subnet.private[*].id
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }
  
  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.project_name}-nodes"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = aws_subnet.private[*].id
  
  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 2
  }
  
  instance_types = [var.instance_type]
  
  depends_on = [
    aws_iam_role_policy_attachment.eks_node_policy
  ]
}

resource "aws_iam_role" "eks_cluster" {
  name = "${var.project_name}-eks-cluster-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster.name
}

resource "aws_iam_role" "eks_nodes" {
  name = "${var.project_name}-eks-nodes-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_node_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks_nodes.name
}
"""

# outputs.tf
"""
output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = aws_eks_cluster.main.name
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}
"""

# Terraform commands:
# terraform init
# terraform plan
# terraform apply
# terraform destroy
# terraform fmt
# terraform validate

Terraform Python SDK (boto3 for AWS)
import boto3
import json

def aws_infrastructure_demo():
    """Demonstrate AWS infrastructure operations with boto3."""
    ec2 = boto3.client('ec2', region_name='us-east-1')
    s3 = boto3.client('s3', region_name='us-east-1')
    
    # List EC2 instances
    print("=== EC2 Instances ===")
    try:
        response = ec2.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                name = next((tag['Value'] for tag in instance.get('Tags', []) 
                           if tag['Key'] == 'Name'), 'Unnamed')
                print(f"  {name}: {instance['InstanceId']} ({instance['State']['Name']})")
    except Exception as e:
        print(f"Error: {e}")
    
    # List S3 buckets
    print("\n=== S3 Buckets ===")
    try:
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            print(f"  {bucket['Name']}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Get VPC information
    print("\n=== VPCs ===")
    try:
        response = ec2.describe_vpcs()
        for vpc in response['Vpcs']:
            cidr = vpc['CidrBlock']
            state = vpc['State']
            print(f"  {vpc['VpcId']}: {cidr} ({state})")
    except Exception as e:
        print(f"Error: {e}")

# aws_infrastructure_demo()

CHAPTER 6: ANSIBLE AUTOMATION
Ansible Playbook
"""
# playbook.yml - Deploy web application
---
- name: Deploy Web Application
  hosts: webservers
  become: yes
  vars:
    app_name: web-app
    app_version: "1.2.3"
    app_port: 5000
    db_host: "{{ vault_db_host }}"
    db_user: "{{ vault_db_user }}"
    db_password: "{{ vault_db_password }}"
  
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install required packages
      apt:
        name:
          - python3
          - python3-pip
          - python3-venv
          - nginx
          - git
        state: present
    
    - name: Create application user
      user:
        name: "{{ app_name }}"
        system: yes
        shell: /bin/false
        home: "/opt/{{ app_name }}"
    
    - name: Create application directory
      file:
        path: "/opt/{{ app_name }}"
        state: directory
        owner: "{{ app_name }}"
        group: "{{ app_name }}"
        mode: '0755'
    
    - name: Clone application repository
      git:
        repo: "https://github.com/example/{{ app_name }}.git"
        dest: "/opt/{{ app_name }}/src"
        version: "v{{ app_version }}"
      become_user: "{{ app_name }}"
    
    - name: Create virtual environment
      command: python3 -m venv /opt/{{ app_name }}/venv
      args:
        creates: "/opt/{{ app_name }}/venv"
      become_user: "{{ app_name }}"
    
    - name: Install Python dependencies
      pip:
        requirements: "/opt/{{ app_name }}/src/requirements.txt"
        virtualenv: "/opt/{{ app_name }}/venv"
      become_user: "{{ app_name }}"
    
    - name: Create systemd service
      template:
        src: templates/app.service.j2
        dest: "/etc/systemd/system/{{ app_name }}.service"
        mode: '0644'
      notify: Restart application
    
    - name: Create nginx configuration
      template:
        src: templates/nginx.conf.j2
        dest: "/etc/nginx/sites-available/{{ app_name }}"
        mode: '0644'
      notify: Reload nginx
    
    - name: Enable nginx site
      file:
        src: "/etc/nginx/sites-available/{{ app_name }}"
        dest: "/etc/nginx/sites-enabled/{{ app_name }}"
        state: link
      notify: Reload nginx
    
    - name: Remove default nginx site
      file:
        path: /etc/nginx/sites-enabled/default
        state: absent
      notify: Reload nginx
    
    - name: Start and enable application service
      systemd:
        name: "{{ app_name }}"
        state: started
        enabled: yes
        daemon_reload: yes
    
    - name: Start and enable nginx
      systemd:
        name: nginx
        state: started
        enabled: yes
    
    - name: Wait for application to start
      wait_for:
        port: "{{ app_port }}"
        delay: 5
        timeout: 60
  
  handlers:
    - name: Restart application
      systemd:
        name: "{{ app_name }}"
        state: restarted
        daemon_reload: yes
    
    - name: Reload nginx
      systemd:
        name: nginx
        state: reloaded
"""

Ansible Inventory
"""
# inventory.ini
[webservers]
web1.example.com ansible_host=192.168.1.10
web2.example.com ansible_host=192.168.1.11
web3.example.com ansible_host=192.168.1.12

[dbservers]
db1.example.com ansible_host=192.168.1.20

[loadbalancers]
lb1.example.com ansible_host=192.168.1.30

[production:children]
webservers
dbservers
loadbalancers

[production:vars]
ansible_user=deploy
ansible_ssh_private_key_file=~/.ssh/deploy_key
ansible_python_interpreter=/usr/bin/python3
env=production
"""

Ansible Python API
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context
from ansible.module_utils.common.collections import ImmutableDict

def run_ansible_playbook(playbook_path, inventory_path):
    """Run Ansible playbook programmatically."""
    # Initialize Ansible context
    context.CLIARGS = ImmutableDict(
        connection='local',
        module_path=[''],
        forks=10,
        become=None,
        become_method=None,
        become_user=None,
        check=False,
        diff=False,
        verbosity=0
    )
    
    # Initialize objects
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=[inventory_path])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    
    # Create playbook executor
    playbook = PlaybookExecutor(
        playbooks=[playbook_path],
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords={}
    )
    
    # Run playbook
    results = playbook.run()
    
    return results

# run_ansible_playbook('playbook.yml', 'inventory.ini')

CHAPTER 7: MICROSERVICES ARCHITECTURE
Microservices Patterns
# Patterns:
# 1. API Gateway: single entry point, routing, authentication
# 2. Service Discovery: dynamic service registration
# 3. Circuit Breaker: prevent cascading failures
# 4. Saga: distributed transactions
# 5. CQRS: separate read and write models
# 6. Event Sourcing: store state changes as events
# 7. Sidecar: auxiliary processes (logging, monitoring)
# 8. Strangler Fig: gradual migration from monolith

# Benefits:
# - Independent deployment
# - Technology diversity
# - Fault isolation
# - Scalability per service
# - Team autonomy

# Challenges:
# - Distributed system complexity
# - Data consistency
# - Testing
# - Monitoring and debugging
# - Network latency

Flask Microservice Example
from flask import Flask, jsonify, request
import requests
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5001')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://order-service:5002')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'api-gateway'}), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Proxy to user service."""
    try:
        response = requests.get(
            f'{USER_SERVICE_URL}/users/{user_id}',
            timeout=5
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"User service error: {e}")
        return jsonify({'error': 'User service unavailable'}), 503

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create order with saga pattern."""
    data = request.json
    user_id = data.get('user_id')
    
    # Step 1: Validate user exists
    try:
        user_response = requests.get(
            f'{USER_SERVICE_URL}/users/{user_id}',
            timeout=5
        )
        if user_response.status_code != 200:
            return jsonify({'error': 'User not found'}), 404
    except requests.exceptions.RequestException:
        return jsonify({'error': 'User service unavailable'}), 503
    
    # Step 2: Create order
    try:
        order_response = requests.post(
            f'{ORDER_SERVICE_URL}/orders',
            json=data,
            timeout=10
        )
        return jsonify(order_response.json()), order_response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Order service error: {e}")
        return jsonify({'error': 'Order service unavailable'}), 503

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details."""
    try:
        response = requests.get(
            f'{ORDER_SERVICE_URL}/orders/{order_id}',
            timeout=5
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Order service unavailable'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

Service Mesh (Istio)
# Istio: service mesh for microservices
# Features: traffic management, security, observability

# Istio VirtualService (traffic routing)
"""
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: web-app
  namespace: production
spec:
  hosts:
  - web-app
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: web-app
        subset: canary
      weight: 100
  - route:
    - destination:
        host: web-app
        subset: stable
      weight: 90
    - destination:
        host: web-app
        subset: canary
      weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: web-app
  namespace: production
spec:
  host: web-app
  subsets:
  - name: stable
    labels:
      version: v1.2.3
  - name: canary
    labels:
      version: v1.3.0
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
"""

# Istio Gateway (ingress)
"""
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: app-gateway
  namespace: istio-system
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*.example.com"
    tls:
      httpsRedirect: true
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - "*.example.com"
    tls:
      mode: SIMPLE
      credentialName: example-tls
"""

CHAPTER 8: OBSERVABILITY AND MONITORING
Prometheus and Grafana
# Prometheus: time-series database for metrics
# Grafana: visualization and dashboards

# prometheus.yml
"""
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
  
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
"""

# alert_rules.yml
"""
groups:
  - name: application_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"
      
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s"
      
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod {{ $labels.pod }} is crash looping"
"""

# Grafana dashboard JSON (example)
"""
{
  "dashboard": {
    "id": null,
    "title": "Application Metrics",
    "tags": ["application"],
    "timezone": "browser",
    "panels": [
      {
        "type": "graph",
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ]
      },
      {
        "type": "graph",
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{status}}"
          }
        ]
      },
      {
        "type": "graph",
        "title": "Latency (95th percentile)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      }
    ]
  }
}
"""

ELK Stack (Elasticsearch, Logstash, Kibana)
# ELK: centralized logging solution

# logstash.conf
"""
input {
  beats {
    port => 5044
  }
  
  tcp {
    port => 5000
    codec => json
  }
}

filter {
  if [type] == "nginx" {
    grok {
      match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
    date {
      match => [ "timestamp", "dd/MMM/YYYY:HH:mm:ss Z" ]
    }
    geoip {
      source => "clientip"
    }
  }
  
  if [type] == "application" {
    json {
      source => "message"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{type}-%{+YYYY.MM.dd}"
  }
  
  stdout {
    codec => rubydebug
  }
}
"""

Python Logging with Structured Output
import logging
import json
from datetime import datetime
from pythonjsonlogger import jsonlogger

def setup_structured_logging():
    """Configure structured JSON logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_structured_logging()

# Example usage
logger.info("User login", extra={
    'user_id': 123,
    'ip_address': '192.168.1.100',
    'user_agent': 'Mozilla/5.0'
})

logger.error("Database connection failed", extra={
    'database': 'postgres',
    'host': 'db.example.com',
    'error': 'Connection timeout'
})

Distributed Tracing (Jaeger)
# OpenTelemetry: unified observability standard

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def setup_tracing(service_name: str):
    """Configure OpenTelemetry tracing."""
    # Set up tracer provider
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    
    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )
    
    # Add batch span processor
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Auto-instrument Flask and requests
    FlaskInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    
    return tracer

# Example usage
tracer = setup_tracing("api-gateway")

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)
        
        # Call user service
        response = requests.get(f'{USER_SERVICE_URL}/users/{user_id}')
        
        span.set_attribute("response.status", response.status_code)
        
        return jsonify(response.json()), response.status_code

CHAPTER 9: GITOPS AND ARGOCD
GitOps Principles
# GitOps: Git as single source of truth
# Principles:
# 1. Declarative: everything described declaratively
# 2. Versioned: Git for version control
# 3. Automated: pull-based deployment
# 4. Continuous: reconciliation loop

# GitOps workflow:
# 1. Developer commits to Git repo
# 2. CI builds and pushes image
# 3. Developer updates manifest with new image tag
# 4. GitOps operator (ArgoCD) detects change
# 5. ArgoCD syncs cluster state to Git state

ArgoCD Application
"""
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  
  source:
    repoURL: https://github.com/example/web-app-manifests.git
    targetRevision: HEAD
    path: k8s/production
  
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  
  revisionHistoryLimit: 10
"""

# Kustomization (kustomization.yaml)
"""
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml
  - configmap.yaml
  - secret.yaml

images:
  - name: myregistry.com/web-app
    newTag: v1.2.3

configMapGenerator:
  - name: app-config
    literals:
      - CACHE_TTL=3600
      - LOG_LEVEL=info

secretGenerator:
  - name: db-credentials
    literals:
      - DB_URL=postgresql://user:pass@db:5432/mydb

patchesStrategicMerge:
  - patches/replicas.yaml
"""

ArgoCD Python Client
import requests
import json
import time

class ArgoCDClient:
    """ArgoCD API client."""
    
    def __init__(self, server_url, username, password):
        self.server_url = server_url.rstrip('/')
        self.token = None
        self.authenticate(username, password)
    
    def authenticate(self, username, password):
        """Get JWT token."""
        response = requests.post(
            f'{self.server_url}/api/v1/session',
            json={'username': username, 'password': password},
            verify=False
        )
        self.token = response.json()['token']
    
    def _headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def list_applications(self):
        """List all applications."""
        response = requests.get(
            f'{self.server_url}/api/v1/applications',
            headers=self._headers(),
            verify=False
        )
        return response.json()['items']
    
    def get_application(self, name):
        """Get application details."""
        response = requests.get(
            f'{self.server_url}/api/v1/applications/{name}',
            headers=self._headers(),
            verify=False
        )
        return response.json()
    
    def sync_application(self, name, revision=None):
        """Sync application."""
        payload = {}
        if revision:
            payload['revision'] = revision
        
        response = requests.post(
            f'{self.server_url}/api/v1/applications/{name}/sync',
            headers=self._headers(),
            json=payload,
            verify=False
        )
        return response.json()
    
    def wait_for_sync(self, name, timeout=300):
        """Wait for application to sync."""
        start = time.time()
        while time.time() - start < timeout:
            app = self.get_application(name)
            status = app['status']['sync']['status']
            health = app['status']['health']['status']
            
            if status == 'Synced' and health == 'Healthy':
                return True
            
            time.sleep(5)
        
        return False

# Usage
# argocd = ArgoCDClient('https://argocd.example.com', 'admin', 'password')
# apps = argocd.list_applications()
# argocd.sync_application('web-app')
# argocd.wait_for_sync('web-app')

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Cloud-Native Patterns
# 12-Factor App:
# 1. Codebase: one codebase, many deploys
# 2. Dependencies: explicitly declare
# 3. Config: store in environment
# 4. Backing services: treat as attached resources
# 5. Build, release, run: strictly separate
# 6. Processes: stateless
# 7. Port binding: export services via port
# 8. Concurrency: scale out via processes
# 9. Disposability: fast startup, graceful shutdown
# 10. Dev/prod parity: keep environments similar
# 11. Logs: treat as event streams
# 12. Admin processes: run as one-off tasks

# Cloud-Native Computing Foundation (CNCF) projects:
# - Kubernetes: container orchestration
# - Prometheus: monitoring
# - Envoy: service proxy
# - Fluentd: log collection
# - Jaeger: distributed tracing
# - Helm: package manager
# - Istio: service mesh
# - ArgoCD: GitOps
# - Falco: runtime security

Security in Cloud (DevSecOps)
# Shift left security:
# - SAST: Static Application Security Testing
# - DAST: Dynamic Application Security Testing
# - SCA: Software Composition Analysis
# - Container scanning: Trivy, Clair
# - Infrastructure scanning: tfsec, checkov
# - Secret detection: git-secrets, trufflehog

# Example: Pre-commit hooks for security
"""
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
  
  - repo: https://github.com/returntocorp/semgrep
    rev: v1.50.0
    hooks:
      - id: semgrep
  
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
"""

Multi-Cloud Strategy
# Benefits:
# - Avoid vendor lock-in
# - Optimize costs
# - Improve resilience
# - Compliance requirements

# Challenges:
# - Complexity
# - Data transfer costs
# - Consistent tooling
# - Security across clouds

# Tools:
# - Terraform: multi-cloud IaC
# - Kubernetes: portable orchestration
# - Crossplane: cloud-agnostic control plane
# - Pulumi: infrastructure as code (multiple languages)

Recommended Reading
# - "The Phoenix Project" by Gene Kim
# - "The DevOps Handbook" by Gene Kim et al.
# - "Site Reliability Engineering" by Google
# - "Kubernetes Up & Running" by Kelsey Hightower
# - "Terraform: Up & Running" by Yevgeniy Brikman
# - "Designing Distributed Systems" by Brendan Burns

# Online Resources
# - Kubernetes documentation: https://kubernetes.io/docs/
# - Terraform documentation: https://www.terraform.io/docs
# - AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
# - CNCF Landscape: https://landscape.cncf.io/
# - DevOps Roadmap: https://roadmap.sh/devops

# End of Cloud Architecture & DevOps Reference