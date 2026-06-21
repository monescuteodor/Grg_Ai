# Web Performance Complete Reference


---

# CHAPTER 1: PERFORMANCE FUNDAMENTALS


## Remarks

Web performance is the speed and responsiveness of websites and applications. Performance directly impacts business: Amazon found that every 100ms of latency costs 1% in sales. Google uses page speed as a ranking factor. Users abandon pages that take more than 3 seconds to load. Performance is not a feature — it's a requirement.

Key concepts: **Core Web Vitals** (Google's performance metrics), **Critical Rendering Path** (how browsers render pages), **Time to First Byte** (server response speed), **Largest Contentful Paint** (when main content visible), **Cumulative Layout Shift** (visual stability), **First Input Delay** (interactivity), **Bundle size** (JavaScript sent to browser), **Caching** (avoid refetching), **CDN** (serve from edge).

Used by: every website. Google PageSpeed Insights scores affect SEO rankings.

Tools: **Lighthouse** (Chrome DevTools audit), **WebPageTest** (detailed analysis), **Chrome DevTools Performance tab**, **PageSpeed Insights** (Google's online tool), **Bundle analyzers** (webpack-bundle-analyzer, source-map-explorer), **Web Vitals library** (measure in field).


## Why Performance Matters

```
BUSINESS IMPACT:
  Amazon:    100ms latency = 1% revenue loss
  Google:    500ms slower = 20% fewer searches
  Walmart:   1s improvement = 2% more conversions
  BBC:       1s slower = 10% users leave
  Pinterest: 40% less wait time = 15% more signups

USER EXPECTATIONS:
  <1 second:    feels instant
  1-3 seconds:  noticeable but acceptable
  3-5 seconds:  frustrating
  >5 seconds:   most users abandon

SEO IMPACT:
  Google ranks faster pages higher (Core Web Vitals is ranking signal).
  Mobile-first indexing means mobile performance matters most.

MOBILE REALITY:
  Average phone is mid-range (not iPhone 16 Pro)
  Average connection: 4G with variable latency
  CPU is 3-5x slower than desktop
  ALWAYS test on real mid-range devices
```


## Core Web Vitals

```
GOOGLE'S THREE KEY METRICS (measured on real users):

LCP (Largest Contentful Paint):
  When does the MAIN content become visible?
  Measures: largest image, text block, or video in viewport
  Good:    ≤ 2.5 seconds
  Poor:    > 4.0 seconds
  
  Fix: optimize images, preload critical resources,
       fast server response, no render-blocking resources

INP (Interaction to Next Paint):
  How fast does the page respond to user input?
  Replaced FID (First Input Delay) in March 2024
  Measures: time from click/tap/keypress to next visual update
  Good:    ≤ 200 milliseconds
  Poor:    > 500 milliseconds
  
  Fix: break long tasks, use web workers, reduce JS execution,
       yield to main thread, avoid forced layout/reflow

CLS (Cumulative Layout Shift):
  How much does content jump around during loading?
  Measures: unexpected layout shifts (elements moving)
  Good:    ≤ 0.1
  Poor:    > 0.25
  
  Fix: set dimensions on images/video, reserve space for ads/embeds,
       don't insert content above existing content, use transform for animations

OTHER IMPORTANT METRICS:
  TTFB (Time to First Byte):    Server response time (<800ms)
  FCP (First Contentful Paint):  First pixel of content (<1.8s)
  TTI (Time to Interactive):     Page fully interactive (<3.8s)
  TBT (Total Blocking Time):    Main thread blocked time (<200ms)
  Speed Index:                   How quickly content is visually populated
```


## Measuring Performance

```javascript
// In Chrome DevTools:
// 1. Open DevTools (F12)
// 2. Lighthouse tab → Run audit
// 3. Performance tab → Record → interact → Stop
// 4. Network tab → disable cache, throttle to 3G

// Web Vitals JavaScript library (measure REAL users)
// npm install web-vitals
import { onCLS, onINP, onLCP, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
    const body = JSON.stringify({
        name: metric.name,
        value: metric.value,
        rating: metric.rating,      // "good", "needs-improvement", "poor"
        delta: metric.delta,
        id: metric.id,
        navigationType: metric.navigationType,
    });

    // Use sendBeacon for reliability (survives page unload)
    if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/vitals', body);
    } else {
        fetch('/api/vitals', { body, method: 'POST', keepalive: true });
    }
}

onCLS(sendToAnalytics);
onINP(sendToAnalytics);
onLCP(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);


// Performance API (built into browser)
// Navigation timing
const nav = performance.getEntriesByType('navigation')[0];
console.log({
    dns:         nav.domainLookupEnd - nav.domainLookupStart,
    tcp:         nav.connectEnd - nav.connectStart,
    ttfb:        nav.responseStart - nav.requestStart,
    download:    nav.responseEnd - nav.responseStart,
    domParse:    nav.domInteractive - nav.responseEnd,
    domReady:    nav.domContentLoadedEventEnd - nav.navigationStart,
    fullLoad:    nav.loadEventEnd - nav.navigationStart,
});

// Resource timing (every asset)
const resources = performance.getEntriesByType('resource');
resources.forEach(r => {
    console.log(`${r.name}: ${r.duration.toFixed(0)}ms, ${r.transferSize} bytes`);
});

// Custom marks (measure your own code)
performance.mark('start-render');
renderComponent();
performance.mark('end-render');
performance.measure('render-time', 'start-render', 'end-render');
const measure = performance.getEntriesByName('render-time')[0];
console.log(`Render took ${measure.duration.toFixed(0)}ms`);
```


---

# CHAPTER 2: CRITICAL RENDERING PATH


## How Browsers Render Pages

```
1. PARSE HTML → DOM (Document Object Model) tree
2. PARSE CSS  → CSSOM (CSS Object Model) tree
3. COMBINE    → Render tree (visible elements only)
4. LAYOUT     → Calculate position and size of each element
5. PAINT      → Fill in pixels (colors, images, text)
6. COMPOSITE  → Layer composition (GPU)

BLOCKING RESOURCES:
  CSS:  render-blocking (browser won't paint until CSS parsed)
  JS:   parser-blocking (browser stops HTML parsing to execute JS)
  
  Order: CSS → JS → HTML parsing resumes

OPTIMIZATION GOAL:
  Make the critical rendering path as SHORT as possible.
  Fewer critical resources → fewer bytes → faster render.
```


## HTML Optimization

```html
<!-- 1. Put CSS in <head> (render-blocking but needed for first paint) -->
<head>
    <link rel="stylesheet" href="/css/critical.css">
</head>

<!-- 2. Defer non-critical CSS -->
<link rel="stylesheet" href="/css/non-critical.css" media="print" onload="this.media='all'">

<!-- 3. Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/img/hero.webp" as="image">
<link rel="preload" href="/css/critical.css" as="style">

<!-- 4. Preconnect to third-party origins -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://api.example.com">
<link rel="dns-prefetch" href="https://cdn.example.com">

<!-- 5. Script loading strategies -->
<!-- Default: blocks HTML parsing -->
<script src="app.js"></script>

<!-- defer: download parallel, execute AFTER HTML parsed (preserves order) -->
<script defer src="app.js"></script>
<script defer src="analytics.js"></script>

<!-- async: download parallel, execute immediately when ready (no order guarantee) -->
<script async src="analytics.js"></script>

<!-- BEST PRACTICE:
     defer for your app code (needs DOM)
     async for independent scripts (analytics, ads)
     inline critical JS in <head> for instant execution
-->

<!-- 6. Fetch priority hints -->
<img src="hero.jpg" fetchpriority="high" alt="Hero">
<img src="footer-logo.jpg" fetchpriority="low" alt="Logo">
<link rel="preload" href="/api/data" as="fetch" fetchpriority="high">

<!-- 7. Meta viewport (prevents mobile zoom delay) -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```


---

# CHAPTER 3: IMAGE OPTIMIZATION


## Image Formats

```
FORMAT COMPARISON:

JPEG:   Photos, gradients. Lossy compression.
        Good quality at 80-85%. No transparency.

PNG:    Screenshots, graphics with transparency.
        Lossless. Larger than JPEG for photos.

WebP:   Modern format by Google. 25-35% smaller than JPEG.
        Supports transparency + animation. 97% browser support.

AVIF:   Newest format. 50% smaller than JPEG!
        Slower to encode. 92% browser support (growing).
        Best quality-to-size ratio.

SVG:    Vector graphics (icons, logos, illustrations).
        Scales perfectly. Text-based (can be inlined/styled with CSS).
        Tiny for simple shapes.

GIF:    Simple animations. Limited to 256 colors.
        Use video (MP4/WebM) for complex animations instead.

PRIORITY: AVIF → WebP → JPEG/PNG (fallback)
```


## Responsive Images

```html
<!-- 1. srcset + sizes (browser picks best size) -->
<img
    src="photo-800.jpg"
    srcset="
        photo-400.jpg 400w,
        photo-800.jpg 800w,
        photo-1200.jpg 1200w,
        photo-1600.jpg 1600w
    "
    sizes="
        (max-width: 640px) 100vw,
        (max-width: 1024px) 50vw,
        33vw
    "
    alt="Product photo"
    loading="lazy"
    decoding="async"
    width="800"
    height="600"
>
<!-- Browser calculates: viewport 800px → needs ~400px image → downloads photo-400.jpg -->

<!-- 2. <picture> for format fallback -->
<picture>
    <source srcset="photo.avif" type="image/avif">
    <source srcset="photo.webp" type="image/webp">
    <img src="photo.jpg" alt="Product" loading="lazy" width="800" height="600">
</picture>
<!-- Browser picks first supported format (AVIF > WebP > JPEG) -->

<!-- 3. Art direction (different crops per viewport) -->
<picture>
    <source srcset="hero-mobile.webp" media="(max-width: 640px)">
    <source srcset="hero-tablet.webp" media="(max-width: 1024px)">
    <img src="hero-desktop.webp" alt="Hero" width="1600" height="800">
</picture>

<!-- CRITICAL: Always set width + height to prevent CLS! -->
<!-- Or use aspect-ratio in CSS: -->
<style>
    .hero-img { aspect-ratio: 16/9; width: 100%; height: auto; }
</style>
```


## Lazy Loading

```html
<!-- Native lazy loading (simplest, best) -->
<img src="photo.jpg" loading="lazy" alt="Below fold" width="400" height="300">

<!-- DON'T lazy-load above-the-fold images! -->
<img src="hero.jpg" loading="eager" alt="Hero" fetchpriority="high" width="1200" height="600">

<!-- Lazy load iframes too -->
<iframe src="https://youtube.com/embed/..." loading="lazy"></iframe>
```

```javascript
// Intersection Observer (custom lazy loading)
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.remove('lazy');
            observer.unobserve(img);
        }
    });
}, {
    rootMargin: '200px',   // Start loading 200px before visible
});

document.querySelectorAll('img.lazy').forEach(img => observer.observe(img));

// HTML:
// <img class="lazy" data-src="real-image.jpg" src="placeholder.jpg" alt="...">
```


## Image Build Pipeline

```bash
# Convert to modern formats (using sharp or imagemagick)
# sharp (Node.js — very fast)
npm install sharp

# Script: optimize all images
node -e "
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputDir = './images';
const outputDir = './optimized';

fs.readdirSync(inputDir).forEach(async file => {
    if (!/\.(jpg|jpeg|png)$/i.test(file)) return;
    
    const input = path.join(inputDir, file);
    const name = path.parse(file).name;
    
    // WebP
    await sharp(input)
        .webp({ quality: 80 })
        .toFile(path.join(outputDir, name + '.webp'));
    
    // AVIF
    await sharp(input)
        .avif({ quality: 65 })
        .toFile(path.join(outputDir, name + '.avif'));
    
    // Responsive sizes
    for (const width of [400, 800, 1200, 1600]) {
        await sharp(input)
            .resize(width)
            .webp({ quality: 80 })
            .toFile(path.join(outputDir, name + '-' + width + '.webp'));
    }
});
"

# ImageMagick (CLI alternative)
convert input.jpg -resize 800x -quality 85 output.jpg
convert input.png -resize 400x output.webp
```


---

# CHAPTER 4: JAVASCRIPT OPTIMIZATION


## Bundle Size

```
WHY IT MATTERS:
  100 KB JS ≈ 350ms parse+compile on mid-range phone.
  1 MB JS ≈ 3.5 seconds (!!!) on same phone.
  Users on 3G download 1 MB in ~5 seconds.

IDEAL TARGETS:
  Initial bundle:   < 170 KB (gzipped)
  Total JS:         < 500 KB (gzipped)
  Per-route chunk:  < 50 KB (gzipped)

TOOLS TO ANALYZE:
  webpack: webpack-bundle-analyzer
  vite: rollup-plugin-visualizer
  generic: source-map-explorer
  online: bundlephobia.com (check package size BEFORE installing)
```


## Code Splitting

```javascript
// React.lazy + Suspense (route-based splitting)
import { lazy, Suspense } from 'react';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
    return (
        <Suspense fallback={<LoadingSpinner />}>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/settings" element={<Settings />} />
            </Routes>
        </Suspense>
    );
}

// Component-level splitting (heavy components)
const ChartComponent = lazy(() => import('./ChartComponent'));
const MarkdownEditor = lazy(() => import('./MarkdownEditor'));

// Dynamic import for libraries
async function generatePDF() {
    const { jsPDF } = await import('jspdf');   // Only loaded when needed
    const doc = new jsPDF();
    doc.text('Hello', 10, 10);
    doc.save('output.pdf');
}

// Next.js dynamic imports
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('../components/Chart'), {
    loading: () => <Skeleton height={400} />,
    ssr: false,   // Don't render on server (client-only)
});
```


## Tree Shaking

```javascript
// Tree shaking: bundler removes unused exports

// BAD: imports entire library
import _ from 'lodash';
_.debounce(fn, 300);
// → Bundles ALL of lodash (~70 KB gzipped!)

// GOOD: import only what you use
import debounce from 'lodash/debounce';
debounce(fn, 300);
// → Bundles only debounce (~1 KB)

// BETTER: use lodash-es (ES modules, tree-shakeable)
import { debounce } from 'lodash-es';

// BEST: use native or tiny alternatives
// lodash.debounce → just-debounce-it (300 bytes)
// moment.js (300 KB!) → date-fns (tree-shakeable) or dayjs (2 KB)
// axios (13 KB) → native fetch (0 KB)

// Ensure tree shaking works:
// 1. Use ES modules (import/export), NOT CommonJS (require)
// 2. Set "sideEffects": false in package.json
// 3. Avoid barrel exports that import everything:

// BAD barrel (index.ts):
export * from './Button';
export * from './Modal';
export * from './Chart';
// → Importing Button may also pull in Chart!

// GOOD: import directly
import { Button } from './components/Button';
```


## Rendering Performance

```javascript
// 1. AVOID FORCED REFLOW (Layout Thrashing)
// BAD: read then write in loop → forces browser to recalculate layout each iteration
for (const el of elements) {
    const height = el.offsetHeight;        // READ (forces layout)
    el.style.height = height * 2 + 'px';   // WRITE (invalidates layout)
    // Next iteration: READ forces recalculation!
}

// GOOD: batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight);   // All reads
elements.forEach((el, i) => {
    el.style.height = heights[i] * 2 + 'px';            // All writes
});


// 2. USE requestAnimationFrame FOR VISUAL UPDATES
// BAD: update on every scroll event (can fire 60+ times/sec)
window.addEventListener('scroll', () => {
    element.style.transform = `translateY(${window.scrollY}px)`;
});

// GOOD: throttle to animation frame
let ticking = false;
window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(() => {
            element.style.transform = `translateY(${window.scrollY}px)`;
            ticking = false;
        });
        ticking = true;
    }
});


// 3. USE CSS TRANSFORMS INSTEAD OF LAYOUT PROPERTIES
// BAD: triggers layout + paint
element.style.left = '100px';
element.style.top = '50px';
element.style.width = '200px';

// GOOD: only triggers composite (GPU, no layout/paint)
element.style.transform = 'translate(100px, 50px) scale(1.5)';
element.style.opacity = '0.5';

// Properties that DON'T trigger layout:
// transform, opacity, filter, will-change


// 4. VIRTUALIZE LONG LISTS
// Don't render 10,000 DOM elements. Render only visible ones.
// Libraries: react-window, react-virtuoso, @tanstack/virtual
import { FixedSizeList } from 'react-window';

function VirtualList({ items }) {
    return (
        <FixedSizeList
            height={600}
            width="100%"
            itemCount={items.length}
            itemSize={50}
        >
            {({ index, style }) => (
                <div style={style}>{items[index].name}</div>
            )}
        </FixedSizeList>
    );
}


// 5. DEBOUNCE EXPENSIVE OPERATIONS
function debounce(fn, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}

const handleSearch = debounce(async (query) => {
    const results = await searchAPI(query);
    setResults(results);
}, 300);

// User types: h-e-l-l-o → only ONE API call (after 300ms idle)


// 6. WEB WORKERS FOR CPU-HEAVY WORK
// Main thread stays responsive
const worker = new Worker('/worker.js');

worker.postMessage({ data: largeDataset, operation: 'sort' });

worker.onmessage = (event) => {
    const sortedData = event.data;
    renderResults(sortedData);
};

// worker.js
self.onmessage = (event) => {
    const { data, operation } = event.data;
    if (operation === 'sort') {
        const sorted = data.sort((a, b) => a.value - b.value);
        self.postMessage(sorted);
    }
};
```


---

# CHAPTER 5: CACHING STRATEGIES


## Browser Cache Headers

```
CACHE-CONTROL HEADER (most important):

Immutable assets (hashed filenames: app.abc123.js):
  Cache-Control: public, max-age=31536000, immutable
  → Cache for 1 year, never revalidate (file hash changes = new URL)

HTML pages:
  Cache-Control: no-cache
  → Always revalidate with server (but can use cached if 304)

API responses:
  Cache-Control: private, max-age=0, must-revalidate
  → Don't cache in shared caches, always check with server

Public static assets:
  Cache-Control: public, max-age=86400
  → Cache for 1 day in any cache (browser, CDN, proxy)

ETAG (content hash):
  Server: ETag: "abc123"
  Client (next request): If-None-Match: "abc123"
  Server: 304 Not Modified (no body — use cached version)
  → Saves bandwidth when content hasn't changed

LAST-MODIFIED:
  Server: Last-Modified: Mon, 10 Jun 2026 12:00:00 GMT
  Client: If-Modified-Since: Mon, 10 Jun 2026 12:00:00 GMT
  Server: 304 Not Modified
```


## Service Worker Cache

```javascript
// service-worker.js — offline-first caching

const CACHE_NAME = 'app-v2';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/css/app.css',
    '/js/app.js',
    '/offline.html',
];

// Install: cache static assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(STATIC_ASSETS);
        })
    );
    self.skipWaiting();   // Activate immediately
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys
                    .filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            );
        })
    );
    self.clients.claim();
});

// Fetch: cache-first for static, network-first for API
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    if (url.pathname.startsWith('/api/')) {
        // Network first (API calls)
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, clone);
                    });
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
    } else {
        // Cache first (static assets)
        event.respondWith(
            caches.match(event.request).then(cached => {
                return cached || fetch(event.request);
            })
        );
    }
});
```


## React / Next.js Caching

```javascript
// Next.js caching strategies

// 1. Static Generation (SSG) — fastest, cached at build time
export async function getStaticProps() {
    const posts = await fetchPosts();
    return {
        props: { posts },
        revalidate: 3600,   // ISR: regenerate every hour
    };
}

// 2. Server-side fetch caching (App Router)
// Cached by default in Next.js 14+
async function getUser(id) {
    const res = await fetch(`https://api.example.com/users/${id}`, {
        next: { revalidate: 60 },   // Cache for 60 seconds
    });
    return res.json();
}

// Force no cache
const res = await fetch(url, { cache: 'no-store' });

// 3. React Query / TanStack Query client-side cache
const { data } = useQuery({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000,     // Fresh for 5 min (no refetch)
    gcTime: 30 * 60 * 1000,       // Keep in cache 30 min
    refetchOnWindowFocus: false,
});
```


---

# CHAPTER 6: FONT AND CSS OPTIMIZATION


## Font Loading

```css
/* 1. Use font-display to prevent invisible text */
@font-face {
    font-family: 'MyFont';
    src: url('/fonts/myfont.woff2') format('woff2');
    font-display: swap;   /* Show fallback immediately, swap when loaded */
    /* Other values:
       block:    hide text 3s then fallback (bad!)
       swap:     show fallback immediately (RECOMMENDED)
       fallback: brief block then fallback (compromise)
       optional: use if cached, skip if not (performance-first)
    */
}

/* 2. Use system font stack (zero load time) */
body {
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        'Segoe UI',
        Roboto,
        Oxygen,
        Ubuntu,
        Cantarell,
        sans-serif;
}

/* 3. Subset fonts (only characters you need) */
/* Use google-webfonts-helper or glyphhanger */
/* Latin subset: ~20KB instead of ~100KB full unicode */
```

```html
<!-- 4. Preload critical fonts -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

<!-- 5. Self-host Google Fonts (faster than Google CDN) -->
<!-- Download from google-webfonts-helper, serve from your domain -->
<!-- Avoids: DNS lookup + connection to fonts.googleapis.com -->
```


## CSS Optimization

```css
/* 1. Minimize CSS (production) */
/* Tools: cssnano, lightningcss, postcss */

/* 2. Remove unused CSS */
/* Tools: PurgeCSS, Tailwind's built-in purge */
/* Tailwind: only generates classes you USE → tiny CSS */

/* 3. Avoid expensive selectors */
/* BAD: universal, deep nesting */
* { box-sizing: border-box; }   /* OK for reset, avoid elsewhere */
.nav ul li a span.icon { }       /* Too specific, slow to match */

/* GOOD: simple, shallow */
.nav-icon { }

/* 4. Use CSS containment for complex layouts */
.card {
    contain: layout style paint;   /* Browser can optimize rendering */
}

/* 5. will-change hint (use sparingly!) */
.animated-element {
    will-change: transform, opacity;   /* GPU layer promotion */
}
/* Remove after animation completes to free GPU memory */

/* 6. Prefer CSS over JavaScript for animations */
/* CSS animations run on compositor thread (smooth even when JS busy) */
.fade-in {
    animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* 7. Critical CSS: inline above-fold CSS in <head> */
/* Extract with tools like critical or critters */
<style>
    /* Only CSS needed for above-the-fold content */
    body { margin: 0; font-family: sans-serif; }
    .header { ... }
    .hero { ... }
</style>
<link rel="stylesheet" href="/css/full.css" media="print" onload="this.media='all'">
```


---

# CHAPTER 7: SERVER-SIDE OPTIMIZATION


## Server Response Time

```python
# TTFB (Time to First Byte) should be < 800ms

# 1. Database query optimization
# BAD: N+1 queries
for user in users:
    posts = db.query("SELECT * FROM posts WHERE user_id = ?", user.id)

# GOOD: single query with JOIN
users_with_posts = db.query("""
    SELECT u.*, p.* FROM users u
    LEFT JOIN posts p ON p.user_id = u.id
""")


# 2. Add caching layer
import redis

cache = redis.Redis()

async def get_popular_posts():
    cached = cache.get('popular_posts')
    if cached:
        return json.loads(cached)
    
    posts = await db.fetch("SELECT * FROM posts ORDER BY views DESC LIMIT 20")
    cache.setex('popular_posts', 300, json.dumps(posts))   # 5 min cache
    return posts


# 3. Compression
# NGINX gzip config
# gzip on;
# gzip_types text/plain text/css application/json application/javascript text/xml;
# gzip_min_length 1000;
# gzip_comp_level 6;

# Brotli (better compression than gzip, 15-25% smaller)
# brotli on;
# brotli_types text/plain text/css application/json application/javascript;


# 4. Connection pooling (see databases_advanced.md)
# 5. CDN for static assets (see system_design.md)
```


## HTTP/2 and HTTP/3

```
HTTP/1.1 PROBLEMS:
  - One request per connection (head-of-line blocking)
  - 6 connections max per domain (browser limit)
  - Text-based headers (verbose, repeated)

HTTP/2 BENEFITS:
  - Multiplexing: many requests on ONE connection
  - Header compression (HPACK)
  - Server push (preemptively send assets)
  - Binary protocol (faster parsing)
  - Stream prioritization

HTTP/3 BENEFITS:
  - Based on QUIC (UDP, not TCP)
  - Even faster connection setup (0-RTT)
  - No head-of-line blocking at transport level
  - Better on lossy networks (mobile)

ENABLING:
  Most CDNs (Cloudflare, CloudFront) support HTTP/2 and HTTP/3 automatically.
  NGINX: http2 on; in listen directive.

WHAT CHANGES FOR DEVELOPERS:
  - Don't need to bundle/sprite assets (multiplexing handles many small files)
  - Don't need domain sharding (one connection is enough)
  - Preload hints replace server push (server push is being deprecated)
```


---

# CHAPTER 8: PERFORMANCE CHECKLIST AND PITFALLS


## Performance Checklist

```
IMAGES:
  ☐ Use WebP/AVIF with JPEG fallback
  ☐ Responsive images with srcset + sizes
  ☐ Lazy load below-fold images (loading="lazy")
  ☐ Set width + height to prevent CLS
  ☐ Compress at build time (80-85% quality)
  ☐ Use CDN for image delivery

JAVASCRIPT:
  ☐ Code split by route (React.lazy / dynamic import)
  ☐ Tree shake unused code (ES modules)
  ☐ Defer non-critical scripts
  ☐ Bundle size < 170 KB gzipped initial
  ☐ Audit dependencies (bundlephobia.com)
  ☐ Remove console.log in production

CSS:
  ☐ Inline critical CSS
  ☐ Remove unused CSS (PurgeCSS)
  ☐ font-display: swap
  ☐ Self-host fonts (avoid Google Fonts CDN)
  ☐ Preload critical fonts

CACHING:
  ☐ Hashed filenames for static assets (cache forever)
  ☐ Proper Cache-Control headers
  ☐ CDN configured
  ☐ Service worker for offline (if applicable)

SERVER:
  ☐ TTFB < 800ms
  ☐ gzip/Brotli compression enabled
  ☐ HTTP/2 enabled
  ☐ Database queries optimized
  ☐ Redis cache for hot data
  ☐ Connection pooling

MONITORING:
  ☐ Core Web Vitals tracked in production (web-vitals)
  ☐ Lighthouse CI in deployment pipeline
  ☐ Real User Monitoring (RUM) dashboard
  ☐ Performance budget enforced

MOBILE:
  ☐ Test on real mid-range device
  ☐ Test on 3G throttling
  ☐ Touch targets ≥ 48px
  ☐ No horizontal scroll
```


## Common Pitfalls

```
PITFALL 1: Unoptimized images
  2 MB hero image → 5 second load on mobile.
  Fix: WebP/AVIF, responsive sizes, lazy loading, compression.

PITFALL 2: Too much JavaScript
  2 MB JS bundle → 7 second parse on mid-range phone.
  Fix: code split, tree shake, audit deps, lazy load.

PITFALL 3: No caching headers
  Every visit re-downloads everything.
  Fix: Cache-Control with hashed filenames for static, ETag for dynamic.

PITFALL 4: Render-blocking resources
  5 CSS files + 3 JS files in <head> → nothing renders until all loaded.
  Fix: inline critical CSS, defer JS, preload important resources.

PITFALL 5: Layout shift (CLS)
  Images/ads load → content jumps down → user clicks wrong thing.
  Fix: set dimensions on media, reserve space for dynamic content.

PITFALL 6: Third-party scripts
  Analytics, chat widgets, ads → 500 KB+ extra JS.
  Fix: load async, delay until after interaction, audit impact.

PITFALL 7: Web fonts FOIT
  Custom font loading → invisible text for 3 seconds.
  Fix: font-display: swap, preload critical fonts, system font fallback.

PITFALL 8: Not measuring real users
  Lighthouse score is synthetic. Real users on real devices may differ.
  Fix: use web-vitals library, track CWV in production.

PITFALL 9: Premature optimization
  Optimizing code that's already fast enough.
  Fix: measure first, optimize actual bottlenecks.

PITFALL 10: Ignoring mobile
  Test only on desktop with fast connection.
  Fix: Chrome DevTools → throttle CPU 4x + network Slow 3G.

PITFALL 11: Too many HTTP requests
  100 small files (even with HTTP/2) has overhead.
  Fix: reasonable bundling, sprite sheets for icons, inline small assets.

PITFALL 12: Memory leaks in SPA
  Event listeners, intervals, closures accumulate → tab crashes.
  Fix: cleanup in useEffect return, WeakRef, monitor heap.

PITFALL 13: Not using CDN
  Server in Frankfurt, user in Tokyo → 200ms RTT per request.
  Fix: CDN (Cloudflare, CloudFront) serves from nearest edge.

PITFALL 14: Blocking main thread
  Heavy computation in event handler → page freezes.
  Fix: Web Workers, requestIdleCallback, break into chunks.

PITFALL 15: No performance budget
  Each sprint adds more JS, more images, more features.
  Fix: set budget (170KB JS, LCP<2.5s), fail CI if exceeded.
```