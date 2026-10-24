"""Slice 8: the demo story through the API, from the upload to the master (fake LinQ)."""

from pathlib import Path

import httpx
import pytest
from conftest import FakeClock
from test_analysis_api import _textured

from safewatch import config, services
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend
from safewatch.types import EventDetail, EventSummary, MasterInbox

ADMIN, OPERATOR, MASTER = {"X-Role": "admin"}, {"X-Role": "operator"}, {"X-Role": "master"}


async def _act(client: httpx.AsyncClient, event_id: int, role: dict[str, str], **body: str) -> str:
    r = await client.post(f"/api/events/{event_id}/actions", json=body, headers=role)
    assert r.status_code == 200, r.text
    return EventDetail.model_validate(r.json()).event.status


async def test_upload_to_master_flow(
    client: httpx.AsyncClient,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
    fake_clock: FakeClock,
) -> None:
    monkeypatch.setattr(services, "_backend", LinqBackend(config.get_settings(), FakeRemoteShell()))
    r = await client.post("/api/sectors", json={"name": "Сектор 7 · Цех"}, headers=ADMIN)
    body = {"sector_id": r.json()["id"], "name": "Камера 1"}
    camera_id = (await client.post("/api/cameras", json=body, headers=ADMIN)).json()["id"]
    clip = _textured(tmp_path / "demo.mp4").read_bytes()  # the name picks the demo scene
    files = {"file": ("demo.mp4", clip, "video/mp4")}
    r = await client.post(f"/api/cameras/{camera_id}/videos", files=files, headers=ADMIN)
    assert r.status_code == 201, r.text
    job = await services.run_next_job()  # the background worker is off in tests
    assert job is not None and job.status == "done"
    r = await client.get(f"/api/cameras/{camera_id}/broadcast")
    assert r.json()["status"] == "playing"  # autostart
    # The broadcast plays by the server clock until the fall reaches the operator feed.
    red = None
    for _ in range(40):
        fake_clock.advance(0.5)
        services.broadcast_tick()  # one step of the worker's broadcast loop
        feed = (await client.get("/api/operator/feed", headers=OPERATOR)).json()
        red = next((e for e in map(EventSummary.model_validate, feed) if e.level == "red"), None)
        if red is not None:
            break
    assert red is not None
    event_id = red.id
    assert await _act(client, event_id, OPERATOR, action="confirm") == "sent_to_master"
    inbox = MasterInbox.model_validate((await client.get("/api/master/inbox")).json())
    assert [e.id for e in inbox.active] == [event_id]
    assert await _act(client, event_id, MASTER, action="accept") == "master_accepted"
    done = await _act(client, event_id, MASTER, action="resolve", comment="Помог подняться")
    assert done == "resolved"
    detail = EventDetail.model_validate((await client.get(f"/api/events/{event_id}")).json())
    assert [a.action for a in detail.actions] == [
        "published",
        "confirmed",
        "sent_to_master",
        "master_accepted",
        "resolved",
    ]
    assert detail.actions[-1].comment == "Помог подняться"
    inbox = MasterInbox.model_validate((await client.get("/api/master/inbox")).json())
    assert inbox.active == [] and [e.id for e in inbox.recent_resolved] == [event_id]
