"""Audit URFall native frame labels against author preview media on CPU.

The preview is a DEPTH|RGB montage. Only the right RGB panel is a model input.
Frame annotation holes remain unknown. No clip label is turned into event onset.
Author zero-state intervals are retained as transition annotation, not medical GT.
"""
import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
from pathlib import Path
import subprocess

from .acquire import sha256

LABELS = {-1: 'not_lying', 0: 'falling_transition', 1: 'lying_on_ground'}
GROUP = 'urfall-all-unknown-subjects-shared-cam0'


def native_rows(features, synchronization, sequence, frame_count):
    """Join independent source annotations by 1-based frame identity, never FPS."""
    times = {}
    for row in csv.reader(synchronization):
        if not row:
            continue
        frame, time_ms = int(row[0]), float(row[1])
        if frame in times or not 1 <= frame <= frame_count or not math.isfinite(time_ms) or time_ms < 0:
            raise ValueError('invalid or duplicate source synchronization row')
        times[frame] = time_ms
    if set(times) != set(range(1, frame_count+1)) or any(times[i] >= times[i+1] for i in range(1, frame_count)):
        raise ValueError('synchronization must cover strictly ordered media frames')
    labels = {}
    for row in csv.reader(features):
        if not row or row[0] != sequence:
            continue
        frame, label = int(row[1]), int(row[2])
        if frame in labels or not 1 <= frame <= frame_count or label not in LABELS:
            raise ValueError('invalid or duplicate posture annotation')
        labels[frame] = label
    return [{'source_frame_id': i, 'source_time_ms': times[i], 'label': labels.get(i),
             'state': LABELS.get(labels.get(i), 'unknown')} for i in range(1, frame_count+1)]


def intervals(rows, video_duration_ms):
    """Group consecutive observed labels including explicit unknown intervals."""
    result = []
    for i, row in enumerate(rows):
        end = rows[i+1]['video_pts_ms'] if i+1 < len(rows) else video_duration_ms
        if end <= row['video_pts_ms']:
            raise ValueError('media interval has no duration')
        if result and result[-1]['state'] == row['state']:
            result[-1].update(end_ms=end, last_source_frame=row['source_frame_id'])
        else:
            result.append({'state': row['state'], 'start_ms': row['video_pts_ms'], 'end_ms': end,
                           'first_source_frame': row['source_frame_id'], 'last_source_frame': row['source_frame_id']})
    return result


def probe(path):
    args = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
            'stream=width,height,avg_frame_rate,nb_frames,duration:frame=best_effort_timestamp_time',
            '-of', 'json', str(path)]
    result = json.loads(subprocess.run(args, check=True, capture_output=True, text=True).stdout)
    stream = result['streams'][0]
    pts = [float(v['best_effort_timestamp_time'])*1000 for v in result['frames']]
    if not pts or any(not math.isfinite(v) or v < 0 for v in pts) or any(a >= b for a,b in zip(pts,pts[1:])):
        raise ValueError('invalid/non-increasing decoded frame PTS')
    stream.update(frame_count=len(pts), duration_ms=float(stream['duration'])*1000,
                  fps=float(Fraction(stream['avg_frame_rate'])))
    return stream, pts


def prepare(root):
    root = Path(root)
    selection = json.loads((root/'selection.json').read_text())
    raw = root/'raw/urfall'; output = root/'processed/urfall'; output.mkdir(parents=True, exist_ok=True)
    annotations = []; manifest = []; presentation_times = {}
    for sequence in selection['source_ids']:
        original = raw/(sequence+'-cam0.mp4')
        stream, pts = probe(original)
        if (stream['width'], stream['height']) != (640,240):
            raise ValueError('preview dimensions changed; visually audit panel geometry before continuing')
        derived = output/(sequence+'-cam0-rgb.mp4')
        if not derived.exists():
            subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(original),'-map','0:v:0',
                            '-vf','crop=320:240:320:0','-an','-c:v','libx264','-crf','18',
                            '-preset','fast',str(derived)], check=True, capture_output=True)
        rgb_stream, rgb_pts = probe(derived)
        if len(rgb_pts) != len(pts) or any(abs(a-b) > 0.01 for a,b in zip(pts,rgb_pts)):
            raise ValueError('RGB derivative changed decoded frame count or presentation clock')
        feature = raw/('urfall-cam0-falls.csv' if sequence.startswith('fall-') else 'urfall-cam0-adls.csv')
        with feature.open() as f, (raw/(sequence+'-data.csv')).open() as s:
            rows = native_rows(f, s, sequence, len(pts))
        for row, time_ms in zip(rows,pts):
            row['video_pts_ms'] = time_ms
        diffs = [abs(row['source_time_ms']-row['video_pts_ms']) for row in rows]
        segments = intervals(rows,stream['duration_ms'])
        frame_file = output/(sequence+'-frames.csv')
        with frame_file.open('w') as stream_out:
            writer = csv.DictWriter(stream_out, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
        transition = [v for v in segments if v['state']=='falling_transition']
        lying = [v for v in segments if v['state']=='lying_on_ground']
        item = {'video_id': sequence+'-cam0', 'source_name': 'URFall', 'camera_id': 'urfall-cam0-front-view-role',
                'scene_id': 'urfall-laboratory' if sequence.startswith('fall-') else 'urfall-home', 'actor_group_id': None, 'group_id': GROUP,
                'split': selection['split'], 'media_path': str(derived), 'media_sha256':sha256(derived),
                'original_preview_path':str(original), 'original_preview_sha256':sha256(original),
                'frame_count':len(pts), 'duration_ms':stream['duration_ms'], 'fps':stream['fps'],
                'width':320, 'height':240, 'crop_xywh':[320,0,320,240],
                'transformation':'right RGB panel cropped from native DEPTH|RGB preview; CPU H264 CRF18',
                'rights':'CC-BY-NC-SA-4.0; source says non-commercial academic use; raw not redistributed',
                'source_url':'https://fenix.ur.edu.pl/~mkepski/ds/uf.html',
                'downloaded_source_file_record':'download-ledger.json',
                'annotation_path':str(frame_file), 'annotation_sha256':sha256(frame_file),
                'native_annotation_source':'URFall author depth-frame posture labels joined by source frame id',
                'rgb_alignment':'matching cam0 montage frame counts and presentation order; manually inspect source intervals',
                'source_vs_encoded_pts_max_abs_ms':max(diffs),
                'unknown_frames':sum(v['state']=='unknown' for v in rows),
                'annotator':'URFall source authors; detailed annotation procedure not supplied on page',
                'annotation_independent_of_current_model_predictions':True,
                'local_review_independent_of_model_developer':False,
                'local_full_clip_review':'NOT_YET_REVIEWED',
                'source_segments':segments,
                'fall_transition_count':len(transition),
                'lying_intervals_ge_3000ms':sum(v['end_ms']-v['start_ms'] >= 3000 for v in lying),
                'episode_gt_status':'NATIVE_POSTURE_REFERENCE_ONLY_REQUIRES_EXPLICIT_EVENT_POLICY_AND_REVIEW',
                'negative_semantics':'not_lying is not an exhaustive annotation of every hazardous action'}
        presentation_times[item["video_id"]] = pts
        manifest.append(item)
        annotations.append({'video_id':item['video_id'],'actor_id':'source-single-person-unverified',
                            'intervals':segments,'review_status':'author_labels_imported',
                            'unknown_windows':[v for v in segments if v['state']=='unknown'],
                            'onset_type':'frame-supported source annotation; not clip start',
                            'right_censoring':{'lying_at_clip_end':bool(lying and lying[-1]['end_ms']==item['duration_ms']),
                                                'prolonged_lying_followup_ms':3000},
                            'prediction_access_for_annotation':False})
    episode_candidates = []
    for item in manifest:
        segs = item['source_segments']
        for index, segment in enumerate(segs):
            if segment['state'] not in ('falling_transition','lying_on_ground'):
                continue
            kind = 'suspected_fall' if segment['state']=='falling_transition' else 'prolonged_lying'
            start = segment['start_ms']; end = segment['end_ms']
            if kind=='suspected_fall' and index+1 < len(segs) and segs[index+1]['state']=='lying_on_ground':
                end = segs[index+1]['end_ms']
            first = segment['first_source_frame']
            # UR source transition labels are fixed one-second windows in this
            # subset. Their first frame is not validated visual fall onset.
            lower = None if first==1 else (start if kind=='suspected_fall'
                     else presentation_times[item['video_id']][first-2])
            upper = segment['end_ms'] if kind=='suspected_fall' else start
            long_enough = kind=='suspected_fall' or segment['end_ms']-start >= 3000
            episode_candidates.append({
                'episode_id':item['video_id']+'/'+kind+'/'+str(first),
                'video_id':item['video_id'], 'event_type':kind,
                'actor_id':'source-single-person-unverified',
                'camera_id':item['camera_id'], 'scene_id':item['scene_id'],
                'actor_group_id':None, 'group_id':GROUP, 'split':item['split'],
                'start_ms':start, 'end_ms':end, 'onset_bounds_ms':[lower,upper],
                'left_censored':first==1,
                'right_censored':end==item['duration_ms'],
                'source_state':segment['state'], 'native_source_frame_start':first,
                'native_source_frame_end':segment['last_source_frame'],
                'source_annotation_file':item['annotation_path'],
                'source_annotation_sha256':item['annotation_sha256'],
                'label_provenance':'source-author posture labels; transition is a coarse window, not verified onset/model prediction',
                'minimum_followup_ms':3000 if kind=='prolonged_lying' else None,
                'policy_duration_eligible':long_enough,
                'episode_scoring_status':'RGB_VISIBILITY_AND_TRANSITION_SEMANTICS_REVIEW_REQUIRED' if long_enough
                    else 'INSUFFICIENT_OBSERVED_DURATION_FOR_3S_RULE',
                'exact_onset_latency_claim':False})
    result = {'schema_version':'temporal-reference-v1','created_at':datetime.now(timezone.utc).isoformat(),
              'split_status':'validation/development; no final test touched',
              'grouping':{'id':GROUP,'basis':'same source/cam0 front-view role; physical camera and subject identities unavailable; all clips kept together'},
              'production_capabilities':{'suspected_fall':'IMPLEMENTED_UNMEASURED_ON_THIS_REFERENCE',
                  'prolonged_lying':'IMPLEMENTED_UNMEASURED_ON_THIS_REFERENCE',
                  'running':'NOT_IMPLEMENTED','zone_intrusion':'NOT_IMPLEMENTED'},
              'metrics':{'precision':None,'recall':None,'f1':None,'status':'NOT_EVALUATED'},
              'media':manifest,'annotations':annotations,'episode_candidates':episode_candidates}
    (root/'urfall-reference.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result


def contact_sheets(root, stride=10):
    """Produce labelled source-PTS sheets for blinded visual audit (no outputs)."""
    import cv2
    from PIL import Image, ImageDraw
    root=Path(root); reference=json.loads((root/'urfall-reference.json').read_text())
    directory=root/'audit'; directory.mkdir(exist_ok=True)
    for media in reference['media']:
        cap=cv2.VideoCapture(media['media_path']); frames=[]; index=0
        frame_rows=list(csv.DictReader(Path(media['annotation_path']).open()))
        while True:
            ok, bgr=cap.read()
            if not ok:break
            if index%stride==0 or index==media['frame_count']-1:
                im=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)); draw=ImageDraw.Draw(im)
                draw.rectangle([0,0,319,20],fill='white')
                draw.text((3,3),f"{media['video_id']} f{index+1} PTS {float(frame_rows[index]['video_pts_ms'])/1000:.2f}s",fill='black')
                frames.append(im)
            index+=1
        cap.release()
        sheet=Image.new('RGB',(1280,240*((len(frames)+3)//4)),'white')
        for i,im in enumerate(frames):sheet.paste(im,((i%4)*320,(i//4)*240))
        sheet.save(directory/(media['video_id']+'-contact.jpg'))


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',required=True);p.add_argument('--contacts',action='store_true');args=p.parse_args(argv)
    result=prepare(args.root)
    if args.contacts:contact_sheets(args.root)
    print(json.dumps({'videos':len(result['media']), 'frames':sum(v['frame_count'] for v in result['media']),
                      'author_transition_intervals':sum(v['fall_transition_count'] for v in result['media']),
                      'unknown_frames':sum(v['unknown_frames'] for v in result['media']),
                      'metrics':'NOT_EVALUATED','running_zone':'NOT_IMPLEMENTED'}))


if __name__=='__main__':main()
