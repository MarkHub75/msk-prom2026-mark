# Финальный ML-конфиг подключения — MOSPROM-2026

Пакет проверен локально на неизменённом Argus main94213c5f,techv9.
Основной профиль — `config/pipeline.stable.local.yaml`: прежние COCO80,
Matvey Split-Pose и Helmet. Новых experimental checkpoint в нём нет.
Капитанский рабочий LinQ/SIBINTEK маршрут остаётся под управлением Марка и LinQ Agent.

## Что подключать

Реестр: `config/models.matvey.release.yaml` — четыре точных ModelSpec.
Три baseline и опциональный старый Fire/Smoke; Phone/newForklift/newPPE исключены.
Все восемь указанных ONNX-файлов реально находятся под `models/matvey/` в пакете.
Полные checkpoint/ONNX/tail SHA, исходные абсолютные пути, версии и fingerprints:
`RELEASE_CANDIDATE.json`. Веса, class maps, confidence и IoU не изменены,
поэтому существующие model versions сохраняются. Новому принятому checkpoint
потребуются новая версия и fingerprint; подменять существующие байты нельзя.

| Назначение | Профиль | Модели |
|---|---|---|
| По умолчанию | pipeline.stable.local.yaml | COCO80 + Split-Pose + Helmet |
| S02 | pipeline.s02.local.yaml | COCO80 + Split-Pose |
| S04, только локальное демо | pipeline.s04.local.yaml | COCO80 + Fire/Smoke |
| S07 | pipeline.s07.local.yaml | COCO80 + Split-Pose |
| Helmet, дополнительный | pipeline.helmet.local.yaml | COCO80 + Split-Pose + Helmet |
| Все четыре направления, локальное демо | pipeline.all-demo.local.yaml | COCO80 + Split-Pose + Helmet + Fire/Smoke |

Все перечисленные файлы находятся в `config/`. Профиль определяет нейросети,
а не переписывает/изолирует правила Argus. Правила, зоны, калибровка, доставка
и интерфейс остаются у Марка. Helmet требует настоящую helmet_required policy;
для проверки не создавалась выдуманная зона, чтобы получить положительное событие.
Fire/Smoke сохраняет известные ложные тревоги на фарах/станках и не включён
в default stable profile. S07 исполняется, но качество падений не принято.

## Подключение к существующему Argus

1. Проверить `sha256sum -c SHA256SUMS` из корня распакованного ML-пакета.
2. Скопировать его `models/` в корень приложения, сохраняя относительные пути.
   Перед заменой уже существующего файла сверить SHA; разные байты под одной
   id@version запрещены. Бинарники не добавлять в Git.
3. Объединить `config/models.matvey.release.yaml` с реестром приложения по
   id@version. Matvey Pose/Helmet/Fire уже есть в main — оставить идентичные
   записи, не создавать дубликаты. COCO-reference — отдельный local model ID;
   не подменять им или его хвостом капитанскую compiled baseline.
4. Выбрать один профиль и перенести только его pipeline/local поля в
   существующий user config. Не заменять весь config/user.yaml: сохранить
   прочие секции Марка. Список pipeline.extra заменяется целиком; для совместного
   демо использовать уже составленный all-demo, а не последовательно применять
   четыре профиля. CPUExecutionProvider/threads1 явно заданы для локальной проверки.
5. В существующем окружении Argus выполнить:

```bash
INFERENCE_BACKEND=local SAFEWATCH_FAKE=0 uv run safewatch doctor
```

Затем загрузить реальный MP4 в существующую камеру через приложение либо
`uv run safewatch import PATH_TO_VIDEO --camera CAMERA_ID`: команда ставит задачу
в очередь штатного worker. Запуск/перезапуск стенда выполняет его владелец.
Наши проверки не запускали TCP-сервер и не меняли стенд капитана.

Сохранённые CPU JSONL при необходимости импортируются штатным CLI:

```bash
INFERENCE_BACKEND=local SAFEWATCH_FAKE=0 uv run safewatch import-artifact FILE.jsonl \
  --video VIDEO_ID --model EXACT_ID@VERSION --backend local
```

VIDEO_ID должен относиться к тому же исходному SHA; профиль target_analysis_fps12
и исходный fps должны давать тот же шаг, что записан в verification artifacts.
Не помечать эти JSONL как LinQ, не добавлять fake и не переносить детекции
на пропущенные кадры. Raw cls обязателен: поле name не является источником
класса в Argus. Pose — ровно COCO17[x,y,confidence],bbox — исходные xyxy pixels.

## Фактические проверки

6/6профилей: `safewatch doctor` exit0 и `GET /api/models` HTTP200.
8ONNX-графов: checker/shape/классы PASS. 531software tests PASS,4skipped;
три отдельных регрессионных проверки маршрутизации сценариев PASS.

| Проверка | Исходных кадров | Реальных CPU-вызовов | Результат Argus |
|---|---:|---:|---|
| Stable, factory3_tr45 |75|114|proximity1,event/evidence1,API200 |
| S04, source fire clip |293|586|fire_smoking1,event/evidence1,API200 |
| S07, URfall06 reference |100|100|0events; падение не распознано |

Итого800CPUcalls,381уникальный обработанный кадр из468исходных. GPU0,TPU0.
На stable/S07 применяется штатный step2; на10FPS Fire — step1. Все индексы,
пропуски по модели и точные sourcePTS_ticks/time_base сохранены в
`verification/*/SOURCE_FRAME_COVERAGE.json`; Argus JSONL округляет ts_ms до0.1ms.
Эти события — настоящие предсказания приложения, а не GT и не подтверждённые
нарушения. Нет независимых eventGT, поэтому TP/FP/FN/P/R/F1 NOT_MEASURED.
В S04 MP4 — ранее подготовленная playback-производная исходного AVI; lineage
и оригинальный source сохранены в source_metadata.json. Байты входного MP4
в новой проверке не менялись. Исторические TPU результаты сюда не смешивались.

Изолированные runtime dependencies для текущего main установлены только
под artifact runtime_deps по wheelSHA из uv.lock; существующие окружения
PyTorch/SDK/Argus не менялись. Settings, исходники и правила приложения
проверены на отсутствие патчей. UI/внешний staging визуально не проверялись.

## Новейший Training handoff

Версия matvey_final_five_progress_20261025_v1 проверена один раз,21ссылка/SHA.
Новых принятых runtime models0. FitA7afb... улучшил sourceF1.625→.736842,
но сохранил press-confusers; FitBc611... не прошёл gate. Новые Helmet/PPE
потеряли no_helmet recall; baseline сохранён. Финальный paired-review ожидается
от Training отдельной версией; никакие исследования/дообучения root не повторял.

## LinQ и момент заморозки

`config/pipeline.linq.keep-current.yaml` лишь сохраняет капитанскую baseline
пару det-yolov8n@640-ap9999 / pose-yolov8n@640-ap9999, без extra и изменений
транспорта. Это не новый TPU-прогон. Fire/Smoke локальный; новую Matvey placement
не утверждаем. Наш4-inputSplit-Pose tail нельзя ставить к капитанской3-output
Pose640программе. Не менять работающую SIBINTEK сборку этим local profile.

Readiness завершена до07:30МСК. После этого — только упаковка/критические
исправления; после08:00МСК никаких архитектурных изменений. Источники, модели
и метрики нового SIBINTEK TPU-демо готовят назначенные владельцы.
