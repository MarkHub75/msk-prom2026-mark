import requests,pathlib,json,datetime,hashlib
p=pathlib.Path('_WORK/W2_A_MATERIALS');p.mkdir(exist_ok=True)
u='https://www.dssl.ru/upload/medialibrary/724/tmh980ov7vkj0pid9s352ib3air808qu/DSSL_price-15.10.2026.xlsx'
r=requests.get(u,timeout=60); print(r.status_code,len(r.content));(p/'DSSL_price-15.10.2026.xlsx').write_bytes(r.content)
print(hashlib.sha256(r.content).hexdigest())
import openpyxl
w=openpyxl.load_workbook(p/'DSSL_price-15.10.2026.xlsx',read_only=True,data_only=True)
print(w.sheetnames)
for s in w:
 for row in s:
  vals=['%s=%s'%(c.column_letter,c.value) for c in row if c.value is not None]
  t=' | '.join(vals)
  if any(x in t.lower() for x in ['hardhat','wear detector','wear_detector','ндс','бессроч','обновлен','anyip','enterpriseip','рубл']): print(s.title,row[0].row,t[:2500])
