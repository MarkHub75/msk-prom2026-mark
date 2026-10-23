# Условия синтеза для сборщика и авторских ролей

Это передача требований двух входных файлов, не выводы вместо исследователей. Сборщик и автор читают обе волны и CRITIC, а не опираются только на эти напоминания.

## Наблюдаемость и доказательства

- Первичные CASE_NOTES.md описывают личное визуальное чтение root всех20 страниц. Не превращать сообщение исследователей «прочитаны заметки root» в независимое чтение кейса. Оригинал сохранён INPUT/CASE_LINQ.pdf, hash проверен. Живой LinQ/SDK/веса/разметка отсутствуют.
- Во всех версиях отчёта различать документированный интерфейс, vendor claim, статический код, опубликованное измерение/bug reproduction автора, наше реальное локальное наблюдение, методический вывод, предлагаемый UNRUN эксперимент и UNKNOWN. Ни одна новая статья не становится нашим benchmark.
- Версии изученных источников не объявлять установленным стеком команды. Stable redirects сохранять как наблюдение web-сайта, не как самостоятельно доказанную дату release. Чужие linq_platform/cv_accuracy_vast эксперименты только со scope/topic/date.
- Сохранять общие методы и ограничения за пределами YOLO/ORT; 12general/3LinQ — распределение W1, не квота страниц/ссылок и не обещание измеренного effort.

## Практический протокол

1. Идентичность source checkpoint/config, частичная загрузка, eval/fusion, фактическое окружение; повторяемость baseline.
2. Immutable exact tensors и source-runtime outputs; ONNX-generated reference не заменяет source baseline. Независимый ground truth нужен отдельно.
3. Export preparation, FP32 unsimplified ONNX, alternate runtime same dtype, каждый graph pass, precision, calibration, compiler/target; сохранять first divergent stage. Если stage недоступен — UNAVAILABLE, не PASS.
4. Decode/NMS/geometry: схемы по task/version/nc/kpt_shape, output names/layout/units, objectness/logits/probabilities, ordering, padded output, dequantization exactly once. Custom class map не COCO heuristic.
5. Stress slices и before/after traces; freeze sampling/PTS/state reset/tracker/rules. Разделить raw tensor, raw detections, post-NMS, tracking и event/notification replay.
6. Quality gate: numerical repeatability/finite-mask/schema; matched boxes/keypoints/class/confidence; per-class/size/occlusion quality; tracking; своевременные события, missed/late/wrong actor/duplicate/false alerts, reviewable exposure и latency. Пороги — решение команды из риска/эталона, не универсальные 1%/1FPS.
7. Restoration order: preprocessing/schema mistake→export/pass rollback→effective calibration investigation→supported selective quantization/correction→QAT only after executable target path→alternative supported model with full re-evaluation. Выбор факторов зависит от first divergence, не всегда каждый шаг последовательно.

## Обязательные блоки внутри итоговых файлов

- Stage→symptom→root candidates→minimal diagnostic→remedy→remaining risk→evidence.
- Method→required access/data→actual compatible backend→reported/estimated/tested benefit→cost/risk→verification. Не обещать время QAT/VRAM/качество RTX3090 без измерений.
- Model family/checkpoint→export/output schema→quantization risks→LinQ evidence level→next test. Архитектура без exact checkpoint не готовый маршрут.
- Metric→unit/split→acceptance interpretation→cannot prove.
- Fidelity ladder: входы/наблюдения/диагностика/continue-or-rollback/пределы каждого этапа.
- Классификатор всех симптомов из тематического промпта: исчезновение, геометрия/зеркало, class map, score shifts, NMS, мелкие объекты, pose/event jitter, ONNX-parity/LinQ-fail, несопоставимые сравнения.
- Предлагаемый информативный golden pack: normal/hard/edge/regression, human/machine, zone crossings, falls, occlusions, scale/phone, light, empty/hard negative, short clips; происхождение/права/независимые splits. Количества — выбранный бюджет, не гарантия репрезентативности.
- 5–15 подробных E-ID (оптимально 10–12 содержательных, если покрывают): входы+access, exact baseline/target stage и sample IDs из будущего manifest, шаги без выдуманных API, outputs/logs/TPU proof, PASS/FAIL/INCONCLUSIVE/UNAVAILABLE, owner/decision/limitations; smoke, regression, end-to-end. ВСЕ UNRUN.
- TPU proof: immutable source→export→compiled lineage/coverage + runtime per-request completion/device identity; UI label/общая utilization не закрывают обе части. Объём допустимой CPU работы/secondary NN boundary выяснить у организаторов.
- Режимы полного SDK / ограниченного сервера / готовой модели или inference-service; какой уровень parity наблюдаем и какие выводы остаются недоступны.
- Доказательства для жюри: одни clips, raw predictions, ground truth/rules/metrics definitions, artifact versions/hashes, measured speed/latency, runtime evidence; реальные ограничения без фабрикации.
- Адресная передача соседним темам и приоритетные вопросы инженерам, без внешних сообщений.

## Финальная форма

Только шесть итоговых файлов из договора. Человеческий — глубокий связный русский текст, собственная логика глав, не 15 механических обзоров. Машинный — английский, YAML с обязательными answers/scope/not_covered/keywords/entity_schema/takeaways/checked_at+timezone/context_version/case+actual-check state/file pointers; каждый answers действительно раскрыт, UNK связан Q-ID. Якоря F/S/K/Q/E стабильны, относительные пути переносимы; внутренние turn-ссылки не использовать. Отдельной роли финального аудитора нет: аккуратность ссылок/фактов входит в работу сборщика/редактора/сжимателя.
