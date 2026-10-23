# LinQ integration: execution status and safe runbook

## Measured state on this Vast instance

Current evidence supersedes the early preflight: stock ResNet50, Helmet and Split-Pose have completed real correlated service calls, including industrial frames. Numeric inputs/outputs and durable journals are outside Git. This proves the reviewed service path executes; it does not establish independent industrial accuracy. The quality audit below distinguishes current Split-Pose from the rejected mixed-output Pose.

Historical preflight on the Vast main environment (2026-10-23 UTC): `/dev/net/tun`, `openvpn`, `tpu_framework` and `pytpu` were unavailable; `hackathon.lin-q.ru` failed DNS resolution (`gaierror`). This describes that container/environment at that time. The user subsequently confirmed authenticated LinQ Jupyter access and the supplied `example.ipynb`. The earlier Vast result does not negate that access. Do not report RTX/ONNX or mocked calls as LinQ execution.

Use [JUPYTER_RUNBOOK.md](JUPYTER_RUNBOOK.md) and `ml.linq.notebook.capture_call` inside the existing authenticated session to capture exactly one inspected supplied call without exporting notebook/session secrets. The helper exports explicit numeric input/output NPZ and allowlisted metadata only. Hardware placement is labeled user/supplied-runtime attestation, never independent proof. No notebook is executed wholesale and no remote endpoint is invented.

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

Reports and arrays: each model's compile directory contains `quantized-torch-scaled-smoke-report.json` and `quantized-torch-scaled-smoke-output.npz`. They are diagnostics from one reused image, not accuracy measurements. The corrective split-output experiment below addresses this specific simulation failure. Original failing evidence remains unchanged. Do not invent missing confidence values or lower the keypoint threshold to accept zeros.


### Corrective split-pose compiler and simulation result

`pose-split-v1` prunes both mixed terminal concatenations and exports boxes, person scores, keypoint XY and keypoint confidence as four separate outputs. Source ONNX SHA256: `802f7cb032ed525855bd271017d376fedc14bfc5789669013cae01361fa5aa00`. TPU_H1M O1 compilation completed in 73.77 seconds. New distinct program: `/workspace/artifacts/linq-sdk/pose-split-compile/model.tpu`, SHA256 `c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b`.

The SDK's explicit `get_outputs_anchors()` maps original names to internal simulator names (`/model.22/...` -> `n_/model.22/...`). The diagnostic uses this map to find scales; it does not rename external detector outputs or guess prefixes. The split quantized simulation preserves keypoint confidence: range 0.004364–0.999023, versus float 0.003418–0.998908. Both decode to three people on the same image. Matched box IoUs are 0.8723/0.7812/0.9108; visible keypoint counts at confidence >=0.5 remain 16/17/9; mean XY differences for mutually visible points are 4.12/4.31/2.78 original-image pixels. This fixes the observed confidence collapse for this single-image diagnostic, not target accuracy or hardware parity.

Artifacts are in `/workspace/artifacts/linq-sdk/pose-split-compile/simulation/`: scaled/raw outputs, float reference outputs, `simulation-report.json`, and `decoded-comparison.json`. Reproduce the tensor diagnostic in the isolated SDK environment:

```bash
PYTHONPATH=. /workspace/.venvs/linq-sdk/bin/python -m ml.linq.simulate \
  --quantized /workspace/artifacts/linq-sdk/pose-split-compile/quantized.qm.onnx \
  --scales /workspace/artifacts/linq-sdk/pose-split-compile/scales.json \
  --inputs /workspace/artifacts/linq-sdk/calibration-smoke.npz \
  --source-onnx /workspace/artifacts/detection/pose-split/weights.onnx \
  --output /workspace/artifacts/linq-sdk/pose-split-compile/simulation
```

If conditioning changes public output names, compilation reports an explicit `output_name_map`; pass `--compile-report` to the diagnostic. The mapping is separate from SDK internal simulation anchors. The candidate still requires representative calibration, independent evaluation, runtime ABI/codec confirmation and completed real TPU inference.

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


## Durable video runner factory

`ml.linq.video:create_runner(effective_manifest)` binds only the reviewed Helmet and Split-Pose program names/hashes to the confirmed `file:///auto/cache/<LINQ_LOGIN>/<program_name>?raw=False` URI. It reads only already configured runtime environment keys; credentials/account/URI are never persisted. Required fields: model_id, program_name, program_path, program_sha256, inputs/outputs specs, rpc_state_dir=`<run>/rpc/<model_id>`, journal_dir=`<run>/requests`, format_source_manifest; timeout defaults to 60.

Each logical `(source epoch, frame, model)` request is keyed by SHA256 of the backend's explicit logical ID. Its identity and input tensor hashes are fsynced before networking. Existing UUIDs use receive-only/cached `AmqpRunner.reconcile`; UNKNOWN never republishes. A definitely NOT_SUBMITTED attempt is archived before a fresh UUID. Reusing a logical ID with changed input/model/program fails. One per-run process lock and active-logical fence prevent fresh publication for another model while a previous job is unresolved; cached completed outputs remain readable.

Success returns logical execution_witness plus allowlisted transport_provenance (distinct UUID, correlated response ID, numeric status, journal state/path, cache/recovery flags and scoped timing). Cached/recovery duration is labeled explicitly and is not original inference latency. Backend independent execution verification remains false.

PendingRequestError produces backend `status=pending`, with code linq_pending, linq_not_submitted or linq_busy. The file worker must stop on the SAME frame without creating an observation/gap or advancing its cursor. A correlated SERVICE_FAILED yields linq_service_failed and never repeats that logical job. Identity/configuration contract errors are fatal rather than missing observations. The factory itself performs no video decoding or additional RPC probes.

## Per-phase RPC timing and bounded disconnect experiment

`AmqpRunner.last_response.timings` and the backend's typed transport provenance now expose only finite nonnegative milliseconds:

- `connection_setup_ms`: official-format/runtime setup, TCP/AMQP handshake, channel/reply queue setup and confirm-mode negotiation. It includes the small local bookkeeping inside those setup spans; it is not device time.
- `serialize_ms`: official request serialization.
- `publish_confirm_ms`: one `basic_publish` call through its broker confirmation; this includes payload transmission, not completion of neural inference.
- `response_wait_ms`: `basic_get`/event processing until the response arrives or transport/deadline fails. Response decode, validation and fsynced storage are outside this phase.
- `close_ms`: owned reply cleanup and connection close, including local cleanup bookkeeping.
- `total_ms`: entire invocation/reconcile, including remaining local validation and durable I/O. Phase sums can be lower than total.

Cached results report `latency_kind=cached_response` with zero network phases and local read cost in total. Receive-only sessions report `recovery_only`; serialize/publish phases stay zero. Neither duration replaces the original request's inference/roundtrip latency. Previous totals alone do not establish whether fresh connection setup dominates the roughly ten-second observed calls; compare measured setup/total and publish/receive shares first.

A controlled experiment belongs in a temporary root-owned harness, never a production retry flag: choose one NEW unprocessed frame, temporarily wrap the existing `pika.BlockingConnection` factory, and replace that connection's `channel.basic_publish` only. Invoke the ORIGINAL confirmed publish once, set a one-shot guard, close the client connection, then return its original result (None may mean successful publisher confirmation). Preserve only close exception type if closing raises. Restore the original factory in `finally`.

Expected result: request becomes ACCEPTED then UNKNOWN when the closed channel cannot receive; reply queue and UUID persist, and the file cursor does not advance. Rerunning the SAME frame/epoch uses receive-only reconciliation of that exact UUID; no task is serialized or published again. A late correlated reply is committed before ACK. A foreign reply remains unacked with UNKNOWN/retained queue, rather than being discarded or treated as success. This simulates a CLIENT disconnect after broker confirmation, not an actual VPN outage. No SSH/VPN/tunnel configuration changes or duplicate TPU probes are part of the experiment. The injected publish phase includes deliberate close-handshake overhead and must be labeled as an experiment, not normal performance.

## Quality sprint: baseline audit and candidate gate

Read-only `python -m ml.linq.quality_audit --artifacts /workspace/artifacts --output <fresh-file.json>` validates baseline weights/ONNX/program/calibration hashes, inventories compiler evidence and reads selected numeric outputs. It does not inspect connection configuration or execute a model. Evidence: `/workspace/artifacts/quality/linq/baseline-audit-final.json`; CPU experiment details and SDK signatures are in `numerical-audit/`. The original model manifests/compile reports retain historical NOT_RUN flags; completed captures and journals provide later execution evidence without mutating those originals.

Pinned artifacts (full hashes are in the audit JSON):

| Model | ONNX SHA256 | TPU SHA256 |
|---|---|---|
| Helmet | `b312701494991ff7ecc82cb86cc71a8a145a871f6ff342908bb5137e1e8caa47` | `408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa` |
| Split-Pose | `802f7cb032ed525855bd271017d376fedc14bfc5789669013cae01361fa5aa00` | `c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b` |

Both use RGB bilinear letterbox114, NCHW float32 `[1,3,640,640]`, /255, O1/TPU_H1M. Helmet returns `output0 [1,6,8400]`. Split-Pose returns the four exact names/shapes above. No repeat sigmoid or neural decode; host NMS once. Both baselines calibrated on ONE public bus image (NPZ SHA256 `028d5e8325942e8a438a41396583aff1a4b14d1ac445f1e4450ace65a4d83faf`). This is a compiler smoke corpus, not representative industrial calibration or independent quality evidence.

Three saved industrial inputs were evaluated sequentially with CPU-only Torch2.9.1+cpu, ONNX Runtime1.29.0, NumPy1.26.4, SDK framework2026.9.45/quant2026.9.98; two threads, no GPU, compile or new remote call. Exact-input person class maxima:

| Saved frame | Native ONNX | SDK scaled simulation | Saved real TPU |
|---|---:|---:|---:|
| public bus smoke | .883262 | .883269 | .883269 |
| industrial-001 F0 | .630153 | .507706 | .507706 |
| industrial-001 F13 | .739911 | .326879 | .326879 |
| industrial-002 sampled F51 | .855734 | .221904 | .221904 |

Entire person-score, keypoint-XY and keypoint-confidence tensors are bit-identical between simulation and saved TPU on these inputs. Top-person anchor keypoints above .5 are respectively native→TPU 12→13,15→16,17→17. Global keypoint max remains about .994. Thus current industrial loss is person-class confidence, **not global keypoint-confidence collapse**. At cutoff .25 the last input loses all person candidates; lowering an event threshold cannot recover a detector candidate already removed by its .25 cutoff. Lowering that cutoff may expose candidates but requires FP/FN evaluation and is not a quantization repair.

Simulation vs hardware boxes differ on 265–300/33600 elements; max all-anchor difference20–20.25 input pixels, max on union(native/sim class>=.25) anchors0/3.3125/3.3125. Do not declare complete tensor parity. The exported-FP→vendor-quantized boundary is the first measured class-score divergence. Conditioned `optimized.onnx` uses custom `custom_op.tpu:swish`, rejected by stock ORT; conditioned-float parity remains unmeasured, so conditioning versus PTQ cannot yet be strictly separated. One-image calibration is a strong actionable hypothesis, not proven sole cause. The historical mixed Pose graph had a different, demonstrated zero-confidence failure and remains rejected.

Reproduce an allocated CPU diagnostic on an EXISTING input with `ml.linq.simulate --quantized <candidate>/quantized.qm.onnx --scales <candidate>/scales.json --inputs <saved>/inputs.npz --source-onnx <export>/weights.onnx --output <fresh-diagnostic> --threads 2`. Optional `--compile-report` uses explicit output-name mappings; historical reports without mappings require identical names. Hardware-aware CPU simulation is never hardware execution.

Candidate preparation is available without SDK execution:

```bash
python -m ml.linq.candidate \
  --onnx <new-export>/weights.onnx --model-manifest <new-export>/manifest.json \
  --calibration-manifest <reviewed-calibration.json> \
  --output /workspace/artifacts/quality/linq/candidates/<unique-id> --max-samples 32
```

The calibration JSON contains `samples` with `path` (numeric NPZ with only `images`), `sha256`, `source_group`, `source_sha256`, `split` (`train` or `calibration`); also `reserved_groups` and `reserved_source_sha256` covering all validation/test groups, and optional `near_duplicate_review`. Group/lineage declarations need dataset-owner review: hash checks cannot discover shared cameras, adjacent clips or perceptual duplicates. The helper rejects declared holdout leakage, tensor duplicates, hash drift, wrong numeric input and any existing output directory. It assembles the corpus and records NOT_COMPILED/NOT_RUN/NOT_EVALUATED; no package install, export, compile or remote request occurs. `--compile` explicitly delegates to existing `ml.linq.compile.compile_model`, O1, in a new `compile/` directory and is reserved for root-approved resource allocation. No second compiler/client is introduced.

Proposed bounded sequence, pending root scheduling:

1. Freeze reviewed original-video/camera/scene groups before frame selection. Use only train/calibration groups. Start 32 frames from at least 8 available independent groups, covering person distance/input size, standing/lying posture, occlusion/truncation, light/background, PPE and empty negatives. These are budget targets, not sufficient-sample claims. No val/test image may enter calibration; bus smoke alone is insufficient.
2. Prepare the same verified RGB/letterbox tensors using the existing detection preprocessor.32 float32 tensors occupy157,286,400 bytes (~150MiB), 64 about300MiB, excluding SDK activation copies. Permit 64 only after32-sample time/RSS measurement and root allocation. Keep exact graph/weights/NMS fixed for the first recalibration comparison; no simultaneous model-family/threshold sweep.
3. Current local SDK `calibrate_torch` explicitly documents activation_percentile=None and samplewise_percentile=None as max-absolute defaults; RegularModel constructor percentile defaults100. No blanket historical percentile recommendation applies. First retain defaults with representative data. Percentile changes require a separate supported, recorded hypothesis after range diagnostics; no silent TypeError retry or unrecorded option fallback.
4. Detection owner exports any separately trained checkpoint with the existing exporter and FP/native parity, and retains the reviewed pre-concat split extraction for Pose. Run allocated O1 PTQ/compile in a unique candidate directory. Validate exact ABI, finite outputs, hashes and same-input source→simulation deltas before asking root for hardware time. No compile or training was performed in this audit.
5. Freeze 5–20 labelled development goldens from groups excluded from calibration, spanning missed persons/small heads/occlusion/empty hard negatives and baseline bus diagnostic. At roughly 10 seconds per request this budgets 50–200 seconds per candidate/model, excluding upload/transfer/queue overhead. Root alone stages a reviewed candidate and executes the existing durable RPC path. Existing runtime pins must never be silently overwritten to admit a candidate.
6. Compare same tensors at every boundary, then decoded person/PPE/visible-kpt outcomes and paired labelled FP/FN/recall/precision with support counts. Numeric maxima are not task quality. Select thresholds on development/validation only; sealed independent test remains untouched until final frozen comparison. Require independent improvement without a critical-scenario regression, completed LinQ ABI/parity evidence and the full frozen bundle before promotion. Otherwise retain current baseline. Recalibration can address observed vendor-path score loss; source-model misses/ownership/scene shift require labels or model/rule work and cannot be repaired by a numeric scale claim.

Checkpoint 24 October 18:00 MSK; freeze 20:00–22:00. Deadline pressure does not relax held-out separation or convert simulated evidence into hardware accuracy. Nine focused numeric/provenance tests use tiny fixtures, not real model-quality tests.

### Allocated Helmet comparison and next candidate

The additional approved CPU-only comparison reused three saved Helmet input tensors. No export, compile, GPU or remote call ran. `/workspace/artifacts/quality/linq/baseline-audit-helmet-pose.json` contains both model audits. Bare-head class maxima (native / simulator / saved TPU):

| Frame | Native | Simulator | TPU |
|---|---:|---:|---:|
| industrial-001 F0 | .020349 | .005641 | .005641 |
| industrial-001 F13 | .130975 | .045131 | .045131 |
| industrial-002 F51 | .549676 | .330021 | .330021 |

All Helmet class-score tensors match simulator/TPU bitwise. For F51 bare-head anchors>=.25 fall 6→3 and >=.5 fall 1→0. Source-vs-TPU pre-NMS candidate xywh max difference 4.4578 input pixels; simulator-vs-TPU selected 3 anchors have zero box difference. Across all background anchors, simulator/TPU box mean absolute difference is .0163–.0209 pixels, maximum 10.03–20.06. Background extrema are not matched-object localization error. The first two native outputs already have no class>=.25, so a promise that recalibration alone will repair those examples is unsupported; annotations/visibility/source model must be reviewed separately.

Root is preparing an initial **8-frame Mendeley train-only** calibration corpus. Construction, UR and SFCHD groups/sources stay entirely reserved for validation/test; they must not be inserted as convenient calibration images. `candidate.py --max-samples 8` records per-source-group sample min/max/mean, RGB channel mean/std, sample count, source-group count, tensor hashes and corpus size (~37.5MiB for 8 images) before any development metric. These numeric statistics cannot establish scene/pose/PPE coverage or correct labels. Root/dataset owner must freeze and review group lineage and near duplicates before preparation. The 32-frame protocol above is a later allocated expansion, not work already performed.

**Review-pinned upload plan only; not implemented or executed:**

1. Preserve baseline ONNX, calibration, quantized model, TPU files, filenames, pins and completed journals. New corpus/export/compile goes in a unique candidate directory. Do not switch the runtime policy while an old request is pending.
2. After candidate compilation and local diagnostics, root reviews the full SHA256, compile report, input/output contract and candidate quality on development data. Choose a distinct literal filename, e.g. `helmet-ptq-e05-<first12-of-reviewed-sha>.tpu`; the full 64-character digest is authoritative, not its filename prefix. The candidate hash is **not yet known** because no candidate has been compiled.
3. Current `upload_agent._MODELS`, the injected reviewed staging helper, `video` factory pins and portable `jupyter` pins intentionally accept baseline hashes only. A new candidate must fail them today. After explicit root selection, prepare a new hash-pinned bootstrap with one additional literal logical candidate key+filename+full digest in the required reviewed tables; retain baseline entries. Do not add wildcard hashes, caller-selected paths, environment pin overrides or arbitrary remote URIs. Root owns staging/bootstrap/pipeline edits outside this agent's scope.
4. Test candidate wrong-hash rejection, filename/path traversal rejection, original-baseline acceptance, existing-different-file refusal, identical-file idempotence and new manifest/program mismatch rejection before deployment. A candidate must not overwrite `helmet-v1.tpu` or `pose-split-v1.tpu`.
5. Root stages the selected candidate through the same bounded user-started Jupyter helper and existing durable AmqpRunner model-upload request. Verify digest+byte-count receipt before a fresh candidate inference UUID. Run 5–20 reviewed development goldens through the existing client only; never reinterpret baseline captures as the candidate. Retain the complete baseline bundle for rollback. No app API change, extra broker client or automatic promotion is needed.

Ten focused fixture tests now cover preparation/provenance and numeric comparison; real model results above come only from saved hardware outputs plus allocated CPU evaluations.

### E03-PTQ Mendeley8: compiled, not evaluated or deployed

Root allocated this single CPU-only experiment. `ml.linq.calibration_frames` prepared exactly one zero-based `floor(nb_frames/2)` decoded RGB frame from each of the eight existing W2-10 clips, using the existing detection preprocessor. Raw RGB/preprocessed NPZ, exact frame indices/source hashes/transforms and reservations are in `/workspace/artifacts/quality/calibration/mendeley-v1/`. All Mendeley, including clips whose original names contain `te`, is now train/calibration-only. The conservative shared unknown-camera component has **one group**, not eight independent cameras. No labels, independent metrics or new source downloads were used.

Construction/UR/SFCHD/SH17 whole families are excluded. The reservation file includes known Construction image/proxy-group hashes, UR original/derived media hashes and available SFCHD/SH17 asset hashes; inventories are incomplete for the latter families, so family-wide exclusion is authoritative. No reserved-source pixels were opened. Original source files are read-only inputs.

Statistics were frozen before any evaluation: 8 samples, 1 group, 39,321,600 tensor bytes, RGB means `[.43600477,.44464802,.44258518]`, standard deviations `[.14976878,.13743987,.13425888]`. Corpus SHA256 `161c8692d1b15249762c6fcb28867c6eaf1c98f190729544d6e917015829544b`. These are numeric summaries, not evidence of sufficient visual coverage.

The existing compiler helper completed O1/TPU_H1M in 75.545 seconds, with CPU affinity restricted to two cores, Torch 2 CPU threads/one interop thread and GPUs hidden. Source ONNX and conditioned ONNX are byte-identical to baseline. The four float32 compile output names/shapes match baseline. Fresh artifacts: `/workspace/artifacts/quality/candidates/pose-ptq-mendeley8-v1/compile/`; program 2,934,603 bytes, SHA256 `0aed469bd7771348ca39c3a3d429166a74e26cb97154ca655a6491800cb67918`. `candidate-compile-review.json` pins compile artifacts and preserves quality=NOT_RUN, LinQ=NOT_RUN, runtime_abi_verified=false.

Proposed filename `pose-ptq-mendeley8-v1-0aed469bd777.tpu` and logical key `pose-ptq-mendeley8-v1` are review metadata only. No upload, staging, inference, allowlist modification or promotion occurred. Root next owns the fixed independent-development numerical/quality comparison before deciding whether to admit this candidate to the reviewed remote path. Baseline remains active.

Reproduction requires a fresh output directory and the frozen reservation metadata: `python -m ml.linq.calibration_frames --clips-root <W2-10> --model-manifest <baseline-manifest> --reservations <reserved-evaluation-sources-v1.json> --output <fresh-calibration-dir>`, followed by the existing candidate preparation and allocated compile path above. Thirteen focused fixture tests pass, including midpoint selection, whole-family exclusion and pre-decode source-overlap rejection. Those tests are separate from the actual successful local compilation and do not establish candidate quality.
