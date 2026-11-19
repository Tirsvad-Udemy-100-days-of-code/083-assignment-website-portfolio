"""The project keeps its promise of one pinned runtime dependency: Flask."""

import re
import tomllib
from pathlib import Path
from typing import Any

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"
PINNED_FLASK = re.compile(r"^Flask==\d+(\.\d+)+$")


# tomllib itself types its result as dict[str, Any]: the keys are not known here.
def load_pyproject() -> dict[str, Any]:
    return tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))


def test_flask_is_the_only_runtime_dependency() -> None:
    dependencies = load_pyproject()["project"]["dependencies"]
    assert len(dependencies) == 1
    assert dependencies[0].startswith("Flask")


def test_flask_is_pinned_to_an_exact_version() -> None:
    dependencies = load_pyproject()["project"]["dependencies"]
    assert PINNED_FLASK.match(dependencies[0])


def test_the_templates_and_the_stylesheet_are_package_data() -> None:
    document = load_pyproject()
    package_data = document["tool"]["setuptools"]["package-data"]
    assert package_data["portfolio.presentation"] == [
        "templates/*.html",
        "static/*.css",
    ]


def test_the_domain_and_application_layers_may_not_import_the_web_framework() -> None:
    document = load_pyproject()
    contracts = document["tool"]["importlinter"]["contracts"]
    forbidden = [
        contract
        for contract in contracts
        if contract["type"] == "forbidden"
        and {"flask", "jinja2"} <= set(contract["forbidden_modules"])
    ]
    assert len(forbidden) == 1
    assert set(forbidden[0]["source_modules"]) == {
        "portfolio.domain",
        "portfolio.application",
    }
