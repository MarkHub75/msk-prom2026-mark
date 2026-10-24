"""Slice 7: the event card with why, history and provenance (tech.md 5.2 EventDetail)."""

from pathlib import Path

import httpx
import pytest
from conftest import FakeClock
from test_analysis_api import _camera, _demo_job
from test_broadcast import at, started

from safewatch import registry, rules, services, store, texts
from safewatch.config import Settings
from safewatch.rules.running import RunningPlugin
from safewatch.types import EpisodeDraft, EventDetail


async def _detail(client: httpx.AsyncClient, event_id: int, role: str | None) -> EventDetail:
    headers = {} if role is None else {"X-Role": role}
    r = await client.get(f"/api/events/{event_id}", headers=headers)
    assert r.status_code == 200, r.text
    return EventDetail.model_validate(r.json())


async def test_detail_why_history_provenance(
    client: httpx.AsyncClient,
    fake_core: Settings,
    fake_clock: FakeClock,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    job = await _demo_job(monkeypatch, tmp_path, _camera())
    assert job.analysis_id is not None
    running, _ = (services.video_analysis(job.video_id)).episodes
    broadcast = store.camera_broadcast(services.video_get(job.video_id).camera_id)
    assert broadcast is not None  # autostart
    at(fake_clock, started(broadcast["id"]), running.confirm_ms)
    services.broadcast_tick()
    (event,) = store.all("SELECT id FROM events")
    fake_clock.advance(1)
    r = await client.post(
        f"/api/events/{event['id']}/actions",
        json={"action": "view"},
        headers={"X-Role": "operator"},
    )
    assert r.status_code == 200

    detail = await _detail(client, event["id"], "operator")
    assert detail.episode == running
    (shot,) = running.evidence
    draft = EpisodeDraft.model_validate(
        running.model_dump() | {"confirm_frame_idx": shot.frame_idx, "escalate_frame_idx": None}
    )
    params = rules.defaults("running")
    assert detail.why == RunningPlugin().explain(draft, params)
    assert detail.why[0].label == texts.WHY_RULE
    assert [(a.action, a.actor_role) for a in detail.actions] == [
        ("published", "system"),
        ("viewed", "operator"),
    ]
    assert detail.actions[0].at < detail.actions[1].at
    assert detail.allowed_actions == ["confirm", "false_alarm", "send_to_master"]
    assert (await _detail(client, event["id"], "master")).allowed_actions == []
    assert (await _detail(client, event["id"], None)).allowed_actions == []
    det, pose = (
        registry.resolve(fake_core.pipeline.detector),
        registry.resolve(fake_core.pipeline.pose or ""),
    )
    p = detail.provenance
    assert (p.backend, p.fake, p.job_id, p.analysis_version) == ("linq", True, job.id, 1)
    assert (p.det_model, p.pose_model) == (f"{det.id}@{det.version}", f"{pose.id}@{pose.version}")
    assert p.video_sha256 == services.video_get(job.video_id).sha256
    assert (p.rule_params, p.evidence_sha256) == (params, shot.sha256)
    assert (detail.video_id, detail.video_start_ms, detail.video_end_ms) == (
        job.video_id,
        running.start_ms,
        running.end_ms,
    )
    assert detail.broadcast is not None and detail.broadcast.id == broadcast["id"]
    assert detail.deliveries == []
    assert (await client.get("/api/events/999")).status_code == 404


async def test_demo_event_detail(client: httpx.AsyncClient) -> None:
    services.seed_demo()
    found = store.one("SELECT id, reason_text, status FROM events ORDER BY id")
    assert found is not None
    detail = await _detail(client, found["id"], "operator")
    assert detail.episode is None and detail.event.mode == "demo"
    assert [(w.label, w.value) for w in detail.why] == [(texts.WHY_REASON, found["reason_text"])]
    p = detail.provenance
    assert (p.backend, p.fake, p.det_model, p.pose_model, p.job_id) == (
        None,
        False,
        None,
        None,
        None,
    )
    assert (p.video_sha256, p.analysis_version, p.rule_params, p.evidence_sha256) == (
        None,
        None,
        {},
        None,
    )
    assert detail.actions[0].action == "published"
    assert detail.event.status == found["status"]
