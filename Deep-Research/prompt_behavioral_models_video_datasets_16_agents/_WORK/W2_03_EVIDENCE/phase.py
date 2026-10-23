import json,random,math
from pathlib import Path
P=Path('_WORK/W2_03_EVIDENCE');events=[('CAVIAR actor7',373,436,552),('CAVIAR actor6',385,489,552),('BEHAVE group1,2',44396-35450,44447-35450,11711),('BEHAVE group0,1',46306-35450,46375-35450,11711),('Walk1 actor1 control',236,511,612)]
rows=[]
for name,a,b,n in events:
 for rate in [25,1,2,5]:
  counts=[];rnd=[];burst=[];wait=[]
  for phase in range(25):
   # Canonical sample ticks at phase/25+k/rate, causal ceil to 25Hz source grid.
   ix=set()
   for k in range(math.ceil(n*rate/25)+1):
    i=phase+(k*25+rate-1)//rate
    if i<n:ix.add(i)
   sel=sorted(i for i in ix if a<=i<=b);counts.append(len(sel))
   if sel:wait.append((sel[0]-a)/25)
   for seed in range(100):
    rng=random.Random(seed);keep=[rng.random()>=.2 for _ in range(n)]
    rnd.append(sum(keep[i] for i in sel))
   for bs in range(a,b+1):burst.append(sum(not(bs<=i<bs+25) for i in sel))
  rows.append({'event':name,'inclusive_local':[a,b],'fps':rate,'phase_minmax':[min(counts),max(counts)],'random20pct_100seeds_phase_minmax':[min(rnd),max(rnd)],'one_second_burst_start_inside_event_minmax':[min(burst),max(burst)],'first_opportunity_delay_seconds_minmax':[min(wait),max(wait)]})
(P/'phase_observability.json').write_text(json.dumps(rows,indent=2))
print('| Label interval | fps | phase count | 20% random drop range | 1s burst range | first opportunity delay s |')
print('|---|---:|---:|---:|---:|---:|')
for r in rows:
 print('| '+r['event']+' | '+str(r['fps'])+' | '+' | '.join('–'.join(map(str,r[k])) for k in ['phase_minmax','random20pct_100seeds_phase_minmax','one_second_burst_start_inside_event_minmax','first_opportunity_delay_seconds_minmax'])+' |')
