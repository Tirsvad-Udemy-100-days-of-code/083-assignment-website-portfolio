# MIL-005: SQLite storage and management

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-005 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Deprecated | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version <br>Verdict Go (RC-022) | [1406a53] |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Flask decision: criterion 7 now says the gateway adds no runtime dependency, because SC3 allows the one Flask dependency later (ADR-0003) <br>Verdict Go (RC-030) | [ae5a380] |

---

## Purpose

Decide whether the portfolio data can live in a SQLite database instead of JSON files: the database holds the projects and the profile, the existing JSON files can be imported once, and the author can change the data with commands. A Go lets the next gateway make the site dynamic.

## Deliverable

A SQLite database (Python `sqlite3`, no new dependency) with a versioned schema for projects (with tags and skills) and for the profile (with skills and links); SQLite implementations of the existing repository ports; the commands `init`, `import` and the management commands for projects and the profile; unit, integration and end-to-end tests. The current `build` and `serve` commands keep working on the JSON files until [MIL-006].

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `python -m portfolio init` creates the database with the current schema version; running it on a database with a newer schema version stops with a clear message (O9) | Both cases pass an end-to-end test | Either case missing |
| 2 | `python -m portfolio import` loads `data/projects.json` and `data/profile.json` through `load_from_json` and writes them in one transaction; it refuses a non-empty database unless `--replace` is given (O9, SC10) | An end-to-end test passes for an empty, a filled and a `--replace` run | A partial import is left behind after an error |
| 3 | The SQLite repositories return the same `Project` and `Profile` objects as the JSON repositories for the sample data (O9, SC10) | A contract test runs against both implementations | A difference in any field |
| 4 | The commands add, change, list and remove a project, and set the profile, validating through the entities; an invalid value gives a one-line message and a non-zero exit code (O9) | End-to-end tests pass | An invalid value is stored |
| 5 | Every SQL statement is parameterised: no value is put into SQL text, and a title such as `x'); DROP TABLE project;--` is stored and shown literally (SC11) | A test with hostile input passes and a search of the source finds no formatted SQL | Any formatted SQL |
| 6 | The database file is not tracked by git and no secret or personal data is stored beyond the portfolio data (SC11) | `.gitignore` lists the file; the scan is clean | Database file tracked |
| 7 | This gateway adds no runtime dependency: `[project] dependencies` is unchanged (SC3) | Inspection of `pyproject.toml` | A dependency added |
| 8 | `pytest`, `ruff`, `mypy --strict`, import-linter, Doxygen (no warning) and the opengrep scan pass (SC2, SC4) | All pass | Any failure |
| 9 | The source review record (`QC-PY-001`) is `Go` | `RC-*` says Go | `No-Go` or missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-004] | The data model (projects with tags and skills, profile with photo) and the ports it uses are the ones delivered there |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O9 (data in SQLite, managed with commands) | [BC-001] Objectives |
| SC3, SC10, SC11 | [BC-001] Success Criteria |
| CN-012 | [SA-001] Primary Concerns |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-24 — one day after the end of the earlier plan window of [PP-001], moved by this scope change.

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Define the database schema and its version | Tables for projects, project tags, project skills, the profile, profile skills and profile links, with keys, `NOT NULL` and `CHECK` rules that match the entity rules, foreign keys switched on, and the schema version in `PRAGMA user_version`. All names and limits come from `constants.py`. | No | |
| 2 | Implement the SQLite repositories | `SqliteProjectRepository` and `SqliteProfileRepository` implement the existing read ports; new narrow ports (and implementations) add, replace and remove a project and set the profile. Every statement is parameterised, one transaction per write, and `sqlite3` errors become the existing data-source errors with the cause kept. The connection is opened and closed by a context manager. | No | |
| 3 | Add the `init` command | Creates the database file (default `data/portfolio.db`) with the schema, or confirms an existing one; stops with a message when the schema version is newer than the program knows. The default path is a constant and the file is added to `.gitignore`. | No | |
| 4 | Add the `import` command | Reads the JSON files with `load_from_json` and writes them in one transaction; refuses a non-empty database unless `--replace`; reports how many projects were imported. | No | |
| 5 | Add the management commands | `project list`, `project add`, `project set`, `project remove` and `profile set`, validated through the entities, with one-line messages and the existing exit-code convention. | No | |
| 6 | Test the storage | Unit tests with in-memory databases, a contract test that runs the same checks against the JSON and the SQLite repositories, integration tests with `tmp_path`, end-to-end tests of the commands, a hostile-input test and a failure-in-the-middle-of-import test that proves nothing is left behind. | No | |
| 7 | Review the source and scan it | Review the source and tests against `QC-PY-001`, write the `RC-*` record, run opengrep with the local rules before each push and fix findings. | No | |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[PP-001]: ../project-plan.md
[MIL-004]: ./mil-004-documentation-and-wrap-up.md
[MIL-006]: ./mil-006-dynamic-site-and-cleanup.md
[1406a53]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/1406a53bbc208284c38c07a83b3d264ffdea7b00
[ae5a380]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/ae5a3801d5a3fc5b5ef24d5a0c9ea5dcabe71db4
