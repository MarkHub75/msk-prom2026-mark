"""Record the current fifteen-slide exports; preserve historical review evidence."""
from pathlib import Path
import datetime, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
exports=read('evidence/exports-15/report.json')
pdf=read('evidence/pdf-report.json')
assert exports['status']=='PASS' and exports['slides']==15 and exports['powerPointOpenRenderExport']=='PASS'
assert pdf['status']=='PASS' and pdf['pages']==15
assert len(read('speaker-notes.json'))==len(read('craft/story.json')['scenes'])==15
paths=['exports/ARGUS_Final_15.pptx','exports/ARGUS_Final.pdf','exports/ATTRIBUTION.txt','preview/ALL_15_SLIDES.png','README.md','SPEAKER_SCRIPT.md','SOURCES.md','VERIFICATION.md','speaker-notes.json','craft/story.json','research/front-final__docs__ECONOMICS_SOURCES.md','research/COMPUTE_BRIEF.md','evidence/exports-15/report.json','evidence/powerpoint-15/report.json','evidence/pdf-report.json']+[f'slides/slide-{n:02}.png' for n in range(1,16)]
data=dict(status='READY_FOR_DELIVERY',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),slides=15,human_acceptance='PENDING',branch='codex/argus-final-presentation',sources=read('research/source-index.json')['heads'],economics_source=dict(branch='front/final',commit='87f8a2c47d9621c8b7620d20c3c0548c0ebb128a',path='docs/ECONOMICS_SOURCES.md'),artifacts=[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=sha(p)) for p in paths])
(ROOT/'DELIVERY.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p}\n' for p in paths),encoding='utf-8')
print('READY: 15 slides, native PowerPoint and lossless PDF checked; human review pending.')
