"""Check an explicitly configured backend: v1 POST/ACK, journal and evidence.

This does not infer endpoints or implement Mark's backend. Use a labelled test
event and a fresh state directory; a restart preserves its incident identity.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import time
from urllib.parse import quote,urlsplit
from urllib.request import Request,build_opener,HTTPRedirectHandler
from uuid import uuid4

from ml.contracts import validate_event
from ml.pipeline.capture_recovery import save_json
from ml.pipeline.delivery import HttpEventSink,Outbox
from ml.pipeline.runtime_lock import deployment_lock


def _get(url,*,token=None,timeout=5,max_bytes=1024*1024):
    class NoRedirect(HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs):return None
    headers={'Authorization':'Bearer '+token} if token else {}
    with build_opener(NoRedirect).open(Request(url,headers=headers),timeout=timeout) as response:
        body=response.read(max_bytes+1)
    if len(body)>max_bytes:raise ValueError('backend response exceeds limit')
    return body


def run_probe(**options):
    root=Path(options['state_dir']).resolve()
    if root.is_relative_to(Path(__file__).parents[2]):raise ValueError('probe state must remain outside Git')
    try:return _run_probe(**options)
    except Exception as error:
        # Validation/preflight failures must not leave a previous latest PASS.
        if root.is_dir():
            event_id=None
            try:event_id=json.loads((root/'probe.json').read_text())['event']['event_id']
            except Exception:pass
            try:
                save_json(root/'last-attempt.json',{'status':'NOT_COMPLETED','event_id':event_id,
                    'receiver_kind':options.get('receiver_kind','external'),
                    'checked_at':datetime.now(timezone.utc).isoformat(),'error_type':type(error).__name__})
            except OSError:pass
        raise


def _run_probe(*,event_url,journal_url,event_file,state_dir,evidence_base_url=None,
              evidence_file=None,journal_key=None,receiver_kind='external',timeout=5):
    root=Path(state_dir).resolve()
    if root.is_relative_to(Path(__file__).parents[2]):raise ValueError('probe state must remain outside Git')
    template=validate_event(json.loads(Path(event_file).read_text()))
    if template.get('execution_backend')!='synthetic-test' and template.get('source_kind')!='repeated-image-fixture':
        raise ValueError('probe requires an explicitly labelled test event')
    if journal_url.count('{event_id}')!=1:raise ValueError('supply the actual journal URL with one {event_id} placeholder')
    token=None if receiver_kind=='local-test' else os.environ.get('MOSPROM_BACKEND_TOKEN')
    sink=HttpEventSink(event_url,token,timeout,evidence_base_url)
    sink.prepare_payload(template)
    if template['evidence']['status']=='ready' and (evidence_file is None or not Path(evidence_file).is_file()):
        raise ValueError('provide the local snapshot before publishing a ready-evidence probe')
    origin=lambda url:(urlsplit(url).scheme,urlsplit(url).netloc)
    if origin(journal_url)!=origin(event_url):raise ValueError('journal and ingest must have the same backend origin')
    if urlsplit(journal_url).username or urlsplit(journal_url).password:raise ValueError('credentials in URL are forbidden')
    identity=hashlib.sha256(json.dumps({'template':template,'destination':sink.delivery_identity,
        'journal_url':journal_url,'journal_key':journal_key},sort_keys=True,allow_nan=False).encode()).hexdigest()
    root.mkdir(parents=True,exist_ok=True)
    with deployment_lock(root/'probe.lock'):
        prepared=root/'probe.json'
        if prepared.exists():
            intent=json.loads(prepared.read_text())
            if intent['identity_sha256']!=identity:raise ValueError('probe input or endpoint changed')
        else:
            event_id=str(uuid4());event={**template,'event_id':event_id}
            if template.get('execution_backend')=='synthetic-test':
                event.update(camera_id='MOSPROM-INTEGRATION-PROBE',stream_epoch=event_id,
                    track_key='MOSPROM-INTEGRATION-PROBE/'+event_id+'/1/1')
            intent={'schema_version':'1.0','identity_sha256':identity,'event':event,'duplicate_ack':False}
            save_json(prepared,intent)
        event=validate_event(intent['event']);started=time.monotonic();box=Outbox(root/'probe.sqlite')
        try:
            box.enqueue(event);box.dispatch(sink)
            if box.counts()['pending']:raise RuntimeError('backend has not acknowledged committed delivery')
            if not intent['duplicate_ack']:
                sink.publish(event);intent['duplicate_ack']=True;save_json(prepared,intent)
            url=journal_url.replace('{event_id}',quote(event['event_id'],safe=''))
            value=json.loads(_get(url,token=token,timeout=timeout))
            if journal_key is not None:value=value[journal_key]
            items=value if isinstance(value,list) else [value]
            matches=[validate_event(item) for item in items if isinstance(item,dict) and item.get('event_id')==event['event_id']]
            if len(matches)!=1 or matches[0]['revision']!=event['revision']:
                raise ValueError('journal did not return one exact incident/revision')
            payload=sink.prepare_payload(event)
            if matches[0]!=payload:raise ValueError('journal differs from the committed wire payload')
            evidence_status='NOT_EXERCISED'
            if event['evidence']['status']=='ready':
                if evidence_file is None:raise ValueError('local evidence file required for exact byte verification')
                local=Path(evidence_file).read_bytes()
                media_url=payload['evidence'].get('snapshot_ref')
                if not media_url:raise ValueError('this probe verifies snapshot evidence')
                media_token=token if origin(media_url)==origin(event_url) else None
                remote=_get(media_url,token=media_token,timeout=timeout,max_bytes=16*1024*1024)
                if hashlib.sha256(remote).digest()!=hashlib.sha256(local).digest():raise ValueError('evidence bytes differ')
                evidence_status='PASS'
            report={'status':'PASS','receiver_kind':receiver_kind,'event_id':event['event_id'],
                'checked_at':datetime.now(timezone.utc).isoformat(),
                'revision':event['revision'],'committed_ack':'PASS','duplicate_same_revision_ack':'PASS',
                'journal_exact_payload':'PASS','evidence_http_sha256':evidence_status,
                'wall_ms':(time.monotonic()-started)*1000,
                'scope':'labelled integration probe; external backend is verified only when receiver_kind=external'}
            save_json(root/'report.json',report);save_json(root/'last-attempt.json',report);return report
        except Exception as error:
            save_json(root/'last-attempt.json',{'status':'NOT_COMPLETED','event_id':event['event_id'],
                'receiver_kind':receiver_kind,'checked_at':datetime.now(timezone.utc).isoformat(),
                'error_type':type(error).__name__})
            raise
        finally:box.close()


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('event-url','journal-url','event-file','state-dir'):parser.add_argument('--'+name,required=True)
    parser.add_argument('--evidence-base-url');parser.add_argument('--evidence-file');parser.add_argument('--journal-key')
    parser.add_argument('--receiver-kind',choices=['external','local-test'],default='external')
    parser.add_argument('--timeout',type=float,default=5)
    args=parser.parse_args(argv)
    try:report=run_probe(**vars(args));print(json.dumps(report));return 0
    except Exception as error:
        # No server body, URL, authentication or exception message is logged.
        print(json.dumps({'status':'NOT_COMPLETED','error_type':type(error).__name__}));return 1


if __name__=='__main__':raise SystemExit(main())
