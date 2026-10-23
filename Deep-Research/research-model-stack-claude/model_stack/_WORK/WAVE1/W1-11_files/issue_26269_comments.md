--- UltralyticsAssistant 2026-09-21T23:10:23Z
👋 Hello @davidnichols-ops, thank you for the detailed reproducible report showing prediction differences between `.pt` and static ONNX models on non-square inputs, including the controlled parity test and cross-platform results. This provides useful evidence that the discrepancy is in the preprocessing path rather than normal export numerical variance.

An automated response has been added, and an Ultralytics engineer will assist soon. We’ll investigate the letterboxing consistency between PyTorch and static ONNX inference, including the behavior of `rect`, static versus dynamic exports, and the proposed parity-test conditions. Your MRE and measurements should be sufficient for initial investigation.
--- Y-T-G 2026-09-22T11:15:13Z
Thanks for reporting.

This isn't a bug. It's expected behavior.

Passing an integer as `imgsz` never claims to guarantee exact square inference. It only guarantees one of the sides would be equal to that. It just means that the longest side is guaranteed to be `imgsz` and the other side would be dynamically determined which depends on whether the model supports dynamic input.

The first suggestion can't be implemented because it will change the behavior is hundreds of thousands of workflows that are live today.

The second is already mentioned in the docs:
https://docs.ultralytics.com/modes/predict#inference-arguments

We already have mAP regression tests as part of benchmarks CI.

For parity tests, you should back up the PR by demonstrating an actual regression that was missed due to the lack of test.
--- davidnichols-ops 2026-09-22T13:38:56Z
Thanks — the `rect=True` note in the predict docs ("backend supports it (PyTorch .pt, or dynamic ONNX / Triton)") covers the behavior I flagged, so I'll take this as expected behavior. Withdrawing suggestion 1 — the compatibility argument is sound — and suggestion 3, since I don't have a demonstrated missed regression to justify the test.

One optional gap: the export docs don't mention the user-visible consequence — a static export runs at full `imgsz`, so on non-square sources its detection set can differ from `.pt` predictions (detections near the confidence threshold can drop; `dynamic=True` or square inputs avoid it). Happy to send a one-sentence docs patch for that if useful; otherwise feel free to close.

--- rromanchuk 2026-09-22T16:56:11Z
something regressed/was fixed with onnx exporting, sanity tests immediately started exploding. Based on title I figured this is unrelated, but timing alone is making me think it's directly related.  I have to gather information first, but just an early PSA. I noticed there has been some re-work of flags so going to start updating my `half` and `end2end` usage 

Longs standing export options were: 
`model.export(format="onnx", half=True, dynamic=True, simplify=True)`


--- rromanchuk 2026-09-22T17:26:19Z
just needed explicit `nms=false`,  it was exporting anchors, looks like the unset default changed
--- pderrenger 2026-09-22T19:27:54Z
Thanks for confirming. To clarify, `nms=None` exports raw one-to-many predictions for external NMS, while `nms=False` explicitly selects the NMS-free one-to-one head; this is an output-head difference rather than exported anchors and is unrelated to the rectangular-letterboxing behavior. See the [end-to-end detection guide](https://docs.ultralytics.com/guides/end2end-detection#exported-outputs).
