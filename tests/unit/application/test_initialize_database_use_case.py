"""Unit tests of the initialize_database use case."""

import pytest

from fakes import FakeDatabaseInitializer
from portfolio.application.use_cases.initialize_database import initialize_database


@pytest.mark.parametrize("created", [True, False])
def test_initialize_database_returns_what_the_initializer_reports(
    created: bool,
) -> None:
    initializer = FakeDatabaseInitializer(created)

    assert initialize_database(initializer) is created
    assert initializer.calls == 1
