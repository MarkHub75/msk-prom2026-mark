# W1_B — зоны, техника, трекинг и обоснованные события

Исследование первой волны; C06–C10. Дата: 2026-10-23, Europe/Moscow (+03:00). Роль: gpt-6.1-sol / medium. Входы: Context-prompt.md, prompt-violation-methods-v2.md, _WORK/PLAN.md и секция W1_B AGENT_PROMPTS.md. Полного кейса, камер, SDK/конфигурации LinQ и данных нет. Обязательность нейроинференса LinQ принята как исходный контекст, совместимость конкретных сетей не проверялась. Training/benchmark/разработка приложения не выполнялись.

Первичные сохранённые выписки: [SOURCES_B/EVIDENCE.md](SOURCES_B/EVIDENCE.md), журнал запросов и недоступности: [SOURCES_B/SEARCH_LOG.md](SOURCES_B/SEARCH_LOG.md). Branch IDs W1-B-S/F сохранены для последующей нормализации. DOC/CODE/MEAS/INF/PROPOSAL/UNKNOWN различаются ниже; чтение кода не означает его выполнение.

## Что меняет выбор команды

Для статической опасной области на видимом полу разумный первый маршрут — детектор человека, лёгкий трекер, нижняя точка контакта с полом, отдельное правило во времени по timestamp и событие с доказательствами. Если задача означает «любая часть тела коснулась опасного объёма», такой маршрут решает другую задачу; это нужно установить до демонстрации. Касание bbox — особенно слабая подмена этого определения.

Метры, динамическая область около техники и допустимость присутствия требуют новых входов. Одной рамки погрузчика недостаточно, чтобы знать footprint, положение вил, рабочий цикл или полномочия человека. Сначала можно честно сделать «человек в заданной оператором области», затем расширять до сближения на калиброванной плоскости при подтверждённых условиях.

Самый полезный отрицательный результат: нельзя взять название настройки VMS за точное определение алгоритма. В Frigate обнаружено расхождение обещанной последовательности кадров и прочитанного v0.18.2 update; dwell внутри реализован через fps-счётчик. В AXIS short-lived filter означает возраст наблюдения в изображении, не время внутри зоны. Отдельно различаются подтверждение нарушения, завершение события, группирование review и cooldown уведомления.

## C06. Геометрия опасной зоны: сначала определить, что пересекается

### Условный выбор

| Требование кейса | Геометрический предикат | Условие применимости / решение |
|---|---|---|
| «Человек стоит/идёт по запрещённой части пола» | point-in-polygon по ground-contact anchor | Начать с bottom center; если bbox обрезан/стопы за препятствием — unknown. Подтвердить ошибку на наших ракурсах E-B01 |
| «Хотя бы одна стопа в зоне» | видимые ankles/foot keypoints: any point in polygon | Требуется pose, confidence/visibility gate. Среднее двух ankles может скрыть пересечение одной ногой; не заменять смысл автоматически |
| «Весь человек в зоне» | явно выбранная containment semantics | Несколько anchors ≠ точная containment сегмента тела. Уточнить, нужна рамка или маска |
| «Любая часть тела в области/около станка» | mask/body region against image ROI либо 3D envelope | Нужен другой label/проверка; floor anchor не наблюдает руку над работающим механизмом |
| «Вход через границу в заданном направлении» | переход между сторонами конечного отрезка + direction + история одного объекта | Не считать просто нахождение на линии. Различать линию входа, линию выхода и неизвестное начало трека уже внутри |
| «Менее d метров от техники» | distance в калиброванной плоскости от человека до footprint/envelope техники | Нужны масштаб, ground calibration и оценка ошибки. Pixels не конвертируются одним коэффициентом по всему перспективному кадру |

**Основание DOC/CODE:** Frigate использует нижний центр (F01); supervision проверяет anchors, any/all (F10); DeepStream разделяет линию и направление и требует историю для crossing (F12). Эти реализации поддерживают выбранную семантику, но не доказывают, что именно её требует заказчик.

**INF:** intersection bbox–polygon подходит для грубого candidate stage. У наклонённого человека верхняя часть bbox может пересечь полигон на изображении при ногах снаружи. Обратная ошибка: bottom center может оказаться за границей при одной ноге внутри. В толпе рамка нередко включает чужие ноги; pose не устраняет ownership автоматически. Нужен отдельный признак `ground_contact_observable`, а не правило «нет ankles — нарушение».

### Плоскость пола, граница и камера

Гомография связывает плоскости (F13), поэтому для ground-plane расстояний калибровать надо точки **на том же полу**, покрывающие используемый участок. Для ручной калибровки предлагаем как минимум четыре неколлинеарных известных соответствия и дополнительные контрольные точки для проверки; больше точек помогают оценить остаток ошибки, но не делают неверную плоскость правильной. Сохранять единицы, исходное разрешение, distortion handling, calibration_version, область валидности и residual на независимых точках. Участок с лестницей/рампой/платформой требует отдельной модели или отказа от metric claim. Ниже границы поля зрения точность не экстраполировать.

**PROPOSAL пространственного гистерезиса:** определить signed distance до границы. Подтверждать вход только глубже внутренней полосы, выход — за внешней; между ними сохранять предыдущий геометрический state и маркировать boundary uncertainty. Ширину полосы выбирать по E-B01 из ошибки локализации; не выдавать фиксированные 10px/20cm за универсальную норму. Если нет метрической калибровки, ширина задаётся в image units и имеет локальный смысл.

**PROPOSAL crossing:** хранить последнее уверенное положение по каждой стороне. Вход — смена сторон с допустимым пересечением конечного отрезка и направлением перемещения; джиттер в boundary band не создаёт новую серию пересечений. Временной разрыв больше установленного допустимого gap делает момент пересечения неизвестным. Если обе наблюдаемые точки снаружи, путь между ними не обязан быть прямым: интерполяция даёт гипотезу. Нельзя уверенно говорить «не входил», если быстрый объект мог пересечь всю зону между выборками.

**PROPOSAL camera validity:** `scene_version` меняется при pan/tilt/zoom, crop, rotation, смене камеры/пресета. Простое resize требует согласованного преобразования координат, а перспектива требует новой calibration. Детекция camera change может быть отдельным health check по стабильным точкам сцены; при несогласованности зоны выключаются до восстановления геометрии. GMC трекера и автоматическая регистрация anchor-transform не гарантируют валидность физической зоны. AXIS отдельно требует recalibration при смене preset (F17).

**Результат C06:** выбрать ground-contact для walk-in зоны при видимом полу; bbox intersection оставить кандидатным или явным другим определением. Homography опциональна для метров, не обязательна для статического image-polygon. Не заявлять 3D контроль или касание механизмов по одному floor anchor.

## C07. Движущаяся техника и условная опасность

### Разделить четыре предиката

1. `person_present`: человек действительно наблюдается, его ground anchor валиден.
2. `equipment_zone`: известная область, footprint или рабочий envelope техники; это не обязательно bbox.
3. `hazard_active`: зона сейчас опасна. Состояние может прийти от PLC/API/согласованного расписания, либо быть самостоятельным визуальным предикатом с ошибкой и unknown.
4. `authorized`: есть подтверждённое разрешение конкретному человеку/роли на конкретную зону и время.

**PROPOSAL:** тревога «несанкционированное присутствие в активной зоне» допустима только при известных истинных первых трёх условиях и известном ложном authorized. Если система умеет только геометрию, имя события должно быть «человек в зоне Z», без слов об отсутствии полномочий. Цвет жилета и постоянный tracker_id сами по себе не дают право доступа. Отсутствующий access-control feed не означает «все неавторизованы». Машина без видимого движения может быть работающей; парковка/активация/движение — разные состояния.

### Ступени метода

| Уровень | Что можно реализовать | Что понадобится сверх детекций | Нерешаемое без новых входов |
|---|---|---|---|
| Статическая image ROI | запрет прохода по выделенной части изображения | камера фиксирована, понятное правило | физическая дистанция и действительное включение оборудования |
| Динамическая image ROI | условная область, связанная с bbox/маской техники | устойчивый track машины, согласованная эвристика expansion | одинаковая безопасная ширина в метрах по кадру, высота рабочего органа |
| Ground-plane envelope | круг/полигон вокруг калиброванного footprint | метрическая homography, габариты/ориентация/ground points | поднятые вилы, стрела/ковш вне пола, человек на иной высоте |
| Direction/speed aware | front/rear sector или swept footprint по траектории | time-correct velocity, ориентация корпуса отдельно от velocity, latency/error budget | гарантированный collision prediction по неизвестному будущему поведению |
| Operational safety rule | envelope активен при работе, исключения по персоналу | надёжные machine-state и authorization inputs | достоверность внешних сигналов при outage |

**INF:** для proximity важна минимальная дистанция от человека до корпуса/рабочего envelope, а не между двумя bbox-centers. Для длинной машины расстояние до центра систематически скрывает близость к краю. Ground envelope можно строить как Minkowski buffer footprint на выбранный запас — это предлагаемая геометрия, не найденный норматив.

**PROPOSAL динамической области:** из пары position/heading строить envelope впереди/сзади машины; порог скорости вводить только с единицами и калибровкой. Поворот корпуса не всегда совпадает с direction of travel, а стрелу нельзя считать частью неподвижного основания. Для time-to-collision проецировать relative velocity только при устойчивой оценке и показывать unknown при остановке, резком повороте или огромной ошибке. В 45 часов не делать TTC главным обещанием без данных и верификации.

Первичный пример monocular proximity действительно найден: камера на экскаваторе и специально заданные геометрические предположения (F19). Его planar-ground limitation опровергает идею «монокулярная камера всегда даёт метры без калибровки». Примерные размеры статьи не переносятся в цех. Frigate speed тоже содержит узкие ограничения (F02); API AXIS radar speed (F18) не подтверждает monocular speed.

**Результат C07:** динамическая image-zone — честный условный fallback. Metric proximity включать только после E-B02; authorization/activation моделировать отдельными трёхзначными входами. Точная дистанция/скорость и 3D collision awareness без этих входов остаются unknown.

## C08. Трекинг: идентичность нужна событию, но не доказывает его

### Выбор для первой реализации

| Вариант | Основание и польза | Риск для нашего события | Условие выбора |
|---|---|---|---|
| ByteTrack | связывает high/low detections, не требует ReID (F14) | IoU/motion gates при редких кадрах; detector threshold может удалить полезные low scores ещё до tracker | первый baseline при неподвижной камере и умеренных occlusions |
| OC-SORT | observation-centric исправление motion error; одинаковые detections показывают association gain с иным tradeoff MOTA (F15) | low FPS всё ещё даёт нулевой IoU; ORU виртуальная траектория не есть реальная видимость | второй кандидат на nonlinear motion/occlusions, оценивать события E-B03 |
| BoT-SORT без/с ReID | GMC и optional appearance; код gating F16 | выше вычислительная нагрузка ReID; похожая форма/размытые кропы/геометрический gate | включать ReID, только если снижает ошибочную передачу event state и дубли при измеренной цене |

Это условная рекомендация, не рейтинг всех трекеров. Процент HOTA на MOT17 не доказывает правильность событий промышленной безопасности; annotation, detector, FPS и domain отличаются. Открытый сравнительный пример F15 полезен именно тем, что удерживает detections одинаковыми и показывает разнонаправленные метрики.

### Время и прореживание

**CODE:** у прочитанного ByteTrack вызов update является дискретным шагом, dt в Kalman фиксирован; frame_rate корректирует lost buffer (F14). **INF:** если подавать нерегулярные результаты удалённого инференса, один update может соответствовать разным реальным промежуткам. Нельзя затем выводить скорость и dwell из номера обработанного кадра. Задержка результата также не равна времени действия на видео.

**PROPOSAL:** каждое наблюдение несёт source frame timestamp/PTS, source frame index, inference completion time и свежесть. Event engine использует source-time; live notification latency использует согласованное время захвата/доставки/публикации. Порядок результатов одного потока проверяется; опоздавший кадр не должен произвольно перематывать state. Timestamp-aware motion model потребует корректировки transition/process covariance, а не просто подстановки fps в один конструктор. Альтернатива — строго фиксированный cadence с известной семантикой пропущенных шагов и отдельно timestamp-based событиями. Конкретный SDK API для этого здесь не предлагается.

Снижение FPS проверять не только средним. Серии пропусков, случайный jitter и пауза связи при том же среднем FPS могут давать иной результат. `max_age=30` в кадровом tracker при 3 и 30 updates/s — разные физические интервалы. Объект может исчезнуть внутри зоны, пройти короткую зону между двумя samples, потерять ID на встречном человеке.

### Как ID ошибки портят safety event

- **Fragmentation:** один человек получает новый ID. Накопленный dwell сбрасывается, нарушение может не подтвердиться; либо создаются два события и двойное уведомление.
- **ID switch:** state «без каски» переносится на другого человека; безопасный worker наследует нарушение или нарушитель наследует compliant.
- **False reactivation:** склейка с неправильным человеком объединяет независимые нарушения и прячет повторный вход.
- **Prediction-only:** tracker держит прошлую геометрию при отсутствии measurement, а event engine ошибочно накапливает подтверждённые секунды.

**PROPOSAL aggregation:** хранить атрибуты вместе с visibility/quality и временем истечения. Выбирать лучшие видимые кадры для конкретного атрибута; сглаживание не должно превращать невидимость в negative. При неоднозначном re-association freeze/expire person attributes; передача state между ID только как отдельный контролируемый механизм с provenance, а не proximity-only склейка. Для геозоны допускается incident continuity через короткий gap, но с полем uncertainty и явным разграничением person identity и event identity.

**Результат C08:** начать с ByteTrack на CPU после детектора, сохранить низкие person scores для association и timestamp provenance. OC-SORT — содержательный второй кандидат; ReID не включать только ради модного названия. Решение по E-B03 должно учитывать event duplicates/misses и contaminated attributes, а не только IDS.

## C09. Подтверждение, dwell, пропажа сигнала и cooldown

### Что реально есть в продуктах

| Механизм | Первичный факт | Что не следует из названия |
|---|---|---|
| Frigate zone inertia/dwell | defaults F05; documentation F01, code F06 | Не принимать за проверенные consecutive frames/continuous wall-clock dwell без trace |
| Frigate object confidence | per-frame gate и история median F04/F07 | Это не автоматически safety-rule N/M и не calibrating probability |
| Frigate track disappearance | вычисляемые кадровые defaults F08 | Конец tracker lifecycle не доказывает физический выход |
| Frigate review cutoff | 40/30 seconds и последняя активность F09 | Cutoff группирования не есть cooldown/период запрета нового события |
| AXIS short-lived | возраст в image F18 | Не считать временем нахождения в опасном полигоне |
| AXIS time in area / keep active | длительность и удержание rule по track F17 | Alarm pulse, active rule и запись — отдельные вещи |

Числа в таблице — найденные defaults конкретных систем, не советы поставить их в safety-прототип. Подтверждённый первичный промышленный протокол приёмки с false alarms/hour пока не получен (SEARCH_LOG). Русские ITV ключи полезны как зацепка, но их параметры остались S19 partial-read и не использованы как факт.

### Проектируемый автомат

**PROPOSAL**, применим к каждому rule × субъект × scene_version; для proximity субъект — пара person/equipment.

`clear → candidate → active → resolving → ended`

Отдельное `observation_state = observed / occluded / stale / signal_lost / scene_invalid`; оно не сводится к violation=true/false. Может сосуществовать с active событием.

- **clear:** наблюдаемое соблюдение либо отсутствие ранее подтверждённого события. Не называется «доказано безопасно», если нужная часть кадра не видна.
- **candidate:** есть наблюдаемые признаки; сохраняется первый qualifying timestamp и промежуточные evidence records.
- **active:** выполнен выбранный temporal predicate. У события разные `observed_start` и `confirmed_at`; первое допускает ретроспективную привязку клипа, второе измеряет фактическую задержку принятия решения.
- **resolving:** видимое восстановление/выход пока проходит отдельный exit-confirmation/hysteresis. Его правило не обязано совпадать с входом.
- **ended:** последняя причина — observed_exit, observed_compliance, rule_disabled, scene_invalid, track_lost_timeout, stream_lost или identity_ambiguous. Только первые два означают наблюдаемое прекращение нарушения.

**Unknown policy:** неизвестные интервалы не добавлять к положительно наблюдаемой длительности. При коротком occlusion можно сохранять active incident для удобства расследования, но обновлять last_observed_at и coverage. Для нового подтверждения continuous dwell unknown разрывает доказанную непрерывность; для «накопленного времени в окне» он не считается ни positive, ни negative. Долгий gap закрывает технически с причиной и right-censored duration, без утверждения «человек вышел». Возврат после gap — отдельное событие либо связь `possibly_same_incident`, если политика это разрешает. Поведение обоих вариантов проверить E-B04.

### Не смешивать временные операторы

| Оператор | Явное определение проекта | Цена и ограничение |
|---|---|---|
| Consecutive hits | N подряд **валидных свежих** наблюдений predicate=true; false/unknown policy задана отдельно | зависит от cadence; N не секунды |
| N of M | минимум N положительных среди последних M валидных/всех samples; denominator и unknown policy записаны | редкая ошибка может пережить vote, серия коррелированных кадров не даёт независимые доказательства |
| Positive duration in W seconds | сумма ограниченных поддержанных интервалов true внутри source-time window | нужен maximum admissible observation gap; нельзя заполнить длинную дыру previous value |
| Continuous dwell | true от первого до последнего наблюдения с gap≤G и оговорённой дискретной поддержкой | не доказывает состояние между кадрами; при low FPS интервал неопределённости шире |
| Cooldown notification | подавление повторной отправки тому же ключу, состояние и evidence продолжают обновляться | может скрыть новый independent incident, если ключ слишком широкий |
| Merge gap | объединение эпизодов после короткого gap при ясном identity/правиле | может объединить реальное прекращение и новый вход; это продуктовая политика, не качество детектора |

**Предлагаемые начальные настройки для E, не универсальные thresholds:** прогнать варианты confirmation 0/0.5/1/2 секунды, exit 0/0.5/1 секунды, gap tolerance 0/один ожидаемый интервал/две ожидаемых выборки; задавать масштаб по реальному cadence и кратчайшему важному нарушению. Для N/M сравнить 1/1, 2/3 и 3/5 на одинаковых timestamp sequences, без трактовки их как нормативов. Cooldown первоначально выключить для измерения raw duplicates; затем сравнить подавление per-event notifications и merge policy. Если полный кейс требует немедленного входа, длительный dwell может быть недопустимым пропуском, даже если снижает FA.

**Результат C09:** собственный timestamp-based state machine легче проверить, чем неявно копировать lifecycle домашней VMS. Повторные updates используют тот же event_id; cooldown ограничивает delivery, а не знание о событии. Пропажа track/signal — unknown/censored cause, не compliant.

## C10. Декларативное правило, event schema и GT matching

### Минимальная выразительность правил

Источники показывают реальные декларативные primitives: class/ROI/direction (F12), zone filters и review gates (F01/F09), capabilities-based scenario schema (F18). Они не доказывают наличие универсального scene-graph DSL или корректность перевода свободного текста в safety-rule.

**PROPOSAL:** для 45 часов ограничить rule schema известными typed predicates и temporal operator. Не выполнять автоматически текстовое «рядом со станком без каски»: пользователь должен получить конкретные зоны, единицы, duration, unknown behavior и проверить их. `AND` должен быть трёхзначным: false делает conjunction false, иначе при хотя бы одном unknown результат unknown. Обычное `NOT unknown = true` запрещено; `NOT unknown = unknown`.

Пример **псевдоконфигурации**, не API существующей библиотеки:

```yaml
rule_id: restricted_floor_01
rule_version: 1
scene_version: camera_01_preset_A_v1
subject: person_track
when:
  all:
    - ground_contact_observable: true
    - inside_zone: {zone_id: Z1, anchor: bottom_center}
    - equipment_active: {source: validated_external_state}
temporal:
  operator: continuous_observed_duration
  confirm_seconds: TO_SELECT_BY_E_B04
  max_observation_gap_seconds: TO_SELECT_BY_CADENCE
on_unknown: freeze_incident_do_not_accumulate_evidence
end:
  observed_exit_confirmation_seconds: TO_SELECT_BY_E_B04
  track_loss: end_with_censored_reason_after_timeout
notifications:
  deduplicate_by: event_id
```

Если external equipment state отсутствует, правило нельзя формально считать готовым; либо удалить этот предикат и переименовать событие, либо сохранять unknown. У `rule_version` и `scene_version` разный смысл: изменение порога не равно перемещению камеры. Перенастройка правила внутри события должна сохранять old version либо явно завершать/пересоздавать событие.

### Схема факта наблюдения и события

**PROPOSAL observation:** `camera_id`, `scene_version`, `source_timestamp`, `source_frame_id`, `inference_received_at`, `model_version`, `track_id`, `track_segment_id`, `detector_bbox`, `anchor`, `anchor_method`, `geometry_valid`, `visibility`, `quality_flags`, `predicates[{name, value:true|false|unknown, score, provenance}]`, `fresh_measurement:boolean`. Score каждого head не заменяет value/visibility. Для пары добавляются equipment_track_id и geometry/activation sources.

**PROPOSAL event:**

| Поля | Назначение |
|---|---|
| event_id, revision, rule_id/version, scene_version | стабильная идентичность, повторная доставка и воспроизводимость |
| camera_id, involved_track_segments, person/equipment association status | не смешивать tracker ID с реальной личностью человека |
| observed_start, confirmed_at, last_observed_at, observed_end, published_at | отделить начало признаков, подтверждение и коммуникационную задержку |
| status, observation_state, end_reason, duration_lower_bound, censored | различать доказанное прекращение и потерю наблюдения |
| zone_id, anchor method, calibration version, distance_units/error if available | что именно измерялось и как |
| evidence frame IDs/timestamps, crop/fullframe references, pre/post clip window | дать возможность проверить predicate вместе с окружением |
| visibility coverage, contributing observations, applied temporal settings | не скрывать дыру в наблюдениях за одной уверенной картинкой |
| notification revisions/delivery IDs, merged_from, possible_related_event_ids | объяснить дубли/склейку и не потерять исходные эпизоды |

Нужна одна лучшая картинка для оператора, но она не доказывает длительность события. Pre/post clip должен включать момент до подтверждения. Score одной детекции не выдавать за калиброванную вероятность всего нарушения.

### Проверка метода на уровне событий

**PROPOSAL протокола для evaluation:** заранее разметить GT как `(camera, rule semantic, actor GT-id or association, onset, offset, observed/unknown intervals, scene_version)`. Пересечения и длительные состояния оценивать отдельно. Короткий crossing — point-like onset event; tIoU длинного interval к нему не подходит. У GT нет зависимости от ID выбранного tracker.

1. Зафиксировать семантику начала: пересечение границы, первый видимый момент отсутствия СИЗ или истечение разрешённого dwell. Иначе latency сравнивается с разными событиями.
2. Для prediction/GT одинакового класса/камеры/зоны строить допустимые пары по actor association, temporal overlap или onset tolerance. При сложной crowd association сохранять ambiguous subset отдельно, не считать соседнего человека успехом.
3. Выбрать **один-к-одному** matching с заранее определённым критерием (например, максимальный tIoU для interval events, минимальное onset error в collar для crossing). Первое matched prediction — TP; лишние predictions одного GT остаются duplicate FP, ненайденные GT — FN.
4. Пороги tIoU/collar задаются задачей/разметочной точностью и sensitivity analysis, не подбираются на test для красивой цифры. DCASE F20 служит примером явного протокола, его 200ms не являются нашим нормативом.
5. Отдельно измерять event precision/recall/F1, duplicate rate, false alerts per observed camera-hour, first notification latency p50/p95/max, missed short-event duration, active-time fragmentation, unknown fraction и observation availability. Показывать число GT/FP и длительность записи, а не только проценты.
6. Для live latency учитывать capture→inference→confirmation→publication. Offline onset delay от source timestamps сообщать отдельно. События на концах клипа/при signal loss right-censored; не требовать от системы выдуманного offset.

**INF:** denominator FA/hour должен быть явно указан: только доступные наблюдаемые часы и/или полное scheduled время с availability рядом. Тишина из-за отключившейся камеры не есть улучшение качества. При нуле FP на коротком негативном видео нельзя обещать ноль тревог на смену. Гипотетическая Poisson верхняя граница около 3/T при нуле наблюдений требует стационарности/независимости; в нашем отчёте она не используется как доказанная гарантия.

**Результат C10:** typed rule + трёхзначные predicates + отдельный event lifecycle; event matching заранее фиксируется. Полный сервис/UX/доставка сообщений здесь не проектируются.

## E-процедуры для практической волны — не выполнены

### E-B01 — выбрать anchor и гистерезис

**Решение:** bottom center достаточно или нужен pose/иной ракурс. **Входы:** фиксированная камера, размеченный полигон, clips нормального прохода, наклона, шага одной ногой, occluded feet, человека перед станком и crowd; GT ground contact/unknown. **Шаги:** заморозить detections, сравнить bbox intersection, bottom center, ankle any/mean при доступном pose; затем повторить с detector errors. Sweep boundary-band отдельно на calibration subset. **Метрики:** false/missed entry events, distance error до границы, задержка, unknown coverage, FPS/calls. **Доказательства:** overlay contact/полигон/GT, timestamps и predicate trace. **Выбор:** если pose улучшает ошибку только на видимых крупных ногах и добавляет inference, оставить bottom center + unknown для иных кадров. **Предел:** не доказывает 3D касание и геометрию другой камеры.

### E-B02 — метрическая близость к технике

**Решение:** можно ли показывать метры/скорость или только условную image-zone. **Входы:** согласованные реальные размеры и контрольные отметки пола, camera calibration, реальные trajectories людей/техники, независимый эталон distance/time; безопасная съёмка без опасного сближения. **Шаги:** построить homography на train points, измерить held-out errors по near/far/edges, проверить поворот/частичную окклюзию/footprint vs center, отдельно при поднятом рабочем органе; perturb calibration и camera shift. **Метрики:** p50/p95/max ground distance error, threshold-crossing errors, скорость error, доля unknown, missed dangerous-envelope events. **Решение:** metric claim только в валидированной области с запасом относительно ошибки; иначе отступить к image-zone. **Предел:** это оценка наблюдения, не сертификация safe stopping distance или collision prevention.

### E-B03 — трекеры на фактической частоте результатов

**Решение:** ByteTrack/OC-SORT/BoT-SORT и нужен ли ReID. **Входы:** одинаковый cached detection stream с confidence ниже association low threshold, GT actor IDs и events, source timestamps, реальные LinQ inference cadence после доступа. **Шаги:** одинаковые детекции подать трём трекерам; отдельно ReID on/off; варианты cadence полного видео, равномерное 10/5/2 FPS как стресс-режимы, burst loss/jitter с тем же средним; оптимизировать на отдельном subset. Записать versions и кадр/секунды всех max_age/buffers. **Метрики:** IDF1/HOTA или IDS/Frag, event F1, event duplicates, transferred wrong PPE state, latency, neural calls/crops, CPU time. **Решение:** выбрать минимально дорогой вариант, достигающий событийных требований; ReID только при подтверждённом выигрыше. **Предел:** benchmark на cached detections не измеряет end-to-end LinQ, сеть и переносимость ReID.

### E-B04 — автомат подтверждения и loss policy

**Решение:** выбрать confirmation/exit/gap и семантику unknown. **Входы:** annotated positive и long negative videos, boundary jitter, 1-frame false detection, true short intrusion, exit/re-entry, occlusion, ID change, stationary violation, signal loss/reconnect, camera shift. **Шаги:** воспроизвести deterministic predicate traces без inference; отдельно replay видео. Сравнить temporal operators и предлагаемые sweep из C09, сохраняя единую GT; провести Frigate v0.18.2 trace-check `inside,outside,inside` и `inside dwell,exit,re-entry` для верификации F06. **Метрики:** event FP/FN/duplicates, confirmation delay, censor reasons, unknown fraction, physical-time invariance при resampling, стабильность event_id. **Решение:** исключить схемы, которые подтверждают нарушение на stale frames или завершают как observed_exit при loss. **Предел:** логически правильный автомат не исправляет плохой detector или ошибочный hazardous-zone смысл.

### E-B05 — контракт правил и измерений

**Решение:** пригодны ли declarative schema и matcher для данного полного кейса. **Входы:** полный кейс, rule examples, вручную составленный набор нескольких GT/predictions с one event split/merge, wrong actor, overlap двух людей, duplicate messages, point crossing, censored event. **Шаги:** эксперт подписывает семантику, проверить три значения AND/NOT, units/version validation; независимо вручную посчитать matching и сравнить с evaluator. Не тестировать тривиальные getters. **Метрики:** доля неоднозначно размечаемых случаев, divergence evaluator/manual, необнаруженные невалидные правила, FP за wrong actor/duplicate. **Решение:** пока semantics спорная — держать rule disabled/unknown; не маскировать неоднозначность средней accuracy. **Предел:** эти проверки оценивают контракт и метод оценки, не точность CV.

## Вопросы и остаточные неизвестные

| ID | Точный вопрос | Как получить ответ / какое решение меняет |
|---|---|---|
| Q-B01 P0 | Опасная зона — площадь пола, любая часть тела, 3D envelope? Вход сам по себе нарушение или только при активной технике/без допуска? | постановщик/полный кейс; меняет C06/C07 и GT |
| Q-B02 P0 | Есть ли фиксированные камеры, полные стопы, реальные метры/план пола, PTZ/смена ракурса? | видео и calibration артефакты; metric method против image-zone |
| Q-B03 P0 | Какая фактическая частота, jitter и задержка LinQ detections; какие timestamps доступны? | linq_platform/video_architecture + E-B03; tracker cadence/temporal logic |
| Q-B04 P0 | Какие максимальная notification latency и минимальная длительность важного события? | постановщик; confirmation 2sec может быть недопустим |
| Q-B05 P1 | Что делать с нарушением, исчезнувшим за станком: keep active, censored close, merge on return? | operator_product + E-B04; event semantics, не детектор |
| Q-B06 P1 | Кто источник machine active/authorization, каков TTL и outage semantics? | постановщик/интеграционный контракт; отсутствие источника ограничивает wording события |
| Q-B07 P1 | Насколько F06/F07 проявляются в runtime Frigate v0.18.2 при interrupted dwell/stale tracking? | replay trace E-B04, полное caller lifecycle; не объявлять баг до проверки |
| Q-B08 P1 | Есть ли первичный промышленный протокол приёмки, включающий GT matching, отрицательные часы и FA/hour? | вторая волна по закупкам/документы заказчика; численных отраслевых требований пока нет |
| Q-B09 P2 | Можно ли получить ITV RegistryKeys нужной версии целиком и целевые страницы VMDA? | повторный сетевой доступ/артефакт; проверить S19, не использовать snippet defaults |

## Адресная передача

- **W1_A / datasets / training_strategy:** любые СИЗ-атрибуты надо привязать к track segment и visibility, а не хранить вечный boolean на ID. Нужны annotations occluded/unknown, identity-switch hard cases и partial ground-contact.
- **W1_C / linq_platform / model_stack:** ByteTrack/геометрия/правила могут исполняться CPU без дополнительных нейровызовов; optional pose и ReID добавляют сети/кропы. Это методический выбор, не подтверждение LinQ export. Не обещать совместимость FastReID или pose head без SDK.
- **video_architecture:** source PTS, stream availability, inference timestamps/cadence, stale/fresh marker критичны. Не смешивать time of arrival с event time. Scene invalidation и out-of-order outputs меняют доказуемость события.
- **evaluation:** E-B01–B05; match 1:1, actor-aware, point/interval отдельно. IDS важен только вместе с event duplicates/misses/contaminated attributes; FA denominator и availability должны быть видны.
- **operator_product:** текущий/подтверждённый/завершённый/censored event, причина завершения, fullframe + best crop + pretrigger clip, rule/scene versions. Cooldown доставки не должен скрывать новый самостоятельный incident.
- **market_deployment:** нет подтверждённого промышленного procurement acceptance. VMS defaults и качественный IAARC proof-of-concept не превращать в показатели промышленной надёжности.
- **hackathon_strategy:** наиболее защищаемый узкий маршрут — статическая floor ROI на фиксированной камере с видимыми стопами, timestamp confirmation и доказательствами. Динамическая техника/метры/полномочия — расширение только при появлении нужных входов.

## Короткая передача корню

Готовы пять ячеек C06–C10, сохранены 19 source cards (одна недочитанная зацепка), 20 F-ID, 5 E-процедур и 9 Q. Главный выбор: ground-contact zone + простой tracker + timestamp event state с unknown/loss reasons. Главное опровержение: names/defaults VMS не задают универсальную семантику; Frigate v0.18.2 DOC/CODE расхождение вынесено в F06–F07 и E-B04. Три решающих неизвестных — смысл опасной зоны, camera/calibration и реальный cadence LinQ. Материалы: _WORK/W1_B.md и _WORK/SOURCES_B/.
