exec(open(__file__.replace('source_checks.py','check.py'),encoding='utf-8').read().split("base='https://download")[0])
log=json.loads((P/'ACCESS.json').read_text())
items=[
 ('https://raw.githubusercontent.com/open-mmlab/mmdeploy/v1.2.0/csrc/mmdeploy/codebase/mmpose/simcc_label.cpp','mmdeploy_simcc_label.cpp'),
 ('https://raw.githubusercontent.com/open-mmlab/mmdeploy/v1.2.0/csrc/mmdeploy/codebase/mmpose/topdown_affine.cpp','mmdeploy_topdown_affine.cpp'),
 ('https://raw.githubusercontent.com/open-mmlab/mmdeploy/v1.2.0/csrc/mmdeploy/codebase/mmpose/topdown_get_bbox_center_scale.cpp','mmdeploy_bbox.cpp'),
 ('https://raw.githubusercontent.com/open-mmlab/mmdeploy/v1.2.0/LICENSE','MMDeploy_LICENSE'),
 ('https://raw.githubusercontent.com/open-mmlab/mmdeploy/v1.2.0/NOTICE','MMDeploy_NOTICE'),
 ('https://raw.githubusercontent.com/open-mmlab/mmpose/v1.1.0/projects/rtmpose/rtmpose/body_2d_keypoint/rtmpose-m_8xb256-420e_coco-256x192.py','pose_config_v1.1.0.py'),
 ('https://api.github.com/repos/open-mmlab/mmpose/git/trees/'+REV+'?recursive=1','mmpose_tree.json'),
 ('https://api.github.com/repos/open-mmlab/mmdeploy/git/ref/tags/v1.2.0','mmdeploy_tag.json'),
 ('https://api.github.com/repos/open-mmlab/mmpose/git/ref/tags/v1.1.0','mmpose_tag.json'),
 ]
for url,name in items:
 try: get(url,name,7000000)
 except Exception as e: print(name,str(e))
urls=[('https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmdet_nano_8xb32-100e_coco-obj365-person-05d8511e.pth','detector_pth'),('https://download.openmmlab.com/mmpose/v1/projects/rtmposev1/rtmpose-m_simcc-body7_pt-body7_420e-256x192-e48f03d0_20230504.pth','body7_pth'),('https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmpose-cpu.zip','recipe_cpu_bundle')]
for url,name in urls:
 r=requests.head(url,timeout=(15,30),allow_redirects=True)
 log.append(dict(url=url,name=name,method='HEAD',status=r.status_code,headers=dict(r.headers),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
(P/'ACCESS.json').write_text(json.dumps(log,indent=2))
print([(x['name'],x['status'],x.get('bytes',x['headers'].get('Content-Length'))) for x in log])
