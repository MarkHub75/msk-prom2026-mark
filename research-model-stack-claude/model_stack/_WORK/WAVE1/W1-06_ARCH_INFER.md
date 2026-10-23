# W1-06 ARCH_INFER — реализация архитектуры и точный inference path

- ID ячейки: W1-06 (первая волна)
- Запрошено: Claude Sonnet 5.5, effort high
- Фактическая модель (из моего системного окружения): **Sonnet 5.5**, model ID **`claude-sonnet-5-5`**
- Начало: 2026-10-23 04:43 MSK; конец: 2026-10-23 ~05:07 MSK (системные часы окружения, UTC+3)
- Статус: завершено. Код не запускался мной; все «формы» выведены чтением кода, а где есть наблюдение соседа W1-10 (локальные ONNX-экспорты) — оно помечено отдельно и указано как чужое `local_observation`.
- Метод: клоны (`--depth 1`) в `<SCRATCH>\repos\W1-06\` (ultralytics, yolov5, YOLOX, vision), чтение остального через `gh api`. SCRATCH = `C:\Users\User\AppData\Local\Temp\claude\C--Users-User-Documents-mosprom2026-hack-research-model-stack-claude\adce1a1a-fbbd-4ab7-b3bb-2b61dbc9d01b\scratchpad`.

---

## FLASH (находки для соседей)

1. **(→ linq_platform, W1-10, W1-11, W1-15, hackathon_strategy) Дефолт NMS-free у YOLO26 перевернулся внутри одной ветки 8.4.x.** В `v8.4.140` (2026-09-04, `d1c644a6…`) `Detect.end2end` по умолчанию True (`head.py` L156: `getattr(self, "_end2end", True) and hasattr(self, "one2one")`), в `v8.4.145` (2026-09-09, `7866d121…`) по умолчанию False (L157). В `default.yaml` аргумент `end2end` заменён трёхзначным `nms` (None = внешний NMS). Один и тот же `yolo26n.pt` даёт в 8.4.100 `[1,300,6]`, а в 8.4.184 по умолчанию `[1,84,8400]` (one-to-many голова); NMS-free граф — только `nms=False`. W1-10 наблюдал вторую половину (локально). Любые инструкции «YOLO26 экспортируется end2end по умолчанию» привязывать к версии.
2. **(→ training_strategy, datasets, W1-07) Структура cls-ветки Detect у YOLOv8 зависит от версии ultralytics, которой собрана модель из YAML.** В `v8.3.0…v8.3.16` `Detect.__init__` строит cls-ветку с depthwise (DWConv3→Conv1) безусловно (как у YOLO11), флаг `legacy` (обычные Conv3→Conv3 для v3/v5/v8/v9) появился в коммите `899fb0495e2` (2024-10-19), первый тег `v8.3.17`. Модель `yolov8n.yaml`, собранная ultralytics 8.3.0–8.3.16, получит другие ключи state_dict (`cv3.i.0.0.*`) и другой граф, чем собранная ≥8.3.17 (`cv3.i.0.*`). Для старта обучения лучше загружать `.pt` (структура берётся из pickled-объекта), а не пересобирать из YAML — но для этого pickled-объект должен быть загружаем (см. п.4).
3. **(→ linq_platform) Внутри «yolo11» и «yolo26» есть блоки с MatMul активация×активация + Softmax (C2PSA и, у YOLO26, ещё `C3k2(attn=True)` на P5).** Это единственные не-свёрточные подграфы во всём ultralytics-стеке; для yolo11n это `Attention` (2×MatMul, 1×Softmax) при N=400 токенов на P5@640, для yolo26n — два таких блока (ONNX: MatMul 4, Softmax 2, W1-10 local_observation). В YOLOv8, YOLOv5, YOLOX, SSDlite их нет. «yolo11» на странице LinQ может скрывать именно это — вопрос к linq_platform (оператор MatMul/Softmax, не сеть целиком).
4. **(→ W1-03, W1-07) `HumanModel`/`HumanDetect`:** по `grep -rIl "HumanDetect\|HumanModel"` в клонах ultralytics@e6d5fc59 (код пакета идентичен v8.4.184), yolov5@af08ba15 и YOLOX@6ddff482 совпадений нет (local_observation) → `*-human.pt` невозможно разобрать/загрузить публичным кодом; подтверждает FLASH W1-03.
5. **(→ W1-11, linq_platform) Выход дефолтного Ultralytics-ONNX склеивает пиксельные координаты и вероятности** (`torch.cat((dbox, scores.sigmoid()), 1)`, `head.py` L217) — подтверждение кодом FLASH-3 W1-11; правильная точка среза для квантования — до `_inference` (три пары `box_s*/cls_s*`), см. §6.1.
6. **(→ W1-11, evaluation) У разных семейств разные «обязанности» внешнего кода:** YOLOX (`export_onnx.py`) по умолчанию экспортирует **без decode** (`decode_in_inference=False`): внешний код обязан делать `(xy+grid)*stride`, `exp(wh)*stride`; вход YOLOX — BGR 0..255 без нормализации и letterbox с паддингом 114 **в левый-верхний угол**. YOLOv5-оригинал — `[1,25200,85]` с objectness; Ultralytics — `[1,84,8400]` без objectness. См. таблицу §5.

---

## Резюме для оркестратора

1. **Ultralytics YOLOv8/YOLO11 (detect), 8.4.184:** сеть принимает `float32 [B,3,H,W]` RGB 0..1 (нормализация вне графа), выходы трёх уровней (strides 8/16/32) идут в `Detect`; в экспорте по умолчанию внутри графа остаются DFL (Reshape→Transpose→Softmax→1×1 Conv), `dist2bbox`, умножение на stride и Sigmoid классов; итог один тензор `[B, 4+nc, A]`, A=8400 при 640×640, боксы `cx,cy,w,h` в пикселях входа, классы — независимые sigmoid, objectness нет. NMS снаружи (по умолчанию).
2. **Различие режимов:** train → dict `{"boxes":[B,64,A],"scores":[B,nc,A],"feats":[…]}`; eval (не export) → `(y, preds)`; export → один тензор. `fuse()` складывает BN в Conv (SiLU остаётся как Sigmoid+Mul в ONNX) и удаляет неиспользуемую голову. `C2f/C3k2` в экспорте переключаются на `forward_split` (ONNX Split вместо chunk).
3. **YOLO11 отличается от YOLOv8 тремя вещами, существенными для компилятора:** `C3k2`, `C2PSA` (attention: MatMul act×act, Softmax, depthwise 3×3), и cls-ветка головы на depthwise-свёртках. YOLOv8 — только Conv/Split/Concat/MaxPool/Resize/SiLU + Softmax в DFL.
4. **YOLO26:** `reg_max=1` (DFL нет, `dfl=Identity`, голова выдаёт 4 расстояния ltrb напрямую), две пары голов (`cv2/cv3` one-to-many и `one2one_cv2/cv3`), атрибуция attention-блоков удваивается. Дефолтный экспорт 8.4.184 — one-to-many `[B,84,8400]` (xywh, без NMS); `nms=False` → one-to-one + `TopK(300)` в графе → `[B,300,6]` `x1,y1,x2,y2,score,cls` (TopK/GatherElements/Mod/ReduceMax — высокорисковые для LinQ операции; не по умолчанию).
5. **YOLOv5 (оригинал, ultralytics/yolov5):** anchor-based, 3 якоря/уровень, `[1,25200,85]` (xywh px, obj, cls; всё уже под sigmoid, декодирование `(2σ−0.5+idx)·s` и `(2σ)²·anchor` в графе); **это не то же самое, что `yolov5su.pt`** (ultralytics YOLOv5u: anchor-free, DFL, без objectness, `[1,84,8400]`). Какой из двух стоит за «yolo5s» LinQ — не установлено.
6. **YOLOX:** decoupled-голова, anchor-free без DFL; экспорт по умолчанию без decode (внешний код обязан повторить grid/stride/exp), Focus-стем (strided slice ×4), SiLU, вход 0..255 BGR. Лицензионную чистоту не проверял (→ W1-04).
7. **SSDlite (torchvision) и TF OD ssd_mobilenet_v2:** принципиально другой контракт — сеть выдаёт сырые `bbox_regression [N,A,4]` и `cls_logits [N,A,C]` (A≈3234 для ssdlite320 по расчёту; 1917 для TF 300×300 по формуле, не наблюдалось), якоря и декодирование с весами (10,10,5,5), softmax/sigmoid и NMS снаружи сети; в torchvision препроцесс (resize+normalize) внутри `forward`, а не в графе после экспорта ядра.
8. **PP-YOLOE+:** DFL (reg_max=16, 17 бинов) + ESE-attention на global avg pool; strides перечислены в порядке 32,16,8; экспорт идёт через Paddle→paddle2onnx (отдельный инструмент); препроцесс — stretch-resize без letterbox. PicoDet — только README.
9. **Главные разрывы:** (i) какие именно реализации/размеры/входы стоят за `yolo5s/yolo8/yolo11` на LinQ — unknown (охват: сайт, руководство IVA H1 через W1-01/W1-12, GitHub — нет публичных исходников вендора); (ii) принимает ли компилятор LinQ Split, SiLU(Sigmoid·Mul), MaxPool 5×5/1, Resize nearest, MatMul act×act, Softmax, Transpose, многовыходной граф — не установлено (→ linq_platform); (iii) численная согласованность «внешний decode по сырым выходам» против «внутреннего» нигде не проверена (предложен эксперимент E1).

---

## 1. Факты

Формат: ID — утверждение; основание; источник и локатор; область применимости; статус проверки; оговорки. «Прочитан код» ≠ «выполнен экспорт».

### 1.1 Версии и области применимости

- **W1-06-F01** — Версия Ultralytics: PyPI latest `8.4.184` = тег `v8.4.184` = commit `f7dd275e5853801674ca78ef51896617bb5362ba` (release 2026-10-22T17:41:34Z); `main` на момент чтения = `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`. `git diff --stat v8.4.184 HEAD -- ultralytics` в моём клоне пуст (различаются 84 файла только вне пакета `ultralytics/`, в основном `docs/`), поэтому **все номера строк ниже для `ultralytics/…` одинаково верны для `v8.4.184` и `e6d5fc59`**. Основание: artifact_metadata (`gh api`, PyPI JSON) + local_observation (git diff). Источник W1-06-S01. Статус: проверена доступность, дифф.
- **W1-06-F02** — `ultralytics/yolov5` HEAD = `af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce` (2026-10-21), latest release `v7.0` (2022-11-22) = commit `915bbf294bb74c859f0b41f1c23bc395014ea679`. Семантика `Detect.forward` в `models/yolo.py` v7.0 и HEAD совпадает (diff касается форматирования и импортов; логика `forward`/`_make_grid` сверена построчно чтением v7.0 L36–95 и HEAD L71–128). Основание: artifact_metadata + source_code. S05. Статус: прочитан код обоих.
- **W1-06-F03** — YOLOX: HEAD `6ddff4824372906469a7fae2dc3206c7aa4bbaee` (2025-06-08), последний release `0.3.0` (2022-04-22; на HEAD тега нет). Основание: artifact_metadata (`gh api`, `git`). S06.
- **W1-06-F04** — torchvision: latest `v0.29.1` (2026-09-30) = `1f1a920d685d46dfbe187934b785b7ecb7a182f2`; `main` = `c725e823011284b77082320577d288f82b36683c`; `git diff --stat v0.29.1 HEAD -- torchvision/models/detection` пуст → номера строк `ssd.py`/`ssdlite.py` одинаковы. Основание: artifact_metadata + local_observation. S07.

### 1.2 Ultralytics: Detect (YOLOv8 / YOLO11 / YOLOv5u / YOLO26) — код @ `v8.4.184`

- **W1-06-F10** — Конструктор `Detect(nc=80, reg_max=16, end2end=False, ch=())`: `no = nc + 4*reg_max`; `cv2` (box) на каждый уровень = `Sequential(Conv(x,c2,3), Conv(c2,c2,3), Conv2d(c2,4*reg_max,1))`, `c2 = max(16, ch[0]//4, 4*reg_max)`; `cv3` (cls) при `legacy` = `Sequential(Conv(x,c3,3), Conv(c3,c3,3), Conv2d(c3,nc,1))`, иначе `Sequential(Sequential(DWConv(x,x,3),Conv(x,c3,1)), Sequential(DWConv(c3,c3,3),Conv(c3,c3,1)), Conv2d(c3,nc,1))`, `c3 = max(ch[0], min(nc,100))`; `dfl = DFL(reg_max) if reg_max>1 else Identity`; при `end2end=True` создаются глубокие копии `one2one_cv2/one2one_cv3`. Основание: source_code, `ultralytics/nn/modules/head.py` L108–143 @ f7dd275. Статус: прочитан код. Согласуется с трассами W1-10 (cls-ветка yolo11n: 80 каналов, `cv3.0.0.0` DW; box-ветка yolo26n: 16 каналов, выход 4).
- **W1-06-F11** — Флаг `legacy`: `parse_model` стартует с `legacy=True` (`tasks.py` L2086), сбрасывает в False при встрече `C3k2` (L2203), `A2C2f` (L2207), `C2fCIB` (L2211), и присваивает **атрибут класса** `m.legacy = legacy` перед созданием `Detect/Segment/Pose/OBB` (L2245). Следствие: YAML на `C2f` (yolov8.yaml) → обычная cls-ветка; YAML на `C3k2` (yolo11.yaml, yolo26.yaml) → depthwise cls-ветка; `yolov5.yaml` (`C3`) → legacy. Основание: source_code. Статус: прочитан. Оговорка: атрибут класса — процессно-глобальное состояние; прямое создание `Detect(...)` после разбора yolo11-модели в том же процессе наследует `legacy=False` (inference из кода).
- **W1-06-F12** — История `legacy`: коммит `899fb0495e2ad05a6a1b0a34909e25e0a8f6b032` («Backward compatibility support for legacy models», 2024-10-19) добавил `legacy`; `git describe --contains` → `v8.3.17~1`. В `v8.3.0` (`6e43d1e1e5db72afbf686dee6745669bcb124b0a`) `Detect.__init__` строит DWConv cls-ветку безусловно (чтение `head.py` @ v8.3.0). Основание: source_code + artifact_metadata (git). S02, S04. Статус: прочитан дифф коммита. Оговорка: не установлено, какой именно версией обучены опубликованные `yolov8n.pt` и т.п. — это pickled-объекты со своей структурой (→ W1-03).
- **W1-06-F13** — `Detect.forward` (L180–204): `forward_head` считает `boxes = cat([box_head[i](x[i]).view(bs, 4*reg_max, -1) …], dim=-1)` → `[B,4*reg_max,A]` и `scores = cat([cls_head[i](x[i]).view(bs, nc, -1) …], dim=-1)` → `[B,nc,A]` (L169–178). **Train** (`self.training`): возвращается словарь `{"boxes","scores","feats"}` (для end2end — `{"one2many":…, "one2one":…}`, где вход one-to-one голов `detach()`-ится, т.е. они не влияют на backbone). **Eval/predict (не export)**: `(y, preds)`. **Export** (`Detect.export=True`): `y` один тензор. Основание: source_code. Статус: прочитан. Оговорка: в `v8.3.0` train возвращал список тензоров `[B, 4*reg_max+nc, h, w]`, а eval — `(y, x)` (`head.py` @ v8.3.0 L58–68): код, читающий выход `model.train()`-режима напрямую, версионно зависим.
- **W1-06-F14** — `_inference` (L206–227): `dbox = decode_bboxes(dfl(boxes), anchors.unsqueeze(0)) * strides`; результат `torch.cat((dbox, scores.sigmoid()), 1)` → **`[B, 4+nc, A]`**. `decode_bboxes` = `dist2bbox(…, xywh = not end2end and not xyxy, dim=1)` (L243–247): по умолчанию боксы **`cx, cy, w, h`**; `xyxy` — при `end2end` или когда экспортёр выставил `m.xyxy = args.nms and …` (exporter L952). Единицы: расстояния DFL — в клетках сетки, анкеры — центры клеток (+0.5), умножение на `strides` даёт **пиксели входа сети** (то есть после letterbox, не нормированные). Кла́ссовые оценки — независимые sigmoid (многометочные), objectness отсутствует. Основание: source_code (`head.py` L206–227, L243–247; `tal.py` L464–490 `make_anchors`, L493–512 `dist2bbox`). Статус: прочитан. Сверено с наблюдением W1-10: дефолтный ONNX `output0 [1,84,8400]`.
- **W1-06-F15** — Якорные точки: `make_anchors(feats, strides, 0.5)` для каждого уровня строит сетку `(sx = arange(w)+0.5, sy = arange(h)+0.5)` с порядком «строка за строкой» (`meshgrid(sy,sx,"ij")`, `stack((sx,sy),-1).view(-1,2)`), уровни склеиваются в порядке **P3(s=8), P4(s=16), P5(s=32)**; `A = Σ (H/s)(W/s)` = 6400+1600+400 = **8400 при 640×640**, 5040 при 384×640 (W1-10 наблюдал `[1,84,5040]`). Пересчёт — когда `self.dynamic or self.shape != shape`; экспортёр ставит `m.shape=None`, `m.dynamic=args.dynamic` (exporter L927–952). Основание: source_code (+ чужое local_observation для 5040). Статус: прочитан. Оговорка: что в статическом ONNX якоря и stride — константы, подтверждается лишь косвенно: у `yolo11n_default` в op_matrix нет `Range/Shape/ConstantOfShape`, а у `yolo11n_dynamic` есть `Range 6, Shape 11, ConstantOfShape 3, Gather 12` (W1-10 local_observation).
- **W1-06-F16** — `DFL(c1=16)` (`block.py` L60–82): `x.view(b,4,c1,a).transpose(2,1).softmax(1)` → фиксированная (requires_grad False) Conv2d 1×1 с весами `arange(c1)` → `[b,4,a]`. Распределение по 16 бинам на сторону (l,t,r,b), Softmax по оси бинов. В ONNX это Reshape→Transpose→Softmax→Conv(1×1)→Reshape. Основание: source_code. Статус: прочитан; число Softmax у yolov8n=1, Transpose=1 (W1-10 op_matrix) согласуется.
- **W1-06-F17** — `Conv` = `Conv2d(bias=False)` → `BatchNorm2d` → `SiLU` (`conv.py` L48–87, `default_act = nn.SiLU()`). `BaseModel.fuse()` (`tasks.py` L243–280): для каждого `Conv/Conv2/DWConv` с `bn`: `m.conv = fuse_conv_and_bn(...)`, `delattr(m,"bn")`, `m.forward = m.forward_fuse` (т.е. Conv+SiLU); `Detect.fuse()` удаляет неиспользуемую ветку. Экспортёр вызывает `model.eval(); model.float(); model = model.fuse(imgsz=…)` до экспорта (exporter L909 `model.eval()`, L911 `model.fuse(imgsz=…)`, цикл по модулям L927 и далее). SiLU в ONNX = `Sigmoid` + `Mul` (нет отдельного оператора): у yolov8n 58/58, yolo11n 78/79 (W1-10). Основание: source_code + чужое local_observation. Статус: прочитан.
- **W1-06-F18** — `C2f` (`block.py` L291–322): `y = list(cv1(x).chunk(2,1))`; затем цепочка `Bottleneck`; `cv2(cat(y))`; `forward_split` (L317) — тот же граф с `split((c,c),1)`. Экспортёр: `elif isinstance(m, C2f) and not is_tf_format: m.forward = m.forward_split` (exporter L956–957; `is_tf_format` L641 = saved_model/pb/edgetpu). `C3k2` — подкласс `C2f` (L1069), поэтому тоже переключается. Следствие: в ONNX `Split` (axis 1, равные части) вместо `chunk`; число Split: yolov8n 8, yolo11n 10 (W1-10). Основание: source_code + чужое local_observation.
- **W1-06-F19** — `SPPF` (`block.py` L211–238): `cv1 = Conv(c1, c1//2, 1, act=False)`, один `MaxPool2d(k=5, s=1, p=2)` применяется 3 раза последовательно, `cat` четырёх, `cv2`; в yolo26.yaml `SPPF, [1024, 5, 3, True]` — с остаточной связью (`add = shortcut and c1==c2`). ONNX: `MaxPool` ×3 (W1-10). Upsample в neck — `nn.Upsample(None, 2, "nearest")` → ONNX `Resize` ×2 (W1-10).
- **W1-06-F20** — YOLO11-специфика (`yolo11.yaml`): `C3k2` (подкласс `C2f`; внутренние блоки `Bottleneck` или `C3k` при `c3k=True`; при `attn=True` — `Bottleneck`+`PSABlock`) и `C2PSA` после SPPF (слой 10): `cv1 → split(c,c) → n×PSABlock(b) → cv2(cat(a,b))`. `PSABlock` = `x + Attention(x)`, затем `x + FFN(x)` (FFN — две 1×1 Conv). `Attention` (`block.py` L1271–1321): `qkv = Conv1×1`, `view(B, heads, 2·key_dim+head_dim, N)`, `split([key_dim,key_dim,head_dim], dim=2)`, `attn = ((q*scale)^T @ k).softmax(-1)`, `x = (v @ attn^T).view(B,C,H,W) + pe(v.reshape(B,C,H,W))` (`pe` — depthwise 3×3), `proj` 1×1. **Оба операнда MatMul — активации**, N = H·W токенов (у P5@640 N=400, матрица внимания `[B, heads, 400, 400]`). Для yolo11n: P5-каналы 256 → C2PSA c=128, `num_heads = max(128//64,1) = 2`, `key_dim = 32`, `head_dim = 64` (вывод из кода и `make_divisible(1024·0.25,8)`); для yolo11s: c=256, heads=4. ONNX yolo11n: `MatMul 2, Softmax 2` (1 — DFL, 1 — attention), у yolov8n `MatMul` нет (W1-10). Основание: source_code + чужое local_observation. Статус: прочитан. Оговорка: на exporter L955 для `coreml` включается `F.scaled_dot_product_attention` — к LinQ не относится.
- **W1-06-F21** — YOLO26 (`cfg/models/26/yolo26.yaml` @ v8.4.184): `end2end: True`, `reg_max: 1`; backbone как у YOLO11 (C3k2, SPPF с shortcut, C2PSA), в neck `C3k2` с `c3k=True`, последний `C3k2 [1024, True, 0.5, True]` (4-й аргумент — `attn=True` → `PSABlock` внутри P5-блока). Итого два attention-блока (ONNX: `MatMul 4, Softmax 2`, у yolo26n `reg_max=1` → DFL-Softmax нет; W1-10). Заявленные на `n`: 260 слоёв, 2 572 280 параметров, 6.1 GFLOPs (комментарий в yaml, author_statement, не перепроверено).
- **W1-06-F22** — YOLO26 `Detect` (reg_max=1): `dfl = Identity`, box-ветка выдаёт 4 канала (ltrb-расстояния в клетках без softmax), `c2 = max(16, ch[0]//4, 4) = 16` для n; две независимые пары голов `cv2/cv3` (one-to-many) и `one2one_cv2/cv3`. **Выбор головы при инференсе** — свойство `end2end` (L155–158): `one2one_cv2 is not None and (_end2end or cv2 is None)`; при `end2end` `_inference` берёт `preds["one2one"]`, боксы декодируются в **xyxy**, затем `postprocess` (L249–264) + `get_topk_index` (L266–288): top-`k` (`k=min(max_det=300, A)`) по max-классу, затем top-k по (anchor×class) `scores.flatten(1)`, `class = index % nc`, на выходе **`[B, 300, 6]` = `[x1,y1,x2,y2,score,class_idx(float)]`**, координаты в пикселях входа. `fuse()`: при `end2end` удаляются `cv2/cv3` (one-to-many), иначе — `one2one_*`. Основание: source_code. Статус: прочитан; формы `[1,300,6]` и состав операций (TopK 2, GatherElements 3, Mod 1, ReduceMax 1, Cast 1, Expand 2, Flatten 1, Unsqueeze 4) подтверждены W1-10 для `yolo26n_e2e`.
- **W1-06-F23** — Что включает NMS-free: **в 8.4.184** `exporter.py` L721–724: `model.end2end = self.args.nms is False or (fmt == "axelera" and nms is None and one2one_cv2 is not None)`; предиктор (`predictor.py` L475) и валидатор (`validator.py` L173) делают то же — **по умолчанию (nms=None, «внешний NMS») активна one-to-many голова**; `default.yaml` L61: «`nms`: None: external NMS (default); True: embed NMS on export; False: NMS-free head if available». Для форматов rknn, ncnn, executorch, paddle, imx, edgetpu, qnn end2end принудительно выключается (L726–728). Основание: source_code @ f7dd275 + артефакт: W1-10 локально получил `yolo26n_default [1,84,8400]` (one-to-many, 368 узлов) и `yolo26n_e2e [1,300,6]` (nms=False, 384 узла).
- **W1-06-F24** — Граница смены дефолта (см. FLASH-1): `default.yaml` в тегах v8.4.100/130/135/140 содержит `end2end:` (bool, optional) и `nms: False`; в v8.4.145/150/165/175/180/184 — только `nms:` (None/True/False). В `head.py` @ v8.4.100 `Detect.end2end` → `getattr(self,"_end2end",True) and hasattr(self,"one2one")`, @ v8.4.140 то же (L156), @ v8.4.145 — как в 8.4.184. Основание: source_code + artifact_metadata (`gh api` на тегах, даты коммитов тегов: v8.4.140 2026-09-04T22:50:34Z, v8.4.145 2026-09-09T12:15:31Z). Статус: прочитаны конкретные строки default.yaml и head.py на этих тегах; экспорт на старых версиях не выполнялся.
- **W1-06-F25** — Встроенный NMS (`nms=True`): `model = NMSModel(self.model, args)` (exporter L1169), `m.xyxy=True`; в ONNX добавляются операции NMS (точный перечень по `op_matrix` W1-10 для yolov8n_nms: NonMaxSuppression 1, NonZero 1, ScatterND 1, GatherND 3, Gather 9, Where 1, Pad 1, ArgMax 1, ReduceMax 1, Greater 1, Squeeze 1; TopK нет; выход `[1,300,6]`). Основание: source_code + чужое local_observation.
- **W1-06-F26** — ONNX-экспорт Ultralytics: `torch.onnx.export(..., dynamo=False при torch>=2.4, opset_version=opset, input_names=["images"], output_names=["output0"] (+"output1" для segment), dynamic_axes=…)` (`utils/export/engine.py` L90–128); `opset = args.opset or best_onnx_opset(onnx)` (L62–86): torch 2.0–2.3 → 17, иначе 18 (и ≤ `onnx.defs.onnx_opset_version()`); `min_opset` = 9 (nearest Upsample), 11 при `nms`; `simplify: True` по умолчанию (`default.yaml` L89) → `onnxslim`; для динамики оси `{0:batch, 2:height, 3:width}`, выход `{0:batch, 2:anchors}`; метаданные (`stride`, `names`, `task`, `imgsz`, `end2end` и др.) пишутся отдельно (exporter L984–1000). Основание: source_code. Статус: прочитан; фактический экспорт сделан W1-10 (opset 18 при torch 2.14.1, один вход `images`, один выход `output0`).
- **W1-06-F27** — Предобработка вне графа (`engine/predictor.py` L183–206): список BGR uint8 → letterbox → `permute BHWC→BCHW`, `flip(1)` BGR→RGB, `.float().div_(255)`; mean/std нет. Граф Ultralytics-ONNX начинается со свёртки (в `op_matrix`: `Div=1` — деление `/2` в `dist2bbox`, не нормализация). Основание: source_code + inference. → W1-11 (детали letterbox).
- **W1-06-F28** — Постобработка внешняя (по умолчанию): `nms.non_max_suppression` (`utils/nms.py` L1–90): вход `[B,4+nc+extra,A]` (BCN) либо end2end `[B,N,6]` (определяется `prediction.shape[-1]==6 or end2end`, L71), порог по max-классу, `xywh2xyxy`, опциональный multi-label, `max_nms=30000`, `max_wh=7680`. Основание: source_code. Статус: прочитан частично (только контракт входа) → W1-11.
- **W1-06-F29** — Замена функции активации возможна на уровне YAML: ключ `activation:` → `Conv.default_act = eval(act)` (`tasks.py` L2088, L2098–2104; при restricted-загрузке — `_SafeLoad.activation`). Позволяет собрать YOLOv8/11 с ReLU/LeakyReLU вместо SiLU, но потребует обучения с нуля или дообучения (веса COCO с SiLU не эквивалентны). Основание: source_code. Применимость к LinQ — hypothesis (требуется знать, поддерживается ли SiLU/Sigmoid·Mul).
- **W1-06-F30** — Форма входа/кратность: `DetectionModel.__init__` определяет `stride` прогоном `zeros(1,ch,256,256)` в режиме training (`tasks.py` L534–552), `bias_init()` вызывается один раз; экспорт использует `check_imgsz(imgsz, stride=model.stride, min_dim=2)` → размеры кратны 32 (W1-10: 384×640 прошёл → `[1,84,5040]`). Прямоугольный вход допустим, но число якорей меняется; `max_det` в экспорте ограничивается `available` (L944–948).

### 1.3 YOLOv5 (оригинал) и YOLOv5u

- **W1-06-F40** — `yolov5/models/yolo.py` `Detect` @ af08ba1 L71–128: **anchor-based**, `no = nc+5`, `na = 3`, `m[i] = Conv2d(ch_i, no·na, 1)`. Forward: `x[i].view(bs,na,no,ny,nx).permute(0,1,3,4,2)`; в eval **sigmoid применяется ко всем каналам** (`x[i].sigmoid().split((2,2,nc+1),4)`), `xy = (xy·2 + grid)·stride`, где `grid = idx − 0.5` (L126) ⇒ `(2σ − 0.5 + idx)·stride`; `wh = (wh·2)²·anchor_grid` (anchor_grid = `anchors·stride`, пиксели); `y = cat(xy, wh, conf[obj+nc])`, `view(bs, na·nx·ny, no)`; уровни склеиваются по оси 1. Возврат: train → список `x`; eval → `(cat(z,1), x)`; export → `(cat(z,1),)` (кортеж из одного тензора). Выход `[B, 25200, 85]` при 640×640, nc=80 (3·(6400+1600+400)); порядок внутри уровня: якорь → y → x. Основание: source_code. Статус: прочитан; фактический экспорт оригинального yolov5 никем не выполнялся (W1-10 экспортировал `yolov5nu/yolov5su`, не `yolov5s.pt`).
- **W1-06-F41** — Якоря: yaml `anchors` в пикселях (P3 `[10,13,16,30,33,23]`, P4 `[30,61,62,45,59,119]`, P5 `[116,90,156,198,373,326]`), в `DetectionModel.__init__` (L242–256) `m.stride` из прогона 256, `check_anchor_order(m)`, `m.anchors /= m.stride.view(-1,1,1)` (в клетках). Объекты `anchors` — buffer ⇒ сохраняются в `state_dict`/`.pt`. Основание: source_code (HEAD L242–256; v7.0 L196–197).
- **W1-06-F42** — Оценка класса при NMS: `x[:, 5:] *= x[:, 4:5]  # conf = obj_conf * cls_conf` (`utils/general.py` L719) — умножение objectness × cls делается **вне сети**. Основание: source_code @ af08ba1. → W1-11.
- **W1-06-F43** — Архитектура `yolov5s.yaml` (v6.0-стиль): `Conv(6×6, s=2, p=2)` вместо Focus, `C3`, `SPPF`, `nn.Upsample(nearest)`, SiLU; в `models/common.py` `SPPF.cv1 = Conv(c1,c_,1,1)` **с активацией** (L329), тогда как в ultralytics `SPPF.cv1(..., act=False)` (F19) — разный граф при одинаковом названии. Основание: source_code. Статус: прочитан.
- **W1-06-F44** — Экспорт yolov5: `export.py` `run()` ставит `m.inplace, m.dynamic, m.export = …` для `Detect` (L1405–1411), модель грузится с `fuse=True` (L1392), `export_onnx` использует `torch2onnx` **из пакета ultralytics** (`from ultralytics.utils.export import torch2onnx`, L327), имена `images`/`output0`, `dynamic_axes` по батчу/высоте/ширине (`output0`: batch, anchors), `onnxslim` по умолчанию; **оpset: CLI default 17 (L1524), значение по умолчанию функции `run()` — 12 (L1302)**. Основание: source_code. Статус: прочитан, не запускался. Оговорка: расхождение дефолтов зависит от способа вызова.
- **W1-06-F45** — YOLOv5u в ultralytics (`cfg/models/v5/yolov5.yaml`): backbone/neck как у yolov5 (Conv 6×6, C3, SPPF), но голова — `Detect, [nc]` ultralytics (anchor-free, DFL reg_max=16, cls-ветка legacy Conv3-Conv3 — C3k2 в yaml нет), без objectness. W1-10 локально: `yolov5nu_default` и `yolov5su_default` → `output0 [1,84,8400]`, 262 узла, Softmax 1. **Это иной контракт и иные веса, чем у `yolov5s.pt` из `ultralytics/yolov5`.** Основание: source_code + чужое local_observation.

### 1.4 YOLOX

- **W1-06-F50** — `YOLOXHead` (`yolox/models/yolo_head.py` @ 6ddff48): на каждом уровне `stem` (1×1, `256·width` каналов) → ветки `cls_convs` (2×3×3) и `reg_convs` (2×3×3) → `cls_preds` (nc), `reg_preds` (4), `obj_preds` (1; от reg-признаков); стрейды 8/16/32. Eval-ветка (L186–213): на уровне `cat([reg_output, obj_output.sigmoid(), cls_output.sigmoid()], 1)`, затем `flatten` и `permute` ⇒ `[B, A, 5+nc]` с порядком каналов `[dx,dy,dw,dh, obj, cls…]`; **при `decode_in_inference=True`** `decode_outputs` (L235–253): `(xy+grid)·stride`, `exp(wh)·stride`, остальное без изменений ⇒ `cx,cy,w,h` в пикселях. Основание: source_code. Статус: прочитан.
- **W1-06-F51** — Экспорт YOLOX (`tools/export_onnx.py`): `--decode_in_inference` — `store_true` (L53–56, default False) и присваивается `model.head.decode_in_inference = args.decode_in_inference` (L86) ⇒ **ONNX по умолчанию без decode** (raw `reg` + sigmoid(obj) + sigmoid(cls)); классовое умолчание `True` (yolo_head.py L36, комментарий «for deploy, set to False»). Прочее: opset default **11** (L29), `torch.onnx._export`, `replace_module(model, nn.SiLU, SiLU)` (SiLU → `x·sigmoid(x)`, L85), `dummy_input = randn(batch,3,*exp.test_size)`, динамические оси только `batch` (L96), `onnxsim` по умолчанию (отключается `--no-onnxsim`), ключи `--input images`, `--output output`. `test_size` по умолчанию (640,640), у `yolox_nano`/`yolox_tiny` — (416,416) (`exps/default/*.py`). Основание: source_code. Статус: прочитан, не запускался. Следствие: внешний код при экспорте по умолчанию обязан повторить `grid`/`stride`/`exp` (порядок: уровни 8,16,32; внутри уровня y-major, x-minor; A = 8400 при 640).
- **W1-06-F52** — Backbone/neck YOLOX: `CSPDarknet` со стемом **`Focus`** (`network_blocks.py` L188–210: четыре среза `x[..., ::2, ::2]`, `[..., 1::2, ::2]`, `[..., ::2, 1::2]`, `[..., 1::2, 1::2]` → `cat` → `BaseConv`), `SPPBottleneck` с параллельными MaxPool k=5/9/13 (L122–144), `YOLOPAFPN` с `nn.Upsample(scale_factor=2, mode="nearest")` (`yolo_pafpn.py` L32), активация SiLU по умолчанию (`yolox_base.py` L28), depthwise-варианты у nano. Attention и DFL нет. Основание: source_code.
- **W1-06-F53** — Предобработка YOLOX: `ValTransform` (`data/data_augment.py` L213–243) при `legacy=False`: `preproc` — letterbox с паддингом **114 в левом верхнем углу** (`padded_img[:h*r,:w*r] = resized`), `cv2.INTER_LINEAR`, **BGR→CHW float32 без /255 и без mean/std** (диапазон 0..255); `legacy=True` — RGB, /255, ImageNet mean/std. Основание: source_code. → W1-11, linq_platform (диапазон калибровки).

### 1.5 SSD / SSDlite / TF OD API

- **W1-06-F60** — `ssdlite320_mobilenet_v3_large` (torchvision 0.29.1; `ssdlite.py` L~255–331): вход `list[Tensor[3,H,W]]` float 0..1; **ресайз до фиксированных 320×320 и нормализация mean=std=0.5 выполняются внутри `forward`** (`GeneralizedRCNNTransform(min, max, mean, std, size_divisible=1, fixed_size=size)`; `ssd.py` L233; defaults `image_mean=[.5]*3`, `image_std=[.5]*3`, ssdlite.py L315–316) ⇒ эффективный диапазон входа [−1,1]. Backbone `mobilenet_v3_large` (Hardswish, `SqueezeExcitation` с `Hardsigmoid`, `AdaptiveAvgPool2d`, ReLU), 6 карт признаков (C4-expansion + последний блок + 4 extra-блока с depthwise stride-2 и ReLU6); голова `SSDLiteHead`: на каждую карту depthwise 3×3 (+BN+ReLU6) → 1×1 для `cls_logits` (num_classes·anchors) и для `bbox_regression` (4·anchors). `num_classes=91` (COCO-индексация с фоном `0`), 6 якорей на ячейку (`DefaultBoxGenerator([[2,3]]*6, min_ratio=.2, max_ratio=.95)`: 2 квадратных + 2·len(ratios)). Основание: source_code. Статус: прочитан, не запускался.
- **W1-06-F61** — Выход и постобработка SSD: `SSDScoringHead.forward` (`ssd.py` L~91–104): для каждой карты `view(N,-1,K,H,W).permute(0,3,4,1,2).reshape(N,-1,K)` и `cat` по оси 1 ⇒ **`bbox_regression [N, A, 4]`, `cls_logits [N, A, 91]`**. `postprocess_detections` (L414–460): `softmax(cls_logits, -1)`, `BoxCoder(weights=(10,10,5,5)).decode_single(boxes, anchors)` (`_utils.py` L183–215: `dx/wx`, `dy/wy`, `dw/ww`, `dh/wh`, `exp` с `clamp(max=log(1000/16))`), `clip_boxes_to_image`, цикл по классам `1..C−1` (порог `score_thresh=0.001`, top-300), `batched_nms(iou 0.55)`, не более 300 детекций; боксы **xyxy в пикселях исходного изображения** (после `transform.postprocess`). Т.е. вся постобработка — Python-циклы с динамическими формами, напрямую в ONNX дающие `Loop/NonMaxSuppression/NonZero…`; осмысленный граф для ускорителя — только «ядро» backbone+head. Основание: source_code. Количество якорей A: **inference** — размеры карт при 320 вход: 20,10,5,3,2,1 (stride16-C4, затем stride-2 экстры) ⇒ `6·(400+100+25+9+4+1) = 3234`; расчёт не проверен прогоном (скрипт `ssdlite_export.py` у W1-10 есть, вывод не сохранён).
- **W1-06-F62** — TF OD API `ssd_mobilenet_v2_coco.config` (tensorflow/models @ `a088bcc4…`, 2026-10-22): `fixed_shape_resizer 300×300`, `num_layers 6`, `min_scale 0.2`, `max_scale 0.95`, `aspect_ratios 1, 2, 0.5, 3, 0.3333`, `box_coder` scales 10/10/5/5, активация `RELU_6`, `score_converter: SIGMOID`, post-NMS `score_threshold 1e-8`, `iou_threshold 0.6`, `max_detections_per_class 100`. `SSDMobileNetV2FeatureExtractor.preprocess` = `(2/255)·x − 1` (`models/ssd_mobilenet_v2_feature_extractor.py` L93); признаки с `layer_15/expansion_output`, `layer_19`, extra-глубины `[-1,-1,512,256,256,128]` (L110–112); `SSDMetaArch.postprocess` декодирует по якорям, применяет `score_conversion_fn` и срезает фон (`ssd_meta_arch.py` L718–735). Основание: source_code/config. Статус: прочитаны фрагменты, не запускалось. Оговорка: **что именно LinQ называет `ssd_mobilenet_v2` (TF OD API v1 zoo, MLPerf-вариант, иное) — unknown**; веса и `frozen_inference_graph.pb` — зона W1-03/W1-01-F28. Число якорей 1917 для 300×300 (19²·3 + (10²+5²+3²+2²+1²)·6) — вывод из конфигурации, не проверено.

### 1.6 PP-YOLOE+ / PicoDet (кратко)

- **W1-06-F70** — `PPYOLOEHead.forward_eval` (PaddleDetection @ `b25522a0f4bde8c80603f3ba5e3472059972e3b5`, `ppdet/modeling/heads/ppyoloe_head.py` L236–271): на каждом уровне `avg_feat = adaptive_avg_pool2d(feat,(1,1))`, ESE-attention `feat·sigmoid(fc(avg))`, затем `pred_cls` / `pred_reg`; `reg_dist` reshape `[-1,4,reg_channels,l]` (reg_channels=17 при `reg_max=16`), softmax по бинам, `proj_conv` 1×1; `cls_score = sigmoid(logit)`. `post_process` (L532–553): `batch_distance2bbox` (xyxy) × stride; при `exclude_post_process=True` выдаётся `concat([bbox, scores.transpose])` `[B,A,4+nc]` в пикселях входа; иначе деление на `scale_factor` и `MultiClassNMS` (конфиг `ppyoloe_plus_crn.yml`: `nms_top_k 1000, keep_top_k 300, score_threshold 0.01, nms_threshold 0.7`), `fpn_strides: [32,16,8]` (порядок от крупного шага к мелкому). Препроцесс eval (`ppyoloe_plus_reader.yml`): `Resize keep_ratio False` (растяжение без паддинга), `NormalizeImage mean 0 std 1 norm_type none`, `Permute`. Основание: source_code/config. Статус: прочитан частично. Оговорка: фактический эффект `NormalizeImage(is_scale)` (деление на 255) не проверялся; экспорт — через `tools/export_model.py` + `paddle2onnx` (отдельный конвертер, не проверялся).
- **W1-06-F71** — PicoDet: по README (`configs/picodet/README.md`) есть варианты «w/ post-process» и «w/o post-process» (`-o export.post_process=False`, `-o export.nms=False`), для ONNX рекомендован экспорт без NMS (много сценариев ONNX поддерживают лишь один вход и фиксированные формы выхода). Код головы не читался ⇒ контракт выхода **не установлен**.

### 1.7 Чужие (соседние) наблюдения, на которые опираюсь

- **W1-06-F80** — W1-10 (локальные экспорты, ultralytics 8.4.184, torch 2.14.1+cpu, onnx 1.23.2, opset 18): yolov8n/yolo11n/yolo26n/yolov5nu/yolov5su по умолчанию `output0 [1,84,8400]`; `nms=True` → `[1,300,6]`; `yolo26n_e2e` → `[1,300,6]`; raw-срезы `rawhead_*` дают раздельные выходы `box_s8 [1,64,80,80]`, `box_s16 [1,64,40,40]`, `box_s32 [1,64,20,20]`, `cls_s8 [1,80,80,80]`… (у yolo26n box-каналов 4). Источник: `W1-10_files\op_matrix.md`, `rawhead_*.json`, `head_traces\*.txt`. Я считаю это чужим local_observation (не перепроверял).
- **W1-06-F81** — W1-12 (reported_measurement вендора): в презентации LinQ (`2026_linq_presentation.pdf`, стр. 4) для HP batch 1 указаны `yolo5s`, `yolov8n_pose`, `ssd_mobilenet_v2`, размер входа/decode/NMS не указаны; в публичном руководстве IVA H1 «протестированы» tiny_yolo2/3, yolo2/3, yolo5s. Значит, **семейство YOLOv8 (C2f+DFL, Pose-голова) вендорски заявлено**, YOLO11 (attention) — только строка на сайте. Это ссылки на W1-01/W1-12, я их не проверял.

---

## 2. Источники

- **W1-06-S01** — `ultralytics/ultralytics`, GitHub, AGPL-3.0 (лицензия репозитория; лицензия весов/данных не проверялась, → W1-04). Тег `v8.4.184` = `f7dd275e5853801674ca78ef51896617bb5362ba` (release 2026-10-22), `main` = `e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8`. Клон `<SCRATCH>\repos\W1-06\ultralytics\` (depth 1, HEAD e6d5fc59 + тег). Проверено 2026-10-23 04:45–05:20 MSK. Файлы: `ultralytics/nn/modules/head.py`, `block.py`, `conv.py`, `ultralytics/nn/tasks.py`, `ultralytics/utils/tal.py`, `ultralytics/utils/nms.py`, `ultralytics/utils/export/engine.py`, `ultralytics/engine/exporter.py`, `predictor.py`, `validator.py`, `ultralytics/cfg/default.yaml`, `cfg/models/{v8,11,26,v5}/*.yaml`. Тип: source_code. Доступ: полный. PyPI `ultralytics 8.4.184` совпадает.
- **W1-06-S02** — `ultralytics/ultralytics` тег `v8.3.0` = `6e43d1e1e5db72afbf686dee6745669bcb124b0a`: `nn/modules/head.py`, `block.py` (через `gh api`, сохранены как `<SCRATCH>\repos\W1-06\old_head_8.3.0.py`, `old_block_8.3.0.py`). 2026-10-23 ~04:50.
- **W1-06-S03** — `ultralytics/ultralytics` теги `v8.4.100`, `v8.4.130/135/140/145/150/165/175/180` — `cfg/default.yaml` и `head.py`/`exporter.py` (v8.4.100, v8.4.140, v8.4.145) через `gh api`. SHA тегов: v8.4.140 `d1c644a6085045ae18dfaecf1b2c10efedaa080b`, v8.4.145 `7866d1217d3f77f4695c07084f09e33c3cb4bc74`. 2026-10-23 ~05:05.
- **W1-06-S04** — Коммит `899fb0495e2ad05a6a1b0a34909e25e0a8f6b032` (2024-10-19, «Backward compatibility support for legacy models (#17010)»), прочитан через blobless-клон истории `<SCRATCH>\repos\W1-06\ultralytics_hist\` (`git show`, `git describe --contains` → `v8.3.17~1`). 2026-10-23 ~05:00.
- **W1-06-S05** — `ultralytics/yolov5`, AGPL-3.0 (репозиторий; ранее GPL-3.0 в v7.0 заголовках — различие лицензий между v7.0 и HEAD замечено по заголовкам файлов: `# YOLOv5 🚀 by Ultralytics, GPL-3.0 license` в v7.0 против `AGPL-3.0` в HEAD, → W1-04). HEAD `af08ba156fd58ed5b0fe7e4e58a22c72c3cdd0ce` (2026-10-21), `v7.0` = `915bbf294bb74c859f0b41f1c23bc395014ea679`. Клон `<SCRATCH>\repos\W1-06\yolov5\`. Файлы: `models/yolo.py`, `models/common.py`, `models/yolov5s.yaml`, `export.py`, `utils/general.py`.
- **W1-06-S06** — `Megvii-BaseDetection/YOLOX`, HEAD `6ddff4824372906469a7fae2dc3206c7aa4bbaee` (2025-06-08), release `0.3.0` (2022-04-22). Клон `<SCRATCH>\repos\W1-06\YOLOX\` (при клонировании на Windows не создался один файл `demo/ncnn/android/.../yoloXncnn.java` из-за длины пути — к делу не относится; рабочее дерево чистое). Файлы: `yolox/models/{yolo_head,yolox,network_blocks,darknet,yolo_pafpn}.py`, `yolox/data/data_augment.py`, `yolox/exp/yolox_base.py`, `exps/default/*.py`, `tools/export_onnx.py`. Лицензия не проверялась (→ W1-04).
- **W1-06-S07** — `pytorch/vision` v0.29.1 = `1f1a920d685d46dfbe187934b785b7ecb7a182f2`; клон depth 1 (HEAD `c725e823…`, файлы detection без различий). Файлы: `torchvision/models/detection/{ssd,ssdlite,anchor_utils,_utils}.py`, `torchvision/models/mobilenetv3.py`. BSD-3 (по W1-02; сам не проверял).
- **W1-06-S08** — `PaddlePaddle/PaddleDetection` HEAD `b25522a0f4bde8c80603f3ba5e3472059972e3b5` (2026-03-16), release v2.9.0 (2026-03-19); `ppdet/modeling/heads/ppyoloe_head.py`, `configs/ppyoloe/_base_/ppyoloe_plus_crn.yml`, `ppyoloe_plus_reader.yml`, `configs/picodet/README.md` — через `gh api` (файл головы сохранён `<SCRATCH>\repos\W1-06\ppyoloe_head.py`).
- **W1-06-S09** — `tensorflow/models` master `a088bcc473f77e8a1b7b38bbfa4ebd4f6313a127` (2026-10-22): `research/object_detection/samples/configs/ssd_mobilenet_v2_coco.config`, `models/ssd_mobilenet_v2_feature_extractor.py`, `meta_architectures/ssd_meta_arch.py` (через `gh api`).
- **W1-06-S10** — Соседний файл W1-10: `ROOT\_WORK\WAVE1\W1-10_EXPORT_ONNX.md`, `W1-10_files\{op_matrix.md,rawhead_*.json,head_traces\*.txt,inventory\*.json}` (прочитаны 2026-10-23 ~05:00; файл W1-10 на тот момент не завершён). Чужое local_observation.
- **W1-06-S11** — Соседние файлы W1-01 (`W1-01_FAMILIES.md`), W1-12 (`W1-12_QUANT_LINQ.md`), W1-11 (`W1-11_PRE_POST.md`, прочитана шапка с FLASH), FLASH от оркестратора (источник W1-03). Использовал только для связки; не перепроверял.

---

## 3. Карточки контрактов («вход → выход»)

Обозначения: B — батч, H×W — вход (кратен 32), A — число якорных точек, nc — число классов. «граф» = то, что остаётся внутри ONNX при экспорте по умолчанию соответствующего инструмента.

### 3.1 Ultralytics YOLOv8 detect (`yolov8*.yaml` / `yolov8n.pt`), @ v8.4.184

| | |
|---|---|
| Вход | `float32 [B,3,H,W]`, RGB, 0..1 (делится на 255 предиктором, F27); letterbox снаружи |
| Backbone/neck | Conv(3×3, s=2)…, `C2f`, `SPPF`, `Upsample nearest ×2`, `Concat`, PAN; всё SiLU; 3 уровня P3/P4/P5 (8/16/32) |
| Голова | per level: box `Conv3→Conv3→Conv1(4·16)`; cls (legacy) `Conv3→Conv3→Conv1(nc)`; `c2=max(16,ch0//4,64)=64`, `c3=max(ch0,min(nc,100))` (для n: 80 при nc=80) |
| train | `dict{"boxes":[B,64,A],"scores":[B,nc,A],"feats":[3]}` (v8.4.184); список из 3 тензоров `[B,64+nc,h,w]` (v8.3.0) |
| eval (predict) | `(y [B,4+nc,A], preds)` (внутри Ultralytics после `fuse()`) |
| export (по умолчанию) | `output0 [B,4+nc,A]`, строки 0–3 = `cx,cy,w,h` в пикселях входа, строки 4.. = sigmoid-вероятности классов; A=8400 при 640² (наблюдалось W1-10: `[1,84,8400]`) |
| Внутри графа | DFL (Reshape/Transpose/Softmax/Conv1×1), anchors/stride (константы при `dynamic=False`, гипотеза/косвенно), `dist2bbox` (Sub/Add/Div2/Concat), `×stride`, Sigmoid классов, Concat по оси 1 |
| Снаружи | /255, RGB, letterbox, обратное преобразование координат, фильтр по порогу, NMS (по умолчанию внешний), имена классов (`metadata_props["names"]`) |
| Расхождение с «ожиданием» внешнего кода | внешний код, ожидающий `[B,A,5+nc]` (YOLOv5/YOLOX) или нормированные координаты, не совместим: транспонирование осей и отсутствие objectness; координаты в пикселях входа, не в [0,1] |

### 3.2 Ultralytics YOLO11 detect (`yolo11*.yaml`)

То же, что 3.1 по контракту выхода (reg_max=16, `[B,4+nc,A]`), но: backbone/neck — `C3k2` (подкласс `C2f`; `Split` при экспорте), `C2PSA` на P5 с `Attention` (F20); cls-ветка головы depthwise (`legacy=False`, F11): `DWConv3→Conv1→DWConv3→Conv1→Conv1(nc)`, `c3 = max(ch0, min(nc,100))`. ONNX yolo11n: 320 узлов, 88 Conv, Split 10, Softmax 2, MatMul 2, Transpose 3, MaxPool 3, Resize 2 (W1-10). Размерность attention-блока зависит от H·W через N=(H/32)(W/32) (при 640² N=400).

### 3.3 Ultralytics YOLO26 detect (`yolo26*.yaml`), @ v8.4.184

| | |
|---|---|
| Структура | как YOLO11 + SPPF-shortcut + `C3k2(attn=True)` в P5 neck; `reg_max=1` (нет DFL), две пары голов `cv2/cv3` и `one2one_cv2/cv3` (F21, F22) |
| train | `{"one2many":{boxes[B,4,A],scores[B,nc,A],feats}, "one2one":{…}}`; one-to-one питается `detach()`-признаками (backbone её градиенты не получает) |
| eval/predict/export по умолчанию (`nms=None`) | **one-to-many**, `[B,4+nc,A]`, `cx,cy,w,h` px (формат как YOLO11), внешний NMS; ONNX 368 узлов, `[1,84,8400]` (W1-10) |
| `nms=False` (NMS-free) | one-to-one голова, `xyxy`, внутри графа `ReduceMax`, `TopK`×2, `GatherElements`×3, `Mod`, `Cast`, `Flatten`, `Expand`, `Unsqueeze`; выход `[B, min(300,A), 6]` = `[x1,y1,x2,y2,score,class_idx]` (class как float; W1-10: 384 узла, `[1,300,6]`) |
| `nms=True` | встроенный NMS, `[1,300,6]` (418 узлов; NonMaxSuppression, NonZero, ScatterND…) |
| Примечание | `fuse()` удаляет неиспользуемую ветку, поэтому *после* экспорта переключить режим нельзя: режим фиксируется при экспорте |
| Версионная оговорка | в v8.4.0–v8.4.140 дефолт был NMS-free (FLASH-1) |

### 3.4 YOLOv5 (оригинал `ultralytics/yolov5`) — `yolov5s.pt`

Вход `float32 [B,3,H,W]` RGB 0..1 (по `detect.py`, не перепроверялось в этом прогоне — сеть сама нормализации не делает: `forward` без деления); выход (export) — кортеж `([B, 3·ΣHW/s², 5+nc],)`: `[cx,cy,w,h (px), obj, cls…]` — всё после sigmoid; декодирование (F40) — в графе: `Sigmoid`, `Mul 2`, `Add grid`, `Mul stride`, `Pow 2` (в ONNX `Mul`/`Pow`) `Mul anchor_grid`. Внешний NMS: `conf = obj·cls` (F42). Это **единственный** кандидат с objectness и anchor-based декодом; квантование выхода требует внимания к диапазону (координаты — сотни, вероятности 0..1).

### 3.5 Ultralytics YOLOv5u (`yolov5nu/su.pt`, `yolov5.yaml` в ultralytics)

Контракт как у YOLOv8 (3.1): `[B,4+nc,8400]`, DFL, нет objectness; backbone yolov5 (C3, SPPF с `act=False` в cv1). Подтверждено W1-10 (`[1,84,8400]`, Softmax 1).

### 3.6 YOLOX (`yolox_s` и др.)

Вход `float32 [B,3,H,W]` BGR 0..255 (F53); выход при экспорте по умолчанию `output [B,A,5+nc]` — `[dx,dy,dw,dh (сырые), obj(σ), cls(σ)…]` (F50, F51); при `--decode_in_inference` — `cx,cy,w,h` px. Опции: opset 11, динамика только по батчу. Внешний код при дефолтном экспорте обязан: построить grid/stride, `(dxy+grid)·stride`, `exp(dwh)·stride`, затем `score = obj·cls` и NMS (в `yolox/utils/boxes.py` `postprocess` — не читал, → W1-11).

### 3.7 SSDlite320-MobileNetV3 (torchvision)

Полная модель: вход `list[Tensor[3,H,W]]` 0..1; внутри resize 320² + (x−0.5)/0.5; выход после NMS — словари `boxes (xyxy, px исходного кадра), scores, labels (1..90)`. «Ядро» для ускорителя: backbone+head → `bbox_regression [N,A,4]` (кодированные смещения, веса 10/10/5/5), `cls_logits [N,A,91]` (логиты, фон = индекс 0); якоря `DefaultBoxGenerator` — вне графа (константы, нормированные [0,1] → умножаются на размер изображения при `anchor_generator`); softmax/decode/NMS снаружи.

### 3.8 TF OD API ssd_mobilenet_v2 (300×300)

Вход `NHWC float (2/255)x−1` (F62); выход ядра: `box_encodings [B,A,1,4]` и `class_predictions_with_background [B,A,C+1]` (по `ssd_meta_arch.predict`; форму `[B,A,1,4]` из памяти не подтверждал по этому прогону — требует проверки по `predict`); декодирование по якорям, sigmoid и NMS в `postprocess` (внутри `frozen_inference_graph.pb`, но как отдельные TF-операции NMS). Соответствие названию на сайте LinQ — unknown.

### 3.9 PP-YOLOE+ (кратко)

F70: `cls_score [B,nc,A]` sigmoid, `reg_dist [B,A,4]` (после softmax+proj, в клетках), `anchor_points [A,2]`, `stride_tensor [A,1]`, порядок уровней 32→16→8; пост-процесс `distance2bbox × stride` (xyxy). С `exclude_post_process`: `[B,A,4+nc]` px. Препроцесс — stretch-resize.

---

## 4. Режимы train / eval / export — сводная таблица различий

| Семейство | train() | eval() (не export) | export-флаг/экспорт | fuse |
|---|---|---|---|---|
| Ultralytics v8/11 @8.4.184 | dict `boxes/scores/feats` (A-оси слиты) | `(y, dict)` с декодом | один тензор `y`; `Detect.export=True, .format, .dynamic, .max_det, .xyxy, .shape=None`; `C2f.forward→forward_split` | BN→Conv; удаляет неиспользуемую ветку |
| Ultralytics v8.3.0 | список из 3 `[B,64+nc,h,w]` | `(y, x)` | `y`; для `tflite/edgetpu` нормировка по размеру сетки внутри `_inference` (код v8.3.0, отсутствует в 8.4.184: в новой редакции форматные ветки `tflite` не в `Detect`) | то же |
| Ultralytics YOLO26 | `{"one2many","one2one"}` | зависит от `end2end` (по умолчанию в 8.4.184 one-to-many) | `nms`-ветвление, TopK-постобработка при `nms=False` | удаляет `cv2/cv3` либо `one2one_*` |
| yolov5 repo | список `x[i]` `[B,3,ny,nx,no]` (сырые) | `(cat(z), x)` с декодом и sigmoid | `(cat(z),)`; `.inplace/.dynamic/.export` | BN→Conv |
| YOLOX | loss-словарь (метки обязательны!) | `[B,A,5+nc]` декод зависит от `decode_in_inference` (класс: True) | `export_onnx.py` ставит `decode_in_inference=False` по умолчанию; SiLU→`x·sigmoid(x)`; BN сливается onnxsim (не проверялось) | `fuse_model` — отдельная функция (не вызывается `export_onnx.py`) |
| torchvision SSD | `losses` dict (нужны targets) | список словарей после NMS | `torch.onnx.export` полной модели → `Loop/NMS…`; «ядро» нужно выделять вручную | нет `fuse` (BN остаётся, сливается при экспорте) |
| PP-YOLOE+ | `forward_train` | `forward_eval` + `post_process` | `exclude_post_process/exclude_nms` флаги | RepVGG-блоки перепараметризуются при export (не читал) |

Примечание по таблице: пункт «BN сливается onnxsim/torch.onnx» для YOLOX и SSD — **hypothesis** (стандартное поведение конвертера в eval-режиме), экспортом не проверялся.

---

## 5. Значимые для компилятора операции по месту в графе (Ultralytics/YOLOX/YOLOv5; SSD/PP-YOLOE — кратко)

Колонка «статус для LinQ» везде **unknown**, пока linq_platform не даст список операторов; ниже — только «что потенциально требует проверки».

| Место | Операция | Где встречается | Что проверить на LinQ |
|---|---|---|---|
| Все свёртки | Conv 1×1, 3×3, stride 2; depthwise 3×3 (cls-ветка YOLO11/26, `Attention.pe`, SSDlite, MobileNet); Conv+BN сливается | все | depthwise, группы, нечётные формы (80×80, 40×40, 20×20) |
| Активации | SiLU = `Sigmoid`+`Mul` (YOLOv5/8/11/26, YOLOX); ReLU6/Hardswish/Hardsigmoid (SSDlite, MobileNetV3); LeakyReLU у YOLOv3/tiny; swish у PP-YOLOE | почти все | поддержка Sigmoid/Mul в int8, точность таблиц, fusion |
| C2f/C3k2 | `Split` (axis 1, равные части), `Concat`, `Add` | v8/11/26 | Split (не Slice), N-арный Concat |
| SPPF | `MaxPool` k=5 s=1 p=2 ×3 | v5/8/11/26 | MaxPool 5×5 stride 1 с padding; YOLOX — 5/9/13 параллельно |
| Neck | `Resize` nearest ×2 (opset 18) / `Upsample` (opset 9) | все | режим nearest, коэффициент 2, форма из констант |
| Focus-стем | 4 strided `Slice` + `Concat` | все YOLOX на `CSPDarknet` (`darknet.py` L115), включая tiny/nano | Slice со stride 2 |
| Attention (C2PSA, C3k2-attn) | `Reshape`, `Split` (q,k,v), `Transpose`, `MatMul` (act×act), `Mul` (scale), `Softmax(-1)`, depthwise Conv | yolo11, yolo26 | MatMul двух активаций, Softmax по 400 токенам, квантование внимания |
| Голова (до decode) | per-level Conv-цепочки; `Reshape [B,C,-1]`; `Concat` по оси HW | v8/11/26 | Reshape с -1, Concat по последней оси |
| DFL | `Reshape(B,4,16,A)`, `Transpose`, `Softmax(axis 1)`, Conv 1×1 с фиксированными весами | v5u/v8/v11/PP-YOLOE | Softmax в int8, фиксированные веса `0..15` |
| Decode | `Sub`, `Add`, `Div 2`, `Concat`, `Mul stride`, `Sigmoid` | Ultralytics | смесь пиксельных координат и 0..1 в одном выходе (F14, W1-11 FLASH-3) |
| YOLOv5 decode | `Sigmoid`, `Mul 2`, `Add`, `Mul`, степень 2, `Mul anchor_grid`, `Reshape/Transpose` из 5D | yolov5 | 5D-тензоры `[B,3,ny,nx,no]` |
| YOLOX decode | `Add grid`, `Exp`, `Mul stride` | YOLOX (опционально) | `Exp` |
| NMS-free (YOLO26 `nms=False`) | `ReduceMax`, `TopK`, `GatherElements`, `Mod`, `Cast`, `Expand`, `Flatten` | yolo26 e2e | вероятно вне ускорителя — выносить на CPU |
| Встроенный NMS (`nms=True`) | `NonMaxSuppression`, `NonZero`, `ScatterND`, `GatherND`, `Where` | все Ultralytics | не отдавать на LinQ; использовать только как «граф для CPU» |
| Динамический экспорт | `Shape`, `Gather`, `Range`, `ConstantOfShape`, `Expand`, `Unsqueeze` (yolo11n_dynamic: 419 узлов vs 320) | при `dynamic=True` | избегать; статическая форма |
| SSD-ядро | depthwise+pointwise, extra-блоки stride 2, `Reshape/Permute` в `[N,A,K]`, `Concat` по оси 1 | ssdlite | Reshape 5D→3D |

---

## 6. Разборы

### 6.1 Где резать граф и что тогда обязан повторить внешний код

Три варианта «границы между LinQ и CPU» (разделение — **inference**, готовность LinQ — unknown):

**(a) Вся сеть внутри (дефолтный Ultralytics-ONNX).** Выход `[B,4+nc,A]`. Плюсы — простая интеграция, NMS на CPU. Риски: DFL-Softmax, `Sigmoid`, `Mul` на пиксельных значениях, смешение шкал (0..640 и 0..1) в одном выходе (W1-11 FLASH-3).

**(b) Срез до `Detect._inference` (W1-10 `rawhead_*`).** Выходы: `box_s8/16/32 [B,4·reg_max,h,w]` (сырые DFL-логиты; у YOLO26 — 4 канала ltrb), `cls_s8/16/32 [B,nc,h,w]` (логиты до sigmoid). Внешний код обязан повторить по шагам (всё — `source_code`, F13–F16):
1. `boxes = cat(box_s*.view(B,4R,-1), -1)` (уровни в порядке 8,16,32), `scores = cat(cls_s*.view(B,nc,-1), -1)`;
2. DFL: `softmax` по 16 бинам на каждую из 4 сторон (`view(B,4,16,A)` — порядок «сторона, затем бин»), взвешенная сумма с весами `0..15` (для YOLO26 — шаг пропущен, `reg_max=1`);
3. якорные точки `(idx+0.5)` в порядке «y-major, x-minor» по уровням, `xyxy = [a−lt, a+rb]` в клетках, `×stride` → пиксели входа (`cx,cy,w,h` либо `xyxy`);
4. `scores = sigmoid(cls)`.
Только после этого — NMS. Для YOLOv5-оригинала повторяются формулы F40; для YOLOX — F50.
Эксперимент E1 предлагает численно сверить такой внешний декодер с внутренним.

**(c) Срез до голов `cv2/cv3` по частям.** Не имеет смысла (cv2/cv3 — просто свёртки).

### 6.2 Почему «yolo5s / yolo8 / yolo11» на LinQ неоднозначны

Из F40–F45: под именем «yolo5s» может стоять (i) оригинальный anchor-based `yolov5s` (`[1,25200,85]`, с objectness, 3 якоря), (ii) `yolov5su` из ultralytics (anchor-free, DFL, `[1,84,8400]`); под «yolo8» — Detect с обычной cls-веткой либо (при сборке 8.3.0–8.3.16) с depthwise-веткой, плюс Pose-вариант (`yolov8n_pose` фигурирует в измерениях вендора, F81); под «yolo11» — или полный C2PSA, или кастомная версия без него. Ни одно из этих различий не видно в публичных материалах. Требуется: список операторов/ONNX-файлов вендора (→ linq_platform).

### 6.3 Что в сетях «не как ждёт внешний код» (сводка расхождений)

- Ultralytics: нет objectness, координаты `cx,cy,w,h` (не xyxy) и пиксельные, оси `[B,C,A]` (канал-первый), а не `[B,A,C]`; при `nms=True`/`nms=False(e2e)` — `[B,300,6]` xyxy и `class_idx` float.
- yolov5-оригинал: `[B,A,5+nc]` с objectness, кортеж из одного тензора.
- YOLOX: BGR 0..255, паддинг в левый верхний угол, по умолчанию без decode.
- SSD: логиты с фоном (индекс 0; 91 класс COCO с «дырами»), кодированные смещения с весами 10/10/5/5, нормализация (x−0.5)/0.5 внутри `forward`.
- PP-YOLOE+: порядок уровней 32→16→8, stretch-resize.

### 6.4 Что даже успех чтения кода не подтверждает

Ничего из этого не доказывает: загрузку весов, успешный экспорт (кроме чужих наблюдений W1-10), корректность численной согласованности, приём компилятором LinQ, исполнение устройством, скорость и качество.

---

## 7. Противоречия

1. **YOLO26: «NMS-free по умолчанию» против «по умолчанию one-to-many».** Материалы до 8.4.140 (и многие пересказы) — первое; код 8.4.145+ и W1-10 — второе; заявление авторов, цитируемое W1-01-F12, «Prediction and validation default to the one-to-many head for accuracy» согласуется со вторым. Меняет: форму выхода (`[1,300,6]` vs `[1,84,8400]`), состав ONNX (TopK/Mod…). Разрешение: фиксировать версию ultralytics в эксперименте и явно передавать `nms=False/None` при экспорте; сверять `metadata["end2end"]`.
2. **YOLOv8 cls-ветка: Conv или DWConv.** Зависит от версии (F11, F12). Меняет: совместимость state_dict при дообучении из YAML и граф. Разрешение: загружать `.pt`; проверять наличие ключей `cv3.0.0.0.conv.weight` (DW) против `cv3.0.0.conv.weight`.
3. **Дефолт opset yolov5-экспорта:** CLI 17 vs `run()` 12 (F44) — следствие способа вызова, не ошибка.
4. **Документальный список LinQ vs код.** Сайт: yolo8/yolo11, нет «Transformer» (tech) vs «CNN/Transformer» (sol); руководство IVA H1: только yolo5s среди современных. YOLO11/26 содержит attention (F20/F21), что формально ближе к «Transformer», чем к «CNN/RNN». Меняет: выбор yolov8 против yolo11 как основной цели. Разрешение: проход конвертера (→ linq_platform).

---

## 8. Открытые вопросы

1. Какие именно реализации/размеры/входы стоят за `yolo5s`, `yolo8`, `yolo11` на LinQ? Где искал: сайт lin-q.ru (через оркестратора), W1-01/W1-12 (руководство, презентация), GitHub (нет публичных исходников вендора). Закрыть: полный кейс, SDK, вопрос организаторам.
2. Принимает ли `onnx_to_tf`/компилятор LinQ: `Split`, `MaxPool 5×5 s1`, `Resize nearest`, `MatMul` act×act, `Softmax`, `Transpose`, `Sigmoid·Mul`, depthwise Conv, 5D-тензоры (YOLOv5)? Закрыть: SDK/конвертер, пробный прогон реальных ONNX (→ linq_platform, E6).
3. Статичны ли якоря/strides в ONNX дефолтного экспорта (константы)? Закрыть: W1-10-граф: поиск `Range/Shape` (косвенно да — F15); прямой ответ — инспекция initializer'ов.
4. Точная форма выходов TF OD `ssd_mobilenet_v2` (в т.ч. `[B,A,1,4]`) — не подтверждена в этом прогоне. Закрыть: чтение `predict`/`_batch_decode` или загрузка `frozen_inference_graph.pb`.
5. Число якорей SSDlite320 (3234) — расчёт; закрыть: прогон `ssdlite_export.py` (W1-10) с печатью `[N,A,K]`.
6. Контракт PicoDet и RepVGG-перепараметризации PP-YOLOE+ — не читались.
7. Как входит `torch.onnx` слияние BN при экспорте YOLOX/SSD (hypothesis) — закрыть экспортом.
8. Лицензии весов/кода для YOLOX/PaddleDetection/torchvision-весов — не проверялись (→ W1-04).
9. Поведение `Detect` при `reg_max` ≠ 16 для нестандартных конфигов (v8-p2/p6) — не читал.

---

## 9. Предлагаемые эксперименты

Все — на CPU, в SCRATCH, версии/коммиты зафиксировать; чужие скрипты не запускать, обёртки писать самим.

- **E1. Численное соответствие внешнего декодера внутреннему (Ultralytics).** Вопрос: можно ли по raw-срезу W1-10 (`box_s*`/`cls_s*`) numpy-кодом из §6.1 воспроизвести `output0`. Кандидаты: `yolov8n.pt`, `yolo11n.pt`, `yolo26n.pt` @ ultralytics 8.4.184 (`f7dd275`), ONNX `rawhead_*` и `*_default` от W1-10. Шаги: одинаковый вход (например, `bus.jpg` с letterbox 640), ORT CPU, numpy-декодер, сравнение `max|Δ|` по боксам (px) и по классам. Измерять: max/mean abs diff, число совпавших боксов после NMS. Сохранить: json с цифрами, скрипт. Интерпретация: Δ≲1e-4 px/1e-6 — контракт подтверждён; иначе искать ошибку порядка осей (`view(B,4,16,A)`), уровней или смещения 0.5. Не подтверждает: ничего про LinQ/квантование. Остановка: совпадение или локализованное расхождение в одной операции.
- **E2. Аудит attention-подграфа.** Вопрос: размеры и количество MatMul/Softmax в yolo11{n,s,m} и yolo26{n,s} при 640² и 384×640. Шаги: по W1-10 `inventory\*.json` либо собственный разбор `onnx.load` (без запуска чужого кода). Измерять: формы входов MatMul, длину токенов N. Интерпретация: если N=400 (640²) и 2 головы (n) — входная информация для linq_platform; если в LinQ нет MatMul act×act, исключить yolo11/26 как целевую модель. Не подтверждает: влияние удаления attention на точность (нужно обучение, → W1-07).
- **E3. Сверка оригинального yolov5 против yolov5u.** Вопрос: подтверждение `[1,25200,85]` и состава ops. Кандидат: `yolov5s.pt` из официальных assets (SHA — по W1-03) + `ultralytics/yolov5@af08ba15`, `python export.py --weights yolov5s.pt --include onnx --opset 12 --imgsz 640` (команда и флаги — из `export.py` L1524, argparse; прочитано). Измерять: форма выхода, число узлов, наличие `Pow/Mul/Add` для декодирования, размер 5D-тензоров. Не подтверждает: совместимость с LinQ. Условие: weights загружать только официальные, не `torch.load` неизвестных.
- **E4. YOLOX без весов:** собрать `exp.get_model()` случайно инициализированный (без скачивания) и экспортировать с/без `decode_in_inference` для сверки форм `[1,8400,85]` и набора ops (Slice×4 в Focus). Не подтверждает: качество, лицензию.
- **E5. SSDlite core.** Запустить `W1-10_files\scripts\ssdlite_export.py` (или свой аналог) и записать `bbox_regression/cls_logits` формы (ожидание `[1,3234,4]`/`[1,3234,91]` — проверка F61).
- **E6. Проход конвертера LinQ (после 13:00 MSK).** Подать ONNX-варианты: `yolov8n` (дефолт), `yolov8n` raw-срез, `yolo11n` raw-срез, `yolov5s` оригинал, `yolox_s` (без decode). Измерять: какие операторы отвергаются. Это **единственный** эксперимент, который закрывает переходы «компилятор принимает граф», остальные — подготовительные.

---

## 10. Передачи соседям

- → linq_platform: список вопросов по операторам из §5 (особенно: `Split`, `MaxPool 5×5/s1`, `Resize nearest`, `MatMul` act×act + `Softmax(-1)` на 400 токенах, `Transpose`/`Reshape` 4D↔3D↔5D, depthwise Conv, `Sigmoid·Mul`, `Concat` по последней оси, `TopK/GatherElements/Mod`); принимает ли конвертер многовыходной граф (6 raw-выходов), статический батч; диапазоны входа (RGB 0..1 для Ultralytics, BGR 0..255 для YOLOX, (x−1)/… для SSD).
- → W1-10 (export): повторить `rawhead_*` для YOLOv5-оригинала (`[1,25200,85]`) и YOLOX (с `decode_in_inference` True/False), сохранить initializer'ы якорей; подтвердить F15 (константы).
- → W1-11 (pre/post): контракты постобработки по семействам (§3, §6.3): `conf = obj·cls` у yolov5/YOLOX; xywh vs xyxy; e2e `[B,300,6]`; SSD softmax-фон; letterbox top-left у YOLOX, stretch у PP-YOLOE; `non_max_suppression` определяет e2e по `shape[-1]==6`.
- → W1-07 / training_strategy: структура cls-ветки зависит от версии (FLASH-2); `activation:` YAML (F29); `legacy` — атрибут класса; YOLO26 обучается с двумя головами, one-to-one питается `detach()`.
- → W1-03: `*-human.pt` не загружаем публичным кодом (grep-подтверждение).
- → datasets / evaluation: имена классов хранятся в метаданных ONNX (`names`), порядок и nc определяют размер последнего Conv (`c3 = max(ch0, min(nc,100))` не зависит от nc, пока nc ≤ ch0); при смене nc меняется лишь последний 1×1 Conv.
- → video_architecture: размер входа влияет на A (`A=Σ(H/s)(W/s)`), на N у attention и на количество кандидатов NMS (8400 при 640²).
- → hackathon_strategy / operator_product: консервативная цепочка — YOLOv8 (C2f, без attention) или YOLOv5 по вендорскому списку; YOLO11/26 — только после подтверждения оператора MatMul.

## 11. Запросы эскалации

1. **Межформатная сверка контрактов** (ONNX vs Paddle vs TF для SSD/PP-YOLOE+): требует загрузки весов и конвертеров (paddle2onnx, tf2onnx), которых у меня нет; передать более сильному исследователю с моими F60–F71 как отправной точкой. Приоритет низкий для хакатона.
2. **Численная верификация внешнего декодера и выбор точек среза для int8** (E1 + квантование): объединить с W1-12; нужен выбор по распределениям сырых выходов (см. `rawhead_*.json`: диапазоны box_raw).
3. **Определение, что такое «yolo11» на LinQ** (с attention или без; какой экспорт): возможно только через SDK/организаторов; передать linq_platform.
