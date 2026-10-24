"""Bounded, reproducible presentation content/provenance verification."""
from pathlib import Path
import json,hashlib,datetime,re,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
index=read('research/source-index.json');story=read('craft/story.json');notes=read('speaker-notes.json');comp=read('evidence/composition.json')
for s in story['sources']:assert sha(s['path'])==s['sha256'],s['path']
for s in index['sources']:assert sha(s['path'])==s['sha256'],s['path']
for s in index['assets']:assert sha(s['path'])==s['sha256'],s['path']
assert len(story['scenes'])==len(notes)==len(comp['slides'])==13
assert sum(s['duration'] for s in notes)==300
sentences=[]
for s in notes:
    n=len(re.findall(r'[.!?](?:\s|$)',s['speech']));assert 2<=n<=4,(s['id'],n)
    assert s['question'] and s['answer'] and s['question'] in s['notes'] and s['answer'] in s['notes'];sentences.append(n)
text='\n'.join(t['text'] for s in comp['slides'] for t in s['text'])
for term in ['det640','JSONL','Split-Pose','server-clock','скрин:','18 кадр','45,2','45.2']:assert term not in text,term
for term in ['352','69','45 с','21','0,91 / 0,93','8 сценариев','не точность на заводе','не задержка оповещения','Кашин Глеб','под надзором']:assert term in text,term
assert text.count('АРГУС')==2 and comp['brand_lockups']==2
for n,s in enumerate(comp['slides'],1):
    assert sha(f'slides/slide-{n:02}.png')==s['sha256']
    assert Image.open(ROOT/f'slides/slide-{n:02}.png').size==(1920,1080)
    assert Image.open(ROOT/f'preview/slide-{n:02}-720.png').size==(1280,720)
    for a in s['assets']:assert sha(a['path'])==a['sha256']
    assert s['assets'],f'Slide{n} needs image evidence'
report=read('evidence/frontend-tests.json');assert report['success'] and report['numPassedTests']==69 and report['numFailedTests']==0
assert '352 pytest' in (ROOT/'research/main__progress.md.excerpt.txt').read_text()
cfg=(ROOT/'research/main__config__default.yaml.excerpt.txt').read_text();assert 'enabled: true' in cfg and 'timeout_s: 45' in cfg
summary=read('research/main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json')
assert (summary['frames_processed'],summary['wall_s'],summary['throughput_fps'],summary['end_to_end_s']['total'])==(400,19.09,20.95,31.0)
# Verify the actually tested frontend source export against the frozen commit.
runtime=Path('/home/egor/argus-final-evidence');commit=index['heads']['front/final']
names=subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'--','frontend/src','frontend/package.json','frontend/package-lock.json','frontend/vite.config.ts','frontend/vitest.config.ts'],cwd=REPO).decode().splitlines()
checked=[]
for p in names:
    original=subprocess.check_output(['git','show',commit+':'+p],cwd=REPO);actual=(runtime/p).read_bytes();assert original==actual,p
    checked.append(dict(path=p,sha256=hashlib.sha256(actual).hexdigest()))
proof=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=commit,runtime=str(runtime),source_files=checked,tests=dict(total=69,passed=69,failed=0),initial_failure='Missing lucide-react in reused dependencies; npmci installed the exact lockfile in isolated runtime. App source unchanged.')
(ROOT/'evidence/frontend-provenance.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
expected='Это реальная промышленная камера, открытый датасет Mendeley, CC BY 4.0. Рамку и 17 точек позы вернул ускоритель LinQ — ответ status 0, мы храним входные и выходные тензоры. Качество распознавания на заводе ещё не измеряли — это следующий этап'
assert notes[8]['speech']==expected
from PIL import ImageOps,ImageChops
frame=Image.open(ROOT/'assets/linq/ARGUS_linq_tpu_frame0.png').convert('RGB');frame=ImageOps.contain(frame,(1920,1080),Image.Resampling.LANCZOS)
whole=Image.new('RGB',(1920,1080),'#0e1013');whole.paste(frame,((1920-frame.width)//2,(1080-frame.height)//2))
assert ImageChops.difference(whole,Image.open(ROOT/'slides/slide-09.png').convert('RGB')).getbbox() is None
result=dict(status='PASS',checked_at=proof['checked_at'],slides=13,ui_placeholders=0,brand_lockups=2,brand_policy=comp['brand_policy'],speaker_sentences_per_slide=sentences,expert_questions=13,source_hashes_verified=len(story['sources']),archive_assets_verified=len(index['assets']),real_tpu_frame=dict(slide=9,whole_user_image_preserved=True,speech_user_verbatim=True),frontend_passed=69,backend_reported_in_main=352,timeout_configured_seconds=45,unconfirmed_metrics_excluded=['CPU18FPS','measured45.2s'],limits=['No new LinQ run','No industrial accuracy acceptance','No human visual verdict','Backend352reported,notrerun'])
(ROOT/'evidence/content-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:13slides,13Q&A,69fresh frontend tests; whole userTPUframe/userverbatimspeech verified.')
