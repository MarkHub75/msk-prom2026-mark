# Индивидуальное поручение W2-04 — вторая волна

Роль: самостоятельный сетевой исследователь gpt-6.1-sol, effort=medium, fork_turns=none. Ты получаешь новый контекст, не запускай субагентов. Рабочая папка текущая; topic model_fidelity_quantization. Это согласованная вторая волна после15 W1 (12general/3LinQ) и отдельного fresh critic high. Команда пяти участников строит industrial safety video service, final neural inference на LinQ обязателен. GPU не арендовали, модели/SDK/сервер не запускались. Кейс найден локально, root прочитал все20 страниц визуально по сохранённым рендерам: _WORK/CASE_NOTES.md; оригинал _WORK/INPUT/CASE_LINQ.pdf. VM/сервис обещаны, actual grant/SDK/device/model/GT отсутствуют. Заявление команды про1FPS и server-file mode — working assumptions, не контракт API/метрик.

Прочитай полностью оба входных договора, _WORK/CRITIC_HANDOFF.md, свой точный K текст ниже и указанные W1/source snapshots. Дальше получай новые первичные сетевые основания по узкому вопросу, а не повтор W1. Открывай фактический content и цепочки provenance, не пересказывай snippets. Даты/версии/commit/locators/author/access фиксируй; живые docs не lockfile. Если PDF bytes доступны, визуально проверь спорные tables/code/footnotes через PDF workflow; failed tool access vs actual closed file разделяй. При недоступном live source можно использовать сохранённый primary excerpt с атрибуцией, не выдавая его за свежий fetch. Copyright: пересказ+locators вместо длинных копий.

Собственный результат _WORK/W2_04.md; snapshots _WORK/MATERIALS_W2_04/. S/F префикс W2-04-. Каждый факт: source, locator, exact version/conditions, actual verification status, limitation, practical decision. Типы vendor claim/documentation/code/published measurement/local observation/inference/proposal/unknown; чтение кода не execution, чужой benchmark не наш. Общие ORT/Intel/NVIDIA возможности не доказывают LinQ. Неизвестность не доказательство отсутствия. Соседние отчёты secondary; их запуски не наши.

Никаких установок SDK, подключения сервера, аренды, training/model benchmarks, приложения, push/PR или сообщений людям. Допустимы маленькие read-only metadata/code inspection и явно аналитические расчёты там, где они нужны; не называй это модельным измерением. Команды/API только с фактической версией и основанием; pseudo-code явно. Опубликованные числа сохраняй вместе с setup, без переноса на LinQ/3090. Новые сильные зацепки можно развить, если меняют поставленный выбор, объяснив пользу.

В результате отдельный блок K dispositions: новый факт/source, что изменилось, closed/scope narrowed/contradiction/open/superseded, оставшийся риск и точный Q со способом закрытия. Не редактируй CRITIC или общие финальные файлы. Остановись при полезном новом основании/ограничивающем условии или содержательно локализованном unknown после адресного поиска; не искать закрытый SDK бесконечно. Короткая передача root:3 находки, блокер, следующий шаг, путь и K outcomes.

## Точный предмет и source targets критика

| W2_04.md | K006 |2–4 primary measurement cards CV PTQ/recovery: Wu arXiv2004.09602, BRECQ arXiv2102.05426/source и один релевантный official detection/pose deployment benchmark при наличии. Сохранить model/dataset/split/input/batch/precision/exclusions/hardware/software/metric/float→PTQ→recovered/cost, неизвестное явно. Минимум одно ограничивающее/negative condition. Stop: реальные reported outcomes помогают выбору; pose INT8 evidence при ненахождении остаётся UNKNOWN, DARK не substitute. |

## Исходная критика

## K006 — Сравнение методов лишено большей части доступных количественных опубликованных результатов

**Приоритет / закрытие:** P1; WEB.

**Проблема и локатор.** W1-07 F10 намеренно не переносит численные результаты paper; W1-08 F07/F14 сохраняет setup/итерации BRECQ, но не outcome; W1-09 HAWQ не использует benchmark gains; W1-10 не переносит SAHI gains. Ограничения верны, однако из них не следует, что числа нужно исключить даже как **чужие измерения с контекстом**. Сейчас «expected benefit (reported/estimated/tested)» рискует стать почти полностью качественным. Особенно мало прямого measurement evidence для CV PTQ/QAT и pose; сценарные аналитические примеры его не заменяют.

**Что меняет для команды.** Нельзя оценить, был ли метод в похожей CV задаче полезен лишь при4бит, восстанавливал ли8бит, какие операторы оставлялись float и сколько engineering/training работы он потребовал. Нужна поддержка выбора, без обещания тех же gains на LinQ.

**Недостающее доказательство.** Две–четыре сильные measurement cards: model/checkpoint, dataset/split, input/batch, W/A precision и exclusions, hardware/software, metric scale, float/PTQ/recovered outcomes, calibration/training cost и недостающие поля. «Аппаратное время не указано» допустимо, если так и написано; нельзя требовать полного идеального артефакта и выбрасывать остальные валидные данные.

**Узкое W2 / source targets / завершение.** **W2-04**: вернуться к авторским результатам Wu et al. arXiv2004.09602 и BRECQ arXiv2102.05426/official repo; дополнить одним первичным detection/pose результатом official deployment benchmark/model card, если он содержит действительное сравнение precision. Проверить negative/limiting result, например dependence на bitwidth, activation exclusions или model family. Зафиксировать абсолютные метрики и разности в их исходной шкале; source independence и source-vs-our measurement. Завершение:2–4 контекстные карточки меняют выбор метода; если прямого pose quantization сравнения не найдено, оно остаётся локализованным UNKNOWN, а DARK coordinate discretisation не выдаётся за INT8 evidence.

**Disposition W2:** PENDING.


