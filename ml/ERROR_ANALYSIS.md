# Error analysis — measured checkpoint

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
