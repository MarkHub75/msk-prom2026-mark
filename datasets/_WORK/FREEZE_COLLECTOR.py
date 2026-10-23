from pathlib import Path
import re,json,hashlib,datetime
R=Path(__file__).resolve().parent.parent
files=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md','_WORK/ID_MAP.md','_WORK/AUTHOR_BRIEF.md']
for name,prefix in [('RAW_FACTS.md','F'),('OPEN_QUESTIONS.md','Q')]:
 p=R/name;s=p.read_text(encoding='utf8')
 s=re.sub(r'^### ('+prefix+r'\d{3}) —',lambda m:f'<a id="{m[1].lower()}"></a>\n\n'+m[0],s,flags=re.M)
 p.write_text(s,encoding='utf8')
p=R/'_WORK/COLLECTOR_FREEZE.json';data=json.loads(p.read_text(encoding='utf8'))
data['checked_at']=datetime.datetime.now().astimezone().isoformat()
data['files']={f:{'bytes':(R/f).stat().st_size,'sha256':hashlib.sha256((R/f).read_bytes()).hexdigest()} for f in files}
data['freeze']=True
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print('Collector freeze:',data['checked_at'])
print('Explicit anchors:',{f:len(re.findall(r'<a id="[sfq]\d{3}"', (R/f).read_text(encoding='utf8'))) for f in ['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md']})
