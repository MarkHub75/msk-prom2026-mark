#!/usr/bin/env bash
# One request only after successful ResNet and hash-verified remote file staging.
set +x
set -euo pipefail
umask 077
cd /workspace/project
if [[ -e /workspace/artifacts/linq-rpc/helmet-001 ]]; then
  echo 'Capture already exists. No resend/overwrite will occur.'
  exit 2
fi
/venv/main/bin/python - <<'PY'
import json
from pathlib import Path
base=Path('/workspace/artifacts/linq-rpc')
resnet=json.loads((base/'resnet50-001/resnet-check.json').read_text())
if resnet['status']!='PASS' or resnet['status_code']!=0:raise ValueError('successful ResNet gate required')
receipt=json.loads((base/'helmet/staging-receipt.json').read_text())
if receipt.get('program_name')!='helmet-v1.tpu' or receipt.get('program_sha256')!='408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa' or receipt.get('status') not in ('STAGED','ALREADY_STAGED_IDENTICAL'):
    raise ValueError('reviewed remote staging receipt required')
PY
/venv/main/bin/python -m ml.pipeline.prepare_model_probe helmet
set -a
source /workspace/linq-client/connection.env
set +a
if [[ "${LINQ_AMQP_HOST:-}" != '127.0.0.1' || "${LINQ_AMQP_PORT:-}" != '15672' || -z "${LINQ_LOGIN:-}" ]]; then
  echo 'Runtime tunnel configuration missing or different'
  exit 2
fi
export PYTHONPATH=/workspace/linq-client:/workspace/project
/workspace/.venvs/linq-client/bin/python -m ml.linq.amqp \
  --format-source-manifest /workspace/artifacts/linq-rpc/format-source.json \
  --exchange tpu.direct --routing-key input --reply-exchange tpu.direct \
  --target-uri "file:///auto/cache/${LINQ_LOGIN}/helmet-v1.tpu?raw=False" \
  --program-file /workspace/artifacts/linq-sdk/helmet-compile/model.tpu \
  --input-npz /workspace/artifacts/linq-rpc/helmet/inputs.npz \
  --output-name output0 --model-id helmet-v1 \
  --output-dir /workspace/artifacts/linq-rpc/helmet-001 \
  --timeout 60 --host 127.0.0.1 --port 15672 \
  --notebook-reply-queue --attest-linq-placement --attest-program-match
/venv/main/bin/python -m ml.pipeline.capture_review \
  --capture /workspace/artifacts/linq-rpc/helmet-001 \
  --expected-program-sha256 408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa
/venv/main/bin/python -m ml.detection.compare_capture \
  --reference /workspace/artifacts/linq-rpc/helmet/golden-outputs.npz \
  --actual /workspace/artifacts/linq-rpc/helmet-001/outputs.npz \
  --manifest /workspace/artifacts/detection/helmet/manifest.json \
  --metadata /workspace/artifacts/linq-rpc/helmet/comparison-metadata.json \
  --output /workspace/artifacts/linq-rpc/helmet-001/comparison.json
