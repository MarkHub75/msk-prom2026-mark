import requests,tarfile,pathlib,json
p=pathlib.Path('_WORK/W1_D12');a=json.loads((p/'pdestre_members.json').read_text());m=a[-1];pos=m['data_offset']+((m['size']+511)//512)*512;u='https://p-destre.di.ubi.pt/datasets/dataset.tar'
r=requests.get(u,headers={'Range':f'bytes={pos}-{pos+511}'},timeout=20);m=tarfile.TarInfo.frombuf(r.content,'utf-8','replace');print(m.name,m.size,pos)
r=requests.get(u,headers={'Range':f'bytes={pos+512}-{pos+511+m.size}'},timeout=20);(p/'pdestre_annotation_08-11-2019-1-1.txt').write_bytes(r.content);print(r.status_code,len(r.content),r.content[:300])
(p/'pdestre_annotation_access.json').write_text(json.dumps(dict(url=u,status=r.status_code,headers=dict(r.headers),member=m.name,size=m.size,header_offset=pos),indent=2))
