# Next.js Complete Reference (App Router)


---

# CHAPTER 1: GETTING STARTED WITH NEXT.JS


## Remarks

Next.js is a React framework by Vercel for full-stack web applications. It provides server-side rendering (SSR), static site generation (SSG), API routes, file-based routing, image optimization, and built-in CSS support. Used by TikTok, Twitch, Notion, Hulu, OpenAI, Anthropic.

**App Router** (Next.js 13+) is the modern paradigm — built on React Server Components, with native streaming, layouts, and async components. The legacy **Pages Router** (pages/) still works but is being phased out for new projects.

Tools: Next.js CLI (create-next-app), Vercel (hosting), Turbopack (faster bundler), SWC (Rust-based compiler).


## Project Setup

```bash
# Create new app (TypeScript, ESLint, Tailwind by default)
npx create-next-app@latest my-app --typescript --tailwind --eslint --app

# Common flags
# --app           App Router (recommended)
# --src-dir       Use src/ folder
# --import-alias  Custom @/ alias for imports

cd my-app
npm run dev       # Start dev server on localhost:3000

# Build for production
npm run build
npm run start     # Run production server
```


## Project Structure

```
my-app/
├── app/                    # App Router root
│   ├── layout.tsx          # Root layout (required)
│   ├── page.tsx            # Home page → /
│   ├── globals.css         # Global styles
│   ├── loading.tsx         # Loading UI
│   ├── error.tsx           # Error boundary
│   ├── not-found.tsx       # 404 page
│   ├── about/
│   │   └── page.tsx        # /about
│   ├── blog/
│   │   ├── page.tsx        # /blog
│   │   ├── [slug]/
│   │   │   └── page.tsx    # /blog/:slug
│   │   └── layout.tsx      # Layout for /blog/*
│   └── api/
│       └── users/
│           └── route.ts    # API endpoint /api/users
├── public/                 # Static files
├── components/             # Shared components
├── lib/                    # Utilities, DB clients
├── next.config.js
├── tailwind.config.ts
└── tsconfig.json
```


---

# CHAPTER 2: FILE-BASED ROUTING


## Pages and Layouts

```tsx
// app/layout.tsx - Root layout (wraps every page)
import './globals.css';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'My App',
  description: 'Built with Next.js',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}

// app/page.tsx - Home page (/)
export default function HomePage() {
  return <h1>Welcome to my site</h1>;
}

// app/about/page.tsx - About page (/about)
export default function AboutPage() {
  return <h1>About us</h1>;
}

// app/blog/layout.tsx - Nested layout (wraps all /blog/* routes)
export default function BlogLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="blog-container">
      <aside><BlogSidebar /></aside>
      <section>{children}</section>
    </div>
  );
}

// app/blog/[slug]/page.tsx - Dynamic route (/blog/anything)
interface Props {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}

export default async function BlogPost({ params, searchParams }: Props) {
  const { slug } = await params;            // Next.js 15+ params are async
  const { ref } = await searchParams;

  const post = await getPostBySlug(slug);
  if (!post) notFound();

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// app/products/[...all]/page.tsx - Catch-all route
// Matches /products/a, /products/a/b, /products/a/b/c
export default async function ProductsPage({ params }: { params: Promise<{ all: string[] }> }) {
  const { all } = await params;
  return <div>Path segments: {all.join('/')}</div>;
}

// app/(marketing)/about/page.tsx - Route groups (parentheses don't affect URL)
// (marketing) is ignored in URL - still /about
// Useful for organizing without URL nesting
```


## Special Files

```tsx
// app/loading.tsx - Shown during navigation (uses Suspense)
export default function Loading() {
  return (
    <div className="flex justify-center p-8">
      <div className="animate-spin">⏳</div>
    </div>
  );
}

// app/error.tsx - Error boundary (must be Client Component)
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="p-8 text-center">
      <h2>Something went wrong!</h2>
      <p className="text-gray-500">{error.message}</p>
      <button onClick={reset} className="mt-4 rounded bg-blue-500 px-4 py-2 text-white">
        Try again
      </button>
    </div>
  );
}

// app/not-found.tsx - 404 page
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="p-8 text-center">
      <h2>404 - Page not found</h2>
      <Link href="/" className="text-blue-500 underline">Go home</Link>
    </div>
  );
}

// Trigger 404 programmatically
import { notFound } from 'next/navigation';

if (!post) notFound();   // Renders not-found.tsx

// app/template.tsx - Like layout but recreated on navigation
// (loses state between routes, useful for animations)
```


## Navigation

```tsx
// Server-side - Link component (preferred)
import Link from 'next/link';

<Link href="/about">About</Link>
<Link href={`/blog/${post.slug}`} prefetch={true}>{post.title}</Link>

// With query params
<Link href={{ pathname: '/search', query: { q: 'next.js' } }}>Search</Link>

// Client-side imperative navigation
'use client';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';

function SearchBar() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const handleSearch = (query: string) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('q', query);
    router.push(`${pathname}?${params.toString()}`);
  };

  // Other methods
  // router.replace('/login')      - No history entry
  // router.back()                  - Go back
  // router.refresh()               - Re-fetch server data
  // router.prefetch('/dashboard')  - Preload route

  return <input onChange={e => handleSearch(e.target.value)} />;
}
```


---

# CHAPTER 3: SERVER COMPONENTS AND CLIENT COMPONENTS


## Default: Server Components

```tsx
// By default, all components in app/ are SERVER COMPONENTS
// They run on the server, never ship JS to client

// app/products/page.tsx
async function ProductsPage() {
  // Direct DB access - no fetch needed!
  const products = await db.product.findMany();

  return (
    <ul>
      {products.map(p => (
        <li key={p.id}>{p.name} - ${p.price}</li>
      ))}
    </ul>
  );
}

// BENEFITS:
// - Zero JS shipped to client for this component
// - Direct DB/API access without exposing keys
// - Smaller bundle, faster First Contentful Paint
// - Async/await directly in components

// LIMITATIONS - Server Components CANNOT:
// - Use useState, useEffect, useContext
// - Use browser APIs (window, document)
// - Use event handlers (onClick, onChange)
// - Import client-only libraries directly
```


## Client Components with 'use client'

```tsx
// 'use client' directive marks file as Client Component
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  // useState works here - this runs in browser

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Clicked {count} times
    </button>
  );
}

// IMPORTANT: 'use client' creates a "boundary"
// Everything imported into a Client Component becomes Client too
// So mark ONLY the leaves that need interactivity, not whole tree
```


## Composing Server and Client Components

```tsx
// app/page.tsx (Server Component)
import ClientCounter from './ClientCounter';
import ServerProductList from './ServerProductList';

export default async function HomePage() {
  const user = await getCurrentUser();

  return (
    <div>
      <h1>Welcome {user.name}</h1>
      {/* Client component for interactivity */}
      <ClientCounter />
      {/* Server component for data fetching */}
      <ServerProductList />
    </div>
  );
}

// PATTERN: Pass Server Components as children/props to Client Components
// This way, Server Component remains server-rendered

// app/Sidebar.tsx (Client)
'use client';

import { useState } from 'react';

export default function Sidebar({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(true);
  return (
    <aside className={open ? 'w-64' : 'w-12'}>
      <button onClick={() => setOpen(!open)}>Toggle</button>
      {/* children stays as Server Component! */}
      {children}
    </aside>
  );
}

// app/page.tsx (Server)
import Sidebar from './Sidebar';
import ServerWidget from './ServerWidget';  // Server component

export default function Page() {
  return (
    <Sidebar>
      <ServerWidget />  {/* Stays server-side! */}
    </Sidebar>
  );
}
```


---

# CHAPTER 4: DATA FETCHING


## Fetch in Server Components

```tsx
// Native fetch with automatic caching
async function getPosts() {
  // Cached by default until manually revalidated
  const res = await fetch('https://api.example.com/posts');
  if (!res.ok) throw new Error('Failed to fetch');
  return res.json();
}

// Force fresh data on every request (no cache)
const res = await fetch('https://api.example.com/data', {
  cache: 'no-store',
});

// Cache with revalidation (ISR-like)
const res = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 },   // Re-fetch every hour
});

// Cache with tags - manual invalidation
const res = await fetch('https://api.example.com/users', {
  next: { tags: ['users'] },
});

// Later, invalidate the tag:
import { revalidateTag } from 'next/cache';
revalidateTag('users');   // Force refetch on next request

// Page using fetched data
export default async function PostsPage() {
  const posts = await getPosts();

  return (
    <ul>
      {posts.map((post: Post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

// Parallel fetching - run requests concurrently
async function PostsAndComments() {
  // Both run in parallel
  const [posts, comments] = await Promise.all([
    getPosts(),
    getComments(),
  ]);

  return (
    <div>
      <PostList posts={posts} />
      <CommentList comments={comments} />
    </div>
  );
}
```


## Streaming with Suspense

```tsx
// Long-running data fetches can stream in independently
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Renders immediately */}
      <UserHeader />

      {/* Streams in when ready, shows fallback meanwhile */}
      <Suspense fallback={<RevenueLoader />}>
        <RevenueChart />
      </Suspense>

      <Suspense fallback={<OrdersLoader />}>
        <RecentOrders />
      </Suspense>
    </div>
  );
}

async function RevenueChart() {
  const data = await getSlowRevenueData();   // Takes 2s
  return <Chart data={data} />;
}

async function RecentOrders() {
  const orders = await getRecentOrders();   // Takes 500ms
  return <OrderTable orders={orders} />;
}

// User sees:
// 1. UserHeader immediately
// 2. RecentOrders after 500ms
// 3. RevenueChart after 2s
// (Without Suspense, would wait 2s for everything)
```


## Direct Database Access

```tsx
// Server Components can directly access DB
// lib/db.ts
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient();

// app/users/page.tsx
import { prisma } from '@/lib/db';

export default async function UsersPage() {
  const users = await prisma.user.findMany({
    select: { id: true, name: true, email: true },
    orderBy: { createdAt: 'desc' },
    take: 50,
  });

  return (
    <table>
      <tbody>
        {users.map(u => (
          <tr key={u.id}><td>{u.name}</td><td>{u.email}</td></tr>
        ))}
      </tbody>
    </table>
  );
}
```


---

# CHAPTER 5: SERVER ACTIONS


## Form Mutations Without API Routes

```tsx
// Server Actions are functions that run on the server, callable from client
// Mark with 'use server' directive

// app/posts/new/page.tsx
import { redirect } from 'next/navigation';
import { revalidatePath } from 'next/cache';

async function createPost(formData: FormData) {
  'use server';   // Marks this as a Server Action

  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // Validate
  if (!title || title.length < 3) {
    return { error: 'Title too short' };
  }

  // Save to DB
  const post = await prisma.post.create({
    data: { title, content, authorId: getCurrentUserId() },
  });

  // Revalidate the posts list
  revalidatePath('/posts');

  // Redirect to new post
  redirect(`/posts/${post.id}`);
}

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```


## Server Actions with useFormStatus and useFormState

```tsx
// app/posts/new/PostForm.tsx
'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { createPost } from './actions';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Post'}
    </button>
  );
}

export default function PostForm() {
  const [state, formAction] = useFormState(createPost, { error: null });

  return (
    <form action={formAction}>
      <input name="title" required />
      <textarea name="content" required />
      {state.error && <p className="text-red-500">{state.error}</p>}
      <SubmitButton />
    </form>
  );
}

// app/posts/new/actions.ts
'use server';   // File-level directive

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const PostSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  content: z.string().min(10, 'Content too short'),
});

export async function createPost(prevState: any, formData: FormData) {
  const parsed = PostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!parsed.success) {
    return { error: parsed.error.errors[0].message };
  }

  await prisma.post.create({ data: parsed.data });
  revalidatePath('/posts');
  return { error: null, success: true };
}
```


## Calling Server Actions from Buttons

```tsx
'use client';

import { deletePost } from './actions';

function PostActions({ postId }: { postId: string }) {
  return (
    <button
      onClick={async () => {
        if (confirm('Delete this post?')) {
          await deletePost(postId);
        }
      }}
    >
      Delete
    </button>
  );
}

// actions.ts
'use server';

export async function deletePost(id: string) {
  // Auth check
  const user = await getCurrentUser();
  if (!user) throw new Error('Unauthorized');

  const post = await prisma.post.findUnique({ where: { id } });
  if (post?.authorId !== user.id) throw new Error('Forbidden');

  await prisma.post.delete({ where: { id } });
  revalidatePath('/posts');
}
```


---

# CHAPTER 6: API ROUTES (ROUTE HANDLERS)


## REST API Endpoints

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/users
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') ?? '1');
  const limit = parseInt(searchParams.get('limit') ?? '20');

  const users = await prisma.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return NextResponse.json({ users, page, limit });
}

// POST /api/users
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    const user = await prisma.user.create({
      data: { name: body.name, email: body.email },
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 400 }
    );
  }
}

// app/api/users/[id]/route.ts - Dynamic API route
interface Context {
  params: Promise<{ id: string }>;
}

// GET /api/users/123
export async function GET(request: NextRequest, context: Context) {
  const { id } = await context.params;
  const user = await prisma.user.findUnique({ where: { id } });

  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  return NextResponse.json(user);
}

// PATCH /api/users/123
export async function PATCH(request: NextRequest, context: Context) {
  const { id } = await context.params;
  const body = await request.json();

  const user = await prisma.user.update({
    where: { id },
    data: body,
  });

  return NextResponse.json(user);
}

// DELETE /api/users/123
export async function DELETE(request: NextRequest, context: Context) {
  const { id } = await context.params;
  await prisma.user.delete({ where: { id } });

  return new NextResponse(null, { status: 204 });
}
```


## Streaming API Responses

```tsx
// app/api/chat/route.ts - Server-Sent Events for AI chat
export async function POST(request: NextRequest) {
  const { message } = await request.json();

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      try {
        // Stream from OpenAI/Anthropic
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: 'gpt-4',
            messages: [{ role: 'user', content: message }],
            stream: true,
          }),
        });

        const reader = response.body?.getReader();
        if (!reader) throw new Error('No reader');

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          controller.enqueue(value);
        }
      } catch (e) {
        controller.error(e);
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```


## CORS and Middleware

```tsx
// middleware.ts (root of project, not in app/)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Add CORS to /api/* requests
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const response = NextResponse.next();
    response.headers.set('Access-Control-Allow-Origin', '*');
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE');
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    return response;
  }

  // Protect /dashboard/* routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    const token = request.cookies.get('auth_token');
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}

// Match only these paths (performance)
export const config = {
  matcher: ['/api/:path*', '/dashboard/:path*'],
};
```


---

# CHAPTER 7: STATIC SITE GENERATION (SSG)


## Static Pages with generateStaticParams

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';

// Pre-build these pages at build time
export async function generateStaticParams() {
  const posts = await prisma.post.findMany({ select: { slug: true } });
  return posts.map(post => ({ slug: post.slug }));
  // Generates /blog/post-1, /blog/post-2, etc. statically
}

// Page metadata - dynamic per slug
export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const post = await getPostBySlug(slug);
  if (!post) return { title: 'Not Found' };

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  };
}

interface Props {
  params: Promise<{ slug: string }>;
}

export default async function BlogPost({ params }: Props) {
  const { slug } = await params;
  const post = await getPostBySlug(slug);
  if (!post) notFound();

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// Force dynamic rendering (no caching)
export const dynamic = 'force-dynamic';

// Force static rendering
export const dynamic = 'force-static';

// Revalidate every N seconds (ISR)
export const revalidate = 60;
```


## On-Demand Revalidation

```tsx
// app/api/revalidate/route.ts - Trigger via webhook
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  // Verify webhook secret
  const secret = request.headers.get('x-webhook-secret');
  if (secret !== process.env.WEBHOOK_SECRET) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { path, tag } = await request.json();

  if (path) revalidatePath(path);
  if (tag) revalidateTag(tag);

  return NextResponse.json({ revalidated: true });
}

// Example: CMS calls this when content changes
// POST /api/revalidate
// { "path": "/blog/post-1" } or { "tag": "posts" }
```


---

# CHAPTER 8: AUTHENTICATION


## NextAuth.js (Auth.js v5)

```tsx
// npm install next-auth@beta
// auth.ts (root)
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';
import GitHub from 'next-auth/providers/github';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/db';
import bcrypt from 'bcryptjs';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'jwt' },

  providers: [
    Google,
    GitHub,
    Credentials({
      name: 'Email',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const user = await prisma.user.findUnique({
          where: { email: credentials?.email as string },
        });
        if (!user) return null;

        const valid = await bcrypt.compare(
          credentials?.password as string,
          user.passwordHash
        );
        if (!valid) return null;

        return { id: user.id, email: user.email, name: user.name };
      },
    }),
  ],

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = (user as any).role;
      }
      return token;
    },
    async session({ session, token }) {
      if (token && session.user) {
        session.user.id = token.id as string;
        (session.user as any).role = token.role;
      }
      return session;
    },
  },

  pages: {
    signIn: '/login',
    error: '/auth-error',
  },
});

// app/api/auth/[...nextauth]/route.ts
export { GET, POST } from '@/auth';

// app/login/page.tsx - Sign-in page
import { signIn } from '@/auth';

export default function LoginPage() {
  return (
    <div>
      <form action={async (formData) => {
        'use server';
        await signIn('credentials', {
          email: formData.get('email'),
          password: formData.get('password'),
          redirectTo: '/dashboard',
        });
      }}>
        <input name="email" type="email" />
        <input name="password" type="password" />
        <button>Sign In</button>
      </form>

      <form action={async () => {
        'use server';
        await signIn('google', { redirectTo: '/dashboard' });
      }}>
        <button>Sign in with Google</button>
      </form>
    </div>
  );
}

// Get session in Server Component
import { auth } from '@/auth';

export default async function Dashboard() {
  const session = await auth();
  if (!session?.user) redirect('/login');

  return <h1>Welcome {session.user.name}</h1>;
}

// Protect routes with middleware
// middleware.ts
export { auth as middleware } from '@/auth';

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
};
```


---

# CHAPTER 9: IMAGES, FONTS, METADATA


## Image Optimization

```tsx
import Image from 'next/image';

// Local images - auto-optimized at build time
import profilePic from '@/public/me.jpg';

<Image
  src={profilePic}
  alt="Profile"
  placeholder="blur"   // Shows blurred preview
  priority             // Preload above-the-fold
/>

// Remote images - need width/height + config
<Image
  src="https://example.com/image.jpg"
  alt="Description"
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, 800px"
/>

// Configure allowed remote hosts - next.config.js
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.example.com' },
      { protocol: 'https', hostname: '*.cloudinary.com' },
    ],
    formats: ['image/avif', 'image/webp'],
  },
};

// Fill mode - parent has position:relative
<div style={{ position: 'relative', width: '100%', height: 400 }}>
  <Image src="/hero.jpg" alt="" fill style={{ objectFit: 'cover' }} />
</div>
```


## Google Fonts (Self-Hosted)

```tsx
// app/layout.tsx
import { Inter, Roboto_Mono } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  );
}

// In CSS or Tailwind
// font-family: var(--font-inter)
// font-mono: var(--font-mono)
```


## Metadata API

```tsx
// Static metadata
export const metadata = {
  title: 'My Page',
  description: 'Description for SEO',
  keywords: ['next.js', 'react', 'typescript'],
  authors: [{ name: 'Teodor', url: 'https://example.com' }],

  openGraph: {
    title: 'My Page',
    description: 'OG description',
    url: 'https://example.com',
    siteName: 'Example',
    images: [{ url: '/og.png', width: 1200, height: 630 }],
    locale: 'en_US',
    type: 'website',
  },

  twitter: {
    card: 'summary_large_image',
    title: 'My Page',
    description: 'Twitter description',
    images: ['/og.png'],
  },

  robots: {
    index: true,
    follow: true,
  },

  alternates: {
    canonical: 'https://example.com',
  },
};

// Dynamic metadata
export async function generateMetadata({ params }: Props) {
  const post = await getPost((await params).id);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: { images: [post.image] },
  };
}

// Title template inheritance
// app/layout.tsx
export const metadata = {
  title: { template: '%s | My Site', default: 'My Site' },
};

// app/about/page.tsx
export const metadata = { title: 'About' };
// Renders as: "About | My Site"
```


---

# CHAPTER 10: DEPLOYMENT AND PRODUCTION


## Environment Variables

```tsx
// .env.local (NOT committed)
DATABASE_URL=postgres://...
NEXT_PUBLIC_API_URL=https://api.example.com
SECRET_KEY=server-only-secret

// .env.production
DATABASE_URL=postgres://prod...

// Access in code
process.env.DATABASE_URL              // Server-side only
process.env.NEXT_PUBLIC_API_URL       // Available in browser (prefix matters!)

// Type-safe env with @t3-oss/env-nextjs
// env.ts
import { createEnv } from '@t3-oss/env-nextjs';
import { z } from 'zod';

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    SECRET_KEY: z.string().min(32),
  },
  client: {
    NEXT_PUBLIC_API_URL: z.string().url(),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    SECRET_KEY: process.env.SECRET_KEY,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
});

// Usage - throws at build time if missing
import { env } from '@/env';
const db = createClient(env.DATABASE_URL);
```


## Performance Best Practices

```tsx
// 1. Use Image and Font from next/* (auto-optimized)

// 2. Reduce client-side JS - default to Server Components
// Only add 'use client' when you need interactivity

// 3. Code-split with dynamic imports
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <Spinner />,
  ssr: false,   // Skip SSR if not needed
});

// 4. Streaming with Suspense for slow data
<Suspense fallback={<Skeleton />}>
  <SlowComponent />
</Suspense>

// 5. Cache fetches aggressively when possible
const data = await fetch(url, { next: { revalidate: 3600 } });

// 6. Use Edge Runtime for low-latency endpoints
// app/api/geo/route.ts
export const runtime = 'edge';
export async function GET(req: NextRequest) {
  return Response.json({ country: req.geo?.country });
}

// 7. Bundle analyzer
// npm install @next/bundle-analyzer
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer({});

// ANALYZE=true npm run build  // Opens analyzer in browser
```


## Common Pitfalls

```tsx
// PITFALL 1: 'use client' boundary too high
// BAD - whole page becomes client component
'use client';
export default function Page() {
  return (
    <div>
      <ServerOnlyStuff />   {/* Wasted - now client */}
      <InteractiveButton />
    </div>
  );
}

// GOOD - only the interactive part is client
export default function Page() {  // Server
  return (
    <div>
      <ServerOnlyStuff />
      <InteractiveButton />   {/* Has its own 'use client' inside */}
    </div>
  );
}

// PITFALL 2: Fetching the same data twice
// BAD - duplicate requests
async function PostPage({ params }: Props) {
  const post = await fetchPost(params.id);    // Request 1
  return <PostHeader post={post} />;
}
async function PostHeader({ post }: { post: Post }) {
  const author = await fetchUser(post.authorId);   // OK
  // But if PostPage also called fetchUser, would duplicate
}

// GOOD - Next.js dedupes fetch() calls within a request automatically

// PITFALL 3: Async params in Next 15+
// Next.js 15 made params and searchParams async (Promise)
// OLD (Next 14):
function Page({ params }: { params: { id: string } }) {
  return <div>{params.id}</div>;
}
// NEW (Next 15+):
async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <div>{id}</div>;
}

// PITFALL 4: Cookies/headers in Server Components
import { cookies, headers } from 'next/headers';

async function Page() {
  const cookieStore = await cookies();      // Async in Next 15+
  const headersList = await headers();      // Async in Next 15+
  const token = cookieStore.get('token');
  const userAgent = headersList.get('user-agent');
}

// PITFALL 5: Forgetting revalidate after mutation
async function createPost(formData: FormData) {
  'use server';
  await prisma.post.create({ data: { ... } });
  // BAD - posts list still shows old data!
}

async function createPost(formData: FormData) {
  'use server';
  await prisma.post.create({ data: { ... } });
  revalidatePath('/posts');   // GOOD - refetch posts list
}
```
