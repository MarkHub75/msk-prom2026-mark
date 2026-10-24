import shutil
import webbrowser
from collections.abc import Iterator
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from safewatch import config, registry
from safewatch.config import Settings, get_settings


@pytest.fixture
def config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    for name in ("default.yaml", "user.example.yaml"):
        shutil.copy(config.CONFIG_DIR / name, tmp_path / name)
    monkeypatch.setattr(config, "CONFIG_DIR", tmp_path)
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def test_settings_carry_no_keys_and_no_fakes(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert settings.linq_jupyter_url == ""
    assert settings.linq_jupyter_password == ""
    assert settings.fake is False
    monkeypatch.setenv("SAFEWATCH_FAKE", "1")
    assert get_settings.__wrapped__().fake is True
    monkeypatch.setenv("SAFEWATCH_FAKE", "0")
    assert get_settings.__wrapped__().fake is False


def test_browser_never_opens(side_effects: list[tuple[str, tuple[object, ...]]]) -> None:
    webbrowser.open("http://127.0.0.1/")
    assert side_effects == [("open", ("http://127.0.0.1/",))]


def test_owner_user_yaml_does_not_reach_tests(config_dir: Path) -> None:
    (config_dir / "user.yaml").write_text("escalation:\n  timeout_s: 99\n", encoding="utf-8")
    assert get_settings().escalation.timeout_s == 45


def test_relative_data_dir_resolves_from_the_repo(config_dir: Path) -> None:
    assert get_settings().data_dir == config.ROOT / "data" / "app"


def test_yaml_typo_stops_the_start(config_dir: Path) -> None:
    text = (config_dir / "default.yaml").read_text(encoding="utf-8")
    (config_dir / "default.yaml").write_text(
        text.replace("  timeout_s: 45", "  timeout_sec: 45"), encoding="utf-8"
    )
    with pytest.raises(ValidationError, match="timeout_sec"):
        get_settings()


def test_models_registry_resolves_active_models(settings: Settings) -> None:
    det, pose = registry.active_models(settings)
    assert (det.id, det.version, det.task, det.input_size) == (
        "det-yolov8n",
        "640-ap9999",
        "detect",
        640,
    )
    assert det.linq_program == "mosprom_det640_cut_ap9999_b1_o1_h1m.tpu"
    assert det.classes[67] == "cell phone"
    assert (pose.task, pose.classes) == ("pose", {0: "person"})
    assert registry.active_classes(settings) == [
        "person",
        "car",
        "bus",
        "train",
        "truck",
        "cell phone",
    ]
    wide = settings.model_copy(deep=True)
    wide.pipeline.detector = "det-yolov8n@960-ap9999"
    assert registry.active_models(wide)[0].input_size == 960
    broken = settings.model_copy(deep=True)
    broken.pipeline.detector = "det-yolov8n@1280-x"
    with pytest.raises(ValueError, match="det-yolov8n@1280-x is not in config/models.yaml"):
        registry.active_models(broken)


def test_v5_sections_load(config_dir: Path) -> None:
    settings = get_settings()
    assert settings.product_name == "Argus"
    assert settings.autocal.person_height_m == 1.7
    assert settings.pipeline.vehicle_classes == ["car", "bus", "truck", "train"]
    assert settings.scenarios.no_helmet["head_frac"] == 0.35
    assert settings.delivery.calls[0].provider == "stub"
    assert settings.demo.pack == Path("data/demo/argus")
    assert len(settings.calculator.assumptions) == 15
    assert {k.id for k in settings.zone_kinds} >= {"helmet_required", "respirator_required"}
    text = (config_dir / "default.yaml").read_text(encoding="utf-8")
    (config_dir / "default.yaml").write_text(
        text.replace("  crf: 23", "  crff: 23"), encoding="utf-8"
    )
    get_settings.cache_clear()
    with pytest.raises(ValidationError, match="crff"):
        get_settings()


def test_matvey_models_resolve(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> None:
    from safewatch import doctor

    models = registry.load_models(registry.MODELS_FILE)
    assert [f"{m.id}@{m.version}" for m in models[:3]] == [
        "det-yolov8n@640-ap9999",
        "det-yolov8n@960-ap9999",
        "pose-yolov8n@640-ap9999",
    ]  # the existing entries stay first and unchanged
    example = yaml.safe_load((config.CONFIG_DIR / "user.matvey.example.yaml").read_text("utf-8"))
    pose = registry.resolve(example["pipeline"]["pose"])
    (helmet,) = [registry.resolve(ref) for ref in example["pipeline"]["extra"]]
    assert (pose.task, pose.classes, pose.linq_program) == (
        "pose",
        {0: "person"},
        "mosprom_matvey_pose_yolov8n_640-v1-acc5f51228b9.tpu",
    )
    assert (helmet.task, helmet.classes, helmet.linq_program) == (
        "detect",
        {0: "helmet", 1: "no_helmet"},
        "mosprom_matvey_helmet_yolov8n_640-v1-5c3af1f3b855.tpu",
    )
    assert settings.pipeline.pose == "pose-yolov8n@640-ap9999"  # default.yaml is not switched
    matvey = settings.model_copy(
        update={
            "inference_backend": "local",
            "pipeline": settings.pipeline.model_copy(update=example["pipeline"]),
        }
    )
    assert "no_helmet" in registry.active_classes(matvey)
    monkeypatch.setattr(doctor, "ROOT", settings.data_dir)  # no models/matvey files there
    checks = {c.what: c for c in doctor._checks(matvey)}
    for ref in (example["pipeline"]["pose"], *example["pipeline"]["extra"]):
        check = checks[f"модель {ref}"]
        assert (check.result, check.ok) == ("нет файла", False)
        assert check.hint.startswith("models/matvey/")
