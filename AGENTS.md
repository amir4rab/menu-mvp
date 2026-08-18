# Agent Instructions

These rules apply to every code or documentation change made in a project created from this template. They are intentionally platform-neutral and should be followed by human contributors as well as coding agents.

## Operating Rules

1. Read the relevant feature brief, architecture decision records, nearby code, tests, and project conventions before proposing or making a change.
2. Clarify conflicting requirements, missing acceptance criteria, data-retention needs, authorization behavior, and external side effects before implementation. Do not guess on security-sensitive behavior.
3. Keep changes small and vertically complete. Include the behavior, authorization, tests, documentation, and migration plan that the change requires.
4. Do not introduce a dependency, framework, service, abstraction, compatibility layer, or background process without a concrete requirement and a documented reason.
5. Preserve backward compatibility for existing users, URLs, data, integrations, and background work unless a reviewed migration or removal plan says otherwise.
6. Never add credentials, real personal data, production exports, or secrets to the repository, logs, fixtures, examples, or error messages.
7. Keep user-facing text translation-ready and locale-sensitive presentation correct from the first feature, even when a project initially enables one locale.
8. Report what changed, how it was verified, and every validation command that could not be run.

## Delivery Workflow

1. For substantial work, create or update a feature brief using `docs/templates/feature-brief.md`.
2. Identify the owning bounded context and the affected interface, application, domain, and infrastructure boundaries.
3. State the expected behavior, authorization rule, validation failures, data change, observability, and tests before coding.
4. Implement the smallest coherent vertical slice. Do not mix unrelated cleanup into feature work.
5. Run the required quality checks and inspect migrations before completion.
6. Update an architecture decision record when a decision is costly to reverse or sets a project-wide pattern.

## Architecture Boundaries

- The web layer owns HTTP, URLs, views, forms, template context, response headers, and HTMX request handling. It must not own business rules or persistence orchestration.
- The application layer owns use cases, transaction boundaries, authorization coordination, and calls to ports. It accepts typed inputs rather than `HttpRequest` objects.
- The domain layer owns business invariants, value objects, entities, policies, and domain events when they are useful. It must not import Django, ORM models, or external clients.
- The infrastructure layer owns Django ORM models, repositories, external APIs, email, storage, cache, task queues, and framework adapters.
- Simple CRUD does not require ceremonial domain objects or repository interfaces. Use the simplest design that preserves clear permissions, validation, tests, and future changeability.
- Do not hide writes in model signals, overridden `save()` methods, template tags, admin actions, or request middleware. Use explicit application commands instead.

## Security and Data Boundaries

- Use the configured custom user model through `settings.AUTH_USER_MODEL` and `get_user_model()`. Never reference Django's default user model directly.
- Authorize every action against both the actor and target object. Login status or a hidden UI control is not authorization.
- Scope querysets to the authorized actor before retrieving objects where possible. Apply a second explicit permission check before sensitive mutations.
- Treat identifiers from routes, forms, headers, webhooks, and external APIs as untrusted input. Validate and normalize them at the boundary.
- Keep CSRF protection enabled for browser session requests. Preserve Django autoescaping and use safe HTML only for reviewed, generated markup.
- Do not log passwords, tokens, session identifiers, full payment data, health details, or unnecessary personal data.

## Migration and Release Boundaries

- Generate migrations with Django, inspect the generated operations and SQL impact, and commit them with the code that needs them.
- Do not edit a migration that has run outside disposable local environments. Create a follow-up migration instead.
- Flag destructive schema changes, large backfills, table-rewriting operations, new non-concurrent PostgreSQL indexes, and irreversible migrations for human review before execution.
- Prefer a tested roll-forward plan. A database rollback is safe only when its data and compatibility consequences are understood.

## Required Validation

Use the project's exact commands. A newly instantiated project should provide equivalents of the following:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py check --deploy --settings=<production-settings-module>
```

Run focused tests during development and the full relevant suite before completion. If infrastructure-dependent checks cannot run locally, state the reason and verify the closest safe alternative.

## Human Approval Required

Request explicit review before merging or deploying changes that:

- change authentication, authorization, session behavior, password handling, or identity-provider behavior;
- handle payments, regulated data, deletion/retention, exports, or security incidents;
- add a production dependency, third-party SDK, external webhook, or background worker;
- perform a destructive, long-running, or data-transforming migration;
- change public contracts, production configuration, backups, or deployment behavior.

## Definition Of Done

A change is complete only when its behavior and failure modes are covered by appropriate tests, permissions are enforced server-side, types and formatting pass, migrations are reviewed, user-visible accessibility impacts are considered, operational failures are observable, and documentation is updated where it changes project behavior.
