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

    def test_duplicate_object_keys_cannot_borrow_machine_moving_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('02');pipe=self.pipeline(Path(tmp),config)
            for raw in batches:
                batch=deepcopy(raw);machine=deepcopy(batch['detections'][1]);machine['bbox_xyxy']=[400,300,480,400]
                batch['detections'].append(machine);pipe.process(batch)
            self.assertFalse([c for c in self.candidates(pipe) if c['scenario_id']=='02'])

    def test_real_facts_require_camera_epoch_and_media_binding(self):
        _,batches=build_case('01');batch=batches[0];batch['backend']='linq';batch['source_sha256']='a'*64
        item=batch['scenario_context']['facts'][0];ctx={'batch':batch};key=item['track_key'];name=item['name']
        self.assertIsNone(fact(ctx,key,name))
        item.update(camera_id=batch['camera_id'],stream_epoch=batch['stream_epoch'],source_sha256=batch['source_sha256'])
        self.assertIsNotNone(fact(ctx,key,name))
        for field in ('camera_id','stream_epoch','source_sha256'):
            old=item[field];item[field]='wrong';self.assertIsNone(fact(ctx,key,name));item[field]=old

    def test_replay_writer_lock_is_acquired_before_state_restore(self):
        from ml.scenarios.cli import replay
        from ml.pipeline.runtime_lock import deployment_lock
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with deployment_lock(root/'video.lock'),patch('ml.scenarios.cli.Outbox') as constructor:
                with self.assertRaises(RuntimeError):replay([],root,load_config())
                constructor.assert_not_called()

    def test_site_policy_cannot_apply_to_an_unbound_camera_geometry(self):
        config,_=build_case('02');config.pop('camera_id')
        with self.assertRaises(ValueError):ScenarioSuite(config)

    def test_immobility_candidate_keeps_observed_support_and_confirmation_times(self):
        with tempfile.TemporaryDirectory() as tmp:
            config,batches=build_case('07');pipe=self.pipeline(Path(tmp),config)
            for batch in batches:pipe.process(batch)
            event=next(e for e in self.candidates(pipe) if e['type']=='immobility_observed')
            self.assertEqual(event['start_media_ms'],event['attributes']['immobility_since_media_ms'])
            self.assertEqual(event['confirmed_media_ms'],event['attributes']['immobility_confirmed_media_ms'])


if __name__=='__main__':unittest.main()
