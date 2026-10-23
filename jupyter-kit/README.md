# MOSPROM LinQ Jupyter kit

Includes current capture/integrity/comparison Python helpers, runtime dependency list, real precompiled Helmet and preferred Split-Pose programs, matching preprocessed golden inputs and float reference outputs. No training/compiler/driver installation, source video, credentials, session state or mixed-pose rejected program is included.

The user reported stock ResNet50 status_code=0, class257, response0.39 seconds. Raw tensors and the remote notebook call have not been provided to the agent. This confirms the reported stock result; it does not verify our models or identify the service API.

**Remote binding is not yet configured.** `bindings.py` is guarded and makes no request. It needs the actual credential-free import/call/result-extraction snippet from the working example.ipynb. `examples/local_pytpu_reference.py` matches a public LOCAL device example and is explicitly not the remote service binding. Do not replace the working service call with that local API unless the notebook actually uses it.

## Upload and local structure checks in Jupyter

Upload linq-jupyter-kit.zip to the same user workspace where the stock notebook worked. In a notebook cell:

```python
from pathlib import Path
import zipfile

DEST = Path('linq-jupyter-kit')
if DEST.exists():
    raise FileExistsError('Choose a new directory; do not overwrite an existing kit/capture')
with zipfile.ZipFile('linq-jupyter-kit.zip') as archive:
    for name in archive.namelist():
        path = Path(name)
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Invalid archive path')
    archive.extractall(DEST)
```

```python
%run linq-jupyter-kit/verify_kit.py
```

Then:

```python
import sys
from pathlib import Path
KIT = Path('linq-jupyter-kit').resolve()
sys.path.insert(0, str(KIT))
import numpy
from PIL import Image
from ml.linq.jupyter import prepare_case, capture_case

helmet = prepare_case(KIT, 'helmet')
print({'model_id': helmet['model_id'], 'program_sha256': helmet['compile_report']['program_sha256']})
```

NumPy/Pillow are already used by the supplied examples. Check imports first. requirements.txt lists only runtime helpers; do not upgrade a working organizer environment blindly. No Torch, Ultralytics, ONNX, compiler or CUDA is required here. The service client remains the one already supplied in example.ipynb.

## Helmet first

Use the actual supplied notebook method to upload/load **models/helmet/model.tpu**. Bind `invoke_helmet(named_inputs)` to that loaded program, wait for completion, require the actual returned status_code to equal0, and return a mapping containing only selected numeric tensors. No endpoint/client signature or output reshaping is inferred by this kit.

Expected candidate boundary: images float32[1,3,640,640] -> output0 float32[1,6,8400]. These are compilation metadata pending verification on the remote runtime. Inputs are already RGB/letterbox/normalized; never apply ResNet preprocessing to them.

Once that actual binding exists in the kernel:

```python
helmet_capture = capture_case(
    KIT, 'helmet', invoke_helmet, 'capture-helmet-001',
    diagnostic_only=True, placement_attested=True,
)
print({'status': helmet_capture['status'], 'call_completed': helmet_capture['call_completed']})
```

`invoke_helmet` is the missing actual service binding, not a function automatically supplied by the organizer. It must load the exact program whose file is hashed. Diagnostic mode records actual selected numeric outputs for the first ABI check and does not set runtime_abi_verified. If tensor names differ, pass an explicit runtime-name -> reference-name map; no positional/shape guessing or implicit dequantization is allowed.

## Export the selected capture

After status completed:

```python
from ml.pipeline.capture_review import review_capture
print(review_capture('capture-helmet-001', helmet['compile_report']['program_sha256'])['status'])

with zipfile.ZipFile('capture-helmet-001.zip', 'x', zipfile.ZIP_DEFLATED) as archive:
    for filename in ('capture.json', 'inputs.npz', 'outputs.npz'):
        archive.write(Path('capture-helmet-001') / filename, filename)
```

Download only that ZIP from Jupyter. It contains selected numeric arrays and allowlisted metadata, no notebook/auth/session objects. Retain it outside Git. Capture input arrays can contain image pixels; use the team's permitted transfer channel.

The comparison module uses package imports. Use a terminal from the extracted kit directory:

```bash
python -m ml.pipeline.capture_review --capture ../capture-helmet-001
python -m ml.detection.compare_capture --reference models/helmet/golden-outputs.npz --actual ../capture-helmet-001/outputs.npz --metadata ../capture-helmet-001/capture.json --manifest models/helmet/manifest.json --output helmet-comparison.json
```

Or call `compare_captures` from the existing kernel; see docs/JUPYTER_KIT.md. Status COMPARED is a numeric diagnostic, not industrial accuracy acceptance.

## Split-Pose second

Only after Helmet capture integrity, actual names/dtype/shape and decoded results are reviewed, use the same actual service to upload/load **models/pose-split/model.tpu**, bind `invoke_pose` to that program, then:

```python
pose = prepare_case(KIT, 'pose-split')
pose_capture = capture_case(KIT, 'pose-split', invoke_pose, 'capture-pose-split-001',
                            diagnostic_only=True, placement_attested=True)
```

Split-Pose outputs four named tensors (boxes, person scores, keypoint XY, keypoint confidence). Keep exact names in the manifest, including `/`; no repeated neural decoding. The earlier mixed-output pose was rejected because PTQ erased confidences and is not shipped. Both included programs use one-image compiler-smoke calibration; target-video accuracy remains unverified.
