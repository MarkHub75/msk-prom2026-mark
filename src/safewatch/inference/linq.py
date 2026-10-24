"""LinQ Jupyter: the shell over `tools/linq/jupyter_remote.py` and the backend (tech.md 6.1).

Blocking: `services` calls `LinqBackend.run` through `asyncio.to_thread`; nothing here writes
to the database.
"""

import contextlib
import importlib.util
import json
import math
import shlex
import time
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import requests
import websocket

from safewatch import clock, registry, texts
from safewatch.config import ROOT, Settings
from safewatch.errors import InferenceError
from safewatch.inference.artifacts import read_jsonl
from safewatch.types import (
    BackendName,
    BackendState,
    BackendStatus,
    InferenceMetrics,
    JobErrorCode,
    ModelSpec,
    RemoteShell,
)

WORKER_FILES = ("linq_tpu.py", "yolo_io.py", "remote/video_worker.py")


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("jupyter_remote", path)
    if spec is None or spec.loader is None:
        raise InferenceError("linq_unavailable", f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class JupyterShell:  # RemoteShell over JupyterRemote from tools/linq/jupyter_remote.py
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._remote: Any = None
        self._module: ModuleType | None = None

    def _clean(self, text: str) -> str:
        for secret in (self.settings.linq_jupyter_password, self.settings.linq_jupyter_token):
            if secret:
                text = text.replace(secret, "***")
        return text[:300]

    def _call(self, fn: Callable[[Any], Any]) -> Any:
        """Run `fn(JupyterRemote)`; network and Jupyter failures become `InferenceError`."""
        try:
            if self._module is None:
                self._module = _load_module(self.settings.linq.tools_dir / "jupyter_remote.py")
            if self._remote is None:
                s = self.settings
                self._remote = self._module.JupyterRemote(
                    s.linq_jupyter_url,
                    s.linq_jupyter_user,
                    s.linq_jupyter_password,
                    s.linq_jupyter_token or None,
                )
            return fn(self._remote)
        except InferenceError:
            raise
        except Exception as exc:
            jupyter = (self._module.JupyterError,) if self._module is not None else ()
            if isinstance(exc, jupyter) and str(exc).startswith("timeout after"):
                raise InferenceError("timeout", self._clean(str(exc))) from None
            network = (requests.ConnectionError, requests.Timeout, websocket.WebSocketException)
            if isinstance(exc, (*network, OSError, *jupyter)):
                self._drop()
                raise InferenceError("linq_unavailable", self._clean(str(exc))) from None
            raise

    def _drop(self) -> None:
        """Forget a broken session: the next call logs in and starts a fresh kernel (R5)."""
        remote, self._remote = self._remote, None
        if remote is not None:
            with contextlib.suppress(Exception):  # the old kernel may be gone with the tunnel
                remote.shutdown_kernel()

    def upload(self, local: Path, remote: str) -> None:
        self._call(lambda jr: jr.upload(local, remote, progress=False))

    def download(self, remote: str, local: Path) -> int:
        n: int = self._call(lambda jr: jr.download(remote, local))
        return n

    def exec(self, cmd: str, timeout: float) -> tuple[int, str, str]:
        result: tuple[int, str, str] = self._call(lambda jr: jr.exec(cmd, timeout=timeout))
        return result

    def size(self, remote: str) -> int | None:
        def size(jr: Any) -> int | None:
            try:
                r = jr._api("GET", f"api/contents/{remote}", params={"content": 0})
            except Exception as exc:
                if "HTTP 404" in str(exc):
                    return None
                raise
            return int(r.json()["size"])

        found: int | None = self._call(size)
        return found


class LinqBackend:  # InferenceBackend
    name: BackendName = "linq"

    def __init__(self, settings: Settings, shell: RemoteShell) -> None:
        self.settings = settings
        self.shell = shell

    def _exec(self, cmd: str) -> str:
        rc, out, err = self.shell.exec(cmd, timeout=self.settings.linq.call_timeout_s)
        if rc != 0:
            raise InferenceError("remote_error", (err or out).strip()[-300:])
        return out

    def run(
        self,
        video: Path,
        video_sha256: str,
        model: ModelSpec,
        step: int,
        out: Path,
        progress: Callable[[float], None],
    ) -> InferenceMetrics:
        started = time.perf_counter()
        linq = self.settings.linq
        tail = ROOT / model.linq_tail if model.linq_tail else None
        if tail is None or not tail.is_file() or not model.linq_program:
            raise InferenceError("model_missing", f"{model.id}@{model.version}: no tail or program")
        home = self._exec("echo $HOME  # sw:home").strip()
        rdir = linq.remote_dir
        absdir = f"{home}/work/{rdir}"
        for name in WORKER_FILES:
            self.shell.upload(linq.tools_dir / name, f"{rdir}/{Path(name).name}")
        self.shell.upload(tail, f"{rdir}/tails/{tail.name}")
        upload_started = time.perf_counter()
        video_name = f"{linq.file_prefix}{video_sha256[:12]}{video.suffix.lower()}"
        remote_video = f"{rdir}/videos/{video_name}"
        if self.shell.size(remote_video) != video.stat().st_size:
            self.shell.upload(video, remote_video)
        upload_s = time.perf_counter() - upload_started

        base = f"{linq.file_prefix}{out.stem[:16]}_{model.task}.jsonl"
        remote_out = f"{absdir}/out/{base}"
        args = ["python", "video_worker.py", "--video", f"videos/{video_name}"]
        args += ["--program", model.linq_program, "--out", remote_out]
        args += ["--size", str(model.input_size), "--step", str(step), "--task", model.task]
        args += ["--conf", str(model.conf), "--iou", str(model.iou)]
        args += ["--inflight", str(linq.inflight)]
        if model.task == "detect":
            args += ["--classes", ",".join(str(c) for c in model.classes)]
        args += ["--tail", f"tails/{tail.name}"]
        worker = " ".join(shlex.quote(a) for a in args)
        started_out = self._exec(
            f"mkdir -p {absdir}/out && cd {absdir} && rm -f {remote_out}.progress && "
            f"(setsid nohup {worker} > {remote_out}.log 2>&1 < /dev/null & "
            f"echo $! > {remote_out}.pid) && echo started  # sw:start"
        )
        if "started" not in started_out:
            raise InferenceError("remote_error", started_out.strip()[-300:])

        self._wait(remote_out, step, started, progress)
        self.shell.download(f"{rdir}/out/{base}", out)
        summary_path = out.parent / f"{out.stem}.summary.json"
        self.shell.download(f"{rdir}/out/{base}.summary.json", summary_path)
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            frames = int(summary["frames_processed"])
            per_frame = summary["per_frame_ms"]
        except (ValueError, KeyError, TypeError) as exc:
            raise InferenceError("bad_output", f"summary: {exc}") from None
        read_jsonl(out, expected_frames=frames)
        total_s = time.perf_counter() - started
        summary["end_to_end_s"] = round(total_s, 3)
        summary_path.write_text(json.dumps(summary, indent=1), encoding="utf-8", newline="\n")
        return InferenceMetrics(
            backend="linq",
            fake=self.settings.fake,
            model_id=model.id,
            model_version=model.version,
            task=model.task,
            input_size=model.input_size,
            step=step,
            frames_processed=frames,
            wall_s=float(summary["wall_s"]),
            throughput_fps=float(summary["throughput_fps"] or 0.0),
            preprocess_ms=per_frame.get("preprocess"),
            postprocess_ms=per_frame.get("postprocess"),
            tpu_rtt_p50_ms=per_frame.get("tpu_rtt_median"),
            tpu_rtt_p90_ms=per_frame.get("tpu_rtt_p90"),
            upload_s=round(upload_s, 3),
            total_s=round(total_s, 3),
            cached=False,
        )

    def _wait(
        self, remote_out: str, step: int, started: float, progress: Callable[[float], None]
    ) -> None:
        """Poll the detached worker until it finishes, stops or runs out of time."""
        linq = self.settings.linq
        while True:
            if time.perf_counter() - started > linq.job_timeout_s:
                self._exec(f"kill $(cat {remote_out}.pid) 2>/dev/null; echo killed  # sw:kill")
                raise InferenceError("timeout", f"no result in {linq.job_timeout_s} s")
            out = self._exec(
                f"cat {remote_out}.progress 2>/dev/null; echo; "
                f"kill -0 $(cat {remote_out}.pid) 2>/dev/null && echo RUNNING || echo STOPPED"
                "  # sw:poll"
            )
            lines = [line for line in out.splitlines() if line.strip()]
            state = lines[-1] if lines else ""
            info: dict[str, Any] = {}
            if len(lines) > 1:
                try:
                    info = json.loads(lines[0])
                except ValueError:
                    # The worker rewrites the file in place: a running one may be caught halfway.
                    if state != "STOPPED":
                        time.sleep(linq.poll_interval_s)
                        continue
                    raise InferenceError("bad_output", f".progress: {lines[0][:100]}") from None
            if info.get("finished"):
                progress(1.0)
                return
            if info.get("n_total"):
                progress(min(1.0, info["done"] / math.ceil(info["n_total"] / step)))
            if state == "STOPPED":
                log = self._exec(f"tail -30 {remote_out}.log  # sw:log")
                last = next((x for x in reversed(log.splitlines()) if x.strip()), "stopped")
                code: JobErrorCode = "model_missing" if "not readable" in log else "remote_error"
                raise InferenceError(code, last.strip()[-300:])
            time.sleep(linq.poll_interval_s)

    def check(self) -> BackendStatus:
        """Jupyter answers `ok`, the TPU programs and local tails of active models are there."""
        settings = self.settings
        status = BackendStatus(
            backend="linq",
            fake=settings.fake,
            state="ok",
            checked_at=clock.now(),
            latency_ms=None,
            present=[],
            missing=[],
            message="",
        )
        timeout = settings.linq.call_timeout_s
        started = time.perf_counter()
        try:
            _, answer, _ = self.shell.exec("echo ok  # sw:check", timeout=timeout)
            latency_ms = round((time.perf_counter() - started) * 1000, 1)
            if answer.strip() != "ok":
                return _finish(status, "bad_answer", texts.LINQ_BAD_ANSWER)
            login = settings.linq_jupyter_user.lower()
            programs_dir = settings.linq.programs_dir.format(login=login)
            # A missing folder fails `ls`: then every program is missing, which stdout shows.
            _, listing, _ = self.shell.exec(f"ls -1 {programs_dir}  # sw:ls", timeout=timeout)
        except InferenceError:
            return _finish(status, "unreachable", texts.LINQ_UNREACHABLE)
        found = {line.strip() for line in listing.splitlines()}
        present: list[str] = []
        missing: list[str] = []
        for model in registry.active_models(settings):
            program = model.linq_program or f"{model.id}@{model.version}"
            (present if program in found else missing).append(program)
            if not model.linq_tail or not (ROOT / model.linq_tail).is_file():
                missing.append(model.linq_tail or f"{model.id}@{model.version}: tail")
        status = status.model_copy(
            update={"latency_ms": latency_ms, "present": present, "missing": missing}
        )
        if missing:
            return _finish(status, "models_missing", texts.LINQ_MODELS_MISSING, missing)
        return _finish(status, "ok", texts.LINQ_OK.format(present=len(present), total=len(present)))


def _finish(
    status: BackendStatus, state: BackendState, text: str, names: list[str] | None = None
) -> BackendStatus:
    """The state with its screen text; a fake backend says so first (tech.md 8.14 badge)."""
    if names is not None:
        text = text.format(names=", ".join(names))
    if status.fake:
        text = texts.BACKEND_FAKE.format(text=text)
    return status.model_copy(update={"state": state, "message": text})
