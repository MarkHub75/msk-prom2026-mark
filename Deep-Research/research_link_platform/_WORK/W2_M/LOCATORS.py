from pathlib import Path
import json, hashlib, datetime
ROOT=Path(__file__).resolve().parents[1]
items=[('W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu_tests/unit/test_parallel.py',[(1,22),(33,42),(64,96),(99,151)]),('W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu/_bindings.py',[(185,253),(302,322),(373,425)]),('W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu_tests/unit/test_watchdog_error.py',[(1,40)]),('W2_J/SOURCE_14.7.0/pytpu-14.7.0/pytpu/tools/get_fps.py',[(27,42),(102,126)]),('W2_J/SOURCE_14.7.0/pytpu-14.7.0/pytpu/pytpu/libtpu_bindings.py',[(179,212),(236,239)]),('W1_06/linq-cv-bench/scr/classification/run_resnet50_parallel_direct.py',[(201,259)])]
out=[]
for rel,ranges in items:
 p=ROOT/rel;b=p.read_bytes();lines=b.decode('utf8').splitlines()
 out.append({'path':rel,'sha256':hashlib.sha256(b).hexdigest(),'total_lines':len(lines),'read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excerpts':[{'start':a,'end':min(z,len(lines)),'lines':[f'{i}: {lines[i-1]}' for i in range(a,min(z,len(lines))+1)]} for a,z in ranges]})
(Path(__file__).parent/'SOURCE_LOCATORS.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved',len(out),'source files; no source module imported, no SDK/native/device invocation')
