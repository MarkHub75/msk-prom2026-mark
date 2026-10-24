"""Slice 20: `no_helmet`, `no_respirator` (tech.md 8.22), `head_objects`, Matvey's helmet."""

from pathlib import Path

import pytest
from test_jobs import _tune, _video
from test_linq_backend import RecordingShell
from test_plugin_status import DEFAULT, statuses
from test_rule_phone import ctx_with, worker
from test_rule_running import zone

from safewatch import registry, rules, services
from safewatch.analysis.episodes import EpisodeManager
from safewatch.analysis.pipeline import analyze
from safewatch.config import Settings, get_settings
from safewatch.inference.linq import LinqBackend
from safewatch.types import (
    AnalysisConfig,
    Detection,
    EpisodeDraft,
    FrameContext,
    FrameDetections,
    ObjectState,
    Observation,
    PersonState,
)

HELMET = "matvey-helmet-yolov8n@640-v1-5c3af1f3b855"
POSE = "matvey-pose-yolov8n@640-v1-acc5f51228b9"
# worker(): bbox (450, 100, 550, 300), 200 px tall, foot (500, 300) inside zone();
# head_frac 0.35 puts the head at y 100..170.
ROWS = [
    ("no_helmet", "helmet", "helmet_required", "Цех 2", "Без каски в зоне «Цех 2»"),
    (
        "no_respirator",
        "respirator",
        "respirator_required",
        "Покрасочная",
        "Без респиратора в зоне «Покрасочная»",
    ),
]


def item(name: str, cx: float, cy: float) -> ObjectState:
    return ObjectState(name=name, bbox=(cx - 8, cy - 8, cx + 8, cy + 8), score=0.6)


def observe(
    scenario: str, people: list[PersonState], objects: list[ObjectState], zones=None, **params
) -> list[Observation]:
    ctx: FrameContext = ctx_with(people, objects, zones)
    return rules.plugin(scenario).observe(ctx, rules.defaults(scenario) | params)


def held(scenario: str, worn: str, kind: str, until_ms: int) -> list[EpisodeDraft]:
    zones = [zone(kind, name="Цех 2")]
    manager = EpisodeManager(get_settings().episodes)
    for i, ts in enumerate(range(0, until_ms + 1, 10)):
        ctx = ctx_with([worker()], [item(f"no_{worn}", 500, 120)], zones, ts)
        manager.update(i, ts, rules.plugin(scenario).observe(ctx, rules.defaults(scenario)))
    ctx = ctx_with([worker()], [item(worn, 500, 120)], zones, until_ms + 10)
    manager.update(
        10_000, until_ms + 10, rules.plugin(scenario).observe(ctx, rules.defaults(scenario))
    )
    return manager.finish(until_ms + 100)


def check_rows(scenario: str, worn: str, kind: str, name: str, text: str) -> None:
    """Rows N, U and the head binding of tech.md 8.22 for one PPE plugin."""
    inside = [zone(kind, name=name)]
    bad = f"no_{worn}"
    (o,) = observe(scenario, [worker()], [item(bad, 500, 120)], inside)
    assert (o.state, o.level, o.hold_s, o.reason_code, o.reason_text, o.zone_id) == (
        "P",
        "yellow",
        3.0,
        scenario,
        text,
        7,
    )
    assert observe(scenario, [worker()], [item(bad, 500, 120)])[0].state == "N"  # no zone
    other = [zone("helmet_required" if kind != "helmet_required" else "respirator_required")]
    assert observe(scenario, [worker()], [item(bad, 500, 120)], other)[0].state == "N"
    assert observe(scenario, [worker()], [item(worn, 500, 120)], inside)[0].state == "N"
    unseen = observe(scenario, [worker()], [], inside)[0]
    assert (unseen.state, unseen.reason_code) == ("U", "head_unseen")
    # The head ends at y = 100 + 0.35 × 200 = 170; x stays within 450..550.
    assert observe(scenario, [worker()], [item(bad, 500, 170)], inside)[0].state == "P"
    low = observe(scenario, [worker()], [item(bad, 500, 171)], inside)[0]
    assert (low.state, low.reason_code) == ("U", "head_unseen")
    assert (
        observe(scenario, [worker()], [item(bad, 500, 171)], inside, head_frac=0.4)[0].state == "P"
    )
    assert observe(scenario, [worker()], [item(bad, 551, 120)], inside)[0].state == "U"
    # Two heads share the object: unknown for both.
    second = worker(track_id=2, bbox=(540.0, 100.0, 640.0, 300.0), anchor=(590.0, 300.0))
    both = observe(scenario, [worker(), second], [item(bad, 545, 120)], inside)
    assert [(x.subject, x.state, x.reason_code) for x in both] == [
        ("track:1", "U", "owner_ambiguous"),
        ("track:2", "U", "owner_ambiguous"),
    ]
    shared_good = observe(scenario, [worker(), second], [item(worn, 545, 120)], inside)
    assert [x.reason_code for x in shared_good] == ["owner_ambiguous", "owner_ambiguous"]
    small = observe(scenario, [worker(height_px=79.0)], [item(bad, 500, 120)], inside)[0]
    assert (small.state, small.reason_code) == ("U", "too_small")
    assert (
        observe(scenario, [worker(height_px=80.0)], [item(bad, 500, 120)], inside)[0].state == "P"
    )
    tall = observe(scenario, [worker(height_px=80.0)], [], inside, min_person_px=81.0)[0]
    assert tall.reason_code == "too_small"
    (custom,) = observe(scenario, [worker()], [item(bad, 500, 120)], inside, hold_s=5.0)
    assert custom.hold_s == 5.0


def test_no_helmet_in_zone_yellow_after_hold() -> None:
    assert held("no_helmet", "helmet", "helmet_required", 2990) == []
    (ep,) = held("no_helmet", "helmet", "helmet_required", 3000)
    assert (ep.scenario, ep.level_initial, ep.reason_text, ep.zone_id) == (
        "no_helmet",
        "yellow",
        "Без каски в зоне «Цех 2»",
        7,
    )
    assert rules.defaults("no_helmet") == {"hold_s": 3.0, "head_frac": 0.35, "min_person_px": 80}
    why = rules.plugin("no_helmet").explain(ep, rules.defaults("no_helmet"))
    assert why[0].value == "Без каски в зоне «Цех 2» дольше 3,0 с"


def test_outside_zone_no_event() -> None:
    (o,) = observe("no_helmet", [worker()], [item("no_helmet", 500, 120)], [zone("danger")])
    assert o.state == "N"
    small = observe("no_helmet", [worker(height_px=10.0)], [], [zone("rest")])[0]
    assert small.state == "N"  # outside the zone the size does not matter


def test_helmet_seen_is_negative() -> None:
    inside = [zone("helmet_required")]
    assert observe("no_helmet", [worker()], [item("helmet", 500, 120)], inside)[0].state == "N"
    # A helmet on someone else's head says nothing about this person.
    away = item("helmet", 800, 120)
    assert observe("no_helmet", [worker()], [away], inside)[0].reason_code == "head_unseen"


def test_surer_class_wins_on_one_head() -> None:
    """R20: `no_helmet` and `helmet` on one head: the higher score wins, a tie stays P."""
    inside = [zone("helmet_required")]
    bare, worn = item("no_helmet", 500, 120), item("helmet", 500, 125)

    def state(bare_score: float, worn_score: float) -> str:
        objects = [
            bare.model_copy(update={"score": bare_score}),
            worn.model_copy(update={"score": worn_score}),
        ]
        return observe("no_helmet", [worker()], objects, inside)[0].state

    assert (state(0.6, 0.6), state(0.61, 0.6), state(0.6, 0.61)) == ("P", "P", "N")


def test_head_unseen_unknown() -> None:
    check_rows(*ROWS[0])


def test_ambiguous_and_small() -> None:
    inside = [zone("helmet_required")]
    second = worker(track_id=2, bbox=(540.0, 100.0, 640.0, 300.0), anchor=(590.0, 300.0))
    # One object on the shared x range: unknown; a second object on one head only binds it.
    pair = observe("no_helmet", [worker(), second], [item("no_helmet", 545, 120)], inside)
    assert [x.reason_code for x in pair] == ["owner_ambiguous", "owner_ambiguous"]
    alone = observe("no_helmet", [worker(), second], [item("no_helmet", 600, 120)], inside)
    assert [x.state for x in alone] == ["U", "P"]
    assert alone[0].reason_code == "head_unseen"
    assert observe("no_helmet", [worker(height_px=79.0)], [], inside)[0].reason_code == "too_small"
    assert (
        observe("no_helmet", [worker(height_px=80.0)], [], inside)[0].reason_code == "head_unseen"
    )


def test_respirator_rows() -> None:
    check_rows(*ROWS[1])
    scenario, worn, kind = ROWS[1][:3]
    assert held(scenario, worn, kind, 2990) == []
    (ep,) = held(scenario, worn, kind, 3000)
    assert (ep.scenario, ep.level_initial) == (scenario, "yellow")


def test_respirator_model_missing_text(core: Settings) -> None:
    default = statuses(DEFAULT)
    assert default["no_helmet"] == ("model_missing", "Модель не подключена: нужны классы no_helmet")
    assert default["no_respirator"] == (
        "model_missing",
        "Модель не подключена: нужны классы no_respirator",
    )
    assert default["no_harness"] == (
        "model_missing",
        "Модель не подключена: нужны классы no_harness",
    )
    assert statuses([*DEFAULT, "no_respirator"])["no_respirator"][0] == "active"
    assert statuses([*DEFAULT, "respirator"])["no_respirator"][0] == "model_missing"
    assert statuses(["no_respirator"])["no_respirator"] == (
        "model_missing",
        "Модель не подключена: нужны классы person",
    )
    metas = {m.id: m for m in rules.scenario_metas(DEFAULT)}
    assert (metas["no_respirator"].icon, metas["no_respirator"].zone_kinds) == (
        "mask",
        ["respirator_required"],
    )
    assert metas["no_helmet"].title == "Без каски в зоне обязательной каски"


async def test_helmet_model_activates_plugin(
    fake_core: Settings,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    make_video,
) -> None:
    tuned = _tune(monkeypatch, fake_core, pipeline={"extra": [HELMET]})
    metas = {m.id: m.status for m in rules.scenario_metas()}
    assert (metas["no_helmet"], metas["no_respirator"]) == ("active", "model_missing")

    shell = RecordingShell()
    monkeypatch.setattr(services, "_backend", LinqBackend(tuned, shell))
    _video(tmp_path, make_video, seconds=1)
    job = await services.run_next_job()
    assert job is not None and job.status == "done"
    starts = [c for c in shell.commands if c.endswith("# sw:start")]
    (helmet,) = [c for c in starts if "mosprom_matvey_helmet_yolov8n" in c]
    assert "--nc 2" in helmet and "--classes" not in helmet

    # The helmet frames reach the plugin: a bare head in the zone for 4 s is one yellow episode.
    model = registry.resolve(HELMET)
    person = Detection(cls=0, name="", score=0.9, bbox_xyxy=(450.0, 100.0, 550.0, 300.0))
    bare = Detection(cls=1, name="", score=0.8, bbox_xyxy=(490.0, 110.0, 510.0, 130.0))
    det = [FrameDetections(frame_idx=i, ts_ms=i * 100, detections=[person]) for i in range(40)]
    extra = [f.model_copy(update={"detections": [bare]}) for f in det]
    cfg = AnalysisConfig(
        width=1000, height=500, fps=10, step=1, duration_ms=4000, calibration=None,
        zones=[zone("helmet_required", name="Цех 2")], rules={}, class_conf=tuned.class_conf,
        active_classes=[*DEFAULT, "helmet", "no_helmet"],
    )  # fmt: skip
    detector = registry.resolve(tuned.pipeline.detector)
    result = analyze(det, None, Path("unused.mp4"), cfg, None, detector, [(model, extra)])
    assert [(e.scenario, e.level_initial, e.reason_text) for e in result.episodes] == [
        ("no_helmet", "yellow", "Без каски в зоне «Цех 2»")
    ]
    assert registry.resolve(POSE).task == "pose"
