# React Hooks and Modern Patterns Complete Reference


---

# CHAPTER 1: ALL HOOKS


## useState — State Management

```jsx
import { useState } from 'react';

// Basic
const [count, setCount] = useState(0);
setCount(count + 1);
setCount(prev => prev + 1);  // Functional update (safer)

// Object state
const [form, setForm] = useState({ name: '', email: '' });
setForm(prev => ({ ...prev, name: 'Alice' }));  // Merge, don't replace

// Array state
const [items, setItems] = useState([]);
setItems(prev => [...prev, newItem]);           // Add
setItems(prev => prev.filter(i => i.id !== id)); // Remove
setItems(prev => prev.map(i => i.id === id ? { ...i, done: true } : i)); // Update

// Lazy initialization (expensive computation)
const [data, setData] = useState(() => computeExpensiveValue());
```


## useEffect — Side Effects

```jsx
import { useEffect } from 'react';

// Run on every render
useEffect(() => { console.log('rendered'); });

// Run once (mount)
useEffect(() => { fetchData(); }, []);

// Run when dependency changes
useEffect(() => { fetchUser(userId); }, [userId]);

// Cleanup (unmount or before re-run)
useEffect(() => {
    const timer = setInterval(() => tick(), 1000);
    return () => clearInterval(timer);  // Cleanup!
}, []);

// Fetch data pattern
useEffect(() => {
    let cancelled = false;
    async function load() {
        const res = await fetch('/api/users');
        const data = await res.json();
        if (!cancelled) setUsers(data);
    }
    load();
    return () => { cancelled = true; };
}, []);
```


## useRef — Persistent References

```jsx
import { useRef } from 'react';

// DOM reference
const inputRef = useRef(null);
<input ref={inputRef} />
inputRef.current.focus();

// Mutable value that doesn't trigger re-render
const renderCount = useRef(0);
useEffect(() => { renderCount.current += 1; });

// Previous value
function usePrevious(value) {
    const ref = useRef();
    useEffect(() => { ref.current = value; }, [value]);
    return ref.current;
}
```


## useMemo & useCallback — Performance

```jsx
import { useMemo, useCallback } from 'react';

// useMemo: cache computed value
const filtered = useMemo(() => {
    return items.filter(i => i.name.includes(search));
}, [items, search]);  // Recompute only when items or search change

// useCallback: cache function reference
const handleClick = useCallback((id) => {
    setItems(prev => prev.filter(i => i.id !== id));
}, []);  // Function identity stays stable
```


## Custom Hooks

```jsx
// useLocalStorage
function useLocalStorage(key, initial) {
    const [value, setValue] = useState(() => {
        const saved = localStorage.getItem(key);
        return saved !== null ? JSON.parse(saved) : initial;
    });
    useEffect(() => { localStorage.setItem(key, JSON.stringify(value)); }, [key, value]);
    return [value, setValue];
}

// useFetch
function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        let cancelled = false;
        setLoading(true);
        fetch(url).then(r => r.json()).then(d => { if (!cancelled) { setData(d); setLoading(false); } })
            .catch(e => { if (!cancelled) { setError(e); setLoading(false); } });
        return () => { cancelled = true; };
    }, [url]);
    return { data, loading, error };
}

// useDebounce
function useDebounce(value, delay = 300) {
    const [debounced, setDebounced] = useState(value);
    useEffect(() => {
        const timer = setTimeout(() => setDebounced(value), delay);
        return () => clearTimeout(timer);
    }, [value, delay]);
    return debounced;
}

// useToggle
function useToggle(initial = false) {
    const [value, setValue] = useState(initial);
    const toggle = useCallback(() => setValue(v => !v), []);
    return [value, toggle];
}
```


---

# CHAPTER 2: COMPONENT PATTERNS

```jsx
// Conditional rendering
function App({ isLoggedIn }) {
    return isLoggedIn ? <Dashboard /> : <Login />;
}

// List rendering
function List({ items }) {
    return <ul>{items.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}

// Loading / Error / Data pattern
function Users() {
    const { data, loading, error } = useFetch('/api/users');
    if (loading) return <Spinner />;
    if (error) return <Error message={error.message} />;
    return <UserList users={data} />;
}

// Controlled form
function Form() {
    const [form, setForm] = useState({ email: '', password: '' });
    const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });
    const handleSubmit = e => { e.preventDefault(); console.log(form); };
    return (
        <form onSubmit={handleSubmit}>
            <input name="email" value={form.email} onChange={handleChange} />
            <input name="password" type="password" value={form.password} onChange={handleChange} />
            <button type="submit">Login</button>
        </form>
    );
}
```