import json, pathlib, requests
root=pathlib.Path(__file__).parent/'A05_SOURCES'
root.mkdir(exist_ok=True)
specs={
 'openpose':('CMU-Perceptual-Computing-Lab/openpose',['README.md','LICENSE','doc/02_output.md']),
 'mmpose':('open-mmlab/mmpose',['projects/rtmpose/README.md','LICENSE','projects/rtmpose/rtmpose/rtmcc_head.py']),
 'depthv2':('DepthAnything/Depth-Anything-V2',['README.md','LICENSE','metric_depth/README.md','metric_depth/depth_anything_v2/dpt.py','depth_anything_v2/dpt.py']),
 'metric3d':('YvanYin/Metric3D',['README.md','LICENSE','mono/utils/do_test.py'])}
out={}
for label,(repo,files) in specs.items():
 r=requests.get('https://api.github.com/repos/'+repo+'/commits',params={'per_page':1},timeout=40)
 r.raise_for_status(); c=r.json()[0]; sha=c['sha']
 out[label]={'repo':repo,'sha':sha,'date':c['commit']['committer']['date'],'files':{}}
 for path in files:
  u=f'https://raw.githubusercontent.com/{repo}/{sha}/{path}'
  rr=requests.get(u,timeout=40)
  out[label]['files'][path]={'url':u,'status':rr.status_code}
  if rr.ok: (root/(label+'__'+path.replace('/','__'))).write_text(rr.text,encoding='utf-8')
(root/'METADATA.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
