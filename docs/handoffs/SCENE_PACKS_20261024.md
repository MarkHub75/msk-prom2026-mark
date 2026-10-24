# Полные видеосцены — Матвей → Егор/Марк

Единый каталог: `/workspace/artifacts/matvey-scene-packs-20261024/`.
Индекс с абсолютными путями: `matvey_manifest.json`.
Это результаты нейросетей, без правил, зон и событий Argus. Финальная схема
приложения пока не зафиксирована; данные остаются полным кадровым intermediate.

Первые три полных GPU-прогона были наблюдены завершёнными **24.10 в14:58:55UTC /
17:58:55МСК**, до чекпоинта18:00. Независимый полный source-аудит выполнен после
чекпоинта. Затем добавлены остальные сцены, без повторения уже готовых forward.

| Папка | Исходных/обработанных кадров | Что показывает / ограничение |
|---|---:|---|
| `S07_urfall01` |160/160|Полный лабораторный fall reference; bbox/COCO17; отдельные11исторических TPU-кадров только Pose. Старые правила этот source fall пропустили |
| `S02_7_te4` |101/101|Погрузчик/штабель и рабочая область; generic COCO vehicle/person proposals, не квалифицированная опасная дистанция |
| `S04_5_tr19` |247/247|Полная сцена с дымкой и работниками; fire/smoke/cigarette-модель отсутствует, происхождение дымки UNKNOWN |
| `S01_3_tr45` |75/75|Промышленный person/vehicle контекст; **не положительное подтверждение бега**, gait/action head не квалифицирован |
| `S02_7_tr15` |52/52|Второй полный forklift/occlusion контекст; нарушение и физическая дистанция не установлены |
| `S07_urfall06` |100/100|Полный лабораторный fall reference с позами; прежний saved-native subset давал наблюдаемый переход, правила здесь не запускаются |
| `S04_6_tr15` |35/35|Короткая сцена с дымкой; первый encoded PTS39.028мс сохранён, не заменён нулём |

Всего **7сцен,770кадров,2310реальных локальных GPU-вызовов**. Каждый кадр прошёл
Pose, Helmet и COCO80 reference. Пропущенных локальных кадров0; пустая детекция
тоже записана как обработанный кадр. **S08 BLOCKED**: просмотренные штабели несёт
погрузчик; это не подтверждённая ручная переноска. Нет qualified cargo/policy
модели. Статус: `S08_BLOCKED/matvey_status.json`; видео/GT не подменялись.

## Файлы в каждой сцене

- `matvey_source_original.mp4` — побитово сохранённый MP4 модельного входа;
- `matvey_detections.json` и `.jsonl` — каждый исходный ordinal, encoded PTS,
  RGBSHA, original image size, backend, модель/версия, все post-NMS bbox/score и
  COCO17тройки `(x,y,confidence)` при наличии; exact inputSHA/letterbox transform;
- `matvey_scene.json` — полный class map, веса/manifest SHA, фиксированные
  confidence.25/NMS.45/max300, model role, proposal counts, wall time, rights и
  отдельные available/absent/cannot_confirm сигналы;
- `matvey_linq_frames.json` — точные TPU-индексы **по каждой модели**, без
  распространения Pose-результата на Helmet/COCO;
- `matvey_missing_frames.json` — отдельные пропуски local/TPU и каждой модели;
- `matvey_validation.json`, `matvey_independent_validation_v1.json` — проверки;
- `matvey_report.txt` — краткий человекочитаемый отчёт.

Общий независимый отчёт: `matvey_independent_review_v2.json`. Он проверил каждый
из770sourceRGB, исходные encodedPTS, все2310входных SHA/transform, class ID/name,
границы bbox, confidence,17точек, полную кадровую сетку и JSON/JSONL соответствие.
Проверка не вызывала нейросеть заново и не устанавливает event accuracy.

## Происхождение и технические границы

Модели прежние: `pose-split-v1`, `helmet-v1`, `coco-reference-yolov8n`.
COCO80 — официальный pretrained reference, не новый Matvey fine-tune и не
квалифицированный detector погрузчика/огня/страховки. Class IDs исходные;
единственный product alias `bare_head→no_helmet`, исходное имя сохранено.
Межклассовые COCO proposals могут описывать один предмет как car/truck/bus/
suitcase; счётчики — **число покадровых предложений**, не уникальные объекты/GT.
Indoor Helmet proposals также могут быть ложными. Независимых P/R/F1 нет.

RTX4090 была проверена через nvidia-smi: активных процессов не было, Training
сообщал FINISHED_GPU_RELEASED. Root занял общий gpu.lock только на время одного
последовательного job; одновременно тяжёлые задачи не запускались. Потоки2,
OpenCV1. Три волны обработаны последовательно, GPU освобождён. При занятом GPU
код выбирает явно помеченный CPU; это не автоматический fallback из LinQ.

Все новые кадровые результаты — `PYTORCH_CUDA`, **не TPU**. Никакой интерполяции
или протягивания детекций на необработанные кадры нет. Raw local NN tensors не
сохранены; полные decoded результаты после фиксированного порога.25 сохранены.
Если будущий контракт требует более низкий порог, ниже него данные из этого
экспорта не восстановить. Препроцессинг PIL BILINEAR отличается от app OpenCV.

Mendeley MP4 исходные, CC BY4.0, DOI10.17632/xjmtb22pff.1; сохранять attribution.
UR MP4 — предсуществующие сжатые RGB-crop preview, использованные моделью,
**не nativeRGB оригинал датасета**; сейчас байты не изменялись. URFall —
академическая NC-SA область; публичная публикация не разрешена этим комплектом.

## Отдельный LinQ

В `S07_urfall01/matvey_separate_historical_linq_capture/` лежит проверенный
исторический настоящий Split-Pose capture на том же MP4SHA: кадры0,15,…,150,
11correlated status0, numeric inputs/outputs и transport timing. Все source/input
SHA и результаты декодирования повторно проверены. Это не новый TPU-прогон,
не подтверждение качества fall и не весь покадровый CUDA-вывод.

Новый limited LinQ-прогон проверен отдельно: `matvey_linq_readiness.json`.
Fresh calls0. Own staging/receipt и Jupyter staging capability отсутствуют;
текущая доступность самого TPU UNKNOWN. Legacy bindings, чужие программы/очереди,
VPN/SSH/службы не использовались/не менялись. Инференс-only команда и gate:
`docs/handoffs/EGOR_LINQ_VIDEO_20261024.md`, `ml.linq_frames`.

## Воспроизведение в текущем workspace

```bash
cd /workspace/project
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
export YOLO_CONFIG_DIR=/workspace/artifacts/NEW_matvey_scene_settings

# Существующие сцены не перезаписывать. Новый полный local run:
/venv/main/bin/python -m ml.scene_packs \
  --root /workspace/artifacts/NEW_matvey_scene_packs

# Проверка готовых файлов без нового neural/TPU call:
/workspace/.venvs/linq-client/bin/python -m ml.scene_packs --verify-only \
  --review-output /workspace/artifacts/NEW_matvey_scene_review.json
```

`--scene S02_7_te4` ограничивает явный список. Для GPU нужен свободный общий lock
и отсутствие активных CUDA-процессов. Исходные datasets/weights не скачиваются
и не меняются. Main и worktree других агентов не редактируются.
