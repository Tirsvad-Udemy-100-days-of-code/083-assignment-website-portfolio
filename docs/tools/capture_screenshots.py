"""Capture the screenshots of the README and the wiki.

Every image comes from this project's own output: the data file, the built
pages, the output of its commands and the served site. Nothing is taken from
the course lectures.

The pictures are taken by a headless browser in a Docker container, never on
the host desktop (a graphical test must not take the user's mouse and
keyboard). Needs Docker and the project's `.venv`.

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


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a command and return its text output; never goes through a shell."""
    return subprocess.run(  # noqa: S603
        command, capture_output=True, text=True, encoding="utf-8", check=check
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


def build_site() -> str:
    """Build the sample site and return the output of the build command."""
    site = WORK / "site"
    shutil.rmtree(site, ignore_errors=True)
    done = run(
        [python_exe(), "-m", "portfolio", "build", "--data", "data", "--out", str(site)]
    )
    return done.stdout + done.stderr


def plain_copy() -> None:
    """Copy the built site without its stylesheet, to show the bare page structure."""
    plain = WORK / "site-plain"
    shutil.rmtree(plain, ignore_errors=True)
    shutil.copytree(WORK / "site", plain)
    for page in plain.glob("*.html"):
        text = page.read_text(encoding="utf-8")
        page.write_text(
            re.sub(r"<link[^>]*stylesheet[^>]*>", "", text), encoding="utf-8"
        )


def capture_preview() -> None:
    """Serve the site from a container and take the picture from another one."""
    run(["docker", "network", "create", NETWORK], check=False)
    run(["docker", "rm", "-f", SERVER_NAME], check=False)
    run(
        [
            "docker", "run", "-d", "--rm", "--name", SERVER_NAME, "--network", NETWORK,
            "-v", f"{ROOT}:/app:ro", "-v", f"{WORK}/site:/site:ro",
            "-e", "PYTHONPATH=/app/src", "-e", "PYTHONDONTWRITEBYTECODE=1",
            PYTHON_IMAGE, "python", "-m", "portfolio", "serve",
            "--out", "/site", "--host", CONTAINER_HOST, "--port", str(SERVER_PORT),
        ]
    )  # fmt: skip
    try:
        url = f"http://{SERVER_NAME}:{SERVER_PORT}/index.html"
        for _ in range(20):
            probe = run(
                ["docker", "run", "--rm", "--network", NETWORK, "--entrypoint", "wget",
                 BROWSER_IMAGE, "-q", "-O", "/dev/null", url],
                check=False,
            )  # fmt: skip
            if probe.returncode == 0:
                break
            time.sleep(1)
        shoot(url, "step-05-preview-server", DESKTOP, network=NETWORK)
    finally:
        run(["docker", "rm", "-f", SERVER_NAME], check=False)
        run(["docker", "network", "rm", NETWORK], check=False)


def main() -> int:
    """Capture every screenshot; return the exit code."""
    WORK.mkdir(exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    build_output = build_site()
    plain_copy()

    data_text = (ROOT / "data" / "projects.json").read_text(encoding="utf-8")
    first_lines = "\n".join(data_text.splitlines()[:30])
    terminal_page(
        WORK / "data.html",
        "data/projects.json",
        "cat data/projects.json",
        first_lines + "\n  ...",
    )
    shoot("file:///work/data.html", "step-01-project-data", TERMINAL)
    shoot(
        "file:///work/site-plain/index.html", "step-02-home-page-structure", (1000, 900)
    )
    shoot("file:///work/site-plain/about.html", "step-03-about-page", (1000, 700))
    shoot("file:///work/site/index.html", "step-04-styled-home-page", DESKTOP)
    shoot("file:///work/site/about.html", "step-04-styled-about-page", (1200, 800))
    shoot("file:///work/site/index.html", "step-04-narrow-screen", NARROW)

    terminal_page(
        WORK / "build.html",
        "Terminal",
        "python -m portfolio build",
        build_output or "(no output)",
    )
    shoot("file:///work/build.html", "step-05-build-command", (1000, 220))
    capture_preview()

    tests = run(
        [python_exe(), "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        check=False,
    )
    terminal_page(WORK / "tests.html", "Terminal", "python -m pytest -q", tests.stdout)
    shoot("file:///work/tests.html", "step-06-tests", (1000, 420))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
