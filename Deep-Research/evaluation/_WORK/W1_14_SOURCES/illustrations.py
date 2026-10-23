from pathlib import Path
import json
p=Path('_WORK/W1_14_SOURCES')
# Mathematical illustrations only. No model/evaluator execution.
strata=[dict(N=900,n=10,k=1),dict(N=100,n=10,k=8)]
unweighted=sum(x['k'] for x in strata)/sum(x['n'] for x in strata)
weighted=sum(x['N']*x['k']/x['n'] for x in strata)/sum(x['N'] for x in strata)
paired=dict(both_success=16,A_only=2,B_only=7,both_fail=5)
n=sum(paired.values())
a=(paired['both_success']+paired['A_only'])/n
b=(paired['both_success']+paired['B_only'])/n
# General interaction illustration; all values hypothetical success fractions.
m00,m10,m01,m11=.5,.6,.55,.8
out=dict(label='mathematical illustrations, not model tests',unweighted_sample_fraction=unweighted,weighted_population_fraction_estimate=weighted,paired=paired,n=n,A_success=a,B_success=b,paired_difference=b-a,interaction=m11-m10-m01+m00)
(p/'illustrations.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
