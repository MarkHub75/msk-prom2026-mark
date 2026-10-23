"""Synthetic temporal acceptance through the actual Pipeline and SQLite Outbox.

No neural model, camera, LinQ hardware or production receiver is exercised.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from ml.behavior import BehaviorEngine
from ml.behavior.scenarios import SCENARIOS, build_scenario, generate
from ml.contracts import validate_observation
from ml.pipeline.delivery import Outbox
from ml.pipeline.runner import Pipeline, read_jsonl


class IdempotentReceiver:
    """Test double for the documented backend contract, not a shipped backend."""
    def __init__(self, *, lose_first_ack=False):
        self.records = {}
        self.notifications = set()
        self.attempts = 0
        self.lose_first_ack = lose_first_ack

    def publish(self, event):
        self.attempts += 1
        key = (event["event_id"], event["revision"])
        if key in self.records and self.records[key] != event:
            raise AssertionError("same event revision changed across retry")
        self.records[key] = deepcopy(event)
        if event["revision"] == 1 and event["state"] == "open":
            self.notifications.add(event["event_id"])
        if self.lose_first_ack:
            self.lose_first_ack = False
            raise TimeoutError("synthetic ACK loss after receiver commit")
        return {"committed": True, "event_id": event["event_id"], "revision": event["revision"]}


class TemporalAcceptance(unittest.TestCase):
    def assert_semantics(self, events, expectation):
        incidents = {}
        for event in events:
            self.assertEqual(event["execution_backend"], "synthetic-test")
            incidents.setdefault(event["event_id"], []).append(event)
        actual = list(incidents.values())
        expected = expectation["expected_incidents"]
        self.assertEqual(len(actual), len(expected))
        for revisions, target in zip(actual, expected):
            self.assertEqual([v["state"] for v in revisions], target["states"])
            self.assertEqual([v["revision"] for v in revisions], target["revisions"])
            self.assertEqual({v["type"] for v in revisions}, {target["type"]})
            self.assertEqual({v["confirmed_media_ms"] for v in revisions}, {target["confirmed_media_ms"]})
            self.assertEqual({v["stream_epoch"] for v in revisions}, {target["stream_epoch"]})
            self.assertEqual(bool(revisions[-1].get("attributes", {}).get("immobility_observed")), target["immobility_observed"])
            self.assertEqual(sum(bool(v.get("attributes", {}).get("immobility_observed")) for v in revisions), int(target["immobility_observed"]))
            if "end_media_ms" in target:
                self.assertEqual(revisions[-1]["end_media_ms"], target["end_media_ms"])
            for event in revisions:
                if "end_media_ms" in event:
                    self.assertGreaterEqual(event["end_media_ms"], event["confirmed_media_ms"])

    def test_scenarios_through_pipeline_restart_replay_and_delivery(self):
        for name in SCENARIOS:
            with self.subTest(scenario=name), tempfile.TemporaryDirectory() as temp:
                batches, expected = build_scenario(name)
                restart = expected["restart_after_observations"]
                db_path = Path(temp)/"outbox.sqlite3"
                outbox = Outbox(db_path)
                pipeline = Pipeline(BehaviorEngine(), outbox, temp)
                events = []
                for batch in batches[:restart]:
                    events.extend(pipeline.process(batch))
                checkpoint = json.loads(json.dumps(outbox.checkpoint()))
                outbox.close()
                outbox = Outbox(db_path)
                pipeline = Pipeline(BehaviorEngine(), outbox, temp)
                self.assertEqual(pipeline.behavior.export_state(), checkpoint)
                for batch in batches[restart:]:
                    events.extend(pipeline.process(batch))
                self.assert_semantics(events, expected)
                # A complete same-epoch replay after a second process restart
                # cannot reopen events or allocate a replacement incident UUID.
                before = deepcopy(pipeline.behavior.export_state())
                outbox.close()
                outbox = Outbox(db_path)
                pipeline = Pipeline(BehaviorEngine(), outbox, temp)
                for batch in batches:
                    self.assertEqual(pipeline.process(batch), [])
                self.assertEqual(pipeline.behavior.export_state(), before)
                receiver = IdempotentReceiver(lose_first_ack=True)
                with patch("ml.pipeline.delivery.time.time", return_value=100):
                    outbox.dispatch(receiver)
                with patch("ml.pipeline.delivery.time.time", return_value=1000):
                    outbox.dispatch(receiver)
                    outbox.dispatch(receiver)
                self.assertEqual(outbox.counts(), {"pending": 0, "delivered": len(events)})
                self.assertEqual(len(receiver.records), len(events))
                self.assertEqual(len(receiver.notifications), expected["expected_incident_notifications"])
                # Unchanged durable records are the same immutable revisions.
                self.assertEqual({(v["event_id"], v["revision"]) for v in events}, set(receiver.records))
                if events:
                    self.assertEqual(receiver.attempts, len(events)+1)
                outbox.close()

    def test_generator_is_deterministic_and_honestly_labelled(self):
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp)/"a", Path(temp)/"b"
            manifest = generate(a)
            generate(b)
            for file in ("observations.jsonl", "expected.json"):
                self.assertEqual((a/file).read_bytes(), (b/file).read_bytes())
            self.assertFalse(manifest["neural_inference_performed"])
            self.assertFalse(manifest["hardware_execution_verified"])
            self.assertFalse(manifest["target_video_accuracy_measured"])
            batches = list(read_jsonl(a/"observations.jsonl"))
            self.assertEqual(len(batches), manifest["observation_count"])
            self.assertEqual({v["backend"] for v in batches}, {"synthetic-test"})
            for batch in batches:
                validate_observation(batch)
            with self.assertRaises(FileExistsError):
                generate(a)
            with self.assertRaises(ValueError):
                generate(Path(temp)/"duplicate", ["compliance", "compliance"])

    def test_cli_selects_requested_scenario(self):
        with tempfile.TemporaryDirectory() as temp:
            run = subprocess.run([sys.executable, "-m", "ml.behavior.scenarios", "--output-dir", temp,
                                  "--scenario", "fall_immobility"], capture_output=True, text=True, check=True)
            self.assertEqual(json.loads(run.stdout)["backend"], "synthetic-test")
            manifest = json.loads((Path(temp)/"expected.json").read_text())
            self.assertEqual([s["name"] for s in manifest["scenarios"]], ["fall_immobility"])


if __name__ == "__main__":
    unittest.main()
