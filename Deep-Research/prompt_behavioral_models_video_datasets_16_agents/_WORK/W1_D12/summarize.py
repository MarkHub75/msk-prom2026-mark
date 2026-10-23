import csv,json,pathlib,collections,zipfile,hashlib
p=pathlib.Path('_WORK/W1_D12');rs=list(csv.reader((p/'pdestre_annotation_08-11-2019-1-1.txt').read_text().splitlines()));print('PDESTRE',len(rs),collections.Counter(len(r) for r in rs),'last',collections.Counter(r[-1] for r in rs));print('phone', [r for r in rs if r[-1]=='7'][:3])
s={'pdestre_rows':len(rs),'pdestre_action_lastcol':dict(collections.Counter(r[-1] for r in rs)),'pdestre_phone_examples':[r for r in rs if r[-1]=='7'][:3]}
for split in ['train','val','test']:
 d=json.loads((p/f'active_object_instances_meccano_{split}.json').read_text());print(split,len(d['images']),len(d['annotations']),d['categories']);print('EX',d['annotations'][0]);s[split]={'images':len(d['images']),'annotations':len(d['annotations']),'categories':d['categories'],'resolutions':dict(collections.Counter(f"{i['width']}x{i['height']}" for i in d['images']))}
 a=list(csv.DictReader((p/f'action_MECCANO_{split}_actions.csv').open()));print('actions',len(a),'videos',sorted(set(r['video_id'] for r in a)));s[split]['actions']=len(a);s[split]['videos']=sorted(set(r['video_id'] for r in a));s[split]['action_map']=dict(sorted({int(r['action_id']):r['action_name'] for r in a}.items()))
with zipfile.ZipFile(p/'meccano_hands.zip') as z:
 n=next(n for n in z.namelist() if n.endswith('.csv'));txt=z.read(n).decode();print('HAND',n,txt[:1000]);(p/'meccano_hand_sample.csv').write_text(txt,encoding='utf-8')
(p/'schema_summary.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
