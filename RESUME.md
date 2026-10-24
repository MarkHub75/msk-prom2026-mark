## VERIFIED FINAL PACKAGE — 2026-10-24

Read docs/handoffs/FINAL_RELEASE_CHECKPOINT_20261025.md first. FullZIP291139722bytes
SHA221d2fc1334d57ad3377087a93f571243c4c225506dd608867c6b97b211decc9;
preview13061488bytes. Codefab9569d,527testsOK(4skipped); portable extracted archive
515payload filesPASS. Paths/digests/limits in ml/reports/final-release-20261025.json.
ActualCPUArgus event/evidence/API1verified; no freshTPU, no independentindustrial
quality. Models frozen unchanged; subsequent work requires new actual capability
or qualified release, not another old hypothesis. No own GPU/TPU jobs left active.

## FINAL ML INTEGRATION — 2026-10-24 16:53 UTC snapshot

Latest concrete handoff: docs/handoffs/FINAL_ML_EVIDENCE_20261025.md,
MODEL_REGISTRY_HANDOFF_20261025.md and DEMO_SELECTION_20261025.md. Final package
/workspace/artifacts/matvey-final-20261025/.12full localCUDA scenes/2830frames,
8490calls including prior scenes;6180new native calls. Separate REAL Argus local
CPU job114calls/38of75frames → episode1/evidence1/event1/API200,15.855s; no UI/liveTPU
claim. Saved actual TPU raw→tail→frozenArguspostprocess→analyze15calls PASS as
MIXED replay,0episodes/0newTPU.527softwaretestsOK(4skipped),5newscenes2060inputaudit
PASS. Main f6b5358a/contract unchanged; ownstaging still absent16:53UTC. RootGPU
jobs finished/GPU0/lockFREE snapshot. Mark owns app/rules; no app code patches.
Models unchanged, no training/compile/promotion. Three demos selected S02/S07/PPE
with explicit quality gaps; S01running person localization2/168COCO,0/168Pose.
All independent target-event metrics NOT_MEASURED. Preserve old7scene/partialTPU
packs. Previous full session handoff below remains historical context.

## LATEST CONTEXT HANDOFF

Read `docs/handoffs/SESSION_HANDOFF_20261024_SCENES.md` in full. Full-scene code
checkpoint2623cabefbe3c9e83e550e5336b1df18c3a17879 is committed. Seven videos,
770full localCUDA frames,2310model calls,522testsOK(4skipped); no freshLinQ.
Closing audit15:46UTC: ownjobs0/GPU0/lockFREE snapshot. Mark's new Argus contract
pending. Session closed at user's handoff request; no automatic next experiment.

## CURRENT FULL SCENE PACKS

7full localCUDA videos/770frames/2310modelcalls COMPLETE,9owned validationtests,
522softwaretestsOK(4skipped). Best3 were forward-complete before18:00MSK; full
independent source audit after. SourceMP4 unchanged. Only11historicalUR01PoseTPU
frames; no freshLinQ (ownstaging/Jupyterabsent). S01/S04contextonly, S08BLOCKED.
Index /workspace/artifacts/matvey-scene-packs-20261024/matvey_manifest.json;
runbook docs/handoffs/SCENE_PACKS_20261024.md. Argus rules/app remain Mark-owned.

## CAPTAIN DEADLINE HANDOFF — 2026-10-24T14:03:58.123953+00:00

Latest priority: original MP4 + real per-frame LinQ detections for Egor/Mark by
24October18:00MSK (15:00UTC). Mark owns rules/zones/events/app; ML does not extend
them. Read main:docs/ML_INTEGRATION.md atf6b5358a without branch switch.
Ready intermediate v2 packages: /workspace/artifacts/matvey-egor-linq-demo-20261024-v2
(industrial522frames, actualTPU only0/13,4calls) and
/workspace/artifacts/matvey-egor-linq-urfall01-20261024-v2 (160frames,11Posecalls
at0/15/.../150). OriginalMP4 bytes unchanged; inputRGB/preprocess and rawoutputs
verified, exact decoded results and timestamps retained.15historicalactualcalls,
0freshrequests; not full inference and not independentquality. FinalArguscontract
pending. OwnMatveystaging/receipt absent; no legacyfreshsubmission or networkchanges.
Historical PIL resize differs from Argus OpenCV; exact tensors/transforms retained.
Runbook docs/handoffs/EGOR_LINQ_VIDEO_20261024.md; report ml/reports/video-handoff-20261024.json.
Existing compatible models delivery39dcc93d reused; no retraining/compile.
Pre-steering demo/feature74WIP preserved under artifacts/matvey-continuation-20261024/
deferred-before-captain-deadline, not activated/merged. Feature arithmetic initial
parity issue (NumPy1/2 scalar promotion) remains deferred, no quality claim.

# Resume MOSPROM ML/CV — saved checkpoint

## COVERAGE TECHNICAL FREEZE — 2026-10-24T12:10:24.449814+00:00

**ЭТАП ЗАВЕРШЁН; после отчёта остановиться и ждать новой задачи.** Срочная директива восьми сценариев выполнена на уровне исполняемых прототипов:8independentrules+8configs+общие context/BehaviorEngine/objectassociation/temporaldedup/EventCandidate/evidence/atomicSQLite и optinсуществующийvideo worker. ВнешнийEventMutationv1,backend/frontend,workingweights не изменены. Codecheckpoint77e019f47242d38a97adb513fbe68a76e8295309; точный последний содержащий SHA=gitlog-1. Матрица ml/SCENARIO_COVERAGE.md; запуск docs/SCENARIO_RUNBOOK.md; контракт docs/SCENARIO_RUNTIME_CONTRACT.md; summary ml/reports/scenario-coverage-20261024.json.

**480softwaretestsPASS**, /workspace/artifacts/matvey-scenarios/software-tests-release.log.24positive/negative/unknownsyntheticcasesPASS, release-acceptance-v1/coverage-acceptance.json. Неaccuracy. Все8rulemodules в ml/scenarios/rules; configs/scenarios/{01..08}.json иsuite.example. Одинtracker existingBehaviorEngine, одинsharedobjects tracker; никаких8CVengines. Missingmodel/action/visibility/policy UNKNOWN/BLOCKED. Non-syntheticfacts требуютcamera/epoch/mediaSHA+currentframe/time/source, duplicateobjectkeysquarantined. Writerlock BEFOREcheckpointrestore; legacy/candidate/state oneSQLite transaction. EpisodeUUID/revision/idempotentreplay/rollbacktested. Newcandidate typeslocalonly, неMarkHTTPendpoint.

REALPASS2: industrial2framesconsume4historicalcorrelatedLinQreplies,0newcalls/0confirmedviolation; real-replay-v1/real-replay-check.json. UR20same225savednative2FPS observations→1candidate07. fall06sevenobs→suspected_fallstart1500/confirm2500ms,readyJPEGframe75; ordinaryADL01tenobs→0, ur07-video-evidence-v1/check.json. SequentialoriginalRGB/sourceSHA/encodedPTS reviewed byteexact in encoded-evidence-review.json. ThisisnativeREPLAY, notnewTPU/industrialindependentaccuracy. CAVIAR345savednative all8rulesrun,0candidates.16Mendeleyvideos/84uniqueviewedframes:02forkliftcontexts3_tr45,7_te4,7_tr15 areREVIEWONLY, no positive/negativeGT.04haze notfire/smoking;03/05/06/08notestablished.

SELECTEDdevelopment07→02→01, **NOT3quality-qualifieddefensedemos**.07onlyrealpositive/evidence+priorPoseLinQ;02industrialcontexts+explainablepredicate butmissingequipmentmodel/policy;01actorGT/priorbackbone butR0/unknownrunningclassifier. OnlyONEnewaftercoverageE012CPUROI fixed4corners60pct, same345inputs/weights/.25/.5/.45, CPU2/CV1/600scap:1380forwards173.06s, running0/46→0/46 FAIL,walking11/482→27/482 with1oldloss; REJECT/no secondvariant/no modelpromotion. ArtifactE012-person-roi-v1, protocol265d81b9..., candidatecodecd7160b3. NewNNcalls coveragecycle1380CPU, GPU0/train0/LinQ0. Oldbaselines/failedexperiments/source data retained.

SEMANTICS: 05three separateclimb/underconveyor/undersuspendedload, notgenericlinecrossing.06harnesspresentaloneUNKNOWN; observablein_useNEG, visibleabsence/not_in_usePOS.07lying/immobility requireobservedfloor; consciousnessnotdiagnosable.01/02autoimage displacementrequiresstaticcamera+provenance. Sitepoliciesbindcamera/originalsize. Newoptinfiletimestamps ffprobeencodedPTS, noCVrelativeorigin;6_tr15offset39.028ms proof. Sourceevidence sequentialordinal, no uncheckedseek.

AGENTS completedinownworktrees: Detection118f26da+ddd8b26d(objectrules),c78732fa(screen),cd7160b3(ROI); Behavior04d7d4a0+a98a5710+0c88b073(spatial/floor/camera); LinQac3ca1fe(requirements)+read-onlycriticalreview. Rootintegratedall, nogroupedGPUjobsactive. TrainingAgentseparateworktree untouched, consumer /workspace/shared/training-handoff/ML_REQUESTS.json REQUEST_ONLY_NO_AUTOSTART pointsimmutablev2requests. GMD4foldTCN/MLP[1,24,74]heads verifiedhash/exportonly, NOTproductionselected/compiled/PTQ/LinQ; inventoryupdated. PPED/SHELdiagnosticdata nottrain/eventeval. Dataworktree/producermanifests untouched.

LIVEBLOCKERS: ownMatveybootstrapstillPREPARED/notpublished; newMatveystaging/namespace-awaremanifest required. Legacyrootcacheverifiedreceiptnotnewplacement. Sharedaccount no captainbaseline/mosprom_*_cut_ap9999*/foreignqueues/network/VPN/SSH/service changes;max1ownTPUrequest/uniqueUUID. No credentialsread/logged/shared. OffVastbackup/remoteGitauth stillunverified, no authenticationloops/forcepush/main edits. Existinglocalmodelarchive19files unchanged(validoriginalweights), unselectedGMDcandidatesnotinthatoldtar; sourcefilesretained. Preexistinguntracked.ipynb_checkpoints/untouched/notstaged; don'tdelete orclaimcleanfulltree.

NEXTonlyafternewuserdecision: Training/Data deliverimmutablequalifieddetectors/actions +blindsourcegroupGT for02/01 and07independentepisodes; activateownMatveystaging inownnotebook withoutcaptaininterference; onequalifiedcandidateLinQ+sealedtest. Do not repeatResNet,oldUR01RPCs/E001–E008/E012ROI. Thesectionsbelowarehistorical,notnewinstructions.

## FOLLOW-UP CLOSED — 2026-10-24T01:32:31.411557+00:00

**СТОП; продолжать только по новой задаче.** Пользователь возобновил работу послеf99edc8d; E006/E007/E008 завершены без сброса бюджетов E001–E005 и без NN/тренировки/компиляции/LinQ/смены порогов. Code checkpoint6b4493a5777299349579e2f3b81f898b395e21f8; точный последний SHA — gitlog-1 содержащегоRESUME. NIGHT_REPORT.md сверху содержит итог follow-up, предыдущие результаты сохранены ниже.

E006 Detection9c501234: native/float одинаковыеprimaryTP/FP, rawНЕbitwise. BaselinePTQ retains19helmetTP+recovers4, bare retains19+loses4; все4bareпотери: saved sameclassIoU>=.5, score<.25. FP18→14=9retained/9безсоответствия/5new. ИсторическийrawNPZbinding по common52order, не embeddedID; полныйaudit-v2авторитетен.

E007 Behaviorf5c92776: running46=30no decodedperson+16IoU<.5, consumer.5gate=0. Original384x288geometry/345IDs/hashes/768XMLboxes verified;188decodedboxes/KPs inbounds.11outofimageGTboxes walkingonly, preserved. Нет preNMS => причина belowdecoderUNKNOWN. Правила/пороги не менялись.

E008root2cf291d9: ml.quality.release_review сопоставляет артефакты/компоненты/историческиеcapturedUUID, использует capture_review; integrityPASS и qualityNOTQUALIFIED отдельно. Finalreview /workspace/artifacts/night-20261024/E008-release-evidence/followup-final-review.json. Никаких network/NNcalls/automaticpromotion. **417tests PASS**, software-tests-followup-001.log, testedMLcommitb85d4f84. Новые summary/13graphdata rows ml/reports/night-followup-20261024.json/.csv; figures-followup/PNG-SVG-PDF внеGit. Повторять NN/старые эксперименты/сохранённыеаудиты не надо.

READYнеизменился, consumer-onlyML_REQUIREMENTSupdated, Dataworktree/backend/frontendнеизменены. Новых eligibletrain/test/geometry нет. Всё общие LinQограничения сохранены, bootstrap НЕ опубликован/Matveyplacement НЕ выполнен, oldmanifestfreshcallsblocked. Binarymodels/архивыбезизменений, offVastbackup/remoteGitunverified, network/services/foreignqueues/captainbaseline untouched. НикакихактивныхMLheavyjobs. Следующие3посленовогодиректива: независимыйactorGT; upstreamperson/ownership+conditioned-floatisolation; validationwinner→ownLinQ→sealedtest. Не создавать работу для заполнения6часов при исчерпанныхбюджетах/отсутствииREADY.

## NIGHT CLOSED — 2026-10-24T01:22:34.026603+00:00

**ОСТАНОВИТЬСЯ после отчёта; новый цикл только по новой задаче пользователя.** Все ночные E001–E005 и software checks завершены; не повторять их. Полный итог: NIGHT_REPORT.md, текущая матрица ml/SCENARIO_COVERAGE.md, точные модели ml/MODEL_INVENTORY.md, метрики ml/reports/night-20261024.json и два CSV рядом. Код перед закрывающей документацией: b1b102bdba6bbfa1177da03a3a426a0510f36d2b; точный последний содержащий commit = git log -1 на matvey_cv.

Шесть новых гипотез, максимум2/направление: Helmet E0018-framePTQ/E005split-output; Fall E002original-vs-half-restoredEDF/E004partialtorso; Running E003H1bodyheight/H2observedbbox. Ни одного promotion/training/нового LinQ RPC. Исходные weights/TPU/пороги сохранены, optionalflags OFF. Все исходные/неудачные артефакты сохранены вне Git. Quality release НЕ ПОДТВЕРЖДЁН: независимый industrial test/cleantrain отсутствует.

Helmet SAME52dev/44complete-class: Native/float macroF1.716422,bareR.71875; baselinePTQ SIMULATED macro.741682,bareR.59375; E001.735185/E005.327778 отвергнуты. Доказано downstream class-level расхождение, механизм conditioning/PTQ отдельно UNKNOWN. E002 source320x240 vs half/restored: torso/frame.6413→.5538,UNKNOWN/missing.5418→.5975,support1/24→0/24,confirmation0/24оба; P/F1/falsealerts-hour NOT_MEASURABLE. E004 UR20same2FPS TP1FP0FN9/F1.1818 unchanged. E003CAVIAR baseline/H1/H2 TP0FP0FN3/F1=0;0/46running actorframes matched,11/528knownactorframes associated. Source development не independent промышленная accuracy; ZoneбезGT.

**397tests PASS**, /workspace/artifacts/night-20261024/software-tests-002.log. Первая попытка397 с2устаревшими staging-fixtures сохранена в001.log; исправлены тестовые пути, productionguards не ослаблены. Никаких пакетов/обучения/моделей нового сценария. Native agents Detection b26aaf74 / Behavior0082c8de / LinQb2dd3c26 интегрированы и закончили; read-only LinQ review также завершён; GPU/TPUheavy jobs нет.

Общие ограничения AGENTS действуют: не менять VPN/SSH/маршруты/firewall/services, не трогать капитанскиеbaseline/mosprom_*_cut_ap9999* и foreignqueues. Все NEW ownremote files matvey/,namesmatvey_, max1ownactiveTPUrequest. Межжурнальный admission+UNKNOWN/receive-only и собственный bootstrappublicationlock/fsync проверены softwarefixtures, sharedVPN не отключали. Исторические Helmet/SplitPose realstatus0 доказательства остаются в /workspace/artifacts/linq-rpc/;11UR01hardwarecalls исторические131.018с/.083958FPS,неrealtime. Не повторятьResNet/старыеprobes.

Bootstrap локально подготовлен/проверен, **НЕ опубликован**: /workspace/artifacts/linq-rpc/matvey-bootstrap-v1/matvey_jupyter_upload_bootstrap.zip, SHA2b1860be05e98adac98697262545e109d7a03a4703eabfe8197930493e35e2f0, ровно2helper. OwnMatvey placement ещё НЕ сделан. Старый verifiedmanifest/program_name годится для terminaloffline review, свежие вызовы блокируются. Перед следующим live этапом нужны отдельный Matvey notebook/kernel, ownstagingSHAreceipt и reviewed namespace-aware runtime manifest; не переименовывать legacyreceipt/не трогатьbaseline. См. верх docs/JUPYTER_RUNBOOK.md. Пароли/токены не передавались и не сохранялись.

Локальный model-only archive19files: /workspace/artifacts/night-20261024/preservation/matvey_models_night_20261024.tar.gz,81,683,583bytes,SHA41bdddf35b647c76d04c2994187c529bf8285f2847ca9ecb91f043a418484601; всеmembershashPASS. **Не off-Vast backup**: approveddestination/account не подтверждён; workspaceнеvolume-backed. Старый архив/checkpoints не удалены. Git remote не подтверждён: прежнийremote/pushexit128/authнедоступна, authenticationloops не повторять. Все ночные commits локальны, main/captain/forcepush не трогались. Dataworktree/backend/frontend не изменены. Графики: /workspace/artifacts/night-20261024/figures; 127строк graphdata/decisiontable в Git.

Следующие3задачи только после новой директивы: (1) frozen independent actor/episode/negativecoverage READY от Data Orchestrator, (2) ограниченный цикл upstream person/ownership/scale + conditioned-float/PTQ isolation без повтора отвергнутого, (3) лучшаяvalidationмодель→собственныйLinQ→sealedtest; одновременно внешняя сохранность послеявногоdestination. Никакого нового автоцикла. Нижние разделы — **история**, не текущие инструкции запуска.

## LATEST CHECKPOINT — ML quality sprint

Preservation update: non-force push of matvey_cv at914739090c7d5662261ed3136e2b197f5d3dee44 failed with exit128/AUTHENTICATION_UNAVAILABLE. Raw credential-bearing output was not retained. All code/metadata commits are saved locally; remote SHA is not verified. Current containing commit is git log-1. Final software check335PASS; independent test and off-Vast binary backup still open.

This section supersedes historical backend priorities and STOP instructions below. Latest user directive: models, ML pipelines and LinQ only. Separate Data Orchestrator owns new dataset search/acquisition/curation. Do not edit backend/frontend/API or /workspace/agents/data-audit. Read ml/SCENARIOS.md, PROGRESS.md, EVAL_REPORT.md, EVAL_PROTOCOL.md, DATA_HANDOFF.md and EXPERIMENTS.csv. Stages: BASELINE -> EVALUATED -> IMPROVED -> FROZEN; stop a scenario after two failed justified hypothesis families. Frozen baseline does not imply independent quality PASS.

**Helmet: FROZEN, unchanged checkpoint.** Fixed52-image quality-v3 (44 complete per class), AI-reviewed development only, confirmed upstream pretraining photo overlap. Full-frame confidence.25/NMS.45: helmet TP19 FP11 FN6, P=.6333 R=.76 F1=.6909; bare_head TP23 FP7 FN9, P=.7667 R=.71875 F1=.7419. MacroF1=.716422. Higher confidence(.4/.5) and fixed four tiles both rejected; two failed families reached. No further Helmet tuning. GT repairs are not model improvement; independent final test and event ownership remain unverified.

**Fall: FROZEN runtime baseline, quality NOT_ACCEPTED.** Native E00 all3274 original-PTS frames/20 UR clips: TP0 FP0 FN10. Source-reference GT is coarse/sampled AI-reviewed, not expert industrial test. Zero eligible prolonged-lying positives. At matched2FPS/225 frames, native and baseline vendor simulation: TP1 FP0 FN9, F1=.1818. Cadences cannot be compared as improvement. H-FALL-02 recent-upright retention gave identical results, rejected/OFF. Second and final hypothesis H-FALL-01 PTQ is REJECTED:8 fixed industrial calibration frames, unchanged source/conditioned graph, O1 compile PASS, TPU SHA0aed469bd7771348ca39c3a3d429166a74e26cb97154ca655a6491800cb67918. Baseline simulation completed225 calls/472.386s CPU2; candidate completed225calls/464.813s. Both yielded TP1 FP0 FN9/F1.1818: no gain. No candidate deployment or actual candidate LinQ. Both failed Fall hypotheses exhausted; freeze baseline as runtime rollback, quality NOT_ACCEPTED. Do not launch a third Fall hypothesis.

**New real LinQ evidence:** /workspace/artifacts/quality/pose/e00-linq-urfall01-2fps. Eleven unique correlated status0 replies; numeric journals verified; no event/one missed reference fall. Original processing131.018s (.083958FPS), RPCp50=10.630s/p95=18.967s. EOF finalization made0new neural calls. All11 input tensors bitwise match SDK-preprocessed frames;9 matched decoded people have zero score/box/keypoint-confidence difference. This proves numeric parity, not accurate fall recognition. Full native49.699s/3274frames is separate GPU timing. No VPN/SSH changes.

**Running/Zone:** offline prototype and identity-aware scorer merged (e42d6186), UNVALIDATED_PROTOTYPE, no public events or real running accuracy. Missing real GT/polygon/coverage yields NOT_EVALUATED/null. Annotation handoff: ml/quality/temporal/MOTION_EVAL.md. Official8-scenario matrix is in ml/SCENARIOS.md. New scenarios wait for suitable data. Data Orchestrator intake was read only; its branch/files were not modified. Shared compute status /workspace/artifacts/quality/COMPUTE_STATUS.json; all ML GPU jobs finished, all heavy ML resources now IDLE. New heavy jobs must coordinate and acquire shared gpu.lock.

**Checks and preservation:**335 software tests PASS after all code merges and a test-only Torch adapter fix; real client environment remains without Torch. Historical v1 temporal metrics retained; corrected v1.1 computes all-missed F1=0 while precision stays undefined. Local quality checkpoint c241c4d1 plus final merged results and metadata; use git log-1 for the final containing commit SHA. Model-only local archive84,222,307bytes/SHAe30f1034b79b6d1610c047b131693c58f15fc667c42ed4fe7c26741c45292445 in /workspace/artifacts/quality/release,24 members hash-verified. It is NOT an external backup. A Google Drive account/destination choice is pending; no rclone remotes exist. Final release/independent test/off-Vast backup are still open, not silently marked complete. See ml/QUALITY_RUNBOOK.md.

## LATEST CHECKPOINT — backend contract and controlled recovery stage

The user resumed after c8dd54a2. This section supersedes the historical video checkpoint below. Autonomous work for this stage is saved; stop after the report and wait for the user's next instruction. Actual Mark-backend integration remains BLOCKED BY MISSING ENDPOINT/SOURCE, not a claimed PASS.

Git started clean on matvey_cv at c8dd54a2, matching origin/matvey_cv. Local working tree has no Mark backend source or configured event/journal/media URL. Only origin/matvey_cv is locally tracked. GitHub connector returned 404 for remote repo access; noninteractive git ls-remote failed (return 128), without printing raw errors/credentials. The user was asked for a backend URL/branch/localpath or private config FILEPATH, never secret values. No backend information arrived before checkpoint. No VPN/SSH/NetworkManager/auth setup was changed, no push or main modification performed.

Implemented without changing models/scenarios:

- Existing EventMutation v1 retained; committed ACK schema added at ml/contracts/schemas/ack.schema.json. HttpEventSink requires committed:true, matching string event_id and actual integer revision (bool/float rejected). Its shared prepare_payload preserves the established evidence URL mapping.
- Pending/retried HTTP delivery binds receiver+media-prefix by SHA256 in SQLite. Endpoint or evidence-prefix changes stop before sending. Tokens are not part of the digest and can rotate; URLs/credentials are not persisted in delivery metadata. Legacy delivered outboxes without identity cannot be rebound while pending; use a new state-dir, do not reset delivered flags.
- ml.pipeline.backend_probe checks explicitly configured POST/ACK, duplicate same revision, configured GET-journal and exact JPEG bytes. Stable labelled test incident UUID survives restart; actual captured fixture source/model provenance is preserved. No API route guessing. report.json is the last successful check; last-attempt.json also records preflight failures. Only safe exception types are logged.
- Existing LOCAL_TEST receiver now has GET journal/latest-revision reads and transactional conflicting-body protection. It is NOT Mark's backend. HTTP COMMIT/ACK loss -> samebody retry, out-of-order journal and concurrent conflict checks are covered by tests.
- Existing LinQ client now exports connection_setup_ms, serialize_ms, publish_confirm_ms, response_wait_ms, close_ms, total_ms with finite typed allowlisting. Cache/reconcile stay distinct from initial inference. Agent commit e2555e5f merged; agent made no live calls.

Actual REAL-video client-disconnect test:

- Existing /workspace/artifacts/video-mvp/industrial-001 continued to ORIGINAL frame 13 / PTS 518.962075848 ms of 4_tr6.mp4. No completed frame 0 or earlier stock/model probes were repeated.
- First model Pose UUID 31ae5ede-0c72-40d0-acf3-bee2a960679c was published once with broker confirmation, then ONLY THIS CLIENT connection was deliberately closed. Core persisted UNKNOWN, worker exit 3, unchanged source cursor. No physical VPN outage or autossh/systemd restart was triggered.
- A fresh worker invocation reconciled SAME UUID receive-only to COMPLETED / status 0 / matching response ID. Helmet UUID 87c8c191-e314-4739-bc3f-79c2dcd31d82 then completed normally, status 0 / matching ID. Exactly 2 new model requests, no recovered-task republish, cursor advanced only after correlated results. This does not confirm a positive industrial violation.
- Evidence/harness: /workspace/artifacts/video-mvp/industrial-001/client-disconnect-check/{intent.json,injected.json,after-disconnect.json,report.json,disconnect.*,reconcile.*}. One-shot intent blocks re-injection; do NOT rerun this completed experiment. If an experiment is interrupted, inspect the saved UUID and resume normal worker instead of generating another request.

Measured ordinary Helmet call: 10429.70 ms total; setup 3286.22 ms, serialization 5.93 ms, publish+confirm 4495.98 ms, response wait 958.25 ms, close 1650.23 ms. N=1 normal sample, no p95 or chip-time claim. Whole REAL frame with artificial failure+recovery took 30052.86 ms, not normal FPS. /workspace/artifacts/backend-integration-001/performance.json records phase shares. Setup+close=47.3%; theoretical complete removal upper bound ~1.90x, NOT an implemented/measured optimization. Proposal only: persistent sequential connection/channel after backend integration and A/B safety benchmark; inspect float32 transfer, decouple slow dispatch, measure long-file export costs. Historical 0.046 FPS is repeated-image control, never realtime. Mark-backend latency is unknown.

Backend verification actually executed: /workspace/artifacts/backend-integration-001/local-contract-review.json. Configured receiver is explicitly LOCAL_TEST_NOT_MARK_BACKEND; canonical labelled prior LinQ fixture was replayed, NO new neural calls in this HTTP check. POST, committedACK, duplicateACK, GET latest journal, GET JPEG / SHA256 and probe restart passed; 1 stored revision / 1 notification. Does not verify Mark ownership, teamfrontend, remotehosting or remote push dedup. Actual external connection cannot be completed until backend endpoints/source are supplied.

Read README.md, docs/BACKEND_CHECK.md, docs/BACKEND_HANDOFF.md, docs/PERFORMANCE.md. Prepared backend command is in BACKEND_CHECK and uses explicit confirmed event/journal/media URLs; synthetic or repeated-image test events remain labelled. Authentication stays runtime-only through MOSPROM_BACKEND_TOKEN or a user-specified external config file, never source/Git/logs.

Final checks: python -m unittest discover -s tests -q -> 231 tests PASS. Tests include existing 217 plus phase/recovery, HTTP ACK loss after commit, stable destination, typedACK, probe/journal/evidence, one-shot diagnostic guard and concurrent conflicting revisions. Root fixed review findings: early preflight failure cannot leave stale latest PASS, and TEST receiver immutable check is serialized. Native agents completed, no active delegated tasks. Sourcevideos/models/rawruntime/secrets remain outside Git; artifacts retained, server left running. Latest root integration commit: git log -1 on matvey_cv.

Next action requires user/team data: actual POST URL, journal URL/response shape and evidence prefix, or Mark backend branch/localpath and startup instructions. Keep the prepared source/payload; do not invent another backend, retrain or repeat completed network/model experiments. Real industrial positive/fall/lying quality and real VPN auto-recovery remain unverified. Stop here.

## Previous video checkpoint (historical)

## LATEST CHECKPOINT — video MVP iteration

The user explicitly resumed after 0c4cb5ff and requested the video MVP. This section supersedes ALL old pause instructions and pending statuses below. At the end of this iteration stop and wait for the next user decision; do not start new features, research, training or experiments automatically.

Functional file MVP implemented using existing components: verified runtime manifests -> original frame IDs/FPS/PTS -> RGB preprocessing -> sequential real Helmet/Split-Pose AMQP calls -> decode -> existing tracking/temporal rules -> event revisions -> exact-frame evidence -> SQLite outbox -> existing HTTP COMMIT/ACK adapter. No GPU fallback, training, recompilation, VPN/SSH/NetworkManager changes or source archive edits. The main PyTorch environment was not changed. OpenCV 4.10.0.84/jsonschema 4.26.0 were added only to /workspace/.venvs/linq-client.

Actual runtime evidence is outside Git in /workspace/artifacts/video-mvp/:

- industrial-001: REAL 4_tr6.mp4 frame 0 / PTS 0; both models status 0,1 person, no helmet/bare_head output. Frame cycle 21481.22 ms; no confirmed episode. Correctly abstains.
- industrial-002: REAL 4_te5.mp4 frame 51 / PTS 2009.607564ms; both models status 0, bare_head 0.3300206, no detected person. Frame cycle 21883.31 ms; no owner/track and no event. Correctly abstains. Neither negative result proves compliance.
- repeated-image-control-001: EXISTING reference.avi is a repeated public still image, explicitly source_kind=repeated-image-fixture / camera CONTROL-FIXTURE-NOT-INDUSTRIAL. 6 frames,12 unique real LinQ RPCs, all matching IDs/status 0,1 missing_helmet incident,2 revisions (open/interrupted EOF),1 snapshot,1 notification in a LOCAL TEST HTTP receiver. This is integration evidence, not a real industrial positive or quality evaluation.

Control performance: 131.7587 s / 6 frames = 0.04554 processed fps; frame-cycle p50 = 22.1603 s, p95 = 25.6389 s; RPC p50 = 10.6766 s, p95 = 13.7390 s including connection/setup/wait/close. Source 5 FPS, requested sample 2 FPS -> actual PTS 0/600/1200/1800/2400/3000ms. Event 94a4106e-87d0-4de8-8e99-5fcd4b41caf7 confirmed on original frame 12 at 2400 ms. Evidence JPEG is evidence/ff39a481-0876-48d9-aac4-f0fe5f6ceeda.jpg. No real-time claim.

integration-review.json verifies event JSON Schema, RPC correlation, source-frame/PTS/RGB/JPEG evidence hashes and real loopback HTTP POST/ACK/GET. resume-review.json confirms cached restart with 0 new RPCs, 12 journals before/after, immutable events.jsonl and1 notification. Cache-invocation timing is separate from original processing metrics. Empty event sets are NOT_EXERCISED for evidence HTTP; historical pre-fix reports are preserved in the negative runs. Source/runtime videos, secrets and model binaries were not added to Git.

Runtime state: video-session.json pins source/config and stream_epoch; requests/<UUID>/ holds numeric inputs/results and intent; rpc/<model>/<logical-hash>/ maps frame/model to transport UUID. SQLite commits observation, video cursor, behavior checkpoint and outbox together. UNKNOWN pauses the SAME frame, exit 3; repeat the same command after network restoration to receive the old response. Only durable NOT_SUBMITTED permits a fresh UUID; cross-model fence and worker lock bound submissions to one. Terminal service errors are gaps, contract errors stop without advancing. Already completed runs make 0 new remote calls. Actual VPN interruption was not provoked; recovery is covered by fault/crash tests.

Commands:

```bash
# Existing verified integration fixture: repeats reuse completed results.
bash /workspace/project/scripts/linq_video_mvp.sh \
  --source /workspace/artifacts/integration/reference.avi \
  --source-kind repeated-image-fixture \
  --camera-id CONTROL-FIXTURE-NOT-INDUSTRIAL \
  --state-dir /workspace/artifacts/video-mvp/repeated-image-control-001 \
  --sample-fps 2 --end-ms 3200 --demo-policy --local-test-sink

# New real industrial file; requires a different state directory.
bash /workspace/project/scripts/linq_video_mvp.sh \
  --source /path/to/industrial.mp4 \
  --state-dir /workspace/artifacts/video-mvp/camera-01 \
  --sample-fps 2 --local-test-sink
```

--demo-policy is explicit min_score 0.25 with unchanged keypoint 0.5 and strict ownership. Defaults remain 0.5 and confirmation 2000 ms / max_gap 750 ms. No thresholds were reduced to force an industrial event. Existing real-video bounded GPU comparisons are labelled NATIVE under /workspace/artifacts/video-review/, not service execution. No suitable sustained industrial positive was established in that finite sample. Positive industrial missing-helmet and positive fall/lying hardware-video acceptance remain OPEN; default confidence policy also needs labelled evaluation.

Backend/frontend handoff: docs/BACKEND_HANDOFF.md and docs/VIDEO_MVP.md; original schema ml/contracts/schemas/event.schema.json, clearly synthetic docs/examples/event.synthetic.json. New optional source_kind/evidence.media_time_ms are backward-compatible v1 fields. Mark's actual backend and permanent evidence hosting are NOT integrated. Local EventSink is a labelled loopback TEST service with committed ACK, stable revision dedup and one notification; it closes after each bounded command. Use a separate state-dir for real backend: already ACKed local-test rows are not automatically resent to another endpoint.

Agents completed in separate worktrees: Detection a6597683 verified manifests +real-video selection; Behavior c654d9ab captured-output acceptance and conservative sampling guidance; LinQ 9a5e5d45 durable per-frame factory/backend pending provenance. Root owns sharedcontracts/fileworker/HTTPtestreceiver/evidence/integration docs. No active delegated tasks remain.

Final verification: python -m unittest discover -s tests -q -> 217 tests PASS. Includes actual-capture ABI checks, behavior replay, pending/UNKNOWN/cached/mismatched requests, SQLite rollback, source epoch/cursor restart, one episode/revisions, evidence PTS and real loopback delivery. Live total this iteration: 4 RPCs across 2 real industrial frames + 12 RPCs in labelled integrationfixture; cached repetitions 0 new calls. Do not repeat these completed TPU checks. Latest integration commit: use git log -1 on matvey_cv; no push performed.

Remaining decisions for next authorized stage: provide/review a suitable positive industrial clip and address model domain/quantization quality; connect Mark's real event/media endpoints; validate fall/lying, end-to-end alert latency and controlled live reconnect on appropriate video. This iteration stops here; artifacts/server remain intact.

## Previous model-RPC checkpoint (historical)

Stock automatic Vast->LinQ ResNet50 has actually completed and passed capture integrity/class checks. Results are /workspace/artifacts/linq-rpc/resnet50-001/; do NOT repeat this job. Official pure-Python format source is /workspace/linq-client/tpu_pycloud_format, user-confirmed version0.0.1 with reviewed hashes at /workspace/artifacts/linq-rpc/format-source.json. Use /workspace/.venvs/linq-client/bin/python with PYTHONPATH=/workspace/linq-client:/workspace/project. Runtime config is /workspace/linq-client/connection.env; never print/commit its values.

OWN MODELS SUCCEEDED ON LINQ. User started the bounded Jupyter helper. Both uploads completed with matching remote SHA256: Helmet 2,751,596 bytes / request adcc0b06-5767-45c6-851a-9bd6b5b7e593; Split-Pose 2,929,222 bytes / request ee97f734-5132-4278-a5ce-ee35ef077251. Receipts are /workspace/artifacts/linq-rpc/{helmet,pose-split}/staging-receipt.json. Do not upload again.

Exactly one real inference per own model completed:

- Helmet request 262bdaa1-c24b-48ac-b073-6b28fd014248: status 0, matching response ID, float32 [1,6,8400], full call 10234.49 ms. /workspace/artifacts/linq-rpc/helmet-001/ contains capture/inputs/outputs/response/integrity/comparison/detections/model-check. Smoke PASS: 2 bare_head detections at 0.352586 / 0.259503. The float reference has 1 detection, matched at IoU 0.925226; 1 extra actual detection. Coordinate/class/confidence checks PASS. This is not target-video quality validation.
- Preferred Split-Pose request 1f986b07-896d-48b9-8b4f-6ce2d0f8dc16: status 0, matching response ID, four expected float32 tensors, full call 11152.85 ms. Same artifact set under /workspace/artifacts/linq-rpc/pose-split-001/. Smoke PASS: 3 persons, matched IoU 0.7812..0.9108; visible keypoints 16/17/9, confidence preserved. Original mixed pose still excluded.

scripts/linq_models_auto.sh all is resumable: completed captures are locally reviewed/reused, not resubmitted. Pending UUIDs reconcile receive-only. Do not rerun a completed TPU job. Next project stage is wiring this verified remote transport into the existing video-worker/backend integration; these single-image probes do not claim end-to-end video quality/performance. Historical packaged manifests remain unverified templates and are not automatically promoted to production bindings.

Network steering: user is moving Arch SSH bridge to autossh/systemd because VPN can drop. Do not change SSH/VPN/NetworkManager from Vast. Durable RPC core 7f705a32, CLI/capture followup 474afee8 and durability fix 97a7a5d2 are merged: fsynced intent/context BEFORE network, UNKNOWN after possible submission, retained reply queue and receive-only reconciliation; terminal tensors saved BEFORE ACK. Both real uploads and inferences used this core; the last fix additionally retains replies if final fsync is uncertain. Root added cached/pending capture resume and concurrency/request locking. Own-session heartbeat 5 s bounds failure detection; Pika blocking RPC/close may overrun the polling deadline, so 60 s is not hard wall-clock cancellation. Missing response never licenses a blind repeat. Previous full suite (160 PASS) was not repeated. No additional network probes or ResNet calls.

## Final checkpoint — iteration closed at the user's request

STOP after the final report. Wait for a new user instruction; do not automatically start any following task, research, experiment or agent. LinQ agent completed its work and review; Detection/Behavior agents have no active tasks. No server was stopped and no artifacts were deleted.

Implemented: pinned automatic Jupyter file staging through a distinct explicit consumer; existing official AMQP client with unique UUIDs, bounded waits, durable intent and selected numeric response; receive-only/offline recovery; duplicate suppression and deployment locking; numeric capture, integrity review, ABI checks and model decoding/comparison. The real service returned successful correlated responses for both models. Full-call latency is separate from recovery/cache time.

Final checks: 20 affected AMQP + 17 recovery tests passed in the isolated LinQ worktree; 13 deployment/recovery tests passed in the integration worktree after merge. Total: 50 affected checks PASS, not a rerun of the full project suite. git diff --check is clean. Runtime artifacts and private configuration remain outside Git; the final integration commit contains code/tests/docs only. Use git log -1 on matvey_cv for that checkpoint's exact hash.

Known limits: Helmet produced one extra detection relative to the float smoke reference. These single-image tests do not establish target-video accuracy or throughput. Actual VPN-loss recovery was not exercised on the live service; fault/crash recovery was checked with targeted tests. Blocking Pika operations can exceed the polling deadline while heartbeat detects loss. Historical packaged manifests remain templates rather than automatically approved video-worker bindings. Backend/frontend end-to-end integration is still pending.

Next three priorities, ONLY after the user explicitly resumes:

1. Bind the verified Helmet/Split-Pose remote transport to the existing video worker with per-model ABI/identity and durable request context; preserve UNKNOWN semantics, with no automatic GPU fallback.
2. Connect real backend event delivery, evidence, notifications and journal; verify persisted ACK and idempotent event revisions across the full MVP.
3. Evaluate target-video detection/behavior quality, latency/throughput and controlled reconnect recovery; keep the extra Helmet detection and quantization differences visible in acceptance reports.

The sections below are historical snapshots. Their old pending statuses and instructions are superseded by CURRENT STATE and this final checkpoint.

## Earlier start instructions (historical)

Continue the approved implementation; do not restart research or model selection. User requested this checkpoint because remaining usage is low. Resume only when the user returns. Do not spawn new work merely from reading this file.

Repository /workspace/project; integration branch matvey_cv. Read AGENTS.md, docs/TASKS.md, docs/ARCHITECTURE.md and this file. Check git status first. Never modify main, commit source videos/secrets/research archive, or share credentials between agents.

## Implemented and verified

- Previous baseline 118e068b: video ML-worker, shared contracts, helmet + split-pose, behavior rules, snapshots, durable SQLite outbox/checkpoint, HTTP committed ACK, actual compiler programs, SDK simulation, 61 tests.
- Current continuation adds AGENTS.md, architecture/task register, stricter consistent wire validators/schemas, ready-evidence delivery fixes, captured-output comparator, deterministic behavior acceptance fixtures, safe Jupyter call capture, and independent capture-integrity review.
- Last full test: `python -m unittest discover -s tests -q` — **96 tests PASS**. Includes mock call capture -> integrity review -> numeric comparator; tampered artifact, invalid tensor manifest, failed call and wrong program hash rejection.
- CLI replay of 8 synthetic acceptance scenarios: 101 observations, 7 incidents, 12 revisions; backend label synthetic-test, pending outbox12, no actual backend deliveries. Artifacts /workspace/artifacts/behavior/orchestrator-acceptance and orchestrator-events.jsonl/orchestrator-summary.json.
- No real TPU capture has been obtained by the orchestrator. No target-video accuracy or real backend/frontend integration claim.

## Actual agent stages

All three native agents were really resumed in separate Git worktrees and completed their coding tasks. They are not currently background workers. Root reviewed/merged their branches into matvey_cv. If a fresh session has no agent objects, spawn replacements with the same isolated ownership only after user resumes.

| Agent | Worktree / branch | Completed stage | Last relevant agent commit |
|---|---|---|---|
| CV Detection | /workspace/agents/detection / agent/detection | CV-02 named NPZ comparison, explicit runtime-to-reference mapping, decoded pose diagnostics; 14 owned tests | 133ea22e |
| Behavior Analysis | /workspace/agents/fall / agent/fall | BH-02 8 synthetic scenarios, restart/replay/ACK-loss acceptance; fixed duplicate equal-gap tracking-generation reset; 30 owned tests | 50dd2f65 |
| LinQ Integration | /workspace/agents/linq / agent/linq | LQ-01 one-call safe notebook capture + manual Jupyter runbook; 31 owned tests | fd5adcbf |
| Root | /workspace/project / matvey_cv | Shared validation, review/merge, capture integrity/comparison integration; 96 combined tests | See git log |

/workspace/agents/speed / agent/speed remains reserved and inactive. No same-worktree concurrent editing.

## Most recent new interfaces

- `ml.linq.notebook.capture_call(run, *, inputs, output_names, program_path, output_dir, model_id, input_specs=None, output_specs=None, runtime_to_reference=None, original_transform=None, expected_class=None, placement_attested=False, max_bytes=...)`.
- Invokes explicitly supplied callable once. New directory contains capture.json, inputs.npz, outputs.npz. No notebook/session/environment/auth dumps. Error messages are reduced to phase/type. Hardware independently_verified always false.
- `ml.pipeline.capture_review.review_capture(directory, expected_program_sha256=None)` verifies completed status, program identity if specified, file hashes, numeric arrays, per-tensor hashes/shape/dtype/nbytes. Hash consistency is not independent hardware proof.
- `ml.detection.compare_capture.compare_captures(reference, actual, runtime_to_reference=None, manifest=None, metadata=None, ...)` returns COMPARED/INVALID_CAPTURE, never hardware/target-quality PASS. CLI `python -m ml.detection.compare_capture --help`.
- `python -m ml.behavior.scenarios --output-dir PATH` writes observations.jsonl + expected.json. Synthetic only.

## LinQ access truth and next priority

The USER CONFIRMS authenticated LinQ Jupyter access and stock example.ipynb with a ready ResNet50 TPU program. This session is not exposed through tools to the orchestrator. Vast still fails DNS for hackathon.lin-q.ru and has no /dev/net/tun/OpenVPN; that does NOT negate user access.

The earlier async question was answered when the user resumed: stock example succeeded with status_code0, class257 and response0.39s. This result is user-reported; numeric tensors and the actual call source are not yet captured locally. Do not ask for passwords/tokens.

Priority1 on resume:
1. Read docs/JUPYTER_RUNBOOK.md. User runs the inspected supplied example in their existing Jupyter session.
2. Bind capture_call to the ACTUAL existing notebook inference expression; the runbook intentionally has guarded placeholders instead of inventing remote API/variable names. If adaptation is needed, request only manually cleaned preprocessing/call code, no auth/source secrets or notebook outputs.
3. Export only capture.json, inputs.npz, outputs.npz. Transfer into a user-chosen directory outside Git, e.g. /workspace/case/linq-capture/.
4. Verify via `python -m ml.pipeline.capture_review --capture PATH [--expected-program-sha256 SHA]`, inspect actual supplied API, then compare numeric outputs against the matching reference. User attestation/correlated completion and integrity checks must not be described as independently verified chip placement.
5. Then test own helmet and preferred split-pose programs on real TPU, verify runtime ABI/codec/name mapping. Do not flip runtime_abi_verified without this.
6. Connect actual team backend/evidence hosting, then measure full-chain latency and independent target-video precision/recall.

## Earlier checkpoint packaging task — now completed

At the earlier checkpoint the small kit had not been built. This task has now been completed; see the latest resumed-work section below and docs/validation/jupyter-kit.json. Do not rebuild models or repeat prior research.

Existing `/workspace/artifacts/linq-handoff.zip` (~65MB) is the earlier model/compiler handoff from previous baseline. It contains helmet + split-pose TPU programs, golden references, vendor ResNet50 assets and earlier source. It does NOT contain latest capture/review/comparison helpers. Its prior SHA256 is in docs/validation/2026-10-23.json.

## Existing model/artifact evidence

- /workspace/artifacts/detection/{helmet,pose,pose-split}/: weights, ONNX, manifests, golden/parity and comparison reports.
- /workspace/artifacts/linq-sdk/{helmet,pose,pose-split}-compile/: actual TPU programs, compile reports, quantized models/scales and SDK simulation.
- Original mixed pose is REJECTED: PTQ zeroed all keypoint confidences.
- Corrective split-pose extracts boxes, class scores, keypoint XY and confidences BEFORE mixed Concats; float output bit-identical on smoke image. SDK simulation preserves confidences; 3/3 decoded people. One-image calibration only, not quality validation.
- Preferred split program SHA256 c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b.
- Helmet program SHA256 408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa.
- Compiler env /workspace/.venvs/linq-sdk; preparation env /workspace/.venv-cv-prepare; existing main PyTorch env unchanged.

## Persistence and limits

/workspace is NOT volume-backed. Local commits and artifacts survive stop/start but not recycle/destroy. No remote push or external backup has been performed in this continuation. Preserve repository/artifacts outside the instance before recycle/destroy. No raw video, credentials, model binary or research archive has been newly committed.

## Latest resumed work — portable kit

User reports successful stock example.ipynb: status_code0, class257, response0.39s. Recorded as user-reported service execution; selected numeric capture still pending. Built /workspace/artifacts/linq-jupyter-kit.zip (~9.5MB), including current code, instructions, runtime-only dependencies and existing Helmet/Split-Pose programs plus golden arrays. See docs/JUPYTER_KIT.md and docs/validation/jupyter-kit.json. LQ-02 helper from56a3d13f merged.113 tests passed; extracted kit imported in isolated Python and both prepare_case calls passed.

The actual remote notebook import/call/result extraction has NOT been provided. An async request for cleaned code was issued, without credentials, but no snippet arrived before packaging. The archive explicitly marks NOT_PROVIDED_YET; bindings.py refuses requests until filled. Do not call the public LOCAL pytpu reference the organizer remote API. No own-model hardware execution has occurred. Next: receive that cleaned fragment, bind the actual successful service API, update the kit, capture stock + Helmet, inspect integrity/ABI/decoded results, then Split-Pose. No training or model regeneration is needed.

Quality checkpoint completion note: all335 tests passed; agents completed, heavy processes idle. This is a frozen runtime/measurement checkpoint, NOT an independently validated final ML release. Remaining dependencies: Data Orchestrator real episode GT/heldout source test and explicit external backup destination/account. Preserve failed experiment artifacts and baseline binaries. No new Helmet/Fall experiment is authorized by this iteration after two failed hypotheses each.
