import configparser,io,pathlib,json,hashlib
import numpy as np
import ONNX_ML_PB2 as pb
P=pathlib.Path(__file__).parent
m=pb.ModelProto();m.ParseFromString((P/'tiny-yolov3-11.onnx').read_bytes())
def arr(t):
 dt={1:'<f4',6:'<i4',7:'<i8',9:'?',11:'<f8'}[t.data_type]
 return (np.frombuffer(t.raw_data,dtype=dt) if t.raw_data else np.array(t.float_data or t.int64_data or t.int32_data,dtype=dt)).reshape(t.dims)
initial={t.name:arr(t) for t in m.graph.initializer}
text=(P/'yolov3-tiny.cfg').read_text(); count={};lines=[]
for line in text.splitlines():
 if line.startswith('['):
  name=line.strip('[]');count[name]=count.get(name,0)+1;line=f'[{name}_{count[name]}]'
 lines.append(line)
c=configparser.ConfigParser();c.read_string('\n'.join(lines))
layers=[]; results=[];f=(P/'yolov3-tiny.weights').open('rb'); header=np.frombuffer(f.read(20),dtype='<i4').tolist();prev=3;idx=0
for section in c.sections():
 d=c[section]
 if section.startswith('convolutional'):
  idx+=1;n=int(d['filters']);size=int(d['size']);bias=np.frombuffer(f.read(n*4),dtype='<f4');bn=None
  if 'batch_normalize' in d:bn=np.frombuffer(f.read(n*12),dtype='<f4').reshape(3,n)
  kernel=np.frombuffer(f.read(n*prev*size*size*4),dtype='<f4').reshape(n,prev,size,size)
  candidate=initial[f'conv2d_{idx}/kernel:0'];r={'conv':idx,'shape':list(kernel.shape),'kernel_exact':bool(np.array_equal(kernel,candidate)),'kernel_max_abs':float(np.max(np.abs(kernel-candidate)))}
  if bn is None:r['bias_exact']=bool(np.array_equal(bias,initial[f'conv2d_{idx}/bias:0']))
  else:
   bnode=next(n for n in m.graph.node if n.op_type=='BatchNormalization' and n.input[0]==next(n for n in m.graph.node if n.name==f'conv2d_{idx}').output[0])
   scale,offset,mean,var=[initial[k] for k in bnode.input[1:]]
   # Historical Keras converter seems to pre-normalize BN state. Compare effective affine maps.
   a=bn[0]/np.sqrt(bn[2]+.001);b=bias-bn[1]*a
   a2=scale/np.sqrt(var+1e-6);b2=offset-mean*a2
   r.update(bn_mean_all_zero=bool(np.all(mean==0)),bn_var_all_one=bool(np.all(var==1)),affine_scale_max_abs=float(np.max(abs(a-a2))),affine_offset_max_abs=float(np.max(abs(b-b2))),darknet_bn_epsilon='.001 hypothesis',gamma_sample=bn[0][:3].tolist(),onnx_scale_sample=scale[:3].tolist())
  results.append(r);prev=n;layers.append(prev)
 elif section.startswith('route'):
  prev=sum(layers[int(x)] for x in d['layers'].split(','));layers.append(prev)
 elif not section.startswith('net'):layers.append(prev)
out={'header_int32':header,'bytes_consumed':f.tell(),'file_size':(P/'yolov3-tiny.weights').stat().st_size,'layers':results}
(P/'PARAMETER_COMPARISON.JSON').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
