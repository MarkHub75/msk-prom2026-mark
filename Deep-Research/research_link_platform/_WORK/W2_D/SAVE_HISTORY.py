import subprocess,pathlib,json,datetime
p=pathlib.Path(__file__).parent; repo=p/'HISTORY.git'
queries={
'REFS':['show-ref'],
'MODEL_ARTIFACT_HISTORY':['log','--all','--oneline','--','experiments','models','artifacts'],
'V8_SOURCE_HISTORY':['log','--all','--format=%H %aI %s','--','scr/detection/export_yolov8s_to_onnx.py','scr/detection/build_yolov8_program.py'],
'DETECT_HISTORY':['log','--all','--format=%H %aI %s','--','scr/detection'],
'V8_INTRO':['show','--stat','f91c66b'],
'TREE':['ls-tree','-r','--name-only','main'],
'README_STATUS_HISTORY':['log','--all','-p','-G','success|valid|failed|accuracy|mAP','--','scr/detection/README.md','RUN_SCENARIO.txt'],
}
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'origin':'https://github.com/sherstpasha/linq-cv-bench.git','queries':{}}
for k,args in queries.items():
 r=subprocess.run(['git','--git-dir='+str(repo),*args],capture_output=True,encoding='utf8');out['queries'][k]={'args':args,'status':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
(p/'GIT_HISTORY_INSPECTION.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print('Saved',len(queries),'read-only history queries')
