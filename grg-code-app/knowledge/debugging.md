# Debugging (systematic)

## Method
1. **Reproduce** reliably. Find the smallest input that triggers it.
2. **Read the error** — full stack trace, top frame in YOUR code. The message usually says what's wrong.
3. **Localize** — bisect: comment out / `git bisect` / binary-search the code path. Add logging around the suspect.
4. **Form a hypothesis**, test it with one change. Change one thing at a time.
5. **Fix the root cause**, not the symptom. Add a test that reproduces it so it can't regress.
6. **Verify** the fix and check you didn't break anything nearby.

## Tools
- Breakpoints/step-debugging (VS Code debugger, `node --inspect`, `pdb`/`breakpoint()`).
- `console.log`/`print` with labels + values; log types and shapes, not just "here".
- Network tab / curl for API issues; check status, headers, body.
- For "works locally, fails in prod": compare env vars, versions, data, and permissions.

## Common causes
- Off-by-one, null/undefined, async race / missing await, wrong types, stale cache, env misconfig, timezone/encoding.
