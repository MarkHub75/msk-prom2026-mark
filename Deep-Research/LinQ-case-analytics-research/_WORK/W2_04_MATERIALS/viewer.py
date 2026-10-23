import pathlib,re,json,requests,fitz
p=pathlib.Path(__file__).parent
url='https://rosstat.gov.ru/storage/mediabank/Trud_2025.pdf'
r=requests.get('https://docs.google.com/viewerng/viewer',params={'url':url},timeout=25)
(p/'TRUD_VIEWER.html').write_text(r.text,encoding='utf8'); print('viewer',r.status_code,len(r.content))
u=json.loads('"'+re.search(r'(/viewerng/upload[^"\s]+)',r.text).group(1)+'"')
r=requests.get('https://docs.google.com'+u,timeout=25);(p/'TRUD_UPLOAD.txt').write_text(r.text,encoding='utf8')
data=json.loads(r.text[4:]);r=requests.get(data['pdf'],timeout=30);(p/'Trud_2025_VIEWER.pdf').write_bytes(r.content)
doc=fitz.open(stream=r.content,filetype='pdf');(p/'TRUD_EXTRACT.txt').write_text('\n'.join(f'\nPDFPAGE {i+1}\n'+page.get_text() for i,page in enumerate(doc)),encoding='utf8')
print('pdf',len(r.content),'pages',len(doc))
for i,page in enumerate(doc):
 t=page.get_text()
 if '5.11.' in t or '5.12.' in t or ('ПО ВИДАМ ЭКОНОМИЧЕСКОЙ' in t and 'ТРАВМ' in t):print('page',i+1,t[:10000])
