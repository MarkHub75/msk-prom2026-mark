# W1-06 — содержательные выписки и локаторы

Доступ 2026-10-23, около 04:19–04:30 Europe/Moscow. Выписки — собственный пересказ с короткими точными литералами; подробные выводы в ../W1_06_RESULT.md. Код не запускался на LinQ.

## W1-06-S01: Framework guide2025

URL https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf ; документ RU.РМДВ.04.06.014-03 34 01. Прочитан локальный extracted text W1-03 и независимо успешно получен через TinyFish.

- pp7–8: quantization создаёт SoftwareNetwork с дополнительными quant/rescale transformations и HardwareNetwork, представляющую TPU поведение в TF.
- p9: `compile_(hardware_parameters,network,parameters,slicing_scheme=None)`; `slicing_scheme` описывает размещение тензоров в памяти, не CPU fallback.
- p10: `DEFAULT`, `STAGING`. STAGING: параллельные TPU pipelines; второй DDR constants load; cache bank coexistence/lifetime/prefetch; layer fusion; flexible slicing. Предупреждение: возможны неверные программы/слишком долгая компиляция, вернуться DEFAULT и отправить bug report. Прямая короткая цитата: «Компиляция в режиме STAGING может иногда давать недопустимые программы или компилировать слишком долго».
- p11: converter ONNX→TF возвращает graph и mapping имён.
- pp19–21: .tpu содержит instructions/constants, затем аппаратный device.load/inference.sync. TF references и TLM — отдельные этапы проверки, не подтверждённый automatic fallback.

## W1-06-S02–S05: актуальные официальные страницы

- https://lin-q.ru/docs содержит direct link на framework guide; не содержит отдельной operator matrix среди извлечённых links.
- https://lin-q.ru/sol : compiler LinQ Compiler; DNN Quant и Graph Optimizer; Python3.8 API/CLI; ПО после регистрации/верификации. Это vendor description, а не точная version/API spec.
- https://lin-q.ru/tech : model-level yolo8/yolo11, без operator-level attributes.
- https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf : p4 Runtime16.18.6 / Framework2026.8.43 / Ubuntu24.04; p5 поддерживаемые семейства. Ни при каких условиях это не версия предоставленного нам SDK.

## W1-06-S06: author source code

Repository https://github.com/sherstpasha/linq-cv-bench ; pinned commit `3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140`, 2026-04-03. Clone в соседнем каталоге `linq-cv-bench`.

- `scr/detection/export_yolov8s_to_onnx.py`: default opset13, 640, batch1, export `nms=False`.
- `scr/detection/build_yolov8_program.py`:98–108 force static input `(1,3,H,W)`; 113–132 converter retry simplify True/False/no option; 170–181 DEFAULT/O1/O5 resolution; 247–300 RegularModel/calibrate/quantize/set_batch/compile. Ни одна ветка не означает CPU partitioning.
- `scr/detection/run_yolov8_tpu.py`:109–112 inference.sync; 279–290 host non_max_suppression после получения output. Timer ограничивает TPU call; NMS дальше.
- `RUN_SCENARIO.txt`:12–44 real TPU env/device requirement; 275–290 fallback ModelZoo — CPU/CUDA baseline, не fallback оператора TPU.
- `requirements.txt`: отсутствуют vendor SDK и ultralytics; `scr/README.md` требует SDK отдельно.
- AST local check: строка206 содержит `args.output_tens\u0e2d\u0e23\u0e4c_name`; ascii=False. Parser destination `output_tensor_name` отличается. Локально проверен AST, не execution. Ожидаемый AttributeError — вывод из кода.

## W1-06-S07: historical custom compiler automation

https://github.com/sttell/IVA_compiler_runner/tree/543ab4a0e53b4efb851af5c592f8089b5685ec70 ; 2022-04-03. Clone `IVA_compiler_runner`.

`include/compile_errors.h`: авторские JSON/weights/padding/input/output errors, не официальный современный LinQ error catalogue. `lib/compiler_core/src/modules/compiler_runner/compilerRunnerModule.cpp`: external command orchestration. Отсутствует доказательство связи этой реализации с LinQ2026; для текущей operator support не использовано.

## Search/access log

Web search: LinQ Compiler; dnn_quant; onnx_direct; IVA TPU compiler github; tpu_framework compiler; LinQ NMS; domain LinQ/hi-tech + operators. GitHub repo search IVA TPU → S07. GitHub code search onnx_direct onnx_to_tf / TPU_128x128_PARAMS → S06. General search содержит много нерелевантного .NET LINQ, отсеяно.

web.open /docs и два PDF → inaccessible; TinyFish те же современные URL → success. TinyFish старый hi-tech guide → target_unreachable. github_fetch users endpoint → unsupported URL, профиль прочитан web. Доступность ресурсов проверена, аппаратное исполнение не проверено.
