"""Validate temporal reference coverage/split lineage without running predictions."""
import argparse
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import shutil

from .acquire import sha256
from .urfall import probe

STATES = {'not_lying','falling_transition','lying_on_ground','unknown'}


def audit_reference(reference, verify_media=False):
    if reference.get('schema_version') != 'temporal-reference-v1':
        raise ValueError('unsupported temporal reference schema')
    videos = {}; group_splits = defaultdict(set); hashes = defaultdict(set)
    for media in reference['media']:
        identity = media['video_id']
        if identity in videos:
            raise ValueError('duplicate video identity')
        duration = media['duration_ms']
        if not isinstance(duration,(int,float)) or isinstance(duration,bool) or not math.isfinite(duration) or duration<=0:
            raise ValueError('invalid duration')
        if not media.get('group_id') or not media.get('split'):
            raise ValueError('explicit group/split required')
        group_splits[media['group_id']].add(media['split'])
        hashes[media['media_sha256']].add(media['split'])
        if verify_media and sha256(media['media_path']) != media['media_sha256']:
            raise ValueError('media hash changed')
        videos[identity] = media
    if any(len(v)>1 for v in group_splits.values()) or any(len(v)>1 for v in hashes.values()):
        raise ValueError('protected source group or exact media copy crosses splits')
    states = Counter(); exposure = Counter(); annotated = set()
    for annotation in reference['annotations']:
        vid = annotation['video_id']
        if vid not in videos or vid in annotated:
            raise ValueError('unknown/duplicate annotation identity')
        annotated.add(vid)
        end = 0
        for interval in annotation['intervals']:
            a,b,state = interval['start_ms'],interval['end_ms'],interval['state']
            if state not in STATES or not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in (a,b)):
                raise ValueError('invalid interval')
            if abs(a-end)>0.01 or b<=a or b>videos[vid]['duration_ms']+0.01:
                raise ValueError('coverage must be exhaustive and nonoverlapping; gaps must be explicit unknown')
            end=b; states[state]+=1; exposure[state]+=b-a
        if abs(end-videos[vid]['duration_ms'])>0.01:
            raise ValueError('annotation does not account for full source duration')
    if annotated != set(videos):
        raise ValueError('missing source annotation is not a negative video')
    capabilities=reference.get('production_capabilities',{})
    capability_results={name:{'status':status,
        'precision':None,'recall':None,
        'reason':'no production implementation/external event type' if status=='NOT_IMPLEMENTED' else 'model predictions not evaluated by this source audit'}
        for name,status in capabilities.items()}
    return {'status':'REFERENCE_AUDIT_PASS','videos':len(videos),'groups':len(group_splits),
            'source_hours':sum(m['duration_ms'] for m in videos.values())/3_600_000,
            'source_annotation_intervals':dict(states),'source_annotation_exposure_ms':dict(exposure),
            'unknown_rate_by_duration':exposure['unknown']/sum(exposure.values()) if exposure else None,
            'metrics':{'status':'NOT_EVALUATED','precision':None,'recall':None,'f1':None},
            'capability_results':capability_results,
            'independent_final_test':'NOT_ACQUIRED_OR_EVALUATED',
            'rgb_episode_visibility_review':'REQUIRED; source posture annotations are not silently final event GT'}


def inventory_mendeley(source, root, *, copy_media=False):
    """Preserve source train/test names, but mark all eight already-viewed clips DEV."""
    source, root = Path(source), Path(root)
    samples = json.loads((source/'SAMPLE_OBSERVATIONS.json').read_text(encoding='utf-8-sig'))
    records=[]
    for sample in samples:
        path = source/sample['filename']
        if sha256(path)!=sample['sha256'] or path.stat().st_size!=sample['bytes']:
            raise ValueError('historical sample no longer matches source artifact hash/size')
        destination=root/'raw/mendeley'/sample['filename']
        if copy_media:
            destination.parent.mkdir(parents=True,exist_ok=True)
            if destination.exists() and sha256(destination)!=sample['sha256']:
                raise ValueError('existing raw copy differs')
            if not destination.exists():shutil.copy2(path,destination)
        stream,_=probe(path)
        records.append({'video_id':path.stem,'media_path':str(destination if copy_media else path),
            'sha256':sample['sha256'],'bytes':sample['bytes'],'source_file_id':sample['id'],
            'source_name':'Mendeley Safe and Unsafe Behaviours','source_version':'xjmtb22pff/1',
            'source_url':'https://data.mendeley.com/datasets/xjmtb22pff/1',
            'license':'CC-BY-4.0; author claims company/employee permissions; not independently audited',
            'source_clip_class':'unsafe_walkway' if path.stem.startswith('0_') else 'safe_walkway',
            'source_partition':'test' if '_te' in path.stem else 'train',
            'split':'development','group_id':'mendeley-xjmtb22pff-entire-factory',
            'camera_id':None,'scene_id':None,'actor_group_id':None,
            'group_basis':'two source cameras, unknown source actor/session mapping; same factory conserved together',
            'duration_ms':stream['duration_ms'],'fps':stream['fps'],
            'width':stream['width'],'height':stream['height'],
            'episode_gt':'UNAVAILABLE','reviewed_negative_exposure_ms':None,
            'unknown_windows':[{'start_ms':0,'end_ms':stream['duration_ms'],
                                'scope':'episode/actor/zone policy truth not annotated'}],
            'zone_geometry':None,'running_labels':'UNAVAILABLE',
            'do_not_infer':'video class does not label each actor, event onset, zone polygon, running or all negatives'})
    result={'schema_version':'temporal-intake-v1','source':'mendeley-xjmtb22pff/1',
            'media':records,'clip_count':len(records),'bytes':sum(v['bytes'] for v in records),
            'all_already_viewed_development':True,'final_test_eligible':False,
            'raw_author_train_test_camera_leakage':'historical inferred views span both source partitions; not independent camera holdout',
            'metrics':{'status':'N/A_NO_EPISODE_GT','precision':None,'recall':None}}
    root.mkdir(parents=True,exist_ok=True)
    (root/'mendeley-intake.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('reference');p.add_argument('--input',required=True);p.add_argument('--output');p.add_argument('--verify-media',action='store_true')
    p=sub.add_parser('mendeley');p.add_argument('--source',required=True);p.add_argument('--root',required=True);p.add_argument('--copy-media',action='store_true')
    args=parser.parse_args(argv)
    if args.command=='reference':
        result=audit_reference(json.loads(Path(args.input).read_text()),args.verify_media)
        if args.output:Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    else:result=inventory_mendeley(args.source,args.root,copy_media=args.copy_media)
    print(json.dumps(result if args.command=='reference' else {'clips':result['clip_count'],'bytes':result['bytes'],'episode_metrics':'N/A_NO_EPISODE_GT'},allow_nan=False))


if __name__=='__main__':main()
