# W2-J: profiler и проверяемое execution evidence для actual access mode

# Second-wave researcher contract

Actual role gpt-6.1-sol medium, fork_turns none. Work folder D:/msk-prom2026-mark/research_link_platform. Read the original task, CRITIC.md and assigned W1/source files before the new investigation. Five experienced developers; 45-hour hackathon; mandatory LinQ inference, online mode/SDK/device SKU still unconfirmed unless RUN_STATE records a later actual grant. This is research, not a submission prototype. Historical context night23Oct2026; record actual access date/time separately.

You own only _WORK/W2_J_RESULT.md and auxiliary _WORK/W2_J/. Use uppercase names for new working artifacts; preserve downloaded original filenames. Do not modify final evidence/reports/critique. Do not delegate. Independently use actual network search/open/fetch plus bounded local source inspection where useful. Consult primary source or authors, pin source/version, do not rely on repeated snippets. Reuse saved evidence without duplicating broad W1 search. Registration/user interaction is owned by root; do not sign up/send messages/use credentials. No resources rented, SDK installed or device job run without concrete new authorization/context.

Every W2 task is tied to K IDs and a missing decision-changing answer. Attempt to falsify the provisional claim and identify limiting conditions, rather than finding one agreeable URL. A closed SDK or failed fetch is a narrow unknown, not a reason to stop unrelated work. Test alternate available retrieval channels when useful, and record actual method/time/status. Never call inaccessible material nonexistent. If a full artifact is unavailable, distinguish metadata/abstract/indexed or cached copy from live binary/source contents. Follow PDF skill if working with PDF; actual screenshot must be seen, a returned link alone is not visual inspection.

Result format: assigned question/K IDs; decision and findings; detailed local facts with W2-J-Fxx/source W2-J-Sxx; direct URLs/titles/authors/document dates/access times/locators; exact code versions/literals/configuration; evidence type separate from actual test status; negative attempts and contradictions; remaining unknowns with resolution path; concrete future experiments and compact root handoff. Clarify what changed from W1 and what did not. Partial script/helper probes are not SDK/compile/device validation. No invented API/CLI/operator/opset/calibration details. Do not copy full articles; use factual paraphrases and brief compliant quotations.

Completion is a useful established answer or precisely localized unknown after sufficient targeted search, not a source quota. Preserve depth and full details on disk, send root only consequential findings and completion.


## Индивидуальное задание оркестратора по критике

- **K:** K013,K009,K014. Решение: как показать обязательный LinQ inference без фиктивного indicator.
- **Старт:** HPS Performance Profiler/DNN Stat/Power Monitor names, W1-15 evidence chain, actual legacy APIs; whole/partial fallback distinction.
- **Новый поиск:** конкретные manuals/package/sample reports/maintainer statements, coverage/partition/strict execution semantics и device identity; различать per-request vs aggregate counters и estimated vs measured values.
- **Фальсификация:** monitoring may not prove our request; no Python fallback is not native guarantee; explicit artifact ISA may offer stronger evidence than utilisation.
- **Выход:** два адаптируемых протокола SSH/container и service-only с полями/сильными и слабыми свидетельствами, безопасным negative control и запросом допустимого критерия жюри. Никакого выдуманного CLI/attestation и отключения shared device.


## Исходные замечания (не считать уже закрытыми)
### K013 — доказательство отсутствия полного и частичного fallback требует разных свидетельств (P0)

**Проблема/область.** W1-15 предлагает сильную цепочку, но profiler только назван в HPS datasheet; реальные commands/counters не найдены. Invalid-device test различает fail-closed при open, но не исключает host operation partitioning или замену модели server-side. Нагрузка общего TPU может быть чужой.

**Последствие.** Скриншот utilisation, node mapping, `backend=LinQ` или return200 не докажут выполнение нашей модели, а строгий критерий жюри неизвестен.

**Нужное доказательство.** Versioned Performance Profiler/DNN Stat manual/sample report; per-request/artifact/device correlation, compiler coverage/partition report или официальная гарантия whole graph/no fallback; допустимый критерий организатора. App-side logs и native runtime остаются разными trust boundaries.

**Вопрос W2 / опровержение.** W2-J: какое сильнейшее **реально доступное** свидетельство связывает конкретный artifact/input/completion с физическим LinQ для SSH и service-only? Проверить альтернативу, что profiler показывает лишь host estimates/aggregate, либо SDK по конструкции не допускает model fallback и coverage доказывается artifact format. Не придумывать `linq-smi`/strict flag и не требовать недоказанную аппаратную attestation как обязательное условие кейса.


### K009 — внешний float32, quantized TF rescale и runtime FULL не связаны численно (P0)

**Проблема/область.** Guide pp16,20–21 и pytpu `_bindings.py`: explicit rescale у quantized TF, original float feed у hardware, enum RAW/PRE_PROCESS/POST_PROCESS/FULL. Эти имена не раскрывают, где выполняются transpose/scales/casts/packing, какие операции уже скомпилированы и что входит в host/native pre/post.

**Последствие.** Ручной int8 cast/rescale может дважды преобразовать данные; отсутствие ручного rescale может быть правильным для одного `.tpu` и неверным для другого. Граница «вся сеть на TPU» также зависит от смысла native stages.

**Нужное доказательство.** Одна `.tpu` + metadata user/raw dtype/shape/scales, documented FULL/RAW transform, raw↔user golden pairs и current SDK API. Сопоставить quantized reference, TLM и runtime на одинаковом входе; не требовать FP32 bitwise equality.

**Вопрос W2 / опровержение.** W2-G совместно W2-F/J: кто выполняет численное преобразование границ программы и что доказывает режим FULL? Искать reference/native headers/examples; проверить альтернативу, что `.tpu` хранит host processing program, который является штатной частью inference. Не называть это ни CPU fallback, ни гарантированно TPU preprocessing до документа.


### K014 — online contract должен включать обновление собственной модели, квоты и путь кадров (P0)

**Проблема/область.** W1-03/09 разложили сценарии, но не установлены control/data plane: разрешён ли custom graph/weights, compiler service или только готовые models, persist storage, runtime sessions, limits, transport и camera reachability. Cloud vacancy и IVA CV Edge API не спецификация LinQ access.

**Последствие.** Можно получить действительный LinQ API, на котором невозможно выполнить собственную PPE модель; локальный UI/remote runtime могут не иметь доступного двустороннего канала/порта. Это влияет на архитектуру сильнее выбора NMS.

**Нужное доказательство.** Official onboarding/API/job/SSH instructions, permitted artifact type/update process, request/response schema/dtype, authentication, quotas and timeouts, concurrency/backpressure, persist/retention и logs. Секреты в отчёты не сохранять.

**Вопрос W2 / опровержение.** W2-L: какие режимы реально подтверждены для demo/соревнования и что у каждого разрешено делать со своей моделью? Попытаться опровергнуть предположение «обязательно нужен shell»: рабочий tensor/model API может закрыть задачу без него. Одновременно искать ограничения service-only, которые заставляют выбрать иной маршрут. Не угадывать endpoints и не отправлять сообщения от имени пользователя.


Выход: _WORK/W2_J_RESULT.md. Все новые первичные evidence и точные unknown сохраняй подробно; короткую передачу отправь root.
