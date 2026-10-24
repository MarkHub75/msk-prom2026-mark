# Error analysis — measured checkpoint

## Saved-output diagnostic follow-up (E006–E008)

No new model experiments or quality gains. E006: all4native→PTQ lostbareGT have saved same-class overlapIoU>=.5 but scorebelow.25; helmet recovers4GT; totalFP18→14 comprises9retained/9withoutcounterpart/5new. Native/float match primaryGT/FP exactly, rawfloat arrays are not bitwiseequal. Conditioning vsPTQcausality remains UNKNOWN; no threshold advice from these developmental errors.

E007 verifies originalframeIDs/384x288 geometry/nativeXMLconversion. Running46actorframes:30no decodedperson at existing.25stage,16IoU<.5,0consumer.5gate. Raising/loweringconsumerconfidence does not address the measured runningbottleneck on this saved sample. Elevenout-of-imageGTboxes arewalkingonly; they are retained, not silentlyclipped and not the explanation forrunning failure. RawpreNMS unavailable => causes belowdecoder UNKNOWN. No independentindustrialquality or originalPTS claim. Thresholds/weights/rules unchanged.

E008 validates pinned localbytes/components/historicalcorrelatedcaptures, but independentquality remainsBLOCKED and Matveyplacement/offVastbackupNOT_VERIFIED. This ledger cannot turn testcounts/booleans into modelaccuracy or independenthardwareattestation. Software417PASS; details/sourcehashes in ml/reports/night-followup-20261024.json. No candidatebudget reset.


## Night error analysis — measured limits

- E001: Native→floatONNX keeps class metrics; downstream conditioning/PTQ/simulator changes bare TP23→19 and FN9→13. Aggregate macroF1 rise hides class recall loss. Eight-image calibration did not repair it. No isolated conditioned-float control: do not claim a proven PTQ mechanism.
- E005: Removing finalconcat preserves all52float tensors bitwise, but split PTQ macroF1 drops to.327778. Anchors/names/mapping checked. Baseline has per-channel scales already, so a single combined globalscale is not the proven cause. Compiler/output-boundary sensitivity is INFERRED, not mechanistically established. Reject and preserve graphs/scale reports.
- E002: Conditional torso/detection .7890→.7869 hides missing-person increase; unconditional torso/frame .6413→.5538 exposes it. Original source quality matters. Source fall-process is neither floorlying nor episode-onset GT. One support hit cannot be advertised as a confirmed timely fall.
- E004: Partial torso reduces unknown counts without adding a true fall episode. Missing KPs cannot supply immobility. Default remains OFF.
- E003: Upstream observation/ownership is the dominant observed bottleneck:0/46knownrunning actorframes associated. Neither apparent speed normalization nor bboxanchor repairs absent observations. Missing detections remainFN, not excluded from recall. No false-alerts/hour estimate from unknown/unboxed background.
- Remaining unmeasured Helmet errors: held/neighbor helmet, hiddenhead, wearer association, small/distant heads. Existing object GT does not fully supervise them. Fall: alreadylying/work-on-floor/hardnegatives and3spositive support absent. Running: industrial gait/fastwalk/turns and approved zonepolicy absent. All require scoped independent actor-level data; no labels fabricated from clip captions.


| Evidence | Error / consequence | Decision |
|---|---|---|
| Construction sourceaudit |1416pairs/1268proxycomponents;30cross-original-split components;10orphanlabels; confirmed pretraining-source photo overlap | Entire source development-only; no independent test claim |
| Helmet corrected52/.25 | helmetTP19/FP11/FN6; bareTP23/FP7/FN9. Original thin source face/neck boxes and incomplete coverage distorted metrics | Blind versionedGT repairs; no claim of model improvement fromGTchange |
| H-HELMET-01 | .4/.5 reduce both class recalls beyond.02guard | Rejected; do not hide misses behind higher precision |
| H-HELMET-02 | tiles helmetFP11->30/FN6->7; bareFP7->16/FN9->5; macroF1.7164->.6066 | Rejected; two failed hypotheses reached; preservefullframe |
| Industrial3numeric probes | personmax .6302/.7399/.8557 -> .5077/.3269/.2219 in conditioned+PTQ/hardware. HelmetF51 baremax .5497->.3300. Simulation/hardware scores bitwise equal | Codec not blamed; original optimizedONNX customops prevent floatconditioning isolation. Newcalib candidate separated; firsttwoHelmet FPinputs alreadybelow.25 |
| NativeUR20 default |0alerts/10fallreferences;245/3274frames have no person abovebehavior.5,539more have allposturesunknown | Poorrecall established, not qualityvalidatedfall detector. Current lying requires continuous observed evidence, source tails short/truncated |
| H-FALL-01 PTQ | Baseline/candidate both TP1 FP0 FN9 at identical225frames; calibration changes do not improve the endpoint | Rejected; second failed Fall hypothesis; freeze baseline, no third tweak |
| H-FALL-02 | retainingupright duringuncertainpose alone gives same0/0/10 allframes,1/0/9 at2FPS | Rejected; OFF bydefault, no extra tuning |
| Temporal cadence |2FPSnative has1TP whilefullFPS0TP; skippedbriefunknowns changecontinuous confirmations | Samecadence mandatory in comparisons; not an accuracyimprovement |
| RealLinQUR01 |11correlatedstatus0calls,0events,1miss;2/11no personabove.5 and2/11allposturesunknown | HardwareexecPASS, recognizerqualityFAIL onthispositive |
| URsource annotations | ADL10 lies onBED, source0/1 notuniversallyfall/floorGT; all10falltails<3s | Bedhardnegative; prolongedlyingpositive support0/recallundefined; preservecoarseonsets/censoring |
| Running/Zone | Pixelmotion affectedbyperspective/IDswitches/occludedankles; no runningGTorapprovedzones yet | Prototypeabstains; no m/s/gait/publicevents/qualityclaims |

No operational false-alerts per hour are estimated from incomplete/sampled reference review. New dataset work is handed off to Data Orchestrator; no model-driven test annotations. Full sourceGT/predictions and failed experiments remain outsideGit. All errors are linked through EVAL_REPORT and EXPERIMENTS.csv.

Software diagnostic: the first merged quantized-backend fixture tests imported Torch in the Torch-free AMQP environment (4errors/319). Test-only FakeTensor adapter corrected the dependency;319tests then passed, no package installs. A preliminary SDK decoder duplicated selected frames through default CFR; its32-call run is FAILED/INVALID and excluded from all paired quality metrics. Corrected passthrough decoding pins every selected RGB hash before inference.
