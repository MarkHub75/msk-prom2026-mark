"""FakeRemoteShell (tech.md 6.1): LinQ Jupyter in memory, driven by a script of faults.

The entry of the script is taken on `# sw:home`, the command every run starts with; the last
entry repeats, an empty script means `None` for every run. Inputs are checked: a path outside
the baseline folder (tech.md 3.1) or a command without its `# sw:` marker is a bug.
"""

import json
import re
import shlex
from pathlib import Path

import cv2
from pydantic import validate_call

from safewatch import config, registry, store
from safewatch.errors import InferenceError
from safewatch.fakes import scenes
from safewatch.types import Fault, ModelTask

HOME = "/home/jovyan"
REMOTE_ERROR_LOG = "RuntimeError: TPU error frame 0: status -3"
AUTO_SCENES = [
    (("run", "бег"), "running"),
    (("fall", "пад"), "fall"),
    (("phone", "тел"), "phone"),
    (("truck", "car", "погруз"), "vehicle"),
    (("fence", "забор"), "fence"),
    (("dark",), "dark"),
]
MARKER = re.compile(r"#\s*sw:(\w+)\s*$")


def auto_scene(filename: str) -> str:
    name = filename.lower()
    for words, scene in AUTO_SCENES:
        if any(word in name for word in words):
            return scene
    return "demo"


class FakeRemoteShell:
    def __init__(self, script: list[Fault | None] | None = None, scene: str = "auto") -> None:
        self.script = script or []
        self.scene = scene
        self.calls: list[str] = []
        self.files: dict[str, bytes] = {}
        self.sources: dict[str, Path] = {}  # remote video → the local file it came from
        self.runs = 0
        self.fault: Fault | None = None
        self.done = 0  # frames of the last started run
        self.remote_dir = config.get_settings().linq.remote_dir

    def _check_path(self, remote: str) -> str:
        path = remote.removeprefix(f"{HOME}/work/").removeprefix("$HOME/work/")
        if not path.startswith(f"{self.remote_dir}/"):
            raise ValueError(f"fake LinQ: {remote} is outside ~/work/{self.remote_dir}/")
        return path

    def _unavailable(self) -> None:
        if self.fault == "unavailable":
            raise InferenceError("linq_unavailable", "fake: LinQ Jupyter is not reachable")

    @validate_call
    def upload(self, local: Path, remote: str) -> None:
        self._unavailable()
        path = self._check_path(remote)
        self.files[path] = local.read_bytes()
        self.sources[path] = local

    @validate_call
    def download(self, remote: str, local: Path) -> int:
        self._unavailable()
        data = self.files[self._check_path(remote)]
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(data)
        return len(data)

    @validate_call
    def size(self, remote: str) -> int | None:
        self._unavailable()
        data = self.files.get(self._check_path(remote))
        return None if data is None else len(data)

    @validate_call
    def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]:
        match = MARKER.search(cmd)
        if match is None:
            raise ValueError(f"fake LinQ: command without a # sw: marker: {cmd}")
        name = match.group(1)
        if name == "home":
            entry = self.script[min(self.runs, len(self.script) - 1)] if self.script else None
            self.fault = entry
            self.runs += 1
        self.calls.append(name)
        self._unavailable()
        handler = getattr(self, f"_{name}", None)
        if handler is None:
            raise ValueError(f"fake LinQ: unknown command {name}")
        out: str = handler(cmd)
        return 0, out, ""

    def _home(self, cmd: str) -> str:
        return f"{HOME}\n"

    def _start(self, cmd: str) -> str:
        args = shlex.split(cmd.split("(", 1)[1].split(">", 1)[0])
        opts = dict(zip(args[4::2], args[5::2], strict=True))  # after `python video_worker.py`
        video = self.sources[f"{self.remote_dir}/{opts['--video']}"]
        cap = cv2.VideoCapture(str(video))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = float(cap.get(cv2.CAP_PROP_FPS)) or 25.0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        task: ModelTask = "pose" if opts["--task"] == "pose" else "detect"
        # uploads/<sha256><ext> lost the original name; the auto scene needs it. Other files
        # (a demo pack build) keep it: the database is not opened for them.
        found = store.video_filename(video.stem) if video.parent.name == "uploads" else None
        original = found or video.name
        scene = auto_scene(original) if self.scene == "auto" else self.scene
        step = int(opts["--step"])
        frames = scenes.render(scene, width, height, fps, frame_count, step, task)
        if "--nc" in opts:  # an extra model: the scenes hold COCO ids, not its classes
            frames = [f.model_copy(update={"detections": []}) for f in frames]
        jsonl = scenes.to_jsonl(frames)
        if self.fault == "bad_output":
            jsonl += "not json\n"
        out = self._check_path(opts["--out"])
        self.files[out] = jsonl.encode()
        summary = {
            "video": video.name,
            "program": opts["--program"],
            "size": int(opts["--size"]),
            "step": step,
            "fps_video": fps,
            "frames_total": frame_count,
            "frames_processed": len(frames),
            "wall_s": 1.0,
            "throughput_fps": float(len(frames)),
            "per_frame_ms": {
                "preprocess": 1.0,
                "postprocess": 1.0,
                "tpu_rtt_median": 10.0,
                "tpu_rtt_p90": 12.0,
            },
            "inflight": int(opts["--inflight"]),
        }
        self.files[out + ".summary.json"] = json.dumps(summary).encode()
        self.done = len(frames)
        return "started\n"

    def _poll(self, cmd: str) -> str:
        if self.fault == "timeout":
            return '{"done": 0}\nRUNNING\n'
        if self.fault == "remote_error":
            return json.dumps({"done": self.done}) + "\nSTOPPED\n"
        return json.dumps({"done": self.done, "finished": True}) + "\nSTOPPED\n"

    def _log(self, cmd: str) -> str:
        return REMOTE_ERROR_LOG + "\n" if self.fault == "remote_error" else "done\n"

    def _kill(self, cmd: str) -> str:
        return "killed\n"

    def _check(self, cmd: str) -> str:
        return "ok\n"

    def _ls(self, cmd: str) -> str:
        models = registry.load_models(registry.MODELS_FILE)
        return "".join(f"{m.linq_program}\n" for m in models if m.linq_program)
