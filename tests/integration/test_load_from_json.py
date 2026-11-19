"""Integration tests of load_from_json against real files."""

from pathlib import Path

import pytest

from data_files import project_entry, write_json
from portfolio.domain.entities.project import Project
from portfolio.infrastructure.errors.data_file_error import DataFileError
from portfolio.infrastructure.load_from_json import load_from_json


def test_load_from_json_reads_the_projects_in_file_order(tmp_path: Path) -> None:
    path = write_json(
        tmp_path / "projects.json",
        [project_entry(title="First"), project_entry(title="Second", type="Game")],
    )
    projects = load_from_json(path)
    assert projects == (
        Project(
            "First",
            "Web app",
            "Shows the weather of a city.",
            "https://example.com/weather.png",
            "https://example.com/weather",
            ("Python", "API"),
            ("Working with web APIs",),
        ),
        Project(
            "Second",
            "Game",
            "Shows the weather of a city.",
            "https://example.com/weather.png",
            "https://example.com/weather",
            ("Python", "API"),
            ("Working with web APIs",),
        ),
    )


def test_load_from_json_maps_type_to_kind_and_img_url_to_image_url(
    tmp_path: Path,
) -> None:
    path = write_json(tmp_path / "p.json", [project_entry(type="Game", img_url="")])
    project = load_from_json(path)[0]
    assert project.kind == "Game"
    assert project.image_url == ""


def test_load_from_json_reads_tags_and_skills(tmp_path: Path) -> None:
    path = write_json(
        tmp_path / "p.json",
        [project_entry(tags=[" C ", "Rust"], skills=["SIMD"])],
    )
    project = load_from_json(path)[0]
    assert project.tags == ("C", "Rust")
    assert project.skills == ("SIMD",)


def test_load_from_json_defaults_tags_and_skills_to_empty(tmp_path: Path) -> None:
    entry = project_entry()
    del entry["tags"]
    del entry["skills"]
    project = load_from_json(write_json(tmp_path / "p.json", [entry]))[0]
    assert project.tags == ()
    assert project.skills == ()


def test_load_from_json_reads_a_relative_image_path(tmp_path: Path) -> None:
    path = write_json(tmp_path / "p.json", [project_entry(img_url=" images/a.svg ")])
    assert load_from_json(path)[0].image_url == "images/a.svg"


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"tags": "C"}, "project 1: 'tags' must be a JSON array"),
        ({"tags": None}, "project 1: 'tags' must be a JSON array"),
        ({"tags": ["C", 3]}, "project 1: tag 2 must be text"),
        ({"skills": {"a": 1}}, "project 1: 'skills' must be a JSON array"),
        ({"skills": [["x"]]}, "project 1: skill 1 must be text"),
        ({"tags": ["C", "  "]}, "project 1: tag must not be blank"),
        ({"skills": ["x" * 61]}, "skill must be at most 60 characters"),
        ({"tags": ["x"] * 11}, "tags must hold at most 10 entries"),
        ({"img_url": "javascript:alert(1)"}, "image_url must be"),
        ({"img_url": "../secret.png"}, "image_url must be"),
        ({"img_url": "data:image/png;base64,AAAA"}, "image_url must be"),
    ],
)
def test_load_from_json_rejects_a_bad_tag_skill_or_image(
    tmp_path: Path, overrides: dict[str, object], message: str
) -> None:
    path = write_json(tmp_path / "p.json", [project_entry(**overrides)])
    with pytest.raises(DataFileError, match=message):
        load_from_json(path)


def test_load_from_json_returns_nothing_for_an_empty_list(tmp_path: Path) -> None:
    assert load_from_json(write_json(tmp_path / "p.json", [])) == ()


def test_load_from_json_reads_unicode(tmp_path: Path) -> None:
    path = write_json(
        tmp_path / "p.json", [project_entry(title="Blåbærgrød", description="東京 ☀")]
    )
    project = load_from_json(path)[0]
    assert project.title == "Blåbærgrød"
    assert project.description == "東京 ☀"


def test_load_from_json_names_the_file_when_it_is_missing(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"
    with pytest.raises(DataFileError, match="file not found") as error:
        load_from_json(path)
    assert str(path) in str(error.value)
    assert isinstance(error.value.__cause__, FileNotFoundError)


def test_load_from_json_fails_when_the_path_is_a_folder(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="cannot read"):
        load_from_json(tmp_path)


def test_load_from_json_fails_on_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "p.json"
    path.write_text("[{", encoding="utf-8")
    with pytest.raises(DataFileError, match="invalid JSON at line 1") as error:
        load_from_json(path)
    assert str(path) in str(error.value)


def test_load_from_json_fails_on_bytes_that_are_not_utf8(tmp_path: Path) -> None:
    path = tmp_path / "p.json"
    path.write_bytes(b"[\xff\xfe]")
    with pytest.raises(DataFileError, match="cannot read"):
        load_from_json(path)


@pytest.mark.parametrize("document", [{"title": "x"}, "text", 3, None])
def test_load_from_json_fails_when_the_document_is_not_a_list(
    tmp_path: Path, document: object
) -> None:
    path = write_json(tmp_path / "p.json", document)
    with pytest.raises(DataFileError, match="must be a JSON array"):
        load_from_json(path)


def test_load_from_json_fails_when_an_entry_is_not_an_object(tmp_path: Path) -> None:
    path = write_json(tmp_path / "p.json", [project_entry(), "text"])
    with pytest.raises(DataFileError, match="project 2 must be a JSON object"):
        load_from_json(path)


@pytest.mark.parametrize(
    "key", ["title", "type", "description", "img_url", "source_code_url"]
)
def test_load_from_json_fails_when_a_key_is_missing(tmp_path: Path, key: str) -> None:
    entry = project_entry()
    del entry[key]
    path = write_json(tmp_path / "p.json", [entry])
    with pytest.raises(DataFileError, match=f"project 1 is missing the key '{key}'"):
        load_from_json(path)


def test_load_from_json_fails_when_a_value_is_not_text(tmp_path: Path) -> None:
    entry: dict[str, object] = {**project_entry(), "title": 7}
    path = write_json(tmp_path / "p.json", [entry])
    with pytest.raises(DataFileError, match="'title' must be text"):
        load_from_json(path)


def test_load_from_json_wraps_an_invalid_domain_value(tmp_path: Path) -> None:
    path = write_json(tmp_path / "p.json", [project_entry(), project_entry(title=" ")])
    with pytest.raises(DataFileError, match="project 2: title must not be blank") as e:
        load_from_json(path)
    assert e.value.__cause__ is not None


def test_load_from_json_wraps_a_value_that_is_too_long(tmp_path: Path) -> None:
    path = write_json(tmp_path / "p.json", [project_entry(title="x" * 31)])
    with pytest.raises(DataFileError, match="title must be at most 30 characters"):
        load_from_json(path)
