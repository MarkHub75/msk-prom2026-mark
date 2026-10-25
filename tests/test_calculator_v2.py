"""Calculator v2 (docs/contracts/calculator_v2.md): golden vectors К13, boundaries, API К10.

Expected numbers are the contract's independent vectors or hand arithmetic written out here,
never a copy of the implementation.
"""

import copy
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import httpx
import pytest
from test_stats_ohs import cameras

from safewatch import calculator as calc
from safewatch import clock, services, store
from safewatch.calculator import EMPTY_KIT, Board, Group, ServerSpec
from safewatch.config import Settings
from safewatch.types import CameraRuleIn, LoadInput, ResultV2

FIX = Path(__file__).parent / "fixtures" / "calculator_v2"
MANAGEMENT, ADMIN = {"X-Role": "management"}, {"X-Role": "admin"}
DET, POSE = "det-yolov8n@640-ap9999", "pose-yolov8n@640-ap9999"
ROLLOUT = "/api/calculator/rollout?format=v2"
SCALE = "/api/calculator/scale?format=v2"


def fixture(name: str) -> Any:
    return json.loads((FIX / f"{name}.json").read_text(encoding="utf-8"))


def load_in(**update: Any) -> LoadInput:
    return LoadInput.model_validate(fixture("rollout_request")["load"] | update)


SPLIT = {"cpu_basis": "split", "decode_cores_per_camera": 0.1}  # К13 CPU columns
HP = Board("HP", 1, 1, Fraction(35), Fraction(500_000))
BOARDS = {"HP": HP}
SERVER = ServerSpec(4, Fraction(16), Fraction(350_000), Fraction(250))


def group(gid: str, n: int, d: float = 1, x: float | None = 1) -> Group:
    weights: tuple[tuple[str, Fraction | None], ...] = (
        ("det", Fraction(d)),
        ("other", None if x is None else Fraction(x)),
    )
    return Group(gid, n, "det", weights)


# --- К13 load and hardware -----------------------------------------------------------------
@pytest.mark.parametrize(
    ("n", "a95", "q", "peak", "surge", "chips", "cpu", "servers"),
    [
        (0, 0, 0, 0, 0, 0, 0, 0),
        (8, 6, 1, 144.5, 94, 3, 11.9265, 1),
        (8, 6, 6, 144.5, 164, 4, 13.428, 1),
        (16, 11, 1, 265.25, 174, 6, 22.02425, 2),
        (200, 112, 0, 2710, 2000, 52, 228.67, 15),
        (200, 112, 200, 2710, 4800, 92, 389.6, 25),
    ],
)
def test_k13_load_vectors(
    n: int, a95: int, q: int, peak: float, surge: float, chips: int, cpu: float, servers: int
) -> None:
    pol = calc.policy(load_in(priority_cameras_reserve=q, **SPLIT))
    found = calc.load_of([group("g", n)] if n else [], pol, 1)
    assert (found.cameras, found.a95, found.q) == (n, a95, q)
    assert found.peak == Fraction(str(peak)) and found.surge == Fraction(str(surge))
    assert found.chips == chips and found.cpu == Fraction(str(cpu))
    plan = calc.select(found.chips, found.cpu, EMPTY_KIT, [HP], BOARDS, SERVER)
    assert plan.purchase is not None and plan.purchase.servers == servers
    assert calc.kit_chips(plan.purchase, BOARDS) == chips


def test_cpu_can_need_more_servers_than_slots() -> None:
    found = calc.load_of(
        [group("g", 200)], calc.policy(load_in(priority_cameras_reserve=0, **SPLIT)), 1
    )
    assert math.ceil(52 / 4) == 13 < 15 == calc.servers_required(52, 52, found.cpu, SERVER)  # type: ignore[arg-type]


def test_tracker_shortens_detector_only() -> None:
    pol = calc.policy(load_in())
    same = [group("g", 8)]
    assert calc.load_of(same, pol, 1).peak == Fraction("144.5")
    assert (calc.load_of(same, pol, 2).peak, calc.load_of(same, pol, 2).chips) == (
        Fraction("108.5"),
        3,
    )
    mix = [group("pose", 4), group("det", 4, x=0)]
    assert (calc.load_of(mix, pol, 1).peak, calc.load_of(mix, pol, 1).chips) == (
        Fraction("120.5"),
        3,
    )
    assert (calc.load_of(mix, pol, 2).peak, calc.load_of(mix, pol, 2).chips) == (
        Fraction("84.5"),
        2,
    )


def test_active_p95_boundaries() -> None:
    half = Fraction(1, 2)
    assert calc.active_p95(0, half, False) == 0
    assert calc.active_p95(5, Fraction(0), False) == 0
    assert calc.active_p95(5, Fraction(1), False) == 5
    assert calc.active_p95(1, half, False) == 1  # P(X ≤ 0) = 0.5 < 0.95
    # 8 cameras: P(X ≤ 5) = 219/256 < 0.95 ≤ P(X ≤ 6) = 247/256
    assert calc.active_p95(8, half, False) == 6
    assert calc.active_p95(8, half, True) == 8
    pol = calc.policy(load_in(peak_mode="all_active"))
    assert calc.load_of([group("g", 8)], pol, 1).peak == 8 * 24


def test_reserve_clamped_and_unknown_weight() -> None:
    big = calc.load_of([group("g", 8)], calc.policy(load_in(priority_cameras_reserve=50)), 1)
    assert big.q == 8 and big.surge == 8 * 24  # the whole surge at full rate
    unknown = calc.load_of([group("g", 8, x=None)], calc.policy(load_in()), 1)
    assert (unknown.cameras, unknown.peak, unknown.chips, unknown.cpu) == (8, None, None, None)


def test_exact_capacity_and_just_above() -> None:
    exact = calc.load_of(
        [group("g", 1, x=0)], calc.policy(load_in(activity_share=1, target_fps=52.4)), 1
    )
    assert (exact.units, exact.chips) == (Fraction("52.4"), 1)
    above = calc.load_of(
        [group("g", 1, x=0)], calc.policy(load_in(activity_share=1, target_fps=52.40001)), 1
    )
    assert above.chips == 2


def test_board_choice_price_zero_unknown_and_ties() -> None:
    hpd = Board("HPD", 2, 1, Fraction(100), None)
    hpq = Board("HPQ", 4, 1, Fraction(150), Fraction(1_500_000))
    boards = {"HP": HP, "HPD": hpd, "HPQ": hpq}
    cheap = calc.select(4, Fraction(1), EMPTY_KIT, [HP, hpd, hpq], boards, SERVER)
    assert cheap.purchase is not None and cheap.purchase.boards == (("HPQ", 1),)
    assert (cheap.selection, cheap.board_capex) == ("priced_optimum", 1_500_000)
    # Equal cost 4 × HP = 1 × HPQ: fewer boards wins.
    tie = {"HP": HP, "HPQ": Board("HPQ", 4, 1, None, Fraction(2_000_000))}
    pick = calc.select(4, Fraction(1), EMPTY_KIT, [HP, tie["HPQ"]], tie, SERVER)
    assert pick.purchase is not None and pick.purchase.boards == (("HPQ", 1),)
    free = {"HP": HP, "HPD": Board("HPD", 2, 1, None, Fraction(0))}
    zero = calc.select(4, Fraction(1), EMPTY_KIT, [HP, free["HPD"]], free, SERVER)
    assert zero.purchase is not None and zero.purchase.boards == (("HPD", 2),)
    assert zero.board_capex == 0
    unpriced = {"HPD": hpd}
    tech = calc.select(3, Fraction(1), EMPTY_KIT, [hpd], unpriced, SERVER)
    assert tech.selection == "technical_only" and tech.board_capex is None
    assert tech.purchase is not None and tech.purchase.boards == (("HPD", 2),)
    unknown_server = calc.select(
        3, Fraction(1), EMPTY_KIT, [HP], BOARDS, ServerSpec(4, Fraction(16), None, None)
    )
    assert unknown_server.server_capex is None and unknown_server.board_capex == 1_500_000


def test_zero_times_unknown_is_known_zero() -> None:
    assert calc.mul(Fraction(0), None) == 0
    assert calc.mul(Fraction(2), None) is None
    assert calc.electricity(Fraction(355), Fraction(0), None) == 0
    assert calc.electricity(Fraction(355), Fraction(8760), Fraction(8)) == Fraction("24878.4")


# --- К8 money and thresholds -----------------------------------------------------------------
def test_k13_money_vector() -> None:
    capex, opex, benefit = Fraction(1_000_000), Fraction(140_000), Fraction(500_000)
    pay = calc.payback_of(capex, opex, benefit, False)
    assert (pay.status, pay.months, pay.within_horizon) == ("within_horizon", 33.333333, True)
    tco = capex + 3 * opex
    assert (tco, 3 * benefit - tco) == (1_420_000, 80_000)
    assert calc.rub(tco / (8 * 36)) == 4930.56
    severe = calc.severe_threshold(tco, Fraction(200_000), Fraction(400_000), False)
    assert (severe.status, severe.expected_prevented_cases, severe.whole_prevented_cases) == (
        "required", 2.05, 3,
    )  # fmt: skip
    assert severe.uncovered_cost_rub == 820_000
    tier = calc.TierCalc(
        "base",
        [calc.Line("boards", None), calc.Line("integration_fixed", Fraction(500_000))],
        [calc.Line("support", None), calc.Line("electricity", Fraction(40_000))],
        [calc.Line("injuries", Fraction(500_000))],
        Fraction(0),
    )
    plan = calc.Plan("technical_only", calc.kit({"HP": 1}, 0), None, Fraction(0))
    boards = {"HP": Board("HP", 1, 1, Fraction(35), None)}
    ev = calc.Evidence(_catalog())
    price = calc.price_threshold(tier, plan, boards, Fraction(1, 10), False, ev)
    assert (price.status, price.board_id, price.boards_to_buy) == ("at_or_below", "HP", 1)
    assert (price.max_unit_price_rub, price.current_unit_price_rub) == (561538.46, None)
    raw = ev.items["tier.base.board_price_threshold.raw_unit_price_rub"].value
    assert raw == 561538.46  # (3 × 460000 / 1.3 − 500000) / 1 = 561538.4615…


def test_payback_boundaries() -> None:
    f = Fraction
    assert calc.payback_of(f(10), f(5), f(5), False).status == "no_positive_effect"
    assert calc.payback_of(f(0), f(5), f(10), False).status == "no_initial_investment"
    assert calc.payback_of(f(0), f(5), f(10), False).months == 0
    assert calc.payback_of(f(0), f(0), f(0), False).status == "not_applicable"
    assert calc.payback_of(None, f(5), f(10), False).status == "insufficient_data"
    assert calc.payback_of(f(1), f(0), f(0), True).status == "not_applicable"
    exact = calc.payback_of(f(36), f(0), f(12), False)  # 12 × 36 / 12 = 36
    assert (exact.status, exact.months, exact.within_horizon) == ("within_horizon", 36, True)
    after = calc.payback_of(f(1_000_000), f(140_000), f(240_000), False)
    assert (after.status, after.months, after.within_horizon) == ("after_horizon", 120, False)
    just = calc.payback_of(f("36.001"), f(0), f(12), False)
    assert just.status == "after_horizon"


def test_severe_threshold_states() -> None:
    f = Fraction
    assert calc.severe_threshold(f(300), f(100), f(10), False).status == "already_covered"
    no_cost = calc.severe_threshold(f(400), f(100), None, False)
    assert (no_cost.status, no_cost.uncovered_cost_rub, no_cost.expected_prevented_cases) == (
        "needs_input", 100, None,
    )  # fmt: skip
    assert calc.severe_threshold(f(400), f(100), f(0), False).status == "needs_input"
    assert calc.severe_threshold(None, f(100), f(10), False).status == "needs_input"
    assert calc.severe_threshold(f(400), f(100), f(10), True).status == "not_applicable"


def _tier(
    boards_amount: Fraction | None, other: Fraction, elec: Fraction, benefit: Fraction
) -> calc.TierCalc:
    return calc.TierCalc(
        "base",
        [calc.Line("boards", boards_amount), calc.Line("servers", other)],
        [calc.Line("support", None), calc.Line("electricity", elec)],
        [calc.Line("injuries", benefit)],
        Fraction(0),
    )


def test_price_threshold_states() -> None:
    ev = calc.Evidence(_catalog())
    hp = {"HP": Board("HP", 1, 1, Fraction(35), Fraction(100))}
    r = Fraction(0)
    none = calc.Plan("priced_optimum", calc.kit({}, 1), Fraction(0), Fraction(0))
    assert (
        calc.price_threshold(
            _tier(Fraction(0), Fraction(10), Fraction(0), Fraction(0)), none, hp, r, False, ev
        ).status
        == "not_applicable"
    )
    one = calc.Plan("priced_optimum", calc.kit({"HP": 1}, 0), Fraction(100), Fraction(0))
    neg = calc.price_threshold(
        _tier(Fraction(100), Fraction(1000), Fraction(0), Fraction(1)), one, hp, r, False, ev
    )
    assert (neg.status, neg.max_unit_price_rub) == ("free_still_insufficient", None)
    # 3 × (B − F) / 1 − C_other = 3 × 100 − 300 = 0: zero is a valid limit.
    zero = calc.price_threshold(
        _tier(Fraction(100), Fraction(300), Fraction(0), Fraction(100)), one, hp, r, False, ev
    )
    assert (zero.status, zero.max_unit_price_rub) == ("at_or_below", 0)
    within = calc.price_threshold(
        _tier(Fraction(100), Fraction(0), Fraction(0), Fraction(100)), one, hp, r, False, ev
    )
    assert (within.status, within.max_unit_price_rub) == ("already_within", 300)
    two = {"HP": Board("HP", 1, 1, None, None), "HPD": Board("HPD", 2, 1, None, None)}
    both = calc.Plan("technical_only", calc.kit({"HP": 1, "HPD": 1}, 0), None, Fraction(0))
    assert (
        calc.price_threshold(
            _tier(None, Fraction(0), Fraction(0), Fraction(1)), both, two, r, False, ev
        ).status
        == "insufficient_data"
    )
    third = calc.price_threshold(
        _tier(Fraction(100), Fraction(0), Fraction(0), Fraction(1, 9)), one, hp, r, False, ev
    )
    assert third.max_unit_price_rub == 0.33  # 1/3 ₽ rounded down to the kopeck


def _catalog() -> calc.Catalog:
    return calc.Catalog({}, {}, {}, {}, Fraction("12.4"), ("linq_platform_queue",), False)


def test_largest_remainder() -> None:
    shares = [("b", Fraction(1, 3)), ("a", Fraction(1, 3)), ("c", Fraction(1, 3))]
    assert calc.largest_remainder(10, shares) == {"a": 4, "b": 3, "c": 3}  # tie: id ascending
    assert calc.largest_remainder(0, shares) == {"a": 0, "b": 0, "c": 0}


# --- API --------------------------------------------------------------------------------------
async def post(
    client: httpx.AsyncClient, url: str, body: Any, role: dict[str, str] = MANAGEMENT
) -> httpx.Response:
    return await client.post(url, json=body, headers=role)


def numbers(got: Any, want: Any, path: str = "") -> list[str]:
    """Differences of every value the contract example states (texts excluded)."""
    if isinstance(want, dict):
        return [
            line for key, value in want.items()
            if key not in ("note", "reason", "title", "evidence", "sources", "warnings", "input")
            for line in numbers(got.get(key, KeyError), value, f"{path}.{key}")
        ]  # fmt: skip
    if isinstance(want, list):
        if not isinstance(got, list) or len(got) != len(want):
            return [f"{path}: {got!r} != {want!r}"]
        return [
            line
            for i, (g, w) in enumerate(zip(got, want, strict=True))
            for line in numbers(g, w, f"{path}[{i}]")
        ]
    return [] if got == want else [f"{path}: {got!r} != {want!r}"]


async def test_k14_rollout_scale_partial_examples(client: httpx.AsyncClient) -> None:
    r = await post(client, ROLLOUT, fixture("rollout_request"))
    assert r.status_code == 200, r.text
    assert numbers(r.json(), fixture("rollout_result")) == []
    ResultV2.model_validate(r.json())
    r = await post(client, SCALE, fixture("scale_request"), ADMIN)
    assert r.status_code == 200, r.text
    assert numbers(r.json(), fixture("scale_projection")) == []
    body = fixture("rollout_request")
    body["hardware"]["allowed_board_ids"] = ["HP"]
    body["hardware"]["board_price_overrides"] = {"HP": None}
    r = await post(client, ROLLOUT, body)
    assert r.status_code == 200, r.text
    assert numbers(r.json(), fixture("partial_projection")) == []


async def test_defaults_v2_bodies_match_contract(client: httpx.AsyncClient) -> None:
    r = await client.get("/api/calculator/defaults")
    assert r.status_code == 200, r.text
    got, want = r.json()["v2"], fixture("defaults_v2")
    for key in (
        "format",
        "contract_version",
        "formula_version",
        "rollout",
        "scale",
        "presets",
        "boards",
        "features",
        "market",
    ):
        assert got[key] == want[key], key
    assert {m["id"]: m for m in got["models"]}[DET] == want["models"][0]
    assert {m["id"]: m for m in got["models"]}[POSE] == want["models"][1]
    codes = [n["code"] for n in got["notices"]]
    assert "SFR_PREVENTION_INFO" in codes and "SFR_DISCOUNT_CONDITIONS" in codes
    ids = {s["id"] for s in got["sources"]}
    referenced = (
        {s for e in got["assumptions"] for s in e["source_ids"]}
        | {s for b in got["boards"] for s in b["source_ids"]}
        | {s for m in got["models"] for s in m["source_ids"]}
    )
    assert referenced <= ids and {"sfr_prevention", "sfr_discount"} <= ids
    assert got["system_profile"] == {"cameras": 0, "groups": []}
    assert [m["status"] for m in got["measurements"]] == ["not_measured", "not_measured"]


@pytest.mark.parametrize(
    ("preset", "chips", "servers", "base_capex"),
    [
        # 5 cameras: A95 = 4, peak 1.25 + 4 × 23.75 = 96.25 → 2 chips; 1 000 000 + 350 000 + 300 000
        ("workshop", 2, 1, 1_650_000),
        # 20 cameras: A95 = 14, peak = 5 + 14 × 23.75 = 337.5 → 7 chips, 2 servers
        ("shop", 7, 2, 7 * 500_000 + 2 * 350_000 + 300_000),
        # 200 cameras: peak 2710 → 52 chips; CPU 2710 × 0.077 = 208.67 → 14 servers
        ("plant", 52, 14, 52 * 500_000 + 14 * 350_000 + 300_000),
    ],
)
async def test_presets_control_numbers(
    client: httpx.AsyncClient, preset: str, chips: int, servers: int, base_capex: int
) -> None:
    defaults = (await client.get("/api/calculator/defaults")).json()["v2"]
    body = next(p["rollout"] for p in defaults["presets"] if p["id"] == preset)
    found = (await post(client, ROLLOUT, body)).json()
    assert found["status"] == "estimated"
    assert (found["load"]["required_chips"], found["hardware"]["purchase"]["servers"]) == (
        chips,
        servers,
    )
    assert found["tiers"][0]["capex_rub"] == base_capex
    request_ev = {e["key"]: e for e in found["evidence"]}
    assert request_ev["request.site.workers"]["status"] == "assumed"  # the preset's own number


async def test_line_sums_and_serialization(client: httpx.AsyncClient) -> None:
    body = fixture("rollout_request")
    body["benefits"]["fines"]["enabled"] = True
    body["benefits"]["sfr_discount"] = {
        "enabled": True,
        "payroll_rub_year": 10_000_000,
        "tariff_share": 0.002,
        "additional_discount_share": 0.4,
    }
    r = await post(client, ROLLOUT, body)
    text = r.text
    assert "NaN" not in text and "Infinity" not in text
    found = r.json()
    for tier in found["tiers"]:
        assert sum(x["amount_rub"] for x in tier["capex_lines"]) == pytest.approx(
            tier["capex_rub"], abs=0.005
        )
        assert sum(x["amount_rub"] for x in tier["opex_lines"]) == pytest.approx(
            tier["opex_rub_year"], abs=0.005
        )
        included = [x["amount_rub"] for x in tier["benefit_lines"] if x["included"]]
        assert sum(included) == pytest.approx(tier["gross_benefit_rub_year"], abs=0.005)
        assert tier["tco_3_year_rub"] == pytest.approx(
            tier["capex_rub"] + 3 * tier["opex_rub_year"], abs=0.01
        )
    base = {x["id"]: x["amount_rub"] for x in found["tiers"][0]["benefit_lines"]}
    # fines: 0.1 × 65000 × 0.2 + 0.1 × 140000 × 0.2; SFR: 10 000 000 × 0.002 × 0.4
    assert (base["fines"], base["sfr_discount"]) == (1300 + 2800, 8000)
    assert set(found) == set(ResultV2.model_fields)
    assert [t["tier"] for t in found["tiers"]] == ["base", "extended", "max"]
    assert [s["id"] for s in found["steps"]] == [
        "naive",
        "dedicated_capacity",
        "scenario_models",
        "activity_pool",
        "tracker",
    ]
    assert [p["cameras"] for p in found["scale_curve"]["points"]] == [5, 10, 25, 50, 100, 200, 500]
    used = {s for e in found["evidence"] for s in e["source_ids"]}
    assert used - {s["id"] for s in found["sources"]} <= {
        s["id"] for s in (await client.get("/api/calculator/defaults")).json()["v2"]["sources"]
    }


async def test_partial_disabled_and_independent_threshold(client: httpx.AsyncClient) -> None:
    body = fixture("rollout_request")
    body["benefits"]["downtime"]["enabled"] = True  # nulls of an enabled line: partial, not 422
    found = (await post(client, ROLLOUT, body)).json()
    assert found["status"] == "partial"
    assert {(m["code"], m["field"]) for m in found["missing"]} >= {
        ("BENEFIT_INPUT_MISSING", "benefits.downtime.events_year")
    }
    base = found["tiers"][0]
    downtime = next(x for x in base["benefit_lines"] if x["id"] == "downtime")
    assert (downtime["amount_rub"], downtime["included"], downtime["status"]) == (
        None,
        True,
        "missing",
    )
    assert (
        base["gross_benefit_rub_year"] is None and base["payback"]["status"] == "insufficient_data"
    )
    assert base["capex_rub"] == 2_150_000  # the known parts stay
    # An unknown injury line does not block the severe threshold of the other lines.
    body = fixture("rollout_request")
    body["benefits"]["injuries"]["rate_per_1000"] = None
    body["benefits"]["fines"]["enabled"] = True
    body["benefits"]["severe_injury_cost_rub"] = 2_000_000
    found = (await post(client, ROLLOUT, body)).json()
    severe = found["tiers"][0]["severe_threshold"]
    tco = found["tiers"][0]["tco_3_year_rub"]
    assert severe["status"] == "required"
    assert severe["expected_prevented_cases"] == pytest.approx(
        (tco - 3 * 4100) / 2_000_000, abs=1e-6
    )
    off = next(x for x in found["tiers"][0]["benefit_lines"] if x["id"] == "labor")
    assert (off["amount_rub"], off["included"], off["status"]) == (0, False, "not_applicable")


async def test_empty_project(client: httpx.AsyncClient) -> None:
    body = fixture("rollout_request")
    body["cameras"] = {"source": "manual", "cameras": 0, "groups": []}
    found = (await post(client, ROLLOUT, body)).json()
    assert found["status"] == "empty"
    base = found["tiers"][0]
    assert (base["capex_rub"], base["opex_rub_year"], base["gross_benefit_rub_year"]) == (0, 0, 0)
    assert (base["rub_per_camera_month"], base["payback"]["status"]) == (None, "not_applicable")
    assert found["hardware"]["purchase"]["boards"] == []


async def test_scale_inventory_vectors(client: httpx.AsyncClient) -> None:
    """К13: 8 → 16 cameras, split CPU, HP 500000, server 350000, other costs 0."""
    base = fixture("scale_request")
    base["load"] |= SPLIT
    for (hp, servers), (buy_hp, buy_servers, cost) in {
        (3, 1): (3, 1, 1_850_000), (4, 1): (2, 1, 1_350_000), (6, 2): (0, 0, 0),
    }.items():  # fmt: skip
        body = copy.deepcopy(base)
        body["installed"] = {"boards": [{"board_id": "HP", "count": hp}], "servers": servers}
        found = (await post(client, SCALE, body, ADMIN)).json()
        hw = found["hardware"]
        assert hw["inventory_basis"] == "provided"
        assert hw["purchase"]["boards"] == ([{"board_id": "HP", "count": buy_hp}] if buy_hp else [])
        assert hw["purchase"]["servers"] == buy_servers
        assert hw["board_capex_rub"] + hw["server_capex_rub"] == cost
        assert found["cost_scope"] == "incremental" and found["tiers"][0]["camera_denominator"] == 8
    base["installed"] = None
    estimated = (await post(client, SCALE, base, ADMIN)).json()
    assert estimated["hardware"]["inventory_basis"] == "estimated"
    assert "INVENTORY_ESTIMATED" in [w["code"] for w in estimated["warnings"]]
    short = copy.deepcopy(base)
    short["installed"] = {"boards": [{"board_id": "HP", "count": 1}], "servers": 1}
    short["added"] = {"source": "manual", "cameras": 0, "groups": []}
    short["costs"]["new_camera_count"] = 0  # ≤ the added cameras
    found = (await post(client, SCALE, short, ADMIN)).json()
    assert "EXISTING_CAPACITY_SHORTFALL" in [w["code"] for w in found["warnings"]]
    assert found["hardware"]["purchase"]["boards"] == [{"board_id": "HP", "count": 2}]  # 3 − 1
    assert found["tiers"][0]["capex_rub"] == 1_000_000  # no added area: only the shortfall
    assert found["tiers"][0]["gross_benefit_rub_year"] == 0
    enough = copy.deepcopy(short)
    enough["installed"] = {"boards": [{"board_id": "HP", "count": 3}], "servers": 1}
    enough["costs"]["new_camera_count"] = 0
    found = (await post(client, SCALE, enough, ADMIN)).json()
    assert (
        found["tiers"][0]["capex_rub"] == 0
        and found["tiers"][0]["payback"]["status"] == "not_applicable"
    )


ERRORS: list[tuple[str, Any, str, str]] = [
    ("load.activity_share", 1.2, "load.activity_share", "OUT_OF_RANGE"),
    ("contract_version", "1.0.0", "contract_version", "UNSUPPORTED_VERSION"),
    ("load.nope", 1, "load.nope", "UNKNOWN_FIELD"),
    ("load.detector_stride", 2, "load.detector_stride", "TRACKER_NOT_VALIDATED"),
    ("load.target_fps", 121, "load.target_fps", "OUT_OF_RANGE"),
    ("load.priority_cameras_reserve", 1.0, "load.priority_cameras_reserve", "SCHEMA_MISMATCH"),
    ("load.decode_cores_per_camera", 0.1, "load.decode_cores_per_camera", "OUT_OF_RANGE"),
    ("cameras.groups.0.share", 0.5, "cameras.groups", "GROUP_SHARES"),
    ("cameras.groups.0.model_ids", [POSE], "cameras.groups.0.model_ids", "SCHEMA_MISMATCH"),
    ("cameras.groups.0.model_ids", [DET, "nope@1"], "cameras.groups.0.model_ids", "UNKNOWN_MODEL"),
    ("hardware.allowed_board_ids", ["HP", "HP"], "hardware.allowed_board_ids", "SCHEMA_MISMATCH"),
    (
        "hardware.board_price_overrides",
        {"XX": 1},
        "hardware.board_price_overrides.XX",
        "UNKNOWN_BOARD",
    ),
    ("costs.new_camera_count", 9, "costs.new_camera_count", "OUT_OF_RANGE"),
    (
        "benefits.sfr_discount.additional_discount_share",
        0.5,
        "benefits.sfr_discount.additional_discount_share",
        "OUT_OF_RANGE",
    ),
    (
        "load.activity_measurement_id",
        "activity_share-nope",
        "load.activity_measurement_id",
        "MEASUREMENT_MISMATCH",
    ),
]


def _set(body: dict[str, Any], path: str, value: Any) -> None:
    *head, last = path.split(".")
    node: Any = body
    for part in head:
        node = node[int(part)] if part.isdigit() else node[part]
    node[int(last) if last.isdigit() else last] = value


@pytest.mark.parametrize(("path", "value", "field", "reason"), ERRORS)
async def test_validation_errors(
    client: httpx.AsyncClient, path: str, value: Any, field: str, reason: str
) -> None:
    body = fixture("rollout_request")
    _set(body, path, value)
    r = await post(client, ROLLOUT, body)
    assert r.status_code == 422, r.text
    assert r.json()["details"] == {"field": field, "reason": reason}
    assert r.json()["code"] == "validation"


async def test_exact_error_bodies_and_format(client: httpx.AsyncClient) -> None:
    body = fixture("rollout_request")
    body["load"]["activity_share"] = 1.2
    assert (await post(client, ROLLOUT, body)).json() == fixture("error_validation")
    fmt = fixture("error_format")
    good = fixture("rollout_request")
    assert (await post(client, "/api/calculator/rollout?format=v3", good)).json() == fmt
    assert (
        await post(client, "/api/calculator/rollout", good)
    ).json() == fmt  # v2 body, legacy format
    legacy = (await client.get("/api/calculator/defaults")).json()["rollout"]
    assert (await post(client, ROLLOUT, legacy)).json() == fmt  # legacy body, v2 format
    r = await client.post(
        ROLLOUT, content=b'{"contract_version": "2.0.0", "x": NaN}', headers=MANAGEMENT
    )
    assert r.status_code == 422
    nan = fixture("rollout_request")
    text = json.dumps(nan).replace('"activity_share": 0.5', '"activity_share": NaN')
    r = await client.post(
        ROLLOUT, content=text.encode(), headers=MANAGEMENT | {"content-type": "application/json"}
    )
    assert r.json()["details"] == {"field": "load.activity_share", "reason": "OUT_OF_RANGE"}
    double = fixture("rollout_request")
    double["benefits"]["injuries"]["cost_scope"] = "all_in"
    assert (await post(client, ROLLOUT, double)).status_code == 200  # nothing else is counted
    double["benefits"]["downtime"]["enabled"] = True
    assert (await post(client, ROLLOUT, double)).json()["details"] == {
        "field": "benefits.injuries.cost_scope", "reason": "DOUBLE_COUNTING",
    }  # fmt: skip
    double["benefits"]["injuries"]["enabled"] = False  # a stored scope of an off line is harmless
    assert (await post(client, ROLLOUT, double)).status_code == 200
    huge = fixture("rollout_request")
    huge["load"]["capacity_derate"] = 0.000001
    r = await post(client, ROLLOUT, huge)
    assert (r.status_code, r.json()["code"]) == (409, "calculation_limit")
    scale = fixture("scale_request")
    scale["installed"] = {"boards": [{"board_id": "HP", "count": 5}], "servers": 1}
    r = await post(client, SCALE, scale, ADMIN)
    assert r.json()["details"] == {"field": "installed.servers", "reason": "INVENTORY_CAPACITY"}


async def test_roles_and_pdf(client: httpx.AsyncClient) -> None:
    rollout, scale = fixture("rollout_request"), fixture("scale_request")
    for url, body, role, status in [
        (ROLLOUT, rollout, {"X-Role": "admin"}, 403),
        (ROLLOUT, rollout, {}, 400),
        (SCALE, scale, {"X-Role": "ohs"}, 403),
        (SCALE, scale, ADMIN, 200),
        (SCALE, scale, MANAGEMENT, 200),
    ]:
        assert (await post(client, url, body, role)).status_code == status, (url, role)
    pdf = "/api/calculator/export.pdf"
    r = await post(client, pdf, {"mode": "rollout", "input": rollout})
    assert (r.status_code, r.json()) == (501, fixture("error_pdf"))
    assert (
        await post(client, pdf, {"mode": "scale", "input": scale}, {"X-Role": "ohs"})
    ).status_code == 403
    features = (await client.get("/api/calculator/defaults")).json()["v2"]["features"]
    assert (features["pdf_available"], features["tracker"]["available"]) == (False, False)


async def test_system_profile_from_rules(client: httpx.AsyncClient, core: Settings) -> None:
    c = cameras()
    services.camera_rule_set(c["south"], "fall", CameraRuleIn(enabled=False), "admin")
    services.camera_rule_set(c["south"], "phone", CameraRuleIn(enabled=False), "admin")
    services.camera_rule_set(c["south"], "fire_smoking", CameraRuleIn(enabled=False), "admin")
    body = fixture("rollout_request")
    body["cameras"] = {"source": "system", "camera_ids": None, "include_seed": False}
    found = (await post(client, ROLLOUT, body)).json()
    groups = found["resolved"]["added"]["groups"]
    assert [(g["camera_ids"], g["model_ids"]) for g in groups] == [
        ([c["north"]], [DET, POSE]), ([c["south"]], [DET]),
    ]  # fmt: skip
    assert found["load"]["cameras"] == 2 and found["status"] == "estimated"
    services.camera_rule_set(c["south"], "no_harness", CameraRuleIn(enabled=True), "admin")
    found = (await post(client, ROLLOUT, body)).json()
    assert found["status"] == "partial" and found["load"]["required_chips"] is None
    assert "SCENARIO_MODEL_MISSING" in [m["code"] for m in found["missing"]]
    body["cameras"] = {
        "source": "system",
        "camera_ids": [c["north"], c["north"]],
        "include_seed": False,
    }
    assert (await post(client, ROLLOUT, body)).json()["details"]["reason"] == "DUPLICATE_CAMERA"
    body["cameras"] = {"source": "system", "camera_ids": [999], "include_seed": False}
    assert (await post(client, ROLLOUT, body)).json()["details"] == {
        "field": "cameras.camera_ids",
        "reason": "OUT_OF_RANGE",
    }
    store.run("UPDATE cameras SET deleted_at = ? WHERE id = ?", clock.iso(clock.now()), c["south"])
    defaults = (await client.get("/api/calculator/defaults")).json()["v2"]
    assert defaults["system_profile"]["cameras"] == 1


def _artifact(
    settings: Settings, camera: int, frames_with_person: int, frames: int, sha: str
) -> None:
    lines = [
        json.dumps({"frame_idx": i, "ts_ms": i * 83.3, "detections": [
            {"cls": 0, "name": "person", "score": 0.9 if i < frames_with_person else 0.3,
             "bbox_xyxy": [0, 0, 1, 1]}]})
        for i in range(frames)
    ]  # fmt: skip
    path = settings.data_dir / "artifacts" / f"{sha}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    at = clock.iso(clock.now())
    store.insert("videos", {
        "camera_id": camera, "filename": f"{sha}.mp4", "sha256": sha, "path": f"uploads/{sha}.mp4",
        "size_bytes": 1, "width": 1, "height": 1, "fps": 12, "frame_count": frames,
        "duration_ms": 1000, "codec": "h264", "browser_playable": 1, "status": "ready",
        "created_at": at,
    })  # fmt: skip
    store.insert("artifacts", {
        "cache_key": f"k{sha}", "video_sha256": sha, "model_id": "det-yolov8n",
        "model_version": "640-ap9999", "task": "detect", "input_size": 640, "step": 2,
        "backend": "linq", "fake": 0, "path": f"artifacts/{sha}.jsonl", "frames": frames,
        "metrics_json": json.dumps({"throughput_fps": 0}), "created_at": at,
    })  # fmt: skip


async def test_activity_measurement_applies_only_by_id(
    client: httpx.AsyncClient, core: Settings
) -> None:
    c = cameras()
    _artifact(core, c["north"], 3, 4, "a1")  # 0.75
    _artifact(core, c["south"], 1, 4, "b1")  # 0.25
    measured = (await client.get("/api/calculator/defaults")).json()["v2"]["measurements"]
    activity = next(m for m in measured if m["key"] == "activity_share")
    assert (activity["status"], activity["value"], activity["sample_count"]) == ("measured", 0.5, 2)
    body = fixture("rollout_request")
    body["load"]["activity_measurement_id"] = activity["id"]
    found = (await post(client, ROLLOUT, body)).json()
    assert "DEMO_ACTIVITY_BIASED" in [w["code"] for w in found["warnings"]]
    body["load"]["activity_share"] = 0.6  # edited by hand, the id stays: mismatch
    r = await post(client, ROLLOUT, body)
    assert r.json()["details"]["reason"] == "MEASUREMENT_MISMATCH"
    _artifact(core, c["south"], 4, 4, "b2")  # new content → a new id
    again = (await client.get("/api/calculator/defaults")).json()["v2"]["measurements"]
    assert next(m for m in again if m["key"] == "activity_share")["id"] != activity["id"]


async def test_legacy_runs_on_the_new_engine(client: httpx.AsyncClient) -> None:
    legacy = (await client.get("/api/calculator/defaults")).json()["rollout"]
    for url in ("/api/calculator/rollout", "/api/calculator/rollout?format=legacy"):
        r = await post(client, url, legacy)
        assert r.status_code == 200, r.text
        assert "format" not in r.json() and r.json()["tiers"][0]["accelerators"] == 3
    for overrides in (
        {"models_per_frame": 0},
        {"models_per_frame": 0.5},
        {"accelerators_per_server": 2.5},
    ):
        r = await post(client, "/api/calculator/rollout", legacy | {"overrides": overrides})
        assert r.status_code == 200, (overrides, r.text)
    zero = (
        await post(
            client, "/api/calculator/rollout", legacy | {"overrides": {"models_per_frame": 0}}
        )
    ).json()
    assert zero["tiers"][0]["accelerators"] == 0 and zero["tiers"][0]["servers"] == 0
    r = await post(client, "/api/calculator/scale", {"cameras_now": 8, "new_cameras": 8}, ADMIN)
    assert (r.json()["accelerators_now"], r.json()["accelerators_total"]) == (3, 6)


async def test_system_any_class_needs_one_model(client: httpx.AsyncClient, core: Settings) -> None:
    c = cameras()
    services.camera_rule_set(c["north"], "fire_smoking", CameraRuleIn(enabled=True), "admin")
    body = fixture("rollout_request")
    body["cameras"] = {"source": "system", "camera_ids": [c["north"]], "include_seed": False}
    found = (await post(client, ROLLOUT, body)).json()
    models = found["resolved"]["added"]["groups"][0]["model_ids"]
    assert models == [DET, POSE, "matvey-fire-smoke-yolov8n@640-s04-v1-4c9f5d05c4d4"]  # no cigarette
    assert [m["code"] for m in found["missing"]] == ["MODEL_COST_UNKNOWN"]  # its weight is unsigned
