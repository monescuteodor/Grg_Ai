# HTML5 Browser APIs Complete Reference


---

# CHAPTER 1: STORAGE APIs


## Remarks

Modern browsers provide powerful APIs that used to require server-side code or plugins. Understanding these APIs lets you build offline-capable, fast, feature-rich web applications.


## LocalStorage and SessionStorage

```javascript
// localStorage: persists across browser sessions
localStorage.setItem('theme', 'dark');
localStorage.setItem('user', JSON.stringify({ name: 'Alice', age: 30 }));

const theme = localStorage.getItem('theme');  // 'dark'
const user = JSON.parse(localStorage.getItem('user'));

localStorage.removeItem('theme');
localStorage.clear();  // Remove everything

// sessionStorage: cleared when tab closes
sessionStorage.setItem('temp', 'value');

// LIMITS: ~5-10 MB per origin
// BLOCKING: operations are synchronous (block main thread)
// SECURITY: accessible by any script on the page (XSS risk)
// Never store: passwords, tokens, sensitive data in localStorage!

// Listening for changes (cross-tab!)
window.addEventListener('storage', (e) => {
    console.log(`Key: ${e.key}, Old: ${e.oldValue}, New: ${e.newValue}`);
    // Fires when ANOTHER tab changes localStorage
});
```


## IndexedDB

```javascript
// IndexedDB: full database in the browser (async, large storage)

function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('MyAppDB', 1);
        
        request.onupgradeneeded = (e) => {
            const db = e.target.result;
            if (!db.objectStoreNames.contains('users')) {
                const store = db.createObjectStore('users', { keyPath: 'id', autoIncrement: true });
                store.createIndex('email', 'email', { unique: true });
                store.createIndex('age', 'age');
            }
        };
        
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function addUser(user) {
    const db = await openDB();
    const tx = db.transaction('users', 'readwrite');
    tx.objectStore('users').add(user);
    return new Promise((res, rej) => {
        tx.oncomplete = res;
        tx.onerror = rej;
    });
}

async function getUsers() {
    const db = await openDB();
    const tx = db.transaction('users', 'readonly');
    const request = tx.objectStore('users').getAll();
    return new Promise((res) => {
        request.onsuccess = () => res(request.result);
    });
}

// LIMITS: hundreds of MB (browser asks permission above ~50MB)
// ASYNC: non-blocking (unlike localStorage)
// USE FOR: offline data, caching API responses, large datasets
```


---

# CHAPTER 2: FETCH AND NETWORK APIs


## Fetch API

```javascript
// GET request
const response = await fetch('/api/users');
if (!response.ok) throw new Error(`HTTP ${response.status}`);
const users = await response.json();

// POST request
const newUser = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Alice', email: 'alice@example.com' }),
});

// With timeout
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000);

try {
    const response = await fetch('/api/data', {
        signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return await response.json();
} catch (err) {
    if (err.name === 'AbortError') {
        console.log('Request timed out');
    }
}

// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('name', 'Document');

await fetch('/api/upload', {
    method: 'POST',
    body: formData,  // No Content-Type header! Browser sets it with boundary.
});

// Download with progress
const response = await fetch('/api/large-file');
const reader = response.body.getReader();
const contentLength = +response.headers.get('Content-Length');
let receivedLength = 0;
const chunks = [];

while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    receivedLength += value.length;
    console.log(`Progress: ${(receivedLength / contentLength * 100).toFixed(1)}%`);
}
```


---

# CHAPTER 3: WEB WORKERS


## Offload Heavy Work

```javascript
// Web Workers run JavaScript in a BACKGROUND THREAD
// They don't block the main thread (UI stays responsive)

// main.js
const worker = new Worker('worker.js');

worker.postMessage({ type: 'sort', data: hugeArray });

worker.onmessage = (e) => {
    console.log('Sorted!', e.data.result);
};

worker.onerror = (e) => {
    console.error('Worker error:', e.message);
};

// worker.js
self.onmessage = (e) => {
    const { type, data } = e.data;

    if (type === 'sort') {
        const sorted = data.sort((a, b) => a - b);  // Heavy operation
        self.postMessage({ result: sorted });
    }
};

// INLINE WORKER (no separate file)
const workerCode = `
    self.onmessage = (e) => {
        const result = heavyComputation(e.data);
        self.postMessage(result);
    };
`;
const blob = new Blob([workerCode], { type: 'application/javascript' });
const worker = new Worker(URL.createObjectURL(blob));

// LIMITATIONS:
// No DOM access (no document, no window)
// No shared memory (communication via postMessage only)
// Can use: fetch, IndexedDB, WebSocket, timers, crypto
// USE FOR: data processing, image manipulation, search, sorting
```


---

# CHAPTER 4: CANVAS API


## 2D Drawing

```javascript
const canvas = document.createElement('canvas');
canvas.width = 800;
canvas.height = 600;
document.body.appendChild(canvas);
const ctx = canvas.getContext('2d');

// Shapes
ctx.fillStyle = '#3b82f6';
ctx.fillRect(50, 50, 200, 100);

ctx.strokeStyle = '#ef4444';
ctx.lineWidth = 3;
ctx.strokeRect(300, 50, 200, 100);

// Path (custom shapes)
ctx.beginPath();
ctx.moveTo(400, 300);
ctx.lineTo(500, 200);
ctx.lineTo(600, 300);
ctx.closePath();
ctx.fillStyle = '#10b981';
ctx.fill();

// Circle
ctx.beginPath();
ctx.arc(150, 300, 50, 0, Math.PI * 2);
ctx.fillStyle = '#f59e0b';
ctx.fill();

// Text
ctx.font = 'bold 24px Arial';
ctx.fillStyle = 'white';
ctx.textAlign = 'center';
ctx.fillText('Hello Canvas!', 400, 500);

// Gradient
const gradient = ctx.createLinearGradient(0, 0, 800, 0);
gradient.addColorStop(0, '#667eea');
gradient.addColorStop(1, '#764ba2');
ctx.fillStyle = gradient;
ctx.fillRect(0, 550, 800, 50);

// Image drawing
const img = new Image();
img.onload = () => ctx.drawImage(img, 0, 0, 100, 100);
img.src = 'sprite.png';

// Pixel manipulation
const imageData = ctx.getImageData(0, 0, 800, 600);
const pixels = imageData.data;  // Uint8ClampedArray [R,G,B,A, R,G,B,A, ...]
for (let i = 0; i < pixels.length; i += 4) {
    const gray = (pixels[i] + pixels[i+1] + pixels[i+2]) / 3;
    pixels[i] = gray;      // R
    pixels[i+1] = gray;    // G
    pixels[i+2] = gray;    // B
    // pixels[i+3] = alpha (unchanged)
}
ctx.putImageData(imageData, 0, 0);  // Grayscale filter!
```


---

# CHAPTER 5: COMMON PITFALLS

```
PITFALL 1: Blocking main thread with heavy computation
  Sorting 1M items on main thread → UI freezes.
  Fix: use Web Workers for heavy computation.

PITFALL 2: Not checking fetch response.ok
  fetch doesn't throw on HTTP errors (404, 500).
  Fix: if (!response.ok) throw new Error(...)

PITFALL 3: localStorage for sensitive data
  Any XSS script can read localStorage.
  Fix: use HttpOnly cookies for auth tokens.

PITFALL 4: Synchronous localStorage in hot paths
  localStorage.getItem() blocks. In a render loop → janky.
  Fix: read once on init, cache in memory.

PITFALL 5: Not handling offline state
  fetch fails silently when offline → blank page.
  Fix: try/catch fetch, show offline indicator, use cached data.

PITFALL 6: Canvas not retina-ready
  Blurry on high-DPI displays.
  Fix: canvas.width = 800 * devicePixelRatio; ctx.scale(dpr, dpr);

PITFALL 7: Memory leaks in Workers
  Creating workers without terminating → memory grows.
  Fix: worker.terminate() when done.

PITFALL 8: Forgetting CORS on fetch
  API works in Postman but not browser.
  Fix: server must send Access-Control-Allow-Origin header.
```