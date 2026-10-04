# Windows apps (native)

## Options
- **WinUI 3 / Windows App SDK** (C#/.NET) — modern native Windows UI (Fluent). Best for Windows-only desktop.
- **.NET MAUI** (C#) — one codebase for Windows + macOS + iOS + Android.
- **WPF** — mature, huge ecosystem, Windows-only, great for line-of-business apps.
- **WinForms** — simplest, legacy but fast to ship internal tools.

## WinUI 3 quickstart
```bash
dotnet new winui3 -n MyApp   # needs Windows App SDK + VS workload
dotnet build
```
- XAML for UI, C# code-behind or MVVM (CommunityToolkit.Mvvm).
- Async: use `async/await`; never block the UI thread.

## Packaging & install
- **MSIX** — modern, sandboxed, Store-ready. `makeappx` / VS packaging project.
- **Installer**: Inno Setup or WiX for a classic `.exe`/`.msi`.
- Sign with an EV code-signing cert to avoid SmartScreen warnings.

## Tips
- Settings: `Windows.Storage.ApplicationData` (packaged) or `%AppData%` (unpackaged).
- Notifications: Windows App SDK `AppNotificationManager`.
- For a quick cross-platform GUI in C#, prefer MAUI; for pure Windows polish, WinUI 3.
