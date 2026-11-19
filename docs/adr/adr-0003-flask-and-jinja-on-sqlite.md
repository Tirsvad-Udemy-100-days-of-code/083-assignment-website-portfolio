# Serve the site with Flask and Jinja on top of SQLite

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0003 |
| CrossReference | [BC-001], [SA-001], [ADR-0002], [MIL-006] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version <br>Verdict Go (RC-032) | pending |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

[ADR-0002] chose SQLite through the standard library and a small server on `http.server` that renders HTML built from Python strings. S01 now wants the website to use Flask. Flask is what the idea repository uses and what course participants know, and it brings routing, error handling, static files and Jinja templates with autoescaping, so less web code has to be written and checked by hand. It also ends the earlier principle of no runtime dependency: S03's concern CN-008 becomes a one-command install with pinned dependencies.

Options evaluated:

1. **Keep the `http.server` handler and the Python-string views.** No dependency, but S01 wants Flask, and routing, escaping and headers stay hand-written.
2. **Flask and Jinja on top of `sqlite3`, behind the existing ports.** One runtime dependency (Flask and the packages it installs), pinned. The storage and the use cases do not change.
3. **Flask, Jinja and SQLAlchemy, as in the idea repository.** Adds an ORM that the ports already make unnecessary and would replace the SQLite repositories of [MIL-005].
4. **Flask used only for routing, with the Python-string views.** Keeps hand-written escaping, which a template engine does by default.

## Decision

Use option 2. The website is a Flask application whose application factory lives in the presentation layer; its pages are Jinja templates with autoescaping on; storage stays on `sqlite3` behind the repository ports. Flask is the only runtime dependency and is pinned to an exact version. The safety rules of [ADR-0002] are kept: a read-only database connection in the application, no write route and no session, one confined images folder, the security headers on every response, and data changed by commands only. The domain and application layers never import `flask` or `jinja2`; an import-linter contract checks it.

## Consequences

**Positive:**

- Routing, error pages, static files and escaping come from a maintained framework, and the templates are easier to read than HTML in Python strings.
- The use cases, the ports and the SQLite repositories do not change, so the layers and their tests stay as they are.
- Participants who know Flask recognise the structure.

**Negative:**

- The project has a runtime dependency (Flask and what it installs) that has to be pinned and kept up to date, and a vulnerability in it is a risk to the site; the opengrep scan and a pinned version limit it.
- The install is `python -m pip install -e .` instead of nothing; the README and the wiki explain it.
- The principle of no runtime dependency of [ADR-0001] and [ADR-0002] ends; SC3 and CN-008 are rewritten.

## Affected Artifacts

- [ADR-0002] — superseded for the web layer by this decision.
- [BC-001] — objectives O1 and O10 and success criteria SC1, SC3 and SC11 follow from it.
- [SA-001] — concerns CN-008 and CN-013.
- [MIL-006] delivers it.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[ADR-0002]: ./adr-0002-sqlite-storage-and-dynamic-site.md
[MIL-006]: ../milestones/mil-006-dynamic-site-and-cleanup.md
