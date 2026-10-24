"""Slice 2, criterion 17: one real run on LinQ through the tunnel (`uv run poe live`)."""

import json
import sqlite3
from pathlib import Path

import pytest
import requests
from dotenv import dotenv_values

from safewatch import cli, config, services
from safewatch.config import ENV_NAMES, ROOT, get_settings
from safewatch.types import CameraIn, SectorIn

CLIP = ROOT / "data" / "videos" / "synthetic_coco_40x1s.mp4"


@pytest.mark.live
@pytest.mark.timeout(900)
async def test_linq_processes_short_clip(
    conn: sqlite3.Connection,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # conftest hides .env from tests; the live run needs the LinQ keys, never prints them.
    env = dotenv_values(ROOT / ".env")
    keys = {f: env[n] for f, n in ENV_NAMES.items() if n.startswith("LINQ_") and env.get(n)}
    if not keys.get("linq_jupyter_url") or not CLIP.is_file():
        pytest.skip("no LINQ_JUPYTER_URL or no clip")
    try:
        requests.get(str(keys["linq_jupyter_url"]), timeout=10, allow_redirects=False)
    except requests.RequestException:
        pytest.skip("LinQ tunnel is down")
    update = {**keys, "data_dir": tmp_path, "fake": False, "inference_backend": "linq"}
    settings = get_settings().model_copy(update=update)
    monkeypatch.setattr(config, "get_settings", lambda: settings)

    sector = services.sector_create(SectorIn(name="Живой прогон"), "admin")
    camera = services.camera_create(CameraIn(sector_id=sector.id, name="LinQ"), "admin")
    assert cli.main(["import", str(CLIP), "--camera", str(camera.id)]) == 0
    job = await services.run_next_job()
    assert job is not None
    assert (job.status, job.error_code) == ("done", None), job.error_text
    assert [m.task for m in job.metrics] == ["detect", "pose"]
    with capsys.disabled():
        for m in job.metrics:
            print(json.dumps(m.model_dump(mode="json"), ensure_ascii=False))
