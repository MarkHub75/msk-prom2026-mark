import datetime, hashlib, json, pathlib, urllib.request
ROOT = pathlib.Path(__file__).parent
manifest = []
def fetch(url, name):
    rec = {'url': url, 'access_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'W2-I research'}), timeout=20) as r:
            b=r.read(); rec.update(status=r.status, content_type=r.headers.get('Content-Type'), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
        (ROOT/name).write_bytes(b)
        rec['saved']=name
        manifest.append(rec)
        return b
    except Exception as e:
        rec['error']=repr(e); manifest.append(rec)
        return None
b=fetch('https://api.github.com/repos/mlcommons/inference_policies/commits/master','MLCOMMONS_COMMIT.json')
if b:
    sha=json.loads(b)['sha']
    fetch(f'https://raw.githubusercontent.com/mlcommons/inference_policies/{sha}/inference_rules.adoc','MLCOMMONS_RULES.adoc')
fetch('https://api.github.com/repos/sherstpasha/linq-cv-bench/git/trees/3ad1b7aa92a6b2fe057e60c36c6e03039ccaa140?recursive=1','REPO_TREE.json')
fetch('https://api.github.com/repos/sherstpasha/linq-cv-bench/releases','REPO_RELEASES.json')
fetch('https://api.github.com/repos/sherstpasha/linq-cv-bench/branches','REPO_BRANCHES.json')
fetch('https://elib.spbstu.ru/dl/3/2026/vr/vr26-931.pdf/en/info','THESIS_INFO.html')
(ROOT/'PRIMARY_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
