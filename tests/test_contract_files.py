import importlib.util
import json
import re
import shutil
import subprocess
from pathlib import Path
from types import ModuleType
from typing import get_args

import pytest
from pydantic import BaseModel, TypeAdapter

from safewatch import cli, texts, types
from safewatch.api import CONTRACT_VERSION, create_app
from safewatch.config import Settings
from safewatch.types import WsMessage, WsType

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contract"


def _load(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "core.autocrlf=false", *args], cwd=repo, check=True)


def test_eol_check_flags_crlf(tmp_path: Path) -> None:
    eol = _load("eol_check")
    _git(tmp_path, "init", "-q")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "good.py").write_bytes(b"x = 1\n")
    (tmp_path / "notes.txt").write_bytes(b"research\r\nfile\r\n")  # outside app paths
    _git(tmp_path, "add", ".")
    assert eol.main(["--root", str(tmp_path)]) == 0
    (tmp_path / "src" / "bad.py").write_bytes(b"x = 1\r\n")
    _git(tmp_path, "add", ".")
    assert eol.crlf_files(tmp_path) == ["src/bad.py"]
    assert eol.main(["--root", str(tmp_path)]) == 1


def test_openapi_matches_app(settings: Settings) -> None:
    on_disk = json.loads((CONTRACT / "openapi.json").read_text(encoding="utf-8"))
    assert on_disk == create_app(settings).openapi()
    assert on_disk["info"]["version"] == CONTRACT_VERSION == "1.1.0"


def test_openapi_only_grows() -> None:
    # Egor's frontend is built on 1.0.0: nothing of it is removed or renamed (tech.md 10.3).
    old = json.loads((CONTRACT / "openapi.1.0.0.json").read_text(encoding="utf-8"))
    new = json.loads((CONTRACT / "openapi.json").read_text(encoding="utf-8"))
    missing = [
        f"{method} {path}"
        for path, methods in old["paths"].items()
        for method in methods
        if method not in new["paths"].get(path, {})
    ]
    schemas = new["components"]["schemas"]
    for name, schema in old["components"]["schemas"].items():
        if name not in schemas:
            missing.append(name)
            continue
        props = schemas[name].get("properties", {})
        missing += [f"{name}.{f}" for f in schema.get("properties", {}) if f not in props]
    assert missing == []
    assert len(new["paths"]) > len(old["paths"])


def test_contract_check_detects_drift(
    core: Settings, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("openapi.json", "ws.schema.json"):
        shutil.copy(CONTRACT / name, tmp_path / name)
    monkeypatch.setattr(cli, "CONTRACT_DIR", tmp_path)
    assert cli.main(["contract", "--check"]) == 0
    # The schema of one model on disk differs from the app, as after an edit of types.py.
    path = tmp_path / "ws.schema.json"
    text = path.read_text(encoding="utf-8").replace('"server_now"', '"now"')
    path.write_text(text, encoding="utf-8", newline="\n")
    assert cli.main(["contract", "--check"]) == 1
    assert cli.main(["contract"]) == 0
    assert cli.main(["contract", "--check"]) == 0


def test_ws_schema_matches_types() -> None:
    on_disk = json.loads((CONTRACT / "ws.schema.json").read_text(encoding="utf-8"))
    assert on_disk == TypeAdapter(WsMessage).json_schema()


def test_ws_examples_cover_every_type() -> None:
    examples = json.loads((CONTRACT / "ws-examples.json").read_text(encoding="utf-8"))
    messages = [WsMessage.model_validate(item) for item in examples]
    assert sorted(m.type for m in messages) == sorted(get_args(WsType))


def test_types_export_contract_names() -> None:
    tech = (ROOT / "tech.md").read_text(encoding="utf-8")
    names = []
    for heading in ("### 5.2", "#### 6.11.2"):
        block = tech.split(heading, 1)[1].split("```python", 1)[1].split("```", 1)[0]
        names += re.findall(r"^class (\w+)", block, re.M) + re.findall(r"^(\w+) = ", block, re.M)
    assert len(names) > 130
    missing = [name for name in names if not hasattr(types, name)]
    assert missing == []


def test_texts_cover_every_literal() -> None:
    assert set(texts.STATUS_TITLES) == set(get_args(types.EventStatus))
    assert set(texts.LEVEL_TITLES) == set(get_args(types.Level))
    assert set(texts.ROLE_TITLES) == set(get_args(types.Role))
    assert set(texts.DEMO_ACTOR) == set(get_args(types.ActorRole))
    assert set(texts.NO_OBSERVATION_TEXTS) == set(get_args(types.NoObservationReason))


V5_FIELDS: dict[type[BaseModel], list[str]] = {
    types.Video: ["web_playable"],
    types.Job: ["status_text", "eta_s", "rate_fps"],
    types.EventSummary: ["clip", "person_name", "person_position", "crew"],
    types.EventDetail: ["can_identify"],
    types.Analysis: ["auto_calibration"],
    types.CameraSetupView: ["auto_calibration"],
    types.PersonState: ["speed_source"],
    types.VehicleState: ["speed_source"],
    types.HudObject: ["projection"],
    types.Delivery: ["delivered_at", "status_text"],
    types.ModelSpec: ["nc", "input_name"],
}  # tech.md 6.11.3


def test_v5_fields_present() -> None:
    without_default = [
        f"{model.__name__}.{name}"
        for model, names in V5_FIELDS.items()
        for name in names
        if name not in model.model_fields or model.model_fields[name].is_required()
    ]
    assert without_default == []
    assert "identified" in get_args(types.LogAction)
    assert get_args(types.Channel.model_fields["kind"].annotation) == ("ws", "webhook", "call")
    # A 1.0.0 event without the v5 fields still passes the model.
    examples = json.loads((CONTRACT / "ws-examples.json").read_text(encoding="utf-8"))
    event = next(item["data"] for item in examples if item["type"] == "event.updated")
    old = {k: v for k, v in event.items() if k not in V5_FIELDS[types.EventSummary]}
    summary = types.EventSummary.model_validate(old)
    assert (summary.clip, summary.person_name, summary.crew) == (None, "", "")
