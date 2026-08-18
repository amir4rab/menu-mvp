# Performance And Pagination

Performance guidance is evidence-led. Every collection must have bounded work and predictable navigation, but the template does not require a cache, worker, search service, tracing platform, or other infrastructure without a demonstrated need.

Use cursor/keyset navigation for every collection endpoint and page. Do not use offset or page-number pagination as an alternative. If a workflow appears to require arbitrary page jumps, redesign the workflow around stable next/previous navigation or another cursor-compatible interaction rather than scanning past an unbounded number of rows.

## Cursor Navigation

Every cursor-based collection must define:

- A stable, deterministic ordering.
- A unique tie-breaker when the primary ordering value is not unique, such as `(created_at, id)`.
- An index that supports the filters and ordering used by the query.
- An opaque cursor that carries or validates the relevant ordering and filter state.
- A bounded maximum page size controlled by the server.
- Clear behavior for an empty collection, the first page, the final page, and an exhausted cursor.

Apply authorization and filters before the cursor boundary. The next cursor must refer to the same authorized result set and sort order as the current page. Do not trust cursor values from the browser; validate their shape, allowed fields, direction, and relationship to the current request.

Fetch at most one more record than the requested page size to determine whether another page exists. Do not run an exact `COUNT(*)` on every request solely to render navigation unless the product explicitly needs that count and the query cost is understood.

Preserve filters, sort state, locale, and relevant form state in normal links and HTMX requests. Invalid, stale, or incompatible cursors should produce a safe validation response rather than an unbounded fallback query.

## Query Shape

- Scope the queryset by actor, tenant, and other authorization boundaries before applying pagination.
- Select only the fields required by the response when a projection materially reduces database or serialization work.
- Use `select_related()` and `prefetch_related()` deliberately to prevent N+1 queries, and verify the resulting query shape.
- Keep database access out of templates and presentation helpers.
- Add indexes for real filter and ordering combinations, and inspect their migration and write costs before deployment.
- Use PostgreSQL query plans and representative data when a collection is large, frequently accessed, or unexpectedly slow.
- Do not load an entire collection into memory to calculate a page, export a response, or render a count.

Cursor logic belongs in the application query or query-service boundary. Views translate request parameters, invoke that query, and render the result; templates only render the supplied page and navigation state.

## Request Timing

Record response duration in structured request logs at the web boundary. The baseline performance signal is the elapsed duration, preferably as `duration_ms`, alongside safe context such as:

- HTTP method and normalized route name.
- Response status.
- Request or correlation ID.
- Whether the response was a full page or an HTMX fragment when that distinction matters.

Do not log raw query strings, cursor contents, session identifiers, or unnecessary personal data. Log duration consistently enough to identify slow routes, then profile the specific view, query, or template before changing architecture. Request timing is a diagnostic signal, not a reason to introduce a monitoring platform or optimize without evidence.

## Tests And Review

Test the first, middle, and final cursor pages, including records with equal primary ordering values. Test empty results, maximum page sizes, invalid or stale cursors, changed filters, changed sort direction, and authorization changes between requests.

Add query-count assertions where a collection's query shape is important. Use integration tests with representative data for indexes and PostgreSQL-specific behavior. Test both complete-page and HTMX representations when both are supported, including preservation of navigation state.

Review request-duration logging for safe route names, useful status information, and absence of sensitive values. Do not set a universal latency target in the template; establish thresholds only when a product's traffic and user impact justify them.
