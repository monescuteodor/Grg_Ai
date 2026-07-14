# Electron Desktop Apps Complete Reference


---

# CHAPTER 1: ELECTRON BASICS


## Remarks

Electron lets you build cross-platform desktop apps using HTML, CSS, and JavaScript. One codebase → runs on Windows, macOS, and Linux. VS Code, Discord, Slack, Notion, Figma Desktop, and Spotify Desktop are all Electron apps. Electron bundles Chromium (browser) + Node.js into a single executable.


## Architecture

```
ELECTRON APP STRUCTURE:
  ┌─────────────────────────────────────┐
  │           MAIN PROCESS              │
  │  (Node.js — has full OS access)     │
  │  - File system, networking          │
  │  - System tray, menus, dialogs      │
  │  - Creates BrowserWindow(s)         │
  │  - Runs: main.js                    │
  └──────────┬──────────────────────────┘
             │ IPC (Inter-Process Communication)
  ┌──────────┴──────────────────────────┐
  │         RENDERER PROCESS             │
  │  (Chromium — your web UI)            │
  │  - HTML, CSS, JavaScript             │
  │  - React/Vue/Angular/vanilla         │
  │  - NO direct OS access (sandboxed)   │
  │  - Runs: index.html                  │
  └──────────────────────────────────────┘

SECURITY: Renderer is sandboxed. To access OS features,
it sends messages to Main via IPC (like client-server).
```


## Quick Start

```javascript
// main.js (Main Process)
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,   // Security: isolate renderer
            nodeIntegration: false,   // Security: no Node in renderer
        },
    });

    mainWindow.loadFile('index.html');
    // Or: mainWindow.loadURL('http://localhost:3000');  // For dev with React

    // Open DevTools in development
    if (process.env.NODE_ENV === 'development') {
        mainWindow.webContents.openDevTools();
    }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// IPC: handle messages from renderer
ipcMain.handle('read-file', async (event, filePath) => {
    const fs = require('fs').promises;
    return await fs.readFile(filePath, 'utf-8');
});

ipcMain.handle('save-file', async (event, filePath, content) => {
    const fs = require('fs').promises;
    await fs.writeFile(filePath, content, 'utf-8');
    return true;
});
```

```javascript
// preload.js (Bridge between Main and Renderer)
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    readFile: (path) => ipcRenderer.invoke('read-file', path),
    saveFile: (path, content) => ipcRenderer.invoke('save-file', path, content),
    onMenuAction: (callback) => ipcRenderer.on('menu-action', callback),
});
// Renderer can now call window.electronAPI.readFile(...)
// But CANNOT access Node.js directly (secure!)
```

```html
<!-- index.html (Renderer Process) -->
<!DOCTYPE html>
<html>
<head>
    <title>My Electron App</title>
    <style>
        body { font-family: system-ui; margin: 0; padding: 20px; background: #1a1a2e; color: #eee; }
        textarea { width: 100%; height: 400px; background: #16213e; color: #eee; border: 1px solid #333; padding: 12px; font-family: monospace; }
        button { background: #3b82f6; color: white; border: none; padding: 8px 16px; cursor: pointer; margin: 8px 4px; }
    </style>
</head>
<body>
    <h1>Text Editor</h1>
    <button onclick="openFile()">Open</button>
    <button onclick="saveFile()">Save</button>
    <textarea id="editor"></textarea>

    <script>
        let currentPath = null;

        async function openFile() {
            // In real app: use dialog.showOpenDialog via IPC
            const path = prompt('File path:');
            if (!path) return;
            const content = await window.electronAPI.readFile(path);
            document.getElementById('editor').value = content;
            currentPath = path;
        }

        async function saveFile() {
            if (!currentPath) { currentPath = prompt('Save as:'); }
            if (!currentPath) return;
            const content = document.getElementById('editor').value;
            await window.electronAPI.saveFile(currentPath, content);
            alert('Saved!');
        }
    </script>
</body>
</html>
```


## Project Setup

```json
// package.json
{
    "name": "my-electron-app",
    "version": "1.0.0",
    "main": "main.js",
    "scripts": {
        "start": "electron .",
        "build:win": "electron-builder --win",
        "build:mac": "electron-builder --mac",
        "build:linux": "electron-builder --linux"
    },
    "devDependencies": {
        "electron": "^31.0.0",
        "electron-builder": "^24.0.0"
    },
    "build": {
        "appId": "com.myapp.desktop",
        "productName": "My App",
        "win": { "target": "nsis" },
        "mac": { "target": "dmg" },
        "linux": { "target": "AppImage" }
    }
}
```

```bash
# Setup
mkdir my-app && cd my-app
npm init -y
npm install --save-dev electron electron-builder

# Run in development
npm start

# Build for distribution
npm run build:win      # Creates .exe installer
npm run build:mac      # Creates .dmg
npm run build:linux    # Creates .AppImage
```


---

# CHAPTER 2: ALTERNATIVES TO ELECTRON


## Lighter Options

```
ELECTRON:
  Pro:  Mature, huge ecosystem, Chrome DevTools
  Con:  ~150MB binary (bundles Chromium), high RAM (~200MB+)
  Use:  Full-featured desktop apps (VS Code, Discord)

TAURI (Rust + WebView):
  Pro:  ~3-10MB binary, low RAM, uses system WebView
  Con:  Newer, smaller ecosystem, Rust backend
  Use:  Lightweight apps where size matters

NEUTRALINO:
  Pro:  ~2MB binary, uses system browser
  Con:  Limited OS APIs compared to Electron
  Use:  Simple utility apps

FLUTTER DESKTOP:
  Pro:  Native rendering (not web), same code as mobile
  Con:  Dart language, larger runtime
  Use:  Cross-platform (mobile + desktop) from one codebase

PWA (Progressive Web App):
  Pro:  0MB install, no bundled browser, auto-updates
  Con:  Limited OS access (no file system, no system tray)
  Use:  Web apps that need "installable" feel (Grg AI!)
```


---

# CHAPTER 3: COMMON PITFALLS

```
PITFALL 1: Enabling nodeIntegration in renderer
  Renderer has full Node.js access → any XSS = full system access!
  Fix: nodeIntegration: false, contextIsolation: true. Use preload bridge.

PITFALL 2: Giant app size
  Electron bundles Chromium (~150MB) + your code.
  Fix: if size matters, use Tauri (~5MB). Or accept the trade-off.

PITFALL 3: High memory usage
  Each Electron window is a Chrome tab (~100MB).
  Fix: minimize windows, lazy-load content, use single-window design.

PITFALL 4: Not using IPC properly
  Directly calling Node APIs from renderer → security hole.
  Fix: whitelist specific IPC handlers in preload.js.

PITFALL 5: No auto-update
  Users stuck on old version forever.
  Fix: electron-updater for automatic updates on launch.

PITFALL 6: Slow startup
  Cold start takes 3-5 seconds.
  Fix: show splash screen, lazy-load heavy modules, use V8 snapshots.
```