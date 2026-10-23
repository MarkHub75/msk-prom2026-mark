# Вторая волна: индивидуальные задания

Полный предмет каждого задания (problem/material/impact/missing evidence/task) сохранён в CRITIC.md под соответствующим K-ID. Это не новый обзор наборов: нужны новые основания, способные подтвердить, ограничить или опровергнуть рекомендации W1.

## Общая часть каждого из трёх исследователей

Роль: gpt-6.1-sol, reasoning_effort=medium, fork_turns=none. Рабочая папка D:/msk-prom2026-mark/datasets. Прочитай UTF8 два входных файла, PLAN.md, CRITIC.md, своё распределение и относящиеся W1 результаты/сохранённые первоисточники. Команда готовит сервис промышленной видеобезопасности для «Открой#Моспром» 2026 с обязательным инференсом LinQ. Полного кейса/целевых данных нет; каска/респиратор/зона/курение — примеры, не окончательная таксономия. RTX4070 доступна для подготовки; другие точные характеристики не установлены.

Ты получаешь новые сетевые материалы доступными инструментами и делаешь небольшие предметные проверки. Массовые полные media downloads, обучение и приложение не нужны. Независимые обращения можно batch, но общие originals не перезаписывай. Дочерних агентов не создавай. Внешним людям не пиши. Не жди пользовательского ответа или соседнего исследования. Связанные notices/новые сильные наблюдения передавай оркестратору и соседям до конца группы.

У каждой ячейки отдельный _WORK/W2-XX.md и _WORK/MATERIALS/W2-XX/. Источники/факты W2-XX-S01/F01 и далее; вид основания отличается от статуса проверки. Источник/автор/прямой URL/версия/commit/locator/дата публикации и отдельно реальная дата доступа/что получено/что не проверено/условия обязательны. Времена берите только фактическим clock; дата без точного интервала лучше выдуманного времени. Числа metadata, annotation records, media files, уникальных сцен и реально декодированных изображений не смешивай.

Выбирай примеры по смыслу, сохраняй IDs и причину отбора; выборочный просмотр не полная валидация. Raw state, geometry, partial labels, rights layers, group inference и derived lineage сохраняются. Неизвестное не заполняется памятью. HTML403/404/429 не прочитанный документ; listing/link не downloaded payload. Разрешение кода/статьи не подменяет media rights. Содержательный access failure после конкретного официального fallback — полезный результат с точной следующей процедурой. Не повторяй W1 как новое независимое подтверждение. Сохраняй результаты прогрессивно.

Для каждого K в своём результате предложи конечный статус и основания: закрыто / область уточнена / противоречие / открыто / утратило значение. Окончательное сведение делает collector. Если P2 откладывается по scope, явно объясни и дай Q, не притворяйся что проверка выполнена. P0 получить содержательно обязательно, хотя результатом может быть локализованная недоступность.

## Исследователь W2-A — SH17, CPPE, условия и масштаб

1. **W2-01 / K001:** released SH17 labels через официальную Kaggle pagination/small files; map и paired released↔raw comparison на одних basenames. Существующее: W1-02/11/14 и MATERIALS. Решение: точный воспроизводимый donor, а не подмена8099release на8102raw.
2. **W2-02 / K002:** содержательно выбранные raw SH17 on/off/safety/vision paired images, реальная geometry/state/association/partial labels. Существующее: rawXML+URLCSV. Решение: есть ли usable wearing supervision или нужна ручная доразметка.
3. **W2-08 / K008:** CPPE original versioned release tree/source-license metadata/category/split↔HF, несколько mask subtypes. Существующее: W1-04/11/10, release v0.1.0/dataset.tar.gz и HF29rows. Решение: traceable conditional respirator donor и точный state gap. Не выдавай subtype за сертификацию.
4. **W2-12 / K012:** bounded notices SFCHD/SH17 и поступающие от соседей archive notices; action matrix code/labels/images/assembly/article. Существующее: W1-10, Pexels legal web чтение с неудачным shell snapshot. Решение: конкретные blockers/fallback, без общей юридической гарантии и внешней переписки.
5. **W2-13 / K013:** annotation-based per-class scale native/conditional letterbox640, SFCHD/SH17raw/CPPE29; исправление threshold<0.1% versus цитата0.12%. Существующие annotations уже сохранены. Решение: donor/crop priority; это расчёт и metadata анализ, не accuracy и не установленный LinQ input.

## Исследователь W2-B — SFCHD и helmet-family artifact

1. **W2-03 / K003:** полный локальный annotation-only consistency COCO↔YOLO, categories/boxes/tolerance/membership/6test paths, candidate missingTXT conversion отдельно. Существующее: W1-03/12/15, COCO/labels/splits сохранены. Решение: reproducible source-of-truth loader/split без замены originals.
2. **W2-04 / K004:** SFCHD author image route, paired semantic samples всех7classes, filename/prefix/run↔split; supplied vs inferred groups, de-identification и реальные возможности holdout. Существующее: paper/tree/JSON. Решение: adapt/development либо ограниченный grouped test, не выдуманные camera IDs. Notices передать A.
3. **W2-05 / K005:** SHWD author archive actual XML/image pairs, geometry hat/person, split/notices. Существующее: README/loader/DriveVOC2028 link. Решение: безопасная head mapping и цена acquisition. 20–50 pairs ориентир, меньший обоснованный sample/access failure допустим; не скачивай все крупные archives ради квоты.
4. **W2-06 / K006:** CHV actual archive map и colored helmet/vest/person pairs, samples/format/completeness/parent overlap. Существующее: W1-03/09 paper+Drive+Baidu. Решение: полезный donor или дороже собственного relabel; notices A.
5. **W2-07 / K007:** SHEL5K actual XML layer count/geometry/protocol/splits и расширенный targeted paired sample. Существующее:5000XML+5000PNG full metadata и3pairs, working Mendeley folder API. Решение: наблюдаемые75,570/75,578 differences и usable state geometry, без обещания commercial rights. ПолныеXML(~19MB metadata sum) получить если маршрут разумно доступен; избегай полной1.3GBmedia загрузки, если достаточно небольших samples. Exact access limit/procedure допустим вместо выдуманного fullcount.

## Исследователь W2-C — smoking, реальное видео, schema и fallback

1. **W2-09 / K009:** восстановить DOI10.3390/electronics12153225 primary paper→data availability→surveillance smoking/calling artifacts; static object/person-action/interval distinction. Параллельно decode локального SmokerRAR, реальные dimensions/confusers/duplicate observations отдельно от source labels. Решение: найден ли localization donor или точная своя разметка.
2. **W2-10 / K010:** Önal Mendeley full file/folder manifest и несколько actual safe/unsafe walkway clips, measured FPS/timebase/duration, annotations, camera inference и lead-in/continuous links. Решение: реальный replay и минимальная event annotation, не falsealerts/hour по691curated clips. Существующее: W1-07 article и рабочий Mendeley pattern C.
3. **W2-11 / K011:** SARD author schema/HOI/splits/source mapping; bounded linked media и frame/ID/geometry check если доступно. Существующее: ZIP directories+4.txt. Решение: temporal donor versus lowerpriority unexplained43GB source. Не называть IDs tracks без основания, не скачивать35GBрадиsample.
4. **W2-14 / K014:** Pictor actual available subset+labels и Construction-PPE no_*/none/Person geometry sample/terms/provenance. Существующее: W1-01/05/11 README/Drive/YAMLrelease. Решение: практический fallback или явное понижение. Вне scope PPE expansions можно отложить с основанием.
5. **W2-15 / K015:** PhysicalAI deterministic family-parent-chunk-media join и exact license conditions; smoke/vap substrings неfamily, packaged/external/unlabeled разделить. Существующее: W1-06/09/15 savedmetadata. Решение: synthetic plumbing donor либо отложенная гипотеза, не industrial holdout. Media sample только если меняет решение.

По завершении группы: краткая передача оркестратору — новые факты, что изменило решение/что не подтвердилось, paths, K-status suggestions и Q. Никакого общего финального файла роль не редактирует.

## Дополнение при возобновлении

Три новые роли resume_w2_a/b/c созданы с fork_turns=none, model=gpt-6.1-sol, reasoning_effort=medium. Им переданы самодостаточные задания прочитать оба входа, RUN_STATE, CRITIC и настоящее WAVE2_PROMPTS, затем продолжить прежние группы A/B/C с инвентаризации собственных MATERIALS и скриптов. Сохранённые проверки повторно не объявлять новыми; при необходимости добрать только незакрытое основание в рамках W2. По каждому W2-XX создать полный файл с provenance и K-status, заменив рабочие placeholders. Shared final files не изменять; дочерних агентов и интерактивных вопросов нет. Индивидуальные предметные задания выше действуют без изменений.
