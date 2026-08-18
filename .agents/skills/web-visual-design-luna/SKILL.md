---
name: web-visual-design-luna
description: Design restrained, modern, accessible web pages for server-rendered Django and HTMX applications using a minimal neutral visual system with first-class light and dark modes.
---

# Web Visual Design Luna

Use this skill when designing or implementing the visual language of a web page, flow, or reusable component in a Django and HTMX application. Treat the page as a server-rendered interface first. HTMX may improve transitions and partial updates, but the underlying HTML, form behavior, accessibility, and information hierarchy must remain complete without client-side rendering.

## Design Direction

Aim for a quiet, precise interface inspired by the restraint of Vercel and shadcn. The page should feel considered through typography, spacing, hierarchy, and interaction states rather than decoration.

- Prefer a minimal neutral palette over a collection of brand colors.
- Use one restrained accent only when it improves hierarchy or identifies a meaningful action.
- Let content, whitespace, and alignment create emphasis.
- Use borders, subtle surface changes, and small tonal shifts before reaching for shadows or color.
- Choose a clear visual concept for the page rather than assembling unrelated cards and controls.
- Preserve the existing product language when one is already established.
- Avoid generic dashboard styling, gratuitous gradients, noisy backgrounds, and decorative elements that do not communicate meaning.

## Start With Structure

Before styling, identify the page's purpose, primary action, important content, and complete set of states. Establish semantic HTML and Django template boundaries before choosing visual treatments.

1. Define the page hierarchy: shell, navigation, heading, supporting context, main content, primary action, and feedback.
2. Group related content with meaningful sections, lists, tables, or forms instead of using cards by default.
3. Choose a consistent content width. Keep long-form reading near 65-75 characters per line and use a wider shell only where the content needs it.
4. Build a responsive layout that collapses intentionally. Do not merely shrink a desktop grid until it becomes cramped.
5. Design the full state matrix before implementation: initial, loading, empty, validation error, request error, success, disabled, and unauthorized or unavailable states where applicable.

## Neutral Color System

Use semantic CSS custom properties. Components should consume roles such as `--background`, `--foreground`, and `--border`, not scattered raw colors. The exact values may be adjusted to suit the product, but the system must remain mostly neutral and maintain clear contrast in both themes.

Recommended roles:

- `--background`: page background
- `--foreground`: primary text and icons
- `--card`: elevated or distinct surface
- `--card-foreground`: content on the card surface
- `--muted`: quiet surface for secondary regions
- `--muted-foreground`: supporting text that still meets contrast requirements
- `--border`: dividers and control boundaries
- `--input`: input boundary when it differs from a normal border
- `--primary`: the main action surface or emphasis color
- `--primary-foreground`: content placed on the primary surface
- `--ring`: keyboard focus indicator
- `--destructive` and `--destructive-foreground`: destructive actions and errors
- `--success`, `--warning`, and their foreground roles when those states are required

An illustrative neutral baseline:

```css
:root {
  color-scheme: light;
  --background: #ffffff;
  --foreground: #18181b;
  --card: #ffffff;
  --card-foreground: #18181b;
  --muted: #f4f4f5;
  --muted-foreground: #71717a;
  --border: #e4e4e7;
  --input: #e4e4e7;
  --primary: #18181b;
  --primary-foreground: #fafafa;
  --ring: #a1a1aa;
  --destructive: #dc2626;
  --destructive-foreground: #ffffff;
}

[data-theme="dark"] {
  color-scheme: dark;
  --background: #09090b;
  --foreground: #fafafa;
  --card: #09090b;
  --card-foreground: #fafafa;
  --muted: #27272a;
  --muted-foreground: #a1a1aa;
  --border: #27272a;
  --input: #3f3f46;
  --primary: #fafafa;
  --primary-foreground: #18181b;
  --ring: #71717a;
  --destructive: #f87171;
  --destructive-foreground: #18181b;
}
```

The values above are a starting point, not a requirement. Check the contrast of every text, icon, border, focus, and status treatment against its actual surface. Keep status colors localized to status content and never communicate meaning through color alone. Pair them with text, an icon with an accessible name, or another clear indicator.

### Theme Behavior

- Give every component a valid appearance in both themes. Do not rely on a white background, black text, or a light-only shadow hidden in a component rule.
- Prefer `data-theme="light"` and `data-theme="dark"` on the root element for an explicit user preference, with `prefers-color-scheme` as the fallback when no explicit preference exists.
- In a Django response, render the resolved theme on `<html>` whenever the server knows the user's preference. This avoids a light page flashing before client-side code changes it.
- Set `color-scheme` so native controls, scrollbars, and form elements match the selected theme.
- If a theme toggle is provided, make it a real accessible control and preserve its preference through the application's established server or session mechanism. Do not make a theme toggle the only way to discover the current theme.
- Test long text, disabled controls, validation messages, focus rings, dialogs, and images in both modes.

## Typography and Spacing

- Use the existing typeface when one exists. Otherwise start with a readable system sans stack rather than adding a font dependency solely for appearance.
- Establish a small type scale with a clear distinction between page title, section heading, body text, metadata, labels, and helper text.
- Use weight and size changes sparingly. Do not make every heading bold, uppercase, or tightly tracked.
- Keep body text comfortable to read with an appropriate line height. Supporting text must remain legible and must not be treated as placeholder decoration.
- Use a consistent spacing scale, preferably based on 4px or 8px increments, and create larger gaps between semantic sections than between controls within a group.
- Use whitespace to separate hierarchy. Avoid filling every empty area with a card, divider, icon, or background tint.
- Keep interactive controls large enough to use comfortably on touch screens and leave enough space to distinguish adjacent actions.

## Surfaces, Borders, and Shape

- Use a small radius scale. A modest radius on controls and a slightly larger radius on grouped surfaces is usually sufficient.
- Prefer a one-pixel semantic border or a subtle surface contrast for grouping. Do not outline every nested element.
- Use shadows only to communicate elevation or a floating relationship. Keep them soft and theme-aware.
- Do not combine heavy borders, strong shadows, large radii, and saturated fills on the same component.
- Keep icon style, stroke weight, and alignment consistent. Icons support labels; they should not replace an unclear label.

## Components and States

Design components from their semantic role and state, not from a visual pattern alone.

- Primary actions should be visually distinct without dominating the page. Use a neutral filled button by default when the design direction is neutral.
- Secondary actions may use an outlined or lower-contrast treatment. Use a ghost action only where its click target remains obvious.
- Destructive actions need explicit wording and a clear destructive state. Do not make a destructive action look like an ordinary secondary action.
- Forms need visible labels, useful helper text, clear required-field treatment, inline validation, and an error summary when several fields fail.
- Inputs must have discernible boundaries in both themes and a strong, non-color-only focus treatment.
- Tables should preserve scanability on narrow screens. If horizontal scrolling is necessary, make it apparent and keep important identifiers available.
- Empty states should explain what is absent and offer the next useful action. Do not use an oversized illustration to compensate for missing guidance.
- Notifications and request feedback should be concise, dismissible when appropriate, and announced accessibly.
- Disabled controls should communicate why an action is unavailable where that reason is not obvious. Do not use disabled styling to hide authorization failures.
- Keep menus, dialogs, popovers, and other floating surfaces visually connected to their trigger and fully usable by keyboard.

For each interactive component, specify at least:

- Default
- Hover, where a pointing device exists
- Focus-visible
- Active or pressed
- Disabled
- Loading
- Success or completion feedback
- Error or invalid feedback

## Django and HTMX Guidance

### Server-Rendered First

- Render meaningful semantic HTML from Django templates on the initial request.
- Treat the full page response and every HTMX fragment as a valid, understandable representation of the interface.
- Keep business rules, authorization, and validation on the server. Visual controls and hidden buttons are not permission checks.
- Use template partials for repeated visual units and give each HTMX replacement a stable, intentional boundary.
- Keep partials free of assumptions about client-side state that the server does not render.

### HTMX Transitions

- Design the before-request, in-flight, response, and failure states instead of relying on a spinner alone.
- Use an `hx-indicator` or an equivalent request class to show localized progress without making the whole page appear broken.
- Keep the triggering control understandable while a request is in progress. Prevent accidental duplicate submissions where needed and restore the control after failure.
- Use `aria-busy`, live regions, or another suitable accessible announcement for meaningful asynchronous feedback.
- Preserve the user's visual position and focus after a fragment swap. A successful update should not unexpectedly move the user to the top of the page.
- Return the smallest valid fragment for the requested target, but make errors render into the same region as the successful result when possible.
- Prefer ordinary links and forms as the baseline. Add HTMX attributes as progressive enhancement rather than creating an HTMX-only path for essential navigation or submission.
- Avoid flashy transitions. Use short, reduced-motion-aware transitions only when they clarify what changed.

### Template Boundaries

- Keep page shell, navigation, content sections, controls, feedback, and repeated rows in predictable template boundaries.
- Give error and success messages stable locations so an HTMX response can update them without changing the surrounding layout.
- Use Django's normal CSRF-protected form flow for browser mutations.
- Render validation errors next to their fields and keep the user's submitted values when a request fails validation.
- Make loading and empty markup part of the template design, not an afterthought added only in JavaScript.

## Responsive and Accessible Output

- Start with the narrow layout and add space or columns as the viewport allows.
- Preserve reading order when grids collapse. Do not use visual reordering that conflicts with keyboard or screen-reader order.
- Ensure navigation, forms, tables, dialogs, and menus remain usable with keyboard, zoom, and touch input.
- Use visible `:focus-visible` styles with sufficient contrast against the current surface.
- Meet at least WCAG AA contrast targets for normal text and controls. Verify muted text instead of assuming that low contrast looks refined.
- Use labels, descriptions, and error associations in the HTML. Do not rely on placeholder text as a label.
- Respect `prefers-reduced-motion: reduce` and avoid motion that is required to understand a state change.
- Keep status and validation information available as text and expose asynchronous updates to assistive technology where appropriate.
- Use semantic landmarks and heading order so the visual hierarchy and document structure agree.

## Implementation Workflow

1. Read the content and request states before selecting components.
2. Define semantic color, typography, spacing, radius, and elevation tokens.
3. Build the semantic Django template and its partial boundaries.
4. Implement the light theme first, then explicitly test and tune the dark theme rather than mechanically inverting colors.
5. Add responsive behavior at content-driven breakpoints.
6. Add HTMX behavior only after the non-JavaScript flow works.
7. Exercise keyboard navigation, focus, validation, loading, empty, success, error, authorization, and reduced-motion states.
8. Review the page at narrow and wide widths in both themes for hierarchy, contrast, alignment, and unintended visual noise.

## Review Checklist

- The page has one clear primary action and a readable visual hierarchy.
- The palette is predominantly neutral and all colors have semantic roles.
- Light and dark themes are complete, intentional, and contrast-checked.
- No component depends on a raw light-only color, invisible border, or color-only status signal.
- Typography, spacing, radii, borders, and shadows follow a small consistent system.
- The initial Django response is useful without JavaScript.
- HTMX swaps preserve context, focus, feedback, and layout stability.
- Forms expose labels, helper text, validation, and server-rendered errors.
- Empty, loading, success, failure, disabled, and unavailable states are designed.
- Responsive behavior preserves content order and usability.
- Keyboard focus, reduced motion, touch targets, and semantic structure have been considered.
- The result feels specific to the content and product rather than like a generic dashboard template.
