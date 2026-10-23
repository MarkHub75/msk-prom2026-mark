from pathlib import Path
import re, json, hashlib

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'_WORK'
def read(p): return (ROOT/p).read_text(encoding='utf-8-sig')
def write(p,s): (ROOT/p).write_text(s.rstrip()+'\n',encoding='utf-8')
units={}
for n in range(1,18):
    p=next(WORK.glob(f'W1_*/U{n:02}.md'))
    units[f'W1-U{n:02}']=(p.relative_to(ROOT).as_posix(),p.read_text(encoding='utf-8-sig'))
for pkg,names in [('PROCESS',['K001','K002','K004','K009','K011']),('EXPERIENCE',['K005','K006','K007']),('CONTRACT',['K003','K008','K010'])]:
    for name in names:
        p=f'_WORK/W2_{pkg}/{name}.md'; units[f'{pkg}-{name}']=(p,read(p))
units['CONTRACT-LOG']=('_WORK/W2_CONTRACT/SEARCH_LOG.md',read('_WORK/W2_CONTRACT/SEARCH_LOG.md'))

# Publication/version, kind, author, locator. Access is a different field below.
META={
'W1-U01-S01':('22.04.2021; №274н; рег.24.05.2021 №63604; копия сохранена 28.05.2021','DOC','Минтруд России; PDF-копия КонсультантПлюс на государственном домене СПб','раздел II; III; A/03.6,A/05.6,A/06.6'),
'W1-U01-S02':('30.07.2026 №324н; рег.02.09.2026 №88111; вступление 01.03.2027','DOC','Минтруд России; воспроизведение КонсультантПлюс','пп.1–3; оригинальный скан не получен'),
'W1-U01-S03':('дата/версия не указаны','SELF-REPORT','Псковский завод Титан-Полимер','вакансии инженера по режиму/охране и начальника отделения ПЭТ'),
'W1-U01-S04':('отчётный 2024; выпуск 26.05.2025','SELF-REPORT','Норникель','подрядчики; аудит ремонтных работ'),
'W1-U01-S05':('отчётный 2024; выпуск 26.05.2025','SELF-REPORT','Норникель','GRI 403-2–403-3'),
'W1-U02-S01':('дата полного зеркала неизвестна; связанный релиз 07.10.2021 получен лишь оболочкой','SELF-REPORT','Норникель / Цифровой Норникель','абзацы Дмитрия Санникова'),
'W1-U02-S02':('дата вакансии не указана','SELF-REPORT','СПб ГБУ Мостотрест','Обязанности/Требования/Условия'),
'W1-U02-S03':('обновлено 06.08.2026; оригинал работодателя не восстановлен','SELF-REPORT','Бобровский сыродельный завод; агрегатор Своё в АПК','Обязанности/Условия'),
'W1-U02-S04':('обновлено 19.10.2026; оригинал HH не получен','SELF-REPORT','Таврия; агрегатор Своё в АПК','Обязанности/Требования'),
'W1-U03-S01':('дата/редакция PDF неизвестны; каталог 10.11.2023 не доказан как дата файла','DOC','СИБУР','вся одностраничная памятка ПАБ'),
'W1-U03-S02':('страница без даты; титул ПЛ-05.05-02 ред.1.0 от 23.04.2024 №22; до12.04.2028','DOC','АО Газпром шельфпроект','Стоп-карты на HTML; PDF только титул'),
'W1-U03-S03':('проект январь–октябрь2024; дата публикации неизвестна; планы2024–2025','VENDOR','Икс-Игрек-Зет Автоматизация; конкурс 1С','Задачи/Мероприятия/Происшествия/Проверки/Суточная отчётность/Стоп-карты/доступ'),
'W1-U04-S01':('04.12.2024 13:48; журнал №12/2024','SELF-REPORT','Дмитрий Гаренских, ООО Газпром бурение; Neftegaz.RU','Второй кит — цифровизация производственной безопасности'),
'W1-U04-S02':('июль2025 на титуле; URL-папка2025/10 не дата документа','VENDOR','ГК ХайТэк / ИВА Когнитив','17страниц; PDFс.5–6,10 (0-based4–5,9)'),
'W1-U05-S01':('дата/версия неизвестны','DOC','UK HSE','Key principles, HTML48–68'),
'W1-U05-S02':('дата издания не установлена; Chemicals Sheet No6','DOC','UK HSE','PDF4стр, p1–2 Alarm rate targets/Operator Reliability'),
'W1-U05-S03':('Fourth Edition; contents filename November2024; full text не получен','DOC','EEMUA','карточка издателя Scope/edition'),
'W1-U05-S04':('Applied Ergonomics47(2015)220–228; DOI2014.10.001; author upload08.10.2018','MEAS','F.Donald,C.Donald,A.Thatcher','авторское full-text представление ResearchGate; abstract/introduction/discussion,pp220,226–228; PDF отдельно не скачан'),
'W1-U05-S05':('дата/версия неизвестны','DOC','UK HSE','Control systems: Alarm presentation/processing/system management'),
'W1-U06-S01':('XProtect2025r3; Last Updated19.08.2026','DOC','Milestone','Alarm definition settings/Operator action required/Maps/Other'),
'W1-U06-S02':('FindFace Multi2.2.1; дата страницы неизвестна','DOC','NtechLab','Application Configuration step7; Work with Alarm Monitor'),
'W1-U07-S01':('Macroscop online4.7; дата текста неизвестна','DOC','Macroscop','Подключение и настройка камер'),
'W1-U07-S02':('online4.7; build клиента неизвестен','DOC','Macroscop','прямое подключение; Подключение через сервер'),
'W1-U07-S03':('online4.7; дата неизвестна','DOC','Macroscop','Статус Инфо/Конфигуратор/Клиент'),
'W1-U07-S04':('HTML version/date неизвестны','DOC','DSSL/TRASSIR','IP devices→Adding IP devices using RTSP'),
'W1-U07-S05':('HTML version/date неизвестны','DOC','DSSL/TRASSIR','IP devices→ONVIF'),
'W1-U07-S06':('HTML version/date неизвестны','DOC','DSSL/TRASSIR','Settings/Detector status monitoring'),
'W1-U07-S07':('Axxon One3.0/3.1; создан09.04.2025','DOC','AxxonSoft; Alina Luchkina','CSV import/поля/Attention'),
'W1-U07-S08':('Macroscop online4.7; дата неизвестна','DOC','Macroscop','Камеры/Тревоги/Ячейки камер'),
'W1-U07-S09':('дата/номер закупки неизвестны; z5385 имя файла','DOC','ОАО НК Янгпур; частное ТЗ обычного СВН','PDF5стр; прочитан текстс.1–4; схемаc.5 не интерпретировалась'),
'W1-U08-S01':('Macroscop online4.7; дата неизвестна','DOC','Macroscop','включение/зона/линия/требования СИЗ/Размеры человека'),
'W1-U08-S02':('навигация4.6 в части открытий, соседние страницы4.7; единый build не установлен','DOC','Macroscop','Проверено наличие спецодежды; условия события'),
'W1-U08-S03':('HTML version/date неизвестны','DOC','DSSL/TRASSIR','Activation/Action/Condition'),
'W1-U08-S04':('HTML version/date неизвестны','DOC','DSSL/TRASSIR','создание schedule/Enable schedule/использование'),
'W1-U08-S05':('Axxon One2.0; updated01.07.2025','DOC','AxxonSoft; Darya Andryieuskaya','General algorithm/working mode/Cycle rules/Editing macros'),
'W1-U08-S06':('Axxon One3.0/3.1; updated20.08.2026','DOC','AxxonSoft; Alena Kniazeva','General information/Bulk application/Attention'),
'W1-U08-S07':('дата/версия неизвестны','VENDOR','Intenseye','Products/Data privacy/Installation; activate EHS scenarios/send alert/Connectivity'),
'W1-U09-S01':('current updated29.09.2026; old version49 от05.04.2021 не основа','DOC','DSSL/TRASSIR; Александр Акимов, update Ольга Селезнева','Описание/типы реакций/Telegram/Express/MAX/SMS/выходы/тревога'),
'W1-U09-S02':('live docs без указанной версии/даты','DOC','MAX для разработчиков','Как создать/Отправка API-запросов/Добавление в чаты'),
'W1-U09-S03':('live docs без указанной версии/даты','DOC','MAX для разработчиков','Как получать события/Webhook'),
'W1-U09-S04':('Bot API10.3; recent changes24.08.2026','DOC','Telegram','sendMessage/CallbackQuery'),
'W1-U09-S05':('L138 Second Edition2013','DOC','UK HSE','PDFpp86–87 §§413–417'),
'W1-U09-S06':('Safety Science16(1993)637–654','MEAS','M.Wogalter,M.Kalsher,B.Racicot','авторский PDF18стр;pp637,641–645,650–652; локальные WOGALTER_1993.pdf/_EXTRACT.txt'),
'W1-U09-S07':('Горный журнал№6/2015 с93–96; DOI10.17580/gzh.2015.06.19','SELF-REPORT','Кубузов,Куренкин,Толпаров(Норникель),Кожиев','издательский PDFс93–96,особенно95–96'),
'W1-U10-S01':('PACM HCI5 CSCW1 Article188 April2021; DOI10.1145/3449287','MEAS','Z.Buçinca,M.B.Malaya,K.Z.Gajos','авторский Harvard PDF:abstract,§§3.1–3.6/results/discussion'),
'W1-U10-S02':('CHI2019; DOI10.1145/3290605.3300233','DOC','Amershi et al.; Microsoft Research','авторский PDF19страниц:abstract/Table1/validation'),
'W1-U10-S03':('XProtect2025r3; Last Updated04.08.2026','DOC','Milestone','основной текст Acknowledge alarms'),
'W1-U11-S01':('footer Июль2023, тело включает февраль2024; версия/обновление неизвестны','SELF-REPORT','Норникель ESG Insights','шаги1,2,4,6'),
'W1-U11-S02':('отчётный2024; выпуск26.05.2025; план с2025','SELF-REPORT','Норникель','новый подход внутренних аудитов; абзацы/таблица профилактики'),
'W1-U11-S03':('отчётный2024; выпуск26.05.2025','SELF-REPORT','Норникель','Изменения2024 в расследовании; подрядчики'),
'W1-U12-S01':('07.10.2026 по открытому тексту','SELF-REPORT','ФНПР; выступления Безюкова/Алексеева/Черногаева','HTML256–278; заключение конференции'),
'W1-U12-S02':('опрос2022; карточка27.03.2023; титул22.03.2023; DOI10.1787/ea0a0fe1-en','MEAS','Lane,Williams,Broecke; OECD','главы2,7,8;табл2.1;рис7.3,8.5; обложка288/шапка287 — одна публикация'),
'W1-U12-S03':('2022 copyright; ISBN9789220368947; точная дата неизвестна','DOC','Frank Hendrickx; ILO WP62','§3.10 Collective rights; Code12.2/5.11'),
'W1-U12-S04':('дата неизвестна; исторический контекст августа2021','SELF-REPORT','РОСПРОФЖЕЛ / портал ФНПР','мобильное приложение/цифровизация инспекций'),
'W1-U13-S01':('XProtect Mobile2025r3; Last Updated04.09.2026','DOC','Milestone','Emergency Alert Notes/steps1–3'),
'W1-U13-S02':('дата/версия неизвестны','DOC','SafeWork NSW,Австралия','риски/What you can do'),
'W1-U14-S01':('online4.7; требуется Macroscop≥4.4,Sigur1.1.1.53.s','DOC','Macroscop','Конфигуратор/общие/камера/автоматизация/журнал'),
'W1-U14-S02':('online4.7; Macroscop≥4.3,Sigur1.1.1.53.s','DOC','Macroscop','лицензия/мастер/Наблюдение и Управление/планы/состояния'),
'W1-U14-S03':('online4.7; дата неизвестна','DOC','Macroscop','Отправить HTTP-запрос/Требования/Переменные'),
'W1-U14-S04':('18.12.2023; 1С:ЗУП КОРП; релиз неизвестен','DOC','Фирма 1С','нормы/выдача/списание/продление/аналитика'),
'W1-U14-S05':('1С:Предприятие8; ссылка8.3; дата/минимальная версия неизвестны','DOC','Фирма 1С','HTTP-сервисы/обработчики/публикация'),
'W1-U14-S06':('№4596118; опубликовано10.09.2026; окончание28.09.2026','DOC','ПАО ЭЛ5-ЭНЕРГО; первичная карточка B2B-Center','обслуживание Macroscop Конаковской ГРЭС; приложение ТЗ не получено'),
'W1-U15-S01':('дата/версия неизвестны','VENDOR','Intenseye','What is Actions/Task creation&routing/Coaching/Toolbox talks/FAQ'),
'W1-U15-S02':('22.04.2025; версия продукта неизвестна','VENDOR','Rachel Richardson; Voxel','Actions in platform/Key Capabilities/From risk to resolution'),
'W1-U15-S03':('дата/версия неизвестны','VENDOR','Protex AI','Area Control Highlights/Customize rules/Track patterns/Drive outcomes'),
'W1-U16-S01':('дата неизвестна; полный ISA101 не получен','DOC','ISA101 committee','Scope/Purpose'),
'W1-U16-S02':('полученный cover Revised Feb2026; сниппет18.12.2023 не принят','UNKNOWN','American Water Military Services Group','PDF188стр: cover; HMI/IGNITION appendix в открытом тексте не найден'),
'W1-U16-S03':('WCAG2.2 W3C Recommendation12.12.2024','DOC','W3C','SC1.4.1,1.4.3,1.4.11,2.1.1,2.4.7,2.5.7,2.5.8,4.1.3'),
'W1-U17-S01':('официальный сайт2026; дата редакции неизвестна','DOC','Организаторы Открой#Моспром2026','кейс LinQ/расписание/Положение; ЛК не получен'),
'W1-U17-S02':('Положение2026; дата редакции неизвестна','DOC','Организаторы Открой#Моспром2026','24страницы; прочитаны §1.2/1.4/1.10 с2–3 и §6.1–6.4 с9–10'),
'W2-PROCESS-S01':('03.04.2025 10:24','SELF-REPORT','Анна Соловьева; Kn51; прямые слова Игнатьева/Стасюка','Умные камеры/Минимизировать риски'),
'W2-PROCESS-S02':('28.07.2025 10:24','SELF-REPORT','Марина Папка; Kn51; Игнатьев/Мокрышев','основной текст; та же линия и редакционная цепочка S01'),
'W2-PROCESS-S03':('04.07.2024 12:03; статус пилота двух бригад','SELF-REPORT','ООО Газпром подземремонт Уренгой; Дмитрий Основский','разработка/слова начальника центральной службы мониторинга'),
'W2-PROCESS-S04':('П КГМК179-62-2025; приказ27.06.2025№КГМК/255-п; введено27.06.2025','DOC','АО Кольская ГМК','PDF45стр; титул/область/13.8,14.1.16/32,15.1–15.4,16.1,17'),
'W2-PROCESS-S05':('116-ФЗ21.07.1997; шапка изменения04.08.2026; вступление всех поправок независимо не сверено','DOC','Закон РФ в системе Кодекс; subdomain не подтверждает сайт Ростехнадзора','шапка/преамбула/ст1–2; не официальный портал публикации'),
'W2-EXPERIENCE-S01':('дата/версия неизвестны','VENDOR','Protex AI','Watch Demo заголовок/form HTML0–35; player не проверен'),
'W2-EXPERIENCE-S02':('отзывы17.02,14.10,19.10.2026; HTML date_modified20.10.2026; версии продукта неизвестны','SELF-REPORT','G2: Amanda B.,Ariana L.,Syed Z.; profile managed by Protex','Amanda273–308;Syed310–339;Ariana182–209; исходные dislike/problems'),
'W2-EXPERIENCE-S03':('дата/версия неизвестны','VENDOR','Protex AI','How works HTML17–39;Technical FAQ3/6/8'),
'W2-EXPERIENCE-S04':('Website DPA Oct2025 footer/metadata; точный день неизвестен','DOC','Protex AI; договорный шаблон, не подписанный договор клиента','8страниц;p4§8;p5§11;p6Schedule1§1.2;p8Schedule2; p6render просмотрен'),
'W2-EXPERIENCE-S05':('Last updated09.10.2026','VENDOR','Protex AI','Protex Intelligence/Privacy-security-data HTML35,54–67'),
'W2-EXPERIENCE-S06':('дата/версия неизвестны','VENDOR','Protex AI','homepage FAQ HTML609–622'),
'W2-EXPERIENCE-S07':('дата/версия неизвестны','VENDOR','Voxel; curated Carlex Glass story,Vonore,Tennessee','Solution/Success HTML33–50; прямое соглашение UAW не получено'),
'W2-EXPERIENCE-S08':('Intenseye Public APIv2; дата страницы неизвестна','DOC','Intenseye','Alerts Arguments/Returns/P.S HTML48–74; API не вызывался'),
'W2-EXPERIENCE-S09':('Intenseye Public APIv2; дата страницы неизвестна','DOC','Intenseye','GET/accuracy/export Returns/examples HTML20–76; JSON пример не измерение'),
'W2-CONTRACT-S01':('FindFace Multi2.2.1; дата неизвестна','DOC','NtechLab','Alert Manager/Work with Alarm Feed HTML59–69,117–182'),
'W2-CONTRACT-S02':('XProtect2025r3; Last Updated16.09.2026','DOC','Milestone','State/Assigned to/Activities HTML30–43'),
'W2-CONTRACT-S03':('RESTful Alarms API1.0.0; Requirements XProtect2023R2+; дата неизвестна','DOC','Milestone','Update alarm3123–3146;history4708–4786;snapshot4793–4900; полный API не прочитан'),
}

SID_RX=r'W[12]-(?:U\d{2}|PROCESS|EXPERIENCE|CONTRACT)-S\d{2}'
FID_RX=r'W[12]-(?:U\d{2}|PROCESS|EXPERIENCE|CONTRACT)-F\d{2}'
sources={}
for unit,(path,txt) in units.items():
    headings=list(re.finditer(r'(?m)^#{1,4}\s+('+SID_RX+r')\s*—\s*(.*)$',txt))
    for i,m in enumerate(headings):
        old=m.group(1)
        if old not in META: continue
        end=headings[i+1].start() if i+1<len(headings) else len(txt)
        block=txt[m.end():end]
        # Restrict metadata to before the first factual definition (some share a paragraph).
        fm=re.search(FID_RX,block)
        before=block[:fm.start()] if fm else block.split('\n## ')[0]
        urls=re.findall(r'https?://[^\s<>]+',before)
        urls=[u.rstrip(').,;') for u in urls]
        sources[old]={'old':old,'title':m.group(2).strip(),'path':path,'meta_original':before.strip(),'urls':list(dict.fromkeys(urls))}
# Source inline definitions.
for old,path in [('W1-U14-S06','_WORK/W1_PRODUCT/U14.md'),('W1-U17-S01','_WORK/W1_PRODUCT/U17.md'),('W1-U17-S02','_WORK/W1_PRODUCT/U17.md')]:
    txt=read(path); line=next(l for l in txt.splitlines() if old in l)
    before=line.split('**W1-U17-F')[0].split('**W1-U14-F')[0]
    sources[old]={'old':old,'title':{'W1-U14-S06':'B2B-Center №4596118, обслуживание СВН Конаковской ГРЭС','W1-U17-S01':'Официальный сайт Открой#Моспром2026','W1-U17-S02':'Положение о молодёжном хакатоне2026'}[old],'path':path,'meta_original':before,'urls':[u.rstrip(').,;') for u in re.findall(r'https?://[^\s<>]+',before)]}
assert set(META)==set(sources),(set(META)-set(sources))
S_MAP={old:f'S{i:03}' for i,old in enumerate(META,1)}
S_MAP['W1-U02-S05']=S_MAP['W1-U01-S03']
S_MAP['W1-U04-S03']=[S_MAP[x] for x in ['W1-U02-S02','W1-U03-S01','W1-U03-S03']]

facts={}
def add(old,body,path,kind=None,src=None,title=None):
    assert old not in facts,old
    prefix=old.rsplit('-F',1)[0] if '-F' in old else old.split(':')[0]
    facts[old]={'old':old,'body':body.strip(),'path':path,'prefix':prefix,'kind':kind,'src':src or [],'title':title}

def para_def(txt,old):
    # All primary local F definitions have a bracket immediately after the ID.
    ms=list(re.finditer(re.escape(old)+r'\s*\[([^\]]+)\]',txt))
    if not ms: return None,None
    m=ms[0]; end=txt.find('\n\n',m.end())
    if end<0:end=len(txt)
    nextdef=re.search(r'\n(?:-\s+)?\*{0,2}'+FID_RX+r'\s*\[',txt[m.end():end])
    if nextdef:end=m.end()+nextdef.start()
    samepara=re.search(r'\*{0,2}'+FID_RX+r'\s*\[',txt[m.end():end])
    if samepara:end=m.end()+samepara.start()
    body=txt[m.end():end].lstrip('*: .')
    return body,m.group(1)

KIND_OVERRIDES={
'W1-U01-F03':'INF','W1-U02-F02':'UNKNOWN','W1-U02-F06':'INF','W1-U03-F02':'INF','W1-U03-F04':'LOCAL-OBS',
'W1-U04-F03':'UNKNOWN','W1-U04-F05':'INF','W1-U05-F05':'INF','W1-U06-F03':'INF','W1-U06-F04':'INF',
'W1-U09-F06':'INF','W1-U10-F04':'INF','W1-U11-F03':'INF','W1-U12-F02':'INF','W1-U13-F03':'INF',
'W1-U16-F02':'UNKNOWN','W1-U16-F04':'INF','W1-U17-F03':'INF','W1-U17-F04':'HYP','W1-U17-F05':'INF','W1-U17-F06':'INF',
'W2-EXPERIENCE-F01':'VENDOR','W2-EXPERIENCE-F02':'LOCAL-OBS','W2-EXPERIENCE-F03':'SELF-REPORT','W2-EXPERIENCE-F04':'HYP','W2-EXPERIENCE-F09':'INF',
'W2-EXPERIENCE-F10':'VENDOR','W2-EXPERIENCE-F14':'INF',
}
W1_COUNTS=[7,6,6,5,6,4,10,8,8,4,8,6,3,7,6,4,6]
for n,count in enumerate(W1_COUNTS,1):
    pref=f'W1-U{n:02}';path,txt=units[pref]
    for k in range(1,count+1):
        old=f'{pref}-F{k:02}';body,rawkind=para_def(txt,old)
        if body is None:
            # IDs in section headings designate a table/procedure, all retained.
            h=re.search(r'(?m)^## .*'+re.escape(old)+r'.*$',txt)
            assert h,old
            e=re.search(r'(?m)^## ',txt[h.end():]);end=h.end()+e.start() if e else len(txt)
            body=txt[h.end():end];rawkind='INF'
        pos=txt.find(old+' [')
        if pos<0:pos=txt.find(old)
        sourceheads=list(re.finditer(r'(?m)^#{1,4}.*('+SID_RX+r')',txt[:pos]))
        src=[sourceheads[-1].group(1)] if sourceheads else []
        src=[s for s in src if s in S_MAP]
        # Documentary F before source heading in intro must not select a source by accident.
        if old=='W1-U02-F06':src=['W1-U01-S03']
        if old in ['W1-U17-F01','W1-U17-F02']:src=[old.replace('-F','-S')]
        kind=KIND_OVERRIDES.get(old)
        if not kind:
            if rawkind in ['INF','наш вывод из F01/F02','наш вывод']:kind='INF'
            elif any(t in rawkind.lower() for t in ['измерение','опубликованный опрос']):kind='MEAS'
            elif 'VENDOR' in rawkind or 'поставщика' in rawkind or 'заявление внедрения' in rawkind:kind='VENDOR'
            elif src:kind=META[src[0]][1] if src[0] in META else 'INF'
            else:kind='INF'
        if n==15 and k in [4,5,6]:kind='INF'
        if n in [7,8,14] and k==count and rawkind=='INF':kind='INF'
        add(old,body,path,kind,src)

# W2 source facts.
for pkg,count in [('PROCESS',7),('EXPERIENCE',16),('CONTRACT',4)]:
    for n in range(1,count+1):
        old=f'W2-{pkg}-F{n:02}'
        found=None
        for unit,(path,txt) in units.items():
            if not unit.startswith(pkg+'-'):continue
            body,rawkind=para_def(txt,old)
            if body is not None:found=(path,txt,body,rawkind);break
        if not found:continue
        path,txt,body,rawkind=found
        pos=txt.find(old+' [')
        sourceheads=list(re.finditer(r'(?m)^#{1,4}.*('+SID_RX+r')',txt[:pos]))
        src=[sourceheads[-1].group(1)] if sourceheads else []
        kind=KIND_OVERRIDES.get(old)
        if not kind:kind=META[src[0]][1] if src and src[0] in META else 'INF'
        if old=='W2-EXPERIENCE-F02':src=[]
        if old=='W2-EXPERIENCE-F09':src=['W2-EXPERIENCE-S04','W2-EXPERIENCE-S05','W2-EXPERIENCE-S06']
        if old=='W2-EXPERIENCE-F14':src=['W2-EXPERIENCE-S09']
        # W2 contract F04 appears in same paragraph after F03; cap first at second marker.
        if pkg=='CONTRACT' and n==3:body=body.split('**W2-CONTRACT-F04')[0].rstrip()
        add(old,body,path,kind,src)

def section(path,start,end=None):
    txt=read(path);a=txt.index(start)+len(start)
    b=txt.index(end,a) if end else len(txt)
    return txt[a:b].strip()

# Long authorial models get one F each; only one canonical copy of each table.
models=[
('W2-EXPERIENCE-F02','_WORK/W2_EXPERIENCE/K005.md','## W2-EXPERIENCE-F02 — точный blocker screenshot-first [OBS]','## W2-EXPERIENCE-S02','LOCAL-OBS'),
('W2-EXPERIENCE-F04','_WORK/W2_EXPERIENCE/K005.md','## Изменение рекомендации [W2-EXPERIENCE-F04, INF]','## Что осталось неизвестным','HYP'),
('W2-EXPERIENCE-F11','_WORK/W2_EXPERIENCE/K006.md','## Предлагаемый data flow для нашего MVP [W2-EXPERIENCE-F11, INF]','## Маскирование','INF'),
('W2-EXPERIENCE-F15','_WORK/W2_EXPERIENCE/K007.md','## Предложенный контракт [W2-EXPERIENCE-F15, INF]','## Независимый архивный путь','INF'),
('W2-EXPERIENCE-F16','_WORK/W2_EXPERIENCE/K007.md','## Независимый архивный путь [W2-EXPERIENCE-F16, INF]','## Остаток неизвестного','INF'),
('W2-CONTRACT-F05','_WORK/W2_CONTRACT/K003.md','## Словарь [W2-CONTRACT-F05, INF]','## Переходы','INF'),
('W2-CONTRACT-F06','_WORK/W2_CONTRACT/K003.md','## Переходы и условия [W2-CONTRACT-F06, INF]','## Что меняется','INF'),
('W2-CONTRACT-F07','_WORK/W2_CONTRACT/K008.md','## Поля, истина и деградация [W2-CONTRACT-F07, INF]','## Clock domains','INF'),
('W2-CONTRACT-F08','_WORK/W2_CONTRACT/K008.md','## Clock domains [W2-CONTRACT-F08, INF]','## Адресная передача','INF'),
('W2-CONTRACT-F09','_WORK/W2_CONTRACT/K010.md','## Выбранный минимальный объём A','## Проверяемый demo contract','HYP'),
('W2-CONTRACT-F10','_WORK/W2_CONTRACT/K010.md','## Проверяемый demo contract [W2-CONTRACT-F10, INF]','## Что изменили','HYP'),
]
for old,path,start,end,kind in models:
    body=section(path,start,end)
    if old in facts: facts[old].update(body=body,kind=kind)
    else:add(old,body,path,kind)

# Derived PROCESS tables have no old F-ID; give semantic aliases in the map.
extras=[
('W2-PROCESS:roles-routes','_WORK/W2_PROCESS/K001.md','## Карта строго ограниченных процессов — наша реконструкция','## Что действительно изменилось','INF','Условные роли и два маршрута A/B'),
('W2-PROCESS:urgency','_WORK/W2_PROCESS/K002.md','## Что опровергнуто','## Последствия для демо','INF','Срочность, порядок warning/review и раздельное время'),
('W2-PROCESS:channels','_WORK/W2_PROCESS/K004.md','## Что изменил поиск','## Полевой тест','INF','Канал: условия и честная демонстрация'),
('W2-PROCESS:metrics','_WORK/W2_PROCESS/K009.md','## Вопрос и действие руководителя','## Что изменилось','INF','Один управленческий вопрос, метрики и несопоставимость'),
('W2-PROCESS:terms','_WORK/W2_PROCESS/K011.md','## Наш словарь для MVP','## Адресная передача','INF','Словарь и пределы регулируемой функции'),
]
for old,path,start,end,kind,title in extras:add(old,section(path,start,end),path,kind,title=title)

expected={f'W1-U{n:02}-F{k:02}' for n,c in enumerate(W1_COUNTS,1) for k in range(1,c+1)}|{f'W2-{p}-F{k:02}' for p,c in [('PROCESS',7),('EXPERIENCE',16),('CONTRACT',10)] for k in range(1,c+1)}
assert expected<=set(facts),expected-set(facts)
# Stable order is W1 U01..17, then PROCESS, EXPERIENCE, CONTRACT, then named synthesized tables.
order=[x for x in sorted(expected) if x.startswith('W1-')]
order += [f'W2-{p}-F{k:02}' for p,c in [('PROCESS',7),('EXPERIENCE',16),('CONTRACT',10)] for k in range(1,c+1)]
order += [x[0] for x in extras]
F_MAP={old:f'F{i:03}' for i,old in enumerate(order,1)}

def norm(text,prefix):
    def local_run(m,p):
        return re.sub(r'[FS]\d{2}',lambda x:str(F_MAP.get(p+'-'+x[0],S_MAP.get(p+'-'+x[0],x[0]))),m[0].split('-',1)[-1] if False else m[0][len(m[1])+1:])
    # Resolve slash/range runs while their unit prefix is still known.
    def run_replace(m):
        p=m[1];tail=m[0][len(p)+1:]
        def one(x):
            v=F_MAP.get(p+'-'+x[0],S_MAP.get(p+'-'+x[0],x[0]));return ', '.join(v) if isinstance(v,list) else v
        return re.sub(r'[FS]\d{2}',one,tail)
    text=re.sub(r'(W[12]-(?:U\d{2}|PROCESS|EXPERIENCE|CONTRACT))-[FS]\d{2}(?:[/–—-][FS]\d{2})+',run_replace,text)
    text=re.sub(r'(?<![\w-])(U\d{2})-[FS]\d{2}(?:[/–—-][FS]\d{2})*',lambda m:run_replace(type('M',(),{'__getitem__':lambda self,k:('W1-'+m[1]) if k==1 else ('W1-'+m[0])})()),text)
    text=re.sub(r'(?<![\w-])(PROCESS|EXPERIENCE|CONTRACT)-[FS]\d{2}(?:[/–—-][FS]\d{2})*',lambda m:run_replace(type('M',(),{'__getitem__':lambda self,k:('W2-'+m[1]) if k==1 else ('W2-'+m[0])})()),text)
    # Fully qualified ranges must be expanded before bare references.
    text=re.sub(r'(W[12]-(?:U\d{2}|PROCESS|EXPERIENCE|CONTRACT))-(F\d{2})([–—-])(F\d{2})',lambda m:f'{F_MAP.get(m[1]+"-"+m[2],m[0])}{m[3]}{F_MAP.get(m[1]+"-"+m[4],m[4])}',text)
    def repl(m):
        v=F_MAP.get(m[0],S_MAP.get(m[0]))
        return ', '.join(v) if isinstance(v,list) else v or m[0]
    text=re.sub(FID_RX+'|'+SID_RX,repl,text)
    text=re.sub(r'(?<![\w-])(U\d{2})-(F\d{2})([–—-])(F\d{2})',lambda m:f'{F_MAP.get("W1-"+m[1]+"-"+m[2],m[0])}{m[3]}{F_MAP.get("W1-"+m[1]+"-"+m[4],m[4])}',text)
    text=re.sub(r'(?<![\w-])(U\d{2})-(F\d{2})',lambda m:F_MAP.get('W1-'+m[1]+'-'+m[2],m[0]),text)
    # Short references inside an origin unit are local, not final IDs (two digits).
    def bare(m):
        v=(F_MAP.get(prefix+'-'+m[1]) if m[1][0]=='F' else S_MAP.get(prefix+'-'+m[1])) or m[0]
        return ', '.join(v) if isinstance(v,list) else v
    text=re.sub(r'(?<![\w-])([FS]\d{2})(?!\d)',bare,text)
    # Rebase Markdown file links from evidence directory to root.
    return text

def clean_links(body,path):
    origin=(ROOT/path).parent
    def repl(m):
        target=m[2]
        if target.startswith(('http:','https:','#')):return m[0]
        absolute=(origin/target).resolve()
        try:rel=absolute.relative_to(ROOT).as_posix()
        except ValueError:return m[0]
        return '['+m[1]+']('+rel+')'
    return re.sub(r'\[([^\]]*)\]\(([^\)]+)\)',repl,body)

# Exact source assignments for authorial models and inline metadata; these are bases, not assertions that the source implements our model.
src_overrides={
'W1-U05-F05':['W1-U05-S01','W1-U05-S04','W1-U05-S05'],
'W1-U06-F03':['W1-U06-S01','W1-U06-S02','W1-U10-S01','W1-U10-S02'],
'W1-U06-F04':['W1-U06-S01','W1-U06-S02'],
'W1-U07-F10':[f'W1-U07-S{k:02}' for k in range(1,10)],
'W1-U08-F08':[f'W1-U08-S{k:02}' for k in range(1,8)],
'W1-U09-F06':[f'W1-U09-S{k:02}' for k in range(1,6)],
'W1-U10-F04':['W1-U10-S01','W1-U10-S02','W1-U10-S03'],
'W1-U13-F03':['W1-U13-S01','W1-U13-S02','W1-U09-S04'],
'W1-U14-F06':[f'W1-U14-S{k:02}' for k in range(1,6)],
'W1-U14-F07':['W1-U14-S06'],
'W1-U15-F06':['W1-U15-S01','W1-U15-S02','W1-U15-S03','W1-U07-S03','W1-U08-S02'],
'W1-U16-F04':['W1-U16-S01','W1-U16-S03','W1-U05-S01'],
'W1-U17-F03':['W1-U17-S01','W1-U17-S02','W1-U08-S01','W1-U15-S01','W1-U15-S02','W1-U07-S03'],
'W1-U17-F04':['W1-U17-S02','W1-U15-S01','W1-U15-S02','W1-U06-S01'],
'W1-U17-F05':['W1-U17-S01'],
'W1-U17-F06':['W1-U17-S02','W1-U07-S03','W1-U15-S01','W1-U15-S02'],
'W2-EXPERIENCE-F04':['W2-EXPERIENCE-S02'],
'W2-EXPERIENCE-F11':['W2-EXPERIENCE-S03','W2-EXPERIENCE-S04'],
'W2-EXPERIENCE-F15':['W2-EXPERIENCE-S08','W1-U10-S02'],
'W2-EXPERIENCE-F16':['W2-EXPERIENCE-S09','W2-EXPERIENCE-S03'],
'W2-CONTRACT-F05':['W2-CONTRACT-S01','W2-CONTRACT-S02','W2-CONTRACT-S03','W1-U06-S02'],
'W2-CONTRACT-F06':['W2-CONTRACT-S01','W2-CONTRACT-S02','W2-CONTRACT-S03'],
'W2-CONTRACT-F07':['W2-CONTRACT-S03','W1-U07-S02','W1-U07-S03','W1-U14-S03','W2-EXPERIENCE-S04'],
'W2-CONTRACT-F08':['W1-U14-S01','W1-U14-S03','W1-U13-S01'],
'W2-CONTRACT-F09':['W1-U17-S01','W1-U17-S02','W2-PROCESS-S01','W2-EXPERIENCE-S08'],
'W2-CONTRACT-F10':['W1-U17-S01','W1-U17-S02'],
'W2-PROCESS:roles-routes':['W1-U04-S01','W2-PROCESS-S01','W2-PROCESS-S02','W2-PROCESS-S03'],
'W2-PROCESS:urgency':['W2-PROCESS-S02','W2-PROCESS-S03'],
'W2-PROCESS:channels':['W2-PROCESS-S02','W2-PROCESS-S04'],
'W2-PROCESS:metrics':['W2-PROCESS-S01','W1-U11-S02','W1-U03-S03'],
'W2-PROCESS:terms':['W2-PROCESS-S05','W1-U03-S01','W1-U03-S03'],
}
for old,src in src_overrides.items():facts[old]['src']=src
# Dependency sources: derive explicit IDs + canonical source of upstream facts recursively.
for old,f in facts.items():
    f['deps']=set(re.findall(FID_RX,f['body']))-{old}
    f['src'] += [s for s in re.findall(SID_RX,f['body']) if s in S_MAP]
    # Add documented bases for authorial W1 sections.
    # A source is attached by its actual claim/context, never by all sources in a cell.
for _ in range(5):
    for f in facts.values():
        for d in list(f['deps']):
            if d in facts:f['src'] += facts[d]['src']
        f['src']=list(dict.fromkeys(f['src']))
for old,f in facts.items():
    fs=[]
    for s in f['src']:
        v=S_MAP.get(s,[]);fs.extend(v if isinstance(v,list) else [v])
    f['final_sources']=list(dict.fromkeys(fs))

write('_WORK/COLLECTOR_DATA.json',json.dumps({'sources':sources,'source_map':S_MAP,'facts':facts,'fact_map':F_MAP},ensure_ascii=False,indent=2,default=list))

srcout=['# Источники operator_product','',
'Срез получения: 23.10.2026, Europe/Moscow (+03:00); W1 около08:15–08:30, W2 около08:39–08:53. Сборка только из сохранённых материалов, новых сетевых доказательств нет. Дата публикации/версия ниже отделена от даты доступа. Локаторы относятся к реально прочитанной части. API/ПО/камера/доставка не запускались; опубликованные измерения не наши эксперименты.',
'', 'Типы: DOC — первичный текст документа/спецификации (включая явно обозначенную правовую копию); VENDOR — заявление поставщика/заинтересованного внедренца; SELF-REPORT — рассказ организации, работодателя, профсоюза или пользователя; MEAS — опубликованное исследование с условиями; UNKNOWN — неполученное содержание. LOCAL-OBS применяется к наблюдению среды в RAW_FACTS. Тип не заменяет статус доступа.',
'', 'Несколько страниц одной компании, зеркала и повторные ссылки не считаются независимыми подтверждениями. Карточки источников дают реквизиты и локаторы; извлечённые утверждения находятся только в RAW_FACTS. [Сопоставление local→final](_WORK/ID_MAP.md).','']
for old in META:
    s=sources[old]
    sid=S_MAP[old];date,kind,author,loc=META[old]
    supported=[F_MAP[o] for o,f in facts.items() if sid in f['final_sources']]
    if old=='W1-U16-S02':status='Получен PDF/cover; нужный HMI appendix НЕ получен/не прочитан. Никакой палитры из сниппета.'
    elif old=='W1-U05-S03':status='Прочитана карточка издателя; полный платный стандарт НЕ получен.'
    elif old=='W1-U14-S06':status='Прочитана HTML-карточка; приложение ТЗ НЕ получено.'
    elif old=='W2-EXPERIENCE-S01':status='Прочитан текст demo-entry; player/UI не проверены, форму не заполняли.'
    else:status='Прочитана указанная часть источника; собственный продуктовый/полевой тест не проводился.'
    urls=s['urls']
    srcout += [f'<a id="{sid.lower()}"></a>',f'## {sid} — {s["title"]}',f'**Автор/организация:** {author}. **Тип:** {kind}.',f'**Публикация/версия:** {date}.',f'**Доступ:** 2026-10-23, Europe/Moscow. **Статус:** {status}',
    '**URL:** '+'; '.join(f'[прямой источник {i+1}]({u})' for i,u in enumerate(urls))+'.',
    f'**Локатор:** {loc}.',f'**F-ID:** {", ".join(supported) or "только происхождение/ограничение"}.',
    f'**Происхождение:** `{old}`; [{s["path"]}]({s["path"]}); [{Path(s["path"]).parent.as_posix()}/SEARCH_LOG.md]({Path(s["path"]).parent.as_posix()}/SEARCH_LOG.md).','']
srcout += ['## Недоступные и ограниченно полученные материалы','',
'Не являются подтверждённым содержанием. Повторные попытки в двух волнах не создают независимых доказательств. Отсутствие доступа не доказывает отсутствия функции/документа.','',
'| Материал | Что получено / чего нет | Где происхождение / связанный вопрос |','|---|---|---|']
unavailable=[
('Официальный 324н [0001202609020016](https://publication.pravo.gov.ru/document/0001202609020016)','Официальный скан недоступен web; Medvestnik download за авторизацией; текст пп1–3 прочитан в правовой базе','_WORK/W1_PEOPLE/SEARCH_LOG.md','Q016'),
('Полные положения Газпром шельфпроект','Публичные PDF — только титулы, не полный порядок; стоп-карты HTML прочитаны','_WORK/W1_PEOPLE/SEARCH_LOG.md','Q003'),
('EEMUA191 / ISA18.2 / IEC62682 / ISA101','Карточки scope прочитаны; полные платные тексты не получены; точные пункты не заявлены','_WORK/W1_HUMAN/SEARCH_LOG.md','Q012'),
('American Water HMI appendix','Полученный188страничный PDF revisedFeb2026 не дал HMI/IGNITION; локальная загрузка403; snippet не факт','_WORK/W1_HUMAN/SEARCH_LOG.md','Q012'),
('[metal-it Тех.задание.pdf](https://etp.metal-it.ru/files/get/62wbdjrEsToerTN9EwXP9CpFfBsF9xSzNKxV8QdmWuGdUN4P1Z9RmCqv6HC6Gmdg7j/Тех.%20задание.pdf)','7страниц распознаны,0строк; screenshot без доступного изображения; TLS failure. Не прочитан, заказчик/реквизиты неизвестны','_WORK/W2_PROCESS/SEARCH_LOG.md','Q015'),
('[B2B4596118](https://www.b2b-center.ru/market/okazanie-uslug-po-provedeniiu-tekhnicheskogo-obsluzhivaniia-kompleksa/tender-4596118/)','Карточка прочитана; ТЗ/допполя за регистрацией не получены','_WORK/W2_PROCESS/SEARCH_LOG.md','Q015'),
('[burgaz follow-up](https://www.burgaz.ru/dmitrij-garenskih-ob-opyte-grupp-kompanij-po-vnedreniyu-ii-v-sistemy-proizvodstvennoj-bezopasnosti/)','Timeout/SSL EOF; поисковые30сек и1% не приняты за SLA/качество','_WORK/W2_PROCESS/SEARCH_LOG.md','Q001'),
('Protex demo/UI','Текст entry прочитан; iab Browser is not available; apps=[],browsers=[]; ни одного UI screenshot/клика/UX-аудита','_WORK/W2_EXPERIENCE/SEARCH_LOG.md','Q010'),
('Независимый архив / HSE missed-event UI','Документированный Alerts export есть; независимый архив, write-контракт и пошаговый missed-event workflow не получены','_WORK/W2_EXPERIENCE/SEARCH_LOG.md','Q007'),
('Полный кейс/ЛК/датасет/SDK/runtime/онлайн-доступ LinQ','Входы содержат анонс; получение полного комплекта и execution artifact не подтверждено','_WORK/W2_CONTRACT/HANDOFF.md','Q004'),
]
for a,b,c,q in unavailable:srcout.append(f'| {a} | {b} | [{c}]({c}); [{q}](OPEN_QUESTIONS.md#{q.lower()}) |')
srcout += ['', '## Локальные оригиналы и независимость','',
'Wogalter: [_WORK/W1_HUMAN/WOGALTER_1993.pdf](_WORK/W1_HUMAN/WOGALTER_1993.pdf), UTF8 extract рядом. Protex DPA: [_WORK/W2_EXPERIENCE/PROTEX_DPA_OCT2025.pdf](_WORK/W2_EXPERIENCE/PROTEX_DPA_OCT2025.pdf), [проверенный render p6](_WORK/W2_EXPERIENCE/DPA_P06.png), extract рядом. Сборщик использовал сохранённые локаторы; большие PDF/extract повторно целиком не читались. Render документа не UI-аудит.',
'', 'КГМК2021 (автономный СИЗ), апрель/июль2025 (линия резки) — разные периоды/системные контексты; не один усреднённый объект. Kn51 апрель/июль — одна связанная линия происхождения. Норникель отчёт/ESG — заинтересованное самораскрытие. G2 — отдельные пользовательские самоотчёты в одном профиле, invite не установленная оплата. Voxel/Carlex/UAW — vendor-curated рассказ без прямого соглашения. Правовые копии не доказывают compliance РФ.']
write('SOURCES.md','\n'.join(srcout))

raw=['# Факты, условия и проверяемые предложения operator_product','',
'Срез: 23.10.2026, Europe/Moscow (+03:00). Это доказательная база двух волн до литературного отчёта. Нового поиска, интервью, UI-аудита, исполнения LinQ, тестов камер/каналов/моделей не было. Прочитанные исследователями документы и опубликованные измерения отделены от наших предложений. Все E ниже предложены и НЕ выполнены.',
'', 'Метки: DOC — документ; VENDOR — заинтересованное продуктовое заявление; SELF-REPORT — первичный рассказ организации/работодателя/пользователя; MEAS — опубликованное измерение, с его выборкой; LOCAL-OBS — фактическое наблюдение доступа/среды; INF — наш вывод/контракт; HYP — проверяемое предложение; UNKNOWN — неустановленное. В смешанном факте DOC+INF авторское следствие явно подписано. Условность и статус чтения действуют независимо от метки.',
'', 'Канонические ID ниже стабильны; [происхождение и local→final](_WORK/ID_MAP.md), [источники](SOURCES.md), [вопросы](OPEN_QUESTIONS.md), [историческая критика](CRITIC.md). Прежняя линейная последовательность W1 не универсальна: итоговые независимые статусы, варианты срочности и объём задают W2-модели в конце фактических карточек. Ссылки W1→W2 в этой базе означают уточнение, а не ретроспективное изменение источника.','']
CELL_MEANING={1:'Роли/полномочия нужно разделить; локальный регламент клиента не получен.',2:'Выбор оперативной очереди или асинхронного разбора остаётся условным.',3:'Видео — вход в существующую процедуру; мера и документ отдельны.',4:'Нужны получатель/право/канал и отдельные основания действия.',5:'Нагрузка измеряется по эпизодам и задачам человека; процессные нормы не переносим.',6:'Карточка требует происхождения, материала и независимых решений.',7:'Готовность camera/decode/inference/media показывается раздельно.',8:'Правило публикуется проверяемо; конфигурация не устанавливает норму ОТ.',9:'Отправка не получение, ACK не действие; канал зависит от разрешений.',10:'Оценка, настройка и обучение — разные операции.',11:'Счёт видео не травматизм; решение связано с причиной/мерой и охватом.',12:'Цели, доступ и право оспаривания требуют политики и прямого worker voice.',13:'Поле зависит от безопасного места/устройства/сети.',14:'Обмен требует версии, mapping, времени, прав и получателя.',15:'Документальные паттерны не доказанная удобность и не отсутствие функций у конкурентов.',16:'Web минимум не гарантирует работу смены/поля; палитра не установлена.',17:'Демо показывает происхождение LinQ и решение человека; реальное исполнение пока не получено.'}
for old in order:
    f=facts[old];fid=F_MAP[old];kind=f['kind'];n=int(old[4:6]) if old.startswith('W1-U') else None
    body=clean_links(norm(f['body'],f['prefix']),f['path'])
    # Section headings embedded in fact bodies become subheadings beneath F cards.
    body=re.sub(r'(?m)^## ', '#### ',body)
    title=f['title'] or old
    src=', '.join(f'[{s}](SOURCES.md#{s.lower()})' for s in f['final_sources']) or 'наша модель по сохранённым W1/W2; документ клиента отсутствует'
    raw += [f'<a id="{fid.lower()}"></a>',f'## {fid} — {title}',f'**Тип:** {kind}. **Источники:** {src}.',
    f'**Происхождение/локатор:** `{old}`; [{f["path"]}]({f["path"]}); точные внешние разделы/страницы и публикация/версия — в соответствующих S-карточках.',
    '**Дата/фактическая проверка:** доступ источников 2026-10-23; прочитана указанная часть. '+('Предложение/вывод, продуктовый и полевой тест НЕ проводился.' if kind in ['INF','HYP'] else 'Опубликованное измерение НЕ повторялось локально.' if kind=='MEAS' else 'Статус неизвестности сохранён; неполученное содержание не подтверждено.' if kind=='UNKNOWN' else 'Наблюдение среды/метаданных, без испытания рабочего процесса.' if kind=='LOCAL-OBS' else 'Чтение не означает запуск продукта/проверку фактической практики.'),
    '',body,'', '**Продуктовый смысл/предел:** '+(CELL_MEANING[n] if n else 'Это уточняет контракт/решение в указанном контексте; применимость к ХайТэк и реальная реализация не установлены.'),'']
write('RAW_FACTS.md','\n'.join(raw))

mapout=['# Карта идентификаторов operator_product','',
'Назначение: W1 U01–U17 по номеру, затем W2 PROCESS/EXPERIENCE/CONTRACT по локальному номеру; затем именованные синтезы без прежнего F-ID. Содержание дублированных crossrefs не размножено в новые факты. Один источник может поддерживать несколько утверждений, что не создаёт независимости. Локальные S-алиасы и составные связи ниже явны. K001–K011 сохраняются. Q/E назначены сборщиком в корневых реестрах.','',
'| Local source | Final |','|---|---|']
for old,new in S_MAP.items():mapout.append(f'| `{old}` | {", ".join(new) if isinstance(new,list) else new} |')
mapout += ['','| Local fact / semantic alias | Final | Origin |','|---|---|---|']
for old in order:mapout.append(f'| `{old}` | [{F_MAP[old]}](../RAW_FACTS.md#{F_MAP[old].lower()}) | [{facts[old]["path"]}]({Path(facts[old]["path"]).relative_to("_WORK").as_posix()}) |')
mapout += ['', 'Повторные упоминания того же local ID в HANDOFF/SEARCH_LOG/K-синтезе ссылаются на ту же final запись. Не считать их новыми фактами. Историческая критика оставляет локальные ID исходной волны; эта карта восстанавливает их связь. Все 17 Uxx и все 11 W2 K прочитаны, также все шесть HANDOFF/SEARCH_LOG; большие PDF/extract не перечитывались целиком.']
write('_WORK/ID_MAP.md','\n'.join(mapout))
print(json.dumps({'sources':len(sources),'facts':len(facts),'w1_facts':sum(W1_COUNTS),'maps':len(F_MAP)},ensure_ascii=False))
