"""Slice 9: camera rules of tech.md 8.3 and the /ohs/rules screen."""

from pathlib import Path

import httpx
import pytest
from test_analysis_api import _analysis, _demo_job
from test_calibration import camera

from safewatch import services
from safewatch.config import Settings
from safewatch.types import ApiError, CameraIn, CameraRule, CameraRuleIn, RulesScreenView

ADMIN, OHS, OPERATOR = {"X-Role": "admin"}, {"X-Role": "ohs"}, {"X-Role": "operator"}


async def test_rule_params_override_and_ranges(
    client: httpx.AsyncClient,
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    linq_tails: Path,
) -> None:
    camera_id = camera()
    url = f"/api/cameras/{camera_id}/rules"
    rules = [CameraRule.model_validate(r) for r in (await client.get(url)).json()]
    by_id = {r.scenario: (r.enabled, r.params, r.status) for r in rules}
    # No rows in the database: the defaults of the config, on while the plugin is active.
    assert by_id["running"] == by_id["fall"] == (True, {}, "active")
    assert by_id["fire_smoking"] == (False, {}, "model_missing")
    assert by_id["load_carrying"] == (False, {}, "skeleton")
    assert rules[0].effective == core.scenarios.running
    assert (await client.get("/api/cameras/999/rules")).status_code == 404

    body = {"enabled": True, "params": {"hold_s": 60.0}}
    r = await client.put(f"{url}/running", json=body, headers=OHS)
    rule = CameraRule.model_validate(r.json())
    assert (r.status_code, rule.params) == (200, {"hold_s": 60.0})
    assert rule.effective == core.scenarios.running | {"hold_s": 60.0}

    async def refused(params: dict[str, float]) -> tuple[int, str]:
        r = await client.put(
            f"{url}/running", json={"enabled": True, "params": params}, headers=OHS
        )
        return r.status_code, ApiError.model_validate(r.json()).message

    assert await refused({"hold_s": 60.01}) == (422, "Параметр hold_s: от 0 до 60")
    assert await refused({"speed_bh_s": 0.49}) == (422, "Параметр speed_bh_s: от 0,5 до 5")
    assert await refused({"jump_m": 1.0}) == (422, "Неизвестный параметр jump_m")
    unknown = await client.put(f"{url}/dancing", json=body, headers=OHS)
    assert (unknown.status_code, unknown.json()["message"]) == (404, "Сценарий не найден")
    assert (await client.put(f"{url}/running", json=body)).status_code == 400
    assert (await client.put(f"{url}/running", json=body, headers=OPERATOR)).status_code == 403

    # A disabled scenario gives no episodes once the video is recomputed.
    plain = {"enabled": True, "params": {}}
    assert (await client.put(f"{url}/running", json=plain, headers=ADMIN)).status_code == 200
    job = await _demo_job(monkeypatch, tmp_path, camera_id)
    before = await _analysis(client, job.video_id)
    assert [e.scenario for e in before.episodes] == ["running", "fall"]
    off = {"enabled": False, "params": {}}
    assert (await client.put(f"{url}/running", json=off, headers=ADMIN)).status_code == 200
    services.video_recompute(job.video_id, "ohs")
    await services.run_next_job()
    after = await _analysis(client, job.video_id)
    assert (after.version, [e.scenario for e in after.episodes]) == (2, ["fall"])


async def test_rules_screen_view(client: httpx.AsyncClient) -> None:
    first, second = (
        camera(),
        services.camera_create(
            CameraIn(sector_id=services.sectors_list()[0].id, name="Камера 2"), "admin"
        ).id,
    )
    services.camera_rule_set(second, "fall", CameraRuleIn(enabled=False), "ohs")
    view = RulesScreenView.model_validate((await client.get("/api/ohs/rules")).json())
    assert [s.id for s in view.scenarios] == [
        "running", "proximity", "phone", "fall", "fence_crossing", "restricted_under",
        "fire_smoking", "no_harness", "suspended_load", "load_carrying", "no_helmet",
        "no_respirator",
    ]  # fmt: skip
    assert [row.camera.id for row in view.rows] == [first, second]
    cells = {
        (row.camera.id, r.scenario): r.enabled
        for row in view.rows
        for r in row.rules
        if r.scenario in ("running", "fall")
    }
    assert cells == {
        (first, "running"): True,
        (first, "fall"): True,
        (second, "running"): True,
        (second, "fall"): False,
    }
