# Build the portfolio with the Python standard library

## Metadata
| Key | Value |
| --- | --- |
| ID | ADR-0001 |
| CrossReference | [BC-001], [SA-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version | pending |

Allowed Status values: `Proposed`, `Accepted`, `Rejected`, `Deprecated`, `Superseded by ADR-NNNN`.

---

## Context

The idea repository for the Day 83 assignment is a Flask application that stores projects in SQLite through SQLAlchemy, renders them with Jinja templates and Bootstrap-Flask, and needs a `FLASK_KEY` environment variable. It has no tests and no run instructions. This project has three forces: S03 and the Business Case want no runtime dependencies (SC3); S02 wants readable code that uses the assignment's function names; and the project is sized at about 60 minutes in the course.

Options evaluated:

1. **Flask and SQLAlchemy, as in the idea repository.** Familiar to course participants, but it adds five or more runtime dependencies and a secret, needs a database file to be seeded before the first run, and hides the layers behind the framework.
2. **A static site generator on the standard library.** `load_from_json` reads the project list, two use cases (`home` and `about`) build plain data, views render HTML with the standard library, and `http.server` previews the result. No dependency, no secret and no database.
3. **Flask without a database** (JSON data only). Removes SQLAlchemy but keeps Flask and Jinja as runtime dependencies.

## Decision

Build the portfolio as a static site generator on the Python standard library (option 2): keep the idea's data keys, page set and function names `home`, `about` and `load_from_json`, and use no runtime dependency.

## Consequences

**Positive:**

- The project runs with Python alone, which meets SC3 and S03's concern CN-008.
- The layers can be tested without a framework or a database, and the dependency direction is checked by import-linter.
- No secret or configuration is needed to run the site.

**Negative:**

- Participants who expect Flask see a different technology; the README and the wiki explain the choice.
- Templates are plain Python strings, not Jinja, so the views carry more code than a template engine would need.
- Features that need a running application (forms, a database) are out of scope and would need a new decision.

## Affected Artifacts

- [BC-001] — Out of Scope names this decision; objective O1 and success criterion SC3 follow from it.
- [SA-001] — the conflict between S02 and S03 is resolved by this decision.

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
