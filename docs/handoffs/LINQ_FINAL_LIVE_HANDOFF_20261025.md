# LINQ FINAL LIVE HANDOFF — 25.10.2026 — PRIVATE

Captain confirms the live LinQ → Argus route S28/R32 and is building demo V2.
This handoff transfers existing ML artifacts. **Do not rerun LinQ research or start
another integration stand.** Main/backend were not modified.

## Requested files, actually checked

- `matvey_final_live_smoke_runner.zip`: exact existing3-member package,11421bytes,
  SHA74737948185cacacb47a846f628ea129e0e35a3264f062df2571f0a566aec81e.
  CRC and every member SHA checked. It contains runner,main yolo_io andREADME;
  it contains no video,tail,TPU or new execution evidence. It is supplied for
  ownership transfer only,not an instruction to repeat the working captain run.
- Original producing-agent text is preserved verbatim in
  `provenance/LINQ_FINAL_LIVE_HANDOFF_20261025.original.md`. Its BLOCKED access
  describes that agent's access,not captain S28/R32 or the state of LinQ.
- `original.mp4`: unchanged Mendeley7_te4,101frames,sourceSHA
  edffc7547cd187b138e05c92440732e8ada60fe96061d90b9b0022ba4065a48d.
  Two additional unchanged MP4s used in R32 are in `videos/`; seeVIDEO_MANIFEST.
- Final local ONNX/tails,Helmet/Split-Pose compiled local binaries and source
  checkpoints are under `models/` and `checkpoints/`. Exact ModelSpecs,full hashes,
  origin and quality scope are in FINAL_MODEL_STATUS.json/.md.

## Pose640 — mandatory matching

Captain's current `pose-yolov8n@640-ap9999` uses
`/auto/cache/hackathon70007/mosprom_pose640_cut_ap9999_b1_o1_h1m.tpu`.
It emits these three float32 tensors:

| Name | Shape |
|---|---|
| `/model.22/dfl/conv/Conv_output_0` | [1,1,4,8400] |
| `/model.22/Sigmoid_output_0` | [1,1,8400] |
| `/model.22/Concat_output_0` | [1,51,8400] |

The matching tail is registered on captain's side as
`models/linq/pose640_cut_ap9999/pose640_cut_ap9999_tail.onnx`.
**That baseline tail binary and its SHA are absent in this workspace.** Keep the
matching file already used by captain. It cannot be safely reconstructed from
our different export or replaced just because both output56channels.

Our supplied `matvey-pose-yolov8n@640-v1-acc5f51228b9` tail is608bytes,
SHA23cdfe907f058713b6a617cb2230d52148eb46d508d8f809c8bb186e73615699.
It expects FOUR float32 tensors:Mul_2[1,4,8400],Sigmoid[1,1,8400],
Mul_4[1,17,2,8400],Sigmoid_1[1,17,1,8400]. Its matching local compiled program
SHA is c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b.
Historical matched replies/tail checks exist; current registered-name remote
placement is not verified. **It is incompatible with captain baseline3-output
program.** Do not replace the working pair during release.

## What to connect now

1. For the already-working LinQ demo,keep captain `det-yolov8n@640-ap9999` plus
   `pose-yolov8n@640-ap9999`,their current matching tails and transport settings.
   `config/pipeline.linq.captain.keep.yaml` states only model selection.
2. For local execution,copy the supplied `models/` tree to the Argus project
   root,merge `config/models.connect_now.local.yaml` by exactid@version,retain
   equal existing records,and apply `config/pipeline.local.stable.yaml`.
   Mark remains owner of existing user config/zones/events/delivery.
3. Fire/smoke can be shown in a separate LOCAL evaluation profile. It has
   no compiled TPU program and retains headlight/equipment false alerts.
4. Phone,Forklift,newPPE and offlineGMD heads stay experimental/inactive.
   No no_harness/suspended_load/cargo/respirator model is supplied.
   S08load_carrying remains a skeleton,not implemented by model registration.

No weights,thresholds,mappings or canonical model versions were changed.
Cache invalidation still requires a newversion if those inputs change.
JSONLs preserve originalframe_idx/ts_ms and COCO17; sidecars distinguish local
saved replay,historicalTPU and captain-confirmedlive. Nothing is interpolated.

## Verification and access

From the extracted archive root:`sha256sum -c SHA256SUMS`.
Private archive integrity,static ONNX checks and secret review are provided in
verification receipts. No runtimecredentials,.env,cookies,notebookstate or
applicationdatabase is included. Runner uses only runtimeconfiguration and the
already documented vendor-examplebrokerdefault; no private secret was inserted.

No authorized shared off-host binary destination is configured/verified here.
Download the exact files through the existing authorized Vast/JupyterLab file
browser at `/workspace/artifacts/matvey-release-final/mark-private-v1/` or the
adjacent PRIVATE ZIP. This path is local to Vast; it is not a publicURL nor a claim
that LinQJupyter sees the same filesystem. Captain can use the established team
transfer route. No public upload was made. Actual recipientACK and off-host
binarybackup remain unverified.
