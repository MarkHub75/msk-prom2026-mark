# W2-E: vendor TinyYOLO3 provenance и сравнимость pre/post веток

# Second-wave researcher contract

Actual role gpt-6.1-sol medium, fork_turns none. Work folder D:/msk-prom2026-mark/research_link_platform. Read the original task, CRITIC.md and assigned W1/source files before the new investigation. Five experienced developers; 45-hour hackathon; mandatory LinQ inference, online mode/SDK/device SKU still unconfirmed unless RUN_STATE records a later actual grant. This is research, not a submission prototype. Historical context night23Oct2026; record actual access date/time separately.

You own only _WORK/W2_E_RESULT.md and auxiliary _WORK/W2_E/. Use uppercase names for new working artifacts; preserve downloaded original filenames. Do not modify final evidence/reports/critique. Do not delegate. Independently use actual network search/open/fetch plus bounded local source inspection where useful. Consult primary source or authors, pin source/version, do not rely on repeated snippets. Reuse saved evidence without duplicating broad W1 search. Registration/user interaction is owned by root; do not sign up/send messages/use credentials. No resources rented, SDK installed or device job run without concrete new authorization/context.

Every W2 task is tied to K IDs and a missing decision-changing answer. Attempt to falsify the provisional claim and identify limiting conditions, rather than finding one agreeable URL. A closed SDK or failed fetch is a narrow unknown, not a reason to stop unrelated work. Test alternate available retrieval channels when useful, and record actual method/time/status. Never call inaccessible material nonexistent. If a full artifact is unavailable, distinguish metadata/abstract/indexed or cached copy from live binary/source contents. Follow PDF skill if working with PDF; actual screenshot must be seen, a returned link alone is not visual inspection.

Result format: assigned question/K IDs; decision and findings; detailed local facts with W2-E-Fxx/source W2-E-Sxx; direct URLs/titles/authors/document dates/access times/locators; exact code versions/literals/configuration; evidence type separate from actual test status; negative attempts and contradictions; remaining unknowns with resolution path; concrete future experiments and compact root handoff. Clarify what changed from W1 and what did not. Partial script/helper probes are not SDK/compile/device validation. No invented API/CLI/operator/opset/calibration details. Do not copy full articles; use factual paraphrases and brief compliant quotations.

Completion is a useful established answer or precisely localized unknown after sufficient targeted search, not a source quota. Preserve depth and full details on disk, send root only consequential findings and completion.


## Индивидуальное задание оркестратора по критике

- **K:** K007,K006,K019. Решение: пригоден ли vendor detector как ранний smoke и как сравнивать его quality.
- **Старт:** `tiny_yolo3_b8_o5_128x128_asic.tpu` path; strict Darknet exporter; ONNX Model Zoo card; `iva_applications11.0.1` source и LICENSE в архиве.
- **Новый поиск/анализ:** actual vendor artifact/weights/recipe or matched package; точный anchors/order/names/scales, RGB/BGR, padding/interpolation and inverse geometry; old MIT decoder b1/255 restrictions. Не скачивать большие датасеты/не проводить benchmark.
- **Фальсификация:** проверить, не неверен ли именно RGB runtime; не подменён ли baseline другим graph с embedded NMS/second input.
- **Выход:** three-path manifest с parity/non-parity verdict по каждому шву; golden tensors/raw outputs specification и небольшой воспроизводимый host-only probe при необходимости. Нельзя заявлять общие веса без hash/source.


## Исходные замечания (не считать уже закрытыми)
### K007 — vendor TinyYOLO3, strict export и Model Zoo остаются тремя непаритетными моделями (P0)

**Проблема/область.** W1-08-F07, W1-10-F05/06, repo TinyYOLO files. Vendor `.tpu` отсутствует; strict export даёт BGR metadata, ORT helper не применяет `image_color_order`; TPU runner делает RGB; Model Zoo имеет другой I/O/NMS и recipe. Дополнительное чтение критика: `iva_applications==11.0.1/tiny_yolo3/postprocess.py` жёстко assert `(1,13,13,255)` и `(1,26,26,255)`. Его MIT наличие не делает его готовым b8/custom-N decoder.

**Последствие.** Измеренная разница AP или FPS будет смесью цветов/весов/head boundary/NMS, а не эффектом quantization/LinQ. Vendor smoke test не докажет путь собственного PPE training.

**Нужное доказательство.** Hash/source vendor weights, `.tpu` metadata и golden tensor/output, original pre/post reference; для baseline — immutable cfg/weights и точный output boundary. Старый helper — лишь versioned source evidence.

**Вопрос W2 / опровержение.** W2-E: можно ли действительно сопоставить хотя бы две эти ветки на одинаковых весах и одинаковом подготовленном входе? Проверить альтернативу, что vendor binary ожидал BGR, а RGB runner сам неверен; не объявлять RGB универсально правильным. Найти готовый artifact/manifest или честно установить непаритетность. Разобрать anchors/masks/order/sigmoid/coordinate transforms и b8 без повторного общего обзора YOLO.


### K006 — исправленный runner всё ещё предполагает COCO80 и конкретную голову/NMS (P0)

**Проблема/область.** W1-08-F06, W1-10-F03; source `run_yolov8_tpu.py` функции `normalize_prediction_shape`, `pick_output`, `load_io_names`, NMS call. Размер84/85, COCO80→91, выбор первого rank≥3 output, неприкреплённая версия Ultralytics и возможный objectness85 не образуют безопасный контракт custom PPE detector. `nms=False` не означает, что выход — нераскодированные feature maps: уровень decode надо установить по exporter.

**Последствие.** Custom число классов ломает host adapter; 85-канальная старая YOLO head может пройти shape-check и быть неверно интерпретирована. Успех API и похожие bbox не обнаружат систематическую ошибку.

**Нужное доказательство.** Actual output schema для pinned exporter: xywh/xyxy, pixels/normalized, sigmoid/objectness/DFL status, class count, transpose/layout; exact NMS source/version и golden raw→boxes.

**Вопрос W2 / опровержение.** W2-D: какие изменения действительно нужны для custom N/classes и какие предположения runner неверны даже после typo fix? Проверить контргипотезу, что современные Ultralytics NMS корректно обрабатывает 85 в данном exporter — нужна версия и source, не текущая rolling doc. Подготовить спецификацию адаптации/небольшой pure helper probe при необходимости; не строить полноценный прототип и не делать новый TPU claim.


### K019 — разрешение изучать source не даёт права распространять SDK/weights/image (P1)

**Проблема/область.** W1-13 различает MIT helper, bindings license unknown, repo license null, OEM software pricing; W1-14 частный registry. Но practical route может молча требовать раздать image пяти участникам, загрузить proprietary weights/данные в cloud или опубликовать `.tpu` в сдаче.

**Последствие.** Даже технически рабочий путь может не позволять перенос tooling/artifact или включение его в публичный repo. Политика ПД формы не SDK EULA. При этом неизвестная лицензия не означает уже установленный запрет на выполнение.

**Нужное доказательство.** Actual license/EULA/download conditions для каждой используемой поставки, sample code, checkpoint и compiled artifact; право execute/modify/redistribute отдельно. Не общий юридический обзор.

**Вопрос W2 / опровержение.** W2-A/E/K: какой конкретный route разрешён доступными условиями и какие права ещё нужно уточнить? Попытаться найти явную лицензию, опровергающую metadata UNKNOWN/null; использовать сохранённый LICENSE из actual archive, не соседний пакет. Не задерживать read-only исследование ожиданием несуществующего согласования.


Выход: _WORK/W2_E_RESULT.md. Все новые первичные evidence и точные unknown сохраняй подробно; короткую передачу отправь root.
