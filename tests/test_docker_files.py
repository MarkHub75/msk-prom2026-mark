from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _service() -> dict:
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    return compose["services"]["safewatch"]


def test_compose_mounts_demo_and_data() -> None:
    service = _service()
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    # SQLite must use a declared named volume, never a Windows host directory.
    data_mounts = [
        mount
        for mount in service["volumes"]
        if isinstance(mount, str) and mount.split(":")[1] == "/app/data/app"
    ]
    assert len(data_mounts) == 1
    source, target = data_mounts[0].split(":")
    assert target == "/app/data/app"
    assert source in compose["volumes"]
    assert not any(char in source for char in ("/", "\\", "."))
    assert not compose["volumes"][source].get("driver_opts")  # no disguised bind volume
    assert not any(
        isinstance(mount, dict) and mount.get("target") == "/app/data/app"
        for mount in service["volumes"]
    )
    assert "./data/demo:/app/data/demo:ro" in service["volumes"]
    assert "./models:/app/models:ro" in service["volumes"]
    assert "8000:8000" in service["ports"]
    lines = (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
    for pattern in ("data/", ".env", ".env.*", "models/"):
        assert pattern in lines
    # The exception works only after the directory it reopens.
    assert lines.index("!data/demo/README.md") > lines.index("data/")


def test_user_config_is_mounted_not_baked_and_env_keeps_priority() -> None:
    service = _service()
    mounts = [m for m in service["volumes"] if isinstance(m, dict)]
    config = next(m for m in mounts if m["target"] == "/app/config/user.yaml")
    assert config["type"] == "bind" and config["source"] == "./config/user.yaml"
    assert config["read_only"] and config["bind"]["create_host_path"] is False
    ignored = (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
    assert "config/user.yaml" in ignored
    assert "**/.env" in ignored and "**/.env.*" in ignored
    assert "LINQ_JUPYTER_URL" not in service.get("environment", {})
    assert service["env_file"] == [{"path": ".env", "required": False}]


def test_image_starts_with_seed_and_health() -> None:
    cmd = next(
        line
        for line in (ROOT / "Dockerfile").read_text(encoding="utf-8").splitlines()
        if line.startswith("CMD ")
    )
    assert '"serve"' in cmd and '"--seed"' in cmd and '"0.0.0.0"' in cmd
    check = " ".join(_service()["healthcheck"]["test"])
    assert check.startswith("CMD python ") and "/api/health" in check
