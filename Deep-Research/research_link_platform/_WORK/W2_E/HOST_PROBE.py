import pathlib,json,hashlib,datetime
import numpy as np,onnxruntime as ort
import ONNX_ML_PB2 as pb
P=pathlib.Path(__file__).parent
m=pb.ModelProto();m.ParseFromString((P/'tiny-yolov3-11.onnx').read_bytes())
opts=ort.SessionOptions();opts.intra_op_num_threads=2;opts.inter_op_num_threads=1
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'onnxruntime':ort.__version__,'provider':'CPUExecutionProvider','tests':[]}
session=ort.InferenceSession(m.SerializeToString(),sess_options=opts,providers=['CPUExecutionProvider'])
for b in [1,2]:
 try:
  x=np.zeros((b,3,416,416),dtype=np.float32);x[:,0,:,:]=.25;x[:,1,:,:]=.5;x[:,2,:,:]=.75
  shape=np.tile(np.array([[321,641]],np.float32),(b,1));out=session.run(None,{'input_1':x,'image_shape':shape})
  r['tests'].append({'batch':b,'status':'success','outputs':[{'name':o.name,'shape':list(v.shape),'dtype':str(v.dtype)} for o,v in zip(session.get_outputs(),out)]})
 except Exception as e:r['tests'].append({'batch':b,'status':'error','error':str(e)})
# Head-only diagnostic derivative; not the original model, not an SDK/device test.
needed={'convolution_output1','convolution_output'};keep=[]
for n in reversed(m.graph.node):
 if any(o in needed for o in n.output):keep.append(n);needed.update(n.input)
del m.graph.node[:];m.graph.node.extend(reversed(keep));del m.graph.output[:]
for name,grid in [('convolution_output1',13),('convolution_output',26)]:
 v=m.graph.output.add();v.name=name;v.type.tensor_type.elem_type=1
 for size in [1,255,grid,grid]:v.type.tensor_type.shape.dim.add().dim_value=size
del m.graph.input[1:]
used={i for n in m.graph.node for i in n.input};initial=[i for i in m.graph.initializer if i.name in used];del m.graph.initializer[:];m.graph.initializer.extend(initial)
heads=ort.InferenceSession(m.SerializeToString(),sess_options=opts,providers=['CPUExecutionProvider'])
x=np.zeros((1,3,416,416),np.float32);x[:,0]=.25;x[:,1]=.5;x[:,2]=.75
o=heads.run(None,{'input_1':x})
with (P/'GOLDEN_SYNTHETIC_RAW.NPZ').open('wb') as golden:
 np.savez(golden,input_nchw=x,coarse_nchw=o[0],fine_nchw=o[1])
r['head_probe']={'model':'in-memory head-only derivative of pinned ONNX','input':'constant RGB .25,.5,.75; no resize','sha256_input':hashlib.sha256(x.tobytes()).hexdigest(),'heads':[{'shape':list(a.shape),'finite':bool(np.all(np.isfinite(a))),'sha256':hashlib.sha256(a.tobytes()).hexdigest(),'min':float(a.min()),'max':float(a.max())} for a in o]}
(P/'HOST_PROBE_RESULT.JSON').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
