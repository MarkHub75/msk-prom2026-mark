"""Freeze completed local evidence as a consumer-scoped READY snapshot.

No download, label invention, pixel audit or Data Orchestrator branch mutation.
Existing producer checksums are verified by handoff.verify_manifest. Input GT
scope and allowed uses remain explicit; iSafety clip actions are not event GT.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from .handoff import SCHEMA, sha256, publish_snapshot

ART = Path('/workspace/artifacts')
RESEARCH = Path('/workspace/datasets/research')
PRODUCER = Path('/workspace/agents/data-audit')


def asset(path, role='annotation', *, expected=None, group=None):
    path=Path(path)
    entry={'path':str(path.resolve()),'sha256':expected or sha256(path),
           'bytes':path.stat().st_size,'role':role}
    if group:entry['group_id']=group
    return entry


def build(*, ml_baseline_only=False):
    git=['git','-C',str(PRODUCER)]
    docs=PRODUCER/'docs/data-audit'
    if not ml_baseline_only:
        if subprocess.check_output(git+['status','--porcelain'],text=True).strip():
            raise ValueError('producer worktree is changing; wait for a committed handoff')
        commit=subprocess.check_output(git+['rev-parse','HEAD'],text=True).strip()
        summary=json.loads((docs/'evidence_summary.json').read_text())
        if summary['download_budget']['successful_files']!=58:
            raise ValueError('producer audited version changed; review before consuming')
        producer_assets=[asset(docs/x,'provenance') for x in
                         ('evidence_summary.json','QUALITY_REPORT.md','SCENARIO_COVERAGE.md','DATASETS.csv')]
        producer_assets+=[asset(RESEARCH/'_audit/downloads.jsonl','provenance')]
    datasets=[]
    def dataset(id,split,caps,scope,rights,assets,**extra):
        datasets.append(dict(dataset_id=id,split=split,capabilities=caps,
            annotation_scope=scope,rights_scope=rights,assets=assets,**extra))
    # Previously frozen ML development set: source/training overlap is disclosed.
    gtpath=ART/'quality/helmet/development-quality-v3.json'
    gt=json.loads(gtpath.read_text());fixed='39e13db80621e4901f0eb0aa15d27b2f9b1cc8e2da951cb107b279532820de6a'
    canonical=dict(gt);claimed=canonical.pop('dataset_digest')
    if claimed!=fixed or hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(',',':')).encode()).hexdigest()!=fixed:
        raise ValueError('frozen semantic dataset digest changed')
    # Canonical content digest and serialized JSON byte hash are DISTINCT.
    assets=[asset(gtpath,expected='346f74cab99ddc2cc9c0f18b3efd95027a0b1ea782738469f502bc771dfd27e0')]+[asset(v['path'],'media',expected=v['file_sha256'],group=v['group_id']) for v in gt['images']]
    dataset('helmet-quality-v3-52','validation',['annotation','detection_quality','inference'],
        'head object boxes;44complete/class,partial/unknown separate; AI reviewed, not wearer/event GT',
        'internal research diagnostics only; source AGPL notice/upstream photo rights unresolved',assets,
        manifest_path=str(gtpath),dataset_semantic_digest=fixed,independent_test=False,pretraining_overlap='CONFIRMED_SHARED_PHOTOGRAPHS')
    calib=ART/'quality/calibration/mendeley-v1/calibration-manifest.json'
    c=json.loads(calib.read_text())
    assets=[asset(calib)]+[asset(calib.parent/v['path'],'calibration_tensor',expected=v['sha256'],group=v['source_group']) for v in c['samples']]
    dataset('mendeley8-calibration-v1','calibration',['calibration'],
        'no episode/box GT;8 deterministic source midpoints,1conservative group',
        'CC-BY-4.0; internal calibration, no redistribution of identifiable media',assets,
        manifest_path=str(calib),independent_test=False)
    refpath=Path('/workspace/datasets/quality/temporal/urfall-reference.json')
    reference=json.loads(refpath.read_text());ep=Path('/workspace/datasets/quality/temporal/episode-gt.source-reference.json')
    assets=[asset(refpath),asset(ep)]
    for video in reference['media']:
        assets+=[asset(video['media_path'],'media',expected=video['media_sha256'],group=video['group_id']),
                 asset(video['annotation_path'],expected=video['annotation_sha256'])]
    dataset('urfall20-preview-v1','validation',['annotation','source_reference_events','inference'],
        'coarse native posture + sampled blind AI context review; not independent exhaustive RGB event GT',
        'CC-BY-NC-SA-4.0 noncommercial academic research only; no public incident portrayal/redistribution',assets,
        manifest_path=str(refpath),episode_gt=str(ep),independent_test=False)
    if ml_baseline_only:
        return {'schema_version':SCHEMA,'status':'READY','version':'night-ml-baseline-snapshot-20261024-v1',
            'producer':{'previous_ml_checkpoint':'1bdeeafc','role':'previously frozen ML-owned validation/calibration; no new Data Orchestrator assets consumed'},
            'consumer_verification_scope':'Integrity/role revalidation of existing frozen ML data, no new source/label/rights audit',
            'source_data_modified':False,'datasets':datasets}
    # New native RGB source representation from the completed independent audit.
    ledger=[json.loads(x) for x in (RESEARCH/'_audit/downloads.jsonl').read_text().splitlines()]
    ur=[v for v in ledger if v.get('status')=='downloaded' and v['path'].startswith('urfall/')]
    audit=RESEARCH/'urfall/inspection/audit.json'
    assets=producer_assets+[asset(audit)]
    for v in ur:
        assets.append(asset(RESEARCH/v['path'],'media' if v['path'].endswith('.zip') else 'annotation',
            expected=v['actual_sha256'],group='urfall-all-unknown-subjects-shared-cam0'))
    dataset('urfall-native-rgb2-v1','validation',['annotation','source_reference_frames','inference'],
        '310 RGB PNG in2ZIP; source depth-derived posture/sync;6unknown ADL frames; no>=3slyingpositive GT',
        'CC-BY-NC-SA-4.0; noncommercial academic research only; hackathon/commercial clearance UNKNOWN',assets,
        manifest_path=str(audit),independent_test=False,archive_pixels_not_yet_opened_by_consumer=True)
    # Reserve source-ID holdout before any new pixel review or model outputs.
    ia=RESEARCH/'isafety/inspection/audit.json';ir=json.loads(ia.read_text())
    candidates={}
    for reason in ('running','walking'):
        rows=[v for v in ir['rows'] if v['reason']==reason]
        if len(rows)!=2:raise ValueError('run/walk source selection changed')
        rows.sort(key=lambda v:hashlib.sha256(('night-motion-v1:'+v['path']).encode()).hexdigest())
        for row,split in zip(rows,('validation','test')):candidates[row['path']]=split
    test_groups={Path(k).name[:11] for k,s in candidates.items() if s=='test'}
    for split in ('validation','test'):
        assets=producer_assets+[asset(ia),asset(RESEARCH/'_audit/isafety_selection.json')]
        selection=[]
        for row in ir['rows']:
            group='isafety-source:'+Path(row['path']).name[:11]
            assigned='test' if Path(row['path']).name[:11] in test_groups else 'validation'
            if assigned!=split:continue
            item=asset(RESEARCH/'isafety'/row['path'],'media',expected=row['sha256'],group=group)
            item.update(source_id=Path(row['path']).stem,author_actions=row['annotation']['gt_actions'],
                        annotation_unit='clip actions, NOT events',selected_run_walk=row['path'] in candidates)
            assets.append(item)
            if row['path'] in candidates:selection.append({'path':item['path'],'source_id':item['source_id'],'group_id':group,'split':split,'sha256':row['sha256']})
        dataset('isafety-night-'+split+'-v1',split,['annotation','metadata_inspection'],
            'author CLIP actions only; model experiments wait for prediction-blind actor/time/zone annotations',
            'CC-BY-NC-SA-4.0; internal research only; upstream web/news/individual permissions not cleared',assets,
            selected_run_walk=selection,independent_test='source-ID-heldout only; camera/actor independence UNKNOWN',
            model_inference_ready=False)
    return {'schema_version':SCHEMA,'status':'READY','version':'night-consumer-snapshot-20261024-v1',
        'producer':{'data_audit_commit':commit,'data_audit_worktree_modified':False,
                    'previous_ml_checkpoint':'1bdeeafc','producer_published_READY':False},
        'consumer_verification_scope':'ML consumer integrity snapshot of completed producer audit and previously frozen ML data; NOT new source/rights/annotation audit or producer endorsement',
        'source_data_modified':False,'datasets':datasets}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True)
    parser.add_argument('--ml-baseline-only',action='store_true',help='existing frozen ML data only; never reads active producer worktree')
    args=parser.parse_args();value=publish_snapshot(build(ml_baseline_only=args.ml_baseline_only),args.output)
    print(json.dumps({'status':value['status'],'version':value['version'],'manifest_sha256':sha256(args.output),
        'datasets':[{k:d[k] for k in ('dataset_id','split','capabilities')} for d in value['datasets']]}))


if __name__=='__main__':main()
