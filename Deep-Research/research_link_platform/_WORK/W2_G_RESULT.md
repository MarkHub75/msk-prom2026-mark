# W2-G — `.tpu`, Python/native boundary и tensor contract

Назначение: K009, K012, K002. Исторический контекст — ночь 23 октября 2026, пять инженеров, 45 часов хакатона. Фактические новые обращения — 2026-10-23 примерно 01:58–02:04 UTC / 04:58–05:04 MSK; точные timestamps HTTP и host probe сохранены в `W2_G/HTTP_LOG.json`, `SUBTREE_FETCH.json`, `HOST_PROBE_RESULT.json`. Прочитаны исходное задание, релевантные разделы CRITIC, W1-09/12/15, W2-F, состояние доступа и actual исходники pytpu15.0.24. SDK/device access не выдан. Ни чужая native library, ни compiler, ни hardware inference не запускались. Выполнен узкий Python-only probe старых методов с fake native объектом и запретом CDLL.

## Решение

**Современный schema/ABI contract не получен; безопасно специфицировать адаптер по старому коду нельзя.** Свежий PyPI JSON и simple index всё ещё ведут к `pytpu15.0.24`, upload2023-11-27. Поиск current headers/source и alternate fetch старого Git-host не дали новой native реализации. Это не означает отсутствия современной поставки у производителя и не доказывает её несовместимость с guide2025. K002/K009/K012 остаются точными вопросами к выдаваемому release.

Есть полезное изменение W1: **даже для исторического binding нельзя утверждать dangling outputs только из отсутствия `.copy()`**. Actual реализация создаёт Python-owned bytearray, numpy возвращает view, а base chain в проверенной CPython3.11.9/NumPy2.4.2 среде удерживает ctypes pointer и backing storage после уничтожения локального ctx. Также Mapping и unknown-name проверки существуют. Вместе с тем host probe подтверждает, что старый Python путь не отвергает wrong dtype/noncontiguous/missing input, а exception внутри `Device.open` пропускает explicit native destroy. Все эти выводы строго ограничены15.0.24 и mock execution; это не найденные ошибки Runtime16.18.6.

Вторая существенная граница: **формат RAW и `ProcessingMode.RAW` независимы**. Более того, в15.0.24 mode влияет только на аргумент native run; Python allocation/reshape выбирается по `_program._is_raw`. Нельзя обещать корректный RAW путь одним переключением enum для произвольной обычной `.tpu`. Нужны documented native semantics и golden user/raw buffers.

## Источники, версии и способы доступа

| ID | Источник, автор, дата и locator | Реальная проверка / локальный снимок |
|---|---|---|
| W2-G-S01 | [PyPI pytpu JSON](https://pypi.org/pypi/pytpu/json), publisher/metadata IVA-Tech, maintainer IvaTechnologies; current release15.0.24, upload2023-11-27T09:41:37.939987Z. `info.version`, `releases`, `urls`, `project_urls`. [Simple index](https://pypi.org/simple/pytpu/). | Fresh HTTPS200 обоих endpoints 02:01:27UTC. `W2_G/PYPI_CURRENT.json`, `PYPI_SIMPLE.html`, hashes в HTTP_LOG. Web project page тоже прочитана; её README относится к другому поколению `iva_tpu`, а не authoritative Device API. |
| W2-G-S02 | [pytpu15.0.24 sdist](https://files.pythonhosted.org/packages/bd/9a/ee7cc0a40291dcb7ef399d30b80892909c3add5e3a0ebf1bc04a8c97f0ba/pytpu-15.0.24.tar.gz), IVA-Tech, 2023. SHA256 `e63ec3c5011de2dc660adcfd321227e41006aac7d8382e330d4667e8356eb27f`. | Reuse W1 actual bytes/source; fresh S01 по-прежнему публикует этот artifact. `_WORK/W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu/_bindings.py`. SHA256 отдельных Python files и AST method spans в `W2_G/SOURCE_LOCATORS.json`. Ни binary runtime, ни modern header в архиве нет. |
| W2-G-S03 | Тот же sdist, `pytpu/_converter_to_raw.py`, `Codec.encode/decode`35–40, schema extraction76–104, conversion107–141. | Actual source inspected; это первичный код поставщика исторического пакета, не восстановленный из README. Dependencies `tpu_tlm_is` не получены/не импортировались. |
| W2-G-S04 | [MLCommons IVATech source2020](https://github.com/mlcommons/inference_results_v0.7/tree/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech), pinned commit `89260c7a0bb2bb86f4adaf1d88e0307162eb602b`; source header mmoroz, 2020. `code/resnet/v1/util.h`, README, SUT. | Fresh GitHub API tree и raw util/README200. Broad tree был `truncated:true`, поэтому отдельно fetched `closed/IVATech` subtree с `truncated:false`; `MLPERF_SUBTREE.json`. `MLPERF_UTIL.h`, `MLPERF_README.md`, saved W1_15/MLPERF_SUT.txt. Native `<tpu.h>` импортируется, но самого tpu.h в этой complete subtree нет; `.tpu` binary в subtree нет. |
| W2-G-S05 | [linq-cv-bench pinned tree](https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140?recursive=1), sherstpasha, commit2026-04-03 `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`. | Fresh API200, complete `truncated:false` tree. No `.tpu`, `.h`, `.hpp`, `.zip` file paths. Это ограниченное наблюдение этого commit; repo — third-party, не SDK reference. |
| W2-G-S06 | [Framework manual H1](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), официальный guide2025, RU.РМДВ.04.06.014-03 34 01, §3.4 printed20–21. | Reuse W1 extracted text/результаты, повторно PDF не обрабатывался и новая visual проверка не заявляется. Документ подтверждает `.tpu`→Device/load/inference/sync и float input пример; не раскрывает native processing placement/формулы. |
| W2-G-S07 | [legacy package homepage](http://git.mmp.iva-tech.ru/tpu_sw/iva_tpu_sdk), publisher metadata locator; HTTPS alternative. [LinQ docs](https://lin-q.ru/docs). | Web open inaccessible; native urllib HTTP/HTTPS старого host — DNS failure, docs — TLS EOF. Fresh logs сохранены. Это transport/access failures, не содержание репозитория и не доказательство закрытости docs. W2-A отдельным TinyFish каналом получил docs navigation, новых runtime download links не передал. |
| W2-G-S08 | [PyPI tpu-tlm-is JSON](https://pypi.org/pypi/tpu-tlm-is/json), exact debug dependency name из исторического кода. | HTTPS404. `EXTRA_FETCH.json`. Это отсутствие endpoint данного project name в данной проверке, не доказательство отсутствия внутреннего пакета или codec в SDK. |
| W2-G-S09 | `W2_G/HOST_PROBE.py`, автор этой ветки, 2026-10-23; `HOST_PROBE_RESULT.json`, UTC02:02:24.533122. | Actual local helper probe CPython3.11.9, NumPy2.4.2, Windows host. Before source execution ctypes.CDLL replaced by function raising AssertionError; lazy source не загружал binary. Все native method accesses заменены Fake; только чтение/запись собственных host буферов. Никакой `.tpu`/device не нужен и не тестировался. |

## Факты с границами применимости

### W2-G-F01 — современная версия не восстановлена

Тип `primary_metadata` + `network_observation`; S01/S07/S08. Current PyPI project release —15.0.24. Внешний runtime16.18.6 из benchmark2026 не обязан совпадать с version Python distribution, поэтому разницу чисел нельзя выдавать за incompatibility или устаревание API. Не получены current `METADATA`, binding source, C headers, SONAME, driver/firmware version matrix, serialized model format version или sample metadata. Это искомые missing fields, а не неизвестные названия методов, которые следует угадывать. S01 public Python source не восстанавливает native ABI.

### W2-G-F02 — Python видит user/raw representation, но не реализует numerical codec

Тип `source_code`, S02, `Program.__init__`273–291, `_load_inference`427–457, `_get_inference`460–484. Native `tpu_get_program_info` возвращает JSON; Python читает `inputs['1']`, `outputs['2']`, `hardware_parameters`. Для ordinary program output interpreted as `user_dtype`, reshaped to `user_shape`; для raw program — uint8 array reshape `(-1,ddr_word_len)`. `_convert_from_uint8_to_user_dtype`487–495 — views, а не quantization/dequantization arithmetic. Он поддерживает dtype string containing `int`, float16 и float32; это не полная type capability matrix TPU. Pointer type `uint8*` — байтовый transport, не доказательство int8 semantic input.

Source size lookups: `tpu_get_input_size(program,index,is_raw)`, `tpu_get_output_size(...)`. Единицы в usage выглядят как bytes: выход выделен bytearray длиной tensor_size, затем dtype view. **Current native contract размера/выравнивания не документирован**; это вывод из исторического usage, а не универсальное соглашение. В Python input `tensor_size` вычислен, но не используется для проверки nbytes.

### W2-G-F03 — available historical schema шире W1 summary

Тип `source_code`, S03 `_get_tensor_description`76–104. Для user tensor reader требует именно:

| Поле | Реальное использование старым converter | Что остаётся неизвестным |
|---|---|---|
| `address`, `size` | `_to_raw_old` оставляет только эти два поля per tensor | Units/address space/alignment/limits/current schema version |
| `user_shape`, `padding` | Из padding pairs и user dimensions строится boolean shape mask | Validity отрицательных padding/current convention, dynamic dimension support |
| `user_order`, `tpu_order` | Передаются в TensorDescription | Значения/axis mapping для actual compiled model; layout нельзя вывести из имени модели |
| `user_dtype`, `tpu_dtype` | Lookup через отдельные STR_TO_* enums | Exact enum table и supported combinations отсутствующего tpu_tlm_is/current SDK |
| `tpu_shape` | Передаётся в TensorDescription | Packing/strides/block layout actual target |
| `scales` | Каждое значение преобразуется float, затем tuple | Direction multiplication/division, scalar/per-axis scope, rounding/saturation и relation к quantizer thresholds |
| `anchor` | Передаётся в TensorDescription | Значение и семантика именно tensor codec. Нельзя отождествлять с YOLO detection anchors |
| `hardware_parameters.cache_word_len`, `ddr_word_len` | Выбор historical target codec | Current accepted targets/format version |

Historical `_get_tpu_parameters` знает ровно пары cache/ddr:128/32→`128x128`,64/16→`64x64`,64/64→`64x64_fpga`; другие пары → NotImplementedError. Это ограничение debug converter15.0.24, не support matrix современных ускорителей.

`Codec.encode` вызывает `tpu_tlm_is.models.iotools.tpu_encode`, `decode` — `tpu_decode`. Actual numerical implementation отсутствует, поэтому перечисленных metadata fields недостаточно для самостоятельной правильной реализации packing/scales. Наличие Python-callable codec подтверждает отдельную host-side debug conversion в этой старой библиотеке; **оно не устанавливает размещение native FULL преобразований**.

### W2-G-F04 — FULL/RAW enum не определяет Python buffer schema

Тип `source_code`, S02 enums165–169, `Inference.__init__`336–371, `_run`373–382, `sync`387–416, raw heuristic498–518. Enum values `RAW=0`, `PRE_PROCESS=1`, `POST_PROCESS=2`, `FULL=3`; `_run` передаёт `mode.value` в `tpu_run_inference`. Код не раскрывает реализацию этих стадий или location host/device. Названия и битовый вид значений не дают права самостоятельно описать stage semantics.

Размеры `_tensor_name_to_tensor_size` вычисляются в init по `_program._is_raw`, а output decoding также проверяет `_is_raw`, **не mode**. `_is_raw_program` открывает ZIP member `metadata.json`; `_is_raw_metadata` берёт первый output region/первый tensor и проверяет отсутствие `user_dtype`, предполагая отсутствие mixed tensors. Этот heuristic не versioned schema validator.

Конвертер создаёт новую ZIP-программу с сокращённой metadata, одновременно заранее сохраняя descriptions в Codec. Поэтому file RAW — отдельное преобразование artifact/metadata, mode RAW — runtime argument. Из source нельзя заключить, что ordinary `.tpu` + `mode=RAW` автоматически выдаст корректные raw tensors через этот Python wrapper. Не доказано и обратное: native может иметь дополнительные соглашения, которых здесь нет. Нужен current reference с supported combinations program format × mode × buffer representation.

### W2-G-F05 — validation concern сужен, не снят

Тип `source_code` + `local_helper_test`; S02 `_load_inference`427–457, S09. Реально отвергается non-Mapping (`ValueError`), неизвестное имя вызывает KeyError. `_run` проверяет native return, `_check_status` — status. Поэтому тезис «вообще нет validation» неверен.

Host fake probe: float64 вместо ожидаемого float32, C-noncontiguous slice и empty input Mapping приняты Python методом без exception до fake registration. Source не проверяет exact input name set, dtype, shape, C-contiguity или nbytes. Input index mapping объединяет inputs и outputs; совпадающие имена могут перезаписать index. Это статический возможный corner case данной реализации, **не утверждение, что compiler допускает такие имена**. Native может дополнительно проверять данные, но raw pointer не несёт numpy shape/strides/dtype; current safeguards и фактическое native failure behaviour не проверены. Не подавать malformed buffers на неизвестную native library ради этого исследования.

### W2-G-F06 — output view и ownership: copy claim опровергнут, dangling claim не подтверждён

Тип `source_code` + `local_helper_test`, S02/S09. Historical comment говорит о copy, но actual output path: `bytearray(np.empty(...uint8))` → ctypes `from_buffer` → cast pointer → `np.ctypeslib.as_array` → dtype `.view` → reshape. Это numpy view, `OWNDATA=False`; probe менял float через pointer, и изменение видно в возвращённом array. Комментарий нельзя цитировать как доказательство output copy.

При этом probe удалил local ctx/pointer, вызвал gc и получил сохранённые `[1.25,-2.5]`; weakref показывает original pointer still alive. Array base chain `ndarray→ndarray→memoryview` удерживает buffer ownership в проверенной среде. Отсутствие `.copy()` само по себе не доказывает use-after-free. Результат не гарантирует совместимость других Python/NumPy releases, поведение native destructor или lifetime современной версии. Выходного native buffer после destroy здесь не читали: вся память создана Python. Вопрос current API «сохраняется ли array после следующего inference/session close» остаётся к документации и actual SDK test.

### W2-G-F07 — cleanup concern исторически конкретен, modern repair неизвестен

Тип `source_code` + `local_helper_test`; S02 `Device.open`185–199, `Device.load`235–253, `Program.inference`307–312, `buffer`315–322; S09. В generators explicit destroy стоит после yield без try/finally. В mock `Device.open` normal exit вызвал destroy, injected exception — не вызвал. ExitStack вокруг `sync` не исправляет отсутствие finally внутри entered context generators. Это реальное свойство control flow15.0.24, не аппаратное измерение leak и не current SDK diagnosis.

В `Program.buffer` TODO предупреждает о нестабильности тестов, **но actual `tpu_destroy_tensor_buffer_object` включён и вызывается на normal exit**. Нельзя писать «буфер никогда не уничтожается» или считать текст2023 доказательством нынешнего crash. В этой ветке не получены modern source/release notes, опровергающие или подтверждающие сохранение проблемы. Отсутствие исправления в публичном legacy архиве не значит отсутствия исправления в current release.

### W2-G-F08 — исторический C++ пример не задаёт современный ABI

Тип `source_code`, S04. `util.h` включает внешний `<tpu.h>` и использует shared_ptr для TPUDevice/TPUProgram; SUT вызывает старое семейство `tpu_program_get_input_buffer`, `tpu_inference_submit`, `tpu_inference_wait`. Это уже другое API family относительно ctypes `tpu_create_*`, `tpu_run_inference`. Source даёт пример lifetime/execution flow соответствующей версии2020, но не typedef definitions, ownership contract современного `<tpu.h>` или ABI stability promise. Совпадающий vendor lineage не разрешает смешивать старые declarations с новой `.so`.

## Versioned API/schema comparison

| Область | Historical C++2020 | Actual pytpu15.0.24 source2023 | Official guide2025 | Current Runtime16.18.6 / выдача2026 |
|---|---|---|---|---|
| API family | `TPUDevice/TPUProgram`, external tpu.h, submit/wait | Device/Program/Inference; create/run/status ctypes | Device.open/load/inference/sync | Header/source not obtained; Python package version unknown |
| Model format | `.tpu` name, compile script | ZIP, metadata.json heuristic | Framework compiled `.tpu` boundary | Format version/compatibility not obtained |
| Schema | No schema specification in harness | inputs region1/outputs region2 + user/tpu fields, hardware params | Named input/output examples | Actual sample JSON absent |
| Processing | Old harness copies sample buffer and reads typed outputs | enum passed native; Python format handling separate | Float prepared input supplied | Numerical transformations/placement unknown |
| Lifecycle | shared_ptr usage; external ownership semantics | host allocations/views and generators above | with-style usage | Repair/exception guarantees not established |

Таблица — различие доказательств, **не compatibility matrix**. Guide2025 не объявлен obsolete. Закрыть diff можно только matching current source/reference, а не сопоставлением version numbers разных компонентов.

## Отрицательные попытки и противоречия

Новые web запросы: exact `pytpu ProcessingMode`, `libtpu.2.so header`, `tpu_get_program_info`, `tpu_set_user_tensor_buffer_ptr`, `pytpu 16.18`, `tpu_framework metadata.json user_dtype`, `pytpu user_shape`, `tpu_run_inference ProcessingMode`, `iva_tpu_sdk header`, `tpu_process_tensor_buffers`, `tpu-tlm-is scales`, `linq 16.18.6`, domain LinQ runtime/SDK/C API. Current authoritative headers/source/schema не обнаружены. Часть queries дала unrelated Google TPU/.NET LINQ/TLM результаты; они не включены как evidence. Search absence не доказывает product absence.

Альтернативы к web failures действительно испытаны: urllib PyPI JSON/simple успешны; старый Git-host HTTP/HTTPS DNS fail; official docs urllib TLS fail; GitHub raw/API успешны. Complete modern third-party repo tree и complete historical IVATech subtree проверены на sample `.tpu`/native headers. Broad MLPerf tree изначально truncated и заменён targeted complete subtree; поэтому нельзя экстраполировать отсутствие файла на весь repository.

Уточнены три противоречия: README против actual API → приоритет versioned source; output comment copy против actual view → приоритет actual operations+probe; TODO unstable buffer destroy против actual enabled destroy → TODO не является current defect. None из них не заменяет native validation.

## Checklist адаптера после получения actual metadata

Это проектная проверка, не готовый generic parser. Один runtime owner получает manifest среды и versioned reference; один model owner даёт canonical input tensor и model lineage. Не создавать конкурирующие manifests.

1. Сохранить exact Python distributions/METADATA, path/source hash binding, native library version/SONAME/hash, matching header/docs и driver/firmware. Получить supported pairing с compiler/target `.tpu`. Не грузить найденную `.so` старым ctypes наугад.
2. Сохранить byte hash `.tpu` и schema/format version официальным reader либо безопасным ZIP inspection, **если actual формат действительно ZIP**. Записать все реальные top-level keys/regions, I/O order/names и hardware_parameters без silent defaults. Не hardcode regions1/2 и raw heuristic из15.0.24, пока current release не подтвердит.
3. На ordinary user I/O проверить exact key set, ordered mapping по current reference, shape, dtype/endian, expected byte count и C-contiguity/strides. C-contiguous conversion выполнять явно с recording; semantic NHWC/NCHW отдельно определяется user_order/reference, contiguity её не исправляет. Raw buffers проверяются по documented packed byte contract, не по product(user_shape) и не простым int8 cast.
4. Сопоставить actual user/tpu metadata: поля из F03 — **кандидаты чтения при их наличии**, не обязательные modern names. Запросить semantic definitions scales/anchor/padding/order; отсутствие field не восполнять guessed scale1. Разделить image normalization/letterbox до runtime, user↔device conversion runtime и detector decode/NMS после outputs.
5. Зафиксировать input lifetime: ownership/copy vs borrow, retention до sync return или async completion, allowed concurrent mutation, output ownership после next run/close. Для foreign-owned outputs current documented copy boundary может быть нужен; legacy отсутствие copy само по себе не повод констатировать defect. При временном defensive copy измерить её стоимость отдельно.
6. Documented exceptions/timeouts/reuse: что остаётся valid после native error, может ли close повторяться, thread safety, session sharing; tests только valid buffers и vendor-supported failure injection. Не лечить legacy cleanup добавлением произвольных duplicate destroys.

## Конкретные следующие эксперименты и разрешение unknown

**E-G1: metadata/ABI capture (SDK нужен; hardware не обязательно, зависит от reader).** Vendor supplies one matching release bundle, sample `.tpu`, expected user/raw I/O and current Python+C API docs. Сохранить files/hash/version и actual metadata. Если metadata доступны только через device.load, перенести этот шаг в выдаваемую LinQ среду. Success: схема и sizes/dtypes/layout привязаны к одному artifact и native ABI; не доказаны correctness/performance.

**E-G2: user/raw numerical parity (SDK+LinQ, совместно W2-F).** Один shared golden float input; runtime FULL(user). Только через supported encoder получить raw input; сравнить documented RAW+postprocess эквивалент с FULL. Сохранить before/after packed arrays, hashes, shapes/scales и error metrics; quantization rounding делает bitwise float equality необоснованным без vendor tolerance. Варьировать mode лишь в documented allowed combinations. Сравнение с quantized TF/reference требует его собственного rescale; не переносить старый helper formula в FULL. Success localizes adapter math для этой модели/release, но не размещение FULL stages.

**E-G3: output ownership/repeated-call (actual SDK+LinQ).** На valid vendor sample сохранить первый returned output, выполнить следующий sync с иным valid input, закрыть session/program по current instructions, gc и сравнить первый output/hash. Где API предоставляет borrow semantics — сначала сделать documented copy, и это будет другой тест. Отдельный disposable own process и ограниченный повтор для RSS/native resource trends; рост RSS не равен автоматически leak из-за allocator/cache. Exception tests — vendor-supported error path, без out-of-bounds buffers/отключения shared device. Success сужает lifecycle concern ровно к проверенному release/path.

**E-G4: stage placement (native reference/profiler/compiler report; совместно W2-J).** Vendor объясняет, какие conversions/compiled host instructions входят в pre/post/FULL, где выполняются packing/transpose/scaling и что включено в timings. Если `.tpu` содержит host processing program, запросить его format/coverage; сейчас это правдоподобная гипотеза, не установленный факт. До подтверждения не называть host pre/post CPU fallback или TPU processing. Numerical parity не доказывает graph coverage/physical execution.

Точный запрос поставщику: matching current pytpu/libtpu/header versions; `.tpu` format/schema version и forward/backward compatibility; one actual Program.info JSON; user/raw byte size, alignment, order/packing/scales semantics; FULL/RAW matrix и stage placement; input/output borrow/copy lifetime; cleanup/error recovery/thread safety; known-good .tpu + golden user/raw pairs. Endpoint/имена новых API не выдумываются.

## Передача root

Новое W2: output copy comment фактически неверен, но dangling-output inference опровергается host ownership probe в проверенной среде; Mapping и unknown-name validation существуют; narrow missing dtype/layout/name-set validation подтверждена только historical Python path. Exception destroy omission воспроизведён только с fake native15.0.24. RAW file heuristic и processing enum независимы, allocation/decoding зависят от format flag, поэтому enum не заменяет encoder. Сохранены реальные historical schema fields; их scales/packing formulas недоступны без tpu_tlm_is/native reference. Современный ABI/model sample не получены после fresh targeted поиска и alternate retrieval. Никаких современных runtime errors, SDK compile/device результатов или placement claims нет.
