# Индивидуальное поручение W2-07 — вторая волна

Роль: самостоятельный сетевой исследователь gpt-6.1-sol, effort=medium, fork_turns=none. Ты получаешь новый контекст, не запускай субагентов. Рабочая папка текущая; topic model_fidelity_quantization. Это согласованная вторая волна после15 W1 (12general/3LinQ) и отдельного fresh critic high. Команда пяти участников строит industrial safety video service, final neural inference на LinQ обязателен. GPU не арендовали, модели/SDK/сервер не запускались. Кейс найден локально, root прочитал все20 страниц визуально по сохранённым рендерам: _WORK/CASE_NOTES.md; оригинал _WORK/INPUT/CASE_LINQ.pdf. VM/сервис обещаны, actual grant/SDK/device/model/GT отсутствуют. Заявление команды про1FPS и server-file mode — working assumptions, не контракт API/метрик.

Прочитай полностью оба входных договора, _WORK/CRITIC_HANDOFF.md, свой точный K текст ниже и указанные W1/source snapshots. Дальше получай новые первичные сетевые основания по узкому вопросу, а не повтор W1. Открывай фактический content и цепочки provenance, не пересказывай snippets. Даты/версии/commit/locators/author/access фиксируй; живые docs не lockfile. Если PDF bytes доступны, визуально проверь спорные tables/code/footnotes через PDF workflow; failed tool access vs actual closed file разделяй. При недоступном live source можно использовать сохранённый primary excerpt с атрибуцией, не выдавая его за свежий fetch. Copyright: пересказ+locators вместо длинных копий.

Собственный результат _WORK/W2_07.md; snapshots _WORK/MATERIALS_W2_07/. S/F префикс W2-07-. Каждый факт: source, locator, exact version/conditions, actual verification status, limitation, practical decision. Типы vendor claim/documentation/code/published measurement/local observation/inference/proposal/unknown; чтение кода не execution, чужой benchmark не наш. Общие ORT/Intel/NVIDIA возможности не доказывают LinQ. Неизвестность не доказательство отсутствия. Соседние отчёты secondary; их запуски не наши.

Никаких установок SDK, подключения сервера, аренды, training/model benchmarks, приложения, push/PR или сообщений людям. Допустимы маленькие read-only metadata/code inspection и явно аналитические расчёты там, где они нужны; не называй это модельным измерением. Команды/API только с фактической версией и основанием; pseudo-code явно. Опубликованные числа сохраняй вместе с setup, без переноса на LinQ/3090. Новые сильные зацепки можно развить, если меняют поставленный выбор, объяснив пользу.

В результате отдельный блок K dispositions: новый факт/source, что изменилось, closed/scope narrowed/contradiction/open/superseded, оставшийся риск и точный Q со способом закрытия. Не редактируй CRITIC или общие финальные файлы. Остановись при полезном новом основании/ограничивающем условии или содержательно локализованном unknown после адресного поиска; не искать закрытый SDK бесконечно. Короткая передача root:3 находки, блокер, следующий шаг, путь и K outcomes.

## Точный предмет и source targets критика

| W2_07.md | K009,K010 | Quantify силу0 ошибок на малом corpus через корректные one-sided binomial/zero-count rate bounds при явных независимых предпосылках; cluster/selection ограничения сохранить. Target: SciPy primary CI docs/source, NIST или иной первичный statistical source; W1-12. Дать гипотетические аналитические расчёты без нормативов кейса. Один acceptance record detection/pose/tracking/events с datum/decision/not-exposed разделением; сценарии small roster/insufficient rare holdout/catalog without source. Stop: допустимый claim и адресат каждого пробела; actual thresholds/GT решает команда. |


## Исходная критика (сохранять историю)

## K009 — Для «ошибок не увидели» не хватает простого количественного ограничения силы вывода

**Приоритет / закрытие:** P1; WEB+методический вывод, затем DATA/TEST.

**Проблема и локатор.** W1-12 раздел «Парная uncertainty» справедливо предупреждает о `[0,0]` bootstrap при нулевых ошибках, few clusters, undefined draws и неэквивалентности `p>0.05`. Но не даёт рабочей альтернативы для типичного hackathon outcome: все немногочисленные события прошли, новых FN или false alerts не зарегистрировано. В результате инженер либо остановится на HOLD без понимания требуемых данных, либо придумает «достаточно20 клипов».

**Что меняет для команды.** Нужно отличать narrow regression PASS на фиксированном roster от утверждения о recall/risk на популяции. Число событий, независимых источников и negative exposure по-разному ограничивают возможный claim. Наращивание одинаковых кадров не решает задачу.

**Недостающее доказательство.** Применимые exact one-sided bounds для простого независимого event model и zero-count rate model, с явными предпосылками; почему эти формулы не годятся автоматически при camera/incident clustering, неоднородности и выборе winner на test. Отдельно — paired regressions, которые net Δrecall может компенсировать новыми TP.

**Узкое W2 / source targets / завершение.** **W2-07**: первичная документация SciPy binomial confidence intervals и NIST/первичный статистический источник для zero-count rate, плюс сохранённый clustered-design материал W1-12. Дать несколько **гипотетических аналитических** расчётов по числу независимых событий/exposure, без назначения нормативов кейса; отдельно показать новый miss vs gained TP. Завершение: читатель может назвать, что доказывает0 ошибок на его roster и какие данные нужны для более сильного утверждения; при неизвестной независимости остаётся descriptive/INCONCLUSIVE, а не фиктивный exact population CI.

**Disposition W2:** PENDING.



## K010 — Бюджеты качества и доступность GT являются решениями/артефактами, которые ещё один поиск не закроет

**Приоритет / закрытие:** P0 для финального acceptance, P1 для подготовки протокола; DECISION+ARTIFACT+TEST.

**Проблема и локатор.** W1-06/07/10/11/12 правильно откладывают δ, absolute floors/caps, critical roster, deadline, минимальную длительность события и достаточный GT. Однако много «PASS по согласованным thresholds» пока являются условной формой, не заполненным quality contract. Это не ошибка отсутствия универсальных констант; опасность возникает, если будущая сборка представит методическую таблицу как готовый допуск. Perfect parity слабого baseline тоже недопустима по safety claim.

**Что меняет для команды.** Нужен маленький конкретный пакет решений до выбора winner: какие сценарии поддерживаем, что можно наблюдать, что считаем одним эпизодом/actor, что обязано пройти smoke, какие абсолютные требования отдельно от сохранения исходной модели, и какую область вообще не оценили. Нужны независимые labels и continuous negatives, а не эталонные predictions вместо GT.

**Недостающее доказательство.** Принятые командой требования и реальные manifests/GT/права/источники. Публикации помогают выбрать форму метрики, но не цену пропуска на конкретной площадке. Заказчик может уточнить deadline; исследователь не вправе выдать найденное в другом benchmark число за официальный допуск.

**Узкое W2 / source targets / завершение.** **W2-07**: сформировать один заполняемый acceptance record для detection+pose+tracking+events, используя W1-12 и локальный кейс с.5/7/13/19, с отдельными полями team decision, datum missing, not exposed, measured. Добавить три сценария ограничений: малый фиксированный regression pack; независимый holdout с недостаточными rare positives; каталог готовых моделей без source checkpoint. Завершение — явная граница допустимого claim и адресат каждого незаполненного поля, а не придуманное численное PASS. Этот пункт окончательно закрывает команда после получения данных, не Medium web search.

**Disposition W2:** PENDING.



