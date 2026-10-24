"""Slice 3: backend_check (tech.md 6.1 `check` and `ls`, cache, WS `backend.status`)."""

import json
from pathlib import Path
from typing import Any

import pytest

from safewatch import config, registry, services, texts
from safewatch.config import Settings
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.hub import hub
from safewatch.inference import local, make_backend
from safewatch.inference.linq import LinqBackend
from safewatch.types import BackendStatus, WsMessage


def _linq(monkeypatch: pytest.MonkeyPatch, settings: Settings) -> FakeRemoteShell:
    shell = FakeRemoteShell()
    monkeypatch.setattr(services, "_backend", LinqBackend(settings, shell))
    return shell


def _programs(settings: Settings) -> list[str]:
    return [str(m.linq_program) for m in registry.active_models(settings)]


async def test_check_four_states(
    core: Settings, linq_tails: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = core.model_copy(update={"linq_jupyter_user": "Team-User"})
    monkeypatch.setattr(config, "get_settings", lambda: settings)
    shell = _linq(monkeypatch, settings)
    listed: list[str] = []
    real_ls = shell._ls

    def ls(cmd: str) -> str:
        listed.append(cmd)
        return real_ls(cmd)

    monkeypatch.setattr(shell, "_ls", ls)
    status = await services.backend_check(force=True)
    assert (status.backend, status.fake, status.state) == ("linq", False, "ok")
    assert status.present == _programs(settings) and status.missing == []
    assert status.latency_ms is not None and status.checked_at is not None
    assert status.message == "LinQ доступен, 2 из 2 программ"
    assert listed == ["ls -1 /auto/cache/team-user  # sw:ls"]  # login in lower case

    # The answer is ours, but a program is gone from the folder.
    detector, pose = _programs(settings)
    monkeypatch.setattr(shell, "_ls", lambda cmd: f"{detector}\nhelmet-v1.tpu\n")
    status = await services.backend_check(force=True)
    assert (status.state, status.present, status.missing) == ("models_missing", [detector], [pose])
    assert status.message == f"Нет программ: {pose}"
    # Programs are all there, a local tail file is not.
    monkeypatch.setattr(shell, "_ls", real_ls)
    tail = str(registry.resolve(settings.pipeline.pose or "").linq_tail)
    (linq_tails / tail).unlink()
    status = await services.backend_check(force=True)
    assert (status.state, status.missing) == ("models_missing", [tail])
    (linq_tails / tail).write_bytes(b"onnx")

    shell.fault = "unavailable"  # tunnel or VPN down
    status = await services.backend_check(force=True)
    assert (status.state, status.message) == ("unreachable", texts.LINQ_UNREACHABLE)
    assert status.latency_ms is None and status.present == []

    shell.fault = None
    monkeypatch.setattr(shell, "_check", lambda cmd: "<!DOCTYPE html><html>login</html>\n")
    status = await services.backend_check(force=True)
    assert (status.state, status.message) == ("bad_answer", texts.LINQ_BAD_ANSWER)


async def test_check_local_and_fake(
    core: Settings, linq_tails: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    local_settings = core.model_copy(update={"inference_backend": "local"})
    monkeypatch.setattr(config, "get_settings", lambda: local_settings)
    root = tmp_path / "local-root"
    monkeypatch.setattr(local, "ROOT", root)
    status = await services.backend_check(force=True)
    assert (status.backend, status.state) == ("local", "models_missing")
    onnx = [str(m.local_onnx) for m in registry.active_models(local_settings)]
    assert status.missing == onnx
    for name in onnx:
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes(b"onnx")
    status = await services.backend_check(force=True)
    assert (status.state, status.present, status.missing) == ("ok", onnx, [])

    fake = core.model_copy(update={"fake": True})
    monkeypatch.setattr(config, "get_settings", lambda: fake)
    monkeypatch.setattr(services, "_backend", make_backend(fake))
    status = await services.backend_check(force=True)
    assert (status.backend, status.fake, status.state) == ("linq", True, "ok")
    assert "фейк" in status.message.lower()


async def test_check_is_cached(
    core: Settings, linq_tails: Path, fake_clock: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    shell = _linq(monkeypatch, core)
    first = await services.backend_check()
    assert shell.calls.count("check") == 1
    fake_clock.advance(core.linq.check_cache_s - 0.001)
    assert await services.backend_check() == first  # within check_cache_s: no LinQ call
    assert shell.calls.count("check") == 1
    forced = await services.backend_check(force=True)
    assert shell.calls.count("check") == 2 and forced.checked_at == fake_clock.now()
    fake_clock.advance(core.linq.check_cache_s)
    await services.backend_check()
    assert shell.calls.count("check") == 3

    # Another check_cache_s changes the window.
    short = core.model_copy(update={"linq": core.linq.model_copy(update={"check_cache_s": 5})})
    monkeypatch.setattr(config, "get_settings", lambda: short)
    fake_clock.advance(5)
    await services.backend_check()
    assert shell.calls.count("check") == 4


async def test_check_publishes_status(
    core: Settings, linq_tails: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _linq(monkeypatch, core)
    client = hub.connect("master")
    status = await services.backend_check()
    message = WsMessage.model_validate(json.loads(client.queue.get_nowait() or ""))
    assert message.type == "backend.status"
    assert isinstance(message.data, BackendStatus) and message.data.state == status.state
    await services.backend_check()  # cached: nothing new on the wire
    assert client.queue.empty()
