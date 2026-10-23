import requests,pathlib,json,datetime,hashlib,zipfile,io,csv,collections,concurrent.futures
p=pathlib.Path('_WORK/W1_M05'); p.mkdir(exist_ok=True)
urls={'upt_readme':'https://raw.githubusercontent.com/fredzzhang/upt/main/README.md','upt_model':'https://raw.githubusercontent.com/fredzzhang/upt/main/upt.py','upt_utils':'https://raw.githubusercontent.com/fredzzhang/upt/main/utils.py','upt_license':'https://raw.githubusercontent.com/fredzzhang/upt/main/LICENSE','upt_revision':'https://api.github.com/repos/fredzzhang/upt/commits/main','hico_readme':'https://raw.githubusercontent.com/fredzzhang/hicodet/main/README.md','hico_download':'https://raw.githubusercontent.com/fredzzhang/hicodet/main/download.sh','ava_download':'https://sites.research.google/gr/ava/download/','ava_val':'https://research.google.com/ava/download/ava_val_v2.2.csv.zip','ava_labels':'https://research.google.com/ava/download/ava_action_list_v2.2.pbtxt'}
def get(k,u):
 try:
  r=requests.get(u,timeout=30); b=r.content; (p/(k+('.zip' if k=='ava_val' else '.txt'))).write_bytes(b);return {'key':k,'url':u,'status':r.status_code,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 except Exception as e:return {'key':k,'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: log=list(ex.map(lambda kv:get(*kv),urls.items()))
(p/'access.json').write_text(json.dumps(log,indent=2),encoding='utf8');print(json.dumps(log,indent=2))
z=zipfile.ZipFile(p/'ava_val.zip'); rows=list(csv.reader(io.StringIO(z.read(z.namelist()[0]).decode()))); grouped=collections.defaultdict(lambda: {'actions':set(),'boxes':set()})
for r in rows:
 k=(r[0],int(r[1]),r[7]); grouped[k]['actions'].add(int(r[6]));grouped[k]['boxes'].add(tuple(r[2:6]))
phones={k:v for k,v in grouped.items() if v['actions']&{15,57}}; joins={k:v for k,v in phones.items() if 14 in v['actions']}
out={'rows':len(rows),'person_timestamps':len(grouped),'phone_person_timestamps':len(phones),'phone_walk_person_timestamps':len(joins),'phone_counts':{str(i):sum(i in v['actions'] for v in grouped.values()) for i in [14,15,57]},'join_counts':{str(i):sum(i in v['actions'] for v in joins.values()) for i in [15,57]},'join_videos':sorted({k[0] for k in joins}),'phone_videos':len({k[0] for k in phones}),'phone_person_keys':len({(k[0],k[2]) for k in phones}),'join_person_keys':len({(k[0],k[2]) for k in joins}),'box_conflicts':sum(len(v['boxes'])>1 for v in joins.values())}
# Consecutive sparse annotated samples are candidates, not continuous verified events.
runs=[]
for vid,pid in sorted({(k[0],k[2]) for k in joins}):
 ts=sorted(k[1] for k in joins if k[0]==vid and k[2]==pid);run=[]
 for t in ts:
  if run and t!=run[-1]+1:runs.append({'video_id':vid,'person_id':pid,'timestamps':run});run=[]
  run.append(t)
 if run:runs.append({'video_id':vid,'person_id':pid,'timestamps':run})
out['runs']=sorted(runs,key=lambda x:-len(x['timestamps']));out['examples']=[{'video_id':k[0],'timestamp':k[1],'person_id':k[2],'actions':sorted(v['actions']),'boxes':sorted(v['boxes'])} for k,v in joins.items()]
(p/'ava_phone_walk_join.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in out.items() if k not in ['examples','runs']},indent=2));print('Longest runs',json.dumps(out['runs'][:8]))
