# Grg Code power features (MCP, sub-agents, commands, patches, memory)

These make Grg Code as capable as Claude Code / Cursor / Codex. Use them.

## Sub-agents — `task` tool
Delegate a focused, read-only investigation to a sub-agent with its own clean context.
- Good for: "explore how auth works", "find where X is defined and who calls it", "research the current Expo Router API".
- The sub-agent has read_file/list_dir/search/web_search/fetch_url/knowledge and returns a concise summary.
- Call: `task({ description:"map the auth flow", prompt:"Read the codebase and summarize how login works: files, tokens, where sessions are stored." })`
- Use it instead of dozens of read/search calls in your own context.

## Multi-file edits — `apply_patch` tool
Change several files in ONE atomic, approved step.
- Each change: `{path, old_string, new_string}` to edit, or `{path, new_string}` (no old_string) to create/overwrite.
- All edits are validated first (old_string must exist and be unique); if any fails, NOTHING is applied — fix and retry.
- Prefer this for refactors touching many files.

## Project memory — `GRGCODE.md` + `remember` tool
Grg Code loads `GRGCODE.md` (or `.grgcode/GRGCODE.md`, `AGENTS.md`, `CLAUDE.md`) from the project root into context every session.
- Put durable conventions there: how to run/build/test, code style, architecture, gotchas.
- Save a fact with `remember({ note:"Run tests with `npm test`; uses Vitest." })` (asks approval, appends to GRGCODE.md).
- The `/init` command generates a GRGCODE.md by exploring the project.

## Slash commands — reusable prompts
Type `/name args` in the composer. Built-ins: /review, /test, /explain, /fix, /commit, /optimize, /init, /scaffold.
- Project commands: add markdown files in `.grgcode/commands/<name>.md`; `$ARGUMENTS` is replaced with what the user typed after the command. Project files override built-ins.
- Example `.grgcode/commands/pr.md`: `Open a PR: run tests, then `gh pr create` with a summary of: $ARGUMENTS`

## MCP — connect external tools
Grg Code is an MCP client. Configure servers in `.grgcode/mcp.json` (project) or `~/.grgcode/mcp.json` (global), Claude-Desktop format:
```json
{
  "mcpServers": {
    "filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "."] },
    "github":     { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"], "env": { "GITHUB_TOKEN": "ghp_..." } }
  }
}
```
- On folder open (or app start for the global file) Grg Code spawns each server, lists its tools and exposes them as `mcp__<server>__<tool>`. Call them like any tool.
- Popular servers: filesystem, github, postgres, sqlite, puppeteer/playwright, brave-search, memory, slack. Least-privilege tokens only.
- If a server needs installing, it runs via `npx -y ...` on first use (needs Node). Tell the user which server + config to add if a capability is missing.
