# Business Case: Website Portfolio

## Metadata
| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-11-19 | Deprecated | Jens Tirsvad Nielsen | S01 | Initial version | [8163226] |
| 2026-11-19 | Accepted | Jens Tirsvad Nielsen | Stand-in for S01 | Removed the notebook from scope and constraints (not requested)<br>Named the assignment's function names in O1<br>Reworded the tooling constraint | [8163226] |

---

## Executive Summary

Day 83 of the course "100 Days of Code: The Complete Python Pro Bootcamp" asks the participant to build a portfolio website that shows their skills and the projects they have built. The lecture gives no step-by-step guidance: the participant must design and build the result alone. This project delivers that assignment as a small, readable Python project: a portfolio site generated from a list of projects, with a home page, an about page and a local preview, built with the Python standard library only. It ships with tests, a Doxygen reference, a README and a three-language wiki (English, Danish, Bahasa Malaysia), so other course participants and repository visitors can run it, learn from it and compare it with their own solution.

## Methodological and Standards Foundation

- Method: plan first, then build. Business Case, Stakeholder Analysis, Project Plan, milestones and tasks are written and reviewed before any code, as the project's framework requires. Use cases are not modelled: the product is a small generator with one actor, and its tasks are plain technical tasks.
- Architecture: Clean Architecture layers (domain, application, infrastructure, presentation), with the dependency direction enforced by tooling.
- Quality: ISO/IEC 25010:2023 characteristics tag every review criterion; Python code is reviewed against the Python programming checklist before each pull request.
- Security: a local static-analysis scan with opengrep runs before each push.
- Language: the Product Owner's language is English and the domain is IT; the wiki is also published in Danish and Bahasa Malaysia.

## Problem Statement

1. The Day 83 assignment is deliberately open: a participant who finishes it alone has no reference to compare against, and a participant who copies a tutorial learns little.
2. The only available idea for this assignment is a Flask and SQLAlchemy application whose repository has no tests, no run instructions and no way to run it without installing and configuring several third-party packages and an environment variable.
3. A portfolio is needed for job interviews, but a beginner's portfolio is often an unstructured folder of scripts that a visitor cannot run or read quickly.

## Business Opportunity

A portfolio site that is easy to install (no runtime dependencies), easy to read (one concern per module, documented), proven by tests, and explained in three languages gives the author a reusable showcase, gives fellow participants a readable reference for the assignment, and gives repository visitors a clear example of a small, well-structured Python project.

## Objectives

| # | Objective |
| --- | --- |
| O1 | Provide a portfolio site generator that builds a home page and an about page from a JSON list of projects, with the function names `home`, `about` and `load_from_json` taken from the idea repository, using the Python standard library only. |
| O2 | Provide a local preview command so the site can be viewed in a browser without installing anything. |
| O3 | Prove the behaviour with automated pytest tests, and keep the dependency direction of the layers checked by tooling. |
| O4 | Document how to create and use a local `.venv`, upgrade pip, run the project and run the tests, for both Windows and Linux. |
| O5 | Explain each build step of the assignment, and what it teaches, in a wiki in English, Danish and Bahasa Malaysia, with one screenshot of this project per step. |
| O6 | Publish the repository with a description and topics, and scan the code with opengrep before every push. |

## Scope

### In Scope

- A Python package under `src/` with the layers domain, application, infrastructure and presentation, and a `constants.py` module for all constants.
- A sample `projects.json` listing portfolio entries, a home page, an about page, a stylesheet and a local preview server, all written to a build folder.
- Tests under `tests/` run with pytest.
- `pyproject.toml`, a Python `.gitignore`, an `.editorconfig`, a Doxygen configuration and Doxygen comments in the source.
- A README from the framework template and a flat wiki in `docs/wiki/` in English, Danish and Bahasa Malaysia, with a Getting Started page for Windows and Linux.
- Screenshots of this project's own output for every step, in the README and the wiki.
- Repository description and topics on the git host.

### Out of Scope

- Reproducing the Flask, SQLAlchemy and Bootstrap application of the idea repository (see ADR-0001).
- A database, user accounts, a contact form, content management or hosting and deployment of the site.
- Copying lecture material: no lecture screenshot, text or video appears in the README or the wiki; the lecture is only summarised.
- Third-party runtime dependencies. Development tools (pytest, ruff, mypy, import-linter) are installed only on request, through an optional extra.
- Use-case modelling, user stories and a domain dictionary: the product is too small to justify them.

## Expected Benefits

### Tangible Benefits

- A runnable site and a test suite that pass on a clean clone with Python 3.13 or newer.
- Zero runtime dependencies, so a visitor needs only Python.
- A Getting Started guide for Windows and Linux that works from a clean machine.
- A wiki with the same page set in three languages.

### Intangible Benefits

- A reference solution for fellow participants to compare with.
- Practice in planning, structured code, testing and documentation, which an interviewer can see.
- A portfolio entry the author can show.

## Strategic Alignment

The project supports the course's own goal for Day 83 (independent work that builds a portfolio) and the author's goal of becoming a Python developer. It follows the same repository conventions as the author's other course projects (a framework-driven documentation set, a three-language wiki with Windows and Linux guides).

## Success Criteria

| # | Criterion | Target | Measure |
| --- | --- | --- | --- |
| SC1 | The site builds and previews | `python -m portfolio build` writes `index.html` and `about.html`; `python -m portfolio serve` serves them on localhost | Manual run plus an end-to-end test |
| SC2 | Tests pass | 100 % of pytest tests pass on Python 3.13 | `python -m pytest` exit code 0 |
| SC3 | No runtime dependencies | `[project] dependencies` in `pyproject.toml` is empty | Inspection of `pyproject.toml` |
| SC4 | Static analysis is clean | 0 findings above the accepted baseline from opengrep, ruff and mypy | Tool output before each push |
| SC5 | Wiki is complete | Every English page has a Danish and a Bahasa Malaysia page; each step page has a screenshot | Page list compared with `QC-WIKI-001` |
| SC6 | Guide works on both systems | Getting Started shows Windows PowerShell and Linux commands for the `.venv`, pip upgrade, run and test | Review against the README and wiki criteria |
| SC7 | Repository is described | The repository has a description and at least five topics | Git host API response |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| The idea repository is a Flask application and a reviewer expects Flask | Medium: the result differs from the idea | Record the decision in ADR-0001; the home page, the about page and the data file of the idea are kept. |
| Danish and Bahasa Malaysia texts are produced without a native reviewer | Medium: wording errors | Keep sentences short, keep code and commands in English, and mark the language check as pending until a person who reads the language has checked it. |
| Screenshots taken on the host desktop would take the user's mouse and keyboard | Medium: interrupts the user | Take screenshots only in a Docker container with a headless browser, as the GUI testing rule requires. |
| A token is committed or printed | High: secret leak | Tokens stay in the untracked `.env`; the project does not read or test it; `.env` is in `.gitignore`; opengrep runs before each push. |
| The Gitea tokens lack a scope for issues, wiki or releases | Medium: sync or wiki publishing fails | Check each endpoint when first needed; stop and report instead of working around it. |
| The local opengrep binary is missing or outdated | Low: scan skipped | Check the binary path before the first push; stop if it cannot run. |

## Assumptions

- The Product Owner, the developer and the reviewer are the same person (S01); in autonomous mode the reviewer role is exercised as a stand-in and each record says so.
- The lecture gives a motivational introduction and the open assignment; no lecture resource file was provided, so none is used.
- The git host's wiki is enabled and the wiki publishing workflow of the organisation is delivered to the repository.
- Docker is available on the author's machine for headless screenshots.

## Constraints

- Python 3.13 or newer, a local `.venv`, pytest, a `pyproject.toml`, a `constants.py` for constants, Doxygen comments and a Doxyfile.
- Folder structure `src/`, `tests/`, `docs/`.
- No project artifact or document names the assistant tooling used to draft it.
- Every change reaches `main` through a branch and a pull request, one per milestone.
- Secrets come from `.env` for personal use only; the project does not import or test them.
- The assignment is sized at about 60 minutes in the course; the project is kept small to match.

## Cost–Benefit Assessment

| Costs | Benefits |
| --- | --- |
| Author effort: about one working session for planning, code, tests and three-language documentation | A runnable reference solution, a portfolio entry and a documented learning path |
| Docker image download for headless screenshots (one-off, development only) | Screenshots taken without disturbing the author's desktop |
| No licence or hosting cost | No runtime dependency to maintain |

The assessment is qualitative because the project is a learning exercise with no revenue.

## Stakeholders

| Stakeholder ID (SA) | Interest in this project |
| --- | --- |
| S01 | Product Owner, developer and reviewer: wants a finished, reviewed portfolio project for the course. |
| S02 | Course participants: want readable, runnable code with the assignment's names and README instructions to run it. |
| S03 | Repository viewers: want a clear description, topics and README, and no runtime dependencies. |

## Recommendation

Proceed: the project is small, has a clear definition of done, needs no runtime dependency and gives all three stakeholders something usable.

---

[SA-001]: ./stakeholder-analysis.md
[8163226]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/commit/816322642c270c0dc5fa0f722c0b3e3f41de5187
