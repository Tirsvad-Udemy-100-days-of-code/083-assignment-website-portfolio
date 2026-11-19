# MIL-003: Site generation and preview

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-003 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version | [8163226] |

---

## Purpose

Decide whether the site can be built and viewed: the data is read from JSON, the pages are rendered and written, and a local server shows them. A Go lets MIL-004 take screenshots and write the documentation from a working site.

## Deliverable

The `infrastructure` and `presentation` packages: `load_from_json`, a JSON-backed repository, the home and about views, a stylesheet, a site writer, the commands `python -m portfolio build` and `python -m portfolio serve`, a sample `data/projects.json` and `data/profile.json`, and integration and end-to-end tests that build the site and fetch its pages from the local server.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | `python -m portfolio build` writes `index.html`, `about.html` and `style.css` to the build folder (SC1) | All three files exist | Any file missing |
| 2 | `python -m portfolio serve` serves `index.html` and `about.html` on `127.0.0.1` and returns HTTP 200 (SC1) | Both return 200 | Any other status |
| 3 | `python -m pytest` passes the unit, integration and end-to-end tests (SC2) | Exit code 0 | Any failure |
| 4 | Every value from the data file is HTML-escaped in the output | A test with markup in a title shows it escaped | Markup is rendered |
| 5 | A missing or invalid data file gives a clear message and a non-zero exit code | Test passes | Traceback or exit code 0 |
| 6 | `[project] dependencies` is still empty (SC3) | Empty | Any entry |
| 7 | The import-linter contracts, `ruff check` and `mypy` pass | Exit code 0 | Any error |
| 8 | The opengrep scan reports no finding above the accepted baseline (SC4) | Zero blocking findings | Any High or Critical finding |
| 9 | The code review record against `qc-programming-python` is `Go` | `RC-*` says Go | `No-Go` or missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-002] | The adapters implement the ports and the commands call the use cases of the core |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O1 (generator, `load_from_json`), O2 (local preview) | [BC-001] Objectives |
| O3 (tests) | [BC-001] Objectives |
| SC1, SC2, SC3, SC4 | [BC-001] Success Criteria |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-22 — inside the plan window 2026-11-19 to 2026-11-23 of [PP-001], after the decision date of [MIL-002].

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Add load_from_json and the JSON repositories | Implement `load_from_json` and the JSON-backed `ProjectRepository` and `ProfileRepository` in `infrastructure/`, with clear errors for a missing file, invalid JSON and missing keys. These are the adapters for the ports of the core. | No | |
| 2 | Add the sample data files | Create `data/projects.json` with at least six sample projects from the course and `data/profile.json` with the about text, with the keys of the idea repository (title, type, description, image URL, source code URL). | No | |
| 3 | Render the home and about pages | Create the views in `presentation/` that turn the data transfer objects of `home` and `about` into HTML with the standard library, with a shared layout (header, navigation, footer) and HTML escaping of every value. | No | |
| 4 | Add the stylesheet | Write `style.css`, a responsive stylesheet (cards in a grid that collapses on a narrow screen) that the site writer copies to the build folder. | No | |
| 5 | Add the site writer and the build command | Implement the site writer adapter and the `build` command, with `--data` and `--out` options whose defaults come from `constants.py`, and wire the composition root in `__main__.py`. | No | |
| 6 | Add the serve command | Implement the `serve` command with `http.server`, bound to `127.0.0.1` by default, with a `--port` option, serving the build folder. | No | |
| 7 | Add integration and end-to-end tests | Write integration tests for the JSON adapters and the writer with `tmp_path`, and an end-to-end test that builds the site, starts the server on a free port in a thread and fetches both pages with `urllib`. No GUI is involved. | No | |
| 8 | Review the adapters and entry points against the Python checklist | Review `src/` and `tests/` against `qc-programming-python`, run ruff, mypy, import-linter and the opengrep scan, write the `RC-*` record and fix any `Fail` before the pull request. | No | |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[MIL-002]: ./mil-002-core-domain-and-use-cases.md
[8163226]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/816322642c270c0dc5fa0f722c0b3e3f41de5187
