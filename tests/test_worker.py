"""Slices 6 and 7: the periods of the background loops come from the config (tech.md 6.6)."""

import asyncio

import pytest
from test_jobs import _tune

from safewatch import services, worker
from safewatch.config import Settings


async def _periods(monkeypatch: pytest.MonkeyPatch) -> dict[str, set[float]]:
    stop = asyncio.Event()
    sleeps: list[float] = []
    calls = {"tick": 0, "job": 0, "escalation": 0}
    real_sleep = asyncio.sleep

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)
        if len(sleeps) >= 9:
            stop.set()
        await real_sleep(0)

    def tick() -> int:
        calls["tick"] += 1
        return 0

    def escalation() -> int:
        calls["escalation"] += 1
        return 0

    async def job() -> None:
        calls["job"] += 1

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(services, "broadcast_tick", tick)
    monkeypatch.setattr(services, "escalation_tick", escalation)
    monkeypatch.setattr(services, "run_next_job", job)
    await asyncio.wait_for(worker.run_forever(stop), 5)
    assert min(calls.values()) >= 3
    return {"sleeps": set(sleeps)}


async def test_loop_periods_from_config(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    assert (await _periods(monkeypatch))["sleeps"] == {0.25, 0.5}
    tuned = {"broadcast": {"tick_ms": 100}, "jobs": {"idle_poll_ms": 700}}
    _tune(monkeypatch, core, escalation={"tick_ms": 300}, **tuned)
    assert (await _periods(monkeypatch))["sleeps"] == {0.1, 0.7, 0.3}
