# Boilerplates — ready-to-use snippets

## Responsive Navbar (React + Tailwind)
```tsx
export function Navbar() {
  const [open, setOpen] = useState(false);
  const links = [["Home","/"],["Features","/features"],["Pricing","/pricing"]];
  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/80 backdrop-blur">
      <nav className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4">
        <a href="/" className="font-bold">Brand</a>
        <div className="hidden gap-6 md:flex">
          {links.map(([l,h]) => <a key={h} href={h} className="text-sm text-muted-foreground hover:text-foreground">{l}</a>)}
        </div>
        <button className="md:hidden" onClick={() => setOpen(o=>!o)} aria-label="Menu">☰</button>
      </nav>
      {open && <div className="border-t border-border px-4 py-2 md:hidden">
        {links.map(([l,h]) => <a key={h} href={h} className="block py-2 text-sm">{l}</a>)}
      </div>}
    </header>
  );
}
```

## Form with validation (controlled)
```tsx
function ContactForm() {
  const [v, setV] = useState({ email: "", msg: "" });
  const [err, setErr] = useState<Record<string,string>>({});
  function submit(e: React.FormEvent) {
    e.preventDefault();
    const next: Record<string,string> = {};
    if (!/^[^@]+@[^@]+\.[^@]+$/.test(v.email)) next.email = "Enter a valid email";
    if (v.msg.trim().length < 10) next.msg = "At least 10 characters";
    setErr(next);
    if (Object.keys(next).length === 0) { /* send */ }
  }
  return (
    <form onSubmit={submit} className="space-y-4">
      <div>
        <label className="text-sm">Email</label>
        <input value={v.email} onChange={e=>setV({...v,email:e.target.value})}
               className="w-full rounded-md border border-border bg-background px-3 py-2"/>
        {err.email && <p className="text-sm text-red-500">{err.email}</p>}
      </div>
      <button className="rounded-md bg-primary px-4 py-2 text-primary-foreground">Send</button>
    </form>
  );
}
```

## Auth pattern (Supabase, email/password)
```ts
const { data, error } = await supabase.auth.signInWithPassword({ email, password });
if (error) showError(error.message);
// Guard a server route:
const { data: { user } } = await supabase.auth.getUser();
if (!user) return new Response("Unauthorized", { status: 401 });
```

## Fetch wrapper (typed)
```ts
export async function api<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, { headers: { "Content-Type": "application/json" }, ...init });
  if (!res.ok) throw new Error((await res.json().catch(()=>({})))?.error ?? res.statusText);
  return res.json() as Promise<T>;
}
```

## Dark-mode toggle
```ts
function toggleTheme() {
  const dark = document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", dark ? "dark" : "light");
}
// on load:
if (localStorage.theme === "dark" || (!("theme" in localStorage) && matchMedia("(prefers-color-scheme: dark)").matches))
  document.documentElement.classList.add("dark");
```
