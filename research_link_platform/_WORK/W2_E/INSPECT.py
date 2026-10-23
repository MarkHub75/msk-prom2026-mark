import pathlib,json,collections,numpy as np
import ONNX_ML_PB2 as pb
P=pathlib.Path(__file__).parent
m=pb.ModelProto(); m.ParseFromString((P/'tiny-yolov3-11.onnx').read_bytes())
def arr(t):
 dt={1:'<f4',6:'<i4',7:'<i8',9:'?',11:'<f8'}[t.data_type]
 a=np.frombuffer(t.raw_data,dtype=dt) if t.raw_data else np.array(t.float_data or t.int64_data or t.int32_data,dtype=dt)
 return a.reshape(list(t.dims))
def info(v):return {'name':v.name,'dtype':v.type.tensor_type.elem_type,'shape':[d.dim_value if d.HasField('dim_value') else d.dim_param for d in v.type.tensor_type.shape.dim]}
initial={t.name:arr(t) for t in m.graph.initializer}
def node(n):
 return {'name':n.name,'op':n.op_type,'inputs':list(n.input),'outputs':list(n.output),'attributes':{a.name:(arr(a.t).tolist() if a.type==4 else list(a.ints) if a.type==7 else a.i if a.type==2 else a.f if a.type==1 else a.s.decode(errors='replace') if a.type==3 else str(a)) for a in n.attribute}}
r={'ir':m.ir_version,'producer':m.producer_name,'producer_version':m.producer_version,'opsets':[(x.domain,x.version) for x in m.opset_import], 'inputs':[info(x) for x in m.graph.input],'outputs':[info(x) for x in m.graph.output],'ops':dict(collections.Counter(x.op_type for x in m.graph.node)),'initializers':[{'name':k,'shape':list(v.shape),'sample':v.reshape(-1)[:8].tolist()} for k,v in initial.items()], 'nodes':[node(n) for n in m.graph.node]}
(P/'GRAPH.JSON').write_text(json.dumps(r,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in r.items() if k not in ['nodes','initializers']},indent=2))
print('CONV',json.dumps([node(n) for n in m.graph.node if n.op_type in ['Conv','BatchNormalization','NonMaxSuppression']],indent=2))
print('SMALL FLOATS',json.dumps({k:v.tolist() for k,v in initial.items() if v.size<20 and v.dtype.kind=='f'},indent=2))
