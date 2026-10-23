# W1E — сохранённые содержательные выписки и статус доступа

Доступ 23.10.2026 Europe/Moscow. Это краткий собственный пересказ с локаторами. Оригинальные bytes и SHA256 — MANIFEST.json. Никаких device/benchmark runs не выполнено. Дата HTTP-доступа и дата commit различны. WEB_SEARCH.json/WEB_OPEN1.json сохраняют исходный ответ web; внутренние turn IDs нужны только для истории инструмента, публичные URL перечислены здесь и в W1E_EVIDENCE.md.

## W1E-S01 MLPerf Inference Rules

URL https://github.com/mlcommons/inference_policies/blob/d3eba2f21026d868ad65cdcad2bb81e4a17ce3d3/inference_rules.adoc ; raw bytes inference_rules.adoc; commit metadata MLPERF_COMMIT.json. Автор MLCommons. Commit 2026-08-20T13:53:45Z, дата отдельного выпуска не установлена.

Локаторы §2.2 consistent system/framework, §2.7 replicability; §3 scenario table; §5.1 latency definition и accuracy/performance. Политика требует воспроизводимости и согласованной конфигурации. SingleStream оценивает последовательный отклик, Offline — throughput. Latency отсчитывается от запланированной выдачи запроса до ответа LoadGen; это не обязательно device-core time. В performance и accuracy используется тот же код. Правила MLPerf не становятся правилами Моспрома. Называть упрощённый собственный тест официальным MLPerf нельзя без соблюдения требований к результату и имени. Новые текущие scenario duration не переносятся на исторические logs0.7.

## W1E-S02 LoadGen README

URL https://github.com/mlcommons/inference/blob/master/loadgen/README.md ; pinned URL/commit/date в MANIFEST.json и LOADGEN_COMMIT.json; README.md — исходное имя. Web open tree вернул Failed to fetch restricted URL; urllib raw чтение успешно, pinned hash совпал.

Локаторы Scope of LoadGen Responsibilities, Responsibilities of a LoadGen User, LoadGen over the Network. Генератор задаёт нагрузку и журналирует запросы; модель/форматы/accuracy scoring задаются пользовательским harness. Он не удостоверяет hardware placement. Network QDL/SUT описывают явную timed boundary. Наш вывод: VALID performance и правильные query IDs полезны для measurement discipline, но не являются независимым proof аппаратного выполнения, весов и accuracy. Accuracy output нужно отдельно оценить.

## W1E-S03 ORT Execution Providers

URL https://onnxruntime.ai/docs/execution-providers/ ; ORT_PROVIDERS.html, версия страницы не задана, access date не release date. Раздел introductory architecture: GetCapability выдаёт поддержанные nodes/subgraphs конкретному provider. Use Execution Providers: приоритет списка задаёт выбор для поддержанного узла, включая переход к CPU в приведённом примере. Следствие: registry/provider list не whole-graph placement proof. Никакого LinQ EP или fallback LinQ этой страницей не установлено.

## W1E-S04 ORT Profiling tools

URL https://onnxruntime.ai/docs/performance/tune-performance/profiling-tools.html ; ORT_PROFILING.html. Раздел In-code profiling описывает JSON с thread/operator timing; EP Profiling зависит от поддержки EP/SDK. Это найденная возможность ORT, не команда LinQ и не полученный нами trace.

## Соседние первичные артефакты, реально повторно прочитанные

linq_platform/_WORK/W1_15/MLPERF_SYSTEM.txt и MLPERF_LOG.txt: IVATech v0.7, pinned subtree89260c7a0bb2bb86f4adaf1d88e0307162eb602b. System IVA_FPGA_1/Alveo U200/250MHz, host i7-7700K, Ubuntu18.04, TF1.15.0, набор runtime/compiler. SingleStream performance VALID: p90 12230138ns, max_async_queries1, min_duration60000ms. Сохранённые bytes соседнего research; не новая загрузка и не наша hardware проверка. Это историческая конфигурация, не LinQ ASIC2026.

linq_platform/_WORK/W2_J_RESULT.md: прочитана полная цепочка source table, telemetry/coverage/request matrix, service-only protocol. HPS datasheet naming profiler не даёт request trace schema; старые README/source нельзя превращать в current SDK. Подробные первичные locators в его таблице, normalized F287–F294 и S026/S063/S075.

evaluation/OPEN_QUESTIONS.md и релевантные human sections: annotation/lineage/unknown и source-hour vs wall-hour, delivery close, request/completion placement. Их E предлагаются, не выполнены на настоящем приложении. Указанные F229–F234 корректируют ранние общие рекомендации: для semantic-false/source-hour достаточно полного журнала и review всех доставок с контекстом; recall требует иного основания.

## Пределы

Нет полного кейса, issued LinQ API/SDK/device grant, принятого witness, camera/test labels или результатов нашей модели. Закрытая документация не обходилась и прочитанной не называется. Не найдены в этой ветке просмотренные защиты LinQ-победителей с таймкодами доказательства. Имеющиеся аналоги W1C не подтверждают точный способ hardware proof; они пригодны для постановки вопросов.
