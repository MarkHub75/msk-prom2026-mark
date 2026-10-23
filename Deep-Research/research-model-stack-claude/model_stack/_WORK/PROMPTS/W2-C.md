# W2-C TF_PATH_SDK_ENV — собственный TF GraphDef (NHWC) и LinQ-подобное окружение

Модель: Claude Opus 5.5, effort medium. Почему Opus: согласование нескольких промежуточных форматов (PyTorch → ONNX → TF GraphDef/SavedModel) с разными раскладками и версиями TF/onnx/numpy, плюс отдельное окружение под требования SDK — класс задач «несколько несовместимых промежуточных форматов». Закрывает K001, K002.

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md`, в `ROOT\CRITIC.md` — K001, K002, K004, проверку 5 в шапке. Опорные: мануал `W1-12_files\Framework_manual_H1.txt` (стр. 87–90, 131–169, 340–370, 521–540), `W1-10_EXPORT_ONNX.md` и `W1-10_files\` (скрипты, op_matrix, freeze), `W1-09_ENVIRONMENTS.md` (F03, «Диагностика машин», F30 про WSL/Docker), `W1-12_QUANT_LINQ.md` (S07 — requirements стенда), `W1-15_E2E_CHAINS.md` (R5a, C7, F20, F26). Читай FLASH `ROOT\_WORK\WAVE2\W2-D_FIRST_HOUR_KIT.md` (номенклатура графов) и `W2-B_VENDOR_CODE.md` (API).

Результат: `ROOT\_WORK\WAVE2\W2-C_TF_PATH_SDK_ENV.md` (+ `W2-C_files\`: lock-файлы, инвентари TF-операций, логи).

## Вопросы
1. **LinQ-подобное окружение**: Ubuntu 20.04 (Docker `ubuntu:20.04` с Docker Desktop или WSL2 — выбери реалистичный путь, зафиксируй), Python 3.11 (и, если быстро, 3.8 как резерв), `tensorflow==2.14.1`, `onnx~=1.16.0`, `onnxruntime~=1.18.0`, `numpy==1.26.4` (по requirements стенда — проверь первичный файл). Протокол: время установки, lock-файл, `onnx.checker` и загрузка в ORT 1.18 графов W1-10 (IR 8/opset 18 и raw opset 13) — что открывается, что нет; импорт TF. Что из этого наша команда должна иметь готовым до 13:00.
2. **Собственный TF-граф** для yolov8n, yolo11n, yolov5s (v7.0 или master — согласуй с W2-G FLASH), yolov8n-pose и mobilenet_v2: документированные пути — Ultralytics `export(format="saved_model")`/`"pb"` (что внутри использует — onnx2tf? проверь по коду 8.4.184 и зафиксируй версии), прямой onnx2tf, иные (onnx-tf — устарел? проверь статус). Получить frozen GraphDef с NHWC-входом; список TF-операций; загрузить через `tf.compat.v1.GraphDef().ParseFromString` и выполнить `tf.compat.v1.Session`, как в примере мануала; численно сравнить с ONNX/PT на одном тензоре (допуски по протоколу W1-11 §6.5).
3. Какие варианты головы (full / raw — номенклатура W2-D) переводятся в TF без потерь и какие операции появляются (Transpose, StridedSlice, SplitV, ResizeNearestNeighbor, BatchMatMul и т.п.). Что меняется с раскладкой (вход NHWC, внутренние транспонирования).
4. Где пролегает граница: что мы не можем проверить без вендорского `onnx_to_tf` (это не тот же конвертер) — сформулируй точные вопросы → linq_platform.

Попытайся опровергнуть: «TF-путь — надёжный запасной вариант». Найди условия, при которых он хуже ONNX-пути (например, лишние Transpose, неподдерживаемые TF-операции в TF 2.14, несовпадение версий).

Ограничения: тяжёлые образы/колёса — разумно; GPU не нужен. Диск ≤ 5 ГБ в SCRATCH (Docker-образы считаются — после работы удалить ненужные образы и записать, что удалено).
