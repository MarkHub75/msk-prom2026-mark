"""Expose pose probabilities BEFORE coordinate/probability concatenation.

This graph surgery adds no Gather after the mixed tensor: it extracts the
upstream boxes, class probability, keypoint XY and keypoint probability tensors
and prunes both the mixed keypoint concat and terminal detection concat.
"""
import argparse
import copy
import json
from pathlib import Path
import shutil
from .export import sha256


def export_split_pose(source_manifest, output_dir, model_id="pose-split-v1"):
    import onnx
    from onnx import helper, TensorProto
    source_manifest, output_dir = Path(source_manifest), Path(output_dir)
    manifest = json.loads(source_manifest.read_text())
    if manifest["decoder"] != "pose_v8" or manifest.get("keypoint_count", 17) != 17:
        raise ValueError("requires decoded COCO-17 pose_v8 source")
    source_graph = source_manifest.parent / manifest["artifacts"]["onnx"]["file"]
    graph = onnx.shape_inference.infer_shapes(onnx.load(source_graph))
    nodes = {name: node for node in graph.graph.node for name in node.output}
    final = nodes[manifest["output_name"]]
    if final.op_type != "Concat" or len(final.input) != 3:
        raise ValueError("expected final boxes/classes/keypoints Concat")
    kp_reshape = nodes[final.input[2]]
    if kp_reshape.op_type != "Reshape":
        raise ValueError("expected keypoint flattening Reshape")
    mixed = nodes[kp_reshape.input[0]]
    if mixed.op_type != "Concat" or len(mixed.input) != 2:
        raise ValueError("expected pre-flatten keypoint XY/probability Concat")
    if nodes[mixed.input[1]].op_type != "Sigmoid" or nodes[final.input[1]].op_type != "Sigmoid":
        raise ValueError("class/keypoint confidence must already be probabilities")
    names = dict(zip(("boxes", "class_scores", "keypoint_xy", "keypoint_scores"),
                     (final.input[0], final.input[1], mixed.input[0], mixed.input[1])))
    # Extractor follows tensor producers backwards. Descendant mixed concats are
    # unreachable and therefore removed, not retained then sliced at graph output.
    extractor = onnx.utils.Extractor(graph)
    result = extractor.extract_model([graph.graph.input[0].name], list(names.values()))
    anchor_count = next(v for v in graph.graph.value_info if v.name == names["class_scores"]).type.tensor_type.shape.dim[-1].dim_value
    if anchor_count < 1:
        raise ValueError("requires static anchor dimension")
    shapes = {"boxes": [1,4,anchor_count], "class_scores": [1,len(manifest["classes"]),anchor_count], "keypoint_xy": [1,17,2,anchor_count], "keypoint_scores": [1,17,1,anchor_count]}
    del result.graph.output[:]
    for semantic, name in names.items():
        result.graph.output.append(helper.make_tensor_value_info(name, TensorProto.FLOAT, shapes[semantic]))
    output_tensors = {name for n in result.graph.node for name in n.output}
    if mixed.output[0] in output_tensors or final.output[0] in output_tensors:
        raise ValueError("mixed coordinate/probability concat unexpectedly retained")
    onnx.checker.check_model(result)
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "weights.onnx"
    onnx.save(result, destination)
    target_manifest = copy.deepcopy(manifest)
    target_manifest.update(model_id=model_id, decoder="split_pose_v8", split_outputs=names,
                           output_shapes={names[k]: v for k,v in shapes.items()},
                           source_onnx_sha256=sha256(source_graph), linq_status="NOT_RUN")
    target_manifest.pop("output_name", None)
    target_manifest["artifacts"]["onnx"] = {"file": destination.name, "sha256": sha256(destination)}
    # Preserve a self-contained immutable package including trusted source weights.
    source_weights = source_manifest.parent / manifest["artifacts"]["weights"]["file"]
    destination_weights = output_dir / "weights.pt"
    if source_weights.resolve() != destination_weights.resolve():
        shutil.copy2(source_weights, destination_weights)
    target_manifest["artifacts"]["weights"]["file"] = destination_weights.name
    target_manifest["graph_surgery"] = {"kind": "pre_concat_output_extraction", "removed_outputs": [mixed.output[0], final.output[0]], "host_operations": "concatenate/reshape only; no repeated sigmoid, coordinate or neural decode"}
    path = output_dir / "manifest.json"
    path.write_text(json.dumps(target_manifest, indent=2) + "\n")
    return path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", required=True); p.add_argument("--output", required=True)
    p.add_argument("--model-id", default="pose-split-v1")
    a=p.parse_args(); print(export_split_pose(a.manifest,a.output,a.model_id))


if __name__ == "__main__": main()
