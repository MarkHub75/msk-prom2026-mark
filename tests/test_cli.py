import io
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

import httpx
import psutil
import pytest

from safewatch import cli, config, services
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend

# The server runs in a child process: the same isolation as conftest, data in tmp_path.
BOOT = """
import sys
from pathlib import Path
from safewatch import cli, config
config.Settings.model_config["env_file"] = None
_read = config._load_yaml
config._load_yaml = lambda p: {} if p.name == "user.yaml" else _read(p)
settings = config.get_settings().model_copy(update={"data_dir": Path(sys.argv[1]), "fake": True})
config.get_settings = lambda: settings
sys.exit(cli.main(sys.argv[2:]))
"""
START_LIMIT_S = 20


def _boot(data_dir: Path, *args: str) -> list[str]:
    return [sys.executable, "-X", "utf8", "-c", BOOT, str(data_dir), *args]


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port: int = sock.getsockname()[1]
        return port


def _wait_health(port: int, proc: subprocess.Popen[bytes]) -> httpx.Response:
    deadline = time.perf_counter() + START_LIMIT_S
    while time.perf_counter() < deadline and proc.poll() is None:
        try:
            return httpx.get(f"http://127.0.0.1:{port}/api/health", timeout=1.0)
        except httpx.TransportError:
            try:
                proc.wait(0.2)  # paces the polling; returns early if the server died
            except subprocess.TimeoutExpired:
                pass
    raise AssertionError("server did not answer /api/health in 20 s")


def test_serve_starts_and_stops(tmp_path: Path) -> None:
    port = _free_port()
    proc = subprocess.Popen(_boot(tmp_path, "serve", "--port", str(port)))
    try:
        response = _wait_health(port, proc)
        assert response.json() == {"status": "ok", "contract": "1.2.0"}
        record = json.loads((tmp_path / "server.pid").read_text(encoding="utf-8"))
        # .venv/Scripts/python.exe may be a launcher: the server is it or its child.
        launcher = psutil.Process(proc.pid)
        assert record["pid"] in [proc.pid] + [c.pid for c in launcher.children()]
        assert record["create_time"] == psutil.Process(record["pid"]).create_time()
        stop = subprocess.run(_boot(tmp_path, "stop"), capture_output=True, text=True, timeout=30)
        assert stop.returncode == 0
        assert stop.stdout.strip() == f"stopped {record['pid']}"
        proc.wait(10)
        assert not (tmp_path / "server.pid").exists()
    finally:
        proc.kill()
    with socket.socket() as busy:
        busy.bind(("127.0.0.1", port))
        busy.listen()
        taken = subprocess.run(_boot(tmp_path, "serve", "--port", str(port)), timeout=60)
    assert taken.returncode == 2


def test_stop_ignores_foreign_pid(core: Settings, capsys: pytest.CaptureFixture[str]) -> None:
    pid_file = core.data_dir / "server.pid"
    assert cli.main(["stop"]) == 0
    assert capsys.readouterr().out.strip() == "not running"
    me = psutil.Process()
    pid_file.write_text(json.dumps({"pid": me.pid, "create_time": me.create_time() - 5}), "utf-8")
    assert cli.main(["stop"]) == 1
    assert me.is_running()
    assert not pid_file.exists()


def test_doctor_fake_mode_ok(fake_core: Settings, capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert "LINQ_JUPYTER_URL: нет" in out
    assert "фейк" in out
    assert "FAIL" not in out


def test_doctor_reports_missing_keys(
    core: Settings,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert cli.main(["doctor"]) == 4
    assert "LINQ_JUPYTER_URL: нет" in capsys.readouterr().out
    secret = core.model_copy(
        update={
            "linq_jupyter_url": "http://127.0.0.1:8888/",
            "linq_jupyter_user": "team-user",
            "linq_jupyter_password": "s3cr3t-pass",
        }
    )
    monkeypatch.setattr(config, "get_settings", lambda: secret)
    # Slice 3: with keys the doctor asks backend_check(force=True); LinQ here is the fake.
    shell = FakeRemoteShell()
    shell.fault = "unavailable"
    monkeypatch.setattr(services, "_backend", LinqBackend(secret, shell))
    assert cli.main(["doctor"]) == 4
    out = capsys.readouterr().out
    assert "LINQ_JUPYTER_URL: есть" in out
    assert "FAIL связь с LinQ: unreachable" in out and shell.calls == ["check", "close"]
    for value in ("s3cr3t-pass", "team-user", "127.0.0.1:8888"):
        assert value not in out
    shell.fault = None
    cli.main(["doctor"])
    assert "ok   связь с LinQ: ok" in capsys.readouterr().out
    assert shell.calls.count("check") == 2  # force: no cache between doctor runs


def test_cli_survives_cp1252_stdout(fake_core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    raw = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(raw, encoding="cp1252"))
    assert cli.main(["doctor"]) == 0
    sys.stdout.flush()
    assert "база".encode() in raw.getvalue()
