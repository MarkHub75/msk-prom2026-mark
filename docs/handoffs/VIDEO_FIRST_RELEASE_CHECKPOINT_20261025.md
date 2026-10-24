# Video-first release checkpoint — 24 October 2026

Implementation commit: `933ffa4a7acf3a3b1d08fa97c34eb4ae63e427b1` on `matvey_cv`.
528 tests passed,4skipped; actual local Argus smoke CPU408calls/event1/evidence1/
API200. Full context: VIDEO_FIRST_FINAL_20261025.md. Mark's backend/rules untouched.

Ready files for Egor and Mark:

- Full ZIP: `/workspace/artifacts/matvey-final-20261025/matvey_video_first_v2.zip`
  356979916bytes, SHA256 `07b9a84645b60c70703c7edbee443cbf386d312cec2c63acca042d39c21577d3`.
- Video preview ZIP: `/workspace/artifacts/matvey-final-20261025/matvey_video_first_preview_v2.zip`
  37749226bytes, SHA256 `cbe5ab5920072975a99d1fe9624b53a35b133e82ba2736dfee816ebc6f20bd71`.
- Expanded package: `/workspace/artifacts/matvey-final-20261025/video-first-v2/`.
  README.md, VIDEO_MANIFEST.json, SCENARIO_COVERAGE.json, FINAL_ML_EVIDENCE.md,
  MODEL_REGISTRY_HANDOFF.md, REPRODUCE.md, SCENARIO_METRICS.csv, BLOCKERS.md.
- Selected videos: demos/S04_fire/fire_positive_gpu.mp4,
  demos/S04_smoke/smoke_positive_gpu.mp4,
  demos/S02_equipment/actual_argus_cpu.mp4. Controls/failures in the same demo
  folders. PPE additional and all3S07diagnostics included.
- New normal app CPU output: actual_argus/S04_smoke/validation.json, events.json,
  evidence.json, api_readbacks.json, annotated.mp4 and own SQLite.
- New model: new_fire_model/ plus ml/models.video_first.yaml; exact smoke0/fire1,
  ref `matvey-fire-smoke-yolov8n@640-s04-v1-4c9f5d05c4d4`,local-only.
- Exact archive receipt: `/workspace/artifacts/matvey-final-20261025/matvey_video_first_v2.receipt.json`.
  Portable fresh-extraction verification:
  `/workspace/artifacts/matvey-final-20261025/matvey_video_first_v2.portable_check.json`.

FullZIP CRC and every archived payload SHA passed;621payload files,10complete
scenes/3297sourceframes/7243full-scene model calls,4models and2actualCPU app results.
Fresh extraction +stdlib verifier also passed. The old golden v1 archive digest
is unchanged. New full-video raw trees stay referenced in place, not duplicated
in the archive; DFire30raw and historicalTPU numeric captures are packaged.

These three presentation sets cover two official directions, not three proven
industrial scenarios. S04headlight falsealert is retained; S07Fall03 missed and
bedADL10 alerts, so current S07 demo is not accepted. DFire30F1 smoke.8333/fire.8966
is source-file annotation diagnostic only, not independent industrial/event GT.
NewTPU0: approved calibration and own isolated staging absent. HistoricalTPU15
calls remain historical. New Data forklift/person and cigarette candidates are
recorded but not promoted without verified Training quality/consumer agreement.

Only matvey_cv may be pushed, non-force. Git publication receipt after push lives
outsideGit next to the archive; binary off-host backup and recipient ACK are not
verified. No own model jobs or delegated workers remain active. Preexisting
.ipynb_checkpoints/ is untouched and unstaged. Next model activation requires an
actual qualified handoff or resolved LinQ gates, not a repeat of rejected work.
