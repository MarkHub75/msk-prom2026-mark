from pathlib import Path
import shutil,subprocess,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
out=ROOT/'assets/linq';out.mkdir(exist_ok=True)
src=Path('/mnt/d/templates/msk-promhack/msk-prom2026-mark/ARGUS_linq_tpu_frame0.png')
shutil.copy2(src,out/src.name)
head=subprocess.check_output(['git','rev-parse','origin/matvey_cv'],cwd=REPO).decode().strip()
paths=['docs/handoffs/EGOR_LINQ_VIDEO_20261024.md','ml/reports/video-handoff-20261024.json']
records=[]
for p in paths:
    data=subprocess.check_output(['git','show',head+':'+p],cwd=REPO)
    name='research/linq-proof__'+p.replace('/','__');(ROOT/name).write_bytes(data)
    records.append(dict(path=name,commit=head,original=p,sha256=hashlib.sha256(data).hexdigest()))
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
meta=dict(checked_at=stamp,image=dict(path='assets/linq/'+src.name,source=str(src),sha256=hashlib.sha256(src.read_bytes()).hexdigest(),display='Whole source1280×576 scaled proportionally to1920×864; centred on16:9canvas; no crop,annotations or redrawing'),git_sources=records,primary_dataset=dict(title='Video Dataset for Safe and Unsafe Behaviours',authors=['Oğuzhan Önal','Emre Dandıl'],year=2024,version=1,doi='10.17632/xjmtb22pff.1',url='https://data.mendeley.com/datasets/xjmtb22pff/1',license='CC BY 4.0',license_url='https://creativecommons.org/licenses/by/4.0/',verified='Primary Mendeley page checked using web tool; its description identifies industrial security-camera footage.'),limits=['Historical saved TPU responses; no fresh LinQ call in this presentation task','Only selected video frames processed,not whole522-frame recording','Input/output tensor retention confirmed by Git handoff report; rawNPZ not re-audited locally in this session','Independent hardware attestation and industrial event accuracy not established'])
(ROOT/'research/linq-proof-index.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'exports/ATTRIBUTION.txt').write_text('Oğuzhan Önal; Emre Dandıl (2024). Video Dataset for Safe and Unsafe Behaviours. Mendeley Data,V1. DOI:10.17632/xjmtb22pff.1.\nhttps://data.mendeley.com/datasets/xjmtb22pff/1\nCC BY4.0: https://creativecommons.org/licenses/by/4.0/\nSlide9: source video frame with saved LinQ TPU results and annotations supplied by the team. Proportionally scaled; no crop or annotation changes.\nOther factory stills: synthetic ChatGPT Images assets provided in the team trailer kit.\n',encoding='utf-8')
print('Real LinQ frame,partial hardware handoff and primary dataset attribution recorded.')
