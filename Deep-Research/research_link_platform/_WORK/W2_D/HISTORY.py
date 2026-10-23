import pathlib,json,requests,datetime,hashlib
p=pathlib.Path(__file__).parent; log=[]
def get(name,url):
 r=requests.get(url,timeout=30); (p/name).write_bytes(r.content); log.append(dict(file=name,url=url,status=r.status_code,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),sha256=hashlib.sha256(r.content).hexdigest())); return r.json()
c=get('COMMITS_PAGE2.json','https://api.github.com/repos/sherstpasha/linq-cv-bench/commits?per_page=100&page=2')
print('page2',len(c))
for x in c: print(x['sha'][:12],x['commit']['message'].splitlines()[0])
for sha in ['842a9e424faa','f21c53313114','2ad93ed85739','6b76cce92310']:
 d=get('COMMIT_'+sha.upper()+'.json','https://api.github.com/repos/sherstpasha/linq-cv-bench/commits/'+sha)
 print(sha,[(f['filename'],f['status']) for f in d.get('files',[])])
(p/'HISTORY_HTTP_LOG.json').write_text(json.dumps(log,indent=2),encoding='utf8')
