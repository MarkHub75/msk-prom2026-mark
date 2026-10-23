"""Portable bundled-model preparation and explicit Jupyter call capture.

No notebook execution, authentication, transport discovery, SDK import, export,
training or dtype/codec guessing occurs here. The user supplies the ACTUAL
runtime callable; successful mocks never establish TPU execution.
"""
from __future__ import annotations

from collections.abc import Mapping
import json
from pathlib import Path
import zipfile

import numpy as np

from .backend import TensorSpec
from .notebook import capture_call, _arrays, _file_hash, _name, _save_report, _transform

# Reviewed immutable candidate programs; replacing/recompiling needs a new review.
_CASES = {
    "helmet": {
        "model_id": "helmet-v1", "decoder": "detect_v8", "classes": ["helmet", "bare_head"],
        "program_sha256": "408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa",
    },
    "pose-split": {
        "model_id": "pose-split-v1", "decoder": "split_pose_v8", "classes": ["person"],
        "program_sha256": "c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b",
    },
}
_MAX_BYTES = 256 * 1024 * 1024


class CaseError(ValueError):
    """Stable configuration failure; no private paths or response contents."""


def _require(condition, code):
    if not condition:
        raise CaseError(code)


def _json(path):
    _require(path.stat().st_size <= 1024 * 1024, "json_file_too_large")
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, dict), "json_object_required")
    return value


def _specs(values):
    _require(isinstance(values, list) and bool(values), "nonempty_spec_list_required")
    result = {}
    for value in values:
        _require(isinstance(value, Mapping), "invalid_tensor_spec")
        spec = TensorSpec.parse(value)
        _name(spec.name)
        _require(spec.name not in result, "duplicate_tensor_spec")
        result[spec.name] = {"shape": list(spec.shape), "dtype": spec.dtype}
    return result


def _numeric_npz(path):
    # Bound expanded ZIP payload before numpy can allocate an untrusted array.
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        _require(bool(entries) and len(entries) <= 64, "invalid_npz_entry_count")
        _require(sum(entry.file_size for entry in entries) <= _MAX_BYTES + 64 * 4096,
                 "npz_byte_budget_exceeded")
    with np.load(path, allow_pickle=False) as archive:
        _require(len(set(archive.files)) == len(archive.files), "duplicate_npz_tensor_name")
        return _arrays({name: archive[name] for name in archive.files}, max_bytes=_MAX_BYTES)


def prepare_case(root, name):
    """Load/validate root/models/{helmet|pose-split}, without any runtime call.

    Required files: manifest.json, compile-report.json, model.tpu, inputs.npz,
    golden-outputs.npz, capture-transform.json. The .tpu hash must match both the
    reviewed source pin and compile report. Global kit inventory verification is
    a separate archive-integrity check; this function asserts numeric/spec
    consistency, not independent provenance or hardware execution.

    Returns owned arrays and explicit candidate specs. ``runtime_abi_verified``
    is always False: compile/reference metadata is not observed runtime ABI.
    """
    try:
        _require(isinstance(name, str) and name in _CASES, "unsupported_model_case")
        base = Path(root).resolve()
        directory = (base / "models" / name).resolve()
        _require(directory.is_relative_to(base), "case_path_outside_bundle")
        filenames = ("manifest.json", "compile-report.json", "model.tpu", "inputs.npz",
                     "golden-outputs.npz", "capture-transform.json")
        paths = {}
        for filename in filenames:
            path = (directory / filename).resolve()
            _require(path.is_relative_to(directory) and path.is_file(), "missing_or_external_case_file")
            paths[filename] = path
        expected = _CASES[name]
        manifest = _json(paths["manifest.json"])
        compiled = _json(paths["compile-report.json"])
        _require(manifest.get("model_id") == compiled.get("model_id") == expected["model_id"],
                 "model_identity_mismatch")
        _require(manifest.get("decoder") == expected["decoder"], "wrong_case_decoder")
        _require(manifest.get("classes") == expected["classes"], "wrong_case_class_map")
        _require(manifest.get("nms_in_graph") is False, "unexpected_graph_nms_contract")
        _require(compiled.get("compile_status") == "PASS", "program_not_compiled")
        _require(compiled.get("program_sha256") == expected["program_sha256"],
                 "unreviewed_program_hash")
        program_hash = _file_hash(paths["model.tpu"])
        _require(program_hash == expected["program_sha256"], "program_hash_mismatch")
        source_hash = manifest.get("artifacts", {}).get("onnx", {}).get("sha256")
        _require(isinstance(source_hash, str) and len(source_hash) == 64 and
                 source_hash == compiled.get("source_onnx_sha256"), "source_graph_hash_mismatch")
        input_specs, output_specs = _specs(compiled.get("inputs")), _specs(compiled.get("outputs"))
        # These candidates have one RGB input; no renaming/layout inference.
        manifest_spec = manifest.get("input")
        _require(isinstance(manifest_spec, Mapping), "manifest_input_required")
        one = _specs([manifest_spec])
        _require(one == input_specs, "manifest_compile_input_mismatch")
        inputs = _arrays(_numeric_npz(paths["inputs.npz"]), names=list(input_specs),
                         specs=input_specs, max_bytes=_MAX_BYTES)
        golden = _arrays(_numeric_npz(paths["golden-outputs.npz"]), names=list(output_specs),
                         specs=output_specs, max_bytes=_MAX_BYTES)
        if name == "helmet":
            _require(set(output_specs) == {manifest.get("output_name")}, "manifest_output_names_mismatch")
        else:
            split = manifest.get("split_outputs")
            _require(isinstance(split, dict) and set(split) == {
                "boxes", "class_scores", "keypoint_xy", "keypoint_scores"}, "split_output_roles_required")
            _require(len(set(split.values())) == 4 and set(split.values()) == set(output_specs),
                     "manifest_output_names_mismatch")
            _require(manifest.get("keypoint_count") == 17 and manifest.get("keypoint_order") == "COCO-17",
                     "wrong_keypoint_contract")
            declared_shapes = manifest.get("output_shapes")
            _require(isinstance(declared_shapes, Mapping) and set(declared_shapes) == set(output_specs) and
                     all(declared_shapes[key] == output_specs[key]["shape"] for key in output_specs),
                     "manifest_compile_output_shape_mismatch")
        transform_doc = _json(paths["capture-transform.json"])
        _require(set(transform_doc) == {"original_transform"}, "transform_metadata_not_allowlisted")
        transform = _transform(transform_doc["original_transform"])
        layout = manifest_spec.get("layout")
        shape = manifest_spec["shape"]
        _require(layout in ("NCHW", "NHWC") and len(shape) == 4, "explicit_image_layout_required")
        height, width = (shape[2], shape[3]) if layout == "NCHW" else (shape[1], shape[2])
        _require((transform["input_width"], transform["input_height"]) == (width, height),
                 "transform_input_size_mismatch")
        return {
            "name": name, "model_id": expected["model_id"], "manifest": manifest,
            "compile_report": compiled, "program_path": paths["model.tpu"],
            "program_sha256": program_hash, "inputs": inputs, "golden_outputs": golden,
            "input_specs": input_specs, "output_specs": output_specs,
            "original_transform": transform, "runtime_abi_verified": False,
        }
    except CaseError:
        raise
    except Exception:
        raise CaseError("invalid_case_bundle") from None


def _name_map(value, reference_names):
    if value is None:
        return {name: name for name in reference_names}
    _require(isinstance(value, Mapping) and bool(value), "explicit_tensor_map_required")
    result = {_name(actual): _name(reference) for actual, reference in value.items()}
    _require(set(result.values()) == set(reference_names) and len(result) == len(reference_names),
             "tensor_map_must_cover_reference_once")
    return result


def _runtime_specs(value, name_map, reference_specs):
    if value is None:
        return {actual: dict(reference_specs[reference]) for actual, reference in name_map.items()}
    _require(isinstance(value, Mapping) and set(value) == set(name_map), "runtime_spec_names_mismatch")
    _require(all(isinstance(spec, Mapping) and set(spec) == {"shape", "dtype"} for spec in value.values()),
             "runtime_specs_allow_shape_dtype_only")
    return _specs([{"name": name, **spec} for name, spec in value.items()])


def require_success_status(status, *, success=0):
    """Guard an EXPLICIT extracted numeric status; never parse an API response.

    A user-bound wrapper may call this after the actual supplied call and before
    selecting outputs. The default zero success convention is explicit and can
    be overridden. No assumption about tuple positions, keys or clients is made.
    """
    _require(isinstance(status, (int, np.integer)) and not isinstance(status, (bool, np.bool_)),
             "explicit_numeric_service_status_required")
    _require(type(success) is int, "explicit_numeric_success_code_required")
    _require(int(status) == success, "service_reported_failure")


def capture_case(root, name, run, output_dir, *, input_map=None, output_map=None,
                 runtime_input_specs=None, runtime_output_specs=None,
                 runtime_abi_verified=False, diagnostic_only=False, placement_attested=False):
    """Prepare a pinned case and invoke the explicitly supplied runtime once.

    Maps are runtime-name -> bundled-reference-name, exact one-to-one. None means
    identity, not inferred renaming. No reshape, scaling, cast or codec fix occurs.
    Strict default requires user-attested verified ABI and checks candidate or
    explicitly supplied specs. ``diagnostic_only=True`` permits first-call ABI
    capture: selected outputs need only be finite numeric arrays unless explicit
    runtime_output_specs are supplied. Actual dtype/shape are preserved for review.
    Neither mode modifies the bundled manifest or establishes runtime verification.
    """
    _require(type(runtime_abi_verified) is bool and type(diagnostic_only) is bool,
             "explicit_boolean_capture_mode_required")
    _require(runtime_abi_verified or diagnostic_only, "verify_abi_or_explicitly_select_diagnostic_capture")
    _require(callable(run), "explicit_runtime_callable_required")
    case = prepare_case(root, name)
    inputs_map = _name_map(input_map, case["input_specs"])
    outputs_map = _name_map(output_map, case["output_specs"])
    input_specs = _runtime_specs(runtime_input_specs, inputs_map, case["input_specs"])
    # Inputs must match the exact bundled tensor unless user changes preprocessing
    # in a separately reviewed case. A spec cannot silently cast/reshape it.
    inputs = _arrays({actual: case["inputs"][reference] for actual, reference in inputs_map.items()},
                     specs=input_specs, max_bytes=_MAX_BYTES)
    output_specs = (None if diagnostic_only and runtime_output_specs is None else
                    _runtime_specs(runtime_output_specs, outputs_map, case["output_specs"]))
    result = capture_call(
        run, inputs=inputs, output_names=list(outputs_map), program_path=case["program_path"],
        output_dir=output_dir, model_id=case["model_id"], input_specs=input_specs,
        output_specs=output_specs, runtime_to_reference=outputs_map,
        original_transform=case["original_transform"], placement_attested=placement_attested,
    )
    result["case_config"] = {
        "name": name, "diagnostic_only": diagnostic_only,
        "runtime_abi_verified_attested": runtime_abi_verified,
        "bundled_runtime_abi_verified": False,
        "expected_program_sha256": case["program_sha256"],
        "output_spec_policy": "observed_numeric_only" if output_specs is None else "assert_explicit_specs",
        "input_map": inputs_map, "output_map": outputs_map,
    }
    # capture_call may reject a preexisting directory before invoking anything.
    # Only update a report that belongs to this exact newly generated capture.
    path = Path(output_dir) / "capture.json"
    try:
        stored = _json(path)
        if stored.get("capture_id") == result["capture_id"]:
            _save_report(path, result)
    except Exception:
        if result["status"] != "failed":
            result["status"] = "failed"
            result["error"] = {"phase": "save_case_config", "exception_type": "CaseError"}
    return result
