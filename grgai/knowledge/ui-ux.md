# UI/UX & modern layouts — best practices

## Visual foundations
- Pick ONE type scale (e.g. 12/14/16/20/24/32/48) and ONE spacing scale (4px steps). Consistency reads as "designed".
- Limit the palette: a background, a foreground/text, one accent, a muted/secondary, a border. Derive states (hover/active) from those.
- Contrast: body text ≥ 4.5:1, large text ≥ 3:1. Never gray-on-gray for important text.
- Whitespace is a feature. Generous padding, clear grouping, one clear primary action per view.

## Landing page structure
1. **Hero**: one-line value prop + subtext + primary CTA (+ secondary). Optional product shot.
2. **Social proof** (logos/testimonials). 3. **Features** (3–6, icon + title + one line). 4. **How it works** (steps). 5. **Pricing**. 6. **FAQ**. 7. **Footer** (nav, legal, socials).
- Above the fold: value prop + CTA must be visible without scrolling.

## Dashboard / app shell
- Left sidebar nav (collapsible) + top bar (search, account) + main content. Or top nav for simpler apps.
- Content: cards/tables with clear headers; KPIs as a row of stat tiles at the top. Empty states with a helpful CTA.
- Keep primary actions top-right of their section; destructive actions need confirmation.

## Components (reusable)
- Build primitives once (Button, Input, Card, Dialog, Badge, Toast) and reuse. Variants via props, not copy-paste.
- Buttons: variants `primary | secondary | ghost | destructive`, sizes `sm | md | lg`, disabled + loading states.
- Forms: label + input + inline error + help text; validate on blur/submit; show a clear success state.

## Responsive & motion
- Mobile-first; collapse multi-column to single column; turn sidebars into a drawer under `md`.
- Tap targets ≥ 44px. Don't hide critical actions behind hover on mobile.
- Motion: 150–250ms ease for hovers/transitions; respect `prefers-reduced-motion`. Subtle > flashy.

## Accessibility
- Semantic HTML, labeled inputs, visible focus rings, keyboard navigable, alt text on images, `aria-live` for async updates.
