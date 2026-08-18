---
name: web-visual-design-kimi3
description: Use when creating or restyling server-rendered web pages (Django templates with HTMX). Covers layout, color, typography, spacing, component styling, and light/dark theming in a minimal, neutral Vercel/Shadcn-inspired aesthetic.
---

# Web Visual Design

Apply this skill whenever generating or modifying HTML/CSS for Django templates, including HTMX partials. The goal is a quiet, content-first interface: neutral surfaces, restrained color, generous whitespace, and crisp typography.

## Design Philosophy

- **Minimal and content-first.** Chrome is invisible; content is the interface. Remove decoration before adding it.
- **Neutral by default.** The palette is a grayscale ramp. Color appears rarely and only with intent: one accent for primary actions and links, muted semantic colors for feedback.
- **Inspired by Vercel/Shadcn.** Think: near-white backgrounds (`#fafafa`, `#ffffff`) and near-black text (`#0a0a0a`) in light mode; inverted (`#0a0a0a` background, `#fafafa` text) in dark mode. Mid-grays (e.g., `#737373`, `#a3a3a3`) for secondary text, and light border grays (e.g., `#e5e5e5` light / `#262626` dark) for separation.
- **Borders over shadows.** Separate surfaces with 1px borders and subtle background shifts. Shadows, if used at all, are small and soft — never heavy or layered.
- **Small radii, generous space.** Border-radius around 6–8px. Prefer more whitespace over more elements. When in doubt, increase padding.

## Color Rules

- Use exactly **one accent color** for interactive emphasis (primary buttons, links, focus rings). A restrained blue such as `#2563eb` (light) / `#3b82f6` (dark) works well, as does pure black-on-white / white-on-black for the Vercel look.
- Semantic colors are **muted**, never saturated: a desaturated green for success, amber for warning, red (e.g., `#dc2626` light / `#ef4444` dark) for destructive/error states.
- Never use gradients, saturated backgrounds, or more than one accent hue.
- Text hierarchy comes from gray tones, not color: primary text is near-black/near-white, secondary text is mid-gray.

## Typography

- Use the **system font stack**: `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`. Monospace (`ui-monospace, "SF Mono", Menlo, monospace`) only for code/IDs.
- Keep a **restrained scale**: a base of 14–16px, a few heading steps, and a small (12–13px) size for metadata. Avoid more than ~5 distinct sizes.
- Limit font weights to normal (400), medium (500), and semibold (600). Headings are semibold, not bold-black.
- Use `line-height` ~1.5 for body text and tighter (~1.2) for headings. Cap line length around 65–75 characters for readability.

## Color Modes (Light & Dark)

- Define **all colors as CSS custom properties** on `:root` for light mode, and override them under a `.dark` class on `<html>`. Components reference only variables (e.g., `var(--background)`, `var(--foreground)`, `var(--border)`, `var(--accent)`) — never hardcoded hex values.
- **Default to system preference** via `prefers-color-scheme`, and provide a **manual toggle** that overrides it and persists the choice in `localStorage`. The toggle wins once the user has chosen.
- Include an **anti-FOUC inline script in `<head>`** that reads `localStorage` (falling back to the media query) and sets the `.dark` class before first paint.
- Verify every component in both modes. Contrast ratios should hold in each; muted dark-mode surfaces use slightly elevated grays (`#171717`, `#1c1c1c`) rather than pure black for cards.

## Component Styling

- **Buttons:** one solid accent-filled primary variant; everything else is ghost (transparent, hover background shift) or outline (1px border). Consistent height (~36–40px) and padding.
- **Forms:** 1px bordered inputs with a subtle background, accent-colored focus ring (thin outline or ring, not a glow), mid-gray placeholders, error text in muted red below the field.
- **Cards:** 1px border, small radius, flat background (or one step above the page background in dark mode). No drop shadows by default.
- **Tables:** horizontal row borders only, no vertical rules, header row in secondary gray text, generous cell padding.
- **Navigation:** text links with gray-to-foreground hover transitions; the active item gets full-contrast text, not a colored pill.

## Django / HTMX Implementation Notes

- Put the stylesheet (with the CSS custom properties and component classes) in the app's `static/` directory and load it in the base template with `{% load static %}` and `{% static '...' %}`.
- **HTMX partials reuse the same classes** as full pages — they inherit the base stylesheet, so never inline per-partial styles.
- **Loading states:** use `hx-indicator` with a subtle opacity fade or a skeleton placeholder; prefer these over spinners. Use `hx-disabled-elt` to dim buttons during requests.
- **Transitions:** keep `hx-swap` transitions subtle (e.g., a short `transition:` settle or a 150–200ms opacity fade). No sliding or bouncing.
- **Dark-mode toggle:** a small button in the base template that flips the `.dark` class and writes to `localStorage`; it must work with HTMX navigation (place it outside swapped regions or use `hx-preserve`).
- Templates stay clean: styling lives in the stylesheet, templates only apply semantic class names.

## Do / Don't

**Do:**
- Use one accent color and a neutral gray ramp.
- Define every color as a variable that works in both light and dark mode.
- Separate with borders and whitespace.
- Keep loading/transition states subtle and fast.

**Don't:**
- Use gradients, heavy shadows, glassmorphism, or saturated backgrounds.
- Hardcode hex colors inside components or templates.
- Introduce multiple accent hues or decorative illustrations.
- Add per-page or per-partial inline styles.
