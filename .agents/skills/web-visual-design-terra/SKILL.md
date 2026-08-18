# Web Visual Design

Use this skill when designing or implementing the visual presentation of Django-rendered web pages and HTMX-enhanced interactions. Preserve the existing product design system when one exists; otherwise, use the direction below.

## Design Direction

Create interfaces that are quiet, precise, and content-led. Take inspiration from the restrained visual language of Vercel and Shadcn UI without reproducing either product.

- Prefer a minimal neutral palette built from warm or cool grays, near-white, and near-black.
- Use one accent color sparingly for primary actions, selected states, and focus rings.
- Let typography, whitespace, alignment, and hierarchy carry meaning before adding decoration.
- Use surfaces, borders, and subtle tonal differences to group content. Cards should represent meaningful groups, not surround every element.
- Use subtle shadows only when an element needs elevation, such as a popover, dialog, or floating menu.
- Avoid colorful gradients, large decorative illustrations, excessive rounded containers, strong shadows, and saturated backgrounds unless the product explicitly requires them.
- Make empty states purposeful and concise. Do not use generic dashboard-style visual clutter.

## Color And Themes

Support both light and dark mode from the first implementation. Define color as semantic tokens, so components express purpose rather than hard-coded color values.

Use tokens with names such as:

- `background` and `foreground` for the page canvas and default text.
- `surface` and `surface-foreground` for raised or grouped content.
- `muted` and `muted-foreground` for secondary surfaces and supporting text.
- `border` and `input` for separation and form controls.
- `primary` and `primary-foreground` for the dominant action.
- `secondary` and `secondary-foreground` for lower-emphasis actions.
- `destructive` and `destructive-foreground` for irreversible or dangerous actions.
- `ring` for keyboard focus.

In light mode, use an off-white or white page background, near-black text, light neutral borders, and modest surface contrast. In dark mode, use a near-black or charcoal page background, near-white text, and subdued gray surfaces and borders. Do not invert a light palette mechanically: tune muted text, borders, focus indicators, and disabled controls independently so their hierarchy remains clear.

- Honor `prefers-color-scheme` unless the product provides a persisted user-selected theme.
- If a theme switcher is present, keep its server-rendered initial state correct and make it keyboard accessible.
- Meet accessible contrast requirements in each mode, including muted text, borders that convey meaning, error text, focus rings, and interactive states.
- Never use color as the only way to convey validation, selection, status, or destructive intent. Pair it with text, icons, or structural cues.

## Typography, Spacing, And Layout

- Use the project typeface. If none is established, choose a legible system sans-serif stack; do not add a font dependency without a concrete requirement.
- Establish a small, predictable type scale. Reserve large display text for genuine page-level hierarchy.
- Keep body copy comfortably readable, with adequate line height and a constrained measure for long-form text.
- Use a consistent spacing scale. Prefer generous section spacing and compact, intentional spacing within form controls and toolbars.
- Align content to a clear grid. Constrain reading and data-entry pages to a useful maximum width rather than stretching every layout across large screens.
- Start with a single responsive column. Add sidebars, multi-column forms, or dense tables only when their information value justifies their complexity.
- Use modest, consistent radii. Avoid making every visual boundary pill-shaped.

## Components And States

Design every interactive element with its complete set of states, not just its default appearance.

- Buttons: clearly distinguish primary, secondary, quiet, and destructive actions. Use a visible disabled style but do not communicate unavailability through low contrast alone.
- Links: make text links visually identifiable and preserve their native behavior. Do not style navigation as a button without a semantic reason.
- Forms: group related fields, show persistent labels, explain required or constrained input before submission where useful, and display errors next to the relevant field.
- Validation: pair error color with clear text, associate errors with their controls, retain entered values after a failed server response, and focus the first invalid field when appropriate.
- Tables and lists: favor readable rows, clear headers, useful empty states, and responsive alternatives for narrow screens. Do not force horizontal scrolling for simple data that can be restacked.
- Status feedback: distinguish informational, success, warning, and error messages by text and structure in addition to color.
- Dialogs and menus: use them only when inline content cannot reasonably serve the workflow. They must have a clear title, an obvious close action, correct focus behavior, and a visible elevation above surrounding content.
- Destructive actions: state the consequence plainly, avoid ambiguous confirmation labels such as "OK", and require an appropriate confirmation step when the action is irreversible.

## Django SSR And HTMX

Server-rendered HTML is the baseline. HTMX progressively improves a page; it must not be required for essential navigation, form submission, or comprehension.

- Use semantic Django templates with proper landmarks, headings, forms, buttons, links, labels, and tables. Render a complete, useful page without JavaScript.
- Keep ordinary `action`, `method`, and `href` attributes functional when HTMX is unavailable. HTMX attributes may enhance the same interaction.
- Design fragments so an HTMX swap changes the smallest meaningful region. Avoid replacing page-level layout for a small form result or list update.
- Keep the dimensions and spacing of loading regions stable to reduce layout shift. Use unobtrusive loading indicators, disabled submit controls, or inline progress feedback as appropriate.
- Render server-side validation failures into the affected form region, preserving values and making errors immediately understandable.
- For successful mutations, return a clear success state, updated content, or a redirect according to the workflow. Do not leave users guessing whether an action completed.
- When a swap changes content that needs announcement, use a suitable accessible live region with concise text. Do not make large, frequently updated page regions live.
- After a swap, preserve focus when possible. For errors, move focus to the form error summary or first invalid field; for newly opened UI, place focus in its logical starting control.
- Use CSS transitions sparingly. Respect `prefers-reduced-motion`, and do not make animation necessary to understand state changes.
- Include empty, loading, error, retry, and permission-denied states for asynchronously enhanced regions when they can occur.

## Responsive And Accessible Baseline

- Design mobile-first and test the page at narrow and wide viewport sizes.
- Ensure tap targets have sufficient size and separation, especially for icon-only controls.
- Provide a visible, high-contrast focus indicator that is not removed or replaced solely by hover styling.
- Use semantic HTML before ARIA. When ARIA is needed, use valid roles, names, states, and relationships.
- Associate every form control with a visible label. Do not use placeholder text as its only label.
- Preserve readable contrast and interaction states in light mode, dark mode, high zoom, and forced-color environments where applicable.
- Ensure the interface remains usable by keyboard and does not rely on hover, precise pointer movement, or color discrimination.

## Pre-Delivery Checklist

- The page is visually calm, content-led, and uses a restrained neutral palette.
- Light and dark themes use semantic tokens and maintain hierarchy and contrast.
- HTML remains complete and usable without HTMX or other JavaScript.
- HTMX updates are focused, stable, accessible, and provide clear loading, error, and success feedback.
- Forms retain values after validation errors and expose labels and errors accessibly.
- Keyboard focus, responsive behavior, empty states, and destructive workflows have been considered.
