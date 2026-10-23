# W2-I — современные performance claims: единицы и протокол

K011, K010, K018. Исследование 23.10.2026, примерно 05:00–05:07 MSK (02:00–02:07 UTC); точные времена фактических HTTP-загрузок в `W2_I/PRIMARY_MANIFEST.json`. Исторический контекст — ночь перед хакатоном. Публичный поиск/чтение исходников и арифметическая диагностика. **SDK/device/compile/inference не выполнялись.** Ни одно число ниже не является нашим benchmark.

## Решение и изменение относительно W1

**Не исправлять `985,72 ms` и `128,90 ms`, не обещать камеры по FPS и не объявлять HPQ независимо измеренным.** Удалось точнее локализовать недостающее доказательство, но исходная таблица остаётся text-only, а modern measurement contract неизвестен.

Новое первичное свидетельство — live GitHub API подтвердил полный pinned tree стороннего проекта, отсутствие опубликованных result/log файлов и releases; прочитан ранее не разобранный параллельный MLPerf wrapper. Он действительно поддерживает независимые процессы на разных devices и суммирует их измеренные rates, а не просто умножает baseline на N. Это опровергает слишком широкую догадку «сторонний multi-device benchmark обязательно арифметический», но **не** устанавливает ни полученное ускорение, ни происхождение HPQ столбца презентации. Связи wrapper→vendor slide нет.

Новая pinned первичная policy MLCommons прямо разделяет Offline throughput и Single Stream latency, разрешает определённую предобработку вне таймера. Поэтому расхождение reciprocal FPS/latency само по себе не доказывает typo. Не установлены сценарии именно слайда. Новой независимой современной экспериментальной линии с полными logs/model/input/quality не найдено. Habr остаётся авторским опытом 2025, ВКР — metadata/abstract. Это не три согласованных benchmark одного устройства.

| K | Статус после W2-I |
|---|---|
| K011 | Открыт: units/visual/modern logs/latency statistic не установлены; альтернативные сценарии сохраняются; corrected transcription не произведена. |
| K010 | Уточнена граница: четыре `/dev/tpu*` и процессы не устанавливают физическую SKU/одну HPQ; performance wrapper может адресовать устройства явно. Аппаратная сверка — W2-H. |
| K018 | Уточнена lineage: новые API bytes подтверждают отсутствие результатов в конкретном публичном snapshot; новый policy source подтверждает лишь семантику методики. Независимых actual modern measurements не прибавилось. |

## Факты с локаторами и actual test boundary

### W2-I-F01. Original presentation: честный отрицательный результат

S01, ООО «ХайТэк», презентация 2026, автор extraction metadata Сергей Севрюков. W2 direct `curl.exe --max-time 20 --http1.1 -k` к canonical HTTPS завершился Schannel TLS handshake failure, exit35 (05:03:23 MSK); `DIRECT_HEADERS.txt` пуст. Web open дал unavailable; screenshot PDF index3 (p4) отказал: content type не application/pdf. **PDF bytes/hash/картинки страницы не получены, actual screenshot не просмотрен.** Не повторяли бесконечно одинаковый fetch и не выдавали ответ remote agent из W2-B за просмотр.

Числа и сноска сохранены без изменения из уже имеющегося `_WORK/W1_08/presentation2026_tinyfish.json`; этот snapshot — тот же upstream source, а не новое независимое доказательство. Сноска: Intel Core i7-10700K @3.80GHz, Ubuntu24.04, Runtime16.18.6, Framework2026.8.43; методика MLCommons MLPerf. Ни сноска, ни сеть с `mlperf` в имени не являются submission ID или LoadGen log. p3 ResNet50 HP460/1046 vs p4 432,9/1112,8 остаются разными опубликованными цифрами без сопоставимого протокола.

### W2-I-F02. Записи измерений сохраняют неизвестный denominator

`W2_I/MEASUREMENT_RECORDS.json` содержит все14 строк p4, original decimal literals и batch, устройства названы HP/HPQ, `tested_here=false`, `evidence_type=vendor_reported_table_text_only`. Input/weights/preset/precision per-model/quality/scenario/latency statistic/boundaries/actual devices — null. Throughput unit из заголовка FPS; не установлено, какой именно image/sample/batch counter делится на какой run interval. Число batch8 не надо дополнительно умножать на8: семантика samples/sec wrapper и слайда не связана.

Показательные записи (source p4; единицы только по extraction):

| model / batch | HP FPS | HP latency ms | HPQ FPS | HPQ latency ms | denominator / tested_here |
|---|---:|---:|---:|---:|---|
| anti_spoof_mn3 /1 |1561,1|985,72|6244,4|985,72|не раскрыт /false|
| lenet5 /1 |12519,7|128,90|50078,8|128,90|не раскрыт /false|
| resnet50 /1 |432,9|2,99|1731,6|2,99|не раскрыт /false|
| resnet50 /8 |1112,8|—|4451,2|—|не раскрыт /false|
| ssd_mobilenet_v2 /1 |556,7|3,54|2226,8|3,54|не раскрыт /false|
| ssd_mobilenet_v2 /8 |428|—|1712|—|не раскрыт /false|
| yolo5s /1 |106,1|23,71|424,4|23,71|не раскрыт /false|
| yolov8n_pose /1 |104,8|21,51|419,2|21,51|не раскрыт /false|

### W2-I-F03. Попытка опровергнуть typo и арифметическое HPQ

Тип: arithmetic inference по S01, без устройства. У всех14 строк отношение HPQ/HP throughput=4 и одинаковые latency literals. Это совместимо и с идеальным масштабированием независимых одинаковых engines, и с расчётной экстраполяцией. При отображённой точности измеренная сумма тоже может оказаться ровно4×. По таблице метод происхождения **неразличим**.

Для batch1 `1000/FPS` не равно опубликованной latency: у anti_spoof≈0,641ms, у lenet≈0,0799ms, ResNet50≈2,310ms, YOLO5s≈9,425ms. Это не даёт права заменить источник. Если throughput измерен Offline на preloaded данных, а latency отдельным последовательным режимом с другой границей, большой разрыв логически возможен. Percentile также не равен reciprocal средней скорости. Для одной и той же последовательной нагрузки с одним outstanding запросом невозможно объяснить столь большой разрыв одним лишь обычным p90: это было бы другое, гораздо более сильное допущение, которого источник не даёт.

Диагностический product `FPS × latency_seconds` у anti_spoof≈1538,8, lenet≈1613,8; подмена ms→us сделала бы его≈1,54/1,61, как порядок ряда других строк. Это **поддерживает подозрение** ошибки единиц, но не устанавливает её. Product нельзя называть measured concurrency: это потребовало бы средней latency и одного steady-state workload. При разных сценариях/percentile Little's-law интерпретация неприменима. Оставлены все исходные значения.

Снижение SSD batch8 throughput также не исправляем: batching не гарантирует рост, в частности может менять memory placement/pipeline/preset. Причину этого конкретного результата без logs не установили. Не выдаём эту правдоподобную причину за факт.

### W2-I-F04. Новый современный primary protocol: только смысл методики

S02 — MLCommons policy commit `d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3`, committer date2026-08-20. Скачаны original source bytes, SHA256 `94c69f01f1e0be24dc057180af6db878d1f5339fd31d54cbe5c386f8e198ce08`; actual HTTP200 02:04:29UTC. `MLCOMMONS_RULES.adoc:133–150,401–420,633–658`.

Policy различает последовательный Single Stream (следующий query после ответа; primary metric p90 early-stopping latency estimate), Server с Poisson requests и ограничением tail latency, Offline с передачей всех samples одним query и throughput. Latency определяется от scheduled pass query до reply. Разрешённая sample-independent resize/channel reorder/crop/normalization может быть untimed. Следовательно generic «MLPerf включает полную загрузку/предобработку/end-to-end камеры» неверно; детали SUT/LoadGen необходимы.

Это не утверждение, что vendor использовал именно этот commit, строго исполнил эти правила или подал официальную submission. Rules2026 не подставлены в logs2020, исторический FPGA повторно не исследовался. Нового primary locator современной LinQ MLCommons submission не найдено; не делаем вывод, что submission никогда не существовала.

### W2-I-F05. Публичный repo содержит возможный протокол масштабирования, но не результаты

S03, `sherstpasha/linq-cv-bench`, pinned commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`. GitHub API tree `truncated=false`,60 tracked tree entries, ни одного пути experiments/mlperf_log/results_summary/accuracy.txt; `REPO_RELEASES.json=[]`; единственная public branch main указывает тот же commit. Публичная HTML main также не содержит results attachment. Это scope данного tree/releases/branches, **не всех исторических commits, пользовательского диска или скрытых releases**. API bytes/hash/time сохранены.

`.gitignore:31–43` явно исключает JSON, ONNX/PT/weights/H5, artifacts/, experiments*/, explanatory-results Markdown. Это не доказательство, что они никогда не были tracked, но объясняет, почему инструкция «сохранить results_summary.json» не равна публикации результата. Для закрытия запроса нужны actual logs/build_summary/.tpu hash из разрешённой автором поставки, а не повторный запуск git search.

`scr/classification/run_resnet50_parallel_mlperf.py:105–131,138–192,235–268`:

- Запускает `mlperf -s offline -m performance -p <program> -q <effective_qps>` для каждого процесса. При переданных devices **реально добавляет `--dev <device>`**, хотя help:34 говорит «for reporting only». Actual support этого CLI binary не проверена: бинарник не получен.
- Пытается наблюдать `/proc/<pid>/fd`→`/dev/tpu*` каждые0,2s. Отсутствие наблюдения не доказывает отсутствие исполнения; открытый fd не доказывает полноту graph execution. Это схема source, не collected observation.
- При всех VALID суммирует `Samples per second` отдельных процессов, усредняет по valid repeats, speedup делит на measured baseline. **Не N×baseline.** `wall_sec` от запуска до завершения процессов сохранён отдельно и не является знаменателем этой суммы. Такая сумма rates отдельных интервалов ещё не синхронное `total_completed/common_window` измерение whole system.
- `RUN_SCENARIO.txt:392–491` сообщает четыре device paths и1/2/3/4-process runs с O5 и vendor `.tpu`. Это authored instructions/reported inventory, не published outcome и не mapping four devices↔oneHPQ. Значение `128x128_asic` в имени `.tpu` не объявлять image input128×128.

Repo custom ResNet50 имеет отдельный exact source contract: exporter `ResNet50_Weights.IMAGENET1K_V2`, shape `(batch,224,224,3)`, NHWC uint8 wrapper с internal normalization (`export_resnet50_to_onnx.py:11–29,57–81`). Это **не** установленный model/input/preset vendor slide: build/weights hashes и результат не опубликованы, vendor `resnet50_mlperf` — другой artifact path. Воспроизводимое имя модели не означает одинаковые веса или качество.

### W2-I-F06. Независимые авторы: scope не расширился до comparable benchmark

S04 — Сергей Нефёдов, Руслан Качмазов, Лев Бабинцев, VK/ВШЭ, Habr30.03.2025. Повторный targeted fetch прочитал original article и outbound links; HTML extraction показывает inline figures до IVA section, а сами IVA results отправлены в cloud link. Direct linked visualization снова404. Даны авторские descriptions preloaded Performance и последовательного Latency, batches1/2/4/8, STAGING failures; нет downloadable matched scripts/logs/model+quality+version package. Это независимая авторская линия опыта, но не измерение текущих Runtime16.18.6/Framework2026.8.43/HPQ. Не приписывать ей современную precision/16TOPS physical measured arithmetic; авторы выводили operation throughput из модели×FPS.

S05 — Рудь Иван Васильевич, магистерская ВКР СПбПУ2026, «Исследование тензорных вычислителей компании „ХайТэк“ на задачах локализации БПЛА…», научный руководитель по indexed metadata Громов Виктор. Targeted search по полному автору/названию дал только library record, публичного доклада/appendix/repo не выявил. W2 web `/en/info` timeout, TinyFish `/en/info` и `/info` proxy_error, urllib `/en/info` TLS EOF; новое чтение metadata не состоялось. W1 открытый abstract с443/430/142/20FPS остаётся provenance этих чисел; W2 search snippet не повышает его до fulltext. Fulltext authorized-only не запрашивали обходом, credentials не использовали. Нет условия сопоставимости MobileNet142 vs vendor1201,7FPS; ни один источник не объявлен ошибочным.

## Реестр новых/переиспользованных первоисточников

| ID | URL, версия/автор/дата, локатор | Read channel / lineage |
|---|---|---|
| W2-I-S01 | https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf ; ОООХайТэк/СергейСеврюков,2026; p3/p4 | W1 saved TinyFish JSON reused; W2 curl/web/screenshot failures. Canonical bytes hash unknown; snapshot hash в MEASUREMENT_RECORDS.json. Один upstream со всеми W1/remote extractions. |
| W2-I-S02 | https://github.com/mlcommons/inference_policies/blob/d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3/inference_rules.adoc ; MLCommons, commit2026-08-20 | Новые HTTP200 original source bytes02:04:29UTC; hash выше; независимая нормативная линия, не LinQ experiment. |
| W2-I-S03 | https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140 ; sherstpasha,commit2026-04-03 | Existing pinned source + новые GitHub tree/releases/branches HTTP20002:04:29–30UTC; manifest hashes. Не vendor delivery. |
| W2-I-S04 | https://habr.com/ru/companies/vk/articles/895432/ ; авторы выше,30.03.2025; section IVA TPU | Новый TinyFish markdown/HTML+links около05:03–05:05MSK; тот же primary article W1, не новый experiment. https://cloud.mail.ru/public/zMRN/F2XL5Qxv3 —404. |
| W2-I-S05 | https://elib.spbstu.ru/dl/3/2026/vr/vr26-931.pdf/info ; /en/info; РудьИ.В.,СПбПУ2026 | W1 abstract reused; W2 direct fetch unsuccessful; search only confirms indexed record. Нет lawful fulltext полученного в W2. |

Сырые новые retrieval replies: `W2_I/R0_NETWORK.json`…`R3_NETWORK.json`, `N0_NETWORK.json`…`N2_NETWORK.json`, `HABR_HTML_NETWORK.json`. Direct HTTP manifest: `PRIMARY_MANIFEST.json`. Web failures и ограниченная область поиска описаны F01/F06. Поиски: точные runtime16.18.6+MLPerf, anti_spoof985, presentation filename; site:lin-q.ru MLPerf/Latency; LinQ HPQ logs; full author/title ВКР. Релевантного нового primary locator modern logs не дали. Общий web часто уводил в .NET LINQ/NYSE HPQ; эти результаты исключены, число поисковых веток не считается количеством свидетельств.

## Минимальная будущая benchmark matrix — рекомендация команды, не vendor API

Сначала зафиксировать actual SKU/revision/chips/endpoints/runtime allocation и согласованный package manifest, weights/ONNX/.qm/.tpu hashes, exact graph I/O, compile preset, calibration/eval split, postprocess. Выполнить correctness parity и task quality на отделённой eval выборке; только прошедший этот gate artifact сравнивать по скорости. Не принимать «VALID» performance за accuracy pass.

| Этап | Граница и обязательный результат |
|---|---|
| Cold | По отдельности process/import, device open, program load, session create, first completed inference. Не смешивать с warm latency. |
| Warm API | Reuse одной session; подготовленный tensor; batch1 и один outstanding; monotonic timestamps до submit и после фактического completion/materialized outputs. mean/p50/p90/p95/p99/max и count; overhead/buffers/transfers входят в API-time, пока profiler не доказал compute-only. |
| Transfers/stages | Отдельные timings host preprocessor, queue wait, API, decode/NMS/rules. H2D/compute/D2H отдельно лишь при matching supported profiler/event semantics; внешним wall timer эти части не разделять. |
| Throughput | Достаточно длинный общий steady window, completed real images/common seconds, warmup/padding исключены из числителя; outstanding/queue depth и batch фиксировать. Report dropped/stale/failed frames, tail latency при той же нагрузке. Batch8 оценивать с ожиданием наполнения, не только infer window. |
| Multi-device | Только после inventory и quota:1 device baseline и authorised N; один artifact/batch/prepost, общий interval, per-device completions, contention, общий CPU/network. Не считать sum per-process rates доказательством общего N× scaling. |
| End-to-end | От capture timestamp до доступного event/result; frame/request identity, sample rate, decode/network/pre/post, queue delay и accepted/dropped frames. Несинхронизированные remote clocks не вычитать: использовать client roundtrip либо установленную синхронизацию и её погрешность. |

Для первого решения достаточно одного approved known-good artifact, batch1, одного устройства, correctness, cold+warm session и sustained pipeline. Затем один разрешённый batch/preset вариант; расширять матрицу при изменении решения. Количество/длительность repeats и число samples выбрать под variance/дедлайн, не выдавать произвольные100/500 за норматив MLPerf. Хранить raw per-request records и summary вместе с config; QPS target отдельно от achieved throughput. Hardware count/fd observation — дополнительное execution evidence, не полная attestation.

## Точные unknown и способ закрытия

1. Vendor p4 original units/footnotes: получить именно original PDF/page image или авторское исправление; затем сверить985,72/128,90 и вернуть corrected transcription только при прямом подтверждении.
2. HPQ measured vs extrapolated: попросить per-device/aggregate modern logs, command/config/scenario/LoadGen revision, число chips/processes, `.tpu`+weights hashes и exact input/preset/quality. Одного ответа «линейное масштабирование» недостаточно для конкретной таблицы.
3. Latency metric: mean/percentile/query/sample, timer boundaries, preload/host I/O/NMS inclusion и наличие отдельных throughput/latency runs. Это одним ответом может снять unit suspicion без изменения числа.
4. Author repo: попросить существующий export experiment summaries/raw logs/build metadata или публичный author appendix; не запускать чужой workflow вслепую и не угадывать missing artifact URLs.

**Решающий эксперимент после фактического доступа:** на одной идентифицированной allocation выполнить approved quality-checked artifact с reusable session в двух явно различных режимах — sequential completed request и bounded outstanding throughput — сохранив raw timestamps/counters и common-window completed images. Он показывает реальные latency/throughput tradeoffs выданной платформы, даже если история vendor p4 останется неизвестной. Сопоставлять с vendor только после совпадения model/shape/quality/release.

**Root handoff:** использовать p4 только как vendor reported indicative table с unresolved units; не пересчитывать на камеры. Новое F05 снимает основание считать repo multi-device script чистой экстраполяцией, но не закрывает measuredHPQ. F04 закрепляет, почему методика MLPerf не означает video E2E. K011 открыт, K010 уточнён в границе topology, K018 содержит явную source lineage. Никакого нового LinQ SDK/device evidence нет.
