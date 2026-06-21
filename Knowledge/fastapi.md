# FastAPI Advanced Reference


---

# CHAPTER 1: GETTING STARTED WITH FASTAPI


## Remarks

FastAPI is a modern Python web framework for building APIs with automatic OpenAPI/Swagger docs, type hints, and async support. Built on Starlette (ASGI) and Pydantic (validation). Performance comparable to Node.js / Go for I/O-heavy workloads. Used by Netflix, Uber, Microsoft, Anthropic.

Key features: automatic request validation from type hints, async/await native, dependency injection, automatic interactive docs at `/docs` and `/redoc`, WebSocket support, background tasks, OAuth2/JWT helpers.

Tools: Uvicorn (ASGI server), Gunicorn (process manager), Pydantic v2 (validation), SQLAlchemy 2.0 (ORM), Alembic (migrations), pytest + httpx (testing).


## Project Setup

```bash
# Create virtual env
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# Install
pip install fastapi[all] uvicorn[standard] sqlalchemy alembic pydantic-settings
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
pip install pytest httpx pytest-asyncio

# Run dev server with hot reload
uvicorn main:app --reload --port 8000

# Run production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Or with Gunicorn (better for production)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```


## Hello World

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API documentation",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/users/{user_id}")
async def get_user(user_id: int, q: str | None = None):
    return {"user_id": user_id, "q": q}

# Auto-generated docs:
# Swagger UI:  http://localhost:8000/docs
# ReDoc:       http://localhost:8000/redoc
# OpenAPI:     http://localhost:8000/openapi.json
```


---

# CHAPTER 2: ROUTING AND PATH OPERATIONS


## HTTP Methods and Path Parameters

```python
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Annotated

app = FastAPI()

# GET with path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Path validation with Annotated (Python 3.9+)
@app.get("/users/{user_id}")
async def get_user(
    user_id: Annotated[int, Path(ge=1, le=10000, description="User ID")],
):
    return {"user_id": user_id}

# Query parameters
@app.get("/search")
async def search(
    q: Annotated[str, Query(min_length=3, max_length=50)],
    skip: int = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    tags: list[str] = Query(default=[]),
):
    return {"q": q, "skip": skip, "limit": limit, "tags": tags}

# POST with request body
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(ge=0, le=150)
    bio: str | None = None

@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    return {"id": 1, **user.model_dump()}

# PUT - full update
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserCreate):
    return {"id": user_id, **user.model_dump()}

# PATCH - partial update
class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    bio: str | None = None

@app.patch("/users/{user_id}")
async def patch_user(user_id: int, updates: UserUpdate):
    update_data = updates.model_dump(exclude_unset=True)
    return {"id": user_id, "updated": update_data}

# DELETE
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    # Return None for 204
    return None
```


## APIRouter — Modular Organization

```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    if user_id > 100:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id}

# routers/posts.py
from fastapi import APIRouter

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/")
async def list_posts():
    return []

# main.py
from fastapi import FastAPI
from routers import users, posts

app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)

# Now we have:
# GET /users/
# GET /users/{user_id}
# GET /posts/
```


## Response Models and Status Codes

```python
from fastapi import FastAPI, status
from pydantic import BaseModel
from datetime import datetime

class UserDB(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str   # Sensitive!
    created_at: datetime

class UserPublic(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    # No password_hash - safe to return

@app.get(
    "/users/{user_id}",
    response_model=UserPublic,   # Only these fields returned
    status_code=status.HTTP_200_OK,
    responses={
        404: {"description": "User not found"},
        500: {"description": "Server error"},
    },
)
async def get_user(user_id: int) -> UserDB:
    # Even if we return DB object with password_hash,
    # response_model filters it out
    user = await db.fetch_user(user_id)
    return user

# Multiple response models with Union
from fastapi.responses import JSONResponse

@app.get("/items/{id}")
async def get_item(id: int):
    if id == 1:
        return JSONResponse(
            status_code=200,
            content={"id": 1, "name": "Item"}
        )
    return JSONResponse(
        status_code=404,
        content={"error": "Not found"}
    )
```


---

# CHAPTER 3: PYDANTIC V2 MODELS


## Advanced Validation

```python
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
from datetime import datetime, date
from typing import Annotated
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class UserCreate(BaseModel):
    # Basic types with validation
    username: Annotated[str, Field(min_length=3, max_length=20, pattern=r'^[a-zA-Z0-9_]+$')]
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]
    age: Annotated[int, Field(ge=13, le=120)]
    birthday: date
    role: UserRole = UserRole.USER
    tags: list[str] = Field(default_factory=list)

    # Field-level validator
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError('Must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Must contain digit')
        return v

    @field_validator('username')
    @classmethod
    def username_no_admin(cls, v: str) -> str:
        if v.lower() in ['admin', 'root', 'system']:
            raise ValueError('Username reserved')
        return v.lower()

    # Model-level validator (after all fields validated)
    @model_validator(mode='after')
    def check_adult(self):
        if self.role == UserRole.ADMIN and self.age < 18:
            raise ValueError('Admin must be 18+')
        return self

    # Configure model
    model_config = {
        "str_strip_whitespace": True,
        "use_enum_values": True,
        "json_schema_extra": {
            "example": {
                "username": "alice",
                "email": "alice@example.com",
                "password": "Secret123",
                "age": 25,
                "birthday": "1999-01-01",
                "role": "user",
                "tags": ["dev", "python"],
            }
        }
    }

# Nested models
class Address(BaseModel):
    street: str
    city: str
    zip_code: Annotated[str, Field(pattern=r'^\d{5}$')]
    country: str = "USA"

class UserWithAddress(BaseModel):
    name: str
    email: EmailStr
    addresses: list[Address] = []   # List of nested models

# Generic models
from typing import TypeVar, Generic
T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int

# Usage
@app.get("/users", response_model=PaginatedResponse[UserPublic])
async def list_users(page: int = 1, size: int = 20):
    users = await db.fetch_users(page, size)
    return PaginatedResponse(items=users, total=100, page=page, page_size=size)
```


## Serialization Controls

```python
from pydantic import BaseModel, Field, computed_field
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str = Field(exclude=True)   # Never serialized
    created_at: datetime
    updated_at: datetime | None = None

    # Computed field (derived from others)
    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.name} <{self.email}>"

# Serialization options
user.model_dump()                          # dict
user.model_dump_json()                     # JSON string
user.model_dump(exclude={'password_hash'}) # Exclude fields
user.model_dump(include={'id', 'name'})    # Only these
user.model_dump(exclude_none=True)         # Skip None values
user.model_dump(exclude_unset=True)        # Only fields set explicitly
user.model_dump(by_alias=True)             # Use field aliases

# Aliases for camelCase JSON ↔ snake_case Python
class UserAPI(BaseModel):
    user_id: int = Field(alias='userId')
    first_name: str = Field(alias='firstName')

    model_config = {"populate_by_name": True}  # Accept both names

# Now accepts both:
# {"userId": 1, "firstName": "Alice"}     - external API
# {"user_id": 1, "first_name": "Alice"}   - internal Python
```


---

# CHAPTER 4: DEPENDENCY INJECTION


## Reusable Dependencies

```python
from fastapi import Depends, HTTPException, status, Header
from typing import Annotated

# Simple dependency function
async def get_pagination(
    skip: int = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return {"skip": skip, "limit": limit}

@app.get("/items")
async def list_items(pagination: Annotated[dict, Depends(get_pagination)]):
    return {"pagination": pagination}

# Dependency with sub-dependencies
async def verify_token(
    authorization: Annotated[str, Header()] = "",
) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = authorization.replace("Bearer ", "")
    # Verify token here
    return token

async def get_current_user(
    token: Annotated[str, Depends(verify_token)]
) -> User:
    user = await db.fetch_user_by_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.get("/me")
async def read_me(user: Annotated[User, Depends(get_current_user)]):
    return user

# Class-based dependencies (stateful)
class Pagination:
    def __init__(
        self,
        skip: int = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 20,
    ):
        self.skip = skip
        self.limit = limit

@app.get("/items")
async def list_items(p: Annotated[Pagination, Depends()]):
    return {"skip": p.skip, "limit": p.limit}

# Dependency for entire router
from fastapi import APIRouter

admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_admin)],  # Applied to ALL routes
)

@admin_router.get("/users")
async def admin_list_users():
    # Already protected by verify_admin
    return []

# Use yield for setup/cleanup (like context manager)
async def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/users")
async def list_users(db: Annotated[Session, Depends(get_db_session)]):
    return db.query(User).all()
```


## Caching Dependencies

```python
from fastapi import Depends
from functools import lru_cache

# Settings loaded once per app
class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()   # Loaded only once

@app.get("/config")
async def show_config(settings: Annotated[Settings, Depends(get_settings)]):
    return {"debug": settings.debug}

# Dependencies cached per request by default
async def get_user(user_id: int) -> User:
    return await db.fetch(user_id)   # Called once per request, even if used multiple times

# Force fresh each time
@app.get("/items", dependencies=[Depends(get_user, use_cache=False)])
async def list_items(): ...
```


---

# CHAPTER 5: AUTHENTICATION AND AUTHORIZATION


## JWT Authentication

```python
# Install: pip install python-jose[cryptography] passlib[bcrypt] python-multipart
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "your-secret-key-here-min-32-chars"  # Use env var!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Password helpers
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# JWT helpers
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None

# Login endpoint
@app.post("/auth/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await db.fetch_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token)

# Get current user from token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.fetch_user_by_username(username)
    if not user:
        raise credentials_exception
    return user

# Role-based authorization
def require_role(role: str):
    async def dependency(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires {role} role"
            )
        return user
    return dependency

@app.get("/admin/dashboard")
async def admin_dashboard(
    admin: Annotated[User, Depends(require_role("admin"))]
):
    return {"message": f"Welcome admin {admin.username}"}

@app.get("/me")
async def read_me(user: Annotated[User, Depends(get_current_user)]):
    return user
```


## API Key Authentication

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader, APIKeyQuery

# Via header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: Annotated[str | None, Security(api_key_header)]) -> str:
    if not api_key:
        raise HTTPException(401, "Missing API key")

    # Check against DB
    valid = await db.is_valid_api_key(api_key)
    if not valid:
        raise HTTPException(401, "Invalid API key")

    return api_key

@app.get("/private")
async def private_endpoint(api_key: Annotated[str, Depends(get_api_key)]):
    return {"message": "authorized"}

# Via query parameter (less secure)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)
```


---

# CHAPTER 6: DATABASES WITH SQLALCHEMY 2.0


## Setup with Async SQLAlchemy

```python
# Install: pip install sqlalchemy[asyncio] asyncpg alembic
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=False)  # echo=True for SQL logs
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Base class
class Base(DeclarativeBase):
    pass

# Models with modern syntax (SQLAlchemy 2.0)
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship - one user has many posts
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    author: Mapped[User] = relationship(back_populates="posts")

# Dependency for getting session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```


## Query Patterns

```python
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload, joinedload

# Create
@app.post("/users")
async def create_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# Read by primary key
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

# Query with filters
@app.get("/users")
async def list_users(
    db: Annotated[AsyncSession, Depends(get_db)],
    active: bool | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    query = select(User)

    if active is not None:
        query = query.where(User.is_active == active)
    if search:
        query = query.where(User.username.ilike(f"%{search}%"))

    query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# Eager loading (avoid N+1 queries)
@app.get("/users/{user_id}/with-posts")
async def get_user_with_posts(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # selectinload - separate query (better for one-to-many)
    query = select(User).where(User.id == user_id).options(selectinload(User.posts))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    # joinedload - JOIN in same query (better for one-to-one or small sets)
    # query = select(User).options(joinedload(User.posts))
    return user

# Update
@app.patch("/users/{user_id}")
async def update_user(
    user_id: int,
    updates: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(400, "No fields to update")

    query = update(User).where(User.id == user_id).values(**update_data)
    result = await db.execute(query)
    if result.rowcount == 0:
        raise HTTPException(404, "User not found")

    await db.commit()
    return await db.get(User, user_id)

# Delete
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(delete(User).where(User.id == user_id))
    if result.rowcount == 0:
        raise HTTPException(404, "User not found")
    await db.commit()

# Aggregations
@app.get("/stats")
async def stats(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(
            func.count(User.id).label("total"),
            func.count(User.id).filter(User.is_active == True).label("active"),
        )
    )
    row = result.one()
    return {"total": row.total, "active": row.active}
```


---

# CHAPTER 7: BACKGROUND TASKS AND ASYNC


## BackgroundTasks for Simple Async Work

```python
from fastapi import BackgroundTasks
import smtplib
from email.message import EmailMessage

def send_email(to: str, subject: str, body: str):
    """Synchronous task - runs after response sent"""
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['To'] = to
    msg.set_content(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)

async def log_event(event: str):
    """Async task - also runs after response"""
    await db.insert_log(event)

@app.post("/users/register")
async def register(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
):
    user = await create_user(user_data)

    # These run AFTER response is sent to user (faster perceived latency)
    background_tasks.add_task(send_email, user.email, "Welcome!", "Hi!")
    background_tasks.add_task(log_event, f"User {user.id} registered")

    return {"message": "Registered", "user_id": user.id}

# Limitation: BackgroundTasks run in same process
# For heavy work, use Celery/RQ/ARQ instead
```


## Celery for Heavy Background Jobs

```python
# Install: pip install celery[redis] redis
# tasks.py
from celery import Celery

celery_app = Celery(
    'my_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_video(self, video_id: int):
    try:
        video = db.get_video(video_id)
        # Heavy work - transcoding, thumbnails, etc.
        result = transcode_video(video.file_path)
        db.update_video(video_id, status="processed", thumbnail=result.thumbnail)
        return {"status": "ok", "video_id": video_id}
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc)

@celery_app.task
def send_bulk_emails(user_ids: list[int], subject: str, body: str):
    for user_id in user_ids:
        user = db.get_user(user_id)
        if user.email:
            send_email(user.email, subject, body)

# In FastAPI endpoint
from tasks import process_video, send_bulk_emails

@app.post("/videos/upload")
async def upload_video(file: UploadFile):
    video = await save_video(file)

    # Queue for background processing
    task = process_video.delay(video.id)

    return {"video_id": video.id, "task_id": task.id, "status": "processing"}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "id": task_id,
        "status": task.status,
        "result": task.result if task.ready() else None,
    }

# Run Celery worker (separate process):
# celery -A tasks worker --loglevel=info
```


## ARQ — Lightweight Async Alternative

```python
# Install: pip install arq
# worker.py
from arq.connections import RedisSettings

async def process_data(ctx, data: dict):
    print(f"Processing {data}")
    # ... do work
    return {"result": "done"}

class WorkerSettings:
    functions = [process_data]
    redis_settings = RedisSettings()

# Run: arq worker.WorkerSettings

# In FastAPI
from arq import create_pool
from arq.connections import RedisSettings

@app.on_event("startup")
async def startup():
    app.state.redis = await create_pool(RedisSettings())

@app.post("/jobs")
async def queue_job(data: dict):
    job = await app.state.redis.enqueue_job('process_data', data)
    return {"job_id": job.job_id}
```


---

# CHAPTER 8: WEBSOCKETS AND STREAMING


## WebSocket Endpoints

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

# Simple echo
@app.websocket("/ws/echo")
async def websocket_echo(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# Chat room with broadcast
class ConnectionManager:
    def __init__(self):
        self.active: dict[str, list[WebSocket]] = {}   # room -> [connections]

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active:
            self.active[room] = []
        self.active[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str):
        if room in self.active:
            self.active[room].remove(websocket)
            if not self.active[room]:
                del self.active[room]

    async def broadcast(self, room: str, message: str, exclude: WebSocket | None = None):
        if room not in self.active:
            return
        for connection in self.active[room]:
            if connection != exclude:
                try:
                    await connection.send_text(message)
                except:
                    pass   # Will be cleaned up on next disconnect

manager = ConnectionManager()

@app.websocket("/ws/chat/{room}/{username}")
async def chat(websocket: WebSocket, room: str, username: str):
    await manager.connect(websocket, room)
    await manager.broadcast(room, f"{username} joined")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room, f"{username}: {data}", exclude=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(room, f"{username} left")

# WebSocket with auth
@app.websocket("/ws/private")
async def private_ws(
    websocket: WebSocket,
    token: str = Query(...),
):
    # Verify token before accepting
    try:
        user = await verify_jwt_token(token)
    except:
        await websocket.close(code=1008)   # Policy violation
        return

    await websocket.accept()
    await websocket.send_json({"user": user.username})

    try:
        while True:
            msg = await websocket.receive_json()
            # Process authenticated messages
    except WebSocketDisconnect:
        pass
```


## Server-Sent Events (SSE)

```python
# SSE - one-way streaming from server to client
# Simpler than WebSockets, works over HTTP/2
from fastapi.responses import StreamingResponse
import asyncio
import json

async def event_generator():
    counter = 0
    while True:
        counter += 1
        # SSE format: "data: <json>\n\n"
        yield f"data: {json.dumps({'count': counter, 'time': str(datetime.now())})}\n\n"
        await asyncio.sleep(1)

@app.get("/events/counter")
async def counter_stream():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )

# Streaming LLM response (like ChatGPT)
async def llm_stream(prompt: str):
    yield f"data: {json.dumps({'event': 'start'})}\n\n"

    async for token in llm_generate(prompt):
        yield f"data: {json.dumps({'token': token})}\n\n"

    yield f"data: {json.dumps({'event': 'done'})}\n\n"

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        llm_stream(request.message),
        media_type="text/event-stream",
    )

# Client (JavaScript):
# const evt = new EventSource('/events/counter');
# evt.onmessage = (e) => console.log(JSON.parse(e.data));
```


## File Uploads

```python
from fastapi import File, UploadFile
import shutil
import aiofiles
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Validate
    if file.size > 10 * 1024 * 1024:   # 10MB limit
        raise HTTPException(413, "File too large")
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Only images allowed")

    # Save async
    dest = UPLOAD_DIR / file.filename
    async with aiofiles.open(dest, "wb") as f:
        while chunk := await file.read(1024 * 1024):   # 1MB chunks
            await f.write(chunk)

    return {"filename": file.filename, "size": file.size}

# Multiple files
@app.post("/upload-multiple")
async def upload_multiple(files: list[UploadFile]):
    results = []
    for file in files:
        dest = UPLOAD_DIR / file.filename
        async with aiofiles.open(dest, "wb") as f:
            content = await file.read()
            await f.write(content)
        results.append({"filename": file.filename, "size": len(content)})
    return results

# Streaming download
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "File not found")

    async def file_generator():
        async with aiofiles.open(file_path, "rb") as f:
            while chunk := await f.read(1024 * 1024):
                yield chunk

    return StreamingResponse(
        file_generator(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```


---

# CHAPTER 9: MIDDLEWARE AND CORS


## Custom Middleware

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
import uuid

app = FastAPI()

# Built-in CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Gzip compression for responses > 1000 bytes
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middleware - request timing + logging
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()

    # Add request ID to logs
    request.state.request_id = request_id

    response = await call_next(request)

    duration = time.time() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    response.headers["X-Request-ID"] = request_id

    print(f"[{request_id}] {request.method} {request.url.path} {response.status_code} {duration*1000:.0f}ms")

    return response

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# Rate limiting with slowapi
# pip install slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/limited")
@limiter.limit("5/minute")
async def limited(request: Request):
    return {"message": "Slow down!"}
```


---

# CHAPTER 10: TESTING


## Pytest with httpx

```python
# conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from main import app, get_db, Base

# Test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture
async def db():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestSession = async_sessionmaker(engine, expire_on_commit=False)
    async with TestSession() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db):
    # Override DB dependency for tests
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

# test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "Secret123",
        "age": 25,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert "password" not in data   # Hashed, not returned

@pytest.mark.asyncio
async def test_get_user_not_found(client):
    response = await client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.asyncio
async def test_auth_required(client):
    response = await client.get("/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_and_access(client, db):
    # Setup - create user
    await client.post("/users", json={
        "username": "bob",
        "email": "bob@example.com",
        "password": "Secret123",
        "age": 30,
    })

    # Login
    login_resp = await client.post(
        "/auth/login",
        data={"username": "bob", "password": "Secret123"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Access protected route
    me_resp = await client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_resp.status_code == 200
    assert me_resp.json()["username"] == "bob"

# Parametrized tests
@pytest.mark.parametrize("username,expected_status", [
    ("ab", 422),         # Too short
    ("admin", 422),      # Reserved
    ("validuser", 201),  # OK
])
async def test_username_validation(client, username, expected_status):
    response = await client.post("/users", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "Secret123",
        "age": 25,
    })
    assert response.status_code == expected_status

# Test WebSocket
async def test_websocket(client):
    async with client.websocket_connect("/ws/echo") as ws:
        await ws.send_text("hello")
        msg = await ws.receive_text()
        assert msg == "Echo: hello"
```


## Common Pitfalls

```python
# PITFALL 1: Blocking I/O in async endpoints
@app.get("/bad")
async def bad_endpoint():
    time.sleep(5)   # BLOCKS entire event loop!
    return {"ok": True}

@app.get("/good")
async def good_endpoint():
    await asyncio.sleep(5)   # Non-blocking
    return {"ok": True}

@app.get("/cpu-bound")
def cpu_bound():   # Use sync def for CPU work - runs in threadpool
    result = expensive_calculation()
    return result

# PITFALL 2: Forgetting await on async functions
async def bad():
    user = db.fetch_user(1)   # Returns coroutine, not user!
    return user.name           # AttributeError

async def good():
    user = await db.fetch_user(1)
    return user.name

# PITFALL 3: Mutable default arguments
def bad(items: list = []):   # SHARED across calls!
    items.append("x")
    return items
# bad() returns ["x"]
# bad() returns ["x", "x"]  - WRONG!

def good(items: list | None = None):
    items = items or []
    items.append("x")
    return items

# PITFALL 4: Not validating file uploads
@app.post("/bad-upload")
async def bad_upload(file: UploadFile):
    # No size check, no type check - attacker can upload 10GB
    content = await file.read()
    return {"size": len(content)}

# PITFALL 5: Storing secrets in code
# BAD
SECRET_KEY = "hardcoded-key"

# GOOD - use environment variables
import os
SECRET_KEY = os.environ["SECRET_KEY"]   # Errors if missing

# Or with pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str

    model_config = {"env_file": ".env"}

settings = Settings()

# PITFALL 6: N+1 queries
@app.get("/bad-users-with-posts")
async def bad(db: Annotated[AsyncSession, Depends(get_db)]):
    users = (await db.execute(select(User))).scalars().all()
    for user in users:
        user.posts   # Triggers query PER USER - if 100 users, 101 queries!
    return users

@app.get("/good-users-with-posts")
async def good(db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(User).options(selectinload(User.posts))
    users = (await db.execute(query)).scalars().all()
    # Just 2 queries total - one for users, one for posts
    return users
```
