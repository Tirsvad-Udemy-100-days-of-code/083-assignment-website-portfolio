# MIL-001: Project setup

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-001 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version | [8163226] |

---

## Purpose

Decide whether the repository is ready to receive code: the project installs, its tooling files exist, a smoke test runs, the repository is described on the git host and the local security scan works. A Go lets MIL-002 start building the domain.

## Deliverable

An installable Python project skeleton under `src/portfolio/` with a `constants.py` module, a passing smoke test under `tests/`, the files `pyproject.toml`, `.gitignore`, `.editorconfig` and `Doxyfile`, a repository on the git host with a description and at least five topics, and a documented local opengrep scan that runs with no finding above the accepted baseline.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `python -m pip install -e ".[dev]"` succeeds in a fresh `.venv` on Python 3.13 | Exit code 0 | Any error |
| 2 | `[project] dependencies` in `pyproject.toml` is empty and `requires-python` is `>=3.13` | Both true | Either false |
| 3 | `python -m pytest` runs the smoke test | Exit code 0 | Failing or no test |
| 4 | `bash framework/scripts/check-editorconfig.sh` passes | Exit code 0 | Any error |
| 5 | `.env` is ignored by git and is not tracked | `git check-ignore .env` prints the path | `.env` is tracked or not ignored |
| 6 | The repository description is set and at least five topics are set (SC7) | Git host API shows both | Either missing |
| 7 | The opengrep scan of the repository reports no finding above the accepted baseline (SC4) | Zero blocking findings | Any High or Critical finding |
| 8 | `doxygen Doxyfile` runs without a warning on the skeleton | Zero warnings | Any warning |
| 9 | The code review record against `qc-programming-python` is `Go` | `RC-*` says Go | `No-Go` or missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| Baseline pull request (Business Case, Stakeholder Analysis, Project Plan, milestones, decision record, governance, traceability matrix) | Nothing goes under `src/` or `tests/` before the baseline is accepted |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O3 (tests and layer checks), O4 (`.venv` and pip) | [BC-001] Objectives |
| O6 (description, topics, opengrep) | [BC-001] Objectives |
| SC2, SC3, SC4, SC7 | [BC-001] Success Criteria |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-20 — inside the plan window 2026-11-19 to 2026-11-23 of [PP-001], consistent with the Business Case constraint of a small project sized at about 60 minutes in the course.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add the Python .gitignore | Add a Python `.gitignore` that also ignores `.env`, `.venv/`, the build folder, the Doxygen output and the local prompt log, so no secret or generated file is committed. The personal `.env` is never read, imported or tested by the project. | No | |
| 2 | Add the .editorconfig | Copy `framework/templates/editorconfig/baseline.editorconfig` to the project root and run `bash framework/scripts/check-editorconfig.sh` until it passes, so every editor uses the same indentation and line endings. | No | |
| 3 | Add pyproject.toml and the package skeleton | Create `pyproject.toml` with `requires-python >=3.13`, no runtime dependencies, a `dev` extra (pytest, ruff, mypy, import-linter) and the pytest settings. Create `src/portfolio/__init__.py`, `src/portfolio/__main__.py` and `src/portfolio/constants.py` with Doxygen comments, and a smoke test under `tests/unit/`. Layer packages are created when their first file is added. | No | |
| 4 | Add the Doxyfile | Generate a `Doxyfile` for the Python source with output in an ignored folder, and describe the Doxygen comment style used in the source, so the reference can be built with `doxygen Doxyfile`. | No | |
| 5 | Set the repository description and topics | Set a one-sentence description and at least five topics on the git host with the repository API, using the token from the personal `.env`. The token is read into the process environment only and never printed or written to a project file. | No | |
| 6 | Install the git hooks and the local opengrep scan | Run `bash framework/scripts/install-git-hooks.sh --enable-plan-gate`, and record the opengrep command (`~/.opengrep/cli/latest/opengrep.exe scan`) used before every push, with the baseline of accepted findings, so the scan result can be compared at every milestone. | No | |
| 7 | Review the setup code against the Python checklist | Review the skeleton against `qc-programming-python`, write the `RC-*` record and fix any `Fail` before the pull request. | No | |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[8163226]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/816322642c270c0dc5fa0f722c0b3e3f41de5187
