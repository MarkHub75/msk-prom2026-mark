# PROPOSED, NOT_RUN. Place beside MMDeploy v1.3.1's stock config before use.
# This is an explicit new export config, not a claim of a stock static file.
_base_ = ['./pose-detection_simcc_onnxruntime_dynamic.py']
onnx_config = dict(dynamic_axes=None, input_shape=[192, 256], optimize=False)
codebase_config = dict(export_postprocess=False)
