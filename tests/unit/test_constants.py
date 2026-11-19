"""Smoke tests of the package skeleton."""

import pytest

from portfolio import __main__ as entry_point
from portfolio import constants


def test_default_host_is_loopback() -> None:
    assert constants.DEFAULT_HOST == "127.0.0.1"


def test_default_port_is_unprivileged() -> None:
    assert constants.DEFAULT_PORT > 1023


def test_main_returns_zero_without_arguments() -> None:
    assert entry_point.main([]) == 0


def test_main_prints_help_and_exits(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        entry_point.main(["--help"])
    assert exit_info.value.code == 0
    assert constants.APP_NAME in capsys.readouterr().out
