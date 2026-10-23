import torch, torch.nn as nn, time
print(torch.__version__, torch.version.cuda, torch.cuda.is_available(), torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))
print("arch_list", torch.cuda.get_arch_list())
m=nn.Sequential(nn.Conv2d(3,64,3,padding=1),nn.SiLU(),nn.Conv2d(64,64,3,padding=1)).cuda().half().eval()
x=torch.randn(8,3,640,640,device="cuda",dtype=torch.float16)
with torch.no_grad():
    y=m(x); torch.cuda.synchronize()
    t=time.time()
    for _ in range(20): y=m(x)
    torch.cuda.synchronize(); print("20 fwd fp16 conv ok", round(time.time()-t,3),"s", y.shape, bool(torch.isfinite(y).all()))
a=torch.randn(2048,2048,device="cuda"); print("matmul ok", float((a@a).abs().mean()))
print("cudnn", torch.backends.cudnn.version())
