"""Capture the screenshots of the README and the wiki.

Every image comes from this project's own output: the data file, the output of
its commands and the pages of the running Flask server. Nothing is taken from
the course lectures.

The pictures are taken by a headless browser in a Docker container, never on
the host desktop (a graphical test must not take the user's mouse and
keyboard). The server runs in a container too: it installs the project there,
so the pictures show a clean install. Needs Docker, an internet connection for
`pip` and the project's `.venv`.

Usage, from the repository root:

    .venv/Scripts/python.exe docs/tools/capture_screenshots.py
"""

import html
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / ".screenshots"
IMAGES = ROOT / "docs" / "images"
BROWSER_IMAGE = "zenika/alpine-chrome:latest"
PYTHON_IMAGE = "python:3.13-slim"
NETWORK = "portfolio-shots"
SERVER_NAME = "portfolio-preview"
SERVER_HOST = f"http://{SERVER_NAME}:8000"
SERVER_PORT = 8000
# The preview server binds to all interfaces of its own container so that the browser
# container can reach it over the private Docker network. No port is published to the
# host, so nothing is exposed; the scan finding is accepted for this reason.
CONTAINER_HOST = "0.0.0.0"  # noqa: S104  # nosemgrep: python-bind-all-interfaces
DESKTOP = (1200, 1150)
NARROW = (390, 900)
TERMINAL = (1000, 560)

TERMINAL_PAGE = """<!doctype html><meta charset="utf-8"><title>terminal</title>
<style>
body{{margin:0;background:#0f172a;color:#e2e8f0;
font:16px/1.5 Consolas,"DejaVu Sans Mono",monospace}}
.bar{{background:#1e293b;padding:10px 16px;color:#94a3b8;font-size:14px}}
pre{{margin:0;padding:18px 22px;white-space:pre-wrap;word-break:break-word}}
.prompt{{color:#4ade80}}
</style>
<div class="bar">{title}</div>
<pre>{body}</pre>
"""


def run(
    command: list[str], *, check: bool = True, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Run a command and return its text output; never goes through a shell."""
    # The command is a list built in this file from constants and the repository's own
    # paths, and shell=False, so no input can add to it; the scan finding is accepted.
    return subprocess.run(  # noqa: S603  # nosemgrep: dangerous-subprocess-use-audit
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=check,
        cwd=cwd,
    )


def python_exe() -> str:
    """Give the Python of the project's virtual environment, else the running one."""
    for candidate in (
        ROOT / ".venv" / "Scripts" / "python.exe",
        ROOT / ".venv" / "bin" / "python",
    ):
        if candidate.exists():
            return str(candidate)
    return sys.executable


def terminal_page(path: Path, title: str, command: str, output: str) -> None:
    """Write an HTML page that shows a command and its real output."""
    body = (
        f'<span class="prompt">$</span> {html.escape(command)}\n{html.escape(output)}'
    )
    path.write_text(
        TERMINAL_PAGE.format(title=html.escape(title), body=body), encoding="utf-8"
    )


def shoot(
    url: str, name: str, size: tuple[int, int], *, network: str | None = None
) -> None:
    """Take one screenshot of a URL with the headless browser in a container."""
    command = ["docker", "run", "--rm", "-v", f"{WORK}:/work"]
    if network:
        command += ["--network", network]
    command += [
        BROWSER_IMAGE,
        "--no-sandbox",
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={size[0]},{size[1]}",
        f"--screenshot=/work/{name}.png",
        url,
    ]
    run(command)
    shutil.copyfile(WORK / f"{name}.png", IMAGES / f"{name}.png")
    print(f"wrote docs/images/{name}.png")


def cli(workdir: Path, *arguments: str) -> tuple[int, str]:
    """Run one portfolio command in a folder; return its exit code and its output."""
    done = run([python_exe(), "-m", "portfolio", *arguments], cwd=workdir, check=False)
    text = (done.stdout + done.stderr).replace("\\", "/")
    return done.returncode, text.strip()


def transcript(workdir: Path, commands: list[list[str]]) -> tuple[str, str]:
    """Run commands one after another; return the first command and the whole output."""
    shown = "python -m portfolio " + " ".join(commands[0])
    lines: list[str] = []
    for index, arguments in enumerate(commands):
        _, text = cli(workdir, *arguments)
        if index:
            lines.append("\n$ python -m portfolio " + " ".join(arguments))
        lines.append(text)
    return shown, "\n".join(lines)


def prepare_workspace() -> Path:
    """Copy the sample data to a scratch folder; no command touches the repository."""
    shutil.rmtree(WORK / "cli", ignore_errors=True)
    (WORK / "cli").mkdir(parents=True)
    shutil.copytree(ROOT / "data", WORK / "cli" / "data")
    shutil.rmtree(WORK / "app", ignore_errors=True)
    app = WORK / "app"
    app.mkdir()
    for name in ("pyproject.toml", "README.md", "LICENSE"):
        shutil.copyfile(ROOT / name, app / name)
    shutil.copytree(
        ROOT / "src", app / "src", ignore=shutil.ignore_patterns("__pycache__")
    )
    return WORK / "cli"


def snapshot(page: str, name: str, extra: str = "") -> None:
    """Save a page of the running server as a file that loads its files from the server.

    `extra` is added to the head, for example a rule that turns the cards. A page
    without its stylesheet is made by removing the link to it.
    """
    probe = run(
        ["docker", "run", "--rm", "--network", NETWORK, "--entrypoint", "wget",
         BROWSER_IMAGE, "-q", "-O", "-", f"{SERVER_HOST}{page}"],
    )  # fmt: skip
    text = probe.stdout
    head = f'<base href="{SERVER_HOST}/">' + extra
    text = text.replace("<head>", "<head>" + head, 1)
    (WORK / f"{name}.html").write_text(text, encoding="utf-8")


def without_stylesheet(name: str) -> None:
    """Remove the link to the stylesheet from a saved page."""
    page = WORK / f"{name}.html"
    text = page.read_text(encoding="utf-8")
    page.write_text(re.sub(r"<link[^>]*stylesheet[^>]*>", "", text), encoding="utf-8")


def start_server(workdir: Path) -> None:
    """Start the Flask server in a container that installs the project first."""
    run(["docker", "network", "create", NETWORK], check=False)
    run(["docker", "rm", "-f", SERVER_NAME], check=False)
    serve = (
        "pip install -q --no-cache-dir --disable-pip-version-check /app && "
        "python -m portfolio serve --db /data/portfolio.db --data /data "
        f"--host {CONTAINER_HOST} --port {SERVER_PORT}"
    )
    run(
        [
            "docker", "run", "-d", "--rm", "--name", SERVER_NAME, "--network", NETWORK,
            "-v", f"{WORK}/app:/app", "-v", f"{workdir}/data:/data",
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            PYTHON_IMAGE, "sh", "-c", serve,
        ]
    )  # fmt: skip
    for _ in range(90):
        probe = run(
            ["docker", "run", "--rm", "--network", NETWORK, "--entrypoint", "wget",
             BROWSER_IMAGE, "-q", "-O", "/dev/null", f"{SERVER_HOST}/"],
            check=False,
        )  # fmt: skip
        if probe.returncode == 0:
            return
        # Wait for the server container to install the project and start; one second
        # between 90 tries.
        time.sleep(1)  # nosemgrep: arbitrary-sleep
    raise RuntimeError("the server container did not start")


def stop_server() -> None:
    """Stop the server container and remove the private network."""
    run(["docker", "rm", "-f", SERVER_NAME], check=False)
    run(["docker", "network", "rm", NETWORK], check=False)


def main() -> int:
    """Capture every screenshot; return the exit code."""
    WORK.mkdir(exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    workdir = prepare_workspace()

    data_text = (ROOT / "data" / "projects.json").read_text(encoding="utf-8")
    first_lines = "\n".join(data_text.splitlines()[:30])
    terminal_page(
        WORK / "data.html",
        "data/projects.json",
        "cat data/projects.json",
        first_lines + "\n  ...",
    )
    shoot("file:///work/data.html", "step-01-project-data", TERMINAL)

    # The server needs a database and reads the folder that holds it.
    command, output = transcript(workdir, [["init"], ["import"], ["project", "list"]])
    terminal_page(WORK / "database.html", "Terminal", command, output)
    shoot("file:///work/database.html", "step-08-database-commands", (1000, 520))

    empty = WORK / "empty"
    shutil.rmtree(empty, ignore_errors=True)
    empty.mkdir()
    command, output = transcript(empty, [["serve"]])
    terminal_page(WORK / "serve-missing.html", "Terminal", command, output)
    shoot("file:///work/serve-missing.html", "step-05-serve-command", (1000, 220))

    start_server(workdir)
    try:
        snapshot("/", "home-plain")
        without_stylesheet("home-plain")
        snapshot("/about", "about-plain")
        without_stylesheet("about-plain")
        turn = (
            "<style>.flip-card .flip-card-inner "
            "{ transform: rotateY(180deg); transition: none; }</style>"
        )
        snapshot("/", "home-flipped", extra=turn)

        shoot(
            "file:///work/home-plain.html",
            "step-02-home-page-structure",
            (1000, 900),
            network=NETWORK,
        )
        shoot(
            "file:///work/about-plain.html",
            "step-03-about-page",
            (1000, 700),
            network=NETWORK,
        )
        shoot(f"{SERVER_HOST}/", "step-04-styled-home-page", DESKTOP, network=NETWORK)
        shoot(
            f"{SERVER_HOST}/about",
            "step-04-styled-about-page",
            (1200, 800),
            network=NETWORK,
        )
        shoot(f"{SERVER_HOST}/", "step-04-narrow-screen", NARROW, network=NETWORK)
        shoot(f"{SERVER_HOST}/", "step-05-preview-server", DESKTOP, network=NETWORK)
        shoot(
            f"{SERVER_HOST}/", "step-07-flip-card-front", (1200, 800), network=NETWORK
        )
        shoot(
            "file:///work/home-flipped.html",
            "step-07-flip-card-back",
            (1200, 800),
            network=NETWORK,
        )
        shoot(
            f"{SERVER_HOST}/about", "step-07-about-page", (1200, 800), network=NETWORK
        )

        # A project added with a command shows on the next request, with no restart.
        cli(
            workdir, "project", "add", "--title", "My new project", "--kind", "Website",
            "--description", "Added with a command while the server runs.",
            "--source-code-url", "https://example.com/my-new-project",
            "--tag", "Flask", "--skill", "SQLite",
        )  # fmt: skip
        shoot(f"{SERVER_HOST}/", "step-08-project-added", (1200, 1750), network=NETWORK)
    finally:
        stop_server()

    tests = run(
        [python_exe(), "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        check=False,
    )
    terminal_page(WORK / "tests.html", "Terminal", "python -m pytest -q", tests.stdout)
    shoot("file:///work/tests.html", "step-06-tests", (1000, 420))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
