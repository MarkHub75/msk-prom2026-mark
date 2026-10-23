# W2_B — закрытие K004/K005/K006

Вторая сетевая волна, gpt-6.1-sol/medium. Фактический доступ23.10.2026,06:15–06:26 Europe/Moscow(+03:00). Полного кейса/SDK/LinQ hardware/исходных камер нет; RTX4070 допустима для будущей отладки, neural inference решения обязателен на LinQ. Модели, VMS и benchmark не запускались. [Первичные выписки и provenance](SOURCES_W2B/EVIDENCE.md), [журнал](SOURCES_W2B/SEARCH_LOG.md). Числа из manuals ниже — свойства конкретных продуктов. Ни один E не выполнен.

Главное изменение: вместо общего списка «ночь/пыль/blur» получены независимые PPE admission conditions и конкретный промышленный pre-bid dispute о невозможном требовании за пределами IR-range. В Frigate теперь прочитана вся нужная цепочка upstream→zone update→end/new track и same-commit docs. Это позволяет сузить кодовый вывод без выдачи его за runtimebug.

## K004 — область применимости уточнена; target-camera качество открыто

Исходный дефицит: W1 дал Bosch/Macroscop pixel/lux limits, но night/IR, resize, compression, blur объяснялись преимущественно физически. Нужен первичный trace условий/ошибок и предел предлагаемой компенсации.

Новые основания W2-B-S01–05/S09–10:

- **W2-B-F01/F02:** Axxon Next4.5 VL требует цветной поток, освещение без резких перемен и качество без compression/noise artifacts; visibility≥8 кадров, минимальная высота самого helmet20px/vest50px. Это другой denominator размера, чем высота человека Bosch. Source unit «200 lux per square meter» сохраняем как дефект формулировки источника, без создания нового норматива.
- **W2-B-F03/F04:** официальные camera/settings manuals раскрывают механизм dark→long exposure→blur, denoise→ghosting. Axis XFQ1656 nightmode — nearIR+visible в monochrome. Bright night picture само по себе не подтверждает цветовой PPE-признак. Bosch onboard analytics получает pre-encoder image; её encoder-independence нельзя переносить на удалённый RTSP pipeline.
- **W2-B-F05/F06:** Frigate crop/preprocessing дают реальный resize trace; сообщение разработчика о росте FP при upscaling малых regions — контрпример без численной оценки. Native crop сохраняет доступные source details, а не восстанавливает отсутствующие. SAHI VisDrone gain остаётся W1 внешним benchmark, не доказательством PPE crop gain.
- **W2-B-F09:** OIL pre-bid p79–83 связывает среду с assessment, amendments и camera-wise exclusions. Вопрос bidder о pitch-dark IR-range — не измерение; ответ internal review — не согласие на гарантию80%.

Практическая таблица ниже — **наш условный план**, не готовые алгоритмы vendors. Триада K001 из W2_A применяется к каждому предикату: отсутствие cue не false, off-body запасной предмет не означает uncovered bodypart. При невозможности наблюдать нужную часть тела результат U.

| Симптом | Что ещё наблюдаемо / чего нет | Допустимая компенсация | Когда abstain | Целевой E slice |
|---|---|---|---|---|
| RGB→monochrome nearIR ночью | silhouette/head geometry могут остаться; цвет каски/жилета больше не измеряется как RGB | Свет для color-mode либо отдельный validated night/IR model+data; писать mode в evidence | Поддержка основана только на дневном цвете, а целевая деталь ночью не читается | C-E03: native day/color vs actual nightIR, в одной камере/ROI; class, bodypart visibility, unknown coverage |
| Деталь есть на source, исчезла после model resize | Есть native source pixels; в tensor объект меньше | Crop **из исходного** decoded frame, разрешённый input либо bounded tiles; сохранить контекст/owner | После crop неразличимо, либо caller не может обеспечить original ROI | C-E03: размеры target до/после preprocess, fullframe vs crop, paired errors и forwards/P95 |
| Compression ringing/blocking на head/hand | Факт присутствия человека может сохраниться, мелкий PPE/cigarette — нет | Менее агрессивный stream, bitrate/quality настройка; выбрать source stream до loss | В компрессированном source нет различимого target; upscale не добавляет GT | C-E03: реальные source codec/bitrate/QP если доступны; synthetic codec sweep отдельно |
| Long exposure или denoise blur/ghosting | Статичный предмет может читаться, движущаяся кисть/голова уже нет | Короткая выдержка с достаточным светом, умеренный denoise; оценить gain/noise tradeoff | Видимая деталь смазана; нельзя переносить прежний clear state бесконечно | C-E03: motion speed/direction, actual exposure/gain, moving vs stationary PPE |
| Steam/dust/exhaust | Может наблюдаться obstruction/contrast loss или visual smoke-like cue; материал/причина не всегда известны | OIL camera-wise exclusions для **стационарного process background**, свет/очистка/другой viewpoint; отдельные negatives | PPE за завесой не виден; исключение дыма не даёт compliant PPE | C-E03/C-E01: real dust/steam clips, visibilityGT; smoke/fire negatives отдельно от smoking-action |
| Topview/occlusion | Верх каски возможен, лицо/coverage респиратора может быть невидимо; floor anchor может быть assumed | Поменять angle/checkpoint camera; принять лишь наблюдаемый helmet predicate | Не видно face target/owner либо ground contact для zone semantics | E-A03/C-E03 и E-B01: angle/part visibility, ownership, floor-anchor validity |

По dust/steam/topview прямого **измеренного PPE error curve** не получено. Axis generic topview warning не даёт проценты по PPE; OIL masking rule относится к site-specific fire/smoke backgrounds. Нельзя доказать80% PPE в пыли либо спасение респиратора denoise-настройкой.

**Решение команды [inference]:** до admission C-E03 не обещать night/IR четыре сценария целиком. Wide view может быть пригоден для person-in-zone, а респиратор/курение потребовать checkpoint. Это выбор разных наблюдаемых предикатов, не недоработанный detector. Если organisers дают только IR, заменить тренировочный режим/объём задачи можно лишь после проверки конкретного night input; grayscale conversion дневного датасета не равна реальному nearIR.

**W2-B-E01 (расширение C-E03, не выполнено):** получить native streams, mode/exposure/codec, camera/ROI/scene version и model preprocessing. Отобрать paired clear/degraded события с target size и visibilityGT; real conditions маркировать отдельно от synthetic sweeps. Сравнить fullframe/crop лишь при одинаковом candidate/GT и ограниченном budget. Метрики: event recall/precision/FA per negative camera-hour, unknown coverage по каждому predicate, latency, number of forwards. Решение: admitted camera-region/режим, checkpoint либо исключить данный predicate. Успех synthetic resize не доказывает real dust, night or дальность.

## K005 — промышленная цепочка найдена; формула приёмки осталась открытой

Исходный дефицит: грантовое itdf КД-ТЗ и DCASE не связывали промышленного клиента с оригинальным procurement/acceptance. Нужны реквизиты, clauses, scenes, denominator и разделение demanded/achieved.

**W2-B-F07/F08/F09:** найдена не обзорная статья, а официальная закупка Oil India Limited **GEM/2026/B/7902194 от11.08.2026**, PPE/Unsafe Act Video Analytics, с оригинальным NIT и опубликованными **01.10.2026** minutes pre-bid от25.08.2026. Цепочка: [карточка заказчика](https://www.oil-india.com/tender-details/124?in_detail=NzBleHVBPT0%3D) → NIT8p → hyperlink к Scope of Work1786430899.pdf на GeM → официальные94 содержательные страницы prebid с quoted SoW clauses и ответами OIL. Полный SoW не скачался, поэтому его полный текст не заявляется прочитанным. PDF/prebid таблицы визуально проверены, ссылки и pages в S06/S07.

| Что требовалось выяснить | Что подтверждено первичным материалом | Что **не** подтверждено |
|---|---|---|
| Industrial scope | PPE, prohibited zones, unsafe acts, fire/smoke; существующие operational CCTV, разные камеры; prebid p6–7 обсуждает716 камер/98 locations-rigs | Реальный объём принятой системы, award и работа в эксплуатации |
| Accuracy threshold | SoW7.13 quoted p12/p24:90% ideal/80% challenging; p19 содержит вопрос о конфликтующем95%; ответ — отдельная оценка по use case, методика Design/OIL approval | Формула accuracy, выборка, CI calculation, FP/FN denominator, achieved90/95 |
| Event/negative time | Bidders прямо запросили GT/sample count/FP/FN; опубликованный ответ их численно не определяет | FA/hour, допустимые duplicates, onset/offset collar и negative observation duration |
| Acceptance chain | p36 row55 quoted SoW10.2: SAT с client team, detection scenarios/alerts, formal GoLive signoff; ответ — criteria до UAT/SAT during implementation | Готовая ПМИ, signed SAT results, опубликованный акт приёмки |
| Camera conditions | p79–80 joint survey/remediation; p82 stable PTZ presets; p83 process backgrounds camera-wise | Соответствие всех legacy streams мелким СИЗ, новая универсальная дальность/освещённость |

Это содержательное изменение K005: **промышленное требование теперь доказано, незавершённость его операционализации тоже доказана**. Пример полезен ровно потому, что procurement может требовать процент без готовой denominator, а поставщики это оспаривают. Не превращать его в стандарт CCTV и не заявлять измеренную успешность. Текущая карточка переносит deadline на12.11.2026; сентябрьская дата раннего NIT не означает completed procurement.

**W2-B-Q01 [постановщик/evaluation]:** запросить собственную ПМИ или согласовать: unit(event/person-frame), GT объём по классам/камерам/dayIR, minimum episode, max delay и source-time origin; negative camera-hours, FP/duplicate definition; unknown coverage/исключённые камеры; boundary/occlusion rules. Если публикация даст только95% accuracy, сначала определить знаменатель и что делать с unobservable cases. Чужой90/80% не выбирает наши thresholds.

**Статус K005:** уточнена область / частично закрыто. Industrial customer→procurement→acceptance-planning теперь есть. Программа/протокол фактической приёмки и формула остаются unknown. Дополнительный бесконечный поиск агрегаторов не заменяет ответ клиента.

## K006 — pinned статическая цепочка замкнута; runtime не проверялся

Исходный дефицит: W1 читал update без полного caller, а docs были latest. Ниже только commit **cfa08c56b23d23280c3d0a218e5a43182c97445b**, same-commit docs и source. Локаторы — строки сохранённых оригинальных Python files, не сокращённого web rendering.

### W2-B-F10 — все записи zone counters и gates

`TrackedObject.__init__`: tracked_object.py65–68 создаёт новые `zone_presence={}`, `zone_loitering={}`, `current_zones=[]`, `entered_zones=[]`. Полный `rg` каталога frigate по двум именам нашёл только инициализацию, lookup и эти присваивания; отдельного caller reset нет:

| Поле / ветка `TrackedObject.update` | Изменение |
|---|---|
| line202 | локальный `zone_score=P+1`, P=stored presence или0 |
| in, разрешённый label/enabled, filters проходят; score<I:295 | сохранить P+1 |
| out,0<score<I:298–299 | сохранить score−1, то есть **прежний P**, не decrement прежнего и не reset |
| in, score≥I:265–289 | при отсутствии speed gate переход к `loitering_score=L+1`; если L+1<threshold, сохранить L+1; иначе добавить current zone, не записывать новый L |
| out после I | P/L не меняются; current local list не пополняется |
| завершение update385–386 | self.obj_data.update(obj_data); current_zones заменить локальным списком; entered_zones сохраняет когда-либо вошедшие |

Disabled zone/label mismatch пропускает обработку, а сохранённые counters не сбрасывает. Filters/speed могут помешать входу; это не трасса ниже. Speed calculation отдельно требует свежего obj_data.frame_time, ordinary point-in-zone — нет. `has_valid_frame` относится к thumbnail gate154+, а не ко всему zone loop. Сам false_positive также не является общим skip зон; значимость/publish затем имеют свои gates.

Same-commit zones.md225/232 и config/camera/zone.py46 описывают consecutive frames. Таким образом **статическое DOC/CODE расхождение для указанных условий подтверждено точнее W1**; не нужно ссылаться на unpinned online docs.

### W2-B-F11 — caller, cadence, stale data

1. video_detect.py106 выбирает **NorfairTracker**. process_frames300/429/434 вызывает match_and_update либо update_frame_times, build438+ кладёт tracked objects в detections, queue534–550 передаёт пакет. При frame=None287–292 нет пакета; при полной очереди534–537 пакет отбрасывается. Поэтому configuredfps не равно гарантированным update calls.
2. `NorfairTracker.match_and_update`509–648: при t.last_detection.frame_time≠current time622–628 увеличивает disappeared и обновляет **estimate**, но `box`, `centroid`, `frame_time` остаются от последней detection. Сохраняемый объект всё ещё может попасть в downstream пакет, пока tracker его возвращает.
3. `update_frame_times`493–507 создаёт detection из сохранённых bbox для объектов с disappeared==0 и текущий frame_time назначается в match_and_update556. Stationary objects также seedятся в video_detect396–405. Поэтому даже равенство timestamps здесь не доказывает новый neural measurement: есть deliberate stationary reuse.
4. object_processing.py773–799 читает пакет и вызывает CameraState.update. CameraState419–425 вызывает TrackedObject.update для пересечения current_ids и previous_ids, **без fresh-frame gate**. Constructor новых IDs373–379 не вызывает update в ту же итерацию.
5. Ordinary zone anchor tracked_object.py188–189 использует `centroid.x` и `box.bottom` входного obj_data, **не estimate**. При prediction-only это последняя measured geometry; называть его predicted bottom-center неточно.

Следствие — цепочка может считать zone updates по сохранённой геометрии до исчезновения track, а stationary reuse может представляться fresh frame_time. Это результат кода при условиях path, не наблюдённое live поведение/частота. Точный Norfair hit/lifetime при реальных detections не восстанавливается ручной трассой.

### W2-B-F12 — ручные трассы (не исполненный тест)

Предпосылки: один включённый обычный zone Z, person, без distances/speed, filters пропускают, один тот же ID, update доходит до zone loop. P/L ниже **stored** counters, C=current_zones, E=entered_zones. `—`=нет записи, эквивалент lookup0. Последовательность начинается **после constructor**, иначе первый кадр лишь создаёт объект.

**Трасса A: in,out,in при inertia3, loitering0.**

| Шаг | Область | Ветка/строки | P после | L после | C/E |
|---|---|---|---|---|---|
| init | — | __init__65–68 | — | — | []/[] |
| u1 | in | score1<3;295 |1|—|[]/[]|
| u2 | out | score2<3;298–299 |1|—|[]/[]|
| u3 | in | score2<3;295 |2|—|[]/[]|
| u4 | in | score3≥3;276–285; threshold0 |2|—|[Z]/[Z]|

Одна тройка in,out,in **ещё не даёт entry** при I3; важно не преувеличить. Но следующий in даёт entry после всего двух подряд in в конце. Последовательность in,out,in,out,in тоже доходит до entry на третьем in. Каждому из этих выводов соответствуют lookup и отсутствие reset, а не запуск.

**Трасса B: частичный dwell, exit,reentry; inertia1, fps5, loitering1s→threshold5.**

| update | in/out | Ветка | P/L после | C/E |
|---|---|---|---|---|
| u1 | in | score1≥1; L1<5,289 |—/1|[]/[]|
| u2 | in | L2<5 |—/2|[]/[]|
| u3 | out | out, score1<inertia1 false |—/2|[]/[]|
| u4 | in reentry | L3<5 |—/3|[]/[]|
| u5 | in | L4<5 |—/4|[]/[]|
| u6 | in | L+1=5,281/284; L не записывается |—/4|[Z]/[Z]|
| u7 | out | C не пополняется,386 |—/4|[]/[Z]|
| u8 | in reentry | L+1 снова5 |—/4|[Z]/[Z]|

Dwell здесь накоплен пятью eligible updates с разрывом; повторный вход после уже достигнутого порога проходит сразу при тех же предпосылках. `entered_zones` не означает current occupancy. Для I3 после достигнутого inertia сохранён P2; он также не требует новой серии после выхода.

**Трасса C: prediction-only при последней measured рамке внутри, I3/L0.** После u1 имеем P1. В следующем upstream кадре detection нет, но Norfair ещё возвращает t:622–628 сохраняют старую `box/frame_time`, изменяют estimate. Downstream updated_ids вызывает update; score history получает0 (tracked_object138–140), zone использует старый inside anchor. u2→P2, u3→C[Z] при продолжающемся возврате track. Если Norfair уже исключил t, вместо u3 будет end path; статическая трасса этого lifetime не измеряет. Если последняя bbox снаружи, prediction-only estimate внутрь **сам по себе не даст entry**, потому что zone не читает estimate.

**Трасса D: stationary reuse без нового detector invocation.** video_detect434→update_frame_times493–507→match556 присваивает текущий frame_time повторённому bbox. Zone обработка идёт как fresh по timestamp, а actual neural observation отсутствует. Следовательно для своего event engine нужен признак provenance measurement/reused/predicted, не только frame_time equality.

### W2-B-F13 — конец, удаление, новый ID

Новый ID upstream возникает NorfairTracker.register273–292 (timestamp+random suffix), downstream constructor заводит чистые counters. В CameraState.update отсутствующий current ID становится removed:494–500 записывает end_time и вызывает callbacks[end], **не очищая zone fields в самом объекте**. Завершённый объект ещё хранится до event_end_subscriber→CameraState.finished307–308 (object_processing819–830), затем удаляется. Повторное отсутствие не даёт новый end callback из-за существующего end_time.

Resolution change — отдельный reset: CameraState310–347 очищает tracked state и при out-of-bounds stale batch может пропустить пакет; video_detect245–260 очищает tracker state. Camera disabled в object_processing789–791 пропускает update, это не наблюдённый выход из зоны. Если upstream действительно новый track с новым ID, counters empty; это не продолжение previous incident и не перенос person identity.

**Статус K006:** статический вопрос caller/init/reset/stale/end/newtrack закрыт в описанном scope; runtime event effect открыт. Допустимая формулировка финального отчёта: «В закреплённом коде при ordinary-zone update счётчики не обнуляются на выходе; caller допускает reuse последней геометрии. Same-commit docs говорят consecutive. Это нужно учитывать в собственной явной политике и проверить replay». Недопустимо: «найден и воспроизведён runtimebug Frigate» или перенос вывода на все версии/конфигурации.

**W2-B-E02 (уточняет E-B04, не выполнено):** при наличии окружения pinned Frigate зафиксировать config/zone/filters/fps и поток timestamped detections. Прогнать четыре приведённые последовательности, отдельно с real measurement, stationary reuse, disappeared/prediction, frame unavailable и queue drops. Сохранить incoming box/estimate/frame_time, actual detector flag, P/L/C/E, currenttime, id/end_time; сравнить с ручным state ledger. Потом на наших событиях оценить event onset/end, duplicates, FA/hour и reset policy. Даже подтверждение ledgers не доказывает пригодность Frigate для промышленной безопасности; цель — выбрать и проверить наш temporal operator.

## Передача корню и соседним темам

- **evaluation/operator_product:** S06–S07 — concrete industrial requirement+unresolved protocol;95/90/80 не достижения. Нужна camera-wise observability/unknown policy до процента accuracy. OIL clauses не являются стандартом.
- **video_architecture/training_strategy:** W2-B-F03–06 — source mode и preprocessing часть контракта; source resolution≠tensor size. Нужны quality/exposure/IR slices и bounded original crops; нет гарантии, что upscale снижает FP.
- **video_architecture/evaluation:** F10–F13 — all counter writes и lifecycle; ordinary zones могут считать stale geometry, stationary timestamps могут выглядеть fresh. Передавать observation provenance отдельно от tracker state.
- **W2_A:** принято уточнение item instance≠bodypart coverage; observed doffing≠uncovered state. Для smoking∧zone использовать Strong Kleene: F∧U=F,T∧U=U; конкретная unknown-camera не превращается в violation/compliant.
- **W2_C:** OIL p80 row14 — клиент отдельно получает вопрос harness presence vs anchored lanyard и отвечает finalize during survey; это не доказательство технической решённости hook. p83 row22 steam/exhaust/dust — practical hard negatives для fire/smoke, не smoking GT.

Остатки: W2-B-Q01 acceptance formula от постановщика; W2-B-Q02 target dayIR/crop/blur/visibility до C-E03; W2-B-Q03 replay E-B04 и реальная cadence/LinQ jitter. Общие финальные/CRITIC не редактировались.
