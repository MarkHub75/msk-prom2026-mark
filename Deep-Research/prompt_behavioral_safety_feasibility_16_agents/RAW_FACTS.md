# RAW_FACTS — Behavioral Safety Feasibility: инженерная база

Срез: **23 октября 2026, Europe/Moscow (UTC+3)**. Сборщик анализировал сохранённые16W1+8W2, fresh CRITIC и notes/provenance/run state; новой сети, третьей волны, приложения, обучения, экспорта или аппаратного прогона не было. Исходные ветки сохранены. База предназначена для принятия решений и разработки после выдачи доступа, а не выдаёт research за готовое приложение.

Навигация: [источники](SOURCES.md), [вопросы и эксперименты](OPEN_QUESTIONS.md), [исходные K и результаты](CRITIC.md), [сопоставление ID](_WORK/ID_MAP.md). F001–F009 — синтез/контракт; F010–F035 — подробные объединённые инженерные записи, включая exact URLs, hashes, I/O, классы, preprocessing, источники данных и отвергнутые варианты. Исходные branch-local ID внутри подробных выписок служат локаторами происхождения; canonical ID — явные F/S/Q/E/K anchors.

<a id="F001"></a>
## F001 — Кейс и обязательный объём

**Тип:** первичный пользовательский PDF + визуальные наблюдения оркестратора. [S001](SOURCES.md#S001), все20страниц; оригинал SHA256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`. Raster PDF; пустая текстовая экстракция не реконструирована из соседнего отчёта. Публичный URL именно этой копии не установлен.

Слайд4 содержит: (1) бег по цеху/резкие перемещения в зоне техники; (2) опасное сближение человека с **движущимися** механизмами/транспортом; (3) использование телефона при работе или перемещении; (4) курение **или** открытый огонь вне отведённых мест; (5) перелезание ограждений/проход под конвейером или подвешенным грузом; (6) работа на высоте без использования страховочной привязи; (7) падение, неподвижное лежание, внешние признаки потери сознания; (8) неправильная переноска груза, **дополнительный** сценарий.

Слайды7/13: команда выбирает приоритеты; надёжное сообщение важнее числа сценариев; требуются video **или** images input, нейросетевое распознавание, оперативное web **или** local-GUI уведомление с кадром/фрагментом, камерой/временем/типом, **одно уведомление на нарушение**, сохраняемый журнал с фильтрами и **реальный LinQ inference с замерами скорости**, расширяемость без полной переработки. Настраиваемые зоны/правила, операторские статусы, dashboard и несколько потоков желательны. Слайд8 отдельно обещает VM и сервис, не задаёт transport/API/upload grant. Слайд5 перечисляет свет/блики/пыль/дым/окклюзии/малые объекты и качественную реакцию в несколько секунд. Численного общего SLA/hold нет. Пример30секунд помощи на слайде12 не норматив неподвижности. Дедлайн25.10.2026 10:00МСК; команда5человек. Сообщения организаторам в research не отправлялись.

<a id="F002"></a>
## F002 — Тип доказательства и фактически выполненные проверки

**Правило интерпретации:** `vendor family named → exact artifact listed/HEAD → actual bytes/hash → graph/source inspected → host inference/parity → frontend/PTQ/compile → device completion/parity/timings → event/journal/UI controls` — разные этапы. В этой программе **нет host NN inference, собственного export/compile или LinQ inference PASS**. Успешный checker также не выполнялся. Наличие source script не его исполнение; proposedE не measuredE.

| Что выполнено | Условия/предел | Где подробности |
|---|---|---|
| Полные GET/хеши YOLOX, official pose, RTMPoseZIP/ONNX | Собственные SHA полного payload; bounded protobuf/pickletools, не execution; графы не ONNX checker | [F014](#F014) |
| Полные GET/статические names forklift и двух firePT | zip/pickle disassembly без torch.load/unpickle; class map не measured quality | [F022](#F022), [F026](#F026) |
| Структурный Range scan MeetCool/SafetyVision | Top-level I/O/opsets/operators прочитаны; full payload/hash не получены | [F012](#F012) |
| GMDCSA6clips,1048frames | Полный decode и последовательные all-frame sheets, visibility/phase annotations; gross motion, не дыхание/сознание | [F017](#F017) |
| CCTV2core+2forklift clips | Полный decode; выбранные stills/contact sheets, не полная actor/frameGT | [F023](#F023), [F022](#F022) |
| NVIDIA2synthetic MP4 | Bounded ZIP64 members,CRC/full memberSHA,decode144frames каждый; review каждые0.5s | [F022](#F022) |
| Weizmann2AVI | Bounded ZIP members,CRC/SHA,126decodedPTS; review каждый5кадр; encoded25FPS | [F020](#F020) |
| FURG3+FIRESENSE2videos | Full decode/all-frame sheets; XML geometry/extra indices/stale boxes/false empty labels установлены | [F026](#F026) |
| Четыре coreMP4 primary identity | GMDCSA2архивных member побайтно/CRC/SHA; SafeUnsafe2primary manifestSHA+localfullSHA | [F015](#F015) |
| Sampling и tracker arithmetic | Synthetic10000phase coverage и constructor/TTL/hold arithmetic, **не** NN/video/model benchmark | [F013](#F013), [F034](#F034) |
| Vendor performance PDF2026 | Official presslink+два textparsers; исходныеbytes/hash/реальныеimages недоступны; reported measurements | [F010](#F010) |

AP/mAP/top1/FPS из cards/papers описывают протокол авторов; не сопоставляются в рейтинг качества событий и не переносятся на целевые камеры или LinQ. При описании local measurements явно называть decode/PTS/hash/арифметику, а не «модель проверена». `UNKNOWN` не `FAIL`, `NOT_RUN` не0.

<a id="F003"></a>
## F003 — Единая матрица всех восьми сценариев

Это качественная матрица выбора, без выдуманных баллов/вероятностей. `MVP-ready candidate` означает достаточный вход в короткий тест, а не доказанный LinQ. Для всех строк compile/device/event metrics NOT_RUN; vendor family/pose row не привязаны к выбранным checkpoint. Нагрузка/усилия перечисляют компоненты, не обещают срок.

| Исходный кейс / operational definition | Реальные video evidence и права | Exact model/weights / processing route | LinQ и performance evidence | Quality evidence | Integration effort | Demo feasibility | Основные FP/FN | Blocking unknowns | Verdict/детальныеF |
|---|---|---|---|---|---|---|---|---|---|
| №1 бег/резкие перемещения: rolling translation velocity/изменение в одном track; gait-run отдельная цель | Weizmann daria_walk/run получены,просмотрены;25FPS encoded против50page,physicalclock неизвестен,publicgrant не установлен. Continuous fastwalk/transition/burst/camera pack отсутствует | YOLOXnano exactONNX416→person0→class-specific ByteTrack→footpoint/H/rolling v; pose/PoseC3DHMDB run32/walk49 толькорезерв | YOLOXIR6/opset11 static graph известен,preproc ambiguity; LinQ ниразунезапущен,actualFPS/E2Eнет | Видимый gait-контраст, не speed/modelscore; floor/capture-time не измерены | Floor measurement+checkpoints,rolling estimator,sourcePTS,localpolicy; initial-window locked_ids заменить | Условно после собственной безопасной fixedcamera записи+rights+device | Fastwalk≠run; movingcamera,IDjump,jitter/occludedfeet;shortburstaliasing | Q001/002/005/007/008; E001/002/005 | **Conditional, priority2**. [F019](#F019),[F020](#F020),[F014](#F014) |
| №2 человек рядом с движущейся техникой: co-visible ordered pair+machine motion+image-space envelope | 3_te1/7_te1 real motion/driver,нет уверенного отдельногоwalkingpedestrian; NVIDIA00238syntheticpair,00298farpartialcontrol; stationarynearнет;NVIDIAterms отдельно | keremberke best.pt exacthash/names0forklift1person;640export ожидаем6channels,не получен→perclass tracks→motiongate→pair episode | `.pt` metadata известна,graph/compile нет; no measuredNN/E2E | Real motion и synthetic co-visibility осмотрены,notnear-missGT;метры/TTCнет | Legacy8.0.21load/export,customdecoder,driverexclusion,footprint,cameraquality,realcontrols | Internal synthetic smoke; complete public realroute NO-GO до gates | DriverFP,otherdepth,occludedfootpoint,turning/reverse,stationarymovingmastFN | Q001/002/009/010/017;E002/006/009 | **Conditional reserve1**. [F021](#F021),[F022](#F022) |
| №3 телефон при ходьбе/работе: use-like evidence и movement/context совпадают у однойперсоны | Нет полученногоtargetphonevideo; AVA15/57rows,NTUphonegated,HICOimages; media rights distinct | YOLOXperson0/phone67 либо officialv8;association+optionalpose/HOIUPT; detector не use | Exactgenericgraph есть,phone-event/exportHOI/deviceнет;smallphonequantizationнеизмерена | Semantics/labels/sourcecode,не localactionaccuracy | Nativecrop/ownerassociation,confusers,temporaloverlap,approvedpolicy;HOI добавляетNN | Near-camera собственныйpermissionedpilot,не full-CCTV claim | Tool/scanner/radio,carryathip,otherperson;small/hiddenphoneFN | Q001/011/017;E002/008/009 | **Conditional reserve2**, послеtargetvisibility. [F024](#F024),[F025](#F025) |
| №4 курение/огонь: выбран только устойчивыйvisibleflame внеactiveallowedROI;smoke отдельно | FURGCar1/BBQ/nonfire+FIRESENSEfire/headlights fullydecoded; CC0/CCBY grants есть,IEEEtitle/UltimateChasewatermark residualscope | Preferred rabah exactPT0smoke1fire AGPL;farhatbackup; expected6406channelONNX ещёнеexport;classfilter+spatialregionFSM+policy | NoLinQ/noactualONNXtwoPT; R3E6readyONNX17 reference,grantunknown;FPS/E2Eнет | XMLbugs/contentreview;нет inferencecomparison. Rabahвыбранпоprovenance,неquality | Isolated8.4.51/export/parity,curateGT,cuts/ROI/permit,regionidentity | Сильнее genericzone как independent исходныйpattern; publicclip scope/action resolve | Lamps/headlights,welding,screen/orangePPE,steam;tinylighterFN;smokingнепокрыт | Q001/002/012/017/018;E002/007/009 | **Conditional priority3, fire-only**. [F026](#F026),[F027](#F027),[F035](#F035) |
| №5 перелезание/подоборудованием: approach→elevation/contact→transfer→landing;knowncorridorA→B частныйroute | Fence exactvideo leads неreviewed,source9IDswap;CAARgated;industrialcompletepositiveнет | Person/pose exactcandidate→sceneobject/side/topgeometry+sequence. Tripwire/occupancy отдельно | Posegraphpath потенциальный,noLinQ/temporalexport;FPS/E2Eнет | Exactsourcefaults/maps,неvalidatedclimb | NeedsceneGT/fenceviews/gates/corridor; aerialloadneeds3D/telemetry | Safe lowmockup owncapture onlyplan; corridorfallback считать одинраз | Raisedhand/bend/step/gate,occlusion,unknownroute,depthambiguity | Q001/013/017;E008/009 | **Research-only fullpattern; narrowconditional**. [F029](#F029),[F030](#F030) |
| №6 высота без привязи: visibleabsence в заранееизвестнойsurface гдеharnessrequired;connectedhook отдельныйнеподтверждённыйclaim | HuangVOC safety-harness/person/clothes;OpenSite4video lead безpayload;targetclipнет | SafetyVisionv2ONNX640IR9/opset20→17channels13classes,No_Harness10card;person11association+surface/visibilityrule;Thalosотвергнут | StructuralRangescan,неfullhash/checker/device;FPS/E2Eнет | CardAP неevent;actual13classnames cardprovenance,неизshape | Needtargettorso/surface/rule,NO-XNMSownership,hook/anchorслой отсутствует | Safegrounddecoration pilot; универсальноconnectedclaim исключить | Occlusion/vest/harnessconfusion,twoowners,collectiveprotection,y-in-image≠height | Q001/014/017;E008/009 | **Reject fullpromise thishackathon; absencepilotconditional**. [F031](#F031),[F032](#F032),[F012](#F012),[F028](#F028) |
| №7 падение/лежание: observedtransition→lowposture→continuousgrosslowmotion;operatorreview,неunconscious | GMDCSA6clips fullydecoded/allframes;S3F07tail6.432033s,S1F11tail2.208033s;EOFcensored;hardnegatives/cropunknown. CorepairprimaryCCBYbyteidentity | ExactYOLOX+RTMPoseSDKRGB2outputs либо officialposePTexport;tracks+validposehistory+FSM;TSSTG404,PoseC3Dbackup | RTMPose actualsymbolicoutputs,opset11;static specialization/parity/deviceopen;officialposeONNXnotexported. NoFPS/E2E | Grossvisibility/phaseannotations,не absolute immobility/modelaccuracy;revieweddevall | Oneposepath+ownerassociation,scale/H/reference/limbmotion,unknown/recovery/longtake | **Best prepared behavioral devpack**, longH/rearm/industrialholdoutmissing | Sit/bend/intentionallying/exerciseFP;hiddenbody/slowcollapse/axisfallFN | Q001/002/005/006/017;E001/002/003/004/009 | **MVP-ready candidate for smoke, conditionalpriority1**. [F016](#F016),[F017](#F017),[F018](#F018),[F014](#F014) |
| №8 переноскагруза,дополнительный: толькоtask-specificobservable rule | Нетполученногоvalidatedcarryingrulevideo;genericpick/carry не improperGT | Pose+knownobject/SKU/massmetadata+approvedroute/peoplecount; exactgeneralindustrialloadweightsнеустановлены | No graph/device/event/e2emeasurement | Ergonomicdocumentsобъясняютнедостающиеmass/frequency/grip;неCVvalidation | Needлокальнаяпроцедура,knownload/route,permissionedtargetvideo | Отложить,еслинетготовогоконкретногоobservablecase | Emptylargebox,hiddenhelper,unrelatedpeople,2Dangles;massunknown | Q015/017;E008 | **Reject currentgenericpromise, additionalonly**. [F031](#F031) |

Слепленные слова в компактных ячейках — технические литералы/сокращения таблицы, не названия функций/API. Детальные F содержат нормальные поля, exactURLs и полный смысл условий.

<a id="F004"></a>
## F004 — Условный shortlist и переключения

**Инженерный вывод после двух волн:** брать не три названия в интерфейсе, а2–3самостоятельных наблюдаемых паттерна с positive/negative evidence. Общий входной gate — accepted LinQ execution и достаточные outputs. До него ни одного deployed/MVP-ready-on-LinQ сценария нет.

1. **№7 suspected fall followed by gross low motion** — первый behavioral candidate. Есть наиболее подробныйdevpack,transition/hardnegative/visibilityGT и two documentedpose routes. Основная угроза — poseparity/device и отсутствие длинного/clear/rearm/industrialholdout. Начать с короткогоH, только если это выбранное правило по смыслу, а не подгонка ради6.432s. ДляH10/30 нужна новая запись; currentclips censored. Еслиpose недоступна, bboxlowposture может быть другимузким наблюдением, но не полноценной заменой этогоclaim. [F014](#F014),[F016](#F016),[F017](#F017),[Q006](OPEN_QUESTIONS.md#Q006).
2. **№1 быстрое перемещение на калиброванном fixed-camera участке** — второйcandidate, если команда может безопасно записатьcontinuouswalk/fastwalk/run+transition+burst и измеритьfloor/time. Neuralpersondetector повторно использует первыйgeneralgraph;rollingvelocity иtimestamps самостоятельнаяtemporalпеременная. При требовании строгогоgait-run или отсутствииcalibration/capturetime/targetpack — опустить вreserve, не переименовыватьzoneoccupancy в бег. [F019](#F019),[F020](#F020),[Q007](OPEN_QUESTIONS.md#Q007),[Q008](OPEN_QUESTIONS.md#Q008).
3. **№4 visibleflame outside allowedROI**, smokingexcluded — conditionalthird. Собственнаяflameclass,PTbytes/names,positive/confuser/allowedpolicyreplay готовят более честный независимыйpattern,чемвтораяgenericzone. AdditionalcustomNN/exportAGPL иmedia/ROI/cut/targetcontrols требуют gate. Приcatalogonly безfireclass исключить; названиеsmoke не создаётfire/smoking. [F026](#F026),[Q012](OPEN_QUESTIONS.md#Q012).

**Резерв1 №2movingforklift image-spacepair:** включить вместо слабоготретьего,еслиполучены разрешённыеtargetpair+stationarynear/driver/farcontrols,принят standaloneweightscope иNNdevicepath. Сейчасsynthetic00238 полезен internalroute,неcompleteindustrial/publicroute;метры/TTCзапрещеныбезgeometryproof. **Резерв2 №3near-cameraphone suspicion whilemoving:** толькоеслиразмер/видимость/use-vs-carry/radio/scanner реальноразделяются,targetrights иdevicecontrolsпроходят;COCObboxсамнетuse. [F022](#F022),[F024](#F024).

**Infrastructure fallback:** один personzone/corridorepisode на реальномCCTV0_te23/4_te1 полезен дляintegration/journal/dedup. Он учитывается **одинраз** и не закрывает автоматически№2или№5. Отдельное согласование scope с экспертом может сделать его принимаемым сужением; это ответорганизатора,не ужеустановленныйфакт. Приcatalogpersononly можно делатьtracks/geometry,нонеобещатьmissingpose/phone/flame/forkliftfeatures. [K001](CRITIC.md#K001),[Q003](OPEN_QUESTIONS.md#Q003).

<a id="F005"></a>
## F005 — Три архитектуры и decision gates

| Архитектура | Что выполняется где | Условия выбора / блокеры | Первое доказательство | F/Q/E |
|---|---|---|---|---|
| A. Detector/pose наLinQ + hosttracker/rules | NNforward на реальномLinQ;hostdecode/preprocess/NMS/association/PTSrules/ledger/UI,если граница разрешена | VM+matchedcompiler либоmanagedcustomservice;exactmodel/hash/alloutputs/precision;hostboundaryapproval. НеобязательноSSH | Организаторскийgoldencompletion/proof,потомодинсвойexacttensorparity;послеэтогоepisode | F010–F015/F034;Q001–003;E001/002/009 |
| B. Temporal/action NN наLinQ | Pose+heatmaps/actionmodel либоRGBtemporal,causalwindow;hostepisode/policy | Толькоесликонкретныеgraphs/runtime/operators/T/shape/cadence/weightsgrant иdevicepathдоказаны. PoseC3D/TSSTG/SlowFastсейчаснепрошли. Неcriticalpath | Actualexport/allI/O+hostreference+frontend/compile/deviceparityнаодинаковомокне. YOLOsupportнеConv3D/attentionproof | F016/F025/F028;Q016;E010 |
| C. Catalog-limited inference service | DeviceNNcatalogID;hostadapterполучаетbbox/keypoints/classmap/timestamps;дальшеfeaturesufficiency+rules | Exactcatalogmanifest/golden/license/responseordering/quota/backendtrace. Catalogpersononlyнеможетсоздатьfire/forklift/use/pose. ManagedvideoUIбезmachineoutputsнеподтверждаетintegrableMVP | Одинcataloggolden+differentinputs+completion/modelversionproof;потомвыборсценариевтолькопореальнымoutputs | F010/F011/F034;Q001–003/019;E001/009 |

Отдельно внутриA: runtime-onlyVM нуждается в штатной компиляции оператором/сервисом и acceptableturnaround; получение `.tpu` безidentity/targetchain не закрываетcustomroute. При отсутствии actualdevicepath остановитьLinQclaim и запроситьworkingbaseline;hostresearchможетпродолжатьсякакhostresearch. СуществованиеpublicFramework2025 неlockдляRuntime16.18.6/Framework2026.8.43.

<a id="F006"></a>
## F006 — Первые упорядоченные smoke tests

Все шаги **предлагаются; NOT_RUN**. Никаких выдуманныхCLI/API/endpoints. Сначала три доказательства: **выданныйgolden наdevice → exactownNNparity → одинfullpositive+hardnegativeчерезepisode/journal/UI**.

1. Зафиксироватьteamgrant/runbook,VM/service/custom/catalogрежим,actualSDK/compiler/runtime/target/device,licenses,quota/expiry;получитьbaseline/hash/input/output и acceptedbackend/completionproof. Выполнитьтолькоштатнуюдиагностику;import/health/devicevisible неNNcomplete. [E001](OPEN_QUESTIONS.md#E001).
2. Runbaseline;сохранитьinputhash,request/job/model/program IDs,accepted→completedtrace,outputcopyпослеcompletion,backendcoverage иtimers. ПриFAIL/UNAVAILABLE следующиеdevicegatesNOT_RUN. FastHTTP/TLM/cachedoutputнеPASS.
3. Одинсвойcandidate:YOLOXnanofullhash изF014,checker/hostsanity **доPTQ**;historicalBGR/RGBambiguityрассматриватьобъявленнымdiagnosticcomparator,неадаптациейнаtestзаднимчислом. Savepreparedtensor/rawoutputs/decoderконфиг. Поdeviceподатьтотжетензор;неполучитьидеальнуюparityодинаковоошибочногоpreprocessingивыдатьеёзаcorrectperception. [E002](OPEN_QUESTIONS.md#E002).
4. Frontend→float→PTQ→compile→deviceoutputs отдельны. Saveeffectiveargs/quantparams/calibrationsplit/graphhash/coverage;unsupportednodeфиксироватьточно. Poseвыбиратьтолькооднуroute:RTMPoseSDKRGB2outputs/staticderivativeлибоofficialposeexport,необасразу. Opsetheadereditнеconversion.
5. Полныеlegalpositive+hardnegative сPTSGT→NNdevice→tracker→rule→persistentepisode→oneUIcard/journal. Дляfall использоватьреальныеHbounds/censoring;ACKнеclear;lossнеlowmotion/safe. [E003](OPEN_QUESTIONS.md#E003),[E009](OPEN_QUESTIONS.md#E009).
6. Повторитьcontinuouslongactive,unknown/reacquire,twoentities,clear/re-entry,retry/out-of-order/restart. Orderedtick,exactly-oneassimilation,source/epochnamespace;predictedbboxнеevidence. [F034](#F034).
7. Послеcorrectness — pacedreplay,source10/5/2/1FPS какварианты,несколькофаз+burstgap;warm/cold/device/RPC/queue/pre/post/confirm/visiblelatency отдельно;fail/drop/late/unknown/FNвзнаменателях. Two-streamfairness толькоеслинужно,неclaimcapacityизTOPS. [E005](OPEN_QUESTIONS.md#E005).
8. Freezeверсиюmodel/rule/ROI/cadence/H/G/N/D,отдельныйblindsession/actor/camera;revieweddevclipsнеholdout. МалыйsmokeнеfactoryFP/hour/reliability. [F033](#F033),[E004](OPEN_QUESTIONS.md#E004).

<a id="F007"></a>
## F007 — Stop-list на оставшийся хакатон

**Условный инженерный вывод, не запрет дальнейшего R&D:** не брать одновременновсесети;необучатьheavyactionstackбездоказаннойнеобходимости/доступа;нечинитьONNXпростымopset/IRheaderedit;непереносить84/85-onlydecoderна6/7/17/56channels;невыбрасыватьsimcc_y;необъявлятьdeviceFAILпопроблемеpublicadapter. НеиспользоватьThalosscaffoldcheckpointдляharness (actualroadclasses),Re-surgencevestкакharness илиgenericyolov5mкакtrainedclimb. [F012](#F012),[F028](#F028),[F030](#F030),[F031](#F031).

TSSTGupstream404/неполныйgrant,PoseC3DConv3D/heatmapcausalroute,UPTDrive/DETR/proposals,AVASlowFast иR3E6неустановленныйgrant — резерв/референсы,некритическаяпоставкакдедлайну. Raidavidsegmentepochs1неподменятьзрелымfire-detector;OpenVINOIRнеLinQartifact. SmokingдальнегоCCTV,connectedhook/allowedanchor иmass/effortcarrying безobservableinputsисключитьизуниверсальныхобещаний. «Untrained»descriptionненастоящеедоказательствоисторииtraining. [F016](#F016),[F024](#F024)–[F031](#F031),[F035](#F035).

Неумножатьоднуzoneна№2/№5;необъявлятьphonebboxuse,smokesmoking,lyingunconscious,harnessconnected,bboxoverlapunderload,pxметрами,t*collisionTTC,absenceofdetectornegativeGT. Неудлинятьrealholdзаморозкой/loop и неразноситьсоседниеframes/overlappingchunks/synchronousviewsвнезависимыеsplits. Globalcooldown,permanenttrackblacklist,first-seentimer,unchangedempty-skippingcallback идт-onlypatchнеготовыйonce-per-eventroute. [F003](#F003),[F034](#F034).

Необнулятьустановленныеcopyrightgrantsиз-заresidualconsent:fourcoreMP4CCBYidentityдоказана. ОдновременнонеобъявлятьcodeApache/MITуниверсальнымweight/media/SDKgrant инеобъявлятьEnterpriseавтоматическиобязательнымдлялюбойзащиты. Не публиковатьresearch-evidencebundle автоматически. НиCPU/RTX/mock,ниexport/compile,TLM/vendorFPSнеLinQdevice/eventPASS. [F015](#F015),[F026](#F026).

<a id="F008"></a>
## F008 — Адресные handoffs соседним темам

| Topic | Передаваемый предмет и решение | Evidence / остаток |
|---|---|---|
| linq_platform | Выданныйrunbook/target/customupload/catalog/golden/acceptedproof;2outputrectangularpose/customchannels;публичныеверсиинесклеивать | F010–F014;Q001–004/019;E001/002 |
| model_stack | Fullhash+actualYOLOX/RTMPosecontracts;BGRhypothesisambiguity;oneposepath;code/weightlicenses;actualcustomexportsещёотсутствуют | F012/F014/F015/F022/F026/F028/F035;Q005/010/016;E002/010 |
| violation_methods | Dynamicobservablesиscope8сценариев,zonefallbackучитываетсяодинраз;use/connected/underloadнеизbbox | F003/F016/F019/F021/F024/F027/F029/F031;Q007/011–015 |
| datasets | Actualfiles/PTS/SHA/primaryidentity;sourceclassmapping/fence9swap;XMLGTerrors;newholdout/permissionedcapture | F015/F017/F018/F020/F022/F023/F025/F026/F030/F033;Q006/008/009/017/020 |
| evaluation | One-to-onematching/eligible/censored/initial/unknown;FNвtimelydenominator;duplicates/FPраздельно;sourcevsmonotonicclocks | F013/F017/F033/F034;Q006/018/020;E003–009 |
| training_strategy | Сейчасinference-first,no training;PTQcalibrationотдельноотdev/test;domain/tiny-object/posecropданные | F012/F014/F026/F032/F033;Q002/005;E002 |
| video_architecture | Fixedcadence/emptytick/preassociationTTLprune;epoch/request/late/dropreasons;boundedqueues,sourceage,fairness | F013/F034;Q018/019;E005/009 |
| operator_product | Keyedonecard/episode,ACKнеclear,uncertainty/unresolved/recovery,rawmodelscoreнеviolationconfidence | F001/F034;Q003/018;E009 |
| hackathon_strategy / market_deployment | Условныйshortlist/stop/gates,сквозноедемо,реальныйLinQproof;publicdeliverable/manifestrights,никакихproductionreliabilityclaims | F004–F007/F015/F026/F033;Q001/003/017 |

Передача означаетфайлы/проверяемыелокаторы;другиетемынезапускалисьи внешнимлюдямничегонеотправлено. Соседниемашинныеотчётывветкахиспользовалиськакleads,некакнезависимаярепликация.

<a id="F009"></a>
## F009 — Реестр противоречий и правил разрешения

| Объект / конфликт | Что установлено | Что не разрешено / следствие | ДетальныеF/K/Q |
|---|---|---|---|
| YOLOX release0.1.1rc0 sourceTag12AugRGBnormalize,asset18Aug,body19Augnormremoval,currentREADMEтотжеURLсBGR | Exactbytes/hash/graphrawdecodeизвестны;выбранcurrentdocumentedBGRrecipe | Неполученempiricalartifact-matchedgolden;необъявлятьlegacyлибоBGRисторическидоказанным | F014;K003;Q005/E002 |
| RTMPoseJSONexpectedstatic17 vsactualsymbolicdims | Actualinputbatchsymbolic,обаoutputjointaxisсимволические;384/512установлены | Configbody17ещёнезаменяетactualruntimeaxis17;нужнаstaticderivative/shapevalidation | F014;K003;Q002/E002 |
| RTMPose rtmlibBGRcaller vsSDKto_rgb:true;meanvsminscore | FullcallerchainпрямойBGRбезswap;wrapperaxismaxmean,MMPose1.1min | ОдинSDKRGBaffinereferenceвыбран,численнойparityнет;неусреднятьконтракты | F014;K003;Q005/E002 |
| Officialpose release8.3.0 vsembedded8.0.77;metadataAGPL vssource8.0.77GPL | ExactPTfullSHA/embeddedAGPL;historicalGPLsourceисовременнаяownerAGPLpolicyсохранены | СтарыйtrainingcodeнеотменяетlicenseexactPT;v8.2.0same-sizeнеbyteidentity | F014/F015;K003/K008;Q017 |
| GMDCSArootMIT vsZenododatasetCCBY;3actorsvs4subjects;READMEv2.0vsactualv2.1 | MediaCCBYявно;core2ZIPmemberidentityproved;consentpublicrepoauthorstatement | Grantsневзаимоотменяются;полныйpersonalreleaseнеполучен;fournewclipsнеобъявленыallZIPverified | F015/F017/F018;K008;Q017 |
| SafeUnsafepage24FPS vsactualVFR23/25;classsafevsotheractor | DecodedPTSкаждогофайлаимеютприоритетдляreplay;labelclip неallpersonGT |0_te23initialoccupancyнеentry;2coreprimarySHAidentityclosed,3/7routeнеобобщать | F015/F022/F023;K005/K008;Q009/020 |
| Weizmannpage50FPS vsencoded25/subsampled | ActualAVI25fps,PTSиframesизвестны | Physicalcapturetime/метрыиsame-tracktransitionневыведены | F020;K006;Q008 |
| FURGXML29FPS/extraindex/staleboxes/emptyflame | Actual2997/100FPS;end+1rows;cuts246/443;BBQempty596–602/639–641сvisiblefire | Нетуниверсальногоglobaloffsetfix;нужнаcurationdelta,невыдаватьsourceGTperfect | F026;K007;Q012/E007 |
| Thaloscardharnessvscheckpointroads,filenameразличается | Actualscaffold_harness_weights.pt map0literal2,1barrier…7pothole | Отклонитьexactrevisionдляharness;неправитьcardmapвместореальныхweights | F028/F031;K001/K008 |
| CigaretteONNXdescription(untrained) | Exporterv8.0.145ставитстрокупоargs.data | Историяtrainingunknown,неоказаласьдоказанноrandom;loaderlayout/pathнесогласованыотдельно | F027;K007 |
| Fence_Securitysample9walking/climbIDsпереставлены | All14obj.namesпрочитаны;explicitpersourcemap | Finaltrainingharmonization/custombestunknown;genericYOLOv5mнетtrainedclimb | F030;Q013 |
| Vendor2026ResNetpage3vs4,throughput4xlatencysame | Textparsersповторилиvalues,officialpressprovenance | Bytes/visual/methodology/checkpointunknown;нельзяиз1/FPSполучитьSLA/numbercameras | F010/F013;K010;Q004 |
| W1firepreferencefarhatvsW2rabah | W2обоимfullbytes/namesподтвердил,cardrabahболееинформативна | Readinesspreferenceтеперьrabah;quality/speedwinnerнеизмерен | F026;K007;E007 |
| TTLпослеassociationвByteTrack | Lostможетreactivateдоexpiry;frame_rateменяетbuffer,неF/Q | ДлястрогогоTTLprepruneвadapter;dt1fixedgridнеавтоматическаяошибка,variable-dtpatchневыбран | F034;K009;Q018/E009 |



## Подробные канонические записи

Исходные W1/W2 ID внутри выписок — provenance locators, а не новые canonical IDs. Сборщик объединяет записи по объекту; repeated core metadata/общие smoke-планы убраны там, где W2 даёт сильнейшее основание. Исторические W1 statements сохраняются с явной отметкой, что изменилось. Приоритет не «W2 всегда прав», а более точное доказательство того же exact artifact. Ссылки на later override находятся в начале каждой записи.

<a id="F010"></a>
## F010 — LinQ: актуальная публичная граница и vendor table

**Нормализованный статус и условия:** Итог второй волны; actual grant/runtime/device NOT_RUN. Таблица только text-extracted reported measurement, visual verification unavailable.

**Источники:** [S002](SOURCES.md#S002), [S003](SOURCES.md#S003), [S004](SOURCES.md#S004), [S005](SOURCES.md#S005), [S006](SOURCES.md#S006), [S007](SOURCES.md#S007), [S008](SOURCES.md#S008).

**Происхождение:** [W2-01.md](_WORK/W2-01.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Дата доступа: **2026-10-23**. K001/K002/K010. Собственная работа второй волны: адресное открытие первичных страниц, PDF text parser и ограниченные GET; без регистрации, переписки, SDK, компиляции, инференса и изменения хоста. **Hardware: NOT_RUN. Team grant: UNKNOWN / не обнаружен в выданных входах.** Единственный итог этой ветки — этот файл.

#### Решение и изменение относительно W1

**Текущего публичного runbook/catalog/SDK release contract именно хакатона не найдено в проверенных источниках. Финальная развилка — `requires organizer/access`.** Это ограниченный отрицательный результат поиска, а не доказательство, что документов нет в кабинете или чате. Доступ команды нельзя установить публичным сайтом.

Новый положительный результат: официальная страница пресс-центра сейчас непосредственно ссылается на `2026_linq_presentation.pdf`; переход по ссылке позволил второму, независимому от TinyFish PDF-парсеру открыть документ как 13 страниц и повторно проверить page locators строк таблицы. Это усиливает происхождение и текстовую сверку W1-15-S01/F01, но **не закрывает K010**: локальные исходные bytes/hash не получены; фактические изображения инструменты не передали. Статус остаётся **`text-extracted reported measurement, visual verification unavailable`**. Ни строка pose, ни имена версий в footer не образуют matched artifact или team grant.

Прочитаны W1-13 полностью и соответствующие S01/F01 W1-14, S01/F01–F03 W1-15, включая их ограничения и отрицательные попытки. Их сведения о выданной среде не повышены до наблюдённых фактов. Применён PDF skill для read-only проверки; render не объявлен выполненным.

#### Новые первичные источники

`current HTML` означает живую страницу без immutable revision. Last-Modified ниже — наблюдённый HTTP validator через TinyFish, **не дата публикации, релиза или выдачи команде**. Все обращения 23.10.2026.

| ID | Exact URL и локатор | Наблюдение, версия и граница |
|---|---|---|
| **W2-01-S01** | https://lin-q.ru/docs — раздел «Фреймворк» и все outbound links; fresh TinyFish fetch, ttl=0 | Открыт полный список публичных ссылок. ETag `"1e747-651d790ad7793-gzip"`; Last-Modified `Fri, 15 May 2026 09:09:07 GMT`; published_date=null. Единственная ссылка раздела Framework ведёт на S02; новых release notes, model manifest, current service API/runbook здесь нет. Robots noindex,nofollow объясняет, почему одной поисковой выдачи недостаточно. |
| **W2-01-S02** | https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf — титул; печатные с.5, 20–24, §3.4 | Заново открыт TinyFish text, а не унаследован из W1. Титул **2025**, `RU.РМДВ.04.06.014-03 34 01`, 28 листов. Это всё ещё историческое руководство IVA H1, не matched release 2026.8.43/16.18.6 и не инструкции сервиса хакатона. |
| **W2-01-S03** | https://lin-q.ru/press — «Материалы» → «Презентация» | TinyFish fresh outbound links и web click проверили exact target S04. ETag `"39f38-65b7389c31d7b-gzip"`; Last-Modified `Mon, 14 Sep 2026 16:00:50 GMT`; published_date=null. Непосредственная первичная provenance link, не URL из стороннего отчёта. |
| **W2-01-S04** | https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf — физические страницы 3/4, zero-based P2/P3 | TinyFish extraction и независимый web PDF parser при переходе с S03; PDF parser сообщает application/pdf, **13 страниц**. Текстовые локаторы P2 lines35–45 и P3 lines46–65. Дата 2026 по титулу; published_date=null, author по extraction «Севрюков Сергей». Байтовая идентичность с экземпляром W1 не доказана. |
| **W2-01-S05** | https://lin-q.ru/tech — «Поддерживаемые сети», lines58–107; https://lin-q.ru/sol#linq_soft — раздел ПО | Свежий web open: семейства YOLO8/YOLO11 и pipeline квантования/графа названы, exact checkpoint/hash/output schema не даны. У ПО общий закрытый download path через регистрацию/верификацию, не публичный хакатонный grant. Нового contract относительно W1-14-S01 не найдено. |
| **W2-01-S06** | https://hackathon2026.otkroimosprom.ru/ — LinQ case | Свежая первичная страница открыта; актуальные материалы с интерфейсом команды в прочитанном публичном разделе не появились. Обещание доступа не повторяется здесь как новое доказательство интерфейса. |

#### Факты и границы

**W2-01-F01 [DOCUMENT OBSERVED].** В текущем public docs index по-прежнему опубликован guide2025. Его пример различает симуляцию TLM и реальное устройство: с.20 перечисляет/открывает TPU, загружает `.tpu`, с.21 выполняет blocking `inference.sync`, с.24 показывает отдельные результаты Original/Quantized/TLM/TPU. Это полезный исторический образец различения backend, **не принятый организатором proof текущего сервиса**. Импорт `tpu_framework` с exit0 проверяет установку, а не устройство. Поэтому не считать ни import, ни TLM execution_time, ни быстрый HTTP ответ hardware PASS.

**W2-01-F02 [TEXT-EXTRACTED REPORTED MEASUREMENT].** S04 подтверждён первичной ссылкой S03 и новым PDF text parser. Заголовки: HP/HPQ, под каждым Throughput FPS и Latency ms. Физическая с.4, строка14 `yolov8n_pose`, batch1: HP **104.8 / 21.51**, HPQ **419.2 / 21.51**. Строка13 `yolo5s`: **106.1 / 23.71**, **424.4 / 23.71**. Footer на P3 называет MLCommons MLPerf; CPU i7-10700K 3.80GHz, Ubuntu24.04, Runtime16.18.6, Framework2026.8.43. P2 даёт ResNet50 HP460/1046 FPS b1/b8; P3 —432.9/1112.8. Расхождение сохранено, не исправлено. Визуальное положение/единицы не подтверждены изображением.

**W2-01-F03 [UNKNOWN / LIMITED NEGATIVE SEARCH].** За pose-строкой не найден matched manifest/download/checksum, input shape/precision/checkpoint, pre/post recipe, golden tensors или compile log. Ни в открытом PDF-тексте, ни в outbound links S01/S03 нет указателя на отдельную методику этой строки. Footer задаёт название методики, но не scenario/revision/config, нагрузку, границы таймера, percentile и accuracy run. Не утверждаем MLPerf submission/certification. Generic YOLO8 family не идентична конкретному `yolov8n-pose.pt`; права кода, весов и данных отдельны. Сведения о chip count не доказывают причину одинаковой latency при четырёхкратном throughput.

**W2-01-F04 [OBSERVED ACQUISITION FAILURE].** Небольшие штатные попытки получить исходник:

- urllib HTTPS exact URL → `SSL: UNEXPECTED_EOF_WHILE_READING`; HTTP → `RemoteDisconnected`.
- urllib HTTPS `?download=1` → тот же SSL EOF; requests exact URL с Referer `/press` → SSL EOF.
- curl.exe HEAD exact URL → code35, schannel SSL/TLS handshake failure.
- Прямой web open сначала Internal Error; web **click** S03 «Презентация» успешно открыл PDF parser. Следовательно, нельзя заключать, что файл отсутствует или вообще закрыт.
- screenshot(P2/P3) через оба web интерфейса вернул ссылки/маркеры `<<ImageDisplayed>>`; инспекция фактического result.content дала только `{type:"text",keys:["type","text"]}`. Ни ImageContent, ни image bytes/path не переданы модели. Это вызов screenshot, **не визуальная инспекция**. Повторение такого маркера не делает единицы визуально проверенными.
- Browser inventory CUA пуст (`[]`), iab unavailable. Никакие браузерные security interstitial не обходились. Локальный PyMuPDF доступен, но без PDF bytes нечего рендерить.

**Исходный PDF bytes = NOT_ACQUIRED; size/hash = UNKNOWN; local rendered slides = NONE.** Hash извлечённого текста, ETag HTML и web page count не подменяют SHA-256 полного PDF. Временный PDF-файл не создан. Это точный остаток K010.

#### Адресный поиск и rejection

Поиск выполнен с открытием первичных результатов: `site:lin-q.ru "2026" "SDK"`; `site:files.lin-q.ru "2026_linq_presentation.pdf"`; `LinQ хакатон 2026 SDK инструкция каталог моделей`; `site:lin-q.ru "2026" "документация"`; `site:files.lin-q.ru/tpu "2026" "Framework"`; `site:lin-q.ru "yolov8n_pose"`; `"2026_linq_presentation.pdf"`; `"yolov8n_pose" "21,51"`; `"TPU Framework" "2026.8.43"`; `site:files.lin-q.ru "Runtime" "2026"`; `site:lin-q.ru хакатон октябрь 2026 инструкция`; `site:lin-q.ru "каталог моделей"`; `site:lin-q.ru "release" OR "runbook" OR "API"`.

Полезные кандидаты: S01 index, S02 для исторической границы runtime/TLM, S03→S04 для происхождения и reported pose measurement. Отклонены как current contract: Automata LINQ SDK (другая платформа), linqapp messaging API (другая платформа), vendor story о другом «Цифровом прорыве» (иное соревнование), грантовая новость «Создай НАШЕ» (не team access), family list без artifact ID. Поисковые snippets не принимаются вместо открытия. Недоступный прямой `/materials` не интерпретируется как отсутствие раздела: настоящий найденный locator — `/press#linq_press_mat`.

#### Known / documented / unknown

| Область | Known здесь | Documented первичным источником | Unknown, необходимое для решения |
|---|---|---|---|
| Public contract | Проверены docs/press/tech/sol и открытый case; нового current runbook не найдено | Guide2025; презентация2026; generic model families | Выданная версия, target, runbook, auth команды |
| Own model | Ничего не загружено/скомпилировано | Исторический compile→`.tpu` path | Право custom upload/update; matched compiler; реальные ограничения |
| Catalog | Exact service model ID не найден | Вендор называет семейства и pose benchmark row | Artifact/hash, I/O, классы/keypoints, preprocessing, golden outputs |
| Completion / device | Ни одного запроса к LinQ | Исторический guide различает TLM/TPU | Job completion, backend trace, согласованный jury proof |
| Host boundary | Не проверена | Guide пример имеет пользовательскую обработку | Разрешённые decode/pre/post/tracking/rules в текущем кейсе |
| Resource/time | Измерений нет | Версии footer относятся чужому измерению | Quota, queue, concurrency, модельные слоты, compile turnaround |

#### Результат по K и поведенческое следствие

| K | Результат этой ветви | История / что осталось |
|---|---|---|
| **K001** | **scoped, глобально open** | Доступный public catalog не установлен; поэтому выбор 2–3 исходных поведений не подтверждён каталогом. Generic zone считать инфраструктурой/fallback один раз. Public pose row — кандидат для запроса, не доказанная возможность конкретной команды. Другие W2 должны дать независимые positive/negative behavioral observations. |
| **K002** | **open — requires organizer/access** | От W1 uncertainty перешли к свежему ограниченному отрицательному результату docs/release поиска. Public document найден; team grant отсутствует среди доказательств. Эти два утверждения не противоречат друг другу. |
| **K010** | **scoped, open по bytes/hash/visual/methodology** | В W1 была только TinyFish extraction; теперь independently parsed PDF через официальный source link и 13-page metadata. Числа повторились, contradiction не обнаружена в текстах; визуальная сверка и byte identity всё ещё unavailable. |

Позитивный условный case: выданный catalog detector реально возвращает person bbox с timestamps → можно отдельно проверять бег по траектории против ходьбы; pose golden возвращает keypoints → проверять падение с переходом и последующей наблюдаемой неподвижностью против наклона/лечь добровольно. Это **proposed experiment**, не успешный прогон. Негативный case: person bbox + polygon occupancy не наблюдает движение техники и не доказывает перелезание; два названия зон не дают два исходных поведения. Даже достаточные output channels без device proof не закрывают LinQ criterion.

#### Пять срочных технических вопросов (заготовка, не отправлена)

1. **Own upload/compile:** какой точный режим и runbook выдан команде; разрешены свои weights/update, какой входной формат, где matched compiler/runtime/target и минимальный рабочий пример?
2. **Golden/catalog outputs:** дайте exact model IDs/artifact hashes (особенно pose), I/O schema, классы/keypoints, preprocessing/postprocessing и один golden input/output; соответствует ли pose из таблицы доступному artifact?
3. **Completion/device proof:** что означает completed response/job и какой backend/device evidence с request/model/version correlation принимается жюри; как отделить TLM/CPU и device time от queue/round-trip?
4. **Host boundary:** разрешены ли на host decode, letterbox/crop, NMS, tracker и временные правила; какие NN-части должны исполняться LinQ и как это показывать?
5. **Quota/turnaround:** какие фактические QPS/concurrency/queue/timeouts/model slots, сроки compile/upload/update и срок действия доступа до дедлайна; какой резервный путь при отказе?

#### Три conditional routes и ближайший шаг

**A — собственная компиляция + runtime/VM.** Только после grant и matched package: vendor golden→проверенный device output/proof→один собственный detector→нужный behavioral candidate. Параметры не брать из guide2025 как ABI2026. На граф/квантование/качество нужны отдельные проверки.

**B — managed custom model / runtime-only.** Получить штатную compile/upload точку или оператора с format/version contract, затем model ID/hash и completed inference. Отсутствие SSH само по себе не блокирует этот маршрут. Очередь компиляции может сделать его невыполнимым по времени; это выясняется Q5, не маркетинговой страницей.

**C — fixed catalog service.** Получить exact output contract/golden, затем выбирать только поведения с достаточными временными наблюдениями; host rules при разрешении. Если каталог не выдаёт достаточных признаков, запросить B/изменение scope. Zone fallback не засчитывать несколькими сценариями.

**Ближайшее требуемое доказательство:** официально выданный команде runbook + один golden input/output + принятый completion/backend proof. После выдачи команда выполняет baseline→candidate→device proof и свои замеры. Исследовательский статус остаётся **NOT_RUN**, без численных accuracy/FPS/SLA. Отдельный остаток K010 — штатно получить PDF bytes с SHA-256 и изображения физических страниц3/4; только после личного просмотра закрывать visual, а без matched manifest/methodology не закрывать переносимость pose-строки.

<a id="F011"></a>
## F011 — LinQ: исторический guide, режимы доступа и completion proof

**Нормализованный статус и условия:** Публичный поиск обновлён F010; guide2025 не текущая ABI. Наличие VM/сервиса в кейсе не означает выдачу команде.

**Источники:** [S002](SOURCES.md#S002), [S003](SOURCES.md#S003), [S008](SOURCES.md#S008), [S009](SOURCES.md#S009), [S010](SOURCES.md#S010), [S011](SOURCES.md#S011).

**Происхождение:** [W1-13.md](_WORK/W1-13.md), `## Новые первичные`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Новые первичные источники и факты

Все URL открывались 23.10.2026. Локаторы web-линий служат ориентирами чтения, не неизменяемыми версиями страниц. У публичных HTML release/commit отсутствует; это прямо указано.

| ID | Источник, версия и локатор | Что установлено и граница доказательства |
|---|---|---|
| **W1-13-S01** | Локальный кейс `_WORK/INPUT/КЕЙС_LinQ.pdf`, с.8; визуальный артефакт `_WORK/CASE_PAGE_08.png`; hash выше | Первичный материал организаторов в пользовательском экземпляре. Два обещанных ресурса; предоставление данной команде не проверено. |
| **W1-13-S02** | [Официальный сайт хакатона](https://hackathon2026.otkroimosprom.ru/), раздел LinQ, web lines 266–277, undated current HTML | **W1-13-F05 [DOC]** Инференс обязателен на LinQ, участникам обещан онлайн-доступ; постановщик ООО «ХайТэк». Сайт не описывает API/VM. Публичные примеры нарушений не заменяют полный локальный кейс. |
| **W1-13-S03** | [Документация производителя](https://lin-q.ru/docs), раздел «Фреймворк», lines 62–66, current HTML | **W1-13-F06 [DOC]** Без авторизации прочитан список публичных документов и ссылка на руководство. Публичный PDF не равен полученному пакету поставки. Первый open дал техническую ошибку, повторный прочитал страницу: это не признак запрета доступа. |
| **W1-13-S04** | [Руководство оператора IVA H1](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), **2025, RU.РМДВ.04.06.014-03 34 01**, печатные с.5–7, 11–13, 20–22 | **W1-13-F07 [DOC]** Условия руководства: Ubuntu 20.04, Python 3.11, RAM ≥32 GB. Пример поставки — wheel `tpu_framework`. Описаны ONNX→TensorFlow→квантование/компиляция→`.tpu`; Framework и runtime разделены. Пример открывает устройство, загружает программу, выполняет синхронный запрос; TLM рассматривается отдельно. Пред-/постобработка задаются пользователем. Список протестированных семейств включает tiny_yolo3 и yolo5s. Это документация поколения, не перечень моделей выданного сервиса, не текущая ABI и не гарантия поддержки любого ONNX. |
| **W1-13-S05** | [ПО и устройства LinQ](https://lin-q.ru/sol), раздел ПО lines 273–293; характеристики HP/HPD/HPQ/HPS/HX, current HTML | **W1-13-F08 [DOC/CLAIM]** На странице ПО указаны Python API/CLI, OEM-поставка, регистрация и верификация для загрузок. Публичное описание Python 3.8 отличается от S04: это разные контексты, не готовый lock. Характеристики продуктов не определяют выданную VM. |
| **W1-13-S06** | [Вход производителя](https://lin-q.ru/members/login), [регистрация](https://lin-q.ru/members/signup/group/zu1sdzcxrlvhqmf-fw2) | **W1-13-F09 [ACCESS OBSERVATION]** Прямые web open вернули техническую недоступность. Формы не отправлялись. Верификацию и процедуру выдачи по этим неудачным запросам установить нельзя; требование верификации подтверждено S05. |

#### Поисковый след и локализованное неизвестное

Новый поиск включал запросы `site:lin-q.ru регистрация верификация программное обеспечение LinQ`, `"LinQ" "хакатон" "API"`, `"LinQ" "хакатон" "виртуальн"`, `site:lin-q.ru "хакатон" "2026"`, `site:hackathon2026.otkroimosprom.ru "LinQ" "сервис"`. В открытых результатах не найдено актуального первичного runbook/API именно хакатонного доступа. Перепечатки и агрегаторы Telegram не использованы как подтверждение интерфейса. Исследование публичного сайта не равнозначно чтению закрытого канала организаторов: актуальные приватные разъяснения остаются неизвестны.

Небольшой read-only GET `https://lin-q.ru/sol` через локальный Python завершился SSL EOF; web позднее прочитал полный раздел ПО. Ошибка одного клиента не интерпретируется как отсутствие документа. Новых endpoint, API-версий и SDK-дистрибутивов не придумано.

**Происхождение:** [W1-13.md](_WORK/W1-13.md), `## Матрица known`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Матрица known / documented / unknown / ask organizers

`known` — непосредственно наблюдено здесь; `documented` — заявлено применимым источником, без аппаратного подтверждения; `unknown` — пробел. Все вопросы — заготовки, **не отправлены**.

| Вопрос | known | documented | unknown | ask organizers |
|---|---|---|---|---|
| VM и сервис | Доступ не использован; реквизитов во входах не найдено | Оба обещаны с.8 [S01] | Выдаются оба, один на выбор, резерв, сроки? | Дайте runbook и роль каждого ресурса, порядок выдачи команде |
| SSH / VPN / web console | Не наблюдались | Конкретный протокол не назван | Адрес, auth, VPN, доступ из РФ/с площадки, expiry | Какой штатный способ входа; разрешены ли пять отдельных пользователей? |
| CPU/RAM/storage/GPU | Конфигурации команды нет | S04 описывает требования инструмента, не VM | vCPU, RAM, диск, наличие NVIDIA/VRAM | Какова выделенная конфигурация и свободное место? GPU вообще предоставляется? |
| TPU / память | Устройство не обнаруживали | Каталог содержит разные продукты [S05] | SKU, chips, assigned IDs, память на чип, свободная квота | Какой runtime target и какие устройства закреплены за командой? |
| Docker / установка | Ничего не ставилось | Кейс не гарантирует Docker/sudo | Container runtime, registry, permissions, persistence | Можно ли свои контейнеры/venv? Где утверждённый образ с digest? |
| SDK / compiler / runtime | SDK не выдан в найденных входах | Публичный документ S04; отдельные скачивания требуют verification S05 | Matched release, driver/firmware, лицензия, compiler location | Дайте совместимый набор и один полный рабочий пример для этой среды |
| Свои модели | Upload не проверен | Framework документирует обработку графов [S04] | Grant сервиса; custom weights/update; компиляция командой или оператором | Можно ли загрузить свои веса и обновить модель до защиты? В каком формате? |
| Форматы | Схема сервиса не найдена | Видео/изображения допустимы как данные кейса [S01] | Вход сервиса: файл, image bytes, tensor, stream, ONNX, `.tpu` | Дайте точный model/data contract, ограничения размеров и ошибки |
| Зоопарк | Ни одного service model ID не известно | В S04 есть список семейств | Точные artifacts, версии, классы, pose, лицензии, downloadable outputs | Дайте catalog с manifest/checksum/golden input/output, не только названия |
| Pre/postprocessing | Нет контрактов нашей модели | Пользовательские функции в примере S04 | RGB/BGR, layout, dtype, scale, letterbox, NMS, координаты | Что делает сервис и что должна делать команда? Версия схемы выходов? |
| Квоты / очередь | Замеров нет | Численная квота не найдена | QPS/concurrency, timeouts, fair use, model slots, resets | Каков гарантированный лимит и как отличить очередь от device time? |
| Сеть / данные | Закрытые адреса не проверялись | Конкретных правил нет | Internet egress, upload cap, RTSP, incoming port, retention | Где разрешены decode, хранение видео и web UI? Как передать небольшой тест? |
| Proof / оценка | Никакого device PASS здесь нет | LinQ и измерения обязательны по кейсу | Accepted evidence, допустимый host processing / partial NN | Какой журнал/экспорт счётчиков принимается жюри? Должна ли вся NN быть на TPU? |
| Права | Договор/лицензия поставки не найдены | OEM-условия на S05 | Использование SDK командой, выдача artifacts жюри, публикация весов | Какие файлы можно включать в сдачу/репозиторий? Есть ли ограничения видео? |

**Происхождение:** [W1-13.md](_WORK/W1-13.md), `## Access decision`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Access decision tree — четыре условных режима

Все ветви ниже — **ANALYSIS**, архитектурные решения после ответа организаторов. Ни один режим не заявляется уже полученным.

```text
0. Получен официальный runbook/ответ с режимом и сроком доступа?
   НЕТ → запросить пакет Q1–Q5; продолжать CPU reference/видео/правила,
         LinQ readiness = UNAVAILABLE. Не объявлять CPU demo LinQ demo.
   ДА → проверить auth штатным способом и срок действия.
        Не удаётся → сохранить код ошибки/время, обращаться в поддержку.

1. Есть программно вызываемый путь с реальным LinQ исполнением?
   НЕТ → есть только витрина/записанный пример → ещё не выполнено;
         нужен доступ к запуску и принятый организаторами proof.
   ДА → какой контракт?

A. VM/shell/container с runtime И разрешённой компиляцией своих графов
   → сохранить version/target/permissions; baseline организатора;
     custom graph → import/PTQ/compile → `.tpu` → runtime → output parity.
   → Если компиляции нет, перейти B; если устройства нет — проверить service B/C.

B. Managed custom-model service либо VM с runtime-only
   → определить точку приёма: graph / `.qm` / `.tpu` / иной официальный artifact.
   → Graph service: разрешённый формат + calibration + compile log + model ID.
   → Runtime-only: получить matched compile service/оператора/образ;
     upload `.tpu` без доступной цепочки подготовки ещё не делает модель переносимой.
   → Версия модели, запрос, результат, backend trace доступны? Да → smoke-test.
     Нет → уточнить proof; никакой произвольный HTTP ответ не считать TPU proof.

C. Сервис только с фиксированным каталогом моделей
   → запросить точные классы/выходы/частоту/числовой эталон.
   → Хватает наблюдаемых признаков выбранным сценариям?
     Да → правила/трекер на host при разрешении; NN остаётся на LinQ.
     Нет → сменить сценарий или запросить расширение; CPU второй detector
           не маскирует отсутствующий обязательный LinQ-признак.

D. Managed video/UI/jobs без прямого tensor endpoint
   → есть машинный экспорт bbox/keypoints/frame timestamps/request IDs?
     Да → адаптер jobs/files/events; проверить ordering, polling, quota, latency.
     Нет → можно ли расширить UI/достать данные официально?
       Да → согласованный extension route и новый contract.
       Нет → live integrable MVP не подтверждён; запросить B/C.
```

Если одновременно выданы VM и сервис, выбирать первую ветвь, которая проходит **baseline → признаки → proof → задержка**, а не более привычный транспорт. VM может оказаться host для клиента сервиса, а не PCIe passthrough; это надо спросить, не определить по слову VM. При смене модели заморозить новый manifest и заново проверить контракт/числовую и событийную цепочку.

#### Кандидаты и отложенные варианты

| Вариант | Решение | Причина |
|---|---|---|
| Полный matched пример организаторов + собственный detector | Первый кандидат при A/B | Уменьшает неизвестные ABI и компиляции; custom качество всё равно проверяется |
| Каталожный person/pose/person+vehicle detector + host temporal rules | Реальный кандидат при C/D и принятой границе NN | Может закрыть 2–3 сценария без собственной компиляции, если outputs достаточны |
| Самостоятельная установка старого публичного pytpu как «готового SDK» | Отложить | Public bindings не доказывают наличие native/driver/compiler и совместимость выданной среды; основание — лишь соседняя зацепка, не проверенный путь здесь |
| Считать перечень YOLO доказательством доступа к готовым весам | Отклонить | Семейство не определяет checkpoint, классы, формат выхода или service model ID |
| Подставить универсальный REST endpoint / ONNX opset13 / batch1 | Отклонить как обязательный контракт | В источниках хакатонного API не найдено; параметры экспорта могут стать пробой после выдачи требований |
| CPU/RTX inference с логотипом LinQ | Не удовлетворяет обязательному условию | Требование касается действительного нейроинференса на ускорителе [S02] |

**Происхождение:** [W1-13.md](_WORK/W1-13.md), `### Что считается`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Что считается успехом на настоящем устройстве

Минимальный reviewable bundle: `grant/runbook version → backend/device identity → model/program identity → input hash → request/job ID → completion trace → output → event → timings`. Для управляемого сервиса отсутствие доступа к PCIe допустимо при принятом организаторами backend proof; одного UI badge недостаточно. Самостоятельный файл `.tpu`, успешно завершившаяся конверсия, TLM и CPU parity находятся до этого критерия.

Различать два вопроса: **(а)** завершился ли этот запрос на LinQ; **(б)** какая часть конкретного NN-графа там выполнялась. Первое не доказывает второе. Для финальной демонстрации нужны оба в той форме, которую согласует постановщик.

<a id="F012"></a>
## F012 — ONNX/LinQ: adapters, operators, PTQ и структурно прочитанные smoking/SafetyVision

**Нормализованный статус и условия:** YOLOX/RTMPose полные actual graphs обновлены F014. Ограничения first-output/84–85 относятся к примеру linq-cv-bench, не самому ускорителю.

**Источники:** [S003](SOURCES.md#S003), [S006](SOURCES.md#S006), [S009](SOURCES.md#S009), [S012](SOURCES.md#S012), [S013](SOURCES.md#S013), [S014](SOURCES.md#S014), [S015](SOURCES.md#S015), [S016](SOURCES.md#S016), [S017](SOURCES.md#S017), [S018](SOURCES.md#S018), [S019](SOURCES.md#S019), [S020](SOURCES.md#S020), [S021](SOURCES.md#S021), [S022](SOURCES.md#S022), [S023](SOURCES.md#S023), [S024](SOURCES.md#S024), [S025](SOURCES.md#S025).

**Происхождение:** [W1-14.md](_WORK/W1-14.md), `## Первичные источники`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Первичные источники, новые открытия и версии

Все URL в этом разделе самостоятельно открыты 23.10.2026. Дата доступа не равна дате публикации. Номера строк ниже — 1-based raw files, перепроверены прямым HTTPS GET; web renderer может удалять пустые строки и показывать иные номера. Содержимое источников пересказано, не скопировано целиком.

#### W1-14-S01 — официальный LinQ, публичная граница

[Технологический стек](https://lin-q.ru/tech), секции «Поддерживаемые сети», «Собственное IP-ядро»; [ПО](https://lin-q.ru/sol), «Программное обеспечение». **A/B:** изготовитель заявляет int8 и семейства yolo8/yolo11; описание ПО даёт последовательность квантование/компиляция, Python API/CLI. Версионированного operator/opset/IR support table, правил dynamic shapes/batch, layout/precision каждого слоя в открытых страницах не найдено. Сайт указывает Python3.8; это не dependency lock для выданного хакатонного SDK. Требуются регистрация и верификация для закрытого скачивания. Публичная надпись CNN/RNN не доказывает поддержку конкретного Conv3D, LSTM или attention graph.

[Framework_manual_H1.pdf](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf) новым web.open недоступен (`Internal Error`); поэтому детали guide2025 ниже помечены как унаследованные из соседнего research, а не лично повторно прочитанный PDF. Унаследованный locator: RU.РМДВ.04.06.014-03 34 01, §3.4 и описание QuantizedModel; это не exact semver поставки2026.

#### W1-14-S02 — первичный сторонний exporter

[export_yolov8s_to_onnx.py](https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_yolov8s_to_onnx.py), owner sherstpasha, commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`. `parse_args`, opset L18, batch L19: default640, batch1, opset13, dynamic/simplify opt-in. `main`, `model.export` L63–70: Ultralytics export с `nms=False`; JSON metadata с L78. **A:** есть конкретный export code path. **U:** successful custom YOLOv8 compile, полученный hash ONNX/.tpu. Владелец не установлен как вендор LinQ; исходник не сертификация совместимости.

#### W1-14-S03 — builder, точные ограничения переноса

[build_yolov8_program.py](https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py), тот же commit, функции `force_static_onnx_input_shape`, `load_converted_graph`, `main`.

**A:** input ValueInfo переписывается на1×3×H×W; frontend пробует `tpu_framework.onnx_to_tf`, затем `onnx_direct.onnx_to_tf`, mapping имён. В `main` выражение `graph.output[0].name` L222, затем `output_nodes:[output_candidate]` L261 выбирает один выход. RTMPose требует обоих имён, всех TF mappings и output descriptions; переписывание header не специализирует Shape/Range/reshape nodes внутри графа. Fixed square calibration tensor этой функции также нельзя переносить на256×192 affine crops.

Путь: `RegularModel(original_graph_def,input_shapes,output_nodes)` → `calibrate` → `quantize(thresholds)` → save `.qm` → `Network.from_quantized_model` → `set_batch` → `compiler.compile_` → `TpuProgram.from_executable` → `.tpu`. Preset O1/O5/DEFAULT; `TPU_128x128_PARAMS` — hardware parameter, не размер картинки. В L276–278 любой TypeError calibrate повторяет вызов без percentile: такой retry скрывает effective parameter и не годится для контролируемого PTQ. Код прочитан, успех исполнения неизвестен.

#### W1-14-S04 — runner и dependency context

[run_yolov8_tpu.py](https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py), тот же commit: `normalize_prediction_shape` L176–183 (проверки84/85 на L179/L181) допускает только channels84/85; `pick_output` с L164 может выбрать один rank≥3 output. `main` L206 обращается к Unicode-атрибуту `args.output_tensอร์_name`, не соответствующему parser destination `output_tensor_name`: вероятен AttributeError. Синхронный inference затем host NMS. Нельзя переносить COCO80→91 mapping на custom classes или подавать pose keypoints в обычный detector NMS. `hasattr(run)`/перебор input names не заменяет установленный API contract; после ошибки нельзя вслепую повторять submit.

[requirements](https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/requirements.txt): numpy1.26.4, onnx~=1.16.0, onnxruntime~=1.18.0, TF2.14.1, torch без pin; SDK не поставлен этим файлом. [RUN_SCENARIO](https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/RUN_SCENARIO.txt), дата25.03.2026, §§1/3.4: TPU environment требует native libraries и реальное устройство, final detection path описан как vendor tiny_yolo3, не self-built YOLOv8. Это авторский план/код, без наших device measurements.

#### W1-14-S05 — Ultralytics head и export semantics

[head.py v8.3.74](https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.74/ultralytics/nn/modules/head.py), `Detect._inference`, `Pose.forward/kpts_decode`; [exporter.py v8.3.74](https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.74/ultralytics/engine/exporter.py), `export_onnx`. **A:** detect export уже выполняет DFL/box decoding и sigmoid class scores; `nms=False` не убирает их. Pose добавляет decoded keypoints. Generic detection output `4+nc`, classic anchor detector `5+nc` и post-NMS rows — разные схемы. Для static640 ожидается8400 позиций, но каждый exact graph нужно проверять. Exporter принимает opset/dynamic/batch; ONNX format не означает готовый PTQ int8 путь. Code AGPL-3.0; права custom weights/data/video проверяются отдельно.

#### W1-14-S06 — RTMPose runtime source

[rtmpose.py](https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/rtmlib/tools/pose_estimation/rtmpose.py), Tau-J/rtmlib commit `03a1693e59e4f7cd84582c0fb30459b3bf18ad42`, `preprocess` и `postprocess`. **A:** отдельный affine crop для каждой bbox, padding1.25, normalize mean/std; два SimCC выхода, argmax decode/ratio2 и inverse crop. Это не multi-person detector. В функции нет явного BGR→RGB reversal; SDK JSON из W1-08 требует to_rgb:true. Это локализованный preprocessing mismatch: нужен выбранный единый golden recipe, не молчаливое смешение двух wrappers. Code Apache-2.0; HF model card declaration и права datasets отдельно.

#### W1-14-S07 — ONNX, формат и версии операторов

[Официальный protobuf v1.17.0](https://raw.githubusercontent.com/onnx/onnx/v1.17.0/onnx/onnx.proto), ModelProto/GraphProto/NodeProto/ValueInfoProto — схема собственного bounded reader. [Concepts](https://onnx.ai/onnx/intro/concepts.html), [Resize](https://onnx.ai/onnx/operators/onnx__Resize.html), [Softmax](https://onnx.ai/onnx/operators/onnx__Softmax.html) — официальные определения. Opset import задаёт набор схем; `ir_version` — отдельная версия сериализации. Node не хранит отдельный номер каждого op: применима schema since_version≤domain import. Например при default opset19 применяются Resize19 и Softmax13; это версии ONNX, **не обещание LinQ support**. Простая замена opset19→13 либо IR number не является конверсией.

**Происхождение:** [W1-14.md](_WORK/W1-14.md), `## PTQ и runtime`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### PTQ и runtime: что известно и что требуется

**W1-14-F03.** FP32 внешний тензор не означает FP32 TPU арифметику; int8 железо не определяет внешний dtype. Нужны user↔raw rescale, scales/zero-points, signedness, per-channel/per-tensor, accumulator precision и output dequantization для exact release. FULL/RAW — имена режимов исторического pytpu, а не универсальный bool «float/int8». Текущая ABI и semantics не проверены; исторический пакет15.0.24 не объявлять matching Runtime16.18.6.

Публичный builder свидетельствует о vendor PTQ на исходном floating graph через TF, не о поддержке готового ONNX QuantizeLinear/DequantizeLinear/QAT. Не готовить QDQ как гарантированный обход. Graph import должен пройти прежде выбора calibration thresholds. Guide2025 по соседнему research описывает data-dependent calibration; scope `percentile` и математическая формула не установлены. Не выдавать percentile100 за доказанный max(abs activation).

Calibration для каждого graph/preprocessing отдельно: репрезентативные разрешённые кадры из целевых камер, маленькие люди/телефоны/сигареты, фон, свет/пыль/окклюзии; для top-down pose именно crops с тем же affine/normalize. Сохранить список/hash и фактическое число; calibration и evaluation разделить по видео/эпизодам. 100/500 — варианты бюджета, не доказанная достаточность. Изменение состава/percentile сравнивать по одному после float parity. Fail-closed на TypeError вместо blanket retry, записать requested/effective arguments и thresholds, если API разрешает. На экспортной ветке не начинать QAT до доказанного PTQ bottleneck и supported import path.

**Происхождение:** [W1-14.md](_WORK/W1-14.md), `## Новая бинарная`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Новая бинарная проверка: конкретные графы и список операций для первого smoke

#### W1-14-S08 — MeetCool smoking ONNX, собственный полный проход структуры top-level graph

[Exact ONNX](https://huggingface.co/MeetCool/yolov8n-smoking-detection/resolve/7d510c6aaa3fbc3048368565d4236993c077dc0a/models/fine_tune_YOLOv8n.onnx), publisher MeetCool; revision **`7d510c6aaa3fbc3048368565d4236993c077dc0a`**. Самостоятельный HTTP Range206 23.10.2026: file length **12,252,672 B**. Успешный проход прочитал **1,078,784 B**,66 выровненных16KiB блоков; payload initializer пропускался по protobuf length. Это не полный файл; часть тензорных bytes могла попасть в блоки рядом с headers. Дополнительная проверка атрибутов первых node fields прочитала49,152 B. Первый диагностический проход того же reader дошёл до EOF из-за ошибки собственного end condition; после исправления reader успешно завершён. Это не ошибка ONNX и не успешный ONNX checker. Полный SHA256 не вычислялся; заявленный LFS hash из W1-08 `afcf1e6d1293427b9221b60c9505e76072f9a295120d0a78c71e35f9c444ff8e` остаётся publisher metadata.

**A: ModelProto.ir_version9; opset_import default domain19.** Graph input `images`, elem_type1 (FLOAT), dims `[1,3,640,640]`; output `output0`, FLOAT `[1,7,8400]`. Считаны **233 top-level NodeProto**,14 разных op_types, все в default domain. Таблица ниже — **наблюдённый инвентарь графа, не LinQ support matrix**.

| ONNX op_type | smoking count, imported set19 | SafetyVision count, imported set20 |
|---|---:|---:|
| Conv | 64 | 64 |
| Sigmoid | 58 | 57 |
| Mul | 58 | 57 |
| Split | 9 | 8 |
| Add | 8 | 8 |
| Concat | 19 | 17 |
| MaxPool | 3 | 3 |
| Resize | 2 | 2 |
| Reshape | 5 | 8 |
| Transpose | 1 | 1 |
| Softmax | 1 | 1 |
| Slice | 2 | 2 |
| Sub | 2 | 2 |
| Div | 1 | 1 |
| **Всего** | **233** | **231** |

**Атрибуты smoking, прямо прочитанные из nodes:** Resize `coordinate_transformation_mode=asymmetric`, `mode=nearest`, `nearest_mode=floor`; Softmax axis1; Split axis1; Reshape allowzero0; Transpose perm `[0,2,1,3]`; MaxPool kernel5×5, pads2/2/2/2, strides1/1,dilations1/1,ceil_mode0. Conv наблюдались kernel3×3 со strides1/2 и pad1 либо1×1 со stride1/pad0; group1,dilations1/1. Slice attributes отсутствуют, параметры находятся во входных тензорах. Численные float attributes и значения initializer в этом reader не декодировались; для compile diagnosis нужны все input constants, attrs и промежуточные shapes из полного разрешённого ONNX inspection. Эти поля нельзя заменять общим «Resize supported».

При opset19 Resize разрешается по ONNX schema19, Softmax по schema13 (S07); остальные op_types тоже разрешаются относительно domain import, а не получают автоматически номер19. **Не смешивать importer поддерживает opset19 с compiler умеет все эти attrs/shapes.** В top-level инвентаре нет NonMaxSuppression, QuantizeLinear, DequantizeLinear, Loop/If/Scan. Наличие Softmax не означает готовый action classifier: здесь по source S05 это DFL bbox head. Никакого ускорительного покрытия этот список не подтверждает.

**W1-14-F04:** MeetCool — теперь не только tail metadata из W1-08: установлен конкретный structural smoke surface из14 операций, IR9/opset19, static batch1. Если supplied frontend отклоняет IR9/opset19 или конкретный Resize/Split/Reshape, это локализуемый conversion blocker; если проходит, quantization/compile/device всё ещё отдельные gates. Возможный новый export checkpoint на согласованном opset — новый граф с собственной parity-проверкой, не редактирование protobuf номера.

#### W1-14-S09 — SafetyVision v2: card claims проверены по бинарной структуре

[Exact ONNX](https://huggingface.co/ayushgupta7777/safetyvision-yolov8/resolve/56a71758b55f0e9f2b4b2d6b51a779a1f882da10/v2/best_640.onnx), publisher ayushgupta7777; revision **`56a71758b55f0e9f2b4b2d6b51a779a1f882da10`**. Собственный HTTP Range206: **44,764,727 B** длина. Успешный structural проход прочитал **1,150,519 B**,71 блок, не полный44.8MB artifact. Full hash/checker/weights/external-data validation не делались; LFS hash из W1-07 `ea18ae903a566e8fa76f3ee1c503075522dca269269315e9c862efa170430b35` — metadata издателя, не наш full-file digest.

**A:** `ir_version9`, default-domain import20; `images` FLOAT `[1,3,640,640]` → `output0` FLOAT `[1,17,8400]`. **231 top-level nodes**,14 op_types, все default domain; counts в таблице S08. Карточные заявления640/13classes/17channels и opset20 подтверждены как serialization contract этого exact v2 файла. Class names/quality/license из W1-07 остаются отдельным evidence: из одной формы17 нельзя восстановить ordered13-class semantics. Реальная card web.open дополнительно оказалась недоступна в моём web-канале, но бинарные range GET успешны. Не менять v2 на root v1 или896 файл.

**W1-14-F05:** у SafetyVision не обнаружился новый top-level operator type по сравнению со smoking, но иной imported set20 и иные head shapes/counts. Следовательно, успешный smoking compiler test полезен как зацепка, однако не сертификат SafetyVision: версии схем, weights/activations memory, quantization sensitivity и class/NMS mapping всё ещё различаются. Атрибуты SafetyVision отдельно не сопоставлялись. Ни `No_Harness`, ни mAP из карточки не доказывают hook/anchor state или event precision.

#### Точный пакет вопросов/операций для первого SDK smoke

1. Для **готового smoking** подать vendor engineer manifest: Model IR9, main opset19; FLOAT images `[1,3,640,640]`, FLOAT output0 `[1,7,8400]`;14 op_types/counts выше и Resize/Softmax/Split/Reshape attrs. Попросить matching release ingest log, полный compile/coverage report и user/raw output description. Нельзя заранее поставить галочки support этим ops.
2. Для **готового SafetyVision**: IR9/main20, input такой же, output `[1,17,8400]`;231 nodes и ordered class map. Не запускать generic COCO84/85 normalizer/NMS без изменения nc13.
3. Для **первого своего detector/pose export**: candidate opset13/static1/nmsFalse, exact source/weights pin, full graph inventory после экспорта. Предполагаемые Conv/Sigmoid/Mul/Resize/DFL ops не выдавать за наблюдённый набор будущего graph; torch/exporter/simplifier могут менять его.
4. Для **RTMPose-t**: opset11 из deployment JSON, actual IR/node types пока U; input rectangular256×192, two outputs и batch1 specialization. Нужно обе tensor descriptions и affine/RGB golden; public square one-output builder не является готовым решением.
5. Сохранить separately: original framework graph → ONNX float → imported float → quantized software → compiled device raw/user outputs → decoded detections/keypoints → episode. Первый не прошедший gate определяет владельца проблемы. Метрика события не может скрыть failed raw parity, а один успешный dummy tensor не доказывает выбранный сценарий.

Итоговая граница: новая первичная проверка уменьшила неизвестность **содержимого двух конкретных ONNX**, но не закрыла **поддержку конкретного SDK, PTQ качество и реальное исполнение LinQ**. Требуемое hardware измерение остаётся работой команды на выданной среде.

<a id="F013"></a>
## F013 — Производительность: определения времени, source sampling, очереди и фактическая арифметика

**Нормализованный статус и условия:** Ни одного нашего LinQ замера. Published vendor numbers не SLA; synthetic phase coverage не NN recall. Tracker route уточнён F034.

**Источники:** [S005](SOURCES.md#S005), [S009](SOURCES.md#S009), [S026](SOURCES.md#S026), [S027](SOURCES.md#S027), [S028](SOURCES.md#S028), [S029](SOURCES.md#S029), [S030](SOURCES.md#S030), [S031](SOURCES.md#S031), [S032](SOURCES.md#S032), [S033](SOURCES.md#S033).

**Происхождение:** [W1-15.md](_WORK/W1-15.md), `## Реестр источников`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Реестр источников: URL, версия, локатор, доказательство

Все источники открывались 23.10.2026. `current HTML` означает отсутствие неизменяемой ревизии, а не найденную дату публикации. Код прочитан, не исполнялся.

| ID | Источник и локатор | Что проверено / ограничение |
|---|---|---|
| **W1-15-S01** | «ХайТэк», [LinQ presentation 2026](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf), слайд 4 «Производительность», footer; слайд 3 для сравнения ResNet | Новый первичный fetch TinyFish `fetch_content`, markdown. Полный текст содержит заголовок 2026 и таблицу. PDF bytes/render не получены: **нет собственной визуальной сверки единиц**. Text metadata author «Севрюков Сергей», published_date=null; дата 2026 по содержимому. Производитель сообщает измерения, raw logs не даны. |
| **W1-15-S02** | [LinQ / решения](https://lin-q.ru/sol), current HTML, разделы HPD/HPQ/HPS и HX, web lines 74–87, 123–137, 168–183, 215–234 | Заявление производителя о ResNet50 2.3 ms и возможности 1.5 ms. На странице HX отдельно отнесено декодирование к CPU; это не decode benchmark сервиса хакатона. |
| **W1-15-S03** | Нефёдов / Качмазов / Бабинцев, VK/ВШЭ, [«Адаптированные нейросетевые алгоритмы на отечественных процессорах»](https://habr.com/ru/companies/vk/articles/895432/), 30.03.2025 06:23; раздел IVA TPU, web lines 96–132 | Первичный авторский рассказ эксперимента: различены preloaded Performance и последовательный Latency, batches 1/2/4/8, проблемы STAGING. Matched scripts/logs/современные версии не установлены. Числа операций не используем для камер. |
| **W1-15-S04** | GStreamer, [queue](https://gstreamer.freedesktop.org/documentation/coreelements/queue.html), current docs, overview; `current-level-*`, `leaky`, `max-size-*` | Очередь блокирует при заполнении либо сбрасывает новые/старые buffers; доступны count/bytes/time. Это механизм предлагаемого адаптера, не свойство LinQ API. |
| **W1-15-S05** | GStreamer, [rtpjitterbuffer](https://gstreamer.freedesktop.org/documentation/rtpmanager/rtpjitterbuffer.html), current docs; `latency`, `drop-on-latency`, `post-drop-messages`, `add-reference-timestamp-meta` | Jitter buffer добавляет задержку, может сбрасывать старые packets и сообщать причину/sequence/PTS. Некоторые возможности зависят от версии, например reference metadata since 1.22; наличие на VM не проверено. |
| **W1-15-S06** | Schulzrinne et al., [RFC 3550](https://www.rfc-editor.org/rfc/rfc3550.html), July 2003, §§5.1, 6.4.1 | RTP clock не равен UTC; sender report связывает RTP/NTP, но NTP может быть относительным/нулевым; точность timestamp не равна его разрядности. Это граница измеримости camera age. |
| **W1-15-S07** | ByteTrack, [byte_tracker.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py), commit `d1bf0191adff59bc8fcfeaa0b33d3d1642552a99`; класс BYTETracker `__init__`, `update`, removal loop | Новый GET exact revision; revision найден через соседний provenance, содержимое открыто самостоятельно. `frame_id` растёт на update, lost budget в кадрах; два порога score для association. |
| **W1-15-S08** | ByteTrack, [kalman_filter.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/kalman_filter.py), тот же commit, `KalmanFilter.__init__` | Новый GET exact revision: constant velocity, `dt=1`. Не адаптируется автоматически к произвольному фактическому dt из PTS. |
| **W1-15-S09** | Python, [time](https://docs.python.org/3/library/time.html#time.perf_counter_ns), открытая версия docs 3.15.1; `perf_counter_ns`, `get_clock_info` | Монотонный локальный интервал и описание clock; это документация, версия интерпретатора VM неизвестна. Наносекундный integer не гарантирует ns accuracy. |

#### Поисковый след и сбои

Запросы `site:files.lin-q.ru "yolo5s" "106"`, `site:lin-q.ru "FPS" "latency"`, targeted Habr latency; открыты vendor sol, presentation, Habr, SPbPU metadata, GStreamer и exact ByteTrack. Общая выдача LinQ performance оказалась слабой; не заменяла чтение источника. Web open презентации HTTPS и HTTP дал недоступность; локальный urllib HTTPS — SSL EOF. TinyFish затем прочитал text, но не оригинальные bytes; применять навык PDF для визуальной проверки было возможно лишь условно, render не выполнен. Не объявляем text extraction визуальным доказательством. SPbPU `/info` и `/en/info` не дали читаемого нового содержания (timeout/ошибка); cloud table `https://cloud.mail.ru/public/zMRN/F2XL5Qxv3` также недоступна. Нельзя повысить прежние 443/430/142/20 FPS из соседних notes до самостоятельно подтверждённых результатов. GitHub API commits дал 403 rate-limit; exact raw files по известному revision прочитаны web. Ни SDK, ни чужой код, ни большие архивы не запускались/не скачивались.

**Происхождение:** [W1-15.md](_WORK/W1-15.md), `## Опубликованные`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Опубликованные измерения LinQ: что именно известно

**W1-15-F01 [REPORTED_MEASUREMENT, S01]** Выборочные строки слайда 4, десятичные разделители нормализованы; latency — **ms по текстовому заголовку**:

| Имя сети в источнике | Batch | HP throughput, FPS | HP latency, ms | HPQ throughput, FPS | HPQ latency, ms |
|---|---:|---:|---:|---:|---:|
| yolo5s | 1 | 106.1 | 23.71 | 424.4 | 23.71 |
| yolov8n_pose | 1 | 104.8 | 21.51 | 419.2 | 21.51 |
| ssd_mobilenet_v2 | 1 | 556.7 | 3.54 | 2226.8 | 3.54 |
| ssd_mobilenet_v2 | 8 | 428 | — | 1712 | — |
| resnet50 | 1 | 432.9 | 2.99 | 1731.6 | 2.99 |
| resnet50 | 8 | 1112.8 | — | 4451.2 | — |

Общие условия footer: Intel Core i7-10700K @3.80GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, методика MLCommons MLPerf. Не установлены input resolution/layout, exact checkpoint/hash, per-row precision/calibration, compiler preset, number in-flight, MLPerf scenario/revision, percentile latency, timer boundaries, decode/pre/post, качество. Указание int8 TOPS продукта не устанавливает precision конкретной строки. `yolo5s` не доказывает identity с нашим YOLOv5 checkpoint; название строки `yolov8n_pose` не подтверждает какой-либо конкретный downloadable YOLOv8n-pose checkpoint/экспорт/качество. Pose не detection. Заголовки первичного извлечения буквально: `Сети (выборочно)`, `Batch`, `LinQ HP`, `LinQ HPQ`, под каждым устройством `Throughput, FPS` и `Latency, ms`.

**W1-15-F02 [ANALYSIS]** HPQ throughput в этих строках ровно 4×HP, latency одинакова; это не доказывает single-request ускорение в 4 раза. FPS не обращаем в SLA: `1/106.1` около 9.43 ms, а указанная latency23.71 ms; без workload/границ нельзя смешать знаменатели. Из этого расхождения не устанавливаются очередь, параллельность или single-request semantics: нужны первичные определения измерений. Для SSD batch8 throughput меньше batch1 — оставлено буквально, причина неизвестна. Слайд3 даёт ResNet50 HP460/1046 FPS b1/b8 против432.9/1112.8 на слайде4: нельзя склеивать в один контролируемый experiment. У подозрительных anti_spoof/lenet единицы не исправляем самостоятельно; эти строки не нужны для решения.

**W1-15-F03 [VENDOR_CLAIM, S02]** Публичные 2.3 ms ResNet50 и возможные1.5 ms не снабжены полным протоколом; они не время обнаружения нарушения. Ни одна таблица не измеряет RTSP→decode→LinQ API→tracker→confirm→UI. Числа пригодны как основания запросить matched sample и повторить тест, а не обещать число камер.

**W1-15-F04 [AUTHOR_EXPERIMENT_REPORT, S03]** Авторский опыт2025 различает заранее загруженные данные ради throughput и последовательную подачу ради latency; исследует batch1/2/4/8 и отмечает compile/runtime сбои со STAGING. Это полезное подтверждение необходимости двух режимов измерений, но не текущий bench H1M/Runtime16 и не воспроизводимый пакет чисел. Слова автора о полном цикле не означают включение камеры/UI. Исторические MLPerf FPGA-результаты из соседнего отчёта не переносим на ASIC: они относятся другой платформе.

**Происхождение:** [W1-15.md](_WORK/W1-15.md), `## Метрики`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Метрики и минимальная трасса

Всё ниже — **W1-15-F05 [DESIGN/ANALYSIS]**, предлагаемый контракт нашей проверки, не названия SDK функций. Manifest: SKU/device IDs и квота; runtime/driver/compiler versions; hash исходных/compiled weights; вход/выход, dtype/layout/size; pre/postprocess; batch и max batch wait; API/transport/payload size; CPU/RAM; codec/resolution/source FPS; очередь/drop policy; sampling; версия правил/порогов; длительность/warmup. Фиксировать фактическое LinQ execution отдельно (W1-13), не считать быстрый HTTP ответ proof.

Для каждого кадра: `run_id,camera_id,stream_epoch,frame_seq,source_pts,time_base,request_id,attempt_id,batch_id,model_hash`; для события `episode_id,event_id,delivery_id`. Reconnect меняет epoch, PTS/track ID не глобальный ключ. Повтор HTTP имеет тот же logical request/event id и отдельный attempt. Timestamp null с причиной при отсутствии, никогда подставное0.

| Метка | Граница |
|---|---|
| `t_capture` | Проверенная camera sampling reference; сохранить source clock и mapping/error |
| `t_release` | Запланированное release кадра при replay в реальном времени |
| `t_receive`, `t_decode` | Кадр доступен приёмнику; затем decoded frame ready |
| `t_enqueue`, `t_dispatch` | Начало ожидания адаптера; выход из очереди |
| `t_submit`, `t_return` | Вход/возврат runtime/API; возврат может означать только accepted |
| `t_output` | Требуемые выходы реально доступны обработчику после официального completion |
| `t_track`, `t_confirm` | Tracker update ready; временное правило впервые подтвердило событие |
| `t_store`, `t_deliver`, `t_visible` | Запись подтверждена; потребитель принял; UI отрисовал карточку |

На одном host длительности считать монотонными часами [S09]. Для удалённого сервиса клиентский `t_output−t_submit` — **API round-trip**, включающий сериализацию/сеть/remote queue/inference/выгрузку в заданных границах. Device-only время доступно только при документированном instrument/привязке к request. Нельзя вычитать server monotonic из client monotonic; нельзя вычислять network как RTT минус несопоставимое устройство percentile.

| Метрика | Формула / знаменатель | Что не покрывает |
|---|---|---|
| Inference device latency | Документированное device end−start; опционально | Всё вне device boundary |
| Completed request latency | `t_output−t_submit`, unique valid successful requests | Более раннюю очередь/decode |
| Scheduled response | `t_output−t_release` | Camera delay до release |
| Decode/pre/post/tracker | Парные границы внутри конкретного frame/request | Нельзя складывать p95 стадий для e2e p95 |
| Frame age at decision | `t_confirm−mapped(t_capture)` | Неизмерима без проверенного capture mapping |
| Receive-age proxy | `t_confirm−t_receive` | Это нижний по охвату proxy, не camera age |
| Throughput | Unique valid completed frames / common wall-clock window; отдельно batches/s | Не своевременность, не source FPS |
| First confirmed violation latency | `t_confirm−t_GT_onset`, один matched episode | Пропущенные эпизоды отдельно; не latency0 |
| Operator notification latency | `t_visible−t_GT_onset` | Backend enqueue не означает видимость |
| Timely event recall(D) | GT episodes с одним уведомлением до D / все eligible GT episodes | D согласовать до прогона; misses остаются в знаменателе |

Дать n, duration, mean/p50/p95/max по камере и pooled; p99 только с n и предупреждением о малой выборке (при100 событиях это почти max). Percentile заранее выбрать, например nearest-rank `x[ceil(p*n)]`. Отдельно cold first call, warm steady run, failures/timeouts/retries/late responses и incomplete на cutoff. В throughput общее окно wall time, не сумма inference time. Drain описать отдельно; хвост после конца окна не добавлять бесшумно к числителю. При выполнении sample100 не выдавать статистическую гарантию хвостов.

**Происхождение:** [W1-15.md](_WORK/W1-15.md), `## Frame skipping`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Frame skipping, окна и aliasing

**W1-15-F06 [ANALYSIS]** Для равномерного sampling с шагом Δ и идеальным наблюдаемым эпизодом длительности d, при равномерной случайной фазе и без иных потерь вероятность получить хотя бы один sample равна `min(1,d/Δ)`. Это геометрия выборки, **не model recall**. При детерминированной фазе эпизод короче Δ может систематически целиком попадать между кадрами. Для m наблюдений нужен как минимум span `(m−1)Δ` между первым/последним, плюс ожидание фазы; добавление hold H не компенсирует пропущенный короткий эпизод. Для гарантии m идеальных samples любой фазы требуется примерно d≥mΔ с оговоркой открытых границ. После jitter/drop нужен фактический max gap, средний FPS не даёт гарантии.

**Выполнена только локальная синтетическая арифметика**: Python3.11, без NN/видео/LinQ/стороннего кода. 10 000 фаз `p=i/10000`, samples `(k+p)/f`, k=0..29, hit если `0≤sample<d`. Полная формула воспроизведения: `sum(any(0 <= (k+p)/f < d for k in range(30)) for p in phases)/10000`. Проверка не замеряла wall-clock performance; вывод программы:

| Sampling f | d=0.2s, fraction phases hit | d=0.5s | d=1s | Span 3 samples |
|---:|---:|---:|---:|---:|
| 1FPS | 0.20 | 0.50 | 1.00 | 2.0s |
| 2FPS | 0.40 | 1.00 | 1.00 | 1.0s |
| 5FPS | 1.00 | 1.00 | 1.00 | 0.4s |
| 10FPS | 1.00 | 1.00 | 1.00 | 0.2s |

Это **W1-15-F07 [EXECUTED_SYNTHETIC_CHECK]**, первые проверенные численные результаты ветки, не измерения качества или мощности LinQ. Подтверждает опасность «три кадра» как универсального debounce. Условие d=0.2s и5FPS даёт100% лишь идеальному sample coverage, не распознаванию.

План проверки настоящих clips: один исходный GT timeline; f=источник,10,5,2,1 FPS — **кандидаты эксперимента, не требования кейса**. Для каждого f не один phase: сместить release минимум на0,¼Δ,½Δ,¾Δ и проверить кратчайший положительный эпизод. Дополнительно один burst gap, а не только равномерное decimation. Должны сохраняться source PTS/GT; нельзя ускорять ролик, оставив nominal FPS, и называть это lowFPS. Offline без drops оценивает признаки; paced replay с тем же sampling оценивает очередь и свежесть; результаты разделить.

**W1-15-F08 [SOURCE_INSPECTION→ANALYSIS, S07/S08]** В pinned ByteTrack lost budget `int(frame_rate/30*track_buffer)`, update увеличивает frame_id на1, motion model dt=1. При вызовах только на выбранных/успешных кадрах модель времени становится временем updates. Передача nominal camera30FPS при обработке2FPS растянет TTL в реальных секундах; переменный gap не исправляется одним fps аргументом. Решение: фиксированный analysis cadence и правильно заданный rate с контролем gaps, либо отдельная timestamp-aware адаптация с проверкой фильтра и covariance; не просто заменить dt в одной строке. Предсказанные boxes не считаются новой визуальной поддержкой правила. S07 также показывает низкий score association; сохранение низкоуверенных boxes для association не означает разрешение подтверждать ими нарушение.

#### Предлагаемый temporal state и gaps

**W1-15-F09 [DESIGN]** `CLEAR → CANDIDATE → CONFIRMED → RECOVERING → CLEAR`, отдельно `UNKNOWN/GAP`. Все H_on/H_off/G_max/age_max в секундах source time, versioned per scenario. Значения выбирать на development positive/negative clips и заморозить перед контрольной выборкой; отсутствие универсального H=3s указать явно.

- CANDIDATE подтверждается только достаточными свежими **измеренными** признаками, span≥H_on, minimum observations и max gap≤G_max. Само течение часов при отсутствии кадров не evidence. Можно time-weighted observed occupancy, но не заполнять весь длительный gap последним label; определить cap поддержки одного sample.
- Один крупный gap или stale output переводит в UNKNOWN/сбрасывает накопление кандидата по явно заданной политике. Пауза сервиса не доказывает ни безопасность, ни продолжение неподвижности. При CONFIRMED сохранить открытый episode и признак uncertain; не закрывать инцидент/не открывать новый только потому, что камера исчезла.
- `H_off` требует наблюдаемого возврата в норму. Cooldown сам по себе не определяет новый episode: продолжающееся нарушение после cooldown не новое. Срыв track ID не должен автоматически дать повтор; сопоставление episode по камере/зоне/типу/геометрии в ограниченном окне, неоднозначность сохранить для аудита.
- Dedupe key = устойчивый `event_id` episode; повтор delivery/reconnect должен быть идемпотентен. UI ACK оператора не заменяет условие окончания поведения. После restart журнал открытых episodes/доставок нужен для проверки одного сообщения.
- Результаты out-of-order упорядочивать по source time в ограниченном reorder window либо отклонять устаревшие с reason; не использовать старый результат как подтверждение нынешнего поведения.

Confidence tradeoff проверять joint grid detector threshold × H_on × sampling на тех же clips. Высокий threshold может уменьшить FP и разорвать наблюдения/породить FN; долгий hold может убрать FP и полностью потерять короткое нарушение. Фиксировать event precision/recall и timely recall, FP/час на отрицательном материале, ID switches/дубли. Порог выбирать по event результату, не только frame mAP. Для pose/скорости учитывать недостоверные keypoints, bbox jitter и scale; линейная интерполяция через gap не доказательство пересечения/падения.

**Происхождение:** [W1-15.md](_WORK/W1-15.md), `## Очереди`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Очереди, декодирование и camera sync

**W1-15-F10 [DESIGN backed by S04/S05]** Для live MVP кандидат — bounded latest-frame mailbox per camera после decode, справедливый dispatch между камерами; размер/age budget выбрать после первого замера. Логировать replacement/timeout/stale counts. Старые compressed interdependent frames нельзя произвольно удалять как независимые картинки: сначала сохранять codec/decode continuity штатным pipeline, сбрасывать decoded analysis frames либо пользоваться документированным механизмом восстановления. Буферы камеры/RTSP/jitter/decode могут оставлять age высоким даже при mailbox1. Поэтому измерять каждый участок, а не только очередь NN. GStreamer даёт queue levels/leaky и jitter drop messages; это проверяемая реализация при наличии версии, не требование ставить GStreamer.

Batch1 предпочтителен для первого измерения. Если batching нужен, зафиксировать maximum batch wait и фактический size distribution; малый поток не должен бесконечно ждать заполнения. Capacity не равна `modelFPS/analysisFPS`: учитываются decode, payload, pre/post, shared quota, многомодельность, fairness. Первый N=2 тест проверяет именно starvation/age по каждой камере; не строим большой capacity benchmark.

**W1-15-F11 [RFC→ANALYSIS, S06]** Для разных камер один frame_seq/PTS не общий момент. Сохранять RTP/PTS mapping и clock uncertainty, проверять offset/drift в начале/конце; при недоступном capture UTC честно публиковать receive-age. Общее физическое событие/видимый таймер в кадре может дать практическую калибровку. Для одного camera человек+техника должны быть из одного source frame либо иметь bounded time mismatch. Межкамерную геометрию/скорость не объединять без калибровки пространства и времени. Если максимальная relative speed v и рассогласование δt, дополнительная пространственная неопределённость порядка v·δt (проектная оценка), её нельзя скрывать за точным порогом метров. Для MVP cross-camera fusion не требуется.

<a id="F014"></a>
## F014 — Core: exact YOLOX nano, official pose и RTMPose; полный pre/post contract

**Нормализованный статус и условия:** Приоритетный собственный graph probe YOLOX nano. BGR recipe — documented test hypothesis, не empirical artifact-matched golden; обе исторические рецептуры и причина ambiguity сохранены.

**Источники:** [S019](SOURCES.md#S019), [S034](SOURCES.md#S034), [S035](SOURCES.md#S035), [S036](SOURCES.md#S036), [S037](SOURCES.md#S037), [S038](SOURCES.md#S038), [S039](SOURCES.md#S039), [S040](SOURCES.md#S040), [S041](SOURCES.md#S041), [S042](SOURCES.md#S042), [S043](SOURCES.md#S043), [S044](SOURCES.md#S044), [S045](SOURCES.md#S045), [S046](SOURCES.md#S046), [S047](SOURCES.md#S047), [S048](SOURCES.md#S048), [S049](SOURCES.md#S049), [S050](SOURCES.md#S050), [S051](SOURCES.md#S051), [S052](SOURCES.md#S052), [S053](SOURCES.md#S053), [S054](SOURCES.md#S054), [S055](SOURCES.md#S055), [S056](SOURCES.md#S056), [S057](SOURCES.md#S057), [S058](SOURCES.md#S058).

**Происхождение:** [W2-02.md](_WORK/W2-02.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Дата доступа и собственных проверок: **23.10.2026**, downloads стартовали **14:54:12 UTC / 17:54:12 МСК**. Прочитаны релевантные исходные секции W1-08 S01–04, W1-14 S03–06 и W1-16 F01; исходное замечание K003 сохранено в `_WORK/PROMPT_W2-02.md`. Начальный совмещённый вывод трёх файлов был усечён, поэтому нужные секции дополнительно читались адресно. Самостоятельные новые GET, полные hashes и статический разбор ниже; W1 не используется вместо новых binary observations.

**Решение:** первый собственный graph для smoke — **официальный YOLOX nano ONNX 416**, один input и один raw output. Один резерв маршрута pose — **RTMPose-t**, только после успешного detector path и при необходимости pose-сценария; это дополнительная crop-wise сеть, не drop-in detector. Официальный **yolov8n-pose.pt v8.3.0** закреплён полным hash и безопасной metadata, но не добавляется третьей сетью в первый перенос: готового ONNX этой ветки здесь нет.

**Статус K003: scoped, не hardware closed.** Artifact identity / observed graph contract закрыты для двух ONNX; единый документированный reference выбран. Точное историческое соответствие YOLOX release bytes одной версии preprocessing остаётся source-provenance ambiguity и требует отдельного host sanity/parity gate; обнаружен конфликт старого tag и release notes. RTMPose actual dimensions символические, а не доказанные статические `[1,17,…]`. Численная parity, checker, shape inference, static specialization, SDK/frontend/PTQ/compile/device и качество событий не выполнялись. Это пакет статического входа в эксперимент, не LinQ PASS.

#### Точный вопрос и границы доказательств

Можно ли передать platform-track **один маленький реально полученный граф** с полным hash, всеми входами/выходами, decoder и явно выбранным preprocessing, чтобы не терять первый запуск на перепутанных 84/85 каналах, цвете и повторном grid decode? Для pose отдельно — можно ли получить оба реальных выхода и воспроизводимый affine reference без установки SDK и без unpickle?

Выполнено только собственное Python stdlib HTTP чтение, SHA256, `zipfile`, ограниченный protobuf wire reader и `pickletools.genops/dis`. Чужие `.py` только скачаны/прочитаны как текст; не импортированы и не исполнены. `torch`, `onnxruntime`, `onnx`, SDK не импортировались; `torch.load`, pickle load, export, training, compilation, inference и benchmark отсутствуют. Каждая загрузка ограничена 16 MiB, извлекаемый ZIP entry — 16 MiB, pickle metadata — 1 MiB. Загружены три выбранных компактных artifact, не model zoo/большие архивы.

Evidence directory: [`W2-02_evidence`](_WORK/W2-02_evidence/). В ней сохранены сами байты, HTTP headers без подписанных redirect URL, исходники, JSON metadata, полный список graph nodes/edges/attrs и статический pickle disassembly. [downloads.json](_WORK/W2-02_evidence/downloads.json), [static_metadata.json](_WORK/W2-02_evidence/static_metadata.json), [graph_nodes.json](_WORK/W2-02_evidence/graph_nodes.json), [sources_manifest.json](_WORK/W2-02_evidence/sources_manifest.json), [acquire.py](_WORK/W2-02_evidence/acquire.py), [inspect_static.py](_WORK/W2-02_evidence/inspect_static.py), [graph_detail.py](_WORK/W2-02_evidence/graph_detail.py) позволяют отделить наблюдение от пересказа. Reader проверяет wire boundaries и собирает I/O/opset/nodes/initializers; он **не ONNX checker и не валидатор математической корректности**. Хеширование полного файла не проверяет качество weights.

Компактный машинный контракт: [smoke_contract.json](_WORK/W2-02_evidence/smoke_contract.json), где primary помечен `documented_test_hypothesis_not_artifact_matched_golden`; общий список50 файлов с полными SHA256 — [all_files_manifest.json](_WORK/W2-02_evidence/all_files_manifest.json).

#### W2-02-S01 — YOLOX nano: полный официальный ONNX и реальная структура

**Первичный artifact:** [официальный release URL](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_nano.onnx). Собственный **полный HTTP GET200**, **3,659,407 B**. SHA256 фактически полученных bytes:

`c789161ed43c8269fcd4e67c67eeeb4e80c622da2eb296a20bc6007bd18a0b7d`

GitHub [release API](https://api.github.com/repos/Megvii-BaseDetection/YOLOX/releases/tags/0.1.1rc0) сохранён в `yolox_release.json`: release published `2021-08-18T12:41:41Z`; asset ID **42724905**, created `2021-08-18T12:34:05Z`, updated `2021-08-18T12:34:07Z`, digest null. Эти даты отличаются от даты нашего доступа и не являются датой training. Release locator не immutable content guarantee; теперь это компенсируется собственным полным hash.

**Наблюдение полного графа:** `ir_version=6`, producer `pytorch`, producer_version `1.7`, default-domain opset **11**; graph `torch-jit-export`. Все I/O FLOAT (elem_type1):

| Роль | Имя | Observed declared shape |
|---|---|---|
| единственный input | `images` | `[1,3,416,416]` |
| единственный output | `output` | `[1,3549,85]` |

369 nodes, 236 initializers. Все op domain пустые/default; нет nested graph, local function или sparse initializer; у initializers нет external_data/data_location EXTERNAL. Следовательно в наблюдённой структуре не требуется external tensor file. Тензорные payload не интерпретировались как веса/математика.

| Оператор | Количество |
|---|---:|
| Conv | 113 |
| Sigmoid | 110 |
| Mul | 104 |
| Concat | 18 |
| Slice | 8 |
| Add | 7 |
| MaxPool | 3 |
| Reshape | 3 |
| Resize | 2 |
| Transpose | 1 |

Ни Exp, ни NonMaxSuppression в реальном графе нет. Конец graph: три head tensors `1066/1108/1150` → Reshape `1158/1166/1174` → `Concat_422(axis2)` → `Transpose_423(perm[0,2,1])` → `output`. Resize attrs: `coordinate_transformation_mode=asymmetric`, `mode=nearest`, `nearest_mode=floor`, `cubic_coeff_a=-0.75`. Полный node inventory с attrs находится в `graph_nodes.json`; это input для проверки frontend, не утверждение поддержки этих операций LinQ.

**Decoder match сильнее одной формы85:** [release-tag exporter](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/e1052df71842031413f6030723c3607b839c80ce/tools/export_onnx.py), L77 явно `model.head.decode_in_inference=False`; [head](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/e1052df71842031413f6030723c3607b839c80ce/yolox/models/yolo_head.py), L189 уже sigmoid для obj/class и L211 условный geometry decoder. Реальный graph не содержит Exp и заканчивается concat/transpose — согласуется с **raw geometry**, уже sigmoid objectness/classes. Это структурное соответствие исходнику; exact command/export commit внутри release artifact не записан и не восстановлен. Нельзя объявлять exporter воспроизведённым.

#### W2-02-F01 — новая коллизия YOLOX source provenance: release tag не равен однозначному recipe

W1-08/W1-16 использовали source commit **6ddff4824372906469a7fae2dc3206c7aa4bbaee**: BGR float0..255, pad114, без normalize. Сейчас отдельно разрешён [git tag 0.1.1rc0](https://api.github.com/repos/Megvii-BaseDetection/YOLOX/commits/0.1.1rc0) → **e1052df71842031413f6030723c3607b839c80ce**, commit date `2021-08-12T02:40:52Z`. Его [onnx_inference.py](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/e1052df71842031413f6030723c3607b839c80ce/demo/ONNXRuntime/onnx_inference.py), L67–69 задаёт mean `(0.485,0.456,0.406)`, std `(0.229,0.224,0.225)`; [preproc](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/e1052df71842031413f6030723c3607b839c80ce/yolox/data/data_augment.py), L182–204 делает BGR→RGB, `/255`, mean/std. В этом старом decoder NMS также class-aware, тогда как текущий официальный demo default class-agnostic.

При этом **сам release API body** описывает обновление `2021/08/19`: удаление normalization, несовместимость old weights и прекращение поддержки old weights в deployment demo. Asset создан18 августа, tag commit12 августа, release body описывает19 августа. Текущий [официальный pinned ONNX README](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/demo/ONNXRuntime/README.md) продолжает ссылаться на **тот же artifact URL**, а [текущий inference](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/demo/ONNXRuntime/onnx_inference.py) использует новый BGR recipe.

**Вывод строго ограничен:** W1 BGR recipe не опровергнут однозначно; опровергнута достаточность «release URL + произвольный source revision» как доказательства исторического export/preproc соответствия. Само имя тега не позволяет предпочесть старую нормализацию, потому что body и актуальная deployment-инструкция ему противоречат. Binary I/O не содержит цветового пространства, а stats весов не служат доказательством preprocessing. **Для первого smoke выбираем один документированный актуальный официальный reference BGR0..255 ниже; confidence в artifact→preprocessing остаётся условной до host sanity/parity.** Не превращать два conflicting recipes в молчаливое переключение после PTQ.

#### W2-02-S02 — единый первый smoke contract: YOLOX-N416-BGR-v1

Это **документированный reference для будущего эксперимента**, не эмпирический golden output. Все source files закреплены одним commit **6ddff4824372906469a7fae2dc3206c7aa4bbaee**, full source hashes сохранены в `sources_manifest.json`:

- [caller](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/demo/ONNXRuntime/onnx_inference.py): `cv2.imread` → `preproc` → `[None,...]` → ORT all outputs → `demo_postprocess` → scores → xyxy/ratio → multiclass_nms.
- [preproc](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/data/data_augment.py), L142–162: uint8 BGR HWC; `r=min(416/H,416/W)`; resize `W'=int(W*r),H'=int(H*r)`, `INTER_LINEAR`, uint8; fill416×416×3 with114; paste resized image **слева сверху** `[0:H',0:W']`; padding только справа/снизу. Нет center letterbox, нет direct stretch, нет RGB swap, `/255` или mean/std. Transpose CHW, contiguous float32, add batch; input `images` shape `[1,3,416,416]`, values0..255.
- [postprocess](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/utils/demo_utils.py), `demo_postprocess`: `p6=False`; grids по stride8,16,32 в порядке52²,26²,13², x-fastest meshgrid; `xy=(raw_xy+grid)*stride`, `wh=exp(raw_wh)*stride` **ровно один раз**. Obj/channel4 и class/channel5:85 уже sigmoid, повторный sigmoid запрещён. `score_c=obj*class_c`. xywh→xyxy, divide every coordinate by original floating `r`; нет subtraction of center pad. Сохранить raw output перед изменяющим его in-place decoder.
- Точно как выбранный текущий demo: `multiclass_nms(...,nms_thr=.45,score_thr=.1)` имеет default **class_agnostic=True**: один argmax class per anchor, `score>.1`, затем общий NMS. NMS использует pixel area/intersection c `+1` и оставляет IoU `<=.45`. `.3` в parser — отдельный **visualization** threshold, не detector threshold. Для smoke `.1/.45` — фиксированные reference values из source, не универсальные производственные пороги. Переход на class-aware NMS или clipping boxes — новая версия контракта с повторной parity; сейчас не смешивать старый release NMS и текущий BGR caller.
- [COCO_CLASSES](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/data/datasets/coco_classes.py): contiguous80, `person=0`, `cell phone=67`; это не COCO category IDs1/77. Сохранён полный файл, hash `b38193c481a73f1f674cedab9e551b15b39b1a7aaed3e09e16505362cc54ad51`.

Host input envelope: `(frame_id,source_pts,H,W,original_Bgr_hash,r,H',W',input_tensor_hash,model_sha,contract_version)`. Device function получает **тот же** подготовленный tensor, возвращает `output` без hidden NMS/decoder или явно документирует отличие. Host result `(xyxy_original,score,class_idx)`; original coordinates до tracker/rules. Никакого «85-channel YOLO значит уже boxes»: конкретный grid decoder обязателен. Если runtime отдаёт иной layout/quantized output, adapter фиксирует effective layout/scale/zero-point до CPU decoder; предположений по имени API нет.

Позитивные будущие controls: человек, несколько людей, видимый near-camera phone, person возле края; прямоугольные landscape/portrait кадры с объектами у нижней/правой границы. Негативные: пустой кадр, padding-only области, два пересекающихся объекта разных classes, отсутствие телефона, мелкий/перекрытый person. Цветовая asymmetric test chart и non-square geometry chart проверяют host tensor/обратное преобразование; это не проверка качества NN. Phone bbox не доказывает phone-use; person tracks не доказывают running.

#### W2-02-S03 — официальный pose checkpoint: точные bytes и статическая metadata

[Artifact v8.3.0/yolov8n-pose.pt](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt), полный GET200, **6,832,633 B**, SHA256:

`c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212`

[Release API](https://api.github.com/repos/ultralytics/assets/releases/tags/v8.3.0), сохранён локально: published `2024-09-29T17:59:56Z`; asset195719300, created `2024-09-29T18:04:52Z`, updated `2024-09-29T18:04:53Z`, digest null. Это официальный pose artifact с проверенным полным содержимым, не HEAD-only.

Открыта ZIP central directory; прочитан только `data.pkl` **105,344 B** для disassembly, SHA256 metadata `42c094d721b9a4192f6eb5d0b0f98ed39f1f8f6d15f8a78e63494737ac7717a2`. 43,181 pickle instructions дизассемблированы, **не исполнены**. [pose_pickle_disassembly.txt](_WORK/W2-02_evidence/pose_pickle_disassembly.txt): offsets6/17 `date=2023-04-17T08:01:11.737149`; offsets50/64 `version=8.0.77`; offset91 AGPL-3.0 embedded license; GLOBAL `ultralytics.nn.tasks PoseModel` и `ultralytics.nn.modules.head Pose`; offset99140 `kpt_shape`, following values17,3; offset100620 `names`, mapping0:`person` at100641/100643. Это статические инструкции, не загруженный Python object и не runtime tensor shape. Видны ссылки FloatStorage/HalfStorage/LongStorage; из этого не объявляется единая runtime precision.

**W2-02-F02:** release label8.3.0 не равен embedded exporter/training code8.0.77. [Source v8.0.77 API](https://api.github.com/repos/ultralytics/ultralytics/commits/v8.0.77) разрешён в **5065ca36a8499b43dd4b938ba73ddb98bc6e278f**. Его loader/export надо рассматривать при будущем разрешённом переносе; совместимость с8.3.0/современным latest не проверена. Никакого actual ONNX opset/I/O этого checkpoint здесь нет. Форма `[1,56,8400]` для static640 остаётся source-derived expectation, не observed metadata. Не выбирать его для первого smoke вместо уже полученного малого ONNX.

#### W2-02-S04 — RTMPose-t: полный ZIP, оба actual outputs, dynamic axes

Дистрибьютор Tau-J, [HF exact revision/ZIP](https://huggingface.co/Tau-J/RTMPose/resolve/cd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd/rtmposev1/onnx_sdk/rtmpose-t_simcc-body7_pt-body7_420e-256x192-026a1439_20230504.zip). **Полный GET200**, **12,547,710 B**, SHA256 фактически полученных bytes:

`937003a70832d9cc34ea16927f504792f3133e92dda1b9c626236bbbe9e805cb`

Совпал с publisher LFS hash из W1; теперь это независимый full-file hash. Для прочитанных ONNX/JSON entries zipfile проверил CRC; JPG entries не извлекались/не просматривались. Извлечён `end2end.onnx`: **13,350,364 B**, SHA256:

`a6c2f6a3896a4d51131d14d7a80a3d08b50f559af5a58a45d5b098aef510a70f`

Название/date suffix20230504 не считаем датой публикации ZIP; внутри directory `20230831/...`. Сохранены exact `deploy.json`, `detail.json`, `pipeline.json`, entry list с sizes/CRC. Detail декларирует MMDeploy1.2.0, MMPose1.1.0, pth URL и config. Это publisher/export metadata, не восстановленный executed environment.

**Наблюдение ONNX:** IR6, producer pytorch1.9, default opset11. Все I/O FLOAT:

| Роль | Имя | Observed declared shape |
|---|---|---|
| input | `input` | `['batch',3,256,192]` |
| output0 | `simcc_x` | `['batch','MatMulsimcc_x_dim_1',384]` |
| output1 | `simcc_y` | `['batch','MatMulsimcc_x_dim_1',512]` |

**W2-02-F03:** эти оси реально символические. `batch_size:1` в deploy JSON не делает graph static, `dynamic_shape:true` это подтверждает. Expected17 joints из model/config/body17 не следует переписывать в observed shape. Два выходных имени и длины384/512 установлены по bytes, не только JSON. Builder, берущий output0, потеряет вертикальную координату. Нужен batch1 specialization/shape validation gate с отдельным derivative hash и проверкой сохранения **обоих** outputs; здесь не выполнялся.

168 nodes, 93 initializers; все default domain, external tensors/nested graphs/functions/sparse initializers не обнаружены. Инвентарь: Conv38, Sigmoid34, Mul48, Concat6, Add5, HardSigmoid4, GlobalAveragePool4, MaxPool3, Div3, MatMul7, Clip2, ReduceSum2, Split2, Sqrt2, Squeeze2, Relu1, Reshape1, Shape1, Slice1, Transpose1, Unsqueeze1. Сумма168. Shape/MatMul/ReduceSum и symbolic axes — отдельный frontend risk, не отрицательное доказательство совместимости LinQ.

#### W2-02-S05/F04 — полный RTMPose caller path и один affine reference

Прослежен закреплённый **Tau-J/rtmlib 03a1693e59e4f7cd84582c0fb30459b3bf18ad42**:

1. [README](https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/README.md), video example L90/L118–124: OpenCV capture→`cap.read()`→`pose_tracker(frame)`; camera/file produces BGR.
2. [PoseTracker](https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/rtmlib/tools/solution/pose_tracker.py), `__call__` L218–245, passes `image` to detector then pose. [Body](https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/rtmlib/tools/solution/body.py), L137–142, does the same direct image pass on direct-call branch. Neither converts channels.
3. [RTMPose.preprocess](https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/rtmlib/tools/pose_estimation/rtmpose.py), bbox padding1.25, affine warp, mean/std directly on incoming image. [BaseTool.inference](https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/rtmlib/tools/base.py), L125–151, only transpose/float32/batch and names all outputs. It does not swap BGR/RGB.

Таким образом для **этой documented caller chain**, а не всех произвольных callers, локальное отсутствие conversion стало подтверждённым whole-path mismatch с actual ZIP `pipeline.json Normalize.to_rgb:true`. Нельзя объявлять все пользовательские callers неправильными: caller, подающий RGB сам, устранит цветовой mismatch. Но прямой documented BGR путь его не устраняет.

Есть и новый score mismatch: pinned rtmlib `post_processings.get_simcc_maximum` L135 combines axis maxima методом **mean**; [MMPose v1.1.0 get_simcc_maximum](https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/mmpose/codecs/utils/post_processing.py), L85–87 выбирает **min**. Координаты argmax могут совпадать, но одинаковые score thresholds давать разные valid joints. Не выдавать rtmlib wrapper и SDK/MMPose contract за один воспроизведённый reference.

**Выбран единственный pose reference `RTMPose-T-SDK-RGB-affine-v1`:** actual ZIP pipeline + MMPose **v1.1.0 / 537bd8e543ab463fb55120d5caaa1ae22d6aaf06**, который явно указан publisher detail. Source references: [TopdownAffine](https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/mmpose/datasets/transforms/topdown_transforms.py), [get_warp_matrix](https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/mmpose/structures/bbox/transforms.py), [config](https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/projects/rtmpose/rtmpose/body_2d_keypoint/rtmpose-t_8xb256-420e_coco-256x192.py), [SimCCLabel.decode](https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/mmpose/codecs/simcc_label.py). Локальные копии получены по tag v1.1.0, затем tag разрешён GitHub API в этот SHA; никакого исполнения MMPose нет.

Рецепт для будущего отдельного host reference:

1. Original BGR uint8, bbox `[x1,y1,x2,y2]` в original coordinates. `center=((x1+x2)/2,(y1+y2)/2)`, initial scale `(x2-x1,y2-y1)*1.25`; reject non-positive bbox. Enlarge scale to width/height ratio192/256, без растяжения тела. Width and height — pixel units, не legacy scale/200.
2. Не UDP: rot0, shift0. Source three points: center, center+(0,-scale_w/2), third point as perpendicular to first two. Destination: `(96,128)`, `(96,128)+(0,-96)`, corresponding third point. `cv2.getAffineTransform`; `warpAffine(...,(192,256),INTER_LINEAR)`, default constant border0. Это exactly documented geometry, а не axis-aligned bbox resize или centered letterbox.
3. BGR→RGB **ровно один раз**, float32; `(RGB-[123.675,116.28,103.53])/[58.395,57.12,57.375]`. Нет дополнительного `/255`. CHW, contiguous, batch1. Сохранить original bbox, adjusted center/scale, affine и inverse matrix с tensor hash; подать `input`.
4. Получить оба outputs **по имени**. Для каждого joint взять `argmax(simcc_x)`/`argmax(simcc_y)`, divide positions by split_ratio2, score=`min(max_x,max_y)`; invalid `score<=0` отдельно. Config/ZIP: normalize false, use_dark false, flip_test false; не добавлять softmax/flip averaging/DARK.
5. Map valid crop coordinates to original: `xy_orig=xy_crop/(192,256)*adjusted_scale + center-adjusted_scale/2`; rot0 согласуется с inverse affine. Дальше только matched person track и keypoint schema COCO17, не OpenPose conversion. Source-derived target runtime shapes batch1×17×384/512 должны быть подтверждены будущим shape/runtime gate; они не заменяют таблицу observed dimensions выше.

Crop positive/negative controls: non-square bbox, bbox partly outside frame, near-border joint, tall/wide bbox, known affine grid, asymmetric RGB patches, occluded/missing joints, empty/no-person frame. Zero persons должно означать **zero pose calls**, а не fallback rtmlib `bboxes=[]→full-frame pose`. Человек может лежать без падения; pose не готовый fall classifier, нужны temporal controls.

#### Права, выбор и отказ от лишних веток

YOLOX code Apache-2.0 по W1 и pinned repository; самостоятельный полный artifact hash не решает отдельный weights grant. Для RTMPose HF card заявляет Apache-2.0, rtmlib/MMPose code licenses отдельно; publisher JSON с pth URL не доказывает права на все training imagery. Для официального Ultralytics checkpoint теперь наблюдён embedded AGPL-3.0; code policy/веса/видео не объединяются автоматически. Никаких legal выводов о распространяемом продукте здесь не делается. Согласие на съёмку и demo clips остаётся отдельным входом.

Useful: малый готовый static single-output YOLOX для person infrastructure и optional phone perception; RTMPose как резерв pose route после detector. Official v8 pose сохранён как bounded reference на случай отказа RTMPose, но дополнительный экспорт не входит в первый smoke. Rejected for immediate smoke: перенос всех сетей сразу; `.pt` как готовый ONNX; первый выход RTMPose; shape85 как decoder; generic zone как несколько behavioral scenarios; изменение opset header вместо настоящей конверсии; BGR/RGB blend между моделями; host inference как LinQ evidence.

#### Минимальный будущий parity / compile / measurement plan

Это **не выполненные команды и не обещанная точность**:

1. **Identity and CPU sanity gate.** Verify exact SHA against this report; official ONNX checker + shape/type inference в разрешённом окружении, сохранить versions/log. Для YOLOX сохранить один разрешённый legal image set с person/phone/non-square/negative controls и текущий reference tensor. Разрешить historical preprocessing ambiguity **до PTQ**: сопоставить official deployment behavior на этом exact asset с pinned BGR reference; legacy normalized variant только заранее объявленный диагностический comparator. Одна лишь согласованность CPU и LinQ на неверно нормализованном tensor не доказывает правильность perception. Если publisher provenance не уточнён и sanity не различает варианты, не выдавать contract match за closed.
2. **Raw parity gate.** CPU ONNX outputs всех имён сохранить в float32 с hash; device/imported float получает identical input tensor. Сравнить rank/layout/NaN/Inf, per-output errors и decoded bbox/class/score. Допуски определить до просмотра результатов, исходя из precision и task sensitivity; универсальных epsilon или процента успеха нет. Decoder один и тот же на обеих сторонах.
3. **Frontend/compile gate.** Получить exact SDK/compiler/runtime/device target/version и supported IR/opset/operators/attrs. Один YOLOX float graph, static batch1, без hidden NMS. Сохранить requested/effective input/output names, conversion logs, compiled artifact/hash. Opset11/IR6 не гарантия поддержки depthwise Conv/Resize/Slice attrs. Нет молчаливого удаления outputs или ручного bump номера opset.
4. **PTQ gate.** Разрешённый representative calibration set отдельно от evaluation, тот же выбранный preprocessing; save hashes/count and effective quant params. Quantized-vs-float raw and decoded parity на small persons/phones/borders. Для RTMPose калибровать **crops**, не full images; static specialization и оба outputs проверять отдельным derivative graph/hash. Не запускать pose до необходимости.
5. **Real-device gate.** Model/program hashes, actual device ID, runtime completion log, copied outputs после completion; host vs device parity. Измерить warmup/cold отдельно, inference p50/p95, transfer/preprocess/postprocess, sustained queue/drop/source-age; hardware/service/VM различать. Доступа нет, поэтому все LinQ результаты unknown. Adapter limitations W1-14 (`linq-cv-bench` first-output builder и84/85-only runner) не равны device limitations; для YOLOX verify grid decode, для pose потребуется two-output adapter.
6. **Event gate.** Реальные legal positive/negative clips с PTS; same object continuous episode→one persistent event_id→одно уведомление→журнал, gaps/ID switch/re-entry/two persons controls. Не называть person/pose detections готовыми behavioral events. NN correctness и dedup correctness проверяются отдельно.

#### Сравнение с W1 и результат по K003

| Часть K003 | Было W1 | Новое первичное доказательство | Результат |
|---|---|---|---|
| YOLOX bytes/hash | HEAD/Range501; source-derived I/O | full GET, local hash, actual IR6/opset11, all I/O,369 nodes, no external data | closed для identity/static structure |
| YOLOX pre/post | поздний BGR source без historical cross-check | release-tag RGB-normalized vs current BGR + release breaking-change text; raw decode graph/source match | scoped: один BGR reference выбран, exact provenance и numerical sanity open |
| официальный pose asset | release URL/size; shapes inferred | full checkpoint hash, safe pickle instructions8.0.77/date/names/kpt_shape/license | closed metadata; ONNX/export open |
| RTMPose actual graph | ZIP JSON и inferred17/static shape | full ZIP+ONNX hashes, actual symbolic dims, both outputs,168 nodes | contradiction для принятия static shapes как observed; static derivative open |
| RTMPose channel path | локальное отсутствие swap | полный documented BGR caller chain без swap + SDK to_rgb true | closed для этого source-path mismatch |
| RTMPose affine/post | смешанные wrapper expectations | SDK/MMPose1.1 exact reference, min-vs-mean score conflict | scoped: один recipe выбран; numerical parity open |
| LinQ | доступ/SDK отсутствуют | доступа не появилось; runtime не выдуман | open experiment/access |

**Оставшиеся Q/E:** Q1 exact accepted platform/device/runtime/operator contract; E1 historical YOLOX input sanity плюс pinned reference raw outputs; E2 CPU→imported/PTQ→real device parity и timings; E3 при выборе pose — static graph specialization, shape17 validation, two-output transfer и crop parity; Q2 отдельные разрешения weights/video. Эти пункты могут менять выбор сценариев, остальные metadata уже не нужно искать повторно.

**Ближайший шаг команды:** в выданном разрешённом окружении открыть именно local `yolox_nano.onnx` с указанным hash, проверить checker/host reference и preprocessing sanity, затем **один** graph импортировать на реальный target. RTMPose/Ultralytics не переносить одновременно. До этого честный статус — reproducible static package / BLOCKED_DEVICE, без заявленных LinQ FPS, accuracy или hardwarePASS.

<a id="F015"></a>
## F015 — Core supply: четыре exact CC BY MP4, лицензии и per-use notices

**Нормализованный статус и условия:** Авторское copyright-основание всех четырёх MP4 установлено. Residual personality/privacy/recording scope не обнуляет CC BY и не является запретом всего research/demo. Это актуальнее неизвестной identity в W1.

**Источники:** [S059](SOURCES.md#S059), [S060](SOURCES.md#S060), [S061](SOURCES.md#S061), [S062](SOURCES.md#S062), [S063](SOURCES.md#S063), [S064](SOURCES.md#S064), [S065](SOURCES.md#S065), [S066](SOURCES.md#S066), [S067](SOURCES.md#S067), [S068](SOURCES.md#S068), [S069](SOURCES.md#S069), [S070](SOURCES.md#S070), [S071](SOURCES.md#S071), [S072](SOURCES.md#S072), [S073](SOURCES.md#S073), [S074](SOURCES.md#S074), [S075](SOURCES.md#S075), [S076](SOURCES.md#S076), [S077](SOURCES.md#S077), [S078](SOURCES.md#S078), [S079](SOURCES.md#S079), [S080](SOURCES.md#S080).

**Происхождение:** [W2-07.md](_WORK/W2-07.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Дата доступа/новых проверок: **23.10.2026, 15:08–15:12 UTC / 18:08–18:12 МСК**. Прочитаны W1-12 полностью, адресные sections/manifests W1-09/W1-10, core S01–04 W1-08 и завершённый W2-02 с exact artifacts. Это адресная проверка прав и происхождения, не универсальный юридический вердикт. Не выполнялись NN inference, обучение, экспорт, компиляция; не отправлялись письма, не делались покупки. Forklift/fire grants оставлены W2-04/06.

**K008 = scoped. Существенная часть закрыта:** все четыре ранее reviewed MP4 теперь связаны с авторскими CC BY 4.0 публикациями не только по имени/ссылке. Два GitHub MP4 побайтово совпадают с реально полученными members Zenodo v2.1 ZIP; два HF MP4 совпадают по полному SHA256 и size с manifest первичного Mendeley V1. Нельзя далее писать «зеркало не сверено» для этих четырёх файлов или «лицензии видео нет». Остаток: scope personality/privacy releases для конкурсной записи; отдельный явный weights grant YOLOX release; выбор открытой/иной поставки и условия SDK compiled artifact. Существующие Apache/CC BY grants сохранены.

#### Точный вопрос для решения

Что можно включить в исходники, weight/compiled bundle, живую защиту и публичную запись именно выбранного smoke stack из W2-02 и четырёх уже reviewed видео? Не смешивать: (1) copyright материала, (2) лицензии кода/weights, (3) права изображённых людей и режим обработки, (4) распространение исполняемого/compiled artifact, (5) право записать и опубликовать сам показ.

#### Новые primary sources и наблюдения

Evidence: [W2-07_evidence](_WORK/W2-07_evidence/), [sources.json](_WORK/W2-07_evidence/sources.json), [extra_sources.json](_WORK/W2-07_evidence/extra_sources.json), [extra2_sources.json](_WORK/W2-07_evidence/extra2_sources.json). Manifest фиксирует URL, время GET, статус, size и SHA. Ошибки 404/недоступность сохранены, не трактуются как отсутствие лицензии. Python scripts — собственное bounded HTTP/static чтение, сторонний код не исполнялся. Web tool дополнительно открыл авторские Mendeley/Zenodo и owner policy; для недоступных HF/raw страниц получен обычный прямой GET.

#### W2-07-S01/F01 — Zenodo v2.1 → два конкретных GitHub MP4: identity CLOSED

Новый [Zenodo API GET](https://zenodo.org/api/records/13354453) подтверждает `dataset`, `version=v2.1`, `license.id=cc-by-4.0`, creator Ekram Alam, related GitHub `tree/v2.1`. Запись опубликована 21.08.2024, дата нашего доступа другая. [Разрешение тега v2.1](https://api.github.com/repos/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/commits/v2.1) дало **5abac7693229900cf80f722e878fbb119211fc1c** — ровно W1-09 revision. Сама запись не доказывает content identity; следующая проверка доказывает её для двух выбранных members.

Для [ZIP content endpoint](https://zenodo.org/api/records/13354453/files/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos-v2.1.zip/content) реально получены шесть HTTP206 ranges: tail65,557 B; central directory26,832 B; два local headers по30 B; два полных compressed streams5,931,157 и5,168,884 B. **Сумма11,192,490 B**, ZIP целиком1,107,545,615 B не скачан. Разобраны183 central directory entries; ZIP member streams распакованы собственным вызовом zlib и сравнены с уже локальными MP4. Оба CRC корректны, `raw == local` true. Полный MD5 всего ZIP **не проверен**; контроль отдельных полных members не является full-archive hash.

Общий member prefix: `ekramalam-GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos-5abac76/`.

| Member / локальный файл | bytes | Полный SHA256 распакованного member = SHA локального MP4 |
|---|---:|---|
| `Subject 1/Fall/11.mp4` / `W1-09_samples/positive_S1_F11.mp4` | 5,961,144 | `c25e4fc9b669cb588b6145d2cfd94f2d403083293c08bc85fa863111372bfea7` |
| `Subject 3/ADL/08.mp4` / `W1-09_samples/negative_S3_A08.mp4` | 5,172,948 | `b383bb83a22b286cfc65fdd934137ee8b29e84aef7be0b540271d7c69d10fa8b` |

Доказательства: [range_log.json](_WORK/W2-07_evidence/range_log.json), binary tail/directory, [zenodo_directory.json](_WORK/W2-07_evidence/zenodo_directory.json), [gmd_identity.json](_WORK/W2-07_evidence/gmd_identity.json), воспроизводимый [identity.py](_WORK/W2-07_evidence/identity.py). Сжатые MP4 streams не сохранены вторым комплектом: есть range locators/hashes и равные им распакованные локальные оригиналы. Identity для остальных181 entries не заявляется.

В ZIP directory есть root LICENSE1,067 B; отдельный [pinned GitHub LICENSE](https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/LICENSE) получен заново: MIT, copyright2024 Ekram Alam; архивный LICENSE member не извлекался. MIT root и dataset CC BY не следует взаимно аннулировать или молча сводить к одной лицензии. Для media используем явный авторский dataset CC BY record; accompanying materials сохраняют MIT notice также. Заявление статьи о signed consent/public repository и противоречие3 actors/4 subjects из W1-12-S05 сохраняются как авторские statements, не как нами проверенные releases.

#### W2-07-S02/F02 — Safe/Unsafe Mendeley V1 → HF MP4: identity CLOSED

Новый рабочий endpoint: [public-api/datasets/xjmtb22pff](https://data.mendeley.com/public-api/datasets/xjmtb22pff), **GET200,519,370 B**, `version=1`, DOI `10.17632/xjmtb22pff.1`, `data_licence.short_name=CC BY4.0`. Прежний пробованный `/versions/1`404 не означает отсутствия API/файлов. [Авторская страница V1](https://data.mendeley.com/datasets/xjmtb22pff/1), опубликована11.06.2024, также прямо даёт CC BY и сообщает разрешения company officials/employees. Файлы созданы в metadata09.06.2024; это не дата съёмки (авторы называют05.11–13.12.2022).

| HF/local file, revision7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5 | Primary Mendeley file id | Primary size / SHA256 = собственный full hash локального MP4 |
|---|---|---|
| `0_te23.mp4` | `a5f9d29f-535e-488f-b55f-8b870974ac39` | 6,391,494 / `e2c053d84413775e6becaf0dc2a1dd69cbfbb47a5747704345ede650d1987a7f` |
| `4_te1.mp4` | `07d51de0-0f53-4e81-930b-2f12897ee191` | 13,209,619 / `11049609f60c52702b90541e6d50146f5ff56d951c9fbf748cd164accb21226a` |

[mendeley_identity.json](_WORK/W2-07_evidence/mendeley_identity.json) сохраняет полные file records/download URL и собственные hashes. Primary MP4 повторно не скачаны: **наблюдение — primary manifest SHA + full local SHA**, а не два независимых полных GET. Для byte identity криптографического совпадения достаточно; не называть это новым визуальным review. Pinned [HF card](https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/blob/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5/README.md) также CC BY, но primary grant больше не зависит от доверия к зеркалу. Permissions statement не раскрывает текст персональных releases и не доказывает scope публичной конкурсной рекламы.

#### W2-07-S03/F03 — выбранный YOLOX nano: code grant явный, standalone weights scope отдельный

Exact graph из W2-02: [official release yolox_nano.onnx](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_nano.onnx),3,659,407 B, SHA256 `c789161ed43c8269fcd4e67c67eeeb4e80c622da2eb296a20bc6007bd18a0b7d`. Полный hash/graph — W2-02, не новая загрузка здесь.

Новые GET лицензий [release-tag e1052df…](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/e1052df71842031413f6030723c3607b839c80ce/LICENSE) и [выбранного source6ddff482…](https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/LICENSE) подтверждают Apache2.0 для repository Work. Вторая сохраняет copyright2021–2022 Megvii Inc. По [recursive tree](https://api.github.com/repos/Megvii-BaseDetection/YOLOX/git/trees/6ddff4824372906469a7fae2dc3206c7aa4bbaee?recursive=1) обнаружен LICENSE, отдельного NOTICE/licensing file нет. §4 требует копию лицензии, сохранение относящихся notices и отметку изменённых файлов; наличие NOTICE проверять и у остальных включённых dependencies.

Отдельное явное предложение «this release ONNX/weights are Apache2.0» в проверенных pinned license/README/release материалах **не установлено**. Официальная раздача в Apache repository — положительная связь publisher/provenance, не нулевое основание. Но code-license нельзя выдавать за независимо документированный полный weights grant. Для внутреннего исследования продолжать выбранный reference с сохранённой provenance; для внешнего bundle либо принять/зафиксировать командную интерпретацию scope официального release, либо получить адресное уточнение владельца/заменить artifact. Ни Apache лицензия чужого uploader, ни full SHA не закрывают этот вопрос сами по себе. Исторический preprocessing conflict из W2-02 сохраняется независимо от лицензии.

#### W2-07-S04/F04 — резерв RTMPose: uploader model-card grant и code licenses разделены

Exact ZIP W2-02: HF `Tau-J/RTMPose`, revision `cd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd`, `rtmposev1/onnx_sdk/rtmpose-t_simcc-body7_pt-body7_420e-256x192-026a1439_20230504.zip`,12,547,710 B, SHA256 `937003a70832d9cc34ea16927f504792f3133e92dda1b9c626236bbbe9e805cb`. [README этой revision](https://huggingface.co/Tau-J/RTMPose/raw/cd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd/README.md) получен200,28 B: card явно Apache2.0. Это **model repository license declaration uploader**, сильнее предположения по MMPose code license; текст не перечисляет сторонние training-data rights.

Извлечённый `rtmpose-t.onnx`:13,350,364 B, полный SHA256 `a6c2f6a3896a4d51131d14d7a80a3d08b50f559af5a58a45d5b098aef510a70f` (повторно вычислен по local bytes этой веткой). ZIP detail из W2-02 связывает модель с OpenMMLab pth и MMPose1.1.0. Новые pinned [MMPose LICENSE](https://raw.githubusercontent.com/open-mmlab/mmpose/537bd8e543ab463fb55120d5caaa1ae22d6aaf06/LICENSE) и [rtmlib LICENSE](https://raw.githubusercontent.com/Tau-J/rtmlib/03a1693e59e4f7cd84582c0fb30459b3bf18ad42/LICENSE) — Apache2.0, copyright2018–2020 Open-MMLab в полученных текстах. Сохранять notices реально заимствованных файлов и библиотеки; не заменять их одним notice команды. Выбранный SDK/MMPose RGB reference из W2-02 не равен исполненному rtmlib, поэтому rtmlib должен попасть в поставку лишь если он фактически включён. Модельный CC/data consent из этого не выводится. Source/weights grant **scoped по uploader declaration**, training-media clearance неизвестен, не автоматический запрет inference.

#### W2-07-S05/F05 — official pose fallback: новая историческая license collision

W2-02 full hash [yolov8n-pose.pt release v8.3.0](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt):6,832,633 B, SHA256 `c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212`; безопасный static metadata read обнаружил AGPL3.0 и package8.0.77. Новый [LICENSE кода8.0.77/5065ca36…](https://raw.githubusercontent.com/ultralytics/ultralytics/5065ca36a8499b43dd4b938ba73ddb98bc6e278f/LICENSE) — **GPL3.0**,35,149 B. Имя локального evidence `ultra_AGPL` исторически неудачно: содержимое GPL, его название не доказательство. [LICENSE v8.3.0](https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/LICENSE) — AGPL3.0,34,523 B.

Нынешняя [owner licensing page](https://www.ultralytics.com/license) прямо распространяет default AGPL на trained models и предлагает открытый/Enterprise варианты. Это позиция владельца на дату доступа. Нельзя вывести из старой версии training package разрешение GPL для позднее разданных exact PT bytes, отменить embedded AGPL или объявить любую демонстрацию обязательной платной. Текущий fallback учитывать под наблюдённым AGPL, historical source conflict явно сохранить. Первый YOLOX smoke не зависит от разрешения этой коллизии.

#### Per-use решение для конкретной сдачи

CC BY [legalcode](https://creativecommons.org/licenses/by/4.0/legalcode.en), §§2–3: copyright grant распространяется на копирование, адаптацию, распространение/показ при выполнении attribution; publicity/privacy/personality не предоставлены. Это два разных слоя, а не требование всегда сначала добыть полный consent для внутреннего research.

| Artifact/action | Внутренний research / inference | Живая защита с экраном | Запись/публикация или передача files |
|---|---|---|---|
| Два GMDCSA MP4 | Copyright CC BY4 установлен для exact bytes; сохранить manifest | Copyright показ разрешён с credits. Consent на public repository заявлен; scope дальнейшего показа отдельно | CC BY допускает копию/адаптацию с credits; explicit media release для новой аудитории не просмотрен. Командное решение о scope, либо собственная безопасная постановка |
| Два Safe/Unsafe MP4 | Primary CC BY4 + primary SHA match; research продолжать | Copyright разрешение есть; permissions statement первичных авторов поддерживает provenance | Публикуемый экран/кадр содержит сами видео и требует attribution; personality/privacy scope остаётся отдельным. Не называть зеркальный файл «нелицензированным» |
| YOLOX pinned code | Apache2; можно читать/использовать по условиям | Credits/source origin доступны в accompanying materials | LICENSE + applicable notices + реальные modifications. Release ONNX weights scope отдельно scoped |
| Exact YOLOX ONNX | Official provenance и reference установлены; code/weights scope не сливать | Не писать «all rights cleared». Сам показ результата не равен раздаче weights | До binary bundle закрыть явный weights scope командной интерпретацией/уточнением. Link-only поставка уменьшает раздачу, но не решает автоматически права использования |
| RTMPose HF ZIP/ONNX + реально включённый code | Card Apache2 declaration + отдельные Apache code grants | Титр model origin, data credits отдельно | Сохранить card revision/LICENSE/notices; modification notice при future shape specialization/PTQ, новые hashes. Не обещать очистку всего training imagery |
| Official yolov8n-pose fallback | Наблюдён AGPL; не нужен первому smoke | Demo не сама по себе доказательство Enterprise necessity | Открытый путь требует фактического выполнения соответствующих source/license obligations; закрытый путь не маркировать MIT. Решение о составе производного приложения и точном corresponding source отдельно |
| Future LinQ compiled graph + SDK/runtime | **Файла здесь нет**, license SDK не получена | Нельзя заявлять уже разрешённую redistributable delivery | Conversion/PTQ не создают новую свободную лицензию. Нужны exact compiler/runtime terms и права на included SDK binaries; модельные notices переносить в bundle |

**Открытая сдача:** практический вариант — исходники команды, pinned dependencies/licenses, воспроизводимый fetch manifest вместо случайно вложенных моделей, credits четырёх CC BY media и отдельная явная лицензия собственных файлов. Если включается Ultralytics, не объявлять весь репозиторий MIT: сначала определить соответствующий открытый scope и подготовить source/config/build материалы. Весь проект ещё не создан/не опубликован этой веткой.

**Иная поставка:** YOLOX/RTMPose маршрут снимает зависимость первого smoke от Ultralytics fallback, но Apache code не является универсальным разрешением на закрытый model+SDK bundle. Для contest source ZIP и для последующего embedded/коммерческого продукта оформить отдельные manifests фактически включённых components. Покупки Enterprise здесь не требуются автоматически и не совершались. Собственный постановочный clip с разрешением на CV/показ/запись — полезный вариант снять конкретную media неопределённость, но пока это предложение, не существующий артефакт.

#### Готовый credits/notices текст для нынешних неизменённых файлов

Текущий verified state: MP4 не обрезаны, не размыты, overlay/перекодирование этой веткой не выполнены; получение ZIP member не меняет MP4 bytes. Ни PTQ, ни compiled models не созданы. Поэтому не копировать условный W1-текст «размытие/фрагмент» как будто это уже сделано.

> Видео GMDCSA24 — Ekram Alam, GMDCSA24: A Dataset for Human Fall Detection in Videos, v2.1, DOI https://doi.org/10.5281/zenodo.13354453, CC BY4.0 https://creativecommons.org/licenses/by/4.0/. Использованы Subject1/Fall/11.mp4 и Subject3/ADL/08.mp4 из GitHub revision5abac7693229900cf80f722e878fbb119211fc1c; совпадение с Zenodo ZIP members проверено. Видео предоставлены без изменения. Сопутствующий MIT notice copyright2024 Ekram Alam сохранён. Использование не означает одобрения команды автором.

> Видео Video Dataset for Safe and Unsafe Behaviours — Oğuzhan Önal, Emre Dandıl, V1, DOI https://doi.org/10.17632/xjmtb22pff.1, CC BY4.0 https://creativecommons.org/licenses/by/4.0/. Файлы0_te23.mp4 и4_te1.mp4 получены из Voxel51/HF revision7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5; SHA256 совпадают с manifest первичного Mendeley V1. Видео предоставлены без изменения. Авторы не заявляли одобрения нашей системы.

> Core detector: YOLOX, Megvii, source6ddff4824372906469a7fae2dc3206c7aa4bbaee, Apache License2.0; Copyright(c)2021–2022 Megvii Inc. Official yolox_nano.onnx release0.1.1rc0; original bytes unchanged. Standalone release weight license scope is recorded separately in the rights manifest.

> Optional pose: Tau-J/RTMPose revisioncd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd, model card declares Apache2.0; MMPose1.1.0 source537bd8e543ab463fb55120d5caaa1ae22d6aaf06, Apache2.0, Copyright2018–2020 Open-MMLab. Model bytes unchanged. Optional fallback yolov8n-pose.pt: Ultralytics, observed embedded AGPL3.0; source and license details accompany any actual redistribution.

Перед внешней поставкой скопировать полные сохранённые LICENSE, а не только этот короткий титр. Future overlay/crop/blur/quantization надо описать **после выполнения**, сохранить отдельный output hash и исходный hash. Credits относятся к материалам; поведенческие labels/уведомления — вывод команды, не утверждение авторов видео. Для действительно записанного demo заменить «без изменения» на точный список изменений и включить credits в саму запись/описание, поскольку accompanying ZIP может не сопровождать видеопубликацию.

#### Сравнение с W1 и оставшиеся Q/E

| Часть K008 | W1 | W2 результат |
|---|---|---|
| GMDCSA GitHub→Zenodo | Related link, archive members неизвестны | **closed** exact two-member identity, CRC/full SHA; CC BY grant сохранён |
| Safe/Unsafe HF→author | Mirror provenance, byte identity неизвестна | **closed** primary V1 manifest SHA256/size = full local hashes |
| Code notices core | Общая Apache/AGPL классификация | **closed/scoped** pinned LICENSE сохранены, YOLOX tree без отдельного NOTICE; runtime dependencies ещё не сформированы |
| Official pose historical code license | Embedded AGPL найден W2-02 | **contradiction/scoped** training-version code GPL против embedded/latest AGPL; старый code license не заменяет observed PT license |
| YOLOX standalone weights | Отдельный grant не установлен | **open/scoped** official publisher связь есть, явный artifact-specific statement не найден в проверенных материалах |
| Consent/live/recording | Авторские permissions statements, releases не просмотрены | **scoped** copyright grants поддерживают use, scope персональных releases не выдуман; live и запись разобраны отдельно |
| Compiled delivery | SDK/файлов нет | **open** exact SDK/runtime redistribution terms и будущий model derivative manifest |

**Пять оставшихся вопросов, которые могут изменить внешнюю поставку:**

1. Q1: какой точный contest deliverable — публичный repository/source ZIP, лишь защита, запись трансляции или коммерческий embedded bundle? Зафиксировать состав до публикации.
2. Q2: команда принимает применение Apache root к official YOLOX release weights или требует адресного owner clarification? Нынешняя ветка не пишет владельцу; внутренний research продолжается.
3. Q3: имеется ли у правообладателей разрешение участников на публичную конкурсную запись/повторное размещение? Исходные заявления согласий сохранены; отсутствие текстов — unknown, не доказанный запрет. Для выбранной широкой публикации решить этот residual scope либо заменить footage собственным.
4. Q4: если задействовать Ultralytics fallback, какой фактический source/model/application scope открывается и какие build/config materials сопровождают bundle с учётом observed AGPL? Не разрешать вопрос одной старой training-version GPL.
5. Q5: какие exact LinQ compiler/runtime/SDK binaries реально передаются и что разрешает их лицензия? Без SDK terms нельзя закрыть external compiled artifact delivery.

Ближайший шаг команды: сохранить данные four-file identities/credits в итоговом manifest, выбрать Q1 delivery, продолжить технический smoke W2-02. Для public media не устраивать повторный общий поиск лицензий: copyright связь этих четырёх MP4 уже закрыта; решать оставшийся scope конкретного использования. Никаких новых accuracy/FPS/hardwarePASS эта правовая проверка не создаёт.

<a id="F016"></a>
## F016 — Падение: observable definition, pose rules и точные temporal alternatives TSSTG/PoseC3D

**Нормализованный статус и условия:** W1 pose URL v8.2.0 не отождествлять с W2 v8.3.0 по размеру. Full hash и GPL/AGPL conflict — F014/F015. Fall readiness усилена F017; consciousness не измеряется.

**Источники:** [S076](SOURCES.md#S076), [S081](SOURCES.md#S081), [S082](SOURCES.md#S082), [S083](SOURCES.md#S083), [S084](SOURCES.md#S084), [S085](SOURCES.md#S085), [S086](SOURCES.md#S086), [S087](SOURCES.md#S087), [S088](SOURCES.md#S088), [S089](SOURCES.md#S089), [S090](SOURCES.md#S090), [S091](SOURCES.md#S091), [S092](SOURCES.md#S092), [S093](SOURCES.md#S093), [S094](SOURCES.md#S094), [S095](SOURCES.md#S095), [S096](SOURCES.md#S096), [S097](SOURCES.md#S097), [S098](SOURCES.md#S098), [S099](SOURCES.md#S099), [S100](SOURCES.md#S100), [S101](SOURCES.md#S101), [S102](SOURCES.md#S102), [S103](SOURCES.md#S103), [S104](SOURCES.md#S104), [S105](SOURCES.md#S105), [S106](SOURCES.md#S106), [S107](SOURCES.md#S107), [S108](SOURCES.md#S108), [S109](SOURCES.md#S109).

**Происхождение:** [W1-01.md](_WORK/W1-01.md), `## 2.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 2. Что именно измерять

Разделить три выходных факта, чтобы не обещать неидентифицируемое:

1. `fall_suspected`: в истории одного человека произошёл быстрый переход из преимущественно вертикальной позы в низкую/лежачую.
2. `lying_observed`: видна низкая/лежачая поза; переход мог не попасть в кадр. Сам по себе этот факт не доказывает падение или нарушение.
3. `post_fall_low_motion`: после кандидата падения достаточно долго видны низкая поза и малое движение. Это основание попросить оператора проверить человека.

Модель детекции возвращает bbox, pose-модель — суставы и confidence. Ни один отдельный bbox/кадр не является событием. Неподвижность — оценка движения изображения с погрешностью, а не измерение дыхания или сознания. Нельзя приравнять `no detections`, lost track или нулевые координаты невидимых суставов к неподвижности. Метры, высоту над полом и м/с без калибровки/глубины не заявлять.

**Происхождение:** [W1-01.md](_WORK/W1-01.md), `## 3.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 3. Три предметных метода и критерии выбора

| Метод | Артефакт / нейрочасть | Temporal context | Что добавляем | Решение |
|---|---|---|---|---|
| A. Pose + история + правила | `yolov8n-pose.pt`, COCO person, 17 суставов | История 1–3 с для перехода плюс настраиваемое подтверждение low motion | Tracker, confidence gating, автомат, evidence clip | Основной путь: один 2D CNN, объяснимые события, повторно используется в других сценариях |
| B. Готовый TSSTG reference | Tiny-YOLO oneclass + AlphaPose + Two-stream ST-GCN, 7 классов | 30 последовательных pose observations одного track | Проверка cadence, сглаживание, последующая неподвижность, alert layer | Использовать только после решения доступности/прав весов; хорошие class semantics, но legacy stack |
| C. PoseC3D NTU60 | OpenMMLab SlowOnly-R50 on 17-joint heatmap volumes, 60 классов | 48 uniformly sampled frames; опубликованный test — 10 clips и mirror augmentation | Online sliding-window policy, tracking attribution, событие/low motion | Резерв при уже готовой OpenMMLab/LinQ инфраструктуре; не первый интеграционный выбор |

#### A. Минимальный рекомендованный pipeline

W1-01-F02 [первичная документация и API metadata]: фиксируем код Ultralytics **v8.3.0**, annotated tag object `a46b49a27a97d44c642882a405c8b57979e6d368`, разрешённый через GitHub API commit **`6e43d1e1e5db72afbf686dee6745669bcb124b0a`**. Официальный asset **`https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n-pose.pt`**, размер metadata **6,832,633 bytes**, release asset digest не предоставлен (`null`). Имя/размер/URL проверены через `https://api.github.com/repos/ultralytics/assets/releases/tags/v8.2.0`; бинарь не скачан, SHA256 не вычислялся. Артефакт также есть в v8.3.0 assets с тем же размером; не следует считать одинаковый размер доказательством идентичного hash. Для воспроизводимости брать именно один указанный URL и затем зафиксировать SHA256.

W1-01-S01 — [pose docs v8.3.0](https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/docs/en/tasks/pose.md), локаторы `Models`, `Predict`, `Export`. Установлены COCO-pretraining и официальный ONNX export `yolo export model=yolov8n-pose.pt format=onnx`. Табличные COCO accuracy и скорости других ускорителей не являются качеством fall detector и не переносятся на LinQ. Текущая неприкреплённая docs/tasks/pose уже описывает другие поколения, поэтому для этого решения использован versioned файл.

W1-01-S02 — [dataset mapping](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/cfg/datasets/coco-pose.yaml), строки 16–22: `kpt_shape: [17,3]`, единственный class **0 person**. Порядок суставов: 0 nose; 1/2 left/right eye; 3/4 ear; 5/6 shoulder; 7/8 elbow; 9/10 wrist; 11/12 hip; 13/14 knee; 15/16 ankle. Источник не содержит классов falling/lying.

W1-01-S03 — [predictor preprocessing](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/predictor.py), `preprocess`, `pre_transform`, строки 115–156. Для numpy OpenCV: LetterBox, BGR→RGB, BHWC→BCHW, contiguous, float, `/255`. Proposed compiled input: static `1×3×640×640`, FP32 сначала; FP16/INT8 только после parity. Letterbox scale/padding сохранить и обратить для bbox/keypoints, иначе история смешивает координаты разных пространств. PyTorch predictor может выбрать rectangular minimal padding; тест LinQ должен явно использовать тот же fixed square preprocessing.

W1-01-S04 — [head.py Pose.forward / kpts_decode](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/nn/modules/head.py), строки 219–255; [PosePredictor.postprocess](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/models/yolo/pose/predict.py). **Выведенный из структуры**, ещё не проверенный реальным export output для static 640 raw ONNX: `1×56×8400` = 4 bbox + 1 person score + 17×(x,y,confidence). Это decoded dense predictions до host NMS, а не готовые tracks. После NMS keypoints reshape в `N×17×3`, scale обратно в исходный кадр. Проверить реальные имена/формы тензоров через ONNX metadata и compiler, не писать их как измеренный результат.

W1-01-F03 [инженерное предложение, не опубликованная точность]: CPU-side tracker сопоставляет bbox между кадрами (для одного человека в демо достаточно геометрического tracker; crowded scene требует отдельной проверки). Для каждого track сохраняются timestamp, raw bbox/pose, confidence, признаки, quality. Исходные позиции тоже хранятся: нормализация каждого skeleton в его собственный bbox уничтожает абсолютное снижение тела в кадре.

Признаки A:

- Средние координаты плеч и таза только по видимым точкам; угол torso shoulder-mid→hip-mid к вертикали кадра; устойчивый наклон, изменение угла и изменение высоты/ширины person bbox.
- Быстрый спуск hip/torso относительно собственной недавней вертикальной высоты человека `H_ref`; скорость в `H_ref/second`, не м/с. `H_ref` брать robust median из видимых upright кадров и замораживать на время кандидата.
- Изменение масштаба и aspect ratio — вспомогательные признаки: bbox расширяется при работе руками, а падение вдоль optical axis может почти не дать горизонтального тела.
- Low motion в низкой позе: robust median displacement видимых суставов и центра bbox в image coordinates, нормированный на `H_ref` и Δt. Дополнительно можно наблюдать optical-flow/motion energy внутри person region, но фон и перемещение камеры требуют компенсации. Одного центра bbox недостаточно: человек двигает конечностями, оставаясь на месте.
- Приоритет confidence: таз, плечи, колени/лодыжки. Отсутствие лодыжек не автоматически исключает всё, но снижает качество; если поза недостаточно наблюдаема, `unknown`, а не forced falling. Для bbox-only пути качество идентификации причины ниже.

Для стендового кандидата переход оценивать по 1–3 с истории и low-motion подтверждать на отдельном настраиваемом интервале. Эти числа — старт инженерного smoke-test, **не универсальные медицинские/нормативные пороги**. Хранить параметры в конфигурации; сравнить несколько значений по небольшому фиксированному positive/negative пакету. Даже идеально измеренная быстрая смена позы не всегда отличает добровольное быстрое укладывание от падения: при одинаковом видео причина неидентифицируема; событие оставлять подозрением для оператора.

#### B. Что реально есть в Human-Falling-Detect-Tracks

W1-01-S05 — [repository](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks), зафиксированный API commit **`7ed2faa4d6147dfd576f58869b6c25545208af35`**, 2021-10-02. README описывает Tiny-YOLO person → AlphaPose → ST-GCN по 30 кадрам; обучение action branch на вручную размеченных skeleton Le2i Coffee room/Home. Указанный исходный стенд i7-8750H/RTX2070 не сопровождается воспроизводимой latency table, поэтому не переносить его на LinQ. README публикует ссылки на detector, pose и TSSTG веса; сами `.pth` в Git tree отсутствуют.

W1-01-S06 — [ActionsEstLoader.py](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks/blob/7ed2faa4d6147dfd576f58869b6c25545208af35/ActionsEstLoader.py), init/predict. Exact zero-based classes: **0 Standing, 1 Walking, 2 Sitting, 3 Lying Down, 4 Stand up, 5 Sit down, 6 Fall Down**. Ожидаемый локальный файл `./Models/TSSTG/tsstg-model.pth`. Вход loader `T×V×3` (x,y,score), normalize по размеру изображения, затем per-pose scaling; добавляет shoulder-mid node, permutation в NCTV; motion — разности соседних нормализованных xy. Return shape `1×7`.

W1-01-S07 — [PoseEstimateLoader.py](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks/blob/7ed2faa4d6147dfd576f58869b6c25545208af35/PoseEstimateLoader.py), строки 26–35; [Graph](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks/blob/7ed2faa4d6147dfd576f58869b6c25545208af35/Actionsrecognition/Utils.py), `coco_cut`. Удаляются глаза и уши: исходные COCO индексы `[0,5,6,7,8,9,10,11,12,13,14,15,16]` → 13 joints; loader добавляет neck/shoulder-mid → 14. **Нельзя подать 17 COCO точек напрямую.** Для YOLO pose adapter надо сохранить этот порядок и confidence; замена AlphaPose на YOLO даёт distribution shift и требует проверки, даже если формы совпадают.

W1-01-S08 — [Models.py](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks/blob/7ed2faa4d6147dfd576f58869b6c25545208af35/Actionsrecognition/Models.py), TwoStreamSpatialTemporalGraph.forward. Точные входы при 30 observations: **points `1×3×30×14`, motion `1×2×29×14`**, выход `1×7` после **sigmoid**, а не mutually exclusive softmax. Не трактовать выведенный на экран процент как откалиброванную вероятность события; классы выбираются argmax. В graph convolution есть `einsum` в ST-GCN modules: поддержка ONNX lowering/целевого compiler не доказана.

W1-01-S09 — [main.py](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks/blob/7ed2faa4d6147dfd576f58869b6c25545208af35/main.py), `preproc`, parser defaults, action loop. Default detector size 384, pose 224×160/resnet50; RGB conversion; tracker max_age=30, n_init=3; классификация когда буфер длины 30; цвета для Fall Down и Lying Down. Это **визуализация action label**, не готовый alert с подтверждением неподвижности, дедупликацией и evidence lifecycle. В коде TSSTG создаётся без передачи CLI device: `--device cpu` не гарантирует CPU для всех ветвей. README basic invocation расходится с parser: реально видео передаётся через `-C/--camera`, не позиционным аргументом.

Temporal caveat [вывод]: 30 observations ≠ 30 секунд. При 30 Hz это около 1 с; при 10 Hz около 3 с; при пропусках наблюдений длительность ещё меняется. Для learned classifier нельзя произвольно сменить sampling cadence без проверки. Интерполяция пропусков должна иметь max-gap, длинный lost interval сбрасывает valid classification window.

Точные опубликованные ссылки весов из README:

- Tiny-YOLO `.pth`: https://drive.google.com/file/d/1obEbWBSm9bXeg10FriJ7R2cGLRsg-AfP/view?usp=sharing
- `.cfg`: https://drive.google.com/file/d/19sPzBZjAjuJQ3emRteHybm2SG25w9Wn5/view?usp=sharing
- AlphaPose resnet50: https://drive.google.com/file/d/1IPfCDRwCmQDnQy94nT1V-_NVtTEi4VmU/view?usp=sharing
- AlphaPose resnet101: https://drive.google.com/file/d/1N2MgE1Esq6CKYA6FyZVKpPwHRyOCrzA0/view?usp=sharing
- TSSTG: https://drive.google.com/file/d/1mQQ4JHe58ylKbBqTjuKzpwN2nwKOWJ9u/view?usp=sharing

W1-01-F04 [реальная HTTP проверка]: малый GET последнего TSSTG `/view` через urllib 2026-10-23 вернул **404 Not Found**; browser open тоже не дал файл. Это свидетельство недоступности по этой ссылке в исследовательской среде, не доказательство окончательного удаления или отсутствия разрешённого зеркала. Остальные Drive weights не проверены до binary metadata. Hash, размер и права checkpoint не установлены. Нельзя называть pipeline download-and-run до решения этого блокера. GitHub recursive tree API показал только `SPPE/LICENSE` среди license files; root LICENSE не найден. Лицензия части не разрешает автоматически копировать весь application/action classifier.

#### C. PoseC3D: реально доступный запасной checkpoint

W1-01-S10 — [official model zoo](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/README.md), `NTU60_XSub`. Зафиксирован API commit **`a5a167dff2399e2d182a60332325f9c0d4663517`**, 2026-03-18. Предобученный keypoint checkpoint:

https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint_20220815-38db104b.pth

**HEAD 200**, Content-Length **8,246,969**, Last-Modified **2022-09-21**, ETag `04E568A88614A15BF1AE8FBBC72523BB`. Это metadata-доступность файла; полный download, SHA256, load/inference не проверены. Zoo заявляет 93.6% top1 NTU60_XSub, 20.6G FLOPs, 2.0M parameters и 10-clips evaluation; это multi-class benchmark, не sensitivity к реальным падениям на заводе и не end-to-end latency.

W1-01-S11 — [exact config](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/slowonly_r50_8xb16-u48-240e_ntu60-xsub-keypoint.py), model и val/test_pipeline. Вход ResNet3dSlowOnly — **17 heatmap channels**, classifier 60 classes. UniformSampleFrames clip_len=48; PoseCompact → resize short side64 → CenterCrop64 → GeneratePoseTarget sigma0.6/use_score → NCTHW_Heatmap. Validation: один clip. Test: 10 clips, double=True с left/right flip; стоимость benchmark не равна одному online inference. Proposed deployment tensor для одного clip: `1×17×48×64×64`, **вывод из config, не проверенный export graph**. Не путать train crop56 с val/test crop64.

W1-01-S12 — [class map](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/tools/data/skeleton/label_map_ntu60.txt): **42 falling zero-based = A43**, **7 sitting down**, **8 standing up**, **41 staggering**. Отдельного stationary lying/unconscious class здесь нет. 48 frames — семплирование исходного action clip, не определённая авторами длительность causal online alarm. Нужна своя фиксированная политика окна и stride; accuracy после этого неизвестна.

W1-01-S13 — [MMDeploy supported models](https://raw.githubusercontent.com/open-mmlab/mmdeploy/main/docs/en/04-supported-codebases/mmaction2.md), раздел Supported models: перечислены TSN/SlowFast/TSM/X3D; **PoseC3D в этой таблице не найден**. Следовательно нельзя обещать его стандартный deployment только потому, что MMAction2 поддержан. Ручной ONNX export нейросетевого backbone/head технически возможен как гипотеза; Conv3D/compiler и preprocessing остаются испытанием. Лицензия [MMAction2 code](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/LICENSE) Apache-2.0; отдельная однозначная лицензия именно checkpoint не установлена. NTU data rights ниже.

**Происхождение:** [W1-01.md](_WORK/W1-01.md), `## 4.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 4. Видео, права и отрицательные контроли

W1-01-S14 — [UR Fall Detection Dataset, первичная страница](https://fenix.ur.edu.pl/~mkepski/ds/uf.html), описание/лицензия/таблицы/Extracted features. 70 sequences: 30 falls, 40 ADL; fall RGB/depth с двух Kinect, ADL с camera0. Страница даёт индивидуальные PNG-sequence zip и видео-ссылки. Rights: **CC BY-NC-SA 4.0, non-commercial academic**, коммерческое использование по обращению к авторам. У derived depth features label -1 not lying, +1 lying, 0 transient falling; переходные 0 авторы не используют в своей posture classification. Это наглядно показывает различие обучения «лежит» и детекции события. RGB-only метод не получает миллиметровые depth features бесплатно. Полный media download и визуальная проверка не выполнялись. Дополнительная metadata-проверка ниже подтверждает доступность конкретных файлов, но не качество сюжета и не право их публичного показа на коммерческом мероприятии.

W1-01-S15 — [NTU RGB+D official](https://rose1.ntu.edu.sg/dataset/actionRecognition/), Action Classes, How to Download, Terms & Conditions. Подтверждён A43 falling down; download требует регистрации/одобрения/соглашения. Данные — academic research / noncommercial; перераспространение и commercial usage без разрешения запрещены, показ изображений субъектов ограничен academic publications/presentations. Не считать pretrained checkpoint, code license и право показывать исходное NTU-видео одним разрешением. NTU брать как источник семантики/модели, не основной быстрый demo-video канал.

W1-01-S16 — [Ultralytics license, первичная политика производителя](https://www.ultralytics.com/license), FAQ trained models и choosing license. Производитель указывает AGPL-3.0 по умолчанию для кода/обученных моделей и отдельную Enterprise поставку для закрытого использования. Это позиция правообладателя, не индивидуальное юридическое заключение. Данные COCO и исходные изображения имеют собственные права; AGPL модели не выдаёт разрешение на показ любого training/demo video. Для hackathon решать лицензию поставки отдельно от технического smoke-test.

**Самый быстрый контролируемый demo package** [предложение]: свои staged ролики с согласиями, безопасным исполнением на мате/имитацией и разрешением на публичный показ; фиксированная камера, виден весь человек до перехода и после него, масштаб близок будущему CCTV. Самостоятельная постановка позволяет иметь точный onset и достаточно длинный post-fall интервал; не выдавать её за реальные несчастные случаи. Сохранить исходную частоту и timestamps. Для независимости controls разнести по людям/ракурсам, а не выбрать лучший take.

| Контроль | Что должно произойти | Ошибка, которую ловит |
|---|---|---|
| Падение боком, сзади/вперёд с длительным лежанием | Один fall candidate, затем одно post_fall_low_motion | FN из-за направления/видимости, дубли |
| Падение и быстрое вставание/перекат | Кандидат возможен, устойчивого low-motion alarm нет | Слипание fall с immobility |
| Присед, наклон за предметом, завязывание обуви | Не подтверждать post-fall event | Высота/bbox threshold FP |
| Обычное/быстрое сидение на стул | Не подтверждать fall+lying | Спуск таза без перехода к лежанию |
| Добровольное укладывание/лежание для ремонта | `lying_observed`; не гарантировать распознавание намерения | Ложная причинность и отсутствующая history |
| Камера стартует с уже лежащим человеком | Отдельный lying observation/настраиваемая review escalation | Выдуманное падение до начала записи |
| Человек лежит, но двигает руками/ногами | Low-motion condition не проходит либо сбрасывается | Использование только bbox center |
| Пропал за станком/вышел за край/другой человек перекрыл | Quality unknown, таймер подтверждения не растёт | No detection = immobile |
| Два человека пересеклись, один присел | Не сшивать истории людей | Track ID switch |
| Камера дрогнула, панорама, сильная тень | Quality gate/компенсация, не подтверждать вслепую | Видимое движение фона/ложный спуск |
| Падение вдоль оптической оси, частично за предметом | Отдельно измерить FN/unknown, не скрывать | Неуниверсальность горизонтального bbox |

W1-01-F05 [реальные HEAD, 2026-10-23]: из первичного HTML URFD извлечены и проверены точные файлы:

- https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0.mp4 — **200**, **1,299,104 bytes**, `video/mp4`.
- https://fenix.ur.edu.pl/~mkepski/ds/data/adl-01-cam0.mp4 — **200**, **1,194,846 bytes**, `video/mp4`.
- https://fenix.ur.edu.pl/~mkepski/ds/data/fall-01-cam0-rgb.zip — **200**, **57,727,213 bytes**, `application/zip`; не скачан.

Это компактная пара positive/negative кандидатов для разрешённого smoke-test без загрузки всего датасета. Длительность, реальный fps, тело/окклюзия, достаточность неподвижного хвоста, сюжет ADL и визуальные аннотации **не установлены** до просмотра. Head Content-Type/200 не заменяет декодирование. Все ограничения W1-01-S14 сохраняются.

**Происхождение:** [W1-01.md](_WORK/W1-01.md), `## 7.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 7. Отказанные/ослабленные варианты

- **Один bbox aspect ratio / fall detection по одному кадру**: допустим cheap trigger `lying_possible`, но не отвечает падение vs сидение/ремонт/окклюзия. Не брать основной event detector.
- **Детектор классов fallen/normal с неизвестного HF/Roboflow зеркала**: без проверенных веса/данных/license/class semantics не сильнее официального pose+правил; не тратить дедлайн на красивый demo без происхождения.
- **MediaPipe pose как автоматическая замена**: иная landmark topology/preprocessing, person-tracking assumptions и перенос в LinQ не проверены; существование host API не доказывает deployability.
- **TSSTG download-and-run**: отложен из-за 404 checkpoint, старой среды, неполных прав, отсутствия подтверждённого ONNX/LinQ export. Возможное разрешённое зеркало и hash могут вернуть его в shortlist.
- **PoseC3D как основной путь**: checkpoint доступен, но добавляются heatmaps, 3D convolutions, online temporal policy и NTU domain gap; MMDeploy support не установлен. Не даёт готовую post-fall immobility state machine.
- **Порог 30 с для каждого случая / «без сознания»**: не следует из кейса/источников; задержка помощи и причина неподвижности не эквивалентны наблюдаемому CV-сигналу.

<a id="F017"></a>
## F017 — Падение: шесть decoded/reviewed GMDCSA clips, интервалы/видимость/hold/censoring

**Нормализованный статус и условия:** W2-03 ранний rights остаток ZIP identity для старой пары закрыт поздним F015. Четыре новых MP4 связаны по author record/revision, но не все проверены как ZIP member. Max gross-low-motion 6.432033s; H10/H30 не eligible.

**Источники:** [S059](SOURCES.md#S059), [S062](SOURCES.md#S062), [S110](SOURCES.md#S110), [S111](SOURCES.md#S111), [S112](SOURCES.md#S112).

**Происхождение:** [W2-03.md](_WORK/W2-03.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Проверка **23.10.2026**, завершение около **14:59 UTC /17:59 МСК**. Входы: полный текст W1-09/W1-12, их source CSV/manifest/локальная MP4-пара и K004/K008/K011 из PROMPT_W2-03. Общие итоговые файлы не менялись. Это получение и ручная содержательная проверка данных, **не benchmark, не нейроинференс, не LinQ PASS**. Чужой код не исполнялся, обучения/экспорта/компиляции/установки зависимостей не было.

#### Решение для выбора сценария

**K004 scoped:** теперь есть реальная дополнительная последовательность `upright→descent→settling→gross low-motion` с консервативно принятым непрерывным видимым хвостом **6.432033 s**, а также полностью проверенные bend/exercise/visibility controls. Это существенно сильнее W1, где новые controls были лишь Range/metadata, а fall-пара была просмотрена по восьми кадрам. Но полного промышленного сценария с H10/30s, выходом из low-motion, повторным событием и независимым holdout пока нет.

**Новый основной candidate W2-03-F01:** GMDCSA Subject3/Fall/07.mp4. Все 269 кадров просмотрены последовательно на листах без временного subsampling; источник полностью декодирован до EOF. На frames76–268, PTS **2.560033–8.992067**, сохраняется лежачая gross-поза без заметного крупного перемещения конечностей/туловища. Голова и туловище видны; тело близко к нижнему левому краю, детали пальцев/дыхания по такому просмотру не устанавливаются. Поэтому label именно `low_motion_gross_posture`, **не абсолютная неподвижность, не потеря сознания**. Измерение количественного движения будущей pose-системы ещё не выполнялось.

#### Первичные источники и воспроизводимые артефакты

**W2-03-S01.** База **G** = `https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/`. Exact commit из W1 сохранён; новые полные GET выполнены по этому commit, без latest. [Закреплённый README](https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/README.md) открыт вебом и сохранён; README ещё цитирует v2.0, тогда как фактический источник — v2.1 commit. Это не исправлено молча. История версии/дата публикации — сведения источника; дата получения — 23.10.2026.

**W2-03-S02.** [Авторский Zenodo API record13354453](https://zenodo.org/api/records/13354453): собственный requests GET200, 3,960B, snapshot `W2-03_evidence/zenodo_record.json`. `metadata.license.id=cc-by-4.0`, `version=v2.1`, `publication_date=2024-08-21`, related identifier указывает GitHub tree/v2.1. HTML-record вебом timeout, API реально получен. ZIP1,107,545,615B **не скачивался**; соответствие ZIP members нашим GitHub binary на уровне bytes неизвестно. Это авторский связанный источник grant, не доказанный hash-match архива.

**W2-03-S03.** [Статья, fullTextXML PMC11416611](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11416611/fullTextXML), DOI `10.1016/j.dib.2024.110892`: собственный GET200, 201,615B, `article.xml`. Прочитаны Experimental Design и Ethics Statement: постановочные indoor-сцены, фиксированная laptop-camera, ручная clip/CSV-разметка; §4 описывает четыре субъекта/три комнаты, Ethics — три актёра и подписанные согласия на public repository. Противоречие чисел и отсутствие текста release сохраняются. Subjects2/3 делят Room2. Основной PMC HTML вернул CAPTCHA; неверный NCBI OA endpoint —404. Никакого обхода доступа не выполнялось.

**W2-03-S04.** [LICENSE exact commit](https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/LICENSE): GET200, 1,067B, MIT Copyright2024 Ekram Alam, сохранён рядом. MIT и Zenodo CC BY не объявляются взаимоисключающими и не смешиваются с правами на weights/личность.

**W2-03-S05.** Новые полные source snapshots `Subject1_ADL.csv`, `Subject2_Fall.csv`, `Subject3_Fall.csv`, `Subject4_Fall.csv`, `Subject4_ADL.csv`. При отборе F01 использован source S3/Fall.csv: ранний transition около1s при clip9s. После получения coarse `Falling[1 to9]` **не** перенесён на весь хвост: свои фазы записаны отдельно. Оригинальные CSV не редактировались.

Все exact URLs/status/bytes/SHA256 сохранены в [downloads.json](_WORK/W2-03_evidence/downloads.json). Собственные bounded acquisition/decode/annotation scripts лежат рядом и не используют чужой executable. Четыре новых MP4 суммарно **22,212,338B**. Это отдельные файлы, не большой dataset archive. Два прежних MP4 использованы на месте без повторной загрузки.

#### Фактически полученные media и decode

У всех шести H.264/time_base **1/30000**. Полный собственный PyAV18.1.0 decode завершился EOF без exception; PTS есть у каждого кадра и строго возрастают. **104+128+269+220+146+181=1,048 кадров**. FPS не фиксировали равным30: измеренные соседние шаги0.0315–0.079833s. Это source timing, не performance устройства. Таблицы каждого PTS/целочисленной duration и полные metadata находятся в [decode_manifest.json](_WORK/W2-03_evidence/decode_manifest.json) и шести `*_pts.csv`.

| ID | Path после G / локальный stem | Полные bytes / кадры / первый–последний PTS, s | SHA256 |
|---|---|---|---|
| W2-03-F01 новый | `Subject%203/Fall/07.mp4` / `Subject3_Fall_07` | 9,262,980 /269 /0–8.992067 | `86a20851a1d3bfacbe11d8977972f95a256893b80cd4de66dc7bb224a4dca55b` |
| W2-03-F02 новый | `Subject%201/Fall/13.mp4` / `Subject1_Fall_13` | 1,389,022 /128 /0.033333–4.321333 | `955a1e53161fc84b53604815fed71ea872cc18fba0473e4e184c85bf3fe59a67` |
| W2-03-F03 новый | `Subject%201/ADL/16.mp4` / `Subject1_ADL_16` | 3,582,225 /104 /0.033333–3.521400 | `e4e8574c3f9da325757a17f123807ff2ffe31abca4bbbb146a67e5d5f82dad77` |
| W2-03-F04 новый | `Subject%204/ADL/05.mp4` / `Subject4_ADL_05` | 7,978,111 /220 /0–7.328333 | `d7bd6f68df5f0c526ab2a1ada10eac780fd429e7cfb58cc14b673eaf1d682d69` |
| W2-03-F05 W1 pair | `Subject%203/ADL/08.mp4` / `negative_S3_A08` | 5,172,948 /146 /0–4.864067 | `b383bb83a22b286cfc65fdd934137ee8b29e84aef7be0b540271d7c69d10fa8b` |
| W2-03-F06 W1 pair | `Subject%201/Fall/11.mp4` / `positive_S1_F11` | 5,961,144 /181 /0.033333–6.097400 | `c25e4fc9b669cb588b6145d2cfd94f2d403083293c08bc85fa863111372bfea7` |

F02=640×480; остальные1280×720. Точные средние rates и stream.duration — в manifest. **Последний наблюдаемый PTS не всегда равен container duration**: например F01 stream.duration270762/30000=9.0254s, последний кадр8.992067s. При ограничении H здесь используется последний реально просмотренный PTS, без прибавления невидимого frame lifetime или остатка контейнера.

Контактные листы здесь **all-frame**, 80 последовательных кадров на страницу с номером и PTS, thumbnail192×108. Открыты все16 листов шести clips. Это содержательный просмотр каждого кадра выбранного интервала, а не только успешный decoder. Метод имеет ограничение: он проверяет крупные движения/видимость, но мелкие движения не гарантирует; нет второго независимого аннотатора и adjudication. Реальная full-resolution media сохранена для последующей проверки спорных деталей. Источник не перезаписан, кадры не зацикливались и не замораживались. У F01 все269 декодированных RGB-frame hashes различны, в принятом хвосте193/193 различны (`F01_frame_uniqueness.json`); это исключает точное повторение decoded frames в данном файле, но само по себе не доказывает authentic capture.

#### Собственная actor/phase/visibility GT

[own_phase_visibility.csv](_WORK/W2-03_evidence/own_phase_visibility.csv) — **собственная**, отдельная от author CSV, покрывает все1,048 кадров неперекрывающимися последовательными интервалами. Frames **0-based**, конец включён; секунды — raw presentation PTS. Это один ручной исследовательский проход по всем кадрам, не certified frame-GT и не bbox/keypoint labels. Границы gross-фаз имеют практическую неопределённость около1–2 кадров; записанные точные PTS — timestamps выбранных frames, а не гарантия точного физического onset.

| ID / actor | Собственные наблюдения по полному clip | Использование в event reference |
|---|---|---|
| F01/S3 | 0–28 upright;29–59 descent;60–75 lying/settling;76–268 stable gross lying | Основной transition→short low-motion candidate. Source fall-label говорит о постановке; наблюдение не раскрывает намерение и не делает «намеренность» распознаваемым классом |
| F02/S1 | 0–7 standing у края;8–38 descent;с39 (PTS1.3774) голова/часть тела уходит за нижний край и не возвращается | После потери видимости whole-body-motion=unknown. Видимые колени не доказывают неподвижность всего тела. Это partial-frame visibility control, **не** краткая окклюзия→reacquisition |
| F03/S1 | 0–7 seated;8–35 bend/reach;36–47 низко наклонён;48–69 возвращается;70–103 seated | Hard negative: берёт предмет с пола сидя на стуле; низкая голова/torso не должна автоматически стать fall. Phone из source description, визуальный target — reach, не phone-use детектор |
| F04/S4 | 0–47 walk/stand, начало обрезано сверху;48–79 supported bend;80–118 supported plank;119–153 torso down;154–172up;173–192down;193–219up | Exercise hard negative и low-head/crop control. Упоры и повторные движения видимы; низкая поза не stationary positive. При уходе torso за край motion unknown, а не zero |
| F05/S3 | 0–8 уже сидит;9–55 reclines с опорой;56–145 лежит с малыми корректировками головы/рук | Source ADL intentional lying; negative к fall-like быстрым descent из upright. Intentionality — author label/наблюдаемая опора, а не медицинский факт. Для policy «любое lying» мог бы быть positive, поэтому правило надо назвать заранее |
| F06/S1 | 0–23 standing;24–69 lowering/recline;70–92 bent knees;93–113 изменение положения ног/settling;114–180 stable gross lying | Прежний positive содержит реальное движение ног после descent. Новый консервативный stable interval короче всего остатка:3.889367–6.097400=2.208033s |

**Не найдено в этих clips:** ремонт на коленях в industrial-like окружении; fully visible лежит+двигает только одной рукой/ногой долго при неподвижном torso; unknown→reacquire того же episode; clear→новый fall; два актёра одновременно. F06 проверяет явное движение ног, F04 — exercise, но ни один не заменяет все эти отдельные controls.

#### Допустимый H, censoring и передача K011

[event_intervals.json](_WORK/W2-03_evidence/event_intervals.json) содержит actor/rule/episode, low-motion start/end frame+PTS, duration bound, censoring, clear/rearm flags. Это **ручной reference вход**, не executed notification system.

- F01: консервативно принятый максимальный непрерывный gross-low-motion интервал этого review **[2.560033,8.992067]**, **6.432033s**. Eligibility по длине: **0<H≤6.432033s** только при принятой gross-motion/visibility policy. Это диапазон доступного наблюдения, не рекомендация выбирать H малым ради PASS и не универсальный порог. Истинный физический onset может быть раньше; более ранний settling не кредитуется.
- F06: принятый gross-low-motion интервал **[3.889367,6.097400]**, **2.208033s**, аналогично0<H≤2.208033s. Если требуется, чтобы **оба** accepted positives могли пройти hold, общий структурный предел **H≤2.208033s**. Для H между2.208033 и6.432033 F06 остаётся censored, F01 ещё потенциально eligible.
- H10s/H30s: **ни одного eligible positive**. Нельзя считать не выданный alert FN, если полного требуемого наблюдения не было; это unobservable/censored. Нельзя достраивать хвост повтором/стоп-кадром или суммировать короткие отрезки.
- Обе low-motion последовательности заканчиваются EOF: **right-censored active observation**, recovery/clear отсутствуют. EOF не равен clear/ACK. F05 начинается seated, поэтому standing prehistory left-censored; не выводить «падения не было до начала записи». F02 после crop — unknown; это потеря информации, не доказанное завершение.
- Для frozen H eligibility/deadline вычислять **по PTS**: первый кадр, у которого `PTS-startPTS≥H`, при непрерывном accepted visibility/motion. Например предложенный только для иллюстрации H5s делает F01 потенциально eligible после7.560033s, но ещё не доказывает результат модели. Сам H не выбран этой веткой.
- W2-08 получает F01-E1/F06-E1 и controls. Сопоставлять одно событие на actor×rule episode; повторные alerts — duplicate. Unknown не должно порождать новое independent episode; исход после reacquisition здесь не проверен. ACK не является observed recovery. Ни event latency, ни FP/hour, ни end-to-end PASS этими файлами не измерены.

#### Независимость, domain и права по конкретной поставке

**Все шесть теперь reviewed/dev**, включая F01. Ни один не остаётся слепым holdout после подбора фаз и H-бюджета. F01/F05 — Subject3/Room2, F02/F03/F06 — Subject1/Room1, F04 — Subject4/Room3. Эти группы не делить по кадрам/соседним windows; Subject2 тоже Room2, поэтому «другой subject» сам по себе не даёт нового room-domain. Исходные recording sessions и overlap pretraining будущих weights неизвестны. Контактные листы показывают разные takes, hashes различны, но это не доказывает statistical independence. Отдельная новая session/camera с freeze параметров нужна до оценки holdout. Домашняя постановка не валидирует завод/PPE/малый actor/night/dust.

| Артефакт / действие | Доказательство и условия | Остаток |
|---|---|---|
| Четыре новых GitHub MP4; copy/decode/internal research | Полные public GET, exact commit/hash; GitHub MIT notice и авторская связанная dataset CC BY4 S02. Notices сохраняются | ZIP-member identity не проверена; dataset grant не переназначается весам |
| Те же MP4, internal neural inference | Copyright основание копирования/data use имеется; сами neural runs здесь не выполнялись | Лицензии model/code/runtime проверяются отдельными ветками |
| Те же MP4, live display | CC BY record поддерживает copyright public-display право при attribution, указании изменений и notices; авторы заявляют public-repository consent | Полный release/likeness scope и3/4 actors неизвестны; не писать «лицензии нет» и не обещать полную очистку всех прав |
| Запись защиты/публичный upload/передача MP4 | Та же CC BY связь и условия; при фактической поставке перечислить конкретные4 hashes и их источники/изменения | Внешняя аудитория/личные права остаются отдельным unresolved полем; для уверенного публичного ролика собственный take с release — практичный путь |
| Source/compiled weights, код приложения | Эта ветка не получала/не включала weights или приложение | GitHub media MIT/Zenodo grant не доказывает их права; training не выполнялся и не требуется для этого evidence pack |

Готовая строка credits: **«GMDCSA24 — Ekram Alam et al.; dataset v2.1, DOI10.5281/zenodo.13354453; GitHub commit5abac7693229900cf80f722e878fbb119211fc1c; Zenodo dataset CC BY4.0; repository MIT notice retained. Изменения: собственная фазовая/visibility-разметка и контактные листы; исходные MP4 не изменены».** При реальном монтаже дополнить только фактическими crop/blur/trim. Оригинальные consent не получены, писем не отправляли. Весь K008 проекта не закрыт этой веткой; точные4 media и scope передаются W2-07.

#### Полезные кандидаты и отклонения

F01 принят для короткого transition+low-motion dev reference, F02 — unknown/crop, F03/F04/F05 — hard negatives, F06 — limb-motion и короткий stable reference. F02 отвергнут как fully visible still-positive. F04 отвергнут как «negative с хорошей полной видимостью всего тела»: низкие фазы частично обрезаны, это отдельная dimension контроля.

Второй dataset не загружался: после полного GMDCSA расширения он не нужен для минимального короткого dev-пакета; для H10/30s нельзя обещать преимущество неполученного clip. URFD из W1 остаётся compact secondary-domain candidate с NC/SA условием, CAUCA — candidate с CC BY, но actual selected AVI в W1 не установлен. Они **не объявлены проверенными этой веткой**. Не расходовать время на большой ZIP ради неустановленного long-tail. Отказ от дополнительного источника — ограниченное решение по текущей полезности, не вывод об отсутствии подходящих сцен во всех этих datasets.

#### Точные оставшиеся Q/E и безопасный следующий шаг

**Q1/E1: длинный H и выход из события.** Снять отдельный цельный take со статичной камерой и разрешением на запись/CV/live/recorded показ. Без реального падения с высоты: на мягком мате участник под контролем спокойно переходит из низкого/сидячего положения в лежачее; явно назвать это безопасной постановкой перехода, не естественным accident. Предыстория5s, settle, затем **H+5s** непрерывной видимой малоподвижной gross-позы (если команда выбирает30s — минимум35s после settle), затем движения рукой/ногой5s, безопасное вставание и ещё5s. Эти числа — design capture budget, не официальные пороги. Быстрый standing-fall не имитировать на твёрдом полу; для него текущий внешний staged clip остаётся отдельным evidence.

**Q2/E2: трудные controls.** Отдельные целые takes: намеренное медленное укладывание; лежит и двигает одной конечностью при стабильном torso; безопасный ремонт/поиск предмета на коленях; стоя→присед→стоя. Та же камера/масштаб, полностью видимые extremities, каждый критический участок≥H+5s. Не объявлять их уже полученными.

**Q3/E3: unknown и rearm.** В отдельной записи закрыть часть тела лёгкой переносной ширмой на2s, затем открыть при сохранении исходной lying позы; после observed recovery выполнить второй безопасный переход. Не имитировать occlusion чёрными кадрами и не считать synthetic edit реальной видимостью. Два участника — отдельная сцена, без опасной техники. Freeze правила unknown/reacquire/rearm заранее.

**Q4/E4: независимость/операционализация.** Второй аннотатор проверяет boundaries и full-resolution motion, команда фиксирует измеримый low-motion критерий/масштаб/visibility и H до blind take. Для настоящего holdout — другая session и желательно другой разрешённый actor/camera/background. Записать actual frame PTS/hashes; clipping и split группировать по исходной записи.

**Итог по K:** K004 **scoped** (короткое наблюдаемое событие добавлено; long-tail/industrial/recovery остаются open); K008 **scoped** (новые media привязаны к существующему grant/notice, release scope и ZIP identity open); K011 **scoped** (поставлены PTS actor×rule reference/censoring/eligibility, executable event lifecycle и hardware run — ответственность дальнейшей интеграции, здесь open). Новых модельных claims нет.

<a id="F018"></a>
## F018 — Падение: дополнительные datasets, exact leads, coarse CSV defects и grouping

**Нормализованный статус и условия:** Бывшие Range-only S1F13/S1A16/S4A05 полностью получены и reviewed F017; более поздняя GT/PTS имеет приоритет. Copyright identity старой пары закрыта F015. URFD/CAUCA/IKAR и gated alternatives сохраняются как резервные источники, не полученные файлы.

**Источники:** [S105](SOURCES.md#S105), [S110](SOURCES.md#S110), [S113](SOURCES.md#S113), [S114](SOURCES.md#S114), [S115](SOURCES.md#S115), [S116](SOURCES.md#S116), [S117](SOURCES.md#S117), [S118](SOURCES.md#S118), [S119](SOURCES.md#S119), [S120](SOURCES.md#S120), [S121](SOURCES.md#S121), [S122](SOURCES.md#S122), [S123](SOURCES.md#S123), [S124](SOURCES.md#S124), [S125](SOURCES.md#S125), [S126](SOURCES.md#S126), [S127](SOURCES.md#S127), [S128](SOURCES.md#S128), [S129](SOURCES.md#S129), [S130](SOURCES.md#S130).

**Происхождение:** [W1-09.md](_WORK/W1-09.md), `## 2.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 2. Первичные источники и версии

Все нижеследующие URL открыты 2026-10-23; там, где endpoint не сработал, это явно указано.

- **W1-09-S01:** [GMDCSA-24, статья авторов](https://pmc.ncbi.nlm.nih.gov/articles/PMC11416611/), *Data Description*, *Experimental Design*, таблицы 2–6, 22, DOI `10.1016/j.dib.2024.110892`. Заявлены 160 постановочных клипов, 81 fall/79 ADL, четыре субъекта, три комнаты; Subjects 2/3 используют одну комнату. Камера ноутбука статична, номинально 720p/30 FPS, есть 640×480. Это описание авторов; точные параметры конкретных MP4 проверены отдельно ниже. Статья содержит неоднозначность: Ethics Statement говорит о трёх актёрах, в основном описании — о четырёх; не исправлять догадкой.
- **W1-09-S02:** [официальный release v2.1](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/releases), GitHub API `/repos/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/commits/v2.1` разрешил exact commit **`5abac7693229900cf80f722e878fbb119211fc1c`**. Recursive tree проверен, MP4 существуют как обычные Git blobs, не только LFS pointers. [Закреплённый корень](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/tree/5abac7693229900cf80f722e878fbb119211fc1c).
- **W1-09-S03:** [Zenodo v2.1, DOI 10.5281/zenodo.13354453](https://zenodo.org/records/13354453), опубликован 21.08.2024; карточка показывает один ZIP **1.1 GB**, MD5 `3d36f2c5c1a666b99639e4e9fd843efb`. Архив не скачан и HEAD архива не выполнен. Оценка 1.95 GB из статьи не совпадает с compressed ZIP и не должна подменять его размер. Для демо полный ZIP не нужен.
- **W1-09-S04:** [закреплённый LICENSE GMDCSA](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/blob/5abac7693229900cf80f722e878fbb119211fc1c/LICENSE): MIT, Copyright 2024 Ekram Alam. Прочитан raw текст. Формулировка стандартного MIT говорит Software; отдельного договора о likeness/public presentation subjects в просмотренных файлах нет. Это сильнее отсутствующей лицензии, но не доказательство безусловного права публичного показа лиц. Получение публично выложенных samples для research выполнено; право использования в публичном конкурсном ролике/его дальнейшего распространения не заявляется установленным. Сохранить notice и авторство, проверить нужный режим демонстрации.
- **W1-09-S05:** временная разметка: [Subject 1/Fall.csv](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/blob/5abac7693229900cf80f722e878fbb119211fc1c/Subject%201/Fall.csv), [Subject 1/ADL.csv](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/blob/5abac7693229900cf80f722e878fbb119211fc1c/Subject%201/ADL.csv), [Subject 3/ADL.csv](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/blob/5abac7693229900cf80f722e878fbb119211fc1c/Subject%203/ADL.csv), [Subject 4/ADL.csv](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/blob/5abac7693229900cf80f722e878fbb119211fc1c/Subject%204/ADL.csv). CSV содержат классы с интервалами в секундах, описание, длительность, освещение и одежду; не frame-level bbox/keypoint ground truth.
- **W1-09-S06:** [URFD official](https://fenix.ur.edu.pl/~mkepski/ds/uf.html), *Fall sequences*, *ADL*, license. Повторно открыт первичный источник: 70 sequences, 30 falls/40 ADL; камеры записываются независимо, синхронизация по ближайшим timestamps. CC BY-NC-SA 4.0 и intended non-commercial academic; commercial use — по обращению к авторам. Exact media HEAD уже в W1-01-F05; не выдавать чужую проверку за собственную загрузку.
- **W1-09-S07:** [CAUCAFall v5](https://data.mendeley.com/datasets/7w7fccy7ky/5), DOI `10.17632/7w7fccy7ky.5`, 18.03.2025; *Description*, *Steps*, *Licence*. Статичная угловая HIKVISION IR, **23 FPS, 1080×960** по карточке; десять субъектных папок, в каждой пять постановочных falls/пять ADL, AVI/PNG/TXT labels; ADL включают прыжки, поднятие предмета, сидение, колени. CC BY 4.0. Прямой конкретный AVI в этой сессии не установлен: Files не раскрыл список, пробный public-api URL не открылся веб-инструментом. Карточка не равна полученному файлу.
- **W1-09-S08:** [Montreal Multiple Cameras Fall Dataset](https://www.iro.umontreal.ca/~labimage/Dataset/) при открытии вернул страницу **Anubis Access Denied, code 9e4edb5b6b850c41**. Первичный binary access не подтверждён; технические цифры из каталогов не принимаются как проверенная спецификация этой ветки.
- **W1-09-S09:** [TsetFall официальный repository](https://github.com/ppgia-unifor/TsetFall_dataset), *Folder structure*, *Video descriptions*, *Download*. Есть human bbox labels NF/FN/FG/C отдельно от AI-assisted extension. Videos RAR расположен в Mega, **ключ расшифровки получается после формы**. Форма не отправлялась; архив не получен. Root GPL-3.0 не доказывает согласия людей на любой показ. Конкретные полезные negatives: seq03 intentional lying on chairs, seq05 sitting on floor, seq15–18 dark exercise. Точных FPS/resolution/размера и пригодного прямого clip здесь не установлено.
- **W1-09-S10:** [HAR-UP official](https://sites.google.com/up.edu.mx/har-up/), *Data*, *Downloads*, *Missing Data*. 17 subjects ×11 activities ×3 trials; камера выдаётся как отдельный **ZIP изображений на trial**, не готовый единый видеоархив; Subject8/activity11/trials2–3 отсутствуют. В текущем прочитанном HTML нет раскрытого прямого Camera ZIP, а лишь встроенный selector. Точный binary и условия demo не установлены. Не превращать общий public available в проверенную загрузку.
- **W1-09-S11:** [SFU IPML реальные падения](https://www.sfu.ca/ipml/research/data-sharing.html), *Databrary Videos of Falls in Long Term Care*. 300 естественных падений 118 пожилых людей, общие пространства двух учреждений; на эпизод XLSX с FPS/resolution и числом видов. Доступ для research/education через Databrary и обращение к владельцу. Это действительно естественные падения, но не открытый немедленный demo channel, не промышленная сцена; контактов не выполняли.
- **W1-09-S12:** [FallDetectionDataset, авторский GitHub](https://github.com/samruddhi-2308/FallDetectionDataset), commit API **`2ea3acbb74db88a4c2d584b3b5a631f180b490f6`**. Checked raw `LICENSE`, `docs/collection_protocol.md`, `docs/ethics_and_privacy.md`, `metadata/label_schema.md`, `annotations/cvat/annotation_manifest.csv`. 54 clips, 48 falls/6 ADL; CC BY-NC 4.0 явно для work, лица различимы. Индекс clip-level, только восемь CVAT XML; mappings помечены `mapped_auto_exact_frame_count`, это не независимая ручная верификация соответствия. Protocol говорит indoor consumer mobile fixed-view, FPS/resolution лишь в future metadata. Полезный резерв, слабее GMDCSA по negatives и длительностям.
- **W1-09-S13:** [IKAR v1.0, AGH](https://agh.rodbuk.pl/dataset.xhtml?persistentId=doi:10.58032/AGH/A1NZPE), DOI `10.58032/AGH/A1NZPE`, 29.09.2026. 278 постановочных falls на матах/7 volunteers, CC BY 4.0, archive 121.4MB MD5 `2667661c258610c0c0aa4bc58a7fc7c2`; negatives в описании не заявлены. `/api/access/datafile/16904` HEAD и README `/16905` GET/HEAD в этой среде закончились TLS handshake timeout; не писать, что архив проверенно скачивается. Карточка помечает public, но binary verification не прошла.

**Происхождение:** [W1-09.md](_WORK/W1-09.md), `## 3.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 3. Рейтинг по пригодности именно к дедлайну

| Место | Набор | Доступность, labels и negatives | Решение |
|---|---|---|---|
| 1 | GMDCSA-24 v2.1 | Exact per-clip URLs; два MP4 полностью декодированы, три дополнительных проверены range+metadata. Temporal seconds CSV; сложные sleep/bend/push-up negatives. Не industrial | Основной независимый smoke/demo pack; reannotate onset/end/visibility для выбранных файлов |
| 2 | URFD | Очень компактные MP4; 30/40 balanced-ish falls/ADL; original timestamp CSV, разные views. W1-01 установил HEAD 200 конкретной пары | Второй домен для cross-dataset проверки; NC/SA ограничение и право показа не решены |
| 3 | CAUCAFall v5 | CC BY, overhead surveillance-подобный ракурс, IR/окклюзии и kneeling negatives. Конкретный AVI не получен | Сильный резерв после binary check, не обещанный готовый clip |
| 4 | State-to-Fall + ADL | Три exact MP4 HEAD200 по 3.6–5.6MB, но NC, лишь 6 ADL, неполные annotations | Дополнительные исходные состояния, не основной validation set |
| 5 | IKAR v1 | 121MB compact archive относительно наборов; CC BY; только положительные классы, binary timeout | Не тратить основное время дедлайна; без negatives недостаточен |
| Отложить | Montreal / TsetFall / UP-Fall / Le2i | Montreal blocked, TsetFall form/key, UP-Fall embedded selector; Le2i authoritative binary/rights не подтверждены | Наличие paper/card/стороннего зеркала не равно готовности |
| Для будущего | SFU Databrary | Естественные инциденты с ограниченным доступом | Не быстрый публичный demo источник |

Le2i official candidate URL `https://imvia.u-bourgogne.fr/en/database/fall-detection-dataset-2/` не открылся веб-инструментом; зеркала Kaggle/HF не исследованы до доказанного разрешения. Особенно не переносить CC BY из карточки производного HF набора из трёх кадров на права полного оригинального видео. SisFall как accelerometer dataset не считать готовым RGB-video источником по неясному mirror «SisFall-processed».

**Происхождение:** [W1-09.md](_WORK/W1-09.md), `## 4.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 4. Пять проверяемых компактных кандидатов

База exact URL **B**:

`https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/`

В URL пробелы кодируются `%20`. Размеры в bytes, длительности ниже фактические video stream/container metadata, а не округлённые CSV. Все пять относятся к S02/S04/S05, поэтому единый issue прав публичного показа сохраняется.

| ID | Exact path после B | Доступ/размер | Что проверено / смысл |
|---|---|---|---|
| W1-09-F01 | `Subject%201/Fall/11.mp4` | HEAD200; полный GET **5,961,144** | **Полный decode181 frames**, 1280×720; video duration6.0974s; avg905000/30487=**29.6848 FPS**. Positive: из стоя в низкую позу, затем ложится/двигается |
| W1-09-F02 | `Subject%203/ADL/08.mp4` | HEAD200; полный GET **5,172,948** | **Полный decode146 frames**, 1280×720; duration4.89617s; avg876000/29377=**29.8192 FPS**. Hard-negative: намеренно укладывается из сидя |
| W1-09-F03 | `Subject%201/Fall/13.mp4` | Range206, full size**1,389,022** | 640×480; video samples128; duration4.3213s; avg**29.6207 FPS**. CSV backward fall, голова не видна; полезен для visibility gating, не легкого positive |
| W1-09-F04 | `Subject%201/ADL/16.mp4` | Range206, full size**3,582,225** | 1280×720; samples104; duration3.52137s; avg**29.5340 FPS**. CSV: из сидя поднимает телефон с пола; низкая голова не должна стать fall alert |
| W1-09-F05 | `Subject%204/ADL/05.mp4` | Range206, full size**7,978,111** | 1280×720; samples220; duration7.36163s; avg**29.8847 FPS**. CSV exercise/push-up view1, walking0–1.9s, exercising2.6–7s; еще не декодирован/визуально не проверен |

Для F03/F04/F05 малый запрос последнего 65536-byte range прочёл MP4 `mdhd`, `tkhd`, `stsz`. FPS вычислен samples/(duration/timescale); это контейнерная средняя частота, не hardware inference FPS и не доказательство полного decode. Для F01/F03/F04 также был GET первого65536-byte range, статус206 и `ftyp`; для F01/F02 полное получение и decode существенно сильнее этих header checks.

#### Реальные локальные артефакты и hashes

Samples находятся в `_WORK/W1-09_samples/`:

- `positive_S1_F11.mp4`: SHA256 **`c25e4fc9b669cb588b6145d2cfd94f2d403083293c08bc85fa863111372bfea7`**.
- `negative_S3_A08.mp4`: SHA256 **`b383bb83a22b286cfc65fdd934137ee8b29e84aef7be0b540271d7c69d10fa8b`**.
- `positive_S1_F11_sheet.jpg` и `negative_S3_A08_sheet.jpg`: контактные листы из восьми кадров, визуально открыты исследователем. Это производные для внутренней проверки, не опубликованы.
- `manifest.json`: воспроизводимые URL/commit/размеры/hashes и реальные decoder timestamps; `SOURCE_LICENSE_MIT.txt`, `SOURCE_Subject1_Fall.csv`, `SOURCE_Subject3_ADL.csv`: точные небольшие source snapshots. Замеренные интервалы соседних PTS: F01 min0.031733s/max0.064s; F02 min0.0316s/max0.048s. Полный повторный decode при формировании manifest также завершился без ошибок.

**W1-09-F06 — собственные визуальные наблюдения F01.** Комната, статичная фронтальная камера, один мужчина; около0–1s стоит, около1.5s уже приседает/опускается, около2s сидит низко, около3s лежит на спине с согнутой ногой, около4–5s на боку/горизонтально. Между кадрами меняется положение ног и тела. CSV относит весь1–6s к `Falling (BW)`, поэтому этот label включает длинную постпереходную фазу. **Нет отдельной авторской GT метки onset неподвижности.** Первый decoded PTS0.03333s, последний6.0974s. Полное декодирование успешно, содержательная проверка выполнена по восьми выбранным кадрам, не по непрерывному просмотру со звуком.

**W1-09-F07 — собственные визуальные наблюдения F02.** Другой человек в другой светлой комнате, сидит внизу, опирается руками, затем контролируемо укладывается на бок примерно между1.2–2s и остаётся низко. Поверхность выглядит как покрытая тканью лежанка/мат; CSV называет floor — не делать метрических/геометрических выводов по изображению. В CSV `Sitting[0 to0.8]; Sleeping[0.8 to4]`; визуальный переход не совпадает с этими грубыми границами кадр-в-кадр. Первый PTS0, последний4.86407s; metadata duration4.89617s, тогда как CSV length4s. Это hard-negative для события падения, хотя отдельный class «лежит» здесь корректен.

**W1-09-F08 — timing caveat.** PyAV сообщил `base_rate=60` обоим файлам, но average_rate около29.7–29.8; MP4 `stts` у F01 содержит неодинаковые sample deltas. Не выбирать60 или ровно30 только по одному полю. Использовать PTS/time_base для скорости позы, low-motion hold, event time и deadline. Диагностика реально декодированного файла отличается от номинальной камеры30FPS в статье.

Дополнительные exact HEAD проверены для S12 base `https://raw.githubusercontent.com/samruddhi-2308/FallDetectionDataset/2ea3acbb74db88a4c2d584b3b5a631f180b490f6/`: `data/standing_to_fall/video_20260216_152051.mp4`200/3,565,031B; `data/adl_no_fall/video_20260216_152523.mp4`200/4,130,035B; `data/sitting_to_fall/video_20260216_152158.mp4`200/5,556,922B. Эти файлы не скачаны/не декодированы; обещать их реальный сюжет по одному label нельзя.

**Происхождение:** [W1-09.md](_WORK/W1-09.md), `## 5.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 5. Labels, splits, negatives и ограничения переноса

**Labels.** GMDCSA не предоставляет в проверенных CSV frame-index onset/offset с отдельными `fall_transition`, `lying`, `stationary`. Классы интервалами могут перекрываться. В CSV найдены синтаксические/семантические дефекты: Subject2/ADL06 `Sitting[9.7 to3]` — обратный интервал; Subject2/ADL04 duration70 при описании exercise0–7; Subject3/ADL04 незакрытые скобки; Subject1/Fall05 лишний `:`. Нельзя парсить строго без validation и принимать каждую строку как точную ground truth. Для пяти demo candidates вручную зафиксировать t0/t1/visibility/движение на оригинальном time axis; human correction хранить отдельно от исходного CSV.

**Splits.** В просмотренном GMDCSA root/tree/статье не найден заданный канонический train/val/test manifest; не утверждать, что его нет во всех исследованиях. Рекомендуемая политика для этой команды: thresholds/dev на Subject1(Room1), final review на Subject4(Room3); Subjects2+3(Room2) держать единым environment group. Разделение по subject без room grouping всё ещё может дать background leakage. Наш F02/Subject3 можно использовать для exploratory hard-negative, тогда его уже нельзя называть нетронутым final holdout. Все соседние crops/frames одного video должны оставаться в одном split. У URFD виды одного падения тоже один group, иначе один эпизод оказывается и в train, и в test.

**Трудные negatives по содержанию CSV:** F02 deliberate lying; F04 bend from chair; F05 push-up; Subject2/ADL09 — садится на пол; Subject3/ADL09 — из лежания на полу встаёт; Subject2/ADL22 — ночные отжимания и сидение; Subject4/ADL10 — walk→bed sleeping; Subject3/ADL13 — сидит на полу ночью. Для последних четырёх video availability не проверена, это exact candidate leads, не готовый demo пакет.

**FP risks:** repair/kneeling/leaning, лежание по работе, сон, упражнения, низкая поза на поверхности, закрытые ноги, край кадра, track-ID switch. **FN risks:** мало предыстории (F03 CSV onset0.4s), медленное сползание, один невидимый person, падение за оборудованием, multi-person interaction, мелкая фигура, пыль/блики, объёмная одежда/PPE, камера движется. В лабораторных данных коврик/кровать и центральная крупная фигура дают shortcuts, не переносимые на завод. Низкое движение всей сцены не означает неподвижность конкретного человека; missing detection не означает person-down.

**Неподвижность:** отсутствие физиологического/медицинского ground truth во всех пяти выбранных файлах. Нельзя считать ADL негативом по всем возможным политикам безопасности: лежание в запретной зоне может быть отдельным операторским событием, но это другой label и другой тест. Сценарий W1-01 должен различать наблюдаемое лежание, подозрение на падение и последующую малоподвижность.

<a id="F019"></a>
## F019 — Бег: translation/gait, калибровка, rolling speed и locked_ids

**Нормализованный статус и условия:** Actual YOLOX graph и preprocessing ambiguity — F014. Generic speed threshold не gait-run. PoseC3D NTU60 не имеет run; HMDB51 имеет run32/walk49.

**Источники:** [S034](SOURCES.md#S034), [S042](SOURCES.md#S042), [S043](SOURCES.md#S043), [S044](SOURCES.md#S044), [S045](SOURCES.md#S045), [S068](SOURCES.md#S068), [S131](SOURCES.md#S131), [S132](SOURCES.md#S132), [S133](SOURCES.md#S133), [S134](SOURCES.md#S134), [S135](SOURCES.md#S135), [S136](SOURCES.md#S136), [S137](SOURCES.md#S137), [S138](SOURCES.md#S138), [S139](SOURCES.md#S139), [S140](SOURCES.md#S140), [S141](SOURCES.md#S141), [S142](SOURCES.md#S142), [S143](SOURCES.md#S143), [S144](SOURCES.md#S144), [S145](SOURCES.md#S145), [S146](SOURCES.md#S146), [S147](SOURCES.md#S147), [S148](SOURCES.md#S148), [S149](SOURCES.md#S149).

**Происхождение:** [W1-02.md](_WORK/W1-02.md), `## Альтернативы`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Альтернативы

| Путь | Наблюдаемый признак | Что честно показывать | Предпосылки | Решение |
|---|---|---|---|---|
| A. Detector + tracker + homography | Скорость footpoint на плоскости пола, зона, длительность | Быстрое перемещение; подозрение на бег | Фиксированная камера, метрические точки на ровном полу, ноги видны, стабильный ID | Основной быстрый кандидат |
| B. Detector + tracker, без метрики | px/s в локальной зоне либо displacement / bbox-height / s | Повышенное перемещение по эвристике данной камеры | Узкий диапазон глубины, контрольные видео, неизменный ракурс | Резерв; не писать м/с и не сравнивать камеры |
| C. Detector + pose + action model | Временная структура суставов | Вероятность run с явным неизвестным классом/качеством | Достаточно видимые конечности, нужный класс weights, crop/track association, экспорт | R&D/резерв, риск на дедлайн |
| D. RGB video/action classifier | Видеоклип целиком или crop человека | Действие clip-level | Подходящие pretrained классы и video preprocessing | Не основной: атрибуция человеку, фон и экспорт усложняют |
| E. Pose-handcrafted gait rule | Колебания коленей/голеностопов, cadence | Подозрение на бег | Полный скелет, частота кадров, проверка негативов | Не называть надёжным классификатором без валидации |

A и B требуют реального нейроинференса детектора на LinQ. То, что последующая логика классическая, не отменяет использования нейросети; окончательную трактовку достаточности именно такой цепочки стоит подтвердить у технического эксперта. Наличие ONNX не означает успешной компиляции LinQ.

**Происхождение:** [W1-02.md](_WORK/W1-02.md), `## Геометрия`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Геометрия, скорость и короткий рывок: инженерный контракт

Ниже предложения W1-02, а не параметры из публикаций и не нормативные пределы скорости.

1. На каждую камеру хранить camera_id, calibration_version, исходный размер кадра, polygon зоны, ground-plane correspondences, единицы, допустимую область калибровки. Одна H на одну плоскость пола; лестница, пандус/настил и разные уровни требуют отдельных поверхностей либо исключения из метрики. Метрический масштаб берётся из измеренных расстояний/плана, не из человеческого роста «по умолчанию».
2. При заметной дисторсии сначала согласованно rectification/undistort; затем калибровка изображения на пол. Homography основана на coplanar points (S01); четыре неколлинеарных соответствия — минимальный конструктивный случай, дополнительные контрольные точки нужны для оценки ошибки. Для каждой новой установки/zoom/resolution/crop пересчитать или корректно преобразовать калибровку.
3. Footpoint p=(bbox center x, bbox bottom y) — приближение контакта с полом. Нельзя без оговорки использовать центр bbox: он находится над плоскостью. Видимые ankle keypoints могут уточнить положение, но прыжки/фаза полёта, тени, спрятанные ноги и частичный bbox остаются источниками ошибки. Если bbox обрезан нижней границей кадра или ноги за станком, метрическую скорость помечать unknown.
4. q_t=dehomogenize(H·[p_x,p_y,1]); v=norm(q_t−q_(t−Δ))/Δt. Здесь q имеет метры только при метрических correspondences. Использовать capture PTS, а не wall-clock inference. Если обработан каждый k-й кадр, Δt включает все пропущенные кадры. Переменный FPS, ускоренное воспроизведение и дропы должны сохранять исходное время.
5. Оценивать скорость в скользящем окне robust regression координат от времени либо несколькими разностями с медианой. Прямое двухкадровое ускорение шумно: дифференцирование усиливает ошибки footpoint и ID switch. Нельзя объявлять «резкий рывок» по одному скачку bbox. Предложение для первого smoke: sustained window 0.6–1.0 s; короткий канал 0.2–0.4 s с более жёсткой проверкой качества/минимального displacement. Это стартовые настройки, не подтверждённые оптимумы.
6. Для рывка хранить rolling скорость до/после начала движения. Большое ускорение должно сопровождаться согласованным направлением, достаточным displacement и непрерывными наблюдениями. Длинное усреднение пропустит рывок; короткое увеличит FP. Отдельно измерить trade-off на 0.3/0.5/1.0 s эпизодах. Если частота инференса слишком мала и рывок попал между кадрами, он не наблюдаем — нельзя восстановить его правилами.
7. Порог скорости задаёт специалист участка как параметр события; универсальный «порог бега» в м/с здесь не установлен. В условиях нехватки геометрии путь B может нормализовать Δpixels на медианную высоту bbox и время. Такая величина не инвариантна к позе/окклюзии/направлению перспективы, не является м/с и требует порогов по зоне/ракурсу.
8. Ошибка скорости растёт при коротком Δt. Если каждая из двух метрических позиций имеет ошибку не более e, грубая верхняя граница ошибки конечной разности — 2e/Δt (собственный вывод из неравенства треугольника). Поэтому в дальней части кадра, где H усиливает шум, нужен quality gate и зона неопределённости вокруг порога. Не выдавать мнимую десятичную точность скорости.

#### Камера движется, кадр меняется, цех плотный

W1-02-F04. BoT-SORT использует camera-motion compensation для association (S05), но это не даёт автоматически метрическую координату пола. Нужно отдельно переводить текущий footpoint в координаты опорного кадра и затем применять H. При вибрации опираться на статический фон, исключать людей/движущиеся станки из оценки warp, отслеживать качество/inlier support. При отказе стабилизации отключать скорость и выдавать camera-quality status. PTZ/zoom/перестановка камеры — инвалидировать старую геометрию. Межкамерная склейка траекторий для MVP не нужна; смена camera_id или сцены сбрасывает state.

ByteTrack помогает не отбрасывать низкоскоринговые реальные bbox, включая частично закрытых людей (S04), но высокий MOT score не гарантирует правильную мгновенную скорость. В плотном цеху ID switch создаёт ложный скачок; association по IoU может терять быстро перемещающегося человека, особенно при редкой обработке. При пересечении людей, merged bbox и неполной траектории измерения приостановить. Track prediction через окклюзию можно использовать для поиска соответствия, но не считать новым подтверждающим наблюдением скорости.

Начало трека не означает начало движения: человек может войти бегущим; ждать контекст предыстории для sustained скорости необязательно, но не называть это обнаружением ускорения. Короткий фрагмент меньше окна и появление за станком дают insufficient evidence, а не normal. При восстановлении ID после пропуска заново накопить наблюдения; разность «до закрытия — после» без явной модели неопределённости может сильно занизить/исказить скорость.

#### Событие, качество, дедупликация

Предлагаемый автомат: unknown → observing → candidate_fast → active → recovery → closed. В candidate переходят лишь реальные наблюдения с достаточным качеством; active после согласованного превышения T_on в окне. Неполные данные переводят в unknown/paused, не подтверждают движение. T_off<T_on и минимальное спокойное время обеспечивают hysteresis. Длительность и пороги подбираются на controls до финального показа.

На входе zone использует footpoint и конфигурацию участка; близость к технике сама по себе ещё не измерена этой веткой. Событие содержит camera_id, zone_id, track/episode ID, начало наблюдения и подтверждения, rule_version, calibration_version, peak/median speed и единицы, quality flags, thumbnail и clip pre/post. Нейронный bbox confidence нельзя называть confidence нарушения.

Одно active episode → одна запись; последующие кадры обновляют evidence, не создают алерт. Закрытие только после recovery/выхода. Для ID fragment короткое пространственно-временное связывание допустимо при однозначном соответствии; при толпе не склеивать разных людей ради удаления дублей. Camera cut закрывает/сбрасывает episode. Измерять отдельно false duplicates и ошибочное объединение двух событий.

**Происхождение:** [W1-02.md](_WORK/W1-02.md), `## Реестр открытых`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Реестр открытых первичных источников

Все обращения 2026-10-23. Source IDs локальные W1-02-Sxx. Commit SHA получены из GitHub API /repos/{repo}/commits/main в этой сессии; URL с main в поиске не считался immutable версией. Веса HEAD доступны — содержимое/хеш не проверены.

**W1-02-S01 — OpenCV geometry, документация 4.13.0.** https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html ; локаторы Basic theory / What is the homography matrix? и Demo 2. Описывает projective plane-to-plane mapping 3×3, 8 DoF, perspective correction. Сильное основание геометрической модели, не готовый алгоритм промышленного бега.

**W1-02-S02 — OpenCV calibration, документация 4.13.0.** https://docs.opencv.org/4.13.0/dc/dbb/tutorial_py_calibration.html ; локаторы Basics, camera matrix, real-world square size. Различает intrinsic/extrinsic, radial/tangential distortion; метрическая единица возникает из известного размера калибровочного объекта. Источник не доказывает точность данной камеры, но запрещает подменять произвольный масштаб метрами.

**W1-02-S03 — Ultralytics exact speed code.** Commit `5d4baa9ee71833da96863f8cefea764838f76705`: https://raw.githubusercontent.com/ultralytics/ultralytics/5d4baa9ee71833da96863f8cefea764838f76705/ultralytics/solutions/speed_estimation.py ; process, строки 86–101. Использует fps, scalar meter_per_pixel, первое max_hist окно; locked_ids запрещает дальнейшие расчёты, результат переводится в целые km/h и ограничивается max_speed. Это прямое доказательство F02. Header указывает AGPL-3.0; лицензия решения/весов отдельно не анализировалась. Официальный guide https://docs.ultralytics.com/guides/speed-estimation тоже открыт, но динамическая документация отличается от pin-кода; код приоритетнее.

**W1-02-S04 — ByteTrack, первичная публикация v3, 2022-04-07.** https://arxiv.org/abs/2110.06864v3 ; abstract. Метод ассоциирует также низкоскоринговые detections для восстановления треков, что полезно при окклюзиях. Указанные авторами MOT17 и V100 результаты — результаты MOT, не бег, не цех, не LinQ. Открыт оригинальный репозиторий, redirect: https://github.com/FoundationVision/ByteTrack ; MIT отмечен GitHub, точные его tracker files/commit в этой ветке не зафиксированы. Дальнейшая реализация должна закрепить выбранную версию.

**W1-02-S05 — BoT-SORT, первичная публикация v2, 2022-07-07.** https://arxiv.org/abs/2206.14651v2 ; abstract. Авторы объединяют motion, appearance и camera-motion compensation для identity tracking. Открыт оригинальный repo https://github.com/NirAharon/BoT-SORT (MIT отмечен GitHub). Exact implementation commit `251985436d6712aaf682aaaf5f71edb4987224bd`, файл https://raw.githubusercontent.com/NirAharon/BoT-SORT/251985436d6712aaf682aaaf5f71edb4987224bd/tracker/gmc.py ; GMC.__init__, apply, applyEcc, applyFeaures. В коде есть sparseOptFlow, orb/sift, ecc; ECC при exception оставляет identity и пишет warning. Такой fallback нельзя принимать за доказанно неподвижную камеру.

**W1-02-S06 — YOLOX official ONNX artifact listing.** Repo SHA `6ddff4824372906469a7fae2dc3206c7aa4bbaee`; открыт https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/main/demo/ONNXRuntime/README.md ; Step2, таблица nano и Step3. Nano: 416×416, ссылка на заранее экспортированный ONNX. Exact asset https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_nano.onnx ; HTTP HEAD 200, Content-Length 3659407 bytes. Это публичный экспортированный detector, не action weights. Параметры accuracy из таблицы — заявленные авторами, не наши. Реальный граф/входы не инспектировались.

**W1-02-S07 — YOLOX I/O и preprocessing, exact code на S06 SHA.** `demo/ONNXRuntime/onnx_inference.py`: https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/demo/ONNXRuntime/onnx_inference.py , main: читает OpenCV image, делает CHW batch, decode, objectness×class, xywh→xyxy, обратный scale и CPU NMS. `yolox/data/data_augment.py`, preproc: https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/data/data_augment.py ; сохраняет BGR, resize с сохранением пропорций, padding 114 справа/снизу, float32 CHW; этот путь не делит на 255 и не делает ImageNet normalization. Не путать с legacy=True.

**W1-02-S08 — YOLOX export, decoder, class mapping, code rights.** На S06 SHA открыты `tools/export_onnx.py`: https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/tools/export_onnx.py (default opset11, batch1, names images/output, decode_in_inference выключен default); `yolox/utils/demo_utils.py`: https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/utils/demo_utils.py (strides 8/16/32, grid decode и exp wh); `yolox/data/datasets/coco_classes.py`: https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/yolox/data/datasets/coco_classes.py (zero-based person=0). LICENSE: https://raw.githubusercontent.com/Megvii-BaseDetection/YOLOX/6ddff4824372906469a7fae2dc3206c7aa4bbaee/LICENSE — Apache-2.0 для repo code. Отдельный grant на release weights и права COCO images этим не установлены.

**W1-02-S09 — MMAction2 PoseC3D exact model zoo.** SHA `a5a167dff2399e2d182a60332325f9c0d4663517`; https://raw.githubusercontent.com/open-mmlab/mmaction2/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/README.md ; HMDB51 row. SlowOnly-R50, uniform48, keypoint heatmaps; заявлены 69.6 top1, 10 clips, 14.6G FLOPs и 3.0M params. Это общая HMDB51 accuracy, не бинарная run-vs-walk и не цех. Точный checkpoint: https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint_20220815-17eaa484.pth ; HEAD 200, Content-Length 12276729 bytes. SHA256 содержимого неизвестен.

**W1-02-S10 — PoseC3D HMDB config.** https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint.py ; открыт main-вариант этого файла; затем HTTP GET pinned файла и bytewise сравнение с main подтвердили идентичность (4248 bytes). Model: Recognizer3D, ResNet3dSlowOnly in_channels17, I3DHead num_classes51. Validation: uniform48, PoseCompact, resize short-side56, center-crop56, Gaussian GeneratePoseTarget sigma0.6/use_score, NCTHW_Heatmap. Test: 10 clips и double flip. Нельзя подставить сырые 17×2 координаты вместо heatmap tensor; число секунд не равно 48 без выбранного sampling. Сокращение test views меняет протокол.

**W1-02-S11 — Точные label maps.** Открыты https://raw.githubusercontent.com/open-mmlab/mmaction2/main/tools/data/hmdb51/label_map.txt (51 строка, zero-based run=32, walk=49, fall_floor=12, smoke=40) и https://raw.githubusercontent.com/open-mmlab/mmaction2/main/tools/data/skeleton/label_map_ntu60.txt (60 строк; run отсутствует, walking towards/apart — interaction classes). Дополнительный HTTP GET pinned путей на S09 SHA подтвердил bytewise идентичность с main (HMDB 377 bytes, NTU60 1143 bytes). Для воспроизводимости использовать S09 SHA; не смешивать порядок классов разных datasets.

**W1-02-S12 — MMAction2 demo и лицензия кода.** https://raw.githubusercontent.com/open-mmlab/mmaction2/a5a167dff2399e2d182a60332325f9c0d4663517/demo/demo_skeleton.py ; main и parse_args. Демо выполняет detection→pose→inference_skeleton и выдаёт один action_label на видео, не готовый track-wise online event detector. Default pose HRNet checkpoint: https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w32_coco_256x192-c78dce93_20200708.pth (наличие ссылки в коде проверено, HTTP/права/экспорт не проверены). Открыт https://raw.githubusercontent.com/open-mmlab/mmaction2/main/LICENSE — Apache-2.0. Отдельные права action/pose weights, HMDB source footage и Kinetics pretraining data не установлены.

#### Неудачные проверки / ограничение поиска

GitHub tree YOLOX/ONNXRuntime не открылся в web, но raw README и source files открылись. Старая страница HMDB Serre Lab перенаправила на главную; старый PDF HMDB был недоступен через web. Поэтому эта ветка **не установила права на публичный показ HMDB video** и не рекомендует скачать любой found clip как лицензионно чистый demo. Во время HTTP проверки один ошибочно набранный checkpoint URL с суффиксом 97d6b56f вернул 404; он отвергнут. Рабочая ссылка 17eaa484 извлечена из открытого README и HEAD-проверена. Никакой подмены 404 выдуманным артефактом нет.

**Происхождение:** [W1-02.md](_WORK/W1-02.md), `## Артефакты`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Артефакты и уровни готовности

#### A. Быстрый путь с YOLOX-Nano

Цепочка: staged footage → OpenCV decode/PTS → S07 preprocessing 416×416 → S06 ONNX detector на LinQ → S08 CPU decode/NMS/class0 → CPU tracker → q_t/H → rolling speed + zone gate → episode → web журнал.

Ожидаемый input по source-contract float32 [1,3,416,416]. Ожидаемый raw output для обычной трёхуровневой COCO head: [1,3549,85], где 3549=52²+26²+13², 85=4+1+80; это **выведенная ожидаемая форма, не измеренный graph metadata release asset**. Перед интеграцией прочитать actual graph и проверить decode flag. Postprocessing/NMS оставить CPU для минимизации требований компилятора. Person-only filtering не превращает исходные weights в обученный person-only detector.

Уровни: family named — да; exact public release — да/HEAD; exported — заявлен ONNX artifact; exported ourselves — нет; compiled LinQ — нет; inference LinQ — нет; end-to-end measured — нет. При плохом recall дальних людей nano заменить на более крупный проверенный detector общекомандного стека, не утверждать, что nano достаточно по одной COCO таблице.

#### C. Pose/action резерв

Цепочка: person→track crops→17 COCO joints/score в каждой временной позиции→PoseC3D heatmaps→51 logits/probs→run32 against walk49→temporal event. Нужны unknown/low-quality и per-person attribution. Не брать demo_skeleton.py как готовый online multi-person event pipeline. Pose estimator costs масштабируются с количеством людей; 3D convolution action model требует отдельной поддержки операций. Поддержка YOLO LinQ не доказывает поддержку PoseC3D. Экспорт/compile не выполнены; не объявлять эту ветку готовой за 1–2 дня.

<a id="F020"></a>
## F020 — Бег: CHAD route и реальные matched Weizmann samples

**Нормализованный статус и условия:** Encoded25FPS против page50FPS: PTS для replay известны, физическое capture time не установлено. Public demo права Weizmann не установлены; собственный continuous target pack ещё предложен, не записан.

**Источники:** [S150](SOURCES.md#S150), [S151](SOURCES.md#S151), [S152](SOURCES.md#S152), [S153](SOURCES.md#S153), [S154](SOURCES.md#S154), [S155](SOURCES.md#S155), [S156](SOURCES.md#S156), [S157](SOURCES.md#S157).

**Происхождение:** [W2-05.md](_WORK/W2-05.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Дата доступа/выполнения 23.10.2026. K006/K001. Прочитаны W1-02 (метод, exact-code finding, staged pack), адресный W1-10-S09 и W1-15-F06–08. Это исследование данных и декодирование, **не inference, tracking test, speed measurement или LinQ benchmark**. Общие итоговые файлы не изменялись.

#### Решение

**W2-05-F01. K006 = scoped, не closed.** Получена настоящая малая walk/run-пара одного именованного участника Weizmann: полные bytes, CRC, SHA256, decoded PTS и визуальный просмотр. Она даёт узкий gait-контраст. Fast-walk, standing/walking→fast в том же непрерывном track, короткий рывок, camera motion и метрические точки пола не покрыты. Разрешение внешнего распространения видео не установлено.

**W2-05-F02. K001 = scoped только для ветви движения.** Отличающая от occupancy переменная — `v_floor(t)` и её изменение в истории одного человека, либо отдельно gait sequence. Это самостоятельный temporal-кандидат исходного сценария №1 при реальном detector inference на LinQ и проверках ниже. Текущее название: **«кандидат: быстрое перемещение человека на калиброванном участке»**. Общий shortlist K001 эта ветвь не закрывает.

Вопрос решения: есть ли continuous positive/negative episodes с понятным временем и правами, отличающие скорость от gait и входа в зону? Узкий gait sample теперь есть; полный operational pack нужно записать. CHAD в текущих ограничениях не дал компактного клипа с адресным run-интервалом.

#### W2-05-S01 — первичный CHAD release и отрицательный результат

[Repository](https://github.com/TeCSAR-UNCC/CHAD), pinned commit `f8a28c13cb5ee27d3283bf6cddb634a0401d76b0`, commit date **2023-06-25T00:59:07Z**. [Immutable README](https://raw.githubusercontent.com/TeCSAR-UNCC/CHAD/f8a28c13cb5ee27d3283bf6cddb634a0401d76b0/README.md), локаторы Structure of Videos / Annotations / Anomaly Labels / Splits. Publication citation — 2023; это отдельно от даты доступа.

Release описывает четыре камеры; имя `<camera>_<video>_<abnormal_present>.mp4`; person-ID/bbox/pose в `.pkl`; бинарный frame array в `.npy`. Running входит в anomaly ontology, но `1` не сообщает action type или виновного person ID. Abnormal interval нельзя автоматически назвать run interval. README предлагает normal-only и mixed splits. Cross-view одновременность не создаёт floor calibration или gait GT.

[Основной video ZIP](https://drive.google.com/file/d/13am4hfhicErcozAYgkmQm02_K-cCmtkQ/view?usp=sharing), [mirror](https://drive.google.com/file/d/1G_gJmWcOKUDrMUC64A_dqrA1NTZvEyEA/view?usp=sharing), [metadata ZIP](https://drive.google.com/file/d/1g01Ay86cuPmKGsrfxddxwA1uG_7bFFmu/view?usp=sharing) открыты. Web viewer показывает sign-in link — это не доказательство обязательной авторизации download. Собственный bounded GET основной страницы дал HTTP200/84 209 bytes HTML. В `itemJson` около архива есть поле `87967801766`; вероятное значение размера, не проверенный полный размер ZIP. Архив не скачивался. Git tree содержит README/LICENSE и две картинки; отдельных MP4 нет.

**W2-05-F03 [SOURCE/NEGATIVE].** Exact CHAD running filename, actor-specific run interval и source PTS не установлены. Pickle/чужой код не запускались. Apache-2.0 repository LICENSE прочитан; отдельные video rights/actor consent для нашего показа не установлены. Это отрицательный результат текущего маршрута, не утверждение о принципиальной недоступности CHAD.

Сохранены `evidence/W2-05/chad_readme.md`, `chad_LICENSE.txt`, `chad_tree.json`, `chad_drive_page.html`. W1-10-S09 уточнён до release schema/access boundary. При последующем получении отдельного MP4 потребуются decoded PTS и ручная actor/gait-разметка; бинарный anomaly label не run GT.

#### W2-05-S02 — первичный Weizmann и фактически полученная пара

[Авторская страница Actions as Space-Time Shapes](https://www.wisdom.weizmann.ac.il/~vision/SpaceTimeActions.html), локаторы Action Recognition / Classification Database / footer. Публикации ICCV2005/PAMI2007; страница сообщает last updated **24 Dec 2007**. Это не дата capture и не immutable revision. На открытой странице явной лицензии видео/consent для нашего внешнего demo не найдено; доступность bytes не заменяет разрешение публичного показа.

Exact URLs: [walk.zip](https://www.wisdom.weizmann.ac.il/~vision/VideoAnalysis/Demos/SpaceTimeActions/DB/walk.zip), [run.zip](https://www.wisdom.weizmann.ac.il/~vision/VideoAnalysis/Demos/SpaceTimeActions/DB/run.zip).

**W2-05-F04 [ACTUAL BYTES].** Полные архивы не скачивались. HEAD: 51 996 002 / 30 591 544 bytes. Реальный HTTP206: tail65 536 bytes каждого ZIP; собственный bounded parser читает central directory/local header и только compressed member, отказывается читать HTTP200 или размеры вне бюджета. DEFLATE/CRC проверены стандартной библиотекой. Всего около7.45MB сетевых member/tail/header bytes. Полные AVI SHA известны, ZIP whole-file SHA неизвестны.

| Файл | Compressed data range включительно | Полный AVI bytes | SHA256 |
|---|---|---:|---|
| `daria_walk.avi` | walk.zip `7008514–11882712` | 6 536 192 | `009fce023da7e907f6de97bc561e9cd7fb74117fa8f7aa11c8c00a30ec6d18dd` |
| `daria_run.avi` | run.zip `16051121–18493208` | 3 269 120 | `e9958bccbdca9e34eb96a59e236e7e1bb6b7e06f4eac187326913a4a4bb44822` |

HEAD Last-Modified: walk2005-12-01 09:37:29GMT; run2005-12-01 09:38:32GMT. Это HTTP metadata, не capture date. Headers/ranges/member CRC/размеры/SHA: `range_manifest.json`; собственный воспроизводимый parser `fetch_members.py`. Не исполняет код источника и не извлекает произвольные paths.

#### Время и собственная визуальная аннотация

Уже установленный `imageio_ffmpeg` executable `ffmpeg-win-x86_64-v7.1.exe` полностью декодировал оба AVI в null output с showinfo, exit0. Новые зависимости не ставились. PNG каждого пятого кадра собраны в просмотренные contact sheets. Логи сохранены. Быстродействие NN/декодера не измерялось.

**W2-05-F05 [OBSERVED ENCODED TIMELINE].** Страница описывает50fps, но полученные AVI имеют rawvideo bgr24,180×144, **25fps, time_base1/25**. Walk84 frames, PTS0…83, last PTS3.32s, duration3.36s. Run42 frames, PTS0…41, last PTS1.64s, duration1.68s. Embedded title содержит `subsampled`, но причина расхождения не доказана. Использовать decoded media PTS для воспроизведения именно этих bytes; подмена50fps вдвое изменяет временную шкалу. **Capture clock/первичная частота записи неизвестны: нельзя выбирать физическое время съёмки и переносить replay speed в м/с.** Это ограниченное расхождение source claim/encoded stream, не доказательство ошибочной первичной записи.

**W2-05-F06 [OUR VISUAL REVIEW].** Contact sheets действительно просмотрены: один человек в похожей одежде, тот же фон/ракурс, справа налево, торс и ноги различимы. В run иной рисунок ног/рук и более быстрое прохождение изображения. Это соответствует source action names; не экспертная разметка каждой фазы полёта и не оценка accuracy. `daria` — source actor match, общего tracker ID между файлами нет. Фон визуально неподвижен; instrumented camera-motion measurement не выполнен.

| Review annotation, 0-based | PTS, полуоткрытый интервал | Значение |
|---|---|---|
| walk frames5…75 | [0.20,3.04)s | Ordinary-walk negative для gait-run; достаточно внутри кадра на просмотренных samples; не специальный fast-walk |
| run frames5…35 | [0.20,1.44)s | Positive candidate для gait-run; не calibrated-speed positive |
| edges вне интервалов | Исключены из quality interval | Вход/выход/обрезание; не normal только из-за отсутствия полного тела |

`review_intervals.csv` — ограниченная наша review annotation, не авторский temporal GT. `decoded_pts.csv` содержит126 decoded timestamps. Действия уже идут в начале файла; onset left-censored, onset-to-alert по ним не измерить. Конец файла не физический конец действия. **Склеить walk+run и назвать естественным same-track transition нельзя.**

[Walk contact](_WORK/evidence/W2-05/walk_contact.jpg), [run contact](_WORK/evidence/W2-05/run_contact.jpg). Исходные AVI и производные PNG сохранены для исследовательской проверки; внешнее распространение по явным условиям не установлено.

#### Раздельные цели и controls

| Функция | Positive | Negative/различающий случай | Статус |
|---|---|---|---|
| Translation speed | Footpoint displacement по измеренному полу/реальному capture Δt выше локального T | Стояние/обычный проход нижеT; камера→unknown | Floor/capture provenance нет, м/с не измерены |
| Gait-run | Временной рисунок одного человека с run label | Ordinary walk; нужны fast-walk/high-knee walk | Узкая matched пара есть; gait NN не запускалась |
| Резкий переход | Рост скорости после наблюдаемого baseline того же ID | Bbox jitter, ID switch, camera motion | Continuous transition отсутствует |
| Короткий рывок | Ручные начало/конец краткого движения | Взмах/наклон, фоновое движение | Требует capture; короткий run clip не «рывок» |

Быстрый шаг может быть positive для translation rule и negative для gait-run. Бег на месте — наоборот. Общего бинарного «опасного бега» на обе routes нет. Зона лишь ограничивает место; решающее отличие — история `q(t),Δt` или gait sequence.

Поступательная route требует измеренных correspondences, fixed reference, видимого footpoint и непрерывного track. Человеческий рост/неизмеренная плитка не эталоны метров. Gait route требует actual runtime action/pose признаков: bbox этого не гарантирует. HMDB/PoseC3D accuracy и W1 class mapping не заменяют local controls и LinQ export/run. Новая пара — будущий узкий input smoke.

#### Собственный capture route — предложен, НЕ выполнен

**W2-05-F07 [PROPOSED].** Безопасный свободный коридор без работающей техники; согласие участников/владельца отдельно на анализ и public demo, отсутствие посторонних, владелец исходников и условия хранения. Consent здесь не получен.

1. Одна камера/штатив без pan/zoom. Стартовый выбранный профиль1080p50/60 с различимыми ногами — не доказанный minimum. Сохранить native файл без пересохранения, orientation/crop, actual PTS/gaps. Статический фон и calibration view до/после. Невидимость ног→unknown, не normal.
2. Запланировать ровный прямоугольник6×2m. После реального промера записать реальные координаты/погрешность рулетки/фото; `(0,0),(6,0),(6,2),(0,2)` допустимы только если измерения совпали. Добавить независимые check points на1/3/5m по обеим длинным сторонам, измерить диагонали. **Здесь ничего не измерено.** Углы дают H correspondences, дополнительные точки — withheld проверку, а не повтор fit на тех же четырёх точках.
3. Два участника отдельно, обе стороны движения и две глубины. Первый dev, второй holdout после freeze параметров. Соседние окна одного прохода не делить между dev/test.
4. Непрерывный master:3s покоя→обычная ходьба→быстрый шаг→ходьба→лёгкий бег→остановка. Повтор в обратную сторону/глубину. Без cut внутри перехода и универсальной предписанной скорости. Если безопасный бег невозможен, сократить scope.
5. Отдельные непрерывные standing→run и walking→run; добровольные рывки target0.3/0.5/1.0s с baseline до/после. Фактическую длительность разметить по кадрам, не по команде участнику; это случаи эксперимента, не требования модели.
6. Negatives: fast-walk; run-in-place; стояние+руки/наклон; ходьба со скрытыми ногами; пересечение двух людей; движение вне зоны. Отдельно **неподвижный человек + небольшое намеренное движение камеры**, возврат fixed view. Pan/zoom инвалидирует старую H; не заявлять скорость до повторной калибровки.
7. `capture_manifest`: camera/actor pseudonym/consent_ref/source SHA/settings/actual PTS/calibration_id. `episodes.csv`: actor/action/onset/end PTS/censoring/visibility/zone/continuous trajectory/uncertainty. Gait и translation labels раздельно. Onset — наблюдаемое изменение, не audio instruction. Для измеренных floor marks записать crossing PTS; `distance/Δcapture_time` — independent segment-average speed, не instant gait GT. Если capture-time provenance не установлен, сохранять только media-time estimate с этим ограничением.

Минимальное покрытие: normal/fast-walk/run в одной геометрии; два same-track transitions; реальный burst; stationary-person/camera-motion negative; known-distance crossing; раздельные dev/holdout episodes. Это coverage pack, не статистически достаточная валидация. До записи сценарий остаётся условным.

#### Следующий эксперимент и критерий допуска

**W2-05-F08 [NOT_RUN].** После LinQ доступа подтвердить neural detector forward/output features; связать source PTS с bbox; проверить обновление rolling speed до/после transition. Неподвижность в первом окне не должна навсегда фиксировать скорость ID — regression против W1-02 locked_ids. Prediction/gap не новое измерение; ID switch→unknown до накопления. Ручной actor label независим от tracker ID.

T_on/T_off, minimum observed displacement/длительность/quality gates выбрать по локальной политике на dev, затем freeze. Универсального running threshold нет. Camera motion/плохаяH/невидимый footpoint→invalid/unknown; отсутствие данных не подтверждает событие. Holdout: source-time sampling10/5/2/1FPS, четыре фазы и burst gap по W1-15-F06–08. Synthetic coverage не model recall. Раздельно TP/FN/FP/unknown, duplicates, ID switches, burst misses, своевременность от ручного onset. Сначала full-rate correctness, затем paced replay/LinQ latency.

Один подтверждённый episode→один event_id→одно уведомление→обновления той же journal record. Наблюдаемый recovery закрывает; gap сам не закрывает/не создаёт повтор. Поля: source onset/confirmation, rule/calibration/model version, speed и единицы только при обоснованной метрике, quality/proof_ref. Bbox confidence не confidence нарушения.

Допуск: LinQ proof; права на показ; measured floor и время; fast-walk policy; same-track transition; camera negative; явно оценённый burst; отсутствие дублей. Сейчас допустимо только: «получены и просмотрены исследовательские samples, подготовлен контракт». Behavioral/device test не выполнен.

#### Сравнение с W1; точные Q/E

| Gap | W1 | W2 | Итог |
|---|---|---|---|
| CHAD | Общая зацепка | Immutable schema, exact archive URLs, bounded metadata | Scoped negative, не run test |
| Walk/run bytes | План/HMDB | Полные matched AVI/SHA/PTS/review | Узкий sample gap закрыт |
| Время | Требование PTS | Page50fps vs encoded25fps | Replay timeline известен, physical capture time неизвестен |
| Fast-walk/transition/burst/camera | План | Точные незакрытые controls/capture route | Open |
| Метры/порог | Метод | Planned measured/check-point route | Open, измерения не выполнены |
| K001 | Риск подмены зоной | Temporal variable и разные цели | Scoped для№1, общий shortlist open |

Q1: принимает ли эксперт локально ограниченную translation speed за исходный№1 либо требует gait-run? Q2: какое правило участка и отношение к fast-walk? Q3: какие исходники разрешены для public demo? Вопросы подготовлены, никому не отправлены.

E1: записать continuous pack и реально измерить floor/time. E2: закрепить actual LinQ model/output/preprocessing/execution proof. E3: holdout controls, sampling/phase, dedup и onset latency. Ближайший шаг — безопасная собственная запись с промерами/правами; дополнительный обзор speed estimation блокер не снимает.

<a id="F021"></a>
## F021 — Moving machine: detection artifacts, geometry/TTC и rejected turnkey projects

**Нормализованный статус и условия:** Actual checkpoint names0forklift1person и full SHA закрыты F022; exact exported graph всё ещё отсутствует. Generic polygon учитывается только как одна infrastructure fallback, не второй сценарий.

**Источники:** [S131](SOURCES.md#S131), [S135](SOURCES.md#S135), [S158](SOURCES.md#S158), [S159](SOURCES.md#S159), [S160](SOURCES.md#S160), [S161](SOURCES.md#S161), [S162](SOURCES.md#S162), [S163](SOURCES.md#S163), [S164](SOURCES.md#S164), [S165](SOURCES.md#S165), [S166](SOURCES.md#S166), [S167](SOURCES.md#S167), [S168](SOURCES.md#S168), [S169](SOURCES.md#S169), [S170](SOURCES.md#S170), [S171](SOURCES.md#S171), [S172](SOURCES.md#S172), [S173](SOURCES.md#S173), [S174](SOURCES.md#S174), [S175](SOURCES.md#S175), [S176](SOURCES.md#S176), [S177](SOURCES.md#S177), [S178](SOURCES.md#S178), [S179](SOURCES.md#S179), [S180](SOURCES.md#S180), [S181](SOURCES.md#S181), [S182](SOURCES.md#S182), [S183](SOURCES.md#S183), [S184](SOURCES.md#S184), [S185](SOURCES.md#S185), [S186](SOURCES.md#S186), [S187](SOURCES.md#S187), [S188](SOURCES.md#S188), [S189](SOURCES.md#S189), [S190](SOURCES.md#S190).

**Происхождение:** [W1-03.md](_WORK/W1-03.md), `## Реестр первичных`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Реестр первичных источников и проверенных артефактов

#### W1-03-S01 — точные веса forklift/person

- Model card: https://huggingface.co/keremberke/yolov8n-forklift-detection ; локаторы Supported Labels, How to use, Evaluation results.
- Metadata: https://huggingface.co/api/models/keremberke/yolov8n-forklift-detection ; дерево: https://huggingface.co/api/models/keremberke/yolov8n-forklift-detection/tree/d8b594f321dd4c64eda16e435601fd266089fc32 . Получены прямым HTTP GET.
- Зафиксированная revision: `d8b594f321dd4c64eda16e435601fd266089fc32`.
- Файл `best.pt`, размер 6,216,376 байт; LFS SHA256 `0dc3816283226f0f7ac5410620394c8ddeef32c5200b371194ac4df4a1ee7d38`. URL: https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/d8b594f321dd4c64eda16e435601fd266089fc32/best.pt . HEAD вернул 200 и content-length 6216376. Это проверка доступности, не скачивание/загрузка модели.
- Config: https://huggingface.co/keremberke/yolov8n-forklift-detection/raw/d8b594f321dd4c64eda16e435601fd266089fc32/config.json ; input_size=640, task=object-detection, model_type=v8, ultralytics=8.0.21, ultralyticsplus=0.0.23.
- Card заявляет ordered labels `['forklift', 'person']`, mAP50=0.83794 на validation, self-reported/unverified. Это не полнота события сближения. Числовое соответствие 0=forklift/1=person ожидается по порядку; **перед использованием проверить model.names**, сам checkpoint не десериализован.
- В model card/metadata нет явной лицензии весов. Не наследовать CC BY автоматически с датасета.

#### W1-03-S02 — данные детектора

https://huggingface.co/datasets/keremberke/forklift-object-detection/raw/2c0f4e8e9085f3079b80137e780aab0e54936cfc/README.md ; API https://huggingface.co/api/datasets/keremberke/forklift-object-detection . Revision `2c0f4e8e9085f3079b80137e780aab0e54936cfc`. Card: 421 изображение, train295/valid84/test42, forklift/person, CC BY 4.0; происхождение Roboflow, auto-orientation, без augmentation. Исходный указанный проект: https://universe.roboflow.com/mohamed-traore-2ekkp/forklift-dsitv/dataset/1 . Это bbox-датасет; он не задаёт движение, безопасную дистанцию, события/временные интервалы, ground-truth TTC. На нём нельзя доказать near-miss recall. Права видео не следуют из прав этого набора.

#### W1-03-S03 — версия кода, I/O и экспорт для S01

Прямо открыты исходники тега `v8.0.21`:

- https://raw.githubusercontent.com/ultralytics/ultralytics/v8.0.21/ultralytics/yolo/data/dataloaders/stream_loaders.py — LoadImages, строки 227–236: чтение BGR, LetterBox, HWC→CHW, BGR→RGB.
- https://raw.githubusercontent.com/ultralytics/ultralytics/v8.0.21/ultralytics/yolo/v8/detect/predict.py — DetectionPredictor.preprocess/postprocess: float/half, /255, NMS, scale_boxes к исходному кадру.
- https://raw.githubusercontent.com/ultralytics/ultralytics/v8.0.21/ultralytics/nn/modules.py — Detect, строки 388–412: decoded xywh и sigmoid классов.
- https://raw.githubusercontent.com/ultralytics/ultralytics/v8.0.21/ultralytics/yolo/engine/exporter.py — строки161,267–305: BCHW zeros input, ONNX exporter, имена `images`/`output0`, opset параметром, checker; для detection отдельный NMS в predictor.
- https://raw.githubusercontent.com/ultralytics/ultralytics/v8.0.21/LICENSE — GPL-3.0 для этого тега. Не подменять современной лицензией текущего main.

Инженерное ожидание для стандартного двухклассового YOLOv8n при фиксированном 640: input `[1,3,640,640]` float32 RGB [0,1]; decoded output `[1,6,8400]` (xywh+2 class scores), затем внешние score threshold/NMS/обратный letterbox. **Это выведено из архитектуры, не измеренная форма экспорта данного best.pt.** Проверить через загрузку/export и actual ONNX graph. Нет отдельного objectness канала в этой ожидаемой форме. При resize без сохранения пропорций или ошибочном undo padding геометрия событий сломается. Не смешивать координаты network input и original frame.

#### W1-03-S04 — tracking как первичный метод

https://arxiv.org/abs/2110.06864v3 — ByteTrack, v3 от 2022-04-07; abstract/method: ассоциация низкоуверенных детекций с треками помогает против фрагментации. Открыт abstract. Публикационные 30 FPS/V100 и MOT-метрики относятся к их эксперименту, не LinQ/нашему складу. https://github.com/ifzhang/ByteTrack ; https://raw.githubusercontent.com/ifzhang/ByteTrack/main/LICENSE — MIT (main не pinned). Для MVP достаточно tracking-by-detection; отдельная ReID сеть необязательна, но ID-switch критичен для скорости и дедупликации. Проверять классы отдельно, не сшивать person с forklift. Движущаяся камера требует компенсации глобального движения либо отклонения такой камеры.

#### W1-03-S05 — рабочий открытый шаблон homography + tracking + speed

https://github.com/roboflow/supervision/blob/594bd0f9802872efcd50cc14564548a85e51dc19/examples/speed_estimation/inference_example.py . SHA установлен через GitHub commits API для этого файла; дата commit 2026-10-06. Файл открыт первоначально на develop, затем ревизия зафиксирована API. Локаторы: `ViewTransformer`, `SOURCE/TARGET`, `BOTTOM_CENTER`, `coordinates`, speed calculation. Он использует perspective transform, anchor внизу bbox, историю идентификатора и время для оценки скорости. Скорость в примере одномерная по Y; перенос на произвольное движение цеха требует полного XY-вектора и реальных единиц TARGET.

README: https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/examples/speed_estimation/README.md — явно требует индивидуальных SOURCE/TARGET для каждой камеры, имеет Ultralytics вариант и vehicles.mp4 downloader. Это дорожный пример, не forklift/pedestrian validation. Видео отдельно не исследовано и права на показ не установлены. Код supervision: https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/LICENSE.md — MIT. Модели/видео имеют отдельные права.

#### W1-03-S06 — статическая зона и pixel distance

https://supervision.roboflow.com/latest/detection/tools/polygon_zone/ — `PolygonZone`, `triggering_anchors`: default BOTTOM_CENTER, anchor-in-mask, не настоящее пересечение полного bbox и polygon. Документация latest — изменяемая. Полезно для минимальной restricted area логики, не содержит знания о движении станка.

https://docs.ultralytics.com/guides/distance-calculation/ и https://docs.ultralytics.com/reference/solutions/distance_calculation/ — `DistanceCalculation.process`, `pixels_distance`: евклидово расстояние между центрами двух выбранных bbox в пикселях. Открыты страницы; это наглядная baseline, не метрический датчик и не автоматический TTC. Центр человека находится выше пола; для floor geometry нужен иной anchor. Текущая страница про YOLO26 не является инструкцией совместимости старого S01 checkpoint.

#### W1-03-S07 — проверка маркетингового названия «forklift safety» по коду

https://github.com/sanaurrehmanarain/forklift-safety-ai ; tree SHA `78a1d68a7831f538d2f06e0e1d494685209cc771` получен GitHub API.

- https://raw.githubusercontent.com/sanaurrehmanarain/forklift-safety-ai/78a1d68a7831f538d2f06e0e1d494685209cc771/app/streamlit/app.py — load_model, zone_polygon, processing loop: фиксированный прямоугольный polygon от размеров кадра, track, pointPolygonTest для нижней середины каждого bbox, alert на каждом кадре.
- https://raw.githubusercontent.com/sanaurrehmanarain/forklift-safety-ai/78a1d68a7831f538d2f06e0e1d494685209cc771/data/dataset.yaml — единственный custom class 0 worker.
- Custom weights существуют по tree, но production-логики движущегося погрузчика нет. При base COCO model код не фильтрует class person и принимает любой bbox за работника. Нет состояния эпизода/дедупликации. README заявляет MIT; есть LICENSE 1076 B, веса и библиотеки отдельно.

Вывод: полезен как UI/zone reference, отказ от использования как готового person-machine detector. Самостоятельный тест запуска не выполнялся.

#### W1-03-S08 — готовый pixel-proximity пример и его точные ограничения

https://github.com/azimjaan21/Forklift_Worker ; SHA `a125147ec949df84dd5427c794d8d827c3406190`.

https://raw.githubusercontent.com/azimjaan21/Forklift_Worker/a125147ec949df84dd5427c794d8d827c3406190/monitoring_worker_forklift.py — функции point_to_bbox_distance/get_worker_anchor_from_pose, main: два predict, ankle→hip→bbox anchor, расстояние точки до forklift bbox, пороги 200/400 pixels. Ни track(), ни скорость техники, ни TTC не реализованы. При отсутствии детекций статус по умолчанию SAFE — нежелательное смешение unknown и safe.

Tree подтверждает `forklift_train/weights/best.pt` 40,524,133 B, `test_samples/test.mp4` 2,360,175 B и демо. Большие файлы не скачаны. README говорит MIT, но отдельного LICENSE в просмотренном tree нет; provenance весов/видео не установлен. Hip fallback непригоден как контактная точка пола для метрической homography. Две сети увеличивают число интеграций LinQ без обязательной выгоды для MVP.

#### W1-03-S09 — AisleGuard: наиболее близкий открытый пример, но не комплект

https://github.com/AayushAswal27/aisleguard ; tree SHA `ca6911da6dca28169dd39131884cf87cb4a49b99`.

- https://raw.githubusercontent.com/AayushAswal27/aisleguard/ca6911da6dca28169dd39131884cf87cb4a49b99/src/risk/ttc.py — constant velocity TTC для кругов через quadratic roots; PET по общим floor cells. TTC здесь размечает синтетическое обучение, не вызывается при infer BRIN.
- https://raw.githubusercontent.com/AayushAswal27/aisleguard/ca6911da6dca28169dd39131884cf87cb4a49b99/src/tracking/tracker.py — YOLO+BoT-SORT, bottom-center и trajectory CSV.
- https://raw.githubusercontent.com/AayushAswal27/aisleguard/ca6911da6dca28169dd39131884cf87cb4a49b99/app/streamlit_app.py — load_state_dict `models/brin/brin_final.pt`, YOLO `models/yolo/best.pt`.
- API tree не содержит ни одного из этих двух файлов; `LICENSE` 0 байт. README 93% collision recall относится к авторскому simulator-trained model и не доказывает результат на складе. Его uncalibrated video demo использует приблизительное масштабирование, что автор признаёт.

Вывод: сильный источник алгоритмической структуры и отрицательных контролей, но не переносимый checkpoint-пакет. Не тратить хакатон на воспроизведение обучения BRIN. Неопределённое переиспользование кода/весов.

#### W1-03-S10 — первичная геометрия и определение surrogate metrics

https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html — Basic theory, Perspective correction: homography связывает плоскости; произвольная 3D сцена одной H не исправляется. Открытая 4.x ссылка перенаправилась на 4.13.0. Отсюда вывод для нашей установки: калибровать пол, а не центры силуэтов; лестницы/рампы/поднятый груз требуют отдельной модели геометрии.

https://www.fhwa.dot.gov/publications/research/safety/08050/index.cfm — SSAM manual FHWA-HRT-08-050, May2008, определения TTC/PET: TTC основан на текущих положении/скорости/траектории, PET — временной зазор последовательного занятия места. Это дорожная surrogate safety методика, не утверждённая норма дистанции для погрузчика. Порог TTC 1.5s из дорожной литературы автоматически не переносить в цех. Threshold определяет ОТ для условий участка.

**Происхождение:** [W1-03.md](_WORK/W1-03.md), `## Инженерная спецификация`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Инженерная спецификация минимальных вариантов (собственные выводы)

#### W1-03-F01 — restricted area, минимальный честный MVP

Вход: фиксированная камера, одна видимая половая зона, bbox person после нейроинференса на LinQ. Ручной polygon в координатах исходного кадра; person bottom-center внутри зоны, допустимое расписание/режим работы. Если режим оборудования неизвестен, событие «человек в запрещённой зоне», без слова «движущаяся». Для станка с неизменным местом это полезно, но работа вращающихся частей по bbox не устанавливается.

Правило-кандидат: несколько наблюдений/0.3–0.5s внутри зоны при валидном track; переход OUTSIDE→CANDIDATE→ACTIVE. Порог — проектная начальная гипотеза, не норматив. Boundary hysteresis: enter polygon и чуть более широкий exit polygon/задержка 0.5–1s. При пропаже трека короткое удержание ACTIVE; отсутствие детекции не считать безопасностью. Длительный UNKNOWN закрывает эпизод с причиной, не создаёт новый сразу после каждого кадра.

Positive: работник входит и остаётся; negative: идёт вдоль границы снаружи, виден на другом уровне/за барьером, погрузчик без человека. Journal: camera, zone/version, track/pair, start, first_confirm, end, evidence, rule, confidence. Одно сообщение при создании ACTIVE, далее обновление записи. Re-entry после действительного выхода — новый эпизод. Cooldown в одиночку недостаточен: создаст повтор при длительном нахождении.

#### W1-03-F02 — person-machine interaction без метрических обещаний

Дополнение к F01: S01 detector для forklift/person; отдельные устойчивые tracks; по технике история ground-anchor в original pixels, время source timestamps, оценка вектора сглаживанием/робастной линейной аппроксимацией по 0.5–1s. Порог движения по контрольной стоящей технике/джиттеру detector, не произвольное «>0 px». История после ID-switch/reset заново набирается; мгновенный скачок скорости от нового ID запрещён.

Условие события: машина подтверждённо движется AND человек попадает в её настроенную proximity envelope AND pair наблюдается несколько раз. Можно дополнить closing trend, но близкий параллельный проход тоже может быть опасен по локальным правилам. Нельзя требовать уменьшения дистанции для всех типов риска. Для одного фиксированного кадрирования допустима area-dependent pixel envelope; подпись UI «2D зона риска», параметры калиброваны только под эту камеру. Масштабирование радиуса от bbox height — лишь эвристика, не метры.

Dynamic zone: swept corridor от позиции техники по её наблюдаемому вектору на короткий горизонт; дополнительно боковой/задний буфер. Heading не всегда совпадает с velocity при повороте/движении назад. Bbox всего погрузчика не содержит точную геометрию вил и груза. Водитель внутри кабины может детектироваться как person и вызывать ложное событие: учесть operator ROI/краткосрочное совместное движение, а не удалять любого человека с bbox overlap (так потеряем пешехода перед машиной).

Motion gate не гарантирует эксплуатационную безопасность: стоящий погрузчик с поднимающейся мачтой/вилами опасен; это отдельный класс движения механизма и потребует keypoints/segmentation/режима оборудования. Перемещение центра bbox этого не видит.

#### W1-03-F03 — метрическая дистанция и условный TTC

Условия: жёстко закреплённая камера, стабильный zoom/crop, undistortion при заметной дисторсии, плоский пол, минимум 4 неколлинеарные соответствующие точки с измеренными XY; лучше дополнительные контрольные точки по всему ROI и независимые измерения ошибок. H переводит контактные точки в метры. Для forklift нужен footprint с размерами/ориентацией/вилами, не просто один центр. Для person — foot anchor и неопределённость. За пределами области калибровки/на рампе состояние unknown либо отдельная H.

Относительные величины: r=p_machine−p_person, u=v_machine−v_person. Closing speed = −r·u/|r|. Время ближайшего подхода t*=−r·u/(u·u), только при u≠0 и t*>0. d_min=|r+u t*|. **t* не равно TTC**: траектории могут пройти с достаточным боковым зазором. Для дисков радиуса R=R_person+R_machine TTC — первый неотрицательный корень |r+ut|²=R²; при отсутствии корня collision по этой модели нет. Если уже внутри R — TTC=0. Реальную форму лучше учитывать полигонами/swept volumes. Простое distance/closing_speed неверно для произвольного пересечения путей.

Это прогноз только при предположении постоянной скорости на коротком горизонте, без знания намерений, реакции, тормозного пути, заноса и остановки. Тормозная safety envelope потребует v·reaction_time+v²/(2a)+margin, причём reaction_time/a должны быть измерены или заданы для конкретной машины/груза/покрытия. Не выдумывать их. PET ретроспективен и подходит near-miss analytics, не предупреждению до первого пересечения.

**Происхождение:** [W1-03.md](_WORK/W1-03.md), `## FP/FN`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### FP/FN, наблюдаемость и событие

| Случай | Ошибка простого baseline | Нужный контроль |
|---|---|---|
| Стоящая техника, дрожащие bbox | Ложное движение | motion threshold на stationary controls, robust history |
| Камера вибрирует | Всё движется | global motion compensation либо quality/unknown |
| Человек ближе по изображению, но на другом плане/за оградой | Ложная близость | ground plane, barrier polygons, разрешённые маршруты |
| Движение назад/поворот | Неверный передний коридор | observed velocity + rear/side zones, history validity |
| Мачта/вилы двигаются на месте | FN от center motion | отдельная постановка; не обещать покрытие |
| Окклюзия человеком/грузом, размытие | Пропуск detector/ID fragmentation | unknown, короткое track retention, event stitching |
| Два человека и один forklift | Смешение пары | ключ camera/person_track/machine_track + spatial reconnect |
| Водитель в кабине | Ложная тревога | операторская область/контекст, отдельный negative |
| Пересекающиеся линии с разным временем прохода | Ложный collision | t* и d_min/TTC, PET для ретроспективы |
| Один безопасный длительный эпизод / один опасный эпизод 10s | Повторные записи | episode state, one emission; ID-switch test |

Дедупликация: базовый ключ пары и camera; пока ACTIVE, не повторять alert независимо от числа кадров. При ID fragmentation сшивать лишь при совместимости класса/позиции/времени, с запретом слияния двух одновременных людей. Несколько машин/людей могут означать несколько реальных событий; политика объединения на уровне зоны должна быть явной. Не подавлять независимое событие глобальным cooldown. Кадр хранит факт наблюдаемого риска и основание правила; слово «нарушение» требует настроенной локальной нормы и обычно операторского подтверждения.

**Происхождение:** [W1-03.md](_WORK/W1-03.md), `## Отказанные`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Отказанные/резервные направления

- S07 как готовый detector движущейся техники — отказ: по коду только worker zone.
- S08 pose+forklift — резерв визуализации: лишняя сеть, чисто pixel proximity, нет motion gate, не установлены права весов/footage.
- S09 BRIN — отказ как быстрый готовый артефакт: checkpoints не в tree, пустой LICENSE, simulator result не переносится. Формула TTC полезна как reference, собственная простая rule-based геометрия предпочтительнее нового обучения.
- HF https://huggingface.co/thalostech2025/thalos-forklift-safety-v1 найден в выдаче: card использует названия near_person и расплывчатое «class names may vary». Без проверки exact output/schema/weights не выбран: изображение с классом near_person само по себе не доказывает динамическое взаимодействие.
- https://github.com/SelimSavas/forklift-and-people-detection-with-YOLOv5 найден: README даёт 3000 изображений/Google Drive и пример /content/best.pt, но наличие переносимого checkpoint и права в рамках этой ветки не установлены. Не преимущество перед точным S01.
- Непроверенные рекламные «30m detection», «100% на 55 изображениях» не являются инженерным подтверждением person-machine events/LinQ; в вывод не использованы.

<a id="F022"></a>
## F022 — Moving forklift: real motion/driver controls, synthetic pair и exact best.pt

**Нормализованный статус и условия:** GO internal synthetic image-space smoke; NO-GO complete public real-world route. MIT publisher index положителен, standalone HF weights scope остаётся отдельным. CC BY primary identity F015 относится к 0_te23/4_te1, не автоматически 3_te1/7_te1.

**Источники:** [S064](SOURCES.md#S064), [S158](SOURCES.md#S158), [S161](SOURCES.md#S161), [S191](SOURCES.md#S191), [S192](SOURCES.md#S192), [S193](SOURCES.md#S193), [S194](SOURCES.md#S194), [S195](SOURCES.md#S195), [S196](SOURCES.md#S196), [S197](SOURCES.md#S197), [S198](SOURCES.md#S198), [S199](SOURCES.md#S199).

**Происхождение:** [W2-04.md](_WORK/W2-04.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Дата доступа/наблюдений: **2026-10-23**. Ветка закрывает адресно K005/K008/K001, не общий выбор MVP. Прочитаны W1-03 полностью, W1-10 полностью, релевантный R3 W1-16, сохранённые W1-10 selected_samples / NVIDIA index / decoded manifest. Все новые файлы в `W2-04_evidence/`. Никакого NN-инференса, экспорта, установки библиотек, обучения или LinQ execution не выполнялось. Чужой код не исполнялся. Собственные bounded HTTP/ZIP/pickletools parsers и существующие PyAV/Pillow использованы для чтения/декодирования. `pickletools.dis` не является unpickle/torch.load.

#### Решение

**GO только для дальнейшего внутреннего smoke исследования synthetic image-space interaction. NO-GO для заявления готового реального moving-forklift pedestrian detector и публичной поставки этого exact checkpoint с полностью закрытыми правами.**

Новая полезная цепочка существует в фактически полученных байтах: **NVIDIA `NV-VAD-v1/video_00238` → отдельные стоящие люди + приближающийся погрузчик → кандидат 2D pair proximity**; `video_00298` даёт normal/distant-machine control. Это синтетические Veo/Cosmos-данные, не настоящие near-miss записи. Необходимый stationary forklift + near person control в выбранных материалах не установлен. Качество/события/метры/TTC и LinQ не проверены.

Начальные `3_te1`/`7_te1` теперь действительно скачаны и декодированы: движение машины видно в обоих, водитель есть; отдельный уверенно различимый **проходящий пешеход** не найден в осмотренных кадрах. У правого станка виден работник, но низ тела/контакт с полом неоднозначен, частично закрыт станком/машиной. Нельзя объявлять его pedestrian near-miss positive по clip label. Эти файлы полезны как real-machine motion/driver controls и как отдельный overload сюжет.

Exact `best.pt` теперь подтверждён локальным SHA256 и статическим чтением names: **0 forklift, 1 person**. Это сильнее W1 ожидаемого mapping. Первичный связанный publisher repository действительно говорит MIT для «project» и перечисляет эту модель; это положительное лицензионное свидетельство, которое надо сохранить. Однако явное распространение MIT на **HF checkpoint/веса/производный compiled artifact** не установлено; HF card/API/tree лицензии весов не содержит. Не заменять данный пробел CC BY датасета и не утверждать доказанное отсутствие любых разрешений.

#### W2-04-S01 — Safe/Unsafe: actual bytes и PTS

Первичная страница: [Önal/Dandıl, dataset V1](https://data.mendeley.com/datasets/xjmtb22pff/1), DOI `10.17632/xjmtb22pff.1`, опубликован **2024-06-11**, CC BY 4.0. Статья/семантика W1 сохранены: класс3 — overload, класс7 — safe carrying; это не labels near-miss. Согласования съёмки заявлены авторами, тексты согласий не получены.

Получено зеркало [Voxel51](https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/tree/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5), revision `7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5`. Exact URL: `https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/resolve/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5/data/` + filename. Полные bytes сохранены; byte identity с **первичным Mendeley ZIP** не установлена. Связь зеркала с dataset по W1 есть; это не новый primary hash proof.

| File | Bytes / SHA256 | Decode (наше наблюдение) |
|---|---|---|
| `3_te1.mp4` | 24,506,317; `79c298ce0cb0eaa9a920285dce299dadc25ebfc737bf1f058c981f6bc2e23517` | 1920×1080, 250 frames, PTS0…9.96, rate25 |
| `7_te1.mp4` | 4,458,655; `d99184fd5b7e3430bf31a31e3080a843e03dbdd4625828c81ffef97417a9a6b6` | 1920×1080, 177 frames, PTS0…7.078984, average rate дробный; после начала есть нерегулярный шаг |

Все PTS в `video_manifest.json`; не заменять их `frame/24`. Контактные листы `3_te1.mp4.jpg`, `7_te1.mp4.jpg` содержат каждый25-й кадр (~1 s); **декодированы все кадры, визуально осмотрены именно листы**, не выполнено непрерывное ручное actor labeling каждого кадра.

**W2-04-F01 — реальные motion/driver controls, но не подтверждённый pedestrian positive.**

- `3_te1`: уже в frame0 машина с высокой стопкой оранжевых контейнеров; frame25/50/75/100 она смещается вправо и ближе к камере, frame150…225 поворачивает у станка. Уверенное визуальное движение на PTS0–5; более позднее изменение ориентации/положения на PTS6–9. Driver в кабине — associated person, не отдельный пешеход. У станка справа видна человеческая фигура; нижние конечности закрыты, нельзя надёжно поставить floor anchor или объявить walking. При перекрытии погрузчиком `unknown`, а не отсутствие человека.
- `7_te1`: машина с двумя контейнерами разворачивается и уходит вглубь/влево; движение уверенно на кадрах0/25/50/75/100/150. Driver в кабине и тот же рабочий участок справа. Отдельного шагающего человека в осмотренных кадрах не установлено. Safe carrying — **не** all-person/all-rule safe label.
- Измеримый image-space claim, без модели: в `3_te1` видимый контур машины смещается в направлении нижнего правого края между PTS0 и3; в `7_te1` тот же объект меняет x/y и ориентацию между PTS0 и6. Это воспроизводимая визуальная проверка movement gate, не оценка физической скорости. Точные bbox/footprint trajectories не размечались.
- Полученного stationary+near отрицательного эпизода здесь нет: остановку у станка по редким кадрам нельзя автоматически считать доказанной неподвижностью; также неизвестно, на ногах ли работник и как далеко он от машины на полу.

#### W2-04-S02 — компактное извлечение NVIDIA без полного ZIP

Первичный [publisher card](https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos), pinned [README](https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos/blob/7f79b39fcd1ef1dc39f23f227cd8a9480d6077db/README.md), revision `7f79b39fcd1ef1dc39f23f227cd8a9480d6077db`. Дата доступа2026-10-23; release metadata2026, не смешивать с датой съёмки или генерации каждого sample. Полные свежие records двух выбранных videos получены из `2026/train/labels.json` и сохранены в `nvidia_actual_selected_labels.json`; provenance в `nvidia_provenance.json`. Внутренние даты/имена annotation batches не являются датой реального события.

Архив: `https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos/resolve/7f79b39fcd1ef1dc39f23f227cd8a9480d6077db/2026/train/videos.zip`, размер **7,954,992,209**. Собственный `range_zip.py` получил хвост, ZIP64 EOCD, central directory, две local headers и два payload. Каждый запрос проверял HTTP206, фактическую длину и Content-Range; non-206 отвергается до полного чтения. Central directory содержит **1486 members**, это теперь observed, не вывод из README.

Успешный проход передал **5,785,956 bytes** архивных диапазонов (`range_log.json`), полный ZIP не получен. Первый проход прочитал ещё245,608 bytes: обычное EOCD содержало ZIP64 sentinel `0xffffffff`; неверная попытка читать по нему не дала entries, затем parser исправлен на ZIP64. Это не пропавший data sample и не отказ Range. Полный hash архива **не вычислялся**. Для извлечённых members проверены длина и ZIP CRC32, затем полный локальный SHA256.

| Member | Payload byte range inclusive / bytes | SHA256 |
|---|---|---|
| `videos/video_00238.mp4` | 1618328501–1622115017 / 3,786,517 | `082334ce4916270d6edaf27b97cf9181f7917615601831d15cdf52c78e2c2222` |
| `videos/video_00298.mp4` | 1803721470–1805475240 / 1,753,771 | `01a382a244a2f5d70916c8b606eac73a4324a4a05adf0588bef873dbacd8ed0e` |

Entries/offsets/compression/CRC в `zip_members.json`, raw directory в `zip_central_directory.bin`. Это доказательство **фактического наличия и получения members**, а не просто media URL/HEAD. Оба MP4 полностью декодированы: **1280×720, 144 frames, 24fps, PTS0…5.958333333, шаг1/24**. PTS в `synthetic_decode.json`, листы каждые12 frames/0.5s в `video_00238.mp4.jpg`, `video_00298.mp4.jpg`.

**W2-04-F02 — synthetic positive с отдельными людьми подтверждён по кадрам.**

`NV-VAD-v1/video_00238`: исходный label `near miss forklift person`, chunk0000–5s=true. На **наших** кадрах два человека в проходе, за ними погрузчик с водителем, движущийся к ним; справа ещё человек/вторая машина на ближнем плане. Основную пару брать **задний приближающийся forklift + мужчина с планшетом либо стоящая рядом женщина**, не драйвер и не правый объект.

- PTS0…3.5: отдельные люди стоят/слабо меняют положение, задняя машина увеличивает проекцию и приближается в изображении; co-visible pair. PTS4…5.5 мужчина делает шаги влево/вперёд и отделяется от траектории; женщина остаётся у стеллажа. Это видимая временная переменная, отсутствующая у generic polygon.
- Driver в задней кабине виден примерно с PTS1.5 и дальше, всё яснее к4.5–5.5; не считать его proximity violation к собственной машине. Точные first visibility/onset по1/24 не размечались.
- Измеримый ручной image-space proxy на листе640×360: нижние концы вил задней машины находятся приблизительно на y≈200 в PTS0 и y≈330 в PTS5.5; изменение **~130 thumbnail px / ~260 native px**. Это грубое считывание листа (погрешность порядка10–20 thumbnail px), не detector output/скорость на полу. Силуэты людей отделимы от кабины; реальная дистанция между стопой и swept footprint не измерена.
- Окно0–1.5 можно использовать как **relatively far in image** против позднего3–4.5, но не как установленно безопасное расстояние. Целый клип не задаёт точную onset. Предсказанный label chunk0–5 и поздний уход человека нельзя выдавать за опасный эпизод с точным ground-truth временем.
- Generated видео может искажать геометрию, поведение, внешний вид и стабильность камеры. По кадрам нет очевидного монтажного разрыва, но геометрическая/физическая достоверность генерации не сертифицирована.

**W2-04-F03 — negative control не идеален, useful с actor scope.**

`NV-VAD-v1/video_00298`: normal, два overlapping chunks0–5 и1–6. Это **один parent source**, не два независимых negative clips. Сверху виден складской проход, работник у коробок, другой человек внизу справа; с PTS≈3 на дальнем конце видна машина, меняющая положение к5.5. Для foreground worker машина остаётся далеко **в изображении**; это useful moving+far candidate. Но с PTS4.5…5.5 другой человек проходит около дальнего forklift: normal publisher label не разрешает размечать этот другой pair как guaranteed safe. Driver/lower-body/footpoint далёкого объекта плохо различимы. `stationary+near` в этой записи также не подтверждён. Нет калибровки или норматива distance.

Source/run grouping: оба records из `NV-VAD-v1`, но разные parent IDs; все windows одного parent держать в одном split. Exact shared generation seed/run/camera для этих двух videos в полученных records не установлен. Разные IDs **не доказывают** независимость генерационного сценария. Не использовать эту пару как обоснование статистической точности или transfer на реальный CCTV.

#### W2-04-S03 — exact checkpoint, bytes и static names

Model: [keremberke/yolov8n-forklift-detection](https://huggingface.co/keremberke/yolov8n-forklift-detection), pinned revision `d8b594f321dd4c64eda16e435601fd266089fc32`. Exact [best.pt](https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/d8b594f321dd4c64eda16e435601fd266089fc32/best.pt), **6,216,376 bytes**, фактический локальный SHA256 `0dc3816283226f0f7ac5410620394c8ddeef32c5200b371194ac4df4a1ee7d38` совпал с LFS oid из свежего tree. Card/config/API/tree и checkpoint сохранены. Файл не десериализован и не выполнялся.

ZIP `data.pkl` разобран `pickletools.dis`, без GLOBAL/REDUCE execution. `checkpoint_pickle_disassembly.txt`, строки32422–32433, pickle byte offsets77445–77505: ключ `names`, словарь **{0:'forklift',1:'person'}**. В этом блоке наблюдается содержимое checkpoint; это не гарантия успешного runtime load или графа ONNX. Путь к training data в pickle — Windows `Forklift-1/data.yaml`, не дополнительная поставка данных.

**W2-04-F04:** exact mapping закрыт на уровне static checkpoint metadata; W1 uncertainty «проверить model.names» сужена. Actual exported graph I/O/operators/normalization/parity остаются непроверенными. W1 ожидаемый `[1,6,8400]` не повышается здесь до observed ONNX shape.

#### W2-04-S04 — publisher grant: положительное свидетельство и граница

Адресный поиск открыл HF card/tree/discussions и связанный первичный [keremberke/awesome-yolov8-models](https://github.com/keremberke/awesome-yolov8-models). У HF карточки нет license поля/лицензионного текста, в exact tree нет LICENSE, discussions не содержат опубликованного уточнения. Это результат конкретной проверки, не доказательство отсутствия grant где-либо.

**Новое:** связанный авторский GitHub index перечисляет exact HF forklift nano model в Detection Models и лицензирует «This project» MIT. Открыты и сохранены [README](https://github.com/keremberke/awesome-yolov8-models/blob/fb4b7895a92913023ef222fdf0957b8ce2015766/README.md) и [LICENSE](https://github.com/keremberke/awesome-yolov8-models/blob/fb4b7895a92913023ef222fdf0957b8ce2015766/LICENSE), pinned commit `fb4b7895a92913023ef222fdf0957b8ce2015766`; `publisher_commit.json`, `publisher_README.md`, `publisher_LICENSE`. Это существенный favorable publisher signal, не игнорировать его и не говорить «вообще лицензии нет». Формулировка не уточняет, что off-repo HF weights и compiled derivatives тоже MIT; отдельный explicit weight grant не найден. Нужна интерпретация/уточнение scope именно этих bytes; писем не отправлялось.

| Артефакт/действие | Установлено | Остаток перед публичной поставкой |
|---|---|---|
| HF best.pt → локальный static research | доступен, точный hash/names; publisher показывает reuse instructions | это не новый legal prohibition и не NN quality proof |
| HF/compiled weights → репозиторий команды, публичный downloadable demo | MIT project index существует; exact standalone grant отсутствует | подтвердить scope автора/выбрать artifact с явным grant; export не меняет происхождение |
| Ultralytics8.0.21 code | W1 первичный тег GPL-3.0 | соблюдать конкретную поставляемую версию; не переименовывать весь stack MIT |
| Forklift image dataset | W1 CC BY4 | не переносить на веса/видео |
| Real Safe/Unsafe MP4 | первичные данные CC BY4, авторы заявляют approvals | credits, связь mirror→primary bytes и конкретный режим показа/consent остаются scoped |
| NVIDIA два MP4 | первичный card NVIDIA Dataset License, предупреждает Google terms для Veo | не CC BY; не обещать unrestricted redistribution/live recording; точный generator для этих IDs не установлен |

README NVIDIA ссылается на [Dataset Agreement PDF 2025-11-26](https://assets.ngc.nvidia.com/products/api-catalog/legal/Personas-Dataset-NVIDIA-Training-Dataset-License-Agreement-2025-11-26.pdf) и Google service terms. Договор PDF здесь полностью не анализировался; blanket публичный/коммерческий grant **не заявлен**. Для текущей внутренней оценки полезность samples есть; публичную видео-поставку решать per-artifact/action. Это отдельный вопрос от очевидной синтетической природы.

#### Статусы K и ближайший эксперимент

| K | Итог W2-04 | Что изменилось относительно W1 |
|---|---|---|
| **K005** | **scoped**, не closed end-to-end | Получены реальные motion clips и synthetic pair positive+частичный far control. Больше не «есть лишь индекс/архив». Нет надёжного real pedestrian interaction positive, stationary+near, NN quality, calibration, LinQ |
| **K008** | **scoped/open для weights redistribution** | Локальные checkpoint bytes/hash/names; найден favorable MIT publisher index, но не explicit standalone weight grant. Data CC BY сохранён; NVIDIA terms отдельно |
| **K001** | **scoped для этого route** | Сценарий остаётся temporal interaction: machine motion + pair separation over PTS. Generic polygon этим не становится. В shortlist считать условным исходным сценарием2 только после event/device/rights gates |

Предложенный observation contract: `(person_id, forklift_id)` с одновременной видимостью → минимум два/несколько valid observations машины в общей системе координат → подтверждённое изменение положения (camera motion отдельно) → расстояние person anchor до agreed machine footprint/опасной области в **image coordinates** → persistence/hysteresis → один incident на pair episode. Driver и worker с закрытым footpoint помечаются associated/unknown соответственно; потеря детекции не означает safe. Ни thresholds, ни event accuracy этим research не установлены.

**Метры запрещены в заявлении**, пока нет измеренной floor calibration с единицами, стабильной камеры, подтверждённых anchors/footprint и проверки ошибки на контрольных точках. Для ramps/разных плоскостей одна homography недостаточна. **TTC в секундах нельзя называть физическим collision TTC** по centroids/uncalibrated pixels/generated scene: нужны геометрия общего пространства, time-valid relative velocity, swept extents и проверенная motion model. PTS делает время реальным для файла, но не делает image coordinates метрами. Здесь допустимы лишь подписанные image-space proxy и наблюдаемое изменение проекции; даже уменьшение такого расстояния не доказывает рост физического риска.

Точные остатки Q/E:

1. **E-real:** получить безопасную собственную/разрешённую фиксированную запись с отдельным человеком на ногах и движущимся forklift; той же камерой stationary+near, moving+far, driver-only, occlusion. Не организовывать опасный near-miss; положительный proxy можно показать при безопасной дистанции и честной 2D трактовке.
2. **E-annotations:** размечать конкретные person/machine IDs, footpoint/visibility, motion intervals, image-space close/far отдельно от safety label. Сейчас контактные листы и грубые интервалы — triage, не frame-level ground truth. Не считать publisher normal all-person negative.
3. **Q-grant:** проверить распространение publisher MIT на exact HF hash и compiled/redistributed derivative либо заменить checkpoint на явно лицензированный artifact. Не подменять CC BY data.
4. **E-device:** фактический export6 channels, class-aware decoder, CPU→LinQ parity и timings, затем события/дедуп/controls. Без этого никакого hardwarePASS.

Ближайший шаг команды: использовать полученные два synthetic MP4 как маленький reproducible host/event smoke пакет после решения artifact grant; параллельно создать безопасные real controls. При невозможности закрыть эти gates к дедлайну — **no-go этой data+checkpoint route как готового третьего сценария**, не переименовывать pedestrian polygon в moving-forklift interaction.

<a id="F023"></a>
## F023 — Factory CCTV и industrial/synthetic data alternatives: clip semantics, права и actual availability

**Нормализованный статус и условия:** Byte identity0_te23/4_te1 закрыта F015. NVIDIA video00238/00298 действительно получены F022, прежнее W1 not-acquired историческое. Safe label4 не all-actor negative; initial occupancy не entry.

**Источники:** [S064](SOURCES.md#S064), [S150](SOURCES.md#S150), [S192](SOURCES.md#S192), [S193](SOURCES.md#S193), [S200](SOURCES.md#S200), [S201](SOURCES.md#S201), [S202](SOURCES.md#S202), [S203](SOURCES.md#S203), [S204](SOURCES.md#S204), [S205](SOURCES.md#S205), [S206](SOURCES.md#S206), [S207](SOURCES.md#S207), [S208](SOURCES.md#S208), [S209](SOURCES.md#S209), [S210](SOURCES.md#S210), [S211](SOURCES.md#S211), [S212](SOURCES.md#S212), [S213](SOURCES.md#S213), [S214](SOURCES.md#S214).

**Происхождение:** [W1-10.md](_WORK/W1-10.md), `## Источники`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Источники и тип доказательства

#### W1-10-S01 — первичный Mendeley dataset V1

[Video Dataset for Safe and Unsafe Behaviours](https://data.mendeley.com/datasets/xjmtb22pff/1), DOI `10.17632/xjmtb22pff.1`, опубликован 2024-06-11, авторы Önal/Dandıl. Открыты Description, Steps to reproduce, Licence. Авторы сообщают 691 clip, две IP-камеры предприятия в Турции, съёмку 39 дней после получения согласований. Страница данных устанавливает **CC BY 4.0**; это лицензия данных, не кода модели. Заявлены MP4/H264/1920×1080/24 FPS; фактические файлы уточняют последнее (S03). HTML web extraction не показал индивидуальный список файлов; не считать это отсутствием файлов. Пробованный `/public-api/datasets/xjmtb22pff/versions/1` ответил 404; этот недокументированный endpoint не использовать как API.

#### W1-10-S02 — первичная статья, семантика и splits

[Önal, Dandıl, Data in Brief 56, 110791](https://pmc.ncbi.nlm.nih.gov/articles/PMC11367630/), DOI `10.1016/j.dib.2024.110791`; [копия учреждения авторов](https://acikkaynak.bilecik.edu.tr/server/api/core/bitstreams/dc6b0007-eb9b-4496-9d00-81ecb68fa9b4/content). Локаторы: Tables 1–3, Figures 1–2, Experimental Design. PMC search вернул полный релевантный текст; последующее open упёрлось в CAPTCHA. Установлено из статьи: camera9 — дорожка и станок, camera14 — погрузчик; train/test 566/125. Классы 0/4 = Safe Walkway Violation/Safe Walkway (178/32 и 50/25 train/test), 3/7 = Carrying Overload with Forklift/Safe Carrying (48/8 и 22/8). Перегруз здесь означает ≥3 блоков против ≤2; это не near-miss. Классы 1/5 — вмешательство, 2/6 — крышка панели. Авторизация в статье связана с жилетом и местным правилом; переносить на иной завод нельзя. Имена `0_tr1`, `0_te1` кодируют класс/split/номер. Одна сцена может содержать несколько поведений. Клиповые классы не задают точный момент начала нарушения. Наличие train/test не доказывает независимость камер или исходных временных эпизодов. Лицензия статьи CC BY-NC не заменяет CC BY данных.

#### W1-10-S03 — доступное зеркало с точными файлами и разметкой

[HF Voxel51/Safe_and_Unsafe_Behaviours](https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours), revision **`7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5`**, получена через [API](https://huggingface.co/api/datasets/Voxel51/Safe_and_Unsafe_Behaviours). Зеркало не авторский первоисточник съёмки; происхождение и license сопоставлены с S01. `gated=false`. [Tree](https://huggingface.co/api/datasets/Voxel51/Safe_and_Unsafe_Behaviours/tree/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5?recursive=true&limit=1000), [samples.json](https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/resolve/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5/samples.json), [metadata.json](https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/resolve/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5/metadata.json), [frames.json](https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/resolve/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5/frames.json) прочитаны прямым GET.

`ground_truth` имеет `_cls=Classification`, `label`; tags задают train/test. `frames.json` содержит пустой массив. В проверенном зеркале **нет bbox/tracks/pose/per-frame risk intervals**. Это события на уровне клипа, не только object boxes, но для оценки detector→tracker→rule нужна собственная actor/event разметка. `metadata.default_classes` имеет технические prefixed names, тогда как sample label человекочитаемый; не считать их идентификаторами YOLO.

Все URLs следующей таблицы имеют один точный prefix:
`https://huggingface.co/datasets/Voxel51/Safe_and_Unsafe_Behaviours/resolve/7369ff1830b5f6c00f7d7383eeeaa90704bfc5b5/data/` + filename. HEAD каждого вернул **200, video/mp4**, Content-Length совпал с tree. Полные sample records сохранены в `W1-10_evidence/selected_samples.json`.

| Filename | Роль | Bytes | Duration s / frames / rate metadata | Проверка содержимого |
|---|---|---:|---|---|
| `0_te23.mp4` | positive zone candidate | 6,391,494 | 10.477582 / 241 / 23.001489 | скачан, decoded, выбранные кадры осмотрены |
| `0_te21.mp4` | дополнительный positive | 6,455,941 | 10.4512 / 252 / 24.112064 | metadata+HEAD, не просмотрен |
| `4_te1.mp4` | negative target actor candidate | 13,209,619 | 6.92 / 173 / 25 | скачан, decoded, выбранные кадры осмотрены |
| `0_tr1.mp4` | настройка зоны/порога | 25,865,947 | 14.015304 / 348 / 24.83 | metadata+HEAD, не просмотрен |
| `4_tr1.mp4` | настройка negative | 22,466,611 | 12.605042 / 315 / 24.99 | metadata+HEAD, не просмотрен |
| `3_te1.mp4` | forklift load, отдельный сценарий | 24,506,317 | 10 / 250 / 25 | metadata+HEAD, не просмотрен |
| `7_te1.mp4` | safe load control, отдельный сценарий | 4,458,655 | 7.118984 / 177 / 24.863097 | metadata+HEAD, не просмотрен |

Локально вычисленные SHA256 двух скачанных файлов совпали с LFS oid:

- `0_te23.mp4`: `e2c053d84413775e6becaf0dc2a1dd69cbfbb47a5747704345ede650d1987a7f`.
- `4_te1.mp4`: `11049609f60c52702b90541e6d50146f5ff56d951c9fbf748cd164accb21226a`.

#### W1-10-S04 — непосредственные наблюдения видео, не вывод из названия

Локальные `W1-10_evidence/0_te23.mp4`, `4_te1.mp4`; 1920×1080. JPEG frames 0,50,100,150 каждого файла извлечены; лично осмотрены frames0/150 каждого. В `0_te23` человек в ярком жилете идёт по серому транспортному коридору, справа видна зелёная дорожка с жёлтыми краями; присутствуют люди дальше и работник за оборудованием слева. В `4_te1` дальний человек идёт по зелёной дорожке, но ближний человек находится у станка вне неё. Видимый fixed view совпадает; промышленное оборудование и физические ограждения видны. Перелезание/проход под установкой и взаимодействие с движущимся forklift в осмотренных кадрах не наблюдаются.

**Safe clip не является all-frame/all-person negative:** target actor на дорожке — negative для его траектории; другой работник у станка не обязан соблюдать дорожку в рабочей зоне. Нельзя закрасить всё вне зелёного forbidden polygon и объявить все детекции нарушителями. Нужны дорожный corridor ROI, разрешённые рабочие островки, actor-specific ground truth и местное правило. Иначе система «правильно» воспроизведёт ошибку постановки задачи. У `0_te23` actor уже вне дорожки на первом кадре: это проверка присутствия/длящегося события; начало выхода и задержку entry по этому фрагменту установить нельзя.

`decoded_manifest.json`: `0_te23` decoded241, last PTS10.397570; интервалы соседних PTS около .04 и .08 s, один .072895. Frame50/100/150 имеют PTS2.037566/4.037566/6.037566. Для `4_te1`: decoded173, PTS0…6.88, каждый шаг .04 s. Значит нельзя считать `frame_index/24` универсальным временем. Duration контейнера, последний PTS и average_rate — разные поля. Это установленная техническая особенность двух файлов, не оценка качества алгоритма.

#### W1-10-S05 — NVIDIA PhysicalAI-Event-Videos: интервалы near-miss, синтетика

[Card](https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos), [API](https://huggingface.co/api/datasets/nvidia/PhysicalAI-Event-Videos), revision **`7f79b39fcd1ef1dc39f23f227cd8a9480d6077db`**, gated=false. Проверены tree и JSON `2026/train/labels.json` (8,656,320 B), не медиа. Card: synthetic/generated, train only, free-text anomaly types, hybrid annotations; права NVIDIA Dataset License с дополнительными условиями для Veo. Не трактовать как CC BY. Метаданные не дают метрическую калибровку или bbox.

Точные records из JSON сохранены в `nvidia_selected_index.json`: `NV-VAD-v1/video_00238` — 6 s/24fps, `near miss forklift person`, chunk000 [0,5] true; `video_00239` — chunk000 [0,5] false и chunk001 [1,6] true. Это сильно перекрывающиеся окна, а не независимые негатив/позитив и не точная onset-разметка. Normal candidates: `video_00298`, `video_01037` (с forklift в описании); медиа не просмотрены. В архиве path `videos/video_00238.mp4`; chunk `chunks/NV-VAD-v1/video_00238/chunk_000.mp4`. `videos.zip` 7,954,992,209 B, `chunks.zip` 3,853,242,520 B; отдельных MP4 tree не содержит. Архивы не скачивались; пути подтверждены схемой/индексом, наличие конкретного member не проверялось. Generation scenarios группировать при split; соседние chunks всегда вместе.

#### W1-10-S06 — новый более геометрически полный synthetic warehouse источник

[NVIDIA PhysicalAI SDG-Warehouse](https://huggingface.co/datasets/nvidia/PhysicalAI-WorldModel-Synthetic-Warehouse-Operations-Scenes), API SHA **`d5b88d3abcf659f304a107f4336b71b4e2159133`**, gated=false; README прочитан HTTP GET. Авторы заявляют Isaac Sim, near-miss с worker/forklift, 5–10 синхронных ракурсов, 2D/3D boxes, intrinsics/extrinsics, depth; лицензия OpenMDW1.1. Это наиболее содержательный найденный кандидат для геометрической валидации, но не реальные заводские записи. Индексы `metadata/runs.parquet`, `clips.parquet`; медиа — WebDataset tar около5GB. Пример ключа README `fd7cc35596b247b16b0b_run_8_seed_864110064.ceiling_00.rgb.mp4` — пример схемы, не проверенный скачанный sample. 549GiB RGB near-miss subset исключён из текущей работы. Ни индексы, ни архивы не скачаны; run-level разбиение, единицы 3D, полноту камер и параметры near-miss ещё проверять. Права и численные характеристики выше — заявления card, не просмотр договорного текста или измерение данных.

#### W1-10-S07 — CAAR: релевантен барьерам/грузу, но доступ ограничен

[Сайт авторов](https://caar24.github.io/caar24/), Features/Gallery/Downloads/Terms. Открыт заново. Промышленные proper/improper actions, fixed/drone/GoPro виды; gallery явно показывает подход к подвешенному грузу и касание. Доступ требует email-запроса; terms: academic research only, no redistribution, no commercial use, disclosure только в academic publications/presentations. Не отправлялись запросы. Готовых exact clip IDs/файлов/лицензированного hackathon demo не получено. Поэтому не ставить CAAR в критическую цепочку дедлайна; snapshots gallery не заменяют видео.

#### W1-10-S08 — iSafetyBench: реальные clips, права на исходники не закрыты

[Project](https://isafetybench.github.io/), [авторское HF](https://huggingface.co/datasets/raiyaanabdullah/isafety-bench), revision API **`8336f1c57076d598677effa1da9870b300790804`**, gated=false. Card прочитан, tree подтверждает отдельные `hazard/*.mp4`, `normal/*.mp4`. Проект заявляет 1100 clips, multi-label действия. Card: CC BY-NC-SA4.0, исходные отрывки YouTube для research/educational/noncommercial purposes, fair-use intent, собственность исходников не заявляется. Лицензия страницы project CC BY-SA4.0 — не лицензия видео. Без первичной actor/event таблицы и просмотра clip не выбран как обязательный источник; возможность скачать mp4 не равна праву использовать любой исходный материал в коммерческом demo. Конкретный пример tree `hazard/-0zRCAh9_N4_trim_0.mp4` подтверждает файл, но его сюжет здесь неизвестен.

#### W1-10-S09 — tracking/anomaly controls, отклонённые замены

[CHAD авторский repository](https://github.com/TeCSAR-UNCC/CHAD): четыре камеры парковки, bbox/re-ID/pose и frame-level anomaly; running/falling и другие действия. Это не industrial forklift risk ontology; anomaly-флаг не означает proximity. Есть links на video/meta/splits, но архив не получен, права видео не установлены — не заменяет нужный near-miss sample.

[VIRAT primary site](https://viratdata.org/): стационарные внешние камеры, люди/автомобили, подробные interaction events и дополнительные DIVA annotations. Ground video под Protection Agreement; interaction «вход в машину/погрузка» не равен опасному сближению. Из-за отсутствия установленного exact licensed risk clip не выбран. [keremberke forklift detector dataset](https://huggingface.co/datasets/keremberke/forklift-object-detection) из W1-03 остаётся изображениями person/forklift: не использовать как видео и temporal-event test.

**Происхождение:** [W1-10.md](_WORK/W1-10.md), `## Минимальный набор`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Минимальный набор и оценивание: инженерный вывод

1. **Calibration:** будущая выборочная загрузка `0_tr1`+`4_tr1`; один фиксированный config по камере. Не изменять polygon по конкретному тестовому человеку. Настроить разрешённую дорожку, пересекаемые рабочие участки, транспортный corridor, footpoint anchor. Это image-space rule; размер в метрах не требуется.
2. **Review/development pair уже на диске:** `0_te23`+`4_te1`. Эти файлы после настоящего анализа нельзя представлять как слепой test. Из официальных оставшихся test clips выбрать закрытый holdout, предварительно подтвердив оригинальные timestamps и отсутствие смежного эпизода из train. Сохранить официальный split как происхождение, не как гарантию camera generalization. Съёмки того же ракурса — scene controls; для межкамерного теста нужен другой реально размеченный view.
3. **Actor annotation:** id, visible interval, footpoint reliability, allowed/forbidden/unknown, initial occupancy, actual crossing start/end; occlusions, разрешённая работа у машины. Число positive/negative episodes по ручной разметке, не просто число class-labelled clips. Каждый ROI/version фиксируется до holdout. Перепроверить полную траекторию всех людей, не только сохранённые stills.
4. **Proximity extension:** отдельная person+forklift нейросеть → class-specific tracks → подтверждение движения машины → relative image-distance/overlap proxy. Оператор forklift внутри кабины не является отдельным пешеходом. Image bbox включает вилы/груз неоднозначно; ground footprint техники лучше центра bbox. Состояния `unknown` при потере ног/машины/камеры; отсутствие detection не означает safe.
5. **Temporal state:** outside→candidate→active→clear, hold в секундах PTS; единый episode UUID camera+rule+actor (для proximity пара actor/machine), одна запись при active, реарм после устойчивого выхода. ID switch/короткую окклюзию склеивать ограниченным TTL, не бесконечным blacklist; различать новое событие второго человека. Пороги hold/clear — tuning parameters, эффективности пока нет.

#### Controls, которые нужны до заявления об успешной проверке

| Проверка | Positive | Negative/сложный control | Основной риск |
|---|---|---|---|
| Zone occupancy | target actor в запрещённом corridor | target на зелёной дорожке; законная работа у станка | scene-level label создаёт ложный GT для другого actor |
| Zone crossing | видимый переход разрешено→запрещено | движение вдоль края, возврат без перехода, вход с уже активным событием | jitter стоп, задержка/потеря быстрого транзита |
| Moving-machine proxy | видимые раздельные пешеход и движущийся forklift рядом | stationary forklift; только водитель; движение машины далеко; разные глубинные планы | без motion gate детектор близости выдаёт лишние alerts |
| Barrier | полностью видимый проход/перелаз с обеих сторон | разрешённые ворота/лестница, работа перед ограждением | 2D пересечение линии не доказывает перелаз |
| Dedup | продолжительное присутствие, уход и повторный вход | один эпизод с окклюзией/ID switch; два человека рядом | duplicate alerts либо ошибочное склеивание |

Для реальных moving-machine positives пока использовать видео организатора с правами или безопасную собственную постановку без настоящего сближения работающей тяжёлой техники. NVIDIA — отдельный synthetic control, явно помеченный. Самостоятельная съёмка не выполнена.

#### Где расстояние недоказуемо

Пиксельная близость двух bbox не задаёт метры: перспектива, высота объектов, части тела вне плоскости пола, скрытые стопы, неизвестные линзы/zoom. Из размера forklift нельзя без проверки вывести масштаб. Требуются фиксированная камера, измеренная плоскость пола и контрольные расстояния, homography/калибровка с ошибкой reprojection, надёжные ground anchors и известные timestamp. Даже homography пола не восстанавливает вертикальную проекцию подвешенного груза. Camera motion/pan/zoom требует новой калибровки. TTC по image trajectories — proxy, не время физического столкновения; симуляционные 3D annotations могут дать synthetic truth, но не калибровку реального CCTV. В проверенных Safe/Unsafe MP4 реальных размеров/калибровочных матриц не найдено.

<a id="F024"></a>
## F024 — Телефон: наличие/hold/use/context, exact COCO и UPT HOI

**Нормализованный статус и условия:** Phone bbox не доказывает use. UPT weight page открыта, payload/hash не получены. Device/executable phone-event test отсутствует. Числа W1 gate — предложения, не official acceptance.

**Источники:** [S046](SOURCES.md#S046), [S047](SOURCES.md#S047), [S075](SOURCES.md#S075), [S076](SOURCES.md#S076), [S215](SOURCES.md#S215), [S216](SOURCES.md#S216), [S217](SOURCES.md#S217), [S218](SOURCES.md#S218), [S219](SOURCES.md#S219), [S220](SOURCES.md#S220), [S221](SOURCES.md#S221), [S222](SOURCES.md#S222), [S223](SOURCES.md#S223), [S224](SOURCES.md#S224), [S225](SOURCES.md#S225), [S226](SOURCES.md#S226), [S227](SOURCES.md#S227), [S228](SOURCES.md#S228), [S229](SOURCES.md#S229), [S230](SOURCES.md#S230), [S231](SOURCES.md#S231), [S232](SOURCES.md#S232), [S233](SOURCES.md#S233), [S234](SOURCES.md#S234), [S235](SOURCES.md#S235).

**Происхождение:** [W1-04.md](_WORK/W1-04.md), `## Семантическая`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Семантическая граница

| Уровень | Доступное наблюдение | Что нельзя автоматически заключать |
|---|---|---|
| Наличие | bbox class cell phone в кадре | владелец, держание, использование |
| Ассоциация | телефон устойчиво около руки конкретного person track | звонок/ввод текста; соседняя рука может принадлежать другому |
| Держание | связанная рука и объект движутся согласованно | отвлечение: человек может просто переносить телефон |
| Вероятное использование | телефон у уха либо перед корпусом с характерными позами/HOI scores несколько кадров | активный звонок, чтение содержимого экрана, направление взгляда, разрешённость операции |
| Событие по правилу | использование совпало по времени с перемещением / заданной запрещённой рабочей зоной | фактическая опасная работа только из присутствия в ROI |
| Нарушение | событие удовлетворяет конкретному согласованному локальному запрету с исключениями | универсальное нарушение техники безопасности |

W1-04-F01 (инженерный вывод): даже достоверное использование телефона в зоне рабочего места может быть разрешённой операцией по наряду, сканированием или служебной связью. Нужна формулировка локального правила. ROI задаёт контекст запрета, но не доказывает, что станок работает или человек выполняет опасную операцию. Для MVP лучше выбирать **ходьбу**, потому что визуально подтверждаемое перемещение проще контекста «опасная работа».

**Происхождение:** [W1-04.md](_WORK/W1-04.md), `## Проверенные`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Проверенные первоисточники и версии

Все ссылки ниже открыты 2026-10-23; для GitHub API выполнен реальный GET.

#### W1-04-S01 — COCO class mapping, зафиксированный source tag

URL: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/cfg/datasets/coco.yaml ; локатор `names`, строки 15 и 82. Факт из исходника: person = **0**, cell phone = **67** в нулевой contiguous YOLO-нумерации. Это не native COCO category_id; нельзя напрямую передавать 67 как COCO JSON ID. GET https://api.github.com/repos/ultralytics/ultralytics/commits/v8.3.0 вернул commit **6e43d1e1e5db72afbf686dee6745669bcb124b0a**. Ни один из 80 классов не обозначает phone use или violation.

#### W1-04-S02 — конкретные доступные release assets

URL метаданных: https://api.github.com/repos/ultralytics/assets/releases/tags/v8.3.0 . Реальный ответ содержит:

| Файл | Размер из API, bytes | Точный URL |
|---|---:|---|
| yolov8n.pt | 6549796 | https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt |
| yolov8s.pt | 22588772 | https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt |
| yolov8n-pose.pt | 6832633 | https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt |

Поле digest в полученных asset metadata отсутствовало/None. Это подтверждает **листинг опубликованного файла**, а не успешное скачивание, SHA-256 или корректность весов. Не смешивать release tag assets с commit исходников ultralytics. Перед использованием скачать один выбранный файл, зафиксировать хеш, model.names и экспортную форму. Официальное описание семейства: https://docs.ultralytics.com/models/yolov8/ ; это живая страница, поэтому реализацию намеренно привязали к v8.3.0, а не текущему main.

#### W1-04-S03 — preprocessing

URL: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/engine/predictor.py ; `BasePredictor.preprocess`, строки 103–119 и `pre_transform`, 128–140. Для numpy-входа: LetterBox, BGR→RGB, BHWC→BCHW, contiguous, float/half и деление на 255. Tensor input уже предполагает подготовку вызывающей стороной. URL: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/data/augment.py ; `LetterBox`: resize с сохранением пропорций и padding. Для воспроизводимого экспорта предложен фиксированный квадрат 640×640, batch 1, RGB float32 [0,1]; отдельно хранить ratio/pad для возврата bbox и crop в исходные координаты. Параметры auto/stride должны совпасть у CPU baseline и LinQ.

#### W1-04-S04 — I/O и экспортный путь

URL: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/nn/modules/head.py ; `Detect.forward`, `_inference`, `decode_bboxes`, строки 54–109 и 122–124. Выход обычного detection head объединяет decoded xywh с sigmoid class scores. Инженерно ожидаемая форма для COCO 640×640 и strides 8/16/32 — **[1,84,8400]**, без отдельного objectness: 4 + 80. Это вывод из архитектуры, **не измеренная форма реально экспортированного файла**. Не применять decoder YOLOv5 с 85 каналами.

URL: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/engine/exporter.py ; `export_onnx`, таблица formats. Наличие ONNX exporter подтверждено исходником. Предлагаемый будущий smoke command: `yolo export model=yolov8n.pt format=onnx imgsz=640 batch=1 dynamic=False simplify=False opset=13` (opset уточнить по LinQ). NMS и возврат координат выполнить на host, если compiler это допускает. Экспорт не запускался; наличие команды не подтверждает поддержку LinQ. Операторы, layout, quantization calibration, DFL/decode, precision и host-device copies требуют проверки SDK.

#### W1-04-S05 — pose, её предел

URL: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/cfg/datasets/coco-pose.yaml ; `kpt_shape: [17,3]`, class person=0. Имена стандартных точек сверены с https://docs.ultralytics.com/datasets/pose/coco/ (`kpt_names`): zero-based nose=0, ears=3/4, elbows=7/8, wrists=9/10, ankles=15/16. Pose даёт запястья, **не пальцы и не взгляд**. Для обычного pose head ожидается 4+1+17×3=56 каналов (при стандартной pose-конфигурации); фактический экспорт надо инспектировать отдельно. Второй весовой файл и второй inference увеличивают риск LinQ и задержку.

#### W1-04-S06 — прямой HOI-кандидат UPT

URL: https://github.com/fredzzhang/upt ; `README: Model Zoo, Inference, Prerequisites, License`. GET https://api.github.com/repos/fredzzhang/upt/commits/main вернул **192743045e4c5f6827299fdc15809f5b97ac1b8e**. Репозиторий архивирован 2025-05-28. Авторы публикуют UPT-R50/HICO-DET, checkpoint filename `upt-r50-hicodet.pt`; веса содержат DETR. Авторский inference 0.042 s относится к RTX3090, не LinQ. Зависимости включают Pocket, DETR и старую PyTorch-рекомендацию 1.9.0. Ссылка на вес реально открыта: https://drive.google.com/file/d/1lvopTC_JlGHdKOyyEZTUp2VtFfCQ-08z/view?usp=sharing ; инструмент увидел страницу входа, **прямое скачивание и размер не подтверждены**. Код BSD-3-Clause подтверждён https://raw.githubusercontent.com/fredzzhang/upt/192743045e4c5f6827299fdc15809f5b97ac1b8e/LICENSE ; отдельная лицензия checkpoint не установлена.

#### W1-04-S07 — точная семантика HOI и интерфейс

URL: https://raw.githubusercontent.com/fredzzhang/upt/192743045e4c5f6827299fdc15809f5b97ac1b8e/assets/actions.txt . Нулевые action IDs HICO: hold=36, read=73, talk_on=101, text_on=103, no_interaction=57. V-COCO имеет иной список: talk_on_phone instr=10; HICO action IDs нельзя переносить туда.

URL: https://raw.githubusercontent.com/fredzzhang/hicodet/9dd59c1/instances_test2015.json . Прочитан JSON аннотаций 3,349,156 bytes по дереву GitHub; изображения не скачивались. Метаданные автора дают object 67=`cell_phone`, correspondence triples `[interaction,object,verb]`: `[283,67,8] carry`, `[284,67,36] hold`, `[285,67,73] read`, `[286,67,75] repair`, `[287,67,101] talk_on`, `[288,67,103] text_on`, `[289,67,57] no_interaction`. Это **нулевые** IDs данного wrapper, не 1-based бумажный список.

URL: https://raw.githubusercontent.com/fredzzhang/upt/main/inference.py ; `visualise_entire_image`, строки 45–63: выход включает boxes, pairing, scores, objects, labels, size. Требуется фильтровать **и object=67, и нужный verb**, а не только общий talk_on. URL: https://raw.githubusercontent.com/fredzzhang/upt/main/utils.py ; `DataFactory`, строки 63–86: test resize short side 800/max_size1333, ToTensor, ImageNet normalization mean [.485,.456,.406], std [.229,.224,.225]. Источники main открыты до фиксации SHA; для реализации использовать зафиксированный выше commit и сверить diff. Переменное число proposals, пары и postprocessing означают дополнительную работу для статического compiler; экспорт на LinQ не найден/не проверен.

#### W1-04-S08 — данные и права

URL: https://umich-ywchao-hico.github.io/ ; `Task 2, Dataset`: HICO-DET — статические изображения и пары human/object boxes с классом взаимодействия, версия 20160224. Это полезный словарь различий holding vs talking/texting, **не готовая промышленная CCTV-video проверка**. Авторская ссылка списка HOI открыта, но Drive отдал login, поэтому mapping получен из S07. Права на исходные изображения/redistribution и отдельная лицензия весов не установлены. Для демонстрации предпочтительны собственные постановочные безопасные записи с разрешением участников.

Ultralytics code license: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/LICENSE — AGPL-3.0. Отдельное актуальное заявление владельца о pretrained models: https://www.ultralytics.com/license (`FAQ: Are Ultralytics YOLO trained models licensed under AGPL-3.0?`) — default AGPL-3.0; Enterprise предлагается для proprietary use. Это сведения издателя, не заключение о конкретном распространении командного продукта. Dataset source https://cocodataset.org/#termsofuse открылся как JS-оболочка без содержательных terms, потому **не утверждаем**, что все COCO изображения автоматически имеют лицензию аннотаций. Code, weights, annotations, images, demo video — отдельные артефакты прав.

**Происхождение:** [W1-04.md](_WORK/W1-04.md), `## Варианты`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Варианты реализации

#### A. Минимальный условно рекомендуемый: detector + association + temporal movement rule

1. Реальный YOLOv8n inference на LinQ для person/phone (host-filter classes 0,67). Это минимизирует число нейросетей; рост качества small phone у `s` — гипотеза, а не гарантия.
2. Tracking person; phone bbox привязать не по одному overlap с торсом, а с учётом пространственного положения, устойчивости связи, совместного движения и отсутствия конкурирующего владельца. При двух близких людях результат ambiguous, событие не подтверждать.
3. Дополнительная pose-сеть на том же crop/кадре при наличии ресурса: телефон около wrist и ear для паттерна звонка; перед торсом около руки — лишь hold/use candidate. Head tilt без видимого телефона не достаточен. Без pose честная формулировка слабее: «телефон связан с перемещающимся человеком», а не «читает телефон».
4. Перемещение по сглаженной траектории footpoint/центра нижней части bbox за окно времени. Нормировать на высоту человека и проверять шум, либо использовать homography только при калибровке плоскости пола. Стабильная камера обязательна; пиксели/сек не метры/сек. Перенос phone у бедра — обязательный отрицательный контроль использования, хотя правило полного запрета держать телефон могло бы трактовать иначе.
5. Событие — одновременное временное пересечение use evidence и movement в запрещённой зоне; телефон раньше ходьбы и ходьба после убирания телефона не событие.

**Ограничение:** one-network вариант доказывает detector+rule, но не полное действие phone use. Нельзя подменять требуемый исходный сценарий наличием телефона без явного ограничения заявляемой функции.

#### B. HOI UPT-R50 + tracking/movement/ROI

Преимущество: модель обучалась различать carry/hold/read/talk_on/text_on и выдаёт связку person-object. Более прямая семантика, чем bbox. Риски: checkpoint доступен только через не проверенный download, старые зависимости, DETR/transformer/переменные пары, неизвестный экспорт и compiler. Для двухдневного MVP это **исследовательский резерв**, не критический путь. Даже идеальный HOI в одном кадре требует времени, контекста и дедупликации.

#### C. Не выбранные пути

- Один generic phone bbox → violation: отвергнут, семантически неверен.
- Только pose/head-down → phone use: отвергнут, одинаковые позы у инструмента, наряда, руки у лица; нет object identity.
- Generic video action recognition без проверенного phone-use class/checkpoint: не выбран. Не установлена end-to-end цепочка до LinQ и person-level события; clip class может смешивать нескольких людей.
- Случайный Roboflow/HF custom phone detector: не выбран в этой ветке без card, лицензии, точного checkpoint и external test. Название проекта phone-use не является доказательством action classification.
- Fine-tuning с нуля: против цели быстрого research/MVP; small object adaptation может понадобиться позже.

**Происхождение:** [W1-04.md](_WORK/W1-04.md), `## Состояние`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Состояние события и ошибки

W1-04-F02: предлагаемый, **не валидированный** автомат на person track: CLEAR → CANDIDATE → ACTIVE → RECOVERING → CLEAR. Начальное окно: 2 секунды с sampling 5–10 Hz, наличие use+movement не менее 60% валидных наблюдений; максимальный допустимый gap 0.5 s. Это только стартовые настройки smoke-test, не универсальные нормы безопасности. Держать minimum observation duration и fraction отдельно от FPS, использовать timestamps.

ACTIVE создаёт один event_id; последующие кадры обновляют evidence/last_seen, не создают сообщения. При пропаже телефона из-за короткой окклюзии сохранять episode, но не накапливать положительное evidence. Снять ACTIVE после 2 s явного отсутствия паттерна или выхода из зоны; rearm после подтверждённого завершения. Потеря track-ID не означает новый инцидент: краткое сопоставление с прошлым person track по времени/позиции, при неоднозначности flag для оператора. Смена камеры не решена без re-ID; никакой гарантии глобального dedup.

FP: рация у уха, сканер штрихкодов, пульт/калькулятор, тёмный инструмент, печатный наряд, чужой телефон за рукой, человек держит телефон при ходьбе без использования, allowed service phone, ошибка tracker/камера двигается. FN: маленький телефон после downscale, рука/перчатка/спина закрывают объект, блеск/тёмный корпус, motion blur, редкий sampling, crowd, hands-free use. Видимость недостаточна → unknown, а не «нарушения нет».

Численный пример small object — **геометрический расчёт**, не benchmark: телефон шириной 18 px на 1920-wide кадре станет примерно 6 px при resize до 640; upsample crop уже потерянных деталей их не восстановит. Персональный crop из **исходного** high-resolution кадра может сохранить сигнал, но добавляет inference/очередь/преобразование координат. Никакой гарантированной минимальной ширины телефона здесь не установлено.

<a id="F025"></a>
## F025 — Action donors: AVA person labels/SlowFast, NTU phone, Smoker/HMDB

**Нормализованный статус и условия:** AVA rows не скачанные/просмотренные movie clips; join walk14 с phone15/57 не выполнен. Numeric source IDs не переносить на head без loader. Smoker image-only, NTU access approval; licenses кода/annotations не очищают исходные фильмы.

**Источники:** [S106](SOURCES.md#S106), [S236](SOURCES.md#S236), [S237](SOURCES.md#S237), [S238](SOURCES.md#S238), [S239](SOURCES.md#S239), [S240](SOURCES.md#S240), [S241](SOURCES.md#S241), [S242](SOURCES.md#S242), [S243](SOURCES.md#S243), [S244](SOURCES.md#S244), [S245](SOURCES.md#S245), [S246](SOURCES.md#S246), [S247](SOURCES.md#S247), [S248](SOURCES.md#S248), [S249](SOURCES.md#S249), [S250](SOURCES.md#S250), [S251](SOURCES.md#S251), [S252](SOURCES.md#S252), [S253](SOURCES.md#S253), [S254](SOURCES.md#S254), [S255](SOURCES.md#S255).

**Происхождение:** [W1-11.md](_WORK/W1-11.md), `## 2.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 2. Телефон: новые первичные пути и точное действие

#### W1-11-S01 — Google AVA Actions v2.2: person-action labels с конкретными клип-локаторами

Первичные страницы: [официальный download/schema/license](https://sites.research.google/gr/ava/download/), [официальная карта 80 действий](https://research.google.com/ava/download/ava_action_list_v2.2.pbtxt), [описание movie clips](https://sites.research.google/gr/ava/). Версия v2.2, дата доступа 23.10.2026.

**W1-11-F04 / D/A.** Лично получен HTTP200 небольшой [ava_val_v2.2.csv.zip](https://research.google.com/ava/download/ava_val_v2.2.csv.zip), **1 611 664 B**; разобран один member `research/action_recognition/ava/website/www/download/ava_val_v2.2.csv`. Строки хранят `video_id,timestamp,x1,y1,x2,y2,action_id,person_id`; координаты нормированы, timestamp — секунда исходного YouTube. Это person boxes с multilabel действиями, **не bbox телефона/сигареты**. Google публикует CC BY4.0 для данных; отдельные права фильмов/их публичного показа здесь не установлены. Исходные media не получены.

Проверенная выборка **всего val CSV**, не число независимых эпизодов:

| Source ID | Буквальный класс | Число строк | Первый встретившийся точный локатор `video,timestamp,bbox,person` |
|---|---|---:|---|
| 15 | `answer phone` | 1113 | `5BDj0ow5hnA,0997,[.146,.600,.186,.796],114` |
| 57 | `text on/look at a cellphone` | 127 | `5BDj0ow5hnA,1345,[.555,.237,.707,.621],409` |
| 54 | `smoke` | 707 | `5BDj0ow5hnA,1362,[.161,.317,.299,.779],430` |
| 20 | `climb (e.g., a mountain)` | 76 | `2PpxiG0WU18,1663,[.160,.022,.441,.761],193` |

Видео-локаторы: [phone call t997](https://www.youtube.com/watch?v=5BDj0ow5hnA&t=997s), [cellphone t1345](https://www.youtube.com/watch?v=5BDj0ow5hnA&t=1345s), [smoking t1362](https://www.youtube.com/watch?v=5BDj0ow5hnA&t=1362s), [climb t1663](https://www.youtube.com/watch?v=2PpxiG0WU18&t=1663s). **Это реконструированные ссылки по author labels; их нынешняя доступность, видео-содержимое и media rights не проверены.** Не выдавать за лично просмотренные позитивные клипы.

**W1-11-F05 / I/P.** Для use-while-walking следует join по тому же `video,timestamp,person_id,bbox` с AVA14 `walk`, а не комбинировать действия двух людей в кадре. Такой join здесь не выполнен; перечисленные phone rows сами по себе не доказывают ходьбу. Взять AVA27 `drink`,29 `eat`,48 `read`,56 `take a photo` как кандидаты confusers после проверки target-policy; отсутствие phone label не всегда доказательство полного negative. Группировать по исходному фильму/клипу, не случайным frames. Доменные разрывы: монтаж, крупные лица, реквизит/актёры, камера движется, отсутствие цехового СИЗ и служебных сканеров/раций. Полезно для action semantics и ограниченного сравнения, непригодно как заводской holdout.

#### W1-11-S02 — MMAction2 AVA SlowFast: действительно найденный checkpoint, но тяжёлая цепочка

Зафиксированный commit **`a5a167dff2399e2d182a60332325f9c0d4663517`**. Лично прочитаны [metafile](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/configs/detection/slowfast/metafile.yml), [config](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/configs/detection/slowfast/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb.py), [label_map](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/tools/data/ava/label_map.txt) и [AVA loader](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/mmaction/datasets/ava_dataset.py).

**W1-11-F06 / A.** Точный [checkpoint](https://download.openmmlab.com/mmaction/v1.0/detection/slowfast/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb/slowfast_kinetics400-pretrained-r50_8xb6-8x8x1-cosine-10e_ava22-rgb_20220906-d934a48f.pth): HEAD200, Content-Length **135 802 749 B**, веса не скачаны. Config: RGB temporal input, `SampleAVAFrames(clip_len=32,frame_interval=2)`, test resize short side256, `NCTHW`, mean `[123.675,116.28,103.53]`, std `[58.395,57.12,57.375]`; FastRCNN с ResNet3dSlowFast и RoIAlign, multilabel head **81 channels с background0**. Нужны внешние person proposals. Это не одно RGB изображение YOLO.

**Class mapping:** без `custom_classes` AVA loader индексирует label по **исходному ID**; интересующие outputs **15,20,54,57**, не нулевые позиции в файле из 60 строк. При `custom_classes` loader создаёт `[0]+custom_classes` и remap через `.index`; такой другой checkpoint/config требует другой карты. API code license Apache2.0 подтверждена; отдельное точное лицензирование pretrained checkpoint и исходных фильмов не установлено этим чтением. ONNX/actual graph I/O/LinQ export не проверены. Модель — резерв action experiment, не рекомендуемый быстрый LinQ baseline.

#### W1-11-S03 — NTU RGB+D / 120: постановочные phone actions с modality и approval gate

[Официальный ROSE Lab](https://rose1.ntu.edu.sg/dataset/actionRecognition/), §§1–3, версия NTU60/120, accessed23.10.2026. **W1-11-F07 / D/C:** нужные source labels **A028 `phone call`, A029 `play with phone/tablet`**; близкие negatives **A001 drink water, A011 reading, A032 taking a selfie, A037 wipe face, A041 sneeze/cough, A044 headache**. Нулевая модельная позиция только после выбранного loader: A028 обычно27, A02928, но нельзя присваивать без его проверки. Страница всех120 классов не содержит smoke/cigarette: не использовать как smoking-positive dataset.

Автор указывает KinectV2 RGB1920×1080, depth/IR512×424, 25-joint 3D skeletons. Для доступа требуются account, request form, Release Agreement и одобрение; RGB60 —136GB, расширение ещё124GB. Никаких account/заявок не создавалось, конкретный AVI payload/terms agreement не получен. Это контролируемое исполнение действий, не промышленные инциденты. Статичный actor phone action не устанавливает use при ходьбе. Пригодно как будущий action donor/постановочные confusers, непригодно как немедленный свободный video bundle или открытая лицензия «на всё».

**Происхождение:** [W1-11.md](_WORK/W1-11.md), `## 3.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 3. Курение: action, cigarette и дым разделены

#### W1-11-S04 — Mendeley Smoker v1: доступные изображения с нужными confusers

[Первичная карточка j45dj8bgfc/1](https://data.mendeley.com/datasets/j45dj8bgfc/1), Ali Khan,15.08.2022, DOI10.17632/j45dj8bgfc.1, CC BY4.0. **W1-11-F08 / D:** карточка задаёт 1120 картинок250×250: `Smoking`560/`NotSmoking`560. Заявлены web-search изображения и похожие жесты non-smokers: питьё, ингалятор, телефон, кашель. Source numeric IDs не задаются: сортировка папок конкретным loader может поменять индекс. Данные image classification; карточка не даёт cigarette boxes, person tracks или timestamps. Сам архив в этой ветке не скачан; соседний datasets сообщает свой полный decode, это не повторённая проверка.

Условно usable для crop classification/ручной подборки жестовых negatives. Неusable как видео для события, для оценки tiny cigarette в full-frame CCTV или доказательство industrial quality. Resize250×250 уже изменил масштаб/контекст: crop accuracy нельзя переносить на 1920-wide кадр с маленьким лицом. Карточка CC BY не подтверждает очищенные права каждого найденного поиском фото/публичного demo. Для демонстрации предпочтительнее собственные/организаторские разрешённые кадры.

#### W1-11-S05 — Zhang et al. Electronics12,3225: сильная локализация, но не готовый download

[Первичная статья](https://www.mdpi.com/2079-9292/12/15/3225), DOI10.3390/electronics12153225,2023, §§method/data availability. Direct web open429; прочитаны индексированные первичные excerpts, полный dataset payload не получен. **W1-11-F09 / C/U:** метод связывает лицо, руку, сигарету/телефон и behavior region. Это точнее семантически, чем fire dataset. В соседнем datasets полный текст устанавливает данные по разумному запросу; здесь публичные exact download/LabelMe numeric mapping/checkpoint/license/video intervals не найдены. Не выдумывать порядок классов из порядка слов статьи. Кандидат для будущего donor-запроса, отвергнут как зависимость на оставшиеся два дня. Запрос автору не отправлялся.

#### W1-11-S06 — HMDB51: настоящие smoke/climb labels, но film clips и разные представления

[Первичная страница Serre Lab](https://serre.lab.brown.edu/hmdb51.html), accessed23.10.2026, official unstabilized release. Автор перечисляет smoke, climb, climb stairs и confusers eat/drink/chew/talk; предоставляет51-class видео и3 splits, заявляет CC BY4.0. [Официальный video download ID](https://drive.google.com/uc?export=download&id=17anw5Oxp7lmp9cMwXPOyOpL5olDLmPpj), [split download ID](https://drive.google.com/uc?export=download&id=1NQxJWJSYWefyNS-LFYCenFih4gRDUPCX). Web redirect download не открылся; ~2GB не загружались. Права каждого movie/web source отдельно не проверены.

**W1-11-F10 / A/I:** прочитан [MMAction2 HMDB label_map](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/tools/data/hmdb51/label_map.txt). Нулевые позиции **5=climb,6=climb_stairs,40=smoke**; negatives **3=chew,10=drink,11=eat,46=talk**. Это именно mapping MMAction, не универсальные IDs любой HMDB-сборки. У W1-06 есть exact PoseC3D HMDB checkpoint; прочитанный здесь metafile тоже его перечисляет. Но skeleton-only модель не видит cigarette identity: smoke class не превращает её в small cigarette detector. Подходит для ограниченного action comparator/позовых confusers; не для независимой проверки smoking-vs-phone на заводе. Stabilized/unstabilized — одни и те же клипы, нельзя разносить между train/test.

#### W1-11-S07 — Конкретные веса сигареты из W1-05: преемственность, не новая проверка бинарника

Соседний W1-05 лично анализировал [cgr_detection/models/last.onnx](https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/models/last.onnx), commit`4a45c911cea365d7d196c2276611749ce5f3180b`. Его результат: class0 `cigarette`, ONNX12 238 102B, embedded AGPL3.0 при MIT code. **W1-11-F11 / attributed A:** пригодный для самостоятельного smoke-test кандидат, но не доказанный smoking action. Provenance/качество остаются открыты; не надо заново объявлять сторонний `judge_smoke` истиной. Нет exact licensed industrial demo video. Для readiness — сначала small-object recall/FP на телефоне, ручке, соломинке, инструменте, паре и губах без сигареты. Сама передача сигареты, удержание у бедра и курение — разные labels.

<a id="F026"></a>
## F026 — Открытое пламя: пять actual videos, XML defects, два exact weights, policy и права

**Нормализованный статус и условия:** Самостоятельный кандидат части сценария4: visible flame outside allowed ROI, не smoking. Rabahdev предпочтён по provenance readiness после binary names, не по измеренной точности/скорости. FURG CC0/FIRESENSE CC BY сохранены наряду с third-party watermark/title risk.

**Источники:** [S076](SOURCES.md#S076), [S079](SOURCES.md#S079), [S256](SOURCES.md#S256), [S257](SOURCES.md#S257), [S258](SOURCES.md#S258), [S259](SOURCES.md#S259), [S260](SOURCES.md#S260), [S261](SOURCES.md#S261), [S262](SOURCES.md#S262), [S263](SOURCES.md#S263), [S264](SOURCES.md#S264), [S265](SOURCES.md#S265).

**Происхождение:** [W2-06.md](_WORK/W2-06.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Проверено 23.10.2026. Вопрос решения: есть ли у fire route проверяемые media/labels/weights/rights, позволяющие конкурировать за третье место с behavioral alternatives, а не выдавать ещё одну generic zone за исходное нарушение? **Да — как условный кандидат «видимое пламя вне разрешённой области». Нет — как уже измеренно готовое LinQ-решение; smoking не реализован.** В этой ветке получены реальные bytes пяти видео и двух PT; декодированы все кадры, просмотрены все покадровые листы и увеличенные спорные кадры. Модель не загружалась, NN inference/export/compile не выполнялись, чужой код не исполнялся.

Входы прочитаны: W1-05 целиком; релевантные S09/S10/F27 W1-11 и S13–17/R5 W1-16 вместе с остальным контекстом файлов; исходная критика K007/K008/K001 из PROMPT_W2-06. Артефакты сохранены в [W2-06_evidence](_WORK/W2-06_evidence/). Скрипты собственные, только bounded HTTP, ZIP/pickletools disassembly, XML и PyAV/PIL decode. Нет torch.load/pickle.load, установки зависимостей или приложения. HTTP manifests содержат точные URL; source/license файлы сохранены локально.

#### Новые первичные источники и тип доказательства

- **W2-06-S01:** [FURG pinned repository](https://github.com/steffensbola/furg-fire-dataset/tree/6aff09d7baa27425f31d1df685284c26cbffe7af), commit `6aff09d7baa27425f31d1df685284c26cbffe7af`. Новый полный GET `Car1.mp4/xml`, `non_fire_patrolbot_onboard.mp4/xml`, `barbecue.mp4/xml`, README, LICENSE; все HTTP200. [downloads.json](_WORK/W2-06_evidence/downloads.json), [tree.json](_WORK/W2-06_evidence/tree.json), [decode_manifest.json](_WORK/W2-06_evidence/decode_manifest.json). README прямо задаёт OpenCV Rect(x,y,width,height), semantic flame. Это источник разметки, не quality certificate.
- **W2-06-S02:** [FIRESENSE v1 / DOI10.5281/zenodo.836749](https://zenodo.org/records/836749), опубликовано 31.07.2017. Новый GET primary API сохранён как [firesense_record.json](_WORK/W2-06_evidence/firesense_record.json). License `cc-by-4.0`. Реальные bounded HTTP206 из [fire_videos.1406.zip/content](https://zenodo.org/api/records/836749/files/fire_videos.1406.zip/content): central directory и только два выбранных member payload. [firesense_range.json](_WORK/W2-06_evidence/firesense_range.json), [firesense_members.json](_WORK/W2-06_evidence/firesense_members.json), [firesense_acquired.json](_WORK/W2-06_evidence/firesense_acquired.json). Полный 622676845B ZIP не скачан; его MD5 не объявляется проверенным.
- **W2-06-S03:** [rabahdev card revision13017fe8…](https://huggingface.co/rabahdev/fire-smoke-yolov8n/blob/13017fe8af477c25f5298d168e2dfede4b000753/README.md), [exact PT](https://huggingface.co/rabahdev/fire-smoke-yolov8n/resolve/13017fe8af477c25f5298d168e2dfede4b000753/best.pt). Новый full GET+SHA, static ZIP data.pkl disassembly, card/API. [rabah_best_dis.txt](_WORK/W2-06_evidence/rabah_best_dis.txt), [checkpoint_static.json](_WORK/W2-06_evidence/checkpoint_static.json), [metadata_locators.json](_WORK/W2-06_evidence/metadata_locators.json).
- **W2-06-S04:** [farhat exact card](https://huggingface.co/farhatullah0066/yolov8n-fire-smoke-detection/blob/e4f808eb87d72b53ccc860c007f564baf174540a/README.md), [PT revisione4f808eb…](https://huggingface.co/farhatullah0066/yolov8n-fire-smoke-detection/resolve/e4f808eb87d72b53ccc860c007f564baf174540a/best.pt). Новый full GET+SHA и независимая static disassembly; [farhat_best_dis.txt](_WORK/W2-06_evidence/farhat_best_dis.txt). Card всего26B, сообщает AGPL, не training report.
- **W2-06-S05:** лично получены source files `pyproject.toml`, `LICENSE`, `ultralytics/engine/exporter.py`, `ultralytics/nn/modules/head.py`, `ultralytics/data/augment.py` для [v8.4.51](https://github.com/ultralytics/ultralytics/tree/v8.4.51) и [v8.4.150](https://github.com/ultralytics/ultralytics/tree/v8.4.150). Все GET200, [sources.json](_WORK/W2-06_evidence/sources.json). Это versioned source, не исполнявшееся окружение. GitHub refs дали annotated tag objects `1276a9ba01aff9b7ed659359b749e2621f8c8f77` и `f2b6bdf40f6581605f5ba34c592495deea8631b7` соответственно — не выдаются за commit SHA. Source hashes в [artifact_hashes.json](_WORK/W2-06_evidence/artifact_hashes.json).
- **W2-06-S06:** [R3-E6 release](https://github.com/Supakorn289/fire-smoke-detection-r3e6/releases/tag/v1.0.0-r3e6) открыт заново; новый recursive tree exact commit `676f3280cf643f874ae6f12b41a4a412409d2830` HTTP200 сохранён [r3e6_tree.json](_WORK/W2-06_evidence/r3e6_tree.json). Во всём дереве нет путей с license/copying/notice. Это более конкретный negative result, чем W1 root LICENSE404; не доказывает отсутствие любого разрешения вне дерева. Готовый ONNX остаётся deployment reference, не выбранной лицензированной поставкой.

#### W2-06-F01 — Полученное media, decode и визуальная семантика

Все FURG видео H264, decoded rate `2997/100`, time_base `1/29970`, PTS0=0, шаг1000 ticks; все прочитаны до EOF без исключения. Header XML `frameRate=29` не использовать для временных порогов. Покадровые CSV сохраняют реальный PTS; индексы здесь с нуля.

| Реальный файл | Bytes / SHA256 | Decode | Наблюдение всех кадров |
|---|---|---|---|
| Car1.mp4 | 18200338 / `52c000a9257ad1e3e84ea29f5be0d7d5e2b1a4c3ed41d86a243640868b2fc92a` | 854×480;630frames; lastPTS20.987654s | Горящий перевёрнутый автомобиль, крупные жёлто-оранжевые языки и чёрный дым. Монтажная смена планов на246,379,443. Пламя присутствует на протяжении; это не ignition/onset→cessation clip. |
| non_fire_patrolbot_onboard.mp4 | 10668507 / `b3e59cf1d8f4916727bc459a0b7c09d5ddfde4b8f0440b9586944abfda7d890c` |1280×720;341frames;lastPTS11.344678s | Низкая мобильная камера, люди, выставочные стенды, яркие потолочные светильники. Видимого пламени ни на одном листе не обнаружено. Frames0–239 — scene;240–244 fade;245–340 IEEE Spectrum outro. Не считать весь runtime отрицательными CCTV-секундами. |
| barbecue.mp4 |31823966 / `5ebaf97bd9cea68804d3da5872de778261c23a7ff8ae6299d8830e0f3fcafb60` |1280×720;902frames;lastPTS30.063397s | Крупное пламя в небольшой жаровне/кирпичном очаге, рядом руки/человек; меняется интенсивность, появляются дым/угли и частичная окклюзия. Это естественный candidate для allowed-flame replay, но изображение не доказывает реальное разрешение огневых работ. |

Просмотрены все15 листов FURG: Car1 `0000/0150/0300/0450/0600`, negative `0000/0150/0300`, barbecue `0000/0150/0300/0450/0600/0750/0900`; увеличенные спорные кадры в `*_detail.jpg`. Листы содержат каждый decoded frame без временного subsampling, но thumbnail160px не гарантирует обнаружение очень малого огня. Вывод «видимого пламени не обнаружено» относится к этому просмотру, не ко всем физическим источникам/скрытым областям.

**FIRESENSE bounded alternative**: tail65536B, два local header по30B, затем compressed634310+2281822B, итого **2981728B Range bodies**, а не весь архив. CRC32 обоих decompressed members совпал с central directory; полные member hashes получены нами. Это не проверка archive MD5 и не независимости от training data.

| Exact member | Реальные bytes/SHA256 | Полный decode и просмотр |
|---|---|---|
|`pos/posVideo11.870.avi` |660282 / `37a3c9ff44fd568a3e517a866e0f2f187fbda7c9932b55d09b463be638ead42e` | MPEG4,400×256,15fps,timebase1/15,178frames,lastPTS11.8s. Малые очаги вдоль лесной опушки, люди рядом, watermark UltimateChase.com. Пламя видно с начала и до конца; заявленный pos согласуется с визуальной семантикой. |
|`neg/negsVideo2.859.avi` |2418108 / `4ba3a1bdfb199ad18191d3c306bb476b593fa07c1bdb34b6028c9008c8b2d5df` | MJPEG,320×240,10fps,timebase1/10,155frames,lastPTS15.4s. Ночная улица, движущиеся автомобили, яркие фары/отражения. Видимого пламени не обнаружено во всех155 кадрах. Это **полезный confuser**, а не только пустая комната. |

Все333 FIRESENSE frames декодированы до EOF, просмотрены четыре all-frame sheets `posVideo11.870_0000/0100` и `negsVideo2.859_0000/0100`. Эти два member не имеют в найденной поставке bbox/XML или точных event intervals. Folder pos/neg — video-level flame semantics, не числовая smoke/fire map. FIRESENSE smoke ZIP не получен: **smoke-only positive/control тут не доказан**.

#### W2-06-F02 — XML: геометрия подтверждена, perfect GT опровергнут

FURG XML содержит OpenCV `x,y,w,h` в исходных pixels, top-left; не normalized YOLO и не xyxy. Car1 frame0 `[260,97,288,293]` → xyxy `[260,97,548,390]`; overlay попадает на flame region, не на весь plume. На all-frame sheets наложены все XML boxes; source schema согласована с primary README. Numeric detector class нет; canonical mapping только `flame → fire`, smoke labels из XML не извлекаются.

Полный parse дал:

| Файл | Decoded indices | XML indices | Nonempty / empty | Ошибка/ограничение |
|---|---|---|---|---|
|Car1|0…629|0…630|631 /0|Extra630 без decoded frame; на склейке246 XML повторяет245 `[213,127,312,275]` и плохо покрывает новый план. На443 остаются два boxes предыдущего442, хотя план сменился. |
|negative|0…340|0…341|0 /342|Все XML annotations empty, теперь это проверено целиком; extra341. Empty не означает пригодный industrial control: почти треть runtime — outro. |
|barbecue|0…901|0…902|893 /10|Extra902. Empty596–602 и639–641; на596/602 и особенно640/641 увеличенный кадр содержит видимый огонь. Это конкретные пропуски разметки. |

На валидных decoded indices нет пропущенных XML indices и нет box за границами кадра. Это синтаксическая валидность, не semantic accuracy. Наличие boxes на frame0 и точных совпадений на других кадрах не устанавливает универсальный offset+1/−1: **не сдвигать всё видео для починки единичных монтажных stale boxes**. Для curated evaluation отрезать XML extra final row, использовать decoded index→PTS, самостоятельно переаннотировать локальные scene-cut/empty ошибки с сохранением original и delta. Это следующий шаг; original XML не переписан, «исправленная GT» не выдумана.

Отдельные монтажные планы Car1 нельзя использовать как независимые очаги/камеры при проверке once-per-episode. Нарезка возле склеек допустима только как явно производный материал с новым manifest. Ни один просмотренный flame clip не доказывает reset после реального затухания и новый onset: для полного event test нужны дополнительные разрешённые controls или честно маркированная replay-последовательность.

#### W2-06-F03 — Два exact checkpoint routes: теперь оба с actual bytes и внутренними names

| Свойство | A: rabahdev | B: farhatullah0066 |
|---|---|---|
|Revision|`13017fe8af477c25f5298d168e2dfede4b000753`|`e4f808eb87d72b53ccc860c007f564baf174540a`|
|PT bytes / наш SHA256|6229802 / `b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f`|6229546 / `0dbc9ded65f5c01455e37669338be0e3df688ade0873258017d62b550d0e964f`|
|Static data.pkl|105081B,365 ZIP members|104779B,365 ZIP members|
|Внутренние names|**0 smoke,1 fire**, offsets90151–90206|**0 smoke,1 fire**, offsets89645–89700|
|Embedded version/date|8.4.51;2026-05-20T11:46:55.561469|8.4.150;2026-09-13T11:11:36.442511+00:00|
|Внутренние train args / YAML|imgsz640;nc2;DetectionModel/Detect;C2f/SPPF/DFL|imgsz640;nc2;DetectionModel/Detect;C2f/SPPF/DFL|
|Weights grant evidence|Card AGPL3; embedded AGPL3 URL|Card AGPL3; embedded AGPL3 URL|
|Training provenance|Card: D-Fire,YOLOv8n COCO base,train/val/test; авторские заявления|Card практически пустая; provenance слабее|

Наша static проверка — `zipfile` и `pickletools.genops/dis`, не исполнение GLOBAL/REDUCE/BUILD. Списки references показывают зависимость сериализованного объекта от PyTorch и Ultralytics classes, но не заменяют runtime load. Строки names и keys с их BININT показаны в disassembly, а не выведены по расположению слов. SHA совпали с W1 LFS metadata, теперь это **полные собственные hashes**, а не publisher-only claims.

**Выбор по readiness:** для первого custom-model эксперимента **A rabahdev** теперь слегка предпочтительнее: раньше W1 отдавал B преимущество лишь за проверенный map; этот пробел у A снят, у A содержательнее training/provenance card, оба компактные и одинаковые labels. Это не превосходство precision, exportability, скорости или safety. B — конкретный второй candidate при проблеме environment/export A. Разница256B не обосновывает сравнение вычислительной скорости. Published mAP A не переносится на эти clips и не даёт сравнения с B.

Source route: сначала изолированная проверка соответствующей embedded версии8.4.51/8.4.150, с фактически записанным environment lock. Source pyproject A задаёт Python>=3.8, numpy>=1.23, opencv>=4.6, torch>=1.8 и исключение torch2.4.0 для Windows, torchvision>=0.9; export extras включают ONNX>=1.12 и onnxslim>=0.1.82. Это ranges, **не frozen environment checkpoint автора**. Для B читать свой pyproject, не наследовать defaults A. `export_onnx` и Detect source в обеих версиях существуют; готового ONNX в двух полученных HF repo API не найдено.

**Предлагаемый контракт, не observed graph:** static batch1,640² RGB FP32[0,1], явный letterbox transform с обратным переносом boxes, export без встроенного NMS, затем class-aware host NMS. Типичный v8 двухклассовый output `[1,6,8400]` — архитектурное ожидание, не измеренный I/O этих PT. Сначала actual exported names/shapes/operators/precision, потом decoder. Нельзя применить 84/85-only COCO runner к6 channels. Все preprocess/export/NMS параметры фиксировать явно; наличие `LetterBox`/`Detect` в source не доказывает, что точный graph успешно экспортируется.

R3-E6 имеет противоположный publisher map **0 Fire,1 Smoke**, fixed768 и опубликованный ONNX по W1. Отсутствие license paths в новом полном exact tree оставляет его reference, даже если он мог бы экономить экспорт. Не скачивался и не запускался здесь. При catalog-only быстрее сначала посмотреть **фактический catalog class map**, output contract и rights: если Fire есть, можно проверить этот detector без custom export; если только COCO/person, fire сценарий не готов, host zone не создаёт недостающий flame feature.

#### W2-06-F04 — Права по реальной поставке и действию

Это проверка evidence/grants, не юридическое заключение. Лицензия кода/весов не очищает каждый training image; отсутствие consent text не есть доказательство его отсутствия.

| Реальный объект / действие | Наблюдённое основание | Решение для поставки |
|---|---|---|
|A/B PT; исследование, последующий экспорт и использование|Оба издателя явно AGPL3 в card и embedded PT; versioned Ultralytics LICENSE AGPL3 получены|Не объявлять MIT. Сохранить AGPL текст, model URLs/revisions/SHA, notices; при распространении производного ONNX/compiled учитывать те же provenance/license obligations, не называть compiler output свободным от них. Командное решение об открытой AGPL поставке или отдельном разрешении остаётся перед публикацией. |
|Код интеграции + NN dependencies|Exact Ultralytics source AGPL; [позиция владельца](https://www.ultralytics.com/license) описывает AGPL и Enterprise|Code delivery/license review привязать к реальному способу публикации и связке; не утверждать автоматически «любой hackathon требует покупки». Наша собственная parser/decode работа не равна интеграции Ultralytics. |
|FURG выбранные MP4/XML, local research|Pinned repository CC0-1.0 LICENSE реально получен|Сохранить grant и attribution/provenance. CC0 — реальное основание, не «лицензии нет». Но negative содержит IEEE Spectrum `spectrum.ieee.org ©2012`, animation credit, что показывает third-party provenance. Per-video clearing для публичного воспроизведения/записи не установлено. Обрезка outro не автоматически снимает права на основной сюжет. |
|FIRESENSE extracted AVI, live replay/запись/републикация|Primary Zenodo record CC BY4.0; exact member identity CRC+SHA|Сильнее связь с конкретным лицензированным dataset, чем произвольный mirror. Сохранить creator metadata/DOI/version/license, имена members, source URL, пометку extraction/изменений. Positive имеет UltimateChase.com watermark: отдельное original-source разрешение не проверено. Negative без явного watermark на просмотренных кадрах, но это не доказательство отсутствия third-party rights. |
|R3-E6 code/weights/ONNX|No license/copying/notice path in pinned full tree; grant не установлен|Reference only, не переносить AGPL другой HF модели или MIT чужого repo на этот release. |

Предлагаемые точные credits для разрешённого использования: «FURG Fire Dataset — Steffens et al.; source github.com/steffensbola/furg-fire-dataset, commit6aff09d7…, files[имя], CC0-1.0 as published; XML overlays/curation by team». Для FIRESENSE: «Nikos Grammalidis, Kosmas Dimitropoulos, Enis Cetin — FIRESENSE database of videos for flame and smoke detection, v1 (31.07.2017), DOI10.5281/zenodo.836749, CC BY4.0 (https://creativecommons.org/licenses/by/4.0/); fire_videos.1406.zip member[имя]; extracted without transcoding; overlays/trim[если были] by team»; Creator names сверены с primary metadata и включены выше. Для A/B — точное repo/revision, SHA и AGPL3 notices. Не публиковать research evidence папку автоматически: она включает чужие видео и PT. Рекомендуемая публичная демонстрация: разрешённый собственный target replay/лицензированный конкретный клип плюс source/model notices; права этих источников оставить traceable, а не скрыть.

#### W2-06-F05 — Самостоятельный scenario contract и controls

**Наблюдаемая временная переменная:** `visible_flame_region` устойчиво подтверждается NN в наблюдённых кадрах и лежит вне camera-specific allowed flame ROI при действующей версии политики. Это свой визуальный класс и region episode, не person occupancy. Smoke выдаётся отдельно как `smoke_like_region`; не является подтверждением пламени или курения. Smoking/cigarette/hand-to-mouth не заявляются.

Конкретная проектная политика для fixed camera: production floor по умолчанию forbidden для открытого видимого огня; оператор заранее задаёт image-plane allowed ROI стационарного разрешённого очага и окно действующего разрешения. Flame bbox полностью внутри allowed ROI при действующем окне → detection сохраняется, violation не открывается. Flame outside или разрешение не действует → candidate incident; пересечение границы/плохая локализация → review/unknown, не скрытое разрешение. Нужны guard-band и правило перекрытия, калибруемые на target, без универсального численного порога. Не переносить дымовой plume centroid в источник пламени. Для мобильного FURG fixed polygon без motion compensation непригоден как реальное правило; использовать короткий стабильный план или только честную иллюстрацию политики.

Контроль **одинакового огня**: воспроизвести один короткий стабильный fragment barbecue с неизменными pixels и дважды применить разные versioned policies — ROI охватывает источник и active permit (expected no violation), затем permit inactive/ROI не охватывает источник (expected violation). Это policy replay, не доказанная заводская ситуация и не новый benchmark качества. Сейчас этот event engine не реализован. Не создавать реальный опасный огонь ради теста.

Положительный sustained flame: Car1 стабильный первый план0…245, без склейки. Negative/confuser: FIRESENSE night-headlights155frames и FURG scene0…239. Allowed positive detection/negative violation: barbecue. Отдельно нужны **steam/welding/dust/bright uniform/screen-fire**, smoke-only и реальное cessation/re-entry; выбранный пакет их не закрывает. Изменения flame shape/краткая окклюзия BBQ полезны для будущего hysteresis/dedup, но XML empty нельзя выдавать за реальные no-fire intervals.

Предложенный event path: valid flame detections→spatial association→persistent forbidden condition→один event_id/одно уведомление→обновления того же incident→close после наблюдаемого отсутствия с hysteresis. Frame drops/stream loss→unknown; не копить persistence по неувиденным кадрам. Два пространственно раздельных очага не склеивать общим cooldown. Episode delay считать по PTS и сохранять onset/confirm/source-age отдельно.

**Disclosure domain shift:** большие пожары автомобиля и близкая жаровня, лесной огонь, движущаяся низкая камера и ночная городская улица отличаются от фиксированного заводского CCTV. Нет измерения маленькой зажигалки, дальнего огня, сварки, quantized LinQ, industrial false alerts/hour. Возможное пересечение training D-Fire с этими публичными источниками не исключено; эти видео development controls, не доказанный независимый test split. Просмотр кадров/совпадение class map — semantic readiness, не качество модели.

#### Итог по K и ближайшее решение

| K | Статус | Что изменилось относительно W1 | Что осталось |
|---|---|---|---|
|K007|**scoped**|Media availability/decode/полная XML семантика теперь закрыты для конкретных clips; два weights реально получены; A names подтверждены. Добавлен night-headlight confuser и BBQ allowed-context candidate. Выявлены GT errors и source-domain limitations.|Нет inference/parity/target quality/device timings; нет smoke-only controls и cessation/re-entry. Fire — обоснованный кандидат третьего сценария, не готовый победитель. |
|K008|**scoped/open per public action**|Exact PT AGPL grants подтверждены из cards+embedded bytes; FURG CC0 и primary FIRESENSE CC BY4 сохранены; конкретный third-party титр/watermark найден, R3-E6 full-tree license negative.|Решение о license obligations конкретной поставки, original-video rights/публичном показе и записи; R3-E6 grant неизвестен. Внутренний research продолжается. |
|K001|**scoped для fire, общий shortlist open**|Узкий source scenario№4 имеет самостоятельную NN-переменную flame и временной region episode, positives/negatives и отдельную allowed-policy проверку.|Не закрывает smoking и не даёт дополнительного сценария за один smoke label. Реализация/target controls и согласованный scope ещё нужны; generic zone считать инфраструктурой один раз. |

**Следующий ограниченный эксперимент:** получить фактический LinQ custom/catalog contract. При custom: взять A exact PT/SHA, isolated runtime с8.4.51, actual model names→export static graph→actual input/output/operators→CPU parity→compile→реальный LinQ request на одинаковом tensor→device parity/timing. Затем пять выбранных clips с поправленным локальным GT и фиксированным правилом; измерить missed/false/late/duplicate/unknown и once-per-episode. При catalog: сначала доказать доступность fire-class и его contract; при отсутствии отказаться от fire как реализованного сценария. Ни данные, ни ONNX reference не дают hardwarePASS.

**Q/E, которые не закрыты research:** Q — разрешены ли custom fire weights и нужный6-channel decoder, либо есть licensed fire catalog; Q — разрешённые ROI/огневые работы и точная публичная поставка. E — реальный device execution/quality, безопасный permissioned target video, steam/welding negatives, прекращение/повторный onset, исправление найденной локальной GT. Текущий результат усиливает огонь относительно generic corridor по семантической независимости и доступным артефактам; победителя по точности/скорости из этих доказательств вывести нельзя.

<a id="F027"></a>
## F027 — Smoking: exact cigarette ONNX, incompatible loader, untrained-string и donor evidence

**Нормализованный статус и условия:** Description(untrained) определяется args.data, не доказывает random/untrained weights. Full GET cigarette ONNX выполнен W1-05 в памяти; local retained binary отсутствует. MIT repo не отменяет embedded AGPL.

**Источники:** [S249](SOURCES.md#S249), [S250](SOURCES.md#S250), [S255](SOURCES.md#S255), [S266](SOURCES.md#S266), [S267](SOURCES.md#S267), [S268](SOURCES.md#S268), [S269](SOURCES.md#S269), [S270](SOURCES.md#S270), [S271](SOURCES.md#S271), [S272](SOURCES.md#S272), [S273](SOURCES.md#S273), [S274](SOURCES.md#S274), [S275](SOURCES.md#S275), [S276](SOURCES.md#S276), [S277](SOURCES.md#S277), [S278](SOURCES.md#S278), [S279](SOURCES.md#S279).

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S01`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S01 — Реальный smoking repository, зафиксированная версия

- URL: https://github.com/Leviathanlzx/cgr_detection ; commit **`4a45c911cea365d7d196c2276611749ce5f3180b`**, получен GitHub REST `repos/Leviathanlzx/cgr_detection/commits?per_page=1`.
- Точное дерево: https://api.github.com/repos/Leviathanlzx/cgr_detection/git/trees/4a45c911cea365d7d196c2276611749ce5f3180b?recursive=1 . Читались `README.md`, `LICENSE`, `ort_inference.py`, `func.py`, `export.py` через raw URL этого commit.
- **W1-05-F01, наблюдение:** README описывает pose → проверку руки/лица → cigarette detector → накопление evidence по ByteTrack ID. Но фактически среди моделей есть только `models/last.onnx` и `models/yolov8n-pose.onnx`; перечисленных README `model/rtdetr-best.onnx`, `rtdetr-best.pt`, `yolov8n-cig.pt` нет. Папок `video` и `datasets` в проверенном дереве тоже нет. Это не доказывает, что их никогда не было, но текущий checkout не является готовой воспроизводимой цепочкой.
- README-метрики RT-DETR и RTX3090 относятся к заявлениям автора, не к нашей проверке и не к LinQ.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S02`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S02 — Exact cigarette ONNX, собственное чтение protobuf metadata

- Файл: https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/models/last.onnx . HEAD **200**; затем GET **200**, **12 238 102 байта**. Получен в оперативную память, не запускался и не сохранён как исполняемый артефакт.
- SHA-256 реально полученных байт: **`3b2b5754ac65f157c10dc180fbfe671bc3df7d3c6cc2b24462835a04243af0ae`**. Git blob SHA: `cf0b14a252f6721b0f5574f41f0df489ea07b722`.
- **W1-05-F02, наблюдение:** ModelProto IR=8, producer=`pytorch`, producer_version=`2.0.1`, opset=17; input `images` FLOAT `[1,3,640,640]`; output `output0` FLOAT `[1,5,8400]`.
- Metadata дословно: `names="{0: 'cigarette'}"`, `task="detect"`, `imgsz="[640, 640]"`, `stride="32"`, `batch="1"`, `version="8.0.145"`, `date="2023-08-02T14:06:18.201648"`, `license="AGPL-3.0 https://ultralytics.com/license"`, **`description="Ultralytics last model (untrained)"`**.
- Собственным read-only parser прочитаны wire fields ModelProto/GraphProto/ValueInfoProto. Схема проверена в первоисточнике https://raw.githubusercontent.com/onnx/onnx/main/onnx/onnx.proto (ModelProto, GraphProto, TypeProto, TensorShapeProto; live main, commit схемы не фиксировался).
- **Неизвестно:** training provenance, исходные данные и split, точная архитектура этого `last`, реальное качество. Наличие массива весов/label не доказывает обучение на сигаретах.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S03`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S03 — Почему `(untrained)` нельзя трактовать буквально

- Точный исходник версии из metadata: https://raw.githubusercontent.com/ultralytics/ultralytics/v8.0.145/ultralytics/engine/exporter.py ; `Exporter`, создание `trained_on`/`description` около строк 217–229 raw файла.
- **W1-05-F03, наблюдение кода:** `trained_on = f'trained on {Path(self.args.data).name}' if self.args.data else '(untrained)'`. Строка выбирается по наличию `args.data` при экспорте, а не по анализу истории обучения tensor weights.
- **Вывод:** `(untrained)` в S02 совместимо с непереданным dataset argument. Это не доказательство случайных/необученных весов. История обучения остаётся неизвестной. Это особенно важно для последующей передачи: не исключать файл по одной этой строке, но и не принимать за проверенный checkpoint.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S04`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S04 — Smoking I/O, preprocessing и несовместимый путь загрузки

- https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/ort_inference.py ; локаторы `InferenceSession`, `cgr_detect_with_onnx`, `pose_estimate_with_onnx`, `postprocess`.
- **W1-05-F04, наблюдение:** загрузчик требует `model/rtdetr-best.onnx`, тогда как S02 лежит в `models/last.onnx`. Нельзя просто заменить путь: postprocess рассчитан на предложения `[N,4+classes]` с нормированными cxcywh и затем умножает boxes на размер изображения. S02 имеет `[1,5,8400]`, то есть иной layout; декодирование и NMS надо согласовать отдельно.
- В коде square padding в правую/нижнюю часть до max(H,W), resize 640×640, BGR→RGB, `/255`, CHW, batch1 FP32. Это **факт реализации для объявленного пути**, не доказанный preprocessing обучения S02; не смешивать с центрированным Ultralytics letterbox.
- Class mapping S02 подтверждён metadata; само значение score и координат требует проверки декодера на известном кадре.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S05`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S05 — Smoking правила и лицензия кода

- https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/func.py ; `judge_smoke`, `cal_dis`, `cal_angle`, `cgr_detect`, `detect_and_draw`.
- **W1-05-F05, наблюдение:** gate: угол локтя <55° **или** расстояние wrist–nose / shoulder–hip <0.8; после него ищется сигарета в crop около носа. При подтверждении счётчик +10, иначе −1, cap100; smoking threshold задаётся отдельно. Это frame-based evidence, а не секунды. При переменном FPS меняется время тревоги. Nose — proxy, не обнаруженный mouth landmark.
- Repo license: https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/LICENSE — MIT, copyright2023. **Разделять:** MIT кода репозитория; embedded AGPL-3.0 конкретного ONNX; права training data/video не установлены. «Весь стек MIT» — неверный вывод. Юридическая совместимость интеграции здесь не устанавливалась.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S07`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S07 — D-Fire: исходные данные и неоднородные права

- https://github.com/gaia-solutions-on-demand/DFireDataset ; commit **`3890a756b224855f4f7ef8d237a70bc1834a4714`**, REST commits/tree200.
- README: https://raw.githubusercontent.com/gaia-solutions-on-demand/DFireDataset/3890a756b224855f4f7ef8d237a70bc1834a4714/README.md . LICENSE: тот же prefix `/LICENSE`.
- **W1-05-F07, заявление авторов:** 21 527 images по сумме категорий: fire-only1164, smoke-only5867, both4658, none9838; YOLO boxes. Это fire/smoke dataset, не cigarette-smoking event dataset.
- LICENSE объявляет CC0 для сборки, одновременно признаёт отсутствие авторских прав на собранные изображения. README отдельно сохраняет условия original providers для `PublicDataset*` (HPWREN, FESB, FireNet). Поэтому «каждое изображение свободно CC0 для продукта» не подтверждено. Проверка archive содержимого/прав каждого кадра не выполнялась.
- Surveillance videos связаны через https://1drv.ms/f/c/c0bd25b6b048b01d/EhT2Jy6L-YlGvZv-gXH2SnYBENQsnUW96LpZtv_6PngjYQ ; web open вернул Internal Error. Доступный exact video file, checksum и лицензия конкретного клипа **не установлены**; dataset LICENSE нельзя автоматически распространить на отдельные видео.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S08`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S08 — Авторская альтернатива fire с временной проверкой

- https://github.com/pedbrgs/Fire-Detection ; commit **`9d99b0e71fd4cc930da053a41b79de1c58aabdf2`** (REST200).
- README: spatial YOLOv5 small/large плюс temporal AVT или TPT; последняя рекомендована автором для indoor. `data/dfire.yaml` на этом commit GET200: `nc:2`, `names:['smoke','fire']`. `LICENSE` GET200: MIT кода.
- https://raw.githubusercontent.com/pedbrgs/Fire-Detection/9d99b0e71fd4cc930da053a41b79de1c58aabdf2/scripts/download_models.sh прочитан, **не запускался**. Содержит Google Drive download IDs `18kwwGYs0CPVvrLwz283v8IXSeTrTE-Um` (small), `14Qhxvruf3cVxZE_e_6tJNCA3w1xzaWQS` (large); README также ведёт на OneDrive. Exact weights payload/хеш здесь не подтверждены. Это полезный источник temporal идеи, менее воспроизводимый резерв весов, чем S06. MIT кода отдельно от upstream YOLO/весов/данных.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S09`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S09 — Smoking research: хорошие признаки, слабая production-проверка

- Pyataeva, Eliseeva,2021, https://ceur-ws.org/Vol-3006/40_regular_paper.pdf открыт полностью; §2.1, §2.3–2.4, §3, tables3–5, pp343–352.
- **W1-05-F08, опубликованное описание:** используются действия рука–губы–пауза–опускание, зажигание, пепел; отмечены трудности дыма при низком разрешении, blur и погоде. Статья описывает 3D ResNet34, но §2.3 input16frames против §2.4 input32frames112². Описаны 70 smoking videos и HMDB51 negatives; в список объединяемых negative actions попадает и smoking — split неоднозначен. Среди hard negatives леденец, ручка во рту, мороженое. Нет установленной ссылки на готовые веса и независимого industrial camera-hour test. Статья CC BY4.0 не предоставляет автоматически права на все videos/weights.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `### W1-05-S10`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-05-S10 — Датасеты курения: image class не равен видео-событию

- https://data.mendeley.com/datasets/j45dj8bgfc/1 открыт; Smoker Detection Dataset v1, Ali Khan,15.08.2022, DOI10.17632/j45dj8bgfc.1, CC BY4.0 в карточке.
- **W1-05-F09, заявление card:** 1120 изображений,560/560,250×250, собраны поиском; в negative задуманы визуально похожие жесты. Это image classification donor, не bbox dataset и не временная разметка CCTV. Права отдельных поисковых фото не восстановлены; авторские слова про confusers не являются нашим просмотром фактического архива.
- Zhang et al.,2023, https://www.mdpi.com/2079-9292/12/15/3225 , §3.1 и Data Availability — страница индексируется, но direct open429, PDF GET403. По доступному поисковому excerpt первоисточника: предварительный отбор кадров MTCNN с наличием лица, face+objects behavior boxes и hand/cigarette/phone objects. Это сильная зацепка методики, но в этой ветке полный текст заново не получен. Числа/лицензия неприсланного датасета и наличие checkpoints не объявляются подтверждёнными. Соседний `datasets` уже содержит более глубокий разбор; не ждать переписки с авторами для MVP.

**Происхождение:** [W1-05.md](_WORK/W1-05.md), `## 3.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 3. Наблюдаемость и worst-case ошибки

Следующее — наши инженерные выводы и проектируемые проверки, а не измеренные характеристики моделей.

**Пиксели важнее марки камеры.** Пример геометрии, не норматив: если видимый рост человека1.7м занимает170px, предмет8мм поперёк тела при той же глубине имеет около0.8px. При resize1920→640 — около0.27px. Это упрощённая проекция без перспективных поправок, но она показывает потерю сигнала. Цифры8мм/1.7м здесь условные. Кроп исходного кадра до уменьшения сохраняет имеющиеся детали; увеличение crop не восстанавливает скрытую сигарету. Универсального подтверждённого требования «лицо Npx» для найденных весов нет.

Smoking FP: питьё/еда, зубочистка/ручка, рация/телефон, кашель, поправление маски, лицо рукой, соседская сигарета, дым за человеком, пар. FN: задний/верхний ракурс, пальцы закрывают сигарету, она у бедра, редкая затяжка, blur, сжатие, невидимые wrist/nose, несколько людей перекрываются. Hand-to-mouth gate сам может отсеять настоящего курящего.

Flame FP: лампы и сигнальные огни, отражения, солнце/блики, оранжевая одежда, экран с изображением огня, разрешённая горелка/печь, сварка и искры. Последние требуют policy: реальный огневой процесс может быть разрешённым, а не ошибкой detector. Smoke FP: пар, туман, пыль, выхлоп, аэрозоль, clouds; temporal persistence не устраняет устойчивый пар. FN: маленький короткий огонёк зажигалки, бесцветное/засвеченное пламя, чёрно-белый/ИК режим, пламя за корпусом, дым вне FOV. Fire model, обученный на больших пожарах, не гарантирует lighter detection.

Zone: ручной polygon должен соответствовать **разрешённому виду деятельности**, расписанию/наряду, камере и версии конфигурации. Для человека — ground contact proxy (bbox bottom center) со своим uncertainty; для огня — overlap flame box с image ROI и border buffer. Проекция bbox огня на пол без геометрии неверна. На границе нужна метка uncertain/manual review. Нельзя определять «рядом с горючими» без отдельно заданной карты/правила. Для дымового облака нельзя брать его centroid как точное место источника.

<a id="F028"></a>
## F028 — Резервные artifacts: MeetCool, Thalos contradiction, PoseC3D HMDB и отказы

**Нормализованный статус и условия:** MeetCool full structural scan F012 дополняет W1 tail. Thalos actual class0 literal string2, не harness; wrong filename исправлением пути не исправляет class map. PoseC3D только резерв, не causal online industrial event.

**Источники:** [S142](SOURCES.md#S142), [S143](SOURCES.md#S143), [S268](SOURCES.md#S268), [S280](SOURCES.md#S280), [S281](SOURCES.md#S281), [S282](SOURCES.md#S282), [S283](SOURCES.md#S283), [S284](SOURCES.md#S284), [S285](SOURCES.md#S285), [S286](SOURCES.md#S286), [S287](SOURCES.md#S287), [S288](SOURCES.md#S288), [S289](SOURCES.md#S289), [S290](SOURCES.md#S290), [S291](SOURCES.md#S291), [S292](SOURCES.md#S292), [S293](SOURCES.md#S293), [S294](SOURCES.md#S294), [S295](SOURCES.md#S295), [S296](SOURCES.md#S296).

**Происхождение:** [W1-08.md](_WORK/W1-08.md), `### W1-08-S05`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-08-S05 — MeetCool smoking: существующий ONNX с реально прочитанными I/O

[Model repo](https://huggingface.co/MeetCool/yolov8n-smoking-detection), HF API/tree GET, revision **`7d510c6aaa3fbc3048368565d4236993c077dc0a`**. Файлы:

- [Exact ONNX](https://huggingface.co/MeetCool/yolov8n-smoking-detection/resolve/7d510c6aaa3fbc3048368565d4236993c077dc0a/models/fine_tune_YOLOv8n.onnx),12,252,672 B; LFS SHA256 **`afcf1e6d1293427b9221b60c9505e76072f9a295120d0a78c71e35f9c444ff8e`**.
- [Exact PT](https://huggingface.co/MeetCool/yolov8n-smoking-detection/resolve/7d510c6aaa3fbc3048368565d4236993c077dc0a/models/fine_tune_YOLOv8n.pt),6,175,026 B; LFS SHA256 **`1b9a365187bc9b7b54f1e75e2cca349270d18a484b14e38953abb27bbbf89347`**.

README отсутствует (`Entry not found`), repository license field U. ONNX HEAD200. **HTTP Range `bytes=-32768`** вернул206, `Content-Range:bytes 12219904-12252671/12252672`; также отдельно прочитан tail4096/16384. В хвосте ONNX protobuf реально найдены GraphProto input/output ValueInfo и ModelProto metadata/opset:

- input **`images`, float32 `[1,3,640,640]`**;
- output **`output0`, float32 `[1,7,8400]`**;
- opset_import default domain **19** (protobuf field8, version19);
- metadata `version:8.3.74`, `date:2025-02-12T10:42:31.072151`, `task:detect`, `stride:32`, `batch:1`, `imgsz:[640,640]`;
- `names:{0:'cigarette',1:'person',2:'smoke'}`;
- export args batch1, half false, dynamic false, simplify true, nms false;
- description указывает training path `/kaggle/working/Smoking-Person-Detection-13/data.yaml` — это provenance clue, **не восстановленный dataset/version/license**.

Прочитаны только диапазоны metadata, не весь12.2MB файл; полный SHA/checker/operator list U. Из standard v8 head + этих форм следует xywh4+3 class scores, без objectness; host confidence/NMS/undo letterbox. Preprocess совпоставлять с S01 source v8.3.74: RGB float `[0,1]`, fixed640. Отсутствие embedded NMS снижает integration surface, но opset19 потребует явного согласования LinQ. Наличие ONNX не означает наличие совместимой статической компиляции.

**License evidence:** сам граф содержит `AGPL-3.0 License (https://ultralytics.com/license)`. Это явная embedded надпись экспортёра; отдельный grant/ownership statement автора custom weights и training data U. Не писать «лицензия полностью неизвестна», скрывая embedded AGPL, и не писать «чистая permissive модель» из-за отсутствия card. Code v8.3.74 AGPL; video отдельно.

Назначение: person↔cigarette/smoke spatial association + prohibited polygon + устойчивость по времени. Класс smoke не равен курению человека, сигарета в bbox не доказывает затяжку; дальняя CCTV сигарета может иметь несколько пикселей. Это резерв perception, не основной MVP без кадрового smoke-test. Single graph включает person, поэтому вторую person-сеть можно не добавлять до проверки recall/ID stability.

**Происхождение:** [W1-08.md](_WORK/W1-08.md), `### W1-08-S07`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-08-S07 — критическое расхождение Thalos scaffold/harness: отклонён

[README](https://huggingface.co/thalostech2025/thalos-scaffold-harness-safety-v1/raw/c07ae29e6095fa0e284a077fdafdb8a857a8eb77/README.md), [API](https://huggingface.co/api/models/thalostech2025/thalos-scaffold-harness-safety-v1). Revision **`c07ae29e6095fa0e284a077fdafdb8a857a8eb77`**. Единственный binary [scaffold_harness_weights.pt](https://huggingface.co/thalostech2025/thalos-scaffold-harness-safety-v1/resolve/c07ae29e6095fa0e284a077fdafdb8a857a8eb77/scaffold_harness_weights.pt),87,685,242 B, LFS SHA256 **`afe570e6bc72549553ec3436660e376bcf826bd3a16ed395ede6b59fe5c62d05`**.

README обещает scaffold/worker_on_scaffold/harness_worn/harness_missing/platform_edge/fall_hazard_zone, оговаривая «names may vary». В примерах указывает другой filename **`scaffold_harness_safety_weights.pt`**, которого нет в tree. Само по себе это ещё можно исправить; **содержимое weights исправлением пути не исправляется**.

**Собственная A-проверка:** собственный Python `io.RawIOBase` read/seek adapter посылал bounded HTTP `Range:bytes=start-end` и проверял206; zipfile прочитал central directory и только `<archive-prefix>/data.pkl` **183,404 B**. Совокупно **219,182 B HTTP payload** для одной проверки, не87.7MB полный файл. Tensor storage не читались; `pickletools.genops` только дизассемблировал pickle-инструкции, `torch.load`/unpickle/class imports не вызывались. Второе повторное чтение использовано для разрешения memo-reference класса0, не для исполнения.

Header: version8.3.171, date2025-11-29T23:37:19.925775, embedded AGPL, `DetectionModel`. **Фактический names dictionary** начинается на data.pkl byte offset143042:

| Numeric ID | Строка в checkpoint |
|---|---|
| 0 | `2` (строка, не предположение о семантике) |
| 1 | `Safety-barrier` |
| 2 | `Safety-bollard` |
| 3 | `Safety-cone` |
| 4 | `cracks` |
| 5 | `open-hole` |
| 6 | `open_manhole` |
| 7 | `pothole` |

Локаторы для независимого повторения: ID0 на offset143064, его `LONG_BINGET358`143066; memo358 зарегистрирован `BINUNICODE '2'`4057 + `LONG_BINPUT358`4063. ID1 строка143073, ID7 строка143211; SETITEMS143228. Это проверенный class map, не догадка по имени файла. Нельзя заменить карту указанными README словами и считать веса harness detector.

**Решение:** отклонить для высоты/привязи/подцепления. Причина локализована в exact revision checkpoint; не утверждаем, что у владельца нигде нет правильных других weights. Не оценивали качество барьеров/люков и не предлагаем этот файл для нового сценария. README model AGPL и embedded AGPL совпадают, HF YAML license отсутствует; training data и отдельное provenance U. Экспорт/реальный execution U. Размер и claimed YOLOv8-large здесь вторичны по отношению к неверной семантике.

**Происхождение:** [W1-08.md](_WORK/W1-08.md), `### W1-08-S08`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-08-S08 — официальный PoseC3D HMDB51, только action-резерв

Owner `open-mmlab/mmaction2`, pinned SHA **`a5a167dff2399e2d182a60332325f9c0d4663517`**. Заново GET [model zoo](https://raw.githubusercontent.com/open-mmlab/mmaction2/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/README.md), HMDB51: SlowOnly-R50,uniform48,keypoint,69.6 top1,10 clips,14.6G,3.0M params — B. Exact checkpoint:

https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint_20220815-17eaa484.pth

Собственный HEAD200, Content-Length12,276,729 B; hash U, суффикс17eaa484 не объявляем полным SHA256. [Exact config](https://raw.githubusercontent.com/open-mmlab/mmaction2/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint.py) GET: ResNet3dSlowOnly17 heatmap channels, I3DHead51. Val uniform48→PoseCompact→short56→crop56→GeneratePoseTarget sigma.6/use_score→NCTHW_Heatmap. Test10 clips и double flip; не обещать published accuracy при одном causal окне.

[Exact labels](https://raw.githubusercontent.com/open-mmlab/mmaction2/a5a167dff2399e2d182a60332325f9c0d4663517/tools/data/hmdb51/label_map.txt), zero-based: **climb5,climb_stairs6,fall_floor12,pick24,run32,sit37,smoke40,stand42,walk49**. `pick` не равно «неправильная переноска»; `climb` не равно запрещённое перелезание через конкретный станок; smoking class на скелетных heatmaps без сигареты особенно требует domain test. Веса не содержат правил опасности.

I/O C one-clip backbone/head `[1,17,48,56,56]` float heatmaps→51 action logits, probabilities после согласованного wrapper. Нельзя подавать сырой `[T,17,2]` вместо heatmaps. Нужна первая pose-сеть, track-wise attribution, causal window/stride, gap policy. 48 кадров sampling — не автоматически48 consecutive frames/1.6s; source FPS и sampling политика обязательны. Conv3D, heatmap preprocessing и export добавляют риск; стандартный PoseC3D MMDeploy path не подтверждён (W1-01 проверял supported table). Наш ONNX/LinQ U, опубликованная top1 не industrial event precision.

[Code LICENSE](https://raw.githubusercontent.com/open-mmlab/mmaction2/a5a167dff2399e2d182a60332325f9c0d4663517/LICENSE) Apache-2.0 проверен заново; отдельное явное разрешение exact checkpoint/data footage U. HMDB/Kinetics source videos не становятся Apache по лицензии MMAction2. Резерв для сравнительного исследования, не критический путь двухдневного MVP. Альтернативный NTU60 PoseC3D из W1-01 содержит falling42, но не run; не подменять class maps.

**Происхождение:** [W1-08.md](_WORK/W1-08.md), `### W1-08-S10`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-08-S10 — дополнительные проверенные кандидаты и причины отказа

**HEIher/smoking-detection:** revision **`12a54cda2ca031e2b96a486bc288e957e56f51c8`**, [best.pt](https://huggingface.co/HEIher/smoking-detection/resolve/12a54cda2ca031e2b96a486bc288e957e56f51c8/best.pt),40,509,349 B, LFS **`0ef558d3cf049d0acbb3f2322bc9e4e53db1a107426e3669622176c30c054d82`**. [Pinned card](https://huggingface.co/HEIher/smoking-detection/raw/12a54cda2ca031e2b96a486bc288e957e56f51c8/README.md): YOLO11-medium, one class cigarette, mAP50.829, custom Roboflow; текст местами говорит cigarette smoke, но output label cigarette. Card явно говорит модель MIT, а upstream Ultralytics code/models policy AGPL; отдельного LICENSE в прочитанном tree нет. Это **конфликт/неполнота происхождения прав, а не доказательство permissive поставки**. ONNX export только пример `model.export`, фактического ONNX нет. Больше, чем S05, не лучше доказан; резерв, не выбран.

**raidavid/yolov8_fire_and_smoke:** revision **`9df0fd95681a29c376af3950742ee691a1c788d3`**, [weights/best.pt](https://huggingface.co/raidavid/yolov8_fire_and_smoke/resolve/9df0fd95681a29c376af3950742ee691a1c788d3/weights/best.pt),6,775,651 B, LFS **`62f990f60e2383576b6a201da0f62464b2943ed07a6fad2817fb97e1dfca7cc8`**. [args.yaml](https://huggingface.co/raidavid/yolov8_fire_and_smoke/raw/9df0fd95681a29c376af3950742ee691a1c788d3/args.yaml) GET: `task:segment`, `model:yolov8n-seg.pt`, `epochs:1`,imgsz640. README/license U. Mask curves в tree согласуются с segmentation. Ожидать detect-only I/O ошибочно: стандартный seg добавляет mask coefficients/prototypes. Отказ как основной зрелый fire detector; сами names/качество не установлены.

**zell-dev/fire-smoke-detection:** revision **`389086f90a0588f5b97e14f56d569c140430730f`**, [directory](https://huggingface.co/zell-dev/fire-smoke-detection/tree/389086f90a0588f5b97e14f56d569c140430730f/best_int8_openvino_model). `best.bin`11,299,224 B LFS **`648909ca3b1c6c85af378c4254060812e550898226c11ffa7d35668a289a38d7`**, `best.xml`453,937 B; [metadata.yaml](https://huggingface.co/zell-dev/fire-smoke-detection/raw/389086f90a0588f5b97e14f56d569c140430730f/best_int8_openvino_model/metadata.yaml): detect,640,batch1,names0fire/1smoke,version8.3.37,embeddedAGPL. HF card Apache-2.0 конфликтует с embeddedAGPL; provenance U. OpenVINO IR export есть по directory, но это **не ONNX, не LinQ format, не автоматически подтверждённый INT8 calibration**. Не выбран как быстрый LinQ путь.

**TommyNgx/YOLOv10-Fire-and-Smoke-Detection:** API revision **`c4f0f354b2f37d8c8c3f2b0647045feca4e756af`** перечисляет best.pt64,111,730 B и model.safetensors63,712,832 B; raw README GET **ограничен доступом: требуется authentication**. LFS oid API скрыты звёздочками. Поэтому не выдавать публичный старый поисковый snippet за нынешнюю свободную доступность checkpoint. Карточки разных revision называют YOLOv10/YOLOv8 и разные licenses; не выбран.

**SHOU-ISD/fire-and-smoke:** revision **`d5908f953bb80e01a51c29ea60bc7eea54be747e`**, tree: `bestEMA.pt`547,299,586 B, `best_ns.pt`273,170,530 B, даже `yolov8n.pt`136,723,177 B. Card library8.0.4 и mAP.449 без достаточного контракта/прав. Название nano не гарантирует6MB; не скачивал и не выбрал.

**M3GHAN/YOLOv8-Object-Detection:** [первичный README](https://github.com/M3GHAN/YOLOv8-Object-Detection) открыт в web: перечисляет Safety-harness и предлагает обучение; видимый tree только notebook/README, готового checkpoint не подтвердил. Шаблон `your-username`/`[Instruction]` не считать download-and-run. **ReeceMorgan/PPE-Detection** revision`f81cd8ef2cf1867224da286840277477455610ba`: tree только.gitattributes, weights отсутствуют. **techceh/harness** revision`c72ab6002a1a3e03639a3ac48db22f30034a4167`: только `edgHarnessExpressv1 (1).safetensors`9,547,800 B без card/config; не установлено даже что это detector, название harness не доказательство промышленного назначения. Эти попадания отсеяны после API-проверки, не добавлены в готовые модели.

**Intel person-detection-action-recognition-0006:** [официальная документация](https://docs.openvino.ai/2023.3/omz_models_model_person_detection_action_recognition_0006.html) открыта: classroom sitting/writing/raising hand/standing/turned around/lie on desk, не running. Вход BGR NHWC1×400×680×3, SSD/action multi-output. Не выбирать как готовый бег только по action-recognition имени.

**TSSTG GajuuzZ:** W1-01 самостоятельно установил404 точной upstream ссылки; эта ветка не восстановила разрешённое зеркало/hash. Search-result mirror не повышает готовность. Отложен, не включён как проверенный download-and-run.

<a id="F029"></a>
## F029 — Ограждение/конвейер/груз: операциональные определения, источники и geometry

**Нормализованный статус и условия:** Tripwire/polygon не completed climb. Подвешенный груз вне ground plane: H пола не даёт его вертикальную проекцию. Zone fallback не засчитывается исходным сценарием5 без согласованного scope.

**Источники:** [S046](SOURCES.md#S046), [S047](SOURCES.md#S047), [S076](SOURCES.md#S076), [S086](SOURCES.md#S086), [S099](SOURCES.md#S099), [S104](SOURCES.md#S104), [S143](SOURCES.md#S143), [S144](SOURCES.md#S144), [S176](SOURCES.md#S176), [S210](SOURCES.md#S210), [S217](SOURCES.md#S217), [S254](SOURCES.md#S254), [S297](SOURCES.md#S297), [S298](SOURCES.md#S298), [S299](SOURCES.md#S299), [S300](SOURCES.md#S300), [S301](SOURCES.md#S301), [S302](SOURCES.md#S302), [S303](SOURCES.md#S303), [S304](SOURCES.md#S304), [S305](SOURCES.md#S305), [S306](SOURCES.md#S306), [S307](SOURCES.md#S307), [S308](SOURCES.md#S308), [S309](SOURCES.md#S309), [S310](SOURCES.md#S310), [S311](SOURCES.md#S311), [S312](SOURCES.md#S312), [S313](SOURCES.md#S313), [S314](SOURCES.md#S314), [S315](SOURCES.md#S315).

**Происхождение:** [W1-06.md](_WORK/W1-06.md), `## Что именно`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Что именно считается наблюдением

| Вариант | Что непосредственно наблюдаем | Что требуется сверх наблюдения | Честное имя события |
|---|---|---|---|
| Tripwire | Один и тот же track меняет сторону конечного отрезка | Запрет направления, непрерывность track, устойчивость к дрожанию | Пересечение настроенной границы |
| Polygon occupancy | Опорная точка человека находится в полигоне | Утверждённая запретная зона и режим её активности | Нахождение в запретной зоне |
| Zone entry | Был снаружи → пересёк границу → устойчиво внутри | История до входа; при появлении внутри это occupancy, не entry | Вход в запретную зону |
| Climb attempt | У ограждения меняются поза и высота стоп/таза | Видимые суставы, контактная область, отрицательные примеры | Признаки попытки перелезания |
| Completed climb | Подход → подъём/перенос ног → перемещение корпуса → приземление с другой стороны | Раздельные геометрии верха ограждения и сторон на земле | Подтверждённое перелезание в данной сцене |
| Conveyor underpass | Track проходит через известный подконвейерный коридор | Карта установки, исключение штатного прохода, правило участка | Проход через запрещённый коридор под конвейером |
| Under suspended load | Человек и груз видны в одном изображении | Проекция груза на землю, высота/подвешенность, активный подъём, допустимые роли | Без геометрии только потенциальное опасное сближение |

Сам факт движения вниз/приседания не доказывает проход под оборудованием; bbox overlap person–load не доказывает физическое расположение под грузом. «Нарушение» задаётся правилами площадки, разрешёнными проходами и режимом оборудования. Эти состояния не следует угадывать из позы.

**Происхождение:** [W1-06.md](_WORK/W1-06.md), `## Проверенные`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Проверенные первичные источники и артефакты

Все URL открыты/получены 2026-10-23. `main/latest` изменяемы; ниже зафиксированы фактически возвращённые SHA. Статус «HTTP metadata» означает только наличие записи/ответа, не работоспособность модели.

#### W1-06-S01 — Supervision: линия и полигон

- Официальная документация: [LineZone](https://supervision.roboflow.com/latest/detection/tools/line_zone/), [PolygonZone](https://supervision.roboflow.com/latest/detection/tools/polygon_zone/).
- Точная версия GitHub: `fd3de344dc9ba2dacd1e996ee6416b60d5e4d0d2`, установленная через `GET https://api.github.com/repos/roboflow/supervision/commits/main`.
- Файлы: [line_zone.py](https://github.com/roboflow/supervision/blob/fd3de344dc9ba2dacd1e996ee6416b60d5e4d0d2/supervision/detection/line_zone.py), локаторы `LineZone.__init__`, `trigger`, `_compute_anchor_sides`; [polygon_zone.py](https://github.com/roboflow/supervision/blob/fd3de344dc9ba2dacd1e996ee6416b60d5e4d0d2/supervision/detection/tools/polygon_zone.py), `PolygonZone.trigger`.
- Подтверждено кодом/документацией: LineZone использует tracker ID и историю сторон, возвращает поэлементные флаги направлений. PolygonZone по умолчанию проверяет `BOTTOM_CENTER`; попадание выбранных anchors не равно пересечению полного bbox/маски с полигоном. Состояние нахождения само по себе не событие входа. Внешний автомат необходим для эпизодов и дедупликации.
- [LICENSE.md](https://github.com/roboflow/supervision/blob/fd3de344dc9ba2dacd1e996ee6416b60d5e4d0d2/LICENSE.md): MIT, подтверждено GitHub license API. Это лицензия кода; весов, прав на видео и гарантий LinQ она не предоставляет.

#### W1-06-S02 — Конкретный pose-based fence прототип; полезен главным образом как отрицательный аудит

- Репозиторий [Khushnoor-gojwari/Fence_detection_wall_and_iron_fence](https://github.com/Khushnoor-gojwari/Fence_detection_wall_and_iron_fence), точный commit `3aa345f049a033f53c38608aec6d586ddc372ca7`, дата коммита API `2026-08-27T09:54:57Z`.
- Прочитан точный [fence_detection.py](https://github.com/Khushnoor-gojwari/Fence_detection_wall_and_iron_fence/blob/3aa345f049a033f53c38608aec6d586ddc372ca7/fence_detection.py), локаторы `Boundary.is_restricted`, `analyze_climb`, `run_stream`, `feet_point`. Это чужой код; не запускался.
- Факты аудита W1-06-F01: `raw_cross` — нахождение feet point на запрещённой стороне, без обязательного предыдущего состояния на разрешённой стороне. Подтверждение — 4 последних положительных наблюдения. Название crossing здесь сильнее фактически проверяемого свойства.
- W1-06-F02: `is_climb = (near and climbing_posture) or ankle_above_line`; последняя ветка обходит near-fence условие. Поднятая рука или согнутая нога с вертикальным торсом дают climbing posture. Сохранение позы 5 наблюдений не доказывает переноса тела через ограждение. При отсутствии ID код использует общий ключ `-1`, смешивая людей. История наблюдений не привязана к elapsed-time; пропуск видимости может нарушить интерпретацию «последовательных кадров».
- Git tree API содержит `data/fenceclimb.mp4` (3 524 804 B), `data/wall.mp4` (3 217 915 B), два output mp4; `models/` содержит только `.gitkeep`. Веса скачиваются скриптом отдельно. Видео не скачаны/не просмотрены: их содержание и пригодность не подтверждены.
- В полном tree нет LICENSE. Права на код и исходные/output видео не установлены; публичный GitHub не означает разрешения на использование/перепубликацию. Репозиторий не рекомендован как готовый компонент; идеи геометрии можно независимо реализовать.

#### W1-06-S03 — YOLOv8n detector / pose, точные доступные веса

- Официальные [YOLOv8 docs](https://docs.ultralytics.com/models/yolov8) подтверждают detection/pose и экспорт. Состояние текущих pose docs уже описывает YOLO26; переносить его экспортные layouts на YOLOv8 нельзя.
- GitHub release API `https://api.github.com/repos/ultralytics/assets/releases/tags/v8.3.0` вернул точные assets:
  - [yolov8n.pt](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n.pt), 6 549 796 B;
  - [yolov8n-pose.pt](https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt), 6 832 633 B.
- Обоим asset API вернул `digest: null`: SHA256 весов не установлен. Файлы не скачивались, физическая успешность загрузки/десериализации не проверялась. Это точные URL релиза, но asset в GitHub не гарантированно неизменяем.
- Код `ultralytics/ultralytics` tag `v8.3.0` разрешился в commit `6e43d1e1e5db72afbf686dee6745669bcb124b0a`. [Pose head](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/nn/modules/head.py), `Pose.forward/kpts_decode`; [yaml](https://github.com/ultralytics/ultralytics/blob/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/cfg/models/v8/yolov8-pose.yaml) задаёт один класс и 17×3 keypoints.
- Минимальный контракт будущего экспорта: batch=1, RGB NCHW FP32 `[1,3,640,640]`, letterbox с сохранением пропорций и учётом padding, значения /255. После декодирования — boxes и keypoints в одной системе координат с исходным кадром; NMS отдельно при обычном raw export. Ожидаемые raw формы для стандартной YOLOv8 640 без встроенного NMS: detection `[1,84,8400]`, pose `[1,56,8400]` (4 box + 1 person score + 51 keypoint); это вывод из архитектуры, **не проверенный ONNX artifact**. Форму, strides, dtype, opset и NMS необходимо фактически прочитать из экспорта.
- Для detection COCO class 0 = person; модель не содержит специальных классов fence/conveyor/suspended_load. Pose class 0 = person. COCO keypoint order: 0 nose; 1/2 eyes; 3/4 ears; 5/6 shoulders; 7/8 elbows; 9/10 wrists; 11/12 hips; 13/14 knees; 15/16 ankles. Применять порог видимости отдельно от person score.
- Текущий primary source для [preprocessing](https://github.com/ultralytics/ultralytics/blob/5d4baa9ee71833da96863f8cefea764838f76705/ultralytics/engine/predictor.py), `preprocess`, и [LetterBox](https://github.com/ultralytics/ultralytics/blob/5d4baa9ee71833da96863f8cefea764838f76705/ultralytics/data/augment.py) прочитан; он полезен для контракта, но не заменяет фиксацию именно экспортирующей версии. Не смешивать current package и старый checkpoint без проверки.
- Код: AGPL-3.0; официальный сайт указывает AGPL-3.0/Enterprise и для моделей. [LICENSE](https://github.com/ultralytics/ultralytics/blob/5d4baa9ee71833da96863f8cefea764838f76705/LICENSE), [официальная лицензия](https://www.ultralytics.com/license). Это не MIT; условия видео/COCO — отдельный слой. Доказательств компиляции/выполнения этих весов на LinQ нет.

#### W1-06-S04 — Fence Climbing HF: существует один маленький опубликованный артефакт, не доказанная большая база

- [Дерево HF](https://huggingface.co/datasets/shangzx/Fence-Climbing-Action-Recognition-Dataset/tree/55d92dcb2108a596c2a1d8bfe35fb8860db0237e), revision API `55d92dcb2108a596c2a1d8bfe35fb8860db0237e`.
- В siblings только `.gitattributes`, `README.md`, `ddcaa30266351f01ecb63ac1d1afe94f.json`, одноимённый `.mp4` (~8.68 MB по tree). Metadata card содержит неправдоподобную size category `1B<n<10B`, которая не доказывает миллиардов примеров.
- Прочитан [точный JSON](https://huggingface.co/datasets/shangzx/Fence-Climbing-Action-Recognition-Dataset/resolve/55d92dcb2108a596c2a1d8bfe35fb8860db0237e/ddcaa30266351f01ecb63ac1d1afe94f.json): поля `file_name`, `duration=36338`, `quality=1080*1920`. Единицы duration не заданы; в прочитанном JSON нет temporal segments, track ID, bbox, pose или класса/negative labels. Видео не просмотрено.
- Карточка декларирует CC-BY-NC-SA-4.0. Это ограничение noncommercial; происхождение видеозаписи/полномочия загрузившего не проверены. Нельзя считать этот артефакт разрешённым публичным хакатонным demo по одному тегу. Польза: возможный единичный кандидат для дополнительной проверки; не обучающая база и не тест обобщения.

#### W1-06-S05 — CAAR, релевантный промышленный контекст

- [Сайт авторов CAAR](https://caar24.github.io/caar24/), секции Features, Gallery, Downloads, Terms of Use. [Первичная ECCV 2024 публикация](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/10056_ECCV_2024_paper.php), Sasaki, Ito, Kondo, «Context-Aware Action Recognition: Introducing a Comprehensive Dataset for Behavior Contrast».
- Авторы заявляют 2.1K untrimmed видео, 4K/30FPS, multi-view, пары proper/improper, девять актёров. Галерея включает подход/прикосновение к подвешенному грузу. Это не доказательство класса «walking under load» и не checkpoint для него.
- Доступ ко всему набору — запрос авторам, затем Box. Условия: только академическое исследование; показ лишь в академических публикациях/презентациях; распространение и коммерческое использование запрещены. Не связывались с авторами, доступ не запрашивали. Для ближайшего MVP ресурс организационно и лицензионно не готов. Польза — основание строить контрастные positive/negative пары с одинаковой сценой.

#### W1-06-S06 — AnywayLabs Suspended Loads: синтетический detector dataset

- [Страница производителя](https://anywaylabs.ai/dataset/suspended-load-in-a-factory), Summary, Class Distribution, Dataset Metadata, Model Performance. Заявлены 500 синтетических изображений, YOLO bbox, классы `worker`/`suspended_load`, CC BY 4.0, обновление 2026-05. Числовой mapping классов и архив не получены.
- Страница декларирует mAP@0.5 0.9929 и validation на real held-out; split, исходные реальные кадры и trained checkpoint публично не предъявлены в прочитанном материале. Это заявленные метрики производителя, не независимо проверенный результат и не качество событий «под грузом».
- Download/Request Access — кнопки; точный публичный URL архива/весов в открытом тексте не установлен. Не отправлялись запросы. Польза — зацепка для собственного suspended-load detector; ценности для быстрого inference-only MVP недостаточно. Изображения не дают временного паттерна.

#### W1-06-S07 — Action baseline PoseC3D/HMDB51, точный, но не готовый industrial classifier

- [Официальный model zoo](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/README.md), commit `a5a167dff2399e2d182a60332325f9c0d4663517`. [Config](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/configs/skeleton/posec3d/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint.py), [label_map](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/tools/data/hmdb51/label_map.txt).
- Точный [checkpoint](https://download.openmmlab.com/mmaction/v1.0/skeleton/posec3d/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint/slowonly_kinetics400-pretrained-r50_8xb16-u48-120e_hmdb51-split1-keypoint_20220815-17eaa484.pth). HEAD 200, Content-Length 12 276 729 B. Веса не скачаны, hash/содержимое/инференс не проверены.
- Config: Recognizer3D/ResNet3dSlowOnly-R50, 17 heatmap channels, 51-class head. Test preprocessing: uniform 48 frames, 10 clips, PoseCompact, resize/center crop 56×56, score-weighted keypoint heatmaps sigma .6, double flip, NCTHW_Heatmap, average probabilities. Это вход из pose sequences/heatmaps, не сырое RGB и не простые 17×2 координаты напрямую.
- Map: нулевая позиция 5 = `climb`, 6 = `climb_stairs`; нет классов «fence violation», «under conveyor», «under suspended load». Скелетный классификатор без object/zone context не знает, что ограждение запрещено. Generic climb может быть лазанием по разрешённой лестнице.
- Код Apache-2.0 ([LICENSE](https://github.com/open-mmlab/mmaction2/blob/a5a167dff2399e2d182a60332325f9c0d4663517/LICENSE)); отдельная однозначная лицензия checkpoint/HMDB исходных видео здесь не установлена. Apache кода не переносится автоматически на чужие видео. Export/quantization/LinQ не проверены. Отказ от этого baseline для обязательного MVP: лишний temporal inference и preprocessing при слабом соответствии классов.

#### W1-06-S08 — Нормативный пример того, почему observation ≠ нарушение

- Официальные OSHA [1917.48(a)(2)](https://www.osha.gov/laws-regs/regulations/standardnumber/1917/1917.48) и [1926.555(a)(5–6)](https://www.osha.gov/laws-regs/regulations/standardnumber/1926/1926.555) описывают защищённые/обозначенные проходы около конвейеров. Первая страница появилась в поиске, прямой open получил 403; вторая прочитана в поисковой выдаче официального домена.
- [1926.1425](https://www.osha.gov/laws-regs/regulations/standardnumber/1926/1926.1425): правила зависят от фазы операции, зоны падения и допускаемых функций работников; частный запрет напрямую под грузом явно указан для tilt-up/down. Не следует превращать фрагмент в универсальную норму всех производств.
- Это зарубежные отраслевые примеры смысловой неоднозначности, **не юридическое заключение и не применимые правила московского предприятия**. Для demo необходимо локальное утверждённое правило зоны, состояние оборудования и исключения.

**Происхождение:** [W1-06.md](_WORK/W1-06.md), `## Проект правил`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Проект правил: инженерные выводы, а не факты об эффективности

#### A. Геометрический MVP

1. Камера фиксирована; оператор задаёт forbidden polygon, разрешённые проходы, active schedule/ручной флаг режима. Person model выдаёт bbox; tracker сохраняет ID. Нейросеть должна реально выполняться на LinQ; CPU tracker/правила сами по себе этого требования не закрывают.
2. Выбирать footpoint по видимым ankles, иначе bottom-center bbox с пометкой низкой надёжности. При перекрытых ногах нижний край bbox может не быть точкой земли. Не смешивать ground polygon с верхней кромкой ограждения.
3. Signed distance к линии: `cross(B-A,P-A)/||B-A||`. До перехода нужна история разрешённой стороны; после — противоположная сторона за hysteresis band. Для конечного tripwire проверить пересечение именно отрезка, а не бесконечной прямой; запретить вырожденные A=B. Zone entry отдельно различает initial occupancy и реальный вход.
4. Автомат `outside → candidate → confirmed → active → cleared`. Порог подтверждения задавать секундами/timestamps, а не фиксированным числом обработанных кадров. Пробные стартовые значения 0.3–0.7 с для entry и 0.5–1 с clear — только tuning hypotheses; быстрый сквозной проход должен сохраняться в истории, иначе dwell filter создаст FN.
5. Единственное сообщение на episode UUID; последующие кадры обновляют эпизод. Реармить после устойчивого выхода. При ID switch/короткой окклюзии — спатиотемпоральное склеивание с ограниченным TTL, включая camera+zone+rule и trajectory; бесконечный set tracker_id непригоден. При нескольких людях не склеивать близкие одновременные события.

Для «под конвейером» нужны отдельные A/B входы и скрытый transit corridor: вход A, окклюзия под установкой, выход B в допустимом временном окне. Само отсутствие bbox не считать проходом. Если проход полностью закрыт от камеры и люди одинаково выходят из соседних коридоров, идентификация неоднозначна; нужен второй ракурс или менее сильная формулировка события.

#### B. Перелезание: pose + объект + последовательность

Нужны как минимум ground-side zones A/B, полоса контакта с ограждением, видимая верхняя кромка и разрешённые ворота. Нельзя одной нарисованной линией одновременно кодировать проекцию вертикального верха и границу двух областей пола.

Автомат: approach(A) → near-fence → elevation/contact candidate → legs/hips transfer → landing(B). Attempt и completed — разные метки. Признаки: нормализованные подъёмы ankles/hips относительно собственной стойки, сгибание коленей, положение wrists относительно кромки, изменение ориентации/топологии тела, движение центра таза через границу. Нормировать на размер человека/перспективу, использовать confidence masks. Одна рука выше плеча, один knee angle, upright torso или ankle_y < fence_y не являются достаточными признаками.

При невидимых суставах вывод `unknown`, не «не перелезает». Крупный bbox около fence может относиться к человеку перед ограждением, а не в контакте с ним. Противоположная сторона после исчезновения может быть достигнута через ворота. Сходная поза возникает при разрешённом ремонте, доставании предмета, махании рукой, приседе, подъёме на ступень. Даже temporal action score `climb` нужно объединять с конфигурацией объекта/зоны и конечной траекторией.

#### C. Подвешенный груз: где заканчивается 2D

Груз в воздухе не лежит на ground plane; обычная homography пола неприменима к bbox груза. Она может перенести footpoint человека на карту пола, но не даёт вертикальную проекцию подвешенного объекта без высоты/3D/дополнительной геометрии. Широкий динамический image polygon может применяться как консервативный экранный proxy, обязательно с таким названием и оценкой FP, а не как измеренная зона падения.

Надёжнее для demo фиксированная вручную известная зона подъёма с ручным active flag; событие «человек в активной опасной зоне». Для физического «под грузом» нужны калиброванные виды/глубина, известная высота и footprint груза, либо телеметрия крана + карта. Требуется различать реально подвешенный, лежащий и неподвижно установленный груз. Допуски стропальщиков/монтажников не определяются наличием каски.

**Происхождение:** [W1-06.md](_WORK/W1-06.md), `## Annotation`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Annotation, калибровка и видео

- На каждый camera view: исходные resolution/FPS/timebase, вершины полигонов в исходных координатах, разрешённые проходы, верх ограждения отдельно, equipment ID, правило/фаза активности, версия конфига. Zoom/pan требует новой привязки. Растяжение картинки без пересчёта зон запрещено.
- Разметка события: actor ID, start/confirmation/end times, видимые contact/elevation/landing этапы, attempted/completed, allowed/forbidden/unknown, occlusion интервалы. Секундная граница подтверждения определяется до оценивания, не после просмотра prediction.
- Для расстояний в метрах нужны параметры ground plane/контрольные расстояния и валидация reprojection. Для entry по image polygon метры не обязательны; нельзя подписывать pixel margin как сантиметры.
- Быстрый источник честного видео — собственная безопасная постановка с согласиями и правом demo, инертным макетом/низкой безопасной преградой; это демонстрация алгоритма на постановочной сцене. Не создавать реальный проход под работающим конвейером или подвешенным тяжёлым грузом. Производственные видео предоставляет организатор с подтверждением прав. В найденных online кандидатах права/полнота для demo не закрыты.
- Разделять калибровочный и отложенный ролик; не назначать polygon специально под каждого человека. Из одного прохода нельзя получать независимые train/test кадры.

<a id="F030"></a>
## F030 — Fence datasets: sample9 remap, exact media leads, отсутствие trained best

**Нормализованный статус и условия:** Для sample9 source1climbing/source2walking, остальных source1walking/source2climbing. Нет доказанной harmonization final training set. Код/видео/веса rights отдельно unknown; generic yolov5m не custom checkpoint.

**Источники:** [S316](SOURCES.md#S316), [S317](SOURCES.md#S317), [S318](SOURCES.md#S318), [S319](SOURCES.md#S319), [S320](SOURCES.md#S320), [S321](SOURCES.md#S321), [S322](SOURCES.md#S322), [S323](SOURCES.md#S323), [S324](SOURCES.md#S324), [S325](SOURCES.md#S325), [S326](SOURCES.md#S326), [S327](SOURCES.md#S327), [S328](SOURCES.md#S328), [S329](SOURCES.md#S329), [S330](SOURCES.md#S330), [S331](SOURCES.md#S331), [S332](SOURCES.md#S332), [S333](SOURCES.md#S333).

**Происхождение:** [W1-11.md](_WORK/W1-11.md), `## 6.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 6. Перелезание: новые source video, реальный ID conflict и ложная готовность checkpoint

#### W1-11-S14 — jongkim228/Fence_Security: пригодные пути, требующие per-source remap

[Первичный repo](https://github.com/jongkim228/Fence_Security/tree/011e048790b0cab1751d7532cac7c02656698990), commit**011e048790b0cab1751d7532cac7c02656698990** из GitHub API23.10.2026. API license null; license grant для code/data/video/weights не найден. Рекурсивное дерево **truncated=true** (в repo закоммичен environment), поэтому отсутствие файла по этому дереву не доказательство. Проверены отдельные root/directory contents и raw small files.

**W1-11-F19 / C/A:** README заявляет586 images, CVAT labels и два behavior classes walking/climbing; fence data с YouTube, также indoor UCF101 relabeled climbing. Артефакты содержат и третий source class fence. Лично прочитаны **все14 `labels/sampleN/obj.names`** на pinned commit:

| Поднабор | Source zero-based IDs | Как переносить |
|---|---|---|
| sample1–8, sample10–14 | **0=fence,1=walking,2=climbing** | source2→canonical climbing |
| sample9 | **0=fence,1=climbing,2=walking** | source1→canonical climbing, source2→canonical walking |

Точные конфликтующие [sample1 obj.names](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/labels/sample1/obj.names) и [sample9 obj.names](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/labels/sample9/obj.names). sample7 имеет trailing empty line, это не четвёртый класс. Прочитан [dataset/train/sample10frame0000.txt](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/dataset/train/sample10frame0000.txt): `2 .546273 .679655 .302815 .521237`, YOLO-like normalized center/size. **Не доказано**, что final dataset/train/val был правильно harmonized автором. Маппинг original CVAT folder и final training labels держать отдельно до проверки provenance.

**W1-11-F20 / A:** конкретные video/label paths, metadata file sizes, не скачанные media:

| Artifact | Путь на том же commit | Bytes / смысл |
|---|---|---|
| sourcevideo | [videos/sample1.mp4](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/videos/sample1.mp4) | 1045694; кандидат, содержимое не просмотрено |
| sourcevideo | [videos/sample10.mp4](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/videos/sample10.mp4) | 3769890; имя связано с sample10, pairing timebase ещё проверить |
| labels | [labels/sample1/obj_train_data](https://github.com/jongkim228/Fence_Security/tree/011e048790b0cab1751d7532cac7c02656698990/labels/sample1/obj_train_data), `labels/sample1/train.txt`, `labels/sample1/sample1.zip` | zip metadata25540B; members не открыты |
| demovideo | [Test_sample.mov](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/Test_sample.mov) | 19364409 |
| demovideo | [Test_sample1.mov](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/Test_sample1.mov) | 26363511 |
| demovideo | [Test_sample2.mov](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/Test_sample2.mov) | 11830584 |
| domain-confuser | [ucf_videos/v_RockClimbingIndoor_g01_c01.avi](https://raw.githubusercontent.com/jongkim228/Fence_Security/011e048790b0cab1751d7532cac7c02656698990/ucf_videos/v_RockClimbingIndoor_g01_c01.avi) | 1400864; indoor sports, не industrial fence violation |

**W1-11-F21 / A/I:** [alert.py](https://github.com/jongkim228/Fence_Security/blob/011e048790b0cab1751d7532cac7c02656698990/alert.py) указывает custom weight **`yolov5/runs/train/intruder_detector12/weights/best.pt`** и target string`climbing`. Root содержит `yolov5m.pt`42806829B, но [train_run.py](https://github.com/jongkim228/Fence_Security/blob/011e048790b0cab1751d7532cac7c02656698990/train_run.py) использует его как initial weights, а `yolov5` — submodule upstream. Наличие trained best.pt по указанному вложенному пути не установлено; не выдавать generic yolov5m.pt за custom climb weights. Конечный model.names не проверен.

Предварительный отказ от готового запуска. Пригодны исходные videos/TXT для ручного bounded replay после rights+semantic inspection. Frame-level behavior bbox не содержит completed-crossing interval, стороны ограждения, разрешённые ворота, track IDs, under-conveyor action. Высокий риск leakage: соседние frames`sample10frame0000...`; split надо делать по исходному видео/сцене, не по кадру. Indoor-climbing source полезен как **hard negative нарушения** при допустимом спорте, даже если автор обучал его как positive action. Для фабрики нужны реальные safe climb лестницы, ремонт, подъём рук, шаг на ступень и проход через ворота.

#### W1-11-S15 — HF Fence-Climbing-Action-Recognition-Dataset: конкретный sample, не миллиард videos

[Первичная карточка](https://huggingface.co/datasets/shangzx/Fence-Climbing-Action-Recognition-Dataset), [API](https://huggingface.co/api/datasets/shangzx/Fence-Climbing-Action-Recognition-Dataset), revision**55d92dcb2108a596c2a1d8bfe35fb8860db0237e**, public/gatedfalse. Лично прочитан pinned [JSON](https://huggingface.co/datasets/shangzx/Fence-Climbing-Action-Recognition-Dataset/raw/55d92dcb2108a596c2a1d8bfe35fb8860db0237e/ddcaa30266351f01ecb63ac1d1afe94f.json): `file_name=ddcaa30266351f01ecb63ac1d1afe94f.mp4,duration=36338,quality=1080*1920`.

**W1-11-F22 / A/C/I:** [exact MP4](https://huggingface.co/datasets/shangzx/Fence-Climbing-Action-Recognition-Dataset/resolve/55d92dcb2108a596c2a1d8bfe35fb8860db0237e/ddcaa30266351f01ecb63ac1d1afe94f.mp4), metadata8682998B; publisher LFS SHA256`2b3e0f3b531ee685c7b26e8036cd729bfc74b775611edd402c83822d63ee823c` (не перепроверен). Inventory: только README/.gitattributes/одинJSON/одинMP4. Card `1B<n<10B` не соответствует опубликованному payload и не даёт права заявлять масштаб. JSON не содержит class ID, person bbox, event interval, visibility или negative labels; единицы duration не заданы, не утверждать36.338s без probe. Карточка CC BY-NC-SA4.0, отдельно коммерческий доступ по договору; заявляет simulated scenarios. Подходит лишь как sample для просмотра после прояснения прав/содержания; не полноценный annotated training dataset и не реальное производство. Веса отсутствуют в полученном inventory. Contact не использован.

#### W1-11-S16 — Общие climbing labels и готовые позовые клипы

**W1-11-F23 / attributed A/I:** из W1-06 остаётся [Khushnoor-gojwari data/fenceclimb.mp4](https://github.com/Khushnoor-gojwari/Fence_detection_wall_and_iron_fence/blob/3aa345f049a033f53c38608aec6d586ddc372ca7/data/fenceclimb.mp4)3524804B и `data/wall.mp4`3217915B. Семантика/права/GT не просмотрены этой веткой. Кодовая позовая эвристика не ground truth. AVA20 и HMDB5/6 — action donors, но climb mountains/stairs не запрещённое перелезание. Для прохода под работающим оборудованием отдельного exact annotated video/weights source в выполненном поиске не найдено: не переименовывать crawl/climb в under-equipment violation.

<a id="F031"></a>
## F031 — Высота/привязь и дополнительная переноска: наблюдаемость, модели и нормативный scope

**Нормализованный статус и условия:** SafetyVision actual graph прочитан F012, former binary unknown обновлён. Card class map остаётся card provenance; No_Harness не connection. Нормативные числа — source scope с отмеченной доступностью, не готовое локальное event rule.

**Источники:** [S025](SOURCES.md#S025), [S334](SOURCES.md#S334), [S335](SOURCES.md#S335), [S336](SOURCES.md#S336), [S337](SOURCES.md#S337), [S338](SOURCES.md#S338), [S339](SOURCES.md#S339), [S340](SOURCES.md#S340), [S341](SOURCES.md#S341), [S342](SOURCES.md#S342), [S343](SOURCES.md#S343), [S344](SOURCES.md#S344), [S345](SOURCES.md#S345), [S346](SOURCES.md#S346), [S347](SOURCES.md#S347), [S348](SOURCES.md#S348), [S349](SOURCES.md#S349), [S350](SOURCES.md#S350), [S351](SOURCES.md#S351), [S352](SOURCES.md#S352), [S353](SOURCES.md#S353), [S354](SOURCES.md#S354), [S355](SOURCES.md#S355), [S356](SOURCES.md#S356), [S357](SOURCES.md#S357), [S358](SOURCES.md#S358), [S359](SOURCES.md#S359).

**Происхождение:** [W1-07.md](_WORK/W1-07.md), `## 1.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 1. Что действительно видно и какие утверждения допустимы

| Уровень | Наблюдаемый признак | Что ещё требуется | Недопустимый автоматический вывод |
|---|---|---|---|
| Человек | bbox/track, видимые стопы, корпус | принадлежность площадке/ярусу, карта сцены | «на высоте», потому что bbox находится сверху кадра |
| Привязь (`harness`) | лямки, пояс/бедренные элементы, часть привязи на корпусе | видимость диагностических частей, ассоциация с конкретным person | «пристёгнут», «правильно надета», «исправна» |
| Строп (`lanyard`) | линия/ремень от привязи, иногда амортизатор | непрерывность, принадлежность человеку, второй конец | «верёвка рядом» = страховочная связь |
| Карабин/крюк (`hook/connector`) | маленький объект и его положение | точка зацепления, замок/ориентация, разрешённый тип соединения | детекция крюка = закрытый исправный карабин |
| Анкер (`anchor/anchorage`) | видимая конструкция/предварительно обозначенная точка | паспорт/проект/допуск точки, прочность, совместимость, число пользователей | любая труба/перила = допустимый анкер |
| Система защиты | несколько перечисленных признаков | локальный ППР/техкарта, альтернативная коллективная защита, высота/запас остановки | «все элементы в кадре» = система отвечает требованиям |

**I / W1-07-F03.** Отрицательные состояния нужно разделить: `visible_absence` (достаточно видимый корпус без привязи), `not_detected` (модель не нашла), `not_visible` (спина/грудь/строп закрыты), `ambiguous_owner`, `out_of_scope`. Только первое является кандидатом на проверку отсутствия. Для непристёгнутости нужен отдельный положительно наблюдаемый признак — например, свободный конец стропа видим целиком и заведомо не закреплён. Даже он не исключает второй независимый строп/средство защиты.

**I / W1-07-F04.** Фиксированная камера + вручную обследованная площадка сильнее монокулярной догадки о метрах. Настройка: polygon рабочей поверхности/входа, тип защиты по зоне, закрываемые участки, список допустимых анкерных зон, привязка к версии техкарты. При пересечении ярусов в проекции нужны отдельные поверхности/маски или другой ракурс. Для границы площадки использовать стопы/контакт с поверхностью; torso-crop — для СИЗ. Если стопы не видны, 2D polygon не доказывает ярус. Homography одной плоскости не восстанавливает произвольную 3D-сцену и высоту падения.

**P / W1-07-F05.** Малые объекты оценивать после реального resize/letterbox. Пример расчёта, не измерение: 1920×1080 → 640×640 с сохранением пропорций даёт масштаб 1/3; крюк шириной 12 px становится 4 px. Crop оригинального person/торса может сохранить больше деталей; увеличение уже размытого crop не восстанавливает замок. Ни универсального минимального размера, ни точности такой схемы мы не установили. Снять распределение размеров привязи/крюка в target-видео и долю пригодных кадров; недоступные для человеческой проверки детали не объявлять решённой задачей модели.

Ассоциация: equipment bbox внутри расширенного torso person, геометрия лямок/стропа и согласованность во времени; при нескольких людях выбирать однозначное соответствие, а не «есть любая привязь в кадре». Один предмет не должен автоматически защищать всех работников. При спорном владельце — unknown. Для `No_Harness` необходимо установить единицу его разметки: person bbox или область корпуса; нельзя молча переносить numeric ID другой модели.

**Происхождение:** [W1-07.md](_WORK/W1-07.md), `## 2.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 2. Проверенные кандидаты: точные классы, веса и ограничения

#### W1-07-S01 — исходная статья Xu/Huang/Huang и Dataset

- [Статья, DOI 10.1049/ipr2.12696](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/ipr2.12696), IET Image Processing 17(4), 1071–1085, 2023; разделы abstract/data availability. **C:** 3300 изображений; опубликованные precision/recall/mAP/FPS относятся к работе авторов, не к нашим камерам/LinQ. В этой ветке показатели не используются как гарантия.
- [Зафиксированное дерево](https://github.com/Huangjiajing96/Dataset/tree/251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c), GitHub API `repos/Huangjiajing96/Dataset`, `commits?per_page=1`, `git/trees/251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c?recursive=1`. **A:** commit `251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c`; API `license: null`; дерево 6602 записей, корни только `Annotations`, `JPEGImages`; файлов `.pt/.onnx/.weights/.py/.yaml`, README/LICENSE не найдено. Это не репозиторий готовой модели.

**A / W1-07-F06.** Получены два XML (не весь корпус):

| Точный immutable файл | Размер изображения из XML | Литеральный класс и bbox |
|---|---|---|
| [Dangerous0001.xml](https://raw.githubusercontent.com/Huangjiajing96/Dataset/251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c/Annotations/Dangerous0001.xml) | 400×486 | `clothes` [109,63,266,166]; `person` [77,11,342,352] |
| [SafetyHarness0001.xml](https://raw.githubusercontent.com/Huangjiajing96/Dataset/251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c/Annotations/SafetyHarness0001.xml) | 1920×1080 | **`safety-harness`** [608,183,908,613]; `person` [403,1,950,1078], person `truncated=1` |

Исправление соседней зацепки: фактическое имя положительного класса в проверенном XML — `safety-harness`, не `harness`. Numeric IDs в VOC XML нет. В этих двух файлах нет person-item relation/track/lanyard/anchor/hook, `database=Unknown`. Полный class inventory всех 3300 XML этой веткой не получен; две записи не доказывают отсутствие иных классов во всём корпусе. Соседний отчёт указывает 3300 XML/3300 JPEG, но это его проверка, а не наш новый полный подсчёт.

**I/U:** полезный донор визуального ношения привязи после проверки всего корпуса и прав; не turnkey-кандидат на срок хакатона. `clothes` — размеченная область одежды, а не универсальный класс фактического отсутствия страховочной системы; имя `Dangerous` не event GT. Статья open access не выдаёт автоматически лицензию на чужие изображения/видео; отсутствие LICENSE не означает permission. Не установлены разрешение на обучение/показ/перераспространение, готовые веса, точный экспорт и пригодное continuous-видео.

#### W1-07-S02 — SafetyVision YOLOv8, наиболее конкретный быстрый кандидат

[Карточка](https://huggingface.co/ayushgupta7777/safetyvision-yolov8), [API metadata с blobs](https://huggingface.co/api/models/ayushgupta7777/safetyvision-yolov8?blobs=true), immutable revision **`56a71758b55f0e9f2b4b2d6b51a779a1f882da10`**, `gated=false` (A). **C:** v2 — YOLOv8s; AGPL-3.0 для весов; 13 классов; `No_Harness` — лишь absence-сигнал. Карточка сообщает 256 test instances и mAP50 0.830 для этого класса, а v1 — один instance/mAP0. Это не независимая проверка. Lanyard/anchor/hook в опубликованной карте отсутствуют.

Карта (D/C): `0 Fall-Detected; 1 Gloves; 2 Goggles; 3 Hardhat; 4 Mask; 5 NO-Gloves; 6 NO-Goggles; 7 NO-Hardhat; 8 NO-Mask; 9 NO-Safety Vest; 10 No_Harness; 11 Person; 12 Safety Vest`. Название `Fall-Detected` не делает одно изображение доказательством падения.

| Файл в revision | Bytes API | SHA256 LFS metadata |
|---|---:|---|
| `v2/best.pt` | 22547434 | `7863be4700dcf831579d610bb3fe3668fb29fb22ab17ca027b55e94b88bfff7a` |
| `v2/best_640.onnx` | 44764727 | `ea18ae903a566e8fa76f3ee1c503075522dca269269315e9c862efa170430b35` |
| `v2/best_896.onnx` | 44926046 | `b250353639e01800f9cbe79c6002b8b041bdae7560328b8e18ad4a42dc3844e1` |

Это metadata подтверждение наличия файлов, а не скачивание/проверка SHA бинарника. [Точный маршрут ONNX](https://huggingface.co/ayushgupta7777/safetyvision-yolov8/resolve/56a71758b55f0e9f2b4b2d6b51a779a1f882da10/v2/best_640.onnx). Root `best.pt/best.onnx/best.onnx.data` — v1; не подменять ими v2. Полный ONNX-граф в этой ветке не разбирался.

#### W1-07-S03 — читаемый код preprocessing/postprocessing SafetyVision

[core/detector.py](https://raw.githubusercontent.com/ayushgupta07xx/SafetyVision/3fba9d358321b14725ee6d329dd2bc99c89c8320/core/detector.py), commit **`3fba9d358321b14725ee6d329dd2bc99c89c8320`**; GitHub API license **AGPL-3.0**, [LICENSE](https://github.com/ayushgupta07xx/SafetyVision/blob/3fba9d358321b14725ee6d329dd2bc99c89c8320/LICENSE). **A:** файл прочитан, не запущен. BGR→RGB; letterbox с сохранением aspect ratio; float32/255; HWC→NCHW, batch dimension; выход предполагается `(1,4+classes,N)`, xywh и class scores, confidence filtering, OpenCV NMS, обратное преобразование pad/scale. Для 640 карточка S02 заявляет `(1,17,8400)`, для 896 — 16464 позиций и opset20/fp32. Фактические input/output names, dtype, shape и operators нужно прочитать из бинарного ONNX перед LinQ.

**A/I / W1-07-F07.** Код выбирает максимальный score по классам, применяет `cv2.dnn.NMSBoxes`, затем связывает NO-X с Person по overlap; это не исследованная гарантия person association. Особо проверить, не подавляет ли общий NMS вложенные Person/No_Harness/другие классы. Не переносить такой постпроцесс без parity-теста. Пример preprocessing в model card просто resize; production-код использует letterbox/RGB — для воспроизведения ориентироваться на проверенный код и зафиксированный контракт, не смешивать варианты.

Права разделять: AGPL исходного кода подтверждена metadata/LICENSE; лицензия весов заявлена карточкой; права пяти исходных Roboflow-наборов, каждого изображения, видео и демонстрационного показа этой веткой не проверены. Не считать производное «унаследование лицензии» полной проверкой цепочки прав.

#### W1-07-S04 — Thalos: отклонён, README противоречит checkpoint

[Карточка](https://huggingface.co/thalostech2025/thalos-scaffold-harness-safety-v1), [API](https://huggingface.co/api/models/thalostech2025/thalos-scaffold-harness-safety-v1?blobs=true); revision **`c07ae29e6095fa0e284a077fdafdb8a857a8eb77`**, gated=false (A). Фактический файл **`scaffold_harness_weights.pt`**, 87685242 bytes, LFS SHA256 `afe570e6bc72549553ec3436660e376bcf826bd3a16ed395ede6b59fe5c62d05`. Карточка/пример URL вместо него называют **`scaffold_harness_safety_weights.pt`** — такого sibling API не показывает. Веса не скачивались/не десериализовались.

**C:** карточка перечисляет `scaffold`, `worker_on_scaffold`, `harness_worn`, `harness_missing`, `platform_edge`, `fall_hazard_zone`, но оговаривает возможное отличие имён. Карточка заявляет AGPL-3.0; YAML-license API null, отдельного LICENSE нет. ONNX нет в inventory; права data/video не установлены.

**A соседней ветки, не собственный бинарный анализ / W1-07-F13.** W1-08 сообщил 2026-10-23 прямую проверку [того же immutable checkpoint](https://huggingface.co/thalostech2025/thalos-scaffold-harness-safety-v1/resolve/c07ae29e6095fa0e284a077fdafdb8a857a8eb77/scaffold_harness_weights.pt): HTTP Range 206, прочитаны ZIP central directory и только `data.pkl` (183404 bytes); всего 219182 bytes HTTP, tensor payload целиком не скачан. `pickletools.genops` без `torch.load/pickle.load` обнаружил `names` на offset143042: `{0:'2', 1:'Safety-barrier', 2:'Safety-bollard', 3:'Safety-cone', 4:'cracks', 5:'open-hole', 6:'open_manhole', 7:'pothole'}`. ID0 — буквальная строка `'2'`: BINUNICODE offset4057, LONG_BINPUT358 offset4063, reference offset143066. Header version8.3.171, date2025-11-29T23:37:19.925775. Подробности — `_WORK/W1-08.md`. **Отказ для harness:** содержимое checkpoint противоречит карточке. Не включать даже как неподтверждённые готовые harness weights. Данная ветка лично установила только API/card mismatch имён файла; binary class contradiction атрибутирована W1-08.

#### W1-07-S05 — отказанный GitHub-кандидат с вводящим в заблуждение названием

[Re-surgence/Safety-Harness-Detection](https://github.com/Re-surgence/Safety-Harness-Detection/tree/fcd2eaceba53a703c0fe4da09cf6bd9a3dfe0390), commit **`fcd2eaceba53a703c0fe4da09cf6bd9a3dfe0390`**. **A:** API `license=null`; `models/best.pt` 19184474 bytes; weights не скачаны. [src/ppe_realtime_alert.py](https://raw.githubusercontent.com/Re-surgence/Safety-Harness-Detection/fcd2eaceba53a703c0fe4da09cf6bd9a3dfe0390/src/ppe_realtime_alert.py) прочитан: map `helmet/gloves/vest/boots/goggles/none/Person/no_helmet/no_goggle/no_gloves/no_boots`; привязи/стропа/анкера нет. Код объявляет `vest/harness` missing, когда не найден **любой vest во всём кадре**. Это не harness-detector и неверная person association для нескольких людей. Отказ от кандидата; название README не доказательство классов. Лицензии кода, весов и данных не установлены.

#### W1-07-S06 — новая исследовательская зацепка про hook, не готовый MVP

[Yao et al., Sensors 2026, 26(13), 4147](https://www.mdpi.com/1424-8220/26/13/4147), DOI `10.3390/s26134147`; [versions](https://www.mdpi.com/1424-8220/26/13/4147/notes): HTML update 2026-09-04. **C:** YOLO-ILB различает `helmet/no-helmet/harness/no-harness/safety hook`; 2700 изображений DJI Mini 3 Pro, 17 проектов; для hook авторы дают AP50 .851/recall .846. Предлагаются положение hook относительно harness и ограничение расстояния через размер bbox. **I:** такая 2D-геометрия — эвристика high/low anchoring, а не подтверждение замкнутой связи с разрешённым анкером. Вид сверху/наклон камеры/наклон человека меняют проекцию. Полный HTML при открытии дал 429, PMC — anti-bot; прочитаны индексированный первичный фрагмент и notes. Публичные точные веса/данные/код и условия доступа не установлены; не объявлять их существующими. Интересно для последующей R&D, не для немедленного запуска.

**Происхождение:** [W1-07.md](_WORK/W1-07.md), `## 3.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 3. Реальные правила: почему «на площадке без harness» не равно нарушение

#### W1-07-S07 — РФ, приказ 782н

[Первичная страница Минтруда](https://mintrud.gov.ru/docs/mintrud/orders/1822) лично открыта: приказ 16.11.2020 №782н, регистрация 61477, дата размещения 18.01.2021; содержит ссылку на приложение DOCX. Страница сохраняет первоначальное окончание 31.12.2025. Это **не** актуальная консолидированная редакция.

[Официальная публикация оригинала](https://publication.pravo.gov.ru/Document/View/0001202012160036) и [изменения 29.04.2025 №287н](https://publication.pravo.gov.ru/Document/View/0001202505300025) запрошены, но не прочитаны из-за timeout/недоступности. [Консолидированная правовая копия](https://base.garant.ru/75062122/53f89421bbdaf741eb2d1ecc4ddb4c33/) и [карточка актуальной редакции](https://www.consultant.ru/document/cons_doc_LAW_371453/) указывают редакцию 29.04.2025 и срок до 01.09.2031. Это вторичное размещение первичного нормативного текста, явно отделённое от официальной публикации; окончательная сверка официального приложения/изменений — открытый gate.

**D с указанным ограничением / W1-07-F08.** П.3: риск падения ≥1,8 м; также условия у неограждённых перепадов и ограждений <1,1 м; падение <1,8 м может входить в определение при работе над механизмами, жидкостью и другими указанными опасностями. П.4 требует оценки риска и локального учёта; п.6 предусматривает инженерные/коллективные меры. Приложение 10 различает удержание, позиционирование, страховку, спасение; наличие одного пояса не устанавливает требуемый состав системы. П.172 отдельно описывает страховочную систему при работе с приставной лестницы >1,8 м; п.174 запрещает поднимать/опускать груз по приставной лестнице. Порог 5 м в правилах о наряде не заменяет общее определение высотных работ.

**I:** для события нужны локальная зона/задача, требуемый тип защиты, разрешённые анкеры и исключения, известное наличие коллективной защиты, актуальная техкарта/ППР/инструкция. Из bbox нельзя прочитать наряд, паспорт анкера, способность выдержать нагрузку и исправность СИЗ. «Без harness на ограждённой площадке» нельзя считать нарушением без соответствующего правила для конкретной работы.

#### W1-07-S08 — OSHA, контроль смысла компонентов, не право РФ

[Официальная интерпретация 08.02.2011](https://www.osha.gov/laws-regs/standardinterpretations/2011-02-08), §1926.502(d)(15): anchorage независимо от крепления подвесной платформы; 5000 pounds/работника либо проектная complete-system альтернатива с safety factor ≥2 под надзором qualified person. [Официальное пояснение системы](https://www.osha.gov/sites/default/files/publications/OSHA3146.pdf) различает anchorage, connectors и body harness, возможные lanyard/lifeline/deceleration device. Доступен индексированный текст первичного источника; прямое открытие документов дало 403. **I:** видимая труба не раскрывает сертифицированную несущую способность. Числа OSHA нельзя переносить в российский event-rule. Ссылка полезна для семантики, не для автоматического юридического решения.

**Происхождение:** [W1-07.md](_WORK/W1-07.md), `## 4.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 4. Быстрая условная цепочка и temporal event

**P / W1-07-F09.** Если организатор предоставляет пригодную зону/видео и разрешает узкое именование:

1. Intake: камера и неподвижный ракурс; обследованная зона; нормативное правило `harness_required`; примеры нескольких систем/цветов СИЗ, разрешённое видео. Разметить видимость и unknown до запуска модели.
2. Получить pinned S02 `v2/best_640.onnx`, проверить SHA256, фактический граф и operators; воспроизвести S03 preprocessing. Проверить RGB, layout, normalized range, pad/scale, output decoding и NMS. Это уже экспортированный сторонний ONNX; наша конверсия/исполнение ещё не доказаны.
3. Нейросеть выдаёт Person/No_Harness, затем tracker/association и zone gate. Если естественные Person boxes часто отсутствуют, не лечить это уверенным присвоением NO-X ближайшему человеку; измерить и исключить неоднозначность.
4. Evidence state на `(camera, zone, track)`: `out_of_scope → observed → candidate → active → resolved`. Candidate нарастает лишь по пригодным кадрам, где torso виден, человек в нужной поверхности, принадлежность NO-X однозначна; unknown не считается подтверждением. Длительный unknown завершает наблюдаемость с причиной, а не «нарушение устранено».
5. Начальный инженерный параметр для исследования: согласованный кандидат ≥1 с в окне 2 с; это не нормативный срок и не измеренная оптимальная настройка. Считать wall-clock timestamps, не число кадров после drop. Окклюзии и краткие пересечения не создают повторного события.
6. `active` порождает **один** incident_id, evidence frame/клип, время/камеру/зону, формулировку наблюдения и основание локального правила. Дальнейшие кадры дополняют его; rearm только после подтверждённого выхода/устойчивого устранения и guard interval. Разрыв track не должен автоматически создавать новый инцидент: короткое сопоставление по зоне/времени/траектории; при сомнении пометка оператору, без выдуманной идентичности.
7. LinQ: спросить доступные exporter/ONNX operators/opset, static-shape/dtype, supported device; compiled artifact и успешный запрос на реальном устройстве фиксировать отдельно. Если opset20 не поддерживается, нужен проверенный другой экспорт/компиляция с parity, не обещание «YOLO поддерживается».

Завершённость уровней сейчас: **family named — да; exact weights metadata — да; exported ONNX listed — да; binary verified — нет; locally inferred — нет; LinQ compiled — нет; hardware measured — нет; event validated — нет**. Скорости S01/S02/S06 и результаты GPU/CPU автора не являются LinQ FPS.

**Происхождение:** [W1-07.md](_WORK/W1-07.md), `## 6.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 6. Дополнительно: переноска груза (ограниченный объём)

**I / W1-07-F11.** По видео можно наблюдать факт совместного движения человека и предмета, число видимых носильщиков, примерную позу/положение рук/наклон корпуса, маршрут, столкновение/падение предмета, вход с грузом на лестницу. Нельзя надёжно получить массу закрытого ящика, центр тяжести/содержимое, индивидуальную допустимую нагрузку, реальный хват/усилие и накопленную нагрузку смены. Большой ящик может быть пустым; маленький — тяжёлым. Класс `person carrying box` не равен `improper carrying`.

#### W1-07-S09 — первичная методика NIOSH

[CDC/NIOSH RNLE](https://www.cdc.gov/niosh/ergonomics/about/rnle.html), 21.02.2024, раздел Key variables; [Applications Manual, revision 09/2021](https://www.cdc.gov/niosh/docs/94-110/default.html), DOI `10.26616/NIOSHPUB94110revised092021`. **D:** RNLE — оценка двухручного подъёма; нужны масса, горизонтальное/вертикальное положение рук, вертикальное перемещение, асимметрия, частота/длительность/отдых, качество захвата. LC 23 kg относится к идеализированному подъёму с коэффициентами, а не универсальному разрешённому весу переноски. **I:** видео без метрики/массы/контекста не вычисляет содержательный LI и не даёт юридический вердикт. RNLE не универсальная модель ходьбы с грузом/одноручной переноски.

#### W1-07-S10 — РФ, нормативный scope

[Приказ 753н, консолидированный текст, разд.V п.34–35](https://base.garant.ru/75057534/53f89421bbdaf741eb2d1ecc4ddb4c33/), редакция 29.04.2025; [публикационная карточка](https://www.consultant.ru/document/cons_doc_LAW_370924/2ff7a8c72de3994f30496a0ccbb1ddafdaddf518/). Это правовые копии, не лично прочитанная официальная публикация. П.34 относится к разовому подъёму **без перемещения** (50/15 кг), п.35 имеет отдельные правила механизации/ответственного лица. Не переносить эти числа в общий детектор переноски. Для работниц/возраста/частоты и иных условий нужны применимые специальные нормы и утверждённая процедура; пол/возраст/медицинские допуски не выводить по внешности.

Быстрый пригодный вариант — конкретное локальное правило: например, запрещённый маршрут с любым грузом определённого проверяемого типа либо подъём/спуск груза по приставной лестнице (S07 п.174). Нужны person+объект, связь рук/движения, ladder/route context и temporal state; для произвольного «груза» готовая проверенная модель/веса здесь **не установлены**. Альтернатива — известный маркированный SKU/масса из справочника и требование двух носильщиков по процедуре; CV лишь подтверждает наблюдаемое число/маршрут, а не взвешивает. Обязательные negative controls: пустые руки, тележка, пустой контейнер, два человека рядом без совместной переноски, скрытые носильщики. Без такой конкретизации сценарий №8 исключить из MVP.

<a id="F032"></a>
## F032 — Height video donor и data-observability controls редких признаков

**Нормализованный статус и условия:** Open-Site4video payload/download/grant не получены; camera-specific diagnostic size после actual resize. Нет универсального минимальногоNpx. Не обнаружено не равно verified absence.

**Источники:** [S360](SOURCES.md#S360).

**Происхождение:** [W1-11.md](_WORK/W1-11.md), `### W1-11-S12`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### W1-11-S12 — Новый Open-Site Monitoring Dataset: релевантное construction video, но payload не получен

[Wu et al., Remote Sensing15(2),347](https://www.mdpi.com/2072-4292/15/2/347), DOI10.3390/rs15020347,2023, §4.1. Direct open429; прочитан индексированный первичный полный раздел. **W1-11-F16 / C:** авторы описывают4196 harness-related images (Google/construction sites),4 video/7200 frames,30fps2560×1080; три высотные сцены и одна наземная; video boxes worker/helmet/harness,3633 attribute crops из тех же материалов. Numeric IDs, конкретный download/checkpoint/лицензия исходных media не установлены; «open-site» в названии не равно открытым файлам.

Потенциально ближе к задаче, чем общие фото PPE, но сейчас **неusable немедленно**: нет exact payload. Attribute crops не независимый test относительно родительских videos/images. Нет доказательства hook connection labels, наблюдаемого анкера, локальных surface zones. Не подставлять эти4 авторских видео в демо как скачанные. Это точечный future contact/acquisition lead, без отправки сообщений авторам.

**Происхождение:** [W1-11.md](_WORK/W1-11.md), `## 7.`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### 7. Негативные контроли, observable labels и малые объекты

**W1-11-F24 / P:** минимальный source-to-target pilot должен проверять диагностическую видимость после фактического preprocess LinQ. Сохранять native resolution, исходный и transformed bbox min-axis телефона/сигареты/лямки/карабина; crop делать из исходного кадра, а не после потери деталей в640. Единого доказанного «минимум N pixels» здесь нет. Наличие класса в checkpoint не доказывает, что он различим на данной дистанции. Отдельные labels: `positive_visible`, `verified_negative_visible`, `unknown_occluded_or_tiny`, `out_of_scope`. Не засчитывать unknown как безопасное поведение.

| Сценарий | Positive control | Обязательный negative/control с тем же ракурсом | FN / unknown |
|---|---|---|---|
| Phone use | Ввод/взгляд на phone и отдельно call; временное пересечение с walking одного person | Phone у бедра; на столе; рация, scanner, clipboard, tool; человек остановился вне запретной зоны | Экран/объект за рукой; handsfree; phone несколько pixels |
| Smoking | Видимая сигарета+курительный жест на разрешённом архивном/постановочном материале | Вода/еда/ингалятор/кашель/ручка/соломинка/телефон; сигарета переносится без smoking | Cigarette закрыта пальцами; отсутствие видимого выдоха не negative |
| Flame/smoke | Реальная flame/smoke область; отметить allowed/process flame отдельно | Пар, пыль, fog, glare, orange PPE, welding, отражение огня на экране; разрешённая горелка | Малое пламя/дым на сходном фоне; цеховой пар неизвестного состава |
| Harness/height | Только visible absence в заданной surface zone либо конкретно размеченное connection evidence | Привязь надета и соединена; жилет/пояс без привязи; ground на той же проекции; guardrail; два работника | Спина/строп закрыты; второй строп неизвестен; anchor вне кадра |
| Climbing | Полный подход→перенос корпуса через определённое ограждение→другая сторона | Разрешённая лестница, gate crossing, поднятая рука, step-up, попытка без завершения, indoor climbing | Ноги/верх fence скрыты; исчезновение за стеной без доказанного маршрута |

**Temporal/dedup:** labels данных не заменяют событийный GT. Для каждой выбранной камеры отдельные onset/offset/unknown и track ownership; candidate подтверждается только валидным наблюдением, active создаёт один event_id. Краткая окклюзия обновляет unknown, не новое событие; завершение/повторный вход — после подтверждённого reset. Конкретные hold/gap параметры брать из общего evaluation pilot, не из длительности source video. Ни один рассмотренный source не даёт достаточный знаменатель long safe factory camera-hours для эксплуатационных FP/hour.

<a id="F033"></a>
## F033 — Data protocol: rights/use, actor-level GT, source grouping, freeze и event counts

**Нормализованный статус и условия:** Исторический абзац W1 о неизвестной identity старых четырёх MP4 заменяется F015. Все просмотренные файлы dev/reviewed. Proposed60–90min/gates — не результат измерения и не обязательство по сроку.

**Источники:** [S059](SOURCES.md#S059), [S062](SOURCES.md#S062), [S064](SOURCES.md#S064), [S077](SOURCES.md#S077), [S112](SOURCES.md#S112), [S361](SOURCES.md#S361), [S362](SOURCES.md#S362), [S363](SOURCES.md#S363), [S364](SOURCES.md#S364).

**Происхождение:** [W1-12.md](_WORK/W1-12.md), `## Первичные основания`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Первичные основания: новые независимые проверки

Все даты доступа ниже — 2026-10-23. Пересказы содержательны, дословные источники целиком не копируются.

| ID | URL / версия / локатор | Что непосредственно установлено и предел |
|---|---|---|
| W1-12-S01 | [Mendeley V1](https://data.mendeley.com/datasets/xjmtb22pff/1), DOI `10.17632/xjmtb22pff.1`, Description/Steps/Licence | Страница открыта вебом. Данные CC BY 4.0; авторы заявляют разрешения предприятия и работников, 691 clips с двух IP-камер за 39 дней. Это заявление владельцев, не просмотр отдельных согласий. Footer про AI rights делает исключение для open access CC-условий; его нельзя читать как отмену лицензии этого dataset. |
| W1-12-S02 | [CC BY 4.0 legalcode](https://creativecommons.org/licenses/by/4.0/legalcode.en), §1(i), §2(a), §2(b), §3(a), §5 | Лицензия включает воспроизведение, распространение и публичный показ/исполнение в рамках прав лицензиара. Условия: авторство, источник, лицензия, указание изменений и сохранение предоставленных notices. Privacy/publicity/personality, товарные знаки и гарантии прав третьих лиц этим не обеспечиваются. |
| W1-12-S03 | [Zenodo record API](https://zenodo.org/api/records/13354453), record 13354453, DOI `10.5281/zenodo.13354453` | Собственный requests GET HTTP200, 3,960 bytes JSON. `metadata.resource_type.type=dataset`, `version=v2.1`, `license.id=cc-by-4.0`, `access_right=open`, creator Ekram Alam. Related identifier указывает GitHub tree/v2.1. Created `2024-08-21T11:27:08.081579+00:00`, updated `2024-08-21T11:30:20.962050+00:00`. HTML Zenodo веб-инструментом дважды timeout, поэтому вывод основан именно на реально полученном API JSON. |
| W1-12-S04 | [GitHub LICENSE exact commit](https://raw.githubusercontent.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/5abac7693229900cf80f722e878fbb119211fc1c/LICENSE), [README](https://github.com/ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos/blob/5abac7693229900cf80f722e878fbb119211fc1c/README.md) | LICENSE GET200, 1,067 bytes: MIT, copyright 2024 Ekram Alam, scope сформулирован Software. README citation ещё указывает v2.0 DOI `12921216`; не подменять им actual v2.1 sample revision. Сохранить обе маркировки, не выбирать удобную молча. |
| W1-12-S05 | [GMDCSA article fullTextXML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11416611/fullTextXML), DOI `10.1016/j.dib.2024.110892`, §4 и Ethics Statement | Собственный GET200, 201,615 bytes. В §4 четыре subjects/три дома, Subjects2/3 одна комната; consent о dataset use. Ethics сообщает три actors, двое авторы/волонтёр, подписанное informed consent и знание о размещении в public repository. Численное противоречие не устранено; scope дальнейшего коммерческого показа consent не раскрыт. Основная PMC HTML выдала CAPTCHA, XML прочитан штатным публичным API без обхода ограничений. |
| W1-12-S06 | [Zenodo licenses docs](https://help.zenodo.org/docs/deposit/describe-records/licenses/), Licenses and rights/Mixed license uploads | Первичная документация открыта: CC BY — default при deposit, возможны mixed-license uploads. Следовательно, metadata S03 — реальное основание, но default не доказывает, что загрузчик специально развёл видео и код. Не выдавать общую лицензию метаданных Zenodo CC0 за лицензию MP4. |
| W1-12-S07 | [Creative Commons AI-training primer](https://certificate.creativecommons.org/using-cc-licensed-works-for-ai-training-2/), §§How to Follow/When Conditions Apply | Первичный разбор открыт. Авторское право и исключения зависят от юрисдикции/действий; training обычно предполагает копирование, а NC относится к uses requiring permission. Консервативные рекомендации primer не являются доказанным универсальным правилом, что любой обученный model автоматически derivative/SA. Здесь обучение не требуется. |
| W1-12-S08 | [YouTube terms](https://www.youtube.com/static?template=terms), дата документа 15.12.2023, Permissions and Restrictions | Открытая текущая страница допускает личный просмотр и embedded player; загрузка/изменение/перераспространение ограничены разрешениями сервиса/правообладателей. Право воспроизведения через embed не является лицензией на извлечение MP4, inference dataset или включение чужого ролика в конкурсную запись. |

Zenodo S03 содержит один ZIP `ekramalam/GMDCSA24-A-Dataset-for-Human-Fall-Detection-in-Videos-v2.1.zip`: **1,107,545,615 bytes**, `md5:3d36f2c5c1a666b99639e4e9fd843efb`, file id `8e43833c-22d9-4ee7-9aa7-32ce5c9dcbe6`. Архив **не получен**, соответствие его members GitHub MP4 **не проверено**. Поэтому нельзя утверждать, что каждый локальный GitHub binary был сверён с лицензированным ZIP. Связка author/версия/related identifier сильная, byte identity остаётся неизвестным.

**Происхождение:** [W1-12.md](_WORK/W1-12.md), `## Формализованный протокол`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Формализованный протокол отбора

**Gate A — provenance/access.** На каждый candidate записать source owner/DOI/revision/exact path, HTTP result, локальные bytes/hash, decoder result, контейнерный codec/размеры/PTS, дату. Все mirror files связать с оригиналом; если byte identity не проверена, оставить это отдельным unresolved полем. HEAD200 и filename недостаточны. Не считать broken file отрицательным событием.

**Gate R — rights.** Отдельные поля `copy`, `inference`, `training`, `presentation_live`, `presentation_recorded`, `redistribute`, evidence URL/scope, notices, consent assertion и unresolved. Отсутствие запрета не записывать как разрешение. Для этого MVP training=false. Показ на защите и последующая публикация в соцсети — разные planned uses. Если public-use gate не закрыт, допустимо завершить internal research и заменить только демонстрируемые media на собственные; сами исследования не блокируются.

**Gate S — semantics/observability.** Два человека команды последовательно размечают весь выбранный clip, второй проверяет спорные интервалы. Unit: actor×rule episode, а не clip class. Поля: `camera/view`, `source_session`, `actor_id`, `[visible_start,end]`, onset interval, offset, initial occupancy, allowed/forbidden/unknown, footpoint/pose reliability, active duration, occlusion, why label, annotator/adjudication. Пограничные/скрытые стопы — unknown, а не safe. Не считать весь fall-labeled clip падением, не превращать движение в конце в неподвижность.

**Gate I — independence.** SHA256 выявляет точные копии. Проверка контактных кадров/перцептивных fingerprints и временной непрерывности выявляет transcodes, соседние обрезки, одинаковых actors/background и перекрывающиеся окна; fingerprints — только повод ручной проверки, не доказательство тождества. Group key содержит исходную запись/сессию, view, subject/room, scenario generation seed для синтетики. Соседние clips и синхронные views одной сцены не разносить в dev/test. У Safe/Unsafe исходные timestamps в просмотренных manifests не установлены: не писать leakage-free. Разбиение GMDCSA по кадрам особенно недопустимо.

**Gate D — domain/controls.** Каждый сценарий обязан иметь positive, обычный negative, hard negative, unknown и rearm/dedup case. Пылевые/ночные/малые actors/PPE/индустриальный пол не представлены GMDCSA: пометить OOD gaps. Safe/Unsafe даёт реальную CCTV геометрию, но выбранные clips короткие и curated, а не natural stream. Фото годятся для detector smoke, не для события с hold/trajectory/падением.

**Gate P — freeze.** Четыре текущих файла имеют статус reviewed/dev/demo. До holdout фиксируются model weights/hash, preprocessing/class mapping, tracker/thresholds, ROI/исключения, hysteresis/hold/clear, rearm, scoring policy. Не менять forbidden polygon под конкретного человека после просмотра результатов. По результатам tuning clip становится dev навсегда; новый holdout брать из другой исходной session, а camera generalization — из другого реально подтверждённого вида.

**Происхождение:** [W1-12.md](_WORK/W1-12.md), `## Быстрый smoke`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Быстрый smoke-test — предложен, НЕ выполнен

За 60–90 минут инженерной работы после доступного LinQ и выбранных weights можно подготовить разметку четырёх файлов и пройти smoke gate, но это оценка бюджета, не замер. Изначально продемонстрировать два ограниченных claims без третьего сценария.

1. Просмотреть полные 28.39s в исходном времени, проверить всех видимых actors и PTS. В F04/F05 вручную уточнить переходы; в F06/F07 определить corridor/рабочие островки до вывода model. Записать спорные интервалы unknown. Freeze manifests/config и исходное видео; не подменять его замороженным кадром/повтором для достижения hold.
2. Реальный путь: decoder→нейросеть **на LinQ**→boxes/pose→tracks→rule state→одна запись/episode→GUI/journal. Успешный ONNX/заранее нарисованная overlay не считается запуском LinQ. Сохранить runner/version/export artifact/hash и actual hardware. Конкретные веса/I-O/export остаются у модельных веток; данные не доказывают совместимость.
3. Fall state: standing/moving→candidate rapid descent→low posture; low-motion — отдельный измеримый признак с visibility gate. F05 не должен давать fall alert только из-за lying; F04 не должен давать «бессознательный». Если выбранный hold превышает доступный post-transition interval, outcome censored/непроверен.
4. Zone state: outside→candidate→active→clear с hold по PTS; initial occupancy помечается отдельно. F06 expected event относится к заданному actor/corridor; F07 target на дорожке не должен тревожить. Работа у станка не становится нарушением по классу clip. Unknown не превращается в доказанный safe.
5. Дополнительные controls потребуют собственной безопасной записи: ходьба вдоль границы без входа; краткая окклюзия одного episode; выход и повторный вход; два человека с разными событиями; длительное неподвижное лежание с безопасной постановкой, смена позы, медленное укладывание. Ни опасный контакт с техникой, ни настоящее падение ради съёмки не нужны. Эти файлы пока отсутствуют.
6. Доставленные записи сопоставить с actor×rule episodes один-к-одному; eligibility и допустимую задержку зафиксировать до run. Один matched alert — TP, второй на тот же episode — duplicate, unmatched assertion — FP либо unresolved, unmatched eligible event — FN. Clip, начинающийся внутри события, не даёт entry-onset latency. Не вводить tIoU для нулевой по длительности notification без отдельного определения.
7. Отчёт: сырые TP/FP/FN/U и duplicates по clip/actor/rule, время negative/unknown exposure, decoder/drop failures; время model и всей цепочки отдельно. Source PTS latency и monotonic wall-clock input→GUI delivery — разные clocks. Для recorded replay раскрыть speed. Четыре clips не дают достоверных p95 по событиям или производственной точности. У curated negative footage можно показать descriptive FP/min именно этих фрагментов, но не ожидаемые FP/camera-hour завода. Не нормировать на длину повторного показа одного файла как на независимую экспозицию.

Критерий принятия именно smoke: все заранее размеченные видимые cases пройдены либо failure явно локализован; F05 без false fall; F07 safe target без zone false alert; active episode создаёт одну запись; реальные LinQ outputs и журнал доступны; неразрешённые случаи раскрыты. Это **предложенный командный gate**, не официальный критерий организатора и не требование достичь процента на четырёх файлах. Не объявлять pass до фактического run.

<a id="F034"></a>
## F034 — Temporal/tracker/event: выбранный fixed-cadence route, TTL, ledger и matching

**Нормализованный статус и условия:** Весь adapter/ledger design NOT_IMPLEMENTED/NOT_RUN. Source inspection и малые арифметические проверки выполнены. dt1 допустим как fixed analysis step; pre-association purge нужен для строгогоTTL, не объявление framework bug. UI exactly-once ограничен сохранённой БД и keyed consumer.

**Источники:** [S030](SOURCES.md#S030), [S031](SOURCES.md#S031), [S365](SOURCES.md#S365), [S366](SOURCES.md#S366), [S367](SOURCES.md#S367), [S368](SOURCES.md#S368), [S369](SOURCES.md#S369), [S370](SOURCES.md#S370), [S371](SOURCES.md#S371), [S372](SOURCES.md#S372), [S373](SOURCES.md#S373), [S374](SOURCES.md#S374).

**Происхождение:** [W2-08.md](_WORK/W2-08.md), `полный файл`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.


Дата исследования и доступа: **23.10.2026**. K009/K011. Первичные исходники открыты заново; чужой код не исполнялся. Прочитаны полный W1-15, W1-16, релевантные smoke6–7 и протокол W1-12, K009/K011 в корневом CRITIC.md и уточнение в PROMPT_W2-08.md. Это инженерный handoff, **не приложение, NN/video benchmark, LinQ measurement или executable event PASS**. В этой ветке нет SDK, устройства и учётных данных. Все параметры ниже — конфигурация предлагаемого опыта, не официальные нормы безопасности.

#### Решение и значение для выбора

Выбрать для первого smoke **прямой pinned FoundationVision ByteTrack на равномерной сетке анализа**, с закрытием каждого шага ровно один раз, empty-update на пропусках, явным pre-association TTL pruning и внешним persistent episode ledger. Первый cadence-кандидат 5 Hz, не обязательный FPS; сначала один camera/stream и batch1, не более одного незавершённого логического запроса на камеру. LinQ даёт только perception; этот документ не утверждает доступность конкретного detector/pose.

**dt=1 допустим как один шаг анализа** при постоянной сетке. Ошибка — менять реальное время между update, сохраняя прежний смысл velocity, noise и TTL. Мы не меняем dt одной строкой и не заявляем физическую оптимальность covariance на любом FPS. Нужны последующие реальные phase/drop/gap controls. Стандартный Ultralytics tracking callback не подходит без изменения: на пустых detections он не продвигает tracker.

Для событий выбран один собственный контракт person / pair / fire-region с однажды создаваемым episode_id и одной карточкой/строкой журнала. Готового внешнего executable once-per-episode reference с подтверждённым LinQ не найдено **в адресно проверенных исходниках**. Поэтому K009 **scoped**, K011 **scoped, execution open**; не closed и не end-to-end PASS.

#### Новые primary-source проверки

Все ссылки действительно открыты web GET 23.10.2026. Дата доступа не дата публикации. ByteTrack/Supervision/Ultralytics — ранее выбранные immutable revisions, проверенные повторно; дата их commit здесь не устанавливалась. DeepSORT HEAD разрешён дополнительно командой `git ls-remote https://github.com/nwojke/deep_sort.git HEAD`, результат `f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab`; далее прочитаны только pinned raw files, не движущийся master. README относит базовую работу к ICIP2017; это не дата текущего commit. SQLite — текущая, изменяемая документация.

| ID | Exact primary source / locator | Тип и установленное |
|---|---|---|
| W2-08-S01 | [ByteTrack byte_tracker.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py), `BYTETracker.__init__/update`, строки 134–263; `STrack.update/re_activate`, 54–81 | SOURCE CODE. Счётчик, association, expiry и activation; детали F01. |
| W2-08-S02 | [ByteTrack kalman_filter.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/kalman_filter.py), `__init__` 37–49, `predict` 97–111, `multi_predict` 157–175 | SOURCE CODE. F и Q, подробности F02. |
| W2-08-S03 | [ByteTrack basetrack.py](https://raw.githubusercontent.com/FoundationVision/ByteTrack/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/basetrack.py), 11–35, 46–50 | SOURCE CODE. `end_frame` возвращает последнее track.frame_id; ID counter class-level, mark_removed меняет state. ID не является глобальной идентичностью человека. |
| W2-08-S04 | [Ultralytics track.py](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/trackers/track.py), `on_predict_start` 31–45, `on_predict_postprocess_end` 62–78 | SOURCE CODE. Constructor `frame_rate=30`, empty detections → `continue`, затем лишь непустые попадают в update; persist/path управляют reset. Это другой ByteTrack implementation, не S01. |
| W2-08-S05 | [Supervision timers.py](https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/examples/time_in_zone/utils/timers.py), `FPSBasedTimer.tick` 27–45, `ClockBasedTimer.tick` 60–79 | SOURCE CODE. `setdefault` первого появления без удаления при выходе; clock-based использует datetime.now. Такой timer не continuous episode engine. |
| W2-08-S06 | [DeepSORT tracker.py](https://raw.githubusercontent.com/nwojke/deep_sort/f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab/deep_sort/tracker.py), `predict` 46–51, `update` 53–83, `_match` 84–118 | SOURCE CODE + inline documentation. Predict вызывается каждый time step перед update; appearance cascade и затем IoU. |
| W2-08-S07 | [DeepSORT track.py](https://raw.githubusercontent.com/nwojke/deep_sort/f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab/deep_sort/track.py), `predict/update/mark_missed` 105–143; [kalman_filter.py](https://raw.githubusercontent.com/nwojke/deep_sort/f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab/deep_sort/kalman_filter.py), 37–49, 97–110 | SOURCE CODE. age/time_since_update в шагах, измерение сбрасывает age-since-update, missed удаляется при `> max_age`; F с dt1. |
| W2-08-S08 | [DeepSORT README](https://raw.githubusercontent.com/nwojke/deep_sort/f08cf1dc470eeb1cd2add1cbf077d95ac6c48aab/README.md), Introduction, Generating detections, Highlevel overview | AUTHOR DOCUMENTATION. Appearance embedding и отдельный TensorFlow network/feature-generation path; не доказательство re-ID качества наших людей или совместимости LinQ. |
| W2-08-S09 | SQLite [UPSERT](https://sqlite.org/lang_upsert.html), §2, §4; [atomic commit](https://www.sqlite.org/atomiccommit.html), §§1–2,9 | DOCS. UNIQUE/PK может превращать повтор INSERT в update/no-op; atomic commit относится к одной транзакции с оговорками filesystem/flush/locking. Это база предлагаемого ledger, не гарантия внешней доставки. UPSERT появился 3.24.0 (04.06.2018); версия VM неизвестна. |

#### W2-08-F01 — Что фактически делает pinned ByteTrack

**SOURCE INSPECTION, S01/S03:** buffer=`int(frame_rate/30*track_buffer)`; frame_id растёт при update. High-score association включает tracked+lost, low-score association — ещё tracked. Reactivation может сохранить ID. Output — активированные tracked, а не все predicted lost. Последующая expiry проверяет `frame_id-end_frame > max_time_lost`. Новый track вне первого шага требует последующего подтверждения. Пятиколоночный input обрабатывается как bbox+score и автоматически масштабируется.

**Новый вывод из порядка операций:** association раньше expiry: lost с возрастом N+1 способен совпасть и обновить end_frame до проверки. Также вновь removed исключаются из lost не тем же самым newly-removed списком до его добавления. Для строгого TTL adapter обязан до association удалить expired/Removed из обоих входных списков; нельзя полагаться только на штатный хвост update. Это статический вывод, не воспроизведённый bug test.

#### W2-08-F02 — Что меняет движение, а что только срок жизни

**SOURCE INSPECTION, S02:** состояние `(x,y,a,h,vx,vy,va,vh)`, F содержит dt1; позиционные/скоростные шумы зависят от текущего h; covariance prediction — `F P Fᵀ + Q`. Аргумент frame_rate не поступает в этот фильтр. Повторные predict действительно меняют mean/covariance. ByteTrack дополнительно обнуляет velocity высоты у не-Tracked перед prediction [S01].

**DESIGN/INFERENCE:** менять frame_rate/buffer или внешний timeout — менять management, не физическую модель движения. Для variable-dt route пришлось бы согласовать F(dt), Q(dt), размерности velocity, measurement noise и missed-management; это не выбранный краткий путь. При равномерном cadence текущая модель работает в шагах сетки, а её adequacy на 5 Hz остаётся экспериментальным вопросом. Дополнительные empty updates делают множество однократных propagation, не один «магический» большой dt.

#### W2-08-F03 — Сравнение с одним близким documented route

| Аспект | Выбранный ByteTrack S01–03 | DeepSORT S06–08 |
|---|---|---|
| Время | predict внутри update; dt1; buffer scaled constructor | явно документирован predict перед каждым update; dt1; max_age в шагах |
| Пропуски | adapter вызывает update с empty `(0,5)` | клиент вызывает predict, затем update([]) |
| Идентичность | bbox/score association, lost reactivation | appearance cascade + IoU, отдельные embedding признаки |
| Почему не замена «из коробки» | нужен cadence/expiry/observed sidecar | тоже нет timestamp API и event engine; embedding требует дополнительного NN/artifact path |
| Решение | минимальный dependency footprint, выбран для smoke | полезный reference правильного разделения predict/measurement, отклонён как срочная замена |

Ни одна сравнительная строка не доказывает превосходство accuracy или скорость на LinQ. Appearance полезен потенциально, но не обещает восстановить любого человека после окклюзии.

#### Один frame / request / epoch contract (предлагаемый)

#### Время и sampling

`camera_id` постоянен для источника; `stream_epoch` — новый UUID при reconnect, PTS discontinuity/backward jump, смене geometry/cadence/rules/model contract либо невозможности безопасно восстановить stream после процесса. `run_id` отдельно обозначает запуск. **Ни PTS, ни track_id не ключ вне epoch.** Отдельный `tracker_generation` увеличивается при reset tracker без reconnect. Зависимые пары только внутри одного camera/epoch.

Сетка `s_k=s_0+kΔ`, Δ=1/f_analysis в source-time; `tick_seq=k`. Для первого file smoke брать регулярный PTS clip и фиксированную фазу; при 30→5 Hz каждый шестой кадр — пример, не предположение о любом файле. Для VFR/live заморозить допустимый jitter ε<Δ/2; единственный unique frame с PTS в `[s_k−ε,s_k+ε]` выбирается детерминированно по ближайшему PTS, при равенстве меньший frame_seq. Один frame не используется дважды. Offset `PTS−s_k` сохраняется. Это bounded approximation равномерной модели; если подходящего кадра нет — gap, не дублирование последней картинки. Порог ε и допустимый observed source-gap G задаются в manifest; произвольный VFR с большими jitter не считается покрытым этим route.

Frame envelope: `camera_id,stream_epoch,frame_seq,source_pts_int,time_base_num/den,source_time,decode_status,original_W/H,transform_id,input_hash,t_receive_mono,t_decode_mono`. frame_seq — номер decoded кадра, не номер inference. Source PTS сохраняется исходным rational; missing PTS → invalid/unknown, без назначения текущего времени. Для replay отдельно `playback_speed,phase,t_release_mono`. Source-time нужен правилам/скорости; host monotonic — очередям/timeout/latency. Camera UTC age публикуется лишь при проверенном clock mapping, иначе receive-age proxy.

#### Запрос и упорядочение

Logical `request_id` связан с одним `(epoch,tick_seq,frame_seq,input_hash,model_hash)`; retry использует тот же request_id и новый attempt_id. Provider job ID отдельный. Если API не поддерживает idempotency, повторное NN выполнение возможно; локальная exactly-one **assimilation** обеспечивается commit watermark, а не заявлением о сервере. Completion = реально доступные выходы, не HTTP accepted.

На камеру один последовательный commit writer. Каждый tick закрывается при valid completion либо истечении bounded deadline B по локальным monotonic часам; B заморожен и измеряется отдельно от source H_on/H_off. Пока предыдущий tick не закрыт, следующий не ассимилируется. Если следующий кадр уже пришёл, mailbox хранит bounded latest eligible frame, вытесненные ticks становятся gaps. Это жертвует throughput ради понятного первого smoke. После deadline нельзя продлить старый запрос новым attempt без общего bound: tick уже gap. Output завершившегося позже, повтор, старый epoch, чужой model/input hash → audit `late/duplicate/wrong_epoch/invalid`, **ноль tracker/rule updates**. При потенциальной асинхронности reorder buffer ограничен B; commit всё равно строго k. Не переигрывать прошлые решения задним числом в online режиме.

Когда source останавливается, watchdog помечает active episodes UNKNOWN по wall-clock age. Нельзя выдумывать будущие source PTS ради наращивания rule hold. При возобновлении короткий известный source gap заполняется пустыми ticks; если gap превышает configured catchup/reset budget — новый epoch/generation и UNKNOWN, без огромного цикла predictions.

#### Один tracker step на закрытый tick

1. До association purge из tracked/lost каждый `Removed` и track, для которого `k-last_measurement_tick>N`; last_measurement_tick sidecar обновляется только от matched detection. Новый generation получает новый namespace. N — целое число шагов, выбранное из желаемого `T_track`; зафиксировать rounding `N=floor(T_track/Δ)`. Для S01 можно задать `frame_rate=f_analysis`, `track_buffer=30*N/f_analysis`; после constructor проверить фактический `max_time_lost==N` из-за int/float округления, при необходимости явно присвоить N. Нельзя подменять это camera FPS.
2. На valid detector frame передать class-specific detections в один tracker instance на класс (person, machine); не позволять class switch через общий class-agnostic association. Для 5 columns — FP bbox+score; передавать **копию** boxes в координатах original image и `img_info=img_size=(H,W)` для scale1. Undo-letterbox выполнен до этого; не применять второй inverse transform. Сохранить raw measured boxes/keypoints и det_id.
3. На timeout/missing/failed frame вызвать update с пустым float ndarray `(0,5)` и тем же geometry. Это prediction/management, не успешный detector negative. При successful no-detection frame также empty input, но sidecar status иной. Пустой ndarray достаточен по прочитанной ветке; совместимость numpy/SciPy/старого np.float требует runtime smoke, пока NOT_RUN.
4. Сохранить `track_id,tracker_generation,matched_det_id,last_measured_pts,observed_this_tick,measurement_quality,predicted_geometry`. Для exact mapping det_id через все association stages нужен маленький hook в `update/re_activate/activate`; IoU guessed mapping постфактум не подходит при двух пересекающихся людях. Состояние после Kalman correction — оценка, не исходная measured bbox. Для speed/pose evidence брать реальные measurement PTS; prediction-only не заполняет историю позы/скорости.
5. Ниже отдельно рассчитывать правило `POSITIVE / NEGATIVE / UNKNOWN` и reason. Low-score association может сохранить ID, но не обязан удовлетворять evidence-quality gate. Даже matched track с плохими keypoints — UNKNOWN для pose-rule. Утрата объекта не равна доказанному прекращению поведения.

#### Один episode interface, три entity variants

Вход rule sample: `(camera,epoch,rule_id,rule_version,entity_key,tick_seq,source_pts,evidence_frame_id,polarity,quality,reason,observed_members)`. Порог/ROI/motion definition входит в config hash. Generic zone не превращается этим контрактом в исходный behavioral scenario.

| Variant | entity_key и наблюдаемая поддержка | Прекращение / неоднозначность |
|---|---|---|
| person | stable local person_uid, map `(generation,track_id)→uid`; правило использует тот же person и измеренные pose/action/trajectory признаки | отрицательный признак у видимой персоны при достаточной quality; потеря/невидимые детали → unknown |
| person–machine pair | ordered `(person_uid,machine_uid)`, rule_id; оба объекта из одного source frame, измеренное движение machine из реальной истории, контекст геометрии | устойчивое наблюдаемое separation/остановка при валидной visibility; один пропавший член → unknown. Разные люди около той же machine — отдельные пары |
| fire region | camera/zone/rule + `region_uid`, bounded one-to-one spatial association измеренных regions через время | successful valid view с достаточной видимостью ROI и устойчивым отсутствием fire может быть negative; detector absence всё равно не гарантия отсутствия огня. Split/merge/occlusion → ambiguous, сохранять lineage. Smoke class сам по себе не fire/smoking |

Person/machine uid создаётся при первом подтверждённом track. Если tracker сохранил ID, сохраняется uid. Если ID новый, bounded reacquisition gate использует class, время ≤T_link, geometry/motion envelope и one-to-one assignment. Для auto-link требуются единственный допустимый predecessor и successor с margin; distance/IoU/margin/T_link — конфиг. При двух допустимых людях не угадывать. `identity_unresolved` сохраняет старый OPEN как UNKNOWN, новый candidate не выпускает повторный alert до разрешения связи/наблюдаемого clear. Это сознательный риск FN/задержки: альтернативная политика «немедленно новый episode» увеличивает duplicates; выбранную политику раскрыть. Нельзя обещать одновременно zero-duplicates и zero-misses при полной потере identity.

Region использует отдельный spatial associator, не модель пешеходной скорости ByteTrack. Два удалённых очага — два uid; расширение одной связной области — update. Если один очаг распался на два перекрывающихся фрагмента, сохранять родительский episode и evidence children; при merge независимых очагов не удалять прежние IDs, помечать ambiguous lineage. Универсального физического определения «тот же огонь» из bbox нет; заранее задать GT policy по ROI/связности и unknown для спорного.

**W2-08-F04 [DESIGN] — операции:** `candidate`, `open`, `update`, `unknown`, `clear`, `rearm`; дополнительно `ack` и `delivery_attempt`, которые не являются наблюдением поведения. На `open` выделяется persistent episode_id. Канонический `event_id=episode_id`; `(event_id,revision)` — версия состояния, `(event_id,notification_kind='open')` — ключ единственного пользовательского уведомления. Snapshot/evidence могут дополняться без новой карточки. Не key из округлённого timestamp/class/global cooldown.

Для минимального smoke H_on/H_off подтверждаются **непрерывной цепочкой валидных samples одной polarity**, min observations m, span по реальным PTS ≥H, соседние source gaps ≤G. Это sample-supported continuity, не доказательство всех мгновений между кадрами. UNKNOWN разрывает/обнуляет candidate и clear chain. Уже OPEN остаётся тем же episode с uncertain=true; время UNKNOWN не прибавляется к observed_positive_duration. Возврат POSITIVE в том же identity продолжает OPEN без нового уведомления. NEGATIVE начинает clear chain; до H_off episode RECOVERING; POSITIVE отменяет recovery. При H_off — CLEAR с `clear_source_pts`, evidence и uncertainty interval, затем REARM после configured наблюдаемого safe interval R (может быть0). Новое нарушение до rearm сохраняется как suppressed/unresolved, а не бесшумно исчезает из evaluation. ACK оператора только изменяет ack fields.

`onset` — интервал от последнего надёжного negative до первого positive; `confirm_source_pts` — текущий source time, `t_confirm_mono` — wall clock принятия. Не подменять onset временем confirmation. При positive с первого видимого кадра `initial_occupancy=true,onset_left_censored=true`; допустим отдельный initial-state alert после H_on, но entry latency не вычисляется. При clip end/stream loss OPEN заканчивает запись периода наблюдения `right_censored`, не observed clear. Превышение UNKNOWN retention может архивировать episode как unresolved/censored, не как safe.

#### UI once, доставка, retry и restart — граница обещаний

**W2-08-F05 [DESIGN, механизм S09]:** минимальный предлагаемый consumer — UI, читающий локальный ledger, а не произвольный push endpoint. В одной SQLite transaction записывать processed tick watermark, изменения episode и outbox open; UNIQUE episode_id и UNIQUE `(event_id,notification_kind)`. UI показывает одну keyed карточку, журнал одну keyed строку, detail/history revisions внутри. Доставка outbox допускает повтор attempt с тем же event_id, UI refresh строится из ledger. Пользовательский ACK не закрывает событие. Append-only audit attempt records — не дополнительные «нарушения».

Crash до transaction commit не создаёт видимой карточки; crash после commit до delivery ACK вызывает повтор той же записи/идентификатора. Это даёт idempotent materialized view **в пределах сохранённой БД и согласованного consumer**, а не универсальный exactly-once транспорт. Если внешняя UI/сервис не принимает event_id/idempotency key или делает отдельный toast на каждый retry, единственность внешнего уведомления неизвестна. Тогда delivery статус accepted не называть visible; необходимо поменять consumer/проверить его фактический API.

Restart процесса: outbox и ранее созданные event IDs восстанавливаются из БД; незавершённые episodes получают UNKNOWN. **Мы не заявляем восстановление Kalman/identity по одному ledger.** Для минимального live route новый stream_epoch и tracker_generation; старые callbacks отвергаются. Продолжающаяся сцена после restart — initial occupancy и возможная связь с прежним OPEN, а не доказанный новый onset. Единственная уверенная связь по bounded reacquisition policy продолжает старую карточку; иначе остаётся unresolved, новые соответствующие alerts блокируются до наблюдаемого clear/rearm или явного identity resolution. Это ограничивает функциональность после restart, но не выдумывает бесшовный once-per-physical-event. Для требования бесшовного продолжения нужен отдельный восстановимый snapshot tracker+uid+rule state либо детерминированный replay сохранённых результатов от checkpoint с теми же версиями; такой adapter **не написан и не проверен**. Потеря/удаление БД вне guarantee.

#### Маленькие counterexample timelines

**W2-08-F06 [OWN BOUNDED ARITHMETIC / DESIGN TRACE]:** ниже ручные детерминированные таблицы по формуле конструктора/контракту, не запуск tracker, модели или LinQ. Собственным компактным Python-расчётом дополнительно проверены `int(rate/30*buffer)`: (30,30)→30, (2,30)→2, (2,60)→4; strict-expiry ticks31/3/5; сброс candidate на U в последовательности P0,P0.5,U1,U1.5,P2,P2.5,P3 даёт confirm3. Это выполненная арифметическая проверка, остальные lifecycle traces — проектное рассуждение. Иллюстрации используют Δ=0.5s, N=4 (T_track=2s), H_on=H_off=1s, m=3, R=0, jitter0; это только параметры примера. P/N/U — measured positive / measured negative / unknown. TTL и episode retention — разные величины.

| Case | Крошечная последовательность | Ожидаемый результат и ошибка наивного решения |
|---|---|---|
| TTL/cadence | defaults rate30,buffer30 → N30. Update лишь2/s: 30 steps=15s; rate2,buffer30 → N2 →1s сетки. Для N4 при2Hz buffer60 | не «dt1 всегда ошибка». TTL растягивается только при несогласованной частоте/параметрах/пропусках update. Из-за strict `>` eligibility до ageN, pre-prune на N+1 |
| Burst gap | last measurement k0,t0; missing k1–4 доt2; reappearance k5,t2.5 | четыре empty steps продвигают prediction и age. В k5 до association age5>N4: старая identity не может пройти tracker TTL. По штатному порядку S01 совпадение в k5 способно re_activate до expiry; pre-prune предотвращает это. Внешний episode не clear |
| Prediction ≠ hold | P@0,P@0.5,U@1,U@1.5,P@2,P@2.5,P@3 | candidate chain обнулён в1; open впервые3, не1 и не2. Predicted bbox на1 не третий positive |
| Long episode | P@0,0.5,1 →E1; P до60 | одна OPEN карточка E1, updates60s. Cooldown10s не порождает E2@11/21… |
| Short occlusion | E1 OPEN; U@2,2.5; P@3 с тем же/однозначно linked uid | E1 UNKNOWN→OPEN, без второго open. U не clear и не новое positive duration |
| ID loss ambiguous | A,B близко; оба U@2; новые tracks7,8@2.5 допускают обе перестановки | два unresolved identity links, не один merged человек; соответствующие repeated opens заблокированы. Нельзя назвать это TP без annotation; возможный новый эпизод остаётся FN/late, если GT его подтверждает |
| Two subjects/pairs | A/P@0,0.5,1; B/P@0.5,1,1.5 рядом с той же machineM | E(A,M)@1 и E(B,M)@1.5: две карточки. Global cooldown подавил бы B. Если M predicted-only, оба pair-rule samples U |
| Clear/re-entry | E1; N@2,2.5,3 →clear@3; P@4,4.5,5 | E2@5, новый event ID. Перманентный blacklist track_id потерял бы E2; timer from first seen включил бы safe interval |
| Inadequate clear | E1; N@2, U@2.5, N@3,3.5,4 | clear лишь4: U разрывает negative-chain. ACK@2 не меняет этого |
| Out-of-order | tick4 timeout→GAP committed; result tick5 пришёл; затем result4 | commit5 после4; поздний4 audit-only. Нельзя откатить трек или пометить старый result текущим PTS |
| Duplicate request | requestQ/attempt1 timeout; attempt2; оба valid responses до cutoff | первый валидный выбранный completion закрывает tick, второй duplicate; один tracker update. Сервис мог реально выполнить NN дважды |
| Delivery/restart | E1 commit+outbox; UI приняла, ACK потерян; процесс restart; retryE1 | одна keyed карточка и одна journal row, два transport attempts. После рестарта новая визуальная identity требует описанного resolution, не просто тот же integer track_id |
| Fire | regionF P@0,0.5,1→E1; bbox растёт; две detections вокруг того же F; отдельно regionG | F update/children без new open; G собственный E2 после H_on; spatial merge F/G → lineage unknown, не удаление старых events |
| Censoring | clip начинается P@0; open@1; clip заканчивается P@1.5 | initial occupancy + right-censored, onset latency/clear unmeasured. Повтор кадра1.5 ещё10s не завершает реальную запись/hold |

#### Единое event matching и сырые counts

**W2-08-F07 [PROPOSED EVALUATION, совместимо W1-12 smoke6–7]:** unit — GT episode `camera/source_session × rule × actor` (либо ordered person–machine pair, либо spatial fire incident), а не класс clip/track ID. GT хранит onset interval, visible intervals, offset/clear interval, initial occupancy, left/right censoring, unknown intervals и entity identity/lineage. GT actor ID размечен человеком, не модельный tracker ID. Для связи prediction↔GT нужна сохранённая spatial/temporal identity evidence; ID число само по себе недостаточно.

До run заморозить eligible-policy, matching onset window, D своевременности, entity geometry threshold, T_link, min observation, H/G/R. Полноценный GT onset без достаточной видимости/длины для заявленного hold — отдельный censored/unobservable bucket с причиной, не произвольное исключение после результатов. Если запись полностью показывает эпизод, но алгоритм пропустил его из-за собственных drops, он остаётся eligible и становится FN. Initial occupancy оценивается отдельным presence stratum; не входит в onset latency, но его alert/miss учитываются.

Matching: построить допустимые пары только same camera/session/rule + соответствующая GT entity + совместимое временное окно. Однозначное maximum-cardinality one-to-one matching; tie-break минимальная onset distance, затем event_id. Temporal window/geometry — предварительно заданные условия, не universal threshold. Дополнительный confirmed OPEN на тот же уже matched GT episode — duplicate, даже при новом ID; он не второй TP. Unmatched подтверждение в известных negative условиях — FP, unresolved evidence — U с перечнем для review. Сырые FP и duplicate показывать отдельно и также combined false/extra-alert count, чтобы duplicates не исчезли из нагрузки. GT без matched event — FN. Для двусмысленной identity нельзя автоматически разнести два сообщения по двум GT людям ради красивого recall.

Показать по scenario/clip/entity: `GT_eligible,GT_initial,GT_censored,GT_unobservable,TP,FN,FP,duplicates,U,late_TP`, negative/unknown exposure seconds; unique OPEN rows, update rows, delivery attempts/retries, UI visible card count, request/tick/gap/late-result counts. Latency confirm/visible — только matched events с известным onset; при interval onset `[a,b]` latency interval `[t−b,t−a]`. FN остаются в denominator timely recall(D). При right-censored tail явно указать, что clear/rearm не проверены. Не применять tIoU к точечному уведомлению без определения interval. Не превращать curated 20s без FP в factory FP/hour и не объединять неодинаковые W1 gates в рейтинг качества.

#### Минимальный handoff: что менять и что проверять дальше

1. **Source/perception adapter:** сохранить исходные PTS/epoch/request mapping, фактические LinQ completion/proof и frozen coordinate/class contract. Без этого output не допускается в tracker. Доступ/компиляция/parity остаются у профильных веток, не симулируются здесь.
2. **Tick driver:** один ordered commit на каждый слот; gap/empty update, bounded deadline/catchup, reject late results; прямой S01 вместо готового callback S04. Вынести N в явный проверяемый параметр.
3. **Tracker adapter:** pre-association TTL/Removed purge; matched detection hook; class separation; единый geometry; identity namespace/reset; совместимость numpy. Не писать variable-dt filter ради первого smoke.
4. **Episode adapter:** описанные полярности/цепочки, entity variants, bounded unique relinking, ambiguity, initial occupancy/censoring; одна persistent OPEN запись, ledger+outbox transaction и keyed UI. Отдельно неизвестная recovery после restart.
5. **Первый будущий опыт:** один короткий positive + hard negative на реальном LinQ, затем тот же источник с фиксированной фазой, shifted phase, одним burst gap, retry/out-of-order и clear/re-entry. Сравнить raw tracks, source gaps, events и visible rows; добавить two-subject control. Пара/огонь допускаются только если реальные NN classes/признаки и GT обеспечены. Все device/event controls сейчас **NOT_RUN**.

#### Статус относительно W1 и оставшиеся Q/E

| K | Что нового относительно W1 | Результат / точный остаток |
|---|---|---|
| K009 | Вместо альтернативы «timestamp rules или time-aware tracker» выбран fixed grid с прямым S01; уточнены constructor, actual empty callback bypass, strict TTL pre-prune, F/Q distinction, jitter/late/epoch semantics | **scoped**: статический route определён. E: реальный runtime compatibility, matched hook/pre-prune tests, no-gap/phase/burst/out-of-order video с сохранёнными identities. Q: доступный device throughput/turnaround B, реальный PTS jitter/clock mapping и подходящий analysis cadence |
| K011 | Выбран один event interface на три entity variants, counts/matching/initial occupancy/censoring и bounded restart semantics; SQLite docs подтверждают только storage механизм, не готовое приложение | **scoped; executable/integration open**. E: ledger+UI consumer действительно идемпотентен, одна карточка/episode при retry, два subjects, clear/re-entry, crash windows, ambiguity recovery. Q: реальный UI/API idempotency/visible ACK, accepted H_on/H_off/G/R/D, политика разрешения identity после долгого gap/restart |

**Полезные candidates:** прямой pinned ByteTrack + cadence driver; S06 как documented per-step reference; SQLite keyed ledger как минимальный выбранный consumer путь. **Отклонены как готовое решение:** unchanged Ultralytics callback, Supervision first-seen timers, frame-rate-only исправление variable gaps, dt-only patch, global cooldown, permanent track blacklist, automatic cross-epoch identity, exactly-once обещание для произвольного HTTP/UI.

Наблюдено здесь: содержание точных primary code/docs и разрешённый DeepSORT revision. Выведено: order-dependent TTL counterexample и арифметика таблиц. Предложено: весь frame/episode/storage contract и контрольные timelines. Неизвестно: качество NN, актуальный hardware/service interface, физическая identity после неоднозначной окклюзии, фактическая UI видимость/transport guarantees. Никакие чужие measurement или собственные hardware PASS не заявлены.

<a id="F035"></a>
## F035 — Reference pipelines: exact code и R3-E6 export/parity/timing reference

**Нормализованный статус и условия:** R3-E6 ready ONNX существует по HEAD, publisher SHA не local full hash. Full-tree license negative уточнён F026. R3-E6 map0Fire1Smoke противоположен rabah/farhat. Остальные R1–R4 консолидированы по объектам F016/F019/F021/F024.

**Источники:** [S076](SOURCES.md#S076), [S081](SOURCES.md#S081), [S161](SOURCES.md#S161), [S162](SOURCES.md#S162), [S175](SOURCES.md#S175), [S260](SOURCES.md#S260), [S265](SOURCES.md#S265), [S271](SOURCES.md#S271), [S272](SOURCES.md#S272), [S367](SOURCES.md#S367), [S368](SOURCES.md#S368), [S375](SOURCES.md#S375), [S376](SOURCES.md#S376), [S377](SOURCES.md#S377), [S378](SOURCES.md#S378), [S379](SOURCES.md#S379), [S380](SOURCES.md#S380), [S381](SOURCES.md#S381), [S382](SOURCES.md#S382), [S383](SOURCES.md#S383), [S384](SOURCES.md#S384), [S385](SOURCES.md#S385), [S386](SOURCES.md#S386), [S387](SOURCES.md#S387), [S388](SOURCES.md#S388), [S389](SOURCES.md#S389), [S390](SOURCES.md#S390), [S391](SOURCES.md#S391), [S392](SOURCES.md#S392), [S393](SOURCES.md#S393), [S394](SOURCES.md#S394), [S395](SOURCES.md#S395), [S396](SOURCES.md#S396), [S397](SOURCES.md#S397), [S398](SOURCES.md#S398), [S399](SOURCES.md#S399), [S400](SOURCES.md#S400), [S401](SOURCES.md#S401).

**Происхождение:** [W1-16.md](_WORK/W1-16.md), `## Реестр новых`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Реестр новых первичных доказательств

Все URL ниже реально запрашивались 23.10.2026. Тип `CODE` — чтение, `META/HEAD` — metadata/доступность, `CLAIM` — заявление издателя; это не исполнение. Небольшие HTTP GET исходников не считаются запуском кода. Точные raw URL одновременно задают commit и локатор; функции/строки указаны там, где существенны.

| ID | Первичный источник и фиксированная версия | Установлено / граница |
|---|---|---|
| **W1-16-S01** | [time_in_zone/ultralytics_file_example.py](https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/examples/time_in_zone/ultralytics_file_example.py), `main`, строки 36–75; [requirements](https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/examples/time_in_zone/requirements.txt) | CODE GET200: model → detections → внешний ByteTrackTracker → zone mask → timer/overlay. Pending ID=-1 удаляются. Зависимости включают supervision, ultralytics, inference, rfdetr, trackers, jsonargparse и video-download tools, без версий. Пример broader, чем минимально нужный runtime. |
| **W1-16-S02** | [utils/timers.py](https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/examples/time_in_zone/utils/timers.py), `FPSBasedTimer.tick` 40–48 / `ClockBasedTimer.tick` 76–84; [general.py](https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/examples/time_in_zone/utils/general.py), `load_zones_config`; [LICENSE.md](https://raw.githubusercontent.com/roboflow/supervision/594bd0f9802872efcd50cc14564548a85e51dc19/LICENSE.md) | CODE GET200: JSON list of polygons → int32; таймеры со временем первого появления и без exit reset; supervision code MIT. Это не разрешение на выбранную модель/видео; отдельную лицензию нового пакета trackers здесь не проверяли. |
| **W1-16-S03** | [YOLOv8-ONNXRuntime/main.py v8.3.0](https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/examples/YOLOv8-ONNXRuntime/main.py), `preprocess` 78–107, `postprocess` 109–176, `main` 178–202 | CODE GET200: cv2 image BGR→RGB, direct resize, `/255`, BCHW FP32; transpose raw predictions, score filter и OpenCV NMS; session.run. Это single-image CPU/CUDA reference, а не готовый video/event app и не LinQ. |
| **W1-16-S04** | [predictor.py](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/predictor.py), `preprocess/pre_transform`; [exporter.py](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/engine/exporter.py), `export_onnx` | CODE: основной путь letterbox/RGB/BCHW/normalization и ONNX exporter. Exact tag→commit взят из W1-01 и повторно открыт pinned raw. Новые GitHub REST commit/release API здесь дали **403**: не объявлять собственное повторное разрешение tag по API. |
| **W1-16-S05** | [COCO names](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/cfg/datasets/coco8.yaml), строки 18,85; [pose predictor](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/models/yolo/pose/predict.py), 33–54 | CODE GET200: 0 person, 67 cell phone; pose postprocess NMS, bbox scale, reshape keypoints, scale_coords. Pose topology/head/17 joints отдельно подробно в W1-01. |
| **W1-16-S06** | [track.py](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/trackers/track.py), 34–49, 71–86; [bytetrack.yaml](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/ultralytics/cfg/trackers/bytetrack.yaml) | CODE GET200: persist/reinitialization, postprocess detections→tracker→results. YAML high=.5, low=.1, new=.6, buffer30, match=.8; constructor uses frame_rate30. Это published defaults, не подобранные пороги под камеру/пропуск кадров. |
| **W1-16-S07** | [distance_calculation.py](https://raw.githubusercontent.com/ultralytics/ultralytics/v8.3.0/ultralytics/solutions/distance_calculation.py), `mouse_event_for_distance`, `start_process`, строки 114–118 | CODE GET200: user picks two IDs, Euclidean **pixels** between centroids. Не готовая автоматическая схема all-person/all-forklift pairs. |
| **W1-16-S08** | [forklift card](https://huggingface.co/keremberke/yolov8n-forklift-detection/raw/d8b594f321dd4c64eda16e435601fd266089fc32/README.md); [config](https://huggingface.co/keremberke/yolov8n-forklift-detection/raw/d8b594f321dd4c64eda16e435601fd266089fc32/config.json); [metadata revision](https://huggingface.co/api/models/keremberke/yolov8n-forklift-detection/revision/d8b594f321dd4c64eda16e435601fd266089fc32) | GET200, public/gated=false; ultralytics8.0.21, ultralyticsplus0.0.23, input640. Card labels ordered forklift/person, numerical IDs надо подтвердить model.names. Checkpoint/права подробнее ниже. |
| **W1-16-S09** | [fall main.py](https://raw.githubusercontent.com/GajuuzZ/Human-Falling-Detect-Tracks/7ed2faa4d6147dfd576f58869b6c25545208af35/main.py), 106–160 | CODE GET200: detector→AlphaPose→tracker→30-observation action classifier. `TSSTG()` без CLI device; predicted tracks смешиваются с proposals. Это class-label overlay; подтверждение неподвижности/one-event lifecycle надо делать отдельно. |
| **W1-16-S10** | [Ultralytics LICENSE exact](https://raw.githubusercontent.com/ultralytics/ultralytics/6e43d1e1e5db72afbf686dee6745669bcb124b0a/LICENSE); [manufacturer licensing](https://www.ultralytics.com/license), trained models FAQ, current unversioned HTML | GET200 AGPL-3.0 у exact code; производитель заявляет default AGPL и для trained models, с отдельной Enterprise поставкой. Это не индивидуальное юридическое заключение о сдаче команды. |
| **W1-16-S11** | [rabahdev card](https://huggingface.co/rabahdev/fire-smoke-yolov8n/raw/13017fe8af477c25f5298d168e2dfede4b000753/README.md); [metadata with blobs](https://huggingface.co/api/models/rabahdev/fire-smoke-yolov8n/revision/13017fe8af477c25f5298d168e2dfede4b000753?blobs=true) | GET200: publisher says D-Fire fine-tune/AGPL; exact LFS metadata получена здесь. Training claims не наша проверка. |
| **W1-16-S12** | [cgr func.py](https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/func.py), `judge_smoke/detect_and_draw/cgr_detect`; [ort_inference.py](https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/ort_inference.py), lines10–17,103–171; [export.py](https://raw.githubusercontent.com/Leviathanlzx/cgr_detection/4a45c911cea365d7d196c2276611749ce5f3180b/export.py) | CODE GET200: разные backend/model paths, preprocessing/direct resize, pose 17×3 и tracker calls, threshold counter. Не проверенная inference-поставка. В W1-05 отдельно установлен недостаток tree/weights и различие code MIT / embedded model AGPL. |
| **W1-16-S13** | [R3-E6 release](https://github.com/Supakorn289/fire-smoke-detection-r3e6/releases/tag/v1.0.0-r3e6); [README exact](https://raw.githubusercontent.com/Supakorn289/fire-smoke-detection-r3e6/676f3280cf643f874ae6f12b41a4a412409d2830/README.md) | NEW: git ls-remote tag→`676f3280cf643f874ae6f12b41a4a412409d2830`; HEAD branch был949458ea… и **не выбран** для route. Release names/shapes/metrics — publisher statements. README says binaries excluded from Git, released separately. |
| **W1-16-S14** | [export_final_onnx_v1.py](https://raw.githubusercontent.com/Supakorn289/fire-smoke-detection-r3e6/676f3280cf643f874ae6f12b41a4a412409d2830/scripts/deployment/export_final_onnx_v1.py), 69–79,155–167,199–309 | CODE GET200: verifies PT hash, exports static batch1/768, opset17, FP32, no simplify/dynamic/embedded NMS; ONNX checker and metadata. Скрипт не запускался. |
| **W1-16-S15** | [verify_pt_onnx_equivalence_v2.py](https://raw.githubusercontent.com/Supakorn289/fire-smoke-detection-r3e6/676f3280cf643f874ae6f12b41a4a412409d2830/scripts/deployment/verify_pt_onnx_equivalence_v2.py), `compare_detections`, calls 772–857 | CODE GET200: hashes, PT/ONNX validation with fixed768 preprocessing, matched detections and fixed-threshold recall comparison. Это authored parity procedure, а не наша parity PASS. |
| **W1-16-S16** | [benchmark_onnx_cpu_v1.py](https://raw.githubusercontent.com/Supakorn289/fire-smoke-detection-r3e6/676f3280cf643f874ae6f12b41a4a412409d2830/scripts/deployment/benchmark_onnx_cpu_v1.py), `letterbox_768`, `postprocess`, `build_session` | CODE GET200: letterbox/rgb tensor FP32 [0,1], xywh→xyxy, class-aware NMS, ORT CPU provider, stage timings. Это measurement reference CPU, не real LinQ benchmark. |
| **W1-16-S17** | [SHA256SUMS](https://raw.githubusercontent.com/Supakorn289/fire-smoke-detection-r3e6/676f3280cf643f874ae6f12b41a4a412409d2830/model/SHA256SUMS.txt); [model README](https://raw.githubusercontent.com/Supakorn289/fire-smoke-detection-r3e6/676f3280cf643f874ae6f12b41a4a412409d2830/model/README.md); [environment](https://raw.githubusercontent.com/Supakorn289/fire-smoke-detection-r3e6/676f3280cf643f874ae6f12b41a4a412409d2830/metadata/environment/pip_freeze_before_onnx.txt) | GET200: publisher hashes; class0 Fire/class1 Smoke; freeze includes ultralytics8.4.95, torch2.11.0+cu128, numpy2.4.4, opencv5.0.0.93. Это запись автора, доступность всех packages/работоспособность среды нами не проверена. Root LICENSE и requirements.txt по exact URL дали404; отсутствие по одному пути не доказывает отсутствие любых разрешений. |

**Происхождение:** [W1-16.md](_WORK/W1-16.md), `## Exact artifact`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### Exact artifact manifest: availability отдельно от исполнения

Собственные HEAD следовали redirect, ответ200 и Content-Length. Не скачивались тела и не вычислялись локальные binary hashes. Publisher LFS/SHA256SUMS нельзя назвать локально проверенным checksum. Официальные GitHub asset URLs фиксируют release/name, но release assets могут заменяться: обязательный будущий локальный hash.

| Artifact / route | Точный URL и результат HEAD | Hash / права / gap |
|---|---|---|
| COCO YOLOv8n, R1/R4 | [yolov8n.pt v8.2.0](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt), **6,549,796 B** | Hash неизвестен; exact code v8.3.0/commit above; AGPL/Enterprise policy S10. COCO/image rights отдельно. |
| Pose, R2 | [yolov8n-pose.pt v8.2.0](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n-pose.pt), **6,832,633 B** | Hash неизвестен; лицензирование как выше. Не fall classifier. |
| Forklift, R3 | [best.pt revision d8b594…](https://huggingface.co/keremberke/yolov8n-forklift-detection/resolve/d8b594f321dd4c64eda16e435601fd266089fc32/best.pt), **6,216,376 B** | W1-03 publisher LFS `0dc3816283226f0f7ac5410620394c8ddeef32c5200b371194ac4df4a1ee7d38`; отдельная weight license не установлена. v8.0.21 code GPL-3.0 по W1-03; нельзя автоматически объявить эту историческую версию AGPL. |
| Fire nano, R5A | [best.pt revision13017…](https://huggingface.co/rabahdev/fire-smoke-yolov8n/resolve/13017fe8af477c25f5298d168e2dfede4b000753/best.pt), **6,229,802 B** | Своё API: LFS `b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f`; publisher AGPL. Проверить exact checkpoint package version, не навязывать v8.3.0 всем custom weights. |
| Fire s PT, R5B | [fire_smoke_r3_e6_final.pt](https://github.com/Supakorn289/fire-smoke-detection-r3e6/releases/download/v1.0.0-r3e6/fire_smoke_r3_e6_final.pt), **89,501,671 B** | Publisher SHA `49dc0464d99a6c250cf3c3e305d4149c3d4ce3ee354d9d7a5ae1cb8c53a22183`. Отдельные права не установлены. |
| Fire s ONNX, R5B | [fire_smoke_r3_e6_final_768_fp32.onnx](https://github.com/Supakorn289/fire-smoke-detection-r3e6/releases/download/v1.0.0-r3e6/fire_smoke_r3_e6_final_768_fp32.onnx), **44,794,673 B** | Publisher SHA `e887a759bcc65c89803c8ea0aa3d8891bcb0e60a5fd334433b2d6d912ba3bc79`. Готовый format не значит LinQ-supported. |

**Происхождение:** [W1-16.md](_WORK/W1-16.md), `## R5`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.

#### R5 — Fire/smoke NN → forbidden-zone rule → region episode; smoking rejected

**A, минимальный:** nano checkpoint rabahdev S11, exact revision/hash/HEAD above. Source inference/export через Ultralytics, но exact package checkpoint сначала инспектировать: модель card не является environment lock. Publisher mapping **0 smoke,1 fire** (передано W1-05; подтвердить model.names). RGB fixed640 FP32, dense output предположительно[1,6,8400], host NMS/undo-transform. Ограничение программы — видимый огонь вне явно заданной разрешённой зоны; smoke отдельно именовать smoke, не подменять fire.

**B, сильнее воспроизводимость deployment:** R3-E6 release S13–S17 уже предоставляет ONNX + hashes + exact export, equivalence и CPU-stage timing paths. Classes **0 Fire,1 Smoke**, наоборот A. Fixed **[1,3,768,768]** FP32; ожидаемый output при обычном two-class head[1,6,12096] — лишь архитектурный вывод, реальная metadata и operators не прочитаны. На LinQ требуется именно detector graph; reference ORT CPU code заменить device call, сохранить letterbox/class-aware NMS/coordinate contract. Опсет17 и большая768 сеть могут оказаться хуже nano для данного compiler. Сначала права и compiler inspection; 44.8MB ONNX доступен по HEAD, но ещё не compiled.

**Путь события:** region detections → temporal spatial association/IoU+zone (личный ID не нужен для пламени) → persistence + forbidden-zone intersection → open incident → updates без новых сообщений → sustained disappearance→close. Не считать каждое меняющееся smoke/fire bbox новым человеком/событием; smoke plume растёт/распадается. Fire и связанный smoke могут быть одним episode, а два удалённых очага — разными. Hysteresis и overlap rules — проектные, требуют controls.

**Smoke R5:** (1) resolve license/metadata/hash, actual names and ONNX I/O; A export либо B published ONNX; (2) CPU and LinQ parity на одинаковых tensors, не переносить готовую publisher CPU equivalence на device; (3) разрешённые изображения/записи flame, smoke-only, пар, пыль, блики/солнце, сварка, жёлтая одежда/экран с огнём; (4) одинаковый видимый fire inside allowed vs outside; (5) один sustained episode, короткая детекционная дыра, два очага, исчезновение и новый очаг. Для видео не создавать опасный огонь ради теста: разрешённый существующий материал либо контролируемая безопасная имитация с честной маркировкой. **Стоп:** неизвестные права/артефакт, false positives на сварке/steam, неподдержанный output6/opset17, контекст зоны не задан. Ни A, ни B **не обнаруживают курение**.

**Smoking rejected как готовый route:** cgr reference S12 полезен как пример pose/crop/evidence counter, но неполон по paths/weights/backend contract. W1-05 установил metadata `last.onnx` с untrained description; это не является доказательством плохого/хорошего качества, зато блокирует молчаливое принятие происхождения. Hand-to-mouth, fire bbox, smoke cloud не заменяют cigarette/use evidence. Нужна отдельная проверенная поставка до включения smoking в основные сценарии.

## Короткие канонические факты для точного цитирования

F010–F035 остаются подробным каталогом. F036–F068 выделяют отдельные claims; источники могут иметь одно происхождение. Ни401URL,ниповторныепроверкиодногорепозиторияне401независимоеподтверждение.

<a id="F036"></a>
## F036 — YOLOX nano: полученный официальный binary

**Тип:** LOCAL_OBSERVATION / full HTTP GET+SHA256. **Статус:** ACTUAL_BYTES; NOT_INFERRED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Официальный yolox_nano.onnx release0.1.1rc0:3,659,407B, собственный SHA256 `c789161ed43c8269fcd4e67c67eeeb4e80c622da2eb296a20bc6007bd18a0b7d`. Release published2021-08-18T12:41:41Z; asset42724905 created18Aug12:34:05Z,updated12:34:07Z,digestnull. Это полный local hash, не LFS claim. Release URL не immutablecodecommit; exacthash закрепляет эти bytes. Инференс/checker/compile не выполнялись.

**Источники:** [S034](SOURCES.md#S034). **Точный локатор:** W2-02.md / W2-02-S01; W2-02_evidence/downloads.json,static_metadata.json; detailed F014.

<a id="F037"></a>
## F037 — YOLOX nano: actual graph contract и raw decoder

**Тип:** LOCAL_STATIC_GRAPH + SOURCE_INSPECTION. **Статус:** GRAPH_OBSERVED; CHECKER/PARITY/DEVICE NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

IR6,pytorch1.7,opset11; FLOAT images[1,3,416,416]→output[1,3549,85],369nodes/236initializers. Conv113,Sigmoid110,Mul104,Concat18,Slice8,Add7,MaxPool3,Reshape3,Resize2,Transpose1; нетExp/NMS/externaldata/nestedgraphs. Head source decode_in_inference=False и graph concat/transpose безExp согласуются с rawxywhgeometry, ужеsigmoidobj/classes. Hostdecode stride8/16/32;xy=(raw+grid)*stride,wh=exp(raw)*stride,score=obj*class ровноодинраз. Это structural/source match, не восстановленный exactexportcommand.

**Источники:** [S034](SOURCES.md#S034), [S044](SOURCES.md#S044). **Точный локатор:** W2-02.md S01/S02; graph_nodes.json,nodeattrs; F014.

<a id="F038"></a>
## F038 — YOLOX: unresolved historical preprocessing provenance

**Тип:** SOURCE_CONTRADICTION + INFERENCE. **Статус:** OPEN; documented test hypothesis selected. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Tag0.1.1rc0→e1052df71842031413f6030723c3607b839c80ce,12Aug2021:RGB,/255,ImageNetmean/std. Actualasset created18Aug; releasebodyannounces19Augnormalizationremoval/incompatibleoldweights;currentpinnedREADME6ddff482…ссылаетсянатотжеassetсBGR0..255recipe. Binaryshapeнехранитцвет. Нет оснований назватьlegacy илиBGR empiricalartifact-matchedgolden. ВыбранcurrentdocumentedBGRtesthypothesis;historicalsanitygateдоPTQ. CPU↔LinQparityнаодинаковоошибочномтензоренедоказываетcorrectperception. K003,Q005,E002.

**Источники:** [S035](SOURCES.md#S035), [S040](SOURCES.md#S040). **Точный локатор:** W2-02.md W2-02-F01; yolox_release.json,smoke_contract.json; F014.

<a id="F039"></a>
## F039 — YOLOX-N416-BGR-v1: выбранная тестовая рецептура

**Тип:** SOURCE_DOCUMENTED_REFERENCE. **Статус:** PROPOSED REFERENCE; NOT empirical golden. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

6ddff482…caller:OpenCVBGRuint8; r=min(416/H,416/W);INTER_LINEARresize toint(Wr),int(Hr);pad114 top-left,right/bottomonly;CHWfloat32batch,безRGBswap,/255,normalize. DecodeF037;xyxy/rбезcenterpadsubtraction. CurrentNMSclass_agnostic=True,argmaxclass,score>.1,IoU<=.45,+1pixelarea;parser.3visualizationthreshold отдельно. COCOcontiguousperson0,phone67,неcategoryIDs1/77. Rawoutputсохранитьдоinplacedecoder;envelopeinput/tensorhash,r,size,modelSHA/contractversion. Exacthistoricalmatch остаётсяF038.

**Источники:** [S042](SOURCES.md#S042), [S043](SOURCES.md#S043). **Точный локатор:** W2-02.md W2-02-S02; smoke_contract.json; F014.

<a id="F040"></a>
## F040 — Official pose PT: exact bytes и исторический license conflict

**Тип:** LOCAL_STATIC_METADATA + OWNER_DOCUMENTS. **Статус:** BYTES/EMBEDDED_METADATA_OBSERVED; EXPORT NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

v8.3.0/yolov8n-pose.pt6,832,633B,SHA256 `c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212`;metadata8.0.77/date2023-04-17T08:01:11.737149,person0,kptshape17×3,embeddedAGPL3.0. Source8.0.77→5065ca36…LICENSEGPL3;v8.3.0sourceLICENSEAGPL3,ownerpolicydefaultAGPLfortrainedmodels. СтараяtrainingcodeversionневыдаётGPLgrantнаэтиexactPT. Output56×8400 толькоarchitectureexpectation;ONNXнеполучен. v8.2.0same-sizeнеbyteidentity.

**Источники:** [S046](SOURCES.md#S046), [S074](SOURCES.md#S074), [S076](SOURCES.md#S076). **Точный локатор:** W2-02 S03/F02 + W2-07 S05/F05; pose_pickle_disassembly.txt; F014/F015.

<a id="F041"></a>
## F041 — RTMPose-t: full ZIP/ONNX identity

**Тип:** LOCAL_OBSERVATION full GET/CRC/SHA. **Статус:** ACTUAL_BYTES; INFERENCE NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Tau-J/RTMPose revisioncd4d7095f5cfc9cfc4f46289bee91ea4a1e1d9fd,exactrtmpose-t_simcc-body7_pt-body7_420e-256x192-026a1439_20230504.zip12,547,710B,SHA `937003a70832d9cc34ea16927f504792f3133e92dda1b9c626236bbbe9e805cb`;end2end.onnx13,350,364B,SHA `a6c2f6a3896a4d51131d14d7a80a3d08b50f559af5a58a45d5b098aef510a70f`. ZIPJSONdeclaresMMDeploy1.2/MMPose1.1. HFmodelcardApache2uploaderdeclaration;codeMMPose/rtmlibApacheотдельно,trainingmedia неочищаются этим. Filename20230504 неpublicationdate,internalfolder20230831 неcapturedate.

**Источники:** [S049](SOURCES.md#S049). **Точный локатор:** W2-02 S04; W2-07 S04; downloads/static metadata; F014/F015.

<a id="F042"></a>
## F042 — RTMPose: actual two outputs и symbolic axes

**Тип:** LOCAL_STATIC_GRAPH. **Статус:** OBSERVED; STATIC_SPECIALIZATION/RUNTIME17AXIS NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

IR6,pytorch1.9,opset11;FLOAT input[batch,3,256,192];simcc_x[batch,MatMulsimcc_x_dim_1,384],simcc_y[batch,MatMulsimcc_x_dim_1,512].168nodes/93initializers,nested/externalнеобнаружены. Bothoutputsrequired. Configbody17/batch_size1непревращаетsymbolicaxesвobservedstatic17. Crop-wiseposeнуждаетсявpersondetector,zeropeople→zeroposecalls. MatMul/Shape/ReduceSum/Sqrtиrectangularinput —compilerгипотезы,неLinQsupport. Staticderivativeнуженотдельныйhash/parity,headereditнедостаточен.

**Источники:** [S049](SOURCES.md#S049). **Точный локатор:** W2-02 S04/F03; graph_nodes.json; F014.

<a id="F043"></a>
## F043 — RTMPose SDK-RGB affine reference и wrapper mismatch

**Тип:** SOURCE_INSPECTION + SELECTED_DESIGN. **Статус:** CALLER_CONFLICT_OBSERVED; NUMERICAL PARITY OPEN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

rtmlib03a1693…documentedOpenCVBGRcaller→PoseTracker/Body→RTMPosepreprocess→BaseTool безchannelswap,впротивоположностьSDKto_rgb:true. rtmlibSimCCscoremean(maxx,maxy),MMPose1.1min. ВыбранSDK/MMPose1.1commit537bd8e…reference:bboxcenter/scale×1.25,aspect192/256,nonUDPaffinewarp192×256,RGBexactlyonce,(RGB−[123.675,116.28,103.53])/[58.395,57.12,57.375],no/255;argmax/2,scoremin,invalid<=0,inverseaffine;noDARK/flip/softmax. Не переносить одинаковыйjointthreshold междуmean/min;wrapperнеобъявленэмпирическиисправленным.

**Источники:** [S019](SOURCES.md#S019), [S054](SOURCES.md#S054). **Точный локатор:** W2-02 S05/F04,SDKpipeline.json,MMPoseTopdownAffine/SimCCLabel.decode; F014.

<a id="F044"></a>
## F044 — Четыре coreMP4: доказанная primary CC BY4 byte identity

**Тип:** LOCAL_IDENTITY_OBSERVATION + PRIMARY_GRANT. **Статус:** CLOSED exact4 COPYRIGHT_IDENTITY; OTHER_RIGHTS SCOPED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

GMDCSAS1/F11(5,961,144B,c25e4fc9…bfea7)иS3/ADL08(5,172,948B,b383bb83…fa8b)равныполнымраспакованнымmembersZenodo13354453v2.1ZIP:CRCcorrect/raw==local/fullSHA. ZIPwholehashнепроверен. SafeUnsafe0_te23(6,391,494B,e2c053d8…7a7f),4_te1(13,209,619B,11049609…126a):fullSHA/localsizeравныprimaryMendeleyV1manifestfileidsa5f9d29f…/07d51de0…. PrimaryMP4повторнонеGET;hashidentityдостаточна,новоговизуальногопросмотранет. Полные64-digitSHA/URLs/credits вF015. Zenodo21.08.2024 иMendeley11.06.2024 прямоCCBY4. Нельзяписатьдляэтих4mirrorunverified/«нетлицензии».

**Источники:** [S059](SOURCES.md#S059), [S063](SOURCES.md#S063). **Точный локатор:** W2-07 S01/F01,S02/F02; gmd_identity.json,mendeley_identity.json,range_log.json; F015.

<a id="F045"></a>
## F045 — Copyright grant и residual per-use права разделены

**Тип:** PRIMARY_LICENSE + SUPPLY_ANALYSIS. **Статус:** POSITIVE GRANTS ESTABLISHED; SCOPED RESIDUALS OPEN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

CCBY4разрешаетcopy/adapt/share/displayсattribution/license/notices/changes;privacy/publicity/personalityневыдаёт. АвторыGMDCSAзаявилиsignedconsent/publicrepository,SafeUnsafepermissionscompany/employees;полныеreleasesнепрочитаны. Residualpublicrecordingscopeнельзяпереписыватькакавтоматическийзапретinternalresearch/livecopyrightuse. YOLOXApachecodeобоихpinsдоказан,officialreleaseprovenanceположительна,explicitstandaloneweightstatementненайден;RTMPoseuploaderApachecardотдельнаотtrainingmedia;SDKcompiledredistributiontermsнеполучены. НепокупатьEnterpriseавтоматически;лицензияфактическойпоставкирешаетсяпосоставу.

**Источники:** [S077](SOURCES.md#S077), [S068](SOURCES.md#S068), [S070](SOURCES.md#S070). **Точный локатор:** W2-07 per-use/credits; CClegalcode§2–3; F015.

<a id="F046"></a>
## F046 — GMDCSA S3/F07: observed short fall→gross-low-motion tail

**Тип:** LOCAL_FULL_DECODE + MANUAL_ALLFRAME_REVIEW. **Статус:** OBSERVED DEV_REFERENCE; NN/EVENT NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

ExactSubject3/Fall/07.mp49,262,980B,SHA `86a20851a1d3bfacbe11d8977972f95a256893b80cd4de66dc7bb224a4dca55b`;269frames1280×720,allPTSvalid/increasing;frames0–28upright,29–59descent,60–75settling,76–268grosslowmotion. Консервативныйcontinuousvisibleinterval[2.560033,8.992067]s = **6.432033s**. Тело у края,ноголова/torsoвидны;thumbnailallframe неbreathing/fingermeasurement/absoluteimmobility/consciousness. EOFright-censored,нетrecovery/clear. Неloop/freezeдлядлинногоH.

**Источники:** [S111](SOURCES.md#S111), [S059](SOURCES.md#S059). **Точный локатор:** W2-03 F01; own_phase_visibility.csv,event_intervals.json,decode_manifest.json; F017.

<a id="F047"></a>
## F047 — Fall hold eligibility и controls: пределынаблюдения

**Тип:** LOCAL_PTS/ANNOTATION + INFERENCE. **Статус:** OBSERVED/CENSORED; H NOT CHOSEN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

S1F11stablegrossinterval[3.889367,6.097400]=2.208033sпоследвиженияног. F07допускает0<H<=6.432033sпоэтойgrosspolicy;обаpositiveодновременноstructurallyeligibleлишьH<=2.208033s. H10/H30:0eligiblepositive,неFNеслиsourceнепоказалнужныйhold. S1F13с1.3774swholebodycropunknown;S1ADL16bend/reach,S4ADL05exercise,S3ADL08supportedintentionallyinghardnegativesдляfall,неallrulesafe. Все6reviewed/dev,1048frames;невидимостьнеzero-motion. Новыйholdout/longtail/rearm/twoperson/reacquisitionещёнужны.

**Источники:** [S111](SOURCES.md#S111). **Точный локатор:** W2-03 phase/hold/splits tables; F017.

<a id="F048"></a>
## F048 — Weizmann matched walk/run: реальные bytes и предел gait-доказательства

**Тип:** LOCAL_BYTES/DECODE/SELECTED_FRAME_REVIEW. **Статус:** SAMPLE_OBSERVED; SPEED/DEVICE/PUBLIC_GRANT UNKNOWN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

daria_walk.avi6,536,192B,SHA009fce023da7e907f6de97bc561e9cd7fb74117fa8f7aa11c8c00a30ec6d18dd;daria_run.avi3,269,120B,SHAe9958bccbdca9e34eb96a59e236e7e1bb6b7e06f4eac187326913a4a4bb44822. CRCboundedZIPmembers;rawvideo180×144,25fps,timebase1/25;84/42frames. Page50fpsvsencoded25/subsampledнеустанавливаетcaptureclock. Reviewwalk[.20,3.04),run[.20,1.44);actionalreadyactive,onsetleftcensored. Similaractor/backgroundgaitcontrast,неcalibratedspeed,неsame-tracktransition;fastwalk/burst/cameramotionнет;publiclicensestatementнеустановлен.

**Источники:** [S155](SOURCES.md#S155), [S156](SOURCES.md#S156), [S157](SOURCES.md#S157). **Точный локатор:** W2-05 F04–F06; range_manifest,decoded_pts,review_intervals; F020.

<a id="F049"></a>
## F049 — CHAD route не дал exact running episode

**Тип:** PRIMARY_SOURCE_SCHEMA + LIMITED_NEGATIVE_SEARCH. **Статус:** SOURCE_READ; VIDEO_NOT_ACQUIRED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

CHADcommitf8a28c13cb5ee27d3283bf6cddb634a0401d76b0:4cameras,<camera>_<video>_<abnormal_present>.mp4,personbbox/posepickle,framebinarynpy. Runningвontology,но1неactiontype/actorid. HugeDriveZIPнеполучен,HTML200ненастоящийZIP;sign-inviewerнедоказываетобязательныйloginfordownload. RepoApacheнеотдельныйvideogrant. Exactrunningfilename/actorinterval/PTSнеустановлены;неabsencemodel/datasetвпринципе.

**Источники:** [S151](SOURCES.md#S151). **Точный локатор:** W2-05 S01/F03; F020.

<a id="F050"></a>
## F050 — Forklift exact checkpoint/names и положительный MIT publisher signal

**Тип:** LOCAL_FULL_SHA/STATIC_NAMES + PRIMARY_PUBLISHER. **Статус:** BYTES/NAMES CLOSED; WEIGHTS_SCOPE SCOPED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

keremberkeHFrevisiond8b594f321dd4c64eda16e435601fd266089fc32/best.pt6,216,376B,SHA `0dc3816283226f0f7ac5410620394c8ddeef32c5200b371194ac4df4a1ee7d38`;safezip/pickletoolsnames0forklift1personobserved. Config640/ultralytics8.0.21+ultralyticsplus0.0.23;expectedONNX[1,6,8400]source-derived,неexported. Code8.0.21GPL3. Publisherawesome-yolov8-modelscommitfb4b7895…перечисляетexactmodel,projectMIT —favorableevidence;HFcard/treeбезявногогрантавесов. НеобнулятьMITsignalинепереноситьCCBYimageDatasetнаweights/compiled.

**Источники:** [S161](SOURCES.md#S161), [S198](SOURCES.md#S198). **Точный локатор:** W2-04 S03/S04,F04;checkpointdisassemblylines32422–32433; F022.

<a id="F051"></a>
## F051 — Moving forklift media: real controls и synthetic pair, без complete realpositive

**Тип:** LOCAL_DECODE/CONTACT_REVIEW. **Статус:** SYNTHETIC_SMOKE_GO; REAL_COMPLETE_ROUTE_NOT_READY. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Real3_te1/7_te1actual250/177frames:движениеforklift/driverвидны,отдельныйуверенныйwalkingpedestrianнет;станочныйработниксoccludedfeetunknown. NVIDIA00238actual1280×720144frames24fps—дваотдельныхчеловека+приближающийсязаднийforklift;00298moving+farforegroundpairpartialnegative,далёкийдругойpairнеall-safe. Stationarynearcontrolнеполучен. ZIP64из7.95GBархиватолько2membersCRC/fullSHA,wholearchiveSHAнет;generatedVeo/Cosmos,NVIDIADatasetLicense+Googleterms,неCCBY. Imageproxyнеметры/physicalTTC;realmotionдоказаноконтактнымreview,неframe-levelnear-missGT.

**Источники:** [S194](SOURCES.md#S194), [S064](SOURCES.md#S064). **Точный локатор:** W2-04 F01–03;video_manifest/synthetic_decode/nvidia_actual_selected_labels; F022.

<a id="F052"></a>
## F052 — Fire exact PT candidates: оба smoke0/fire1, readiness preference rabah

**Тип:** LOCAL_FULL_SHA/STATIC_METADATA + UPLOADER_CARDS. **Статус:** BYTES/NAMES/AGPL OBSERVED; QUALITY/EXPORT/DEVICE NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Rabahrevision13017fe8af477c25f5298d168e2dfede4b000753,6,229,802B,SHA `b91633799ceb052c814b4f8b77a37efc9a40f002d528df97d74463585fa4f28f`,embedded8.4.51;Farhate4f808eb87d72b53ccc860c007f564baf174540a,6,229,546B,SHA `0dbc9ded65f5c01455e37669338be0e3df688ade0873258017d62b550d0e964f`,8.4.150. Обоимactualnames0smoke1fire,card+embeddedAGPL. RabahсодержательнееD-Firetrainingcard;послеnamesпроверкипредпочтёнпоредукциинеизвестностиprovenance,непобедеaccuracy/speed. ReadyONNXне найден;640[1,6,8400]покаexpectation.

**Источники:** [S260](SOURCES.md#S260), [S262](SOURCES.md#S262). **Точный локатор:** W2-06 F03;checkpoint_static,metadata_locators,fullPTdisassembly; F026.

<a id="F053"></a>
## F053 — Fire media actual decode и FURG XML semantic defects

**Тип:** LOCAL_ALL_FRAME_REVIEW/PTS/XML. **Статус:** OBSERVED DATA; NOT PERFECT GT/NOT MODEL EVAL. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

FURGCar1630frames,nonfire341,barbecue902,2997/100FPS(timebase1/29970),неXML29. XMLxywhframe0Car1[260,97,288,293]→xyxy[260,97,548,390]. Укаждогоextraendrow+1;Car1cuts246/443retainsstalepriorboxes;BBQempty596–602/639–641свидимымпламенем,неrealcessation. Nonfirescene0–239,fade240–244,IEEEoutro245–340неindustrialnegativeexposure. FIRESENSEposVideo11.870178frames15fps/forestflame;negsVideo2.859155frames10fps/nightheadlightconfuser,CRC/SHAactualmembers. Smoke-onlycontrolнет;пламясначала/доEOF,onset/clearнепроверены.

**Источники:** [S256](SOURCES.md#S256), [S257](SOURCES.md#S257). **Точный локатор:** W2-06 F01/F02;decode_manifest,XMLparse/allframesheets; F026.

<a id="F054"></a>
## F054 — Fire policy и media/model licenses без smoking подмены

**Тип:** PRIMARY_GRANTS + PROPOSED_RULE. **Статус:** POLICY NOT_IMPLEMENTED; COPYRIGHT GRANTS OBSERVED/SCOPED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

VisibleflameoutsideactiveallowedROI→persistentregionepisode;smokeотдельно,неsmoking. SameBBQpixels+allowedactivepermitvsinactivepermit —предлагаемыйpolicyreplay,неfactorytruth/modelbenchmark. FURGrootCC0реальноесть,ноnegative©IEEE2012thirdpartyscope;FIRESENSEprimaryCCBY4/exactmembers,positiveUltimateChasewatermarkresidualsourceclearance. AGPLexactPT/codeнеочищаетtrainingimages;R3E6fulltree676f3280…nolicense/copying/noticepaths,grantunknownreferenceonly,map0Fire1Smoke. Ниавтозапретresearch,ниautomaticunrestrictedpublicbundleневыводятся.

**Источники:** [S256](SOURCES.md#S256), [S257](SOURCES.md#S257), [S265](SOURCES.md#S265). **Точный локатор:** W2-06 F04/F05; W1-16 R5/S13–17; F026/F035.

<a id="F055"></a>
## F055 — SafetyVision v2: actual ONNX и card class map — разные уровни

**Тип:** RANGE_STATIC_GRAPH + UPLOADER_CARD. **Статус:** GRAPH_OBSERVED_PARTIAL; FULLSHA/CHECKER/DEVICE NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

revision56a71758b55f0e9f2b4b2d6b51a779a1f882da10/v2/best_640.onnx44,764,727B;publisherLFSea18ae903a566e8fa76f3ee1c503075522dca269269315e9c862efa170430b35неlocalfullhash. Range1,150,519B:IR9/opset20/imagesFLOAT[1,3,640,640]→output0FLOAT[1,17,8400],231nodes/14optypes. Card13classes:No_Harness10,Person11,Fall-Detected0;orderednamesневыведеныиз17channels. AGPLweightspercard/codeLICENSE. Visibleabsenceнеconnectedhook/height;NMSвложенныхPerson/NO-Xиownerassociationнуждаютсявparity. Неv1root/896variant.

**Источники:** [S025](SOURCES.md#S025). **Точный локатор:** W1-14 S09/F05 + W1-07 S02/S03; F012/F031.

<a id="F056"></a>
## F056 — Thalos scaffold/harness: exact checkpoint опровергает card

**Тип:** LOCAL_RANGE_STATIC_PICKLE_METADATA. **Статус:** REJECT this exact revision FOR HARNESS. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

c07ae29e6095fa0e284a077fdafdb8a857a8eb77/scaffold_harness_weights.pt87,685,242B;read219,182HTTPbytes/datapkl183,404B,неfullfile. Actualnames{0:literalstring2,1:Safety-barrier,2:Safety-bollard,3:Safety-cone,4:cracks,5:open-hole,6:open_manhole,7:pothole};offset143042/memo358resolvesclass0string2. Cardpromisesharness/scaffoldиwrongscaffold_harness_safety_weights.ptfilename. Correctfilenameнеисправляетwrongclasses;неутверждатьчтоуownerнигденетдругихcorrectweights.

**Источники:** [S285](SOURCES.md#S285). **Точный локатор:** W1-08 S07/F01; W1-07 attributedF13; F028/F031.

<a id="F057"></a>
## F057 — Cigarette ONNX: untrained metadata не training history

**Тип:** FULL_GET/STATIC_GRAPH + SOURCE_EXPORTER. **Статус:** ACTUAL_BYTES/METADATA; TRAINING UNKNOWN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

cgrlast.onnx12,238,102B,SHA3b2b5754ac65f157c10dc180fbfe671bc3df7d3c6cc2b24462835a04243af0aeполныйGETвпамять,неretainedlocalmodel. IR8/opset17/images[1,3,640,640]→output0[1,5,8400],cigarette0,embeddedAGPL/8.0.145. Exporterdescription(untrained)генерируетсяеслиargs.dataотсутствует;не randomweightsproof. RepoMITcodeотдельно. Actualloaderexpectsabsentrtdetrpath/другойlayout;неturnkeysmoking. MeetCoolalternativeopset19/7channels0cigarette1person2smoke—perception,неaction.

**Источники:** [S255](SOURCES.md#S255), [S270](SOURCES.md#S270). **Точный локатор:** W1-05 S02–05/F02–05; W1-08 S05,W1-14 S08; F027/F028/F012.

<a id="F058"></a>
## F058 — PoseC3D/TSSTG: точные резервы не готовые события

**Тип:** PRIMARY_CODE/HEAD + LIMITED_ACCESS_OBSERVATION. **Статус:** REFERENCE_ONLY; EXPORT/DEVICE/EVENT OPEN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

TSSTGupstreamDrive404впроверке;7classesStanding/Walking/Sitting/LyingDown/Standup/Sitdown/FallDown,30observations,13COCOsubset+shouldermid=14;points[1,3,30,14],motion[1,2,29,14]→7sigmoid. Rootgrantнеустановлен. PoseC3DNTUcheckpointHEAD2008,246,969B,falling42(A43),нетrun/stationaryunconscious;HMDBHEAD20012,276,729B,run32/walk49/fall_floor12/climb5/smoke40,heatmaps[1,17,48,56,56]expectation,неrawposeRGB. Published10clipaccuracyнеcausalindustrialeventquality;Conv3D/export/currentLinQнепроверены.

**Источники:** [S088](SOURCES.md#S088), [S143](SOURCES.md#S143). **Точный локатор:** W1-01 S05–13;W1-08 S08; F016/F028.

<a id="F059"></a>
## F059 — Телефон: object/use/policy и action donors

**Тип:** SOURCE_SEMANTICS + ENGINEERING_INFERENCE. **Статус:** CONDITIONAL RESERVE; TARGET EVENT NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

COCOcontiguousperson0/phone67неuse. Needsamepersonownership,use-likehand/ear/HOIevidenceивременноеwalking/workcontext. Carryathip/radio/scannerобязательныеcontrols;workROIненастоящийworkingmachine. UPT HICOtalk_on101/text_on103/read73/hold36/object67;Drivepayloadnotverified. AVA15answerphone/57text-look,person-actionboxesnotphoneboxes;joinwalk14неисполнен. AVASlowFast81channelsinclbackground0/32framesinterval2/externalproposals,noLinQ. NTUA028call/A029phone-tabletgated. Телефонмалпослеresize→nativecropнепослеутратыдеталей.

**Источники:** [S215](SOURCES.md#S215), [S237](SOURCES.md#S237). **Точный локатор:** W1-04 semantics/S06–08;W1-11 S01–03; F024/F025.

<a id="F060"></a>
## F060 — Fence source numeric remap и неподтверждённый trained best

**Тип:** PRIMARY_ANNOTATION/CODE_INSPECTION. **Статус:** CLASS_CONFLICT OBSERVED; TRAINEDARTIFACT UNKNOWN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Fence_Security011e048790b0cab1751d7532cac7c02656698990:all14obj.namesread. sample9map0fence1climbing2walking;sample1–8,10–14map0fence1walking2climbing. Finaltrainharmonizationнепроверена. alert.pyexpectsnestedintruder_detector12/weights/best.pt,неподтверждён;rootyolov5m.ptinitialweightsnottrainedclimb. Videos/sample1.mp4(1,045,694B),sample10(3,769,890B)метаданные,notdecoded/reviewed. sourceYouTube/UCF/rightsunknown;adjacentframesнезависимы. Climbingнеcompletedforbiddenfencecrossing/underconveyor.

**Источники:** [S318](SOURCES.md#S318), [S317](SOURCES.md#S317). **Точный локатор:** W1-11 S14/F19–21; F030.

<a id="F061"></a>
## F061 — Высота/груз: отсутствующие observable inputs

**Тип:** PRIMARY_DATA/DOMAIN_DOCUMENTS + INFERENCE. **Статус:** FULLPROMISE EXCLUDED; LOCALRULE PILOT CONDITIONAL. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

HuangactualVOCliteralsafety-harness/person/clothes,неhook/lanyard/anchorconnection;нетnumericIDs/weights/license вreadtree. Harnesspresenceнеcorrectconnection/anchorstrength;notdetectedнеvisibleabsence;topimageyнеheight. Correctelevatedsurface+localprotectionrule+visibilityнужны. Carryingbbox/2Dposeнеmass/grip/effort/shiftfrequency;RNLE23kgидеализированнаяliftingconstant,неуниверсальныйcarrylimit. Нормативныеисточникиисcopeнепревращатьвсамостоятельнуюнормунаbbox;sourceofficialamendmentsнеполностьюпрочитаны.

**Источники:** [S337](SOURCES.md#S337), [S356](SOURCES.md#S356). **Точный локатор:** W1-07 F03–08/F11,S01/S07/S09/S10; F031.

<a id="F062"></a>
## F062 — Vendor pose benchmark: цифры и строгая граница

**Тип:** VENDOR_REPORTED_MEASUREMENT via TEXT_EXTRACTION. **Статус:** TEXT_RECONFIRMED; BYTES/HASH/VISUAL/MATCHEDMODEL UNKNOWN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Officialpress→2026presentation13pages;P3physicalpage4row14yolov8n_pose,b1:HP104.8FPS/21.51ms,HPQ419.2/21.51. yolo5s106.1/23.71,424.4/23.71. Footeri7-10700K3.80GHz/Ubuntu24.04/Runtime16.18.6/Framework2026.8.43/MLCommonsMLPerfname. OriginalPDFbytes/hash/imagesнеполучены;2parserstextнеvisualverification. Exactcheckpoint/inputsize/precision/timingboundaries/scenario/percentiles/accuracyнеустановлены. ResNetpage3vs4числарасходятся;4xthroughputsamelatencyне4xrequestspeed;1/FPSнеlatency. ЭтонеourLinQmeasurementи неeventSLA.

**Источники:** [S005](SOURCES.md#S005), [S004](SOURCES.md#S004). **Точный локатор:** W2-01 F02–04/S03–04 + W1-15 F01–03; F010/F013.

<a id="F063"></a>
## F063 — LinQ access: public promise не team grant/completion

**Тип:** CASE/PRIMARY_DOCUMENTS + LIMITED_LOCAL/PUBLIC_SEARCH. **Статус:** ACCESS/SDK/DEVICE UNKNOWN; HARDWARE NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

Кейс8обещаетVMисервис;вissuedworkspaceнетcredentials/runbook/SDK/catalog. Docsindexв2026всёещёlinksGuide2025IVA H1,неmatchedrelease2026. Ownupload/update/compile/outputs/quota/hostboundaryнеустановлены;publicfamilyYOLO8/11неexactcheckpoint. Deviceproofbundle:grant→backend/device→model/programhash→inputhash→request/job→completedoutput→event→timings;import/TLM/HTTPaccepted/devicevisibleнеproof. ManagedserviceбезSSHможетподойтиеслиacceptedbackendtrace+outputs;обратноеVMshellбезdeviceнеподходит.

**Источники:** [S002](SOURCES.md#S002), [S003](SOURCES.md#S003), [S008](SOURCES.md#S008). **Точный локатор:** W2-01 F01/F03 + W1-13 access tree/criteria; F010/F011.

<a id="F064"></a>
## F064 — Fixed-cadence ByteTrack route и observed/predicted separation

**Тип:** SOURCE_INSPECTION + SELECTED_DESIGN. **Статус:** SOURCE_OBSERVED; ADAPTER NOT_IMPLEMENTED/NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

ChosenFoundationVisionByteTrackd1bf019…fixedanalysisgrid(initial5Hzcandidate),oneorderedcommitpertick,empty(0,5)updateongap/timeoutand successfulnodetectionwithdifferentstatussidecar. Detectionsoriginalxyxy+scorecopy,img_info=img_size=(H,W)scale1,perclassinstances;hookmatcheddet_idthroughallstages;predictedgeometryнеvisualevidence. Actualdt1stateF/Q;frame_rateonlybuffer. Variable-dtF/Q/velocity/noiseadapterневыбран. Ultralyticsv8.3.0callbackemptycontinueнеadvancetracker;DeepSORTтожеdt1/frameage+extraembeddingNN,неtimestampawaremagicreplacement.

**Источники:** [S030](SOURCES.md#S030), [S367](SOURCES.md#S367). **Точный локатор:** W2-08 F01–03 / framecontract; F034.

<a id="F065"></a>
## F065 — ByteTrack строгийTTL требует pre-association pruning

**Тип:** SOURCE_ORDER_INSPECTION + SMALL_ARITHMETIC. **Статус:** STATIC_COUNTEREXAMPLE; ACTUAL_RUNTIME_TEST NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

buffer=int(frame_rate/30*track_buffer),expiryframe_id-end_frame>Nпослеassociation;lostвозрастаN+1можетreactivateиобновитьend_frameдоexpiry. ДлявыбранногoстрогогоTTLadapterprepurgesExpired/Removedизtracked/lostдоassociation;lastmeasurementticksidecarнеpredictedtime. N=floor(Ttrack/Δ),constructorverifyeffectiveN. Δ=.5,N4:lastmeasurek0,gap1–4,reappear5→oldidentityexcludedpreassociation;episodeостаётсяunknown,неclear. Выполненылишьconstructorarithmetic(30,30)→30,(2,30)→2,(2,60)→4;неframeworkbugbenchmark.

**Источники:** [S030](SOURCES.md#S030), [S031](SOURCES.md#S031). **Точный локатор:** W2-08 F01/F02/F06;trackerupdateorder; F034.

<a id="F066"></a>
## F066 — Единый frame/request/episode contract

**Тип:** PROPOSED_ENGINEERING_CONTRACT. **Статус:** DESIGN ONLY; EVENT PASS NOT_RUN. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

camera/stream_epoch/frame_seq/sourcePTS(timebase)/modelhash/inputhash/requestid/tickseq;retry same requestid newattempt. Orderedcommitswithboundeddeadline,rejectlate/duplicate/wrongepochwithouttrackerupdate. Personuid/orderedperson-machinepair/regionuidтриvariants. MeasuredP/N/U;H_on/H_offнепрерывнаяvalidchain,minobservations,PTSspan/gapbound;Uсбрасываетcandidate/clearchain,OPENсохраняетuncertain;PпослеUтотжеepisode,неnewalert. Clearтолькоobservednegative+hysteresis,ACKнеclear;rearmотдельно;initialoccupancy/onsetleftcensoredиEOFrightcensored. Ambiguousrelinkнеугадываетдвухлюдей;FN/deduptradeoffраскрывается.

**Источники:** [S030](SOURCES.md#S030). **Точный локатор:** W2-08 proposed frame/episode sections/F04; F034.

<a id="F067"></a>
## F067 — Once UI/journal: persistent keyedledger, ограниченная гарантия

**Тип:** SQLITE_DOCUMENTS + PROPOSED_DESIGN. **Статус:** NOT_IMPLEMENTED/NOT_TESTED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

event_id=episode_id,revisionдляupdates,UNIQUE(event_id,notification_kind=open);однаtransactionwatermark+episode+outbox. UIчитаетkeyedcard/journalrow;retryoutboxтотжеID,transportattemptauditнеnewviolation. Crashbeforecommitнетcard,aftercommitretryтотжеevent. ЭтоidempotentmaterializedviewвсохранённойБД/consumer,неuniversalexactlyonceHTTPdelivery. RestartнестанавливаетKalmanidentityизledger:newepoch/generation,unknown/unresolvedдоboundedresolutionилиobservedclear. Дляseamlessrestartнуженsnapshot/replayещёнепроверенный.

**Источники:** [S373](SOURCES.md#S373), [S374](SOURCES.md#S374). **Точный локатор:** W2-08 F05/restart/timelines; SQLiteUPSERT/atomic docs; F034.

<a id="F068"></a>
## F068 — Event evaluation: eligible/censored/one-to-one/raw counts

**Тип:** PROPOSED_EVALUATION backed by reviewed data. **Статус:** PROTOCOL ONLY; NO QUALITY METRICS MEASURED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

GTunitcamera/source_session×rule×actor/orderedpair/spatialfireincident;humanentityIDнетrackerID. Freezeeligibility,H/G/R/D/matching/geometryдоrun. Maximumcardinalityone-to-onematchingсfrozenwindows/tiebreak;secondopenonmatchedGTduplicateнеTP;knownnegativeunmatchedFP,unresolvedU,eligibleGTunmatchedFN. Algorithmowndropsнеисключаютsourcefullyeligibleepisode. Sourcecensoringотдельно. CountsGTeligible/initial/censored/unobservable,TP/FN/FP/duplicates/U/lateTP,negative/unknownseconds,uniqueOPEN/update/delivery/retry/UIcounts. Intervalonset[a,b]→latency[t−b,t−a];FNвtimelyrecallDdenominator. CuratedsecondsнеfactoryFP/hour.

**Источники:** [S373](SOURCES.md#S373), [S111](SOURCES.md#S111). **Точный локатор:** W2-08 F07; W1-12 smoke6–7; F033/F034.

<a id="F069"></a>
## F069 — Performance/coverage: clocks и sampling арифметика

**Тип:** PRIMARY_DOCS + OWN_SYNTHETIC_ARITHMETIC + DESIGN. **Статус:** SYNTHETIC CHECK EXECUTED; REAL E2E NOT_MEASURED. **Дата доступа исходных проверок:**2026-10-23; публикации/revisions отдельно в записи.

SourcePTSдляbehavior,timecapturemappingдляcameraage;hostmonotonicдляqueue/RPC/visiblelatency. Device latency/RPCaccepted/completedthroughput/frameage/confirm/visibleразныеboundaries;нескладыватьp95стадий. RTPнеUTCбезvalidatedRTCPmapping. IdealsamplingΔ/duniformphasecoverage=min(1,d/Δ),неmodelrecall. 10000phasearithmetictest:d.2sна1/2/5Hz=.20/.40/1.00,threeobservationsspan2/1/.4s. Burstgaps/jitter/occlusionмогутсломатьsamplecoverage;averageFPSнегарантируетmaxgap. Frozenphasesweep/pacedreplay/failurecountsнужныпозже.

**Источники:** [S029](SOURCES.md#S029), [S027](SOURCES.md#S027). **Точный локатор:** W1-15 F05–11; W2-08 cadence; F013/F034.
