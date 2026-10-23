# W1-01 — выбор стратегии через baseline и диагностику ошибок

Дата сетевой проверки: 2026-10-23, 03:02–03:04 UTC / 06:02–06:04 Europe/Moscow. Это время исследования, отдельно от расписания хакатона. Входы Context-prompt.md, prompt-training-strategy.md и индивидуальное задание W1-01 прочитаны. Полного кейса, целевых файлов, SDK LinQ и определённого checkpoint нет. Выполнены поиск, открытие первичных материалов и чтение metadata; обучение, установка библиотек и inference не выполнялись.

## Вопрос и решение

Как выбрать следующую работу: оставить готовые веса, исправить данные/обработку/правило, разметить целевой материал или обучать? Рекомендация ветки — сначала получить воспроизводимую baseline в правильной постановке и локализовать ограничение. Наличие GPU не даёт основания сразу начинать большой прогон. Сохранить готовую модель как рабочий кандидат можно, если она проходит заранее заданные требования на независимом целевом материале и реальный путь исполнения на LinQ. Сейчас достаточность ни одной модели не установлена.

Утверждения ниже помечены: **DOC** — первичная документация; **PAPER** — содержание первичной статьи; **CODE** — прочитанный исходник; **LOCAL** — наше действие; **INFERENCE** — рекомендация/вывод этой ветки; **PROPOSED** — будущий эксперимент. Ни один предложенный протокол не является выполненным тестом.

## Источники и извлечённые факты

### W1-01-S01 — TIDE, статья

Daniel Bolya, Sean Foley, James Hays, Judy Hoffman, ECCV 2020. [PDF авторов](https://dbolya.github.io/tide/paper.pdf), [метаданные arXiv v2](https://arxiv.org/abs/2008.08115v2). Первая версия 18.08.2020, v2 31.08.2020; доступ 23.10.2026. Локаторы: §2.1–2.3, Fig.1–2, страницы PDF 4–8. Версию PDF на авторском сайте отдельно не удалось установить; библиографическая версия подтверждена arXiv.

**W1-01-F01 [PAPER].** TIDE разбивает ошибки detection на классификацию, локализацию, их сочетание, дубликаты, фон и пропущенные GT. В основном определении используются foreground IoU 0.5 и background IoU 0.1; это диагностические настройки авторов, не пороги бизнес-событий. Каждый oracle считается относительно исходного результата: ΔAP = AP после условного исправления − исходный AP. Последовательное исправление разных ошибок меняет их кажущийся вклад. Применение требует predictions и GT, не устройства обучения. [S01, §2.1–2.3]

**W1-01-F02 [INFERENCE из F01].** Разложение описывает проявление ошибки, а не причинный диагноз. Пропуск может соответствовать маленькому объекту, occlusion, неверному preprocessing, отсутствующему классу или недостатку обучения. ΔAP oracle нельзя объявлять достижимым выигрышем следующего fine-tuning. TIDE не оценивает, правильно ли человек связан с каской и достаточно ли длительно нарушено правило.

### W1-01-S02 — TIDE, авторская реализация

[Страница авторов](https://dbolya.com/tide/), разделы Installation, Usage; [setup.py на зафиксированном commit](https://github.com/dbolya/tide/blob/49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1/setup.py). Commit HEAD установлен командой `git ls-remote https://github.com/dbolya/tide.git HEAD` при исследовании; это metadata, не запуск TIDE. Дата commit не установлена; доступ 23.10.2026.

**W1-01-F03 [CODE/DOC/LOCAL].** `setup.py` содержит package `tidecv`, version `1.0.1`; HEAD — `49a5d2a4aeb56795e93a3ed7cc7e6d25757bb4c1`. Авторский пример принимает COCO-result файл через `datasets.COCOResult` и вызывает `tide.evaluate(..., mode=TIDE.BOX)`, `summarize`, `plot`. Это возможный путь анализа уже сохранённых predictions; работа с нашим форматом и текущим Python не проверена. Для нестандартных классов нужен корректный адаптер/GT; стандартный пример COCO нельзя молча считать оценкой кейса.

### W1-01-S03 — TorchVision Object Detection Finetuning Tutorial

[Первичная документация PyTorch](https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html). На странице: Created 14.12.2023, Last Updated 05.09.2025, Last Verified 05.11.2024; требование torchvision >=0.16. Снимок страницы прочитан 23.10.2026; точный revision сайта и установленная у команды версия неизвестны. Локаторы: Defining the Dataset; Finetuning from a pretrained model; Testing forward() method; Putting everything together.

**W1-01-F04 [DOC].** Пример переводит COCO-pretrained Faster/Mask R-CNN на пользовательские классы, заменяя predictor. В контракте torchvision boxes имеют XYXY pixel coordinates, `labels` — integer, `0` зарезервирован для background, `image_id` уникален. В tutorial отдельно проверяются forward с targets и inference в `eval()`. Это основание для проверки контракта данных и mode до эксперимента; conventions других детекторов проверяются отдельно. Демонстрационный Penn-Fudan содержит 170 изображений и 345 pedestrian instances; его случайное image-level разбиение не задаёт независимый протокол для соседних CCTV-кадров. Мы не переносим его AP, optimizer recipe или время на команду.

### W1-01-S04 — Identifying Label Errors in Object Detection Datasets by Loss Inspection

Marius Schubert et al. [Полный текст arXiv v3](https://arxiv.org/html/2303.06999v3), [метаданные](https://arxiv.org/abs/2303.06999). Первая версия 13.03.2023, v3 19.12.2023; доступ 23.10.2026. Локаторы: §1 Introduction, §3 Label Error Detection, Supplementary Material / Dataset Dependent Parameters.

**W1-01-F05 [PAPER].** Авторы рассматривают missing labels/drops, class flips, box shifts и background spawns. Их способ ранжирования использует classification и regression losses обеих стадий двухстадийного detector; высокий score или uncertainty не эквивалентны проверенной ошибке label. Исследование включает симулированные и реальные ошибки. Здесь не переносим численный precision из abstract, поскольку его полный режим и база для нашего кейса не сопоставлены. Практическое следствие: спорное FP сначала проверять человеком против annotation policy; автоматическое несовпадение model/GT не выбирает, кто прав. Метод loss inspection не является установленной функцией выбранного YOLO trainer.

### W1-01-S05 — Ultralytics Model Validation

[Официальная документация](https://docs.ultralytics.com/modes/val). Дата публикации/revision не указана; доступ 23.10.2026. Страница описывает текущие YOLO26 и preview YOLO27, не фиксирует package release/commit. Поэтому это документационное предупреждение, не обещание наличия параметров в установленной команде версии. Локаторы: Usage Examples, Arguments for YOLO Model Validation, Rectangular Validation, Per-Image Precision Recall and F1.

**W1-01-F06 [DOC].** Документация предупреждает: official weights без явного `data` могут использовать fallback task dataset `coco8.yaml`. Настройки confidence и NMS IoU влияют на итог; validation geometry может отличаться от predict/fixed export, в том числе из-за rectangular padding. В текущем тексте есть сохранение predictions JSON и per-image TP/FP/FN. Проверять конкретные API и defaults нужно на зафиксированном release. Следствие для baseline: явно фиксировать dataset, split, геометрию и postprocessing, а не полагаться на автоматическое восстановление settings.

### Недоступный первичный след

Missing Labels in Object Detection, Xu/Bai/Ghanem, CVPRW 2019: PDF `https://openaccess.thecvf.com/content_CVPRW_2019/papers/Weakly%20Supervised%20Learning%20for%20Real-World%20Computer%20Vision%20Applications/Xu_Missing_Labels_in_Object_Detection_CVPRW_2019_paper.pdf` и HTML по тому же названию вернули web-tool HTTP 403 Forbidden. Поиск видел документ, но он не считается прочитанным. Независимый первичный путь для текущего решения — открытый полный текст S04; выводы и числа недоступной статьи не используются. Дальнейший поиск её exact recipe не меняет решение W1-01 и передаётся ветке partial labels при необходимости.

## Диагностический минимум — наша предлагаемая процедура, а не универсальный benchmark

**W1-01-F07 [INFERENCE из F01/F04/F05/F06 и исходной постановки].** Baseline — это комплект из checkpoint и неизменяемого контракта наблюдения, а не только один mAP. До выбора обучения нужно собрать следующие сведения:

1. **Что считается успехом.** Развести object classes, наблюдаемые состояния и violation events. Уточнить неоднозначное: «helmet присутствует» против «helmet надет данным человеком»; «нет видимого респиратора» против «нарушено обязательное правило ношения». Не вводить эти классы как уже заданные организаторами.
2. **Что видно.** Посмотреть исходный кадр и фактический input после resize/padding/crop; записать размер нужного объекта в пикселях на обоих этапах, размытие, перекрытия и доступность временного контекста. Ручная неразличимость — сигнал ограничения наблюдения, а не математическое доказательство невозможности для любой модели. Если различимость появляется только в исходнике, проверять input geometry раньше большого обучения; если требуется контекст вне изображения, уточнять постановку/камеру.
3. **Что загружено.** Хеши weights/config; class names и mapping; размер/цветовой порядок/нормализацию; формат boxes; inverse transforms; actual runtime; режим eval; confidence, NMS и max detections. Визуализировать GT и predictions на реальном входе после transforms. Неверное отображение labels/coordinates сначала исправляется как ошибка pipeline.
4. **На чём сравнивается.** Разделить рабочий материал для диагностики/доразметки/настройки и независимую оценку, сохранив camera/session/time provenance. Не разбивать соседние frames одной траектории случайно между train и validation. Разные часы одной камеры и новая камера отвечают на разные вопросы; оценка внутри камеры не доказывает перенос на новую.
5. **Какая ошибка повторяется.** Таблица объектов: class, TP/FP/FN, категория TIDE/ручного разбора, размер, камера, условия видимости, GT audit status. Таблица событий: event ID, interval, person/track, требуемый object evidence, правило, тревога, причина спорного решения. Число errors сопровождать denominators и покрытием; выборка только ошибок непригодна для оценки распространённости.
6. **Можно ли воспроизвести.** Сохранить сырые predictions до event logic, промежуточные связи/траектории, overlays, выбранные timestamps и решения аннотатора. Иначе изменение правила легко принять за улучшение detector.

Не задаём заранее число кадров: оно должно обеспечить представительство камер, условий, позитивов и негативов, которое допускают фактические данные и время ручной работы. Если редкое событие не встретилось, это отсутствие свидетельства о качестве, а не «нулевые ошибки».

## Матрица ситуация → наблюдение → интервенция → проверка

Все строки — условные рекомендации **INFERENCE/PROPOSED**, не подтверждённые на целевых данных.

| Ситуация | Нужное наблюдение | Следующая интервенция | Проверка и предел |
|---|---|---|---|
| Только открытые данные и готовые веса | Есть ли нужный class/output contract; сходны ли ракурс и масштаб | Сохранить zero-update reference; проверить pipeline; запросить/разметить target audit | Open-source validation характеризует source; достаточность на target пока неизвестна |
| Есть немного target labels | Они полны для нужных классов? Независимы ли сцены? Какие ошибки повторяются? | Сначала audit mapping/coverage, затем небольшой controlled fine-tuning против unchanged baseline | Одинаковые target validation, preprocessing, rules; новый camera split при доступности |
| Есть только target video без labels | Есть ли разрешение на его adaptation; какие условия и события представлены | Выделить непересекающиеся adaptation/assessment группы; разметить диагностическую порцию | Без проверенного GT нельзя измерить target AP/recall или доказать пользу pseudo-labels |
| Labels неоднородны, много «FP» | Человек подтверждает missing annotation или иное правило labeling | Исправить policy и спорную разметку; сохранить версии до/после | Не штрафовать модель за незамеченные GT; оценивать обе модели на одинаковом исправленном наборе |
| Boxes/classes верны, тревога ошибочна | Связь person/PPE, зона, длительность, track ID или дедупликация неверны | Исправить соответствующее event/association rule | E02 с вручную проверенным evidence; не требовать нового detector training по умолчанию |
| Объект пропадает после resize | В исходнике различим, на actual input теряет признаки | Контролируемое разрешение/crop experiment, затем при необходимости обучение под тот input | Сравнить object/event quality и число inference calls; LinQ feasibility отдельно |
| Веса не содержат новый класс | Class map действительно не кодирует нужный смысл | Найти подходящие веса или подготовить полную разметку и изменить predictor/training | Confidence threshold не создаёт отсутствующий класс; экспорт изменённого graph вновь проверяется |
| Частый фон путается с классом | FP повторяются на независимых проверенных негативных сценах | Целевая доразметка hard negatives либо focused data change | Проверить, не потерян ли recall редких позитивов; не набирать лишь соседние повторения |
| Ошибки одной камеры/смены | Согласованные labels, та же pipeline, отличия видимости/домена | Представительные target examples; ограниченное supervised adaptation как кандидат | Сохранить оценку других камер и базовых классов; улучшение одной не гарантирует общего |
| Неясен визуальный сигнал | Спор сохраняется при исходном кадре и времени, человеческие решения расходятся | Уточнить определение события, abstention/unknown или нужный обзор камеры | Не объявлять отсутствие видимого объекта доказанным отсутствием объекта |
| Готовые веса проходят требования | Пройден независимый target protocol и интеграционный путь | Сохранить рабочий кандидат; следующий прогон только под конкретную оставшуюся ошибку | Приёмка включает target runtime и event failures; это не пожизненная гарантия |
| FP-модель хороша, после export хуже | Разница воспроизводится на тех же input/predictions | Проверить geometry/numerics/output parsing, затем компрессию | Переобучение до локализации export loss может исправлять неверную причину |

## E-процедуры для практической волны

### W1-01-E01 — воспроизводимая zero-update baseline и выбор первой интервенции

**Решение:** можно ли оставить готовые веса; нужен ли data/pipeline fix или training. **Входы:** утверждённая task ontology; лицензированные target images/video и возможность ручного GT; пригодный checkpoint/config от model_stack; фактическое окружение. **Контроль:** weights неизменны; единый evaluation contract, отдельные diagnostic и assessment группы; зафиксированные правила и preprocessing.

**Действия:** (1) Записать manifest, проверить class map и несколько overlays actual model input. (2) Запустить исходные веса в reference runtime, сохранить raw detections и output contract. (3) Сопоставить с проверенной разметкой и разобрать проявления F01, а также связь с масштабом/видимостью. (4) Проверить спорные GT; исправлять данные только версионно. (5) Выполнить события с неизменными правилами. (6) Выбрать одно вмешательство, затрагивающее преобладающую подтверждённую причину; обучение — один из вариантов.

**Метрики:** object AP с явно названным IoU protocol, per-class precision/recall на зафиксированной operating point, TP/FP/FN и denominators по группам; отдельно event recall/false alarms и длительность наблюдения по протоколу evaluation. При отсутствии GT доступны лишь overlays, покрытие и гипотезы; численное target quality не заявляется.

**Артефакты:** dataset/split manifest с camera/session/time и label version, checkpoint hash, code/package version, полный config, raw predictions, actual input overlays, audit corrections с причинами, error table, event log, runtime identity. Не сохранять персональные данные в публичные отчёты без оснований и доступа.

**Исходы:** pipeline invalid → сначала fix и новая reference; labels invalid → audit и единый исправленный evaluation set; objects достаточны/events нет → E02; систематические object errors при видимом сигнале → targeted data + controlled training comparison; сигнал не установлен → E03. **Stop rule:** не начинать большой training при неверной таксономии, невалидных координатах или невозможности оценить target результат. Приёмка готовых весов — только по заранее заданным требованиям и реальному LinQ execution. **Предел:** reference CPU/RTX не подтверждает LinQ, diagnostic sample не доказывает перенос на все камеры.

### W1-01-E02 — локализация object против event ошибки

**Решение:** тратить усилия на detector training или на association/temporal logic. **Входы:** короткие диагностические clips с проверенным event GT, object evidence и идентичностями, требуемыми конкретным правилом; воспроизводимый rule engine. **Контроль:** один clip set, same timestamps/rules/zones; меняется только входная информация соответствующего этапа.

**Действия:** A — обычные detections → associations/tracks → events. B — вручную проверенные object boxes/classes на тех же кадрах → те же associations/tracks → events. Если B всё ещё ошибочен, C — проверенные associations/identity/zone evidence → те же temporal rules. Это ручная oracle-подстановка для диагностики, не заявка на production performance. Если интерфейс не позволяет такую подстановку, зафиксировать необходимые stage logs и выполнить структурированный ручной разбор; не заявлять выполненный B/C.

**Метрики:** paired перечень изменившихся event TP/FP/FN, event timing и причина каждого исправления/остатка. **Артефакты:** versions A/B/C evidence, rules, audit decisions, traces, overlays, timestamps. **Исходы:** A→B исправляет ошибки — object stage участвует, но конкретный способ обучения ещё неизвестен; B→C исправляет — association/track issue; C сохраняет ошибку — правило, постановка или event GT требуют проверки. **Stop rule:** если reference labels/identity спорны, прекратить причинную атрибуцию до согласования; не обучать detector ради ошибки, сохраняющейся при правильном object evidence. **Предел:** идеальные objects не гарантируют, что практический detector достижим; oracle не прогнозирует выигрыш AP или event quality.

### W1-01-E03 — тест наблюдаемости и потери сигнала при обработке

**Решение:** менять input/camera/context либо пробовать data/training. **Входы:** diagnostic positives/negatives, native frame и actual input representation, разрешение просматривать короткий temporal context, согласованная инструкция labeling. **Контроль:** один и тот же физический эпизод; фиксировать, какую информацию видел reviewer.

**Действия:** независимые reviewers при возможности помечают состояние и `unknown` на native frame, actual transformed input и разрешённом clip context. После первоначальных независимых решений обсуждают расхождения; записывают причины, размер объекта и occlusion. Не показывать model label до первичного решения. Это скрининг, не измерение Bayes error.

**Метрики:** counts согласий/расхождений/unknown по representation и условиям; object size distribution; дополнительно paired model results только после actual inference test. **Артефакты:** manifests views, audit form, instructions, disagreement log. **Исходы:** native различим/actual нет → input-scale branch; single frame нет/clip да → temporal context branch; даже clip спорен → task/camera/GT question. **Stop rule:** не расширять training только ради неустановимого target label; уточнить требуемое наблюдение. **Предел:** human disagreement не доказывает абсолютную невозможность model inference, agreement не доказывает достижимую точность. LinQ cost input/crops остаётся отдельным вопросом.

## Открытые вопросы

| ID | Неизвестное и решение | Как закрыть |
|---|---|---|
| W1-01-Q01 | Точная ontology/events, обязательные metrics и разрешённый context; без них нельзя принять baseline | Полный кейс/ответ постановщика; приоритет высокий |
| W1-01-Q02 | Есть ли target video, camera/session metadata, labels и annotation policy; разрешено ли adaptation на нём | Получить артефакты и проверить provenance вместе с datasets/evaluation; высокий |
| W1-01-Q03 | Исходный checkpoint, class coverage, package release, preprocess/output contracts | model_stack даёт hash/config и небольшой reference test; высокий |
| W1-01-Q04 | Реальное LinQ input shape, preprocessing, export/runtime и evidence выполнения | linq_platform; версия SDK и actual artifact, высокий |
| W1-01-Q05 | Доступна ли stage-level подстановка объектов/связей в event rules | violation_methods/video_architecture; если нет — минимальный trace contract, средний |
| W1-01-Q06 | Какие требования достаточности и допустимые пропуски/тревоги установлены для редких событий | Кейсовые критерии и evaluation; без них нет честного stop/acceptance threshold |

## Адресные передачи

- **→ model_stack:** F04/F06: проверить contract loader и predictor, явный dataset argument, actual validation geometry, возможность сохранять raw pre-event predictions. Сначала нужен один воспроизводимый unchanged checkpoint, затем training modes соседних веток.
- **→ datasets:** F05/E01: перепроверить FP против GT, согласовать missing/unknown/negative annotation policy, сохранить camera/session provenance. Не считать неразмеченное отсутствие отрицательным label автоматически.
- **→ evaluation:** E01/E02: нужны separate object/event contracts, denominators и групповые split; training comparison не должен одновременно менять confidence/NMS/geometry/rules. При редком событии отсутствие примеров не превращается в acceptance.
- **→ violation_methods:** E02: ошибка ношения СИЗ, зоны или длительности может сохраняться при идеальных object boxes; нужна проверяемая stage boundary, не универсальное требование дообучать.
- **→ linq_platform / video_architecture:** F06/E03: тот же actual input и output parsing должны быть сопоставлены с reference; рост resolution/crops меняет число вызовов и graph contract. Поддержка/скорость LinQ этой веткой не установлены.
- **→ operator_product / hackathon_strategy:** E03/Q06: в демонстрации отдельно обозначать `unknown` из-за невидимости и model miss; обещать пригодность только в проверенных условиях. Сохранить рабочую reference, пока новая версия не получила проверяемое преимущество.

## Остаточные ограничения ветки

Публичные источники подтверждают инструменты диагностики и конкретные опасности несопоставимого протокола; они не задают, сколько target labels достаточно для нашего кейса, какие weights победят и стоит ли менять learning rate. Для этого нужны целевые данные и E01–E03. Текущее содержательное завершение — матрица решений, stage-level диагностика и фиксированный контракт baseline. Каталог всех методов и точные fine-tuning recipes находятся за границей W1-01 и передаются другим веткам.
