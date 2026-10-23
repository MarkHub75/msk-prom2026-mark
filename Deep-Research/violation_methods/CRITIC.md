# Критика первой волны violation_methods

Этап: fresh-context CRITIC после W1, до W2. Дата: 2026-10-23, Europe/Moscow (+03:00). Прочитаны полностью оба входных промпта, `_WORK/PLAN.md`, `_WORK/W1_A.md`, `_WORK/W1_B.md`, `_WORK/W1_C.md`, три `SOURCES_*/EVIDENCE.md` и журналы поиска A/B; журнал C включён в его EVIDENCE. Нового интернет-поиска, инференса и benchmark не проводилось. Проверяется доказательная картина первой волны, а не ещё не существующие итоговые отчёты. Ниже сохранены исходные замечания; результаты W2 должен добавить сборщик, не переписывая первоначальную критику.

Первая волна уже даёт полезный базовый маршрут: наблюдаемое состояние части тела/пола → связь с субъектом → трёхзначные предикаты → подтверждение по времени источника → событие с причинами потери наблюдения. Основной дефицит сосредоточен в двух примерах анонса — RGB-курении и промышленном респираторе вне лица, — а также в первичных следах промышленных условий и приёмки. Перебирать заново семейства детекторов, pose и трекеров не требуется. Есть одна конкретная семантическая ошибка, которую нужно исправить до синтеза: отсутствие подтверждения курения нельзя называть соблюдением; наблюдение запасного СИЗ вне тела нельзя автоматически превращать в отсутствие защиты на теле.

## Покрытие карты первой волны

«Достаточно» означает достаточно для условного выбора метода и честного ограничения, а не проверенную работоспособность на камерах кейса.

| Ячейка | Оценка покрытия | Что меняет W2 |
|---|---|---|
| C01 определения СИЗ | Сильная схема наблюдаемости и локальной политики; требуется уточнение единицы состояния | K001: item instance против body-part coverage |
| C02 постановка СИЗ | Достаточное сравнение; есть same-detector опровержение универсального превосходства pose | Повторный обзор не нужен |
| C03 ownership | Конкретная предлагаемая геометрия и честно локализованный дефицит crowd benchmark | Целевой выигрыш решается E-A02; не требовать ещё общего HOI-обзора |
| C04 малые СИЗ/респиратор | Условия видимости и различие medical/industrial установлены; direct off-face evidence не получено | K003 |
| C05 unknown/selective | Достаточно теории, интерфейсов и ограничений переноса; E-A04/05 содержательны | Наш FA/coverage tradeoff только эксперимент |
| C06 геометрия зон | Достаточно первичных реализаций anchors, crossing и ограничений плоскости | Значение зоны — постановщик, геометрическая ошибка — E-B01/02 |
| C07 техника | Полезная лестница от image ROI до ground envelope; отдельно activation/authorization | Без видео/калибровки не закрывается поиском |
| C08 трекинг | Достаточно для ByteTrack baseline и осмысленного второго кандидата; fixed dt и ReID gates прочитаны | Фактический low-FPS выбор — E-B03 |
| C09 временная логика | Хорошо разделены dwell, lifecycle, grouping, cooldown; DOC/CODE lead ещё не замкнут | K006 |
| C10 правила/события/GT | Практичная авторская схема, статусы обозначены; промышленного приёмочного протокола нет | K005; не превращать DCASE в CCTV-стандарт |
| C11 smoking | Корректные кандидаты и hard negatives, но слабое сравнительное RGB evidence; ошибка триады | K001/K002 |
| C12 fall/hook | Сильное опровержение harness→attached; опубликованный temporal fall method не разобран, hook lead открыт | Ограниченная необязательная ветка K007 |
| C13 камеры/среда | Есть конкретные Bosch/Macroscop условия; реальные средовые цифры и отрицательные следы крайне узки | K004/K005 |
| C14 OVD/VLM | Fixed vocabulary vs dynamic graph обосновано; реальная польза verifier не подтверждена | Ограниченный поиск K008; затем E-C04, а не обещание |
| C15 LinQ/INT8 | Достаточная методическая матрица требований и раздельные gates; конкретная поддержка не установлена | Не расширять до исследования SDK; нужны артефакт/доступ/постановщик |

## Замечания и точные задачи второй волны

### K001 — статус «не подтверждено» и состояние отдельного предмета смешиваются с соблюдением

**Приоритет: P0, исправить до остальных выводов о событиях.**

**Затронутый материал.** `_WORK/W1_C.md`, C11, абзац «Состояния для событий»: compliant определяется через «ни action, ни нарушение зоны не подтверждены». `_WORK/W1_A.md`, C01, `state=on_target_part/off_target_part/absent_visible/unknown` и строки таблицы «Очки»/«Респиратор»; C04, таксономия off-face. Контрольное основание уже есть в W1_B C10: трёхзначный AND и `NOT unknown = unknown`.

**Проблема.** Неподтверждённое действие может быть unknown. Для `smoking AND hazardous_zone` соблюдение правила следует из установленной ложности хотя бы одного необходимого предиката, а не из отсутствия подтверждения обоих. Человек с видимой сигаретой вне опасной зоны не нарушает именно это правило, хотя smoking=true. В СИЗ `off_target_part` — отношение конкретного предмета, а `protected/not protected` — состояние части тела: у человека могут быть надетые очки и запасная пара на лбу/в руке, либо надетый респиратор и второй на шее. Для каски таблица A уже требует видимой голой головы; такую защиту от ложного вывода надо последовательно сохранить и для остальных СИЗ.

**Последствие.** Ошибочные compliant при невидимом лице и false violation от запасного предмета; разная разметка A/B/C, неверный GT и перенос логики в будущий код.

**Нужное доказательство.** Здесь не требуется новый benchmark: достаточно явной семантики предикатов и проверяемых ручных контрпримеров. Источники A-S07/08 и B C10 уже поддерживают разделение item/bodypart/coverage и трёхзначную логику.

**W2-задача.** Согласовать таблицу истинности `observed protection state × requirement × zone × action` с раздельными true/false/unknown; ввести item instance и body-part coverage как разные записи либо явно оговорить ограничение one-item. Разобрать вручную пять трасс: smoking неизвестен внутри зоны; smoking=true снаружи; smoking=true при неизвестной зоне; запасные очки/респиратор off-body при надетой защите; off-body виден, целевая часть скрыта. Указать корректный rule result и что требуется увидеть для negative. Это исследовательская спецификация, не создание приложения. Не объявлять unknown-safe.

### K002 — маршрут RGB-курения выбран по слишком узкой и неоднозначной первичной базе

**Приоритет: P0 для четырёх примеров анонса.**

**Затронутый материал.** `_WORK/W1_C.md`, C11 «Практический каскад» и «Условный выбор C11»; `SOURCES_C/EVIDENCE.md`, C-S05/F05, C-S06/F06, C-S07/F07; журнал smoking queries и недоступный Domination.

**Проблема.** Единственная прочитанная RGB clip-работа имеет 16/32-frame несогласованность, неясный negative split и сравнение на 20 клипах. Патент не даёт измеренной валидации; TP-LINK использует температуру. Это достаточно для списка кандидатов и объяснения трудности, но недостаточно, чтобы сравнить object-only, gesture-only и object+temporal route именно на похожих не-курениях. Не установлен полезный минимум наблюдаемости RGB smoking-продукта; search-index Domination не является таким минимумом.

**Последствие.** Команда может затратить часы на сигаретный detector там, где нужен action candidate, либо на тяжёлый clip graph там, где простого крупного object cue достаточно. Формулировка «курение поддержано» станет шире реально обоснованного.

**Нужное доказательство.** Прочитанная оригинальная RGB smoking работа/авторский код/руководство, раскрывающие признаки, scene/view/target size, temporal input, test split и состав hard negatives; полезно сравнительное или отрицательное свидетельство. Thermal/IMU материалы отделять от RGB. Никакой обязательной квоты источников.

**W2-задача.** Развить точечные цепочки RGB cigarette+gesture/hand-mouth action → full text → code/issues или manual. В первую очередь попытаться получить body Domination независимым доступным путём либо сопоставимый настоящий RGB manual; извлечь условия только из реально прочитанного. Сопоставить object и action подходы по наблюдаемым cue, sampling window, ошибкам от drink/eat/phone/PPE adjustment, числу neural inputs и пределу результата. Проверить, есть ли действительно held-out negatives/camera transfer и event denominator. Если прямого matched comparison нет, зафиксировать это и сохранить два условных baseline для C-E01, не ранжируя их по чужим несопоставимым AP.

### K003 — промышленный респиратор off-face остаётся предложенной таксономией без завершённого практического следа

**Приоритет: P0.**

**Затронутый материал.** `_WORK/W1_A.md`, C04, Q-A03/Q-A05; `SOURCES_A/EVIDENCE.md`, S04/F05 (SH17 on/off), S13/F20–21 (industrial head crops), S17/F25 (checkpoint abstract); журнал поиска A, цепочка 5 и недоступные gasmask/MAFA источники. `_WORK/W1_C.md`, C13/С15.

**Проблема.** Установлено, почему medical-mask class не решает industrial respirator. Но direct neck/hand/on-face benchmark не найден, extended on/off tags SH17 не инспектированы в поставке, industrial cartridge result имеет оговорки в метриках. При этом для примера «снят респиратор» критична разница состояния uncovered/off-face и действия снятия. Входы для реализации уже видимого состояния ещё не доведены до конкретной семантики реально доступного артефакта.

**Последствие.** Есть риск взять generic mask веса и обнаружить после старта, что они не содержат ни нужный тип, ни off-body состояния. Равным образом нельзя требовать off-face detector, если требование решается наблюдаемым uncovered face.

**Нужное доказательство.** Прочитанная annotation guide/файл классов/небольшой пример реальных annotations для on/off, либо full text промышленного/контрольного пункта с точными состояниями и ограничениями. Нужна семантика, а не каталог весов и лицензий. Отсутствие публичных данных допустимо как результат локализованного поиска.

**W2-задача.** Проследить SH17 extended tag → официальный annotation artifact/пример и установить, доступны ли отношения wearer/on-off и распространяются ли они на mask/respirator или лишь generic object. Отдельно проверить целевую первичную цепочку respirator worn/removed/neck/hand с industrial half-face/cartridge/N95, не подменяя её COVID mask. Сохранить матрицу: что источник реально различает, annotation unit, source visibility, negative/unknown, переход или состояние. Итогом должны стать две условные постановки — `face visibly uncovered under requirement` и `observed removal transition` — с минимальными входами и stop condition при невидимом лице. Наличие готовой модели и LinQ-исполнение не выводить из статьи.

### K004 — численные условия камер получены, но средовые отказы покрыты преимущественно физическими объяснениями

**Приоритет: P1; закрывает применимость основных сценариев.**

**Затронутый материал.** `_WORK/W1_C.md`, C13, абзац «Ночь/ИК» и C-E03; C-S01/F01, C-S02/F02, C-S14/F14; A-S12/F18 (единственное конкретное low-light gloves failure). В W1_A C04 и E-A03 transfer на реальные камеры оставлен эксперименту.

**Проблема.** Bosch/Macroscop дают хорошие product-specific admission conditions, но night/IR, compression, dust/steam, topview и domain shift в основном перечислены качественно. Первичного анализа с режимом съёмки, измеренным отказом или issue/repro для этих факторов почти нет. Нельзя все такие случаи закрыть одной фразой «unknown»: важно знать, какая информация исчезла физически, а где помогают native crops/смена preprocessing/отдельный режим.

**Последствие.** Камерные условия будут честными, но слишком общими для выбора wide view против checkpoint и для ответа на вопрос жюри о night/IR. Утверждение об эффективности crop/tiling в конкретной среде может превысить основание SAHI VisDrone.

**Нужное доказательство.** Первичный product manual, deployment/error analysis, code issue с воспроизводимым контекстом или оригинальное испытание PPE/smoking в одной из ключевых сред. Нужны режим, target/camera units и что именно мерили; чужой общий robustness benchmark не превращать в PPE-цифры.

**W2-задача.** Искать не все погодные эффекты симметрично, а два решающих разрыва: RGB→night/IR для helmet/vest/face-PPE и потерю малых объектов от input resize/compression/blur. Следовать сильной цепочке до первичного условия/ошибки; проверить, не требует ли рекомендованная компенсация другой камеры, освещения или модели. По пыли/пару/topview, если нет прямых данных, локализовать неизвестное после содержательного поиска. Сформировать маленькую таблицу «симптом → что наблюдаемо → допустимая компенсация → когда abstain → какой E slice». Не придумывать универсальные проценты деградации или новые pixel thresholds.

### K005 — требование промышленного заказчика и приёмка всё ещё не связаны в одну проверяемую цепочку

**Приоритет: P1.**

**Затронутый материал.** A-S16/F24, Q-A07; `_WORK/SOURCES_B/SEARCH_LOG.md`, раздел закупок, Q-B08; C-Q08. W1_B C10 использует DCASE как явно ограниченный пример temporal matching.

**Проблема.** Найденный itdf документ — грантовое КД-ТЗ с «достоверностью» без достаточного denominator; это не подтверждённая закупка промышленной системы и не measured acceptance. В остальных ветках есть поисковые запросы, но не конкретный industrial заказчик → контракт/ТЗ → условия испытания → параметры события. Это важнейший недополученный практический тип источника из задания. Существующая авторская event-методика полезна и не должна ждать закупки, но она не становится отраслевым нормативом.

**Последствие.** Нельзя обосновать числом 95/98% ни собственный prototype, ни отраслевые требования к FA/hour, задержке или наблюдаемости. Нельзя также называть поля авторского matcher доказанной промышленной приёмкой.

**Нужное доказательство.** Оригинальное вложение конкретного промышленного тендера/заказчика, руководство испытаний или протокол с идентификатором/датой/версией и определением хотя бы части: event, negative observation time, duplicates, response time, camera conditions. Requirement и achieved result разнести; приёмочный результат не обязателен, если доступно только ТЗ.

**W2-задача.** Уйти от повторения общих запросов W1 к цепочкам конкретных HSE/PPE/zone продуктов и промышленных заказчиков, корпоративным площадкам и оригинальным вложениям. Проверять подходящие карточки по full attachment, не по агрегатору. Для удачной цепочки сохранить реквизиты и точный clause, denominator/scene/время или явно их отсутствие. Попытаться пройти к программе/протоколу испытаний. Если ответ не найден, закрыть сетевую часть точным searched scope и передать постановщику запрос реального acceptance protocol; не продлевать поиск бесконечно и не подменять его городской охранной аналитикой.

### K006 — Frigate DOC/CODE расхождение полезно, но незамкнутый caller lifecycle нельзя усиливать до установленной семантики системы

**Приоритет: P1, узкая проверка сильной зацепки.**

**Затронутый материал.** `_WORK/W1_B.md`, вводное «Что меняет выбор команды», C09 и E-B04/Q-B07; `SOURCES_B/EVIDENCE.md`, S01, S06/F06–F07, pinned commit `cfa08c56b23d23280c3d0a218e5a43182c97445b`.

**Проблема.** Прочитанный update действительно даёт содержательный повод проверить reset inertia/loitering и fresh measurement. Автор правильно не называет это runtime bug. Но online docs unpinned, а полный caller/lifecycle не прочитан; неизвестно, где именно инициализируются/меняются zone counters и какие stale obj_data доходят до этого участка. Вывод во вступлении звучит несколько завершённее, чем ограничение карточки F06.

**Последствие.** В итоговом тексте легко превратить осторожный lead в неверный тезис «Frigate накапливает не подряд» или использовать его как доказательство дефекта чужого продукта. Команде полезнее точно воспроизводимая семантика оператора, чем неподтверждённый bug claim.

**Нужное доказательство.** Статическая цепочка pinned кода: initialization → caller/update cadence → in/out/stale paths → reset/end/new track; при возможности — docs того же tag либо честное различие версий. Runtime эффект отдельно остаётся непроверенным, если не исполнялся.

**W2-задача.** Прочитать caller и все записи в `zone_presence`/`zone_loitering`/счётчики нужного объекта на этом commit; составить ручные трассы `in,out,in`, `in,dwell,exit,reentry`, prediction-only и new track. Для каждой строки указать функцию/ветку и изменение state, явно отметить непроверенные допущения. Можно проверить issue/commit обсуждение того же поведения, сохранив самостоятельность происхождения. Это узкое чтение и логическая трассировка, не запуск VMS/benchmark. Если статической базы недостаточно, ослабить вывод до «требует replay E-B04»; не обещать новый runtime результат.

### K007 — второстепенные fall/hook сценарии содержат правильные запреты, но мало основания для выбора положительного метода

**Приоритет: P2; не вытеснять четыре примера анонса.**

**Затронутый материал.** `_WORK/W1_C.md`, C12/C-E02; C-S03/F03, C-S04/F04 (lying product), C-S08/F08 (Lim failure), C-S20/F20 (HDS-YOLOv5 abstract), C-Q06.

**Проблема.** Надёжно доказано, что один продукт фактически ищет lying, а Lim не распознал hook и не реализовал connection. Но положительная временная fall-постановка изложена как общая идея без прочитанного оригинального алгоритма/отрицательных примеров. Утверждение «должен наблюдать ... устойчивое последующее состояние» слишком жёстко как общее определение: падение с быстрым восстановлением всё равно падение. HDS hook-status lead содержательно не проверен; конкретная новая работа может ограничить слишком широкий вывод «attachment по видео не решён».

**Последствие.** Нельзя быстро выбрать метод, если полный кейс добавит fall или clipped hook; можно ошибочно исключить падение без лежания либо принять hook presence за connection.

**Нужное доказательство.** Full text C-S20 с class/annotation semantics; для fall — одна действительно прочитанная первичная temporal постановка и её intentional lying/fast recovery ограничения. Не нужны большой каталог action-моделей и медицинская диагностика.

**W2-задача.** Проверить HDS-YOLOv5 на точный смысл classes/GT: hook present, used/unused, geometric relation, mechanically connected, gate locked; выписать тестовые условия и что доказательством не является. Если доступ не получен, записать границу. Найти исходный temporal fall method с негативными действиями и раздельными transition/posture endpoints; уточнить правило suspected_fall так, чтобы lying persistence была возможным cue, а не необходимым определением всех падений. Сохранить conditional route для case-added сценария. Если после targeted поиска нет подходящей базы, явно отложить fall-event/hook connection до данных, не выдавать лежачий detector за замену.

### K008 — практическая ценность VLM-verifier пока сведена к гипотезе; поиск должен проверить именно каскадную пользу

**Приоритет: P2, опциональный путь; не блокирует detector+rules.**

**Затронутый материал.** `_WORK/W1_C.md`, C14, C-F28, C-E04; C-S12/F12 (POPE2023, abstract/introduction), журнал C, VLM group.

**Проблема.** POPE корректно доказывает возможность object hallucination у изученных моделей, но ничего не говорит о net benefit verifier на CCTV candidates, lost TP, negative scenes, latency или современных выбранных вариантах. W1 честно не обещает снижение FA. При этом поиск в основном закончился на общем hallucination benchmark, а не на первичном опыте detector→VLM verification, который прямо запрошен темой.

**Последствие.** «Killer feature» остаётся неранжируемой: неизвестно, существует ли подходящий опубликованный practical trace, либо эту ветку разумнее сразу оставить только эксперименту. Общий benchmark не обосновывает ни успех, ни бесполезность конкретного каскада.

**Нужное доказательство.** Оригинальная работа/авторский code/первичное испытание, где VLM проверяет уже найденные CCTV/safety/action candidates и доступны paired errors или достаточно точные operating conditions. Желательно ограничивающее/отрицательное свидетельство. Generic VQA accuracy или ещё один POPE-пересказ не закрывают вопрос.

**W2-задача.** Выполнить ограниченный targeted поиск detector alarm verification / video anomaly false alarm VLM с industrial/surveillance контекстом. Для найденного первичного материала установить candidate selection, crop/context/frame sampling, model/version/prompt, paired FP rescue и TP loss, event/frame unit, latency hardware и split. Если независимого прямого исследования нет, так и зафиксировать; не собирать список моделей. Оставить C-E04 как единственный путь выбора нашего verifier. Условие исполнения всей neural chain на LinQ остаётся вопросом постановщику, не предметом домысла W2.

## Что уже установлено достаточно и не нуждается в повторном обзорном поиске

1. **Геометрия и семантика классов различаются.** SHWD `person` — negative head, SH17 head/face/mask не означают bare head/industrial respirator, Pictor W/WH/WV/WHV — комбинации состояний. A-S01–05/F01–09 достаточно для запрета слепого merge. Остаток доступности on/off artifact — узкий K003, а не новая инвентаризация датасетов.
2. **Pose не универсальный победитель.** A-S05/F08 даёт same-detector/same-training сравнение и small-scale контрпример. Этого достаточно, чтобы начинать с простой association и выбирать pose по E-A02, не по репутации.
3. **Unknown имеет практическое основание.** AWS person/bodypart/item/coverage+indeterminate и Macroscop невидимое лицо подтверждают такой интерфейс; selective risk–coverage имеет чёткие предпосылки. A-S07–11/F12–17. Ни один из этих источников не измеряет качество нашего gate.
4. **RGB не подтверждает fit/seal/фильтр/прочность anchor.** A-S10/F15 и C-S08/F08 вместе с физической границей наблюдения достаточно ограничивают обещания. Дополнительный юридический обзор не нужен.
5. **Floor ROI требует явно выбранного anchor; image ROI не даёт метры/3D.** B-S01/S09–11/F01/F10/F12–13 и B-S17/F19 поддерживают условный выбор bottom center и planar ограничения. Конкретная ошибка остаётся эксперименту.
6. **Tracker ID не является личностью и не гарантирует события.** B-S12–14/F14–16 дают достаточно оснований про fixed dt, weak detections, low-FPS IoU и ReID gating. Не нужен новый общий рейтинг MOT; E-B03 ответит на целевой event tradeoff.
7. **Dwell, object age, grouping cutoff и notification cooldown различны.** B-S01–08/S15–16/F01–09/F17–18 достаточно; точный Frigate counter lead отдельно K006. Числа defaults не универсальные стартовые нормы.
8. **Условия Bosch/Macroscop численно пригодны как условия конкретного продукта.** C-F01/02 и A-F16/17 можно сохранить с единицами, resolution, revision и scope. Это одна общая цепочка Macroscop, а не независимые подтверждения A и C. DORI25/63/125/250 px/m — человеческие DORI-категории, не PPE admission threshold.
9. **Fixed vocabulary OVD и dynamic text graph — разные нагрузки.** C-S09–11/F09–11 достаточны для этого методического вывода. Не установлено ни качество small PPE, ни компиляция LinQ. Универсально объявлять attention unsupported или INT8 непригодным нельзя.
10. **INT8 требует отдельного quality gate, а не только compile pass.** C-S15/16/F15/16 дают механизм и конкретный контрпример. Размер эффекта для выбранных PPE/pose нельзя достроить из PeopleNet/ViT. C-E05 достаточно содержателен как будущая проверка.

Нет основания объявлять W1_A/B/C независимыми экспериментальными подтверждениями: это исследователи, читающие источники. Повторное чтение Macroscop и официального анонса сохраняется одним происхождением. README, статья и авторский код одного метода помогают уточнять разные утверждения, но не дают три независимые репликации.

## Что не закроется одним новым интернет-поиском

| Неизвестное | Кто/что закрывает | Решение команды |
|---|---|---|
| Обязательные нарушения, допустимые PPE-типы, снятие как transition или off-face state, смысл опасной зоны, минимальный важный эпизод/latency, отношение к unknown | полный кейс и постановщик | taxonomy, GT, приоритет функций и допустимое подтверждение |
| Какие neural stages обязаны работать на LinQ, назначенные hardware/SDK/compiler и доступные artifacts | постановщик + доступ к LinQ/SDK | допустимость verifier/ReID/pose/cascade, граница CPU |
| Наблюдаемость головы/лица/кистей/сигареты в реальных source streams, night/IR, настоящий crop budget | реальные видео + E-A03/C-E01/C-E03 | включать метод, ограничить поддерживаемый camera region или перейти к checkpoint |
| Наш выигрыш geometry/pose ownership и ошибки запасного/соседнего СИЗ | целевой relation GT + E-A02 | оправдан ли дополнительный neural stage |
| Стабильность tracker/events при реальном LinQ cadence, jitter, gaps, out-of-order | measured cadence + E-B03/04 | tracker, max gap, confirmation и loss policy |
| Coverage/recall цена abstention, stale best-frame policy, фактические FA/hour | длительные target negatives и E-A04/05/E-B04 | deployment admission и честные метрики |
| Наш VLM net benefit и FP/INT8→event drift | неизменный candidate/GT set + C-E04/05 на назначенном исполнении | включить/отключить verifier, выбрать precision route |

Найденный чужой threshold или benchmark может помочь спроектировать проверку, но не заменит её. Ни один E-ID первой волны не выполнен; предполагаемая будущая проверка не закрывает замечание сейчас.

## Группировка W2 для оркестратора

- **W2_A, наблюдаемый предикат и респиратор:** K001 + K003. Сначала согласовать триаду и scope item/bodypart, затем проверить реально доступные on/off semantics. Это P0, с передачей event contract в W2_B/C. Нужны конкретные annotation/manual evidence, а не каталог моделей.
- **W2_B, промышленная практика и события:** K004 + K005 + K006. Приоритет — первичные условия и industrial attachment chain; Frigate проверить узко по pinned caller, не превращать в исследование всей VMS. К K004 можно привлечь находки соседнего пакета smoking.
- **W2_C, действия и опциональный verifier:** K002 в первую очередь; K007/K008 ограничить оставшимся содержательным поиском, не вытеснять четыре примера анонса. Сначала RGB smoking и hard negatives; затем точные hook classes/fall endpoint и direct VLM cascade evidence.

Каждый пакет должен вернуть для своих K-ID: новый ответ и происхождение; закрыто / уточнена область / противоречие / осталось открытым; что это меняет в выборе метода; какой остаток передаётся E-ID/постановщику. Сетевую недоступность сохранять как результат доступа, а не отрицательное доказательство существования метода. Новых общих агентов-аудиторов и третьей волны для этих вопросов не требуется.

## Обработка замечаний после W2

На момент исходной критики результаты W2 ещё не получены. Этот раздел предназначен сборщику для добавления статусов и ссылок на реальные W2 S/F, без ретроспективного изменения K001–K008.

## Добавление COLLECTOR: результаты двух волн

Дата сборки:2026-10-23, Europe/Moscow(+03:00). Исходный текст критики выше сохранён без ретроспективной правки. Ниже обработка реальных W2_A/B/C, а не финальный аудит или новая исследовательская волна. Новых сетевых запросов, моделей и подагентов сборщик не выполнял; все E остаются предложениями.

<a id="k001"></a>
### K001 — закрыто семантически; качество получения предикатов не измерено

W2_A разделила item observation и target coverage; coverageT может дать любой надетый approved item, spare off-body не даёт coverageF. Полные Strong Kleene AND/NOT таблицы факторизуют27 C/R/Z и81 с action; пять ручных counterexamples разобраны. [F100](RAW_FACTS.md#f100)/F102/F119, источники [S007](SOURCES.md#s007)/S008 и локальный counterexample [F067](RAW_FACTS.md#f067). W1_C фраза «ни action, ни нарушение зоны не подтверждены→compliant» **superseded**. Missing cue→U, F compound-rule не global compliance; observed negative требует отдельного контракта. Остаток [Q001](OPEN_QUESTIONS.md#q001)/Q008/Q009/Q013; [E001](OPEN_QUESTIONS.md#e001)/E010/E011/E016. Ручные логические трассы не benchmark.

<a id="k002"></a>
### K002 — область существенно уточнена; matched route benefit открыт

W2_C получила parsed primary RGB Domination1.17 §8.8 ([F090](RAW_FACTS.md#f090)/S072, visual QA недоступна), две fulltext cigarette object работы ([F091](RAW_FACTS.md#f091)/F092), pinned fusion code с global history/first boxes/no ownership ([F093](RAW_FACTS.md#f093)). Это обосновывает условный face/object route и ограничение scene/face size, а также опровергает автоматический вывод из слова smoking/temporal. Product optimum100px не universal minimum; thermal TP-LINK5–10m остаётся иной модальностью. Matched object/gesture/object+temporal test с eat/drink/phone/adjustPPE, camera-disjoint и eventFP denominator не получен. Методический выбор [F123](RAW_FACTS.md#f123); [Q004](OPEN_QUESTIONS.md#q004)/Q009, [E011](OPEN_QUESTIONS.md#e011). Нельзя ранжировать маршруты по AP несопоставимых cigarette images.

<a id="k003"></a>
### K003 — состояние/transition и actual artifact уточнены; industrial off-neck/hand/removal остаётся открытым

W2_A реально прочитала2VOC+2YOLO SH17 и off-body image ([F066](RAW_FACTS.md#f066)–[F068](RAW_FACTS.md#f068)), article/YAML mapping ([F007](RAW_FACTS.md#f007)), industrial3M head-state fulltext ([F069](RAW_FACTS.md#f069)/F070), R2PPE guide+actualJSON ([F072](RAW_FACTS.md#f072)/F073). Статья extended и base export разнесены; не заявляется, что tags нигде нет. Medical mask/R2PPE healthcare не cartridge workshop. Source files промышленной head-state не получены, neck/hand/transition GT отсутствует в полученном материале. [F101](RAW_FACTS.md#f101)/F102 дают два маршрута A visible uncovered state/B observed transition, stop при невидимом лице/нет before-state/IDswitch; item-doffing отдельно от coverage-loss. [Q001](OPEN_QUESTIONS.md#q001)/Q002/Q010/Q011, [E001](OPEN_QUESTIONS.md#e001)/E003/E016. K003 не закрыто обещанием готовой модели или LinQ.

<a id="k004"></a>
### K004 — первичные условия среды усилены; target degradation curves неизвестны

W2_B добавила independent Axxon VL4.5 manual conditions ([F076](RAW_FACTS.md#f076)/F077), Axis nearIR/blur/compression ([F078](RAW_FACTS.md#f078)), Bosch pre-encoder boundary ([F079](RAW_FACTS.md#f079)), Frigate upscale developer claim и resize code ([F080](RAW_FACTS.md#f080)/F081), industrial OIL survey/remediation/dispute/exclusions ([F084](RAW_FACTS.md#f084)). Symptom→compensation→abstain table [F122](RAW_FACTS.md#f122) задаёт проверку, не достигнутую компенсацию. RGB/NIR/thermal не смешиваются, source/native/tensor pixels разнесены. Прямых measured PPE dust/steam/topview curves и качества камер кейса нет. [Q004](OPEN_QUESTIONS.md#q004), [E003](OPEN_QUESTIONS.md#e003)/E013. Числа manuals — свойства версии, не наши admission guarantees.

<a id="k005"></a>
### K005 — industrial procurement chain найдена; приёмочная формула/результаты открыты

Oil India Limited GEM/2026/B/7902194 от11.08.2026: official NIT8p и prebid meeting25.08, published01.10.2026,97p/94numbered content получены ([S068](SOURCES.md#s068)/S069,[F082](RAW_FACTS.md#f082)–[F084](RAW_FACTS.md#f084)). Quoted SoW7.13 требует90% ideal/80% challenging, вопрос о95% не снимает неопределённость. Ответы оставляют per-use-case Design/approval и SAT/UAT criteria during implementation. Full SoW по hyperlink не получен; signed SAT/achieved performance/FAhours нет. Это частичное закрытие industrial customer→procurement→acceptance planning, не доказательство90/95% работы. [Q008](OPEN_QUESTIONS.md#q008)/Q016,[E010](OPEN_QUESTIONS.md#e010). itdf остаётся grant КД-ТЗ; DCASE — audio matching example, не CCTV standard.

<a id="k006"></a>
### K006 — pinned static chain закрыта в указанном scope; runtime effect открыт

W2_B прочитала all writes, caller/Norfair/stationary reuse/init/reset/end/newID и same-commit docs cfa08c56b23d23280c3d0a218e5a43182c97445b. [F085](RAW_FACTS.md#f085)–[F088](RAW_FACTS.md#f088)/S070 содержат точные ledgers/строки. Out сохраняет presence P, не reset; ordinary zone читает last measured box, **не estimate**. Timestamp equality может возникнуть от stationary reuse без нового detector invocation. In,out,in при inertia3 само ещё не entry; следующий in даёт entry в описанных условиях. Новая incarnation имеет чистые counters; removed/end не observed_exit. Это статическое DOC/CODE расхождение с ручными трассами, **не воспроизведённый runtimebug**. [Q007](OPEN_QUESTIONS.md#q007)/Q015,[E017](OPEN_QUESTIONS.md#e017)/E009. Actual Norfair lifetime/cadence/queue impact не измерены.

<a id="k007"></a>
### K007 — чрезмерное обобщение исправлено; case-specific endpoint/physical GT открыты

W2_C fulltext HDS ([F094](RAW_FACTS.md#f094)/S076) различает exact Wrong place/Safe/Wrong tie/Too thin/Not closed, а не только presence.9738 после augmentation8:1:1 не доказывает source-disjoint split; physical gate-lock/anchor protocol не дан. Поэтому не утверждаем, что attachment vision вообще не решают, но не раскрываем Safe в механическую сертификацию. Temporal fall Iazzi/Núñez-Marcos ([F095](RAW_FACTS.md#f095)/F096) имеют разные endpoints/exclusions/units. W1 требование устойчивого последующего lying **superseded**: fast recovery не отменяет observed transition, lying/immobility отдельно ([F124](RAW_FACTS.md#f124)). [Q018](OPEN_QUESTIONS.md#q018),[E012](OPEN_QUESTIONS.md#e012); необязательная ветка не расширяет автоматически анонс.

<a id="k008"></a>
### K008 — direct cascade traces найдены; net benefit нашего verifier открыт

W2_C получила NVIDIA VSS3.3.0 candidate→clip workflow/parser/timeout failure trace ([F099](RAW_FACTS.md#f099)/S081), Guo industrial recheck abstract ([F098](RAW_FACTS.md#f098)/S080) и Kim fulltext ([F097](RAW_FACTS.md#f097)/S079). Поэтому direct traces существуют; утверждение «paired evidence нет вообще» слишком широко. Guo numbers abstract-only без TP-loss/split audit; Kim each-frame Florence2/adaptive YOLO threshold .5→.3 повышает recall ценой precision, не reject-only rescue table. [F125](RAW_FACTS.md#f125)/Q019/E014 задают paired baseline TP/FP→accepted/rejected/unverified, upstream recall и latency; [Q005](OPEN_QUESTIONS.md#q005)/Q006 сохраняют LinQ boundary. Detector+rules остаётся baseline, verifier optional по измерению. Ни FA↓, ни пригодность LinQ не установлены.

### Результат сборки для дальнейших ролей

Нормализованы81S и125F,20Q и17E; повторные чтения одной цепочки не стали независимыми экспериментами. Полные процедуры находятся в OPEN_QUESTIONS.md; source/fact registry — SOURCES.md/RAW_FACTS.md. Полные old→new mapping и author handoff — _WORK/ID_MAP.md и _WORK/COLLECTOR_HANDOFF.md. Приоритет доказательств и W2 supersession явно заданы. Ни один E не выполнен; новое неизвестное после двух волн передано Q, скрытой третьей волны нет.
