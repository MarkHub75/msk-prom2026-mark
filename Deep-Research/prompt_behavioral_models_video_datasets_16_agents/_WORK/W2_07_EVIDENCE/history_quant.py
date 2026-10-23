import requests,json,pathlib
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); r=requests.get('https://api.github.com/repos/tensorflow/models/commits?path=official/projects/movinet&until=2021-07-22T00:00:00Z&per_page=1',timeout=30); (p/'historical_commit.json').write_text(r.text); print(r.status_code,r.text[:1600])
for name in ['a0-stream-kinetics-600-classification-tflite-int8','a0-stream-kinetics-600-classification-tflite-float16']:
 u='https://www.kaggle.com/api/v1/models/google/movinet/tflite/'+name+'/1/download'; r=requests.get(u,timeout=30,stream=True); print(u,r.status_code,r.url,r.headers.get('Content-Length'),r.headers.get('Content-Type')); (p/(name+'_headers.json')).write_text(json.dumps(dict(url=u,status=r.status_code,final=r.url,headers=dict(r.headers)),indent=2)); r.close()
