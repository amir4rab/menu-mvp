# Django SSR And HTMX

## Rendering Model

Django Templates are the primary user interface. A normal URL should render a complete, meaningful page. HTMX improves specific interactions by requesting and swapping server-rendered fragments; it does not move business rules or rendering responsibility into browser JavaScript.

Use semantic HTML first. A page should retain its core workflow with standard links and form submissions where reasonable. HTMX behavior may be unavailable because of a browser setting, a network issue, an integration mistake, or an accessibility tool.

Internationalization is a rendering concern from the first feature. Keep all user-visible messages translation-ready, use Django's locale-aware formatting, and preserve the active locale across complete pages, redirects, and HTMX fragments. Public cacheable pages use locale-prefixed URLs; private or authorized pages use the project's documented session or cookie locale policy. See [Internationalization](internationalization.md) for the complete baseline.

## Views, Forms, And Responses

- Use Django forms or typed input parsing at every browser input boundary. Validate format, ownership, ranges, and cross-field rules before invoking application code.
- Use POST-Redirect-GET after a successful standard form submission to prevent accidental resubmission.
- For an HTMX form, return the updated fragment or use an explicit HTMX redirect after success. Return a swap-compatible validation response for expected form errors.
- Do not use GET requests to mutate server state. Use POST, or another appropriate unsafe method with CSRF protection.
- Return `404` for objects that should not be disclosed, and use explicit permission behavior for resources the user may know exist. Match the product's security model consistently.
- Keep view functions or class-based views small. Query input, call a use case or query service, and render a response.

## HTMX Conventions

- Give every HTMX endpoint an ordinary HTTP meaning. Do not create an endpoint that only works when a client sends a private header.
- Choose a stable fragment boundary and name the template accordingly, for example `appointments/_appointment_row.html`.
- Vary cacheable responses by `HX-Request` when the full-page and fragment representations differ. Do not cache personalized pages in a shared cache without a reviewed strategy.
- Use `hx-target` and `hx-swap` intentionally. Keep the affected region small and ensure replacement markup remains valid HTML in that location.
- Prefer server-generated events or response headers for small UI coordination. Do not introduce a client state store for ordinary form and list interactions.
- Treat duplicate submissions, stale pages, and concurrent updates as server-side concerns. Disable buttons for feedback but enforce idempotency or conflict handling on the server when needed.
- Document non-obvious fragment contracts and add integration tests for high-value interactions.

## Accessibility

- Use semantic headings, labels, buttons, links, tables, and landmarks before adding ARIA.
- Every form field has a programmatically associated label and accessible validation message.
- Preserve or deliberately move focus after a swap, modal action, or validation failure. Do not strand keyboard users in replaced content.
- Announce meaningful dynamic updates with an appropriate live region without making routine updates noisy.
- Preserve visible focus indicators, sufficient contrast, keyboard access, and reduced-motion preferences.
- Test representative flows with keyboard-only navigation. Include accessibility acceptance criteria in the feature brief.

## Templates And Presentation

- Keep templates presentation-focused. They may format supplied data and select included fragments; they must not query the database, calculate policy, or decide permissions.
- Build a small, documented base template and component vocabulary. Avoid a global template tag library that becomes an untyped application layer.
- Use Django's `{% translate %}` and `{% blocktranslate %}` tags for user-visible text. Translate complete messages with meaningful placeholders and pluralization rather than concatenating fragments.
- Use Django's automatic escaping. Mark content safe only after it is generated from controlled markup or sanitized for its exact output context.
- Use template inheritance for shared page structure and includes for repeated fragments. Do not create deeply nested inheritance chains that obscure the rendered result.
- Provide empty, loading, error, and permission-denied states for user-visible collections and workflows.
- Set the document language and direction from the active locale. Prefer CSS logical properties and allow for translated text expansion; test a representative right-to-left locale when one is enabled.

## Static Assets And Performance

Use Django's static-files pipeline and a documented production static-file strategy. Choose a CSS approach per project; do not make a CSS framework a template-wide requirement. Optimize images, use cursor-based navigation for every collection, and profile database queries before considering additional infrastructure. See [Performance and pagination](performance-and-pagination.md) for query and request-timing guidance.

Cache only after defining ownership, invalidation, personalization, and failure behavior. Cache keys must include every input that affects the representation, including locale or permission context where relevant.
