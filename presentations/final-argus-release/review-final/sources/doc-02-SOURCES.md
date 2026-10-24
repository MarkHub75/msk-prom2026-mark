# Источники утверждений и границы готовности

Git fetch выполнен перед работой. Снимки источников зафиксированы: 2026-10-24T17:32:39.558066+03:00 МСК. Реальные модели иLinQ в этой сессии не запускались.

## Проверенные ветки

- `main`: `f6b5358afee60d1190f5b5e9decc77292b9087c9`
- `front/final`: `a5e43affea9d87fc9049dcf2b4a1ed670fb85a03`
- `matvey_cv`: `53992b3aaa7b89cf65062f343a1e2d776c7c3d2a`

## Технические факты

| Утверждение | Основание | Ограничение |
|---|---|---|
| YOLOv8n иYOLOv8n-pose исполнялись наLinQTPU | s03: LINQ_CONTRACT §§4–6 | Раздельные аппаратные испытания; не стабильный совместный продуктовый pipeline |
| Детектор:≈21кадр/с на записи1280×720 | s04:400/400frames,wall_s19.09,throughput_fps20.95,inflight8,total31.0; s03:размеркадра | Неalertlatency,неchiptime,неполнаяdet+poseскорость |
| Recall0.91/IoU0.93 | s03:сопоставлениеTPU иCPUFP32 после квантования | Неprecision/recall производственных нарушений; исходная модель служит reference |
| CPU-режим предусмотрен | main:src/safewatch/inference/local.py,снимокcpu | Замер18FPS не найден и исключён; новыхCPUвидеопрогонов здесь нет |
| Собственные каска/поза скомпилированы и имелиTPUисполнение | s19:EVAL_REPORT,исторические correlatedcaptures; s21handoff | Новаяпоставкаs22:new_linq_execution/remote_placement NOT_RUN,qualityNOT_EVALUATED. Не выдавать прошлые запросы за новый установленный релиз |
| Восемь групп имеют правила-прототипы | s19,s20:одинобщийobservation/tracking/temporal/evidencepipeline иsyntheticacceptance | Не8обученных нейродетекторов и не8сценариев с принятым промышленным качеством |
|352тестаbackend | s02:progress.md,итогночи/R15 наmain | Сохранённыйотчёт; не новыйpytestзапуск этой сессии. Старые25vitestmain не смешиваются с69новогоfrontend |
|69тестовfrontend PASS | evidence/frontend-tests.json иfrontend-provenance.json; изолированная копияfront/final@a5e43aff | Первоеокружение не содержалоlucide-react:исходныйнеуспешныйreport сохранён;послеnpmci все69PASS,кодне менялся |
|45с автопередача красного безрешения оператора | s05:enabledtrue,timeout45,tick500ms; s06:services.escalation_tick | Конфигурация и код,неподтверждённыйзамер45.2с. Это не обязательный переходжёлтого вкрасное |
| Один эпизод ведёт одну карточку тревоги | s01/s06:эпизоды и события обновляются | Эскалация и передача могут отправлять обновления/уведомления; не обещание одного сетевого сообщения навесьинцидент |
| «Нет наблюдения» видимо | Настоящий01скрин; OperatorDepth.test.tsx,прошедшийновыйfrontendнабор | Не гарантия нулевыхпропусков; потеряканала не считается безопасностью |
| Журнал,печатныйPDF,аналитика,зоны,калибровка,правила | front/final:s10–s17 плюс пользовательскиеснимки | Демоданные не являютсяindustrialmetrics; PDFчерезпечатныйпуть,трендлинейный,неAIforecast |

## Рассказ и неподтверждённые обещания

Слайды2–3 формулируют продуктовую задачу и ценность без измеренногоэкономическогоэффекта. Пятьролей и интерфейсы подтверждены кодом/присланными изображениями. Слайд11явно помечаетпилот,on-premрядомсLinQ иAPI-поставку какплан/гипотезу; текущийдоступкLinQ удалённый,локальнаяпоставкаоборудования не подтверждена. Цены,ROI,снижение травматизма,сроки,автоматическаяостановкастанков инепроведённыйзаводскойпилот не заявлены.

## Что обновилось послеfetch

- main:f6b5358a уточняет контрактподключенияML; R15долги иtimeoutобщегоLinQ остаются. Текущийstatus не выводим изстаройматрицыS0–S10/S0–S11.
- front/final:a5e43aff,новыеэкраны/общийskin и подписьмастера«Принятыемеры». Свежийнабор69тестовпроверенпослеустановкизависимостейизегоlockfile.
- matvey_cv:53992b3a содержит восемьпрограммныхпрототипов и новуюпоставкумоделейсABI/handoff. Наличиеэтойпоставки не означает новогоLinQразмещения,новогопрогонаилиindustrialquality. Историческоеживоеисполнение собственныхмоделей сохранено какотдельныйфакт.

## Что исключено

-18кадр/сCPU и45.2сэскалации: отсутствуютпроверяемыезамеры; пользовательсообщил,чтоисточникемунезвестен. Не восстановлены догадкой.
- Точность91% на производстве,положительнаяприёмкавсех8сценариев,нулевыеложные,обещанныйэффект/окупаемость.
- СравнительноепревосходствонадIVACV илидругимконкурентом:исследование/сопоставимыезамеры отсутствуют.
- НоваяполнаяLinQинтеграция,новыйуспешныйпрогонновойпоставки,чистоеdeviceвремя изнедостоверногополяworker.

## Изображения: происхождение и выбор

Архивпользователя: `/mnt/d/templates/msk-promhack/msk-prom2026-mark/Downloads (2).zip`; SHA256 `e8902c73624c98eebcb4ba6bf2e5c3887f8f2a31aecd5b5f89e4b39369d31159`. Вложенныеzip распакованы какданные; никакиескриптыизархива не запускались.

assets/screens содержит19оригинальныхPNG иисходныйsheet.jpg изargus-screens.zip. assets/stills содержит8заводскихPNG изargus-trailer-kit.zip/stills. READMEархива прямо указываетChatGPTImages,24октября,синтетическиекадры1280×720; рамкидляпадения/бега —ручные. Впрезентацииониневыдаютсяза реальнуюкамерузавода. Ихноваягенерация не требовалась; мокапы/выноски/типографика выполненыдетерминированно.

НаUIслайдах видна demo-маркировка.02/03/05/06/08 — повествовательнаяцепочка изнесколькихдемосостояний,неодинзамерпродолжительного события.03-takeover-red.png относитсякbackend/fake;05–08 — кdemo/mockedсостояниям.03-takeover-red-mock.png и04-red-event-card.png содержат501 видеометода;онисохраненывисточниках,ноневыбраныкакдоказательствореализованноговидео.04-red-event-card-backend.png показываетрасхождениерамки/сцены инеиспользуетсядляподтверждениякачества. На12использованреальный08journal и07masterresolved. Ошибки инадписивсамихисходныхскриншотахнеретушировались. Статусготовностиограничендемо-циклом;живойruntimeэтойветкинеобъявлялсяпровереннымпооднимкартинкам.

Кадр13-camera-live изучен в контексте настройки, но отдельное второе похожее изображение не добавлено; основной14 показываетзоны,15калибровку,12матрицуправил. На6реальные10/11показаныполностью,09добавленкакфрагментотчёта. Всеcrop ипозицииактивов: evidence/composition.json.

## Полный реестр Git-источников

| ID | Коммит/путь | Снимок |
|---|---|---|
| s01 | `f6b5358a:tech.md` | [research/main__tech.md.excerpt.txt](research/main__tech.md.excerpt.txt) |
| s02 | `f6b5358a:progress.md` | [research/main__progress.md.excerpt.txt](research/main__progress.md.excerpt.txt) |
| s03 | `f6b5358a:docs/linq/LINQ_CONTRACT.md` | [research/main__docs__linq__LINQ_CONTRACT.md.excerpt.txt](research/main__docs__linq__LINQ_CONTRACT.md.excerpt.txt) |
| s04 | `f6b5358a:results/linq_smoke/synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json` | [research/main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json](research/main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json) |
| s05 | `f6b5358a:config/default.yaml` | [research/main__config__default.yaml.excerpt.txt](research/main__config__default.yaml.excerpt.txt) |
| s06 | `f6b5358a:src/safewatch/services.py` | [research/main__src__safewatch__services.py.excerpt.txt](research/main__src__safewatch__services.py.excerpt.txt) |
| s07 | `f6b5358a:docs/ML_INTEGRATION.md` | [research/main__docs__ML_INTEGRATION.md](research/main__docs__ML_INTEGRATION.md) |
| s08 | `f6b5358a:contract/openapi.json` | [research/main__contract__openapi.json](research/main__contract__openapi.json) |
| s09 | `f6b5358a:contract/ws.schema.json` | [research/main__contract__ws.schema.json](research/main__contract__ws.schema.json) |
| s10 | `a5e43aff:frontend/src/features/Stats.tsx` | [research/front-final__frontend__src__features__Stats.tsx](research/front-final__frontend__src__features__Stats.tsx) |
| s11 | `a5e43aff:frontend/src/features/ManagementStats.tsx` | [research/front-final__frontend__src__features__ManagementStats.tsx](research/front-final__frontend__src__features__ManagementStats.tsx) |
| s12 | `a5e43aff:frontend/src/features/CameraSetup.tsx` | [research/front-final__frontend__src__features__CameraSetup.tsx](research/front-final__frontend__src__features__CameraSetup.tsx) |
| s13 | `a5e43aff:frontend/src/features/Rules.tsx` | [research/front-final__frontend__src__features__Rules.tsx](research/front-final__frontend__src__features__Rules.tsx) |
| s14 | `a5e43aff:frontend/src/features/Incident.tsx` | [research/front-final__frontend__src__features__Incident.tsx](research/front-final__frontend__src__features__Incident.tsx) |
| s15 | `a5e43aff:frontend/src/features/Master.tsx` | [research/front-final__frontend__src__features__Master.tsx](research/front-final__frontend__src__features__Master.tsx) |
| s16 | `a5e43aff:frontend/src/features/Journal.tsx` | [research/front-final__frontend__src__features__Journal.tsx](research/front-final__frontend__src__features__Journal.tsx) |
| s17 | `a5e43aff:frontend/src/features/Report.tsx` | [research/front-final__frontend__src__features__Report.tsx](research/front-final__frontend__src__features__Report.tsx) |
| s18 | `a5e43aff:frontend/src/styles/ds.css` | [research/front-final__frontend__src__styles__ds.css.excerpt.txt](research/front-final__frontend__src__styles__ds.css.excerpt.txt) |
| s19 | `53992b3a:ml/EVAL_REPORT.md` | [research/matvey_cv__ml__EVAL_REPORT.md](research/matvey_cv__ml__EVAL_REPORT.md) |
| s20 | `53992b3a:ml/SCENARIO_COVERAGE.md` | [research/matvey_cv__ml__SCENARIO_COVERAGE.md](research/matvey_cv__ml__SCENARIO_COVERAGE.md) |
| s21 | `53992b3a:docs/ML_HANDOFF_MATVEY.md` | [research/matvey_cv__docs__ML_HANDOFF_MATVEY.md](research/matvey_cv__docs__ML_HANDOFF_MATVEY.md) |
| s22 | `53992b3a:ml/safewatch.delivery.json` | [research/matvey_cv__ml__safewatch.delivery.json](research/matvey_cv__ml__safewatch.delivery.json) |

Хеши,строки/диапазоны,размерыизображений ивложенныепути: [source-index.json](research/source-index.json). Полныеисполняемыепроверки: scripts/audit.py. Пользовательскиерешения обименах/бренде: research/USER_DECISIONS.md. Хеши подтверждаютбайты; смысловуютрактовкуограничений фиксируетэтотдокументи заметкидокладчика.

## Утверждения по сценам

### 01. Видеоконтроль промышленной безопасности

- Видеоконтроль с полным циклом реакции. Источники: user, s01. Демо и отдельные аппаратные результаты, не промышленный пилот.

### 02. Камеры есть. Реакция не гарантирована.

- Камер недостаточно без внимания, ответственного и журнала мер. Источники: user, s01. Без внешней статистики или неподтверждённого числа экранов.

### 03. От опасности — к подтверждённым мерам.

- Видим опасность, поднимаем нужного человека, фиксируем реакцию. Источники: s01, user. Продуктовая ценность; не измеренный эффект.

### 04. Каждому — свой экран. И своя задача.

- Пять ролевых рабочих мест. Источники: s01, s10, s11, s12, s15, assets. Код и реальные предоставленные снимки; не промышленная эксплуатация.

### 05. Тревога заканчивается действием.

- Жёлтый/красный,мастер,меры,журнал. Источники: s01, s06, s14, s15, s16, assets. Скриншоты из разныхdemo/seed; не один измеренный ML-run.

### 06. Больше событий ≠ больше опасности.

- Журнал,PDF,аналитика; охват и подтверждённые рядом со счётчиками. Источники: s10, s11, s16, s17, assets. Все значения в UI демонстрационные; тренд не нейросетевой прогноз.

### 07. Настроить участок — прямо на кадре.

- Зоны,калибровка и правила на камере доступны через UI. Источники: s12, s13, assets. Штатная настройка без кода; требуется ответственная проверка геометрии.

### 08. Нейросеть видит. Правило решает.

- YOLOv8n/pose исполнялисьTPU; detector recording≈21FPS;recall.91/IoU.93кFP32. Источники: s03, s04. Раздельные hardware tests; throughput записи,не alert/device latency и не industrialquality.
- Восемь программных прототипов и исторические своиHelmet/PoseTPU-runs. Источники: s19, s20, s21, s22. Не восемь обученных/принятых recognizers; новая поставкаhardware/placementNOT_RUN.
- CPU local mode существует. Источники: cpu. 18FPS отсутствует среди подтверждённых результатов и исключено.

### 09. Кадр, обработанный на LinQ TPU

- Real industrial Mendeley frame with saved LinQ status0 output,bbox and17posepoints. Источники: linq-frame, linq-handoff, linq-proof, mendeley. Partial historical capture,not full-video inference or industrial event accuracy. No fresh TPU call in this task.

### 10. Тревога не должна потеряться.

- 352backend по main;69frontend в новом запуске;45с включены как настройка. Источники: s02, s05, s06, front-tests. 352не rerun здесь;45.2не измерено. Программные тесты не измеряют taskaccuracy.
- Нет наблюдения показано явно. Источники: no-observation, assets. Наличие статусаUI,не нулевые пропуски.

### 11. Начинаем с участка. Масштабируем по фактам.

- Предлагаемый пилот→измерения→масштаб;on-prem/API как гипотеза. Источники: user, s08. Без подтверждённых клиентов,цен,ROI,дат и поставленного локальногоTPU.

### 12. Цикл реакции собран. Качество проверяем.

- Стабильный общийTPU,независимое качество и подходящие данные остаются открыты. Источники: s02, s07, s19, s20, s21. Демо-цикл собран,промышленная приёмка не завершена.

### 13. Увидеть — мало. Нужно довести до мер.

- Пять участников команды указаны пользователем. Источники: user. Имена подтверждены; роли и портреты не выдуманы.

## Добавление: слайд9 «Модели исполняются на LinQ TPU»

После технологической схемы добавлен отдельный слайд с ARGUS_linq_tpu_frame0.png. Остальные слайды сдвинуты, итог —13. Изображение предоставил пользователь; source1280×576 целиком масштабирован до1920×864 и центрирован на16:9. Подписи, рамка и17точек не перерисованы, не обрезаны; сверху и снизу нейтральные поля. Текст докладчика сохранён дословно.

Это реальная камера открытого датасета, а не синтетический кадр трейлера и не внедрение команды на заводе. Источник: Oğuzhan Önal; Emre Dandıl (2024), Video Dataset for Safe and Unsafe Behaviours, Mendeley Data,V1. [Официальная страница и лицензия CC BY4.0](https://data.mendeley.com/datasets/xjmtb22pff/1), DOI10.17632/xjmtb22pff.1. Атрибуция включена в заметки PowerPoint и exports/ATTRIBUTION.txt. Страница источника проверена браузингом; данные о промышленной камере и лицензии подтверждены первичным источником.

Свежий matvey_cv@53992b3a: docs/handoffs/EGOR_LINQ_VIDEO_20261024.md и ml/reports/video-handoff-20261024.json подтверждают сохранённые status0,корреляцию запроса/ответа,входные и выходные числовые тензоры для отдельных промышленных кадров. Экспорт частичный, нового TPU-вызова при нём не было. NPZ в этой презентационной сессии локально не переаудированы; сохранены Git-снимки отчёта, его SHA и оригинал предоставленного PNG. Кадр не доказывает обработку всего ролика, промышленную точность или независимую аттестацию чипа. Подпись21FPS на картинке относится к другому baseline-тесту; собственная поза на этом кадре не объявляется realtime.

После дополнительного fetch фронт обновился доa5e43aff (сирена показывает доказательный кадр). На этой версии заново запущены69тестов — всеPASS; исходники экспорта сверены с Git. Пользовательские скриншоты не пересоздавались: они сохраняют собственные состояния и время съёмки. Проверенный main не изменился. Новый LinQ proof-index с датой,хешами и первичной ссылкой: research/linq-proof-index.json.
