# Next.js App Router Complete Reference


---

# CHAPTER 1: PROJECT STRUCTURE

```
my-app/
├── app/
│   ├── layout.jsx         # Root layout (wraps all pages)
│   ├── page.jsx           # Home page (/)
│   ├── loading.jsx        # Loading UI
│   ├── error.jsx          # Error UI
│   ├── globals.css
│   ├── about/
│   │   └── page.jsx       # /about
│   ├── blog/
│   │   ├── page.jsx       # /blog
│   │   └── [slug]/
│   │       └── page.jsx   # /blog/my-post (dynamic route)
│   └── api/
│       └── users/
│           └── route.js   # API endpoint /api/users
├── components/
│   ├── Header.jsx
│   └── Footer.jsx
├── public/                 # Static files
├── next.config.js
└── package.json
```


## Pages and Layouts

```jsx
// app/layout.jsx — Root Layout (required)
export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>
                <Header />
                <main>{children}</main>
                <Footer />
            </body>
        </html>
    );
}

// app/page.jsx — Home Page
export default function Home() {
    return (
        <div>
            <h1>Welcome</h1>
            <p>This is the home page</p>
        </div>
    );
}

// app/about/page.jsx — About Page
export default function About() {
    return <h1>About Us</h1>;
}

// app/blog/[slug]/page.jsx — Dynamic Route
export default function BlogPost({ params }) {
    return <h1>Post: {params.slug}</h1>;
}
```


## Server Components vs Client Components

```jsx
// SERVER COMPONENT (default) — runs on server, no JavaScript sent to browser
// Can: fetch data, access database, read files, use secrets
// Cannot: use useState, useEffect, onClick, browser APIs
export default async function Users() {
    const users = await fetch('https://api.example.com/users').then(r => r.json());
    return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// CLIENT COMPONENT — runs in browser, add 'use client' at top
'use client';
import { useState } from 'react';

export default function Counter() {
    const [count, setCount] = useState(0);
    return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```


## API Routes

```javascript
// app/api/users/route.js
import { NextResponse } from 'next/server';

export async function GET() {
    const users = [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }];
    return NextResponse.json(users);
}

export async function POST(request) {
    const body = await request.json();
    return NextResponse.json({ id: 3, ...body }, { status: 201 });
}
```


## Data Fetching

```jsx
// Server Component — fetch directly (no useEffect needed!)
export default async function Products() {
    const products = await fetch('https://api.example.com/products', {
        cache: 'no-store',        // Always fresh (SSR)
        // cache: 'force-cache',  // Cache forever (SSG)
        // next: { revalidate: 60 }, // Revalidate every 60s (ISR)
    }).then(r => r.json());

    return (
        <div className="grid grid-cols-3 gap-4">
            {products.map(p => <ProductCard key={p.id} product={p} />)}
        </div>
    );
}
```


---

# CHAPTER 2: COMMON PITFALLS

```
PITFALL 1: Using useState in Server Components
  Server Components can't use hooks.
  Fix: add 'use client' at top of file, or extract interactive part into Client Component.

PITFALL 2: Fetching data in Client Components
  Using useEffect to fetch → slower, no SEO, loading flash.
  Fix: fetch in Server Component (default) — data is ready before page renders.

PITFALL 3: Importing server-only code in Client Components
  Database calls in 'use client' file → exposes secrets.
  Fix: keep DB/API calls in Server Components or API routes.

PITFALL 4: Not using loading.jsx
  Page takes 3 seconds to load → user sees blank page.
  Fix: add loading.jsx in the same folder → Next.js shows it automatically.
```