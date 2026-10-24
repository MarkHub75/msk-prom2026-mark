# SESSION HANDOFF — MOSPROM-2026: полные видеосцены

Последний closing audit: **2026-10-24 15:46:02 UTC / 18:46:02 МСК**.
Полные сцены и код сохранены в commit
**`2623cabefbe3c9e83e550e5336b1df18c3a17879`** ветки `matvey_cv`.
Этот handoff сохраняется следующим документационным коммитом; его containing SHA:
`git log -1 --format=%H -- docs/handoffs/SESSION_HANDOFF_20261024_SCENES.md`.
После передачи остановиться; следующая работа — в новой сессии по новой директиве.

## 1. Актуальная роль и приоритет

Матвей/root owns **нейросетевые модели, их качество, ONNX/TPU, LinQ и реальные
покадровые результаты**. **Марк owns Argus: правила, зоны, треки/события, backend и
приложение; Егор — frontend. Не дублировать их правила и не менять их код.**
Старые8observation-rule прототипов остаются историческим frozen checkpoint,
но больше не являются направлением новой разработки ML.

Последняя задача до handoff: полноценные scene packs S02/S07/S04/S01 и S08 при
наличии подходящих данных. Сначала2–3сцены до24октября18:00МСК, после него —
расширение. Первые3полных GPU-forward результата наблюдались завершёнными
**14:58:55UTC / 17:58:55МСК**. Полный независимый аудит, дополнительные сцены и ZIP
завершены после чекпоинта. Не утверждать, что поздняя упаковка/аудит были до него.
Общий официальный deadline загрузки решения остаётся **25октября10:00МСК /07:00UTC**.

Марк обещал обновлённый Argus-контракт примерно через40минут. **Он ещё не получен**.
Последняя remote-main проверка этой итерации вернула
`f6b5358afee60d1190f5b5e9decc77292b9087c9`; документ `docs/ML_INTEGRATION.md`
там старый. Main читался через git show/fetch без переключения ветки.
Не придумывать финальную JSON-схему: текущие outputs явно INTERMEDIATE.

## 2. Git, ownership, процессы

- Root worktree **`/workspace/project`**, ветка **`matvey_cv`**. Main не изменялся.
- Код сцены,9owned tests, малые отчёты и регистры: commit2623cabe выше.
- Предыдущий head `e9179bc81ea2ff9bf162dab5b59cc027a9d5314b` уже был push/remote-SHA
  verified. Раньше ещё push verified53992b3a. Старые blanket-заявления об
  AUTHENTICATION_UNAVAILABLE исторические: в этой сессии non-force push работал.
- Текущий handoff+2623cabe нужно сохранить обычным push matvey_cv; итог будет в
  финальном ответе/closing receipt вне Git. Не force и не main.
- Единственный прежний untracked **`.ipynb_checkpoints/`** не открывался, не
  удалялся, не индексировался. Не делать git add . и не объявлять весь tree чистым.
- Все кодовые изменения сделаны только в root worktree. Data/Training/Detection/
  Behavior/LinQ worktree не редактировались и их ветки автоматически не мержились.
- В closing audit GPU compute processes=0, общий gpu.lock был FREE,
  собственных активных `ml.scene_packs`, `ml.linq_frames`, `ml.video_handoff` PID=0.
  Это snapshot, не обещание будущей свободной GPU. Все свои GPU jobs завершились.
- Новых native subagents в этой итерации не запускали; исторические completed
  агенты не являются активными workers. Не выдумывать фоновые задания.

Изоляция остаётся прежней: root здесь; Detection `/workspace/agents/detection`,
Behavior `/workspace/agents/fall`, LinQ `/workspace/agents/linq`; Data owns
`/workspace/agents/data-audit`, Training owns `/workspace/agents/training`.
Не трогать чужие worktree. За рамками root helpers сохраняется ownership AGENTS.md.

## 3. Главный готовый результат — семь полных видеосцен

**Единый каталог:** `/workspace/artifacts/matvey-scene-packs-20261024/`.
**Индекс:** `matvey_manifest.json` — абсолютные пути, статусы, per-scene limits.
**Инструкция:** `docs/handoffs/SCENE_PACKS_20261024.md` и копия `matvey_README.md`
в artifact-каталоге. Малый Git summary: `ml/reports/scene-packs-20261024.json`.

| Scene ID / папка | Полностью обработано | Смысл и действительный предел |
|---|---:|---|
|`S07_urfall01`|160/160|Лабораторный source fall, полная последовательность bbox/pose.11исторических Pose TPU-кадров того же MP4 отдельно; прежний rule endpoint этот fall пропустил |
|`S02_7_te4`|101/101|Погрузчик/штабель и люди: generic COCO vehicle/person proposals, не квалифицированная опасная дистанция |
|`S04_5_tr19`|247/247|Полная сцена с дымкой; fire/smoke/cigarette inference отсутствует, источник дымки UNKNOWN |
|`S01_3_tr45`|75/75|Factory person/vehicle context; **не положительная демонстрация распознанного бега**, action head не квалифицирован |
|`S02_7_tr15`|52/52|Второй forklift/occlusion context; физическая дистанция/нарушение не установлены |
|`S07_urfall06`|100/100|Полный лабораторный fall reference; прежний saved-native subset давал наблюдаемый переход, новые правила не запускались |
|`S04_6_tr15`|35/35|Короткая haze scene; первый encoded PTS **39.028мс**, не0 |

Итого **770original frames ×3existing models =2310реальных PyTorch CUDA forward**.
У каждой модели есть результат каждого кадра, включая пустой detections list.
Пропущенных local inference frames0; интерполяции/протягивания детекций нет.
Это полное **покадровое покрытие входа**, не качество распознавания всех сценариев.

**S08 не подменять:** `S08_BLOCKED/matvey_status.json`. Подтверждённой сцены
человек-owned ручной переноски и qualified cargo/policy модели нет. Forklift stack
не является manual-cargo GT. S01/S04 тоже остаются context-only по указанным выше
сигналам, а не принятыми positive demos своих действий.

В каждой готовой scene-папке:

1. `matvey_source_original.mp4` — побитовая копия входного MP4, без перекодирования.
2. `matvey_detections.json` и `.jsonl` — все original frame_index/encoded PTS,
   image size/RGBSHA/backend, model/version, IDs/names/confidence/bbox, COCO17
   `(x,y,score)` при наличии, exact inputSHA и letterbox transform.
3. `matvey_scene.json` — source/model/manifest SHA, class maps, role,
   thresholds, rights, per-frame proposal counts, timing, signal limitations.
4. `matvey_linq_frames.json` — **по каждой модели** реальные TPU indices/origin;
   `matvey_missing_frames.json` — local и per-model TPU gaps.
5. `matvey_validation.json`, `matvey_independent_validation_v1.json`,
   `matvey_report.txt` — проверки и человеческие технические ограничения.

Счётчики — число предложений моделей **по кадрам**, не уникальные люди/объекты,
не GT и не события. COCO может путать car/truck/bus/suitcase на одной технике;
indoor Helmet proposals тоже могут быть false positives. Нельзя считать
отсутствие специалиста/детекции доказательством отсутствия нарушения.

## 4. ZIP для передачи, проверенные по всем членам

Архив лучших3сцен:
`/workspace/artifacts/matvey-scene-packs-20261024/matvey_best_three_v1.zip`
— **21,876,290bytes**,68members,
SHA256 `2fb53f9a24de4bb09c13bf7f6f3b26c857f9022724f345c5805084cd0d7943f6`.
Содержит S07_urfall01/S02_7_te4/S04_5_tr19, оригиналы+полные результаты+проверки.

Все7сцен:
`/workspace/artifacts/matvey-scene-packs-20261024/matvey_all_scenes_v1.zip`
— **35,438,479bytes**,108members,
SHA256 `247333eadbafde0ff1dc81e0060942623611cdca2697e8bca231855f98ae2f28`.
Рядом `.sha256` и `*_archive_review.json`; member SHA verification PASS у обоих.
Архивы не изменять; новое содержимое — новая версия. Это **не off-Vast backup**.

Егор уже получил предшествующий partial-capture ZIP
`/workspace/artifacts/matvey_egor_linq_20261024_v2.zip`,59,748,256bytes,
SHA `d787e6f28e1ff309faedec6499e7ded522708f8eae41f3f3cb54970db90b9247`.
Он НЕ полный scene pack:2industrialframes+11URframes,15исторических TPU replies.
Не смешивать его scope с новой полной CUDA обработкой.

## 5. Модели, происхождение данных и ресурс

Новых weights, training, compile, threshold search или model promotion не было.
`ml/scene_packs.py` использует существующий NativeReferenceBackend/preprocess/decode:

| Модель | Weights / SHA256 | Статус |
|---|---|---|
|Pose `pose-split-v1`|`/workspace/artifacts/detection/pose-split/weights.pt`, `c6fa93dd1ee4a2c18c900a45c1d864a1c6f7aba75d84f91648a30b7fb641d212`|COCO17/person0, stable weights; historical TPU qualified only in recorded scope |
|Helmet `helmet-v1`|`/workspace/artifacts/detection/helmet/weights.pt`, `05ed3a517485292d42d6eb6c9be3987ea51cd162e04807d2741eadcac8a19e6c`|source classes helmet0/bare_head1; product alias1→no_helmet |
|COCO80 reference|`/workspace/artifacts/safewatch-delivery/reference/yolov8n.pt`, `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`|официальный pretrained reference, не Matvey fine-tune и **не TPU-qualified** |

Точный source class map, model role и manifest SHA лежат в каждой scene metadata.
Confidence floor **.25**, class-aware NMS**.45**, max300, original-pixel xyxy,
COCO17. Препроцессинг **PIL BILINEAR RGB letterbox640/pad114/float32×1/255**.
Raw local NN output tensors **не сохранены**; полные decoded результаты после
порога сохранены. Если контракт попросит floor.1, ниже.25 этот экспорт не
восстановить — нужен отдельный local rerun, не выдумывать потерянные detections.

До GPU job: nvidia-smi empty, Training published FINISHED_GPU_RELEASED,
общий `/workspace/artifacts/quality/gpu.lock` свободен. Root занял его, запускал
только один sequential job, Torch2threads/OpenCV1, освободил после завершения.
Три короткие волны не пересекались. Closing audit GPU0/free lock; не делать
вывод о будущей занятости. CLI выбирает CPU при занятом GPU; результаты явно
маркированы. Это не fallback из LinQ.

Mendeley5MP4 из immutable `mendeley-factory-replay16/v1-20261024`, CC BY4.0,
DOI10.17632/xjmtb22pff.1; весь family calibration-known. UR2MP4 — предсуществующие
lossy RGB-crop previews, **не nativeRGB originals**; академическая NC-SA область.
Во время экспорта байты не менялись. No source search/acquisition, GT не создавался,
test не открывался. Producer/frozen READY capabilities rechecked **post-run**;
каждый выбранный source SHA был проверен **до** его forward. Receipts в каталоге.
Никаких independent P/R/F1/event accuracy из этих scene packs не следует.

## 6. LinQ — что настоящее, что заблокировано

**Fresh TPU calls этой full-scene итерации0.**
`matvey_linq_readiness.json`: own staging/receipt отсутствует; Jupyter runtime
URL/auth capability в этом процессе/известном project runtime config не настроена.
Проверялось только наличие, значения не читались/не логировались. Наличие AMQP
runtime config не даёт filesystem upload. Сам TPU сейчас **availability UNKNOWN**,
не «сломался». Сеть, SSH/VPN, services и чужие программы/очереди не менялись.

В **S07_urfall01** вложен `matvey_separate_historical_linq_capture/`: тот же source
SHA `ad08c42886c274c03876a68fb7f2be3b065c951d7202847317d126c61bb1d760`,
только Split-Pose, кадры0/15/…/150,11correlated status0. Numeric inputs/outputs,
UUID/receipt/ABI/file+tensors SHA/source-input bitwise parity повторно проверены.
Это отдельная историческая hardware sequence, не770CUDAframes и не fresh run.
У Helmet/COCO в этих сценах TPU-кадров0. У прочих6сцен их0 у всех моделей.

Старые2industrial TPUframes относятся к **другому** MP4 `4_tr6`, source SHA
`f0e34d76de139450b97decbb4e032a525d8ce9959d972cdd0071a1de69250c6a`.
Нельзя приписать их S02_7_te4/7_tr15. Исторический transport-inclusive latency
порядка10–23сек/вызов, не realtime; device-only time/independent chip attestation
не установлены. Export/cache timing не заменяет реальную call latency.

Готовый inference-only driver **`ml.linq_frames`** использует существующий
DurableVideoRunner/AMQP/journal/admission, не пишет второй клиент и не запускает
правила. Bindings подготовлены локально:
`/workspace/artifacts/matvey_frame_inference_bindings_20261024_v1/`.
Preflight offline требует ownMatvey program name, pinned bytes/SHA/ABI, настоящий
staging receipt и completed numeric upload UUID с own reply namespace, SHA/bytecount.
Сейчас он возвращает BLOCKED до сети. Предподготовлен12-frame encoded-time sample
industrial4_tr6, максимум24sequential calls. Driver remote-run **NOT_RUN**;
gate/cache/ABI fixtures9PASS. Сохранённый cache сравнивает с raw durable tensors.

Own bootstrap `/workspace/artifacts/linq-rpc/matvey-bootstrap-v1/` остаётся
PREPARED/unpublished. Исторические root-cache receipts не подтверждают новое
размещение. Не переименовывать их. Новые remote файлы только `matvey/`, имена
`matvey_`, один ownrequest, полный canonical UUID. UNKNOWN→тот же UUID receive-only;
не blindretry и не purge/redeclare чужой queue. Legacy fresh bindings запрещены.
Main `tools/linq/jupyter_remote.py` был просмотрен: его `_hub_login` может
автоматически стартовать single-user server при отсутствии ответа. Этот путь
не запускался; нельзя использовать его для обхода запрета service changes.
Нужен уже разрешённый собственный kernel/channel, без чужих остановок.

## 7. Совместимость Argus и отдельный готовый model kit

Авторитет — актуальный `main:docs/ML_INTEGRATION.md`, прочитать заново при обновлении.
Известная ревизияf6b5358a: primary detector обязан COCO80 (не person-only и не
padding); техника car/bus/train/truck только из detector. Phone имя `cell phone`
с пробелом, forklift — generic truck7; не придумывать новый forklift-class.
Pose `{0:person}`,17COCO. Helmet extra `{0:helmet,1:no_helmet}`; PPE rule отсутствует.
Fire/smoke/cigarette/no_harness/suspended_load — только точные согласованные имена,
qualified specialist weights в опубликованной области не найдены.

Старый FrameDetections: frame_idx/ts_ms/detections{cls,name,score,bbox_xyxy,kpts}.
15records предыдущих partial packs прошли реальные main Pydantic types в памяти;
это **не приёмка обновлённого Argus**. В прежней app нет external JSONL importer:
не класть файлы в кэш/БД и не писать отдельный REST sender. App сам делает события.
Current Argus uses **OpenCV INTER_LINEAR**, наш historical/local input — PIL;
не утверждать input parity этих двух preprocessors. Координаты уже исходные.

Совместимый готовый ONNX/head/tail/TPU kit от commit39dcc93d:
`/workspace/artifacts/safewatch-delivery/matvey_safewatch_delivery_v2.tar.gz`,
49,675,479bytes, SHA `7cfcf125189f4e0034d1de7a88033d465c0c6be453cee5f145a3ca3755f3892b`.
`docs/ML_HANDOFF_MATVEY.md`, `ml/models.matvey.yaml`, `ml/pipeline.matvey.yaml`,
`ml/safewatch.delivery.json`. Pose full/tail[1,56,8400], float ABI parity0;
Helmet[1,6,8400]+identity tail. Новая placement/newLinQ для этого kit NOT_RUN.
Registry refs: `matvey-pose-yolov8n@640-v1-acc5f51228b9` и
`matvey-helmet-yolov8n@640-v1-5c3af1f3b855`; не подменять файлы под старой version.
Стандартный app uploader использует mosprom_work/root-cache и mosprom_matvey
имена; это конфликт с текущей strict ownMatvey областью, **не обходить его**.
App source/registry/remote worker правит Марк, root передаёт модели/данные.

## 8. Проверки и воспроизведение

Последний full software log: `matvey_software_tests_v2.log` в scene-root,
**522tests OK (4skipped),7.432s**.9scene-validation tests проверяют пропуски,
неверные class IDs/poses/boxes, bool-index, provenance и непустую кадровую сетку;
empty detections не считаются пропуском. Tests не accuracy.

`matvey_independent_review_v2.json`: PASS7scenes/770sourceframes/2310input
hash+transform checks, JSON/JSONL equality, source byte/RGB/PTS, per-model gaps,
class maps, bbox/COCO17. Verified through client NumPy1.26.4; forward использовал
main NumPy2.5.4. `matvey_release_integrity_final.json`: integrityPASS и
**quality_release=NOT_QUALIFIED** одновременно. Не флипать quality flag из-за hashes.
Closing audit: `matvey_session_close_audit.json`. Проверенные логи сохранены;
во время подготовки этого handoff forward/tests/TPU заново не запускались.

```bash
cd /workspace/project
git branch --show-current
git status --short
git log -1 --format=%H

# Без нейросети/TPU; новое имя отчёта обязательно:
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
/workspace/.venvs/linq-client/bin/python -m ml.scene_packs --verify-only \
  --review-output /workspace/artifacts/NEW_matvey_scene_review.json

# Только если новый полный local run действительно нужен; outputs не перезаписывать:
OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2 \
YOLO_CONFIG_DIR=/workspace/artifacts/NEW_matvey_settings \
/venv/main/bin/python -m ml.scene_packs --root /workspace/artifacts/NEW_matvey_scene_packs
```

Нужен существующий `/venv/main` с Torch/Ultralytics для forward, client venv для
offline проверки. Main environment, drivers, compiler env не менять. `.venvs/linq-sdk`
отдельный, в этой итерации не использовался. `ffprobe` обязателен; нет тихого FPS
fallback. Повторять уже завершённые NN/RPC ради проверки сети не нужно.

## 9. История, которую нельзя потерять/начать заново

Предыдущий полный контекст: `docs/handoffs/SESSION_HANDOFF_20261024.md` (история
до полных scene packs), MODEL_INVENTORY/EVAL_REPORT/EXPERIMENTS/PROGRESS.
Eight-rule stage:8runnable rules,24synthetic cases,480software tests; технический
freeze, не8точных моделей. E012 CPU4corner ROI running0/46→0/46 REJECT, без2ndvariant.
Helmet confidence/tiling, history/upright и industrial PTQ гипотезы ранее reject;
не повторять без новых данных/директивы, не сбрасывать exhausted budgets.
Оригинальный mixed Pose TPU rejected по confidence PTQ; preferred Split-Pose.

Commit d06a6efd: explicit weak-video intake нового schema проверил160media и
34,172clock rows. GMD train123/val37, **whole-video weak labels only**, test empty;
это не bbox/frame/onset GT. MLP CPU fine-tune macroF1 .729532→.729532 gain0 REJECT.
Четыре GMD TCN/MLP heads[1,24,74] export-only/unselected; outer-fold нельзя выбрать
по test. New RGB-MIL source-only result в peer inventory gain.054093, но scalar
head не YOLO bbox ABI, deployment/LinQ false. Не включать автоматически в Argus.

Pre-steering WIP сохранён **вне Git**, не активирован:
`/workspace/artifacts/matvey-continuation-20261024/deferred-before-captain-deadline/`.
Там renderer и feature74 adapter/tests. Начальная feature review FAIL bitwise:
до1.49e-8 velocity drift из-за NumPy1.26 float32/scalar64 promotion vs NumPy2.5.
Не объявлять этот adapter закрытым/готовым и не начинать его вместо текущей задачи.
Полный diagnostic failure JSON сохранён рядом в matvey-continuation; новых
обучений/моделей из этого WIP не было.

## 10. Следующие действия для новой сессии

1. Проверить branch/status, прочитать этот файл/AGENTS/SCENE_PACKS runbook.
   Сначала дать команде готовые7scenes и2ZIP, если ещё не забрали; не пересчитывать.
2. Получить/прочитать обновлённый **реальный Argus contract**. Написать только ML
   форматный adapter по указанным полям, сохранить исходные PTS/frame IDs/model
   identity/source/product class maps и per-model backend/LinQ provenance. Не
   подменять отсутствующий контракт догадкой, не менять app/DB/rules.
3. Если требуется .1 floor, учесть отсутствие raw local outputs: отдельный
   согласованный all-frame local rerun на свободной GPU/CPU, новый pack version.
   Не считать это новой моделью/accuracy gain. Сначала проверить Training/GPU lock.
4. Fresh LinQ только после реального authorized own upload/receipt/binding и
   согласованного слота. Применить existing client/driver,1ownrequest, ограниченный
   sample, реальные correlated tensors/timings; любой UNKNOWN reconcile SAMEUUID.
   Без условий сохранить blocker, работать с готовыми local data.
5. Для положительных S01/S04/S08/quality нужны qualified models и scoped original
   scene/GT от Data/Training. Не начинать source discovery/GT invention, не
   мержить их branches, не выдавать generic contexts за положительные события.
6. До final release отдельно independent quality, actual app integration и
   timing/rights gates; пока открыты. Source/manual/synthetic facts не model proof.

Весь material large data/predictions/weights/TPU/raw tensors вне Git. Workspace
не считается volume-backed; verified external binary backup **нет**, approved
destination/account не предоставлен. Локальные ZIP не backup; никаких private
media uploads. Git push включает только owned code/docs/малые metadata.
Не менять VPN/SSH/routes/services, чужие queues/programs/kernels, baseline/ или
`mosprom_*_cut_ap9999*`. Не печатать/искать credential stores/полные process env.
Передача завершает эту сессию; новых автоматических исследований/циклов не начинать.
