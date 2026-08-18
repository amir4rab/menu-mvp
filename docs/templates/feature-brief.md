# Feature Brief: <title>

**Status:** Draft | Ready | In progress | Shipped

**Owner:** <name or team>

**Date:** <YYYY-MM-DD>

## Problem And Outcome

Describe the user problem, the intended outcome, and how the team will know it is successful.

## Scope

**In scope:**

- <behavior>

**Out of scope:**

- <behavior intentionally excluded>

## Users And Authorization

| Actor | Allowed actions | Explicitly not allowed |
| --- | --- | --- |
| <role> | <actions> | <actions> |

State object-level rules, tenant boundaries, sensitive data handling, and audit requirements.

## User Flow And Acceptance Criteria

1. Given <starting state>, when <action>, then <observable outcome>.
2. Given <invalid or exceptional state>, when <action>, then <safe outcome>.
3. Given <unauthorized actor>, when <action>, then <expected denial behavior>.

Note normal page behavior, HTMX fragments, no-JavaScript fallback, redirects, messages, localization, and accessibility requirements where they apply.

## Localization

**Default locale:** <locale>

**Supported locales:** <locale list; one locale is valid for an initial release>

**Fallback and negotiation:** <behavior for unsupported locales, browser preferences, saved preferences, and the default>

**Locale selection:** <URL prefixes for public cacheable pages; session/cookie behavior for private pages>

**Translation impact:** <new messages, catalogs, placeholders, pluralization, persisted content, and release workflow>

**RTL impact:** <none, or layout/components/tests affected by right-to-left locales>

## Performance And Pagination

**Collection behavior:** <None | collection or result set affected>

**Pagination strategy:** <cursor/keyset ordering and cursor state>

**Ordering and index:** <stable ordering, unique tie-breaker, and supporting index>

**Page-size limit:** <maximum page size and empty/end-of-list behavior>

**Query and request timing:** <query-shape risks, N+1 concerns, and `duration_ms` logging expectations>

## Technical Design

**Owning module:** <bounded context>

**Application command/query:** <name>

**Domain rules or invariants:**

- <rule>

**Interfaces and integrations:**

- <form, URL, external system, email, task, or API>

**Data change:** None | <schema/data description>

**Configuration or operational change:** None | <description>

**Localization change:** None | <locale, catalog, formatting, selection, or translated-content description>

**Performance change:** None | <pagination, query, index, response-size, or request-timing description>

## Risks And Rollout

Describe authorization, privacy, migration, concurrency, performance, failure, and user-support risks. State the rollout, monitoring, and roll-forward or rollback plan if the change is not trivially reversible.

## Test Plan

- <domain/application behavior>
- <authorization and validation cases>
- <integration or database behavior>
- <web or HTMX behavior>
- <manual accessibility or operational verification>

## Agent Handoff

List relevant files, decisions, constraints, prohibited approaches, and commands required to validate the work.
