"""Verify real ONNX inference in an isolated, detached SafeWatch checkout.

Only that disposable checkout's registry/user config and owned output are changed.
No server is started, no network/TPU is used, and no source code is patched.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

from ml.safewatch_delivery import digest


def git(app, *args):
    return subprocess.run(["git", "-C", str(app), *args], capture_output=True, text=True, check=True).stdout.strip()


def _run(app, output, python, bundles):
    import cv2
    import numpy as np
    import yaml
    app, output = Path(app).resolve(), Path(output).resolve()
    detached = subprocess.run(["git", "-C", str(app), "symbolic-ref", "--quiet", "HEAD"],
                              capture_output=True).returncode == 1
    if not detached or git(app, "status", "--porcelain", "--", "src", "tools"):
        raise ValueError("clean detached disposable SafeWatch worktree required")
    if (app / "config/user.yaml").exists():
        raise ValueError("refusing to replace an existing user configuration")
    entries = []
    sources = []
    for bundle in bundles:
        bundle = Path(bundle).resolve()
        manifest = json.loads((bundle / "MANIFEST.json").read_text())
        for item in manifest["files"]:
            path = Path(item["path"]).resolve()
            relative = path.relative_to(bundle)
            if relative.parts[0] != "models" or digest(path) != item["sha256"]:
                raise ValueError("unsafe or changed bundle file")
            target = app / relative
            if target.exists():
                raise ValueError("refusing to overwrite existing application model")
        entries.append(manifest["model"])
        sources.append(manifest)
    by_role = {m["role"]: m["model"] for m in sources if m["role"] != "extra"}
    if set(by_role) != {"detector", "pose"}:
        raise ValueError("a genuine COCO80 reference detector and Matvey pose are required")
    output.mkdir(parents=True, exist_ok=False)
    registry = app / "config/models.yaml"
    original = yaml.safe_load(registry.read_text())
    refs = {f'{m["id"]}@{m["version"]}' for m in original["models"]}
    if any(f'{m["id"]}@{m["version"]}' in refs for m in entries):
        raise ValueError("model registry collision")
    for bundle, manifest in zip(bundles, sources):
        for item in manifest["files"]:
            source = Path(item["path"])
            target = app / source.relative_to(Path(bundle).resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    registry.write_text(yaml.safe_dump({"models": original["models"] + entries}, sort_keys=False))
    ref = lambda m: f'{m["id"]}@{m["version"]}'
    settings = {"data_dir": str(output / "app-data"), "local": {"threads": 1},
        "pipeline": {"detector": ref(by_role["detector"]), "pose": ref(by_role["pose"]),
            "extra": [ref(m["model"]) for m in sources if m["role"] == "extra"],
            "target_analysis_fps": 5, "min_analysis_fps": 5}}
    (app / "config/user.yaml").write_text(yaml.safe_dump(settings, sort_keys=False))
    # Known-empty artificial scene: this is wiring evidence, never industrial GT.
    video = output / "matvey_empty_control.avi"
    cv2.setNumThreads(1)
    writer = cv2.VideoWriter(str(video), cv2.VideoWriter_fourcc(*"MJPG"), 5, (640, 360))
    if not writer.isOpened():
        raise ValueError("control video encoder unavailable")
    for _ in range(5): writer.write(np.zeros((360, 640, 3), np.uint8))
    writer.release()
    labels = output / "eval.compatibility-only.yaml"
    labels.write_text("# Synthetic empty-scene software fixture; NOT model-quality GT.\n" +
        yaml.safe_dump({"deadline_s": 5, "videos": [{"path": str(video), "expected": []}]}))
    env = os.environ.copy()
    env.update({k: "1" for k in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS")})
    env.update(INFERENCE_BACKEND="local", SAFEWATCH_FAKE="0", CUDA_VISIBLE_DEVICES="",
               PYTHONPATH=str(app / "src"))
    # Runtime-only secrets, if present in the parent, are unnecessary in this local test.
    for key in list(env):
        if key.startswith("LINQ_") or key in ("MOSPROM_BACKEND_TOKEN",): env.pop(key)
    commands = [
        [str(python), "-m", "safewatch", "doctor"],
        [str(python), "-m", "safewatch", "eval", str(labels), "--out", str(output / "eval")],
    ]
    observed = []
    for i, command in enumerate(commands):
        start = time.monotonic()
        result = subprocess.run(command, cwd=app, env=env, capture_output=True, text=True, timeout=120)
        (output / f"command-{i}.stdout.txt").write_text(result.stdout)
        (output / f"command-{i}.stderr.txt").write_text(result.stderr)
        observed.append({"argv": command, "returncode": result.returncode,
                         "wall_seconds": time.monotonic() - start})
        if result.returncode:
            raise RuntimeError(f"local command {i} failed; inspect owned output logs")
    probe = """import json
from safewatch import config,registry,rules
from safewatch.inference.artifacts import read_jsonl
s=config.get_settings()
print(json.dumps({'module_root':str(config.ROOT),'active_classes':registry.active_classes(s),
 'scenarios':{m.id:m.status for m in rules.scenario_metas()},
 'artifacts':{p.name:len(read_jsonl(p,None)) for p in s.data_dir.joinpath('artifacts').glob('*.jsonl')}}))
"""
    result = subprocess.run([str(python), "-c", probe], cwd=app, env=env,
                            capture_output=True, text=True, check=True, timeout=30)
    acceptance = json.loads(result.stdout)
    if acceptance["module_root"] != str(app) or acceptance["scenarios"]["fall"] != "active":
        raise ValueError("wrong source checkout or missing scenario classes")
    if len(acceptance["artifacts"]) != len(entries) or any(v != 5 for v in acceptance["artifacts"].values()):
        raise ValueError("not all real model artifact rows were produced")
    report = {"status": "PASS_LOCAL_COMPATIBILITY", "main_revision": git(app, "rev-parse", "HEAD"),
        "commands": observed, "acceptance": acceptance, "models": entries,
        "video": {"path": str(video), "sha256": digest(video), "kind": "synthetic-empty-control", "frames": 5},
        "gpu_jobs": 0, "tpu_requests": 0, "accuracy_claim": False,
        "limits": ["No industrial-quality or positive-event acceptance", "No new LinQ qualification",
                   "COCO80 is an official reference, NOT a Matvey-trained checkpoint", "No PPE plugin in application"]}
    (output / "local-check.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def run(app, output, python, bundles):
    app, output = Path(app).resolve(), Path(output).resolve()
    # Refuse a branch checkout BEFORE any write, including cleanup writes.
    if subprocess.run(["git", "-C", str(app), "symbolic-ref", "--quiet", "HEAD"],
                      capture_output=True).returncode != 1:
        raise ValueError("detached disposable checkout required")
    registry = app / "config/models.yaml"
    user = app / "config/user.yaml"
    if user.exists():
        raise ValueError("existing user configuration must not be touched")
    original = registry.read_bytes()
    try:
        report = _run(app, output, python, bundles)
        # Retain experiment config outside the checkout, with the evidence.
        shutil.copyfile(registry, output / "models.experiment.yaml")
        shutil.copyfile(user, output / "user.experiment.yaml")
    finally:
        registry.write_bytes(original)
        if user.exists(): user.unlink()
    report["temporary_configuration_removed"] = True
    (output / "local-check.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--python", required=True)
    parser.add_argument("--bundle", action="append", required=True)
    args = parser.parse_args()
    report = run(args.app, args.output, args.python, args.bundle)
    print(json.dumps({k: report[k] for k in ("status", "main_revision", "acceptance", "gpu_jobs", "tpu_requests")}, indent=2))


if __name__ == "__main__": main()
