import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import numpy as np

from ml.safewatch_delivery import (
    COCO80, canonical_classes, combine, digest, prepare, tail_for_outputs,
    token, validate_local, write_eval_labels,
)

try:
    import onnx
    import onnxruntime
except ImportError:
    onnx = None


class ProfileTests(unittest.TestCase):
    def test_coco_subset_registry_does_not_change_head(self):
        self.assertEqual(len(COCO80), 80)
        self.assertEqual(canonical_classes(COCO80, "detector")[7], "truck")
        with self.assertRaises(ValueError):
            canonical_classes(["person"], "detector")
        changed = list(COCO80)
        changed[7] = "forklift"
        with self.assertRaises(ValueError):
            canonical_classes(changed, "detector")

    def test_extra_maps_names_without_inventing_negative_evidence(self):
        self.assertEqual(canonical_classes(["helmet", "bare_head"], "extra"),
                         {0: "helmet", 1: "no_helmet"})
        self.assertEqual(canonical_classes(["flame", "smoke"], "extra", {"flame": "fire"}),
                         {0: "fire", 1: "smoke"})
        for names, mapping in [(["harness"], {"harness": "no_harness"}),
                               (["truck"], {}), (["fire", "flame"], {"flame": "fire"})]:
            with self.assertRaises(ValueError):
                canonical_classes(names, "extra", mapping)

    def test_filename_and_weak_label_guards(self):
        self.assertEqual(token("640-v1"), "640-v1")
        for bad in ["../v1", "v1/path", "v1@other", ""]:
            with self.assertRaises(ValueError): token(bad)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.json"
            source.write_text(json.dumps({"reviewed_complete": False, "videos": []}))
            with self.assertRaises(ValueError):
                write_eval_labels(source, Path(directory) / "eval.yaml")


@unittest.skipIf(onnx is None, "preparation ONNX/ORT environment required")
class GraphTests(unittest.TestCase):
    def make_split(self):
        from onnx import helper, numpy_helper, TensorProto
        arrays = {"boxes": np.arange(12, dtype=np.float32).reshape(1, 4, 3),
                  "scores": np.full((1, 1, 3), .7, np.float32),
                  "xy": np.arange(102, dtype=np.float32).reshape(1, 17, 2, 3),
                  "confidence": np.full((1, 17, 1, 3), .9, np.float32)}
        nodes = [helper.make_node("Constant", [], [n], value=numpy_helper.from_array(a))
                 for n, a in arrays.items()]
        graph = helper.make_graph(nodes, "fixture",
            [helper.make_tensor_value_info("images", TensorProto.FLOAT, [1, 3, 8, 8])],
            [helper.make_tensor_value_info(n, TensorProto.FLOAT, list(a.shape)) for n, a in arrays.items()])
        model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 13)])
        model.ir_version = 7
        manifest = {"decoder": "split_pose_v8", "classes": ["person"],
            "input": {"name": "images", "shape": [1, 3, 8, 8], "layout": "NCHW", "scale": 1/255},
            "split_outputs": {"boxes": "boxes", "class_scores": "scores",
                "keypoint_xy": "xy", "keypoint_scores": "confidence"},
            "keypoint_count": 17, "nms_in_graph": False, "padding_value": 114}
        return model, manifest, arrays

    def test_pose_triplets_are_interleaved_not_xy_then_conf(self):
        from ml.safewatch_delivery import session
        head, source, arrays = self.make_split()
        tail = tail_for_outputs(head, source)
        full = combine(head, tail)
        self.assertEqual(validate_local(full, source, "pose"), 8)
        expected = np.concatenate([arrays["boxes"], arrays["scores"],
            np.concatenate([arrays["xy"], arrays["confidence"]], axis=2).reshape(1, 51, 3)], axis=1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/"full.onnx"
            onnx.save(full, path)
            actual = session(path).run(None, {"images": np.zeros((1, 3, 8, 8), np.float32)})[0]
            np.testing.assert_array_equal(actual, expected)
        broken = dict(source, split_outputs=dict(source["split_outputs"], keypoint_scores="missing"))
        with self.assertRaises(ValueError): tail_for_outputs(head, broken)

    def test_bundle_pins_program_lineage_and_never_overwrites(self):
        head, source, _ = self.make_split()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            onnx_path = directory/"weights.onnx"
            onnx.save(head, onnx_path)
            source["artifacts"] = {"onnx": {"file": onnx_path.name, "sha256": digest(onnx_path)}}
            manifest = directory/"manifest.json"
            manifest.write_text(json.dumps(source))
            target = directory/"bundle"
            release = prepare(manifest, target, "matvey-pose", "640-v1", "pose")
            self.assertEqual(release["statuses"]["new_linq_execution"], "NOT_RUN")
            self.assertIsNone(release["model"]["linq_program"])
            self.assertTrue(release["model"]["linq_tail"].startswith("models/matvey/"))
            before = digest(target/"MANIFEST.json")
            with self.assertRaises(FileExistsError):
                prepare(manifest, target, "matvey-pose", "640-v1", "pose")
            self.assertEqual(digest(target/"MANIFEST.json"), before)
            program = directory/"model.tpu"
            program.write_bytes(b"fixture-only-not-a-TPU-program")
            report = directory/"report.json"
            report.write_text(json.dumps({"compile_status": "PASS", "source_onnx_sha256": "bad",
                                         "program_sha256": digest(program)}))
            with self.assertRaisesRegex(ValueError, "lineage"):
                prepare(manifest, directory/"bad-bundle", "matvey-pose", "640-v1", "pose",
                        compiled=program, compile_report=report)

    def test_cut_graph_keeps_decoded_output_and_revision_tracks_class_order(self):
        from onnx import TensorProto, helper, numpy_helper
        a = np.array([[[4], [4], [2], [2], [.8], [.2]]], np.float32)
        graph = helper.make_graph([
            helper.make_node("Constant", [], ["features"], value=numpy_helper.from_array(a)),
            helper.make_node("Identity", ["features"], ["output0"])], "detect",
            [helper.make_tensor_value_info("images", TensorProto.FLOAT, [1,3,8,8])],
            [helper.make_tensor_value_info("output0", TensorProto.FLOAT, [1,6,1])])
        model = helper.make_model(graph, opset_imports=[helper.make_opsetid("",13)])
        model.ir_version = 7
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            onnx.save(model, base/"weights.onnx")
            source = {"decoder":"detect_v8", "classes":["fire","smoke"],
                "input":{"shape":[1,3,8,8],"layout":"NCHW","scale":1/255},
                "nms_in_graph":False,"padding_value":114,
                "artifacts":{"onnx":{"file":"weights.onnx","sha256":digest(base/"weights.onnx")}}}
            (base/"manifest.json").write_text(json.dumps(source))
            one = prepare(base/"manifest.json",base/"one","matvey-fire","v1","extra",cut_at=["features"])
            two = prepare(base/"manifest.json",base/"two","matvey-fire","v1","extra",
                          mapping={"fire":"smoke","smoke":"fire"})
            self.assertNotEqual(one["model"]["version"],two["model"]["version"])
            self.assertEqual(one["float_parity"]["max_abs_error"],0)

    def test_failed_sdk_attempt_retains_failure_without_hardware_claim(self):
        from ml.safewatch_delivery import compile_cut
        model, _, _ = self.make_split()
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            onnx.save(model,directory/"head.onnx")
            np.savez(directory/"calibration.npz",images=np.zeros((1,3,8,8),np.float32))
            with mock.patch.dict("sys.modules",{"tpu_framework":None}):
                with self.assertRaisesRegex(RuntimeError,"SDK compile failed"):
                    compile_cut(directory/"head.onnx",directory/"calibration.npz",
                                directory/"compile","fixture")
            report = json.loads((directory/"compile/compile-report.json").read_text())
            self.assertEqual(report["compile_status"],"FAIL")
            self.assertEqual(report["failed_stage"],"sdk_import")
            self.assertEqual(report["linq_status"],"NOT_RUN")
            self.assertFalse((directory/"compile/model.tpu").exists())


if __name__ == "__main__": unittest.main()
