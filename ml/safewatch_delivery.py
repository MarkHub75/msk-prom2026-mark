"""Offline SafeWatch packaging. Never uploads, submits TPU jobs or changes training.

Run in the existing preparation environment; --compile is an explicit, separate
CPU SDK operation requiring calibration provenance. Binaries stay outside Git.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import time


COCO80 = (
    "person,bicycle,car,motorcycle,airplane,bus,train,truck,boat,traffic light,"
    "fire hydrant,stop sign,parking meter,bench,bird,cat,dog,horse,sheep,cow,"
    "elephant,bear,zebra,giraffe,backpack,umbrella,handbag,tie,suitcase,frisbee,"
    "skis,snowboard,sports ball,kite,baseball bat,baseball glove,skateboard,"
    "surfboard,tennis racket,bottle,wine glass,cup,fork,knife,spoon,bowl,banana,"
    "apple,sandwich,orange,broccoli,carrot,hot dog,pizza,donut,cake,chair,couch,"
    "potted plant,bed,dining table,toilet,tv,laptop,mouse,remote,keyboard,cell phone,"
    "microwave,oven,toaster,sink,refrigerator,book,clock,vase,scissors,teddy bear,"
    "hair drier,toothbrush"
).split(",")
EXTRA_CLASSES = {
    "fire", "smoke", "cigarette", "no_harness", "suspended_load", "cell phone",
    "helmet", "no_helmet", "vest", "no_vest",
}
ALIASES = {"Hardhat": "helmet", "NO-Hardhat": "no_helmet", "bare_head": "no_helmet"}
DETECTOR_CLASSES = {i: COCO80[i] for i in (0, 2, 5, 6, 7, 67)}


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def descriptor(path):
    path = Path(path)
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": digest(path)}


def token(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,79}", value):
        raise ValueError("id/version must be a lowercase filename-safe token")
    return value


def canonical_classes(names, role, mapping=None):
    if role not in ("detector", "pose", "extra") or not names:
        raise ValueError("explicit role and complete ordered class vocabulary required")
    mapping = mapping or {}
    if not isinstance(mapping, dict) or set(mapping) - set(names):
        raise ValueError("class mapping contains unknown source labels")
    classes = [mapping.get(n, ALIASES.get(n, n)) for n in names]
    if role == "detector":
        if names != COCO80 or classes != COCO80:
            raise ValueError("primary detector must preserve all 80 COCO channels/order; forklift is truck ID7")
        return DETECTOR_CLASSES.copy()
    if role == "pose":
        if classes != ["person"]:
            raise ValueError("pose requires one person class and COCO17")
        return {0: "person"}
    if len(set(classes)) != len(classes) or set(classes) - EXTRA_CLASSES:
        raise ValueError("extra vocabulary unsupported, duplicated, or requires tracked people/vehicles")
    if any(n in {"harness", "safety_harness", "helmet", "vest"} and
           classes[i].startswith("no_") for i, n in enumerate(names)):
        raise ValueError("positive equipment presence cannot be relabelled as absence")
    return dict(enumerate(classes))


def tensor_spec(value):
    import onnx
    dims = [d.dim_value for d in value.type.tensor_type.shape.dim]
    if not dims or any(d <= 0 for d in dims):
        raise ValueError("static tensor dimensions required")
    if value.type.tensor_type.elem_type != onnx.TensorProto.FLOAT:
        raise ValueError("SafeWatch boundary requires float32")
    return {"name": value.name, "shape": dims, "dtype": "float32"}


def session(path):
    import onnxruntime as ort
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = opts.inter_op_num_threads = 1
    return ort.InferenceSession(str(path), opts, providers=["CPUExecutionProvider"])


def tail_for_outputs(head, source):
    """Adapt the already decoded Matvey ABI; never repeat sigmoid or DFL."""
    import onnx
    from onnx import helper, TensorProto, numpy_helper
    import numpy as np
    specs = [tensor_spec(v) for v in head.graph.output]
    names = [s["name"] for s in specs]
    initializers = []
    if source.get("decoder") == "split_pose_v8":
        split = source["split_outputs"]
        expected = [split[k] for k in ("boxes", "class_scores", "keypoint_xy", "keypoint_scores")]
        if set(names) != set(expected):
            raise ValueError("split pose needs the four explicit named outputs")
        shapes = {s["name"]: s["shape"] for s in specs}
        anchors = shapes[split["boxes"]][-1]
        wanted = [[1, 4, anchors], [1, 1, anchors], [1, 17, 2, anchors], [1, 17, 1, anchors]]
        if [shapes[n] for n in expected] != wanted:
            raise ValueError("split pose shapes differ from COCO17 contract")
        initializers = [numpy_helper.from_array(np.array([1, 51, anchors], np.int64),
                                               "matvey_kpt_shape")]
        nodes = [
            helper.make_node("Concat", [split["keypoint_xy"], split["keypoint_scores"]],
                             ["matvey_kpt_triplets"], axis=2),
            helper.make_node("Reshape", ["matvey_kpt_triplets", "matvey_kpt_shape"],
                             ["matvey_kpt_flat"]),
            helper.make_node("Concat", [split["boxes"], split["class_scores"], "matvey_kpt_flat"],
                             ["matvey_decoded"], axis=1),
        ]
        output_shape = [1, 56, anchors]
    else:
        if len(specs) != 1:
            raise ValueError("decoded export needs one output or an explicit cut")
        output_shape = specs[0]["shape"]
        nodes = [helper.make_node("Identity", [names[0]], ["matvey_decoded"])]
    graph = helper.make_graph(nodes, "matvey_safewatch_tail", list(head.graph.output),
        [helper.make_tensor_value_info("matvey_decoded", TensorProto.FLOAT, output_shape)], initializers)
    tail = helper.make_model(graph, opset_imports=list(head.opset_import))
    tail.ir_version = head.ir_version
    onnx.checker.check_model(tail)
    return tail


def combine(head, tail):
    import onnx
    full = copy.deepcopy(head)
    full.graph.node.extend(copy.deepcopy(list(tail.graph.node)))
    full.graph.initializer.extend(copy.deepcopy(list(tail.graph.initializer)))
    del full.graph.output[:]
    full.graph.output.extend(copy.deepcopy(list(tail.graph.output)))
    onnx.checker.check_model(full)
    return full


def validate_local(model, source, role):
    import onnx
    onnx.checker.check_model(model)
    if len(model.graph.input) != 1 or len(model.graph.output) != 1:
        raise ValueError("one named image input and one decoded output required")
    inp, out = tensor_spec(model.graph.input[0]), tensor_spec(model.graph.output[0])
    size = source["input"]["shape"][-1]
    if inp != {"name": "images", "shape": [1, 3, size, size], "dtype": "float32"}:
        raise ValueError("SafeWatch requires images float32 static NCHW square input")
    if source.get("nms_in_graph") is not False or source.get("padding_value") != 114:
        raise ValueError("explicit nms=False, pad114 contract required")
    if source["input"].get("scale") != 1 / 255 or source["input"].get("layout") != "NCHW":
        raise ValueError("RGB/255 NCHW preprocessing required")
    if role == "pose" and source.get("keypoint_count") != 17:
        raise ValueError("COCO17 pose required")
    channels = 56 if role == "pose" else 4 + len(source["classes"])
    if out["shape"][:2] != [1, channels] or len(out["shape"]) != 3:
        raise ValueError("decoded BCN channel count is incompatible")
    return size


def parity(full_path, head_path, tail_path, input_spec):
    """One bounded CPU wiring check, not model accuracy or hardware evidence."""
    import numpy as np
    rng = np.random.default_rng(20261024)
    inp = {"images": rng.random(input_spec["shape"], dtype=np.float32)}
    full, head, tail = session(full_path), session(head_path), session(tail_path)
    a = full.run(None, inp)[0]
    raw = dict(zip([o.name for o in head.get_outputs()], head.run(None, inp)))
    b = tail.run(None, {i.name: raw[i.name] for i in tail.get_inputs()})[0]
    if not np.isfinite(a).all() or not np.isfinite(b).all() or a.shape != b.shape:
        raise ValueError("nonfinite or inconsistent head/tail output")
    error = float(np.max(np.abs(a - b)))
    if not np.allclose(a, b, atol=1e-4, rtol=1e-5):
        raise ValueError("float head/tail parity failed")
    return {"status": "PASS", "scope": "one synthetic tensor; CPU float ABI only",
            "max_abs_error": error, "shape": list(a.shape)}


def compile_cut(head_path, calibration, output, model_id):
    """Explicit SDK recipe: static b1, CPU PTQ percentile99.99, O1/H1M.

    Not invoked for an existing compiled bundle; no simulator or TPU execution.
    Unsupported SDK signatures fail rather than silently dropping PTQ options.
    """
    import onnx
    import numpy as np
    output = Path(output)
    output.mkdir(exist_ok=False)
    report = {"model_id": model_id, "source_onnx_sha256": digest(head_path),
        "calibration_sha256": digest(calibration), "compile_status": "RUNNING",
        "target": "TPU_H1M", "preset": "O1", "batch": 1,
        "activation_percentile": 99.99, "runtime_abi_verified": False,
        "linq_status": "NOT_RUN"}
    start = time.monotonic()
    stage = "sdk_import"
    try:
        from tpu_framework import (RegularModel, Network, compiler, TpuProgram,
                                   O1, TPU_H1M, preliminary_model_conditioning)
        stage = "conditioning"
        original = onnx.load(str(head_path))
        model = preliminary_model_conditioning(original)
        onnx.save(model, output / "conditioned.onnx")
        report["inputs"] = [tensor_spec(v) for v in model.graph.input]
        report["outputs"] = [tensor_spec(v) for v in model.graph.output]
        stage = "calibration_validation"
        with np.load(calibration, allow_pickle=False) as data:
            corpus = {n: np.ascontiguousarray(data[n]) for n in data.files}
        if set(corpus) != {s["name"] for s in report["inputs"]}:
            raise ValueError("calibration input names differ")
        for spec in report["inputs"]:
            arr = corpus[spec["name"]]
            if (arr.dtype != np.float32 or list(arr.shape[1:]) != spec["shape"][1:] or
                    arr.shape[0] < 1 or not np.isfinite(arr).all()):
                raise ValueError("invalid calibration tensors")
        stage = "ptq"
        regular = RegularModel(model=model)
        thresholds = regular.calibrate_torch(calibration_data=corpus, device="cpu",
                                             activation_percentile=99.99)
        RegularModel.dump_thresholds(str(output / "thresholds.json"), thresholds)
        quantized = regular.quantize(thresholds)
        quantized.save(file_dir=str(output), file_name="quantized.qm.onnx")
        stage = "compile"
        network, _ = Network.from_quantized_model(quantized)
        network.set_batch(1)
        executable, descriptions = compiler.compile_(hardware_parameters=TPU_H1M,
                                                     network=network, parameters=O1)
        TpuProgram.from_executable(executable, descriptions).to_file(str(output / "model.tpu"))
        report.update(compile_status="PASS", program_sha256=digest(output / "model.tpu"))
    except Exception as error:
        report.update(compile_status="FAIL", failed_stage=stage, exception_type=type(error).__name__)
    report["wall_seconds"] = time.monotonic() - start
    (output / "compile-report.json").write_text(json.dumps(report, indent=2) + "\n")
    if report["compile_status"] != "PASS":
        raise RuntimeError("SDK compile failed; inspect the retained compile report")
    return report


def prepare(source_manifest, output, model_id, version, role, *, mapping=None,
            compiled=None, compile_report=None, cut_at=None, compile_now=False,
            calibration=None, calibration_manifest=None, conf=.1, iou=.45):
    import onnx
    import yaml
    source_manifest, output = Path(source_manifest), Path(output)
    source = json.loads(source_manifest.read_text())
    model_id, version = token(model_id), token(version)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not 0 <= v <= 1
           for v in (conf, iou)):
        raise ValueError("finite confidence/NMS thresholds in [0,1] required")
    classes = canonical_classes(source["classes"], role, mapping)
    if source.get("decoder") not in ("detect_v8", "pose_v8", "split_pose_v8"):
        raise ValueError("classifier/raw/unknown model ABI is not a YOLO detection export")
    source_file = source_manifest.parent / source["artifacts"]["onnx"]["file"]
    if digest(source_file) != source["artifacts"]["onnx"]["sha256"]:
        raise ValueError("source ONNX hash mismatch")
    head = onnx.load(str(source_file))
    onnx.checker.check_model(head)
    tail = tail_for_outputs(head, source)
    full = combine(head, tail)
    size = validate_local(full, source, role)
    if compiled and (cut_at or compile_now):
        raise ValueError("existing TPU cannot be attached to a newly cut/recompiled graph")
    if bool(compiled) != bool(compile_report):
        raise ValueError("existing TPU requires matching compile report")
    revision = {"adapter": "safewatch-delivery-v1", "source": digest(source_file),
                "classes": classes, "role": role, "conf": conf, "iou": iou,
                "cut_at": cut_at, "program": digest(compiled) if compiled else None,
                "calibration": digest(calibration) if calibration else None}
    fingerprint = hashlib.sha256(json.dumps(revision, sort_keys=True).encode()).hexdigest()[:12]
    # ModelSpec.version is the application's cache identity. Never reuse it for new bytes.
    version = token(version + "-" + fingerprint)
    # Create a new immutable bundle. An existing directory is never overwritten.
    output.mkdir(parents=True, exist_ok=False)
    relative = Path("models") / "matvey" / model_id / version
    files = output / relative
    files.mkdir(parents=True)
    stem = "matvey_" + model_id.removeprefix("matvey-").replace("-", "_") + "_" + version
    local_path, head_path, tail_path = [files / f"{stem}{suffix}.onnx"
                                      for suffix in ("", "_head", "_tail")]
    onnx.save(full, str(local_path))
    onnx.save(head, str(head_path))
    onnx.save(tail, str(tail_path))
    if cut_at:
        if not all(isinstance(n, str) and n for n in cut_at):
            raise ValueError("explicit nonempty cut tensor names required")
        # The local model keeps the decoded head. The TPU gets only the exact cut.
        onnx.utils.extract_model(str(local_path), str(head_path), ["images"], cut_at)
        onnx.utils.extract_model(str(local_path), str(tail_path), cut_at, ["matvey_decoded"])
    check = parity(local_path, head_path, tail_path, source["input"])
    report = None
    if compile_now:
        if not calibration or not calibration_manifest:
            raise ValueError("explicit calibration NPZ and provenance are required")
        info = json.loads(Path(calibration_manifest).read_text())
        if (info.get("split") not in ("train", "calibration") or not info.get("groups") or
                info.get("calibration_allowed") is not True or
                info.get("sha256") != digest(calibration)):
            raise ValueError("calibration needs allowed train/calibration groups and matching hash")
        compile_dir = output / "compile"
        report = compile_cut(head_path, calibration, compile_dir, model_id)
        compiled, compile_report = compile_dir / "model.tpu", compile_dir / "compile-report.json"
    program = None
    if compiled:
        report = json.loads(Path(compile_report).read_text())
        if (report.get("compile_status") != "PASS" or
                report.get("source_onnx_sha256") != digest(head_path) or
                report.get("program_sha256") != digest(compiled)):
            raise ValueError("TPU compile lineage/hash mismatch")
        # Names in the tail must match the runtime output descriptors, never guessed.
        actual = {o["name"]: o["shape"] for o in report["outputs"]}
        wanted = {s["name"]: s["shape"] for s in map(tensor_spec, onnx.load(str(tail_path)).graph.input)}
        if actual != wanted:
            raise ValueError("conditioned/runtime output map requires an explicit reviewed tail")
        if compile_now:
            # Actual compiler output bytes also invalidate the app's artifact cache.
            suffix = digest(compiled)[:8]
            version = token(version + "-" + suffix)
            stem += "_" + suffix
        program = "mosprom_" + stem + ".tpu"
        shutil.copyfile(compiled, files / program)
        shutil.copyfile(compile_report, files / f"{stem}_compile-report.json")
    entry = {"id": model_id, "version": version, "task": "pose" if role == "pose" else "detect",
             "input_size": size, "conf": conf, "iou": iou, "classes": classes,
             "linq_program": program, "linq_tail": (relative / tail_path.name).as_posix(),
             "local_onnx": (relative / local_path.name).as_posix()}
    (output / "models.matvey.yaml").write_text(yaml.safe_dump({"models": [entry]}, sort_keys=False))
    switch = {"pipeline": {role: [f"{model_id}@{version}"] if role == "extra" else f"{model_id}@{version}"}}
    (output / "user.matvey.yaml").write_text(yaml.safe_dump(switch, sort_keys=False))
    release = {"schema": "matvey-safewatch-delivery-v1", "role": role,
        "source": descriptor(source_manifest), "source_onnx": descriptor(source_file),
        "model": entry, "float_parity": check,
        "statuses": {"local_abi": "PASS", "compile": ("PASS" if compile_now else "EXISTING_PASS") if compiled else "NOT_RUN",
            "new_linq_execution": "NOT_RUN", "remote_placement": "NOT_RUN",
            "scenario_quality": "NOT_EVALUATED",
            "scenario_support": "NO_PPE_PLUGIN" if set(classes.values()) & {"helmet", "no_helmet", "vest", "no_vest"} else "EXISTING_PLUGIN_CLASSES_ONLY"},
        "files": [descriptor(p) for p in sorted(files.iterdir())]}
    (output / "MANIFEST.json").write_text(json.dumps(release, indent=2) + "\n")
    return release


def write_eval_labels(source, output):
    """Only explicit, complete reviewed event GT may become SafeWatch labels."""
    data = json.loads(Path(source).read_text())
    if data.get("reviewed_complete") is not True or data.get("scope") not in ("development", "validation"):
        raise ValueError("incomplete/weak/sealed annotations cannot become exhaustive event GT")
    scenarios = {"running", "proximity", "phone", "fall", "fence_crossing", "restricted_under",
                 "fire_smoking", "no_harness", "suspended_load"}
    if not data.get("videos"):
        raise ValueError("videos required")
    for video in data["videos"]:
        if set(video) - {"path", "camera_id", "expected"} or "expected" not in video:
            raise ValueError("explicit path/expected required; unknown fields not allowed")
        if not Path(video["path"]).is_file():
            raise ValueError("video file missing")
        for event in video["expected"]:
            if event["scenario"] not in scenarios or not 0 <= event["start_s"] < event["end_s"]:
                raise ValueError("invalid event or scenario")
    import yaml
    with Path(output).open("x") as out:
        yaml.safe_dump({"deadline_s": data.get("deadline_s", 5), "videos": data["videos"]}, out, sort_keys=False)


def main():
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[key] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--manifest")
    src.add_argument("--weights", help="trusted existing checkpoint; CPU export only")
    p.add_argument("--output", required=True)
    p.add_argument("--model-id", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--role", choices=("detector", "pose", "extra"), required=True)
    p.add_argument("--class-map", default="{}", help="explicit JSON source label -> canonical label")
    p.add_argument("--size", type=int, default=640)
    p.add_argument("--conf", type=float, default=.1)
    p.add_argument("--iou", type=float, default=.45)
    p.add_argument("--compiled")
    p.add_argument("--compile-report")
    p.add_argument("--cut-at", help="comma-separated exact graph tensors; no heuristic cut")
    p.add_argument("--compile", action="store_true", dest="compile_now")
    p.add_argument("--calibration")
    p.add_argument("--calibration-manifest")
    p = sub.add_parser("eval-labels")
    p.add_argument("--source", required=True)
    p.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "eval-labels":
        write_eval_labels(args.source, args.output)
        return
    source = args.manifest
    if args.weights:
        if Path(args.output).exists():
            raise ValueError("bundle already exists")
        from ml.detection.export import export_model
        staging = Path(args.output).with_name(Path(args.output).name + "-source")
        if staging.exists():
            raise ValueError("export staging already exists")
        source = export_model(args.weights, staging, args.model_id,
            "pose_v8" if args.role == "pose" else "detect_v8", args.size, 13)
    release = prepare(source, args.output, args.model_id, args.version, args.role,
        mapping=json.loads(args.class_map), compiled=args.compiled, compile_report=args.compile_report,
        cut_at=args.cut_at.split(",") if args.cut_at else None, compile_now=args.compile_now,
        calibration=args.calibration, calibration_manifest=args.calibration_manifest,
        conf=args.conf, iou=args.iou)
    print(json.dumps({"model": release["model"], "statuses": release["statuses"]}, indent=2))


if __name__ == "__main__":
    main()
