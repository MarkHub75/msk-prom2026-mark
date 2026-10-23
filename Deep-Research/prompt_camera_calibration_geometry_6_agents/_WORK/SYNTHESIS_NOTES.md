# Рабочие правила синтеза

## Что не потерять при сборке

1. Пересказ checkpoint не заменяет официальный PDF; официальный перечень кейса в этом запуске не прочитан. Матрица соответствует сценариям тематического задания.
2. Infer rate / decode rate / source time / processing latency — разные переменные. Никакой заявленной универсальной нижней границы FPS.
3. Floor H переводит только точки на выбранной плоскости; масштаб из реальных метрических координат, не из самого факта четырёх кликов. Нельзя рассчитать arbitrary H по одному отрезку без дополнительных ограничений.
4. Bottom-center bbox — измерительная гипотеза о contact point, confidence детектора не является error bar координат.
5. Threshold / calibration residual / hold-out error / statistical confidence / observability — разные сущности.
6. Для safety event нужны допустимая операция, состояние механизма, активность зоны, видимость. Ни overlap, ни proximity сами по себе не доказывают нарушение.
7. Состояние «недостаточно данных» и доля покрытия нужны вместе с precision/recall. Не исключать abstentions из знаменателя так, чтобы улучшить метрику.
8. Никаких обещаний certified protective function, точности в сантиметрах, LinQ compatibility либо доступного SDK.

## Структура реестров

S: original URL; author; date/version; accessed timestamp; locator; agent-local ID; F links; read status; provenance/limitations. Local origin S для двух входов и расчётного примера отдельно от внешних документов.

F: claim/definition; evidence label; S+locator; inputs/units; scope; checked status; caveat; decision. Related original Axx-F mappings remain explicit. При выведенных формулах ссылка на исходные факты и пометка INFERENCE.

K: собственное замечание оркестратора, затронутые F, влияние, что уточнено при сопоставлении, остаточный Q. review_mode обязательно; без выдуманной истории критика и второй волны.

Q: precise missing answer; known evidence; reason unresolved; decision; priority; acquisition mode; method; F/K/E links.

E: proposed only, except explicitly executed synthetic arithmetic in GEOMETRY_SANITY.py. Inputs/access; decision changed; operations; metrics; saved evidence; pass/fail branches; non-proof. Не выдавать рекомендованные acceptance budgets за измеренное качество.

## Архитектура будущего текста (уточнить по результатам)

Практический выбор 2–3 функций → геометрическая идентифицируемость → calibration wizard and lifecycle → uncertainty/abstain → track/time/speed → operational proximity → hard 3D scenarios → full 11-column decision matrix → tool/license/compute placement → experiments/priorities/handoffs.

## Локальный расчёт

Запущен Python 3.11 script GEOMETRY_SANITY.py; stdout в GEOMETRY_SANITY_RESULT.json. Это analytical pinhole toy model без OpenCV, моделей, LinQ или видео. Камера на высоте 4 m, horizontal optical axis, f=1000 px, no distortion; dZ errors from +1 px at Z=8/20/40 m approximately 0.016/0.100/0.396 m. Point z=1 m above floor at Z=8 m falsely maps to Z=10.667 m. No claim about any real camera. Toy straight path through 0.4 m zone at 2 m/s occupies 0.2 s and both 1 Hz endpoints outside; segment crossing requires trajectory assumption.
