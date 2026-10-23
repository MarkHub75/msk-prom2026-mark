import pathlib,json,hashlib,re,urllib.parse,datetime
p=pathlib.Path('_WORK/W2_A_MATERIALS')
metal='https://etp.metal-it.ru/files/get/62wbdjrEsToerTN9EwXP9CpFfBsF9xSzNKxV8QdmWuGdUN4P1Z9RmCqv6HC6Gmdg7j/%D0%A2%D0%B5%D1%85.%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5.pdf'
s=pathlib.Path('_WORK/W1_E_PROCUREMENT_FAILURES.md').read_text(encoding='utf8');ntek=re.search(r'https://oao-ntek[^\s]+',s).group();n=urllib.parse.unquote(ntek.rsplit('/',1)[1])
manifest=[]
for name,url,t in [('Тех. задание.pdf',metal,'2026-10-23 06:12–06:14 UTC'),(n,ntek,'2026-10-23 06:16–06:18 UTC')]:
 b=(p/name).read_bytes();manifest.append({'filename':name,'source_url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'transport':'Public Google Docs Viewer fetched public source; downloaded binary from viewer-emitted googleusercontent URL. No authentication. Direct requests SSL EOF.','access_window_utc':t,'original_binary_at_origin_not_independently_hash_compared':True})
(p/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
# Remove only our transient viewer HTML, empty extraction/proxy responses and duplicate renamed NTEK; preserve source-name PDFs and page renders.
for name in ['DSSL_OFFICE_FRAME.html','DSSL_OFFICE_VIEWER.html','DSSL_PROXY_RESPONSE.txt','DSSL_VIEWERNG.html','DSSL_VIEWER_RESPONSE.html','DSSL_VIEWER_UPLOAD_RESPONSE.txt','GOOGLE_VIEWER_RESPONSE.html','METAL_IT_EXTRACT.txt','METAL_IT_PROXY_EXTRACT.txt','НТЭК_ПЕРЕЧЕНЬ_2024.pdf']:
 q=p/name
 if q.is_file():q.unlink()
