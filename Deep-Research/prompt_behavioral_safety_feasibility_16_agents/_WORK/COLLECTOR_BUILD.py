from pathlib import Path
import re, json, hashlib
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parent.parent
W=ROOT/'_WORK'
def read(name): return (W/name).read_text(encoding='utf-8-sig')
def section(name, prefix):
    text=read(name); lines=text.splitlines(); start=next(i for i,l in enumerate(lines) if l.startswith(prefix))
    level=len(lines[start])-len(lines[start].lstrip('#'))
    end=next((i for i in range(start+1,len(lines)) if re.match(r'^#{1,'+str(level)+r'} ',lines[i])),len(lines))
    return '\n'.join(lines[start:end]).strip()
records=[]
def add(title, parts, note=''):
    fid=f'F{len(records)+10:03d}'
    bodies=[]
    for name,prefix in parts:
        body=read(name) if prefix is None else section(name,prefix)
        bodies.append((name,prefix,body))
    records.append(dict(id=fid,title=title,parts=bodies,note=note))

# Consolidation is by engineering object. Repeated general smoke plans and W1
# core metadata superseded by W2 are not copied into the canonical base.
add('LinQ: актуальная публичная граница и vendor table', [('W2-01.md',None)], 'Итог второй волны; actual grant/runtime/device NOT_RUN. Таблица только text-extracted reported measurement, visual verification unavailable.')
add('LinQ: исторический guide, режимы доступа и completion proof', [('W1-13.md','## Новые первичные'),('W1-13.md','## Матрица known'),('W1-13.md','## Access decision'),('W1-13.md','### Что считается')], 'Публичный поиск обновлён F010; guide2025 не текущая ABI. Наличие VM/сервиса в кейсе не означает выдачу команде.')
add('ONNX/LinQ: adapters, operators, PTQ и структурно прочитанные smoking/SafetyVision', [('W1-14.md','## Первичные источники'),('W1-14.md','## PTQ и runtime'),('W1-14.md','## Новая бинарная')], 'YOLOX/RTMPose полные actual graphs обновлены F014. Ограничения first-output/84–85 относятся к примеру linq-cv-bench, не самому ускорителю.')
add('Производительность: определения времени, source sampling, очереди и фактическая арифметика', [('W1-15.md','## Реестр источников'),('W1-15.md','## Опубликованные'),('W1-15.md','## Метрики'),('W1-15.md','## Frame skipping'),('W1-15.md','## Очереди')], 'Ни одного нашего LinQ замера. Published vendor numbers не SLA; synthetic phase coverage не NN recall. Tracker route уточнён F034.')
add('Core: exact YOLOX nano, official pose и RTMPose; полный pre/post contract', [('W2-02.md',None)], 'Приоритетный собственный graph probe YOLOX nano. BGR recipe — documented test hypothesis, не empirical artifact-matched golden; обе исторические рецептуры и причина ambiguity сохранены.')
add('Core supply: четыре exact CC BY MP4, лицензии и per-use notices', [('W2-07.md',None)], 'Авторское copyright-основание всех четырёх MP4 установлено. Residual personality/privacy/recording scope не обнуляет CC BY и не является запретом всего research/demo. Это актуальнее неизвестной identity в W1.')
add('Падение: observable definition, pose rules и точные temporal alternatives TSSTG/PoseC3D', [('W1-01.md','## 2.'),('W1-01.md','## 3.'),('W1-01.md','## 4.'),('W1-01.md','## 7.')], 'W1 pose URL v8.2.0 не отождествлять с W2 v8.3.0 по размеру. Full hash и GPL/AGPL conflict — F014/F015. Fall readiness усилена F017; consciousness не измеряется.')
add('Падение: шесть decoded/reviewed GMDCSA clips, интервалы/видимость/hold/censoring', [('W2-03.md',None)], 'W2-03 ранний rights остаток ZIP identity для старой пары закрыт поздним F015. Четыре новых MP4 связаны по author record/revision, но не все проверены как ZIP member. Max gross-low-motion 6.432033s; H10/H30 не eligible.')
add('Падение: дополнительные datasets, exact leads, coarse CSV defects и grouping', [('W1-09.md','## 2.'),('W1-09.md','## 3.'),('W1-09.md','## 4.'),('W1-09.md','## 5.')], 'Бывшие Range-only S1F13/S1A16/S4A05 полностью получены и reviewed F017; более поздняя GT/PTS имеет приоритет. Copyright identity старой пары закрыта F015. URFD/CAUCA/IKAR и gated alternatives сохраняются как резервные источники, не полученные файлы.')
add('Бег: translation/gait, калибровка, rolling speed и locked_ids', [('W1-02.md','## Альтернативы'),('W1-02.md','## Геометрия'),('W1-02.md','## Реестр открытых'),('W1-02.md','## Артефакты')], 'Actual YOLOX graph и preprocessing ambiguity — F014. Generic speed threshold не gait-run. PoseC3D NTU60 не имеет run; HMDB51 имеет run32/walk49.')
add('Бег: CHAD route и реальные matched Weizmann samples', [('W2-05.md',None)], 'Encoded25FPS против page50FPS: PTS для replay известны, физическое capture time не установлено. Public demo права Weizmann не установлены; собственный continuous target pack ещё предложен, не записан.')
add('Moving machine: detection artifacts, geometry/TTC и rejected turnkey projects', [('W1-03.md','## Реестр первичных'),('W1-03.md','## Инженерная спецификация'),('W1-03.md','## FP/FN'),('W1-03.md','## Отказанные')], 'Actual checkpoint names0forklift1person и full SHA закрыты F022; exact exported graph всё ещё отсутствует. Generic polygon учитывается только как одна infrastructure fallback, не второй сценарий.')
add('Moving forklift: real motion/driver controls, synthetic pair и exact best.pt', [('W2-04.md',None)], 'GO internal synthetic image-space smoke; NO-GO complete public real-world route. MIT publisher index положителен, standalone HF weights scope остаётся отдельным. CC BY primary identity F015 относится к 0_te23/4_te1, не автоматически 3_te1/7_te1.')
add('Factory CCTV и industrial/synthetic data alternatives: clip semantics, права и actual availability', [('W1-10.md','## Источники'),('W1-10.md','## Минимальный набор')], 'Byte identity0_te23/4_te1 закрыта F015. NVIDIA video00238/00298 действительно получены F022, прежнее W1 not-acquired историческое. Safe label4 не all-actor negative; initial occupancy не entry.')
add('Телефон: наличие/hold/use/context, exact COCO и UPT HOI', [('W1-04.md','## Семантическая'),('W1-04.md','## Проверенные'),('W1-04.md','## Варианты'),('W1-04.md','## Состояние')], 'Phone bbox не доказывает use. UPT weight page открыта, payload/hash не получены. Device/executable phone-event test отсутствует. Числа W1 gate — предложения, не official acceptance.')
add('Action donors: AVA person labels/SlowFast, NTU phone, Smoker/HMDB', [('W1-11.md','## 2.'),('W1-11.md','## 3.')], 'AVA rows не скачанные/просмотренные movie clips; join walk14 с phone15/57 не выполнен. Numeric source IDs не переносить на head без loader. Smoker image-only, NTU access approval; licenses кода/annotations не очищают исходные фильмы.')
add('Открытое пламя: пять actual videos, XML defects, два exact weights, policy и права', [('W2-06.md',None)], 'Самостоятельный кандидат части сценария4: visible flame outside allowed ROI, не smoking. Rabahdev предпочтён по provenance readiness после binary names, не по измеренной точности/скорости. FURG CC0/FIRESENSE CC BY сохранены наряду с third-party watermark/title risk.')
add('Smoking: exact cigarette ONNX, incompatible loader, untrained-string и donor evidence', [('W1-05.md','### W1-05-S01'),('W1-05.md','### W1-05-S02'),('W1-05.md','### W1-05-S03'),('W1-05.md','### W1-05-S04'),('W1-05.md','### W1-05-S05'),('W1-05.md','### W1-05-S07'),('W1-05.md','### W1-05-S08'),('W1-05.md','### W1-05-S09'),('W1-05.md','### W1-05-S10'),('W1-05.md','## 3.')], 'Description(untrained) определяется args.data, не доказывает random/untrained weights. Full GET cigarette ONNX выполнен W1-05 в памяти; local retained binary отсутствует. MIT repo не отменяет embedded AGPL.')
add('Резервные artifacts: MeetCool, Thalos contradiction, PoseC3D HMDB и отказы', [('W1-08.md','### W1-08-S05'),('W1-08.md','### W1-08-S07'),('W1-08.md','### W1-08-S08'),('W1-08.md','### W1-08-S10')], 'MeetCool full structural scan F012 дополняет W1 tail. Thalos actual class0 literal string2, не harness; wrong filename исправлением пути не исправляет class map. PoseC3D только резерв, не causal online industrial event.')
add('Ограждение/конвейер/груз: операциональные определения, источники и geometry', [('W1-06.md','## Что именно'),('W1-06.md','## Проверенные'),('W1-06.md','## Проект правил'),('W1-06.md','## Annotation')], 'Tripwire/polygon не completed climb. Подвешенный груз вне ground plane: H пола не даёт его вертикальную проекцию. Zone fallback не засчитывается исходным сценарием5 без согласованного scope.')
add('Fence datasets: sample9 remap, exact media leads, отсутствие trained best', [('W1-11.md','## 6.')], 'Для sample9 source1climbing/source2walking, остальных source1walking/source2climbing. Нет доказанной harmonization final training set. Код/видео/веса rights отдельно unknown; generic yolov5m не custom checkpoint.')
add('Высота/привязь и дополнительная переноска: наблюдаемость, модели и нормативный scope', [('W1-07.md','## 1.'),('W1-07.md','## 2.'),('W1-07.md','## 3.'),('W1-07.md','## 4.'),('W1-07.md','## 6.')], 'SafetyVision actual graph прочитан F012, former binary unknown обновлён. Card class map остаётся card provenance; No_Harness не connection. Нормативные числа — source scope с отмеченной доступностью, не готовое локальное event rule.')
add('Height video donor и data-observability controls редких признаков', [('W1-11.md','### W1-11-S12'),('W1-11.md','## 7.')], 'Open-Site4video payload/download/grant не получены; camera-specific diagnostic size после actual resize. Нет универсального минимальногоNpx. Не обнаружено не равно verified absence.')
add('Data protocol: rights/use, actor-level GT, source grouping, freeze и event counts', [('W1-12.md','## Первичные основания'),('W1-12.md','## Формализованный протокол'),('W1-12.md','## Быстрый smoke')], 'Исторический абзац W1 о неизвестной identity старых четырёх MP4 заменяется F015. Все просмотренные файлы dev/reviewed. Proposed60–90min/gates — не результат измерения и не обязательство по сроку.')
add('Temporal/tracker/event: выбранный fixed-cadence route, TTL, ledger и matching', [('W2-08.md',None)], 'Весь adapter/ledger design NOT_IMPLEMENTED/NOT_RUN. Source inspection и малые арифметические проверки выполнены. dt1 допустим как fixed analysis step; pre-association purge нужен для строгогоTTL, не объявление framework bug. UI exactly-once ограничен сохранённой БД и keyed consumer.')
add('Reference pipelines: exact code и R3-E6 export/parity/timing reference', [('W1-16.md','## Реестр новых'),('W1-16.md','## Exact artifact'),('W1-16.md','## R5')], 'R3-E6 ready ONNX существует по HEAD, publisher SHA не local full hash. Full-tree license negative уточнён F026. R3-E6 map0Fire1Smoke противоположен rabah/farhat. Остальные R1–R4 консолидированы по объектам F016/F019/F021/F024.')

def repair_links(text):
    def repl(m):
        label,target=m.group(1),m.group(2)
        if target.startswith(('http://','https://','#','mailto:')): return m.group(0)
        if target.startswith('_WORK/'): out=target
        else: out='_WORK/'+target
        # Retain only portable links that actually resolve; plain missing locator otherwise.
        path=out.split('#')[0]
        return f'[{label}]({out})' if (ROOT/path).exists() else f'{label} (исходный локатор: `{target}`)'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',repl,text)

url_info={}
for rec in records:
    for name,prefix,body in rec['parts']:
        for m in re.finditer(r'https?://[^\s<>`\[\]"|]+',body):
            url=m.group().rstrip(').,;:—')
            if len(url)<12 or '{' in url or '/repos/{' in url: continue
            item=url_info.setdefault(url,dict(facts=[],origins=[],context=[]))
            if rec['id'] not in item['facts']: item['facts'].append(rec['id'])
            origin=f'{name}: {prefix or "полный файл"}'
            if origin not in item['origins']: item['origins'].append(origin)
            line=body[body.rfind('\n',0,m.start())+1:body.find('\n',m.end()) if '\n' in body[m.end():] else len(body)]
            if line not in item['context']: item['context'].append(line)

def owner(url):
    p=urlparse(url); seg=p.path.strip('/').split('/')
    if p.netloc in ('github.com','raw.githubusercontent.com'): return '/'.join(seg[:2])
    if p.netloc.endswith('huggingface.co'):
        if seg and seg[0] in ('datasets','api'): return 'Hugging Face publisher: '+ '/'.join(seg[:4])
        return 'Hugging Face publisher: '+ '/'.join(seg[:2])
    if 'lin-q.ru' in p.netloc: return 'LinQ / ООО «ХайТэк»'
    return {'zenodo.org':'Автор записи Zenodo; creator и DOI в factual record','data.mendeley.com':'Автор Mendeley dataset; creator в factual record','download.openmmlab.com':'OpenMMLab','www.wisdom.weizmann.ac.il':'Weizmann / authors Space-Time Actions','creativecommons.org':'Creative Commons','www.osha.gov':'OSHA','www.cdc.gov':'CDC/NIOSH'}.get(p.netloc,p.netloc)

sources=['# SOURCES — нормализованный реестр\n\nСборка: 2026-10-23, Europe/Moscow (UTC+3). Новые сетевые обращения сборщиком не выполнялись. Внешние обращения W1/W2 датированы 23.10.2026; публикация/версия отдельно в контексте записи. Один exact URL имеет один S-ID, повторные обращения не считаются независимыми источниками. Разные revisions/файлы не сливаются. Code, weights, data, video и compiled runtime имеют разные grants. В F ниже сохранены exact version/date/locator, доступность и реально выполненный тип проверки.\n', '<a id="S001"></a>\n## S001 — пользовательский официальный кейс LinQ\n\nВладелец: постановщик ООО «ХайТэк»/организаторы; тип: предоставленный первичный PDF. [Exact-byte local copy](_WORK/INPUT/КЕЙС_LinQ.pdf). 20 страниц, SHA256 `7dbece3cf414e2a09ff03c93e9e1ed87172d7724fb7edd5cd3a3ad565063689e`. Дата кейса по заданию23.10.2026; доступ23.10.2026. Публичный URL именно этого экземпляра неизвестен. Все20 raster-страниц просмотрены оркестратором; text extraction пуста. [Происхождение](_WORK/CASE_PROVENANCE.md), [визуальные notes](_WORK/CASE_ROOT_NOTES.md). Поддерживает F001/F003–F008.\n']
for i,(url,info) in enumerate(url_info.items(),2):
    sid=f'S{i:03d}'; info['sid']=sid
    immutable=re.search(r'/([a-f0-9]{40}|v\d[^/ ]*)/',url)
    version=immutable.group(1) if immutable else 'Стабильная revision в URL не установлена; конкретная версия/дата и область указаны в F/контексте. Не считать current/latest immutable.'
    context=' '.join(info['context'][:2]); context=context[:2400]
    sources.append(f'<a id="{sid}"></a>\n## {sid} — {owner(url)}\n\nПрямой URL: {url}\n\nВладелец/издатель: {owner(url)}. Тип: '+('artifact/checkpoint/media' if re.search(r'\.(onnx|pt|pth|mp4|avi|zip)(?:[/?]|$)',url) else 'первичный документ, исходный код, card/API или author page; точный тип в локаторе')+f'. Версия/дата: `{version}`. Дата доступа:2026-10-23 (ветки, не новая проверка сборщиком).\n\nЛокаторы происхождения: '+ '; '.join(info['origins'])+'. Поддерживает '+', '.join(f'[{f}](RAW_FACTS.md#{f})' for f in info['facts'])+'.\n\nКонтекст версии/наличия/прав (собственная выписка исследователей; ссылка может иметь только HEAD/metadata, а не полученный payload):\n\n'+context+'\n')
sources.append('## Важные недоступные или невыданные материалы\n\n- Текущий runbook команды, SDK/compiler/runtime matched release, catalog IDs/golden outputs, credentials и device logs: не выданы в рассмотренных входах; публичный поиск не заменяет выдачу. [F010](RAW_FACTS.md#F010), [Q001](OPEN_QUESTIONS.md#Q001).\n- Оригинальные bytes/hash и изображения performance PDF2026 не получены; text parser13pages доступен по official press link. [F010](RAW_FACTS.md#F010), [Q004](OPEN_QUESTIONS.md#Q004).\n- TSSTG upstream Drive checkpoint404 в проверке; весов, разрешённого зеркала/hash нет. UPT Drive page не full download. [F016](RAW_FACTS.md#F016), [F024](RAW_FACTS.md#F024).\n- URFD только exact pair HEAD; CAUCA exact AVI не получен; Montreal blocked; TsetFall form/key; IKAR TLS timeout; SFU/NTU/CAAR approval/restrictions. [F018](RAW_FACTS.md#F018), [F029](RAW_FACTS.md#F029).\n- CHAD огромный ZIP не получен; exact running actor/interval не установлен. Fence custom best не подтверждён; Open-Site media не получены. [F020](RAW_FACTS.md#F020), [F030](RAW_FACTS.md#F030), [F032](RAW_FACTS.md#F032).\n- YOLOX explicit standalone weight scope, forklift HF weight scope, R3-E6 grant, future SDK redistribution и residual media recording scope открыты адресно, а не объявлены отсутствующими разрешениями вообще. Четыре coreMP4 имеют доказанное CC BY4 copyright основание [F015](RAW_FACTS.md#F015).\n')
(ROOT/'SOURCES.md').write_text('\n'.join(sources),encoding='utf-8')

preface=(W/'COLLECTOR_SYNTHESIS.md').read_text(encoding='utf-8') if (W/'COLLECTOR_SYNTHESIS.md').exists() else '# RAW_FACTS — инженерная база\n\nПромежуточная сборка: canonical F010–F035 сохранены; вводный синтез дополняется.\n'
raw=[preface, '\n## Подробные канонические записи\n\nИсходные W1/W2 ID внутри выписок — provenance locators, а не новые canonical IDs. Сборщик объединяет записи по объекту; repeated core metadata/общие smoke-планы убраны там, где W2 даёт сильнейшее основание. Исторические W1 statements сохраняются с явной отметкой, что изменилось. Приоритет не «W2 всегда прав», а более точное доказательство того же exact artifact. Ссылки на later override находятся в начале каждой записи.\n']
mapping=[]
for rec in records:
    fid=rec['id']; raw.append(f'<a id="{fid}"></a>\n## {fid} — {rec["title"]}\n\n**Нормализованный статус и условия:** {rec["note"]}\n')
    sids=[inf['sid'] for inf in url_info.values() if fid in inf['facts']]
    raw.append('**Источники:** '+', '.join(f'[{s}](SOURCES.md#{s})' for s in sids)+'.\n')
    seen=set()
    for name,prefix,body in rec['parts']:
        raw.append(f'**Происхождение:** [{name}](_WORK/{name}), `{prefix or "полный файл"}`. Авторские оценки и P/NOT_RUN остаются предложениями; A/CODE — чтение/metadata, не execution.\n')
        # Remove first report title; demote headings to keep all stable F anchors top-level.
        lines=body.splitlines()
        if lines and lines[0].startswith('# '): lines=lines[1:]
        body='\n'.join('#### '+l.lstrip('#').strip() if l.startswith('#') else l for l in lines)
        paras=body.split('\n\n'); unique=[]
        for para in paras:
            key=para.strip()
            if key and key not in seen: unique.append(para); seen.add(key)
        body=repair_links('\n\n'.join(unique))
        raw.append(body+'\n')
        for bid in sorted(set(re.findall(r'W[12]-\d{2}-[SFQE]\d{2,3}',body))): mapping.append((bid,fid,name,prefix or 'full'))
(ROOT/'RAW_FACTS.md').write_text('\n'.join(raw),encoding='utf-8')
idmap=['# ID_MAP — branch IDs → canonical\n\nS-ID относятся к exactURL; F-ID — консолидированному engineering object. Одно исходное Sxx могло объединять несколько документов, поэтому mapping может быть one-to-many. Ссылка на F — область исходного наблюдения, не утверждение равенства каждой формулировки. Устаревшее состояние явно уточнено над соответствующей F.\n\n| Branch ID | Canonical F | Provenance section |\n|---|---|---|']
for bid,fid,name,prefix in sorted(set(mapping)): idmap.append(f'|{bid}|[{fid}](../RAW_FACTS.md#{fid})|{name} / {prefix}|')
idmap.append('\n## Exact URL → canonical S\n\n| Canonical S | URL |\n|---|---|')
for url,info in url_info.items(): idmap.append(f'|[{info["sid"]}](../SOURCES.md#{info["sid"]})|{url}|')
idmap.append('\n## Branch coverage\n\nВсе16W1 и8W2 входят в provenance/consolidation. Branch-local Q/E без устойчивой уникальности нормализуются тематически в OPEN_QUESTIONS; исходные K001–K011 неизменны. Итоговый handoff содержит смысловую карту.\n')
(W/'ID_MAP.md').write_text('\n'.join(idmap),encoding='utf-8')
(W/'COLLECTOR_BUILD_STATE.json').write_text(json.dumps({'status':'detailed_base_saved_synthesis_questions_pending','facts':len(records),'sources':len(url_info)+1,'raw_bytes':(ROOT/'RAW_FACTS.md').stat().st_size},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'facts':len(records),'sources':len(url_info)+1,'raw_bytes':(ROOT/'RAW_FACTS.md').stat().st_size},ensure_ascii=False))
