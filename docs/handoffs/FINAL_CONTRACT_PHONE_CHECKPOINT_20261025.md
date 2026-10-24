# Final contract and Phone release checkpoint

Implementation commit `fae4c444fd56219951433fde335d7b0659722810`, branch matvey_cv.
Tested unchanged Argus main434b0f75/v6.528softwaretestsPASS,4skipped,7.485s.
Root contract/handoff: docs/ML_HANDOFF_MATVEY.md. No src/main/backend edits.

Ready files:

- Full ZIP `/workspace/artifacts/matvey-final-20261025/matvey_contract_phone_v1.zip`
  558485921bytes, SHA256 `4578c04e617cd21f947fb588b513b9dbe71ccbd8712f43d9a8b629c2283daa70`.
- Preview `/workspace/artifacts/matvey-final-20261025/matvey_phone_preview_v1.zip`
  72308778bytes, SHA256 `1a733b8e580d197490051b71ab0996d8bf4a4f1d263fe7c3b2a7b9e51eae1b80`.
- Expanded `/workspace/artifacts/matvey-final-20261025/contract-phone-v1/`.
  README.md, MODEL_REGISTRY_HANDOFF.md, config/, MODEL_REGISTRY.json,
  VIDEO_MANIFEST.json, SCENARIO_COVERAGE.json, METRICS.csv, verify_bundle.py.
- Current ModelSpec/pipeline handoff in Git: ml/models.matvey.yaml,
  ml/pipeline.matvey.yaml, ml/pipeline.matvey.phone.experimental.yaml.
- BestPhonePT71154817…, productONNXd15369d2…; exact sourcephone0/face1→
  product0cell phone; nativeargmax preserved beforefilter. Experimental record
  matvey-phone-object-yolov8n@640-contract-v1-7115481796de is default-INACTIVE.
- Phone videos: scenes/gmd-subject4-adl02/annotated.mp4,
  scenes/meva-g506-phone-action/annotated.mp4,
  scenes/meva-g331-document-control/annotated.mp4,
  scenes/mendeley-4-tr13-unlabelled-context/annotated.mp4.
  Sources, three exactJSONLs, native/scenePTS and allframe provenance included.
- FP illustrations: metrics/hard_confusors/results/annotated/241_Phone_candidate.jpg,
  443_Phone_candidate.jpg; source-label confusions, not industrial eventGT.
- Actual CPUdemo build pack: argus_demo_CPU/manifest.json; imported real app
  event/evidence/API/SQLite proof: argus_demo_CPU_proof/validation.json.
- Sparse15historical TPU JSONLs are clearly separate. FreshTPU0.

348payload files verified offline and allZIPpayloadSHA read back.6ModelSpec
records(5uniqueweightmodels plusdiagnosticCOCOalias),4newGPUscenes/1539frames/
4617calls;6CPUdemo videos/6060calls,6cachedjobs/event5/evidence5/API200. Normal
smokejob816CPUcalls. Additional127GPUCOCOval/30CPUfireval/24CPUhardcontrols/
1PhoneCPUprobe; total11675newrealcalls in this contract+Phone turn,0newTPU.
No raws duplicated:7.26GB video payload stays at immutable RAW_REFERENCES paths.
Old v1/v2 archives remain unchanged; no off-host binary backup is verified.

TrueCOCOFPI127 TP16/FP6/FN51,F1.35955 vsPhone49/12/18,F1.765625. This is
source validation, not independent industrial quality. Video transfer weak:
only1candidateframe>.30;actualArgusphoneevents0forbothprofiles. Hardconfusors12:
COCOphone0,candidate3(highconf remotes+hand). Candidate frozenEXPERIMENTAL,
stableCOCO/Pose/Helmet preserved. No new ROI/confidence/960/training cycle.

Sourcephone/bbox/eventGT and valid industrial negatives are limited. GMDhint
notGT;MEVAdocument actor coexists withphoneactors;Mendeley notnegativeGT.
S08load_carrying mainplugin is skeleton/NOT_IMPLEMENTED;no8implementedclaim.
LinQstaticcuts/tailplan exists,compile/PTQ/liveadmission remainsCLOSED.

Final push is non-force matvey_cv only. Exact remote release SHA/publication
receipt is saved outsideGit next to the archives after push. Shared local notice
is not recipient ACK. All Data/Training/LinQ delegates completed; no model jobs.
Preexisting .ipynb_checkpoints/ untouched/unstaged. Next model work requires new
qualified data or explicit task; no automatic extra variant from this checkpoint.
