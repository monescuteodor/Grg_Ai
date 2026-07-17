# CI/CD Pipelines Complete Reference


---

# CHAPTER 1: FUNDAMENTALS


## Remarks

CI/CD (Continuous Integration / Continuous Deployment) automates building, testing, and deploying code. Every push to git triggers an automated pipeline that catches bugs before they reach production. Used by every professional software team.


## GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml

      - name: Lint
        run: |
          pip install ruff
          ruff check .

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_TOKEN }} | docker login -u ${{ secrets.DOCKER_USER }} --password-stdin
          docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to server
        run: |
          ssh deploy@server "docker pull myapp:${{ github.sha }} && docker-compose up -d"
```


## GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - pytest tests/ -v

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t registry.gitlab.com/myapp:$CI_COMMIT_SHA .
    - docker push registry.gitlab.com/myapp:$CI_COMMIT_SHA

deploy:
  stage: deploy
  only:
    - main
  script:
    - ssh deploy@server "docker pull && docker-compose up -d"
```


---

# CHAPTER 2: DOCKER IN CI/CD


## Dockerfile Best Practices

```dockerfile
# Multi-stage build (small final image)
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

# .dockerignore
# venv/
# __pycache__/
# .git/
# *.pyc
# .env
```


---

# CHAPTER 3: COMMON PITFALLS

```
PITFALL 1: No caching in CI
  pip install runs every time → 5min wasted per build.
  Fix: cache dependencies between runs.

PITFALL 2: Running tests only on main
  Bugs caught too late → broken main branch.
  Fix: run tests on EVERY pull request.

PITFALL 3: Secrets in code
  API keys committed to git → security breach.
  Fix: use CI secrets/environment variables, never hardcode.

PITFALL 4: No staging environment
  Deploy directly to production → bugs hit users.
  Fix: deploy to staging first, test, then promote to prod.

PITFALL 5: Ignoring failing tests
  "Just merge it, tests are flaky" → bugs accumulate.
  Fix: fix flaky tests immediately. Tests must be reliable.

PITFALL 6: No rollback plan
  Bad deploy → site down, no way to revert.
  Fix: keep previous Docker images, automate rollback.
```