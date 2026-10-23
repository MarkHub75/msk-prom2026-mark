# Environment smoke test

- Main agent: GPT-6-based Codex; exact model identifier and reasoning effort are not exposed in this session.
- Web search: succeeded with one search for `LinQ HiTech AI accelerator lin-q.ru`. Result: "Ускорители для искусственного интеллекта LinQ" — https://lin-q.ru/
- Sub-agent spawning: available through `collaboration.spawn_agent`; exactly one sub-agent was successfully spawned.
- Sub-agent settings: reasoning effort was explicitly set to `medium` and accepted. The tool exposes a `model` override parameter, but no model override was requested or tested; the default model was used. Setting effort required `fork_turns: "none"`.
- Concurrency: 4 total active-agent slots, including the main agent, allowing up to 3 concurrent sub-agents while the main agent is active.
- Limits/errors: no tool errors observed. Exact main-agent model identifier and effort are unavailable; model override capability was not tested.
