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
