# W2-F: quantizer semantics, thresholds и калибровка с контролем качества

# Second-wave researcher contract

Actual role gpt-6.1-sol medium, fork_turns none. Work folder D:/msk-prom2026-mark/research_link_platform. Read the original task, CRITIC.md and assigned W1/source files before the new investigation. Five experienced developers; 45-hour hackathon; mandatory LinQ inference, online mode/SDK/device SKU still unconfirmed unless RUN_STATE records a later actual grant. This is research, not a submission prototype. Historical context night23Oct2026; record actual access date/time separately.

You own only _WORK/W2_F_RESULT.md and auxiliary _WORK/W2_F/. Use uppercase names for new working artifacts; preserve downloaded original filenames. Do not modify final evidence/reports/critique. Do not delegate. Independently use actual network search/open/fetch plus bounded local source inspection where useful. Consult primary source or authors, pin source/version, do not rely on repeated snippets. Reuse saved evidence without duplicating broad W1 search. Registration/user interaction is owned by root; do not sign up/send messages/use credentials. No resources rented, SDK installed or device job run without concrete new authorization/context.

Every W2 task is tied to K IDs and a missing decision-changing answer. Attempt to falsify the provisional claim and identify limiting conditions, rather than finding one agreeable URL. A closed SDK or failed fetch is a narrow unknown, not a reason to stop unrelated work. Test alternate available retrieval channels when useful, and record actual method/time/status. Never call inaccessible material nonexistent. If a full artifact is unavailable, distinguish metadata/abstract/indexed or cached copy from live binary/source contents. Follow PDF skill if working with PDF; actual screenshot must be seen, a returned link alone is not visual inspection.

Result format: assigned question/K IDs; decision and findings; detailed local facts with W2-F-Fxx/source W2-F-Sxx; direct URLs/titles/authors/document dates/access times/locators; exact code versions/literals/configuration; evidence type separate from actual test status; negative attempts and contradictions; remaining unknowns with resolution path; concrete future experiments and compact root handoff. Clarify what changed from W1 and what did not. Partial script/helper probes are not SDK/compile/device validation. No invented API/CLI/operator/opset/calibration details. Do not copy full articles; use factual paraphrases and brief compliant quotations.

Completion is a useful established answer or precisely localized unknown after sufficient targeted search, not a source quota. Preserve depth and full details on disk, send root only consequential findings and completion.


## Индивидуальное задание оркестратора по критике

- **K:** K008,K009,K020. Решение: как измерять PTQ loss и избегать ложного percentile experiment.
- **Старт:** guide §§3.1/термины; RegularModel code; memmap recipe и silent TypeError retry; сохранённые historical dnn_quant traces.
- **Новый поиск:** актуальная API/spec/examples threshold granularity/rounding/signedness/percentile/save-load, QAT/QDQ только при конкретной зацепке; layerwise compare tool и current TLM numerical scope. Не создавать учебник INT8.
- **Фальсификация:** проверить weights-only vs activations percentile, наличие нового QAT path, ignored parameter и double rescale.
- **Выход:** точная numerical evidence matrix; staged eval protocol для малых СИЗ с camera/time-separated calibration/eval, memory/time artifacts и исходами. 100/500 не объявлять достаточным нормативом.


## Исходные замечания (не считать уже закрытыми)
### K008 — PTQ путь есть, но percentile/threshold и численная схема не раскрыты (P1)

**Проблема/область.** W1-07-F02–07 и guide p8: percentile описан как процент весовых коэффициентов, repo передаёт его calibrate и ловит любой TypeError с повтором без параметра. Неизвестны activation/weight clipping, signedness, granularity, rounding, accumulator, QAT/QDQ import. Два/100/500 samples — разные цели, не нормы достаточности.

**Последствие.** Эксперимент percentile может менять не тот параметр или не менять его вовсе; «INT8 ONNX» может не войти в LinQ path; потеря мелких СИЗ может остаться не локализована. Memmap ~2.29GiB — backing store, не peak RAM калибровки.

**Нужное доказательство.** Актуальный quantizer reference/source docstrings, threshold schema/save-load, effective parameters/logging, layerwise comparison; точный calibration→input recipe и качество на независимом eval.

**Вопрос W2 / опровержение.** W2-F: что именно калибрует `RegularModel.calibrate`, как применяется percentile и что можно повторить/экспортировать? Проверить контргипотезы «параметр относится только к weights», «новое API поддерживает activation clipping/QAT». Если SDK недоступен, дать versioned документальный остаток и минимальный эксперимент, различающий эти исходы; не назначать стандартную asymmetric/per-channel схему из общего знания.


### K009 — внешний float32, quantized TF rescale и runtime FULL не связаны численно (P0)

**Проблема/область.** Guide pp16,20–21 и pytpu `_bindings.py`: explicit rescale у quantized TF, original float feed у hardware, enum RAW/PRE_PROCESS/POST_PROCESS/FULL. Эти имена не раскрывают, где выполняются transpose/scales/casts/packing, какие операции уже скомпилированы и что входит в host/native pre/post.

**Последствие.** Ручной int8 cast/rescale может дважды преобразовать данные; отсутствие ручного rescale может быть правильным для одного `.tpu` и неверным для другого. Граница «вся сеть на TPU» также зависит от смысла native stages.

**Нужное доказательство.** Одна `.tpu` + metadata user/raw dtype/shape/scales, documented FULL/RAW transform, raw↔user golden pairs и current SDK API. Сопоставить quantized reference, TLM и runtime на одинаковом входе; не требовать FP32 bitwise equality.

**Вопрос W2 / опровержение.** W2-G совместно W2-F/J: кто выполняет численное преобразование границ программы и что доказывает режим FULL? Искать reference/native headers/examples; проверить альтернативу, что `.tpu` хранит host processing program, который является штатной частью inference. Не называть это ни CPU fallback, ни гарантированно TPU preprocessing до документа.


### K020 — эксперименты нужны как дерево решений с одним владельцем каждой границы (P0 для итогового handoff)

**Проблема/область.** Во всех W1 много хороших E, но они дублируются: inventory/smoke/parity/performance повторены почти в каждой ветке. Нет общей спецификации, какой минимальный успешный результат даёт переход к custom model и когда остановить неподтверждённый путь в пределах45часов. Hardcoded «30–60мин» в W1-11 — план, не измеренное время.

**Последствие.** Пять инженеров будут повторять inventory и спорить о разных preprocess вместо закрытия независимых стадий; слишком сложный ladder без доступного TLM может выглядеть обязательным.

**Нужное доказательство/уточнение.** Для каждого W2 результата: состояние «можно проверить сейчас / нужен SDK / нужен LinQ / нужен ответ постановщика», exact artifacts/prerequisites, ожидаемое наблюдение, альтернативный исход и что success **не доказывает**. Одна shared golden input/output specification, один model manifest, уникальные владельцы. TLM — полезный checkpoint при наличии, не mandatory доступный инструмент.

**Вопрос W2 / опровержение.** Каждая W2-ветка обязана дать решающий эксперимент с минимумом предпосылок и попыткой опровержения своего provisional conclusion. Проверить гипотезу «known-good vendor smoke обязателен»: если поставщик даёт только compiler+custom example, возможен другой подтверждаемый старт. Сборщик затем объединяет E/R и priority questions без отдельной поисковой/аудиторской стадии. Не разрабатывать сдаваемый prototype в исследовании.


Выход: _WORK/W2_F_RESULT.md. Все новые первичные evidence и точные unknown сохраняй подробно; короткую передачу отправь root.
