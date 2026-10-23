import onnx,pathlib,json,collections,hashlib
P=pathlib.Path(__file__).parent
path=next((P/'extracted').rglob('end2end.onnx'))
m=onnx.load(str(path),load_external_data=False)
def shape(x):
 t=x.type.tensor_type
 return dict(name=x.name,dtype=onnx.TensorProto.DataType.Name(t.elem_type),shape=[d.dim_param if d.dim_param else d.dim_value for d in t.shape.dim])
summary=dict(ir_version=m.ir_version,producer_name=m.producer_name,producer_version=m.producer_version,opset=[dict(domain=o.domain,version=o.version) for o in m.opset_import],inputs=[shape(x) for x in m.graph.input],outputs=[shape(x) for x in m.graph.output],node_count=len(m.graph.node),operators=dict(collections.Counter((n.domain+':'+n.op_type) for n in m.graph.node)),initializer_count=len(m.graph.initializer),initializer_dtypes=dict(collections.Counter(onnx.TensorProto.DataType.Name(t.data_type) for t in m.graph.initializer)),external_initializers=[dict(name=t.name,external=[dict(key=x.key,value=x.value) for x in t.external_data]) for t in m.graph.initializer if t.external_data],metadata=[dict(key=x.key,value=x.value) for x in m.metadata_props],tail=[dict(name=n.name,op=n.op_type,input=list(n.input),output=list(n.output)) for n in m.graph.node[-20:]])
onnx.checker.check_model(m)
summary['checker']='onnx.checker.check_model passed; static protobuf/schema check only'
(P/'GRAPH.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
