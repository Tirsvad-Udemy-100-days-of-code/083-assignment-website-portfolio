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
| 2026-11-19 | Deprecated | Jens Tirsvad Nielsen | Stand-in for S01 | Initial version <br>Verdict Go (RC-023) | [1406a53] |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Flask decision: the dynamic site is a Flask application with Jinja templates; new criteria on templates, escaping, the pinned dependency and the layer contract; new tasks 1 to 5 and 7; the documents move to ADR-0003 (ADR-0003) <br>Verdict Go (RC-031) | [ae5a380] |

---

## Purpose

Decide whether the site is a Flask application on SQLite: a running Flask application renders the home and about pages with Jinja templates from the database on every request, Flask is the one pinned runtime dependency, the static build and the JSON stores are gone, and the documents describe the new way of working. A Go closes the change.

## Deliverable

A Flask application (an application factory in the presentation layer) with Jinja templates for the home page (a flip card for each project) and the about page, a stylesheet, safe image serving and security headers; `python -m portfolio serve` starts it; Flask pinned in `pyproject.toml`; the `build` command, the static site writer, the standard library handler, the Python-string views and the JSON stores removed (`load_from_json` stays as the importer of [MIL-005]); an updated README, wiki in English, Danish and Bahasa Malaysia, Doxygen reference and screenshots; ADR-0003 in place of ADR-0002 for the web layer.

## Go / No-Go Criteria

| # | Criterion (objectively checkable) | Go | No-Go |
| --- | --- | --- | --- |
| 1 | After a project is added or changed with a command, the next request to the running Flask application shows it, without a restart or a rebuild (O10, SC1) | An end-to-end test against a running server passes | The page is stale |
| 2 | The application answers `GET` and `HEAD` for `/`, `/about`, `/static/style.css` and `/images/<file>`, `404` for anything else and `405` for other methods, with error pages that show no stack trace and with debug off (O10, SC11) | End-to-end tests for each case | Any other answer |
| 3 | The pages are rendered by Jinja templates with autoescaping on: a title such as `<script>alert(1)</script>` is shown as text; no template or code marks user data safe (`safe` filter, `Markup`) (SC11) | A test with hostile text passes and a search finds none | Unescaped output |
| 4 | The images route serves only files inside the `images` folder of the data folder; `..`, absolute paths, encoded separators and symbolic links out of the folder give `404` (SC11) | Tests with hostile paths pass | A file outside the folder is served |
| 5 | Every response carries `Content-Security-Policy: default-src 'self'`, `X-Content-Type-Options: nosniff` and `Referrer-Policy: no-referrer`; the application reads the database read-only, has no write route and no session, needs no secret key, and listens on `127.0.0.1` by default (SC11) | Tests check the headers, the read-only open and the routes | Any missing |
| 6 | Flask is the only runtime dependency and is pinned to an exact version in `pyproject.toml`; the README setup installs it; the site runs after `python -m pip install -e .` (SC3, SC6) | Inspection and an install in a clean `.venv` | Another dependency or an unpinned one |
| 7 | A missing or unreadable database gives a one-line message that names `init` and `import`, and a non-zero exit code (O9) | An end-to-end test passes | A traceback |
| 8 | `build`, `build_site`, the static site writer, the standard library handler, the Python-string views and the JSON repositories are removed and nothing imports them; import-linter keeps the four layer contracts and has a contract that the domain and application layers do not import `flask` or `jinja2` (O1, SC2) | `lint-imports` passes and a search finds none | Any left, or a contract missing |
| 9 | The README and the wiki (three languages, same page set) describe the Flask application, `init`, `import`, the management commands and `serve`; each step page that changed has a new screenshot taken in Docker (SC5, SC6) | `QC-WIKI-001` has no `Fail`; screenshots exist | A stale page or picture |
| 10 | `doxygen Doxyfile` has no warning; `pytest`, `ruff`, `mypy --strict`, import-linter and the opengrep scan pass (SC2, SC4) | All pass | Any failure |
| 11 | ADR-0003 is accepted and ADR-0002 is marked `Superseded by ADR-0003` (O10) | Both Version Histories say so | Either missing |
| 12 | The published wiki is checked on the host after the merge (`QC-WIKI-001` criterion 14) | Sidebar and links work | Any dead link |
| 13 | The review records for the source, the wiki and the README are `Go` | `RC-*` says Go | `No-Go` or missing |

## Dependencies

| Depends on | Reason |
| --- | --- |
| [MIL-005] | The database, the SQLite repositories, `init`, `import` and the management commands |

## Traceability

| Business Case objective / KPI / user story | Reference |
| --- | --- |
| O1 (amended), O10 (Flask application rendering from the database), O4, O5 | [BC-001] Objectives |
| SC1, SC2, SC3 (amended), SC4, SC5, SC6, SC10, SC11 | [BC-001] Success Criteria |
| CN-008 (amended), CN-012, CN-013 | [SA-001] Primary Concerns |

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
| 1 | Add Flask as the pinned dependency | Add `Flask` with an exact version to `[project] dependencies` in `pyproject.toml`, install it in the `.venv`, add a layer contract that the domain and application layers do not import `flask` or `jinja2`, and describe the install in the README. Flask is the only runtime dependency. | No | |
| 2 | Write the Flask application | An application factory `create_app` in the presentation layer with the routes `/`, `/about`, `/static/style.css` and `/images/<file>`; each request opens the database read-only, runs the `home` or `about` use case and renders a template; error handlers for `404` and `405` show no stack trace; debug is off; GET and HEAD only; no session and no secret key. The use cases and the file reader come from the composition root. | No | |
| 3 | Replace the views with Jinja templates | A base layout, the home page with a flip card for each project and the about page become Jinja templates in the package, with autoescaping on, the safe-URL check as a template filter, no `safe` filter and no `Markup`; the stylesheet moves to Flask's static folder; the templates and the stylesheet are included in the package data. | No | |
| 4 | Serve images safely | A narrow port reads files from the `images` folder of the data folder with the same path confinement as before, and the route serves them with `X-Content-Type-Options: nosniff` and a content type taken from the file extension of the image whitelist. | No | |
| 5 | Add the security headers | An after-request handler adds `Content-Security-Policy: default-src 'self'`, `X-Content-Type-Options: nosniff` and `Referrer-Policy: no-referrer` to every response, error pages included. | No | |
| 6 | Change the `serve` command | `serve` takes `--db`, `--data`, `--host` and `--port`, checks the database first and names `init` and `import` when it is missing, and starts the Flask application with debug off. The loopback host stays the default. | No | |
| 7 | Remove the static build, the standard library handler, the old views and the JSON stores | Delete the `build` command, `build_site`, the `SiteWriter` and its implementation, the standard library handler and the Python-string views, and the JSON repositories; keep `load_from_json` as the importer; update the composition root, the tests and the import-linter contracts. | No | |
| 8 | Test the dynamic site | Flask test-client tests for every route, method, header, template and hostile path; end-to-end tests against a running server on port 0; a test that changes data with a command and sees it on the next request; a test of the missing-database message. | No | |
| 9 | Write the decision record | ADR-0003: Flask and Jinja on top of SQLite; ADR-0002 becomes `Superseded by ADR-0003`. | No | |
| 10 | Update the README, the wiki and the Doxygen reference | Change Getting started (the install now pulls Flask), the data and preview steps, add a step for SQLite and the Flask application in English, Danish and Bahasa Malaysia, keep commands and code in English, and run `doxygen Doxyfile` with no warning. | No | |
| 11 | Retake the screenshots | Update `docs/tools/capture_screenshots.py` to install the project, initialise and import a database inside the container and take the pictures of the running site; GUI work stays in Docker, never on the host desktop. | No | |
| 12 | Run the final checks and review | Run pytest, ruff, mypy, import-linter, Doxygen and the opengrep scan; review the source, the wiki and the README; write the `RC-*` records. | No | |
| 13 | Verify the published wiki | After the merge, check the sidebar, every page and every link on the host and record it. | No | |

---

[BC-001]: ../business-case.md
[SA-001]: ../stakeholder-analysis.md
[MIL-005]: ./mil-005-sqlite-storage-and-management.md
[1406a53]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/1406a53bbc208284c38c07a83b3d264ffdea7b00
[ae5a380]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/ae5a3801d5a3fc5b5ef24d5a0c9ea5dcabe71db4
