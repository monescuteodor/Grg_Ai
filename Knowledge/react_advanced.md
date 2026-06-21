# React Advanced Reference


---

# CHAPTER 1: GETTING STARTED WITH REACT


## Remarks

React is a JavaScript library by Meta for building user interfaces. It introduced component-based architecture, virtual DOM diffing, and unidirectional data flow. Used by Facebook, Instagram, Netflix, Airbnb, Discord, Uber.

Modern React (18+) is built on **Fiber reconciler** with concurrent rendering. Key concepts: **functional components** (default), **hooks** (state and lifecycle), **JSX** (HTML-like syntax compiled to JS), **virtual DOM** (in-memory representation diffed against real DOM).

Tools: Vite (fastest dev server), Create React App (legacy), React DevTools (browser extension), TypeScript (strongly recommended), ESLint with eslint-plugin-react-hooks.


## Project Setup

```bash
# Vite (recommended - fast HMR)
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev

# Next.js (full-stack framework)
npx create-next-app@latest my-app --typescript --tailwind --app

# Build
npm run build      # → dist/ folder
npm run preview    # Test production build locally
```


## Hello World

```tsx
// src/App.tsx
import { useState } from 'react';

function App() {
  const [count, setCount] = useState<number>(0);

  return (
    <div>
      <h1>Hello, React!</h1>
      <button onClick={() => setCount(c => c + 1)}>
        Clicked {count} times
      </button>
    </div>
  );
}

export default App;

// src/main.tsx (entry point)
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```


---

# CHAPTER 2: BUILT-IN HOOKS


## useState — Local Component State

```tsx
import { useState } from 'react';

function Counter() {
  // Simple state
  const [count, setCount] = useState<number>(0);

  // Object state - ALWAYS create new object (immutable update)
  const [user, setUser] = useState({ name: 'Alice', age: 30 });

  // BAD - mutates state directly
  // user.age = 31;
  // setUser(user);   // React won't re-render (same reference)

  // GOOD - new object via spread
  setUser({ ...user, age: 31 });

  // Functional update - use when new state depends on previous
  setCount(prev => prev + 1);

  // Lazy initial state - expensive computation runs only once
  const [items, setItems] = useState<Item[]>(() => {
    return expensiveLoadFromStorage();   // Runs only on first render
  });

  return <div>{count}</div>;
}
```


## useEffect — Side Effects

```tsx
import { useEffect, useState } from 'react';

function Profile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  // Run on mount + when userId changes
  useEffect(() => {
    let cancelled = false;

    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(data => {
        if (!cancelled) setUser(data);   // Prevents race condition
      });

    // Cleanup runs BEFORE next effect or on unmount
    return () => {
      cancelled = true;
    };
  }, [userId]);

  // Mount only (empty deps)
  useEffect(() => {
    console.log('Mounted');
    return () => console.log('Unmounted');
  }, []);

  // Every render (no deps) - usually wrong, avoid this
  useEffect(() => {
    console.log('Every render');
  });

  // Setting up subscriptions
  useEffect(() => {
    const subscription = pubSub.subscribe('event', handleEvent);
    return () => subscription.unsubscribe();
  }, []);

  return <div>{user?.name}</div>;
}
```


## useReducer — Complex State Logic

```tsx
import { useReducer } from 'react';

interface State {
  count: number;
  history: number[];
  error: string | null;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'set'; payload: number }
  | { type: 'reset' }
  | { type: 'error'; message: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return {
        ...state,
        count: state.count + 1,
        history: [...state.history, state.count + 1],
        error: null,
      };
    case 'decrement':
      if (state.count <= 0) {
        return { ...state, error: 'Cannot go below zero' };
      }
      return {
        ...state,
        count: state.count - 1,
        history: [...state.history, state.count - 1],
      };
    case 'set':
      return { ...state, count: action.payload, history: [action.payload] };
    case 'reset':
      return { count: 0, history: [], error: null };
    case 'error':
      return { ...state, error: action.message };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, {
    count: 0,
    history: [],
    error: null,
  });

  return (
    <div>
      <p>Count: {state.count}</p>
      <p>History: {state.history.join(', ')}</p>
      {state.error && <p style={{ color: 'red' }}>{state.error}</p>}

      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'set', payload: 100 })}>Set 100</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```


## useRef — Mutable References Without Re-render

```tsx
import { useRef, useEffect } from 'react';

function VideoPlayer() {
  // Ref to DOM element
  const videoRef = useRef<HTMLVideoElement>(null);

  // Ref to mutable value (does NOT trigger re-render)
  const playCountRef = useRef<number>(0);
  const isFirstRenderRef = useRef<boolean>(true);

  useEffect(() => {
    if (isFirstRenderRef.current) {
      isFirstRenderRef.current = false;
      return;   // Skip first render
    }
    // Run only on updates
    console.log('Updated, not mounted');
  });

  const handlePlay = () => {
    videoRef.current?.play();
    playCountRef.current += 1;   // No re-render
    console.log('Played:', playCountRef.current);
  };

  return (
    <div>
      <video ref={videoRef} src="/video.mp4" />
      <button onClick={handlePlay}>Play</button>
    </div>
  );
}

// Forwarding refs to custom components
import { forwardRef } from 'react';

interface InputProps {
  placeholder?: string;
}

const FancyInput = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} className="fancy" />
));

function Form() {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <>
      <FancyInput ref={inputRef} placeholder="Enter name" />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
    </>
  );
}
```


## useMemo and useCallback — Memoization

```tsx
import { useMemo, useCallback, useState, memo } from 'react';

function ExpensiveList({ items, filter }: { items: Item[]; filter: string }) {
  // useMemo - cache computed value, recompute only when deps change
  const filtered = useMemo(() => {
    console.log('Filtering...');
    return items.filter(item => item.name.toLowerCase().includes(filter.toLowerCase()));
  }, [items, filter]);

  // useMemo for derived stats
  const stats = useMemo(() => {
    const total = filtered.reduce((s, i) => s + i.price, 0);
    return {
      count: filtered.length,
      total,
      avg: filtered.length > 0 ? total / filtered.length : 0,
    };
  }, [filtered]);

  return (
    <div>
      <p>Showing {stats.count} items, avg ${stats.avg.toFixed(2)}</p>
      <ul>
        {filtered.map(item => <li key={item.id}>{item.name}</li>)}
      </ul>
    </div>
  );
}

// useCallback - cache function reference (use with memo'd children)
function Parent() {
  const [count, setCount] = useState(0);
  const [filter, setFilter] = useState('');

  // BAD - new function every render, breaks memo
  // const handleClick = (id: string) => console.log('Click', id);

  // GOOD - stable reference
  const handleClick = useCallback((id: string) => {
    console.log('Click', id);
  }, []);   // No dependencies = same reference forever

  // With dependencies - new only when count changes
  const handleSubmit = useCallback((value: string) => {
    console.log(`Submit ${value} with count ${count}`);
  }, [count]);

  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      <input value={filter} onChange={e => setFilter(e.target.value)} />
      <MemoizedChild onClick={handleClick} onSubmit={handleSubmit} />
    </>
  );
}

const MemoizedChild = memo(({ onClick, onSubmit }: Props) => {
  console.log('Child render');
  return <div>...</div>;
});
```


## useContext — Avoiding Prop Drilling

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface Theme {
  mode: 'light' | 'dark';
  toggle: () => void;
}

const ThemeContext = createContext<Theme | undefined>(undefined);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  const toggle = () => setMode(m => m === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ mode, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Custom hook with error handling
export function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
}

// Usage anywhere in tree
function ThemeToggle() {
  const { mode, toggle } = useTheme();
  return <button onClick={toggle}>Mode: {mode}</button>;
}

// App.tsx
function App() {
  return (
    <ThemeProvider>
      <DeepComponent />   {/* Can access theme without prop drilling */}
    </ThemeProvider>
  );
}
```


---

# CHAPTER 3: ADVANCED HOOKS


## useTransition — Non-Blocking Updates

```tsx
import { useTransition, useState } from 'react';

function SearchableList({ items }: { items: Item[] }) {
  const [query, setQuery] = useState('');
  const [filtered, setFiltered] = useState(items);
  const [isPending, startTransition] = useTransition();

  const handleChange = (value: string) => {
    setQuery(value);   // Urgent - update input immediately

    // Mark as non-urgent - React can interrupt for higher priority
    startTransition(() => {
      const result = items.filter(item =>
        item.name.toLowerCase().includes(value.toLowerCase())
      );
      setFiltered(result);
    });
  };

  return (
    <>
      <input
        value={query}
        onChange={e => handleChange(e.target.value)}
        placeholder="Search..."
      />
      {isPending && <p>Filtering...</p>}
      <List items={filtered} />
    </>
  );
}

// When to use useTransition:
// - Tab switching with expensive content
// - Search with large datasets
// - Routing transitions
// - Heavy computation in render
```


## useDeferredValue — Lazy Value Updates

```tsx
import { useDeferredValue, useMemo } from 'react';

function SearchResults({ query }: { query: string }) {
  // Use a "stale" version of query while a fresh one is processing
  const deferredQuery = useDeferredValue(query);

  // Heavy computation uses deferred value
  const results = useMemo(() => {
    return expensiveSearch(deferredQuery);
  }, [deferredQuery]);

  // Visual feedback when stale
  const isStale = query !== deferredQuery;

  return (
    <div style={{ opacity: isStale ? 0.5 : 1 }}>
      {results.map(r => <Result key={r.id} {...r} />)}
    </div>
  );
}

// Difference from useTransition:
// - useTransition: you control the update timing inside startTransition
// - useDeferredValue: React decides when to update based on priority
```


## useId — Stable Unique IDs

```tsx
import { useId } from 'react';

function FormField({ label }: { label: string }) {
  const id = useId();   // Unique, stable across server/client
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input id={id} />
    </div>
  );
}

// Multiple IDs from one useId
function PasswordField() {
  const id = useId();
  return (
    <>
      <label htmlFor={`${id}-password`}>Password</label>
      <input id={`${id}-password`} type="password" aria-describedby={`${id}-hint`} />
      <p id={`${id}-hint`}>Must be 8+ characters</p>
    </>
  );
}

// IMPORTANT: Don't use useId for list keys! Use stable IDs from data
```


## useSyncExternalStore — External Stores

```tsx
import { useSyncExternalStore } from 'react';

// Subscribing to browser APIs / external stores
function useWindowWidth() {
  return useSyncExternalStore(
    // Subscribe function
    (callback) => {
      window.addEventListener('resize', callback);
      return () => window.removeEventListener('resize', callback);
    },
    // Get current value
    () => window.innerWidth,
    // Server snapshot (for SSR)
    () => 1024   // Default width on server
  );
}

function ResponsiveLayout() {
  const width = useWindowWidth();
  return width < 768 ? <MobileLayout /> : <DesktopLayout />;
}

// Online/offline status
function useOnlineStatus() {
  return useSyncExternalStore(
    (callback) => {
      window.addEventListener('online', callback);
      window.addEventListener('offline', callback);
      return () => {
        window.removeEventListener('online', callback);
        window.removeEventListener('offline', callback);
      };
    },
    () => navigator.onLine,
    () => true
  );
}
```


## useImperativeHandle — Custom Ref API

```tsx
import { useImperativeHandle, forwardRef, useRef } from 'react';

interface CustomInputHandle {
  focus: () => void;
  clear: () => void;
  getValue: () => string;
}

const CustomInput = forwardRef<CustomInputHandle, { placeholder?: string }>(
  (props, ref) => {
    const inputRef = useRef<HTMLInputElement>(null);

    useImperativeHandle(ref, () => ({
      focus: () => inputRef.current?.focus(),
      clear: () => {
        if (inputRef.current) inputRef.current.value = '';
      },
      getValue: () => inputRef.current?.value ?? '',
    }), []);

    return <input ref={inputRef} {...props} />;
  }
);

// Parent uses custom API instead of raw DOM
function Parent() {
  const inputRef = useRef<CustomInputHandle>(null);

  return (
    <>
      <CustomInput ref={inputRef} placeholder="Type here" />
      <button onClick={() => inputRef.current?.focus()}>Focus</button>
      <button onClick={() => inputRef.current?.clear()}>Clear</button>
      <button onClick={() => console.log(inputRef.current?.getValue())}>Log</button>
    </>
  );
}
```


---

# CHAPTER 4: CUSTOM HOOKS


## Reusable Stateful Logic

```tsx
// useLocalStorage - sync state with localStorage
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(key: string, initial: T): [T, (value: T | ((prev: T) => T)) => void] {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initial;
    } catch {
      return initial;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
      console.error('Failed to save', e);
    }
  }, [key, value]);

  return [value, setValue];
}

// usePrevious - access previous value
import { useRef, useEffect } from 'react';

export function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T | undefined>(undefined);
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
}

// useDebounce - debounce rapidly-changing values
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debounced, setDebounced] = useState<T>(value);
  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  return debounced;
}

// useFetch - generic data fetching with cleanup
interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

export function useFetch<T>(url: string): FetchState<T> & { refetch: () => void } {
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: true,
    error: null,
  });
  const [trigger, setTrigger] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setState(s => ({ ...s, loading: true }));

    fetch(url)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        if (!cancelled) setState({ data, loading: false, error: null });
      })
      .catch(error => {
        if (!cancelled) setState({ data: null, loading: false, error });
      });

    return () => { cancelled = true; };
  }, [url, trigger]);

  return { ...state, refetch: () => setTrigger(t => t + 1) };
}

// useIntersection - detect when element enters viewport
import { useEffect, useState, RefObject } from 'react';

export function useIntersection(
  ref: RefObject<Element>,
  options: IntersectionObserverInit = {}
): boolean {
  const [isIntersecting, setIsIntersecting] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => setIsIntersecting(entry.isIntersecting),
      options
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [ref, options.root, options.rootMargin, options.threshold]);

  return isIntersecting;
}

// Usage - lazy-load images
function LazyImage({ src, alt }: { src: string; alt: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const visible = useIntersection(ref, { rootMargin: '100px' });

  return (
    <div ref={ref} style={{ minHeight: 200 }}>
      {visible && <img src={src} alt={alt} />}
    </div>
  );
}

// useEventListener - clean event handling
import { useEffect, useRef } from 'react';

export function useEventListener<K extends keyof WindowEventMap>(
  event: K,
  handler: (e: WindowEventMap[K]) => void,
  element: Window | Document = window
) {
  const savedHandler = useRef(handler);

  useEffect(() => { savedHandler.current = handler; }, [handler]);

  useEffect(() => {
    const listener = (e: Event) => savedHandler.current(e as WindowEventMap[K]);
    element.addEventListener(event, listener);
    return () => element.removeEventListener(event, listener);
  }, [event, element]);
}

// Usage
function KeyboardShortcuts() {
  useEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      console.log('Save shortcut');
    }
  });
  return null;
}
```


---

# CHAPTER 5: PERFORMANCE OPTIMIZATION


## React.memo — Skip Unnecessary Re-renders

```tsx
import { memo } from 'react';

// Component re-renders only when props change (shallow comparison)
const ExpensiveCard = memo(function ExpensiveCard({ user, onClick }: Props) {
  console.log('Render Card', user.id);

  return (
    <div onClick={() => onClick(user.id)}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </div>
  );
});

// Custom comparison for deep equality
const Chart = memo(
  function Chart({ data }: { data: number[] }) {
    return <svg>{/* render */}</svg>;
  },
  (prev, next) => {
    if (prev.data.length !== next.data.length) return false;
    return prev.data.every((v, i) => v === next.data[i]);
  }
);

// IMPORTANT: memo only helps if props are stable references
// Pair with useCallback / useMemo in parent

function Parent() {
  const [count, setCount] = useState(0);

  // BAD - new object every render breaks memo
  // <ExpensiveCard user={{ id: 1, name: 'X' }} />

  // GOOD - stable reference
  const user = useMemo(() => ({ id: 1, name: 'Alice', email: 'a@b.com' }), []);
  const handleClick = useCallback((id: number) => console.log(id), []);

  return (
    <>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      <ExpensiveCard user={user} onClick={handleClick} />
    </>
  );
}
```


## Virtualization for Long Lists

```tsx
// npm install @tanstack/react-virtual
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,   // Row height in pixels
    overscan: 5,              // Render 5 items above/below visible
  });

  return (
    <div ref={parentRef} style={{ height: 500, overflow: 'auto' }}>
      <div style={{
        height: `${rowVirtualizer.getTotalSize()}px`,
        width: '100%',
        position: 'relative',
      }}>
        {rowVirtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {items[virtualItem.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}

// Renders only ~10-15 DOM nodes even for 100,000 items
```


## Code Splitting with Lazy Loading

```tsx
import { lazy, Suspense } from 'react';

// Lazy-load components - separate bundle, loaded on demand
const AdminDashboard = lazy(() => import('./AdminDashboard'));
const Chart = lazy(() => import('./Chart'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Suspense>
  );
}

// Lazy with named export
const Modal = lazy(() =>
  import('./Modal').then(m => ({ default: m.Modal }))
);

// Preload on hover - import early but don't render yet
function Nav() {
  const preloadAdmin = () => import('./AdminDashboard');

  return (
    <a href="/admin" onMouseEnter={preloadAdmin}>
      Admin
    </a>
  );
}
```


## Profiling and Diagnosis

```tsx
// React DevTools Profiler - record render times in browser
// Look for:
// 1. Components rendering when they shouldn't (use memo + useCallback)
// 2. Components with long render times (use useMemo, virtualization, code split)
// 3. Wasted renders (props identical but still rendering)

// Programmatic profiling
import { Profiler } from 'react';

function onRender(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  if (actualDuration > 16) {  // Slower than 60fps frame
    console.warn(`Slow render in ${id}: ${actualDuration.toFixed(2)}ms`);
  }
}

function App() {
  return (
    <Profiler id="App" onRender={onRender}>
      <MyComponent />
    </Profiler>
  );
}
```


---

# CHAPTER 6: SUSPENSE AND CONCURRENT FEATURES


## Suspense for Data Fetching

```tsx
import { Suspense } from 'react';

// Suspense allows components to "wait" for something
function App() {
  return (
    <Suspense fallback={<Skeleton />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}

// With multiple boundaries - streaming UI
function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<StatsLoader />}>
        <Stats />
      </Suspense>

      <Suspense fallback={<ChartLoader />}>
        <RevenueChart />
      </Suspense>

      <Suspense fallback={<OrdersLoader />}>
        <RecentOrders />
      </Suspense>
    </div>
  );
}
// Each section streams in independently when ready
```


## Error Boundaries

```tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback: (error: Error, reset: () => void) => ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Caught error:', error, info);
    // Report to Sentry/etc
  }

  reset = () => this.setState({ hasError: false, error: null });

  render() {
    if (this.state.hasError && this.state.error) {
      return this.props.fallback(this.state.error, this.reset);
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary
  fallback={(error, reset) => (
    <div>
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Retry</button>
    </div>
  )}
>
  <App />
</ErrorBoundary>

// Combine with Suspense - one fallback for errors, another for loading
<ErrorBoundary fallback={<ErrorUI />}>
  <Suspense fallback={<Loading />}>
    <App />
  </Suspense>
</ErrorBoundary>
```


## Concurrent React Concepts

```tsx
// React 18+ runs in "concurrent mode" by default with createRoot

// Key behaviors:
// 1. Automatic batching - all state updates in event handlers batched
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  setItems(i => [...i, newItem]);
  // Triggers ONE re-render, not three (even across promises now)
}

// 2. Concurrent rendering - React can interrupt long renders
// Marks transitions as low priority (useTransition)
// User input is high priority

// 3. Suspense for SSR streaming
// Server can stream HTML for ready components first, deferred ones later

// useTransition example - smooth tab switching
function TabContainer() {
  const [tab, setTab] = useState<'home' | 'posts' | 'admin'>('home');
  const [isPending, startTransition] = useTransition();

  const selectTab = (newTab: typeof tab) => {
    startTransition(() => setTab(newTab));
  };

  return (
    <>
      <button onClick={() => selectTab('home')} disabled={isPending}>Home</button>
      <button onClick={() => selectTab('posts')} disabled={isPending}>Posts</button>
      <button onClick={() => selectTab('admin')} disabled={isPending}>Admin</button>

      {isPending && <p>Loading...</p>}

      <Suspense fallback={<Loading />}>
        {tab === 'home' && <Home />}
        {tab === 'posts' && <Posts />}
        {tab === 'admin' && <Admin />}
      </Suspense>
    </>
  );
}
```


---

# CHAPTER 7: FORMS AND VALIDATION


## React Hook Form + Zod

```tsx
// npm install react-hook-form zod @hookform/resolvers
import { useForm, SubmitHandler } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Schema validation
const SignupSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string()
    .min(8, 'At least 8 characters')
    .regex(/[A-Z]/, 'At least one uppercase letter')
    .regex(/[0-9]/, 'At least one number'),
  age: z.coerce.number().min(18, 'Must be 18+').max(120),
  terms: z.boolean().refine(v => v === true, 'You must accept terms'),
});

type SignupForm = z.infer<typeof SignupSchema>;

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isDirty },
    reset,
    watch,
  } = useForm<SignupForm>({
    resolver: zodResolver(SignupSchema),
    defaultValues: { email: '', age: 18, terms: false },
  });

  // Watch specific field
  const password = watch('password');

  const onSubmit: SubmitHandler<SignupForm> = async (data) => {
    try {
      await fetch('/api/signup', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      reset();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>
        Email:
        <input {...register('email')} />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </label>

      <label>
        Password:
        <input type="password" {...register('password')} />
        {errors.password && <span className="error">{errors.password.message}</span>}
      </label>

      <label>
        Age:
        <input type="number" {...register('age')} />
        {errors.age && <span className="error">{errors.age.message}</span>}
      </label>

      <label>
        <input type="checkbox" {...register('terms')} />
        I accept terms
        {errors.terms && <span className="error">{errors.terms.message}</span>}
      </label>

      <button type="submit" disabled={isSubmitting || !isDirty}>
        {isSubmitting ? 'Signing up...' : 'Sign Up'}
      </button>
    </form>
  );
}
```


## Controlled vs Uncontrolled

```tsx
// Controlled - React owns the value
function ControlledInput() {
  const [value, setValue] = useState('');
  return (
    <input
      value={value}
      onChange={e => setValue(e.target.value)}
    />
  );
}

// Uncontrolled - DOM owns the value, accessed via ref
function UncontrolledInput() {
  const ref = useRef<HTMLInputElement>(null);
  const handleSubmit = () => {
    console.log(ref.current?.value);
  };
  return (
    <>
      <input ref={ref} defaultValue="initial" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}

// When to use:
// - Controlled: when value affects other state, validation on change
// - Uncontrolled: for "submit-only" forms, file inputs (always uncontrolled)

// File input - always uncontrolled
function FileUpload() {
  const fileRef = useRef<HTMLInputElement>(null);
  const handleUpload = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    await fetch('/upload', { method: 'POST', body: formData });
  };
  return (
    <>
      <input ref={fileRef} type="file" accept="image/*" />
      <button onClick={handleUpload}>Upload</button>
    </>
  );
}
```


---

# CHAPTER 8: PATTERNS AND ARCHITECTURE


## Compound Components

```tsx
// Build flexible, composable components with related parts
import { createContext, useContext, useState, ReactNode } from 'react';

interface TabsContextType {
  active: string;
  setActive: (id: string) => void;
}

const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ children, defaultTab }: { children: ReactNode; defaultTab: string }) {
  const [active, setActive] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }: { children: ReactNode }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ id, children }: { id: string; children: ReactNode }) {
  const ctx = useContext(TabsContext)!;
  return (
    <button
      className={ctx.active === id ? 'active' : ''}
      onClick={() => ctx.setActive(id)}
    >
      {children}
    </button>
  );
}

function TabPanel({ id, children }: { id: string; children: ReactNode }) {
  const ctx = useContext(TabsContext)!;
  if (ctx.active !== id) return null;
  return <div className="tab-panel">{children}</div>;
}

// Attach as static properties
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage - clean, flexible API
<Tabs defaultTab="home">
  <Tabs.List>
    <Tabs.Tab id="home">Home</Tabs.Tab>
    <Tabs.Tab id="profile">Profile</Tabs.Tab>
    <Tabs.Tab id="settings">Settings</Tabs.Tab>
  </Tabs.List>

  <Tabs.Panel id="home"><HomeContent /></Tabs.Panel>
  <Tabs.Panel id="profile"><ProfileContent /></Tabs.Panel>
  <Tabs.Panel id="settings"><SettingsContent /></Tabs.Panel>
</Tabs>
```


## Render Props

```tsx
// Pass a function as children/prop to share logic
interface MouseTrackerProps {
  children: (pos: { x: number; y: number }) => ReactNode;
}

function MouseTracker({ children }: MouseTrackerProps) {
  const [pos, setPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handler = (e: MouseEvent) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);

  return <>{children(pos)}</>;
}

// Usage
<MouseTracker>
  {({ x, y }) => <div>Mouse at ({x}, {y})</div>}
</MouseTracker>

// Modern alternative: just use a custom hook
function useMousePosition() {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  useEffect(() => {
    const handler = (e: MouseEvent) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', handler);
    return () => window.removeEventListener('mousemove', handler);
  }, []);
  return pos;
}

function MouseDisplay() {
  const { x, y } = useMousePosition();
  return <div>Mouse at ({x}, {y})</div>;
}
```


## Higher-Order Components (HOC) — Legacy

```tsx
// HOCs wrap components to add functionality - mostly replaced by hooks
function withAuth<P extends object>(Component: React.ComponentType<P>) {
  return function AuthenticatedComponent(props: P) {
    const { user, loading } = useAuth();
    if (loading) return <Spinner />;
    if (!user) return <Redirect to="/login" />;
    return <Component {...props} />;
  };
}

const ProtectedDashboard = withAuth(Dashboard);

// Modern equivalent - just guard inline or with a hook
function Dashboard() {
  const { user, loading } = useAuth();
  if (loading) return <Spinner />;
  if (!user) return <Redirect to="/login" />;
  return <div>Dashboard content</div>;
}
```


---

# CHAPTER 9: TESTING


## Jest + React Testing Library

```tsx
// npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest jest-environment-jsdom

// Counter.tsx
import { useState } from 'react';

export function Counter({ initial = 0 }) {
  const [count, setCount] = useState(initial);
  return (
    <div>
      <p data-testid="count">{count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}

// Counter.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter', () => {
  it('renders with initial value', () => {
    render(<Counter initial={5} />);
    expect(screen.getByTestId('count')).toHaveTextContent('5');
  });

  it('increments when button clicked', async () => {
    const user = userEvent.setup();
    render(<Counter />);

    await user.click(screen.getByText('Increment'));
    await user.click(screen.getByText('Increment'));

    expect(screen.getByTestId('count')).toHaveTextContent('2');
  });

  it('resets to 0', async () => {
    const user = userEvent.setup();
    render(<Counter initial={10} />);

    await user.click(screen.getByText('Reset'));
    expect(screen.getByTestId('count')).toHaveTextContent('0');
  });
});
```


## Testing Async Components

```tsx
import { render, screen, waitFor } from '@testing-library/react';

// Mock fetch globally
global.fetch = jest.fn();

beforeEach(() => {
  (global.fetch as jest.Mock).mockReset();
});

it('loads user data', async () => {
  (global.fetch as jest.Mock).mockResolvedValue({
    ok: true,
    json: async () => ({ id: '1', name: 'Alice' }),
  });

  render(<UserProfile userId="1" />);

  // Wait for async update
  expect(await screen.findByText('Alice')).toBeInTheDocument();
});

it('shows error on fetch failure', async () => {
  (global.fetch as jest.Mock).mockResolvedValue({
    ok: false,
    status: 500,
  });

  render(<UserProfile userId="1" />);

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});

// Better: use MSW (Mock Service Worker) for API mocking
// npm install --save-dev msw
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({ id: params.id, name: 'Alice' });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```


## Testing Custom Hooks

```tsx
// npm install --save-dev @testing-library/react
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('starts at initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('increments', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });
    expect(result.current.count).toBe(1);

    act(() => {
      result.current.increment();
      result.current.increment();
    });
    expect(result.current.count).toBe(3);
  });
});
```


---

# CHAPTER 10: COMMON PITFALLS


## Frequent Bugs and Anti-Patterns

```tsx
// PITFALL 1: Stale closure in useEffect
function BadCounter() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    setInterval(() => {
      setCount(count + 1);   // count is always 0 - stale!
    }, 1000);
  }, []);
}

function GoodCounter() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const id = setInterval(() => {
      setCount(c => c + 1);   // Functional update - always current
    }, 1000);
    return () => clearInterval(id);   // Cleanup!
  }, []);
}

// PITFALL 2: Missing effect dependencies
function BadSearch({ query }: { query: string }) {
  useEffect(() => {
    fetch(`/api/search?q=${query}`).then(/*...*/);
  }, []);   // BUG - query missing, effect uses stale query
}

function GoodSearch({ query }: { query: string }) {
  useEffect(() => {
    fetch(`/api/search?q=${query}`).then(/*...*/);
  }, [query]);   // Re-runs when query changes
}

// PITFALL 3: Setting state during render
function BadComponent({ value }: { value: number }) {
  const [doubled, setDoubled] = useState(0);
  setDoubled(value * 2);   // BAD - infinite loop!
  return <div>{doubled}</div>;
}

function GoodComponent({ value }: { value: number }) {
  // Don't store derived state - compute it
  const doubled = value * 2;
  return <div>{doubled}</div>;
}

// PITFALL 4: Mutating state
function BadList() {
  const [items, setItems] = useState([1, 2, 3]);
  const addItem = () => {
    items.push(4);   // MUTATION - no re-render!
    setItems(items);
  };
}

function GoodList() {
  const [items, setItems] = useState([1, 2, 3]);
  const addItem = () => {
    setItems(prev => [...prev, 4]);   // New array
  };
}

// PITFALL 5: Key={index} when list reorders
function BadList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map((item, i) => (
        <li key={i}>   {/* Bad - causes wrong updates on reorder */}
          <input defaultValue={item.name} />
        </li>
      ))}
    </ul>
  );
}

function GoodList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>   {/* Stable ID */}
          <input defaultValue={item.name} />
        </li>
      ))}
    </ul>
  );
}

// PITFALL 6: Over-using context for everything
// Context re-renders EVERY consumer when value changes
// For large state, split into multiple contexts or use Zustand/Jotai

// BAD - single huge context
const AppContext = createContext({
  user: null,
  theme: 'light',
  cart: [],
  notifications: [],
  // ... many more
});

// GOOD - separate concerns
const UserContext = createContext(null);
const ThemeContext = createContext('light');
const CartContext = createContext([]);
// Or use external store - Zustand/Jotai/Redux

// PITFALL 7: Forgetting cleanup
function BadSubscription() {
  useEffect(() => {
    socket.connect();
    socket.on('msg', handleMsg);
    // BAD - no cleanup, memory leak
  }, []);
}

function GoodSubscription() {
  useEffect(() => {
    socket.connect();
    socket.on('msg', handleMsg);
    return () => {
      socket.off('msg', handleMsg);
      socket.disconnect();
    };
  }, []);
}

// PITFALL 8: useEffect for non-side-effects
function BadDerivedState({ a, b }: { a: number; b: number }) {
  const [sum, setSum] = useState(0);
  useEffect(() => {
    setSum(a + b);   // BAD - causes extra render
  }, [a, b]);
}

function GoodDerivedState({ a, b }: { a: number; b: number }) {
  const sum = a + b;   // Derived value - no useEffect needed
  // If expensive, use useMemo:
  // const sum = useMemo(() => expensive(a, b), [a, b]);
}
```
