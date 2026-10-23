# W2-H: аппаратные ревизии, адресация памяти и multi-device mapping

# Second-wave researcher contract

Actual role gpt-6.1-sol medium, fork_turns none. Work folder D:/msk-prom2026-mark/research_link_platform. Read the original task, CRITIC.md and assigned W1/source files before the new investigation. Five experienced developers; 45-hour hackathon; mandatory LinQ inference, online mode/SDK/device SKU still unconfirmed unless RUN_STATE records a later actual grant. This is research, not a submission prototype. Historical context night23Oct2026; record actual access date/time separately.

You own only _WORK/W2_H_RESULT.md and auxiliary _WORK/W2_H/. Use uppercase names for new working artifacts; preserve downloaded original filenames. Do not modify final evidence/reports/critique. Do not delegate. Independently use actual network search/open/fetch plus bounded local source inspection where useful. Consult primary source or authors, pin source/version, do not rely on repeated snippets. Reuse saved evidence without duplicating broad W1 search. Registration/user interaction is owned by root; do not sign up/send messages/use credentials. No resources rented, SDK installed or device job run without concrete new authorization/context.

Every W2 task is tied to K IDs and a missing decision-changing answer. Attempt to falsify the provisional claim and identify limiting conditions, rather than finding one agreeable URL. A closed SDK or failed fetch is a narrow unknown, not a reason to stop unrelated work. Test alternate available retrieval channels when useful, and record actual method/time/status. Never call inaccessible material nonexistent. If a full artifact is unavailable, distinguish metadata/abstract/indexed or cached copy from live binary/source contents. Follow PDF skill if working with PDF; actual screenshot must be seen, a returned link alone is not visual inspection.

Result format: assigned question/K IDs; decision and findings; detailed local facts with W2-H-Fxx/source W2-H-Sxx; direct URLs/titles/authors/document dates/access times/locators; exact code versions/literals/configuration; evidence type separate from actual test status; negative attempts and contradictions; remaining unknowns with resolution path; concrete future experiments and compact root handoff. Clarify what changed from W1 and what did not. Partial script/helper probes are not SDK/compile/device validation. No invented API/CLI/operator/opset/calibration details. Do not copy full articles; use factual paraphrases and brief compliant quotations.

Completion is a useful established answer or precisely localized unknown after sufficient targeted search, not a source quota. Preserve depth and full details on disk, send root only consequential findings and completion.


## Индивидуальное задание оркестратора по критике

- **K:** K010,K002,K011. Решение: compiler target/memory fit/concurrency и interpretation scaling.
- **Старт:** W1-02 SOURCE_EXTRACTS, exact paired manuals/datasheets, presentation p2/p3, RUN_SCENARIO §8 four-device HPD1M label.
- **Новый поиск:** original visual tables/revision metadata, vendor SKU documentation и memory planning/partition examples; установить scope power/PCIe conflicts и H1M/partnumber link уже учесть как найденную.
- **Фальсификация:** расхождения могут быть разные комплектации; несколько `/dev` не доказывают одну HPD; sum memory может быть доступна via explicit graph distribution, но это требует docs.
- **Выход:** конфликтная таблица с status/resolution, mapping diagram/table chip↔card↔endpoint↔runtime context и first-inventory protocol. Не бесконечная аппаратная история/оценка производства.


## Исходные замечания (не считать уже закрытыми)
### K010 — конкретная топология/память неизвестны, а имена папок противоречат числу устройств (P1; P0 после выдачи target)

**Проблема/область.** W1-02: HP 16/32GB, Gen3/Gen2; HPD/HPQ power и названия исполнений; aggregate DDR. Новый locator критика: `RUN_SCENARIO.txt` §8 называет HPD1M и четыре `/dev/tpu3…0`, тогда как РЭ HPD1M-01 описывает два chips/endpoints, HPD1M-10/11 (HPQ) — четыре. Это может быть несколько карт, переименование, общий host или неточное label; вывод о числе чипов по имени каталога недопустим.

**Последствие.** Неверная оценка multi-device scaling, памяти на граф и quota; некорректное сравнение HP/HPD и перенос artifact target.

**Нужное доказательство.** Даты/revisions hardware PDFs, authoritative SKU↔chip↔PCIe endpoint↔runtime device mapping, per-graph memory limits/memory planner, hardware_parameters. Установить physical capabilities отдельно от negotiated link и allocated resources.

**Вопрос W2 / опровержение.** W2-H: какие расхождения реально относятся одному исполнению и какие снимаются revision/BOM? Визуально сверить конфликтные таблицы, включить presentation p3 (HP PCIe2.0, иные TDP). Попытаться опровергнуть «единая память недоступна»: искать explicit multi-chip graph partitioning/remote memory docs; отсутствие таких docs оставить unknown, а не «платформа не умеет».


### K002 — нет единого современного dependency/ABI manifest (P0)

**Проблема/область.** W1-04-F02–09, W1-09-F03–08, W1-13-F11/13/18: Python3.8 сайта, Python3.11 guide, Ubuntu20.04 guide, Ubuntu24.04 и Framework2026.8.43/Runtime16.18.6 benchmark, pytpu15.0.24 и TF2.14.1 стороннего repo — разные свидетельства. Это не единая установка и не набор обязательных зависимостей.

**Последствие.** Потеря часов на несовместимые Python/native wheels или использование старого ctypes с новой libtpu; ложное обещание Windows/WSL/ARM из `py3-none-any`/логотипов.

**Нужное доказательство.** Для одного release: exact distributions/Requires-Python/Requires-Dist, native `.so`/driver/firmware pairing, compiler target, tested OS/ISA; официальный image digest или lock/wheelhouse и install guide. CPU-only compilation отдельно от hardware runtime.

**Вопрос W2 / опровержение.** W2-A: можно ли восстановить **одну** согласованную поставку современнее/равную guide2025, и какие части действительно требуют LinQ? Искать release metadata, существующие официальные download artifacts/containers, dependencies и CPU-only example. Проверить контргипотезу, что guide2025 всё ещё точно описывает текущий wheel, а отличие Ubuntu — лишь benchmark context. Не объявлять doc obsolete без доказательства.


### K011 — современная таблица performance ещё text-only и не имеет единого timing contract (P1)

**Проблема/область.** W1-11-F01/02, сохранённый presentation JSON p3/p4. `anti_spoof 985.72ms`, `lenet5 128.90ms` при тысячах FPS; HPQ=4×HP во всех строках и та же latency; p3 ResNet460/1046 против p4 432.9/1112.8; batch8 SSD slower. Их нельзя чинить делением на1000. Заявление «по методике MLPerf» не submission/log.

**Последствие.** Ошибка единиц/сценария превратится в ожидания latency/камер; искусственное среднее с ВКР и историческим FPGA создаст ложную уверенность.

**Нужное доказательство.** Визуальная таблица/исходный слайд, units и footnote; modern logs/scenario/LoadGen/version/model/input/preset/precision/quality/device count, inclusion transfers/NMS и latency percentile. Сам внешний timer sync также не чистый compute.

**Вопрос W2 / опровержение.** W2-I: что обозначают FPS/latency в этой конкретной таблице и есть ли underlying modern protocol? Попытаться опровергнуть гипотезу typo: иные scenario/overlap/percentile могут согласовать числа. Проверить, действительно ли HPQ измерялся отдельно. ВКР/авторский repo исследовать лишь для недостающего протокола; защищённый full text не обходить. При неуспехе сохранить числа без «исправления» и не обещать камеры.


Выход: _WORK/W2_H_RESULT.md. Все новые первичные evidence и точные unknown сохраняй подробно; короткую передачу отправь root.
