"""Lossless eight-page static review PDF and pixel-level round-trip check."""
from pathlib import Path
import json,hashlib
import fitz
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'exports/ARGUS_Final_Skeleton.pdf'
doc=fitz.open()
for n in range(1,9):
    page=doc.new_page(width=960,height=540)
    page.insert_image(page.rect,filename=str(ROOT/f'slides/slide-{n:02}.png'))
doc.set_metadata({'title':'Каркас финальной презентации','author':'Команда продукта','subject':'Eight exact image slides; see PPTX for speaker notes'})
doc.save(out,deflate=True)
doc.close()
checks=[]
with fitz.open(out) as check:
    assert check.page_count==8
    for n,page in enumerate(check,1):
        pix=page.get_pixmap(matrix=fitz.Matrix(2,2),alpha=False)
        rendered=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        source=Image.open(ROOT/f'slides/slide-{n:02}.png').convert('RGB')
        assert rendered.size==source.size==(1920,1080)
        assert ImageChops.difference(source,rendered).getbbox() is None
        checks.append({'slide':n,'rasterPixelIdentical':True})
report={'status':'PASS','pages':8,'checks':checks,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(ROOT/'evidence/pdf-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS:lossless8-page PDF; all1920×1080 rendered pixels identical.')
