"""Read-only public Google Viewer retrieval used for EVRAZ 2024, 2026-10-23."""
import json
import pathlib
import re
import requests

folder = pathlib.Path(__file__).parent
source = 'https://www.evraz.ru/upload/iblock/a2c/9gimdu0ootuz5gm0b2pe962mvla00uia/EVRAZ_Sustainability_report_2024.pdf'
response = requests.get('https://docs.google.com/viewerng/viewer', params={'url': source}, timeout=30)
response.raise_for_status()
(folder / 'VIEWER.html').write_text(response.text, encoding='utf-8')
match = re.search(r'(/viewerng/upload[^"\s]+)', response.text)
if not match:
    raise RuntimeError('Viewer did not supply an upload metadata link')
metadata_path = json.loads('"' + match.group(1) + '"')
response = requests.get('https://docs.google.com' + metadata_path, timeout=30)
response.raise_for_status()
(folder / 'VIEWER_UPLOAD.txt').write_text(response.text, encoding='utf-8')
metadata = json.loads(response.text[4:])
response = requests.get(metadata['pdf'], timeout=30)
response.raise_for_status()
(folder / 'EVRAZ_VIEWER.pdf').write_bytes(response.content)
