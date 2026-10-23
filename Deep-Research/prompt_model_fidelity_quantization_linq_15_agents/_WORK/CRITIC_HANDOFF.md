# Передача независимого критика

Дата: 2026-10-23, MSK. Полный исходный текст критики: [../CRITIC.md](../CRITIC.md). Прочитаны оба задания, PLAN/RUN_STATE/CASE_NOTES и все15 W1; дополнительный просмотр сохранённых primary code/manual extraction. Новых сетевых запросов, моделей, SDK, GPU и субагентов не было. Контекст критика независимый; позиция root не задавалась как обязательный вывод.

## Вывод для root

W1 достаточна по общим механизмам fidelity, provenance/splits, decoder/geometry, precision, small objects/pose, tracking/events и трём сценариям доступа. Повторять эти обзоры не нужно. Нужны семь адресных W2: version seams; ONNX→TF identity и цельный model contract; effective quantization/QAT consumer; количественные primary CV measurement cards; реальное содержание LinQ published results/runtime evidence; два запасных export маршрута; small-data uncertainty и acceptance record.

P0: K001/002/004/005 — до больших training/QAT и выбора target recipe. K010/011 — до claim о принятом качестве и реальном исполнении. K006/007/008/009 — P1, меняют обоснование выбора и силу результата. K003 — P1, предотвращает склейку несовместимых примеров.

## Mapping и самодостаточные задания Medium

Все задачи: gpt-6.1-sol / medium по договору; root назначает фактическими параметрами. Собственный результат `_WORK/W2_XX.md`, snapshots по необходимости в `_WORK/MATERIALS_W2_XX/`. Читать конкретные K и указанные W1. Не запускать SDK/модели/сервер, не арендовать GPU и не связываться с внешними людьми. Новые сведения — только по первичным code/docs/author measurements с точной версией, локатором и условиями. Завершение определяется новым основанием или ограничивающим условием; повтор W1 без нового результата не закрывает K.

| Результат | K-ID | Предмет, source targets и stop condition |
|---|---|---|
| W2_01.md | K001 | Разрешить ровно швы guide2025/публичных packages/2026 example: Python, quantize/calibrate, save/from_quantized_model, target/defaults, DEFAULT/STAGING vsO1/O5. Target: оригинал Framework_manual_H1.pdf, официальные редакции/release notes/package metadata. При PDF bytes визуально проверить спорные страницы. Таблица proven interface/unknown compatibility. Не найден matched release→точный запрос bundle; не искать бесконечно закрытый SDK. |
| W2_02.md | K002,K003 | Один цельный Ultralytics8.3.230 Detect/Pose безNMS contract с exact head/export/preprocess/NMS/inverse source; сравнить существенные helpers v8.3.0 из W1-05. Затем ONNX tensor+port+role→TF→QM/TPU mapping по реальному `onnx_to_tf`/`onnx_direct` поставщику, без подмены одноимённым converter. Target: pinned Ultralytics code, guide, pinned build_yolov8_program.py и доступный primary importer metadata/source. Stop: связанный контракт, G01–04 version delta, importer-specific UNKNOWN и минимальный probe. |
| W2_03.md | K004,K005 | Установить объект LinQ percentile и наличие consumer для QDQ/encodings/QAT/mixed precision. Target: version-specific official API/source/sample; W1-14 guide и build code; ORT/NNCF/AIMET только для различения арифметики. Отдельно ограниченно разрешить ORT auto_mixed_precision docs/code CPU/GPU конфликт exact tag+ORT version. Stop: confirmed/unknown/contradicted capability matrix и proof перед GPU; отсутствие public evidence не назвать отсутствием функции. |
| W2_04.md | K006 |2–4 primary measurement cards CV PTQ/recovery: Wu arXiv2004.09602, BRECQ arXiv2102.05426/source и один релевантный official detection/pose deployment benchmark при наличии. Сохранить model/dataset/split/input/batch/precision/exclusions/hardware/software/metric/float→PTQ→recovered/cost, неизвестное явно. Минимум одно ограничивающее/negative condition. Stop: реальные reported outcomes помогают выбору; pose INT8 evidence при ненахождении остаётся UNKNOWN, DARK не substitute. |
| W2_05.md | K007,K011 | Проверить, какие LinQ результаты реально опубликованы: pinned RUN_SCENARIO result paths, авторские release/results/logs, vendor presentation сноски. Не считать expected MLPerf VALID raw measured result; не приписывать TinyYOLO3 результат self-build YOLOv8. Target: pinned repo/author artifacts, official PDF, pytpu runtime code/docs по установленным версиям. Проверить completion barrier, FULL/RAW user IO scope, warmup/batch denominator в чужих numbers. Stop: evidence card на каждый пригодный результат, оставшиеся runtime-native неизвестные и matched-trace запрос; никаких запусков benchmark. |
| W2_06.md | K008 | Два exact export route cards как запасной выбор: один detector вне обычного YOLO Detect, один pose (например RT-DETR и выбранный RTMPose/SimCC). Target: official model config/source/export docs, version-matched MMDeploy если применим. Указать operators/shapes/outputs/decoder/preprocess/quant tooling/negative conditions и LinQ evidence level. Сопоставить с W2-02 и vendor-ready branch W2-05. Stop: следующий test и причина prefer/reject; имя семейства не поддержка LinQ. Не делать весь model_stack заново. |
| W2_07.md | K009,K010 | Quantify силу0 ошибок на малом corpus через корректные one-sided binomial/zero-count rate bounds при явных независимых предпосылках; cluster/selection ограничения сохранить. Target: SciPy primary CI docs/source, NIST или иной первичный statistical source; W1-12. Дать гипотетические аналитические расчёты без нормативов кейса. Один acceptance record detection/pose/tracking/events с datum/decision/not-exposed разделением; сценарии small roster/insufficient rare holdout/catalog without source. Stop: допустимый claim и адресат каждого пробела; actual thresholds/GT решает команда. |

## Как оценивать поступивший W2

Для каждого K сохранить новый факт, source pointer, изменившийся вывод, остаточный риск и disposition: closed; scope narrowed; contradicted; remains open; superseded. Не переписывать исходную критику. Открытый SDK вопрос после адресного поиска является конкретным Q с владельцем/артефактом, а не основанием ещё раз пересказать vendor home page.

Важные ограничения для синтеза:

- Не смешивать documentation, static code, author plan/status, published measurement и our test. Ни одна W1 модель/SDK/device проверка не выполнена.
- K006 просит сохранить **чужие числа с их контекстом**, не прогноз LinQ. Неполный hardware field не повод удалить сильное measured accuracy evidence, если граница ясно записана.
- K007 не отрицает successful vendor run; требует не повышать авторский план/expected status до прочитанного raw результата. COCO image adapter и server video runner — разные scope.
- K010 не требует найти универсальный процент деградации. Нужны принимаемые человеком budgets и реальные data/GT; WEB этого не заменит.
- Для конечных A–F достаточно W1 основы плюс W2 уточнения. Свести десятки локальных E в5–15 общих E-ID, добавить ONNX→TF import и режим not-exposed/confounded. Все E остаются PROPOSED, пока не было реального запуска.
- В финальной шестёрке не создавать дополнительный финальный аудиторский файл или роль. CRITIC — история первой критики и W2 disposition.

Редактировались только `CRITIC.md` и этот handoff. Дальше root составляет индивидуальные W2 prompts и запускает согласованную вторую волну; сборщик затем объединяет реестры и дописывает disposition.
