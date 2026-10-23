# W2-D: современный custom detector и корректный custom-class output adapter

# Second-wave researcher contract

Actual role gpt-6.1-sol medium, fork_turns none. Work folder D:/msk-prom2026-mark/research_link_platform. Read the original task, CRITIC.md and assigned W1/source files before the new investigation. Five experienced developers; 45-hour hackathon; mandatory LinQ inference, online mode/SDK/device SKU still unconfirmed unless RUN_STATE records a later actual grant. This is research, not a submission prototype. Historical context night23Oct2026; record actual access date/time separately.

You own only _WORK/W2_D_RESULT.md and auxiliary _WORK/W2_D/. Use uppercase names for new working artifacts; preserve downloaded original filenames. Do not modify final evidence/reports/critique. Do not delegate. Independently use actual network search/open/fetch plus bounded local source inspection where useful. Consult primary source or authors, pin source/version, do not rely on repeated snippets. Reuse saved evidence without duplicating broad W1 search. Registration/user interaction is owned by root; do not sign up/send messages/use credentials. No resources rented, SDK installed or device job run without concrete new authorization/context.

Every W2 task is tied to K IDs and a missing decision-changing answer. Attempt to falsify the provisional claim and identify limiting conditions, rather than finding one agreeable URL. A closed SDK or failed fetch is a narrow unknown, not a reason to stop unrelated work. Test alternate available retrieval channels when useful, and record actual method/time/status. Never call inaccessible material nonexistent. If a full artifact is unavailable, distinguish metadata/abstract/indexed or cached copy from live binary/source contents. Follow PDF skill if working with PDF; actual screenshot must be seen, a returned link alone is not visual inspection.

Result format: assigned question/K IDs; decision and findings; detailed local facts with W2-D-Fxx/source W2-D-Sxx; direct URLs/titles/authors/document dates/access times/locators; exact code versions/literals/configuration; evidence type separate from actual test status; negative attempts and contradictions; remaining unknowns with resolution path; concrete future experiments and compact root handoff. Clarify what changed from W1 and what did not. Partial script/helper probes are not SDK/compile/device validation. No invented API/CLI/operator/opset/calibration details. Do not copy full articles; use factual paraphrases and brief compliant quotations.

Completion is a useful established answer or precisely localized unknown after sufficient targeted search, not a source quota. Preserve depth and full details on disk, send root only consequential findings and completion.


## Индивидуальное задание оркестратора по критике

- **K:** K005,K006,K018,K020. Решение: какой custom PPE model route имеет лучшую доказательную опору.
- **Старт:** pinned YOLOv8 exporter/build/runner, RUN_SCENARIO final Tiny path; vendor yolo5s/yolov8n_pose; СПбПУ metadata `vr26-931`.
- **Новый поиск:** success evidence автора repo/пояснительные материалы/history/issues и официальный exact YOLO5s/YOLO8/YOLO11 sample. Для найденной конфигурации проследить веса/exporter→compiler→runtime; отдельно source version Ultralytics NMS и 4+N/5+N semantics.
- **Фальсификация:** найти контрпример предпочтению v8; исследовать возможность modern supported detector, пропущенного W1. Не расширять в полный обзор модельного рынка/обучения.
- **Выход:** 2–3 условных кандидата по замкнутости chain, exact gaps/gates; postprocess schema для custom classes и planned patch list. Unicode bug повторно не исследовать. Если автор сообщает запуск — это reported execution, не наш тест.


## Исходные замечания (не считать уже закрытыми)
### K005 — условный shortlist ещё не доказывает, что YOLOv8s лучше других путей (P0)

**Проблема/область.** W1-08 рекомендует YOLOv8s/n, но найденный benchmark — `yolov8n_pose`, repo self-build — detection s, а `RUN_SCENARIO.txt` финализирует detection на vendor TinyYOLO3. У self-build YOLOv8 нет success logs; отсутствие таких логов не доказывает невозможность. YOLO11 пока family claim, но ВКР СПбПУ имеет авторское сообщение `YOLO11l OBB 20FPS` с нераскрытыми условиями.

**Последствие.** Модельная команда может выбрать наименее подтверждённый граф ради современного имени или отказаться от поддержанного vendor export, который не найден в W1.

**Нужное доказательство.** Exact task/variant/weights/exporter/package versions/HW/batch, build log/`.tpu` и quality evidence. Один known-good detector для smoke test и один путь custom weights должны быть разведены.

**Вопрос W2 / опровержение.** W2-D: существует ли доступный первичный успех custom YOLOv8 detection либо более прямой YOLO5s/YOLO11 detector путь на matched LinQ? Искать автора repo, history/tags/issues/публичную пояснительную записку, технические материалы производителя/университета без обхода авторизации. Попытаться опровергнуть предпочтение YOLOv8: сравнить **замкнутость артефактов**, а не популярность. Если ни один путь не замкнут, дать равноправные условные кандидаты с конкретным первым gate.


### K006 — исправленный runner всё ещё предполагает COCO80 и конкретную голову/NMS (P0)

**Проблема/область.** W1-08-F06, W1-10-F03; source `run_yolov8_tpu.py` функции `normalize_prediction_shape`, `pick_output`, `load_io_names`, NMS call. Размер84/85, COCO80→91, выбор первого rank≥3 output, неприкреплённая версия Ultralytics и возможный objectness85 не образуют безопасный контракт custom PPE detector. `nms=False` не означает, что выход — нераскодированные feature maps: уровень decode надо установить по exporter.

**Последствие.** Custom число классов ломает host adapter; 85-канальная старая YOLO head может пройти shape-check и быть неверно интерпретирована. Успех API и похожие bbox не обнаружат систематическую ошибку.

**Нужное доказательство.** Actual output schema для pinned exporter: xywh/xyxy, pixels/normalized, sigmoid/objectness/DFL status, class count, transpose/layout; exact NMS source/version и golden raw→boxes.

**Вопрос W2 / опровержение.** W2-D: какие изменения действительно нужны для custom N/classes и какие предположения runner неверны даже после typo fix? Проверить контргипотезу, что современные Ultralytics NMS корректно обрабатывает 85 в данном exporter — нужна версия и source, не текущая rolling doc. Подготовить спецификацию адаптации/небольшой pure helper probe при необходимости; не строить полноценный прототип и не делать новый TPU claim.


### K018 — число веток не равно числу независимых доказательств (P1, сквозное)

**Проблема/область.** Большая часть W1-04…15 зависит от одного guide extraction, одного repo commit и одного sdist. Часто «independent AST» подтверждает лишь тот же host literal. Text из TinyFish, web cached PDF и повторная TinyFish extraction могут быть одной upstream версией. Отдельные новые сильные линии — IVATech archive, industrial partner docs, university author metadata — требуют собственной области применимости.

**Последствие.** Сборщик может превратить десять ссылок на один defect/claim в десять подтверждений hardware support. Неясная сохранность PDF bytes мешает установить, что каналы видели ту же редакцию.

**Нужное доказательство.** Source lineage, canonical URL/content hash/commit/version и `read channel/status`; независимость по автору/эксперименту, а не исследователю. Primary source runtime log и чужой код не взаимозаменяемы.

**Вопрос W2 / опровержение.** Во всех заданиях: какое **новое первичное** доказательство добавлено сверх существующего source lineage? W2-D/I/K целенаправленно ищут независимые технические протоколы, пытаясь опровергнуть гипотезу «весь modern вывод замкнут на vendor slide и один repo». Если найден только пересказ, записать зависимость и не повышать статус. Отдельная W2-ветка для повторной сверки всех фактов не нужна.


### K020 — эксперименты нужны как дерево решений с одним владельцем каждой границы (P0 для итогового handoff)

**Проблема/область.** Во всех W1 много хороших E, но они дублируются: inventory/smoke/parity/performance повторены почти в каждой ветке. Нет общей спецификации, какой минимальный успешный результат даёт переход к custom model и когда остановить неподтверждённый путь в пределах45часов. Hardcoded «30–60мин» в W1-11 — план, не измеренное время.

**Последствие.** Пять инженеров будут повторять inventory и спорить о разных preprocess вместо закрытия независимых стадий; слишком сложный ladder без доступного TLM может выглядеть обязательным.

**Нужное доказательство/уточнение.** Для каждого W2 результата: состояние «можно проверить сейчас / нужен SDK / нужен LinQ / нужен ответ постановщика», exact artifacts/prerequisites, ожидаемое наблюдение, альтернативный исход и что success **не доказывает**. Одна shared golden input/output specification, один model manifest, уникальные владельцы. TLM — полезный checkpoint при наличии, не mandatory доступный инструмент.

**Вопрос W2 / опровержение.** Каждая W2-ветка обязана дать решающий эксперимент с минимумом предпосылок и попыткой опровержения своего provisional conclusion. Проверить гипотезу «known-good vendor smoke обязателен»: если поставщик даёт только compiler+custom example, возможен другой подтверждаемый старт. Сборщик затем объединяет E/R и priority questions без отдельной поисковой/аудиторской стадии. Не разрабатывать сдаваемый prototype в исследовании.


Выход: _WORK/W2_D_RESULT.md. Все новые первичные evidence и точные unknown сохраняй подробно; короткую передачу отправь root.

Новая находка W2-C: primary Ultralytics v8.3.0 Detect export=True с nms=False всё ещё вызывает _inference, DFL/decode/cls.sigmoid. Точный repo не pin ultralytics и model bytes нет, значит actual ONNX nodes пока не установлены. Сопоставь semantics output/NMS отдельно, не приравнивай noNMS к raw conv head. W2-C сохранит source locators.
