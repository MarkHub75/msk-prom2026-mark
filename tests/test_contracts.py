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

    def test_boolean_numbers_and_malformed_items_rejected(self):
        for key in ('frame_id', 'media_time_ms'):
            value=batch(0,[person()]);value[key]=True
            with self.assertRaises(ValueError): validate_observation(value)
        for item in (None, {}, {'bbox_xyxy':[0,1],'class_name':'person','score':.9}):
            value=batch(0,[item])
            with self.assertRaises(ValueError): validate_observation(value)
        value=event();value['revision']=True
        with self.assertRaises(ValueError): validate_event(value)

    def test_ready_media_and_retired_epoch_chronology(self):
        value=event();value['evidence']={'status':'ready','snapshot_ref':None}
        with self.assertRaises(ValueError): validate_event(value)

    def test_evidence_pts_is_optional_but_finite_original_media_time(self):
        for invalid in (True,None,-1,float('nan')):
            value=event();value['evidence']['media_time_ms']=invalid
            with self.assertRaises(ValueError):validate_event(value)
        value=event();value['evidence']['media_time_ms']=2000
        self.assertIs(validate_event(value),value)
        value=event();value['end_media_ms']=1000
        with self.assertRaises(ValueError): validate_event(value)
