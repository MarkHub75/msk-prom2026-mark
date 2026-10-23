# W1-05: целевые выписки и протокол доступа

Доступ 23.10.2026 примерно 04:18–04:24 MSK. Ниже короткие технические литералы и собственный пересказ; полные статьи не копируются. Локаторы — печатные страницы guide, пока без визуальной сверки. Основной результат: ../W1_05_RESULT.md.

## S01 — Framework IVA H1, 2025, RU.РМДВ.04.06.014-03 34 01

URL https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf . Независимый сетевой TinyFish fetch успешно; сравнение с уже сохранённым `_WORK/W1_03/Framework_manual_H1_extracted.txt`. Оба extraction согласуются по интересующим строкам. web open не смог получить URL (Internal Error). Это не аппаратная проверка.

Точные интерфейсные литералы (источник — API reference, не предложенный нами код):

- p7: `as_graph(batch_size=1, batch_axis=0, platform='64x64_fpga')`; описание ниже на той же странице называет default платформы `128x128_asic`.
- p7: `quantize(original_graph_def, input_shapes, output_nodes, calibration_dict, percentile=100.0, batch_axis=0, explicit_batch_value=None)`.
- p8: `original_graph_def (GraphDef)`; `tf.compat.v1.GraphDef`; `Tuple[Optional[int], ...]`; `_InMemoryQuantizedModel`.
- p9: `compile_(hardware_parameters,network,parameters,slicing_scheme=None)`; `Tuple[Executable, Dict[str, TensorDescription]]`; `get_hw_params(tpu_type)`.
- p11: `onnx_to_tf(onnx_model: onnx.ModelProto)`; `Tuple[tensorflow.Graph, Dict[str, str]]`; module `onnx_direct`.
- p12: extraction литерал `INPUT_TENSOR_NAME = ' input:1'`; возможны опечатка/extraction loss.
- p14: extraction литерал `onnx.ModeProto`; `return onnx.load(GRAPH_PATH)`.
- p19: `original_graph_def = onnx_to_tf(original_graph_def)`; `input_shapes={INPUT_TENSOR_NAME: (1, 224, 224, 3)}`.
- p20: `Network.from_quantized_model(quantized_model)`; `TpuProgram.from_executable(*tlm_program)`; `tpu_program.to_file(tpu_program_file_name)`.
- p20–21: `tpu.Device.list_devices()`; `tpu.Device.open(available_tpu_devices[0])`; `tpu_device.load(tpu_program_file_name)`; `tpu_program.inference()`; `inference.sync(input_dict_with_op_names)`.

Пересказ: p13–15 пример RGB/float32/NHWC/224² с mean subtraction и batch0. p16 rescale относится к квантованному TF-графу; runtime-пример p20 передаёт test input без явного rescale. p25 формат `.qm` — квантованная модель, `.tpu` p20 — исполняемая программа, их смешивать нельзя. p20 документ проводит границу Framework/SDK. p7–8 batch parameters не раскрывают произвольный dynamic H/W. p10 STAGING допускает плохую программу/долгую компиляцию; DEFAULT предложен для новой сети.

## S02 — /sol

URL https://lin-q.ru/sol ; web open успешно. Дата страницы не указана.

Короткая цитата (7 слов): «Интеграция PyTorch через ONNX». Числа: блок HX — PyTorch `2.0.0`, ONNX `1.15.0`, в обоих случаях нижняя граница. Собственный пересказ: блок ПО описывает Python3.8; название IVA H1 привязано к аппаратным системам LinQ H. Не экстраполировать HX-минимумы на все продукты.

## S05 — presentation2026

URL https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf ; TinyFish fetch успешно; metadata author Сергей Севрюков. p4 literals: `Ubuntu 24.04`, `TPU Runtime 16.18.6`, `TPU Framework 2026.8.43`. Это контекст измерений производителя. p4 содержит yolo5s batch1 и yolov8n_pose batch1; export settings не даны.

## S06 — HPS datasheet

URL https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf ; TinyFish fetch успешно. Extraction искажает кириллицу `/uniXXXX`; механически декодировано. Короткая цитата: «int8 (основной), в перспективе fp16/b/f_loat16». Последнее слово extraction искажено; визуально проверить bfloat16. Дата документа не установлена.

## S07–S09 — стандарты

https://onnx.ai/onnx/repo-docs/Versioning.html — Versioning Principles: собственный пересказ: IR, operator и model версии независимы; package release имеет отдельную версию. Не использовать ONNX package1.15 как opset15.

https://onnx.ai/onnx/repo-docs/IR.html — TensorShapeProto: `dim_value`, `dim_param`. Пересказ: числовая, символическая и неизвестная размерности — разные формы описания, допустимые стандартом, но поддержка backend отдельно проверяется.

https://docs.pytorch.org/docs/2.14/onnx.html — export parameter `opset_version`; правило документации: выбирать его по целевому backend/compiler. По stable произошёл redirect на эту версию; это не версия, выбранная для LinQ.

## Неработавшие URL

TinyFish errors `target_unreachable`:

- https://hi-tech.org/solutions/sol/frejmvork-fw-tpu-h-rukovodstvo-polzovatelya.pdf
- https://hi-tech.org/solutions/sol/frejmvork-fw-tpu-h-instrukcziya-po-ustanovke.pdf

Ресурсы не объявлены несуществующими; другая ветка может получить через иной канал.
