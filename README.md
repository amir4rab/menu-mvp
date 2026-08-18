# Agentic Django SSR Template

This repository is a documentation-first template for building small and medium Django applications with server-side rendering (SSR). It is intended primarily for consultancy projects that need strong engineering defaults without prematurely becoming distributed systems.

It defines how people and coding agents should build a Django application. It deliberately does not include a runnable application, cloud account, or deployment-specific infrastructure. Create those after the project has clarified its domain, users, and hosting constraints.

## Default Stack

| Area | Default |
| --- | --- |
| Python | Python 3.13 |
| Dependency management | `uv`, with the lockfile committed |
| Web framework | Current supported Django LTS or stable release approved for the project |
| Rendering | Django Templates, progressively enhanced with HTMX |
| Internationalization | Django translation and localization support enabled from the first commit; one or more configured locales |
| Architecture | Modular monolith with proportional hexagonal/DDD boundaries |
| Database | PostgreSQL outside isolated local experimentation |
| Local environment | Docker Compose for consultancy projects |
| Quality | Ruff, MyPy strict mode with Django stubs, pytest and pytest-django |
| Delivery | Pull requests, CI, reviewed migrations, environment-driven settings |
| Identity | A custom user model from the first migration, Django sessions, groups and permissions |

## How To Use This Template

1. Create a repository from this template and rename it for the product.
2. Read [AGENTS.md](AGENTS.md) before asking an agent to make changes.
3. Read [the architecture guide](docs/architecture.md), then choose bounded contexts and record material choices using [an architecture decision record](docs/templates/architecture-decision-record.md).
4. Establish the Python project with `uv`, Django, PostgreSQL, the quality tools, and the CI checks in [the engineering standards](docs/engineering-standards.md).
5. Start each substantial feature from [the feature brief](docs/templates/feature-brief.md).
6. Apply the delivery, security, and sizing guidance before the first production deployment.

## Principles

- Favor a modular monolith over services until an independently deployable boundary has a demonstrated benefit.
- Keep HTML as the primary application interface. HTMX improves interactions; it does not create a second client application.
- Put business rules in explicit application and domain code, not in views, templates, signals, or admin actions.
- Prefer boring, well-supported Django and PostgreSQL features over bespoke abstractions.
- Make types, tests, authorization, schema migrations, logs, and configuration part of normal feature work.
- Use bounded cursor-based collection navigation and request-duration logging before considering additional performance infrastructure.
- Keep user-facing text translation-ready and presentation locale-aware from the first commit, even when the initial release has one locale.
- Scale process and infrastructure with project risk, not team anxiety. See [project sizing](docs/project-sizing.md).
- Give agents narrow, verifiable tasks and require the same evidence expected from a human contributor.

## Documentation Map

| Document | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Mandatory workflow and constraints for coding agents and contributors |
| [Architecture](docs/architecture.md) | Modular-monolith, hexagonal/DDD boundaries, and data-access guidance |
| [Django SSR and HTMX](docs/django-ssr-and-htmx.md) | Server-rendered UI, forms, HTMX, accessibility, and caching rules |
| [Internationalization](docs/internationalization.md) | Translation, locale selection, formatting, catalog workflow, and RTL readiness |
| [Performance and pagination](docs/performance-and-pagination.md) | Cursor navigation, bounded queries, query shape, and request-duration logging |
| [Engineering standards](docs/engineering-standards.md) | Python, typing, configuration, dependencies, tests, and quality gates |
| [Testing and quality](docs/testing-and-quality.md) | Test levels, test-data rules, CI gates, and review expectations |
| [Security and operations](docs/security-and-operations.md) | Identity, authorization, security settings, logging, health, and operations |
| [Delivery and migrations](docs/delivery-and-migrations.md) | Git workflow, Docker/CI baseline, safe PostgreSQL changes, and releases |
| [Project sizing](docs/project-sizing.md) | What stays mandatory and what can be reduced for solo projects |
| [Feature brief](docs/templates/feature-brief.md) | Feature definition and agent handoff template |
| [Architecture decision record](docs/templates/architecture-decision-record.md) | Lightweight record for consequential technical decisions |

## Non-Goals

This template does not prescribe a cloud provider, CSS framework, task queue, cache, event broker, multi-tenancy strategy, API framework, or frontend build tool. Adopt one only when a product requirement justifies its cost and document the decision.

The template also does not promise zero-downtime deployments. It requires safe, reviewed migrations and operationally honest release plans instead.
