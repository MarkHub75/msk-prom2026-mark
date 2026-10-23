from pathlib import Path
import urllib.request, hashlib, json, datetime

root=Path(__file__).parent
sources=[
 ("W2-04-S01","scipy_matching_v1.17.1.pyx","https://raw.githubusercontent.com/scipy/scipy/v1.17.1/scipy/sparse/csgraph/_matching.pyx"),
 ("W2-04-S02","scipy_maximum_matching_1.17.0.html","https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.sparse.csgraph.maximum_bipartite_matching.html"),
 ("W2-04-S03","networkx_min_cost_flow.html","https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.min_cost_flow.html"),
]
records=[]
for sid,name,url in sources:
    r={"source_id":sid,"url":url,"access_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url,timeout=35) as response:
            data=response.read()
            r.update(status=response.status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),saved=name)
            (root/name).write_bytes(data)
    except Exception as e:r["failure"]=repr(e)
    records.append(r)
(root/"retrieval.json").write_text(json.dumps(records,indent=2),encoding="utf-8")
print(json.dumps(records,indent=2))
