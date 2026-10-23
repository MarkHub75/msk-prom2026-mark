# SOURCES — violation_methods

Дата сетевых обращений и инспекции источников: **2026-10-23, Europe/Moscow (+03:00)**; интервалы волн около05:59–06:26. Это дата доступа, отдельно от публикаций/revisions. Сборка:2026-10-23 06:28 MSK; новой сети, моделей, VMS runtime, обучения и benchmark в сборке нет. Прочитаны сохранённые материалы обеих волн. Все E — предложения, **ни один E не выполнен**. Локальные metadata/XML/JSON/изображения читались в исследовательских волнах; это не запуск модели.

Легенда: **DOC** первичная документация/раскрытие метода; **CODE** исходный код прочитан, не выполнен; **PUB-MEAS** опубликованное измерение автора; **VENDOR** заявление заинтересованной стороны, включая abstract-only report; **LOCAL-OBS** инспекция сохранённого артефакта/визуальное наблюдение; **INF** наш вывод из указанных оснований; **PROP** предложение для проверки; **UNK** точное неизвестное/статус доступа. Тип основания и фактический статус проверки различаются. Чужой эксперимент не наш тест; требование не достижение. Источники одной цепочки не независимые репликации.

Реестр объединяет обе реальные волны. В каждой карточке сохранены автор, прямые URL, публикация/revision (либо явно неизвестно), прочитанный локатор, доступ/ограничения и поддерживаемые факты. Выписки — собственный пересказ исследователей. Дополнительная metadata и все ограничения в карточке относятся ко всем перечисленным F, если не указано иначе. Числа не превращаются в рекомендации проекта.

Одна карточка Macroscop PPE объединяет A/C. Статья и поставка SH17 связаны, но проверка двух файлов не полная инспекция. HDS abstract заменён полным W2 чтением в той же цепочке. Frigate docs/code разных модулей имеют отдельные локаторы, но одно происхождение. AWS pages, Axis pages, R2PPE paper/artifact также связаны и не являются независимыми испытаниями. Точные old→new связи: [_WORK/ID_MAP.md](_WORK/ID_MAP.md).

<a id="s001"></a>
## S001 — SHWD

**Поддерживаемые F:** [F001](RAW_FACTS.md#f001). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S01; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Автор: njvisionpower, Safety-Helmet-Wearing-Dataset.
- URL README: https://raw.githubusercontent.com/njvisionpower/Safety-Helmet-Wearing-Dataset/c952631dfc352e0defdd54b4785a9be6576451ad/README.md
- URL прочитанного кода: https://raw.githubusercontent.com/njvisionpower/Safety-Helmet-Wearing-Dataset/c952631dfc352e0defdd54b4785a9be6576451ad/train_yolo.py
- Версия: c952631dfc352e0defdd54b4785a9be6576451ad, committer date 2019-12-17T12:39:49Z. Дата создания датасета не установлена по этим файлам.
- Локатор: README Introduction, How to use dataset; train_yolo.py строки 25–27, 103–107.
- [F001](RAW_FACTS.md#f001), primary doc + code inspection: 7,581 изображение; 9,044 положительных helmet wearing objects; 111,514 отрицательных normal head objects. Названия классов: hat и person. Здесь person обозначает отрицательный объект головы без каски, не полноразмерную рамку тела. Код подтверждает ровно два class literals. Метрика в скрипте VOC07 mAP при IoU .5.
- Ограничение: изображения/аннотации из архива не скачивались и не инспектировались; README-семантика не доказывает отсутствие ошибок каждой аннотации.
- Смысл: запретить автоматический merge person из SHWD с person COCO/SH17 без явного преобразования геометрии и семантики.

<a id="s002"></a>
## S002 — CHV

**Поддерживаемые F:** [F002](RAW_FACTS.md#f002). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S02; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Zijian Wang, Yimin Wu, Lichao Yang, Arjun Thirunavukarasu, Colin Evison, Yifan Zhao.
- URL: https://raw.githubusercontent.com/ZijianWang-ZW/PPE_detection/907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d/README.md
- Связанная статья: Fast Personal Protective Equipment Detection for Real Construction Sites Using Deep Learning Approaches, Sensors 21(10),3478,2021, https://doi.org/10.3390/s21103478 (полный текст не получен, 429).
- Версия repo: 907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d, committer 2022-11-03T08:35:47Z.
- Локатор: Introduction, CHV Dataset, Results.
- [F002](RAW_FACTS.md#f002), primary artifact: CHV распознаёт person, vest и четыре цвета helmet. Это отдельные предметы, а не четыре состояния одетого человека. Авторы отобрали 1,330 качественных изображений из более 10,000. README сообщает лучший mAP86.55% для YOLOv5x и 52FPS для v5s на TeslaP40/24GB, CPU4cores/8GB.
- Ограничение: README не даёт достаточной методики для межстатейного ранжирования. Нельзя переносить FPS на LinQ. Отбор качественных кадров ограничивает оценку плохого промышленного видео.

<a id="s003"></a>
## S003 — Pictor-PPE

**Поддерживаемые F:** [F003](RAW_FACTS.md#f003), [F004](RAW_FACTS.md#f004). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S03; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы метода: Nipun D. Nath, Amir H. Behzadan, Stephanie G. Paal. Статья Automation in Construction112,103085,2020; владелец repo ciber-lab.
- URL: https://raw.githubusercontent.com/ciber-lab/pictor-ppe/8f41c9525bbd1f45245f593c7502a1934eef06fa/README.md
- Код: https://raw.githubusercontent.com/ciber-lab/pictor-ppe/8f41c9525bbd1f45245f593c7502a1934eef06fa/src/yolo3/detect.py
- Версия: 8f41c9525bbd1f45245f593c7502a1934eef06fa, committer 2024-12-18T19:37:18Z.
- Локатор: README Methods/Approaches, Results; detect.py function detection.
- [F003](RAW_FACTS.md#f003), primary artifact: A1 детектирует worker/hat/vest и классифицирует отношения; A2 прямо детектирует W/WH/WV/WHV; A3 детектирует worker и классифицирует его crop VGG16/ResNet50/Xception. W означает neither hat nor vest, WH только каска, WV только жилет, WHV оба. Авторы README называют лучшим A2 с72.3%mAP.
- [F004](RAW_FACTS.md#f004), code inspection: detect.py — декодирование YOLO и NMS, возвращает рамки/score/class; в этом файле нет доказательства связи PPE–worker. Чтение этого файла не равно проверке полного A1 decision tree.
- Ограничение: полный оригинальный paper и downstream notebooks в этой ветке не прочитаны; нельзя восстановить из README все режимы разметки unknown. Ограничения разметки Pictor критикует [S005](SOURCES.md#s005), это отдельное авторское наблюдение.

<a id="s004"></a>
## S004 — SH17

**Поддерживаемые F:** [F005](RAW_FACTS.md#f005), [F006](RAW_FACTS.md#f006), [F007](RAW_FACTS.md#f007). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S04; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Hafiz Mughees Ahmad, Afshin Rahimi, University of Windsor.
- URL статьи: https://arxiv.org/html/2407.04590v1 ; версияv1, 2024-07-05.
- YAML: https://raw.githubusercontent.com/ahmadmughees/SH17dataset/2f832c289f9deea063367045ed8230b26e3e7ea9/sh17.yaml
- Repo revision: 2f832c289f9deea063367045ed8230b26e3e7ea9, committer 2024-12-04T15:29:53Z.
- Локаторы прочитаны: III-B/C TableII, IV TablesIII–V, Appendix train/test; YAML names.
- [F005](RAW_FACTS.md#f005), primary doc: head допускает любой вид головы; face размечается при видимом носе. Face-mask-medical — медицинская маска, не общий industrial respirator. Предусмотрены расширенные on/off tags; off означает предмет в сцене, но не надет. Glasses имеют safety/vision; earmuffs включают обычные over-ear headphones. YAML17 базовых labels не кодирует tags, называется face-mask и содержит отдельные person/head/face/hands/gloves/helmet.
- [F006](RAW_FACTS.md#f006), published measurement: YOLOv9-e на SH17 test: helmet recall67.8%,gloves58.9%,face-mask73.2%. На Pictor mapping трёх классов TableV: helmet recall23.7%,AP50=55.5%; vest всего28instances. IV-A текст all mAP58.8, таблица58.9. Это frame/object metrics, не события.
- Ограничение: on/off presence в статье не доказывает доступность tags в используемом YOLO export; архив не изучен. Лицензии не исследовались. Статья сама не устанавливает пригодность к камерам кейса.

Дополнение/история чтения той же цепочки (W2-A-S02); не независимый эксперимент:

Ahmad/Rahimi, Journal of Safety Science and Resilience,2024; [DOI](https://doi.org/10.1016/j.jnlssr.2024.09.002), §3.3 Table2/Note; текст открыт через издателя/индекс. [YAML master](https://raw.githubusercontent.com/ahmadmughees/SH17dataset/2f832c289f9deea063367045ed8230b26e3e7ea9/sh17.yaml) прочитан и сохранён `sh17.yaml`; [Kaggle branch YAML](https://raw.githubusercontent.com/ahmadmughees/SH17dataset/c8bcd13b3f1b9ef42f856f4ec5d194d29df25ed0/sh17_kaggle.yaml) сохранён `sh17_kaggle.yaml`.

**[F007](RAW_FACTS.md#f007) [primary documentation].** Статья утверждает extended tags on/off у нескольких СИЗ, включая medical mask. Off означает предмет в сцене вне ношения. Отдельного wearer ID Table2 не описывает. Medical mask не заявлен промышленной cartridge полумаской. Порядок17 категорий Table2 не равен YOLO indices: фактические `helmet=10`, `hands=11`, `head=12`, `face-mask=5`. Проверенные VOC/TXT согласуются с YAML, а не с порядком таблицы.

Предел: статья о выпуске tags и реально прочитанные примеры базового экспорта — разные основания; ни одно не является industrial off-face benchmark.

<a id="s005"></a>
## S005 — head keypoint vs boxes/direct person state

**Поддерживаемые F:** [F008](RAW_FACTS.md#f008), [F009](RAW_FACTS.md#f009), [F010](RAW_FACTS.md#f010). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S05; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Bartosz Wójcik, Mateusz Żarski, Kamil Książek, Jarosław Adam Miszczak, Mirosław Jan Skibniewski.
- URL: https://arxiv.org/html/2106.10944v1 ; v1,2021-06-21.
- Реально прочитано: §3.1 Algorithm1, §3.2 dataset, §4.3, §5 Tables7/9, §6 Fig9.
- [F008](RAW_FACTS.md#f008), primary method: person без найденной head keypoint остаётся неопределённым person; при head keypoint проверяется попадание в helmet bbox. Авторы отмечают Pictor-v3, где видимый только ниже пояса человек размечен non-wearer. Это критика авторов, не наш аудит Pictor.
- [F009](RAW_FACTS.md#f009), published comparison: dataset7,035, train5,269/test1,766, X101 detector. Table7 AP keypoint=.675, same-detector refitDT=.664, NathDT=.654; APsmall=.211/.222/.222. Table9 keypoint vs same-training FasterRCNN direct wearer/nonwearer: AP=.675/.663, AP50 обе.826, APsmall=.211/.248. Преимущество ограничено метрикой/масштабом.
- [F010](RAW_FACTS.md#f010), primary failure evidence: Fig9 — missing helmet, occluded person+helmet, ошибочная keypoint, small scale, partial-person missing keypoint. §6 предостерегает от гражданских negative examples, ведущих к shortcut worker/civilian.
- Ограничение: статья не опубликованный отдельный benchmark crowded ownership; правило не исключает две головы в одной bbox каски. Вv1 GitHub указан placeholder, код не проверен.

<a id="s006"></a>
## S006 — modular pose/crop PPE

**Поддерживаемые F:** [F011](RAW_FACTS.md#f011), [F012](RAW_FACTS.md#f012). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S06; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Selcuk Anil Karatopak, Deniz Sen, Huawei Türkiye R&D Center.
- URL: https://www.eleco.org.tr/ELECO2023/eleco2023-papers/97.pdf ; ELECO2023, точная дата PDF не указана.
- Локатор: pp2–4 §3.2–3.6, Fig1, Table1; прочитаны эти разделы и setup.
- [F011](RAW_FACTS.md#f011), primary method: YOLOv7 pose даёт17keypoints; отдельные crops/CNN для PPE. Для gloves требуются elbow/wrist confidence; руки позади torso отбрасываются. Для glasses back-facing crops не идут в classifier. Fig1 имеет wearing/not-wearing/indecisive. Glove classifier имеет glove/no-glove/undefined.
- [F012](RAW_FACTS.md#f012), published measurement: закрытые CCTV данные; split glove90/10, hardhat/vest80/20. Table1 crop-classifier test accuracy hardhat.92/vest.98/glove.86/eyeglass.95; это не end-to-end event recall. Coverage там геометрическая величина, не selective prediction coverage. В формуле/пояснении denominator и толкование вызывают неоднозначность: не переносить его без проверки.
- Ограничение: нет публичных данных для независимой проверки; ошибки crop/pose не сведены в событийную метрику. Порогов видимости как универсальных нет.

<a id="s007"></a>
## S007 — коммерческий интерфейс трёх состояний

**Поддерживаемые F:** [F013](RAW_FACTS.md#f013). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S07; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Автор: Amazon Web Services, Rekognition Developer Guide, latest/unpinned, дата публикации не указана.
- URL: https://docs.aws.amazon.com/rekognition/latest/dg/ppe-request-response.html
- Локатор: Understanding the DetectProtectiveEquipment response, BodyParts, CoversBodyPart, Summary; прочитаны.
- [F013](RAW_FACTS.md#f013), primary doc: отдельно confidence person, bodypart, item, coverage. CoversBodyPart отсекает предмет рядом, но не доказывает защиту или корректное ношение. Summary разделяет PersonsWithRequiredEquipment, PersonsWithoutRequiredEquipment, PersonsIndeterminate. Последнее включает недостаточную confidence person/bodypart/equipment/coverage относительно MinConfidence. Требование80% в примере — пример API, не рекомендованный промышленный operating point. Документ рекомендует лицо к камере.
- Ограничение: API не запускалось; механизм модели не раскрыт, независимое качество не установлено. Логическая структура пригодна как образец схемы, применение AWS в кейсе не предлагается.

<a id="s008"></a>
## S008 — гранулярность PPE API

**Поддерживаемые F:** [F014](RAW_FACTS.md#f014). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S08; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Автор: AWS, latest/unpinned; дата публикации неизвестна.
- URL: https://docs.aws.amazon.com/rekognition/latest/dg/ppe-detection.html
- Локатор: Types of PPE, Summarizing, Notes; прочитан весь основной текст.
- [F014](RAW_FACTS.md#f014), primary doc: face cover включает cloth/surgical/N95, но API не возвращает конкретный subtype покрытия. PPE IDs генерируются per-image и не сохраняются между кадрами. Confidence50–100 — шкала сервиса.
- Ограничение/смысл: generic face cover не равен соответствующему респиратору; выдачу per-frame нельзя считать треком сотрудника. Нельзя выдавать score за откалиброванную вероятность события.

<a id="s009"></a>
## S009 — selective classification

**Поддерживаемые F:** [F015](RAW_FACTS.md#f015). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S09; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Yonatan Geifman, Ran El-Yaniv.
- URL: https://arxiv.org/html/1705.08500v2 ; v2,2017-06-01.
- Локатор: §§2–3 problem setting/risk, §§4–5 confidence/experiments; прочитаны постановка, допущения, summary экспериментов.
- [F015](RAW_FACTS.md#f015), original theoretical method: selection g позволяет отказаться; coverage — доля принятых, risk — ошибка на принятых. Статистическая гарантия строится на i.i.d. выборке из того же распределения P. Softmax response/MC-dropout сравниваются на CIFAR/ImageNet, не PPE видео.
- Ограничение/смысл: основание для risk–coverage отчёта и калибровочной выборки. Гарантия не переносится автоматически на соседние кадры, другую камеру/цех или отобранные лучшие кадры. Выбор max confidence сам по себе не верифицированная политика abstention.

<a id="s010"></a>
## S010 — manufacturer respirator instructions

**Поддерживаемые F:** [F016](RAW_FACTS.md#f016). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S10; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Автор: 3M, Half Facepiece Respirator6000 Series User Instructions.
- URL: https://multimedia.3m.com/mws/media/96751O/3m-6000-series-half-facepiece-respirator-user-instructions.pdf
- Версия/дата: revision/date в прочитанных разделах не найдены; документ61PDFстраница, датировка поискового индекса не принимается за дату документа.
- Локатор: English printed pp9–11/PDF indices8–10 Fitting Instructions, Donning, User Seal Checks, Fit Testing; Use limitations p3.
- [F016](RAW_FACTS.md#f016), primary manual: надевание закрывает рот/нос, регулируются верхние/нижние straps. При каждом надевании выполняется pressure seal check, до выдачи требуется fit testing. Проверка включает ощущения утечки/деформации при вдохе/выдохе; совместимые PPE также участвуют в fit test. Пригодность filter/cartridge зависит от загрязнителя и условий.
- Ограничение: инструкция конкретного семейства, US/Canada/Brazil references; не российская юридическая квалификация. Из обычного CCTV RGB нельзя подтвердить утечки, соответствие фильтра, service life или успешный fit test.

<a id="s011"></a>
## S011 — Macroscop4.7, ограничения и определения

**Поддерживаемые F:** [F017](RAW_FACTS.md#f017), [F018](RAW_FACTS.md#f018). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S11; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Автор: Macroscop. URL: https://doc.macroscop.com/analytics/hard-hats/requirements.htm
- Версия4.7; footer Last updated22.10.2026, не утверждается дата первого выпуска.
- Прочитаны: Детектирование (Каска, Жилет, Респиратор, Очки, Перчатки), Размеры объекта, сцена/ракурс.
- [F017](RAW_FACTS.md#f017), primary vendor doc: респиратор должен закрывать нижнее/всё лицо, medical masks исключены. Невидимое лицо => наличие/отсутствие respirator/glasses не определяется. Очки на уровне глаз, не лба; поддерживается цветная оправа/полностью цветные очки. Жилет определяется как любая надетая одежда без рукавов, любого цвета.
- [F018](RAW_FACTS.md#f018), primary vendor conditions: head>=60×60px для respirator/glasses/shield/earmuffs; hands>=40×40px gloves; vest>=60×60px; person>=80pxheight и>=2%width/8%height кадра. Gloves: видимые кисти, без посторонних предметов/кармана,>=10сек в кадре; одна видимая перчатка может дать presence, но две видимые руки с одной голой=>absence. Camera downward<=35°, лицо к камере<=60° для facePPE.
- Ограничение: конкретная модель/версия, не универсальные пределы. Наличие glove на одной видимой руке не доказывает обе перчатки. Значение vest не совпадает с certified/high-vis. Не измерялось нами.

Дополнение/история чтения той же цепочки (C-S02); не независимый эксперимент:

Автор: Macroscop. https://doc.macroscop.com/analytics/hard-hats/requirements.htm . Открыта документация **4.7**, внизу Last updated **22.10.2026**. Первоначальный cached web-result и поздний live-result могут иметь разную навигацию; для фактов использован прочитанный body 4.7. Локаторы: «Видеопоток», «Сцена и расположение камеры», «Респиратор», «Очки», «Размеры объекта».

**[F018](RAW_FACTS.md#f018) [primary doc]:** нейросетевые режимы >=3 FPS, HD 1280×720; увеличение выше HD не увеличивает количество/мелкость распознаваемых объектов. Цветное изображение, без существенных compression artifacts; наклон от горизонтали <=35°, угол лица к камере для respirator/glasses/shield <=60°. Для малых лицевых PPE голова >=60×60 px, кисть для перчатки >=40×40; человек >=80 px и >=2% ширины/8% высоты кадра. При невидимом лице presence/absence respirator/glasses **не определяется**. Медицинская маска не относится к респиратору. Эти условия продукта не являются границей информации для любого детектора. Ту же цепочку независимо читал W1_A; не считать вторым независимым источником.

<a id="s012"></a>
## S012 — реальный steel plant и отказы

**Поддерживаемые F:** [F019](RAW_FACTS.md#f019), [F020](RAW_FACTS.md#f020). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S12; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Kyle Toth, Monika Singhal, Dhwanil Chauhan, Jay Polra, Chenn Zhou, Garrett Page, Conrad Fisher.
- URL: https://link.springer.com/article/10.1007/s40192-026-00461-6
- Название: A Dual-Model Approach to Industrial Safety: Computer Vision for PPE Compliance and Hazard-Zone Monitoring in Steel Production; опубликовано12.05.2026.
- Прочитаны Methodology/Data/ModelIntegration/Testing, Results и Limitations.
- [F019](RAW_FACTS.md#f019), primary deployment study: personYOLOv8m→workerROI→PPEYOLOv8m, четыре PPE, steel footage SteelDynamics/CharterSteel. Неоднозначные экземпляры исключались при разметке. §SystemLimitations: gloves полностью не идентифицированы более чем в20% low-light frames; no temporal history/no worker tracking, framewise inconsistencies дают ложные non-compliance. Published F1.93PPE не устраняет этот отказ. Детальные operational metrics confidential.
- [F020](RAW_FACTS.md#f020), published illustrative comparison: §Results сравнение single/multi-stage авторы называют иллюстративным, не standalone benchmark. Personbbox contains all PPE используется как compliance logic; это не доказательство bodypart ownership.
- Ограничение: ограниченный набор ~10industry clips, plant-specific bias; нет открытых часов наблюдений/FA perhour. Не основание обещать такой F1 в кейсе.

<a id="s013"></a>
## S013 — head-mounted industrial PPE

**Поддерживаемые F:** [F021](RAW_FACTS.md#f021), [F022](RAW_FACTS.md#f022). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S13; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Velibor Isailovic, Aleksandar Peulic, Marko Djapan, Marija Savkovic, Arso M. Vukicevic.
- URL: https://www.nature.com/articles/s41598-022-20282-9?code=1&error=cookies_not_supported
- Canonical: https://doi.org/10.1038/s41598-022-20282-9 ; опубликовано29.09.2022, ScientificReports12,16347.
- Прочитаны Materials/Methods, Experiments, Discussion, Conclusion. Table2 separate link не получен; численные значения ниже из Discussion, не реконструированная таблица.
- [F021](RAW_FACTS.md#f021), published measurement:12,682image/12PPE, public+author images; head crops, random70/15/15split. Три detectors FasterRCNN/MobileNetV2SSD/YOLOv5. Meanprecision по трём архитектурам clothmask=.570, cartridge respirator=.540; surgical/N95 входят в группы >.9. Checkpoint setting предложен авторами. Собственная часть данных закрыта.
- [F022](RAW_FACTS.md#f022), methodological caveat/local reading: в §Experiments изложение IoU TP/FN не описывает полноценный обычный unmatched-prediction FP accounting; не считать эти precision числа сертификатом operation/event качества. Статья также по ошибке называет FasterRCNN single-stage. Ввиду этих оговорок источник полезен для относительной трудности классов и постановки, не эталон метрик.

<a id="s014"></a>
## S014 — best view патент

**Поддерживаемые F:** [F023](RAW_FACTS.md#f023). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S14; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы/изобретатели: 郑小玉, 刘自强; assignee PowerChina Chengdu Engineering Co Ltd (GooglePatentsmetadata).
- URL: https://patents.google.com/patent/CN110414400A/en
- Filing22.07.2019, publication05.11.2019; прочитаны Abstract, description method, claims; английский машинный перевод.
- [F023](RAW_FACTS.md#f023), primary patent disclosure: face detection/tracking→face landmarks/PnP→выбор лучшего Euler-angle helmet region→classifier. В description best angle по трём направлениям<=15°. Это описанная конструкция quality-based frame selection.
- Ограничение: патентные заявления о>99% без достаточного benchmark не принимаются как measurement. Face dependence ограничивает спины/окклюзию. Не значит, что надо ждать фронтального лица для каски, видимой сзади.

<a id="s015"></a>
## S015 — pose-anchor патент

**Поддерживаемые F:** [F024](RAW_FACTS.md#f024). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S15; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы/изобретатели: 樊思萌,赵东山,胡志坤,朱言庆; Zhiyang Innovation Technology Co Ltd.
- URL: https://patents.google.com/patent/CN113537019A/en
- Filing07.07.2021, publication22.10.2021; B version grant23.07.2024 не исследована. Прочитаны Abstract, Background и disclosure; машинный перевод.
- [F024](RAW_FACTS.md#f024), primary patent disclosure: AlphaPose nose+shoulders строят headROI, SSD классифицирует каску. Background называет наклон/приседание/лежачую позу трудными для прежних схем.
- Ограничение: не независимый тест и не доказательство улучшения; наличие носа/плеч нужно проверять. Полезен как практический след каскада, но не как причина усложнять MVP.

<a id="s016"></a>
## S016 — потребительское ТЗ «Видеоконтроллер»

**Поддерживаемые F:** [F025](RAW_FACTS.md#f025). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S16; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Организация-публикатор: АНО «Агентство по технологическому развитию», домен itdf.ru.com; потребитель по§1.3 ООО«Вега-Абсолют». Авторы/дата утверждения в прочитанном документе не указаны.
- URL: https://www.itdf.ru.com/208/contracts/391/%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5.pdf
- Прочитаны титульная часть/§1–3, printedp5Table4, §10/11;13PDFpages. Основание ППРФ208от18.02.2022 — не дата этогоТЗ и не ID закупки.
- [F025](RAW_FACTS.md#f025), primary requirement: Таблица4 требует наличие каски/шлема на голове>=95%,очков на лице>=98%,щитка/маски на лице>=98%,перчаток на руках>=90%;1–50зон/кадр. Это требования, не достигнутые результаты. Формулировки bodypart-specific, не presence-anywhere.
- Ограничение: термин«достоверность» без достаточно явного denominator/scene; программа испытаний должна разрабатываться отдельным этапом. Протокол приёмки с результатами не получен. Документ грантового конкурса на КД, не установленная закупка системы безопасности. Подтверждает требования к отношениям, не реализуемость цифр.

<a id="s017"></a>
## S017 — новая классификация N95/goggles: только abstract

**Поддерживаемые F:** [F026](RAW_FACTS.md#f026). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-A-S17; сохранённый реестр [_WORK/SOURCES_A/EVIDENCE.md](_WORK/SOURCES_A/EVIDENCE.md).

- Авторы: Peiran Liu,Xingjian Ma,Haozhi Chen,Denny Yu.
- URL: https://pubmed.ncbi.nlm.nih.gov/42246247/
- Название Automated Assessment of PPE Compliance with Fast Lightweight Deep Learning Based Computer Vision, 05.06.2026, DOI10.1080/24725838.2026.2671785.
- Прочитан только Abstract/metadata. Fulltext не прочитан.
- [F026](RAW_FACTS.md#f026), author reported abstract: entry checkpoint; PPE-CLS/PPE-BQZEL; N95/goggles;2.8Mparams; accuracy.91/.94 vs ViT.88/.90 и до5×faster. Spatial awareness+state-space layer.
- Ограничение: это не дальнее surveillance исследование, нет в прочитанном camera/occlusion/FAhours/детальной экспорта информации. Зацепка для соседнего model_stack/training, не готовый выбор и не подтверждение LinQ.

<a id="s018"></a>
## S018 — Frigate Zones [DOC]

**Поддерживаемые F:** [F027](RAW_FACTS.md#f027), [F028](RAW_FACTS.md#f028). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S01; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: Frigate project. URL: https://docs.frigate.video/configuration/zones/ . Дата публикации не указана; online docs version unpinned. Прочитаны разделы Zones, Zone Loitering, Zone Inertia, Speed Estimation, Best practices and caveats. Версия кода отдельно [S022](SOURCES.md#s022)–[S025](SOURCES.md#s025); тождественность веб-документации релизу не предполагается.

**[F027](RAW_FACTS.md#f027).** Присутствие задаёт нижний центр bbox; величина пересечения рамки с полигоном не используется. Документация описывает `inertia` как последовательные кадры, примеры 3 и 1. `loitering_time` — минимальное время до включения зоны, пример 4 секунды. Это примеры настройки, не промышленные нормативы. Есть различие lifecycle: человек в loitering zone поддерживает review до выхода; для иных объектов stationary влияет на окончание.

**[F028](RAW_FACTS.md#f028).** Speed estimation требует четырёхточечной зоны на земле и измеренных длин сторон; рекомендовано прямолинейное движение, стабильная рамка и видимый нижний центр. Вне откалиброванной зоны скорость может искажаться. Производитель подчёркивает оценочный характер скорости. Это не доказательство точности около погрузчика или законности безопасной дистанции.

Практический смысл: anchor и единицы времени должны быть явной частью правила; геометрическое пересечение bbox и footprint-смысл события различаются.

<a id="s019"></a>
## S019 — Frigate MQTT [DOC]

**Поддерживаемые F:** [F029](RAW_FACTS.md#f029). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S02; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: Frigate project. URL: https://docs.frigate.video/integrations/mqtt/ . Дата публикации неизвестна; version unpinned. Прочитан `frigate/events`, пример before/after payload, `frigate/available`.

**[F029](RAW_FACTS.md#f029).** Обновления одного tracked object имеют одинаковый `id`; типы сообщений `new`, `update`, `end`. Первое сообщение публикуется после выхода из false_positive; лучший snapshot или смена зоны создают обновление. Финальное сообщение содержит `end_time`. Payload различает `current_zones` и `entered_zones`, содержит frame/start/end time и snapshot. Availability различает нормальную остановку, неожиданную потерю соединения и online. Это разные lifecycle: состояние процесса, трека и смыслового нарушения нельзя объединять одним флагом.

Ограничение: API сообщает конец трека, но не устанавливает физическую причину исчезновения человека и не обещает доказанный выход из зоны.

<a id="s020"></a>
## S020 — Frigate Filters [DOC]

**Поддерживаемые F:** [F030](RAW_FACTS.md#f030). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S03; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: Frigate project. URL: https://docs.frigate.video/configuration/object_filters/ . Дата неизвестна; version unpinned. Прочитан Object Scores и Minimum Score.

**[F030](RAW_FACTS.md#f030).** `min_score` отбрасывает отдельные слабые детекции; `threshold` связан с медианой истории score, дополненной до минимум трёх элементов. Слишком высокий min_score может удалить далёкие/перекрытые реальные объекты и разорвать треки. В примере документа есть табличная несогласованность score 0.90 против истории 0.95; числа этой таблицы не используем как эталон реализации. Это подтверждение различия detection gate и track confirmation, а не универсальное N из M.

<a id="s021"></a>
## S021 — Frigate release provenance [CODE metadata]

**Поддерживаемые F:** metadata/статус доступа; не отдельное измерение. **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S04; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: Frigate contributors. URL: https://github.com/blakeblackshear/frigate/releases/tag/v0.18.2 . GitHub API на дату доступа сообщил latest release `v0.18.2`, опубликован 2026-10-15T22:41:47Z. Tag разрешён через commit API: `cfa08c56b23d23280c3d0a218e5a43182c97445b`, commit date 2026-10-15T12:02:08Z. Это фиксация найденного релиза, не утверждение, что организаторы используют Frigate.

<a id="s022"></a>
## S022 — Frigate zone configuration [CODE]

**Поддерживаемые F:** [F031](RAW_FACTS.md#f031). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S05; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

URL: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/camera/zone.py . Автор/версия [S021](SOURCES.md#s021). Прочитан raw-файл tag v0.18.2, строки 42–57, 108–116.

**[F031](RAW_FACTS.md#f031).** Объявленные defaults: `inertia=3`, `loitering_time=0`, `speed_threshold=None`. Валидация предупреждает о совместном loitering_time с distances/speed_threshold. Это источник параметров релиза, не рекомендуемые пороги проекта.

<a id="s023"></a>
## S023 — Frigate TrackedObject.update [CODE]

**Поддерживаемые F:** [F032](RAW_FACTS.md#f032), [F033](RAW_FACTS.md#f033). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S06; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

URL: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/tracked_object.py . Автор/версия [S021](SOURCES.md#s021). Прочитаны initialization 50–80, update 130–390, serialization 400–433. Локаторы особенно 137–151, 186–207, 263–303.

**[F032](RAW_FACTS.md#f032).** `zone_score` вычисляется как прежнее сохранённое значение плюс один. Ветка снаружи при промежуточном счёте сохраняет `zone_score-1`, то есть прежнее значение, без обнуления. По чтению этот фрагмент не реализует reset последовательной серии, обещанной [S018](SOURCES.md#s018). После достижения inertia значение уже не обновляется этой веткой. `zone_loitering` увеличивается в подходящих in-zone обновлениях, сравнивается с `loitering_time * detect.fps`; явного сброса при выходе в прочитанном update нет. Это обнаруженное расхождение семантики DOC/CODE, **не проверенный runtime bug**: вызывающий lifecycle и полная трасса могут менять эффект.

**[F033](RAW_FACTS.md#f033).** Для отсутствующего в текущем кадре объекта score history получает 0; сохраняются последние десять score. Зональная проверка сама по себе не имеет общего условия свежести frame_time (такое условие есть в speed-ветке). Значит, при интеграции следует отдельно проверять, когда и с какими obj_data вызывается update. Предсказанное положение не становится наблюдением.

<a id="s024"></a>
## S024 — Frigate detection defaults [CODE]

**Поддерживаемые F:** [F034](RAW_FACTS.md#f034). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S07; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

URLs: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/camera/detect.py и https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/config.py . Автор/версия [S021](SOURCES.md#s021). Прочитаны DetectConfig 63–78; config.py 842–850.

**[F034](RAW_FACTS.md#f034).** `detect.fps` default 5. Неустановленный `min_initialized` вычисляется как max(int(fps/2), 2), `max_disappeared` как fps*5. Это кадровые параметры lifecycle; приблизительное соответствие пяти секундам зависит от частоты реальных обновлений. Defaults не доказывают, что 5 FPS достаточно для наших камер.

<a id="s025"></a>
## S025 — Frigate review cutoff [CODE]

**Поддерживаемые F:** [F035](RAW_FACTS.md#f035). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S08; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

URLs: https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/config/camera/review.py и https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/review/maintainer.py . Автор/версия [S021](SOURCES.md#s021). Прочитаны AlertsConfig/DetectionsConfig и maintainer 139–158, 180–237, 429–555.

**[F035](RAW_FACTS.md#f035).** Cutoff defaults 40 секунд для alerts и 30 для detections; maintainer проверяет frame_time относительно последней активности плюс cutoff. Для законченного review end_time берётся из last_alert_time/last_detection_time. Это задержка закрытия/группирования review, **не cooldown запрета следующего самостоятельного нарушения**. Review использует current_zones; severity tracked object в другом участке использует entered_zones. Нельзя переносить semantics одного поля на весь проект.

<a id="s026"></a>
## S026 — Supervision PolygonZone [DOC + CODE]

**Поддерживаемые F:** [F036](RAW_FACTS.md#f036), [F037](RAW_FACTS.md#f037). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S09; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: Roboflow contributors. Docs: https://supervision.roboflow.com/latest/detection/tools/polygon_zone/ . Прочитаны Attributes и код trigger. Latest release API: `0.31.1`, 2026-10-20T18:13:09Z; tag commit `f2adfadf2cf9050f44bcb0e71b4b160d8746eab1`, 2026-10-20T18:04:12Z. Код прочитан raw tag: https://github.com/roboflow/supervision/blob/f2adfadf2cf9050f44bcb0e71b4b160d8746eab1/src/supervision/detection/tools/polygon_zone.py , init 84–122, trigger 134–213.

**[F036](RAW_FACTS.md#f036).** Default anchor BOTTOM_CENTER; `require_all_anchors=True` использует all, False — any. Это проверка заданных точек маской, не точное пересечение bbox-полигон: даже any четырёх углов не покрывает случай тонкого полигона через середину bbox. Trigger округляет координаты, проверяет bounds, суммирует попадания. Опциональный coord_transform преобразует anchors; он требует корректной оценки движения камеры извне.

**[F037](RAW_FACTS.md#f037).** В прочитанном trigger tracker_id не используется, хотя warning документации говорит о нём. Для текущего count identity не нужна; для уникальных входов и dwell её нужно хранить отдельно. Это CODE/DOC расхождение, не проверенный runtime defect.

<a id="s027"></a>
## S027 — NVIDIA Gst-nvdsanalytics [DOC]

**Поддерживаемые F:** [F038](RAW_FACTS.md#f038). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S10; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: NVIDIA. URL: https://docs.nvidia.com/deepstream/text/DS_plugin_gst-nvdsanalytics . Доступный dev-guide перенаправил на документацию с меткой версии **9.2**; дата публикации не установлена. Старый URL 7.1 позднее дал ошибку archive redirect; не приписываем прочитанное версии 7.1. Прочитаны вводные 27–32, Features, Configuration File Parameters 70–109.

**[F038](RAW_FACTS.md#f038).** ROI использует bottom center; direction/line crossing требуют tracker-id и истории. Линия задаётся отдельно от вектора направления. `extended=0` ограничивает пересечение отрезком, 1 — продолженной линией. `mode` strict/balanced/loose регулирует допустимое направление, численные угловые пороги не раскрыты. config-width/config-height задают исходное разрешение, правила масштабируются для runtime. Масштабирование разрешения не означает компенсацию pan/zoom/смены ракурса. Документ подтверждает декларативные параметры и metadata output, но не переносимость самого NVIDIA plugin на LinQ.

<a id="s028"></a>
## S028 — OpenCV homography [DOC]

**Поддерживаемые F:** [F039](RAW_FACTS.md#f039). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S11; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: OpenCV contributors. URL после редиректа: https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html . Версия 4.13.0; дата публикации неизвестна. Прочитаны Introduction, Basic theory и coplanar/perspective correction sections.

**[F039](RAW_FACTS.md#f039).** Planar homography задаёт преобразование плоскостей матрицей 3×3 с восемью степенями свободы. Это основание проектировать ground-plane geometry. Применять floor homography к голове, ковшу, поднятым вилам или человеку на платформе — дополнительное необоснованное предположение. Сам документ не даёт требуемой для безопасности ошибки расстояния.

<a id="s029"></a>
## S029 — ByteTrack [MEAS автора + CODE]

**Поддерживаемые F:** [F040](RAW_FACTS.md#f040). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S12; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Авторы: Yifu Zhang et al. Статья: https://arxiv.org/abs/2110.06864v3 , v3 2022-04-07; прочитаны abstract и metadata. Код: https://github.com/FoundationVision/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/byte_tracker.py , BYTETracker.__init__/update; commit 2022-12-11T07:05:00Z, получен API main на дату доступа. Второй файл: https://github.com/FoundationVision/ByteTrack/blob/d1bf0191adff59bc8fcfeaa0b33d3d1642552a99/yolox/tracker/kalman_filter.py , KalmanFilter.__init__.

**[F040](RAW_FACTS.md#f040).** Двухэтапная association использует слабые детекции для восстановления существующих tracklets. В прочитанном коде низкая группа ограничена score>0.1, а high зависит от track_thresh. `frame_id` увеличивается на вызов update, `buffer_size=int(frame_rate/30*track_buffer)`; Kalman dt фиксирован 1. Поэтому передача frame_rate меняет буфер, но сама не вводит переменный timestamp в motion model. Эти параметры — конкретная реализация, не нормативы.

Ограничение: benchmark abstract на MOT17 не отвечает на event-F1 в цехе. Низкие score следует сохранять для association, не автоматически принимать их за надёжные атрибуты СИЗ.

<a id="s030"></a>
## S030 — OC-SORT [MEAS автора + метод]

**Поддерживаемые F:** [F041](RAW_FACTS.md#f041). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S13; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Авторы: Jinkun Cao, Jiangmiao Pang, Xinshuo Weng, Rawal Khirodkar, Kris Kitani. URL: https://arxiv.org/html/2203.14360v3 , 2023-03-16; CVPR 2023. Прочитаны abstract, §3–4, §5.2, Table 2, KITTI limitation, Appendix F. PDF CVF дал 403, использован авторский arXiv HTML.

**[F041](RAW_FACTS.md#f041).** На MOT20-test с одинаковыми detections Table 2: ByteTrack/OC-SORT HOTA 61.3/62.1, MOTA 77.8/75.5, IDF1 75.2/75.9, IDs 1223/913, Frag 1460/1198. Улучшение association сопровождается снижением MOTA: единственный показатель не выбирает метод. ORU исправляет накопленную motion error после повторного наблюдения; виртуальные наблюдения не являются доказательствами видимого нарушения. Авторы прямо отмечают низкий/нулевой IoU при low FPS или быстрых объектах в default IoU association. Внешность — дополнительная cue, а не гарантия.

<a id="s031"></a>
## S031 — BoT-SORT [CODE + авторское описание]

**Поддерживаемые F:** [F042](RAW_FACTS.md#f042). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S14; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Авторы: Nir Aharon, Roy Orfaig, Ben-Zion Bobrovsky. Статья: https://arxiv.org/abs/2206.14651v2 , 2022-07-07; прочитан abstract/metadata. Код: https://github.com/NirAharon/BoT-SORT/blob/251985436d6712aaf682aaaf5f71edb4987224bd/tracker/bot_sort.py . API main commit date 2022-10-30T15:12:42Z. Прочитаны BOTSORT init/update, ReID/GMC/association.

**[F042](RAW_FACTS.md#f042).** ReID опционален через with_reid; FastReID encoder вызывается на dets. GMC применяется отдельно к track states. Appearance distance маскируется и appearance threshold, и геометрическим proximity threshold. Значит, добавление ReID не гарантирует спасения очень большого разрыва между кадрами при неизменном gate. Семейство без ReID и с ReID имеет разную нейровычислительную нагрузку; GMC не калибрует автоматически физическую опасную зону.

<a id="s032"></a>
## S032 — AXIS Object Analytics manual [DOC]

**Поддерживаемые F:** [F043](RAW_FACTS.md#f043), [F044](RAW_FACTS.md#f044). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S15; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: Axis Communications. URL: https://help.axis.com/en-us/axis-object-analytics . Дата публикации неизвестна; online manual version unpinned. Прочитаны Modify a scenario, Calibrate perspective, PTZ preset, Ignore short-lived objects, Record video when human stays too long.

**[F043](RAW_FACTS.md#f043).** Time in area и Keep active while tracked — отдельные настройки. Последняя держит rule активным по треку, а не только на время alarm. Short-lived filter задерживает реакцию; запись нуждается в prebuffer. Perspective calibration использует объекты известной высоты на земле; поддержка зависит от камеры. При смене PTZ preset нужна перекалибровка; рекомендация manual — минимум 15 секунд между preset в guard tour. Это конкретный продуктовый режим, не универсальное время стабилизации камеры.

Дополнение/история чтения той же цепочки (W2-B-S09); не независимый эксперимент:

Автор Axis Communications, **September2026** на странице; https://help.axis.com/en-us/axis-object-analytics . Прочитаны Considerations и Classification. **[F044](RAW_FACTS.md#f044):** взгляд строго сверху затрудняет classification; частичная видимость, fog/noise/плохой контраст ограничивают generic human/vehicle analytics. Это не численная оценка topview PPE. Не распространять4%/8% human heights на сигарету или респиратор.

<a id="s033"></a>
## S033 — AXIS Object Analytics API [DOC]

**Поддерживаемые F:** [F045](RAW_FACTS.md#f045). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S16; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Автор: Axis Communications. URL: https://www.developer.axis.com/vapix/applications/axis-object-analytics-api/ . Дата неизвестна, website unpinned; примеры apiVersion 1.2, поддержку надо получать от устройства. Прочитаны Configuration capabilities, Scenario types/triggers/filters, Short-lived objects, Occupancy in area.

**[F045](RAW_FACTS.md#f045).** `timeShortLivedLimit` отсчитывает время видимости объекта в изображении: объект, уже видимый дольше фильтра, может сразу вызвать alarm при входе в include area. Это не dwell внутри зоны. `triggerDelay` occupancy — секунды после достижения численного порога. Разрешённые min/max/default и комбинации сценариев запрашиваются `getConfigurationCapabilities`; нельзя назначить один универсальный набор для всех камер. Speed filter в прочитанном API требует secondary radar, поэтому не служит доказательством monocular metric speed. В строках таблицы capabilities есть расхождения имён Time/Distance; буквальные примеры следует проверять capabilities, не копировать механически.

<a id="s034"></a>
## S034 — Monocular proximity around excavator [MEAS автора, качественные результаты]

**Поддерживаемые F:** [F046](RAW_FACTS.md#f046). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S17; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Авторы: Hyojoo Son, Hyunwoo Sung, Hyunchul Choi, Sungwook Lee, Changwan Kim. 2017, ISARC pp.500–505, DOI 10.22260/ISARC2017/0069. URL полного текста: https://www.iaarc.org/publications/fulltext/ISARC2017-Paper069.pdf . Прочитаны §2–5, страницы PDF 2–5; фигуры 1–5 рассмотрены через извлечённый текст/описания; screenshot вызван, но изображение инструмент не вывел, поэтому визуальная QA рисунка не заявляется.

**[F046](RAW_FACTS.md#f046).** Исследование допускает monocular proximity при известных высоте/азимуте камеры и плоской земле; камера на корпусе экскаватора, distortion correction, shadow removal, perspective transforms. Пример выделяет препятствия высотой минимум 1 м и круговую область для заданного экскаватора; это условия метода, не безопасные нормативы. В conclusion отказ от planar-ground assumption остаётся future work. Публикация показывает примеры работы, не даёт измерения event false alarms/hour. Для цеха нужны собственные ground calibration и модель footprint/рабочего органа.

<a id="s035"></a>
## S035 — DCASE 2022 event matching [DOC протокола]

**Поддерживаемые F:** [F047](RAW_FACTS.md#f047). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S18; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Авторы: организаторы DCASE Task 4 (Romain Serizel et al., список на странице). URL: https://dcase.community/challenge2022/task-sound-event-detection-in-domestic-environments . Контекст 2022, дата последнего обновления неизвестна. Прочитаны Strong annotations, Evaluation metrics и Contrastive metric.

**[F047](RAW_FACTS.md#f047).** Публичный протокол разделяет intersection-based и collar-based event F1; collar example onset 200ms, offset max(200ms,20% duration), с явно выбранным operating point. Это **аудиозадача**; переносим только принцип объявленного temporal matching и отдельно class/time annotations. Указанные допуски и результаты нельзя объявлять стандартом промышленной видеоаналитики.

<a id="s036"></a>
## S036 — ITV/Axxon registry manuals: доступ частичный, параметры не приняты как факт

**Поддерживаемые F:** metadata/статус доступа; не отдельное измерение. **Доступ:**2026-10-23 (+03:00). **Происхождение:** W1-B-S19; сохранённый реестр [_WORK/SOURCES_B/EVIDENCE.md](_WORK/SOURCES_B/EVIDENCE.md).

Зацепки: https://docs.itvgroup.ru/confluence/pages/viewpage.action?pageId=157705313 ; https://docs.itvgroup.ru/confluence/download/attachments/337546226/RegistryKeys.pdf?api=v2 ; https://docs.itvgroup.ru/confluence/download/attachments/136937518/RegistryKeys.pdf . Web один раз открыл первые страницы/оглавление 344-страничного «Интеллект 5.0», updated 06.02.2025. Последующее чтение целевых страниц не удалось (502/TLS EOF); standalone 4.11 page metadata: Roman Nazarov, обновление Evgeniya Kononova 26.11.2025.

Поисковые сниппеты содержат `VMDA.oneAlarmPerTrack`, `LongInZoneTimeout2`, `report_frequency`; это полезные точные ключи для второй волны, но окружающие таблицы нужной версии реально не прочитаны. **Не использовать defaults 1/10sec/3000ms из этой зацепки как доказанные параметры нашего отчёта.** Нет подтверждённого документа приёмочных испытаний или закупки по промышленной безопасности.

<a id="s037"></a>
## S037 — Bosch VCA 6.30 Releaseletter

**Поддерживаемые F:** [F048](RAW_FACTS.md#f048). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S01; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Автор: Bosch Security Systems B.V., BT-VS/MKP-AIC Product Management, Hildesheim. Документ датирован **16.10.2024**, название в PDF — Bosch Releaseletter VCA 6.30. URL: https://cdn.commerce.boschsecurity.com/public/documents/RL_VCA_Release_Note_enUS_88157155723.pdf . Копия: [bosch-vca630.pdf](_WORK/SOURCES_C/bosch-vca630.pdf); визуально проверена страница 5: [BOSCH_PPE_PAGE.png](_WORK/SOURCES_C/BOSCH_PPE_PAGE.png). Web не смог разобрать application/octet-stream; urllib получил PDF, PyMuPDF отрисовал p5. Poppler в PATH не найден; использован доступный PyMuPDF.

**[F048](RAW_FACTS.md#f048) [primary doc]:** p5, блок PPE Limitations: применимо к CPP14, исключены 3000/multi/corner/panoramic. Детекция/трекинг 7.5 FPS вместо обычных 15; PPE attributes примерно раз в 3 секунды для каждого человека. В аналитическом разрешении 1280×720 или 1024×576 для 8MP-камер: жилет — минимум 48 px **высоты человека**, каска — 96 px. Минимум 200 lx, вертикальные стоящие/идущие люди, PPE обращено к камере, без перекрытий, рекомендуют движение по одному. Полосы жилета должны стать видимыми; белая каска не должна быть пересвечена. Это требования конкретного продукта, не эксперимент на нашей модели.

<a id="s038"></a>
## S038 — Macroscop: семантика падения

**Поддерживаемые F:** [F049](RAW_FACTS.md#f049). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S03; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

https://doc.macroscop.com/analytics/fall-detector/overview.htm . Автор Macroscop. Прочитан body и «Примечание», текущая страница Last updated 22.10.2026, навигация 4.7; первый cached result показывал 4.6. **[F049](RAW_FACTS.md#f049) [primary doc]:** модуль называет падением лежачее положение человека и прямо исключает определение самого процесса падения. Это предметная оговорка, которую маркетинговое имя скрывает.

<a id="s039"></a>
## S039 — Macroscop: fall requirements

**Поддерживаемые F:** [F050](RAW_FACTS.md#f050). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S04; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

https://doc.macroscop.com/analytics/fall-detector/requirements.htm . Автор Macroscop, docs4.7, Last updated 22.10.2026. Прочитаны разделы «Видеопоток», «Изображение», «Сцена и расположение камеры». **[F050](RAW_FACTS.md#f050) [primary doc]:** >=10 FPS; оптимальное HD/FullHD; цвет, стабильное равномерное освещение, без существенных артефактов; человек целиком и >=8% высоты кадра; наклон к горизонтальной поверхности <=35°; исключаются отражающие зеркальные поверхности. Не универсальный FPS для любой fall/action модели.

<a id="s040"></a>
## S040 — Video based human smoking event detection method

**Поддерживаемые F:** [F051](RAW_FACTS.md#f051). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S05; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Авторы Anna V. Pyataeva, Maria S. Eliseeva. SDM-2021, 24–27.08.2021; pp343–352. https://ceur-ws.org/Vol-3006/40_regular_paper.pdf . Прочитаны pp343–348 и p351/table5; не только abstract.

**[F051](RAW_FACTS.md#f051) [published method/measurement]:** Sec2.1 рассматривает последовательность рука к губам → пауза → опускание, зажигание и стряхивание пепла; дым нестабилен по форме/прозрачности и зависит от съёмки. 3D ResNet34, Sec2.3 говорит input16frames, Sec2.4 — 32frames 112×112: явная внутренняя неоднозначность. Experimental section: 70 smoking videos, HMDB51 negatives; тест дополнен леденцом, ручкой во рту, мороженым; split80/20. Table5 сравнивает ResNet/ResNetM на 20 клипах, заявляет улучшение, но не даёт события на камеру-час или industrial external validation. Несогласованное описание negatives (6766 и включение smoking в перечне HMDB51) не позволяет восстановить чистый split. Сохранённые цифры не переносить на цех. Практический смысл: клип и hard negatives обязательны; это слабое основание для оценки production FA.

<a id="s041"></a>
## S041 — CN109598214A

**Поддерживаемые F:** [F052](RAW_FACTS.md#f052). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S06; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Автор/изобретатель 杨恒 (Yang Heng); original assignee Shenzhen Emo Technology Co Ltd. Публикация **09.04.2019**, priority22.11.2018. https://patents.google.com/patent/CN109598214A/en . Прочитаны metadata, описание S110–S130 и claims1–5; машинный EN-перевод Google Patents.

**[F052](RAW_FACTS.md#f052) [patent method, no measured validation]:** локализует рот, ищет светящуюся область, при перекрытии рот–рука ищет её на руке; pose keypoints возможны для определения mouth/hand regions. Отмечает сбои face methods при большом угле/закрытом лице. Не опубликована приёмочная точность метода. В наших условиях сварка, отражения, светодиоды и невидимый тлеющий конец требуют проверки как hard negatives/unknown. Патент доказывает существование постановки, не её качество и не свободу использования.

<a id="s042"></a>
## S042 — TP-LINK 红外测温08—吸烟检测使用指导

**Поддерживаемые F:** [F053](RAW_FACTS.md#f053). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S07; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Автор TP-LINK视觉安防; дата/версия на странице не установлены. https://security.tp-link.com.cn/service/detail_article_4828.html . Прочитан body «功能介绍/配置流程».

**[F053](RAW_FACTS.md#f053) [vendor manual/claim]:** камера использует AI **вместе с температурным обнаружением**; рекомендуемая дистанция smoking detection около5–10m. На момент текста standalone, без push в recorder/APP, возможен alarm output. Дистанция относится к этой тепловой системе, не к любому RGB smoking detector. Конкретная оптика/модель на странице не указана. Пригодно как контрпример: коммерческое «детектирует курение» может требовать другой модальности.

<a id="s043"></a>
## S043 — Lim et al., harness/hook

**Поддерживаемые F:** [F054](RAW_FACTS.md#f054). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S08; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Jeeyoung Lim, Dae Gyo Jung, Chansik Park, Dae Young Kim. **31.07.2022**, Advances in Civil Engineering,4678479. DOI https://doi.org/10.1155/2022/4678479 ; publisher https://onlinelibrary.wiley.com/doi/10.1155/2022/4678479 . Авторский PDF получен из репозитория Chung-Ang University: https://scholarworks.bwise.kr/cau/bitstream/2019.sw.cau/78560/1/Computer%20Vision%20Process%20Development%20regarding%20Worker%27s%20Safety%20Harness%20and%20Hook%20to%20Prevent%20Fall%20Accidents%3B%20Focused%20on%20System%20Scaffolds%20in%20South%20Korea.pdf . Прочитаны p5–10, особенно conclusion p10. После выписки полная статья удалена из служебных материалов по поручению хранить пересказ.

**[F054](RAW_FACTS.md#f054) [published observation/limitation]:** процесс различает harness, hook, attachment facility и контекст scaffold/workphase. В sample application p8 worker распознан, hook не найден из-за малого размера. Conclusion p10 повторяет: worker/harness recognized, hook not recognized; систему проверки **connection** ещё нужно создать, в этой работе этого не сделано. Пример/методология не являются доказательством обнаружения пристёгнутого карабина. Аннотация сама по себе могла бы создать обратное впечатление. Наш вывод: наличие harness и близость hook к anchor недостаточны для доказательства механического зацепления/запертого замка.

<a id="s044"></a>
## S044 — YOLO-World paper and pinned developer documentation

**Поддерживаемые F:** [F055](RAW_FACTS.md#f055). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S09; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Tianheng Cheng et al., CVPR **June2024**, pp16901–16911. https://openaccess.thecvf.com/content/CVPR2024/html/Cheng_YOLO-World_Real-Time_Open-Vocabulary_Object_Detection_CVPR_2024_paper.html . Прочитан abstract; PDF web403, подробную постановку подтверждает developer doc https://github.com/AILab-CVC/YOLO-World/blob/4f70adbaacf5685bd9ec5bea85f1f91057f6fc0b/docs/reparameterize.md . Commit master SHA получен GitHub API и pinned raw-file прочитан23.10.2026. Это документация, код не запускался.

**[F055](RAW_FACTS.md#f055) [primary developer doc]:** embeddings текста можно включить параметрами в голову: final classification становится1×1 convolution, а не transpose/matmul. Doc предусматривает reparameterize head `YOLOWorldHeadModule` и neck `MaxSigmoidCSPLayerWithTwoConv`; подготовить NxD embeddings и новый checkpoint. Словарь выбирается до исполняемого графа; новый словарь требует повторной подготовки артефакта, и на LinQ может потребовать recompilation. Последнее — наш вывод, не подтверждённый LinQ API. Не вся модель становится «без attention» только по этому тексту, и detection не превращается в проверку соблюдения.

<a id="s045"></a>
## S045 — YOLOE

**Поддерживаемые F:** [F056](RAW_FACTS.md#f056). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S10; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Ao Wang, Lihao Liu, Hui Chen, Zijia Lin, Jungong Han, Guiguang Ding. v1 10.03.2025, **v2 17.10.2025**. https://arxiv.org/html/2503.07465v2 . Прочитаны abstract, introduction, Sec3.1–3.4.

**[F056](RAW_FACTS.md#f056) [published method]:** RepRTA text prompts reparameterizes auxiliary network into classification head при inference/transfer; авторы называют полученную архитектуру идентичной YOLO. Visual prompts SAVPE и prompt-free LRPC — отдельные механизмы, не следуют автоматически из fixed text graph. «Zero overhead» относится к сравнению этой текстовой схемы с YOLO, не к нулевой стоимости whole pipeline, LinQ compilation или новой категории без ошибок. Качество промышленных респираторов/сигарет и event FA не установлено.

<a id="s046"></a>
## S046 — Grounding DINO

**Поддерживаемые F:** [F057](RAW_FACTS.md#f057). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S11; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Shilong Liu et al. v1 09.03.2023, **v5 19.07.2024**. https://arxiv.org/html/2303.05499v5 . Прочитаны abstract, introduction, Sec3 architecture. **[F057](RAW_FACTS.md#f057) [published method]:** text-image fusion в feature enhancer, language-guided queries, cross-modality decoder; self/cross-attention. Описание произвольных объектов/атрибутов не означает скомпилированную сменную1×1 голову. Наш вывод: требования к графу и текстовым inputs существенно богаче фиксированного reparameterized vocabulary; возможность LinQ не установлена, запрещать её без ops list нельзя.

<a id="s047"></a>
## S047 — POPE / object hallucination

**Поддерживаемые F:** [F058](RAW_FACTS.md#f058). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S12; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao, Ji-Rong Wen; EMNLP **December2023**, pp292–305. https://aclanthology.org/2023.emnlp-main.20/ ; paper https://aclanthology.org/2023.emnlp-main.20.pdf . Прочитаны abstract/введение PDF и publisher metadata.

**[F058](RAW_FACTS.md#f058) [published measurement/limitation]:** LVLM могут утверждать объекты, отсутствующие на изображении; visual instructions и co-occurrence влияют на hallucination. POPE использует polling questions для оценки. Исследование относится к изученным2023 моделям/benchmark, не измеряет current VLM на промышленных тревогах. Наш вывод: положительный ответ verifier не ground truth; проверять paired precision/recall и hallucinated predicates, а не обещать снижение FA по факту добавления VLM.

<a id="s048"></a>
## S048 — SAHI

**Поддерживаемые F:** [F059](RAW_FACTS.md#f059). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S13; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Fatih Cagatay Akyon, Sinan Onur Altinuc, Alptekin Temizel. ICIP2022, arXiv v5 **24.10.2022**. https://arxiv.org/html/2202.06934v5 . Прочитаны abstract, Sec3 Proposed Approach и Sec4/Table1. **[F059](RAW_FACTS.md#f059) [published method/measurement]:** overlapping image patches делают small targets относительно крупнее на входе сети, результаты объединяются; возможно full-image pass. Уточнение после Sec4/Table1: gains 6.8/5.1/5.3 — AP50 в процентных пунктах для FCOS/VFNet/TOOD на VisDrone19 test-dev, SAHI+FI+25% overlap против FI, не smoking/PPE. VisDrone tiles640×640, xView400×400; singleIoU0.5, maxdets500. Наш вывод: кропы помогают сохранить исходные детали при resize, но не восстанавливают отсутствующий сигнал; цена — несколько forward passes, overlap duplicates и merge. Утверждение introductory DORI статьи не принимаем как PPE-норматив; [S049](SOURCES.md#s049) точнее разграничивает назначение DORI.

<a id="s049"></a>
## S049 — Axis pixel density white paper

**Поддерживаемые F:** [F060](RAW_FACTS.md#f060). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S14; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Автор Axis Communications, версия страницы **April2026**. https://whitepapers.axis.com/en-us/pixel-density-based-on-iec-62676-4-2014 . Прочитаны Summary/Operational requirements/Simplified model. **[F060](RAW_FACTS.md#f060) [primary vendor explanation of standard]:** 2014 DORI25/63/125/250 px/m описывает человеческое восприятие detection/observation/recognition/identification. Страница явно говорит, что для software analytics применяются другие определения. Свет, оптика, compression также влияют. Это объяснение IEC62676-4:2014, а не установленный действующий на2026 PPE-стандарт; стандарт полностью не читался.

<a id="s050"></a>
## S050 — PTQ4ViT

**Поддерживаемые F:** [F061](RAW_FACTS.md#f061). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S15; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Zhihang Yuan, Chenhao Xue, Yiqi Chen, Qiang Wu, Guangyu Sun. v1 24.11.2021, **v3 23.06.2024**. https://arxiv.org/html/2111.12293v3 . Прочитаны abstract/introduction/Sec3.2. **[F061](RAW_FACTS.md#f061) [published mechanism/measurement]:** post-softmax значения неравномерны, GELU асимметричен; обычный uniform PTQ может терять малые значения и давать >1% accuracy drop даже8bit. Специальный twin-uniform quantization даёт <0.5% drop на ImageNet ViT/DeiT/Swin. Это опровергает и «INT8 безопасен автоматически», и «attention невозможно квантизовать». Не доказательство LinQ реализации этих схем и не измерение позовых keypoints/малых PPE.

<a id="s051"></a>
## S051 — NVIDIA QAT counterexample

**Поддерживаемые F:** [F062](RAW_FACTS.md#f062). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S16; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Varun Praveen/NVIDIA. **04.08.2020**. https://developer.nvidia.com/blog/improving-int8-accuracy-using-quantization-aware-training-and-tao-toolkit/ . Прочитаны авторский основной текст, Figure1 и Results/table1, AI-generated summary не использован.

**[F062](RAW_FACTS.md#f062) [vendor published measurement]:** PeopleNet-ResNet18 mAP FP32 78.37→PTQ59.06→QAT78.06; ResNet34 80.2→62→79.57. Автор показывает spurious bounding boxes после TensorRT INT8 PTQ, предупреждает о regression output granularity. Это конкретный DetectNet/PeopleNet/entropy-calibrator пример; не универсальный размер падения, не современный YOLO и не LinQ. Наш вывод: смотреть FP→INT8 не только mAP, но и новые ложные candidate/events; float output может требовать поддержки платформы, которой пока нет.

<a id="s052"></a>
## S052 — public LinQ tech

**Поддерживаемые F:** [F063](RAW_FACTS.md#f063). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S17; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

ООО «ХайТэк»; дата страницы неизвестна, доступ23.10.2026. https://lin-q.ru/tech . Прочитаны блоки «Тензорный процессор», «Собственное IP-ядро», «Поддерживаемые сети», framework. **[F063](RAW_FACTS.md#f063) [vendor claim]:** LinQ H — int8, CNN/RNN; в списке yolo5s/yolo8/yolo11 и другие. Отсутствуют точные checkpoints, shapes, opsets, postprocess boundary и SDK version. Список семейств не гарантирует исполнение выбранного pose/seg/open-vocab варианта.

<a id="s053"></a>
## S053 — public LinQ HPS datasheet/home

**Поддерживаемые F:** [F064](RAW_FACTS.md#f064). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S18; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

ООО «ХайТэк», дата/revision PDF не указана. https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf ; https://lin-q.ru/ . Прочитаны datasheet p1–3, homepage product family. **[F064](RAW_FACTS.md#f064) [vendor claim]:** HPS имеет основной int8; fp16/bfloat16 обозначены перспективой. PyTorch через ONNX и LinQ Compiler/DNN Quant заявлены. HPS — одна конкретная линейка, homepage различает HP/HPD/HPQ/HPS/HX. Не установлено, какой ускоритель/SDK дают на хакатоне; «полная поддержка ONNX» в datasheet не substitutes supported ops/test compile.

<a id="s054"></a>
## S054 — официальный анонс

**Поддерживаемые F:** [F065](RAW_FACTS.md#f065). **Доступ:**2026-10-23 (+03:00). **Происхождение:** C-S19; сохранённый реестр [_WORK/SOURCES_C/EVIDENCE.md](_WORK/SOURCES_C/EVIDENCE.md).

Организаторы Открой#Моспром; дата публикации блока неизвестна, доступ23.10.2026. https://hackathon2026.otkroimosprom.ru/ . Прочитан блок кейса LinQ. **[F065](RAW_FACTS.md#f065) [primary announcement]:** примеры smoking near flammables, respirator removed, no hardhat, danger zone; real-time video service; model inference must run on LinQ, online access promised. Нет в прочитанном блоке SDK/оборудования/точного списка обязательных сценариев. Это анонс, не полный кейс.

<a id="s055"></a>
## S055 — официальная поставка SH17 и её два реальных примера

**Поддерживаемые F:** [F066](RAW_FACTS.md#f066), [F067](RAW_FACTS.md#f067), [F068](RAW_FACTS.md#f068). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-A-S01; сохранённый реестр [_WORK/SOURCES_W2A/EVIDENCE.md](_WORK/SOURCES_W2A/EVIDENCE.md).

Авторы: Hafiz Mughees Ahmad, Afshin Rahimi; владелец Kaggle mugheesahmad.

- [Репозиторий](https://github.com/ahmadmughees/SH17dataset), master `2f832c289f9deea063367045ed8230b26e3e7ea9`; [дерево](https://api.github.com/repos/ahmadmughees/SH17dataset/git/trees/master?recursive=1). Собственная сохранённая запись `sh17-tree.json` содержит `truncated=false`. GitHub release assets просмотрены: веса, отдельный extended annotation artifact не найден.
- [Kaggle](https://www.kaggle.com/datasets/mugheesahmad/sh17-dataset-for-ppe-detection); [metadata API](https://www.kaggle.com/api/v1/datasets/view/mugheesahmad/sh17-dataset-for-ppe-detection): dataset ID5329058, version1, lastUpdated `2024-07-03T23:09:23.513Z`. API metadata получены локально, web body пустой.
- [Конкретный VOC](https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName=voc_labels%2Fcareer-firefighter-relaxing-job-162540.xml), [YOLO](https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName=labels%2Fcareer-firefighter-relaxing-job-162540.txt), [исходное изображение](https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName=images%2Fcareer-firefighter-relaxing-job-162540.jpeg). Сохранены `voc_labels-career-firefighter-relaxing-job-162540.xml`, `labels-career-firefighter-relaxing-job-162540.txt`, `firefighter.jpeg`.
- Второй basename `building-construction-building-site-constructing`: `sh17-sample-voc-download`, `labels-building-construction-building-site-constructing.txt`; те же URL с заменой basename и расширения.

**[F066](RAW_FACTS.md#f066) [artifact inspection].** В проверенных XML: filename/size, object name/pose/truncated/difficult/bndbox; wearer ID, on/off и relation отсутствуют. В TXT пять колонок. Firefighter helmet: YOLO class10, bbox `[.536750,.393375,.249833,.274750]`; XML `[2471,1024,3970,2123]` при6000×4000. Класс9 второго примера — gloves.

**[F067](RAW_FACTS.md#f067) [local visual observation].** В firefighter фото каска лежит на снятой куртке; голова сидящего человека вне кадра. Разметка сохраняет helmet как предмет, но не сообщает off или отсутствие защиты головы. Это конкретный контрпример `object_present => worn` и `off-body => uncovered`.

**[F068](RAW_FACTS.md#f068) [scope/unknown].** Инспектированы два примера, не все8099. Официальный отдельный extended export не получен. Нельзя утверждать, что tags нигде не существуют; нельзя обещать wearer relation в скачиваемой YOLO/VOC поставке.

<a id="s056"></a>
## S056 — industrial 3M head-state, полный текст

**Поддерживаемые F:** [F069](RAW_FACTS.md#f069), [F070](RAW_FACTS.md#f070). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-A-S03; сохранённый реестр [_WORK/SOURCES_W2A/EVIDENCE.md](_WORK/SOURCES_W2A/EVIDENCE.md).

Zhu Yi, Wang Bangrong, Wang Jun, Xu Xiaofeng, *YOLOv8-LPE—a gas mask wearing detection method for industrial scenarios*, Journal of Qingdao University of Technology46(6),149–156,2025; received2024-04-28 — не дата выпуска. [Страница PDF издателя](https://cjournal.hep.com.cn/1673-4602/CN/PDF/1217769465963126793), [прямой PDF](https://jf2.hep.com.cn/aac09e01e03546ab91293b47895a116a.pdf). Web redirect failed; HTTP download200,6,520,852bytes,8pages, PyMuPDF text прочитан; p151 отрисована и визуально осмотрена. Сохранён только locator screenshot `gasmask-table-page.png`, не полная статья.

**[F069](RAW_FACTS.md#f069) [primary annotation semantics].** §1 pp150–151/Table1/Fig1–2: industrial3M cartridge head-state. Front/side wear_mask, no_wear, wear_wrong; седьмой back_head. Wrong включает обычную медицинскую маску вместо промышленной. Реальные+симулированные сцены,7992images,6058train/1934test. Neck/hand и removal-transition классов нет; unknown не отдельный PPE-class, back_head — observable orientation, который наша политика должна отобразить в unknown face coverage.

**[F070](RAW_FACTS.md#f070) [published measurement caveat].** §3.1p153: input1280², stated Nvidia GTX3090. §3.2 неверно описывает AP IoU threshold как confidence threshold; Table2 также содержит несогласованный F1. Эти ошибки ограничивают доверие интерпретации метрик. Не используем aggregate mAP для обещания событий, LinQ или transfer. Код/annotation artifact по этой работе не получены.

<a id="s057"></a>
## S057 — исходная Faster R-CNN цепочка, ограниченный доступ

**Поддерживаемые F:** [F071](RAW_FACTS.md#f071). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-A-S04; сохранённый реестр [_WORK/SOURCES_W2A/EVIDENCE.md](_WORK/SOURCES_W2A/EVIDENCE.md).

Bangrong Wang, Jun Wang, Xiaofeng Xu, Xianglin Bao; *Gas mask wearing detection based on Faster R-CNN*, [DOI](https://doi.org/10.3233/AIS-220460). First online17.08.2023, issue16(1):57–71,14.03.2024. [Издатель](https://journals.sagepub.com/doi/abs/10.3233/AIS-220460).

**[F071](RAW_FACTS.md#f071) [access status].** PDF URL редиректит на restricted abstract; epdf/full/старый IOS URL не открылись. Поисковый индекс показывает Table1/6134images/15scenes, но этот body не получен: не выдаём его за прочитанный fulltext и не объединяем с7992images [S056](SOURCES.md#s056). Новый [S056](SOURCES.md#s056) даёт самостоятельное прочитанное основание семантики.

<a id="s058"></a>
## S058 — R2PPE: N95/adherence и ambiguous omission

**Поддерживаемые F:** [F072](RAW_FACTS.md#f072). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-A-S05; сохранённый реестр [_WORK/SOURCES_W2A/EVIDENCE.md](_WORK/SOURCES_W2A/EVIDENCE.md).

Wanzhao Yang, Mary S. Kim, Genevieve J. Sippel, Aaron H. Mun, Kathleen H. McCarthy, Beomseok Park, Aleksandra Sarcevic, Marius George Linguraru, Ivan Marsic, Randall S. Burd. *An image dataset for surveillance of personal protective equipment adherence in healthcare*, Scientific Data12,96,17.01.2025. [DOI](https://doi.org/10.1038/s41597-024-04355-0); [официальный fulltext XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11742010/fullTextXML) получен; Methods/Dataset Annotation, Table1, Data Records прочитаны. PMC web давал recaptcha, XML независимым HTTP доступен.

**[F072](RAW_FACTS.md#f072) [primary annotation guide].** Mask absent = не надет либо открыты нос и рот; incomplete = нос открыт, рот закрыт. N95 complete выделен из regular mask. Неразрешимую для разметчика неоднозначность пропускали, а не помечали absent. Поэтому отсутствие annotation не отрицательное доказательство. Клинические simulations и их цвета/формы не промышленная переносимость; fit/seal и cartridge off-neck/hand не доказаны.

<a id="s059"></a>
## S059 — фактическая R2PPE разметка

**Поддерживаемые F:** [F073](RAW_FACTS.md#f073). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-A-S06; сохранённый реестр [_WORK/SOURCES_W2A/EVIDENCE.md](_WORK/SOURCES_W2A/EVIDENCE.md).

Те же создатели. [Zenodo record](https://zenodo.org/records/13851664), publication27.09.2024,v1, modified29.09.2024; [annotations.zip](https://zenodo.org/records/13851664/files/annotations.zip?download=1),md5 record `c190615219de9b9b389c705c95d0c7f0`. Архив получен и JSON прочитан в памяти; изображения34.5GB/видео6GB не скачивались. Собственная небольшая выборка+schema summary: `r2ppe-annotation-inspection.json`.

**[F073](RAW_FACTS.md#f073) [artifact inspection].** `annotations/combined.json`:10034images,123751annotations,18categories. Реальны IDs7 Mask_Absent_ma,8 Mask_Incomplete_mi,9 N95_complete_nc,10 N95_Strap_s,17 PAPR_pr,18 Head. Union annotation keys: area,bbox,category_id,id,image_id,iscrowd,segmentation. Нет wearer_id/track_id/relation keys. Это state labels+bbox; N95_Strap не факт seal. No neck/hand/remove labels. Source2 actual schema подтверждена, но healthcare не industrial cartridge.

<a id="s060"></a>
## S060 — FMR-DB и патентный контрпример

**Поддерживаемые F:** [F074](RAW_FACTS.md#f074). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-A-S07; сохранённый реестр [_WORK/SOURCES_W2A/EVIDENCE.md](_WORK/SOURCES_W2A/EVIDENCE.md).

Antonio Costantino Marceddu, Bartolomeo Montrucchio,2020. [Институциональная запись FMR-DB](https://iris.polito.it/handle/11583/2856883), DOI10.21227/wg71-v415. Реально прочитан abstract/metadata: half/full-face, disposable valved/unvalved и occlusion negatives; файлов в записи нет. IEEE DataPort через web недоступен. **[F074](RAW_FACTS.md#f074) [scope]:** полезная таксономическая зацепка, не полученная neck/hand annotation поставка.

<a id="s061"></a>
## S061 — CN117079082A — многоракурсная проверка маски

**Поддерживаемые F:** [F075](RAW_FACTS.md#f075). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-A-S07-patent; сохранённый реестр [_WORK/SOURCES_W2A/EVIDENCE.md](_WORK/SOURCES_W2A/EVIDENCE.md).

CN117079082A, Nanjing Aokan Information Technology; 熊秀芳,何欣,肖伟,尹科才,董文杰; filing16.10.2023,publication17.11.2023. [Текст](https://patents.google.com/patent/CN117079082A/zh), description S201–206 прочитаны. **[F075](RAW_FACTS.md#f075) [patent disclosure, not measured deployment]:** lithium-cell dismantling, front/diagonal multiple4MPcameras; заднюю ориентацию предлагается разрешать другим видом. Mask/Unmask пример опирается на цвет лица/маски. Это контрпример generic «correct wearing»: camera/context-specific shortcut, без публичного neck/hand/unknown benchmark. Численные обещания качества не заимствуются.

<a id="s062"></a>
## S062 — Axxon Next VL: условия потока и освещения [primary manual]

**Поддерживаемые F:** [F076](RAW_FACTS.md#f076). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S01; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Автор страницы Gleb Matskevich / AxxonSoft; updated 29.05.2023. Версия строго **Axxon Next 4.5.0–4.5.10**, не нынешняя линейка One. URL: https://docs.axxonsoft.com/confluence/spaces/next45en/pages/260906681/Video+stream+and+scene+requirements+for+PPE+detection+tool+VL+operation . Прочитан body items1–3, не только сниппет.

**[F076](RAW_FACTS.md#f076).** VL требует цвет; для typical tasks указан ≥13FPS. Раздел lighting не гарантирует стабильность при ночи/засветке, требует постоянства освещения. Текст пишет «200 lux per square meter»: единица в оригинале некорректна, здесь не исправляем её в новый норматив. Указаны ограничения перекрытий, отражений, вибрации, грязной оптики и fisheye. Это admission conditions конкретного модуля, не измерение деградации и не физическая невозможность любого IR-детектора. Новое относительно Macroscop: независимая продуктовая цепочка подтверждает, что generic camera night mode не является обещанием PPE night support.

<a id="s063"></a>
## S063 — Axxon Next VL: условия изображения объекта [primary manual]

**Поддерживаемые F:** [F077](RAW_FACTS.md#f077). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S02; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Тот же автор, дата и версия. URL: https://docs.axxonsoft.com/confluence/spaces/next45en/pages/260906683/Objects+image+requirements+for+PPE+detection+tool+VL . Прочитаны items1–6 и таблица.

**[F077](RAW_FACTS.md#f077).** Требуются визуальная различимость СИЗ человеком, отсутствие шумов/артефактов сжатия/барьеров, видимость ≥8 кадров. Minimum **height of equipment on body area**: helmet/hood/gloves20px, vest50px. Это размер предмета, не человека; нельзя смешать с Bosch96px высоты человека. Таблица даёт59px/m и ~100px высоты объекта для перечисленных разрешений, но неоднозначное название последней колонки не превращаем в точное width×height. Порог не переносится на наш tensor. Смысл: документировать, где измерен размер, отдельно от source resolution.

<a id="s064"></a>
## S064 — Axis XFQ1656 manual [primary manual]

**Поддерживаемые F:** [F078](RAW_FACTS.md#f078). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S03; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Автор Axis Communications; версия страницы **July2026**; URL https://help.axis.com/en-us/axis-xfq1656 . Прочитаны Adjust image: night mode, Reduce motion blur, Maximize details; Analytics and apps → PPE monitoring.

**[F078](RAW_FACTS.md#f078).** Night mode использует visible+nearIR и формирует monochrome image. Против blur manual предлагает более короткую выдержку/больший gain и при необходимости дополнительный свет; gain повышает шум. Для деталей — меньше compression, ценой bitrate/возможного FPS. PPE subsection предупреждает: малый объект может дать как miss, так и false alarm; нестандартная форма каски также даёт false alarm. Численного PPE night recall или универсального пиксельного порога нет. Из этого не следует, что thermal=NIR или что настройка экспозиции гарантирует восстановление PPE.

<a id="s065"></a>
## S065 — Bosch/Keenfinity settings [primary support/manual]

**Поддерживаемые F:** [F079](RAW_FACTS.md#f079). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S04; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Автор Bosch Video Systems / текущий официальный support Keenfinity Group. URL https://knowledge.keenfinity-group.com/video-systems/article/how-to-optimize-camera-settings-for-video-analytic . Дата публикации не установлена; иллюстрация image2022-3-22 не принята за дату статьи. Прочитаны собственно article после длинной навигации, §1–5.

**[F079](RAW_FACTS.md#f079).** Exposure и temporal/spatial denoise могут снижать detail/contrast, создавать motion blur/ghosting; крайний low light может лишить детектор объекта. Важное ограничение переноса: рассматриваемая встроенная Bosch analytics получает изображение **до encoder**; её нечувствительность к compression не относится к нашему серверу, получающему декодированный RTSP. Thermal cameras описаны отдельно и не равны night grayscale. Это механизм/рекомендации производителя, не PPE-сравнительный эксперимент.

<a id="s066"></a>
## S066 — Frigate crop/resize developer report и pinned preprocessing [code + developer claim]

**Поддерживаемые F:** [F080](RAW_FACTS.md#f080). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S05; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Автор ответа NickM-27, **25.06.2026**; https://github.com/blakeblackshear/frigate/discussions/23563 . Прочитан вопрос, accepted answer и replies. **[F080](RAW_FACTS.md#f080):** автор сообщает об увеличении FP при испробованном увеличении слишком маленьких regions; dataset, denominator и численная величина не раскрыты. Это ограничивающий опыт разработчика, не controlled benchmark и не PPE. Поэтому увеличение crop не обещаем как универсальное улучшение.

<a id="s067"></a>
## S067 — Frigate v0.18.2 — crop → tensor preprocessing

**Поддерживаемые F:** [F081](RAW_FACTS.md#f081). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S05-preprocess; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Pinned docs/code: commit `cfa08c56b23d23280c3d0a218e5a43182c97445b` (v0.18.2 по W1 provenance), автор Frigate contributors; дата commit15.10.2026 по W1 metadata. URL https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/docs/docs/frigate/camera_setup.md , строки19–25; code https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/util/object.py , `create_tensor_input`,288–305. Сохранены camera_setup.md, util_object.py. **[F081](RAW_FACTS.md#f081) [code inspection]:** region преобразуется в RGB/BGR/YUV, затем при несовпадении shape resize в model.width×height через INTER_LINEAR. Camera docs объясняют потерю деталей при уменьшении большого region. Это конкретная реализация crop→tensor, не проверка нашей модели.

<a id="s068"></a>
## S068 — конкретная промышленная закупка Oil India [official procurement]

**Поддерживаемые F:** [F082](RAW_FACTS.md#f082). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S06; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Заказчик Oil India Limited, Duliajan, Ministry of Petroleum and Natural Gas. Номер **GEM/2026/B/7902194**, dated **11.08.2026**, услуга PPE and Unsafe Act Detection using Video Analytics. Официальная карточка https://www.oil-india.com/tender-details/124?in_detail=NzBleHVBPT0%3D . Открытая на дату доступа карточка показывает closing12.11.2026 и opening13.11.2026; ранний NIT содержит прежние даты08.09.2026, поэтому не использовать NIT как актуальный календарь.

Оригинальный NIT URL https://www.oil-india.com/download-tender-document?ten_detail=NzBleHVDSEw2RXFyMmdHdQ%3D%3D . Web отверг binary/octet-stream; PowerShell успешно получил8p PDF: [OIL_NIT.pdf](_WORK/SOURCES_W2B/OIL_NIT.pdf), текст OIL_NIT.txt. Прочитаны p1,4–5; p4 hyperlink ведёт к **Scope of Work1786430899.pdf** на GeM: https://bidplus.gem.gov.in/resources/upload_nas/AugQ326/bidding/biddoc/bid-9738605/1786430899.pdf . Полный SoW **не получен**: web inaccessible; PowerShell transfer closed; curl35s timeout. Его clauses ниже читаются в официальных prebid-таблицах, а не объявляются прямым чтением полного SoW.

**[F082](RAW_FACTS.md#f082).** Это уже идентифицированная закупка промышленного клиента, не грант/маркетинг. Но наличие NIT и спецификации не подтверждает award, внедрение, accepted performance либо действующий SLA.

<a id="s069"></a>
## S069 — Oil India pre-bid minutes: самая полезная часть цепочки [official clarification]

**Поддерживаемые F:** [F083](RAW_FACTS.md#f083), [F084](RAW_FACTS.md#f084). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S07; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Автор Oil India Limited. Заголовок **Minutes of Pre-Bid Meeting dated25.08.2026 (GEM/2026/B/7902194)**; опубликовано в официальной карточке **01.10.2026**. URL https://www.oil-india.com/download-tender-document?detail=NzBleHVDck00a3lnMlFxc2tzdVlrTUI0cC92Vg%3D%3D . Получен97p PDF:94 нумерованные содержательные страницы+3 добавочные без извлечённого текста. [OIL_PREBID.pdf](_WORK/SOURCES_W2B/OIL_PREBID.pdf), извлечённый OIL_PREBID.txt. Визуально проверены p12,24,36,79,80,81,82,83; PNG сохранены.

**[F083](RAW_FACTS.md#f083).** p12 row13, p24 rows6–7: quoted SoW7.13 требует90% ideal/80% challenging; ответ заказчика относит оценку к каждому use case и переносит методику в Design с OIL approval. Denominator, FP/FN и temporal matching этим ответом не заданы. p36 row55: SAT/signoff предусмотрены, criteria решат до UAT/SAT. p19 фиксирует вопрос о конфликтующих95% и90/80%; ответ не даёт новой формулы. Это документированная **незавершённая спецификация приёмки**, не95% achieved.

**[F084](RAW_FACTS.md#f084).** p79 row10: участник оспаривает80% вне IR-range; OIL отвечает internal review, а не принимает физическую гарантию. p79–80 row11: small PPE на legacy wide views → joint survey/remediation report; upgrades у OIL. p82 row18: zone analytics только fixed park/approved stable PTZ presets. p83 row22: steam/dust/exhaust/flares оценивать camera-wise с exclusions/calibration; чисел PPE dust recall нет. Утверждение bidder и обязательный ответ OIL различены.

<a id="s070"></a>
## S070 — pinned Frigate caller/lifecycle [code inspection, без исполнения]

**Поддерживаемые F:** [F085](RAW_FACTS.md#f085), [F086](RAW_FACTS.md#f086), [F087](RAW_FACTS.md#f087), [F088](RAW_FACTS.md#f088). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S08; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Единственная версия во всём разборе `cfa08c56b23d23280c3d0a218e5a43182c97445b`. GitHub API rate-limit, затем codeload ZIP успешно скачан; никаких инструкций из репозитория не исполняли. `rg` всего каталога frigate по zone_presence/zone_loitering нашёл записи только в tracked_object.py; сохранён COUNTER_WRITES.txt. Локальные оригиналы имеют настоящую нумерацию с пустыми строками; web text иногда удаляет пустые строки, его номера не использовать как Python line numbers.

Paths/URLs и прочитанные места:

- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/tracked_object.py : init65–68, update130–140, zone186–305, state385–386; local tracked_object.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/camera/state.py : finished307–308; reset310–347; update349–425, removed494–500; local camera_state.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/object_processing.py : queue773–799; cleanup819–830; local object_processing.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/track/norfair_tracker.py : register273–292; deregister312–316; update459–491; synthetic stationary493–507; match509–648; local norfair_tracker.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/frigate/video/detect.py : tracker106; process_frames176+, resolution reset245–260, missing frame287–292, stationary/detection300–434, build438+, queue534–550; local video_detect.py.
- https://github.com/blakeblackshear/frigate/blob/cfa08c56b23d23280c3d0a218e5a43182c97445b/docs/docs/configuration/zones.md : Zone Inertia223–232; local zones.md. Same-commit docs требуют consecutive, поэтому W1 unpinned-doc оговорка здесь устранена для этого утверждения. zone_config.py46 также consecutive.

**[F085](RAW_FACTS.md#f085)–[F088](RAW_FACTS.md#f088).** Подробная собственная ручная трасса и все scope-оговорки в [W2_B.md](_WORK/W2_B.md), K006. Это не runtimebug, не tested defect, не характеристика иных релизов. Lifecycle статически исследован; очередь/активность Norfair и actual event impact ещё проверяются replay [E009](OPEN_QUESTIONS.md#e009).

<a id="s071"></a>
## S071 — Axxon One collection requirements [primary manual/vendor claim]

**Поддерживаемые F:** [F089](RAW_FACTS.md#f089). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-B-S10; сохранённый реестр [_WORK/SOURCES_W2B/EVIDENCE.md](_WORK/SOURCES_W2B/EVIDENCE.md).

Автор Alina Luchkina,09.04.2025, One3.0/3.1; https://docs.axxonsoft.com/confluence/spaces/ONE2025/pages/314536470/Data+collection+requirements+for+neural+network+training . Прочитана общая таблица и PPE subsection. **[F089](RAW_FACTS.md#f089):** требует actual camera/resolution/conditions; для PPE отдельно сказано artificial constant lighting. Рекламные общие90–97% и5–7% не извлекаются как PPE achieved: denominator не определён. Общий custom-training claim night/IR на отраслевой странице не отменяет более узкую спецификацию PPE.

<a id="s072"></a>
## S072 — Domination RGB manual

**Поддерживаемые F:** [F090](RAW_FACTS.md#f090). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S01; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Автор/правообладатель: ООО «ВИПАКС+». **Domination Analytics Service 1.17**, дата документа в прочитанном тексте не установлена. URL: https://vipaks.com/upload/iblock/7d1/ibl4j282dihtz91dyg4rhje484fqhcgs/Руководство_Domination%20Analytics%20Service_1.17_конфигуратор.pdf . Прочитан web PDF body: §8.8, печатные p41–43, parsed lines1124–1193. Это полный связный раздел, не search snippet. Live requests и web screenshot затем дали404; полученный HTML ошибочно распознавался PyMuPDF как28-page HTML document, **он не manual**, удалён. Визуальная проверка этого источника не состоялась. Дополнительный mirror v1.18 (102pages) прочитан только parsed text: https://manuals.plus/m/830afd7a86fb962114bb062cd7de9c416b70e922b0b0a84080b3e7acf6d80579.pdf ; не считать независимым подтверждением.

**Vendor documentation, не измерение:** face front/profile→cigarette near face. Для v1.17: horizontal installation, tilt≤15°, height2–4m, face distance3–8m; no wide-angle/fisheye; resolution≥1920×1080, recommended2592×1944; **optimal linear face size100px**, FPS≥5. Чёткое контрастное изображение, равномерный свет, automatic white balance/other auto settings off. IR camera mode условно допускается при столь же качественном изображении; это не thermal measurement. Рекомендованы одиночные сцены, максимум3 потенциальных людей, известные smoking zones; crowd/постоянное постороннее движение запрещены. Sensitivity default50% — **настройка**, не calibrated probability/accuracy. Повышение чувствительности повышает FP; включение каждого face orientation option добавляет нагрузку. Окно подтверждения, hard-negative test, event denominator и hardware throughput не раскрыты.

<a id="s073"></a>
## S073 — DAHD-YOLO object semantics

**Поддерживаемые F:** [F091](RAW_FACTS.md#f091). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S02; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Jianfei Zhang, Chengwei Jiang. **26.02.2025**, Sensors25(5):1433, DOI10.3390/s25051433. Primary full PDF получен requests200 с publisher asset: https://mdpi-res.com/d_attachment/sensors/sensors-25-01433/article_deploy/sensors-25-01433.pdf ; landing https://www.mdpi.com/1424-8220/25/5/1433 (web429/requests403); PMC recaptcha. Прочитаны introduction, §4.1–4.3.9, conclusion, data availability; visually p13. SHA256653abd2e5b6f853213b3f77e80da89878e67afb124645b8ceee4a85e222762c1.

**Published method/measurement:** единственный GT label — cigarette; AP=mAP именно поэтому.2810 интернет/сетевых изображений, ручная проверка,8:1:1 image split. Временного action window нет. Introduction описывает FP от fingers/pens/railings и включения lips/fingers в cigarette box. Визуальные примеры не дают eat/drink/phone/PPE-adjustment confusion matrix. §4.3.9 «generalization» **переобучает** модели на Kaggle cigarette-butts data и оценивает valid set; это не held-out camera transfer готовой smoking model. На RK3588 опубликованы throughput/latency/quantization результаты, но они не LinQ; FPS и per-image latency различаются при multithreading. Авторы сами ограничивают single-seed статистическую значимость и diversity реальных сцен. Связанного author repo/code/issues в статье не дано, data availability лишь «within article». Не использовать mAP cigarette как smoking-event recall.

<a id="s074"></a>
## S074 — industrial CDPA-Net всё ещё image detector

**Поддерживаемые F:** [F092](RAW_FACTS.md#f092). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S03; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Meng Wang, Mei Li, Chao He. **26.04.2026**, Mathematics14(9):1462, DOI10.3390/math14091462. Primary publisher PDF https://mdpi-res.com/d_attachment/mathematics/mathematics-14-01462/article_deploy/mathematics-14-01462.pdf получен200; landing https://www.mdpi.com/2227-7390/14/9/1462 web429. Прочитаны §3.1, architecture, §4 и conclusion; SHA256285345916744e6d7df0ee12916a32e52dbacd32e58e355b3ad1d5d23ba0f4bcd.

**Published method/measurement:** ICSSD6890 industrial images; VOC annotation **cigarette region**, manual cross-check.9:1 train-validation:test, train-validation further3:1. «Pose-aware» означает learned contour/orientation/spectral cues, не tracked skeleton+temporal action classifier.640×640, RTX4090 listed. Temporal cues/motion degradation оставлены future work. Нет camera-disjoint split, event FP/h, explicit eat/drink/phone/adjustPPE negatives или сопоставления object-only с gesture-only в одинаковых условиях. Это свежий industrial object route, а не закрытие K002 matched comparison. Не переносить headline FPS на LinQ и не считать слово pose proof of action recognition.

<a id="s075"></a>
## S075 — pinned object+temporal code, отрицательная проверка

**Поддерживаемые F:** [F093](RAW_FACTS.md#f093). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S04; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Автор handle **Promenade258**. Repository https://github.com/Promenade258/Multidimensional-Smoking-Detection . HEAD получен git ls-remote: **9e70e3fe7816a305187621c4443953842d1e3f7e**, commit patch Date21.06.2026 08:29:40+08:00. Прочитаны README, весь main.py, open issues(0): https://github.com/Promenade258/Multidimensional-Smoking-Detection/issues . Pinned source https://raw.githubusercontent.com/Promenade258/Multidimensional-Smoking-Detection/9e70e3fe7816a305187621c4443953842d1e3f7e/main.py . Локаторы по нормализованным splitlines: constants23–32, global deque114, sampling162, first boxes212–214, history268–269, score290+. API metadata endpoint не дал sha; pin получен git, дата из patch.

**Code inspection, без запуска/не paper validation:** every3rd frame: YOLO cigarette+mouth на width640 и MediaPipe Hands на оригинале; max2 hands.90px distances;20 processed observations, threshold8 hand-near-mouth. История глобальна, mouth/cigarette выбираются `[0]`, person ownership/tracks нет. Score: cigarette0.5, coexistence1, joint proximity2.5, history1; smoking≥2. Поэтому contemporaneous object+mouth плюс история может подтвердить без текущей hand-cigarette spatial relation. Исторический сигнал не time-invariant:20 processed observations≈60 source frames, не20 source frames; wallclock зависит от FPS. README не даёт held-out test/paired ablation, error denominator или measured latency. Название No Smoking при missing mouth/hand не следует копировать в нашу триаду. Это конкретное предупреждение о реализации fusion, не установленный runtime bug и не доказательство бесполезности temporal cue.

<a id="s076"></a>
## S076 — HDS-YOLOv5 fulltext

**Поддерживаемые F:** [F094](RAW_FACTS.md#f094). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S05; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Mingju Chen, Zhongxiao Lan, Zhengxu Duan, Sihang Yi, Qin Su. **25.07.2023**, MBE20(8):15476–15495, DOI10.3934/mbe.2023691. Primary PDF https://www.aimspress.com/aimspress-data/mbe/2023/8/PDF/mbe-20-08-691.pdf получен requests200,20,500,035bytes (web refused size). Metadata https://www.aimspress.com/article/doi/10.3934/mbe.2023691 . Прочитан fulltext, особенно §4.1–4.4/Fig9/Table3/Table4/conclusion. Визуально p15486 и15488. SHA2561c52bd3577713ec00040c0167a96c23ad95e304b40c05f0d6f8ff03d920db3c7.

**Published measurement:** пять **exact class names**: `Wrong place`, `Safe`, `Wrong tie`, `Too thin`, `Not closed`. Это hooked-state discrimination, шире presence/used-unused.3378 photos: staged hanging on domestic power tower, Xiaomi11, разные lighting/time/distance/focal lengths + internet. После masking/flips9738, затем8:1:1; group/source-disjoint split до augment не описан.640×640, TITAN XP; mAP50.912, Not closed AP.870; model24FPS (baseline27), Table3/4. LabelImg boxes; operational GT guide для валидности anchor, load-bearing tie, physical gate-lock inspection/measurement не дан. `Not closed` — визуально размеченный класс, не proof of locked gate у каждого Safe. Нельзя утверждать «видео attachment не решают вообще»; можно утверждать «наша camera/GT/physical closure не подтверждены».

Дополнение/история чтения той же цепочки (C-S20); не независимый эксперимент:

Mingju Chen, Zhongxiao Lan, Zhengxu Duan, Sihang Yi, Qin Su. **25.07.2023**, MBE20(8):15476–15495. https://www.aimspress.com/article/doi/10.3934/mbe.2023691 . Открыты publisher metadata/abstract, fulltext не получен. **[F094](RAW_FACTS.md#f094) [author claim only]:** hook status detector HDS-YOLOv5 сообщает91.2%mAP@0.5/24FPS. Не используем эти цифры для выбора: не установлены class definitions, test split и означает ли статус реальную связь с anchor. Это полезная зацепка второй волны, не закрытый ответ.

<a id="s077"></a>
## S077 — первичный temporal fall с явными intentional lying negatives

**Поддерживаемые F:** [F095](RAW_FACTS.md#f095). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S06; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Abderrazak Iazzi, Mohammed Rziza, Rachid Oulad Haj Thami. **26.02.2021**, J.Imaging7(3):42, DOI10.3390/jimaging7030042. Primary PDF https://mdpi-res.com/d_attachment/jimaging/jimaging-07-00042/article_deploy/jimaging-07-00042.pdf получен200; landing https://www.mdpi.com/2313-433X/7/3/42 web429. Прочитаны §3.4/Algorithm2, §4.3.3/Table11, discussion; p11 rendered. SHA256157b2a7b460b313742a49b700a4b4b2cd3d62c04e28fb744579e9d508b67bd78.

**Published method/measurement:** silhouette/SVM posture→abnormal(lay/bend)→floor overlap85%→transition from stand/sit<25frames→inactivity25frames. Это **авторские экспериментальные**, не универсальные thresholds. Floor размечается вручную в первом кадре. Table11:155/159 falls,4FP/136nonfalls; lying2FP/25, bending2FP/20. Исключены короткие клипы без времени на confirmation, first-frame-person/background contamination и occluded falls. Только single person; occlusion/multiperson limitations. Fast recovery отдельным тестом не оценён; по алгоритму отсутствие inactivity gate не даст alarm, даже если transition наблюдался. Разделять transition-event и post-fall immobility endpoint; последнее не определяет все падения.

<a id="s078"></a>
## S078 — RGB motion-stack fall; endpoint errors

**Поддерживаемые F:** [F096](RAW_FACTS.md#f096). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S07; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Adrián Núñez-Marcos, Gorka Azkune, Ignacio Arganda-Carreras. **06.12.2017**, WCМC2017:9474806, DOI10.1155/2017/9474806. https://onlinelibrary.wiley.com/doi/10.1155/2017/9474806 . Прочитаны §3.1–3.3, §4.3–4.4. Author code link https://github.com/AdrianNunez/Fall-Detection-with-CNNs-and-Optical-Flow — только ссылка, код в W2 не аудирован.

**Published method/error analysis:** TV-L1 optical flow horizontal+vertical, VGG16 input224×224×20:10 flow frames, sliding step1; transfer ImageNet→UCF101→fall. URFD/FDD5fold, Multicam leave-camera-out, balanced folds. Ошибки оцениваются по overlapping **10-frame stacks**, не alarms/hour: slow bending→lying14.06% анализированных FP stacks, pre/postfall labeling mismatch51.41%. Редкие falls from knees/quadruped/topview и blank flow at distance — documented failure types. Не требует post-fall immobility как отдельного universal gate; fast recovery performance всё равно не опубликована. Это альтернативная temporal formulation и предупреждение о boundary GT/stack vs event metrics, не ready industrial fall model.

<a id="s079"></a>
## S079 — прямой YOLO/VLM CCTV paper, но не reject-only verifier

**Поддерживаемые F:** [F097](RAW_FACTS.md#f097). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S08; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Jongeun Kim, Yejin Lee, Dongsik Yoon, Chansung Jung, Gunhee Lee, HDC LABS. ICLR workshop28.04.2025; PMLR296 published12.08.2025. https://proceedings.mlr.press/v296/kim25a.html ; primary PDF https://raw.githubusercontent.com/mlresearch/v296/main/assets/kim25a/kim25a.pdf получен requests200. Прочитаны все12pages; visually p4 tables. SHA2564c5467f8da721cd8a470b58c658b8bebcb6b87a26352bb093b9aa7fa2f036d5d.

**Published measurement:** underground/indoor car-park CCTV. AlgorithmC.4 feeds **each frame** to Florence2; prompt asks whether smoke or fire exists; positive VLM lowers YOLO threshold.5→.3, else.5; alert additionally VLM-validated. Florence2large fp16, checkpoint revision и evaluation GPU не установлены; TableC.1 latency.28s/2.3GB, deployment4FPS and RTSP/upload1.6×offline overhead. Test1081 images, mixed real/synthetic, group-camera heldout не заявлен. YOLOv8s precision fire.843→.838, smoke.944→.931; recall.835→.904/.833→.885. Это **recall gain + precision loss**, не доказанное снижение FA. Нет per-candidate paired FP rescue/TP loss/event confusion matrix. Definitions B.2 matching GT на object-absent images не полностью разъясняют negative accounting. Не смешивать adaptive-threshold classification table с чистым detector→reject verifier.

<a id="s080"></a>
## S080 — ближайшая industrial alarm-recheck публикация, доступ только abstract

**Поддерживаемые F:** [F098](RAW_FACTS.md#f098). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S09; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

Guo Jing(郭京), Li Jun, Gao Lin, Wang Lin, Zhou Junbo, Wang Mingkun, Wang Xiaoyu, Zhang Xianrong; Xi'an Thermal Power Research Institute. **25.08.2026**, Thermal Power Generation, DOI10.19666/j.rlfd.202605095. https://rlfd.cbpt.cnki.net/portal/journal/portal/client/paper/6c11b23634725f0d601039b8e611da01 . Открыты metadata, Chinese+English abstracts и references; body требует cnki.net, fulltext **не получен**.

**Author abstract claim:** high-recall detector→VLM semantic recheck, helmet/uniform/smoke/flame,1068 on-site alarm images,3domestic VLM, four prompt stages; terminal alarm volume−33.6%, false-alarm share31.9→12.5%. Эта прямая промышленная зацепка опровергает утверждение «подобных исследований нет». Model/version/prompt exact text, split, paired TP loss/FP rescue, hardware/latency/event denominator недоступны. Числа не подтверждают coverage preservation и не должны стать KPI нашего verifier.

<a id="s081"></a>
## S081 — operational alert verification trace NVIDIA

**Поддерживаемые F:** [F099](RAW_FACTS.md#f099). **Доступ:**2026-10-23 (+03:00). **Происхождение:** W2-C-S10; сохранённый реестр [_WORK/SOURCES_W2C/EVIDENCE.md](_WORK/SOURCES_W2C/EVIDENCE.md).

NVIDIA VSS documentation **v3.3.0**, publication date not established; accessed23.10.2026. https://docs.nvidia.com/vss/vision-agent/agent-workflows/alert-verification ; old latest URL redirected into modern documentation. Прочитаны workflow/deployment/known issues. https://docs.nvidia.com/vss/vision-agent/agent-workflows/industry-specific-examples/warehouse-operations-blueprint/operations-monitoring-troubleshooting-faq-known-limitations/accuracy-performance-benchmarks — прочитана benchmark scope.

**Primary developer doc, не independent measurement:** object detection/tracking+behavior analytics produce candidate alerts; VLM sees associated clips sporadically. Short clips and model/config can impair accuracy; remote timeout default5s may need increase. Known parser failure: semantically valid `rejected` verdict may fail raw A/B or Yes/No schema and persist as verification-failed. Upstream restart can stop new alerts. Warehouse benchmark page points to Sparse4D/latency; no paired alert-rescue table there. Это подтверждённый implementation workflow и failure trace, но statement «reduce FP» остаётся vendor intent; наша net benefit не измерена.

## Недоступное и partial-read — предел реестра

Полные статусы сохранены в карточках и журналах: [A](_WORK/SOURCES_A/SEARCH_LOG.md), [B](_WORK/SOURCES_B/SEARCH_LOG.md), [C](_WORK/SOURCES_C/EVIDENCE.md), [W2A](_WORK/SOURCES_W2A/SEARCH_LOG.md), [W2B](_WORK/SOURCES_W2B/SEARCH_LOG.md), [W2C](_WORK/SOURCES_W2C/SEARCH_LOG.md).

- ITV RegistryKeys: прочитаны metadata/оглавление, целевые VMDA таблицы не получены; `VMDA.oneAlarmPerTrack`, `LongInZoneTimeout2`, `report_frequency` только leads. Snippet defaults1/10sec/3000ms не факты.
- CHV paper полный текст429; авторский pinned README прочитан. Pictor full paper/downstream A1 tree не прочитаны; decode.py не подтверждает весь relationship алгоритм.
- N95 PPE-CLS abstract-only; FMR-DB institutional abstract-only; predecessor gas-mask Faster R-CNN restricted; данные6134/15scenes из поискового индекса не принимаются fulltext.
- Industrial alarm-recheck Guo2026: abstracts прочитаны, fulltext CNKI не получен. Публикационные числа остаются author claims без paired error audit.
- Oil India NIT и prebid получены; полный Scope of Work1786430899.pdf по извлечённому hyperlink не получен. Цитаты SoW — из официальных minutes; signed SAT/UAT/achieved protocol не получен.
- Domination1.17: §8.8 parsed primary manual прочитан; live bytes/screenshot404, локальная visual QA не состоялась; mirror1.18 — та же цепочка. Ранние W1 snippets заменены этим более сильным, но ограниченным чтением.
- ACM DOI10.1145/3511176.3511194 smoking fusion403; matched object/gesture/event benchmark не получен.
- OSHA403, MAFA403, ряд PMC recaptcha/MDPI429 и отдельные patent/model leads перечислены в журналах. Отказ конкретного инструмента не доказательство отсутствия документа. Домыслы из snippets не включены как сведения полного источника.

Сборщик не выполнял повторных сетевых запросов. Точный незакрытый остаток и дальнейший способ получения — [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
