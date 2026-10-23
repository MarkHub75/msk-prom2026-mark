import torch, torch.nn as nn, warnings, onnx, onnxruntime as ort, numpy as np
warnings.filterwarnings("ignore")
m=nn.Sequential(nn.Conv2d(3,8,3,padding=1),nn.SiLU(),nn.Upsample(scale_factor=2)).eval()
x=torch.randn(1,3,64,64)
def info(f):
    p=onnx.load(f); print("  ir",p.ir_version,"opsets",[(o.domain,o.version) for o in p.opset_import],"ops",sorted({n.op_type for n in p.graph.node}), "producer",p.producer_name,p.producer_version)
    s=ort.InferenceSession(f,providers=["CPUExecutionProvider"]); y=s.run(None,{s.get_inputs()[0].name:x.numpy()})[0]
    print("  ort max abs diff", float(np.abs(y-m(x).detach().numpy()).max()))
for name,kw in [("default dynamo=True",{}),("dynamo=False op17",{"dynamo":False,"opset_version":17}),("dynamo=False op21",{"dynamo":False,"opset_version":21}),("dynamo=True op17",{"dynamo":True,"opset_version":17}),("dynamo=True op23",{"dynamo":True,"opset_version":23})]:
    try:
        torch.onnx.export(m,x,"t.onnx",**kw); print(name,"OK"); info("t.onnx")
    except Exception as e:
        print(name,"FAIL",type(e).__name__,str(e)[:200].replace("\n"," "))
