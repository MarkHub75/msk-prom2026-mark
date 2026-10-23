"""ONNX -> LinQ TPU program for Ultralytics YOLO (runs in the WSL SDK venv, see setup_sdk_wsl.sh).

    ~/linq_sdk/venv/bin/python tools/linq/sdk/compile_yolo.py models/yolov8n_640_op13.onnx \
        [--preset O1] [--n-calib-src 50] [--cut-at name1,name2,...] [--activation-percentile P]

Steps (vendor compile.py, with real calibration instead of random data):
  1. optional cut: head = images -> cut tensors (goes to TPU), tail = cut tensors -> outputs
     (saved as *_tail.onnx, runs in onnxruntime on CPU) — this is how the vendor ships yolov8n_pose
  2. preliminary_model_conditioning
  3. calibrate_torch on letterboxed person frames (coco128 persons + h-flips; held-out test split)
  4. quantize -> .qm.onnx; CPU fake-quant check vs fp32 onnxruntime on held-out images
  5. Network.from_quantized_model -> compiler.compile_(TPU_H1M, preset) -> .tpu
Everything goes to models/linq/<tag>/ plus <tag>.report.json (requested AND applied params).
"""
from __future__ import annotations

import argparse
import inspect
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")  # never silently pick a GPU

import cv2
import numpy as np
import onnx
import onnxruntime as ort

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools" / "linq"))
import yolo_io  # noqa: E402

COCO = REPO / "data" / "coco128"


def person_images() -> tuple[list[Path], list[Path], list[Path]]:
    """(person images sorted, non-person images sorted). Deterministic."""
    imgs = sorted((COCO / "images" / "train2017").glob("*.jpg"))
    person, other = [], []
    for p in imgs:
        lbl = COCO / "labels" / "train2017" / (p.stem + ".txt")
        has = lbl.exists() and any(l.startswith("0 ") for l in lbl.read_text().splitlines())
        (person if has else other).append(p)
    return person, other


def load_rgb(p: Path) -> np.ndarray:
    return cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2RGB)


def calib_tensor(paths: list[Path], size: int) -> np.ndarray:
    xs = []
    for p in paths:
        img = load_rgb(p)
        for variant in (img, img[:, ::-1].copy()):  # original + horizontal flip
            xs.append(yolo_io.preprocess(variant, size)[0])
        h, w = img.shape[:2]  # + a 0.8 centre crop (closer, larger people)
        crop = img[int(h * .1):int(h * .9), int(w * .1):int(w * .9)].copy()
        xs.append(yolo_io.preprocess(crop, size)[0])
    return np.concatenate(xs, 0).astype(np.float32)


def strip_initializer_inputs(m: onnx.ModelProto) -> None:
    inits = {i.name for i in m.graph.initializer}
    for i in [i for i in m.graph.input if i.name in inits]:
        m.graph.input.remove(i)


def strip_unused_initializers(m: onnx.ModelProto) -> None:
    used = {i for n in m.graph.node for i in n.input}
    for init in [i for i in m.graph.initializer if i.name not in used]:
        m.graph.initializer.remove(init)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("onnx")
    ap.add_argument("--preset", default="O1", choices=["O1", "O3", "O5"])
    ap.add_argument("--n-calib-src", type=int, default=50, help="person images used (x3 variants)")
    ap.add_argument("--cut-at", default="", help="comma list of tensor names: TPU head ends here")
    ap.add_argument("--tag", default="")
    ap.add_argument("--activation-percentile", type=float)
    ap.add_argument("--samplewise-percentile", type=float)
    ap.add_argument("--skip-compile", action="store_true")
    a = ap.parse_args()

    import torch
    import tpu_framework as tfw
    from dnn_quant.api import QuantizedModel, RegularModel, TpuDtype

    src = Path(a.onnx).resolve()
    meta = json.loads(src.with_suffix(".json").read_text())
    size = meta["inputs"][0]["shape"][-1]
    in_name = meta["inputs"][0]["name"]
    tag = a.tag or f"{src.stem}_{a.preset.lower()}" + ("_cut" if a.cut_at else "")
    out = REPO / "models" / "linq" / tag
    out.mkdir(parents=True, exist_ok=True)
    rep: dict = {"tag": tag, "source_onnx": src.name, "sdk": {}, "timings_s": {}, "requested": vars(a)}
    import importlib.metadata as md
    for d in ("tpu_framework_bin", "tpu_compiler_bin", "dnn_quant_bin", "onnx_direct_bin", "torch", "onnx"):
        rep["sdk"][d] = md.version(d)

    model = onnx.load(str(src))
    strip_initializer_inputs(model)
    if any(d.dim_value == 0 for i in model.graph.input for d in i.type.tensor_type.shape.dim):
        raise SystemExit("dynamic input shape: export with dynamic=False")

    # 1. optional cut
    head = model
    if a.cut_at:
        cut = [c for c in a.cut_at.split(",") if c]
        head = tfw.get_sub_model(model, [in_name], cut)
        tail = tfw.get_sub_model(model, cut, [o.name for o in model.graph.output])
        strip_unused_initializers(tail)  # get_sub_model keeps every weight of the full model
        onnx.save(head, out / f"{tag}_head.onnx")
        onnx.save(tail, out / f"{tag}_tail.onnx")
        rep["cut"] = {"head_outputs": cut, "tail_ops": sorted({n.op_type for n in tail.graph.node}),
                      "tail_onnx": f"{tag}_tail.onnx"}
    head_out_names = [o.name for o in head.graph.output]

    # 2. conditioning
    t = time.time()
    opt = tfw.preliminary_model_conditioning(head)
    onnx.save(opt, out / f"{tag}_opt.onnx")
    rep["timings_s"]["conditioning"] = round(time.time() - t, 1)

    # 3. calibration (real frames, held-out test split)
    person, other = person_images()
    calib_src, test_person = person[:a.n_calib_src], person[a.n_calib_src:]
    test_imgs = test_person[:8] + other[:4]
    calib = calib_tensor(calib_src, size)
    rep["calibration"] = {"source": "coco128 person images + hflip + 0.8 centre crop",
                          "n_src_images": len(calib_src), "n_frames": int(calib.shape[0]),
                          "tensor": [list(calib.shape), str(calib.dtype)],
                          "test_images": [p.name for p in test_imgs]}
    rm_kwargs = {}
    rm = RegularModel(model=opt, **rm_kwargs)
    cal_kwargs = {"calibration_data": {in_name: calib}, "device": "cpu"}
    if a.activation_percentile is not None:
        cal_kwargs["activation_percentile"] = a.activation_percentile
    if a.samplewise_percentile is not None:
        cal_kwargs["samplewise_percentile"] = a.samplewise_percentile
    # applied = exactly what the signature accepts; no try/except retry that could drop a param
    sig = inspect.signature(RegularModel.calibrate_torch).parameters
    unknown = [k for k in cal_kwargs if k not in sig]
    if unknown:
        raise SystemExit(f"calibrate_torch does not accept {unknown}")
    rep["calibration"]["applied_params"] = {k: v for k, v in cal_kwargs.items() if k != "calibration_data"}
    rep["calibration"]["regular_model_params"] = {"percentile": rm.__dict__.get("percentile", "default 100.0"),
                                                  **rm_kwargs}
    t = time.time()
    thresholds = rm.calibrate_torch(**cal_kwargs)
    rep["timings_s"]["calibration"] = round(time.time() - t, 1)
    RegularModel.dump_thresholds(str(out / "thresholds.json"), thresholds)
    del calib

    t = time.time()
    qm = rm.quantize(thresholds)
    qm_name = f"{tag}.qm.onnx"
    qm.save(file_dir=str(out), file_name=qm_name)
    rep["timings_s"]["quantize"] = round(time.time() - t, 1)

    # 4. CPU fake-quant vs fp32 (head outputs, then through the same tail -> detections)
    qm = QuantizedModel.load(str(out / qm_name))
    g = qm.as_torch_graph(batch_size=1, cache_word_length=tfw.TPU_H1M.tpu_parameters.cache_word_length)
    anchors = g.get_outputs_anchors() | g.get_inputs_anchors()
    g.gm.eval()
    fp_head = ort.InferenceSession(head.SerializeToString(), providers=["CPUExecutionProvider"])
    fp_full = ort.InferenceSession(model.SerializeToString(), providers=["CPUExecutionProvider"])
    tail_sess = (ort.InferenceSession(str(out / f"{tag}_tail.onnx"), providers=["CPUExecutionProvider"])
                 if a.cut_at else None)
    kpt = tuple(meta["kpt_shape"]) if meta.get("kpt_shape") else None
    cmp, fq_dump = [], {}
    for p in test_imgs:
        x, m = yolo_io.preprocess(load_rgb(p), size)
        ref = fp_full.run(None, {in_name: x})[0]
        xs = qm.rescale({anchors[in_name]: x}, TpuDtype.Input)
        with torch.no_grad():
            outs = g.gm(*(torch.as_tensor(xs[n]) for n in g._input_layer_names))
        if not isinstance(outs, (list, tuple)):
            outs = [outs]
        out_anchor_names = [anchors[n] for n in head_out_names]
        raw = qm.rescale({n: o.cpu().numpy() for n, o in zip(out_anchor_names, outs)}, TpuDtype.Output)
        head_vals = {n: raw[anchors[n]] for n in head_out_names}
        fq = tail_sess.run(None, head_vals)[0] if tail_sess else head_vals[head_out_names[0]]
        fq_dump[p.name] = fq
        d_ref = yolo_io.postprocess(ref, m, nc=meta["nc"], kpt_shape=kpt)
        d_fq = yolo_io.postprocess(fq, m, nc=meta["nc"], kpt_shape=kpt)
        cmp.append({"image": p.name, "max_abs_out_diff": float(np.abs(fq - ref).max()),
                    **yolo_io.match_dets(d_ref, d_fq)})
    np.savez_compressed(out / "fakequant_outputs.npz", **fq_dump)
    rep["fakequant_vs_fp32"] = cmp
    rec = [c["recall_vs_ref"] for c in cmp if c["n_ref"]]
    ious = [c["mean_iou"] for c in cmp if c["mean_iou"] is not None]
    rep["fakequant_summary"] = {"mean_recall_vs_fp32": float(np.mean(rec)) if rec else None,
                                "mean_iou": float(np.mean(ious)) if ious else None}
    print("fake-quant vs fp32:", json.dumps(rep["fakequant_summary"]))

    # 5. compile
    if not a.skip_compile:
        t = time.time()
        network, renaming = tfw.Network.from_quantized_model(str(out / qm_name))
        network.set_batch(1)
        executable, tdesc = tfw.compiler.compile_(hardware_parameters=tfw.TPU_H1M, network=network,
                                                  parameters=getattr(tfw, a.preset))
        prog = tfw.TpuProgram.from_executable(executable, tdesc)
        prog_name = f"{tag}_b1_{a.preset.lower()}_h1m.tpu"
        prog.to_file(str(out / prog_name))
        rep["timings_s"]["compile"] = round(time.time() - t, 1)
        rep["program"] = {"file": prog_name, "bytes": (out / prog_name).stat().st_size,
                          "renaming": dict(renaming),
                          "tensor_descriptions": {k: repr(v)[:400] for k, v in tdesc.items()}}
        print("compiled:", prog_name, rep["program"]["bytes"], "bytes")
    (out / f"{tag}.report.json").write_text(json.dumps(rep, indent=1, default=str))
    print("report:", out / f"{tag}.report.json")


if __name__ == "__main__":
    main()
