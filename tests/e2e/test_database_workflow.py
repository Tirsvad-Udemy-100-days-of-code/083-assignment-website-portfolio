"""End-to-end tests of the commands that create and manage the SQLite database."""

import sqlite3
from pathlib import Path

import pytest

from data_files import profile_document, project_entry, write_json
from portfolio import __main__ as entry_point
from portfolio.constants import (
    DEFAULT_DATA_DIR,
    DEFAULT_DATABASE_PATH,
    EXIT_DATA_ERROR,
    EXIT_OK,
    HOME_PAGE_FILE_NAME,
    PROFILE_FILE_NAME,
    PROJECTS_FILE_NAME,
    SCHEMA_VERSION,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA = PROJECT_ROOT / DEFAULT_DATA_DIR
SAMPLE_PROJECT_COUNT = 6
HOSTILE_TITLE = "x'); DROP TABLE project;--"

# The rows of project, project_tag, project_skill and profile.
COUNT_ROWS = (
    "SELECT (SELECT COUNT(*) FROM project), (SELECT COUNT(*) FROM project_tag),"
    " (SELECT COUNT(*) FROM project_skill), (SELECT COUNT(*) FROM profile)"
)

ADD_ARGUMENTS = [
    "--title",
    "Weather app",
    "--kind",
    "Web app",
    "--description",
    "Shows the weather.",
    "--source-code-url",
    "https://example.com/weather",
]


class Result:
    def __init__(self, code: int, out: str, err: str) -> None:
        self.code = code
        self.out = out
        self.err = err

    def assert_failed_on_one_line(self, *fragments: str) -> None:
        assert self.code == EXIT_DATA_ERROR
        assert self.out == ""
        assert self.err.startswith("error: ")
        assert self.err.count("\n") == 1
        assert "Traceback" not in self.err
        for fragment in fragments:
            assert fragment in self.err


class CommandRunner:
    """Runs the program in this process and gathers what it wrote."""

    def __init__(self, capsys: pytest.CaptureFixture[str]) -> None:
        self._capsys = capsys

    def __call__(self, *arguments: str) -> Result:
        code = entry_point.main(list(arguments))
        captured = self._capsys.readouterr()
        return Result(code, captured.out, captured.err)


@pytest.fixture
def run(capsys: pytest.CaptureFixture[str]) -> CommandRunner:
    return CommandRunner(capsys)


@pytest.fixture
def db(tmp_path: Path) -> Path:
    return tmp_path / "portfolio.db"


@pytest.fixture
def ready(db: Path, run: CommandRunner) -> Path:
    """An initialised, empty database."""
    assert run("init", "--db", str(db)).code == EXIT_OK
    return db


@pytest.fixture
def filled(ready: Path, run: CommandRunner) -> Path:
    """A database that holds the sample data."""
    result = run("import", "--db", str(ready), "--data", str(SAMPLE_DATA))
    assert result.code == EXIT_OK
    return ready


def project_titles(run: CommandRunner, db: Path) -> list[str]:
    result = run("project", "list", "--db", str(db))
    assert result.code == EXIT_OK
    return [line.split(" | ")[0] for line in result.out.splitlines()]


def stored_counts(db: Path) -> tuple[int, ...]:
    connection = sqlite3.connect(db)
    try:
        return tuple(connection.execute(COUNT_ROWS).fetchone())
    finally:
        connection.close()


# init


def test_init_creates_the_database_with_the_current_schema(
    db: Path, run: CommandRunner
) -> None:
    result = run("init", "--db", str(db))

    assert result.code == EXIT_OK
    assert f"Created the database {db}" in result.out
    assert result.err == ""
    connection = sqlite3.connect(db)
    try:
        version = connection.execute("PRAGMA user_version").fetchone()[0]
    finally:
        connection.close()
    assert version == SCHEMA_VERSION


def test_init_on_an_existing_database_confirms_it_and_keeps_the_data(
    filled: Path, run: CommandRunner
) -> None:
    result = run("init", "--db", str(filled))

    assert result.code == EXIT_OK
    assert "is up to date" in result.out
    assert len(project_titles(run, filled)) == SAMPLE_PROJECT_COUNT


def test_init_stops_on_a_schema_newer_than_the_program(
    ready: Path, run: CommandRunner
) -> None:
    connection = sqlite3.connect(ready)
    connection.execute("PRAGMA user_version = 99")
    connection.close()

    result = run("init", "--db", str(ready))

    result.assert_failed_on_one_line("schema version 99", "newer")


def test_init_uses_the_default_database_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, run: CommandRunner
) -> None:
    monkeypatch.chdir(tmp_path)

    result = run("init")

    assert result.code == EXIT_OK
    assert (tmp_path / DEFAULT_DATABASE_PATH).is_file()


def test_init_refuses_a_file_that_is_not_a_sqlite_database_with_a_message(
    db: Path, run: CommandRunner
) -> None:
    db.write_text("not a database " * 50, encoding="utf-8")

    result = run("init", "--db", str(db))

    result.assert_failed_on_one_line("not a database", str(db))


@pytest.mark.parametrize(
    "arguments",
    [
        ("project", "list"),
        ("project", "remove", "A"),
        ("profile", "set", "--name", "A"),
        ("import",),
    ],
)
def test_a_command_on_a_missing_database_asks_for_init(
    db: Path, run: CommandRunner, arguments: tuple[str, ...]
) -> None:
    result = run(*arguments, "--db", str(db))

    result.assert_failed_on_one_line("run the init command")
    assert not db.exists()


def test_a_command_on_a_database_without_schema_asks_for_init(
    db: Path, run: CommandRunner
) -> None:
    sqlite3.connect(db).close()

    result = run("project", "list", "--db", str(db))

    result.assert_failed_on_one_line("init")


def test_a_command_on_a_file_that_is_not_a_database_gives_a_message(
    db: Path, run: CommandRunner
) -> None:
    db.write_text("not a database " * 50, encoding="utf-8")

    result = run("project", "list", "--db", str(db))

    result.assert_failed_on_one_line("not a database")


# import


def test_import_into_an_empty_database_loads_the_sample_data(
    ready: Path, run: CommandRunner
) -> None:
    result = run("import", "--db", str(ready), "--data", str(SAMPLE_DATA))

    assert result.code == EXIT_OK
    assert f"Imported {SAMPLE_PROJECT_COUNT} projects" in result.out
    assert project_titles(run, ready)[0] == "Prime Number Benchmark"
    assert len(project_titles(run, ready)) == SAMPLE_PROJECT_COUNT


def test_import_refuses_a_database_that_holds_data(
    filled: Path, run: CommandRunner
) -> None:
    before = stored_counts(filled)

    result = run("import", "--db", str(filled), "--data", str(SAMPLE_DATA))

    result.assert_failed_on_one_line("--replace")
    assert stored_counts(filled) == before


def test_import_with_replace_overwrites_the_stored_data(
    filled: Path, run: CommandRunner, tmp_path: Path
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(data / PROJECTS_FILE_NAME, [project_entry(title="Only one")])
    write_json(data / PROFILE_FILE_NAME, profile_document(name="Grace Hopper"))

    result = run("import", "--db", str(filled), "--data", str(data), "--replace")

    assert result.code == EXIT_OK
    assert "Imported 1 projects" in result.out
    assert project_titles(run, filled) == ["Only one"]


def test_import_of_an_empty_project_list_reports_zero(
    ready: Path, run: CommandRunner, tmp_path: Path
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(data / PROJECTS_FILE_NAME, [])
    write_json(data / PROFILE_FILE_NAME, profile_document())

    result = run("import", "--db", str(ready), "--data", str(data))

    assert result.code == EXIT_OK
    assert "Imported 0 projects" in result.out


def test_import_leaves_nothing_behind_when_the_profile_file_is_invalid(
    ready: Path, run: CommandRunner, tmp_path: Path
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(data / PROJECTS_FILE_NAME, [project_entry()])
    (data / PROFILE_FILE_NAME).write_text("{", encoding="utf-8")

    result = run("import", "--db", str(ready), "--data", str(data))

    result.assert_failed_on_one_line("invalid JSON")
    assert stored_counts(ready) == (0, 0, 0, 0)


def test_import_leaves_nothing_behind_when_a_project_is_invalid(
    ready: Path, run: CommandRunner, tmp_path: Path
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(
        data / PROJECTS_FILE_NAME,
        [
            project_entry(title="Good"),
            project_entry(title="Bad", img_url="javascript:x"),
        ],
    )
    write_json(data / PROFILE_FILE_NAME, profile_document())

    result = run("import", "--db", str(ready), "--data", str(data))

    result.assert_failed_on_one_line("project 2", "image_url")
    assert stored_counts(ready) == (0, 0, 0, 0)


def test_import_leaves_nothing_behind_when_a_title_occurs_twice(
    ready: Path, run: CommandRunner, tmp_path: Path
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    write_json(data / PROJECTS_FILE_NAME, [project_entry(), project_entry()])
    write_json(data / PROFILE_FILE_NAME, profile_document())

    result = run("import", "--db", str(ready), "--data", str(data))

    result.assert_failed_on_one_line("already exists")
    assert stored_counts(ready) == (0, 0, 0, 0)


def test_import_with_a_missing_data_folder_gives_a_message(
    ready: Path, run: CommandRunner, tmp_path: Path
) -> None:
    result = run("import", "--db", str(ready), "--data", str(tmp_path / "none"))

    result.assert_failed_on_one_line("file not found")


# project list, add, set, remove


def test_project_list_of_a_new_database_says_there_is_no_project(
    ready: Path, run: CommandRunner
) -> None:
    result = run("project", "list", "--db", str(ready))

    assert result.code == EXIT_OK
    assert result.out == "No projects.\n"


def test_project_add_stores_a_project_with_tags_and_skills(
    ready: Path, run: CommandRunner
) -> None:
    result = run(
        "project",
        "add",
        "--db",
        str(ready),
        *ADD_ARGUMENTS,
        "--image-url",
        "https://example.com/weather.png",
        "--tag",
        "Python",
        "--tag",
        "API",
        "--skill",
        "Web APIs",
    )

    assert result.code == EXIT_OK
    assert "Added the project 'Weather app'" in result.out
    listing = run("project", "list", "--db", str(ready))
    assert listing.out == "Weather app | Web app | https://example.com/weather\n"
    connection = sqlite3.connect(ready)
    try:
        tags = connection.execute(
            "SELECT value FROM project_tag ORDER BY position"
        ).fetchall()
    finally:
        connection.close()
    assert tags == [("Python",), ("API",)]


def test_project_add_places_the_project_after_the_others(
    filled: Path, run: CommandRunner
) -> None:
    run("project", "add", "--db", str(filled), *ADD_ARGUMENTS)

    titles = project_titles(run, filled)

    assert len(titles) == SAMPLE_PROJECT_COUNT + 1
    assert titles[-1] == "Weather app"


@pytest.mark.parametrize(
    ("override", "fragment"),
    [
        (["--title", " "], "title must not be blank"),
        (["--title", "x" * 31], "title must be at most 30 characters"),
        (["--kind", "x" * 31], "kind must be at most 30 characters"),
        (["--description", "x" * 251], "description must be at most 250"),
        (["--image-url", "javascript:alert(1)"], "image_url must be"),
        (["--image-url", "../secret.png"], "image_url must be"),
        (["--image-url", "images/readme.txt"], "image_url must be"),
        (["--source-code-url", " "], "source_code_url must not be blank"),
        (["--tag", " "], "tag must not be blank"),
        (["--tag", "x" * 31], "tag must be at most 30 characters"),
        (["--skill", "x" * 61], "skill must be at most 60 characters"),
    ],
)
def test_project_add_rejects_an_invalid_value_and_stores_nothing(
    ready: Path, run: CommandRunner, override: list[str], fragment: str
) -> None:
    arguments = [*ADD_ARGUMENTS, *override]
    # A later option wins over an earlier one for a single value in argparse.
    result = run("project", "add", "--db", str(ready), *arguments)

    result.assert_failed_on_one_line(fragment)
    assert stored_counts(ready) == (0, 0, 0, 0)


def test_project_add_rejects_more_than_the_largest_number_of_tags(
    ready: Path, run: CommandRunner
) -> None:
    tags = [part for number in range(11) for part in ("--tag", f"t{number}")]

    result = run("project", "add", "--db", str(ready), *ADD_ARGUMENTS, *tags)

    result.assert_failed_on_one_line("at most 10")
    assert stored_counts(ready) == (0, 0, 0, 0)


def test_project_add_accepts_the_largest_number_of_tags(
    ready: Path, run: CommandRunner
) -> None:
    tags = [part for number in range(10) for part in ("--tag", f"t{number}")]

    result = run("project", "add", "--db", str(ready), *ADD_ARGUMENTS, *tags)

    assert result.code == EXIT_OK
    assert stored_counts(ready)[1] == 10


def test_project_add_rejects_a_title_that_is_taken(
    ready: Path, run: CommandRunner
) -> None:
    run("project", "add", "--db", str(ready), *ADD_ARGUMENTS)

    result = run("project", "add", "--db", str(ready), *ADD_ARGUMENTS)

    result.assert_failed_on_one_line("already exists", "Weather app")
    assert project_titles(run, ready) == ["Weather app"]


def test_project_set_changes_the_given_fields_and_keeps_the_rest(
    ready: Path, run: CommandRunner
) -> None:
    run(
        "project",
        "add",
        "--db",
        str(ready),
        *ADD_ARGUMENTS,
        "--tag",
        "a",
        "--skill",
        "s",
    )

    result = run("project", "set", "Weather app", "--db", str(ready), "--kind", "CLI")

    assert result.code == EXIT_OK
    assert "Changed the project 'Weather app'" in result.out
    listing = run("project", "list", "--db", str(ready))
    assert listing.out == "Weather app | CLI | https://example.com/weather\n"
    assert stored_counts(ready)[1:3] == (1, 1)


def test_project_set_renames_a_project_and_keeps_its_place(
    filled: Path, run: CommandRunner
) -> None:
    before = project_titles(run, filled)

    result = run(
        "project",
        "set",
        before[1],
        "--db",
        str(filled),
        "--new-title",
        "Renamed",
        "--tag",
        "x",
        "--tag",
        "y",
    )

    assert result.code == EXIT_OK
    after = project_titles(run, filled)
    assert after == [before[0], "Renamed", *before[2:]]


def test_project_set_rejects_an_invalid_value_and_keeps_the_project(
    filled: Path, run: CommandRunner
) -> None:
    before = run("project", "list", "--db", str(filled)).out

    result = run(
        "project",
        "set",
        "Prime Number Benchmark",
        "--db",
        str(filled),
        "--image-url",
        "javascript:alert(1)",
    )

    result.assert_failed_on_one_line("image_url must be")
    assert run("project", "list", "--db", str(filled)).out == before


def test_project_set_without_a_new_value_is_refused(
    filled: Path, run: CommandRunner
) -> None:
    result = run("project", "set", "Prime Number Benchmark", "--db", str(filled))

    result.assert_failed_on_one_line("nothing to change")


def test_project_set_of_an_unknown_project_is_refused(
    filled: Path, run: CommandRunner
) -> None:
    result = run("project", "set", "Nothing", "--db", str(filled), "--kind", "CLI")

    result.assert_failed_on_one_line("no project has the title 'Nothing'")


def test_project_set_to_a_title_that_is_taken_is_refused(
    filled: Path, run: CommandRunner
) -> None:
    titles = project_titles(run, filled)

    result = run(
        "project", "set", titles[0], "--db", str(filled), "--new-title", titles[1]
    )

    result.assert_failed_on_one_line("already exists")
    assert project_titles(run, filled) == titles


def test_project_remove_removes_the_project_and_its_lists(
    filled: Path, run: CommandRunner
) -> None:
    before = project_titles(run, filled)
    counts_before = stored_counts(filled)

    result = run("project", "remove", before[0], "--db", str(filled))

    assert result.code == EXIT_OK
    assert f"Removed the project '{before[0]}'" in result.out
    assert project_titles(run, filled) == before[1:]
    after = stored_counts(filled)
    assert after[0] == counts_before[0] - 1
    assert after[1] < counts_before[1]
    assert after[2] < counts_before[2]


def test_project_remove_of_an_unknown_project_is_refused(
    filled: Path, run: CommandRunner
) -> None:
    result = run("project", "remove", "Nothing", "--db", str(filled))

    result.assert_failed_on_one_line("no project has the title 'Nothing'")
    assert len(project_titles(run, filled)) == SAMPLE_PROJECT_COUNT


# profile set


def test_profile_set_creates_the_profile_from_the_required_fields(
    ready: Path, run: CommandRunner
) -> None:
    result = run(
        "profile",
        "set",
        "--db",
        str(ready),
        "--name",
        "Grace Hopper",
        "--headline",
        "Compiler pioneer",
        "--summary",
        "Wrote the first compiler.",
        "--skill",
        "COBOL",
        "--skill",
        "Leadership",
        "--link",
        "Site=https://example.com/?a=b",
    )

    assert result.code == EXIT_OK
    assert result.out == "Created the profile\n"
    connection = sqlite3.connect(ready)
    try:
        link = connection.execute("SELECT label, url FROM profile_link").fetchall()
        skills = connection.execute(
            "SELECT skill FROM profile_skill ORDER BY position"
        ).fetchall()
    finally:
        connection.close()
    assert link == [("Site", "https://example.com/?a=b")]
    assert skills == [("COBOL",), ("Leadership",)]


@pytest.mark.parametrize(
    "arguments",
    [
        ["--headline", "h", "--summary", "s", "--skill", "x"],
        ["--name", "n", "--summary", "s", "--skill", "x"],
        ["--name", "n", "--headline", "h", "--skill", "x"],
        ["--name", "n", "--headline", "h", "--summary", "s"],
    ],
)
def test_profile_set_refuses_a_new_profile_that_lacks_a_required_field(
    ready: Path, run: CommandRunner, arguments: list[str]
) -> None:
    result = run("profile", "set", "--db", str(ready), *arguments)

    result.assert_failed_on_one_line("new profile needs")
    assert stored_counts(ready)[3] == 0


def test_profile_set_changes_the_given_fields_and_keeps_the_others(
    filled: Path, run: CommandRunner
) -> None:
    result = run("profile", "set", "--db", str(filled), "--headline", "A new headline")

    assert result.code == EXIT_OK
    assert result.out == "Changed the profile\n"
    connection = sqlite3.connect(filled)
    try:
        name, headline, photo = connection.execute(
            "SELECT name, headline, photo FROM profile"
        ).fetchone()
        links = connection.execute("SELECT COUNT(*) FROM profile_link").fetchone()[0]
        skills = connection.execute("SELECT COUNT(*) FROM profile_skill").fetchone()[0]
    finally:
        connection.close()
    assert (name, headline, photo) == (
        "Jens Tirsvad Nielsen",
        "A new headline",
        "images/profile.jpg",
    )
    assert (links, skills) == (2, 8)


def test_profile_set_replaces_the_skills_and_the_links(
    filled: Path, run: CommandRunner
) -> None:
    result = run(
        "profile",
        "set",
        "--db",
        str(filled),
        "--skill",
        "Rust",
        "--link",
        "Blog=https://example.com/blog",
        "--photo",
        "images/me.png",
    )

    assert result.code == EXIT_OK
    connection = sqlite3.connect(filled)
    try:
        skills = connection.execute("SELECT skill FROM profile_skill").fetchall()
        links = connection.execute("SELECT label, url FROM profile_link").fetchall()
        photo = connection.execute("SELECT photo FROM profile").fetchone()[0]
    finally:
        connection.close()
    assert skills == [("Rust",)]
    assert links == [("Blog", "https://example.com/blog")]
    assert photo == "images/me.png"


@pytest.mark.parametrize(
    ("arguments", "fragment"),
    [
        (["--name", " "], "name must not be blank"),
        (["--photo", "../me.png"], "photo must be"),
        (["--photo", "me.txt"], "photo must be"),
        (["--skill", " "], "skill must not be blank"),
        (["--link", "no-separator"], "must look like LABEL=URL"),
        (["--link", "=https://example.com"], "label must not be blank"),
        (["--link", "Label="], "url must not be blank"),
        ([], "nothing to change"),
    ],
)
def test_profile_set_rejects_an_invalid_value_and_keeps_the_profile(
    filled: Path, run: CommandRunner, arguments: list[str], fragment: str
) -> None:
    result = run("profile", "set", "--db", str(filled), *arguments)

    result.assert_failed_on_one_line(fragment)
    connection = sqlite3.connect(filled)
    try:
        name = connection.execute("SELECT name FROM profile").fetchone()[0]
        links = connection.execute("SELECT COUNT(*) FROM profile_link").fetchone()[0]
    finally:
        connection.close()
    assert (name, links) == ("Jens Tirsvad Nielsen", 2)


# hostile input and the unchanged commands


def test_hostile_titles_are_stored_and_shown_literally_through_the_commands(
    ready: Path, run: CommandRunner
) -> None:
    add = [a if a != "Weather app" else HOSTILE_TITLE for a in ADD_ARGUMENTS]
    assert run("project", "add", "--db", str(ready), *add).code == EXIT_OK
    robert = ["--title", "Robert'); --", *ADD_ARGUMENTS[2:]]
    assert run("project", "add", "--db", str(ready), *robert).code == EXIT_OK

    listing = run("project", "list", "--db", str(ready))

    assert listing.out.splitlines()[0].startswith(HOSTILE_TITLE)
    assert listing.out.splitlines()[1].startswith("Robert'); --")
    assert stored_counts(ready)[0] == 2

    assert (
        run("project", "set", HOSTILE_TITLE, "--db", str(ready), "--kind", "'; --").code
        == EXIT_OK
    )
    assert run("project", "remove", HOSTILE_TITLE, "--db", str(ready)).code == EXIT_OK
    assert project_titles(run, ready) == ["Robert'); --"]


def test_a_title_that_looks_like_a_condition_removes_nothing(
    filled: Path, run: CommandRunner
) -> None:
    result = run("project", "remove", "' OR '1'='1", "--db", str(filled))

    result.assert_failed_on_one_line("no project has the title")
    assert len(project_titles(run, filled)) == SAMPLE_PROJECT_COUNT


def test_build_still_reads_the_json_files_and_ignores_the_database(
    filled: Path, run: CommandRunner, tmp_path: Path
) -> None:
    run("project", "remove", "Prime Number Benchmark", "--db", str(filled))
    site = tmp_path / "site"

    result = run("build", "--data", str(SAMPLE_DATA), "--out", str(site))

    assert result.code == EXIT_OK
    home = (site / HOME_PAGE_FILE_NAME).read_text(encoding="utf-8")
    assert "Prime Number Benchmark" in home
