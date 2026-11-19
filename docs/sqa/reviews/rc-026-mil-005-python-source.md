# SQA Review Record: Python source of mil-005-sqlite-storage-and-management

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-026 |
| CrossReference | [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go | pending |

---

## Artifact Under Review

- Instance reviewed: Python source and tests of branch `mil-005-sqlite-storage-and-management` (the SQLite schema, repositories, `init`, `import` and the management commands, with their tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)
- Checks run: `pytest -q` 619 passed; `ruff check .` and `ruff format --check .` clean; `mypy --strict` clean on 135 files; `lint-imports` 4 kept, 0 broken; `doxygen Doxyfile` no warning; opengrep with `.opengrep.yml` 0 findings and the community python rules 0 findings; `pyproject.toml` `dependencies = []` checked by a test; `data/portfolio.db` ignored by git

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | New modules, classes and constants follow PEP 8 casing: `sqlite_database.py`, `SqliteProjectRepository`, `SCHEMA_VERSION`, `DEFAULT_DATABASE_PATH`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`import_portfolio`, `replace_all`, `require_current_schema`); no single-letter names outside tiny scopes. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check .` and `ruff format --check .` pass on 387 files; no `noqa`, `nosemgrep` or `type: ignore` was added. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every new function, method and test is annotated, `-> None` included; `mypy --strict` passes on 135 files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare `except`; `sqlite3.Error` and `OSError` become `DatabaseError` with `raise ... from err`; no exception is swallowed. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; no builtin is shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | Connections are opened through `contextlib.closing` and each operation runs in a transaction context; a test deletes the database file afterwards, which proves no connection stays open on Windows. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Every new module, class and public function has a Doxygen docstring; `doxygen Doxyfile` prints no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No logging was added; commands write one `error:` line to stderr; nothing personal is logged. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No design class diagram exists: the project models no use case ([BC-001] Out of Scope). The classes follow tasks 1 to 6 of [MIL-005]; no deviation. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 310 new tests named for the behaviour: unit with in-memory databases, a contract test against both repository implementations, integration with `tmp_path`, end to end through the commands, an atomicity test and hostile-input tests; no network and no order dependence. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes; no `Any` is used. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` is still empty and a test checks it; no dependency was added. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The schema, the version and the connection handling each live once (`sqlite_schema.py`, `sqlite_database.py`); messages and defaults are in `constants.py`; the entity rules are not repeated in SQL beyond `NOT NULL` and not-blank checks. SQL text is static strings inside the adapter modules. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports 4 contracts kept, 0 broken: the new ports are in the application layer, their SQLite implementations in infrastructure, the commands in presentation; only `__main__.py` builds the adapters. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | The write ports are narrow protocols; use cases receive them; the importer takes the existing read ports, so `load_from_json` is reused; new behaviour was added by extension. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | New files are in `application/ports`, `application/use_cases`, `infrastructure`, `presentation/commands` and the `unit`, `integration` and `e2e` test folders; imports point inward. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English, snake_case, without space. |

## Overall Verdict

Go — every Mandatory criterion of `QC-PY-001` passes and the checks listed above are clean.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[BC-001]: ../../business-case.md
[MIL-005]: ../../milestones/mil-005-sqlite-storage-and-management.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
