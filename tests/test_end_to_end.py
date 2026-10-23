"""Synthetic tensor-to-alert contract test; never a hardware/accuracy benchmark."""
import json
import tempfile
import threading
import unittest
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
from ml.detection import preprocess, decode
from ml.behavior import BehaviorEngine
from ml.pipeline.delivery import Outbox, HttpEventSink
from ml.pipeline.runner import Pipeline


class EndToEndTest(unittest.TestCase):
    def test_synthetic_raw_tensors_to_single_committed_alert(self):
        received=[]
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                received.append(body)
                self.send_response(200);self.end_headers()
                self.wfile.write(json.dumps({'committed':True,'event_id':body['event_id'],'revision':body['revision']}).encode())
            def log_message(self,*args): pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                box=Outbox(Path(tmp)/'events.sqlite')
                sink=HttpEventSink(f'http://127.0.0.1:{server.server_port}/api/v1/ml/events',evidence_base_url='https://evidence.example/artifacts')
                pipe=Pipeline(BehaviorEngine(),box,tmp,sink)
                image=np.zeros((640,640,3),np.uint8)
                base={'input':{'name':'images','shape':[1,3,640,640],'layout':'NCHW','dtype':'float32'},'output_name':'output0','output_layout':'BCN'}
                pose_manifest={**base,'decoder':'pose_v8','classes':['person']}
                ppe_manifest={**base,'decoder':'detect_v8','classes':['helmet','bare_head']}
                _,transform=preprocess(image,pose_manifest)
                pose=np.zeros((1,56,1),np.float32)
                pose[0,:5,0]=[140,100,80,200,.99]
                points=np.zeros((17,3),np.float32)
                points[0]=[140,20,.99]
                points[5]=[120,50,.99];points[6]=[160,50,.99]
                points[11]=[120,130,.99];points[12]=[160,130,.99]
                pose[0,5:,0]=points.reshape(-1)
                ppe=np.array([140,22.5,40,35,.01,.99],np.float32).reshape(1,6,1)
                ds=decode({'output0':pose},pose_manifest,transform)+decode({'output0':ppe},ppe_manifest,transform)
                for t in range(0,5001,500):
                    batch={'schema_version':'1.0','camera_id':'c','stream_epoch':'s','frame_id':t//500,
                           'media_time_ms':t,'image_size':[640,640],'status':'ok','detections':ds,'backend':'synthetic-test'}
                    pipe.process(batch,image)
                self.assertEqual(len(received),1)
                self.assertEqual(received[0]['type'],'missing_helmet')
                self.assertEqual(received[0]['confirmed_media_ms'],2000)
                self.assertTrue(received[0]['evidence']['snapshot_ref'].startswith('https://evidence.example/artifacts/evidence/'))
                self.assertEqual(box.counts(),{'pending':0,'delivered':1})
                self.assertEqual(len(list((Path(tmp)/'evidence').glob('*.jpg'))),1)
                box.close()
        finally:
            server.shutdown();server.server_close();thread.join()
