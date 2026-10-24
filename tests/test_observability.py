"""Slice 11: blind intervals of tech.md 8.10 and the episode that runs through one."""

from pathlib import Path

import pytest
from conftest import MakeVideo

from safewatch import config, registry, rules, texts
from safewatch.analysis import pipeline
from safewatch.analysis.observability import Luma, find_gaps
from safewatch.config import ObservabilityConfig, Settings, get_settings
from safewatch.fakes import scenes
from safewatch.media import sample_luma
from safewatch.types import AnalysisConfig, AnalysisResult, CameraRule

BRIGHT = (120.0, 50.0)  # mean, std of an ordinary frame


def _params(**update: float) -> ObservabilityConfig:
    return get_settings().observability.model_copy(update=update)


def _gaps(
    frames_ts: list[int], luma: list[Luma], duration_ms: int, **update: float
) -> list[tuple[int, int, str]]:
    return [
        (g.start_ms, g.end_ms, g.reason)
        for g in find_gaps(frames_ts, luma, duration_ms, _params(**update))
    ]


def _run(mean: float, std: float, start: int, end: int, duration: int = 10_000) -> list[Luma]:
    """Samples every 100 ms: (mean, std) in `[start, end)`, an ordinary frame elsewhere."""
    return [(t, *((mean, std) if start <= t < end else BRIGHT)) for t in range(0, duration, 100)]


def test_stale_gap_from_missing_frames() -> None:
    assert _gaps([0, 2000, 4001, 4100], [], 5000) == [(2000, 4001, "stale")]
    assert _gaps([0, 2000, 4000], [], 5000) == []
    # stale_after_ms is read: 1999 ms of silence is stale at 1998.
    assert _gaps([0, 1999], [], 5000, stale_after_ms=1998) == [(0, 1999, "stale")]


def test_dark_and_obstructed_gaps(tmp_path: Path, make_video: MakeVideo) -> None:
    assert _gaps([], _run(34, 50, 1000, 4000), 10_000) == [(1000, 4000, "dark")]
    assert _gaps([], _run(34, 50, 1000, 3900), 10_000) == []  # 2,9 s
    assert _gaps([], _run(35, 50, 1000, 4000), 10_000) == []
    assert _gaps([], _run(120, 11, 1000, 4000), 10_000) == [(1000, 4000, "obstructed")]
    assert _gaps([], _run(120, 12, 1000, 4000), 10_000) == []
    # A run up to the end of the video lasts until `duration_ms`.
    assert _gaps([], _run(34, 50, 7000, 10_000), 10_000) == [(7000, 10_000, "dark")]
    # The keys are read: a threshold or the minimum duration moves the answer.
    assert _gaps([], _run(39, 50, 1000, 4000), 10_000, dark_mean=40) == [(1000, 4000, "dark")]
    assert _gaps([], _run(120, 15, 1000, 4000), 10_000, obstructed_std=16) == [
        (1000, 4000, "obstructed")
    ]
    assert _gaps([], _run(34, 50, 1000, 3900), 10_000, min_duration_s=2.9) == [(1000, 3900, "dark")]
    # sample_luma on a real file: a flat dark clip is dark and featureless, once a second.
    luma = sample_luma(make_video(tmp_path, 4, 10, luma=20), 1.0)
    assert [t for t, _, _ in luma] == [0, 1000, 2000, 3000]
    assert all(mean < 35 and std < 12 for _, mean, std in luma)
    assert _gaps([], luma, 4000) == [(0, 4000, "dark"), (0, 4000, "obstructed")]
    assert sample_luma(tmp_path / "missing.mp4", 1.0) == []


W, H, STEP_MS = 8000, 240, 80  # wide enough that the person never wraps at the edge


def _episodes(
    scene: str, det_drop: tuple[int, int] | None = None, speed_bh_s: float = 1.5
) -> AnalysisResult:
    """12 s of a scene through `analyze`; frames in `det_drop` are missing from the artifact."""
    settings = get_settings()
    det = scenes.render(scene, W, H, 25, 300, 2, "detect")
    if det_drop is not None:
        det = [f for f in det if not det_drop[0] <= f.ts_ms < det_drop[1]]
    rule = CameraRule(
        camera_id=1, scenario="running", enabled=True, params={"speed_bh_s": speed_bh_s},
        effective={}, status="active",
    )  # fmt: skip
    cfg = AnalysisConfig(
        width=W, height=H, fps=25, step=2, duration_ms=12_000, calibration=None, zones=[],
        rules={"running": rule}, class_conf=settings.class_conf,
        active_classes=registry.active_classes(settings),
    )  # fmt: skip
    model = registry.resolve(settings.pipeline.detector)
    return pipeline.analyze(det, None, Path("unused.mp4"), cfg, None, model)


@pytest.fixture
def luma(monkeypatch: pytest.MonkeyPatch) -> list[Luma]:
    """What `sample_luma` returns to `analyze`; a test fills it."""
    samples: list[Luma] = []
    monkeypatch.setattr(pipeline.media, "sample_luma", lambda path, every_s: samples)
    return samples


@pytest.mark.parametrize("blind_s", [3, 6])
def test_uncertain_time_in_why(luma: list[Luma], blind_s: int) -> None:
    start, end = 4000, 4000 + blind_s * 1000
    luma += _run(10, 50, start, end, 12_000)
    result = _episodes("running")
    assert [(g.start_ms, g.end_ms, g.reason) for g in result.gaps] == [(start, end, "dark")]
    running = [e for e in result.episodes if e.scenario == "running"]
    if blind_s > get_settings().episodes.lost_timeout_s:
        # Longer than lost_timeout_s: closed at the last P, a new episode after the gap.
        assert [e.end_reason for e in running] == ["track_lost_timeout", "video_end"]
        assert running[0].end_ms < start
        return
    (episode,) = running  # the runner is seen in the dark, but a dark frame tells nothing
    assert episode.end_reason == "video_end" and episode.start_ms < start
    assert blind_s * 1000 <= episode.uncertain_ms < blind_s * 1000 + 2 * STEP_MS
    why = rules.plugin("running").explain(episode, rules.defaults("running"))
    lost = [w.value for w in why if w.label == texts.WHY_UNCERTAIN]
    assert (texts.WHY_UNCERTAIN, lost) == ("Потеря видимости", [f"{blind_s} с"])


def test_stale_gap_counts_as_blind_time(
    luma: list[Luma], settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A walker (running rule at 0,4 H/s) keeps his track over 0,6 s without frames."""
    tuned = settings.model_copy(
        update={"observability": settings.observability.model_copy(update={"stale_after_ms": 500})}
    )
    monkeypatch.setattr(config, "get_settings", lambda: tuned)
    result = _episodes("walk", (4000, 4600), speed_bh_s=0.4)
    assert [(g.start_ms, g.end_ms, g.reason) for g in result.gaps] == [(3920, 4640, "stale")]
    (episode,) = [e for e in result.episodes if e.scenario == "running"]
    # The 720 ms gap itself plus the frames after it, until the speed window refills.
    assert episode.uncertain_ms >= 4640 - 3920
