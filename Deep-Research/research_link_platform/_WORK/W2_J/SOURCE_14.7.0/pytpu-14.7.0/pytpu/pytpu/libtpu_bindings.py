from ctypes import (CDLL, pointer, c_char, c_char_p, c_int, c_void_p, c_uint32, c_uint8, c_size_t, c_bool, cast, POINTER, CFUNCTYPE, Structure, py_object, addressof)
from enum import Enum
import asyncio
import numpy as np

from ..tools.helpers import input_metadata
from ..tools.helpers import output_metadata
from ..tools.helpers import convert_from_uint8_to_user_dtype


libtpu = CDLL('/usr/lib/libtpu.2.so')
# libtpu = CDLL('libtpu-experimental/build/libtpu.so')
# libtpu = CDLL('/home/d.baburin/iva_tpu_sdk/libtpu.2/build/libtpu.2.so')

__all__ = [
    'TPUDevice',
    'TPUProgram',
    'TPUTensorBufferObject',
    'TPUInference',
    'kPreprocess',
    'kPostprocess',
    'TPUProcessingMode',
    'TPUTensorBufferType',
    'TPUInferenceStatus',
    'load_inference',
    'get_inference',
    'submit_inference',
]



class TPUDevice(Structure):

    _fields_ = []

    def __init__(self, dev_name):
        # self.pointer = libtpu.tpu_create_device(c_int(dev_no))
        self.pointer = libtpu.tpu_create_device(c_char_p(dev_name))

    def __del__(self):
        return libtpu.tpu_destroy_device(self.pointer)

    def is_valid(self):
        return libtpu.tpu_is_device_valid(self.pointer)

    def init(self):
        return libtpu.tpu_init_device(self.pointer)

    def get_error(self):
        return libtpu.tpu_get_device_error_message(self.pointer)

    def info(self):
        return libtpu.tpu_get_device_info(self.pointer)

    def load_program(self, program):
        return libtpu.tpu_load_program(self.pointer, program.pointer)

    def run_inference(self, inference, mode):
        return libtpu.tpu_run_inference(self.pointer, inference.pointer, mode)

    def submit_inference(self, inference, mode, callback_fn, context):
        return libtpu.tpu_submit_inference(self.pointer, inference.pointer, mode, callback_fn, context)


class TPUProgram(Structure):

    _fields_ = []

    def __init__(self, program_path):
        self.pointer = libtpu.tpu_create_program(c_char_p(program_path))

    def __del__(self):
        return libtpu.tpu_destroy_program(self.pointer)

    def is_valid(self):
        return libtpu.tpu_is_program_valid(self.pointer)

    def info(self):
        return libtpu.tpu_get_program_info(self.pointer)

    def get_error(self):
        return libtpu.tpu_get_program_error_message(self.pointer)

    def get_batch_size(self):
        return libtpu.tpu_get_batch_size(self.pointer)

    def get_input_count(self):
        return libtpu.tpu_get_input_count(self.pointer)

    def get_input_size(self, n, raw):
        return libtpu.tpu_get_input_size(self.pointer, c_size_t(n), c_bool(raw))

    def get_output_count(self):
        return libtpu.tpu_get_output_count(self.pointer)

    def get_output_size(self, n, raw):
        return libtpu.tpu_get_output_size(self.pointer, c_size_t(n), c_bool(raw))


class TPUTensorBufferObject(Structure):

    _fields_ = []

    def __init__(self, prog, Type):
        self.pointer = libtpu.tpu_create_tensor_buffer_object(prog.pointer, Type)

    def __del__(self):
        return libtpu.tpu_destroy_tensor_buffer_object(self.pointer)

    def process_tensor_buffers(self):
        return libtpu.tpu_process_tensor_buffers(self.pointer)

    def get_tensor_buffer_ptr(self, n, raw):
        return libtpu.tpu_get_tensor_buffer_ptr(self.pointer, c_size_t(n), c_bool(raw))

    def set_user_tensor_buffer_ptr(self, n, ptr):
        return libtpu.tpu_set_user_tensor_buffer_ptr(self.pointer, c_size_t(n), ptr)


class TPUInference(Structure):

    _fields_ = []

    def __init__(self, program):
        self.pointer = libtpu.tpu_create_inference(program.pointer)

    def __del__(self):
        return libtpu.tpu_destroy_inference(self.pointer)

    def get_program(self):
        return libtpu.tpu_get_inference_program(self.pointer)

    def get_inputs(self):
        return libtpu.tpu_get_inference_inputs(self.pointer)

    def set_inputs(self, buf_obj):
        return libtpu.tpu_set_inference_inputs(self.pointer, buf_obj.pointer)

    def set_outputs(self, buf_obj):
        return libtpu.tpu_set_inference_outputs(self.pointer, buf_obj.pointer)

    def get_outputs(self):
        return libtpu.tpu_get_inference_outputs(self.pointer)

    def get_status(self):
        return libtpu.tpu_get_inference_status(self.pointer)

    def get_error(self):
        return libtpu.tpu_get_inference_error_message(self.pointer)

CB_POINTER = CFUNCTYPE(None, POINTER(TPUInference), c_int, c_void_p)


def load_inference(data, program, mode=False):
    in_meta = input_metadata(program)
    out_meta = output_metadata(program)

    if not isinstance(data, dict):
        data_ = {}
        for k, d_ in zip(in_meta, (data, )):
            data_.update({k: d_})
        data = data_

    tpu_input = TPUTensorBufferObject(program, TPUTensorBufferType.kInputs.value)
    for i, (k, data) in enumerate(data.items()):
        in_tensor = bytearray(data)
        p_in_tensor = (c_uint8 * program.get_input_size(i, mode)).from_buffer(in_tensor)
        tpu_input.set_user_tensor_buffer_ptr(i, cast(p_in_tensor, POINTER(c_uint8)))

    out_ctx = []
    tpu_output = TPUTensorBufferObject(program, TPUTensorBufferType.kOutputs.value)
    for o, k in enumerate(out_meta):
        out_tensor = bytearray(np.empty((program.get_output_size(o, mode), ), dtype=np.uint8))
        p_out_tensor = (c_uint8 * program.get_output_size(o, mode)).from_buffer(out_tensor)
        c_out_ptr = cast(p_out_tensor, POINTER(c_uint8))
        out_ctx.append(c_out_ptr)
        tpu_output.set_user_tensor_buffer_ptr(o, c_out_ptr)
    return tpu_input, tpu_output, tuple(out_ctx)

@CB_POINTER
def inference_cb_(inference, result, context):
    cast(context, POINTER(py_object)).contents.value.set()


@CB_POINTER
def inference_cb(inference, result, context):
    cast(context, POINTER(py_object)).contents.value = True


async def submit_inference_(device, program, inference, output_buffer, mode):
    finish_flag = asyncio.Event()
    finish_flag_p = cast(pointer(py_object(finish_flag)), c_void_p)
    # print(f'Flag status before: {finish_flag.is_set()}')
    status = device.submit_inference(inference, mode, inference_cb, finish_flag_p)
    await POINTER(py_object).from_address(addressof(finish_flag_p)).contents.value.wait()

    # print(f'Flag status after: {POINTER(py_object).from_address(addressof(finish_flag_p)).contents.value.is_set()}')
    assert status == 0


async def submit_inference(device, program, inference, output_buffer, mode):
    finish_flag = False
    finish_flag_p = cast(pointer(py_object(finish_flag)), c_void_p)
    # print(f'Flag status before: {finish_flag}')
    status = device.submit_inference(inference, mode, inference_cb, finish_flag_p)
    while not POINTER(py_object).from_address(addressof(finish_flag_p)).contents.value:
        await asyncio.sleep(0)

    # print(f'Flag status after: {POINTER(py_object).from_address(addressof(finish_flag_p)).contents.value}')
    assert status == 0, 'Inference did not start!'

def get_inference(program, output_buffer, out_ctx, as_dict=True, mode=False):
    out_meta = output_metadata(program)
    collected_data = dict() if as_dict else list()

    for i, k in enumerate(out_meta):
        data = np.ctypeslib.as_array(out_ctx[i], shape = (program.get_output_size(i, mode), ))
        data = convert_from_uint8_to_user_dtype(data, out_meta[k]['user_dtype'])
        data = data.reshape(out_meta[k]['user_shape'])
        if as_dict:
            collected_data.update({k: data})
        else:
            collected_data.append(data)
    return collected_data

class TPUProcessingMode(Enum):
    kRaw = 0
    kPreprocess = 1
    kPostprocess = 2
    kFull = 3

class TPUTensorBufferType(Enum):
    kInputs = 0
    kOutputs = 1

class TPUInferenceStatus(Enum):
    kOk = 0
    kError = 1
    kDevError = 2


# TPUDevice
libtpu.tpu_create_device.restype = POINTER(TPUDevice)
# libtpu.tpu_create_device.argtypes = [c_int]
libtpu.tpu_create_device.argtypes = [c_char_p]

libtpu.tpu_destroy_device.restype = c_void_p
libtpu.tpu_destroy_device.argtypes = [POINTER(TPUDevice)]

libtpu.tpu_is_device_valid.restype = c_int
libtpu.tpu_is_device_valid.argtypes = [POINTER(TPUDevice)]

libtpu.tpu_init_device.restype = c_int
libtpu.tpu_init_device.argtypes = [POINTER(TPUDevice)]

libtpu.tpu_get_device_error_message.restype = c_char_p
libtpu.tpu_get_device_error_message.argtypes = [POINTER(TPUDevice)]

libtpu.tpu_get_device_info.restype = c_char_p
libtpu.tpu_get_device_info.argtypes = [POINTER(TPUDevice)]

libtpu.tpu_load_program.restype = c_int
libtpu.tpu_load_program.argtypes = [POINTER(TPUDevice), POINTER(TPUProgram)]

libtpu.tpu_run_inference.restype = c_int
libtpu.tpu_run_inference.argtypes = [POINTER(TPUDevice), POINTER(TPUInference), c_int]

libtpu.tpu_submit_inference.restype = c_int
libtpu.tpu_submit_inference.argtypes = [POINTER(TPUDevice), POINTER(TPUInference), c_int, CB_POINTER, c_void_p]

# TPUProgram
libtpu.tpu_create_program.restype = POINTER(TPUProgram)
libtpu.tpu_create_program.argtypes = [POINTER(c_char)]

libtpu.tpu_destroy_program.restype = c_void_p
libtpu.tpu_destroy_program.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_is_program_valid.restype = c_int
libtpu.tpu_is_program_valid.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_get_program_info.restype = c_char_p
libtpu.tpu_get_program_info.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_get_program_error_message.restype = c_char_p
libtpu.tpu_get_program_error_message.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_get_batch_size.restype = c_size_t
libtpu.tpu_get_batch_size.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_get_input_count.restype = c_size_t
libtpu.tpu_get_input_count.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_get_input_size.restype = c_size_t
libtpu.tpu_get_input_size.argtypes = [POINTER(TPUProgram), c_size_t, c_bool]

libtpu.tpu_get_output_count.restype = c_size_t
libtpu.tpu_get_output_count.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_get_output_size.restype = c_size_t
libtpu.tpu_get_output_size.argtypes = [POINTER(TPUProgram), c_size_t, c_bool]

# TPUTensorBufferObject
libtpu.tpu_create_tensor_buffer_object.restype = POINTER(TPUTensorBufferObject)
libtpu.tpu_create_tensor_buffer_object.argtypes = [POINTER(TPUProgram), c_int]

libtpu.tpu_destroy_tensor_buffer_object.restype = c_void_p
libtpu.tpu_destroy_tensor_buffer_object.argtypes = [POINTER(TPUTensorBufferObject)]

libtpu.tpu_process_tensor_buffers.restype = c_void_p
libtpu.tpu_process_tensor_buffers.argtypes = [POINTER(TPUTensorBufferObject)]

libtpu.tpu_get_tensor_buffer_ptr.restype = POINTER(c_uint8)
libtpu.tpu_get_tensor_buffer_ptr.argtypes = [POINTER(TPUTensorBufferObject), c_size_t, c_bool]

libtpu.tpu_set_user_tensor_buffer_ptr.restype = POINTER(c_uint8)
libtpu.tpu_set_user_tensor_buffer_ptr.argtypes = [POINTER(TPUTensorBufferObject), c_size_t, POINTER(c_uint8)]

# TPUInference
libtpu.tpu_create_inference.restype = POINTER(TPUInference)
libtpu.tpu_create_inference.argtypes = [POINTER(TPUProgram)]

libtpu.tpu_destroy_inference.restype = c_void_p
libtpu.tpu_destroy_inference.argtypes = [POINTER(TPUInference)]

libtpu.tpu_get_inference_program.restype = POINTER(TPUProgram)
libtpu.tpu_get_inference_program.argtypes = [POINTER(TPUInference)]

libtpu.tpu_get_inference_inputs.restype = POINTER(TPUTensorBufferObject)
libtpu.tpu_get_inference_inputs.argtypes = [POINTER(TPUInference)]

libtpu.tpu_set_inference_inputs.restype = POINTER(TPUTensorBufferObject)
libtpu.tpu_set_inference_inputs.argtypes = [POINTER(TPUInference), POINTER(TPUTensorBufferObject)]

libtpu.tpu_get_inference_outputs.restype = POINTER(TPUTensorBufferObject)
libtpu.tpu_get_inference_outputs.argtypes = [POINTER(TPUInference)]

libtpu.tpu_set_inference_outputs.restype = POINTER(TPUTensorBufferObject)
libtpu.tpu_set_inference_outputs.argtypes = [POINTER(TPUInference), POINTER(TPUTensorBufferObject)]

libtpu.tpu_get_inference_status.restype = c_int
libtpu.tpu_get_inference_status.argtypes = [POINTER(TPUInference)]

libtpu.tpu_get_inference_error_message.restype = c_char_p
libtpu.tpu_get_inference_error_message.argtypes = [POINTER(TPUInference)]
