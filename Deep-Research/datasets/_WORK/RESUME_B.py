import sys,json,pathlib,collections,xml.etree.ElementTree as ET,hashlib,concurrent.futures
from W2_B_ZIP import Remote
import zipfile
from PIL import Image,ImageDraw,ImageOps
R=pathlib.Path(__file__).parent

def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf8")
def sfextra():
 o=R/'MATERIALS/W2-03';a=json.loads((o/'AUDIT.json').read_text());d=json.loads((R/'MATERIALS/W1-03/SFCHD-SCALE/dataset_SFCHD/annotations/all_data.json').read_text());ims={i['id']:i for i in d['images']};rr=[]
 for q in a['invalid_geometry']:
  b=q['annotation']['bbox'];im=ims[q['annotation']['image_id']];rr.append(max(0,-b[0],-b[1],b[0]+b[2]-im['width'],b[1]+b[3]-im['height']))
 allnames={i['file_name'] for i in d['images']};b=R/'MATERIALS/W1-03/SFCHD-SCALE/dataset_SFCHD/new_split_yolo';ss={s:set(pathlib.PurePosixPath(l).name for l in (b/(s+'.txt')).read_text().splitlines() if l.strip()) for s in ['train','val','test']}
 save(o/'SUPPLEMENT.json',{'out_of_bounds_n':len(rr),'max_overflow_pixels':max(rr),'over_0_001pixel':sum(x>0.001 for x in rr),'over_0_01pixel':sum(x>0.01 for x in rr),'train_val_intersection':sorted(ss['train']&ss['val']),'all_minus_trainval':sorted(allnames-(ss['train']|ss['val'])),'split_names_not_coco':sorted((ss['train']|ss['val']|ss['test'])-allnames),'split_duplicates':{s:len((b/(s+'.txt')).read_text().splitlines())-len(ns) for s,ns in ss.items()}})
 print('supplement',max(rr),flush=True)

def pairs(num):
 o=R/('MATERIALS/W2-'+num);f=Remote(num);z=zipfile.ZipFile(f);names=z.namelist();dest=o/'pairs';dest.mkdir(exist_ok=True);log=[]
 def get(n):
  p=dest/pathlib.Path(n).name
  if not p.exists():p.write_bytes(z.read(n))
  log.append({'member':n,'local':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});save(o/'SELECTED_MEMBERS.json',log);save(o/'RANGE_LOG_RESUME.json',f.log)
 if num=='04':
  d=json.loads((R/'MATERIALS/W1-03/SFCHD-SCALE/dataset_SFCHD/annotations/all_data.json').read_text());ims={i['id']:i for i in d['images']};aa=collections.defaultdict(list)
  for a in d['annotations']:aa[a['image_id']].append(a)
  chosen=[]
  for c in range(7):
   k=next(i for i,v in aa.items() if any(a['category_id']==c for a in v) and i not in chosen);chosen.append(k)
  chosen += [i for i in ims if ims[i]['file_name']=='192.168.2.20_1c_29.jpg']
  for k in chosen:
   n=next(n for n in names if pathlib.Path(n).name==ims[k]['file_name'] and '/images/' in n);get(n)
  save(o/'SAMPLE_SELECTION.json',[{'image':ims[k],'annotations':aa[k],'reason':'first annotation order example of each class, plus missing TXT case'} for k in chosen])
 elif num=='05':
  xmls=list(dest.glob('*.xml'));chosen=[p for p in xmls if p.stem in ['000000','000993','001477','part2_000069','part2_000761','PartA_00063','PartA_00535','PartA_00772']]
  for p in chosen:
   n=next(n for n in names if pathlib.Path(n).stem==p.stem and pathlib.Path(n).suffix.lower()=='.jpg');get(n)
 elif num=='06':
  labs=[n for n in names if n.startswith('CHV_dataset/annotations/') and n.endswith('.txt')]
  # spaced 24 labels, preserve existing four; choose class coverage from actual labels
  for n in labs[::max(1,len(labs)//24)][:24]:get(n)
  covered=set();chosen=[]
  for p in sorted(dest.glob('ppe_*.txt')):
   cs={int(l.split()[0]) for l in p.read_text().splitlines() if l.strip()}
   if cs-covered:chosen.append(p);covered|=cs
  for p in chosen:
   n=next(n for n in names if pathlib.Path(n).stem==p.stem and n.lower().endswith('.jpg') and not n.startswith('__MACOSX'));get(n)
  save(o/'SAMPLE_SELECTION.json',{'classes_in_labels':sorted(covered),'chosen':[p.name for p in chosen],'reason':'24 spaced real annotations plus previously saved, greedy six-class coverage'})
 save(o/'SELECTED_MEMBERS.json',log)
 print('done',num,len(log),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='extra':sfextra()
 else:pairs(sys.argv[1])
