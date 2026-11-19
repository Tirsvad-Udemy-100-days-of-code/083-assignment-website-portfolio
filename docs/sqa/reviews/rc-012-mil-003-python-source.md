# SQA Review Record: Python source of mil-003-site-generation-and-preview

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-012 |
| CrossReference | [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go | [53db60c] |

---

## Artifact Under Review

- Instance reviewed: Python source and tests of branch `mil-003-site-generation-and-preview` (adapters, views, commands and tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)
- Checks run: `pytest -q` 189 passed; `ruff check .` and `ruff format --check .` clean; `mypy` clean; `lint-imports` 4 kept; `doxygen Doxyfile` no warning; `python -m portfolio build` writes the three files; opengrep scan with `.opengrep.yml` 0 findings

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Packages `infrastructure`, `presentation`; modules `load_from_json.py`, `html_safety.py`; classes `FileSiteWriter`, `HtmlSiteRenderer`, `DataFileError`; constants such as `SAFE_URL_SCHEMES`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`is_safe_url`, `build_site`, `create_server`); no single-letter names. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check .` and `ruff format --check .` pass on 279 files; the suppressions are `S311` for tests, and one `# nosemgrep: python37-compatibility-importlib2` on the `importlib.resources` import: the host scan flagged it as a Python 3.7 compatibility problem, a false positive because the project requires Python 3.13 or newer; the line carries the reason. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function, method and test is annotated, `-> None` included; `mypy --strict` passes on 77 files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare `except`; `OSError` and `JSONDecodeError` are re-raised as `SiteWriteError` and `DataFileError` with `raise ... from err`; no exception is swallowed. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; no builtin is shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | Files are read and written with `Path.read_text` and `Path.write_text`; the server is closed in a `finally` block. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Every module, class and public function has a Doxygen docstring; `doxygen Doxyfile` prints no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | User messages use `sys.stdout.write` and `sys.stderr.write`; diagnostics and the server access log use `logging`; no secret or personal data is logged. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No design class diagram exists: the project models no use case ([BC-001] Out of Scope). The classes follow the tasks of [MIL-003]; no deviation. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 189 tests named for the behaviour: unit with fakes, integration with `tmp_path`, end to end through a server on port 0; no external network and no order dependence. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes; no `Any` is used. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` is empty (SC3); every `dev` tool is used. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Escaping and URL checking live once in `views/html_safety.py`; constants only in `constants.py`; the data keys are mapped once in `load_from_json`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports 4 contracts kept, 0 broken: presentation > infrastructure > application > domain, the domain imports no other layer, presentation does not import infrastructure, infrastructure does not import presentation; only `__main__` names concrete adapters. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | Ports are narrow protocols (`SiteWriter`, `SiteRenderer`, the repositories); each command has one use case; the use case depends on protocols only. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `domain`, `application`, `infrastructure`, `presentation` under `src/portfolio` and `unit`, `integration`, `e2e` under `tests/` as in the layout; the presentation layer uses `commands`, `views` and `shared`. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English, snake_case, without space. |

## Overall Verdict

Go — every Mandatory criterion of `QC-PY-001` passes and the checks listed above are clean.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[BC-001]: ../../business-case.md
[MIL-003]: ../../milestones/mil-003-site-generation-and-preview.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[53db60c]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/53db60c1a016b07abf9b27b093f0501591ae69c5
