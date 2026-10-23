#!/usr/bin/env bash
# Sequential REAL LinQ file worker; runtime secrets are never echoed.
set +x
set -euo pipefail
umask 077
cd /workspace/project
set -a
source /workspace/linq-client/connection.env
set +a
export PYTHONPATH=/workspace/linq-client:/workspace/project
exec /workspace/.venvs/linq-client/bin/python -m ml.pipeline.video_mvp "$@"
