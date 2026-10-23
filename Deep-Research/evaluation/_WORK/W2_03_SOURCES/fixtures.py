"""Exact finite-design arithmetic, invented corpus, no model execution."""
from itertools import combinations
from math import comb
from fractions import Fraction as F
from pathlib import Path
import json,platform
N,n=4,2
samples=list(combinations(range(N),n))
def mean(xs):
 xs=list(xs)
 return sum(xs)/len(xs)
def varhat(vals,s):
 v=[F(vals[i]) for i in s]; avg=mean(v)
 s2=sum((x-avg)**2 for x in v)/(n-1)
 return N*N*(1-F(n,N))*s2/n
counts=[2,1,0,1]; hits=[1,0,0,1]
episodes=[('P',-5,2,None),('A',2,3,0),('B',8,29,1),('C',10,12,0),('D',39,45,1)]
episode_rows=[]
derived_counts=[0]*N;derived_hits=[0]*N
for key,start,end,success in episodes:
 owner=int(start//10) if 0<=start<40 else None
 touched=[i for i in range(N) if start<(i+1)*10 and end>i*10]
 inclusion=F(sum(bool(set(s)&set(touched)) for s in samples),len(samples))
 episode_rows.append({'id':key,'start':start,'end':end,'owner':owner,'overlap_cores':touched,'overlap_inclusion':inclusion})
 if owner is not None:
  derived_counts[owner]+=1;derived_hits[owner]+=success
assert derived_counts==counts and derived_hits==hits
rows=[]
for s in samples:
 rows.append({'s':s,'events_hat':F(N,n)*sum(counts[i] for i in s),'detected_hat':F(N,n)*sum(hits[i] for i in s),'variance_events_hat':varhat(counts,s)})
est=[r['events_hat'] for r in rows]
assert mean(est)==sum(counts)
assert mean(r['detected_hat'] for r in rows)==sum(hits)
assert mean((x-mean(est))**2 for x in est)==mean(r['variance_events_hat'] for r in rows)
ratio_counts=[1,1,1,7];ratio_hits=[1,1,1,0]
ratios=[F(sum(ratio_hits[i] for i in s),sum(ratio_counts[i] for i in s)) for s in samples]
assert mean(ratios)==F(9,16)
overlap={m:1-F(comb(N-m,n) if N-m>=n else 0,comb(N,n)) for m in [1,2,3,4]}
pi=[F(1),F(1),F(1,2),F(1,2)]; selected=[0,1,3]
ue=sum(F(counts[i])/pi[i] for i in selected);ut=sum(F(hits[i])/pi[i] for i in selected)
assert ue==5 and ut==3 and ut/ue==F(3,5)
out={'python':platform.python_version(),'kind':'LOCAL MATH; invented finite population, exhaustive design enumeration',
 'ownership_counts':counts,'ownership_hits':hits,'episode_boundaries':episode_rows,'samples':rows,
 'expected_total':mean(est),'true_total':sum(counts),'exact_design_variance':mean((x-mean(est))**2 for x in est),
 'overlap_inclusion_by_cores_touched':overlap,
 'ratio_counterexample':{'events':ratio_counts,'detected':ratio_hits,'true_ratio':F(3,10),'sample_ratios':ratios,'mean_ratio':mean(ratios),
 'mean_event_total_hat':mean(F(N,n)*sum(ratio_counts[i] for i in s) for s in samples),
 'mean_detected_total_hat':mean(F(N,n)*sum(ratio_hits[i] for i in s) for s in samples)},
 'zero_positive_example_probability':F(comb(3,2),comb(4,2)),
 'unequal_alert_strata':{'pi':pi,'selected':selected, 'weighted_events':ue,'weighted_detected':ut,'weighted_ratio':ut/ue,'naive_ratio':F(sum(hits[i] for i in selected),sum(counts[i] for i in selected))}}
def clean(x):
 if isinstance(x,F):return {'exact':str(x),'decimal':float(x)}
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
Path(__file__).with_name('fixtures.json').write_text(json.dumps(clean(out),indent=2),encoding='utf-8')
print(json.dumps(clean(out),indent=2))
