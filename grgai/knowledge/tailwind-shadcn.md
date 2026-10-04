# TailwindCSS + shadcn/ui — best practices

## Tailwind setup
- Install per framework (Next/Vite have flags). Configure `content` globs so classes aren't purged.
- Define design tokens as CSS variables in `globals.css` under `:root` and `.dark`; map them in `tailwind.config` `theme.extend.colors` (e.g. `background`, `foreground`, `primary`, `muted`, `border`).
- Prefer utility classes in markup. Extract a component (not an `@apply` blob) when a pattern repeats.
- Use the `cn()` helper (`clsx` + `tailwind-merge`) to compose conditional classes without conflicts:
```ts
export function cn(...i: ClassValue[]) { return twMerge(clsx(i)); }
```

## Dark mode
- `darkMode: 'class'` in config. Toggle by adding/removing `dark` on `<html>`. Persist choice in `localStorage`, and respect `prefers-color-scheme` on first load.
- Always style via tokens (`bg-background text-foreground`) so both themes work from one markup.

## shadcn/ui
- Init: `npx shadcn@latest init`; add components: `npx shadcn@latest add button card dialog input ...`.
- Components are **copied into your repo** (`components/ui/`) — you own and can edit them. Not a dependency to upgrade.
- Built on Radix primitives (accessible) + Tailwind tokens. Compose them; keep your app components in `components/` separate from `components/ui/` primitives.

## Responsive & layout
- Mobile-first: base styles are mobile; add `sm: md: lg: xl:` for larger. Test at 375px, 768px, 1280px.
- Layout with fl/grid: `flex`, `grid grid-cols-1 md:grid-cols-3 gap-4`, `container mx-auto px-4`.
- Spacing scale is 4px steps; keep vertical rhythm consistent. Max content width ~`max-w-7xl`.
- Use semantic HTML (`<header> <main> <nav> <section>`), focus-visible rings, and `aria-*` for a11y.
