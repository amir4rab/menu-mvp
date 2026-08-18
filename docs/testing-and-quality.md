# Testing And Quality

## Testing Strategy

Test behavior at the lowest boundary that provides meaningful confidence. Do not duplicate the same assertion across every test layer.

| Test level | Purpose | Typical examples |
| --- | --- | --- |
| Domain unit | Prove invariant and policy behavior without Django | value-object rules, pricing, state transitions |
| Application | Prove a use case coordinates permissions, transaction work, and ports | scheduling, cancellation, approval workflows |
| Integration | Prove adapters work with Django and PostgreSQL | ORM constraints, repository queries, email/storage adapters |
| Web | Prove URLs, forms, rendering, redirects, permissions, and HTMX fragments | user-visible workflow and error paths |
| Browser | Prove a few critical end-to-end flows in a real browser | sign-in, high-value submission, accessible interactive UI |

Use `pytest` and `pytest-django`. Keep tests deterministic, isolated, readable, and fast enough for routine local use. Factories are usually preferable to large shared fixtures; fixtures may be used for stable reference data or integration contracts.

## What To Test

- Test business rules, state transitions, permissions, validation errors, not-found behavior, and side effects.
- Test database constraints and concurrency-sensitive rules at integration level. Application-only checks are not sufficient for data integrity.
- Test every write path for an unauthorized actor and an actor authorized for a different object or tenant.
- Test standard and HTMX representations for workflows where both are supported.
- Test the default locale and representative non-default locales for translated labels, validation messages, context, pluralization, locale-aware formatting, and documented fallback behavior.
- Test public locale-prefixed URLs and private session or cookie locale selection, including redirects and HTMX fragments. Test right-to-left direction and keyboard interaction when an RTL locale is enabled.
- Test cursor-based collections at the first, middle, and final pages, including equal primary sort values, invalid or stale cursors, changed filters, changed sort direction, empty results, and maximum page sizes.
- Add query-count or query-shape assertions where a collection's database behavior is important, and verify request-duration log fields when logging is part of the feature contract.
- Test redirects, messages, and response status only when they are user or client contracts; avoid brittle assertions about incidental markup.
- Add regression coverage for every fixed production defect when it can be reproduced safely.
- Add browser tests for the small number of workflows whose breakage would materially harm users or revenue. Do not use browser tests as the only test layer.

## Test Data And External Effects

- Use fictional, minimal data. Never copy production personal data into local fixtures or CI.
- Freeze time or inject a clock for time-sensitive behavior. Make random values deterministic in tests.
- Use fakes for application ports when testing application behavior, and contract/integration tests for real adapters.
- Do not send real email, charge payments, call production APIs, or enqueue uncontained background work in tests.
- Test asynchronous handlers for idempotency and safe retry behavior when background work exists.

## CI Quality Gates

CI is required for consultancy projects and should run on every pull request. Its baseline gates are formatting, linting, static typing, automated tests, migration consistency, and production deployment checks with safe test settings.

Add a PostgreSQL-backed test job when database behavior, constraints, indexes, locking, or PostgreSQL-specific queries matter. SQLite is not a substitute for PostgreSQL behavior. Add dependency scanning through the repository host or an approved scanner, and review findings rather than blindly suppressing them.

Coverage is a signal, not a target to game. Set coverage thresholds only after the project has a meaningful baseline. Review untested risk, especially authorization, money, destructive actions, and migration code.

## Code Review Checklist

- The feature brief and acceptance criteria are satisfied.
- The change has a clear module owner and respects architecture boundaries.
- Inputs, permissions, errors, and external side effects are handled explicitly.
- Tests cover the relevant successful, invalid, unauthorized, and failure paths.
- Database query behavior and migrations are appropriate for expected data volume.
- Collection navigation is cursor-based, bounded, and backed by an appropriate stable ordering and index.
- New UI is accessible and works with normal form navigation where required.
- User-facing text is translation-ready, locale-sensitive formatting is correct, and enabled translation catalogs compile.
- Request logs contain safe route, status, correlation, and duration fields where request timing is required.
- Logs and error reporting support diagnosis without exposing sensitive data.
- Dependencies, settings, documentation, and rollout steps are reviewed when changed.
