"""Checks factual numerals against frozen primary JSON and all composed text ink."""
from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
snap=ROOT/'research/source-snapshots'
raw=json.loads((snap/'main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json').read_text())
assert (raw['frames_total'],raw['frames_processed'],raw['wall_s'],raw['throughput_fps'],raw['end_to_end_s']['total'],raw['inflight'])==(400,400,19.09,20.95,31.0,8)
smoke=read('research/smoke-mock-fresh.json')
assert len(smoke['rows'])==30 and all(row['result']=='PASS' for row in smoke['rows']) and smoke['target']=='mock'
ml=(snap/'matvey_cv__ml__EVAL_REPORT.md').read_text()
assert '335' in ml and 'NOT_ACCEPTED' in ml
sdk=(snap/'matvey_cv__docs__STATUS.md').read_text()
assert '2026.9.45' in sdk and 'TPU_H1M' in sdk
parity=json.loads((snap/'matvey_cv__ml__reports__pose-linq-ur01-parity.json').read_text())
assert parity['paired_frames']==11 and 'fall missed' in parity['quality_scope']
comp=read('evidence/composition.json')
assert len(comp['slides'])==8
cmap={k:TTFont(ROOT/'assets/fonts'/v).getBestCmap() for k,v in [('regular','GolosText-Regular.ttf'),('semi','GolosText-Semibold.ttf'),('bold','GolosText-Bold.ttf')]}
checks=[]
for slide in comp['slides']:
    p=ROOT/f"slides/slide-{slide['slide']:02}.png"
    assert Image.open(p).size==(1920,1080)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==slide['sha256']
    for t in slide['text']:
        assert all(ord(c) in cmap[t['weight']] for c in t['text']),t['text']
        x1,y1,x2,y2=t['bounds']
        assert x1>=96 and x2<=1824 and y1>=54 and y2<=1026,t
    for i,a in enumerate(slide['text']):
        for b in slide['text'][i+1:]:
            x1,y1,x2,y2=a['bounds']; u1,v1,u2,v2=b['bounds']
            assert min(x2,u2)<=max(x1,u1) or min(y2,v2)<=max(y1,v1), (slide['slide'],a['text'],b['text'])
    if slide['slide']==3:
        visible=' '.join(t['text'] for t in slide['text'])
        assert all(s in visible for s in ['Тест детектора','≈21','19,09','Recall/IoU','не точность'])
    if slide['slide']==6:
        assert 'Демонстрационные данные. Кадры синтетические. Рамки размечены вручную.' in [t['text'] for t in slide['text']]
    checks.append(dict(slide=slide['slide'],allGlyphsPresent=True,safeTextInk=True,imageHashMatch=True,textPairsDoNotOverlap=True))
report=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),slides=8,
    baselinePrimaryJSON='400/400;19.09s;20.95FPS;31.0s;inflight8',freshMock='30PASS/0FAIL/0SKIP',
    ownModels='Latest335 software-tests report and negative one-fall development result cross-checked',checks=checks,
    limits=['Semantic claim support additionally reviewed by independent technical researcher; this script alone cannot certify meaning.',
            'Artwork and screenshot internal text require visual inspection. Room projection and spoken delivery are not measured.'])
(ROOT/'evidence/content-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS:8image hashes, glyph coverage, safe text ink and primaryJSON numerals.')
