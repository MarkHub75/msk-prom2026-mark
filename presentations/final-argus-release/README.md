# Финальная презентация Argus

Актуальная версия: **15 слайдов**. После архитектуры добавлен слайд 09 «Как Argus экономит вычисления», после плана пилота — слайд 13 «Экономика».

- [PowerPoint — актуальные 15 слайдов](exports/ARGUS_Final_15.pptx).
- [PDF — актуальные 15 слайдов](exports/ARGUS_Final.pdf).
- [PNG: как Argus экономит вычисления](slides/slide-09.png).
- [PNG: экономика](slides/slide-13.png).
- [Общее превью](preview/ALL_15_SLIDES.png).
- [Текст докладчика и вопросы](SPEAKER_SCRIPT.md).
- [Источники и оговорки](SOURCES.md).
- [Проверка актуальной версии](VERIFICATION.md).

Новые слайды используют графитовую палитру, Source Sans 3 и приглушённый синий `#8ba9cc`. PNG — 1920×1080; в PPTX каждый слайд представлен одним изображением, заметки докладчика остаются текстовыми.

Экономика основана на `front/final@87f8a2c47d9621c8b7620d20c3c0548c0ebb128a:docs/ECONOMICS_SOURCES.md`: Росстат 2025, КоАП 5.27.1 (ч. 4, 5, ред. 2026), кейс АлЭС 2026 по данным заказчика. Снижение зарегистрированных нарушений во внешнем кейсе не представлено как снижение травматизма или результат Argus. Точная окупаемость — после пилота; калькулятор показывает точку безубыточности при заданных допущениях. Срок окупаемости не обещается.

Схема вычислений отражает режимы из запроса пользователя. Дополнительные аппаратные замеры и процент экономии не добавлены. Исходный промышленный кадр LinQ сохранён целиком на слайде 10; его речь и атрибуция сохранены.

Файл `ARGUS_Final.pptx` был заблокирован для записи и содержит прежние 13 слайдов; актуальный PowerPoint сохранён как `ARGUS_Final_15.pptx`. Каталоги `review-final`, `review-13`, `evidence/*-13`, прежнее общее превью и их отчёты — история версии из 13 слайдов. Они не подтверждают новую версию; актуальные отчёты находятся в `evidence/exports-15`, `evidence/powerpoint-15` и `evidence/pdf-report.json`.

Воспроизведение в Python с Pillow, fonttools и PyMuPDF и Node с PptxGenJS:

```bash
python scripts/compose.py
# При изменении исходного рассказа: python scripts/story.py
# story.py автоматически применяет scripts/add-economics-compute.py.
node scripts/exports.mjs
python scripts/pdf-preview.py
# Windows PowerPoint: scripts/powerpoint-check.ps1
python scripts/verify-exports.py --require-powerpoint
python scripts/deliver.py
```

При отдельном запуске `add-economics-compute.py` изменения применяются повторно без дублирования слайдов. `SAFEWATCH_PPTXGENJS_MODULE` позволяет указать установленный модуль PptxGenJS. Прежние сценарии полного frontend/Craft/HRE-аудита относятся к версии из 13 слайдов; для этой правки продуктовые тесты заново не запускались.
