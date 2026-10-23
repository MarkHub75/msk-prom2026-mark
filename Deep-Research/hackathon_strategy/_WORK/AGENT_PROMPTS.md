# Реестр индивидуальных заданий

Общие обязательные условия в каждом задании ниже конкретизированы файлами _WORK/PROMPTS. Каждый агент читает оба входных файла целиком, работает с самостоятельным контекстом, сохраняет результат и материалы в своём каталоге. Модель и effort реально передаются параметрами spawn_agent; текст задания не используется как замена настройки.

| Роль | Модель | Effort | Файл задания | Результат |
|---|---|---|---|---|
| W1A | gpt-6.1-sol | medium | PROMPTS/W1A.md | W1/W1A_RULES.md |
| W1B | gpt-6.1-sol | medium | PROMPTS/W1B.md | W1/W1B_HISTORY.md |
| W1C | gpt-6.1-sol | medium | PROMPTS/W1C.md | W1/W1C_ANALOGUES.md |
| W1D | gpt-6.1-sol | medium | PROMPTS/W1D.md | W1/W1D_EXECUTION.md |
| W1E | gpt-6.1-sol | medium | PROMPTS/W1E.md | W1/W1E_EVIDENCE.md |
| W1F | gpt-6.1-sol | medium | PROMPTS/W1F.md | W1/W1F_DEFENCE.md |

Поздние роли и задания будут добавляться при соответствующих переходах, после получения реального материала.

| CRITIC | gpt-6.1-sol | high | PROMPTS/CRITIC.md | ../CRITIC.md; CRITIC_HANDOFF.md |
| COLLECTOR (подготовлен, ещё не запущен) | gpt-6.1-sol | high | PROMPTS/COLLECTOR.md | четыре доказательных файла |
| AUTHOR (подготовлен) | gpt-6.1-sol | high | PROMPTS/AUTHOR.md | AUTHOR_DRAFT.md |
| EDITOR (подготовлен) | gpt-6.1-sol | high | PROMPTS/EDITOR.md | ../report_human_hackathon_strategy.md |
| COMPRESSOR (подготовлен) | gpt-6.1-sol | high | PROMPTS/COMPRESSOR.md | ../report_machine_hackathon_strategy.md |

| W2A | gpt-6.1-sol | medium | PROMPTS/W2A.md + CRITIC_HANDOFF W2-A | W2/W2A_BINDING_RULES.md |
| W2B | gpt-6.1-sol | medium | PROMPTS/W2B.md + CRITIC_HANDOFF W2-B | W2/W2B_WINNER_ARTIFACTS.md |
| W2C | gpt-6.1-sol | medium | PROMPTS/W2C.md + CRITIC_HANDOFF W2-C | W2/W2C_LINQ_PRECEDENT.md |
| W2D | gpt-6.1-sol | medium | PROMPTS/W2D.md + CRITIC_HANDOFF W2-D | W2/W2D_MINIMUM_EVIDENCE.md |

## Фактическое исполнение после второй волны

- W2A/B/C/D: все четыре запущены и завершены, gpt-6.1-sol, medium, fork_turns=none.
- CRITIC: завершён отдельным агентом gpt-6.1-sol high, fork_turns=none; новой сети не было.
- COLLECTOR: запущен 23.10.2026 около10:17+03:00, gpt-6.1-sol high, fork_turns=none; четыре доказательных файла, никаких новых сетевых доказательств.
- AUTHOR, EDITOR, COMPRESSOR: пока только подготовлены, запуск будет строго по очереди после handoff предыдущей роли.

- COLLECTOR завершён: окончательные75S/110F/32Q/10E/14QA, четыре доказательных файла, ID_MAP и COLLECTOR_HANDOFF.
- AUTHOR запускается после завершения collector: gpt-6.1-sol high, fork_turns=none, PROMPTS/AUTHOR.md; новая сеть запрещена.

- AUTHOR завершён: AUTHOR_DRAFT.md и AUTHOR_NOTES.md; собственная проверка записи, никаких новых доказательств/экспериментов.
- EDITOR фактически запущен после окончательного author handoff: gpt-6.1-sol high, fork_turns=none, PROMPTS/EDITOR.md. Его владение — report_human_hackathon_strategy.md и EDITOR_NOTES.md; задача литературная, не дополнительный аудит.

- EDITOR завершён: report_human_hackathon_strategy.md и EDITOR_NOTES.md; литература/перенос путей/собственная согласованность, без новой исследовательской стадии.
- COMPRESSOR фактически запущен после окончательного editor handoff: gpt-6.1-sol high, fork_turns=none, PROMPTS/COMPRESSOR.md. Последняя роль, владение report_machine_hackathon_strategy.md и COMPRESSOR_NOTES.md; после неё нет аудитора.

- COMPRESSOR завершён: report_machine_hackathon_strategy.md и COMPRESSOR_NOTES.md. Все15дочерних ролей исполнены с указанными model/effort/fork_turns. После окончательного handoff нет новых ролей или проверочной стадии; корень обновил только служебный журнал и передал результаты.
