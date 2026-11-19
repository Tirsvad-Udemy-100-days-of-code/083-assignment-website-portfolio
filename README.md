# 🚀 Portfolio Website

A portfolio website generator written with the Python standard library only, built as the Day 83 assignment of the Udemy course "100 Days of Code: The Complete Python Pro Bootcamp". It reads a list of projects from a JSON file, writes a home page where every project is a flip card (picture, name and description on the front; source code, tags and the skills it shows on the back) and an about page with a link to the author's LinkedIn profile and the profile photo, and shows them on a local preview server. It is for fellow course participants who want a readable, runnable solution to compare with their own, and for anyone browsing the repository for ideas.

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

The Day 83 lecture asks for a website that shows your skills and the things you have built, without step-by-step guidance. This project is one answer to that assignment: the idea comes from a Flask and SQLAlchemy application, but the result needs no runtime dependency, so it runs with Python alone (the decision is recorded in [ADR-0001][ADR-0001]). The assignment's function names `home`, `about` and `load_from_json` are kept.

The repository is laid out in `src/`, `tests/` and `docs/`:

| Folder | What it holds |
| --- | --- |
| `src/portfolio/domain/` | The `Project` and `Profile` entities and their rules; no input or output |
| `src/portfolio/application/` | The use cases `home`, `about` and `build_site`, and the ports they need |
| `src/portfolio/infrastructure/` | `load_from_json`, the JSON repositories and the site writer |
| `src/portfolio/presentation/` | The HTML views, the stylesheet and the `build` and `serve` commands |
| `src/portfolio/constants.py` | Every constant of the project |
| `data/` | The sample `projects.json` and `profile.json`, and the images they use (`data/images/`) |
| `tests/` | Unit, integration and end-to-end tests (`pytest`) |
| `docs/` | Project documents, the wiki sources and the screenshots |

### The build steps

The project was built in seven steps. Each step has a page in the wiki that explains what it teaches; the pictures are taken from this project's own output.

| Step | What it adds | Screenshot |
| --- | --- | --- |
| 1. Project data | Projects are described in a JSON file and read by `load_from_json` | ![Step 1: the project data][step-1] |
| 2. Home page | The `home` use case and a page that lists the projects | ![Step 2: the home page without a stylesheet][step-2] |
| 3. About page | The `about` use case and a page about the owner | ![Step 3: the about page without a stylesheet][step-3] |
| 4. Style | A responsive stylesheet: a card grid that folds to one column | ![Step 4: the styled home page][step-4] |
| 5. Preview | The `build` and `serve` commands show the site in a browser | ![Step 5: the site on the local preview server][step-5] |
| 6. Tests | pytest tests prove each layer, and a layer check guards the design | ![Step 6: the test run][step-6] |
| 7. Flip cards and profile | Projects as flip cards with tags and skills, a LinkedIn link and a profile photo | ![Step 7: the back of a flip card][step-7] |

The front of a card shows the picture, name and description; the back shows the source code, the tags and the skills:

![The front of a project card][step-7-front]

On a narrow screen the cards fold into one column:

![The styled home page on a narrow screen][step-4-narrow]

## 📋 Requirements

- Python 3.13 or newer. The project has no runtime dependencies.
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

With the environment active, build the site and show it:

```text
python -m portfolio build
python -m portfolio serve
```

`build` reads `data/projects.json` and `data/profile.json` and writes `index.html`, `about.html` and `style.css` to the `build/` folder. `serve` shows that folder at <http://127.0.0.1:8000>; press `Ctrl+C` to stop it. Both commands have options:

```text
python -m portfolio build --data data --out build
python -m portfolio serve --out build --host 127.0.0.1 --port 8000
python -m portfolio --help
```

To show your own projects, edit `data/projects.json`: each entry has `title`, `type`, `description`, `img_url` (an `http(s)` address or a path in the data folder, such as `images/my-project.svg`), `source_code_url` and the optional lists `tags` and `skills`. To show your own profile, edit `data/profile.json`: add your links (LinkedIn, GitHub) and put your photo in `data/images/`, then set `"photo": "images/profile.jpg"`; without a photo the about page shows an avatar with your initials. A missing or invalid data file gives a one-line message and a non-zero exit code.

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

`lint-imports` checks that the layers only depend inward. `doxygen Doxyfile` builds the API reference into `docs/doxygen/html/`. The screenshots are retaken with `python docs/tools/capture_screenshots.py`, which needs Docker.

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
| [Decision record][ADR-0001] | Why the site is built with the standard library |
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
[ADR-0001]: ./docs/adr/adr-0001-standard-library-site-generator.md
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
