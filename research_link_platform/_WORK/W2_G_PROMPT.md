# W2-G: `.tpu` schema, current runtime/native ABI и пользовательские/сырые тензоры

# Second-wave researcher contract

Actual role gpt-6.1-sol medium, fork_turns none. Work folder D:/msk-prom2026-mark/research_link_platform. Read the original task, CRITIC.md and assigned W1/source files before the new investigation. Five experienced developers; 45-hour hackathon; mandatory LinQ inference, online mode/SDK/device SKU still unconfirmed unless RUN_STATE records a later actual grant. This is research, not a submission prototype. Historical context night23Oct2026; record actual access date/time separately.

You own only _WORK/W2_G_RESULT.md and auxiliary _WORK/W2_G/. Use uppercase names for new working artifacts; preserve downloaded original filenames. Do not modify final evidence/reports/critique. Do not delegate. Independently use actual network search/open/fetch plus bounded local source inspection where useful. Consult primary source or authors, pin source/version, do not rely on repeated snippets. Reuse saved evidence without duplicating broad W1 search. Registration/user interaction is owned by root; do not sign up/send messages/use credentials. No resources rented, SDK installed or device job run without concrete new authorization/context.

Every W2 task is tied to K IDs and a missing decision-changing answer. Attempt to falsify the provisional claim and identify limiting conditions, rather than finding one agreeable URL. A closed SDK or failed fetch is a narrow unknown, not a reason to stop unrelated work. Test alternate available retrieval channels when useful, and record actual method/time/status. Never call inaccessible material nonexistent. If a full artifact is unavailable, distinguish metadata/abstract/indexed or cached copy from live binary/source contents. Follow PDF skill if working with PDF; actual screenshot must be seen, a returned link alone is not visual inspection.

Result format: assigned question/K IDs; decision and findings; detailed local facts with W2-G-Fxx/source W2-G-Sxx; direct URLs/titles/authors/document dates/access times/locators; exact code versions/literals/configuration; evidence type separate from actual test status; negative attempts and contradictions; remaining unknowns with resolution path; concrete future experiments and compact root handoff. Clarify what changed from W1 and what did not. Partial script/helper probes are not SDK/compile/device validation. No invented API/CLI/operator/opset/calibration details. Do not copy full articles; use factual paraphrases and brief compliant quotations.

Completion is a useful established answer or precisely localized unknown after sufficient targeted search, not a source quota. Preserve depth and full details on disk, send root only consequential findings and completion.


## Индивидуальное задание оркестратора по критике

- **K:** K009,K012,K002. Решение: безопасный и корректный tensor adapter.
- **Старт:** saved pytpu15.0.24 actual code (README отдельно), guide runtime API, Program.info metadata/hardware_parameters, FULL/RAW enums.
- **Новый поиск:** current Python/C/C++ reference/headers/source/serialized model schema, version compatibility, user/raw buffers/scale/layout/lifetime; actual `.tpu` sample при доступности. Не выполнять неизвестный native code; artifact ZIP reading допустим как research.
- **Фальсификация:** найти changed validation/cleanup/current `.so` contract; проверить, какие stages FULL делает на host/device и не является ли older raw heuristic неприменимым.
- **Выход:** versioned API/schema diff и утверждения с границами; validation checklist на actual metadata, не generic guessed names; request list для закрытых fields. Современные проблемы не выводить из2023 TODO.


## Исходные замечания (не считать уже закрытыми)
### K009 — внешний float32, quantized TF rescale и runtime FULL не связаны численно (P0)

**Проблема/область.** Guide pp16,20–21 и pytpu `_bindings.py`: explicit rescale у quantized TF, original float feed у hardware, enum RAW/PRE_PROCESS/POST_PROCESS/FULL. Эти имена не раскрывают, где выполняются transpose/scales/casts/packing, какие операции уже скомпилированы и что входит в host/native pre/post.

**Последствие.** Ручной int8 cast/rescale может дважды преобразовать данные; отсутствие ручного rescale может быть правильным для одного `.tpu` и неверным для другого. Граница «вся сеть на TPU» также зависит от смысла native stages.

**Нужное доказательство.** Одна `.tpu` + metadata user/raw dtype/shape/scales, documented FULL/RAW transform, raw↔user golden pairs и current SDK API. Сопоставить quantized reference, TLM и runtime на одинаковом входе; не требовать FP32 bitwise equality.

**Вопрос W2 / опровержение.** W2-G совместно W2-F/J: кто выполняет численное преобразование границ программы и что доказывает режим FULL? Искать reference/native headers/examples; проверить альтернативу, что `.tpu` хранит host processing program, который является штатной частью inference. Не называть это ни CPU fallback, ни гарантированно TPU preprocessing до документа.


### K012 — legacy Python source не задаёт текущий native ABI, buffers и lifecycle (P0)

**Проблема/область.** W1-09/12/15, `_bindings.py`: lazy absolute `.so`, native JSON schema, inputs pointers без dtype/size validation, RAW ZIP heuristic; context managers имеют yield без try/finally, TODO buffer destroy. Это конкретный source2023, не установленная уязвимость/дефект Runtime2026.

**Последствие.** Ошибочный ndarray layout/dtype может не дать раннего исключения; старый binding нельзя безопасно считать актуальным. Повторный inference/cleanup после exception и живучесть output arrays требуют контракта.

**Нужное доказательство.** Matching current Python/native headers/reference и version matrix; metadata schema user/raw region keys, input lifetime/contiguity, buffer ownership/output copy semantics, release notes cleanup. Устройство/`.so` не запускать старым ctypes наугад.

**Вопрос W2 / опровержение.** W2-G: какие конкретные API/ABI и tensor schemas действуют в доступной современной поставке? Найти public headers/examples/package source, сопоставить с15.0.24. Попытаться опровергнуть опасения о cleanup/validation современным кодом или явным native контрактом. Если версия не получена, legacy риски маркировать только как вопросы, а не troubleshooting2026.


### K002 — нет единого современного dependency/ABI manifest (P0)

**Проблема/область.** W1-04-F02–09, W1-09-F03–08, W1-13-F11/13/18: Python3.8 сайта, Python3.11 guide, Ubuntu20.04 guide, Ubuntu24.04 и Framework2026.8.43/Runtime16.18.6 benchmark, pytpu15.0.24 и TF2.14.1 стороннего repo — разные свидетельства. Это не единая установка и не набор обязательных зависимостей.

**Последствие.** Потеря часов на несовместимые Python/native wheels или использование старого ctypes с новой libtpu; ложное обещание Windows/WSL/ARM из `py3-none-any`/логотипов.

**Нужное доказательство.** Для одного release: exact distributions/Requires-Python/Requires-Dist, native `.so`/driver/firmware pairing, compiler target, tested OS/ISA; официальный image digest или lock/wheelhouse и install guide. CPU-only compilation отдельно от hardware runtime.

**Вопрос W2 / опровержение.** W2-A: можно ли восстановить **одну** согласованную поставку современнее/равную guide2025, и какие части действительно требуют LinQ? Искать release metadata, существующие официальные download artifacts/containers, dependencies и CPU-only example. Проверить контргипотезу, что guide2025 всё ещё точно описывает текущий wheel, а отличие Ubuntu — лишь benchmark context. Не объявлять doc obsolete без доказательства.


Выход: _WORK/W2_G_RESULT.md. Все новые первичные evidence и точные unknown сохраняй подробно; короткую передачу отправь root.
