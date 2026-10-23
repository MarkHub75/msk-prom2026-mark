import csv,collections,json,pathlib,statistics,requests
p=pathlib.Path('_WORK/W1_D12');rs=list(csv.reader((p/'pdestre_annotation_11-11-2019-1-2.txt').read_text().splitlines()));ph=[r for r in rs if r[-1]=='7'];d={'rows':len(rs),'phone_rows':len(ph),'phone_ids':dict(collections.Counter(r[1] for r in ph)),'phone_frame_minmax':[min(int(r[0]) for r in ph),max(int(r[0]) for r in ph)],'phone_bbox_col4_range':[min(float(r[4]) for r in ph),max(float(r[4]) for r in ph)],'phone_bbox_col5_range':[min(float(r[5]) for r in ph),max(float(r[5]) for r in ph)],'action_counts':dict(collections.Counter(r[-1] for r in rs))};print(d);(p/'pdestre_phone_summary.json').write_text(json.dumps(d,indent=2))
a=json.loads((p/'pdestre_members.json').read_text());print([x for x in a if x['name'].endswith('/11-11-2019-1-2.MP4')])
for sid in set(r[1] for r in ph):
 pp=[int(r[0]) for r in ph if r[1]==sid];print(sid,len(pp),min(pp),max(pp))
print('resolution counts',json.loads((p/'schema_summary.json').read_text())['test']['resolutions'])
