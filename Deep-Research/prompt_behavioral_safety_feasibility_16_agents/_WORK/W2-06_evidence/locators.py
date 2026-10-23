import json,pathlib,hashlib,requests,pickletools,zipfile
r=pathlib.Path('_WORK/W2-06_evidence');out={}
for short,ver in [('rabah','8.4.51'),('farhat','8.4.150')]:
 with zipfile.ZipFile(r/(short+'_best.pt')) as z:
  b=z.read(next(n for n in z.namelist() if n.endswith('data.pkl')));ops=list(pickletools.genops(b)); snippets={}
  for i,(op,a,pos) in enumerate(ops):
   if op.name in ('BINUNICODE','SHORT_BINUNICODE') and a in ('names','imgsz','version','license','date','nc','yaml_file'):
    snippets.setdefault(a,[]).append({'offset':pos,'next_ops':[(o.name,arg,p) for o,arg,p in ops[i:i+17]]})
 out[short]={'snippets':snippets,'tag_ref':requests.get(f'https://api.github.com/repos/ultralytics/ultralytics/git/ref/tags/v{ver}',timeout=30).json()}
(r/'metadata_locators.json').write_text(json.dumps(out,indent=2));
files=[{'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in r.iterdir() if p.is_file() and not p.name.endswith('.jpg')];(r/'artifact_hashes.json').write_text(json.dumps(files,indent=2));print([(k,v['tag_ref'].get('object')) for k,v in out.items()])
