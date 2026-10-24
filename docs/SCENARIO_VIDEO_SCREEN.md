# Existing industrial-video screen: all eight scenarios

No violation episode was established. This bounded AI visual screen reviewed the
existing producer READY `mendeley-factory-replay16/v1-20261024` solely for the
approved use **manual actor/zone/event annotation preparation**. READY scope and
all source hashes were verified before pixels and rechecked afterward. Producer
manifest SHA: `0a51efec6b04dba61bfde9ff24d8f48e418094b0f51789f35f49e5da99458a16`.
No new source, annotation GT, NN inference, training, GPU, compiler, LinQ request
or network operation was used. Original media and producer release are unchanged.

All16 videos were sampled at four equidistant encoded-PTS targets spanning their
first/last frames, selecting the nearest original decoded frame. Four private
contact sheets contain64 entries. Two additional bounded chronological contacts
(12 frames each from `3_tr45` and `6_tr15`) added20 distinct source frames, for84
unique viewed frames. This remains sparse visual screening, not exhaustive video
annotation or an action benchmark. Source filenames and source categories were
not interpreted as event/actor truth. No imagery is included in Git.

| Official scenario | Screen result | Remaining evidence |
|---|---|---|
|01 running/abrupt movement | UNKNOWN; visible aisle locomotion is not established running | Continuous action/trajectory review, camera geometry, policy. Not automatically selected for demo. |
|02 dangerous machinery/vehicle approach | CANDIDATE_FOR_REVIEW: `3_tr45`, `7_te4`, `7_tr15` show a moving forklift/stack beside an occupied work area | Vehicle/person tracks, depth/ground-plane or explicit calibrated danger zones, machine motion and safe-separation policy. Visible movement is not a proven unsafe approach. |
|03 phone during equipment work/movement | UNKNOWN; no phone object/use resolved | Phone ownership, visible wrist/head relation, action and work/motion facts. |
|04 smoking/open fire outside allowed places | Ambiguous-phenomenon review only: `5_tr19`, `6_tr15` show haze near machinery | Steam/dust versus smoke source, actual cigarette/flame and gesture, ownership and permitted zones. No smoking or fire positive established. |
|05 barrier crossing/under conveyor or suspended cargo | UNKNOWN; guards and equipment context visible, but no such whole-body passage established | Barrier topology, continuous person path and valid-entry policy; suspended-load/clearance evidence. |
|06 height work without harness | UNKNOWN; perspective/background operators do not establish physical elevation or harness state | Surveyed elevated area, visible working actor and harness/anchor state; absence is not a label. |
|07 fall/lying/immobility | UNKNOWN; no episode established in these samples | Continuous posture and visible floor evidence. Not automatically selected for demo. |
|08 unsafe cargo carrying | UNKNOWN for current person-carried-load rule | Forklift-carried stacks are transport context, not person-owned manual carrying. Need ownership and explicit observable carrying policy; no weight/medical inference. |

The enlarged temporal contact for `6_tr15` did **not** confirm an initial
thumbnail impression of a hand-to-face gesture: no phone/cigarette or smoking
action was resolved. Haze remains ambiguous. The forklift temporal contact shows
position change; danger, authorization, physical distance and driver visibility
remain unestablished. These distinctions prevent context from becoming invented
positive GT. Ordinary-looking walking/workstation scenes are candidates for
future ordinary-reference review, not labelled negative episodes.

Current trusted baseline classes are person/COCO17 pose and helmet/bare_head.
Specialist phone, cigarette/flame, steam discrimination, vehicle/machinery,
barrier, harness and cargo ownership coverage was not verified or asserted
complete here. No model predictions were consulted. Real-video and actual LinQ
quality gates for those scenarios remain open. Precision, recall, F1 and false
alerts/hour are NOT_MEASURABLE from this screen.

Private artifacts:
`/workspace/artifacts/matvey-scenarios/video-screen-v1/report.json` contains all
16 source/video hashes,64 original-frame timestamps, per-video all-eight status,
needed objects/facts, coverage and ordinary-reference limits. `screen-inputs.json`
and `sequence-inputs.json` preserve extraction provenance and original/decoder
clocks; `extract_contacts.py`, `extract_sequences.py`, `write_report.py` reproduce
the bounded screen inputs/metadata. Contacts/frames remain outside Git. Encoded
PTS is authoritative: OpenCV's relative clock can have an offset (notably the
39ms first encoded PTS of `6_tr15`), and both clocks are retained. The approved
private preparation scope does not itself establish public demo clearance,
independent evaluation, or exhaustive temporal GT.
