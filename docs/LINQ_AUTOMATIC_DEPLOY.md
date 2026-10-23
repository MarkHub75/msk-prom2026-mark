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

The initial command stopped at upload_preflight with jupyter_upload_agent_not_ready, publish_attempted=false. No Helmet bytes or Helmet inference were sent. All local model/golden/preprocessing checks passed. Ordinary mixed-pose remains excluded because its confidence quantization failed; only pose-split is allowed.

## Network recovery work

Current transport has UUID, finite deadlines, exact ID/status checks and no blind publisher retry. The new infrastructure may reconnect the tunnel independently; Vast never edits autossh/systemd, SSH, NetworkManager or VPN configuration. A lost connection after a possible publication must remain UNKNOWN until a correlated reply or an actual completion witness is recovered. Broker confirmation alone is not worker completion.

Durable request intent, retained ambiguous reply queues and receive-only reconciliation are the next transport changes. They must be covered by new failure/crash tests, rather than repeating prior model/network experiments. A restored TCP connection alone must never cause the previous TPU task to be sent again.
