import unittest
import numpy as np
from ml.detection import preprocess,decode
from tests.test_detection import manifest

class SplitDetectionTests(unittest.TestCase):
    def setUp(self):
        self.m=manifest();self.split=dict(self.m,decoder='split_detect_v8',split_outputs={'boxes':'b','class_scores':'s'})
        _,self.t=preprocess(np.zeros((320,640,3),np.uint8),self.m)
        self.raw=np.array([[100,200,40,40,.9,.1],[101,201,40,40,.8,.1],[100,200,40,40,.1,.95]],np.float32).T[None]
    def test_host_concat_restores_geometry_probabilities_and_single_nms(self):
        outputs={'b':self.raw[:,:4],'s':self.raw[:,4:]}
        self.assertEqual(decode(self.raw,self.m,self.t),decode(outputs,self.split,self.t))
        self.assertEqual(len(decode(outputs,self.split,self.t)),2)
    def test_invalid_names_shape_logits_and_nonfinite_rejected(self):
        bad=[{'b':self.raw[:,:4],'s':self.raw[:,4:,:1]},
             {'b':self.raw[:,:4],'s':self.raw[:,4:]*2},
             {'b':self.raw[:,:4]*np.nan,'s':self.raw[:,4:]},
             {'b':self.raw[:,:4],'s':self.raw[:,4:],'extra':self.raw}]
        for outputs in bad:
            with self.subTest(outputs=list(outputs)),self.assertRaises(ValueError):decode(outputs,self.split,self.t)
