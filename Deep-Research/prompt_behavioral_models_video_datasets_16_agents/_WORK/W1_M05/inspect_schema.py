import requests,pathlib,json,re,hashlib,datetime
from bs4 import BeautifulSoup
p=pathlib.Path('_WORK/W1_M05')
u='https://raw.githubusercontent.com/fredzzhang/hicodet/9dd59c1/instances_train2015.json';r=requests.get(u,timeout=30);print('JSON',r.status_code,len(r.content));r.raise_for_status();d=r.json();(p/'hico_annotations.txt').write_bytes(r.content)
print('keys',list(d)); summary={'url':u,'download_bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'keys':list(d),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()}
for k,v in d.items():
 if k!='annotation': print(k,str(v)[:2000])
# Derive class correlation rather than assume output verb ids are 600-way HOI ids.
for k in ['objects','verbs','correspondence']:
 if k in d:summary[k]=d[k]
(p/'hico_schema_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
s=BeautifulSoup((p/'upt_weights_binary.txt').read_text(), 'html.parser');f=s.find('form'); params={x['name']:x.get('value','') for x in f.find_all('input') if x.get('name')};u=f['action'];r=requests.get(u,params=params,timeout=30,stream=True);chunk=next(r.iter_content(4096));print('WEIGHT_RANGE',r.status_code,r.headers.get('content-type'),r.headers.get('content-length'),chunk[:20].hex());r.close();(p/'weight_probe.json').write_text(json.dumps({'request_base':u,'id':params['id'],'status':r.status_code,'headers':dict(r.headers),'first4096_sha256':hashlib.sha256(chunk).hexdigest(),'prefix_hex':chunk[:20].hex(),'download_completed':False,'time':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
text=(p/'upt_github.txt').read_text();m=re.search(r'"currentOid":"([a-f0-9]+)"',text); print('UPT REVISION',m.group(1) if m else 'not found');(p/'upt_revision_observed.txt').write_text(m.group(1) if m else 'not found')
