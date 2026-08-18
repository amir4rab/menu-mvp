---
name: web-visual-design-deepseek-flash
description: Visual design guidance for SSR web pages built with Django and HTMX using Tailwind CSS. Use when styling pages, components, or partials — color choices, layout, typography, spacing, and light/dark mode. Encourages a minimal, neutral, Vercel-style palette applied through Tailwind utility classes with an SSR-safe dark mode toggle.
---

# Web Visual Design

## Core Principles

- Minimalism: every element earns its place. Remove decoration before adding it.
- Neutral first: near-black, near-white, and gray scale carry the interface. Color is a signal, not decoration.
- Whitespace is a layout tool: generous spacing improves clarity more than borders and shadows.
- Consistency: reuse the same Tailwind tokens for spacing, border, text, and surface across all partials.
- Deliver content with the least visual noise that preserves hierarchy and readability.

## Palette (Vercel-style, Neutral)

Paint in neutral scale; the accent must be the only saturated element on the page.

Light mode (`light` / default):

- Surface: `bg-white`, text `text-neutral-950`
- Muted surface: `bg-neutral-100`, borders `border-neutral-200`
- Muted text: `text-neutral-500`, headings `text-neutral-900`
- URL/links or primary actions (only if needed): a single accent such as `text-blue-600` / `bg-blue-600`

Dark mode:

- Surface: `bg-neutral-950`, text `text-neutral-100` (near-black mode, °Vercel-style)
- Muted surface: `bg-neutral-900`, borders `border-neutral-800`
- Muted text: `text-neutral-400`, headings `text-neutral-50`
- Accent: `text-blue-500` / `bg-blue-500` only if used in light mode

Rules:

- Never place dark-mode hues on light-mode pages or vice versa; each mode is a complete set.
- Avoid pure `#000` fills at scale; prefer `neutral-950` for depth without harsh contrast.
- No gradients, glows, shadows beyond `shadow-sm`, or saturated backgrounds except the single accent.
- Maintain WCAG AA contrast in both modes for body text (muted text on surface must still pass).

## Tailwind Usage

- Utility-first throughout: no inline `style=` attributes in templates or partials.
- Stick to the default Tailwind spacing scale and `text-sm`/`text-base` body sizes; use `text-lg`/`text-2xl` sparingly for headings.
- Define any custom brand accent in `tailwind.config.*` (theme.extend.colors) rather than repeating hex values.
- Configure dark variant for class toggling (Tailwind v3: `darkMode: 'class'`; Tailwind v4: custom variant for `.dark`).
- Interactive states: `hover:`/`focus-visible:` only; no permanent hovers, no unlabeled color-only states.

## Dark Mode (SSR-safe for Django + HTMX)

Mechanism:

- Theme lives as a class (`dark` or absent) on the `<html>` element; all `dark:` utilities hang off it.
- Django view/context processor reads the `theme` cookie and renders `<html lang="..." class="dark">` (or classless) in base.html — correct theme server-side, no flash of wrong theme (FOUC) on full loads.
- When no cookie is set, honor `prefers-color-scheme: dark` via a small inline script or CSS media default.
- Toggle control sends the choice to the server (e.g., `hx-post`-style cookie setter) and updates the `dark` class client-side for immediacy.

HTMX notes:

- Partial swaps never re-render `<html>`, so they inherit the current theme automatically — keep partials theme-agnostic.
- Never hard-code a theme inside a partial; always use `dark:` variants.
- Ensure `hx-swap` targets keep both variants valid (test each partial in both modes).

## Django/HTMX Application

- Tailwind is built as a Django static asset (via the project's build pipeline); utility classes ship in CSS, templates stay clean.
- Compose pages from small base templates and partials; reuse the same token choices everywhere.
- Focus management and contrast apply to every interactive element, including HTMX-triggered ones.
- User-visible text stays translation-ready; visuals must not rely on text color alone.

## Checklist

- [ ] Only neutral scale + the single allowed accent used
- [ ] Both light and dark variants styled for every component/partial
- [ ] Contrast passes AA in both modes
- [ ] No inline styles; utilities only
- [ ] Dark theme renders server-side from the cookie — no FOUC on full load
- [ ] HTMX partial swaps tested in both modes
- [ ] Spacing consistent with the default scale; no ad-hoc values
- [ ] No gradients, glows, or decorative color