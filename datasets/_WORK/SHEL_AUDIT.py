from pathlib import Path
import json,xml.etree.ElementTree as ET,collections,hashlib
r=Path('_WORK');p=r/'MATERIALS/W2-07';cc=collections.Counter();bad=[];empty=[];fn=[];wh=collections.Counter();flags=collections.Counter();examples=collections.defaultdict(list)
for f in (p/'XML').glob('*.xml'):
 rt=ET.parse(f).getroot();w=int(rt.findtext('size/width'));h=int(rt.findtext('size/height'));wh[(w,h)]+=1;obs=rt.findall('object')
 if not obs:empty.append(f.name)
 if Path(rt.findtext('filename')).stem!=f.stem:fn.append([f.name,rt.findtext('filename')])
 cats=collections.Counter()
 for ob in obs:
  c=ob.findtext('name');cc[c]+=1;cats[c]+=1;b=[int(ob.findtext('bndbox/'+k)) for k in ['xmin','ymin','xmax','ymax']];flags[(ob.findtext('truncated'),ob.findtext('difficult'))]+=1
  if b[0]<0 or b[1]<0 or b[2]>w or b[3]>h or b[2]<=b[0] or b[3]<=b[1]:bad.append([f.name,c,b,[w,h]])
 for c in cats:
  if len(examples[c])<2:examples[c].append(f.name)
 if cats.get('person_no_helmet') and cats.get('person_with_helmet') and len(examples['mixed'])<4:examples['mixed'].append(f.name)
 if sum(cats.values())>100 and len(examples['crowded'])<3:examples['crowded'].append(f.name)
m=json.loads((r/'MATERIALS/W1-15/shel-Annotations-manifest.json').read_text());hh=[]
for x in m:
 f=p/'XML'/x['filename'];sha=hashlib.sha256(f.read_bytes()).hexdigest()
 if sha!=x['content_details']['sha256_hash']:hh.append(f.name)
a={'files':len(list((p/'XML').glob('*.xml'))),'objects':sum(cc.values()),'classes':cc,'invalid_boxes':bad,'empty':empty,'filename_mismatch':fn,'dimensions':{str(k):v for k,v in wh.items()},'flags':{str(k):v for k,v in flags.items()},'examples':examples,'hash_mismatch':hh};(p/'XML_AUDIT.json').write_text(json.dumps(a,indent=2));print('SUMMARY',a['files'],a['objects'],cc,'bad',len(bad),'empty',empty,'fn',len(fn),'flags',flags,'hashmismatch',hh,'examples',examples)
