import unittest
import numpy as np
from ml.detection import preprocess, decode


def manifest(decoder="detect_v8", classes=None):
    return {"decoder": decoder, "classes": classes or ["helmet", "bare_head"], "input": {"shape": [1,3,640,640], "dtype": "float32", "layout": "NCHW"}, "thresholds": {"confidence": .25, "iou": .45, "max_detections": 10}}


class CodecTests(unittest.TestCase):
    def test_letterbox_rgb_and_roundtrip_odd_resize(self):
        image = np.zeros((333,777,3), np.uint8); image[:,:,0] = 255
        tensor, t = preprocess(image, manifest())
        self.assertEqual(tensor.shape, (1,3,640,640))
        self.assertTrue(tensor.flags.c_contiguous)
        self.assertEqual(tensor[0,0,t.top,0], 1)
        self.assertEqual(tensor[0,2,t.top,0], 0)
        np.testing.assert_allclose(t.points([[0,t.top],[640,t.top+t.resized_height]]), [[0,0],[777,333]])

    def test_v5_objectness_is_not_v8(self):
        _, t = preprocess(np.zeros((640,640,3),np.uint8),manifest())
        rows = np.array([[[100,100,20,20,.1,.9,.1]]],np.float32)
        self.assertEqual(decode(rows, manifest("detect_v5"), t), [])
        rows[0,0,4] = .9
        result = decode(rows, manifest("detect_v5"), t)
        self.assertAlmostEqual(result[0]["score"], .81, places=5)

    def test_nms_class_aware_and_original_coordinates(self):
        _, t = preprocess(np.zeros((320,640,3),np.uint8),manifest())
        rows = np.array([[100,200,40,40,.9,.1],[101,201,40,40,.8,.1],[100,200,40,40,.1,.95]],np.float32)
        out = decode(rows.T[None], manifest(), t)
        self.assertEqual(len(out),2)
        self.assertEqual(out[0]["class_name"],"bare_head")
        np.testing.assert_allclose(out[0]["bbox_xyxy"],[80,20,120,60])

    def test_pose_geometry(self):
        m = manifest("pose_v8",["person"])
        _, t = preprocess(np.zeros((320,640,3),np.uint8),m)
        row = np.array([100,200,40,40,.9]+[100,200,.8]*17,np.float32)
        out = decode(row[None,:,None],m,t)
        self.assertEqual(len(out[0]["keypoints"]),17)
        np.testing.assert_allclose(out[0]["keypoints"][0],[100,40,.8],atol=1e-6)

    def test_abi_invalid_or_ambiguous_output_rejected(self):
        m=manifest(); _,t=preprocess(np.zeros((2,2,3),np.uint8),m)
        with self.assertRaises(ValueError): decode(np.zeros((1,7,1),np.float32),m,t)
        with self.assertRaises(ValueError): decode({"a":np.zeros((1,6,1)),"b":np.zeros((1,6,1))},m,t)
        with self.assertRaises(ValueError): decode(np.full((1,6,1),np.nan),m,t)
        with self.assertRaises(ValueError): decode(np.zeros((1,6,1)),dict(m,nms_in_graph=True),t)
        self.assertEqual(decode(np.zeros((1,6,0),np.float32),m,t),[])

    def test_input_type_and_logit_rejected(self):
        with self.assertRaises(ValueError): preprocess(np.zeros((2,2,3),np.float32),manifest())
        m=manifest(); _,t=preprocess(np.zeros((2,2,3),np.uint8),m)
        raw=np.array([[[1],[1],[1],[1],[3],[.2]]],np.float32)
        with self.assertRaises(ValueError): decode(raw,m,t)


if __name__ == "__main__": unittest.main()
