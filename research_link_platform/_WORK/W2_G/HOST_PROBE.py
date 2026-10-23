"""Historical Python-only probes. CDLL is replaced before source execution. No native runtime."""
import ctypes, datetime, gc, json, pathlib, platform, types, weakref
import numpy as np
root=pathlib.Path(__file__).parent
source=root.parent/'W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu/_bindings.py'
ns={'__name__':'historical_bindings_probe'}
original=ctypes.CDLL
def forbidden(*a,**k): raise AssertionError('native library loading forbidden')
ctypes.CDLL=forbidden
try: exec(compile(source.read_text(encoding='utf8'),str(source),'exec'),ns)
finally: ctypes.CDLL=original
class Fake:
 def __init__(self): self.calls=[]
 def __getattr__(self,name):
  def call(*args):
   self.calls.append(name)
   if name=='tpu_is_device_valid': return 1
   return 0
  return call
fake=Fake(); ns['_LIB_TPU_BINDER']=types.SimpleNamespace(libtpu=fake)
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':platform.python_version(),'numpy':np.__version__,'native_loaded':False}
for kind in ['normal','exception']:
 fake.calls.clear()
 try:
  with ns['Device'].open('/not/a/device'):
   if kind=='exception': raise RuntimeError('injected host exception')
 except RuntimeError: pass
 out['device_context_'+kind]=list(fake.calls)
# Real historical output allocation and decoding methods, fake pointer-registration only.
program=types.SimpleNamespace(_pointer=0,_output_metadata={'output':{'user_dtype':'float32','user_shape':[2]}},_hardware_parameters_metadata={},_is_raw=False)
obj=ns['Inference'].__new__(ns['Inference']); obj._program=program; obj._pointer=0
obj._tensor_name_to_tensor_index={'input':0,'output':0}; obj._tensor_name_to_tensor_size={'input':8,'output':8}
buf=types.SimpleNamespace(_pointer=0,set_user_tensor_buffer_ptr=lambda *args:None)
inp=np.array([3,4],dtype='float32')
ctx=obj._load_inference(buf,buf,{'input':inp})
ptr=ctx['output']; floats=ctypes.cast(ptr,ctypes.POINTER(ctypes.c_float)); floats[0]=1.25; floats[1]=-2.5
arr=obj._get_inference(ctx)['output']; reference=weakref.ref(ptr)
floats[0]=7.5
out['output_is_view_mutation_visible']=arr.tolist()==[7.5,-2.5]
floats[0]=1.25
base_chain=[]; base=arr
while base is not None:
 base_chain.append(type(base).__name__); base=getattr(base,'base',None)
del ctx, ptr, floats; gc.collect()
out['output_lifetime']={'values_after_ctx_gc':arr.tolist(),'owns_data':bool(arr.flags.owndata),'base_chain':base_chain,'original_pointer_alive':reference() is not None}
try: obj._load_inference(buf,buf,[inp])
except Exception as e: out['non_mapping']=type(e).__name__+': '+str(e)
for label,value in [('wrong_dtype',np.array([1,2],dtype='float64')),('non_contiguous',np.arange(4,dtype='float32')[::2]),('missing_input',None)]:
 try:
  obj._load_inference(buf,buf,{} if value is None else {'input':value}); out[label]='accepted by historical Python method with fake native registration'
 except Exception as e: out[label]=repr(e)
try: obj._load_inference(buf,buf,{'unknown':inp})
except Exception as e: out['unknown_name']=repr(e)
(root/'HOST_PROBE_RESULT.json').write_text(json.dumps(out,indent=2),encoding='utf8'); print(json.dumps(out,indent=2))
