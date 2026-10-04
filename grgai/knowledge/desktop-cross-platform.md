# Desktop apps — cross-platform (Electron vs Tauri)

## Choose
- **Tauri 2** (Rust + web UI): tiny binaries (~3-10MB), low RAM, secure by default. Best default for new desktop apps. Needs Rust toolchain.
- **Electron**: heavier (~100MB+), but maximum ecosystem/Node access. Use when you need deep Node/native modules or the team only knows JS.
- Native (WinUI/SwiftUI/GTK) → see `windows-apps`, `macos-apps`, `linux-apps`.

## Tauri quickstart
```bash
npm create tauri-app@latest         # pick a frontend (React/Vue/Svelte/vanilla)
cd app && npm install
npm run tauri dev                   # dev
npm run tauri build                 # produces installers per-OS
```
- Frontend is a normal web app in `src/`. Rust backend commands in `src-tauri/src/`.
- IPC: `#[tauri::command]` in Rust, `invoke('cmd', {args})` in JS.
- Bundles: `.msi`/`.exe` (Win), `.dmg`/`.app` (macOS), `.deb`/`.AppImage` (Linux).

## Electron quickstart
```bash
npm create @quick-start/electron    # Vite + Electron scaffold
```
- 3 processes: main (Node), preload (bridge, `contextBridge.exposeInMainWorld`), renderer (UI). Keep `contextIsolation:true`, `nodeIntegration:false`.
- Package with `electron-builder` (targets: nsis, dmg, AppImage). Sign for distribution.

## Gotchas
- Auto-update: Tauri updater / electron-updater + a release server.
- File paths differ per OS — use the framework's path APIs.
- Code signing is required for smooth installs (Win: EV cert; macOS: notarization).
