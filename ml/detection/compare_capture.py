"""Compare named numeric captures without claiming hardware execution or quality.

The actual NPZ contains explicit runtime output names. A JSON name map is
runtime-name -> reference-name; omitted map means identity names, never inferred
from shapes. Inputs/outputs must be exported separately as numeric-only NPZ.
"""
import argparse
from dataclasses import fields
import json
from pathlib import Path
import numpy as np
from .codec import LetterboxTransform, decode
from .export import sha256


def load_numeric_npz(path):
    """Load owned numeric arrays only; pickle/object/string/complex are forbidden."""
    with np.load(path, allow_pickle=False) as archive:
        values = {}
        for name in archive.files:
            if name in values:
                raise ValueError("duplicate NPZ tensor name")
            array = archive[name]
            if array.dtype.kind not in "iuf":
                raise ValueError(f"tensor {name!r} is not a real numeric array")
            values[name] = array.copy()
    if not values:
        raise ValueError("empty tensor capture")
    return values


def _summary(values):
    array = np.asarray(values, dtype=np.float64).reshape(-1)
    if not array.size:
        return {"count": 0, "mean": None, "max": None, "p95": None}
    return {"count": int(array.size), "mean": float(array.mean()), "max": float(array.max()), "p95": float(np.percentile(array,95))}


def _differences(reference, actual, relative_epsilon):
    # float64 avoids subtraction overflow for integer captures. Integer types
    # above exact float64 range are rejected instead of silently rounded.
    for array in (reference,actual):
        if array.dtype.kind in "iu" and array.size and np.any(np.abs(array.astype(np.longdouble)) > 2**53):
            raise ValueError("integer capture exceeds exact float64 comparison range")
    a,b=np.asarray(reference,np.float64),np.asarray(actual,np.float64)
    absolute=np.abs(a-b)
    relative=absolute/np.maximum(np.abs(a),relative_epsilon)
    if not np.all(np.isfinite(absolute)) or not np.all(np.isfinite(relative)):
        raise ValueError("numeric difference overflow")
    return {"absolute":_summary(absolute), "relative":_summary(relative),
            "relative_definition":"abs(actual-reference)/max(abs(reference),epsilon)",
            "relative_epsilon":relative_epsilon, "exact_equal":bool(np.array_equal(reference,actual))}


def _validated_transform(metadata,manifest):
    if metadata is None or "original_transform" not in metadata:
        return None
    value=metadata["original_transform"]
    keys={f.name for f in fields(LetterboxTransform)}
    if not isinstance(value,dict) or set(value)!=keys or any(not isinstance(v,int) or isinstance(v,bool) for v in value.values()):
        raise ValueError("original_transform must contain exact integer LetterboxTransform fields")
    t=LetterboxTransform(**value)
    if min(t.original_width,t.original_height,t.input_width,t.input_height,t.resized_width,t.resized_height)<=0 or min(t.left,t.top)<0:
        raise ValueError("invalid original_transform dimensions")
    if t.left+t.resized_width>t.input_width or t.top+t.resized_height>t.input_height:
        raise ValueError("resized image falls outside model input")
    spec=manifest["input"];shape=spec["shape"];layout=spec.get("layout","NCHW")
    if layout=="NCHW":height,width=shape[2:4]
    elif layout=="NHWC":height,width=shape[1:3]
    else:raise ValueError("unknown manifest input layout")
    if (t.input_height,t.input_width)!=(height,width):
        raise ValueError("transform/manifest input dimensions differ")
    return t


def _iou(a,b):
    a,b=np.asarray(a,float),np.asarray(b,float)
    inter=float(np.maximum(np.minimum(a[2:],b[2:])-np.maximum(a[:2],b[:2]),0).prod())
    union=float(np.maximum(a[2:]-a[:2],0).prod()+np.maximum(b[2:]-b[:2],0).prod()-inter)
    return inter/max(union,1e-12)


def compare_decoded(reference,actual,min_match_iou=.1):
    """Class-aware greedy IoU pairing for diagnostics, never GT/quality scoring."""
    candidates=[]
    for i,a in enumerate(reference):
        for j,b in enumerate(actual):
            iou=_iou(a["bbox_xyxy"],b["bbox_xyxy"])
            if a["class_name"]==b["class_name"] and iou>min_match_iou:
                candidates.append((-iou,i,j))
    used_a,used_b=set(),set();pairs=[]
    for neg_iou,i,j in sorted(candidates):
        if i in used_a or j in used_b:continue
        used_a.add(i);used_b.add(j);a,b=reference[i],actual[j]
        pair={"reference_index":i,"actual_index":j,"class_name":a["class_name"],"box_iou":-neg_iou,
              "box_absolute_pixel_difference":_summary(np.abs(np.asarray(a["bbox_xyxy"])-np.asarray(b["bbox_xyxy"]))),
              "score_absolute_difference":abs(a["score"]-b["score"])}
        ka,kb=a.get("keypoints"),b.get("keypoints")
        if ka is not None and kb is not None:
            ka,kb=np.asarray(ka,float),np.asarray(kb,float)
            if ka.shape!=kb.shape:pair["keypoints"]={"status":"SHAPE_MISMATCH"}
            else:
                visible=(ka[:,2]>=.5)&(kb[:,2]>=.5)
                pair["keypoints"]={"status":"COMPARED","confidence_absolute_difference":_summary(abs(ka[:,2]-kb[:,2])),
                    "reference_visible_at_0_5":int((ka[:,2]>=.5).sum()),"actual_visible_at_0_5":int((kb[:,2]>=.5).sum()),
                    "jointly_visible_count":int(visible.sum()),"jointly_visible_xy_l2_pixels":_summary(np.linalg.norm(ka[visible,:2]-kb[visible,:2],axis=1))}
        pairs.append(pair)
    return {"status":"COMPARED","reference_count":len(reference),"actual_count":len(actual),"pairs":pairs,
            "unmatched_reference_indices":sorted(set(range(len(reference)))-used_a),
            "unmatched_actual_indices":sorted(set(range(len(actual)))-used_b),
            "pairing":"class-aware greedy descending IoU, diagnostic only", "min_match_iou":min_match_iou,
            "quality_acceptance":"NOT_EVALUATED"}


def compare_captures(reference,actual,runtime_to_reference=None,manifest=None,metadata=None,relative_epsilon=1e-8,min_match_iou=.1):
    if not np.isfinite(relative_epsilon) or relative_epsilon<=0 or not 0<=min_match_iou<=1:
        raise ValueError("invalid comparison parameters")
    if runtime_to_reference is None and metadata is not None:
        runtime_to_reference=metadata.get("runtime_to_reference")
    names=dict(runtime_to_reference) if runtime_to_reference is not None else {key:key for key in actual}
    if any(not isinstance(k,str) or not isinstance(v,str) for k,v in names.items()) or len(set(names.values()))!=len(names):
        raise ValueError("name map must be one-to-one strings runtime -> reference")
    unmapped_actual=sorted(set(actual)-set(names));missing_actual=sorted(set(names)-set(actual))
    unmapped_reference=sorted(set(reference)-set(names.values()));unknown_reference=sorted(set(names.values())-set(reference))
    report={"schema_version":"1.0","status":"COMPARED","scope":"named tensor numerical comparison only",
            "hardware_execution":"NOT_ESTABLISHED_BY_COMPARISON","target_quality":"NOT_EVALUATED",
            "name_map":names,"unmapped_actual":unmapped_actual,"missing_actual":missing_actual,
            "unmapped_reference":unmapped_reference,"unknown_reference":unknown_reference,"outputs":{},
            "decoded":{"status":"SKIPPED","reason":"manifest or original_transform metadata unavailable"}}
    invalid=bool(unmapped_actual or missing_actual or unmapped_reference or unknown_reference)
    renamed={}
    for actual_name,reference_name in names.items():
        if actual_name not in actual or reference_name not in reference:continue
        a,b=np.asarray(reference[reference_name]),np.asarray(actual[actual_name]);item={"actual_name":actual_name,"reference_shape":list(a.shape),"actual_shape":list(b.shape),"reference_dtype":str(a.dtype),"actual_dtype":str(b.dtype)}
        reason=None
        if a.dtype.kind not in "iuf" or b.dtype.kind not in "iuf":reason="NON_NUMERIC_DTYPE"
        elif not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):reason="NONFINITE"
        elif a.shape!=b.shape:reason="SHAPE_MISMATCH"
        elif a.dtype!=b.dtype:reason="DTYPE_MISMATCH"
        if reason:item["status"]=reason;invalid=True
        else:
            try:item.update(status="COMPARED",**_differences(a,b,relative_epsilon));renamed[reference_name]=b
            except ValueError as exc:item.update(status="INVALID_NUMERIC_RANGE",reason=str(exc));invalid=True
        report["outputs"][reference_name]=item
    if not reference or not actual:invalid=True
    if invalid:
        report["status"]="INVALID_CAPTURE"
        report["decoded"]={"status":"SKIPPED","reason":"tensor/name validation failed"}
    elif manifest is not None and metadata is not None:
        try:
            transform=_validated_transform(metadata,manifest)
            if transform is not None:
                report["decoded"]=compare_decoded(decode(reference,manifest,transform),decode(renamed,manifest,transform),min_match_iou)
        except (ValueError,KeyError,TypeError) as exc:
            report["decoded"]={"status":"INVALID_METADATA_OR_OUTPUT","reason":str(exc)}
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--reference",required=True);p.add_argument("--actual",required=True)
    p.add_argument("--name-map",help="JSON object actual runtime output name -> reference output name")
    p.add_argument("--manifest");p.add_argument("--metadata",help="JSON with original_transform dataclass fields")
    p.add_argument("--relative-epsilon",type=float,default=1e-8);p.add_argument("--min-match-iou",type=float,default=.1)
    p.add_argument("--output",required=True);a=p.parse_args()
    read=lambda path:json.loads(Path(path).read_text()) if path else None
    try:
        report=compare_captures(load_numeric_npz(a.reference),load_numeric_npz(a.actual),read(a.name_map),read(a.manifest),read(a.metadata),a.relative_epsilon,a.min_match_iou)
        report["captures"]={"reference_sha256":sha256(a.reference),"actual_sha256":sha256(a.actual)}
    except (ValueError,TypeError,KeyError,OSError) as exc:
        report={"schema_version":"1.0","status":"INVALID_CAPTURE","reason":str(exc),"hardware_execution":"NOT_ESTABLISHED_BY_COMPARISON","target_quality":"NOT_EVALUATED"}
    Path(a.output).write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"hardware_execution":report["hardware_execution"],"target_quality":report["target_quality"]}))
    if report["status"]!="COMPARED":raise SystemExit(2)


if __name__=="__main__":main()
