import json
from pathlib import Path

import pytest

from safewatch.errors import InferenceError
from safewatch.fakes import scenes
from safewatch.fakes.remote import FakeRemoteShell, auto_scene
from safewatch.types import Fault, FrameDetections

OUT = "$HOME/work/baseline/out/baseline_0123456789abcdef_detect.jsonl"


def _start(video: str) -> str:
    return (
        "mkdir -p $HOME/work/baseline/out && cd $HOME/work/baseline && rm -f x.progress && "
        f"(setsid nohup python video_worker.py --video videos/{video} --program p.tpu --out {OUT} "
        "--size 640 --step 2 --task detect --conf 0.1 --iou 0.45 --inflight 4 --classes 0,67 "
        f"--tail tails/t.onnx > {OUT}.log 2>&1 < /dev/null & echo $! > {OUT}.pid) "
        "&& echo started  # sw:start"
    )


def _run(shell: FakeRemoteShell, video: Path) -> tuple[str, str]:
    """One run in the order of LinqBackend (tech.md 6.1): home, upload, start, poll."""
    shell.exec("echo $HOME  # sw:home", 60.0)
    shell.upload(video, f"baseline/videos/{video.name}")
    shell.exec(_start(video.name), 60.0)
    _, poll, _ = shell.exec("cat x.progress; echo; kill -0 1 && echo RUNNING  # sw:poll", 60.0)
    _, log, _ = shell.exec("tail -30 x.log  # sw:log", 60.0)
    return poll, log


@pytest.mark.parametrize("fault", [None, "unavailable", "timeout", "remote_error", "bad_output"])
def test_fake_remote_faults(fault: Fault | None, tmp_path: Path, make_video, fake_core) -> None:
    video = make_video(tmp_path, 2.0, 10.0, name="fall_01.mp4")
    shell = FakeRemoteShell([fault])
    if fault == "unavailable":
        with pytest.raises(InferenceError) as error:
            shell.exec("echo $HOME  # sw:home", 60.0)
        assert error.value.code == "linq_unavailable"
        with pytest.raises(InferenceError):
            shell.upload(video, f"baseline/videos/{video.name}")
        return
    poll, log = _run(shell, video)
    progress, state = poll.strip().split("\n")
    jsonl = tmp_path / "out.jsonl"
    shell.download(OUT.removeprefix("$HOME/work/"), jsonl)
    lines = jsonl.read_text(encoding="utf-8").splitlines()
    summary = json.loads(shell.files[OUT.removeprefix("$HOME/work/") + ".summary.json"])
    if fault is None:
        assert json.loads(progress) == {"done": 10, "finished": True}
        assert state == "STOPPED"
        assert summary["frames_processed"] == len(lines) == 10
        assert [FrameDetections.model_validate_json(line).frame_idx for line in lines[:2]] == [0, 2]
    if fault == "timeout":
        assert (json.loads(progress), state) == ({"done": 0}, "RUNNING")
        assert shell.exec("kill 1  # sw:kill", 60.0)[1] == "killed\n"
    if fault == "remote_error":
        assert "finished" not in json.loads(progress) and state == "STOPPED"
        assert "status -3" in log
    if fault == "bad_output":
        assert json.loads(progress)["finished"] is True
        assert lines[-1] == "not json"
    assert shell.calls[:3] == ["home", "start", "poll"]


def test_fake_script_repeats_last_entry(tmp_path: Path, make_video, fake_core) -> None:
    video = make_video(tmp_path, 1.0, 10.0)
    shell = FakeRemoteShell([None, "timeout"])
    assert '"finished": true' in _run(shell, video)[0]
    assert "RUNNING" in _run(shell, video)[0]
    assert "RUNNING" in _run(shell, video)[0]


def test_fake_checks_inputs(tmp_path: Path, fake_core) -> None:
    shell = FakeRemoteShell()
    with pytest.raises(ValueError, match="outside"):
        shell.size("mosprom_work/videos/x.mp4")
    with pytest.raises(ValueError, match="marker"):
        shell.exec("ls", 60.0)
    assert shell.exec("echo ok  # sw:check", 60.0)[1] == "ok\n"
    assert "mosprom_pose640_cut_ap9999_b1_o1_h1m.tpu" in shell.exec("ls -1 x  # sw:ls", 60.0)[1]


@pytest.mark.parametrize(
    ("name", "scene"),
    [("run_1.mp4", "running"), ("бег.mp4", "running"), ("Падение.mp4", "fall"),
     ("phone.mp4", "phone"), ("погрузчик.mp4", "vehicle"), ("забор.mp4", "fence"),
     ("dark.mp4", "dark"), ("clip.mp4", "demo")],
)  # fmt: skip
def test_auto_scene_by_file_name(name: str, scene: str) -> None:
    assert auto_scene(name) == scene


@pytest.mark.parametrize("scene", scenes.SCENES)
def test_scenes_are_valid_and_deterministic(scene: str) -> None:
    def render(seed: int, task: str = "detect") -> str:
        return scenes.to_jsonl(scenes.render(scene, 1280, 720, 25.0, 250, 2, task, seed))  # type: ignore[arg-type]

    text = render(0)
    lines = text.splitlines()
    assert len(lines) == 125
    frames = [FrameDetections.model_validate_json(line) for line in lines]
    assert [f.frame_idx for f in frames[:3]] == [0, 2, 4]
    assert render(0) == text
    pose = [FrameDetections.model_validate_json(line) for line in render(0, "pose").splitlines()]
    if scene in ("dark", "empty"):
        assert all(not f.detections for f in frames)
        return
    assert render(1) != text
    people = [d for f in pose for d in f.detections]
    assert people and all(d.kpts is not None and len(d.kpts) == 17 for d in people)
