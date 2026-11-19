"""End-to-end tests: build the site, serve it and fetch the pages over HTTP."""

import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from data_files import profile_document, project_entry, write_json
from portfolio import __main__ as entry_point
from portfolio.constants import (
    ABOUT_PAGE_FILE_NAME,
    DEFAULT_DATA_DIR,
    DEFAULT_HOST,
    EXIT_DATA_ERROR,
    EXIT_OK,
    EXIT_OUTPUT_ERROR,
    HOME_PAGE_FILE_NAME,
    PROFILE_FILE_NAME,
    PROJECTS_FILE_NAME,
    STYLESHEET_FILE_NAME,
)
from portfolio.presentation.commands.serve_command import create_server

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TIMEOUT_SECONDS = 5


def fetch(server: ThreadingHTTPServer, path: str) -> tuple[int, str, str]:
    url = f"http://{DEFAULT_HOST}:{server.server_port}/{path}"
    with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
        body = response.read().decode("utf-8")
        return response.status, response.headers.get("Content-Type", ""), body


@pytest.fixture
def running_server(tmp_path: Path) -> Iterator[ThreadingHTTPServer]:
    site = tmp_path / "site"
    code = entry_point.main(
        ["build", "--data", str(PROJECT_ROOT / DEFAULT_DATA_DIR), "--out", str(site)]
    )
    assert code == EXIT_OK
    server = create_server(site, DEFAULT_HOST, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=TIMEOUT_SECONDS)


def test_build_writes_the_three_files(tmp_path: Path) -> None:
    site = tmp_path / "site"
    code = entry_point.main(
        ["build", "--data", str(PROJECT_ROOT / DEFAULT_DATA_DIR), "--out", str(site)]
    )
    assert code == EXIT_OK
    for name in (HOME_PAGE_FILE_NAME, ABOUT_PAGE_FILE_NAME, STYLESHEET_FILE_NAME):
        assert (site / name).is_file()


def test_server_serves_the_home_page(running_server: ThreadingHTTPServer) -> None:
    status, content_type, body = fetch(running_server, HOME_PAGE_FILE_NAME)
    assert status == 200
    assert content_type.startswith("text/html")
    assert "Band Name Generator" in body
    assert 'class="card"' in body


def test_server_serves_the_about_page(running_server: ThreadingHTTPServer) -> None:
    status, _, body = fetch(running_server, ABOUT_PAGE_FILE_NAME)
    assert status == 200
    assert "Jens Tirsvad Nielsen" in body
    assert "Python developer in training" in body


def test_server_serves_the_stylesheet(running_server: ThreadingHTTPServer) -> None:
    status, content_type, body = fetch(running_server, STYLESHEET_FILE_NAME)
    assert status == 200
    assert content_type.startswith("text/css")
    assert "grid-template-columns" in body


def test_server_answers_the_root_with_the_home_page(
    running_server: ThreadingHTTPServer,
) -> None:
    status, _, body = fetch(running_server, "")
    assert status == 200
    assert "Band Name Generator" in body


def test_server_answers_404_for_an_unknown_page(
    running_server: ThreadingHTTPServer,
) -> None:
    with pytest.raises(urllib.error.HTTPError) as error:
        fetch(running_server, "nothing.html")
    assert error.value.code == 404


def test_built_pages_escape_markup_from_the_data(tmp_path: Path) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(
        data / PROJECTS_FILE_NAME,
        [
            project_entry(
                title="<script>alert(1)</script>", source_code_url="javascript:x"
            )
        ],
    )
    write_json(data / PROFILE_FILE_NAME, profile_document(name="<b>Eve</b>"))
    site = tmp_path / "site"
    assert entry_point.main(["build", "--data", str(data), "--out", str(site)]) == 0
    home = (site / HOME_PAGE_FILE_NAME).read_text(encoding="utf-8")
    about = (site / ABOUT_PAGE_FILE_NAME).read_text(encoding="utf-8")
    assert "<script>" not in home
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in home
    assert "javascript:" not in home
    assert "<b>Eve</b>" not in about
    assert "&lt;b&gt;Eve&lt;/b&gt;" in about


def test_build_with_no_data_files_fails_with_a_message(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = entry_point.main(["build", "--data", str(tmp_path)])
    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert captured.err.startswith("error: ")
    assert "file not found" in captured.err
    assert PROJECTS_FILE_NAME in captured.err
    assert "Traceback" not in captured.err
    assert captured.err.count("\n") == 1


def test_build_with_invalid_json_fails_with_a_message(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / PROJECTS_FILE_NAME).write_text("[", encoding="utf-8")
    code = entry_point.main(["build", "--data", str(tmp_path), "--out", str(tmp_path)])
    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert "invalid JSON" in captured.err
    assert not (tmp_path / HOME_PAGE_FILE_NAME).exists()


def test_serve_with_a_missing_output_folder_fails_with_a_message(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = entry_point.main(["serve", "--out", str(tmp_path / "nothing")])
    assert code == EXIT_OUTPUT_ERROR
    assert "does not exist" in capsys.readouterr().err
