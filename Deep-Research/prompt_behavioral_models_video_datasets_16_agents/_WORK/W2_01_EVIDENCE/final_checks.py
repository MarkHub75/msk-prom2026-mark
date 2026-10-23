exec(open(__file__.replace('final_checks.py','check.py'),encoding='utf-8').read().split("base='https://download")[0])
log=json.loads((P/'ACCESS.json').read_text())
get('https://download.openmmlab.com/mmpose/v1/projects/rtmpose/rtmdet_nano_8xb32-100e_coco-obj365-person-05d8511e.pth','detector_05d8511e.pth',5000000)
get('https://raw.githubusercontent.com/open-mmlab/mmpose/'+REV+'/LICENSES.md','MMPose_LICENSES.md',100000)
get('https://raw.githubusercontent.com/open-mmlab/mmdeploy/6cd29e2152d6935bde2f9252b47170724bac20ac/csrc/mmdeploy/codebase/mmpose/simcc_label.cpp','mmdeploy_simcc_commit.cpp',100000)
import onnx
path=next((P/'extracted').rglob('end2end.onnx')); m=onnx.load(str(path),load_external_data=False)
head=[dict(name=x.name,dims=list(x.dims)) for x in m.graph.initializer if 'head' in x.name]
(P/'POSE_HEAD_DIMS.json').write_text(json.dumps(head,indent=2))
print('done')
