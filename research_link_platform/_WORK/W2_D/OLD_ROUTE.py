import requests,pathlib,json,datetime,hashlib
p=pathlib.Path(__file__).parent; sha='2ad93ed85739319d9f364b984a04a8a3b2ff8f12'; log=[]
def fetch(name,url):
 r=requests.get(url,timeout=30); (p/name).write_bytes(r.content); log.append(dict(file=name,url=url,status=r.status_code,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest())); return r
t=fetch('OLD_TREE.json',f'https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/{sha}?recursive=1').json()
for x in t.get('tree',[]):
 path=x['path']
 if 'detection/' in path and ('yolov5' in path or path.endswith('README.md')):
  print(path)
  fetch('OLD_'+path.split('/')[-1],f'https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/{sha}/{path}')
(p/'OLD_HTTP_LOG.json').write_text(json.dumps(log,indent=2),encoding='utf8')
