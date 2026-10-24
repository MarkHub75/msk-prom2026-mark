"""Extract existing decoded boxes and Sigmoid class probabilities before Concat."""
import copy
import json
from pathlib import Path
from .export import sha256


def export_split_detect(source_manifest, output_dir, model_id='matvey_helmet_split_v1'):
    import onnx
    source_manifest=Path(source_manifest); out=Path(output_dir)
    m=json.loads(source_manifest.read_text()); source=source_manifest.parent/m['artifacts']['onnx']['file']
    if m['decoder']!='detect_v8' or sha256(source)!=m['artifacts']['onnx']['sha256']:
        raise ValueError('verified detect_v8 source required')
    graph=onnx.shape_inference.infer_shapes(onnx.load(source))
    producers={name:n for n in graph.graph.node for name in n.output}
    final=producers[m['output_name']]
    if final.op_type!='Concat' or len(final.input)!=2 or producers[final.input[1]].op_type!='Sigmoid':
        raise ValueError('expected boxes/probability final Concat')
    axis=next(a.i for a in final.attribute if a.name=='axis')
    if axis!=1: raise ValueError('expected channel concat')
    names=dict(zip(('boxes','class_scores'),final.input))
    result=onnx.utils.Extractor(graph).extract_model([m['input']['name']],list(names.values()))
    shapes={v.name:[d.dim_value for d in v.type.tensor_type.shape.dim] for v in result.graph.output}
    if shapes[names['boxes']]!=[1,4,8400] or shapes[names['class_scores']]!=[1,len(m['classes']),8400]:
        raise ValueError('unexpected static ABI')
    if any(m['output_name'] in n.output for n in result.graph.node): raise ValueError('final concat retained')
    onnx.checker.check_model(result)
    out.mkdir(parents=True,exist_ok=False); onnx.save(result,out/'weights.onnx')
    target=copy.deepcopy(m); target.pop('output_name');target.update(model_id=model_id,decoder='split_detect_v8',
        split_outputs=names,output_shapes=shapes,source_onnx_sha256=sha256(source),
        parent_manifest_sha256=sha256(source_manifest),linq_status='NOT_RUN',
        graph_surgery={'kind':'pre_concat_output_extraction','host_operations':'concatenate only; no sigmoid or neural math',
                       'removed_node':final.name,'removed_output':m['output_name']})
    target['artifacts']['onnx']={'file':'weights.onnx','sha256':sha256(out/'weights.onnx')}
    target['artifacts']['weights']['file']=str((source_manifest.parent/m['artifacts']['weights']['file']).resolve())
    (out/'manifest.json').write_text(json.dumps(target,indent=2)+'\n')
    return out/'manifest.json'
