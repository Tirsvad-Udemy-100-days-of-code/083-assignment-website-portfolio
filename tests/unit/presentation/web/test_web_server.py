"""Unit tests of the server helpers: a fake server stands in for the real one."""

import pytest

from portfolio.presentation.web.server import serve, serve_app
from web_app import make_test_app


class FakeServer:
    def __init__(self, error: BaseException | None = None) -> None:
        self.server_port = 4321
        self.closed = False
        self._error = error

    def serve_forever(self) -> None:
        if self._error is not None:
            raise self._error

    def server_close(self) -> None:
        self.closed = True


def test_serve_closes_the_server_after_it_stopped() -> None:
    server = FakeServer()

    serve(server)

    assert server.closed is True


def test_serve_reports_the_stop_on_ctrl_c_and_closes_the_server(
    capsys: pytest.CaptureFixture[str],
) -> None:
    server = FakeServer(KeyboardInterrupt())

    serve(server)

    assert server.closed is True
    assert capsys.readouterr().out == "Server stopped.\n"


def test_serve_closes_the_server_when_it_fails() -> None:
    server = FakeServer(RuntimeError("boom"))

    with pytest.raises(RuntimeError, match="boom"):
        serve(server)

    assert server.closed is True


def test_serve_app_tells_where_the_site_is(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    server = FakeServer(KeyboardInterrupt())
    calls: list[tuple[str, int]] = []

    def fake_create_server(_app: object, host: str, port: int) -> FakeServer:
        calls.append((host, port))
        return server

    monkeypatch.setattr(
        "portfolio.presentation.web.server.create_server", fake_create_server
    )

    serve_app(make_test_app(), "127.0.0.1", 0)

    assert calls == [("127.0.0.1", 0)]
    assert "Serving the portfolio at http://127.0.0.1:4321/" in capsys.readouterr().out
    assert server.closed is True
