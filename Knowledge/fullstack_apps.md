# Full-Stack App Building Complete Reference


---

# CHAPTER 1: APP ARCHITECTURE PATTERNS


## Single Page Application (SPA)

```
Architecture:
  Browser loads ONE HTML page → JavaScript renders everything
  Navigation: URL changes but page never reloads
  
  Frontend (React/Vue/Angular)
       │ API calls (fetch/axios)
       ▼
  Backend (FastAPI/Express/Django)
       │ Database queries
       ▼
  Database (PostgreSQL/MongoDB)

Folder structure:
  myapp/
  ├── frontend/          # React/Vue
  │   ├── src/
  │   │   ├── components/
  │   │   ├── pages/
  │   │   ├── hooks/
  │   │   ├── utils/
  │   │   ├── api/       # API client functions
  │   │   ├── App.jsx
  │   │   └── main.jsx
  │   └── package.json
  ├── backend/           # FastAPI/Express
  │   ├── routes/
  │   ├── models/
  │   ├── middleware/
  │   ├── utils/
  │   └── server.py
  └── docker-compose.yml
```


## Complete Express.js Backend

```javascript
// server.js — Full Express backend
const express = require('express');
const cors = require('cors');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
app.use(cors());
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

// ─── DATABASE (in-memory for demo, use PostgreSQL in production) ───
let users = [];
let items = [];
let nextId = 1;

// ─── AUTH MIDDLEWARE ───
function auth(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token provided' });
    try {
        req.user = jwt.verify(token, JWT_SECRET);
        next();
    } catch(e) {
        res.status(401).json({ error: 'Invalid token' });
    }
}

// ─── AUTH ROUTES ───
app.post('/api/register', async (req, res) => {
    const { email, password, name } = req.body;
    if (!email || !password) return res.status(400).json({ error: 'Email and password required' });
    if (users.find(u => u.email === email)) return res.status(409).json({ error: 'Email exists' });

    const hash = await bcrypt.hash(password, 12);
    const user = { id: nextId++, email, name, password: hash, createdAt: new Date() };
    users.push(user);

    const token = jwt.sign({ id: user.id, email }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user.id, email, name } });
});

app.post('/api/login', async (req, res) => {
    const { email, password } = req.body;
    const user = users.find(u => u.email === email);
    if (!user || !(await bcrypt.compare(password, user.password))) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }
    const token = jwt.sign({ id: user.id, email }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ token, user: { id: user.id, email, name: user.name } });
});

// ─── CRUD ROUTES (protected) ───
app.get('/api/items', auth, (req, res) => {
    const userItems = items.filter(i => i.userId === req.user.id);
    res.json(userItems);
});

app.post('/api/items', auth, (req, res) => {
    const item = { id: nextId++, ...req.body, userId: req.user.id, createdAt: new Date() };
    items.push(item);
    res.status(201).json(item);
});

app.put('/api/items/:id', auth, (req, res) => {
    const item = items.find(i => i.id === parseInt(req.params.id) && i.userId === req.user.id);
    if (!item) return res.status(404).json({ error: 'Not found' });
    Object.assign(item, req.body, { updatedAt: new Date() });
    res.json(item);
});

app.delete('/api/items/:id', auth, (req, res) => {
    const idx = items.findIndex(i => i.id === parseInt(req.params.id) && i.userId === req.user.id);
    if (idx === -1) return res.status(404).json({ error: 'Not found' });
    items.splice(idx, 1);
    res.json({ success: true });
});

// ─── ERROR HANDLER ───
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

app.listen(3000, () => console.log('Server running on port 3000'));
```


## Complete FastAPI Backend

```python
# server.py — Full FastAPI backend
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import bcrypt

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SECRET = "your-secret-key"

# Models
class UserCreate(BaseModel):
    email: str
    password: str
    name: str = ""

class ItemCreate(BaseModel):
    title: str
    content: str = ""

# Database (use SQLAlchemy + PostgreSQL in production)
users_db = []
items_db = []
next_id = 1

# Auth
def get_current_user(authorization: str = ""):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Not authenticated")
    try:
        payload = jwt.decode(authorization[7:], SECRET, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

@app.post("/api/register")
def register(data: UserCreate):
    global next_id
    if any(u["email"] == data.email for u in users_db):
        raise HTTPException(409, "Email exists")
    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
    user = {"id": next_id, "email": data.email, "name": data.name, "password": hashed}
    users_db.append(user)
    next_id += 1
    token = jwt.encode({"id": user["id"], "email": data.email, "exp": datetime.utcnow() + timedelta(days=7)}, SECRET)
    return {"token": token, "user": {"id": user["id"], "email": data.email, "name": data.name}}

@app.post("/api/login")
def login(data: UserCreate):
    user = next((u for u in users_db if u["email"] == data.email), None)
    if not user or not bcrypt.checkpw(data.password.encode(), user["password"]):
        raise HTTPException(401, "Invalid credentials")
    token = jwt.encode({"id": user["id"], "email": data.email, "exp": datetime.utcnow() + timedelta(days=7)}, SECRET)
    return {"token": token, "user": {"id": user["id"], "email": data.email, "name": user["name"]}}

@app.get("/api/items")
def get_items(user=Depends(get_current_user)):
    return [i for i in items_db if i["user_id"] == user["id"]]

@app.post("/api/items")
def create_item(data: ItemCreate, user=Depends(get_current_user)):
    global next_id
    item = {"id": next_id, "title": data.title, "content": data.content, "user_id": user["id"], "created_at": datetime.utcnow().isoformat()}
    items_db.append(item)
    next_id += 1
    return item
```


---

# CHAPTER 2: FRONTEND PATTERNS


## React App with API Integration

```jsx
// App.jsx — Complete React CRUD app
import { useState, useEffect } from 'react';

const API = 'http://localhost:3000/api';

function App() {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [items, setItems] = useState([]);
    const [title, setTitle] = useState('');

    const headers = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` };

    useEffect(() => { if (token) fetchItems(); }, [token]);

    async function fetchItems() {
        const res = await fetch(`${API}/items`, { headers });
        if (res.ok) setItems(await res.json());
    }

    async function login(email, password) {
        const res = await fetch(`${API}/login`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        const data = await res.json();
        if (data.token) { localStorage.setItem('token', data.token); setToken(data.token); }
    }

    async function addItem() {
        if (!title.trim()) return;
        await fetch(`${API}/items`, { method: 'POST', headers, body: JSON.stringify({ title }) });
        setTitle('');
        fetchItems();
    }

    async function deleteItem(id) {
        await fetch(`${API}/items/${id}`, { method: 'DELETE', headers });
        fetchItems();
    }

    if (!token) return <LoginForm onLogin={login} />;

    return (
        <div style={{ maxWidth: 600, margin: '40px auto', padding: 20 }}>
            <h1>My App</h1>
            <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
                <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Add item..."
                    style={{ flex: 1, padding: 10, borderRadius: 8, border: '1px solid #ccc' }}
                    onKeyDown={e => e.key === 'Enter' && addItem()} />
                <button onClick={addItem} style={{ padding: '10px 20px', borderRadius: 8, background: '#6366f1', color: '#fff', border: 'none', cursor: 'pointer' }}>Add</button>
            </div>
            {items.map(item => (
                <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', padding: 12, borderBottom: '1px solid #eee' }}>
                    <span>{item.title}</span>
                    <button onClick={() => deleteItem(item.id)} style={{ color: 'red', background: 'none', border: 'none', cursor: 'pointer' }}>Delete</button>
                </div>
            ))}
        </div>
    );
}
```


## Complete Landing Page Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My App</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, sans-serif; color: #1a1a2e; }
        
        /* Hero */
        .hero { min-height: 100vh; display: flex; align-items: center; justify-content: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; padding: 20px; }
        .hero h1 { font-size: clamp(2rem, 5vw, 4rem); margin-bottom: 16px; }
        .hero p { font-size: 1.2rem; opacity: 0.9; max-width: 600px; margin: 0 auto 32px; }
        .hero-btn { display: inline-block; padding: 14px 32px; background: white; color: #667eea;
            border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; transition: transform 0.2s; }
        .hero-btn:hover { transform: translateY(-2px); }
        
        /* Features */
        .features { padding: 80px 20px; max-width: 1100px; margin: 0 auto; }
        .features h2 { text-align: center; font-size: 2rem; margin-bottom: 48px; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px; }
        .feature-card { padding: 32px; border-radius: 12px; border: 1px solid #e5e7eb; transition: box-shadow 0.2s; }
        .feature-card:hover { box-shadow: 0 4px 24px rgba(0,0,0,0.08); }
        .feature-card h3 { margin-bottom: 8px; }
        .feature-card p { color: #666; line-height: 1.6; }
        
        /* Footer */
        footer { background: #1a1a2e; color: white; text-align: center; padding: 40px 20px; }
    </style>
</head>
<body>
    <section class="hero">
        <div>
            <h1>Build Something Amazing</h1>
            <p>A modern platform to help you create, deploy, and scale your applications.</p>
            <a href="#features" class="hero-btn">Get Started</a>
        </div>
    </section>
    <section class="features" id="features">
        <h2>Features</h2>
        <div class="features-grid">
            <div class="feature-card">
                <h3>Fast</h3>
                <p>Built for speed with optimized rendering and lazy loading.</p>
            </div>
            <div class="feature-card">
                <h3>Secure</h3>
                <p>End-to-end encryption and industry-standard security practices.</p>
            </div>
            <div class="feature-card">
                <h3>Scalable</h3>
                <p>From prototype to millions of users without changing your stack.</p>
            </div>
        </div>
    </section>
    <footer><p>&copy; 2026 My App. All rights reserved.</p></footer>
</body>
</html>
```


---

# CHAPTER 3: COMMON APP PATTERNS


## Todo App Pattern

```javascript
// Universal todo pattern — works in any framework

// State
let todos = JSON.parse(localStorage.getItem('todos') || '[]');
let filter = 'all'; // all | active | completed

// Actions
function addTodo(text) {
    todos.push({ id: Date.now(), text, completed: false, createdAt: new Date() });
    save(); render();
}

function toggleTodo(id) {
    const todo = todos.find(t => t.id === id);
    if (todo) todo.completed = !todo.completed;
    save(); render();
}

function deleteTodo(id) {
    todos = todos.filter(t => t.id !== id);
    save(); render();
}

function editTodo(id, text) {
    const todo = todos.find(t => t.id === id);
    if (todo) todo.text = text;
    save(); render();
}

function clearCompleted() {
    todos = todos.filter(t => !t.completed);
    save(); render();
}

// Computed
function filteredTodos() {
    if (filter === 'active') return todos.filter(t => !t.completed);
    if (filter === 'completed') return todos.filter(t => t.completed);
    return todos;
}

function save() { localStorage.setItem('todos', JSON.stringify(todos)); }
```


## Dashboard Layout Pattern

```css
/* Dashboard grid layout */
.dashboard {
    display: grid;
    grid-template-columns: 250px 1fr;
    grid-template-rows: 60px 1fr;
    grid-template-areas:
        "sidebar header"
        "sidebar main";
    height: 100vh;
}

.dash-header {
    grid-area: header;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 24px; border-bottom: 1px solid #e5e7eb;
}

.dash-sidebar {
    grid-area: sidebar;
    background: #1a1a2e; color: white;
    padding: 20px 0;
    overflow-y: auto;
}

.dash-main {
    grid-area: main;
    padding: 24px;
    overflow-y: auto;
    background: #f5f5f7;
}

/* Stats cards */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px; margin-bottom: 24px;
}

.stat-card {
    background: white; padding: 20px; border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.stat-card .label { font-size: 13px; color: #888; }
.stat-card .value { font-size: 28px; font-weight: 700; margin-top: 4px; }

/* Responsive: collapse sidebar on mobile */
@media (max-width: 768px) {
    .dashboard { grid-template-columns: 1fr; grid-template-areas: "header" "main"; }
    .dash-sidebar { display: none; }
}
```