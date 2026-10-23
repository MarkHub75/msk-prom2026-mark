import copy
import unittest
from ml.contracts import validate_observation, validate_event
from test_behavior import batch, person
from test_delivery import event

class ContractsTest(unittest.TestCase):
    def test_unknown_version_and_nonfinite_keypoints_rejected(self):
        value=batch(0,[person()]);value['schema_version']='2.0'
        with self.assertRaises(ValueError): validate_observation(value)
        value=batch(0,[person()]);value['detections'][0]['keypoints'][0][0]=float('nan')
        with self.assertRaises(ValueError): validate_observation(value)

    def test_gap_cannot_smuggle_positive_observations(self):
        value=batch(0,[person()]);value['status']='gap'
        with self.assertRaises(ValueError): validate_observation(value)

    def test_revision_and_times_are_validated(self):
        value=event();value['confirmed_media_ms']=float('nan')
        with self.assertRaises(ValueError): validate_event(value)
        value=event();value['schema_version']='2.0'
        with self.assertRaises(ValueError): validate_event(value)
