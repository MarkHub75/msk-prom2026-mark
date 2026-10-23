# Передача редактору человеческого отчёта

Авторская роль завершена 2026-10-23 23:43:50 Europe/Moscow (clock20:43:50UTC). Новых сетевых доказательств, установки/импорта SDK, моделей, benchmark/training/export/device/quality запусков и субагентов автор не создавал. Доказательные реестры не изменены.

## Готовый артефакт

- [DRAFT_HUMAN.md](DRAFT_HUMAN.md): 149646 bytes, 113166 Unicode characters, 519 строк, 12237 whitespace-delimited words на момент авторской проверки. Это самостоятельный большой русский отчёт, не финальный human.
- Финальный `report_human_model_fidelity_quantization.md` создаёт отдельный редактор. Машинный отчёт — отдельная следующая роль.

Композиция причинная: рекомендуемый путь/границы доказательства → понятие fidelity и пять gates → ladder A → provenance/golden C → preprocess/geometry/heads/NMS → export/graph → numeric/PTQ → recovery и опубликованные измерения → small/pose/temporal → symptom classifier B → LinQ route/version seams/access regimes/alternatives → quality/uncertainty/AR01 →12E → decision tree D →5-person actions/handoffs →jury F.

## Покрытие и что сохранять

Все A–F включены. Есть сравнительные таблицы stage/symptom/cause/diagnostic/remedy/risk/evidence, method/access/backend/benefit/cost/verification, model/output/quant/import/LinQ-level/next-test, metric/unit/split/interpretation/limits. Подробно раскрыты все12 **единых** E001–E012, с exact links в OPEN_QUESTIONS; никаких новых E-ID не заведено. Для каждого описаны цель/owner, requirements, stage pair, будущие role-based samples, процедура/outputs, device evidence либо N/A, исходы и cannot-prove. Первые priority tests E002/E003/E005 явно зависят отE001/Q001–Q003 иE004 передE005.

Выбранные автором стартовые организационные количества pack24–40frames/8–12clips явно **proposal**, не evidence достаточной мощности. Бюджет E011 до6semantic regions+2boundary probes унаследован из единой программы, тоже выбранный/согласуемый. Порогиδ/floors/caps/D/α и scope всё ещё TEAM_DECISION_PENDING; actual data/weights/SDK/access отсутствуют, MEASURED none. Ни один E не пройден. Исторические contest45h не перезапущены.

Особые W2 corrections сохранены:

- Source runtime outputs не подменены ONNX ReferenceEvaluator expected; same tensor и complete media pipeline раздельны.
- U8.3.230 commit389b87f8cb9dbf2f31be8b70a94a3e47e11693db связывает helpers; prepared eager/fusion/export flags — отдельный parent; simplifyFalse не выключает folding/fusion.
- Native rect condition включаетdynamic non-IMX, Model.predict добавляетrectTrue. G01/G03 геометрия иG04 no Pose box round/no low-conf xy zeroing сохранены; docstring не implementation.
- BCN/no-objectness/decoded DFL+sigmoid/custom nc1/2/3, Pose tail, nc2 mistaken BNC final6 shortcut (explicit nc/end2endFalse не выключают), NMS in-place/ties/branch/caps/padding/time-limit сохранены.
- onnxsimcheck_n0/check_ok, PyTorch arbitraryverificationthresholds неqualitybudgets; IR/opset/Resize/Softmax/layout schema различены.
- Converterclipping1e−7/1e4 неlimitsFP16; BF16range/mantissa; dtype storage/input неcompute proof.
- ORT1.22Percentilefactory99.999/docstring99.99; NNCFMIXED неFP16/INT8; sample-statistic vsaggregation; LinQpercentileweights-wording/default100/currentformulaunknown, blanketTypeErrorretry неunsupportedkeyword proof.
- Current LinQ QDQ/sidecar/QAT/mixed consumer UNKNOWN. E007 beforeGPU; grid preservation/FP islands/upstreamloss иboundaries невыдуманы.
- ORTconverter1.16ModelProtoCPU иseparateprovider-selectablemodel-path API, ORT1.23.2CPUFP32casts инеpinruntime неупрощены доGPU-only/CPUimpossible.
- Четыреpublishedmeasurementcardsсцифрами/условиями/unknowns, отрицательныйYOLOX ипрямойncnnposeINT8 evidence сохранены; неourresults/неLinQforecast. Partial/QAT иPTQrecipes несклеенывsequentialrun.
- Guide/currentsource/oldPyPIREADME/benchmarkversionsразнесены; pytpu15.0.24имеетDevice/Program/Inference,lazynativeCDLL. Guide-03неwheelrelease. Returnassignmentнеsingle-returnproof; O1/O5aliasesнеустановлены; extractedplatformdiscrepancyнеverifiedmanualbug.
- ONNXvalue/Node/TFportidentity, firstoutput/stripport/staticmetadatarewrite — отдельныеclientrisks; supplierfloatgateнепропущен.
- FULL/PRE/POST/RAWmode≠RAWprogram; bytepointer≠INT8numeric; view≠dequant; Codec требуетinternal tpu_tlm_is/currentavailabilityunknown. syncdocumentedblocking неопределяет .runcurrentABI.
- VendorTinyYOLO3author-done неself-buildYOLOv8measurement; rawmetrics/logsнедоступны; vendorperformanceextractionнеvisualverification. PythonbatchwarmupseamнеприписанnativeMLPerf/table.
- RT-DETR-lGridSample16/internalTopK/attention иRTMPose-mM1.3.2+D1.3.1dependencyoverride/twooutputs/crop/GAU/ScaleNorm/flip-off неготовыеLinQfallbacks. WeightsURIsнеполученныеbytes.
- ByteTrackdt1/framecount, sourcePTS/epoch/clockdomain, ReIDadditionalNN иfutureinterpolationнеonlineproof; allGTepisodesвrecalldenominator, completecensus/exposure/lostgained/unknown остаются.
- One-sidedCP/HPPформулыиnumericexamplesявноhypothetical, iid/HPP/selection/clustering/fewclusters/undefined limitations рядом. Пятьrequiredgates, absoluteB+pairedNI, HOLD/INCONCLUSIVE иscopeбезproductionguarantee сохранены.

Последний список в notes умышленно плотный служебный; в human это раскрыто нормальными абзацами, таблицами и процедурами. Редактору полезно расставить пробелы вокруг version/чисел в самых плотных table cells, не меняя literals/значения.

## Доказательная база и пути

Прочитаны оба входных договора, PROMPT_AUTHOR/SYNTHESIS_REQUIREMENTS/AUTHOR_HANDOFF, CASE_NOTES, нормализованные assertion/type/conditions/limitations карточекF001–F250, source identities/versions/provenanceS001–S188, Q001–Q019/единыеE001–E012 иCRITIC/W2dispositions; дополнительные tables/protocols RAW читались адресно, особенно source/golden/preprocess/numeric/temporal/quality/LinQ/AR01. Повторные boilerplateactual-scope поля не образуют нового свидетельства. Сохранённые ветки иoriginalsources не превращены внашиexecutions.

Главные указатели: [RAW_FACTS](../RAW_FACTS.md), [SOURCES](../SOURCES.md), [OPEN_QUESTIONS](../OPEN_QUESTIONS.md), [CRITIC](../CRITIC.md), [AUTHOR_HANDOFF](AUTHOR_HANDOFF.md), [ID_MAP](ID_MAP.md), [CASE_NOTES](CASE_NOTES.md), [CASE_LINQ.pdf](INPUT/CASE_LINQ.pdf). SourcePDFhash7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e проверенroot, автор не создавал повторного визуального чтения. Guide/presentationPDFиспользованычерезатрибутированныеprimaryextractions, невизуально.

При переносе DRAFT из `_WORK/` в корень **обязательно переназначить относительные ссылки**: `../RAW_FACTS.md`→`RAW_FACTS.md` (аналогичноSOURCES/OPEN_QUESTIONS/CRITIC), `INPUT/CASE_LINQ.pdf`→`_WORK/INPUT/CASE_LINQ.pdf`, `CASE_NOTES.md`→`_WORK/CASE_NOTES.md`, `AUTHOR_HANDOFF.md`→`_WORK/AUTHOR_HANDOFF.md`. Прямые primary URLs не менять. Составные labels `Fxxx–Fyyy` ссылаются на первый explicit anchor contiguous карточек, это навигация к диапазону, не отдельный несуществующийID.

## Авторские проверки

Встроенная проверка Python читала созданный DRAFT строгимUTF8, проверила260relativeMarkdownlinktargets, включаяexplicitanchors. **0 missingfiles/anchors**, **0replacementcharactersU+FFFD**. Все12Esections существуют ровно поодному. Проверка — служебное чтение текста/файлов, неtestmodel/export/device и неотдельнаярольаудита. После редактуры/переноса ссылочную проверку нужно выполнить внутри редакторской работы. Итоговые evidence registries не изменены.

Остатки не требуют третьегоresearch: Q001–Q011артефакты/доступ/SDK/device/инструкция; Q012policydecision; Q013rights+GT; Q014design+independence; Q015observability; Q016fallbackadmission; Q017measuredresourcepilot; Q018rawthirdpartylogs/PDFbytes; Q019optionalORTtooling. Уполномоченные owners и конкретное закрытие находятся в едином OPEN_QUESTIONS.
