# W1-11. Производительность LinQ: что именно измерено

Проверка: 2026-10-23, примерно 04:20–04:37 Europe/Moscow. Исследование первичных публичных материалов; собственных запусков LinQ, TPU Runtime, компиляции или inference НЕ было. Отдельно выполнена минимальная Python-проверка обращения к отсутствующему атрибуту argparse.Namespace и статический разбор чужого кода.

## Главный вопрос и ответ

Можно ли из публичных показателей LinQ обещать задержку и число камер конкретного хакатонного решения? Нет. Появилась полезная актуальная таблица производителя с устройствами HP/HPQ и версиями окружения, но без input shapes, весов, модели preprocessing/postprocessing, сценария LoadGen и определения latency. Она пригодна для выбора первых экспериментов, а не для SLA. HPS — агрегированный модуль, его 960 INT8 TOPS нельзя присваивать одной карте, одному чипу или выделенному участнику cloud-ресурсу.

Сильная дополнительная находка: существуют настоящие первичные MLPerf v0.7 logs, configuration, code и model locator IVATech. Это **историческая FPGA на Alveo U200**, не измерение LinQ H1M/HPQ/HPS 2026. Архив показывает, какие условия должны сопровождать современные числа, и непосредственно объясняет, почему Offline FPS не равен single-request latency. Не использовать его как доказательство скорости или ABI нынешней платформы.

Практическое обещание команды до доступа: «проверим и покажем выполнение выбранной модели на выделенном LinQ; сообщим измеренную сквозную задержку и устойчивую пропускную способность при указанной нагрузке». Обещание конкретного числа RTSP-камер пока не обосновано.

## Факты: тип доказательства отдельно от выполненной проверки

### F01. Актуальная vendor benchmark-таблица, а не собственный тест

Тип: `reported_measurement` + `vendor_statement`. Проверка: собственный сетевой TinyFish fetch прочитал PDF; web open, CLI TLS и попытка браузерного визуального просмотра не дали отрендеренную страницу. Следующая транскрипция — **извлечённый текст, визуальная верификация не выполнена**. Источник W1-11-S01, p4, таблица «Производительность»; десятичные запятые сохранены.

| Сеть | Batch | HP FPS | HP latency, ms | HPQ FPS | HPQ latency, ms |
|---|---:|---:|---:|---:|---:|
| anti_spoof_mn3 | 1 | 1561,1 | 985,72 | 6244,4 | 985,72 |
| inception_v3 | 1 | 287,1 | 4,77 | 1148,4 | 4,77 |
| inception_v3 | 8 | 480,8 | - | 1923,2 | - |
| lenet5 | 1 | 12519,7 | 128,90 | 50078,8 | 128,90 |
| lenet5 | 8 | 84961,6 | - | 339846,4 | - |
| mobilenet_v2 | 1 | 1201,7 | 1,44 | 4806,8 | 1,44 |
| mobilenet_v2 | 8 | 2456,8 | - | 9827,2 | - |
| resnet152 | 1 | 228,4 | 5,34 | 913,6 | 5,34 |
| resnet50 | 1 | 432,9 | 2,99 | 1731,6 | 2,99 |
| resnet50 | 8 | 1112,8 | - | 4451,2 | - |
| ssd_mobilenet_v2 | 1 | 556,7 | 3,54 | 2226,8 | 3,54 |
| ssd_mobilenet_v2 | 8 | 428 | - | 1712 | - |
| yolo5s | 1 | 106,1 | 23,71 | 424,4 | 23,71 |
| yolov8n_pose | 1 | 104,8 | 21,51 | 419,2 | 21,51 |

Сноска связывает измерение с методикой MLCommons MLPerf и средой Intel Core i7-10700K @3.80GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43. Нет submission ID, LoadGen version/scenario, input sizes, weight hashes, calibration/quality, latency percentile, queue depth, числа активных чипов/процессов, clocks, границы I/O, decode/NMS. INT8 указан в линейке аппаратуры, но precision каждого эксперимента отдельно не раскрыт.

### F02. Внутренняя проверка чисел опровергает простые экстраполяции

Тип: `inference`; проверка: арифметика по S01, без железа.

- Во всех строках HPQ throughput ровно в четыре раза выше HP, а latency одинакова. Это совместимо с агрегированием независимых процессоров; не доказывает четырёхкратного ускорения одиночного запроса. Не установлено, действительно ли HPQ измерен независимо или таблица масштабирована арифметически.
- ResNet50 HP reciprocal throughput = 1000/432,9 ≈2,31ms, тогда как опубликованная latency2,99ms. HPQ reciprocal =0,578ms, опубликованная latency остаётся2,99ms. YOLO5s HP reciprocal ≈9,43ms против23,71ms. Значит, FPS и latency не описывают один последовательный цикл одинаковым способом. Возможны разные сценарии, overlap, очереди, percentile; конкретный механизм неизвестен.
- Пара значений anti_spoof/lenet выглядит необычно при заголовке ms. Нельзя молча делить эти latency на1000 или объявлять опечаткой: микросекунды/ошибка извлечения/исходная ошибка/другой знаменатель — только гипотезы. Браузерная попытка не смогла отрендерить PDF и повторила extract; это **не независимое визуальное подтверждение**.
- Batch8 для SSD MobileNetV2 даёт меньший FPS, чем batch1. Нельзя обещать рост от batching вообще. У batch8 не опубликована latency, поэтому выигрыш throughput ResNet не означает улучшения реакции камеры.
- p3 той же презентации имеет другие округлённые ResNet50 HP значения460/1046FPS при batch1/8, p4 —432,9/1112,8. У p3 нет сопоставимого полного протокола. Это разные показатели внутри документа, не доказательство регрессии SDK.

### F03. HPS, карта и чип — разные уровни

Тип: `vendor_statement`/`primary_documentation`; проверка: web прочитал S02/S03/S04, собственный fetch S01.

На /tech LinQ H имеет24INT8 TOPS, SRAM16MB и двухканальный DDR4+ECC controller. /sol описывает HPQ на четырёх LinQ H,96TOPS. HPS datasheet задаёт3U node,960INT8 TOPS,640GB DDR4 ECC,2×PCIe×16 Gen4; ResNet50 batch1~2,3ms и потенциальные1,5ms. INT8 основной, FP16/BFloat16 названы перспективой. Дополнительное аппаратное video-codec оборудование опционально. В p3 презентации колонка HPS не содержит ResNet50 FPS; p8 объединяет40+ моделей; p9 HPC объединяет два HPS и server,1920TOPS,100+ моделей.

Инженерный вывод: суммарная память640GB не доказывает, что одна программа видит непрерывное640GB пространство или компилятор автоматически разбивает одну модель между всеми процессорами. Число одновременно размещаемых/исполняемых моделей не равно числу камер, частоте запросов или deadline. Опция codec не подтверждает, что штатная карта сама декодирует RTSP. Не присваивать облачному участнику весь HPS/HPC без идентификации выделенных устройств и contention.

### F04. Guide документирует влияние компиляции и TLM, не end-to-end benchmark

Тип: `primary_documentation`. Проверка: чтение сохранённого соседней веткой текста публичного guide S05; не выполнен локальный fetch оригинала и не запускался код.

Guide2025 RU.РМДВ.04.06.014-03 34 01, §3.2/p9–10: DEFAULT и STAGING, параллелизм pipeline, второй DDR, placement/cache и fusion. Для STAGING прямо оговорены возможная длительная компиляция и неверные программы, fallback DEFAULT. §3.3/p17 выводит `execution_time_us` как оценку TLM. §3.1 задаёт batch при построении графа; §3.3/p16 отмечает batch-sensitive quantized graph. Значит, время simulator/TLM нельзя представлять измерением runtime; preset и batch — обязательные параметры протокола. Версии хоста2025 (Ubuntu20.04/Python3.11/RAM≥32GB) не совпадают с benchmark environment2026; нет основания устанавливать одно окружение как универсальное.

### F05. Публичный авторский repo даёт три разных знаменателя скорости

Тип: `source_code`. Проверка: прочитан pinned source S06–S08 локального clone, S06 также открыт сетевым web; inference не запускался. Commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`.

1. `run_resnet50_performance.py:44–146`: wrapper вызывает `mlperf -s offline -m performance -p ... -q ...`, default QPS500 для batch1 и1000 дляbatch8,3runs. Берёт `Samples per second`, проверяет `Result is: VALID`. QPS — requested workload parameter, не измеренный FPS. Код не публикует сам результат; .tpu и vendor mlperf binary нужны отдельно. Наличие mlperf в названии файла не делает запуск официальной submission.
2. `run_resnet50_parallel_direct.py:201–314`: отдельный subprocess на explicit device/shard; `effective_fps = total / wall_sec`, таймер до Popen и до завершения всех процессов. Это включает startup/import/data/model-load/accuracy/output work. `shards[].throughput_img_per_sec` использует иной внутренний знаменатель, поэтому их сумму нельзя непосредственно сравнивать с aggregate effective_fps.
3. `run_yolov8_tpu.py:269–334`: таймер только вокруг `run_once`; imread/letterbox/BGR→RGB/float normalization/batching выполняются до, NMS/box mapping/predictions JSON после. FPS в summary =measured_images / infer_time, не скорость pipeline. warmup10images; частично пересекающая warmup batch учитывает полное batch-время при частичном числителе, последний batch может padding. Нет распределения individual latency. Вариант `inference.run`/`sync` выбирается по наличию атрибута; семантика полного завершения ветки run не доказана.

### F06. Подтверждённая локальная проверка ошибки примера

Тип: `source_code` + `local_observation`. Проверка: AST нашёл `args.output_tensอร์_name`; parser объявляет `--output-tensor-name`. Минимальный `argparse.Namespace(output_tensor_name='out')` с getattr на фактическую Unicode-строку дал AttributeError. Артефакт `_WORK/W1_11/STATIC_CHECK.json`. В source обращение происходит до Device.list_devices/open. Полный скрипт не запускался: он может ранее остановиться на missing files/dependencies. Это дефект стороннего примера, не обнаруженная ошибка LinQ SDK. Не называть repo готовым воспроизводимым benchmark без исправления и реального TPU-run.

### F07. Историческая Python binding помогает определить границу API-time

Тип: `source_code`. Проверка: прочитан S09 из сохранённого source pytpu15.0.24, runtime не загружался. `_bindings.py:387–416` sync резервирует I/O buffers, подготавливает pointers, вызывает native run, получает NumPy output и проверяет status. Следовательно даже sync wall-time этого кода шире device compute. README той поставки описывает старый iva_tpu interface и timings/stats; в фактическом `_bindings.py` соответствующих методов timings/stats нет. Не обещать доступность profiler/stat fields по README и не переносить ABI2023 на Runtime2026. Source предлагает повторно использовать inference session, поэтому создание model/session на каждый кадр исказит steady-state тест.

### F08. Настоящие исторические MLPerf logs и условия (существенная новая ветка)

Тип: `reported_measurement` + `source_code` + `primary_documentation`. Проверка: выполнены независимый web search, GitHub API tree и HTTP чтение оригинальных файлов S10; файлы сохранены в `_WORK/W1_11/MLPERF_2020`. Это **чужой состоявшийся тест**, не наш запуск.

Closed/IVATech, `iva-fpga-1`, statusRDI/edge; AlveoU200,250MHz,1accelerator, i7-7700K4.20GHz,16GBhostRAM,Ubuntu18.04,TF1.15.0. Measurements JSON: inputINT8,weightsINT8/FP16,quantization без retraining, исходные веса `https://zenodo.org/record/2535873/files/resnet50_v1.pb`. Code QSL готовит shape[1,224,224,3], preprocessing до query. SingleStream run1 VALID: p90=12,230138ms,mean12,081844ms,p99=12,345478ms,max14,198754ms,QPS incl overhead82,37; samples/query1,max_async1. Offline run1 VALID:88,8239samples/s, samples/query24576, aggregate query276,682437431s; один logging-allocation warning, ошибок нет. Accuracy75,756%,50000images.

Разницы файлов тоже существенны: system JSON называет libtpu7.1.15/compiler13.1.0; README перечисляет libtpu7.1.17/compiler14.0.0. QSL source возвращает PerformanceSampleCount10, log фиксирует1024. Это запрещает утверждать, что сегодняшняя копия всех source-файлов побайтно описывает использованный бинарник. Исторические условия всё равно намного прозрачнее современного слайда. Подробности и exact locators в реестре ниже.

Инженерный вывод: Offline aggregate latency276секунд означает длительность большого query, а не задержку одного кадра276секунд. Точно так же inverse88,8239FPS не заменяет p90 single-stream12,23ms. Это первичный конкретный контрпример смешению знаменателей. Подмена этой FPGA современным24TOPS ASIC или линейное умножение результата по частоте некорректны.

### F09. Авторские эксперименты2025 сообщают ограничения оптимизации

Тип: `reported_measurement`. Проверка: сетевое чтение первичной статьи S11 целиком; linked таблица cloud.mail.ru вернула404, поэтому её чисел не видел. Авторы Сергей Нефёдов, Руслан Качмазов, Лев Бабинцев, мастерская ВШЭ/VK. Статья30.03.2025 от аккаунта fivanov. Для IVA TPU описаны режим с предварительно загруженными данными и последовательный latency, batch1/2/4/8, проблемы compile/run некоторых STAGING-вариантов. Нет пригодной полной фиксации board/runtime/model hashes/input/quality для переноса на2026.

Авторы оценивают arithmetic throughput вручную через операции×FPS и называют floating-point производительностью; это не следует автоматически интерпретировать как физически выполненные FLOPS, INT8 TOPS или измеренные performance counters. Числа утилизации из статьи не дают коэффициент пересчёта для нашего решения. Их сообщение о remote GUI является историческим авторским опытом, не подтверждением доступа участников2026.

### F10. Университетская работа2026 — зацепка, но full protocol недоступен

Тип: `reported_measurement` на уровне авторской аннотации. Проверка: web прочитал metadata S12; повторные web/TinyFish/CLI запросы нестабильны. Полный текст не прочитан. Магистерская ВКР Рудь Иван Васильевич, СПбПУ, 2026, визуальная локализация БПЛА/LinQ H. Аннотация перечисляет ResNet34 — 443 FPS; ResNet50 — 430 FPS; MobileNetV2 — 142 FPS; YOLO11l OBB — 20 FPS. Таблица прав: Internet full text — авторизованные пользователи СПбПУ, анонимные без действия чтения. Shape/batch/runtime/precision/denominator не установлены; возможна несопоставимость моделей и сценариев. Особенно MobileNetV2: 142 против 1201,7 FPS на vendor slide — повод выяснять условия, а не объявлять ошибочным один источник.

## Почему число камер пока не следует ни из одного результата

Это `inference` и план измерения, а не цитата источника.

TOPS — число арифметических операций при определённой precision/clock/utilization; камера задаёт decoded resolution, codec, frame rate, inference cadence и deadline. Между ними нужны decode, resize/letterbox, copies/network transport, inference, NMS, tracking, бизнес-логика, serialization. Много камер создают очереди и хвостовые задержки. Один поток может требовать нескольких моделей, crop-inference по множеству объектов, либо пропуска кадров. Разделение одного FPS на «25кадров/с» не устанавливает real-time capacity.

Допустимый после доступа расчёт является лишь нагрузочной гипотезой: суммарная потребность inference = сумма(camera inference cadence × число model invocations). Её надо сверить со **сквозным** sustainable throughput при целевом p95/p99 и drops/queue age. Не подставлять vendor ResNet FPS вместо нашей detection/pose/tracking pipeline. Не измерять throughput на повторённом blank input без accuracy и выдавать за полезные camera FPS.

## Неизвестное, противоречия и адресные проверки

1. **Timing contract p4**: у производителя запросить exact input/output tensor shapes, model/weight hashes, preset, INT8 calibration/accuracy, LoadGen commit/scenario/config, pXX/mean, includes transfers/pre/post, count devices/queues. Отдельно исходные логи anti_spoof/lenet и подтверждение единиц. Без этого latency остаётся vendor claim с неопределённой областью.
2. **Allocated hardware**: модель платы/число чипов и `/dev/tpu*`, частота/power cap, память на device, загрузка другими пользователями. Online endpoint может выделять fraction общего HPC; throughput одной карты не гарантирован облачному запросу.
3. **Memory and concurrency**: загрузить одну модель, записать resident device/host memory до/после, начать1session и1request, затем несколько sessions/models/devices при доступном API. Проверить memory-release и устойчивость без предположения общего640GB pool. Не использовать неподтверждённые API из старого README.
4. **Historical artifacts**: архив2020 полезен как протокол и C API пример, но установка7.x libtpu/14.x compiler не предлагается. Отсутствие современной submission в выполненном поиске не доказывает, что её нет.

## Конкретный первый эксперимент после доступа

**E11-01, переносимость и baseline,30–60мин**: сохранить environment/device inventory; SHA256 исходной и скомпилированной модели, compiler preset/batch; один известный image, проверить numerical result/accuracy против CPU reference. Цель — подтвердить полезное исполнение на device до обсуждения скорости. Отдельно compiler/TLM result и physical runtime result.

**E11-02, границы latency,30–45мин**: после заранее объявленного warmup измерить монотонным clock отдельно decode/preprocess, API sync включая transfers, postprocess, полный request и remote roundtrip. Зафиксировать count,mean,p50,p95,p99,max; model/session load и cold start отдельными строками. Если API asynchronous — дождаться completion до stop timer. Сохранить raw per-request records, не только итоговый FPS.

**E11-03, реальная capacity,45–60мин**: batch1 и один поток; затем увеличение offered load/числа потоков и отдельно batch при поддержке. Записать actual completions/s,queue age,drops/errors,p95/p99,memory и power/clock если доступны. Начать с одного явного device, затем с нескольких. Остановить рост при нарушении целевого deadline; не усреднять хвостовые задержки между повторами. Проверить, что outputs и качество сохраняются.

**E11-04, камеры,после первых трёх**: включить реальные codec/resolution/cadence/transport/tracking, ограниченные очереди и frame-drop policy; мерить от timestamp получения кадра до события UI. Камерный claim делать только для этой конфигурации с запасом относительно насыщения. На RTX4070 измерять тот же pipeline/shape/quality, фиксируя фактический VRAM и software; это baseline разработки, не замена обязательному LinQ execution.

## Реестр источников и точные locators

Все URL ниже прочитаны/проверены 2026-10-23 около 04:20–04:37 MSK. Даты обхода поисковика не использованы как даты выпуска.

| ID | URL / title / author / date | Locator и ограничения |
|---|---|---|
| W1-11-S01 | https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf — российские решения ускорения нейросетей, ОООХайТэк,2026; PDF metadata автор СергейСеврюков | p3hardware; p4benchmark+footnote; p8HPS; p9HPC. TinyFish text fetched лично, visual render не удался. Нет raw logs/inputs. |
| W1-11-S02 | https://lin-q.ru/sol — Модули ускорения LinQ,ОООХайТэк,dateunknown | sections HPQ/HPS, web lines124–183; product claims, не протокол. |
| W1-11-S03 | https://lin-q.ru/tech — Технологический стек,ОООХайТэк,dateunknown | chip characteristics lines34–53; только peak/spec. |
| W1-11-S04 | https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf — LinQHPS datasheet,ОООХайТэк,dateunknown | p1keyfeatures,p2specs,p3codec. web PDF открыт,4pages. |
| W1-11-S05 | https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf — руководство пользователя2025, RU.РМДВ.04.06.014-03 34 01 | §3.1p7–8,§3.2p9–10,§3.3p16–17. Прочитан `_WORK/W1_03/Framework_manual_H1_extracted.txt`, не собственная download. |
| W1-11-S06 | https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/classification/run_resnet50_performance.py — sherstpasha,commit2026-04-03 | resolve_qps,main,parse_mlperf_summary; side author code, не результат и не vendor distribution. |
| W1-11-S07 | https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/classification/run_resnet50_parallel_direct.py | run_scale lines201–314; просмотрен source в pinned clone. |
| W1-11-S08 | https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py | main lines187–341; Unicode attr208,clock269–271,NMS274+,accounting312+. |
| W1-11-S09 | https://pypi.org/project/pytpu/15.0.24/ — pytpu,2023; source SHA256 e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f | `_bindings.py:307–416`,README89–101. Локальная копия `_WORK/W1_09/PYTPU_SOURCE`; ABI2026неизвестен. |
| W1-11-S10 | https://github.com/mlcommons/inference_results_v0.7/tree/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech — IVATech submission,MLPerf0.7,2020 | systems/iva-fpga-1.json; measurements/iva-fpga-1/resnet/{SingleStream,Offline}/iva-fpga-1_v1_*.json; results/iva-fpga-1/resnet/{SingleStream,Offline}/performance/run_1/mlperf_log_summary.txt; SingleStream/accuracy/accuracy.txt; code/resnet/v1/IvaTPUQuerySampleLibrary.cpp. Историческая FPGA. |
| W1-11-S11 | https://habr.com/ru/companies/vk/articles/895432/ — «Адаптированные нейросетевые алгоритмы на отечественных процессорах»,Нефёдов/Качмазов/Бабинцев,VK/ВШЭ,2025-03-30 | IVA TPU section,lines96–132. Linked table https://cloud.mail.ru/public/zMRN/F2XL5Qxv3 returned404. Часть claims операционно неточна; не независимая сертификация. |
| W1-11-S12 | https://elib.spbstu.ru/dl/3/2026/vr/vr26-931.pdf/info — «Исследование тензорных вычислителей компании ХайТэк на задачах локализации БПЛА…»,РудьИ.В.,СПбПУ2026 | metadata/abstract/access-rights. Полный PDF ограничен авторизованным СПбПУ; shapes и timing protocol недоступны. |
| W1-11-S13 | https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc — MLCommons Inference rules,текущая ветка | §3Scenarios; §4 benchmark metadata requirements. Rules master не отождествлять с версией измерений2020или2026. Сохранён MLPERF_RULES.adoc. |
| W1-11-S14 | https://lin-q.ru/press — Пресс-центр,ОООХайТэк,dateunknown | sectionМатериалы,linkПрезентация; подтверждает официальный provenance S01. |

## Реальный поиск и ошибки доступа

Использованы web search/open и запасной search_service, TinyFish fetch, read-only browser automation для одной PDF-страницы, requests/curl и GitHub API. Запросы: LinQ H benchmark latency YOLO ResNet2026; LinQHPSпроизводительность; exact LinQ432,9; LinQMobileNet142; site:lin-q.ruMLPerf; site:mlcommons.orgLinQ; IVA TPU MLPerf2020; HiTech inference_results_v0.7; название статьи ВШЭ; exact filename презентации. Шум .NETLINQ, GoogleTPU, однофамильцев LinQ отсеивался.

S01: web/search_service internal error; curl Schannel TLS handshake failure; Python SSL UNEXPECTED_EOF_WHILE_READING; HTTP remote disconnected. TinyFish fetch открыл PDF-text. Browser run https://agent.tinyfish.ai/runs/48b64bc0-46b1-4fc2-90ad-6cf83794fbd6 завершён: PDF не отрендерился, browser показал link/dark background, повторно извлечён текст. Поэтому отдельный visual channel НЕ подтвердил числа; незаметно выдать extract за screenshot было бы ошибкой.

S12: первичная metadata иногда доступна web, повторные запросы timeout/proxy_error, CLI TLS EOF. Полный guessed download route не открылся; access-rights table уже объясняет ограничение anonymous. Не обходились ограничения авторизации. S11cloud.mail linked таблица404. GitHub API/raw доступны, документы2020сохранены. Начальный printUnicode в PowerShell console выдал UnicodeEncodeError; JSON уже записался, проверка повторно прочитана с PYTHONIOENCODING=utf-8. Ни один сбой не выдан за отсутствие самого источника.

## Handoff

Для основного отчёта взять p4 как vendor-reported ориентиры и все ограничения рядом; обязательно сохранить различие HP/HPQ/HPS/HPC, single request / aggregate FPS и отсутствующие shape/weights. Запросить vendor raw log/latency definition раньше обещания камер. Новые первичные2020логи дают убедительный пример разных знаменателей, но не современную скорость. СтатьяВШЭ и ВКРСПбПУ — адресные независимые зацепки, их численные результаты без недостающих условий не объединять в среднее.
