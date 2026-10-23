# W1_C — действия, камеры, open vocabulary и ограничения LinQ

Первая волна, C11–C15. Исследовательский доступ 2026-10-23 примерно 06:00–06:06 Europe/Moscow. Входы Context-prompt.md, prompt-violation-methods-v2.md и PLAN.md прочитаны UTF-8; полный кейс/SDK/камеры отсутствуют. Поиск web, открытие primary docs, локальное чтение/визуальная проверка Bosch PDF; обучения, benchmark и приложения нет. [Реестр, выписки и журнал доступа](SOURCES_C/EVIDENCE.md). Префиксы C-S/C-F/C-E/C-Q уникальны в ветке; сборщик может перенумеровать с mapping.

## Выбор для команды

Для45 часов разумен условный маршрут: обычный детектор+событийная логика для наблюдаемых объектов; smoking — только при достаточном крупном лице/руке и с hard negatives; lying — отдельное состояние, а fall — временное событие; clipped hook — отдельная задача, не следствие надетой привязи. Фиксированный словарь YOLO-World/YOLOE потенциально снимает постоянный text encoder, но не снимает export/compile/accuracy gates. Сигнал неизвестного нужен при невидимом лице, мелкой сигарете/замке и неизвестном материале бочки. Эти решения являются нашими условными выводами из C-F01–C-F19, не установленным ТЗ.

## C11. Курение: что именно утверждать

**C-F21 [inference/proposal, C-F05–07]:** разделить три наблюдения: `cigarette_visible`, `hand_to_mouth_pattern`, `smoking_action`. Сигарета в руке ещё не доказывает текущий puff; единичное касание рта не доказывает smoking. Дым не является обязательным условием: он может не быть виден; в цехе пар/пыль/сварка могут быть очень похожи. Поэтому smoke detector допустим как дополнительная улика, не как единственный критерий.

Практический каскад: person/face/hand candidate → enlarged original-image ROI → cigarette/object cue и/или sequence classifier → evidence aggregation по тому же человеку. Если нет читаемого crop, результат unknown. Pose wrist-to-head distance — дешёвый на CPU **после** получения keypoints candidate generator; без дополнительного свидетельства он выдаёт только «рука у лица». Для удалённого широкого обзора action-only alternative может покрыть кандидатов, но требует отдельного доменного теста и не должен называться доказанным smoking.

**C-F22 [proposal]:** правило `smoking_near_flammables = smoking_action(person,t) AND person_in_configured_flammable_zone(person,t)`. Нельзя заменять вторую часть VLM-фразой «похоже на горючие материалы». Содержимое закрытой бочки/ёмкости и статус технологического процесса не наблюдаемы из RGB; предпочтительна предоставленная постановщиком ROI/карта оборудования/операционный признак. Если нужна именно дистанция до мобильного материала, необходима идентификация материала и геометрия/калибровка; область близости в пикселях остаётся image-space approximation. Передача W1_B.

Состояния для событий: compliant — человек наблюдаем, и ни action, ни нарушение зоны не подтверждены в текущем покрываемом интервале; violation — обе необходимые части подтверждены с временным перекрытием; unknown — недостаточная видимость/action evidence/неизвестная горючая зона. «Не подтверждено курение» не равно гарантии, что человек не курил.

Hard negatives для собственной проверки: питьё из бутылки/кружки/через трубочку; еда руками/ложкой/леденец; телефон/рация; поправление респиратора; протирание лица/кашель; ручка/инструмент во рту; сигарета в кармане/на столе/в руке; vape при иной форме устройства; дым от соседа; пар/пыль, отражения и сварка. Последний набор — наша предлагаемая промышленная проверка, не перечень опубликованной валидации C-S05.

**Условный выбор C11:** close view и понятный smoke-free zone — ROI/object+temporal confirmation; small cigarette but readable arms — action candidate with explicit uncertainty, возможно verifier только после paired test; мелкий человек/спина/закрытое лицо — unknown/не включать сценарий как решённый. Полноценная3D video модель добавляет непрерывный clip buffer, temporal sampling и тяжёлые operations; не первый гарантированный LinQ путь.

## C12. Падение, лежащий человек, высота и страховка

**C-F23 [inference, C-F03–04]:** lying-state detector наблюдает состояние в кадре. Fall-event detector должен наблюдать переход: до падения, изменение позы/положения, устойчивое последующее состояние. Кадр lying не раскрывает причину. В промышленности работа лёжа под машиной, монтаж/сварка внизу, намеренное приседание/укладывание и обслуживание оборудования являются обязательными отрицательными сценариями. Один dwell threshold не решает различение: работник может долго работать лёжа; упавший может сразу подняться.

Предлагаемая семантика: `person_lying` — обзорное уведомление/состояние; `suspected_fall` — временной переход с клипом; `medical_emergency` — не выводить по одной RGB-позе. ROI для плановой работы лёжа и расписание работ могут менять severity, но не должны уничтожать evidence. Начало клипа/потеря трека/окклюзия до lying дают unknown о самом падении. Камерное движение требует отдельной обработки, иначе pixel-speed/pose transition ложны.

**C-F24 [inference, C-F08]:** разложить высотное нарушение на `in_height_work_context`, `harness_worn`, `lanyard_visible`, `hook_visible`, `hook_attached_to_valid_anchor`, `gate_locked`. Детектор привязи покрывает только один предикат. Простое пересечение hook/anchor boxes не доказывает сцепление; невидимый карабин не доказывает отсутствие. Валидность anchor/расчётная прочность/внутреннее запирание не следуют из RGB. Даже при близком виде требуется разметка connection state и настоящий hard negative «рядом/приложен, но не защёлкнут». Проверка work-at-height в метрах требует известной геометрии сцены или внешнего контекста; простое положение выше картинки непригодно.

C-S08 особенно ценно как опубликованный отрицательный результат: успешная методологическая аннотация не равна реализованному распознаванию замка. Для45 часов можно честно показать harness presence в заданной высотной зоне; обещание «пристёгнут карабин» допускается только после отдельной наблюдаемости и теста. Не все варианты vision hook detector отвергнуты: C-S20 остаётся конкретной зацепкой для full text/class audit второй волны.

## C13. Камера: численные требования и цена кропов

Подтверждённые числа и их границы сохранены в C-F01–04. Сравнивать нужно **разные единицы**: Bosch — рост человека в аналитическом кадре; Macroscop small PPE — голова/кисть в видеокадре; DORI — px/m для человека-оператора, не PPE. Числа одного продукта нельзя выдавать минимальными для модели команды. Не путать illustrative modules A/B в вводном примере Macroscop с требованиями PPE: реальные углы находятся в «Сцена и расположение камеры».

**C-F25 [inference]:** requirement camera acceptance должен содержать source stream resolution, analysis tensor size, crop policy, target width/height на обоих этапах, ракурс, видимость части тела и режим день/ночь. При letterbox resize приблизительно `target_px_tensor = target_px_source * min(Wtensor/Wsource, Htensor/Hsource)` до padding. Это геометрическая формула, не гарантия качества. Увеличение4K source бесполезно, если вся картинка всё равно сжата до того же tensor и ROI не используется; увеличение focal length/ROI может повысить реальную детализацию, digital upscaling не создаёт её.

Ночь/ИК: цветные классы одежды теряют исходную информацию; перенос RGB режима на IR требует отдельного теста. Пыль/пар/дым могут закрывать форму; motion blur/long exposure уничтожает границы малых объектов; compression может убрать тонкую сигарету/ремень; сильный topview закрывает лицо и меняет силуэт; fisheye/вибрация/пересвет меняют геометрию и видимость. Это качественные физические причины и ограничения manuals, не измеренные нами проценты деградации. Если качество невозможно восстановить камерой/светом/потоком, событие должно перейти в unknown, а не автоматически в violation.

**C-F26 [proposal/inference, C-F13]:** сравнить1 full-frame call, full frame+person crops и slicing. Полный SAHI на каждом кадре дорог: при кадре W×H, tilesw×h, шаге sw/sh приблизительно `K=(ceil(max(0,W-w)/sw)+1)*(ceil(max(0,H-h)/sh)+1)` forwards плюс опциональный full-frame. Border handling конкретной реализации уточнить; это расчёт нагрузки, не benchmark. Для промышленного narrow ROI часто выгоднее crop только видимого face/head/hand лучших кадров и только кандидатов. Трек с low confidence нельзя загонять в endless crops без лимита бюджета.

**Решение C13:** admission gate на видимость и размер **нужной части тела**, плюс лучший кадр в bounded time window; модельный threshold подобрать C-E03. DORI служит планированию обзора, не оправданию детекции сигареты. Приёмочного industrial протокола с номером закупки, заданными FA/hour и camera conditions в этой ветке не найдено; это точный пробел, а не свидетельство отсутствия таких внедрений.

## C14. Open vocabulary и VLM verifier

**C-F27 [inference, C-F09–11]:** различать offline vocabulary preparation и dynamic prompting. Для известного короткого списка классов условно предпочесть reparameterized text mode YOLO-World/YOLOE: один подготовленный image graph и фиксированный class mapping. Это снижает структуру online workload, но требует проверить сохранённые class order, similarity semantics, head dimensions, operator graph и повторную компиляцию при обновлении vocabulary. Динамическое свободное описание может требовать text encoder и cross-attention; не обещать такой режим из факта экспорта fixed prompts.

Open-vocabulary вывод «helmet» не отвечает «чья каска/на голове/правильный тип/исправна». Описание «worker without respirator» может работать как person appearance category, но это нужно проверять на голова невидима/респиратор на шее/маленькое лицо; отсутствие позитивного bbox не даёт отрицательного факта. Полезная быстрая роль OVD — поиск candidates, подсказки разметчику, проверка, видит ли модель нужную сущность в новых камерах. Это proposed workflow, не доказанная промышленная точность.

**C-F28 [proposal, C-F12]:** verifier receives original crop **и** умеренный контекст/короткий клип, формулирует узкие наблюдаемые predicates с enum `supported / contradicted / not_visible`; сохраняются raw answer/model/prompt/version/crop/time. Не спрашивать «есть ли нарушение?» без определения. Сравнить detector alone vs cascade на одних и тех же кандидатах. Нужны paired TP→FN (verifier пропустил реальное), FP→TN (отсёк ложное), FP→FP, TP→TP, а также латентность/стоимость/unknown-rate. Выигрыш precision при потере recall не объявлять улучшением без цели; если VLM вызывается только на candidates, нельзя приписать ему recall по пропущенным первым этапом событиям.

Verifiers могут задерживать событие, терять мелкий объект при downscale, опираться на priors, менять ответы при prompts. Multi-frame VLM не гарантирует временное понимание. Горючесть материала/застёгнутость невидимого замка остаются unknown. Установленного primary industrial paired-study, обещающего снижение FA именно на наших четырёх сценариях, не получено. Поэтому VLM — условный дополнительный этап после C-E04 и правил LinQ, не обязательная основа демо.

## C15. Нейровызовы и требования к LinQ

**C-F29 [inference matrix; не таблица supported ops].** Пусть f — анализируемые кадры/с, P — число людей, h — число выбранных heads/hands, r — crop refresh/c, K — число tiles, c — candidates/c, v — verifier images or clips/c. Batch может объединить submissions, но не убрать вычисление P crops. Самостоятельно низкий f не гарантирует экономию, если поток людей увеличивает P.

| Метод | Нейровызовы/данные | Какие выходы/операции предъявить платформе | CPU после инференса | Неизвестное / риск |
|---|---|---|---|---|
| Single multi-class detector | f image forwards/s | conv/resize/concat, bbox+class heads; возможно DFL decode | NMS/decode, ownership, rules | конкретный export и граница graph/postprocess |
| Person→attribute crop | f detector + P*r classifier crops/s | fixed-size classifier; multiple independent crops | crop selection/association/vote | очередь и stale attribute, число людей |
| Person→head→smallPPE | f + P*r_head + h*r_ppe |2–3 разных сети/heads | связывание координат/кадров | пропуск ранней стадии обрывает cascade |
| Bottom-up pose | f pose forwards | keypoint coords/confidences или heatmaps | skeleton geometry, rules | layout/stride/argmax; INT8 positional effect неизвестен |
| Top-down pose | f detector + P*r_pose | pose network per person crop | track/keypoint matching | стоимость растёт с P; occluded joints unknown |
| SAHI/full frame+crops | K*f (+f optional) | тот же detector многократно | merge/NMS/reprojection | K overhead, context fragmentation |
| Clip3D/temporal action | per-person sliding clips at stride, не просто один кадр |3D convolution/pool либо attention/RNN, temporal input shape | buffer/timestamps/event state | поддержка конкретных3D/temporal ops и valid sample timestamps |
| Reparameterized OVD | f image forwards; text preparation offline | выбранный fixed head/neck; класс→индекс | class mapping/ownership/events | экспортированный граф нужно проверить, даже если название YOLO |
| GroundingDINO/dynamicOVD | image+text-dependent computation | tokenizer/text encoder, matmul/attention/LN/Softmax, multi-input | prompt prep, rules | конкретные opset/shapes/support неизвестны |
| VLM verifier | c calls/s, v frames/call | image encoder/projector+token generation/KV-cache, часто dynamic length | gating/audit/format validation | обязательность всех нейроэтапов на LinQ не уточнена; на CPU/GPU обход обещать нельзя |

Операции перечислены как архитектурные требования семейства, не как извлечённая inventory конкретного ONNX. Если custom graph уносит decode/NMS на CPU, это не меняет location нейроинференса, но согласовать допустимую границу с постановщиком. Геометрия ROI, homography, трек без ReID, state machines/confirmation/cooldown не требуют neural inference; ReID embeddings требуют дополнительную сеть. Это требует передачи W1_B/video_architecture.

**C-F30 [inference, C-F15–18]:** четыре отдельных gate: export works → graph compiles → executes on assigned LinQ → accuracy/event quality preserved. Публичные заявления LinQ об INT8/ONNX/YOLO не закрывают ни один gate для выбранного собственного артефакта полностью. Их можно использовать для составления short list и вопросов. Нельзя переносить HPS 960TOPS/ResNet latency на неизвестный hackathon hardware или сетевой RPC.

**C-F31 [inference]:** проверка INT8 должна включать размерные/сценовые slices: мелкий cigarette/head, respirator on neck, backlight/IR/blur, crowded association, keypoint displacement. Confidence shifts могут изменить NMS, track lifecycle и N/M-event logic без большой средней mAP разницы. C-F15 даёт механизм attention sensitivity и пример успешного 8 bit; C-F16 даёт конкретный случай spurious boxes. Прямого primary доказательства размера INT8-потери **наших** pose/smallPPE нет. Heatmap-coordinate quantization нельзя путать с arithmetic INT8. Точный calibration/QAT формат и возможность mixed precision/float heads — вопросы LinQ, не установленная опция.

## C-E: предложенные проверки следующей практической волны

Все ниже — процедуры, не выполненные эксперименты; без универсальных порогов.

| ID / меняемое решение | Входы | Шаги | Метрики / решение / предел вывода |
|---|---|---|---|
| **C-E01 Smoking observability/cascade** | исходные клипы каждой камеры, видимые smoking sessions и перечисленные hard negatives, person/action annotations; материал зоны подтверждён постановщиком |1) разметить видимость сигареты/лица/руки и action intervals;2) оставить отдельную камеру/смену;3) сравнить object-only, gesture-only candidate и object+clip/time;4) применить один и тот же AND zone rule | event precision/recall, FA/camera-hour, latency, unknown coverage; выбрать каскад по event budget. Успех в разыгранном RGB не доказывает реальную пожарную опасность/ИК перенос |
| **C-E02 Fall vs lying + hook adversarial** | безопасно разыгранные slow lie, kneel, under-machine work, fall-like transition; hook rig close/attached/unlatched/occluded, известная anchor map | отдельно GT transition/state; оценить до/после окна, затем hook visibility and connection states; не выполнять опасные реальные падения | confusion intentional lying/fall, delay, missed fast recovery; hook-state precision / unknown by size. Если annotators не видят gate, label unknown. Успех не подтверждает anchor strength / полное PPE compliance |
| **C-E03 Camera/crop budget** | native recorded streams включая день/ночь/IR, blur/compression examples; сохранённые source and tensor sizes, camera pose | измерить target px до/после resize; сравнить full frame, bounded person/head crop, tiles; условия варьировать по одному и маркировать реальные vs synthetic degradation | recall/precision/unknown по размерам и condition; latency P50/P95, forwards/sec, duplicates; выбрать minimum validated size/angle **для конкретной модели/камеры**. Downsample sweep не доказывает дальность по линзе или реальную пыль |
| **C-E04 VLM paired verification** | неизменный candidate set+GT, заранее зафиксированные prompts/models; отдельный calibration and test | preserve raw crop, context clip; ответ enum; paired table transitions; измерить обе версии pipeline | rescued FP / lost TP, event metrics, abstention coverage, latency/cost. При отсутствии net benefit/при ресурсном конфликте убрать verifier. Не устанавливает full-stream recall и не доказывает вывод о скрытом материале |
| **C-E05 LinQ compile + precision gate** | точный hardware/SDK/version/ONNX opset, representative calibration data, reference FP outputs, собственный promised method graph | зафиксировать artifact hash/class mapping/preprocessing; inspect ops, compile, run with execution evidence; сравнить raw outputs→detections→events на одинаковых frames; отдельно measure RPC/queue | compile pass, fallback ops, execution proof, raw tensor drift, AP small/keypoint displacement/FA/hour, P95 latency; выбираем plain detector/cascade/OVD по успешным gates. Успех одного checkpoint не доказывает поддержку семейства / online SLA |

## C-Q: точные неизвестные

- **C-Q01 [P0 постановщик/полный кейс]:** какие именно нейросетевые этапы обязаны исполняться на LinQ? Допустим ли внешний verifier, или вся neural chain? Меняет допустимость C14/C15. Из анонса известна только общая обязательность inference.
- **C-Q02 [P0 артефакт/SDK]:** назначенная модель устройства, SDK/compiler revision, static/dynamic shapes, поддержка attention/3D conv/keypoint heads/QDQ, возможность float outputs / CPU fallback. Не спрашиваем абстрактно «поддерживает YOLO», предъявляем export graph C-E05.
- **C-Q03 [P0 данные/практика]:** source camera / body-part px, ракурсы, day/IR, smoking evidence visibility; C-E01/C-E03 решат, включать ли smoking/респиратор/hook.
- **C-Q04 [P0 постановщик]:** smoking рядом с чем: размеченная пожароопасная зона или автоматическое определение материалов? По RGB нельзя доказать содержимое ёмкости. Нужен supplied context.
- **C-Q05 [P1 практика]:** сколько candidate FA от еды/рации/поправления СИЗ и от намеренной работы лёжа; какие latency/FA/hour приемлемы? Нужны negatives/цель оценки.
- **C-Q06 [P1 сеть/следующая волна]:** HDS-YOLOv5 full text/classes действительно различает clipped/unclipped или только hook presence? Metadata abstract получены; полная semantics не установлена. Не закрывает connection gate.
- **C-Q07 [P1 практика]:** INT8 ухудшает ли именно малые PPE/keypoints на assigned LinQ при реальной calibration? Общие mechanisms установлены, эффект нанашем graph нет.
- **C-Q08 [P2 закупки]:** приёмочный industrial video analytic протокол с номером контракта, camera requirements и FA/hour. В открытом поиске этой ветки не получен; не придумывать 95% accuracy без denominator.

## Адресная передача

- **W1_A / datasets / evaluation:** C-S02 общий первоисточник Macroscop, не независимое подтверждение двух агентов. Для smoking нужны hard negative action labels; для fall разные state/transition GT; для hook presence/attachment/gate unknown. C-E01/02/03.
- **W1_B / video_architecture:** smoking AND flammable zone C-F22; camera/visibility changes invalidate inference; workload C-F29 зависит от P/K/clip stride; attributes may have timestamp age, не выдавать старое состояние за текущий кадр.
- **linq_platform / model_stack:** fixed text reparameterization C-F09/10 и pinned YOLO-World doc; dynamic GDINO C-F11 другая нагрузка. Передать ops inventory / precision gate C-E05. Публичный список LinQ C-F17 не checkpoint guarantee.
- **training_strategy:** small PPE calibration / night domain, hard negatives smoke/hand-to-mouth; medical mask ≠ respirator. Generic zero-shot AP не снимает local data requirement.
- **operator_product / hackathon_strategy:** карточка evidence должна различать visible lying / suspected fall / verified smoking и unknown material/connection; не обещать clipped hook по harness bbox. В 45 часов действовать по условным gates, не по длине feature list.

Короткая передача корню: наиболее сильны Bosch p5 с численными requirements; Lim2022 p10 с признанным нераспознанным hook/непроверенным connection; Macroscop lying semantics; fixed prompt graph vs dynamic prompt distinction; INT8 не гарантирует preserved false alarms. Файл готов для критика; открытые вопросы C-Q01–08, процедуры C-E01–05.
