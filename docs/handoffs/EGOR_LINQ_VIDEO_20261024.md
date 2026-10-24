# Матвей → Егор/Марк: MP4 и настоящие результаты LinQ

Приоритет капитана: передача до **24.10.2026 18:00 МСК / 15:00 UTC**.
Роль ML ограничена моделями, инференсом и детекциями. Правила, зоны, события и
приложение остаются у Марка. `main` и чужие worktree не изменялись.

Комплект использует **сохранённые настоящие TPU-ответы**. Нового удалённого
инференса при экспорте не было. Финальная схема Argus ожидается; текущий JSON —
полный промежуточный результат, не готовый импорт в приложение.

Единый архив для передачи:
`/workspace/artifacts/matvey_egor_linq_20261024_v2.zip`,59,748,256bytes,
SHA256 `d787e6f28e1ff309faedec6499e7ded522708f8eae41f3f3cb54970db90b9247`.
Все57файлов проверены; рядом `.sha256`. Это локальный delivery, не off-Vast backup.

## Готовые файлы

| Комплект | Папка вне Git | Настоящая TPU-обработка |
|---|---|---|
| Промышленная камера, Mendeley `4_tr6` | `/workspace/artifacts/matvey-egor-linq-demo-20261024-v2/` | Кадры **0, 13** из522; исходные PTS **0, 518.962 мс**; Helmet + Split-Pose,4ответа |
| Короткий лабораторный URFall01 | `/workspace/artifacts/matvey-egor-linq-urfall01-20261024-v2/` | Кадры **0,15,30,45,60,75,90,105,120,135,150** из160; PTS0–5000мс; Split-Pose,11ответов |

В каждой папке:

- `matvey_source_original.mp4` — **исходный MP4 без перекодирования/изменения байтов**;
- `matvey_linq_frames.intermediate.json` — frame index, исходный encoded PTS,
  размер кадра, RGB SHA, классы/ID/confidence/bbox, все17COCO-точек с confidence,
  model/version/programSHA, transform и request/response/status/timing;
- `matvey_tpu_proof.json` — allowlisted подтверждения реальных исторических
  завершений и результаты проверки соответствия исходным кадрам;
- `numeric/<request-UUID>/inputs.npz`, `response.npz`,
  `matvey_completion_receipt.json` — полные выбранные числовые тензоры;
- `models/*_decoder.json` — точный исторический preprocessing/decoder ABI;
- `matvey_checksums.json` — размеры и SHA256 всех выданных файлов.

Полный MP4 в комплекте не означает полный инференс. `coverage.partial=true`,
точные обработанные индексы перечислены в JSON; остальные кадры **NOT_INFERRED**,
не отрицательные примеры. EOF-запись UR151 — отдельная non-inference запись,
она не включена в11обработанных кадров. UR — лабораторный пример; независимое
промышленное качество и факт успешного распознавания падения не заявляются.
UR MP4 — ранее подготовленный сжатый RGB-crop preview, использованный в том
инференсе, а не исходная nativeRGB-запись датасета. Сейчас он не изменялся.

Исходный industrial SHA256:
`f0e34d76de139450b97decbb4e032a525d8ce9959d972cdd0071a1de69250c6a`.
Исходный URFall01 SHA256:
`ad08c42886c274c03876a68fb7f2be3b065c951d7202847317d126c61bb1d760`.

## Что проверено

Копии MP4 побитово совпали. Каждый показанный кадр заново прочитан по исходному
ordinal и encoded PTS. Исторический preprocessing **побитово воспроизвёл входы
всех15запросов**. Проверены SHA файлов и каждого тензора, finite values, именованный
ABI, совпадение UUID запроса/ответа, status0. Декодирование сохранённых TPU-выходов
повторно дало именно выданные детекции. Секреты/URI/состояние notebook не экспортированы.

Промышленные4RPC: исторический transport-inclusive total10.285–11.072с/вызов,
сумма42.657с. UR11RPC:9.424–22.685с/вызов, сумма130.654с. Это сохранённое время
реальных вызовов; export/cache/review time отдельно, device-only time неизвестно.
Независимой аттестации физического чипа эти локальные проверки не дают.

## Совместимость и последующее преобразование

Прочитан `main:docs/ML_INTEGRATION.md` на ревизии
`f6b5358afee60d1190f5b5e9decc77292b9087c9`, ветка не переключалась.
Согласованный текущим документом mapping: Pose `{0:person}`; Helmet
`{0:helmet,1:no_helmet}`, исходное `bare_head` сохранено отдельным полем.
Новые имена классов не вводились. Helmet — extra; существующие правила Argus
не содержат PPE-плагин. Четыре выхода Pose требуют готового хвоста `[1,56,8400]`.

Исторический ML preprocessing использовал **PIL BILINEAR**, текущий Argus —
**OpenCV INTER_LINEAR**. Нельзя объявлять их входы идентичными. Передаваемые bbox
и точки уже в исходных пикселях; сохранены фактические transform и входные
тензоры. Полные выходы позволят преобразовать JSON/порог записи после получения
контракта без повторного TPU-инференса. Значения confidence и source labels не GT.
Внешнего импорта JSONL в прежней ревизии приложения нет; БД/кэш не изменялись.

Готовые модели/ONNX/TPU/tails и registry entries уже выданы отдельно в
`/workspace/artifacts/safewatch-delivery/matvey_safewatch_delivery_v2.tar.gz`;
SHA256 `7cfcf125189f4e0034d1de7a88033d465c0c6be453cee5f145a3ca3755f3892b`.
Инструкция: `docs/ML_HANDOFF_MATVEY.md`; записи `ml/models.matvey.yaml`.
Это прежние веса с адаптацией ABI, не новые trained detectors.

## Воспроизведение без нового запроса

```bash
cd /workspace/project
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
/workspace/.venvs/linq-client/bin/python -m ml.video_handoff \
  --verify-only --output /workspace/artifacts/matvey-egor-linq-demo-20261024-v2
/workspace/.venvs/linq-client/bin/python -m ml.video_handoff \
  --verify-only --output /workspace/artifacts/matvey-egor-linq-urfall01-20261024-v2

# Новый экспорт — только в новую папку, без замены старых evidence:
/workspace/.venvs/linq-client/bin/python -m ml.video_handoff \
  --profile industrial --output /workspace/artifacts/NEW-matvey-industrial-export
/workspace/.venvs/linq-client/bin/python -m ml.video_handoff \
  --profile urfall01 --output /workspace/artifacts/NEW-matvey-ur-export
```

Новый TPU-прогон пока **BLOCKED**, текущая аппаратная доступность UNKNOWN:
нет подтверждённого собственного Matvey staging/receipt и допустимого binding.
Bootstrap остаётся PREPARED, не опубликован. Наличие AMQP/runtime config не решает
file placement. Стандартный загрузчик приложения пишет в общую `mosprom_work/`
и root-cache область; при действующем требовании `matvey/` он не запускался.
VPN/SSH/маршруты/службы/чужие очереди/программы не менялись. Для свежего запуска
нужны разрешённый own upload, matching SHA receipt и согласованный одиночный слот.

Материалы предназначены для разрешённой командной проверки. Mendeley: CC BY4.0,
источник DOI10.17632/xjmtb22pff.1; сохранять attribution. URFall: академическая
NC-SA область; публичная публикация медиа этим экспортом не разрешается.

## Подготовленная команда нового инференса без правил

`ml.linq_frames` вызывает существующий DurableVideoRunner; BehaviorEngine,
сценарии, зоны, события, backend/frontend приложения не запускаются. Подготовлены
локальные manifests в `/workspace/artifacts/matvey_frame_inference_bindings_20261024_v1/`.
Они не являются подтверждением удалённого размещения. План в `matvey_sampling_plan.json`
выбирает12ближайших кадров к равномерным encoded-PTS целям до первого model call.
Максимум24последовательных model calls, не более одного запроса в полёте.

```bash
cd /workspace/project
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
client=/workspace/.venvs/linq-client/bin/python
bindings=/workspace/artifacts/matvey_frame_inference_bindings_20261024_v1

# Сейчас возвращает BLOCKED/exit2, не открывая сетевого соединения:
"$client" -m ml.linq_frames --preflight-only \
  --manifest "$bindings/matvey_helmet_manifest.json" \
  --manifest "$bindings/matvey_pose-split_manifest.json"

# Только после реального own upload, matching SHA receipt и согласованного слота:
# runtime connection.env загрузить в свой процесс без печати, как в существующем runbook.
"$client" -m ml.linq_frames \
  --source /workspace/artifacts/matvey-egor-linq-demo-20261024-v2/matvey_source_original.mp4 \
  --source-sha256 f0e34d76de139450b97decbb4e032a525d8ce9959d972cdd0071a1de69250c6a \
  --manifest "$bindings/matvey_helmet_manifest.json" \
  --manifest "$bindings/matvey_pose-split_manifest.json" \
  --frames 0,47,95,142,189,237,284,332,379,426,474,521 \
  --output /workspace/artifacts/NEW_matvey_linq_frames_run
```

Gate требует receipt STAGED/namespace=matvey, точные bytes/SHA/name/model и
реальный completed upload UUID с собственным reply namespace и числовым
подтверждением SHA/byte_count. Старые bindings/receipts не проходят. На UNKNOWN
exit3 останавливается тот же кадр; повторить точно ту же команду/папку для
receive-only reconcile прежнего UUID. Уже сохранённые результаты повторно
проверяются по исходному RGB, модели, transform и числовому durable journal без
нового inference. GPU fallback отсутствует. Финальная схема Argus не выдумывается.

Новый driver проверен локальными fixture-тестами gate/cache; actual remote run
этого entry point NOT_RUN. Runtime capability audit также подтвердил отсутствие
настроенного Jupyter staging доступа в этой среде; секретные значения не читались.
