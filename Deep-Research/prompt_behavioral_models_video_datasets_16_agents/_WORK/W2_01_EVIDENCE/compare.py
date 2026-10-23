import pathlib,json,onnx,hashlib,collections
P=pathlib.Path(__file__).parent
def contract(p):
 m=onnx.load(str(p),load_external_data=False);onnx.checker.check_model(m)
 def io(x):return dict(name=x.name,dtype=onnx.TensorProto.DataType.Name(x.type.tensor_type.elem_type),shape=[d.dim_param or d.dim_value for d in x.type.tensor_type.shape.dim])
 return dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),ir=m.ir_version,opsets=[dict(domain=x.domain,version=x.version) for x in m.opset_import],input=[io(x) for x in m.graph.input],output=[io(x) for x in m.graph.output],nodes=len(m.graph.node),operators=dict(collections.Counter(n.domain+':'+n.op_type for n in m.graph.node)),external=[x.name for x in m.graph.initializer if x.external_data],checker='pass, static only')
det=contract(P/'cpu_selected/rtmpose-ort/rtmdet-nano/end2end.onnx')
tiny=contract(pathlib.Path('../prompt_behavioral_safety_feasibility_16_agents/_WORK/W2-02_evidence/rtmpose-t.onnx'))
(P/'DETECTOR_GRAPH.json').write_text(json.dumps(det,indent=2))
(P/'TINY_EXISTING_GRAPH_REPARSE.json').write_text(json.dumps(tiny,indent=2))
manifest=[dict(name=str(p.relative_to(P/'cpu_selected')),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (P/'cpu_selected').rglob('*') if p.is_file()]
(P/'CPU_SELECTED_HASHES.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(dict(detector=det,tiny=tiny),indent=2))
