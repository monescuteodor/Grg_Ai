# Browser extensions (Manifest V3)

Works in Chrome/Edge/Brave; Firefox is mostly compatible (uses `browser.*`).

## manifest.json
```json
{
  "manifest_version": 3,
  "name": "My Ext", "version": "1.0.0",
  "action": { "default_popup": "popup.html" },
  "background": { "service_worker": "bg.js" },
  "content_scripts": [{ "matches": ["<all_urls>"], "js": ["content.js"] }],
  "permissions": ["storage", "activeTab", "scripting"]
}
```

## Parts
- **Popup** — small UI (HTML/JS) from the toolbar icon.
- **Background service worker** — events, alarms, message hub (no DOM, can sleep).
- **Content script** — runs in the page, can read/modify the DOM. Talk to background via `chrome.runtime.sendMessage`.
- Storage: `chrome.storage.sync` / `.local`.

## Ship
- Chrome Web Store (one-time $5 dev fee), Firefox AMO, Edge Add-ons. Zip the folder; provide screenshots + privacy policy.
- Least-privilege permissions (reviewers reject over-broad ones). No remote code in MV3.
