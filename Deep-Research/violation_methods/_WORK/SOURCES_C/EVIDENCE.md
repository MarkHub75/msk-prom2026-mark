# W1_C: сохранённые первичные доказательства

Доступ: 2026-10-23, примерно 06:00–06:05 Europe/Moscow (+03:00). Дата доступа не является датой публикации. Только выписки в собственном пересказе; полный текст статей не сохраняется. Обозначения C-Sxx / C-Fxx сохраняются при сборке. Чтение через web и, для Bosch и Lim, локальное извлечение PDF. Ничего не запускалось как модель.

## C-S01 — Bosch VCA 6.30 Releaseletter

Автор: Bosch Security Systems B.V., BT-VS/MKP-AIC Product Management, Hildesheim. Документ датирован **16.10.2024**, название в PDF — Bosch Releaseletter VCA 6.30. URL: https://cdn.commerce.boschsecurity.com/public/documents/RL_VCA_Release_Note_enUS_88157155723.pdf . Копия: [bosch-vca630.pdf](bosch-vca630.pdf); визуально проверена страница 5: [BOSCH_PPE_PAGE.png](BOSCH_PPE_PAGE.png). Web не смог разобрать application/octet-stream; urllib получил PDF, PyMuPDF отрисовал p5. Poppler в PATH не найден; использован доступный PyMuPDF.

**C-F01 [primary doc]:** p5, блок PPE Limitations: применимо к CPP14, исключены 3000/multi/corner/panoramic. Детекция/трекинг 7.5 FPS вместо обычных 15; PPE attributes примерно раз в 3 секунды для каждого человека. В аналитическом разрешении 1280×720 или 1024×576 для 8MP-камер: жилет — минимум 48 px **высоты человека**, каска — 96 px. Минимум 200 lx, вертикальные стоящие/идущие люди, PPE обращено к камере, без перекрытий, рекомендуют движение по одному. Полосы жилета должны стать видимыми; белая каска не должна быть пересвечена. Это требования конкретного продукта, не эксперимент на нашей модели.

## C-S02 — Macroscop: PPE requirements

Автор: Macroscop. https://doc.macroscop.com/analytics/hard-hats/requirements.htm . Открыта документация **4.7**, внизу Last updated **22.10.2026**. Первоначальный cached web-result и поздний live-result могут иметь разную навигацию; для фактов использован прочитанный body 4.7. Локаторы: «Видеопоток», «Сцена и расположение камеры», «Респиратор», «Очки», «Размеры объекта».

**C-F02 [primary doc]:** нейросетевые режимы >=3 FPS, HD 1280×720; увеличение выше HD не увеличивает количество/мелкость распознаваемых объектов. Цветное изображение, без существенных compression artifacts; наклон от горизонтали <=35°, угол лица к камере для respirator/glasses/shield <=60°. Для малых лицевых PPE голова >=60×60 px, кисть для перчатки >=40×40; человек >=80 px и >=2% ширины/8% высоты кадра. При невидимом лице presence/absence respirator/glasses **не определяется**. Медицинская маска не относится к респиратору. Эти условия продукта не являются границей информации для любого детектора. Ту же цепочку независимо читал W1_A; не считать вторым независимым источником.

## C-S03 — Macroscop: семантика падения

https://doc.macroscop.com/analytics/fall-detector/overview.htm . Автор Macroscop. Прочитан body и «Примечание», текущая страница Last updated 22.10.2026, навигация 4.7; первый cached result показывал 4.6. **C-F03 [primary doc]:** модуль называет падением лежачее положение человека и прямо исключает определение самого процесса падения. Это предметная оговорка, которую маркетинговое имя скрывает.

## C-S04 — Macroscop: fall requirements

https://doc.macroscop.com/analytics/fall-detector/requirements.htm . Автор Macroscop, docs4.7, Last updated 22.10.2026. Прочитаны разделы «Видеопоток», «Изображение», «Сцена и расположение камеры». **C-F04 [primary doc]:** >=10 FPS; оптимальное HD/FullHD; цвет, стабильное равномерное освещение, без существенных артефактов; человек целиком и >=8% высоты кадра; наклон к горизонтальной поверхности <=35°; исключаются отражающие зеркальные поверхности. Не универсальный FPS для любой fall/action модели.

## C-S05 — Video based human smoking event detection method

Авторы Anna V. Pyataeva, Maria S. Eliseeva. SDM-2021, 24–27.08.2021; pp343–352. https://ceur-ws.org/Vol-3006/40_regular_paper.pdf . Прочитаны pp343–348 и p351/table5; не только abstract.

**C-F05 [published method/measurement]:** Sec2.1 рассматривает последовательность рука к губам → пауза → опускание, зажигание и стряхивание пепла; дым нестабилен по форме/прозрачности и зависит от съёмки. 3D ResNet34, Sec2.3 говорит input16frames, Sec2.4 — 32frames 112×112: явная внутренняя неоднозначность. Experimental section: 70 smoking videos, HMDB51 negatives; тест дополнен леденцом, ручкой во рту, мороженым; split80/20. Table5 сравнивает ResNet/ResNetM на 20 клипах, заявляет улучшение, но не даёт события на камеру-час или industrial external validation. Несогласованное описание negatives (6766 и включение smoking в перечне HMDB51) не позволяет восстановить чистый split. Сохранённые цифры не переносить на цех. Практический смысл: клип и hard negatives обязательны; это слабое основание для оценки production FA.

## C-S06 — CN109598214A

Автор/изобретатель 杨恒 (Yang Heng); original assignee Shenzhen Emo Technology Co Ltd. Публикация **09.04.2019**, priority22.11.2018. https://patents.google.com/patent/CN109598214A/en . Прочитаны metadata, описание S110–S130 и claims1–5; машинный EN-перевод Google Patents.

**C-F06 [patent method, no measured validation]:** локализует рот, ищет светящуюся область, при перекрытии рот–рука ищет её на руке; pose keypoints возможны для определения mouth/hand regions. Отмечает сбои face methods при большом угле/закрытом лице. Не опубликована приёмочная точность метода. В наших условиях сварка, отражения, светодиоды и невидимый тлеющий конец требуют проверки как hard negatives/unknown. Патент доказывает существование постановки, не её качество и не свободу использования.

## C-S07 — TP-LINK 红外测温08—吸烟检测使用指导

Автор TP-LINK视觉安防; дата/версия на странице не установлены. https://security.tp-link.com.cn/service/detail_article_4828.html . Прочитан body «功能介绍/配置流程».

**C-F07 [vendor manual/claim]:** камера использует AI **вместе с температурным обнаружением**; рекомендуемая дистанция smoking detection около5–10m. На момент текста standalone, без push в recorder/APP, возможен alarm output. Дистанция относится к этой тепловой системе, не к любому RGB smoking detector. Конкретная оптика/модель на странице не указана. Пригодно как контрпример: коммерческое «детектирует курение» может требовать другой модальности.

## C-S08 — Lim et al., harness/hook

Jeeyoung Lim, Dae Gyo Jung, Chansik Park, Dae Young Kim. **31.07.2022**, Advances in Civil Engineering,4678479. DOI https://doi.org/10.1155/2022/4678479 ; publisher https://onlinelibrary.wiley.com/doi/10.1155/2022/4678479 . Авторский PDF получен из репозитория Chung-Ang University: https://scholarworks.bwise.kr/cau/bitstream/2019.sw.cau/78560/1/Computer%20Vision%20Process%20Development%20regarding%20Worker%27s%20Safety%20Harness%20and%20Hook%20to%20Prevent%20Fall%20Accidents%3B%20Focused%20on%20System%20Scaffolds%20in%20South%20Korea.pdf . Прочитаны p5–10, особенно conclusion p10. После выписки полная статья удалена из служебных материалов по поручению хранить пересказ.

**C-F08 [published observation/limitation]:** процесс различает harness, hook, attachment facility и контекст scaffold/workphase. В sample application p8 worker распознан, hook не найден из-за малого размера. Conclusion p10 повторяет: worker/harness recognized, hook not recognized; систему проверки **connection** ещё нужно создать, в этой работе этого не сделано. Пример/методология не являются доказательством обнаружения пристёгнутого карабина. Аннотация сама по себе могла бы создать обратное впечатление. Наш вывод: наличие harness и близость hook к anchor недостаточны для доказательства механического зацепления/запертого замка.

## C-S09 — YOLO-World paper and pinned developer documentation

Tianheng Cheng et al., CVPR **June2024**, pp16901–16911. https://openaccess.thecvf.com/content/CVPR2024/html/Cheng_YOLO-World_Real-Time_Open-Vocabulary_Object_Detection_CVPR_2024_paper.html . Прочитан abstract; PDF web403, подробную постановку подтверждает developer doc https://github.com/AILab-CVC/YOLO-World/blob/4f70adbaacf5685bd9ec5bea85f1f91057f6fc0b/docs/reparameterize.md . Commit master SHA получен GitHub API и pinned raw-file прочитан23.10.2026. Это документация, код не запускался.

**C-F09 [primary developer doc]:** embeddings текста можно включить параметрами в голову: final classification становится1×1 convolution, а не transpose/matmul. Doc предусматривает reparameterize head `YOLOWorldHeadModule` и neck `MaxSigmoidCSPLayerWithTwoConv`; подготовить NxD embeddings и новый checkpoint. Словарь выбирается до исполняемого графа; новый словарь требует повторной подготовки артефакта, и на LinQ может потребовать recompilation. Последнее — наш вывод, не подтверждённый LinQ API. Не вся модель становится «без attention» только по этому тексту, и detection не превращается в проверку соблюдения.

## C-S10 — YOLOE

Ao Wang, Lihao Liu, Hui Chen, Zijia Lin, Jungong Han, Guiguang Ding. v1 10.03.2025, **v2 17.10.2025**. https://arxiv.org/html/2503.07465v2 . Прочитаны abstract, introduction, Sec3.1–3.4.

**C-F10 [published method]:** RepRTA text prompts reparameterizes auxiliary network into classification head при inference/transfer; авторы называют полученную архитектуру идентичной YOLO. Visual prompts SAVPE и prompt-free LRPC — отдельные механизмы, не следуют автоматически из fixed text graph. «Zero overhead» относится к сравнению этой текстовой схемы с YOLO, не к нулевой стоимости whole pipeline, LinQ compilation или новой категории без ошибок. Качество промышленных респираторов/сигарет и event FA не установлено.

## C-S11 — Grounding DINO

Shilong Liu et al. v1 09.03.2023, **v5 19.07.2024**. https://arxiv.org/html/2303.05499v5 . Прочитаны abstract, introduction, Sec3 architecture. **C-F11 [published method]:** text-image fusion в feature enhancer, language-guided queries, cross-modality decoder; self/cross-attention. Описание произвольных объектов/атрибутов не означает скомпилированную сменную1×1 голову. Наш вывод: требования к графу и текстовым inputs существенно богаче фиксированного reparameterized vocabulary; возможность LinQ не установлена, запрещать её без ops list нельзя.

## C-S12 — POPE / object hallucination

Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao, Ji-Rong Wen; EMNLP **December2023**, pp292–305. https://aclanthology.org/2023.emnlp-main.20/ ; paper https://aclanthology.org/2023.emnlp-main.20.pdf . Прочитаны abstract/введение PDF и publisher metadata.

**C-F12 [published measurement/limitation]:** LVLM могут утверждать объекты, отсутствующие на изображении; visual instructions и co-occurrence влияют на hallucination. POPE использует polling questions для оценки. Исследование относится к изученным2023 моделям/benchmark, не измеряет current VLM на промышленных тревогах. Наш вывод: положительный ответ verifier не ground truth; проверять paired precision/recall и hallucinated predicates, а не обещать снижение FA по факту добавления VLM.

## C-S13 — SAHI

Fatih Cagatay Akyon, Sinan Onur Altinuc, Alptekin Temizel. ICIP2022, arXiv v5 **24.10.2022**. https://arxiv.org/html/2202.06934v5 . Прочитаны abstract, Sec3 Proposed Approach и Sec4/Table1. **C-F13 [published method/measurement]:** overlapping image patches делают small targets относительно крупнее на входе сети, результаты объединяются; возможно full-image pass. Уточнение после Sec4/Table1: gains 6.8/5.1/5.3 — AP50 в процентных пунктах для FCOS/VFNet/TOOD на VisDrone19 test-dev, SAHI+FI+25% overlap против FI, не smoking/PPE. VisDrone tiles640×640, xView400×400; singleIoU0.5, maxdets500. Наш вывод: кропы помогают сохранить исходные детали при resize, но не восстанавливают отсутствующий сигнал; цена — несколько forward passes, overlap duplicates и merge. Утверждение introductory DORI статьи не принимаем как PPE-норматив; C-S14 точнее разграничивает назначение DORI.

## C-S14 — Axis pixel density white paper

Автор Axis Communications, версия страницы **April2026**. https://whitepapers.axis.com/en-us/pixel-density-based-on-iec-62676-4-2014 . Прочитаны Summary/Operational requirements/Simplified model. **C-F14 [primary vendor explanation of standard]:** 2014 DORI25/63/125/250 px/m описывает человеческое восприятие detection/observation/recognition/identification. Страница явно говорит, что для software analytics применяются другие определения. Свет, оптика, compression также влияют. Это объяснение IEC62676-4:2014, а не установленный действующий на2026 PPE-стандарт; стандарт полностью не читался.

## C-S15 — PTQ4ViT

Zhihang Yuan, Chenhao Xue, Yiqi Chen, Qiang Wu, Guangyu Sun. v1 24.11.2021, **v3 23.06.2024**. https://arxiv.org/html/2111.12293v3 . Прочитаны abstract/introduction/Sec3.2. **C-F15 [published mechanism/measurement]:** post-softmax значения неравномерны, GELU асимметричен; обычный uniform PTQ может терять малые значения и давать >1% accuracy drop даже8bit. Специальный twin-uniform quantization даёт <0.5% drop на ImageNet ViT/DeiT/Swin. Это опровергает и «INT8 безопасен автоматически», и «attention невозможно квантизовать». Не доказательство LinQ реализации этих схем и не измерение позовых keypoints/малых PPE.

## C-S16 — NVIDIA QAT counterexample

Varun Praveen/NVIDIA. **04.08.2020**. https://developer.nvidia.com/blog/improving-int8-accuracy-using-quantization-aware-training-and-tao-toolkit/ . Прочитаны авторский основной текст, Figure1 и Results/table1, AI-generated summary не использован.

**C-F16 [vendor published measurement]:** PeopleNet-ResNet18 mAP FP32 78.37→PTQ59.06→QAT78.06; ResNet34 80.2→62→79.57. Автор показывает spurious bounding boxes после TensorRT INT8 PTQ, предупреждает о regression output granularity. Это конкретный DetectNet/PeopleNet/entropy-calibrator пример; не универсальный размер падения, не современный YOLO и не LinQ. Наш вывод: смотреть FP→INT8 не только mAP, но и новые ложные candidate/events; float output может требовать поддержки платформы, которой пока нет.

## C-S17 — public LinQ tech

ООО «ХайТэк»; дата страницы неизвестна, доступ23.10.2026. https://lin-q.ru/tech . Прочитаны блоки «Тензорный процессор», «Собственное IP-ядро», «Поддерживаемые сети», framework. **C-F17 [vendor claim]:** LinQ H — int8, CNN/RNN; в списке yolo5s/yolo8/yolo11 и другие. Отсутствуют точные checkpoints, shapes, opsets, postprocess boundary и SDK version. Список семейств не гарантирует исполнение выбранного pose/seg/open-vocab варианта.

## C-S18 — public LinQ HPS datasheet/home

ООО «ХайТэк», дата/revision PDF не указана. https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf ; https://lin-q.ru/ . Прочитаны datasheet p1–3, homepage product family. **C-F18 [vendor claim]:** HPS имеет основной int8; fp16/bfloat16 обозначены перспективой. PyTorch через ONNX и LinQ Compiler/DNN Quant заявлены. HPS — одна конкретная линейка, homepage различает HP/HPD/HPQ/HPS/HX. Не установлено, какой ускоритель/SDK дают на хакатоне; «полная поддержка ONNX» в datasheet не substitutes supported ops/test compile.

## C-S19 — официальный анонс

Организаторы Открой#Моспром; дата публикации блока неизвестна, доступ23.10.2026. https://hackathon2026.otkroimosprom.ru/ . Прочитан блок кейса LinQ. **C-F19 [primary announcement]:** примеры smoking near flammables, respirator removed, no hardhat, danger zone; real-time video service; model inference must run on LinQ, online access promised. Нет в прочитанном блоке SDK/оборудования/точного списка обязательных сценариев. Это анонс, не полный кейс.

## C-S20 — HDS-YOLOv5, ограниченный доступ

Mingju Chen, Zhongxiao Lan, Zhengxu Duan, Sihang Yi, Qin Su. **25.07.2023**, MBE20(8):15476–15495. https://www.aimspress.com/article/doi/10.3934/mbe.2023691 . Открыты publisher metadata/abstract, fulltext не получен. **C-F20 [author claim only]:** hook status detector HDS-YOLOv5 сообщает91.2%mAP@0.5/24FPS. Не используем эти цифры для выбора: не установлены class definitions, test split и означает ли статус реальную связь с anchor. Это полезная зацепка второй волны, не закрытый ответ.

## Журнал закрытых/недоступных веток

- Domination smoking URL https://domination.one/products/analitycs/litsenziya-na-modul-videoanalitiki-detektor-kureniya/ : web internal error, urllib SSL timeout, requests read timeout18s. Search-index показывает face100px/5FPS/1080p, но **не записываем фактом**, поскольку body не прочитан.
- Bosch первый resources-boschsecurity CDN404; заменён официальным cdn.commerce.boschsecurity.com, PDF1,140,468 bytes получен, p5 visually verified.
- ISARC Lee2021 fulltext URL077...Paper139.pdf404; proceedings36.98MB web limit. Search-index96.58% hook attachments по IMU не записываем прочитанным источником. Вместо него полноценный C-S08 с прямо признанным camera failure.
- MDPI hook2024/YOLO-ILB2026 открытие429. Не используем их геометрические формулы и результаты как прочитанные.
- FallVision PMC11950752 recaptcha. Не переносим dataset metadata из search-index как исследованный результат.
- Запросы на закупки: `site.zakupki.gov.ru "видеоаналитика" "касок" "техническое"`, «контроль касок техническое задание пикселей», Chinese smoking installation. Приёмочного протокола с ID закупки и event FA для этой ветки не получено. W1_A отдельно нашёл grant ТЗ itdf.ru, это не подтверждённая госзакупка и не независимый measurement.
- Запросы pose quantization приводили к heatmap coordinate discretization и motion-token compression. Это **не INT8 arithmetic quantization**. Не использовать их как доказательство INT8 деградации ключевых точек. Прямой размер эффекта для нашей pose/PPE остаётся неизвестен.

## Техническое происхождение и журнал поиска

Bosch PDF: 34 страницы; SHA256 a53e68bea1a746768f5b020c91ee4284c4ebc6b281df89d0e449306d5ad376d3. PDF прочитан как документация, p5 отрисована и просмотрена; ни один model inference не выполнялся.

Поисковые группы (23.10.2026):

- `smoking detection cigarette hand mouth eating drinking video primary paper` → CEUR Pyataeva; wearable IMU papers исключены как доказательство CCTV качества.
- `site.hikvision.com smoking pixels`, `курения пикселей видеоаналитика`, `吸烟检测 摄像机 安装 要求 人脸 像素 海康` → недоступный Domination, TP-LINK thermal manual; RGB universal minimum не установлен.
- `site.docs.macroscop.com касок минимальный пикселей`, `site.hikvision.com Hard Hat pixel`, `site.dahuasecurity.com Smoking Pixel` → Macroscop4.7/Bosch6.30/Dahua2020 manual. Dahua smoking configuration открыт, численных пригодных требований не извлечено, в выводы не включён.
- `safety harness hook detection vision paper`, `fall detection lying down intentional lying surveillance camera dataset primary paper` → Lim fulltext с признанным failure, HDS abstract, Macroscop explicit lying semantics.
- `YOLO-World real-time open vocabulary object detection reparameterize CVPR 2024`, `YOLOE real time seeing anything reparameterization 2025`, `Grounding DINO 1.5 open set object detection arxiv` → первичные papers и pinned reparameterization doc, без export test.
- `POPE evaluating object hallucination large vision language models EMNLP 2023`, `SAHI slicing aided hyper inference small object detection paper`, `quantization object detection small objects activation outliers INT8 paper PTQ4ViT`, `post training quantization pose estimation heatmap int8 paper accuracy` → primary mechanisms; отдельно отвергнуты coordinate quantization работы как нерелевантные INT8.
- `site.lin-q.ru tech ONNX INT8` → tech/home/HPS datasheet, публичные family claims; exact hackathon config неизвестна.
