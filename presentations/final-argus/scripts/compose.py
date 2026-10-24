from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
from fontTools.ttLib import TTFont
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
W,H=1920,1080
BG,SURFACE,LINE='#111214','#191b1f','#353941'
WHITE,MUTED,DIM='#f2f4f7','#a3abb7','#8893a2'
RED,AMBER='#ff5d65','#ffb65c'
F={k:ROOT/'assets/fonts'/f'SourceSans3-{v}.ttf' for k,v in [('regular','Regular'),('semi','Semibold'),('bold','Bold')]}
CMAP={k:TTFont(p).getBestCmap() for k,p in F.items()}
inventory=[]; slots=[];current=0
def txt(im,x,y,s,size=32,color=WHITE,weight='regular',maxw=1712):
    d=ImageDraw.Draw(im);f=ImageFont.truetype(str(F[weight]),size)
    for n,t in enumerate(s.split('\n')):
        if not t: continue
        assert all(ord(c) in CMAP[weight] for c in t),(current,t,'missing glyph')
        yy=y+n*round(size*1.18);b=d.textbbox((x,yy),t,font=f,anchor='lt')
        assert b[2]<=x+maxw,(current,t,'width',b)
        assert 96<=b[0] and b[2]<=1824 and 54<=b[1] and b[3]<=1026,(current,t,b)
        for prev in inventory[-1]['text']:
            a=prev['bounds'];assert min(b[2],a[2])<=max(b[0],a[0]) or min(b[3],a[3])<=max(b[1],a[1]),(current,t,prev['text'],'overlap')
        d.text((x,yy),t,font=f,fill=color,anchor='lt')
        inventory[-1]['text'].append(dict(text=t,size=size,weight=weight,bounds=list(b)))
def line(im,xy,color=LINE,width=2):ImageDraw.Draw(im).line(xy,fill=color,width=width)
def box(im,b,fill=SURFACE,outline=LINE):ImageDraw.Draw(im).rectangle(b,fill=fill,outline=outline,width=2)
def arrow(im,a,b,color=MUTED):
    import math
    line(im,[a,b],color,3);angle=math.atan2(b[1]-a[1],b[0]-a[0])
    ImageDraw.Draw(im).polygon([b,(b[0]-13*math.cos(angle-.5),b[1]-13*math.sin(angle-.5)),(b[0]-13*math.cos(angle+.5),b[1]-13*math.sin(angle+.5))],fill=color)
def start(n,category,art=False):
    global current
    current=n; im=Image.new('RGB',(W,H),BG);inventory.append(dict(slide=n,text=[],assets=[]))
    if art:
        p=ROOT/'assets/art/industrial-hero.png';im.paste(ImageOps.fit(Image.open(p).convert('RGB'),(W,H)),(0,0))
        shade=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(shade)
        for x in range(W):d.line([(x,0),(x,H)],fill=(9,11,14,round(180*max(0,1-x/1550))))
        d.rectangle((0,930,W,H),fill=(9,11,14,220));im=Image.alpha_composite(im.convert('RGBA'),shade).convert('RGB')
        inventory[-1]['assets'].append(dict(path=str(p.relative_to(ROOT)),kind='generated illustration, reused from prior approved-scope materials',sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    txt(im,104,68,category.upper(),27,MUTED,weight='semi')
    txt(im,104,998,'МАТЕРИАЛЫ К ФИНАЛЬНОЙ ЗАЩИТЕ',21,DIM)
    txt(im,1738,998,f'{n:02d} / 08',22,DIM,maxw=80)
    return im
def title(im,s,sub=None):
    txt(im,104,160,s,78,weight='semi')
    if sub:txt(im,104,265,sub,33,MUTED)
def frame(im,ident,label,b):
    x,y,w,h=b;p=ROOT/'assets/screens'/f'{ident}.png'
    box(im,(x,y,x+w,y+h),'#14171b',None)
    d=ImageDraw.Draw(im)
    for xx in range(x,x+w,30):
        d.line((xx,y,min(xx+14,x+w),y),fill=DIM,width=2);d.line((xx,y+h,min(xx+14,x+w),y+h),fill=DIM,width=2)
    for yy in range(y,y+h,30):
        d.line((x,yy,x,min(yy+14,y+h)),fill=DIM,width=2);d.line((x+w,yy,x+w,min(yy+14,y+h)),fill=DIM,width=2)
    state='placeholder'
    if p.exists():
        image=ImageOps.contain(Image.open(p).convert('RGB'),(w-4,h-4),Image.Resampling.LANCZOS)
        im.paste(image,(x+(w-image.width)//2,y+(h-image.height)//2));state='user-provided screenshot'
    else:
        size=30 if w<500 else 32
        f=ImageFont.truetype(str(F['regular']),size);length=d.textlength(label,font=f)
        txt(im,x+(w-length)/2,y+h/2-18,label,size,MUTED,maxw=w-24)
    slots.append(dict(id=ident,slide=current,label=label,rect=list(b),file=f'assets/screens/{ident}.png',state=state))
def node(im,x,y,w,head,body):
    box(im,(x,y,x+w,y+128));txt(im,x+23,y+22,head,35,weight='semi',maxw=w-46);txt(im,x+23,y+76,body,27,MUTED,maxw=w-46)
def save(im):
    p=ROOT/f'slides/slide-{current:02}.png';im.save(p,optimize=True)
    im.resize((1280,720),Image.Resampling.LANCZOS).save(ROOT/f'preview/slide-{current:02}-720.png')
    inventory[-1]['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()

im=start(1,'Проблема',True)
txt(im,104,174,'АРГУС',104,weight='bold')
txt(im,104,353,'Опасное событие\nдолжно стать действием.',86,weight='semi',maxw=1500)
txt(im,108,600,'Поток с камер непрерывен.\nВнимание оператора ограничено.',40,MUTED,maxw=1270)
line(im,[(108,787),(1040,787)],MUTED)
txt(im,108,832,'Нужен понятный путь: сигнал, решение,\nответственный, подтверждённые меры.',35,maxw=1300)
txt(im,104,956,'Индустриальное изображение — иллюстрация.',22,DIM)
save(im)

im=start(2,'Пользователи и роли')
title(im,'У события есть ответственный','Оператор проверяет. Мастер действует. Охрана труда анализирует.')
for y,head,body in [(363,'Оператор','Проверяет событие и выбирает действие'),(552,'Мастер смены','Принимает поручение и сообщает о мерах'),(741,'Охрана труда','Смотрит журнал, причины и реакцию')]:
    line(im,[(104,y-20),(966,y-20)]);txt(im,104,y,head,45,weight='semi',maxw=860);txt(im,104,y+70,body,31,MUTED,maxw=860)
frame(im,'roles','скрин: роли и навигация',(1070,342,746,484))
txt(im,1070,871,'Дополнительные роли:',30,MUTED,maxw=746)
txt(im,1070,916,'руководство · администратор',33,weight='semi',maxw=746)
save(im)

im=start(3,'Путь события')
title(im,'От сигнала до принятых мер','Жёлтое → красное → мастер → журнал')
steps=[('yellow','Жёлтое','скрин: жёлтая тревога','Проверить сигнал',AMBER),('red','Красное','скрин: красная тревога','Открыть доказательство',RED),('master','Мастер','скрин: поручение мастеру','Принять и указать меры',WHITE),('journal','Журнал','скрин: журнал события','Сохранить историю',WHITE)]
for i,(ident,head,label,action,color) in enumerate(steps):
    x=104+i*443
    txt(im,x,349,head,43,color,weight='semi',maxw=380)
    frame(im,ident,label,(x,423,383,327))
    txt(im,x,795,action,29,MUTED,maxw=390)
    if i<3:arrow(im,(x+393,586),(x+432,586))
txt(im,104,905,'Подтверждение, передача и устранение фиксируются раздельно.',33,weight='semi')
save(im)

im=start(4,'Аналитика')
title(im,'Журнал становится картиной смены','От отдельных событий — к разбору причин и реакции')
frame(im,'analytics','скрин: аналитика',(104,345,1134,548))
for y,head,body in [(360,'Где?','Секторы, камеры,\nсценарии'),(548,'Когда?','Период, смены,\nдинамика'),(736,'Как реагируют?','Вердикты,\nвремя реакции')]:
    txt(im,1320,y,head,42,weight='semi',maxw=496);txt(im,1320,y+64,body,32,MUTED,maxw=496)
txt(im,104,936,'Демо-значения на будущих снимках не являются производственными метриками.',28,MUTED)
save(im)

im=start(5,'LinQ — факты и оговорки')
title(im,'Baseline исполнялся на TPU','YOLOv8n 640 и YOLOv8n-pose 640: компиляция и исполнение подтверждены')
txt(im,104,343,'Тест детектора · 400 кадров · 1280 × 720',32,MUTED)
txt(im,104,422,'≈21',180,weight='semi',maxw=700);txt(im,111,619,'кадр/с обработки записи',37,weight='semi')
line(im,[(817,421),(817,680)])
txt(im,889,442,'19,09 с',105,weight='semi',maxw=460);txt(im,895,583,'Обработка',33,MUTED,maxw=400)
txt(im,1425,442,'31 с',105,weight='semi',maxw=390);txt(im,1431,583,'С загрузкой',33,MUTED,maxw=380)
txt(im,104,724,'Свои модели: есть отчёты исполнения на TPU; интеграция — отдельная задача.',30,MUTED)
box(im,(104,802,1816,863),'#2b2010',None)
txt(im,126,822,'Стабильный сквозной прогон backend на LinQ ещё не подтверждён.',31,AMBER,maxw=1660)
txt(im,104,900,'21 кадр/с — не задержка тревоги. Recall/IoU — сравнение с FP32 при квантовании,',27,MUTED)
txt(im,104,939,'а не точность обнаружения нарушений на производстве.',27,MUTED)
save(im)

im=start(6,'Архитектура')
title(im,'Один конвейер. Разные рабочие места.','Архив и эмуляция потока; нейросети и правила разделены')
for x,w,head,body in [(104,280,'Видео','Загрузка записи'),(433,425,'LinQ Jupyter','TPU: детектор и поза'),(907,425,'JSONL-кэш','Сохранённые детекции'),(1381,435,'CPU','Трекинг и правила')]:node(im,x,356,w,head,body)
for x1,x2 in [(384,433),(858,907),(1332,1381)]:arrow(im,(x1+5,420),(x2-5,420))
node(im,1381,542,435,'Эпизоды','Продолжающийся риск')
node(im,760,542,572,'Эмуляция эфира','Публикация по серверным часам')
node(im,104,542,607,'WebSocket','Доставка событий и обновлений')
arrow(im,(1599,490),(1599,536));arrow(im,(1375,606),(1338,606));arrow(im,(754,606),(717,606))
node(im,104,729,607,'Рабочие места','Оператор · мастер · охрана труда')
node(im,760,729,1056,'Журнал и аналитика','История действий, происхождение, период и разрезы')
arrow(im,(407,676),(407,723));arrow(im,(717,793),(754,793))
txt(im,104,910,'OpenAPI + WS-схема · заменяемый frontend · отдельный stateful-мок',32,MUTED)
save(im)

im=start(7,'Что честно не готово')
title(im,'Граница готовности видна','Исполнение модели, качество и промышленная эксплуатация — разные проверки')
gaps=[('Сквозной LinQ','Нужны стабильная очередь\nи воспроизводимый прогон'),('Качество CV','Нужна независимая проверка\nна целевых видео'),('Эксплуатационные метрики','Задержка и ложные тревоги\nещё требуют измерений')]
for i,(head,body) in enumerate(gaps):
    y=360+i*176;txt(im,104,y,head,42,weight='semi',maxw=880);txt(im,104,y+63,body,31,MUTED,maxw=880)
frame(im,'provenance','скрин: происхождение события',(1070,345,746,470))
txt(im,1070,857,'Режим, источник и история\nдействий видны оператору.',31,MUTED,maxw=746)
txt(im,104,940,'Промышленный пилот и независимая приёмка качества ещё не подтверждены.',28,MUTED)
save(im)

im=start(8,'План')
title(im,'Следующий шаг — проверяемый результат','Сначала собрать контур, затем измерить качество и проверить рабочий процесс')
plans=[('01','Собрать контур','Свои модели в общем backend\nСтабильный прогон LinQ'),('02','Проверить качество','Размеченные целевые видео\nЛожные тревоги и задержка'),('03','Провести пилот','Оператор и мастер на участке\nПриёмка полного цикла реакции')]
for i,(number,head,body) in enumerate(plans):
    x=104+i*590;txt(im,x,381,number,45,DIM,weight='semi',maxw=530);line(im,[(x,454),(x+530,454)])
    txt(im,x,492,head,44,weight='semi',maxw=530);txt(im,x,574,body,31,MUTED,maxw=530)
txt(im,104,786,'Цель — проверить полный цикл:\nот события до подтверждённых мер.',57,weight='semi')
txt(im,104,949,'Сроки и целевые значения — после измерений и согласования.',27,MUTED)
save(im)

assert sum(t['text'].count('АРГУС') for s in inventory for t in s['text'])==1
assert not any('SafeWatch' in t['text'] for s in inventory for t in s['text'])
(ROOT/'evidence/composition.json').write_text(json.dumps(dict(canvas=[W,H],brand_occurrences=1,ui_images_in_skeleton=0,slides=inventory),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'screenshot-slots.json').write_text(json.dumps(slots,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sheet=Image.new('RGB',(1968,2256),BG)
for n in range(1,9):sheet.paste(Image.open(ROOT/f'slides/slide-{n:02}.png').resize((960,540),Image.Resampling.LANCZOS),(16+((n-1)%2)*976,16+((n-1)//2)*560))
sheet.save(ROOT/'preview/8-slides.png',optimize=True)
print('8 slides composed. Brand appears once. UI slots are explicit placeholders; glyphs/bounds/overlaps checked.')
