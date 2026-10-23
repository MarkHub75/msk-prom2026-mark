from pathlib import Path
import re, json, hashlib
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / '_WORK'
files = sorted(WORK.glob('W1_[0-9][0-9].md')) + sorted(WORK.glob('W2_?.md'))
branches = {}
for p in files:
    key = p.stem.replace('_', '-')
    branches[key] = {'file': p.name, 'text': p.read_text(encoding='utf-8-sig')}

# Read every retained result in full. Preserve detailed arguments rather than
# guessing a shorter substitute; source and fact IDs below are stable in file order.
source_records = {}
source_order = []
def add_source(key, number, record):
    old = f'{key}-S{number}'
    if old not in source_records:
        source_order.append(old)
        source_records[old] = {'branch': key, 'record': record.strip()}
    elif len(record) > len(source_records[old]['record']):
        source_records[old]['record'] = record.strip()

for key, b in branches.items():
    lines = b['text'].splitlines()
    for i, line in enumerate(lines):
        # A source definition is a table's first cell, a source paragraph, or
        # a source subheading; references in prose are deliberately excluded.
        m = re.match(r'^\|\s*\**(?:'+re.escape(key)+r'-)?S(\d{2})\b', line)
        if m:
            add_source(key, m.group(1), line)
            continue
        m = re.match(r'^(?:#{2,4}\s+|(?:- )?\*\*)'+re.escape(key)+r'-S(\d{2})\b', line)
        if m:
            end = i+1
            if line.startswith('#'):
                while end < len(lines) and not re.match(r'^#{1,3}\s', lines[end]): end += 1
            else:
                while end < len(lines) and lines[end].strip() and not re.match(r'^(?:- )?\*\*'+re.escape(key)+r'-S\d{2}\b',lines[end]): end += 1
            add_source(key, m.group(1), '\n'.join(lines[i:end]))

# Explicit inherited locators: these records refer to the same pinned trainer
# or to exact HEAD URLs already stated in their branch, not newly fetched URLs.
source_records['W2-A-S02']['record'] += '\nURL того же source: https://github.com/ultralytics/ultralytics/blob/de290d865035acbfa4bb24cc88960d8b52c26e45/ultralytics/engine/trainer.py . Locator L768–837,909–920,1005–1022,1071–1145.'
source_records['W2-C-S15']['record'] += '\nТочные HEAD URL: https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26s.pt ; https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_coco.pth ; https://huggingface.co/Peterande/D-FINE/resolve/19214e91f5ce4c1e609022c38b1fc953c47404e7/dfine_m_coco.pth ; https://github.com/Peterande/storage/releases/download/dfinev1.0/dfine_m_obj2coco.pth ; https://github.com/Peterande/storage/releases/download/dfinev1.0/PPHGNetV2_B2_stage1.pth ; https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.pth .'

source_map = {old: f'S{i+4:03}' for i,old in enumerate(source_order)}
source_map.update({'LOCAL-CASE':'S001','LOCAL-CONTEXT':'S002','LOCAL-PROCESS':'S003'})
local_fact_map = {}
sections = []
source_section = re.compile(r'(Реестр.*(?:источ|свидетел|доказатель)|Журнал доказательств|Первичн.*(?:evidence|доказательн|свидетел)|Дополнительные проверенные локаторы)',re.I)
for key,b in branches.items():
    chunks = re.split(r'(?m)^## ', b['text'])
    b['preamble'] = chunks[0]
    for chunk in chunks[1:]:
        title,_,body=chunk.partition('\n')
        if source_section.search(title) and not re.search(re.escape(key)+r'-F\d{2}',body):
            continue
        fid = f'F{len(sections)+21:03}'
        local_ids = sorted(set(re.findall(re.escape(key)+r'-F\d{2}', body)))
        for old in local_ids: local_fact_map.setdefault(old,fid)
        sections.append({'id':fid,'branch':key,'title':title.strip(),'body':body.strip(),'locals':local_ids})

def normalize(text, key):
    # Full branch IDs first; same-branch S shorthand only inside brackets or
    # source labels. Keep original local IDs alongside normalized IDs in ID_MAP.
    for old,new in sorted(source_map.items(), key=lambda x:-len(x[0])):
        text = re.sub(r'(?<![A-Za-z0-9-])'+re.escape(old)+r'(?!\d)',new,text)
    for old,new in sorted(local_fact_map.items(), key=lambda x:-len(x[0])):
        text = re.sub(r'(?<![A-Za-z0-9-])'+re.escape(old)+r'(?!\d)',new,text)
    def short(m):
        num=m.group(1)
        return source_map.get(f'{key}-S{num}',m.group(0))
    text = re.sub(r'(?<![\w-])S(\d{2})(?!\d)', short,text)
    text = text.replace('](../CRITIC.md)','](CRITIC.md)')
    # Branch files live one level below final evidence files.
    text = re.sub(r'\]\((W[12][_-][^):\s]+)\)',r'](_WORK/\1)',text)
    text = text.replace('`D:\\...`','`WINDOWS_DRIVE:\\...`')
    return text

for sec in sections:
    sec['body'] = normalize(sec['body'],sec['branch'])
    sec['sources'] = sorted(set(re.findall(r'\bS\d{3}\b',sec['body'])))

def refs(key):
    return ', '.join(s['id'] for s in sections if s['branch']==key)

src = ['# SOURCES — cv_accuracy_vast\n',
'''Реестр собран только из сохранённых результатов 16 веток W1 и 7 веток W2. Нового интернет-поиска сборщик не делал. Дата доступа сетевых свидетельств — **2026-10-23**; точное время, если известно, указано в карточке/исходном branch. Дата публикации, release, commit и Last-Modified отделены от доступа. Если дата или версия не названа в карточке, значение — **unknown**; «live» не является версией. Полный source SHA, tag, опубликованный digest и вычисленный digest полученных байтов — разные поля. Карточки сохраняют эту границу.

S-ID обозначает конкретное чтение/набор тесно связанных первичных локаторов внутри branch. Повтор одного URL в разных ветках сохранён отдельным evidence record: это позволяет не смешивать разные версии, состав прочитанного и происхождение. Несколько URL внутри одной карточки перечислены явно, их отдельные роли описаны в locator. Автор и название приводятся в сохранённой карточке; если они там не установлены — **unknown**, а не угаданы по домену. Нет оснований автоматически называть первичным содержимое issue пользователя, соседний отчёт или выполненным тестом API/docs.

F-связи ниже — точные ссылки из соответствующих записей плюс branch-level контекст. Исходные определения всех source-ID сохранены; подробное обратное соответствие — [_WORK/ID_MAP.md](_WORK/ID_MAP.md). Методологические выводы и предлагаемые процедуры не являются опубликованными результатами источников.
''',
'''## S001 — Официальный кейс LinQ, визуальные наблюдения root

- Автор/издатель: ООО «ХайТэк» / организаторы «Открой#Моспром» 2026. Название: «КЕЙС_LinQ.pdf»; явная версия файла/дата публикации внутри просмотренного документа **unknown**. Контекст выдачи — 23.10.2026, это отдельное сообщение задания.
- URL официальной страницы соревнования: https://hackathon2026.otkroimosprom.ru/ . Публичный direct URL точных PDF bytes **unknown**. Локальный первоисточник находился в соседнем исследовании; сохранённая переносимая provenance: [_WORK/CASE_NOTES.md](_WORK/CASE_NOTES.md).
- Доступ/визуальное чтение: 2026-10-23, все 20 raster pages, отдельно читаемые p5/7/13. PDF size 8,320,969 bytes; SHA256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`. Root дополнительно локально сверил CASE_PROVENANCE и exact-byte INPUT copy: hash совпал с original, пять sheets созданы из этого PDF. Это локальное input/provenance observation, не новая сеть. Сборщик не выполнял повторный просмотр PDF.
- Locator: pp5,7,8,9,12,13,15,18,19. Тип: прямое визуальное наблюдение root, переданное в локальной записи; не OCR и не новый runtime test.
- F-связи: F001–F004, F008, F013, F017.

## S002 — Исходный договор и тематическое поручение

- Автор: пользователь / исследовательская программа команды. Названия: [Context-prompt.md](Context-prompt.md), [prompt_cv_accuracy_vast_research.md](prompt_cv_accuracy_vast_research.md). Версия общего договора `mosprom-research-v1`; точная дата редакции файлов unknown. URL: не опубликован, локальные первичные инструкции.
- Доступ: 2026-10-23. Locator: тематические §§0–3,8–11 и общий контекст §§2–6. Тип: заданный контекст, полномочия и team reports; не hardware inventory и не официальная scoring formula.
- F-связи: F002–F004, F017–F020.

## S003 — Журнал фактически выполненного исследования

- Автор: root и самостоятельные исследовательские ветки. Источник: [_WORK/RUN_STATE.md](_WORK/RUN_STATE.md), [_WORK/W2_RESOLUTION_MAP.md](_WORK/W2_RESOLUTION_MAP.md), [CRITIC.md](CRITIC.md) и сохранённые ветки. URL: локальные рабочие свидетельства, не публичные источники.
- Версия/дата: запуск с 2026-10-23T19:36:01+03:00; W2 закончена 20:50:48+03:00; collector начат 20:51:04+03:00. Доступ сборщика: 2026-10-23. Locator: хронология W1→critic→W2; K001–K011.
- Тип: процессная provenance. Фактические действия: сетевое read-only чтение primary code/docs/metadata; public offers; малый URFD CSV; release CLI wheel bytes и статическое сравнение. Не было model training/export/benchmark/GPU rental/LinQ execution.
- F-связи: F002, F010–F013, F017–F020; все branch sections ниже.
''']

for old in source_order:
    r=source_records[old]; sid=source_map[old]; key=r['branch']
    record=normalize(r['record'],key)
    urls=list(dict.fromkeys(re.findall(r'https?://[^\s<>\]\)\|]+',record)))
    linked=[s['id'] for s in sections if sid in s['sources']]
    if not linked: linked=[s['id'] for s in sections if s['branch']==key]
    # Keep original detailed card, including attribution, exact section and caveat.
    labels=re.findall(r'\[([^\]]+)\]\(https?://',record)
    title=labels[0] if labels else old+' / локальное свидетельство'
    if old=='W1-10-S09': title='CASE_NOTES — root visual observations'
    revisions=list(dict.fromkeys(re.findall(r'\b[0-9a-f]{40}\b|\bv?\d+\.\d+\.\d+(?:[\w.-]*)?',record)))
    src.extend([f'## {sid} — {title} ({old})\n',
        f'- Provenance: [{key}](_WORK/{branches[key]["file"]}); исходная карточка `{old}`. Доступ: **2026-10-23**.\n',
        '- Автор/организация: атрибуция в сохранённой карточке ниже; если явно не названа — **unknown**. Название и точный locator: карточка ниже.\n',
        '- Версия/commit/tag: '+(', '.join('`'+v+'`' for v in revisions) if revisions else '**unknown / live undated**, если карточка не устанавливает иной идентификатор')+'. Дата публикации/revision: только явно установленная в карточке, иначе **unknown**; не дата доступа.\n',
        '- Тип основания: primary code/docs/paper/metadata либо локальное наблюдение, точный тип и предел приведены в карточке. Ни source version, ни авторский benchmark не installed/tested target runtime.\n',
        '- URL: '+('; '.join(f'<{u}>' for u in urls) if urls else '**unknown / локальная provenance, см. карточку**')+'.\n',
        '- F-связи: '+', '.join(linked)+'.\n\n', record+'\n\n'])
(ROOT/'SOURCES.md').write_text('\n'.join(src),encoding='utf-8')

# Persist machine-readable assembly index for reproducible author navigation.
index={'sources':source_map,'facts':local_fact_map,'sections':[{k:v for k,v in s.items() if k!='body'} for s in sections],
       'branch_inputs':{k:{'file':v['file'],'sha256':hashlib.sha256(v['text'].encode()).hexdigest(),'chars_read':len(v['text'])} for k,v in branches.items()}}
(WORK/'COLLECTOR_INDEX.json').write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')

raw_head=normalize((WORK/'COLLECTOR_INTEGRATED.md').read_text(encoding='utf-8'),'LOCAL')
raw=[raw_head,'\n# Подробный каталог сохранённых наблюдений, выводов и процедур\n',
'''Следующие F-записи сохраняют содержательную детализацию обеих волн. Это нормализованные секции базы с полными исходными условиями, а не новый независимый эксперимент сборщика. Локальные F-ID внутри секции могут ссылаться на один глобальный F-ID: единицей хранения выбран смысловой блок, а не каждое предложение. Все local→global соответствия находятся в ID_MAP.

Для каждого блока действует обязательная шкала: **DOC/static** — прочитанный код/docs/metadata; **PUBLISHED** — численный результат авторов с их условиями; **OBSERVED** — реально полученный HTTP/малый artifact и его локальная проверка; **INFERRED/PROPOSED** — наш вывод/будущая процедура; **UNRUN** — не исполнено. Точные типы уточняются внутри записи. Ни одна запись не даёт собственных target accuracy/VRAM/throughput/latency/RPO: они unknown. Предлагаемые команды и эксперименты не исполнялись.

При конфликте W1 и W2 применимость устанавливается F005–F014 и W2 записью: выбранный source-backed envelope заменяет candidate latest image как рабочее предложение; actual wheel заменяет legacy CLI claim; ResNet50 worked sample отделён от yolo5s tested-name; O365 lineage YOLO26 и точный grant D-FINE HF уточнены. Исходная история W1 остаётся доступна, но не является активным runbook. Все экспериментальные разделы ниже — библиотека для последующих решений, **не очередь обязательных запусков**; активная очередь только F003/F017.
''']

for s in sections:
    key=s['branch']; warnings=[]
    if key in ['W1-02','W1-06']: warnings.append('Detector priority/provenance/recipe уточнены W2-B/C: нет target ranking; YOLO26 не COCO-only; YOLOX weight grant unresolved.')
    if key=='W1-06': warnings.append('Предарендная circular wording заменена F003/F017: до rental документальные/data/local CPU checks, затем отдельно разрешённая оплачиваемая qualification actual3090; heavy training только после неё. Freeze/unfreeze не второй обязательный B.')
    if key in ['W1-09','W1-11']: warnings.append('Различающиеся split схемы являются альтернативами; принят единый F004. SELECT не используется для настройки knob и затем подтверждения.')
    if key in ['W1-13','W1-14']: warnings.append('Активный минимум F010/F012: native pre-strip copy+external receipt; сложный controller/exact replay deferred. shell=True относится к legacy vast.py, не выбранному wheel. Stock OOM/NaN/save mutations учтены W2-A.')
    if key=='W1-13': warnings.append('W1 image torch2.14.1/digest сохраняется только как metadata candidate; активное предложение env выбрано F007/W2-B (2.5.1/0.20.1), а не готовая общая recipe этого образа. Старые legacy/local:C copy примеры не команды выбранного wheel; актуальный будущий runbook F012/W2-G.')
    if key=='W2-B': warnings.append('После W2-C активный источник условного D-FINE-M — exact pinned HF COCO artifact F005/F006 с model-level designation; native GitHub URL этого manifest сохранён как авторская provenance, byte identity GitHub/HF не доказана. Все env/adapter поля остаются UNRUN.')
    if key=='W1-16': warnings.append('W2-F уточняет: manual worked ResNet50 classification; yolo5s только tested-name, exact detection fallback не установлен.')
    if key=='W1-12': warnings.append('Цены — только снимок 20:04:35–37 MSK; W2-G уточняет actual wheel и current-current loading billing conflict; будущая цена/счёт unknown.')
    if key in ['W1-03','W1-04','W1-05','W1-08','W1-10','W1-15']: warnings.append('Эта ветка — исследовательский каталог условных альтернатив. Не расширяет активный A/B/C route; дополнительные neural nodes/development runs deferred без наблюдённой причины и gate.')
    raw.extend([f'## {s["id"]} — {key}: {s["title"]}\n',
       f'- Происхождение/locator: [{key}](_WORK/{branches[key]["file"]}), раздел «{s["title"]}»; прочитанный snapshot 2026-10-23.\n',
       '- Основание: сохранённая documentary/аналитическая запись branch; конкретные наблюдения, published числа и предлагаемые решения разделены в деталях.\n',
       '- Источники: '+(', '.join(s['sources']) if s['sources'] else 'source registry этого branch и локальный S001/S002; для вывода без отдельного locator основание — авторский синтез, не самостоятельный external fact')+'.\n',
       '- Фактическая проверка: только документальное чтение/metadata, если ниже не назван конкретный полученный малый artifact; model/train/export/3090/LinQ и предлагаемые acceptance tests — **UNRUN**.\n',
       '- Версия, условия, границы и противоречия: сохранены в деталях ниже; неустановленные значения **unknown**.\n'])
    if warnings: raw.append('- Применимость после интеграции: '+' '.join(warnings)+'\n')
    raw.append('\n'+s['body']+'\n\n')
(ROOT/'RAW_FACTS.md').write_text('\n'.join(raw),encoding='utf-8')

imap=['# ID_MAP — стабильное соответствие branch→S/F/E/Q\n',
      'Сборка только из сохранённых материалов; все 23 result-файла прочитаны скриптом полностью, без обрезки вывода. SHA входов и размеры чтения — `COLLECTOR_INDEX.json`. Подробные секции сохраняют исходное содержание; короткие авторские решения F001–F020 находятся впереди RAW_FACTS.\n',
      '## Источники\n\n| Branch ID | Global ID | Provenance |\n|---|---|---|']
for old in source_order: imap.append(f'| {old} | {source_map[old]} | _WORK/{branches[source_records[old]["branch"]]["file"]} |')
imap.append('\n## Явные исходные F-ID\n\n| Branch ID | Global block |\n|---|---|')
for old,new in sorted(local_fact_map.items()): imap.append(f'| {old} | {new} |')
imap.append('\n## Полный section index (включая факты без исходного F-ID)\n\n| Branch | F | Раздел |\n|---|---|---|')
for s in sections: imap.append(f'| {s["branch"]} | {s["id"]} | {s["title"].replace("|","/")} |')
imap.append('''\n## Эксперименты и вопросы

| Branch experiment / вопрос | Global E / Q | Активность |
|---|---|---|
| W1-01 E1, W1-04 E04, W1-09 calibration/FSM, W2-D E01 | E001/E002; Q001–Q005 | Минимальные logic/oracle/causal development проверки; всё UNRUN |
| W1-02 detector E, W1-06 FT, W2-C spatial E | E006/E007; Q008/Q009 | Один FT только route B; challenger только C |
| W1-03 pose E | E010; Q017 | Deferred |
| W1-05 tracker E | E009; Q017 | Только после observed ID/event errors |
| W1-07 selection/annotation E, W1-08 augmentation E | E008; Q008/Q009 | Одна обусловленная ошибкой переменная, без обязательного sweep |
| W1-10 cascade/KD E, W2-E verifier E | E011; Q010/Q017 | Deferred; не обязательный MVP |
| W1-11 selection/ASHA E | E007; Q009 | Manual bounded queue; ASHA deferred |
| W1-12 cost, W1-15 1vs2 E | E012; Q013–Q016 | Одна GPU default, вторая только после измерения |
| W1-13/14 recovery E, W2-A negative drill, W2-G integrity E | E004/E005; Q011/Q012/Q015 | Минимальный native+receipt; exact replay deferred |
| W1-16 E16, W2-B stack E, W2-F P0–P8 | E003/E004; Q006/Q007/Q018–Q021 | Обязательные target gates, UNRUN |
| W2-G Q-G01 loading / Q-G02 units / Q-G03 state / Q-G04 payments / Q-G05 closure | Q015 / Q014–Q015 / Q015 / Q013 / Q012–Q016 | Исходные вопросные метки сохранены в подробном материале как provenance; final Q-ID находятся в OPEN_QUESTIONS |
''')
(WORK/'ID_MAP.md').write_text('\n'.join(imap),encoding='utf-8')
print(json.dumps({'branches':len(branches),'source_records':len(source_order),'sections':len(sections),'explicit_local_facts':len(local_fact_map)},ensure_ascii=False))
