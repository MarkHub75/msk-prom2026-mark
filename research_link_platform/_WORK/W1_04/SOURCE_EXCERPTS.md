# W1-04 — собственные короткие выписки

Доступ 23.10.2026 около04:20–04:25 Europe/Moscow. Ниже содержательный пересказ; полные чужие страницы не копируются. Способы получения и ограничения сохраняются в RESULT.

## W1-04-S01 — https://lin-q.ru/sol

Раздел ПО: квантование и компиляция, API Python3.8, CLI; ПО связано с OEM-аппаратной поставкой. Download требует регистрации и верификации. Web прочитан. Короткий точный литерал: `Python 3.8`.

## W1-04-S02 — https://files.lin-q.ru/tpu/docs/Framework_manual_H1.pdf

TinyFish самостоятельно извлёк руководство2025; документ `RU.РМДВ.04.06.014-03 34 01`. §2.1.1 задаёт Ubuntu20.04, i7-7700, RAM≥32ГБ, Python3.11. §2.2 — venv/pip/import. С.17–20 разделяют TLM/сохранение `.tpu` и реальную работу Device API. С.23 log с python3.8: внутреннее расхождение контекстов. Короткие точные литералы: `tpu_framework-py3-none-any.whl`, `python3 -c "import tpu_framework"`.

## W1-04-S03 — https://files.lin-q.ru/tpu/pr/2026_linq_presentation.pdf

TinyFish текст: 2026; author metadata Севрюков Сергей. Benchmark слайд4: i7-10700K @3.80GHz / Ubuntu24.04 / TPU Runtime16.18.6 / TPU Framework2026.8.43. Слайд6 содержит заголовок ОС/архитектур, картинная часть не извлечена. Не переносить benchmark configuration на доступ команды.

## W1-04-S04 — https://files.lin-q.ru/tpu/docs/_HPact_manual_LINQ_HP1M_02.pdf

TinyFish hardware guide §2.4: после PCIe монтажа проверить обнаружение endpoint, затем установить отдельные компоненты драйвера LINQ H1 по документации производителя. Ожидается один endpoint. Точные диагностические литералы: `lspci | grep MIPS`, `MIPS: Device 2805:0006 (rev 08)`.

## W1-04-S05 — https://files.lin-q.ru/tpu/docs/_HPQact_manual_LINQ_HPD1M_11.pdf

TinyFish §2.4 с.14–15: после монтажа четырёхпроцессорного модуля — четыре endpoint той же идентификации, затем драйвер LINQ H1. Hardware detection и SDK inference — разные проверки. /docs показывает HPQ Active, обозначение файла HPD1M-11, оба сохранены.

## W1-04-S06 — https://files.lin-q.ru/tpu/datasheet/linq_hps_datasheet.pdf

Web PDF доступен. С.2 содержит vendor claim об интеграции в гетерогенные кластеры x86/ARM/Mips64/E2K. С.4 обещает User Guide, Installation Guide, Developer SDK и developer portal; наличие перечисления не подтверждает доступ к этим артефактам. Версионная ABI-матрица не дана.

## W1-04-S07 — https://lin-q.ru/docs

TinyFish получил страницу и ссылки на семь hardware manuals, framework guide и datasheets. robots metadata `noindex,nofollow`. Web open tool отказал, поэтому отказ одного способа не равен закрытой документации.

## W1-04-S08 — https://lin-q.ru/hr

Web: вакансия C++ описывает существующий Python cloud-inference prototype и C++ пре-альфа. Контейнеризация Docker/Kubernetes относится к направлениям дальнейшей проработки. Дата вакансии не установлена. Это дополнительная зацепка к облачной ветке, не контракт production service и не Dockerfile.

## W1-04-S09 — https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/

Web PyPA spec: три части wheel compatibility tag относятся к interpreter/version, ABI и platform. `py3-none-any` сам по себе не описывает все внешние и транзитивные зависимости и не подтверждает поддержку Windows всего LinQ stack.

## W1-04-S10 — историческая страница и недоступные guides

https://hi-tech.org/services/tenzornyie-vyichisleniya/frejmvorki/frejmvork-fw-tpu-h → TinyFish final URL https://hi-tech.org/local/get/?ACTION=SERVICE&EL=663/ . Страница описывает Python3.8 и CLI, OEM поставку, ссылается на:

- https://hi-tech.org/solutions/sol/frejmvork-fw-tpu-h-rukovodstvo-polzovatelya.pdf
- https://hi-tech.org/solutions/sol/frejmvork-fw-tpu-h-instrukcziya-po-ustanovke.pdf

TinyFish обе ссылки: `target_unreachable`. Web install URL вернул нынешний HTML системного интегратора. Содержимое guides не изучено, версии и требования не восстановлены.
