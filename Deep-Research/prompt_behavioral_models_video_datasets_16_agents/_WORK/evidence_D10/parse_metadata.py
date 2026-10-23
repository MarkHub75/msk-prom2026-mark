import requests,pathlib,re,json,csv,collections,datetime
p=pathlib.Path('_WORK/evidence_D10')
r=requests.get('https://sites.google.com/up.edu.mx/har-up',timeout=25)
p.joinpath('har-up.html').write_text(r.text,encoding='utf-8')
print('iframes', re.findall(r'<iframe[^>]+src="([^"]+)',r.text))
for name in ['urfall-cam0-falls.csv','urfall-cam0-adls.csv']:
 rows=list(csv.reader(p.joinpath(name).open()))
 group=collections.defaultdict(list)
 for x in rows: group[x[0]].append(x)
 out={'rows':len(rows),'sequences':len(group),'labels':dict(collections.Counter(x[2] for x in rows)),'sequences_with_lying':[k for k,v in group.items() if any(x[2]=='1' for x in v)],'transitions':{k:[(v[i][1],v[i][2]) for i in range(len(v)) if i==0 or v[i][2]!=v[i-1][2]] for k,v in group.items()}}
 p.joinpath(name+'.summary.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 print(name,json.dumps(out)[:1200])
