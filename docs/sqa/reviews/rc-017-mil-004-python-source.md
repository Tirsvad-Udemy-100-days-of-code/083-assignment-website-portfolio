# SQA Review Record: Python source of mil-004-documentation-and-wrap-up

## Metadata
| Key | Value |
| --- | --- |
| ID | RC-017 |
| CrossReference | [QC-PY-001] |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version<br>Verdict Go | pending |

---

## Artifact Under Review

- Instance reviewed: Python source and tests of branch `mil-004-documentation-and-wrap-up` (the LinkedIn link, the profile photo and image copy, and the project flip cards with tags and skills, with their tests)
- Checklist used: [QC-PY-001]
- Scope: full review
- Language and domain: n/a
- Language reviewer: none
- Mode: autonomous, not independent (the reviewer is a stand-in for S01)
- Checks run: `pytest -q` 308 passed; `ruff check .` and `ruff format --check .` clean; `mypy --strict` clean on 81 files; `lint-imports` 4 kept, 0 broken; `doxygen Doxyfile` no warning; opengrep scan with `.opengrep.yml` 0 findings; end-to-end tests build the real data folder with and without a profile photo

## Checklist Results

| # | Criterion | Status | Evidence/Notes |
| --- | --- | --- | --- |
| 1 | Packages, modules, functions, variables, classes and constants follow PEP 8 casing (`snake_case`, `PascalCase`, `UPPER_SNAKE`) | Pass | New modules `confined_path.py`, `data_folder_reader.py`; classes `FolderDataFileReader`; constants such as `MAX_TAGS`, `IMAGE_EXTENSIONS` follow PEP 8 casing. |
| 2 | Names state purpose in the domain's language; no unexplained abbreviations, no single-letter names outside tiny scopes | Pass | Names state purpose (`resolve_inside`, `read_bytes`, `write_bytes`, `initials`); no single-letter names. |
| 3 | Code is produced by the project's formatter and passes its linter with no unexplained suppressions | Pass | `ruff check .` and `ruff format --check .` pass; no new suppression. |
| 4 | Every function and method signature is type-annotated, including `-> None` | Pass | Every new function, method and test is annotated, `-> None` included; `mypy --strict` passes. |
| 5 | No bare `except:`, no swallowed exceptions; specific exceptions are raised and the cause is kept (`raise ... from`) | Pass | No bare `except`; `OSError` and `ValueError` are handled with a specific type and re-raised as `DataFileError` or `SiteWriteError` with `raise ... from err`. |
| 6 | No mutable default arguments and no shadowed builtins | Pass | No mutable default argument; no builtin is shadowed. |
| 7 | Files, locks and connections are managed with context managers | Pass | Files are read and written with `Path.read_bytes` and `Path.write_bytes`, which close the file themselves. |
| 8 | Public modules, classes and functions have docstrings that say what, not how | Pass | Every new module, class and public function has a Doxygen docstring; `doxygen Doxyfile` prints no warning. |
| 9 | Logging uses `logging`, not `print`; no secrets or personal data in log output | Pass | No logging was added; the commands keep writing user messages with `sys.stdout.write` and `sys.stderr.write`; nothing personal is logged. |
| 10 | Classes and operations trace to the Design Class Diagram they implement; deviations are recorded | Pass | No design class diagram exists: the project models no use case ([BC-001] Out of Scope). The classes follow tasks 8 to 10 of [MIL-004]; no deviation. |
| 11 | Tests exist for new behaviour, are named for the behaviour, and do not depend on order or the network | Pass | 119 new tests named for the behaviour: unit with fakes, integration with `tmp_path`, end to end through the real data folder; a symlink test skips itself when the OS refuses a symlink; no network, no order dependence. |
| 12 | Type checker runs in strict mode without errors; `Any` is justified in a comment | Pass | `mypy --strict` passes; no `Any` is used. |
| 13 | Dependencies are declared and pinned in the project's dependency file, none unused | Pass | `dependencies` is still empty (SC3); no dependency was added. |
| 14 | Each piece of knowledge (a business rule, constant, format, validation or query) is defined in one place; code is merged only where it expresses the same knowledge, not where it merely looks alike | Pass | The path check lives once in `infrastructure/confined_path.py` and is used by the reader and by both writer methods; the image and tag limits are constants in `constants.py`; escaping and URL checks stay in `views/html_safety.py`. |
| 15 | Imports point inward: business-rule modules import no framework, database, UI or delivery-mechanism code, and there are no import cycles | Pass | `lint-imports` reports 4 contracts kept, 0 broken: the new port `DataFileReader` is in the application layer and its implementation in infrastructure; presentation imports no infrastructure. |
| 16 | SOLID holds: a class or module has one reason to change; new behaviour is added by extension, not by editing a type test in several places; subclasses honour the contract of their base; protocols are narrow; high-level code depends on protocols or abstract types and receives its implementations | Pass | `DataFileReader` and `SiteWriter` are narrow protocols; `build_site` receives its reader and writer from the composition root; new behaviour (images, tags, skills) was added by extension of the entities, DTOs and views. |
| 17 | Source is laid out in the layers and folders of the clean architecture folder structure (`domain`, `application`, `infrastructure`, `presentation` packages under `src/`, and `unit`, `integration` and `e2e` under `tests/`), in `snake_case`, and imports between the layers point inward | Pass | New files are in `application/ports`, `infrastructure` and `tests/integration`; imports point inward. |
| 18 | File and folder names are English, contain no space and no character outside letters, digits, `-`, `_` and `.`, and follow the casing of the language for files | Pass | All names are English, snake_case, without space; the image files are lower case with `-`. |

## Overall Verdict

Go — every Mandatory criterion of `QC-PY-001` passes and the checks listed above are clean.

## Action Items

| Action | Owner | Due |
| --- | --- | --- |
| None | S01 | - |

---

[BC-001]: ../../business-case.md
[MIL-004]: ../../milestones/mil-004-documentation-and-wrap-up.md
[QC-PY-001]: ../../../framework/qc/code/qc-programming-python.md
