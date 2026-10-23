# W2-K DATA_AUDIT — SH17: head при каске и утечки; construction-ppe: статистика и аудит

Модель: Claude Sonnet 5.5, effort medium. Почему: получение данных и прогон готового аудитора/статистики — точная, но не глубоко аналитическая работа. Закрывает K019, K023 (данные).

Прочитай `ROOT\_WORK\CONTEXT.md`, `ROOT\_WORK\CONTEXT_WAVE2.md` (п. 9: сторонние .pt не загружать), в `ROOT\CRITIC.md` — K019, K023, K018 (размеры объектов нужны W2-L). Опорные: `W1-05_PPE_HELMET_VEST.md` (F04–F06, Q1, E3), `W1-14_METRICS.md` (F25, F26), `W1-08_DATA_CONTRACTS.md` и `W1-08_files\audit_yolo_dataset.py`, `W1-03_WEIGHTS.md` (F13). Читай FLASH `W2-F_REAL_FINETUNE.md` (путь к construction-ppe — не скачивай дважды).

Результат: `ROOT\_WORK\WAVE2\W2-K_DATA_AUDIT.md` (+ `W2-K_files\`: json-статистика, гистограммы в csv/png малого размера).

## Что сделать
1. **construction-ppe**: sha zip против `bef8dcb5…`; аудитор W1-08; распределение классов по сплитам; размеры боксов (в пикселях исходника и после letterbox 640/960/1280) по классам — передай таблицу в FLASH для W2-L; near-duplicate между train/val/test (perceptual hash, например imagehash/phash в своём CPU-venv); ракурсы (кратко по выборке); логика отрицательных классов (`no_helmet` и т.п.) — как размечены (на голове? на человеке?).
2. **SH17 метки**: найти легально доступные метки (GitHub release/репозиторий ahmadmughees, HF/зеркала, Kaggle — без ключа/логина нельзя, тогда фиксируй). Если метки доступны: доля `helmet`-боксов с перекрывающимся `head` (IoA ≥ τ для нескольких τ), гистограммы; размеры `head`/`helmet`; near-duplicates train/test по хешам. Если меток нет — по README/статье установить правила разметки head/helmet (цитаты) и оставить unknown; **не загружать** `.pt` SH17 (решение оркестратора).
3. Вывод для правила «нарушение = head без helmet» и для кроп-набора W2-I.

Попытайся опровергнуть: «construction-ppe пригоден как публичный sanity/валидационный набор» (утечки, ракурсы, размер).
