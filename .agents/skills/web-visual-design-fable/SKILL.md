---
name: web-visual-design-fable
description: Visual design system for server-rendered Django + HTMX pages styled with Tailwind CSS. Use whenever you build, style, or restyle any page, template, partial, or component in this stack. Defines a minimal neutral color system (semantic tokens, automatic light/dark theming with server-side override), typography, spacing, component recipes, and HTMX state styling.
---

# Web Visual Design — Fable

A design language for SSR pages built with Django templates, HTMX, and Tailwind CSS (v4, CSS-first config). The aesthetic is quiet, neutral, and content-first — in the spirit of Vercel and shadcn/ui: white/near-black surfaces, a gray ramp for everything else, hue only where it carries meaning.

## 1. Philosophy

- **Monochrome by default.** Surfaces and text are achromatic grays. If you reach for a color, it must *mean* something: destructive, success, or focus. There is no brand accent.
- **Contrast does the hierarchy.** Primary content is near-black on near-white (or inverted); secondary content steps down to `muted-foreground`. Never invent intermediate grays.
- **Borders over shadows.** Separation comes from 1px borders and spacing. Shadows are reserved for elements that genuinely float (menus, dialogs).
- **Whitespace is a feature.** When a layout feels bad, add space before adding decoration.
- **Semantic tokens only.** Templates never use raw palette utilities (`bg-gray-100`, `text-neutral-500`, hex values). They use the tokens below, which is also what makes dark mode free.

## 2. Color system

One semantic token set, defined once with `light-dark()` so every token carries both modes. Values are OKLCH; the ramp is pure gray (chroma 0) except the two status hues.

```css
/* static/src/app.css */
@import "tailwindcss";

:root {
  color-scheme: light dark;                 /* follow the OS by default */

  /*                       light                dark                    */
  --background:            light-dark(oklch(1 0 0),        oklch(0.145 0 0));
  --foreground:            light-dark(oklch(0.15 0 0),     oklch(0.985 0 0));
  --card:                  light-dark(oklch(1 0 0),        oklch(0.19 0 0));
  --muted:                 light-dark(oklch(0.967 0 0),    oklch(0.25 0 0));
  --muted-foreground:      light-dark(oklch(0.53 0 0),     oklch(0.7 0 0));
  --border:                light-dark(oklch(0.92 0 0),     oklch(1 0 0 / 12%));
  --input:                 light-dark(oklch(0.92 0 0),     oklch(1 0 0 / 16%));
  --primary:               light-dark(oklch(0.2 0 0),      oklch(0.92 0 0));
  --primary-foreground:    light-dark(oklch(0.985 0 0),    oklch(0.2 0 0));
  --secondary:             light-dark(oklch(0.967 0 0),    oklch(0.25 0 0));
  --secondary-foreground:  light-dark(oklch(0.2 0 0),      oklch(0.985 0 0));
  --destructive:           light-dark(oklch(0.55 0.22 26), oklch(0.65 0.2 26));
  --destructive-foreground: light-dark(oklch(1 0 0),       oklch(0.2 0 0));
  --success:               light-dark(oklch(0.5 0.15 150), oklch(0.72 0.19 150));
  --ring:                  light-dark(oklch(0.6 0 0),      oklch(0.65 0 0));

  --radius: 0.625rem;
}

/* Manual override: forcing color-scheme flips every light-dark() token */
:root[data-theme="light"] { color-scheme: light; }
:root[data-theme="dark"]  { color-scheme: dark; }

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-success: var(--success);
  --color-ring: var(--ring);

  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);

  --font-sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
}

@layer base {
  * { border-color: var(--color-border); }
  body {
    background: var(--color-background);
    color: var(--color-foreground);
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
  }
}
```

Token meanings:

| Token | Use for |
|---|---|
| `background` / `foreground` | Page ground and body text. |
| `card` | Raised surface (cards, panels, table headers). Text on it is still `foreground`. |
| `muted` / `muted-foreground` | Subtle fills (hover states, skeletons, code) and secondary text (captions, help text, timestamps). |
| `border` / `input` | 1px separation lines; `input` for form control borders (slightly stronger in dark). |
| `primary` / `primary-foreground` | The one solid button per view. Near-black in light, near-white in dark. |
| `secondary` / `secondary-foreground` | Low-emphasis filled buttons and chips. |
| `destructive` / `destructive-foreground` | Delete/danger actions and error text. In dark mode it lightens, so its paired text darkens — same rule as `primary`. |
| `success` | Positive status text/badges only. Never a button color. |
| `ring` | Focus rings, everywhere, both modes. |

**Rules**
- Never `dark:` variants for color. If you feel you need one, the fix is a token, not a variant.
- Never raw palette classes or hex in templates. `grep -rE 'bg-(gray|neutral|zinc|slate)-|#[0-9a-fA-F]{3,6}' templates/` should return nothing.
- Body-size text pairs must hold WCAG AA (≥ 4.5:1): the values above were chosen so that `foreground`, `muted-foreground`, `destructive`, and `success` all pass on `background`, `card`, and `muted`, and each `*-foreground` passes on its fill, in both modes. If you tune a value, re-check its pairs.
- Opacity modifiers (`hover:bg-primary/90`, `bg-destructive/10`) are the only sanctioned way to derive in-between shades.

Tailwind build in Django (standalone CLI, no Node needed):

```bash
tailwindcss -i static/src/app.css -o static/css/app.css --minify   # --watch in dev
```

Link `{% static 'css/app.css' %}` from the base template.

## 3. Theming: system by default, one cookie to override, zero flash

Three states: no cookie → follow OS; `theme=light` / `theme=dark` → forced. Because Django renders the attribute server-side and the system case is pure CSS, **no JavaScript runs and no wrong-theme flash is possible**.

```python
# context_processors.py  (register in TEMPLATES["OPTIONS"]["context_processors"])
def theme(request):
    t = request.COOKIES.get("theme", "")
    return {"theme": t if t in ("light", "dark") else ""}
```

```html
{# base.html #}
<html lang="en" {% if theme %}data-theme="{{ theme }}"{% endif %}>
<head>
  <meta name="color-scheme" content="{% if theme %}{{ theme }}{% else %}light dark{% endif %}">
  ...
```

(The `<meta>` mirrors the CSS so even the instant before the stylesheet loads paints the right ground.)

```python
# views.py — works with plain forms; no JS required
def set_theme(request):
    theme = request.POST.get("theme", "")
    response = redirect(request.POST.get("next") or "/")
    if theme in ("light", "dark"):
        response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 365, samesite="Lax")
    else:
        response.delete_cookie("theme")   # back to system
    return response
```

The toggle is a small form (three buttons: Light / Dark / System) posting to `set_theme` with `next={{ request.path }}`. `hx-boost` navigation is safe: it swaps `<body>`, so the `data-theme` attribute on `<html>` survives.

## 4. Typography

- **Stack:** the system stack defined above. If a webfont is truly wanted, self-host one neutral grotesk (Inter/Geist-like) and keep the same tokens.
- **Scale (rem-based, small):** `text-sm` (14px) is the default UI size; `text-base` (16px) for prose; headings `text-lg` / `text-xl` / `text-2xl` / `text-3xl` with `font-semibold tracking-tight`. Nothing larger than `text-3xl` inside an app view.
- **Weights:** 400 body, 500 labels/nav/buttons, 600 headings. Never 700+.
- **Secondary text** is `text-muted-foreground`, not a smaller size. Change color before changing size.
- **Numbers** in tables and metrics get `tabular-nums`.
- Prose measure: `max-w-prose` or `max-w-[65ch]`; line-height `leading-relaxed` for prose, default elsewhere.

## 5. Spacing, surfaces, depth

- **4px rhythm.** Use the Tailwind scale; common picks: `gap-2/3/4`, control padding `px-3 py-2` (dense `px-2.5 py-1.5`), card padding `p-6`, section spacing `py-8`–`py-12`, page gutters `px-4 sm:px-6`.
- **Layout:** center content in `max-w-5xl mx-auto` (forms: `max-w-md`). Prefer `flex`/`grid` + `gap` over margins.
- **Radius:** `rounded-md` on controls, `rounded-lg` on cards/dialogs, `rounded-full` on pills and avatars.
- **Depth:** flat by default. Cards: `border bg-card` (no shadow, or `shadow-xs` at most). Overlays (dropdown, dialog, toast): `border bg-card shadow-lg`. Nothing else casts shadow.
- **Dividers:** `divide-y divide-border` inside lists/tables rather than per-row borders.

## 6. Component recipes

Class strings for Django partials (`{% include %}`); keep them verbatim so pages stay uniform.

**Buttons** — shared base:
`inline-flex items-center justify-center gap-2 h-9 px-4 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:opacity-50 disabled:pointer-events-none`

| Variant | Add | Use |
|---|---|---|
| Primary | `bg-primary text-primary-foreground hover:bg-primary/90` | One per view. |
| Secondary | `bg-secondary text-secondary-foreground hover:bg-secondary/80` | Everything else filled. |
| Outline | `border border-input bg-background hover:bg-muted` | Neutral actions beside inputs. |
| Ghost | `hover:bg-muted` | Toolbars, icon buttons, cancel. |
| Destructive | `bg-destructive text-destructive-foreground hover:bg-destructive/90` | Delete, always paired with confirmation. |

**Input / select / textarea:**
`flex w-full h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50`

Django forms — attach once, in the form class, not per template:

```python
INPUT = "flex w-full h-9 rounded-md border border-input bg-transparent px-3 py-1 text-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-50"

class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": INPUT}))
```

Field partial: label `text-sm font-medium`, help text `text-sm text-muted-foreground`, errors `text-sm text-destructive`, stacked with `space-y-1.5`; invalid inputs add `border-destructive`.

**Card:** `rounded-lg border bg-card p-6` — title `text-lg font-semibold tracking-tight`, description `text-sm text-muted-foreground`, header block `space-y-1.5 mb-4`.

**Table:** wrapper `overflow-x-auto rounded-lg border`; table `w-full text-sm`; header cells `h-10 px-3 text-left font-medium text-muted-foreground bg-card`; body `divide-y divide-border`, cells `px-3 py-2.5`; row hover `hover:bg-muted/50`; numeric cells `text-right tabular-nums`.

**Nav bar:** `border-b bg-background` wrapper, inner `max-w-5xl mx-auto flex h-14 items-center gap-6 px-4`; links `text-sm text-muted-foreground hover:text-foreground transition-colors`, active link `text-foreground font-medium`.

**Badge:** `inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium` + neutral `border text-muted-foreground` / success `bg-success/10 text-success` / destructive `bg-destructive/10 text-destructive`. Pair status badges with a text label, never a dot alone.

**Empty state:** centered `py-12 text-center` block — icon or glyph in `text-muted-foreground`, one-line title `text-sm font-medium`, one-line hint `text-sm text-muted-foreground`, optional secondary button. No illustrations.

## 7. HTMX states & motion

Motion is functional feedback only: 150 ms, ease, opacity/color — no slides, no bounces.

```css
/* app.css additions */
.htmx-indicator { opacity: 0; transition: opacity 150ms ease; }
.htmx-request .htmx-indicator, .htmx-request.htmx-indicator { opacity: 1; }

@media (prefers-reduced-motion: no-preference) {
  .htmx-settling [hx-swap-fade], [hx-swap-fade].htmx-settling { animation: fade-in 150ms ease; }
  @keyframes fade-in { from { opacity: 0; } }
}
```

- **Every `hx-post`/`hx-get` that can take >100 ms gets an `hx-indicator`** — an inline spinner (`size-4 animate-spin`, stroked in `currentColor`) or the word "Saving…" in `text-muted-foreground`.
- While a form is in flight, rely on `htmx-request` + the button's `disabled:opacity-50` styles (`hx-disabled-elt="find button"`).
- **Skeletons** for slow-loading regions (`hx-trigger="load"`): blocks of `animate-pulse rounded-md bg-muted` sized like the real content.
- Swapped-in content may fade via the `hx-swap-fade` hook above; guarded by `prefers-reduced-motion`, as is `animate-pulse` (`motion-reduce:animate-none`).
- Errors from HTMX partials render as normal Django form errors (`text-destructive`) or an inline alert `rounded-md border border-destructive/25 bg-destructive/10 px-3 py-2 text-sm text-destructive` — no toast library.

## 8. Accessibility

- **Contrast floors:** ≥ 4.5:1 for body text, ≥ 3:1 for large text and UI outlines/focus rings. The token pairs in §2 satisfy this; hold the line when tuning.
- **Focus is always visible:** the `focus-visible:ring-2 focus-visible:ring-ring` pattern on every interactive element. Never remove an outline without a replacement.
- **Color never carries meaning alone:** destructive/success always come with a word or icon.
- `color-scheme` (set in §2–3) keeps native form controls, scrollbars, and highlights matched to the active theme — don't restyle those by hand.
- Keep interactive targets ≥ 36px tall (`h-9`); icon-only buttons get `aria-label`.

## 9. Do / Don't

**Do**
- Use semantic tokens for every color decision; let `light-dark()` do dark mode.
- Default to `text-sm`, borders, whitespace, and one primary button per view.
- Style Django widgets in the form class; keep component class strings verbatim in partials.
- Give every non-instant HTMX request an indicator, and every element a visible focus ring.

**Don't**
- Don't use `dark:` color variants, raw gray utilities, or hex values in templates.
- Don't introduce accent/brand hues, gradients, or decorative shadows.
- Don't animate anything longer than ~150 ms or without `prefers-reduced-motion` cover.
- Don't hand-build a JS theme switcher — the cookie + `data-theme` + `color-scheme` flow already covers it without FOUC.
