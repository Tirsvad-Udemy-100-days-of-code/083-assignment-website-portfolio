"""End-to-end tests: build the site, serve it and fetch the pages over HTTP."""

import html
import json
import re
import shutil
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
    assert "Prime Number Benchmark" in body
    assert 'class="flip-card"' in body


def test_server_serves_the_about_page(running_server: ThreadingHTTPServer) -> None:
    status, _, body = fetch(running_server, ABOUT_PAGE_FILE_NAME)
    assert status == 200
    assert "Jens Tirsvad Nielsen" in body
    assert "Software developer" in body
    assert "https://www.linkedin.com/in/tirsvad74/" in body


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
    assert "Prime Number Benchmark" in body


def test_server_serves_a_copied_image(running_server: ThreadingHTTPServer) -> None:
    status, content_type, body = fetch(running_server, "images/prime-numbers-c.svg")
    assert status == 200
    assert content_type.startswith("image/svg+xml")
    assert body.startswith("<svg")


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


def build_real_data(tmp_path: Path) -> Path:
    site = tmp_path / "site"
    code = entry_point.main(
        ["build", "--data", str(PROJECT_ROOT / DEFAULT_DATA_DIR), "--out", str(site)]
    )
    assert code == EXIT_OK
    return site


def load_sample_projects() -> list[dict[str, object]]:
    text = (PROJECT_ROOT / DEFAULT_DATA_DIR / PROJECTS_FILE_NAME).read_text("utf-8")
    projects: list[dict[str, object]] = json.loads(text)
    return projects


def string_list(project: dict[str, object], key: str) -> list[str]:
    value = project[key]
    assert isinstance(value, list)
    return [str(item) for item in value]


def test_home_page_has_one_flip_card_with_both_faces_per_project(
    tmp_path: Path,
) -> None:
    home = (build_real_data(tmp_path) / HOME_PAGE_FILE_NAME).read_text("utf-8")
    projects = load_sample_projects()
    cards = home.split('<article class="flip-card" tabindex="0">')[1:]
    assert len(projects) == 6
    assert len(cards) == len(projects)
    for project, card in zip(projects, cards, strict=True):
        front, back = card.split('<div class="flip-card-face flip-card-back">')
        assert html.escape(str(project["title"])) in front
        assert html.escape(str(project["description"])) in front
        assert f'src="{project["img_url"]}"' in front
        assert f'href="{project["source_code_url"]}"' in back
        assert 'rel="noopener noreferrer">Source code</a>' in back
        for tag in string_list(project, "tags"):
            assert f'<li class="tag">{html.escape(tag)}</li>' in back
        for skill in string_list(project, "skills"):
            assert f"<li>{html.escape(skill)}</li>" in back


def test_build_copies_every_project_image_unchanged(tmp_path: Path) -> None:
    site = build_real_data(tmp_path)
    data = PROJECT_ROOT / DEFAULT_DATA_DIR
    for project in load_sample_projects():
        relative = str(project["img_url"])
        assert (site / relative).read_bytes() == (data / relative).read_bytes()


AVATAR_IMAGE_PATTERN = r'<img class="avatar" src="([^"]+)" alt="([^"]+)">'


def copy_sample_data(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    shutil.copytree(PROJECT_ROOT / DEFAULT_DATA_DIR, data)
    return data


def set_photo(data: Path, photo: str | None) -> None:
    """Point the profile at `photo`, or remove the key when it is None."""
    profile_path = data / PROFILE_FILE_NAME
    profile = json.loads(profile_path.read_text("utf-8"))
    if photo is None:
        profile.pop("photo", None)
    else:
        profile["photo"] = photo
    write_json(profile_path, profile)


def test_about_page_links_to_linkedin_and_shows_the_real_profile_photo(
    tmp_path: Path,
) -> None:
    site = build_real_data(tmp_path)
    about = (site / ABOUT_PAGE_FILE_NAME).read_text("utf-8")
    assert (
        '<a href="https://www.linkedin.com/in/tirsvad74/" '
        'rel="noopener noreferrer">LinkedIn</a>'
    ) in about
    assert "https://github.com/Tirsvad" in about
    match = re.search(AVATAR_IMAGE_PATTERN, about)
    assert match is not None
    assert match.group(1) == "images/profile.jpg"
    assert match.group(2) == "Jens Tirsvad Nielsen"
    assert "avatar-initials" not in about
    copied = (site / "images" / "profile.jpg").read_bytes()
    assert (
        copied
        == (PROJECT_ROOT / DEFAULT_DATA_DIR / "images" / "profile.jpg").read_bytes()
    )


def test_about_page_shows_the_initials_avatar_when_the_profile_has_no_photo(
    tmp_path: Path,
) -> None:
    data = copy_sample_data(tmp_path)
    set_photo(data, None)
    site = tmp_path / "site"
    assert entry_point.main(["build", "--data", str(data), "--out", str(site)]) == 0
    about = (site / ABOUT_PAGE_FILE_NAME).read_text("utf-8")
    assert (
        '<a href="https://www.linkedin.com/in/tirsvad74/" '
        'rel="noopener noreferrer">LinkedIn</a>'
    ) in about
    assert '<div class="avatar avatar-initials" aria-hidden="true">JN</div>' in about
    assert '<img class="avatar"' not in about
    assert not (site / "images" / "profile.jpg").exists()


def build_with_photo(tmp_path: Path, photo_bytes: bytes) -> Path:
    data = copy_sample_data(tmp_path)
    (data / "images" / "profile.png").write_bytes(photo_bytes)
    set_photo(data, "images/profile.png")
    site = tmp_path / "site"
    assert entry_point.main(["build", "--data", str(data), "--out", str(site)]) == 0
    return site


def test_about_page_shows_the_supplied_photo_and_the_build_copies_it(
    tmp_path: Path,
) -> None:
    photo = b"\x89PNG\r\n\x1a\n" + bytes(range(32))
    site = build_with_photo(tmp_path, photo)
    about = (site / ABOUT_PAGE_FILE_NAME).read_text("utf-8")
    match = re.search(AVATAR_IMAGE_PATTERN, about)
    assert match is not None
    assert match.group(1) == "images/profile.png"
    assert match.group(2) == "Jens Tirsvad Nielsen"
    assert "avatar-initials" not in about
    assert (site / match.group(1)).read_bytes() == photo


def test_build_fails_with_a_message_when_the_photo_file_is_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data = copy_sample_data(tmp_path)
    (data / "images" / "profile.jpg").unlink()
    site = tmp_path / "site"
    code = entry_point.main(["build", "--data", str(data), "--out", str(site)])
    captured = capsys.readouterr()
    assert code == EXIT_DATA_ERROR
    assert "profile.jpg" in captured.err
    assert "file not found" in captured.err
    assert "Traceback" not in captured.err
    assert not site.exists()


@pytest.mark.parametrize(
    "image",
    [
        "javascript:alert(1)",
        "data:image/png;base64,AAAA",
        "../secret.png",
        "/etc/a.png",
    ],
)
def test_build_fails_with_a_message_for_an_unsafe_project_image(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], image: str
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(data / PROJECTS_FILE_NAME, [project_entry(img_url=image)])
    write_json(data / PROFILE_FILE_NAME, profile_document())
    site = tmp_path / "site"
    code = entry_point.main(["build", "--data", str(data), "--out", str(site)])
    assert code == EXIT_DATA_ERROR
    assert "image_url must be" in capsys.readouterr().err
    assert not site.exists()


def test_build_fails_with_a_message_when_a_project_image_is_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(data / PROJECTS_FILE_NAME, [project_entry(img_url="images/none.svg")])
    write_json(data / PROFILE_FILE_NAME, profile_document())
    code = entry_point.main(
        ["build", "--data", str(data), "--out", str(tmp_path / "s")]
    )
    assert code == EXIT_DATA_ERROR
    assert "none.svg: file not found" in capsys.readouterr().err
