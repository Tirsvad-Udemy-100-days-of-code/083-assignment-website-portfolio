# SQA Review Record: Python source of mil-002-core-domain-and-use-cases

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-011 |
| CrossReference | [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go | pending |

---

## Artifact Under Review

- Instance reviewed: Python source and tests of branch `mil-002-core-domain-and-use-cases` (domain, application and unit tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)
- Checks run: `pytest -q` 57 passed; `ruff check .` and `ruff format --check .` clean; `mypy` clean; `lint-imports` 2 kept; `doxygen Doxyfile` no warning; opengrep scan with `.opengrep.yml` 0 findings

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Packages `domain`, `application`; modules `project.py`, `home.py`; classes `Project`, `HomePage`, `InvalidProjectError`; constants `MAX_TITLE_LENGTH` and `HOME_PROJECT_LIMIT`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`require_non_blank`, `ProjectRepository`, `list_projects`); no single-letter names. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check .` and `ruff format --check .` pass; the only suppression is `S311` for tests, which seed `random.Random(1)` on purpose. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every function, method and test is annotated, `-> None` included; `mypy --strict` passes on 34 files. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare `except`; `home` raises `ValueError` for a limit below 1; entities raise `InvalidProjectError` and `InvalidProfileError`, which derive from `DomainError`. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; the builtin `type` is not shadowed (the field is `kind`). |
| 7 | Files, locks and connections are managed with context managers | Pass | No file, lock or connection is opened in the layers or in the tests. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Every module, class and public function has a Doxygen docstring; `doxygen Doxyfile` prints no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print` and no logging call in the layers. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No design class diagram exists: the project models no use case ([BC-001] Out of Scope). The classes follow the Clean Architecture layout and the tasks of [MIL-002]; no deviation. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 57 tests named for the behaviour, using fakes of the ports, no file system and no network, independent of order. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes; no `Any` is used. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` is empty; each `dev` tool is used (pytest, ruff, mypy, import-linter). |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | Blank and length checks live once in `domain/validation.py`; every limit is a constant in `constants.py`; mapping to DTOs is private to each use case. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports 2 contracts kept, 0 broken: `application` imports `domain`, and `domain` imports no other layer; there are no cycles. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | Each class and function has one reason to change; the ports are narrow protocols with one method each; the use cases depend on those protocols only. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `domain` (`entities`, `value_objects`, `errors`), `application` (`ports`, `dto`, `use_cases`) under `src/portfolio` and `tests/unit` mirror the layout; `infrastructure` and `presentation` are created in [MIL-003] with their first file. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English, snake_case, without space. |

## Overall Verdict

Go — every Mandatory criterion of `QC-PY-001` passes and the checks listed above are clean.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[BC-001]: ../../business-case.md
[MIL-002]: ../../milestones/mil-002-core-domain-and-use-cases.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
