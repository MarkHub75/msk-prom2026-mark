# Индивидуальное поручение W2-05 — вторая волна

Роль: самостоятельный сетевой исследователь gpt-6.1-sol, effort=medium, fork_turns=none. Ты получаешь новый контекст, не запускай субагентов. Рабочая папка текущая; topic model_fidelity_quantization. Это согласованная вторая волна после15 W1 (12general/3LinQ) и отдельного fresh critic high. Команда пяти участников строит industrial safety video service, final neural inference на LinQ обязателен. GPU не арендовали, модели/SDK/сервер не запускались. Кейс найден локально, root прочитал все20 страниц визуально по сохранённым рендерам: _WORK/CASE_NOTES.md; оригинал _WORK/INPUT/CASE_LINQ.pdf. VM/сервис обещаны, actual grant/SDK/device/model/GT отсутствуют. Заявление команды про1FPS и server-file mode — working assumptions, не контракт API/метрик.

Прочитай полностью оба входных договора, _WORK/CRITIC_HANDOFF.md, свой точный K текст ниже и указанные W1/source snapshots. Дальше получай новые первичные сетевые основания по узкому вопросу, а не повтор W1. Открывай фактический content и цепочки provenance, не пересказывай snippets. Даты/версии/commit/locators/author/access фиксируй; живые docs не lockfile. Если PDF bytes доступны, визуально проверь спорные tables/code/footnotes через PDF workflow; failed tool access vs actual closed file разделяй. При недоступном live source можно использовать сохранённый primary excerpt с атрибуцией, не выдавая его за свежий fetch. Copyright: пересказ+locators вместо длинных копий.

Собственный результат _WORK/W2_05.md; snapshots _WORK/MATERIALS_W2_05/. S/F префикс W2-05-. Каждый факт: source, locator, exact version/conditions, actual verification status, limitation, practical decision. Типы vendor claim/documentation/code/published measurement/local observation/inference/proposal/unknown; чтение кода не execution, чужой benchmark не наш. Общие ORT/Intel/NVIDIA возможности не доказывают LinQ. Неизвестность не доказательство отсутствия. Соседние отчёты secondary; их запуски не наши.

Никаких установок SDK, подключения сервера, аренды, training/model benchmarks, приложения, push/PR или сообщений людям. Допустимы маленькие read-only metadata/code inspection и явно аналитические расчёты там, где они нужны; не называй это модельным измерением. Команды/API только с фактической версией и основанием; pseudo-code явно. Опубликованные числа сохраняй вместе с setup, без переноса на LinQ/3090. Новые сильные зацепки можно развить, если меняют поставленный выбор, объяснив пользу.

В результате отдельный блок K dispositions: новый факт/source, что изменилось, closed/scope narrowed/contradiction/open/superseded, оставшийся риск и точный Q со способом закрытия. Не редактируй CRITIC или общие финальные файлы. Остановись при полезном новом основании/ограничивающем условии или содержательно локализованном unknown после адресного поиска; не искать закрытый SDK бесконечно. Короткая передача root:3 находки, блокер, следующий шаг, путь и K outcomes.

## Точный предмет и source targets критика

| W2_05.md | K007,K011 | Проверить, какие LinQ результаты реально опубликованы: pinned RUN_SCENARIO result paths, авторские release/results/logs, vendor presentation сноски. Не считать expected MLPerf VALID raw measured result; не приписывать TinyYOLO3 результат self-build YOLOv8. Target: pinned repo/author artifacts, official PDF, pytpu runtime code/docs по установленным версиям. Проверить completion barrier, FULL/RAW user IO scope, warmup/batch denominator в чужих numbers. Stop: evidence card на каждый пригодный результат, оставшиеся runtime-native неизвестные и matched-trace запрос; никаких запусков benchmark. |

## Исходная критика (сохранять историю)

## K007 — Публичный LinQ код и план запуска пока сильнее доказаны, чем опубликованный результат конкретного переноса

**Приоритет / закрытие:** P1 для research, P0 для заявления о выполненном переносе; WEB, затем TEST.

**Проблема и локатор.** W1-13 F15/F17, «Статусы доказательств»; W1-15 F04/F05; сохранённый RUN_SCENARIO §3.4 пишет final valid vendor TinyYOLO3 path, но также `MLPerf performance is expected to be VALID`. Это авторский сценарий/статус, а не автоматически прочитанный raw result. Self-build YOLOv8 source и его defects не являются ни успешным измерением YOLOv8, ни опровержением всей LinQ detection. Официальная презентация даёт иной источник — vendor-reported benchmark, без установленного custom-checkpoint fidelity.

**Что меняет для команды.** Возможны две симметричные ошибки: повысить наличие скрипта до «проверенный перенос YOLOv8», либо отвергнуть полезный vendor TinyYOLO3 опыт из-за ошибки другого скрипта. Нужен точный объект каждого опубликованного результата, особенно baseline identity.

**Недостающее доказательство.** Доступные result JSON/accuracy output/MLPerf logs/config/model hash или явная фиксация их отсутствия; dataset и decoder equality для source-target comparison; отличие performance-only от accuracy runs. Перепечатки одной таблицы остаются одной цепочкой.

**Узкое W2 / source targets / завершение.** **W2-05**: проследить указанные RUN_SCENARIO result paths в pinned linq-cv-bench и возможных связанных авторских release/result artifacts; отдельно открыть первичную таблицу vendor presentation с её сносками при доступных bytes/рендере. Для каждого результата дать «actually reported / merely proposed / artifact unavailable», исходную метрику и полный доступный контекст. Не запускать benchmark, не рисовать LinQ vs NVIDIA сравнение. Завершение: как минимум выяснено, что именно публичный материал измерил; отсутствие файлов не превращается в отсутствие функции/успеха, но ограничивает доказательную силу.

**Disposition W2:** PENDING.



## K011 — Completion и FULL/RAW остаются version-specific; без них нельзя интерпретировать latency и численный output

**Приоритет / закрытие:** P0 для фактического запуска; WEB частично, ARTIFACT+TEST.

**Проблема и локатор.** W1-14 F06–F08 и W1-15 F01/F03/E03/E06. Guide описывает blocking sync, сторонний runner предпочитает `.run` при наличии, а исторический pytpu15 Python binding передаёт mode native. Само наличие `.run`, byte pointer и user_dtype не доказывает completion, quant arithmetic или placement PRE/POST. Наряду с этим W1-15 нашёл warmup/batch accounting defect. «Inference FPS» из такого wrapper нельзя без дополнительных условий сравнить с source end-to-end throughput или временем до уведомления.

**Что меняет для команды.** Можно измерить enqueue вместо inference, повторно rescale user-format output или посчитать не тот denominator. Это способно испортить и качество, и доказательство TPU, даже если модель корректно скомпилирована.

**Недостающее доказательство.** Версионный runtime contract `.run/.sync`, result readiness, mode PRE/RAW/POST/FULL, tensor descriptors и reset/error behavior; для реального job — связка artifact/session/device/input/completion/output. Device inventory и service label отдельно полезны, но не дают этот proof.

**Узкое W2 / source targets / завершение.** **W2-05**: проследить доступную первичную документацию/код pytpu15 и более новых официально доступных runtime examples только до предела раскрытого API; отдельно отметить, чего Python binding не сообщает о native implementation. При анализе опубликованных timing logs из K007 проверить completion barrier, warmup в целых batches, completed real frames и named latency boundary. Выход — допустимые evidence levels для full SDK/restricted VM/catalog service и недостающий runtime artifact. Завершение: историческое поведение не переносится на выданный ABI; если актуальный contract закрыт, вопрос закрывается только matched manual+completed smoke trace, без бесконечного поиска.

**Disposition W2:** PENDING.



