# Linux apps (native + packaging)

## GUI toolkits
- **GTK 4** (+ libadwaita) — GNOME-native look; language: C, Rust (gtk-rs), Python (PyGObject), Vala.
- **Qt 6** (C++ or Python/PySide6) — cross-platform, powerful widgets, great tooling.
- Web-based (Tauri/Electron) also works well — see `desktop-cross-platform`.

## Python + GTK quickstart
```python
import gi; gi.require_version('Gtk','4.0')
from gi.repository import Gtk
class App(Gtk.Application):
    def do_activate(self):
        w = Gtk.ApplicationWindow(application=self, title='Hi')
        w.set_child(Gtk.Label(label='Hello Linux')); w.present()
App().run()
```

## Packaging (pick one+)
- **Flatpak** — sandboxed, distro-agnostic, Flathub distribution. `flatpak-builder` + a manifest.
- **AppImage** — single portable file, run anywhere. `appimagetool`.
- **Snap** — Ubuntu-centric. `snapcraft`.
- Distro packages: `.deb` (Debian/Ubuntu), `.rpm` (Fedora).

## Services
- Background daemons: a `systemd` unit in `~/.config/systemd/user/` or `/etc/systemd/system/`.
- Desktop entry: a `.desktop` file in `~/.local/share/applications/` for menu integration.
