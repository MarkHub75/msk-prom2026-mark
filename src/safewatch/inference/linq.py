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

from safewatch import clock, media, registry, texts
from safewatch.config import ROOT, LinqConfig, Settings
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
START_S = 120  # worker start and the first in-flight batch (tech.md 8.29)


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("jupyter_remote", path)
    if spec is None or spec.loader is None:
        raise InferenceError("linq_unavailable", f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def job_timeout_s(linq: LinqConfig, frames: int) -> float:
    """The whole run (tech.md 8.29): a slow queue answers `inflight` frames per `slow_rtt_s`."""
    return max(linq.job_timeout_s, START_S + math.ceil(frames / linq.inflight) * linq.slow_rtt_s)


def rate_eta(done: int, total: int, elapsed_s: float) -> tuple[float | None, float | None]:
    """`Job.rate_fps` and `Job.eta_s` from frames done since `# sw:start`; none before an answer."""
    if done <= 0 or elapsed_s <= 0:
        return None, None
    rate = done / elapsed_s
    return round(rate, 2), round(max(0, total - done) / rate, 1)


def _html(exc: Exception) -> bool:
    """Jupyter answered with a web page (a proxy or login page) instead of its API (R5)."""
    return isinstance(exc, requests.JSONDecodeError) or "<html" in str(exc).lower()


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
            if isinstance(exc, (*jupyter, requests.JSONDecodeError)) and _html(exc):
                self._drop()
                raise InferenceError("bad_output", self._clean(str(exc))) from None
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

    def close(self) -> None:
        """Shut the kernel of this process on the shared account (tech.md 8.29); again: no-op."""
        self._drop()

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
        # (done, total, seconds since `# sw:start`) of the model running now; services reads it
        # in the progress callback for `Job.rate_fps`, `eta_s` and `status_text` (tech.md 8.29).
        self.live: tuple[int, int, float] | None = None

    def close(self) -> None:
        self.shell.close()

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
        args += ["--inflight", str(linq.inflight), "--reply-timeout", f"{linq.reply_timeout_s:g}"]
        if f"{model.id}@{model.version}" in self.settings.pipeline.extra:
            args += ["--nc", str(len(model.classes))]  # an extra model keeps all its classes
        elif model.task == "detect":
            args += ["--classes", ",".join(str(c) for c in model.classes)]
        args += ["--tail", f"tails/{tail.name}"]
        probe = media.probe_video(video)
        frames_total = math.ceil((probe.frame_count if probe else 0) / step)
        self.live = None
        started_out = self._exec(self._start_command(absdir, remote_out, args))
        if "started" not in started_out:
            raise InferenceError("remote_error", started_out.strip()[-300:])

        self._wait(remote_out, step, started, frames_total, progress)
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

    @staticmethod
    def _start_command(absdir: str, remote_out: str, args: list[str]) -> str:
        """`# sw:start`: a worker left on the same `<out>` is stopped first (tech.md 8.29)."""
        worker = " ".join(shlex.quote(a) for a in args)
        pid = f"{remote_out}.pid"
        return (
            f"mkdir -p {absdir}/out && cd {absdir} && "
            f"{{ [ -f {pid} ] && kill $(cat {pid}) 2>/dev/null; rm -f {pid}; }} && "
            f"rm -f {remote_out}.progress && "
            f"(setsid nohup {worker} > {remote_out}.log 2>&1 < /dev/null & "
            f"echo $! > {pid}) && echo started  # sw:start"
        )

    def _wait(
        self,
        remote_out: str,
        step: int,
        started: float,
        frames_total: int,
        progress: Callable[[float], None],
    ) -> None:
        """Poll the detached worker until it finishes, stops or runs out of time."""
        linq = self.settings.linq
        limit_s = job_timeout_s(linq, frames_total)
        worker_started = time.perf_counter()
        while True:
            if time.perf_counter() - started > limit_s:
                self._exec(f"kill $(cat {remote_out}.pid) 2>/dev/null; echo killed  # sw:kill")
                raise InferenceError("timeout", f"no result in {limit_s:g} s")
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
            total = math.ceil(info["n_total"] / step) if info.get("n_total") else frames_total
            done = int(info.get("done", 0))
            self.live = (done, total, time.perf_counter() - worker_started)
            progress(min(1.0, done / total) if total else 0.0)
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
        except InferenceError as exc:
            if exc.code == "bad_output":  # a web page instead of the Jupyter API (tech.md 8.29)
                return _finish(status, "bad_answer", texts.LINQ_BAD_ANSWER)
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
