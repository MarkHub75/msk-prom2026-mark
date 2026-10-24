## Video-first final integration — 2026-10-24 19:31 UTC

Current package: `/workspace/artifacts/matvey-final-20261025/video-first-v2/`.
See `docs/handoffs/VIDEO_FIRST_FINAL_20261025.md` and
`ml/reports/video-first-final-20261025.json`. Main f6b5358a and its ML contract
remain unchanged. New real pretrained smoke0/fire1 model is integrated locally;
no training or new TPU execution. Seven new full scenes:2648frames/5296calls
(3966GPU,1330CPU). Selected package includes three prior scenes:10/3297/7243.
New actual Argus CPU smoke job:408calls,204/407frames/model, event1/evidence1,
API200,48.434s. No app/rule/backend changes. Source DFire30 detector F1 smoke.8333,
fire.8966; overlap/exhaustiveness UNKNOWN, not independent industrial/event GT.
Fire headlight false alert retained. Current S07 Fall03 missed/bedADL10 alert;
not accepted as a successful fall demo.528testsPASS(4skipped). Latest Data
research forklift/person and cigarette ABI candidates are recorded, not promoted.
All assigned agents completed; no own compute jobs. No new automatic experiment.

# Dataset card — quality-v1 (intake)

No target-site holdout or expert-adjudicated event GT was supplied. Dataset authors' labels, AI visual audit, calibration material and independent evaluation are distinct provenance layers.

| Source | Current evidence / role | Rights and semantic gate |
|---|---|---|
| Construction-PPE local snapshot |1416 paired images, original1132/143/141train/val/test;10 orphan labels quarantined.52fixed source-val images;44complete/class afterversionedblindAIreview; confirmedsamephoto overlapwithpretrainingsource | Internal AGPL-3.0 notice; upstream photo rights/completeness unknown. Object/part labels, not person-state truth. Provisional annotation benchmark only until QA |
| SH17 | 20IDs frozenbeforeinference;13/20filesobtained; handedofftoDataOrchestratorwithnoGT/modeltest | README NC-SA/Zenodo NC differences and individual photo rights must be retained. Head is not automatically no-hardhat; off is not a violating wearer |
| Roboflow Construction Site Safety | Baseline keremberke card pinnedCCBY4.0; sourcevalid3962images boundedoverlapaudit completed | hard-hats-fhbh5/2 confirmed; same-photooverlapwithConstruction; trainarchiveuninspected |
| Mendeley xjmtb22pff/1 |8actualindustrialvideos(~156MB); ENTIREsource calibration-only; exactly8midpoints used; notcamera-hours/test | Dataset CC BY4.0 per prior primary audit; no episode/box GT implied by video labels. Camera grouping and policy geometry must be reviewed |
| UR Fall | 20cam0 videos:10fall+10ADL,3274frames59unknown; rightRGBpanelderivedwithPTS | Noncommercial academic NC-SA restrictions; one conservative camera/source group, development only. Posture -1/0/1 is not automatically our event taxonomy |
| OmniFall | Primary card/repo/temporal annotations audit, no bulk acquisition | License header/body conflict and separate source-video rights; cross-domain source/component split required |

Data lives in /workspace/datasets/quality and /workspace/artifacts/quality. Source images/videos, full annotations and predictions are not committed. New sourcework/curation afterthelatestdirective is ownedbytheseparateDataOrchestrator; thiscard/CSVareexistingintakesnapshots. Dataset CSV stores provenance/checksums/grouping, not identifiable media. Any redistribution, training or external display beyond the verified licence scope remains gated.

## Immutable producer handoff used during the night

Only `/workspace/shared/dataset-handoff/READY.json` entries with matching release manifest/file hashes and exact approved use were consumed; no Data Orchestrator worktree changes/merge/search/download.

| Release | Approved role and limits |
|---|---|
| SHEL5K diagnostic19/v1-20261024 |19images/312sourceobjects;8rawperson UNKNOWN; CC BY-NC3.0. Parser/geometry/QA only, not training, independent test or public employee imagery |
| Mendeley replay16/v1-20261024 |16videos/3112frames, source already calibration-known, CC BY4.0; replay/import/calib preparation only. No actor/event/zone GT |
| EDF native source3/v1-20261024 |3original320x240MP4/12917frames,24nativefall-process positive windows. Originalmedia/nativeGT CC BY4.0 via producer primary-source audit; staged air-mattress, fullfamily development. +/-1frame origin uncertainty; complementUNKNOWN. Not floorlying/immobility or industrial finaltest |
| CAVIAR source3/v1-20261024 |1713JPEG/3XML, literal227running/2451walking annotations; visible226/2431 afterappearanceexclusions. Sharedcamera/actors development, sourceBY-SA versionunspecified. Localresearch only; originalJPEG ordinal*40ms nominaltime, not originalPTS; unboxed/otherstatesUNKNOWN |

Root CSV adds release-level metadata references only, not copies of producer's individual asset records. Full verified assets/splits/checksums remain in each immutable release. No independent test or clean complete training release arrived; no training performed. Historical Helmet semanticdigest39e13... is not serializedGTfileSHA346f74...; current fields distinguish both.

## Received weak-video training release — 24 October, continuation

The immutable GMD weak-video release is now consumed with a separate schema-aware
verifier: 160 media files and 34,172 pinned clock rows, train123/val37, no test.
Only VIDEO_WEAK_LABEL_CLASSIFICATION is approved; labels are whole-video source
ADL/Fall categories, with zero new HUMAN_VERIFIED event/bbox annotations.
CC BY4.0 attribution and restrictions remain pinned. Root rechecked bytes and
exact cross-split media/RGB digest equality from clocks, without fresh decode.
270 producer pHash candidates remain unresolved; physical actor/camera independence
is UNKNOWN. Subject folders1/2/3 train,4 validation; all derivatives stay together.
New adaptation is a data capability, not authorization to start training. Existing
four-head retraining is forbidden. Details: reports/intake-20261024.json.

## Complete scene-export inputs, 24 October

Seven already available MP4 inputs were exported without changing bytes: five
Mendeley factory clips and two URFall lossy RGB-crop previews. All770frames were
forwarded through unchanged Pose/Helmet/COCO80-reference weights, with sourceSHA,
encodedPTS/RGB/input checks. This creates model proposals, not new GT. Entire
Mendeley family is calibration-known; UR remains source-development/academic
NC-SA. No independent final test or new source acquisition. Producer READY roles
were rechecked after the runs; each selected source SHA was checked before its
forward. Partial specialist/action coverage remains UNKNOWN. Paths and precise
rights/limits: docs/handoffs/SCENE_PACKS_20261024.md.
