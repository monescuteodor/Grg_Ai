# Web Accessibility (a11y) Complete Reference


---

# CHAPTER 1: ACCESSIBILITY FUNDAMENTALS


## Remarks

Accessibility (a11y) means making websites usable by everyone, including people with visual, motor, hearing, or cognitive disabilities. ~15% of the world's population has some form of disability. Good accessibility also improves UX for everyone: keyboard navigation, screen readers, color contrast, and semantic HTML benefit all users.


## Semantic HTML (Foundation)

```html
<!-- BAD: div soup (screen reader sees nothing meaningful) -->
<div class="header">
    <div class="nav">
        <div class="link" onclick="goto('/')">Home</div>
        <div class="link" onclick="goto('/about')">About</div>
    </div>
</div>
<div class="content">
    <div class="title">Welcome</div>
    <div class="text">Hello world</div>
</div>

<!-- GOOD: semantic HTML (screen reader understands structure) -->
<header>
    <nav aria-label="Main navigation">
        <a href="/">Home</a>
        <a href="/about">About</a>
    </nav>
</header>
<main>
    <h1>Welcome</h1>
    <p>Hello world</p>
</main>
<footer>
    <p>© 2026 My App</p>
</footer>

<!-- Semantic elements and their meaning:
  <header>   — page/section header
  <nav>      — navigation links
  <main>     — primary content (only ONE per page)
  <article>  — self-contained content (blog post, comment)
  <section>  — thematic grouping of content
  <aside>    — sidebar, related content
  <footer>   — page/section footer
  <h1>-<h6>  — heading hierarchy (DON'T skip levels!)
  <button>   — clickable action
  <a href>   — navigation link
  <form>     — user input
  <label>    — labels for form inputs
-->
```


## ARIA (Accessible Rich Internet Applications)

```html
<!-- ARIA adds meaning when HTML alone isn't enough -->

<!-- ARIA roles -->
<div role="alert">Error: Invalid email address</div>
<div role="status">Saving...</div>
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
    <h2 id="dialog-title">Confirm Delete</h2>
    <p>Are you sure?</p>
    <button>Yes</button>
    <button>Cancel</button>
</div>

<!-- ARIA labels -->
<button aria-label="Close menu">✕</button>  <!-- Screen reader: "Close menu button" -->
<input aria-label="Search" type="search" placeholder="Search...">
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Footer links">...</nav>  <!-- Distinguishes multiple navs -->

<!-- ARIA states -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" hidden>...</ul>

<button aria-pressed="true">Bold</button>   <!-- Toggle button: on/off -->
<div aria-busy="true">Loading content...</div>
<input aria-invalid="true" aria-describedby="error-msg">
<span id="error-msg">Email must contain @</span>

<!-- Live regions (announce changes to screen readers) -->
<div aria-live="polite">3 results found</div>  <!-- Announced when changed -->
<div aria-live="assertive">Error: Connection lost</div>  <!-- Interrupts immediately -->

<!-- RULE: No ARIA is better than bad ARIA -->
<!-- Use native HTML first: <button> not <div role="button"> -->
<!-- ARIA doesn't add behavior, only meaning! -->
```


## Keyboard Navigation

```html
<!-- ALL interactive elements must be keyboard-accessible -->

<!-- Focus order (tabindex) -->
<button>First (natural)</button>           <!-- Tab order: 1 -->
<a href="/about">Second (natural)</a>      <!-- Tab order: 2 -->
<div tabindex="0">Third (made focusable)</div>  <!-- Tab order: 3 -->
<div tabindex="-1">Not in tab order (programmatic focus only)</div>

<!-- NEVER use tabindex > 0 (breaks natural order!) -->

<!-- Skip navigation link (first element, hidden until focused) -->
<a href="#main-content" class="skip-link">Skip to content</a>
<nav>...long navigation...</nav>
<main id="main-content">...</main>

<style>
.skip-link {
    position: absolute;
    top: -100%;
    left: 0;
    z-index: 100;
}
.skip-link:focus {
    top: 0;  /* Shows when Tab is pressed */
    background: #000;
    color: #fff;
    padding: 8px 16px;
}
</style>
```

```javascript
// Focus management for modals/dialogs
function openModal(modal) {
    modal.hidden = false;
    const focusable = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    focusable[0]?.focus();  // Focus first element in modal
    
    // Trap focus inside modal
    modal.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
        if (e.key === 'Escape') closeModal(modal);
    });
}
```


## Color and Contrast

```css
/* WCAG contrast ratios:
   Normal text: 4.5:1 minimum (AA), 7:1 enhanced (AAA)
   Large text (18px+ or 14px+ bold): 3:1 minimum (AA)
   
   Check: use browser DevTools → Accessibility tab
   Or: webaim.org/resources/contrastchecker/
*/

/* GOOD contrast */
.text { color: #d8d8d8; background: #0a0a0a; }  /* 14.7:1 ✅ */

/* BAD contrast */
.text { color: #888888; background: #666666; }   /* 1.9:1 ❌ */

/* Don't rely on color alone */
/* BAD: only color indicates error */
.error { color: red; }

/* GOOD: color + icon + text */
.error { color: red; }
.error::before { content: "⚠ "; }
/* Screen reader: "Warning: Invalid email" */
/* Color-blind users: see the icon */

/* Focus indicator (NEVER remove!) */
/* BAD: */
*:focus { outline: none; }  /* Keyboard users can't see where they are! */

/* GOOD: custom focus style */
:focus-visible {
    outline: 2px solid #3b82f6;
    outline-offset: 2px;
}
```


---

# CHAPTER 2: COMMON PITFALLS

```
PITFALL 1: Images without alt text
  <img src="chart.png"> → screen reader says "image"
  Fix: <img src="chart.png" alt="Revenue growth chart showing 40% increase in Q3">
  Decorative images: alt="" (empty alt, not missing alt)

PITFALL 2: Removing focus outlines
  :focus { outline: none } → keyboard users are blind
  Fix: style :focus-visible instead (only shows for keyboard, not mouse)

PITFALL 3: Div as button
  <div onclick="submit()"> → not keyboard accessible, no screen reader role
  Fix: <button onclick="submit()"> — gets keyboard, role, and focus for free

PITFALL 4: Color-only information
  "Required fields are in red" → color-blind users can't tell
  Fix: add asterisk, icon, or text label alongside color

PITFALL 5: Missing form labels
  <input placeholder="Email"> → placeholder disappears on type, no screen reader label
  Fix: <label for="email">Email</label><input id="email">

PITFALL 6: Auto-playing media
  Video/audio plays automatically → disorienting, especially for screen reader users
  Fix: never autoplay with sound. Provide play/pause controls.

PITFALL 7: Not testing with keyboard
  Everything works with mouse but broken with keyboard.
  Fix: unplug mouse, navigate your site with Tab/Enter/Escape only.

PITFALL 8: Skipping heading levels
  <h1> then <h3> (no h2) → broken document outline
  Fix: use headings in order. Style with CSS, not heading level.
```