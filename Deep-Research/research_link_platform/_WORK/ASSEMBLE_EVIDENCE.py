from pathlib import Path
import re, json, html
from urllib.parse import urlsplit, urlunsplit, unquote

ROOT=Path(__file__).resolve().parent.parent
WORK=ROOT/'_WORK'
FILES=sorted(WORK.glob('W1_*_RESULT.md'))+sorted(WORK.glob('W2_?_RESULT.md'))
URL=re.compile(r'https?://[^\s<>|`)]+')
SID=re.compile(r'(?:(W[12]-[0-9A-Z]{1,2})-)?S(\d{1,2})(?!\d)')
FID=re.compile(r'(?:(W[12]-[0-9A-Z]{1,2})-)?F(\d{1,2})(?!\d)')

def urls(s):
    found=[]
    for u in URL.findall(s):
        u=html.unescape(u).rstrip('.,;。')
        while u.endswith(')') and u.count(')')>u.count('('): u=u[:-1]
        u=u.rstrip(']')
        if u not in found: found.append(u)
    return found

def canon(u):
    p=urlsplit(u); path=unquote(p.path)
    if p.netloc.lower() in ('lin-q.ru','ivacv.ru') and path!='/' and not path.lower().endswith('.pdf'): path=path.rstrip('/')
    return urlunsplit((p.scheme.lower(),p.netloc.lower(),path,p.query,''))

def branch(f): return f.stem.replace('_RESULT','').replace('_','-')
def link(kind,id):
    name={"S":"SOURCES.md","F":"RAW_FACTS.md","Q":"OPEN_QUESTIONS.md"}[kind]
    return f'[{id}]({name}#{id.lower()})'

sources=[]; byurl={}; source_alias={}; texts={}; definitions={}
for f in FILES:
    b=branch(f); t=f.read_text(encoding='utf-8-sig'); texts[b]=t
    lines=t.splitlines(); found=[]; source_section=False
    # Only definition-style rows/paragraphs, never an inline citation in a fact.
    for i,line in enumerate(lines):
        if re.match(r'^#{2,3} ',line):
            if 'источник' in line.lower() or 'sources with' in line.lower(): source_section=True
            elif line.startswith('## '):source_section=False
        if not source_section:continue
        m=re.match(r'^\s*(?:\|\s*|[-*]\s+)?(?:\*\*)?((?:W[12]-[0-9A-Z]{1,2}-)?S\d{1,2})(?:\*\*)?[.:|\s]',line)
        if not m: continue
        sid=m.group(1); local=sid if sid.startswith('W') else b+'-'+sid
        rec=line
        if not line.lstrip().startswith('|'):
            j=i+1
            while j<len(lines) and lines[j].strip() and not re.match(r'^\s*(?:[-*]\s+)?(?:\*\*)?(?:W[12]-[0-9A-Z]{1,2}-)?S\d',lines[j]):
                rec+='\n'+lines[j];j+=1
        if local not in [x[0] for x in found]: found.append((local,rec))
    for local,rec in found:
        us=urls(rec)
        if not us:
            inherited=re.findall(r'(?<![-\w])S(\d{1,2})(?!\d)',rec.split(local.split('-')[-1],1)[-1])
            for no in inherited:
                alias=b+'-S'+no
                if alias in definitions:
                    us.extend(urls(definitions[alias]))
                    if us:break
        if not us:
            us=['local://'+b+'/'+local.rsplit('-',1)[-1]]
        ids=[]
        for u in us:
            key=canon(u) if not u.startswith('local:') else u
            if key not in byurl:
                sid=f'S{len(sources)+1:03d}'; byurl[key]=sid
                sources.append({'id':sid,'url':u,'canonical':key,'records':[],'aliases':[],'facts':[]})
            sid=byurl[key]; obj=sources[int(sid[1:])-1]
            obj['records'].append({'branch':b,'local':local,'text':rec,'file':f.name})
            if local not in obj['aliases']:obj['aliases'].append(local)
            ids.append(sid)
        source_alias[local]=list(dict.fromkeys(ids));definitions[local]=rec

facts=[];fact_alias={}; matrix_units=[]
for f in FILES:
    b=branch(f);t=texts[b];lines=t.splitlines(); starts=[]
    for i,line in enumerate(lines):
        m=re.match(r'^\s*(?:#{1,4}\s+|[-*]\s+|\|\s*)?(?:\*\*)?((?:W[12]-[0-9A-Z]{1,2}-)?F\d{1,2})(?!\d)',line)
        if m: starts.append((i,m.group(1)))
    for n,(i,token) in enumerate(starts):
        local=token if token.startswith('W') else b+'-'+token
        if local in fact_alias: continue
        line=lines[i]
        if line.lstrip().startswith('|'):
            end=i+1
        elif line.lstrip().startswith('- ') and not line.lstrip().startswith('- **'):
            end=starts[n+1][0] if n+1<len(starts) else len(lines)
            for j in range(i+1,end):
                if re.match(r'^#{1,3}\s+',lines[j]):end=j;break
        else:
            end=starts[n+1][0] if n+1<len(starts) else len(lines)
            for j in range(i+1,end):
                if re.match(r'^##\s+',lines[j]):end=j;break
        body='\n'.join(lines[i:end]).strip()
        if line.lstrip().startswith('|'):
            h=i-1
            while h>=0 and lines[h].lstrip().startswith('|'):h-=1
            block=lines[h+1:i]
            if len(block)>=2:body=block[0]+'\n'+block[1]+'\n'+line
        # A fact ends before source/experiment or editorial sections at same depth.
        fid=f'F{len(facts)+1:03d}';fact_alias[local]=fid
        refs=[]
        for sm in SID.finditer(body):
            alias=(sm.group(1) or b)+'-S'+sm.group(2)
            refs.extend(source_alias.get(alias,[]))
        if not refs:
            refs=[x for a,ids in source_alias.items() if a.startswith(b+'-') for x in ids]
        refs=list(dict.fromkeys(refs))
        facts.append({'id':fid,'local':local,'branch':b,'file':f.name,'line':i+1,'body':body,'sources':refs,'kind':'fact'})
    # Preserve detailed matrices/protocols omitted from individual fact cards.
    for m in re.finditer(r'(?m)^## (.+)\n',t):
        name=m.group(1);st=m.end(); nxt=re.search(r'(?m)^## ',t[st:]);en=st+nxt.start() if nxt else len(t)
        content=t[st:en].strip()
        keep=any(x in name.lower() for x in ('матриц','сопоставление продуктов','карта доступности','карта объектов','хронология','измерен','сравнение','отделение машин','диагностические сообщения','таблица конфликтов','mapping:','three-path manifest','component/version','versioned api','version/evidence','symptom','численн','confirmed versus','queue/timestamp','staged evaluation','спецификация adapter','источники с рабоч'))
        if keep and not ('факты' in name.lower() or 'источники' in name.lower()):
            fid=f'F{len(facts)+1:03d}'
            refs=[]
            for sm in SID.finditer(content): refs.extend(source_alias.get((sm.group(1) or b)+'-S'+sm.group(2),[]))
            if not refs:refs=[x for a,ids in source_alias.items() if a.startswith(b+'-') for x in ids]
            facts.append({'id':fid,'local':b+'-MATRIX-'+str(len(matrix_units)+1),'branch':b,'file':f.name,'line':t[:m.start()].count('\n')+1,'body':'### '+name+'\n\n'+content,'sources':list(dict.fromkeys(refs)),'kind':'matrix'})
            matrix_units.append(fid)

def replace_refs(body,b):
    def source(m):
        alias=(m.group(1) or b)+'-S'+m.group(2)
        ids=source_alias.get(alias)
        return ', '.join(link('S',s) for s in ids) if ids else m.group(0)
    def fact(m):
        alias=(m.group(1) or b)+'-F'+m.group(2);id=fact_alias.get(alias)
        return link('F',id) if id else m.group(0)
    # URLs and code must remain exact; resolve prose refs outside code spans/fences only.
    out=[];in_fence=False
    for line in body.splitlines():
        if line.startswith('```'):in_fence=not in_fence;out.append(line);continue
        if not in_fence:
            chunks=re.split(r'(`[^`]*`)',line)
            line=''.join(c if c.startswith('`') else FID.sub(fact,SID.sub(source,c)) for c in chunks)
        out.append(line)
    return '\n'.join(out)

def status(f):
    b=f['branch'];local=f['local'];n=int(local.rsplit('F',1)[-1]) if re.search(r'-F\d+$',local) else 0
    if b=='W2-E' and f['kind']=='matrix':return 'source_code + local_observation + unknown','mixed per cell: actual public ONNX bytes,13conv comparison, ORT1.31.0 CPU b1 success/b2 failure; vendor.tpu/strict export/LinQ not run'
    if b=='W2-L' and f['kind']=='matrix':return 'engineering_recommendation grounded in primary documentation','conditional routes/our queue contract; not an executed access route or a vendor capability claim'
    if b=='W2-F' and f['kind']=='matrix':return 'engineering_recommendation grounded in primary documentation','planned staged evaluation; no SDK calibration/compile/device run'
    if b=='W2-E' and n in (2,3,4,5):return 'local_observation + source_code','binary/weights inspection; F05: actual ONNX Runtime 1.31.0 CPU b1/b2 + diagnostic raw-head derivative; no LinQ'
    if (b=='W2-G' and n in (5,6,7)) or (b=='W2-D' and n==7):return 'source_code + local_helper_test','actual host helper/mock execution; no native SDK/device; limits in record'
    if b=='W1-10' and n in (2,4,6):return 'source_code + local_helper_test','actual isolated helper/formula/AST probe: _WORK/W1_10/CONTRACT_PROBES_RESULT.json; NumPy2.4.2; no OpenCV pixel resize, SDK or device execution'
    if (b=='W1-15' and n==5):return 'source_code + local_helper_test','actual isolated listing-expression mock: _WORK/W1_15/STATIC_SOURCE_CHECK.json; no native load or hardware'
    if (b=='W1-12' and n==11) or (b=='W1-14' and n==6):return 'source_code + local_helper_test','actual AST/argparse.Namespace identifier check; no full runner/SDK/device'
    if (b=='W1-09' and n==10) or (b=='W1-08' and n==6) or (b=='W1-11' and n==6):return 'source_code + local_helper_test','actual AST/isolated helper check; no full runner/model/device execution'
    if b=='W2-B' and n<=4:return 'network_observation / reported_remote_observation','retrieval/tool outcomes only; no PDF image inspected'
    s=f['body'].lower()
    kinds=[]
    for k in ['primary_documentation','vendor_statement','vendor_claim','reported_measurement','source_code','primary_metadata','local_observation','unknown','historical_documentation','engineering_inference']:
        if k in s:kinds.append(k)
    if not kinds:
        if b in ('W1-05','W1-04','W1-03','W1-02','W1-01'):kinds=['primary_documentation / vendor_statement; see record']
        else:kinds=['source_code / primary_documentation; see record']
    return ' + '.join(kinds),'read_source_or_document; local archive/hash/metadata inspection where specified; no neural-model execution in this record, no proprietary SDK compile/LinQ run'

meta={'sources':sources,'source_alias':source_alias,'facts':facts,'fact_alias':fact_alias,'matrix_units':matrix_units}
(WORK/'ASSEMBLY_DATA.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')

for f in facts:
    for sid in f['sources']: sources[int(sid[1:])-1]['facts'].append(f['id'])

src=['# SOURCES — LinQ platform\n','Дата доказательств: 2026-10-23, 04:15–05:14 Europe/Moscow (01:15–02:14 UTC). Сборка читает сохранённые материалы обеих волн, без нового внешнего поиска. Исторический контекст подготовки — ночь23.10.2026. S-ID обозначает первичный URL/версию либо локальный протокол; несколько извлечений одного URL — одна provenance lineage. Стабильные ссылки: `#s001`. Даты документа и доступа разделены в карточках.\n','Общий статус: публичные документы и открытые source/artifact bytes получены выборочно. Закрытая поставка SDK, современная native library/driver и LinQ не получены в исследовании; исход пользовательского signup не сообщён. Реальные CPU ONNX-пробы перечислены отдельно в RAW_FACTS, это не LinQ execution. PDF text extraction не повышен до визуального чтения.\n']
for s in sources:
    u=s['url'];p=urlsplit(u);domain=p.netloc;path=p.path
    local=u.startswith('local:')
    title=path.rsplit('/',1)[-1] or domain
    if domain in ('lin-q.ru','files.lin-q.ru'):author='ООО «ХайТэк» / LinQ';kind='первичный источник изготовителя: документация/заявление, по содержанию карточки'
    elif domain in ('github.com','api.github.com','raw.githubusercontent.com'):
        author='Владелец репозитория и авторы файла по URL/сохранённой карточке';kind='первичный код/метаданные автора; принадлежность LinQ vendor не предполагается'
    elif domain.endswith('pythonhosted.org') or domain=='pypi.org':author='Publisher/author package metadata в карточках';kind='первичный опубликованный package artifact/metadata; native runtime не подразумевается'
    elif domain=='ivacv.ru':author='IVA CV / «Когнитив Солюшнс» (для старого guide «ИВА Когнитив»)';kind='первичная документация/заявление интегратора'
    elif local:author='Исследователь соответствующей ветки';kind='наш сохранённый протокол/производная выписка; не независимый upstream'
    else:author='Точный автор/организация в исходной карточке ниже, если установлены';kind='первичный по указанной ниже области либо discovery-only; не аппаратная проверка'
    date='не установлена; точные установленные версии/даты в provenance ниже'
    if 'Framework_manual_H1' in u:title='Фреймворк IVA H1. Руководство оператора';date='2025; RU.РМДВ.04.06.014-03 34 01'
    if '2026_linq_presentation' in u:title='Российские решения для аппаратного ускорения работы нейронных сетей';date='2026; точный день выпуска не установлен'
    if local:title=s['aliases'][0]+' — локальный протокол/производная source-выписка'
    locator='Локальные файлы и точные разделы ниже; внешний URL не применяется' if local else f'[{u}]({u})'
    src+=['<a id="'+s['id'].lower()+'"></a>\n',f'## {s["id"]} — {title}\n',f'- Прямой URL/локатор: {locator}\n',f'- Автор/primary relation: {author}; {kind}.\n',f'- Дата документа/версия: {date}. Дата доступа:23.10.2026, точное окно/секунды при наличии в provenance; сборка не выполняла новых GET.\n',f'- Product/SDK/configuration: определяется названием/версией/commit и exact scope каждой карточки ниже; совместимость разных releases не предполагается.\n',f'- Алиасы волн: '+', '.join(s['aliases'])+'\n',f'- Факты: '+(', '.join(link('F',x) for x in dict.fromkeys(s['facts'])) or 'контекст/поиск; см. provenance ниже')+'\n','- Название, автор, локатор и фактическая доступность: первичные карточки ниже сохраняют точные сведения и ошибки каждого канала. Неизвестные поля не установлены; URL/year upload не подменяет дату документа.\n']
    # Keep a unique technical source description per branch; this preserves differences in access.
    seen=set()
    for r in s['records']:
        key=(r['branch'],r['text'])
        if key in seen:continue
        seen.add(key)
        rec=r['text'].strip('| ')
        src+=[f'**{r["local"]} — [{r["file"]}](_WORK/{r["file"]})**\n\n{rec}\n']
(ROOT/'SOURCES.md').write_text('\n'.join(src),encoding='utf-8')

raw=['# RAW_FACTS — LinQ: нормализованная доказательная база\n','Актуальность источников:23.10.2026, 04:15–05:14 MSK. Это подробные наблюдения двух волн, не итоговый литературный отчёт. F-ID стабилен; S-ID ведёт к источнику и точному locator/provenance. Каждая карточка сохраняет отдельные evidence_type и actual_check. Дата проверки не является датой выпуска. W1 наблюдения остаются историей поиска; при расхождении действует явно указанная W2 disposition, а не удобная формулировка.\n','## Реально выполненные проверки\n\n- Сетевое чтение/архивы/исходники/AST и helper-пробы; протоколы под `_WORK`.\n- W2-E: скачаны реальные ONNX35,511,756B и weights35,434,956B; сравнены13conv kernels и2final biases; ONNX Runtime1.31.0 CPU: b1 success, b2 Squeeze failure; выполнена diagnostic head-only derivative. Это actual CPU model inference.\n- W2-D/G: shape helper и fake-native host probes, включая output view ownership; native `.so` не загружалась.\n- Не выполнены proprietary SDK installation/import/conversion/calibration/compile/TLM/LinQ inference. Пользовательский исход регистрации неизвестен. Не утверждается отсутствие возможностей у закрытой поставки.\n','## Обязательные W2 corrections для чтения W1\n\n1. `tf.graph_util.import_graph_def` существует в upstreamTF2.14.1; `Session(graph=None)` использует default graph. Немедленный crash/отсутствующий namespace не доказаны; остаются return/type/import namespace/names seams.\n2. Отсутствие output `.copy()` вpytpu15.0.24 не доказывает dangling: Python-owned backing удерживается base chain в host probe. Historical exception cleanup omission узко подтверждён mock, современный дефект не установлен.\n3. ModelZooTinyYOLO3 — реальные fine masks1,2,3 и embeddedNMS .6/.5/max20, исходный Darknet/runner0,1,2; public conv lineage не равна full-graph parity и не касается невыданного vendor.tpu.\n4. IVA CV `walkers-node:0.1.310` — склейка0.1.3+page10 по двум page-separated text extractions; visual/registry не подтверждены. Другие tags тоже склеены. Ниже W1 literal хранится только как история, не команда запуска.\n5. HP01=16GB,HP02=32GB документированы отдельно; общий datasheet под ссылкой02 всё ещё16GB/Gen3. Multi-device sample — реплики, pooled-memory graph не установлен.\n6. W1 blanket «никакого inference» относится W1/LinQ; W2 имеет actual public CPU inference.\n']
last=None
for f in facts:
    if f['branch']!=last:
        last=f['branch'];raw+=['\n## '+last+' — '+texts[last].splitlines()[0].lstrip('# ')+'\n']
    typ,check=status(f)
    title=f['local']
    lines=f['body'].splitlines()
    first=lines[-1] if f['body'].startswith('|') else lines[0]
    if first.startswith('|'):
        cells=first.strip('| ').split('|'); title=cells[1].strip() if len(cells)>1 else title
    else:
        first=re.sub(r'^(?:#{1,4}\s+|\*\*|[-*]\s+)','',first)
        first=re.sub(r'^(?:W[12]-[0-9A-Z]{1,2}-)?F\d{1,2}[.: —-]*','',first).strip('* ')
        title=first.split('**')[0]
    title=title[:180]
    correction=''
    if f['branch']=='W1-14' and f['local'].endswith('F02') or f['branch']=='W1-15' and f['local'].endswith('F16'):
        correction='**W2 disposition:** image0.1.310 superseded by page-separated0.1.3+p10; '+link('F',fact_alias['W2-K-F01'])+'. W1 literal below is search history, not an exact deploy tag.\n'
    if f['branch']=='W1-15' and f['local'].endswith(('F08','F09')):
        correction='**W2 clarification:** output is a view, not a numerical copy; Python-owned backing was retained in mock probe; '+link('F',fact_alias['W2-G-F06'])+'.\n'
    if f['branch']=='W1-02':correction+='**W2 scope update:** hardware variants/conflicts refined in '+link('F',fact_alias['W2-H-F02'])+', '+link('F','F279')+'; do not repeat generic HP16/32 contradiction.\n'
    raw+=['<a id="'+f['id'].lower()+'"></a>\n',f'### {f["id"]} — {title}\n',f'- Исходный локатор: [{f["local"]}](_WORK/{f["file"]}), строка{f["line"]}; контекст проверки23.10.2026; даты/версии первоисточников — в S.\n',f'- evidence_type: {typ}.\n',f'- actual_check: {check}.\n',f'- Sources: '+', '.join(link('S',s) for s in f['sources'])+'\n','- Version/configuration/scope/limitations: точные литералы и границы сохранены в наблюдении ниже; неизвестные поля не заполнены догадкой.\n',correction,replace_refs(f['body'],f['branch'])+'\n']
(ROOT/'RAW_FACTS.md').write_text('\n'.join(raw),encoding='utf-8')

mp=['# ID_MAP — локальные IDs → стабильные S/F\n','Mapping относится к двум завершённым волнам; source alias с несколькими первичными URL отображается в несколько S. Факт хранит originating branch/line, поэтому разделение доказательств не теряется.\n','## Sources\n','| Local | Global canonical records |\n|---|---|']
for a,ids in source_alias.items():mp.append('| '+a+' | '+', '.join(ids)+' |')
mp+=['\n## Facts\n','| Local | Global |\n|---|---|']
for f in facts:mp.append('| '+f['local']+' | '+f['id']+' |')
(WORK/'ID_MAP.md').write_text('\n'.join(mp),encoding='utf-8')
print(json.dumps({'sources':len(sources),'facts':len(facts),'source_aliases':len(source_alias),'fact_aliases':len(fact_alias),'matrix_records':len(matrix_units)},ensure_ascii=False))
