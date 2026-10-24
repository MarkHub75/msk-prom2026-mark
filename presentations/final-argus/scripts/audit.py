"""Check final skeleton content, reproducible source hashes and native output."""
from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
sources=read('research/source-index.json')
for s in sources['sources']:assert sha(s['path'])==s['sha256'],s['path']
story=read('craft/story.json')
for s in story['sources']:assert sha(s['path'])==s['sha256'],s['path']
inventory=read('evidence/composition.json');slots=read('screenshot-slots.json')
assert len(inventory['slides'])==8 and len(story['scenes'])==8
text='\n'.join(t['text'] for s in inventory['slides'] for t in s['text'])
assert text.count('АРГУС')==1 and 'SafeWatch' not in text
assert len(slots)==7 and all(s['state']=='placeholder' for s in slots)
assert not list((ROOT/'assets/screens').glob('*.png'))
assert sum(n['duration'] for n in read('speaker-notes.json'))==280
for n,s in enumerate(inventory['slides'],1):assert sha(f'slides/slide-{n:02}.png')==s['sha256']
summary=read('research/main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json')
assert (summary['frames_processed'],summary['wall_s'],summary['throughput_fps'],summary['end_to_end_s']['total'])==(400,19.09,20.95,31.0)
assert all(t in text for t in ['400 кадров','1280 × 720','≈21','19,09 с','31 с'])
assert 'не задержка тревоги' in text and 'а не точность обнаружения' in text
exports=read('evidence/exports/report.json');assert exports['status']=='PASS' and exports['powerPointOpenRenderExport']=='PASS'
report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),slides=8,ui_placeholders=7,actual_ui_screenshots=0,brand_visible_occurrences=1,source_hashes_verified=len(sources['sources']),story_source_hashes_verified=len(story['sources']),speaker_budget_seconds=280,limits=['No new LinQ run','No front/final runtime certification','Not a human acceptance verdict','No independent industrial accuracy claim'])
(ROOT/'evidence/content-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:8 slides,7 explicit UI placeholders,one visible product name,frozen facts and sources.')
