# CLI tools

## Pick language
- **Node/TS**: `commander` or `yargs`; ship via npm (`bin` field) or `pkg`/Bun to a binary.
- **Python**: `typer` (modern) or `argparse`; ship via `pipx` or PyInstaller.
- **Go**: `cobra`; compiles to a single static binary — best for distribution.

## Node example (commander)
```js
#!/usr/bin/env node
import { program } from 'commander';
program.name('greet').argument('<name>').option('-l, --loud')
  .action((name,o)=> console.log(o.loud ? `HI ${name.toUpperCase()}!` : `hi ${name}`));
program.parse();
```
```json
// package.json
{ "bin": { "greet": "./cli.js" }, "type": "module" }
```

## Good CLI UX
- `--help` for every command; sensible defaults; `--json` for machine output.
- Exit codes: 0 ok, non-zero on error. Read stdin when piped.
- Progress + color for humans, but detect non-TTY and stay plain. Config via flags > env > file.
- Distribute: npm, Homebrew tap, `curl | sh` installer, or GitHub Releases binaries.
