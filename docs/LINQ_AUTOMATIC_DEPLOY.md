# Automatic Helmet -> Split-Pose deployment

Stock ResNet50 is already completed and integrity-checked. Do not repeat its request or configure VPN/SSH again. Raw results remain outside Git at /workspace/artifacts/linq-rpc/resnet50-001/.

## Separate upload channel

The existing RabbitMQ tunnel transports bytes; it grants no filesystem access. A dedicated broker queue successfully carried the reviewed Helmet-sized binary, but remote file writes require an explicit helper inside the authorized Jupyter kernel. It uses the real PyTask/serialize/deserialize and the same AmqpRunner on Vast. It never targets tpu.direct/input for upload.

The bootstrap has been published. On Arch, in the already authenticated stock notebook, execute the entire cell from:

`/workspace/artifacts/linq-rpc/start_jupyter_upload.py`

The cell derives the cache directory from the successful stock headers, checks that stock file is visible, verifies the two-file helper ZIP by SHA256 and starts a separate connection/consumer. It does not export notebook auth/session data, read browser credentials, or change the existing channel. Only the two pinned model blobs are accepted, with an8MiB size cap,4messages and300seconds lifetime. It cannot choose arbitrary target paths or execute uploaded code. The bootstrap code itself is explicitly reviewed and hash-pinned before the user's import.

Expected status: UPLOAD_AGENT_READY. If the stock cache is not visible, stop: this is an actual filesystem boundary, not a reason to guess a different URI. After initial setup, `restart_linq_upload_agent()` restarts the same bounded service inside that notebook without another bootstrap download.

## One command on Vast

```bash
bash /workspace/project/scripts/linq_models_auto.sh all
```

Or select only `helmet` or `pose-split`. The command reads the existing private connection.env without echoing it. It checks prerequisite results, reviewed program hashes and an active upload consumer before publishing. It uploads each program with the existing AMQP client, verifies the returned SHA256/byte count, then calls the actual TPU worker. The program URI remains in the confirmed configured account's cache; no alternative path is substituted.

Outputs are /workspace/artifacts/linq-rpc/helmet-001/ and pose-split-001/. They include numeric captures, integrity review, decoded objects, numeric comparison and model-check report. Same-input smoke acceptance requires reference detections matched class-wise with IoU>=.5; Split-Pose must retain visible keypoints. This is not target-video accuracy acceptance.

Both first actual own-model calls completed on 2026-10-23 with matching response IDs, status 0 and capture-integrity/ABI/smoke PASS:

| Model | Request UUID | Full AMQP call | Decoding |
|---|---|---|---|
| Helmet | 262bdaa1-c24b-48ac-b073-6b28fd014248 | 10234.49 ms | 2 bare_head, scores 0.352586/0.259503; reference 1 matched at IoU 0.925226, 1 extra actual |
| Split-Pose | 1f986b07-896d-48b9-8b4f-6ce2d0f8dc16 | 11152.85 ms | 3 persons; visible keypoints 16/17/9; box IoU 0.7812..0.9108 |

These timings include connection/setup/wait/close, not just TPU compute. The Helmet extra detection is recorded, not hidden by the smoke gate. Target-video precision/recall and end-to-end video performance remain unmeasured. Re-running the command reuses these completed results; it does not submit a new inference.

After the user started the Jupyter helper, both uploads completed with correlated replies and matching remote SHA256/byte counts. Receipts are outside Git in /workspace/artifacts/linq-rpc/{helmet,pose-split}/staging-receipt.json. Helmet: 2,751,596 bytes, SHA 408fa39cebc6d971a28ad41fb0ec4b81eee5ae50c175af699860a221770b32aa. Split-Pose: 2,929,222 bytes, SHA c3ad355488a293203131a541bb366a91b89a5cc17bdec1609a5ba705c1fe247b. A completed staging receipt is reused without another upload. The helper's lifetime is no longer relevant to files already placed. Ordinary mixed-pose remains excluded.

## Network recovery work

The transport assigns a UUID and fsyncs its journal and capture association BEFORE opening the connection. The authenticated AMQP handshake, reply setup and (for uploads) active Jupyter consumer check must succeed before publication. These establish broker/channel availability, not TPU capacity. Each operation has a finite deadline and exactly one publisher attempt. The tunnel may reconnect independently; Vast never edits autossh/systemd, SSH, NetworkManager or VPN configuration.

States in /workspace/artifacts/linq-rpc/requests/<UUID>/request.json:

| State | Meaning | Next action |
|---|---|---|
| NOT_SUBMITTED | Publication has not started | Preserve the failed attempt; a fresh UUID is safe |
| SUBMITTING | Durable intent precedes a possible publish | After restart, treat as UNKNOWN |
| ACCEPTED | Broker publisher confirmation received | Await the correlated worker response; not completion |
| UNKNOWN | Timeout, connection loss or crash after possible publish | Receive only from the retained reply queue |
| COMPLETED | Matching ID, status0, validated numeric outputs durably saved | Use local tensors; no network needed |
| SERVICE_FAILED | Matching worker response reports nonzero status | Report the failure; do not automatically resubmit |

Run the SAME command after restoration. The orchestrator locks concurrent invocations, reuses valid staging receipts and completed captures, and reconciles pending UUIDs through the existing AmqpRunner. It never rebuilds or republishes a pending TPU request. A durable NOT_SUBMITTED record is the sole fresh-attempt condition. Legacy uncertain captures without a journal association stop for explicit completion evidence.

The response NPZ and terminal metadata are fsynced BEFORE broker ACK. A crash while assembling capture.json/outputs.npz is repaired from that durable response, preserving inputs and validating hashes. Completed results are not appended twice. A restored TCP connection, an empty queue, or a missing queue never proves that an earlier TPU task did not execute. If a correlated response cannot be recovered, the request stays UNKNOWN until an actual completion witness is available; this deployment has no separate organizer task-status API.

The request lock must be acquired before interpreting NOT_SUBMITTED, including when another direct client is still in preflight. Reconciliation time is reported separately from the original full-call latency. The 60-second polling deadline can be exceeded by blocking Pika RPC/close while the session heartbeat detects failure; it is not remote cancellation.

Only new/affected failure and recovery tests are run for these changes. Stock ResNet50 and prior model preparation checks are not repeated.
