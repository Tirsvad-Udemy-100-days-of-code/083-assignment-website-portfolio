"""Integration tests of the JSON profile repository."""

from pathlib import Path

import pytest

from data_files import profile_document, write_json
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.domain.value_objects.link import Link
from portfolio.infrastructure.errors.data_file_error import DataFileError
from portfolio.infrastructure.repositories.json_profile_repository import (
    JsonProfileRepository,
)


def test_repository_reads_the_profile(tmp_path: Path) -> None:
    path = write_json(tmp_path / "profile.json", profile_document())
    profile = JsonProfileRepository(path).get_profile()
    assert profile.name == "Ada Lovelace"
    assert profile.headline == "Software developer"
    assert profile.summary == "Builds small, tested programs."
    assert profile.skills == ("Python", "Testing")
    assert profile.links == (Link("GitHub", "https://example.com/me"),)


def test_repository_reads_the_photo_path(tmp_path: Path) -> None:
    path = write_json(
        tmp_path / "profile.json", profile_document(photo=" images/profile.jpg ")
    )
    assert JsonProfileRepository(path).get_profile().photo == "images/profile.jpg"


@pytest.mark.parametrize("photo", [None, "missing-key"])
def test_repository_gives_no_photo_when_it_is_not_set(
    tmp_path: Path, photo: str | None
) -> None:
    document = profile_document()
    if photo is None:
        document["photo"] = None
    path = write_json(tmp_path / "profile.json", document)
    assert JsonProfileRepository(path).get_profile().photo is None


def test_repository_accepts_a_profile_without_links(tmp_path: Path) -> None:
    path = write_json(tmp_path / "profile.json", profile_document(links=[]))
    assert JsonProfileRepository(path).get_profile().links == ()


def test_repository_reads_unicode(tmp_path: Path) -> None:
    path = write_json(
        tmp_path / "profile.json", profile_document(name="Søren Åberg", skills=["東京"])
    )
    profile = JsonProfileRepository(path).get_profile()
    assert profile.name == "Søren Åberg"
    assert profile.skills == ("東京",)


def test_repository_reports_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DataSourceError, match=r"profile\.json: file not found"):
        JsonProfileRepository(tmp_path / "profile.json").get_profile()


def test_repository_reports_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(DataFileError, match="invalid JSON"):
        JsonProfileRepository(path).get_profile()


@pytest.mark.parametrize("document", [[], "text", None])
def test_repository_reports_a_document_that_is_not_an_object(
    tmp_path: Path, document: object
) -> None:
    path = write_json(tmp_path / "profile.json", document)
    with pytest.raises(DataFileError, match="the profile must be a JSON object"):
        JsonProfileRepository(path).get_profile()


@pytest.mark.parametrize("key", ["name", "headline", "summary", "skills", "links"])
def test_repository_reports_a_missing_key(tmp_path: Path, key: str) -> None:
    document = profile_document()
    del document[key]
    path = write_json(tmp_path / "profile.json", document)
    with pytest.raises(DataFileError, match=f"missing the key '{key}'"):
        JsonProfileRepository(path).get_profile()


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"name": 3}, "'name' must be text"),
        ({"skills": "Python"}, "'skills' must be a JSON array"),
        ({"skills": ["Python", 3]}, "skill 2 must be text"),
        ({"photo": 3}, "'photo' must be text"),
        ({"links": {"label": "x"}}, "'links' must be a JSON array"),
        ({"links": ["GitHub"]}, "link 1 must be a JSON object"),
        ({"links": [{"label": "GitHub"}]}, "link 1 is missing the key 'url'"),
    ],
)
def test_repository_reports_a_wrong_shape(
    tmp_path: Path, overrides: dict[str, object], message: str
) -> None:
    path = write_json(tmp_path / "profile.json", profile_document(**overrides))
    with pytest.raises(DataFileError, match=message):
        JsonProfileRepository(path).get_profile()


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"name": "  "}, "name must not be blank"),
        ({"skills": []}, "skills must not be empty"),
        ({"skills": [" "]}, "skill must not be blank"),
        ({"photo": "https://example.com/me.jpg"}, "photo must be a relative path"),
        ({"photo": "../me.jpg"}, "photo must be a relative path"),
        ({"photo": "javascript:alert(1)"}, "photo must be a relative path"),
        ({"links": [{"label": "", "url": "https://x.example"}]}, "label must not be"),
    ],
)
def test_repository_wraps_an_invalid_domain_value(
    tmp_path: Path, overrides: dict[str, object], message: str
) -> None:
    path = write_json(tmp_path / "profile.json", profile_document(**overrides))
    with pytest.raises(DataFileError, match=message) as error:
        JsonProfileRepository(path).get_profile()
    assert error.value.__cause__ is not None
    assert str(path) in str(error.value)
