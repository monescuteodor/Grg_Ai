# CSS Advanced Complete Reference


---

# CHAPTER 1: MODERN LAYOUT


## Remarks

CSS has evolved dramatically. Flexbox and Grid replaced float hacks. CSS variables replaced preprocessor variables. Container queries, cascade layers, and :has() selector make CSS more powerful than ever. Modern CSS can do what JavaScript used to be required for.


## Flexbox Deep Dive

```css
/* FLEXBOX: one-dimensional layout (row OR column) */

.container {
    display: flex;
    
    /* Main axis (horizontal for row, vertical for column) */
    flex-direction: row;           /* row | row-reverse | column | column-reverse */
    justify-content: center;       /* flex-start | center | flex-end | space-between | space-around | space-evenly */
    
    /* Cross axis (perpendicular to main) */
    align-items: center;           /* flex-start | center | flex-end | stretch | baseline */
    
    /* Multi-line */
    flex-wrap: wrap;               /* nowrap | wrap | wrap-reverse */
    align-content: space-between;  /* Controls wrapped lines */
    
    gap: 16px;                     /* Space between items (modern, cleaner than margins) */
}

/* FLEX ITEM PROPERTIES */
.item {
    flex: 1;                       /* Shorthand: grow shrink basis */
    /* flex: 1 = flex: 1 1 0%  (grow, shrink, start from 0) */
    /* flex: 0 1 auto = default  (don't grow, can shrink, natural size) */
    
    flex-grow: 1;                  /* How much extra space to take */
    flex-shrink: 0;                /* Don't shrink below basis */
    flex-basis: 300px;             /* Starting size before grow/shrink */
    
    align-self: flex-end;          /* Override align-items for this item */
    order: -1;                     /* Reorder (lower = first) */
}

/* COMMON PATTERNS */

/* Center anything */
.center-everything {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

/* Navbar: logo left, links right */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 24px;
    height: 60px;
}

/* Card grid that wraps */
.card-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
}
.card-grid > * {
    flex: 1 1 300px;  /* Min 300px, grows to fill */
    max-width: 400px;
}

/* Sticky footer */
.page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}
.page > main {
    flex: 1;  /* Main content fills available space */
}
```


## CSS Grid Deep Dive

```css
/* GRID: two-dimensional layout (rows AND columns) */

.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);     /* 3 equal columns */
    grid-template-rows: auto 1fr auto;          /* Header, content, footer */
    gap: 24px;
}

/* Responsive grid WITHOUT media queries! */
.auto-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
}
/* auto-fill: create as many columns as fit
   minmax(280px, 1fr): each column min 280px, max equal share */

/* Named areas */
.page-layout {
    display: grid;
    grid-template-columns: 250px 1fr 200px;
    grid-template-rows: 60px 1fr 50px;
    grid-template-areas:
        "header  header  header"
        "sidebar content aside"
        "footer  footer  footer";
    min-height: 100vh;
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.aside   { grid-area: aside; }
.footer  { grid-area: footer; }

/* Responsive: collapse to single column on mobile */
@media (max-width: 768px) {
    .page-layout {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "content"
            "footer";
    }
    .sidebar, .aside { display: none; }
}

/* Grid item placement */
.item {
    grid-column: 1 / 3;      /* Span columns 1-2 */
    grid-row: 1 / 2;         /* Row 1 */
    grid-column: span 2;      /* Span 2 columns from current */
}

/* Subgrid (CSS Grid Level 2) */
.parent {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
}
.child {
    display: grid;
    grid-template-columns: subgrid;  /* Inherit parent's column tracks */
    grid-column: span 3;
}
```


---

# CHAPTER 2: CSS VARIABLES AND THEMING


## Custom Properties

```css
:root {
    /* Colors */
    --color-primary: #3b82f6;
    --color-primary-dark: #2563eb;
    --color-bg: #0a0a0a;
    --color-text: #d8d8d8;
    --color-border: #2a2a2a;
    --color-surface: #151515;
    
    /* Typography */
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', 'Courier New', monospace;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.25rem;
    --font-size-xl: 1.5rem;
    
    /* Spacing */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    
    /* Borders */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 16px;
    --radius-full: 9999px;
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 250ms ease;
}

/* Dark/Light theme toggle */
[data-theme="light"] {
    --color-bg: #ffffff;
    --color-text: #1a1a1a;
    --color-border: #e5e5e5;
    --color-surface: #f5f5f5;
}

/* Usage */
.card {
    background: var(--color-surface);
    color: var(--color-text);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    font-family: var(--font-sans);
    transition: transform var(--transition-fast);
}
.card:hover {
    transform: translateY(-2px);
}

/* Component-level variable overrides */
.compact-card {
    --space-lg: 12px;  /* Tighter padding just for this component */
}
```


---

# CHAPTER 3: ANIMATIONS AND TRANSITIONS


## Transitions

```css
/* Transition = animate between two states */
.button {
    background: var(--color-primary);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    
    /* Transition specific properties */
    transition: background 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
}
.button:hover {
    background: var(--color-primary-dark);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}
.button:active {
    transform: translateY(0);
}

/* PERFORMANCE: only animate transform and opacity! */
/* These use GPU (compositor layer) → 60fps guaranteed */
/* BAD: transition: width, height, top, left, margin → triggers layout */
/* GOOD: transition: transform, opacity → GPU-accelerated */
```


## Keyframe Animations

```css
/* Fade in + slide up */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
.animate-in {
    animation: fadeInUp 0.4s ease-out forwards;
}

/* Spinner */
@keyframes spin {
    to { transform: rotate(360deg); }
}
.spinner {
    width: 24px;
    height: 24px;
    border: 3px solid var(--color-border);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

/* Pulse */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.loading-skeleton {
    background: var(--color-surface);
    animation: pulse 1.5s ease-in-out infinite;
    border-radius: var(--radius-sm);
}

/* Staggered entrance (each child delays slightly) */
.stagger-in > * {
    opacity: 0;
    animation: fadeInUp 0.4s ease-out forwards;
}
.stagger-in > *:nth-child(1) { animation-delay: 0.0s; }
.stagger-in > *:nth-child(2) { animation-delay: 0.1s; }
.stagger-in > *:nth-child(3) { animation-delay: 0.2s; }
.stagger-in > *:nth-child(4) { animation-delay: 0.3s; }

/* Typing animation */
@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}
@keyframes blink-cursor {
    50% { border-color: transparent; }
}
.typewriter {
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid var(--color-text);
    animation: typing 2s steps(30) forwards,
               blink-cursor 0.8s step-end infinite;
}
```


---

# CHAPTER 4: RESPONSIVE DESIGN


## Media Queries and Fluid Design

```css
/* Mobile-first breakpoints */
/* Default: mobile styles */

/* Tablet (768px+) */
@media (min-width: 768px) {
    .container { max-width: 720px; }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
    .container { max-width: 960px; }
}

/* Large desktop (1280px+) */
@media (min-width: 1280px) {
    .container { max-width: 1200px; }
}

/* Fluid typography (no media queries needed!) */
h1 {
    font-size: clamp(1.5rem, 4vw, 3rem);
    /* min: 1.5rem, preferred: 4% viewport width, max: 3rem */
}

p {
    font-size: clamp(0.875rem, 1.5vw, 1.125rem);
}

/* Fluid spacing */
.section {
    padding: clamp(24px, 5vw, 80px);
}

/* Container queries (CSS 2023+) */
.card-container {
    container-type: inline-size;
}

@container (min-width: 400px) {
    .card {
        display: grid;
        grid-template-columns: 120px 1fr;
    }
}

/* Prefer dark mode from OS */
@media (prefers-color-scheme: dark) {
    :root {
        --color-bg: #0a0a0a;
        --color-text: #d8d8d8;
    }
}

/* Reduced motion (accessibility) */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```


---

# CHAPTER 5: COMMON PITFALLS

```
PITFALL 1: Not using box-sizing: border-box
  width: 200px + padding: 20px = total 240px. Confusing!
  Fix: *, *::before, *::after { box-sizing: border-box; }

PITFALL 2: Animating width/height/top/left
  Triggers layout recalculation → janky 30fps.
  Fix: use transform: translate/scale and opacity only.

PITFALL 3: Using px for everything
  Ignores user font-size preferences (accessibility).
  Fix: rem for font-sizes, em for component spacing, px for borders.

PITFALL 4: z-index wars
  z-index: 99999 to "fix" stacking.
  Fix: create stacking context with isolation: isolate. Use layer system.

PITFALL 5: !important everywhere
  Specificity nightmare, impossible to override.
  Fix: use lower specificity selectors, CSS layers, or cascade order.

PITFALL 6: Not using gap
  Margins on flex/grid children → double spacing on edges.
  Fix: gap: 16px on container (clean, no edge issues).

PITFALL 7: Viewport units without fallback
  100vh on mobile includes browser chrome → overflow.
  Fix: height: 100dvh (dynamic viewport height) or min-height: 100vh.

PITFALL 8: Forgetting overflow hidden/auto
  Content overflows container → horizontal scroll on page.
  Fix: overflow: hidden on containers, overflow: auto for scrollable.
```