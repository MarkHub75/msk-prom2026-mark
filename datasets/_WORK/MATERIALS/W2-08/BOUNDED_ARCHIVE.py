import requests,pathlib,json
p=pathlib.Path('_WORK/MATERIALS/W2-08');u='https://github.com/Rishit-dagli/CPPE-Dataset/releases/download/v0.1.0/dataset.tar.gz';r=requests.get(u,headers={'Range':'bytes=0-8388607'},stream=True,timeout=45); data=b''
for ch in r.iter_content(1024*256):
 data+=ch
 if len(data)>=8388608:break
r.close();(p/'dataset_FIRST8MiB.tar.gz.part').write_bytes(data);(p/'RANGE_RESPONSE.json').write_text(json.dumps({'url':u,'final_url':r.url,'status':r.status_code,'headers':dict(r.headers),'bytes_read':len(data)},indent=2));print(r.status_code,len(data),r.headers.get('Content-Range'))
t=json.loads(pathlib.Path('_WORK/MATERIALS/W1-10/CPPE-Dataset_tree.json').read_text());print([x['path'] for x in t['tree'] if any(k in x['path'].lower() for k in ['meta','data','json','csv','download'])])
