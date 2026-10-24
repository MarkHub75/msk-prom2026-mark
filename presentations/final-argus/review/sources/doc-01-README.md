# Каркас финальной презентации

Восемь слайдов в запрошенном порядке. Название продукта видно один раз — на обложке. Семь мест UI оставлены рамками «скрин: …»; старые или сгенерированные экраны не используются. Это версия до получения настоящих скриншотов в17:00.

- [PowerPoint](exports/ARGUS_Final_Skeleton.pptx) — один полный PNG на слайд, текстовые заметки докладчика.
- [PDF-превью](exports/ARGUS_Final_Skeleton.pdf).
- [Все восемь слайдов одним изображением](preview/8-slides.png).
- [PNG1920×1080](slides/) и [версии1280×720](preview/).
- [Сценарий4:40](SPEAKER_SCRIPT.md), [источники и оговорки](SOURCES.md).
- [Карта будущих снимков](SCREENSHOT_SLOTS.md).
- [Human Review](http://127.0.0.1:8735/msk-promhack/argus-final-presentation/presentations/final-argus/review/) — штатный неизменённый HRE OS; решения человека не заполнены.

Git-основание зафиксировано в [research/source-index.json](research/source-index.json). Текущий frontend проверен по коду `front/final`; новый живой прогон этого frontend не заявляется. Нейросети здесь не запускаются. UI ждёт настоящих снимков.

Графика и типографика следуют актуальной тёмной дизайн-системе: Source Sans3, нейтральные поверхности, красный/янтарный для опасности. Обложка использует ранее созданную ChatGPT Images индустриальную иллюстрацию; она явно подписана. Точные числа и русский текст наложены Pillow из зафиксированных исходных строк. Лицензия шрифта — assets/fonts/OFL.txt.

Проверки и ограничения после завершения — [VERIFICATION.md](VERIFICATION.md). DOM-critic не читает текст внутри PNG: его findings сохраняются; они дополняются проверкой глифов, границ, пересечений и визуальным просмотром. Human Review не утверждён автоматически.

Для воспроизведения нужны существующий OS, toolchain и Chromium. `scripts/setup.py` фиксирует источники и копирует базовые утилиты в новый материал: не запускать поверх последующих правок. Рендер — `scripts/compose.py`; контракты и заметки — `scripts/contracts.py`; экспорт — `scripts/exports.mjs` с `SAFEWATCH_PPTXGENJS_MODULE` на установленный PptxGenJS. PDF — `scripts/pdf-preview.py`. Нативная проверка — `scripts/powerpoint-check.ps1` и `scripts/verify-exports.py --require-powerpoint`.

Поддерживаемый OS workflow:

```bash
CRAFT_PLAYWRIGHT_MODULE=/path/to/playwright/index.mjs CRAFT_CHROMIUM=/path/to/chrome node /mnt/d/templates/frontend-hackathon-os/production/presentation_factory/craft/v1/capture.mjs craft/adapter.json evidence/NEW_CAPTURE
```

Capture использует только техническую поверхность `craft/capture.html` для измерения PNG. Для выступления предназначен PowerPoint. После замены снимков следует создать новые capture/review-ревизии, повторить native export и проверить соответствие исходным PNG. Замороженные evidence этой версии не перезаписывать.
