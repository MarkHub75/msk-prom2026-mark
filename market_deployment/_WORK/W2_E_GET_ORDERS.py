import requests,pathlib,re,hashlib,json,datetime
p=pathlib.Path('_WORK/W2_E_MATERIALS')
items=[('VESTNIK_2026_52.pdf','http://vestnikmoscow.mos.ru/wp-content/uploads/2026/09/zhurnal-vestnik-moskvy-%E2%84%96-52.pdf'),('ORDER_2026_SELECTION.pdf','https://gisp.gov.ru/nmp/upload/docs/7dd7592238429eb2c5dc9618f8f45540c2fc6aa88544674ad53f27ab0aaa7d9b.pdf'),('ORDER_2026_RISK.pdf','https://gisp.gov.ru/nmp/upload/docs/5d78d92ca2c61258b40b399cd551f6351a98f6b911a95fc41c79d7bf63d672b4.pdf')]
for name,u in items:
 try:
  r=requests.get('https://docs.google.com/gview',params={'embedded':'1','url':u},timeout=20);m=re.search(r'https://doc-[^" ]+',r.text)
  if not m:print(name,'NO_URL');continue
  b=requests.get(m.group(),timeout=20).content
  if b[:4]!=b'%PDF':print(name,'NOT_PDF');continue
  (p/name).write_bytes(b);mf=json.loads((p/'MANIFEST.json').read_text(encoding='utf8'));mf.append(dict(file=name,url=u,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),transport='Public Google Docs Viewer, origin hash not compared'));(p/'MANIFEST.json').write_text(json.dumps(mf,ensure_ascii=False,indent=2),encoding='utf8');print(name,len(b))
 except Exception as e:print(name,type(e).__name__)
