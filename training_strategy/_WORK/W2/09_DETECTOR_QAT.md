# W2-09 — Detector QAT → export: конкретный NVIDIA YOLOv7 route и граница LinQ

**K009; исследователь второй волны gpt-6.1-sol/medium.** Проверено 23.10.2026, 07:49–07:55 Europe/Moscow (UTC+3); это время исследования, не дата соревнования/публикации. Статус: прочитаны общий/тематический промпты, обязательный блок W2, PLAN, исходная критика K009 и внешние неизвестные, W1-13 полностью, W1-15 E04, W1-10 F12. Выполнены primary search + открытие документации, GitHub API tree/commit metadata и чтение исходников по HTTPS. **Не выполнялись установка toolkit, download weights, training, export, compilation, inference или benchmark.**

## Ответ и изменение решения

Публичный detector-specific путь существует: **NVIDIA-AI-IOT/yolo_deepstream, `yolov7_qat`, YOLOv7 → fusion → quantized modules/rules → calibration → feature-reconstruction QAT → ONNX Q/DQ opset 13 → TensorRT**. Код прочитан до конкретного loss и экспортера. Это существенно точнее общего Jacob QAT paper из W1. Однако это **не полностью закреплённый воспроизводимый toolchain**: авторская инструкция клонирует неприкреплённый YOLOv7 и устанавливает неприкреплённый `pytorch-quantization`; historical package lock/checksums опубликованных weights/ONNX не установлены. Ни одного полностью воспроизводимого LinQ QAT route этой работой не установлено.

Особенно важно: найденный QAT не использует detector GT loss; он восстанавливает признаки исходной модели через MSE. Его нельзя назвать штатным supervised fine-tuning для новых PPE classes. Переход с выбранного YOLO8/11/26 на YOLOv7 ради такого примера не обоснован. Следующая работа до QAT — получить **реальный SDK quant contract и sample, совпадающий с выбранной архитектурой**, затем закрыть dependency lock. K009: **уточнена область применимости / найден concrete code route; точный environment и target match открыты**.

## Источники и фактически полученные артефакты

Все даты доступа: 23.10.2026. Copyright в исходнике не считается датой публикации/измерения. Чтение кода не означает проверку его выполнения. Ссылки на `main` ниже заменены установленными SHA там, где это существенно.

| S-ID | Первичный источник, версия, локатор | Что реально получено |
|---|---|---|
| W2-09-S01 | NVIDIA-AI-IOT, [YOLOv7 QAT README](https://github.com/NVIDIA-AI-IOT/yolo_deepstream/blob/e9b75770ea58713d1cb3902d67c36e11acb888d7/yolov7_qat/README.md), SHA `e9b75770ea58713d1cb3902d67c36e11acb888d7`, Setup/How To QAT/Results | README открыт браузером и raw HTTPS; дерево/commit через GitHub API. Дата публикации route не установлена. |
| W2-09-S02 | NVIDIA, [scripts/qat.py](https://github.com/NVIDIA-AI-IOT/yolo_deepstream/blob/e9b75770ea58713d1cb3902d67c36e11acb888d7/yolov7_qat/scripts/qat.py), тот же SHA; `load_yolov7_model`, `cmd_quantize`, `supervision_policy`, `export_onnx` | Полный текст скрипта; API/порядок вызовов, без выполнения. |
| W2-09-S03 | NVIDIA, [quantization/quantize.py](https://github.com/NVIDIA-AI-IOT/yolo_deepstream/blob/e9b75770ea58713d1cb3902d67c36e11acb888d7/yolov7_qat/quantization/quantize.py), тот же SHA; `initialize`, `replace_to_quantization_module`, `calibrate_model`, `finetune`, `export_onnx` | Полный код, включая фактический loss. |
| W2-09-S04 | NVIDIA, [quantization/rules.py](https://github.com/NVIDIA-AI-IOT/yolo_deepstream/blob/e9b75770ea58713d1cb3902d67c36e11acb888d7/yolov7_qat/quantization/rules.py), тот же SHA; `find_quantizer_pairs` | Полный код анализа Concat/MaxPool QDQ. |
| W2-09-S05 | NVIDIA TensorRT `release/8.5`, установленный SHA `68b5072fdb9df6b6edab1392b02a705394b2e906`; [tensor_quant.py](https://github.com/NVIDIA/TensorRT/blob/68b5072fdb9df6b6edab1392b02a705394b2e906/tools/pytorch-quantization/pytorch_quantization/tensor_quant.py), `ScaledQuantDescriptor`, `_tensor_quant`; [VERSION](https://github.com/NVIDIA/TensorRT/blob/68b5072fdb9df6b6edab1392b02a705394b2e906/tools/pytorch-quantization/VERSION) = `2.1.2` | Версионный source arithmetic reference, **не установленная версия package в опыте автора**. Raw code открыт; архивная docs URL перенаправляла на latest и не использована как доказательство 8.5.3. |
| W2-09-S06 | NVIDIA, [quant_conv.py](https://github.com/NVIDIA/TensorRT/blob/68b5072fdb9df6b6edab1392b02a705394b2e906/tools/pytorch-quantization/pytorch_quantization/nn/modules/quant_conv.py), тот же toolkit SHA; `QuantConv2d`, `_quant` | Source defaults/weight placement. |
| W2-09-S07 | NVIDIA, [tensor_quantizer.py](https://github.com/NVIDIA/TensorRT/blob/68b5072fdb9df6b6edab1392b02a705394b2e906/tools/pytorch-quantization/pytorch_quantization/nn/modules/tensor_quantizer.py), тот же toolkit SHA; `_get_amax`, `_fb_fake_quant`, `forward` | Source range/zero-point/export switch. |
| W2-09-S08 | WongKinYiu/YOLOv7 author repo, [models/yolo.py](https://github.com/WongKinYiu/yolov7/blob/a207844b1ce82d204ab36d87d496728d3d2348e7/models/yolo.py), main resolved SHA `a207844b1ce82d204ab36d87d496728d3d2348e7`; `Model.fuse`, `IDetect.fuseforward`; v0.1 resolves `9a00c173a44bfcf3a58cc2a60e37deb6a1fb9e03` | Прочитаны fusion/head interface; v0.1 проверен отдельно. Это кандидат source pin, **не доказательство author test на нём**. |
| W2-09-S09 | ONNX, [QuantizeLinear-13](https://onnx.ai/onnx/operators/onnx__QuantizeLinear.html#quantizelinear-13), Summary/Attributes | Открыта конкретная operator version 13 внутри текущей документации 1.24.0; не переносились новые types/blocks. |
| W2-09-S10 | OpenMMLab, [MMrazor v1.0.0 quantization guide](https://mmrazor.readthedocs.io/en/v1.0.0/user_guides/quantization_user_guide.html), revision `d9c5bc84`, full SHA `d9c5bc845cc5fa178dce9a5424830a2aee122f86`; [RetinaNet config](https://github.com/open-mmlab/mmrazor/blob/d9c5bc845cc5fa178dce9a5424830a2aee122f86/configs/quantization/ptq/base/ptq_tensorrt_retina_r50_1x_coco_calib32xb32.py); [ResNet QAT](https://github.com/open-mmlab/mmrazor/blob/d9c5bc845cc5fa178dce9a5424830a2aee122f86/configs/quantization/qat/base/qat_openvino_resnet18_10e_8xb32_in1k.py) | Открыты guide и оба config; tree v1.0.0 и main `90c7af1fdf35a606a2fceaaeb4b6be2f0dac4eb7` просмотрены через API. |
| W2-09-S11 | NVIDIA, [scripts/eval-trt.sh](https://github.com/NVIDIA-AI-IOT/yolo_deepstream/blob/e9b75770ea58713d1cb3902d67c36e11acb888d7/yolov7_qat/scripts/eval-trt.sh), route SHA | Полный shell script; не запускался. |

Публичные model links из S01: [QAT checkpoint](https://nvidia.box.com/shared/static/vph9af9rbe7ed7ibfnajsk248mw9nq9f), [QAT ONNX](https://nvidia.box.com/shared/static/v1ze885p35hfjl96xtw8s0xbcpv64tfr). Это найденные **ссылки на артефакты**, не скачанные/проверенные binaries; browser click ONNX link вернул Internal Error. Доступность, SHA256 и фактический graph не подтверждены.

## Новые факты и trace одного route

### W2-09-F01 — Почему MMrazor не выбран готовым detector QAT recipe

**Наблюдение по документации/конфигам/дереву, S10.** Guide закрепляет `torch==1.13`, export через ветку MMDeploy `for_mmrazor`; для dense heads предлагает fork MMDetection. Найденный RetinaNet R50-FPN config содержит `PTQLoop`/calibration, а доступные QAT configs в обследованных v1.0.0/main — ResNet18/LSQ. Поэтому соединение RetinaNet PTQ config с ResNet QAT training loop было бы нашим новым port. Это ограниченный negative result данного дерева, не утверждение отсутствия QAT support или любого внешнего detector config.

### W2-09-F02 — Training interface найден, но это reconstruction QAT

**Код S03, `finetune` и `calibrate_model`.** Замена modules использует toolkit default map; затем калибровка собирает ranges и `method="mse"`. QAT создаёт frozen quant-disabled clone; Adam обучает модель по сумме MSE hooked features. GT detector loss не вызывается. Defaults: 10 epochs, максимум 1000 batches/epoch, AMP, LR schedule `0:1e-6, 3:1e-5, 8:1e-6`; это recipe автора, не наша рекомендация. Calibrated ranges отключают дальнейший сбор статистики. Экспорт включает `use_fb_fake_quant`, вызывает `torch.onnx.export` в eval/no_grad и выключает switch. **Вывод:** labels нужны для оценки качества; эта реализация не учит новую семантику классов посредством bbox/class supervision. Данный факт уточняет blanket wording W1-13-F05 о labels для QAT loss: найден label-free reconstruction вариант.

### W2-09-F03 — Detector-specific вход, checkpoint, selection и export

**Код S02.** Загружается `torch.load(...)["model"]`, выполняется `model.float().eval().fuse()` до quant insertion. COCO train loader: 640, augment=True, batch default 10; calibration/QAT получают `float()/255`. Supervision policy выбирает отдельные top-level layers и исключает last head. Per-epoch COCO AP выбирает сохранение `{"model": model}`; optimizer/resume state не входит. `export_onnx` выставляет last-head `.concat=True`, адаптирует grid, объявляет opset 13, вход `images`, выход `outputs`; `--dynamic` делает динамическим **batch**, не H/W. Default dummy — `[1,3,640,640]` FP32. Это tied-to-YOLOv7 API, не generic exporter для YOLO8/11/26.

### W2-09-F04 — Fusion и head являются частью quant contract

**Код S08.** `Model.fuse` сворачивает Conv+BN, переводит RepConv и OREPA в deploy representation, сворачивает implicit head parameters и меняет forward. В `IDetect.fuseforward` `.concat=True` возвращает concatenated decoded predictions; для COCO head `nc=80`, `no=nc+5`. NMS по этому пути не добавлен. **Наш вывод:** менять fusion order после QAT нельзя без повторной parity проверки. В v0.1 `concat` interface не найден, в обследованном main он есть; release weight URL `v0.1/yolov7.pt` не закрепляет source compatibility экспортера. Нужны source pin и reload smoke, а не подмена source tag названием weight release.

### W2-09-F05 — Q/DQ placement не просто автоматическая обёртка Conv

**Код S04.** Правила просматривают временный ONNX, находят quantizers на ветвях Concat и MaxPool. Они возвращают пары для последующего разделения одного input quantizer между связанными modules. Это ограниченный pattern matcher с предположениями о соседстве Q→DQ→Conv и именовании weight nodes. Он не устанавливает глобальную поддержку произвольного residual/attention/head graph. Не переносить на другую архитектуру по одному имени YOLO. **Вывод:** совпадение scales/axes недостаточно; target должен сохранить смысл размещения QDQ и допустимой fusion.

### W2-09-F06 — Arithmetic reference toolkit 2.1.2, условный до environment lock

**Наблюдение по S05–S07.** Это исследованный reference, а не доказанная package версия S01 experiment.

| Contract field | Установленное по source reference | Ограничение переноса |
|---|---|---|
| Signedness / bit | Descriptor default 8-bit signed, `unsigned=False`, `fake_quant=True` [S05]; route задаёт histogram input descriptor [F02] | Не присваивать unsigned activation по аналогии с OpenVINO/MMrazor |
| Activation granularity | Descriptor default axis=None → per tensor [S05] | Фактический QAT checkpoint нужно инспектировать |
| Conv weight granularity | `QuantConv2d` default `axis=(0)` → output-channel K в KCRS; input/weight quantizers применяются до convolution [S06] | Не axis=1 activation layout; depthwise/head должны проверяться отдельно |
| Range / scale | Descriptor `narrow_range=False`; `_tensor_quant` clamp signed full range `[-128,127]`, inverse scale `127/amax`, round; fake outputs возвращаются в FP [S05] | Это не integer training и не свидетельство accumulator/bias precision LinQ |
| Zero-point / export | `_fb_fake_quant`: scale=`amax/127`, zero point 0; scalar для per-tensor, vector для per-channel, bounds `[-128,127]` [S07] | Не affine offset из произвольного PTQ; фактический emitted dtype/axis ещё требует graph inspection |
| Rounding | Native reference вызывает Tensor `.round_()` [S05]; ONNX QuantizeLinear-13 определяет nearest-even и saturation [S09] | Пограничные half-step/clipping values должны быть будущим parity тестом, не обещанием bit identity |
| Learned ranges | Descriptor default `learn_amax=False` [S05] | Нельзя называть этот route LSQ или learned clipping |

**Финальный format contract:** путь к ONNX использует PyTorch native fake-quant export representation; ожидаются `QuantizeLinear`/`DequantizeLinear`, не `QLinearConv`, не `.ort`. QDQ остаётся в FP operator graph и задаёт quant boundaries; actual backend precision устанавливается compilation/placement log. ONNX per-axis default axis=1 не заменяет явно необходимый Conv weight axis=0. S07/S09 подтверждают требуемую семантику, но реальный binary ONNX здесь не получен.

### W2-09-F07 — Авторский backend evidence ограничен и имеет shape discrepancy

**Документация S01 + код S11.** README связывает detector, COCO evaluation, QAT checkpoint и ONNX; предлагает контейнер `nvcr.io/nvidia/pytorch:22.09-py3`, но `pip install pytorch-quantization` не фиксирует package version. В таблице указан input 640 и TensorRT/Orin, однако `eval-trt.sh` принудительно экспортирует 672 и допускает `--fp16` для detection layer. **Вывод:** не реконструирована точная опубликованная измерительная цепочка, поэтому AP/FPS из README не используются как прогноз/сравнение для LinQ и не приписываются одному закреплённому environment. Claim «all nodes INT8» требует actual layer report; presence QDQ сам его не доказывает.

## Paper → implementation → candidate → target: статус уровней

| Уровень | Статус | Что меняет решение |
|---|---|---|
| QAT principle | W1-13-F12 уже установлен | Не нужен повторный generic paper обзор |
| Detector implementation | Найден и прочитан F02–F05 | Конкретный reconstruction route существует |
| Exact reproducible recipe | **Неполон**: README не фиксирует YOLO/toolkit исторического опыта; ONNX/weights checksum не получены | Нужен artifact/environment lock W2-09-Q01; source pins этого исследования не заменяют author run manifest |
| Candidate architecture | YOLOv7 sample; selected case model неизвестна | Нельзя объявить поддержку YOLO8/11/26/new class adaptation |
| LinQ arithmetic/export compatibility | **Не установлена** | Нужен W2-09-Q02; TensorRT-specific rules не target evidence |
| Target benefit | **Не измерен** | Будущий post-export gate W2-09-E01 |

## Матрица public supports / tool mismatch / SDK question / future experiment

| Часть | Public supports | Tool mismatch или gap | Вопрос/следующий gate |
|---|---|---|---|
| Training | Detector feature reconstruction with fake quant | Не supervised bbox/class recipe; нет доказанного current environment lock | Q01 + same-data controls E01 |
| Quant representation | Signed symmetric zero-point 0 reference; per-tensor activations/per-output-channel Conv weights | Реальный LinQ может требовать другой range/axes/quantizer | Q02 arithmetic/sample |
| Placement/fusion | YOLOv7 deploy fusion + Concat/MaxPool scale sharing | TensorRT-specific patterns; detector head mixed precision возможна | Q02 placement/exclusions, затем inspect graph |
| Export | ONNX opset13 QDQ; dynamic batch | QDQ ≠ quantized LinQ package; shape 640/672 не унифицирован | SDK versioned acceptance sample, E01 parity |
| Target | Авторские NVIDIA links | Ни LinQ compile, ни actual execution не выполнены | Target placement/raw outputs/metrics обязательны |

## Открытые вопросы, адресаты и конкретные требуемые артефакты

**W2-09-Q01 — artifact/environment, P1 → model_stack.** Для выбранной архитектуры получить единый manifest: source SHA detector и QAT patch, wheel version/hash toolkit, torch/ONNX/exporter versions, container digest, checkpoint class definitions и SHA256, calibration/range state, export command/effective settings, sample FP+QDQ graphs с expected outputs. Что известно: все code locators F02–F06 доступны; чего нет: verified historical combination и полученный binary graph. Закрытие — предоставленный авторский lock либо отдельный будущий compatibility smoke на явно выбранных pins. Не выдавать reference toolkit 2.1.2 за установленную автором версию. Для PPE потребуется готовый supervised FP checkpoint; этот script не добавляет новые классы.

**W2-09-Q02 — SDK contract, критический → linq_platform.** Запрашивать не абстрактное «есть ли int8», а следующие ответы **для фактически выданного SDK/compiler/runtime build и устройства**:

1. Кто задаёт ranges/quantization: DNN Quant из FP ONNX или внешний QAT? Принимаются ли ONNX QDQ opset13, сохранённые training scales/zero points; сохраняются они или перекалибруются? Нужен рабочий SDK sample с graph и expected outputs.
2. S8 activations+weights? Per-tensor activations, per-output-channel Conv weights axis=0 в KCRS? Как трактуются layout changes, depthwise/group Conv и detection head axes? Range `[-128,127]` или `[-127,127]`; zero-point обязательно 0? Каковы rounding tie rule, clipping, bias/accumulator/requant precision?
3. Fusion до/после QDQ: Conv+BN/RepConv/implicit head допустимы? Scale sharing Concat/MaxPool, Add, Resize/Upsample, sigmoid/decode поддерживаются? Можно ли исключать head/sensitive nodes или оставлять FP16/FP32; как это отражается в log и выполнении?
4. Допустим ли данный decoded head без NMS, input layout/normalization/static H/W/dynamic batch? Где выполняются NMS и обратное преобразование координат? Какие ops fallback на host, какой final binary format и reproducible compiler command?

Изменяемое решение: при FP-only import с собственным quantizer внешний QDQ route может не иметь смысла; при совпадении QAT import contract появляется основание маленького trial. Ответ «ONNX поддерживается» не закрывает Q02. Общий LinQ public search не повторялся.

**W2-09-Q03 — experiment, P1 → evaluation/datasets.** Есть ли независимые labels/сессии для измерения критичного recall после преобразования и отдельные development inputs для calibration/reconstruction? В W1 уже задан правильный split; неизвестна фактическая coverage. Без неё хорошее feature MSE не подтверждает пригодность детектора. Приоритет Q03 повышается только после FP export/PTQ diagnostics и SDK agreement.

## W2-09-E01 — Будущий QAT decision gate с точным контролем

Это уточнение W1-13-E03 и W1-15-E04, **не выполненный опыт и не отдельный обязательный trial для каждого метода**.

**Вопрос/входы.** При доказанной PTQ потере на нужных slices восстанавливает ли QAT качество в реально принятом LinQ artifact? Нужны Q01 lock и Q02 sample/contract, frozen supervised FP checkpoint с нужными classes, FP export parity, отдельные calibration/development train данные и независимые labeled camera/session groups. Не начинать по одному training flag или JPEG примерам автора.

**Контроль.** Сохранить исходный FP, FP continuation, PTQ и QAT, начатые от одинаковых weights. FP continuation и supervised QAT должны получать те же labels, order/exposures, augmentations, updates, optimizer budget и checkpoint-selection material; единственное основное вмешательство — target-matched fake quant. **Для найденного reconstruction script это другая постановка:** зафиксировать отсутствие GT loss; дать quant-disabled continuation с теми же images/hooks/optimizer/updates и отдельно назвать reconstruction objective. Такой FP self-reconstruction может почти не давать gradients, что ожидаемо и не равно сильному supervised FP baseline. Если добавлен detection loss/labels, это новый supervised port: одинаковый loss/labels нужен обеим веткам, и это нельзя назвать точным воспроизведением S03. Нельзя скрыто приписать QAT эффект teacher supervision, изменённой data exposure или новых annotations.

**Действия.** После bounded reload/forward/export smoke на development inputs проверить реальный QDQ graph: opset, dtype и ranges, zero points, per-channel axis/length, shared scales, оставшиеся FP islands, head outputs, shape. Сравнить reloaded native FP → FP export → QAT simulated → фактический post-export backend → compiled LinQ outputs на тех же canonical tensors. Если LinQ FP недоступен, target difference включает compiler и quantization, отдельно это записать. Для main comparison фиксировать preprocessing/NMS/thresholds, class map и event rules.

**Измерения/доказательства.** На каждой применимой стадии — AP с указанным IoU protocol, critical-class recall/precision, small-object/camera slices и paired errors; на event clips — fixed-rule event recall/false alarms. Numerical boundary tests — half-step, saturation, zero tensors; tensor differences помогают локализации, не заменяют GT metrics. Сохранять hashes configs/inputs/checkpoints/graphs, actual steps/exposures, selection history, quant params, exporter/SDK logs, fallback/precision/placement, raw outputs и независимые metric tables. Latency/peak memory измерять на actual device с fixed batch/shape/concurrency; модельное и end-to-end время отдельно. Точные бюджеты/допуски назначаются до опыта по фактическим данным/стоимости, здесь не выдуманы.

**Исходы/stop.** PTQ уже проходит constraints → оставить PTQ. FP export плох → чинить export до QAT. QDQ не принимается либо arithmetic меняется → остановить trial, вернуть Q02/штатный SDK путь. Simulated QAT улучшился, post-export ухудшился → investigate placement/arithmetic, не promote checkpoint. Target quality и performance проходят заранее заданные критерии против continuation/PTQ → freeze bundle и выполнить согласованный final holdout gate. Inconclusive/critical recall regression → rollback. Успех TensorRT/reference runtime не закрывает ни LinQ execution, ни camera generalization.

## Короткая передача

**Автору/сборщику:** K009 улучшен concrete detector code evidence; главный новый факт — label-free reconstruction objective и неполный historical environment lock. Не писать «MMrazor имеет готовый RetinaNet QAT config» по найденному PTQ. **→ model_stack:** Q01, fused YOLOv7/head serialization/export interfaces F03/F04. **→ linq_platform:** Q02, конкретный signed/per-axis/QDQ contract вместо общего ONNX вопроса. **→ evaluation/datasets:** Q03/E01, same-data FP continuation и фактическая post-export оценка. **Для очереди:** QAT остаётся условной веткой после PTQ diagnostics и SDK agreement; наличие красивого NVIDIA sample не повышает её до обязательного первого trial.
