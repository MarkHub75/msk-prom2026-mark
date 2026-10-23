import requests,pathlib,zipfile,io,csv,json,collections
p=pathlib.Path('_WORK/W1_D12');u='https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades.zip';r=requests.get(u,timeout=25);(p/'Charades.zip').write_bytes(r.content);print(r.status_code,len(r.content));z=zipfile.ZipFile(io.BytesIO(r.content));print(z.namelist())
for n in z.namelist():
 if not n.endswith('/'):(p/('charades_'+pathlib.Path(n).name)).write_bytes(z.read(n))
cl=(p/'charades_Charades_v1_classes.txt').read_text();print('\n'.join(l for l in cl.splitlines() if any(w in l.lower() for w in ['phone','walk','book','laptop'])));print((p/'charades_license.txt').read_text() if (p/'charades_license.txt').exists() else 'NO LICENSE FILE')
for n in ['train','test']:
 rs=list(csv.DictReader((p/f'charades_Charades_v1_{n}.csv').open()));print(n,len(rs),rs[0]);ph=[x for x in rs if any(c in x['actions'] for c in ['c107','c108','c109'])];print(ph[:1])
