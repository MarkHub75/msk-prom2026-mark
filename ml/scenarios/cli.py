"""Opt-in eight-scenario replay on the existing tracker/outbox/evidence pipeline."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from ml.behavior import BehaviorEngine
from ml.contracts import validate_observation
from ml.pipeline.delivery import Outbox
from ml.pipeline.runner import Pipeline
from ml.pipeline.capture_recovery import save_json
from .engine import ScenarioSuite,load_config


class VideoEvidenceFrames:
    """Read original frames only when source bytes, frame index and PTS match."""
    def __init__(self,path):
        import cv2
        from ml.pipeline.file_video import file_hash
        self.cv2=cv2;self.sha256=file_hash(path);self.cap=cv2.VideoCapture(str(path))
        if not self.cap.isOpened():raise ValueError('evidence source unavailable')

    def __call__(self,batch):
        if batch.get('source_sha256')!=self.sha256:raise ValueError('original video source hash required for evidence')
        cv2=self.cv2;self.cap.set(cv2.CAP_PROP_POS_FRAMES,batch['frame_id']);ok,bgr=self.cap.read()
        if not ok or abs(self.cap.get(cv2.CAP_PROP_POS_MSEC)-batch['media_time_ms'])>2:
            raise ValueError('evidence frame/PTS differs from analyzed frame')
        if [bgr.shape[1],bgr.shape[0]]!=list(batch['image_size']):raise ValueError('evidence original geometry differs')
        return cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)

    def close(self):self.cap.release()


def replay(source,state_dir,config,*,frame_provider=None):
    root=Path(state_dir);root.mkdir(parents=True,exist_ok=True)
    outbox=Outbox(root/'events.sqlite')
    try:
        suite=ScenarioSuite(config);pipeline=Pipeline(BehaviorEngine(config.get('behavior')),outbox,root,scenario_suite=suite)
        for raw in source:
            batch=validate_observation(raw.get('batch',raw))
            frame=frame_provider(batch) if frame_provider and batch['status']=='ok' else None
            pipeline.process(batch,frame)
        outbox.export_jsonl(root)
        candidates=[json.loads(x[0]) for x in outbox.db.execute('SELECT body FROM scenario_candidates ORDER BY rowid')]
        findings=[f for row in outbox.db.execute('SELECT body FROM scenario_diagnostics') for f in json.loads(row[0])['findings']]
        result={'mode':'SAVED_OBSERVATION_RULE_REPLAY_NO_NEW_INFERENCE','prototype':True,
                'new_neural_calls':0,'new_remote_calls':0,'independent_accuracy_measured':False,
                'candidate_revisions':len(candidates),'candidate_episodes':len({e['candidate_id'] for e in candidates}),
                'scenario_candidate_counts':dict(Counter(e['scenario_id'] for e in candidates if e['revision']==1)),
                'verdict_counts':dict(Counter(f['scenario_id']+':'+f['verdict'] for f in findings)),
                'external_event_v1_changed':False}
        save_json(root/'scenario-summary.json',result)
        return result
    finally:outbox.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir',required=True)
    parser.add_argument('--config',help='Explicit site suite; default configs have no invented site policies')
    parser.add_argument('--input',help='Existing direct or wrapped ObservationBatch JSONL, not video inference')
    parser.add_argument('--synthetic-scenario',choices=[f'{i:02d}' for i in range(1,9)])
    parser.add_argument('--variant',choices=['positive','negative','unknown'],default='positive')
    parser.add_argument('--synthetic-evidence',action='store_true',help='Labelled black test image only; never real-video evidence')
    parser.add_argument('--source-video',help='Optional original video for hash/index/PTS-bound evidence, never triggers inference')
    args=parser.parse_args()
    if bool(args.input)==bool(args.synthetic_scenario):parser.error('choose existing observations OR explicit synthetic scenario')
    provider=None
    if args.synthetic_scenario:
        if args.source_video:parser.error('real video cannot back a synthetic observation fixture')
        from .fixtures import build_case
        config,source=build_case(args.synthetic_scenario,args.variant)
        if args.synthetic_evidence:
            def provider(batch):
                import numpy as np
                from PIL import Image,ImageDraw
                w,h=batch['image_size'];im=Image.new('RGB',(w,h));ImageDraw.Draw(im).text((10,10),'SYNTHETIC RULE TEST - NO VIDEO OR MODEL',fill='white')
                return np.asarray(im)
    else:
        if args.synthetic_evidence:parser.error('synthetic evidence cannot be attached to real saved observations')
        config=load_config(args.config)
        source=(json.loads(line) for line in Path(args.input).read_text().splitlines() if line.strip())
    real_provider=None
    try:
        if args.source_video:real_provider=VideoEvidenceFrames(args.source_video);provider=real_provider
        print(json.dumps(replay(source,args.state_dir,config,frame_provider=provider),allow_nan=False))
    finally:
        if real_provider is not None:real_provider.close()


if __name__=='__main__':
    try:main()
    except Exception as error:
        print(json.dumps({'status':'FAILED','error_type':type(error).__name__}),file=sys.stderr)
        raise SystemExit(1)
