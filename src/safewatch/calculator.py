"""Payback and scale calculator (tech.md 8.25): pure functions over `CalcAssumption` values."""

import math

from safewatch import texts
from safewatch.types import (
    CalcAssumption,
    CalcTier,
    RolloutIn,
    RolloutResult,
    ScaleIn,
    ScaleResult,
    TierResult,
    WhyItem,
)


def _ceil(x: float) -> int:
    """Ceil without float noise: 3 × 0.1 × 10 is 3.0000000000000004 and must stay 3."""
    return math.ceil(round(x, 9))


def _accelerators(cameras: int, fps: float, a: dict[str, float], capacity_fps: float) -> int:
    return _ceil(cameras * fps * a["models_per_frame"] / capacity_fps)


def _servers(accelerators: int, a: dict[str, float]) -> int:
    return _ceil(accelerators / a["accelerators_per_server"])


def _qty(x: float) -> str:
    return str(int(x)) if x == int(x) else texts.fmt_num(x)


def _line(label: str, n: float, price: float) -> WhyItem:
    """«Ускорители LinQ: 3 × 500 000 ₽»."""
    return WhyItem(label=label, value=f"{_qty(n)} × {texts.fmt_rub(price)}")


def rollout(
    data: RolloutIn,
    assumptions: dict[str, CalcAssumption],
    analysis_fps: float,
    events_per_camera_day: float | None,
) -> RolloutResult:
    a = {key: item.value for key, item in assumptions.items()}
    incident_cost = (
        data.downtime_cost_rub
        + data.fine_cost_rub
        + data.treatment_cost_rub
        + data.lawsuit_cost_rub
    )
    accelerators = _accelerators(data.cameras, analysis_fps, a, a["accelerator.capacity_fps"])
    servers = _servers(accelerators, a)
    zones = data.cameras * a["zones_per_camera"]
    new_cameras = _ceil(data.cameras * a["new_cameras_share"])

    base = (
        accelerators * a["accelerator.price_rub"]
        + servers * a["server.price_rub"]
        + a["integration_rub"]
    )
    extended = base + zones * a["light_sound_rub"]
    top = extended + data.workshops * a["speaker_rub"] + new_cameras * a["new_camera_rub"]
    base_items = [
        _line(texts.CALC_ACCELERATORS, accelerators, a["accelerator.price_rub"]),
        _line(texts.CALC_SERVERS, servers, a["server.price_rub"]),
        WhyItem(label=texts.CALC_INTEGRATION, value=texts.fmt_rub(a["integration_rub"])),
    ]
    extended_items = [*base_items, _line(texts.CALC_LIGHT_SOUND, zones, a["light_sound_rub"])]
    top_items = [
        *extended_items,
        _line(texts.CALC_SPEAKERS, data.workshops, a["speaker_rub"]),
        _line(texts.CALC_NEW_CAMERAS, new_cameras, a["new_camera_rub"]),
    ]

    def tier(name: CalcTier, capex: float, items: list[WhyItem]) -> TierResult:
        opex = capex * a["support_share_year"]
        savings = data.incidents_per_year * incident_cost * a[f"reduction.{name}"]
        payback = capex / (savings - opex) * 12 if savings > opex else None
        verdict = (
            texts.CALC_NOT_PROFITABLE
            if payback is None
            else texts.CALC_PAYBACK_MONTHS.format(n=texts.fmt_num(payback))
        )
        return TierResult(
            tier=name,
            title=texts.CALC_TIER_TITLES[name],
            accelerators=accelerators,
            servers=servers,
            capex_rub=capex,
            opex_rub_year=opex,
            savings_rub_year=savings,
            payback_months=payback,
            items=[*items, WhyItem(label=texts.CALC_PAYBACK, value=verdict)],
        )

    shifts = data.operators * data.shifts_per_day
    return RolloutResult(
        incident_cost_rub=incident_cost,
        incidents_per_1000_workers=(
            data.incidents_per_year / data.workers * 1000 if data.workers else None
        ),
        events_per_operator_shift=(
            events_per_camera_day * data.cameras / shifts
            if events_per_camera_day is not None and shifts
            else None
        ),
        tiers=[
            tier("base", base, base_items),
            tier("extended", extended, extended_items),
            tier("max", top, top_items),
        ],
        assumptions=list(assumptions.values()),
    )


def scale(
    data: ScaleIn,
    assumptions: dict[str, CalcAssumption],
    analysis_fps: float,
    capacity_fps: float,
    capacity_source: str,
) -> ScaleResult:
    a = {key: item.value for key, item in assumptions.items()}
    total = data.cameras_now + data.new_cameras
    now = _accelerators(data.cameras_now, analysis_fps, a, capacity_fps)
    accelerators = _accelerators(total, analysis_fps, a, capacity_fps)
    servers = _servers(accelerators, a)
    added_servers = servers - _servers(now, a)
    capex = (
        (accelerators - now) * a["accelerator.price_rub"]
        + added_servers * a["server.price_rub"]
        + data.new_cameras * a["new_camera_rub"]
    )
    return ScaleResult(
        cameras_total=total,
        analysis_fps=analysis_fps,
        capacity_fps=capacity_fps,
        capacity_source=capacity_source,
        accelerators_now=now,
        accelerators_total=accelerators,
        servers_total=servers,
        capex_rub=capex,
        items=[
            _line(texts.CALC_ACCELERATORS, accelerators - now, a["accelerator.price_rub"]),
            _line(texts.CALC_SERVERS, added_servers, a["server.price_rub"]),
            _line(texts.CALC_NEW_CAMERAS, data.new_cameras, a["new_camera_rub"]),
        ],
        assumptions=list(assumptions.values()),
    )
