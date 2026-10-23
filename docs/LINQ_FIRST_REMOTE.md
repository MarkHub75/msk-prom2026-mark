# First automatic Vast -> LinQ inference

The stock ResNet50 request has completed through the existing loopback AMQP tunnel, using the real source-pinned tpu_pycloud_format0.0.1 and the user-provided runtime file outside Git. ID correlation, status, exact input/output ABI and capture integrity passed. Exactly one inference publication was attempted. This is a completed service inference, not an AMQP-connectivity smoke. Numerical arrays, task ID and timing reports remain outside Git:

`/workspace/artifacts/linq-rpc/resnet50-001/{capture.json,inputs.npz,outputs.npz,response.json,resnet-check.json,integrity-review.json}`

The saved timing is whole client connection/channel/publish/wait/close time, not chip-compute time. Local expected program bytes are hashed; remote program bytes were not independently inspected. No connection.env values are recorded in this document or exported into a model package.

## Exact launch entrypoint

```bash
cd /workspace/project
bash scripts/linq_resnet_probe.sh
```

The default capture directory already exists after the successful first call. The script intentionally refuses to resend or overwrite it. The actual first invocation used the same flags and environment-loading steps written in that script. Review the existing capture instead:

```bash
PYTHONPATH=/workspace/project /workspace/.venvs/linq-client/bin/python -m ml.pipeline.capture_review --capture /workspace/artifacts/linq-rpc/resnet50-001
```

The client reads `/workspace/linq-client/connection.env` inside its process. Never print or upload this file. Authentication is not embedded in command arguments. Request/reply exchange tpu.direct, routing input, stock URI in the configured user's /auto/cache namespace, notebook reply-queue policy and timeout60 come directly from the confirmed organizer notebook. No guessed credentials/path or automatic resend exists.

## Helmet file deployment is a separate operation

`file://` is resolved by the LinQ worker. A Vast file with the same name is not enough. RabbitMQ tensor transport does not implement program-file upload. Upload **only** `/workspace/artifacts/linq-rpc/helmet-upload.zip` through the already authenticated organizer Jupyter. Do not upload connection.env.

In the stock notebook's kernel, after uploading the ZIP:

```python
import json, sys, zipfile
from pathlib import Path
from urllib.parse import urlsplit, unquote
from tpu_pycloud_format import TARGET_URI_ATTR_NAME

folder = Path('helmet-upload')
if folder.exists():
    raise FileExistsError('Choose a new directory; do not overwrite a previous upload')
with zipfile.ZipFile('helmet-upload.zip') as archive:
    archive.extractall(folder)
sys.path.insert(0, str(folder.resolve()))
from stage_helmet import stage

# headers is the request-header mapping from the successful stock notebook cell.
# It is read in memory, never printed, serialized or exported.
stock = urlsplit(headers[TARGET_URI_ATTR_NAME])
if stock.scheme != 'file' or Path(unquote(stock.path)).name != 'torch_resnet50_b1_o5_h1m.tpu':
    raise ValueError('Use the actual successful stock request headers')
receipt = stage(Path(unquote(stock.path)).parent)
Path('helmet-staging-receipt.json').write_text(json.dumps(receipt, indent=2))
print({'status': receipt['status'], 'program_sha256': receipt['program_sha256']})
```

The helper requires the selected directory to already contain the stock program. It verifies the reviewed Helmet SHA256, refuses different existing bytes and reports no account/path. It never creates guessed namespaces or changes an existing program. If Jupyter cannot see that directory, stop: request the organizer's supported program-upload/shared-cache route, rather than trying another URI. Worker visibility is only confirmed by a completed subsequent Helmet request.

Download only `helmet-staging-receipt.json` and place it at:

`/workspace/artifacts/linq-rpc/helmet/staging-receipt.json`

Then the ready one-request script is:

```bash
cd /workspace/project
bash scripts/linq_helmet_probe.sh
```

It gates on the successful stock result plus the receipt hash; prepares the existing golden RGB/letterbox images input (no training/compilation), calls the same ml.linq.amqp client exactly once, verifies capture integrity and writes named-output/decoded comparison outside Git. It refuses existing captures and does not retry a timeout. Original error text is bounded/redacted; no alternative program URI is substituted. INT8 calibration is still a one-image compiler smoke, so a successful call does not establish target CCTV accuracy.

Split-Pose follows only after Helmet's actual file/transport/output checks. Its existing reviewed program remains ready; no training or model regeneration is needed.
