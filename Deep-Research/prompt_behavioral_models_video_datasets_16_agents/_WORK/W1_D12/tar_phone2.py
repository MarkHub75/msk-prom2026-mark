import requests,tarfile,pathlib,json,csv,collections
p=pathlib.Path('_WORK/W1_D12');old=json.loads((p/'pdestre_phone_search.json').read_text())[-1];pos=old['header_offset']+512+((old['size']+511)//512)*512;u='https://p-destre.di.ubi.pt/datasets/dataset.tar';s=requests.Session();out=[];read=0
for i in range(16):
 r=s.get(u,headers={'Range':f'bytes={pos}-{pos+511}'},timeout=15);m=tarfile.TarInfo.frombuf(r.content,'utf-8','replace');rec=dict(member=m.name,size=m.size,header_offset=pos)
 if m.name.endswith('.txt') and not pathlib.Path(m.name).name.startswith('._') and m.size<4000000:
  rr=s.get(u,headers={'Range':f'bytes={pos+512}-{pos+511+m.size}'},timeout=25);read+=len(rr.content);rs=list(csv.reader(rr.text.splitlines()));ph=[r for r in rs if len(r)==26 and r[-1]=='7'];rec.update(status=rr.status_code,rows=len(rs),phone_rows=len(ph),phone_ids=dict(collections.Counter(r[1] for r in ph)));print(rec)
  if ph:(p/('pdestre_annotation_'+pathlib.Path(m.name).name)).write_bytes(rr.content)
  if any(r[1]!='-1' for r in ph):out.append(rec);break
 out.append(rec);pos+=512+((m.size+511)//512)*512
 if read>9000000:break
(p/'pdestre_phone_search2.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('read_bytes',read)
