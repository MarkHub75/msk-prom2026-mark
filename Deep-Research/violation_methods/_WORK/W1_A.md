# W1_A — СИЗ: постановка, ownership, мелкие объекты и unknown

Первая волна, C01–C05. Исследователь назначен gpt-6.1-sol/medium; дочерних агентов не создавал. Доступ23.10.2026, Europe/Moscow(+03:00), начало около05:59. Прочитаны входные Context-prompt.md, prompt-violation-methods-v2.md, _WORK/PLAN.md и индивидуальное задание. Полного кейса, камер, данных, SDK/конфигурации LinQ нет. Никаких тренировок, инференса или локальных benchmark не выполнялось.

Основная рекомендация: определить задачу как **состояние конкретного СИЗ на видимой части тела конкретного человека**, плюс обязательное неизвестное состояние. Для каски начать с детектора головы/состояния или person+helmet с явной head association, затем выбирать усложнение по ошибкам. Для респиратора, очков и перчаток сразу предусмотреть отказ, высокий detail camera и контрольную точку. Не выдавать распознанный предмет, medical mask или generic cover за доказанную защиту.

Подробная первичная база и ограничения находятся в [SOURCES_A/EVIDENCE.md](SOURCES_A/EVIDENCE.md), полный журнал запросов/недоступного — [SOURCES_A/SEARCH_LOG.md](SOURCES_A/SEARCH_LOG.md). Ниже ссылки S/F с префиксом W1-A отсылают к этому реестру. Числа сохраняются в реестре, чтобы синтез не терял условия.

## C01. Что именно система должна утверждать

### Выбор: разделить observed state и нарушение правила

Предложение W1-A-P01: у СИЗ хранить две независимые сущности:

1. Наблюдение: `equipment_type`, `bodypart`, `state`, `owner_track`, `observability`, `evidence_time`.
2. Правило: где/когда/для какой роли требуется этот тип, какие внешне похожие типы допустимы.

`state` может быть `on_target_part`, `off_target_part`, `absent_visible`, `unknown`. Первая и вторая категории используют положительное наблюдение предмета/его положения. `absent_visible` требует достаточной видимости целевой части и валидированного negative classifier; это не просто отсутствие детекции. `unknown` охватывает мелкий/скрытый объект, crop, back-facing для задачи лица, плохой свет/blur, конкурирующих владельцев, неподдерживаемый тип.

Нарушение = требование активно AND установлено наблюдаемое нарушение. Отключённое/неизвестное требование нельзя заменять негативным состоянием СИЗ. Когда респиратор не требуется в зоне, снятый предмет не составляет автоматически нарушение; зона/role-policy поступает от постановщика/оператора.

| СИЗ | Что считать наблюдаемым соблюдением | Что считать наблюдаемым нарушением при активном требовании | Когда unknown | Что RGB не доказывает |
|---|---|---|---|---|
| Каска | Допустимый по локальной политике тип расположен на голове того же человека | Достаточно видимая голова без каски; каска явно в руке/на столе и голова видна голой | Голова скрыта/за границей; две подходящие головы; недостаточно деталей для hood/cap vs hardhat | Ударная пригодность, срок службы, внутренние повреждения, корректная подвеска; ремень вне отдельного наблюдаемого признака |
| Респиратор | Допустимый тип закрывает нужные области лица по согласованному визуальному правилу | Видимые открытые нос/рот при требовании; снят на шею/в руку и это видно | Лицо отвернуто, закрыто другим предметом/щитком; одноразовая маска неотличима от нужного типа | Fit/seal, фильтр против конкретного загрязнителя, исчерпание cartridge, достаточный oxygen |
| Жилет/сигнальная одежда | Предписанная одежда на торсе; допустимая куртка учитывается как альтернатива | Видимый торс без требуемой одежды | Торс закрыт/в кадре фрагмент/IR при требовании цвета | Сертифицированную отражательную способность, класс защиты, весь контур застёжек |
| Защитные очки | Нужный тип на глазах, если доступны нужные детали | Очки явно на лбу/в руке либо видимые глаза без очков | Спина/профиль, прозрачная модель неразличима, visor закрывает очки | Сертификацию стекла, устойчивость к воздействиям, пригодность обычных corrective glasses |
| Перчатки | **Для каждой требуемой руки** виден допустимый glove на кисти | Хотя бы одна требуемая видимая голая кисть | Руки в карманах/за корпусом/инструментом, тёмные перчатки сливаются, не видна вторая рука | Химическую стойкость/материал/целостность/правильный размер |

Это наша операциональная схема, не буквальная юридическая квалификация. Таблица нужна для разметки и демо; типы/обязательность должны подтвердиться полным кейсом.

Первичные основания: S10 manufacturer instructions отделяют видимое положение от pressure seal/fit procedures. S07–08 коммерческий API уже разделяет person/bodypart/item/coverage и indeterminate; S11 прямо запрещает определять наличие/отсутствие facePPE по невидимому лицу. Это показывает реализуемую структуру свидетельств, не независимую гарантию качества этих продуктов.

Критическое расхождение semantics: S11 «жилет» не означает high-vis; базовые S04 `glasses` могут быть corrective, `earmuffs` включают обычные headphones. Нельзя просто переименовать общий объект в требуемый защитный класс. Цвет каски может быть входом локальной role-policy, но его значение нельзя придумывать по цвету без правил объекта.

Ремень каски: `strap_visible_closed` можно добавить отдельным атрибутом только при соответствующем масштабе/ракурсе и GT. `helmet_on` не должно автоматически включать `strap_closed`. В этой ветке не получен первичный pixel/performance benchmark по ремню; при объявленном обязательном ремне потребуется отдельная ветка/проверка.

## C02. Детекция предмета, head-state, атрибуты, каскад и pose

### Сравнение постановок и условный выбор

| Постановка | Получаемый выход | Практическая польза | Ключевой отказ | Когда выбрать |
|---|---|---|---|---|
| Person+PPE object detector | Рамки независимых предметов/людей | Одно full-frame обращение, много классов, понятные evidence boxes | Неправильный владелец/предмет рядом; missed smallPPE превращается в ложное отсутствие | Базовый вариант для каски/жилета при явной association и visibility |
| `head_with_helmet`/`bare_head` | Локальное состояние головы | Меньше posthocownership; negative — положительно обнаруженная голая голова | Трудно прикрепить голову к полному track в толпе; hood/cap/small head | Простая каска без обязательной person identity, если данные именно head boxes |
| Whole-person states | Рамка человека+сочетание СИЗ | Прямая выдача compliance; A2 Pictor | Fine detail теряется в фоне/person crop, число комбинаций растёт; unknown часто не размечен | Ограниченные PPE и подходящие GT/камеры; выбирать по matched evaluation |
| Person crop→multi-label attributes | На каждого человека вектор атрибутов | Естественно несколько PPE одновременно, можно приоритизировать crop | Crop содержит соседей/предметы в руке; downstream ошибки person detection | Крупные изолированные люди/проходная, head/hand crops доступны |
| Bodypart/pose→PPE crop classifier/detector | Состояния на конкретных частях тела | Деталь получает больше inputpixels; явные unknown conditions | Ошибка pose уводит crop; невидимые части не восстановятся; стоимость на человека | Мелкие PPE или ownership действительно главный bottleneck |
| Learned HOI/relations | Обученная связь wore/held/person/part | Может выразить wear vs carry и сложные положения | Нужны relation labels/hard negatives, дополнительный model/export risk | После доказанного провала простых правил и при готовых данных; не default45h |

Это методическое сравнение. Архитектуры/веса/экспорт относятся к model_stack. Joint detection+pose возможен одним нейровызовом; это не значит, что любая исходная сеть так устроена или исполняется LinQ.

Фактическое сопоставление источников не устанавливает единственного победителя. S03 представляет все три Pictor approaches и на своих данных предпочитает direct states. S05 сравнивает на одинаковом detector и обучении relation rules/keypoint/direct states: общий выигрыш head-keypoint мал, small-object результаты хуже альтернатив. Поэтому не следует автоматически считать pose самым точным решением. S06 показывает полезный crop pipeline с indecisive, но даёт accuracy отдельных classifiers, не полную вероятность обнаружения нарушения. S12 даёт практический steel cascade, но framewise ошибки сохраняются. S13 указывает на классовую зависимость эффективности.

### Семантика четырёх важных источников: не смешивать bbox geometry

| Источник | Что обозначает класс | Какое нарушение из этого ещё НЕ следует | Что передать datasets |
|---|---|---|---|
| SHWD/S01 | `person` — negative normal **head**; `hat` — положительный helmet-wearing объект | `person` не рамка тела; отсутствие `hat` не достаточный negative | Сохранить namespace и annotation unit, визуально проверить реальные XML |
| SH17/S04 | Отдельные bodyparts/PPE; head любой ракурс, face только при видимом носе; medical mask; extended on/off | Head не тождествен bare_head; невидимый нос не равно отсутствие лица/респиратора; basehelmet не равен wornhelmet | Проверить tag export, не терять on/off; не переводить medicalmask в industrialrespirator |
| CHV/S02 | Person, vest, четыре цвета helmet; отдельные объекты | Helmet color не готовая role; object presence не wearing | Нужны owner/part annotations и localcolor mapping при требовании |
| Pictor/S03 | A1objects; A2/A3W/WH/WV/WHV | W не unknown; сочетания не показывают видимость частей | Ввести unknown/ignore по GT; проверить неоднозначные partial people из критики S05 |

Решение для45 часов: держать единый интерфейс part-state и использовать наиболее простой доступный detector за ним. Переход к pose не должен требовать менять event-rule schema. При наличии только готовых helmet/head весов обеспечить честный helmet-specific сценарий, а не заявлять все СИЗ по похожим меткам. Детекция generichelmet пригодна как первый сигнал, `compliant` требует соответствующего bodypart relationship.

## C03. Связь предмет–человек–часть тела

### Предложенная процедура W1-A-P02

На первом этапе рассматривать association как отдельную задачу, с собственной ошибкой. Personbbox containment — только генератор кандидатов. Для каждого PPE сохранить кандидаты owner и part-region, затем разрешать соответствия; объект PPE не должен независимо закрывать требование у нескольких людей.

Для каски простая геометрия: область головы из head detector, либо верхней части personbbox только в валидированном upright setting. Проверять перекрытие PPE с головой/anchor containment; расстояние нормировать на размер головы/человека. При конкурирующих владельцах и близких scores — unknown. Для толпы полезно one-to-one assignment helmet↔head; его можно сделать CPU. Для двух gloves это отношение к двум разным handparts, а не одному wholeperson. Для респиратора — к face lower region, а не торсу.

Абсолютная высота каски как процент personbbox ломается при наклоне/приседе/лежачем человеке; anchor от pose может помочь. Поза не гарантирует истинной видимости: предсказанная координата скрытой кисти остаётся гипотезой. Не следует засчитывать keypoint confidence как самостоятельный сертификат видимости. S05Algorithm1 позволяет выразить неизвестную голову, S06 демонстрирует отбрасывание потенциально скрытых кистей, S15 патент показывает практическую nose/shoulder localization, но не независимый выигрыш.

Трудные сцены для разметки/проверки:

- Каска в руке в нижней половине кадра; каска рядом с головой другого человека; снятие каски с поднятой рукой — held helmet временно перекрывает голову.
- Два человека пересеклись: helmetbbox геометрически содержит две head anchors; one-to-one минимизирует дубли, но ambiguity всё ещё требует unknown.
- Наклон к станку: голова уже не в верхней доле personbbox; соседний жилет/helmet лежит в том же crop.
- Каска на столе/стеллаже; mannequin/poster/reflection; белая cap/hood/baldhead; industrial shape confusing background.
- Объект за плечом, видимая только половина человека, helmet detector промолчал. Этот случай нельзя превращать в `bare_head`.

Две разные ошибки: **false violation** от missedhelmet при видимой голове и **false compliance** от каски в руке/у соседа. Улучшать precision violation при игнорировании falsecompliance опасно: получится вежливая система, пропускающая нарушения. Эти ошибки измеряются раздельно.

Самый большой остаток неизвестного C03: не найден первичный открытый эксперимент, где одинаковые detections и GTowner/part позволяют оценить geometricvsfullposevslearnedHOI именно на толпе/heldPPE. S05 даёт более узкое same-detector сравнение; нельзя выдавать его AP за отдельную точность ownership. Требуется E-A02.

## C04. Респиратор на лице/шее/в руке, очки и перчатки

### Респиратор: выбор постановки

Предложение W1-A-P03: начальная целевая taxonomy `approved_respirator_on_face`, `respirator_off_face` (при необходимости подтипы neck/hand), `face_visible_uncovered`, `unknown`. Не требовать обязательной находки снятого респиратора, чтобы подтвердить uncoveredface; одновременно не объявлять отсутствие по невидимому лицу. Если кейс требует именно действие снятия, кадр off-face доказывает состояние, но не факт перехода: нужны два состояния одного трека и временная последовательность.

Детектор предмета может оставить mask-on-neck положительным присутствием PPE. Whole-face classifier может считать его no-mask; это приемлемо для требования закрыть лицо, но теряет объяснение снятого состояния. Для demo оператору лучше показать crop лица и обнаруженный предмет на шее/руке, если доступен. Neck/hand labels — наше предложение; подтверждённого industrial benchmark для него в ветке не найдено.

Перенос COVID не следует сводить к утверждению, что все COVID данные только фронтальные. Источники разнообразны; проблема прежде всего в **другой целевой семантике**, видимости и домене. Surgical/cloth/N95 и cartridge respirator отличаются формой, не вся маска подходит зоне; некоторые classifiers смешивают закрытие лица с наличием любой маски. S04 сам по себе медицинский класс; S08genericcover не возвращает subtype; S13 прямо показывает, что cartridge class намного труднее familiar masks. S17 новая N95/goggle работа ограничена entrycheckpoint и abstract.

Условия малого PPE должны задаваться в nativecamera pixels до ресайза. Увеличение кропа сохраняет имеющийся сигнал и даёт сети больше inputextent, но не восстанавливает исчезнувшие нос/дужку/руку. Полезнее контролируемый вход с подходящим объективом/ракурсом, чем обещание superresolution. Точное требование минимального размера выбирается E-A03; product thresholds S11 — ориентир реализуемой зоны применимости, не обещание нашей модели.

Перчатки: хранить left/right state. Один visibleglove не может установить соблюдение обеих рук. Если правило требует обе и видна голая кисть, нарушение установлено независимо от второй неизвестной. Если одна в перчатке и другая скрыта, итог обеих — unknown. Это намеренно строже некоторой commercialpresence semanticsS11. Для инструмента, контакта с материалом и руки за спиной нужны отдельные видимые/неопределённые примеры.

Очки: обычные correctiveglasses и защитные goggles должны различаться там, где это требуется. Очки на лбу — видимый предмет, off-target. Прозрачная оправа/щиток поверх очков повышают необходимость unknown; состояние eyesvisible должно учитывать допустимую защиту, не считать любую окклюзию нарушением. Если нужный защитный тип визуально неотличим от обычного, classification по RGB не докажет соответствие: остаётся approvedtypespolicy/контрольный пункт/проверка человеком.

Наблюдаемость может быть camera/class-specific: каска спереди/сзади ещё распознаваема, facePPE сзади нет, рука за torso нет. Не нужен единый boolean `person_visible` для всех СИЗ.

## C05. Unknown, selective prediction, лучшие кадры и временная логика

### Выбор: явный отказ и ограниченная давность свидетельства

Предложение W1-A-P04: eligibility gate перед негативным решением. Проверить наличие целевой части, её nativepixels, crop truncation, occlusion/ambiguity, качество, допустимый ракурс и supportclass. Только eligible observation попадает в PPEstate classifier/rules. Причина отказа сохраняется: `part_not_visible`, `too_small`, `low_quality`, `owner_ambiguous`, `unsupported_type`, `inference_missing`. Отсутствие нейроответа/потеря видео — отдельная техническая причина, не barehead.

`unknown` не эквивалент безопасно; событие уже установившегося нарушения не должно автоматически закрываться только потому, что человек отвернулся. Передать Bstate machine три входа: observed violation, observedcompliance, unknown. Во время unknown остановить накопление положительного подтверждения и увеличить age последнего достоверного наблюдения; истечение срока означает lost/unknown, а не evidencecompliant. Пауза либо сброс окна после длительной окклюзии — настраиваемый выбор E-A04, не найденный универсальный порог.

Калибровка: отдельно precision/recallstates на eligibleframes и coverage на всех требуемых person-time/событиях. Иначе abstention создаёт искусственно прекрасную точность при почти нулевом охвате. S09 даёт корректную risk–coverage постановку, но i.i.d. guarantee здесь нельзя заявить без новых предпосылок. Frameconfidence и eventconfidence также разные сущности. Не назначать универсальный `confidence>.8` по примеру чужого API.

Лучшие кадры: отбирать evidence по независимым признакам качества/видимости и минимизировать дубли, а не просто выбирать максимум violation score за весь track. Иначе длинный трек почти неизбежно найдёт единичный FP, а кадр до снятия PPE будет слишком долго доказывать compliance. Хранить boundedrecentwindow и timestamp; выбирать отдельно лучший recenthead/face/left/right crop. Не склеивать соблюдение всех СИЗ из кадров, между которыми человек успел сменить состояние. Патент S14 — первичный след quality-basedviewselection, не доказательство его универсальности.

Практический набор evidence: исходный fullframe, partcrop, время/sourceframe, relation/owner, наблюдаемый predicate, qualityreason, model/configversion. Один sharpcrop может объяснять ручную проверку лучше десятков бездоказательных красных bbox. При unknown можно выбрать лучший имеющийся кадр и явно показать ограничение, не генерируя обвинение.

Отрицательный practicalevidenceS12 показывает, зачем это нужно: хороший средний F1 ещё совместим с серьёзными glovefailures в lowlight и false non-compliance от framewiseinconsistency. Рецепт temporal+visibility plausibly полезен, но в этой работе он futureenhancement: не выдавать снижение FA после нашего gate за установленную цифру.

## Требования методов к LinQ/нагрузке: передача C15

Расчёт ниже — логическое число вызовов, не benchmark и не совместимость.

| Вариант | Нейросеть | Рост с людьми | CPU-часть |
|---|---|---|---|
| Fullframeperson+PPE | Обычно1detector/frame | Размер выхода растёт, число исходных входов фиксировано | Association,tracking,eventlogic |
| Headdetector/state |1detector/frame; personnetwork отдельно при необходимости | Нужна связь с track | Matching/visibilityrules |
| Person→cropclassifier |1person pass + до Ppersoncrops | Может batching; логически Pcropinferences | Cropping/resize/track/evidence |
| Posejoint→Kbodypartclassifiers |1pose pass + до Σpersons visibleparts | Classifiers/heads/crops масштабируются с P/K | Cropgeometry,eligiblegates,matching |
| HeadorientedROI→multiPPEdetector |1localizer + до Pheadcrops | Один crop может дать сразу несколько PPE | Policy,association |

P — число людей, K — активные PPE/parts. Batch меняет число API invocations/latency, но не число входных cropimages. ROI/keypoint/rotatedcrop/resampling операции и INT8localization sensitivity нужно проверить на конкретной экспортной цепочке. Не установлено, поддерживает ли LinQ эти модели/ops. CPU геометрия не заменяет обязательный нейроинференс на LinQ, но сама его не требует.

## Предлагаемые E-ID: не выполнялись

### E-A01 — контракт классов и отрицательной разметки

- Решение: использовать ли доступные GT/веса без semanticremap.
- Вход: annotationguide и небольшой стратифицированный набор кадров каждого кандидата SHWD/SH17/CHV/Pictor, включая tiny/partial/backview/heldPPE; данные кейса при появлении.
- Шаги: для каждого bbox назвать annotationunit и observedpart; два разметчика независимо ставят compliant/violation/unknown и owner. Сверить labelnames/YAML/extendedtags с фактическими annotations; измерить disagreement и класс unknown, ошибочно размеченный negative.
- Метрики: доля bboxwrongunit, taxonomyconflicts, adjudicatedambiguity, false-negative-labelrate по сценам. Отдельно missingannotation vs visualabsence.
- Решение по результату: remap, relabel/ignore, исключить набор либо использовать только положительные objects. Успех не доказывает переноса камер/лицензий.

### E-A02 — ownership на фиксированных detections

- Решение: достаточно ли простой геометрии или pose стоимость оправдана.
- Вход: одни и те же person/head/PPEdetections либо oracleboxes; GTowner/part; сцены: изоляция, crowdcrossing, leaning, helmetinhand/table, donning/doffing.
- Шаги: сравнить containment/normalizedheaddistance, one-to-oneheadmatching, poseanchors. Сначала oracleboxes отделяют relationerror от detectorerror; затем реальный detector показывает полную цепочку. Пороги выбрать только calibrationclips, testclips из другой сцены.
- Метрики: owneraccuracy на разрешённых связях, ambiguousfraction, ложное complianceheldPPE, missedviolation, errorbycrowddensity/pose/nativeheadsize; latency и calls/person.
- Решение: оставить simplest вариант, выполняющий согласованные событийные требования; pose включить для конкретных failuregroups. Успех на постановочных клипах не доказывает deploymentcrowds.

### E-A03 — минимальная наблюдаемость по PPE

- Решение: где camera/class поддерживается и когда ставить unknown; нужен ли checkpoint.
- Вход: реальные camera/video с согласованными PPE типами и GT; натуральные разные расстояния/ракурсы/освещение плюс controlleddegradation для изоляции факторов. Nativehead/hand/PPEpixelmeasurements.
- Шаги: разметить visiblepositive/visiblenegative/unobservable; сравнить fullframevsnativecrop, head-statevsface/handclassifier. Оценивать helmet/respirator/glasses/gloves раздельно; особые классы respirator-neck/hand и protectivevscorrectiveglasses.
- Метрики: recallviolations, precision, falsecompliance, unknowncoverage, stateconfusion по size/angle/occlusion/light/compression; effectiveinputpixels и neuralcalls.
- Решение: выбрать empiricaloperatingregion и camera-specificgates. Ни одна точка sampledresolution не универсальный физический pixelthreshold; синтетическое уменьшение не заменяет реальные optics/blur/свет.

### E-A04 — temporalunknown и best-evidencepolicy

- Решение: какую логику подтверждения/aging принимать B/C10.
- Вход: временные GT и tracks для wear→remove→hold→occlude→rewear; дополнительные pureunknown и negativeclips; реальные timestamps/пропускикадров.
- Шаги: сравнить perframe, recenteligibleobservations, quality-selectedframes, разные unknownpause/reset/expirationpolicies. Calibration/test разделять по clip/camera, а не соседним кадрам. Не выбирать bestframe по testGT.
- Метрики: eventprecision/recall, FA/camera-hour, delay от observableonset, falseclosureunderocclusion, stalestateage, decisioncoverage/person-time, evidenceinterpretability.
- Решение: выбрать policy по tradeoff с явными неизвестными, не максимальному frameF1. Успех не подтверждает realworlddistribution при тренировочных отыгранных клипах.

### E-A05 — selectiveprediction и доменный сдвиг

- Решение: являются ли confidence/qualityranking полезными для отказа, сколько охвата теряется.
- Вход: calibrationcamera и unseenheldoutcamera/shift; трёхсостояний GT включая unsupportedPPE.
- Шаги: сравнить ungated, confidenceonly, visibility+sizegate, combinedselectivepolicy; заморозить пороги, построить risk–coverage на одинаковом test. Отдельно OOD и длительные окклюзии; считать ошибку на всём eligible и всём person-time.
- Метрики: selectiveerror/coveragecurve, eventFA, violationrecallincludingabstentions, unknownbyreason, calibrationerror истоимость лишних вызовов.
- Решение: включить отказ, если реальный tradeoff лучше приемлемого baseline. Не обещать теоретическую i.i.d.guarantee на коррелированном потоке.

## Адресная передача соседним темам

| Тема | Передать | Последствие |
|---|---|---|
| datasets | F01/F05, E-A01, PictorpartialnegativecritiqueF07 | Annotationunit/unknown/on-off критичнее названия класса; SH17medicalmask не industrialrespirator |
| model_stack | Семейства fullframeheadstate/partcascade; F08/F11/F20 | Не выбирать pose по общей репутации; нужны доступные экспортируемые weights и целевые классы |
| training_strategy | HardnegativesheldPPE/hood/cap, opaquevscolorlessglasses, one-visiblehand; E-A01/03 | Нужны relation/visibilitylabels и реальные сцены производства, нельзя учить unknown как negative |
| evaluation | E-A02/04/05 и falsecompliance от heldPPE | FrameAP/cropaccuracy не events; unknowncoverage и FAhours необходимы |
| video_architecture | Recentpartcrops/nativepixels; timestamp и inference-missingreason; Σvisibleparts нагрузка | Нельзя агрессивно уменьшать поток для малых PPE; неисторический bestframe |
| operator_product | Part-state/evidence/unknownreason; approvedPPEpolicy | Объяснимый evidence, возможность пересмотра; unknown не обвинение и не безопасно |
| linq_platform | Таблица нагрузки; detector/pose/cropclassifier и resampling | Только условные требования; нет проверенной совместимости |
| hackathon_strategy | Каска/жилетпервый маршрут; respiratorrequiresvisibleface/controlpoint | Демо показывает hardnegative/unknown, не декларирует ненаблюдаемую защиту |

## Остаточные вопросы Q-A

- Q-A01, постановщик/полный кейс, высший приоритет: какие конкретные респираторы/очки/сигнальная одежда допустимы, требуются ли обе перчатки/strap икак оценивается unknown? Меняет taxonomy ивозможность RGBproof.
- Q-A02, камеры/данные: native размерголовы/кистей,ракурс,реальноеосвещение/IR,скрытиестанками,предписанное placement. Меняетдоступностьмалых PPE и choicecheckpoint.
- Q-A03, E-A01/dataartifact: доступны ли SH17extendedon-offtags ввыбранном export, корректен ли unitSHWD икак размечены partialpeoplePictor? Ссылка на статью недостаточна.
- Q-A04, E-A02: даёт ли pose достаточный выигрыш ownership для наших crowd/leaningclips после учётас mallobjectloss и neuralcost?
- Q-A05, dataset+E-A03: существуют лит argetGT/готовые веса именно industrialrespiratorneck/hand и можно ли визуально подтвердить тип? Открытый поиск не получил такого прямого benchmark.
- Q-A06, E-A04/05: какая unknownaging/bestframepolicy сохраняет recall снятия иприемлемый decisioncoverage?
- Q-A07, benchmark/procurementartifact: есть ли реальный acceptanceprotocol с denominator/FAhours для малых PPE? Найденное ТЗ S16 — requirement без результатов.

## Короткая передача корню

Содержательно закрыты C01–C05 условными решениями, 17S/25F,5E. Самые важные находки: несовместимая семантика SHWDperson/SH17head-face-medicalmask; Pictorpartialunknownproblem; same-detectorcomparison не поддерживает универсальное превосходство pose; коммерческая документация явно признаёт facePPEindeterminate; реальные малые PPE/lowlight провалы;manufacturer граница fit/seal. Главные неизвестные — конкретный тип PPE,наблюдаемость камер,доступные теги/веса,relation ошибки на целевой сцене. Материалы готовы для freshcontext критика; новые операционные цифры не выдуманы.
