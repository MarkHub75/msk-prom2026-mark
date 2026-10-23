import ast,pathlib,json,hashlib,datetime
p=pathlib.Path(__file__).parent
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[]}
for f in list(p.glob('SOURCE_*/**/*.py'))+list(p.glob('SOURCE_*/**/README.md')):
    b=f.read_bytes();t=b.decode();x={'file':str(f.relative_to(p)),'sha256':hashlib.sha256(b).hexdigest(),'lines':len(t.splitlines())}
    if f.suffix=='.py':
        try:
            tree=ast.parse(t);x['definitions']=[{'name':n.name,'start':n.lineno,'end':n.end_lineno} for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
        except Exception as e:x['parse_error']=repr(e)
    r['files'].append(x)
(p/'SOURCE_LOCATORS.json').write_text(json.dumps(r,indent=2),encoding='utf8')
