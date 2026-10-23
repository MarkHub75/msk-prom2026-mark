"""Bounded real client-disconnect acceptance test; never changes VPN/SSH.

Use an already prepared, PAUSED real-video state. One new sampled frame is
submitted. Its first model connection is closed AFTER broker confirmation, then
the same frame resumes through the existing receive-only request journal.
"""
import argparse
from contextlib import redirect_stdout,redirect_stderr
import json
from pathlib import Path
import sqlite3
import time
from unittest.mock import patch

from ml.linq.journal import RequestJournal
from ml.pipeline.capture_recovery import save_json
from ml.pipeline.local_sink import local_event_sink


def _cursor(root):
    with sqlite3.connect(root/'events.sqlite') as db:
        row=db.execute("SELECT body FROM checkpoints WHERE name='video'").fetchone()
    return json.loads(row[0]) if row else None


def run_probe(state_dir,source):
    import pika
    from ml.pipeline.cli import main as worker_main
    root=Path(state_dir).resolve();source=Path(source).resolve()
    session=json.loads((root/'video-session.json').read_text());before=_cursor(root)
    if session.get('source_kind','real-video')!='real-video' or not before or before['complete']:
        raise ValueError('requires an existing paused REAL video state')
    report_dir=root/'client-disconnect-check';report_dir.mkdir(exist_ok=True)
    if (report_dir/'intent.json').exists():raise ValueError('experiment already started; use its saved pending request, never inject twice')
    prior_ids={path.parent.name for path in (root/'requests').glob('*/request.json')}
    save_json(report_dir/'intent.json',{'scope':'planned client close after broker confirm, NOT actual VPN loss',
        'cursor_before':before,'request_ids_before':sorted(prior_ids),'fault_injected':False})
    started=time.monotonic();published=[];original_connect=pika.BlockingConnection
    def connect(parameters):
        connection=original_connect(parameters);original_channel=connection.channel
        def channel(*args,**kwargs):
            value=original_channel(*args,**kwargs);original_publish=value.basic_publish
            def publish(*args,**kwargs):
                confirmed=original_publish(*args,**kwargs)
                if confirmed is not False and not published:
                    request_id=kwargs['properties'].headers['tpu_pycloud_message_id']
                    published.append(request_id)
                    # Persist the one-shot marker before disconnecting this client.
                    save_json(report_dir/'injected.json',{'request_id':request_id,'broker_confirmation_returned':True})
                    try:connection.close()
                    except Exception:pass
                return confirmed
            value.basic_publish=publish;return value
        connection.channel=channel;return connection
    def invoke(arguments,step):
        with (report_dir/(step+'.stdout.jsonl')).open('x') as output,(report_dir/(step+'.stderr.log')).open('x') as error:
            with redirect_stdout(output),redirect_stderr(error):
                try:worker_main(arguments);return 0
                except SystemExit as exit:return exit.code
    manifests=[root/'pose-split-verified.json',root/'helmet-verified.json']
    rules=report_dir/'rules.json';save_json(rules,session['rules'])
    with local_event_sink(root/'test-receiver',root/'evidence') as receiver:
        arguments=['--state-dir',str(root),'--rules',str(rules),'--sink-kind','local-test',
            '--backend-url',receiver['event_url'],'--evidence-base-url',receiver['evidence_base_url'],
            'video','--source',str(source),'--backend','linq','--camera-id',session['camera_id'],
            '--sample-fps',str(session['sample_fps']),'--start-ms',str(session['start_ms']),
            '--max-frames','1','--linq-runner-factory','ml.linq.video:create_runner']
        if session['end_ms'] is not None:arguments+=['--end-ms',str(session['end_ms'])]
        for manifest in manifests:arguments+=['--manifest',str(manifest)]
        with patch.object(pika,'BlockingConnection',side_effect=connect):
            first_code=invoke(arguments,'disconnect')
        if len(published)!=1:raise ValueError('expected exactly one confirmed publication before injected loss')
        store=RequestJournal(root/'requests');request_id=published[0]
        uncertain=store.load(request_id);cursor_after_loss=_cursor(root)
        save_json(report_dir/'after-disconnect.json',{'worker_exit_code':first_code,
            'request':uncertain,'cursor':cursor_after_loss})
        if first_code!=3 or uncertain['state']!='UNKNOWN' or cursor_after_loss!=before:
            raise ValueError('disconnect did not preserve pending frame and UNKNOWN request')
        second_code=invoke(arguments,'reconcile')
        completed=store.load(request_id);after=_cursor(root)
        new_ids={path.parent.name for path in (root/'requests').glob('*/request.json')}-prior_ids
        with sqlite3.connect(root/'events.sqlite') as db:
            row=db.execute('SELECT body FROM observations WHERE frame_id=?',(after['frame_id'],)).fetchone()
        observation=json.loads(row[0]) if row else None
        provenance=[record['transport_provenance'] for record in observation['execution_records']] if observation else []
        if (second_code!=0 or completed['state']!='COMPLETED' or len(new_ids)!=2 or request_id not in new_ids or
            after['frame_id']<=before['frame_id'] or after['stream_epoch']!=before['stream_epoch'] or
            provenance[0]['request_id']!=request_id or provenance[0].get('reconcile_only') is not True or
            any(p['status_code']!=0 or p['request_id']!=p['response_id'] for p in provenance)):
            raise ValueError('recovery correlation/state/one-request-per-model invariant failed')
        result={'status':'PASS','scope':'REAL video frame, controlled client disconnect AFTER confirmation; VPN not modified or faulted',
            'initial_worker_exit':first_code,'recovery_worker_exit':second_code,'request_id':request_id,
            'state_after_disconnect':'UNKNOWN','state_after_recovery':'COMPLETED','cursor_before':before,'cursor_after':after,
            'new_request_ids':sorted(new_ids),'fresh_publications':2,'recovered_request_republished':False,
            'frame_media_ms':observation['media_time_ms'],'transport_provenance':provenance,
            'wall_ms_including_injected_failure':(time.monotonic()-started)*1000,
            'normal_inference_sample':provenance[1],'team_backend_integration':'NOT_VERIFIED'}
        save_json(report_dir/'report.json',result);return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir',required=True);parser.add_argument('--source',required=True)
    args=parser.parse_args(argv)
    try:
        result=run_probe(args.state_dir,args.source)
        print(json.dumps({key:result[key] for key in ('status','request_id','state_after_disconnect','state_after_recovery','fresh_publications','recovered_request_republished','frame_media_ms','wall_ms_including_injected_failure','transport_provenance')}))
        return 0
    except Exception as error:
        print(json.dumps({'status':'NOT_COMPLETED','error_type':type(error).__name__,
            'next_action':'inspect saved UUID; never inject/re-publish again blindly'}));return 1


if __name__=='__main__':raise SystemExit(main())
