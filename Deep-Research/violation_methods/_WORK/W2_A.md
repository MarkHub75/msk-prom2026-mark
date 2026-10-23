# W2_A — K001/K003: предмет, покрытие и наблюдаемое снятие респиратора

Вторая волна, gpt-6.1-sol/medium. Доступ23.10.2026, проверенные часы06:19 Europe/Moscow(+03:00). Основания: входные Context-prompt.md/prompt-violation-methods-v2.md, PLAN, CRITIC K001/K003, W1_A/C и их EVIDENCE; новые материалы в [SOURCES_W2A/EVIDENCE.md](SOURCES_W2A/EVIDENCE.md), журнал [SEARCH_LOG.md](SOURCES_W2A/SEARCH_LOG.md). Это исследовательская спецификация и инспекция источников. Приложение, модели, benchmark и практические E-прогоны не выполнялись.

**Изменение решения:** off-body относится к отдельному экземпляру, а нарушение СИЗ — к отсутствию нужного покрытия части тела при действующем требовании. Промышленная head-state постановка получила новый полный первоисточник; готовые industrial neck/hand/removal annotations по-прежнему не получены. Официальная SH17 поставка теперь проверена на двух реальных примерах, а не только по статье: on/off/wearer fields в этих VOC/YOLO файлах отсутствуют. Для N95 найден и реально прочитан отдельный state annotation artifact R2PPE, но он медицинский.

## K001 — закрыто семантически, практическое качество не проверено

Исходный дефицит: W1_C называл отсутствие подтверждённого smoking/zone соблюдением; W1_A объединял off-target конкретного предмета с отсутствием защиты человека. Ни один новый benchmark не нужен для исправления этих двух логических ошибок. Ниже собственная спецификация **W2-A-F12 [proposal/formal definition]**, опирающаяся на разделение bodypart/equipment/CoversBodyPart у AWS W1-A-S07/08 и на трехзначную логику W1_B C10. Это предлагаемая семантика проекта, не обещание точности классификатора.

### Две единицы записи

`item_observation`: frame/time, item_id, визуальный тип, bbox, отношение к person/part, relation state T/F/U, источник связи. On-target подтверждает положение данного предмета. Off-target подтверждает, что именно этот экземпляр не закрывает нужную часть. Если он лежит отдельно, wearer может вообще отсутствовать; «владелец вещи» и «человек, которого вещь сейчас защищает» — разные отношения.

`coverage_observation`: person/track, target_part (head/eyes/nose-mouth/left-hand/right-hand), timestamp, approved-type-policy, coverage T/F/U, visibility/quality, evidence_item_ids, reason. CoverageT означает видимое покрытие хотя бы одним допустимым экземпляром. Покрытие — визуальный операциональный предикат, не доказательство fit/seal/сертификации или исправности.

CoverageF требует видимой целевой области и подтверждения отсутствия любого допускаемого покрытия, либо явно видимого недостаточного покрытия по согласованной политике. Оно не получается из «не найден положительный bbox», «найден off-body предмет», «виден неизвестный тип» или «все найденные предметы off». Unknown включает невидимую часть, недоступный ракурс, недостаточную детализацию, неоднозначного wearer и неподдерживаемый тип. Предмет поверх/под другим СИЗ или второй надетый экземпляр требуют оценить целевую часть, а не вывести F из одного неподходящего предмета.

Смысл агрегирования: `exists worn approved item` может установить coverageT; `no detected worn item` не устанавливает coverageF. Именно поэтому запасной респиратор на шее не отменяет надетый второй. Для обеих рук coverage=`left AND right`: голая видимая левая даётF независимо от скрытой правой; левая в перчатке и скрытая правая даютU.

Новая локальная иллюстрация W2-A-F02: [SH17 firefighter](SOURCES_W2A/firefighter.jpeg) содержит размеченную helmet на лежащей куртке и человека с головой вне кадра. У этого item off-target, у головы coverageU. Нельзя размечать человека как bare-head по этому кадру.

### Полные таблицы T/F/U, без подмены unknown соблюдением

T — утверждение подтверждено доступным наблюдением/контекстом; F — подтверждено его отрицание; U — оснований недостаточно. Это не пороги confidence. NOT:T→F,F→T,U→U. Любой rule-result относится только к названному правилу и временному окну.

Полная AND-таблица, используемая на каждом шаге:

| X∧Y | Y=T | Y=F | Y=U |
|---|---|---|---|
| X=T | T | F | U |
| X=F | F | F | F |
| X=U | U | F | U |

Для СИЗ R=`требование данного approved-type действует`, Z=`человек находится в зоне действия`, C=`целевая часть имеет допустимое визуальное покрытие`. Applicability G=R∧Z. R может зависеть от роли/операции/наряда; неизвестную роль не заменять false. Если правило не зональное, Z=T по определению правила.

| R | Z=T: G | Z=F: G | Z=U: G |
|---|---|---|---|
| T | T | F | U |
| F | F | F | F |
| U | U | F | U |

Состояние нарушения PPE: Vppe=G∧NOT C.

| G | C=T | C=F | C=U |
|---|---|---|---|
| T | F | T | U |
| F | F | F | F |
| U | F | U | U |

Это факторизация всех27 комбинаций observed coverage×requirement×zone, не выборочная иллюстрация. Если правило действует только во время действия A, применять ещё `V=Vppe∧A` по полной AND-таблице: вместе таблицы определяют все81 сочетание C/R/Z/A. Для обычного постоянно действующего PPE правила A=T. Действие снятия не следует автоматически добавлять в правило «носить респиратор»: иначе человек, пришедший уже без него, никогда не нарушит правило.

Для курения H=`подтверждённый supplied hazardous/flammable context и положение человека в нём`; S=`курение в данном окне`. Vsmoke=S∧H:

| S | H=T | H=F | H=U |
|---|---|---|---|
| T | T | F | U |
| F | F | F | F |
| U | U | F | U |

VsmokeF — это ложность **именно** «курит в опасной зоне»; это не глобальное compliance, отсутствие курения, отсутствие пожароопасности или безопасность человека. Если H составной, например zone_membership∧material_context∧activation, unknown любого необходимого компонента распространяется через тот же AND. Детектор бочки не устанавливает, что содержимое горюче.

**Откуда берётся negative smoking:** только из определённого наблюдаемого отрицательного интервала с согласованным разметочным контрактом. Например, разбор полного нужного окна при видимых руках/лице/объекте может установить питьё вместо smoking; не следует считать любое питьё доказательством отсутствия параллельного smoking. «Ни сигарету, ни action не подтвердили» само по себе даётU. По отсутствию smoke plume тоже нельзя поставитьF. False составного правила может быть надёжно получен из H=F, даже если S=U.

### Пять ручных контрпримеров из K001

Это выполненная ручная проверка согласованности определения, без исполнения кода/модели и без заявления measurement.

| Трасса | Наблюдение/контекст | Правильные предикаты и итог | Что нужно увидеть для отрицательного решения |
|---|---|---|---|
| W2-A-T01 | В зоне; рука/рот закрыты оборудованием, smoking cue не найден | H=T,S=U,Vsmoke=U | Достаточно наблюдаемое отрицательное окно либо подтверждённый выход из зоны; cue-missing недостаточно |
| W2-A-T02 | Smoking явно виден, ноги/anchor достоверно снаружи согласованной зоны | S=T,H=F,Vsmoke=F | Для этого rule отрицание уже даёт H=F; smoking остаётсяT |
| W2-A-T03 | Smoking виден; anchor скрыт, граница/материал неизвестны | S=T,H=U,Vsmoke=U | Надёжный H=F или отрицаниеS по согласованному окну; отсутствие material detection не H=F |
| W2-A-T04 | Одни approved очки на глазах, вторые в руке; либо один respirator на лице, второй на шее. Требование действует внутри зоны | itemA on-targetT,itemB on-targetF,C=T,R=T,Z=T,Vppe=F | Видимое допустимое покрытие уже устанавливает отрицание этого PPE-rule; запасной item ничего не отменяет |
| W2-A-T05 | Off-body respirator/helmet виден, лицо/голова скрыты или вне кадра. Требование действует | item on-targetF,C=U,R=T,Z=T,Vppe=U | Увидеть целевую часть с допустимой защитой для V=F; видимая открытая часть установит V=T; off-body item не решает ни то ни другое |

Unknown не safe. При начавшемся событии потеря видимости не является основанием observed-clear. Отдельный жизненный цикл хранит последнее достоверное состояние, его возраст и lost-observation; временное подтверждение не должно накапливать U как положительные кадры. Событие состояния может быть подтверждено по eligible observations, но несколько U подряд не доказывают непрерывность нарушения во всём пропуске.

Последствие закрытия K001: исправить C11 triad в синтезе; schema и GT обязаны хранить item relation отдельно от target coverage и от rule-result. Таблицы переданы W2_B/C и корню. Остаток для эксперимента — качество полученияT/F/U и временная политика, а не логическая таблица.

## K003 — область уточнена; прямой industrial neck/hand/removal artifact остаётся открытым

Исходный дефицит: SH17 extended on/off был только заявлением статьи; медицинский mask class мог быть принят за industrial respirator; состояние off-face смешивалось с действием снятия. Нужны actual annotations, guide, visibility и negative/unknown.

### Что изменилось после нового поиска

| Источник/артефакт | Реальная единица/состояния | Owner/wearer / visibility | Negative/unknown и предел |
|---|---|---|---|
| W2-A-S01/S02 SH17 | item/bodypart bbox; статья описывает extended on/off; реально прочитаны2VOC+2YOLO | В этих XML/TXT нет wearer/relation/on-off fields; off-body helmet визуально подтверждён.17indices YAML, не порядок Table2 | `face-mask`=medical; off-body labels не дают coverage. Отдельный extended artifact не получен; нельзя отрицать его существование |
| W2-A-S03 industrial YOLOv8-LPE fulltext | head-state; industrial3M cartridge, front/side wear/no_wear/wear_wrong, back_head | Fig2 boxes на головах, отдельная ориентацияback. Реальный annotation файл/guide не получен | Медицинская маска вместо требуемой полумаски — wrong в области источника. Back remap→U наш. Neck/hand/removal и explicit unknown классов нет |
| W2-A-S05/S06 R2PPE guide+actualJSON | state bbox: MaskAbsent,MaskIncomplete,N95Complete,N95Strap,PAPR,Head и др. | actual123751 annotation key-union не имеет wearer/track/relation. Guide неоднозначные labels опускает | Пропуск label не negative; N95 subtype отличим от regularmask в этом контракте. Клиника не cartridge workshop. Нет neck/hand/remove labels |
| W2-A-S07 FMR-DB institutional abstract | half/full-face/disposable respirator categories; occlusion negatives | Это реально прочитанный abstract; datafiles не получены | Не прямое доказательство off-neck/hand, unknown или transition разметки |
| W1-A-S10 manufacturer3M | donning/strap/seal instruction | Требует человеческой fit/seal проверки | Не visual GT/benchmark; RGB не доказывает герметичность/пригодность cartridge |

**W2-A-F13 [inference from artifact inspection].** SH17 useful positive object data не заменяет wearer/coverage GT. Base YOLO index5 с именем face-mask не означает industrial type. Публикация слова extended не означает, что training loader прочитает on/off из текущих TXT. Достаточное условие использования extended версии: реально получить отдельный annotation artifact, inspect fields/guide и подтвердить mapping на видимых on/off examples. До этого on/off строится собственной разметкой/геометрией как проверяемое предложение.

Новая industrial работа S03 полезнее ещё одного COVID detector: она непосредственно разделяет cartridge на голове, видимое отсутствие и wrong mask; но не даёт готового off-body/remove решения. «Wrong» также не следует автоматически трактовать как нарушенную посадку/strap: в §1 это может означать медицинскую маску. Class names без guide опасны. Сами метрики S03 имеют оговорки W2-A-F06; выбор главы по этим aggregate цифрам не обоснован.

### Два разных целевых задания и один дополнительный предикат

**Постановка A — `face visibly uncovered under requirement`.** Требуется установить визуальное отсутствие нужного покрытия сейчас, а не доказать историю предмета. Минимум: согласованный required/approved-type policy, видимый nose-mouth region с достаточной детализацией и допустимым ракурсом, owner-person link, действующая зона/требование, timestamps. Кандидат: head/face state classifier или local detector+coverage relation. Необязательно находить снятый предмет на шее/в руке. Если лицо открыто, человек пришёл в кадр уже без СИЗ, violation состояния может бытьT.

**Stop condition A:** лицо скрыто/спина, слишком мало деталей, неизвестный тип или owner ambiguity → coverageU. Не выдавать absent по missingbbox, не восстанавливать голое лицо из предмета в руке. Для already-open event — lost-observation, не clear. Если класс/камера не поддерживаются, отложить сценарий/предложить checkpoint, а не обещать устранить неизвестное resize.

**Постановка B — `observed removal transition`.** Сначала постановщик должен уточнить: нужно само действие снятия конкретного item или начало отсутствия покрытия? Для строгого item-doffing нужны привязанный item и человек, наблюдаемый on-target до, временно связанная траектория/контакт снятия и off-target после; непрерывность/пропуски и допустимый интервал должны быть согласованы. Для coverage-loss transition достаточно достоверногоC=T до иC=F после у того же человека при приемлемой непрерывности, но это не всегда идентификация снятого item. Если событие произошло в blind gap, можно локализовать изменение между последнимT и первымF, нельзя заявить наблюдённое действие или точный onset.

**Stop condition B:** нет достоверного состояния «до», произошёл IDswitch, лицо скрыто в критическом промежутке, либо item identity неоднозначна → removalU/not observed. При этом состояние uncovered может отдельно бытьT. Начало клипа с голым лицом — нарушение состояния при требовании, но не observed removal.

**Дополнительный предикат D=`данный item снят` независим от C.** Человек снимает один из двух надетых допустимых предметов: D=T, но C может остатьсяT, Vppe=F. Человек надевает второй респиратор до снятия первого: нельзя выдавать violation из одного doffing action. Для правила нарушения вследствие снятия требуется `D∧R∧Z∧NOT C`, а не толькоD. Это уточнение предотвращает повтор ошибки K001 во временной модели.

Эти маршруты — **W2-A-F14 [proposal]**, не запущенная реализация. Нейросетевые входы A можно ограничить visible face/head crops; B потребует time-aligned sequence/item association. Отсюда разные GT, нагрузка и задержка. LinQ support любого конкретного export остаётся за отдельным compile/execute/precision gate, а не следует из названия YOLOv8.

## Минимальные следующие проверки и вопросы

### W2-A-E01 — semantic annotation acceptance до обучения

Решение: пригоден ли конкретный annotation export для coverage/removal задачи. Входы: actual выбранный архив и guide, реальные on-face/off-neck/off-hand/duplicate-item/back-head/occlusion кадры, разрешённый PPE policy. Два разметчика отдельно ставят item relation, coverage, requirement, zone и rule-result. Проверить IDs по YAML, пропуски ambiguity/negative, наличие wearer/track/time. Сохранить disagreement и причиныU; universal numeric acceptance threshold не придумывать. Выход: explicit remap/ignore/relabel либо отказ от использования набора как stateGT. Успех не доказывает перенос камер или доступность весов. Уже выполненная W2 инспекция — только узкая часть этого acceptance, не весь E01.

### W2-A-E02 — state против transition на одних клипах

Решение: какой смысл «снят респиратор» реально поддержать. Входы: native clips с согласованными типами; wear→remove→neck/hand→rewear, вступление уже uncovered, скрытое снятие, duplicate/spare, swapping, чужой item/IDswitch. GT C(t),D(t),visibility и applicability раздельны. Сначала ручная наблюдаемость, затем в практической волне две модели/логики. Считать state confusion, false-compliance, unknown/person-time, event recall, FA/camera-hour, observable-onset delay и долю false-removal из blind gaps. Если разметчики не видят transition, пометить U, не forced-negative. Решение: ограничить demo/state-only либо включить transition при подтверждённом выигрыше. Успех на постановочных клипах не доказывает plant deployment или fit/seal.

| Q-ID | Остаток / получение | Что меняет |
|---|---|---|
| W2-A-Q01 P0 постановщик | «Снят»=видимое отсутствие защиты сейчас, observed doffing или оба? Что делать при клипе без предыстории? | Выбор A/B, GT и onset |
| W2-A-Q02 P0 постановщик+video | Какие approved respirator types, видимы ли nose-mouth/голова nativepixels и камеры? Допустим ли checkpoint? | Возможность meaningfulT/F, поддерживаемая область |
| W2-A-Q03 P1 artifact | Где отдельный SH17extended archive/guide, какие поля wearer/on-off? Искали repo/tree/releases/Kaggle, дваbaseexamples прочитаны | Нужна ли собственная relationship разметка |
| W2-A-Q04 P1 artifact/данные | Есть ли industrial neck/hand/removal GT либо целевые клипы? Китайский fulltext даёт head-state, файлы не получены; R2PPE даёт medical state | Доступность обучения/валидации B |
| W2-A-Q05 P0 политика/evaluation | Как учитывать unknown в denominator, разрешённая давность evidence, latency/false-alert budget? | Event confidence, coverage и правила завершения |

## Передача сборщику и соседям

- **Корень/сборщик:** K001 закрыто определениями/таблицами/5ручными трассами. K003 **уточнена область**, direct industrial off-neck/hand/removal artifact остаётся открытым. F01–11 — новые источники/наблюдения; F12–14 — собственные формальные определения/выводы/предложения. Не объединять статусы.
- **datasets/training_strategy:** SH17 class-order Table2 не YOLOindex; базовые файлы не доказательство extended. R2PPE ambiguous omission не negative; actualJSON source сохранён summary. Industrial3M семантика S03 полезна для своей taxonomy, но не выдаёт нам dataset/weights.
- **evaluation/operator_product:** ruleF относится только к этому правилу. Separate item-doff, coverage-loss и visible-state evidence; неизвестное не safety/clear. Хранить наблюдаемый onset и bounds изменения через gap.
- **W2_B/C:** отправлены K001 exactAND/itemcoverage semantics. Согласовать temporal falseclosure/unknownaging и smoking source, не переопределять U как непойманныйpositive. Ни патент, ни статья не дают operational FA для наших камер.
- **model_stack/linq_platform:** A/B требуют разных inputs/temporal graph и call budget. Generic medical mask detector не substitute industrial approved-type coverage. Выбор checkpoint/экспорта подтверждать практическими gates.
