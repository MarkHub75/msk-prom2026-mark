"""Slice 24: payback and scale calculator (tech.md 8.25, 9)."""

import math
from typing import Any

import httpx
import pytest
from test_operator_views import event
from test_stats_ohs import cameras

from safewatch import clock, store
from safewatch.config import Settings
from safewatch.types import (
    BackendName,
    CalculatorDefaults,
    InferenceMetrics,
    RolloutResult,
    ScaleResult,
    TierResult,
    WhyItem,
)

MANAGEMENT, ADMIN = {"X-Role": "management"}, {"X-Role": "admin"}
CONFIG_CAPACITY = "замер LinQ 24.10 14:52: детектор 640, inflight 4, общая очередь площадки"


def artifact(
    throughput_fps: float, backend: BackendName = "linq", fake: int = 0, rtt: float = 50
) -> None:
    """An artifact row as the core writes it: `metrics_json` without `cached`."""
    n = store.one("SELECT count(*) FROM artifacts")[0]  # type: ignore[index]
    metrics = InferenceMetrics(
        backend=backend, fake=bool(fake), model_id="det", model_version="1", task="detect",
        input_size=640, step=1, frames_processed=100, wall_s=10, throughput_fps=throughput_fps,
        preprocess_ms=None, postprocess_ms=None, tpu_rtt_p50_ms=rtt, tpu_rtt_p90_ms=None,
        upload_s=None, total_s=10, cached=False,
    )  # fmt: skip
    store.insert("artifacts", {
        "cache_key": f"k{n}", "video_sha256": f"s{n}", "model_id": "det", "model_version": "1",
        "task": "detect", "input_size": 640, "step": 1, "backend": backend, "fake": fake,
        "path": f"artifacts/k{n}.jsonl", "frames": 100,
        "metrics_json": metrics.model_dump_json(exclude={"cached"}),
        "created_at": clock.iso(clock.now()),
    })  # fmt: skip


async def defaults(client: httpx.AsyncClient) -> CalculatorDefaults:
    r = await client.get("/api/calculator/defaults")
    assert r.status_code == 200, r.text
    return CalculatorDefaults.model_validate(r.json())


async def rollout(client: httpx.AsyncClient, **update: Any) -> RolloutResult:
    body = (await defaults(client)).rollout.model_dump() | update
    r = await client.post("/api/calculator/rollout", json=body, headers=MANAGEMENT)
    assert r.status_code == 200, r.text
    return RolloutResult.model_validate(r.json())


async def scale(client: httpx.AsyncClient, **body: Any) -> ScaleResult:
    r = await client.post("/api/calculator/scale", json=body, headers=ADMIN)
    assert r.status_code == 200, r.text
    return ScaleResult.model_validate(r.json())


# The 1.1.0 routes run on the v2 engine (docs/contracts/calculator_v2.md К12): 8 cameras of
# detector + pose at activity 0.5 need ceil(144.5 / 52.4) = 3 chips, CPU 144.5 × 0.077 = 11.1 of
# 16 cores and ceil(3 / 4) = 1 server; the electricity of 3 × 35 + 250 W is
# 0.355 kW × 8760 h × 8 ₽ = 24 878.4 ₽ a year.
ELECTRICITY = 0.355 * 8760 * 8


async def test_rollout_three_tiers_formulas(client: httpx.AsyncClient) -> None:
    found = await rollout(client)
    base, extended, top = found.tiers
    assert [t.tier for t in found.tiers] == ["base", "extended", "max"]
    assert [t.title for t in found.tiers] == ["Базовый", "Расширенный", "Максимальный"]
    assert found.incident_cost_rub == 500_000 + 200_000 + 300_000 + 500_000 == 1_500_000
    assert found.incidents_per_1000_workers == 4 / 200 * 1000 == 20
    assert all(t.accelerators == 3 for t in found.tiers)
    assert all(t.servers == 1 for t in found.tiers)
    assert base.capex_rub == 3 * 500_000 + 1 * 350_000 + 300_000 == 2_150_000
    assert extended.capex_rub == base.capex_rub + 8 * 1 * 25_000 == 2_350_000
    assert top.capex_rub == extended.capex_rub + 2 * 40_000 + math.ceil(8 * 0.2) * 30_000
    assert top.capex_rub == 2_490_000
    for t, reduction in zip(found.tiers, (0.2, 0.3, 0.4), strict=True):
        assert t.opex_rub_year == pytest.approx(t.capex_rub * 0.15 + ELECTRICITY)
        assert t.savings_rub_year == pytest.approx(4 * 1_500_000 * reduction)
    assert base.payback_months == pytest.approx(
        2_150_000 / (1_200_000 - (322_500 + ELECTRICITY)) * 12
    )
    assert base.items == [
        WhyItem(label="Ускорители LinQ", value="3 × 500 000 ₽"),
        WhyItem(label="Серверы под ускорители", value="1 × 350 000 ₽"),
        WhyItem(label="Пусконаладка и подключение камер", value="300 000 ₽"),
        WhyItem(label="Электроэнергия вычислительного оборудования в год", value="24 878 ₽"),
        WhyItem(label="Окупаемость", value="30,3 мес."),
    ]
    assert extended.items[3] == WhyItem(
        label="Световой и звуковой сигнал у зон", value="8 × 25 000 ₽"
    )
    assert top.items[4:6] == [
        WhyItem(label="Громкоговорители в цеха", value="2 × 40 000 ₽"),
        WhyItem(label="Новые IP-камеры с монтажом", value="2 × 30 000 ₽"),
    ]
    keys = {a.key for a in found.assumptions}
    assert {"v2.load.activity_share", "v2.load.effective_chip_fps"} <= keys


async def test_payback_none_when_not_profitable(client: httpx.AsyncClient) -> None:
    # Every tier costs 1 000 000 ₽, opex 100 000 ₽ + electricity; one incident of 1 000 000 ₽.
    free = {k: 0 for k in ("accelerator.price_rub", "server.price_rub", "light_sound_rub",
                           "speaker_rub", "new_camera_rub")}  # fmt: skip
    overrides = free | {
        "integration_rub": 1_000_000, "support_share_year": 0.1,
        "reduction.base": 0.1, "reduction.extended": 0.2, "reduction.max": 0.3,
    }  # fmt: skip
    plant: dict[str, Any] = {
        "incidents_per_year": 1, "downtime_cost_rub": 1_000_000, "fine_cost_rub": 0,
        "treatment_cost_rub": 0, "lawsuit_cost_rub": 0,
    }  # fmt: skip
    found = await rollout(client, **plant, overrides=overrides)
    base, extended, top = found.tiers

    def verdict(t: TierResult) -> str:
        return t.items[-1].value

    opex = 100_000 + ELECTRICITY
    assert (base.savings_rub_year, base.opex_rub_year) == (100_000, pytest.approx(opex))
    assert (base.payback_months, verdict(base)) == (None, "Не окупается при этих допущениях")
    assert extended.payback_months == pytest.approx(1_000_000 / (200_000 - opex) * 12)
    assert verdict(extended) == "159,7 мес."
    assert top.payback_months == pytest.approx(1_000_000 / (300_000 - opex) * 12)

    lower = await rollout(client, **plant, overrides=overrides | {"reduction.extended": 0.12})
    assert lower.tiers[1].payback_months is None  # 120 000 ₽ below opex


async def test_overrides_and_unknown_key(client: httpx.AsyncClient) -> None:
    plain = await rollout(client)
    free = await rollout(client, overrides={"accelerator.price_rub": 0})
    for before, after in zip(plain.tiers, free.tiers, strict=True):
        assert after.capex_rub == before.capex_rub - 3 * 500_000
    price = next(a for a in free.assumptions if a.key == "accelerator.price_rub")
    assert (price.value, price.source) == (0, "задано в расчёте")
    # An explicit capacity_fps is the effective chip capacity of this legacy calculation.
    queue = await rollout(client, overrides={"accelerator.capacity_fps": 12.4})
    assert queue.tiers[0].accelerators == math.ceil(144.5 / 12.4) == 12
    assert queue.tiers[0].servers == math.ceil(12 / 4) == 3

    body = (await defaults(client)).rollout.model_dump()
    url = "/api/calculator/rollout"
    for change, field in [
        ({"overrides": {"no.such.key": 1}}, "overrides.no.such.key"),
        ({"overrides": {"server.price_rub": -1}}, "overrides.server.price_rub"),
        ({"overrides": {"accelerator.capacity_fps": 0}}, "overrides.accelerator.capacity_fps"),
        ({"cameras": 0}, "cameras"),
        ({"workshops": 0}, "workshops"),
        ({"workers": -1}, "workers"),
        ({"fine_cost_rub": -0.5}, "fine_cost_rub"),
    ]:
        r = await client.post(url, json=body | change, headers=MANAGEMENT)
        assert r.status_code == 422, change
        assert (r.json()["message"], r.json()["details"]) == (
            f"Неверное значение: {field}", {"field": field},
        )  # fmt: skip
    r = await client.post(url, json=body | {"cameras": "x"}, headers=MANAGEMENT)
    assert (r.status_code, r.json()["details"]) == (422, {"field": "body.cameras"})
    r = await client.post("/api/calculator/scale", json={"cameras_now": 8, "new_cameras": -1},
                          headers=ADMIN)  # fmt: skip
    assert (r.status_code, r.json()["details"]) == (422, {"field": "new_cameras"})
    r = await client.post("/api/calculator/scale", headers=ADMIN, json={
        "cameras_now": 8, "new_cameras": 1, "overrides": {"nope": 1},
    })  # fmt: skip
    assert r.status_code == 422


async def test_scale_accelerators_from_measured(client: httpx.AsyncClient) -> None:
    found = await scale(client, cameras_now=8, new_cameras=8)
    assert (found.capacity_fps, found.capacity_source) == (
        52.4, "Эффективная ёмкость чипа LinQ: заявление вендора × запас",
    )  # fmt: skip
    assert (found.cameras_total, found.analysis_fps) == (16, 12)
    # 16 cameras: A95 = 11, peak 4 + 11 × 23.75 = 265.25 → 6 chips, CPU 20.4 → 2 servers.
    assert (found.accelerators_now, found.accelerators_total, found.servers_total) == (3, 6, 2)
    assert found.capex_rub == (6 - 3) * 500_000 + (2 - 1) * 350_000 + 8 * 30_000
    assert found.items == [
        WhyItem(label="Ускорители LinQ", value="3 × 500 000 ₽"),
        WhyItem(label="Серверы под ускорители", value="1 × 350 000 ₽"),
        WhyItem(label="Новые IP-камеры с монтажом", value="8 × 30 000 ₽"),
    ]

    artifact(10)
    artifact(14)
    artifact(100, fake=1)
    # The shared LinQ queue is a reference for the naive step, not the chip capacity (К12).
    again = await scale(client, cameras_now=8, new_cameras=8)
    assert (again.accelerators_total, again.capex_rub) == (6, found.capex_rub)
    # 4 cameras: A95 = 4, peak 1 + 4 × 23.75 = 96 → 2 chips, 1 server.
    fresh = await scale(client, cameras_now=0, new_cameras=4)
    assert (fresh.accelerators_now, fresh.accelerators_total, fresh.servers_total) == (0, 2, 1)


async def test_roles(client: httpx.AsyncClient) -> None:
    body = (await defaults(client)).rollout.model_dump()
    small = {"cameras_now": 4, "new_cameras": 2}
    for url, data, role, status in [
        ("/api/calculator/rollout", body, "admin", 403),
        ("/api/calculator/rollout", body, "ohs", 403),
        ("/api/calculator/rollout", body, None, 400),
        ("/api/calculator/rollout", body, "management", 200),
        ("/api/calculator/scale", small, "ohs", 403),
        ("/api/calculator/scale", small, None, 400),
        ("/api/calculator/scale", small, "admin", 200),
        ("/api/calculator/scale", small, "management", 200),
    ]:
        headers = {"X-Role": role} if role else {}
        r = await client.post(url, json=data, headers=headers)
        assert r.status_code == status, (url, role)
    r = await client.post("/api/calculator/rollout", json=body | {"cameras": 0}, headers=ADMIN)
    assert r.status_code == 403  # the role is checked before the numbers


async def test_defaults_list_sources(
    client: httpx.AsyncClient, settings: Settings, fake_clock: Any
) -> None:
    empty = await defaults(client)
    keys = [a.key for a in settings.calculator.assumptions]
    assert [a.key for a in empty.assumptions] == keys and len(keys) == 15
    assert all(a.source.strip() and a.editable for a in empty.assumptions)
    assert (empty.rollout.cameras, empty.rollout.workshops, empty.rollout.workers) == (8, 2, 200)
    assert (empty.scale.cameras_now, empty.scale.new_cameras) == (8, 8)
    assert empty.measured == []
    assert (await rollout(client)).events_per_operator_shift is None

    artifact(10, rtt=40)
    artifact(14, rtt=60)
    c = cameras()
    for _ in range(3):
        event(c["north"])
    event(c["south"])
    event(c["south"], status="superseded")
    event(c["north"], is_demo=1)
    event(c["north"], started_at="2026-09-01T08:00:00.000Z")  # older than stats.default_days
    found = await defaults(client)
    measured = {m.key: m for m in found.measured}
    assert all(m.source.strip() and not m.editable for m in found.measured)
    assert measured["measured.capacity_fps"].value == 12
    assert measured["measured.tpu_rtt_p50_ms"].value == 50
    per_day = measured["measured.events_per_camera_day"]
    assert per_day.value == pytest.approx(4 / 2 / 30)
    assert per_day.source == "журнал: события эфира за 30 дн. на камеру с событиями"
    shift = (await rollout(client)).events_per_operator_shift
    assert shift == pytest.approx(4 / 2 / 30 * 8 / (2 * 2))
    assert (await rollout(client, shifts_per_day=0)).events_per_operator_shift is None
