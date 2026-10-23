from pathlib import Path
import re, json

ROOT=Path(__file__).resolve().parent.parent
def read(p): return (ROOT/p).read_text(encoding='utf-8-sig')
def write(p,t): (ROOT/p).write_text(t.strip()+'\n',encoding='utf-8')
branches=[('W1-A','SOURCES_A','W1_A.md'),('W1-B','SOURCES_B','W1_B.md'),('C','SOURCES_C','W1_C.md'),('W2-A','SOURCES_W2A','W2_A.md'),('W2-B','SOURCES_W2B','W2_B.md'),('W2-C','SOURCES_W2C','W2_C.md')]
cards=[]
for prefix,folder,report in branches:
    data=read('_WORK/'+folder+'/EVIDENCE.md')
    matches=list(re.finditer(r'^## ('+re.escape(prefix)+r'-S\d{2})[^\n]*',data,re.M))
    for i,m in enumerate(matches):
        end=matches[i+1].start() if i+1<len(matches) else len(data)
        body=data[m.end():end].strip()
        # C's search log follows the last source card, not part of that source.
        body=re.split(r'\n## (?:Журнал|Техническое)',body)[0].strip()
        cards.append(dict(old=m.group(1),title=m.group(0).split(' — ',1)[-1],body=body,prefix=prefix,folder=folder,report=report))

# Split two branch cards that accidentally combined independent origins.
for c in list(cards):
    if c['old']=='W2-A-S07':
        a,b=c['body'].split('\n\nCN117079082A,',1)
        c['body']=a
        x=c.copy(); x.update(old='W2-A-S07-patent',title='CN117079082A — многоракурсная проверка маски',body='CN117079082A,'+b)
        cards.insert(cards.index(c)+1,x)
    if c['old']=='W2-B-S05':
        a,b=c['body'].split('\n\nPinned docs/code:',1)
        c['body']=a
        x=c.copy(); x.update(old='W2-B-S05-preprocess',title='Frigate v0.18.2 — crop → tensor preprocessing',body='Pinned docs/code:'+b)
        cards.insert(cards.index(c)+1,x)

# Same document/chain is not independent confirmation. Keep all distinct observations.
merges={'C-S02':'W1-A-S11','W2-A-S02':'W1-A-S04','W2-B-S09':'W1-B-S15','C-S20':'W2-C-S05'}
byold={c['old']:c for c in cards}
for old,dest in merges.items():
    c=byold[old]; d=byold[dest]
    d.setdefault('supplements',[]).append(c)
cards=[c for c in cards if c['old'] not in merges]
sources={}
smap={}
for i,c in enumerate(cards,1):
    sid=f'S{i:03d}'; c['id']=sid; sources[sid]=c; smap[c['old']]=sid
    for x in c.get('supplements',[]): smap[x['old']]=sid

# Stable question/experiment consolidation: these are decisions, not one entry per researcher.
qgroups=[
 ('Q001',['Q-A01','W2-A-Q02'],'Политика допустимых СИЗ и обязательные визуальные признаки'),
 ('Q002',['W2-A-Q01'],'«Снят респиратор»: состояние или наблюдённое действие'),
 ('Q003',['Q-B01','C-Q04','W2-C-Q02'],'Смысл опасной/горючей зоны, контекст и полномочия'),
 ('Q004',['Q-A02','Q-B02','C-Q03','W2-B-Q02'],'Native камеры, видимость и допустимые режимы'),
 ('Q005',['C-Q01','W2-C-Q04'],'Граница обязательного нейроинференса на LinQ'),
 ('Q006',['C-Q02'],'Назначенные LinQ hardware/SDK и точный исполняемый граф'),
 ('Q007',['Q-B03'],'Capture timestamps и реальная cadence результатов'),
 ('Q008',['Q-B04','W2-A-Q05','W2-B-Q01','C-Q05'],'Приёмка, FA/latency/unknown и знаменатели'),
 ('Q009',['W2-C-Q01'],'Контракт smoking и наблюдаемого отрицательного окна'),
 ('Q010',['Q-A03','W2-A-Q03'],'SH17 extended и фактическая семантика экспортов'),
 ('Q011',['Q-A05','W2-A-Q04'],'Industrial neck/hand/removal GT'),
 ('Q012',['Q-A04'],'Нужен ли pose/HOI для ownership на целевых сценах'),
 ('Q013',['Q-A06','Q-B05'],'Unknown, aging и best-frame policy'),
 ('Q014',['Q-B06'],'Источник activation/authorization и TTL'),
 ('Q015',['Q-B07','W2-B-Q03'],'Runtime Frigate и реальная устойчивость событий'),
 ('Q016',['Q-A07','Q-B08','C-Q08'],'Промышленная ПМИ/подписанная приёмка и полный SoW'),
 ('Q017',['Q-B09'],'ITV RegistryKeys нужной версии'),
 ('Q018',['C-Q06','W2-C-Q03'],'Fall/hook endpoint и physical GT'),
 ('Q019',[],'VLM paired benefit и допустимый путь исполнения'),
 ('Q020',['C-Q07'],'INT8 drift на нашем графе и событиях')]
qmap={old:q for q,olds,_ in qgroups for old in olds}
egroups=[('E001',['E-A01','W2-A-E01']),('E002',['E-A02']),('E003',['E-A03']),('E004',['E-A04']),('E005',['E-A05']),('E006',['E-B01']),('E007',['E-B02']),('E008',['E-B03']),('E009',['E-B04']),('E010',['E-B05']),('E011',['C-E01','W2-C-E01']),('E012',['C-E02','W2-C-E02']),('E013',['C-E03','W2-B-E01']),('E014',['C-E04','W2-C-E04']),('E015',['C-E05']),('E016',['W2-A-E02']),('E017',['W2-B-E02'])]
emap={old:e for e,olds in egroups for old in olds}
facts=[]; fmap={}
def addfact(old,title,body,sid=None,kind='DOC',origin=None):
    fid=f'F{len(facts)+1:03d}'; fmap[old]=fid
    facts.append(dict(id=fid,old=old,title=title,body=body,sid=sid,kind=kind,origin=origin))
    return fid

# Fact granularity follows individual branch observations; limitations are retained.
for c in cards:
    for sub in [c]+c.get('supplements',[]):
        prefix=sub['prefix']; body=sub['body']; sid=c['id']
        if sub['old']=='C-S20': continue # fuller W2 record supersedes partial abstract, mapped below
        # W2_C has a single F in the heading, so preserve the complete detailed record.
        if prefix=='W2-C':
            n=re.search(r'-S(\d+)',sub['old']).group(1)
            old=f'W2-C-F{n}'; kind='PUB-MEAS' if n in ['02','03','05','06','07','08'] else ('CODE' if n=='04' else ('VENDOR' if n=='09' else 'DOC'))
            addfact(old,sub['title'],body,sid,kind,sub)
            continue
        # W2-B F10–13 are in the report; source card only points to them.
        if sub['old']=='W2-B-S08':
            rep=read('_WORK/W2_B.md')
            for n in range(10,14):
                m=re.search(r'^### W2-B-F'+str(n)+r' — ([^\n]+)\n',rep,re.M)
                end=re.search(r'^### |^## |^\*\*Статус K006',rep[m.end():],re.M)
                text=rep[m.end():m.end()+end.start()] if end else rep[m.end():]
                addfact(f'W2-B-F{n:02d}',m.group(1),text,sid,'CODE',sub)
            continue
        # Capture numbered entries, including in-line identifiers and all associated limits.
        pat=re.compile(r'(?:\*\*)?('+re.escape(prefix)+r'-F\d{2})(?![–\d])(?:[^\n]*?)(?:\*\*|,|\.)(?=\s|\*)')
        ms=list(pat.finditer(body))
        if not ms:
            # Source metadata (release provenance / restricted leads) still has a source card.
            continue
        for j,m in enumerate(ms):
            end=ms[j+1].start() if j+1<len(ms) else len(body)
            text=body[m.start():end].strip()
            # Leave source-wide contextual metadata in SOURCES; include full observation/limits here.
            old=m.group(1)
            if old in fmap: continue
            kind='DOC'
            t=text.lower()
            if 'published measurement' in t or 'published comparison' in t or 'published illustrative' in t: kind='PUB-MEAS'
            elif 'code inspection' in t or 'code metadata' in t: kind='CODE'
            elif 'artifact inspection' in t or 'local visual' in t or 'local reading' in t: kind='LOCAL-OBS'
            elif 'access status' in t or 'scope/unknown' in t: kind='UNK'
            elif 'vendor claim' in t or 'author reported abstract' in t: kind='VENDOR'
            elif 'patent' in t: kind='DOC'
            if prefix=='W1-B' and int(old[-2:]) in [5,6,7,8,9,11,14,16]: kind='CODE'
            if prefix=='W1-B' and old.endswith('15'): kind='PUB-MEAS'
            addfact(old,sub['title']+' — наблюдение '+old[-2:],text,sid,kind,sub)

# Merge exact Macroscop overlap, but retain C's FPS/HD detail and source-specific constraints.
a=fmap['W1-A-F17']; b=fmap['C-F02']
af=next(f for f in facts if f['id']==a); bf=next(f for f in facts if f['id']==b)
af['body']+='\n\nДополнение того же документа (одно происхождение):\n'+bf['body']
facts.remove(bf); fmap['C-F02']=a
# Renumber once after consolidation.
for i,f in enumerate(facts,1):
    prev=f['id']; newid=f'F{i:03d}'
    for key,val in list(fmap.items()):
        if val==prev: fmap[key]=newid
    f['id']=newid
fmap['C-F20']=fmap['W2-C-F05']

def section(txt,start,end=None):
    a=txt.index(start); b=txt.index(end,a) if end else len(txt)
    return txt[a:b].strip()

# Significant project definitions/proposals have F records, but no invented S source.
repA=read('_WORK/W2_A.md')
addfact('W2-A-F12','Формальная семантика item, coverage, T/F/U и rule-result',section(repA,'### Две единицы записи','Последствие закрытия K001:'),None,'PROP')
addfact('W2-A-F13','SH17 base export не заменяет wearer/coverage GT',section(repA,'**W2-A-F13','### Два разных целевых задания'),None,'INF')
addfact('W2-A-F14','Состояние uncovered, coverage-loss и item-doffing — разные задачи',section(repA,'### Два разных целевых задания','## Минимальные следующие проверки'),None,'PROP')

repB=read('_WORK/W1_B.md')
for old,title,start,end in [
 ('B-P06','Геометрия floor zone, crossing, гистерезис и camera validity','## C06.','## C07.'),
 ('B-P07','Техника: envelope, metric proximity, activation и authorization','## C07.','## C08.'),
 ('B-P08','Трек, timestamps, low FPS и перенос атрибутов','## C08.','## C09.'),
 ('B-P09','Автомат событий, confirmation/clear/loss/cooldown','## C09.','## C10.'),
 ('B-P10','Декларативная схема, evidence и actor-aware event matching','## C10.','## E-процедуры')]:
    addfact(old,title,section(repB,start,end),None,'PROP',dict(prefix='W1-B',folder=''))

repC=read('_WORK/W1_C.md')
for n in range(21,32):
    m=re.search(r'\*\*C-F'+str(n)+r'\b',repC)
    if not m: raise ValueError(n)
    nxt=re.search(r'\*\*C-F\d+\b|^## C-E:',repC[m.end():],re.M)
    end=m.end()+nxt.start() if nxt else len(repC)
    body=repC[m.start():end]
    # Strip the superseded W1 triad; retain all other operational detail.
    body=re.sub(r'^Состояния для событий:.*?\n\n','**Исправление W2:** triad задаёт F item/coverage/T/F/U ниже; unconfirmed smoking не F, ruleF не global compliance.\n\n',body,flags=re.M|re.S)
    if n==23:
        body=body.replace('Fall-event detector должен наблюдать переход: до падения, изменение позы/положения, устойчивое последующее состояние.','Уточнение W2: fall-transition требует наблюдаемого перехода; устойчивое лежание/неподвижность — отдельный endpoint, не обязательное условие любого падения.')
    addfact(f'C-F{n}',f'Методический вывод W1 C-F{n} с учётом W2',body,None,'PROP' if n in [21,22,26,28,29] else 'INF',dict(prefix='C',folder=''))

extra=[
('P-PPE','Общий контракт наблюдаемости СИЗ и admission gate',r'''Наблюдение целевой части хранит person/track incarnation, part, source time, качество/видимость, допустимый тип и coverage T/F/U. Для каски part=head; для респиратора nose-mouth; очки=eyes; перчатки=левая/правая кисть раздельно; жилет=torso. Наличие item вне целевой части не устанавливает coverageF. Если надет другой допустимый item, spare off-body не создаёт нарушение. CoverageF требует наблюдаемого отрицательного состояния, а не missing bbox.

Предлагаемый eligibility gate проверяет native размер нужной части, разрешённый ракурс, truncation, occlusion, освещение/blur, поддерживаемый тип и owner ambiguity. Причины U: `part_not_visible`, `too_small`, `low_quality`, `owner_ambiguous`, `unsupported_type`, `inference_missing`. Невидимая pose keypoint остаётся гипотезой; confidence точки не сертификат наблюдаемости. PPE state отделён от rule applicability: unknown role/requirement не F. Цвет каски не даёт право доступа без локальной политики.

Каска: видимая голая голова против approved helmet на голове; hood/cap/hair/baldhead/reflections — hard negatives. Не доказываются внутренняя исправность, подвеска, срок службы и ремень. Если ремень обязателен, `strap_visible_closed` — отдельная задача с GT/масштабом. Респиратор: визуальный coverage и approved type, без обещания seal/fit/cartridge life. Очки: corrective vs safety, прозрачная оправа, goggles/visor и очки на лбу требуют отдельной taxonomy. Жилет: разрешённая защитная одежда/куртка, а не generic sleeveless garment. Ночной monochrome не доказывает дневной цвет/сертифицированную отражательность. Обе перчатки: C=left AND right; F на видимой голой кисти достаточно для F обеих, T на одной и U на второй дают U.

Это предложение проекта на основаниях W1-A-F12/13/15/16/17 и W2-A-F12. Оно не измерялось. Native crop выделяет существующие детали; увеличение не восстанавливает отсутствующие. Проверки E001/E003/E013, вопросы Q001/Q004/Q008.'''),
('P-ASSOC','Сравнение постановок СИЗ и отдельная проверка ownership',r'''Условный первый вариант — person+PPE detector с явной head/part association либо head-state detector при подходящем annotation unit. Direct person states полезны при ограниченных комбинациях/достаточной детали; crop multi-label масштабируется с людьми и может включать соседа/held PPE. Pose/bodypart crops полезны при реальном ownership bottleneck, но добавляют localization failures и входные crops. Learned HOI требует relation GT и export path; не default за45часов. Joint detection+pose может быть одной сетью, но это свойство конкретного artifact.

Containment personbbox — генератор кандидатов, не доказательство ношения. Сопоставлять helmet↔head one-to-one, проверять overlap/anchor и нормированную дистанцию; расстояния/пороги подбирать на calibration. При конкурирующих владельцах — U. Верхняя доля personbbox работает лишь в валидированном upright setting: leaning/crouching/lying ломают её. PPE одного человека не должно закрывать требование нескольких людей. Для респиратора связь с lower face, для gloves с двумя конкретными hands.

Hard cases: каска в руке/на столе/на поясе, поднятая при снятии рука, соседи и crossing, частичный человек/чужие ноги, hood/cap, poster/mannequin/reflection, visor поверх очков, рука с инструментом. Раздельно считать false violation от miss и false compliance от held/neighbor PPE. Сравнение на одинаковых detections/oracle boxes отделяет relation error от detector error. W1-A-F08 не является crowd ownership benchmark и не устанавливает универсального превосходства pose. E002/Q012.'''),
('P-SELECT','Свежесть, лучшие кадры и selective risk–coverage',r'''Предложение: quality gate и bounded recent window для каждого head/face/left/right crop; evidence выбирается по видимости/качеству независимо от testGT, а не максимальному violation score за весь длинный track. Старое wearing наблюдение не подтверждает current coverage после снятия. Нельзя собрать «все СИЗ надеты» из несовместимых по времени кадров. Хранить последнее достоверное значение, source timestamp и age; U не накапливает positive evidence и не даёт observed-clear. Policy pause/reset/expire требует E004/E009.

Показывать error на принятых решениях вместе с decision coverage на всем требуемом person-time, recall including abstentions и причинами U. Confidence-only, visibility+size и combined policy сравниваются на held-out camera; мягкий score не гарантирует calibrated event probability. Теория W1-A-F14 требует i.i.d. одного распределения, не переносится автоматически на соседние кадры/другой цех. E005/Q013.'''),
('P-W2CAM','Симптом среды → допустимая компенсация → abstention',section(read('_WORK/W2_B.md'),'| Симптом |','**W2-B-E01')),
('P-W2SMOKE','Условные RGB smoking routes и ограничения сравнения',section(read('_WORK/W2_C.md'),'| Маршрут |','### W2-C-E01')),
('P-W2FALL','Fall/hook: уточнённые endpoints и предел механического вывода',section(read('_WORK/W2_C.md'),'## K007:','### W2-C-E02')),
('P-W2VLM','VLM каскад: что закрыто источниками и что неизвестно',section(read('_WORK/W2_C.md'),'## K008:','### W2-C-E04')),
]
for old,title,body in extra: addfact(old,title,body,None,'PROP' if old not in ['P-W2VLM'] else 'INF')

dest={**{k:('SOURCES.md',v) for k,v in smap.items()},**{k:('RAW_FACTS.md',v) for k,v in fmap.items()},**{k:('OPEN_QUESTIONS.md',v) for k,v in qmap.items()},**{k:('OPEN_QUESTIONS.md',v) for k,v in emap.items()}}
def norm(text,ctx=None):
    # Local links move from an evidence/report directory to the root. Direct web URLs stay direct.
    if ctx:
        base=ROOT/'_WORK'/ctx['folder']
        def fixlink(m):
            target=m.group(2)
            if re.match(r'^(?:https?:|#)',target): return m.group(0)
            p=(base/target).resolve()
            try: target=p.relative_to(ROOT).as_posix()
            except ValueError: return m.group(0)
            return '['+m.group(1)+']('+target+')'
        text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',fixlink,text)
    # Convert explicit branch IDs to portable normalized links. Avoid substitutions inside URLs.
    keys=sorted(dest,key=len,reverse=True)
    pattern=r'(?<![\w/-])('+('|'.join(re.escape(k) for k in keys))+r')(?![\w-])'
    text=re.sub(pattern,lambda m:'['+dest[m.group(1)][1]+']('+dest[m.group(1)][0]+'#'+dest[m.group(1)][1].lower()+')',text)
    if ctx:
        prefix=ctx['prefix']
        def short(m):
            key=prefix+'-'+m.group(1)
            if key not in dest: return m.group(0)
            file,ident=dest[key]
            return '['+ident+']('+file+'#'+ident.lower()+')'
        # Exclude already generated anchor targets and link labels.
        text=re.sub(r'(?<![\w/\[#-])([SF]\d{2})(?![\w\]])',short,text)
    text=text.replace('E-C04','E014')
    # Local absolute service paths are not portable; none should be generated.
    return text

common='''Дата сетевых обращений и инспекции источников: **2026-10-23, Europe/Moscow (+03:00)**; интервалы волн около05:59–06:26. Это дата доступа, отдельно от публикаций/revisions. Сборка:2026-10-23 06:28 MSK; новой сети, моделей, VMS runtime, обучения и benchmark в сборке нет. Прочитаны сохранённые материалы обеих волн. Все E — предложения, **ни один E не выполнен**. Локальные metadata/XML/JSON/изображения читались в исследовательских волнах; это не запуск модели.

Легенда: **DOC** первичная документация/раскрытие метода; **CODE** исходный код прочитан, не выполнен; **PUB-MEAS** опубликованное измерение автора; **VENDOR** заявление заинтересованной стороны, включая abstract-only report; **LOCAL-OBS** инспекция сохранённого артефакта/визуальное наблюдение; **INF** наш вывод из указанных оснований; **PROP** предложение для проверки; **UNK** точное неизвестное/статус доступа. Тип основания и фактический статус проверки различаются. Чужой эксперимент не наш тест; требование не достижение. Источники одной цепочки не независимые репликации.'''

out=['# SOURCES — violation_methods',common,'''Реестр объединяет обе реальные волны. В каждой карточке сохранены автор, прямые URL, публикация/revision (либо явно неизвестно), прочитанный локатор, доступ/ограничения и поддерживаемые факты. Выписки — собственный пересказ исследователей. Дополнительная metadata и все ограничения в карточке относятся ко всем перечисленным F, если не указано иначе. Числа не превращаются в рекомендации проекта.

Одна карточка Macroscop PPE объединяет A/C. Статья и поставка SH17 связаны, но проверка двух файлов не полная инспекция. HDS abstract заменён полным W2 чтением в той же цепочке. Frigate docs/code разных модулей имеют отдельные локаторы, но одно происхождение. AWS pages, Axis pages, R2PPE paper/artifact также связаны и не являются независимыми испытаниями. Точные old→new связи: [_WORK/ID_MAP.md](_WORK/ID_MAP.md).''']
for sid,c in sources.items():
    support=[f['id'] for f in facts if f['sid']==sid]
    # C-F02 was merged into the same source's main observation.
    links=', '.join(f'[{f}](RAW_FACTS.md#{f.lower()})' for f in support) or 'metadata/статус доступа; не отдельное измерение'
    out+=['<a id="'+sid.lower()+'"></a>\n## '+sid+' — '+c['title'],
          '**Поддерживаемые F:** '+links+'. **Доступ:**2026-10-23 (+03:00). **Происхождение:** '+c['old']+'; сохранённый реестр [_WORK/'+c['folder']+'/EVIDENCE.md](_WORK/'+c['folder']+'/EVIDENCE.md).',
          norm(c['body'],c)]
    for x in c.get('supplements',[]):
        out+=['Дополнение/история чтения той же цепочки ('+x['old']+'); не независимый эксперимент:',norm(x['body'],x)]
out+=['''## Недоступное и partial-read — предел реестра

Полные статусы сохранены в карточках и журналах: [A](_WORK/SOURCES_A/SEARCH_LOG.md), [B](_WORK/SOURCES_B/SEARCH_LOG.md), [C](_WORK/SOURCES_C/EVIDENCE.md), [W2A](_WORK/SOURCES_W2A/SEARCH_LOG.md), [W2B](_WORK/SOURCES_W2B/SEARCH_LOG.md), [W2C](_WORK/SOURCES_W2C/SEARCH_LOG.md).

- ITV RegistryKeys: прочитаны metadata/оглавление, целевые VMDA таблицы не получены; `VMDA.oneAlarmPerTrack`, `LongInZoneTimeout2`, `report_frequency` только leads. Snippet defaults1/10sec/3000ms не факты.
- CHV paper полный текст429; авторский pinned README прочитан. Pictor full paper/downstream A1 tree не прочитаны; decode.py не подтверждает весь relationship алгоритм.
- N95 PPE-CLS abstract-only; FMR-DB institutional abstract-only; predecessor gas-mask Faster R-CNN restricted; данные6134/15scenes из поискового индекса не принимаются fulltext.
- Industrial alarm-recheck Guo2026: abstracts прочитаны, fulltext CNKI не получен. Публикационные числа остаются author claims без paired error audit.
- Oil India NIT и prebid получены; полный Scope of Work1786430899.pdf по извлечённому hyperlink не получен. Цитаты SoW — из официальных minutes; signed SAT/UAT/achieved protocol не получен.
- Domination1.17: §8.8 parsed primary manual прочитан; live bytes/screenshot404, локальная visual QA не состоялась; mirror1.18 — та же цепочка. Ранние W1 snippets заменены этим более сильным, но ограниченным чтением.
- ACM DOI10.1145/3511176.3511194 smoking fusion403; matched object/gesture/event benchmark не получен.
- OSHA403, MAFA403, ряд PMC recaptcha/MDPI429 и отдельные patent/model leads перечислены в журналах. Отказ конкретного инструмента не доказательство отсутствия документа. Домыслы из snippets не включены как сведения полного источника.

Сборщик не выполнял повторных сетевых запросов. Точный незакрытый остаток и дальнейший способ получения — [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).''']
write('SOURCES.md','\n\n'.join(out))

out=['# RAW_FACTS — violation_methods',common,'''## Правила чтения и приоритет уточнений

Это подробная база наблюдений, условий и предложений до литературного синтеза. Каждый F имеет явный anchor; источник/локатор и фактический доступ сохранены в S. Если поле не установлено, нельзя достроить его из названия модели или общего знания. Все факты доступны после переноса папки.

**W2 supersedes W1:** item-instance on/off-body отделён от coverage; spare off-body не нарушение при надетом другом. Unconfirmed smoking=U, а не F; F конкретного compound rule не global compliance. NOT U=U; AND Strong Kleene. Off-face state не observed removal transition. Fall не требует неподвижного лежания после каждого перехода. HDS пять status classes шире presence, но не механическая сертификация. Frigate — pinned static analysis, не воспроизведённый runtime bug. Эти правила применяются и к сохраняемым историческим выпискам W1.

Фактический источник не усиливается: bright crop/thermal/manual/DORI не универсальный RGB PPE threshold; required accuracy не achieved; no annotation не absence; LinQ family list не поддержка назначенного graph. Исходная критика сохранена в [CRITIC.md](CRITIC.md), а old→new mapping — [_WORK/ID_MAP.md](_WORK/ID_MAP.md).''',
'## Индекс фактов\n\n'+'\n'.join('- ['+f['id']+'](#'+f['id'].lower()+') — '+f['title'] for f in facts)]
for f in facts:
    out.append('<a id="'+f['id'].lower()+'"></a>\n## '+f['id']+' — '+f['title'])
    if f['sid']:
        c=sources[f['sid']]
        out.append('**Тип:** '+f['kind']+'. **Источник, locator/revision/условия чтения:** ['+f['sid']+'](SOURCES.md#'+f['sid'].lower()+'). **Дата доступа:**2026-10-23 (+03:00). **Проверено:** только документ/код/указанный артефакт в объёме карточки; модель не запускалась. **Происхождение:** '+f['old']+'.')
    else:
        out.append('**Тип:** '+f['kind']+'. **Статус:** исследовательская спецификация/вывод, не измерение и не готовая SDK-реализация. **Контекст:**2026-10-23 (+03:00); камеры/полный кейс/назначенный LinQ неизвестны. Основания и связи — в тексте; отдельный фиктивный S не создаётся. **Происхождение:** '+f['old']+'.')
    out.append(norm(f['body'],f['origin']))
    if f['old'] in ['W1-B-F06','W1-B-F07']:
        out.append('**Уточнение W2 имеет приоритет:** см. '+', '.join('['+fmap['W2-B-F'+str(n)]+'](#'+fmap['W2-B-F'+str(n)].lower()+')' for n in range(10,14))+'. Ordinary zone использует last measured box/centroid, не predicted estimate; reuse может получить новый timestamp без нового neural measurement. Статические ledgers не runtime test.')
    if f['old']=='C-F23':
        out.append('**W2 supersedes:** lying/immobility не необходимые условия любого fall-transition. См. ['+fmap['P-W2FALL']+'](#'+fmap['P-W2FALL'].lower()+').')
    if f['old'] in ['W1-A-F05','W2-A-F04']:
        out.append('**Artifact boundary:** наличие extended в статье не означает on/off/wearer в base YOLO/VOC. Два проверенных примера, не весь архив: ['+fmap['W2-A-F01']+'](#'+fmap['W2-A-F01'].lower()+'), ['+fmap['W2-A-F03']+'](#'+fmap['W2-A-F03'].lower()+'); [Q010](OPEN_QUESTIONS.md#q010).')
write('RAW_FACTS.md','\n\n'.join(out))

# Machine-readable service state feeds the subsequent question/handoff writer only.
write('_WORK/COLLECTOR_IDS.json',json.dumps(dict(smap=smap,fmap=fmap,qmap=qmap,emap=emap,source_count=len(sources),fact_count=len(facts)),ensure_ascii=False,indent=2))
mapping=['# ID_MAP — branch → общие ID','Сборка2026-10-23 (+03:00). Общие S/F/Q/E уникальны. Несколько oldID могут указывать на один объединённый факт/вопрос/эксперимент. Это не несколько независимых подтверждений. Заголовки в итоговых файлах имеют явные lowercase anchors.','| Branch ID | Общий ID | Примечание |','|---|---|---|']
for typ,mp,fn in [('S',smap,'SOURCES.md'),('F',fmap,'RAW_FACTS.md'),('Q',qmap,'OPEN_QUESTIONS.md'),('E',emap,'OPEN_QUESTIONS.md')]:
    for old,new in mp.items():
        note=''
        if old in merges: note='Одна цепочка; объединено с '+merges[old]
        if old=='C-F02': note='Числа/ограничения Macroscop объединены с W1-A-F17, без независимой репликации'
        if old=='C-F20': note='W2 fulltext supersedes W1 abstract; scope/метрики полного текста'
        if old.startswith('W2-B-S05-') or old.startswith('W2-A-S07-'): note='Разделено независимое происхождение внутри одной branch карточки'
        mapping.append('| '+old+' | ['+new+'](../'+fn+'#'+new.lower()+') | '+note+' |')
mapping+=['''## Дополнительные пояснения

- Bare `Sxx/Fxx` в исходной ветке относятся к её namespace. В нормализованном тексте точные branchIDs связаны с общими anchors; сокращённые перечисления/диапазоны в старых source notes читаются в контексте карточки, не как общие трёхзначные IDs.
- `E-C04` в критике — вариант записи `C-E04`, общий E014. W2-C-E02 содержит две связанные необязательные slices fall/hook, сохранённые вместе в E012 с раздельными endpoint/метриками.
- E003 проверяет наблюдаемость/размер по PPE; E013 camera/preprocessing workload и деградации. Их решения связаны, но не тождественны. E004 aging/best evidence и E009 общий автомат также сохранены отдельно, с общим replay набором.
- E017 — узкое воспроизведение pinned Frigate ledgers как часть выбора temporal policy E009; это не выполненный тест.
- F formal definitions/proposals не получают выдуманный S. Их основания — реальные S/F в тексте и две волны.
- K001–K008 не перенумеровываются и исходная критика не переписывается. Итоги W2 только добавлены в CRITIC.md.
''']
write('_WORK/ID_MAP.md','\n\n'.join(mapping[:3])+'\n'+'\n'.join(mapping[3:]))
print(json.dumps(dict(sources=len(sources),facts=len(facts),smap=smap,fmap=fmap),ensure_ascii=False,indent=2))
