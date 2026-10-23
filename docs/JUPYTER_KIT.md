# Portable LinQ kit

Build from the existing repository and artifacts, without training or compilation:

```bash
python -m ml.pipeline.jupyter_kit --output /workspace/artifacts/linq-jupyter-kit.zip
```

Archive root: README.md, requirements.txt, verify_kit.py, guarded bindings.py, run_case.py, examples/, current minimal ml/ package, docs/, and models/{helmet,pose-split}/. Each model includes existing model.tpu, manifest.json, compile-report.json, inputs.npz, golden-outputs.npz and capture-transform.json. No PyTorch weights, ONNX/compiler, videos or authentication files enter this allowlist.

KIT-MANIFEST.json pins every other archive member by byte size and SHA256. verify_kit.py needs only the standard library. The archive checksum is recorded separately after building. Model files must match existing compiler hashes and the packaged golden inputs are compared byte-for-byte with the saved preprocessing result.

The user reports the stock example succeeded (status_code0, class257,0.39s). The actual remote import/call/result extraction is not present locally. The kit therefore marks actual_remote_api_binding NOT_PROVIDED_YET and refuses to send an invented request. A separate local pytpu example is labelled LOCAL. Complete the binding only from the credential-free actual notebook fragment; no passwords, tokens, cookies, usernames or full notebook outputs are needed.

Jupyter upload/extraction/capture instructions are in the archive README. First import verify_kit, then prepare_case('helmet'), then use the existing actual API to load that case's model.tpu and bind a callable. Capture one call; validate integrity and compare named outputs. Repeat with pose-split only after Helmet checks. Do not blindly set runtime_abi_verified or apply SDK simulator scales to runtime outputs.

Notebook comparison after a captured Helmet call:

```python
import json
from ml.pipeline.capture_review import review_capture
from ml.detection.compare_capture import load_numeric_npz, compare_captures

review = review_capture('capture-helmet-001', helmet['compile_report']['program_sha256'])
metadata = json.loads(Path('capture-helmet-001/capture.json').read_text())
comparison = compare_captures(
    helmet['golden_outputs'], load_numeric_npz('capture-helmet-001/outputs.npz'),
    manifest=helmet['manifest'], metadata=metadata,
)
print({'integrity': review['status'], 'numeric': comparison['status'],
       'decoded': comparison['decoded']['status']})
Path('helmet-comparison.json').write_text(json.dumps(comparison, indent=2))
```

This confirms transfer/numeric consistency, not independently signed hardware placement or target-video quality. capture.json retains the actual input/output hashes and caller-attested placement separately.
