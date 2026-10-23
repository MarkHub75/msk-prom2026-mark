import requests,pathlib,json,hashlib,zlib,struct
p=pathlib.Path('_WORK/W2_06_EVIDENCE');m=json.loads((p/'mmodalfire_manifest.json').read_text());ses=requests.Session();log=[]
def fetch(a,b):
 r=ses.get('https://ndownloader.figshare.com/files/53696243',headers={'Range':f'bytes={a}-{b}'},timeout=30);assert r.status_code==206;log.append({'start':a,'end':b,'status':r.status_code,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()});return r.content
end=fetch(4929210002,4929210009);prefix=(p/'rar_first64k.bin').read_bytes()[:29]
for i in m['members']:
 if i['filename'].endswith('.xlsx') or i['filename'].endswith('Readme.txt'):
  data=fetch(i['offset'],i['data_offset']+i['data_size']-1);out=p/('metadata_'+('sheet' if '.xlsx' in i['filename'] else 'readme')+'.rar');out.write_bytes(prefix+data+end)
(p/'metadata_member_ranges.json').write_text(json.dumps(log,indent=2))
