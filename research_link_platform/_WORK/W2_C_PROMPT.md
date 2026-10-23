# W2-C: ONNX frontend и минимальная карта graph constraints кандидатов

# Second-wave researcher contract

Actual role gpt-6.1-sol medium, fork_turns none. Work folder D:/msk-prom2026-mark/research_link_platform. Read the original task, CRITIC.md and assigned W1/source files before the new investigation. Five experienced developers; 45-hour hackathon; mandatory LinQ inference, online mode/SDK/device SKU still unconfirmed unless RUN_STATE records a later actual grant. This is research, not a submission prototype. Historical context night23Oct2026; record actual access date/time separately.

You own only _WORK/W2_C_RESULT.md and auxiliary _WORK/W2_C/. Use uppercase names for new working artifacts; preserve downloaded original filenames. Do not modify final evidence/reports/critique. Do not delegate. Independently use actual network search/open/fetch plus bounded local source inspection where useful. Consult primary source or authors, pin source/version, do not rely on repeated snippets. Reuse saved evidence without duplicating broad W1 search. Registration/user interaction is owned by root; do not sign up/send messages/use credentials. No resources rented, SDK installed or device job run without concrete new authorization/context.

Every W2 task is tied to K IDs and a missing decision-changing answer. Attempt to falsify the provisional claim and identify limiting conditions, rather than finding one agreeable URL. A closed SDK or failed fetch is a narrow unknown, not a reason to stop unrelated work. Test alternate available retrieval channels when useful, and record actual method/time/status. Never call inaccessible material nonexistent. If a full artifact is unavailable, distinguish metadata/abstract/indexed or cached copy from live binary/source contents. Follow PDF skill if working with PDF; actual screenshot must be seen, a returned link alone is not visual inspection.

Result format: assigned question/K IDs; decision and findings; detailed local facts with W2-C-Fxx/source W2-C-Sxx; direct URLs/titles/authors/document dates/access times/locators; exact code versions/literals/configuration; evidence type separate from actual test status; negative attempts and contradictions; remaining unknowns with resolution path; concrete future experiments and compact root handoff. Clarify what changed from W1 and what did not. Partial script/helper probes are not SDK/compile/device validation. No invented API/CLI/operator/opset/calibration details. Do not copy full articles; use factual paraphrases and brief compliant quotations.

Completion is a useful established answer or precisely localized unknown after sufficient targeted search, not a source quota. Preserve depth and full details on disk, send root only consequential findings and completion.


## Индивидуальное задание оркестратора по критике

- **K:** K004,K005,K008. Решение: что передать `model_stack` и какие варианты экспорта действительно проверять.
- **Старт:** W1-05/06; pinned build/export source; guide importer; запросы точных `onnx_direct`, `RegularModel`, target names.
- **Новый поиск:** versioned frontend docs/source/examples, actual supported opset/IR/attributes; direct ONNX alternative; batch/HW constraints и shape-dependent constants. Сосредоточиться на графах из W2-D/E, а не всех ONNX operators.
- **Фальсификация:** static13/noNMS может быть лишь авторским выбором, а современный parser поддерживать другие opsets/dynamic batch; наоборот successful export не гарантирует lowering. Unknown не помечать unsupported.
- **Выход:** table `candidate→operator/attribute→evidence/version→risk→minimal differentiating test`; точный exporter/graph inventory handoff. Если нет model bytes, не выдумывать actual graph nodes по семейному имени.


## Исходные замечания (не считать уже закрытыми)
### K004 — поддержка ONNX не локализована до импортера, opset/IR и атрибутов (P0)

**Проблема/область.** W1-05-F03–13, W1-06 operator matrix: нет supported opset/IR/domains, ограничений `Resize`, shape ops, DFL/decode, dynamic shape/batch. Repo `force_static_onnx_input_shape` меняет input declaration, но само по себе не переписывает все shape-dependent constants графа. Opset13 и static640 — решение автора; ONNX>=1.15 из HX — package version.

**Последствие.** «Валидный ONNX» или изменение dim_value не гарантируют правильные внутренние shapes, импорт и компиляцию. Можно преждевременно забраковать архитектуру или неделями обходить несуществующий запрет.

**Нужное доказательство.** Versioned frontend reference/operator matrix или exact successful export+import/compile protocol; attributes/dtypes/ranks, shape inference и обработка output names. Минимальные графы должны происходить из реального выбранного кандидата.

**Вопрос W2 / опровержение.** W2-C: для конкретных YOLO detection/head exports какие реальные узлы и атрибуты определяют риск и есть ли первичное подтверждение их lowering? Проверить альтернативу: современный SDK использует иной direct ONNX path, поэтому старый TF seam не применим. Разделить documented support / source intent / actual compile. Не перечислять типичные NPU ограничения как найденные LinQ restrictions.


### K005 — условный shortlist ещё не доказывает, что YOLOv8s лучше других путей (P0)

**Проблема/область.** W1-08 рекомендует YOLOv8s/n, но найденный benchmark — `yolov8n_pose`, repo self-build — detection s, а `RUN_SCENARIO.txt` финализирует detection на vendor TinyYOLO3. У self-build YOLOv8 нет success logs; отсутствие таких логов не доказывает невозможность. YOLO11 пока family claim, но ВКР СПбПУ имеет авторское сообщение `YOLO11l OBB 20FPS` с нераскрытыми условиями.

**Последствие.** Модельная команда может выбрать наименее подтверждённый граф ради современного имени или отказаться от поддержанного vendor export, который не найден в W1.

**Нужное доказательство.** Exact task/variant/weights/exporter/package versions/HW/batch, build log/`.tpu` и quality evidence. Один known-good detector для smoke test и один путь custom weights должны быть разведены.

**Вопрос W2 / опровержение.** W2-D: существует ли доступный первичный успех custom YOLOv8 detection либо более прямой YOLO5s/YOLO11 detector путь на matched LinQ? Искать автора repo, history/tags/issues/публичную пояснительную записку, технические материалы производителя/университета без обхода авторизации. Попытаться опровергнуть предпочтение YOLOv8: сравнить **замкнутость артефактов**, а не популярность. Если ни один путь не замкнут, дать равноправные условные кандидаты с конкретным первым gate.


### K008 — PTQ путь есть, но percentile/threshold и численная схема не раскрыты (P1)

**Проблема/область.** W1-07-F02–07 и guide p8: percentile описан как процент весовых коэффициентов, repo передаёт его calibrate и ловит любой TypeError с повтором без параметра. Неизвестны activation/weight clipping, signedness, granularity, rounding, accumulator, QAT/QDQ import. Два/100/500 samples — разные цели, не нормы достаточности.

**Последствие.** Эксперимент percentile может менять не тот параметр или не менять его вовсе; «INT8 ONNX» может не войти в LinQ path; потеря мелких СИЗ может остаться не локализована. Memmap ~2.29GiB — backing store, не peak RAM калибровки.

**Нужное доказательство.** Актуальный quantizer reference/source docstrings, threshold schema/save-load, effective parameters/logging, layerwise comparison; точный calibration→input recipe и качество на независимом eval.

**Вопрос W2 / опровержение.** W2-F: что именно калибрует `RegularModel.calibrate`, как применяется percentile и что можно повторить/экспортировать? Проверить контргипотезы «параметр относится только к weights», «новое API поддерживает activation clipping/QAT». Если SDK недоступен, дать versioned документальный остаток и минимальный эксперимент, различающий эти исходы; не назначать стандартную asymmetric/per-channel схему из общего знания.


Выход: _WORK/W2_C_RESULT.md. Все новые первичные evidence и точные unknown сохраняй подробно; короткую передачу отправь root.
