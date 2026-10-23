# Индивидуальные задания и фактические запуски

Полные самодостаточные задания первой волны сохранены отдельно; шаблон модели/effort применяется параметрами spawn_agent, не только текстом.
- W1-01 : [PROMPT_W1_01.md](PROMPT_W1_01.md) → W1_01.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-02 : [PROMPT_W1_02.md](PROMPT_W1_02.md) → W1_02.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-03 : [PROMPT_W1_03.md](PROMPT_W1_03.md) → W1_03.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-04 : [PROMPT_W1_04.md](PROMPT_W1_04.md) → W1_04.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-05 : [PROMPT_W1_05.md](PROMPT_W1_05.md) → W1_05.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-06 : [PROMPT_W1_06.md](PROMPT_W1_06.md) → W1_06.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-07 : [PROMPT_W1_07.md](PROMPT_W1_07.md) → W1_07.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-08 : [PROMPT_W1_08.md](PROMPT_W1_08.md) → W1_08.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-09 : [PROMPT_W1_09.md](PROMPT_W1_09.md) → W1_09.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-10 : [PROMPT_W1_10.md](PROMPT_W1_10.md) → W1_10.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-11 : [PROMPT_W1_11.md](PROMPT_W1_11.md) → W1_11.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-12 : [PROMPT_W1_12.md](PROMPT_W1_12.md) → W1_12.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-13 : [PROMPT_W1_13.md](PROMPT_W1_13.md) → W1_13.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-14 : [PROMPT_W1_14.md](PROMPT_W1_14.md) → W1_14.md; gpt-6.1-sol / medium / fork_turns=none.
- W1-15 : [PROMPT_W1_15.md](PROMPT_W1_15.md) → W1_15.md; gpt-6.1-sol / medium / fork_turns=none.

## Аналитические и авторские роли
- critic: [PROMPT_CRITIC.md](PROMPT_CRITIC.md), реально запущен отдельно gpt-6.1-sol/high/fork_turns=none после15W1.
- collector: [PROMPT_COLLECTOR.md](PROMPT_COLLECTOR.md), ожидает W2.
- author: [PROMPT_AUTHOR.md](PROMPT_AUTHOR.md), ожидает evidence assembly.
- editor: [PROMPT_EDITOR.md](PROMPT_EDITOR.md), ожидает draft.
- compressor: [PROMPT_COMPRESSOR.md](PROMPT_COMPRESSOR.md), ожидает финальный human report.
Имена назначают параметры при запуске; четыре будущие записи не заявляют фактическое выполнение.


## Вторая волна
- Семь полных PROMPT_W2_01…07.md с точными K sections/source targets/stop conditions.
- W2_01, W2_02, W2_03 запущены отдельно gpt-6.1-sol/medium/fork_turns=none; остальные ожидают слотов.
- При генерации initial regex пропустил таблицу04 из-за отсутствия пробела; полный PROMPT_W2_04 восстановлен до запуска. Семь независимых задач сохранены.

- Все7W2 завершены (см. W2_MANIFEST.json).
- collector реально запущен gpt-6.1-sol/high/fork_turns=none после обеих волн. Владение: SOURCES/RAW_FACTS/OPEN_QUESTIONS + CRITIC disposition и служебные handoff/mapping; другие роли пока не пишут общие файлы.

- collector завершён: см.COLLECTOR_NOTES/AUTHOR_HANDOFF.
- author реально запущен отдельно gpt-6.1-sol/high/fork_turns=none; PROMPT_AUTHOR.md → DRAFT_HUMAN.md + AUTHOR_NOTES.md.

- author завершён, см.AUTHOR_NOTES.
- editor реально запущен gpt-6.1-sol/high/fork_turns=none; PROMPT_EDITOR.md → report_human_model_fidelity_quantization.md + EDITOR_NOTES.md.

- editor завершён, см.EDITOR_NOTES; finalhuman готов.
- compressor реально запущен gpt-6.1-sol/high/fork_turns=none; PROMPT_COMPRESSOR.md → report_machine_model_fidelity_quantization.md + COMPRESSOR_NOTES.md. Последняя авторскаяроль, отдельногоfinalreview нет.

- compressor завершён24.10.2026 00:05:42MSK; report_machine иCOMPRESSOR_NOTES готовы. Все согласованныероли завершены; дополнительныхролей/финальноговалидаторанет.
