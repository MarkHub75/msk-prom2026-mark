from pathlib import Path
import subprocess,json,hashlib,datetime,zipfile,io,shutil
from PIL import Image,ImageOps,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
for d in ['assets/screens','assets/stills','assets/fonts','research','evidence','slides','preview','exports','craft','scripts']: (ROOT/d).mkdir(parents=True,exist_ok=True)
OLD=ROOT.parent/'final-argus'
for p in (OLD/'assets/fonts').iterdir():shutil.copy2(p,ROOT/'assets/fonts'/p.name)
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
heads={r:git('rev-parse','origin/'+r).decode().strip() for r in ['main','front/final','matvey_cv']}
spec=[('main','tech.md',[(29,78),(2994,3058),(3094,3131)]),('main','progress.md',[(1,32),(173,184),(210,219)]),('main','docs/linq/LINQ_CONTRACT.md',[(73,109)]),('main','results/linq_smoke/synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json',None),('main','config/default.yaml',[(139,164)]),('main','src/safewatch/services.py',[(1540,1590),(1730,1755)]),('main','docs/ML_INTEGRATION.md',None),('main','contract/openapi.json',None),('main','contract/ws.schema.json',None),('front/final','frontend/src/features/Stats.tsx',None),('front/final','frontend/src/features/ManagementStats.tsx',None),('front/final','frontend/src/features/CameraSetup.tsx',None),('front/final','frontend/src/features/Rules.tsx',None),('front/final','frontend/src/features/Incident.tsx',None),('front/final','frontend/src/features/Master.tsx',None),('front/final','frontend/src/features/Journal.tsx',None),('front/final','frontend/src/features/Report.tsx',None),('front/final','frontend/src/styles/ds.css',[(1,108)]),('matvey_cv','ml/EVAL_REPORT.md',None),('matvey_cv','ml/SCENARIO_COVERAGE.md',None),('matvey_cv','docs/ML_HANDOFF_MATVEY.md',None),('matvey_cv','ml/safewatch.delivery.json',None)]
index=[]
for n,(ref,path,ranges) in enumerate(spec,1):
    raw=git('show',heads[ref]+':'+path)
    if ranges:
        lines=raw.decode('utf-8-sig').splitlines(); raw=('\n'.join(f'{i}: {lines[i-1]}' for lo,hi in ranges for i in range(lo,min(hi,len(lines))+1))+'\n').encode()
    dest='research/'+ref.replace('/','-')+'__'+path.replace('/','__')+('.excerpt.txt' if ranges else '')
    (ROOT/dest).write_bytes(raw);index.append(dict(id=f's{n:02}',ref=ref,commit=heads[ref],original=path,path=dest,ranges=ranges,sha256=hashlib.sha256(raw).hexdigest()))
archive=Path('/mnt/d/templates/msk-promhack/msk-prom2026-mark/Downloads (2).zip')
assets=[]
with zipfile.ZipFile(archive) as outer:
    for name in outer.namelist():
        with zipfile.ZipFile(io.BytesIO(outer.read(name))) as inner:
            for item in inner.infolist():
                if item.is_dir():continue
                p=Path(item.filename);dest=None
                if name=='argus-screens.zip' and p.suffix.lower() in ['.png','.jpg']:dest=ROOT/'assets/screens'/p.name
                if name=='argus-trailer-kit.zip' and 'stills' in p.parts and p.suffix.lower()=='.png':dest=ROOT/'assets/stills'/p.name
                if name=='argus-trailer-kit.zip' and p.name=='README.md':dest=ROOT/'research/TRAILER_KIT_README.md'
                if dest:
                    data=inner.read(item);dest.write_bytes(data)
                    entry=dict(archive=name,member=item.filename,path=str(dest.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest())
                    if dest.suffix.lower() in ['.png','.jpg']:entry['size']=list(Image.open(dest).size)
                    assets.append(entry)
(ROOT/'research/source-index.json').write_text(json.dumps(dict(checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),heads=heads,sources=index,asset_archive=dict(path=str(archive),sha256=hashlib.sha256(archive.read_bytes()).hexdigest()),assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
screens=sorted(p for p in (ROOT/'assets/screens').glob('*.png'))
sheet=Image.new('RGB',(1800,((len(screens)+3)//4)*300),'#161616');font=ImageFont.truetype(str(ROOT/'assets/fonts/SourceSans3-Regular.ttf'),19)
for n,p in enumerate(screens):
    x=(n%4)*450;y=(n//4)*300;im=ImageOps.contain(Image.open(p).convert('RGB'),(430,250));sheet.paste(im,(x+(450-im.width)//2,y));ImageDraw.Draw(sheet).text((x+10,y+262),p.name,fill='white',font=font)
sheet.save(ROOT/'preview/input-screens.jpg',quality=90)
print(json.dumps(dict(heads=heads,sources=len(index),asset_files=len(assets),screens=len(screens)),ensure_ascii=False))
