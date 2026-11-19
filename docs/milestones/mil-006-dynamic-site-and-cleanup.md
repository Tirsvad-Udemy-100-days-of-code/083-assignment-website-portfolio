# MIL-006: Dynamic site and cleanup

## Metadata
| Key | Value |
| --- | --- |
| ID | MIL-006 |
| CrossReference | [BC-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version <br>Verdict Go (RC-023) | pending |

---

## Purpose

Decide whether the site is dynamic and SQLite is the only store: a running server renders the home and about pages from the database on every request, the static build and the JSON stores are gone, and the documents describe the new way of working. A Go closes the change.

## Deliverable

`python -m portfolio serve` renders `/` and `/about` from the database on each request and serves the stylesheet and the images; the `build` command, the static site writer and the JSON stores are removed (`load_from_json` stays as the importer of [MIL-005]); an updated README, wiki in English, Danish and Bahasa Malaysia, Doxygen reference and screenshots; ADR-0002 in place of ADR-0001.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | After a project is added or changed with a command, the next request to the running server shows it, without a restart or a rebuild (O10, SC1) | An end-to-end test against a running server passes | The page is stale |
| 2 | The server answers `GET` and `HEAD` for `/`, `/about`, `/style.css` and `/images/<file>`, `404` for anything else and `405` for other methods (O10, SC11) | End-to-end tests for each case | Any other answer |
| 3 | The images route serves only files inside the data folder's `images` folder; `..`, absolute paths, encoded separators and symbolic links out of the folder give `404` (SC11) | Tests with hostile paths pass | A file outside the folder is served |
| 4 | Every response carries `Content-Security-Policy: default-src 'self'`, `X-Content-Type-Options: nosniff` and `Referrer-Policy: no-referrer`; the server reads the database read-only, listens on `127.0.0.1` by default and never prints a stack trace to the visitor (SC11) | Tests check the headers, the read-only open and the error page | Any missing |
| 5 | A missing or unreadable database gives a one-line message that names `init` and `import`, and a non-zero exit code (O9) | An end-to-end test passes | A traceback |
| 6 | `build`, `build_site`, the static site writer and the JSON repositories are removed; no code imports them; import-linter keeps the four layer contracts (O1, SC2) | A search finds none and `lint-imports` passes | Any left |
| 7 | The README and the wiki (three languages, same page set) describe `init`, `import`, the management commands and `serve`; each step page that changed has a new screenshot taken in Docker (SC5, SC6) | `QC-WIKI-001` has no `Fail`; screenshots exist | A stale page or picture |
| 8 | `doxygen Doxyfile` has no warning; `pytest`, `ruff`, `mypy --strict`, import-linter and the opengrep scan pass; `[project] dependencies` is still empty (SC2, SC3, SC4) | All pass | Any failure |
| 9 | ADR-0002 is accepted and ADR-0001 is marked `Superseded by ADR-0002` (O9, O10) | Both Version Histories say so | Either missing |
| 10 | The published wiki is checked on the host after the merge (`QC-WIKI-001` criterion 14) | Sidebar and links work | Any dead link |
| 11 | The review records for the source, the wiki and the README are `Go` | `RC-*` says Go | `No-Go` or missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-005] | The database, the SQLite repositories, `init`, `import` and the management commands |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O10 (dynamic site rendered from the database on request) | [BC-001] Objectives |
| O1, O2 (amended), O4, O5 | [BC-001] Objectives |
| SC1, SC2, SC3, SC4, SC5, SC6, SC10, SC11 | [BC-001] Success Criteria |
| CN-012 | [SA-001] Primary Concerns |

## Ownership

| Role | Stakeholder ID (SA) |
| --- | --- |
| Owner | S01 |
| Approving reviewer | S01 |

## Target Date

2026-11-25 — one day after the decision date of [MIL-005].

## Tasks

| # | Task | Summary | Needs its own Use Case/User Story? | Reference |
| --- | --- | --- | --- | --- |
| 1 | Write the dynamic request handler | A `http.server` handler whose routes are `/`, `/about`, `/style.css` and `/images/<file>`; each request opens the database read-only, runs the `home` or `about` use case and renders the existing views; `404` and `405` pages; the security headers; no stack trace to the visitor; GET and HEAD only. The handler lives in the presentation layer and receives its use cases and its file reader from the composition root. | No | |
| 2 | Serve images safely | A narrow port reads files from the `images` folder of the data folder with the same path confinement as before, and the handler maps `/images/<file>` to it with a content type taken from a fixed table. | No | |
| 3 | Change the `serve` command | `serve` takes `--db`, `--data`, `--host` and `--port`, checks the database first and names `init` and `import` when it is missing. The loopback host stays the default. | No | |
| 4 | Remove the static build and the JSON stores | Delete the `build` command, `build_site`, the `SiteWriter` and its implementation, and the JSON repositories; keep `load_from_json` as the importer; update the composition root, the tests and the import-linter contracts. | No | |
| 5 | Test the dynamic site | End-to-end tests against a running server on port 0 for every route, method, header and hostile path; a test that changes data with a command and sees it on the next request; a test of the missing-database message. | No | |
| 6 | Write the decision record | ADR-0002: SQLite through the standard library and a server that renders on request; ADR-0001 becomes `Superseded by ADR-0002`. | No | |
| 7 | Update the README, the wiki and the Doxygen reference | Change Getting started, the data and preview steps, add a step for SQLite and the dynamic server in English, Danish and Bahasa Malaysia, keep commands and code in English, and run `doxygen Doxyfile` with no warning. | No | |
| 8 | Retake the screenshots | Update `docs/tools/capture_screenshots.py` to initialise and import a database inside the container and take the pictures of the running site; GUI work stays in Docker, never on the host desktop. | No | |
| 9 | Run the final checks and review | Run pytest, ruff, mypy, import-linter, Doxygen and the opengrep scan; review the source, the wiki and the README; write the `RC-*` records. | No | |
| 10 | Verify the published wiki | After the merge, check the sidebar, every page and every link on the host and record it. | No | |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[MIL-005]: ./mil-005-sqlite-storage-and-management.md
