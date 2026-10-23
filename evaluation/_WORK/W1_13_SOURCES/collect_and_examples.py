from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, inspect, platform, warnings
import requests
import numpy as np
import scipy
from scipy.stats import bootstrap, binomtest, chi2

root = Path(__file__).resolve().parent
urls = {
 'bootstrap-1.17.1.html': 'https://docs.scipy.org/doc/scipy-1.17.1/reference/generated/scipy.stats.bootstrap.html',
 '_resampling.py': 'https://raw.githubusercontent.com/scipy/scipy/527eb7fd7953a1de068f94bf8b322f249b9405ae/scipy/stats/_resampling.py',
 '_binomtest.py': 'https://raw.githubusercontent.com/scipy/scipy/527eb7fd7953a1de068f94bf8b322f249b9405ae/scipy/stats/_binomtest.py',
 'Cameron_Miller_JHR_2015.pdf':'https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf',
 'field2007jrssb.pdf':'https://bemlar.ism.ac.jp/zhuang/Refs/Refs/field2007jrssb.pdf',
 'cawley10a.pdf':'https://jmlr.csail.mit.edu/papers/volume11/cawley10a/cawley10a.pdf',
 '0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf':'https://proceedings.mlsys.org/paper_files/paper/2021/file/0184b0cd3cfb185989f858a1d9f5c1eb-Paper.pdf',
 'poisson.test.html':'https://stat.ethz.ch/R-manual/R-devel/library/stats/html/poisson.test.html',
 'mcnemar.html':'https://www.statsmodels.org/stable/generated/statsmodels.stats.contingency_tables.mcnemar.html',
}
manifest=[]
for filename,url in urls.items():
    try:
        r=requests.get(url, timeout=35)
        item=dict(file=filename,url=url,final_url=r.url,status=r.status_code,access_utc=datetime.now(timezone.utc).isoformat(),bytes=len(r.content))
        if r.ok:
            (root/filename).write_bytes(r.content)
            item['sha256']=hashlib.sha256(r.content).hexdigest()
    except Exception as e:
        item=dict(file=filename,url=url,error=str(e),access_utc=datetime.now(timezone.utc).isoformat())
    manifest.append(item)
(root/'retrieval.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')

out=[]
out.append(f'Python={platform.python_version()}, SciPy={scipy.__version__}, NumPy={np.__version__}')
out.append('bootstrap signature='+str(inspect.signature(bootstrap)))
for k,n in [(0,20),(20,20),(1,1),(1,5),(0,1)]:
    ci=binomtest(k,n).proportion_ci(method='exact')
    out.append(f'binomial k={k},n={n}, two-sided CP95={tuple(ci)}')
out.append('zero failures in 20 independent trials, one-sided upper95='+str(binomtest(0,20,alternative='less').proportion_ci().high))
out.append('20 successes in 20 independent trials, one-sided lower95='+str(binomtest(20,20,alternative='greater').proportion_ci().low))
for k,T in [(0,10),(1,10)]:
    lower=0.0 if k==0 else chi2.ppf(.025,2*k)/(2*T)
    upper=chi2.ppf(.975,2*(k+1))/(2*T)
    out.append(f'Poisson count={k}, exposure={T} h, two-sided95 rate={lower,upper}; zero one-sided95={-np.log(.05)/T if k==0 else None}')
with warnings.catch_warnings(record=True) as ws:
    warnings.simplefilter('always')
    z=bootstrap((np.zeros(20),),np.mean,rng=13,n_resamples=9999,method='BCa')
    out.append(f'all-zero Bernoulli BCa={z.confidence_interval},warnings={[type(w.message).__name__ for w in ws]}')
z=bootstrap((np.zeros(20),),np.mean,rng=13,n_resamples=9999,method='percentile')
out.append(f'all-zero Bernoulli percentile={z.confidence_interval}')

# Four hypothetical cameras; each camera is one row of paired sufficient counts.
# Ratio-of-sums differences estimate exposure-weighted event recall B-A.
a=np.array([9.,1.,4.,0.]); b=np.array([10.,1.,3.,1.]); n=np.array([10.,2.,5.,1.])
def delta(a,b,n,axis=-1):
    return (np.sum(b,axis=axis)-np.sum(a,axis=axis))/np.sum(n,axis=axis)
res=bootstrap((a,b,n),delta,paired=True,vectorized=True,method='percentile',rng=13,n_resamples=9999)
out.append(f'four-camera micro recall A={a.sum()/n.sum()},B={b.sum()/n.sum()},difference={delta(a,b,n)},paired cluster percentile95={res.confidence_interval}; descriptive only')
out.append(f'macro recall A={np.mean(a/n)},B={np.mean(b/n)},difference={np.mean((b-a)/n)}')
# One positive camera among four: a bootstrap sample has no positives with (3/4)^4 probability.
out.append(f'four cameras, positive in only one: probability undefined recall resample={(3/4)**4}')
# 10 independent paired GT episodes: discordant correct outcomes b=1 and c=2.
out.append(f'paired exact McNemar conditional binomial b=1,c=2,p={binomtest(1,3,.5).pvalue}')
(root/'examples.txt').write_text('\n'.join(out)+'\n',encoding='utf-8')
print('\n'.join(out))
print('Retrieval:',[(x['file'],x.get('status',x.get('error'))) for x in manifest])
