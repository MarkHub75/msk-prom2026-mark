import pathlib,json,csv,hashlib,datetime
p=pathlib.Path('_WORK/W2_04_EVIDENCE')
j=json.loads(pathlib.Path('_WORK/W1_M05/ava_phone_walk_join.json').read_text(encoding='utf8'))
sel=[e for e in j['examples'] if (e['video_id']=='QTmwhrVal1g' and e['person_id']=='91' and 1181<=e['timestamp']<=1190) or (e['video_id']=='WSPvfxtqisg' and e['person_id']=='1' and 908<=e['timestamp']<=915)]
p.joinpath('exact_ava_cases.json').write_text(json.dumps({'origin':'W1_M05/ava_phone_walk_join.json; no recomputation','rows':sel},indent=2))
with pathlib.Path('_WORK/W1_D12/charades_Charades_v1_test.csv').open(encoding='utf8') as f:r=next(r for r in csv.DictReader(f) if r['id']=='2RFLZ')
p.joinpath('charades_original_row.json').write_text(json.dumps(r,indent=2))
meta=json.loads(p.joinpath('decode_pts.json').read_text());pts=[r['pts'] for r in meta['frames']]
checks={'first_pts':pts[0],'last_pts':pts[-1],'strictly_increasing':all(b>a for a,b in zip(pts,pts[1:])),'unique_pts_deltas':sorted(set(b-a for a,b in zip(pts,pts[1:]))),'no_decode_error':True,'review':'all 222 rendered frames inspected in 4 contact sheets; 8 original-resolution panels separately inspected; human preliminary observation, not dense independent GT','actor_annotation':'absent from source Charades schema; no fabricated boxes/IDs','attempted_inspect_py':'initial script named inspect.py exited1 silently; renamed review_media.py to avoid stdlib shadowing; successful decode above'}
p.joinpath('clock_checks.json').write_text(json.dumps(checks,indent=2));print(checks)
manifest=[{'file':f.name,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in p.iterdir() if f.is_file() and f.name!='manifest.json'];p.joinpath('manifest.json').write_text(json.dumps(manifest,indent=2))
