import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import numpy as np
from ml.detection.compare_capture import compare_captures, load_numeric_npz


def pose_fixture():
    count=2
    m={"decoder":"split_pose_v8","classes":["person"],"keypoint_count":17,
       "input":{"shape":[1,3,640,640],"layout":"NCHW"},
       "split_outputs":{"boxes":"b","class_scores":"s","keypoint_xy":"xy","keypoint_scores":"kp"}}
    arrays={"b":np.array([[[100,400],[200,400],[40,40],[40,40]]],np.float32),
            "s":np.array([[[.9,.8]]],np.float32),"xy":np.full((1,17,2,count),100,np.float32),"kp":np.full((1,17,1,count),.8,np.float32)}
    meta={"original_transform":{"original_width":640,"original_height":320,"input_width":640,"input_height":640,"resized_width":640,"resized_height":320,"left":0,"top":160}}
    return m,arrays,meta


class CaptureTests(unittest.TestCase):
    def test_explicit_mapping_numeric_changes_no_acceptance(self):
        reference={"expected":np.array([0.,2.],np.float32)}
        actual={"runtime":np.array([.1,2.2],np.float32)}
        r=compare_captures(reference,actual,{"runtime":"expected"},relative_epsilon=.1)
        self.assertEqual(r["status"],"COMPARED")
        self.assertAlmostEqual(r["outputs"]["expected"]["absolute"]["max"],.2,places=6)
        self.assertAlmostEqual(r["outputs"]["expected"]["relative"]["max"],1,places=6)
        self.assertEqual(r["target_quality"],"NOT_EVALUATED")
        self.assertEqual(r["hardware_execution"],"NOT_ESTABLISHED_BY_COMPARISON")
        self.assertEqual(r["decoded"]["status"],"SKIPPED")
        self.assertEqual(compare_captures(reference,actual)["status"],"INVALID_CAPTURE")

    def test_finite_shape_dtype_and_name_checks(self):
        a={"x":np.array([1.],np.float32)}
        for b,status in [({"x":np.array([np.nan],np.float32)},"NONFINITE"),
                         ({"x":np.array([1.,2.],np.float32)},"SHAPE_MISMATCH"),
                         ({"x":np.array([1.],np.float64)},"DTYPE_MISMATCH")]:
            r=compare_captures(a,b)
            self.assertEqual(r["status"],"INVALID_CAPTURE")
            self.assertEqual(r["outputs"]["x"]["status"],status)
        self.assertEqual(compare_captures(a,dict(a,extra=np.array([1.])))["status"],"INVALID_CAPTURE")
        with self.assertRaises(ValueError):compare_captures(a,a,{"a":"x","b":"x"})

    def test_pickle_strings_and_complex_not_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/"capture.npz"
            for array in [np.array([{}],object),np.array(["secret"],str),np.array([1j])]:
                np.savez(p,x=array)
                with self.assertRaises(ValueError):load_numeric_npz(p)
            np.savez(p,x=np.array([1.,2.],np.float32))
            self.assertEqual(load_numeric_npz(p)["x"].dtype,np.float32)

    def test_decoded_split_identity_and_capture_metadata_mapping(self):
        m,a,meta=pose_fixture()
        actual={"runtime_"+k:v.copy() for k,v in a.items()}
        meta["runtime_to_reference"]={"runtime_"+k:k for k in a}
        r=compare_captures(a,actual,manifest=m,metadata=meta)
        self.assertEqual(r["decoded"]["status"],"COMPARED")
        self.assertEqual(r["decoded"]["reference_count"],2)
        self.assertEqual(len(r["decoded"]["pairs"]),2)
        self.assertEqual(r["decoded"]["pairs"][0]["keypoints"]["jointly_visible_xy_l2_pixels"]["max"],0)
        self.assertEqual(r["decoded"]["unmatched_actual_indices"],[])
        actual["runtime_s"][:]=0
        r=compare_captures(a,actual,manifest=m,metadata=meta)
        self.assertEqual(r["status"],"COMPARED")
        self.assertEqual(r["decoded"]["actual_count"],0)
        self.assertEqual(r["decoded"]["unmatched_reference_indices"],[0,1])

    def test_transform_missing_or_invalid_is_explicit(self):
        m,a,meta=pose_fixture()
        self.assertEqual(compare_captures(a,a,manifest=m)["decoded"]["status"],"SKIPPED")
        self.assertEqual(compare_captures(a,a,manifest=m,metadata={})["decoded"]["status"],"SKIPPED")
        meta["original_transform"]["input_width"]=12
        self.assertEqual(compare_captures(a,a,manifest=m,metadata=meta)["decoded"]["status"],"INVALID_METADATA_OR_OUTPUT")

    def test_large_integer_precision_and_empty_arrays(self):
        a={"x":np.array([2**63],np.uint64)}
        self.assertEqual(compare_captures(a,a)["outputs"]["x"]["status"],"INVALID_NUMERIC_RANGE")
        a={"x":np.array([],np.float32)};r=compare_captures(a,a)
        self.assertEqual(r["status"],"COMPARED")
        self.assertIsNone(r["outputs"]["x"]["absolute"]["max"])
        json.dumps(r,allow_nan=False)

    def test_cli_numeric_difference_exit_zero_is_not_tolerance_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory);np.savez(p/"ref.npz",x=np.array([1.],np.float32));np.savez(p/"actual.npz",x=np.array([100.],np.float32))
            command=[sys.executable,"-m","ml.detection.compare_capture","--reference",str(p/"ref.npz"),"--actual",str(p/"actual.npz"),"--output",str(p/"report.json")]
            result=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            r=json.loads((p/"report.json").read_text())
            self.assertEqual(r["target_quality"],"NOT_EVALUATED")
            self.assertEqual(r["outputs"]["x"]["absolute"]["max"],99.)
            np.savez(p/"actual.npz",x=np.array([np.inf],np.float32))
            self.assertEqual(subprocess.run(command,capture_output=True,text=True).returncode,2)


if __name__=="__main__":unittest.main()
