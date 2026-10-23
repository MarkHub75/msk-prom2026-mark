#!/usr/bin/env bash
# Exactly one authorized ResNet50 request. Never echo private runtime values.
set +x
set -euo pipefail
umask 077
cd /workspace/project
if [[ -e /workspace/artifacts/linq-rpc/resnet50-001 ]]; then
  echo 'Capture already exists. Review it; this script will not resend or overwrite.'
  exit 2
fi
set -a
source /workspace/linq-client/connection.env
set +a
if [[ "${LINQ_AMQP_HOST:-}" != '127.0.0.1' || "${LINQ_AMQP_PORT:-}" != '15672' || -z "${LINQ_LOGIN:-}" ]]; then
  echo 'Runtime configuration does not match the confirmed tunnel or lacks login'
  exit 2
fi
if [[ ! -f /workspace/artifacts/linq-rpc/resnet50/inputs.npz ]]; then
  /venv/main/bin/python -m ml.pipeline.prepare_resnet_probe
fi
export PYTHONPATH=/workspace/linq-client:/workspace/project
exec /workspace/.venvs/linq-client/bin/python -m ml.linq.amqp \
  --format-source-manifest /workspace/artifacts/linq-rpc/format-source.json \
  --exchange tpu.direct --routing-key input --reply-exchange tpu.direct \
  --target-uri "file:///auto/cache/${LINQ_LOGIN}/torch_resnet50_b1_o5_h1m.tpu?raw=False" \
  --program-file /workspace/artifacts/linq-api/torch_resnet50_b1_o5_h1m.tpu \
  --input-npz /workspace/artifacts/linq-rpc/resnet50/inputs.npz \
  --output-name 495 --model-id stock-resnet50 \
  --output-dir /workspace/artifacts/linq-rpc/resnet50-001 \
  --timeout 60 --host 127.0.0.1 --port 15672 \
  --notebook-reply-queue --attest-linq-placement
