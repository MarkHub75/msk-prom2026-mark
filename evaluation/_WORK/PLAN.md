# PLAN — evaluation

The useful output is a reproducible chain from a system claim to observable truth, evaluation unit, matching rule, numerator/denominator, uncertainty and an engineering decision. Object AP, person-state correctness, event usefulness and verified LinQ execution remain separate claims.

## Sequence and ownership

Fifteen independent medium researchers execute in five queues of three. Each reads the common instructions and its individual assignment in `AGENT_PROMPTS.md`, opens primary sources, retains versioned evidence and writes only its own `W1_XX.md` (and its own source subdirectory if useful). The root coordinates and records transitions.

| Cell | Question / decision | Initial evidence route | Output |
|---|---|---|---|
| 01 | Truth, visibility, unknown and annotation agreement; what can be labeled? | Annotation primary methodology, benchmark annotation policies | W1_01.md |
| 02 | Exact object AP and matching; can two detector results be compared? | COCO evaluator source at pinned commit | W1_02.md |
| 03 | Person–PPE ownership and full-chain evaluation | Primary PPE annotation/evaluation, component oracles | W1_03.md |
| 04 | Zone geometry and boundary truth | Primary geometry APIs and camera calibration | W1_04.md |
| 05 | Temporal event matching, duplicates and censoring | ActivityNet/DCASE/event localization evaluator code | W1_05.md |
| 06 | False alerts and exposure; what does zero establish? | Primary statistical definitions and video event protocols | W1_06.md |
| 07 | Group splits and leakage; what population is tested? | Official split APIs and original leakage studies | W1_07.md |
| 08 | Threshold selection, calibration and abstention | Guo paper, official calibration/threshold docs | W1_08.md |
| 09 | Tracking metrics versus alert continuity | TrackEval code and HOTA paper | W1_09.md |
| 10 | Export/quantization parity; where does behavior change? | Official runtime/export/quantization guidance | W1_10.md |
| 11 | Timing boundaries, clocks and freshness | MLPerf, TensorRT timing guidance, primary clock docs | W1_11.md |
| 12 | Load, drops, availability and coverage | MLPerf loadgen, primary workload/failure accounting | W1_12.md |
| 13 | Small-sample uncertainty and paired comparison | SciPy bootstrap, primary proportion/rate procedures | W1_13.md |
| 14 | Error taxonomy and causal diagnosis | TIDE source/paper, oracle and ablation methods | W1_14.md |
| 15 | Reproducible harness, honest demo, official case/LinQ evidence | Official event site/rules and LinQ pages, evaluator artifacts | W1_15.md |

After all results: prepare neutral handoff → independent high critic writes `CRITIC.md` with K-IDs → medium second wave addresses actual gaps, including attempts to refute key recommendations → high collector writes three registries and dispositions in CRITIC → high author writes Russian draft → high editor publishes Russian report → high compressor publishes English report with valid YAML front matter. No extra final verification role.

## Evidence requirements

Each used primary source: URL, author, publication/version date (or unknown), access time with timezone, locator, commit where code matters, factual retrieval status. Each important observation: branch-prefixed ID, source/locator, actual inspection versus execution, applicability, edge cases, alternative explanation. Own derivations and proposed protocols explicitly identified. Preserve unresolved official data, metrics and LinQ access as actionable questions.

## Final deliverables

## Adaptive second wave after fresh criticism

Four distinct gaps warrant new evidence rather than repeating all fifteen first-wave topics. The critic found adequate coverage of AP/person separation, unknown truth, grouping/leakage, calibration, few-group uncertainty, basic timing and workload failure accounting.

| Cell | Critic issues | New evidence / decision | Owner output |
|---|---|---|---|
| W2_01 | K001 | Exact public LinQ sync/TLM/manual/version and placement scope; distinguish documentation from actual assigned environment | `_WORK/W2_01.md` |
| W2_02 | K002–K003 | Exposure estimands, sufficient review, source cohort versus delivery workload, delayed-alert/drain attribution | `_WORK/W2_02.md` |
| W2_03 | K004 | Probability-sampled review, onset-owned events, inclusion probabilities and boundary/length bias | `_WORK/W2_03.md` |
| W2_04 | K005–K006 | Deterministic matching fixtures, uncertain onset and censoring, lexicographic ties and latency interpretation | `_WORK/W2_04.md` |

Each cell receives full common context and individual task in `_WORK/W2_AGENT_PROMPTS.md`; requested profile stays `gpt-6.1-sol`, medium, fresh context. Execute three at a time then refill one slot. No third wave or final auditor. Collector resolves all K-IDs by evidence or explicit Q-ID and preserves original criticism.

`SOURCES.md`, `RAW_FACTS.md`, `CRITIC.md`, `OPEN_QUESTIONS.md`, `report_human_evaluation.md`, `report_machine_evaluation.md`. No global INDEX or extra final report. Experiment cards E-IDs and addressed handoffs live in these files.
