# Behavioral models and video data — plan

Started 2026-10-23T22:12:28+03:00, Europe/Moscow. Context mosprom-research-v1.

Both input prompts read completely. Six deliverables at this workspace root; all intermediate work under `_WORK/`.

## Real execution settings

Delegation exists via collaboration.spawn_agent; explicit `model=gpt-6.1-sol`, `reasoning_effort=medium/high`, `fork_turns=none`. Three child slots available concurrently (four total including root). Root model/effort cannot be changed from inside this session; no global settings will be modified. Child settings are explicit and logged. Finished slots will be reused or subsequent agents launched as supported; actual counts recorded.

## Pipeline and ownership

1. W1: sixteen individually assigned independent searches M01–M08, D09–D16 with private outputs. Exact topic sections copied to individual prompts. Read neighboring findings as internal secondary leads and verify primary artifacts. Avoid repeating broad feasibility research.
2. Fresh High critic reads W1 and original briefs, writes CRITIC.md before any W2 search.
3. W2: 6–10 targeted Medium searches derived from K IDs, aimed at decisive artifacts, semantics, limits and independent counterevidence.
4. Separate High collector sequentially owns SOURCES.md, RAW_FACTS.md, OPEN_QUESTIONS.md and appends outcomes to CRITIC.md. No new network research.
5. Separate High writer creates Russian draft; separate High editor saves final human report; separate High compressor saves English report and performs its own content/format checks. No final auditor or third search wave.

## Synthesis requirements

All eight case scenarios; method/weights/video/annotation compatibility; exact artifact URLs and provenance; status and separate code/weights/data rights; hard negatives; conditional 2–3 MVP shortlist and 1–2 additional hazards only if supported; three routes (detector/tracker rules, pose temporal, video model); video/subject/site split; causal event metrics; PTS-preserving low-FPS tests; proposed eight-stage experiments, kill gates and handoffs. No training, paid compute, implementation, outreach or fabricated LinQ support.

## Local leads

Original case found at `../LinQ-case-analytics-research/КЕЙС_LinQ.pdf`; inspect locally. Existing machine reports in `../prompt_behavioral_safety_feasibility_16_agents/`, `../prompt_cv_accuracy_vast_research/`, `../prompt_camera_calibration_geometry_6_agents/`, `../datasets/`, `../evaluation/`, `../research_link_platform/`. These are secondary internal sources with their own dates, not independent primary verification.
