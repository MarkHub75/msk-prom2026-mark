"""Derive an operational model manifest from reviewed, existing TPU captures.

This is local evidence validation, not network access or independent hardware
attestation. Source/candidate manifests are never modified.
"""
from copy import deepcopy
import json
from pathlib import Path
from uuid import UUID
import numpy as np
from ml.pipeline.capture_review import review_capture
from .export import sha256
from .codec import decode, LetterboxTransform
from .compare_capture import load_numeric_npz

PROFILES={"helmet":("helmet-v1","helmet-v1.tpu","detect_v8"),
          "pose-split":("pose-split-v1","pose-split-v1.tpu","split_pose_v8")}


def _json(path):
    return json.loads(Path(path).read_text())


def _specs(values):
    if not isinstance(values,list) or not values:
        raise ValueError("empty compiler ABI")
    result={}
    for spec in values:
        if not isinstance(spec,dict) or set(spec)!={"name","shape","dtype"}:
            raise ValueError("invalid compiler tensor specification")
        name,shape=spec["name"],spec["shape"]
        if not isinstance(name,str) or not name or name in result or not isinstance(shape,list) or not shape or any(type(v) is not int or v<=0 for v in shape):
            raise ValueError("invalid compiler ABI name/shape")
        dtype=np.dtype(spec["dtype"])
        if dtype.kind!="f":raise ValueError("MVP runtime ABI must be decoded floating tensors")
        result[name]={"shape":shape,"dtype":dtype.name}
    return result


def prepare_verified_manifest(name,artifacts_root="/workspace/artifacts"):
    if name not in PROFILES:raise ValueError("only helmet and pose-split are supported")
    model_id,program_name,decoder=PROFILES[name]
    root=Path(artifacts_root).resolve()
    source_dir=root/"detection"/name
    compile_dir=root/"linq-sdk"/(name+"-compile")
    capture_dir=root/"linq-rpc"/(name+"-001")
    source_path=source_dir/"manifest.json";compiled_path=compile_dir/"compile-report.json"
    response_path=capture_dir/"response.json";receipt_path=root/"linq-rpc"/name/"staging-receipt.json"
    source,compiled,response,receipt=(_json(p) for p in (source_path,compiled_path,response_path,receipt_path))
    program_path=compile_dir/"model.tpu"
    if program_path.is_symlink() or not program_path.is_file():raise ValueError("missing regular local TPU program")
    program_hash=sha256(program_path)
    if source.get("model_id")!=model_id or source.get("decoder")!=decoder or compiled.get("model_id")!=model_id:
        raise ValueError("source/compiled model identity mismatch")
    if compiled.get("compile_status")!="PASS" or compiled.get("stages",{}).get("compile",{}).get("status")!="PASS":
        raise ValueError("compiler did not report successful completion")
    if compiled.get("program_sha256")!=program_hash:raise ValueError("compiled/local program hash mismatch")
    artifact=source.get("artifacts",{}).get("onnx",{})
    onnx_path=source_dir/artifact.get("file","")
    if onnx_path.resolve().parent!=source_dir.resolve() or onnx_path.is_symlink() or not onnx_path.is_file():
        raise ValueError("invalid source ONNX artifact")
    if sha256(onnx_path)!=artifact.get("sha256") or compiled.get("source_onnx_sha256")!=artifact.get("sha256"):
        raise ValueError("source ONNX differs from compiled graph")
    integrity=review_capture(capture_dir,expected_program_sha256=program_hash)
    capture=_json(capture_dir/"capture.json")
    if capture.get("model_id")!=model_id:raise ValueError("capture model identity mismatch")
    request=capture.get("journal_request_id")
    if not isinstance(request,str) or str(UUID(request))!=request:raise ValueError("invalid capture request UUID")
    if (response.get("status")!="completed" or type(response.get("status_code")) is not int or response["status_code"]!=0 or
        response.get("request_id")!=request or response.get("response_id")!=request or response.get("journal_request_id")!=request or
        response.get("remote_completion")!="response_received"):
        raise ValueError("failed or uncorrelated runtime response")
    if (receipt.get("status")!="STAGED" or receipt.get("model_id")!=model_id or
        receipt.get("program_name")!=program_name or receipt.get("program_sha256")!=program_hash or
        type(receipt.get("bytes")) is not int or receipt["bytes"]!=program_path.stat().st_size or receipt.get("remote_completion")!="response_received"):
        raise ValueError("staging receipt differs from captured program")
    inputs,outputs=_specs(compiled.get("inputs")),_specs(compiled.get("outputs"))
    inp=source["input"]
    if inputs!={inp["name"]:{"shape":inp["shape"],"dtype":np.dtype(inp["dtype"]).name}}:
        raise ValueError("source input ABI differs from compiler")
    for kind,specs in (("inputs",inputs),("outputs",outputs)):
        actual={key:{"shape":v["shape"],"dtype":v["dtype"]} for key,v in capture[kind].items()}
        if actual!=specs:raise ValueError("capture tensor ABI differs from compiler")
    if response.get("outputs")!=outputs:raise ValueError("runtime response output ABI mismatch")
    if decoder=="split_pose_v8":
        if set(outputs)!=set(source["split_outputs"].values()):raise ValueError("split source output names mismatch")
        if source.get("output_shapes")!={key:v["shape"] for key,v in outputs.items()}:raise ValueError("split source output shapes mismatch")
    elif set(outputs)!={source["output_name"]}:raise ValueError("source output name mismatch")
    # Validate actual captured outputs against exact public decoder, without
    # pretending this identity-coordinate decode measures target-video quality.
    shape=inp["shape"]
    if inp.get("layout")!="NCHW" or len(shape)!=4:raise ValueError("MVP source input must be NCHW")
    h,w=shape[2:]
    decode(load_numeric_npz(capture_dir/"outputs.npz"),source,LetterboxTransform(w,h,w,h,w,h,0,0))
    # Allowlist source fields, excluding URLs, account strings and arbitrary SDK metadata.
    keys=("schema_version","model_id","decoder","classes","source_classes","input","output_name","output_layout","nms_in_graph","padding_value","thresholds","versions","opset","keypoint_count","keypoint_order","split_outputs","output_shapes")
    result={key:deepcopy(source[key]) for key in keys if key in source}
    result["linq"]={"runtime_abi_verified":True,"program_path":str(program_path),"program_name":program_name,
        "program_sha256":program_hash,"inputs":[{"name":key,**value} for key,value in inputs.items()],
        "outputs":[{"name":key,**value} for key,value in outputs.items()],
        "input_map":{key:key for key in inputs},"output_map":{key:key for key in outputs},
        "verification_basis":"existing completed status-0 correlated capture; hashes and decoder ABI validated",
        "independent_hardware_attestation":False,"target_video_quality":"NOT_EVALUATED",
        "evidence_paths":{"source_manifest":str(source_path),"compile_report":str(compiled_path),"capture":str(capture_dir/"capture.json"),
                          "response":str(response_path),"staging_receipt":str(receipt_path)}}
    # Explicit local source weight path supports reference diagnostics without any remote URI.
    weights=source.get("artifacts",{}).get("weights",{}).get("file")
    if isinstance(weights,str) and weights and (source_dir/weights).resolve().parent==source_dir.resolve():
        result["weights_path"]=str(source_dir/weights)
    return result
