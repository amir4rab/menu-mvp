# Feature Brief: Basic Authentication

**Status:** Shipped

**Owner:** menu-mvp

**Date:** 2026-08-19

## Problem And Outcome

The project has no accounts layer. The engineering baseline requires a custom user model before the first migration, and the product needs username/password authentication so users can identify themselves. Outcome: a visitor can sign up, log in, and log out, and the home page reflects the session state.

## Scope

**In scope:**

- Custom `User` model (`AbstractUser` subclass) configured as `AUTH_USER_MODEL` before any migration exists.
- Registration with username and password (Django's password validators applied).
- Login with username and password, honoring a safe `next` redirect.
- Logout via POST (GET is unsupported since Django 6.0).
- Minimal home page as the post-auth landing destination.

**Out of scope:**

- Password change/reset and email flows.
- Profile pages, `@login_required` product content, roles/groups.
- Rate limiting, MFA, email verification.
- Quality tooling setup (ruff, mypy, pytest, django-stubs) and production settings module.

## Users And Authorization

| Actor | Allowed actions | Explicitly not allowed |
| --- | --- | --- |
| Anonymous visitor | View home, sign up, log in | Log out, access no other product content (none exists yet) |
| Registered user | View home, log in, log out | Any manage/admin action outside Django admin permission rules |

Sessions use Django's cookie-based session authentication with CSRF protection enabled. There are no object-level permissions in this slice.

## User Flow And Acceptance Criteria

1. Given an anonymous visitor, when they sign up with a valid unique username and matching allowed passwords, then a user is created, the visitor is logged in, and they are redirected to the home page showing their username.
2. Given any visitor, when they submit a duplicate username, mismatched passwords, or an invalid password (too common/short/numeric), then the form shows the corresponding Django validation error and no account is created.
3. Given a registered user, when they log in with the wrong password or an unknown username, then the login form shows an error and no session is created.
4. Given a logged-in user, when they submit the logout POST form, then they are logged out and redirected to the public home page; a GET to the logout URL returns 405.
5. Given an anonymous visitor, when they log in with valid credentials, then they are redirected to `LOGIN_REDIRECT_URL` (or the validated `next` parameter).

## Localization

**Default locale:** en

**Supported locales:** en

**Fallback and negotiation:** Django default; missing translations fall back to source strings.

**Locale selection:** Session-only private pages; public pages plain (no locale prefixes yet).

**Translation impact:** All user-visible strings use `{% translate %}` / `{% blocktranslate %}` tags and `gettext_lazy` where Python-side. No catalogs generated yet; single enabled locale.

**RTL impact:** none currently.

## Performance And Pagination

**Collection behavior:** None.

## Technical Design

**Owning module:** accounts (`menu_mvp.accounts`)

**Application command/query:** none; Django auth forms and views used directly (`LoginView`, `LogoutView`, `UserCreationForm` subclass `SignupForm`).

**Domain rules or invariants:**

- Username unique, case-insensitive per `AbstractUser`.
- Password strength enforced by the configured `AUTH_PASSWORD_VALIDATORS`.

**Interfaces and integrations:**

- URLs: `/` home, `/accounts/login/`, `/accounts/logout/`, `/accounts/signup/`.
- Templates: `base.html`, `home.html`, `accounts/login.html`, `accounts/signup.html`.
- Static: `css/base.css` (no CSS framework, per project sizing).
- Admin: custom `User` registered with `UserAdmin`.

**Data change:** New `accounts_user` table via initial migration `0001_initial` (project's first migration).

**Configuration or operational change:** `AUTH_USER_MODEL`, `INSTALLED_APPS`, `LOGIN_URL`/`LOGIN_REDIRECT_URL`/`LOGOUT_REDIRECT_URL`, template `DIRS`, `LANGUAGES` + `LocaleMiddleware` (i18n baseline).

**Localization change:** `LANGUAGES` and `LocaleMiddleware` added per the internationalization baseline.

**Performance change:** None.

## Risks And Rollout

- `AUTH_USER_MODEL` is irreversible after the first migration without a data migration; it is set now while the database is empty and no migrations exist.
- No rate limiting on login/signup in this slice; flag for the risk-model review before production launch.

## Test Plan

- Signup: success and auto-login; duplicate username; mismatched passwords; common password; GET renders form.
- Login: valid credentials + `next` handling; wrong password; unknown username; GET shows form without a session.
- Logout: POST-only requirement and redirect; GET returns 405.
- Home page: public, shows username when authenticated.

## Agent Handoff

Relevant files: `config/settings.py`, `config/urls.py`, `src/menu_mvp/accounts/*`, `src/menu_mvp/templates/*`, `src/menu_mvp/static/css/base.css`.

Validation commands:

```bash
uv run python manage.py test
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py check
```

Commands that cannot run (tooling not installed): `uv run ruff format --check .`, `uv run ruff check .`, `uv run mypy .`, `uv run pytest`.