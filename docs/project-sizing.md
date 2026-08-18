# Project Sizing

This template optimizes for consultancy projects with a small to medium delivery team, changing requirements, and an expectation of production support. The goal is proportionate rigor: reduce operational burden for a solo project without discarding the practices that prevent expensive failures.

## Always Keep

The following practices are mandatory at every size:

- Python 3.13, `uv`, and a committed lockfile.
- Formatting, linting, strict type checking, and automated tests.
- A custom user model before the first migration.
- Server-side authorization, CSRF protection, safe configuration, and secret hygiene.
- Translation-ready user-facing text and locale-aware presentation, even when only one locale is enabled initially.
- Reviewed migrations and a tested database backup approach before production use.
- Clear module ownership, explicit business rules, and a small feature brief for meaningful work.
- Error reporting or a practical way to discover production failures.

## Consultancy Default

Use these by default when delivering to a client or supporting a shared production system:

| Capability | Why it is the default |
| --- | --- |
| PostgreSQL in local, CI where relevant, and production | Avoids environment-specific database behavior |
| Docker Compose | Reproducible developer onboarding and support environments |
| Pull-request CI | Prevents regressions across changing contributors |
| Staging or a production-like verification environment | Reduces client-facing deployment risk |
| Structured logs and centralized error reporting | Supports handover and incident diagnosis |
| Release and migration checklist | Makes operational risk visible before deployment |
| Architecture decision records | Preserves context through staff and client changes |
| Dependency and security scanning | Detects known supply-chain risk |

## Solo Project Reductions

A solo developer may simplify the following when the product risk is low and the owner accepts the trade-off:

| Capability | Acceptable reduction | Do not reduce when |
| --- | --- | --- |
| Local database | SQLite for early local iteration | PostgreSQL-specific behavior, multiple contributors, or a production launch is near |
| Docker Compose | Documented local `uv` setup | Onboarding others, maintaining several services, or reproducing support issues |
| CI | Run the same checks locally, then add CI before collaboration or launch | The repository accepts outside contributions or deploys frequently |
| Staging | Test a defined release checklist in a controlled production window | Data migrations, payment changes, or complex integrations are involved |
| Observability | Basic managed error reporting and logs | Users depend on availability or background work can fail silently |
| ADRs | Keep decisions in concise issue or README notes | A decision affects multiple modules, vendors, or future contributors |
| Browser tests | Test critical flows manually and retain lower-level automation | An HTMX workflow is revenue-critical or repeatedly regresses |

These reductions are deliberate temporary choices. Record the chosen boundary and the signal that will require restoring the consultancy default.

## Add Only When A Signal Exists

| Capability | Add it when |
| --- | --- |
| Redis/cache | Measurements show repeated expensive reads and invalidation can be owned |
| Background worker and scheduler | Work is slow, retryable, scheduled, or must survive a request |
| Object-permission package | A simple explicit policy cannot express the required scale or relationship rules |
| Multi-tenancy framework | Tenant isolation, provisioning, billing, or branding has concrete requirements |
| Search service | PostgreSQL search cannot meet measured relevance, scale, or filter needs |
| Event broker | Independently operated consumers or durable asynchronous integration is required |
| Distributed tracing and metrics platform | Multiple services or frequent performance incidents need cross-system diagnosis |
| Cloud-specific IaC | Hosting is stable enough that repeatable account-level infrastructure has clear value |

Add the capability with an owner, operational runbook, local development story, test strategy, cost estimate, and removal or migration consideration.
