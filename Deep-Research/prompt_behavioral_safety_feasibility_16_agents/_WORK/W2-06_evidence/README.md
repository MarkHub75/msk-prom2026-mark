# W2-06 evidence, 2026-10-23
Only static research. No model inference, torch.load, pickle.load, export, compiler, device calls, or application. Existing PyAV/PIL decoded media; own scripts downloaded bounded source/media and statically disassembled ZIP pickle instructions.

- downloads.json: full FURG MP4/XML and HF PT/card URLs, bytes, SHA256.
- decode_manifest.json + *_pts.csv + all-frame sheets + *_detail.jpg: full FURG decode, original XML overlays; original GT retained, known errors are described in ../W2-06.md.
- checkpoint_static.json + metadata_locators.json + *_dis.txt: safe static PT inspection; GLOBAL/REDUCE printed, not executed.
- sources.json + versioned source files: primary source dependencies, AGPL license, export/head/letterbox references.
- firesense_range.json/members.json/acquired.json + firesense_record.json: primary ZIP Range extraction, member CRC/hash/decode and CC BY4 metadata. Whole ZIP not acquired or hashed.
- r3e6_tree.json: full pinned tree; no license/copying/notice paths found. Reference only.
- artifact_hashes.json: current local non-image evidence hashes; not a publisher signature.

Video/model/license grants remain artifact/action specific; do not automatically publish this folder. See ../W2-06.md for review observations, rights scope, scenario contract, and open gates.
