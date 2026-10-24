"""Slice 2: LinqBackend commands (tech.md 6.1), JSONL checks (5.3), JupyterShell errors."""

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import requests

from safewatch import registry
from safewatch.config import Settings
from safewatch.errors import InferenceError
from safewatch.fakes.remote import FakeRemoteShell
from safewatch.inference import linq
from safewatch.inference.artifacts import read_jsonl
from safewatch.inference.linq import JupyterShell, LinqBackend


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
