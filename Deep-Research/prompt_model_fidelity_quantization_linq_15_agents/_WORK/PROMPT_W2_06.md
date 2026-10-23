# Индивидуальное поручение W2-06 — вторая волна

Роль: самостоятельный сетевой исследователь gpt-6.1-sol, effort=medium, fork_turns=none. Ты получаешь новый контекст, не запускай субагентов. Рабочая папка текущая; topic model_fidelity_quantization. Это согласованная вторая волна после15 W1 (12general/3LinQ) и отдельного fresh critic high. Команда пяти участников строит industrial safety video service, final neural inference на LinQ обязателен. GPU не арендовали, модели/SDK/сервер не запускались. Кейс найден локально, root прочитал все20 страниц визуально по сохранённым рендерам: _WORK/CASE_NOTES.md; оригинал _WORK/INPUT/CASE_LINQ.pdf. VM/сервис обещаны, actual grant/SDK/device/model/GT отсутствуют. Заявление команды про1FPS и server-file mode — working assumptions, не контракт API/метрик.

Прочитай полностью оба входных договора, _WORK/CRITIC_HANDOFF.md, свой точный K текст ниже и указанные W1/source snapshots. Дальше получай новые первичные сетевые основания по узкому вопросу, а не повтор W1. Открывай фактический content и цепочки provenance, не пересказывай snippets. Даты/версии/commit/locators/author/access фиксируй; живые docs не lockfile. Если PDF bytes доступны, визуально проверь спорные tables/code/footnotes через PDF workflow; failed tool access vs actual closed file разделяй. При недоступном live source можно использовать сохранённый primary excerpt с атрибуцией, не выдавая его за свежий fetch. Copyright: пересказ+locators вместо длинных копий.

Собственный результат _WORK/W2_06.md; snapshots _WORK/MATERIALS_W2_06/. S/F префикс W2-06-. Каждый факт: source, locator, exact version/conditions, actual verification status, limitation, practical decision. Типы vendor claim/documentation/code/published measurement/local observation/inference/proposal/unknown; чтение кода не execution, чужой benchmark не наш. Общие ORT/Intel/NVIDIA возможности не доказывают LinQ. Неизвестность не доказательство отсутствия. Соседние отчёты secondary; их запуски не наши.

Никаких установок SDK, подключения сервера, аренды, training/model benchmarks, приложения, push/PR или сообщений людям. Допустимы маленькие read-only metadata/code inspection и явно аналитические расчёты там, где они нужны; не называй это модельным измерением. Команды/API только с фактической версией и основанием; pseudo-code явно. Опубликованные числа сохраняй вместе с setup, без переноса на LinQ/3090. Новые сильные зацепки можно развить, если меняют поставленный выбор, объяснив пользу.

В результате отдельный блок K dispositions: новый факт/source, что изменилось, closed/scope narrowed/contradiction/open/superseded, оставшийся риск и точный Q со способом закрытия. Не редактируй CRITIC или общие финальные файлы. Остановись при полезном новом основании/ограничивающем условии или содержательно локализованном unknown после адресного поиска; не искать закрытый SDK бесконечно. Короткая передача root:3 находки, блокер, следующий шаг, путь и K outcomes.

## Точный предмет и source targets критика

| W2_06.md | K008 | Два exact export route cards как запасной выбор: один detector вне обычного YOLO Detect, один pose (например RT-DETR и выбранный RTMPose/SimCC). Target: official model config/source/export docs, version-matched MMDeploy если применим. Указать operators/shapes/outputs/decoder/preprocess/quant tooling/negative conditions и LinQ evidence level. Сопоставить с W2-02 и vendor-ready branch W2-05. Stop: следующий test и причина prefer/reject; имя семейства не поддержка LinQ. Не делать весь model_stack заново. |

## Исходная критика (сохранять историю)

## K008 — Смена архитектуры ещё не имеет достаточно конкретного запасного export-маршрута

**Приоритет / закрытие:** P1; WEB, затем ARTIFACT+TEST.

**Проблема и локатор.** W1-04 хорошо различает FasterRCNN, DETR/RT-DETR и SimCC; W1-08 дерево, шаг8 предлагает более совместимую архитектуру; W1-13 F20 не подтверждает их LinQ support. Но для альтернатив пока нет столь же цельного маршрута export/output/quantization как для Ultralytics Detect. «Сменить модель» может оказаться переходом к ROI/custom ops/attention/crop codec, которые сложнее исходной проблемы.

**Что меняет для команды.** При stop-loss нужен проверяемый запасной путь и критерий отказа, а не расширенный список брендов. Большее float качество или официальный ONNX export не гарантируют меньший риск LinQ import.

**Недостающее доказательство.** Два компактных, закреплённых route cards из разных семейств: исходная model/config identity, export tool и версии, output signature, ключевые operator/shape constraints, точка decoder/pose crop, PTQ/QAT tooling scope, реально подтверждённый уровень LinQ. Нужны также отрицательные условия, при которых route не является запасным.

**Узкое W2 / source targets / завершение.** **W2-06**: выбрать один detector вне обычного YOLO Detect и один pose-путь из уже релевантных W1 кандидатов; например RT-DETR и MMPose RTMPose/SimCC. По официальному source/config/export documentation (для MMPose — соответствующему MMDeploy пути, если он реально относится к выбранной конфигурации) собрать два exact route cards. Не обещать применимость любого SimCC codec ко всем RTMPose. Сравнить со static Ultralytics reference из W2-02 и vendor-ready model branch из W2-05. Завершение: по каждой альтернативе есть следующая проверка и причина предпочесть/отвергнуть её; LinQ UNKNOWN допускается и не маскируется общей export support.

**Disposition W2:** PENDING.



