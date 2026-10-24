"""`safewatch doctor` (tech.md 8.17): what is set up, never the value of a key."""

import asyncio
from dataclasses import dataclass

from safewatch import registry, services
from safewatch.config import ENV_NAMES, ROOT, Settings
from safewatch.db import connect, migrate

SECRET_KEYS = [
    "linq_jupyter_url",
    "linq_jupyter_user",
    "linq_jupyter_password",
    "linq_jupyter_token",
]
TOOLS = ["jupyter_remote.py", "linq_tpu.py", "yolo_io.py", "remote/video_worker.py"]


@dataclass
class Check:
    what: str
    result: str
    ok: bool
    hint: str = ""


def _checks(settings: Settings) -> list[Check]:
    linq = settings.inference_backend == "linq"
    live = linq and not settings.fake
    checks: list[Check] = []
    for key in SECRET_KEYS:
        present = bool(getattr(settings, key))
        # Password and token are alternatives: one of them is enough.
        needed = live and key in ("linq_jupyter_url", "linq_jupyter_user")
        hint = "" if present or not needed else "впишите в .env или включите SAFEWATCH_FAKE=1"
        checks.append(
            Check(ENV_NAMES[key], "есть" if present else "нет", present or not needed, hint)
        )
    if live and not (settings.linq_jupyter_password or settings.linq_jupyter_token):
        checks.append(Check("пароль или токен Jupyter", "нет", False, "LINQ_JUPYTER_PASSWORD"))
    checks.append(Check("INFERENCE_BACKEND", settings.inference_backend, True))
    checks.append(Check("SAFEWATCH_FAKE", "1" if settings.fake else "0", True))
    try:
        models = registry.active_models(settings)
    except ValueError as exc:
        checks.append(Check("реестр моделей", "ошибка", False, str(exc)))
        models = []
    for model in models:
        what = f"модель {model.id}@{model.version}"
        path = model.linq_tail if linq else model.local_onnx
        if linq and settings.fake:
            checks.append(Check(what, "фейк", True))
        elif path is None or not (ROOT / path).is_file():
            checks.append(Check(what, "нет файла", False, path or "нет пути в config/models.yaml"))
        else:
            checks.append(Check(what, "есть", True))
    if linq:
        for name in TOOLS:
            present = (settings.linq.tools_dir / name).is_file()
            checks.append(Check(f"tools/linq/{name}", "есть" if present else "нет", present))
        checks.append(_linq_check(settings))
    try:
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        db = connect(settings.data_dir / "safewatch.db")
        migrate(db)
        db.close()
        checks.append(Check("база", "открывается", True))
    except Exception as exc:  # any failure here is the answer of the check
        checks.append(Check("база", "ошибка", False, type(exc).__name__))
    return checks


def _linq_check(settings: Settings) -> Check:
    if settings.fake:
        return Check("связь с LinQ", "фейк", True)
    if not (settings.linq_jupyter_url and settings.linq_jupyter_user):
        return Check("связь с LinQ", "нет ключей", False, "LINQ_JUPYTER_URL, LINQ_JUPYTER_USER")
    status = asyncio.run(services.backend_check(force=True))
    return Check("связь с LinQ", status.state, status.state == "ok", status.message)


def run(settings: Settings) -> int:
    try:
        checks = _checks(settings)
    finally:
        services.backend_close()  # the kernel of the check leaves the shared account (8.29)
    for check in checks:
        mark = "ok  " if check.ok else "FAIL"
        hint = f" — {check.hint}" if check.hint else ""
        print(f"{mark} {check.what}: {check.result}{hint}")
    return 0 if all(check.ok for check in checks) else 4
