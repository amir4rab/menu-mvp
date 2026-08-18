# Engineering Standards

## Python And Dependencies

Use Python 3.13 and `uv`. Declare runtime, development, and optional dependency groups in `pyproject.toml`; commit `uv.lock`. Pin the supported Python range deliberately and update dependencies in small, reviewable batches.

Use the current supported Django LTS or stable release selected at project start. Record exceptions to this baseline in an architecture decision record.

Before adding a package, verify that the standard library or Django does not already solve the problem, that the package is actively maintained, that its license is acceptable, and that it has a narrow, documented role. Remove unused dependencies instead of retaining them for hypothetical work.

## Types

Run MyPy in strict mode with `django-stubs` and `django-stubs-ext`. Annotate production function signatures, class attributes when inference is unclear, public application commands and queries, external integration payloads, and error-prone boundaries.

- Prefer `X | None` over `Optional[X]` in new Python 3.13 code.
- Prefer immutable `dataclass` value objects for structured domain inputs and outputs where they improve meaning.
- Use `Protocol` for a genuinely substitutable application port; do not create interfaces around one-off helpers.
- Do not silence type failures broadly. Isolate unavoidable untyped boundaries, validate their runtime shape, and explain narrow ignores.
- Do not use `Any` as a shortcut around an unclear model or integration contract.

Types supplement runtime validation. Browser, environment, database, and third-party inputs remain untrusted even when their Python annotations are precise.

## Formatting And Static Analysis

Ruff formats and lints all Python code. Configure the target version for Python 3.13 and make CI fail on formatting, lint, and type errors. Keep configuration in `pyproject.toml` so developers and agents run the same commands.

Use clear names and small cohesive functions. Comments explain non-obvious decisions, invariants, performance constraints, or external behavior; they do not restate code. Prefer explicit module ownership over a growing catch-all `utils` package.

## Configuration

Settings are environment-driven and validated at application startup. Separate development, test, and production configuration while keeping the settings structure understandable. Provide an `.env.example` containing names and safe example values only.

- Never default production `DEBUG`, secret keys, allowed hosts, databases, or email providers silently.
- Fail early for missing or invalid required production settings.
- Keep configuration parsing centralized and typed; application modules receive explicit settings or ports rather than reading environment variables ad hoc.
- Use separate credentials and databases for local, test, staging, and production environments.
- Treat feature flags as temporary product controls with owners and removal dates, not a replacement for release discipline.

Internationalization is part of the initial Django configuration. Define the default and supported locales, enable Django's built-in translation and localization features, and configure locale middleware before feature work begins. A project may start with one enabled locale, but templates, Python messages, forms, emails, and HTMX fragments must already be translation-ready. Follow [the internationalization guide](internationalization.md) for locale selection, catalog handling, formatting, and RTL behavior.

## Error Handling And Logging

Use form errors and typed business failures for expected outcomes. Log unexpected exceptions once at the most useful boundary with safe, structured context. Central error reporting captures unhandled failures in non-development environments.

Logs are structured and include timestamp, severity, event name, request or correlation ID, module/use-case name, and safe resource identifiers where useful. Request logs also include the normalized route, response status, and elapsed duration such as `duration_ms`. Do not include secrets, raw query strings, cursor contents, or unnecessary personal data. Make log messages useful for an operator who did not write the feature. Follow [performance and pagination](performance-and-pagination.md) for collection and request-timing guidance.

## Baseline Commands

Every instantiated project must expose the following checks through documented commands, normally via `uv run`:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py check --deploy --settings=<production-settings-module>
```

Run `ruff format .` only as a deliberate formatting change, then inspect the diff. A project may add commands for dependency auditing, template linting, browser tests, or migration linting when its risk profile justifies them.
