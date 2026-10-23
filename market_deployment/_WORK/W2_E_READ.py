import fitz,pathlib,requests,re,urllib.parse,json,hashlib,datetime
p=pathlib.Path('_WORK/W2_E_MATERIALS')
d=fitz.open(p/'410_PP_2024_BASE.pdf')
for i in [3,4,6,7]:
 t=d[i].get_text(); print('PAGE',i+1);print(t[t.find('5.1.'): ] if '5.1.' in t else t[-2500:])
urls=[('VESTNIK_2026_52.pdf','https://vestnikmoscow.mos.ru/wp-content/uploads/2026/09/zhurnal-vestnik-moskvy-№-52.pdf'),('537_PP_2025.pdf','https://www.mos.ru/upload/documents/files/8910/537-PP.pdf?1')]
for name,u in urls:
 try:
  r=requests.get('https://docs.google.com/gview',params={'embedded':'1','url':u},timeout=25);m=re.search(r'https://doc-[^" ]+',r.text)
  if not m: print(name,'NO_URL');continue
  b=requests.get(m.group(),timeout=25).content
  if b[:4]==b'%PDF':
   (p/name).write_bytes(b); print(name,len(b))
   mf=json.loads((p/'MANIFEST.json').read_text(encoding='utf8'));mf.append(dict(file=name,url=u,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),transport='Public Google Docs Viewer'));(p/'MANIFEST.json').write_text(json.dumps(mf,ensure_ascii=False,indent=2),encoding='utf8')
 except Exception as e:print(type(e).__name__)
