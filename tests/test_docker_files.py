from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _service() -> dict:
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    return compose["services"]["safewatch"]


def test_compose_mounts_demo_and_data() -> None:
    service = _service()
    assert "./data/app:/app/data/app" in service["volumes"]
    assert "./data/demo:/app/data/demo:ro" in service["volumes"]
    assert "./models:/app/models:ro" in service["volumes"]
    assert "8000:8000" in service["ports"]
    lines = (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
    for pattern in ("data/", ".env", ".env.*", "models/"):
        assert pattern in lines
    # The exception works only after the directory it reopens.
    assert lines.index("!data/demo/README.md") > lines.index("data/")


def test_image_starts_with_seed_and_health() -> None:
    cmd = next(
        line
        for line in (ROOT / "Dockerfile").read_text(encoding="utf-8").splitlines()
        if line.startswith("CMD ")
    )
    assert '"serve"' in cmd and '"--seed"' in cmd and '"0.0.0.0"' in cmd
    check = " ".join(_service()["healthcheck"]["test"])
    assert check.startswith("CMD python ") and "/api/health" in check
