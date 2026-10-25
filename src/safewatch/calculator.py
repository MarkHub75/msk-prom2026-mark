"""Payback and scale calculator (tech.md 8.25, docs/contracts/calculator_v2.md): pure functions.

One engine serves both formats: load (К6), hardware (К7), money and thresholds (К8). The
legacy 1.1.0 routes are an adapter over it (К12). Arithmetic is exact (`Fraction`): a ceil
of the load never sees float noise and money is rounded only on output (К3).
"""

import math
from collections.abc import Callable, Iterator
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any, Literal, cast, get_args

from pydantic import BaseModel
from scipy.stats import binom

from safewatch import texts
from safewatch.config import CalcInputConfig
from safewatch.errors import Conflict, ValidationFailed
from safewatch.types import (
    BoardCount,
    BoardOffer,
    CalcAssumption,
    CalcMode,
    CalcTier,
    CurvePoint,
    EquipmentState,
    HardwareResult,
    LoadInput,
    LoadResult,
    ManualCameraProfile,
    ModelLoad,
    MoneyLine,
    Notice,
    NumberStatus,
    NumericEvidence,
    PaybackResult,
    PriceThreshold,
    ResolvedGroup,
    ResolvedProfile,
    ResolvedV2,
    ResultStatus,
    ResultV2,
    RolloutIn,
    RolloutRequestV2,
    RolloutResult,
    ScaleCurve,
    ScaleIn,
    ScaleRequestV2,
    ScaleResult,
    SevereThreshold,
    SourceRecord,
    StepV2,
    TierResult,
    TierResultV2,
    WhyItem,
)

Q = Fraction | None
Request = RolloutRequestV2 | ScaleRequestV2
TIERS: tuple[CalcTier, ...] = ("base", "extended", "max")
HORIZON_YEARS = 3
MONTHS = 12 * HORIZON_YEARS
CURVE_POINTS = (5, 10, 25, 50, 100, 200, 500)
MAX_CAMERAS = 10_000
MAX_GROUPS = 128
MAX_MODELS = 32
MAX_BOARDS = 64
MAX_CHIPS = 100_000  # К3: a bigger technical task is 409 calculation_limit
SEARCH_BUDGET = 2_000_000  # board combinations of one selection (К7: bounded exact search)
PCT95 = 0.95


# --- numbers ------------------------------------------------------------------------------
def fr(x: float | int) -> Fraction:
    """The decimal the client sent: 0.15 is 3/20, not the nearest binary double."""
    return Fraction(repr(x)) if isinstance(x, float) else Fraction(x)


def opt(x: float | int | None) -> Q:
    return None if x is None else fr(x)


def _round(x: Fraction, digits: int) -> float:
    scale = 10**digits
    return float(Fraction(math.floor(x * scale + Fraction(1, 2)), scale))


def rub(x: Q) -> float | None:
    """Money to kopecks (К3)."""
    return None if x is None else _round(x, 2)


def num(x: Q) -> float | None:
    """Load, cores, months and thresholds to 6 digits (К3)."""
    return None if x is None else _round(x, 6)


def rub_down(x: Fraction) -> float:
    """A price limit is shown rounded down to the kopeck: it never exceeds the threshold."""
    return float(Fraction(math.floor(x * 100), 100))


def ceil(x: Fraction) -> int:
    return math.ceil(x)


def mul(*factors: Q) -> Q:
    """0 × unknown is a known 0 (К3); otherwise any unknown factor makes the product unknown."""
    if any(f is not None and f == 0 for f in factors):
        return Fraction(0)
    out = Fraction(1)
    for f in factors:
        if f is None:
            return None
        out *= f
    return out


def total(values: list[Q]) -> Q:
    out = Fraction(0)
    for v in values:
        if v is None:
            return None
        out += v
    return out


def invalid(field: str, reason: str) -> ValidationFailed:
    message = texts.CALC2_FIELD_INVALID.format(field=field)
    return ValidationFailed(message, field=field, reason=reason)


def limit_error() -> Conflict:
    return Conflict("calculation_limit", texts.CALC2_LIMIT.format(n=MAX_CHIPS), limit=MAX_CHIPS)


# --- camera groups ------------------------------------------------------------------------
@dataclass(frozen=True)
class Group:
    """Cameras with one model set; `weights` are work units, None when unknown (К6)."""

    id: str
    cameras: int
    detector: str
    weights: tuple[tuple[str, Q], ...]

    @property
    def d(self) -> Q:
        return dict(self.weights)[self.detector]

    @property
    def x(self) -> Q:
        return total([w for m, w in self.weights if m != self.detector])


def largest_remainder(n: int, shares: list[tuple[str, Fraction]]) -> dict[str, int]:
    """Whole cameras of `n` by shares: floor, then the remainder by fraction desc, id asc (К4)."""
    raw = {gid: n * share for gid, share in shares}
    out = {gid: math.floor(value) for gid, value in raw.items()}
    left = n - sum(out.values())
    order = sorted(shares, key=lambda item: (-(raw[item[0]] - out[item[0]]), item[0]))
    for gid, _ in order[:left]:
        out[gid] += 1
    return out


def manual_groups(profile: ManualCameraProfile) -> list[ResolvedGroup]:
    counts = largest_remainder(profile.cameras, [(g.id, fr(g.share)) for g in profile.groups])
    return [
        ResolvedGroup(id=g.id, cameras=counts[g.id], camera_ids=[], model_ids=g.model_ids)
        for g in profile.groups
        if counts[g.id] > 0
    ]


def prefixed(groups: list[ResolvedGroup], prefix: str) -> list[ResolvedGroup]:
    """Group ids of `resolved.total` (К8): current:… and added:… never collide."""
    return [g.model_copy(update={"id": f"{prefix}:{g.id}"}) for g in groups]


def profile(groups: list[ResolvedGroup]) -> ResolvedProfile:
    return ResolvedProfile(cameras=sum(g.cameras for g in groups), groups=groups)


@dataclass(frozen=True)
class Catalog:
    models: dict[str, ModelLoad]
    boards: dict[str, BoardOffer]
    sources: dict[str, SourceRecord]
    inputs: dict[str, CalcInputConfig]
    platform_fps: Fraction  # naive denominator: a measurement or the signed default
    platform_source_ids: tuple[str, ...]
    tracker_available: bool


def model_weight(model_id: str, load: LoadInput, catalog: Catalog) -> Q:
    if model_id in load.model_cost_overrides:
        return fr(load.model_cost_overrides[model_id])
    return opt(catalog.models[model_id].work_units)


def to_groups(resolved: list[ResolvedGroup], load: LoadInput, catalog: Catalog) -> list[Group]:
    out = []
    for g in resolved:
        detector = next(m for m in g.model_ids if catalog.models[m].kind == "detector")
        weights = tuple((m, model_weight(m, load, catalog)) for m in g.model_ids)
        out.append(Group(g.id, g.cameras, detector, weights))
    return out


def scaled(groups: list[Group], n: int) -> list[Group]:
    """The same model mix for `n` cameras (scale curve, К8): largest remainder of the shares."""
    cameras = sum(g.cameras for g in groups)
    counts = largest_remainder(n, [(g.id, Fraction(g.cameras, cameras)) for g in groups])
    return [replace(g, cameras=counts[g.id]) for g in groups if counts[g.id] > 0]


# --- load (К6) ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Policy:
    p: Fraction
    f: Fraction
    b: Fraction  # min(target, surge)
    i: Fraction  # 1 / idle_check_s
    all_active: bool
    reserve: int
    capacity: Fraction  # C = reference × derate
    cpu_ms: Fraction
    decode: Fraction


def policy(load: LoadInput, target_fps: Fraction | None = None) -> Policy:
    f = fr(load.target_fps) if target_fps is None else target_fps
    return Policy(
        p=fr(load.activity_share),
        f=f,
        b=min(f, fr(load.surge_fps)),
        i=1 / fr(load.idle_check_s),
        all_active=load.peak_mode == "all_active",
        reserve=load.priority_cameras_reserve,
        capacity=fr(load.reference_chip_fps) * fr(load.capacity_derate),
        cpu_ms=fr(load.cpu_ms_per_unit),
        decode=fr(load.decode_cores_per_camera),
    )


def active_p95(n: int, p: Fraction, all_active: bool) -> int:
    """The least k with P(Bin(n, p) ≤ k) ≥ 0.95 (К6); all_active: n."""
    if n == 0 or p == 0:
        return 0
    if all_active or p == 1:
        return n
    k = int(binom.ppf(PCT95, n, float(p)))
    while k > 0 and binom.cdf(k - 1, n, float(p)) >= PCT95:
        k -= 1
    while binom.cdf(k, n, float(p)) < PCT95:
        k += 1
    return min(k, n)


def top(k: int, items: list[tuple[Fraction, str, int]]) -> Fraction:
    """Top(k, delta): the k most expensive cameras, groups by delta desc, id asc (К6)."""
    out, left = Fraction(0), k
    for delta, _, n in sorted(items, key=lambda item: (-item[0], item[1])):
        take = min(n, left)
        out += take * delta
        left -= take
    return out


@dataclass(frozen=True)
class Load:
    cameras: int
    a95: int
    q: int
    peak: Q
    surge: Q
    units: Q
    chips: int | None
    cpu: Q


def cpu_cores(units: Fraction, n: int, pol: Policy) -> Fraction:
    return units * pol.cpu_ms / 1000 + n * pol.decode


def load_of(groups: list[Group], pol: Policy, stride: int) -> Load:
    """peak = Σ n·idle + Top(A95, active − idle); surge = Σ n·surge + Top(q, active − surge)."""
    n = sum(g.cameras for g in groups)
    a95 = active_p95(n, pol.p, pol.all_active)
    q = min(pol.reserve, n)
    if any(g.d is None or g.x is None for g in groups):
        return Load(n, a95, q, None, None, None, None, None)
    peak_items, surge_items = [], []
    idle_sum, surge_sum = Fraction(0), Fraction(0)
    for g in groups:
        d, x = cast(Fraction, g.d), cast(Fraction, g.x)
        active = pol.f * (d / stride + x)
        idle = pol.i * d
        surge = pol.b * (d / stride + x)
        idle_sum += g.cameras * idle
        surge_sum += g.cameras * surge
        peak_items.append((active - idle, g.id, g.cameras))
        surge_items.append((active - surge, g.id, g.cameras))
    peak = idle_sum + top(a95, peak_items)
    surge = surge_sum + top(q, surge_items)
    units = max(peak, surge)
    return Load(n, a95, q, peak, surge, units, ceil(units / pol.capacity), cpu_cores(units, n, pol))


def full_units(groups: list[Group], pol: Policy) -> Q:
    """N·f·M_full: every camera runs every distinct model of the profile, every frame."""
    weights: dict[str, Q] = {}
    for g in groups:
        weights.update(g.weights)
    m_full = total(list(weights.values()))
    n = sum(g.cameras for g in groups)
    return None if m_full is None else n * pol.f * m_full


def scenario_units(groups: list[Group], pol: Policy) -> Q:
    """Every camera active with only its own models, detector every frame."""
    return total([mul(Fraction(g.cameras), pol.f, total([g.d, g.x])) for g in groups])


# --- hardware (К7) ------------------------------------------------------------------------
@dataclass(frozen=True)
class Board:
    id: str
    chips: int
    slots: int
    power: Q
    price: Q


@dataclass(frozen=True)
class ServerSpec:
    slots: int
    cores: Fraction
    price: Q
    power: Q
    chips_per_server: Fraction | None = None  # legacy `accelerators_per_server` (К12)


@dataclass(frozen=True)
class Kit:
    boards: tuple[tuple[str, int], ...]  # board id → count > 0, by id
    servers: int


EMPTY_KIT = Kit((), 0)


def kit(counts: dict[str, int], servers: int) -> Kit:
    return Kit(tuple(sorted((b, n) for b, n in counts.items() if n > 0)), servers)


def kit_chips(k: Kit, boards: dict[str, Board]) -> int:
    return sum(n * boards[b].chips for b, n in k.boards)


def kit_slots(k: Kit, boards: dict[str, Board]) -> int:
    return sum(n * boards[b].slots for b, n in k.boards)


def kit_power(k: Kit, boards: dict[str, Board], spec: ServerSpec) -> Q:
    """Passport maxima: an upper estimate, not the measured draw (К7)."""
    parts = [mul(Fraction(n), boards[b].power) for b, n in k.boards]
    return total([*parts, mul(Fraction(k.servers), spec.power)])


def kit_add(a: Kit, b: Kit) -> Kit:
    counts = dict(a.boards)
    for board, n in b.boards:
        counts[board] = counts.get(board, 0) + n
    return kit(counts, a.servers + b.servers)


def servers_required(slots: int, chips: int, cpu: Fraction, spec: ServerSpec) -> int:
    """max(ceil(slots / slots_per_server), ceil(cpu / usable_cores)) (К7)."""
    if spec.chips_per_server is not None:
        by_slots = ceil(chips / spec.chips_per_server)
    else:
        by_slots = ceil(Fraction(slots, spec.slots))
    return max(by_slots, ceil(cpu / spec.cores))


def combos(types: list[Board], need: int) -> Iterator[dict[str, int]]:
    """Count vectors covering `need` chips; the last type tops up the rest (bounded search)."""
    order = sorted(types, key=lambda b: (-b.chips, b.id))
    *head, last = order
    seen = [0]

    def rec(i: int, rem: int, acc: dict[str, int]) -> Iterator[dict[str, int]]:
        if i == len(head):
            seen[0] += 1
            if seen[0] > SEARCH_BUDGET:
                raise limit_error()
            yield acc | {last.id: math.ceil(rem / last.chips) if rem > 0 else 0}
            return
        board = head[i]
        for n in range(math.ceil(rem / board.chips) + 1 if rem > 0 else 1):
            yield from rec(i + 1, max(0, rem - n * board.chips), acc | {board.id: n})

    yield from rec(0, need, {})


@dataclass(frozen=True)
class Plan:
    selection: Literal["priced_optimum", "technical_only", "unresolved"]
    purchase: Kit | None
    board_capex: Q
    server_capex: Q


UNRESOLVED = Plan("unresolved", None, None, None)


def select(
    chips: int | None,
    cpu: Q,
    before: Kit | None,
    allowed: list[Board],
    boards: dict[str, Board],
    spec: ServerSpec,
) -> Plan:
    """The cheapest priced purchase on top of `before`, else the technical one (К7)."""
    if chips is None or cpu is None or before is None:
        return UNRESOLVED
    need = max(0, chips - kit_chips(before, boards))
    ids = sorted(b.id for b in allowed)

    def outcome(counts: dict[str, int]) -> tuple[Kit, int, int]:
        after = kit_add(before, kit(counts, 0))
        servers = servers_required(kit_slots(after, boards), kit_chips(after, boards), cpu, spec)
        buy = max(0, servers - before.servers)
        return kit(counts, buy), buy, kit_chips(after, boards) - chips

    def lex(counts: dict[str, int]) -> tuple[int, ...]:
        return tuple(-counts.get(i, 0) for i in ids)

    def priced_key(counts: dict[str, int]) -> tuple[Any, ...]:
        _, buy, extra = outcome(counts)
        cost = sum((n * cast(Fraction, boards[b].price) for b, n in counts.items()), Fraction(0))
        if spec.price is None:  # the unknown part is minimised first, never priced as 0
            return (buy, cost, sum(counts.values()), extra, lex(counts))
        return (cost + buy * spec.price, buy, sum(counts.values()), extra, lex(counts))

    def technical_key(counts: dict[str, int]) -> tuple[Any, ...]:
        _, buy, extra = outcome(counts)
        return (sum(counts.values()), extra, buy, lex(counts))

    def best(types: list[Board], key: Callable[[dict[str, int]], tuple[Any, ...]]) -> Kit | None:
        if need == 0:
            return outcome({})[0]
        if not types:
            return None
        return outcome(min(combos(types, need), key=key))[0]

    selection: Literal["priced_optimum", "technical_only"] = "priced_optimum"
    purchase = best([b for b in allowed if b.price is not None], priced_key)
    if purchase is None:
        selection, purchase = "technical_only", best(allowed, technical_key)
    if purchase is None:
        return UNRESOLVED
    board_capex = total([mul(Fraction(n), boards[b].price) for b, n in purchase.boards])
    server_capex = mul(Fraction(purchase.servers), spec.price)
    return Plan(selection, purchase, board_capex, server_capex)


def state(k: Kit | None, boards: dict[str, Board], spec: ServerSpec) -> EquipmentState | None:
    if k is None:
        return None
    return EquipmentState(
        boards=[BoardCount(board_id=b, count=n) for b, n in k.boards],
        chips=kit_chips(k, boards),
        servers=k.servers,
        used_slots=kit_slots(k, boards),
        power_w=num(kit_power(k, boards, spec)),
    )


def electricity(power_w: Q, hours: Fraction, tariff: Q) -> Q:
    """(W / 1000) × hours × ₽/kWh; 8760 is a 24/7 year (К8)."""
    return mul(None if power_w is None else power_w / 1000, hours, tariff)


# --- evidence (К5) ------------------------------------------------------------------------
def _numeric(annotation: Any) -> bool:
    args = get_args(annotation) or (annotation,)
    return bool not in args and any(a in (int, float) for a in args)


def walk_inputs(obj: BaseModel, prefix: str = "") -> Iterator[tuple[str, float | int | None]]:
    """Every numeric input of a request: path and value. Ids, flags and texts are not inputs."""
    for name, info in type(obj).model_fields.items():
        value = getattr(obj, name)
        path = f"{prefix}{name}"
        if isinstance(value, BaseModel):
            yield from walk_inputs(value, path + ".")
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, BaseModel):
                    yield from walk_inputs(item, f"{path}.{i}.")
        elif isinstance(value, dict):
            for key, item in value.items():
                if item is None or isinstance(item, int | float):
                    yield f"{path}.{key}", item
        elif isinstance(value, bool):
            continue
        elif value is None and _numeric(info.annotation):
            yield path, None
        elif isinstance(value, int | float):
            yield path, value


def _glob(path: str) -> str:
    return ".".join("*" if part.isdigit() else part for part in path.split("."))


def _lookup(data: Any, path: str) -> Any:
    for part in path.split("."):
        if isinstance(data, list) and part.isdigit() and int(part) < len(data):
            data = data[int(part)]
        elif isinstance(data, dict) and part in data:
            data = data[part]
        else:
            return KeyError
    return data


class Evidence:
    """`NumericEvidence` of the inputs and of every derived number, by stable key (К5)."""

    def __init__(self, catalog: Catalog) -> None:
        self.catalog = catalog
        self.items: dict[str, NumericEvidence] = {}

    def add(
        self,
        key: str,
        value: Q | float | int,
        unit: str,
        status: NumberStatus,
        sources: list[str],
        formula: str | None = None,
        depends: tuple[str, ...] | list[str] = (),
        title: str | None = None,
    ) -> None:
        if isinstance(value, Fraction):
            shown = rub(value) if unit.startswith("₽") else num(value)
        else:
            shown = None if value is None else float(value)
        if shown is None and status != "not_applicable":
            status = "missing"
        self.items[key] = NumericEvidence(
            key=key,
            title=title or key,
            value=shown,
            unit=unit,
            status=status,
            source_ids=sorted(set(sources)),
            formula=formula,
            depends_on=list(depends),
            reason=texts.CALC2_MISSING_VALUE if shown is None and status == "missing" else None,
        )

    def derived(
        self, key: str, value: Q, unit: str, formula: str, depends: tuple[str, ...] | list[str]
    ) -> None:
        sources = {s for d in depends if d in self.items for s in self.items[d].source_ids}
        self.add(
            key, value, unit, "derived", sorted(sources) or ["team_defaults"], formula, depends
        )

    def value(self, key: str) -> Q:
        item = self.items.get(key)
        return None if item is None or item.value is None else fr(item.value)

    def request(self, req: BaseModel, reference: dict[str, Any]) -> None:
        """An input equal to the defaults (or the preset) keeps their source; else user_input."""
        for path, value in walk_inputs(req):
            spec = self.catalog.inputs.get(path) or self.catalog.inputs.get(_glob(path))
            title, unit = (spec.title, spec.unit) if spec else (path, "значение")
            sources = list(spec.source_ids) if spec else ["team_defaults"]
            if value is None:
                self.add(f"request.{path}", None, unit, "missing", sources, title=title)
            elif _lookup(reference, path) == value:
                self.add(f"request.{path}", value, unit, "assumed", sources, title=title)
            else:
                self.add(f"request.{path}", value, unit, "known", ["user_input"], title=title)


# --- the v2 engine ------------------------------------------------------------------------
@dataclass(frozen=True)
class Scope:
    mode: CalcMode
    current: list[ResolvedGroup]  # ids already prefixed
    added: list[ResolvedGroup]
    installed: Kit | None  # scale: the provided inventory; None — estimate it
    missing: tuple[Notice, ...] = ()  # notices of the system profiles
    warnings: tuple[Notice, ...] = ()


def board_table(req: Request, catalog: Catalog) -> dict[str, Board]:
    overrides = req.hardware.board_price_overrides
    return {
        b.id: Board(
            id=b.id,
            chips=b.chips,
            slots=b.slots,
            power=opt(b.power_w),
            price=opt(overrides[b.id]) if b.id in overrides else opt(b.price_rub),
        )
        for b in catalog.boards.values()
    }


def server_spec(req: Request) -> ServerSpec:
    s = req.hardware.server
    return ServerSpec(s.slots, fr(s.usable_cpu_cores), opt(s.price_rub), opt(s.power_w))


@dataclass(frozen=True)
class StepCalc:
    chips: int | None
    plan: Plan
    reason: str


def greenfield(
    chips: int | None, cpu: Q, allowed: list[Board], boards: dict[str, Board], spec: ServerSpec
) -> StepCalc:
    """A new installation for a step or a curve point; a too big one stays unresolved."""
    if chips is None:
        return StepCalc(None, UNRESOLVED, texts.CALC2_STEP_UNKNOWN)
    if chips > MAX_CHIPS:
        return StepCalc(None, UNRESOLVED, texts.CALC2_STEP_LIMIT)
    try:
        plan = select(chips, cpu, EMPTY_KIT, allowed, boards, spec)
    except Conflict:
        return StepCalc(None, UNRESOLVED, texts.CALC2_STEP_LIMIT)
    priced = plan.selection == "priced_optimum" and plan.server_capex is not None
    return StepCalc(
        chips, plan, texts.CALC2_STEP_GREENFIELD if priced else texts.CALC2_STEP_UNPRICED
    )


class Notes:
    def __init__(self, missing: tuple[Notice, ...], warnings: tuple[Notice, ...]) -> None:
        self.missing, self.warnings = list(missing), list(warnings)

    def miss(self, code: str, field: str | None, what: str) -> None:
        if not any(m.code == code and m.field == field for m in self.missing):
            message = texts.CALC2_MISSING[code].format(what=what)
            self.missing.append(Notice(code=code, field=field, message=message))

    def warn(self, code: str, field: str | None) -> None:
        if not any(w.code == code for w in self.warnings):
            self.warnings.append(Notice(code=code, field=field, message=texts.CALC2_WARNINGS[code]))


LOAD_DEPENDS = (
    "request.load.activity_share",
    "request.load.target_fps",
    "request.load.surge_fps",
    "request.load.idle_check_s",
    "request.load.priority_cameras_reserve",
    "request.load.reference_chip_fps",
    "request.load.capacity_derate",
)


def calculate(
    req: Request,
    scope: Scope,
    catalog: Catalog,
    reference: dict[str, Any],
    events_per_camera_day: float | None,
) -> ResultV2:
    """ResultV2 of a validated request whose camera profiles are resolved into `scope`."""
    load_in, costs = req.load, req.costs
    pol = policy(load_in)
    boards = board_table(req, catalog)
    spec = server_spec(req)
    allowed = [boards[b] for b in req.hardware.allowed_board_ids]
    current = to_groups(scope.current, load_in, catalog)
    groups = current + to_groups(scope.added, load_in, catalog)
    stride = load_in.detector_stride
    ev = Evidence(catalog)
    ev.request(req, reference)
    notes = Notes(scope.missing, scope.warnings)

    used_models = sorted({m for g in groups for m, _ in g.weights})
    for model_id in used_models:
        model, own = catalog.models[model_id], model_id in load_in.model_cost_overrides
        weight = model_weight(model_id, load_in, catalog)
        ev.add(
            f"catalog.models.{model_id}.work_units",
            weight,
            "экв.ед.",
            "known" if own else "assumed",
            ["user_input"] if own else model.source_ids,
            title=model.title,
        )
        if weight is None:
            notes.miss("MODEL_COST_UNKNOWN", f"load.model_cost_overrides.{model_id}", model_id)
    for b in boards.values():
        offer = catalog.boards[b.id]
        for attr, value, unit in (
            ("chips", b.chips, "шт."),
            ("slots", b.slots, "шт."),
            ("power_w", b.power, "Вт"),
            ("price_rub", b.price, "₽"),
        ):
            own = attr == "price_rub" and b.id in req.hardware.board_price_overrides
            ev.add(
                f"catalog.boards.{b.id}.{attr}",
                value,
                unit,
                "known" if own else "assumed",
                ["user_input"] if own else offer.source_ids,
                title=f"{offer.title}: {attr}",
            )
    depends = [*LOAD_DEPENDS, *(f"catalog.models.{m}.work_units" for m in used_models)]

    total_load = load_of(groups, pol, stride)
    if total_load.chips is not None and total_load.chips > MAX_CHIPS:
        raise limit_error()
    if total_load.chips is None and not notes.missing:
        notes.miss("MODEL_COST_UNKNOWN", "load.model_cost_overrides", "профиля")
    n_total = total_load.cameras
    n_scope = sum(g.cameras for g in groups) - sum(g.cameras for g in current)

    # Steps: the greenfield need of all cameras under one assumption at a time (К6).
    naive_units = full_units(groups, pol)
    override = load_in.platform_capacity_override_fps
    platform = fr(override) if override is not None else catalog.platform_fps
    naive_cpu = None if naive_units is None else cpu_cores(naive_units, n_total, pol)
    naive_chips = None if naive_units is None else ceil(naive_units / platform)
    dedicated = None if naive_units is None else ceil(naive_units / pol.capacity)
    scenario = scenario_units(groups, pol)
    scenario_cpu = None if scenario is None else cpu_cores(scenario, n_total, pol)
    pool = load_of(groups, pol, 1)
    rows: list[tuple[str, StepCalc | None]] = [
        ("naive", greenfield(naive_chips, naive_cpu, allowed, boards, spec)),
        ("dedicated_capacity", greenfield(dedicated, naive_cpu, allowed, boards, spec)),
        (
            "scenario_models",
            greenfield(
                None if scenario is None else ceil(scenario / pol.capacity),
                scenario_cpu,
                allowed,
                boards,
                spec,
            ),
        ),
        ("activity_pool", greenfield(pool.chips, pool.cpu, allowed, boards, spec)),
    ]
    tracked = load_of(groups, pol, 2) if catalog.tracker_available else None
    rows.append(
        (
            "tracker",
            None
            if tracked is None
            else greenfield(tracked.chips, tracked.cpu, allowed, boards, spec),
        )
    )

    # Hardware: before (inventory), purchase, after (К7).
    current_load = load_of(current, pol, stride)
    basis: Literal["none", "provided", "estimated"] = "none"
    before: Kit | None = EMPTY_KIT
    if scope.mode == "scale":
        if scope.installed is not None:
            before, basis = scope.installed, "provided"
        else:
            basis = "estimated"
            before = select(
                current_load.chips, current_load.cpu, EMPTY_KIT, allowed, boards, spec
            ).purchase
            notes.warn("INVENTORY_ESTIMATED", "installed")
        if before is not None and current_load.chips is not None and current_load.cpu is not None:
            servers = servers_required(
                kit_slots(before, boards), kit_chips(before, boards), current_load.cpu, spec
            )
            if kit_chips(before, boards) < current_load.chips or before.servers < servers:
                notes.warn("EXISTING_CAPACITY_SHORTFALL", "installed")
    plan = select(total_load.chips, total_load.cpu, before, allowed, boards, spec)
    after = None if plan.purchase is None or before is None else kit_add(before, plan.purchase)
    if plan.purchase is not None:
        for bid, n in plan.purchase.boards:
            if boards[bid].price is None:
                notes.miss("BOARD_PRICE_UNKNOWN", f"hardware.board_price_overrides.{bid}", bid)
            if boards[bid].power is None:
                notes.miss("POWER_UNKNOWN", f"catalog.boards.{bid}.power_w", bid)
            ev.derived(
                f"hardware.purchase.{bid}.count",
                Fraction(n),
                "шт.",
                "max(0, required_chips − installed_chips)",
                ["load.required_chips"],
            )
        if plan.purchase.servers and spec.price is None:
            notes.miss("SERVER_PRICE_UNKNOWN", "hardware.server.price_rub", "")
        if plan.purchase.servers and spec.power is None:
            notes.miss("POWER_UNKNOWN", "hardware.server.power_w", "сервера")
        ev.derived(
            "hardware.purchase.servers",
            Fraction(plan.purchase.servers),
            "шт.",
            "max(0, required_servers − installed_servers)",
            ["load.required_cpu_cores"],
        )

    load_res = LoadResult(
        cameras=n_total,
        active_p95=total_load.a95,
        priority_cameras_effective=total_load.q,
        peak_units_s=num(total_load.peak),
        surge_units_s=num(total_load.surge),
        required_units_s=num(total_load.units),
        effective_chip_units_s=cast(float, num(pol.capacity)),
        required_chips=total_load.chips,
        required_cpu_cores=num(total_load.cpu),
        naive_chips=naive_chips,
        basis=load_in.peak_mode,
    )
    for key, value in load_res.model_dump(exclude={"basis"}).items():
        ev.derived(f"load.{key}", opt(value), "значение", "Формулы К6", depends)
    bought = [k for k in ev.items if k.startswith("hardware.purchase.") and k.endswith(".count")]
    ev.derived(
        "hardware.board_capex_rub", plan.board_capex, "₽", "Σ purchase.count × board.price", bought
    )
    ev.derived(
        "hardware.server_capex_rub",
        plan.server_capex,
        "₽",
        "purchase.servers × server.price",
        ["hardware.purchase.servers", "request.hardware.server.price_rub"],
    )

    # In scale only the added equipment is paid for (К7): the purchase power.
    tariff = opt(costs.electricity_rub_kwh)
    power = None if plan.purchase is None else kit_power(plan.purchase, boards, spec)
    elec = (
        None
        if plan.purchase is None
        else electricity(power, fr(costs.operating_hours_year), tariff)
    )
    if plan.purchase is not None and elec is None and tariff is None:
        notes.miss("COST_INPUT_MISSING", "costs.electricity_rub_kwh", "тариф на электроэнергию")
    ev.derived(
        "cost.electricity_rub_year",
        elec,
        "₽/год",
        "power_scope_w/1000 × hours × tariff",
        ["request.costs.operating_hours_year", "request.costs.electricity_rub_kwh"],
    )

    empty = n_total == 0
    tiers = []
    for t in TIERS:
        calc = tier_calc(t, req, n_scope, plan, elec, ev, notes)
        tiers.append(
            tier_result(calc, n_scope, empty, plan, boards, fr(costs.support_share_year), ev)
        )

    steps = []
    for step_id, step in rows:
        title = texts.CALC2_STEPS[step_id]
        if step is None:
            steps.append(
                StepV2(
                    id=step_id,
                    title=title,
                    available=False,
                    chips=None,
                    servers=None,
                    equipment_capex_rub=None,
                    reason=texts.CALC2_STEP_TRACKER_OFF,
                )
            )
            continue
        p = step.plan
        capex = None if p.purchase is None else total([p.board_capex, p.server_capex])
        steps.append(
            StepV2(
                id=step_id,
                title=title,
                available=True,
                chips=step.chips,
                servers=None if p.purchase is None else p.purchase.servers,
                equipment_capex_rub=rub(capex),
                reason=step.reason,
            )
        )
        ev.derived(
            f"steps.{step_id}.chips", opt(step.chips), "шт.", f"К6: ступень {step_id}", depends
        )
        ev.derived(
            f"steps.{step_id}.equipment_capex_rub",
            capex,
            "₽",
            "boards + servers, greenfield",
            [f"steps.{step_id}.chips", "request.hardware.server.price_rub"],
        )

    curve = scale_curve(groups, pol, stride, req, n_scope, allowed, boards, spec, ev)
    if not groups and not empty:
        notes.missing.append(
            Notice(
                code="CURVE_PROFILE_MISSING", field=None, message="Нет камер для кривой масштаба."
            )
        )

    shifts = req.site.operators * req.site.shifts_per_day
    events = None
    if events_per_camera_day is not None and shifts:
        events = fr(events_per_camera_day) * n_scope / shifts

    notes.warn("MODELED_POLICY_NOT_DEPLOYED", "load")
    if load_in.peak_mode == "independent_p95":
        notes.warn("INDEPENDENT_ACTIVITY_ASSUMPTION", "load.activity_share")
    if total_load.q < n_total:
        notes.warn("PRIORITY_RESERVE_LIMIT", "load.priority_cameras_reserve")
    if any(ev.items[f"catalog.models.{m}.work_units"].status == "assumed" for m in used_models):
        notes.warn("MODEL_WEIGHT_ASSUMED", "load.model_cost_overrides")
    if ev.items["request.load.reference_chip_fps"].status == "assumed":
        notes.warn("VENDOR_CAPACITY_NOT_APP_MEASUREMENT", "load.reference_chip_fps")
    notes.warn("PLATFORM_QUEUE_NOT_CHIP", "load.platform_capacity_override_fps")
    if load_in.activity_measurement_id is not None:
        notes.warn("DEMO_ACTIVITY_BIASED", "load.activity_measurement_id")

    used = {s for e in ev.items.values() if e.value is not None for s in e.source_ids}
    used |= {s for m in used_models for s in catalog.models[m].source_ids}
    if override is None:
        used |= set(catalog.platform_source_ids)
    sources = [catalog.sources[s] for s in sorted(used) if s in catalog.sources]
    if any(s.verification == "pending_primary" for s in sources):
        notes.warn("SOURCE_PENDING_PRIMARY", None)
    if req.benefits.severe_injury_cost_rub is None:
        notes.warn("SEVERE_COST_REQUIRED", "benefits.severe_injury_cost_rub")

    status: ResultStatus = "ready"
    if empty:
        status = "empty"
    elif notes.missing:
        status = "partial"
    elif (
        basis == "estimated"
        or any(e.status == "assumed" for e in ev.items.values())
        or any(s.verification in ("pending_primary", "cached_primary") for s in sources)
    ):
        status = "estimated"
    spare = None
    if after is not None and total_load.chips is not None:
        spare = kit_chips(after, boards) - total_load.chips
    return ResultV2(
        format="v2",
        contract_version="2.0.0",
        formula_version="argus-calc-2.0",
        mode=scope.mode,
        status=status,
        cost_scope="whole_project" if scope.mode == "rollout" else "incremental",
        horizon_years=3,
        resolved=ResolvedV2(
            current=profile(scope.current),
            added=profile(scope.added),
            total=profile([*scope.current, *scope.added]),
            input=req,
        ),
        load=load_res,
        hardware=HardwareResult(
            selection=plan.selection,
            inventory_basis=basis,
            before=state(before, boards, spec),
            purchase=state(plan.purchase, boards, spec),
            after=state(after, boards, spec),
            required_before_chips=current_load.chips if scope.mode == "scale" else 0,
            required_after_chips=total_load.chips,
            spare_chips_after=spare,
            board_capex_rub=rub(plan.board_capex),
            server_capex_rub=rub(plan.server_capex),
            note=texts.CALC2_HW_NOTE[plan.selection],
        ),
        tiers=tiers,
        steps=steps,
        scale_curve=curve,
        operator_events_per_shift=num(events),
        evidence=list(ev.items.values()),
        sources=sources,
        warnings=notes.warnings,
        missing=notes.missing,
    )


# --- money (К8) ---------------------------------------------------------------------------
@dataclass
class Line:
    id: str
    amount: Q
    depends: tuple[str, ...] = ()
    included: bool = True
    status: NumberStatus = "derived"
    evidence: str = ""


@dataclass
class TierCalc:
    tier: CalcTier
    capex: list[Line]
    opex: list[Line]
    benefits: list[Line]
    hours: Fraction

    @property
    def capex_total(self) -> Q:
        return total([line.amount for line in self.capex])

    @property
    def opex_total(self) -> Q:
        return total([line.amount for line in self.opex])

    @property
    def benefit_total(self) -> Q:
        return total([line.amount for line in self.benefits if line.included])


CAPEX_FIELDS = {
    "integration_fixed": "costs.integration_fixed_rub",
    "integration_cameras": "costs.integration_per_camera_rub",
    "physical_cameras": "costs.new_camera_unit_rub",
    "signals": "costs.signal_unit_rub",
    "speakers": "costs.speaker_per_workshop_rub",
    "max_cameras": "costs.new_camera_unit_rub",
}


def tier_calc(
    tier: CalcTier, req: Request, n_scope: int, plan: Plan, elec: Q, ev: Evidence, notes: Notes
) -> TierCalc:
    """CAPEX lines of a tier (base ⊂ extended ⊂ max), support, electricity and benefits."""
    costs, t = req.costs, f"tier.{tier}"
    n, ncc = Fraction(n_scope), Fraction(costs.new_camera_count)
    camera = opt(costs.new_camera_unit_rub)
    bought = plan.purchase is not None
    lines = [
        Line("boards", plan.board_capex if bought else None, ("hardware.board_capex_rub",)),
        Line("servers", plan.server_capex if bought else None, ("hardware.server_capex_rub",)),
        Line(
            "integration_fixed",
            opt(costs.integration_fixed_rub) if n_scope else Fraction(0),
            ("request.costs.integration_fixed_rub",),
        ),
        Line(
            "integration_cameras",
            mul(n, opt(costs.integration_per_camera_rub)),
            ("request.costs.integration_per_camera_rub",),
        ),
        Line(
            "physical_cameras",
            mul(ncc, camera),
            ("request.costs.new_camera_count", "request.costs.new_camera_unit_rub"),
        ),
    ]
    if tier != "base":
        lines.append(
            Line(
                "signals",
                mul(n, fr(costs.signal_zones_per_camera), opt(costs.signal_unit_rub)),
                ("request.costs.signal_zones_per_camera", "request.costs.signal_unit_rub"),
            )
        )
    if tier == "max":
        extra = min(n - ncc, Fraction(ceil(n * fr(costs.max_additional_camera_share))))
        workshops = Fraction(req.site.workshops) if n_scope else Fraction(0)
        lines.append(
            Line(
                "speakers",
                mul(workshops, opt(costs.speaker_per_workshop_rub)),
                ("request.site.workshops", "request.costs.speaker_per_workshop_rub"),
            )
        )
        lines.append(
            Line(
                "max_cameras",
                mul(extra, camera),
                ("request.costs.max_additional_camera_share", "request.costs.new_camera_unit_rub"),
            )
        )
    for line in lines:
        line.evidence = f"{t}.capex.{line.id}"
        line.status = "derived" if line.amount is not None else "missing"
        ev.derived(
            line.evidence, line.amount, "₽", f"К8: {texts.CALC2_CAPEX_LINES[line.id]}", line.depends
        )
        if line.amount is None and line.id in CAPEX_FIELDS:
            notes.miss(
                "COST_INPUT_MISSING", CAPEX_FIELDS[line.id], texts.CALC2_CAPEX_LINES[line.id]
            )
    calc = TierCalc(tier, lines, [], [], Fraction(0))
    ev.derived(
        f"{t}.capex_rub",
        calc.capex_total,
        "₽",
        "sum(capex_lines)",
        [line.evidence for line in lines],
    )
    support = mul(calc.capex_total, fr(costs.support_share_year))
    ev.derived(
        f"{t}.opex.support",
        support,
        "₽/год",
        "capex × support_share_year",
        [f"{t}.capex_rub", "request.costs.support_share_year"],
    )
    calc.opex = [
        Line(
            "support",
            support,
            status="derived" if support is not None else "missing",
            evidence=f"{t}.opex.support",
        ),
        Line(
            "electricity",
            elec,
            status="derived" if elec is not None else "missing",
            evidence="cost.electricity_rub_year",
        ),
    ]
    ev.derived(
        f"{t}.opex_rub_year",
        calc.opex_total,
        "₽/год",
        "support + electricity",
        [f"{t}.opex.support", "cost.electricity_rub_year"],
    )
    calc.benefits = benefit_lines(tier, req, n_scope, ev, notes)
    ev.derived(
        f"{t}.gross_benefit_rub_year",
        calc.benefit_total,
        "₽/год",
        "sum(included benefits)",
        [b.evidence for b in calc.benefits],
    )
    if n_scope:
        calc.hours = sum((fr(row.hours_saved_year) for row in req.benefits.labor.rows), Fraction(0))
    return calc


def benefit_lines(
    tier: CalcTier, req: Request, n_scope: int, ev: Evidence, notes: Notes
) -> list[Line]:
    """Benefits of the enterprise, each with its own switch; unknown is null, not 0 (К8)."""
    ben, t = req.benefits, f"tier.{tier}"
    out: list[Line] = []

    def line(
        lid: str,
        enabled: bool,
        amount: Q,
        formula: str,
        depends: tuple[str, ...],
        needs: list[tuple[str, Q]],
    ) -> None:
        key = f"{t}.benefit.{lid}"
        if not enabled or n_scope == 0:  # off, or no added area: no added benefit
            out.append(
                Line(lid, Fraction(0), included=False, status="not_applicable", evidence=key)
            )
            ev.add(key, Fraction(0), "₽/год", "not_applicable", ["user_input"])
            return
        for field, value in needs if amount is None else []:
            if value is None:
                notes.miss("BENEFIT_INPUT_MISSING", field, field)
        out.append(
            Line(lid, amount, status="derived" if amount is not None else "missing", evidence=key)
        )
        ev.derived(key, amount, "₽/год", formula, depends)

    inj = ben.injuries
    injured = opt(inj.annual_injured_workers)
    if injured is None and inj.rate_per_1000 is not None:
        injured = Fraction(req.site.workers) * fr(inj.rate_per_1000) / 1000
    ev.derived(
        "benefits.injured_workers_year",
        injured,
        "чел./год",
        "annual_injured_workers, иначе workers × rate_per_1000 / 1000",
        [
            "request.site.workers",
            "request.benefits.injuries.rate_per_1000",
            "request.benefits.injuries.annual_injured_workers",
        ],
    )
    line(
        "injuries",
        inj.enabled,
        mul(injured, opt(inj.cost_per_injured_worker_rub), fr(getattr(inj.reduction, tier))),
        "injured_year × direct_cost × reduction",
        (
            "benefits.injured_workers_year",
            "request.benefits.injuries.cost_per_injured_worker_rub",
            f"request.benefits.injuries.reduction.{tier}",
        ),
        [
            ("benefits.injuries.rate_per_1000", injured),
            ("benefits.injuries.cost_per_injured_worker_rub", opt(inj.cost_per_injured_worker_rub)),
        ],
    )
    dt = ben.downtime
    line(
        "downtime",
        dt.enabled,
        mul(
            opt(dt.events_year),
            opt(dt.days_per_event),
            opt(dt.day_cost_rub),
            fr(getattr(dt.reduction, tier)),
        ),
        "events_year × days_per_event × day_cost × reduction",
        (
            "request.benefits.downtime.events_year",
            "request.benefits.downtime.days_per_event",
            "request.benefits.downtime.day_cost_rub",
            f"request.benefits.downtime.reduction.{tier}",
        ),
        [
            ("benefits.downtime.events_year", opt(dt.events_year)),
            ("benefits.downtime.days_per_event", opt(dt.days_per_event)),
            ("benefits.downtime.day_cost_rub", opt(dt.day_cost_rub)),
        ],
    )
    items = ben.fines.items
    fines = [
        mul(fr(i.inspection_probability_year), opt(i.amount_rub), fr(getattr(i.reduction, tier)))
        for i in items
    ]
    line(
        "fines",
        ben.fines.enabled,
        total(fines),
        "Σ inspection_probability × fine × reduction",
        tuple(f"request.benefits.fines.items.{k}.amount_rub" for k in range(len(items))),
        [(f"benefits.fines.items.{k}.amount_rub", part) for k, part in enumerate(fines)],
    )
    sfr = ben.sfr_discount
    line(
        "sfr_discount",
        sfr.enabled,
        mul(opt(sfr.payroll_rub_year), opt(sfr.tariff_share), opt(sfr.additional_discount_share)),
        "payroll × tariff × additional_discount",
        (
            "request.benefits.sfr_discount.payroll_rub_year",
            "request.benefits.sfr_discount.tariff_share",
            "request.benefits.sfr_discount.additional_discount_share",
        ),
        [
            ("benefits.sfr_discount.payroll_rub_year", opt(sfr.payroll_rub_year)),
            ("benefits.sfr_discount.tariff_share", opt(sfr.tariff_share)),
            ("benefits.sfr_discount.additional_discount_share", opt(sfr.additional_discount_share)),
        ],
    )
    rows = ben.labor.rows
    labor = [mul(fr(row.hours_saved_year), opt(row.hour_cost_rub)) for row in rows]
    line(
        "labor",
        ben.labor.monetize,
        total(labor),
        "Σ hours_saved × hour_cost",
        tuple(f"request.benefits.labor.rows.{k}.hour_cost_rub" for k in range(len(rows))),
        [(f"benefits.labor.rows.{k}.hour_cost_rub", part) for k, part in enumerate(labor)],
    )
    return out


def tier_result(
    calc: TierCalc,
    n_scope: int,
    empty: bool,
    plan: Plan,
    boards: dict[str, Board],
    support_share: Fraction,
    ev: Evidence,
) -> TierResultV2:
    t = f"tier.{calc.tier}"
    capex, opex, benefit = calc.capex_total, calc.opex_total, calc.benefit_total
    net = None if benefit is None or opex is None else benefit - opex
    tco = None if capex is None or opex is None else capex + HORIZON_YEARS * opex
    balance = None if benefit is None or tco is None else HORIZON_YEARS * benefit - tco
    per_camera = None if tco is None or n_scope == 0 else tco / (n_scope * MONTHS)
    ev.derived(
        f"{t}.net_benefit_rub_year",
        net,
        "₽/год",
        "gross − opex",
        [f"{t}.gross_benefit_rub_year", f"{t}.opex_rub_year"],
    )
    ev.derived(
        f"{t}.tco_3_year_rub",
        tco,
        "₽",
        "capex + 3 × opex",
        [f"{t}.capex_rub", f"{t}.opex_rub_year"],
    )
    ev.derived(
        f"{t}.net_balance_3_year_rub",
        balance,
        "₽",
        "3 × gross − TCO3",
        [f"{t}.gross_benefit_rub_year", f"{t}.tco_3_year_rub"],
    )
    ev.derived(
        f"{t}.rub_per_camera_month",
        per_camera,
        "₽/камера/мес",
        "TCO3 / (Nscope × 36)",
        [f"{t}.tco_3_year_rub"],
    )
    b_other = total([b.amount for b in calc.benefits if b.included and b.id != "injuries"])
    severe_cost = ev.value("request.benefits.severe_injury_cost_rub")

    def money(lines: list[Line], titles: dict[str, str]) -> list[MoneyLine]:
        return [
            MoneyLine(
                id=line.id,
                title=titles[line.id],
                amount_rub=rub(line.amount),
                included=line.included,
                status=line.status,
                evidence_keys=[line.evidence],
            )
            for line in lines
        ]

    return TierResultV2(
        tier=calc.tier,
        title=texts.CALC_TIER_TITLES[calc.tier],
        capex_rub=rub(capex),
        opex_rub_year=rub(opex),
        gross_benefit_rub_year=rub(benefit),
        net_benefit_rub_year=rub(net),
        tco_3_year_rub=rub(tco),
        net_balance_3_year_rub=rub(balance),
        rub_per_camera_month=rub(per_camera),
        camera_denominator=n_scope,
        labor_hours_year=cast(float, num(calc.hours)),
        capex_lines=money(calc.capex, texts.CALC2_CAPEX_LINES),
        opex_lines=money(calc.opex, texts.CALC2_OPEX_LINES),
        benefit_lines=money(calc.benefits, texts.CALC2_BENEFIT_LINES),
        payback=payback_of(capex, opex, benefit, empty),
        severe_threshold=severe_threshold(tco, b_other, severe_cost, empty),
        board_price_threshold=price_threshold(calc, plan, boards, support_share, empty, ev),
    )


def payback_of(capex: Q, opex: Q, benefit: Q, empty: bool) -> PaybackResult:
    """12·capex / net only for a positive net; a term over 36 months stays a number (К8)."""
    text = texts.CALC2_PAYBACK

    def out(status: str, months: Q, within: bool | None, what: str = "") -> PaybackResult:
        return PaybackResult(
            status=status,
            months=num(months),
            within_horizon=within,
            reason=text[status].format(what=what),
        )

    if empty:
        return out("not_applicable", None, None)
    if capex is None or opex is None or benefit is None:
        what = (
            "стоимость проекта"
            if capex is None
            else "годовые расходы"
            if opex is None
            else "выгода"
        )
        return out("insufficient_data", None, None, what)
    net = benefit - opex
    if capex == 0 and opex == 0 and benefit == 0:
        return out("not_applicable", None, None)
    if net <= 0:
        return out("no_positive_effect", None, False)
    if capex == 0:
        return out("no_initial_investment", Fraction(0), True)
    months = 12 * capex / net
    within = months <= MONTHS
    return out("within_horizon" if within else "after_horizon", months, within)


def severe_threshold(tco: Q, b_other: Q, severe_cost: Q, empty: bool) -> SevereThreshold:
    """Severe cases to prevent in 3 years in place of the injury line, not on top of it (К8)."""
    text = texts.CALC2_SEVERE

    def out(status: str, expected: Q, gap: Q, reason: str) -> SevereThreshold:
        return SevereThreshold(
            status=status,
            expected_prevented_cases=num(expected),
            whole_prevented_cases=None if expected is None else ceil(expected),
            uncovered_cost_rub=rub(gap),
            reason=text[reason],
        )

    if empty:
        return out("not_applicable", None, None, "not_applicable")
    if tco is None or b_other is None:
        return out("needs_input", None, None, "needs_total")
    gap = max(Fraction(0), tco - HORIZON_YEARS * b_other)
    if gap == 0:
        return out("already_covered", Fraction(0), gap, "already_covered")
    if not severe_cost:
        return out("needs_input", None, gap, "needs_cost")
    return out("required", gap / severe_cost, gap, "required")


def price_threshold(
    calc: TierCalc,
    plan: Plan,
    boards: dict[str, Board],
    r: Fraction,
    empty: bool,
    ev: Evidence,
) -> PriceThreshold:
    """Pmax = [3(B − F)/(1 + 3r) − C_other] / q for one bought board type, kit fixed (К8)."""
    text, t = texts.CALC2_PRICE, f"tier.{calc.tier}"

    def out(
        status: str, board: str | None, q: int, pmax: float | None, current: Q, what: str = ""
    ) -> PriceThreshold:
        return PriceThreshold(
            status=status,
            board_id=board,
            boards_to_buy=q,
            max_unit_price_rub=pmax,
            current_unit_price_rub=rub(current),
            reason=text[status].format(board=board or "", what=what),
        )

    bought = [] if plan.purchase is None else list(plan.purchase.boards)
    if empty or not bought:
        return out("not_applicable", None, 0, None, None)
    unknown = [b for b, _ in bought if boards[b].price is None]
    if len(unknown) > 1:
        return out("insufficient_data", None, 0, None, None, "цены нескольких типов плат")
    var = (
        unknown[0]
        if unknown
        else min(
            bought, key=lambda item: (-item[1] * cast(Fraction, boards[item[0]].price), item[0])
        )[0]
    )
    q, current = dict(bought)[var], boards[var].price
    others = [mul(Fraction(n), boards[b].price) for b, n in bought if b != var]
    c_other = total([*(line.amount for line in calc.capex if line.id != "boards"), *others])
    benefit, elec = calc.benefit_total, calc.opex[1].amount
    if c_other is None or benefit is None or elec is None:
        what = "прочие вложения" if c_other is None else "выгода" if benefit is None else "тариф"
        return out("insufficient_data", var, q, None, current, what)
    raw = (HORIZON_YEARS * (benefit - elec) / (1 + HORIZON_YEARS * r) - c_other) / q
    ev.derived(
        f"{t}.board_price_threshold.c_other_rub",
        c_other,
        "₽",
        f"sum(capex_lines except variable {var} purchase)",
        [line.evidence for line in calc.capex if line.id != "boards"],
    )
    ev.derived(
        f"{t}.board_price_threshold.raw_unit_price_rub",
        raw,
        "₽",
        "(3 × (B − electricity) / (1 + 3r) − C_other) / q",
        [
            f"{t}.board_price_threshold.c_other_rub",
            f"{t}.gross_benefit_rub_year",
            "cost.electricity_rub_year",
            "request.costs.support_share_year",
        ],
    )
    if raw < 0:
        return out("free_still_insufficient", var, q, None, current)
    if current is not None and current <= raw:
        return out("already_within", var, q, rub_down(raw), current)
    return out("at_or_below", var, q, rub_down(raw), current)


def scale_curve(
    groups: list[Group],
    pol: Policy,
    stride: int,
    req: Request,
    n_scope: int,
    allowed: list[Board],
    boards: dict[str, Board],
    spec: ServerSpec,
    ev: Evidence,
) -> ScaleCurve:
    """Greenfield base TCO per camera for 5…500 cameras of the same mix (К8)."""
    costs = req.costs
    share = Fraction(costs.new_camera_count, n_scope) if n_scope else Fraction(0)
    points = []
    for n in CURVE_POINTS:
        step = StepCalc(None, UNRESOLVED, "")
        if groups:
            lp = load_of(scaled(groups, n), pol, stride)
            step = greenfield(lp.chips, lp.cpu, allowed, boards, spec)
        p = step.plan
        tco = per = None
        if p.purchase is not None:
            cameras = min(Fraction(n), Fraction(ceil(n * share)))
            capex = total(
                [
                    p.board_capex,
                    p.server_capex,
                    opt(costs.integration_fixed_rub),
                    mul(Fraction(n), opt(costs.integration_per_camera_rub)),
                    mul(cameras, opt(costs.new_camera_unit_rub)),
                ]
            )
            elec = electricity(
                kit_power(p.purchase, boards, spec),
                fr(costs.operating_hours_year),
                opt(costs.electricity_rub_kwh),
            )
            opex = total([mul(capex, fr(costs.support_share_year)), elec])
            tco = None if capex is None or opex is None else capex + HORIZON_YEARS * opex
            per = None if tco is None else tco / (n * MONTHS)
            ev.derived(
                f"curve.{n}.tco_3_year_rub",
                tco,
                "₽",
                "greenfield base: C + 3O",
                ["request.hardware.server.price_rub", "request.costs.support_share_year"],
            )
            ev.derived(
                f"curve.{n}.rub_per_camera_month",
                per,
                "₽/камера/мес",
                "TCO3 / (N × 36)",
                [f"curve.{n}.tco_3_year_rub"],
            )
        points.append(
            CurvePoint(
                cameras=n,
                chips=step.chips,
                servers=None if p.purchase is None else p.purchase.servers,
                tco_3_year_rub=rub(tco),
                rub_per_camera_month=rub(per),
            )
        )
    return ScaleCurve(
        scope="greenfield_reference", tier="base", points=points, note=texts.CALC2_CURVE_NOTE
    )


# --- legacy 1.1.0 adapter (К12) -----------------------------------------------------------
LEGACY_DETECTOR, LEGACY_OTHER = "legacy:detector", "legacy:other"


@dataclass(frozen=True)
class LegacyBasis:
    """The v2 numbers the legacy formulas do not carry (config `calculator_v2`)."""

    load: LoadInput
    server_cores: Fraction
    server_power: Q
    hp_power: Q
    tariff: Q
    hours: Fraction


def _qty(x: float) -> str:
    return str(int(x)) if x == int(x) else texts.fmt_num(x)


def _line(label: str, n: float, price: float) -> WhyItem:
    """«Ускорители LinQ: 3 × 500 000 ₽»."""
    return WhyItem(label=label, value=f"{_qty(n)} × {texts.fmt_rub(price)}")


def legacy_group(cameras: int, models_per_frame: float) -> Group:
    """M equivalent models on every camera: d = min(1, M), x = max(0, M − 1) (К12)."""
    m = fr(models_per_frame)
    weights = ((LEGACY_DETECTOR, min(Fraction(1), m)), (LEGACY_OTHER, max(Fraction(0), m - 1)))
    return Group("added:legacy", cameras, LEGACY_DETECTOR, weights)


def _legacy_policy(
    a: dict[str, float], overrides: dict[str, float], basis: LegacyBasis, fps: float
) -> Policy:
    """v2 load policy at the pipeline fps; an explicit capacity_fps override replaces C."""
    pol = policy(basis.load, fr(fps))
    if "accelerator.capacity_fps" in overrides:
        pol = replace(pol, capacity=fr(a["accelerator.capacity_fps"]))
    return pol


def _legacy_hw(a: dict[str, float], basis: LegacyBasis) -> tuple[dict[str, Board], ServerSpec]:
    """HP at the legacy price; servers by `accelerators_per_server` HP and by CPU (К12)."""
    for field, value in (
        ("costs.electricity_rub_kwh", basis.tariff),
        ("catalog.boards.HP.power_w", basis.hp_power),
        ("hardware.server.power_w", basis.server_power),
    ):
        if value is None:
            raise ValidationFailed(
                texts.CALC2_LEGACY_PRICING.format(field=field),
                field=field,
                reason="LEGACY_REQUIRES_PRICING",
            )
    hp = Board("HP", 1, 1, basis.hp_power, fr(a["accelerator.price_rub"]))
    spec = ServerSpec(
        1,
        basis.server_cores,
        fr(a["server.price_rub"]),
        basis.server_power,
        chips_per_server=fr(a["accelerators_per_server"]),
    )
    return {"HP": hp}, spec


def _legacy_plan(
    cameras: int,
    a: dict[str, float],
    pol: Policy,
    before: Kit,
    boards: dict[str, Board],
    spec: ServerSpec,
) -> tuple[Load, Kit]:
    found = load_of([legacy_group(cameras, a["models_per_frame"])], pol, 1)
    if cast(int, found.chips) > MAX_CHIPS:
        raise limit_error()
    plan = select(found.chips, found.cpu, before, list(boards.values()), boards, spec)
    return found, cast(Kit, plan.purchase)


def _legacy_assumptions(
    assumptions: dict[str, CalcAssumption], pol: Policy, basis: LegacyBasis, overridden: bool
) -> list[CalcAssumption]:
    """The config assumptions and the v2 numbers the legacy answer now depends on."""
    extra = [
        ("v2.load.activity_share", "Доля времени, когда на камере есть люди", pol.p, "доля"),
        (
            "v2.load.priority_cameras_reserve",
            "Резерв тревожных камер",
            Fraction(pol.reserve),
            "шт.",
        ),
        ("v2.load.effective_chip_fps", texts.CALC_EFFECTIVE_CAPACITY, pol.capacity, "экв. кадр/с"),
        ("v2.load.cpu_ms_per_unit", "CPU на единицу нагрузки", pol.cpu_ms, "мс"),
        (
            "v2.hardware.server.usable_cpu_cores",
            "Полезных ядер CPU в сервере",
            basis.server_cores,
            "ядро",
        ),
        (
            "v2.costs.electricity_rub_kwh",
            "Тариф на электроэнергию",
            cast(Fraction, basis.tariff),
            "₽/кВт·ч",
        ),
        ("v2.costs.operating_hours_year", "Часов работы в году", basis.hours, "ч"),
    ]
    out = list(assumptions.values())
    for key, title, value, unit in extra:
        source = texts.CALC_LEGACY_SOURCE
        if key == "v2.load.effective_chip_fps" and overridden:
            source = texts.CALC_LEGACY_CAPACITY_OVERRIDE
        out.append(
            CalcAssumption(
                key=key, title=title, value=float(value), unit=unit, source=source, editable=False
            )
        )
    return out


def rollout(
    data: RolloutIn,
    assumptions: dict[str, CalcAssumption],
    analysis_fps: float,
    events_per_camera_day: float | None,
    basis: LegacyBasis,
) -> RolloutResult:
    a = {key: item.value for key, item in assumptions.items()}
    pol = _legacy_policy(a, data.overrides, basis, analysis_fps)
    boards, spec = _legacy_hw(a, basis)
    _, purchase = _legacy_plan(data.cameras, a, pol, EMPTY_KIT, boards, spec)
    accelerators, servers = kit_chips(purchase, boards), purchase.servers
    power = kit_power(purchase, boards, spec)
    elec = cast(Fraction, electricity(power, basis.hours, basis.tariff))
    incident_cost = (
        data.downtime_cost_rub
        + data.fine_cost_rub
        + data.treatment_cost_rub
        + data.lawsuit_cost_rub
    )
    zones = data.cameras * a["zones_per_camera"]
    new_cameras = ceil(data.cameras * fr(a["new_cameras_share"]))
    base = (
        accelerators * fr(a["accelerator.price_rub"])
        + servers * fr(a["server.price_rub"])
        + fr(a["integration_rub"])
    )
    extended = base + fr(zones) * fr(a["light_sound_rub"])
    top_ = extended + data.workshops * fr(a["speaker_rub"]) + new_cameras * fr(a["new_camera_rub"])
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

    def tier(name: CalcTier, capex: Fraction, items: list[WhyItem]) -> TierResult:
        opex = capex * fr(a["support_share_year"]) + elec
        savings = fr(data.incidents_per_year) * fr(incident_cost) * fr(a[f"reduction.{name}"])
        payback = capex / (savings - opex) * 12 if savings > opex else None
        verdict = (
            texts.CALC_NOT_PROFITABLE
            if payback is None
            else texts.CALC_PAYBACK_MONTHS.format(n=texts.fmt_num(float(payback)))
        )
        return TierResult(
            tier=name,
            title=texts.CALC_TIER_TITLES[name],
            accelerators=accelerators,
            servers=servers,
            capex_rub=float(capex),
            opex_rub_year=float(opex),
            savings_rub_year=float(savings),
            payback_months=None if payback is None else float(payback),
            items=[
                *items,
                WhyItem(label=texts.CALC_ELECTRICITY, value=texts.fmt_rub(float(elec))),
                WhyItem(label=texts.CALC_PAYBACK, value=verdict),
            ],
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
            tier("max", top_, top_items),
        ],
        assumptions=_legacy_assumptions(
            assumptions, pol, basis, "accelerator.capacity_fps" in data.overrides
        ),
    )


def scale(
    data: ScaleIn,
    assumptions: dict[str, CalcAssumption],
    analysis_fps: float,
    basis: LegacyBasis,
) -> ScaleResult:
    """Legacy scale: today's inventory is the greenfield plan of today's cameras (К12)."""
    a = {key: item.value for key, item in assumptions.items()}
    pol = _legacy_policy(a, data.overrides, basis, analysis_fps)
    boards, spec = _legacy_hw(a, basis)
    now_load, before = _legacy_plan(data.cameras_now, a, pol, EMPTY_KIT, boards, spec)
    cameras = data.cameras_now + data.new_cameras
    total_load, purchase = _legacy_plan(cameras, a, pol, before, boards, spec)
    added_boards, added_servers = kit_chips(purchase, boards), purchase.servers
    capex = (
        added_boards * fr(a["accelerator.price_rub"])
        + added_servers * fr(a["server.price_rub"])
        + data.new_cameras * fr(a["new_camera_rub"])
    )
    overridden = "accelerator.capacity_fps" in data.overrides
    return ScaleResult(
        cameras_total=cameras,
        analysis_fps=analysis_fps,
        capacity_fps=float(pol.capacity),
        capacity_source=(
            texts.CALC_LEGACY_CAPACITY_OVERRIDE if overridden else texts.CALC_EFFECTIVE_CAPACITY
        ),
        accelerators_now=cast(int, now_load.chips),
        accelerators_total=cast(int, total_load.chips),
        servers_total=kit_add(before, purchase).servers,
        capex_rub=float(capex),
        items=[
            _line(texts.CALC_ACCELERATORS, added_boards, a["accelerator.price_rub"]),
            _line(texts.CALC_SERVERS, added_servers, a["server.price_rub"]),
            _line(texts.CALC_NEW_CAMERAS, data.new_cameras, a["new_camera_rub"]),
        ],
        assumptions=_legacy_assumptions(assumptions, pol, basis, overridden),
    )


# --- validation of a v2 request (К3, К4, К10) ---------------------------------------------
def _range(
    field: str, value: float | None, lo: float | None, hi: float | None, lo_open: bool = False
) -> None:
    if value is None:
        return
    if (lo is not None and (value <= lo if lo_open else value < lo)) or (
        hi is not None and value > hi
    ):
        raise invalid(field, "OUT_OF_RANGE")


def _shares(field: str, shares: Any) -> None:
    for tier in TIERS:
        _range(f"{field}.{tier}", getattr(shares, tier), 0, 1)


def validate_profile(field: str, prof: Any, catalog: Catalog) -> None:
    """A manual profile: groups, shares summing to 1, one detector per group, known models."""
    if not isinstance(prof, ManualCameraProfile):
        return
    _range(f"{field}.cameras", prof.cameras, 0, MAX_CAMERAS)
    if len(prof.groups) > MAX_GROUPS:
        raise invalid(f"{field}.groups", "OUT_OF_RANGE")
    if prof.cameras == 0 and prof.groups:
        raise invalid(f"{field}.groups", "GROUP_SHARES")
    if prof.cameras > 0 and not prof.groups:
        raise invalid(f"{field}.groups", "GROUP_SHARES")
    ids = [g.id for g in prof.groups]
    if len(set(ids)) != len(ids):
        raise invalid(f"{field}.groups", "GROUP_SHARES")
    for k, g in enumerate(prof.groups):
        path = f"{field}.groups.{k}"
        _range(f"{path}.share", g.share, 0, 1, lo_open=True)
        if (
            not g.model_ids
            or len(g.model_ids) > MAX_MODELS
            or len(set(g.model_ids)) != len(g.model_ids)
        ):
            raise invalid(f"{path}.model_ids", "SCHEMA_MISMATCH")
        for m in g.model_ids:
            if m not in catalog.models:
                raise invalid(f"{path}.model_ids", "UNKNOWN_MODEL")
        if sum(catalog.models[m].kind == "detector" for m in g.model_ids) != 1:
            raise invalid(f"{path}.model_ids", "SCHEMA_MISMATCH")
    if prof.groups and abs(sum((fr(g.share) for g in prof.groups), Fraction(0)) - 1) > Fraction(
        1, 10**9
    ):
        raise invalid(f"{field}.groups", "GROUP_SHARES")


def validate(req: Request, catalog: Catalog) -> None:
    """Range and cross-field rules a schema cannot express; the first failure in field order."""
    scale_mode = isinstance(req, ScaleRequestV2)
    site = req.site
    _range("site.workshops", site.workshops, 0 if scale_mode else 1, None)
    _range("site.workers", site.workers, 0, None)
    _range("site.shifts_per_day", site.shifts_per_day, 0, 3)
    _range("site.working_days_year", site.working_days_year, 1, 366)
    _range("site.operators", site.operators, 0, None)

    ld = req.load
    _range("load.activity_share", ld.activity_share, 0, 1)
    _range("load.target_fps", ld.target_fps, 0, 120, lo_open=True)
    _range("load.surge_fps", ld.surge_fps, 0, ld.target_fps, lo_open=True)
    _range("load.idle_check_s", ld.idle_check_s, 0, None, lo_open=True)
    if fr(1) / fr(ld.idle_check_s) > fr(ld.target_fps) / ld.detector_stride:
        raise invalid("load.idle_check_s", "OUT_OF_RANGE")
    _range("load.priority_cameras_reserve", ld.priority_cameras_reserve, 0, MAX_CAMERAS)
    if ld.detector_stride == 2 and not catalog.tracker_available:
        raise invalid("load.detector_stride", "TRACKER_NOT_VALIDATED")
    _range("load.reference_chip_fps", ld.reference_chip_fps, 0, None, lo_open=True)
    _range("load.capacity_derate", ld.capacity_derate, 0, 1, lo_open=True)
    _range(
        "load.platform_capacity_override_fps",
        ld.platform_capacity_override_fps,
        0,
        None,
        lo_open=True,
    )
    for model_id, weight in ld.model_cost_overrides.items():
        if model_id not in catalog.models:
            raise invalid(f"load.model_cost_overrides.{model_id}", "UNKNOWN_MODEL")
        _range(f"load.model_cost_overrides.{model_id}", weight, 0, None, lo_open=True)
    _range("load.cpu_ms_per_unit", ld.cpu_ms_per_unit, 0, None)
    _range(
        "load.decode_cores_per_camera",
        ld.decode_cores_per_camera,
        0,
        0 if ld.cpu_basis == "inclusive" else None,
    )

    hw = req.hardware
    if not hw.allowed_board_ids or len(hw.allowed_board_ids) > MAX_BOARDS:
        raise invalid("hardware.allowed_board_ids", "OUT_OF_RANGE")
    if len(set(hw.allowed_board_ids)) != len(hw.allowed_board_ids):
        raise invalid("hardware.allowed_board_ids", "SCHEMA_MISMATCH")
    for board in hw.allowed_board_ids:
        if board not in catalog.boards:
            raise invalid("hardware.allowed_board_ids", "UNKNOWN_BOARD")
    for board, price in hw.board_price_overrides.items():
        if board not in catalog.boards:
            raise invalid(f"hardware.board_price_overrides.{board}", "UNKNOWN_BOARD")
        _range(f"hardware.board_price_overrides.{board}", price, 0, None)
    _range("hardware.server.slots", hw.server.slots, 1, None)
    _range("hardware.server.usable_cpu_cores", hw.server.usable_cpu_cores, 0, None, lo_open=True)
    _range("hardware.server.price_rub", hw.server.price_rub, 0, None)
    _range("hardware.server.power_w", hw.server.power_w, 0, None)

    c = req.costs
    for name in (
        "integration_fixed_rub",
        "integration_per_camera_rub",
        "electricity_rub_kwh",
        "signal_zones_per_camera",
        "signal_unit_rub",
        "speaker_per_workshop_rub",
        "new_camera_unit_rub",
    ):
        _range(f"costs.{name}", getattr(c, name), 0, None)
    _range("costs.support_share_year", c.support_share_year, 0, 1)
    _range("costs.operating_hours_year", c.operating_hours_year, 0, 8784)
    _range("costs.max_additional_camera_share", c.max_additional_camera_share, 0, 1)

    b = req.benefits
    inj = b.injuries
    for name in ("annual_injured_workers", "rate_per_1000", "cost_per_injured_worker_rub"):
        _range(f"benefits.injuries.{name}", getattr(inj, name), 0, None)
    _shares("benefits.injuries.reduction", inj.reduction)
    for name in ("events_year", "days_per_event", "day_cost_rub"):
        _range(f"benefits.downtime.{name}", getattr(b.downtime, name), 0, None)
    _shares("benefits.downtime.reduction", b.downtime.reduction)
    if len({i.id for i in b.fines.items}) != len(b.fines.items):
        raise invalid("benefits.fines.items", "SCHEMA_MISMATCH")
    for k, item in enumerate(b.fines.items):
        _range(
            f"benefits.fines.items.{k}.inspection_probability_year",
            item.inspection_probability_year,
            0,
            1,
        )
        _range(f"benefits.fines.items.{k}.amount_rub", item.amount_rub, 0, None)
        _shares(f"benefits.fines.items.{k}.reduction", item.reduction)
    sfr = b.sfr_discount
    _range("benefits.sfr_discount.payroll_rub_year", sfr.payroll_rub_year, 0, None)
    _range("benefits.sfr_discount.tariff_share", sfr.tariff_share, 0, 1)
    _range("benefits.sfr_discount.additional_discount_share", sfr.additional_discount_share, 0, 0.4)
    for k, row in enumerate(b.labor.rows):
        _range(f"benefits.labor.rows.{k}.hours_saved_year", row.hours_saved_year, 0, None)
        _range(f"benefits.labor.rows.{k}.hour_cost_rub", row.hour_cost_rub, 0, None)
    _range("benefits.severe_injury_cost_rub", b.severe_injury_cost_rub, 0, None)
    labor_money = b.labor.monetize and any(r.hours_saved_year > 0 for r in b.labor.rows)
    if (
        inj.enabled
        and inj.cost_scope == "all_in"
        and (b.downtime.enabled or b.fines.enabled or labor_money)
    ):
        raise invalid("benefits.injuries.cost_scope", "DOUBLE_COUNTING")

    if isinstance(req, RolloutRequestV2):
        validate_profile("cameras", req.cameras, catalog)
    else:
        validate_profile("current", req.current, catalog)
        validate_profile("added", req.added, catalog)
        if req.installed is not None:
            seen: set[str] = set()
            for k, inv in enumerate(req.installed.boards):
                if inv.board_id not in catalog.boards:
                    raise invalid(f"installed.boards.{k}.board_id", "UNKNOWN_BOARD")
                if inv.board_id in seen:
                    raise invalid(f"installed.boards.{k}.board_id", "SCHEMA_MISMATCH")
                seen.add(inv.board_id)
                _range(f"installed.boards.{k}.count", inv.count, 0, None)
            _range("installed.servers", req.installed.servers, 0, None)
            slots = sum(i.count * catalog.boards[i.board_id].slots for i in req.installed.boards)
            if slots > req.installed.servers * req.hardware.server.slots:
                raise invalid("installed.servers", "INVENTORY_CAPACITY")


def validate_scope(req: Request, n_scope: int, n_total: int) -> None:
    """Rules that need the resolved camera counts."""
    if n_total > MAX_CAMERAS:
        raise invalid(
            "cameras.cameras" if isinstance(req, RolloutRequestV2) else "added.cameras",
            "OUT_OF_RANGE",
        )
    _range("costs.new_camera_count", req.costs.new_camera_count, 0, n_scope)
