import datetime,hashlib,json,pathlib,re
root=pathlib.Path(__file__).parent
work=root.parent
raw=(work/'W1_08/presentation2026_tinyfish.json').read_bytes()
text=json.loads(raw)['results'][0]['text']
rows=[]
for line in text.splitlines():
    m=re.match(r'^(\d+) (\S+) ([18]) ([\d,]+) ([\d,\-]+) ([\d,]+) ([\d,\-]+)$',line)
    if not m: continue
    idx,model,batch,hp,hl,hpq,ql=m.groups()
    f=lambda s:float(s.replace(',','.'))
    row={'source':'W2-I-S01','locator':f'p4 extracted row {idx}','model_label':model,'batch':int(batch),'input_shape':None,'weights_hash':None,'compile_preset':None,'quality':None,'scenario':None,'latency_statistic':None,'latency_boundaries':None,'throughput_denominator':'seconds (FPS label); sample/query/completed-image semantics undisclosed','devices_actual':None,'tested_here':False,'evidence_type':'vendor_reported_table_text_only','HP':{'throughput_FPS_literal':hp,'latency_ms_literal':hl},'HPQ':{'throughput_FPS_literal':hpq,'latency_ms_literal':ql},'arithmetic_only':{'HPQ_over_HP_throughput':f(hpq)/f(hp),'reciprocal_HP_ms':1000/f(hp),'same_latency_literals':hl==ql}}
    if hl!='-': row['arithmetic_only']['HP_throughput_times_reported_latency_seconds']=f(hp)*f(hl)/1000
    rows.append(row)
(root/'MEASUREMENT_RECORDS.json').write_text(json.dumps({'source_snapshot_sha256':hashlib.sha256(raw).hexdigest(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'warning':'No correction of published units. Arithmetic diagnostics are not measurements. Source is W1 extraction, not new visual evidence.','records':rows},ensure_ascii=False,indent=2),encoding='utf-8')
tree=json.loads((root/'REPO_TREE.json').read_text())
summary={'tree_truncated':tree['truncated'],'tracked_paths':len(tree['tree']),'matching_result_log_experiment_paths':[x['path'] for x in tree['tree'] if any(y in x['path'].lower() for y in ['experiment','mlperf_log','results_summary','accuracy.txt'])]}
(root/'REPO_SCOPE.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary)); print('table records',len(rows))
