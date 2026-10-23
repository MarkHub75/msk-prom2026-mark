# W1_A — первичная доказательная база

Дата доступа ко всем источникам: 2026-10-23, Europe/Moscow (+03:00). Это дата исследования, не публикации. Источники действительно открывались web-инструментом; ниже собственные краткие выписки, не копии статей. Репозитории не запускались. Метаданные commits получены непосредственно GitHub REST API /repos/{owner}/{repo}/commits/master. Все численные результаты — опубликованные авторами, не наше измерение. Branch IDs остаются до нормализации сборщиком.

## W1-A-S01 — SHWD

- Автор: njvisionpower, Safety-Helmet-Wearing-Dataset.
- URL README: https://raw.githubusercontent.com/njvisionpower/Safety-Helmet-Wearing-Dataset/c952631dfc352e0defdd54b4785a9be6576451ad/README.md
- URL прочитанного кода: https://raw.githubusercontent.com/njvisionpower/Safety-Helmet-Wearing-Dataset/c952631dfc352e0defdd54b4785a9be6576451ad/train_yolo.py
- Версия: c952631dfc352e0defdd54b4785a9be6576451ad, committer date 2019-12-17T12:39:49Z. Дата создания датасета не установлена по этим файлам.
- Локатор: README Introduction, How to use dataset; train_yolo.py строки 25–27, 103–107.
- W1-A-F01, primary doc + code inspection: 7,581 изображение; 9,044 положительных helmet wearing objects; 111,514 отрицательных normal head objects. Названия классов: hat и person. Здесь person обозначает отрицательный объект головы без каски, не полноразмерную рамку тела. Код подтверждает ровно два class literals. Метрика в скрипте VOC07 mAP при IoU .5.
- Ограничение: изображения/аннотации из архива не скачивались и не инспектировались; README-семантика не доказывает отсутствие ошибок каждой аннотации.
- Смысл: запретить автоматический merge person из SHWD с person COCO/SH17 без явного преобразования геометрии и семантики.

## W1-A-S02 — CHV

- Авторы: Zijian Wang, Yimin Wu, Lichao Yang, Arjun Thirunavukarasu, Colin Evison, Yifan Zhao.
- URL: https://raw.githubusercontent.com/ZijianWang-ZW/PPE_detection/907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d/README.md
- Связанная статья: Fast Personal Protective Equipment Detection for Real Construction Sites Using Deep Learning Approaches, Sensors 21(10),3478,2021, https://doi.org/10.3390/s21103478 (полный текст не получен, 429).
- Версия repo: 907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d, committer 2022-11-03T08:35:47Z.
- Локатор: Introduction, CHV Dataset, Results.
- W1-A-F02, primary artifact: CHV распознаёт person, vest и четыре цвета helmet. Это отдельные предметы, а не четыре состояния одетого человека. Авторы отобрали 1,330 качественных изображений из более 10,000. README сообщает лучший mAP86.55% для YOLOv5x и 52FPS для v5s на TeslaP40/24GB, CPU4cores/8GB.
- Ограничение: README не даёт достаточной методики для межстатейного ранжирования. Нельзя переносить FPS на LinQ. Отбор качественных кадров ограничивает оценку плохого промышленного видео.

## W1-A-S03 — Pictor-PPE

- Авторы метода: Nipun D. Nath, Amir H. Behzadan, Stephanie G. Paal. Статья Automation in Construction112,103085,2020; владелец repo ciber-lab.
- URL: https://raw.githubusercontent.com/ciber-lab/pictor-ppe/8f41c9525bbd1f45245f593c7502a1934eef06fa/README.md
- Код: https://raw.githubusercontent.com/ciber-lab/pictor-ppe/8f41c9525bbd1f45245f593c7502a1934eef06fa/src/yolo3/detect.py
- Версия: 8f41c9525bbd1f45245f593c7502a1934eef06fa, committer 2024-12-18T19:37:18Z.
- Локатор: README Methods/Approaches, Results; detect.py function detection.
- W1-A-F03, primary artifact: A1 детектирует worker/hat/vest и классифицирует отношения; A2 прямо детектирует W/WH/WV/WHV; A3 детектирует worker и классифицирует его crop VGG16/ResNet50/Xception. W означает neither hat nor vest, WH только каска, WV только жилет, WHV оба. Авторы README называют лучшим A2 с72.3%mAP.
- W1-A-F04, code inspection: detect.py — декодирование YOLO и NMS, возвращает рамки/score/class; в этом файле нет доказательства связи PPE–worker. Чтение этого файла не равно проверке полного A1 decision tree.
- Ограничение: полный оригинальный paper и downstream notebooks в этой ветке не прочитаны; нельзя восстановить из README все режимы разметки unknown. Ограничения разметки Pictor критикует S05, это отдельное авторское наблюдение.

## W1-A-S04 — SH17

- Авторы: Hafiz Mughees Ahmad, Afshin Rahimi, University of Windsor.
- URL статьи: https://arxiv.org/html/2407.04590v1 ; версияv1, 2024-07-05.
- YAML: https://raw.githubusercontent.com/ahmadmughees/SH17dataset/2f832c289f9deea063367045ed8230b26e3e7ea9/sh17.yaml
- Repo revision: 2f832c289f9deea063367045ed8230b26e3e7ea9, committer 2024-12-04T15:29:53Z.
- Локаторы прочитаны: III-B/C TableII, IV TablesIII–V, Appendix train/test; YAML names.
- W1-A-F05, primary doc: head допускает любой вид головы; face размечается при видимом носе. Face-mask-medical — медицинская маска, не общий industrial respirator. Предусмотрены расширенные on/off tags; off означает предмет в сцене, но не надет. Glasses имеют safety/vision; earmuffs включают обычные over-ear headphones. YAML17 базовых labels не кодирует tags, называется face-mask и содержит отдельные person/head/face/hands/gloves/helmet.
- W1-A-F06, published measurement: YOLOv9-e на SH17 test: helmet recall67.8%,gloves58.9%,face-mask73.2%. На Pictor mapping трёх классов TableV: helmet recall23.7%,AP50=55.5%; vest всего28instances. IV-A текст all mAP58.8, таблица58.9. Это frame/object metrics, не события.
- Ограничение: on/off presence в статье не доказывает доступность tags в используемом YOLO export; архив не изучен. Лицензии не исследовались. Статья сама не устанавливает пригодность к камерам кейса.

## W1-A-S05 — head keypoint vs boxes/direct person state

- Авторы: Bartosz Wójcik, Mateusz Żarski, Kamil Książek, Jarosław Adam Miszczak, Mirosław Jan Skibniewski.
- URL: https://arxiv.org/html/2106.10944v1 ; v1,2021-06-21.
- Реально прочитано: §3.1 Algorithm1, §3.2 dataset, §4.3, §5 Tables7/9, §6 Fig9.
- W1-A-F07, primary method: person без найденной head keypoint остаётся неопределённым person; при head keypoint проверяется попадание в helmet bbox. Авторы отмечают Pictor-v3, где видимый только ниже пояса человек размечен non-wearer. Это критика авторов, не наш аудит Pictor.
- W1-A-F08, published comparison: dataset7,035, train5,269/test1,766, X101 detector. Table7 AP keypoint=.675, same-detector refitDT=.664, NathDT=.654; APsmall=.211/.222/.222. Table9 keypoint vs same-training FasterRCNN direct wearer/nonwearer: AP=.675/.663, AP50 обе.826, APsmall=.211/.248. Преимущество ограничено метрикой/масштабом.
- W1-A-F09, primary failure evidence: Fig9 — missing helmet, occluded person+helmet, ошибочная keypoint, small scale, partial-person missing keypoint. §6 предостерегает от гражданских negative examples, ведущих к shortcut worker/civilian.
- Ограничение: статья не опубликованный отдельный benchmark crowded ownership; правило не исключает две головы в одной bbox каски. Вv1 GitHub указан placeholder, код не проверен.

## W1-A-S06 — modular pose/crop PPE

- Авторы: Selcuk Anil Karatopak, Deniz Sen, Huawei Türkiye R&D Center.
- URL: https://www.eleco.org.tr/ELECO2023/eleco2023-papers/97.pdf ; ELECO2023, точная дата PDF не указана.
- Локатор: pp2–4 §3.2–3.6, Fig1, Table1; прочитаны эти разделы и setup.
- W1-A-F10, primary method: YOLOv7 pose даёт17keypoints; отдельные crops/CNN для PPE. Для gloves требуются elbow/wrist confidence; руки позади torso отбрасываются. Для glasses back-facing crops не идут в classifier. Fig1 имеет wearing/not-wearing/indecisive. Glove classifier имеет glove/no-glove/undefined.
- W1-A-F11, published measurement: закрытые CCTV данные; split glove90/10, hardhat/vest80/20. Table1 crop-classifier test accuracy hardhat.92/vest.98/glove.86/eyeglass.95; это не end-to-end event recall. Coverage там геометрическая величина, не selective prediction coverage. В формуле/пояснении denominator и толкование вызывают неоднозначность: не переносить его без проверки.
- Ограничение: нет публичных данных для независимой проверки; ошибки crop/pose не сведены в событийную метрику. Порогов видимости как универсальных нет.

## W1-A-S07 — коммерческий интерфейс трёх состояний

- Автор: Amazon Web Services, Rekognition Developer Guide, latest/unpinned, дата публикации не указана.
- URL: https://docs.aws.amazon.com/rekognition/latest/dg/ppe-request-response.html
- Локатор: Understanding the DetectProtectiveEquipment response, BodyParts, CoversBodyPart, Summary; прочитаны.
- W1-A-F12, primary doc: отдельно confidence person, bodypart, item, coverage. CoversBodyPart отсекает предмет рядом, но не доказывает защиту или корректное ношение. Summary разделяет PersonsWithRequiredEquipment, PersonsWithoutRequiredEquipment, PersonsIndeterminate. Последнее включает недостаточную confidence person/bodypart/equipment/coverage относительно MinConfidence. Требование80% в примере — пример API, не рекомендованный промышленный operating point. Документ рекомендует лицо к камере.
- Ограничение: API не запускалось; механизм модели не раскрыт, независимое качество не установлено. Логическая структура пригодна как образец схемы, применение AWS в кейсе не предлагается.

## W1-A-S08 — гранулярность PPE API

- Автор: AWS, latest/unpinned; дата публикации неизвестна.
- URL: https://docs.aws.amazon.com/rekognition/latest/dg/ppe-detection.html
- Локатор: Types of PPE, Summarizing, Notes; прочитан весь основной текст.
- W1-A-F13, primary doc: face cover включает cloth/surgical/N95, но API не возвращает конкретный subtype покрытия. PPE IDs генерируются per-image и не сохраняются между кадрами. Confidence50–100 — шкала сервиса.
- Ограничение/смысл: generic face cover не равен соответствующему респиратору; выдачу per-frame нельзя считать треком сотрудника. Нельзя выдавать score за откалиброванную вероятность события.

## W1-A-S09 — selective classification

- Авторы: Yonatan Geifman, Ran El-Yaniv.
- URL: https://arxiv.org/html/1705.08500v2 ; v2,2017-06-01.
- Локатор: §§2–3 problem setting/risk, §§4–5 confidence/experiments; прочитаны постановка, допущения, summary экспериментов.
- W1-A-F14, original theoretical method: selection g позволяет отказаться; coverage — доля принятых, risk — ошибка на принятых. Статистическая гарантия строится на i.i.d. выборке из того же распределения P. Softmax response/MC-dropout сравниваются на CIFAR/ImageNet, не PPE видео.
- Ограничение/смысл: основание для risk–coverage отчёта и калибровочной выборки. Гарантия не переносится автоматически на соседние кадры, другую камеру/цех или отобранные лучшие кадры. Выбор max confidence сам по себе не верифицированная политика abstention.

## W1-A-S10 — manufacturer respirator instructions

- Автор: 3M, Half Facepiece Respirator6000 Series User Instructions.
- URL: https://multimedia.3m.com/mws/media/96751O/3m-6000-series-half-facepiece-respirator-user-instructions.pdf
- Версия/дата: revision/date в прочитанных разделах не найдены; документ61PDFстраница, датировка поискового индекса не принимается за дату документа.
- Локатор: English printed pp9–11/PDF indices8–10 Fitting Instructions, Donning, User Seal Checks, Fit Testing; Use limitations p3.
- W1-A-F15, primary manual: надевание закрывает рот/нос, регулируются верхние/нижние straps. При каждом надевании выполняется pressure seal check, до выдачи требуется fit testing. Проверка включает ощущения утечки/деформации при вдохе/выдохе; совместимые PPE также участвуют в fit test. Пригодность filter/cartridge зависит от загрязнителя и условий.
- Ограничение: инструкция конкретного семейства, US/Canada/Brazil references; не российская юридическая квалификация. Из обычного CCTV RGB нельзя подтвердить утечки, соответствие фильтра, service life или успешный fit test.

## W1-A-S11 — Macroscop4.7, ограничения и определения

- Автор: Macroscop. URL: https://doc.macroscop.com/analytics/hard-hats/requirements.htm
- Версия4.7; footer Last updated22.10.2026, не утверждается дата первого выпуска.
- Прочитаны: Детектирование (Каска, Жилет, Респиратор, Очки, Перчатки), Размеры объекта, сцена/ракурс.
- W1-A-F16, primary vendor doc: респиратор должен закрывать нижнее/всё лицо, medical masks исключены. Невидимое лицо => наличие/отсутствие respirator/glasses не определяется. Очки на уровне глаз, не лба; поддерживается цветная оправа/полностью цветные очки. Жилет определяется как любая надетая одежда без рукавов, любого цвета.
- W1-A-F17, primary vendor conditions: head>=60×60px для respirator/glasses/shield/earmuffs; hands>=40×40px gloves; vest>=60×60px; person>=80pxheight и>=2%width/8%height кадра. Gloves: видимые кисти, без посторонних предметов/кармана,>=10сек в кадре; одна видимая перчатка может дать presence, но две видимые руки с одной голой=>absence. Camera downward<=35°, лицо к камере<=60° для facePPE.
- Ограничение: конкретная модель/версия, не универсальные пределы. Наличие glove на одной видимой руке не доказывает обе перчатки. Значение vest не совпадает с certified/high-vis. Не измерялось нами.

## W1-A-S12 — реальный steel plant и отказы

- Авторы: Kyle Toth, Monika Singhal, Dhwanil Chauhan, Jay Polra, Chenn Zhou, Garrett Page, Conrad Fisher.
- URL: https://link.springer.com/article/10.1007/s40192-026-00461-6
- Название: A Dual-Model Approach to Industrial Safety: Computer Vision for PPE Compliance and Hazard-Zone Monitoring in Steel Production; опубликовано12.05.2026.
- Прочитаны Methodology/Data/ModelIntegration/Testing, Results и Limitations.
- W1-A-F18, primary deployment study: personYOLOv8m→workerROI→PPEYOLOv8m, четыре PPE, steel footage SteelDynamics/CharterSteel. Неоднозначные экземпляры исключались при разметке. §SystemLimitations: gloves полностью не идентифицированы более чем в20% low-light frames; no temporal history/no worker tracking, framewise inconsistencies дают ложные non-compliance. Published F1.93PPE не устраняет этот отказ. Детальные operational metrics confidential.
- W1-A-F19, published illustrative comparison: §Results сравнение single/multi-stage авторы называют иллюстративным, не standalone benchmark. Personbbox contains all PPE используется как compliance logic; это не доказательство bodypart ownership.
- Ограничение: ограниченный набор ~10industry clips, plant-specific bias; нет открытых часов наблюдений/FA perhour. Не основание обещать такой F1 в кейсе.

## W1-A-S13 — head-mounted industrial PPE

- Авторы: Velibor Isailovic, Aleksandar Peulic, Marko Djapan, Marija Savkovic, Arso M. Vukicevic.
- URL: https://www.nature.com/articles/s41598-022-20282-9?code=1&error=cookies_not_supported
- Canonical: https://doi.org/10.1038/s41598-022-20282-9 ; опубликовано29.09.2022, ScientificReports12,16347.
- Прочитаны Materials/Methods, Experiments, Discussion, Conclusion. Table2 separate link не получен; численные значения ниже из Discussion, не реконструированная таблица.
- W1-A-F20, published measurement:12,682image/12PPE, public+author images; head crops, random70/15/15split. Три detectors FasterRCNN/MobileNetV2SSD/YOLOv5. Meanprecision по трём архитектурам clothmask=.570, cartridge respirator=.540; surgical/N95 входят в группы >.9. Checkpoint setting предложен авторами. Собственная часть данных закрыта.
- W1-A-F21, methodological caveat/local reading: в §Experiments изложение IoU TP/FN не описывает полноценный обычный unmatched-prediction FP accounting; не считать эти precision числа сертификатом operation/event качества. Статья также по ошибке называет FasterRCNN single-stage. Ввиду этих оговорок источник полезен для относительной трудности классов и постановки, не эталон метрик.

## W1-A-S14 — best view патент

- Авторы/изобретатели: 郑小玉, 刘自强; assignee PowerChina Chengdu Engineering Co Ltd (GooglePatentsmetadata).
- URL: https://patents.google.com/patent/CN110414400A/en
- Filing22.07.2019, publication05.11.2019; прочитаны Abstract, description method, claims; английский машинный перевод.
- W1-A-F22, primary patent disclosure: face detection/tracking→face landmarks/PnP→выбор лучшего Euler-angle helmet region→classifier. В description best angle по трём направлениям<=15°. Это описанная конструкция quality-based frame selection.
- Ограничение: патентные заявления о>99% без достаточного benchmark не принимаются как measurement. Face dependence ограничивает спины/окклюзию. Не значит, что надо ждать фронтального лица для каски, видимой сзади.

## W1-A-S15 — pose-anchor патент

- Авторы/изобретатели: 樊思萌,赵东山,胡志坤,朱言庆; Zhiyang Innovation Technology Co Ltd.
- URL: https://patents.google.com/patent/CN113537019A/en
- Filing07.07.2021, publication22.10.2021; B version grant23.07.2024 не исследована. Прочитаны Abstract, Background и disclosure; машинный перевод.
- W1-A-F23, primary patent disclosure: AlphaPose nose+shoulders строят headROI, SSD классифицирует каску. Background называет наклон/приседание/лежачую позу трудными для прежних схем.
- Ограничение: не независимый тест и не доказательство улучшения; наличие носа/плеч нужно проверять. Полезен как практический след каскада, но не как причина усложнять MVP.

## W1-A-S16 — потребительское ТЗ «Видеоконтроллер»

- Организация-публикатор: АНО «Агентство по технологическому развитию», домен itdf.ru.com; потребитель по§1.3 ООО«Вега-Абсолют». Авторы/дата утверждения в прочитанном документе не указаны.
- URL: https://www.itdf.ru.com/208/contracts/391/%D0%A2%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5.pdf
- Прочитаны титульная часть/§1–3, printedp5Table4, §10/11;13PDFpages. Основание ППРФ208от18.02.2022 — не дата этогоТЗ и не ID закупки.
- W1-A-F24, primary requirement: Таблица4 требует наличие каски/шлема на голове>=95%,очков на лице>=98%,щитка/маски на лице>=98%,перчаток на руках>=90%;1–50зон/кадр. Это требования, не достигнутые результаты. Формулировки bodypart-specific, не presence-anywhere.
- Ограничение: термин«достоверность» без достаточно явного denominator/scene; программа испытаний должна разрабатываться отдельным этапом. Протокол приёмки с результатами не получен. Документ грантового конкурса на КД, не установленная закупка системы безопасности. Подтверждает требования к отношениям, не реализуемость цифр.

## W1-A-S17 — новая классификация N95/goggles: только abstract

- Авторы: Peiran Liu,Xingjian Ma,Haozhi Chen,Denny Yu.
- URL: https://pubmed.ncbi.nlm.nih.gov/42246247/
- Название Automated Assessment of PPE Compliance with Fast Lightweight Deep Learning Based Computer Vision, 05.06.2026, DOI10.1080/24725838.2026.2671785.
- Прочитан только Abstract/metadata. Fulltext не прочитан.
- W1-A-F25, author reported abstract: entry checkpoint; PPE-CLS/PPE-BQZEL; N95/goggles;2.8Mparams; accuracy.91/.94 vs ViT.88/.90 и до5×faster. Spatial awareness+state-space layer.
- Ограничение: это не дальнее surveillance исследование, нет в прочитанном camera/occlusion/FAhours/детальной экспорта информации. Зацепка для соседнего model_stack/training, не готовый выбор и не подтверждение LinQ.
