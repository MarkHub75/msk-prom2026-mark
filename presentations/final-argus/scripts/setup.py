from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import subprocess,json,hashlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
old=Path('/mnt/d/templates/msk-promhack/safewatch-checkpoint-pptx/presentations/checkpoint-2026-10-24')
for key,weight in [('Regular',400),('Semibold',600),('Bold',700)]:
    f=TTFont(ROOT/'assets/fonts/SourceSans3-Variable.ttf')
    instantiateVariableFont(f,{'wght':weight},inplace=True).save(ROOT/f'assets/fonts/SourceSans3-{key}.ttf')
heads={ref:subprocess.check_output(['git','rev-parse','origin/'+ref],cwd=REPO,text=True).strip() for ref in ['main','front/final','matvey_cv']}
specs=[('main','tech.md',[(29,78),(2994,3058),(3094,3131)]),('main','progress.md',[(1,36)]),
 ('main','docs/linq/LINQ_CONTRACT.md',[(73,109)]),
 ('main','results/linq_smoke/synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json',None),
 ('main','docs/ML_INTEGRATION.md',None),('main','contract/openapi.json',None),('main','contract/ws.schema.json',None),
 ('front/final','frontend/src/App.tsx',None),('front/final','frontend/src/roles.ts',None),
 ('front/final','frontend/src/features/Incident.tsx',None),('front/final','frontend/src/features/Stats.tsx',None),
 ('front/final','frontend/src/features/Journal.tsx',None),('front/final','frontend/src/styles/ds.css',[(1,104)]),
 ('matvey_cv','ml/EVAL_REPORT.md',None)]
sources=[]
for i,(ref,path,ranges) in enumerate(specs,1):
    data=subprocess.check_output(['git','show',heads[ref]+':'+path],cwd=REPO)
    name=ref.replace('/','-')+'__'+path.replace('/','__')
    if ranges:
        lines=data.decode().splitlines()
        data='\n'.join(f'{j}: {lines[j-1]}' for a,b in ranges for j in range(a,min(b,len(lines))+1)).encode()
        name+='.excerpt.txt'
    p='research/'+name;(ROOT/p).write_bytes(data)
    sources.append(dict(id=f's{i+1:02}',ref=ref,commit=heads[ref],original=path,path=p,ranges=ranges,sha256=hashlib.sha256(data).hexdigest()))
(ROOT/'research/source-index.json').write_text(json.dumps(dict(checked_at=datetime.now(ZoneInfo('Europe/Moscow')).isoformat(),heads=heads,sources=sources),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['exports.mjs','powerpoint-check.ps1','verify-exports.py','pdf-preview.py','package-review.py','browser-qa.mjs']:
    s=(old/'scripts'/name).read_text(encoding='utf-8-sig')
    s=s.replace('SafeWatch_Checkpoint_2026-10-24','ARGUS_Final_Skeleton').replace('safewatch-checkpoint-20261024','argus-final-skeleton').replace('safewatch-checkpoint-pptx/presentations/checkpoint-2026-10-24','argus-final-presentation/presentations/final-argus').replace('8724','8734').replace('8725','8735').replace('HUMAN_SAFEWATCH_CHECKPOINT_PRODUCTION_REVIEW','HUMAN_ARGUS_FINAL_SKELETON_REVIEW')
    s=s.replace("pptx.title = 'SafeWatch — технический чекпойнт — 24 октября 2026';","pptx.title = 'АРГУС — каркас финальной презентации';")
    s=s.replace("pptx.author = 'SafeWatch';","pptx.author = 'Команда продукта';").replace("pptx.company = 'SafeWatch';","pptx.company = 'Команда продукта';")
    s=s.replace('SafeWatch · технический чекпойнт · 8 слайдов','Каркас финальной презентации · 8 слайдов')
    (ROOT/'scripts'/name).write_text(s,encoding='utf-8')
(ROOT/'.gitattributes').write_text('* -text\nresearch/** -whitespace\nevidence/** -whitespace\nreview/** -whitespace\nassets/fonts/** -whitespace\n',encoding='utf-8')
print('Source snapshots, current design fonts and existing OS export tooling prepared.')
