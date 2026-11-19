# MIL-004: Documentation and wrap-up

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-004 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version | [8163226] |

---

## Purpose

Decide whether the project can be handed to course participants and repository viewers: a newcomer can set it up, run it and test it from the README, and can learn each build step from the wiki in three languages. A Go closes the project.

## Deliverable

`README.md` from the framework template, the Doxygen reference, and a flat wiki in `docs/wiki/` in English, Danish and Bahasa Malaysia with a Home page, a Getting Started page, a lecture summary, one page per build step and a sidebar, with one screenshot of this project's own output per step in the README and the wiki.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | Following the README on a clean clone (`.venv`, `python -m pip install --upgrade pip`, install, build, serve, test) works on Windows PowerShell (SC6) | Every command succeeds | Any command fails |
| 2 | The Getting Started page shows the same commands for Linux (SC6) | Commands for both systems | Either missing |
| 3 | Every English wiki page has a Danish and a Bahasa Malaysia page, and `QC-WIKI-001` has no `Fail` (SC5) | Page sets identical | Any page missing |
| 4 | Each build step has one screenshot taken from this project's own output, in the README and in the wiki (SC5) | All steps have an image | Any step without an image |
| 5 | No lecture screenshot, text or video is in the repository | None found | Any found |
| 6 | `doxygen Doxyfile` runs with no warning | Zero warnings | Any warning |
| 7 | No project artifact names the assistant tooling used to draft it | A search of the tracked files finds none | Any found |
| 8 | `python -m pytest`, `ruff check`, `mypy`, import-linter and the opengrep scan pass on the final tree (SC2, SC4) | All pass | Any failure |
| 9 | The wiki is published and the sidebar and links work on the host (QC-WIKI-001 criterion 14) | Checked on the host | Any dead link |
| 10 | The review records for the README, the wiki and any changed code are `Go` | `RC-*` says Go | `No-Go` or missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-003] | The screenshots and the commands in the documents come from the working site |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O4 (`.venv`, pip, run, test on both systems) | [BC-001] Objectives |
| O5 (wiki in three languages with a screenshot per step) | [BC-001] Objectives |
| SC5, SC6 | [BC-001] Success Criteria |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-23 — the end of the plan window 2026-11-19 to 2026-11-23 of [PP-001], after the decision date of [MIL-003].

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Capture one screenshot per build step in Docker | Build a Docker image with a headless browser and write a script that builds the site and captures the five steps (project data, home page structure, about page, styled and narrow layout, local preview) into `docs/images/`. The screenshots come from this project's own output and are never taken on the host desktop. | No | |
| 2 | Write the README | Write `README.md` from `framework/templates/README-template.md`: overview, requirements, creating and using a `.venv`, `python -m pip install --upgrade pip`, running the project, running the tests, the screenshots, the licence and the links. | No | |
| 3 | Write the English wiki | Write the flat wiki pages in `docs/wiki/`: Home, Getting Started for Windows and Linux, the lecture summary in the author's own words, one page per build step saying what it teaches and showing its screenshot, and the sidebar. | No | |
| 4 | Write the Danish wiki | Translate every English page to Danish as `<Page>-da.md` with the language line, keeping commands and code in English. The language check stays Pending until a person who reads Danish has checked it. | No | |
| 5 | Write the Bahasa Malaysia wiki | Translate every English page to Bahasa Malaysia as `<Page>-ms.md` with the language line, keeping commands and code in English. The language check stays Pending until a person who reads the language has checked it. | No | |
| 6 | Build the Doxygen reference | Run `doxygen Doxyfile`, fix every warning in the source comments and document the command in the README and the wiki. | No | |
| 7 | Run the final checks | Run pytest, ruff, mypy, import-linter and the opengrep scan on the final tree and search the tracked files for lecture material and for the assistant tooling name, then record the results in the review records. | No | |
| 8 | Review the documents and verify the published wiki | Review the README and the wiki against `QC-WIKI-001`, write the `RC-*` records, and after the merge check the sidebar and links on the published wiki. | No | |

---

[BC-001]: ../business-case.md
[PP-001]: ../project-plan.md
[MIL-003]: ./mil-003-site-generation-and-preview.md
[8163226]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/816322642c270c0dc5fa0f722c0b3e3f41de5187
