import pathlib,json,requests,hashlib
p=pathlib.Path('_WORK/W2_06_EVIDENCE');m=json.loads((p/'mmodalfire_manifest.json').read_text());ses=requests.Session();log=[];prefix=(p/'rar_first64k.bin').read_bytes()[:29];r=ses.get('https://ndownloader.figshare.com/files/53696243',headers={'Range':'bytes=4929210002-4929210009'},timeout=20);end=r.content
for i in m['members']:
 if i['filename'].endswith(('Humidifier4-1.csv','Humidifier4-2.csv')):
  a=i['offset'];b=i['data_offset']+i['data_size']-1;r=ses.get('https://ndownloader.figshare.com/files/53696243',headers={'Range':f'bytes={a}-{b}'},timeout=25);assert r.status_code==206;out=p/(pathlib.PurePosixPath(i['filename']).stem+'.rar');out.write_bytes(prefix+r.content+end);log.append({'member':i,'status':r.status_code,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()})
(p/'sensor_member_access.json').write_text(json.dumps(log,indent=2))
