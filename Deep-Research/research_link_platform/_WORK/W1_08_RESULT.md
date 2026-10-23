# W1-08 — модели, YOLO и сила доказательств

Дата фактического чтения: 2026-10-23, примерно 04:23–04:29 Europe/Moscow (+03:00). Исследователь W1-08. Это исследование, не реализация прототипа. Экспорт, квантование, компиляция и запуск на LinQ нами не выполнялись.

## Главный вопрос и вывод

Какие конкретные модели имеют основания для короткого списка model_stack и что реально подтверждено между названием семейства, весами, экспортом и выполнением на LinQ?

Лучше всего документирован путь **готовая vendor TinyYOLO3 `.tpu` → direct pytpu runner → внешнее декодирование/NMS → COCOeval**. Но сам бинарник и его исходные веса в найденном публичном репозитории не опубликованы. Для переобучаемой современной модели наиболее полезная зацепка — **Ultralytics YOLOv8s → ONNX opset13, static640, no embedded NMS → tpu_framework → `.qm` → `.tpu`**. Это конкретный сторонний исходный код, а не официальный SDK и не доказательство успешного исполнения: в runner есть ошибка имени атрибута до обращения к устройству, а compiler/runtime logs и результаты в checkout отсутствуют.

Официальные материалы подтверждают больше, чем одно общее «поддерживается YOLO»: руководство2025 называет протестированные `tiny_yolo2`, `yolo2`, `tiny_yolo3`, `yolo3`, `yolo5s`; /tech и презентация2026 дополнительно называют YOLO4/YOLO8/YOLO11. Презентация2026 сообщает измерение `yolo5s` и **`yolov8n_pose`**, но это не YOLOv8s detection и не YOLO11. Нельзя переносить это измерение на любую новую голову или произвольный exporter.

Практическое решение: запросить у инженеров готовый working detector и его точные контракты как первый аппаратный smoke test; параллельно готовить YOLOv8s/n detection с закреплёнными версиями и внешним NMS. YOLO11 оставить условным кандидатом до получения конкретного примера/операторного отчёта. FCN-ResNet50 полезен как доказательная ветка segmentation, но не первоочередной детектор СИЗ. ResNet50 — удобный контроль окружения, а не решение задачи детекции.

## Уровни доказательств

Уровни ниже не сливаются: A — название производителя; B — техническое описание/код; C — точные доступные веса и экспортированный артефакт; D — compiler log и `.tpu` с происхождением; E — runtime log/результаты/измерение с условиями. Наличие кода генерации C/D/E не равно наличию самого C/D/E.

| Модель/семейство | Что названо официально | Конкретная конфигурация/пример | Веса и артефакт | Compiler log | Измерение/реальный статус |
|---|---|---|---|---|---|
| TinyYOLOv3 | Guide2025 §3.4: протестирована; /tech; presentation2026 p5 | Сторонний runner для `tiny_yolo3_b8_o5_128x128_asic.tpu`; input `(8,416,416,3)` NHWC, `input_1:0`, unit float | Vendor `.tpu` только внешний путь; весов/хеша vendor нет. Отдельный strict exporter из pjreddie cfg/weights | В публичном checkout не найден | README утверждает подтверждённый runtime contract; численных сохранённых результатов нет. Наш статус: код прочитан |
| YOLOv8s detection | /tech и presentation2026: только YOLO8 | Реальный exporter/build/runner в commit3ad1b7…; default640, opset13, noNMS; build b1/b8 | Строка `yolov8s.pt`, поддержаны также n/m/l/x; веса/ONNX/хеш в checkout отсутствуют | Код компиляции есть, успешного лога нет | Ошибка runner до TPU; численного результата нет; аппаратно не проверялось |
| YOLOv8n pose | presentation2026 p4: точное имя `yolov8n_pose` | Batch1, HP/HPQ, общий benchmark context | Input resolution, exporter, weights, task config не раскрыты | Не опубликован в просмотренном материале | Vendor: HP104.8FPS/21.51ms; HPQ419.2FPS/21.51ms. Не наш тест |
| YOLO5s | Guide2025 §3.4; /tech; presentation p4/p5 | p4 b1; остальная точная конфигурация не раскрыта | Нет исходного checkpoint/hash/export | Нет | Vendor: HP106.1FPS/23.71ms; HPQ424.4FPS/23.71ms. Не наш тест |
| YOLO2/3, TinyYOLO2 | Guide2025 «протестированы»; /tech | Только имена в просмотренном guide | Не установлены | Не установлены | Публичное именование/заявление тестирования, не воспроизводимый пакет |
| YOLO4, YOLO11 | /tech, presentation2026 p5 | Только семейства; нет n/s/m/task/размера | Не установлены | Не установлены | В просмотренных источниках нет точного теста/метрик |
| FCN-ResNet50 | Сторонний repo; не путать с guide `FCN_8s` | torchvision; COCO_WITH_VOC_LABELS_V1; initial520x520, opset18, output logits | Идентификатор pretrained weights закреплён в коде; байты/хеш/ONNX не включены | Build/compile code есть; RUN_SCENARIO отдельно предупреждает, что O5 не дал final reproducible result | README заявляет рабочие контуры TPU/ORT; опубликованных чисел checkout не содержит |
| ResNet50 custom | Guide содержит ONNX end-to-end пример, /tech torch_resnet50 и др. | Repo torchvision IMAGENET1K_V2; NHWC224x224 input 0..255, normalization внутри wrapper; opset13 | Enum weights есть, bytes/hash нет | Код есть, лога нет | Отдельные vendor resnet50_mlperf программы не тождественны этому exporter |
| Остальные сети /tech | densenet121; efficientnet_b0/b1/b2/b3; inception_v1/v2/v3/v4; lenet5; mobilenet_v1/v2; nasnet_mobile; pnasnet_large/mobile; resnet152/34; resnet50_mlperf/v2; ssd_mobilenet_v1/v2; scrfd2.5g; torch_densenet169/mobilenet_v2/resnet50; vgg19; xception | Имена, местами точный вариант | Нет полного manifest | Нет | Для части p4 есть vendor performance, не задача этой ветки; не доказательство любой пользовательской модификации |

Основания таблицы: W1-08-S01…S10. «Нет» означает не обнаружено в конкретно просмотренном публичном checkout/материале; не утверждается несуществование у производителя.

## Подробные факты и инженерные следствия

### F01. Официальный перечень не является Model Zoo с артефактами

Тип: vendor_statement; проверка: /tech реально открыт и прочитан web; presentation text прочитан TinyFish. На /tech есть перечисление моделей, но просмотренный блок не даёт checkpoint URLs, hashes, input/output manifests или compiler logs. На /sol Model Zoo перечислен как компонент комплекта ПО. Это подтверждает существование предложения производителя, но не доступность комплекта нам. Точные «YOLO8» и «YOLO11» не задают размер модели, task, input, exporter или версию пакета.

Guide2025 §3.4 использует более сильную формулировку «протестированных с использованием фреймворка IVA H1», но также без конфигураций. Дополнительные имена guide: FCN_8s (назван классом U-Net), seresnet50, flownet, REGNET_Y_800MF, anti_spoof_mn. Не подменять FCN_8s современным torchvision FCN-ResNet50.

### F02. Современное vendor-измерение относится к pose

Тип: reported_measurement производителя; проверка: прочитан извлечённый текст первичного PDF, не собственный benchmark. Presentation2026 p4 содержит `yolo5s` и `yolov8n_pose`, оба b1. Общая сноска: Intel Core i7-10700K @3.80GHz, Ubuntu24.04, TPU Runtime16.18.6, TPU Framework2026.8.43, заявленная методика MLCommons MLPerf. Значения приведены в матрице. Нет веса/разрешения/числа потоков/raw logs/точного режима MLPerf/качества. У HPQ throughput ровно4x HP, latency сохранена — не выводить из этого end-to-end скорость одной видеокамеры. Фраза методики не доказывает официальный submitted MLPerf result.

### F03. Происхождение стороннего репозитория установлено до commit

Тип: source_code + local_observation; проверка: прочитан checkout W1-06, `git rev-parse HEAD` и `git show -s --format=fuller HEAD` выполнены. HEAD `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`; автор/committer `sherstpasha`; 2026-04-03 12:44:54 +0700. Сообщение: Add error handling for device detection in parallel MLPerf scripts. Это пользовательский primary code и свидетельство его собственных инженерных попыток. Не обнаружено основания называть его официальным LinQ SDK или гарантированной конфигурацией хакатона.

`.gitignore` исключает `*.json`, `*.onnx`, `*.pt`, `*.weights`, `*.h5`, `data/`, `artifacts/`, `experiments*/`, `third_party/`, а также `POYASNITELNAYA_ZAPISKA_LinQ_RESULTS.md`. Поэтому наличие упоминаний результатов в сценарии не означает их публикацию. В checkout есть код и RUN_SCENARIO, отсутствуют сами model binaries/compiler logs/results summaries. Нельзя извлечь количественный benchmark из перечисленных путей.

### F04. YOLOv8: точный экспорт и неприкреплённые версии

Тип: source_code; проверка: прочитаны `export_yolov8s_to_onnx.py`, `build_yolov8_program.py`, `run_yolov8.py`, `run_yolov8_tpu.py`.

Exporter default: `YOLO('yolov8s.pt')`; ONNX `imgsz=640`, `opset=13`, `batch=1`, `dynamic=False`, `simplify=False`, `nms=False`. `YOLO_AUTOINSTALL=False`. При существующем локальном пути использует его; для встроенных n/s/m/l/x передаёт имя Ultralytics. Иного immutable asset URL/version/SHA код не фиксирует. Sidecar JSON сохраняет weights string/source, opset, batch, img size, flags, input/output names/shape, но не package versions и checksum checkpoint/ONNX.

requirements: `numpy==1.26.4`, `onnx~=1.16.0`, `onnxruntime~=1.18.0`, `tensorflow==2.14.1`, `setuptools<81`; torch/torchvision без версии; ultralytics вообще не включён в requirements (runner требует установить отдельно). `tf2onnx` для strict exporter тоже отдельная зависимость. Это не воспроизводимый lockfile. Актуальные online Ultralytics docs уже показывают более новые поколения/изменения default export flags; нельзя ими подменять неизвестную версию автора апреля2026.

### F05. YOLOv8: build contract

Тип: source_code; проверка: только чтение. В build вход ONNX принудительно статизируется `[1,3,640,640]`; calibration RGB, NCHW, float32 /255, letterbox. Общий helper: OpenCV INTER_LINEAR, padding114, rounded scaled width/height, symmetric integer padding. Вызов `onnx_to_tf` пробует namespace tpu_framework, затем onnx_direct; варианты `try_simplify=True`, False, без параметра. Это адаптационный код, не документированный универсальный контракт SDK.

После RegularModel/calibrate/quantize сохраняется `.qm`; default percentile100, 500 calibration images, chunk128; `Network.from_quantized_model`, `network.set_batch`, `compiler.compile_(hardware_parameters=TPU_128x128_PARAMS, ..., parameters=O1)`, `TpuProgram.from_executable(...).to_file(...)`; defaults batches1/8. `128x128` — параметр аппаратного массива, не разрешение входного изображения. Детальную компиляцию/калибровку исследуют W1-06/W1-07; здесь важен model contract, а не подтверждение результата.

### F06. YOLOv8 runner: конкретная блокирующая ошибка

Тип: source_code + local_observation; проверка: AST без импортов и аппаратного запуска. В `run_yolov8_tpu.py:206` вызывается `args.output_tensอร์_name`; parser определяет `--output-tensor-name`, то есть `output_tensor_name`. В середине фактического атрибута стоят U+0E2D/U+0E23/U+0E4C. В нормальном исполнении после прохождения ранних проверок это приводит к AttributeError до `tpu.Device.list_devices()`. Сохранён протокол `_WORK/W1_08/yolov8_runner_ast_audit.json`. Это вывод из синтаксиса, не зарегистрированный аппаратный error log.

Дополнительно: input probing пробует несколько tensor names и `run`/`sync`, output selection может взять первый rank≥3 tensor. Это полезные эвристики при диагностике, но для acceptance нужен manifest с единственным правильным output. Код принимает формы `[B,84,N]`/`[B,N,84]` и также85; это COCO80-specific предположение. После обучения на N иных классов ширина4+N не пройдёт проверку. Даже принятие85 не доказывает корректную семантику objectness для другой версии YOLO.

Postprocessing выполняется на host: `ultralytics.utils.nms.non_max_suppression`, conf0.001, IoU0.65, max_det300, преобразование координат обратно после letterbox, COCO80→91 categories. Для касок/респираторов нужно убрать фиксированную COCO mapping и явно задать class count. Наличие CPU torch для NMS не означает CPU исполнения backbone; это отдельная стадия.

Timing обрамляет только `run_once`, не preprocessing/NMS/декодирование/видео. Warmup вычитается числом изображений; при пересечении границы warmup внутри batch может учитываться полный batch time с меньшим числом measured images. Поэтому скриптовый FPS нельзя выдавать за end-to-end FPS или строгий latency benchmark без проверки методики.

### F07. TinyYOLO3: три разных маршрута

Тип: source_code; проверка: прочитаны README/exporter/downloader/runner/ORT helpers.

1. **Vendor TPU**: внешний путь `linq_files/tpu_programs/tiny_yolo3_b8_o5_128x128_asic.tpu`, `input_1:0`, b8, NHWC416, float0..1. `run_tiny_yolo3_accuracy.py` выполняет letterbox и BGR→RGB. Runner декодирует raw-head выходы; generic формы поддерживают транспонирование/перестановки. Anchor defaults `10,14 23,27 37,58 81,82 135,169 344,319`, masks coarse→fine `3,4,5|0,1,2`, classes80. Декодирование использует sigmoid xy/objectness/classes, exp wh, anchors, grid/stride; внешний NMS. Это не встроенный NMS Model Zoo. Quality direct TPU + COCOeval; performance отдельно mlperf. README называет runtime contract подтверждённым, но бинарник/manifest/raw result недоступны в checkout.
2. **Strict ONNX**: cfg `https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg`, weights `https://data.pjreddie.com/files/yolov3-tiny.weights`; код сам строит Keras модель, читает Darknet header/BN/conv weights, сохраняет h5, экспортирует tf2onnx opset13; dynamic batch default0, NHWC416, `input_1`, raw heads. Имена enum/layers и anchors доступны, но URL cfg на master и weight URL без checksum — ещё не immutable provenance. Сравнение с vendor weights пока гипотеза: vendor source/hash не раскрыты.
3. **ONNX Model Zoo**: downloader использует `https://huggingface.co/onnxmodelzoo/tiny-yolov3-11/resolve/main/tiny-yolov3-11.onnx`; model card показывает ONNX1.6/opset11, ~34MB, image NCHW1x3x416x416 и второй input1x2 original image size, outputs boxes/scores/selected indices. Это другой graph boundary со встроенным selection/NMS, не raw-head vendor `.tpu`.

Важное расхождение: strict metadata задаёт BGR; ORT `preprocess_image` фактически оставляет OpenCV BGR и вообще не применяет поле image_color_order. Vendor runner делает RGB. Оба используют общий padding114/INTER_LINEAR. В primary Model Zoo card пример PIL RGB, padding128/BICUBIC. Поэтому «тот же TinyYOLO3» не означает честное сравнение качества или скорости. Сначала нужен byte-identical prepared tensor и проверка головы/весов. Это конкретный повод для sanity test цветного изображения до большого COCOeval.

Model Zoo card сообщает mAP0.331 как значение исходной TinyYOLOv3 на COCO, не LinQ INT8 measurement и не наш ORT test. Не переносить это качество на vendor compiled model.

### F08. FCN-ResNet50: точные веса известнее, но итогов исполнения нет

Тип: source_code + primary_documentation; проверка: source files, RUN_SCENARIO и torchvision docs прочитаны. Export использует `FCN_ResNet50_Weights.COCO_WITH_VOC_LABELS_V1`, wrapper возвращает `model(x)['out']`; default tensor `[1,3,520,520]`, float normalized, input `input`, output `logits`, opset18, `dynamo=False`, constant folding, dynamic_axes batch/height/width. Quantizer позже статизирует input. Host preprocessing RGB PIL, принудительный square520 resize, /255 и ImageNet mean/std. Runtime делает argmax по class axis и resize mask nearest к исходному размеру. Это 21 labels (20 VOC + background), не произвольный промышленный segmentation head.

Torchvision primary docs объясняют, что enum обучен на COCO subset с VOC20; стандартный transform resize short side520 с aspect ratio и normalization. Репозиторный square resize — собственный контракт; его нельзя назвать byte-identical official transform. Публикуемое torchvision mIoU60.5 относится к COCO-val2017-VOC-labels, не к TPU INT8 и не прямо к репозиторному VOC2012 eval.

Standalone compile defaults O5/b8, но RUN_SCENARIO явно говорит, что segmentation O5 не дал final reproducible result и не должен входить в final result set. Это содержательная отрицательная зацепка; наличие defaultO5 не доказательство работоспособности. README называет TPU и ORT контуры рабочими, но численных summaries/logs в публичном checkout нет.

### F09. Разные контракты нельзя унифицировать по названию модели

Тип: inference из S04–S09. В одном repo ResNet50 wrapper принимает NHWC0..255 с normalization внутри ONNX; YOLOv8 принимает NCHW0..1; TinyYOLO3 vendor NHWC0..1 RGB; TinyYOLO3 ORT остаётся BGR; FCN принимает уже нормализованный NCHW. Универсальный `frame/255` перед любым `.tpu` неверен. Первым артефактом интеграции должен быть machine-readable model manifest: source weights/hash; versions; graph/checksum; exact tensor names/shapes/layout/color/range; resize/pad/interpolation; class map; raw head/postprocessing; calibration provenance; compiler target/batch/preset; runtime version.

## Противоречия и ограничения

- Guide2025 Python3.11/Ubuntu20.04 vs /sol Python3.8 — разные публичные сведения, не установлен единый совместимый environment. Presentation2026 benchmark Ubuntu24.04/Runtime16.18.6/Framework2026.8.43 не означает выдаваемую команде версию.
- Поддержка ONNX>=1.15.0 в блоке HX /sol — версия Python package, не opset15 и не общий предел компилятора. Repo показывает YOLO opset13 и FCN18 как намерение автора; успешный компиляторный лог для18 не опубликован.
- YOLOv8n_pose vendor measurement и YOLOv8s detection code — разные конфигурации. Ни одно не доказывает YOLO11 segmentation/pose/OBB.
- Model Zoo — название компонента поставки производителя и название независимого ONNX Model Zoo. Их нельзя объединять.
- В презентации список сетей — p5; p6 — архитектуры/ОС с графикой. В этой ветке p6 визуально не увиден. Text extraction не доказывает содержимое логотипов; не делаю выводов о поддерживаемых ОС/CPU по невидимым изображениям.

## Поиск и фактически выполненные операции

Прочитаны профильное задание W1_08, положения §7/9/11 большого prompt, guide extracted W1-03, checkout W1-06 (read-only), /tech, /sol через TinyFish, primary model cards/docs. Запросы web: `site:lin-q.ru "Model Zoo"`, `"LinQ" "yolo" github`, `"linq-cv-bench"`. Слово LinQ даёт много нерелевантного C# и одноимённых компаний; они не использованы.

Web open GitHub pinned tree вернул restricted URL; TinyFish открыл публичный root, CLI git checkout доступен. Web и search_service open PDF вернули inaccessible; curl Schannel TLS handshake failure; Python requests HTTPS SSLEOFError даже без verification; HTTP remote disconnected. TinyFish извлёк PDF text, сохранено `_WORK/W1_08/presentation2026_tinyfish.json`. Исходный PDF скачать не удалось, screenshot/render p6 не выполнен. Навык PDF прочитан и применён к выбору визуальной проверки, но отсутствие байтов локализовано; никакие невидимые логотипы не интерпретировались.

AST inspection runner выполнен без imports и без исполнения модели. Ни weight bytes, ни `.onnx`, ни `.qm`, ни `.tpu` нами не получены; device credentials отсутствуют. Собственных throughput/mAP/mIoU measurements нет.

## Shortlist, неизвестные и следующие проверки

1. **Первый smoke test: vendor TinyYOLO3** при предоставленном бинарнике/SDK. Попросить `.tpu` + checksum + compiler target + actual tensor descriptions + эталонный image/tensor/output + source weights identity. Цель — подтвердить pipeline и устройство; не окончательное качество детекции СИЗ.
2. **Основной условный детектор: YOLOv8s или n detection**, static input640, external NMS, pinned Ultralytics/torch/onnx/export version, exact checkpoint hash. До первого compile не заявлять поддержку customN classes. Исправить runner typo, shape hardcode84/85 и COCO mapping как отдельную будущую адаптацию, не менять исследовательский checkout.
3. **Если есть официальный YOLO5s example**, запросить и предпочесть первый working compiled package для раннего checkpoint. Семейство имеет guide+modern vendor benchmark, но публичная воспроизводимая сборка здесь не найдена.
4. **YOLO11** — только после SDK-specific sample или compile feasibility report. Имя на сайте недостаточно для решения команды потратить большую часть45часов.
5. **ResNet50** — контроль доступности devices/SDK/quantization fidelity; **FCN-ResNet50** — альтернативный segmentation experiment только при требовании задачи и поддержке opset/resize, с O1 и проверкой качества прежде оптимизацииO5.

Конкретные вопросы инженерам: какая точная YOLO8/11 task+variant+input+exporter версия проверена? Есть ли отдельный pose пример и можно ли получить raw output decoder? Выполняются ли DFL/reshape/concat/resize/sigmoid на TPU или host? Поддерживаются ли custom number of classes и batch1? Где model_zoo с checksum и input/output manifests? Есть ли compiler report unsupported ops и запрет silent fallback? Какой именно package/runtime будет на online instance?

Предлагаемые эксперименты после доступа: (E1) decode fixed image на float baseline и vendor TPU, сохранить prepared tensor/output names/checksums; (E2) проверить RGB/BGR на цветном synthetic tensor, padding/interpolation отдельно; (E3) exporter static640 noNMS → ONNX checker/shape inventory → conversion → calibration → compile с полными логами; (E4) сравнить float/quantized/emulated/TPU outputs и mAP на одном subset; (E5) b1 сначала, затем b8, отдельно device time и end-to-end frame latency; (E6) class count !=80, чтобы поймать host assumptions до обучения; (E7) измерить фактическую стоимость external NMS/tracker/video. Все E — будущие, не выполнены.

Handoff W1-06: typo runner line206 и отсутствие success logs; W1-07: RGB/BGR и padding mismatches, current YOLO preprocessing; оркестратору/соседнему model research: shortlist строго условный, exact vendor configs unknown, современный измеренный YOLO — pose n, а доступный код — detection s.

## Источники

Все accessed 2026-10-23 около04:23–04:29+03:00; даты документа указаны отдельно. URL с commit — стабильный locator.

- **W1-08-S01** — ООО ХайТэк, «Технологический стек», дата страницы неизвестна, [страница](https://lin-q.ru/tech), блок «Поддерживаемые сети». Статус: web full text прочитан. Ограничение: vendor list, без artifacts.
- **W1-08-S02** — ООО ХайТэк, «Модули ускорения / ПО», дата неизвестна, [страница](https://lin-q.ru/sol), блоки FW/Model Zoo/HX. Статус: TinyFish текст прочитан. Ограничение: комплект ПО не получен.
- **W1-08-S03** — ООО ХайТэк, Framework manual H1,2025, RU.РМДВ.04.06.014-03 34 01, [PDF](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), §3.3 resnet50 ONNX example; §3.4 pp21–22 список. Прочитан W1-03 extracted text; original screenshot не выполнялся этой веткой.
- **W1-08-S04** — ООО ХайТэк, «Российские решения для аппаратного ускорения работы нейронных сетей»,2026, metadata author Севрюков Сергей, [PDF](https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf), p4 benchmark, p5 model list, p6 graphics unknown. Статус: TinyFish extracted text сохранён. PDF inaccessible для web/CLI; visual p6 не проверен.
- **W1-08-S05** — sherstpasha, linq-cv-bench, commit3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140,2026-04-03, [tree](https://github.com/sherstpasha/linq-cv-bench/tree/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140). Локальный read-only checkout W1-06; git hash/metadata проверены. `.gitignore`, requirements, RUN_SCENARIO, scr READMEs. Нет публичных бинарников/measurements в просмотренном tree.
- **W1-08-S06** — тот же author/commit/date, [YOLOv8 exporter](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_yolov8s_to_onnx.py), [build](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py), [runner](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py#L206). Статус: код прочитан/AST, не executed.
- **W1-08-S07** — тот же author/commit/date, [TinyYOLO3 strict exporter](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_tiny_yolo3_strict_to_onnx.py), [TPU accuracy](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_accuracy.py), [ORT helper](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/onnx_runtime_utils.py), downloader/README. Статус: source read, weights download не выполнялся.
- **W1-08-S08** — ONNX Model Zoo, [Tiny YOLOv3 model card](https://huggingface.co/onnxmodelzoo/tiny-yolov3-11), дата не установлена, Inference/Input/Output/Validation sections. Primary card прочитана web. mAP — исходный published baseline, не LinQ.
- **W1-08-S09** — sherstpasha, тот же commit/date, [FCN exporter](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/segmentation/export_fcn_resnet50_to_onnx.py), [RUN_SCENARIO](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/RUN_SCENARIO.txt), segmentation quantize/compile/runtime and classification exporter read. Не executed.
- **W1-08-S10** — Torchvision primary docs, [fcn_resnet50](https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.segmentation.fcn_resnet50.html), live stable doc version0.29 при проверке; weights enum/preprocessing/training labels. Статус: документ прочитан. Эта live версия не установлена как версия repo автора.
- **W1-08-S11** — Ultralytics primary docs, [Model Export](https://docs.ultralytics.com/modes/export/), live doc date unknown. Статус: прочитан; содержит более новые YOLO поколения и defaults, поэтому используется только как предупреждение о дрейфе документации, не для реконструкции April2026 exporter.

