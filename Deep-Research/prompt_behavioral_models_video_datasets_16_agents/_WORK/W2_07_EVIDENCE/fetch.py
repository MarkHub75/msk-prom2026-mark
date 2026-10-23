import requests,json,hashlib,pathlib,datetime
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); logs=[]
def fetch(url,name):
 r=requests.get(url,timeout=60); logs.append(dict(url=url,status=r.status_code,headers=dict(r.headers),time=datetime.datetime.now(datetime.timezone.utc).isoformat(),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())); r.raise_for_status(); (p/name).write_bytes(r.content); return r
fetch('https://storage.googleapis.com/tf_model_garden/vision/movinet/movinet_a0_stream.tflite','movinet_a0_stream.tflite')
c=fetch('https://api.github.com/repos/tensorflow/models/commits/master','commit.json').json()['sha']; print('commit',c)
for path in ['README.md','modeling/movinet_layers.py','modeling/movinet.py','modeling/movinet_model.py','tools/export_saved_model.py','movinet_tutorial.ipynb','files/kinetics_600_labels.txt']:
 try: fetch('https://raw.githubusercontent.com/tensorflow/models/'+c+'/official/projects/movinet/'+path,path.replace('/','_'))
 except Exception as e: print(e)
fetch('https://raw.githubusercontent.com/tensorflow/models/'+c+'/LICENSE','LICENSE')
(p/'fetch_log.json').write_text(json.dumps(logs,indent=2)); print([(x['url'].split('/')[-1],x['status'],x['bytes']) for x in logs])
