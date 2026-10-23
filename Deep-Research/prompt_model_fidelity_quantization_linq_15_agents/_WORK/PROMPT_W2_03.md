# Индивидуальное поручение W2-03 — вторая волна

Роль: самостоятельный сетевой исследователь gpt-6.1-sol, effort=medium, fork_turns=none. Ты получаешь новый контекст, не запускай субагентов. Рабочая папка текущая; topic model_fidelity_quantization. Это согласованная вторая волна после15 W1 (12general/3LinQ) и отдельного fresh critic high. Команда пяти участников строит industrial safety video service, final neural inference на LinQ обязателен. GPU не арендовали, модели/SDK/сервер не запускались. Кейс найден локально, root прочитал все20 страниц визуально по сохранённым рендерам: _WORK/CASE_NOTES.md; оригинал _WORK/INPUT/CASE_LINQ.pdf. VM/сервис обещаны, actual grant/SDK/device/model/GT отсутствуют. Заявление команды про1FPS и server-file mode — working assumptions, не контракт API/метрик.

Прочитай полностью оба входных договора, _WORK/CRITIC_HANDOFF.md, свой точный K текст ниже и указанные W1/source snapshots. Дальше получай новые первичные сетевые основания по узкому вопросу, а не повтор W1. Открывай фактический content и цепочки provenance, не пересказывай snippets. Даты/версии/commit/locators/author/access фиксируй; живые docs не lockfile. Если PDF bytes доступны, визуально проверь спорные tables/code/footnotes через PDF workflow; failed tool access vs actual closed file разделяй. При недоступном live source можно использовать сохранённый primary excerpt с атрибуцией, не выдавая его за свежий fetch. Copyright: пересказ+locators вместо длинных копий.

Собственный результат _WORK/W2_03.md; snapshots _WORK/MATERIALS_W2_03/. S/F префикс W2-03-. Каждый факт: source, locator, exact version/conditions, actual verification status, limitation, practical decision. Типы vendor claim/documentation/code/published measurement/local observation/inference/proposal/unknown; чтение кода не execution, чужой benchmark не наш. Общие ORT/Intel/NVIDIA возможности не доказывают LinQ. Неизвестность не доказательство отсутствия. Соседние отчёты secondary; их запуски не наши.

Никаких установок SDK, подключения сервера, аренды, training/model benchmarks, приложения, push/PR или сообщений людям. Допустимы маленькие read-only metadata/code inspection и явно аналитические расчёты там, где они нужны; не называй это модельным измерением. Команды/API только с фактической версией и основанием; pseudo-code явно. Опубликованные числа сохраняй вместе с setup, без переноса на LinQ/3090. Новые сильные зацепки можно развить, если меняют поставленный выбор, объяснив пользу.

В результате отдельный блок K dispositions: новый факт/source, что изменилось, closed/scope narrowed/contradiction/open/superseded, оставшийся риск и точный Q со способом закрытия. Не редактируй CRITIC или общие финальные файлы. Остановись при полезном новом основании/ограничивающем условии или содержательно локализованном unknown после адресного поиска; не искать закрытый SDK бесконечно. Короткая передача root:3 находки, блокер, следующий шаг, путь и K outcomes.

## Точный предмет и source targets критика

| W2_03.md | K004,K005 | Установить объект LinQ percentile и наличие consumer для QDQ/encodings/QAT/mixed precision. Target: version-specific official API/source/sample; W1-14 guide и build code; ORT/NNCF/AIMET только для различения арифметики. Отдельно ограниченно разрешить ORT auto_mixed_precision docs/code CPU/GPU конфликт exact tag+ORT version. Stop: confirmed/unknown/contradicted capability matrix и proof перед GPU; отсутствие public evidence не назвать отсутствием функции. |

## Исходная критика (сохранять историю)

## K004 — LinQ percentile нельзя включать в общий calibration sweep до выяснения объекта параметра

**Приоритет / закрытие:** P0 для sweep; WEB частично, ARTIFACT+TEST.

**Проблема и локатор.** W1-07 «Проверенные реализации» и матрица B; W1-14 F02/F03/E02/E03; W1-13 F11. Общие ORT activation histogram percentile и NNCF per-sample quantile уже хорошо различены. Однако guide LinQ описывает percentile через **весовые коэффициенты**, а сторонний RegularModel.calibrate имеет иной API и blanket TypeError retry. Ни одинаковое имя, ни разные requested CLI values не устанавливают несколько разных activation-calibration опытов.

**Что меняет для команды.** Можно потратить время на мнимый sweep, неверно объяснить улучшение rare-class recall либо выбрать диапазоны, которые вообще не были применены. Сначала effective config, затем экспериментальный фактор.

**Недостающее доказательство.** Формула/scope параметра конкретного release, supported numeric domain, место применения до/после weight quantization, actual thresholds/encodings, лог успешного fresh-model вызова без скрытого retry. Изменение activation thresholds само по себе не доказывает прямой activation percentile — оно может быть следствием изменённых весов.

**Узкое W2 / source targets / завершение.** **W2-03**: адресно искать определение percentile в официальном API/исходнике именно LinQ и сравнить его с прочитанными версиями ORT/NNCF. Выдать таблицу «weights/activations/оба/не установлено; requested/effective; доказательство». Если текущая реализация закрыта, закончить точным SDK-вопросом и двухфакторным micrograph plan из E03, без нового перебора общих calibration статей. Завершение: нельзя интерпретировать параметр сверх найденного определения; окончательный effect остаётся TEST.

**Disposition W2:** PENDING.



## K005 — QAT/mixed precision описаны предметно, но у целевого compiler нет доказанного consumer численного контракта

**Приоритет / закрытие:** P0 до расхода GPU; WEB частично, ARTIFACT+TEST.

**Проблема и локатор.** W1-08 F01/F04/F11/F15, downstream export contract; W1-09 F10–F13 и FP island discussion; W1-14 Q14-03. Наличие ONNX QDQ, AIMET encodings, FP32 block или обученных scales не устанавливает, что LinQ их импортирует и сохраняет. При float-import+recalibration AdaRound может оптимизировать другую сетку; FP island после уже округлённого feature map не возвращает потерянную информацию. Это честно признано W1, но остаётся главным условием применимости «следующего метода спасения».

**Что меняет для команды.** До установления consumer нельзя обосновать ни дополнительный GPU trial, ни обещание selective precision. Нужна развилка «сохраняется explicit contract / можно симулировать native quantizer / остаются только поддерживаемый PTQ и смена модели».

**Недостающее доказательство.** Для реального SDK — допустимые W/A/bias/accumulator types, rounding/saturation, scale/zero-point/axis, QDQ/sidecar preservation, supported precision boundaries и placement. Для ORT auto-mixed path отдельно остаётся конкретное docs/code расхождение CPU/GPU из W1-09 F10; это не блокирует ручную диагностику и не должно превращаться в утверждение, что mixed precision вообще невозможна.

**Узкое W2 / source targets / завершение.** **W2-03**: искать только vendor-specific QAT/imported-encodings/mixed-precision path и ограничивающие условия; результаты иных производителей использовать как описание требования, не поддержку LinQ. Для локального альтернативного инструмента разрешить конфликт W1-09 на exact package tag/release и ORT EP/kernel version по первичному code/docs, без запуска/установки. Выход — capability table confirmed/unknown/contradicted с одним минимальным proof перед обучением. Завершение: найден реальный consumer либо выбор остаётся условным и вынесен в вопрос инженеру; не требовать ещё статей QAT для закрытия SDK неизвестности.

**Disposition W2:** PENDING.



