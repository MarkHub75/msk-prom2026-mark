# LinQ integration: execution status and safe runbook

## Measured state on this Vast instance

2026-10-23 UTC: `/dev/net/tun` absent; `openvpn`, `tpu_framework` and `pytpu` unavailable. `hackathon.lin-q.ru` fails DNS resolution (`gaierror`), so Jupyter/TCP cannot be reached here. Authentication, vendor ResNet50 and our models have **not run**. This is an access/runtime blocker, not evidence of a model/compiler failure. Do not report RTX/ONNX or mocked calls as LinQ execution.

Run the safe inventory again:

```bash
python -m ml.linq.preflight --timeout 3
```

It prints statuses and HTTP status numbers only. It never opens a VPN profile, reads credentials, authenticates, emits response cookies, installs packages or changes routing. HTTP reachability does not prove authentication. Its final `hardware_inference_confirmed` remains false.

## Issued documents and public artifacts

Official case instructions define ONNX -> vendor SDK quantization/compilation -> TPU program -> named input tensor -> accelerator API -> output tensors. They provide SDK share `https://cloud.lin-q.ru/s/bEqr922zr6NXHy4` and API examples share `https://cloud.lin-q.ru/s/QcFLdkdLb71BOmm`. Both share pages returned HTTP 200 on this instance. API ZIP download was read in memory (87,279,767 bytes, sha256 `5fdb904a67cae4c8b2cb0b6f2485bbf7d58b8a8643fffd20a79fce2f8e5ae23f`). It contains nested C, C++, OpenCV ResNet50 and Python API archives. This confirms artifact availability, not installability or remote-service ABI.

No vendor package has been installed into the existing PyTorch environment. The inspected nested Python archive has SHA256 `5ab6d731b3e9700363b6d5c9bebfbbbf4b7928af46173156ddb5d451dc1c5bf8`. It contains an image, `torch_resnet50_b1_o5_h1m.tpu` and an example using `Device.list_devices -> Device.open -> load -> inference -> inference.run(inputs)`. Input is `input.1`, NCHW float32 224×224, output `495`, expected class 257 with offset 1. This issued example uses **run**, not the historical **sync** API; it is local and does not define remote Jupyter transport.

`LocalPytpuRunner(program_path, program_sha256)` implements that exact local API as a context manager, verifies the pinned program hash before importing runtime, retains its session across requests and copies outputs before closing it. It is usable only on a host with matched `pytpu`, native libraries and visible TPU device. It has been tested only with a mock runtime here.

The SDK public share was inventoried through bounded ZIP range reads: `tpu_framework_2026.9.45.zip`, 505,123,114 bytes. Downloaded constituent wheels live outside Git at `/workspace/artifacts/linq-sdk/`; compiler environment is isolated at `/workspace/.venvs/linq-sdk`. The bundle requires Python 3.12.11 and provides cp312 Linux x86_64 wheels (this host is Python 3.12.15). Framework 2026.9.45 pins compiler 2026.9.493, quantizer 2026.9.98, onnx_direct 2026.8.23, Torch 2.9.1, TensorFlow 2.20.0, Keras 3.14.0, NumPy 1.26.4 and ONNX ~1.16. The existing main environment remains untouched.

**The current SDK changes the research-era path:** the supplied compiler accepts ONNX via `preliminary_model_conditioning`, `RegularModel`, `calibrate_torch`, `quantize`, `Network.from_quantized_model`, `compiler.compile_(TPU_H1M, O1)` and `TpuProgram.to_file`. Do not assemble an old TensorFlow conversion recipe. The bundled random calibration is only a smoke fixture; our compilation helper requires an NPZ of real preprocessed images.

```bash
PYTHONPATH=. /workspace/.venvs/linq-sdk/bin/python -m ml.linq.compile \
  --onnx /path/to/weights.onnx --calibration /path/to/calibration.npz \
  --model-id helmet-v1 --output /path/to/compiled --preset O1
```

A completed compile report still records `linq_status=NOT_RUN` and `runtime_abi_verified=false`. Its tensor specs describe conditioned ONNX and must be checked against actual TPU metadata. The adapter expects `model_id`, `program_sha256`, `inputs` and `outputs`; preserve the detection manifest and pass its dedicated `linq` block merged with `model_id` after runtime ABI verification.

## Completed local compilation experiment

Helmet ONNX `b312701494991ff7ecc82cb86cc71a8a145a871f6ff342908bb5137e1e8caa47` completed current SDK conditioning, `calibrate_torch`, quantization and TPU_H1M O1 compilation in 72.66 seconds. Program is `/workspace/artifacts/linq-sdk/helmet-compile/model.tpu`, SHA256 `408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa`. Pose ONNX `398cc23eac1b4702656d2ec4486d7aa1e5bda8563d33babaa9017ab3fdd5b02f` also compiled successfully in 76.26 seconds. Its program is `/workspace/artifacts/linq-sdk/pose-compile/model.tpu`, SHA256 `23c0e53439032860706c28d1e9f493f1e84bda85b679997b7336412db62c4e1c`. Conditioned output is `output0` float32 `[1,56,8400]` (same input). Full local compile metadata is alongside each program in `compile-report.json`; downloaded wheel hashes are in `/workspace/artifacts/linq-sdk/package-inventory.json`.

The exact supplied ResNet example, image and program are available at `/workspace/artifacts/linq-api/`, with `vendor-inventory.json`. Vendor program SHA256: `0bac3ad590505fb20753e4888bec3fce9202a6e1c96cad3abe74a2a4b283d60c`. These are public supplied assets, not a completed hardware run.

This is a **compiler smoke**, using exactly one real bus photograph after the same RGB letterbox preprocessor. It proves the selected full decoded detection graph passes this compiler build; it does not validate quantized detector accuracy. The SDK upgraded opset 13 to 17 during conditioning. Conditioned ONNX ABI: `images` float32 `[1,3,640,640]` -> `output0` float32 `[1,6,8400]`. Actual TPU runtime ABI and hardware execution remain unverified. Replace this calibration with a representative separate PPE corpus before claiming accuracy.


### Quantized simulation gate: pose confidence failure

A bounded CPU hardware-aware Torch graph check was run on the same calibration image using `QuantizedModel.load(...).as_torch_graph(batch_size=1).gm(...)`. This graph consumes/returns quantized codes; direct comparison to float ONNX is invalid. The first raw probe is retained with `valid_for_accuracy=false`. A second diagnostic applies `round(input * images.data_scale)` and multiplies each output channel by its recorded `scales.json` data scale. The scaling policy still needs confirmation against the actual vendor/runtime codec; this is not hardware parity.

Under that explicit policy, helmet class scores remain nonzero (maximum 0.35259 versus float 0.35823; 3 versus 2 anchors above 0.25). Pose person scores also survive (30 versus 30 anchors above 0.25). **Pose keypoint confidence channels are all zero**, while float keypoint confidence reaches 0.99891. The recorded output scale is 5.81299 for all keypoint channels, including confidence; mixing pixel coordinates with probabilities loses the confidence signal. This candidate pose program is therefore **not accepted for behavior analysis**, despite successful compilation.

Reports and arrays: each model's compile directory contains `quantized-torch-scaled-smoke-report.json` and `quantized-torch-scaled-smoke-output.npz`. They are diagnostics from one reused image, not accuracy measurements. Next graph experiment should separate keypoint coordinates and confidence into different output tensors before PTQ, preserve the output mapping, then reassemble the decoder input on the host and repeat reference/quantized/runtime tests. Do not invent missing confidence values or lower the keypoint threshold to accept zeros.

## First access on the Arch laptop

1. Check TUN presence, installed OpenVPN client, current resolver and network manager. Ubuntu package/systemd commands from the supplied PDF are not Arch instructions.
2. Import the organizer's profile through the available client. Keep the profile and any credential material outside Git. Enter credentials interactively in the trusted VPN/Jupyter UI or use an existing protected OS credential mechanism; never put a password in command arguments or notebook cells.
3. Establish VPN. Verify the assigned route and DNS for `lin-q.ru`; organizer Ubuntu example names route `10.0.114.0/24`, but verify the actual issued configuration. Preserve the normal internet route where supported. Do not replace host routing blindly.
4. Resolve `hackathon.lin-q.ru`, then open `http://hackathon.lin-q.ru/` over VPN. Confirm authenticated Jupyter access and a running kernel. Do not copy its authenticated URL/cookies into logs or this repository.
5. Inspect `examples` and `packages`. Capture only SDK/runtime versions, Python/OS/architecture, input/output specs, program names/hashes, quotas and supported completion semantics. Use the supplied per-team username only in the runtime call as instructed; exclude it from committed artifacts.
6. Run the supplied ResNet50 example. Preserve sanitized request correlation, program hash, known input hash, tensor shapes/dtypes, output and completion record. Save notebooks without credentials and clear sensitive outputs before sharing.
7. Compile a team-owned static-shape model using a separate environment matching the supplied compiler. Upload the `.tpu` program through the supported interface. Test the exact exported tensor against reference output; only then run video frames.

If Jupyter works but the programmatic remote path is unknown, inspect the actual supplied notebook/client. Do not guess an inference URL. If only a local-on-Jupyter API exists, run the adapter there and connect through a supported transport; never expose an unauthenticated notebook/kernel or raw TPU server to the internet.

## Adapter contract

```python
from ml.linq import LinQBackend
backend = LinQBackend(manifest, runner=issued_runner)
result = backend.infer({"request_id": "req-1", "model_id": manifest["model_id"],
                        "inputs": {"input_name": contiguous_numpy_array}})
```

Manifest `inputs` and `outputs` are nonempty lists of `{name, shape, dtype}` with exact positive static dimensions. `program_sha256` identifies the compiled artifact. Runner is a blocking callable `(inputs, metadata) -> outputs` or returns `{outputs, execution_witness}`. Its implementation must use the verified supplied API. It must not log raw exceptions/auth headers or silently switch to CPU/GPU. `runner=None` produces `linq_unavailable`.

The adapter checks model identity, exact names, shape, dtype, finite values, contiguous storage and byte size before submission, and validates/copies output arrays before transfer to another consumer. Errors contain stable codes and exception types only, never SDK exception messages. Validated successful output does not prove TPU placement: `execution_verified` stays false. A correlated `execution_witness` may preserve an allowlisted service completion claim; independent run evidence must still be reviewed.

`runner_ms` measures the whole blocking call, including transport/wait when those occur in the runner; it is **not device time**. `total_ms` includes adapter validation and copies. Do not publish `runner_ms` as chip latency.

Timeout/retry behavior belongs to the issued transport. A local timeout is not remote cancellation. Start with one outstanding call, do not blindly retry an ambiguously accepted request, and reconcile remote completion before reusing its quota. This synchronous adapter does not claim cancellation support.

## Acceptance and handoff

Required gates: VPN; authenticated Jupyter; matched SDK/compiler; completed vendor ResNet50; compiled own model; completed own-model run; reference/TPU parity; video cadence and event latency. Record PASS/FAIL/UNAVAILABLE/NOT_RUN independently. A model manifest and copied tensors without completed LinQ evidence leave the hardware gate open.

Tests in `tests/test_linq.py` cover mocked contracts, invalid inputs/outputs, output ownership, error redaction, witness correlation and honest preflight status. They do not test hardware, VPN authentication, quantization quality or model accuracy.
