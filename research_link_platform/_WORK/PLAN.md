# LinQ research execution plan
Started 2026-10-23 04:15 Europe/Moscow / 01:15 UTC. Historical preparation context: night of 23 Oct 2026.

User requested same folder: use research_link_platform directly, overriding nested linq_platform instruction. Preserve original prompt.

## Capability and role allocation
Three simultaneous child slots; queue 15 separate W1 tasks, then fresh critic high, substantive W2 medium tasks based on K IDs, assembler high, author high, editor high, compressor high. All children explicitly gpt-6.1-sol, fork_turns none. Current orchestrator model/effort cannot be changed/verified by spawn tool; do not claim it was switched. No global settings changed.
Tools: web__run/search_service_web_run, TinyFish fetch/search, GitHub connectors, exec HTTP/file operations available. Actual SDK/device access: none at start. No mail/account creation, resource rental, training or prototype implementation.

## Wave 1 ownership and decisions
01 names/history; 02 hardware; 03 SDK/documentation + official case/timeline; 04 environment; 05 import; 06 operators/compiler; 07 quantization; 08 model compatibility; 09 runtime/access; 10 video/tensors; 11 performance; 12 diagnostics; 13 ecosystem; 14 integrations; 15 execution evidence.
Individual prompts W1_NN_PROMPT.md explain sources, decision relevance, depth, evidence conditions and ownership. Results W1_NN_RESULT.md; private auxiliary W1_NN/.
Dependencies: 01/02 prevent product confusion; 03/04 determine feasible setup; 05–08 inform model_stack; 09/10/15 constrain architecture and proof; 11 prevents unsupported camera promises; 12–14 expose reproducibility gaps. Share critical findings without duplicating branches.
Enough evidence means useful engineering answer or concrete unknown with recorded search and resolution path, never a source-count target.

## Pipeline and outputs
W1 -> fresh-context critic CRITIC.md -> W2 tasks tied to K IDs, attempt falsification -> assembler SOURCES.md RAW_FACTS.md OPEN_QUESTIONS.md + K dispositions -> author _WORK/HUMAN_DRAFT.md -> editor report_human_linq_platform.md -> compressor report_machine_linq_platform.md with required YAML metadata/index fields.
No final auditor or third web wave. Exactly six generated final Markdown files in research root, original prompt preserved. Working artifacts only _WORK. All significant knowledge has provenance/status, dates, and honest test boundary. Future experiments E IDs and conditional routes R IDs in reports. Final response Russian with links and limits.
