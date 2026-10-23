import requests,pathlib,json,re,datetime
p=pathlib.Path('_WORK/W1_M05');urls={'ava_excluded':'https://research.google.com/ava/download/ava_val_excluded_timestamps_v2.2.csv','ava_eval_labels':'https://research.google.com/ava/download/ava_action_list_v2.2_for_activitynet_2019.pbtxt','ava_dataset_code':'https://raw.githubusercontent.com/open-mmlab/mmaction2/main/mmaction/datasets/ava_dataset.py','mmaction_github':'https://github.com/open-mmlab/mmaction2'}
logs=[]
for k,u in urls.items():
 r=requests.get(u,timeout=25);(p/(k+'.txt')).write_bytes(r.content);logs.append({'key':k,'url':u,'status':r.status_code,'bytes':len(r.content),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 if k=='mmaction_github':
  m=re.search(r'"currentOid":"([a-f0-9]+)"',r.text);print('MMAction revision',m.group(1) if m else 'unknown');(p/'mmaction_revision_observed.txt').write_text(m.group(1) if m else 'unknown')
(p/'access_final.json').write_text(json.dumps(logs,indent=2));j=json.loads((p/'ava_phone_walk_join.json').read_text());excluded=set(tuple(x.split(',')) for x in (p/'ava_excluded.txt').read_text().strip().splitlines());print('excluded join',sum((x['video_id'],str(x['timestamp'])) in excluded for x in j['examples']));print('eval labels',[(m[0],m[1]) for m in re.findall(r'name: "([^"]+)"\s+label_id: (\d+)',(p/'ava_eval_labels.txt').read_text()) if m[1] in ['14','15','57']]);print(logs)
