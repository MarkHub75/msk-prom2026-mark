"""Slices 2 and 28: LinqBackend commands (6.1, 8.29), JSONL checks (5.3), JupyterShell errors."""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
import requests
from fastapi.testclient import TestClient

from safewatch import doctor, registry, services, texts
from safewatch.api import create_app
from safewatch.config import Settings
from safewatch.errors import InferenceError
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.hub import hub
from safewatch.inference import linq
from safewatch.inference.artifacts import read_jsonl
from safewatch.inference.linq import JupyterShell, LinqBackend
from safewatch.types import CameraIn, Job, SectorIn


class RecordingShell(FakeRemoteShell):
    """The fake, plus every command and upload target, to check what LinqBackend sends."""

    def __init__(self) -> None:
        super().__init__()
        self.commands: list[str] = []
        self.uploads: list[str] = []

    def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]:
        self.commands.append(cmd)
        return super().exec(cmd, timeout)

    def upload(self, local: Path, remote: str) -> None:
        self.uploads.append(remote)
        super().upload(local, remote)


def test_commands_use_baseline_dir_and_registry(
    fake_core: Settings, tmp_path: Path, make_video, linq_tails: Path
) -> None:
    shell = RecordingShell()
    backend = LinqBackend(fake_core, shell)
    clip = make_video(tmp_path, 1, 25)
    sha = hashlib.sha256(clip.read_bytes()).hexdigest()
    detector = registry.resolve(fake_core.pipeline.detector)
    pose = registry.resolve(str(fake_core.pipeline.pose))
    out = tmp_path / "artifacts" / f"{'a' * 64}.jsonl"
    metrics = backend.run(clip, sha, detector, 2, out, lambda share: None)
    assert metrics.frames_processed == 13 and out.is_file()
    backend.run(clip, sha, pose, 2, tmp_path / "artifacts" / f"{'b' * 64}.jsonl", lambda s: None)

    starts = [c for c in shell.commands if c.endswith("# sw:start")]
    det, pos = starts
    assert all(r.startswith("baseline/") for r in shell.uploads)
    assert f"baseline/videos/baseline_{sha[:12]}.mp4" in shell.uploads
    assert shell.uploads.count(f"baseline/videos/baseline_{sha[:12]}.mp4") == 1  # size matched
    assert "/work/baseline/out/baseline_aaaaaaaaaaaaaaaa_detect.jsonl" in det
    for cmd, model in ((det, detector), (pos, pose)):
        assert f"--program {model.linq_program}" in cmd
        assert f"--size {model.input_size}" in cmd and "--inflight 4" in cmd
        assert "--conf 0.1" in cmd and f"--tail tails/{Path(str(model.linq_tail)).name}" in cmd
        assert f"--video videos/baseline_{sha[:12]}.mp4" in cmd
    assert "--classes 0,2,5,6,7,67" in det and "--classes" not in pos
    assert "--task pose" in pos
    assert not any("mosprom_work" in c for c in shell.commands + shell.uploads)
    summary = json.loads((out.parent / f"{out.stem}.summary.json").read_text(encoding="utf-8"))
    assert summary["end_to_end_s"] >= 0


LINE = {"frame_idx": 0, "ts_ms": 0.0, "detections": []}


@pytest.mark.parametrize(
    ("lines", "expected", "ok"),
    [
        ([LINE, LINE | {"frame_idx": 2}], 2, True),
        ([LINE, LINE | {"frame_idx": 2}], None, True),
        (["not json"], None, False),
        ([{"frame_idx": 0, "ts_ms": 0.0}], None, False),
        ([LINE, LINE], None, False),
        ([LINE | {"frame_idx": 3}, LINE | {"frame_idx": 2}], None, False),
        ([LINE, LINE | {"frame_idx": 2}], 3, False),
        ([LINE, LINE | {"frame_idx": 2}], 1, False),
    ],
)
def test_jsonl_validation_rows(
    tmp_path: Path, lines: list[object], expected: int | None, ok: bool
) -> None:
    path = tmp_path / "a.jsonl"
    text = "".join((x if isinstance(x, str) else json.dumps(x)) + "\n" for x in lines)
    path.write_text(text, encoding="utf-8")
    if ok:
        assert [f.frame_idx for f in read_jsonl(path, expected)] == [0, 2]
    else:
        with pytest.raises(InferenceError) as info:
            read_jsonl(path, expected)
        assert info.value.code == "bad_output"


class JupyterError(RuntimeError):
    pass


def _module(error: Exception, on: str) -> SimpleNamespace:
    class Remote:
        def __init__(self, *args: object) -> None:
            if on == "login":
                raise error

        def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]:
            raise error

    return SimpleNamespace(JupyterRemote=Remote, JupyterError=JupyterError)


@pytest.mark.parametrize(
    ("error", "on", "code"),
    [
        (requests.ConnectionError("refused s3cret-pw"), "login", "linq_unavailable"),
        (JupyterError("JupyterHub login rejected s3cret-pw"), "login", "linq_unavailable"),
        (requests.Timeout("read timed out"), "exec", "linq_unavailable"),
        (JupyterError("timeout after 5 s (kernel interrupted)"), "exec", "timeout"),
    ],
)
def test_jupyter_shell_maps_errors(
    core: Settings,
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
    on: str,
    code: str,
) -> None:
    settings = core.model_copy(update={"linq_jupyter_password": "s3cret-pw"})
    monkeypatch.setattr(linq, "_load_module", lambda path: _module(error, on))
    with pytest.raises(InferenceError) as info:
        JupyterShell(settings).exec("echo ok  # sw:check", timeout=5)
    assert info.value.code == code
    assert "s3cret-pw" not in str(info.value)


def test_jupyter_shell_starts_fresh_session_after_network_error(
    core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    made: list[object] = []

    class Remote:
        def __init__(self, *args: object) -> None:
            made.append(self)

        def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]:
            raise requests.ConnectionError("tunnel down")

        def shutdown_kernel(self) -> None:
            raise requests.ConnectionError("tunnel down")

    module = SimpleNamespace(JupyterRemote=Remote, JupyterError=JupyterError)
    monkeypatch.setattr(linq, "_load_module", lambda path: module)
    shell = JupyterShell(core)
    for _ in range(2):
        with pytest.raises(InferenceError):
            shell.exec("echo ok  # sw:check", timeout=5)
    assert len(made) == 2


# --- slice 28: the slow queue of the platform (tech.md 8.29) ------------------------------
def test_job_timeout_scales_with_frames(core: Settings) -> None:
    cfg = core.linq
    assert (cfg.inflight, cfg.slow_rtt_s, cfg.job_timeout_s) == (4, 12.0, 1800)
    assert linq.job_timeout_s(cfg, 720) == 2280  # 120 + 180 batches x 12 s
    assert linq.job_timeout_s(cfg, 10) == 1800  # a short clip keeps job_timeout_s
    slower = cfg.model_copy(update={"slow_rtt_s": 20.0})
    assert linq.job_timeout_s(slower, 720) == 120 + 180 * 20


def _worker_timeouts(
    monkeypatch: pytest.MonkeyPatch, clip: Path, out: Path, *extra: str
) -> list[float]:
    """Runs video_worker.main() with a stub TPU client; the `timeout` of every `collect`."""
    seen: list[float] = []
    yolo = SimpleNamespace(
        preprocess=lambda img, size: (np.zeros((1, 3, 8, 8), np.float32), None),
        postprocess=lambda *args, **kw: [],
    )
    reply = SimpleNamespace(ok=True, rtt_s=0.01, outputs={"y": np.zeros(1)}, worker={})

    class Client:
        def __enter__(self) -> "Client":
            return self

        def __exit__(self, *exc: object) -> None:
            return None

        def input_queue_info(self) -> dict[str, int]:
            return {}

        def submit(self, program: str, inputs: object) -> str:
            return "id"

        def collect(self, ids: list[str], timeout: float) -> list[object]:
            seen.append(timeout)
            return [reply]

    tpu = SimpleNamespace(TpuClient=Client, program_uri=lambda p: p)
    monkeypatch.setitem(sys.modules, "yolo_io", yolo)
    monkeypatch.setitem(sys.modules, "linq_tpu", tpu)
    path = Path(__file__).parents[1] / "tools/linq/remote/video_worker.py"
    spec = importlib.util.spec_from_file_location("baseline_video_worker", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    argv = ["video_worker.py", "--video", str(clip), "--program", "p.tpu", "--out", str(out)]
    monkeypatch.setattr(sys, "argv", [*argv, "--step", "10", *extra])
    module.main()
    return seen


def test_reply_timeout_passed(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shell = RecordingShell()
    clip = make_video(tmp_path, 1, 25)
    sha = hashlib.sha256(clip.read_bytes()).hexdigest()
    detector = registry.resolve(fake_core.pipeline.detector)
    LinqBackend(fake_core, shell).run(clip, sha, detector, 2, tmp_path / "a.jsonl", lambda s: None)
    (start,) = [c for c in shell.commands if c.endswith("# sw:start")]
    assert "--inflight 4 --reply-timeout 120 " in start

    out = tmp_path / "out.jsonl"
    assert set(_worker_timeouts(monkeypatch, clip, out, "--reply-timeout", "7.5")) == {7.5}
    assert set(_worker_timeouts(monkeypatch, clip, out)) == {120}


def test_start_kills_previous_worker(
    fake_core: Settings, tmp_path: Path, make_video, linq_tails: Path
) -> None:
    shell = RecordingShell()
    clip = make_video(tmp_path, 1, 25)
    sha = hashlib.sha256(clip.read_bytes()).hexdigest()
    detector = registry.resolve(fake_core.pipeline.detector)
    LinqBackend(fake_core, shell).run(clip, sha, detector, 2, tmp_path / "a.jsonl", lambda s: None)
    (start,) = [c for c in shell.commands if c.endswith("# sw:start")]
    pid = "/home/jovyan/work/baseline/out/baseline_a_detect.jsonl.pid"
    stop = f"{{ [ -f {pid} ] && kill $(cat {pid}) 2>/dev/null; rm -f {pid}; }} && "
    assert stop in start
    assert start.index(stop) < start.index(".progress") < start.index("(setsid nohup")
    assert start.endswith(f"echo $! > {pid}) && echo started  # sw:start")


class SlowQueueShell(FakeRemoteShell):
    """The fake whose worker answers 0, then 120 of 720 frames (step 2) before it finishes."""

    def __init__(self) -> None:
        super().__init__()
        self.polls = 0

    def _poll(self, cmd: str) -> str:
        self.polls += 1
        if self.polls == 1:
            return '{"done": 0, "n_total": 1440}\nRUNNING\n'
        if self.polls == 2:
            return '{"done": 120, "n_total": 1440}\nRUNNING\n'
        return super()._poll(cmd)


async def test_eta_and_rate_text(
    fake_core: Settings,
    tmp_path: Path,
    make_video,
    linq_tails: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert linq.rate_eta(120, 720, 40.0) == (3.0, 200.0)
    assert linq.rate_eta(0, 720, 40.0) == (None, None)
    wait = "LinQ: ждём первый ответ TPU (очередь площадки)"
    assert texts.job_progress_text(0, 720, None, None) == wait

    now = [0.0]  # the clock of the backend: every poll interval is 40 s
    fake_time = SimpleNamespace(
        perf_counter=lambda: now[0], sleep=lambda s: now.__setitem__(0, now[0] + 40)
    )
    monkeypatch.setattr(linq, "time", fake_time)
    monkeypatch.setattr(services, "_backend", LinqBackend(fake_core, SlowQueueShell()))
    published: list[Job] = []

    def publish(type: str, data: object, audience: object = None) -> None:
        if type == "job.progress" and isinstance(data, Job) and data.status == "running":
            published.append(data)

    monkeypatch.setattr(hub, "publish", publish)
    sector = services.sector_create(SectorIn(name="Цех"), "admin")
    camera = services.camera_create(CameraIn(sector_id=sector.id, name="Камера"), "admin")
    services.video_import(camera.id, make_video(tmp_path, 1, 25))
    job = await services.run_next_job()
    assert job is not None and job.status == "done" and job.eta_s is None

    shown = [
        (j.status_text, j.rate_fps, j.eta_s) for j in published if j.status_text[:5] == "LinQ:"
    ]
    progress = "LinQ: 120 из 720 кадров · 3,0 кадр/с · осталось ~3 мин"
    assert shown[:2] == [(wait, None, None), (progress, 3.0, 200.0)]
    assert services._live == {}


def test_close_shuts_kernel(
    core: Settings, fake_core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    shutdowns: list[int] = []

    class Remote:
        def __init__(self, *args: object) -> None:
            pass

        def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]:
            return 0, "ok\n", ""

        def shutdown_kernel(self) -> None:
            shutdowns.append(1)

    module = SimpleNamespace(JupyterRemote=Remote, JupyterError=JupyterError)
    monkeypatch.setattr(linq, "_load_module", lambda path: module)
    shell = JupyterShell(core)
    shell.close()  # no session yet: nothing to shut
    shell.exec("echo ok  # sw:check", timeout=5)
    shell.close()
    shell.close()
    assert shutdowns == [1]

    fake = FakeRemoteShell()
    monkeypatch.setattr(services, "_backend", LinqBackend(fake_core, fake))
    services.backend_close()
    assert fake.calls == ["close"]


def test_doctor_and_lifespan_close_backend(
    fake_core: Settings, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    closed: list[str] = []
    monkeypatch.setattr(services, "backend_close", lambda: closed.append("close"))
    assert doctor.run(fake_core) == 0
    assert closed == ["close"]
    with TestClient(create_app(fake_core)):
        pass
    assert closed == ["close", "close"]


def test_html_answer_is_bad_answer(core: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    page = JupyterError("POST api/kernels: HTTP 502 <HTML><body>Bad Gateway</body></HTML>")
    monkeypatch.setattr(linq, "_load_module", lambda path: _module(page, "exec"))
    with pytest.raises(InferenceError) as info:
        JupyterShell(core).exec("echo ok  # sw:check", timeout=5)
    assert info.value.code == "bad_output"
    status = LinqBackend(core, JupyterShell(core)).check()
    assert (status.state, status.message) == ("bad_answer", texts.LINQ_BAD_ANSWER)

    not_json = requests.JSONDecodeError("Expecting value", "<!doctype html>", 0)
    monkeypatch.setattr(linq, "_load_module", lambda path: _module(not_json, "exec"))
    with pytest.raises(InferenceError) as info:
        JupyterShell(core).exec("echo ok  # sw:check", timeout=5)
    assert info.value.code == "bad_output"
