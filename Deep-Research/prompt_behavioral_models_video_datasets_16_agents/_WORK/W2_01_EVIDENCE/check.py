import requests, pathlib, hashlib, json, zipfile, datetime, collections
P=pathlib.Path(__file__).parent
REV='759b39c13fea6ba094afc1fa932f51dc1b11cbf9'
log=[]
def get(url,name,cap=60000000):
 r=requests.get(url,timeout=(15,60),stream=True)
 chunks=[]; n=0
 for b in r.iter_content(65536):
  n+=len(b)
  if n>cap: raise ValueError('cap')
  chunks.append(b)
 data=b''.join(chunks)
 (P/name).write_bytes(data)
 log.append(dict(url=url,status=r.status_code,bytes=len(data),headers=dict(r.headers),sha256=hashlib.sha256(data).hexdigest(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),name=name))
 (P/'ACCESS.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
 return data
base='https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/'
arc='rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.zip'
get(base+'onnx_sdk/'+arc,arc)
z=zipfile.ZipFile(P/arc)
manifest=[]
for i in z.infolist():
 if i.is_dir(): continue
 data=z.read(i.filename)
 manifest.append(dict(name=i.filename,size=i.file_size,compressed=i.compress_size,sha256=hashlib.sha256(data).hexdigest()))
 target=P/'extracted'/i.filename
 target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
(P/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
for path,name in [('projects/rtmpose/README.md','README.md'),('projects/rtmpose/rtmpose/body_2d_keypoint/rtmpose-m_8xb256-420e_coco-256x192.py','pose_config.py'),('projects/rtmpose/rtmdet/person/rtmdet_nano_320-8xb32_coco-person.py','detector_config.py'),('projects/rtmpose/examples/onnxruntime/main.py','onnx_main.py'),('LICENSE','MMPose_LICENSE'),('NOTICE','MMPose_NOTICE')]:
 get('https://raw.githubusercontent.com/open-mmlab/mmpose/'+REV+'/'+path,name,2000000)
print(json.dumps(manifest,indent=2))
