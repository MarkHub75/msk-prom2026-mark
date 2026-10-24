"""Slice 1: sectors and cameras through the HTTP API (tech.md 16, slice 1)."""

from typing import Any

import httpx
import pytest

from safewatch import services, store
from safewatch.config import Settings
from safewatch.types import ApiError, Camera, CamerasAdminView, Meta, Sector

ADMIN = {"X-Role": "admin"}
AT = "2026-10-24T09:00:00.000Z"


async def _sector(client: httpx.AsyncClient, name: str, sort_order: int = 0) -> Sector:
    body = {"name": name, "sort_order": sort_order}
    response = await client.post("/api/sectors", json=body, headers=ADMIN)
    assert response.status_code == 201, response.text
    return Sector.model_validate(response.json())


async def _camera(client: httpx.AsyncClient, sector_id: int, name: str = "Камера") -> Camera:
    body = {"sector_id": sector_id, "name": name}
    response = await client.post("/api/cameras", json=body, headers=ADMIN)
    assert response.status_code == 201, response.text
    return Camera.model_validate(response.json())


def _error(response: httpx.Response, status: int, code: str) -> ApiError:
    assert response.status_code == status, response.text
    body = ApiError.model_validate(response.json())
    assert body.code == code
    return body


async def test_meta_lists_roles_statuses_zone_kinds(
    client: httpx.AsyncClient, core: Settings
) -> None:
    meta = Meta.model_validate((await client.get("/api/meta")).json())
    assert (meta.product_name, meta.contract) == ("SafeWatch", "1.0.0")
    assert (meta.inference_backend, meta.fake, meta.timezone) == ("linq", False, core.timezone)
    roles = {r.id: r for r in meta.roles}
    assert list(roles) == ["operator", "master", "ohs", "management", "admin"]
    assert roles["operator"].actions == ["view", "confirm", "false_alarm", "send_to_master"]
    assert roles["master"].actions == ["accept", "resolve"]
    assert [roles[r].actions for r in ("ohs", "management", "admin")] == [[], [], []]
    assert roles["master"].title == "Мастер смены"
    assert [lv.id for lv in meta.levels] == ["yellow", "red"]
    assert len(meta.statuses) == 9
    terminal = {s.id for s in meta.statuses if s.terminal}
    assert terminal == {"false_alarm", "resolved", "auto_finished", "superseded"}
    assert next(s.title for s in meta.statuses if s.id == "new") == "Новое"
    assert len(meta.zone_kinds) == 8
    assert meta.zone_kinds[0].id == "danger"
    assert [s.id for s in meta.scenarios] == [
        "running", "proximity", "phone", "fall", "fence_crossing", "restricted_under",
        "fire_smoking", "no_harness", "suspended_load", "load_carrying",
    ]  # fmt: skip


async def test_meta_follows_settings(
    client: httpx.AsyncClient, core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    from safewatch import config

    other = core.model_copy(
        update={"product_name": "Другой", "fake": True, "inference_backend": "local"}
    )
    monkeypatch.setattr(config, "get_settings", lambda: other)
    meta = Meta.model_validate((await client.get("/api/meta")).json())
    assert (meta.product_name, meta.fake, meta.inference_backend) == ("Другой", True, "local")


async def test_sector_crud_and_unique_name(client: httpx.AsyncClient) -> None:
    b = await _sector(client, "  Б-сектор  ", sort_order=1)
    assert b.name == "Б-сектор"
    a = await _sector(client, "А" * 80, sort_order=1)
    first = await _sector(client, "Я-сектор", sort_order=0)
    for name in ("", "   ", "А" * 81):
        response = await client.post("/api/sectors", json={"name": name}, headers=ADMIN)
        assert _error(response, 422, "validation").message == "Название: от 1 до 80 символов"
    taken = await client.post("/api/sectors", json={"name": " Б-сектор"}, headers=ADMIN)
    assert _error(taken, 409, "name_taken").message == "Сектор с таким названием уже есть"

    renamed = await client.put(
        f"/api/sectors/{b.id}", json={"name": "Б2", "sort_order": 1}, headers=ADMIN
    )
    assert renamed.status_code == 200
    assert Sector.model_validate(renamed.json()).name == "Б2"
    same = await client.put(
        f"/api/sectors/{b.id}", json={"name": "Б2", "sort_order": 1}, headers=ADMIN
    )
    assert same.status_code == 200  # its own name is not taken
    clash = await client.put(f"/api/sectors/{b.id}", json={"name": first.name}, headers=ADMIN)
    _error(clash, 409, "name_taken")

    listed = [Sector.model_validate(s) for s in (await client.get("/api/sectors")).json()]
    assert [s.id for s in listed] == [first.id, a.id, b.id]  # sort_order, then name


async def test_sector_delete_with_cameras_conflicts(client: httpx.AsyncClient) -> None:
    full = await _sector(client, "Полный")
    camera = await _camera(client, full.id)
    busy = await client.delete(f"/api/sectors/{full.id}", headers=ADMIN)
    _error(busy, 409, "sector_not_empty")
    empty = await _sector(client, "Пустой")
    assert (await client.delete(f"/api/sectors/{empty.id}", headers=ADMIN)).status_code == 204
    assert [s.id for s in services.sectors_list()] == [full.id]
    # A deleted camera keeps history in the sector: still a conflict, not a 500.
    assert (await client.delete(f"/api/cameras/{camera.id}", headers=ADMIN)).status_code == 204
    history = await client.delete(f"/api/sectors/{full.id}", headers=ADMIN)
    _error(history, 409, "sector_not_empty")


async def test_camera_rejects_bad_input(client: httpx.AsyncClient) -> None:
    sector = await _sector(client, "Цех")
    cases: list[tuple[dict[str, Any], str]] = [
        ({"sector_id": sector.id, "name": " "}, "Название: от 1 до 80 символов"),
        ({"sector_id": sector.id, "name": "К" * 81}, "Название: от 1 до 80 символов"),
        ({"sector_id": sector.id, "name": "К", "description": "о" * 301}, "Описание: до 300 символов"),  # noqa: E501
        ({"sector_id": 999, "name": "К"}, "Сектор не найден"),
    ]  # fmt: skip
    for body, message in cases:
        response = await client.post("/api/cameras", json=body, headers=ADMIN)
        assert _error(response, 422, "validation").message == message
    body = {"sector_id": sector.id, "name": " " + "К" * 80, "description": "о" * 300}
    created = await client.post("/api/cameras", json=body, headers=ADMIN)
    assert created.status_code == 201
    camera = Camera.model_validate(created.json())
    assert camera.name == "К" * 80
    assert (camera.has_calibration, camera.zones_count, camera.videos_count) == (False, 0, 0)


def _playing_broadcast(camera_id: int) -> int:
    with store.tx():
        video = store.insert("videos", {
            "camera_id": camera_id, "filename": "a.mp4", "sha256": "h", "path": "uploads/h.mp4",
            "size_bytes": 1, "width": 2, "height": 2, "fps": 25, "frame_count": 1,
            "duration_ms": 40, "codec": "avc1", "browser_playable": 1, "status": "ready",
            "created_at": AT,
        })  # fmt: skip
        artifact = store.insert("artifacts", {
            "cache_key": "k", "video_sha256": "h", "model_id": "m", "model_version": "v",
            "task": "detect", "input_size": 640, "step": 2, "backend": "linq", "fake": 1,
            "path": "p", "frames": 1, "metrics_json": "{}", "created_at": AT,
        })  # fmt: skip
        analysis = store.insert("analyses", {
            "video_id": video, "version": 1, "det_artifact_id": artifact, "config_json": "{}",
            "hud_path": "h", "gaps_json": "[]", "duration_ms": 40, "created_at": AT,
        })  # fmt: skip
        return store.insert("broadcasts", {
            "camera_id": camera_id, "video_id": video, "analysis_id": analysis,
            "started_at": AT, "loop": 1, "status": "playing",
        })  # fmt: skip


async def test_camera_crud_soft_delete(client: httpx.AsyncClient) -> None:
    first, second = await _sector(client, "Первый"), await _sector(client, "Второй")
    camera = await _camera(client, first.id, "Пресс")
    keep = await _camera(client, first.id, "Склад")
    patch = {"sector_id": second.id}
    moved = await client.patch(f"/api/cameras/{camera.id}", json=patch, headers=ADMIN)
    assert moved.status_code == 200
    assert Camera.model_validate(moved.json()).model_dump() == {
        **camera.model_dump(),
        "sector_id": second.id,
    }
    renamed = await client.patch(
        f"/api/cameras/{camera.id}", json={"name": "Пресс 2"}, headers=ADMIN
    )
    assert (renamed.json()["name"], renamed.json()["sector_id"]) == ("Пресс 2", second.id)
    bad = await client.patch(f"/api/cameras/{camera.id}", json={"sector_id": 999}, headers=ADMIN)
    assert _error(bad, 422, "validation").message == "Сектор не найден"
    by_sector = (await client.get("/api/cameras", params={"sector_id": second.id})).json()
    assert [c["id"] for c in by_sector] == [camera.id]

    broadcast = _playing_broadcast(camera.id)
    assert (await client.get(f"/api/cameras/{camera.id}")).json()["videos_count"] == 1
    assert (await client.delete(f"/api/cameras/{camera.id}", headers=ADMIN)).status_code == 204
    _error(await client.get(f"/api/cameras/{camera.id}"), 404, "not_found")
    assert [c["id"] for c in (await client.get("/api/cameras")).json()] == [keep.id]
    view = CamerasAdminView.model_validate((await client.get("/api/admin/cameras")).json())
    assert [c.id for c in view.cameras] == [keep.id]
    row = store.one("SELECT deleted_at FROM cameras WHERE id = ?", camera.id)
    assert row is not None and row["deleted_at"] is not None
    stopped = store.one("SELECT status, stopped_at FROM broadcasts WHERE id = ?", broadcast)
    assert stopped is not None and stopped["status"] == "stopped" and stopped["stopped_at"]


async def test_writes_require_admin_role(client: httpx.AsyncClient) -> None:
    sector = await _sector(client, "Цех")
    camera = await _camera(client, sector.id)
    writes = [
        ("post", "/api/sectors", {"name": "Х"}),
        ("put", f"/api/sectors/{sector.id}", {"name": "Х"}),
        ("delete", f"/api/sectors/{sector.id}", None),
        ("post", "/api/cameras", {"sector_id": sector.id, "name": "Х"}),
        ("patch", f"/api/cameras/{camera.id}", {"name": "Х"}),
        ("delete", f"/api/cameras/{camera.id}", None),
    ]
    for method, path, body in writes:
        anonymous = await client.request(method, path, json=body)
        assert _error(anonymous, 400, "role_required").message == "Выберите роль"
        operator = await client.request(method, path, json=body, headers={"X-Role": "operator"})
        _error(operator, 403, "forbidden_role")
    assert [s.name for s in services.sectors_list()] == ["Цех"]
    assert services.camera_get(camera.id).name == "Камера"


async def test_unknown_ids_are_404(client: httpx.AsyncClient) -> None:
    requests = [
        ("get", "/api/cameras/999", None),
        ("get", "/api/cameras?sector_id=999", None),
        ("patch", "/api/cameras/999", {"name": "Х"}),
        ("delete", "/api/cameras/999", None),
        ("put", "/api/sectors/999", {"name": "Х"}),
        ("delete", "/api/sectors/999", None),
    ]
    for method, path, body in requests:
        response = await client.request(method, path, json=body, headers=ADMIN)
        assert _error(response, 404, "not_found").message in (
            "Камера не найдена",
            "Сектор не найден",
        )


async def test_cameras_admin_view_shape(client: httpx.AsyncClient) -> None:
    empty = CamerasAdminView.model_validate((await client.get("/api/admin/cameras")).json())
    assert (empty.sectors, empty.cameras) == ([], [])
    sector = await _sector(client, "Цех")
    camera = await _camera(client, sector.id)
    with store.tx():
        store.insert("zones", {
            "camera_id": camera.id, "kind": "danger", "name": "Пресс",
            "points_json": "[[0,0],[1,0],[0,1]]", "created_at": AT,
        })  # fmt: skip
    view = CamerasAdminView.model_validate((await client.get("/api/admin/cameras")).json())
    assert [s.id for s in view.sectors] == [sector.id]
    assert [(c.id, c.sector_id, c.zones_count) for c in view.cameras] == [(camera.id, sector.id, 1)]
