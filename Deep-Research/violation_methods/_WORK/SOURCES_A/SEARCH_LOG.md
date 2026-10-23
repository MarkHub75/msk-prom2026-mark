# Журнал получения W1_A

Доступ: 23.10.2026 Europe/Moscow. Web search/open применялись самостоятельно. Результаты с отказом не использованы как прочитанные доказательства.

## Развитые цепочки

1. `SH17 dataset personal protective equipment17 classes paper Pictor CHV SHWD head helmet` → оригинальная SH17 arxiv2407.04590v1 → TableII annotation definitions → четыре авторских GitHub → raw README/YAML → GitHub API commit metadata. Закрывает семантику head/person/face/mask и on/off; наличие полных extended tags в скачиваемой поставке остаётся неизвестным.
2. `personal protective equipment detection pose association helmet in hand worker hardhat paper` → Wójcik2021 → алгоритм/keypoint и Tables7/9 → Fig9 failure cases → модульная ELECO2023 работа. Получено прямое сравнение на одном detector и опровергающий small-scale результат. Не найден открытый benchmark именно crowded owner errors с hand-held helmet и bodypart GT.
3. `site.docs.aws.amazon.com rekognition protective equipment occluded body parts confidence unknown` → DeveloperGuide response schema → indeterminate и CoversBodyPart caveat. Получен первичный интерфейс триады; качество сервиса не проверялось.
4. `site.arxiv.org selective classification risk coverage Geifman El-Yaniv2017` → оригинальный1705.08500v2 §§2–3. Проверено i.i.d. допущение; PPE-видео гарантий не обнаружено.
5. `respirator wearing detection industrial masks neck hand computer vision paper` → head-mountedPPE2022, steel-production2026, N95classification2026. Открыты fulltext Nature/Springer и abstract PubMed. Найдены отрицательные результаты industrial cartridge и low-light gloves. Узкий вопрос отдельного класса industrial respirator-on-neck vs in-hand остаётся без первичного открытого measurement; COVID general mask этого не закрывает.
6. `site:multimedia.3m.com respirator user seal check6000 pdf` → manufacturer half-facepiece instructions. Прочитаны fitting/seal/fit-testing; подтверждена граница наблюдаемости RGB.
7. `контроль наличия касок техническое задание закупка видеоаналитика СИЗ` → itdf grantТЗ391 → прочитана Table4. Это не приёмочный measured protocol; реальный закупочный ID/результаты не установлены.
8. `site:patents.google.com helmet head wearing detection person` → CN113537019A → linked prior CN110414400A → quality/best-face region. Оба patents открыты; accuracy claims не использованы.
9. Русские `детектор СИЗ каски руководство неизвестно лицо не видно перчатки респиратор`; `site:docs.itvgroup.ru детектора экипировки пиксел` → ITV docs. Страницы найдены в поиске, но opens502. W1_C передал прямой Macroscop requirements URL; этот источник открыт мной отдельно, найдены определения/численные требования и особый vest meaning.

## Недоступное / не считать прочитанным

- OSHA1910.134 и Major Requirements: webopen403. Не использовалось как standalone legal evidence; вместо него primary3Mmanual.
- ITV ИнтеллектX5.5 page348493199 (VL image requirements),348493159 (валидная экипировка),5.0page246786721: поисковая выдача содержала таблицы, но webopen502 и PythonurllibSSLunexpectedEOF. PDF DetectorPack2.8 versions тоже502. Не получена первичная страница; значения20pxhelmet/50pxvest/200lux оттуда остаются search leads, не facts нашей ветки.
- Sensors21/10/3478 CHV, AppliedSciences10/15/5129 ChenDemachi и Buildings15/3/354 UAV:429. CHV поддерживается авторским README, не unseen fullpaper.
- CVF2017 MAFA html/pdf403. Сниппеты про32px ignore/occlusion не использованы как прочитанное доказательство.
- NSF original XiongTang2021 purl10295995:502. GitHubruoxinx/PPE-Detection-Pose найден, содержательное открытие не доведено; результаты .97/.95F1 не занесены в доказанную базу. Более сильное same-detector comparison уже есть S05; повторная обзорная работа не нужна для текущего выбора.
- PMC11648733/8391571/9372528 приopen recaptcha. Не считать прочитанными статьи healthcare/COVID по search previews. EuropePMC fallback также недоступен. Не переносились опубликованные там цифры.
- Sage gasmask DOI10.3233/AIS-220460:timeout. Полного paper нет. Нельзя использовать snippet23.2%gain.
- Karlsson arxiv2212.04794: abstract открыт; PDF17.8MB отвергнут toolcontentlength; html404. Не включён в основные S: обнаруженные abstract3/5m и mAP99/89 не дают условий камеры для переноса.
- Случайная попытка GitHubSHWD issue19 failed; никакого реального issue complaint оттуда не извлечено.

## Что не выполнялось

Training/inference/benchmark отсутствуют. Изображения датасетов и GT архивы не скачивались; legal/licenses review отсутствует. Код SHWDtrain и Pictordecode прочитан, не запускался. Совместимость LinQ не оценивалась. Отсутствие найденного evidence не означает отсутствие метода или SDK.
