# W2-H VENDOR_FALLBACK — запасные tiny-YOLOv3 и SSD-MobileNetV2 как обучаемые цепочки; демонстрация «зоны» на вендорской COCO-программе

Модель: Claude Sonnet 5.5, effort high. Почему: прослеживание обучения и экспорта через несколько файлов в старых фреймворках (darknet/keras-yolo3, TF OD API) с выводом совместимости с вендорским контрактом. Закрывает K016.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md`, в `ROOT\CRITIC.md` — K016. Опорные: `W1-12_QUANT_LINQ.md` (F14, F16, F18 — вендорский tiny_yolo3, iva_applications), `W1-11_PRE_POST.md` (F29, 6.3 — контракт tiny_yolo3: 416 NHWC 0..1, якоря, маски), `W1-15_E2E_CHAINS.md` (R5a), `W1-06_ARCH_INFER.md` (F62, TF OD API ssd_mobilenet_v2), `W1-03_WEIGHTS.md` (TF zoo, ONNX Zoo), `W1-16_PPE_RESP_SMOKE_ZONE.md` (опасная зона). Читай FLASH `W2-B_VENDOR_CODE.md` и `W2-C_TF_PATH_SDK_ENV.md`.

Результат: `ROOT\_WORK\WAVE2\W2-H_VENDOR_FALLBACK.md` (+ `W2-H_files\`).

## Вопросы
1. **Демонстрация «зоны» без своей компиляции**: что точно нужно, чтобы запустить вендорскую `tiny_yolo3_b8_o5_128x128_asic.tpu` (COCO-80, `person`) и сделать хостовый decode/NMS + полигон (контракт выходов по W1-11-F29/iva_applications; batch 8). Напиши и проверь на CPU **хостовый декодер tiny-YOLOv3** на эталонной ONNX/Keras-модели того же семейства (например, ONNX Zoo tiny-yolov3 или keras-yolo3 веса), с явной пометкой, что это не вендорская программа.
2. **tiny-YOLOv3 на наши классы**: выбери реалистичный путь (AlexeyAB/darknet, keras-yolo3 или иной поддерживаемый в 2026 — проверь актуальность и лицензию), окружение (Python/TF/CUDA), формат меток и конвертер из YOLO-txt, команда обучения, экспорт в Keras → frozen TF GraphDef до NMS (raw heads), якоря/маски, вход 416 NHWC 0..1. Если окружение поднимается за разумное время — проверь 1–2 эпохи на construction-ppe (путь — FLASH W2-F), иначе точно опиши блокер.
3. **SSD-MobileNetV2 TF OD API**: `pipeline.config` (`num_classes`, `fine_tune_checkpoint_type: detection`), совместимость TF OD API с TF 2.14/py3.11 (deprecated-статус по W1-02), экспорт frozen graph с `output_nodes` до постпроцессинга, обучение 1 эпохи — только если реалистично; иначе блокер и оценка часов.
4. Лицензии кода и весов (darknet, keras-yolo3, TF models) кратко.

Попытайся опровергнуть: «вендорский tiny_yolo3 — надёжный запасной демо-путь» (качество person на CCTV-кадрах, batch 8, вход 416).

GPU — только через блокировку; тяжёлые окружения — в пределах диска ≤5 ГБ.
