import requests,pathlib,json,fitz,rarfile,shutil
p=pathlib.Path('_WORK/MATERIALS/W2-10')
for k,u in {'folders':'https://data.mendeley.com/public-api/datasets/xjmtb22pff/folders/1','rootfiles':'https://data.mendeley.com/public-api/datasets/xjmtb22pff/files?folder_id=root&version=1&$start=0&$limit=1000'}.items():
 r=requests.get(u,timeout=40);(p/(k+'.json')).write_bytes(r.content);print(k,r.status_code,r.text[:1500])
doc=fitz.open('_WORK/MATERIALS/W2-09/paper.pdf');t='\n'.join(p.get_text() for p in doc);pathlib.Path('_WORK/MATERIALS/W2-09/paper.txt').write_text(t,encoding='utf8')
for word in ['Data Availability','3.1.','collected','label']:
 i=t.find(word);print(word,t[max(0,i-100):i+2600])
print('tools',[(x,shutil.which(x)) for x in ['unrar','unar','bsdtar','7z','ffmpeg']]);print('rar',rarfile.UNRAR_TOOL,rarfile.tool_setup())
