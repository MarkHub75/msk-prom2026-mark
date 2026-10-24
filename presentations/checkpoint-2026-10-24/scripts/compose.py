"""Deterministic image-slide composition; original assets remain untouched."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fontTools.ttLib import TTFont
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'slides'
OUT.mkdir(exist_ok=True)
(ROOT / 'preview').mkdir(exist_ok=True)
(ROOT / 'evidence').mkdir(exist_ok=True)
W, H = 1920, 1080
BG, SURFACE, LINE = '#0e1114', '#151a1f', '#35404a'
WHITE, MUTED, DIM = '#e6ebef', '#aab5bf', '#7f8d9a'
RED, AMBER = '#e5484d', '#e8a33d'
FONTS = {k: ROOT / 'assets/fonts' / v for k, v in {
    'regular': 'GolosText-Regular.ttf', 'semi': 'GolosText-Semibold.ttf',
    'bold': 'GolosText-Bold.ttf'}.items()}
inventory = []
current = None
CMAP = {key: TTFont(value).getBestCmap() for key, value in FONTS.items()}

def font(size, weight='regular'):
    return ImageFont.truetype(str(FONTS[weight]), size)

def txt(im, x, y, value, size=32, color=WHITE, weight='regular', maxw=None, leading=1.24, essential=True):
    draw = ImageDraw.Draw(im)
    face = font(size, weight)
    for n, line in enumerate(value.split('\n')):
        yy = y + n * round(size * leading)
        if not line:
            continue
        missing = sorted({char for char in line if ord(char) not in CMAP[weight]})
        if missing:
            raise ValueError(f'Slide {current}: unsupported glyphs {missing}: {line}')
        box = draw.textbbox((x, yy), line, font=face, anchor='lt')
        if maxw is not None and box[2] > x + maxw:
            raise ValueError(f'Slide {current}: text exceeds width: {line} ({box[2]-x}>{maxw})')
        if essential and not (96 <= box[0] and box[2] <= 1824 and 54 <= box[1] and box[3] <= 1026):
            raise ValueError(f'Slide {current}: unsafe text bounds {box}: {line}')
        draw.text((x, yy), line, font=face, fill=color, anchor='lt', stroke_width=0)
        inventory[-1]['text'].append({'text': line, 'size': size, 'weight': weight,
            'color': color, 'bounds': list(box), 'essential': essential})

def line(im, xy, color=LINE, width=2):
    ImageDraw.Draw(im).line(xy, fill=color, width=width)

def rect(im, box, fill=SURFACE, outline=None, width=1, radius=0):
    d = ImageDraw.Draw(im)
    if radius:
        d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    else:
        d.rectangle(box, fill=fill, outline=outline, width=width)

def arrow(im, start, end, color=MUTED, width=3):
    import math
    line(im, [start, end], color, width)
    a = math.atan2(end[1]-start[1], end[0]-start[0])
    p = [(end[0], end[1]),
         (end[0]-12*math.cos(a-0.5),end[1]-12*math.sin(a-0.5)),
         (end[0]-12*math.cos(a+0.5),end[1]-12*math.sin(a+0.5))]
    ImageDraw.Draw(im).polygon(p, fill=color)

def mark(im, x=104, y=66, scale=1):
    ImageDraw.Draw(im).polygon([(x+15*scale,y),(x+29*scale,y),(x+13*scale,y+38*scale),(x,y+38*scale)], fill=RED)

def start(n, section, art=None):
    global current
    current = n
    im = Image.new('RGB', (W,H), BG)
    if art:
        im.paste(ImageOps.fit(Image.open(ROOT / art).convert('RGB'), (W,H)),(0,0))
        shade = Image.new('RGBA',(W,H),(0,0,0,0))
        sd = ImageDraw.Draw(shade)
        for x in range(W):
            opacity = round(220 * min(1,max(0,(1800-x)/700))) if n==7 else 0
            if opacity:
                sd.line([(x,0),(x,H)],fill=(8,11,14,opacity))
        for y in range(930,H):
            sd.line([(0,y),(W,y)],fill=(8,11,14,220))
        im=Image.alpha_composite(im.convert('RGBA'),shade).convert('RGB')
    inventory.append({'slide': n, 'text': [], 'assets': []})
    if art:
        inventory[-1]['assets'].append({'path': art, 'role': 'generated illustration', 'rect':[0,0,W,H]})
    mark(im)
    txt(im,150,70,'SafeWatch',34,weight='bold')
    txt(im,104,996,'МОСПРОМ 2026  /  ТЕХНИЧЕСКИЙ ЧЕКПОЙНТ',22,MUTED)
    txt(im,1605,996,f'{section}  /  {n:02d}',22,MUTED,maxw=210)
    return im

def title(im, text, subtitle=None, size=76):
    txt(im,104,163,text,size,weight='semi',maxw=1712,leading=1.14)
    if subtitle:
        txt(im,104,270,subtitle,32,MUTED,maxw=1712)

def source(im,text):
    txt(im,104,956,text,22,DIM,maxw=1712)

def save(im,n):
    path=OUT/f'slide-{n:02d}.png'
    im.save(path, optimize=True)
    im.resize((1280,720),Image.Resampling.LANCZOS).save(ROOT/'preview'/f'slide-{n:02d}-720.png')
    inventory[-1]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()

def shot(im,name,box,crop=None):
    path=ROOT/'assets/screenshots'/name
    pic=Image.open(path).convert('RGB')
    original=list(pic.size)
    if crop:
        pic=pic.crop(crop)
    x,y,w,h=box
    # Explicit contain; no stretching, relettering, repainting or invented interface.
    pic=ImageOps.contain(pic,(w,h),Image.Resampling.LANCZOS)
    xx=x+(w-pic.width)//2; yy=y+(h-pic.height)//2
    im.paste(pic,(xx,yy))
    inventory[-1]['assets'].append({'path':str(path.relative_to(ROOT)), 'role':'actual frontend capture',
        'original':original,'crop':crop,'rect':[xx,yy,pic.width,pic.height],
        'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    rect(im,(xx-1,yy-1,xx+pic.width,yy+pic.height),fill=None,outline=LINE)

def node(im,box,heading,detail=None,accent=None,heading_size=33):
    x,y,w,h=box
    rect(im,(x,y,x+w,y+h),SURFACE,LINE)
    if accent:
        rect(im,(x,y,x+4,y+h),accent)
    txt(im,x+24,y+23,heading,heading_size,weight='semi',maxw=w-48)
    if detail:
        txt(im,x+24,y+72,detail,26,MUTED,maxw=w-48,leading=1.2)

# 01 — product thesis, roles and original industrial artwork.
im=start(1,'ПРОДУКТ','assets/generated/industrial-hero.png')
txt(im,104,183,'Промышленная\nбезопасность',100,weight='semi',maxw=1100,leading=1.08)
txt(im,108,443,'Внимание оператора —\nна опасном событии.',43,WHITE,maxw=1060,leading=1.23)
txt(im,108,572,'24 октября 2026  ·  11:00 МСК',28,MUTED)
layer=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(layer)
d.rectangle((80,694,1840,914), fill=(14,17,20,238))
im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
for x,head,detail in [(104,'Оператор','Получает и проверяет'),(695,'Мастер','Реагирует на поручение'),(1290,'Охрана труда','Анализирует журнал')]:
    txt(im,x,728,head,38,weight='semi')
    txt(im,x,791,detail,29,MUTED,maxw=500)
arrow(im,(579,766),(643,766));arrow(im,(1169,766),(1237,766))
txt(im,104,870,'ПЯТЬ РОЛЕЙ',21,DIM)
txt(im,316,868,'оператор  ·  мастер  ·  охрана труда  ·  руководство  ·  администратор',26,MUTED,maxw=1470)
source(im,'Концепция продукта: tech.md §2  ·  Индустриальное изображение — сгенерированная иллюстрация')
save(im,1)

# 02 — one causal architecture; snake reading order follows arrows.
im=start(2,'СИСТЕМА')
title(im,'Видео → событие → действие','Обработка архива и эмуляция эфира по серверным часам')
node(im,(104,351,250,130),'Видео','Загрузка файла')
node(im,(400,351,340,130),'LinQ Jupyter','Видео целиком')
node(im,(786,351,390,130),'TPU-инференс','Детектор + поза')
node(im,(1222,351,594,130),'Кэш детекций','JSONL · один анализ записи')
for a,b in [(354,400),(740,786),(1176,1222)]:arrow(im,(a+6,415),(b-6,415))
node(im,(1376,531,440,130),'CPU','Трекинг и правила')
node(im,(1020,531,310,130),'Эпизоды','Без дублей')
node(im,(461,531,513,130),'Эмуляция эфира','По серверным часам')
node(im,(104,531,311,130),'WebSocket','Публикация')
arrow(im,(1600,487),(1600,525))
for a,b in [(1376,1330),(1020,974),(461,415)]:arrow(im,(a-6,595),(b+6,595))
node(im,(104,711,465,112),'Оператор',None,RED)
node(im,(626,711,465,112),'Мастер')
node(im,(1148,711,668,112),'Журнал реакции')
arrow(im,(259,667),(259,705));arrow(im,(575,767),(620,767));arrow(im,(1097,767),(1142,767))
txt(im,104,865,'Одно продолжающееся нарушение — одно оповещение.',31,weight='semi',maxw=1712)
txt(im,104,910,'Подтверждение, передача и устранение — разные действия.',31,MUTED,maxw=1712)
source(im,'Contract-first: OpenAPI + WS-схема  ·  Заменяемый frontend  ·  Отдельный stateful-мок  ·  Схема целевого конвейера')
save(im,2)

# 03 — measured baseline results, with qualifications on the same slide.
im=start(3,'LINQ')
title(im,'LinQ: реальное исполнение на TPU','Baseline: YOLOv8n 640 и YOLOv8n-pose 640 скомпилированы и выполнены')
txt(im,104,346,'Тест детектора  ·  400 кадров  ·  1280 × 720',32,MUTED,maxw=1712)
txt(im,96,426,'≈21',190,weight='semi',maxw=730)
txt(im,108,641,'кадр/с',43,weight='semi')
txt(im,108,704,'Пропускная способность',29,MUTED)
line(im,[(835,431),(835,741)])
txt(im,902,444,'19',135,weight='semi');txt(im,1093,529,'с',49,MUTED)
txt(im,908,614,'Обработка',33,weight='semi');txt(im,908,664,'19,09 с по логу',26,MUTED)
txt(im,1372,444,'31',135,weight='semi');txt(im,1560,529,'с',49,MUTED)
txt(im,1377,614,'С загрузкой',33,weight='semi');txt(im,1377,664,'Полное время',26,MUTED)
rect(im,(104,784,1816,849),'#282118')
rect(im,(104,784,109,849),AMBER)
txt(im,130,802,'Интегрированный backend: стабильный ответ TPU пока не получен.',30,AMBER,maxw=1650)
txt(im,104,876,'21 кадр/с — обработка записи, а не время доставки тревоги оператору.',27,MUTED,maxw=1712)
txt(im,104,916,'Recall/IoU в отчёте — сохранность при квантовании относительно FP32,',25,MUTED,maxw=1712)
txt(im,104,949,'а не точность обнаружения нарушений на производстве.',25,MUTED,maxw=1712)
save(im,3)

# 04 — latest own-model proof supersedes old STATUS.md.
im=start(4,'МОДЕЛИ')
title(im,'Собственные модели дошли до TPU','Каска и Split-Pose: исполнение подтверждено; качество ещё проверяем')
node(im,(104,359,500,222),'01  ONNX','CPU/CUDA и ONNX\natol = rtol = 1e−3\nНа одном кадре',heading_size=37)
node(im,(662,359,500,222),'02  SDK LinQ','2026.9.45 · TPU_H1M\nОба графа скомпилированы\nSplit сохраняет confidence¹',heading_size=37)
node(im,(1220,359,596,222),'03  Реальный TPU','Helmet + Split-Pose\nСохранены ответы status 0\nс привязкой к запросам',accent=WHITE,heading_size=37)
arrow(im,(611,469),(655,469));arrow(im,(1169,469),(1213,469))
txt(im,104,622,'ИСПОЛНЕНО НА TPU',74,weight='semi',maxw=1712)
txt(im,108,726,'335 программных проверок · PASS по отчёту ветки',25,MUTED,maxw=1712)
line(im,[(104,790),(1816,790)])
txt(im,104,827,'Исполнение ещё не подтверждает качество',42,weight='semi',maxw=1712)
txt(im,104,893,'URfall-01: ответы TPU получены, но единственное падение пропущено.',30,AMBER,maxw=1712)
source(im,'¹ Исправление confidence проверено симуляцией SDK  ·  Свежие источники: ml/EVAL_REPORT.md и RELEASE_MANIFEST.json')
save(im,4)

# 05 — compact maturity matrix and current actual control room.
im=start(5,'ГОТОВНОСТЬ')
title(im,'Готовность по слоям','Статус по коду и проверкам после git fetch; сквозной продукт ещё собирается')
rows=[
    ('Backend и контракт','Работает¹','REST/WS, реакции; основа S0–S11',WHITE),
    ('Правила детекции','На синтетике','Бег, падение, сближение, телефон,\nограждение, опасная зона',MUTED),
    ('Frontend и действия','На моке','Оператор → мастер → журнал',AMBER),
    ('Демо-контур','30/30','Свежий smoke stateful-мока',WHITE)]
for k,(head,status,detail,color) in enumerate(rows):
    y=350+k*137
    txt(im,104,y,head,33,weight='semi',maxw=570)
    txt(im,667,y+4,status,26,color,maxw=195)
    txt(im,104,y+54,detail,26,MUTED,maxw=735,leading=1.2)
    line(im,[(104,y+118),(837,y+118)])
shot(im,'03-yellow-control-room.png',(891,350,925,521))
txt(im,891,883,'Текущий front/control-room · кадры синтетические',25,MUTED,maxw=925)
txt(im,891,920,'¹ LinQ-интеграция нестабильна.',25,AMBER,maxw=925)
source(im,'Огонь / СИЗ: нет моделей в main  ·  Перенос груза: правило ещё не завершено')
save(im,5)

# 06 — real captured steps, not generated UI.
im=start(6,'ДЕМО')
title(im,'Проверяем путь реакции','Живая демонстрация текущего frontend на stateful-моке')
txt(im,104,347,'01',31,AMBER,weight='semi');txt(im,164,343,'Бег',43,weight='semi')
txt(im,693,347,'02',31,RED,weight='semi');txt(im,753,343,'Падение',43,weight='semi')
txt(im,1446,347,'03',31,MUTED,weight='semi');txt(im,1506,343,'Мастер',43,weight='semi')
# Current queue: exact crop, no fabricated overlays.
shot(im,'03-yellow-control-room.png',(104,417,488,452),crop=(1575,176,1915,741))
shot(im,'07-red-incident.png',(647,417,729,279),crop=(268,212,1000,626))
shot(im,'07-red-incident.png',(647,719,729,150),crop=(1204,558,1917,729))
shot(im,'10-master-mobile-task.png',(1446,414,370,480))
txt(im,104,901,'Проверяет событие',29,MUTED,maxw=510)
txt(im,647,901,'Доказательство → передача',29,MUTED,maxw=740)
txt(im,1446,901,'Меры → журнал',29,MUTED,maxw=370)
txt(im,104,951,'Демонстрационные данные. Кадры синтетические. Рамки размечены вручную.',28,AMBER,maxw=1712)
save(im,6)

# 07 — six bounded priorities with generated industrial camera artwork.
im=start(7,'ДАЛЬШЕ','assets/generated/industrial-camera.png')
title(im,'До финальной защиты',None)
txt(im,104,278,'Приоритет — доказать весь конвейер и измерить качество.',34,MUTED,maxw=1630)
items=[
    ('01','Стабильный интегрированный прогон LinQ'),
    ('02','Интеграция своих моделей в общий конвейер'),
    ('03','Precision/Recall на размеченных видео'),
    ('04','Ложные тревоги на камеро-час'),
    ('05','Задержка от события до оповещения'),
    ('06','Оставшиеся сценарии и проверка качества')]
for i,(num,value) in enumerate(items):
    y=359+i*65
    txt(im,104,y+6,num,27,DIM)
    txt(im,176,y,value,33,weight='semi',maxw=1500)
txt(im,104,795,'Отличие: полный цикл тревоги до мастера, сводка смены,',28,weight='semi',maxw=1712)
txt(im,104,835,'видимое «нет наблюдения», происхождение каждого события.',28,weight='semi',maxw=1712)
txt(im,104,886,'Ближайший конкурент на LinQ — IVA CV',30,MUTED,maxw=1712)
source(im,'Без обещаний метрик до измерений  ·  Промышленная камера — сгенерированная иллюстрация')
save(im,7)

# 08 — questions aligned with current queue/measurement uncertainty.
im=start(8,'ЭКСПЕРТАМ')
title(im,'Вопросы экспертам LinQ','Нужны критерии доказательства и воспроизводимый способ измерения')
questions=[
    'Какое подтверждение работы на LinQ\nпримет жюри?',
    'Какие стадии конвейера\nобязательно выполнять на TPU?',
    'Как стабилизировать очередь\nпри ограниченном числе обработчиков?',
    'Как получить достоверное время\nвыполнения непосредственно на TPU?']
for i,q in enumerate(questions):
    y=364+i*139
    txt(im,104,y+5,f'0{i+1}',34,DIM,weight='semi')
    txt(im,208,y,q,39,weight='semi',maxw=1590,leading=1.15)
    if i<3:line(im,[(208,y+111),(1816,y+111)])
source(im,'Стабильность очереди остаётся открытой  ·  Время RPC и wall-clock не равно чистому времени исполнения TPU')
save(im,8)

(ROOT/'evidence/composition.json').write_text(json.dumps({'version':1,'canvas':[W,H],
    'font':'Golos Text (exact frontend source files, OFL)',
    'method':'Pillow deterministic typography and layout; original generated assets and UI captures untouched',
    'slides':inventory},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Static visual preview; final delivery is PPTX, this is not a presentation application.
thumb_w,thumb_h=960,540
sheet=Image.new('RGB',(1968,2256),BG)
d=ImageDraw.Draw(sheet)
for n in range(1,9):
    xx=16+((n-1)%2)*976; yy=16+((n-1)//2)*560
    pic=Image.open(OUT/f'slide-{n:02d}.png').resize((thumb_w,thumb_h),Image.Resampling.LANCZOS)
    sheet.paste(pic,(xx,yy))
sheet.save(ROOT/'preview/SafeWatch_8_slides.png',optimize=True)
print('Composed 8 slides at 1920×1080; safe text bounds checked; contact sheet and 720p previews saved.')
