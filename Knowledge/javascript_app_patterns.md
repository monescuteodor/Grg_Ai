# JavaScript Application Patterns Reference


---

# CHAPTER 1: STATE MANAGEMENT


## Simple State Store (No Framework)

```javascript
// Minimal reactive state store — works anywhere
function createStore(initialState) {
    let state = { ...initialState };
    const listeners = [];

    return {
        getState() { return { ...state }; },
        setState(updates) {
            state = { ...state, ...updates };
            listeners.forEach(fn => fn(state));
        },
        subscribe(fn) {
            listeners.push(fn);
            return () => listeners.splice(listeners.indexOf(fn), 1);
        }
    };
}

// Usage
const store = createStore({ count: 0, user: null, items: [] });

// Subscribe to changes
store.subscribe(state => {
    document.getElementById('count').textContent = state.count;
    document.getElementById('items').innerHTML = state.items.map(i => '<li>' + i + '</li>').join('');
});

// Update state
store.setState({ count: store.getState().count + 1 });
store.setState({ items: [...store.getState().items, 'New item'] });
```


## Client-Side Router (No Library)

```javascript
// Simple hash router — no library needed
const routes = {
    '/': () => '<h1>Home</h1><p>Welcome!</p>',
    '/about': () => '<h1>About</h1><p>About us page</p>',
    '/contact': () => '<h1>Contact</h1><form><input placeholder="Email"><button>Send</button></form>',
    '/404': () => '<h1>404</h1><p>Page not found</p>',
};

function router() {
    const path = location.hash.slice(1) || '/';
    const render = routes[path] || routes['/404'];
    document.getElementById('app').innerHTML = render();
}

window.addEventListener('hashchange', router);
window.addEventListener('load', router);

// Navigate: <a href="#/about">About</a>
// Or: location.hash = '#/about';
```


## Fetch Wrapper with Error Handling

```javascript
// API client with auth, errors, retry
const api = {
    baseURL: '/api',
    token: localStorage.getItem('token'),

    async request(method, path, body) {
        const headers = { 'Content-Type': 'application/json' };
        if (this.token) headers['Authorization'] = 'Bearer ' + this.token;

        try {
            const res = await fetch(this.baseURL + path, {
                method,
                headers,
                body: body ? JSON.stringify(body) : undefined,
            });

            if (res.status === 401) {
                this.token = null;
                localStorage.removeItem('token');
                location.hash = '#/login';
                throw new Error('Session expired');
            }

            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.error || 'Request failed: ' + res.status);
            }

            return await res.json();
        } catch (e) {
            if (e.name === 'TypeError') throw new Error('Network error — check your connection');
            throw e;
        }
    },

    get(path) { return this.request('GET', path); },
    post(path, body) { return this.request('POST', path, body); },
    put(path, body) { return this.request('PUT', path, body); },
    delete(path) { return this.request('DELETE', path); },
};

// Usage
const items = await api.get('/items');
const newItem = await api.post('/items', { title: 'Hello' });
await api.delete('/items/5');
```


---

# CHAPTER 2: DOM UTILITIES


## Common DOM Helpers

```javascript
// Query shorthand
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

// Create element with attributes and children
function el(tag, attrs = {}, ...children) {
    const element = document.createElement(tag);
    for (const [key, val] of Object.entries(attrs)) {
        if (key === 'class') element.className = val;
        else if (key === 'style' && typeof val === 'object') Object.assign(element.style, val);
        else if (key.startsWith('on')) element.addEventListener(key.slice(2).toLowerCase(), val);
        else element.setAttribute(key, val);
    }
    for (const child of children) {
        if (typeof child === 'string') element.appendChild(document.createTextNode(child));
        else if (child) element.appendChild(child);
    }
    return element;
}

// Usage
document.body.appendChild(
    el('div', { class: 'card' },
        el('h2', {}, 'Title'),
        el('p', {}, 'Description'),
        el('button', { onClick: () => alert('Clicked!') }, 'Click me')
    )
);

// Debounce (for search input)
function debounce(fn, ms = 300) {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), ms);
    };
}

// Throttle (for scroll events)
function throttle(fn, ms = 100) {
    let throttled = false;
    return function(...args) {
        if (throttled) return;
        fn.apply(this, args);
        throttled = true;
        setTimeout(() => { throttled = false; }, ms);
    };
}

// Intersection Observer (lazy load / animate on scroll)
function onVisible(selector, callback) {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                callback(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    document.querySelectorAll(selector).forEach(el => observer.observe(el));
}

// Usage: fade in elements when they scroll into view
onVisible('.fade-in', el => el.classList.add('visible'));
```


---

# CHAPTER 3: LOCAL STORAGE PATTERNS

```javascript
// Type-safe localStorage wrapper
const storage = {
    get(key, fallback = null) {
        try {
            const val = localStorage.getItem(key);
            return val !== null ? JSON.parse(val) : fallback;
        } catch { return fallback; }
    },
    set(key, value) {
        localStorage.setItem(key, JSON.stringify(value));
    },
    remove(key) {
        localStorage.removeItem(key);
    },
    clear() {
        localStorage.clear();
    }
};

// Usage
storage.set('user', { name: 'Alice', theme: 'dark' });
const user = storage.get('user', { name: 'Guest' });
storage.set('todos', [{ text: 'Buy milk', done: false }]);
```