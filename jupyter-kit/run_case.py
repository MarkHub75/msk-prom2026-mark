"""Prepare or capture Helmet first, then Split-Pose through the explicit binding."""
import argparse
import json
from pathlib import Path
from ml.linq.jupyter import prepare_case, capture_case


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name',choices=['helmet','pose-split'])
    parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--output-dir')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    case=prepare_case(root,args.name)
    if args.prepare_only:
        print(json.dumps({'model_id':case['model_id'],'program_sha256':case['compile_report']['program_sha256'],
                          'input_specs':case['input_specs'],'output_specs':case['output_specs'],
                          'runtime_abi_verified':False}))
        return
    import bindings
    if bindings.BINDING_READY is not True:
        parser.error('Actual example.ipynb service binding is not configured; no inference was attempted')
    if not args.output_dir:
        parser.error('--output-dir must name a new capture directory')
    run=bindings.make_runner(case['program_path'],list(case['input_specs']),list(case['output_specs']))
    result=capture_case(root,args.name,run,args.output_dir,diagnostic_only=True,placement_attested=True)
    print(json.dumps({'status':result['status'],'call_completed':result['call_completed']}))
    if result['status']!='completed':raise SystemExit(2)

if __name__=='__main__':main()
