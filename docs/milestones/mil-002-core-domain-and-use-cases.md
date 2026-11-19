# MIL-002: Core domain and use cases

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-002 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version | [8163226] |

---

## Purpose

Decide whether the business rules of the portfolio are correct and independent of files, HTML and the command line. A Go lets MIL-003 build the adapters and the entry points around a tested core.

## Deliverable

The `domain` and `application` packages under `src/portfolio/`: the `Project` and `Profile` entities, the ports for reading them, and the use cases `home` and `about`, with unit tests that use fakes of the ports, Doxygen comments in the source and an import-linter contract that checks the dependency direction.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `python -m pytest tests/unit` passes | Exit code 0 | Any failure |
| 2 | The domain and application tests use no file system, network or framework | No such import in `tests/unit` | Any such import |
| 3 | The import-linter contract passes: `domain` imports nothing from the other layers, `application` imports only `domain` | Contract kept | Contract broken |
| 4 | Every constant is in `constants.py`, with no magic number or repeated string in the layers | Review finds none | Any found |
| 5 | `ruff check` and `mypy` report no error on `src/` | Exit code 0 | Any error |
| 6 | The opengrep scan reports no finding above the accepted baseline | Zero blocking findings | Any High or Critical finding |
| 7 | The code review record against `qc-programming-python` is `Go` | `RC-*` says Go | `No-Go` or missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-001] | The package, tooling and plan gate must exist before the domain is written |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O1 (home and about from a list of projects, the assignment's function names) | [BC-001] Objectives |
| O3 (tests and layer checks) | [BC-001] Objectives |
| SC2 | [BC-001] Success Criteria |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-21 — inside the plan window 2026-11-19 to 2026-11-23 of [PP-001], after the decision date of [MIL-001].

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add the Project and Profile entities | Create the immutable `Project` entity (title, type, description, image URL, source code URL, as in the idea repository) and the `Profile` entity (name, headline, skills, links) in `domain/`, with validation rules whose limits come from `constants.py`. Entities hold no input or output. | No | |
| 2 | Add the repository ports | Define the narrow ports `ProjectRepository` and `ProfileRepository` in `application/ports/`, each with one read method, so the use cases never name a file or a format. | No | |
| 3 | Add the home and about use cases | Implement `home` (the featured projects, at most the limit in `constants.py`, in a stable or seeded order) and `about` (the profile) in `application/use_cases/`, returning plain data transfer objects. The names are those of the idea repository. | No | |
| 4 | Unit-test the core with fakes | Write pytest tests under `tests/unit/` for the entities and use cases using in-memory fakes of the ports, covering valid data, invalid data and the limit. | No | |
| 5 | Check the layer direction with import-linter | Add the import-linter contracts to `pyproject.toml` and run them, so a dependency that points outward fails the check. | No | |
| 6 | Review the core against the Python checklist | Review `src/` and `tests/` against `qc-programming-python`, run ruff, mypy and the opengrep scan, write the `RC-*` record and fix any `Fail` before the pull request. | No | |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[MIL-001]: ./mil-001-project-setup.md
[8163226]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/816322642c270c0dc5fa0f722c0b3e3f41de5187
