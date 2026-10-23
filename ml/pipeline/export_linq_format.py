"""Export ONLY the exact installed official format package from LinQ Jupyter.

Standalone script: standard library only. No Conda export, credentials, notebook
cells, pip indexes, broker calls or environment dumps. Run on LinQ only when
organizers permit transferring this client library to the team's Vast instance.
"""
import argparse
import hashlib
import importlib
import importlib.metadata as metadata
import importlib.util
import inspect
import json
from pathlib import Path
import platform
import re
import sys
import zipfile

MODULE = 'tpu_pycloud_format'
VERSION = '0.0.1'


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _signature(value):
    try:
        return [{'name':p.name,'kind':str(p.kind),'required':p.default is inspect.Parameter.empty}
                for p in inspect.signature(value).parameters.values()]
    except (ValueError,TypeError):
        return None


def export_package(output, *, authorized_by_organizers=False,
                   expected_site='/opt/conda/lib/python3.11/site-packages'):
    if authorized_by_organizers is not True:
        raise PermissionError('organizer permission is required before exporting this client package')
    spec=importlib.util.find_spec(MODULE)
    if spec is None or not spec.origin:
        raise ModuleNotFoundError('exact official format module is unavailable in this kernel')
    origin=Path(spec.origin).resolve()
    site=Path(expected_site).resolve()
    if not origin.is_relative_to(site) or not origin.is_file():
        raise ValueError('module source does not match the expected installed LinQ location')
    dist=metadata.distribution(MODULE)
    if dist.version!=VERSION:
        raise ValueError('exact official version 0.0.1 is required')
    package=importlib.import_module(MODULE)
    symbols={name:getattr(package,name) for name in ('PyTask','serialize','deserialize')}
    if not all(callable(value) for value in symbols.values()):
        raise ValueError('official module does not expose the required callable API')
    payload={}
    if spec.submodule_search_locations:
        root=origin.parent
        for path in sorted(root.rglob('*')):
            if not path.is_file() or '__pycache__' in path.parts or any(part.startswith('.') for part in path.relative_to(root).parts):
                continue
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError('linked/external package member cannot be exported')
            if path.suffix not in ('.py','.pyi','.so','.pyd','.proto','.typed') and path.name!='py.typed':
                continue
            payload[MODULE+'/'+path.relative_to(root).as_posix()]=path.read_bytes()
    else:
        if origin.suffix not in ('.py','.so','.pyd'):
            raise ValueError('unsupported installed module format; request the official wheel')
        payload[origin.name]=origin.read_bytes()
    if not payload:
        raise ValueError('no package code was collected')
    # Only normalized dependency names and installed versions; never include
    # direct URLs, pip config, private index credentials, or arbitrary metadata.
    dependencies={}
    requires=[]
    for requirement in dist.requires or []:
        match=re.match(r'\s*([A-Za-z0-9][A-Za-z0-9_.-]*)',requirement)
        if not match:
            raise ValueError('unsupported dependency declaration')
        name=match.group(1)
        try:
            version=metadata.version(name)
        except metadata.PackageNotFoundError:
            version=None
        dependencies[name]=version
        if version and re.fullmatch(r'[A-Za-z0-9_.+!-]+',version):
            requires.append(f'Requires-Dist: {name}=={version}')
    clean_metadata='\n'.join(['Metadata-Version: 2.1','Name: tpu-pycloud-format',f'Version: {VERSION}',*requires,'',''])
    prefix=f'{MODULE}-{VERSION}.dist-info/'
    payload[prefix+'METADATA']=clean_metadata.encode()
    payload[prefix+'top_level.txt']=(MODULE+'\n').encode()
    report={
        'module':MODULE,'version':VERSION,'source':'organizer-installed LinQ client package',
        'source_python':platform.python_version(),'source_machine':platform.machine(),
        'source_platform':sys.platform,
        'pure_python':not any(name.endswith(('.so','.pyd')) for name in payload),
        'dependencies':dependencies,
        'api':{name:_signature(value) for name,value in symbols.items()},
        'format_only':True,'notebook_or_credentials_exported':False,
        'files':{name:{'sha256':_sha(body),'bytes':len(body)} for name,body in payload.items()},
    }
    payload['SOURCE.json']=(json.dumps(report,indent=2)+'\n').encode()
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,body in payload.items():archive.writestr(name,body)
    return {'status':'EXPORTED','archive':output.name,'sha256':_sha(output.read_bytes()),
            'module':MODULE,'version':VERSION,'source_python':report['source_python'],
            'pure_python':report['pure_python'],'api':report['api']}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='tpu_pycloud_format-0.0.1-linq-client.zip')
    parser.add_argument('--authorized-by-organizers',action='store_true')
    parser.add_argument('--expected-site',default='/opt/conda/lib/python3.11/site-packages')
    args=parser.parse_args()
    try:
        result=export_package(args.output,authorized_by_organizers=args.authorized_by_organizers,expected_site=args.expected_site)
    except Exception as exc:
        print(json.dumps({'status':'NOT_EXPORTED','error_type':type(exc).__name__}))
        raise SystemExit(2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
