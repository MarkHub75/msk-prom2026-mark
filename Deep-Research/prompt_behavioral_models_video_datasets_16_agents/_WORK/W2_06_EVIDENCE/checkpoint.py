import requests,io,json,pathlib,hashlib,zipfile,pickletools,datetime
p=pathlib.Path('_WORK/W2_06_EVIDENCE'); rev='13017fe8af477c25f5298d168e2dfede4b000753'
u=f'https://huggingface.co/rabahdev/fire-smoke-yolov8n/resolve/{rev}/best.pt'
r=requests.get(u,timeout=40); r.raise_for_status(); assert len(r.content)<10000000;(p/'best.pt').write_bytes(r.content)
z=zipfile.ZipFile(io.BytesIO(r.content)); pk=next(n for n in z.namelist() if n.endswith('data.pkl')); data=z.read(pk)
# Disassemble bytecode only. No pickle load, torch import, model execution.
out=io.StringIO();pickletools.dis(data,out=out);(p/'checkpoint_pickle_disassembly.txt').write_text(out.getvalue(),encoding='utf8')
(p/'checkpoint_static.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':u,'status':r.status_code,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'zip_members':[{'name':i.filename,'size':i.file_size,'compressed':i.compress_size} for i in z.infolist()],'pickle_member':pk},indent=2));print('checkpoint',len(r.content),hashlib.sha256(r.content).hexdigest())
