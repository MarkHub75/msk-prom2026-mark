from pathlib import Path
p=Path('_WORK/W2_06_EVIDENCE/manual_manifest.py');s=p.read_text(encoding='utf8')
s=s.replace('total=65536','total=65536;session=requests.Session(); signed=None;signed_at=0')
s=s.replace('global total','global total,signed,signed_at')
s=s.replace("r=requests.get(base,headers={'Range':f'bytes={pos}-{min(4929210009,pos+4095)}'},timeout=20);r.raise_for_status();assert r.status_code==206", "r=session.get(signed if signed and time.monotonic()-signed_at<7 else base,headers={'Range':f'bytes={pos}-{min(4929210009,pos+4095)}'},timeout=20);r.raise_for_status();assert r.status_code==206\n if r.history:signed=r.url;signed_at=time.monotonic()")
s=s.replace('pos=8',"pos=8\nif (p/'mmodalfire_manifest.json').exists():\n old=json.loads((p/'mmodalfire_manifest.json').read_text());members=old['members'];blocks=old['blocks'];total=old['total_range_bytes'];last=blocks[-1];pos=last['offset']+last['header_size']+last['data_size'];print('RESUME',len(members),pos,flush=True)")
p.write_text(s,encoding='utf8')
