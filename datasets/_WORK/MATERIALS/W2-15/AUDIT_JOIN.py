import pathlib,json,csv,re,collections
p=pathlib.Path(__file__).parent;b=pathlib.Path('_WORK/MATERIALS/W1-06/PhysicalAI-Event-Videos');parents=json.loads((b/'2026/train/labels.json').read_text()); rules=json.loads((b/'anomaly-category-mapping.json').read_text())['rules'];manifest=list(csv.DictReader((b/'2026/train/video_manifest.csv').open())); print('manifestfields',manifest[:1]);print('parentfields',parents[0].keys());print('chunkfields',parents[0]['chunks'][0].keys())
out=[]
for par in parents:
 for c in par['chunks']:
  family=next((r['family'] for r in rules if re.search(r['regex'],c.get('anomaly_type',''),re.I)),'Other / ambiguous') if c.get('is_anomaly') else 'Normal'
  if family!='Smoking / vaping':continue
  matches=[m for m in manifest if m.get('dataset')==par['dataset'] and m['filename']==pathlib.PurePosixPath(par['video_path']).name]
  out.append({'key':[par['dataset'],par['video_id'],c['chunk_index']],'parent':{k:v for k,v in par.items() if k!='chunks'},'chunk':c,'media_manifest_matches':matches})
(p/'EXACT_JOIN.json').write_text(json.dumps(out,indent=2),encoding='utf8')
stats={'selected_chunks':len(out),'selected_parents':len(set(tuple(r['key'][:2]) for r in out)),'by_dataset':dict(collections.Counter(r['key'][0] for r in out)),'manifest_match_cardinality':dict(collections.Counter(len(r['media_manifest_matches']) for r in out)),'unique_chunk_keys':len(set(tuple(r['key']) for r in out)),'nonpositive_time_windows':[r['key'] for r in out if r['chunk']['end_time_sec']<=r['chunk']['start_time_sec']]}
(p/'JOIN_SUMMARY.json').write_text(json.dumps(stats,indent=2)); print(stats)
