# Internationalization

Every instantiated project must be ready for internationalization from its first commit. A first release may enable only one locale, but user-facing text, formatting, routing, and templates must not make adding another locale require a rewrite.

Use Django's built-in internationalization and localization features unless a concrete product requirement justifies another approach. Do not add a translation service or third-party package merely because a project may need more languages later.

## Baseline

At project start, record:

- The default locale.
- The supported locales, even when the initial list contains only one locale.
- The fallback and missing-translation behavior.
- Which public URLs use locale prefixes and which private workflows use a session or cookie locale.
- Whether persisted product content is translated, or remains in its source language.

The baseline requires the following:

- Every user-visible string in templates, Python code, forms, validation messages, emails, and HTMX fragments is translation-ready.
- Dates, numbers, percentages, decimal values, and other locale-sensitive presentation use Django's locale-aware formatting rather than hand-built strings.
- Translation context and pluralization are preserved when the meaning or grammatical form depends on them.
- The active locale is represented consistently in the complete page, forms, redirects, and HTMX responses.
- Layouts remain usable when translated text is longer than the source text and when an enabled locale uses right-to-left text.

Do not silently translate user-generated or domain content. If product content must exist in several languages, define its ownership, storage model, editorial workflow, fallback behavior, and tests in a feature brief or architecture decision record.

## Django Configuration

Use Django's native translation stack:

- Set `USE_I18N = True` and define `LANGUAGE_CODE` and `LANGUAGES` explicitly in settings.
- Add `LocaleMiddleware` in the documented Django order: after session middleware and before common middleware.
- Use `i18n_patterns()` for locale-prefixed public URL patterns and Django's built-in `set_language` view with session or cookie persistence for private workflows.
- Store project-level catalogs under the documented `LOCALE_PATHS`, or use each app's conventional `locale` directory.
- Keep source translation catalogs in the repository and generate compiled catalogs as part of the build or release process. Commit `.po` files; generated `.mo` and `.pot` files do not belong in source control unless a project has a documented reason to keep them.
- Use `gettext()` or `gettext_lazy()` in Python, and `{% translate %}` or `{% blocktranslate %}` in templates after loading Django's `i18n` tags.
- Use translation context and plural forms instead of concatenating translated fragments or interpolating untrusted HTML.
- Use Django's built-in language-selection view and middleware behavior as adapters for the chosen locale policy.

Generate and compile catalogs with Django's documented tooling, review messages for context and placeholders, and make catalog compilation part of CI or the release verification when translations are enabled. Missing translations should fall back according to the documented policy; they must not produce broken markup, untranslated security-sensitive instructions, or invalid formatted values.

## Locale Selection

Choose locale selection according to the visibility and caching model of the page:

- Public, cacheable pages use locale-prefixed URLs. The locale is explicit in links, redirects, canonical URL decisions, and cache keys.
- Private or authorized pages use a session or cookie locale. Do not put personalized responses in a shared cache without a reviewed strategy that accounts for locale, actor, and permission context.
- Define the negotiation order between an explicit URL, a saved user preference, a cookie or session value, the browser language, and the default locale.
- Validate requested locale identifiers against the configured language list and fall back safely for unsupported or malformed values.
- Show a language switcher only when more than one locale is enabled. It must preserve the user's current workflow where possible and remain usable with keyboard navigation and assistive technology.

The locale policy applies equally to normal requests and HTMX requests. A fragment must not unexpectedly reset the language or return text in a different locale from the page that requested it.

## Translation-Safe Presentation

Keep translation boundaries meaningful:

- Translate complete messages, not sentence fragments joined together in code or templates.
- Pass values through named placeholders and preserve their semantic meaning for translators.
- Use pluralization for counts and distinguish ambiguous terms with translation context.
- Keep user-provided values escaped and separate from translated markup.
- Avoid embedding text in images, CSS, JavaScript-only controls, or inaccessible icon-only actions.
- Use locale-aware Django formatting for presentation while keeping canonical values in stable storage formats.

Set the document `lang` and `dir` values from the active locale. Prefer CSS logical properties such as `margin-inline`, `padding-block`, and `inset-inline` over left/right assumptions. Verify navigation, forms, tables, notifications, modals, and HTMX swaps with a representative right-to-left locale when the project supports one.

## Tests And Operations

Test the default locale and representative non-default locales at the web boundary. Cover translated labels and errors, context-sensitive messages, pluralization, locale-aware formatting, fallback behavior, locale selection, redirects, and both full-page and HTMX responses.

When right-to-left locales are enabled, test direction-sensitive layout and keyboard interaction in a browser. Check that translation catalogs compile, placeholders remain valid, and the release process makes the required catalogs available to the application. Review user-facing changes for translation impact before release.
