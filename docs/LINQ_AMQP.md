# One-request LinQ AMQP capture

`ml.linq.amqp` performs exactly one publish through the current tunnel `127.0.0.1:15672`. It does not create a VPN, invent broker credentials, select another program after failure, or retry an ambiguously accepted request.

The user has confirmed a successful stock notebook call (`status_code=0`, class 257, reported 0.39 s). The current client uses the actual transferred `tpu_pycloud_format` source, not a replacement serializer. Agent-side transport tests are mocked; a stock notebook result is not an agent-side own-model capture.

## Actual inspected protocol

- Official `PyTask(data=inputs)` has no task-ID field. `serialize(PyTask)` returns bytes.
- `deserialize(body)` returns `(data, metadata, worker_data)`. Only selected numeric `data` arrays and numeric `worker_data['status_code']` are used. Worker metadata and raw error objects are never dumped.
- Correlation is the AMQP header `tpu_pycloud_message_id`.
- Exact target URI is header `uri`; it is not reconstructed from an arbitrary filename.
- `response_routing_keys` is a JSON list. For the confirmed direct reply it contains the explicitly created reply queue.
- User-confirmed request/reply exchange: `tpu.direct`; request routing key: `input`; reply queue: `notebook_{request_id[:8]}`, auto-delete, bound to `tpu.direct` using its own name. The client additionally makes the unique reply queue exclusive so closing the connection removes it.
- Confirmed stock URI pattern: `file:///auto/cache/<actual LinQ login>/torch_resnet50_b1_o5_h1m.tpu?raw=False`. `--login-env LINQ_LOGIN` composes ONLY this explicitly confirmed stock URI. The actual login must already be configured privately. Alternatively pass an exact `--target-uri`; never pass auth tokens in it.

## Exact format dependency

Only version `0.0.1` is accepted. A normal installed distribution must report exactly that version. The user transferred source-only code without dist-info; that route requires an explicit reviewed manifest, `/workspace/artifacts/linq-rpc/format-source.json`, with distribution, version and SHA256 for `__init__.py`, `_io.py`, `headers.py`, `message_pb2.py` and `message.proto`. The loader verifies all five source files and rejects unreviewed active Python files before importing the package. Its version attribution remains the user's official-source attestation; hashes provide local consistency, not independent upstream authenticity.

`PYTHONPATH` must explicitly include the transferred module directory. No PyPI substitute, copied protobuf schema or fallback serializer is generated. Missing/wrong format produces a stable action error before opening a broker connection.

## Private broker configuration

Choose an existing private file **outside Git** containing exactly `username`, `password`, `virtual_host`. Pass only its path via `--connection-config`. No contents are printed or copied into capture artifacts. Alternatively set exactly `LINQ_AMQP_USERNAME`, `LINQ_AMQP_PASSWORD`, `LINQ_AMQP_VHOST` in the user's protected runtime environment. There are no guest/default credential guesses and no history/store scans.

All connection host/port values are overridden on a copy of the supplied parameters and restricted to `127.0.0.1:15672`. The original credentials/TLS object is not printed or mutated. Socket, connection-stack and broker-blocked waits are bounded; polling has a total deadline. A timeout does not cancel remote TPU execution or prove nonacceptance. One published request must be reconciled before anyone considers another request.

## Prepared stock request (root performs the authorized live call)

The placeholders below require actual configured values; do not run until those are confirmed. Input NPZ is already the exact vendor-preprocessed float32 `input.1` tensor `[1,3,224,224]`. Expected selected output is `495`; the observed actual shape/dtype is recorded rather than guessed.

```bash
PYTHONPATH=/workspace/linq-client:/workspace/project \
/workspace/.venvs/linq-client/bin/python -m ml.linq.amqp \
  --format-source-manifest /workspace/artifacts/linq-rpc/format-source.json \
  --connection-config /EXPLICIT/PRIVATE/connection.json \
  --exchange tpu.direct --routing-key input --reply-exchange tpu.direct \
  --notebook-reply-queue --login-env LINQ_LOGIN \
  --program-file /workspace/artifacts/linq-api/torch_resnet50_b1_o5_h1m.tpu \
  --input-npz /workspace/artifacts/linq-rpc/resnet50/inputs.npz \
  --output-name 495 --model-id stock-resnet50 \
  --output-dir /workspace/artifacts/linq-rpc/NEW-CAPTURE-DIRECTORY \
  --timeout 60 --host 127.0.0.1 --port 15672
```

`--program-file` supplies **local expected program bytes** for SHA256; it does not prove the remote URI loaded those same bytes. Only after checking the remote program identity may the caller add `--attest-program-match`. `--attest-linq-placement` is likewise user/runtime attestation, never independent chip verification.

A new capture directory contains `capture.json`, `inputs.npz`, validated `outputs.npz` and safe `response.json`. Response diagnostics contain generated UUID, numeric status, publish/completion state, timings and numeric output names/shapes/dtypes. They omit connection parameters, target URI, worker identifiers and arbitrary metadata. On service failure, only a bounded 1024-character error excerpt is exposed after removing the explicitly supplied password and credential-like URI/query fields. `--save-service-error` additionally writes that same sanitized excerpt privately to `service-error.txt`; it never writes the raw worker metadata/error object. Error output is reduced to code/phase/type when serialization or connection fails.

Publisher confirmation is enabled and `mandatory=True` is set; there is one publish attempt even if the confirmation/connection fails. An ACKed correlated nonzero response remains a failed capture; outputs are not fabricated. The connection is closed in `finally`. Local timeouts/connection closure never imply remote cancellation.

## Explicit binding extension

If the actual notebook uses a different reply route or task construction, use `--binding private_module:create_binding`; the callable takes no arguments and returns `AmqpBinding` or its exact field mapping. Keep the binding outside Git when it accesses protected config. It must not open a connection itself.

Required fields: actual `parameters`, `task_factory(request_id,reply_queue,inputs,program)`, `get_response_id(decoded,amqp_properties)`, `get_status(decoded)`, `get_outputs(decoded)`, explicit `output_names`, `request_exchange`, `request_routing_key`, and `reply_policy`. Policies are `default_exchange` or `custom_setup`, the latter requiring `reply_setup(channel,reply_queue,request_id)`. Optional factories are `properties_factory(request_id,reply_queue,program)` and `reply_queue_factory(request_id)`. No PyTask kwargs/response positions are guessed by the generic binding path. A format source manifest must still be supplied and verified.

No live request was sent while implementing/testing this module. Tests cover mock success, exact headers/queue policy, ID mismatch, timeout, nonzero status, one ambiguous publish, close-on-error, serialization failure, finite-output validation, credential redaction and missing/wrong dependency guards.
