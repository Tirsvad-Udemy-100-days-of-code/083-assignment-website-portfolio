"""No SQL text is built from values: a search of the source finds no formatted SQL.

The check reads the syntax tree of every module of the package: a string that holds
a SQL keyword must not be an f-string, must not be joined with `+` or formatted with
`%` or `.format`, and the text given to `execute` must not be built on the spot.
"""

import ast
import re
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[2] / "src" / "portfolio"
SQL_WORDS = re.compile(
    r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|PRAGMA|WHERE|VALUES)\b",
    re.IGNORECASE,
)
EXECUTE_METHODS = {"execute", "executemany", "executescript"}
MODULES = sorted(PACKAGE.rglob("*.py"))


def holds_sql(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and SQL_WORDS.search(node.value) is not None
    )


def is_built_text(node: ast.AST) -> bool:
    if isinstance(node, ast.JoinedStr | ast.BinOp):
        return True
    return isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)


def problems(path: Path) -> list[str]:
    found: list[str] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        line = getattr(node, "lineno", 0)
        if isinstance(node, ast.JoinedStr) and any(
            holds_sql(part) for part in node.values
        ):
            found.append(f"{path.name}:{line}: f-string with SQL")
        if (
            isinstance(node, ast.BinOp)
            and isinstance(node.op, ast.Add | ast.Mod)
            and (holds_sql(node.left) or holds_sql(node.right))
        ):
            found.append(f"{path.name}:{line}: SQL joined or formatted")
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "format"
            and holds_sql(node.func.value)
        ):
            found.append(f"{path.name}:{line}: SQL formatted with format()")
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in EXECUTE_METHODS
            and node.args
            and is_built_text(node.args[0])
        ):
            found.append(f"{path.name}:{line}: SQL text built in the call")
    return found


def test_the_source_has_modules_to_check() -> None:
    names = {path.name for path in MODULES}
    assert "sqlite_project_repository.py" in names
    assert "sqlite_schema.py" in names


@pytest.mark.parametrize("path", MODULES, ids=lambda path: path.name)
def test_no_module_builds_sql_from_values(path: Path) -> None:
    assert problems(path) == []


def test_the_check_finds_formatted_sql(tmp_path: Path) -> None:
    sample = tmp_path / "bad.py"
    sample.write_text(
        "def run(c, title):\n"
        '    c.execute(f"SELECT * FROM project WHERE title = {title}")\n'
        '    c.execute("SELECT * FROM project WHERE title = \'" + title + "\'")\n'
        "    c.execute(\"SELECT * FROM project WHERE title = '%s'\" % title)\n"
        '    c.execute("SELECT {}".format(title))\n',
        encoding="utf-8",
    )

    assert len(problems(sample)) >= 5
