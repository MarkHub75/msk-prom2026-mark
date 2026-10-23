import urllib.request, json, hashlib, datetime
from pathlib import Path
root = Path(__file__).parent
items = [
 ('scipy_binomtest.py','https://raw.githubusercontent.com/scipy/scipy/527eb7fd7953a1de068f94bf8b322f249b9405ae/scipy/stats/_binomtest.py'),
 ('scipy_ci_live.html','https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats._result_classes.BinomTestResult.proportion_ci.html'),
 ('nist_zero.html','https://www.itl.nist.gov/div898/handbook/apr/section4/apr451.htm'),
 ('nist_poisson.html','https://www.itl.nist.gov/div898/handbook/eda/section3/eda366j.htm'),
 ('cameron_miller_2015.pdf','https://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015.pdf')]
records=[]
for name,url in items:
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(url,timeout=45) as r:
            data=r.read(); status=r.status; final=r.url
        (root/name).write_bytes(data)
        records.append(dict(file=name,url=url,final_url=final,status=status,accessed_at=t,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    except Exception as e:
        records.append(dict(file=name,url=url,accessed_at=t,error=str(e)))
(root/'retrieval.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records,indent=2))
