from pathlib import Path
import requests,json,av,hashlib
r=Path('_WORK/W2-03_evidence')
for name,u in [('zenodo_record.json','https://zenodo.org/api/records/13354453'),('article.xml','https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC11416611')]:
 try:
  x=requests.get(u,timeout=25);x.raise_for_status();(r/name).write_bytes(x.content);print(name,x.status_code,len(x.content))
 except Exception as e: print(name,type(e).__name__,str(e))
p=r/'Subject3_Fall_07.mp4'; c=av.open(str(p)); hashes=[hashlib.sha256(f.to_ndarray(format='rgb24').tobytes()).hexdigest() for f in c.decode(video=0)]; c.close(); result={'scope':'decoded RGB hashes; uniqueness is not proof of capture authenticity','frames':len(hashes),'unique_entire_clip':len(set(hashes)),'tail_frames_76_268':len(hashes[76:]),'unique_tail':len(set(hashes[76:]))};(r/'F01_frame_uniqueness.json').write_text(json.dumps(result,indent=2));print(result)
