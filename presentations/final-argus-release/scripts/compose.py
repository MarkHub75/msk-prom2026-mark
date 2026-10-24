"""Art-directed image-slide composition. All UI bytes originate in the user archive.
No AI redraw of UI, demo metric fabrication or inferred factory measurements.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
from fontTools.ttLib import TTFont
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];W,H=1920,1080;N=15
BG='#161616';PANEL='#202226';RAISED='#26292f';LINE='#41454d';WHITE='#f3f5f7';MUTED='#bcc4cf';DIM='#949eac'
RED='#ff5d65';AMBER='#ffb65c';CYAN='#55d6f5';VIOLET='#a38bff';GREEN='#64d8b0'
BLUE='#8ba9cc'
BRAND='АРГУС';TAG='под надзором'
F={k:ROOT/'assets/fonts'/f'SourceSans3-{v}.ttf' for k,v in [('regular','Regular'),('semi','Semibold'),('bold','Bold')]}
CMAP={k:TTFont(p).getBestCmap() for k,p in F.items()};inv=[];current=0
def font(size,weight='regular'):return ImageFont.truetype(str(F[weight]),size)
def txt(im,x,y,s,size=34,color=WHITE,weight='regular',maxw=1744,leading=1.12):
    d=ImageDraw.Draw(im);f=font(size,weight)
    for i,t in enumerate(s.split('\n')):
        if not t:continue
        assert all(ord(c) in CMAP[weight] for c in t),(current,'glyph',t)
        yy=y+i*round(size*leading);b=d.textbbox((x,yy),t,font=f,anchor='lt')
        assert b[2]<=x+maxw+1,(current,'width',t,b,maxw)
        assert b[0]>=70 and b[2]<=1850 and b[1]>=44 and b[3]<=1058,(current,'safe bounds',t,b)
        for p in inv[-1]['text']:
            a=p['bounds'];assert min(b[2],a[2])<=max(b[0],a[0]) or min(b[3],a[3])<=max(b[1],a[1]),(current,'text overlap',t,p['text'])
        d.text((x,yy),t,font=f,anchor='lt',fill=color);inv[-1]['text'].append(dict(text=t,size=size,bounds=list(b),weight=weight))
def line(im,points,color=LINE,width=2):ImageDraw.Draw(im).line(points,fill=color,width=width)
def rect(im,b,fill=PANEL,outline=None,r=0,width=2):
    d=ImageDraw.Draw(im)
    if r:d.rounded_rectangle(b,radius=r,fill=fill,outline=outline,width=width)
    else:d.rectangle(b,fill=fill,outline=outline,width=width)
def arrow(im,a,b,color=CYAN,width=3):
    line(im,[a,b],color,width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);d=ImageDraw.Draw(im)
    d.polygon([b,(b[0]-14*math.cos(ang-.5),b[1]-14*math.sin(ang-.5)),(b[0]-14*math.cos(ang+.5),b[1]-14*math.sin(ang+.5))],fill=color)
def shadow(im,b,r=22,alpha=170):
    layer=Image.new('RGBA',(W,H));ImageDraw.Draw(layer).rounded_rectangle(b,radius=r,fill=(0,0,0,alpha));layer=layer.filter(ImageFilter.GaussianBlur(22));im.paste(layer,(0,0),layer)
def asset(im,name,b,kind='screen',crop=None,contain=False,r=0,alpha=255):
    p=ROOT/'assets'/('screens' if kind=='screen' else 'stills')/name;source=Image.open(p).convert('RGB')
    if crop:source=source.crop(crop)
    x,y,w,h=map(round,b)
    if contain:
        source=ImageOps.contain(source,(w,h),Image.Resampling.LANCZOS);x+=(w-source.width)//2;y+=(h-source.height)//2
    else:source=ImageOps.fit(source,(w,h),Image.Resampling.LANCZOS)
    mask=Image.new('L',source.size,alpha)
    if r:ImageDraw.Draw(mask).rounded_rectangle((0,0,source.width,source.height),radius=r,fill=alpha)
    im.paste(source,(x,y),mask)
    inv[-1]['assets'].append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rect=[x,y,source.width,source.height],crop=crop,kind='actual supplied UI screenshot' if kind=='screen' else 'supplied synthetic factory still'))
    return (x,y,source.width,source.height)
def shade(im,left=215,right=20,bottom=0):
    mask=Image.new('RGBA',(W,H));d=ImageDraw.Draw(mask)
    for x in range(W):d.line((x,0,x,H),fill=(10,12,15,round(left+(right-left)*x/W)))
    if bottom:d.rectangle((0,870,W,H),fill=(13,15,18,bottom))
    im.paste(mask,(0,0),mask)
def start(n,category,photo=None,demo=False):
    global current
    current=n;inv.append(dict(slide=n,text=[],assets=[]));im=Image.new('RGB',(W,H),BG)
    if photo:asset(im,photo,(0,0,W,H),kind='still');shade(im)
    else:
        d=ImageDraw.Draw(im)
        for x in range(88,W,160):d.line((x,98,x,976),fill='#1b1d20')
        for y in range(98,978,160):d.line((88,y,1832,y),fill='#1b1d20')
    txt(im,88,53,category.upper(),25,MUTED,weight='semi')
    footer='Демо-интерфейс · синтетические кадры и события' if demo else 'МОСПРОМ 2026 · ФИНАЛЬНАЯ ЗАЩИТА'
    txt(im,88,1022,footer,23,DIM,maxw=1600)
    txt(im,1748,1020,f'{n:02} / {N}',24,DIM,maxw=90)
    return im
def heading(im,title,sub=None,size=76):
    txt(im,88,125,title,size,weight='semi')
    if sub:txt(im,92,230,sub,33,MUTED)
def monitor(im,name,x,y,w,accent=LINE):
    h=round(w*9/16);shadow(im,(x-18,y-18,x+w+22,y+h+42));rect(im,(x-13,y-13,x+w+13,y+h+17),'#090b0d',accent,r=18)
    asset(im,name,(x,y,w,h),contain=True)
    rect(im,(x+w*.44,y+h+18,x+w*.56,y+h+41),'#34373d')
    rect(im,(x+w*.32,y+h+40,x+w*.68,y+h+47),'#535862',r=3)
    return (x,y,w,h)
def laptop(im,name,x,y,w,accent=LINE):
    h=round(w*9/16);shadow(im,(x-20,y-18,x+w+22,y+h+48));rect(im,(x-13,y-13,x+w+13,y+h+13),'#0a0c0f',accent,r=18)
    asset(im,name,(x,y,w,h),contain=True)
    d=ImageDraw.Draw(im);d.polygon([(x-36,y+h+15),(x+w+36,y+h+15),(x+w+14,y+h+37),(x-14,y+h+37)],fill='#454b55');line(im,[(x-36,y+h+16),(x+w+36,y+h+16)],'#9da4ad',2)
    rect(im,(x+w*.4,y+h+15,x+w*.6,y+h+20),'#1c2027',r=2)
    return (x,y,w,h)
def phone(im,name,x,y,w,accent=LINE):
    src=Image.open(ROOT/'assets/screens'/name);h=round(w*src.height/src.width)
    shadow(im,(x-10,y-10,x+w+25,y+h+22),r=28);rect(im,(x-10,y-10,x+w+10,y+h+10),'#090b0d',accent,r=26)
    asset(im,name,(x,y,w,h),contain=True);return(x,y,w,h)
def badge(im,x,y,label,color=CYAN,size=25):
    w=round(ImageDraw.Draw(im).textlength(label,font=font(size,'semi')))+34
    rect(im,(x,y,x+w,y+size+24),PANEL,color,r=5);txt(im,x+17,y+12,label,size,color,weight='semi',maxw=w-30);return w
def highlight(im,screen,srcbox,color=CYAN):
    x,y,w,h=screen;x1,y1,x2,y2=srcbox
    b=(x+x1*w/1920,y+y1*h/1080,x+x2*w/1920,y+y2*h/1080)
    rect(im,b,None,color,r=3,width=3);return b
def lockup(im,x,y,size=190):
    txt(im,x+5,y,TAG,34,MUTED,maxw=700)
    txt(im,x,y+56,BRAND,size,weight='bold',maxw=1100)
def save(im):
    # Repaint the small navigation labels after photographic grading.
    d=ImageDraw.Draw(im)
    for n,t in enumerate(inv[-1]['text'][:3]):
        d.text((t['bounds'][0],t['bounds'][1]),t['text'],font=font(t['size'],t['weight']),fill=MUTED if n==0 else DIM,anchor='lt')
    p=ROOT/f'slides/slide-{current:02}.png';im.save(p,optimize=True)
    im.resize((1280,720),Image.Resampling.LANCZOS).save(ROOT/f'preview/slide-{current:02}-720.png')
    inv[-1]['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()

# 01 — a brand-led film still, with manually placed event evidence.
im=start(1,'Промышленная безопасность','fall.png');shade(im,left=140,right=0,bottom=0)
lockup(im,88,157,188)
txt(im,96,489,'Видеоконтроль промышленной безопасности',40,maxw=1000)
txt(im,96,552,'Нейросети на ускорителях LinQ',40,CYAN,maxw=1000)
b=(round(.482*W),round(.535*H),round(.641*W),round(.689*H));rect(im,b,None,RED,width=4)
rect(im,(b[0],b[3]+16,b[0]+520,b[3]+76),'#331c20',RED,r=3)
txt(im,b[0]+18,b[3]+33,'Падение и неподвижность',30,RED,weight='semi',maxw=490)
txt(im,96,919,'Увидеть опасность. Довести реакцию до результата.',35,weight='semi')
txt(im,96,972,'Синтетический кадр · рамка размечена вручную',25,MUTED)
save(im)

# 02 — the director's problem, illustrated by simultaneous camera views.
im=start(2,'Проблема',photo='press.png');shade(im,left=160,right=30)
txt(im,88,143,'Камеры есть.\nРеакция не гарантирована.',83,weight='semi',maxw=1500)
for n,name in enumerate(['press.png','forklift.png','conveyor.png','welding.png','gate.png','toolshop.png']):
    x=1070+(n%2)*385;y=375+(n//2)*186;asset(im,name,(x,y,360,165),kind='still');rect(im,(x,y,x+360,y+165),None,LINE)
for y,number,head,body in [(415,'01','Внимание ограничено','Оператор не видит десятки экранов сразу.'),(599,'02','У тревоги нет хозяина','Без поручения сигнал остаётся на мониторе.'),(783,'03','Урок не закреплён','Без разбора причин нарушение повторяется.')]:
    txt(im,88,y,number,38,AMBER,weight='semi',maxw=80);txt(im,177,y,head,44,weight='semi',maxw=830);txt(im,177,y+62,body,31,MUTED,maxw=830)
txt(im,1070,963,'Иллюстративные, синтетические кадры',25,MUTED,maxw=750)
save(im)

# 03 — the promise is a human workflow, with the real product as visual proof.
im=start(3,'Решение',demo=True)
txt(im,88,130,'От опасности —\nк подтверждённым мерам.',76,weight='semi',maxw=1100)
s=monitor(im,'01-dispatcher-calm.png',690,330,1110,CYAN)
phone(im,'06-master-event-measures.png',460,425,222,RED)
for y,head,body,c in [(433,'Видим опасность','Событие и доказательство',AMBER),(616,'Поднимаем человека','Оператор → мастер',RED),(799,'Фиксируем реакцию','Меры остаются в журнале',CYAN)]:
    line(im,[(88,y-17),(315,y-17)],c,3);txt(im,88,y,head,35,c,weight='semi',maxw=545);txt(im,88,y+57,body,29,MUTED,maxw=545)
badge(im,1270,283,'Диспетчерская',CYAN)
save(im)

# 04 — a screen for each responsibility; large role labels carry the meaning.
im=start(4,'Пять ролей',demo=True)
heading(im,'Каждому — свой экран. И своя задача.')
roles=[('Оператор','Проверить и передать','02-dispatcher-yellow.png',AMBER),('Мастер','Принять и указать меры','06-master-event-measures.png',RED),('Охрана труда','Разобрать причины','10-ohs-analytics.png',CYAN),('Руководство','Видеть общую картину','11-management.png',VIOLET),('Администратор','Настроить камеры\nи правила','14-admin-zones.png',MUTED)]
for n,(role,task,name,c) in enumerate(roles):
    x=88+n*354;txt(im,x,302,role,35,c,weight='semi',maxw=340)
    if n==1:phone(im,name,x+61,400,201,c)
    else:
        monitor(im,name,x,448,321,c)
        # Relevant real fragment below, with the full screen retained above.
        crop=(90,88,1500,570) if n in [2,3] else (88,118,1500,790)
        asset(im,name,(x,712,321,143),crop=crop);rect(im,(x,712,x+321,855),None,LINE)
    txt(im,x,913,task,28,MUTED,maxw=340)
save(im)

# 05 — a cinematic storyboard, using the requested original screenshot sequence.
im=start(5,'Путь события',demo=True)
heading(im,'Тревога заканчивается действием.')
for x,head,c in [(88,'Проверить',AMBER),(548,'Среагировать',RED),(1015,'Принять меры',WHITE),(1455,'Сохранить',CYAN)]:txt(im,x,294,head,35,c,weight='semi',maxw=390)
monitor(im,'02-dispatcher-yellow.png',88,382,410,AMBER)
monitor(im,'03-takeover-red.png',548,382,410,RED)
phone(im,'05-master-inbox.png',1036,368,171,RED)
phone(im,'06-master-event-measures.png',1231,368,171,RED)
monitor(im,'08-journal-preview.png',1455,382,370,CYAN)
for a,b,c in [((507,498),(535,498),AMBER),((969,498),(1018,498),RED),((1415,498),(1443,498),CYAN)]:arrow(im,a,b,c)
for x,body,w in [(88,'Жёлтый сигнал:\nоператор проверяет',410),(548,'Красная тревога:\nзахват внимания и кадр',410),(1020,'Поручение на телефоне:\nмастер фиксирует меры',400),(1455,'История события:\nрешение и результат',370)]:txt(im,x,803,body,31,MUTED,maxw=w)
txt(im,88,943,'Подтверждение, передача и устранение — разные действия.',35,weight='semi')
save(im)

# 06 — large chart-led screen, with small documentary evidence flanking it.
im=start(6,'Охрана труда и руководство',demo=True)
heading(im,'Больше событий ≠ больше опасности.')
s=monitor(im,'10-ohs-analytics.png',88,320,1120,CYAN)
highlight(im,s,(1468,634,1895,692),CYAN)
badge(im,88,243,'Демо-данные',AMBER,size=25)
txt(im,1320,303,'Охват камер\nДоля подтверждённых',34,CYAN,weight='semi',maxw=505)
asset(im,'11-management.png',(1320,405,505,284),contain=True);rect(im,(1320,405,1825,689),None,VIOLET)
txt(im,1320,712,'Руководству — контекст',30,MUTED,maxw=505)
txt(im,1320,775,'Журнал → PDF',32,weight='semi',maxw=505)
asset(im,'09-report.png',(1320,825,505,171),crop=(415,50,1590,449));rect(im,(1320,825,1825,996),None,LINE)
save(im)

# 07 — geometry is visible on the actual camera image, not a text checklist.
im=start(7,'Настройка без программиста',demo=True)
heading(im,'Настроить участок — прямо на кадре.')
txt(im,91,235,'Зоны и условия привязаны к конкретной камере.',31,MUTED,maxw=1250)
s=laptop(im,'14-admin-zones.png',88,319,1150,CYAN)
highlight(im,s,(330,156,1535,967),CYAN)
for y,name,head,body,c in [(317,'15-admin-calibration.png','Калибровка','Масштаб и геометрия',CYAN),(681,'12-rules-matrix.png','Правила','Зоны, условия, чувствительность',AMBER)]:
    asset(im,name,(1365,y,460,259),contain=True);rect(im,(1365,y,1825,y+259),None,c)
    txt(im,1365,y+275,head,34,c,weight='semi',maxw=460)
save(im)

# 08 — the proof slide: one flow, one large measured result, scoped caveats.
im=start(8,'Архитектура',photo='welding.png');shade(im,left=185,right=165)
heading(im,'Нейросеть видит. Правило решает.')
nodes=[(88,255,'Камера','Видео участка'),(389,370,'Нейросети','LinQ TPU или CPU'),(805,370,'Трекинг и правила','Движение и контекст'),(1221,255,'Эпизоды','Риск во времени'),(1522,303,'Роли','Оператор → мастер')]
for x,w,head,body in nodes:
    rect(im,(x,290,x+w,435),'#1b2026',LINE,r=8);txt(im,x+20,316,head,34,weight='semi',maxw=w-36);txt(im,x+20,376,body,26,MUTED,maxw=w-36)
for x1,x2 in [(343,389),(759,805),(1175,1221),(1476,1522)]:arrow(im,(x1+7,362),(x2-8,362),CYAN)
txt(im,88,502,'21',188,CYAN,weight='semi',maxw=440)
txt(im,94,708,'кадр/с на LinQ TPU',36,weight='semi',maxw=650)
txt(im,94,769,'YOLOv8n · тест записи 1280×720',30,MUTED,maxw=660)
line(im,[(760,506),(760,884)])
txt(im,828,510,'0,91 / 0,93',70,weight='semi',maxw=950)
txt(im,832,606,'Recall / IoU к FP32 после квантования',31,MUTED,maxw=980)
txt(im,832,681,'8 сценариев — правила-прототипы',37,VIOLET,weight='semi',maxw=990)
txt(im,832,755,'Каска и поза: скомпилированы и исполнены на TPU.',30,weight='semi',maxw=990)
txt(im,832,809,'Качество проверяем; общая интеграция ещё открыта.',29,MUTED,maxw=990)
txt(im,88,914,'21 кадр/с — обработка записи, не задержка оповещения. Поза также исполнена на TPU.',27,MUTED)
txt(im,88,956,'Recall/IoU здесь — сохранность к FP32, не точность на заводе. Фон — синтетическая иллюстрация.',26,MUTED)
save(im)

# 09 — progressively narrower work, using only the operating settings supplied by the user.
im=start(9,'Ресурсы · событийная обработка')
heading(im,'Как Argus экономит вычисления',size=72)
txt(im,92,230,'Частота по событию · каскад моделей · трекинг на CPU',32,MUTED)
steps=[
    (88,300,980,112,'01','Все камеры, 5 проверок/с','Детектор движения на CPU, <1 мс на кадр'),
    (118,438,920,112,'02','Есть движение → LinQ','Детектор людей до 10 кадров/с'),
    (148,576,860,112,'03','Есть человек → каскад','Поза и СИЗ только на вырезке человека'),
    (178,714,800,112,'04','Между кадрами детектора','Трекер на CPU'),
]
for x,y,w,h,num,head,body in steps:
    rect(im,(x,y,x+w,y+h),PANEL,LINE,r=8)
    line(im,[(x,y+10),(x,y+h-10)],BLUE,4)
    txt(im,x+21,y+22,num,26,BLUE,weight='semi',maxw=50)
    txt(im,x+82,y+18,head,35,weight='semi',maxw=w-102)
    txt(im,x+82,y+68,body,29,MUTED,maxw=w-102)
    if num!='04':arrow(im,(578,y+h+5),(578,y+h+22),BLUE,2)
line(im,[(1110,300),(1110,902)],LINE)
for y,num,body in [
    (313,'01','Пустые кадры\nдо нейросети не доходят'),
    (493,'02','Полная частота и все модели —\nтолько в момент события'),
    (673,'03','Ускорители считаются по пиковой\nодновременной активности,\nа не по числу камер'),
]:
    txt(im,1150,y,num,26,BLUE,weight='semi',maxw=55)
    txt(im,1213,y,body,39,weight='semi',maxw=625,leading=1.18)
txt(im,88,851,'Пусто → контрольный кадр раз в 3–5 с.',29,BLUE,maxw=1000)
txt(im,88,896,'Вне смены — дежурный режим: только движение, тревога охране.',27,MUTED,maxw=1000)
line(im,[(88,950),(1832,950)],BLUE)
txt(im,88,973,'Точность там, где что-то происходит. Вычисления не тратим там, где ничего не происходит.',32,weight='semi')
save(im)

# 10 — user-supplied genuine LinQ proof, no added captions or cropped labels.
current=10;inv.append(dict(slide=10,text=[],assets=[]))
im=Image.new('RGB',(W,H),'#0e1013')
proof_path=ROOT/'assets/linq/ARGUS_linq_tpu_frame0.png'
proof=Image.open(proof_path).convert('RGB');proof=ImageOps.contain(proof,(W,H),Image.Resampling.LANCZOS)
im.paste(proof,((W-proof.width)//2,(H-proof.height)//2))
inv[-1]['assets'].append(dict(path=str(proof_path.relative_to(ROOT)),sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),rect=[(W-proof.width)//2,(H-proof.height)//2,proof.width,proof.height],crop=None,kind='User-supplied real industrial dataset frame with saved LinQ TPU output; original captions preserved'))
save(im)

# 09 — actual test count, configured timeout, real loss-of-observation evidence.
report=json.loads((ROOT/'evidence/frontend-tests.json').read_text())
assert report['success'] and report['numFailedTests']==0,'Frontend proof is incomplete; do not claim passing tests.'
count=report['numPassedTests']
im=start(11,'Надёжность продукта',demo=True)
heading(im,'Тревога не должна потеряться.')
for x,number,label,c in [(88,'352','теста backend¹',CYAN),(690,str(count),'тестов frontend',VIOLET),(1292,'45 с','автопередача красного²',AMBER)]:
    txt(im,x,288,number,122,c,weight='semi',maxw=530);txt(im,x+5,444,label,34,MUTED,maxw=530)
line(im,[(88,520),(1825,520)])
txt(im,88,572,'Один эпизод —\nодна карточка тревоги.',48,weight='semi',maxw=875)
txt(im,91,741,'Зафиксированный API-контракт',35,CYAN,weight='semi',maxw=900)
txt(im,91,811,'Потеря сигнала не выглядит как безопасность.',31,MUTED,maxw=900)
asset(im,'01-dispatcher-calm.png',(1098,575,727,150),crop=(1182,841,1544,904),contain=True);rect(im,(1098,575,1825,725),None,AMBER)
asset(im,'01-dispatcher-calm.png',(1460,760,365,217),crop=(1360,944,1544,1054));rect(im,(1460,760,1825,977),None,AMBER)
txt(im,1098,772,'«Нет\nнаблюдения»',39,AMBER,weight='semi',maxw=333)
txt(im,88,927,'¹ Отчёт main.  ² Включено в конфигурации; натурный замер не подтверждён.',25,MUTED,maxw=1300)
save(im)

# 10 — an explicit proposed deployment, rooted in a photographed factory frame.
im=start(12,'Для бизнеса · план и гипотезы',photo='conveyor.png');shade(im,left=165,right=130)
heading(im,'Начинаем с участка. Масштабируем по фактам.')
for n,(head,body,c) in enumerate([('Пилот','Один участок\nи согласованные сценарии',CYAN),('Измерения','Качество, ложные тревоги\nи время реакции',VIOLET),('Масштаб','Решение по результатам\nи рабочему процессу',AMBER)]):
    x=88+n*594;rect(im,(x,363,x+536,664),'#20262b',LINE,r=9)
    txt(im,x+27,398,head,51,c,weight='semi',maxw=480);txt(im,x+29,492,body,34,MUTED,maxw=480)
    if n<2:arrow(im,(x+546,510),(x+581,510),c)
rect(im,(88,766,1825,944),'#1a2026',CYAN,r=9)
txt(im,121,796,'Гипотеза поставки',28,CYAN,weight='semi',maxw=620)
txt(im,121,851,'On-prem рядом с LinQ',46,weight='semi',maxw=900)
txt(im,1178,823,'Интеграция по API\nв процессы предприятия',36,MUTED,maxw=600)
txt(im,88,976,'Синтетическая иллюстрация · цены и эффект не обещаем до пилота',24,MUTED)
save(im)

# 11 — completed product proof and the honest next acceptance step.
# 13 — external context and pilot-based economics; no promised payback period.
im=start(13,'Для бизнеса · источники и границы эффекта')
heading(im,'Экономика')
txt(im,92,230,'Ценность — в снижении рисков и управляемой реакции.',33,MUTED)
for x,w in [(88,532),(650,596),(1276,556)]:rect(im,(x,307,x+w,678),PANEL,LINE,r=8)
txt(im,113,335,'1,17',94,BLUE,weight='semi',maxw=470)
txt(im,116,452,'на 1000 работников в год',32,weight='semi',maxw=480)
txt(im,116,509,'Пострадавшие на производстве\nОбрабатывающая промышленность',29,MUTED,maxw=480)
txt(im,116,607,'Росстат · 2025',28,BLUE,weight='semi',maxw=480)
txt(im,116,644,'Форма 7-травматизм · опубликовано в 2026',23,DIM,maxw=480)
txt(im,678,348,'до 150 тыс. ₽',64,BLUE,weight='semi',maxw=540)
txt(im,678,441,'Штраф юрлицу за необеспечение',30,weight='semi',maxw=540)
txt(im,678,481,'СИЗ 2-го класса риска',30,weight='semi',maxw=540)
txt(im,678,535,'При повторном — приостановка\nдеятельности до 90 суток',30,MUTED,maxw=540)
txt(im,678,627,'КоАП 5.27.1, ч. 4, 5 · ред. 2026',27,BLUE,weight='semi',maxw=540)
txt(im,1304,335,'−69%',94,BLUE,weight='semi',maxw=500)
txt(im,1304,452,'зарегистрированных нарушений',31,weight='semi',maxw=500)
txt(im,1304,509,'Кейс АлЭС, Казахстан\nДанные заказчика, не травматизм',29,MUTED,maxw=500)
txt(im,1304,607,'Самрук-Энерго · 2026',28,BLUE,weight='semi',maxw=500)
txt(im,1304,644,'Внешний кейс, не результат пилота Argus',23,DIM,maxw=500)
txt(im,88,720,'Эффект: снижение рисков и повторных нарушений,',40,weight='semi')
txt(im,88,774,'ускорение реакции и меньше ручного контроля.',40,weight='semi')
line(im,[(88,857),(1832,857)],BLUE)
txt(im,88,892,'Точная окупаемость — после пилота.',43,BLUE,weight='semi')
txt(im,88,957,'Калькулятор в продукте показывает точку безубыточности при заданных допущениях.',33,MUTED)
save(im)

im=start(14,'Что готово и что дальше',demo=True)
heading(im,'Цикл реакции собран. Качество проверяем.')
monitor(im,'08-journal-preview.png',88,327,920,RED)
phone(im,'07-master-resolved.png',809,585,175,CYAN)
badge(im,88,907,'Оператор → мастер → журнал',CYAN,size=27)
for y,head,body,c in [(315,'Замкнуть TPU-контур','Стабильный общий прогон,\nа не только отдельные исполнения',CYAN),(525,'Оценить на размеченных видео','Качество событий и ложные тревоги;\nотдельно — задержка уведомления',VIOLET),(735,'Дообучить нужные сценарии','Каска, огонь, курение —\nпосле подготовки подходящих данных',AMBER)]:
    txt(im,1110,y,head,38,c,weight='semi',maxw=715);txt(im,1110,y+66,body,31,MUTED,maxw=715)
txt(im,1110,936,'Промышленный пилот ещё впереди.',29,MUTED,maxw=715)
save(im)

# 12 — brand lockup and actual team names, never invented portraits or roles.
im=start(15,'Команда',photo='toolshop.png');shade(im,left=225,right=25)
lockup(im,88,140,184)
txt(im,94,457,'Увидеть — мало.\nНужно довести до мер.',62,weight='semi',maxw=1100)
line(im,[(94,666),(1040,666)],CYAN,3)
names=['Ожигов Егор','Панин Матвей','Закон Марк','Ведерников Федор','Кашин Глеб']
for n,name in enumerate(names):
    col=n//3;row=n%3;txt(im,94+col*552,718+row*75,name,39,maxw=520)
txt(im,94,963,'Команда продукта · синтетическая иллюстрация',25,MUTED)
save(im)

assert len(inv)==N
(ROOT/'evidence/composition.json').write_text(json.dumps(dict(canvas=[W,H],brand_constant=BRAND,brand_lockups=2,brand_policy='One reusable lockup; cover and ending as requested. Native logos inside authentic screenshots are preserved.',slides=inv),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sheet=Image.new('RGB',(1968,16+math.ceil(N/2)*564),BG)
for n in range(1,N+1):sheet.paste(Image.open(ROOT/f'slides/slide-{n:02}.png').resize((960,540),Image.Resampling.LANCZOS),(16+((n-1)%2)*976,16+((n-1)//2)*564))
sheet.save(ROOT/f'preview/ALL_{N}_SLIDES.png',optimize=True)
print(f'{N} image slides composed; exact glyphs, text bounds and text overlaps checked.')
