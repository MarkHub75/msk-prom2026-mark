# W1-13 — PTQ/QAT, pruning и целевое исполнение

Исследовано: 2026-10-23, начало сетевой проверки 04:06:37 UTC / 07:06:37 Europe/Moscow. Даты публикации источников указаны отдельно. Область: стратегия компрессии детектора и проверка преобразований; SDK/runtime LinQ, target data, конкретный checkpoint и конфигурация устройства отсутствуют. Выполнены поиск и открытие первичных документов/кода; обучение, экспорт, benchmark, аренда и запуск SDK не выполнялись.

## Решение для команды

Сначала сохранить качественный FP checkpoint и доказать корректность его экспорта. Далее проверить фактический маршрут компилятора LinQ; PTQ исследовать на совместимом с этим маршрутом графе. QAT имеет смысл как отдельная гипотеза после локализации потери PTQ и получения требований целевого квантования. QDQ/QOperator — способы представления квантованного ONNX, а `.ort` — формат модели ONNX Runtime; ни одно название само по себе не устанавливает поддержку LinQ.

Публичное основание сильнее, чем простое «всё неизвестно»: LinQ действительно заявляет int8, PyTorch→ONNX→LinQ Compiler и DNN Quant. Но документы не определяют нашу версию SDK, точный opset/operator set, signedness, granularities, формат calibration и импорт QAT. Поэтому нельзя назначить ORT quantizer заменой DNN Quant или обещать, что уже квантованный ONNX будет принят.

Pruning требует различать маску нулей, физическое уменьшение плотного графа и специальный sparse runtime. Процент нулей, уменьшенный архив или FLOPs не являются доказательством ускорения устройства. Для 45-часового кейса безопасный порядок исследования: работающий компактный baseline → реальный export/target → PTQ с разбором потерь → только затем обоснованный QAT или изменение архитектуры. Это наш условный вывод, а не опубликованный результат на CCTV.

## Реестр первичных источников

Все URL ниже открыты 2026-10-23 в текущем сеансе. «Дата неизвестна» означает отсутствие установленной даты публикации/версии, а не свежесть материала.

| ID | Источник, организация, версия/дата | URL и точный локатор | Поддерживает |
|---|---|---|---|
| W1-13-S01 | Microsoft, Quantize ONNX models; unversioned web docs, дата неизвестна | https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html ; ONNX quantization representation format; Static/Dynamic Quantization; Method/Data type selection; Pre-processing; FAQ | F01–F03 |
| W1-13-S02 | Microsoft ORT source, tag `v1.23.2`; tag выбран для воспроизводимого чтения, не объявлен latest | https://raw.githubusercontent.com/microsoft/onnxruntime/v1.23.2/onnxruntime/python/tools/quantization/quantize.py ; `quantize_static`, строки 453–475 и docstring аргументов; `quantize_dynamic` | F04 |
| W1-13-S03 | Microsoft/Intel ORT source, tag `v1.23.2` | https://raw.githubusercontent.com/microsoft/onnxruntime/v1.23.2/onnxruntime/python/tools/quantization/calibrate.py ; `CalibrationMethod` 142–146; `CalibrationDataReader.get_next` 148–164 | F05 |
| W1-13-S04 | Microsoft/Intel ORT source, tag `v1.23.2` | https://raw.githubusercontent.com/microsoft/onnxruntime/v1.23.2/onnxruntime/python/tools/quantization/qdq_loss_debug.py ; module docstring 6–11; `create_weight_matching`, `modify_model_output_intermediate_tensors`, `collect_activations`, `create_activation_matching` | F06 |
| W1-13-S05 | Microsoft, ORT model format; web docs unversioned | https://onnxruntime.ai/docs/performance/model-optimizations/ort-format-models.html ; What is the ORT model format?; Convert ONNX models to ORT format, строки 187–227 | F07 |
| W1-13-S06 | PyTorch pruning tutorial, страница показывает `2.14.0+cu130`; дата страницы неизвестна | https://docs.pytorch.org/tutorials/intermediate/pruning_tutorial.html ; iterative pruning; serialization; Remove pruning re-parametrization, строки 619–684 | F08 |
| W1-13-S07 | PyTorch code, tag `v2.9.0`; это отдельная закреплённая версия, не версия tutorial | https://raw.githubusercontent.com/pytorch/pytorch/v2.9.0/torch/nn/utils/prune.py ; `BasePruningMethod.apply_mask` 47–66, `apply` 146–175; `LnStructured.compute_mask` 621–683 | F09 |
| W1-13-S08 | Jesse Cai, Daniel Haziza, Supriya Rao / PyTorch; June 20 2024, на странице также November 13 2024 без объяснения типа даты | https://pytorch.org/blog/accelerating-neural-network-training/ ; How does this work?, строки 80–97 | F10 |
| W1-13-S09 | Hao Li et al., Pruning Filters for Efficient ConvNets, ICLR 2017; arXiv v3 2017-03-10, v1 2016-08-31 | https://arxiv.org/pdf/1608.08710 ; abstract; §1; §3, особенно физическое удаление filters и feature maps | F11 |
| W1-13-S10 | Benoit Jacob et al., Google, Quantization and Training …; arXiv v1 2017-12-15 | https://arxiv.org/pdf/1712.05877 ; Fig.1.1, §2, §3 Training with simulated quantization | F12 |
| W1-13-S11 | ООО «ХайТэк», LinQ tech; дата/SDK version неизвестны | https://lin-q.ru/tech ; Собственное IP-ядро; Поддерживаемые сети, строки 45–96 | F13 |
| W1-13-S12 | ООО «ХайТэк», LinQ HPS datasheet, 4 страницы; дата/редакция PDF не установлены | https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf ; PDF p.2 «Технические характеристики», p.3 «Программный стек и инструменты», p.4 «Заказ и поддержка» (номера с 1) | F14 |

Механизмы доступа: web open HTML/raw/PDF успешны, p.3 datasheet дополнительно запрошена screenshot. CVF HTML для Jacob paper вернул HTTP 403: https://openaccess.thecvf.com/content_cvpr_2018/html/Jacob_Quantization_and_Training_CVPR_2018_paper.html . Независимый первичный путь arXiv PDF открыт успешно (S10). Экспериментальные API не запускались. Динамическая документация и закреплённый код не смешиваются в одну «текущую версию».

## Подробные факты и границы

### W1-13-F01 — Представление ONNX quantization [документация S01]

QOperator использует отдельные quantized operators, например `QLinearConv` и `MatMulInteger`. QDQ вставляет `QuantizeLinear`/`DequantizeLinear`. Документация связывает QDQ также с некоторыми экспортами QAT. Наличие QDQ не означает, что каждый оператор реально исполняется целочисленно или что выбранный backend его примет.

### W1-13-F02 — PTQ и QAT [документация S01]

Static PTQ получает activation ranges на calibration inputs; dynamic рассчитывает параметры во время inference с дополнительной работой. ORT рекомендует static для CNN, dynamic для RNN/transformers, но это рекомендация ORT. QAT предлагается при неудовлетворительном PTQ; retraining выполняется исходным framework, ORT здесь не является QAT trainer.

### W1-13-F03 — Подготовка и потеря точности [документация S01]

Shape inference и отдельная предварительная оптимизация облегчают quantization/debugging; fusion Conv+BN изменяет граф. Quantization не сохраняет точность гарантированно. Поддержка и выигрыш зависят от hardware/runtime; рекомендации S8S8/QDQ для ORT CPU не являются настройками LinQ.

### W1-13-F04 — Реальные параметры ORT `v1.23.2` [код S02, чтение без запуска]

Подпись `quantize_static`: `calibration_data_reader`, `quant_format=QuantFormat.QDQ`, `per_channel=False`, `reduce_range=False`, `activation_type=QuantType.QInt8`, `weight_type=QuantType.QInt8`, `calibrate_method=CalibrationMethod.MinMax`, `nodes_to_quantize=None`, `nodes_to_exclude=None`, `op_types_to_quantize=None`, `use_external_data_format=False`, `calibration_providers=None`, `extra_options=None`. Это установленные defaults выбранного tag, не оптимум детектора.

У API есть выбор операторов и исключения узлов: допустимо исследовать selective quantization при локализованной деградации, если target compiler допускает соответствующий mixed graph. Наличие параметра в ORT не устанавливает такую возможность LinQ. Код main из поисковой выдачи не использован для переноса новых параметров в tag.

### W1-13-F05 — Calibration data contract [код S03]

`CalibrationDataReader.get_next()` возвращает dict inputs для ONNX inference; `None` завершает итерацию. Enum выбранного tag включает `MinMax`, `Entropy`, `Percentile`, `Distribution`; список enum шире краткого веб-описания. Само наличие enum не является оценкой пользы метода или универсальной поддержкой downstream.

Аннотации не входят в этот интерфейс. Наш вывод: нужны корректные фактические model inputs; labels требуются отдельно для оценки качества и обучающего QAT loss. Calibration pool должен быть отделён от независимой проверки; подбор метода по validation делает validation частью разработки.

### W1-13-F06 — Локализация расхождения [код S04]

Модуль предназначен сравнивать веса/активации FP и quant graph на одинаковых inputs. В нём есть добавление промежуточных outputs, сбор активаций и matching. Наш вывод: сравнивать нужно одинаковую стадию графа; различия после отдельной FP-оптимизации не следует приписывать только quantization. Для LinQ доступность intermediates и соответствие tensor names ещё неизвестны.

### W1-13-F07 — `.ort` не синоним INT8 [документация S05]

ORT format предназначен в том числе для уменьшенных сборок ORT; полная сборка читает ONNX и ORT. Конвертер загружает/оптимизирует ONNX, пишет `.ort` и operator configuration для reduced build. Это отдельная ось от QDQ/QOperator и разрядности; хранить FP ONNX до такой конвертации необходимо для переносимого дальнейшего маршрута. Поддержка `.ort` LinQ не установлена.

### W1-13-F08/F09 — «Structured pruning» инструмента может означать маску [документация S06 и код S07]

Tutorial показывает `ln_structured(..., n=2, dim=0)` с занулением целых output channels. Маска и original parameters сериализуются. `remove` закрепляет pruned weight и убирает reparameterization; tutorial не утверждает уменьшение размерности слоя.

Закреплённый код подтверждает: `apply_mask` умножает original tensor на mask; `LnStructured.compute_mask` создаёт mask той же формы. Значит этот API сам по себе не делает graph surgery с удалением каналов/соединений. Даже structured mask нельзя выдавать за компактный плотный экспорт. Это наблюдение по коду, а не замер размера файла или runtime.

### W1-13-F10 — Нули и sparse kernels [авторское техническое объяснение S08]

PyTorch объясняет, что dense kernels продолжают обрабатывать занулённые элементы. Ускорение sparsity требует compressed representation и соответствующих sparse kernels. 2:4 — специальный pattern с не более двух ненулевых значений в группе четырёх; описанная аппаратная ветка относится к NVIDIA и библиотечной поддержке. Нельзя переносить её на LinQ или любой Conv graph.

### W1-13-F11 — Физическое удаление фильтров [первичная работа S09]

Работа удаляет целые filters и соответствующие feature maps, получая меньшие dense operations вместо irregular sparsity. Это основание отличать архитектурное уменьшение от маски; в статье исследуются классификационные CNN/CIFAR/ImageNet, не наш PPE detector. Числа выигрыша из abstract не используются как прогноз скорости LinQ. Для detection neck/head, residual/concat связей и малых объектов нужен отдельный корректный путь graph surgery, fine-tuning и проверки.

### W1-13-F12 — Что QAT должно моделировать [первичная работа S10]

Fig.1.1 и §3 описывают simulated quantization в FP training, включая weights и activations; inference scheme использует integer arithmetic. Метод совместно проектируется с целевой арифметикой, а не просто понижает dtype обучаемых параметров. Работа рассматривает MobileNet classification и COCO detection на CPU; она не подтверждает SDK LinQ. Наш вывод: до QAT нужны требования rounding/clipping, scales/zero points, fusion placement и поддерживаемого экспортера. Сам fake-quant checkpoint ещё не deploy artifact.

### W1-13-F13/F14 — Что публично заявляет LinQ [заявление производителя S11/S12]

Tech page называет int8 IP-ядро и включает `yolo5s`, `yolo8`, `yolo11` в список сетей. Datasheet HPS описывает PyTorch→ONNX→LinQ Compiler, DNN Quant для int8, а также Developer SDK/портал. Это публичные заявления о семействе/стеке без версии и exact model graph.

Проверенные разделы не раскрывают accepted opset, QDQ/QOperator, signedness, per-tensor/per-channel axes, calibration format/algorithm, экспорт QAT, fallback и sparse formats. SDK не получен. Слово «поддержка ONNX» не заменяет operator/version matrix. Информация HPS не устанавливает, что организаторы выдадут HPS или идентичный software stack.

## Условные маршруты

| Наблюдение | Следующее действие | Условие принятия |
|---|---|---|
| FP export уже изменяет outputs/качество | Исправить export/input/output contract до quantization | Согласованная FP цепочка; величина допуска определена по задаче |
| LinQ принимает FP ONNX и сам квантует | Сохранить FP ONNX, calibration pool и настройки DNN Quant | Получены воспроизводимые compiler log, target outputs и качество |
| LinQ требует уже квантованный граф | Получить точный sample и quantization contract | Проверен конкретный exporter/quantizer + SDK version |
| PTQ теряет критичный recall | Проверить coverage calibration, preprocessing, graph matching; затем selective quantization или QAT | Поддержка target и парная оценка, без скрытой смены порогов |
| Нужна меньшая latency, граф dense | Сравнить меньшую поддержанную модель или физически уменьшенный dense graph | Измеренная target latency и приемлемая потеря качества |
| Есть sparse kernel LinQ с известным pattern | Исследовать ровно этот pattern | Компилятор/профиль подтверждает sparse execution; иначе ветка не обоснована |

## Открытые вопросы

- **W1-13-Q01, приоритет критический → linq_platform:** какая реально выдаваемая модель устройства, SDK/compiler/runtime build, operator/opset matrix и пример входного артефакта? Меняет весь export/quant route. Закрытие: файлы SDK и успешная компиляция минимального фактического детектора, не пресс-релиз.
- **W1-13-Q02, критический → linq_platform/model_stack:** кто делает quantization — DNN Quant или внешнее средство; принимаются FP ONNX, QDQ, QOperator, QAT graphs? Каковы signedness, scales/axes, zero point, accumulation, rounding, fusion, exclusions? Нужны versioned guide, sample, compiler diagnostics. Публичный поиск этого контракта не установил; отсутствие результата не доказывает отсутствия поддержки.
- **W1-13-Q03 → datasets/evaluation:** какие камеры/сессии доступны для calibration, validation и независимой проверки, есть ли редкие состояния и мелкие объекты? Универсального числа calibration frames не назначаем. Labels для calibration inputs не обязательны по ORT API, но без labels нельзя измерить деградацию.
- **W1-13-Q04 → linq_platform/video_architecture:** какие операции реально идут на ускорителе, что остаётся на host, как получить graph placement/precision/fallback log и синхронизированное время? Скомпилированный файл и название int8 не отвечают.
- **W1-13-Q05 → model_stack:** поддержан ли QAT выбранным training/export stack именно для этого detector, и соответствует ли он Q02? Training flags не выдуманы.
- **W1-13-Q06 → linq_platform:** есть ли sparse kernels, supported pattern/layout и ограничения shapes? До подтверждения unstructured pruning оставлен исследовательским вариантом без обещания latency.

## Предлагаемые процедуры следующей практической волны

Ни одна E-процедура здесь не выполнена. Команды для неизвестного SDK не приводятся. Все допуски качества и latency следует определить с evaluation и условиями полного кейса до сравнения.

### W1-13-E01 — Парная FP→export→quant→target проверка

**Вопрос/решение:** где возникает потеря и какой артефакт пригоден для интеграции? **Входы:** выбранные model/checkpoint/exporter revisions от model_stack; неизменный class map; реальные независимые frames/clips с labels и camera/session IDs; отдельный calibration pool; SDK/device access для целевой части.

**Контроль:** одна и та же исходная картинка не гарантирует один input. Сохранить и подать одни и те же фактические input tensors (hash, dtype, shape, layout, channel order, normalization), с фиксированными decode/resize/letterbox/padding и обратным mapping координат. Если SDK требует другой input dtype, документировать преобразование и сравнивать эквивалентный контракт, не скрывать его. Зафиксировать batch, static/dynamic dimensions, eval mode, preprocessing, output names/order, logits/decoded boxes, class mapping, thresholds, NMS, top-k и coordinate convention. Не перенастраивать пороги между кандидатами в основном сравнении.

**Действия:** (1) native FP → FP ONNX; (2) FP ONNX → preprocessed FP graph; (3) тот же граф → quant graph или штатный compile/quant route; (4) фактическое target execution. Для каждой соседней пары сохранить raw outputs на одинаковых inputs; отдельно проверить общий event pipeline на тех же clips. Если target FP невозможен, native/ORT FP остаётся reference, но target delta объединяет эффекты compiler и quantization; это явно подписать.

**Метрики:** max/relative tensor deviations там, где tensors сопоставимы; detection AP с указанным IoU protocol, recall/precision по классам/size/camera, критичные пропуски; event recall/false alarms только при неизменных правилах. Считать paired differences на тех же независимых единицах, включая примеры расхождения до/после NMS.

**Артефакты:** hashes checkpoint/graphs/inputs, export args, manifests splits, calibration IDs, версии инструментов, compiler logs, placements/fallback/precision, raw outputs, metric config, визуальные пары ошибок. **Исходы:** FP export плох → чинить export; preprocessing optimization плоха → разбирать fusion; quant плох → E02; target-only плох → compiler/runtime investigation. **Stop rule:** прекратить дальнейшую компрессию при нарушенном FP parity или неизвестном input contract. **Предел:** успех ORT не подтверждает LinQ; успех на небольшой выборке не гарантирует редкие камеры/события.

### W1-13-E02 — Calibration и локализация PTQ loss перед QAT

**Гипотеза:** потеря определяется покрытием activation ranges/несколькими узлами и может быть снижена без нового training. **Входы:** прошедший E01 FP graph; calibration pool из разрешённых development cameras/sessions; validation labels; exact target quantizer contract. **Контроль:** одинаковый FP graph, inputs, split, thresholds/NMS; менять одну calibration стратегию за сравнение. Не использовать финальный holdout для выбора метода.

**Действия:** проверить представительность lighting/scale/background/positive/negative и повторов соседних кадров; сравнить несколько обоснованных subsets и доступные calibration algorithms. В ORT исследовательской ветке S03 даёт reader interface; S04 позволяет activation matching. Для LinQ использовать только полученный SDK interface. При локализованном узле проверить исключение/mixed precision лишь если target поддерживает.

**Метрики/артефакты:** из E01 плюс histogram/ranges/scales, saturation/clipping при доступности, IDs calibration frames и activation divergence. **Исходы:** устойчивое PTQ удовлетворяет критериям → оставить PTQ; loss остаётся и target QAT contract известен → E03; contract неизвестен → Q02, не запускать произвольный QAT. **Stop rule:** остановить перебор при заранее заданном лимите candidate checks или отсутствии релевантного улучшения; лимит назначить по фактическому времени. **Предел:** улучшение calibration validation ещё требует независимого подтверждения.

### W1-13-E03 — QAT или pruning как отдельное вмешательство

**Входы:** E01 baseline, установленные Q02/Q05; train labels и разрешённые development данные; для pruning — реальная graph surgery или подтверждённый sparse backend. **Контроль:** отделить QAT от дополнительного FP fine-tuning: сопоставить исходный FP, продолженное FP training с сопоставимыми данными/updates, PTQ и QAT export. Для pruning сохранить непрореженный baseline и comparable recovery training. Не менять одновременно resolution/head/classes и attribution.

**Действия:** QAT симулирует установленную target arithmetic; экспорт и прогон обязательны. Pruning фиксирует topology, pattern, удалённые channels, dependent layers; проверить shape/outputs до recovery training и повторить E01 после него. **Метрики:** качество по критичным slices; serialized bytes отдельно от package archive; parameter counts и FLOPs с convention отдельно; actual target model-only latency/peak memory отдельно от end-to-end video latency/throughput.

**Контроль времени:** одинаковые batch/concurrency/input shape, warmup, режим синхронизации, device/SDK, load, transfers и включённые стадии; latency distributions и очередь, без подмены network/RPC/decoder overhead временем модели. **Артефакты:** topology/masks, seeds/config, training checkpoint selection, quant params, compiled artifact и placement log, timing protocol. **Исходы:** меньше FLOPs без ускорения → не заявлять speedup; ускорение ценой критичного recall → отказ/другой компактный baseline; target artifact проходит оба критерия → кандидат интеграции. **Stop rule:** прекратить при несовместимости graph или неподтверждённом target pattern, до дорогого recovery training. **Предел:** локальный runtime speedup не гарантирует ускорение удалённого многокамерного сервиса.

## Адресная передача

**→ linq_platform:** F13/F14 дают проверенный public lead на DNN Quant и Compiler; получить Q01/Q02/Q04/Q06. Не сводить вопрос к «поддерживает ли ONNX»: нужен exact quant/import/execution contract.

**→ model_stack:** сохранить native FP checkpoint и FP ONNX; нужен versioned export recipe и реально поддержанный QAT route. F04 — только ORT v1.23.2 API, F09 — предупреждение о маске вместо graph surgery.

**→ datasets:** calibration pool покрывает рабочие условия и не заменяет labeled evaluation. Хранить frame/session provenance и отделять development/holdout.

**→ evaluation:** E01 разделяет FP export/graph optimization/quant/target effects; закрепить NMS/thresholds и input tensors; проверять редкие классы/малые объекты, не только aggregate AP.

**→ video_architecture:** model-only target timing и end-to-end видео — разные измерения; записывать host fallback, transfer/RPC, concurrency и queue. Нулевые веса/FLOPs/разрядность не служат proof of execution или speed.

Ветка завершена на уровне документационного решения: пригодность конкретной модели, QAT route, calibration budget и latency LinQ остаются предметом получения SDK/данных и E-процедур.

