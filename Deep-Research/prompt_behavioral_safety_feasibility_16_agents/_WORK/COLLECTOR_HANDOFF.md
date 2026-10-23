# COLLECTOR_HANDOFF — READY_FOR_AUTHOR

Статус: **готово для отдельного автора**. Срез23.10.2026, Europe/Moscow(UTC+3). Сборщик прочитал16полныхW1,8W2,исходнуюкритику,обаinputprompt иCASE_ROOT_NOTES/CASE_PROVENANCE/RUN_STATE; выполнял только локальную аналитическую сборку. Новых сетевых доказательств, приложений, NN inference, export/compile/device benchmark, третьей волны или субагентов нет.

Готовы четыре доказательных файла в корне: [RAW_FACTS](../RAW_FACTS.md), [SOURCES](../SOURCES.md), [OPEN_QUESTIONS](../OPEN_QUESTIONS.md), [CRITIC](../CRITIC.md). История11K сохранена, результатыW2 добавлены отдельно с каноническими ссылками. [ID_MAP](ID_MAP.md) и [локальная проверка ссылок](COLLECTOR_LINK_CHECK.json) — служебные результаты сборки, не дополнительная аудитная стадия. F001–F009 — синтез; F010–F035 — подробные объектные каталоги; **F036–F069 — короткие конкретные факты с type/status/S-ID/точным branch+evidence locator**. S001–S401 —401разныхURL/локальных первичных объектов, **не401независимое подтверждение**. Код, metadata, README, card, LICENSE, release и веса одного repo образуют связанную цепочку происхождения. Ничего не выводить из количества ссылок.

## Главная доказательная картина

Две волны подготовили конкретный вход в разработку, но не выполнили обязательный аппаратный этап. Ни одна модель команды не запущена на LinQ, NN host inference/parity также не выполнялись. Реально выполнены получение и статический разбор артефактов, декодирование/просмотр выбранных данных, доказательство byte identity и малые арифметические проверки. Это подробно разведено в [F002](../RAW_FACTS.md#F002). Vendor numbers и published AP/mAP/top1 не превращаются в наши измерения.

**Условный порядок MVP:** №7 подозрение на падение с последующей наблюдаемой малой подвижностью; №1 быстрое перемещение на калиброванном fixed-camera участке при наличии собственной continuous постановки и согласованного определения; №4 видимое пламя вне разрешённой области, отдельно от smoking. Сценарии2movingforklift и3near-cameraphone — два резерва со своими gates. Никаких числовых feasibility scores. [Матрица всех8](../RAW_FACTS.md#F003), [shortlist/переключения](../RAW_FACTS.md#F004), [триархитектуры](../RAW_FACTS.md#F005), [порядокsmoke](../RAW_FACTS.md#F006), [stop-list](../RAW_FACTS.md#F007), [handoffsтемам](../RAW_FACTS.md#F008).

Generic person-zone/corridor — полезная infrastructure fallback на реальномCCTV. Учитывать её одинраз. Она не превращается в опасное сближение с **движущейся** техникой или completed climbing только из-за разных названий polygon. Ответ эксперта может согласовать узкий scope; он ещё не получен. Точность/одноуведомление важнее искусственно набранных трёх названий.

## Конкретные ссылки для основного рассказа

| Предмет | Короткие факты | Подробный каталог |
|---|---|---|
| Exact YOLOX bytes/hash, graph, rawdecoder | [F036](../RAW_FACTS.md#F036),[F037](../RAW_FACTS.md#F037) | F014 |
| YOLOX preprocessing ambiguity и выбранный BGR test hypothesis | **[F038](../RAW_FACTS.md#F038),[F039](../RAW_FACTS.md#F039)** | F014 |
| Official pose exact PT и embeddedAGPL/historicalGPL source | [F040](../RAW_FACTS.md#F040) | F014/F015 |
| RTMPose exact ZIP/ONNX, оба symbolic outputs, SDK RGB/min-score affine recipe | [F041](../RAW_FACTS.md#F041)–[F043](../RAW_FACTS.md#F043) | F014 |
| Четыре coreMP4 primaryCCBY4 byteidentity и per-use scopes | **[F044](../RAW_FACTS.md#F044),[F045](../RAW_FACTS.md#F045)** | F015 сготовымиcredits/notices |
| Grosslowmotion6.432033s, EOF, H/censoring/controls | **[F046](../RAW_FACTS.md#F046),[F047](../RAW_FACTS.md#F047)** | F016–F018 |
| Weizmann matched gait samples, encoded25vs50page; CHAD route | [F048](../RAW_FACTS.md#F048),[F049](../RAW_FACTS.md#F049) | F019/F020 |
| Forklift exactnames/hash/MIT publisher signal и real/synthetic media | [F050](../RAW_FACTS.md#F050),[F051](../RAW_FACTS.md#F051) | F021–F023 |
| Fire two exactPT, GTdefects, allowedpolicy/media rights | [F052](../RAW_FACTS.md#F052)–[F054](../RAW_FACTS.md#F054) | F026/F035 |
| SafetyVision actualgraph/cardmap; Thalos reject; cigaretteuntrainedstring | [F055](../RAW_FACTS.md#F055)–[F057](../RAW_FACTS.md#F057) | F012/F027/F028/F031 |
| Temporalreserves/phone/fence/height-load limits | [F058](../RAW_FACTS.md#F058)–[F061](../RAW_FACTS.md#F061) | F016/F024/F025/F028–F032 |
| Vendorpose row strictlimits / actualaccess | [F062](../RAW_FACTS.md#F062),[F063](../RAW_FACTS.md#F063) | F010/F011/F013 |
| Fixedgridtracker/strictTTL/episode/ledger/matching/clocks | [F064](../RAW_FACTS.md#F064)–[F069](../RAW_FACTS.md#F069) | F033/F034 |

## Оговорки, которые должны пережить оба отчёта

1. **YOLOX:** exact official release graph получен и полныйSHA известен. Однако tag12AugRGB-normalized,asset18Aug,releasebody19Augnormalizationremoval иcurrentREADMEсBGR на тотжеURL противоречат простой historical привязке. Выбран current documentedBGR recipe как тестовая гипотеза; нет empiricalartifact-matchedgolden. Не выбирать legacy по одному tag и не объявлять currentBGR доказанным историческим соответствием. ДоPTQ нужен sanitygate; rawCPU-deviceparity сама не спасает одинаково неверную нормализацию.
2. **RTMPose:** actual graph имеет два outputs и symbolicbatch/jointaxis. Expected17изconfig не observedstaticshape. SDK/MMPoseRGB affine/minscore выбран вместо смешивания documentedrtmlibBGR/meanscore. Numericparity/staticderivative/runtime17axis не выполнялись.
3. **GMDCSA:** S3F07conservativegrosslowmotion[2.560033,8.992067]s=6.432033s; S1F11stable2.208033s. Всеrevieweddev. H10/H30:ниодногоeligiblepositive. EOFнеclear; нетrecovery/rearm/industrialholdout. Grosslowmotionнеabsoluteimmobility/consciousness. Данные допускают тест короткогоH, ноH не надо уменьшать толькорадиPASS.
4. **CCBY4:** у старых четырёх coreMP4 доказано соответствие primarygrants. Два GMDCSA ZIPmembers побайтно равны local; дваSafeUnsafe primarymanifestSHA равны localfullSHA. Не сохранять старое mirrorunverified/«видеолицензиянеустановлена» для этойчетвёрки. Personality/privacy/recordingrelease — отдельный residualscope, не автоматический запрет internalresearch/livecopyrightuse. Готовые exactcredits вF015; никакого fictional crop/blur/trim не приписывать: originalMP4unchanged, производные sheets/annotations отдельно.
5. **Supply:** YOLOX codeApache и officialreleaseprovenance — положительное основание; explicitstandaloneweightstatement не найден. Forklift authorindexMITproject — положительный publisher signal, не полностью установленный HFweight/compiledscope. Officialpose embeddedAGPL противsource8.0.77GPL не решать в пользу удобнойстаройлицензии. FireAGPLнеавтопокупкаEnterprise. SDKcompiledfiles/terms вообще не получены.
6. **Forklift:** real3_te1/7_te1 подтверждают движение машины/driver, не надёжный walkingpedestrianpositive. Synthetic00238pair реальнополучен,00298onlypartialfarcontrol;stationarynearнет. Не заявлятьrealindustrialnear-missvalidation,метры/TTC или completepublicroute. Driver не отдельный пешеход собственноймашины.
7. **Fire:** обаexactPTnames0smoke1fire подтверждены. Rabah выбран по provenance/readiness послеW2, не measuredaccuracy/speed. FURGXMLextraendrow/staleboxesнаcuts/falseemptyflame иheader29vsactual29.97 нельзя замолчать. FURGCC0/FIRESENSECCBYgrants сохранить вместе с IEEEtitle/UltimateChasewatermark residualscope. R3E6 имеет opposite0Fire1Smoke;readyONNX/hash/scriptsпоpublisher,grantunknownreference. Fireнеsmoking.
8. **Vendor:** pose104.8FPS/21.51msHP и419.2/21.51HPQ — text-extractedreportedmeasurement,visualverificationunavailable. OriginalPDFbytes/hash/images нет. FooterRuntime16.18.6/Framework2026.8.43 не matchedteamversion. Noexactcheckpoint/input/precision/timerscenario;ResNetpage3/4difference сохранена. 1/FPSнеlatency/numbercameras/eventSLA.
9. **Temporal:** fixedanalysisgrid выбран, initial5Hz лишьcandidate. dt1 как шагсетки допустим;frame_rateменяетbufferнеF/Q. Для strictTTL нуженpre-associationprune: штатнаяlostassociation раньшеexpiry допускаетreactivation. Empty-skippingcallback,first-seentimer,globalcooldown/permanentblacklist не готовыесобытия. Ledger+keyedUIonce — проект, не выполненныйPASS и неуниверсальный exactlyoncetransport/restartidentity.

## Q/E и исходы критики

[Q001–Q003](../OPEN_QUESTIONS.md#Q001) требуют официальной выдачи/трактовки. [Q005](../OPEN_QUESTIONS.md#Q005) — preprocessing/parity. [Q006](../OPEN_QUESTIONS.md#Q006) — fallH/longtail. Q007–Q016 — scenario-specificgates. [Q017](../OPEN_QUESTIONS.md#Q017) — конкретная публичная поставка с сохранением положительныхgrants. Q018–Q020 — tracker/UI/cadence/clocks/holdout.

Первые практические проверки: **E001организаторскийgolden/deviceproof → E002одинexactNN/sanity/parity → E003/E009одинbehavioralpositive+hardnegativeчерезevent/journal/keyedUI**. ОстальныеE004–E010 адресно закрываютlongtail/movement/forklift/fire/rarevisibility/optionaltemporalroute. ВсеPROPOSED/NOT_RUN, неfulfilledmeasurements.

K001–K011 получили11исходов. Частично закрыты source/binary/media/grantподчасти, но нет полного закрытия hardware/eventgate. K008exact4copyrightidentityclosed — значимое положительное закрытие; K003 появился unresolvedpreprocconflict;K004 теперьshorttailреальноесть;K005realpositiveвсёещёнет;K006narrowgaitsampleесть;K007fireусилен;K009/K011boundeddesignвыбран,implementationнепроизведён;K010visual/bytesopen. ИсторическиеpendingвначалеCRITICотносятсякдоW2,actualstatusesвдобавленномразделе.

Автору не нужно перечитывать401URL как401исследование или повторять network. Достаточно сначалаF001–F009,даннойкартыgranularfacts иQ/E,затемоткрыватьподробныйкаталогдляexactliterals/backup/rejectedobjects. Отчёт должен стать связной русской инженерной историей с ясным условным выводом; не переносить плотный табличный/служебный синтаксис базы в готовую прозу. Сжимателю затем сохранить meaningfulbackupmodels/data/classmaps/rights/условия,а не толькоshortlist.
