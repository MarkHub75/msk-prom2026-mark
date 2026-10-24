import asyncio
import inspect
import os
import sqlite3
import webbrowser
from collections.abc import AsyncIterator, Callable, Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import cv2
import httpx
import numpy as np
import pytest

from safewatch import clock, config, services, store, worker
from safewatch.config import ENV_KEYS, ENV_NAMES, Settings, get_settings
from safewatch.db import connect, migrate
from safewatch.hub import hub

ROOT = Path(__file__).resolve().parents[1]

# Isolation from the owner's machine, part 1: config/user.yaml (budgets, sizes tuned for a live
# check) must not change what tests see. Tests read the committed yaml files only.
_read_yaml = config._load_yaml


def _without_user_yaml(path: Path) -> dict[str, Any]:
    return {} if path.name == "user.yaml" else _read_yaml(path)


config._load_yaml = _without_user_yaml

# Part 2: keys from .env and the environment must not reach tests. The .env file is not read
# at all, the variables are dropped, and fixtures blank every key once more.
Settings.model_config["env_file"] = None
for _name in ENV_NAMES.values():
    os.environ.pop(_name, None)
get_settings.cache_clear()

# Switches keep their own values in the fixtures; a non-string switch belongs here too.
SWITCHES = {"fake", "inference_backend"}
NO_KEYS = {name: "" for name in ENV_KEYS if name not in SWITCHES}

# Part 3: calls that leave the test process (browser, OS notifications, sounds). Add the
# project's own (module, attribute) pairs in the slice that brings them.
SIDE_EFFECTS: list[tuple[object, str]] = [(webbrowser, "open")]


@pytest.fixture(autouse=True)
def side_effects(monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, tuple[object, ...]]]:
    """What the code tried to open or show: tests never reach a real browser or toast."""
    seen: list[tuple[str, tuple[object, ...]]] = []
    for owner, name in SIDE_EFFECTS:
        original = getattr(owner, name)

        def record(*args: object, _name: str = name, **kwargs: object) -> bool:
            seen.append((_name, args))
            return True

        async def record_async(*args: object, _name: str = name, **kwargs: object) -> bool:
            return record(*args, _name=_name)

        stub = record_async if inspect.iscoroutinefunction(original) else record
        monkeypatch.setattr(owner, name, stub)
    return seen


@pytest.fixture
def conn(monkeypatch: pytest.MonkeyPatch) -> Iterator[sqlite3.Connection]:
    """Fresh in-memory database, also used by `store`; lazy singletons start over."""
    db = connect(":memory:")
    migrate(db)
    monkeypatch.setattr(store, "_conn", db)
    monkeypatch.setattr(store, "_depth", 0)
    monkeypatch.setattr(hub, "clients", set())
    monkeypatch.setattr(services, "_backend", None)
    monkeypatch.setattr(services, "_backend_status", None)
    monkeypatch.setattr(services, "_camera_seen", {})
    monkeypatch.setattr(services, "_sector_seen", {})
    monkeypatch.setattr(services, "_preview_cache", {})
    yield db
    db.close()


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Committed config, no keys, no fakes, LinQ backend, data in `tmp_path`."""
    update = {**NO_KEYS, "data_dir": tmp_path, "fake": False, "inference_backend": "linq"}
    return get_settings().model_copy(update=update)


@pytest.fixture
def core(settings: Settings, conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch) -> Settings:
    """`services` on a fresh database with test settings."""
    monkeypatch.setattr(config, "get_settings", lambda: settings)
    return settings


@pytest.fixture
def fake_core(core: Settings, monkeypatch: pytest.MonkeyPatch) -> Settings:
    """`services` with SAFEWATCH_FAKE=1: LinQ is FakeRemoteShell."""
    fake = core.model_copy(update={"fake": True})
    monkeypatch.setattr(config, "get_settings", lambda: fake)
    return fake


@pytest.fixture
async def client(
    core: Settings, monkeypatch: pytest.MonkeyPatch
) -> AsyncIterator[httpx.AsyncClient]:
    """The app over ASGI with its lifespan; the background worker is off."""
    from safewatch.api import create_app

    async def idle(stop: asyncio.Event) -> None:
        return None

    monkeypatch.setattr(worker, "run_forever", idle)
    app = create_app(core)
    started, done = asyncio.Event(), asyncio.Event()

    # ASGITransport skips lifespan; anyio wants it entered and left in one task.
    async def run_lifespan() -> None:
        async with app.router.lifespan_context(app):
            started.set()
            await done.wait()

    task = asyncio.create_task(run_lifespan())
    await started.wait()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://127.0.0.1") as c:
        yield c
    done.set()
    await task


class FakeClock:
    def __init__(self, start: datetime) -> None:
        self.current = start

    def now(self) -> datetime:
        return self.current

    def advance(self, seconds: float) -> None:
        self.current += timedelta(seconds=seconds)


@pytest.fixture
def fake_clock(monkeypatch: pytest.MonkeyPatch) -> FakeClock:
    """`clock.now` frozen at 2026-10-24 09:00 UTC; tests move it with `advance`."""
    fake = FakeClock(datetime(2026, 10, 24, 9, 0, tzinfo=UTC))
    monkeypatch.setattr(clock, "now", fake.now)
    return fake


MakeVideo = Callable[..., Path]


@pytest.fixture
def make_video() -> MakeVideo:
    """Write an mp4 (FourCC mp4v) of flat frames; `luma` sets their brightness."""

    def make(
        tmp_path: Path,
        seconds: float,
        fps: float,
        size: tuple[int, int] = (320, 240),
        luma: int | None = None,
        name: str = "clip.mp4",
    ) -> Path:
        path = tmp_path / name
        writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
        frames = max(1, round(seconds * fps))
        for i in range(frames):
            value = luma if luma is not None else 60 + i % 120
            writer.write(np.full((size[1], size[0], 3), value, dtype=np.uint8))
        writer.release()
        return path

    return make


@pytest.fixture
def linq_tails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Tail ONNX files of every registry model, empty, under a fake repo root (CI has none)."""
    from safewatch import registry
    from safewatch.inference import linq

    root = tmp_path / "repo"
    for model in registry.load_models(registry.MODELS_FILE):
        if model.linq_tail:
            (root / model.linq_tail).parent.mkdir(parents=True, exist_ok=True)
            (root / model.linq_tail).write_bytes(b"onnx")
    monkeypatch.setattr(linq, "ROOT", root)
    return root
