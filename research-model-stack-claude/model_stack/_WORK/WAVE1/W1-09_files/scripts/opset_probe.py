import onnx, onnxruntime as ort
from onnx import helper, TensorProto
for op in (17,18,19,20,21,22,23,24,25,26,27,28):
    for ir in (8,10,11,12,13,14):
        try:
            x=helper.make_tensor_value_info('x',TensorProto.FLOAT,[1,3]); y=helper.make_tensor_value_info('y',TensorProto.FLOAT,[1,3])
            g=helper.make_graph([helper.make_node('Relu',['x'],['y'])],'g',[x],[y])
            m=helper.make_model(g,opset_imports=[helper.make_opsetid('',op)],ir_version=ir)
            ort.InferenceSession(m.SerializeToString(),providers=['CPUExecutionProvider'])
            r='ok'
        except Exception as e:
            r='FAIL '+str(e)[:90].replace('\n',' ')
        if ir in (8,10,14) or r!='ok': print(op,ir,r)
