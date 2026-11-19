"""Unit tests of the import_portfolio use case."""

import pytest

from fakes import FakeImportTarget, InMemoryProfileStore, InMemoryProjectStore
from portfolio.application.errors.data_source_error import DataSourceError
from portfolio.application.errors.database_not_empty_error import (
    DatabaseNotEmptyError,
)
from portfolio.application.errors.duplicate_project_error import DuplicateProjectError
from portfolio.application.errors.profile_not_found_error import ProfileNotFoundError
from portfolio.application.use_cases.import_portfolio import import_portfolio
from sample_data import make_profile, make_project


def test_import_hands_the_projects_and_the_profile_to_an_empty_target() -> None:
    projects = [make_project(title="A"), make_project(title="B")]
    profile = make_profile()
    target = FakeImportTarget(empty=True)

    count = import_portfolio(
        InMemoryProjectStore(projects),
        InMemoryProfileStore(profile),
        target,
        replace=False,
    )

    assert count == 2
    assert target.imported == (tuple(projects), profile)


def test_import_refuses_a_target_that_holds_data() -> None:
    target = FakeImportTarget(empty=False)

    with pytest.raises(DatabaseNotEmptyError):
        import_portfolio(
            InMemoryProjectStore([make_project()]),
            InMemoryProfileStore(make_profile()),
            target,
            replace=False,
        )

    assert target.imported is None


def test_import_replaces_the_data_of_a_filled_target_when_asked() -> None:
    target = FakeImportTarget(empty=False)

    count = import_portfolio(
        InMemoryProjectStore([make_project()]),
        InMemoryProfileStore(make_profile()),
        target,
        replace=True,
    )

    assert count == 1
    assert target.imported is not None


def test_import_of_no_projects_reports_zero() -> None:
    target = FakeImportTarget()

    count = import_portfolio(
        InMemoryProjectStore(), InMemoryProfileStore(make_profile()), target, False
    )

    assert count == 0


def test_import_rejects_a_title_that_occurs_twice() -> None:
    target = FakeImportTarget()
    projects = [make_project(title="Same"), make_project(title="Same")]

    with pytest.raises(DuplicateProjectError):
        import_portfolio(
            InMemoryProjectStore(projects),
            InMemoryProfileStore(make_profile()),
            target,
            replace=True,
        )

    assert target.imported is None


def test_import_writes_nothing_when_the_profile_cannot_be_read() -> None:
    target = FakeImportTarget()

    with pytest.raises(DataSourceError):
        import_portfolio(
            InMemoryProjectStore([make_project()]),
            InMemoryProfileStore(None),
            target,
            replace=True,
        )

    assert target.imported is None
    assert issubclass(ProfileNotFoundError, DataSourceError)
