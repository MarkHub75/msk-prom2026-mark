# W2-B — Source-backed training/export envelopes, YOLO26s и D-FINE-M

Дата доступа **2026-10-23**. Реальные часы хоста: `2026-10-23T20:34:14.1511481+03:00`, Europe/Moscow. Реально выполнены чтение W1/CRITIC и интернет-чтение первичных requirements, API, export/training code, release notes, PyPI metadata. **Не выполнялись** install/resolve окружения, import моделей, forward/backward, training, export, ONNX/ORT execution, измерение 3090/24GB или LinQ. Веса/датасеты не скачивались, расходы отсутствуют. Материалы свежих HTTPS-чтений: `W2_B_MATERIALS/`, URL и timestamps — `fetch.json`. Чтение metadata не является скачиванием wheel или проверкой пакета.

## Решение и изменение решения W1

**W2-B-F01.** Не брать W1-13 image `torch2.14.1` как готовый общий trainer/exporter. Для первой проверяемой реализации выбрать **два изолированных model environments** с одним небольшим, согласованным core: Linux x86_64, Python **3.11.9**, Torch **2.5.1**, torchvision **0.20.1**. Train: официальные cu124 wheels; export: такие же версии CPU wheels. Проекты и их extras не смешивать в одном env. Это выбранный **compatibility envelope**, не installed lock и не доказанная комбинация. PyTorch официально публикует эту пару и индексы; Python взят из native D-FINE setup. Не требуется контейнер со всеми семействами. [S01–S04]

**W2-B-F02.** Общий floating export baseline: NumPy **1.26.4**, ONNX **1.17.0**, ORT CPU **1.20.1**; для image utilities OpenCV **4.10.0.84**. Выбор конкретных pins — **INFERRED**, существование версий/declared metadata — **DOC**, imports/parity — **UNRUN**. Python3.11 удовлетворяет metadata ONNX/transformers; ONNX требует numpy>=1.20 и protobuf>=3.20.2; ORT требует numpy>=1.21.6. ORT1.20 матрица содержит opset21/IR10, что покрывает выбранные opset16/18 по версии, но не гарантирует наличие всех kernels/численный parity. Фактический IR надо прочитать из экспортированного файла. [S08–S11]

**W2-B-F03.** YOLO export — explicit legacy `dynamo=False` внутри native wrapper; D-FINE export — небольшой зафиксированный adapter к native script, static batch1, `dynamo=False`, без simplification. D-FINE stock CLI **не даёт выключить** simplify: `store_true` вместе с `default=True`; отсутствие `--simplify` не отключает его. Этот новый факт меняет команду W1: для первого unsimplified parity нельзя просто убрать флаг. [S05–S07]

**W2-B-F04.** Conservative fallback: **Torch2.4.1 / torchvision0.19.1**, Python3.11.9, те же NumPy/ONNX/ORT и изоляция; official cu124 train / CPU export indexes. YOLO fallback export opset17, D-FINE16, legacy mode; это другой recipe ID, fresh smoke обязателен. В 2.4.1 `torch.onnx.export` действительно принимает `dynamo=False`. Не использовать Torch2.4.0 на Windows: pinned Ultralytics явно исключает эту комбинацию. Возврат к2.4.1 не является утверждением о неправильности2.14.1 или гарантией fit. [S01,S02,S12]

## K-ID: исходная критика сохранена

**K002, CRITIC.md, P0**: pinned base/digest и SHA разных проектов не образуют согласованную Python/Torch/vision/exporter/ONNX/ORT recipe; D-FINE наследует Torch exporter default, YOLO явно задаёт legacy; installed lock нельзя выдумывать. Эта критика **подтверждена**, не переписана. Статус после W2-B: **закрыто документально в части source-backed выбранных envelopes и entrypoints; runtime часть остаётся открытой**. Новые evidence: native requirements, explicit2.5.1 API, версия пары vision, D-FINE CLI-default trap, release BC changes и PyPI metadata. На сегодня ни один manifest ниже не имеет статуса `installed`/`tested`.

**K001, CRITIC.md, P0**: native Ultralytics OOM/NaN recovery может менять recipe внутри exit0; accumulation/native EMA resume не обещают lossless continuation. Статус здесь: **уточнена применимость, не закрыто этой веткой**. Сохранение того же Ultralytics SHA сохраняет проблему независимо от выбранного Torch. Передача W2-A обязательна: нельзя «закрыть» её сменой package pins. Root сообщил, что `optimizer_step`/`on_before_zero_grad` hooks stock loop не вызывает; здесь такие hooks не предлагаются как работающие. Успех установки не является доказательством immutable trial.

## Манифест A: YOLO26s baseline

Статусы: **DOC** — прямо прочитано в первичном источнике; **INFERRED** — наш выбор внутри объявленных ограничений; **UNRUN** — практическая проверка не проведена. Поле может иметь одновременно `DOC + INFERRED + UNRUN`: наличие API документировано, значение выбрано нами, исполнение неизвестно.

| Поле | Значение / статус |
|---|---|
| Source | Ultralytics SHA `de290d865035acbfa4bb24cc88960d8b52c26e45`, snapshot `8.4.184`; **DOC**, install **UNRUN**. Ставить из checkout этого SHA, не floating pip release |
| Python / OS | Linux x86_64 + Python3.11.9; project declares Python>=3.8, выбранная micro-version **INFERRED**, runtime inventory **UNRUN** |
| Train core | torch2.5.1 / torchvision0.20.1 official cu124 pair **DOC**; выбор **INFERRED**, driver/GPU/ABI/import **UNRUN** |
| Export core | Python3.11.9 + torch2.5.1 / torchvision0.20.1 CPU, NumPy1.26.4, ONNX1.17.0, ORT CPU1.20.1; pins **INFERRED**, availability/requirements частично **DOC**, исполнение **UNRUN** |
| Init | `https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt`; W1-02 metadata SHA256 `646f8bc3fe0a656803d95c294f7852321748cb29d13466a1af8862e2db384a1b`; байты и hash **UNRUN**, source asset identity передана W1-02/W2-C |
| Exposure / license | W2-C сообщает O365v1→COCO recipe и AGPL/Enterprise; **handoff**, не объявлять COCO-only или permissive. Сохранить exact W2-C source record и notices до запуска |
| Training entrypoint | `from ultralytics import YOLO; YOLO(LOCAL_INIT).train(data=LOCAL_DATA_YAML, imgsz=640, batch=B, epochs=E, optimizer="AdamW", lr0=0.0003, nbs=N, seed=0, device=0, amp=True, resume=False)`; API **DOC**, recipe values **INFERRED**, весь run **UNRUN** |
| Physical/effective batch | B/N определяет qualification; E — заранее выбранное окно после данных. Не брать auto batch и не считать B=2 проверенным fit; все эти поля до qualification **UNRUN**. Ограничить val отдельно |
| Export entrypoint | `YOLO(LOCAL_SELECTED_PT).export(format="onnx", imgsz=640, batch=1, dynamic=False, simplify=False, half=False, nms=False, opset=18, device="cpu")`; API/mode semantics **DOC**, значения **INFERRED**, artifact **UNRUN** |
| Head | `nms=False` выбирает one-to-one/e2e в этой ревизии; `images`→`output0`, ожидаемый `[B,K,6]` = xyxy/score/class. Это **DOC expected contract**, actual head/fusion/dtype/shape **UNRUN** |
| Exporter mode | native `ultralytics/utils/export/engine.py::torch2onnx`, TORCH>=2.4 передаёт `dynamo=False`; **DOC**, actual call/artifact **UNRUN** |
| Simplifier | Не устанавливать `[export-base]` ради первого несжатого графа: он затягивает onnxslim>=0.1.82. При `simplify=False` native ONNX branch требует ONNX, ORT можно поставить отдельно для comparator; **DOC/INFERRED**, run **UNRUN** |
| Recovery | native OOM/NaN path требует W2-A fail/fork policy; **UNRUN**. Смена B/N/AMP после ошибки = новый recipe/run; exit0 недостаточен |

Первый экспорт намеренно не содержит embedded NMS. One-to-one всё ещё содержит top-k/gather. Если LinQ не принимает этот путь, отдельный dense artifact с `nms=None` допустим **только при наличии one-to-many head в фактическом checkpoint**. `Detect.end2end` getter сохраняет e2e, если fusion уже удалил `cv2`: одно присваивание/флаг не восстанавливает отсутствующие веса. Dense `[B,4+C,A]` и e2e нельзя сравнивать как одну голову; нужны отдельные reference и качество. [S06,S13]

Пример будущей установки core, **не исполнен**:

```bash
# В train env A, после создания Python3.11.9 окружения:
python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu124
# В отдельном export env A:
python -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cpu
# После применения выбранных constraints к установке pinned проекта:
python -m pip install numpy==1.26.4 onnx==1.17.0 onnxruntime==1.20.1 opencv-python==4.10.0.84
```

Эти команды фиксируют core, **не образуют полный install script/lock**. В editable install проекта тоже передать constraints, чтобы resolver не заменил core. Собрать собственный wheel/lock и image digest только после resolution; `pip check`, freeze и smoke обязательны. Нельзя подменить2.14.1 base установкой2.5.1 поверх и продолжать называть image готовым2.14.1 recipe.

## Манифест B: D-FINE-M challenger

| Поле | Значение / статус |
|---|---|
| Source | `Peterande/D-FINE@956d1709314c2c6a4df6f34de232054578a7449f`; **DOC**, install **UNRUN** |
| Native requirements | torch>=2.0.1, torchvision>=0.15.2, faster-coco-eval>=1.6.6, PyYAML, tensorboard, scipy, calflops, transformers, loguru; **DOC**, без верхних границ/lock |
| Python/core | Native README Python3.11.9 **DOC**; выбранные Torch2.5.1/vision0.20.1 cu124 train, CPU export удовлетворяют declared minima **INFERRED**, фактическая совместимость **UNRUN** |
| Ancillary constraints | transformers4.44.2, calflops0.3.2 — выбранные **INFERRED** candidates, PyPI versions/metadata **DOC**; остальной полный lock ещё **UNRUN**. calflops тянет accelerate>=0.22.0 и HF hub; transformers требует hub>=0.23.2,<1.0 и tokenizers>=0.19,<0.20. Их пересечение не является resolved env |
| Init / exposure | `https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_coco.pth` — primary README model-zoo **DOC**. Отдельно от obj365/obj2coco; hash полученных байтов **UNRUN**, веса не скачаны |
| Config | `configs/dfine/custom/dfine_hgnetv2_m_custom.yml` плюс все include: custom_detection/runtime/dataloader/optimizer/dfine_hgnetv2; HGNetv2 B2,4 decoder layers **DOC** |
| Data adaptation | Собственный frozen config меняет `num_classes:777`, train/val paths и class mapping; original custom YAML содержит placeholders. Это необходимая **INFERRED** работа, **UNRUN**; нельзя запускать placeholder config как target training |
| Training entrypoint | `python train.py -c configs/team/dfine_m_target.yml -t LOCAL_DFINE_M_COCO --use-amp --seed 0 --output-dir output/RUN_ID`; flags **DOC**, path/recipe **INFERRED**, запуск **UNRUN**. `-t` = tuning, не `-r` resume |
| Train mutations | frozen config Btrain/Bval/epochs/stop_epoch/optimizer/AMP/EMA; native stage transition `stop_epoch` reloads `best_stg1.pth` и меняет EMA decay. Сократить epochs без согласования stop_epoch — другой recipe; **DOC/INFERRED**, execution **UNRUN** |
| Export entrypoint | stock `python tools/deployment/export_onnx.py -c SAME_CONFIG -r LOCAL_SELECTED_PTH`; **DOC**, но для выбранного первого gate использовать `tools/deployment/export_onnx_static_w2b.py` с нижеследующим diff **INFERRED, UNRUN** |
| Export envelope | CPU torch2.5.1/vision0.20.1, numpy1.26.4, onnx1.17.0, ORT CPU1.20.1; **INFERRED, UNRUN**. onnxsim0.4.36 — только отдельный optional simplified artifact |
| State / head | Native предпочитает `checkpoint["ema"]["module"]`, иначе `["model"]`, затем `model.deploy()+postprocessor.deploy()`; **DOC**. Reference обязан использовать этот же wrapper/state |
| Inputs / outputs | FP32 `images[1,3,640,640]`, int64 `orig_target_sizes[1,2]`; `labels/boxes/scores`; в выбранном adapter static batch1/opset16/legacy **INFERRED**, native names/opset **DOC**, actual graph **UNRUN** |
| Postprocess | native focal sigmoid→global query/class top-k→boxes gather, deploy outputs без train evaluator remap. Сохранить num_top_queries, category mapping, semantic size и inverse transform; **DOC**, parity **UNRUN** |

Минимальный **предлагаемый, не созданный/неисполненный executable adapter diff** к S07 (до исполнения сохранить patch bytes+hash):

```diff
- data = torch.rand(32, 3, 640, 640)
+ data = torch.rand(1, 3, 640, 640)
  size = torch.tensor([[640, 640]])
+ model.eval()
...
- dynamic_axes=dynamic_axes,
+ dynamic_axes=None,
  opset_version=16,
+ dynamo=False,
...
- default=True,  # в parser --simplify
+ default=False, # --simplify opt-in; первоначально не передавать
```

`size` здесь задаёт выбранную координатную систему640², не автоматически исходное H/W кадра; preprocessor/CPU inverse geometry обязаны ей соответствовать. В исходнике dummy batch32 при size batch1 допускает broadcasting; изменение наbatch1 убирает этот ненужный квалификационный ресурсный фактор, но не доказывает fit обучения. `--check` остаётся structural checker. Simplified граф сохранить под другим именем, не перезаписывать единственную unsimplified копию; такой output-name patch также versioned. [S07,S14]

## Конкретные несовместимости/негативные результаты

**W2-B-F05.** Native D-FINE source не объявляет ONNX/ORT/onnxsim в requirements. Установка `-r requirements.txt` не устанавливает полный export path. Более того, imports `src` могут тянуть training dependencies и при export; нельзя обещать «экспортный env состоит из Torch+ONNX» без import smoke. Выбранные transformers/calflops pins уменьшают дрейф, но не подтверждены авторами как их installed stack. [S03,S07,S15,S16]

**W2-B-F06.** PyTorch2.6 официально изменил default `torch.load` на `weights_only=True`. В D-FINE local tuning/resume и exporter вызовы не задают `weights_only`. Следовательно, произвольный upgrade меняет semantics загрузки. Это **риск**, а не доказательство, что все D-FINE checkpoints сломаются: plain state_dict может загрузиться. Torch2.5.1 обходит именно эту смену default, но разрешает старую pickle semantics: использовать только установленное trusted происхождение/hash. Не прописывать глобальное отключение защит загрузки ради непроверенного файла. [S17,S18]

**W2-B-F07.** Текущий Ultralytics pyproject содержит нижние границы и platform markers, а не lock; extras могут принести новые зависимости. `export-base` требует onnxslim>=0.1.82 и Python>=3.11 ORT>=1.20; выбранные ORT1.20.1/ONNX1.17 это допускают. Но simplifier намеренно исключён из первого пути. Зафиксировать NumPy1.26.4 + OpenCV4.10.0.84 полезно для legacy envelope: нельзя поставить произвольный current OpenCV и считать NumPy pin автоматически совместимым. PyPI4.10.0.84 metadata для Python3.11 требует numpy>=1.23.5. [S02,S10,S19]

Версия2.14.1 из W1-13 не опровергнута: её metadata существование не является доказательством применимости D-FINE old exporter. Live previous-versions при новом открытии уже показывает2.13.0 выше2.6.0; прежний W1 stale view не переносить как актуальное состояние. Рекомендация2.5.1 основана на конкретной exporter/load семантике и официальной паре, а не гонке за latest.2.4.1 fallback также UNRUN. [S01,S04,S12,S17]

Дополнительное ограничение K001 у challenger: `det_engine.py` при AMP сохраняет `NaN.pth`, если boxes содержат NaN/Inf, но этот block сам не прерывает обучение; дальше scaler может пропустить optimizer step. `det_solver.py` меняет state на stage boundary. Поэтому «нет YOLO recovery» не означает immutable D-FINE progress. Требуется journal nonfinite/skipped-step/stage-reload; ожидаемый stage transition заранее часть recipe, неожиданное recovery/NaN — failed trial. Это статическое чтение, negative drill не выполнен. [S20,S21]

## Один будущий discriminating experiment, без аренды сейчас

**Вопрос:** достаточно ли выбранных source-compatible envelopes для одного полного train→save/reload→same-head floating ONNX→ORT пути, или несовместимость локализуется в dependency/import/load/trace/runtime? Сначала проверять экспорт pretrained, чтобы не тратить training run на неизвестный exporter. Данные — небольшой разрешённый DEV fixture с raw frames и golden RGB/normalized tensors, explicit class mapping и geometry. Synthetic tensor разрешён для shape/smoke, но не для quality evidence.

1. В отдельно разрешённой подготовке создать A/B environments из frozen source и выбранных constraints; записать resolver report, wheel hashes, Python/build/platform, `pip check`, imports. Разрешать зависимости без бесконтрольной замены core. При конфликте остановиться с отчётом, затем новый manifest ID; не редактировать старый lock. Записать полный resolved lock и image digest лишь после факта.
2. Trusted init download/hash, показать key/missing/unmatched logs. D-FINE custom nc/path placeholders заменить frozen target config. До training экспортировать same-deploy reference наCPU, checker, ORT CPU comparator для golden tensor. Проверить head/state/names/dtype/shapes/opset/IR/operator inventory. Численные tolerance задать заранее по box/score, top-k ties сравнивать отдельно; несовпадения не скрывать одним mAP.
3. Только после разрешения hardware smoke: конкретная3090, inventory driver/CUDA/cuDNN/device, representative forward/backward, native val, save/reload. Btrain/Bval увеличить лишь в отдельном qualification run; измерить peak allocated/reserved и параметры реального batch/accumulation, AMP skipped/nonfinite steps.24GB fit и длительность до этого unknown.
4. После training повторить export/parity именно выбранного checkpoint и state; отдельно LinQ gate W2-F. Не считать экспорт до fine-tune достаточным для final model, другой head/precision/input требует нового gate.
5. Если2.5.1 path ломается на API/trace, пробовать fallback2.4.1/vision0.19.1 с новым ID; если ломается LinQ operator, смена Torch сама по себе не решение. Сначала локализовать op; conditional dense/CPU postprocess/new graph policy, затем новый parity. Unsupported required neural graph ⇒ baseline/challenger blocked для этого deployment, не ложный quality failure.

**Артефакты:** constraints+resolved lock, install logs, source/patch/config/checkpoint/tensor/ONNX hashes, raw comparator outputs, traces/операторы, recovery/step log, memory train/val, exact hardware, decision PASS/FAIL/BLOCKED и locator. **Метрики**: imports/checker/runtime errors; max/quantiles absolute/relative score и box error; label/ranking differences near ties; actual completed optimizer updates; nonfinite/skipped steps; peaks. Никаких invented времени/VRAM/вероятностей.

**Успех не доказывает:** target accuracy, tiny PPE recall, multi-camera latency, LinQ compilation/placement/quantization, независимость dataset splits, точный lossless resume или совместимость другой версии. DEV export fixes/threshold/checkpoint tuning не проводить на lockbox. TRAIN/VAL/SELECT/lockbox должны быть separated по incident/camera/scene lineage, соседние кадры не независимые samples.

## Хэндoff и оставшиеся блокеры

- **W2-A/K001:** применить fail/fork policy к этому же Ultralytics SHA; confirmed-loop hooks вместо выдуманных callbacks, не приравнивать EMA updates к успешным optimizer steps. D-FINE stage reload и AMP skips явно учесть.
- **W2-C:** checkpoint bytes hash/license/exposure; O365 provenance YOLO26 и D-FINE COCO/obj2coco разделить. Source licenses не выдают target-data permission.
- **W2-F:** передать distinct graph contracts A-one2one-opset18 / A-dense-conditional / B-static-postprocess-opset16; реальные supported IR/opset/layout/input dtypes/TopK/Gather/GridSample/LinQ SDK остаются внешними Q. Никаких TPU claims из ORT CPU.
- **Владелец реализации:** создать два environment constraints, недостающий full lock и небольшой D-FINE adapter; Python3.11.9 availability/Linux base digest/host driver — inventory. Нужны разрешённые данные, trusted weights, доступный CPU для import/export и отдельно GPU для train smoke. Никакие расходы настоящим документом не разрешены.
- Незакрытые package decisions: build isolation setuptools/wheel; все noncore dependencies Ultralytics (включая ultralytics-platform дляPython>=3.11), D-FINE faster-coco-eval/scipy/PyYAML/tensorboard/loguru; transitive accelerate/HF/tokenizers/safetensors/protobuf; wheel tags/GLIBC/CPU libs. Нет основания писать «все SHA pinned ⇒ stack runnable».

## Первичные evidence records

Все доступны/прочитаны **2026-10-23**. Author=project contributors, кроме D-FINE: Yansong Peng et al.; publication/version отдельно от access. Locator — symbol/section надёжнее строк, поскольку web/plain normalization даёт разную нумерацию. DOC — статическое source/metadata/docs, не наш runtime.

| ID | Автор, версия, URL, locator | Evidence / ограничения |
|---|---|---|
| **W2-B-S01** | PyTorch contributors, live [Previous versions](https://pytorch.org/get-started/previous-versions/), sections v2.5.1/v2.4.1 | Official Torch/vision pairs + cu124/CPU install indexes; release versions, не installed env |
| **W2-B-S02** | Ultralytics, SHA de290d…, [pyproject.toml](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/pyproject.toml), project/dependencies/export-base/export-legacy-torch | Declared constraints/markers; не whole dependency resolution |
| **W2-B-S03** | Peng et al., SHA956d170…, [requirements.txt](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/requirements.txt), весь9-line file | Native minimal requirements; ONNX stack отсутствует |
| **W2-B-S04** | PyTorch, tagv2.5.1, [torch/onnx/__init__.py](https://github.com/pytorch/pytorch/blob/v2.5.1/torch/onnx/__init__.py), export signature dynamo=False | Versioned API, not model compatibility |
| **W2-B-S05** | Ultralytics, de290d…, [utils/export/engine.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/utils/export/engine.py), torch2onnx/best_onnx_opset | Explicit legacy and version-dependent automatic opset |
| **W2-B-S06** | Ultralytics, de290d…, [engine/exporter.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/exporter.py), Exporter.__call__/export_onnx | Head selection/native package checks/output names; local fresh copy preserved |
| **W2-B-S07** | Peng et al.,956d170…, [export_onnx.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/tools/deployment/export_onnx.py), main/parser | EMA/deploy/batch32/opset16/dynamic axes/defaultTrue simplify; no explicit dynamo |
| **W2-B-S08** | ONNX contributors, [PyPI1.17.0 metadata](https://pypi.org/pypi/onnx/1.17.0/json), info.requires_python/requires_dist/urls | Declared distributions only; saved JSON |
| **W2-B-S09** | Microsoft ORT contributors, [PyPI1.20.1 metadata](https://pypi.org/pypi/onnxruntime/1.20.1/json), requires_dist/urls | CPU distribution, not provider/hardware performance |
| **W2-B-S10** | Microsoft ORT, [compatibility](https://onnxruntime.ai/docs/reference/compatibility.html), ONNX opset support row1.20; [versioned v1.20.1 policy](https://github.com/microsoft/onnxruntime/blob/v1.20.1/docs/Versioning.md) | Version/opset/IR necessary bounds, no exhaustive environment guarantee |
| **W2-B-S11** | Peng et al.,956d170…, [README](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/README.md), Quick start/Setup + model zoo M | Python3.11.9; COCO checkpoint URL; no Torch pin |
| **W2-B-S12** | PyTorch, v2.4.1, [torch/onnx/utils.py](https://github.com/pytorch/pytorch/blob/v2.4.1/torch/onnx/utils.py), export signature L176–196 | Fallback API accepts dynamo=False, not executed |
| **W2-B-S13** | Ultralytics, de290d…, [head.py](https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/nn/modules/head.py), Detect.end2end/forward/fuse/postprocess | Fusion/head conditional; actual checkpoint not inspected |
| **W2-B-S14** | Peng et al.,956d170…, [postprocessor.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/zoo/dfine/postprocessor.py), forward/deploy | scaling/query selection/early deploy return before remap |
| **W2-B-S15** | Hugging Face team, [transformers4.44.2 metadata](https://pypi.org/pypi/transformers/4.44.2/json), info.requires_python/requires_dist | Candidate pin, not D-FINE authors tested env |
| **W2-B-S16** | MrYXJ/calflops contributors, [calflops0.3.2 metadata](https://pypi.org/pypi/calflops/0.3.2/json); [onnxsim0.4.36 metadata](https://pypi.org/pypi/onnxsim/0.4.36/json) | Dependency edges; onnxsim optional in our adapter |
| **W2-B-S17** | PyTorch, [v2.6.0 release notes](https://github.com/pytorch/pytorch/releases/tag/v2.6.0), Backwards Incompatible changes / Flip default torch.load | Documented behavior change, not observed D-FINE failure |
| **W2-B-S18** | Peng et al.,956d170…, [_solver.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/_solver.py), load_resume_state/load_tuning_state | torch.load without explicit weights_only; strict/mismatched state rules |
| **W2-B-S19** | OpenCV wheels maintainers, [opencv-python4.10.0.84 metadata](https://pypi.org/pypi/opencv-python/4.10.0.84/json) | Python-conditioned numpy minimum; no binary import test |
| **W2-B-S20** | Peng et al.,956d170…, [det_engine.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_engine.py), train_one_epoch AMP/nonfinite | Save NaN.pth, scaler step/update, not runtime audit |
| **W2-B-S21** | Peng et al.,956d170…, [det_solver.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/src/solver/det_solver.py), stop_epoch block | Native best_stg1 reload/EMA decay mutation |
| **W2-B-S22** | Peng et al.,956d170…, [train.py](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/train.py), parser/main; [M custom](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dfine/custom/dfine_hgnetv2_m_custom.yml); [custom dataset](https://github.com/Peterande/D-FINE/blob/956d1709314c2c6a4df6f34de232054578a7449f/configs/dataset/custom_detection.yml) | Exact flags/config includes and placeholder class/path; recipes not run |

Отрицательные сетевые наблюдения: guessed `src/misc/profiler.py` и `src/zoo/dfine/dfine_postprocessor.py` дали404; правильный `postprocessor.py` открыт. Versioned docs2.5/onnx web отказал, вместо него открыт tagv2.5.1 API source. Эти отказы не трактуются как отсутствие функциональности.
