# Delivery And Migrations

## Delivery Workflow

Use short-lived branches and pull requests. Every substantial pull request links to a feature brief, describes user-visible behavior, lists configuration and migration effects, and states validation evidence. Keep unrelated refactors separate from behavior changes whenever possible.

Consultancy projects should provide a Docker Compose environment that uses the same major PostgreSQL version as production, avoids storing secrets in images, and exposes only required development ports. Document the normal local commands in the generated project's README.

CI runs the quality gates in `docs/engineering-standards.md` and `docs/testing-and-quality.md`. Protect the default branch after the team has a stable CI baseline. Deployment credentials are never available to untrusted pull requests.

## Safe Django Migrations

Generate migrations with `makemigrations`, commit them alongside the application change, and review their operations before merge. Run `makemigrations --check --dry-run` in CI to ensure migrations are not missing.

Before deploying a migration, assess these questions:

- Does it lock, rewrite, scan, or copy a large table?
- Does an index need PostgreSQL concurrent creation, requiring a non-atomic migration and an operational plan?
- Does a new non-null field, default, unique constraint, or foreign key affect existing rows or write availability?
- Does it transform or delete data, and is that transformation batched, observable, restartable, and tested?
- Can both the previous and new application versions operate against the schema during the release?
- Is a backup available and has the team selected a safe roll-forward or rollback action?

For risky changes, prefer an additive sequence: introduce compatible schema, deploy code that supports it, backfill in controlled batches, verify, switch reads/writes, then remove obsolete schema in a later release. This is a safety technique, not a requirement to claim zero downtime.

Do not edit a migration that has run in shared, staging, or production environments. Do not use a reverse migration as an automatic recovery plan when data may have changed incompatibly. Rolling forward with a corrective migration is often safer.

## Data Migrations

Treat data migrations as production programs. Keep them isolated from incidental schema changes, use historical models supplied by Django migrations, process in batches, avoid network calls, record progress where restartability is needed, and estimate their runtime on representative data.

For exceptional large transformations, use a management command or separately operated job rather than a migration when that provides better observability, throttling, and recovery. Document the execution order and completion criteria in the release notes.

## Release Checklist

- CI is green, dependencies are locked, and deployment settings are validated.
- Migrations and their PostgreSQL impact have been reviewed and rehearsed when risk warrants it.
- Backup status, rollback or roll-forward plan, and responsible operator are known.
- Required environment variables, static assets, workers, and scheduled tasks are accounted for.
- Translation catalogs are compiled and the enabled locales, locale selection, and representative localized user journey have been verified.
- Health checks, logs, error reporting, and alert ownership are active.
- User-facing changes, support impact, and any manual post-deploy action are recorded.
- After release, verify the critical user journey and watch errors and key operational signals.
