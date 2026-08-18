# Architecture

## Default Shape

Build a modular monolith. One Django deployment and one PostgreSQL database provide the default operational model. Modules align with business capabilities such as accounts, billing, catalog, or scheduling, not technical categories such as `views` or `utils`.

Each module may use a light hexagonal structure when its business rules warrant it:

```text
src/
  config/                         # Settings, root URLs, ASGI/WSGI
  modules/
    scheduling/
      application/                # Commands, queries, use cases, ports
      domain/                     # Entities, value objects, policies
      infrastructure/             # ORM mappings, repositories, gateways
      web/                        # Views, forms, URLs, templates, HTMX adapters
      apps.py
      tests/
```

Django convention files such as `models.py` or `admin.py` may be thin adapters or re-exports when the framework needs them. They must not become a second home for business logic.

Do not split a module into these directories simply because the layout exists. A small CRUD module can start with colocated view, form, query, and model code, then separate only when behavior becomes difficult to reason about. The dependency direction still applies.

## Layer Responsibilities

| Layer | Owns | Does not own |
| --- | --- | --- |
| Web | HTTP, URLs, forms, templates, HTMX responses, request parsing | Business decisions, transactions, direct cross-module writes |
| Application | Use cases, commands, queries, transaction boundaries, orchestration, port calls | HTTP objects, template rendering, ORM implementation details |
| Domain | Invariants, value objects, entities, policies, meaningful events | Django imports, database queries, HTTP, external SDKs |
| Infrastructure | ORM persistence, external clients, cache, storage, email, tasks | Product workflow decisions or authorization policy hidden in adapters |

Dependencies point inward: web and infrastructure depend on application and domain; application depends on domain and abstract ports; domain depends only on the Python standard library or narrowly justified pure-Python packages.

## Use Cases And Transactions

Model important state changes as named application commands, for example `ScheduleAppointment`, `CancelBooking`, or `ApproveExpense`. A command should have typed input, execute a coherent business operation, and return a typed result or a known business failure.

Start a database transaction at the application boundary when several writes must succeed together. Use database constraints for invariants the database can enforce. Use `select_for_update()` only where concurrency analysis shows a real write race; explain the protected invariant in a nearby comment or test.

Views translate request data into form or command input, invoke the use case, and choose a response. They do not implement a second version of the workflow.

## Persistence And Queries

- Django ORM models are persistence representations. Keep framework-independent business logic out of them when the model represents a meaningful domain concept.
- Keep model validation useful, but do not assume `Model.save()` or `Model.clean()` is called by every data path. Enforce critical invariants in application/domain behavior and database constraints.
- Use repository ports only when a use case needs to be independent of persistence, the persistence strategy varies, or the query is sufficiently complex. Do not wrap every `QuerySet` in a repository.
- Read-only pages may use optimized ORM query services or projections directly from the application layer. Keep filtering and authorization explicit.
- Avoid N+1 queries by choosing `select_related`, `prefetch_related`, projections, cursor pagination, and query-count assertions where material.
- Use cursor/keyset navigation for every collection query. Define a stable ordering, a unique tie-breaker, a bounded page size, and an index that supports the query. See [performance and pagination](performance-and-pagination.md).
- Prefer foreign keys and database constraints to application-only references. Specify `on_delete` behavior deliberately.
- Cross-module writes go through the target module's application API rather than importing its ORM model and mutating it opportunistically.

## Events And Background Work

Use synchronous commands first. Add a background worker only when a task is slow, retryable, scheduled, or must survive the request lifecycle.

If a successful database write must trigger asynchronous work, record the intent transactionally using an outbox-like pattern before relying on a worker. Do not dispatch a task before the transaction commits. Make task handlers idempotent and observable.

Domain events are useful for decoupling meaningful business facts. They are not a replacement for simple direct function calls inside a small module, and they do not imply an event-driven architecture.

## Errors And Boundaries

Expected business failures use typed results or narrow exceptions that the web layer maps to a user-appropriate response. Validation failures remain close to forms or input parsing. Unexpected failures are logged with safe context and allowed to reach central error reporting.

Do not return raw exceptions, tracebacks, model internals, or provider error messages to users. Do not use broad `except Exception` blocks unless the code logs, preserves context, and has a defined recovery behavior.

## When To Extract A Service

Keep a capability in the modular monolith unless it needs an independent deployment cadence, distinct scaling profile, isolated security or compliance boundary, or ownership by a separately operating team. Network boundaries add latency, observability, failure, data-consistency, and deployment costs. Record a decision before introducing one.
