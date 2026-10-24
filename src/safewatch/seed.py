"""Demo world (tech.md 8.16): sectors, cameras, zones and a history of events, all `is_demo=1`.

`build_demo` is pure and deterministic for a given `now`; `seed_demo` writes it through store.
"""

import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from safewatch import clock, config, store, texts
from safewatch.types import ActorRole, EventStatus, Level, LogAction, SeedReport, Verdict

SEED = 2026
DAYS = 42
EVENTS = 240

YELLOW_SHARE = 0.8
WEEKLY_YELLOW_DROP = 0.06
YELLOW_OUTCOMES = [("confirmed", 0.50), ("false_alarm", 0.15), ("auto_finished", 0.35)]
RED_OUTCOMES = [("resolved", 0.70), ("false_alarm", 0.20), ("timeout", 0.10)]
YELLOW_SCENARIOS = ["running", "proximity", "phone"]
RED_SCENARIOS = ["fall", "fence_crossing", "restricted_under", "proximity", "running"]
TIMEOUT_S = 45
STATUS_OF: dict[str, EventStatus] = {
    "confirmed": "confirmed",
    "false_alarm": "false_alarm",
    "auto_finished": "auto_finished",
    "resolved": "resolved",
    "timeout": "resolved",
}

# Zones per camera index: kind and normalized points.
ZONES: dict[int, list[tuple[str, list[list[float]]]]] = {
    0: [("danger", [[0.55, 0.35], [0.9, 0.35], [0.9, 0.85], [0.55, 0.85]])],
    1: [("vehicle_path", [[0.0, 0.6], [1.0, 0.6], [1.0, 0.95], [0.0, 0.95]])],
    2: [("vehicle_path", [[0.1, 0.5], [0.7, 0.5], [0.7, 1.0], [0.1, 1.0]])],
    4: [("under_load", [[0.3, 0.2], [0.7, 0.2], [0.7, 0.6], [0.3, 0.6]])],
    5: [("fence", [[0.5, 0.1], [0.5, 0.95]]), ("danger", [[0.55, 0.2], [1.0, 0.2], [1.0, 0.9]])],
    6: [("lying_allowed", [[0.2, 0.55], [0.8, 0.55], [0.8, 0.95], [0.2, 0.95]])],
}


@dataclass
class DemoAction:
    at: datetime
    actor_role: ActorRole
    action: LogAction
    from_status: EventStatus | None
    to_status: EventStatus | None
    comment: str = ""


@dataclass
class DemoEvent:
    n: int
    camera: int  # index into DemoWorld.cameras
    zone: int | None  # index into DemoWorld.zones
    scenario: str
    reason_text: str
    level: Level
    status: EventStatus
    verdict: Verdict
    escalated_by_timeout: bool
    started_at: datetime
    published_at: datetime
    red_at: datetime | None
    ended_at: datetime
    actions: list[DemoAction] = field(default_factory=list)


@dataclass
class DemoWorld:
    sectors: list[str]
    cameras: list[tuple[int, str, str]]  # sector index, name, description
    zones: list[tuple[int, str, str, list[list[float]]]]  # camera index, kind, name, points
    events: list[DemoEvent]


def _outcomes(rng: random.Random, n: int, shares: list[tuple[str, float]]) -> list[str]:
    out: list[str] = []
    for name, share in shares[:-1]:
        out += [name] * round(n * share)
    out += [shares[-1][0]] * (n - len(out))
    rng.shuffle(out)
    return out


def _yellow_days(rng: random.Random, n: int) -> list[int]:
    """Day offsets back from yesterday; yellow events drop by about 6 % a week."""
    weeks = DAYS // 7
    weights = [(1 - WEEKLY_YELLOW_DROP) ** w for w in range(weeks)]  # w=0: oldest week
    counts = [int(n * w / sum(weights)) for w in weights]
    for week in range(n - sum(counts)):  # the remainder goes to the oldest weeks
        counts[week] += 1
    days: list[int] = []
    for week, count in enumerate(counts):
        first = DAYS - 1 - week * 7
        days += [first - rng.randrange(7) for _ in range(count)]
    return days


def _history(e: DemoEvent, outcome: str, rng: random.Random) -> None:
    def later(t: datetime, lo: int, hi: int) -> datetime:
        return t + timedelta(seconds=rng.randint(lo, hi))

    t = e.published_at
    e.actions.append(DemoAction(t, "system", "published", None, "new"))
    if outcome == "auto_finished":
        e.actions.append(DemoAction(e.ended_at, "system", "auto_finished", "new", "auto_finished"))
        return
    if outcome == "timeout":
        t = t + timedelta(seconds=TIMEOUT_S)
        e.actions.append(DemoAction(t, "system", "timeout_escalated", "new", "sent_to_master"))
        e.escalated_by_timeout = True
        prev: EventStatus = "sent_to_master"
    else:
        t = later(t, 5, 30)
        e.actions.append(DemoAction(t, "operator", "viewed", "new", "viewed"))
        t = later(t, 3, 40)
        if outcome == "false_alarm":
            e.actions.append(DemoAction(t, "operator", "false_alarm", "viewed", "false_alarm"))
            e.verdict = "false_alarm"
            return
        e.actions.append(DemoAction(t, "operator", "confirmed", "viewed", "confirmed"))
        e.verdict = "confirmed"
        if e.level == "yellow":
            return
        e.actions.append(DemoAction(t, "operator", "sent_to_master", "confirmed", "sent_to_master"))
        prev = "sent_to_master"
    t = later(t, 60, 300)
    e.actions.append(DemoAction(t, "master", "master_accepted", prev, "master_accepted"))
    t = later(t, 300, 1800)
    comment = rng.choice(texts.DEMO_RESOLVE_COMMENTS)
    e.actions.append(DemoAction(t, "master", "resolved", "master_accepted", "resolved", comment))


def build_demo(now: datetime, tz: str) -> DemoWorld:
    rng = random.Random(SEED)
    cameras = [(i // 2, name, desc) for i, (name, desc) in enumerate(texts.DEMO_CAMERAS)]
    zones = [
        (cam, kind, texts.DEMO_ZONE_NAMES[kind], points)
        for cam, items in ZONES.items()
        for kind, points in items
    ]
    midnight = clock.local(now, tz).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = midnight - timedelta(days=1)
    n_yellow = round(EVENTS * YELLOW_SHARE)
    plan: list[tuple[Level, int, str]] = []
    for day, outcome in zip(
        _yellow_days(rng, n_yellow), _outcomes(rng, n_yellow, YELLOW_OUTCOMES), strict=True
    ):
        plan.append(("yellow", day, outcome))
    n_red = EVENTS - n_yellow
    for outcome in _outcomes(rng, n_red, RED_OUTCOMES):
        plan.append(("red", rng.randrange(DAYS), outcome))
    events: list[DemoEvent] = []
    for level, day, outcome in plan:
        start = yesterday - timedelta(days=day) + timedelta(seconds=rng.randrange(86400))
        scenario = rng.choice(YELLOW_SCENARIOS if level == "yellow" else RED_SCENARIOS)
        camera = rng.randrange(len(cameras))
        own = [z for z, (cam, *_rest) in enumerate(zones) if cam == camera]
        published = start + timedelta(seconds=rng.randint(2, 8))
        event = DemoEvent(
            n=0,
            camera=camera,
            zone=own[0] if own and rng.random() < 0.5 else None,
            scenario=scenario,
            reason_text=rng.choice(texts.DEMO_REASONS[scenario]),
            level=level,
            status=STATUS_OF[outcome],
            verdict="none",
            escalated_by_timeout=False,
            started_at=start,
            published_at=published,
            red_at=published if level == "red" else None,
            ended_at=published + timedelta(seconds=rng.randint(5, 120)),
        )
        _history(event, outcome, rng)
        events.append(event)
    events.sort(key=lambda e: e.started_at)
    for n, event in enumerate(events, start=1):
        event.n = n
    return DemoWorld(list(texts.DEMO_SECTORS), cameras, zones, events)


def seed_demo() -> SeedReport:
    if store.demo_world_exists():
        return SeedReport(skipped=True, **store.demo_counts())
    world = build_demo(clock.now(), config.get_settings().timezone)
    at = clock.iso(clock.now())
    with store.tx():
        sector_ids = [
            store.insert("sectors", {"name": name, "sort_order": i, "is_demo": 1, "created_at": at})
            for i, name in enumerate(world.sectors, start=1)
        ]
        camera_ids = [
            store.insert(
                "cameras",
                {
                    "sector_id": sector_ids[sector],
                    "name": name,
                    "description": desc,
                    "is_demo": 1,
                    "created_at": at,
                },
            )
            for sector, name, desc in world.cameras
        ]
        zone_ids = [
            store.insert(
                "zones",
                {
                    "camera_id": camera_ids[cam],
                    "kind": kind,
                    "name": name,
                    "points_json": json.dumps(points),
                    "created_at": at,
                },
            )
            for cam, kind, name, points in world.zones
        ]
        for e in world.events:
            event_id = store.insert(
                "events", _event_row(e, world, sector_ids, camera_ids, zone_ids)
            )
            for a in e.actions:
                store.insert(
                    "event_actions",
                    {
                        "event_id": event_id,
                        "at": clock.iso(a.at),
                        "actor_role": a.actor_role,
                        "actor_name": texts.DEMO_ACTOR[a.actor_role],
                        "action": a.action,
                        "from_status": a.from_status,
                        "to_status": a.to_status,
                        "comment": a.comment,
                    },
                )
    return SeedReport(skipped=False, **store.demo_counts())


def _event_row(
    e: DemoEvent,
    world: DemoWorld,
    sector_ids: list[int],
    camera_ids: list[int],
    zone_ids: list[int],
) -> dict[str, Any]:
    return {
        "pub_key": f"demo:{e.n}",
        "camera_id": camera_ids[e.camera],
        "sector_id": sector_ids[world.cameras[e.camera][0]],
        "zone_id": zone_ids[e.zone] if e.zone is not None else None,
        "scenario": e.scenario,
        "title": texts.SCENARIO_TITLES[e.scenario],
        "reason_text": e.reason_text,
        "level": e.level,
        "status": e.status,
        "operator_verdict": e.verdict,
        "escalated_by_timeout": int(e.escalated_by_timeout),
        "started_at": clock.iso(e.started_at),
        "published_at": clock.iso(e.published_at),
        "red_at": clock.iso(e.red_at) if e.red_at else None,
        "ended_at": clock.iso(e.ended_at),
        "is_demo": 1,
    }


def demo_camera_ids() -> list[int]:
    return [int(row["id"]) for row in store.demo_cameras()]
