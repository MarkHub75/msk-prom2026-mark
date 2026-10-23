#!/usr/bin/env bash
# After one authorized Jupyter bootstrap cell: upload+verify, then real inference.
set +x
set -euo pipefail
umask 077
cd /workspace/project
set -a
source /workspace/linq-client/connection.env
set +a
export PYTHONPATH=/workspace/linq-client:/workspace/project
client=/workspace/.venvs/linq-client/bin/python
if [[ "${1:-helmet}" == 'all' ]]; then
  "$client" -m ml.pipeline.remote_deploy helmet
  "$client" -m ml.pipeline.remote_deploy pose-split
else
  "$client" -m ml.pipeline.remote_deploy "${1:-helmet}"
fi
