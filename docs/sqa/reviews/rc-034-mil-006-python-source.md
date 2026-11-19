# SQA Review Record: Python source of mil-006-flask-site

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-034 |
| CrossReference | [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go | [0c64aed] |

---

## Artifact Under Review

- Instance reviewed: Python source and tests of branch `mil-006-flask-site` (the Flask application, the Jinja templates, the read-only database, the images route, the security headers, the `serve` command and the removal of the static build, with their tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)
- Checks run: `pytest -q` 767 passed, 1 skipped (a test that needs a `?` in a file name, which Windows does not allow); `ruff check .` and `ruff format --check .` clean; `mypy --strict` clean on 130 files; `lint-imports` 5 kept, 0 broken; `doxygen Doxyfile` no warning; opengrep with `.opengrep.yml` 0 findings and with the community python rules 0 findings; a running-server test shows a project added with a command on the next request; the server was also started by hand and `/`, `/about`, `/images/profile.jpg` and `/static/style.css` answered 200 with the headers

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | New modules, functions and constants follow PEP 8 casing: `page_routes.py`, `create_app`, `SECURITY_HEADERS`, `IMAGE_CONTENT_TYPES`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`register_image_route`, `image_content_type`, `safe_url`, `create_server`); no single-letter names outside tiny scopes. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check .` and `ruff format --check .` pass on 394 files; no `noqa`, `nosemgrep` or `type: ignore` was added to `src/` or `tests/`. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every new function, method and test is annotated, `-> None` included; `mypy --strict` passes on 130 files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare `except`; `DataSourceError` from the image reader gives a 404 and from the page providers a plain 500 page, with the cause only in the debug log; no exception is swallowed. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; no builtin is shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | The read-only SQLite connection is opened through `contextlib.closing`; the images are read with `Path.read_bytes`; the test server is stopped in a `finally` block. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Every new module, class and public function has a Doxygen docstring; `doxygen Doxyfile` prints no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | Only `logging` at debug level is used for a failing request or a server that cannot start; the commands write one `error:` line to stderr; nothing personal is logged. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No design class diagram exists: the project models no use case ([BC-001] Out of Scope). The classes follow tasks 1 to 8 of [MIL-006]; the deviations are listed in the pull request. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | About 150 new tests named for the behaviour: Flask test-client tests for routes, methods, headers and templates, hostile-text and hostile-path tests, a read-only test, a running-server test of freshness, a test that no `safe` filter or `Markup` is used; no network beyond the loopback, no order dependence. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes; no `Any` is used. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `pyproject.toml` lists one dependency, `Flask==3.1.3`, pinned to an exact version; a test checks it; no dependency is unused. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Routes, template names, security headers, image content types and messages live once in `constants.py`; the safe-URL rule is one function used by the template filter; the image confinement is the one in `confined_path.py`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports 5 contracts kept, 0 broken, among them one that the domain and application layers import no `flask` or `jinja2`; the Flask code is in presentation and only `__main__.py` builds the adapters. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The pages get their data through providers made by the composition root and the images through the existing `DataFileReader` port; the use cases did not change for Flask. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | New files are in `presentation/web`, `presentation/templates`, `infrastructure` and the test folders; imports point inward. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English, snake_case, without space; the template files are lower case. |

## Overall Verdict

Go — every Mandatory criterion of `QC-PY-001` passes and the checks listed above are clean.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[BC-001]: ../../business-case.md
[MIL-006]: ../../milestones/mil-006-dynamic-site-and-cleanup.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[0c64aed]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/0c64aed29bbd9484f961c11b6965844b9d1afb3e
