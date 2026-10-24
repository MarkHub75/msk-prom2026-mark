# Источники и границы утверждений

Проверено: 2026-10-24T15:31:15.703095+03:00. Git fetch выполнен; снимки источников зафиксированы по хешам, без обращения к LinQ. Новых runtime-тестов front/final и ML здесь нет.

## Проверенные головы веток

- `main`: `5d940ba22ebebb2255ff7b12252268c3d9d393ab`
- `front/final`: `72358bde5a3e8098c09c5132dd2e2cb90751e16f`
- `matvey_cv`: `8f879606dc7511ef7893d6be57f8f9efb12112e8`

## Источники

| ID | Git-путь | Снимок |
|---|---|---|
| s02 | `main:tech.md` | [research/main__tech.md.excerpt.txt](research/main__tech.md.excerpt.txt) |
| s03 | `main:progress.md` | [research/main__progress.md.excerpt.txt](research/main__progress.md.excerpt.txt) |
| s04 | `main:docs/linq/LINQ_CONTRACT.md` | [research/main__docs__linq__LINQ_CONTRACT.md.excerpt.txt](research/main__docs__linq__LINQ_CONTRACT.md.excerpt.txt) |
| s05 | `main:results/linq_smoke/synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json` | [research/main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json](research/main__results__linq_smoke__synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json) |
| s06 | `main:docs/ML_INTEGRATION.md` | [research/main__docs__ML_INTEGRATION.md](research/main__docs__ML_INTEGRATION.md) |
| s07 | `main:contract/openapi.json` | [research/main__contract__openapi.json](research/main__contract__openapi.json) |
| s08 | `main:contract/ws.schema.json` | [research/main__contract__ws.schema.json](research/main__contract__ws.schema.json) |
| s09 | `front/final:frontend/src/App.tsx` | [research/front-final__frontend__src__App.tsx](research/front-final__frontend__src__App.tsx) |
| s10 | `front/final:frontend/src/roles.ts` | [research/front-final__frontend__src__roles.ts](research/front-final__frontend__src__roles.ts) |
| s11 | `front/final:frontend/src/features/Incident.tsx` | [research/front-final__frontend__src__features__Incident.tsx](research/front-final__frontend__src__features__Incident.tsx) |
| s12 | `front/final:frontend/src/features/Stats.tsx` | [research/front-final__frontend__src__features__Stats.tsx](research/front-final__frontend__src__features__Stats.tsx) |
| s13 | `front/final:frontend/src/features/Journal.tsx` | [research/front-final__frontend__src__features__Journal.tsx](research/front-final__frontend__src__features__Journal.tsx) |
| s14 | `front/final:frontend/src/styles/ds.css` | [research/front-final__frontend__src__styles__ds.css.excerpt.txt](research/front-final__frontend__src__styles__ds.css.excerpt.txt) |
| s15 | `matvey_cv:ml/EVAL_REPORT.md` | [research/matvey_cv__ml__EVAL_REPORT.md](research/matvey_cv__ml__EVAL_REPORT.md) |

Полные commit/SHA256/строки: [source-index.json](research/source-index.json). Источники не являются новым замером. Ночная диагностика в начале ML EVAL_REPORT имеет приоритет над историческими разделами.

## Утверждения по слайдам

### 1. Опасное событие должно стать действием.

Нужен путь от сигнала к ответственному и подтверждённым мерам.
Источники: s02, user. Продуктовая задача, не измеренное снижение риска.
### 2. У события есть ответственный

Оператор, мастер, охрана труда, руководство, администратор.
Источники: s02, s10. Роли/маршруты подтверждены кодом; новый runtime не проверялся.
### 3. От сигнала до принятых мер

Проверка, красное событие, поручение мастеру и журнал действий.
Источники: s02, s07, s11. Жёлтый→красный условен; confirm красного автоматически фиксирует передачу.
### 4. Журнал становится картиной смены

Период, сектор, камера, сценарий, вердикты и время реакции.
Источники: s12, s13. Наличие в коде; значения demo не становятся производственными метриками.
### 5. Baseline исполнялся на TPU

Baseline det640/pose640 исполнялись на TPU; detector video400frames:19.09s,20.95FPS,total31s.
Источники: s04, s05. Пропускная способность detector-записи, не общая det+pose/alert/device latency.

Свои Helmet/Split-Pose имеют отчёты реального TPU исполнения.
Источники: s15. Исторические отчёты; task quality NOT_ACCEPTED и независимый final test NOT_RUN.

Стабильный интегрированный backend-прогон не подтверждён.
Источники: s03. Поздний R5 timeout; не отменяет отдельный успешный baseline smoke.
### 6. Один конвейер. Разные рабочие места.

Jupyter/TPU→JSONL→CPU tracking/rules→episodes→server-clock replay→WS→roles→journal.
Источники: s02, s04, s06, s07, s08. Проектная архитектура; стабильность общего LinQ остаётся открытой.
### 7. Граница готовности видна

Сквозной LinQ, независимое качество, задержка и ложные тревоги требуют проверки.
Источники: s03, s06, s15. Не объявлять собственные модели никогда не исполненными на TPU.
### 8. Следующий шаг — проверяемый результат

Собрать общий контур, измерить качество и проверить цикл на участке.
Источники: s03, s06, s15, user. План без обещанных дат, KPI и уже проведённого пилота.

## Что изменилось относительно раннего задания

- main уже содержит R15/S0–S15 и новый docs/ML_INTEGRATION.md. Старые S0–S10 и S0–S11 не повторяются как текущая граница готовности.
- front/final содержит реальные импорты страниц и обновлённую тёмную дизайн-систему. Старый FRONTEND_STATUS.md не принимается за актуальную реализацию. Здесь проверен код; пользовательские снимки пока отсутствуют.
- matvey_cv описывает историческое исполнение собственных моделей на TPU и более позднюю saved-output/SDK диагностику. Формулировка «только скомпилированы, на TPU не исполнялись» устарела. Счётчики тестов не выносим: в отчёте есть более новые секции,335 не является актуальной единственной цифрой.
- Стабильный общий LinQ backend, независимая industrial-quality, false alerts/camera-hour и event-to-alert latency не подтверждены. Хороший отдельный baseline не доказывает это.

## Сознательно исключено

- «Точность91%», производственные P/R без независимых данных, zero false alarms, снижение травматизма/окупаемость, уже проведённый заводской пилот.
- «Все модели работают на LinQ», чистое chip timing по worker.inference_time,21FPS как alert latency или скорость общего det+pose-конвейера.
- Включённая45-секундная автоэскалация: конфигурация в этой задаче не проверялась.
- Превосходство над IVA CV и статус «ближайшего конкурента»: в проверенных Git-источниках нет сравнительного исследования. По пользовательскому утверждению не делаем подтверждённый конкурентный вывод.
- Старые UI-скриншоты, визуально сгенерированные экраны и выдуманные значения аналитики.

## Допущения

План — последовательность работ без новых сроков и численных обещаний. Будущие UI-снимки принимаются как реальные материалы пользователя, происхождение и режим каждого снимка проверяются при замене. Заголовок с названием продукта виден ровно один раз.
