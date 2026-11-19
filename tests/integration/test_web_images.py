"""The images route against a real folder: what it serves and what it refuses."""

import os
from pathlib import Path

import pytest
from flask.testing import FlaskClient

from fakes import InMemoryDataFileReader
from portfolio.constants import IMAGE_CONTENT_TYPES
from portfolio.infrastructure.data_folder_reader import FolderDataFileReader
from web_app import make_client

SECRET = b"top secret"
PNG = b"\x89PNG\r\n\x1a\n" + bytes(range(64))


@pytest.fixture
def data(tmp_path: Path) -> Path:
    """A data folder with images and, beside the images, files that must not leak."""
    folder = tmp_path / "data"
    (folder / "images" / "sub").mkdir(parents=True)
    (folder / "images" / "a.png").write_bytes(PNG)
    (folder / "images" / "sub" / "b.svg").write_bytes(b"<svg/>")
    (folder / "images" / "notes.txt").write_bytes(SECRET)
    (folder / "images" / "page.html").write_bytes(b"<script>alert(1)</script>")
    (folder / "images" / "UPPER.PNG").write_bytes(PNG)
    (folder / "secret.png").write_bytes(SECRET)
    (folder / "projects.json").write_bytes(SECRET)
    (tmp_path / "outside.png").write_bytes(SECRET)
    return folder


@pytest.fixture
def client(data: Path) -> FlaskClient:
    return make_client(images=FolderDataFileReader(data / "images"))


def test_an_image_is_served_with_its_bytes_and_its_type(client: FlaskClient) -> None:
    response = client.get("/images/a.png")

    assert response.status_code == 200
    assert response.data == PNG
    assert response.headers["Content-Type"] == "image/png"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_an_image_in_a_sub_folder_is_served(client: FlaskClient) -> None:
    response = client.get("/images/sub/b.svg")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/svg+xml")


def test_the_ending_may_be_in_upper_case(client: FlaskClient) -> None:
    response = client.get("/images/UPPER.PNG")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"


@pytest.mark.parametrize("ending", sorted(IMAGE_CONTENT_TYPES))
def test_every_whitelisted_ending_gets_its_own_content_type(
    tmp_path: Path, ending: str
) -> None:
    (tmp_path / f"x{ending}").write_bytes(b"data")
    client = make_client(images=FolderDataFileReader(tmp_path))

    response = client.get(f"/images/x{ending}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == IMAGE_CONTENT_TYPES[ending]


@pytest.mark.parametrize("path", ["/images/notes.txt", "/images/page.html"])
def test_a_file_with_an_ending_outside_the_whitelist_is_404(
    client: FlaskClient, path: str
) -> None:
    response = client.get(path)

    assert response.status_code == 404
    assert SECRET not in response.data
    assert b"<script>alert(1)</script>" not in response.data


@pytest.mark.parametrize(
    "path",
    [
        "/images/none.png",
        "/images/sub",
        "/images/sub/",
        "/images/sub.png",
        "/images/",
        "/images",
    ],
)
def test_a_missing_file_or_a_folder_is_404(client: FlaskClient, path: str) -> None:
    assert client.get(path).status_code == 404


@pytest.mark.parametrize(
    "path",
    [
        "/images/../secret.png",
        "/images/sub/../../secret.png",
        "/images/../../outside.png",
        "/images/%2e%2e/secret.png",
        "/images/%2E%2E/secret.png",
        "/images/..%2fsecret.png",
        "/images/..%2Fsecret.png",
        "/images/%2e%2e%2fsecret.png",
        "/images/sub%2f..%2f..%2fsecret.png",
        "/images/..%5csecret.png",
        "/images/..\\secret.png",
        "/images/sub\\..\\..\\secret.png",
        "/images/%252e%252e/secret.png",
        "/images/....//secret.png",
        "/images/.%2e/secret.png",
        "/images/../projects.json",
        "/images/secret.png%00.png",
        "/images/a.png%00",
        "/images/a.png/../../secret.png",
    ],
)
def test_a_path_out_of_the_images_folder_is_404(client: FlaskClient, path: str) -> None:
    response = client.get(path)

    assert response.status_code == 404
    assert SECRET not in response.data


@pytest.mark.parametrize(
    "path",
    [
        "/images/C:/secret.png",
        "/images/C:\\secret.png",
        "/images/%2fsecret.png",
        "/images/file:///secret.png",
    ],
)
def test_a_drive_or_a_scheme_in_the_path_is_never_served(
    client: FlaskClient, path: str
) -> None:
    response = client.get(path)

    assert response.status_code != 200
    assert SECRET not in response.data


def test_an_absolute_path_is_404(client: FlaskClient, data: Path) -> None:
    absolute = str(data / "secret.png").replace("\\", "/").lstrip("/")

    response = client.get(f"/images/{absolute}")

    assert response.status_code == 404
    assert SECRET not in response.data


def test_a_symbolic_link_out_of_the_folder_is_404(
    client: FlaskClient, data: Path
) -> None:
    try:
        os.symlink(data / "secret.png", data / "images" / "link.png")
    except (OSError, NotImplementedError):
        pytest.skip("symbolic links are not available here")

    response = client.get("/images/link.png")

    assert response.status_code == 404
    assert SECRET not in response.data


def test_a_symbolic_link_to_a_file_inside_the_folder_is_served(
    client: FlaskClient, data: Path
) -> None:
    try:
        os.symlink(data / "images" / "a.png", data / "images" / "same.png")
    except (OSError, NotImplementedError):
        pytest.skip("symbolic links are not available here")

    assert client.get("/images/same.png").data == PNG


def test_a_missing_images_folder_gives_404(tmp_path: Path) -> None:
    client = make_client(images=FolderDataFileReader(tmp_path / "nothing"))

    assert client.get("/images/a.png").status_code == 404


def test_the_reader_is_not_asked_for_a_path_the_route_refuses() -> None:
    reader = InMemoryDataFileReader({"a.png": PNG, "notes.txt": SECRET})
    client = make_client(images=reader)

    for path in ("/images/notes.txt", "/images/../a.png", "/images/a.png%00"):
        assert client.get(path).status_code == 404

    assert reader.reads == []
