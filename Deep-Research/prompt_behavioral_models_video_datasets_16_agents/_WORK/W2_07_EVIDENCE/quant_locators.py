import requests,pathlib,json,bs4
p=pathlib.Path('_WORK/W2_07_EVIDENCE'); urls=['https://tfhub.dev/tensorflow/movinet/a0/stream/kinetics-600/classification/1','https://tfhub.dev/tensorflow/lite-model/movinet/a0/stream/kinetics-600/classification/tflite/float16/1','https://api.github.com/repos/tensorflow/models/commits?path=official/projects/movinet/modeling/movinet_layers.py&until=2021-07-22T00:00:00Z&per_page=1']; logs=[]
for i,u in enumerate(urls):
 try:
  r=requests.get(u,timeout=35); (p/f'quant_locator_{i}.txt').write_text(r.text,encoding='utf8'); logs.append(dict(url=u,status=r.status_code,final=r.url,headers=dict(r.headers),bytes=len(r.content))); print(i,r.status_code,r.url,len(r.content)); print(bs4.BeautifulSoup(r.text,'html.parser').get_text(' ',strip=True)[:1200])
 except Exception as e: logs.append(dict(url=u,error=str(e)))
(p/'quant_locator_log.json').write_text(json.dumps(logs,indent=2))
