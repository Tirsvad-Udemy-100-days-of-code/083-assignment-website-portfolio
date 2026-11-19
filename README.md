# 🚀 Portfolio Website

A portfolio website written in Python with Flask and SQLite, built as the Day 83 assignment of the Udemy course "100 Days of Code: The Complete Python Pro Bootcamp". The projects and the profile live in a SQLite database that you change with commands. A Flask server renders a home page where every project is a flip card (picture, name and description on the front; source code, tags and the skills it shows on the back) and an about page with a link to the author's LinkedIn profile and the profile photo, from the database on every request. It is for fellow course participants who want a readable, runnable solution to compare with their own, and for anyone browsing the repository for ideas.

## 📚 Table of Contents

- [Overview](#-overview)
- [Requirements](#-requirements)
- [Setup](#-setup)
- [Run](#-run)
- [Tests](#-tests)
- [License](#-license)
- [Links](#-links)
- [Appendix: Project documents](#-appendix-project-documents)

## 🧭 Overview

The Day 83 lecture asks for a website that shows your skills and the things you have built, without step-by-step guidance. This project is one answer to that assignment: the idea comes from a Flask and SQLAlchemy application. This project keeps Flask, Jinja templates and SQLite, and uses Python's own `sqlite3` module instead of SQLAlchemy, so Flask is the only runtime dependency, pinned to an exact version (the decision is recorded in [ADR-0003][ADR-0003]). The assignment's function names `home`, `about` and `load_from_json` are kept; `load_from_json` now reads the sample JSON files once, to import them into the database.

The repository is laid out in `src/`, `tests/` and `docs/`:

| Folder | What it holds |
| --- | --- |
| `src/portfolio/domain/` | The `Project` and `Profile` entities and their rules; no input or output |
| `src/portfolio/application/` | The use cases (`home`, `about`, `init`, `import` and the project and profile commands) and the ports they need |
| `src/portfolio/infrastructure/` | `load_from_json`, the SQLite database, schema and repositories, and the file reader |
| `src/portfolio/presentation/` | The Flask application, the Jinja templates, the stylesheet and the commands |
| `src/portfolio/constants.py` | Every constant of the project |
| `data/` | The sample `projects.json` and `profile.json` to import, and the images they use (`data/images/`); the database `portfolio.db` is made here |
| `tests/` | Unit, integration and end-to-end tests (`pytest`) |
| `docs/` | Project documents, the wiki sources and the screenshots |

### The build steps

The project was built in eight steps. Each step has a page in the wiki that explains what it teaches; the pictures are taken from this project's own output.

| Step | What it adds | Screenshot |
| --- | --- | --- |
| 1. Project data | The sample projects are described in a JSON file and read by `load_from_json` | ![Step 1: the project data][step-1] |
| 2. Home page | The `home` use case and a page that lists the projects | ![Step 2: the home page without a stylesheet][step-2] |
| 3. About page | The `about` use case and a page about the owner | ![Step 3: the about page without a stylesheet][step-3] |
| 4. Style | A responsive stylesheet: a card grid that folds to one column | ![Step 4: the styled home page][step-4] |
| 5. Preview | The `serve` command shows the site in a browser | ![Step 5: the site on the local preview server][step-5] |
| 6. Tests | pytest tests prove each layer, and a layer check guards the design | ![Step 6: the test run][step-6] |
| 7. Flip cards and profile | Projects as flip cards with tags and skills, a LinkedIn link and a profile photo | ![Step 7: the back of a flip card][step-7] |
| 8. SQLite and Flask | The data moves into SQLite, commands change it and Flask shows it on every request | ![Step 8: the database commands][step-8] |

The front of a card shows the picture, name and description; the back shows the source code, the tags and the skills:

![The front of a project card][step-7-front]

On a narrow screen the cards fold into one column:

![The styled home page on a narrow screen][step-4-narrow]

## 📋 Requirements

- Python 3.13 or newer. Flask is the only runtime dependency; `pip` installs it with the setup below.
- Git, to clone the repository.
- Optional, for development: `pytest`, `ruff`, `mypy` and `import-linter`, installed with the `dev` extra (see Setup).
- Optional, for the API reference: [Doxygen](https://www.doxygen.nl/).
- Optional, to retake the screenshots: Docker. The pictures are taken in a container, never on the desktop.

## 🛠️ Setup

Clone the repository, create a local virtual environment named `.venv`, upgrade pip and install the project with its development tools.

Windows (PowerShell):

```powershell
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux and macOS:

```bash
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If PowerShell refuses to run the activation script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` in that window first. To leave the environment, run `deactivate`. Without the development tools, use `python -m pip install -e .` instead.

## ▶️ Run

With the environment active, create the database, fill it with the sample data and start the server:

```text
python -m portfolio init
python -m portfolio import
python -m portfolio serve
```

`init` creates `data/portfolio.db`. `import` copies `data/projects.json` and `data/profile.json` into it once; after that the database is the only source (`import --replace` imports again over a filled database). `serve` starts a Flask server at <http://127.0.0.1:8000> that reads the database on every request; press `Ctrl+C` to stop it. The server only reads, so you change the data with commands, and the next page load shows the change:

```text
python -m portfolio project list
python -m portfolio project add --title "My new project" --kind Website --description "Added with a command while the server runs." --source-code-url https://example.com/my-new-project --tag Flask --skill SQLite
python -m portfolio project set --help
python -m portfolio project remove --help
python -m portfolio profile set --headline "Systems Developer" --skill Python
python -m portfolio serve --db data/portfolio.db --data data --host 127.0.0.1 --port 8000
python -m portfolio --help
```

To show your own projects, add them with `project add` (an image is an `http(s)` address or a path in the data folder, such as `images/my-project.svg`; a card can have tags and skills). To show your own profile, use `profile set`: add your links (LinkedIn, GitHub) and put your photo in `data/images/`, then set `--photo images/profile.jpg`; without a photo the about page shows an avatar with your initials. A missing database or an invalid value gives a one-line message and a non-zero exit code; `serve` names `init` and `import` when the database is missing.

## 🧪 Tests

```text
python -m pytest
```

The other checks used before every change:

```text
python -m ruff check .
python -m ruff format --check .
python -m mypy
lint-imports
doxygen Doxyfile
```

`lint-imports` checks that the layers only depend inward and that the domain and application layers do not import Flask or Jinja. `doxygen Doxyfile` builds the API reference into `docs/doxygen/html/`. The screenshots are retaken with `python docs/tools/capture_screenshots.py`, which needs Docker.

## 📄 License

GNU Affero General Public License v3.0 or later; see [LICENSE][license].

## 🔗 Links

- [Repository][repository]
- [Documentation][documentation]
- [Issue tracker][issues]

## 📎 Appendix: Project documents

The documents a newcomer needs, in reading order.

| Document | What it tells you |
| --- | --- |
| [AGENTS.md][agents] | The rules for automated assistants in this repository |
| [Business Case][BC-001] | Why the project exists, its scope and success criteria |
| [Stakeholder Analysis][SA-001] | Who is involved; the stakeholder IDs used for owners and reviewers |
| [Project Plan][PP-001] | The gateways and their schedule |
| [Milestones][milestones] | One document per gateway: Go/No-Go criteria and tasks |
| [Decision records][adr] | Why the site uses SQLite, and why Flask with Jinja ([ADR-0003][ADR-0003]) |
| [Artifact registry][registry] | Where each artifact type lives, the next version, the PO language and domain |
| [Traceability matrix][TM-001] | How the artifacts link and when each was last reviewed |
| [Governance][GOV-001] | The review workflow, who decides and how disputes escalate |
| [Framework README][framework-readme] | The framework this project uses |
| [Framework changelog][framework-changelog] | What changed in each framework release |

---

[repository]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio
[documentation]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/wiki
[issues]: https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/issues
[license]: ./LICENSE
[agents]: ./AGENTS.md
[BC-001]: ./docs/business-case.md
[SA-001]: ./docs/stakeholder-analysis.md
[PP-001]: ./docs/project-plan.md
[milestones]: ./docs/milestones/
[adr]: ./docs/adr/
[ADR-0003]: ./docs/adr/adr-0003-flask-and-jinja-on-sqlite.md
[registry]: ./docs/artifact-registry.md
[TM-001]: ./docs/sqa/traceability-matrix.md
[GOV-001]: ./docs/sqa/governance.md
[framework-readme]: ./framework/README.md
[framework-changelog]: ./framework/CHANGELOG.md
[step-1]: ./docs/images/step-01-project-data.png
[step-2]: ./docs/images/step-02-home-page-structure.png
[step-3]: ./docs/images/step-03-about-page.png
[step-4]: ./docs/images/step-04-styled-home-page.png
[step-4-narrow]: ./docs/images/step-04-narrow-screen.png
[step-5]: ./docs/images/step-05-preview-server.png
[step-6]: ./docs/images/step-06-tests.png
[step-7]: ./docs/images/step-07-flip-card-back.png
[step-7-front]: ./docs/images/step-07-flip-card-front.png
[step-8]: ./docs/images/step-08-database-commands.png
