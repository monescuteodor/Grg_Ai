'use strict';
const $ = (id) => document.getElementById(id);
const msgs = $('msgs'), chat = $('chat'), input = $('input');
let busy = false, projectDir = '';

// ─── sessions ───
let sessions = [];
let curId = null;
try { sessions = JSON.parse(localStorage.getItem('grgcode-sessions') || '[]'); } catch (e) { sessions = []; }
function saveSessions() { try { localStorage.setItem('grgcode-sessions', JSON.stringify(sessions.slice(0, 100))); } catch (e) {} }
function curSession() { return sessions.find(s => s.id === curId); }
function makeId() { return 's' + Date.now() + Math.random().toString(36).slice(2, 6); }

function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
var _gcRunnable = ['html','htm','css','javascript','js','svg','jsx','tsx','react','typescript','ts'];
function fmt(text) {
    let h = esc(text);
    const blocks = [];
    h = h.replace(/```(\w*)\n?([\s\S]*?)```/g, (m, l, code) => {
        l = (l || '').toLowerCase();
        code = code.replace(/\n$/, '');
        var runnable = _gcRunnable.indexOf(l) !== -1;
        var runBtn = runnable ? '<button class="cb-btn cb-run" onclick="gcRunPreview(this)">▶ Preview</button>' : '';
        var head = '<div class="cb-head"><span class="cb-lang">' + (l || 'code') + '</span><span class="cb-actions">' + runBtn + '<button class="cb-btn" onclick="gcCopyCode(this)">Copy</button></span></div>';
        blocks.push('<div class="code-wrap" data-lang="' + l + '">' + head + '<pre><code>' + code + '</code></pre></div>');
        return '' + (blocks.length - 1) + '';
    });
    h = h.replace(/`([^`\n]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
    h = h.replace(/(\d+)/g, (m, i) => blocks[+i]);
    return h;
}
function gcCopyCode(btn) {
    var wrap = btn.closest('.code-wrap'); if (!wrap) return;
    var codeEl = wrap.querySelector('code'); if (!codeEl) return;
    var txt = codeEl.textContent;
    try { navigator.clipboard.writeText(txt); } catch (e) {}
    var old = btn.textContent; btn.textContent = 'Copied'; setTimeout(function(){ btn.textContent = old; }, 1200);
}

// ─── ADVANCED PREVIEW (React/JSX + Babel + Tailwind + responsive) ───
var _gcDanger = [/document\.cookie/i, /child_process/i, /require\s*\(\s*['"]fs/i, /rm\s+-rf/i, /__proto__/i];
var _gcLastPreview = '';

function _looksReact(code) {
    if (!code) return false;
    if (/\bimport\s+React\b/.test(code)) return true;
    if (/\bfrom\s+['"]react['"]/.test(code)) return true;
    if (/\bReactDOM\b/.test(code)) return true;
    if (/\buse(State|Effect|Ref|Memo|Callback|Reducer|Context)\s*\(/.test(code)) return true;
    if (/\bexport\s+default\s+function\s+[A-Z]/.test(code)) return true;
    if (/return\s*\(?\s*</.test(code) && /<[A-Za-z][^>]*>/.test(code)) return true;
    if (/<([A-Z][A-Za-z0-9]*)[\s/>]/.test(code) && /\b(function|const|class)\b/.test(code)) return true;
    return false;
}
function _looksTailwind(s) {
    if (!s) return false;
    return /class(Name)?\s*=\s*["'][^"']*\b(flex|grid|(p|m|px|py|mx|my|pt|pb|pl|pr|mt|mb|ml|mr)-\d|gap-\d|text-(xs|sm|base|lg|xl|\dxl|center|white|gray|slate)|bg-(white|black|gray|slate|blue|red|green|indigo|zinc|neutral)|rounded|shadow|w-\d|h-\d|items-|justify-|font-(bold|semibold|medium))\b/.test(s);
}
function _buildReactDoc(js, css, html) {
    js = js.replace(/^\s*import\s+[^;]*;?\s*$/gm, '');
    js = js.replace(/^\s*export\s+default\s+/gm, '__grg_default = ');
    js = js.replace(/^\s*export\s+/gm, '');
    var name = null, m;
    m = js.match(/__grg_default\s*=\s*function\s+([A-Za-z0-9_]+)/); if (m) name = m[1];
    if (!name) { m = js.match(/__grg_default\s*=\s*([A-Za-z0-9_]+)\s*;?/); if (m) name = m[1]; }
    if (!name) { m = js.match(/function\s+(App|Main|Root|[A-Z][A-Za-z0-9_]*)\s*\(/); if (m) name = m[1]; }
    if (!name) { m = js.match(/(?:const|let|var)\s+(App|Main|Root|[A-Z][A-Za-z0-9_]*)\s*=\s*(?:\([^)]*\)|[A-Za-z0-9_]+)\s*=>/); if (m) name = m[1]; }
    js = js.replace(/__grg_default\s*=\s*function\s+([A-Za-z0-9_]+)/, 'function $1');
    js = js.replace(/__grg_default\s*=\s*/, name ? '/* default */ var __grg_ignore_default = ' : 'var __grg_root = ');
    if (!name && /var __grg_root =/.test(js)) name = '__grg_root';
    var hasMount = /ReactDOM\.(createRoot|render)/.test(js);
    var mount = '';
    if (!hasMount && name) {
        mount = '\ntry{var _r=document.getElementById("root");if(ReactDOM.createRoot){ReactDOM.createRoot(_r).render(React.createElement(' + name + '));}else{ReactDOM.render(React.createElement(' + name + '),_r);}}catch(e){document.getElementById("root").innerHTML="<pre style=\\"color:#b91c1c;padding:16px\\">"+e.message+"</pre>";console.error(e);}';
    }
    var hooks = 'var {useState,useEffect,useRef,useMemo,useCallback,useReducer,useContext,useLayoutEffect,Fragment,createContext}=React;';
    var safe = (hooks + '\n' + js + mount).replace(/<\/script/gi, '<\\/script');
    var tw = _looksTailwind(js + ' ' + (html || '')) ? '<scr' + 'ipt src="https://cdn.tailwindcss.com"></scr' + 'ipt>' : '';
    return '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        + '<scr' + 'ipt src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></scr' + 'ipt>'
        + '<scr' + 'ipt src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></scr' + 'ipt>'
        + '<scr' + 'ipt src="https://cdn.jsdelivr.net/npm/@babel/standalone@7/babel.min.js"></scr' + 'ipt>'
        + tw
        + '<style>body{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#fff;color:#111;}' + (tw ? '' : '#root{padding:20px;}') + '</style>'
        + (css ? '<style>' + css + '</style>' : '')
        + '</head><body><div id="root"></div>'
        + '<scr' + 'ipt type="text/babel" data-presets="react,typescript">' + safe + '</scr' + 'ipt>'
        + '</body></html>';
}
function _injectConsole(html) {
    var cjs = '<scr' + 'ipt>(function(){var box=document.createElement("div");box.id="__grgconsole";box.style.cssText="position:fixed;left:0;right:0;bottom:0;max-height:45%;overflow:auto;background:#0c0a14;color:#cbd5e1;font:12px/1.55 ui-monospace,Menlo,monospace;border-top:1px solid #322a48;padding:6px 10px 8px;display:none;z-index:2147483647;white-space:pre-wrap;word-break:break-word;";'
      + 'function esc(x){try{return typeof x==="object"?JSON.stringify(x,null,2):String(x)}catch(e){return String(x)}}'
      + 'function add(color,args){var l=document.createElement("div");if(color)l.style.color=color;l.textContent=Array.prototype.map.call(args,esc).join(" ");box.appendChild(l);box.style.display="block";box.scrollTop=box.scrollHeight;}'
      + 'var L=console.log,E=console.error,W=console.warn,I=console.info;'
      + 'console.log=function(){L.apply(console,arguments);add("",arguments)};'
      + 'console.info=function(){I.apply(console,arguments);add("#93c5fd",arguments)};'
      + 'console.warn=function(){W.apply(console,arguments);add("#fbbf24",arguments)};'
      + 'console.error=function(){E.apply(console,arguments);add("#f87171",arguments)};'
      + 'window.addEventListener("error",function(e){add("#f87171",[e.message+"  ("+(e.lineno||0)+":"+(e.colno||0)+")"])});'
      + 'window.addEventListener("unhandledrejection",function(e){add("#f87171",["Unhandled: "+((e.reason&&e.reason.message)||e.reason)])});'
      + 'function mount(){if(document.body&&!document.body.contains(box))document.body.appendChild(box);}'
      + 'if(document.body)mount();document.addEventListener("DOMContentLoaded",mount);'
      + '})();</scr' + 'ipt>';
    if (html.indexOf('</body>') !== -1) return html.replace('</body>', cjs + '</body>');
    return html + cjs;
}
function gcRunPreview(btn) {
    var panel = document.getElementById('gc-preview');
    var frame = document.getElementById('gc-frame');
    var badge = document.getElementById('gc-badge');
    var message = btn.closest('.msg') || document.getElementById('msgs');
    var allCodeBlocks = message.querySelectorAll('.code-wrap');
    var htmlParts = [], cssParts = [], jsParts = [], reactParts = [], fullHtml = null;
    for (var i = 0; i < allCodeBlocks.length; i++) {
        var lang = (allCodeBlocks[i].getAttribute('data-lang') || '').toLowerCase();
        var codeEl = allCodeBlocks[i].querySelector('code'); if (!codeEl) continue;
        var code = codeEl.textContent;
        var trimmed = code.trim().toLowerCase();
        if (trimmed.indexOf('<!doctype') === 0 || trimmed.indexOf('<html') === 0) { fullHtml = code; continue; }
        if (lang === 'css' || lang === 'scss') cssParts.push(code);
        else if (lang === 'jsx' || lang === 'tsx' || lang === 'react') reactParts.push(code);
        else if (lang === 'javascript' || lang === 'js' || lang === 'ts' || lang === 'typescript') { if (_looksReact(code)) reactParts.push(code); else jsParts.push(code); }
        else if (lang === 'html' || lang === 'htm' || lang === 'svg' || code.trim().charAt(0) === '<') htmlParts.push(code);
        else if (lang === '' || lang === 'code') {
            if (_looksReact(code)) reactParts.push(code);
            else if (code.trim().charAt(0) === '<') htmlParts.push(code);
            else if (code.indexOf('{') !== -1 && code.indexOf(':') !== -1 && code.indexOf(';') !== -1 && !/\b(function|=>|var |let |const )\b/.test(code)) cssParts.push(code);
            else jsParts.push(code);
        }
    }
    var allCode = htmlParts.join('\n') + cssParts.join('\n') + jsParts.join('\n') + reactParts.join('\n') + (fullHtml || '');
    var isSafe = true;
    for (var s = 0; s < _gcDanger.length; s++) { if (_gcDanger[s].test(allCode)) { isSafe = false; break; } }
    if (badge) { badge.textContent = isSafe ? '✓ Safe' : '⚠ Warning'; badge.className = 'gc-badge ' + (isSafe ? 'ok' : 'bad'); }
    var result;
    if (reactParts.length > 0 && !fullHtml) {
        result = _buildReactDoc(reactParts.join('\n\n'), cssParts.join('\n'), htmlParts.join('\n'));
    } else if (fullHtml) {
        result = fullHtml;
        if (cssParts.length > 0) { var ci = '<style>' + cssParts.join('\n') + '</style>'; result = result.indexOf('</head>') !== -1 ? result.replace('</head>', ci + '</head>') : ci + result; }
        if (jsParts.length > 0) { var ji = '<scr' + 'ipt>' + jsParts.join('\n') + '</scr' + 'ipt>'; result = result.indexOf('</body>') !== -1 ? result.replace('</body>', ji + '</body>') : result + ji; }
    } else {
        var body = htmlParts.length > 0 ? htmlParts.join('\n') : '';
        var tw = _looksTailwind(body + cssParts.join('\n')) ? '<scr' + 'ipt src="https://cdn.tailwindcss.com"></scr' + 'ipt>' : '';
        var css = cssParts.length > 0 ? '<style>' + cssParts.join('\n') + '</style>' : '';
        var js = '';
        if (jsParts.length > 0) { js = '<scr' + 'ipt>' + jsParts.join('\n').replace(/<\/script/gi, '<\\/script') + '</scr' + 'ipt>'; }
        var pad = tw ? '' : 'padding:20px;';
        result = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">' + tw + '<style>body{font-family:system-ui,-apple-system,sans-serif;' + pad + 'background:#fff;color:#111;}</style>' + css + '</head><body>' + body + js + '</body></html>';
    }
    _gcLastPreviewClean = result;        // publishable doc (no dev console injected)
    result = _injectConsole(result);
    _gcLastPreview = result;
    frame.srcdoc = result;
    panel.classList.add('open');
}
var _gcLastPreviewClean = '';
function _gcToast(msg) {
    var t = document.getElementById('gc-toast');
    if (!t) {
        t = document.createElement('div'); t.id = 'gc-toast';
        t.style.cssText = 'position:fixed;left:50%;bottom:30px;transform:translateX(-50%);background:#1b1b27;border:1px solid #2a2a3a;color:#e7e7ef;padding:10px 16px;border-radius:10px;font-size:13px;z-index:500;box-shadow:0 8px 30px rgba(0,0,0,.4);opacity:0;transition:opacity .15s';
        document.body.appendChild(t);
    }
    t.textContent = msg; t.style.opacity = '1';
    clearTimeout(t._h); t._h = setTimeout(function () { t.style.opacity = '0'; }, 2600);
}
async function gcPublishPreview() {
    var html = _gcLastPreviewClean || _gcLastPreview;
    if (!html) { _gcToast('Run a preview first.'); return; }
    var btn = document.getElementById('gc-publish');
    if (btn) btn.style.opacity = '.5';
    _gcToast('Publishing…');
    try {
        var j = await window.grg.billPost('/api/publish', { html: html });
        if (!j || !j.url) throw new Error((j && j.error) || 'Publish failed');
        var full = 'https://grg-ai.com' + j.url;
        try { await navigator.clipboard.writeText(full); } catch (e) {}
        gcShowPublished(full);
    } catch (e) {
        _gcToast('Publish failed: ' + (e && e.message || 'try again'));
    } finally { if (btn) btn.style.opacity = ''; }
}
function gcShowPublished(url) {
    var ov = document.getElementById('gc-pub-ov');
    if (!ov) {
        ov = document.createElement('div');
        ov.id = 'gc-pub-ov';
        ov.style.cssText = 'position:fixed;inset:0;z-index:400;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;padding:20px';
        ov.onclick = function (e) { if (e.target === ov) ov.style.display = 'none'; };
        ov.innerHTML = '<div style="background:var(--bg-surface,#15151f);border:1px solid var(--border,#2a2a3a);border-radius:14px;max-width:440px;width:100%;padding:22px;box-shadow:0 20px 60px rgba(0,0,0,.5)">'
            + '<div style="font-weight:700;font-size:15px;margin-bottom:6px">Published — live page</div>'
            + '<div style="color:var(--text-dim,#9a9ab0);font-size:12.5px;margin-bottom:14px">Anyone with this link can open your generated page. It runs sandboxed on grg-ai.com.</div>'
            + '<div style="display:flex;gap:8px"><input id="gc-pub-url" readonly style="flex:1;background:var(--bg,#0e0e16);border:1px solid var(--border,#2a2a3a);border-radius:8px;padding:9px 11px;color:var(--text,#e7e7ef);font-size:12.5px">'
            + '<button id="gc-pub-copy" style="background:linear-gradient(135deg,#8b5cf6,#6d28d9);color:#fff;border:0;border-radius:8px;padding:0 15px;font-weight:600;cursor:pointer">Copy</button></div>'
            + '<div style="display:flex;gap:8px;margin-top:13px">'
            + '<button id="gc-pub-open" style="flex:1;background:var(--bg,#0e0e16);border:1px solid var(--border,#2a2a3a);border-radius:8px;padding:9px;color:var(--text,#e7e7ef);cursor:pointer;font-size:12.5px">Open in browser</button>'
            + '<button id="gc-pub-close" style="flex:1;background:transparent;border:1px solid var(--border,#2a2a3a);border-radius:8px;padding:9px;color:var(--text-dim,#9a9ab0);cursor:pointer;font-size:12.5px">Close</button></div></div>';
        document.body.appendChild(ov);
        ov.querySelector('#gc-pub-copy').onclick = function () {
            var inp = document.getElementById('gc-pub-url'); inp.select();
            navigator.clipboard.writeText(inp.value).then(function () { _gcToast('Link copied'); }, function () {});
        };
        ov.querySelector('#gc-pub-open').onclick = function () {
            try { window.grg.openExternal(document.getElementById('gc-pub-url').value); } catch (e) {}
        };
        ov.querySelector('#gc-pub-close').onclick = function () { ov.style.display = 'none'; };
    }
    ov.querySelector('#gc-pub-url').value = url;
    ov.style.display = 'flex';
}
function gcSetDevice(btn, w) {
    var frame = document.getElementById('gc-frame');
    var btns = document.querySelectorAll('#gc-devices .pv-dev');
    for (var i = 0; i < btns.length; i++) btns[i].classList.remove('active');
    if (btn) btn.classList.add('active');
    if (!w) { frame.style.width = ''; frame.style.margin = ''; frame.style.maxWidth = ''; frame.parentElement.style.background = ''; }
    else { frame.style.width = w + 'px'; frame.style.maxWidth = '100%'; frame.style.margin = '0 auto'; frame.parentElement.style.background = 'var(--bg-surface)'; }
}
function gcRefreshPreview() {
    var frame = document.getElementById('gc-frame');
    if (_gcLastPreview) { frame.srcdoc = ''; setTimeout(function(){ frame.srcdoc = _gcLastPreview; }, 30); }
}
function gcPopoutPreview() {
    if (!_gcLastPreview) return;
    try { window.grg && window.grg.openPreview ? window.grg.openPreview(_gcLastPreview) : window.open('data:text/html;charset=utf-8,' + encodeURIComponent(_gcLastPreview), '_blank'); }
    catch (e) { window.open('data:text/html;charset=utf-8,' + encodeURIComponent(_gcLastPreview), '_blank'); }
}
function gcClosePreview() {
    document.getElementById('gc-preview').classList.remove('open');
    document.getElementById('gc-frame').srcdoc = '';
    var first = document.querySelector('#gc-devices .pv-dev'); if (first) gcSetDevice(first, 0);
}

function atBottom() { return chat.scrollHeight - chat.scrollTop - chat.clientHeight < 120; }
function scroll() { chat.scrollTop = chat.scrollHeight; }

// ─── transcript persistence ───
function trans() { const s = curSession(); return s ? (s.transcript = s.transcript || []) : []; }
function pushTrans(item) { const s = curSession(); if (s) { s.transcript = s.transcript || []; s.transcript.push(item); } }
async function persist() {
    const s = curSession(); if (!s) return;
    try { s.messages = await window.grg.getConversation(); } catch (e) {}
    s.folder = projectDir; s.ts = Date.now();
    if (!s.title || s.title === 'New session') { const u = (s.transcript || []).find(x => x.t === 'user'); if (u) s.title = u.text.slice(0, 46); }
    saveSessions(); renderSessions();
}

// ─── render ───
function clearWelcome() { const w = msgs.querySelector('.welcome'); if (w) w.remove(); }
function renderWelcome() {
    msgs.innerHTML = `<div class="welcome">
        <div class="logo">Grg<span class="dot">.</span>AI</div>
        <div class="ask">What should we build?</div>
        <div class="sub">Your AI coding agent — it reads, writes and runs code in <b>${esc(_projName(projectDir))}</b>.</div>
        <div class="examples">
            <div class="ex" data-p="Explore this project and give me a short overview of what it does and its structure."><b>Explain this project</b>Get an overview of the codebase</div>
            <div class="ex" data-p="Create a Python script hello.py that prints a colorful welcome banner, then run it."><b>Create &amp; run a script</b>Scaffold code and execute it</div>
            <div class="ex" data-p="Find bugs or improvements in this project and fix the most important one."><b>Find &amp; fix a bug</b>Review and patch the code</div>
            <div class="ex" data-p="Add a README.md with setup instructions for this project."><b>Write a README</b>Document the project</div>
        </div></div>`;
    msgs.querySelectorAll('.ex').forEach(el => el.onclick = () => { input.value = el.getAttribute('data-p'); autoSize(); send(); });
}
function addMsg(role, text) {
    clearWelcome();
    if (role === 'user') { const pc = document.getElementById('plan-card'); if (pc) pc.remove(); }  // fresh plan per task
    const wrap = atBottom();
    const div = document.createElement('div'); div.className = 'msg';
    div.innerHTML = `<div class="msg-head"><div class="av2 ${role === 'user' ? 'user' : 'ai'}">${role === 'user' ? 'U' : 'G'}</div><div class="who">${role === 'user' ? 'You' : 'Grg Code'}</div></div><div class="body">${fmt(text)}</div>`;
    msgs.appendChild(div); if (wrap) scroll();
}
// Visible task plan (TODO checklist) driven by the agent's update_plan tool.
function renderPlan(steps) {
    if (!Array.isArray(steps) || !steps.length) return;
    clearWelcome();
    const wrap = atBottom();
    let card = document.getElementById('plan-card');
    if (!card) { card = document.createElement('div'); card.id = 'plan-card'; card.className = 'plan-card'; }
    const done = steps.filter(s => s && s.status === 'done').length;
    let h = '<div class="plan-head"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg><span>Plan</span><span class="plan-count">' + done + '/' + steps.length + '</span></div>';
    h += steps.map(s => {
        const st = (s && s.status) || 'pending';
        const ic = st === 'done' ? '&#10003;' : (st === 'in_progress' ? '<span class="ps-spin"></span>' : '&#9675;');
        return '<div class="plan-step ' + st + '"><span class="ps-ic">' + ic + '</span><span class="ps-t">' + esc((s && s.title) || '') + '</span></div>';
    }).join('');
    card.innerHTML = h;
    msgs.appendChild(card);   // move to the bottom so it stays visible as work proceeds
    if (wrap) scroll();
}
function addStatus(text) {
    clearWelcome(); const old = $('status'); if (old) old.remove();
    const d = document.createElement('div'); d.className = 'status-line'; d.id = 'status';
    d.innerHTML = '<span class="spin"></span><span>' + esc(text) + '</span>';
    msgs.appendChild(d); scroll();
}
function clearStatus() { const s = $('status'); if (s) s.remove(); }
const toolCards = {};
function addToolCall(data) {
    if (data.name === 'task') { addSubAgent(data.id, (data.args && data.args.description) || 'exploring…'); return; }
    clearStatus(); const wrap = atBottom();
    var _docName = ''; if (data.name === 'create_document') { try { var _s = typeof data.args.spec === 'string' ? JSON.parse(data.args.spec) : data.args.spec; _docName = (_s && (_s.filename || _s.title || _s.type)) || 'document'; } catch (e) { _docName = 'document'; } }
    const argStr = data.name === 'run_command' ? (data.args.command || '') : data.name === 'git' ? ('git ' + (data.args.args || '')) : data.name === 'knowledge' ? (data.args.topic || 'list topics') : data.name === 'create_document' ? _docName : (data.args.path || data.args.query || JSON.stringify(data.args));
    const card = document.createElement('div'); card.className = 'tool';
    card.innerHTML = `<div class="tool-head"><span class="tname">${esc(data.name)}</span><span class="targ">${esc(argStr)}</span><span class="tstat"><span class="spin"></span></span></div><div class="tool-out"></div>`;
    card.querySelector('.tool-head').onclick = () => card.classList.toggle('open');
    msgs.appendChild(card); toolCards[data.id] = { card, name: data.name, arg: argStr }; if (wrap) scroll();
}
function setToolResult(data) {
    const rec = toolCards[data.id]; if (!rec) return;
    const bad = /^Error|^ERROR|denied|not found|not enabled/.test(data.result || '');
    rec.card.querySelector('.tstat').innerHTML = bad ? '<span class="dot-no">✕</span>' : '<span class="dot-ok">✓</span>';
    rec.card.querySelector('.tool-out').textContent = data.result || '(no output)';
    pushTrans({ t: 'tool', name: rec.name, arg: rec.arg, result: (data.result || '').slice(0, 4000), bad });
}
function renderToolStatic(item) {
    const card = document.createElement('div'); card.className = 'tool';
    card.innerHTML = `<div class="tool-head"><span class="tname">${esc(item.name)}</span><span class="targ">${esc(item.arg)}</span><span class="tstat">${item.bad ? '<span class="dot-no">✕</span>' : '<span class="dot-ok">✓</span>'}</span></div><div class="tool-out">${esc(item.result)}</div>`;
    card.querySelector('.tool-head').onclick = () => card.classList.toggle('open');
    msgs.appendChild(card);
}

// ─── sub-agent nested thread (task tool) ───
const subCards = {};
function _subArg(name, args) {
    if (!args) return '';
    if (name === 'search' || name === 'web_search') return args.query || '';
    if (name === 'fetch_url') return args.url || '';
    if (name === 'knowledge') return args.topic || 'list';
    return args.path || JSON.stringify(args || {}).slice(0, 80);
}
function addSubAgent(id, description) {
    clearStatus(); const wrap = atBottom();
    let rec = subCards[id];
    if (!rec) {
        const card = document.createElement('div'); card.className = 'subagent open';
        card.innerHTML = '<div class="sa-head"><span class="sa-ico">◆</span><span class="sa-title">Sub-agent</span><span class="sa-desc"></span><span class="sa-stat"><span class="spin"></span></span></div><div class="sa-body"></div><div class="sa-summary" style="display:none"></div>';
        card.querySelector('.sa-head').onclick = () => card.classList.toggle('open');
        msgs.appendChild(card);
        rec = subCards[id] = { card, rows: {} };
    }
    if (description) rec.card.querySelector('.sa-desc').textContent = description;
    if (wrap) scroll();
}
function subToolAdd(id, callId, name, args) {
    if (!subCards[id]) addSubAgent(id, '');
    const rec = subCards[id]; const body = rec.card.querySelector('.sa-body');
    const row = document.createElement('div'); row.className = 'sub-row';
    row.innerHTML = '<span class="sr-ic"><span class="spin"></span></span><span class="sr-name">' + esc(name) + '</span><span class="sr-arg">' + esc(_subArg(name, args)) + '</span>';
    const out = document.createElement('div'); out.className = 'sr-out'; out.style.display = 'none';
    row.onclick = () => { out.style.display = out.style.display === 'none' ? 'block' : 'none'; };
    body.appendChild(row); body.appendChild(out);
    rec.rows[callId] = { row, out };
    if (atBottom()) scroll();
}
function subToolResult(id, callId, name, result) {
    const rec = subCards[id]; if (!rec || !rec.rows[callId]) return;
    const bad = /^Error|^ERROR|denied|not found|not available/.test(result || '');
    rec.rows[callId].row.querySelector('.sr-ic').innerHTML = bad ? '<span class="dot-no">✕</span>' : '<span class="dot-ok">✓</span>';
    rec.rows[callId].out.textContent = result || '(no output)';
}
function subEnd(id, result, error) {
    const rec = subCards[id]; if (!rec) return;
    rec.card.querySelector('.sa-stat').innerHTML = error ? '<span class="dot-no">✕</span>' : '<span class="dot-ok">✓</span>';
    const sum = rec.card.querySelector('.sa-summary');
    sum.style.display = 'block'; sum.innerHTML = fmt(error ? ('Error: ' + error) : (result || ''));
    rec.card.classList.remove('open'); // collapse the steps, keep the summary visible
    pushTrans({ t: 'tool', name: 'task', arg: (rec.card.querySelector('.sa-desc').textContent || ''), result: (result || error || '').slice(0, 4000), bad: !!error });
}

// ─── MCP settings panel ───
let _mcpData = null, _mcpScope = 'global';
const MCP_PRESETS = {
    filesystem: { command: 'npx', args: ['-y', '@modelcontextprotocol/server-filesystem', '.'] },
    github: { command: 'npx', args: ['-y', '@modelcontextprotocol/server-github'], env: { GITHUB_TOKEN: '' } },
    memory: { command: 'npx', args: ['-y', '@modelcontextprotocol/server-memory'] },
    puppeteer: { command: 'npx', args: ['-y', '@modelcontextprotocol/server-puppeteer'] },
    sqlite: { command: 'npx', args: ['-y', '@modelcontextprotocol/server-sqlite', '--db-path', './data.db'] }
};
async function openMcp() {
    try { _mcpData = await window.grg.mcpGet(); } catch (e) { _mcpData = { global: { mcpServers: {} }, project: null, hasFolder: false, status: [] }; }
    if (!_mcpData.global) _mcpData.global = { mcpServers: {} };
    if (!_mcpData.global.mcpServers) _mcpData.global.mcpServers = _mcpData.global.servers || {};
    if (_mcpScope === 'project' && !_mcpData.hasFolder) _mcpScope = 'global';
    document.getElementById('mcp-ov').classList.add('show');
    renderMcp();
}
function closeMcp() { document.getElementById('mcp-ov').classList.remove('show'); }
function _mcpCfg() {
    if (_mcpScope === 'project') { if (!_mcpData.project) _mcpData.project = { mcpServers: {} }; if (!_mcpData.project.mcpServers) _mcpData.project.mcpServers = _mcpData.project.servers || {}; return _mcpData.project; }
    return _mcpData.global;
}
function _mcpStatusOf(name) { const key = String(name).replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase(); return (_mcpData.status || []).find(s => s.name.toLowerCase() === key); }
function renderMcp() {
    const body = document.getElementById('mcp-body');
    const servers = _mcpCfg().mcpServers || {};
    let h = '<div class="mcp-tabs">'
        + '<button class="mcp-tab ' + (_mcpScope === 'global' ? 'active' : '') + '" onclick="setMcpScope(\'global\')">Global · all projects</button>'
        + '<button class="mcp-tab ' + (_mcpScope === 'project' ? 'active' : '') + '"' + (_mcpData.hasFolder ? '' : ' disabled title="Open a project folder first"') + ' onclick="setMcpScope(\'project\')">This project</button></div>';
    const names = Object.keys(servers);
    if (!names.length) h += '<div class="mcp-empty">No MCP servers here yet. Add one below, or use a quick preset.</div>';
    names.forEach(n => {
        const s = servers[n] || {}; const st = _mcpStatusOf(n);
        const badge = s.disabled ? '<span class="mcp-badge off">disabled</span>'
            : (st ? '<span class="mcp-badge on">connected · ' + st.tools.length + ' tools</span>' : '<span class="mcp-badge">not connected</span>');
        h += '<div class="mcp-srv"><div class="ms-top"><b>' + esc(n) + '</b>' + badge + '</div>'
            + '<div class="ms-cmd">' + esc((s.command || '') + ' ' + ((s.args || []).join(' '))) + '</div>'
            + '<div class="ms-actions"><label class="ms-toggle"><input type="checkbox" ' + (s.disabled ? '' : 'checked') + ' onchange="toggleMcp(this,\'' + esc(n) + '\')"> enabled</label>'
            + '<button class="ms-del" onclick="delMcp(\'' + esc(n) + '\')">Delete</button></div></div>';
    });
    h += '<div class="mcp-presets">Quick add:'
        + Object.keys(MCP_PRESETS).map(k => ' <button onclick="presetMcp(\'' + k + '\')">' + k + '</button>').join('') + '</div>';
    h += '<div class="mcp-add"><div class="mcp-add-t">Add a server</div>'
        + '<input id="mcp-name" placeholder="name (e.g. github)">'
        + '<input id="mcp-cmd" placeholder="command (default: npx)">'
        + '<input id="mcp-args" placeholder="args, space-separated (e.g. -y @modelcontextprotocol/server-github)">'
        + '<textarea id="mcp-env" rows="2" placeholder="env, one per line: KEY=value"></textarea>'
        + '<button class="mcp-add-btn" onclick="addMcp()">Add to list</button></div>';
    h += '<div class="mcp-foot"><button class="mcp-save" onclick="saveMcp()">Save & Reconnect</button><span id="mcp-msg"></span></div>';
    body.innerHTML = h;
}
function setMcpScope(s) { if (s === 'project' && !_mcpData.hasFolder) return; _mcpScope = s; renderMcp(); }
function toggleMcp(el, n) { const c = _mcpCfg(); if (c.mcpServers[n]) c.mcpServers[n].disabled = !el.checked; }
function delMcp(n) { const c = _mcpCfg(); delete c.mcpServers[n]; renderMcp(); }
function addMcp() {
    const name = (document.getElementById('mcp-name').value || '').trim(); if (!name) return;
    const cmd = (document.getElementById('mcp-cmd').value || '').trim() || 'npx';
    const args = (document.getElementById('mcp-args').value || '').trim();
    const env = {}; (document.getElementById('mcp-env').value || '').split('\n').forEach(l => { const i = l.indexOf('='); if (i > 0) env[l.slice(0, i).trim()] = l.slice(i + 1).trim(); });
    const srv = { command: cmd, args: args ? args.split(/\s+/) : [] }; if (Object.keys(env).length) srv.env = env;
    _mcpCfg().mcpServers[name] = srv; renderMcp();
}
function presetMcp(key) { const p = MCP_PRESETS[key]; if (!p) return; _mcpCfg().mcpServers[key] = JSON.parse(JSON.stringify(p)); renderMcp(); }
async function saveMcp() {
    const msg = document.getElementById('mcp-msg'); msg.textContent = 'Saving & reconnecting…';
    try {
        const r = await window.grg.mcpSave(_mcpScope, _mcpCfg());
        if (r && r.error) { msg.textContent = 'Error: ' + r.error; return; }
        _mcpData.status = (r && r.status) || [];
        msg.textContent = 'Saved · ' + _mcpData.status.length + ' server(s) connected.';
        renderMcp();
    } catch (e) { msg.textContent = 'Error: ' + e.message; }
}
window.openMcp = openMcp; window.closeMcp = closeMcp; window.setMcpScope = setMcpScope;
window.toggleMcp = toggleMcp; window.delMcp = delMcp; window.addMcp = addMcp; window.presetMcp = presetMcp; window.saveMcp = saveMcp;

// ─── Slash-command editor ───
let _cmdData = null, _cmdScope = 'global', _cmdEditing = { name: '', body: '' };
async function openCmds() {
    const box = document.getElementById('cmd-hint'); if (box) box.style.display = 'none';
    try { _cmdData = await window.grg.commandsGet(); } catch (e) { _cmdData = { builtins: {}, global: [], project: null, hasFolder: false }; }
    if (_cmdScope === 'project' && !_cmdData.hasFolder) _cmdScope = 'global';
    _cmdEditing = { name: '', body: '' };
    document.getElementById('cmd-ov').classList.add('show');
    renderCmds();
}
function closeCmds() { document.getElementById('cmd-ov').classList.remove('show'); }
function _cmdCustomList() { return (_cmdScope === 'project' ? (_cmdData.project || []) : _cmdData.global) || []; }
function renderCmds() {
    const body = document.getElementById('cmd-body');
    const custom = _cmdCustomList();
    let h = '<div class="mcp-tabs">'
        + '<button class="mcp-tab ' + (_cmdScope === 'global' ? 'active' : '') + '" onclick="setCmdScope(\'global\')">Global · all projects</button>'
        + '<button class="mcp-tab ' + (_cmdScope === 'project' ? 'active' : '') + '"' + (_cmdData.hasFolder ? '' : ' disabled title="Open a project folder first"') + ' onclick="setCmdScope(\'project\')">This project</button></div>';
    // custom commands (editable)
    h += '<div class="cmd-sec">Your commands</div>';
    if (!custom.length) h += '<div class="mcp-empty">No custom commands in this scope yet. Create one below.</div>';
    custom.forEach(c => {
        h += '<div class="cmd-rowi"><span class="cmd-slug">/' + esc(c.name) + '</span>'
            + '<span class="cmd-prev">' + esc((c.body || '').replace(/\s+/g, ' ').slice(0, 60)) + '</span>'
            + '<button onclick="editCmd(\'' + esc(c.name) + '\')">Edit</button>'
            + '<button class="ms-del" onclick="deleteCmd(\'' + esc(c.name) + '\')">Delete</button></div>';
    });
    // builtins (customizable → creates an override)
    h += '<div class="cmd-sec">Built-in commands <span class="cmd-hintnote">(Customize makes an editable copy in this scope)</span></div>';
    Object.keys(_cmdData.builtins || {}).forEach(n => {
        h += '<div class="cmd-rowi"><span class="cmd-slug">/' + esc(n) + '</span>'
            + '<span class="cmd-prev">' + esc((_cmdData.builtins[n] || '').replace(/\s+/g, ' ').slice(0, 60)) + '</span>'
            + '<button onclick="customizeBuiltin(\'' + esc(n) + '\')">Customize</button></div>';
    });
    // editor
    h += '<div class="mcp-add"><div class="mcp-add-t">' + (_cmdEditing.name ? 'Edit /' + esc(_cmdEditing.name) : 'New command') + '</div>'
        + '<input id="cmd-name-in" placeholder="command name (e.g. pr)" value="' + esc(_cmdEditing.name) + '">'
        + '<textarea id="cmd-body-in" rows="5" placeholder="Prompt template. Use $ARGUMENTS for what the user types after the command.">' + esc(_cmdEditing.body) + '</textarea>'
        + '<div class="cmd-hintnote">Tip: <code>$ARGUMENTS</code> is replaced with the text after /' + esc(_cmdEditing.name || 'name') + '.</div>'
        + '<div class="mcp-foot"><button class="mcp-save" onclick="saveCmd()">Save command</button><button class="cmd-new" onclick="newCmd()">Clear</button><span id="cmd-msg"></span></div></div>';
    body.innerHTML = h;
}
function setCmdScope(s) { if (s === 'project' && !_cmdData.hasFolder) return; _cmdScope = s; renderCmds(); }
function editCmd(name) { const c = _cmdCustomList().find(x => x.name === name); _cmdEditing = { name: name, body: c ? c.body : '' }; renderCmds(); }
function customizeBuiltin(name) { _cmdEditing = { name: name, body: (_cmdData.builtins && _cmdData.builtins[name]) || '' }; renderCmds(); }
function newCmd() { _cmdEditing = { name: '', body: '' }; renderCmds(); }
async function saveCmd() {
    const name = (document.getElementById('cmd-name-in').value || '').trim();
    const bodyv = document.getElementById('cmd-body-in').value || '';
    const msg = document.getElementById('cmd-msg');
    if (!name) { msg.textContent = 'Give it a name.'; return; }
    if (!bodyv.trim()) { msg.textContent = 'Write the prompt template.'; return; }
    try {
        const r = await window.grg.commandSave(_cmdScope, name, bodyv);
        if (r && r.error) { msg.textContent = 'Error: ' + r.error; return; }
        _cmdData = await window.grg.commandsGet(); // refresh
        _cmdEditing = { name: '', body: '' };
        refreshCommands(); // update the / palette
        renderCmds();
        msg.textContent = 'Saved /' + (r.name || name) + '.';
    } catch (e) { msg.textContent = 'Error: ' + e.message; }
}
async function deleteCmd(name) {
    try {
        const r = await window.grg.commandDelete(_cmdScope, name);
        if (r && r.error) return;
        _cmdData = await window.grg.commandsGet();
        if (_cmdEditing.name === name) _cmdEditing = { name: '', body: '' };
        refreshCommands();
        renderCmds();
    } catch (e) {}
}
window.openCmds = openCmds; window.closeCmds = closeCmds; window.setCmdScope = setCmdScope;
window.editCmd = editCmd; window.customizeBuiltin = customizeBuiltin; window.newCmd = newCmd;
window.saveCmd = saveCmd; window.deleteCmd = deleteCmd;

// ─── Skills / knowledge manager ───
let _skData = null, _skScope = 'global', _skEditing = { name: '', body: '' };
async function openSkills() {
    try { _skData = await window.grg.knowledgeGet(); } catch (e) { _skData = { bundled: [], global: [], project: null, hasFolder: false }; }
    if (_skScope === 'project' && !_skData.hasFolder) _skScope = 'global';
    _skEditing = { name: '', body: '' };
    document.getElementById('sk-ov').classList.add('show');
    renderSkills();
}
function closeSkills() { document.getElementById('sk-ov').classList.remove('show'); }
function _skCustomList() { return (_skScope === 'project' ? (_skData.project || []) : _skData.global) || []; }
function renderSkills() {
    const body = document.getElementById('sk-body');
    const custom = _skCustomList();
    let h = '<div class="mcp-tabs">'
        + '<button class="mcp-tab ' + (_skScope === 'global' ? 'active' : '') + '" onclick="setSkillScope(\'global\')">Global · all projects</button>'
        + '<button class="mcp-tab ' + (_skScope === 'project' ? 'active' : '') + '"' + (_skData.hasFolder ? '' : ' disabled title="Open a project folder first"') + ' onclick="setSkillScope(\'project\')">This project</button></div>';
    h += '<div class="cmd-sec">Your skills</div>';
    if (!custom.length) h += '<div class="mcp-empty">No custom skills in this scope yet. Create one below, or Customize a built-in.</div>';
    custom.forEach(c => {
        h += '<div class="cmd-rowi"><span class="cmd-slug">' + esc(c.name) + '</span>'
            + '<span class="cmd-prev">' + esc((c.body || '').replace(/[#*`>\-]/g, '').replace(/\s+/g, ' ').slice(0, 55)) + '</span>'
            + '<button onclick="editSkill(\'' + esc(c.name) + '\')">Edit</button>'
            + '<button class="ms-del" onclick="deleteSkill(\'' + esc(c.name) + '\')">Delete</button></div>';
    });
    h += '<div class="cmd-sec">Built-in skills <span class="cmd-hintnote">(' + (_skData.bundled || []).length + ' — Customize makes an editable copy in this scope)</span></div>';
    (_skData.bundled || []).forEach(c => {
        h += '<div class="cmd-rowi"><span class="cmd-slug">' + esc(c.name) + '</span>'
            + '<span class="cmd-prev">' + esc((c.body || '').replace(/[#*`>\-]/g, '').replace(/\s+/g, ' ').slice(0, 55)) + '</span>'
            + '<button onclick="customizeSkill(\'' + esc(c.name) + '\')">Customize</button></div>';
    });
    h += '<div class="mcp-add"><div class="mcp-add-t">' + (_skEditing.name ? 'Edit skill: ' + esc(_skEditing.name) : 'New skill') + '</div>'
        + '<input id="sk-name-in" placeholder="skill name (e.g. graphql, my-stack)" value="' + esc(_skEditing.name) + '">'
        + '<textarea id="sk-body-in" rows="10" placeholder="Markdown knowledge the agent loads on demand. Keep it dense and practical: recommended stack, key commands, a minimal example, gotchas, a checklist.">' + esc(_skEditing.body) + '</textarea>'
        + '<div class="cmd-hintnote">The agent loads this when it calls <code>knowledge(&quot;' + esc(_skEditing.name || 'name') + '&quot;)</code> before building. Kept under ~8000 chars.</div>'
        + '<div class="mcp-foot"><button class="mcp-save" onclick="saveSkill()">Save skill</button><button class="cmd-new" onclick="newSkill()">Clear</button><span id="sk-msg"></span></div></div>';
    body.innerHTML = h;
}
function setSkillScope(s) { if (s === 'project' && !_skData.hasFolder) return; _skScope = s; renderSkills(); }
function editSkill(name) { const c = _skCustomList().find(x => x.name === name); _skEditing = { name: name, body: c ? c.body : '' }; renderSkills(); }
function customizeSkill(name) { const c = (_skData.bundled || []).find(x => x.name === name); _skEditing = { name: name, body: c ? c.body : '' }; renderSkills(); }
function newSkill() { _skEditing = { name: '', body: '' }; renderSkills(); }
async function saveSkill() {
    const name = (document.getElementById('sk-name-in').value || '').trim();
    const bodyv = document.getElementById('sk-body-in').value || '';
    const msg = document.getElementById('sk-msg');
    if (!name) { msg.textContent = 'Give the skill a name.'; return; }
    if (!bodyv.trim()) { msg.textContent = 'Write the knowledge content.'; return; }
    try {
        const r = await window.grg.knowledgeSave(_skScope, name, bodyv);
        if (r && r.error) { msg.textContent = 'Error: ' + r.error; return; }
        _skData = await window.grg.knowledgeGet();
        _skEditing = { name: '', body: '' };
        renderSkills();
        msg.textContent = 'Saved skill "' + (r.name || name) + '".';
    } catch (e) { msg.textContent = 'Error: ' + e.message; }
}
async function deleteSkill(name) {
    try {
        const r = await window.grg.knowledgeDelete(_skScope, name);
        if (r && r.error) return;
        _skData = await window.grg.knowledgeGet();
        if (_skEditing.name === name) _skEditing = { name: '', body: '' };
        renderSkills();
    } catch (e) {}
}
window.openSkills = openSkills; window.closeSkills = closeSkills; window.setSkillScope = setSkillScope;
window.editSkill = editSkill; window.customizeSkill = customizeSkill; window.newSkill = newSkill;
window.saveSkill = saveSkill; window.deleteSkill = deleteSkill;

// ─── Template manager ───
let _tplData = null, _tplScope = 'global', _tplEditing = { name: '', raw: '' };
function _tplSkeleton(name) {
    return '{\n  "name": "' + (name || 'my-template') + '",\n  "description": "What this starter is",\n  "run": ["npm install", "npm run dev"],\n  "files": [\n    { "path": "index.html", "content": "<h1>Hello from Grg Code</h1>" }\n  ]\n}';
}
async function openTemplates() {
    try { _tplData = await window.grg.templatesGet(); } catch (e) { _tplData = { bundled: [], global: [], project: null, hasFolder: false }; }
    if (_tplScope === 'project' && !_tplData.hasFolder) _tplScope = 'global';
    _tplEditing = { name: '', raw: '' };
    document.getElementById('tpl-ov').classList.add('show');
    renderTpls();
}
function closeTemplates() { document.getElementById('tpl-ov').classList.remove('show'); }
function _tplCustomList() { return (_tplScope === 'project' ? (_tplData.project || []) : _tplData.global) || []; }
function renderTpls() {
    const body = document.getElementById('tpl-body');
    const custom = _tplCustomList();
    let h = '<div class="mcp-tabs">'
        + '<button class="mcp-tab ' + (_tplScope === 'global' ? 'active' : '') + '" onclick="setTplScope(\'global\')">Global · all projects</button>'
        + '<button class="mcp-tab ' + (_tplScope === 'project' ? 'active' : '') + '"' + (_tplData.hasFolder ? '' : ' disabled title="Open a project folder first"') + ' onclick="setTplScope(\'project\')">This project</button></div>';
    h += '<div class="cmd-sec">Your templates</div>';
    if (!custom.length) h += '<div class="mcp-empty">No custom templates in this scope yet. Create one below, or Customize a built-in.</div>';
    custom.forEach(t => {
        h += '<div class="cmd-rowi"><span class="cmd-slug">' + esc(t.name) + '</span>'
            + '<span class="cmd-prev">' + esc((t.description || '') + ' · ' + t.fileCount + ' files') + '</span>'
            + '<button onclick="editTpl(\'' + esc(t.name) + '\')">Edit</button>'
            + '<button class="ms-del" onclick="deleteTpl(\'' + esc(t.name) + '\')">Delete</button></div>';
    });
    h += '<div class="cmd-sec">Built-in templates <span class="cmd-hintnote">(' + (_tplData.bundled || []).length + ' — Customize makes an editable copy)</span></div>';
    (_tplData.bundled || []).forEach(t => {
        h += '<div class="cmd-rowi"><span class="cmd-slug">' + esc(t.name) + '</span>'
            + '<span class="cmd-prev">' + esc((t.description || '') + ' · ' + t.fileCount + ' files') + '</span>'
            + '<button onclick="customizeTpl(\'' + esc(t.name) + '\')">Customize</button></div>';
    });
    h += '<div class="mcp-add"><div class="mcp-add-t">' + (_tplEditing.name ? 'Edit template: ' + esc(_tplEditing.name) : 'New template') + '</div>'
        + '<input id="tpl-name-in" placeholder="template name (e.g. sveltekit-app)" value="' + esc(_tplEditing.name) + '">'
        + '<textarea id="tpl-json-in" rows="12" spellcheck="false" placeholder="Template JSON">' + esc(_tplEditing.raw || _tplSkeleton(_tplEditing.name)) + '</textarea>'
        + '<div class="cmd-hintnote">JSON: <code>{name, description, run:[cmds], files:[{path, content}]}</code>. The agent creates it via <code>scaffold("name")</code>.</div>'
        + '<div class="mcp-foot"><button class="mcp-save" onclick="saveTpl()">Save template</button><button class="cmd-new" onclick="newTpl()">Clear</button><span id="tpl-msg"></span></div></div>';
    body.innerHTML = h;
}
function setTplScope(s) { if (s === 'project' && !_tplData.hasFolder) return; _tplScope = s; renderTpls(); }
function editTpl(name) { const t = _tplCustomList().find(x => x.name === name); _tplEditing = { name: name, raw: t ? t.raw : '' }; renderTpls(); }
function customizeTpl(name) { const t = (_tplData.bundled || []).find(x => x.name === name); _tplEditing = { name: name, raw: t ? t.raw : '' }; renderTpls(); }
function newTpl() { _tplEditing = { name: '', raw: '' }; renderTpls(); }
async function saveTpl() {
    const name = (document.getElementById('tpl-name-in').value || '').trim();
    const json = document.getElementById('tpl-json-in').value || '';
    const msg = document.getElementById('tpl-msg');
    if (!name) { msg.textContent = 'Give the template a name.'; return; }
    try {
        const r = await window.grg.templateSave(_tplScope, name, json);
        if (r && r.error) { msg.textContent = 'Error: ' + r.error; return; }
        _tplData = await window.grg.templatesGet();
        _tplEditing = { name: '', raw: '' };
        renderTpls();
        msg.textContent = 'Saved template "' + (r.name || name) + '".';
    } catch (e) { msg.textContent = 'Error: ' + e.message; }
}
async function deleteTpl(name) {
    try { const r = await window.grg.templateDelete(_tplScope, name); if (r && r.error) return; _tplData = await window.grg.templatesGet(); if (_tplEditing.name === name) _tplEditing = { name: '', raw: '' }; renderTpls(); } catch (e) {}
}
window.openTemplates = openTemplates; window.closeTemplates = closeTemplates; window.setTplScope = setTplScope;
window.editTpl = editTpl; window.customizeTpl = customizeTpl; window.newTpl = newTpl; window.saveTpl = saveTpl; window.deleteTpl = deleteTpl;

// ─── Project memory (GRGCODE.md) editor ───
async function openMemory() {
    let d; try { d = await window.grg.memoryGet(); } catch (e) { d = { hasFolder: false, content: '', source: null }; }
    const body = document.getElementById('mem-body');
    if (!d.hasFolder) {
        body.innerHTML = '<div class="mcp-empty">Open a project folder first — project memory (GRGCODE.md) is per-project.</div>';
    } else {
        let note = '';
        if (d.source && d.source !== 'GRGCODE.md') note = '<div class="cmd-hintnote" style="margin-bottom:8px">The agent currently reads <b>' + esc(d.source) + '</b>. Saving here creates GRGCODE.md, which takes priority.</div>';
        body.innerHTML = note
            + '<textarea id="mem-in" rows="16" spellcheck="false" placeholder="# Project notes for Grg Code&#10;&#10;- How to run / build / test&#10;- Stack &amp; architecture&#10;- Conventions and gotchas">' + esc(d.content) + '</textarea>'
            + '<div class="cmd-hintnote">Loaded into the agent\'s context every session. The agent can also append here with the <code>remember</code> tool.</div>'
            + '<div class="mcp-foot"><button class="mcp-save" onclick="saveMemory()">Save GRGCODE.md</button><span id="mem-msg"></span></div>';
    }
    document.getElementById('mem-ov').classList.add('show');
}
function closeMemory() { document.getElementById('mem-ov').classList.remove('show'); }
async function saveMemory() {
    const el = document.getElementById('mem-in'); if (!el) return;
    const msg = document.getElementById('mem-msg');
    try { const r = await window.grg.memorySave(el.value); if (r && r.error) { msg.textContent = 'Error: ' + r.error; return; } msg.textContent = 'Saved — loaded into the agent every session.'; }
    catch (e) { msg.textContent = 'Error: ' + e.message; }
}
window.openMemory = openMemory; window.closeMemory = closeMemory; window.saveMemory = saveMemory;

// ─── consolidated "Manage" menu ───
function toggleToolsMenu(e) { if (e) e.stopPropagation(); const m = document.getElementById('tools-menu'); if (m) m.classList.toggle('open'); }
function closeToolsMenu() { const m = document.getElementById('tools-menu'); if (m) m.classList.remove('open'); }
document.addEventListener('click', (e) => { if (!e.target.closest('#tools-dd')) closeToolsMenu(); });
window.toggleToolsMenu = toggleToolsMenu; window.closeToolsMenu = closeToolsMenu;
// simple line-level diff (LCS) → array of {t:'ctx'|'add'|'del', s}
function lineDiff(oldText, newText) {
    const a = String(oldText || '').split('\n'), b = String(newText || '').split('\n');
    const n = a.length, m = b.length;
    if (n * m > 400000) { // too big to diff cheaply — show as full replacement
        return a.map(s => ({ t: 'del', s })).concat(b.map(s => ({ t: 'add', s })));
    }
    const dp = Array.from({ length: n + 1 }, () => new Int32Array(m + 1));
    for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--)
        dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    const out = []; let i = 0, j = 0;
    while (i < n && j < m) {
        if (a[i] === b[j]) { out.push({ t: 'ctx', s: a[i] }); i++; j++; }
        else if (dp[i + 1][j] >= dp[i][j + 1]) { out.push({ t: 'del', s: a[i] }); i++; }
        else { out.push({ t: 'add', s: b[j] }); j++; }
    }
    while (i < n) out.push({ t: 'del', s: a[i++] });
    while (j < m) out.push({ t: 'add', s: b[j++] });
    return out;
}
function diffHtml(oldText, newText) {
    const rows = lineDiff(oldText, newText);
    const MAX = 300;
    const shown = rows.slice(0, MAX);
    let html = shown.map(r => {
        const sign = r.t === 'add' ? '+' : r.t === 'del' ? '-' : ' ';
        return `<div class="dl ${r.t}">${esc(sign + ' ' + r.s)}</div>`;
    }).join('');
    if (rows.length > MAX) html += `<div class="dl more">… ${rows.length - MAX} more lines</div>`;
    return html || '<div class="dl ctx">(no changes)</div>';
}
function addApproval(data) {
    clearStatus();
    const div = document.createElement('div'); div.className = 'approval';
    const hasDiff = data.diffOld !== undefined || data.diffNew !== undefined;
    const icon = data.kind === 'command'
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>';
    const bodyHtml = hasDiff
        ? `<div class="ap-diff">${diffHtml(data.diffOld, data.diffNew)}</div>`
        : `<div class="ap-body">${esc(data.kind === 'command' ? ('$ ' + data.command) : (data.path + '\n\n' + (data.preview || '')))}</div>`;
    div.innerHTML = `<div class="ap-title">${icon} ${esc(data.title)}${data.path ? ' — ' + esc(data.path) : ''}</div>${bodyHtml}<div class="ap-actions"><button class="ap-btn ap-yes">Approve</button><button class="ap-btn ap-no">Deny</button></div>`;
    const done = (ok) => { window.grg.approve(data.id, ok); div.querySelector('.ap-actions').innerHTML = '<span style="font-size:12px;color:' + (ok ? 'var(--green)' : 'var(--text-mute)') + '">' + (ok ? '✓ Approved' : '✕ Denied') + '</span>'; };
    div.querySelector('.ap-yes').onclick = () => done(true);
    div.querySelector('.ap-no').onclick = () => done(false);
    msgs.appendChild(div); scroll();
}

function renderTranscript() {
    msgs.innerHTML = '';
    const s = curSession();
    if (!s || !s.transcript || !s.transcript.length) { renderWelcome(); return; }
    for (const it of s.transcript) {
        if (it.t === 'user') addMsg('user', it.text);
        else if (it.t === 'assistant') addMsg('assistant', it.text);
        else if (it.t === 'tool') renderToolStatic(it);
    }
    scroll();
}

// ─── sessions sidebar ───
function _projName(f) { if (!f) return 'No folder'; return f.replace(/[\\/]+$/, '').split(/[\\/]/).pop() || f; }
function renderSessions() {
    const list = $('sessions');
    if (!sessions.length) { list.innerHTML = '<li class="sess-empty">No sessions yet</li>'; return; }
    const groups = {};
    sessions.forEach(s => { const f = s.folder || 'No folder'; (groups[f] = groups[f] || []).push(s); });
    const folders = Object.keys(groups).sort((a, b) => Math.max(...groups[b].map(x => x.ts || 0)) - Math.max(...groups[a].map(x => x.ts || 0)));
    const folderSvg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>';
    let html = '';
    folders.forEach(f => {
        html += '<div class="sgroup-label" title="' + esc(f) + '">' + folderSvg + '<span>' + esc(_projName(f)) + '</span></div>';
        groups[f].sort((a, b) => (b.ts || 0) - (a.ts || 0)).forEach(s => {
            html += '<li class="sess ' + (s.id === curId ? 'active' : '') + '" data-id="' + s.id + '"><span class="st">' + esc(s.title || 'New session') + '</span><button class="sdel" data-id="' + s.id + '" title="Delete">✕</button></li>';
        });
    });
    list.innerHTML = html;
    list.querySelectorAll('.sess').forEach(li => li.onclick = (e) => { if (e.target.classList.contains('sdel')) return; loadSession(li.getAttribute('data-id')); });
    list.querySelectorAll('.sdel').forEach(b => b.onclick = (e) => { e.stopPropagation(); delSession(b.getAttribute('data-id')); });
}
function setTitle() { const s = curSession(); $('sess-title').textContent = s ? (s.title || 'New session') : 'New session'; }
function newSession() {
    const s = { id: makeId(), title: 'New session', folder: projectDir, transcript: [], messages: [], ts: Date.now() };
    sessions.unshift(s); curId = s.id;
    window.grg.newSession();
    saveSessions(); renderSessions(); setTitle(); renderWelcome(); input.focus();
}
async function loadSession(id) {
    if (busy) return;
    const s = sessions.find(x => x.id === id); if (!s) return;
    curId = id;
    if (s.folder && s.folder !== projectDir) { projectDir = s.folder; window.grg.setFolder(s.folder); setFolder(s.folder); }
    window.grg.setConversation(s.messages || []);
    renderSessions(); setTitle(); renderTranscript();
}
function delSession(id) {
    sessions = sessions.filter(s => s.id !== id);
    saveSessions();
    if (curId === id) { curId = null; if (sessions.length) loadSession(sessions.sort((a, b) => (b.ts || 0) - (a.ts || 0))[0].id); else newSession(); }
    else renderSessions();
}

// ─── send / controls ───
function setBusy(v) { busy = v; $('send').style.display = v ? 'none' : 'flex'; $('stop').style.display = v ? 'flex' : 'none'; }
function send() {
    const text = input.value.trim(); if (!text || busy) return;
    if (!curSession()) newSession();
    const hint = document.getElementById('cmd-hint'); if (hint) hint.style.display = 'none';
    const fhint = document.getElementById('file-hint'); if (fhint) fhint.style.display = 'none';
    addMsg('user', text); pushTrans({ t: 'user', text });   // show the user's ORIGINAL text
    input.value = ''; autoSize(); setBusy(true); addStatus('Grg is thinking…');
    // Private agents: redact PII in the TYPED text only (never file contents) before it leaves.
    window.grg.send((typeof _grgAgent !== 'undefined' && _grgAgent && _agentsAllowed()) ? _piiRedact(text) : text);
}

// ─── slash commands (reusable prompts) ───
let _commands = [];
try { if (window.grg.listCommands) window.grg.listCommands().then(c => { _commands = c || []; }); } catch (e) {}
function refreshCommands() { try { window.grg.listCommands().then(c => { _commands = c || []; }); } catch (e) {} }
function updateCmdHint() {
    const box = document.getElementById('cmd-hint'); if (!box) return;
    const m = input.value.match(/^\/([a-zA-Z0-9_-]*)$/);
    if (!m) { box.style.display = 'none'; box.innerHTML = ''; return; }
    const q = m[1].toLowerCase();
    const matches = _commands.filter(c => c.toLowerCase().startsWith(q)).slice(0, 8);
    let h = matches.map((c, i) => '<div class="cmd-item' + (i === 0 ? ' sel' : '') + '" data-cmd="' + c + '">/' + c + '</div>').join('');
    h += '<div class="cmd-manage" onclick="openCmds()">✎ Manage commands…</div>';
    box.innerHTML = h;
    box.style.display = 'block';
    box.querySelectorAll('.cmd-item').forEach(el => el.onclick = () => { input.value = '/' + el.getAttribute('data-cmd') + ' '; box.style.display = 'none'; input.focus(); autoSize(); });
}

// ─── @-file mentions ───
let _files = [];
function refreshFiles() { try { if (window.grg.listFiles) window.grg.listFiles().then(f => { _files = f || []; }); } catch (e) {} }
refreshFiles();
function _atToken() {
    const v = input.value, pos = input.selectionStart != null ? input.selectionStart : v.length;
    const m = v.slice(0, pos).match(/(?:^|\s)@([\w./\\-]*)$/);
    return m ? { q: m[1], at: pos - m[1].length - 1, end: pos } : null;
}
function updateFileHint() {
    const box = document.getElementById('file-hint'); if (!box) return;
    const t = _atToken();
    if (!t) { box.style.display = 'none'; box.innerHTML = ''; return; }
    const q = t.q.toLowerCase();
    let matches = _files.filter(f => f.toLowerCase().indexOf(q) >= 0);
    matches.sort((a, b) => (b.split('/').pop().toLowerCase().startsWith(q) ? 1 : 0) - (a.split('/').pop().toLowerCase().startsWith(q) ? 1 : 0));
    matches = matches.slice(0, 8);
    if (!matches.length) { box.style.display = 'none'; return; }
    box.innerHTML = matches.map((f, i) => '<div class="cmd-item' + (i === 0 ? ' sel' : '') + '" data-f="' + f.replace(/"/g, '&quot;') + '">@' + f + '</div>').join('');
    box.style.display = 'block';
    box.querySelectorAll('.cmd-item').forEach(el => el.onclick = () => completeFile(el.getAttribute('data-f')));
}
function completeFile(f) {
    const t = _atToken(); if (!t) return;
    const v = input.value;
    input.value = v.slice(0, t.at) + '@' + f + ' ' + v.slice(t.end);
    document.getElementById('file-hint').style.display = 'none';
    input.focus(); autoSize();
}

// ─── Checkpoints / Undo ───
function showUndo(id, count) {
    clearStatus();
    const div = document.createElement('div'); div.className = 'status-line';
    div.innerHTML = '<span style="color:var(--text-dim)">Changed ' + count + ' file' + (count > 1 ? 's' : '') + ' this task.</span> ';
    const b = document.createElement('button'); b.textContent = '↶ Undo'; b.className = 'undo-btn';
    b.onclick = async () => { b.disabled = true; b.textContent = 'Reverting…'; try { const r = await window.grg.revertCheckpoint(id); div.innerHTML = '<span style="color:var(--amber)">↶ Reverted ' + ((r && (r.restored + r.removed)) || '') + ' file change(s).</span>'; renderFileTree && renderFileTree(); } catch (e) { div.textContent = 'Revert failed: ' + e.message; } };
    div.appendChild(b);
    msgs.appendChild(div); if (atBottom()) scroll();
}
let _cpData = [];
async function openCheckpoints() {
    try { _cpData = await window.grg.listCheckpoints(); } catch (e) { _cpData = []; }
    const body = document.getElementById('cp-body');
    if (!_cpData.length) { body.innerHTML = '<div class="mcp-empty">No checkpoints yet. They\'re created automatically whenever Grg changes files in a task.</div>'; }
    else {
        body.innerHTML = _cpData.map(c => {
            const when = new Date(c.ts).toLocaleTimeString();
            return '<div class="cmd-rowi"><span class="cmd-slug" style="color:var(--text-mute)">' + when + '</span>'
                + '<span class="cmd-prev">' + esc(c.user || '(task)') + ' · ' + c.count + ' file' + (c.count > 1 ? 's' : '') + '</span>'
                + (c.reverted ? '<span style="color:var(--amber);font-size:11.5px">reverted</span>' : '<button onclick="revertCp(\'' + c.id + '\')">↶ Revert</button>') + '</div>';
        }).join('');
    }
    document.getElementById('cp-ov').classList.add('show');
}
function closeCheckpoints() { document.getElementById('cp-ov').classList.remove('show'); }
async function revertCp(id) {
    try { await window.grg.revertCheckpoint(id); renderFileTree && renderFileTree(); openCheckpoints(); } catch (e) {}
}
window.openCheckpoints = openCheckpoints; window.closeCheckpoints = closeCheckpoints; window.revertCp = revertCp;
function autoSize() { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight, 200) + 'px'; }
function setFolder(p) {
    projectDir = p || '';
    $('folder-path').textContent = projectDir ? _projName(projectDir) : 'No folder';
    $('folder-path').title = projectDir || 'No folder selected — pick one for file work, or just chat';
    var clr = $('folder-clear'); if (clr) clr.style.display = projectDir ? 'flex' : 'none';
    renderFileTree();
    refreshCommands();  // project .grgcode/commands are folder-scoped
    refreshFiles();     // for @-mentions autocomplete
}
function clearFolder() {
    window.grg.setFolder('');
    setFolder('');
    if (curSession()) { curSession().folder = ''; saveSessions(); renderSessions(); }
}
window.clearFolder = clearFolder;

// ─── File Explorer ───
function _ftIcon(dir) {
    return dir
        ? '<svg class="ft-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>'
        : '<svg class="ft-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>';
}
function _ftBuild(nodes) {
    const ul = document.createElement('div');
    for (const n of (nodes || [])) {
        const row = document.createElement('div');
        row.className = 'ft-row' + (n.dir ? ' dir' : '');
        row.innerHTML = _ftIcon(n.dir) + '<span class="ft-name">' + escHtml(n.name) + '</span>';
        ul.appendChild(row);
        if (n.dir) {
            const kids = document.createElement('div');
            kids.className = 'ft-children closed';
            kids.appendChild(_ftBuild(n.children || []));
            ul.appendChild(kids);
            row.onclick = (e) => { e.stopPropagation(); kids.classList.toggle('closed'); };
        } else {
            row.onclick = (e) => { e.stopPropagation(); openFileViewer(n.path); };
        }
    }
    return ul;
}
function escHtml(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
async function renderFileTree() {
    const box = $('file-tree'); if (!box) return;
    let tree = [];
    try { tree = await window.grg.listTree(); } catch (e) {}
    box.innerHTML = '';
    if (!tree || !tree.length) { box.innerHTML = '<div class="ft-empty">Empty or no folder</div>'; return; }
    box.appendChild(_ftBuild(tree));
}
// ─── Monaco code editor (opened from the File Explorer) ───
const _MLANG = { js:'javascript', jsx:'javascript', mjs:'javascript', cjs:'javascript', ts:'typescript', tsx:'typescript', json:'json', html:'html', htm:'html', css:'css', scss:'scss', less:'less', md:'markdown', markdown:'markdown', py:'python', rb:'ruby', go:'go', rs:'rust', java:'java', c:'c', h:'c', cpp:'cpp', cc:'cpp', hpp:'cpp', cs:'csharp', php:'php', sh:'shell', bash:'shell', yml:'yaml', yaml:'yaml', xml:'xml', sql:'sql', toml:'ini', ini:'ini', vue:'html', svelte:'html' };
function _langFor(p) { const ext = (p.split('.').pop() || '').toLowerCase(); return _MLANG[ext] || 'plaintext'; }
let _monaco = null, _editor = null, _fvPath = null, _fvClean = '';
function ensureMonaco(cb) {
    if (_monaco) return cb();
    if (!window.require) return cb('no-monaco');
    try { window.require(['vs/editor/editor.main'], function () { _monaco = window.monaco; cb(); }); }
    catch (e) { cb('no-monaco'); }
}
function _updateDirty() {
    if (!_editor) return;
    const dirty = _editor.getValue() !== _fvClean;
    const d = $('fv-dirty'); if (d) d.textContent = dirty ? '● unsaved' : '';
    const s = $('fv-save'); if (s) s.disabled = !dirty;
}
async function openFileViewer(path) {
    const ov = $('fv-overlay'); if (!ov) return;
    _fvPath = path;
    $('fv-path').textContent = path;
    $('fv-dirty').textContent = '';
    ov.classList.add('open');
    let content = '';
    try { content = await window.grg.readFileDirect(path); } catch (e) { content = 'Error: ' + e.message; }
    _fvClean = content;
    ensureMonaco(function (err) {
        const host = $('fv-editor');
        if (err || !_monaco) { host.textContent = content; return; }
        if (!_editor) {
            _editor = _monaco.editor.create(host, { value: content, language: _langFor(path), theme: 'vs-dark', automaticLayout: true, fontSize: 13, minimap: { enabled: false }, scrollBeyondLastLine: false, tabSize: 2 });
            _editor.onDidChangeModelContent(_updateDirty);
            _editor.addCommand(_monaco.KeyMod.CtrlCmd | _monaco.KeyCode.KeyS, saveFileViewer);
        } else {
            _monaco.editor.setModelLanguage(_editor.getModel(), _langFor(path));
            _editor.setValue(content);
        }
        _updateDirty();
        setTimeout(function () { try { _editor.layout(); } catch (e) {} }, 40);
    });
}
async function saveFileViewer() {
    if (!_editor || !_fvPath) return;
    const content = _editor.getValue();
    const r = await window.grg.writeFileDirect(_fvPath, content);
    if (r === 'ok') { _fvClean = content; const d = $('fv-dirty'); if (d) d.textContent = '✓ saved'; $('fv-save').disabled = true; renderFileTree(); }
    else { const d = $('fv-dirty'); if (d) d.textContent = r || 'save failed'; }
}
function closeFileViewer() { const ov = $('fv-overlay'); if (ov) ov.classList.remove('open'); }
window.closeFileViewer = closeFileViewer;
window.saveFileViewer = saveFileViewer;
(function () {
    const t = $('files-toggle'), tree = $('file-tree');
    if (t && tree) t.onclick = (e) => { if (e.target.id === 'files-refresh') return; t.classList.toggle('closed'); tree.classList.toggle('closed'); };
    const r = $('files-refresh'); if (r) r.onclick = (e) => { e.stopPropagation(); renderFileTree(); };
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && $('fv-overlay').classList.contains('open')) closeFileViewer(); });
})();

// ─── Persistent terminal ───
let _termOpen = false, _termHist = [], _termHi = -1;
function toggleTerm(force) {
    _termOpen = (force !== undefined) ? force : !_termOpen;
    $('term-panel').classList.toggle('open', _termOpen);
    $('term-toggle').classList.toggle('active', _termOpen);
    if (_termOpen) { window.grg.termStart(); setTimeout(() => $('term-in').focus(), 60); }
}
function termWrite(text) { const out = $('term-out'); if (!out) return; out.textContent += text; out.scrollTop = out.scrollHeight; }
window.grg.on('term-output', (d) => termWrite(d));
window.grg.on('term-exit', (code) => termWrite('\n[shell exited' + (code != null ? ' (' + code + ')' : '') + ']\n'));
(function () {
    const tin = $('term-in');
    $('term-toggle').onclick = () => toggleTerm();
    $('term-hide').onclick = () => toggleTerm(false);
    $('term-clear').onclick = () => { $('term-out').textContent = ''; tin.focus(); };
    $('term-restart').onclick = () => { window.grg.termKill(); $('term-out').textContent = ''; setTimeout(() => window.grg.termStart(), 120); tin.focus(); };
    tin.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const v = tin.value;
            termWrite('❯ ' + v + '\n');
            if (v.trim()) { _termHist.push(v); if (_termHist.length > 100) _termHist.shift(); }
            _termHi = _termHist.length;
            window.grg.termInput(v);
            tin.value = '';
        } else if (e.key === 'ArrowUp') { if (_termHi > 0) { _termHi--; tin.value = _termHist[_termHi] || ''; } e.preventDefault(); }
        else if (e.key === 'ArrowDown') { if (_termHi < _termHist.length - 1) { _termHi++; tin.value = _termHist[_termHi] || ''; } else { _termHi = _termHist.length; tin.value = ''; } e.preventDefault(); }
    });
})();

// ─── reasoning ("thinking") bubble ───
let reasonWrap = null, reasonBody = null, reasonText = '', reasonLast = 0, reasonCollapsed = false;
function ensureReason() {
    if (reasonBody) return;
    clearStatus(); clearWelcome();
    const wrap = atBottom();
    const d = document.createElement('div'); d.className = 'think open';
    d.innerHTML = '<div class="think-head"><span class="think-ico">✦</span><span class="think-t">Thinking…</span><span class="think-chev">▾</span></div><div class="think-body"></div>';
    d.querySelector('.think-head').onclick = () => d.classList.toggle('open');
    msgs.appendChild(d); reasonWrap = d; reasonBody = d.querySelector('.think-body');
    reasonCollapsed = false;
    if (wrap) scroll();
}
function collapseReason() {
    if (reasonWrap && !reasonCollapsed) {
        reasonBody.textContent = reasonText;
        reasonWrap.querySelector('.think-t').textContent = 'Thought process';
        reasonWrap.classList.remove('open');
        reasonCollapsed = true;
    }
}
function finalizeReason() {
    if (reasonWrap) {
        if (reasonText.trim()) { reasonBody.textContent = reasonText; reasonWrap.querySelector('.think-t').textContent = 'Thought process'; reasonWrap.classList.remove('open'); }
        else reasonWrap.remove();
    }
    reasonWrap = null; reasonBody = null; reasonText = ''; reasonCollapsed = false;
}

// ─── streaming assistant bubble ───
let streamBody = null, streamText = '', streamLast = 0;
function finalizeStream() {
    finalizeReason();
    if (streamBody) {
        var _ft = (typeof _grgAgent !== 'undefined' && _grgAgent && _agentsAllowed()) ? _piiRestore(streamText) : streamText;
        streamBody.innerHTML = fmt(_ft);
        if (_ft.trim()) pushTrans({ t: 'assistant', text: _ft });
    }
    streamBody = null; streamText = '';
}
function ensureStreamBubble() {
    if (streamBody) return;
    clearStatus(); clearWelcome();
    const wrap = atBottom();
    const div = document.createElement('div'); div.className = 'msg';
    div.innerHTML = '<div class="msg-head"><div class="av2 ai">G</div><div class="who">Grg Code</div></div><div class="body"></div>';
    msgs.appendChild(div); streamBody = div.querySelector('.body');
    if (wrap) scroll();
}

// ─── agent events ───
window.grg.on('assistant-text', (t) => { finalizeStream(); clearStatus(); var _rt = (typeof _grgAgent !== 'undefined' && _grgAgent && _agentsAllowed()) ? _piiRestore(t) : t; addMsg('assistant', _rt); pushTrans({ t: 'assistant', text: _rt }); });
window.grg.on('assistant-reasoning', (tok) => {
    ensureReason();
    reasonText += tok;
    const now = Date.now();
    if (now - reasonLast > 50) { reasonLast = now; reasonBody.textContent = reasonText; if (atBottom()) scroll(); }
});
window.grg.on('assistant-token', (tok) => {
    collapseReason();
    ensureStreamBubble();
    streamText += tok;
    const now = Date.now();
    if (now - streamLast > 50) { streamLast = now; streamBody.innerHTML = fmt((typeof _grgAgent !== 'undefined' && _grgAgent && _agentsAllowed()) ? _piiRestore(streamText) : streamText); if (atBottom()) scroll(); }
});
window.grg.on('assistant-flush', () => finalizeStream());
window.grg.on('tool-call', (d) => { finalizeStream(); addToolCall(d); });
window.grg.on('tool-result', (d) => setToolResult(d));
window.grg.on('subagent-start', (d) => { finalizeStream(); addSubAgent(d.id, d.description); });
window.grg.on('subagent-tool', (d) => subToolAdd(d.id, d.callId, d.name, d.args));
window.grg.on('subagent-tool-result', (d) => subToolResult(d.id, d.callId, d.name, d.result));
window.grg.on('subagent-end', (d) => subEnd(d.id, d.result, d.error));
window.grg.on('approval-request', (d) => { finalizeStream(); addApproval(d); });
window.grg.on('agent-status', (t) => { finalizeStream(); addStatus(t); });
window.grg.on('agent-plan', (steps) => { finalizeStream(); renderPlan(steps); });
window.grg.on('agent-compacted', () => { finalizeStream(); clearStatus(); const d = document.createElement('div'); d.className = 'status-line'; d.textContent = '— context auto-compacted —'; d.style.opacity = '.6'; msgs.appendChild(d); scroll(); });
window.grg.on('agent-error', (e) => { finalizeStream(); clearStatus(); const d = document.createElement('div'); d.className = 'status-line err'; d.textContent = '⚠ ' + e; msgs.appendChild(d); scroll(); });
window.grg.on('agent-stopped', () => { finalizeStream(); clearStatus(); const d = document.createElement('div'); d.className = 'status-line'; d.textContent = 'Stopped.'; msgs.appendChild(d); });
window.grg.on('agent-done', () => { finalizeStream(); clearStatus(); });
window.grg.on('agent-idle', () => { finalizeStream(); clearStatus(); setBusy(false); persist(); input.focus(); });
window.grg.on('checkpoint', (d) => { if (d && d.count) showUndo(d.id, d.count); });

$('send').onclick = send;
$('stop').onclick = () => window.grg.stop();
input.addEventListener('input', updateCmdHint);
input.addEventListener('input', updateFileHint);
input.addEventListener('keydown', (e) => {
    const fbox = document.getElementById('file-hint');
    const fOpen = fbox && fbox.style.display === 'block';
    if (fOpen && (e.key === 'Tab' || e.key === 'Enter')) {
        e.preventDefault();
        const sel = fbox.querySelector('.cmd-item.sel') || fbox.querySelector('.cmd-item');
        if (sel) completeFile(sel.getAttribute('data-f'));
        return;
    }
    if (e.key === 'Escape' && fOpen) { fbox.style.display = 'none'; return; }
    const box = document.getElementById('cmd-hint');
    const hintOpen = box && box.style.display === 'block';
    if (hintOpen && (e.key === 'Tab' || (e.key === 'Enter' && /^\/[a-zA-Z0-9_-]*$/.test(input.value)))) {
        e.preventDefault();
        const sel = box.querySelector('.cmd-item.sel') || box.querySelector('.cmd-item');
        if (sel) { input.value = '/' + sel.getAttribute('data-cmd') + ' '; box.style.display = 'none'; autoSize(); }
        return;
    }
    if (e.key === 'Escape' && hintOpen) { box.style.display = 'none'; return; }
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
});
input.addEventListener('input', autoSize);
$('new-btn').onclick = newSession;
$('folder').onclick = async () => { const s = await window.grg.pickFolder(); setFolder(s.projectDir); if (curSession()) { curSession().folder = s.projectDir; saveSessions(); renderSessions(); } };

// approval mode (Ask for approval / Auto-run)
let approveAuto = false;
function setApproveMode(auto) {
    approveAuto = auto;
    window.grg.setApproveMode(auto);
    const b = $('mode-btn'), l = $('mode-label'), ico = $('mode-ico');
    b.classList.toggle('auto', auto);
    l.textContent = auto ? 'Auto-run' : 'Ask for approval';
    ico.innerHTML = auto ? '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>' : '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>';
    try { localStorage.setItem('grgcode-auto', auto ? '1' : '0'); } catch (e) {}
}
$('mode-btn').onclick = () => setApproveMode(!approveAuto);
try { if (localStorage.getItem('grgcode-auto') === '1') setApproveMode(true); } catch (e) {}

// ─────────────────── Specialist agents (ported from grg-ai.com) ───────────────────
// Pick a specialist; it layers its expertise onto Grg Code's engineering workflow.
// PRIVATE agents redact your typed sensitive data (emails/IDs/IBANs/cards/secrets)
// locally before it leaves the machine, and restore it in the reply. File contents are
// NEVER redacted (that would break code). Agent runs cost more credits (heavier workload).
var _grgAgent = false;
var _piiMap = { o2p: {}, p2o: {} };
var _piiCount = {};
function _resetPII() { _piiMap = { o2p: {}, p2o: {} }; _piiCount = {}; }
var _PII_PATTERNS = [
    ['SECRET', '(?:sk-[A-Za-z0-9]{16,}|sk_(?:live|test)_[A-Za-z0-9]{10,}|rk_(?:live|test)_[A-Za-z0-9]{10,}|gsk_[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_\\-]{20,}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}|whsec_[A-Za-z0-9]{10,})'],
    ['EMAIL', '[A-Za-z0-9._%+\\-]+@[A-Za-z0-9.\\-]+\\.[A-Za-z]{2,}'],
    ['IBAN', '[A-Z]{2}\\d{2}(?:[ ]?[A-Z0-9]{3,4}){3,7}'],
    ['CARD', '(?:\\d[ \\-]?){14,16}\\d'],
    ['CNP', '[1-8]\\d{12}'],
    ['PHONE', '(?:\\+?\\d{1,3}[ .\\-]?)?07\\d{2}[ .\\-]?\\d{3}[ .\\-]?\\d{3}|\\+\\d{10,14}']
];
function _piiRedact(text) {
    if (!text || !_grgAgent) return text;
    var out = String(text);
    for (var k = 0; k < _PII_PATTERNS.length; k++) {
        var type = _PII_PATTERNS[k][0];
        var re = new RegExp(_PII_PATTERNS[k][1], 'g');
        out = out.replace(re, function (m) {
            if (_piiMap.o2p[m]) return _piiMap.o2p[m];
            _piiCount[type] = (_piiCount[type] || 0) + 1;
            var ph = '[' + type + '_' + _piiCount[type] + ']';
            _piiMap.o2p[m] = ph; _piiMap.p2o[ph] = m;
            return ph;
        });
    }
    return out;
}
function _piiRestore(text) {
    if (!text || !_grgAgent) return text;
    return String(text).replace(/\[[A-Z]+_\d+\]/g, function (ph) { return _piiMap.p2o[ph] != null ? _piiMap.p2o[ph] : ph; });
}
var _AGENTS = [
    // LEGAL
    { id:'law-litig',  cat:'Legal',    name:'Litigation Lawyer',   desc:'Disputes, pleadings, strategy', privacy:true,
      prompt:'You are a senior litigation lawyer. Analyze disputes, draft pleadings and legal arguments, assess risk and procedure, and cite the relevant statutes/case-law structure. Be precise, hedge where the law is uncertain, and flag when a licensed local lawyer is required.' },
    { id:'law-contract', cat:'Legal',  name:'Contracts Lawyer',    desc:'Draft & review contracts', privacy:true,
      prompt:'You are a senior contracts lawyer. Draft, review and red-line contracts clause by clause, explain risky terms in plain language, suggest fallback wording, and keep numbering/clause structure. Note jurisdiction-specific caveats.' },
    { id:'law-gdpr',   cat:'Legal',    name:'GDPR / Privacy Auditor', desc:'Data-protection compliance', privacy:true,
      prompt:'You are a GDPR and data-protection auditor. Assess processing activities against GDPR principles, lawful bases, DPIAs, data-subject rights, retention and transfers; produce actionable, prioritized compliance findings with article references.' },
    { id:'law-labor',  cat:'Legal',    name:'Employment Lawyer',   desc:'Labor law & HR', privacy:true,
      prompt:'You are an employment/labor lawyer. Advise on contracts, dismissals, working time, discrimination and HR policy, balancing employer and employee perspectives, with clear procedure and risk flags.' },
    { id:'law-ip',     cat:'Legal',    name:'IP Lawyer',           desc:'Trademarks, patents, copyright', privacy:true,
      prompt:'You are an intellectual-property lawyer. Advise on trademarks, patents, copyright and licensing, infringement risk and filing strategy, with clear next steps.' },
    // DEVELOPMENT
    { id:'dev-arch',   cat:'Development', name:'Senior Architect',  desc:'System & app architecture', privacy:false,
      prompt:'You are a principal software architect. Design robust, scalable systems; weigh trade-offs explicitly; produce clean folder structures, data models and sequence of steps; prefer boring, proven tech. Write production-quality code.' },
    { id:'dev-react',  cat:'Development', name:'React / Node Engineer', desc:'Full-stack web', privacy:false,
      prompt:'You are a senior React/Node full-stack engineer. Write modern, typed, accessible, production-ready code (Next.js/Vite, Tailwind, clean APIs), explain decisions briefly, and include error handling.' },
    { id:'dev-python', cat:'Development', name:'Python / Data Engineer', desc:'Backend, data, scripting', privacy:false,
      prompt:'You are a senior Python engineer. Write clean, tested, efficient Python (FastAPI, pandas, async), explain complexity, and handle edge cases and errors explicitly.' },
    { id:'dev-devops', cat:'Development', name:'DevOps / Cloud Engineer', desc:'CI/CD, Docker, cloud', privacy:false,
      prompt:'You are a senior DevOps/cloud engineer. Design CI/CD, containers, IaC and observability; give exact, copy-pasteable configs; call out security and cost.' },
    { id:'dev-mobile', cat:'Development', name:'Mobile Engineer',   desc:'iOS / Android / RN', privacy:false,
      prompt:'You are a senior mobile engineer (SwiftUI, Jetpack Compose, React Native, Expo). Write idiomatic, performant mobile code and cover store-submission and platform specifics.' },
    { id:'dev-db',     cat:'Development', name:'Database Architect', desc:'SQL, schemas, performance', privacy:false,
      prompt:'You are a database architect. Design normalized schemas, write correct SQL, tune queries and indexes, and advise on Postgres/MySQL/Mongo/Redis trade-offs.' },
    { id:'dev-review', cat:'Development', name:'Code Reviewer',     desc:'Bugs, quality, security', privacy:false,
      prompt:'You are a meticulous senior code reviewer. Find real bugs, security issues, and simplifications; give concrete, prioritized fixes with code; be direct but constructive.' },
    { id:'dev-embed',  cat:'Development', name:'Embedded / IoT Engineer', desc:'Arduino, ESP32, robotics', privacy:false,
      prompt:'You are an embedded/IoT and robotics engineer. Write correct firmware (Arduino, ESP32, RP2040, MicroPython), explain wiring/timing/power, and cover motors, sensors, PID and protocols.' },
    // SECURITY
    { id:'sec-pentest', cat:'Security', name:'Security / Pentest', desc:'Appsec, threat modeling', privacy:true,
      prompt:'You are an application-security engineer (authorized testing only). Threat-model systems, find OWASP-class vulnerabilities, explain exploitation at a conceptual level and give concrete remediations. Refuse clearly malicious, unauthorized requests.' },
    { id:'sec-compliance', cat:'Security', name:'Compliance (ISO/SOC2)', desc:'Security frameworks & audits', privacy:true,
      prompt:'You are a security-compliance consultant. Map controls to ISO 27001 / SOC 2 / NIST, draft policies, and produce audit-ready, prioritized gap analyses.' },
    // BUSINESS
    { id:'biz-analyst', cat:'Business', name:'Business Analyst',    desc:'Requirements, process, data', privacy:false,
      prompt:'You are a senior business analyst. Clarify requirements, model processes, analyze data and trade-offs, and produce clear, structured recommendations for decisions.' },
    { id:'biz-market',  cat:'Business', name:'Marketing Strategist', desc:'Growth, positioning, copy', privacy:false,
      prompt:'You are a marketing strategist. Craft positioning, growth and content strategy with concrete, measurable actions and channels; be specific, not generic.' },
    { id:'biz-finance', cat:'Business', name:'Financial Analyst',   desc:'Models, metrics, unit economics', privacy:false,
      prompt:'You are a financial analyst. Build models, analyze metrics and unit economics, and explain assumptions and sensitivities clearly. You are not a licensed financial advisor — add that caveat for personal-investment questions.' },
    { id:'biz-startup', cat:'Business', name:'Startup Advisor',     desc:'Product, GTM, fundraising', privacy:false,
      prompt:'You are a seasoned startup advisor. Pressure-test ideas, product, go-to-market and fundraising; be honest about weaknesses and give prioritized, practical next steps.' },
    // WRITING
    { id:'wr-tech',    cat:'Writing',  name:'Technical Writer',     desc:'Docs, guides, specs', privacy:false,
      prompt:'You are a technical writer. Produce clear, well-structured docs, READMEs, API references and guides with correct Markdown, examples and consistent terminology.' },
    { id:'wr-copy',    cat:'Writing',  name:'Copywriter',          desc:'Landing pages, ads, emails', privacy:false,
      prompt:'You are a conversion copywriter. Write crisp, persuasive copy (headlines, landing pages, ads, emails) matched to the audience and offer; give a few variations.' },
    { id:'wr-academic', cat:'Writing', name:'Academic Editor',      desc:'Papers, citations, clarity', privacy:false,
      prompt:'You are an academic editor. Improve clarity, structure, argument and citation style (APA/IEEE/etc.) while preserving the author\'s meaning; flag unsupported claims.' },
    // DATA / AI
    { id:'ai-ml',      cat:'Data & AI', name:'ML / AI Engineer',    desc:'LLMs, RAG, pipelines', privacy:false,
      prompt:'You are an ML/AI engineer. Design and debug LLM apps, RAG, embeddings, fine-tuning and data pipelines; give concrete, runnable code and evaluation advice.' },
    { id:'ai-data',    cat:'Data & AI', name:'Data Scientist',      desc:'Analysis, stats, viz', privacy:false,
      prompt:'You are a data scientist. Analyze data rigorously, pick correct statistics and visualizations, explain findings plainly, and avoid over-claiming from the data.' },
    // OTHER
    { id:'gen-research', cat:'Other',  name:'Research Assistant',   desc:'Deep, structured research', privacy:false,
      prompt:'You are a thorough research assistant. Break questions down, reason step by step, compare sources and options, and present balanced, well-structured, cited conclusions.' },
    { id:'gen-translate', cat:'Other', name:'Translator / Localizer', desc:'Natural translation & tone', privacy:true,
      prompt:'You are a professional translator and localizer. Translate naturally (not literally), preserve tone and formatting, and keep any [REDACTED] placeholders untouched.' }
];
var _AGENT_CATS = ['Legal','Development','Security','Business','Writing','Data & AI','Other'];
var _AGENT_ICONS = {
    'Legal':       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3v18"/><path d="M5 7h14"/><path d="M7 7l-3 6a3 3 0 0 0 6 0z"/><path d="M17 7l-3 6a3 3 0 0 0 6 0z"/><path d="M8 21h8"/></svg>',
    'Development': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    'Security':    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    'Business':    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><line x1="3" y1="20" x2="21" y2="20"/><rect x="5" y="11" width="3" height="7"/><rect x="10.5" y="6" width="3" height="12"/><rect x="16" y="13" width="3" height="5"/></svg>',
    'Writing':     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>',
    'Data & AI':   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="7" y="7" width="10" height="10" rx="1"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/></svg>',
    'Other':       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l2.1 5.4L20 9.3l-4 3.6L17 19l-5-2.8L7 19l1-6.1-4-3.6 5.9-.9z"/></svg>'
};
function _agentIcon(cat) { return _AGENT_ICONS[cat] || _AGENT_ICONS['Other']; }
var _PRIV_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="10" height="10" style="vertical-align:-1px"><rect x="4" y="11" width="16" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>';
var _EDIT_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4z"/></svg>';
var _customAgents = [];
try { _customAgents = JSON.parse(localStorage.getItem('grgcode_custom_agents') || '[]') || []; } catch (e) { _customAgents = []; }
function _allAgents() { return _customAgents.concat(_AGENTS); }
function _saveCustomAgents() { try { localStorage.setItem('grgcode_custom_agents', JSON.stringify(_customAgents)); } catch (e) {} }
var _activeAgent = null;
try { var _sa = localStorage.getItem('grgcode_active_agent'); if (_sa) { var _all0 = _allAgents(); for (var _ai=0; _ai<_all0.length; _ai++) if (_all0[_ai].id === _sa) _activeAgent = _all0[_ai]; } } catch (e) {}
_grgAgent = !!(_activeAgent && _activeAgent.privacy);
// Specialist agents are a PAID feature (GrgPro / GrgUltra). Free & signed-out can't use them.
function _agentsAllowed() { try { return !!(_user && _account && (_account.plan === 'pro' || _account.plan === 'ultra')); } catch (e) { return false; } }
function _agentUpsell() { try { _gcToast('Specialist agents are a GrgPro feature — upgrade to use them.'); } catch (e) {} try { openBilling(); } catch (e) {} }
function _pushAgentToMain() { try { var ok = _agentsAllowed() && _activeAgent; window.grg.setAgent(ok ? { id: _activeAgent.id, name: _activeAgent.name, prompt: _activeAgent.prompt, privacy: !!_activeAgent.privacy } : null); } catch (e) {} }
// After the plan is known (or on sign-out), drop a leftover agent the user may no longer be entitled to.
function _reconcileAgent() { try { if (_activeAgent && !_agentsAllowed()) { _activeAgent = null; _grgAgent = false; try { localStorage.removeItem('grgcode_active_agent'); } catch (e) {} } _pushAgentToMain(); if (typeof updateAgentUI === 'function') updateAgentUI(); } catch (e) {} }
function selectAgent(id) {
    if (id && !_agentsAllowed()) { closeAgentPicker(); _agentUpsell(); return; }
    var a = null, all = _allAgents();
    for (var i = 0; i < all.length; i++) if (all[i].id === id) a = all[i];
    _activeAgent = a;
    _grgAgent = !!(a && a.privacy);
    _resetPII();
    try { if (a) localStorage.setItem('grgcode_active_agent', a.id); else localStorage.removeItem('grgcode_active_agent'); } catch (e) {}
    _pushAgentToMain();
    updateAgentUI();
    closeAgentPicker();
}
function clearAgent() { selectAgent(null); }
function _agentRow(a, isCustom) {
    var active = (_activeAgent && _activeAgent.id === a.id) ? ' active' : '';
    var tools = isCustom ? '<span class="agent-tools">'
        + '<span class="agent-tool" onclick="event.stopPropagation();editCustomAgent(\'' + a.id + '\')" title="Edit">' + _EDIT_SVG + '</span>'
        + '<span class="agent-tool" onclick="event.stopPropagation();deleteCustomAgent(\'' + a.id + '\')" title="Delete">✕</span></span>' : '';
    return '<button class="agent-item' + active + '" onclick="selectAgent(\'' + a.id + '\')">'
         + '<span class="agent-ico">' + _agentIcon(a.cat) + '</span>'
         + '<span class="agent-meta"><span class="agent-name">' + esc(a.name) + (a.privacy ? ' <span class="agent-priv">' + _PRIV_SVG + ' PRIVATE</span>' : '') + '</span>'
         + '<span class="agent-desc">' + esc(a.desc || '') + '</span></span>' + tools + '</button>';
}
function renderAgentList(q) {
    q = (q || '').toLowerCase().trim();
    var list = document.getElementById('agent-list'); if (!list) return;
    var html = '<button class="agent-create" onclick="openCreateAgent()"><span class="ac-plus">+</span> Create your own agent</button>';
    var mine = _customAgents.filter(function (a) { return !q || (a.name + ' ' + (a.desc || '') + ' ' + a.cat).toLowerCase().indexOf(q) !== -1; });
    if (mine.length) {
        html += '<div class="agent-cat-head">Your Agents</div>';
        mine.forEach(function (a) { html += _agentRow(a, true); });
    }
    for (var c = 0; c < _AGENT_CATS.length; c++) {
        var cat = _AGENT_CATS[c];
        var items = _AGENTS.filter(function (a) { return a.cat === cat && (!q || (a.name + ' ' + a.desc + ' ' + a.cat).toLowerCase().indexOf(q) !== -1); });
        if (!items.length) continue;
        html += '<div class="agent-cat-head">' + cat + '</div>';
        items.forEach(function (a) { html += _agentRow(a, false); });
    }
    list.innerHTML = html;
}
var _editingAgentId = null;
function openCreateAgent(id) {
    if (!_agentsAllowed()) { _agentUpsell(); return; }
    _editingAgentId = id || null;
    var a = null;
    if (id) { for (var i = 0; i < _customAgents.length; i++) if (_customAgents[i].id === id) a = _customAgents[i]; }
    document.getElementById('ca-title').textContent = a ? 'Edit agent' : 'Create your own agent';
    document.getElementById('ca-name').value = a ? a.name : '';
    document.getElementById('ca-desc').value = a ? (a.desc || '') : '';
    document.getElementById('ca-prompt').value = a ? a.prompt : '';
    document.getElementById('ca-priv').checked = a ? !!a.privacy : false;
    var sel = document.getElementById('ca-cat'); if (sel) sel.value = a ? a.cat : 'Other';
    document.getElementById('ca-err').textContent = '';
    document.getElementById('agent-create-ov').classList.add('visible');
    setTimeout(function () { document.getElementById('ca-name').focus(); }, 50);
}
function closeCreateAgent() { document.getElementById('agent-create-ov').classList.remove('visible'); }
function saveCustomAgent() {
    var name = document.getElementById('ca-name').value.trim();
    var desc = document.getElementById('ca-desc').value.trim();
    var prompt = document.getElementById('ca-prompt').value.trim();
    var cat = document.getElementById('ca-cat').value;
    var priv = document.getElementById('ca-priv').checked;
    var err = document.getElementById('ca-err');
    if (!name) { err.textContent = 'Please give your agent a name.'; return; }
    if (prompt.length < 15) { err.textContent = 'Write a longer instruction / system prompt (what the agent does).'; return; }
    if (_editingAgentId) {
        for (var i = 0; i < _customAgents.length; i++) if (_customAgents[i].id === _editingAgentId) {
            _customAgents[i] = { id: _editingAgentId, cat: cat, name: name, desc: desc, prompt: prompt, privacy: priv, custom: true };
            if (_activeAgent && _activeAgent.id === _editingAgentId) { _activeAgent = _customAgents[i]; _grgAgent = !!priv; _pushAgentToMain(); }
        }
    } else {
        _customAgents.unshift({ id: 'custom-' + Date.now(), cat: cat, name: name, desc: desc, prompt: prompt, privacy: priv, custom: true });
    }
    _saveCustomAgents();
    closeCreateAgent();
    renderAgentList(document.getElementById('agent-search') ? document.getElementById('agent-search').value : '');
    updateAgentUI();
}
function editCustomAgent(id) { openCreateAgent(id); }
function deleteCustomAgent(id) {
    if (!confirm('Delete this agent?')) return;
    _customAgents = _customAgents.filter(function (a) { return a.id !== id; });
    _saveCustomAgents();
    if (_activeAgent && _activeAgent.id === id) clearAgent();
    renderAgentList(document.getElementById('agent-search') ? document.getElementById('agent-search').value : '');
}
function openAgentPicker() {
    if (!_agentsAllowed()) { _agentUpsell(); return; }
    renderAgentList('');
    var ov = document.getElementById('agent-ov'); if (ov) ov.classList.add('visible');
    var s = document.getElementById('agent-search'); if (s) { s.value = ''; setTimeout(function () { s.focus(); }, 50); }
}
function closeAgentPicker() { var ov = document.getElementById('agent-ov'); if (ov) ov.classList.remove('visible'); }
function updateAgentUI() {
    var pill = document.getElementById('agent-pill');
    var label = document.getElementById('agent-label');
    var banner = document.getElementById('agent-banner');
    if (_activeAgent) {
        if (label) label.textContent = _activeAgent.name;
        if (pill) pill.classList.add('active');
        if (banner) { banner.className = 'agent-banner on'; banner.innerHTML = '<span class="ab-ico">' + _agentIcon(_activeAgent.cat) + '</span> <b>' + esc(_activeAgent.name) + '</b> active · uses more credits' + (_activeAgent.privacy ? ' · ' + _PRIV_SVG + ' your typed sensitive data is redacted before it leaves your device' : '') + ' <span class="ab-x" onclick="clearAgent()" title="Exit agent">✕</span>'; }
    } else {
        if (label) label.textContent = 'Agents';
        if (pill) pill.classList.remove('active');
        if (banner) banner.className = 'agent-banner';
    }
}
_pushAgentToMain();
updateAgentUI();

// model selector — mirrors the models on grg-ai.com, grouped by family.
// Groq models run as full agents (tools). Premium (OpenRouter) need credits.
// Mirrors the full model list on grg-ai.com (image-only models excluded — the agent doesn't generate images).
const AGENT_MODELS = [
    // Grg (Groq, free — full tool use)
    { id: 'auto', name: 'AutoGrg', family: 'Grg', tag: 'Auto', free: true },
    { id: 'openai/gpt-oss-120b', name: 'Grg Code', family: 'Grg', tag: 'Flagship', free: true },
    { id: 'poolside/laguna-s-2.1:free', name: 'Grg Coder', family: 'Grg', tag: 'Code', free: true },
    { id: 'openai/gpt-oss-20b', name: 'Grg Fast', family: 'Grg', tag: 'Fast', free: true },
    // Anthropic
    { id: 'anthropic/claude-sonnet-5', name: 'Claude Sonnet 5', family: 'Anthropic', tag: 'Pro', free: false },
    { id: 'anthropic/claude-opus-4.8', name: 'Claude Opus 4.8', family: 'Anthropic', tag: 'Pro', free: false },
    { id: 'anthropic/claude-opus-4.6', name: 'Claude Opus 4.6', family: 'Anthropic', tag: 'Pro', free: false },
    { id: 'anthropic/claude-fable', name: 'Claude Fable', family: 'Anthropic', tag: 'Fast', free: false },
    // OpenAI
    { id: 'openai/gpt-5.6', name: 'GPT-5.6', family: 'OpenAI', tag: 'Pro', free: false },
    { id: 'openai/gpt-5.5', name: 'GPT-5.5', family: 'OpenAI', tag: 'Pro', free: false },
    { id: 'openai/gpt-5.2', name: 'GPT-5.2', family: 'OpenAI', tag: 'Pro', free: false },
    { id: 'openai/gpt-5.1-codex', name: 'GPT-5.1 Codex', family: 'OpenAI', tag: 'Code', free: false },
    { id: 'openai/gpt-4o', name: 'GPT-4o', family: 'OpenAI', tag: 'Fast', free: false },
    // Meta
    { id: 'meta-llama/llama-4-maverick', name: 'Llama 4 Maverick', family: 'Meta', tag: 'Pro', free: false },
    { id: 'meta-llama/llama-4-scout', name: 'Llama 4 Scout', family: 'Meta', tag: 'Fast', free: false },
    // Qwen
    { id: 'qwen/qwen3.8-27b', name: 'Qwen3.8 27B', family: 'Qwen', tag: 'Reason', free: true },
    { id: 'qwen/qwen3-coder', name: 'Qwen3 Coder', family: 'Qwen', tag: 'Code', free: false },
    { id: 'qwen/qwen3-vl', name: 'Qwen3 VL', family: 'Qwen', tag: 'Vision', free: false },
    // DeepSeek
    { id: 'deepseek/deepseek-v4-flash-0731:free', name: 'DeepSeek V4 Flash', family: 'DeepSeek', tag: 'Fast', free: true },
    { id: 'deepseek/deepseek-r1', name: 'DeepSeek R1', family: 'DeepSeek', tag: 'Reason', free: false },
    { id: 'deepseek/deepseek-v4', name: 'DeepSeek V4', family: 'DeepSeek', tag: 'Smart', free: false },
    // Google
    { id: 'google/gemma-4-31b-it:free', name: 'Gemma 4 31B', family: 'Google', tag: 'Vision', free: true },
    { id: 'google/gemini-3.1-pro-preview', name: 'Gemini 3 Pro', family: 'Google', tag: 'Pro', free: false },
    { id: 'google/gemini-2.5-pro', name: 'Gemini 2.5 Pro', family: 'Google', tag: 'Pro', free: false },
    // Nvidia
    { id: 'nvidia/nemotron-3-ultra-550b-a55b:free', name: 'Nemotron Ultra 550B', family: 'Nvidia', tag: '550B', free: true },
    { id: 'nvidia/nemotron-3.5-lightning:free', name: 'Nemotron 3.5 Lightning', family: 'Nvidia', tag: 'Reason', free: true },
    // xAI
    { id: 'x-ai/grok-4.6', name: 'Grok 4.6', family: 'xAI', tag: 'Pro', free: false },
    { id: 'x-ai/grok-4', name: 'Grok 4', family: 'xAI', tag: 'Pro', free: false },
    { id: 'x-ai/grok-4.1', name: 'Grok 4.1', family: 'xAI', tag: 'Pro', free: false },
    // Moonshot
    { id: 'moonshotai/kimi-k3', name: 'Kimi K3', family: 'Moonshot', tag: 'Pro', free: false },
    { id: 'moonshotai/kimi-k2.7-code', name: 'Kimi K2.7 Code', family: 'Moonshot', tag: 'Code', free: false },
    { id: 'moonshotai/kimi-k2.6', name: 'Kimi K2.6', family: 'Moonshot', tag: 'Pro', free: false },
    // Mistral
    { id: 'mistralai/codestral-2508', name: 'Codestral', family: 'Mistral', tag: 'Code', free: false },
    { id: 'mistralai/mistral-large-2', name: 'Mistral Large 2', family: 'Mistral', tag: 'Pro', free: false },
    // GLM
    { id: 'z-ai/glm-5.2:free', name: 'GLM 5.2', family: 'GLM', tag: 'Smart', free: true },
    { id: 'z-ai/glm-5.3', name: 'GLM 5.3', family: 'GLM', tag: 'Pro', free: false },
    // inclusionAI
    { id: 'inclusionai/ling-3.0-flash-vl:free', name: 'Ling 3.0 Flash VL', family: 'inclusionAI', tag: 'Vision', free: true }
];
const FAMILY_ORDER = ['Grg', 'Anthropic', 'OpenAI', 'Google'];
// Only these show in the picker. AutoGrg is the universal default; Claude / GPT / Gemini
// stay individually selectable. Every other model above is still valid and routable — it
// lives inside the AutoGrg pool (the backend classifies the task, scans availability and
// picks the best affordable model) instead of cluttering the dropdown.
const MENU_MODELS = ['auto','anthropic/claude-opus-4.8','anthropic/claude-sonnet-5','anthropic/claude-fable','openai/gpt-5.6','openai/gpt-5.5','openai/gpt-4o','openai/gpt-5.1-codex','google/gemini-3.1-pro-preview','google/gemini-2.5-pro'];
let curModel = 'auto';
function renderModelMenu() {
    const menu = $('cmodel-menu');
    const ck = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="14" height="14"><polyline points="20 6 9 17 4 12"/></svg>';
    const lk = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>';
    let html = '';
    FAMILY_ORDER.forEach(fam => {
        const items = AGENT_MODELS.filter(m => m.family === fam && MENU_MODELS.indexOf(m.id) >= 0);
        if (!items.length) return;
        html += '<div class="cmodel-fam">' + fam + '</div>';
        items.forEach(m => {
            html += `<div class="cmodel-item ${m.free ? '' : 'locked'}" data-id="${m.id}"><span class="mck">${m.id === curModel ? ck : ''}</span><span class="mnm">${m.name}</span><span class="mtag">${m.tag}</span>${m.free ? '' : '<span class="mlock">' + lk + '</span>'}</div>`;
        });
    });
    menu.innerHTML = html;
    menu.querySelectorAll('.cmodel-item').forEach(el => el.onclick = () => selectModel(el.getAttribute('data-id')));
}
function selectModel(id) {
    const m = AGENT_MODELS.find(x => x.id === id); if (!m) return;
    curModel = id; window.grg.setModel(id);
    $('cmodel-label').textContent = m.name;
    try { localStorage.setItem('grgcode-model', id); } catch (e) {}
    $('cmodel-menu').classList.remove('open'); renderModelMenu();
}
$('cmodel-btn').onclick = (e) => { e.stopPropagation(); $('cmodel-menu').classList.toggle('open'); };
document.addEventListener('click', (e) => { if (!e.target.closest('#cmodel-dd')) $('cmodel-menu').classList.remove('open'); });
try { const sm = localStorage.getItem('grgcode-model'); if (sm && AGENT_MODELS.find(x => x.id === sm) && MENU_MODELS.indexOf(sm) >= 0) selectModel(sm); else selectModel('auto'); } catch (e) { renderModelMenu(); }

// ─── auth (Grg AI account via Firebase) ───
let _authMode = 'in', _user = null;
window.openAuth = () => { $('auth-ov').classList.add('show'); $('au-err').textContent = ''; setTimeout(() => $('au-email').focus(), 60); };
window.closeAuth = () => $('auth-ov').classList.remove('show');
window.authTab = (m) => { _authMode = m; $('tab-in').classList.toggle('active', m === 'in'); $('tab-up').classList.toggle('active', m === 'up'); $('au-submit').textContent = m === 'in' ? 'Sign In' : 'Create account'; };
window.authSubmit = async () => {
    if (!window._fb) { $('au-err').textContent = 'Auth still loading…'; return; }
    const email = $('au-email').value.trim(), pass = $('au-pass').value;
    if (!email || !pass) { $('au-err').textContent = 'Enter email and password'; return; }
    $('au-err').textContent = '';
    try {
        if (_authMode === 'in') await window._fb.signInWithEmailAndPassword(window._fb.auth, email, pass);
        else await window._fb.createUserWithEmailAndPassword(window._fb.auth, email, pass);
        closeAuth();
    } catch (e) { $('au-err').textContent = (e.message || 'Failed').replace('Firebase:', '').replace(/\(auth.*\)\.?/, '').trim(); }
};
window.doSignOut = (e) => { if (e) e.stopPropagation(); if (window._fb) window._fb.signOut(window._fb.auth); };
function renderAcct() {
    const box = $('acct-box');
    if (_user) {
        const name = _user.displayName || (_user.email || '').split('@')[0] || 'User';
        const credits = _account ? bFmtTok(_account.credits_balance || 0) + ' credits' : 'View credits';
        box.innerHTML = `<div class="acct"><div class="av">${(name[0] || 'U').toUpperCase()}</div><div class="atx"><b>${esc(name)}</b><small>${esc(_user.email || '')}</small></div><button class="sout" title="Sign out"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg></button></div><div class="bill-pill" id="bill-pill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5h5M9 12h6M9.5 14.5h5"/></svg> ${credits} · Top up</div>`;
        box.querySelector('.acct').onclick = openBilling; box.querySelector('.sout').onclick = doSignOut;
        const pill = box.querySelector('#bill-pill'); if (pill) pill.onclick = openBilling;
    } else {
        box.innerHTML = `<div class="acct" id="signin-cta"><div class="ai"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg></div><div class="atx"><b>Sign in</b><small>Use your Grg AI account</small></div></div>`;
        box.querySelector('#signin-cta').onclick = openAuth;
    }
}
function initAuth() {
    if (!window._fb) return;
    window._fb.onAuthStateChanged(window._fb.auth, (u) => { _user = u; _account = null; try { window.grg.setUid(u ? u.uid : null); } catch (e) {} renderAcct(); if (u) loadAccount(); else { try { _reconcileAgent(); } catch (e) {} } });
}

// ─── Billing / credits (mirrors the website; card entry happens in the browser) ───
let _account = null;
function bFmtTok(n) { n = Number(n) || 0; if (n >= 1e6) return (n / 1e6).toFixed(2).replace(/\.?0+$/, '') + 'M'; if (n >= 1000) return (n / 1000).toFixed(1).replace(/\.0$/, '') + 'k'; return String(n); }
async function loadAccount() {
    if (!_user) { _account = null; return; }
    try { _account = await window.grg.billAccount(_user.uid); } catch (e) { _account = null; }
    renderBilling(); renderAcct();
    try { _reconcileAgent(); } catch (e) {}   // agents are paid-only; drop/restore based on plan
}
function openBilling() { if (!_user) { openAuth(); return; } $('bill-ov').classList.add('show'); loadAccount(); }
function closeBilling() { $('bill-ov').classList.remove('show'); }
window.openBilling = openBilling; window.closeBilling = closeBilling;
function renderBilling() {
    if (!_user || !$('bill-acct')) return;
    const a = _account || {};
    const name = _user.displayName || (_user.email || '').split('@')[0] || 'User';
    $('bill-acct').innerHTML = '<div class="av">' + (name[0] || 'U').toUpperCase() + '</div><div class="bx"><b>' + esc(name) + '</b><small>' + esc(_user.email || '') + '</small></div>';
    const isPro = a.plan === 'pro';
    $('bill-plan').innerHTML = 'Plan: <span class="badge">' + (isPro ? 'GRG PRO' : 'FREE') + '</span>';
    $('bill-upgrade').style.display = isPro ? 'none' : 'block';
    $('bill-manage').style.display = isPro ? 'block' : 'none';
    $('bc-bal').textContent = bFmtTok(a.credits_balance || 0) + ' credits';
    let html = '';
    if (isPro) {
        const tot = a.plan_credits_total || 0, left = a.plan_credits || 0, used = Math.max(0, tot - left), pct = tot ? Math.min(100, Math.round(used / tot * 100)) : 0;
        html += '<div class="bc-alloc"><div class="pa-top"><span>Plan allowance</span><span>' + bFmtTok(used) + ' / ' + bFmtTok(tot) + ' credits</span></div><div class="pa-bar"><div class="pa-fill" style="width:' + pct + '%"></div></div><div class="pa-note">' + (left > 0 ? bFmtTok(left) + ' plan credits left this month' : 'Plan allowance used up — using top-up credits') + '</div></div>';
    }
    const um = a.usage_models || {}; const ids = Object.keys(um).sort((x, y) => (um[y].tokens || 0) - (um[x].tokens || 0));
    if (ids.length) {
        html += '<div style="margin-top:8px">';
        ids.slice(0, 6).forEach(id => { html += '<div style="display:flex;justify-content:space-between;padding:3px 0;border-top:1px solid var(--border);font-size:12px"><span style="color:var(--text-dim)">' + esc(id.split('/').pop()) + '</span><span style="color:var(--accent-2)">' + bFmtTok(um[id].tokens) + ' tok</span></div>'; });
        html += '</div>';
    } else { html += '<div style="margin-top:8px;font-size:11.5px;color:var(--text-mute)">No premium usage yet.</div>'; }
    $('bc-meta').innerHTML = html;
}
async function _checkout(endpoint, body) {
    if (!_user) { openAuth(); return; }
    try {
        const d = await window.grg.billPost(endpoint, Object.assign({ uid: _user.uid, email: _user.email }, body));
        if (d && d.url) { window.grg.openExternal(d.url); _billWaiting(); }
        else alert((d && (d.detail || d.error)) || 'Could not open checkout. Try again.');
    } catch (e) { alert('Payment error. Try again.'); }
}
function startTopup(eur) { eur = Math.round(Number(eur) * 100) / 100; if (!(eur >= 1 && eur <= 500)) { alert('Enter an amount between €1 and €500'); return; } _checkout('/api/create-topup', { eur }); }
function startTopupCustom() { const el = $('bc-custom-amt'); const v = el ? parseFloat(el.value) : NaN; if (!(v >= 1 && v <= 500)) { alert('Enter an amount between €1 and €500'); if (el) el.focus(); return; } startTopup(v); }
function upgradePlan() { _checkout('/api/create-checkout', { interval: 'monthly' }); }
async function manageSub() {
    if (!_user) return;
    try { const d = await window.grg.billPost('/api/create-portal', { uid: _user.uid }); if (d && d.url) window.grg.openExternal(d.url); else alert('No subscription to manage.'); } catch (e) { alert('Error.'); }
}
window.startTopup = startTopup; window.startTopupCustom = startTopupCustom; window.upgradePlan = upgradePlan; window.manageSub = manageSub;
// After paying in the browser, poll for the new balance for a while, and on window focus.
let _billPoll = null;
function _billWaiting() { let n = 0; if (_billPoll) clearInterval(_billPoll); _billPoll = setInterval(() => { n++; loadAccount(); if (n > 25) { clearInterval(_billPoll); _billPoll = null; } }, 4000); }
window.addEventListener('focus', () => { if (_user) loadAccount(); });
window.addEventListener('fb-ready', initAuth);

// ─── init ───
renderAcct();
if (window._fb) initAuth();
(async () => {
    const s = await window.grg.getState();
    setFolder(s.projectDir);
    renderSessions();
    if (sessions.length) { loadSession(sessions.sort((a, b) => (b.ts || 0) - (a.ts || 0))[0].id); }
    else newSession();
    input.focus();
})();
