# Progressive Web Apps (PWA) Complete Reference


---

# CHAPTER 1: PWA FUNDAMENTALS


## Remarks

A PWA is a web app that feels like a native app — installable, works offline, sends push notifications, and loads instantly. PWAs use Service Workers for caching, a Web App Manifest for installation, and HTTPS for security. Major PWAs: Twitter, Starbucks, Pinterest, Spotify (web), Grg AI (via Chrome install!).


## Web App Manifest

```json
// manifest.json
{
    "name": "Grg AI Assistant",
    "short_name": "Grg AI",
    "description": "AI-powered programming assistant",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0a0a0a",
    "theme_color": "#0a0a0a",
    "orientation": "any",
    "icons": [
        {
            "src": "/icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        },
        {
            "src": "/icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png"
        },
        {
            "src": "/icons/icon-maskable-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "maskable"
        }
    ]
}
```

```html
<!-- index.html -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#0a0a0a">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="apple-touch-icon" href="/icons/icon-192.png">
```


## Service Worker (Offline Support)

```javascript
// sw.js — Service Worker

const CACHE_NAME = 'grg-ai-v1';
const ASSETS = [
    '/',
    '/index.html',
    '/style.css',
    '/app.js',
    '/icons/icon-192.png',
];

// Install: cache essential assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(ASSETS))
            .then(() => self.skipWaiting())
    );
});

// Activate: clean old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(k => k !== CACHE_NAME)
                    .map(k => caches.delete(k))
            )
        ).then(() => self.clients.claim())
    );
});

// Fetch: serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    // Skip non-GET requests
    if (event.request.method !== 'GET') return;

    // Skip API calls (always go to network)
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request).catch(() =>
                new Response(JSON.stringify({ error: 'Offline' }),
                    { headers: { 'Content-Type': 'application/json' } })
            )
        );
        return;
    }

    // Cache-first strategy for static assets
    event.respondWith(
        caches.match(event.request).then(cached => {
            if (cached) return cached;
            return fetch(event.request).then(response => {
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                return response;
            });
        })
    );
});

// Register in main app
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(reg => console.log('SW registered'))
        .catch(err => console.error('SW failed:', err));
}
```


## Caching Strategies

```
CACHE-FIRST (static assets):
  Check cache → hit? Return cached.
  Miss? Fetch from network → cache → return.
  Best for: CSS, JS, images, fonts.

NETWORK-FIRST (API data):
  Try network → success? Cache and return.
  Fail? Return cached version.
  Best for: API responses, dynamic content.

STALE-WHILE-REVALIDATE (best of both):
  Return cached immediately (fast!).
  Simultaneously fetch fresh version → update cache.
  Next request gets fresh data.
  Best for: news feeds, user profiles.

NETWORK-ONLY (real-time):
  Always fetch from network. No caching.
  Best for: chat messages, stock prices.

CACHE-ONLY (fully offline):
  Only serve from cache. Never fetch.
  Best for: offline-first apps after initial sync.
```


---

# CHAPTER 2: INSTALLABILITY


## Install Prompt

```javascript
// Capture the install prompt
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();  // Don't show browser's default prompt
    deferredPrompt = e;
    showInstallButton();  // Show YOUR custom button
});

function handleInstallClick() {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();  // Show install dialog
    deferredPrompt.userChoice.then(result => {
        if (result.outcome === 'accepted') {
            console.log('App installed!');
        }
        deferredPrompt = null;
    });
}

// Detect if already installed
window.addEventListener('appinstalled', () => {
    console.log('PWA installed');
    hideInstallButton();
});

// Check if running as installed app
if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('Running as installed PWA');
}
```


## PWA Requirements Checklist

```
REQUIRED for installability:
  ✅ HTTPS (or localhost for development)
  ✅ Web App Manifest with name, icons (192px + 512px), start_url, display
  ✅ Service Worker registered
  ✅ User engagement (visited at least twice, 30+ seconds apart)

RECOMMENDED:
  ✅ Offline page (show something useful when offline)
  ✅ Fast loading (<3 seconds on 3G)
  ✅ Responsive design (works on any screen size)
  ✅ App-like navigation (no browser chrome in standalone mode)
  ✅ Splash screen (background_color + icons in manifest)

TEST WITH:
  Chrome DevTools → Application tab → Manifest / Service Workers
  Lighthouse audit → PWA section
  chrome://flags → #bypass-app-banner-engagement-checks (skip wait for testing)
```


---

# CHAPTER 3: COMMON PITFALLS

```
PITFALL 1: Caching API responses indefinitely
  User sees stale data forever.
  Fix: network-first for API calls, or stale-while-revalidate with TTL.

PITFALL 2: Not versioning cache
  Updated app but old cache still served → users see old version.
  Fix: change CACHE_NAME on each deploy ('v1' → 'v2').

PITFALL 3: Service worker scope
  SW at /js/sw.js can only control /js/* paths.
  Fix: place sw.js at root (/).

PITFALL 4: Not handling SW updates
  New SW waits until all tabs close → user never gets update.
  Fix: skipWaiting() + clients.claim(), or prompt user to refresh.

PITFALL 5: Caching too much
  Caching 500MB of assets → user's storage fills up.
  Fix: cache only essential assets. Set storage limits.

PITFALL 6: No offline fallback
  Offline user sees browser's default error page.
  Fix: cache an offline.html page, serve it when network fails.
```