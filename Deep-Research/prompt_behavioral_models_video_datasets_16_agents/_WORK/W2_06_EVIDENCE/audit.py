import pathlib,csv,json,collections,datetime,hashlib
p=pathlib.Path('_WORK/W2_06_EVIDENCE');m=json.loads((p/'mmodalfire_manifest.json').read_text());stats={'complete':m['complete'],'members':len(m['members']),'extensions':dict(collections.Counter(pathlib.PurePosixPath(x['filename']).suffix if not x['directory'] else 'directory' for x in m['members'])),'all_block_crcs_ok':all(x['crc_ok'] for x in m['blocks']),'solid_member_count':sum(x['solid'] for x in m['members']),'total_range_bytes':m['total_range_bytes'],'videos':sorted([{'filename':x['filename'],'compressed':x['data_size'],'bytes':x['uncompressed']} for x in m['members'] if x['filename'].endswith('.mp4')],key=lambda x:x['compressed'])};(p/'manifest_summary.json').write_text(json.dumps(stats,indent=2))
audit=[]
for f in (p/'sensor').rglob('*.csv'):
 rows=list(csv.reader(f.read_text(encoding='gb18030').splitlines()));r={'file':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'rows_excluding_header':len(rows)-1,'header':rows[0],'first':rows[1],'last':rows[-1],'column_counts':dict(collections.Counter(len(x) for x in rows))}
 if f.name.endswith('4-1.csv'):
  ts=[datetime.datetime.fromisoformat(x[1]) for x in rows[1:]];dt=[(b-a).total_seconds() for a,b in zip(ts,ts[1:])];r.update({'wall_clock_span_s':(ts[-1]-ts[0]).total_seconds(),'strict_monotonic':all(x>0 for x in dt),'min_step':min(dt),'max_step':max(dt)})
 audit.append(r)
(p/'sensor_csv_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'stats':{k:v for k,v in stats.items() if k!='videos'},'sensor':audit},ensure_ascii=False,indent=2))
