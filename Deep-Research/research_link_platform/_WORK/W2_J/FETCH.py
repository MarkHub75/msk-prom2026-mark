import urllib.request,json,hashlib,datetime,pathlib,tarfile,io
ROOT=pathlib.Path(__file__).parent
log=[]
def fetch(url,name):
    r={'url':url,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'name':name}
    try:
        with urllib.request.urlopen(url,timeout=25) as f:
            b=f.read();r.update(status=f.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),headers=dict(f.headers));(ROOT/name).write_bytes(b)
        return b
    except Exception as e:r['error']=repr(e)
    finally:log.append(r);(ROOT/'HTTP_LOG.json').write_text(json.dumps(log,indent=2),encoding='utf8')
for v in ['13.0.13','14.7.0']:
    b=fetch('https://pypi.org/pypi/pytpu/'+v+'/json','PYPI_'+v+'.json')
    if not b:continue
    for u in json.loads(b)['urls']:
        if u['packagetype']=='sdist':
            a=fetch(u['url'],u['filename'])
            if not a:continue
            with tarfile.open(fileobj=io.BytesIO(a),mode='r:gz') as t:
                names=[]
                for m in t.getmembers():
                    names.append(m.name)
                    if m.isfile() and m.name.endswith(('.py','.h','.hpp','.md')):
                        p=ROOT/('SOURCE_'+v)/m.name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(t.extractfile(m).read())
                (ROOT/('TREE_'+v+'.json')).write_text(json.dumps(names,indent=2),encoding='utf8')
for url,name in [('https://lin-q.ru/docs','DOCS.html'),('https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf','linq_hps_datasheet.pdf')]:fetch(url,name)
