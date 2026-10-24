# Источники утверждений и границы готовности

Git fetch выполнен перед работой. Снимки источников зафиксированы: 2026-10-24T16:53:37.642286+03:00 МСК. Реальные модели иLinQ в этой сессии не запускались.

## Проверенные ветки

- `main`: `f6b5358afee60d1190f5b5e9decc77292b9087c9`
- `front/final`: `3f13f1936114f97946bc1bdaac1a420091748a80`
- `matvey_cv`: `39dcc93def2d95cf260c7d980df0a3090e6bbf0f`

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
|69тестовfrontend PASS | evidence/frontend-tests.json иfrontend-provenance.json; изолированная копияfront/final@3f13f193 | Первоеокружение не содержалоlucide-react:исходныйнеуспешныйreport сохранён;послеnpmci все69PASS,кодне менялся |
|45с автопередача красного безрешения оператора | s05:enabledtrue,timeout45,tick500ms; s06:services.escalation_tick | Конфигурация и код,неподтверждённыйзамер45.2с. Это не обязательный переходжёлтого вкрасное |
| Один эпизод ведёт одну карточку тревоги | s01/s06:эпизоды и события обновляются | Эскалация и передача могут отправлять обновления/уведомления; не обещание одного сетевого сообщения навесьинцидент |
| «Нет наблюдения» видимо | Настоящий01скрин; OperatorDepth.test.tsx,прошедшийновыйfrontendнабор | Не гарантия нулевыхпропусков; потеряканала не считается безопасностью |
| Журнал,печатныйPDF,аналитика,зоны,калибровка,правила | front/final:s10–s17 плюс пользовательскиеснимки | Демоданные не являютсяindustrialmetrics; PDFчерезпечатныйпуть,трендлинейный,неAIforecast |

## Рассказ и неподтверждённые обещания

Слайды2–3 формулируют продуктовую задачу и ценность без измеренногоэкономическогоэффекта. Пятьролей и интерфейсы подтверждены кодом/присланными изображениями. Слайд10явно помечаетпилот,on-premрядомсLinQ иAPI-поставку какплан/гипотезу; текущийдоступкLinQ удалённый,локальнаяпоставкаоборудования не подтверждена. Цены,ROI,снижение травматизма,сроки,автоматическаяостановкастанков инепроведённыйзаводскойпилот не заявлены.

## Что обновилось послеfetch

- main:f6b5358a уточняет контрактподключенияML; R15долги иtimeoutобщегоLinQ остаются. Текущийstatus не выводим изстаройматрицыS0–S10/S0–S11.
- front/final:3f13f193,новыеэкраны/общийskin и подписьмастера«Принятыемеры». Свежийнабор69тестовпроверенпослеустановкизависимостейизегоlockfile.
- matvey_cv:39dcc93d содержит восемьпрограммныхпрототипов и новуюпоставкумоделейсABI/handoff. Наличиеэтойпоставки не означает новогоLinQразмещения,новогопрогонаилиindustrialquality. Историческоеживоеисполнение собственныхмоделей сохранено какотдельныйфакт.

## Что исключено

-18кадр/сCPU и45.2сэскалации: отсутствуютпроверяемыезамеры; пользовательсообщил,чтоисточникемунезвестен. Не восстановлены догадкой.
- Точность91% на производстве,положительнаяприёмкавсех8сценариев,нулевыеложные,обещанныйэффект/окупаемость.
- СравнительноепревосходствонадIVACV илидругимконкурентом:исследование/сопоставимыезамеры отсутствуют.
- НоваяполнаяLinQинтеграция,новыйуспешныйпрогонновойпоставки,чистоеdeviceвремя изнедостоверногополяworker.

## Изображения: происхождение и выбор

Архивпользователя: `/mnt/d/templates/msk-promhack/msk-prom2026-mark/Downloads (2).zip`; SHA256 `e8902c73624c98eebcb4ba6bf2e5c3887f8f2a31aecd5b5f89e4b39369d31159`. Вложенныеzip распакованы какданные; никакиескриптыизархива не запускались.

assets/screens содержит19оригинальныхPNG иисходныйsheet.jpg изargus-screens.zip. assets/stills содержит8заводскихPNG изargus-trailer-kit.zip/stills. READMEархива прямо указываетChatGPTImages,24октября,синтетическиекадры1280×720; рамкидляпадения/бега —ручные. Впрезентацииониневыдаютсяза реальнуюкамерузавода. Ихноваягенерация не требовалась; мокапы/выноски/типографика выполненыдетерминированно.

НаUIслайдах видна demo-маркировка.02/03/05/06/08 — повествовательнаяцепочка изнесколькихдемосостояний,неодинзамерпродолжительного события.03-takeover-red.png относитсякbackend/fake;05–08 — кdemo/mockedсостояниям.03-takeover-red-mock.png и04-red-event-card.png содержат501 видеометода;онисохраненывисточниках,ноневыбраныкакдоказательствореализованноговидео.04-red-event-card-backend.png показываетрасхождениерамки/сцены инеиспользуетсядляподтверждениякачества. На11использованреальный08journal и07masterresolved. Ошибки инадписивсамихисходныхскриншотахнеретушировались. Статусготовностиограничендемо-циклом;живойruntimeэтойветкинеобъявлялсяпровереннымпооднимкартинкам.

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
| s10 | `3f13f193:frontend/src/features/Stats.tsx` | [research/front-final__frontend__src__features__Stats.tsx](research/front-final__frontend__src__features__Stats.tsx) |
| s11 | `3f13f193:frontend/src/features/ManagementStats.tsx` | [research/front-final__frontend__src__features__ManagementStats.tsx](research/front-final__frontend__src__features__ManagementStats.tsx) |
| s12 | `3f13f193:frontend/src/features/CameraSetup.tsx` | [research/front-final__frontend__src__features__CameraSetup.tsx](research/front-final__frontend__src__features__CameraSetup.tsx) |
| s13 | `3f13f193:frontend/src/features/Rules.tsx` | [research/front-final__frontend__src__features__Rules.tsx](research/front-final__frontend__src__features__Rules.tsx) |
| s14 | `3f13f193:frontend/src/features/Incident.tsx` | [research/front-final__frontend__src__features__Incident.tsx](research/front-final__frontend__src__features__Incident.tsx) |
| s15 | `3f13f193:frontend/src/features/Master.tsx` | [research/front-final__frontend__src__features__Master.tsx](research/front-final__frontend__src__features__Master.tsx) |
| s16 | `3f13f193:frontend/src/features/Journal.tsx` | [research/front-final__frontend__src__features__Journal.tsx](research/front-final__frontend__src__features__Journal.tsx) |
| s17 | `3f13f193:frontend/src/features/Report.tsx` | [research/front-final__frontend__src__features__Report.tsx](research/front-final__frontend__src__features__Report.tsx) |
| s18 | `3f13f193:frontend/src/styles/ds.css` | [research/front-final__frontend__src__styles__ds.css.excerpt.txt](research/front-final__frontend__src__styles__ds.css.excerpt.txt) |
| s19 | `39dcc93d:ml/EVAL_REPORT.md` | [research/matvey_cv__ml__EVAL_REPORT.md](research/matvey_cv__ml__EVAL_REPORT.md) |
| s20 | `39dcc93d:ml/SCENARIO_COVERAGE.md` | [research/matvey_cv__ml__SCENARIO_COVERAGE.md](research/matvey_cv__ml__SCENARIO_COVERAGE.md) |
| s21 | `39dcc93d:docs/ML_HANDOFF_MATVEY.md` | [research/matvey_cv__docs__ML_HANDOFF_MATVEY.md](research/matvey_cv__docs__ML_HANDOFF_MATVEY.md) |
| s22 | `39dcc93d:ml/safewatch.delivery.json` | [research/matvey_cv__ml__safewatch.delivery.json](research/matvey_cv__ml__safewatch.delivery.json) |

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

### 09. Тревога не должна потеряться.

- 352backend по main;69frontend в новом запуске;45с включены как настройка. Источники: s02, s05, s06, front-tests. 352не rerun здесь;45.2не измерено. Программные тесты не измеряют taskaccuracy.
- Нет наблюдения показано явно. Источники: no-observation, assets. Наличие статусаUI,не нулевые пропуски.

### 10. Начинаем с участка. Масштабируем по фактам.

- Предлагаемый пилот→измерения→масштаб;on-prem/API как гипотеза. Источники: user, s08. Без подтверждённых клиентов,цен,ROI,дат и поставленного локальногоTPU.

### 11. Цикл реакции собран. Качество проверяем.

- Стабильный общийTPU,независимое качество и подходящие данные остаются открыты. Источники: s02, s07, s19, s20, s21. Демо-цикл собран,промышленная приёмка не завершена.

### 12. Увидеть — мало. Нужно довести до мер.

- Пять участников команды указаны пользователем. Источники: user. Имена подтверждены; роли и портреты не выдуманы.
