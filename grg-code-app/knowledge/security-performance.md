# Security, performance & accessibility

## Web security (OWASP essentials)
- Validate + sanitize all input; **parameterize** DB queries (no SQL injection).
- Escape output to prevent **XSS**; set a Content-Security-Policy. Use httpOnly/Secure/SameSite cookies + CSRF tokens.
- AuthN/AuthZ on every protected route; check ownership, not just login. Rate-limit.
- Keep deps updated (`npm audit`, Dependabot). Never commit secrets; rotate leaked ones.
- HTTPS everywhere; secure headers (HSTS, X-Content-Type-Options). Principle of least privilege.

## Performance (web)
- Ship less JS: code-split, lazy-load, tree-shake. Compress (gzip/brotli). Cache with correct headers.
- Images: modern formats (AVIF/WebP), responsive sizes, lazy loading. Avoid layout shift (set dimensions).
- Measure with Lighthouse / Web Vitals (LCP, CLS, INP). Debounce expensive work. Virtualize long lists.
- Backend: add indexes, avoid N+1, cache hot reads, paginate, use CDNs.

## Accessibility (a11y)
- Semantic HTML; labels for inputs; alt text for images. Keyboard-navigable (focus states, no traps).
- Color contrast >= 4.5:1; respect `prefers-reduced-motion`. ARIA only when semantics are missing.
- Test with keyboard + a screen reader.
