# W1-14 METRICS — опубликованные результаты, метрики и сопоставимость

- ID ячейки: W1-14 (первая волна)
- Запрошено: Claude Sonnet 5.5, effort high
- Фактическая модель (из системного окружения исследователя): «Sonnet 5.5», model ID `claude-sonnet-5-5`
- Начало: 2026-10-23 ~04:43 MSK; конец: 2026-10-23 ~05:01 MSK (по системным часам машины, пояс «RTZ 2» = UTC+3)
- Язык: русский; литералы (команды, имена файлов, версии, цитаты) — как в источниках.
- Методологическая оговорка: ряд внешних документов (arXiv HTML/PDF, PMC) читался через WebFetch, который возвращает пересказ малой моделью, а не дословный текст. Такие факты помечены «(WebFetch-пересказ)» и считаются author_statement/reported_measurement с пониженной проверенностью до сверки по первичному PDF. Всё, что взято из репозиториев, читалось дословно (`gh api` / локальный клон).

---

## FLASH (находки, важные соседям)

1. **Опубликованные скорости Ultralytics для разных поколений измерены на РАЗНОМ железе и не сравнимы.** YOLOv8 и YOLOv5u: «A100 TensorRT» (0.99 мс у v8n); YOLO11/YOLO26: «T4 TensorRT10» (1.5 мс у 11n, 1.7 мс у 26n); YOLO12: «T4 TensorRT» FP16; YOLO27 (не выпущена): RTX PRO 6000 TensorRT11 FP16, CPU AMD EPYC 9655. Наивное чтение «v8n 0.99 мс быстрее 11n 1.5 мс» — ложное. (W1-14-F03, F04)
2. **В таблице YOLO26 заголовочный mAP и скорость относятся к РАЗНЫМ головам.** Headline mAP 40.9 (YOLO26n) — one-to-many голова + NMS (по умолчанию); скорость опубликована с `nms=False` — NMS-free one-to-one голова, у которой mAP 40.1 («e2e»-колонка). Сравнивать скорость нужно с e2e-колонкой. (F05)
3. **Опубликованный val-mAP Ultralytics считается на прямоугольных (rect) батчах с паддингом `ceil(shape*imgsz/stride+0.5)*stride`** (пример из docs: квадрат 640 → вход 672×672), а `predict()` и квадратные fixed-shape экспорты используют 640×640. Для LinQ (фиксированная форма входа, подразумевается — hypothesis) это значит: цифра из таблицы не равна качеству деплоя; надо мерить `rect=False` (docs/en/modes/val.md). → linq_platform, evaluation. (F09)
4. **Ultralytics Benchmark (37 датасетов, единый протокол) инвертирует COCO-ранжирование:** YOLO26n (COCO 40.9, лучший из n-моделей) на макро-mAP50-95 — последний среди n (44.08 < YOLOv5nu 45.09 < YOLOv8n 45.89 < YOLO11n 46.19). Разброс между поколениями внутри размера ~1–2 п.п.; сами авторы отмечают, что seed 0 не полностью детерминирован. Вывод: разница COCO-mAP в 1–3 п.п. не предсказывает порядок после fine-tune; выбирать по своим данным. В бенчмарк входит SH17 («Safe Human 17»), но пер-датасетные числа в документе не опубликованы. (F12)
5. **LinQ «~2,3 мс для ResNet-50 (batch=1), при оптимизациях – до 1,5 мс» — одна и та же формулировка в даташитах HX (24 TOPS, один LinQ H) и HPS (до 960 TOPS)**, и на сайте lin-q.ru/sol: «текущий: 2,3 мс, возможность оптимизации до 1,5 мс». Нигде не указаны: вариант ResNet-50, вход, точность, область тайминга (устройство или с передачей по PCIe/препроцессингом), метод усреднения. 1,5 мс — «возможность», не измерение. → linq_platform (вопросы в разделе 8). Те же 2,3 мс заявлены для HP (1 чип), HPD (2 чипа), HPS (узел до 960 TOPS) и HX (24 TOPS). (F21–F22)
6. **Из даташита HX (не из CONTEXT):** фреймворки «TensorFlow (версия не ниже 2.9.1), PyTorch (версия не ниже 2.0.0), ONNX (версия не ниже 1.15.0)»; TPU 750 МГц, 24 TOPS, DDR4 до 16 ГБ; на плате HX ещё RK3588 NPU 6 TOPS; «Model Zoo» упоминается в портале разработчика. → linq_platform. (F23)
7. **Протокол «одна и та же модель — две цифры скорости» присутствует в одном README:** PP-YOLOE+_l: 149.2 FPS (V100 TensorRT FP16, без чтения данных и NMS) против 42.02 fps end-to-end (pre+inference+post+NMS, TRT-FP16). Разница 3.55×. Любая «быстрая» опубликованная цифра по умолчанию — «только forward». (F16)
8. **SH17: одно held-out множество (1620 изображений) служит и val, и «test» в публикации;** README ссылается на ultralytics==8.0.38 для обучения YOLOv9/YOLOv10 (эта версия не может содержать эти архитектуры — внутреннее противоречие). Метрики SH17 (YOLOv9-e 70.9 mAP50) нельзя считать независимой оценкой. (F25–F26)

---

## Резюме для оркестратора

Главный вопрос: какие опубликованные цифры сопоставимы. Короткий ответ: **почти никакие кроссемейственные скоростные цифры и очень мало кросс-семейственных цифр качества**. COCO val2017 mAP50-95 для детекторов в основном сопоставим по определению метрики (101-точечная интерполяция, IoU 0.5:0.95 — одинаково в pycocotools и в Ultralytics, F07–F08), но расходится по условиям: NMS IoU (0.65 у ultralytics/yolov5 vs 0.7 у Ultralytics 8.x), head (NMS vs NMS-free), прямоугольный паддинг, дополнительные данные (Objects365 у D-FINE/RT-DETR «+O365» строк), test-dev vs val (YOLOX, PP-YOLOE). Независимое переизмерение (RF-DETR «SAB», pycocotools на всём val2017, T4 TRT FP16 bs=1) даёт для YOLO11 на 2.1–2.9 AP ниже, чем Ultralytics (37.4 vs 39.5 для n); причина не установлена (F14).

Скорость: у каждого проекта своя область («только forward без NMS» у PP-YOLOE, YOLOv5-original (NMS ≈1 мс не входит), PicoDet, YOLOX-README (в коде три числа: forward/NMS/inference); «с препроцессингом и NMS» у TF1 zoo и PP-YOLOE end-to-end; у RT-DETR для YOLO NMS добавлен TRT-плагином). Ни одна из этих цифр не переносится на RTX 4070 и LinQ: они фиксируют конкретную пару (GPU, версия TRT, точность, батч); у LinQ есть единственная опубликованная цифра (ResNet-50 batch=1 2,3 мс) без условий.

Для задач СИЗ/нарушений: опубликованные PPE-метрики — на малых и/или потенциально протекающих сплитах (SH17: 80/20 без val; CHV: 133 тестовых изображения, отобранные из SHWD и GDUT-HWD, т.е. не независимы от них; SHWD: класс `person` = голова без каски, сплит и определение mAP не заданы; Hard Hat Workers (Roboflow/keremberke): метка метрики «precision» для значения «mAP@0.5», `verified: false`). Event-level метрик (нарушение за N кадров, ложные тревоги в час) в найденных публикациях нет — найден только «доступ к ним через треккинг+окно» (MDPI Sensors 2025: mAP@0.5 детектора на SHWD + MOTA/IDF1 на 3 коротких видео, но не P/R по событиям). Это разрыв, который закрывается только собственной разметкой на видео (→ evaluation, datasets).

Главные разрывы: (1) условия измерения LinQ ResNet-50; (2) ни одной опубликованной цифры качества int8 для детектора на LinQ; (3) нет публичной event-level методологии для СИЗ; (4) причина расхождения YOLO11 39.5 vs 37.4 не установлена. Протокол честного сравнения — раздел 6; эксперименты — раздел 9.

---

## 3. Факты

Формат: `W1-14-Fnn` — утверждение; основание; источник `S..` + локатор; область применимости; статус проверки; оговорки.

### 3.1 Официальные таблицы Ultralytics

**F01** — В документации Ultralytics (tag v8.4.184) присутствуют страницы моделей: yolo11, yolo12, yolo26, **yolo27** (превью), yolov10, yolov9, yolov8, yolov5 (YOLOv5u) и др. YOLO26 выпущена: веса `yolo26{n,s,m,l,x}.pt` лежат в релизе `ultralytics/assets` v8.4.0 (2026-01-13), YOLO27 — «Models are undergoing final R&D … not yet available. No launch date is set»; «Model weights, configurations, and implementation code are not being released at this time». Основание: primary_documentation + artifact_metadata. Источник S01 (`docs/en/models/yolo27.md`, строки 1–12; `docs/en/models/yolo26.md`), S03 (assets v8.4.0, список файлов с sha256). Статус: «прочитан текст документации; проверена доступность метаданных файла (скачивание не выполнялось)». Область: Ultralytics-семейство на 2026-10-23. Оговорка: для нашего стека YOLO27 недоступна — её цифры (42.6–60.5 mAP, RTX PRO 6000) исключить из сравнений.

**F02** — Подпись под таблицей детекции (docs/en/tasks/detect.md, v8.4.184): «mAPval values are for single-model single-scale on COCO val2017 dataset. Reproduce with `yolo detect val data=coco.yaml device=0`. Add `nms=False` to reproduce the e2e column»; «Speed averaged over COCO val images with ONNX on CPU and TensorRT10 on an NVIDIA T4 GPU. Reproduce with `yolo detect val data=coco.yaml batch=1 device=0|cpu nms=False`»; «Params and FLOPs values are for fused models after Conv/BatchNorm folding and removal of the unused detection branch. Pretrained checkpoints retain the full training architecture and may show higher counts.» Основание: primary_documentation. S01. Статус: прочитан текст. Область: страница, обслуживающая YOLO26 (macro `docs/macros/yolo-det-perf.md`); таблица YOLO11 (`docs/en/models/yolo11.md`, строки 52–68) содержит только числа без этих подписей на странице модели. Оговорка: что в «Speed» входит preprocess/NMS — документация указывает лишь `nms=False` и `batch=1`; разбивка preprocess/inference/postprocess в таблице не публикуется (она печатается валидатором, см. F10).

**F03** — Железо в таблицах скорости различается между семействами. YOLOv8 (`docs/en/models/yolov8.md` стр. 60–69): «Speed CPU ONNX (ms)» и «Speed A100 TensorRT (ms)», значения с 2 знаками без ±. YOLOv5u (`yolov5.md` стр. 51–63): «A100 TensorRT». YOLO11 (`yolo11.md` стр. 62–68): «T4 TensorRT10», значения «± σ». YOLO12 (`yolo12.md` стр. 76–84): «T4 TensorRT», CPU «-», подпись: «Inference speed measured on an NVIDIA T4 GPU with TensorRT FP16 precision». YOLO26 (macro): «T4 TensorRT10». YOLO27: «NVIDIA RTX PRO 6000 (TensorRT 11, FP16) … AMD EPYC 9655 (ONNX Runtime, FP32)». Основание: primary_documentation. S01. Статус: прочитан. Вывод (inference): строки A100 и T4 одной таблицей сравнивать нельзя.

**F04** — Наглядный пример ловушки (числа из S01, одно и то же `n`-масштаб): YOLOv8n 0.99 мс (A100) / mAP 37.3; YOLOv5nu 1.06 мс (A100) / 34.3; YOLO11n 1.5 ± 0.0 мс (T4 TRT10) / 39.5; YOLO12n 1.64 мс (T4 TRT) / 40.6; YOLO26n 1.7 ± 0.0 мс (T4 TRT10, nms=False) / 40.9 (e2e 40.1). Основание: primary_documentation + inference. Статус: числа прочитаны. Вывод: порядок по колонке скорости отражает смену GPU, а не архитектуру.

**F05** — YOLO26: две колонки mAP («50-95» и «50-95(e2e)») и скорость, опубликованная с `nms=False`. Из `docs/en/guides/end2end-detection.md` (v8.4.184, строки 8–10, 100–104): «Prediction and validation use the one-to-many head with NMS by default … Set `nms=False` to use the faster, NMS-free one-to-one head»; «The published YOLO26 COCO results show that the one-to-many head improves detection mAP by 0.6–0.8 points … 40.9 versus 40.1 for YOLO26n, and 57.5 versus 56.9 for YOLO26x»; «Published NMS-free speed measurements use `nms=False`. Compare accuracy and latency using the same head selection, image size, precision and hardware.» Основание: primary_documentation (+inference: заголовочный mAP и скорость относятся к разным головам). S01. Статус: прочитан. Оговорка: экспорт YOLO26 в ONNX по умолчанию (`nms=None`) — сырые one-to-many выходы `(N, nc+4, 8400)`; `nms=False` — `(N, 300, 6)` (end2end-detection.md стр. 70–80) — какой из них приемлем для LinQ, не установлено (→ linq_platform).

**F06** — Выборка опубликованных чисел (COCO val2017, imgsz 640; S01): 

| Модель | mAP50-95 | CPU ONNX (мс) | GPU TensorRT (мс) и GPU | params (M) | FLOPs (B) |
|---|---|---|---|---|---|
| YOLOv5nu | 34.3 | 73.6 | 1.06 (A100) | 2.6 | 7.7 |
| YOLOv5su | 43.0 | 120.7 | 1.27 (A100) | 9.1 | 24.0 |
| YOLOv8n | 37.3 | 80.4 | 0.99 (A100) | 3.2 | 8.7 |
| YOLOv8s | 44.9 | 128.4 | 1.20 (A100) | 11.2 | 28.6 |
| YOLOv8m | 50.2 | 234.7 | 1.83 (A100) | 25.9 | 78.9 |
| YOLO11n | 39.5 | 56.1 ± 0.8 | 1.5 ± 0.0 (T4 TRT10) | 2.6 | 6.5 |
| YOLO11s | 47.0 | 90.0 ± 1.2 | 2.5 ± 0.0 (T4 TRT10) | 9.4 | 21.6 |
| YOLO11m | 51.5 | 183.2 ± 2.0 | 4.7 ± 0.1 (T4 TRT10) | 20.1 | 68.1 |
| YOLO12n | 40.6 | - | 1.64 (T4 TRT FP16) | 2.6 | 7.5 |
| YOLO12s | 48.0 | - | 2.61 (T4) | 9.3 | 23.3 |
| YOLO26n | 40.9 (e2e 40.1) | 38.9 ± 0.7 | 1.7 ± 0.0 (T4 TRT10, nms=False) | 2.4 | 5.5 |
| YOLO26s | 48.6 (47.8) | 87.2 ± 0.9 | 2.5 ± 0.0 | 9.5 | 20.9 |
| YOLO26m | 53.1 (52.5) | 220.0 ± 1.4 | 4.7 ± 0.1 | 20.4 | 68.4 |
| ultralytics/yolov5 (anchor-based, v7.0) YOLOv5n | 28.0 | 45 (CPU b1) | 6.3 (V100 b1) / 0.6 (V100 b32) | 1.9 | 4.5 |
| ultralytics/yolov5 YOLOv5s | 37.4 | 98 | 6.4 / 0.9 | 7.2 | 16.5 |

Основание: primary_documentation / author_statement. S01, S14. Статус: числа прочитаны из файлов с указанием commit. Оговорки: (а) LinQ-список содержит «yolo5s» — это может быть anchor-based YOLOv5s (37.4) или YOLOv5su (43.0): 5.6 п.п. разницы при одном и том же названии (hypothesis о неоднозначности; что на деле — unknown, → linq_platform); (б) YOLOv5n/s скорость в оригинальном README — V100, NMS ≈1 мс/изобр. не включена (F17); (в) столбцы FLOPs: Ultralytics считает `thop` MACs × 2 (`ultralytics/utils/torch_utils.py::get_flops`, строка `return thop.profile(...)[0] / 1e9 * 2` в v8.4.184, строка 667), torchvision `_ops` у resnet18 = 1.814 (≈ GMACs), т.е. FLOPs разных репозиториев могут быть в разных единицах — не сравнивать без проверки.

**F07** — Код вычисления AP в Ultralytics (`ultralytics/utils/metrics.py`, v8.4.184, f7dd275e): `_AP_X = np.linspace(0, 1, 101)` (стр. 767); `compute_ap` (стр. 771–792) строит огибающую точности и интегрирует `np.interp(_AP_X, mrec, mpre)` по 101 точке («101-point interpolation (COCO)»); `ap_per_class` (стр. 795–892) считает AP по 10 порогам IoU 0.5:0.95 для каждого класса, у которого есть метки в val (`unique_classes` из `target_cls`); классы без предсказаний получают AP=0; **P, R, F1 в итоговой строке — значения при conf, максимизирующем сглаженный средний F1** (`i = smooth(f1_curve.mean(0), 0.1).argmax()`, стр. 886), а не при conf=0.25. mAP = среднее по классам (макро): `Metric.map = all_ap.mean()` (стр. 987–995). Основание: source_code. S02. Статус: прочитан код (не запускался). Область: v8.4.184.

**F08** — Параметры валидатора (S02): `iouv = torch.linspace(0.5, 0.95, 10)` (`models/yolo/detect/val.py`, стр. 59); NMS при валидации: `non_max_suppression(preds, self.args.conf, self.args.iou, nc=0 if detect, multi_label=True, agnostic=single_cls or agnostic_nms, max_det=self.args.max_det, end2end=...)` (стр. 159–181) — **multi_label=True** (один бокс может дать несколько классовых предсказаний; в `utils/nms.py` стр. 92: `multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)`, т.е. действует только при числе классов > 1); в `predict.py` (стр. 55–66) вызов без multi_label (по умолчанию False в сигнатуре `nms.py` стр. 19). Дефолты (`ultralytics/cfg/default.yaml`): `conf:` пусто («defaults: predict=0.25, val=0.001 (0.01 for obb)», стр. 55), `iou: 0.7` (стр. 56), `max_det: 300` (стр. 57), `save_json: False` (стр. 54). Сопоставление детекций с GT: жадное по убыванию conf, по каждому порогу IoU отдельно, без iscrowd (`engine/validator.py::match_predictions` стр. 321–358; вариант Hungarian только при `use_scipy=True`). Дополнительно: в `nms.py` стр. 91, 165–167 задан лимит времени `time_limit = 2.0 + max_time_img * bs` (max_time_img=0.05 с), при превышении печатается «NMS time limit … exceeded» и цикл по изображениям батча прерывается (`break`) — оставшиеся изображения батча получают пустой вывод; при conf=0.001 на медленном CPU или слабой модели это может молча занижать метрики (inference из кода; на практике не воспроизводилось). Основание: source_code. Статус: прочитан. Следствие (inference): внутренний mAP ≈ COCO-подобный, но не идентичен pycocotools — различия: нет iscrowd/ignore-областей, maxDets 300 на изображение против 100 на (изображение, категория) в pycocotools (`cocoeval.py`: `maxDets=[1,10,100]`, S15), multi_label NMS, средний по классам только присутствующим в val. Числовая величина расхождения здесь не измерялась (unknown; эксперимент E2).

**F09** — Геометрия валидации. `docs/en/modes/val.md` (v8.4.184, стр. 93–100): для detect/segment/pose/OBB `rect=True` округляет размеры батча: `ceil(shape * imgsz / stride + 0.5) * stride`, остаток паддинга делится на две стороны; пример — квадрат 640×640 при `imgsz=640`, stride 32 → вход 672×672 (по 16 px с каждой стороны), «while `predict()` uses 640×640 without padding. This difference can affect validation metrics. For square, stride-aligned inputs, `model.val(rect=False)` matches the geometry of `predict()` and square fixed-shape exports. During training, these YOLO tasks use rectangular validation batches regardless of the training `rect` setting, so `model.train(rect=False)` still selects `best.pt` using rectangular validation.» `build.py` стр. 267: `pad = 0.0 if mode == "train" else 0.5`. Основание: primary_documentation + source_code. S01, S02. Статус: прочитан. Следствие (inference): (а) цифра таблицы и цифра fixed-shape деплоя (в том числе на LinQ, если граф фиксирован — hypothesis) измерены в разной геометрии; (б) `best.pt` при обучении выбирается по rect-валидации.

**F10** — Тайминг валидатора (S02): `Profile` — 4 таймера: preprocess, inference, loss, postprocess (`engine/validator.py` стр. 246–275); значения «per image» = накопленное время / число изображений датасета × 1e3 (стр. 288); `Profile` синхронизирует ускоритель (cuda/npu/xpu, `utils/ops.py` стр. 54–55); перед циклом — `model.warmup(imgsz=(1 if pt else batch, C, *imgsz))` (стр. 241–243). В валидаторе `preprocess` = перенос на устройство + `.float()/255` (или `.half()` при `quantize==16`; `val.py` стр. 97–110), т.е. **декодирование JPEG и letterbox выполняются в dataloader и в тайминг не входят**; в `predictor.py` (стр. 183–206) `preprocess` включает `pre_transform` (letterbox), перенос на устройство, BGR→RGB, нормировку — и именно эти три таймера (preprocess/inference/postprocess) печатаются в predict. Основание: source_code. Статус: прочитан. Следствие: «preprocess» в логах val и predict — разные величины.

**F11** — Для детекции на нестандартных данных `save_json=True` запускает `faster-coco-eval` (`val.py::coco_evaluate`, стр. 566–629, ≥1.6.7), а не pycocotools; для COCO/LVIS и «custom json» (любой detect-датасет при `save_json`) GT-словарь строится из YOLO-меток (`init_metrics` стр. 148 `build_gdict`; `update_metrics` стр. 234; bbox в оригинальных пикселях, `area = w*h`, `iscrowd=0`); в stats добавляются `metrics/mAP_small|medium|large(B)` (стр. 619). Документ `modes/val.md` стр. 311: «On detection datasets, `save_json=True` also reports small-, medium-, and large-object mAP through `faster-coco-eval`.» Основание: source_code + primary_documentation. Статус: прочитан. Оговорка: в официальном COCO GT `area` — площадь сегментации (`coco.py` стр. 338–357: для результатов `area = bb[2]*bb[3]`, для GT берётся `ann['area']`), у bbox-only датасета area = w·h → границы small/medium/large (32²/96², `cocoeval.py` стр. 509) для COCO и для наших данных не эквивалентны. Размерные бины считаются в пикселях оригинала, поэтому зависят от разрешения камеры.

**F12** — «Ultralytics Benchmark» (`docs/en/datasets/detect/ultralytics-benchmark.md`, v8.4.184): 37 датасетов, единый протокол — до 1000 изображений train, полный val, `fraction=[1000, 1.0, 0.0]`, дообучение одного и того же предобученного checkpoint 100 эпох, patience 100, seed 0, batch 16, imgsz 640; «Seed 0 is not fully deterministic, so YOLO27m and YOLO27l report the mean of 3 such runs» (остальные — один прогон); размерные mAP считаются масштабированием площади на `(640 / max(w, h)) ** 2` перед бинами COCO; «Candidate datasets were checked for exact and near-duplicate images across the training and validation splits. Flagged pairs were reviewed, and confirmed split leaks were removed or the affected dataset was replaced.» Макро-mAP50-95 (%) — N: YOLO27n 49.25, YOLO11n 46.19, YOLOv8n 45.89, YOLOv5nu 45.09, YOLO26n 44.08; S: YOLO11s 47.78, YOLO26s 47.47, YOLOv8s 47.35, YOLOv5su 47.30; M: YOLO26m 49.42, YOLOv5mu 48.19, YOLO11m 48.15, YOLOv8m 47.99; L/X: YOLO26x 49.85, YOLO26l 49.72, YOLO11l 48.53, YOLOv5lu 48.03, YOLOv8l 48.02, YOLOv8x 47.67, YOLOv5xu 47.35, YOLO11x 47.24 (YOLO27 — не выпущена). Основание: reported_measurement (автор — разработчик семейства, интерес: продвигает YOLO26/27) + primary_documentation. S01. Статус: прочитан. Следствие (inference): на COCO порядок n: 26 > 12 > 11 > v8 > v5u; на 37 доменных датасетах: 11 > v8 > v5u > 26. Пер-датасетные числа (в том числе SH17 = «Safe Human 17») в документе не приведены — unknown, нужны через Ultralytics Platform (не проверялось).

**F13** — INT8-качество в Ultralytics docs (TensorRT, A100, `ultralytics==8.2.4`, `tensorrt==8.6.1.post1`, YOLOv8n): COCO val mAP50 / mAP50-95: FP32 0.52 / 0.37; FP16 0.52 / 0.37; INT8 0.47 / 0.33; в таблице «Predict» использовалась batch 8, «COCO val» — batch 1 (`docs/en/integrations/tensorrt.md` стр. 280–301). Тексты: «INT8 can still shift confidence values, so select the operating threshold from the INT8 model's own F1 curve»; «calibration for INT8 is specific to each device»; NVIDIA рекомендует ≥500 репрезентативных калибровочных изображений (стр. 209–217, 272). Основание: reported_measurement + primary_documentation. S01. Статус: прочитан. Оговорка: это TensorRT PTQ, **не** путь компилятора LinQ (DNN Quant); числа округлены до 2 знаков; по классам и размерам не разложены.

### 3.2 Другие семейства: условия опубликованных цифр

**F14** — Независимое переизмерение (README roboflow/rf-detr @5b22dfc0, «SAB», roboflow/single_artifact_benchmarking): «All COCO accuracy numbers are measured in-house for every model shown, computed with pycocotools in SAB over the full 5,000-image `val2017` split … All latency numbers were measured on an NVIDIA T4 using TensorRT, FP16, and batch size 1. Parameter counts are deployment (fused) `nn.Module` parameter counts». COCO AP50:95 / latency (мс): YOLO11-N 37.4 / 2.5; YOLO11-S 44.4 / 3.2; YOLO11-M 48.6 / 5.1; YOLO26-N 40.3 / 1.7; YOLO26-S 47.7 / 2.6; YOLO26-M 52.5 / 4.4; D-FINE-N 42.7 / 2.1; D-FINE-S 50.6 / 3.5; RF-DETR-N 48.4 / 2.3 (384×384); RF-DETR-S 53.0 / 3.5 (512×512). Сравнение с Ultralytics (F06): YOLO11 n/s/m на 2.1/2.6/2.9 AP ниже, YOLO26 n/s/m на 0.6/0.9/0.6 ниже; YOLO11-N на T4 2.5 мс против 1.5 мс. Таблица RF100-VL AP50:95 для YOLO26-N 52.0, YOLO11-N 55.3, RF-DETR-N 57.7, D-FINE-N 58.2 (другое распределение данных). Основание: reported_measurement (автор — разработчик конкурирующего RF-DETR; конфликт интересов). S11. Статус: прочитан. Причина расхождения с Ultralytics — **не установлена** (hypothesis: экспорт/NMS-порог/ограничения TRT-плагина; в README не раскрыто). AP строк D-FINE-S/M/L/X в этой таблице (50.6/55.0/57.2/59.3) практически совпадает с чекпоинтами «Objects365+COCO» из README D-FINE (50.7/55.1/57.3/59.3), а не с COCO-only (48.5/52.3/54.0/55.8) (F15) — т.е. строки D-FINE, вероятно, используют предобучение на Objects365 (inference по совпадению чисел; README SAB это не раскрывает), что ставит в неравные условия по данным с YOLO/RF-DETR-COCO-строками.

**F15** — D-FINE (@956d1709, README): «Latency is evaluated on a single T4 GPU with batch_size = 1, fp16, and TensorRT==10.4.0» (стр. 135). COCO-only AP^val / latency: N 42.8 / 2.12 мс; S 48.5 / 3.49; M 52.3 / 5.62; L 54.0 / 8.07; X 55.8 / 12.89. Obj365+COCO: S 50.7; M 55.1; L 57.3; X 59.3 при тех же latency. Основание: author_statement. S10. Статус: прочитан. Оговорка: строки с предобучением на Objects365 используют дополнительные данные; README рекомендует их для fine-tuning, но предупреждает: «If your categories are very simple, it might lead to overfitting and suboptimal performance» (стр. 117).

**F16** — PP-YOLOE (PaddleDetection @b25522a0, `configs/ppyoloe/README.md`): «PP-YOLOE inference speed is tested on single Tesla V100 with batch size as 1, CUDA 10.2, CUDNN 7.6.5, TensorRT 6.0.1.8»; «the speed in Model Zoo do not contains the time cost of data reading and post-processing (NMS)»; «End-to-end speed test includes pre-processing + inference + post-processing and NMS time … Xeon Gold 5117 … V100, CUDA 11.2, CUDNN 8.2.0, TensorRT 8.0.1.6». PP-YOLOE+_l: 149.2 FPS (TRT FP16, forward) против end-to-end TRT-FP16 42.02 fps; PP-YOLOE+_s 333.3 FPS vs 47.85; AP: val и test-dev приведены отдельными колонками (PP-YOLOE+_s: 43.7 / 43.9). Основание: author_statement. S13. Статус: прочитан. PicoDet (@b25522a0, `configs/picodet/README_en.md`): латентность — Intel i7-10750H MKLDNN 12 потоков и Snapdragon 865 (FP16, Paddle-Lite); «When testing the speed benchmark, the post-processing is not included in the exported model»; есть QAT-модель: PicoDet-S 416 fp32 32.5 → INT8 31.5 (mAP val 0.5:0.95; Paddle-Lite INT8).

**F17** — ultralytics/yolov5 (@af08ba15, релиз v7.0, 2022-11-22, anchor-based): «mAPval … Reproduce using: `python val.py --data coco.yaml --img 640 --conf 0.001 --iou 0.65`» (NMS IoU 0.65, а в Ultralytics 8.x — 0.7); «Speed … averaged over COCO val images using an AWS p3.2xlarge V100 instance. Non-Maximum Suppression (NMS) time (~1 ms/image) is not included.»; GPU Speed в разделе P6: batch 32. Основание: author_statement. S14. Статус: прочитан.

**F18** — YOLOX (@6ddff482, README + код `yolox/evaluators/coco_evaluator.py`): таблица содержит колонки mAP val и mAP test (test-dev) и «Speed V100 (ms)» без подписи под таблицей; воспроизведение скорости: `python -m yolox.tools.eval -n yolox-s -c yolox_s.pth -b 1 -d 1 --conf 0.001 --fp16 --fuse`. В коде оценщика время считается раздельно: `inference_time` (forward), `nms_time`, и выводится «forward / NMS / inference» (сумма) (стр. 144–182, 263–280). Из статьи arXiv 2107.08430 (WebFetch-пересказ ar5iv): «FPS and latency in this report are all measured with FP16-precision and batch=1 on a single Tesla V100»; «The latency and FPS in this table are measured without post-processing» (подпись к Table 2); в других таблицах не указано. Light-модели (Nano 25.8, Tiny 32.8 mAP) — вход 416, скорость не опубликована. Основание: author_statement + source_code. S06. Статус: код — прочитан; статья — пересказ. Оговорка: какое из трёх чисел кода соответствует колонке README — не указано (unknown).

**F19** — RT-DETR (@df2a96c8, README + статья 2304.08069 через WebFetch-пересказ): README: «T4 TensorRT FP16(FPS)»; R18 46.5 AP / 217 FPS, R50 53.1 / 108, HGNetv2-L 53.0 / 114, R101 54.3 / 74; строки «COCO + Objects365» — другие данные. Статья: бенчмарк на COCO val2017; «append the NMS post-processing plugin of TensorRT for YOLO detectors»; время для YOLO измерено «according to the NMS thresholds of the corresponding accuracy» и без I/O и memcpy; явного batch в тексте не указано (в таблицах «FPS_bs=1» — со слов пересказа). Основание: author_statement. S09. Статус: README прочитан; статья — пересказ. Следствие: у RT-DETR FPS для YOLO включают NMS-плагин TRT, у Ultralytics — нет (F02, nms=False) — значения FPS из RT-DETR и из Ultralytics не взаимозаменяемы.

**F20 (прочие)** — torchvision (@c725e823; v0.29.1): `SSDLite320_MobileNet_V3_Large_Weights.COCO_V1`: `box_map` 21.3 («COCO-val2017»), `num_params` 3 440 060, `_ops` 0.583, `_file_size` 13.418; `SSD300_VGG16_Weights.COCO_V1`: `box_map` 25.1, 35 641 826 params, `_ops` 34.858. Это **не** `ssd_mobilenet_v1/v2` из списка LinQ (те — TF OD API). TF1 Detection Zoo (@a088bcc4): ssd_mobilenet_v1_coco — 30 мс, mAP 21; ssd_mobilenet_v2_coco — 31 мс, 22; ssdlite_mobilenet_v2_coco — 27 мс, 22; «running time in ms per 600x600 image (including all pre and post-processing) … Nvidia GeForce GTX TITAN X»; «detector performance on subset of the COCO validation set … mAP rounded to the nearest integer»; для мобильных/EdgeTPU моделей: MobileDet-EdgeTPU fp32/uint8 mAP 25.9/25.6 (Pixel 4 Edge TPU 6.9 мс), MobileDet-DSP 28.9/28.8 (12.3 мс). Основание: artifact_metadata (torchvision), author_statement (TF zoo). S07, S08. Статус: прочитан. Следствие: у «ssd_mobilenet_v1/v2» на LinQ опубликованное качество — «mAP ≈21–22 на подмножестве val, округление до целого»; сравнимо только с самим собой.

**F20b** — YOLOv6 (@e86a483f): колонки «Speed T4 trt fp16 b1/b32 (fps)», TRT 7.2; мобильные — MNN 2.3.0, 2 потока, 10 прогревов, 100 циклов. Таблица квантования: YOLOv6-N RepOpt INT8 34.8 mAP vs «YOLOv6-N FP16» 35.9 — но заголовочная модель YOLOv6-N (v3.0) имеет 37.5 (т.е. baseline квантованной таблицы — другая модель, 300 эпох). YOLOv10 README (@453c6e38): колонка «Latency» без указания железа в README. YOLOv9 (@5b1ea9a8): AP val/AP50/AP75 без скорости, воспроизведение — `val.py --conf 0.001 --iou 0.7 --save-json`. NanoDet (@be9b4a90): CPU i7-8700 и ARM Kirin 980 (ncnn), без GPU. Основание: author_statement. S12, S13. Статус: прочитан (кратко).

### 3.3 LinQ: условия единственной опубликованной цифры

**F21** — `lin-q.ru/sol` (снято 2026-10-23, копия страницы в SCRATCH): «Сверхнизкая задержка при малом батче (текущий: 2,3 мс, возможность оптимизации до 1,5 мс для ResNet-50)» для модулей HP/HPD/HPQ/HPS; «Высокая эффективность на малом батче на CNN/Transformer моделях». Даташит HPS (`files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf`, 4 стр.): «Низкая задержка: ~2,3 мс для ResNet-50 (batch=1), при оптимизациях – до 1,5 мс»; в таблице: «Задержка инференса (ResNet-50) ~2,3 мс (batch=1), до 1,5 мс (при оптимизации)»; «Поддержка форматов данных int8 (основной), в перспективе fp16/bfloat16»; «Тактовая частота вычислительных блоков До 1 ГГц (динамически управляемая)»; «Возможность одновременного запуска до 40 моделей нейронных сетей». Страница описывает HP (1× LinQ H, 750 МГц, «до 8 Гбайт/с (8 линий)») и HPD (2× LinQ H, «до 8 Гбайт/с (16 линий)») — одна и та же фраза о 2,3 мс повторяется для HP/HPD/HPQ/HPS (1, 2, 4 чипа и узел), т.е. цифра не зависит от числа чипов (inference). Основание: primary_documentation (маркетинговый уровень). S16. Статус: PDF прочитан (текст извлечён, `W1-14_files\linq_hps_datasheet_extract.txt`). Не указано: вариант ResNet-50 (в списке сайта есть `resnet50_mlperf`, `resnet50_v2`, `torch_resnet50`), размер входа, точность исполнения слоёв, включена ли передача данных и пред/постобработка, один чип или узел, метод усреднения, дата/версия компилятора.

**F22** — Даташит HX (`linq_hx_datasheet.pdf`, 4 стр., извлечён текст): та же фраза «~2,3 мс для ResNet-50 (batch=1), при оптимизациях – до 1,5 мс», но при «До 24 TOPS (int8) и 6 TOPS (NPU RK3588) на одном модуле», TPU «Частота 750 МГц», DDR4 до 16 ГБ. Следствие (inference): число 2,3 мс не масштабируется с TOPS (24 TOPS в HX и «до 960 TOPS» в HPS дают одно значение) — это, по-видимому, латентность одного ядра/чипа LinQ H при batch=1 (hypothesis; тот факт, что «batch=1» не использует всё устройство HPS, прямо не заявлен). Статус: прочитан.

**F23** — HX: «Поддержка фреймворков и специализированных библиотек: TensorFlow (версия не ниже 2.9.1), PyTorch (версия не ниже 2.0.0), ONNX (версия не ниже 1.15.0)»; «Архитектура поддерживает целочисленные данные с разрядностью 8 бит (int8) и векторные вычислители»; «портал разработчика и база знаний (доступ к Model Zoo, образцам кода)»; «ПОДДЕРЖИВАЕМЫЕ СЕТИ»: свёрточные для классификации, для детекции, GAN, «сверточные нейронные сети трансформеры для … семантической сегментации», для определения положения тел по ключевым точкам. Основание: primary_documentation (HX). Статус: прочитан. Не установлено, распространяются ли версии на HP/HPS (→ linq_platform).

**F24** — Опубликованных цифр качества или скорости детектора (yolo5s/yolo8/yolo11/ssd) на LinQ найдено **0**: проверены lin-q.ru/sol, lin-q.ru/tech (по CONTEXT), HPS/HX-даташиты, `2025_HiTech_site_LinQ_A.pdf` (2 стр., реестровые сведения, ПО и языки Python, C/C++; фреймворки PyTorch, ONNX, TensorFlow). Основание: unknown. Охват: 4 локальных PDF/HTML, без SDK/Model Zoo (доступа нет).

### 3.4 Опубликованные PPE-метрики

**F25** — SH17 (arXiv 2407.04590; J. Safety Sci. Resilience, doi 10.1016/j.jnlssr.2024.09.002; WebFetch-пересказ HTML + README репо @2f832c28): 8099 изображений (Pexels), 17 классов, 75 994 инстанса (сумма классов Table II = 76 318 — расхождение в самой статье); сплит «80% train / 20% test» (1620 test, 15 358 инстансов), валидационного сплита в статье нет; `sh17.yaml` в репозитории задаёт `train` и `val` (оба — файлы списков), `test:` пусто, README: «reproduce … on the SH17 validation set … `model.val(data="sh17.yaml", batch=1, imgsz=640)`»; обучение: imgsz 640, 200 эпох, batch 128→32; метрики: YOLOv9-e P 81.0 / R 65.0 / mAP50 70.9 / mAP50-95 48.7; YOLOv8-n 58.0 / 36.6; YOLOv10-x 67.8 / 46.7; по классам (YOLOv9-e mAP50/mAP50-95): person 92.1/77.9, head 93.5/74.3, helmet 77.0/57.6, face-mask 75.5/49.2, safety-vest 57.7/38.1, foot 29.3/14.0; кросс-доменный тест на Pictor-PPE (YOLOv9-e): all 58.9 / 37.6, helmet 55.5 / 30.0, safety-vest 35.5 / 21.2 (текст говорит 58.8). Лицензия датасета: CC BY-NC-SA 4.0 (README). Размеры объектов: 39 764 аннотаций < 1% площади изображения, 59 025 < 5%; оригинальные размеры до 8192×5462 при обучении 640. Основание: author_statement. S17. Статус: прочитан. 

**F26** — SH17: признаки риска (inference, из первичного описания): (а) единственный held-out набор служит и «val» (в yaml/README), и «test» (в статье) → при обучении Ultralytics `best.pt` выбирается по fitness на val (docs/val.md, F09), значит выбранная контрольная точка настроена на те же 1620 изображений, по которым отчитаны метрики (оптимистичное смещение, величина не измерена); (б) «After removing duplicate samples» — упомянуто, но про near-duplicates и про разделение по фотографу/сцене ничего не сказано; (в) README утверждает, что все модели v8/v9/v10 обучались на `ultralytics==8.0.38` — эта версия вышла задолго до YOLOv9/YOLOv10 (противоречие, причина неизвестна); (г) стоковые фото Pexels ≠ CCTV: 8192×5462 vs 640 для обучения.

**F27** — SHWD (репозиторий njvisionpower/Safety-Helmet-Wearing-Dataset @c952631d, последний коммит 2019-12-17): 7581 изображений, 9044 «hat» (positive) и 111 514 «person» (negative = голова без каски); «Some of negative objects got from SCUT-HEAD»; бенчмарк «map: darknet 88.5, mobile1.0 86.3, mobile0.25 75.0» без определения mAP (IoU-порог, интерполяция, сплит); формат Pascal VOC, `ImageSets/Main/{trainval,test}`; фреймворк MXNet/GluonCV. Основание: author_statement. S18. Статус: прочитан README; сплит-файлы и данные не скачивались (Baidu/GDrive). Следствие (inference): класс `person` в SHWD означает «голова без каски», а не человека; такая метка не сравнима с `person` в COCO/SH17. 

**F28** — CHV (Wang et al., Sensors 2021, doi 10.3390/s21103478; PMC8156681; WebFetch-пересказ): 1330 изображений, 9209 инстансов, отобраны «from about 10,000 images collected from GDUT-HWD and SHWD»; сплит 1064/133/133 «selected randomly»; про near-duplicates и источник кадров не сказано; классы: person, vest, blue, red, white, yellow (цвета касок); TP при IoU > 0.5; «AP is the area under the Precision×Recall curve»; YOLOv5x mAP 86.55; GPU-скорость — Tesla P40, среднее по 133 тестовым изображениям, «Image read/write time is excluded», batch/precision/NMS не указаны; YOLOv5s 52 FPS. Основание: author_statement. S19. Следствие: (а) тест из 133 изображений даёт широкий доверительный интервал; (б) так как CHV собран из SHWD и GDUT-HWD, оценка на CHV модели, обученной на SHWD/GDUT-HWD, не независима (inference). 

**F29** — Pictor-PPE (ciber-lab/pictor-ppe @8f41c952; Nath, Behzadan, Paal, Automation in Construction 112 (2020) 103085): Pictor-v3 — 774 crowd-sourced + 698 web-mined изображений, 2496 + 2230 рабочих; три подхода (A1: YOLO-v3 детектирует worker/hat/vest → классификатор W/WH/WV/WHV; A2: YOLO-v3 сразу классифицирует рабочего; A3: YOLO-v3 + CNN на вырезке). README: «The best is Approach-2 (72.3% mAP)» (график с числами — изображение, не прочитан). Это пример **метрики уровня рабочего (комплаенс), а не уровня предмета** (author_statement, S20). Другие источники называют 784 изображения (WebSearch, AAAI-препринт) — расхождение со счётом README (774+698); не разрешено.

**F30** — Hard Hat (Roboflow Universe «Hard Hats» v2; HF `keremberke/hard-hat-detection` sha 694c6135…, 2023-01-16): train 13 782 / valid 3 962 / test 2 001; «Resize to 640x640 (Stretch)»; «No image augmentation techniques were applied» (README.roboflow.txt). Модель HF `keremberke/yolov8m-hard-hat-detection` (sha 65c3a88d…, 2023-02-22; библиотека `ultralytics==8.0.23`): метрика в `model-index` — `type: precision`, `name: mAP@0.5(box)`, `value: 0.81115`, `verified: false`, split `validation`; в карточке: «since mAP@0.5 is not available on hf.co/metrics»; классы модели в тексте: `['Hardhat', 'NO-Hardhat']`, у датасета: `['hardhat', 'no-hardhat']` (регистр). Основание: artifact_metadata + author_statement. S21. Следствие (inference): (а) метрика заявлена на `validation`, т.е. на том же сплите, по которому выбирается `best.pt`; (б) «Stretch»-ресайз при обучении означает искажение пропорций, которое не воспроизводится letterbox-препроцессингом по умолчанию (F09) — не сравнивать без единого препроцессинга; (в) near-duplicate между сплитами из видео-кадров не проверялся (unknown: Roboflow-источник не изучен).

**F31** — Event-/track-level в публикациях: (а) MDPI Sensors 25(20), 6487 (2025, doi 10.3390/s25206487, PMC12568081): детектор YOLOv5+SACA обучен на SHWD, mAP@0.5 0.940 (YOLOv8 0.919, YOLOv9 0.924), трекер — MOTA 90.5%, IDF1 84.2%, 5 переключений идентичности; проверка на **трёх** видео (Hikvision, 20 fps, 1920×1080), сценарии описаны текстом; состояние «каска/без каски» определяется скользящим окном по кадрам (трек с числом кадров ниже порога считается ложным); **P/R по событиям и ложные тревоги в час не приводятся**; обучение на RTX 4070 12 ГБ (Table 1). (б) WebSearch (2 запроса, 2026-10-23): репозитории с «30 подряд кадров без каски → нарушение» (дизайн-решение, без метрики, не верифицировано); AI City Challenge 2023 Track 5 (мотоциклисты без шлема, CVPRW 2023) упомянут в поиске, но PDF отдал HTTP 403 — метрики не прочитаны. Основание: author_statement / unknown. S22, S23. Вывод: публичного бенчмарка/метода оценки «человек без каски N кадров → событие, FA/час» не найдено (охват: 3 поисковых запроса + прочтение MDPI-статьи).

### 3.5 Определения метрик COCO

**F32** — pycocotools (`cocoapi` @8c9bcc3c, последний коммит 2020-02-20), `cocoeval.py`: `iouThrs [.5:.05:.95]`, `recThrs [0:.01:1]` (101), `maxDets [1 10 100]`, `areaRng` all/small `[0, 32²]`/medium `[32², 96²]`/large `[96², 1e5²]` (стр. 25–28, 509–510), `iscrowd`-GT получает ignore (стр. 106–109), детекции сверх `maxDets[-1]` отбрасываются по (изображение, категория) (стр. 175–176, 199–200). В `coco.py::loadRes` для bbox `area = bb[2]*bb[3]` (стр. 338). Основание: source_code. S15. Статус: прочитан.

---

## 4. Таблица измерений: что именно измерено (сводная по условиям)

Сводка «число — условия — происхождение». Колонки: ключевая метрика; сплит/протокол качества; imgsz; железо/стек скорости; что входит в время; оговорка.

| Семейство / источник | Качество (метрика, сплит) | imgsz | Скорость: железо / стек / батч / точность | Что входит во время | Главная оговорка |
|---|---|---|---|---|---|
| Ultralytics YOLO11 (S01) | mAP50-95, COCO val2017, single-scale | 640 | CPU ONNX; T4 TRT10 | в docs YOLO11: не расшифровано; общий footnote: `batch=1 ... nms=False` | на v8.3.0/v8.4.0 footnote говорил «Amazon EC2 P4d», таблица — «Tesla T4» (противоречие, F03) |
| Ultralytics YOLOv8 / YOLOv5u (S01) | то же | 640 / (P6: 1280) | CPU ONNX; A100 TRT | не расшифровано | другое GPU, чем у YOLO11/26 |
| Ultralytics YOLO12 (S01) | то же | 640 | T4 TRT FP16; CPU «-» | не расшифровано | CPU-колонка пуста |
| Ultralytics YOLO26 (S01, S05) | mAP50-95: NMS-голова и e2e (NMS-free) | 640 | T4 TRT10, `nms=False` (F02) | forward NMS-free головы; precision/batch в статье не указаны (WebFetch) | headline mAP ≠ голова скорости (F05) |
| YOLO27 (S01) | превью | 640 (800 для l) | RTX PRO 6000 TRT11 FP16; EPYC 9655 ONNX FP32 | — | не выпущена |
| ultralytics/yolov5 (v7.0) (S14) | mAP, `--conf 0.001 --iou 0.65` | 640/1280 | V100 b1/b32; CPU b1 | NMS ~1 мс **не** входит | anchor-based; IoU NMS 0.65 |
| YOLOX (S06) | val и test-dev | 640 / 416 (light) | V100, FP16, b=1 (статья) | Table 2: «without post-processing» (статья, WebFetch) | README без подписи |
| PP-YOLOE+ (S13) | val и test-dev | 640 | V100 TRT FP16 b1 (TRT 6.0.1.8) | без чтения данных и NMS; e2e — с NMS | 149.2 vs 42.02 FPS (l) |
| PicoDet (S13) | val2017 | 320–640 | i7-10750H MKLDNN, Snapdragon 865 | без пост-обработки (benchmark=True) | не GPU |
| RT-DETR (S09) | val2017 (+O365 строки) | 640 | T4 TRT FP16 | для YOLO добавлен TRT-NMS-плагин; I/O и memcpy исключены | b не указан в тексте |
| D-FINE (S10) | val2017 (+O365 строки) | 640 | T4, b=1, fp16, TRT 10.4.0 | не расшифровано | доп. данные |
| RF-DETR / SAB (S11) | pycocotools, полный val2017 | разное | T4, TRT, FP16, b=1 | не расшифровано | автор — конкурент |
| YOLOv6 (S12) | val2017 | 640/1280 | T4 TRT 7.2 FP16 b1/b32 | не расшифровано | quant-таблица с другим baseline |
| TF1 zoo SSD (S08) | подмножество COCO val, целое число | 300 (вход) / 600×600 кадр | GTX TITAN X | «including all pre and post-processing» | округление до целого |
| torchvision SSDLite (S07) | box_map, COCO-val2017 | 320 | — | — | не ssd_mobilenet LinQ |
| LinQ ResNet-50 (S16) | — | не указан | не указан; batch=1 | не указано | см. F21–F22 |

---

## 5. Источники

Времена в колонке «Проверено» приблизительные (сессия 04:43–05:03 MSK по системным часам; точное время каждого запроса не журналировалось).

| ID | Название / владелец | URL | Тип | Версия / revision | Проверено (MSK, 2026-10-23) | Состояние |
|---|---|---|---|---|---|---|
| W1-14-S01 | Ultralytics docs (`docs/en/...`), ultralytics/ultralytics | https://github.com/ultralytics/ultralytics | docs в репозитории | tag **v8.4.184**, commit `f7dd275e5853801674ca78ef51896617bb5362ba` (клон depth 1 в SCRATCH); main на момент проверки `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8` (2026-10-22T20:27Z) | ~04:45–05:01 | доступен; локаторы: `docs/en/models/{yolo11,yolov8,yolov5,yolo12,yolo26,yolo27}.md`, `docs/en/tasks/detect.md`, `docs/macros/yolo-det-perf.md`, `docs/en/modes/val.md`, `docs/en/guides/end2end-detection.md`, `docs/en/integrations/tensorrt.md`, `docs/en/datasets/detect/ultralytics-benchmark.md` |
| W1-14-S02 | Ultralytics код валидации/метрик | то же | исходный код | v8.4.184 / `f7dd275e…` | ~04:50–05:01 | доступен; `ultralytics/utils/metrics.py`, `models/yolo/detect/val.py`, `engine/validator.py`, `utils/nms.py`, `models/yolo/detect/predict.py`, `engine/predictor.py`, `cfg/default.yaml`, `data/build.py`, `utils/ops.py` (класс Profile), `utils/torch_utils.py` (`get_flops`) |
| W1-14-S03 | Релиз ultralytics/assets v8.4.0 (2026-01-13) | https://github.com/ultralytics/assets/releases/tag/v8.4.0 | artifact_metadata | `gh api repos/ultralytics/assets/releases/tags/v8.4.0` | ~04:55 | метаданные доступны (размеры и sha256 digest): напр. `yolo26n.pt` 5 544 453 байт, sha256 `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef`; `yolo11n.pt` 5 613 764, `0ebbc80d…ee1`; `yolov8n.pt` 6 549 796, `f59b3d83…b36`; `yolov5nu.pt` 5 562 759, `9e9c1be4…937`; `yolo12n.pt` 5 595 063. Файлы не скачивались, не десериализовались |
| W1-14-S04 | История docs Ultralytics: tags v8.3.0, v8.3.100, v8.4.0 | `gh api repos/ultralytics/ultralytics/contents/docs/en/...?ref=<tag>` | docs | указанные теги | ~05:00 | доступен |
| W1-14-S05 | Ultralytics YOLO26: Unified Real-Time End-to-End Vision Models, Jocher et al. | https://arxiv.org/abs/2606.03748 (HTML https://arxiv.org/html/2606.03748) | preprint | v1, 2026-06-02 | ~05:01 | прочитано через WebFetch (пересказ) |
| W1-14-S06 | YOLOX, Megvii-BaseDetection; arXiv 2107.08430 | https://github.com/Megvii-BaseDetection/YOLOX ; https://ar5iv.labs.arxiv.org/html/2107.08430 | README+код+статья | commit `6ddff4824372906469a7fae2dc3206c7aa4bbaee` (2025-06-08) | ~04:58–05:01 | README и код прочитаны; статья — WebFetch-пересказ (PDF не разобран) |
| W1-14-S07 | torchvision detection weights | https://github.com/pytorch/vision | исходный код | commit `c725e823011284b77082320577d288f82b36683c`; релиз v0.29.1 (2026-09-30) | ~04:59 | `torchvision/models/detection/ssdlite.py` стр. 187–206, `ssd.py` стр. 28–47; `docs/source/models.rst` стр. 452 «Box MAPs are reported on COCO val2017» |
| W1-14-S08 | TF1 Detection Model Zoo, tensorflow/models | https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf1_detection_zoo.md | docs | commit `a088bcc473f77e8a1b7b38bbfa4ebd4f6313a127` (master, 2026-10-22) | ~05:00 | прочитан |
| W1-14-S09 | RT-DETR, lyuwenyu; arXiv 2304.08069 | https://github.com/lyuwenyu/RT-DETR ; https://ar5iv.labs.arxiv.org/html/2304.08069 | README+статья | commit `df2a96c8c3a098567a1149bf0248da6efe6d495d` (2026-10-09) | ~05:01 | README прочитан; статья — WebFetch-пересказ |
| W1-14-S10 | D-FINE, Peterande | https://github.com/Peterande/D-FINE | README | commit `956d1709314c2c6a4df6f34de232054578a7449f` (2026-08-19) | ~05:01 | прочитан |
| W1-14-S11 | RF-DETR + SAB, roboflow | https://github.com/roboflow/rf-detr ; https://github.com/roboflow/single_artifact_benchmarking | README | commit `5b22dfc0940697ce1abdfa681a5f7392b3eddbfb` (2026-10-16) | ~05:01 | README прочитан; репозиторий SAB не открывался |
| W1-14-S12 | YOLOv10 (THU-MIG), YOLOv9 (WongKinYiu), YOLOv6 (meituan), NanoDet (RangiLyu) READMEs | github.com/{THU-MIG/yolov10, WongKinYiu/yolov9, meituan/YOLOv6, RangiLyu/nanodet} | README | `453c6e38…`, `5b1ea9a8…`, `e86a483f…`, `be9b4a90…` | ~05:01 | прочитаны по тексту; YOLOv7/EfficientDet не разбирались |
| W1-14-S13 | PaddleDetection (PP-YOLOE, PicoDet) | https://github.com/PaddlePaddle/PaddleDetection | README | commit `b25522a0f4bde8c80603f3ba5e3472059972e3b5` (2026-03-16) | ~05:01 | `configs/ppyoloe/README.md`, `configs/picodet/README_en.md` |
| W1-14-S14 | ultralytics/yolov5 | https://github.com/ultralytics/yolov5 | README | commit `af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce` (2026-10-21), релиз v7.0 | ~05:01 | прочитан |
| W1-14-S15 | cocoapi (pycocotools) | https://github.com/cocodataset/cocoapi | исходный код | commit `8c9bcc3cf640524c4c20a9c40e89cb6a2f2fa0e9` (2020-02-20) | ~05:01 | `PythonAPI/pycocotools/{cocoeval,coco}.py` прочитаны выборочно; PyPI-пакет pycocotools может отличаться — не проверялось |
| W1-14-S16 | LinQ: lin-q.ru/sol, lin-q.ru/tech, даташиты HPS/HX, 2025_HiTech_site_LinQ_A.pdf | https://lin-q.ru/sol ; https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf ; …/linq_hx_datasheet.pdf ; https://files.lin-q.ru/tpu/docs/2025_HiTech_site_LinQ_A.pdf | primary_documentation (маркетинг) | версий/дат в файлах не указано | ~04:48–05:01 | все скачаны и прочитаны (pypdf в SCRATCH venv); выписки в `W1-14_files\` |
| W1-14-S17 | SH17: A Dataset for Human Safety and PPE Detection in Manufacturing Industry (Ahmad, Rahimi) | https://arxiv.org/abs/2407.04590 ; https://github.com/ahmadmughees/SH17dataset | статья+репо | commit `2f832c289f9deea063367045ed8230b26e3e7ea9` (2024-12-04) | ~05:01 | статья — WebFetch-пересказ HTML; README, `sh17.yaml`, скрипты — прочитаны |
| W1-14-S18 | SHWD | https://github.com/njvisionpower/Safety-Helmet-Wearing-Dataset | репо | commit `c952631dfc352e0defdd54b4785a9be6576451ad` (2019-12-17) | ~05:01 | README прочитан; данные (Baidu/GDrive) не скачивались |
| W1-14-S19 | Fast PPE Detection for Real Construction Sites Using Deep Learning Approaches (CHV), Sensors 2021 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8156681 | статья | doi 10.3390/s21103478 | ~05:01 | WebFetch-пересказ |
| W1-14-S20 | pictor-ppe (ciber-lab) | https://github.com/ciber-lab/pictor-ppe | репо | commit `8f41c9525bbd1f45245f593c7502a1934eef06fa` (2024-12-18) | ~05:01 | README прочитан; графики результатов — изображения, не прочитаны |
| W1-14-S21 | HF `keremberke/yolov8m-hard-hat-detection`; HF dataset `keremberke/hard-hat-detection` | https://huggingface.co/keremberke/yolov8m-hard-hat-detection ; https://huggingface.co/datasets/keremberke/hard-hat-detection | artifact_metadata | model sha `65c3a88dc3fda5dd22711a55c46d079e2c95e2cf` (2023-02-22), dataset sha `694c61350faf9a6622586d6cf50f45e1631862dc` (2023-01-16) | ~05:01 | доступны; `best.pt` не скачивался |
| W1-14-S22 | Optimizing Helmet Use Detection in Construction Sites via Fuzzy Logic-Based State Tracking, Sensors 25(20) 6487 | https://www.mdpi.com/1424-8220/25/20/6487 (сайт отдаёт 403) → Europe PMC PMC12568081 fullTextXML | статья | doi 10.3390/s25206487, created 2025-10-21 | ~05:01 | текст получен через Europe PMC REST (дословно, локально) |
| W1-14-S23 | Поиски по event-level оценке СИЗ/касок | WebSearch ×3 | результаты поиска | — | ~05:01 | CVPRW 2023 AI City Track 5 PDF — HTTP 403; MDPI — 403 (обойдено через EuropePMC) |

---

## 6. Протокол честного сравнения вариантов (для нас)

Принцип: **разделять три вопроса и три набора чисел** — (А) качество детектора на нашей предметной области (офлайн, изображения), (Б) качество события (видео, тревоги), (В) латентность/пропускная способность по стадиям. Опубликованные цифры используются только как prior для отбора кандидатов, а не для выбора победителя.

### 6.1 Данные и сплиты (против утечек)
1. Сплит по группам: видео/камера/сцена/смена (не по кадрам). Любые кадры одного видео — в одном сплите. (Причина: F26, F28, F30 — нет проверки near-duplicates.)
2. Проверка near-duplicate между train/val/test перцептивным хешем и/или эмбеддингом; результат (число удалённых пар) записать. (Образец: Ultralytics Benchmark, F12.)
3. Аугментационные копии (Roboflow и т.п.) — только в train; в val/test — только исходные кадры. Фиксировать версию экспорта датасета.
4. Три роли: train / val (выбор чекпоинта, порогов) / test (одна финальная оценка). Не использовать один набор как val и test (F26). Тест не участвует в выборе conf-порога.
5. Каждому числу — размеры: число изображений, инстансов по классам, по размерным бинам, по камерам. Для малых тестов (порядка сотен изображений, как CHV-133) — доверительные интервалы бутстрэпом по группам; без интервалов разницу менее порядка нескольких п.п. не интерпретировать (F12: даже на 37 датасетах разброс между поколениями 1–2 п.п. при нефиксируемом seed).
6. Несколько seed для финальных кандидатов при разнице < ~2 п.п. (число seed — решение evaluation; обоснование — F12 «Seed 0 is not fully deterministic»).

### 6.2 Единый инференс-контракт
1. Одинаковые: imgsz, режим resize (letterbox vs stretch — соответствовать обучению; F30), нормализация, цветовой порядок, `max_det` не ниже максимального числа объектов на кадре (валидатор Ultralytics сам поднимает `max_det`, `_check_max_det`, val.py стр. 64–94).
2. NMS: один и тот же тип (class-aware vs agnostic), IoU, `multi_label` — зафиксировать и **выровнять между кандидатами**; для NMS-free моделей (YOLO26 `nms=False`, DETR-семейство) публиковать результат для **обеих** голов или явно одной (F05).
3. Геометрия: для сравнения с деплоем использовать `rect=False`/квадратный fixed-shape; отдельно сообщить rect-значение для связи с опубликованными таблицами (F09).
4. Два режима отчёта: (а) «benchmark» — conf=0.001 (дефолт val Ultralytics, F08) для AP/PR-кривых; (б) «operating point» — conf, выбранный на val по заданному критерию (F1 или целевая precision), и на test отчитываются P/R/FP на кадр именно при нём. Значение P/R из итоговой строки Ultralytics (F07) — при conf max-F1, не при 0.25 и не при рабочем пороге.

### 6.3 Метрики качества детектора
- Один и тот же оценщик для всех кандидатов: сохранить предсказания в COCO-JSON и считать одним инструментом (pycocotools или faster-coco-eval; не смешивать внутреннюю mAP Ultralytics с чужими; F08, F11, F32).
- Отчёт: AP50-95, AP50, AR; **по классам** (особенно нарушающий класс — «голова без каски»/`NO-Hardhat`; см. таксономию в W1-05), **по размерам** (small/medium/large; указать, в оригинальных пикселях или после масштабирования до imgsz; F11, F12), по камерам/освещению; confusion между helmet↔head↔no-helmet.
- Для каждого класса — количество GT и количество предсказаний; класс без GT выпадает из mAP (F07) — следить.
- Калибровка и сдвиг порога: сравнивать распределение score fp32 vs int8 (F13).

### 6.4 Скорость — раздельно, на целевом железе
- Стадии: декодирование видео; resize/letterbox; перенос host→device; forward на устройстве; перенос device→host; декод выходов/NMS; трекер; правила. Каждая стадия — отдельное число (F10 показывает, что даже Ultralytics-логи val и predict различаются по смыслу «preprocess»).
- Протокол: фиксировать версию драйвера/рантайма/компилятора, режим питания; прогрев (число итераций записать), синхронизация устройства перед остановкой таймера (как `Profile`), steady-state; отчёт p50/p95/p99 и пропускная способность при реальном числе потоков, не только среднее.
- Batch: сообщать batch=1 (латентность) и реальный рабочий batch/число потоков (пропускная способность) отдельно.
- Не переносить цифры между GPU/NPU: T4/A100/V100/RTX PRO 6000 ≠ RTX 4070 ≠ LinQ. Для RTX 4070 и LinQ чисел в этом исследовании нет и придумывать их нельзя.
- Для LinQ — отдельная колонка «device-only» и «end-to-end с хост-передачей», пока не выяснено, что входит в 2,3 мс (F21–F22).

### 6.5 fp32 vs int8
- Одна и та же обученная модель → fp32 baseline и int8 по пути компилятора LinQ (когда появится); **не сравнивать с другой моделью, обученной иначе** (в README YOLOv6 baseline квантованной таблицы — 35.9, заголовочный — 37.5; F20b).
- Калибровочный набор отдельный от test, репрезентативный (требование по аналогии: NVIDIA ≥500 изображений — F13, как гипотеза для LinQ DNN Quant; для LinQ число неизвестно).
- Отчёт: ΔAP50-95/ΔAP50 по классам и **по размерным бинам** (небольшие каски на дальнем плане — основной риск; цифры по ним в публикациях отсутствуют: unknown), ΔP/R при **фиксированном** и при **перевыбранном** пороге (F13), ΔFA/час; численная согласованность ONNX-fp32 vs torch vs int8 на одних и тех же входах (до NMS).
- Чек-лист переходов (CONTEXT §3): артефакт → загрузка → обучение → экспорт → граф корректен → согласованность → компилятор принимает → устройство исполняет → качество/скорость. Метрики пунктов независимы.

### 6.6 Событийный уровень (выписать для → evaluation)
- Определить событие: например «трек человека, класс головы без каски, ≥ k кадров из окна m, в зоне/кадре». Параметры (k, m) — выбираются на val-видео, фиксируются до test.
- GT: интервалы нарушений по видео (начало/конец), размечает человек; негативные длинные фрагменты (часы без нарушений) обязательны.
- Сопоставление: предсказанная тревога засчитывается, если пересекает GT-интервал с допуском по времени; считать event-precision, event-recall, задержку обнаружения, **ложные тревоги на камеру-час** при фиксированной рабочей точке, число переключений идентичности трека, влияющих на повторные тревоги. Цитируемая в MDPI-статье пара MOTA/IDF1 (F31) — про трекинг, не про тревоги.
- Ранжирование моделей по AP кадра не гарантирует ранжирование по FA/час (inference: на события влияют калибровка, устойчивость на «хвостах» и трекер); проверять отдельным экспериментом (E5).

### 6.7 Шаблон отчёта (одна строка на кандидата)
`модель@commit/веса(sha256) | данные(версия, split, n) | imgsz+режим resize | NMS/голова | conf | AP50-95/AP50 (all, small/med/large, по классам) | P/R/FP на кадр @рабочий порог | fp32/int8 Δ | скорость по стадиям (p50/p95), железо+стек, batch | событийные метрики | seed/число прогонов | дата`.

---

## 7. Противоречия и несопоставимости

**С1. Скорость между семействами Ultralytics (A100 vs T4).** F03/F04. Выбор меняет: нельзя ранжировать по столбцу «ms». Разрешение: измерять самим на одном железе (E3).

**С2. Footnote vs таблица для YOLO11.** В тегах v8.3.0, v8.3.100, v8.4.0 `docs/en/tasks/detect.md`: «Speed averaged … using an Amazon EC2 P4d instance … Reproduce by `yolo val detect data=coco.yaml batch=1 device=0|cpu`», а таблица `yolo11.md` (v8.3.0/v8.4.0) озаглавлена «Tesla T4 TensorRT». В v8.4.184 footnote: «TensorRT10 on an NVIDIA T4 … `nms=False`». Условия измерения исторически менялись/уточнялись; для чисел YOLO11 (1.5 мс) ссылаться только на актуальный footnote, оговаривая, что соответствие чисел заявленным условиям проверено лишь чтением, не измерением.

**С3. Ultralytics vs SAB (RF-DETR) для YOLO11/YOLO26.** F14: расхождение 2.1–2.9 AP (YOLO11) и 0.6–0.9 AP (YOLO26), latency 2.5 vs 1.5 мс (YOLO11-N). Обе стороны заинтересованы. Выбор меняет: какой YOLO11 «реально» дадут в экспорте через TensorRT-плагин NMS. Разрешение: E2 (локальный прогон `yolo val` на COCO val или на своей выборке и сверка с pycocotools).

**С4. Метки метрик HF-карточки.** F30: `type: precision` для значения `mAP@0.5(box)`, `verified: false`. Не использовать как эталон.

**С5. SH17: сплит и версия кода.** F26: «test» (статья) = «val» (README/yaml); `ultralytics==8.0.38` не поддерживает заявленные YOLOv9/v10. Статья vs README расходятся в счёте инстансов (76 318 по классам vs 75 994). Разрешение: скачать списки `train_files.txt`/`test_files.txt` с Kaggle и проверить пересечение и near-duplicates (E6) — не выполнялось (доступ к Kaggle не проверялся).

**С6. Pictor-PPE: 784 vs 774+698 изображений.** F29. Не разрешено; неважно для выбора, важно для ссылок.

**С7. «yolo5s» в списке LinQ.** F06(а): 37.4 (anchor-based v5s) vs 43.0 (v5su). Выбор меняет: эталон для fp32. Закрыть вопросом к linq_platform / по SDK.

**С8. FLOPs в разных единицах.** F06(в): Ultralytics GFLOPs = MACs×2; torchvision `_ops` у resnet18 1.814 (≈GMACs). Не сравнивать FLOPs между репозиториями без пересчёта.

---

## 8. Открытые вопросы

| # | Вопрос | Где искали | Чем закрыть |
|---|---|---|---|
| Q1 | Что именно измерено в LinQ «2,3 мс / 1,5 мс для ResNet-50 (batch=1)»: вариант (resnet50_v2 / resnet50_mlperf / torch_resnet50), вход, точность слоёв, один чип/узел, включены ли передача по PCIe, препроцессинг, постпроцессинг (softmax/argmax), метод усреднения/прогрев, версия компилятора, дата; что значит «оптимизации» (ручная настройка графа, частота 1 ГГц против 750 МГц, прунинг?) | lin-q.ru/sol, HPS/HX-даташиты, `2025_HiTech…pdf` | SDK/Performance Profiler, Model Zoo, вопрос организаторам/ХайТэк, реальный замер на LinQ → linq_platform |
| Q2 | Есть ли у LinQ опубликованные/внутренние числа качества (mAP) и латентности для `yolo5s/yolo8/yolo11` (размер, imgsz, fp32 vs int8) | те же материалы: найдено 0 | Model Zoo LinQ, SDK, спросить на хакатоне |
| Q3 | Сколько стоит int8-квантование (DNN Quant) для детектора по классам и размерным бинам | публикаций нет; для TRT — F13 (±0.04 mAP50-95 у v8n, без разложения) | эксперимент на LinQ/симуляция PTQ, E4 |
| Q4 | Почему Ultralytics-значение YOLO11 (39.5 AP) выше, чем в SAB (37.4)? | README RF-DETR, docs Ultralytics | E2 (локально) |
| Q5 | Как соотносятся внутренний mAP Ultralytics и pycocotools численно на нашем датасете и на COCO | код F08, F11, F32; число не измерялось | E2 |
| Q6 | Пер-датасетные результаты Ultralytics Benchmark для Safe Human 17 (SH17) по поколениям | docs (только макро) | Ultralytics Platform (доступ не проверялся) |
| Q7 | Есть ли публичные event-level методики/датасеты для СИЗ с интервальной разметкой | 3 WebSearch, MDPI-статья | расширенный поиск «temporal localization PPE», AI City Challenge Track 5 отчёты (PDF, 403); → datasets/evaluation |
| Q8 | Размерные (small/medium/large) AP для кандидатов на PPE-датасетах | не опубликованы (кроме макро Ultralytics Benchmark) | E4 через `save_json=True` (F11) |
| Q9 | Включает ли Ultralytics «Speed» в таблицах YOLO11/YOLOv8 NMS | footnote YOLO11 в v8.4.184 прямо не привязан; общий — `nms=False` (для YOLO26) | прочитать `ultralytics/utils/benchmarks` / воспроизвести `yolo val batch=1` на T4 (нет железа) |
| Q10 | Какая версия pycocotools/PyPI используется при публикации чисел в разных репозиториях | не проверялась | не нужен для выбора; для воспроизведения зафиксировать у нас |

---

## 9. Предлагаемые эксперименты

Окружение пока не установлено (не подставлять типичные значения); ниже — шаги и критерии. Команды берутся из документации с источником; всё остальное — псевдокод.

**E1. «val mAP vs метрики при рабочем пороге» (локально, любой CPU/GPU).** Кандидат: `yolo11n.pt` (assets v8.4.0, sha256 `0ebbc80d…ee1`, F03/S03) либо любой чекпоинт, обученный на нашем датасете; Ultralytics v8.4.184. Шаги: `yolo val model=… data=<наш.yaml> conf=0.001` (документировано: modes/val.md), затем `conf=0.25` и `conf=<рабочий>`; сохранить `Precision/Recall/mAP50/mAP50-95`, `PR_curve.png`, `F1_curve.png`. Ожидаемое: mAP при conf=0.25 ниже (обрезанная кривая, F07/F08); P/R из строки при conf=0.001 — при conf max-F1. Что измерять: P, R, FP/кадр при трёх conf; сравнить с `predict` (conf=0.25) на 100 кадрах: число боксов. Не подтверждает: качество на LinQ. Остановка: сделано, когда есть таблица по трём conf.

**E2. «Внутренний mAP Ultralytics vs COCO-evaluator» (COCO val2017 или наш датасет).** Кандидат: те же чекпоинты. Шаги: `yolo val … save_json=True` (F11) → получить `predictions.json`; посчитать отдельным pycocotools-скриптом (псевдокод: `COCOeval(gt, dt, 'bbox')` по `cocoeval.py` @8c9bcc3c). Измерять: разность AP50-95 между внутренней и COCO-метрикой; влияние `rect=True/False` (F09), `iou=0.65/0.7` (F17), `max_det=100/300`, `multi_label`. Интерпретация: если разность < доли п.п. — внутренняя метрика пригодна для отбора; иначе — использовать единый COCO-оценщик. Не подтверждает: причину расхождения с SAB (для этого нужен TRT-экспорт с NMS-плагином).

**E3. «Скорость по стадиям на RTX 4070 (и CPU)».** Кандидаты: YOLOv8n/11n/26n (чекпоинты S03), `.pt` и ONNX fp32. Шаги: `yolo val … batch=1` (печатает preprocess/inference/loss/postprocess, F10) и собственный замер вокруг `predict` на фиксированных кадрах (псевдокод: прогрев, `cuda.synchronize`, p50/p95). Записать: драйвер/CUDA/ONNX Runtime-версии. Интерпретация: число — только для RTX 4070 и только этого стека; **не** переносится на LinQ. Остановка: стабильные p50/p95 на ≥ N прогонов (N фиксируется заранее).

**E4. «Кандидаты на нашем датасете: сопоставимый протокол + размерные бины».** Когда будет датасет: шаги по §6.1–6.5; `yolo val … save_json=True` для S/M/L AP (F11) с пересчётом площади к 640-масштабу по рецепту Ultralytics Benchmark (F12) и также в пикселях оригинала; ≥ 3 seed. Измерять: AP по классам и размерам, P/R/FP на кадр при рабочем пороге. Подтверждает: порядок кандидатов на наших данных. Не подтверждает: порядок на LinQ int8.

**E5. «Ранжирование по AP vs ранжирование по тревогам».** Кандидаты: 2–3 модели с близким AP. Данные: ≥ несколько часов размеченного видео с интервалами нарушений. Шаги: §6.6. Измерять: event-P/R, FA/час, задержку. Интерпретация: если порядок отличается от AP, выбирать по событию. Не подтверждает: перенос на другие камеры.

**E6. «Проверка утечки SH17/CHV/SHWD» (если нужно использовать как предобучение/эталон).** Скачать списки сплитов (Kaggle/GDrive), посчитать перцептивные хеши, найти пары train↔test, SHWD↔CHV↔GDUT-HWD. Измерять: доля near-duplicate. Остановка: не нужен, если эти датасеты используются только как источник train и не служат эталоном.

**E7. LinQ (только при доступе к устройству/SDK).** Шаги: измерить ResNet-50 batch=1 в двух областях (device-only / host-to-host) на той же сборке компилятора, зафиксировать вариант модели и вход; затем те же кандидатные детекторы; сравнить fp32-эталон ONNX и int8 по §6.5. Подтвердит или опровергнет F21–F22. Условие остановки: ответ на Q1.

---

## 10. Передачи соседям

→ **evaluation**:
- Протокол §6 целиком (данные/сплиты, единый инференс-контракт, раздельный тайминг, fp32↔int8 по классам и размерам, событийный уровень с FA/камера-час).
- Не использовать как эталон: SH17 (val=test, версия кода), CHV (133 теста, выборка из SHWD/GDUT-HWD), SHWD (`person`=голова без каски, неопределённая mAP), HF-карточки keremberke (метка метрики).
- Ультралитикс-определения: P/R при max-F1 (не при 0.25), mAP макро по классам с метками, `rect` геометрия (F07–F09).
- Событийных публичных метрик не найдено (F31) — нужна собственная разметка интервалов.

→ **linq_platform**:
- Q1/Q2 (условия 2,3 мс; числа для yolo5s/8/11; что такое «yolo5s»).
- F23: HX-даташит — TF ≥ 2.9.1, PyTorch ≥ 2.0.0, ONNX ≥ 1.15.0; «Model Zoo» на портале разработчика.
- Нужны сведения: принимает ли компилятор NMS-free выход YOLO26 `(N,300,6)` и/или сырой `(N,nc+4,8400)` (F05); как LinQ обрабатывает сигмоиду/Concat (для калибровки порога после int8; F13 как аналогия TRT, не LinQ).
- Для fixed-shape графа: потребуется `rect=False` измерение (F09).

→ **datasets**: SH17 лицензия CC BY-NC-SA 4.0 + Pexels (F25); деление на группы; near-duplicate чек; CHV/SHWD/GDUT-HWD перекрываются; размеры объектов: SH17 — 39 764 из 75 994 аннотаций < 1% площади.

→ **training_strategy**: ранжирование на COCO не предсказывает после fine-tune (F12) → не выбирать по COCO; несколько seed; выбор `best.pt` по rect-валидации (F09); для сильных предобучений (Objects365 у D-FINE/RT-DETR) README предупреждает о переобучении на простых классах (F15).

→ **video_architecture**: раздельные стадии тайминга (§6.4); пропускная способность ≠ латентность; для NPU-стыка важно, что в публикациях «speed» чаще = forward без декода/NMS.

→ **operator_product / hackathon_strategy**: выбирать модель по метрике, привязанной к событию (FA/час), а не по COCO-mAP; цифры конкурентов в публикациях не переносятся на LinQ.

→ **W1-05 / W1-16 (если читают)**: SH17/CHV/SHWD/Pictor/Hard Hat — условия и риски в F25–F30; в SHWD `person`=голова без каски; в Hard Hat (Roboflow) обучающий ресайз «Stretch».

---

## 11. Запросы эскалации

1. **Воспроизведение расхождения YOLO11 39.5 vs 37.4 (SAB) и вклада NMS-плагина TensorRT** — нужен GPU-эксперимент (T4 или аналог) и репозиторий roboflow/single_artifact_benchmarking, который я не открывал. Уже найдено: README @5b22dfc0, Ultralytics docs v8.4.184, определения F07–F11.
2. **Разбор Table S8/S9/S10 статьи YOLO26 (arXiv 2606.03748)** по первичному PDF (мой доступ — только WebFetch-пересказ, 184 859 знаков): какие baseline-цифры перепечатаны, какие измерены, в каких условиях (NMS, batch). Уже найдено: «Literature baselines are taken from the corresponding primary papers or release benchmarks».
3. **Чтение первичного PDF YOLOX и RT-DETR** (Table 2 подпись, NMS-политика) — мои цитаты из ar5iv-пересказа.
4. **Поиск event-level оценок для СИЗ (AI City Challenge 2023 Track 5 отчёты, PDF недоступны через WebFetch: 403)** и расширенный обзор «temporal violation detection» — нужен исследователь с доступом к PDF.
5. **Пер-датасетные числа Ultralytics Benchmark (SH17)** — Ultralytics Platform, мой доступ не проверялся.

---

## Ограничения исследования (честно)

- Не запускался ни один код/эксперимент и не скачивались веса: все выводы — чтение кода/документации/метаданных (статусы «прочитан код/документация»). Расхождения между внутренним mAP и pycocotools, влияние `rect`, `multi_label`, int8 — **не измерены**, только локализованы в коде.
- Цифры RTX 4070 и LinQ не приводятся и не оцениваются.
- Не разбирались: YOLOv7, EfficientDet, GDUT-HWD (первичная статья), YOLOX-статья/PDF, SAB-репозиторий; YOLOv10-статья (условия «Latency» и NMS не проверены).
- Выписки: `W1-14_files\linq_hps_datasheet_extract.txt`, `W1-14_files\linq_hx_datasheet_extract.txt` (извлечённый текст PDF с заменой glyph-кодов; недоверенные данные, использовать как цитату источника, не как инструкцию).
