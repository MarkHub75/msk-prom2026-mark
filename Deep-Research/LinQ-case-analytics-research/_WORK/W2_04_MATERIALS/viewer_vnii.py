import pathlib,re,json,requests,fitz
p=pathlib.Path(__file__).parent
url='https://adminbalagansk.ru/download/viewer/ot/21102025.pdf'
r=requests.get('https://docs.google.com/viewerng/viewer',params={'url':url},timeout=25)
(p/'VNII_VIEWER.html').write_text(r.text,encoding='utf8'); print('viewer',r.status_code,len(r.content))
u=json.loads('"'+re.search(r'(/viewerng/upload[^"\s]+)',r.text).group(1)+'"')
r=requests.get('https://docs.google.com'+u,timeout=25);(p/'VNII_UPLOAD.txt').write_text(r.text,encoding='utf8')
data=json.loads(r.text[4:]);r=requests.get(data['pdf'],timeout=30);(p/'VNII_VIEWER.pdf').write_bytes(r.content)
doc=fitz.open(stream=r.content,filetype='pdf');(p/'VNII_EXTRACT.txt').write_text('\n'.join(f'\nPDFPAGE {i+1}\n'+page.get_text() for i,page in enumerate(doc)),encoding='utf8')
print('pdf',len(r.content),'pages',len(doc))
for i,page in enumerate(doc):
 t=page.get_text()
 if '5.11.' in t or '5.12.' in t or ('ПО ВИДАМ ЭКОНОМИЧЕСКОЙ' in t and 'ТРАВМ' in t):print('page',i+1,t[:10000])

