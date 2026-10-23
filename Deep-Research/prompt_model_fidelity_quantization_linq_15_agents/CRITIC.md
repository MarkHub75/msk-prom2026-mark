# Независимая критика первой волны model_fidelity_quantization

Критик получил отдельное начало без разговорной истории оркестратора. Прочитаны полностью оба входных задания, `_WORK/PLAN.md`, `_WORK/RUN_STATE.md`, `_WORK/CASE_NOTES.md` и все `_WORK/W1_01.md`…`W1_15.md`; дополнительно прочитаны относящиеся к замечаниям сохранённые исходники и извлечение руководства H1. Новых сетевых материалов, запусков моделей/SDK и субагентов в этой роли не было. Время чтения установлено clock: 2026-10-23 19:45:36–19:49:32 UTC, то есть 22:45:36–22:49:32 MSK. Это этап критики W1, **не финальный аудит ещё не написанных отчётов**.

Фактический статус: первая волна содержит 15 самостоятельных результатов, 12 general / 3 LinQ. Все модельные и аппаратные E-проверки остаются NOT_RUN. Полный кейс существует; его содержание в данном проходе принято по явно атрибутированному визуальному наблюдению root в CASE_NOTES, без заявления о собственном повторном просмотре PDF. Выбранного checkpoint, размеченного corpus, SDK и предоставленного сервера нет.

## Что уже достаточно установлено

Первая волна содержательна. Повторять пятнадцать обзоров ради независимости не требуется.

- **Источник ошибки отделён от названия преобразования.** W1-01/02/03 обосновали различие между working source baseline, подготовленной export-моделью, валидным ONNX и численной/задачной эквивалентностью. Особенно полезны контрпримеры ONNX reference, полученного от самого export, `verify=True` без жёсткого quality gate и `onnxsim(check_n=0)` без inference comparison.
- **Decoder и геометрия покрыты конкретным кодом.** W1-04/05 дают custom nc, objectness, DFL, pose extras, NMS, layout, odd letterbox, crop/affine и timestamp fixtures. Ограничения стороннего linq-cv-bench нельзя «лечить QAT». Повторно доказывать опечатку, COCO84/85 и COCO mapping не нужно.
- **Численные и задачные критерии не смешаны.** W1-06/09/12 объясняют clipping конвертера, фактический dtype, накопление, QDQ boundaries, survival bias совпавших detections и отличие tensor parity от независимого GT. Универсального `atol`, процента mAP или минимального FPS не выдумано.
- **Данные и события покрыты сильнее обычного export research.** W1-01/07/10/11/12 разделяют calibration/tuning/test, camera/incident lineage, маленькие признаки, owner association, visibility, PTS, fixed-dt trackers, causal/offline inference, дедупликацию и false alerts per camera-hour. Аналитические примеры не названы измерениями. Потребность в новых реальных данных не закрывается ещё одной статьёй.
- **LinQ не подменён другим backend.** W1-13/14/15 обнаружили документированный ONNX→TF→QM→compiler→TPU путь, но честно не называют его выполненным переносом наших весов. Старые PyPI API, guide 2025, сторонний код 2026 и версии vendor benchmark не объединены в выдуманный установленный SDK. Полный SDK, ограниченная VM и готовый сервис рассмотрены раздельно.
- **Независимость происхождения в основном сохранена.** Несколько чтений одного guide, файлов одного repo и повторных vendor pages не объявлены независимыми экспериментами. Root notes о кейсе остаются одной цепочкой наблюдения. Это нужно сохранить при назначении общих S-ID.

Главный недостаток W1 — не недостаток общих предупреждений. Между ними ещё нет нескольких замкнутых **версионных маршрутов и карточек измерений**, на основании которых команда выберет конкретный следующий шаг. Часть пробелов можно сузить во второй волне; реальное качество, предоставленный ABI и целевые бюджеты останутся вопросами к артефактам и команде.

## Как читать замечания

P0 — блокирует дорогую работу или утверждение о переносе/исполнении; P1 — существенно меняет выбор метода либо силу вывода. Типы закрытия: **WEB** — новый первичный документ/код/опубликованный результат; **ARTIFACT** — фактический model/SDK/data/access; **DECISION** — явное решение команды; **TEST** — отдельная разрешённая практическая проверка. WEB может сузить ARTIFACT-вопрос, но не заменяет его.

Ниже зафиксирована **исходная критика**. Сборщик должен дописать к K-ID результаты W2 и disposition, сохранив этот текст и дату. Незаполненный disposition сейчас означает «вторая волна ещё не рассмотрена».

## K001 — Нет доказанного соответствия между поколениями LinQ API

**Приоритет / закрытие:** P0; WEB частично, окончательно ARTIFACT+TEST.

**Проблема и локатор.** [W1-13](./_WORK/W1_13.md), F01/F06/F07/F19 и «Какие поколения нельзя смешивать»; [W1-14](./_WORK/W1_14.md), F11/F12. Найдены конкретные разрывы: Python3.8 против3.11, classmethod quantize против RegularModel.calibrate, разные save/from_quantized_model, DEFAULT/STAGING против O1/O5, противоречащие platform defaults в извлечённом guide. Они правильно названы неизвестными, но пока не установлено, какие различия относятся к редакции документа, реальному переходу API или ошибке текстового извлечения. Нельзя выбирать интерфейс из наиболее удобной строки разных материалов.

**Что меняет для команды.** Обученный custom artifact может оказаться неразвёртываемым, а «исправление» SDK через retries — менять само преобразование. Нужен один compatibility bundle до QAT и обучения больших кандидатов. При этом отсутствие публичной таблицы не означает несовместимость.

**Недостающее доказательство.** Version-matched manual/release/example либо точный официальный текст о переходе; для фактической среды — hashes wheels/native/runtime/driver, signatures и known-good artifact. Публичный benchmark Framework2026.8.43/Runtime16.18.6 не является этим bundle.

**Узкое W2 / source targets / завершение.** **W2-01**: проверить именно перечисленные швы по оригиналу Framework_manual_H1.pdf, доступным официальным редакциям/release notes и package metadata. При возможности получить PDF bytes визуально проверить только спорные страницы7–11/19–21 и титул; не объявлять text extraction визуальным чтением. Выход — таблица «утверждение→редакция→доказанный интерфейс→неизвестная совместимость», без новой общей брошюры. Завершение: каждое расхождение разрешено первичным локатором либо превращено в точный пункт запроса bundle; после этого прекратить общий поиск закрытого SDK.

**Disposition W2:** PENDING.

## K002 — Самый важный дополнительный importer-переход ещё не имеет семантического контракта

**Приоритет / закрытие:** P0; WEB частично, ARTIFACT+TEST обязательно.

**Проблема и локатор.** W1-13, F02/F09/F10/F12, карта ONNX→TF; W1-14 E04; W1-02/03 описывают PyTorch↔ONNX существенно подробнее, чем **ONNX↔TF через конкретный `onnx_to_tf`**. Сохранённый `build_yolov8_program.py` сначала переписывает input metadata, затем перебирает converter/simplification, отображает имена и пробует несколько output names. Успешный RegularModel constructor не подтверждает ни тождество выбранного тензора, ни сохранение layout и graph cut. Имя `onnx_to_tf` нельзя автоматически отождествить с любым популярным проектом onnx-tf/onnx2tf.

**Что меняет для команды.** PyTorch↔ORT PASS и плохой LinQ output могут разделяться ошибкой import ещё до quantizer. Если выбрать другой одноимённый tensor/порт либо потерять второй output, сравнение «PTQ ухудшил» причинно неверно. Сравнение только конечных боксов не восстановит это различие.

**Недостающее доказательство.** Идентичность поставщика и версии importer; точная семантика mapping, входов/выходов и возможных transpose; список преобразованных operators/attributes; float TF outputs на том же canonical input. Понадобится либо mapping семантических выходов, либо честная отметка о необозримой границе.

**Узкое W2 / source targets / завершение.** **W2-02**: проследить этот importer по официальному guide, фактическим import lines и доступным metadata/source `onnx_direct`/`tpu_framework`, не устанавливая SDK и не подменяя его сторонним converter. Составить admission contract: ONNX tensor name+port+shape+role→TF tensor name+port+shape+role→QM/TPU descriptor; вынести принудительную static-shape правку отдельным parent artifact. Привязать к обычному Detect и Pose выбранной закреплённой реализации, включая все outputs. Завершение: найден первичный контракт и минимальные probes либо указано, какие поля можно получить только из выданного SDK; неподтверждённые операции остаются UNKNOWN, а не UNSUPPORTED.

**Disposition W2:** PENDING.

## K003 — Полезные YOLO факты взяты из разных версий; целостный worked example ещё не собран

**Приоритет / закрытие:** P1; WEB, затем ARTIFACT+TEST.

**Проблема и локатор.** W1-02/04 закрепляют Ultralytics8.3.230; W1-05 — preprocess/inverse v8.3.0; W1-11 — оригинальные ByteTrack/BoT-SORT. Сторонний LinQ repo не pin Ultralytics/torch. Каждый локальный вывод ограничен версией корректно, но будущий читатель может склеить «стандартный YOLO pipeline» из этих фрагментов. Особо опасны `.pt`-dependent rectangle, расположение NMS между файлами, nc inference, `shape[-1]==6`, inverse geometry и используемая tracker integration.

**Что меняет для команды.** Это может создать новый decoder/preprocess mismatch уже при следовании отчёту. Нужен один полностью прослеживаемый иллюстративный маршрут; он не должен становиться без основания рекомендацией поставить эту версию на сервер.

**Недостающее доказательство.** Совпадающие tag/commit для head, export helper, preparation/fusion, predictor, LetterBox, inverse helpers, NMS и конфигурации выходов. Изменения между v8.3.0 и8.3.230, влияющие на конкретные W1 fixtures, пока не сведены.

**Узкое W2 / source targets / завершение.** **W2-02**: по закреплённому Ultralytics8.3.230 проследить один обычный non-end2end Detect и один Pose без NMS: вход→подготовка→export→decoded pre-NMS output→общий NMS→inverse. Проверить, какие из G01–G04 W1-05 сохраняются, а какие требуют новой версии expected result. Custom nc=1/2/3 и kpt_shape задаются manifest, не эвристикой. Выход — один version-coherent contract и короткий diff, не повтор W1-04. Завершение: каждый используемый helper имеет тот же immutable commit либо явно обозначенную внешнюю зависимость; установленная версия LinQ adapter всё ещё требует environment manifest.

**Disposition W2:** PENDING.

## K004 — LinQ percentile нельзя включать в общий calibration sweep до выяснения объекта параметра

**Приоритет / закрытие:** P0 для sweep; WEB частично, ARTIFACT+TEST.

**Проблема и локатор.** W1-07 «Проверенные реализации» и матрица B; W1-14 F02/F03/E02/E03; W1-13 F11. Общие ORT activation histogram percentile и NNCF per-sample quantile уже хорошо различены. Однако guide LinQ описывает percentile через **весовые коэффициенты**, а сторонний RegularModel.calibrate имеет иной API и blanket TypeError retry. Ни одинаковое имя, ни разные requested CLI values не устанавливают несколько разных activation-calibration опытов.

**Что меняет для команды.** Можно потратить время на мнимый sweep, неверно объяснить улучшение rare-class recall либо выбрать диапазоны, которые вообще не были применены. Сначала effective config, затем экспериментальный фактор.

**Недостающее доказательство.** Формула/scope параметра конкретного release, supported numeric domain, место применения до/после weight quantization, actual thresholds/encodings, лог успешного fresh-model вызова без скрытого retry. Изменение activation thresholds само по себе не доказывает прямой activation percentile — оно может быть следствием изменённых весов.

**Узкое W2 / source targets / завершение.** **W2-03**: адресно искать определение percentile в официальном API/исходнике именно LinQ и сравнить его с прочитанными версиями ORT/NNCF. Выдать таблицу «weights/activations/оба/не установлено; requested/effective; доказательство». Если текущая реализация закрыта, закончить точным SDK-вопросом и двухфакторным micrograph plan из E03, без нового перебора общих calibration статей. Завершение: нельзя интерпретировать параметр сверх найденного определения; окончательный effect остаётся TEST.

**Disposition W2:** PENDING.

## K005 — QAT/mixed precision описаны предметно, но у целевого compiler нет доказанного consumer численного контракта

**Приоритет / закрытие:** P0 до расхода GPU; WEB частично, ARTIFACT+TEST.

**Проблема и локатор.** W1-08 F01/F04/F11/F15, downstream export contract; W1-09 F10–F13 и FP island discussion; W1-14 Q14-03. Наличие ONNX QDQ, AIMET encodings, FP32 block или обученных scales не устанавливает, что LinQ их импортирует и сохраняет. При float-import+recalibration AdaRound может оптимизировать другую сетку; FP island после уже округлённого feature map не возвращает потерянную информацию. Это честно признано W1, но остаётся главным условием применимости «следующего метода спасения».

**Что меняет для команды.** До установления consumer нельзя обосновать ни дополнительный GPU trial, ни обещание selective precision. Нужна развилка «сохраняется explicit contract / можно симулировать native quantizer / остаются только поддерживаемый PTQ и смена модели».

**Недостающее доказательство.** Для реального SDK — допустимые W/A/bias/accumulator types, rounding/saturation, scale/zero-point/axis, QDQ/sidecar preservation, supported precision boundaries и placement. Для ORT auto-mixed path отдельно остаётся конкретное docs/code расхождение CPU/GPU из W1-09 F10; это не блокирует ручную диагностику и не должно превращаться в утверждение, что mixed precision вообще невозможна.

**Узкое W2 / source targets / завершение.** **W2-03**: искать только vendor-specific QAT/imported-encodings/mixed-precision path и ограничивающие условия; результаты иных производителей использовать как описание требования, не поддержку LinQ. Для локального альтернативного инструмента разрешить конфликт W1-09 на exact package tag/release и ORT EP/kernel version по первичному code/docs, без запуска/установки. Выход — capability table confirmed/unknown/contradicted с одним минимальным proof перед обучением. Завершение: найден реальный consumer либо выбор остаётся условным и вынесен в вопрос инженеру; не требовать ещё статей QAT для закрытия SDK неизвестности.

**Disposition W2:** PENDING.

## K006 — Сравнение методов лишено большей части доступных количественных опубликованных результатов

**Приоритет / закрытие:** P1; WEB.

**Проблема и локатор.** W1-07 F10 намеренно не переносит численные результаты paper; W1-08 F07/F14 сохраняет setup/итерации BRECQ, но не outcome; W1-09 HAWQ не использует benchmark gains; W1-10 не переносит SAHI gains. Ограничения верны, однако из них не следует, что числа нужно исключить даже как **чужие измерения с контекстом**. Сейчас «expected benefit (reported/estimated/tested)» рискует стать почти полностью качественным. Особенно мало прямого measurement evidence для CV PTQ/QAT и pose; сценарные аналитические примеры его не заменяют.

**Что меняет для команды.** Нельзя оценить, был ли метод в похожей CV задаче полезен лишь при4бит, восстанавливал ли8бит, какие операторы оставлялись float и сколько engineering/training работы он потребовал. Нужна поддержка выбора, без обещания тех же gains на LinQ.

**Недостающее доказательство.** Две–четыре сильные measurement cards: model/checkpoint, dataset/split, input/batch, W/A precision и exclusions, hardware/software, metric scale, float/PTQ/recovered outcomes, calibration/training cost и недостающие поля. «Аппаратное время не указано» допустимо, если так и написано; нельзя требовать полного идеального артефакта и выбрасывать остальные валидные данные.

**Узкое W2 / source targets / завершение.** **W2-04**: вернуться к авторским результатам Wu et al. arXiv2004.09602 и BRECQ arXiv2102.05426/official repo; дополнить одним первичным detection/pose результатом official deployment benchmark/model card, если он содержит действительное сравнение precision. Проверить negative/limiting result, например dependence на bitwidth, activation exclusions или model family. Зафиксировать абсолютные метрики и разности в их исходной шкале; source independence и source-vs-our measurement. Завершение:2–4 контекстные карточки меняют выбор метода; если прямого pose quantization сравнения не найдено, оно остаётся локализованным UNKNOWN, а DARK coordinate discretisation не выдаётся за INT8 evidence.

**Disposition W2:** PENDING.

## K007 — Публичный LinQ код и план запуска пока сильнее доказаны, чем опубликованный результат конкретного переноса

**Приоритет / закрытие:** P1 для research, P0 для заявления о выполненном переносе; WEB, затем TEST.

**Проблема и локатор.** W1-13 F15/F17, «Статусы доказательств»; W1-15 F04/F05; сохранённый RUN_SCENARIO §3.4 пишет final valid vendor TinyYOLO3 path, но также `MLPerf performance is expected to be VALID`. Это авторский сценарий/статус, а не автоматически прочитанный raw result. Self-build YOLOv8 source и его defects не являются ни успешным измерением YOLOv8, ни опровержением всей LinQ detection. Официальная презентация даёт иной источник — vendor-reported benchmark, без установленного custom-checkpoint fidelity.

**Что меняет для команды.** Возможны две симметричные ошибки: повысить наличие скрипта до «проверенный перенос YOLOv8», либо отвергнуть полезный vendor TinyYOLO3 опыт из-за ошибки другого скрипта. Нужен точный объект каждого опубликованного результата, особенно baseline identity.

**Недостающее доказательство.** Доступные result JSON/accuracy output/MLPerf logs/config/model hash или явная фиксация их отсутствия; dataset и decoder equality для source-target comparison; отличие performance-only от accuracy runs. Перепечатки одной таблицы остаются одной цепочкой.

**Узкое W2 / source targets / завершение.** **W2-05**: проследить указанные RUN_SCENARIO result paths в pinned linq-cv-bench и возможных связанных авторских release/result artifacts; отдельно открыть первичную таблицу vendor presentation с её сносками при доступных bytes/рендере. Для каждого результата дать «actually reported / merely proposed / artifact unavailable», исходную метрику и полный доступный контекст. Не запускать benchmark, не рисовать LinQ vs NVIDIA сравнение. Завершение: как минимум выяснено, что именно публичный материал измерил; отсутствие файлов не превращается в отсутствие функции/успеха, но ограничивает доказательную силу.

**Disposition W2:** PENDING.

## K008 — Смена архитектуры ещё не имеет достаточно конкретного запасного export-маршрута

**Приоритет / закрытие:** P1; WEB, затем ARTIFACT+TEST.

**Проблема и локатор.** W1-04 хорошо различает FasterRCNN, DETR/RT-DETR и SimCC; W1-08 дерево, шаг8 предлагает более совместимую архитектуру; W1-13 F20 не подтверждает их LinQ support. Но для альтернатив пока нет столь же цельного маршрута export/output/quantization как для Ultralytics Detect. «Сменить модель» может оказаться переходом к ROI/custom ops/attention/crop codec, которые сложнее исходной проблемы.

**Что меняет для команды.** При stop-loss нужен проверяемый запасной путь и критерий отказа, а не расширенный список брендов. Большее float качество или официальный ONNX export не гарантируют меньший риск LinQ import.

**Недостающее доказательство.** Два компактных, закреплённых route cards из разных семейств: исходная model/config identity, export tool и версии, output signature, ключевые operator/shape constraints, точка decoder/pose crop, PTQ/QAT tooling scope, реально подтверждённый уровень LinQ. Нужны также отрицательные условия, при которых route не является запасным.

**Узкое W2 / source targets / завершение.** **W2-06**: выбрать один detector вне обычного YOLO Detect и один pose-путь из уже релевантных W1 кандидатов; например RT-DETR и MMPose RTMPose/SimCC. По официальному source/config/export documentation (для MMPose — соответствующему MMDeploy пути, если он реально относится к выбранной конфигурации) собрать два exact route cards. Не обещать применимость любого SimCC codec ко всем RTMPose. Сравнить со static Ultralytics reference из W2-02 и vendor-ready model branch из W2-05. Завершение: по каждой альтернативе есть следующая проверка и причина предпочесть/отвергнуть её; LinQ UNKNOWN допускается и не маскируется общей export support.

**Disposition W2:** PENDING.

## K009 — Для «ошибок не увидели» не хватает простого количественного ограничения силы вывода

**Приоритет / закрытие:** P1; WEB+методический вывод, затем DATA/TEST.

**Проблема и локатор.** W1-12 раздел «Парная uncertainty» справедливо предупреждает о `[0,0]` bootstrap при нулевых ошибках, few clusters, undefined draws и неэквивалентности `p>0.05`. Но не даёт рабочей альтернативы для типичного hackathon outcome: все немногочисленные события прошли, новых FN или false alerts не зарегистрировано. В результате инженер либо остановится на HOLD без понимания требуемых данных, либо придумает «достаточно20 клипов».

**Что меняет для команды.** Нужно отличать narrow regression PASS на фиксированном roster от утверждения о recall/risk на популяции. Число событий, независимых источников и negative exposure по-разному ограничивают возможный claim. Наращивание одинаковых кадров не решает задачу.

**Недостающее доказательство.** Применимые exact one-sided bounds для простого независимого event model и zero-count rate model, с явными предпосылками; почему эти формулы не годятся автоматически при camera/incident clustering, неоднородности и выборе winner на test. Отдельно — paired regressions, которые net Δrecall может компенсировать новыми TP.

**Узкое W2 / source targets / завершение.** **W2-07**: первичная документация SciPy binomial confidence intervals и NIST/первичный статистический источник для zero-count rate, плюс сохранённый clustered-design материал W1-12. Дать несколько **гипотетических аналитических** расчётов по числу независимых событий/exposure, без назначения нормативов кейса; отдельно показать новый miss vs gained TP. Завершение: читатель может назвать, что доказывает0 ошибок на его roster и какие данные нужны для более сильного утверждения; при неизвестной независимости остаётся descriptive/INCONCLUSIVE, а не фиктивный exact population CI.

**Disposition W2:** PENDING.

## K010 — Бюджеты качества и доступность GT являются решениями/артефактами, которые ещё один поиск не закроет

**Приоритет / закрытие:** P0 для финального acceptance, P1 для подготовки протокола; DECISION+ARTIFACT+TEST.

**Проблема и локатор.** W1-06/07/10/11/12 правильно откладывают δ, absolute floors/caps, critical roster, deadline, минимальную длительность события и достаточный GT. Однако много «PASS по согласованным thresholds» пока являются условной формой, не заполненным quality contract. Это не ошибка отсутствия универсальных констант; опасность возникает, если будущая сборка представит методическую таблицу как готовый допуск. Perfect parity слабого baseline тоже недопустима по safety claim.

**Что меняет для команды.** Нужен маленький конкретный пакет решений до выбора winner: какие сценарии поддерживаем, что можно наблюдать, что считаем одним эпизодом/actor, что обязано пройти smoke, какие абсолютные требования отдельно от сохранения исходной модели, и какую область вообще не оценили. Нужны независимые labels и continuous negatives, а не эталонные predictions вместо GT.

**Недостающее доказательство.** Принятые командой требования и реальные manifests/GT/права/источники. Публикации помогают выбрать форму метрики, но не цену пропуска на конкретной площадке. Заказчик может уточнить deadline; исследователь не вправе выдать найденное в другом benchmark число за официальный допуск.

**Узкое W2 / source targets / завершение.** **W2-07**: сформировать один заполняемый acceptance record для detection+pose+tracking+events, используя W1-12 и локальный кейс с.5/7/13/19, с отдельными полями team decision, datum missing, not exposed, measured. Добавить три сценария ограничений: малый фиксированный regression pack; независимый holdout с недостаточными rare positives; каталог готовых моделей без source checkpoint. Завершение — явная граница допустимого claim и адресат каждого незаполненного поля, а не придуманное численное PASS. Этот пункт окончательно закрывает команда после получения данных, не Medium web search.

**Disposition W2:** PENDING.

## K011 — Completion и FULL/RAW остаются version-specific; без них нельзя интерпретировать latency и численный output

**Приоритет / закрытие:** P0 для фактического запуска; WEB частично, ARTIFACT+TEST.

**Проблема и локатор.** W1-14 F06–F08 и W1-15 F01/F03/E03/E06. Guide описывает blocking sync, сторонний runner предпочитает `.run` при наличии, а исторический pytpu15 Python binding передаёт mode native. Само наличие `.run`, byte pointer и user_dtype не доказывает completion, quant arithmetic или placement PRE/POST. Наряду с этим W1-15 нашёл warmup/batch accounting defect. «Inference FPS» из такого wrapper нельзя без дополнительных условий сравнить с source end-to-end throughput или временем до уведомления.

**Что меняет для команды.** Можно измерить enqueue вместо inference, повторно rescale user-format output или посчитать не тот denominator. Это способно испортить и качество, и доказательство TPU, даже если модель корректно скомпилирована.

**Недостающее доказательство.** Версионный runtime contract `.run/.sync`, result readiness, mode PRE/RAW/POST/FULL, tensor descriptors и reset/error behavior; для реального job — связка artifact/session/device/input/completion/output. Device inventory и service label отдельно полезны, но не дают этот proof.

**Узкое W2 / source targets / завершение.** **W2-05**: проследить доступную первичную документацию/код pytpu15 и более новых официально доступных runtime examples только до предела раскрытого API; отдельно отметить, чего Python binding не сообщает о native implementation. При анализе опубликованных timing logs из K007 проверить completion barrier, warmup в целых batches, completed real frames и named latency boundary. Выход — допустимые evidence levels для full SDK/restricted VM/catalog service и недостающий runtime artifact. Завершение: историческое поведение не переносится на выданный ABI; если актуальный contract закрыт, вопрос закрывается только matched manual+completed smoke trace, без бесконечного поиска.

**Disposition W2:** PENDING.

## Предлагаемая вторая волна: семь содержательных поручений

| W2 | K-ID | Основное новое основание / ограничение | Режим завершения |
|---|---|---|---|
| W2-01 | K001 | Разрешение конкретных guide/API/version seams; визуальная сверка спорного извлечения при доступном оригинале | WEB либо точный matched-bundle ARTIFACT запрос |
| W2-02 | K002, K003 | Целостный закреплённый Detect/Pose контракт и identity на ONNX→TF→target границах | WEB contract; непубличный importer остаётся ARTIFACT+TEST |
| W2-03 | K004, K005 | Объект LinQ percentile и consumer quantization contract; границы QAT/mixed precision | WEB при наличии, иначе ограниченное UNKNOWN с proof plan |
| W2-04 | K006 |2–4 контекстные primary CV quantization/recovery measurement cards и отрицательное условие | Новый опубликованный measurement evidence |
| W2-05 | K007, K011 | Реальное содержание LinQ published results, completion/IO/timing contracts и сила device evidence | WEB result/code/trace provenance; actual service остаётся ARTIFACT+TEST |
| W2-06 | K008 | Два конкретных запасных export route cards, с рисками import и условиями отказа | WEB, без декларации LinQ support |
| W2-07 | K009, K010 | Конечная сила small-data/zero-failure вывода и заполняемый quality contract | Первичное statistical основание+аналитический пример; решения остаются за командой |

Ни одно поручение не должно повторять общий W1 обзор, устанавливать SDK, запускать модели, арендовать GPU, входить на сервер или связываться с инженерами. Вопрос инженеру означает подготовленный текст в файлах. Если новый первичный материал не найден после адресной проверки, это полезный результат только с конкретной границей неизвестности; подтверждение отсутствия функции требует отдельного положительного основания.

## Что не следует отправлять в ещё один сетевой круг

1. **Checkpoint/config/source inference и custom class semantics.** Получить реальные артефакты; названия семейств их не заменяют. Без source допускается качество чёрного ящика, но не checkpoint fidelity.
2. **SDK/environment/access grant и binary compatibility.** Публичные версии служат вопросами, не фактической конфигурацией сервера. После W2-01/03/05 нужен matched bundle и unchanged known-good artifact, затем разрешённый smoke.
3. **Лицензированные real clips, independent GT, calibration/tuning/test groups, critical events и negative exposure.** Без них недостижимы наши quality numbers. Synthetic decoder/geometry fixtures полезны, но не являются заводской оценкой.
4. **Цена ошибок, supported scenarios, deadline, δ/floors/caps и unknown policy.** Это решение команды/постановщика. Устное1FPS не отменяет фазовые пропуски и оперативность из кейса.
5. **Фактические TPU placement, numerical output, FPS, latency, память и часы QAT.** Только конкретный выполненный тест. Published claims остаются published claims, а расчёт по pilot — ещё не выполненный pilot.

## Покрытие A–F и указания сборке

На этапе W1 все A–F имеют достаточную содержательную основу для синтеза. Это **готовность материала**, а не выполненная программа тестов.

| Артефакт | Достаточная основа W1 | Что необходимо сохранить в итоговой сборке |
|---|---|---|
| A Fidelity ladder |01/02/03/06/12/13/14 | Отдельный ONNX→TF import; adjacent и source→final deltas; UNAVAILABLE/confounded edge вместо выдуманного FP target |
| B Симптом→причина→проверка |02/03/04/05/06/10/12 | Разделить output semantics, geometry, float runtime, quantizer, compiler и downstream; один симптом не является доказательством одной причины |
| C Golden pack |01/05/07/10/11/12 | Канонические tensors+геометрия+PTS; tiny/visibility/owner slices; continuous negative exposure; независимый GT и лицензии; статус NOT_COLLECTED |
| D Decision tree/stop-loss |03/07/08/09/10/12 | Не переходить к QAT до локализации; ограниченный rescue budget; откат полного model+preprocess+decoder+rules bundle; альтернативы по K008 |
| E LinQ tests |12 E01–06;13 E01–07;14 E01–06;15 E01–07 | Свести многочисленные локальные E в **5–15 общих E-ID**, без создания десятков дублирующих обязательств. Для каждого указать decision, requirements, role-based sample IDs, stage pair, observable evidence, PASS/FAIL/HOLD и cannot-prove. Имена будущих samples — спецификация, не существующие файлы |
| F Защита |12/15; кейс5/7/13 | Одни исходные клипы, связанный artifact/device/completion trace, raw/canonical outputs, GT и плохие примеры, раздельные quality/timing/device claims. Никаких выдуманных сравнений с NVIDIA |

Нужен один общий реестр S/F/K/Q/E, в котором repeated manual/repo sources дедуплицированы, а разные версии одного файла различимы. Живые docs с неизвестной датой не нужно удалять из-за формальной неполноты; numeric или API совет должен иметь доступный scope. В таблице методов отделить reported benefit от hypothesis и NOT_RUN. В model matrix отделить model family listing, documented route, readable source, published run и our test.

На диске требуется ровно шесть итоговых Markdown из задания; CRITIC.md — один из них. Остальные промежуточные материалы остаются в `_WORK/`. Отсутствие остальных пяти конечных файлов сейчас ожидаемо: сборщик/автор/редактор/сжиматель ещё не отработали. Дополнительная финальная проверочная роль для закрытия этой критики не требуется.

## Первичный порядок действий после W2

Результаты W2 должны дать более узкие условия выбора, а не искусственный PASS. Первыми остаются: получить access+matched bundle+known-good model; заморозить source/model/data contract; выполнить input/output admission и unchanged-device smoke; проверить float export/import, затем quantization/compiler boundary; после этого independent task/event replay с фактическим schedule. Дорогой QAT идёт только при доказанной нужде и передаваемом numerical contract.


<a id="w2-dispositions"></a>
## Дополнение сборщика после W2 — исходная критика выше сохранена

Дата: 2026-10-23, Europe/Moscow. Исходные PENDING в тексте выше — историческое состояние критика **до** W2, не текущий итог. Полный неизменённый оригинал сохранён в [_WORK/CRITIC_W1_ORIGINAL.md](_WORK/CRITIC_W1_ORIGINAL.md). Ни одно documentary/source закрытие ниже не device test. Все E001–E012 [PROPOSED/UNRUN](OPEN_QUESTIONS.md#experiment-program); actual installed bundle/model/GT/grant и measurements отсутствуют. Новых сетевых доказательств сборщик не получал. Идентификаторы источников/фактов нормализованы в [ID_MAP](_WORK/ID_MAP.md).

<a id="K001"></a>
### K001 — narrowed; actual compatibility open

**Primary S pointers:** [S133](SOURCES.md#S133), [S150](SOURCES.md#S150), [S151](SOURCES.md#S151), [S139](SOURCES.md#S139).

**Новый результат:** [_WORK/W2_01.md](_WORK/W2_01.md), F01–F09, fresh guide extraction, PyPI metadata и проверенный sdist15.0.24. [F203](RAW_FACTS.md#F203)/[F204](RAW_FACTS.md#F204) показывают Device/Program/Inference и lazy `/usr/lib/libtpu.2.so`; stale PyPI long_description не определяет source API. [F198](RAW_FACTS.md#F198) установил документальную линию-03 после-02; wheel mapping не появился. [F199](RAW_FACTS.md#F199)/[F200](RAW_FACTS.md#F200)/[F201](RAW_FACTS.md#F201)/[F202](RAW_FACTS.md#F202) разнесли calibrate/quantize/save/return/platform/preset seams.

**Изменившийся вывод:** частное предположение «публичный pytpu обязательно только старые классы» superseded; несовместимость поколений не доказана. Не утверждать single-return против tuple по одному присваиванию и O1=DEFAULT/O5=STAGING по imports. **Остаток:** actual Framework/compiler/native compatibility и platform discrepancy неизвестны, PDF bytes/visual verification не получены. Закрытие Q002/Q005 через matched bundle/manual и E003/E007; не ещё один общий web round.

<a id="K002"></a>
### K002 — narrowed; importer semantics open

**Primary S pointers:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139), [S160](SOURCES.md#S160), [S161](SOURCES.md#S161).

**Новый результат:** [_WORK/W2_02.md](_WORK/W2_02.md), [F212](RAW_FACTS.md#F212)/[F213](RAW_FACTS.md#F213) и S12–S16. Guide конкретно называет `onnx_direct.onnx_to_tf` и tuple Graph/mapping; client source assumptions выявлены до value/producer/port. Составлен explicit ONNX→TF→QM/TPU admission и два identity/layout/multi-port probes. Exact importer search/PyPI404 не дали supplier implementation/version.

**Изменившийся вывод:** одноимённые onnx-tf/onnx2tf не замены; source→ORT PASS не локализует target PTQ. Static metadata modification, simplify retries, stripping port и first-output selection — самостоятельные риски client. **Остаток:** callable/distribution/build/mapping/float-output contract не выданы; Q004/Q005/Q015, E005 затем actual same-tensor float gate. Если float boundary not exposed после grant, import+quantization confounded; это не closed.

<a id="K003"></a>
### K003 — closed в source-coherent worked-contract scope

**Primary S pointers:** [S019](SOURCES.md#S019), [S153](SOURCES.md#S153), [S045](SOURCES.md#S045), [S159](SOURCES.md#S159).

**Новый результат:** [_WORK/W2_02.md](_WORK/W2_02.md), [F206](RAW_FACTS.md#F206)/[F207](RAW_FACTS.md#F207)/[F208](RAW_FACTS.md#F208)/[F209](RAW_FACTS.md#F209)/[F210](RAW_FACTS.md#F210)/[F211](RAW_FACTS.md#F211), S01–S11. Один immutable Ultralytics389b87f8cb9dbf2f31be8b70a94a3e47e11693db связывает preparation/export/head/preprocess/NMS/inverse/Results; Detect и Pose имеют по одному no-NMS output0. G01/G02 image geometry сохранена; G03 wrapper rect/dynamic matrix обновлена; G04 Pose box без round и no low-conf xy zeroing вопреки stale docstrings.

**Изменившийся вывод:** автор может описать цельный пример, не склеивая8.3.0/8.3.230 и original tracker. **Остаток:** weights/custom class/skeleton/external dependency lock/actual installed adapter unknown; это documentary closed, не tested pipeline. Q003/Q010; E002/E004/E005. NMS branch/ties/side effects требуют actual frozen fixtures.

<a id="K004"></a>
### K004 — narrowed; effective percentile open

**Primary S pointers:** [S133](SOURCES.md#S133), [S139](SOURCES.md#S139), [S134](SOURCES.md#S134).

**Новый результат:** [_WORK/W2_03.md](_WORK/W2_03.md), [F214](RAW_FACTS.md#F214)/[F215](RAW_FACTS.md#F215)/[F216](RAW_FACTS.md#F216), S01–S03. Literal guide связывает percentile с weights/default100; formula/tails/current scope не установлены. Fresh pinned client hash подтвердил blanket TypeError retry и отсутствие effective config. Bounded vendor search не дал current numerical definition.

**Изменившийся вывод:** не включать LinQ CLI X в activation histogram sweep по аналогии ORT/NNCF. Предложен полный2×2 P×calibration distributions с fresh models; activation thresholds могут измениться опосредованно через weights. **Остаток:** Q006/E006 — exact SDK definition+dump/implementation или supported frozen-weight intervention, не угадывание значения. Нет evidence функции не равно absence; отсутствие effect на insensitive fixture не proof ignored.

<a id="K005"></a>
### K005 — narrowed; LinQ consumer open, частный ORT categorical вывод contradicted

**Primary S pointers:** [S133](SOURCES.md#S133), [S101](SOURCES.md#S101), [S162](SOURCES.md#S162), [S164](SOURCES.md#S164), [S165](SOURCES.md#S165).

**Новый результат:** [_WORK/W2_03.md](_WORK/W2_03.md), [F217](RAW_FACTS.md#F217)/[F218](RAW_FACTS.md#F218)/[F219](RAW_FACTS.md#F219)/[F220](RAW_FACTS.md#F220)/[F221](RAW_FACTS.md#F221)/[F222](RAW_FACTS.md#F222)/[F223](RAW_FACTS.md#F223)/[F224](RAW_FACTS.md#F224) и [F225](RAW_FACTS.md#F225)/[F226](RAW_FACTS.md#F226)/[F227](RAW_FACTS.md#F227)/[F228](RAW_FACTS.md#F228)/[F229](RAW_FACTS.md#F229). Capability matrix не нашла доказанного LinQ QDQ/encodings/QAT/mixed consumer. Найден отдельный `auto_convert_mixed_precision_model_path(...,provider,...)` в converter1.16.0; ModelProto path hardcodedCPU, ORT1.23.2 kernel/cast source объясняет FP16 graph с FP32 CPU compute для части узлов.

**Изменившийся вывод:** universal GPU-only/CPU impossible inference слишком сильна; наличие GPU не переключает ModelProto API. Converter не pin ORT, live docs не release contract, совместная execution не проверена. **Остаток:** LinQ route A external preserve/B native simulator/C native PTQ выбирается по Q007/E007 before training; local ORT tooling Q019/E011 optional. Parser/compile acceptance не arithmetic preservation и CPU validation не CUDA/LinQ proof.

<a id="K006"></a>
### K006 — closed для published quantitative support

**Primary S pointers:** [S086](SOURCES.md#S086), [S093](SOURCES.md#S093), [S167](SOURCES.md#S167), [S168](SOURCES.md#S168).

**Новый результат:** [_WORK/W2_04.md](_WORK/W2_04.md), [F230](RAW_FACTS.md#F230)/[F231](RAW_FACTS.md#F231)/[F232](RAW_FACTS.md#F232)/[F233](RAW_FACTS.md#F233), S01–S05; полученные paper PDF Tables визуально сверены, official tagged benchmark rows прочитаны. Wu b0 top1 76.85→72.06→76.35partial или отдельная76.95QAT; BRECQ FasterRCNN-R50 COCO38.55float/38.29W4A8/38.54W8A8/34.23W2A8; MMDeploy YOLOX40.5PyTorch/40.3TRT-FP32,FP16/29.3INT8; ncnn S-ViPNAS pose.687→.683 и Wholebody.459→.445.

**Изменившийся вывод:** методы имеют прямое количественное CV/pose основание с limiting outcomes, не только общие caveats. Условия/metric scales/calibration/cost/exclusions/unknown setup сохранены в RAW; разные methods не склеены в один sequential run. **Остаток:** никакого нашего LinQ benefit, benchmark/reproduction/GPU hour estimate это не закрывает. Actual target compatibility Q007, industrial data/GT Q013 и E007/E008/E011 остаются отдельно.

<a id="K007"></a>
### K007 — narrowed; raw author run/model identity open

**Primary S pointers:** [S140](SOURCES.md#S140), [S169](SOURCES.md#S169), [S170](SOURCES.md#S170), [S137](SOURCES.md#S137).

**Новый результат:** [_WORK/W2_05.md](_WORK/W2_05.md), [F234](RAW_FACTS.md#F234)/[F235](RAW_FACTS.md#F235)/[F236](RAW_FACTS.md#F236)/[F237](RAW_FACTS.md#F237) и S01–S08. Fresh complete pinned/main tree, releases=[],Actions0 в checked scope не содержат указанных JSON/logs; ignore rules объясняют possible local artifacts, не доказывают их existence. TinyYOLO3 author done/expected VALID отделён от self-build YOLOv8 route. Vendor presentation имеет отдельные numerical FPS/ms cards с setup16.18.6/2026.8.43 и unknown fidelity/IO/timing boundaries.

**Изменившийся вывод:** нельзя утверждать опубликованное measured successful custom YOLOv8 transfer из наличия scripts; нельзя отрицать vendor successful run из absence artifacts или дефекта другого runner. HPQ4×HP и latency равная не proof independent measurement,1000/FPS не восстанавливает скрытый latency scope. **Остаток:** Q018 raw results/model hashes/original PDF+methodology; visual table unverified. Наш E003/E008/E010 необходимы для собственных claims.

<a id="K008"></a>
### K008 — closed для двух source route cards; target fallback open

**Primary S pointers:** [S174](SOURCES.md#S174), [S175](SOURCES.md#S175), [S177](SOURCES.md#S177), [S180](SOURCES.md#S180), [S181](SOURCES.md#S181), [S182](SOURCES.md#S182).

**Новый результат:** [_WORK/W2_06.md](_WORK/W2_06.md), [F241](RAW_FACTS.md#F241)/[F242](RAW_FACTS.md#F242)/[F243](RAW_FACTS.md#F243)/[F244](RAW_FACTS.md#F244)/[F245](RAW_FACTS.md#F245), S01–S13. RT-DETR-l U8.3.230 static640/opset16/BNC300 requires internal GridSample/TopK/attention; RTMPose-m M1.3.2+D1.3.1 uses17×384/512 SimCC, host crop/argmax/inverse, GAU/ScaleNorm and two outputs. Найдены actual RTMCC rewrite, requirementsM1.0.0 vs new metadata seam, bypass flip-TTA, explicit proposed B1 static config.

**Изменившийся вывод:** “сменить архитектуру” теперь конкретная admission развилка с prefer/reject и точными blockers, а не claim более лёгкого LinQ route. **Остаток:** weights bytes/hashes/actual dependency lock/source export+target support/execution неизвестны. Q016/E011→E004/E005/E007/E008; source card closed не deployable supported fallback. При неподдержанном op без equivalent lowering остановить до QAT.

<a id="K009"></a>
### K009 — narrowed; методическая WEB-часть closed, population data open

**Primary S pointers:** [S184](SOURCES.md#S184), [S185](SOURCES.md#S185), [S186](SOURCES.md#S186), [S130](SOURCES.md#S130).

**Новый результат:** [_WORK/W2_07.md](_WORK/W2_07.md), [F246](RAW_FACTS.md#F246)/[F247](RAW_FACTS.md#F247)/[F248](RAW_FACTS.md#F248)/[F250](RAW_FACTS.md#F250) и S01–S05/S07. SciPy exact one-sided CP и NIST fixed-time HPP дают при zero misses `1−α^(1/n)` и zero false `−lnα/T`; разные endpoints/models. Аналитические examples/α vsα/2, selection/clustering/missingness и lost/gained paired table сохранены.

**Изменившийся вывод:** zero errors на finite fully-reviewed roster даёт узкий descriptive regression evidence; independent population bound только при declared iid/HPP sampling/frozen policy/complete follow-up.20iid positives с0miss не recall100 claim. **Остаток:** actual counts/exposure/design/independence и rare support не получены; Q013/Q014/E008/E009/E012. Кластеризация не чинится числом frames/произвольным n_eff/дегенеративным bootstrap. Formula не actual model measurement и не принятый норматив.

<a id="K010"></a>
### K010 — open для final acceptance; protocol preparation closed

**Primary S pointers:** [S003](SOURCES.md#S003), [S188](SOURCES.md#S188).

**Новый результат:** [_WORK/W2_07.md](_WORK/W2_07.md), [F249](RAW_FACTS.md#F249)/AR01 и три scenario claims, визуально перепроверены кейсс.5/7/13/19. Единая запись объединяет detection/pose/tracking/events/timing/device, owners и independent statuses TEAM_DECISION_PENDING/DATUM_MISSING/NOT_EXPOSED/MEASURED. Small debug roster/rare holdout/catalog without source cases имеют честные границы.

**Изменившийся вывод:** форма quality contract готова, missing inputs/решения конкретны; future interface unknown не уже NOT_EXPOSED, MEASURED none. **Остаток:** supported scenarios/deadline/δ/floors/caps/α/stop/multiplicity и GT/rights/lineage/actual runs выбирает/получает команда. Q012/Q013/Q014, E001/E008/E009/E010/E012. Нет универсального1%/1FPS и нельзя принять слабый baseline за fidelity.

<a id="K011"></a>
### K011 — narrowed; current native ABI/completion open

**Primary S pointers:** [S172](SOURCES.md#S172), [S173](SOURCES.md#S173), [S145](SOURCES.md#S145), [S133](SOURCES.md#S133).

**Новый результат:** [_WORK/W2_05.md](_WORK/W2_05.md), [F238](RAW_FACTS.md#F238)/[F239](RAW_FACTS.md#F239)/[F240](RAW_FACTS.md#F240) и S05–S10. Verified sdist дал sync→native run→read/status chain и Codec `tpu_tlm_is` dependency/descriptors. RAW mode не RAW program, byte pointer не INT8 numerical type, view не dequant. Python vendor direct adapter имеет measured-call-only scope и warmup boundary numerator/time mismatch; native MLPerf wrapper другой путь и слабый VALID predicate/possible stale logs.

**Изменившийся вывод:** historical exposed contract описан до native boundary; static timing analysis не actual benchmark и не дефект всех MLPerf/vendor numbers. Guide blocking sync не определяет `.run`, current timeout/reset/readiness/precision/PRE/POST placement. **Остаток:** Q008/Q009/Q011/Q018, matching manual/descriptors и correlated completed smoke E003/E007/E010. Без completion/device/clock mapping HOLD соответствующего claim; исторический wrapper не current ABI proof.

## Итог распределения закрытий

Три замечания закрыты в явно ограниченной documentary/source/published области: K003/K006/K008. Семь narrowed с оставшимся actual target/data условием: K001/K002/K004/K005/K007/K009/K011. K010 остаётся open для final acceptance. В K005 contradicted только слишком широкий ORT вывод; target capability не объявлена contradicted/absent. Ни один K не снят как not relevant, никаких device tests не выполнено. Следующие действия — получение конкретных артефактов/решений и отдельные разрешённые E, а не скрытая третья сетевая волна.
