# Store the portfolio in SQLite and render the site on request

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0002 |
| CrossReference | [BC-001], [SA-001], [ADR-0001], [ADR-0003], [MIL-005], [MIL-006] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Deprecated | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version <br>Verdict Go (RC-024) | [1406a53] |
| 2026-11-19 | Superseded by ADR-0003 | Jens Tirsvad Nielsen | Stand-in for S01 | Superseded by ADR-0003: the web layer is Flask with Jinja templates; the SQLite storage, the read-only server and the safety rules are kept <br>Verdict Go (RC-033) | [ae5a380] |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

[ADR-0001] chose a static site generator that reads JSON files and writes pages to a folder. S01 now wants the site to be dynamic and the data to be stored in SQLite instead of JSON. The two forces from [ADR-0001] still hold: S03 and [BC-001] want no runtime dependency, and the code must stay in testable layers. Python ships `sqlite3` and `http.server`, so both wishes can be met without a package.

Options evaluated:

1. **Flask and SQLAlchemy, as in the idea repository.** Familiar, but adds several runtime dependencies and a secret; rejected for the reasons in [ADR-0001].
2. **SQLite through `sqlite3`, and a request handler on `http.server` that renders the pages on each request.** No dependency; the data changes with commands and shows on the next request. The server runs a small surface: read-only routes, no forms, no login.
3. **The same, plus a web admin page.** Adds forms, login, sessions and CSRF protection; a much larger attack surface. S01 chose not to include it.
4. **Keep static pages and only read from SQLite.** Does not meet the request for a dynamic site.

## Decision

Use option 2. The database is a SQLite file opened through the standard library, with a versioned schema, parameterised statements and one transaction per write. The site is served by an `http.server` handler that opens the database read-only and renders the existing views on each request. Data is changed by commands, not by the web site. The JSON files are only an input to a one-time `import`, through `load_from_json`; the static `build` command and the JSON stores are removed.

## Consequences

**Positive:**

- Still no runtime dependency (SC3); the layers and their tests stay as they are, because the repositories are ports.
- A data change shows on the next request, without a rebuild.
- The server has no write route, so there is no form, session or CSRF risk.

**Negative:**

- The site needs a running process and a database file; the README and the wiki explain `init`, `import` and `serve`.
- Hostile input now reaches SQL and file paths: every statement is parameterised, the images route is confined to one folder, and tests with hostile input guard both.
- The data is no longer readable as plain text in the repository; the sample JSON stays as the import source.
- A web admin page would need a new decision.

## Affected Artifacts

- [ADR-0001] — superseded by this decision; its no-runtime-dependency principle is kept.
- [BC-001] — objectives O1, O2 (amended), O9 and O10 and success criteria SC1, SC10 and SC11 follow from it.
- [SA-001] — concern CN-012.
- [MIL-005] and [MIL-006] deliver it.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[ADR-0001]: ./adr-0001-standard-library-site-generator.md
[ADR-0003]: ./adr-0003-flask-and-jinja-on-sqlite.md
[MIL-005]: ../milestones/mil-005-sqlite-storage-and-management.md
[MIL-006]: ../milestones/mil-006-dynamic-site-and-cleanup.md
[1406a53]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/1406a53bbc208284c38c07a83b3d264ffdea7b00
[ae5a380]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/ae5a3801d5a3fc5b5ef24d5a0c9ea5dcabe71db4
