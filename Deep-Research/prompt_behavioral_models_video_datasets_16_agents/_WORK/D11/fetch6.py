import requests,pathlib,json,datetime,hashlib
p=pathlib.Path('_WORK/D11');stem='VIRAT_S_050301_00_000000_000036';ann=json.loads((p/'all_annotation_items.json').read_text());out=[]
for x in ann:
 if x['name'].startswith(stem) and not x['name'].endswith('mapping.txt'):
  u='https://data.kitware.com/api/v1/item/'+x['_id']+'/download';r=requests.get(u,timeout=30);(p/x['name']).write_bytes(r.content);out.append(dict(name=x['name'],url=u,status=r.status_code,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),access=datetime.datetime.now(datetime.timezone.utc).isoformat()))
vid=requests.get('https://data.kitware.com/api/v1/item?folderId=56f581ce8d777f753209ca43&limit=0',timeout=30).json();(p/'all_video_items.json').write_text(json.dumps(vid));v=next(x for x in vid if x['name']==stem+'.mp4');print('video',v)
files=requests.get('https://data.kitware.com/api/v1/item/'+v['_id']+'/files',timeout=30).json();(p/'selected_video_files.json').write_text(json.dumps(files));u='https://data.kitware.com/api/v1/file/'+files[0]['_id']+'/download';r=requests.head(u,timeout=30,allow_redirects=True);out.append(dict(name=v['name'],url=u,method='HEAD',status=r.status_code,headers=dict(r.headers),item_size=v['size'],access=datetime.datetime.now(datetime.timezone.utc).isoformat()))
(p/'access6.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
for x in ann:
 if x['name']==stem+'.viratdata.mapping.txt':
  for l in (p/x['name']).read_text().splitlines():
   a=l.split()
   if a[1]=='10':print('run',a[:6],'object ids',[k for k,b in enumerate(a[6:]) if b=='1'])
