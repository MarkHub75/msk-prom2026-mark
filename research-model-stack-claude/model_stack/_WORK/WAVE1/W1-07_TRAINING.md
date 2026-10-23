# W1-07 TRAINING — обучение, fine-tuning и жизненный цикл checkpoint

## 0. Шапка

- ID ячейки: **W1-07** (первая волна)
- Запрошено: Claude Sonnet 5.5, effort high
- Фактическая модель (из моего системного окружения): **Sonnet 5.5, model ID `claude-sonnet-5-5`**
- Начало: 2026-10-23 ~04:43 MSK; конец: 2026-10-23 ~05:00 MSK (время по системным часам рабочей машины, `date` показывал «RTZ 2026»; UTC+3 принято как MSK)
- Что сделано: прочитан код Ultralytics (tag v8.4.184), YOLOX (master), YOLOv5 (v7.0); выполнены **локальные пробы без обучения и без скачивания весов** (сборка моделей из yaml со случайной инициализацией, перенос весов между ними, синтетический checkpoint). Обучение не запускалось. Официальные предобученные `.pt` не скачивались и не десериализовались.
- Файлы-приложения: `W1-07_files\` (скрипты проб и их вывод; см. S09).

## 1. FLASH (для соседей)

1. **Ultralytics 8.4.x ведёт себя иначе, чем документация/мнемоника про 8.0–8.3.** За 2026 год в `main` добавлены: перенос скрытых слоёв cls-ветки при смене `nc` для моделей `n` (раньше они пропускались из-за ширины `c3 = max(ch[0], min(nc,100))`), **перенос строк cls-головы по совпадению имён классов (`cls_remap=True` по умолчанию)**, `cls_pw` (веса классов), `quantize=8` (QAT через NVIDIA ModelOpt), `optimizer=auto` → MuSGD/AdamW, EMA с «ремонтом» NaN, `time=` и т.д. Все выводы по обучению привязаны к **tag v8.4.184 (commit f7dd275e…)**; версию нужно **пиновать** (S01, W1-07-F01).
2. **Лог `Transferred N/N items from pretrained weights` теперь не доказывает, что голова классов обучена/перенесена.** В v8.4.184 счётчик включает «ремаппнутые по имени» тензоры, и при совпадении хотя бы одного имени класса показывает **100 % (499/499 для yolo11n)**, хотя последний conv каждой cls-ветки (6 тензоров у yolo11n, 12 у yolo26n) заново инициализирован и заполнен только по совпавшим строкам. Без совпадений имён показывает 493/499 (локальная проба W1-07-F10, S09). → W1-08: порядок/написание `names` в `data.yaml` теперь влияет на веса, а не только на подписи.
3. **`best.pt` по умолчанию выбирается по mAP50-95 (веса 0/0/0/1)**, а не по 0.1·mAP50+0.9·mAP50-95 (YOLOv5 v7.0 и Ultralytics ≤ v8.3.100). Граница версий: v8.3.100 → v8.3.200 (W1-07-F23). → evaluation.
4. **Контрольная точка в процессе обучения и после — разные форматы.** Во время обучения `last.pt/best.pt` — полные (ema fp16 + optimizer, `model=None`, `epoch=N`); в конце `strip_optimizer` превращает оба в «финальные» (`model`=EMA fp16, `ema/optimizer=None`, **`epoch=-1` → resume невозможен**). Прерванный прогон оставляет нестрипнутый `last.pt` — он пригоден для resume и для `load_checkpoint`, но `ckpt["model"]` в нём `None` (W1-07-F14–F16). → W1-10: экспорт берёт EMA, округлённый до fp16.
5. **Локальная среда по умолчанию — CPU-only torch** (`torch 2.9.1+cpu`, `torch.cuda.is_available()==False`, при том что `nvidia-smi` работает). Для обучения на RTX 4070 нужна CUDA-сборка torch (→ W1-09).
6. **Для LinQ-цепочки:** по W1-12/W1-01 (соседи, S10) LinQ принимает fp32 ONNX/TF-граф и квантует сам (PTQ по калибровке). Ultralytics-QAT (`quantize=8`, ModelOpt, Q/DQ-узлы) — ветка, **не подтверждённая** для LinQ; в базовый план обучения не включать (W1-07-H03).
7. Оригинальный `ultralytics/yolov5` **v7.0 не работает с torch ≥ 2.6 «из коробки»** (`torch.load` без `weights_only=False`; issues #13513, #13675), а `master` yolov5 зависит от пакета `ultralytics` (`from ultralytics.utils.patches import torch_load`). Если «yolo5s» LinQ ≡ оригинальный anchor-based YOLOv5s v7.0, обучение в «родном» репозитории требует отдельного окружения со старым torch либо master (W1-07-F31).

## 2. Резюме для оркестратора

- **Основной путь обучения — Ultralytics `YOLO("<модель>.pt").train(data=…)`** (или CLI `yolo detect train model=<модель>.pt data=… `). Весь путь «начальные веса → обучение → best.pt → загрузка для экспорта» прослежен по коду v8.4.184 с locators (разд. 6.1). Подтверждено: исходное `.pt` грузится через `load_checkpoint` (берёт **EMA**, приводит к fp32), новая `DetectionModel` строится из `yaml` чекпоинта с `nc` датасета, веса переносятся по совпадению **имя+форма**, меняется только то, что зависит от `nc`.
- **Что именно переносится при nc≠80** (локальная проба, 5 конфигов: yolo11n/s, yolo26n, yolov8n, yolov5u): у всех семейств заново создаётся только последний `Conv2d(c3→nc)` каждой cls-ветки (3 уровня × weight+bias = 6 тензоров; у YOLO26 ещё `one2one_cv3` → 12). Бэкбон, neck, box-ветки (`cv2`), скрытые слои cls-ветки переносятся (для `n`-моделей — благодаря новому коду «перестройки на ширину источника»; в голой `intersect_dicts` у yolo11n переносилось бы 448/499). Строки cls-conv, чьи **имена классов совпали** (регистр/пробелы игнорируются), копируются из источника, включая bias.
- **Для нашей задачи это даёт «бесплатный» тёплый старт для `person`** (имя совпадает с COCO), но **не для** `helmet`/`hardhat`/`vest`/`no_helmet`… (в COCO их нет). Тёплый старт из своего прошлого чекпоинта по совпадающим именам — тоже работает (проба D/E).
- **Resume**: требует нестрипнутого `last.pt` (`epoch>=0`, optimizer не `None`), разрешает менять только узкий список аргументов (`imgsz, batch, device, close_mosaic, augmentations, save_period, workers, cache, patience, time, freeze, val, plots, channels_last, distill_model, save_dir`); остальное игнорируется с предупреждением. **При изменении `nc` resume ломается** (strict `load_state_dict` EMA, размеры буферов optimizer) — вывод из кода, эмпирически не проверено (W1-07-I05). **При том же `nc`, но другом порядке `names` — вероятна тихая рассинхронизация** весов EMA и live-модели (W1-07-H01).
- **Стоимость**: в первичных материалах **нет** ни одного опубликованного времени обучения на потребительской GPU. Есть: YOLOv5 README «1/2/4/6/8 суток на V100 для n/s/m/l/x» (COCO, 300 эпох — reported_measurement), рецепт YOLO26 (Objects365 150 эпох + COCO 40–245 эпох, batch 128). Времени на RTX 4070 нет → **только измерение на месте** (эксп. E1/E2). Верхнюю границу времени можно задать **аргументом `time=<часы>`**: он переопределяет `epochs` и пересчитывает расписание LR после первой эпохи (код L678–684).
- **Главные точки риска**: (1) дрейф поведения версий Ultralytics; (2) «зелёный» лог при фактически новой/неверно упорядоченной голове; (3) `optimizer=auto` меняет оптимизатор и lr по числу итераций (порог 10000) и **игнорирует `lr0`**; (4) AMP-проверка скачивает `yolo26n.pt` и без сети молча пропускается; (5) NaN: AdamW+AMP на YOLO26 (issue #24063), поведение «не сохранять NaN-EMA» (issue #24871); (6) `fraction` берёт **первые N отсортированных** изображений, не случайные; (7) модификация архитектуры (замена C2PSA/активаций) ломает/обесценивает перенос весов.
- **Главные разрывы (unknown)**: ни одна практическая проверка (реальный `train`, реальный resume, реальный `best.pt`) не выполнена; не известны ограничения LinQ на архитектуру (SiLU, C2PSA, Resize, DFL, end2end-голова), от которых зависит, придётся ли менять YAML и терять часть предобучения (→ linq_platform, W1-12).
- **Рекомендованный минимальный прогон** — разд. 9 (E1–E5): ≥ 5 мин на CPU/GPU, ловит загрузку весов, градиенты (overfit малой выборки), сохранение/strip, resume, NaN/AMP.

## 3. Факты

Формат: ID — утверждение — основание — источник/локатор — область применимости — статус проверки — оговорки. Все номера строк относятся к **ultralytics tag v8.4.184, commit f7dd275e5853801674ca78ef51896617bb5362ba**, если не указано иное.

### 3.1 Версии и конфигурация

- **W1-07-F01** — На 2026-10-23 ~04:44 MSK latest release `ultralytics/ultralytics` = **v8.4.184** (опубликован 2026-10-22T17:41:34Z); `main` в тот момент = `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8` (2026-10-22T20:27:18Z), tag v8.4.184 → `f7dd275e5853801674ca78ef51896617bb5362ba` (commit date 2026-10-22 19:39:36 +0200). PyPI `ultralytics` latest = 8.4.184 (список версий через `pip index versions`). — artifact_metadata/local_observation — S01, S05 — проверено: `gh release list`, `gh api`, `pip index`. Оговорка: релизы выходят каждые 1–3 дня; «latest» к моменту хакатона может измениться.
- **W1-07-F02** — `default.yaml` (v8.4.184) содержит значения по умолчанию: `epochs 100, patience 100, batch 16, imgsz 640, pretrained True, cls_remap True, optimizer auto, close_mosaic 10, amp True, lr0 0.01, lrf 0.01, momentum 0.937, weight_decay 0.0005, warmup_epochs 3.0, warmup_momentum 0.8, warmup_bias_lr 0.1, box 7.5, cls 0.5, cls_pw 0.0, dfl 1.5, nbs 64, fraction 1.0, freeze (пусто), multi_scale 0.0, rect False, cache False, workers 8, seed 0, deterministic True, time (пусто), quantize (пусто), distill_model (пусто)`. — source_code — S01 `ultralytics/cfg/default.yaml` L10–L128 — прочитан файл.
- **W1-07-F03** — Рецепт YOLO26 (официальные чекпоинты): Objects365v1 pre-train 150 эпох → COCO fine-tune; оба этапа 640×640, MuSGD, batch 128. COCO-этап: epochs n/s/m/l/x = 245/70/80/60/40; lr0 n 0.0054, s–x 0.00038; `warmup_epochs ≈ 1`; `close_mosaic 10`. Эти значения «зашиты» в `ckpt["train_args"]`. — author_statement (документация репозитория) — S02 `docs/en/guides/yolo26-training-recipe.md` — документ прочитан целиком; **значения в самих `.pt` не проверены** (чужие чекпоинты не десериализовались).
- **W1-07-F04** — Документация рекомендует: «A good starting point is 300 epochs» (guides/model-training-tips; пересказ WebFetch-модели, дословность не гарантирована); для fine-tune: `patience 10–20`, `warmup` ≈ 1 эпоха, малые датасеты (<1000 изображений) `mosaic=0.5, mixup=0, copy_paste=0, optimizer=AdamW, lr0=0.001, epochs≈50, patience=20, freeze=10`. — author_statement — S02 `finetuning-guide.md`, `yolo26-training-recipe.md` (разд. «Small datasets»), S04 — прочитано. Это рекомендации вендора, не измерения на нашей задаче.

### 3.2 Загрузка весов, смена числа классов

- **W1-07-F05** — Три способа старта и их фактический путь (код):
  - `YOLO("m.pt").train(data=…)`: `Model.train` (`engine/model.py` L807+; блок L889–L896) при непустом `self.ckpt` и `resume` не заданном вызывает `trainer.get_model(weights=self.model, cfg=self.model.yaml)` → `DetectionTrainer.get_model` (`models/yolo/detect/train.py` L183–L199): создаёт `DetectionModel(cfg, nc=data["nc"], ch=data["channels"])`, **выставляет `model.names=data["names"]` ДО загрузки** (`set_model_names_for_load` L145–L149, если `cls_remap`), затем `model.load(weights)` (`nn/tasks.py` L326–L380). `cfg` берётся **из чекпоинта** (`self.model.yaml`), а не из вашего yaml.
  - `YOLO("m.yaml").load("m.pt").train(…)`: `Model.load` (L320+) грузит веса в 80-классовую модель из yaml, ставит `self.ckpt`; далее то же, что выше, но `cfg` — ваш yaml (путь для кастомной архитектуры).
  - `YOLO("m.yaml").train(…)`: `self.ckpt` пуст → `BaseTrainer.setup_model` (`engine/trainer.py` L873–L907): веса `None`, если `pretrained` не строка-путь; `pretrained=True` для yaml **веса не качает** (подтверждено и текстом docs, S03/S02).
  - `pretrained="путь.pt"` (строка) → `load_checkpoint(путь)` (L887–L888 / `model.py` L891–L892) — явный источник весов независимо от `model=`.
  — source_code — статус «прочитан код»; цепочка `YOLO(.pt).train` подтверждена частично локально (шаг `get_model→load` воспроизведён пробой S09, без `Model.train`).
- **W1-07-F06** — `load_checkpoint` (`nn/tasks.py` L2022–L2068): `candidate = ckpt.get("ema") or ckpt.get("model")` — **берётся EMA, если он есть**; затем `.float()`, `model.args` из `ckpt["train_args"]`, `model.pt_path`, `.eval()`. `torch_safe_load` (L1875–L2019) использует `torch_load` с `weights_only` **выключенным по умолчанию**; безопасный режим включается переменной окружения `ULTRALYTICS_SAFE_LOAD` (`utils/__init__.py` L75, `nn/tasks.py` L1898–L1900). Оригинальные чекпоинты ultralytics/yolov5 (`models.*` в pickle) дают явную ошибку `TypeError … NOT forwards compatible` (L1971–L1980). — source_code.
- **W1-07-F07** — `BaseModel.load` (L326–L380) в v8.4.184: (а) берёт `weights.get("ema") or weights["model"]` → fp32 state_dict; (б) если голова `Detect`, обе модели не fused и входные ширины `cv2[i][0].conv.in_channels` совпадают — **перестраивает cls-ветки (`cv3`, `one2one_cv3`) цели на ширину источника** (глубокая копия источника, новый последний `Conv2d(in, nc_new, 1)`), затем `head.bias_init()`; (в) `_remap_cls_by_names` (L382–L450); (г) `intersect_dicts(csd, self.state_dict())` — перенос по **имени и форме** (`utils/torch_utils.py` L723–L735), `load_state_dict(strict=False)`; (д) особая обработка `model.0.conv.weight` при другом числе входных каналов; (е) лог `Transferred {len_updated_csd}/{len(self.model.state_dict())} items from pretrained weights` (L378), где `len_updated_csd = len(updated_csd) + cls_remapped` (L365). — source_code.
- **W1-07-F08** — `_remap_cls_by_names` (L382–L450): сопоставляет имена классов цели и источника (`str.strip().lower()`); пропускает, если у любой стороны имена — заглушки `{0:"0",1:"1",…}` (L409), если ни одно имя не совпало, или если число и порядок имён идентичны (тогда копирует `intersect_dicts`); копирует строки `weight` (если форма остальных измерений совпала) и `bias` **только в конечные cls-conv Detect-веток** (`cv3.i`, `one2one_cv3.i`, `proto.semseg`); совпавшие тензоры удаляются из `csd`. Лог: `Remapped {n_match}/{tgt_nc} cls head rows from pretrained weights by class name` (L449). — source_code; пример поведения — F10.
- **W1-07-F09** — Конструктор `Detect` (`nn/modules/head.py` L38+): `c2 = max(16, ch[0]//4, reg_max*4)`, `c3 = max(ch[0], min(nc, 100))`; `bias_init`: box-bias=2.0, cls-bias = `log(5/nc/(640/stride)²)`. Значит для `n`-моделей (`ch[0]=64`) ширина скрытых cls-слоёв зависит от `nc` (nc≤64 → 64, nc=80 → 80); для `s` и крупнее (`ch[0]≥128`) при nc≤100 не зависит. — source_code. Следствие: до PR #26570 (2026-10-07) для `n`-моделей при малом `nc` вся cls-ветка не переносилась.
- **W1-07-F10** — **Локальная проба переноса (random-init источник nc=80 → цель nc=4, `DetectionModel.load`)**, версия ultralytics 8.4.184 (колесо PyPI), torch 2.9.1+cpu; вывод: `W1-07_files\out_transfer_probe.txt`, `out_transfer_probe2.txt`.

  | Конфиг | Тензоров в цели | «Голая» `intersect_dicts` | После `load` (совпало ≥1 имя) | Нет совпадений имён | Не равны источнику |
  |---|---|---|---|---|---|
  | yolo11n | 499 | 448 | **499/499** | 493/499 | 6 (`model.23.cv3.{0,1,2}.2.{weight,bias}`) |
  | yolo11s | 499 | 493 | 499/499 | — | 6 |
  | yolo26n | 708 | 606 | 708/708 | (док.: 696/708) | 12 (+`one2one_cv3`) |
  | yolov8n (yolov8.yaml) | 355 | 319 | 355/355 | — | 6 (`model.22.cv3…`) |
  | yolov5u (cfg/models/v5/yolov5.yaml, scale n) | 427 | 391 | 427/427 | — | 6 (`model.24.cv3…`) |

  Ширина скрытого слоя cls-ветки yolo11n/yolo26n у цели после загрузки = 80 (как у источника), а не 64, которые дал бы yaml с nc=4. Проверено: случай A (нет совпадающих имён) → 493/499 для yolo11n; B (nc=1, `person`) → `Remapped 1/1`, 499/499; C (имена цели — заглушки) → 493/499; D (свой nc=4 → новый nc=6 с тремя общими именами и другим порядком) → `Remapped 3/6`, строки совпали побайтно с исходными; E (тот же nc=4, другой порядок имён) → `Remapped 4/4`, строки переставлены верно; F (имена источника — заглушки) → 493/499. — local_observation; **ограничение**: источником служили случайно инициализированные модели из yaml, а не официальные `.pt` (набор ключей и форм определяется архитектурой, так что счётчики применимы к официальному `yolo11n.pt` при той же архитектуре; это inference). Числа «после load» включают remap и поэтому не отличают «голову обучать с нуля» от «голова перенесена» (см. FLASH-2).
- **W1-07-F11** — Документация: «fine-tuning YOLO26n from COCO (80) onto a 5-class dataset transfers 696 of 708 weight tensors, plus any compatible classification rows matched by name» (S02 `finetuning-guide.md`, разд. «How Pretrained Weight Transfer Works»). — author_statement; совпадает с локальной пробой: 708 тензоров, 12 из них (cv3/one2one_cv3 последние conv) новые. 
- **W1-07-F12** — Модификации архитектуры и перенос (проба 3, `out_probe3.txt`, yolo11n): (а) замена `C2PSA` (слой 10) на `nn.Identity` с сохранением индексов → `Transferred 451/457`, параметров 2 355 884 против 2 590 620 (−234 736): индексы не сдвинулись, ключи совпали; (б) замена SiLU→ReLU через `Conv.default_act = nn.ReLU()` до сборки → 493/499 (ключи и формы те же, активации безпараметровые). Если же **удалить** слой (индексы сдвигаются), ключи вида `model.N.*` перестанут совпадать с весами по именам — перенос пойдёт по совпадению «имя+форма» и может молча сопоставить неродственные слои с одинаковой формой (inference из `intersect_dicts`; удаление со сдвигом локально не проверялось). — local_observation + inference.
- **W1-07-F13** — Заморозка (`freeze`): `engine/trainer.py` L381–L409. int `N` → слои `0..N-1` (имена вида `model.{i}.`); список → индексы либо строки-подпути вида `"23.cv2"`; **`.dfl` замораживается всегда**; параметры с `requires_grad=False`, не попавшие в список, принудительно включаются обратно (warning); если заморожено всё — `RuntimeError`. Замороженные BatchNorm2d переводятся в `eval()` (`_model_train` L760–L766), т. е. **статистики BN замороженных слоёв не обновляются**. Локальная проба на yolo11n nc=4: `freeze=10` → 43.1 % параметров (1 115 760 из 2 590 620), `freeze=11` → 52.7 % (весь бэкбон 0–10), `freeze=[0,1,2]` → 0.5 %, `freeze=["23.cv2"]` → 14.7 %; слой 10 = `C2PSA`, 9 = `SPPF`, 23 = `Detect` (`out_transfer_probe2.txt`). У yolov8/yolov5u (yaml): бэкбон — слои 0–9, поэтому `freeze=10` покрывает весь бэкбон; у yolo11/yolo26 бэкбон 0–10. — source_code + local_observation (подсчёт имитирует логику трейнера, сам трейнер не запускался).

### 3.3 Checkpoint: что сохраняется

- **W1-07-F14** — `BaseTrainer.save_model` (L768–L837) пишет за каждую эпоху (при `save=True` или на финальной): словарь `{epoch, best_fitness, stopper{best_fitness,best_epoch}, model: None, ema (глубокая копия EMA в fp16, NCHW, criterion=None, NaN→0 через nan_to_num_), updates, modelopt (QAT-состояние или None), optimizer (state_dict, тензоры в fp16 кроме step/exp_avg/exp_avg_sq/square_avg), scaler, train_args (vars(args)), train_metrics (метрики + fitness), train_results (results.csv как dict), date, version, git{root,branch,commit,message,origin}, license, docs}`. Всегда пишет `last.pt`; `best.pt` — если `best_fitness == fitness`; `epoch{N}.pt` при `save_period>0`. — source_code. **Поле `model` равно `None` именно в этом виде** (комментарий в коде: «resume and final checkpoints derive from EMA»).
- **W1-07-F15** — В конце обучения `final_eval` (L1005–L1022) вызывает `strip_optimizer(last)` и `strip_optimizer(best, updates={"train_results": …})`. `strip_optimizer` (`utils/torch_utils.py` L895–L960): `x["model"] = x["ema"]`, `.half()`, `requires_grad=False`, `criterion=None`, `args` → dict; `optimizer, best_fitness, stopper, ema, updates, scaler = None`; **`epoch = -1`**; `train_args` отфильтрованы по `DEFAULT_CFG_KEYS`; метаданные `date/version/license/docs` перезаписываются. Затем best.pt валидируется заново. — source_code.
- **W1-07-F16** — **Локальная проба жизненного цикла** (`out_ckpt_lifecycle_probe.txt`; синтетический checkpoint, собранный по коду F14 из собственной random-init модели, не результат реального trainer): до strip — `model=None`, `ema`≠None (fp16), `epoch=1`, `optimizer`≠None, 10.7 МБ; после `strip_optimizer` — `model`≠None (fp16, `requires_grad=False`), `ema=None`, `optimizer=None`, `epoch=-1`, 5.44 МБ; `load_checkpoint` обеих версий возвращает `DetectionModel` в **fp32** с `names={0:'person',…}` и `stride=[8,16,32]`. — local_observation; оговорка: реальный `last.pt/best.pt` из trainer не наблюдался.
- **W1-07-F17** — Следствия для экспорта (→ W1-10): веса в checkpoint — **fp16-округлённый EMA**; `load_checkpoint` возвращает fp32 с этими округлёнными значениями; `names` и `nc` берутся из атрибутов сохранённого модуля (`update_attr(include=["yaml","nc","args","names","stride","class_weights"])`, L649); `train_args` внутри checkpoint содержит локальные пути (`data`, `save_dir`). — source_code (L649, L789–L796).
- **W1-07-F18** — Resume: `check_resume` (L1024–L1069): читает `args` из checkpoint (`load_checkpoint(last)[0].args`), подставляет `data` из текущего вызова, после чего разрешает переопределять только `{imgsz, batch, device, close_mosaic, augmentations, save_period, workers, cache, patience, time, freeze, val, plots, channels_last, distill_model, save_dir}`; прочее → warning «Resume ignores […], using checkpoint values». `resume_training` (L1128–L1145): `start_epoch = ckpt["epoch"]+1`, `assert 0 < start_epoch < epochs` (иначе «nothing to resume»); `Model.train` для `resume=True` требует `ckpt["epoch"] >= 0` и `optimizer is not None`, иначе предупреждает и **стартует новое обучение** (`model.py` L877–L887). `_load_checkpoint_state` (L1071–L1086): `optimizer.load_state_dict`, `scaler`, **`ema.ema.load_state_dict(ckpt["ema"].float().state_dict())` (strict)**, `ema.updates`, `best_fitness`, `stopper`. — source_code. Документация (S03, WebFetch-пересказ): «Pass an explicit `data=` alongside `resume` to continue on a different dataset» — код допускает подмену `data` (L1037–L1038), но поведение при другом `nc`/`names` не описано.
- **W1-07-F19** — Восстановление при NaN: `_handle_nan_recovery` (L1088–L1126): при NaN/Inf в loss или fitness (кроме первой эпохи) до 3 раз перезагружает `last.pt` (EMA → модель, optimizer, scaler); после 3 попыток — `RuntimeError`. `save_model` (L776–L785) перед записью «чинит» NaN в EMA копированием из живой модели, где она конечна, затем `nan_to_num_`. Корень issue #24871 (в v8.4.70 checkpoint не сохранялся при NaN в EMA) здесь, судя по коду, устранён. — source_code; issue — S08.

### 3.4 Цикл обучения, оптимизатор, AMP, loss

- **W1-07-F20** — `_setup_train` (L341–L466): порядок — `setup_model` → `set_model_attributes` (`nc`, `names`, `args` на модель) → `check_imgsz` (кратно `max stride`, ≥ 32) → [QAT] → `attempt_compile` → freeze → **`check_amp`** → `DistillationModel` (если `distill_model`) → DDP → `auto_batch` (если `batch<1`) → `_build_train_pipeline` (даталоадеры, `accumulate = max(round(nbs/batch),1)`, масштаб `weight_decay`, `build_optimizer`, `_setup_scheduler`) → validator → `set_class_weights` → `ModelEMA` → `resume_training`. — source_code.
- **W1-07-F21** — `build_optimizer` (L1155–L1246): при `optimizer=auto` (по умолчанию) **игнорирует `lr0`**: `iterations = ceil(len(dataset)/max(batch, nbs)) * epochs` (L326); если `iterations > 10000` → **MuSGD**, lr 0.01, momentum 0.9, иначе **AdamW** с `lr = round(0.002*5/(4+nc), 6)` (= `0.01/(4+nc)`), momentum 0.9, и `warmup_bias_lr=0.0`; выбор записывается обратно в `args.optimizer/lr0` (поэтому resume воспроизводит его). Параметры делятся на группы: bias (без decay), BN/norm-веса (без decay), остальные веса (decay), для MuSGD — отдельная группа для 2D/4D параметров, а **голова cls (`cv3`, `one2one_cv3`) получает lr×3** (L1225–L1236). Примеры для 4 классов: lr_fit = 0.00125. — source_code; расчёт `lr_fit` — inference (арифметика по формуле).
- **W1-07-F22** — Шаг оптимизации (L909–L920) и цикл (L468–L700): `GradScaler`, `unscale_`, **`clip_grad_norm_(max_norm=10.0)`**, `step`, `zero_grad`, `ema.update`. Warmup (L520–L538): `nw = round(min(warmup_epochs, epochs-1)*nb)`; lr поднимается 0→`initial_lr*lf`, bias-lr падает с `warmup_bias_lr` до lr0, momentum `warmup_momentum→momentum`, `accumulate` растёт 1→`nbs/batch`. Расписание: линейное `max(1-x/epochs,0)*(1-lrf)+lrf` или `cos_lr` (L268–L274). `close_mosaic`: на первом шаге эпохи `>= epochs - close_mosaic` включается `_close_dataloader_mosaic` (`mosaic=mixup=copy_paste=cutmix=0`, `data/dataset.py` L389–L399). При OOM в первой эпохе — до 3 повторов с уменьшением batch вдвое (L566–L601). — source_code.
- **W1-07-F23** — Fitness для `best.pt` = `0·P + 0·R + 0·mAP50 + 1·mAP50-95` (`utils/metrics.py` L1011–L1014, класс `Metric`, v8.4.184). Проверено по тегам: `w=[0,0,0.1,0.9]` на v8.1.0, v8.2.0, v8.3.0, v8.3.100; `w=[0,0,0,1.0]` на v8.3.200, v8.4.0, v8.4.100. YOLOv5 v7.0: `[0,0,0.1,0.9]` (`utils/metrics.py` L17–L20). EarlyStopping (`torch_utils.py`, class EarlyStopping): останов при `epoch - best_epoch >= patience`, `patience=100` по умолчанию. — source_code + artifact_metadata (чтение файлов по тегам через `gh api`).
- **W1-07-F24** — Loss (`utils/loss.py` v8.4.184): `v8DetectionLoss` (L354–L511): BCE по классам (`BCEWithLogitsLoss(reduction="none")`), цели — soft-оценки TAL; `TaskAlignedAssigner(topk=10, alpha=0.5, beta=6.0)`; box = CIoU, dfl = DFL (если `reg_max>1`) либо L1 (YOLO26, `reg_max=1`); усиления `box 7.5, cls 0.5, dfl 1.5`; потери умножаются на batch size (`loss*batch_size`). Для end2end-голов (YOLO26, `one2one_cv2` есть) — `E2ELoss` (L1283–L1315): one2many (`topk=10`) + one2one (`topk=7, topk2=1`) с весами `o2m` 0.8→0.1 по эпохам (decay от `hyp.epochs`), в логе — компоненты one2one. — source_code.
- **W1-07-F25** — Дисбаланс классов: новый `cls_pw ∈ [0,1]` (default 0.0 = выкл): веса `w_c = (1/count_c)^cls_pw`, классы без обучающих меток получают среднее, затем нормировка на среднее=1; считается по `train_loader.dataset.labels` (до аугментаций); применяется как **множитель на все BCE-ячейки колонки класса** (`bce_loss *= class_weights`, `loss.py` L465–L466), т. е. и на позитивы, и на негативные ячейки класса — это не `pos_weight` YOLOv5. Реализация: `DetectionTrainer.get_class_counts/compute_class_weights/set_class_weights` (L151–L181); PR #26599 (2026-10-08) «Keep classes without train labels neutral». В Ultralytics нет аналога YOLOv5 `--image-weights` (grep по пакету — 0 совпадений). — source_code.
- **W1-07-F26** — Проверка AMP (`utils/checks.py` L987–L1040): для CUDA отключает AMP по регулярке имени GPU (`1660|1650|1630|t400|t550|t600|t1000|t1200|t2000|k40m`; RTX 4070 не совпадает); затем сравнивает вывод FP32 vs AMP на `bus.jpg` модели `yolo26n.pt`, **скачивая её** (`WEIGHTS_DIR/yolo26n.pt`); при `ConnectionError` — «checks skipped», AMP остаётся включённым; при `AssertionError` — AMP выключается. `amp="bf16"` пропускает проверку (L414). — source_code. Известные проблемы: issue #24063 (YOLO26m, AdamW lr0=0.005, amp=True, 8.4.24 — loss NaN к 4-й эпохе; SGD работал; рекомендации в треде: `amp=False`, снизить `lr0`) — reported (S08).
- **W1-07-F27** — `time=<часы>` (L678–L684, L606–L614): после каждой эпохи `epochs = ceil(time*3600 / mean_epoch_time)`, пересоздаётся scheduler, warmup пересчитывается; останов по времени. Переопределяет `epochs` (default.yaml L13). `fraction` (`data/base.py` L224–L226): `count = fraction (int>1) или round(N*fraction)`, берётся `im_files[:count]` от **отсортированного** списка → не случайная подвыборка. — source_code.
- **W1-07-F28** — `channels_last`: авто-включается для CUDA-обучения на не-Windows; на Windows отключено после сообщения мейнтейнеров (issue #26105: замедление 2.7 it/s → 1.2 s/it на RTX 5090 при NHWC). МногогPU на Windows с официальными колёсами torch≥2.4 «не работает» (S03, пересказ). — source_code (trainer.py L345–L353) + reported_measurement (issue #26105, один пользователь; условия: RTX 5090, Windows) — S08, S03. ОС команды **не установлена** — применимо только если окажется Windows.
- **W1-07-F29** — QAT: `quantize=8` (или `int8`) → `prepare_qat` (`torch_utils.py` L438–L488): подставляет **NVIDIA ModelOpt** `INT8_DEFAULT_CFG` (fake-quant на Conv/Linear, диапазоны калибруются по 8 батчам и далее фиксированы), выходные conv головы остаются float; `torch.onnx.export` пишет Q/DQ; нужны `nvidia-modelopt>=0.44, huggingface_hub` (авто-установка через `check_requirements`). — source_code. К LinQ не относится напрямую: LinQ-компилятор принимает fp32 и сам квантует (S10, W1-12) — **совместимость Q/DQ с LinQ не установлена**.

### 3.5 YOLOX

- **W1-07-F30** — YOLOX (Megvii-BaseDetection/YOLOX, master `6ddff4824372906469a7fae2dc3206c7aa4bbaee`; последний release 0.3.0 от 2022-04-22; последний commit в `main` 2025-06-08):
  - Конфиг — `Exp`-файл: `num_classes=80`, `depth/width`, `input_size=(640,640)`, `multiscale_range=5`, `max_epoch=300`, `warmup_epochs=5`, `basic_lr_per_img=0.01/64` (lr = это × batch), `scheduler="yoloxwarmcos"`, `no_aug_epochs=15`, `min_lr_ratio=0.05`, `ema=True`, `weight_decay=5e-4`, `momentum=0.9`, `eval_interval=10`, `mosaic_prob=1, mixup_prob=1, degrees 10, shear 2` (`yolox/exp/yolox_base.py` L14–L110). Пример для кастомных данных: `exps/example/custom/yolox_s.py` (`num_classes=71`, `eval_interval=1`).
  - Fine-tune: `-c ckpt.pth` без `--resume` → `load_ckpt(model, ckpt["model"])` (`core/trainer.py` L336–L342; `utils/checkpoint.py` L10–L29): для каждого ключа модели при отсутствии ключа или **несовпадении формы — `logger.warning` и пропуск** (для `cls_preds` при num_classes≠80 — предупреждения «Shape of … in checkpoint is …, while … in model is …»; обучаем-с-нуля остаются только эти тензоры; число предупреждений = число cls-тензоров; точное число не наблюдалось). `model.head.initialize_biases(1e-2)` вызывается в `get_model` **до** загрузки весов (L127), поэтому у перенесённых слоёв bias заменится предобученным, у новых — останется prior.
  - Resume (`--resume`, опционально `-c`, `-e`): `model.load_state_dict(ckpt["model"])` (**strict**), `optimizer.load_state_dict`, `best_ap`, `start_epoch` (L312–L335). В `save_ckpt` (L399–L415) в `"model"` кладётся `state_dict` **EMA, если `ema=True`** → при resume EMA-веса становятся «живыми» весами, а EMA заново создаётся из модели (`ModelEMA(model, 0.9998)`, `updates = max_iter*start_epoch`). Сохраняются `latest_ckpt.pth` каждую эпоху, `last_epoch_ckpt.pth`/`best_ckpt.pth` после eval, `last_mosaic_epoch_ckpt.pth` на границе `no_aug_epochs`.
  - Заморозка: только через переопределение `get_model` с `freeze_module(model.backbone.backbone)` (`docs/freeze_module.md`; функция `yolox/utils/model_utils.py` L131).
  - Loss (`yolo_head.py` L403–L404): `5.0·iou + obj + cls (+ l1 после выключения mosaic)`; SimOTA-назначение. При `no_aug` (последние `no_aug_epochs`) включаются L1-loss и `eval_interval=1` (`trainer.py` L220–L230).
  — source_code; обучения/загрузки не выполнялись.

### 3.6 YOLOv5 (ultralytics/yolov5)

- **W1-07-F31** — YOLOv5 v7.0 (`915bbf294bb74c859f0b41f1c23bc395014ea679`, release 2022-11-22; `master` = `af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce`, 2026-10-21):
  - `train.py` L113–L124: при `.pt` weights: `torch.load` → `Model(cfg or ckpt['model'].yaml, nc=nc, anchors=hyp.get('anchors'))` → `csd = intersect_dicts(ckpt['model'].float().state_dict(), model.state_dict(), exclude=['anchor'] if (cfg or hyp.get('anchors')) and not resume else [])` → `strict=False` → `Transferred {len(csd)}/{len(model.state_dict())} items from {weights}`. Голова (`model.24.m.*`, conv на `na*(5+nc)`) при nc≠80 пропускается автоматически по форме; **якоря берутся из чекпоинта**, `check_anchors` (AutoAnchor) может пересчитать их под датасет (L195–L196; `--noautoanchor` отключает).
  - Масштабирование loss: `hyp['box'] *= 3/nl; hyp['cls'] *= nc/80*3/nl; hyp['obj'] *= (imgsz/640)²*3/nl` (L234–L236); `cls_pw/obj_pw` — `pos_weight` BCE (`utils/loss.py` L100–L101); `model.class_weights` вычисляются, но используются только для `--image-weights` (выборка изображений).
  - Freeze: `--freeze N` (слои `model.0..N-1`; «backbone=10»), L135–L141. Resume: `--resume` (`smart_resume`, `utils/torch_utils.py` L361–L378): optimizer, EMA, `best_fitness`, `start_epoch`; `ckpt['model']` и `ckpt['ema']` сохраняются оба в fp16 вместе с `optimizer` и `opt` (L372–L388), по окончании `strip_optimizer` для last/best. Fitness `[0,0,0.1,0.9]`.
  - Время: README: «Training times for YOLOv5n/s/m/l/x are 1/2/4/6/8 days on a V100 GPU» (README L194–L195, COCO 300 эпох) — author_statement/reported_measurement без деталей данных.
  - `torch.load` без `weights_only=False` в v7.0 (train.py L123, models/experimental.py L79) → с torch ≥ 2.6 ломается (issues #13513, #13675; ответ мейнтейнера: использовать master или откатить torch ≤ 2.5.1); `master` использует `ultralytics.utils.patches.torch_load` (зависит от пакета ultralytics). — source_code + reported (issues); локально не воспроизводилось.
  — прочитан код; не запускалось.

## 4. Источники

- **W1-07-S01** — Репозиторий `ultralytics/ultralytics`, tag **v8.4.184** → commit `f7dd275e5853801674ca78ef51896617bb5362ba` (2026-10-22 19:39 +0200); клон `SCRATCH\repos\W1-07\ultralytics` (depth 1). Файлы: `engine/trainer.py` (1413 строк), `engine/model.py`, `models/yolo/detect/train.py` (256), `nn/tasks.py` (2410), `nn/modules/head.py`, `utils/torch_utils.py` (1258), `utils/loss.py` (1508), `utils/tal.py`, `utils/checks.py`, `utils/metrics.py`, `data/base.py`, `data/dataset.py`, `data/utils.py`, `cfg/default.yaml`, `cfg/models/{11,26,v5,v8}/*.yaml`. Проверено 2026-10-23 04:44–04:55 MSK. Лицензия кода AGPL-3.0 (по заголовкам; детали → W1-04).
- **W1-07-S02** — Документация в репозитории @ тот же commit: `docs/en/guides/finetuning-guide.md` (235 строк), `docs/en/guides/yolo26-training-recipe.md` (337 строк), `docs/en/models/{yolo11,yolo26}.md`. Прочитано полностью (первые два).
- **W1-07-S03** — https://docs.ultralytics.com/modes/train/ — веб-страница, на момент проверки 2026-10-23 помечена «Updated 3 days ago»; получена через WebFetch (**пересказ малой модели, не дословная копия**; цитаты нужно сверять с исходником).
- **W1-07-S04** — https://docs.ultralytics.com/guides/model-training-tips/ — аналогично, WebFetch-пересказ, 2026-10-23.
- **W1-07-S05** — PyPI `ultralytics` 8.4.184 (установлено в `SCRATCH\venv-W1-07` с `--no-deps`; окружение: Python 3.13.9, torch 2.9.1+cpu, torchvision 0.24.1, numpy 2.3.4, PyYAML 6.0.3, polars 2.0.0, opencv-python-headless 5.0.0.93) — `W1-07_files\env_versions.txt`. Конфиг Ultralytics перенаправлен в SCRATCH через `YOLO_CONFIG_DIR`.
- **W1-07-S06** — `Megvii-BaseDetection/YOLOX` master `6ddff4824372906469a7fae2dc3206c7aa4bbaee` (commit 2025-06-08); latest release 0.3.0 (2022-04-22T07:20:43Z); клон `SCRATCH\repos\W1-07\YOLOX`. Файлы: `yolox/core/trainer.py` (428), `yolox/exp/yolox_base.py` (358), `yolox/utils/checkpoint.py`, `yolox/utils/ema.py`, `yolox/models/{yolox,yolo_head}.py`, `tools/train.py`, `exps/default/*.py`, `exps/example/custom/yolox_s.py`, `docs/freeze_module.md`. Замечание: при клонировании на Windows git сообщил о проблеме с одним файлом `demo/ncnn/android/...yoloXncnn.java` (путь/регистр); для задачи несущественно; `yolox/tools/` в рабочей копии содержит только `__init__.py` (в репозитории CLI-модуль — симлинк на `tools/`; документация вызывает `python -m yolox.tools.train`) — на Windows запускать `tools/train.py`.
- **W1-07-S07** — `ultralytics/yolov5` tag **v7.0** → `915bbf294bb74c859f0b41f1c23bc395014ea679` (release 2022-11-22); `master` = `af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce` (2026-10-21). Клон v7.0 `SCRATCH\repos\W1-07\yolov5`; для master прочитаны только строки `torch.load` через `gh api`. Файлы v7.0: `train.py` (633), `utils/loss.py`, `utils/metrics.py`, `utils/torch_utils.py`, `data/hyps/hyp.scratch-low.yaml`, `README.md`.
- **W1-07-S08** — GitHub issues/PR (состояние на 2026-10-23): ultralytics #24871 (NaN EMA → checkpoint не сохраняется, 8.4.70, closed 2026-08-05; ответ Y-T-G: «NaN loss and the checkpoint wasn't saved because it's corrupted»), #24063 (YOLO26m + AdamW + AMP → NaN, 8.4.24, closed 2026-06-21), #24577 (расхождение метрик между 8.4.6 и 8.4.53; OBB, ответ: сравнивать mAP, а не абсолютные loss), #26105 (channels_last на Windows), PR #25038/#25051 (cls remap by name, 2026-07), #26570 (перенос имён/первой conv, 2026-10-07), #26599/#26600 (cls_pw); yolov5 #13513, #13675 (torch ≥ 2.6). Прочитаны заголовки и первые комментарии.
- **W1-07-S09** — Локальные пробы (скрипты и вывод в `W1-07_files\`): `transfer_probe.py` → `out_transfer_probe.txt`; `transfer_probe2.py` → `out_transfer_probe2.txt`; `probe3.py` + `yolo11_noC2PSA_identity.yaml` → `out_probe3.txt`; `ckpt_lifecycle_probe.py` → `out_ckpt_lifecycle_probe.txt`; `env_versions.txt`. Запуск: `YOLO_CONFIG_DIR=<SCRATCH>\cfgdir-W1-07`, venv `SCRATCH\venv-W1-07` (system-site-packages: torch 2.9.1+cpu). Никаких весов/датасетов не скачивалось; источники — модели, собранные из yaml со случайной инициализацией; обучение не запускалось.
- **W1-07-S10** — Файлы соседей (только чтение, для координации): `WAVE1\W1-01_FAMILIES.md` (FLASH: Framework_manual_H1.pdf, список протестированных сетей включает `yolo5s`, YOLO26 выпущен), `WAVE1\W1-12_QUANT_LINQ.md` (путь ONNX → onnx_to_tf → dnn_quant (PTQ, ~100 калибровочных образцов) → compiler; публичное измерение `yolo5s` 106,1 FPS и `yolov8n_pose` 104,8 FPS на LinQ HP по методике MLPerf). Их утверждения я не проверял.
- **W1-07-S11** — Выводы `gh release list` (Ultralytics, YOLOX, yolov5) 2026-10-23 04:44.

## 5. Цепочки и карточки

### 5.1 Ultralytics: цепочка «начальные веса → обучение → best.pt → загрузка для экспорта» (v8.4.184)

1. **Вход**: `YOLO("yolo11n.pt")` → `Model._load` → `load_checkpoint` → `self.model` = EMA fp32 (F06), `self.ckpt` = исходный dict. Альтернативно `YOLO("cfg.yaml").load("x.pt")` (F05).
2. **`Model.train(data=…)`** (`engine/model.py` L807–L896): склейка `args = {**overrides, **custom, **kwargs, "mode":"train"}`; для `resume=True` — проверка, что checkpoint пригоден (F18); создаётся `DetectionTrainer`; если не resume и есть `self.ckpt` — `trainer.model = trainer.get_model(weights=self.model, cfg=self.model.yaml)` (L889–L896).
3. **`get_model`** (`detect/train.py` L183–L199): `DetectionModel(cfg, nc=data["nc"])` → имена цели → `model.load(weights)` (F07). Логи: `Overriding model.yaml nc=80 with nc=K`, `Remapped n/K cls head rows…` (если совпали имена), `Transferred A/B items from pretrained weights`.
4. **`_setup_train`** (F20): `set_model_attributes` → `model.nc/names/args`; `check_imgsz`; freeze (F13) с логами `Freezing layer '…'`; AMP-проверка (F26); даталоадеры; `build_optimizer` (F21; лог `optimizer: … with parameter groups N weight(decay=0.0), M weight(decay=…), K bias(decay=0.0)`); `set_class_weights` (F25); `ModelEMA(decay=0.9999, tau=2000)` (`torch_utils.py` L817–L893: `decay = 0.9999·(1−exp(−updates/2000))`).
5. **Цикл** (F22): forward под `autocast`, `loss.sum()`, backward через `GradScaler`; шаг каждые `accumulate` батчей; `ema.update`; в конце эпохи `ema.update_attr(…)`; валидация **EMA** (`validator(self)`); `fitness` (F23) → `save_metrics` в `results.csv` → `save_model` (F14).
6. **Завершение**: `final_eval` → `strip_optimizer(last)`, `strip_optimizer(best)` (F15) → валидация best.pt.
7. **Загрузка для экспорта**: `YOLO("runs/detect/<name>/weights/best.pt")` → `load_checkpoint` (EMA/`model` → fp32, F06, F16) → дальше W1-10. Классы: `model.names` (`dict[int,str]`).

### 5.2 Что происходит с головой при смене числа классов (сводка)

| Элемент | nc=80→4 (COCO→наш) | Источник |
|---|---|---|
| бэкбон, neck | переносятся полностью | F10 |
| box-ветка `cv2` (+`one2one_cv2`) | переносится (форма не зависит от nc) | F09, F10 |
| скрытые слои cls-ветки `cv3.*.{0,1}` | переносятся (в 8.4.184 — с перестройкой ширины для `n`-моделей) | F07, F10 |
| последний `Conv2d(c3→nc)` cls-ветки | новый; строки по совпавшим именам копируются из источника | F08, F10 |
| bias cls-conv | инициализация `log(5/nc/(640/stride)²)`; для совпавших имён — копия из источника | F07–F09 |
| `names`, `nc` | из `data.yaml` | `detect/train.py` L139–L149 |
| «Transferred N/N» | **100 % при ≥1 совпавшем имени** (обманчиво) | FLASH-2, F10 |

### 5.3 Сравнительная таблица реализаций

| Аспект | Ultralytics 8.4.184 | YOLOX (master) | YOLOv5 v7.0 |
|---|---|---|---|
| Конфиг | `yaml` + `default.yaml`/CLI args | Python `Exp` файл | `--cfg` yaml + `hyp.yaml` + CLI |
| Перенос при nc≠80 | по имени+форме, remap строк по именам | по ключу+форме, предупреждение на каждый несовпавший | по имени+форме (`intersect_dicts`) |
| Что хранит checkpoint | EMA fp16 (+optimizer до strip) | `state_dict` (EMA, если включена) + optimizer + `start_epoch`, `best_ap` | `model` и `ema` fp16 + optimizer + opt |
| Resume | `resume`, узкий белый список аргументов, strict EMA | `--resume`, strict, EMA-веса становятся живыми | `--resume`, `smart_resume` |
| Заморозка | `freeze=N/list/module path` | только через `get_model` | `--freeze N` |
| Fitness / best | mAP50-95 (смена между v8.3.100 и v8.3.200) | AP50-95 → `best_ckpt.pth` | 0.1·mAP50+0.9·mAP50-95 |
| Дисбаланс | `cls_pw` | нет (по коду не найдено) | `cls_pw` (pos_weight), `--image-weights` |
| Оптимизатор | auto: MuSGD/AdamW или явный | SGD nesterov | SGD (по умолчанию), Adam/AdamW |
| Среда | пакет pip, torch≥… | старый код (2022), `torch.cuda.amp` | v7.0 несовместим с torch≥2.6 |

### 5.4 Fine-tune vs from-scratch vs resume (решение)

- **Fine-tune из `.pt`** (рекомендация вендора; F04) — путь по умолчанию. Для родственных к COCO сцен (люди в кадре) бэкбон/neck предобучены; новые классы (каска, жилет, респиратор, сигарета) — с нуля в cls-conv.
- **From scratch (`yaml`)** — только если архитектуру придётся менять радикально (удаление слоёв, смена активаций с потерей качества) и нет подходящих весов; по оценке документации требует «significantly more resources» (S02). Времени на это в бюджете 45 ч, скорее всего, нет (inference; бюджет не измерен).
- **Свои веса → новое обучение**: стартовать из прежнего `best.pt` как `model=` — это **не resume**, а новое обучение с переносом по именам (проба D/E).
- **Resume** — только для продолжения прерванного прогона с неизменёнными `data`/`nc`/`names`.

### 5.5 Малый датасет, дисбаланс, imgsz, rect, multi-scale (что есть в коде)

- Малый датасет: `freeze`, снижение `mosaic/mixup/copy_paste`, явный `optimizer=AdamW lr0=0.001`, `patience` 10–20 (F04, F21); `optimizer=auto` на малом числе итераций уже выбирает AdamW с низким lr (F21).
- Дисбаланс: `cls_pw` (F25); тюнить по val (док. `finetuning-guide.md`); семплирование по изображениям отсутствует (в YOLOv5 есть).
- `imgsz`: любое, кратное `max stride` (округляется `check_imgsz`, L358); все четыре семейства полностью свёрточные → fine-tune на другом `imgsz`, чем у предобучения (640), возможен без перестройки весов (inference; влияние на качество не измерено). Для экспорта фиксированный вход LinQ **не установлен** (→ linq_platform).
- `rect` (train): `rect=True` отключает shuffle при неодинаковых формах батчей (`detect/train.py` L94–L96) и несовместим с multi-GPU; для val `rect=True` включён всегда (`build_yolo_dataset(..., rect=mode=="val")`, L76).
- `multi_scale`: доля `imgsz`, размеры округляются до кратных stride (`preprocess_batch` L120–L136); влияет на `auto_batch` (максимальный размер).

### 5.6 Стоимость обучения (только reported)

| Что | Значение | Условия | Тип |
|---|---|---|---|
| YOLOv5 n/s/m/l/x, COCO, 300 эпох | 1/2/4/6/8 суток | один V100 (мульти-GPU быстрее) | author_statement (README) |
| YOLO26 COCO-этап | 245/70/80/60/40 эпох (n/s/m/l/x) | batch 128, 640, MuSGD, после 150 эпох Objects365 | author_statement (S02) |
| Время на RTX 4070 | **не установлено** | — | unknown (искали: README/docs Ultralytics, YOLOX, YOLOv5, issues) |

Вывод: оценивать только измерением `s/it` в эксп. E1; бюджет задавать через `time=` (F27). Формулу `iterations = ceil(N/max(batch,64))·epochs` (F21) использовать для предсказания выбора оптимизатора.

## 6. Противоречия

1. **Лог «Transferred N/N» vs документация «696 of 708».** Документация (F11) считает «перенесено 696», лог в 8.4.184 для той же модели при совпадении хотя бы одного имени показывает 708/708 (F10). Расходятся определения счётчика; выбор: не использовать лог как проверку головы — сравнивать веса напрямую (E1).
2. **Документация о resume («можно менять только `data`», S03) vs код (белый список из 15 аргументов, F18).** Скорее всего, пересказ WebFetch неполон; решение — читать `check_resume`.
3. **`best.pt` и fitness.** Разные версии (F23) дают разные «лучшие» эпохи при одних данных; при сравнении экспериментов между версиями сравнивать результаты по одной метрике, а не по тому, какой чекпоинт назван best.
4. **Рекомендации по epochs:** «300 как стартовая точка» (S04) vs fine-tune «50–100» (S02, `finetuning-guide.md`, `yolo26-training-recipe.md`). Ни то, ни другое не измерено на нашей задаче; разрешается экспериментом E2/E3 (кривая val vs эпохи на реальных данных).
5. **Документированная эквивалентность `freeze=10` «backbone».** Для yolo11/yolo26 слой 10 (C2PSA) остаётся обучаемым, для yolov8/yolov5u — `freeze=10` заморозит весь бэкбон (F13): одинаковое число — разный смысл.

## 7. Открытые вопросы

| ID | Вопрос | Где искали | Чем закрыть |
|---|---|---|---|
| W1-07-I01 | Какой пакет/версию Ultralytics ставить на хакатоне и совпадает ли поведение официальных `yolo11n.pt/yolov8n.pt/yolov5nu.pt` (обученных старым кодом) с моей пробой на random-init моделях? | код, docs | эксп. E1 с реальным `.pt` (после W1-03) |
| W1-07-I02 | Что именно означает `yolo5s/yolo8/yolo11` на LinQ — определяет, обучать ли anchor-based YOLOv5 (v7.0, `models.yolo`-pickle) или `yolov5u`/YOLOv8/11 | W1-01/W1-12 | → linq_platform, реальный компилятор/ONNX |
| W1-07-I03 | Требуется ли менять архитектуру (SiLU, C2PSA, Resize, Concat, DFL/end2end head) для компилятора LinQ — и тогда насколько обесценится предобучение | W1-12 (оператор-список в мануале отсутствует) | SDK / реальное устройство |
| W1-07-I04 | Время `s/it` и VRAM на RTX 4070 для n/s при 640 и 960/1280 | не найдено в первичных материалах | эксп. E1 |
| W1-07-I05 | Поведение resume при смене `nc` и при смене порядка `names` при том же `nc` | код (strict EMA load, F18) | эксп. E4 |
| W1-07-I06 | Действительно ли `check_amp` без сети пропускается без побочных эффектов; не сломает ли отсутствие `yolo26n.pt` старт | код L1033–L1036 | E1 в офлайне |
| W1-07-I07 | Замораживаются ли BN-статистики замороженных слоёв так, как ожидаем (влияние на качество при малом датасете) | код F13 | абляция `freeze` в E3 |
| W1-07-I08 | Нормально ли совместимы официальные `.pt` для yolo11n с кодом переноса (в частности `legacy`-флаг головы Detect для yolov8-checkpoint) | код `parse_model` L2086, L2203–L2245 | E1 с реальными .pt |
| W1-07-I09 | OS команды (Windows → `workers`, `channels_last`, multi-GPU) | не установлено | вопрос команде |

## 8. Гипотезы

- **W1-07-H01** — *Resume при том же `nc`, но изменённом порядке `names`* пройдёт без ошибки (формы совпадают), но EMA (загружается строго из checkpoint со старым порядком строк cls-conv) и живая модель (перенос по именам) разойдутся; best.pt, сохраняемый из EMA, будет содержать веса в старом порядке под новыми подписями до тех пор, пока EMA не «догонит» (decay→0.9999). Основание: код `setup_model`/`get_model` (remap) против `_load_checkpoint_state` (L1079–L1084). **Не проверялось.** Практическое правило: не resume-ить после правки `data.yaml`; начинать новый прогон из `last.pt` как весов.
- **W1-07-H02** — `optimizer=auto` на нашем размере данных (N ≲ 5–6 тыс. обучающих изображений при 100 эпохах → ≲ 10 000 итераций) выберет AdamW с `lr0 ≈ 0.01/(4+nc)`; для N ≳ 10 тыс. и той же длительности — MuSGD (lr 0.01, голова ×3). Это даёт разное качество/стабильность при близких данных; в рецепте лучше зафиксировать оптимизатор явно. Основание: F21 (арифметика). Не измерено.
- **W1-07-H03** — QAT через ModelOpt в Ultralytics не нужен/вреден для LinQ-пути, пока не будет документировано, что LinQ принимает Q/DQ-ONNX: по W1-12 вход — fp32-граф + калибровка. Основание: S10. Не проверено на реальном компиляторе.
- **W1-07-H04** — Замена `C2PSA` на Identity/удаление и/или SiLU→ReLU снизят mAP до дообучения, но перенос весов формально пройдёт (F12); потребуется дообучение всей сети, а не только головы. Не измерено.
- **W1-07-H05** — Поведение YOLOX/YOLOv5 с torch ≥ 2.6: YOLOX `torch.load` грузит dict тензоров (вероятно, совместимо с `weights_only=True`), YOLOv5 v7.0 — нет (F31). Для YOLOX не проверено.

## 9. Предлагаемые эксперименты (обучение пока не запускалось)

Общее окружение (E0): отдельный venv (на CUDA-сборке torch; версия по W1-09), `pip install ultralytics==8.4.184` (пин), `YOLO_CONFIG_DIR` в отдельный каталог, `yolo checks` (команда из docs/CLI Ultralytics), сохранить `pip freeze`, вывод `nvidia-smi`, SHA256 используемых `.pt` (из W1-03). Записывать полный stdout в файл. Остановка: любое необъяснённое расхождение шагов 1–3 → не переходить к длинному обучению.

**E1. Sanity-train «5–15 минут» (загрузка весов, градиенты, сохранение).**
- Кандидат: Ultralytics 8.4.184 + официальный `yolo11n.pt` (и, если решит W1-01/W1-12, `yolov8n.pt`/`yolov5nu.pt`); веса из W1-03.
- Данные: мини-набор из реальных данных (≥ 32 train, ≥ 8 val; присутствуют все целевые классы; 2–3 кадра без объектов; **выбор вручную/случайно, не `fraction=`**, т. к. `fraction` берёт первые N по имени — F27). `data.yaml` с `names` в порядке, который будет и в боевом датасете.
- Команда (CLI формы из документации Ultralytics): `yolo detect train model=yolo11n.pt data=mini.yaml epochs=3 imgsz=640 batch=8 workers=2 plots=True name=e1_sanity` (+ `device=0`). Параметры `epochs/batch` — условные, подобрать под мини-набор.
- Смотреть в логе (и что означает):
  - `Overriding model.yaml nc=80 with nc=K` — K должно равняться числу классов `data.yaml`;
  - `Remapped n/K cls head rows…` — ожидаемо n=1 для `person`, если он в `names` под таким именем; другие имена (`helmet`, `vest`) в COCO отсутствуют;
  - `Transferred A/B items`: для yolo11n ожидается **499/499** при ≥1 совпадении имён, **493/499** без совпадений (F10); если A заметно меньше (например 448/499) — неправильная ширина/модель/версия; если A/B слишком мало (< ~90 %) — загрузка не удалась (другая архитектура/неподходящий `cfg`);
  - `optimizer: …` — какой оптимизатор и lr выбрал `auto`, число групп параметров;
  - `AMP: checks passed ✅` / `checks skipped` / `checks failed` (F26);
  - `Freezing layer 'model.23.dfl.conv.weight'` — должен появляться всегда (F13);
  - сканирование датасета: `corrupt`, `empty`, `duplicate` — число пустых/повреждённых изображений (W1-08);
  - потери `box_loss/cls_loss/dfl_loss` убывают, нет `nan`; `Instances` > 0 в каждой строке;
  - `train_batch0.jpg`, `labels.jpg`, `labels_correlogram.jpg`: боксы совпадают с объектами, подписи классов верные.
- Сохранить: весь `runs/detect/e1_sanity` (args.yaml, results.csv, weights/*.pt, plots), лог консоли, SHA256 `last.pt/best.pt`.
- Интерпретация: хорошо — пункты выше выполнены. Не доказывает: качество на реальных данных, работу на LinQ, экспорт. Стоп: NaN в первой эпохе при `amp=True` → повторить `amp=False`; различие → проблема AMP/драйвера (F26).

**E2. Overfit малой выборки (градиенты и сопоставление классов).**
- 8–16 изображений (train=val), `mosaic=0 mixup=0 close_mosaic=0 epochs≈50–100 imgsz=640 batch=8 patience=0`, свой оптимизатор явно (`optimizer=AdamW lr0=0.001`, F21).
- Ожидание: `box_loss`, `cls_loss` падают до малых значений, `metrics/mAP50(B)` на тех же изображениях → близко к 1 по всем классам; `predict` на этих кадрах возвращает правильные имена классов.
- Не проходит (mAP по классу ≈ 0 при убывающем loss) → ошибка в метках/порядке `names`/`nc` (→ W1-08), а не в моделях.
- Измерить: время эпохи (`s/it`), VRAM — единственные честные данные для оценки стоимости (F27/5.6).

**E3. Абляция заморозки и длительности на реальной выборке (сколько часов вкладывать).**
- Фиксируем разбиение train/val; прогоны: `freeze=None` vs `freeze=10` (yolo11) vs `freeze=11` на одинаковом `epochs`, `seed=0`, `deterministic=True`; записывать mAP50-95 по эпохам (`results.csv`).
- Цель: найти эпоху плато (кривая); решить число эпох и необходимость заморозки. Не переносить ранние выводы с `n` на `s`.
- Ограничение: один сид — шум; три сида на ключевой развилке (если время позволяет).

**E4. Resume: корректный и некорректный (риск тихой ошибки).**
- (a) Корректный: прогон `epochs=6`, остановка после ~3-й эпохи (Ctrl-C/kill), затем `yolo train resume model=runs/detect/<name>/weights/last.pt` (форма взята из текста ошибки в `check_resume`, L1033–L1035). Смотреть: `Resuming training … from epoch 4 to 6 total epochs`, оптимизатор продолжен, `close_mosaic` срабатывает в нужную эпоху, нет `Resume ignores […]` для неожиданных аргументов.
- (b) Некорректный: resume с `data.yaml`, где `nc` изменён → ожидаем `RuntimeError` size mismatch на загрузке EMA (I05). Либо порядок `names` изменён при том же `nc` → ожидаем прохождение без ошибки и расхождение EMA/живой модели (H01): сравнить прогноз на кадре с известным классом до/после.
- (c) Завершённый прогон: `last.pt` после `strip_optimizer` → resume должен отказаться (F15, `epoch=-1`).
- Что даже успех не подтверждает: корректность на DDP/multi-GPU.

**E5. Проверка checkpoint и загрузки для экспорта.**
- `py -I -m zipfile -l best.pt` (без unpickling) — список файлов; затем загрузка **только своего** `best.pt` через `YOLO("best.pt")` и вывод `model.names`, `model.model.yaml['nc']`, dtype параметров (ожидаем fp32 после `load_checkpoint`), размер файла (стрипнутый ≈ в 2 раза меньше нестрипнутого, F16).
- Сравнить `best.pt` и `last.pt` по `train_metrics`. Передать `best.pt` и SHA256 в W1-10 (экспорт).

**E6. NaN/AMP-стресс (опционально, если E1 показал нестабильность).**
- Повторить E1 с `amp=False`; затем с `optimizer=AdamW lr0` в 3–5 раз ниже; для YOLO26 сверить с issue #24063. Снять `grad` через `clip_grad_norm_` (max_norm=10, F22). Условие остановки: два варианта дали NaN → смена модели/окружения.

**E7 (после появления SDK/устройства).** Прогнать `best.pt` от E5 через путь «ONNX → LinQ» (→ linq_platform, W1-10). До этого заявлять «обучение завершено» можно только как «обучено и загружается».

## 10. Передачи соседям

- → **linq_platform**: (1) какие архитектурные элементы допускает компилятор (SiLU, Resize/Upsample nearest, Concat, C2PSA/attention, DFL (reshape/softmax/conv), end2end-голова `one2one_cv*`)? От ответа зависит, меняем ли YAML (F12) и сколько предобучения теряем; (2) что такое «yolo5s/yolo8/yolo11» на LinQ (anchor-based v7.0 или `*u`; размеры; вход); (3) принимает ли путь `onnx_to_tf` Q/DQ-ONNX (для QAT, H03).
- → **W1-08 / datasets**: порядок и написание `names` теперь влияют на перенос весов (`cls_remap`); `person` совпадает с COCO — единообразить имена в слитых датасетах; `fraction` брать нельзя для сортированных каталогов; проверка по логам `Remapped n/K`.
- → **W1-10 (export)**: источник весов — EMA, округлённый до fp16 (F17); экспорт делать из стрипнутого `best.pt`; лог `Transferred` не гарантирует голову; `model.names` — `dict[int,str]` из data.yaml; чекпоинты, оборванные Ctrl-C, нестрипнуты (`model=None`).
- → **W1-09 (environments)**: локально torch CPU-only; AMP-проверка и `check_requirements` могут ходить в сеть; `YOLO_CONFIG_DIR` позволяет изолировать settings; для QAT нужны ModelOpt + HF Hub.
- → **W1-03/W1-05**: приоритет — веса с классами, чьи **имена** совпадут с нашими (для remap): `person`, возможно `helmet`/`hardhat`/`vest` в доменных весах; зафиксировать точные написания.
- → **training_strategy**: параметры, стоящие экспериментов (E3): `freeze`, `epochs`, `optimizer/lr0`, `cls_pw`, `close_mosaic`, `imgsz`/`multi_scale`; рецепт YOLO26 как образец; QAT — отложить.
- → **evaluation**: `best.pt` выбирается по mAP50-95; для PPE-классов с разной важностью при необходимости выбирать чекпоинт по своей метрике (`save_period=1` + оффлайн-оценка).
- → **video_architecture / hackathon_strategy**: бюджет — `time=<часы>` ограничивает прогон, `epoch{N}.pt` через `save_period`; первый чекпоинт-ориентир 23.10 18:00 — достаточно E1/E2 на малой выборке.

## 11. Запросы эскалации

1. **(сильный исследователь/эксперимент) Реальный прогон E1–E4 на CUDA-машине** с официальными `.pt`: подтвердить F10 для реальных чекпоинтов (I01, I08), измерить s/it и VRAM (I04), проверить resume при смене `names`/`nc` (I05, H01). Найденные материалы: этот файл, скрипты в `W1-07_files\`.
2. **(linq_platform) Совместимость архитектуры с компилятором LinQ** (I03): без неё невозможно решить, обучаем ли штатный YOLO11/YOLOv8/YOLOv5 или требуется «LinQ-friendly» вариант с переобучением.
3. **(W1-04/legal) Лицензии весов и данных** для переноса/дообучения — вне моего участка.
