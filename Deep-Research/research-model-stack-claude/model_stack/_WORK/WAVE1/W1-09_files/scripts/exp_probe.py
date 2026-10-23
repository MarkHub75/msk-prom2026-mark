import torch, torch.nn as nn, warnings, traceback
warnings.filterwarnings("ignore")
m=nn.Sequential(nn.Conv2d(3,8,3,padding=1),nn.SiLU(),nn.Upsample(scale_factor=2)).eval()
x=torch.randn(1,3,64,64)
for name,kw in [("default(dynamo=True), no opset",{}),("dynamo=False opset17",{"dynamo":False,"opset_version":17}),("dynamo=False opset 18",{"dynamo":False,"opset_version":18}),("dynamo=False opset 20",{"dynamo":False,"opset_version":20}),("dynamo=False opset 21",{"dynamo":False,"opset_version":21})]:
    try:
        torch.onnx.export(m,x,"t.onnx",**kw); print(name,"OK")
    except Exception as e:
        print(name,"FAIL",type(e).__name__,str(e)[:200].replace("\n"," "))
