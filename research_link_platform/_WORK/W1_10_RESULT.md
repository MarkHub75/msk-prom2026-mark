# W1-10 — видео, tensor contracts и граница аппаратного inference

Дата исследования: 23.10.2026, фактические операции около 04:26–04:35 Europe/Moscow. Вопрос: что именно получает и возвращает LinQ, какие преобразования делает host, и как отделить ошибку адаптера от потери точности квантования и от ограничений видеосервиса?

## Вывод для команды

Документ 2025 явно ставит границу между Framework и SDK на файле `.tpu`; приложение отдельно готовит словарь тензоров и отдельно интерпретирует результат. Доступный сторонний код 2026 подтверждает такую архитектуру примеров: чтение картинок, letterbox, RGB conversion, normalization, NMS, возвращение координат и запись результатов выполняются Python/NumPy/OpenCV/PyTorch на host. Это описание конкретных примеров, а не запрет выполнять часть этих операций внутри другого поддерживаемого графа. Подтверждённого RTSP → decode → inference → tracker demo LinQ среди прочитанных материалов нет. Поддержка decode и готовая видеоплатформа — незакрытый вопрос поставки.

Практический минимальный путь: получить готовый `.tpu` и его **явный входной/выходной контракт**, сделать replay одного и того же сохранённого тензора через reference и LinQ; только после этого подключать video decode и tracking. Название YOLO, число каналов, успешный вызов runtime и похожие bounding boxes контракт не заменяют. Сторонний `linq-cv-bench` — полезная карта интерфейсов, но требует проверки и исправлений: обнаружены ошибочное имя аргумента YOLOv8 и отдельный дефект определения uint8 в helper auxiliary inputs.

## Источники и область применимости

Все URL ниже проверялись или сопоставлялись с локальным pinned checkout 23.10.2026. S02–S08 — первичный авторский исходный код **стороннего** sherstpasha, связь с производителем не установлена. Общая версия этих файлов: commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, дата commit 03.04.2026 по материалам W1-06; локально выполнен `git rev-parse HEAD`, совпадение подтверждено. Код прочитан, но модели не экспортировались, не компилировались и на TPU не запускались.

| ID | Источник, автор, URL, locator | Статус и ограничения |
|---|---|---|
| W1-10-S01 | Производитель LinQ, «Руководство оператора», RU.РМДВ.04.06.014-03 34 01, 2025. [PDF](https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf), печатные стр.13,15–21; локальная копия текста `_WORK/W1_03/Framework_manual_H1_extracted.txt` | Прочитан извлечённый текст. Повторный web open PDF вернул Internal Error; визуальная сверка PDF мной не выполнена. В тексте есть опечатки/артефакты: не использовать код как гарантированно исполняемый. Это версия 2025, не обещание интерфейса runtime хакатона. |
| W1-10-S02 | sherstpasha, [coco_utils.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/coco_utils.py#L18), lines18–40 | Прочитан локально и через raw web; геометрия дополнительно проверена формулами без OpenCV. |
| W1-10-S03 | sherstpasha, [run_yolov8_tpu.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_tpu.py), funcs `run_once`, `normalize_prediction_shape`, `main`, lines176–310 | Локальное чтение и web open; AST-проверка опечатки. Не было аппаратного запуска. |
| W1-10-S04 | sherstpasha, [run_yolov8_onnx.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_yolov8_onnx.py), funcs `make_batch`, `main` | Прочитан локально, ONNX Runtime не запускался. |
| W1-10-S05 | sherstpasha, [export_yolov8s_to_onnx.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/export_yolov8s_to_onnx.py), `main`; [build_yolov8_program.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/build_yolov8_program.py#L46), `preprocess_yolo` | Прочитаны локально; exporter default opset13, imgsz640, batch1, nms=False; не запускались. |
| W1-10-S06 | sherstpasha, [run_tiny_yolo3_accuracy.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_accuracy.py), lines137,269,309,404,415,446,492,562,770 | Прочитан локально. Изолированно выполнен только helper `infer_desc_dtype`. Артефакт с «vendor» в имени этим не становится официальным SDK. |
| W1-10-S07 | sherstpasha, [run_tiny_yolo3_vendor.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/detection/run_tiny_yolo3_vendor.py), DEFAULT_* и CLI | Прочитан локально; бинарный `.tpu` не верифицирован. |
| W1-10-S08 | sherstpasha, [run_fcn_resnet50_accuracy.py](https://github.com/sherstpasha/linq-cv-bench/blob/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140/scr/segmentation/run_fcn_resnet50_accuracy.py), lines16–17,82,199,210,282–298 | Прочитан локально; результат/маски не получались. |
| W1-10-S09 | LinQ, [Модули ускорения LinQ](https://lin-q.ru/sol), разделы HPS / HX / Программное обеспечение; дата страницы не установлена | Страница открыта web 23.10.2026, около04:28. Только vendor_statement, не проверка наличия компонентов в поставке. |
| W1-10-S10 | Ultralytics, [utils.nms API](https://docs.ultralytics.com/reference/utils/nms/), non_max_suppression; rolling docs, дата версии не зафиксирована | Открыта web 23.10.2026. Используется только для подтверждения отдельного API NMS; точная версия установленного в repo Ultralytics неизвестна. |
| W1-10-S11 | OpenCV, [VideoCapture Class Reference](https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html), read/retrieve/getBackendName | Открыто web; redirect на документацию4.13.0. read включает grab и decode; это документация OpenCV, не наличие VideoCapture-интеграции LinQ. |

## Подробные факты и инженерные последствия

### F01. Официальный пример 2025 показывает границу до и после графа

Тип: primary_documentation. Проверка: прочитан локальный extracted guide, не аппаратный тест. Основание S01, стр.13,15–21.

В классификационном примере preprocessing предоставляет пользователь вместе с исходной моделью: PIL RGB; центральный квадрат со стороной `int(min(H,W)*0.85)`; resize224×224; float32; вычитание по RGB `[123.68,116.779,103.939]`; batch axis0. Формат `NHWC`, input shape `(1,224,224,3)`. Это **не** стандартный рецепт для всех LinQ/YOLO: здесь нет деления на255 и нет NCHW. Postprocess — индекс `argmax + 1` (классы примера нумеруются с1). Его применение к другому model zoo может дать систематическое смещение категории.

Тот же preprocess используется для калибровки и тестового изображения. Guide последовательно сравнивает исходный TensorFlow, квантованную модель, TLM и TPU через общую проверку ожидаемого класса; для quantized graph вход/выход проводят через `quantized_model.rescale`. При этом в примере `inference.sync` получает исходный словарь preprocess, без отдельного явного `rescale` в пользовательском hardware-call. **Вывод inference:** нельзя автоматически кормить int8 только потому, что вычислитель int8, и нельзя добавлять rescale поверх runtime без выяснения его контракта. Из одного walkthrough неизвестны все правила dtype/scales конкретного нового `.tpu`.

Guide явно называет `.tpu` границей Framework/SDK: Framework получает исходную модель, SDK загружает программу и исполняет заданные данные. Демонстрация использует `Device.list_devices → Device.open → device.load → program.inference → inference.sync`. Входы/выходы — словари. TensorFlow tensor name с `:0` преобразуется в operation name для TLM/runtime; это соглашение примера, не основание удалять произвольный суффикс во всех экспортерах. Извлечённый input literal выглядит как `' input:1'`, а helper удаляет лишь `:0`: из-за качества текста не фиксировать это как реальное обязательное input name.

Guide проверяет top1 на одном примере и печатает top16; этого недостаточно для доказательства численной эквивалентности, mAP или видеостабильности. TLM time является оценкой, не измерением end-to-end приложения.

### F02. Точный общий letterbox pinned repo

Тип: source_code; проверка: чтение S02, формулы проверены локально. Для конкретных detection runners:

1. По изображению H×W вычисляется `r=min(S/H,S/W)`; resized size `(round(W*r), round(H*r))`, Python `round`.
2. `cv2.resize(...,INTER_LINEAR)`, полотно строго S×S. `dw=S-new_w`, `dh=S-new_h`; слева `dw//2`, справа остаток; сверху `dh//2`, снизу остаток. При нечётном padding дополнительный пиксель справа/снизу. Это не auto-stride letterbox и не растягивание изображения к квадрату.
3. Constant border `(114,114,114)`. Helper возвращает **номинальный** r и целочисленные left/top. Нет ограничителя scaleup: маленькие кадры могут увеличиваться.

Локальная проверка формул S=640: 1920×1080 →640×360, top/bottom140; 641×479 →640×478, top/bottom81. Во втором случае реальные масштабы x/y после округления немного отличаются, но код сохраняет единый r. Для воспроизведения именно этого примера inverse mapping должен повторять его r; для нового адаптера геометрическую конвенцию нужно зафиксировать и проверить. Это не установленная ошибка LinQ и не аппаратная численная проверка. OpenCV локально отсутствует, пиксельная интерполяция не выполнялась.

### F03. YOLOv8 boundary: RGB float NCHW и host NMS

Тип: source_code. Проверка: чтение S03–S05, исполнение модели не выполнено.

При default640 оба TPU и ONNX runner используют `cv2.imread → letterbox → [:,:,::-1] → transpose(2,0,1) → float32/255 → expand_dims`. На runtime передаётся batch `[B,3,640,640]`, RGB unit float. Build calibration `preprocess_yolo` повторяет этот путь. Не нужно менять layout на NHWC по аналогии с guide2025: это разные модели и конверсия должна сохранять контракт конкретного экспорта.

Exporter задаёт `nms=False`. Runner ожидает rank3, ось каналов84 или85, при необходимости транспонирует в `[B,C,N]`. Это только эвристическая проверка формы; она не доказывает порядок координат, наличие objectness, степень декодирования, число классов, отсутствие sigmoid в графе или семантику85 каналов. Выход по умолчанию выбирается из build summary либо эвристикой «единственный / первый rank≥3 ndarray». В multi-output графе следует требовать точное имя и семантику каждого выхода.

Вызов runtime возвращает NumPy, далее `torch.from_numpy(pred)` и `ultralytics.utils.nms.non_max_suppression(conf=0.001,iou=0.65,max_det=300)` выполняются **после** таймера. Torch tensor создан на host, явного CUDA transfer нет. Указанные thresholds — evaluation defaults конкретного repo, не рекомендуемые product thresholds. Точная версия Ultralytics не закреплена и здесь не установлена: одних84/85 каналов недостаточно, чтобы безопасно смешивать разные YOLO heads.

После NMS код считает координаты xyxy в пикселях input canvas: x=(x-pad_x)/r, y=(y-pad_y)/r, clamp к `[0,W-1]`/`[0,H-1]`; затем переводит к COCO top-left xywh. Боксы шириной/высотой≤1 отбрасываются, class index0..79 переводится в COCO category id через COCO80_TO_91 (в id есть пропуски). Это важно для tracker/event слоя: нельзя передавать туда canvas coordinates или COCO id как непрерывный class index.

Batch helper добивает неполный batch повтором последнего изображения; декодируются лишь реальные строки metas. Файл `_b8.tpu` означает попытку исполнения fixed batch8, а не 8 независимых RTSP pipelines. Нужно сопоставить каждой строке реальные camera/frame/timestamp и исключить padded copies из результатов.

### F04. YOLOv8 пример в pinned состоянии нельзя объявлять runnable

Тип: source_code + local_observation. S03 line206 обращается к `args.output_tens\u0e2d\u0e23\u0e4c_name`, parser определяет `output_tensor_name`. Изолированный AST probe проверил отсутствие первого атрибута у `argparse.Namespace(output_tensor_name=None)`. Если выполнение дошло до этой строки (есть program/dependencies/COCO), будет AttributeError; строка предшествует `Device.list_devices/open`. Полный скрипт не запускался и мог бы раньше упасть по отсутствующим файлам/зависимостям. Это дефект стороннего примера, не доказательство дефекта SDK.

### F05. TinyYOLO3: два принципиально разных output contracts

Тип: source_code; проверка: прочитан S06–S07, не hardware run. Default runner: `S=416`, NHWC, RGB float32/255, batch8, input name `input_1:0`; возможны CLI `nchw`/`uint8`, но это переключатели приложения, а не доказанная поддержка любого layout/range бинарником. Название `.tpu` с `128x128` не равно размеру картинки416×416: без tensor metadata нельзя читать размеры входа из filename.

`decode_predictions` сначала пробует rank3 combined output с85 значениями/кандидат: boxes предполагаются уже decoded center-xywh, а objectness и classes — logits, к ним применяется sigmoid, score=obj×cls. Затем host class-aware `torchvision.ops.batched_nms`, inverse-letterbox и COCO mapping. Если binary уже выдаёт вероятности или нормализованные boxes, форма может пройти, но обработка будет семантически неправильной. Наличие sigmoid/диапазоны нужно сверять с graph/artifact, не угадывать по rank.

Альтернативный путь raw heads принимает rank4 NCHW/NHWC с каналами, кратными85; переводит в `[B,A,Hg,Wg,85]`, сортирует головы по grid height, использует anchors `10,14 23,27 37,58 81,82 135,169 344,319`, masks `3,4,5|0,1,2`. На host вычисляет `xy=(sigmoid(txy)+grid)*stride`, `wh=exp(twh)*anchor`, sigmoid(objectness/classes), scores, NMS, координаты. Здесь `stride=S/grid_height` используется по обеим осям: код рассчитан на квадратный вариант, не произвольную прямоугольную голову. Эти формулы доказывают реальный перенос **head decode** на host в данном пути, а не только NMS.

Выбор combined/head по размерности с перехватом исключений — адаптационная эвристика. Для результата хакатона нужен adapter с одним установленным вариантом и fail-fast при несовпадении; тихое переключение ветки может скрыть ошибку версии/выхода. Отсутствие ветки уже-NMS outputs `[B,N,6]` не означает отсутствие такой возможности у LinQ.

### F06. Auxiliary input нельзя подбирать только по имени и успешности вызова

Тип: source_code + local_observation/inference; S06 funcs269,290,309,337.

Runner пробует input names с/без `:0`, introspection полей и стандартные guesses. При тексте ошибки `Missing required input tensor "..."` строит auxiliary inputs. Если имя содержит `shape`, использует H,W оригинальных изображений; размер2 → H,W **первой** картинки; размер2B → rows для каждой картинки; размер1 → S. Иные размеры дополняются нулями; non-shape inputs заполняются нулями. Не установлено, требуют ли конкретные binaries original-shape, resized-shape, canvas-shape, W,H или H,W. Успех runtime удостоверяет структурную приемлемость feed, но не правильность семантики.

В `infer_desc_dtype` substring `int8` проверяется раньше `uint8`. Локальный изолированный вызов с `{'dtype':'uint8'}` вернул `int8` (NumPy2.4.2). Это воспроизведённый helper defect, **только** для helper auto auxiliary dtype; основной explicit preprocessing uint8 использует `np.uint8` напрямую. Кроме того, значение поля `size` helper сначала интерпретирует как bytes, если кратно dtype.itemsize; без schema это неоднозначно — SDK может обозначать число элементов. Это риск адаптера, не установленный SDK bug.

### F07. Segmentation подтверждает, что «общего LinQ preprocess» нет

Тип: source_code; S08. RGB PIL → bilinear **stretch** к width×height (defaults520×520), `/255`, channel normalization mean `[0.485,0.456,0.406]`, std `[0.229,0.224,0.225]`, NCHW float32. Нет letterbox. На host из logits выбирается class axis, argmax → uint8 mask, затем nearest resize до исходного H×W. Argmax-before-resize и resize-logits-before-argmax не обязаны давать один результат на границах: эталон должен повторять точный порядок. Fallback class axis=smallest dimension — эвристика, не безопасный контракт произвольного output tensor. Возвращаемая маска не содержит instance IDs или temporal identity.

### F08. Открытые показатели runner не означают RTSP throughput

Тип: source_code + inference. В S03 timer ограничен `run_once`; чтение файла, letterbox/batch assembly, NMS, координаты, JSON вне него. S06 и S08 устроены аналогично. Даже такое время нельзя без runtime trace назвать временем **только вычислителя**: синхронный вызов может включать driver/data transfer/host conversions. S03 принимает `.run` если существует, иначе `.sync`; семантика блокирования первого не документирована прочитанным guide, который использует sync. Следует отдельно подтвердить completion/fencing перед timing.

У warmup есть пограничный эффект: если warmup10 пересекается с batch8, второй batch целиком входит во время, но в числитель measured images идёт6. Последний padded batch может исполнять8 копий при меньшем числе реальных кадров. Это не чистый hardware throughput и не линейная оценка stream capacity. В repo `rg` по `VideoCapture|rtsp|track|avcodec|ffmpeg|gstreamer` совпадений не дал; анализировались image-dataset runners. Отрицательный результат ограничен этим checkout, не всей экосистемой.

### F09. Decode относится к конкретной конфигурации, tracking остаётся незакрытым

Тип: vendor_statement по S09; проверка: страница прочитана web. У HPS аппаратное **видеокодирование** перечислено как дополнительная ASIC-опция; это не обещание decode на LinQ H. У HX функции decoder перечислены в CPU-секции рядом с RK3588; TPU отделён. Отсюда inference: нельзя переносить эти функции на PCIe-модуль или обещанный cloud endpoint. Нужны точные product/BOM/API. В прочитанных guide/code не найден API track IDs, RTSP reconnect, ordering или rule engine.

OpenCV VideoCapture.read согласно S11 включает grab и decode. Поэтому добавление `cap.read()` в приложение добавит отдельную стоимость/буферизацию; измерение только inference не учитывает её. Это свойство API OpenCV, а не выбранный обязательный decoder. Для host MVP разумна явная цепочка `source → decode → frame metadata → preprocess → tensor inference → postprocess → per-camera tracker → rules → UI` (inference/recommendation, пока не реализация).

## Предлагаемый тест эквивалентности и его границы

Ниже эксперименты **не выполнены**, это конкретный handoff, не заявление о готовой работоспособности.

**E01: контракт поставленного артефакта.** Сохранить `.tpu`, исходные веса/export/graph/calibration config hashes, SDK/runtime/driver versions, device, все input/output names, shapes/layout/dtypes/scales, units/ranges, batch axis/static B, original coordinate convention. Узнать, включает ли граф normalize, head decode, sigmoid, NMS. Выгрузка actual metadata важнее filename и heuristics. Зафиксировать лицензию/доступность исходных весов отдельно с W1-08.

**E02: offline golden tensors.** Выбрать10–20 фиксированных изображений: portrait/landscape, odd dimensions/padding, RGB patches, маленький объект у границы, crowded/empty scene. Один раз декодировать их фиксированным backend/version и сохранить decoded frame, preprocessing tensor `.npy`, r/new_w/new_h/left/top, camera/frame ids. Exact equality input tensors ожидается только при одинаковом implementation/backend; смена Pillow↔OpenCV/interpolation — отдельный эксперимент, не молчаливый переход. Если сравнивают экспортированные ONNX и `.tpu`, feed должен быть сохранённым **одним** тензором; layout conversion фиксируется отдельно. Не перекодировать JPEG заново для каждой стороны.

**E03: лестница локализации расхождения.** Source framework FP32 → ONNX Runtime → quantized/reference graph → TLM → device, насколько эти уровни доступны в выданном SDK. Записать raw outputs до postprocess на одном и том же tensor, names/shapes/dtype/min/max/NaN. Для FP32 conversion сравнить max/mean absolute error и relative error с epsilon; для quantized/device не требовать bitwise FP32 equality, проверить scales, saturation и task accuracy. Численные допуски согласовать по baseline, заранее не обещать «1e-3» для любых моделей. Если original/ONNX расходятся — разбирать export; quantized/TLM — lowering/quantization; TLM/device — target/runtime; одинаковые raw outputs и разные boxes — host adapter. Уровни могут отсутствовать в новой версии — тогда сохранить missing checkpoint.

**E04: postprocess отдельно.** Одни raw outputs отправить в один pinned host postprocessor для всех backends. Для YOLO сравнивать matching по class+IoU и координатам, score deltas, count/duplicate/missing; порядок NMS rows не является устойчивым идентификатором. Threshold-near и одинаковые scores могут менять NMS дискретно; прикладывать raw candidates. Synthetic boxes проверяют center→corner, inverse letterbox, clipping, COCO class mapping, masks/anchors и отсутствие double sigmoid/NMS. Для segmentation — идентичный argmax/resize порядок и mIoU на одном наборе. Только task-level metric на репрезентативной выборке оценивает приемлемую потерю; один успешный класс из guide не заменяет её.

**E05: video replay и tracking.** Сперва фиксированный короткий clip и последовательность decoded frames с timestamps; никаких live network вариаций между сравниваемыми backend. Проверять stream/frame identity, порядок, padded-row exclusion, единый original coordinate space. Tracker state отдельный на camera, обновление по фактическому timestamp/пропуску кадров, reconnect/reset policy явная. Track IDs не следует сравнивать численно между независимыми прогонами: оценивать непрерывность/переключения/события после согласованного matching. Затем live RTSP: логировать ingress/decode/queue/infer/post/track/event times, frame age p50/p95/p99, dropped frames, queue length, decode failures/reconnects. Ограничить очередь и объявить discard policy; медленный host postprocess может накапливать устаревшие кадры при хорошем inference FPS.

**E06: honest performance.** Раздельно: model service time sync call; host preprocess/NMS; end-to-end from frame arrival to event/UI; число реально обработанных кадров на camera/sec. Указать streams, resolution, codec, decode backend, FPS sampling, batch formation wait, host CPU, transfers, warmup batches. Для online cloud добавлять RPC serialization/network/queue; локальный pytpu `Device.open` не доказывает remote API. Не считать padded repeats полезными кадрами. Установка RTX4070 сама по себе не доказывает доступность или zero-copy decode; это отдельная конфигурация и проверка.

## Противоречия и неизвестные

- Guide2025 NHWC/crop/mean-subtraction и YOLOv8 NCHW/letterbox/unit-float не противоречат друг другу: относятся к разным моделям. Их смешение — опасная ошибка интеграции.
- Padding114 repo против128 model-card, BGR/RGB TinyYOLO ONNX vs TPU уже разобраны W1-08. В этой ветке не объявляется ни один вариант универсально правильным: нужна связь binary↔weights↔recipe. Смещение канала может менять точность без runtime error.
- Guide2025 Python3.11 и /sol Python3.8, более новый benchmark Framework2026.8.43/Runtime16.18.6 (передано W1-03) — разные версии источников. Совместимость и контракт выданного SDK не установлены.
- Нет установленного знания о аппаратном decode, resize, color conversion, NMS, tracking для **поставки хакатона**; наличие host операций в repo не доказывает отсутствие device alternatives. Требуется official artifact-specific пример или profiling trace.
- Не получены runtime metadata реального `.tpu`, stream API, DMA/zero-copy/shared memory layout, асинхронная completion semantics, input auxiliary schemas, batching между streams, stateful tracker support, cloud transport contract.
- Неполные dependencies/нет SDK и артефактов в git — известное ограничение воспроизводимости W1-06. Локально нет cv2; никаких pixel preprocessing, экспорта, компиляции, inference, mAP/FPS тестов здесь не проводилось.

## Поиск, доступ и сохранённые локальные проверки

Прочитаны разделы7/9/11 исходного research prompt. Сделан собственный web open официальных `/docs`, guidePDF, `/sol`, pinned GitHub и raw helper; поисковые запросы `site:lin-q.ru RTSP video декодирование preprocessing`, `site:lin-q.ru "NMS"`, `site:github.com "pytpu" "VideoCapture"`. Полезный direct hit — `/sol`; конкретного LinQ RTSP/tracker API эти запросы не выявили. `/docs` и PDF через web дали Internal Error, в то время как `/sol` и GitHub открылись. Это ограничение инструмента, не отсутствие документации. Alternative: уже полученный W1-03 extracted text guide; его прочитал самостоятельно. Повторно скачивать исторические guides не потребовалось, потому что новая точная граница найдена в2025 guide и pinned2026 code.

`_WORK/W1_10/CONTRACT_PROBES.py` и `CONTRACT_PROBES_RESULT.json` содержат воспроизводимые локальные проверки AST/NumPy helper и геометрии формул. Исходный checkout не изменялся. Первый запуск вывода упал на Windows cp1251 при печати тайских символов; исправлено escaping JSON и повторный запуск успешен. Это ошибка вывода исследовательского probe, не целевого repo. Команда `import numpy,cv2` обнаружила отсутствие cv2; NumPy2.4.2 имеется. Никакая зависимость не устанавливалась.

## Передача оркестратору

1. Использовать официальную `.tpu` Framework/SDK boundary как основу архитектуры, но запросить актуальный tensor contract выданной модели.
2. Для realtime сервиса гарантирован пока лишь условный tensor-inference путь; decode/host pre/post/NMS/tracking и network считать отдельными бюджетами.
3. Дополнительно к W1-08 подтверждён новейший локальный helper defect `uint8→int8`; adaptive auxiliary feed по имени/размеру не годится как установленный contract.
4. Лучший первый smoke test — replay сохранённого input tensor и raw output, затем единый postprocessor. Он быстрее локализует проблему, чем подключение RTSP с нефиксированными кадрами.
5. Нужен ответ поставщика: exact `.tpu` metadata + preprocessing/postprocessing reference; есть ли поддерживаемый video/cloud пример; где завершение async/sync и какие части входят в latency. Не откладывать host tracker/UI на ожидание неопубликованного видео SDK.
