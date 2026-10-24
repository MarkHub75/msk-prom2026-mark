"""Synthetic stage-attribution contracts; not additional model experiments."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from ml.quality.temporal.observation_audit import attribute,xml_index,audit
from ml.quality.temporal.caviar import digest


def obj(box=None):return {'bbox_xyxy_original':box or [10,10,30,50]}
def person(score=.8,box=None):return {'class_name':'person','score':score,'bbox_xyxy':box or [10,10,30,50],'detection_id':'p','keypoints':None}


class ObservationAuditTests(unittest.TestCase):
    def test_decoder_absence_is_not_consumer_threshold_loss(self):
        self.assertEqual(attribute([obj()],[],0)['category'],'no_decoded_person')
        self.assertEqual(attribute([obj()],[{**person(),'class_name':'machine'}],0)['category'],'no_decoded_person')

    def test_existing_decoder_and_consumer_stages_are_distinct(self):
        for score in (.25,.499999):
            r=attribute([obj()],[person(score)],0)
            self.assertEqual(r['category'],'consumer_score_gate')
            self.assertTrue(r['decoder_unique_owner']);self.assertFalse(r['consumer_unique_owner'])
        self.assertEqual(attribute([obj()],[person(.5)],0,True)['category'],'consumer_unique_anchor_observed')
        self.assertEqual(attribute([obj()],[person(.5)],0,False)['category'],'pose_anchor_or_track_gap')

    def test_localization_does_not_become_score_gate_or_actor_credit(self):
        r=attribute([obj()],[person(.9,[100,100,130,150])],0)
        self.assertEqual(r['category'],'localization_below_ownership_iou')
        self.assertEqual(r['best_decoded_person_iou'],0)

    def test_ambiguous_ownership_is_not_resolved_greedily(self):
        self.assertEqual(attribute([obj(),obj()],[person(.8)],0)['category'],'ambiguous_ownership')
        self.assertEqual(attribute([obj()],[person(.8),person(.9)],0)['category'],'ambiguous_ownership')

    def test_native_xml_center_geometry_and_labels_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'source.xml';p.write_text('<dataset name="Synthetic"><frame number="5"><objectlist><object id="2"><box xc="4" yc="20" w="12" h="10"/><appearance>visible</appearance><hypothesislist><hypothesis><movement>running</movement></hypothesis></hypothesislist></object></objectlist></frame></dataset>')
            name,rows=xml_index(p)
            self.assertEqual(name,'Synthetic');self.assertEqual(rows[(5,'2')]['bbox'],[-2,15,10,25])
            self.assertEqual(rows[(5,'2')]['movement_values'],['running'])

    def _fixture(self,root):
        seq='Synthetic';xml=root/'source.xml';xml.write_text('<dataset name="Synthetic"><frame number="0"><objectlist><object id="0"><box xc="20" yc="30" w="20" h="40"/><appearance>visible</appearance><hypothesislist><hypothesis><movement>running</movement></hypothesis></hypothesislist></object></objectlist></frame></dataset>')
        row={'sequence':seq,'frame_id_from_source_filename':0,'frame_index0':0,'canonical_frame_time_ms':0,'width':100,'height':100,'path':str(root/'Synthetic000.jpg'),'bytes':1,'sha256':'a'*64,'source_annotation_path':str(xml),
            'source_objects':[{'source_object_id':'0','track_id':'Synthetic:0','bbox_xyxy_original':[10,10,30,50],'appearance':'visible','movement_values':['running']}]}
        annotation=root/'frame_annotations.jsonl';annotation.write_text(json.dumps(row)+'\n')
        selected=root/'selected.jsonl';selected.write_text(json.dumps(row)+'\n')
        manifest=root/'manifest.json';manifest.write_text('{}')
        protocol=root/'protocol.json';protocol.write_text(json.dumps({'baseline':{'running_only':True,'speed_units':'image_diagonals_per_second','speed_threshold':.2,'min_score':.5,'keypoint_score':.5},'hashes':{str(manifest):digest(manifest),str(annotation):digest(annotation)}}))
        batch={'schema_version':'1.0','camera_id':seq,'stream_epoch':'synthetic-epoch','frame_id':0,'media_time_ms':0,'image_size':[100,100],'status':'ok','backend':'synthetic-test','detections':[person()]}
        obs=root/'observations.jsonl';obs.write_text(json.dumps({'video_id':seq,'batch':batch,'input_sha256':'a'*64})+'\n')
        model=root/'model.json';model.write_text(json.dumps({'thresholds':{'confidence':.25}}))
        execution=root/'run.json';execution.write_text(json.dumps({'status':'COMPLETED','observations_sha256':digest(obs),'protocol_sha256':digest(protocol),'selected_inputs_sha256':digest(selected),'model_manifest_sha256':digest(model)}))
        return protocol,selected,obs,execution,model,'synthetic-pointer'

    def test_full_saved_record_audit_has_no_inference_and_counts_anchor_gap(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);args=self._fixture(root)
            with patch('ml.quality.temporal.observation_audit.load_producer_ready',return_value=({'absolute_path':str(root)},{'synthetic':True})):
                r=audit(*args,root/'output')
            self.assertFalse(r['new_inference']);self.assertFalse(r['threshold_sweep'])
            self.assertEqual(r['totals'],{'running:pose_anchor_or_track_gap':1})
            self.assertEqual(r['checks']['native_xml_actor_boxes_verified'],1)

    def test_tampered_model_identity_rejected_before_attribution(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);args=self._fixture(root);Path(args[4]).write_text('{"thresholds":{"confidence":0.1}}')
            with patch('ml.quality.temporal.observation_audit.load_producer_ready',return_value=({'absolute_path':str(root)},{})):
                with self.assertRaisesRegex(ValueError,'decoder'):audit(*args,root/'output')

if __name__=='__main__':unittest.main()
