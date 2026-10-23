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

