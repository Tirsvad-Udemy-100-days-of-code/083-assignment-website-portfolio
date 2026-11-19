**English** · [Dansk](Getting-Started-da) · [Bahasa Malaysia](Getting-Started-ms)

# Getting started

You need Python 3.13 or newer and Git. The project has no runtime dependencies. Docker is only needed to retake the screenshots, and Doxygen only to build the API reference.

## Set up

Windows (PowerShell):

```text
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Linux and macOS:

```text
git clone https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio.git
cd 083-assignment-website-portfolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The `.venv` folder is a private copy of Python for this project, so nothing is installed system-wide. Run `deactivate` to leave it.

## Run

```text
python -m portfolio build
python -m portfolio serve
```

Open <http://127.0.0.1:8000> in a browser. Press `Ctrl+C` to stop the server.

## Test

```text
python -m pytest
```

Continue with the [Lecture summary](Lecture-Summary) or go straight to [Step 1](Step-1-Project-Data).
