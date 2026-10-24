# SafeWatch — текущая ревизия r3

Восемь растровых слайдов PowerPoint, структура сохранена. Исправлены сноски слайда 5, указана проверенная основа S0–S11, пересняты текущие экраны, усилен акцент на TPU, добавлены отличия и IVA CV, обновлены порты показа. Новых численных результатов CV не добавлено.

- [PowerPoint](exports/SafeWatch_Checkpoint_2026-10-24.pptx)
- [PDF](exports/SafeWatch_Checkpoint_2026-10-24.pdf)
- [Превью всех слайдов](preview/SafeWatch_8_slides.png), [8 PNG](slides/)
- [Сценарий и заметки](SPEAKER_SCRIPT.md)
- [Источники](SOURCES.md), [текущий source-index](research/revision-r3/source-index.json)
- [Проверка](VERIFICATION.md), [съёмка UI](research/frontend-r3-summary.md)

Текущие источники: main b4fb994c, front/control-room 1b8822ef, demo/checkpoint 053683da. На слайде оставлена запрошенная основа S0–S11; свежий main продвинулся дальше, журнал backend уже реализован. Предыдущие source snapshots сохраняют происхождение прежних численных испытаний LinQ и ML.

Показ: http://localhost:5173, мок REST4010 и WS4011. Мок tools/checkpoint-demo, последовательность reset → next → next --force. Кадры синтетические, рамки ручные; это пользовательская демонстрация, не измерение качества CV. Код SafeWatch не менялся; runtime изолирован.

Финальный Human Review — [review-r3/](review-r3/), неизменённый OS renderer v1.1. Решения не выбраны. Старые review/ и review-r2/ — история, не актуальная оценка. Локальный адрес: http://127.0.0.1:8725/msk-promhack/safewatch-checkpoint-pptx/presentations/checkpoint-2026-10-24/review-r3/

Сервер HRE: python3 -m http.server 8725 --bind 127.0.0.1 --directory /mnt/d/templates

Workflow: [craft/WORKFLOW.md](craft/WORKFLOW.md). Для текущей ревизии используются evidence/craft-r3, evidence/browser-r3 и review-r3, revision=3. Presentation Craft не утверждает человеческий вкус автоматически; checkpoint HUMAN_SAFEWATCH_CHECKPOINT_PRODUCTION_REVIEW остаётся открытым.
