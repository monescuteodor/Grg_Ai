'use strict';
const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const fs = require('fs');
const os = require('os');
const http = require('http');
const { exec, spawn } = require('child_process');

const BACKEND = 'https://grg-ai.com';
const MAX_ITERS = 30;
// This build's version number — BUMP with each release (must match the vN in artifactName).
// Hardcoded on purpose: electron-builder strips the `build` field from the packaged
// package.json, so reading artifactName at runtime returned 0 and the updater always fired.
const APP_VERSION = 37;

let win = null;
let projectDir = process.cwd();
let conversation = [];
let cancelled = false;
let running = false;
let autoApprove = false;
let agentModel = 'auto';  // AutoGrg by default — the backend classifies the task and routes to the best affordable model
let agentUid = null;  // set from the renderer when signed in; used for premium gating/metering
let activeAgent = null;  // {id,name,prompt,privacy} — a specialist agent chosen in the renderer (null = normal Grg Code)
// Privacy preamble (only added for a PRIVATE agent): the renderer redacts the user's typed
// PII to placeholders before it reaches the model, and restores them locally in the reply.
const GRGAGENT_PRIVACY = 'PRIVACY MODE: the user\'s sensitive data (emails, phone numbers, national IDs/CNP, IBANs, card numbers, API secrets) in their typed messages has been REDACTED to typed placeholders like [EMAIL_1], [IBAN_1], [SECRET_1]. Treat each placeholder as a real value of that type, reason about it normally, and ALWAYS keep the exact placeholder tokens verbatim in your reply — never invent, alter or guess the real values; the client substitutes them back locally.';
const pendingApprovals = new Map();
let curCheckpoint = null;      // active per-task snapshot of files about to change
const checkpoints = [];        // history of {id, ts, user, ops:[{path, before, existed}]}

// ─────────────────────────── window ───────────────────────────
function createWindow() {
    win = new BrowserWindow({
        width: 1180,
        height: 800,
        minWidth: 720,
        minHeight: 520,
        backgroundColor: '#0a0711',
        title: 'Grg Code',
        icon: path.join(__dirname, 'renderer', 'icon.ico'),
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        }
    });
    win.setMenuBarVisibility(false);
    win.loadFile(path.join(__dirname, 'renderer', 'index.html'));
}

app.whenReady().then(() => {
    // Start with NO folder — the user can pick one for file work, or just chat.
    projectDir = null;
    createWindow();
    setTimeout(() => { try { initMCP(); } catch (e) {} }, 800);  // connect any global MCP servers (~/.grgcode/mcp.json)
    app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });

function send(channel, payload) { if (win && !win.isDestroyed()) win.webContents.send(channel, payload); }

// ─────────────────────────── path safety ───────────────────────────
function safeResolve(p) {
    if (!projectDir) throw new Error('No project folder is selected.');
    const target = path.resolve(projectDir, p || '.');
    const root = path.resolve(projectDir);
    if (target !== root && !target.startsWith(root + path.sep)) {
        throw new Error('Path is outside the project folder: ' + p);
    }
    return target;
}
const _FILE_TOOLS = new Set(['list_dir', 'read_file', 'write_file', 'edit_file', 'search', 'git']);

// ─────────────────────────── tools ───────────────────────────
const TOOLS = [
    { type: 'function', function: { name: 'list_dir', description: 'List files and folders in a directory (relative to the project root).', parameters: { type: 'object', properties: { path: { type: 'string', description: 'Directory path, default "."' } } } } },
    { type: 'function', function: { name: 'read_file', description: 'Read a text file. For big files read in chunks with offset (1-indexed start line) + limit (number of lines) so you only pull what you need — this keeps you well under the token/minute limit. Omit them to get the first ~500 lines.', parameters: { type: 'object', properties: { path: { type: 'string' }, offset: { type: 'integer', description: 'start line (1-indexed)' }, limit: { type: 'integer', description: 'how many lines' } }, required: ['path'] } } },
    { type: 'function', function: { name: 'write_file', description: 'Create or overwrite a file with the given content. Requires user approval.', parameters: { type: 'object', properties: { path: { type: 'string' }, content: { type: 'string' } }, required: ['path', 'content'] } } },
    { type: 'function', function: { name: 'edit_file', description: 'Replace an exact substring in a file with new text. Requires user approval.', parameters: { type: 'object', properties: { path: { type: 'string' }, old_string: { type: 'string' }, new_string: { type: 'string' } }, required: ['path', 'old_string', 'new_string'] } } },
    { type: 'function', function: { name: 'run_command', description: 'Run a shell command in the project folder and return its output. Requires user approval.', parameters: { type: 'object', properties: { command: { type: 'string' } }, required: ['command'] } } },
    { type: 'function', function: { name: 'search', description: 'Search the project files for a text/regex pattern (like grep).', parameters: { type: 'object', properties: { query: { type: 'string' }, path: { type: 'string', description: 'Subdirectory to search, default "."' } }, required: ['query'] } } },
    { type: 'function', function: { name: 'git', description: 'Run a git command in the project folder, e.g. "status -s", "diff", "log --oneline -10", "add -A", "commit -m \\"message\\"". Read-only subcommands (status, diff, log, show, branch, remote, ls-files, rev-parse, describe, blame) run without approval; anything that changes the repo requires user approval.', parameters: { type: 'object', properties: { args: { type: 'string', description: 'Arguments after "git", e.g. "status -s".' } }, required: ['args'] } } },
    { type: 'function', function: { name: 'knowledge', description: 'Load Grg Code\'s app/web-building knowledge base (best practices, patterns, boilerplates). Call with no topic to list available topics; call with a topic to read that guide. Use it BEFORE scaffolding or building an app/website so you follow current best practices.', parameters: { type: 'object', properties: { topic: { type: 'string', description: 'A topic slug from the list (e.g. "nextjs"). Omit to list all topics.' } } } } },
    { type: 'function', function: { name: 'create_document', description: 'Create a real Office file — PowerPoint (.pptx), Excel (.xlsx) or Word (.docx) — and save it to the folder. Use for presentations, spreadsheets, and documents. Requires user approval.', parameters: { type: 'object', properties: { spec: { type: 'string', description: 'JSON spec. pptx: {"type":"pptx","filename":"name","title":"...","slides":[{"title":"...","bullets":["..."]}]}. xlsx: {"type":"xlsx","filename":"name","sheets":[{"name":"Sheet1","headers":["A","B"],"rows":[["x",1]]}]}. docx: {"type":"docx","filename":"name","title":"...","sections":[{"heading":"H","level":1,"paragraphs":["..."],"bullets":["..."]}]}.' } }, required: ['spec'] } } },
    { type: 'function', function: { name: 'web_search', description: 'Search the web (DuckDuckGo) for CURRENT info: library versions, APIs, docs, app-store rules, prices, hardware. Returns titles, URLs and snippets. Read-only, no approval needed.', parameters: { type: 'object', properties: { query: { type: 'string' }, n: { type: 'integer', description: 'max results (default 5)' } }, required: ['query'] } } },
    { type: 'function', function: { name: 'fetch_url', description: 'Fetch a web page and return its readable text — use to read a doc/page found via web_search. Read-only, no approval needed.', parameters: { type: 'object', properties: { url: { type: 'string' } }, required: ['url'] } } },
    { type: 'function', function: { name: 'update_plan', description: 'Create or update your visible step-by-step task plan (a TODO checklist shown to the user). Call it at the START of any multi-step task and whenever a step changes status. Use it to think through the work and track progress so you never stop early.', parameters: { type: 'object', properties: { steps: { type: 'array', items: { type: 'object', properties: { title: { type: 'string' }, status: { type: 'string', enum: ['pending', 'in_progress', 'done'] } }, required: ['title'] } } }, required: ['steps'] } } },
    { type: 'function', function: { name: 'scaffold', description: 'Scaffold a full starter project from Grg Code\'s template library. Call with NO template to list templates; call with a template name to write all its files into the project. Requires user approval. After scaffolding, tell the user the run commands.', parameters: { type: 'object', properties: { template: { type: 'string', description: 'Template name (omit to list all).' }, dir: { type: 'string', description: 'Optional subfolder to scaffold into (default project root).' } } } } },
    { type: 'function', function: { name: 'apply_patch', description: 'Apply MULTIPLE file changes at once (multi-file edit). For each change: give path + old_string + new_string to edit, OR path + new_string only (omit old_string) to create/overwrite a file. All edits are validated first (old_string must exist and be unique); if any fails, nothing is applied. One approval covers the whole patch. Prefer this for multi-file refactors.', parameters: { type: 'object', properties: { changes: { type: 'array', items: { type: 'object', properties: { path: { type: 'string' }, old_string: { type: 'string', description: 'omit to create/overwrite the file' }, new_string: { type: 'string' } }, required: ['path', 'new_string'] } } }, required: ['changes'] } } },
    { type: 'function', function: { name: 'task', description: 'Spawn a focused sub-agent to investigate/research ONE thing and report back a concise answer (e.g. "explore how auth works", "find where X is defined", "research the latest Expo router API"). The sub-agent has read-only + web tools and its own context, so it keeps your main context clean. Use it for exploration and research you would otherwise do with many read/search calls.', parameters: { type: 'object', properties: { description: { type: 'string', description: 'Short label for the sub-task.' }, prompt: { type: 'string', description: 'Full instructions for the sub-agent.' } }, required: ['description', 'prompt'] } } },
    { type: 'function', function: { name: 'remember', description: 'Save a durable project convention/fact to GRGCODE.md (project memory that is loaded into your context every session). Use when you learn how this repo wants things done (build/test commands, style, gotchas). Requires user approval.', parameters: { type: 'object', properties: { note: { type: 'string' } }, required: ['note'] } } },
    { type: 'function', function: { name: 'image_search', description: 'Find REAL photos for a query (keyless: Openverse/Wikimedia). Returns real image URLs + attribution. Use to put real, relevant images in what you build (a location, product, food, mood, etc.).', parameters: { type: 'object', properties: { query: { type: 'string' }, n: { type: 'integer', description: 'how many (default 5)' } }, required: ['query'] } } },
    { type: 'function', function: { name: 'add_image', description: 'Download a REAL photo for a query and save it into the project (for apps/sites that need LOCAL image files). Requires user approval. Note: for plain web/HTML you can instead just use <img src="https://grg-ai.com/img?q=keywords"> which resolves to a real photo with no download.', parameters: { type: 'object', properties: { query: { type: 'string' }, path: { type: 'string', description: 'where to save, e.g. public/images/hero.jpg (default assets/images/<query>.jpg)' } }, required: ['query'] } } }
];
const GIT_READONLY = new Set(['status', 'diff', 'log', 'show', 'branch', 'remote', 'ls-files', 'rev-parse', 'describe', 'blame', 'shortlog']);

// ─── Knowledge base / skills (app/web building) ───
// Merged from bundled defaults + global (~/.grgcode/knowledge) + project
// (.grgcode/app_building_knowledge). Project overrides global overrides bundled.
function kbDirFor(scope) {
    if (scope === 'bundled') return path.join(__dirname, 'knowledge');
    if (scope === 'global') return path.join(os.homedir(), '.grgcode', 'knowledge');
    if (scope === 'project') return projectDir ? path.join(projectDir, '.grgcode', 'app_building_knowledge') : null;
    return null;
}
function kbListIn(scope) {
    const d = kbDirFor(scope); if (!d) return [];
    try {
        return fs.readdirSync(d).filter(f => /\.(md|json|txt)$/i.test(f)).map(f => {
            let body = ''; try { body = fs.readFileSync(path.join(d, f), 'utf8'); } catch (e) {}
            return { name: f.replace(/\.[^.]+$/, ''), body };
        }).sort((a, b) => a.name.localeCompare(b.name));
    } catch (e) { return []; }
}
function kbList() {
    const names = new Set();
    ['bundled', 'global', 'project'].forEach(s => kbListIn(s).forEach(c => names.add(c.name)));
    return Array.from(names).sort();
}
function kbRead(topic) {
    const slug = String(topic || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    for (const s of ['project', 'global', 'bundled']) { // project overrides global overrides bundled
        const d = kbDirFor(s); if (!d) continue;
        for (const ext of ['md', 'json', 'txt']) {
            const f = path.join(d, slug + '.' + ext);
            try { if (fs.existsSync(f)) return fs.readFileSync(f, 'utf8').slice(0, 8000); } catch (e) {}
        }
    }
    return 'No knowledge doc named "' + topic + '". Available: ' + kbList().join(', ');
}

// ─── Scaffold templates (starter projects) ───
// Merged: bundled (__dirname/templates) + global (~/.grgcode/templates) + project (.grgcode/templates).
function tplDirFor(scope) {
    if (scope === 'bundled') return path.join(__dirname, 'templates');
    if (scope === 'global') return path.join(os.homedir(), '.grgcode', 'templates');
    if (scope === 'project') return projectDir ? path.join(projectDir, '.grgcode', 'templates') : null;
    return null;
}
function tplListIn(scope) {
    const d = tplDirFor(scope); if (!d) return [];
    try {
        return fs.readdirSync(d).filter(f => /\.json$/i.test(f)).map(f => {
            let raw = '', obj = null; try { raw = fs.readFileSync(path.join(d, f), 'utf8'); obj = JSON.parse(raw); } catch (e) {}
            return { name: f.replace(/\.json$/i, ''), raw, obj };
        }).sort((a, b) => a.name.localeCompare(b.name));
    } catch (e) { return []; }
}
function tplList() {
    const names = new Set();
    ['bundled', 'global', 'project'].forEach(s => tplListIn(s).forEach(t => names.add(t.name)));
    return Array.from(names).sort();
}
function tplRead(name) {
    const slug = String(name || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    for (const s of ['project', 'global', 'bundled']) { // project overrides global overrides bundled
        const d = tplDirFor(s); if (!d) continue;
        const f = path.join(d, slug + '.json');
        try { if (fs.existsSync(f)) return JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) {}
    }
    return null;
}

function listDir(p) {
    const dir = safeResolve(p || '.');
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    const lines = entries
        .filter(e => !['node_modules', '.git', 'dist', '.venv', '__pycache__'].includes(e.name))
        .slice(0, 300)
        .map(e => (e.isDirectory() ? '[dir]  ' : '       ') + e.name);
    return (lines.join('\n') || '(empty)');
}
function readFile(p, offset, limit) {
    const f = safeResolve(p);
    const stat = fs.statSync(f);
    if (stat.size > 3 * 1024 * 1024) return '(file too large: ' + Math.round(stat.size / 1024) + ' KB — use search, or read_file with offset/limit)';
    const text = fs.readFileSync(f, 'utf8');
    const lines = text.split('\n');
    const total = lines.length;
    const DEFAULT = 500;   // lines returned when no range is asked (keeps free-tier token use low)
    if (offset != null || limit != null) {
        const start = Math.max(0, (parseInt(offset) || 1) - 1);   // 1-indexed
        const lim = limit != null ? Math.max(1, parseInt(limit)) : DEFAULT;
        const slice = lines.slice(start, start + lim);
        const more = (start + slice.length) < total ? '  (more below — call read_file with offset=' + (start + slice.length + 1) + ')' : '';
        return 'Lines ' + (start + 1) + '-' + (start + slice.length) + ' of ' + total + ':' + more + '\n' + slice.join('\n');
    }
    if (total > DEFAULT) {
        return 'File has ' + total + ' lines; showing 1-' + DEFAULT + ' (call read_file with offset/limit for the rest):\n' + lines.slice(0, DEFAULT).join('\n');
    }
    return text;
}
function writeFile(p, content) {
    const f = safeResolve(p);
    fs.mkdirSync(path.dirname(f), { recursive: true });
    fs.writeFileSync(f, content == null ? '' : String(content), 'utf8');
    return 'Wrote ' + p + ' (' + Buffer.byteLength(content || '') + ' bytes)';
}
function editFile(p, oldStr, newStr) {
    const f = safeResolve(p);
    let text = fs.readFileSync(f, 'utf8');
    if (!text.includes(oldStr)) return 'ERROR: old_string not found in ' + p + '. Read the file first to get the exact text.';
    const count = text.split(oldStr).length - 1;
    if (count > 1) return 'ERROR: old_string appears ' + count + ' times in ' + p + '; make it unique.';
    text = text.replace(oldStr, newStr);
    fs.writeFileSync(f, text, 'utf8');
    return 'Edited ' + p;
}
// ─── Checkpoints: snapshot a file's contents before the agent changes it ───
function recordBefore(rel) {
    if (!curCheckpoint || !rel) return;
    if (curCheckpoint.ops.some(o => o.path === rel)) return;   // only the first change per file
    let before = null, existed = false;
    try { before = fs.readFileSync(safeResolve(rel), 'utf8'); existed = true; } catch (e) { existed = false; }
    curCheckpoint.ops.push({ path: rel, before: before, existed: existed });
}
function revertCheckpoint(id) {
    const cp = checkpoints.find(c => c.id === id);
    if (!cp) return { error: 'checkpoint not found' };
    let restored = 0, removed = 0;
    for (let i = cp.ops.length - 1; i >= 0; i--) {
        const op = cp.ops[i];
        try {
            if (op.existed) { const f = safeResolve(op.path); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, op.before, 'utf8'); restored++; }
            else { try { fs.unlinkSync(safeResolve(op.path)); removed++; } catch (e) {} }
        } catch (e) {}
    }
    cp.reverted = true;
    return { ok: true, restored: restored, removed: removed, files: cp.ops.map(o => o.path) };
}

// ─── @-file mentions: flat project file list + expand "@path" into context ───
function flatFiles(rel, depth, out) {
    rel = rel || '.'; depth = depth || 0; out = out || [];
    if (out.length > 4000) return out;
    const skip = new Set(['node_modules', '.git', 'dist', 'build', '.next', '.venv', '__pycache__', '.cache', '.grgcode']);
    let abs; try { abs = safeResolve(rel); } catch (e) { return out; }
    let entries; try { entries = fs.readdirSync(abs, { withFileTypes: true }); } catch (e) { return out; }
    for (const e of entries) {
        if (skip.has(e.name)) continue;
        const child = (rel === '.' ? '' : rel + '/') + e.name;
        if (e.isDirectory()) { if (depth < 6) flatFiles(child, depth + 1, out); }
        else out.push(child);
    }
    return out;
}
function expandMentions(text) {
    if (!projectDir || !text || text.indexOf('@') < 0) return '';
    const seen = {}; const parts = []; let m;
    const re = /@([\w./\\-]+)/g;
    while ((m = re.exec(text)) !== null) {
        let rel = m[1].replace(/\\/g, '/'); if (seen[rel]) continue; seen[rel] = 1;
        try {
            const f = safeResolve(rel);
            if (fs.existsSync(f) && fs.statSync(f).isFile()) {
                let c = fs.readFileSync(f, 'utf8'); if (c.length > 6000) c = c.slice(0, 6000) + '\n… [truncated]';
                parts.push('=== ' + rel + ' ===\n' + c);
            }
        } catch (e) {}
        if (parts.join('').length > 20000) break;
    }
    return parts.length ? 'Files the user referenced with @ (use them as context):\n\n' + parts.join('\n\n') : '';
}

function runCommand(command) {
    return new Promise((resolve) => {
        exec(command, { cwd: projectDir, timeout: 120000, maxBuffer: 4 * 1024 * 1024, windowsHide: true }, (err, stdout, stderr) => {
            let out = '';
            if (stdout) out += stdout;
            if (stderr) out += (out ? '\n' : '') + stderr;
            if (err && err.killed) out += '\n[command timed out]';
            if (err && typeof err.code === 'number') out += '\n[exit code ' + err.code + ']';
            resolve(out.trim() || '(no output)');
        });
    });
}
function search(query, p) {
    const root = safeResolve(p || '.');
    const results = [];
    let re;
    try { re = new RegExp(query, 'i'); } catch (e) { re = null; }
    const skip = new Set(['node_modules', '.git', 'dist', '.venv', '__pycache__']);
    function walk(dir, depth) {
        if (depth > 6 || results.length >= 60) return;
        let entries;
        try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return; }
        for (const e of entries) {
            if (results.length >= 60) break;
            if (skip.has(e.name)) continue;
            const full = path.join(dir, e.name);
            if (e.isDirectory()) walk(full, depth + 1);
            else {
                try {
                    if (fs.statSync(full).size > 500 * 1024) continue;
                    const content = fs.readFileSync(full, 'utf8');
                    const lines = content.split('\n');
                    for (let i = 0; i < lines.length; i++) {
                        const hit = re ? re.test(lines[i]) : lines[i].toLowerCase().includes(query.toLowerCase());
                        if (hit) { results.push(path.relative(projectDir, full) + ':' + (i + 1) + ': ' + lines[i].trim().slice(0, 160)); if (results.length >= 60) break; }
                    }
                } catch (e2) { /* skip binary/unreadable */ }
            }
        }
    }
    walk(root, 0);
    return results.length ? results.join('\n') : 'No matches for "' + query + '"';
}

function requestApproval(info) {
    if (autoApprove) { send('auto-approved', info); return Promise.resolve(true); }
    return new Promise((resolve) => {
        const id = 'ap_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);
        pendingApprovals.set(id, resolve);
        send('approval-request', Object.assign({ id }, info));
    });
}

async function executeTool(name, args, callId) {
    if (typeof name === 'string' && name.startsWith('mcp__')) return await mcpCall(name, args);
    if (!projectDir && _FILE_TOOLS.has(name)) {
        return 'No project folder is selected. Ask the user to pick a folder (top-right) to work with files. You can still answer questions and write code inline without a folder.';
    }
    switch (name) {
        case 'list_dir': return listDir(args.path || '.');
        case 'read_file': return readFile(args.path, args.offset, args.limit);
        case 'search': return search(args.query, args.path || '.');
        case 'write_file': {
            let existing = '';
            try { existing = fs.readFileSync(safeResolve(args.path), 'utf8'); } catch (e) {}
            const ok = await requestApproval({ kind: 'write', title: 'Write file', path: args.path, diffOld: existing, diffNew: String(args.content || '') });
            if (!ok) return 'User denied writing ' + args.path;
            recordBefore(args.path);
            return writeFile(args.path, args.content);
        }
        case 'edit_file': {
            const ok = await requestApproval({ kind: 'edit', title: 'Edit file', path: args.path, diffOld: String(args.old_string || ''), diffNew: String(args.new_string || '') });
            if (!ok) return 'User denied editing ' + args.path;
            recordBefore(args.path);
            return editFile(args.path, args.old_string, args.new_string);
        }
        case 'run_command': {
            const ok = await requestApproval({ kind: 'command', title: 'Run command', command: args.command });
            if (!ok) return 'User denied running: ' + args.command;
            return await runCommand(args.command);
        }
        case 'git': {
            const a = String(args.args || '').trim();
            const sub = (a.split(/\s+/)[0] || '').toLowerCase();
            const cmd = 'git ' + a;
            if (!GIT_READONLY.has(sub)) {
                const ok = await requestApproval({ kind: 'command', title: 'Run git', command: cmd });
                if (!ok) return 'User denied: ' + cmd;
            }
            return await runCommand(cmd);
        }
        case 'create_document': {
            let spec;
            try { spec = typeof args.spec === 'string' ? JSON.parse(args.spec) : args.spec; }
            catch (e) { return 'Invalid document spec JSON: ' + e.message; }
            if (!spec || !spec.type) return 'Document spec needs a "type" (pptx/xlsx/docx).';
            const dir = projectDir || app.getPath('documents') || os.homedir();
            let fname = String(spec.filename || spec.title || 'document').replace(/[^A-Za-z0-9 ._-]/g, '').trim() || 'document';
            if (!/\.(pptx|xlsx|docx)$/i.test(fname)) fname += '.' + spec.type;
            const dest = path.join(dir, fname);
            const ok = await requestApproval({ kind: 'write', title: 'Create document', path: dest, diffOld: '', diffNew: '(' + String(spec.type).toUpperCase() + ' document: ' + (spec.title || fname) + ')' });
            if (!ok) return 'User denied creating ' + fname;
            try {
                const res = await fetch(BACKEND + '/api/doc/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(spec) });
                if (!res.ok) { let e; try { e = (await res.json()).error; } catch (x) {} return 'Document generation failed: ' + (e || ('error ' + res.status)); }
                const buf = Buffer.from(await res.arrayBuffer());
                fs.writeFileSync(dest, buf);
                return 'Created ' + dest + ' (' + Math.round(buf.length / 1024) + ' KB).';
            } catch (e) { return 'Error creating document: ' + e.message; }
        }
        case 'knowledge': {
            if (!args.topic) {
                const topics = kbList();
                return topics.length
                    ? 'Knowledge base topics: ' + topics.join(', ') + '\nCall knowledge with one of these to read it.'
                    : 'No knowledge base available.';
            }
            return kbRead(args.topic);
        }
        case 'web_search': {
            const q = String(args.query || '').trim();
            if (!q) return 'Provide a search query.';
            const n = Math.max(1, Math.min(parseInt(args.n) || 5, 8));
            try {
                const r = await fetch(BACKEND + '/api/web/search?q=' + encodeURIComponent(q) + '&n=' + n);
                const j = await r.json();
                const res = j.results || [];
                if (!res.length) return 'No results for: ' + q;
                return res.map((x, i) => (i + 1) + '. ' + x.title + '\n   ' + x.url + (x.snippet ? '\n   ' + x.snippet : '')).join('\n\n');
            } catch (e) { return 'Search failed: ' + e.message; }
        }
        case 'fetch_url': {
            const u = String(args.url || '').trim();
            if (!/^https?:\/\//i.test(u)) return 'Provide a valid http(s) URL.';
            try {
                const r = await fetch(u, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' } });
                let html = await r.text();
                html = html.replace(/<script[\s\S]*?<\/script>/gi, ' ').replace(/<style[\s\S]*?<\/style>/gi, ' ').replace(/<!--[\s\S]*?-->/g, ' ');
                let text = html.replace(/<[^>]+>/g, ' ').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/\s+/g, ' ').trim();
                if (text.length > 6000) text = text.slice(0, 6000) + '… [truncated]';
                return text || '(no readable text found)';
            } catch (e) { return 'Fetch failed: ' + e.message; }
        }
        case 'update_plan': {
            const steps = Array.isArray(args.steps) ? args.steps : [];
            send('agent-plan', steps);
            const done = steps.filter(s => s && s.status === 'done').length;
            return 'Plan updated (' + done + '/' + steps.length + ' steps done).';
        }
        case 'scaffold': {
            if (!args.template) {
                const t = tplList();
                return t.length ? 'Available templates: ' + t.join(', ') + '\nCall scaffold with a template name to create it.' : 'No templates available.';
            }
            const spec = tplRead(args.template);
            if (!spec) return 'No template named "' + args.template + '". Available: ' + tplList().join(', ');
            if (!projectDir) return 'No project folder is selected — ask the user to pick a folder (top-right), then scaffold.';
            const sub = String(args.dir || '').trim().replace(/[\\/]+$/, '');
            const files = spec.files || [];
            const previewList = files.map(f => (sub ? sub + '/' : '') + f.path).join('\n');
            const ok = await requestApproval({ kind: 'write', title: 'Scaffold: ' + spec.name, path: (sub || '.'), diffOld: '', diffNew: 'Create ' + files.length + ' files:\n' + previewList });
            if (!ok) return 'User denied scaffolding ' + spec.name;
            const written = [];
            for (const f of files) {
                const rel = (sub ? sub + '/' : '') + f.path;
                try { writeFile(rel, f.content); written.push(rel); }
                catch (e) { return 'Failed writing ' + rel + ': ' + e.message + ' (wrote ' + written.length + ' so far)'; }
            }
            const run = (spec.run && spec.run.length) ? '\nTo run it: ' + spec.run.join(' && ') : '';
            return 'Scaffolded "' + spec.name + '" — ' + written.length + ' files created.' + run;
        }
        case 'apply_patch': {
            const changes = Array.isArray(args.changes) ? args.changes : [];
            if (!changes.length) return 'No changes provided.';
            const plan = [], errs = [];
            for (const ch of changes) {
                const p = String((ch && ch.path) || '').trim();
                if (!p) { errs.push('(a change is missing "path")'); continue; }
                if (ch.old_string == null || ch.old_string === '') { plan.push({ path: p, create: true, content: String(ch.new_string || '') }); continue; }
                let cur; try { cur = fs.readFileSync(safeResolve(p), 'utf8'); } catch (e) { errs.push(p + ': file not found to edit'); continue; }
                const idx = cur.indexOf(ch.old_string);
                if (idx < 0) { errs.push(p + ': old_string not found'); continue; }
                if (cur.indexOf(ch.old_string, idx + 1) >= 0) { errs.push(p + ': old_string is not unique (add more context)'); continue; }
                plan.push({ path: p, cur, old: ch.old_string, neu: String(ch.new_string || '') });
            }
            if (errs.length) return 'Patch NOT applied (nothing changed). Fix and retry:\n- ' + errs.join('\n- ');
            const preview = plan.map(x => (x.create ? 'CREATE ' : 'EDIT   ') + x.path).join('\n');
            const ok = await requestApproval({ kind: 'write', title: 'Apply patch — ' + plan.length + ' files', path: plan.map(x => x.path).join(', ').slice(0, 120), diffOld: '', diffNew: preview });
            if (!ok) return 'User denied the patch.';
            const done = [];
            for (const x of plan) {
                try { recordBefore(x.path); writeFile(x.path, x.create ? x.content : x.cur.replace(x.old, x.neu)); done.push(x.path); }
                catch (e) { return 'Applied ' + done.length + ' file(s), then failed on ' + x.path + ': ' + e.message; }
            }
            return 'Applied patch to ' + done.length + ' file(s): ' + done.join(', ');
        }
        case 'task': {
            const desc = String(args.description || 'sub-task').slice(0, 80);
            const prompt = String(args.prompt || '').trim();
            if (!prompt) return 'Provide a prompt for the sub-agent.';
            return await runSubAgent(desc, prompt, callId);
        }
        case 'image_search': {
            const q = String(args.query || '').trim(); if (!q) return 'Provide an image query.';
            const n = Math.max(1, Math.min(parseInt(args.n) || 5, 10));
            try {
                const r = await fetch(BACKEND + '/api/images/search?q=' + encodeURIComponent(q) + '&n=' + n);
                const j = await r.json(); const im = j.images || [];
                if (!im.length) return 'No images found for: ' + q + '. You can still use <img src="' + BACKEND + '/img?q=' + encodeURIComponent(q) + '"> (falls back to a real photo).';
                return im.map((x, i) => (i + 1) + '. ' + (x.title || 'photo') + '\n   ' + x.url + (x.credit ? ('\n   by ' + x.credit + (x.license ? ' (' + x.license + ')' : '')) : '')).join('\n\n')
                    + '\n\nTip: in web code you can also embed <img src="' + BACKEND + '/img?q=' + encodeURIComponent(q) + '&w=1600&h=900"> directly (no download).';
            } catch (e) { return 'Image search failed: ' + e.message; }
        }
        case 'add_image': {
            const q = String(args.query || '').trim(); if (!q) return 'Provide an image query.';
            if (!projectDir) return 'No project folder — pick one to save images, or use <img src="' + BACKEND + '/img?q=' + encodeURIComponent(q) + '"> in web code (no download needed).';
            let rel = String(args.path || '').trim();
            if (!rel) { const slug = q.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40) || 'image'; rel = 'assets/images/' + slug + '.jpg'; }
            const ok = await requestApproval({ kind: 'write', title: 'Download image', path: rel, diffOld: '', diffNew: 'Download a real photo for "' + q + '" → ' + rel });
            if (!ok) return 'User denied downloading the image.';
            try {
                const r = await fetch(BACKEND + '/img?q=' + encodeURIComponent(q)); // follows the redirect to a real photo
                if (!r.ok) return 'Image fetch failed: HTTP ' + r.status;
                const buf = Buffer.from(await r.arrayBuffer());
                recordBefore(rel); const abs = safeResolve(rel); fs.mkdirSync(path.dirname(abs), { recursive: true }); fs.writeFileSync(abs, buf);
                return 'Saved a real photo to ' + rel + ' (' + Math.round(buf.length / 1024) + ' KB). Reference it in code as ' + rel + '.';
            } catch (e) { return 'Error downloading image: ' + e.message; }
        }
        case 'remember': {
            const note = String(args.note || '').trim();
            if (!note) return 'Nothing to remember.';
            if (!projectDir) return 'No project folder selected — cannot save project memory.';
            let cur = ''; try { cur = fs.readFileSync(safeResolve('GRGCODE.md'), 'utf8'); } catch (e) {}
            const add = (cur ? '' : '# GRGCODE.md — project notes for Grg Code\n') + '\n- ' + note + '\n';
            const ok = await requestApproval({ kind: 'write', title: 'Remember → GRGCODE.md', path: 'GRGCODE.md', diffOld: cur, diffNew: cur + add });
            if (!ok) return 'User denied saving the note.';
            writeFile('GRGCODE.md', cur + add);
            return 'Saved to GRGCODE.md (loaded into context every session).';
        }
        default: return 'Unknown tool: ' + name;
    }
}

// ─────────────────────────── agent loop ───────────────────────────
function systemPrompt() {
    const skills = kbList();
    const tpls = tplList();
    const mem = readProjectMemory();
    const mcpCount = mcpTools().length;
    return {
        role: 'system',
        content: [
            'You are Grg Code, a SENIOR AI software engineer working on the user\'s machine — as capable as the best coding agents (Claude Code, Cursor, Codex). You plan, build, run and verify real software.',
            (projectDir
                ? 'Project folder: ' + projectDir + ' (OS: ' + process.platform + ').'
                : 'No project folder is selected (OS: ' + process.platform + '). You can answer and write code inline; to read/create files, ask the user to pick a folder (top-right).'),
            'Tools: list_dir, read_file, search, write_file, edit_file, apply_patch (multi-file), run_command, git, web_search, fetch_url, image_search, add_image, update_plan, task (sub-agent), scaffold, knowledge, remember, create_document' + (mcpCount ? ', plus ' + mcpCount + ' external MCP tools (mcp__*)' : '') + '.',
            'WORKFLOW — follow it every time:',
            '1) For any multi-step task, FIRST call update_plan with 3-8 concrete steps, and keep it updated (in_progress/done) as you work. This keeps you from stopping early.',
            '2) Explore with list_dir/read_file/search before editing. Never edit a file you have not read. For big exploration/research, delegate to a sub-agent with the task tool to keep your context clean.',
            '3) Before building or scaffolding, call knowledge for the matching skill and follow current best practices.',
            '4) For a NEW project, use scaffold (real starter templates) instead of hand-writing boilerplate.',
            '5) Implement: edit_file (unique old_string) or write_file for one file; apply_patch for a multi-file change in one shot.',
            '6) VERIFY: run the build/tests with run_command, read the errors, and fix until it actually works. Do not claim done without verifying.',
            '7) Finish with a short summary of what changed and how to run it. When you learn a durable repo convention (build/test cmd, style, gotcha), save it with remember.',
            'Use web_search + fetch_url for current library versions, APIs, docs, app-store rules, pricing and hardware. Use create_document for real .pptx/.xlsx/.docx. Use git (read-only runs freely; commits need approval).',
            'IMAGES: when what you build needs photos, use REAL ones — in web/HTML embed <img src="https://grg-ai.com/img?q=<comma,keywords>&w=1600&h=900"> (resolves to a real photo, no download), or use add_image to download a real photo into the project for native/local use; image_search previews options. NEVER leave broken placeholder images.',
            (skills.length ? 'Skills you can load (knowledge <topic>): ' + skills.join(', ') + '.' : ''),
            (tpls.length ? 'Scaffold templates (scaffold <name>): ' + tpls.join(', ') + '.' : ''),
            (mem ? '\n─── PROJECT MEMORY (GRGCODE.md — follow these conventions) ───\n' + mem + '\n─── end project memory ───' : ''),
            (activeAgent ? '\n─── ACTIVE SPECIALIST: ' + activeAgent.name + ' ───\nAdopt this expertise and style on top of your engineering workflow:\n' + activeAgent.prompt + (activeAgent.privacy ? '\n' + GRGAGENT_PRIVACY : '') + '\n─── end specialist ───' : ''),
            'Shell commands and file writes require the user to approve them. Keep going until the task is fully done and verified; be concise but thorough. When finished with no more tool calls, reply with a normal message.'
        ].filter(Boolean).join('\n')
    };
}

async function streamBackend(messages, toolsArg) {
    const res = await fetch(BACKEND + '/api/agent/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages, tools: toolsArg || allTools(), model: agentModel, uid: agentUid, agent: activeAgent ? activeAgent.id : undefined })
    });
    if (!res.ok || !res.body) {
        let e = 'Server error ' + res.status;
        try { const j = await res.json(); e = j.error || e; } catch (x) {}
        throw new Error(e);
    }
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = '', content = '', toolCalls = null, err = null;
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (cancelled) { try { await reader.cancel(); } catch (e) {} break; }
        buf += dec.decode(value, { stream: true });
        const lines = buf.split('\n');
        buf = lines.pop();
        for (const line of lines) {
            const t = line.trim();
            if (!t.startsWith('data:')) continue;
            const data = t.slice(5).trim();
            if (data === '[DONE]') continue;
            let p;
            try { p = JSON.parse(data); } catch (e) { continue; }
            if (p.error) err = p.error;
            if (p.notice) send('agent-status', p.notice);
            if (p.reasoning) send('assistant-reasoning', p.reasoning);
            if (p.token) { content += p.token; send('assistant-token', p.token); }
            if (p.tool_calls) toolCalls = p.tool_calls;
        }
    }
    if (err) throw new Error(err);
    return { content, tool_calls: toolCalls };
}

// ─────────────────── auto-compact (like Claude Code) ───────────────────
// Estimate the size of the running conversation; when it grows large, summarize
// the older turns into one note so we stay well under the model's token limit.
const COMPACT_CHARS = 18000; // ~4.5k tokens — leaves room for tools + reply under the free tier's ~8k/min cap
function convChars(msgs) {
    let n = 0;
    for (const m of msgs) {
        if (m.content) n += String(m.content).length;
        if (m.tool_calls) n += JSON.stringify(m.tool_calls).length;
    }
    return n;
}
async function summarizeHead(text) {
    const res = await fetch(BACKEND + '/api/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            model: 'openai/gpt-oss-20b', temperature: 0.2, max_tokens: 800,
            messages: [
                { role: 'system', content: 'You compress a coding-assistant session into a compact, factual hand-off note so work can continue. Keep: the user\'s goal, decisions taken, files created/edited and key code facts, current state, and what to do next. Terse bullet points, no filler.' },
                { role: 'user', content: 'Summarize the conversation so far:\n\n' + text.slice(0, 24000) }
            ]
        })
    });
    const j = await res.json();
    if (j.error) throw new Error(j.error);
    return (j.message && j.message.content) || '';
}
async function maybeCompact() {
    if (convChars(conversation) < COMPACT_CHARS) return;
    // Keep the most recent user turn (and anything after it) live; summarize the rest.
    let tailStart = conversation.length - 1;
    while (tailStart > 0 && conversation[tailStart].role !== 'user') tailStart--;
    if (tailStart <= 0) return; // nothing safe to fold away yet
    const head = conversation.slice(0, tailStart);
    const tail = conversation.slice(tailStart);
    send('agent-status', 'Auto-compacting context…');
    let summary = '';
    try {
        const text = head.map(m => {
            let c = m.content || '';
            if (m.tool_calls) c += ' [called: ' + m.tool_calls.map(t => t.function && t.function.name).join(', ') + ']';
            return (m.role || '').toUpperCase() + ': ' + c;
        }).join('\n');
        summary = await summarizeHead(text);
    } catch (e) { return; } // if summarizing fails, just keep the full history
    if (!summary) return;
    conversation = [{ role: 'system', content: 'Summary of the earlier conversation (auto-compacted):\n' + summary }].concat(tail);
    send('agent-compacted', { summary });
}

// ═══════════════════ MCP (connect external tool servers) ═══════════════════
// Reads .grgcode/mcp.json (project) or ~/.grgcode/mcp.json — Claude-Desktop format:
// { "mcpServers": { "name": { "command": "npx", "args": ["-y","@modelcontextprotocol/server-filesystem","."] } } }
const mcpServers = {}; // name -> { proc, tools, nextId, pending, buf }
function mcpConfigPath(scope) {
    if (scope === 'project') return projectDir ? path.join(projectDir, '.grgcode', 'mcp.json') : null;
    return path.join(os.homedir(), '.grgcode', 'mcp.json');
}
function readMcpFile(p) { try { if (p && fs.existsSync(p)) return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) {} return null; }
// Merge global + project servers (project overrides same-named).
function loadMergedMcp() {
    const g = readMcpFile(mcpConfigPath('global')) || {};
    const p = readMcpFile(mcpConfigPath('project')) || {};
    const gs = g.mcpServers || g.servers || {};
    const ps = p.mcpServers || p.servers || {};
    return Object.assign({}, gs, ps);
}
function mcpStatusList() { return Object.entries(mcpServers).map(([n, s]) => ({ name: n, tools: (s.tools || []).map(t => t.name) })); }
function mcpSend(srv, method, params) {
    return new Promise((resolve, reject) => {
        const id = srv.nextId++;
        srv.pending.set(id, { resolve, reject });
        try { srv.proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params: params || {} }) + '\n'); }
        catch (e) { srv.pending.delete(id); return reject(e); }
        setTimeout(() => { if (srv.pending.has(id)) { srv.pending.delete(id); reject(new Error('MCP timeout: ' + method)); } }, 90000); // generous: first connect may npx-download the server
    });
}
function mcpNotify(srv, method, params) { try { srv.proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', method, params: params || {} }) + '\n'); } catch (e) {} }
function mcpOnData(srv, chunk) {
    srv.buf += chunk; let i;
    while ((i = srv.buf.indexOf('\n')) >= 0) {
        const line = srv.buf.slice(0, i).trim(); srv.buf = srv.buf.slice(i + 1);
        if (!line) continue;
        let msg; try { msg = JSON.parse(line); } catch (e) { continue; }
        if (msg.id != null && srv.pending.has(msg.id)) {
            const pr = srv.pending.get(msg.id); srv.pending.delete(msg.id);
            if (msg.error) pr.reject(new Error((msg.error && msg.error.message) || 'MCP error')); else pr.resolve(msg.result);
        }
    }
}
async function initMCP() {
    for (const k of Object.keys(mcpServers)) { try { mcpServers[k].proc.kill(); } catch (e) {} delete mcpServers[k]; }
    const servers = loadMergedMcp();
    for (const [rawName, sc] of Object.entries(servers)) {
        if (!sc || !sc.command || sc.disabled) continue;
        const name = String(rawName).replace(/[^a-zA-Z0-9]+/g, '_');
        try {
            const proc = spawn(sc.command, sc.args || [], { cwd: projectDir || undefined, env: Object.assign({}, process.env, sc.env || {}), shell: process.platform === 'win32' });
            const srv = { proc, tools: [], nextId: 1, pending: new Map(), buf: '' };
            proc.stdout.on('data', d => mcpOnData(srv, d.toString()));
            proc.stderr.on('data', () => {});
            proc.on('error', () => {}); proc.on('exit', () => { delete mcpServers[name]; });
            mcpServers[name] = srv;
            await mcpSend(srv, 'initialize', { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'GrgCode', version: '1.0' } });
            mcpNotify(srv, 'notifications/initialized', {});
            const tl = await mcpSend(srv, 'tools/list', {});
            srv.tools = (tl && tl.tools) || [];
            send('agent-status', 'MCP connected: ' + name + ' (' + srv.tools.length + ' tools)');
        } catch (e) { try { delete mcpServers[name]; } catch (x) {} }
    }
}
function mcpTools() {
    const out = [];
    for (const [name, srv] of Object.entries(mcpServers)) {
        for (const t of srv.tools) {
            out.push({ type: 'function', function: {
                name: 'mcp__' + name + '__' + t.name,
                description: (t.description || ('MCP tool ' + t.name)).slice(0, 300),
                parameters: t.inputSchema || { type: 'object', properties: {} }
            } });
        }
    }
    return out;
}
async function mcpCall(fullName, args) {
    const parts = String(fullName).split('__'); // ['mcp', server, tool...]
    const server = parts[1]; const tool = parts.slice(2).join('__');
    const srv = mcpServers[server]; if (!srv) return 'MCP server not connected: ' + server;
    try {
        const res = await mcpSend(srv, 'tools/call', { name: tool, arguments: args || {} });
        const content = (res && res.content) || [];
        const text = content.map(c => c.type === 'text' ? c.text : JSON.stringify(c)).join('\n');
        return (text || '(no output)').slice(0, 4000);
    } catch (e) { return 'MCP call failed: ' + e.message; }
}
function allTools() { return TOOLS.concat(mcpTools()); }

// ═══════════════════ Sub-agents (delegate a focused task) ═══════════════════
const SUBAGENT_SAFE = new Set(['list_dir', 'read_file', 'search', 'web_search', 'fetch_url', 'knowledge']);
async function runSubAgent(description, prompt, parentId) {
    const pid = parentId || ('sub_' + Date.now());
    const subTools = TOOLS.filter(t => SUBAGENT_SAFE.has(t.function.name));
    const sys = { role: 'system', content: 'You are a focused sub-agent spawned by Grg Code to do ONE task and report back to the main agent. Task: ' + description + '. Use the read-only tools (list_dir, read_file, search, web_search, fetch_url, knowledge) to investigate, then return a concise, complete, self-contained answer/findings. Do not ask questions — do your best with what you can read. End with the answer only.' };
    let msgs = [sys, { role: 'user', content: prompt }];
    let final = '';
    send('subagent-start', { id: pid, description: description });
    for (let i = 0; i < 8; i++) {
        if (cancelled) break;
        let r; try { r = await streamBackend(msgs, subTools); } catch (e) { send('subagent-end', { id: pid, error: e.message }); return 'Sub-agent error: ' + e.message; }
        const calls = Array.isArray(r.tool_calls) ? r.tool_calls : [];
        msgs.push({ role: 'assistant', content: r.content || '', tool_calls: calls.length ? calls : undefined });
        if (!calls.length) { final = r.content || ''; break; }
        for (const c of calls) {
            if (cancelled) break;
            const nm = c.function && c.function.name; let a = {}; try { a = JSON.parse((c.function && c.function.arguments) || '{}'); } catch (e) {}
            send('subagent-tool', { id: pid, callId: c.id, name: nm, args: a });
            let res; try { res = SUBAGENT_SAFE.has(nm) ? await executeTool(nm, a) : 'That tool is not available to a sub-agent.'; } catch (e) { res = 'Error: ' + e.message; }
            res = String(res).slice(0, 3000);
            send('subagent-tool-result', { id: pid, callId: c.id, name: nm, result: res });
            msgs.push({ role: 'tool', tool_call_id: c.id, content: res });
        }
    }
    final = final || '(sub-agent finished without a clear summary)';
    send('subagent-end', { id: pid, result: final });
    return final;
}

// ═══════════════════ Slash commands (reusable prompts) ═══════════════════
const BUILTIN_COMMANDS = {
    review: 'Review the code you just wrote (or the current diff via `git diff`) for bugs, edge cases, security and clarity. List concrete issues with fixes, then apply the important ones. $ARGUMENTS',
    test: 'Write and run tests for the relevant code. Load the testing-qa skill first. Report pass/fail and fix any failures until green. $ARGUMENTS',
    explain: 'Explain how this works, clearly and concisely, naming the key files and the flow: $ARGUMENTS',
    fix: 'Find and fix this bug. First reproduce it, then fix the root cause, then verify with a test/run: $ARGUMENTS',
    commit: 'Create a git commit for the current changes. Run `git status` and `git diff` first, group related changes, write a concise conventional-commit message, then commit. Ask before pushing.',
    optimize: 'Profile and optimize the performance of: $ARGUMENTS. Measure first (load the security-performance skill), then optimize, then verify behavior is unchanged.',
    init: 'Explore this project (structure, stack, scripts, conventions) and create or update GRGCODE.md at the project root capturing: what it is, how to run/build/test, the stack, and coding conventions. Use write_file or the remember tool.',
    scaffold: 'Scaffold a new project. List templates with the scaffold tool, pick the best fit for: $ARGUMENTS, create it, then tell me exactly how to run it.'
};
function cmdDirFor(scope) {
    if (scope === 'project') return projectDir ? path.join(projectDir, '.grgcode', 'commands') : null;
    return path.join(os.homedir(), '.grgcode', 'commands'); // global
}
function listCommandsIn(scope) {
    const d = cmdDirFor(scope); if (!d) return [];
    try {
        return fs.readdirSync(d).filter(f => /\.md$/i.test(f)).map(f => {
            let body = ''; try { body = fs.readFileSync(path.join(d, f), 'utf8'); } catch (e) {}
            return { name: f.replace(/\.md$/i, ''), body };
        }).sort((a, b) => a.name.localeCompare(b.name));
    } catch (e) { return []; }
}
function listCommands() {
    const names = new Set(Object.keys(BUILTIN_COMMANDS));
    ['global', 'project'].forEach(s => listCommandsIn(s).forEach(c => names.add(c.name)));
    return Array.from(names).sort();
}
function getCommand(name) {
    const slug = String(name || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    for (const s of ['project', 'global']) { // project overrides global overrides builtin
        const d = cmdDirFor(s); if (!d) continue;
        const f = path.join(d, slug + '.md');
        try { if (fs.existsSync(f)) return fs.readFileSync(f, 'utf8'); } catch (e) {}
    }
    return BUILTIN_COMMANDS[slug] || null;
}
function expandCommand(text) {
    const m = String(text).match(/^\/([a-zA-Z0-9_-]+)\s*([\s\S]*)$/);
    if (!m) return text;
    const body = getCommand(m[1]); if (body == null) return text;
    const arg = (m[2] || '').trim();
    return body.replace(/\$ARGUMENTS/g, arg).replace(/\$1/g, arg);
}

// ═══════════════════ Project memory (GRGCODE.md) ═══════════════════
function readProjectMemory() {
    if (!projectDir) return '';
    for (const rel of ['GRGCODE.md', '.grgcode/GRGCODE.md', 'AGENTS.md', 'CLAUDE.md']) {
        try { const f = path.join(projectDir, rel); if (fs.existsSync(f)) return fs.readFileSync(f, 'utf8').slice(0, 4000); } catch (e) {}
    }
    return '';
}

async function runAgent(userText, extraContext) {
    if (running) return;
    running = true;
    cancelled = false;
    if (extraContext) conversation.push({ role: 'system', content: extraContext });
    conversation.push({ role: 'user', content: userText });
    curCheckpoint = { id: 'cp' + Date.now(), ts: Date.now(), user: String(userText || '').slice(0, 80), ops: [] };
    try {
        await maybeCompact();
        for (let iter = 0; iter < MAX_ITERS; iter++) {
            if (cancelled) { send('agent-stopped'); break; }
            send('agent-status', 'Grg is thinking…');
            let result;
            try { result = await streamBackend([systemPrompt()].concat(conversation)); }
            catch (e) { send('agent-error', e.message); break; }
            const content = result.content || '';
            const calls = Array.isArray(result.tool_calls) ? result.tool_calls : [];
            conversation.push({ role: 'assistant', content, tool_calls: calls.length ? calls : undefined });
            send('assistant-flush');
            if (!calls.length) { send('agent-done'); break; }
            for (const call of calls) {
                if (cancelled) break;
                const name = call.function && call.function.name;
                let args = {};
                try { args = JSON.parse((call.function && call.function.arguments) || '{}'); } catch (e) {}
                send('tool-call', { id: call.id, name, args });
                let result;
                try { result = await executeTool(name, args, call.id); }
                catch (e) { result = 'Error: ' + e.message; }
                result = String(result);
                send('tool-result', { id: call.id, name, result: result.slice(0, 4000) });
                conversation.push({ role: 'tool', tool_call_id: call.id, content: result.slice(0, 4000) });
            }
            if (iter === MAX_ITERS - 1) send('agent-error', 'Reached the step limit for this task.');
        }
    } catch (e) {
        send('agent-error', e.message);
    } finally {
        running = false;
        if (curCheckpoint && curCheckpoint.ops.length) {
            checkpoints.push(curCheckpoint);
            if (checkpoints.length > 40) checkpoints.shift();
            send('checkpoint', { id: curCheckpoint.id, count: curCheckpoint.ops.length });
        }
        curCheckpoint = null;
        send('agent-idle');
    }
}

// ─────────────────────────── IPC ───────────────────────────
// ─── File Explorer ───
function buildTree(rel, depth) {
    rel = rel || '.'; depth = depth || 0;
    const skip = new Set(['node_modules', '.git', 'dist', 'build', '.next', '.venv', '__pycache__', '.cache']);
    let abs; try { abs = safeResolve(rel); } catch (e) { return []; }
    let entries; try { entries = fs.readdirSync(abs, { withFileTypes: true }); } catch (e) { return []; }
    entries = entries.filter(e => !skip.has(e.name)).slice(0, 300);
    entries.sort((a, b) => (Number(b.isDirectory()) - Number(a.isDirectory())) || a.name.localeCompare(b.name));
    const out = [];
    for (const e of entries) {
        const childRel = (rel === '.' ? '' : rel + '/') + e.name;
        if (e.isDirectory()) out.push({ name: e.name, path: childRel, dir: true, children: depth < 4 ? buildTree(childRel, depth + 1) : [] });
        else out.push({ name: e.name, path: childRel, dir: false });
    }
    return out;
}
ipcMain.handle('list-tree', () => { try { return buildTree('.', 0); } catch (e) { return []; } });
ipcMain.handle('read-file-direct', (e, rel) => {
    try {
        const f = safeResolve(rel);
        if (fs.statSync(f).size > 400 * 1024) return '(file too large to preview — ' + Math.round(fs.statSync(f).size / 1024) + ' KB)';
        return fs.readFileSync(f, 'utf8');
    } catch (err) { return 'Error: ' + err.message; }
});
// User-initiated save from the Monaco editor (their own action → no approval prompt).
ipcMain.handle('write-file-direct', (e, rel, content) => {
    try {
        const f = safeResolve(rel);
        fs.mkdirSync(path.dirname(f), { recursive: true });
        fs.writeFileSync(f, content == null ? '' : String(content), 'utf8');
        return 'ok';
    } catch (err) { return 'Error: ' + err.message; }
});

// ─── Persistent terminal (a real shell kept alive; cd & env persist) ───
let termProc = null;
function termSpawn() {
    if (termProc) return;
    const isWin = process.platform === 'win32';
    const cmd = isWin ? 'powershell.exe' : (process.env.SHELL || 'bash');
    const args = isWin ? ['-NoLogo', '-NoProfile'] : ['-i'];
    try {
        termProc = spawn(cmd, args, { cwd: projectDir, env: process.env, windowsHide: true });
    } catch (e) { send('term-output', 'Could not start shell: ' + e.message + '\n'); return; }
    termProc.stdout.on('data', (d) => send('term-output', d.toString()));
    termProc.stderr.on('data', (d) => send('term-output', d.toString()));
    termProc.on('exit', (code) => { send('term-exit', code); termProc = null; });
    send('term-output', '● shell started in ' + projectDir + '\n');
}
ipcMain.on('term-start', () => termSpawn());
ipcMain.on('term-input', (e, line) => {
    termSpawn();
    try { if (termProc && termProc.stdin.writable) termProc.stdin.write(String(line) + '\n'); } catch (x) {}
});
ipcMain.on('term-kill', () => { if (termProc) { try { termProc.kill(); } catch (x) {} termProc = null; } });

ipcMain.handle('get-state', () => ({ projectDir, platform: process.platform }));
ipcMain.handle('pick-folder', async () => {
    const r = await dialog.showOpenDialog(win, { properties: ['openDirectory'], title: 'Choose a project folder' });
    if (!r.canceled && r.filePaths[0]) { projectDir = r.filePaths[0]; conversation = []; }
    return { projectDir };
});
ipcMain.on('send-message', (e, text) => { if (text && text.trim()) { const t = text.trim(); runAgent(expandCommand(t), expandMentions(t)); } });
ipcMain.handle('list-commands', () => listCommands());
ipcMain.handle('list-files', () => { try { return flatFiles('.', 0, []); } catch (e) { return []; } });
ipcMain.handle('list-checkpoints', () => checkpoints.map(c => ({ id: c.id, ts: c.ts, user: c.user, count: c.ops.length, reverted: !!c.reverted })).reverse());
ipcMain.handle('revert-checkpoint', (e, id) => revertCheckpoint(id));
// ─── Slash-command editor ───
ipcMain.handle('commands-get', () => ({
    builtins: BUILTIN_COMMANDS,
    global: listCommandsIn('global'),
    project: projectDir ? listCommandsIn('project') : null,
    hasFolder: !!projectDir
}));
ipcMain.handle('command-save', (e, payload) => {
    const scope = (payload && payload.scope) || 'global';
    const slug = String((payload && payload.name) || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    if (!slug) return { error: 'Invalid name (use letters, numbers, - or _).' };
    const body = String((payload && payload.body) || '');
    const d = cmdDirFor(scope); if (!d) return { error: 'No project folder selected — pick one, or use Global.' };
    try { fs.mkdirSync(d, { recursive: true }); fs.writeFileSync(path.join(d, slug + '.md'), body); }
    catch (err) { return { error: String((err && err.message) || err) }; }
    return { ok: true, name: slug };
});
ipcMain.handle('command-delete', (e, payload) => {
    const scope = (payload && payload.scope) || 'global';
    const slug = String((payload && payload.name) || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    const d = cmdDirFor(scope); if (!d) return { error: 'no dir' };
    try { const f = path.join(d, slug + '.md'); if (fs.existsSync(f)) fs.unlinkSync(f); } catch (err) { return { error: String((err && err.message) || err) }; }
    return { ok: true };
});
// ─── Skills / knowledge editor ───
ipcMain.handle('knowledge-get', () => ({
    bundled: kbListIn('bundled'),
    global: kbListIn('global'),
    project: projectDir ? kbListIn('project') : null,
    hasFolder: !!projectDir
}));
ipcMain.handle('knowledge-save', (e, payload) => {
    const scope = (payload && payload.scope) || 'global';
    if (scope !== 'global' && scope !== 'project') return { error: 'Pick Global or This project.' };
    const slug = String((payload && payload.name) || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    if (!slug) return { error: 'Invalid name (use letters, numbers, - or _).' };
    const d = kbDirFor(scope); if (!d) return { error: 'No project folder selected — pick one, or use Global.' };
    try { fs.mkdirSync(d, { recursive: true }); fs.writeFileSync(path.join(d, slug + '.md'), String((payload && payload.body) || '')); }
    catch (err) { return { error: String((err && err.message) || err) }; }
    return { ok: true, name: slug };
});
ipcMain.handle('knowledge-delete', (e, payload) => {
    const scope = (payload && payload.scope) || 'global';
    if (scope !== 'global' && scope !== 'project') return { error: 'bad scope' };
    const slug = String((payload && payload.name) || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    const d = kbDirFor(scope); if (!d) return { error: 'no dir' };
    try { for (const ext of ['md', 'json', 'txt']) { const f = path.join(d, slug + '.' + ext); if (fs.existsSync(f)) fs.unlinkSync(f); } }
    catch (err) { return { error: String((err && err.message) || err) }; }
    return { ok: true };
});
// ─── Template editor ───
function _tplMeta(t) { return { name: t.name, description: (t.obj && t.obj.description) || '', fileCount: ((t.obj && t.obj.files) || []).length, raw: t.raw }; }
ipcMain.handle('templates-get', () => ({
    bundled: tplListIn('bundled').map(_tplMeta),
    global: tplListIn('global').map(_tplMeta),
    project: projectDir ? tplListIn('project').map(_tplMeta) : null,
    hasFolder: !!projectDir
}));
ipcMain.handle('template-save', (e, payload) => {
    const scope = (payload && payload.scope) || 'global';
    if (scope !== 'global' && scope !== 'project') return { error: 'Pick Global or This project.' };
    const slug = String((payload && payload.name) || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    if (!slug) return { error: 'Invalid name (letters, numbers, - or _).' };
    let obj; try { obj = JSON.parse((payload && payload.json) || ''); } catch (err) { return { error: 'Invalid JSON: ' + err.message }; }
    if (!obj || !Array.isArray(obj.files) || !obj.files.length) return { error: 'Template needs a non-empty "files" array of {path, content}.' };
    if (!obj.name) obj.name = slug;
    const d = tplDirFor(scope); if (!d) return { error: 'No project folder selected — pick one, or use Global.' };
    try { fs.mkdirSync(d, { recursive: true }); fs.writeFileSync(path.join(d, slug + '.json'), JSON.stringify(obj, null, 2)); }
    catch (err) { return { error: String((err && err.message) || err) }; }
    return { ok: true, name: slug };
});
ipcMain.handle('template-delete', (e, payload) => {
    const scope = (payload && payload.scope) || 'global';
    if (scope !== 'global' && scope !== 'project') return { error: 'bad scope' };
    const slug = String((payload && payload.name) || '').toLowerCase().replace(/[^a-z0-9_-]/g, '');
    const d = tplDirFor(scope); if (!d) return { error: 'no dir' };
    try { const f = path.join(d, slug + '.json'); if (fs.existsSync(f)) fs.unlinkSync(f); } catch (err) { return { error: String((err && err.message) || err) }; }
    return { ok: true };
});
// ─── Project memory (GRGCODE.md) editor ───
ipcMain.handle('memory-get', () => {
    if (!projectDir) return { hasFolder: false, content: '', source: null };
    let source = null;
    for (const rel of ['GRGCODE.md', '.grgcode/GRGCODE.md', 'AGENTS.md', 'CLAUDE.md']) { if (fs.existsSync(path.join(projectDir, rel))) { source = rel; break; } }
    let content = ''; try { content = fs.readFileSync(path.join(projectDir, 'GRGCODE.md'), 'utf8'); } catch (e) {}
    return { hasFolder: true, content, source };
});
ipcMain.handle('memory-save', (e, payload) => {
    if (!projectDir) return { error: 'No project folder selected.' };
    try { fs.writeFileSync(path.join(projectDir, 'GRGCODE.md'), String((payload && payload.content) || '')); }
    catch (err) { return { error: String((err && err.message) || err) }; }
    return { ok: true };
});
// ─── MCP settings ───
ipcMain.handle('mcp-get', () => {
    const global = readMcpFile(mcpConfigPath('global')) || { mcpServers: {} };
    const projPath = mcpConfigPath('project');
    const project = projPath ? (readMcpFile(projPath) || { mcpServers: {} }) : null;
    if (!global.mcpServers) global.mcpServers = global.servers || {};
    if (project && !project.mcpServers) project.mcpServers = project.servers || {};
    return { global, project, hasFolder: !!projectDir, status: mcpStatusList() };
});
ipcMain.handle('mcp-save', async (e, payload) => {
    const scope = (payload && payload.scope) || 'global';
    const config = (payload && payload.config) || { mcpServers: {} };
    const p = mcpConfigPath(scope);
    if (!p) return { error: 'No project folder selected — pick one first, or use Global.' };
    try { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, JSON.stringify(config, null, 2)); }
    catch (err) { return { error: String((err && err.message) || err) }; }
    try { await initMCP(); } catch (x) {}
    return { ok: true, status: mcpStatusList() };
});
ipcMain.handle('mcp-reconnect', async () => { try { await initMCP(); } catch (x) {} return { status: mcpStatusList() }; });
ipcMain.on('stop', () => { cancelled = true; });
ipcMain.on('new-session', () => { conversation = []; });
ipcMain.handle('get-conversation', () => conversation);
ipcMain.on('set-conversation', (e, conv) => { conversation = Array.isArray(conv) ? conv : []; });
ipcMain.on('set-folder', (e, p) => {
    try {
        if (!p) { projectDir = null; }
        else if (fs.statSync(p).isDirectory()) { projectDir = p; }
        else { return; }
        if (termProc) { try { termProc.kill(); } catch (x) {} termProc = null; }
        initMCP();  // reload MCP servers for the new project folder (.grgcode/mcp.json)
    } catch (x) {}
});
ipcMain.on('set-uid', (e, uid) => { agentUid = uid || null; });
ipcMain.on('set-approve-mode', (e, auto) => { autoApprove = !!auto; });
ipcMain.on('set-model', (e, m) => { if (typeof m === 'string' && m) agentModel = m; });
ipcMain.on('set-agent', (e, a) => { activeAgent = (a && a.id && a.prompt) ? { id: a.id, name: a.name || 'Agent', prompt: a.prompt, privacy: !!a.privacy } : null; });
ipcMain.on('approval-response', (e, { id, ok }) => {
    const resolve = pendingApprovals.get(id);
    if (resolve) { pendingApprovals.delete(id); resolve(!!ok); }
});
ipcMain.on('open-external', (e, url) => { shell.openExternal(url); });

// ─── In-app updater (portable exe: download the newest build, then relaunch into it) ───
ipcMain.handle('check-update', async () => {
    try {
        const r = await fetch(BACKEND + '/api/grgcode/version', { cache: 'no-store' });
        const j = await r.json();
        const latest = parseInt(j.version, 10) || 0;
        return { current: APP_VERSION, latest: latest, filename: j.filename,
                 url: BACKEND + j.url, updateAvailable: latest > APP_VERSION };
    } catch (e) { return { current: APP_VERSION, latest: 0, error: e.message, updateAvailable: false }; }
});
ipcMain.handle('download-update', async (e, url, filename) => {
    try {
        const r = await fetch(url);
        if (!r.ok) throw new Error('HTTP ' + r.status);
        const buf = Buffer.from(await r.arrayBuffer());
        if (buf.length < 1000000) throw new Error('download too small');
        const dir = app.getPath('downloads') || app.getPath('temp');
        const dest = path.join(dir, filename || ('GrgCode-update-' + Date.now() + '.exe'));
        fs.writeFileSync(dest, buf);
        return { ok: true, path: dest };
    } catch (e2) { return { ok: false, error: e2.message }; }
});
ipcMain.handle('launch-update', async (e, p) => {
    try { const err = await shell.openPath(p); if (err) throw new Error(err);
          setTimeout(() => { try { app.quit(); } catch (x) {} }, 900); return { ok: true }; }
    catch (e2) { return { ok: false, error: e2.message }; }
});
ipcMain.on('show-in-folder', (e, p) => { try { shell.showItemInFolder(p); } catch (x) {} });

// ─── Google sign-in (system browser → backend mints a custom token → loopback) ───
let _googleAuthServer = null;
ipcMain.handle('start-google-auth', async () => {
    try {
        if (_googleAuthServer) { try { _googleAuthServer.close(); } catch (e) {} _googleAuthServer = null; }
        const state = Math.random().toString(36).slice(2) + Date.now().toString(36);
        const server = http.createServer((req, res) => {
            let u;
            try { u = new URL(req.url, 'http://127.0.0.1'); } catch (e) { res.writeHead(400); res.end(); return; }
            if (u.pathname !== '/cb') { res.writeHead(404); res.end(); return; }
            const token = u.searchParams.get('token'), st = u.searchParams.get('state');
            const page = (ok) => '<!doctype html><meta charset="utf-8"><body style="font-family:system-ui,-apple-system,sans-serif;background:#0e0b17;color:#ece9f6;display:flex;align-items:center;justify-content:center;height:100vh;margin:0"><div style="text-align:center"><h2 style="margin:0 0 8px">' + (ok ? 'Signed in to Grg Code' : 'Sign-in could not be verified') + '</h2><p style="color:#9990b3">' + (ok ? 'You can close this tab and return to the app.' : 'Please return to Grg Code and try again.') + '</p></div></body>';
            res.writeHead(200, { 'Content-Type': 'text/html' });
            if (token && st === state) { res.end(page(true)); send('google-token', token); }
            else { res.end(page(false)); }
            setTimeout(() => { try { server.close(); } catch (e) {} }, 500);
            _googleAuthServer = null;
        });
        await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
        _googleAuthServer = server;
        const port = server.address().port;
        setTimeout(() => { if (_googleAuthServer === server) { try { server.close(); } catch (e) {} _googleAuthServer = null; } }, 300000);
        await shell.openExternal(BACKEND + '/grgcode-auth?port=' + port + '&state=' + encodeURIComponent(state));
        return { ok: true };
    } catch (e) { return { ok: false, error: e.message }; }
});

// Open a rendered preview in its own window (popout button in the preview panel).
ipcMain.handle('open-preview', (e, html) => {
    try {
        const pw = new BrowserWindow({
            width: 1024, height: 768, backgroundColor: '#ffffff', title: 'Grg Code — Preview',
            webPreferences: { sandbox: true, contextIsolation: true, nodeIntegration: false }
        });
        pw.setMenuBarVisibility(false);
        pw.loadURL('data:text/html;charset=utf-8,' + encodeURIComponent(String(html || '')));
        return true;
    } catch (err) { return false; }
});

// Billing API proxied through the main process (Node fetch → no CORS, no API opening).
ipcMain.handle('bill-account', async (e, uid) => {
    try { const r = await fetch(BACKEND + '/api/account?uid=' + encodeURIComponent(uid)); return await r.json(); }
    catch (err) { return { error: String((err && err.message) || err) }; }
});
ipcMain.handle('bill-post', async (e, apiPath, body) => {
    try { const r = await fetch(BACKEND + apiPath, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body || {}) }); return await r.json(); }
    catch (err) { return { error: String((err && err.message) || err) }; }
});
