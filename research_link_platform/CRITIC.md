# Независимая критика первой волны LinQ и задания второй волны

Дата анализа: 23.10.2026, Europe/Moscow (UTC+03:00), после завершения всех 15 веток W1; локальные часы проверены в 04:43:57. Роль: отдельный критик со свежим контекстом, gpt-6.1-sol / high. Прочитаны целиком исходный `prompt-linq-platform.md`, `_WORK/PLAN.md`, `_WORK/RUN_STATE.md` и все `_WORK/W1_01_RESULT.md` … `_WORK/W1_15_RESULT.md`. Дополнительно прочитаны сохранённые первичные материалы, перечисленные ниже. Нового сетевого поиска и получения внешних доказательств критик не выполнял, субагентов не создавал.

Это исходная критика **до W2**. Статус всех K при передаче: `ожидает W2`, если явно не сказано, что достаточно корректной классификации уже имеющегося свидетельства. Позднее сборщик добавляет результаты обработки, F/S/Q/E-ссылки и итоговый статус, сохраняя исходный текст замечания. Отдельного финального аудитора этот файл не вводит.

## Независимый вывод

Первая волна существенно восстановила платформу: есть публичное техническое руководство, ясная граница `.qm`/`.tpu`/runtime, конкретные сторонние исходники, исторические bindings и настоящее промышленное интеграционное свидетельство. Ветки в целом честно различают код, заявление и запуск. Главный дефицит — **ни одной согласованной современной поставки с точной моделью, версиями, I/O и аппаратным протоколом**. Поэтому выбор «YOLOv8s static640 opset13» пока является удобной исследовательской гипотезой, а не уже найденным оптимальным или совместимым решением.

Сильнейший технический риск находится на стыках: ONNX → `onnx_direct` → имена/layout TF → `RegularModel`/старый `QuantizedModel.quantize` → threshold/`.qm` → compiler target/preset → `.tpu` metadata → `ProcessingMode.FULL` → raw outputs → конкретный decoder/NMS. Все части встречаются, но их принадлежность одному работающему release не установлена. Многократное чтение одного guide и повторение AST-дефекта разными ветками этот разрыв не закрывают.

Препятствие доступа нельзя расширять: публичная документация доступна, публичный Python source скачан, полноценный SDK и реальное устройство команде **не предоставлены по сохранённым наблюдениям**. Предложенная пользователем ручная регистрация, формы и остановленный Computer Use не являются получением SDK. Computer Use завершён без ввода; продолжения UI эта критика не требует.

## Что уже достаточно установлено и не требует повторного общего поиска

1. **Предмет и уровни продуктов.** ООО «ХайТэк»/LinQ — нужная платформа; `.NET LINQ` и одноимённые сервисы исключены. Чип H, карты HP/HPD/HPQ, HPS и HPC — разные уровни; HPC с двумя HPS не является одним выделенным ускорителем. HX содержит отдельный RK3588/NPU. Основания: W1-01, W1-02, первичные `/tech`, `/sol`, hardware manuals. Уточнять нужно конкретное исполнение, а не снова доказывать существование линейки.
2. **Связь имён без обещания ABI.** Текущая `/sol` прямо связывает IVA H1 framework с LinQ H. В сохранённой презентации 2026 p2 прямо написано `LinQ H1M (К1945ВМ3Я)`; в РЭ HPQ тот же номер микропроцессора. Это уже документальная связь, пропущенная частью итоговых handoff W1. Не требуется новый общий поиск этого соответствия. Из него не следует совместимость IVA H/E/FPGA с H1M.
3. **Публичный guide и gate загрузок.** `/docs` и `Framework_manual_H1.pdf` публично прочитаны; скачивание ПО на `/sol` объявлено доступным после регистрации и верификации. Регистрация и кабинет хакатона — разные контуры. Механизм/срок верификации и фактический результат регистрации неизвестны.
4. **Документированный маршрут конкретной редакции.** Guide 2025 `RU.РМДВ.04.06.014-03 34 01` описывает ONNX → TF → квантование → внутренний Network → `.tpu` → локальный `pytpu` device API. Это содержательная техническая опора, не выданный SDK и не доказательство её устаревания: слово «исторический» означает дату/область, а не установленную отмену поддержки.
5. **Проверка старого `pytpu`.** Sdist 15.0.24 скачан, hash установлен; native `/usr/lib/libtpu.2.so` отсутствует в поставке Python; импорт ленивый; listing `/dev` слабее open/init. README и actual API расходятся. Повторная демонстрация тех же строк или установка старого пакета ради проверки импорта не нужна.
6. **Дефекты стороннего примера.** Unicode-атрибут YOLOv8 runner и `uint8→int8` в auxiliary helper установлены статически/изолированными локальными probes. Первый воспроизведён многими ветками, но это один дефект одного commit. Не нужны новые одинаковые AST-проверки. Исправление не доказывает аппаратную совместимость.
7. **Нет универсального preprocessing.** Guide ResNet, custom ResNet, YOLOv8, vendor TinyYOLO3 и FCN имеют разные контракты. В pinned примерах NMS/часть head decode выполняются на host. Это не доказанный запрет device NMS в платформе вообще.
8. **Пики и исторический MLPerf.** TOPS нельзя переводить в камеры; сумма DDR нескольких чипов не равна установленному лимиту одного графа. MLPerf v0.7 IVATech действительно опубликован, но относится к FPGA Alveo U200. Не нужно углублять историю FPGA для оценки современного detector, если не найдено прямой связи.
9. **Официальный контекст кейса.** Обязательность LinQ inference, обещанный online access и расписание 2026 проверены W1-03. 45 часов — корректный интервал 23.10 13:00 → 25.10 10:00. Не перепроверять расписание в каждой W2-ветке; полное ТЗ/текущие изменения остаются отдельным условием после их получения.

## Матрица покрытия исходных 15 практических вопросов

`док.` = есть конкретная документация/код; `условно` = полезный маршрут, но его совместимость не установлена; `открыто` = ответ влияет на решение и отсутствует. Это оценка содержания, а не число найденных ссылок.

| № исходного вопроса | Покрытие W1 и уже полезный ответ | Существенный остаток | K / W2 |
|---|---|---|---|
| 1. Названия, чип/модуль/система/стек | W1-01/02: док., уровни и связь IVA H1/LinQ; p2 presentation связывает H1M/К1945ВМ3Я | Точное выданное исполнение, ревизии и совместимость targets | K002,K010 / W2-A,H |
| 2. Путь модели | W1-05/06/07/09: док. маршрут редакции -03 и сторонний новый API | Согласованный release, exporter/importer, mapping, compile call и runtime handoff | K003,K004,K008,K009,K012 / W2-B,C,F,G |
| 3. Компоненты, получение, лицензии, версии | W1-03/04/13: публичные guides, PyPI source, gate; SDK не получен | Полная поставка, licenses/переносимость, wheelhouse/image digest | K001,K002,K019 / W2-A |
| 4. Обоснованные модели/детекторы | W1-08: разделены семейства, pose benchmark, сторонний detection code и vendor Tiny | Exact modern detector и собственная голова; бинарники/golden tensors | K005,K006,K007 / W2-D,E |
| 5. Форматы/операции/shapes/precision/pre/post | W1-05/06/07/10: точные локальные контракты; универсальная support matrix не найдена | Opset/IR/attributes, batch/HW, numerical runtime contract, decoder semantics | K004,K006–K009 / W2-C–G |
| 6. Что делать на ПК/RTX и что требует LinQ | W1-04/05/10: подготовка/эталон условно; CPU-only compile правдоподобен | Зависимость compiler/TLM от native runtime/лицензии; предел доказательства | K002,K020 / W2-A,B + deliverables всех веток |
| 7. Значение online access | W1-03/09: корректно разделены SSH/container/job/API | Реальный onboarding, custom model/update, transport/quota/retention | K001,K014 / W2-A,L |
| 8. Video/tracking/rules/UI | W1-10/14: boundaries док., IVA CV integration; image runners не RTSP | Выданный video path, decode/CPU/network budgets, кадры/очереди | K014,K016,K017 / W2-K,L |
| 9. Производительность | W1-02/11: сильное разделение denominator; современная таблица и FPGA logs | Визуальная транскрипция/единицы, реальный modern protocol и multi-chip scaling | K010,K011 / W2-H,I |
| 10. Ошибки/диагностика | W1-12/13: guide warning, exact legacy error templates, host defects | Современные codes, cleanup/recovery/timeouts/concurrency | K012,K015 / W2-G,M |
| 11. Максимально полезные эксперименты | W1-03…15: много хороших предложений | Единые входы/outputs, stop/go критерии, выполнимый приоритет первых часов | K020 / все W2, затем сборщик |
| 12. Первые вопросы экспертам | W1-03/09/12/15: вопросы подробны | Удалить дубли, отделить ответ организатора от SDK-only/hardware-only проверки | K001,K014,K020 / W2-A,L,M + сборщик |
| 13. Подтверждение LinQ execution | W1-15: сильная лестница свидетельств и ограничения negative control | Реальные profiler/manuals, per-request/device binding и coverage всего graph | K009,K013 / W2-G,J |
| 14. Несколько путей реализации | W1-08/09/14: vendor detector/custom compile/service-only условно | Критерии переключения, допустимость host stages и custom weights | K005,K014,K016,K020 / W2-D,K,L |
| 15. Handoff соседним research | Все ветки дают полезные зацепки | Машинно точный candidate manifest, calibration split и границы claims | K004–K009,K017–K020 / все W2 и сборщик |

## Исходные замечания K001–K020

Приоритет `P0` блокирует выбор основного пути/корректность; `P1` заметно меняет модель, интеграцию или диагностику; `P2` полезен при наличии сильной зацепки и не должен задерживать основной маршрут. Приоритет исследования не означает уже существующий дефект LinQ.

### K001 — signup, SDK download и право исполнения остаются разными событиями (P0)

**Проблема/область.** W1-03-F03–06, `ACCESS_HELP_RESULT.md`, RUN_STATE фиксируют лишь публичные формы и gate; пользователь может регистрироваться вручную, подтверждённого результата нет. Нельзя повышать `sdk_access` до «получен» по готовности пользователя помочь или считать верификацию гарантированно ручной. Остановленный Computer Use не является активной сессией ввода.

**Последствие.** Архитектура может ошибочно рассчитывать на локальную компиляцию/установку, тогда как аккаунт даст лишь документы либо организатор выдаст другой сервер.

**Нужное доказательство.** Реальный доступный артефакт с названием/hash/версией или прочитанный authenticated список; отдельно подтверждение права device inference/его режима. Состояние регистрации — только фактическое сообщение пользователя или наблюдение, не предположение.

**Вопрос W2 / опровержение.** W2-A: какие конкретные инструменты доступны без gate/через разрешённый пользователем уже существующий доступ и какие остаются недоступны? Попытаться опровергнуть гипотезу «весь executable SDK закрыт»: проверить реальные прямые links/официальные bundles из навигации, а не угадывать имена файлов. Если доступа нет, завершить точным перечнем отсутствующих артефактов; не повторять signup-исследование и не ждать регистрацию как условия работы всей волны.

### K002 — нет единого современного dependency/ABI manifest (P0)

**Проблема/область.** W1-04-F02–09, W1-09-F03–08, W1-13-F11/13/18: Python3.8 сайта, Python3.11 guide, Ubuntu20.04 guide, Ubuntu24.04 и Framework2026.8.43/Runtime16.18.6 benchmark, pytpu15.0.24 и TF2.14.1 стороннего repo — разные свидетельства. Это не единая установка и не набор обязательных зависимостей.

**Последствие.** Потеря часов на несовместимые Python/native wheels или использование старого ctypes с новой libtpu; ложное обещание Windows/WSL/ARM из `py3-none-any`/логотипов.

**Нужное доказательство.** Для одного release: exact distributions/Requires-Python/Requires-Dist, native `.so`/driver/firmware pairing, compiler target, tested OS/ISA; официальный image digest или lock/wheelhouse и install guide. CPU-only compilation отдельно от hardware runtime.

**Вопрос W2 / опровержение.** W2-A: можно ли восстановить **одну** согласованную поставку современнее/равную guide2025, и какие части действительно требуют LinQ? Искать release metadata, существующие официальные download artifacts/containers, dependencies и CPU-only example. Проверить контргипотезу, что guide2025 всё ещё точно описывает текущий wheel, а отличие Ubuntu — лишь benchmark context. Не объявлять doc obsolete без доказательства.

### K003 — guide нельзя превращать в запускаемый пример без восстановления потерянных швов (P0)

**Проблема/область.** Полный `_WORK/W1_03/Framework_manual_H1_extracted.txt`, pp7,11–14,17,19–20: tuple converter vs single value; Graph vs GraphDef; `ModeProto`; input `' input:1'` и helper `:0`; пропуск определения `tlm_program`; `tf.graph_util.import_graph_def` и другие фрагменты в тексте. Несколько веток видели один extraction; это не визуальное доказательство ошибок оригинала.

**Последствие.** Буквальный перенос фрагментов даст host/API errors до compiler; исправление по догадке будет выдано за официальный рецепт.

**Нужное доказательство.** Оригинальные страницы/векторный текст с сохранённым checksum и matching исходный `end_to_end.py`; точная сигнатура/возврат конвертера и compile call для того же release.

**Вопрос W2 / опровержение.** W2-B: что действительно написано в оригинальном guide, а что потеряно extraction, и существует ли исходный example? Попытаться опровергнуть каждый потенциальный дефект оригиналом/исходником. Сделать errata table `literal → канал → подтверждённый смысл → неизвестное`, не ремонтировать proprietary API воображением. Если bytes получить нельзя, сохранить только статус text-only и не повторять тот же extraction как visual check.

### K004 — поддержка ONNX не локализована до импортера, opset/IR и атрибутов (P0)

**Проблема/область.** W1-05-F03–13, W1-06 operator matrix: нет supported opset/IR/domains, ограничений `Resize`, shape ops, DFL/decode, dynamic shape/batch. Repo `force_static_onnx_input_shape` меняет input declaration, но само по себе не переписывает все shape-dependent constants графа. Opset13 и static640 — решение автора; ONNX>=1.15 из HX — package version.

**Последствие.** «Валидный ONNX» или изменение dim_value не гарантируют правильные внутренние shapes, импорт и компиляцию. Можно преждевременно забраковать архитектуру или неделями обходить несуществующий запрет.

**Нужное доказательство.** Versioned frontend reference/operator matrix или exact successful export+import/compile protocol; attributes/dtypes/ranks, shape inference и обработка output names. Минимальные графы должны происходить из реального выбранного кандидата.

**Вопрос W2 / опровержение.** W2-C: для конкретных YOLO detection/head exports какие реальные узлы и атрибуты определяют риск и есть ли первичное подтверждение их lowering? Проверить альтернативу: современный SDK использует иной direct ONNX path, поэтому старый TF seam не применим. Разделить documented support / source intent / actual compile. Не перечислять типичные NPU ограничения как найденные LinQ restrictions.

### K005 — условный shortlist ещё не доказывает, что YOLOv8s лучше других путей (P0)

**Проблема/область.** W1-08 рекомендует YOLOv8s/n, но найденный benchmark — `yolov8n_pose`, repo self-build — detection s, а `RUN_SCENARIO.txt` финализирует detection на vendor TinyYOLO3. У self-build YOLOv8 нет success logs; отсутствие таких логов не доказывает невозможность. YOLO11 пока family claim, но ВКР СПбПУ имеет авторское сообщение `YOLO11l OBB 20FPS` с нераскрытыми условиями.

**Последствие.** Модельная команда может выбрать наименее подтверждённый граф ради современного имени или отказаться от поддержанного vendor export, который не найден в W1.

**Нужное доказательство.** Exact task/variant/weights/exporter/package versions/HW/batch, build log/`.tpu` и quality evidence. Один known-good detector для smoke test и один путь custom weights должны быть разведены.

**Вопрос W2 / опровержение.** W2-D: существует ли доступный первичный успех custom YOLOv8 detection либо более прямой YOLO5s/YOLO11 detector путь на matched LinQ? Искать автора repo, history/tags/issues/публичную пояснительную записку, технические материалы производителя/университета без обхода авторизации. Попытаться опровергнуть предпочтение YOLOv8: сравнить **замкнутость артефактов**, а не популярность. Если ни один путь не замкнут, дать равноправные условные кандидаты с конкретным первым gate.

### K006 — исправленный runner всё ещё предполагает COCO80 и конкретную голову/NMS (P0)

**Проблема/область.** W1-08-F06, W1-10-F03; source `run_yolov8_tpu.py` функции `normalize_prediction_shape`, `pick_output`, `load_io_names`, NMS call. Размер84/85, COCO80→91, выбор первого rank≥3 output, неприкреплённая версия Ultralytics и возможный objectness85 не образуют безопасный контракт custom PPE detector. `nms=False` не означает, что выход — нераскодированные feature maps: уровень decode надо установить по exporter.

**Последствие.** Custom число классов ломает host adapter; 85-канальная старая YOLO head может пройти shape-check и быть неверно интерпретирована. Успех API и похожие bbox не обнаружат систематическую ошибку.

**Нужное доказательство.** Actual output schema для pinned exporter: xywh/xyxy, pixels/normalized, sigmoid/objectness/DFL status, class count, transpose/layout; exact NMS source/version и golden raw→boxes.

**Вопрос W2 / опровержение.** W2-D: какие изменения действительно нужны для custom N/classes и какие предположения runner неверны даже после typo fix? Проверить контргипотезу, что современные Ultralytics NMS корректно обрабатывает 85 в данном exporter — нужна версия и source, не текущая rolling doc. Подготовить спецификацию адаптации/небольшой pure helper probe при необходимости; не строить полноценный прототип и не делать новый TPU claim.

### K007 — vendor TinyYOLO3, strict export и Model Zoo остаются тремя непаритетными моделями (P0)

**Проблема/область.** W1-08-F07, W1-10-F05/06, repo TinyYOLO files. Vendor `.tpu` отсутствует; strict export даёт BGR metadata, ORT helper не применяет `image_color_order`; TPU runner делает RGB; Model Zoo имеет другой I/O/NMS и recipe. Дополнительное чтение критика: `iva_applications==11.0.1/tiny_yolo3/postprocess.py` жёстко assert `(1,13,13,255)` и `(1,26,26,255)`. Его MIT наличие не делает его готовым b8/custom-N decoder.

**Последствие.** Измеренная разница AP или FPS будет смесью цветов/весов/head boundary/NMS, а не эффектом quantization/LinQ. Vendor smoke test не докажет путь собственного PPE training.

**Нужное доказательство.** Hash/source vendor weights, `.tpu` metadata и golden tensor/output, original pre/post reference; для baseline — immutable cfg/weights и точный output boundary. Старый helper — лишь versioned source evidence.

**Вопрос W2 / опровержение.** W2-E: можно ли действительно сопоставить хотя бы две эти ветки на одинаковых весах и одинаковом подготовленном входе? Проверить альтернативу, что vendor binary ожидал BGR, а RGB runner сам неверен; не объявлять RGB универсально правильным. Найти готовый artifact/manifest или честно установить непаритетность. Разобрать anchors/masks/order/sigmoid/coordinate transforms и b8 без повторного общего обзора YOLO.

### K008 — PTQ путь есть, но percentile/threshold и численная схема не раскрыты (P1)

**Проблема/область.** W1-07-F02–07 и guide p8: percentile описан как процент весовых коэффициентов, repo передаёт его calibrate и ловит любой TypeError с повтором без параметра. Неизвестны activation/weight clipping, signedness, granularity, rounding, accumulator, QAT/QDQ import. Два/100/500 samples — разные цели, не нормы достаточности.

**Последствие.** Эксперимент percentile может менять не тот параметр или не менять его вовсе; «INT8 ONNX» может не войти в LinQ path; потеря мелких СИЗ может остаться не локализована. Memmap ~2.29GiB — backing store, не peak RAM калибровки.

**Нужное доказательство.** Актуальный quantizer reference/source docstrings, threshold schema/save-load, effective parameters/logging, layerwise comparison; точный calibration→input recipe и качество на независимом eval.

**Вопрос W2 / опровержение.** W2-F: что именно калибрует `RegularModel.calibrate`, как применяется percentile и что можно повторить/экспортировать? Проверить контргипотезы «параметр относится только к weights», «новое API поддерживает activation clipping/QAT». Если SDK недоступен, дать versioned документальный остаток и минимальный эксперимент, различающий эти исходы; не назначать стандартную asymmetric/per-channel схему из общего знания.

### K009 — внешний float32, quantized TF rescale и runtime FULL не связаны численно (P0)

**Проблема/область.** Guide pp16,20–21 и pytpu `_bindings.py`: explicit rescale у quantized TF, original float feed у hardware, enum RAW/PRE_PROCESS/POST_PROCESS/FULL. Эти имена не раскрывают, где выполняются transpose/scales/casts/packing, какие операции уже скомпилированы и что входит в host/native pre/post.

**Последствие.** Ручной int8 cast/rescale может дважды преобразовать данные; отсутствие ручного rescale может быть правильным для одного `.tpu` и неверным для другого. Граница «вся сеть на TPU» также зависит от смысла native stages.

**Нужное доказательство.** Одна `.tpu` + metadata user/raw dtype/shape/scales, documented FULL/RAW transform, raw↔user golden pairs и current SDK API. Сопоставить quantized reference, TLM и runtime на одинаковом входе; не требовать FP32 bitwise equality.

**Вопрос W2 / опровержение.** W2-G совместно W2-F/J: кто выполняет численное преобразование границ программы и что доказывает режим FULL? Искать reference/native headers/examples; проверить альтернативу, что `.tpu` хранит host processing program, который является штатной частью inference. Не называть это ни CPU fallback, ни гарантированно TPU preprocessing до документа.

### K010 — конкретная топология/память неизвестны, а имена папок противоречат числу устройств (P1; P0 после выдачи target)

**Проблема/область.** W1-02: HP 16/32GB, Gen3/Gen2; HPD/HPQ power и названия исполнений; aggregate DDR. Новый locator критика: `RUN_SCENARIO.txt` §8 называет HPD1M и четыре `/dev/tpu3…0`, тогда как РЭ HPD1M-01 описывает два chips/endpoints, HPD1M-10/11 (HPQ) — четыре. Это может быть несколько карт, переименование, общий host или неточное label; вывод о числе чипов по имени каталога недопустим.

**Последствие.** Неверная оценка multi-device scaling, памяти на граф и quota; некорректное сравнение HP/HPD и перенос artifact target.

**Нужное доказательство.** Даты/revisions hardware PDFs, authoritative SKU↔chip↔PCIe endpoint↔runtime device mapping, per-graph memory limits/memory planner, hardware_parameters. Установить physical capabilities отдельно от negotiated link и allocated resources.

**Вопрос W2 / опровержение.** W2-H: какие расхождения реально относятся одному исполнению и какие снимаются revision/BOM? Визуально сверить конфликтные таблицы, включить presentation p3 (HP PCIe2.0, иные TDP). Попытаться опровергнуть «единая память недоступна»: искать explicit multi-chip graph partitioning/remote memory docs; отсутствие таких docs оставить unknown, а не «платформа не умеет».

### K011 — современная таблица performance ещё text-only и не имеет единого timing contract (P1)

**Проблема/область.** W1-11-F01/02, сохранённый presentation JSON p3/p4. `anti_spoof 985.72ms`, `lenet5 128.90ms` при тысячах FPS; HPQ=4×HP во всех строках и та же latency; p3 ResNet460/1046 против p4 432.9/1112.8; batch8 SSD slower. Их нельзя чинить делением на1000. Заявление «по методике MLPerf» не submission/log.

**Последствие.** Ошибка единиц/сценария превратится в ожидания latency/камер; искусственное среднее с ВКР и историческим FPGA создаст ложную уверенность.

**Нужное доказательство.** Визуальная таблица/исходный слайд, units и footnote; modern logs/scenario/LoadGen/version/model/input/preset/precision/quality/device count, inclusion transfers/NMS и latency percentile. Сам внешний timer sync также не чистый compute.

**Вопрос W2 / опровержение.** W2-I: что обозначают FPS/latency в этой конкретной таблице и есть ли underlying modern protocol? Попытаться опровергнуть гипотезу typo: иные scenario/overlap/percentile могут согласовать числа. Проверить, действительно ли HPQ измерялся отдельно. ВКР/авторский repo исследовать лишь для недостающего протокола; защищённый full text не обходить. При неуспехе сохранить числа без «исправления» и не обещать камеры.

### K012 — legacy Python source не задаёт текущий native ABI, buffers и lifecycle (P0)

**Проблема/область.** W1-09/12/15, `_bindings.py`: lazy absolute `.so`, native JSON schema, inputs pointers без dtype/size validation, RAW ZIP heuristic; context managers имеют yield без try/finally, TODO buffer destroy. Это конкретный source2023, не установленная уязвимость/дефект Runtime2026.

**Последствие.** Ошибочный ndarray layout/dtype может не дать раннего исключения; старый binding нельзя безопасно считать актуальным. Повторный inference/cleanup после exception и живучесть output arrays требуют контракта.

**Нужное доказательство.** Matching current Python/native headers/reference и version matrix; metadata schema user/raw region keys, input lifetime/contiguity, buffer ownership/output copy semantics, release notes cleanup. Устройство/`.so` не запускать старым ctypes наугад.

**Вопрос W2 / опровержение.** W2-G: какие конкретные API/ABI и tensor schemas действуют в доступной современной поставке? Найти public headers/examples/package source, сопоставить с15.0.24. Попытаться опровергнуть опасения о cleanup/validation современным кодом или явным native контрактом. Если версия не получена, legacy риски маркировать только как вопросы, а не troubleshooting2026.

### K013 — доказательство отсутствия полного и частичного fallback требует разных свидетельств (P0)

**Проблема/область.** W1-15 предлагает сильную цепочку, но profiler только назван в HPS datasheet; реальные commands/counters не найдены. Invalid-device test различает fail-closed при open, но не исключает host operation partitioning или замену модели server-side. Нагрузка общего TPU может быть чужой.

**Последствие.** Скриншот utilisation, node mapping, `backend=LinQ` или return200 не докажут выполнение нашей модели, а строгий критерий жюри неизвестен.

**Нужное доказательство.** Versioned Performance Profiler/DNN Stat manual/sample report; per-request/artifact/device correlation, compiler coverage/partition report или официальная гарантия whole graph/no fallback; допустимый критерий организатора. App-side logs и native runtime остаются разными trust boundaries.

**Вопрос W2 / опровержение.** W2-J: какое сильнейшее **реально доступное** свидетельство связывает конкретный artifact/input/completion с физическим LinQ для SSH и service-only? Проверить альтернативу, что profiler показывает лишь host estimates/aggregate, либо SDK по конструкции не допускает model fallback и coverage доказывается artifact format. Не придумывать `linq-smi`/strict flag и не требовать недоказанную аппаратную attestation как обязательное условие кейса.

### K014 — online contract должен включать обновление собственной модели, квоты и путь кадров (P0)

**Проблема/область.** W1-03/09 разложили сценарии, но не установлены control/data plane: разрешён ли custom graph/weights, compiler service или только готовые models, persist storage, runtime sessions, limits, transport и camera reachability. Cloud vacancy и IVA CV Edge API не спецификация LinQ access.

**Последствие.** Можно получить действительный LinQ API, на котором невозможно выполнить собственную PPE модель; локальный UI/remote runtime могут не иметь доступного двустороннего канала/порта. Это влияет на архитектуру сильнее выбора NMS.

**Нужное доказательство.** Official onboarding/API/job/SSH instructions, permitted artifact type/update process, request/response schema/dtype, authentication, quotas and timeouts, concurrency/backpressure, persist/retention и logs. Секреты в отчёты не сохранять.

**Вопрос W2 / опровержение.** W2-L: какие режимы реально подтверждены для demo/соревнования и что у каждого разрешено делать со своей моделью? Попытаться опровергнуть предположение «обязательно нужен shell»: рабочий tensor/model API может закрыть задачу без него. Одновременно искать ограничения service-only, которые заставляют выбрать иной маршрут. Не угадывать endpoints и не отправлять сообщения от имени пользователя.

### K015 — concurrency, cancel и безопасное восстановление неизвестны (P1)

**Проблема/область.** W1-12 выявил legacy cleanup/watchdog TODO; W1-09 не нашёл supported async/thread API. Persistent video service добавляет очереди/таймауты/worker restart, которых single-frame example не проверяет. Native submit symbol не равен публичному async API.

**Последствие.** Одно exception может испортить worker/session; retry в том же процессе или перебор input names скрывает первопричину. Reset shared driver может нарушить работу других команд.

**Нужное доказательство.** Current troubleshooting/release notes, error code table, thread/process/session isolation, timeouts/cancel/retry semantics, safe participant recovery path. Если документов нет — последовательный эксперимент с ordinary permitted error, new worker и known-good artifact, без watchdog fault injection.

**Вопрос W2 / опровержение.** W2-M: какие ошибки/состояния действительно требуют new process, session reload или администратора и что можно диагностировать без reset? Искать доказательства исправленного cleanup/current contract; опровергнуть перенос старого skipped watchdog test на современную платформу. Не повторять Unicode bug и не публиковать выдуманные modprobe/reset команды.

### K016 — промышленная интеграция сильнее маркетинга, но не единый доказанный PPE pipeline на LinQ (P1)

**Проблема/область.** W1-14-S01/S02/S03/S04: новость2026 ПАК ОТПБ прямо называет LinQ; guide IVA CV даёт generic container `/dev/tpu0`, image0.1.310 и Edge-api; user guide перечисляет PPE/events. Не установлено, что это одна и та же build/model конфигурация и что все NN-стадии/события выполнены LinQ. Именованные deployments IVA CV не указывают TPU.

**Последствие.** Склейка трёх документов создаст несуществующий freely runnable official PPE demo; число типов событий/камер UI не даст throughput/качество или лицензии.

**Нужное доказательство.** Matching deployment manifest/model/backend inventory/image digest/licensing, технический доклад/видео с таймкодами фактического execution и stage boundaries, данные пилота. Registry URL не означает анонимно доступный образ.

**Вопрос W2 / опровержение.** W2-K: можно ли связать ПАК ОТПБ с конкретным TPU container/model pipeline и получить переносимый deployment recipe? Попытаться опровергнуть предположение, что generic `/dev/tpu0` относится именно текущему LinQ H1M/PPE build; искать version/date/backend в первичном guide. Проверить record четырёхсетевой «Лиры» как сообщение/наблюдаемую демонстрацию, а не приравнивать к четырём RTSP streams.

### K017 — decode, host quota и многокамерная задержка остаются отдельной инженерной веткой (P1)

**Проблема/область.** W1-10/14 хорошие boundaries, но actual codec/decoder/source cadence/frame timestamps/backpressure/CPU budget в доступе неизвестны. W1-02 местами называет HPS video-ASIC декодером, W1-10 уточняет видеокодирование; из неоднозначного «codec» нельзя вывести decode. HX video functions относятся RK3588, не автоматически TPU.

**Последствие.** Успешный detector FPS может сопровождаться растущим frame age; NMS/tracker/decode на ограниченном host станет bottleneck. Batching из восьми камер добавляет ожидание batch formation и fairness, отсутствующие в image runner.

**Нужное доказательство.** Точная опция/BOM/API encode/decode, доступный host CPU/RAM/network, multi-stream example/scheduler и timestamp/queue semantics. Для протокола — отдельно cold start, sync-call time, network, batch wait, frame age и event delay.

**Вопрос W2 / опровержение.** W2-K/L: есть ли реальный поддержанный video path и что ускоряет именно он? Проверить альтернативу, что decode уже включён в supplied service, либо API принимает только тензоры. Проектировать bounded queue/drop/reconnect как условный наш adapter; не выдавать его за функцию SDK. Уточнить допустимость host tracking/NMS у постановщика после полного ТЗ.

### K018 — число веток не равно числу независимых доказательств (P1, сквозное)

**Проблема/область.** Большая часть W1-04…15 зависит от одного guide extraction, одного repo commit и одного sdist. Часто «independent AST» подтверждает лишь тот же host literal. Text из TinyFish, web cached PDF и повторная TinyFish extraction могут быть одной upstream версией. Отдельные новые сильные линии — IVATech archive, industrial partner docs, university author metadata — требуют собственной области применимости.

**Последствие.** Сборщик может превратить десять ссылок на один defect/claim в десять подтверждений hardware support. Неясная сохранность PDF bytes мешает установить, что каналы видели ту же редакцию.

**Нужное доказательство.** Source lineage, canonical URL/content hash/commit/version и `read channel/status`; независимость по автору/эксперименту, а не исследователю. Primary source runtime log и чужой код не взаимозаменяемы.

**Вопрос W2 / опровержение.** Во всех заданиях: какое **новое первичное** доказательство добавлено сверх существующего source lineage? W2-D/I/K целенаправленно ищут независимые технические протоколы, пытаясь опровергнуть гипотезу «весь modern вывод замкнут на vendor slide и один repo». Если найден только пересказ, записать зависимость и не повышать статус. Отдельная W2-ветка для повторной сверки всех фактов не нужна.

### K019 — разрешение изучать source не даёт права распространять SDK/weights/image (P1)

**Проблема/область.** W1-13 различает MIT helper, bindings license unknown, repo license null, OEM software pricing; W1-14 частный registry. Но practical route может молча требовать раздать image пяти участникам, загрузить proprietary weights/данные в cloud или опубликовать `.tpu` в сдаче.

**Последствие.** Даже технически рабочий путь может не позволять перенос tooling/artifact или включение его в публичный repo. Политика ПД формы не SDK EULA. При этом неизвестная лицензия не означает уже установленный запрет на выполнение.

**Нужное доказательство.** Actual license/EULA/download conditions для каждой используемой поставки, sample code, checkpoint и compiled artifact; право execute/modify/redistribute отдельно. Не общий юридический обзор.

**Вопрос W2 / опровержение.** W2-A/E/K: какой конкретный route разрешён доступными условиями и какие права ещё нужно уточнить? Попытаться найти явную лицензию, опровергающую metadata UNKNOWN/null; использовать сохранённый LICENSE из actual archive, не соседний пакет. Не задерживать read-only исследование ожиданием несуществующего согласования.

### K020 — эксперименты нужны как дерево решений с одним владельцем каждой границы (P0 для итогового handoff)

**Проблема/область.** Во всех W1 много хороших E, но они дублируются: inventory/smoke/parity/performance повторены почти в каждой ветке. Нет общей спецификации, какой минимальный успешный результат даёт переход к custom model и когда остановить неподтверждённый путь в пределах45часов. Hardcoded «30–60мин» в W1-11 — план, не измеренное время.

**Последствие.** Пять инженеров будут повторять inventory и спорить о разных preprocess вместо закрытия независимых стадий; слишком сложный ladder без доступного TLM может выглядеть обязательным.

**Нужное доказательство/уточнение.** Для каждого W2 результата: состояние «можно проверить сейчас / нужен SDK / нужен LinQ / нужен ответ постановщика», exact artifacts/prerequisites, ожидаемое наблюдение, альтернативный исход и что success **не доказывает**. Одна shared golden input/output specification, один model manifest, уникальные владельцы. TLM — полезный checkpoint при наличии, не mandatory доступный инструмент.

**Вопрос W2 / опровержение.** Каждая W2-ветка обязана дать решающий эксперимент с минимумом предпосылок и попыткой опровержения своего provisional conclusion. Проверить гипотезу «known-good vendor smoke обязателен»: если поставщик даёт только compiler+custom example, возможен другой подтверждаемый старт. Сборщик затем объединяет E/R и priority questions без отдельной поисковой/аудиторской стадии. Не разрабатывать сдаваемый prototype в исследовании.

## Содержательная карта второй волны

Ниже 13 групп получилось из разных недостающих инженерных ответов, а не из квоты. Их можно выдать самостоятельным Medium-исследователям очередями. Взаимозависимые K уже объединены; broad повтор W1 не нужен. За каждым заданием отдельный `_WORK/W2_XX_RESULT.md`/подкаталог; общий CRITIC меняет затем только сборщик. Все сетевые исследования выполняются gpt-6.1-sol / medium. Исследователи сохраняют новые evidence и попытку опровержения даже при незакрытом вопросе.

### W2-A — современная поставка SDK, получение и воспроизводимое окружение

- **K:** K001,K002,K019,K020. Решение: где можно компилировать/исполнять и какой environment готовить.
- **Старт:** W1-03/04/13; `ACCESS_HELP_RESULT.md`; `/docs`, `/sol`; guide2025; named Runtime16.18.6/Framework2026.8.43; PyPI maintainer graph и negative lookups уже проверены.
- **Новый поиск:** release/install notes, реальный direct bundle/официальный channel, METADATA/Requires-Dist/native pairing, current model-zoo locator и лицензия. Если пользователь фактически предоставил доступ/файлы — исследовать их read-only, hash/состав, не предполагать отсылку credentials. Не повторять форму регистрации; не создавать аккаунты/сообщения.
- **Фальсификация:** попытаться найти открытый executable release; проверить, совместим ли guide -03 с modern stack и действительно ли compiler работает без device/native runtime.
- **Выход:** одна нормализованная component/version/access/license matrix с неизвестными ячейками; executable minimal install/CPU-compile test только как план, если поставка не получена. Exact unavailable observations, не «SDK отсутствует вообще».

### W2-B — оригинальный framework guide, errata и полный end-to-end source

- **K:** K003,K002,K020. Решение: можно ли начать со штатного source example.
- **Старт:** полный W1-03 extraction и W1-05 discrepancy table; original URL. Отдельный visual gap presentation p6 можно закрыть здесь, если получены bytes; performance p4 принадлежит W2-I, hardware conflicts — W2-H.
- **Новый поиск/чтение:** получить оригинал законным доступным каналом/официальный source archive, render pp7/11–14/17/19–21, проверить page count/metadata; найти `end_to_end.py`/`onnx_to_tf` signature и missing compile assignment.
- **Фальсификация:** ошибки могли быть extraction loss, а return types/API могли принадлежать разным версиям. Не утверждать original bug по одному текстовому каналу.
- **Выход:** source-preserving errata и версия matched example; если source отсутствует — точная спецификация запроса, без выдуманного runnable script. OS logos, если прочитаны, остаются claim, не install matrix.

### W2-C — ONNX frontend и минимальная карта graph constraints кандидатов

- **K:** K004,K005,K008. Решение: что передать `model_stack` и какие варианты экспорта действительно проверять.
- **Старт:** W1-05/06; pinned build/export source; guide importer; запросы точных `onnx_direct`, `RegularModel`, target names.
- **Новый поиск:** versioned frontend docs/source/examples, actual supported opset/IR/attributes; direct ONNX alternative; batch/HW constraints и shape-dependent constants. Сосредоточиться на графах из W2-D/E, а не всех ONNX operators.
- **Фальсификация:** static13/noNMS может быть лишь авторским выбором, а современный parser поддерживать другие opsets/dynamic batch; наоборот successful export не гарантирует lowering. Unknown не помечать unsupported.
- **Выход:** table `candidate→operator/attribute→evidence/version→risk→minimal differentiating test`; точный exporter/graph inventory handoff. Если нет model bytes, не выдумывать actual graph nodes по семейному имени.

### W2-D — современный custom detector и корректный custom-class output adapter

- **K:** K005,K006,K018,K020. Решение: какой custom PPE model route имеет лучшую доказательную опору.
- **Старт:** pinned YOLOv8 exporter/build/runner, RUN_SCENARIO final Tiny path; vendor yolo5s/yolov8n_pose; СПбПУ metadata `vr26-931`.
- **Новый поиск:** success evidence автора repo/пояснительные материалы/history/issues и официальный exact YOLO5s/YOLO8/YOLO11 sample. Для найденной конфигурации проследить веса/exporter→compiler→runtime; отдельно source version Ultralytics NMS и 4+N/5+N semantics.
- **Фальсификация:** найти контрпример предпочтению v8; исследовать возможность modern supported detector, пропущенного W1. Не расширять в полный обзор модельного рынка/обучения.
- **Выход:** 2–3 условных кандидата по замкнутости chain, exact gaps/gates; postprocess schema для custom classes и planned patch list. Unicode bug повторно не исследовать. Если автор сообщает запуск — это reported execution, не наш тест.

### W2-E — vendor TinyYOLO3 provenance и сравнимость pre/post веток

- **K:** K007,K006,K019. Решение: пригоден ли vendor detector как ранний smoke и как сравнивать его quality.
- **Старт:** `tiny_yolo3_b8_o5_128x128_asic.tpu` path; strict Darknet exporter; ONNX Model Zoo card; `iva_applications11.0.1` source и LICENSE в архиве.
- **Новый поиск/анализ:** actual vendor artifact/weights/recipe or matched package; точный anchors/order/names/scales, RGB/BGR, padding/interpolation and inverse geometry; old MIT decoder b1/255 restrictions. Не скачивать большие датасеты/не проводить benchmark.
- **Фальсификация:** проверить, не неверен ли именно RGB runtime; не подменён ли baseline другим graph с embedded NMS/second input.
- **Выход:** three-path manifest с parity/non-parity verdict по каждому шву; golden tensors/raw outputs specification и небольшой воспроизводимый host-only probe при необходимости. Нельзя заявлять общие веса без hash/source.

### W2-F — quantizer semantics, thresholds и калибровка с контролем качества

- **K:** K008,K009,K020. Решение: как измерять PTQ loss и избегать ложного percentile experiment.
- **Старт:** guide §§3.1/термины; RegularModel code; memmap recipe и silent TypeError retry; сохранённые historical dnn_quant traces.
- **Новый поиск:** актуальная API/spec/examples threshold granularity/rounding/signedness/percentile/save-load, QAT/QDQ только при конкретной зацепке; layerwise compare tool и current TLM numerical scope. Не создавать учебник INT8.
- **Фальсификация:** проверить weights-only vs activations percentile, наличие нового QAT path, ignored parameter и double rescale.
- **Выход:** точная numerical evidence matrix; staged eval protocol для малых СИЗ с camera/time-separated calibration/eval, memory/time artifacts и исходами. 100/500 не объявлять достаточным нормативом.

### W2-G — `.tpu` schema, current runtime/native ABI и пользовательские/сырые тензоры

- **K:** K009,K012,K002. Решение: безопасный и корректный tensor adapter.
- **Старт:** saved pytpu15.0.24 actual code (README отдельно), guide runtime API, Program.info metadata/hardware_parameters, FULL/RAW enums.
- **Новый поиск:** current Python/C/C++ reference/headers/source/serialized model schema, version compatibility, user/raw buffers/scale/layout/lifetime; actual `.tpu` sample при доступности. Не выполнять неизвестный native code; artifact ZIP reading допустим как research.
- **Фальсификация:** найти changed validation/cleanup/current `.so` contract; проверить, какие stages FULL делает на host/device и не является ли older raw heuristic неприменимым.
- **Выход:** versioned API/schema diff и утверждения с границами; validation checklist на actual metadata, не generic guessed names; request list для закрытых fields. Современные проблемы не выводить из2023 TODO.

### W2-H — аппаратные ревизии, адресация памяти и multi-device mapping

- **K:** K010,K002,K011. Решение: compiler target/memory fit/concurrency и interpretation scaling.
- **Старт:** W1-02 SOURCE_EXTRACTS, exact paired manuals/datasheets, presentation p2/p3, RUN_SCENARIO §8 four-device HPD1M label.
- **Новый поиск:** original visual tables/revision metadata, vendor SKU documentation и memory planning/partition examples; установить scope power/PCIe conflicts и H1M/partnumber link уже учесть как найденную.
- **Фальсификация:** расхождения могут быть разные комплектации; несколько `/dev` не доказывают одну HPD; sum memory может быть доступна via explicit graph distribution, но это требует docs.
- **Выход:** конфликтная таблица с status/resolution, mapping diagram/table chip↔card↔endpoint↔runtime context и first-inventory protocol. Не бесконечная аппаратная история/оценка производства.

### W2-I — современный benchmark: единицы, сценарии и первичные протоколы

- **K:** K011,K010,K018. Решение: какие числа допускаются в защите и что измерять самим.
- **Старт:** presentation2026 p3/p4 сохранённый JSON, W1-11 normalized table, historical pinned MLPerf как образец scope, public thesis/Habr/source repo leads.
- **Новый поиск:** original visual table/underlying modern logs, exact model/input/preset/quality/scenario/latency metric; current MLPerf submission только если обнаружен primary locator. ВКР — публичная lawful версия/доклад/приложение; full text за login не обходить.
- **Фальсификация:** ms may be correct under another scenario; HPQ might be measured or arithmetic. Не заменять значения собственными догадками и не искать ещё десятки пересказов цифр.
- **Выход:** measurement records со denominator/units/tested_here; corrected transcription **только при source evidence**, иначе unresolved conflict. Minimal benchmark matrix correctness first, cold/warm/session/data transfer/end-to-end раздельно.

### W2-J — profiler и проверяемое execution evidence для actual access mode

- **K:** K013,K009,K014. Решение: как показать обязательный LinQ inference без фиктивного indicator.
- **Старт:** HPS Performance Profiler/DNN Stat/Power Monitor names, W1-15 evidence chain, actual legacy APIs; whole/partial fallback distinction.
- **Новый поиск:** конкретные manuals/package/sample reports/maintainer statements, coverage/partition/strict execution semantics и device identity; различать per-request vs aggregate counters и estimated vs measured values.
- **Фальсификация:** monitoring may not prove our request; no Python fallback is not native guarantee; explicit artifact ISA may offer stronger evidence than utilisation.
- **Выход:** два адаптируемых протокола SSH/container и service-only с полями/сильными и слабыми свидетельствами, безопасным negative control и запросом допустимого критерия жюри. Никакого выдуманного CLI/attestation и отключения shared device.

### W2-K — техническая промышленная интеграция, IVA CV и video boundary

- **K:** K016,K017,K019,K018. Решение: можно ли использовать готовую интеграцию либо перенести её architecture lessons.
- **Старт:** W1-14 exact IVA CV admin/user guides, platform/ОТПБ, image0.1.310, registry, «Лира» interview/Aquarius announcement.
- **Новый поиск/чтение:** сохранить технические source excerpts/страницы и version scope; проверить matching LinQ backend/image/model/event pipeline, public sample/license/pull conditions; если видео доступно — смотреть и указывать таймкоды, не цитировать аннотацию как просмотр.
- **Фальсификация:** generic TPU mapping may target older hardware; industrial cases may use other backend; encode option does not establish decode. Не исследовать остальных клиентов ради списка логотипов.
- **Выход:** конкретная deploy sequence и missing supplied assets, source-based per-stage host/device boundary; multi-camera conditions и что не установлено. Права/доступы к registry не угадывать, авторизацию не обходить.

### W2-L — online control/data plane и ограничения видеосервиса

- **K:** K014,K017,K001,K020. Решение: где живут custom model, runtime worker и сервис команды.
- **Старт:** public case promise, W1-09 conditional modes, W1-14 Edge-api строго отдельного продукта.
- **Новый поиск:** official online/demo/onboarding docs, custom graph/weights upload/compile/run/update, payload/file/job/SSH permissions, quota/concurrency/network/persist/session limits. Если нет новых материалов — не имитировать API; составить адресные questions с решением после каждого ответа.
- **Фальсификация:** service-only может быть достаточен; shell может не позволять long-running server/порты/cameras. Проверить обе ветки, а не автоматический выбор SSH.
- **Выход:** confirmed-vs-conditional control/data plane matrix и R branches, bounded queue/timestamp/frame identity contract как **наша** рекомендация; first5 expert questions. Ответы не запрашивать письмом/чатом без пользовательского поручения.

### W2-M — современная диагностика, session isolation и безопасное восстановление

- **K:** K015,K012,K020. Решение: когда retry, reload или worker replacement и что сохранять при сбое.
- **Старт:** W1-12 exact templates/legacy limitations; repo blanket retries; skipped watchdog как historical question, не современный fault.
- **Новый поиск:** current runtime error tables/release notes, supported concurrency/multiprocess/async cancel, safe reset/reference sample; сопоставить версии с W2-A/G и обнаружить documented fixes.
- **Фальсификация:** old cleanup hazard may be fixed/native-protected; oneprocess/perdevice may be sample choice, not constraint.
- **Выход:** symptom→owner(layer)→evidence→differentiating check→safe action/version; future restart/reload/timeout experiment без destructive fault injection. CLI/system-reset команды давать лишь из matching docs; отсутствие сведений оставить отдельным blocker/question.

## Общие условия сдачи W2, чтобы не потерять инженерную ценность

Каждой группе нужен не новый обзор, а изменение конкретного решения. Обязательные поля результата: связанные K; какие существующие provisional conclusions пытались опровергнуть; новые источники с version/hash/locator и зависимостью происхождения; что нашли и что не нашли; actual access/test boundary; какая гипотеза выдержала/изменилась; exact unknown и способ закрыть; один решающий будущий эксперимент и один handoff соседям. Не нужно много однотипных проверок ради количества.

Без SDK допустимы чтение/статический анализ/малые изолированные probes, но нельзя маркировать их export/compile/device success. Даже если ручная регистрация даст SDK посреди волны, это не автоматически выдаёт device; сначала обновить состояния конкретных компонентов. Не устанавливать старые public packages в пользовательское рабочее environment ради формального progress.

Технические вопросы поставщику группировать по решениям: (1) actual access/custom model/target и критерий обязательного inference; (2) matching release/known-good example/полный delivery manifest; (3) artifact I/O+pre/post и поддержанный custom export; (4) quota/logs/profiler/recovery; (5) exact shape/quant quality только после первых ответов. Полное подробное Q сохраняется, но первая встреча не должна стать опросом о всех неопределённых low-level параметрах сразу.

После W2 сборщик назначает стабильные F/S/Q/E/R и фиксирует обработку каждого K (`закрыт новым доказательством / уточнена область / противоречие / открыт / потерял значение`) с source locator. Несогласованные параметры остаются несогласованными. Сборка/автор/редактор/сжиматель не получают скрытую третью web-волну и не превращаются в дополнительный финальный аудит.

## Дополнительно прочитанные критиком сохранённые доказательства

Индекс всех прочитанных результатов первой волны: [01 — имена](_WORK/W1_01_RESULT.md), [02 — оборудование](_WORK/W1_02_RESULT.md), [03 — доступ](_WORK/W1_03_RESULT.md), [04 — окружение](_WORK/W1_04_RESULT.md), [05 — импорт](_WORK/W1_05_RESULT.md), [06 — компилятор](_WORK/W1_06_RESULT.md), [07 — квантование](_WORK/W1_07_RESULT.md), [08 — модели](_WORK/W1_08_RESULT.md), [09 — runtime](_WORK/W1_09_RESULT.md), [10 — видео/I/O](_WORK/W1_10_RESULT.md), [11 — performance](_WORK/W1_11_RESULT.md), [12 — диагностика](_WORK/W1_12_RESULT.md), [13 — экосистема](_WORK/W1_13_RESULT.md), [14 — интеграции](_WORK/W1_14_RESULT.md), [15 — execution evidence](_WORK/W1_15_RESULT.md). Исходное задание: [prompt-linq-platform.md](prompt-linq-platform.md); организация: [PLAN](_WORK/PLAN.md), [RUN_STATE](_WORK/RUN_STATE.md).

Канонические первичные локаторы, используемые в K и W2: [Framework manual H1](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), [презентация2026](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf), [HP datasheet](https://files.lin-q.ru/tpu/datasheet/linq_hp_datasheet.pdf), [HP1M-02 РЭ](https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf), [HPD1M-01 РЭ](https://files.lin-q.ru/tpu/docs/_HPDpass_manual_LINQ_HPD1M_01.pdf), [HPQ/HPD1M-10 РЭ](https://files.lin-q.ru/tpu/docs/_HPQpass_manual_LINQ_HPD1M_10.pdf), [HPS datasheet](https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf), [pytpu15.0.24](https://pypi.org/project/pytpu/15.0.24/), [iva-applications11.0.1](https://pypi.org/project/iva-applications/11.0.1/), [pinned linq-cv-bench](https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140), [IVA CV administrator guide](https://ivacv.ru/wp-content/uploads/2026/05/Руководство_администратора_сайт.pdf), [ВКР СПбПУ — открытая metadata](https://elib.spbstu.ru/dl/3/2026/vr/vr26-931.pdf/info), [IVATech MLPerf v0.7 pinned](https://github.com/mlcommons/inference_results_v0.7/tree/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech). Эти ссылки указывают происхождение сохранённых свидетельств; критик их заново по сети не запрашивал.

- `_WORK/W1_03/Framework_manual_H1_extracted.txt` — полный guide extraction; первичный URL https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf ; paragraphs/pages выше. Оригинальные PDF bytes/visual verification отсутствуют в W1.
- `_WORK/W1_08/presentation2026_tinyfish.json` — весь текст official2026 slides, особенно p2 H1M/partnumber, p3 HP2.0/TDP, p4 benchmark и пустая графическая p6; https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf .
- `_WORK/W1_02/SOURCE_EXTRACTS.md`, `_WORK/W1_06/SOURCE_EXCERPTS.md`, `_WORK/W1_11/ACCESS_LOG.md`, `_WORK/ACCESS_HELP_RESULT.md` — параметры/locator/access provenance, с оговоркой, что это сохранённые выписки исследователей.
- `_WORK/W1_06/linq-cv-bench/RUN_SCENARIO.txt` целиком; `scr/detection/build_yolov8_program.py`, `run_yolov8_tpu.py` целиком; relevant strict exporter/ORT helper source fragments. Canonical pinned tree https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140 . Никакие исходники не изменялись и модели не запускались.
- `_WORK/W1_09/PYTPU_SOURCE/pytpu-15.0.24/pytpu/_bindings.py` целиком; source/hash в W1-09/W1-15. Чтение подтверждает actual branches, но не поведение отсутствующей `.so`.
- `_WORK/W1_13/SOURCE/iva_applications-11.0.1/setup.py`, `src/iva_applications/tiny_yolo3/postprocess.py`, relevant yolo3 source locators, `_WORK/W1_13/KEY_SOURCE_LOCATORS.TXT`. Новое узкое наблюдение о hardcoded tiny heads — source_code, не execution; лицензия/archive attribution остаются в W1-13.
- `_WORK/W1_10/CONTRACT_PROBES_RESULT.json` — реальный изолированный helper result и formula-only geometry, не OpenCV pixel test/не аппаратный запуск.
- `_WORK/W1_11/MLPERF_2020/SYSTEMS__IVA-FPGA-1.JSON` и SingleStream log summary — действительно FPGA/current source архив; 12,230138ms p90 вычисляется из12230138ns и не является LinQ H1M performance. Pinned archive https://github.com/mlcommons/inference_results_v0.7/tree/89260c7a0bb2bb86f4adaf1d88e0307162eb602b/closed/IVATech .

## Реестр обработки после W2

Этот раздел зарезервирован для сборщика. На момент написания второй волны ещё нет; ни один пробел не объявлен закрытым будущим экспериментом. Исходные замечания K001–K020 выше сохраняются неизменными; здесь добавляются отдельные строки с W2 result/F/S/Q/E и итоговым состоянием.


## Фактические dispositions после завершения W2 — добавлено сборщиком

Дата:23.10.2026, после W2-A…M. Исходные K001–K020 и формулировки W2 выше не переписывались. Это результат обработки двух волн, не финальная проверка отчётов. Стабильные E/R и owners: [_WORK/AUTHOR_HANDOFF.md](_WORK/AUTHOR_HANDOFF.md); local → global: [_WORK/ID_MAP.md](_WORK/ID_MAP.md). ActualCPU/model/helper границы: [F333](RAW_FACTS.md#f333). Источник каждого F указан в карточке; для удобства рядом добавлены основные S.

<a id="k001-w2"></a>
### K001 — остался открытым; область уточнена

- Что найдено и изменило исходную картину: W2-A/L reconfirmed publicdocs/gatedsoftware; noactualgrant/authenticatedlisting. Useractualsignup не сообщён; нельзясчитать download/device выданными.
- Факты/источники: [F198](RAW_FACTS.md#f198), [F200](RAW_FACTS.md#f200), [F302](RAW_FACTS.md#f302), [F309](RAW_FACTS.md#f309); [S019](SOURCES.md#s019), [S037](SOURCES.md#s037), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002), [S003](SOURCES.md#s003), [S035](SOURCES.md#s035), [S001](SOURCES.md#s001), [S034](SOURCES.md#s034).
- Остаток: [Q001](OPEN_QUESTIONS.md#q001), [Q002](OPEN_QUESTIONS.md#q002). Плановые проверки/маршруты: E001, E015. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k002-w2"></a>
### K002 — остался открытым; version axes разделены

- Что найдено и изменило исходную картину: W2-A/G/H/B получили source/metadata, ноне modernbundle. CPU-only compile остаётсяпроверяемойгипотезой; current guide необъявлен obsolete.
- Факты/источники: [F203](RAW_FACTS.md#f203), [F204](RAW_FACTS.md#f204), [F209](RAW_FACTS.md#f209), [F210](RAW_FACTS.md#f210), [F262](RAW_FACTS.md#f262), [F329](RAW_FACTS.md#f329); [S065](SOURCES.md#s065), [S033](SOURCES.md#s033), [S019](SOURCES.md#s019), [S113](SOURCES.md#s113), [S003](SOURCES.md#s003), [S037](SOURCES.md#s037), [S014](SOURCES.md#s014), [S002](SOURCES.md#s002).
- Остаток: [Q002](OPEN_QUESTIONS.md#q002), [Q006](OPEN_QUESTIONS.md#q006), [Q007](OPEN_QUESTIONS.md#q007). Плановые проверки/маршруты: E001, E007, E008. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k003-w2"></a>
### K003 — уточнена область; две подозреваемые ошибки опровергнуты

- Что найдено и изменило исходную картину: UpstreamTF2.14.1имеет graph_util.import_graph_def; None возвратдопустимдля Session default graph. Остаются convertertuple/GraphDef/namespace/names/compilecall. PDFbytes/images/end_to_endsource не получены; plaintextremoteclaim не visual proof.
- Факты/источники: [F211](RAW_FACTS.md#f211), [F212](RAW_FACTS.md#f212), [F213](RAW_FACTS.md#f213), [F215](RAW_FACTS.md#f215), [F216](RAW_FACTS.md#f216), [F217](RAW_FACTS.md#f217), [F218](RAW_FACTS.md#f218), [F219](RAW_FACTS.md#f219); [S030](SOURCES.md#s030), [S033](SOURCES.md#s033), [S118](SOURCES.md#s118), [S117](SOURCES.md#s117), [S115](SOURCES.md#s115), [S116](SOURCES.md#s116), [S119](SOURCES.md#s119), [S120](SOURCES.md#s120).
- Остаток: [Q010](OPEN_QUESTIONS.md#q010), [Q031](OPEN_QUESTIONS.md#q031). Плановые проверки/маршруты: E004, E019. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k004-w2"></a>
### K004 — остался открытым; source/bytes/standard границы уточнены

- Что найдено и изменило исходную картину: VersionedUltralytics/YOLO5/ONNXsources разделили DFL/decode/noNMS, shapeinput patch и attrs. ActualLinQparser/opset/lowering нет; неделать source-derivednodes за inventoryabsentbytes.
- Факты/источники: [F220](RAW_FACTS.md#f220), [F221](RAW_FACTS.md#f221), [F223](RAW_FACTS.md#f223), [F224](RAW_FACTS.md#f224), [F228](RAW_FACTS.md#f228), [F230](RAW_FACTS.md#f230), [F232](RAW_FACTS.md#f232), [F328](RAW_FACTS.md#f328); [S055](SOURCES.md#s055), [S048](SOURCES.md#s048), [S122](SOURCES.md#s122), [S123](SOURCES.md#s123), [S128](SOURCES.md#s128), [S129](SOURCES.md#s129), [S130](SOURCES.md#s130), [S121](SOURCES.md#s121).
- Остаток: [Q008](OPEN_QUESTIONS.md#q008), [Q009](OPEN_QUESTIONS.md#q009). Плановые проверки/маршруты: E002, E004. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k005-w2"></a>
### K005 — остался открытым; shortlist уточнён

- Что найдено и изменило исходную картину: Fullauthorhistory/source и thesisabstract не закрыли custom route. v8source-detailed, classic5svendor-matched,11matchedsample условноравноправны;5su не classic5s;11OBB не horizontalPPE.
- Факты/источники: [F233](RAW_FACTS.md#f233), [F234](RAW_FACTS.md#f234), [F235](RAW_FACTS.md#f235), [F236](RAW_FACTS.md#f236), [F242](RAW_FACTS.md#f242), [F330](RAW_FACTS.md#f330); [S133](SOURCES.md#s133), [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S135](SOURCES.md#s135), [S134](SOURCES.md#s134), [S002](SOURCES.md#s002), [S140](SOURCES.md#s140), [S136](SOURCES.md#s136).
- Остаток: [Q020](OPEN_QUESTIONS.md#q020), [Q034](OPEN_QUESTIONS.md#q034). Плановые проверки/маршруты: E002, E004, E007, E009, E011. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k006-w2"></a>
### K006 — закрыт новым доказательством как source defect/spec; исправленный adapter ещё не проверен

- Что найдено и изменило исходную картину: W2-D versionedNMS и actualshapehelper доказали COCO84/85heuristicfailnc1/2/3,85objectnessmisinterpretation, axisambiguity, A6shortcut, map/output/importdefects. Спецификация patch дана, productionfix/modelparity неисполнены.
- Факты/источники: [F237](RAW_FACTS.md#f237), [F238](RAW_FACTS.md#f238), [F239](RAW_FACTS.md#f239), [F240](RAW_FACTS.md#f240), [F241](RAW_FACTS.md#f241), [F242](RAW_FACTS.md#f242); [S137](SOURCES.md#s137), [S138](SOURCES.md#s138), [S139](SOURCES.md#s139), [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S141](SOURCES.md#s141), [S133](SOURCES.md#s133), [S134](SOURCES.md#s134).
- Остаток: [Q003](OPEN_QUESTIONS.md#q003), [Q020](OPEN_QUESTIONS.md#q020). Плановые проверки/маршруты: E003. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k007-w2"></a>
### K007 — обнаружено конкретное противоречие рецептов; vendor identity открыт

- Что найдено и изменило исходную картину: ActualModel ZooONNX/weights13kernels+finalbiasesmatch, но fineanchors1,2,3vsDarknet0,1,2, embeddedNMS.6/.5/max20, geometry и batch разные. ORTCPUb1success, b2Squeezefail; strict actual export и vendor binary не получены.
- Факты/источники: [F243](RAW_FACTS.md#f243), [F244](RAW_FACTS.md#f244), [F245](RAW_FACTS.md#f245), [F246](RAW_FACTS.md#f246), [F247](RAW_FACTS.md#f247), [F248](RAW_FACTS.md#f248), [F249](RAW_FACTS.md#f249), [F251](RAW_FACTS.md#f251), [F333](RAW_FACTS.md#f333); [S142](SOURCES.md#s142), [S143](SOURCES.md#s143), [S144](SOURCES.md#s144), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147), [S148](SOURCES.md#s148), [S149](SOURCES.md#s149).
- Остаток: [Q019](OPEN_QUESTIONS.md#q019). Плановые проверки/маршруты: E002, E009, E010. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k008-w2"></a>
### K008 — остался открытым; эксперимент и риск effective parameter локализованы

- Что найдено и изменило исходную картину: Summary несохраняет requested/effectiveP/retry; calibrate TypeError retry можетскрывать internal error. Weights-only неопровергнут; thresholdschema/save-load/numericaldetails/QAT/QDQunknown.
- Факты/источники: [F252](RAW_FACTS.md#f252), [F253](RAW_FACTS.md#f253), [F254](RAW_FACTS.md#f254), [F255](RAW_FACTS.md#f255), [F260](RAW_FACTS.md#f260), [F261](RAW_FACTS.md#f261); [S030](SOURCES.md#s030), [S048](SOURCES.md#s048), [S154](SOURCES.md#s154), [S155](SOURCES.md#s155), [S089](SOURCES.md#s089), [S156](SOURCES.md#s156), [S019](SOURCES.md#s019), [S063](SOURCES.md#s063).
- Остаток: [Q011](OPEN_QUESTIONS.md#q011), [Q012](OPEN_QUESTIONS.md#q012), [Q013](OPEN_QUESTIONS.md#q013). Плановые проверки/маршруты: E005, E006, E011. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k009-w2"></a>
### K009 — уточнена область; современный numerical/native contract открыт

- Что найдено и изменило исходную картину: Pointeruint8/NumPyview не dequantization; RAWfilekind и mode независимы, allocation по fileflag; oldcodecfields есть, формулынет. Native FULL placement и raw↔user golden не получены.
- Факты/источники: [F256](RAW_FACTS.md#f256), [F257](RAW_FACTS.md#f257), [F258](RAW_FACTS.md#f258), [F263](RAW_FACTS.md#f263), [F264](RAW_FACTS.md#f264), [F265](RAW_FACTS.md#f265), [F292](RAW_FACTS.md#f292); [S063](SOURCES.md#s063), [S030](SOURCES.md#s030), [S048](SOURCES.md#s048), [S065](SOURCES.md#s065), [S158](SOURCES.md#s158).
- Остаток: [Q014](OPEN_QUESTIONS.md#q014), [Q018](OPEN_QUESTIONS.md#q018). Плановые проверки/маршруты: E008, E010. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k010-w2"></a>
### K010 — частично закрыт SKU evidence; остальные конфликты/actual mapping открыты

- Что найдено и изменило исходную картину: HP01=16GB, HP02=32GB прямодокументированы; catalog generic16GB под 02 остаётся. Gen2manuals/presentationvsGen3family, active/passive необъясняют power. Parallel code этореплики; four/devlabel не cardmapping; singlegraphpoolingunknown.
- Факты/источники: [F271](RAW_FACTS.md#f271), [F272](RAW_FACTS.md#f272), [F273](RAW_FACTS.md#f273), [F274](RAW_FACTS.md#f274), [F275](RAW_FACTS.md#f275), [F276](RAW_FACTS.md#f276), [F277](RAW_FACTS.md#f277), [F278](RAW_FACTS.md#f278), [F279](RAW_FACTS.md#f279), [F280](RAW_FACTS.md#f280); [S019](SOURCES.md#s019), [S161](SOURCES.md#s161), [S021](SOURCES.md#s021), [S162](SOURCES.md#s162), [S023](SOURCES.md#s023), [S039](SOURCES.md#s039), [S025](SOURCES.md#s025), [S033](SOURCES.md#s033).
- Остаток: [Q016](OPEN_QUESTIONS.md#q016), [Q017](OPEN_QUESTIONS.md#q017), [Q033](OPEN_QUESTIONS.md#q033). Плановые проверки/маршруты: E008, E013, E020. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k011-w2"></a>
### K011 — остался открытым; альтернативы и знаменатели уточнены

- Что найдено и изменило исходную картину: Originalvisual/modernlogs нет; units985.72/128.90ms неисправлены. PinnedMLCommonspolicy разделяет scenarios; new parallel script суммирует rates, непросто N×baseline, носвязьс slideHPQ неустановлена.
- Факты/источники: [F281](RAW_FACTS.md#f281), [F282](RAW_FACTS.md#f282), [F283](RAW_FACTS.md#f283), [F284](RAW_FACTS.md#f284), [F285](RAW_FACTS.md#f285), [F286](RAW_FACTS.md#f286), [F331](RAW_FACTS.md#f331); [S033](SOURCES.md#s033), [S165](SOURCES.md#s165), [S044](SOURCES.md#s044), [S017](SOURCES.md#s017), [S076](SOURCES.md#s076), [S077](SOURCES.md#s077).
- Остаток: [Q023](OPEN_QUESTIONS.md#q023), [Q031](OPEN_QUESTIONS.md#q031), [Q032](OPEN_QUESTIONS.md#q032). Плановые проверки/маршруты: E012, E019. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k012-w2"></a>
### K012 — уточнена область; чрезмерный dangling вывод потерял основание

- Что найдено и изменило исходную картину: MockCPython3.11.9/NumPy2.4.2: outputviewretainPython-ownedbacking; nocopy не useafterfree. Mapping/unknown-name validation есть; dtype/noncontiguous/missinginput неотвергнутыстарым Python. Exceptiondestroymockomission подтверждён, modernfix/nativefailureunknown.
- Факты/источники: [F262](RAW_FACTS.md#f262), [F263](RAW_FACTS.md#f263), [F264](RAW_FACTS.md#f264), [F266](RAW_FACTS.md#f266), [F267](RAW_FACTS.md#f267), [F268](RAW_FACTS.md#f268), [F269](RAW_FACTS.md#f269), [F270](RAW_FACTS.md#f270); [S064](SOURCES.md#s064), [S157](SOURCES.md#s157), [S082](SOURCES.md#s082), [S019](SOURCES.md#s019), [S159](SOURCES.md#s159), [S065](SOURCES.md#s065), [S158](SOURCES.md#s158), [S160](SOURCES.md#s160).
- Остаток: [Q014](OPEN_QUESTIONS.md#q014), [Q015](OPEN_QUESTIONS.md#q015). Плановые проверки/маршруты: E008, E016. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k013-w2"></a>
### K013 — остался открытым; evidence protocol уточнён

- Что найдено и изменило исходную картину: Currentprofiler/manual/report/coverageguarantee не получены. Oldavg/maxaccumulated и README/source mismatch; disable_static_checker не strict. Предусмотрены SSH/service-onlylineage+completion+accepted witness безвыдуманного CLI/attestationrequirement.
- Факты/источники: [F287](RAW_FACTS.md#f287), [F288](RAW_FACTS.md#f288), [F289](RAW_FACTS.md#f289), [F290](RAW_FACTS.md#f290), [F291](RAW_FACTS.md#f291), [F292](RAW_FACTS.md#f292), [F293](RAW_FACTS.md#f293), [F294](RAW_FACTS.md#f294); [S026](SOURCES.md#s026), [S166](SOURCES.md#s166), [S167](SOURCES.md#s167), [S168](SOURCES.md#s168), [S169](SOURCES.md#s169), [S063](SOURCES.md#s063), [S075](SOURCES.md#s075), [S019](SOURCES.md#s019).
- Остаток: [Q005](OPEN_QUESTIONS.md#q005), [Q021](OPEN_QUESTIONS.md#q021), [Q022](OPEN_QUESTIONS.md#q022). Плановые проверки/маршруты: E009, E012. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k014-w2"></a>
### K014 — остался открытым actual contract; SSH mandatory assumption потеряло значение

- Что найдено и изменило исходную картину: W2-L conditionalcustomservice может быть достаточенпри updates/rawoutputs/quotas/evidence. Shell самнегарантия network/lifecycle/compiler. Нового officialonboarding/API нет.
- Факты/источники: [F302](RAW_FACTS.md#f302), [F309](RAW_FACTS.md#f309), [F312](RAW_FACTS.md#f312), [F313](RAW_FACTS.md#f313); [S035](SOURCES.md#s035), [S001](SOURCES.md#s001), [S034](SOURCES.md#s034), [S003](SOURCES.md#s003), [S014](SOURCES.md#s014), [S030](SOURCES.md#s030), [S026](SOURCES.md#s026), [S103](SOURCES.md#s103).
- Остаток: [Q001](OPEN_QUESTIONS.md#q001), [Q003](OPEN_QUESTIONS.md#q003), [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005). Плановые проверки/маршруты: E015. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k015-w2"></a>
### K015 — уточнена область; modern recovery/cancel открыт

- Что найдено и изменило исходную картину: Historical thread test15.0.24 и async14.7source существуют, нопоследний callbackunchecked/timeoutnone,8threadsTODOmismatch/noassert. Process per device не constraint, anyexception не mandatoryrestart. Native error recovery current нет.
- Факты/источники: [F311](RAW_FACTS.md#f311), [F316](RAW_FACTS.md#f316), [F317](RAW_FACTS.md#f317), [F318](RAW_FACTS.md#f318), [F319](RAW_FACTS.md#f319), [F320](RAW_FACTS.md#f320), [F321](RAW_FACTS.md#f321), [F323](RAW_FACTS.md#f323), [F324](RAW_FACTS.md#f324), [F325](RAW_FACTS.md#f325), [F326](RAW_FACTS.md#f326); [S063](SOURCES.md#s063), [S171](SOURCES.md#s171), [S065](SOURCES.md#s065), [S169](SOURCES.md#s169), [S019](SOURCES.md#s019), [S003](SOURCES.md#s003), [S064](SOURCES.md#s064), [S074](SOURCES.md#s074).
- Остаток: [Q015](OPEN_QUESTIONS.md#q015), [Q024](OPEN_QUESTIONS.md#q024), [Q025](OPEN_QUESTIONS.md#q025), [Q028](OPEN_QUESTIONS.md#q028). Плановые проверки/маршруты: E016, E017. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k016-w2"></a>
### K016 — уточнена область; версия исправлена; matching PPE build открыт

- Что найдено и изменило исходную картину: Page-separateddoubletext показывает 0.1.3+p10, не 0.1.310; visual/registry не получены. Guide прямоназывает LinqTPU, поэтому genericunnamedhypothesis частичноопровергнута. H1M/PPE/ПАКОТПБ imageidentity неустановлена; videonotviewed.
- Факты/источники: [F295](RAW_FACTS.md#f295), [F296](RAW_FACTS.md#f296), [F297](RAW_FACTS.md#f297), [F298](RAW_FACTS.md#f298), [F300](RAW_FACTS.md#f300), [F301](RAW_FACTS.md#f301), [F327](RAW_FACTS.md#f327); [S103](SOURCES.md#s103), [S105](SOURCES.md#s105), [S102](SOURCES.md#s102), [S104](SOURCES.md#s104), [S106](SOURCES.md#s106).
- Остаток: [Q027](OPEN_QUESTIONS.md#q027), [Q031](OPEN_QUESTIONS.md#q031). Плановые проверки/маршруты: E018, E019. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k017-w2"></a>
### K017 — остался открытым actual video budget; архитектурная граница уточнена

- Что найдено и изменило исходную картину: Optionalcodec/encode неустанавливает LinQHdecode; HXvideoRK3588scope. IVAjob500ms/10s не NNlatency; bounded queue/timestamps/fairness—наша policy. Actualpayload/network/CPU/decoderunknown.
- Факты/источники: [F298](RAW_FACTS.md#f298), [F299](RAW_FACTS.md#f299), [F312](RAW_FACTS.md#f312), [F313](RAW_FACTS.md#f313), [F332](RAW_FACTS.md#f332); [S103](SOURCES.md#s103), [S104](SOURCES.md#s104), [S035](SOURCES.md#s035), [S030](SOURCES.md#s030), [S063](SOURCES.md#s063), [S171](SOURCES.md#s171).
- Остаток: [Q004](OPEN_QUESTIONS.md#q004), [Q023](OPEN_QUESTIONS.md#q023), [Q030](OPEN_QUESTIONS.md#q030). Плановые проверки/маршруты: E012, E014. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k018-w2"></a>
### K018 — закрыт как требование нормализации provenance; независимые modern logs не появились

- Что найдено и изменило исходную картину: CanonicalSURL/version и W1/W2aliases сведены, source-code/reported/actualCPU/mock раздельны. RepeatedAST не hardwarecorroboration; Model Zoo/HF одна LFSlineage; thesispriorbench неновый run; новые upstreamsources не LinQ experiments.
- Факты/источники: [F233](RAW_FACTS.md#f233), [F236](RAW_FACTS.md#f236), [F244](RAW_FACTS.md#f244), [F284](RAW_FACTS.md#f284), [F285](RAW_FACTS.md#f285), [F286](RAW_FACTS.md#f286), [F333](RAW_FACTS.md#f333); [S133](SOURCES.md#s133), [S049](SOURCES.md#s049), [S060](SOURCES.md#s060), [S136](SOURCES.md#s136), [S143](SOURCES.md#s143), [S144](SOURCES.md#s144), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146).
- Остаток: [Q034](OPEN_QUESTIONS.md#q034). Плановые проверки/маршруты: E002, E009, E012. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k019-w2"></a>
### K019 — частично закрыт LICENSE evidence; actual supply rights открыты

- Что найдено и изменило исходную картину: Actualiva_applications11.0.1MITLICENSE сильнее UNKNOWNmetadata; bindings license unknown, Model ZooMIT/Apacheconflict сохранён. IVA CVcommercialcost не grant и notexecutionban. SDK/image/weights/.tpu teamredistribution неизвестны.
- Факты/источники: [F203](RAW_FACTS.md#f203), [F205](RAW_FACTS.md#f205), [F250](RAW_FACTS.md#f250), [F300](RAW_FACTS.md#f300); [S065](SOURCES.md#s065), [S090](SOURCES.md#s090), [S145](SOURCES.md#s145), [S146](SOURCES.md#s146), [S147](SOURCES.md#s147), [S148](SOURCES.md#s148), [S149](SOURCES.md#s149), [S150](SOURCES.md#s150).
- Остаток: [Q026](OPEN_QUESTIONS.md#q026), [Q035](OPEN_QUESTIONS.md#q035). Плановые проверки/маршруты: E001. Закрытие source/spec замечания не означает исполненный будущий эксперимент.

<a id="k020-w2"></a>
### K020 — закрыт как handoff/design task; эксперименты остаются будущими

- Что найдено и изменило исходную картину: Назначеныединые20E/8R/35Q,5functionalowners, shared model/data/goldenmanifest, stop/go ипределы proof. Vendorknown-good/TLMoptional; CPU/SDK/device/organizerdependencies явны. Практические LinQ результатынеобъявленыизплана.
- Факты/источники: [F261](RAW_FACTS.md#f261), [F312](RAW_FACTS.md#f312), [F313](RAW_FACTS.md#f313), [F326](RAW_FACTS.md#f326), [F329](RAW_FACTS.md#f329), [F330](RAW_FACTS.md#f330), [F333](RAW_FACTS.md#f333); [S019](SOURCES.md#s019), [S030](SOURCES.md#s030), [S048](SOURCES.md#s048), [S154](SOURCES.md#s154), [S155](SOURCES.md#s155), [S063](SOURCES.md#s063), [S089](SOURCES.md#s089), [S156](SOURCES.md#s156).
- Остаток: [Q001](OPEN_QUESTIONS.md#q001), [Q002](OPEN_QUESTIONS.md#q002), [Q003](OPEN_QUESTIONS.md#q003), [Q004](OPEN_QUESTIONS.md#q004), [Q005](OPEN_QUESTIONS.md#q005). Плановые проверки/маршруты: E001–E020, R001–R008. Закрытие source/spec замечания не означает исполненный будущий эксперимент.
