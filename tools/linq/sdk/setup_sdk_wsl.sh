#!/usr/bin/env bash
# Set up the LinQ tpu_framework SDK (cp312 linux wheels) in WSL Ubuntu without sudo.
#   wsl -d Ubuntu -- bash /mnt/d/msk-prom2026-mark/tools/linq/sdk/setup_sdk_wsl.sh
# Result: ~/linq_sdk/venv (Python 3.12.11, as the SDK README requires).
set -euo pipefail
REPO="${REPO:-/mnt/d/msk-prom2026-mark}"
PKT="$REPO/vendor/linq/sdk/Framework/tpu_framework/tpu_framework/packets"
SDK_HOME="$HOME/linq_sdk"

export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
uv python install 3.12.11
mkdir -p "$SDK_HOME"
[ -d "$SDK_HOME/venv" ] || uv venv "$SDK_HOME/venv" --python 3.12.11
cd "$PKT"
# requirements.txt lists the vendor wheels by relative path + pinned onnxruntime/pytest/attrs
uv pip install --python "$SDK_HOME/venv/bin/python" -r requirements.txt
# extra tools for our scripts (export sidecars, image IO for calibration)
uv pip install --python "$SDK_HOME/venv/bin/python" "opencv-python-headless<4.12" pillow
"$SDK_HOME/venv/bin/python" - <<'EOF'
import importlib.metadata as md, sys
print("python", sys.version.split()[0])
for d in ("tpu_framework_bin", "tpu_compiler_bin", "dnn_quant_bin", "onnx_direct_bin", "onnxruntime", "onnx", "torch", "numpy"):
    try:
        print(f"{d:20} {md.version(d)}")
    except md.PackageNotFoundError:
        print(f"{d:20} -")
import tpu_framework
print("tpu_framework import OK:", [n for n in ("RegularModel", "QuantizedModel", "Network", "compiler", "TpuProgram", "O1", "O5", "TPU_H1M") if hasattr(tpu_framework, n)])
EOF
