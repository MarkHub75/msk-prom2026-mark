import requests,tarfile,pathlib,json,csv,collections,datetime
p=pathlib.Path('_WORK/W1_D12');info=json.loads((p/'pdestre_annotation_access.json').read_text());pos=info['header_offset']+512+((info['size']+511)//512)*512;u=info['url'];s=requests.Session();out=[];read=0
for i in range(25):
 r=s.get(u,headers={'Range':f'bytes={pos}-{pos+511}'},timeout=15);m=tarfile.TarInfo.frombuf(r.content,'utf-8','replace');rec=dict(member=m.name,size=m.size,header_offset=pos)
 if m.name.endswith('.txt') and not pathlib.Path(m.name).name.startswith('._') and m.size<4000000:
  rr=s.get(u,headers={'Range':f'bytes={pos+512}-{pos+511+m.size}'},timeout=25);read+=len(rr.content);rs=list(csv.reader(rr.text.splitlines()));phones=[r for r in rs if len(r)==26 and r[-1]=='7'];rec.update(status=rr.status_code,rows=len(rs),phone_rows=len(phones),phone_examples=phones[:5]);print(rec)
  if phones:
   (p/('pdestre_annotation_'+pathlib.Path(m.name).name)).write_bytes(rr.content);out.append(rec);break
 out.append(rec);pos+=512+((m.size+511)//512)*512
 if read>12000000:break
(p/'pdestre_phone_search.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('read_bytes',read)
