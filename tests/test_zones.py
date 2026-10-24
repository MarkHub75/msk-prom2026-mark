"""Slice 9: zones of tech.md 8.11 and their geometry rules (tech.md 9)."""

import math
from typing import Any

import httpx
from test_calibration import camera

from safewatch import store
from safewatch.types import ApiError, Zone

ADMIN, OHS, OPERATOR = {"X-Role": "admin"}, {"X-Role": "ohs"}, {"X-Role": "operator"}


def _ring(n: int) -> list[tuple[float, float]]:
    return [
        (0.5 + 0.4 * math.cos(2 * math.pi * k / n), 0.5 + 0.4 * math.sin(2 * math.pi * k / n))
        for k in range(n)
    ]


async def test_zone_crud_and_geometry_rules(client: httpx.AsyncClient) -> None:
    camera_id = camera()
    url = f"/api/cameras/{camera_id}/zones"

    async def create(kind: str, points: list[Any], name: str = "Пресс") -> tuple[int, str]:
        body = {"kind": kind, "name": name, "points": points}
        r = await client.post(url, json=body, headers=OHS)
        return r.status_code, ApiError.model_validate(r.json()).message if r.is_error else ""

    assert (await create("danger", _ring(3)))[0] == 201
    assert (await create("danger", _ring(32)))[0] == 201
    for n in (2, 33):
        assert await create("danger", _ring(n)) == (422, "Полигон: от 3 до 32 точек")
    assert (await create("fence", [(0.1, 0.5), (0.9, 0.5)]))[0] == 201
    assert await create("fence", _ring(3)) == (422, "Линия — ровно 2 точки")
    assert await create("fence", [(0.1, 0.5), (0.1, 0.5)]) == (422, "Линия — ровно 2 точки")
    assert await create("lava", _ring(3)) == (422, "Неизвестный тип зоны")
    assert (await create("danger", _ring(4), name="я" * 60))[0] == 201
    assert (await create("danger", _ring(4), name="я" * 61))[0] == 422
    assert (await create("danger", _ring(4), name="   "))[0] == 422
    flat = [(0.1, 0.1), (0.5, 0.5), (0.9, 0.9)]
    assert (await create("danger", flat))[0] == 422  # degenerate: no area
    assert await create("danger", [(0.1, 0.1), (1.01, 0.1), (0.5, 0.9)]) == (
        422,
        "Точки вне кадра",
    )

    body = {"kind": "danger", "name": "Пресс", "points": _ring(4)}
    assert (await client.post(url, json=body)).status_code == 400
    assert (await client.post(url, json=body, headers=OPERATOR)).status_code == 403
    assert (await client.post("/api/cameras/999/zones", json=body, headers=OHS)).status_code == 404

    zones = [Zone.model_validate(z) for z in (await client.get(url)).json()]
    assert [z.kind for z in zones] == ["danger", "danger", "fence", "danger"]
    first = zones[0]
    r = await client.patch(f"/api/zones/{first.id}", json={"name": " Станок "}, headers=ADMIN)
    assert (r.status_code, Zone.model_validate(r.json()).name) == (200, "Станок")
    patch = {"points": [(0.1, 0.1), (0.9, 0.1)]}  # a polygon stays a polygon
    assert (
        await client.patch(f"/api/zones/{first.id}", json=patch, headers=OHS)
    ).status_code == 422
    assert (await client.patch(f"/api/zones/{first.id}", json={"name": "x"})).status_code == 400

    assert (await client.delete(f"/api/zones/{first.id}", headers=OPERATOR)).status_code == 403
    assert (await client.delete(f"/api/zones/{first.id}", headers=OHS)).status_code == 204
    assert (await client.delete(f"/api/zones/{first.id}", headers=OHS)).status_code == 404
    left = [Zone.model_validate(z).id for z in (await client.get(url)).json()]
    assert first.id not in left and len(left) == 3
    row = store.one("SELECT deleted_at FROM zones WHERE id = ?", first.id)
    assert row is not None and row["deleted_at"] is not None  # soft delete: the row stays
    camera_row = (await client.get(f"/api/cameras/{camera_id}")).json()
    assert camera_row["zones_count"] == 3
