"""Preserve unknown field meanings. Do not expose raw IDs as tracks."""
import pathlib,json,collections
p=pathlib.Path(__file__).parent;lines=pathlib.Path('_WORK/MATERIALS/W1-07/SARD_4.txt').read_text().splitlines();rows=[]
for number,line in enumerate(lines,1):
 t=line.split();rows.append({'line':number,'raw_id_1':int(t[0]),'raw_id_2':int(t[1]),'source_class':t[2],'raw_action':' '.join(t[3:-4]),'raw_box':list(map(int,t[-4:]))})
by=collections.defaultdict(list)
for r in rows:by[r['raw_id_2']].append(r)
summary={'rows':len(rows),'unique_raw_id_1':len(set(r['raw_id_1'] for r in rows)),'unique_raw_id_2':len(by),'raw_id_2_cross_class':[{'id':k,'classes':sorted(set(r['source_class'] for r in v))} for k,v in by.items() if len(set(r['source_class'] for r in v))>1],'nonpositive_xyxy_if_interpreted':sum(r['raw_box'][2]<=r['raw_box'][0] or r['raw_box'][3]<=r['raw_box'][1] for r in rows),'raw_id_2_examples':{str(k):[v[0],v[len(v)//2],v[-1]] for k,v in list(by.items())[:5]}}
(p/'PARSER_AUDIT.json').write_text(json.dumps(summary,indent=2));print({k:v for k,v in summary.items() if k!='raw_id_2_examples'})
