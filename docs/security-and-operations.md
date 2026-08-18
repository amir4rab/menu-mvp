# Security And Operations

## Identity And Authorization

Create the project's custom user model before the first migration and configure `AUTH_USER_MODEL` from the start. Use Django session authentication for the SSR application unless a documented requirement selects an external identity provider.

Use Django groups and permissions as the baseline role mechanism. For object-level decisions, define a policy in the owning module that answers whether a specific actor may perform a specific action on a specific object. Do not depend solely on template visibility, URL naming, or broad role checks.

- Restrict querysets by actor or tenant before object retrieval where possible.
- Recheck authorization before sensitive state changes, especially when data can change between page render and submission.
- Use password reset, email verification, session invalidation, rate limiting, and MFA according to the product's risk model.
- Record security-relevant actions where auditability is required: actor, action, target, outcome, timestamp, and safe request context.
- Define who can create privileged users and how access is removed before production launch.

## Django Security Baseline

Enable Django's production security settings over HTTPS: secure session and CSRF cookies, HTTPS redirect where the proxy arrangement supports it, `SECURE_PROXY_SSL_HEADER` only behind a trusted proxy, appropriate HSTS after HTTPS is verified, and secure allowed-host configuration.

Keep CSRF middleware and template autoescaping enabled. Set clickjacking protection and a reviewed Content Security Policy. Configure uploads with explicit type, size, storage, access-control, malware-scanning, and retention decisions. Never trust an uploaded filename or browser-supplied MIME type.

Run `manage.py check --deploy` against production-like settings before a release. This is a baseline check, not a complete security review.

## Secrets And Privacy

Store secrets in the deployment environment or an approved secret manager. The repository contains only variable names and safe placeholders. Rotate exposed credentials immediately and treat the incident as a security event.

Collect the minimum personal data required for the product. Document data purpose, access, retention, deletion, export, and processor obligations when personal or regulated data is involved. Avoid sensitive values in analytics, logs, URLs, error reporting, and support screenshots.

## Logging, Errors, And Health

Use structured application logs and centralized error reporting in non-development environments. Include a correlation or request ID that can follow a request through logs and asynchronous work, and include safe request duration when diagnosing endpoint performance. Redact secrets, raw query strings, cursor contents, and sensitive fields before they reach any logging or monitoring provider.

Provide two health concepts when operational infrastructure needs them:

- A liveness check verifies that the process can respond and must not require external dependencies.
- A readiness check verifies the dependencies required to serve traffic, with bounded timeouts and no disclosure of sensitive topology.

Alert on user-impacting failures, error-rate changes, and unavailable critical dependencies. Prefer actionable alerts over dashboards that nobody owns. Define an owner and runbook for every production alert.

## Operational Baseline

Consultancy projects use PostgreSQL, Docker Compose for reproducible local services, CI, a documented deployment command or pipeline, and a production process manager appropriate to the chosen host. The deployment strategy remains provider-neutral unless an engagement requires otherwise.

Back up production databases, encrypt backups, restrict restoration access, and periodically test restoration. Document recovery expectations for database loss, accidental deletion, and a failed release. Apply least privilege to database and deployment credentials.

Use timeouts and bounded retries for outbound network calls. Make externally visible operations idempotent where users, workers, or providers may retry them. Track failures that require manual reconciliation.
