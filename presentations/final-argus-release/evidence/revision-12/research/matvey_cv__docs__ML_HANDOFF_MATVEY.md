# Matvey → SafeWatch: выдача моделей

Проверено 24.10.2026 по `origin/main` **f6b5358afee60d1190f5b5e9decc77292b9087c9** и его `docs/ML_INTEGRATION.md`. Код приложения не изменён. Все изменения выдачи находятся в `matvey_cv`; main не коммитился и не пушился в этой задаче.

## 1. Что действительно готово

| Модель | Выдача | Что включает в SafeWatch | Что НЕ подтверждено |
|---|---|---|---|
| `matvey-pose-yolov8n@640-v1-acc5f51228b9` | Полный ONNX `[1,56,8400]`, TPU Split-Pose и CPU-хвост; local PASS | COCO17-признаки существующего `fall`, геометрии и привязки объектов; нужен основной COCO80 detector капитана | Новое размещение и запуск в SafeWatch на LinQ, промышленное качество |
| `matvey-helmet-yolov8n@640-v1-5c3af1f3b855` | ONNX `[1,6,8400]`, существующий TPU и identity-tail; local PASS | Объекты `helmet` / `no_helmet` как extra | **В приложении нет PPE-плагина**: автоматического события отсутствия каски не будет |

Это прежние обученные веса, а не новое улучшение. Четыре выхода Split-Pose собраны хвостом в правильном порядке `(x,y,confidence)` для каждой из 17 точек. Сигмоиды, DFL и координатный decode повторно не применяются. На одном одинаковом синтетическом float32-входе полный ONNX и head+tail дали **max abs error 0** у обеих моделей. Это ABI-проверка, не оценка качества или TPU-проверка.

Полные сведения с текущими SHA256: [инвентаризация](../ml/safewatch.inventory.json), [выдача и evidence](../ml/safewatch.delivery.json), [реестр](../ml/models.matvey.yaml), [минимальный pipeline override](../ml/pipeline.matvey.yaml), [маппинг классов](../ml/safewatch.class_map.json).

## 2. Инвентаризация и несовместимости

Проверены опубликованные `/workspace/artifacts/detection`, handoff/артефакты `/workspace/artifacts/training`, `/workspace/runs`; чужие worktree и процессы не изменялись. «Не найдено» ниже относится к этой области, а не означает, что никто больше ничего не обучает. Последние опубликованные training reports сообщают завершённые прогоны; действующий scheduler не подменяется этим снимком.

| Моя модель / результат | Фактический вход, классы, состояние | Требование приложения / действие |
|---|---|---|
| Helmet YOLOv8n DetectionModel | 640 RGB/NCHW; `helmet,bare_head`; веса `/workspace/artifacts/detection/helmet/weights.pt`; ONNX и O1/H1M TPU существуют | Только extra; `bare_head→no_helmet`. PPE-сценарий требует изменения приложения; как detector с nc2 запрещён |
| Pose YOLOv8n PoseModel | 640; `person`, COCO17; веса `/workspace/artifacts/detection/pose/weights.pt`, полный ONNX есть | Float full ONNX совместим с local. Старый mixed-output TPU отклонён из-за PTQ-confidence проблемы, его не выдаём |
| Split-Pose, те же веса | `/workspace/artifacts/detection/pose-split/weights.onnx`; четыре decoded выхода; `/workspace/artifacts/linq-sdk/pose-split-compile/model.tpu` | Добавлен concat/reshape-tail и полный ONNX. TPU-байты сохранены; новый бинарник не компилировался |
| Person-only Detect из Pose | Один класс `person`, preflight compatibility-only; `/workspace/artifacts/training/matvey_yolo_pilot_20261024/matvey_cpu_preflight_v4/matvey_person_detect_pretrained.pt` | **Не основной detector**: SafeWatch требует все 80 каналов COCO. Padding нулевыми каналами или переименование не выполняются |
| GMD TCN/MLP, четыре outer-fold head | `pose_window [1,24,74] → fall_logit [1,1]`; ONNX exported, TPU нет, единый production head не выбран | Это временные классификаторы, не YOLO. Нельзя превратить scalar logit в bbox записью реестра; нужен temporal classifier hook приложения |
| GMD fine-tune MLP | `matvey_gmd_finetune_v1/matvey_best.pt`; source-validation gain 0, rejected | Не публикуется как улучшенная модель и не подменяет baseline |
| RGB-MIL, обученный кандидат | `matvey_rgb_mil_gpu_fp32_v1/matvey_best.pt`; ONNX `matvey_rgb_core_export_v1/matvey_rgb_core.onnx`; `rgb_frame [1,3,320,320]→frame_logit [1,1]`, TPU нет | Host pooling + raw pose prior; source-validation-only improvement. Нужен classifier integration hook, в `pipeline.extra` сейчас не подходит |
| Огонь/дым, сигарета | Готовых bbox-checkpoint/ONNX/TPU в опубликованной области не найдено | Нужны отдельные extra с точными `fire`, `smoke`, `cigarette`; не выдаём за них RGB fall-classifier |
| Погрузчик/техника | Готового Matvey COCO80 fine-tune не найдено | Основной детектор сохраняет 80 COCO-классов; погрузчик — `truck`, ID7. `forklift` или `truck` в extra не участвует в трекинге техники |
| Привязь, груз, жилет | Соответствующих готовых bbox-моделей в опубликованной области не найдено | Нужны `no_harness` / `suspended_load` как extra. Позитивный `harness` не доказывает отсутствие привязи; жилет пока без PPE-плагина |
| Собственные восемь observation-модулей | Внутренние правила/`EventCandidate`, включая synthetic acceptance cases | Это код правил, не восемь обученных детекторов. SafeWatch использует свои плагины; этот слой не переносит и не подменяет архитектуру поведения |

Исходники экспорта уже были: `ml/detection/export.py` (CPU weights→static ONNX), `ml/linq/compile.py` (исторический SDK compiler). Новый слой **не заменяет** эти модели, training pipeline, детекции или правила поведения.

Старые демо `/workspace/artifacts/video-mvp/*` и `/workspace/artifacts/matvey-scenarios/*` содержат `ObservationBatch`/`EventMutation` JSONL, снимки и журналы; это **не** SafeWatch `FrameDetections`. Внешнего JSONL-импорта в SafeWatch нет. Repeated-image/synthetic сценарии помечены; их нельзя выдавать за реальные промышленные нарушения. Исторические реальные video/LinQ-прогоны сохранены отдельно, при этой выдаче не повторялись.

## 3. Капитану: подключение за 10 минут

Действия ниже выполняет владелец приложения в своей рабочей копии. Наш скрипт их на main/боевом сервере не выполняет.

1. Получить архив и проверить **SHA256 из `ml/safewatch.delivery.json → archive`**. Текущий архив находится вне Git в `/workspace/artifacts/safewatch-delivery/`. В нём только модели и малые handoff-файлы, без видео, секретов и Git-метаданных. Вложенный `MATVEY_MANIFEST.json` перечисляет относительные пути и хеши.
2. Распаковать в корень SafeWatch: пути начинаются с `models/matvey/`. Общие модели не перезаписываются: имена включают версию и content fingerprint. Не заменять целиком существующую папку `models/`.
3. **Добавить** обе записи из `ml/models.matvey.yaml` в список `models:` приложения. Не заменять существующие записи реестра. Если PPE не нужен, Helmet можно не добавлять и не активировать.
4. В `config/user.yaml` поставить только `pipeline.pose: matvey-pose-yolov8n@640-v1-acc5f51228b9` (готовый фрагмент `ml/pipeline.matvey.yaml`). Сохранить `pipeline.detector` капитана и уже подключённые extra. Списки extra заменяются целиком, не дополняются автоматически.
5. Для проверки без LinQ: `INFERENCE_BACKEND=local`, `SAFEWATCH_FAKE=0`; основной detector капитана тоже должен иметь доступный полный local ONNX. После согласованного перезапуска выполнить `uv run safewatch doctor`, затем `uv run safewatch eval <свой-reviewed-eval.yaml> --out <новая-папка>` или импорт видео через работающий сервер. Подробные Bash/PowerShell-команды — в контракте main.
6. Для настоящего LinQ нужен отдельный согласованный слот и размещение **наших** TPU-файлов под итоговыми именами из `linq_program`. До этого `backend-check` закономерно может сообщать отсутствующие программы. Наличие локального `.tpu` и старый успешный capture нового размещения не доказывают.
7. После загрузки и проверки ABI переключить backend на `linq`, явно выключить fake и выполнить один короткий последовательный прогон. Сохранить request/response ID, output/status и полную задержку; местоположение файлов и doctor не заменяют этот тест.

**Имена и общая инфраструктура:** локальные артефакты начинаются с `matvey_`. Стандартный `upload_program.py` приложения принудительно добавляет `mosprom_`; итоговые записи используют уникальные `mosprom_matvey_*`, как в принятом контракте. Он также использует staging `mosprom_work/`, а не `matvey/`. Поэтому он **не запускался** этой задачей: режим изоляции/слот согласует капитан. Никаких `--force`, перезаписи `baseline/`, общих `mosprom_*_cut_ap9999*`, чужих очередей или ядер. Рабочие папки ML остаются `matvey/`; VPN, SSH, маршруты и службы не меняются. Потоки CPU/ORT/OpenCV — 1; собственный разрешённый запрос — не более одного в полёте.

## 4. Как выпускать следующий checkpoint

Слой: `python -m ml.safewatch_delivery prepare`. Выходная папка должна быть **новой**; существующий bundle не изменяется. `--version` обязателен; к нему автоматически добавляется fingerprint ONNX, классов, роли, порогов и имеющегося TPU. При новой компиляции учитывается также хеш полученного бинарника. Это защищает от старого кэша SafeWatch.

Подготовить существующий manifest и ранее скомпилированный Split-Pose (CPU, без новых TPU/compile вызовов):

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' \
/workspace/.venv-cv-prepare/bin/python -m ml.safewatch_delivery prepare \
  --manifest /workspace/artifacts/detection/pose-split/manifest.json \
  --output /workspace/artifacts/safewatch-delivery/NEW-pose-release \
  --model-id matvey-pose-yolov8n --version 640-v2 --role pose \
  --compiled /workspace/artifacts/linq-sdk/pose-split-compile/model.tpu \
  --compile-report /workspace/artifacts/linq-sdk/pose-split-compile/compile-report.json
```

Новые доверенные YOLO-веса: вместо `--manifest` задать `--weights /path/to/best.pt`. Экспорт выполняется на CPU: static batch1, FP32, opset13, `nms=False`. Автоматического скачивания весов нет. `--role detector` проверяет полный порядок COCO80; `--role pose` требует `person` и COCO17; новые object-классы идут `--role extra`. Явный маппинг: `--class-map '{"flame":"fire"}'`; неизвестные/дублирующиеся классы и позитивное `harness→no_harness` отклоняются. Пороги: `--conf 0.1 --iou 0.45`.

Для будущей новой компиляции запускать тот же модуль из согласованного **SDK-окружения**, последовательно и с внешним лимитом времени:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES='' \
timeout 300 /workspace/.venvs/linq-sdk/bin/python -m ml.safewatch_delivery prepare \
  --manifest /path/to/new-export/manifest.json \
  --output /workspace/artifacts/safewatch-delivery/NEW-compiled-release \
  --model-id matvey-fire-yolov8n --version 640-v1 --role extra \
  --cut-at /model.22/dfl/conv/Conv_output_0,/model.22/Sigmoid_output_0 \
  --compile --calibration /path/to/calibration.npz \
  --calibration-manifest /path/to/calibration-provenance.json
```

Это **шаблон**, не существующая fire-модель и не автоматически выполненный эксперимент. Имена cut проверяются по конкретному графу; не переносить их на другую архитектуру по названию семейства. `calibration-provenance.json` должен явно содержать `split: train` или `calibration`, непустые `groups`, `calibration_allowed: true` и `sha256` NPZ. Validation/test для PTQ не допускаются. Сам пользовательский manifest не доказывает независимость групп — она проверяется до запуска.

SDK-ветка реализует conditioning → CPU calibration с `activation_percentile=99.99` → PTQ → batch1/O1/TPU_H1M. Неизвестные SDK-сигнатуры/имена выходов завершают выпуск ошибкой с сохранением отчёта, без молчаливого fallback. Новая SDK-ветка в этой задаче **не выполнялась**: нет нового calibration/compile/TPU-эксперимента. Для текущих двух моделей использованы неизменённые ранее скомпилированные TPU и проверены их хеши, lineage и имена/формы выходов.

Bundle содержит `models/matvey/.../{полный ONNX,head,tail,TPU при наличии}`, `models.matvey.yaml`, `user.matvey.yaml`, `MANIFEST.json`. Manifest различает local ABI, compile, remote placement, новый LinQ и качество. Без скомпилированной программы `linq_program: null`; такой выпуск предназначен только для local.

## 5. Что проверено в приложении

Изолированный detached worktree: `/tmp/safewatch-matvey-local`, исходники `origin/main` f6b5358a. Только временный реестр, временный `config/user.yaml` и игнорируемые бинарники; код, API, миграции и main-ветка не менялись. После прогона пользовательский конфиг удалён, реестр восстановлен. БД/видео/JSONL находятся вне Git в `/workspace/artifacts/safewatch-delivery/local-check-v1/`.

Вызваны настоящие CLI `python -m safewatch doctor` и `python -m safewatch eval ... --out ...` с `INFERENCE_BACKEND=local`, `SAFEWATCH_FAKE=0`, CPU/ORT threads1. Это те же команды, что `uv run safewatch doctor/eval`; интерпретатор и `PYTHONPATH` явно привязаны к тестовому окружению/checkout. Код капитана не патчился.

- Doctor: exit0; все три ONNX найдены.
- Eval: exit0, примерно **2.83 с** полного вызова на 5 кадрах; это не FPS LinQ и не реальное время камеры.
- Созданы три настоящих модельных JSONL по 5 `FrameDetections`: официальный COCO-reference, Matvey Pose и Matvey Helmet.
- `fall/running/proximity/phone/fence_crossing/restricted_under` имеют формальный статус `active`; `fire_smoking/no_harness/suspended_load` — `model_missing`, `load_carrying` — `skeleton`.
- Видео — **искусственная пустая сцена**, 640×360, 5 FPS. Оно проверяет проводку и схемы, не положительное падение и не промышленное качество. FP/час/accuracy из этого теста не публикуются.
- Поддерживающий COCO80 YOLOv8n взят из официального Ultralytics assets v8.3.0, SHA `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`; он нужен только тесту и **не объявляется дообучением Матвея**. В архив двух моделей он не включён.

Воспроизведение: создать **новый detached** worktree от зафиксированного main и вызвать `python -m ml.safewatch_local_check --app <worktree> --python <SafeWatch-python> --output <новая-папка> --bundle <COCO-reference-bundle> --bundle <pose-bundle> --bundle <helmet-bundle>`. Тест отказывается работать на ветке, менять существующий user-конфиг или перезаписывать модели. Полные команды, параметры, stdout/stderr и source revision сохранены в `local-check-v1/local-check.json` и `command-*.txt`.

## 6. Качество, GT и незакрытые задачи

Исторический Helmet: native/float object development macroF1 около 0.7164 при conf .25; PTQ менял class tradeoffs. Это пересекающаяся с источником предобучения development-выборка, **не независимая промышленная оценка**. У нового реестра floor .1, поэтому старые метрики не являются оценкой новой конфигурации.

Исторический Pose/Fall на 225 кадрах 2 FPS: TP1/FP0/FN9, F1≈0.1818; baseline качество не принято. Старые реальные LinQ captures подтверждают прежнее исполнение Split-Pose, а не текущий SafeWatch-bundle или его новое размещение.

RGB-MIL по опубликованному `matvey_result_final.json`: source-validation macroF1 .72953→.78363 (+.05409), fall recall .82353 без снижения. Это 37 weak/source clips и отдельная скалярная модель с pooling/prior; не actor-level industrial test и не готовая bbox-модель SafeWatch.

Разметка `/workspace/datasets/quality/temporal/episode-gt.source-reference.json` явно не имеет полной независимой human-review; URFall reference содержит uncertainty/unknown. В `safewatch eval` нет масок неизвестного, actor-aware matching или bounded-onset GT. Поэтому разметка **не была молча превращена в полный список expected**. `eval.compatibility-only.yaml` относится только к пустому искусственному control, не к заводскому видео.

Для действительно полностью просмотренной development/validation-разметки есть `python -m ml.safewatch_delivery eval-labels --source reviewed-events.json --output eval.matvey.yaml`. Вход: `reviewed_complete: true`, `scope: development|validation`, `videos: [{path, camera_id?, expected: [{scenario,start_s,end_s}]}]`, опционально `deadline_s`. Weak/неполные/sealed-test данные отклоняются. Нативный `suspected_fall` нельзя автоматически переименовать в `fall` без согласования GT-семантики.

Предложения приложению — **не реализованы**: PPE-плагин; temporal/RGB classifier hook; tracked extra-vehicles; импорт внешних GPU JSONL; отдельный namespace/staging загрузчика; optional no-tail ABI и настраиваемый input name; полноценный actor/unknown-aware scorer. До появления соответствующих object-checkpoint новые fire/cigarette/harness/load записи не создаются как «готовые».

Новые GPU-задачи, TPU-запросы, обучения и компиляции при выдаче: **0**. Активные процессы, сеть, SSH/VPN и общая инфраструктура не останавливались и не перенастраивались. Контроль реального нового LinQ и согласованный слот остаются отдельным release gate.

Проверки слоя выдачи: **7/7** тестов в preparation-окружении (включая реальную ONNX/ORT сборку хвоста); общий `unittest discover` — **499 tests OK, skipped=4** в linQ-client окружении, где ONNX-тесты дополнительно выполнены отдельно. SHA всех файлов выдачи, local evidence и всех членов архива проверены. Программные тесты не являются измерением accuracy. В рабочем дереве оставлены нетронутыми чужие параллельные изменения и `.ipynb_checkpoints/`.
