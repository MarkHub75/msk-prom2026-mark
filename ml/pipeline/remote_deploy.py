"""Upload reviewed model bytes via an explicit Jupyter agent, then use same TPU client.

No filesystem access is inferred from the RabbitMQ tunnel. The remote agent must
be started by the user inside the authorized notebook. Upload and inference use
ml.linq.amqp; no alternate inference transport/codec exists here.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
from uuid import UUID
import numpy as np
from ml.linq.amqp import AmqpError,AmqpRunner,official_binding,_environment_parameters,main as amqp_main
from ml.pipeline.capture_review import review_capture
from ml.pipeline.prepare_model_probe import prepare
from ml.detection.compare_capture import compare_captures,load_numeric_npz
from ml.detection.codec import decode,LetterboxTransform
from ml.pipeline.capture_recovery import complete_capture,save_json
from ml.pipeline.runtime_lock import deployment_lock

ARTIFACTS=Path('/workspace/artifacts')
PROFILES={
 'helmet':('helmet-v1','helmet-v1.tpu','408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa'),
 'pose-split':('pose-split-v1','pose-split-v1.tpu','c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b'),
}


def resume_operation(directory,purpose,output_names,timeout):
    """Receive/cache only: an existing request is never republished here."""
    from ml.linq.journal import RequestJournal
    directory=Path(directory)
    pointer=json.loads((directory/'request-pointer.json').read_text())
    request_id=pointer['journal_request_id']
    if str(UUID(request_id))!=request_id:raise ValueError('invalid persisted request UUID')
    base=ARTIFACTS/'linq-rpc/requests'
    expected=(base/request_id).resolve()
    if (pointer.get('schema_version')!='1.0' or pointer.get('purpose')!=purpose or
        Path(pointer['journal_path']).resolve()!=expected):
        raise ValueError('invalid durable request association')
    store=RequestJournal(base)
    # A direct client can still be in preflight while its state is NOT_SUBMITTED.
    # Its transport lock must be released before that state licenses a new UUID.
    with store.lock(request_id):
        record=store.load(request_id)
        if (record.get('purpose')!=purpose or record.get('capture_dir')!=str(directory.resolve()) or
            set(record['output_names'])!=set(output_names)):
            raise ValueError('durable request context mismatch')
        if purpose=='inference':
            capture=json.loads((directory/'capture.json').read_text())
            if record.get('capture_id')!=capture.get('capture_id') or record.get('inputs')!=capture.get('inputs'):
                raise ValueError('capture differs from original durable request')
        if record['state']=='NOT_SUBMITTED':return None,None
    binding=None
    if record['state'] not in ('COMPLETED','SERVICE_FAILED'):
        binding=official_binding(_environment_parameters(),request_exchange='tpu.direct',
            request_routing_key='input',reply_exchange='' if purpose=='model_upload' else 'tpu.direct',
            output_names=output_names,format_source_manifest=ARTIFACTS/'linq-rpc/format-source.json')
    runner=AmqpRunner(binding,journal_dir=base,purpose=purpose,timeout=timeout)
    try:
        outputs=runner.reconcile(request_id)
    finally:
        if runner.last_response is not None:
            save_json(directory/('upload-response.json' if purpose=='model_upload' else 'response.json'),runner.last_response)
    return outputs,runner.last_response


def _archive_unsent_pointer(directory):
    path=directory/'request-pointer.json'
    request_id=json.loads(path.read_text())['journal_request_id']
    path.rename(directory/('request-pointer.'+request_id+'.not-submitted.json'))
    previous=directory/'upload-response.json'
    if previous.exists():previous.rename(directory/('upload-response.'+request_id+'.not-submitted.json'))


def upload_program(name, bridge, timeout=60):
    model_id,filename,sha=PROFILES[name]
    program=ARTIFACTS/'linq-sdk'/(name+'-compile')/'model.tpu'
    body=program.read_bytes()
    if hashlib.sha256(body).hexdigest()!=sha:raise ValueError('local reviewed program changed')
    state=ARTIFACTS/'linq-rpc'/name;state.mkdir(parents=True,exist_ok=True)
    receipt_path=state/'staging-receipt.json'
    if receipt_path.exists():
        receipt=json.loads(receipt_path.read_text())
        if (receipt.get('status')!='STAGED' or receipt.get('model_id')!=model_id or
            receipt.get('program_sha256')!=sha or receipt.get('program_name')!=filename or
            receipt.get('bytes')!=len(body)):
            raise ValueError('existing staging receipt differs from reviewed program')
        return receipt
    result=None;response=None
    if (state/'request-pointer.json').exists():
        result,response=resume_operation(state,'model_upload',['sha256','byte_count'],timeout)
        if result is None:_archive_unsent_pointer(state)
    elif (state/'upload-response.json').exists():
        previous=json.loads((state/'upload-response.json').read_text())
        if previous.get('publish_attempted') is not False:
            raise ValueError('legacy upload may have been submitted; explicit reconciliation required')
    if result is None:
        result,response=_submit_upload(name,bridge,body,state,timeout)
    if result['sha256'].shape!=(32,) or result['sha256'].dtype!=np.uint8 or result['sha256'].tobytes().hex()!=sha:
        raise ValueError('remote staged hash mismatch')
    if result['byte_count'].shape!=(1,) or result['byte_count'].dtype!=np.int64 or int(result['byte_count'][0])!=len(body):
        raise ValueError('remote staged byte count mismatch')
    receipt={'status':'STAGED','model_id':model_id,'program_name':filename,'program_sha256':sha,
             'bytes':len(body),'upload_request_id':response['request_id'],
             'remote_completion':response['remote_completion'],
             'scope':'remote Jupyter file staging; not neural inference'}
    save_json(receipt_path,receipt)
    return receipt


def _submit_upload(name,bridge,body,state,timeout):
    queue=bridge.get('upload_queue')
    if not isinstance(queue,str) or not re.fullmatch(r'notebook_upload_[a-f0-9]{32}',queue):raise ValueError('invalid dedicated upload queue')
    binding=official_binding(_environment_parameters(),request_exchange='',request_routing_key=queue,
        reply_exchange='',output_names=['sha256','byte_count'],
        format_source_manifest=ARTIFACTS/'linq-rpc/format-source.json',
        reply_queue_factory=lambda request_id:'notebook_'+request_id[:8])
    def check_ready(channel,reply_queue,request_id):
        try:
            declared=channel.queue_declare(queue=queue,passive=True)
            if declared.method.consumer_count<1:raise ValueError('no active upload consumer')
        except Exception as error:
            raise AmqpError('jupyter_upload_agent_not_ready','upload_preflight',exception_type=type(error).__name__) from None
    binding.reply_policy='custom_setup';binding.reply_setup=check_ready
    runner=AmqpRunner(binding,name,timeout=timeout,journal_dir=ARTIFACTS/'linq-rpc/requests',
                      purpose='model_upload',capture_dir=state)
    try:
        result=runner({'program_bytes':np.frombuffer(body,dtype=np.uint8)})
    finally:
        attempt=getattr(runner,'last_response',None)
        if attempt is not None:
            save_json(state/'upload-response.json',attempt)
    return result,runner.last_response


def verify_model(name,output):
    model_id,filename,sha=PROFILES[name]
    probe=ARTIFACTS/'linq-rpc'/name
    review=review_capture(output,sha)
    metadata=json.loads((probe/'comparison-metadata.json').read_text())
    manifest=json.loads((ARTIFACTS/'detection'/name/'manifest.json').read_text())
    report=json.loads((ARTIFACTS/'linq-sdk'/(name+'-compile')/'compile-report.json').read_text())
    actual=load_numeric_npz(output/'outputs.npz');reference=load_numeric_npz(probe/'golden-outputs.npz')
    specs={s['name']:s for s in report['outputs']}
    if set(actual)!=set(specs):raise ValueError('actual output names mismatch')
    for key,value in actual.items():
        spec=specs[key]
        if list(value.shape)!=spec['shape'] or value.dtype!=np.dtype(spec['dtype']) or not np.isfinite(value).all():
            raise ValueError('actual output ABI/values mismatch')
    with np.load(output/'inputs.npz',allow_pickle=False) as capture,np.load(probe/'inputs.npz',allow_pickle=False) as expected:
        if set(capture.files)!=set(expected.files) or any(not np.array_equal(capture[k],expected[k]) for k in expected.files):raise ValueError('actual input differs from golden source')
    comparison=compare_captures(reference,actual,manifest=manifest,metadata=metadata)
    decoded=decode(actual,manifest,LetterboxTransform(**metadata['original_transform']))
    width=metadata['original_transform']['original_width'];height=metadata['original_transform']['original_height']
    for det in decoded:
        x1,y1,x2,y2=det['bbox_xyxy']
        if det['class_name'] not in manifest['classes'] or not 0<=det['score']<=1 or not(0<=x1<=x2<=width and 0<=y1<=y2<=height):raise ValueError('invalid decoded class/score/coordinates')
        points=det.get('keypoints')
        if points is not None and (len(points)!=17 or any(len(p)!=3 or not(0<=p[0]<=width and 0<=p[1]<=height and 0<=p[2]<=1) for p in points)):
            raise ValueError('invalid decoded keypoint coordinates/confidence')
    pairs=comparison.get('decoded',{}).get('pairs',[])
    golden_smoke=bool(comparison['status']=='COMPARED' and pairs and not comparison['decoded']['unmatched_reference_indices'] and all(p['box_iou']>=.5 for p in pairs))
    if name=='pose-split':
        golden_smoke=golden_smoke and all(p.get('keypoints',{}).get('actual_visible_at_0_5',0)>0 for p in pairs)
    response=json.loads((output/'response.json').read_text())
    request_id=response.get('request_id')
    if (not isinstance(request_id,str) or str(UUID(request_id))!=request_id or
        response.get('status_code')!=0 or request_id!=response.get('response_id') or
        response.get('remote_completion')!='response_received'):
        raise ValueError('successful correlated TPU response required')
    result={'status':'PASS' if golden_smoke else 'NEEDS_REVIEW','model_id':model_id,
            'status_code':response['status_code'],'request_id':response['request_id'],
            'capture_integrity':review['status'],'output_abi':'PASS','decoded_count':len(decoded),
            'classes':sorted({d['class_name'] for d in decoded}),
            'reference_detection_count':comparison.get('decoded',{}).get('reference_count'),
            'unmatched_actual_count':len(comparison.get('decoded',{}).get('unmatched_actual_indices',[])),
            'unmatched_reference_count':len(comparison.get('decoded',{}).get('unmatched_reference_indices',[])),
            **response_latency(response),
            'same_input_smoke_policy':'all reference detections matched class-wise, box IoU>=0.5; pose retains visible keypoints',
            'target_video_quality':'NOT_EVALUATED'}
    (output/'integrity-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (output/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
    (output/'detections.json').write_text(json.dumps(decoded,indent=2)+'\n')
    (output/'model-check.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def response_latency(response):
    recovered=bool(response.get('reconcile_only') or response.get('cached_response'))
    duration=response.get('timings',{}).get('total_ms')
    return {'roundtrip_ms':None if recovered else duration,
            'recovery_ms':duration if recovered else None,
            'latency_kind':'recovery_only' if recovered else 'full_amqp_call'}


def run(name,bridge_path,timeout=60):
    with deployment_lock(ARTIFACTS/'linq-rpc/deployment.lock'):
        return _run(name,bridge_path,timeout)


def _run(name,bridge_path,timeout):
    if name not in PROFILES:raise ValueError('unknown reviewed model')
    stock=json.loads((ARTIFACTS/'linq-rpc/resnet50-001/resnet-check.json').read_text())
    if stock['status']!='PASS' or stock['status_code']!=0:raise ValueError('successful stock gate required')
    if name=='pose-split':
        helmet=json.loads((ARTIFACTS/'linq-rpc/helmet-001/model-check.json').read_text())
        if helmet['status']!='PASS':raise ValueError('reviewed Helmet gate required before Split-Pose')
    output=ARTIFACTS/'linq-rpc'/(name+'-001')
    report=json.loads((ARTIFACTS/'linq-sdk'/(name+'-compile')/'compile-report.json').read_text())
    if output.exists():
        capture=json.loads((output/'capture.json').read_text())
        if capture.get('model_id')!=PROFILES[name][0] or capture.get('program',{}).get('sha256')!=PROFILES[name][2]:
            raise ValueError('existing capture identity differs from reviewed model')
        if capture.get('status')=='completed' and (output/'response.json').is_file():
            result=verify_model(name,output);print(json.dumps({'phase':'cached_result',**result}))
            return 0 if result['status']=='PASS' else 2
        values,response=resume_operation(output,'inference',[s['name'] for s in report['outputs']],timeout)
        if values is not None:
            complete_capture(output,values,response)
            result=verify_model(name,output);print(json.dumps({'phase':'reconciled_result',**result}))
            return 0 if result['status']=='PASS' else 2
        # Durable NOT_SUBMITTED is the sole automatic fresh-attempt condition.
        request_id=json.loads((output/'request-pointer.json').read_text())['journal_request_id']
        attempts=ARTIFACTS/'linq-rpc/attempts';attempts.mkdir(parents=True,exist_ok=True)
        output.rename(attempts/(name+'-'+request_id+'-not-submitted'))
    login=os.environ.get('LINQ_LOGIN')
    if not isinstance(login,str) or not re.fullmatch(r'[A-Za-z0-9_@.+-]{1,128}',login):raise ValueError('explicit LinQ account required')
    if os.environ.get('LINQ_AMQP_HOST')!='127.0.0.1' or os.environ.get('LINQ_AMQP_PORT')!='15672':raise ValueError('confirmed tunnel configuration required')
    bridge=json.loads(Path(bridge_path).read_text())
    print(json.dumps({'phase':'prepare','result':prepare(name,root=ARTIFACTS)}))
    receipt=upload_program(name,bridge,timeout)
    print(json.dumps({'phase':'upload','status':receipt['status'],'program_sha256':receipt['program_sha256']}))
    model_id,filename,_=PROFILES[name]
    args=['--format-source-manifest',str(ARTIFACTS/'linq-rpc/format-source.json'),
          '--exchange','tpu.direct','--routing-key','input','--reply-exchange','tpu.direct',
          '--target-uri',f'file:///auto/cache/{login}/{filename}?raw=False',
          '--program-file',str(ARTIFACTS/'linq-sdk'/(name+'-compile')/'model.tpu'),
          '--input-npz',str(ARTIFACTS/'linq-rpc'/name/'inputs.npz'),
          '--output-dir',str(output),'--model-id',model_id,'--timeout',str(timeout),
          '--journal-dir',str(ARTIFACTS/'linq-rpc/requests'),
          '--host','127.0.0.1','--port','15672','--notebook-reply-queue','--save-service-error',
          '--attest-linq-placement','--attest-program-match']
    for spec in report['outputs']:args.extend(['--output-name',spec['name']])
    code=amqp_main(args)
    if code:return code
    result=verify_model(name,output);print(json.dumps(result))
    return 0 if result['status']=='PASS' else 2


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('model',choices=list(PROFILES))
    parser.add_argument('--bridge',default='/workspace/artifacts/linq-rpc/upload-bridge.json')
    parser.add_argument('--timeout',type=float,default=60)
    args=parser.parse_args()
    try:return run(args.model,args.bridge,args.timeout)
    except AmqpError as error:
        print(json.dumps({'status':'NOT_COMPLETED','error':error.details}));return 1
    except Exception as error:
        print(json.dumps({'status':'NOT_COMPLETED','error_type':type(error).__name__}));return 1

if __name__=='__main__':raise SystemExit(main())
