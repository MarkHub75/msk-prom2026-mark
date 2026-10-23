# W2-B — оригинальный guide, швы примера и граница source/version

Назначение: K003, K002, K020. Исследование 23.10.2026 04:49–04:55 MSK (01:49–01:55 UTC); исторический контекст подготовки сохранён. SDK, учётные данные и LinQ не получены; установки пакетов, компиляции и исполнения модели нет. Прочитаны W2_B_PROMPT, исходный research prompt, замечания критика и релевантные W1-03/W1-05/source snapshots. PDF skill применён к попыткам чтения, авторинга PDF нет.

## Решение

**Нельзя пока начинать с объявленного официальным runnable `end_to_end.py`: публичный matching source не найден, binary guide не получен, версия его зависимостей не установлена.** Можно использовать guide как карту стадий и подготовить пакет вопросов к его авторам. Не следует переписывать пропущенный compile call, менять `onnx_direct` на сторонний конвертер или чинить proprietary return types по догадке.

Содержательное изменение относительно W1: **опровергнут возможный вывод, что `tf.graph_util.import_graph_def` сам по себе является отсутствующим TF2 API или что присваивание его результата в `graph` немедленно ломает Session.** В проверенном официальном TF2.14.1 этот экспорт существует; возвращаемый `None` допустим для Session и означает default graph. Реальная условная проблема — согласование default import namespace с feed/fetch names и изоляция повторных импортов. Это статическое доказательство по upstream исходникам, не тест с SDK и не установление используемой LinQ версии TensorFlow.

K003 остаётся открыт, но область подозреваемых дефектов уточнена. K002: нового согласованного delivery manifest нет. K020: ниже дан один решающий эксперимент и альтернативный старт без обязательного vendor Model Zoo.

## Факты и источники

| ID | Факт и решение | Тип основания / actual test |
|---|---|---|
| W2-B-F01 | CLI binary retrieval guide/presentation по HTTPS завершился TLS EOF; HTTP guide — remote disconnect; `curl.exe` с принудительным TLS1.2 — handshake failure. Оригинальных PDF bytes и их checksum нет. | actual network observations, S01/S02/S07; не отсутствие PDF |
| W2-B-F02 | web screenshot guide p11 отказал: content type не application/pdf; ссылку или вызов screenshot не считать просмотром. | tool failure, S01; visual verification отсутствует |
| W2-B-F03 | TinyFish live browser run сообщил, что PDF виден и имеет28 страниц; повторил converter tuple p11 и single assignment p19. Ответ содержит только текст, ни image block, ни PNG, ни screenshot URL. Это новая удалённая заявка browser agent, но не просмотр страниц исследователем. Число28 не разрешает конфликт W1 `27` vs титул `Листов28`. | reported remote observation S06; no actual screenshot seen |
| W2-B-F04 | Старый URL `hi-tech.org/...rukovodstvo-polzovatelya.pdf` реально отвечает200, но `Content-Type: text/html`, 29101 bytes; web показывает главную ООО «Хайтэк-Интеграция», ИНН7722350688. Он не дал PDF и не является source guide для сверки. | downloaded HTTP headers + web HTML, S03; новый точный отрицательный результат |
| W2-B-F05 | TF v2.14.1 экспортирует `graph_util.import_graph_def` и `import_graph_def`; функция импортирует в текущий default Graph, по умолчанию добавляет scope import, а без return_elements возвращает None. Она не является фабрикой нового tf.Graph. | official upstream source S04, importer.py354–411,485–493,549–552; static only |
| W2-B-F06 | TF v2.14.1 Session при graph=None использует ops.get_default_graph(); следовательно строка guide-text не доказывает TypeError от Session. Default import prefix может привести к несоответствию имён; повторный импорт — к новому scope/старым nodes. Нужен минимальный прогон в matching среде, а не исправление от имени LinQ. | official upstream source S05 session.py662–668 + S04; conditional inference, не выполнено |
| W2-B-F07 | ONNX v1.15.0 экспортирует ModelProto; load_model возвращает этот тип, load является alias load_model. В этом source нет ModeProto. Это подтверждает подозрительность literal, но не доказывает наличие опечатки на исходной странице PDF. | official upstream source S08, __init__.py38,92,176–180, конец файла; static only |
| W2-B-F08 | Pinned third-party ResNet builder явно допускает tuple/single converter, преобразует tf.Graph через as_graph_def, затем использует RegularModel/calibrate/quantize и распаковывает Network result. Эти защитные ветки не доказывают, что обе формы когда-либо были поддержаны одним SDK; sample не matching официальный end-to-end. | S09 source_code, actual network read + W1 saved source; не execution |
| W2-B-F09 | Целевые web поиски по end_to_end.py+tpu_framework/IVA/LinQ, onnx_to_tf+tpu_framework/128x128, точному designation и Framework_manual_H1 не дали релевантного официального source archive/errata. Broad onnx_direct выдаёт одноимённый LocalAI и исключён. | actual targeted search; не утверждение, что source не существует |

### Реестр источников с точными локаторами

- **W2-B-S01:** ООО «ХайТэк», «Фреймворк IVA H1. Руководство оператора»,2025, RU.РМДВ.04.06.014-03 34 01, https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf . W2 direct access04:49–04:54MSK не дал binary; reusable W1 text `_WORK/W1_03/Framework_manual_H1_extracted.txt`. Страницы далее — печатные markers extraction, не проверенные PDF indices. Номер документа -03 не package version.
- **W2-B-S02:** ООО «ХайТэк», презентация2026, https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf . Requests access04:50:53MSK — TLS EOF; p6 logos не просмотрены, не извлекать OS install matrix из старого текста.
- **W2-B-S03:** https://hi-tech.org/solutions/sol/frejmvork-fw-tpu-h-rukovodstvo-polzovatelya.pdf ; actual requests04:50:53MSK, HTTP200 text/html; title «Российский системный интегратор „Хайтэк-Интеграция“». Это текущий HTML response старого locator, не новая редакция PDF.
- **W2-B-S04:** The TensorFlow Authors, official source tag **v2.14.1**, https://raw.githubusercontent.com/tensorflow/tensorflow/v2.14.1/tensorflow/python/framework/importer.py . Download01:51:51UTC,23137bytes, SHA256 `0290f8813bc0d0d4b651957c0e7af17c113b959a4b541d24a7584c4f63338f76`; `_WORK/W2_B/TF_2_14_1_IMPORTER.py`. Version chosen as explicit historical upstream comparison, **not established LinQ dependency**.
- **W2-B-S05:** The TensorFlow Authors, v2.14.1, https://raw.githubusercontent.com/tensorflow/tensorflow/v2.14.1/tensorflow/python/client/session.py ; downloaded around04:52MSK; exact timestamp/hash in `_WORK/W2_B/PRIMARY_SOURCE_MANIFEST.json`, local `TF_2_14_1_SESSION.py`.
- **W2-B-S06:** TinyFish run `f6382bd0-39bf-42b3-b341-fac6cb25677d`, https://agent.tinyfish.ai/runs/f6382bd0-39bf-42b3-b341-fac6cb25677d ;04:51–04:54MSK,120s,9steps, completed. Raw reply `_WORK/W2_B/REMOTE_BROWSER_RESULT.json`. Requested screenshots pp11/19/20; none returned. Its discussion of missing assignment incorrectly focused on `compiler = ...` rather than `tlm_program = compiler.compile_(...)`; **do not use its negative conclusion as proof that the seam is absent**.
- **W2-B-S07:** `_WORK/W2_B/DOWNLOAD_ATTEMPTS.json`, exact UTC times/URLs/status/headers, no usable binary. Curl TLS1.2 and web failures described F01/F02.
- **W2-B-S08:** ONNX Project Contributors, official tag **v1.15.0**, https://raw.githubusercontent.com/onnx/onnx/v1.15.0/onnx/__init__.py ; downloaded01:51:52UTC,11579bytes, SHA256 `bbfc456c210c654fe22eb69950f82a51741bb6c5b7c6a2375a71d25cac5960a0`; `_WORK/W2_B/ONNX_1_15_0_INIT.py`. Explicit upstream comparison, not dependency pin for guide.
- **W2-B-S09:** sher stpasha / `sherstpasha`, linq-cv-bench, commit **3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140**, https://raw.githubusercontent.com/sherstpasha/linq-cv-bench/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/classification/build_resnet50_program.py ; network read04:53MSK, load_converted_graph/to_graph_def/map_tensor_name/RegularModel/compile sections; reusable source `_WORK/W1_06/linq-cv-bench/scr/classification/build_resnet50_program.py`. Авторство user handle, не LinQ vendor. Source version pinned, SDK version не установлен этим файлом.

## Source-preserving errata: literal → канал → установленный смысл → неизвестное

Ни одна строка таблицы не выдаёт реконструкцию за официальный runnable code. Сохраняем canonical text W1 без редактирования.

| Локатор / literal | Канал | Что подтверждено / опровержение | Что нужно получить |
|---|---|---|---|
| p7 signature64x64_fpga vs prose128x128_asic | W1 text only | В одном extraction два defaults. Ни один не выбран. | original p7 + actual as_graph signature/target matching release |
| p11 converter Tuple[Graph,dict]; p19 один original_graph_def | W1 text + remote reported observation | Расхождение воспроизводится в отчёте browser agent; actual image не получен. TF importer source не принимает tuple как GraphDef. | installed converter source/signature и фактический returned object, name mapping, matching source example |
| p14 onnx.ModeProto | W1 text only + ONNX upstream | Тип отсутствует в проверенном official ONNX1.15.0. Это условный host-level seam, не установленная ошибка original PDF. | visual p14 и actual dependency version; не править чужой source молча |
| p12 leading space в input:1; p17 helper удаляет только :0 | W1 text only | :1 может быть легальным tensor port TF; нельзя автоматически менять на :0. Helper не преобразует этот literal в OP name. Ведущий пробел может быть extraction loss. | exact names ONNX/converted graph/.tpu metadata, p12/17 screenshots |
| p14 graph=tf.graph_util.import_graph_def(...) | text + official TF source | Сам namespace **подтверждён**, прежняя гипотеза отсутствующего API опровергнута для TF2.14.1. None return + Session разрешены. | actual namespace/scope/graph isolation на supplied TF; parity до quantization |
| p19–20 Network → tlm_program use без assignment | W1 text only; remote отрицание нерелевантно | В extraction нет defining compile call. Не объявляем original bug. Formal p9 допускает compile_, но не даёт основания подставить kwargs/Network return из другого release. | полный end_to_end.py и compiler.compile_ того же release; page20 image |
| p14 return test-input dict без def; p16 batch_size=1 без comma; p17 SUFFIX/_SUFFIX, test_input_dict.item, TLM context | W1 text only | Дополнительные признаки фрагментации примера. Переносы/вырезанные определения не отделены от source ошибок. | full source, imports, helper definitions и indentation; p13–17 images |

**Версионная граница.** Guide2025 -03, benchmark Framework2026.8.43/Runtime16.18.6, public pytpu15.0.24, third-party source commit и TF2.14.1 — пять разных provenance/version axes. Их нельзя соединить в installation recipe. Даже формально успешный import Framework не докажет converter compatibility, правильный target или runtime ABI.

## Точный запрос поставщику вместо выдуманного скрипта

Один архив/commit для фактически выданной среды: неизменённый `end_to_end.py` (или актуальный replacement), все его imports/helpers, model weights/ONNX checksum и exporter metadata, одно calibration/test image с ожидаемыми full outputs, preprocessing и class-index convention, exact package/native/driver/firmware manifest, compiler target. Отдельно показать фактический converter return и mapping names/layout; Network.from_quantized_model return; defining compile call и его result; expected .qm/.tpu hashes либо объяснение недетерминированных полей; доступность TLM и границы численной точности.

Если source не распространяется, достаточно versioned API reference + поддержанного минимального custom example, который реально можно запустить в supplied environment; попросить автора показать именно эти пропуски. Не требуется выдумывать `compiler = ...`: речь о присваивании результата компиляции переменной, которую далее распаковывает TpuProgram.

## Один решающий эксперимент для K020

**E-B01; владелец — один инженер интеграции/importer**, другие инженеры потребляют сохранённый manifest/golden tensor, не дублируют inventory. Сейчас можно проверить upstream source semantics и статические имена; решающий experiment требует supplied SDK. LinQ для стадии converter не предполагается обязательным, но CPU-only поддержка supplied release должна быть установлена из его delivery docs.

Prerequisites: exact SDK/dependency manifest, поддержанный converter или иной frontend, неизменённая маленькая модель (vendor или custom), один canonical preprocessed tensor/hash, исходные float outputs с dtype/shape/name metadata. Запустить только source→frontend conversion→float reference, вывести реальные type(return), module/file/version, mapping и full I/O names. Сравнить все значения выхода с заранее объявленной tolerance; сохранять исходный exception и stage при failure, без broad fallback на другой converter.

Success: frontend создаёт согласованный graph/I/O и parity на canonical input. Это разрешает перейти к quantization/compile; **не доказывает quant quality, ISA target, .tpu correctness, device inference или производительность**. Альтернатива: unsupported source/API/type/name mismatch → минимальный reproducer и вопрос автору, не тратить45ч на догадочную замену APIs. Если доступ только service-only, E-B01 выполняет поставщик либо применяется документированный upload path с теми же hashes/I/O.

**Попытка опровержения обязательности vendor smoke:** Model Zoo/готовый ResNet не является логически обязательным gate. При наличии compiler+supported custom example можно начать с собственного минимального supported graph и независимых golden outputs. Он должен пройти frontend→quant/compile→runtime и подтверждение device execution; это меньше доказывает о сложной детекторной модели, но даёт проверяемый старт. TLM полезен при наличии и версии; его отсутствие не делает реальный device smoke невозможным. Владельцы compiler/runtime/device evidence назначаются root отдельно.

## Остаток и handoff

Не закрыты visual p7/11–14/17/19–21 и presentation p6; оригинальные PDF metadata/page count/hash; version-matched official end_to_end source, onnx_direct source/return и missing compile assignment. Пути закрытия — законно полученный binary от поставщика/доступный primary mirror, затем render и реальный просмотр PNG; source archive matching delivery. Не просить заново один и тот же текстовый extraction.

Root: убрать категорический «tf.graph_util API invalid» и «Session(None) crashes», сохранить условный namespace seam. Не повышать TinyFish plain-text report до visual proof, даже при формулировке renders successfully. Отсутствие SDK не мешало точному upstream опровержению, но всё proprietary остаётся узким unknown. Нового работающего примера, install matrix или LinQ execution результата эта ветка не установила.
