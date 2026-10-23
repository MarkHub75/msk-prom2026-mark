import requests,tarfile,io,json,pathlib,time
p=pathlib.Path('_WORK/W1_D12');u='https://p-destre.di.ubi.pt/datasets/dataset.tar';session=requests.Session();out=[];pos=0;total=0
for i in range(170):
 r=session.get(u,headers={'Range':f'bytes={pos}-{pos+511}'},timeout=15)
 if r.status_code!=206 or len(r.content)!=512: print('BAD',r.status_code,len(r.content));break
 total+=len(r.content)
 try:m=tarfile.TarInfo.frombuf(r.content,'utf-8','replace')
 except Exception as e:print(e);break
 out.append({'name':m.name,'size':m.size,'header_offset':pos,'data_offset':pos+512})
 if '/annotation/' in m.name and m.name.endswith('.txt') and m.size<3000000:
  rr=session.get(u,headers={'Range':f'bytes={pos+512}-{pos+511+m.size}'},timeout=20);total+=len(rr.content)
  (p/('pdestre_'+pathlib.Path(m.name).name)).write_bytes(rr.content)
  print('ANNOT',m.name,m.size,rr.content[:200]);break
 pos+=512+((m.size+511)//512)*512
print('members',len(out),'bytes',total,'last',out[-3:]);(p/'pdestre_members.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
