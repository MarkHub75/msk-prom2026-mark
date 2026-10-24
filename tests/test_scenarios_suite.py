"""Synthetic integration/failure tests; never model accuracy or TPU execution."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from jsonschema import Draft202012Validator

from ml.behavior import BehaviorEngine
from ml.contracts import validate_event
from ml.pipeline.delivery import Outbox
from ml.pipeline.runner import Pipeline
from ml.scenarios.engine import ScenarioSuite,load_config
from ml.scenarios.fixtures import build_case
from ml.scenarios.contracts import validate_candidate
from ml.scenarios.common import fact


class ScenarioSuiteTests(unittest.TestCase):
    def pipeline(self,root,config):
        box=Outbox(root/'events.sqlite');self.addCleanup(box.close)
        return Pipeline(BehaviorEngine(config.get('behavior')),box,root,scenario_suite=ScenarioSuite(config))

    def candidates(self,pipeline):
        return [json.loads(r[0]) for r in pipeline.outbox.db.execute('SELECT body FROM scenario_candidates ORDER BY rowid')]

    def test_all_eight_positive_negative_unknown_through_same_pipeline(self):
        schema=json.loads((Path(__file__).resolve().parents[1]/'ml/contracts/schemas/event_candidate.schema.json').read_text())
        validator=Draft202012Validator(schema)
        for identity in (f'{i:02d}' for i in range(1,9)):
            for variant in ('positive','negative','unknown'):
                with self.subTest(scenario=identity,variant=variant),tempfile.TemporaryDirectory() as tmp:
                    config,batches=build_case(identity,variant);pipe=self.pipeline(Path(tmp),config)
                    for batch in batches:pipe.process(batch)
                    own=[e for e in self.candidates(pipe) if e['scenario_id']==identity and e['revision']==1]
                    self.assertEqual(bool(own),variant=='positive')
                    for value in self.candidates(pipe):validate_candidate(value);validator.validate(value)
                    for row in pipe.outbox.db.execute('SELECT body FROM outbox'):validate_event(json.loads(row[0]))
                    findings=[f for row in pipe.outbox.db.execute('SELECT body FROM scenario_diagnostics') for f in json.loads(row[0])['findings']]
                    self.assertEqual({f['scenario_id'] for f in findings},set(load_config()['modules']))
                    if variant=='unknown':self.assertTrue(any(f['scenario_id']==identity and f['verdict'] in ('UNKNOWN','BLOCKED') for f in findings))

    def test_exact_evidence_frame_and_source_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('03');root=Path(tmp);pipe=self.pipeline(root,config)
            for batch in batches:pipe.process(batch,np.zeros((480,640,3),dtype=np.uint8))
            event=next(e for e in self.candidates(pipe) if e['scenario_id']=='03')
            evidence=event['evidence'];meta=json.loads((root/evidence['snapshot_ref']).with_suffix('.json').read_text())
            self.assertEqual(meta['media_time_ms'],event['confirmed_media_ms']);self.assertEqual(meta['frame_id'],evidence['frame_id'])
            self.assertEqual(meta['camera_id'],event['camera_id']);self.assertEqual(evidence['status'],'ready')

    def test_restart_replay_and_continuing_episode_do_not_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('03');root=Path(tmp);pipe=self.pipeline(root,config)
            for b in batches[:4]:pipe.process(b)
            other=self.pipeline(root,config)
            for b in batches:other.process(b)
            first=self.candidates(other);self.assertEqual(len([e for e in first if e['scenario_id']=='03' and e['revision']==1]),1)
            for b in batches:other.process(b)
            self.assertEqual(first,self.candidates(other))

    def test_gap_never_accumulates_pending_confirmation(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('03');pipe=self.pipeline(Path(tmp),config)
            pipe.process(batches[0]);pipe.process(batches[1])
            gap={**batches[2],'status':'gap','detections':[]};pipe.process(gap)
            pipe.process(batches[3]);pipe.process(batches[4])
            self.assertFalse(self.candidates(pipe))
            camera=pipe.behavior.export_state()['cameras'][batches[0]['camera_id']]
            key=f"{batches[0]['camera_id']}/{batches[0]['stream_epoch']}/{camera['generation']}/{camera['tracks'][0]['id']}"
            for raw in batches[5:8]:
                observed=deepcopy(raw)
                for value in observed['scenario_context']['facts']:
                    if value['track_key'].startswith(batches[0]['camera_id']+'/'):value['track_key']=key
                pipe.process(observed)
            self.assertTrue(self.candidates(pipe))

    def test_atomic_candidate_failure_rolls_back_both_track_and_event_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('03');pipe=self.pipeline(Path(tmp),config)
            pipe.process(batches[0]);pipe.process(batches[1])
            behavior,suite=pipe.behavior.export_state(),pipe.scenario_suite.export_state()
            original=pipe.candidate_journal.commit
            def broken(*args):original(*args);raise OSError('synthetic transaction failure')
            with patch.object(pipe.candidate_journal,'commit',side_effect=broken):
                with self.assertRaises(OSError):pipe.process(batches[2])
            self.assertEqual(behavior,pipe.behavior.export_state());self.assertEqual(suite,pipe.scenario_suite.export_state())
            self.assertEqual(len(self.candidates(pipe)),0)
            pipe.process(batches[2]);self.assertTrue(self.candidates(pipe))

    def test_changed_committed_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('03');pipe=self.pipeline(Path(tmp),config);pipe.process(batches[0])
            changed=deepcopy(batches[0]);changed['detections']=[]
            with self.assertRaises(ValueError):pipe.process(changed)

    def test_source_epoch_does_not_borrow_pending_duration(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('01');pipe=self.pipeline(Path(tmp),config)
            pipe.process(batches[0]);pipe.process(batches[1])
            reset=deepcopy(batches[0]);reset['stream_epoch']='new-epoch';reset['scenario_context']['facts']=[]
            pipe.process(reset)
            for b in batches[:2]:pipe.process(b) # retired results are ignored
            self.assertFalse(self.candidates(pipe))

    def test_invalid_or_duplicate_facts_never_become_observed(self):
        _,batches=build_case('01');ctx={'batch':batches[0]};value=batches[0]['scenario_context']['facts'][0]
        self.assertIsNotNone(fact(ctx,value['track_key'],value['name']))
        batches[0]['scenario_context']['facts'].append(deepcopy(value));self.assertIsNone(fact(ctx,value['track_key'],value['name']))
        batches[0]['scenario_context']['facts']=[{**value,'media_time_ms':1}];self.assertIsNone(fact(ctx,value['track_key'],value['name']))

    def test_existing_external_contract_rejects_new_candidate_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('03');pipe=self.pipeline(Path(tmp),config)
            for b in batches:pipe.process(b)
            event=next(e for e in self.candidates(pipe) if e['scenario_id']=='03')
            with self.assertRaises(ValueError):validate_event(event)


if __name__=='__main__':unittest.main()
