import requests,pathlib,re,hashlib,json,datetime
p=pathlib.Path('_WORK/W2_E_MATERIALS');p.mkdir(exist_ok=True)
urls={
'VESTNIK_2026_52.pdf':'https://vestnikmoscow.mos.ru/wp-content/uploads/2026/09/zhurnal-vestnik-moskvy-%E2%84%96-52.pdf',
'410_PP_2024_BASE.pdf':'https://www.mos.ru/upload/documents/files/9314/PostanovleniePravitelstvaMoskviot22032022410-PP.pdf',
'537_PP_2025.pdf':'https://www.mos.ru/upload/documents/files/8910/537-PP.pdf',
'631_PP_2025_BASE.pdf':'https://www.mos.ru/upload/content/files/2b552d79304ffcce8e7c77de6d655d8f/0Post.pdf',
'GISP_GRANT_12449149.pdf':'https://portfolio.gisp.gov.ru/nmp/measure/12449149/pdf',
'EXPERTISE_410_PP_2025.pdf':'https://www.mos.ru/upload/documents/files/373/Zakluchenie410-PP.pdf'}
manifest=[]
for name,u in urls.items():
 try:
  r=requests.get('https://docs.google.com/gview',params={'embedded':'1','url':u},timeout=25)
  m=re.search(r'https://doc-[^" ]+',r.text)
  if not m: print(name,'NO_PDF_URL');continue
  b=requests.get(m.group(),timeout=25).content
  if b[:4]!=b'%PDF':print(name,'NOT_PDF',len(b));continue
  (p/name).write_bytes(b)
  manifest.append(dict(file=name,url=u,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),transport='Public Google Docs Viewer; binary original hash at origin not independently compared'))
  print(name,len(b))
 except Exception as e:print(name,type(e).__name__)
(p/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
