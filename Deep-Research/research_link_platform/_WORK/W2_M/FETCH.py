from pathlib import Path
import urllib.request, json, datetime, hashlib, tarfile, io
OUT=Path(__file__).parent
logs=[]
for url,name in [('https://pypi.org/pypi/pytpu/json','PYPI_CURRENT.json'),('http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk','LEGACY_HOME.html'),('https://lin-q.ru/docs','DOCS_DIRECT.html')]:
    row={'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':name}
    try:
        with urllib.request.urlopen(url,timeout=20) as r:
            b=r.read();row.update(status=r.status,final_url=r.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest());(OUT/name).write_bytes(b)
    except Exception as e:row.update(error=repr(e))
    logs.append(row)
j=json.loads((OUT/'PYPI_CURRENT.json').read_text('utf8'))
u=j['releases']['14.7.0'][0]
row={'url':u['url'],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':u['filename'],'expected_sha256':u['digests']['sha256']}
try:
    with urllib.request.urlopen(u['url'],timeout=20) as r:b=r.read();row.update(status=r.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest());(OUT/u['filename']).write_bytes(b)
    with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz') as t:
        names=t.getnames()
        snippets={n:t.extractfile(n).read().decode('utf8') for n in names if n.endswith(('tools/get_fps.py','pytpu/libtpu_bindings.py'))}
    (OUT/'SOURCE_14_7_0.json').write_text(json.dumps(snippets,ensure_ascii=False,indent=2),encoding='utf8')
except Exception as e:row.update(error=repr(e))
logs.append(row)
(OUT/'HTTP_LOG.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(logs,ensure_ascii=False,indent=2))
