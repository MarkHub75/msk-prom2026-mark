# Behavioral models and video data — canonical evidence base

Topic `behavioral_models_video_data`; context `mosprom-research-v1`. This file contains normalized decision records and detailed evidence dossiers from all sixteen W1 and seven W2 tasks. The collector performed local reading, synthesis and integrity checks only. No third search wave, neural inference, training, export, compilation or LinQ execution occurred. Exact source identities are in [SOURCES.md](SOURCES.md); branch aliases are mapped in [_WORK/ID_MAP.md](_WORK/ID_MAP.md).

<a id="F001"></a>
## F001 — authoritative case and target behavior

**Status: primary document through root direct local PDF inspection; collector synthesis.** [S001](SOURCES.md#S001) identifies the portable original twenty-page case and its SHA256. Root rendered and visually read all pages; the collector uses the saved direct-reading notes, not an independent visual inspection. Page4 lists running/abrupt movement around equipment, dangerous proximity to moving mechanisms, phone during equipment work **or movement through the workshop**, smoking/open flame outside designated places, barrier climbing/under conveyors or suspended loads, height without attachment, fall/lying/immobility/possible loss of consciousness, and incorrect carrying as an additional scenario.

Pages5,7,9,13 require reliable timely notification, suppression of repeat messages during one continuing episode, camera configuration and a persistent filterable journal with evidence, camera, time and type. Page13 requires actual neural inference on LinQ and speed measurements. “Several seconds” is not a numerical class-independent SLA. Page12's thirty-second assistance illustration is not a specified immobility threshold. The case allows a focused scenario set with an extensible architecture. Reading it supplied no target videos, SDK version, device count, accepted host/device partition or quality threshold.

The historical “full case missing” premise is superseded. Phone movement must survive the narrower thematic paraphrase. Page15 gives checkpoint24October19:00 versus18:00 in historical context; current planning needs a separate organizer check. The owned RTX4070 in the general context and planned1–2RTX3090 24GB experimental rental in the thematic brief are different resource statements, neither an actual installed configuration nor rental authorization. The oral “even1FPS, prioritize quality” is a reported preference, not measured temporal sufficiency.

<a id="F002"></a>
## F002 — actual work and evidence ladder

**Status: recorded execution history.** Sixteen distinct fresh Medium W1 agents completed M01–M08/D09–D16. A separate fresh High critic saved CRITIC.md before seven fresh Medium W2 agents. This is a separate High collector. [TASKS.json](_WORK/TASKS.json), [TASKS_W2.json](_WORK/TASKS_W2.json), [RUN_STATE.md](_WORK/RUN_STATE.md) and [CRITIC_ORIGINAL.md](_WORK/CRITIC_ORIGINAL.md) preserve actual roles and history. Writer, editor and compressor are later separate roles.

Keep these stages distinct: model family exists → exact trained artifact found → access checked → full bytes/hash → static schema → reference execution → causal event benchmark → export parity → actual LinQ execution. HEAD is metadata, range GET is partial access, a checksum is identity, and media decode is not inference. Branch `local_test` may mean CSV/ZIP/RAR/HDF5/ONNX/TFLite parsing, media clocks, bounded visual review or deterministic annotation arithmetic. No source benchmark was independently reproduced as model performance here. Target accuracy, VRAM, CPU/RTX speed and LinQ support remain unknown.

Source copies and mirrors are one provenance family. A downloaded annotation does not prove current media access; HTTP200 may be a watch-player error or Drive quota HTML. A reviewed development fixture cannot become a blind target holdout. Positive grants, unresolved scope and explicit restrictions are separate records.

<a id="F003"></a>
## F003 — method registry: pose and tracking frontends

Every row below is a concrete candidate, not measured industrial success. Required fields are task, paper/code/revision, exact weight, input/output, temporal/runtime contract, training/evaluation conditions, failures, baseline/export risks and unknowns. Exact URLs and saved acquisition locators are preserved in the detailed records. Shared unknowns across all rows: industrial event quality, actual runtime/memory/throughput and LinQ compatibility.

| Method identity | Input → output and timing | Evidence and original evaluation boundary | Fit, failure and next gate |
|---|---|---|---|
| RTMPose-m body7 e48f03d0, SDK1.2.0 | External person xywh → corrected RGB CropResizePad256×192 → FLOAT NCHW → SimCC x/y384/512. COCO17 supported by head weights; serialized joint axis is symbolic. | Full ZIP/ONNX hash and static schema. Seven-dataset training is author-declared; public COCO config does not recover the complete mixture. {{W2-01-F001}} {{W2-01-F002}} {{W2-01-F003}} | Posture/transition frontend. Detector mandatory. SDK crop/color/decode parity comes before target tests. |
| RTMPose-t body7 026a1439 | Same exact pipeline hash/interface;168nodes versus m247;13.35MB graph versus54.33MB. | Existing local graph independently reparsed, no new tiny download or m/t runtime comparison. {{W2-01-F006}} | Smaller comparator. Promote m only if target event evidence justifies it. |
| RTMO-s COCO8db55a59 / body7dac2bf74 | Single-stage bottom-up640²; boxes and17points after decode. | COCO PTH and body7 SDK ZIP are different checkpoints, HEAD only. Author latency uses V100/ORT. {{M01-F004}} {{M01-F009}} | Crowded-scene alternative; exact graph/decode/export unverified. |
| YOLO11n-pose v8.3.0 asset | Whole image, typical640; person boxes and COCO17. Wrapper outputs are not raw export schema. | HEAD6255593B; AGPL/Enterprise licensing decision. No execution. {{M01-F002}} {{M01-F009}} {{M01-F011}} | Convenient baseline; distant workers lose pixels and truncation/occlusion remain. |
| ViTPose-B classic | External bbox;256×192 crop; COCO17 heatmaps. | Apache code; original OneDrive returned HTML, binary access unestablished. OCHuman uses GT boxes; COCO uses56AP detector and flip. {{M01-F005}} {{M01-F009}} | Offline accuracy comparator with equal boxes; GT-box pose AP omits detector failures. |
| MoveNet MultiPose Lightningv1 | RGB dimensions multiples32; recommended256long side; output[1,6,56], hard maximum6 detections. | TFL3 prefix/metadata access; Apache model statement. Card describes3–6ft webcam and surveillance out of scope. {{M01-F007}} {{M01-F009}} | Exploratory close-person route. SinglePose emits one selected person; tracker capacity does not increase detection cap. |
| MediaPipe full float16v1 |224² detector →256² landmarker;33 image/world points, video timestamps. | Current API num_poses>0, default1; older2021 card describes single person and excludes distant surveillance. Task HEAD9398198B. {{M01-F007}} {{M01-F008}} | Busy async calls can drop frames. Estimated hip-relative metres are not calibrated scene distance. |
| ByteTrack d1bf0191… | Detector xyxy+score; high/low association; tracked/lost/removed distinct. | MIT code; detector weights/training external; no tracker run. {{M02-F01}} {{M02-F02}} | Common host baseline, with source-time expiry and separate event ledger. |
| OC-SORT8462e7… | Nx5 input; empty advances time, None returns before clock increment; output xyxy+ID. | MIT, default max_age30/min_hits3/delta_t3 in update steps. {{M02-F04}} {{M02-F05}} | Retained ID can be withheld from output after a gap; no output cannot clear an incident. |
| BoT-SORT2519854… | Detector/crops, optional ReID with spatial IoU gate; live CMC choice separate. | MIT; published test commands add retrospective interpolation. {{M02-F03}} {{M02-F08}} | Appearance cannot rescue a pair rejected by the spatial gate. Report raw causal output separately. |
| DeepSORT / StrongSORT | Appearance+geometry; demo may emit one-step predictions. | GPL code, separate embedding dependency; StrongSORT++ AFLink/GSI reads full trajectories. {{M02-F06}} {{M02-F07}} | Predicted/interpolated boxes are not observed action or immobility. |

Default COCO pose summary has all/medium/large, no AP-small. This does not mean small people are excluded from allAP. Ground-truth visibility is not predicted confidence. Target evaluation must stratify original person size, occlusion and truncation while retaining detector misses in the all-event denominator. Pose does not directly detect phone, cigarette, attachment correctness, consciousness or physical distance.

<a id="F004"></a>
## F004 — method registry: temporal, HOI and risk models

| Exact candidate | Input, output and time contract | Artifact/evaluation evidence | Decisive limitation |
|---|---|---|---|
| SlowOnlyR50 HMDB51, MMAction0.24.1 |8frames interval4;3D recognizer,51classes; source clip/crop aggregation. |127223551B HEAD, run32/walk49; config pinned. {{M04-F01}} | Genuine separate gait names, but movie domain, actor localization and causal trailing-window evaluation remain. |
| SlowFastR50 AVA22, MMAction a5a167… | Full RGB32frames interval2 plus person proposals; RoIAlign81 multilabel channels including0; offsets−32…+30 at30Hz. |135802749B HEAD, no full hash; AVA frame-mAP protocol. {{W1-M05-F003}} {{W1-M05-F004}} | About1second future input. Annotation review does not make its centered model causal. |
| UPT-R50 HICO-DET,192743… | Image → boxes, pairing[2,M],117verbs,80objects,scores,size. Pair indices are image-local. |219754181B advertised,4096B ZIP prefix checked; not full weights; BSD3 code. {{W1-M05-F005}} {{W1-M05-F006}} | Human–phone interaction donor, no operation/movement policy or chronology. Carry/use can coexist. |
| udayraj28 fall LSTM, e1c36… |30×5features: angle, CoGy, framewise CoGdelta, bbox aspect, mean pose confidence → normal/falling/fallen. | Full810808B PTH,8228B ONNX+807424B external data; IR10/opset17,2LSTM. {{M03-F04}} | Unknown grant, overlapping-window split and heuristic labels. Real structural artifact, not clean industrial evidence. |
| Rchit13 fall H5,47b543… | Actual code30frames×24XY, plain LSTM128→64 binary, despite README60frames/BiLSTM. |4018632B HDF5 observed; scalers not loaded; MIT code with inference-only component wording. {{M03-F06}} | Scaling fitted before split, filename labels; artifact/preprocessing contract still needs inspection. |
| MoViNet-A0 Stream float | FLOAT32[1,1,172,172,3]+43states →600logits+43states; prefix since reset. | Full27141832B TFLite,44/44 signature,896ops. External state payload2696832B only. {{W2-07-F01}} {{W2-07-F03}} | Causal convolution, cumulative head/block pools; no current-event/clear or actor output. |
| MoViNet-A0 INT8v1 | Same external FLOAT32 image/buffer/logits shapes; underscore state names; internal quantized modified graph. | Full3276048B model,227ops;30block state pairs identity; explicit Apache2 model grant. {{W2-07-F02}} | Different architecture from float, not a pure precision parity pair. |
| STGCN++ joint COCO17, MMAction1.2 | PreNormalize2D → joint/score features →100uniform samples across supplied action;2people; ten test clips. |5859545B HEAD; author NTU60xsub joint89.29%; actual config16epochs×Repeat5 despite80e filename. {{M08-F03}} |100samples has no fixed seconds. Pose extractor and NTU terms differ from target CCTV. |
| X3D-XS PyTorchVideo |4frames; builder crop160 versus demo182; demo12/30 stride gives1.6s; RGB/255,mean.45/std.225. |30779313B HEAD, K400400class head. {{M08-F04}} | Freeze one recipe; K400 lacks plain run/walk, nearest name is not policy. |
| TSM/TSN MMAction |8segments across supplied clip; test TenCrop gives80images,224px. | TSM97651119B HEAD; bidirectional shifts within clip. {{M08-F05}} | Whole-clip sampling/endpoints and future shift require a new online protocol. |
| VideoMAE-B |16frames interval4,5clips×ThreeCrop=15views; test-only resize224 versus README320. |173099345B HEAD, K400 recognition;87M/180G are source statistics. {{M08-F06}} | Offline transfer reference, outside critical path without clean target data/device path. |
| NearCollision6Image6s_027 | Six RGB224² at10Hz,0.5s history → first person within1m of moving camera in next6s. | Weight prefix plus actual two overlapping HDF5 windows; VGG16/regression. {{M06-F01}} {{M06-F02}} {{M06-F04}} | Ego proximity is not third-party worker–forklift risk. Missing raw IDs and code/centering/shape contradictions. |
| FP-TTC625e5… | Monocular temporal TTC to observation plane, trained Driving/KITTI. | Official code; advertised folder did not expose a verified weight in bounded check. {{M06-F05}} | Wrong risk reference and incomplete supply. |
| SynthSite YOLOWorld/DINO | Text objects+image geometry; clip-global votes/gap fill; DINO~1FPS aggregation. | Public schema/code/results; candidate weights HEAD, authors' exact run hash unknown. {{M07-F03}} {{M07-F04}} | All synthetic; anthropometric scale is not calibrated3D, pair ownership and causality remain. |

Industrial quality and runtime remain unknown for every row. Image AP, poseAP, clip top1, AVA mAP, tracking HOTA and industrial event recall are different quantities. New head training, cadence, crop, trailing window or reset policy changes the evaluation contract.

<a id="F005"></a>
## F005 — exact checkpoint registry and retrieval levels

These are build/reference identities, not working-system claims. Exact URLs appear in SOURCES and the detailed records. Hashes below are local full-body SHA256 unless explicitly described otherwise. Static ONNX/TFLite parsing and pickle opcode inspection do not execute the model.

| Artifact | Retrieved identity/schema | Rights and remaining gate |
|---|---|---|
| RTMPose-m body7e48f03d0 ZIP |50799818B, `f7fbb6c5c11a1bb70f3d445e4ddec5d144ea89ad5649c081ef976f9b24a0b741`; ONNX54330655B, `5c0a4bf67953e6d2ac43ce15e77dc9d5d354ae18430a47d2c5963a7bc5683e3c`,IR6/opset11,no external data. | Apache2 code; archive has no specific weight grant. Matching detector, SDK crop/decode parity, runtime/device remain. |
| Corresponding body7 PTH |54551099B HEAD only; exporter detail names it. Not downloaded or numerically compared. | Do not substitute AIC+COCO63eb25f7. |
| RTMDet-nano05d8511e recipe PTH |4224050B, `05d8511e7b3fabc62e27d2f624179e004ad14ee63a86ca9d9d22c88f3db0eee1`; one-person config. | Exact matching export/full mmdetection/MMDeploy stack and specific weight scope open. |
| CPU demo96154d0b detector ONNX | Ranged ZIP members, not whole ZIP;4012393B, `b8585adb6d1352796f6e86337e09c3459b830645a7e7192d9381670bea2facbd`,688ops including NMS/dynamic shapes. | Old SDK/mmdet versions, local source PTH unresolved. Distinct candidate, not recipe05d8511e. |
| Existing RTMPose-t body7 ONNX |13350364B, `a6c2f6a3896a4d51131d14d7a80a3d08b50f559af5a58a45d5b098aef510a70f`; local reparse only. | Same pipeline, no measured m/t quality or cost comparison. |
| Small fall LSTM PTH/ONNX/data | `96918521abd9d2f29693887bcd673ea62ad8e293574b8639c7109b9abf71edc1` / `580a1f7e40593013dbca52566d8d72f9fe849d8a6e8a1512c79ed85df9f1b716` / `6b7ab751f5f4ab738ead96bb1ab1c11b936b34e41dda0a36ebabadd3bd86b412`. | Unknown license, heuristic labels/split issues. ONNX alone is incomplete; external data required. |
| keremberke forklift best.pt d8b594… |6216376B, `0dc3816283226f0f7ac5410620394c8ddeef32c5200b371194ac4df4a1ee7d38`; static map0forklift/1person. | MIT catalogue is positive scope evidence, card has no specific weight license. Runtime/export/transfer open. |
| rabahdev fire-smoke best.pt13017… |6229802B, `b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f`; static map0smoke/1fire. | Explicit AGPL3 card/embedded metadata. Export/input/NMS and real temporal controls open. |
| MoViNet float Google TFLite |27141832B, `04c02709bce4a8233b03f36620909924735051cfd4bcc83e3d9d7db9bbf375ad`; storage generation1626903706896942. | Official artifact, source Apache2; exact float model grant less direct than INT8 instance. State/runtime/head/device open. |
| MoViNet INT8 Kaggle322/v1/445 | Tar2641653B hash`7b395747f5ed76429adac76e13a1d04e8ae6efe7a4196b39f32fc2b2f44e05d9`;1.tflite3276048B hash`6125b36e2485eeb5cc1fd6206cf5e5d70235593fbc84610d1dce97fe3aa9c2ac`. | Explicit Apache2 model-instance grant. Different graph/state keys require separate quality comparison. |

Evidence: {{W2-01-F001}} {{W2-01-F004}} {{W2-01-F005}} {{W2-01-F006}} {{M03-F04}} {{W2-05-F07}} {{W2-06-F01}} {{W2-07-F01}} {{W2-07-F02}}. HEAD/probe-only SlowOnly, SlowFast, UPT, STGCN++, X3D, TSM, VideoMAE, RTMO, YOLO11, MoveNet, MediaPipe, DINO and YOLOWorld remain distinct retrieval statuses in their detailed records.

<a id="F006"></a>
## F006 — video dataset registry: falls, gait and phone

Shared unknowns unless specifically established: total physical event count, full original duration, complete subject/site diversity, public-demo/consent scope and target quality. Frames, annotation rows, segments and windows are not independent original videos. Reviewed fixtures are development material.

| Dataset/release/originator | Media/access and scene | Labels, groups and target compatibility | Rights/use and missing gate |
|---|---|---|---|
| GMDCSA24 v2.1, Alam et al.,5abac… | Three exact original MP4s identity-checked/decoded W2:181/146/139frames,1280×720/1280×720/640×480,~30Hz PTS. | OmniFall458segments/160videos;75train subjects1/3,48val subject2,37test subject4. Fall/fallen/lie_down/lying separate. | Positive MIT repository + CC BY4 Zenodo; annotation NC/SA conflict separate. Reviewed subject4 member is now development. {{M03-F02}} {{W2-02-F01}} {{W2-02-F07}} |
| URFD, Kępski/Kwolek2014 |30fall/40ADL;cam0 parallel floor,cam1 ceiling falls-only. PNG ZIP HEAD; adl10 preview300frames640×240 side-by-side,30Hz. | Source frame/syncms and posture−1/0/+1;1470ADL+1 rows in16sequences. Official subject split unestablished. | CC BY-NC-SA4 academic/noncommercial, commercial permission separate; preview not verified pixel-identical to raw PNG. {{D10-F04}} {{D10-F05}} {{W2-02-F05}} |
| UP-Fall, Martínez-Villaseñor et al.2019 |17healthy actors, room/mattress, two fixed views;~18.4Hz consolidated source. Drive label/downloader URLs returned quota HTML; raw images not acquired. | Timestamped states change inside activity folders; historical train subjects1–12/test13–17;3s windows50%overlap majority labels. | Raw-image grant not established by paper CC BY; deliberate lying/pickup/jump useful negatives once obtained. {{D10-F08}} {{D10-F10}} |
| Montreal MCF2010 + erratum2025 | Eight wide-angle cameras, one actor; index/PDFs and ZIP metadata accessible, no video acquisition. | Nine states include sofa/ground lying/crouch; corrected reference cameras/time offsets. Scenario23 conflict remains. | All views/scenario one group; no actor-disjoint test possible. Video grant/access and visual semantics open. {{D10-F12}} {{D10-F13}} {{D10-F14}} |
| Le2i/ImViA | Old URL404; newer DOI/package lead503 at check; no media. | Package documents conversion/labels, not current acquired source. | Package CC BY-NC-SA3 attribution is a lead, not independent current grant verification. {{M03-F03}} |
| OmniFall, Schneider et al.,HF83572… | Unified labels/splits; source media separate. Synthetic9.716GB TAR32B probe only. | `path,label,start,end,subject,cam,dataset`;fall1/fallen2/lie_down5/lying6;walk includes running. Multiview EOF/duplicate warnings. | Frontmatter NC4 versus narrative NC-SA4 conflict; package Apache2 code;5s synthetic clips cannot prove long holds. {{M03-F01}} {{M03-F03}} |
| CAVIAR, Fisher team/INRIA2003 | Fight_RunAway1/Walk1 fully decoded552/612frames,384×288, nominal25Hz with nonincreasing PTS. | Actor-centered bbox XML and movement; actor7 walk→run373–436→walk; actor6 run385–489. | Positive CC BY-SA statement, version unknown. Ordinal origin±1 unresolved; preserve PTS and explicitly synthetic i/25 sanity clock. {{W2-03-F02}} {{W2-03-F04}} {{W2-03-F06}} |
| KTH, Schuldt/Laptev/Caputo2004 |25actors/four conditions;~600AVIs/2391subsequences. Three person15 clips decoded160×12025Hz. | Walking/jogging/running separate;1-based inclusive intervals; original8/8/9subject split. | Homogeneous gait sanity donor, not factory acceptance; source rights remain separate. {{M04-F03}} {{M04-F04}} |
| Edinburgh BEHAVE interactions | Full35450–47160 AVI,11711frames640×48025Hz, not unrelated2022BEHAVE. | XGTF top-left boxes; global frame−35450 candidate. Nested/overlapping RunTogether groups not dense all-actor gait. | Free-research/citation statement positive; standardized commercial/demo redistribution not established. {{D11-F01}} {{W2-03-F03}} {{W2-03-F06}} |
| VIRAT Ground R2/DIVA | Exact source folders and annotation joins inspected; no new fully reviewed gait video fixture. | Original person/event joins, minimum-duration and post-action tail semantics. DIVA includes gait despite current MEVA exclusions. | Agreement permits lawful research/commercial use subject to acceptance, PII and redistribution conditions; not accepted for team. {{D11-F04}} {{D11-F05}} {{D11-F06}} {{D11-F07}} |
| HMDB51, MIT/Brown | Smoking class110RAR members; two AVIs acquired/decoded236/59frames320×24030Hz. | Clip-class smoke; no dense puff/onset/actor/object labels. Separate SlowOnly run/walk head exists. | Current official CC BY4 statement positive; upstream film/web footage rights separate. {{D14-F02}} |
| AVA22, Google Research | CSV243029rows acquired. Two exact phone-source YouTube player routes unavailable; HTML200 is not media. | Sparse1Hz actor boxes/actions;77phone+walk person-seconds,27runs/eightvideos/24video-person pairs, not77events. | Annotation CC BY4; first route reports copyright removal, second generic unavailable. {{W1-M05-F001}} {{W2-04-F001}} |
| Charades, AllenAI2016 |2RFLZ member765584B,222frames480×270~15.029Hz; all frames visually reviewed W2. | Clip-owned action/start/end, no actor or phone boxes. Desk-phone ear-use beside table; no convincing concurrent walking. | Noncommercial research/evaluation; public modified/third-party distribution restricted. Donor, not target event pack. {{W1-D12-F001}} {{W2-04-F002}} {{W2-04-F003}} |
| P-DESTRE | Phone attributes in actual annotation payload;733MB-class media member not retrieved. | Phone rows ID−1 cannot form one track; width/height interpretation unresolved. | No decoded phone-actor fixture; exact media/rights/coordinate gates remain. {{W1-D12-F003}} |
| MECCANO/100DOH/DMD/NTU | MECCANO active-object JSON and tool-weight locator;100DOH contact donor; DMD/NTU restrictions. | MECCANO has no phone taxonomy; generic contact does not separate radio/scanner; NTU action/skeleton not industrial policy. | Rights and RGB/skeleton representation separate; use normal hand/tool confusers only when obtained. {{W1-D12-F004}} {{W1-D12-F006}} {{W1-D12-F007}} |

<a id="F007"></a>
## F007 — video dataset registry: industry, machines, flame and handling

| Dataset/source | Actual artifact/scene evidence | Label semantics and overlap | Rights, use and remaining gate |
|---|---|---|---|
| Safe/Unsafe factory CCTV | Accessible real factory donor, bounded media/payload checks by D09. | Source overload/safe-unsafe categories are not certified near-miss GT. | Keep factory-domain donor, not universal case events. {{D09-F11}} |
| SARDv1, Chengfeng Wu2026 | Core manifest748videos/11actions; supplementary nine MP4/nine TXT; two carry/ladder videos fully decoded. |4.txt160824rows,49546person,6594Unknow; frame29track1stand(L)box1446,120,1498,192. Missing frames not negatives; adjacent source-ID cuts grouped. | CC BY4 metadata, upstream clips separate. Claimed included splits/definitions absent from checked manifests. {{D09-F01}} {{D09-F03}} {{D09-F04}} |
| Foundation Pitv2, Zhao et al.2025 | Four RAR manifests12+22+6+2=42MP4, no event sidecars;40Pexels names+two Donggang. | Downloaded distance_mix image XML/JSON is not aligned video risk GT. Filename FPS is not measured. | CC BY4 with third-party caveat; construction donor needs event annotation. {{D09-F05}} {{D09-F06}} {{D09-F07}} |
| ENIGMA-360, Ragusa et al.2026 | Abstract180ego/exo pairs; website360pairs tile conflicts. Two downloader-generated raw URLs404. |68procedure actions;103/29/48ID split; raw45JSON46intervals end748.863s. | CC BY-NC4, raw video gap; paired views one group. Normal electronics work, not violation labels. {{D09-F08}} |
| Factory Operation, Kataoka et al.2022 | One full265s MP4,3975frames640×48015Hz; six samples machine/empty area; corresponding daily CSV inspected. | Authors30h/three days/one camera;12work labels per second; model uses100frames1Hz=100s context. | Kaggle licenseUnknown; paper CC BY not data grant. Potential longer control only after full review. {{D09-F09}} {{D09-F10}} |
| PhysicalAI-SmartSpaces, NVIDIA2cbe956… | Real first60s Warehouse026four views/027seven views plus calibration; Camera0000full1080p30Hz1800frames decoded. | Separate workers and routine advancing driven truck visible by sampled review; real GT/depth withheld. All synchronized views one group. | Positive CC BY4 plus contradictory hidden-target/privacy/no-training wording. Not certified risk GT. {{W2-05-F01}} {{W2-05-F02}} {{W2-05-F04}} {{W2-05-F05}} |
| Real RGB/thermal forklift benchmark | Two RGB/two thermal sensors ride forklift; authors19420images/camera, no archive acquired. | Person/people/background, occlusion, centroid depth; not external fixed-camera pair risk. | Request-only nonprofit data. Article CC BY does not waive access. {{D13-F06}} {{D13-F07}} |
| NearCollision HDF5 | Actual bounded two six-frame RGB windows;1038examples in937MBtest metadata. | Labels0…5.9s, Mean2.299754/Variance2.983061; adjacent windows five/six frames identical. | Unknown data/code/weights grant; missing recording IDs/PTS, wrong ego target. Dependence is not proven train/test leakage. {{M06-F02}} {{M06-F03}} |
| Fence/wall repo3aa345… | Two full301frame1080p30Hz files,~10s each. | Samples return to same side; wall overlaid timecode moves backward; no completed crossing labels. | Capture/generation lineage and license unknown. Not verified real CCTV. {{M07-F01}} {{M07-F02}} |
| SynthSite, GovTech2904ec… |227video/label references consistent; media not acquired; all generated. | Tier1unanimous150(76unsafe/74safe);Tier2seventy-seven(39/38). True_Positive/False_Positive are GT names. | Stress/demo only if scope cleared, never real lockbox/FP-hour. {{M07-F03}} {{M07-F05}} |
| MmodalFire, Zhang/Jia et al.2026 | RAR4.929GB,103member manifest:70CSV/28MP4/1XLSX/1TXT/3dirs. One42.506s raw video fully decoded1064frames1080pHEVC~25Hz. |38worksheet sessions; mist Aug10/dry ice Aug4. Acquired short video Aug2 excludes both. Sensor pair22815rows each is not visual GT. | CC BY4 data/MIT code. Paper65experiments/two labs versus28raw files unresolved units/layout. Actual mist video **UNCONFIRMED**. {{W2-06-F02}} {{W2-06-F03}} {{W2-06-F04}} |
| SAFELIFT, Zenodo18243098 | Env2 frontal ZIP4253000B acquired, eight anonymized real clips decoded; other views unacquired. | Physical lift/lower endpoints,176unknown/six intermediate not binary unsafe; timing/unit caveats in record. | Handling donor only; mass/frequency/coupling/task/carry route missing. {{D14-F01}} |
| CML/CAAR/UW-IOM | CML skeleton metadata, CAAR request/academic gate, UW-IOM temporal action lead. | Promising climb/crawl/attachment contrasts, no matched ready target RGB+weights+events. | Preserve localized access failures, not global nonexistence. {{M07-F07}} {{M07-F08}} {{D14-F06}} |
| SURREACT/SynAPT/REMAG | Published transfer comparisons; large REMAG archives HEAD only; SURREACT credential route401. | Gains and losses depend on source/background/task/backbone. Motion/render twins share parent. | Source research-only assets may constrain demo; no industrial event/real FP-hour proof. {{D16-F01}} {{D16-F02}} {{D16-F03}} {{D16-F05}} |

<a id="F008"></a>
## F008 — fall clocks and finite observation horizons

**Status: actual bytes/decode/source-code/CSV checks, preliminary single-researcher visual interpretation.** W2_02 resolves the join for its **four files only**, not the entire GMD/OmniFall/URFD corpus. Raw PTS, time_base, stream_start and relative seconds are separate. GMD conversion copies bytes after renaming; the package decoder adds stream.start_time to annotation seconds. Join against `(PTS−stream.start_time)*time_base`. S1 raw origin.033333 is real, but its last relative6.064067 lies inside label end6.08. The early raw-clock “missing tail” diagnostic is superseded. Package EOF repetition cannot create independent hold evidence.

| File | Original annotation seconds / source frame | Last actual observation | Maximum labelled tail, not motionless truth |
|---|---|---:|---|
| GMD S1Fall11 | standing[0,.52), fall[.52,2.7), fallen[2.7,6.08) |6.064067relative |3.364067s fallen; leg adjustment occurs; sampled coarse stability from4.2 leaves at most1.864067s. |
| GMD S3ADL08 | lie_down[0,3.71597), lying[3.716,4.896) |4.864067 |1.148067s labelled lying; controlled lowering on mat, earlier history left-censored. |
| GMD S4Fall01 | standing[0,1.14), fall[1.14,2.44), fallen[2.44,4.66) |4.624167 |2.184167s fallen; bed/cot support, not observed ground accident; now reviewed development. |
| URFD adl10 |−1frames1–169,0frames170–199,+1frames200–300 |9968ms source sync |3.338s+1; reclines/settles on sofa, body partly cropped. |

None of these four provides10s or30s post-transition hold or a complete recovery/clear/rearm cycle. This is not a corpus-wide absence claim. A10s preview is not10s lying. UR preview ordinal+1 joins source frame, but source sync differs from preview30Hz by−12.333…+11.333ms and raw PNG pixel identity remains unverified. Source+1 is posture, not accident, floor location or immobility. The1470ADL+1 rows are labelled rows, not confirmed floor-lying observations. Evidence: {{W2-02-F01}} {{W2-02-F02}} {{W2-02-F03}} {{W2-02-F04}} {{W2-02-F05}} {{W2-02-F06}}.

<a id="F009"></a>
## F009 — gait alignment and low-FPS observation opportunity

**Status: full decode, native-scale overlays and deterministic annotation arithmetic; no model run.** CAVIAR1×center-box and BEHAVE1×top-left boxes fit reviewed people;0.5×/2× fail. BEHAVE global frame−35450 locates the acquired clip, but±1origin remains ambiguous. CAVIAR nonincreasing PTS occurs at RunAway indices2,3,125,176,359 and Walk1 indices38,598. No adjacent byte-identical RGB images were found; do not delete images because timestamps repeat. BEHAVE PTS=i+1 at1/25 is strict; full-source XML1FPS metadata does not replace the acquired25FPS clock. CAVIAR i/25 is an explicitly synthetic evaluation clock, not recovered capture time. Retain both clocks and test mappingδ−1/0/+1.

Actor7 running373–436 has64labelled frames, actor6 running385–489 has105. BEHAVE selected groups[1,2]44396–44447 and[0,1]46306–46375 have52/70inclusive frames; nested rows are not extra independent episodes or all-person gait GT. Actor6 last7×4bbox is a visibility stress case, and disappearing at the edge is not physical cessation.

Enumerating25sampling phases gives actor7 only2–3/5–6/12–13samples at1/2/5FPS, actor6 gives4–5/8–9/21. Declared synthetic20%drop seeds0–99 can leave zero1FPS observations; a one-second burst is a separate stress condition. These are annotation-time opportunities, not recall. Without drops, first opportunity delay ranges0–.96s at1FPS,0–.48s at2FPS,0–.16s at5FPS, before model/window/confirmation/notification delay. Evidence: {{W2-03-F02}} {{W2-03-F03}} {{W2-03-F04}} {{W2-03-F05}} {{W2-03-F06}} {{W2-03-F07}}.

<a id="F010"></a>
## F010 — phone supply and concurrent-action limits

**Status: actual annotation parsing, official player responses and complete bounded Charades review.** AVA77same-person phone+walk samples are useful sparse co-labels, not77events, continuous phone visibility or equipment state. Source15answer phone and57text/look are different. Exact QTmwhrVal1g/person91seconds1181–1190 and WSPvfxtqisg/person1seconds908–915 return playerERROR with no media stream. First reports copyright removal on Reliance Entertainment request; second is generically unavailable. HTML200 is not playable video. This does not establish all AVA unavailable.

All222Charades2RFLZframes were reviewed at480×270, PTS step1000/15029, last14.704904s. One actor enters2.329–3.660, reaches desk3.726–4.857, raises hand/device4.924–5.123, holds an ear-side pose5.190–8.184, lowers8.251–9.448 and returns/reaches9.515–12.177. Source c0193.0–10.4 is broader than visible ear use. Script/cord/desk context supports a stationary desk-phone interpretation. No convincing simultaneous locomotion/use was established, no source walking interval or person/phone boxes exist. Preserve original labels separately from preliminary observations.

UPT/HICO positively supplies image pair and multi-label carry/hold/talk evidence. Carry is not a veto against use. Radio/scanner are not explicit80-object categories. Hand-to-face, tool, PPE adjustment, allowed terminal and permitted phone controls remain unmeasured. Phone stays reserve pending target footage with visible same-actor object/use/concurrence and policy. Evidence: {{W1-M05-F001}} {{W1-M05-F002}} {{W1-M05-F006}} {{W1-M05-F007}} {{W2-04-F001}} {{W2-04-F002}} {{W2-04-F003}} {{W2-04-F004}}.

<a id="F011"></a>
## F011 — real warehouse passage is not certified near-miss

**Status: complete media/hash/decode, sampled preliminary visual inventory and unresolved primary-document contradiction.** Warehouse026Camera0000 is60s/1800frames1080p30Hz, SHA256`83ed232a2f5fe3031807ed19020e1a44fe386e89b68f9bea621797f1552c9cda`. Review covers every second plus5FPS detail33–41.8s, not every frame. At least three free workers and one advancing driven forklift/reach-truck are visible. Bending/handling precedes~34s, truck advances~34–38s, a vest worker carries a box left~38–40.6s, operator is visible~44–46s, truck leaves the lower image~48s. This is routine passage/co-presence, not certified danger, metre distance, TTC, yielding causation or procedure violation.

Current2cbe956… card/changelog explicitly releases first60s of two real test scenes with calibration, without GT/depth. Croissant and paper retain hidden-target/privacy/train-exclusion wording. It is unknown whether that describes an unreleased remainder or stale text about these files. Preserve the positive CC BY4 card/Croissant/Track1 grant and this separate scope question. Challenge FAQ manual-test-label restrictions are a competition protocol, not automatically a universal copyright ban. No challenge labels/tuning were created here.

Detector d8b594… static map0forklift/1person is opposite AI City Person0/Forklift1. Card640-input ultralytics8.0.21/ultralyticsplus0.0.23 validation mAP50.83794 is author image performance, not event transfer. Needed controls: stationary-near, moving-far, driver-only, reverse/turn, barrier separation, occluded feet/forks, independently surveyed envelope and pair-event GT. No dangerous staging is needed. Evidence: {{W2-05-F01}} {{W2-05-F02}} {{W2-05-F03}} {{W2-05-F04}} {{W2-05-F05}} {{W2-05-F06}} {{W2-05-F07}} {{W2-05-F08}}.

<a id="F012"></a>
## F012 — flame supply closure and actual mist gap

**Status: full static weight confirmation, complete RAR headers/member extraction and short video decode, no inference.** Fire checkpoint13017… has explicit AGPL3, map0smoke/1fire and full6.23MB hash. It detects regions, not smoking people or permission. Card D-Fire50epochs/640/batch16/AppleMPS test mAP50.754/mAP50–95.430 are unreplicated image conditions. Export graph/input/output/NMS remain unknown. D-Fire CC0 collection retains third-party terms; old FURG/FIRESENSE are not automatically independent holdout.

MmodalFire RAR is non-solid,103members, exact declared archive end and valid header CRC. Full archive MD5 not locally verified. Paper65experiments/two labs versus actual28rawMP4/38settings rows is unresolved count/layout, not proof65is false. Dry ice Aug4/mist Aug10 settings and Humidifier4 CSV pair22815rows/~356.68s are actually acquired. Video mapping requires camera overlay time against opaque filenames. Only acquired short raw clip is Aug2~09:33,42.506s/1064frames, outside all listed mist/dry-ice sessions. **Mist video is UNCONFIRMED.** Sensor rows are not visual negative GT; no dense ignition/clear/rearm GT was acquired. Midpoint-centered5s sequence classification is not a causal event protocol.

The visible-flame route needs permissioned continuous onset/clear, industrial steam/dust/smoke-only, allowed furnace/welding and active/inactive permit controls. Two HMDB smoke clips do not provide puff ownership or flame event truth. Evidence: {{W2-06-F01}} {{W2-06-F02}} {{W2-06-F03}} {{W2-06-F04}} {{W2-06-F05}} {{D14-F02}}.

<a id="F013"></a>
## F013 — MoViNet state is prefix classification

**Status: source/static graph inference, no invocation.** Float27.14MB and INT8 variant3.276MB each have one serving_default signature,44inputs/44outputs: image+43states, logits+43states. No init_states signature. External image is FLOAT32[1,1,172,172,3], logits[1,600]. INT8 internal computation does not imply integer external I/O: buffers/logits/image are FLOAT32, counters INT32. Match by signature names, not array position; float slash names and INT8 underscore names differ.

Head sum/count classifies the prefix since zero-reset. Float also has15block cumulative pool pairs. The modified INT8 architecture removes squeeze/excitation, with30block state I/O identities; head pooling stays active. No PTS input exists: dropped source time does not advance count, refeeding a frame does, cadence changes physical horizon. Prefix dilution and lingering event features are plausible source/graph consequences, not measured behavior. Reset all states at declared independent video/camera/crop identity boundaries; frequent resets change the reference and require cold-start testing.

Official600-label map is pinned but not embedded. Looking-at-phone265/talking-cellphone516/texting525/smoking477/jogging236/welding588 are donors/confusers, not industrial policy heads. Historical INT8 Pixel4 CPU4.80ms/65%top1/3.1MB and recommended5FPS concern modified K60010s clips, not this float binary, LinQ or event latency. Evidence: {{W2-07-F01}} {{W2-07-F02}} {{W2-07-F03}} {{W2-07-F04}} {{W2-07-F05}} {{W2-07-F06}}.

<a id="F014"></a>
## F014 — annotation semantic matrix and proposed target record

Preserve source annotations unchanged, with a separate operational target layer. Source states/actions do not silently become safety events.

| Actual source example | Established meaning | Missing target semantics |
|---|---|---|
| URFD adl10/frame200/+1, sync6630ms | Source posture/time; visible sofa recline in preview. | Accident/floor location/whole-body low motion/recovery. |
| OmniFall S1Fall11 fall.52–2.7 | Action interval under its definition, stream-relative join. | Independent first-visible onset, physical accident, immobility hold. |
| CAVIAR actor7 running373–436 | Actor-linked movement label. | Dense visibility, exact ordinal origin, industrial zone/policy. |
| BEHAVE[1,2]RunTogether44396–44447 | Group interaction interval. | Every person's gait/visibility; nested-row independence. |
| AVA same-person15+14 at t | Sparse answer-phone and walk labels. | Device localization, dense concurrence, equipment/permit context. |
| Charades c0193.0–10.4 | Broad clip-owned talk-phone/camera interval. | Actor/device pair, visible onset, concurrent walking. |
| SARD frame29track1stand(L)box | Tracked source object/action row. | Video clock join, unsafe condition, policy and episode. |
| SmartSpaces calibration/tracks | Geometry/tracking format. | Released real GT, surveyed safety envelope, risk/permit. |
| SynthSite True_Positive | Reviewer-judged generated clip hazard. | Real physical event, actor/pair interval and target validity. |
| SAFELIFT endpoint/unknown | Endpoint research measurement. | Agreed categorical handling violation, load/task context. |

Proposed fields: source_id, original_sha/revision, parent_source/session/sync group, subject/site/camera, media_time_base/raw_pts_origin/stream_start/clock_mapping_version, event_id, actor or ordered-pair IDs, scenario literal and policy_version, action/state, start/end/evidence intervals, visible/occluded/unknown spans, allowed ROI/active permit, censoring, source versus operational label, annotator/provenance/disagreement and train/dev/lockbox role. Track identity, physical person identity and event identity differ. Record physical onset if known, first visible evidence, confirmation and notification separately.

QA includes schema/ranges, clock monotonicity or documented anomalies, actor/pair coverage, parent/sync grouping, uncertain boundaries, independent double annotation/adjudication and retained disagreement. Unlabelled spans are not automatically negatives. CVAT video XML carries frame-indexed tracks/occlusion but needs a PTS/policy sidecar; consensus task export can omit replicas, so retain per-job opinions. VIA3 supports temporal segments; its BSD code grant does not clear footage. ActivityNet mAP and sed_eval matching principles are useful, but their default tIoU/collars are not case thresholds. Evidence: {{D15-F01}} {{D15-F02}} {{D15-F03}} {{D15-F04}} {{D15-F05}} and full D15 records below.

<a id="F015"></a>
## F015 — central eight-case method ↔ video compatibility matrix

**Status: proposed decisions derived from inspected supply/semantics.** No row is a validated industrial detector. All inherit metrics F017 and conditional device boundary F021. Exact artifact/access/rights are in F003–F007 and detailed dossiers; a ready development pack is not a target lockbox.

| Case / observable target | Baseline and escalation | Exact supply / development pack | Extra annotation, controls and stop gate |
|---|---|---|---|
|1Run/abrupt movement around equipment | Footpoint track displacement/time+configured zone; pose/RGB gait if legs observable; geometry for physical speed. | CAVIAR/BEHAVE/KTH decoded labels; SlowOnly HMDB run32/walk49 HEAD; exact RTMPose static bundle. | Define gait versus fast motion/acceleration; target actor/zone/visibility. Fast-walk, carrying, turns, ID crossings, camera shake/platform controls; near/far/front/side and native/1/2/5FPS. Stop physical speed without survey, gait without visibility. |
|2Moving-machine danger | Person/forklift detector+track+machine motion+pair-specific ground envelope. | Real SmartSpaces routine60s/hash/PTS, full keremberke two-class weight/static map; NearCollision wrong ego target. | Pair/motion/driver/occlusion/permit GT and surveyed envelope. Stationary-near, moving-far, driver-only, reverse/turn, barriers. Reserve until rights/GT/geometry; stop risk from bbox overlap. |
|3Phone during equipment work OR workshop movement | Person–small-object/use association plus concurrent context; wrist/head crop aid only. | UPT image pair probe; AVA sparse positives but exact selected videos unavailable; Charades desk phone reviewed. | Dense same-actor device/use/movement or equipment state; radio/scanner/tool/PPE adjustment/carry/allowed terminal controls. Stop when pixels cannot distinguish object/use; reserve. |
|4Smoking/open flame outside designated place | Split tasks: flame region+time+active permit ROI; smoking needs person/device/puff evidence. | Full fire best.pt AGPL0smoke/1fire; two HMDB smoke clips; actual Mmodal manifest/sensors, mist video UNCONFIRMED. | Onset/clear/visibility/permit GT; steam/dust/smoke-only/furnace/welding/reflection/screen/tiny ignition. Narrow flame development only until controls. Stop smoking claim from plume head. |
|5Barrier / under conveyor or suspended load | Safe-side→transfer→opposite landing for completed climb; configured corridor occupancy is one narrower fallback; physical under-load needs3D/load state. | Two fence probes unknown lineage/no completion; SynthSite227generated labels/code and candidate weights HEAD; SARD ladder donor. | Completed/attempt/normal stages, actor/load pair and allowed maintenance. Reach/crouch/behind-machine/landed-load controls. Stop “under” from2D overlap and “crossed” without previous side. |
|6Height without valid attachment | Known elevated area plus visible harness/lanyard/connector/anchor and requirement. | Primary hook paper/request-only data, CAAR authorization gate; generic pose/PPE not attachment truth. | Loose hook/wrong anchor/occluded strap/ground PPE controls; closer/other view or procedure. Stop connection claim from hook-above-harness. |
|7Fall / lying / observed low motion | Causal transition, separate lying and visible low-motion hold; pose+tracking+ledger, temporal head only after comparison. | Exact m/t static pose, four actual GMD/UR clock fixtures and intentional/sofa controls, OmniFall split/semantics. | Long permissioned target hold/recovery and independent visibility/transition GT. Maintenance prone/rest/sit/pickup/kneel controls. Stop10/30s hold on short tails; no consciousness diagnosis. |
|8Incorrect carrying | Observed lift/lower/carry plus agreed load/task procedure; kinematics only evidence component. | SAFELIFT eight clips/endpoints, SARD tool/steel carry, UW-IOM lead. | Mass/frequency/coupling/route/task and safe/unsafe GT; team/tool-assisted/one-hand/occluded load controls. Stop universal unsafe classifier from endpoint/action labels. |

Static perception can supply objects/posture but a safety event also needs time, identity and policy. Metrics include common event/timely recall, precision, FP per reviewed camera-hour, duplicates and latency, plus per-row action confusion, pair association, object ownership, onset/permit/attachment visibility or handling-rule agreement. Geometry, FPS, camera elevation, object pixels and occlusion are conditions, not generic performance assurances. One reusable zone mechanism is one capability, not several independent hazards.

<a id="F016"></a>
## F016 — negative controls and missing evidence

| Failure mechanism | Acquired counterevidence | Required target controls still missing |
|---|---|---|
| Fall versus posture | Controlled GMD ADL08 lying, UR sofa, GMD S4bed,1470UR ADL+1labelled rows. | Maintenance prone/rest/slow collapse, sit/pickup/kneel, long hold, occlusion and recovery. |
| Gait versus image speed | KTH walk/jog/run, CAVIAR walking and walk→run→walk. | Fast walk, short burst, running in place, platform/camera movement, near/far and ID switches. |
| Phone versus hand pose | Desk-phone clip and HICO carry/hold/talk coexistence. | Radio/scanner/terminal/tool, hearing protection/wiping/eating, inactive equipment/allowed phone. |
| Pair risk | Routine warehouse handling, truck/operator-like passage and occlusion. | Certified stationary-near/moving-far/driver-only/reverse/turn/barrier separation. |
| Flame versus context | Mmodal Aug2room handling sample, mist settings/sensors without mapped video. | Actual mist, industrial steam/dust/smoke-only, permitted welding/furnace, screens/reflections. |
| Barrier/under-load | Same-side fence attempt, generated safe/unsafe examples. | Completed transfer versus reach, repair crouch, behind-object, landed load, permitted corridor. |
| Attachment/height | Papers expose proximity cue versus unobserved connection. | Occluded strap, loose/wrong hook, ground worker, actual anchor procedure. |
| Handling | Tool-assisted brick lift and SAFELIFT endpoint/unknown variation. | Rule-specific mass/frequency/coupling/team lift/carry route and safe handling. |

Authorize and fully review continuous negative exposure against the defined operational target. Missing labels and invisible positives cannot become negatives. Eligibility is GT-driven, not “detector found it.” Titles/outros/frozen/looped/repeated images and synthetic footage cannot inflate real-camera exposure. Drops/busy/reconnect periods retain missing-observation status; production service accounting is separate from inference-only speed. Evidence F008–F015, D15 and D16 dossiers.

<a id="F017"></a>
## F017 — causal event metrics and lifecycle contract

**Status: proposed protocol grounded in case and code.** Predeclare one-to-one alert↔GT matching with compatible class/actor/pair, onset or overlap tolerance, uncertain boundaries and censoring. Do not choose favorable matching after predictions. A stable episode ledger is separate from tracker IDs. Measured, predicted, retained-lost, removed and emitted track states need separate fields. Pre-association expiry based on last measured source PTS prevents late reacquisition after a nominal TTL; long buffers can merge different people. A missed box/joint/frame is unknown, not safe or immobility time. Already lying at first frame does not retrospectively prove fall; right-censored lying cannot prove clear/rearm.

Report all-known-event recall including unobservable, timely recall against agreed deadline, observable/eligible subset recall with coverage, event precision, unmatched alerts per reviewed camera-hour, duplicates per GT event, onset/first-evidence/confirmation/notification latency, duration and clear errors, censoring, critical misses and camera/scale/visibility/lighting strata. Detector failure cannot remove a GT event from the primary denominator. Negative-hour definitions must state label completeness, unknown spans and service state.

Media PTS and processing wall time are separate. Unpaced replay measures causal source-time decisions, not live notification latency. Paced/live tests preserve decode/enqueue/request/result/confirmation/storage/notification wall timestamps, queue age/drops, reconnects and execution location. Future-suffix perturbation must not alter earlier causal alerts. Centered AVA, whole-clip voting, StrongSORT++ AFLink/GSI and postsequence interpolation cannot be reported as t=t online evidence. Evidence: [S001](SOURCES.md#S001), {{M02-F02}} {{M02-F05}} {{M02-F06}} {{M02-F07}} {{M02-F08}} and D15 detailed matching records; [E004](OPEN_QUESTIONS.md#E004).

<a id="F018"></a>
## F018 — provenance and leakage ledger

Split before frame/window/crop generation. Group original continuous recording and derivatives, then subject/session/site/camera according to the generalization claim. Keep official source split and current role separately. Reviewed S4Fall01 was source test but is now development here; familiar subjects1/3 cannot be independent test. New target lockbox must stay untouched.

Specific linked families: UR two views of one fall and ceiling-view falls-only confounding; MCF eight views/one actor/scenario; CMDFall pre-cut duplicates; ENIGMA ego/exo pair; SmartSpaces four/seven synchronized views of one minute; SARD adjacent YouTube-ID cuts and stock provenance; HMDB same film; AVA neighboring seconds/shots; Charades same subject/take; NearCollision adjacent windows sharing five/six images; NTU concurrent views/pose conversions; K400val overlapping K700train and AVA-Kinetics incorporating AVA/K700; D-Fire relationship to legacy fire corpora; synthetic prompt/background/motion/source twins.

Start exact hash/source-ID ledger, then authorized near-duplicate and temporal-overlap QA with human review. Report uncertainty by recording/event groups, not frame/window counts. Observed within-test overlap is not itself proof of train/test leakage. Public test-video access does not authorize tuning or turn it into independent train data. Evidence: {{M03-F02}} {{M03-F03}} {{M06-F03}} {{M08-F08}} {{D09-F04}} {{W2-02-F07}} {{W2-05-F03}} {{D16-F01}}.

<a id="F019"></a>
## F019 — rights ledger with positive grants preserved

**Status: source statements, not legal opinion.** Code, weights, annotations, source media, privacy/consent and redistribution are separate. Missing standalone LICENSE does not negate an explicit card grant; public access does not replace one.

| Family/layer | Positive established scope | Separate unknown/restriction |
|---|---|---|
| OpenMMLab | Apache2 MMPose/MMDeploy code, listed algorithm exceptions. | Specific body7/detector weight grant not found; upstream mixture/terms separate. |
| Google models | Explicit Apache2 MoveNet and MoViNet INT8 model-instance statements. | Exact float grant less direct; training media and industrial scope separate. |
| Ultralytics/fire | AGPL/Enterprise route; rabahdev explicit AGPL model. | Runtime/export dependencies, D-Fire third-party media caveat; no all-MIT chain. |
| GMD | MIT repository and CC BY4 Zenodo release. | Attribution/distribution route and actor/site/privacy. |
| OmniFall | Apache2 package code, positive NC annotation statements. | NC4 frontmatter versus NC-SA4 narrative; underlying source video terms. |
| URFD/UP-Fall/MCF | URFD NC-SA4 academic; public/citation and documentation evidence for others. | Competition/commercial/demo/raw-image grants not all established. |
| HMDB/CAVIAR/BEHAVE | Current HMDB CC BY4, CAVIAR CC BY-SA, BEHAVE free-research/citation. | Upstream footage, exact SA version, commercial/public redistribution. |
| AVA/Charades | AVA annotation CC BY4; Charades defined noncommercial research/evaluation. | Source copyright/unavailability, Charades modified-data/third-party distribution limits. |
| SmartSpaces | CC BY4 card/Croissant/official download statement. | Contradictory hidden-target/privacy/training text and independent derivative use. |
| SARD/Foundation Pit | CC BY4 records. | YouTube/Pexels/third-party origin terms and individual releases. |
| MmodalFire | CC BY4 data and MIT author code. | Actual selected-video mapping and separate target-factory authorization. |
| VIRAT Ground | Lawful research/commercial agreement. | User acceptance, PII, limited redistribution; no acceptance performed for team. |
| Small fall/NearCollision/fence | Actual artifacts publicly readable. | No explicit grant found in inspected paths; not permission or proof of permanent prohibition. |
| CAAR/NTU/SURREACT | Specific academic/research/request agreements. | Not automatically commercial demo/training permission via a public paper/derived pickle. |

No outreach or agreement acceptance was done for the team. Private evaluation, public hackathon demo, open repository redistribution and commercial deployment are distinct owner questions. Exact wording, versions and locators remain in SOURCES and detailed records.

<a id="F020"></a>
## F020 — three conditional routes and hypotheses

All routes are proposed and unimplemented. Each shares artifact/rights E001, grouped data E002, causal metrics E004 and actual device E008 gates. No acceptance percentage or runtime promise is invented.

1. **Detector/tracker plus timed camera rules.** Hypothesis: one defined observable event such as configured corridor occupancy, visible flame outside an active permitted ROI, or measured moving-machine envelope can meet agreed event/FP requirements without a generic video model. Inputs are source-PTS frames, exact detector class map, ROI/policy, measured track state; outputs are actor/pair event, evidence, unknown, confirmation and clear. Split continuous camera/site/session groups before tuning. Compare bbox-only against tracking+ledger, measuring timely/all-event recall, FP/hour, duplicates and latency. Stop if the physical target is unobservable, controls fail or host/device partition is forbidden. One zone fallback counts as one capability.
2. **Pose plus causal temporal rules/light head.** Hypothesis: adequate person/joint pixels and a matched detector/crop let transition+posture+observed motion separate fall from deliberate lying better than bbox aspect alone. Inputs are exact RTMPose m/t contract, boxes, PTS, track quality and joint scores; outputs are separate fall_suspected, lying_observed, observed_low_motion and unknown. GMD/UR clock fixtures are development; evaluate on new actor/site/camera groups with maintenance, long hold and recovery. Compare m/t, bbox, tracking and pose before adding the problematic small LSTM. Stop if visibility/history or chronology is insufficient, or pose adds false certainty. N seconds needs policy and actual N seconds, not padding.
3. **Video model/cascade after baseline failure.** Hypothesis: a relevant past-only RGB/skeleton module improves event precision/recall on permissioned sequences where rules lack action cues. Exact choices are MoViNet float with a full state ledger, X3D-XS with a frozen crop recipe, or STGCN++ with verified pose channels. AVA remains lookahead/offline unless its protocol is explicitly changed. Inputs are declared history/cadence/crop identity, never GT boundaries; scores feed a separate event policy. Lock grouped test before head/threshold selection. Compare event metrics, coverage, latency, prefix length, reset and cadence. Stop without a relevant head/labels, measured gain, affordable state/latency or device path. Heavy VideoMAE/SlowFast/ensembles stay outside critical path.

<a id="F021"></a>
## F021 — LinQ boundary and neighboring-topic handoffs

The case requires actual neural inference on LinQ. Detector/pose/flame on device with decode/tracker/geometry/rules on CPU is a **conditional design**, not an accepted partition. Host temporal execution alone is insufficient. ONNXopset11, no custom ops, TFLite availability or VM visibility does not establish support. No SDK commands are invented.

| Recipient | Established handoff / changed decision | Required next input |
|---|---|---|
| model_stack | Exact body7 graph/SDK1.2 RGB/CropResizePad/minSimCC; recipe05d8511e differs from old demo96154d0b. Static fire/forklift maps; MoViNet variants distinct. | Complete versioned detector export/reference, preprocessing/decoder parity and notices. F003–F005/F013 |
| linq_platform | Mandatory device execution, host partition unknown; detector NMS/dynamic shape, pose MatMul and streaming states are separate risks. | Issued SDK/compiler/runtime/device, unsupported report, artifact/input/job/raw-output execution provenance. E008 |
| model_fidelity_quantization | Full hashes/schemas; modified MoViNet INT8 cannot isolate pure quantization error. | Architecture-controlled precision pairs where possible; raw-output and event delta with fixed GT. |
| camera_calibration_geometry | Calibration exists but not independently certified safety distance; footpoints and off-plane loads ambiguous. | Surveyed planes/footprints, camera-change invalidation and uncertain boundaries. E007 |
| datasets/evaluation | Precise four fall fixtures, gait clock ambiguity, desk-phone fallback, routine warehouse and mist gap. | Permissioned continuous target positives/negatives, long holds/recovery and independent actor/pair GT/lockbox. |
| training_strategy/cv_accuracy_vast | Supply exists; small fall labels/splits weak; synthetic gain conditional. | Split before windows, baseline ablation before head adaptation; actual available resources, no assumed VRAM/time. |
| video_architecture | PTS/wall clock, emitted versus retained/predicted IDs, MoViNet reset/prefix and drops. | Causal request/event ledger, stream epochs, queue/drop/unknown status and paced end-to-end timing. |
| operator_product/hackathon_strategy | One continuous event→one message with evidence/unknown; no diagnosis or physical overclaim. | Scenario/policy, red/yellow meaning, deadline origin, hold/gap/clear/rearm and acceptable error budget. |
| behavioral_safety_feasibility | Supply/clock/semantic results update prior provisional choices. | Keep W2 scope_narrowed, adopt shortlist gates rather than importing old readiness. |

<a id="F022"></a>
## F022 — conditional MVP shortlist and stop-list

**First: observed fall transition, with separate lying/visible-low-motion states.** This has the best research readiness: exact pose static frontend, actual media/clock fixture, rich transition-versus-intentional-lying semantics and hard negatives. Start with m/t and an explicit matching detector choice, then target long hold/recovery clips with independent GT. It remains conditional: no model/event/device run, no10/30s hold in four reviewed tails, no diagnosis.

**Second: one camera's clearly defined gait/abrupt-motion rule around equipment.** Actual CCTV transition/walking labels plus KTH and exact HMDB run/walk locator enable an honest source-level comparison. Target fast-walk, short burst, occlusion and zone GT must pass; keep it reserve if not. Use “image displacement proxy” without metric geometry.

**Third, conditional alternative: visible flame outside active permitted ROI.** Exact small AGPL weights/map are now strong supply evidence, but temporal negatives/onset/clear remain weaker than a ready-MVP claim. Admit only after industrial steam/allowed fire/permit and recovery controls. Mist video is still unconfirmed. Drop it if that gate fails; no need to fill a three-scenario quota.

Moving-forklift envelope is operationally valuable but reserve until pair-event GT, geometry and use scope are resolved. Phone is reserve until visible object/concurrent work or movement target data exists. A narrowly named corridor occupancy fallback is one infrastructure option.

Stop-list until new external inputs: unconsciousness diagnosis; correct harness connection from hook/bbox; physical under-load/collision from2D overlap; universal unsafe carrying from pose; phone-while-walking from the desk-phone donor; K400/K600 class names as industrial heads; long holds from padded/looped tails; retrospective output as online; heavy temporal training without clean labels/device path; generated footage as real holdout or FP-hour.

<a id="F023"></a>
## F023 — additional hazard and synthetic transfer limits

One supported **research extension** is apparent person-directed physical aggression: AVA64fight/hit and76push are real evaluation classes, with478/86validation person-second rows, not independent event counts. The AVA trained-head/proposal route exists, but example55Ihr6uVIDAat991s was not opened/decoded, and close-contact/helping-work negatives/industrial holdout are absent. It is not a ready extra MVP feature. Incorrect carrying is already case item8; a second generic zone name is not another hazard. No second complete extension is invented to satisfy a quota. Evidence {{M08-F07}}.

Synthetic benefit is conditional. SURREACT Kinetics15 one-shot uses15real train clips/725real test: real-only26.2%, synthetic-only9.4%, real+synthetic MiniKinetics backgrounds32.7%, LSUN26.3%. SynAPT TimeSformer HMDB synthetic pretraining54.38 versus Kinetics59.51, MiniSSV251.10 versus48.92, under stated initializations. REMAG11actions reports synthetic4–8points behind real, conventional CG above neural rendering and mocap above reconstructed motion; models already use K400 pretraining,64frame/300epoch conditions. These are author comparisons, not industrial event forecasts. Motion/source/render twins share groups; real target test remains independent. VideoPhy/VBench physics/consistency/dynamics scores are not safety GT. Generated demos need explicit synthetic labels and permitted source assets. Evidence {{D16-F01}} {{D16-F02}} {{D16-F03}} {{D16-F04}} {{D16-F05}} {{D16-F06}}.

<a id="F024"></a>
## F024 — contradictions and supersession

| Issue | Canonical treatment |
|---|---|
| Case/context | Full case available; phone includes workshop movement; checkpoint19:00 versus18:00 remains planning discrepancy. |
| Pose supply | body7 is not AIC+COCO; CPU demo detector is not recipe detector; SDK crop/RGB differs from Python demo. Numerical consequences unmeasured. |
| Fall clock | Relative-stream join supersedes early S1 raw-clock tail diagnostic; four-fixture horizons are not corpus-wide limits. |
| URFD posture | Original+1ground-lying wording coexists with visible sofa recline in adl10. Keep source label and observation separately. |
| OmniFall rights | NC4 frontmatter versus NC-SA4 narrative unresolved; positive source-video grants survive. |
| MCF23 | Index confound-only versus report falling1520–1595/3574–3614; erratum does not resolve. Inspect before positive/negative admission. |
| Gait |2×BEHAVE scale rejected; CAVIAR extra images not adjacent duplicates; exact origin/capture clock still open. |
| Small fall models | README/report/checkpoint score/epoch mismatch, heuristics/windows/scaling problems prevent clean performance attribution. |
| SmartSpaces | Real release/CC BY4/download coexist with hidden-target/privacy/train language. Keep positive grant and narrow scope question. |
| MmodalFire |28raw files/38settings versus65experiments/two labs unresolved units/layout; mist sensors do not equal mist video. |
| MoViNet | README13MB versus actual27.14MB float; INT8 usage typo and modified architecture retained, no pure precision pairing. |
| HMDB | Later official CC BY4 statement updates earlier W1 uncertainty; upstream footage still separate. |
| Numeric classes | OmniFall walk includes run; K400 lacks plain run/walk; AVA source IDs≠60class positions; HOI verbs≠600interactions; detector map≠AI City map. |

K001–K007 all end **scope_narrowed**, with closed artifact subcomponents and remaining experiment/scope gates. Exact outcomes are appended to [CRITIC.md](CRITIC.md), preserving original criticism verbatim. Documentary checks cannot close an unrun numerical/event/device test.

<a id="F025"></a>
## F025 — concrete immediate sequence

Choose one observable target and policy. Obtain permissioned continuous target positives and matched negatives with independent GT. Freeze exact artifact/class map/pre/post and complete detector dependency. Build a CPU/RTX reference, then causal source-PTS event ledger and identity/clear/rearm tests. Compare native/1/2/5FPS phases/drops before adaptation. Request SDK/device/host-boundary facts early because they can invalidate the architecture; perform exact LinQ compile/run quality delta later. No rental, training or new search wave is implied.

[Q001–Q018](OPEN_QUESTIONS.md#Q001) and [E001–E008](OPEN_QUESTIONS.md#E001) define unresolved decisions and the full proposed roadmap, including inputs, actions, expected observations, decision gates, failure modes, saved evidence and what PASS does not prove. No arbitrary acceptance percentage, memory or runtime promise is used.
