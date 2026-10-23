import pathlib,csv,collections,json
p=pathlib.Path('_WORK/W1_D12');s={}
for split in ['train','test']:
 rs=list(csv.DictReader((p/f'charades_Charades_v1_{split}.csv').open()));ct=collections.Counter();ex={};clips={}
 for r in rs:
  for a in r['actions'].split(';'):
   if not a:continue
   c,b,e=a.split();
   if c in ['c015','c016','c017','c018','c019']:
    ct[c]+=1;clips.setdefault(c,set()).add(r['id']);ex.setdefault(c,{'id':r['id'],'subject':r['subject'],'actions':r['actions'],'length':r['length']})
 s[split]={'intervals':dict(ct),'clips':{k:len(v) for k,v in clips.items()},'examples':ex};print(split,s[split])
(p/'charades_phone_summary.json').write_text(json.dumps(s,indent=2));print('SELECT',s['test']['examples']['c019'])
