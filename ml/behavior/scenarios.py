"""Deterministic synthetic temporal-contract fixtures, without model inference.

Generate outside the repository with:
    python -m ml.behavior.scenarios --output-dir /workspace/artifacts/behavior/acceptance
"""
import argparse
import json
from copy import deepcopy
from pathlib import Path

SCENARIOS = (
    "missing_helmet", "fall_immobility", "starts_lying", "compliance",
    "gaps", "ambiguous_people", "no_repeat", "epoch_reset",
)


def _person(*, lying=False, x=100):
    points = [[0, 0, 0] for _ in range(17)]
    if lying:
        box = [x, 100, x + 200, 180]
        values = {0: (x+20, 130), 5: (x+40, 120), 6: (x+40, 150),
                  7: (x+50, 120), 8: (x+50, 150), 9: (x+80, 120),
                  10: (x+80, 150), 11: (x+120, 120), 12: (x+120, 150),
                  13: (x+140, 120), 14: (x+140, 150),
                  15: (x+170, 120), 16: (x+170, 150)}
    else:
        box = [x, 0, x+80, 200]
        values = {0: (x+40, 20), 5: (x+20, 50), 6: (x+60, 50),
                  11: (x+20, 130), 12: (x+60, 130)}
    for i, xy in values.items():
        points[i] = [*xy, 0.99]
    return {"detection_id": "synthetic-person", "class_name": "person", "score": 0.99,
            "bbox_xyxy": box, "keypoints": points}


def _head(kind="bare_head"):
    return {"detection_id": "synthetic-head", "class_name": kind, "score": 0.99,
            "bbox_xyxy": [120, 5, 160, 40], "keypoints": None}


def _batch(name, time_ms, detections, *, status="ok", epoch="synthetic-epoch-1"):
    return {"schema_version": "1.0", "camera_id": f"synthetic-{name}",
            "stream_epoch": epoch, "frame_id": int(time_ms // 500),
            "media_time_ms": time_ms, "image_size": [1000, 800],
            "request_id": f"synthetic-{name}-{epoch}-{time_ms}",
            "model_id": "synthetic-observations-v1", "backend": "synthetic-test",
            "status": status, "detections": detections,
            "fixture_origin": "synthetic-no-neural-inference"}


def _expected(kind, confirmed, states, *, immobility=False, epoch="synthetic-epoch-1", end=None):
    value = {"type": kind, "confirmed_media_ms": confirmed, "states": states,
             "revisions": list(range(1, len(states)+1)),
             "immobility_observed": immobility, "stream_epoch": epoch}
    if end is not None:
        value["end_media_ms"] = end
    return value


def build_scenario(name):
    """Return independent observation sequence and semantic expectations.

    Expectations specify incident identity *relationships*, never generated UUIDs
    or engine wall-clock emission times. Open incidents at the finite trace end
    are censored, not evidence that a real hazard has cleared.
    """
    if name not in SCENARIOS:
        raise ValueError(f"unknown scenario: {name}")
    batches = []
    if name == "missing_helmet":
        for t in range(0, 4501, 500):
            batches.append(_batch(name, t, [_person(), _head()]))
        expected = [_expected("missing_helmet", 2000, ["open"])]
        description = "Continuous positive bare-head observations confirm once after two seconds."
    elif name == "fall_immobility":
        for t in (0, 500):
            batches.append(_batch(name, t, [_person()]))
        for t in range(1000, 6501, 500):
            batches.append(_batch(name, t, [_person(lying=True)]))
        expected = [_expected("suspected_fall", 2000, ["open", "open"], immobility=True)]
        description = "Observed upright-to-lying transition; immobility updates the same incident UUID."
    elif name == "starts_lying":
        for t in range(0, 5501, 500):
            batches.append(_batch(name, t, [_person(lying=True)]))
        expected = [_expected("prolonged_lying", 3000, ["open", "open"], immobility=True)]
        description = "An already lying person is not reported as an observed fall transition."
    elif name == "compliance":
        for t in range(0, 5501, 500):
            batches.append(_batch(name, t, [_person(), _head("helmet")]))
        expected = []
        description = "Visible helmet and upright person do not create any violation."
    elif name == "gaps":
        for t in range(0, 1501, 500):
            batches.append(_batch(name, t, [_person(), _head()]))
        batches.append(_batch(name, 2000, [], status="gap"))
        for t in range(3000, 6001, 500):
            batches.append(_batch(name, t, [_person(), _head()]))
        batches.append(_batch(name, 6500, [], status="gap"))
        expected = [_expected("missing_helmet", 5000, ["open", "interrupted"], end=6500)]
        description = "A gap breaks pending dwell; a later gap interrupts rather than resolves a confirmed incident."
    elif name == "ambiguous_people":
        for t in range(0, 5501, 500):
            batches.append(_batch(name, t, [_person(), _person(x=110), _head()]))
        expected = []
        description = "A head compatible with two overlapping people does not establish wearer ownership."
    elif name == "no_repeat":
        for t in range(0, 7501, 500):
            kind = "helmet" if 3000 <= t <= 3500 else "bare_head"
            batches.append(_batch(name, t, [_person(), _head(kind)]))
        expected = [_expected("missing_helmet", 2000, ["open", "closed"], end=3000)]
        description = "Observed compliance closes the incident; same uninterrupted presence remains notification-suppressed."
    else:  # epoch_reset
        for t in range(0, 2501, 500):
            batches.append(_batch(name, t, [_person(), _head()]))
        for t in range(0, 2501, 500):
            batches.append(_batch(name, t, [_person(), _head()], epoch="synthetic-epoch-2"))
        expected = [_expected("missing_helmet", 2000, ["open", "interrupted"], end=2500),
                    _expected("missing_helmet", 2000, ["open"], epoch="synthetic-epoch-2")]
        description = "A new source clock interrupts the previous epoch at its own last observed media time."
    return deepcopy(batches), {
        "name": name, "camera_id": f"synthetic-{name}", "description": description,
        "observation_count": len(batches), "restart_after_observations": len(batches)//2,
        "expected_incidents": expected,
        "expected_incident_notifications": len(expected),
    }


def generate(output_dir, names=None, *, overwrite=False):
    """Write observations.jsonl and expected.json; refuse accidental overwrite."""
    names = list(names or SCENARIOS)
    if len(set(names)) != len(names):
        raise ValueError("scenario names must be unique")
    built = [build_scenario(name) for name in names]
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    observations_path, expected_path = directory/"observations.jsonl", directory/"expected.json"
    if not overwrite and any(p.exists() for p in (observations_path, expected_path)):
        raise FileExistsError("scenario output exists; choose another directory or --overwrite")
    observations = [batch for batches, _ in built for batch in batches]
    manifest = {
        "schema_version": "1.0", "artifact_kind": "synthetic-temporal-contract-fixtures",
        "backend": "synthetic-test", "neural_inference_performed": False,
        "hardware_execution_verified": False, "target_video_accuracy_measured": False,
        "observation_file": observations_path.name, "observation_count": len(observations),
        "scenarios": [expectation for _, expectation in built],
        "acceptance": {"one_notification_per_incident_uuid": True,
                       "revisions_preserve_uuid": True,
                       "same_epoch_restart_and_replay_preserve_identity": True,
                       "event_end_uses_own_epoch_clock": True},
    }
    observations_path.write_text("".join(json.dumps(v, sort_keys=True, allow_nan=False)+"\n" for v in observations))
    expected_path.write_text(json.dumps(manifest, indent=2, sort_keys=True, allow_nan=False)+"\n")
    return manifest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--scenario", action="append", choices=SCENARIOS,
                        help="repeat to select cases; default: all")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    manifest = generate(args.output_dir, args.scenario, overwrite=args.overwrite)
    print(json.dumps({"artifact_kind": manifest["artifact_kind"],
                      "backend": manifest["backend"],
                      "scenario_count": len(manifest["scenarios"]),
                      "observation_count": manifest["observation_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
