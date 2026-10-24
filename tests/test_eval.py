"""Slice 14: quality evaluation (tech.md 8.18, 9; criteria 1-4)."""

import json
from pathlib import Path

import psutil
import pytest
import test_plugin_status
import yaml
from test_analysis_api import _camera, _textured
from test_jobs import _tune

from safewatch import cli, config, evaluate, services, store
from safewatch.config import Settings
from safewatch.errors import NotFound, ValidationFailed
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference.linq import LinqBackend
from safewatch.types import CameraRuleIn, EpisodeDraft, EvalMetrics, EvalReport, ExpectedEvent

FALL = ExpectedEvent(scenario="fall", start_s=12.0, end_s=30.0)
extra_registry = test_plugin_status.extra_registry  # the fixture: a registry with fire-test@1


def episode(confirm_s: float, scenario: str = "fall") -> EpisodeDraft:
    ms = round(confirm_s * 1000)
    return EpisodeDraft(
        scenario=scenario,
        subject="track:1",
        zone_id=None,
        level_initial="red",
        level_max="red",
        start_ms=ms - 1000,
        confirm_ms=ms,
        escalate_ms=None,
        end_ms=ms + 1000,
        end_reason="observed_exit",
        reason_code=scenario,
        reason_text="",
        method="relative",
        confidence=0.9,
        metrics={},
        uncertain_ms=0,
        confirm_frame_idx=0,
        escalate_frame_idx=None,
    )


def kinds(outcomes: list[evaluate.Outcome]) -> list[str]:
    return sorted(kind for _, kind, _ in outcomes)


def row(rows: list[EvalMetrics], scenario: str) -> EvalMetrics:
    return next(r for r in rows if r.scenario == scenario)


def labels_file(tmp_path: Path, data: object, name: str = "labels.yaml") -> Path:
    path = tmp_path / name
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return path


def shell(
    monkeypatch: pytest.MonkeyPatch, script: list[str | None] | None = None
) -> FakeRemoteShell:
    fake = FakeRemoteShell(script)  # type: ignore[arg-type]
    monkeypatch.setattr(services, "_backend", LinqBackend(config.get_settings(), fake))
    return fake


def test_matching_deadline_boundary() -> None:
    # Criterion 2: the delay of exactly deadline_s is a tp, 0.001 s more is late and an fn.
    exact = evaluate.match_episodes([FALL], [episode(17.0)], 5.0)
    assert exact == [("fall", "tp", 5.0)]
    late = evaluate.match_episodes([FALL], [episode(17.001)], 5.0)
    assert kinds(late) == ["fn", "late"]
    # The deadline is the argument: the same episode is a tp with a longer one.
    assert kinds(evaluate.match_episodes([FALL], [episode(17.001)], 5.002)) == ["tp"]
    # The confirm moment on end_s is outside the label; one ms before it is inside.
    at_end = evaluate.match_episodes([FALL], [episode(30.0)], 20.0)
    assert kinds(at_end) == ["fn", "fp"]
    assert kinds(evaluate.match_episodes([FALL], [episode(29.999)], 20.0)) == ["tp"]
    # Before start_s: outside; on start_s: a tp with zero delay.
    assert kinds(evaluate.match_episodes([FALL], [episode(11.999)], 5.0)) == ["fn", "fp"]
    assert evaluate.match_episodes([FALL], [episode(12.0)], 5.0) == [("fall", "tp", 0.0)]
    # Another scenario never pairs.
    assert kinds(evaluate.match_episodes([FALL], [episode(13.0, "running")], 5.0)) == ["fn", "fp"]
    # Criterion 3: no tp, so precision and recall are 0 and f1 has a zero denominator.
    rows = services._eval_rows(late, 1.0)
    fall = row(rows, "fall")
    assert (fall.tp, fall.fn, fall.late, fall.fp, fall.expected, fall.episodes) == (
        0,
        1,
        1,
        0,
        1,
        1,
    )
    assert fall.recall == 0.0 and fall.precision is None and fall.f1 is None
    assert fall.fp_per_hour == 0.0
    assert fall.delay_s.n == 0 and fall.delay_s.p50 is None
    # Zero hours of video: fp_per_hour has no denominator.
    assert row(services._eval_rows(exact, 0.0), "*").fp_per_hour is None


def test_duplicates_and_false_alarms() -> None:
    running = ExpectedEvent(scenario="running", start_s=0.0, end_s=10.0)
    eps = [episode(14.0), episode(13.0), episode(40.0), episode(2.0, "running")]
    outcomes = evaluate.match_episodes([FALL, running], eps, 5.0)
    # Greedy by delay: 13.0 (1 s) wins, 14.0 is a duplicate of the same label; 40.0 is an fp.
    assert sorted(outcomes, key=str) == sorted(
        [
            ("fall", "tp", 1.0),
            ("fall", "duplicate", None),
            ("fall", "fp", None),
            ("running", "tp", 2.0),
        ],
        key=str,
    )
    # A late second episode of a matched label is a duplicate too, not late.
    assert kinds(evaluate.match_episodes([FALL], [episode(13.0), episode(25.0)], 5.0)) == [
        "duplicate",
        "tp",
    ]
    # Each label takes one episode: two labels, two episodes inside both, two tps.
    second = ExpectedEvent(scenario="fall", start_s=13.0, end_s=30.0)
    both = evaluate.match_episodes([FALL, second], [episode(13.5), episode(14.0)], 5.0)
    assert kinds(both) == ["tp", "tp"]
    # Criterion 3: metrics per scenario and the total row, two hours of video.
    rows = services._eval_rows(outcomes, 2.0)
    assert [r.scenario for r in rows] == ["fall", "running", "*"]
    fall, total = row(rows, "fall"), row(rows, "*")
    assert (fall.expected, fall.episodes, fall.tp, fall.fp, fall.duplicates) == (1, 3, 1, 1, 1)
    assert fall.precision == 0.5 and fall.recall == 1.0
    assert fall.f1 == pytest.approx(2 / 3)
    assert fall.fp_per_hour == 0.5
    assert (total.expected, total.episodes, total.tp, total.fn, total.fp) == (2, 4, 2, 0, 1)
    assert total.precision == pytest.approx(2 / 3) and total.recall == 1.0
    assert (total.delay_s.n, total.delay_s.p50, total.delay_s.p95) == (2, 1.0, 2.0)


def test_labels_schema_errors(core: Settings, tmp_path: Path) -> None:
    video = _textured(tmp_path / "demo.mp4")
    good = {
        "videos": [
            {"path": str(video), "expected": [{"scenario": "fall", "start_s": 1.0, "end_s": 2.0}]}
        ]
    }
    bad = [
        {
            "videos": [
                {
                    "path": str(video),
                    "expected": [{"scenario": "fall", "start_s": 2.0, "end_s": 2.0}],
                }
            ]
        },
        {
            "videos": [
                {
                    "path": str(video),
                    "expected": [{"scenario": "fall", "start_s": 3.0, "end_s": 2.0}],
                }
            ]
        },
        {"videos": [{"path": str(video), "expected": [{"scenario": "fall", "start_s": 1.0}]}]},
        {"deadline_s": 5},
        None,
    ]
    for i, data in enumerate(bad):
        with pytest.raises(ValidationFailed):
            services.eval_run(labels_file(tmp_path, data, f"bad{i}.yaml"))
    (tmp_path / "broken.yaml").write_text("videos: [", encoding="utf-8")
    with pytest.raises(ValidationFailed):
        services.eval_run(tmp_path / "broken.yaml")
    with pytest.raises(NotFound):
        services.eval_run(tmp_path / "missing.yaml")
    missing_video = {"videos": [{"path": str(tmp_path / "none.mp4"), "expected": []}]}
    with pytest.raises(NotFound):
        services.eval_run(labels_file(tmp_path, missing_video, "nv.yaml"))
    unknown_camera = {"videos": [{"path": str(video), "camera_id": 99, "expected": []}]}
    with pytest.raises(NotFound):
        services.eval_run(labels_file(tmp_path, unknown_camera, "nc.yaml"))
    # The neighbour of each bad file passes: start_s < end_s, every field in place.
    assert services._eval_labels(labels_file(tmp_path, good, "good.yaml")).videos[0].expected


def test_eval_cli_exit_codes(
    core: Settings,
    tmp_path: Path,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    video = _textured(tmp_path / "demo.mp4")
    expected = [{"scenario": "fall", "start_s": 0.0, "end_s": 20.0}]
    good = labels_file(tmp_path, {"videos": [{"path": str(video), "expected": expected}]})
    bad = labels_file(tmp_path, {"videos": [{"path": str(video)}]}, "bad.yaml")
    assert cli.main(["eval", str(bad)]) == 2
    assert "Разметка" in capsys.readouterr().err
    assert cli.main(["eval", str(tmp_path / "missing.yaml")]) == 3
    shell(monkeypatch, ["unavailable"])
    assert cli.main(["eval", str(good)]) == 4
    assert "linq_unavailable" in capsys.readouterr().err
    shell(monkeypatch)
    out = tmp_path / "out"
    assert cli.main(["eval", str(good), "--out", str(out)]) == 0
    printed = capsys.readouterr().out
    assert printed.startswith(str(out)) and "| * |" in printed


def test_report_files_written(
    core: Settings, tmp_path: Path, linq_tails: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    video = _textured(tmp_path / "demo.mp4")  # auto scene: demo, yellow running and red fall
    expected = [{"scenario": "fall", "start_s": 0.0, "end_s": 20.0}]
    labels = labels_file(tmp_path, {"videos": [{"path": str(video), "expected": expected}]})
    fake = shell(monkeypatch)
    report = services.eval_run(labels)
    # Default folder: eval/<YYYYMMDD-HHMMSS>/ under data_dir (tech.md 5.3).
    out = Path(report.out_dir)
    assert out.parent == core.data_dir / "eval" and len(out.name) == len("20261024-090000")
    assert EvalReport.model_validate(json.loads((out / "report.json").read_text("utf-8"))) == report
    md = (out / "report.md").read_text("utf-8")
    assert "| сценарий |" in md and "| * |" in md
    assert "recall валиден только при полной разметке видео" in md
    assert report.hours == pytest.approx(20 / 3600, rel=0.01)
    assert report.deadline_s == core.eval.deadline_s
    assert row(report.rows, "running").episodes > 0
    assert row(report.rows, "fall").expected == 1
    starts = fake.calls.count("start")
    assert starts > 0
    # Second run: artifacts come from the cache, the fake starts no worker.
    services.eval_run(labels, tmp_path / "again")
    assert fake.calls.count("start") == starts
    # Key eval.deadline_s: the whole label is in time with 20 s, nothing with 0.001 s.
    _tune(monkeypatch, core, eval={"deadline_s": 20.0})
    wide = services.eval_run(labels, tmp_path / "wide")
    assert (row(wide.rows, "fall").tp, row(wide.rows, "fall").fn) == (1, 0)
    _tune(monkeypatch, core, eval={"deadline_s": 0.001})
    tight = services.eval_run(labels, tmp_path / "tight")
    assert tight.deadline_s == 0.001
    assert (row(tight.rows, "fall").tp, row(tight.rows, "fall").fn) == (0, 1)
    # camera_id brings the rules of that camera: running off, no running episodes.
    camera_id = _camera()
    services.camera_rule_set(camera_id, "running", CameraRuleIn(enabled=False), "admin")
    on_camera = {"videos": [{"path": str(video), "camera_id": camera_id, "expected": expected}]}
    report = services.eval_run(labels_file(tmp_path, on_camera, "cam.yaml"), tmp_path / "cam")
    assert all(r.scenario != "running" for r in report.rows)
    assert row(report.rows, "fall").tp == 0  # deadline still 0.001


def test_eval_refuses_running_server(
    core: Settings, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Debt S14: a live server owns the database; a reused pid of server.pid is not one."""
    me = psutil.Process()
    pid_file = core.data_dir / "server.pid"
    pid_file.write_text(json.dumps({"pid": me.pid, "create_time": me.create_time()}), "utf-8")
    assert cli.main(["eval", str(tmp_path / "missing.yaml")]) == 5
    assert "Остановите сервер: uv run safewatch stop" in capsys.readouterr().err
    pid_file.write_text(json.dumps({"pid": me.pid, "create_time": 1.0}), "utf-8")
    assert cli.main(["eval", str(tmp_path / "missing.yaml")]) == 3  # went on to the labels


def test_eval_pose_fallback(
    core: Settings, tmp_path: Path, linq_tails: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Debt S14: pose remote_error in eval → the analysis without keypoints, like a job."""
    video = _textured(tmp_path / "demo.mp4")
    expected = [{"scenario": "fall", "start_s": 0.0, "end_s": 20.0}]
    labels = labels_file(tmp_path, {"videos": [{"path": str(video), "expected": expected}]})
    fake = shell(monkeypatch, [None, "remote_error"])  # detector fine, pose stops
    report = services.eval_run(labels, tmp_path / "out")
    assert fake.calls.count("start") == 2
    tasks = [r["task"] for r in store.all("SELECT task FROM artifacts")]
    assert tasks == ["detect"]  # no keypoints were stored
    assert row(report.rows, "running").episodes > 0
    assert (tmp_path / "out" / "report.md").is_file()


def test_eval_extra_fallback(
    core: Settings, tmp_path: Path, extra_registry: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """R30: an extra model failing in eval → the analysis without it, like a job (8.30 item 10)."""
    _tune(monkeypatch, core, pipeline={"extra": ["fire-test@1"]})
    video = _textured(tmp_path / "demo.mp4")
    expected = [{"scenario": "fall", "start_s": 0.0, "end_s": 20.0}]
    labels = labels_file(tmp_path, {"videos": [{"path": str(video), "expected": expected}]})
    fake = shell(monkeypatch, [None, "remote_error", None])  # only the extra model stops
    report = services.eval_run(labels, tmp_path / "out")
    assert fake.calls.count("start") == 3  # detector, extra, pose
    models = [r["model_id"] for r in store.all("SELECT model_id FROM artifacts ORDER BY id")]
    assert models == ["det-yolov8n", "pose-yolov8n"]
    assert row(report.rows, "running").episodes > 0
