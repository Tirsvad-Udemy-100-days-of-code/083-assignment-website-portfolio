# SQA Review Record: Python source of mil-001-project-setup

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-010 |
| CrossReference | [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go | [24bf6ae] |

---

## Artifact Under Review

- Instance reviewed: Python source and tests of branch `mil-001-project-setup` (skeleton of the package and the smoke tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)
- Checks run: `pytest -q` 4 passed; `ruff check .` clean; `ruff format --check .` clean; `mypy` clean; `doxygen Doxyfile` no warning; opengrep scan with `.opengrep.yml` 0 findings

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | Modules `portfolio`, `constants`, `__main__`; function `build_parser`; constants `APP_NAME` and `DEFAULT_PORT`. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose; no single-letter names. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check .` and `ruff format --check .` pass; the only suppressions are none. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | `build_parser`, `main` and every test are annotated, `-> None` included; `mypy --strict` passes. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No `try` block exists; argparse raises `SystemExit` for bad input. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No default arguments are mutable and no builtin is shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | No file, lock or connection is opened. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Module, function and constant comments are Doxygen docstrings or `##` comments that say what the item is. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No `print` and no logging call; the argparse help is the only output. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No design class diagram exists: the project models no use case ([BC-001] Out of Scope). The skeleton has no class. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | Four tests named for the behaviour; none depends on order or the network. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes; no `Any` is used. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` is empty (SC3); the `dev` extra declares pytest, ruff, mypy and import-linter, all used or about to be used in MIL-002. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The parser description lives only in `constants.py` as `APP_DESCRIPTION`; the agent moved it there from `__main__.py` during the review. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `__main__` imports only `portfolio.constants`; there is no cycle and no layer package yet. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | `build_parser` and `main` each have one reason to change; there is no type test. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | `src/portfolio` and `tests/unit` follow the layout; a layer package or test folder is created when its first file is added, so `domain`, `application`, `infrastructure`, `presentation`, `integration` and `e2e` do not exist yet. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English, lower case, without space. |

## Overall Verdict

Go — every Mandatory criterion of `QC-PY-001` passes and the checks listed above are clean.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
[24bf6ae]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/24bf6ae3f1aed725ec1d61efcc5364f1dea9868d
