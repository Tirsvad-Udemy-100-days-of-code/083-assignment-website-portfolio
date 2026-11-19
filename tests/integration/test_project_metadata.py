"""The project keeps its promise of no runtime dependency."""

import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def test_the_runtime_dependencies_are_empty() -> None:
    document = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))
    assert document["project"]["dependencies"] == []
