"""Finite-corpus episode scoring, not an industrial reliability estimate."""
import json
import argparse
from pathlib import Path


def evaluate(truth, predictions, deadline_ms=5000):
    if deadline_ms < 0:
        raise ValueError('negative deadline')
    # One delivered logical incident counts once, regardless of revisions.
    unique = {}
    for event in predictions:
        key = event['event_id']
        if key not in unique or event['revision'] < unique[key]['revision']:
            unique[key] = event
    predictions = sorted(unique.values(), key=lambda x: (x['confirmed_media_ms'], x['event_id']))
    matched = set()
    delays = []
    false = 0
    for event in predictions:
        candidates = []
        for i, gt in enumerate(truth):
            if i in matched:
                continue
            if any(event[key] != gt[key] for key in ('camera_id','stream_epoch','type')):
                continue
            confirmed = event['confirmed_media_ms']
            if gt['start_media_ms'] <= confirmed <= min(gt['end_media_ms'], gt['start_media_ms']+deadline_ms):
                candidates.append(i)
        if candidates:
            index = min(candidates, key=lambda i: truth[i]['start_media_ms'])
            matched.add(index)
            delays.append(event['confirmed_media_ms']-truth[index]['start_media_ms'])
        else:
            false += 1
    tp = len(matched)
    return {'protocol':'finite-corpus-timely-confirmation-v1', 'tp':tp, 'fp':false, 'fn':len(truth)-tp,
            'precision':tp/len(predictions) if predictions else None,
            'recall':tp/len(truth) if truth else None, 'confirmation_delays_ms':delays,
            'deadline_ms':deadline_ms, 'delivery_latency_measured':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--truth',required=True,help='JSON array of fully observed episode intervals')
    parser.add_argument('--predictions',required=True,help='JSONL event mutations')
    parser.add_argument('--deadline-ms',type=float,default=5000)
    args=parser.parse_args()
    truth=json.loads(Path(args.truth).read_text())
    predictions=[json.loads(s) for s in Path(args.predictions).read_text().splitlines() if s.strip()]
    print(json.dumps(evaluate(truth,predictions,args.deadline_ms),allow_nan=False))

if __name__=='__main__': main()
