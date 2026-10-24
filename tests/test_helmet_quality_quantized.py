import unittest
from unittest.mock import patch
from ml.quality.helmet.quantized import comparison, verified_inputs

class QuantizedPolicyTests(unittest.TestCase):
    def metric(self,f=.7,r=.8,fp=4):
        return {'classes':{c:{'f1':f,'recall':r,'fp':fp} for c in ('helmet','bare_head')}}
    def test_gain_cannot_override_recall_or_false_positive_guard(self):
        base=self.metric()
        self.assertTrue(comparison(base,self.metric(.72))['accepted'])
        self.assertFalse(comparison(base,self.metric(.72,.77))['accepted'])
        self.assertFalse(comparison(base,self.metric(.72,fp=5))['accepted'])
        self.assertFalse(comparison(base,self.metric(.705))['accepted'])
    def test_changed_ready_rejected_before_dataset_load(self):
        with patch('ml.quality.helmet.quantized.sha256',return_value='0'*64),patch('ml.quality.helmet.quantized.load_ready') as load:
            with self.assertRaises(ValueError): verified_inputs('changed.json')
            load.assert_not_called()
    def test_undefined_primary_cannot_pass(self):
        with self.assertRaises(ValueError): comparison(self.metric(None),self.metric())
