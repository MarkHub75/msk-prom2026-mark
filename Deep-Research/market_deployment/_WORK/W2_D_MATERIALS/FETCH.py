import pathlib,re,json,requests,sys
p=pathlib.Path(__file__).parent
url=sys.argv[1] if len(sys.argv)>1 else 'https://rosstat.gov.ru/storage/mediabank/pr_travm_2025.xlsx'
r=requests.get('https://docs.google.com/viewerng/viewer',params={'url':url},timeout=30)
print('viewer',r.status_code,len(r.content))
t=r.text
(p/'VIEWER.html').write_text(t,encoding='utf8')
u=json.loads('"'+re.search(r'(/viewerng/upload[^"\s]+)',t).group(1)+'"')
r=requests.get('https://docs.google.com'+u,timeout=30)
print(r.status_code,r.text[:5000])
(p/'VIEWER_UPLOAD.txt').write_text(r.text,encoding='utf8')
data=json.loads(r.text[4:])
binary=requests.get(data['pdf'],timeout=30)
stem='METHOD_538' if '538' in url else 'pr_travm_2025_VIEWER_CONVERTED'
(p/(stem+'.pdf')).write_bytes(binary.content)
import fitz
doc=fitz.open(stream=binary.content,filetype='pdf')
text='\n'.join(page.get_text() for page in doc)
(p/(stem+'_EXTRACT.txt')).write_text(text,encoding='utf8')
print('PDF',len(binary.content),'pages',len(doc),text)
