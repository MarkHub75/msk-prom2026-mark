from pathlib import Path
import re,json,urllib.parse,datetime,hashlib
ROOT=Path(__file__).resolve().parent.parent
FILES={
'W1-A':'W1_A_COMPETITORS_PRICES.md','W1-B':'W1_B_EFFECT_ECONOMICS.md','W1-C':'W1_C_LEGAL_MOSCOW_BUYER.md',
'W1-D':'W1_D_HARDWARE_OPERATIONS.md','W1-E':'W1_E_PROCUREMENT_FAILURES.md','W1-F':'W1_F_GLOBAL_MARKET_DIFFERENTIATION.md',
'W2-A':'W2_A_PROCUREMENT_PRICES.md','W2-B':'W2_B_CURRENT_LAW_DATA.md','W2-C':'W2_C_LINQ_COMMERCIAL_REGISTRIES.md',
'W2-D':'W2_D_EFFECT_PILOT_ECONOMICS.md','W2-E':'W2_E_MOSCOW_BUYER_PATH.md','W2-F':'W2_F_COMPETITOR_POSITIONING.md'}
DOCS={k:(ROOT/'_WORK'/v).read_text(encoding='utf-8-sig') for k,v in FILES.items()}
ACCESS={'W1-A':'05:36–05:40, повторно 05:44','W1-B':'05:36–05:44','W1-C':'05:36–05:44:50','W1-D':'05:45–05:52','W1-E':'05:45–05:51','W1-F':'05:45–05:48','W2-A':'06:05–06:19','W2-B':'06:05:32–06:18','W2-C':'06:05–06:11','W2-D':'06:19–06:32','W2-E':'06:19–06:28','W2-F':'06:24–06:28 (синтез D/E до 06:34)'}
URL=re.compile(r'https?://[^\s<>|]+')
sources={};facts={}
for p,t in DOCS.items():
    lines=t.splitlines()
    for i,line in enumerate(lines):
        sm=re.match(r'^(?:\|\s*\*{0,2}|-\s*\*{0,2}|\*{0,2})('+p+r'-S\d+)\b',line)
        if sm:sources[sm[1]]={'prefix':p,'raw':line,'line':i+1}
        fm=re.match(r'^(?:\|\s*\*{0,2}|(?:- )?\*{0,2}(?:Наш вывод )?)('+p+r'-F\d+)\b',line)
        if fm:
            block=line
            if not line.startswith('|'):
                j=i+1
                while j<len(lines) and not lines[j].startswith('#') and not re.match(r'^(?:\*{0,2}|(?:- )?\*{0,2}(?:Наш вывод )?)W[12]-[A-F]-[FS]\d+',lines[j]):
                    block+='\n'+lines[j];j+=1
            facts[fm[1]]={'prefix':p,'raw':block,'line':i+1}

def urlkey(u):
    u=urllib.parse.unquote(u.rstrip('.,;)]`'))
    x=urllib.parse.urlsplit(u)
    host=x.netloc.lower().removeprefix('www.')
    path=x.path.rstrip('/')
    # Different pages of registry search are different observed rows, not one document.
    query=x.query if ('/reestr' in path and x.query) else ''
    if host.endswith('gisp.gov.ru') and '/nmp/measure/' in path:path=path.removesuffix('/pdf')
    return urllib.parse.urlunsplit(('https',host,path,query,x.fragment if x.fragment.startswith('/product/') else ''))

smap={};sgroups={};keys={}
for local,rec in sources.items():
    urls=URL.findall(rec['raw'])
    key=urlkey(urls[0]) if urls else local
    if local=='W2-A-S03':key=urlkey(URL.findall(sources['W1-E-S01']['raw'])[0])
    if key not in keys:keys[key]=f'S{len(keys)+1:03d}'
    sid=keys[key];smap[local]=sid;sgroups.setdefault(sid,[]).append(local)

alias={'W2-A-F05':'W1-E-F01','W2-A-F09':'W1-A-F04','W2-C-F02':'W1-A-F17','W2-C-F08':'W1-D-F02',
       'W2-F-F04':'W1-A-F13','W2-F-F09':'W1-F-F04','W2-F-F11':'W2-D-F01','W2-F-F12':'W2-D-F07',
       'W2-F-F13':'W2-E-F03','W2-F-F14':'W2-E-F09'}
fmap={};fgroups={};fkeys={}
for local,rec in facts.items():
    key=alias.get(local,local)
    if key not in fkeys:fkeys[key]=f'F{len(fkeys)+1:03d}'
    fid=fkeys[key];fmap[local]=fid;fgroups.setdefault(fid,[]).append(local)

def norm(text,p):
    # Protect full branch-prefixed references, including abbreviated cross-branch chains.
    placeholders={}
    def protect(m):
        chain=m[0];cp=chain[:4]
        values=[]
        for rm in re.finditer(r'([SF])(\d{2})(?:[–—-](?:[SF])?(\d{2}))?',chain[5:]):
            kind=rm[1];a=int(rm[2]);b=int(rm[3] or rm[2]);mp=smap if kind=='S' else fmap
            values.extend(mp.get(f'{cp}-{kind}{n:02d}',f'{cp}-{kind}{n:02d}') for n in range(a,b+1))
        value=', '.join(values)
        token=f'ZZZREF{len(placeholders)}ZZZ';placeholders[token]=value;return token
    text=re.sub(r'W[12]-[A-F]-[SF]\d{2}(?:[–—-](?:[SF])?\d{2})?(?:/[SF]\d{2}(?:[–—-](?:[SF])?\d{2})?)*',protect,text)
    # Expand local ranges: global IDs are not necessarily contiguous after deduplication.
    def ran(m):
        kind=m[1];a=int(m[2]);b=int(m[3]);mp=smap if kind=='S' else fmap
        return ', '.join(mp.get(f'{p}-{kind}{n:02d}',f'{p}-{kind}{n:02d}') for n in range(a,b+1))
    text=re.sub(r'\b([SF])(\d{2})[–—-](?:[SF])?(\d{2})\b',ran,text)
    def short(m):
        local=f'{p}-{m[1]}{int(m[2]):02d}';return (smap|fmap).get(local,local)
    text=re.sub(r'(?<![A-Za-z0-9_-])([SF])(\d{2})(?!\d)',short,text)
    for token,value in placeholders.items():text=text.replace(token,value)
    # Resolve relative material links in final topic-root files.
    text=text.replace('`W2_A_MATERIALS/','`_WORK/W2_A_MATERIALS/').replace('`W2_B_MATERIALS/','`_WORK/W2_B_MATERIALS/').replace('`W2_C_MATERIALS/','`_WORK/W2_C_MATERIALS/').replace('`W2_D_MATERIALS/','`_WORK/W2_D_MATERIALS/').replace('`W2_E_MATERIALS/','`_WORK/W2_E_MATERIALS/').replace('`W2_F_MATERIALS/','`_WORK/W2_F_MATERIALS/')
    return text

def section(p,start,end=None):
    t=DOCS[p];a=t.index(start);b=t.index(end,a+len(start)) if end else len(t)
    return norm(t[a:b].strip(),p)

def striprow(raw,local):
    first,sep,tail=raw.partition('\n')
    s=first.strip().strip('|').strip()
    s=re.sub(r'^\*{0,2}'+re.escape(local)+r'\*{0,2}[. —-]*','',s).strip()
    s=s.lstrip('|').strip()
    return (s.replace(' | ','; ')+sep+tail).replace('**','')

def refs(rec):
    return sorted(set(re.findall(r'\bS\d{3}\b',norm(rec['raw'],rec['prefix']))))

# Additional facts for useful analytic blocks that the waves did not give local F IDs.
EXTRA=[
('COL-PILOT','Предлагаемый протокол измерения пользы',section('W1-B','## 4. Протокол полезного пилота','## 5. Прозрачная экономика')),
('COL-OPERATIONS','Эксплуатация, полный TCO, энергия и архив',section('W1-D','## Эксплуатация и TCO','## Реестр источников')),
('COL-DATA','Условные четыре режима данных и нормативный допуск',section('W2-B','## Условная карта данных','## Реестр новых источников')),
('COL-PRICE','Разделённый реестр цен, налогов и стадий',section('W2-A','## Реестр денежных ориентиров','## Источники,')),
('COL-TZ','Матрица российского проектного ТЗ n=1',section('W2-A','## Матрица требований','## Реестр денежных')),
('COL-HW','Послойные реестры и российская коммерческая карта',section('W2-C','## Реестровая карта','## BOM-вопросник')),
('COL-ECON','Воспроизводимая условная экономика с P/L unknown',section('W2-D','## Один условный объект','## Пилот:')),
('COL-POSITION','Опровержение отличий и условия отказа',section('W2-F','## Матрица проверки отличий','## Адресные решения')),
('COL-BUYER','Документированные звенья покупателя и условный путь',section('W2-E','## Цепочка покупателя','## Точные вопросы')),
('COL-FOREIGNTZ','Российские закупочные зацепки и границы иностранных документов',section('W1-E','## Российские процедуры','## M11:')),
('COL-RISK','Вероятностная экономика травм, штрафов и страхования',section('W1-B','### Риск травм, штрафы и страхование','## 6. Источники')),
]
for key,title,body in EXTRA:
    fid=f'F{len(fkeys)+1:03d}';fkeys[key]=fid;fmap[key]=fid;fgroups[fid]=[key]

reverse={sid:set() for sid in sgroups}
for local,rec in facts.items():
    for sid in refs(rec):
        if sid in reverse:reverse[sid].add(fmap[local])
for key,title,body in EXTRA:
    for sid in re.findall(r'\bS\d{3}\b',body):
        if sid in reverse:reverse[sid].add(fmap[key])

def write(name,s): (ROOT/name).write_text(s.strip()+'\n',encoding='utf-8')

src=['# SOURCES — market_deployment','',
'Сборка 23.10.2026 после обеих волн; нового сетевого доступа сборщик не выполнял. Доступ ниже — фактическая исследовательская сессия 23.10.2026 (UTC; Москва = UTC+3), не дата публикации. Дата публикации/редакции неизвестна, если она прямо не указана. Чтение и доступ атрибутированы исследователям. Стабильные F-ID находятся в [RAW_FACTS.md](RAW_FACTS.md), локальные алиасы — в [_WORK/ID_MAP.md](_WORK/ID_MAP.md).',
'', '## Происхождение и независимость','',
'Повторное чтение одного URL объединено в одну запись с журналом разных стадий доступа. Несколько хостов одной нормы, пресс-релиза или одной оценки рынка не являются независимыми подтверждениями: это показано в RAW_FACTS. Норма на СПС/зеркале сохраняет нормативное содержание, но хост не является официальным оригиналом. Индекс, открытая статья, полученный бинарник и выполненное испытание — разные состояния. Не все перечисленные адреса были доступны: отрицательные наблюдения имеют отдельную доказательную роль и точный статус.',
'','## Реестр использованных оснований и наблюдений доступа','']
for sid,locals_ in sgroups.items():
    src+= [f'### {sid}', '']
    allurls=[]
    for local in locals_:
        rec=sources[local];p=rec['prefix']; raw=striprow(rec['raw'],local)
        src += [f'**{p}, доступ 23.10.2026 {ACCESS[p]} UTC.** {norm(raw,p)}',
                f'Запись чтения: [{FILES[p]}, строка {rec["line"]}](_WORK/{FILES[p]}).','']
        allurls.extend(URL.findall(raw))
    src += ['**Поддерживает:** '+(', '.join(sorted(reverse[sid])) or 'наблюдение доступа/ограничение в тематических регистрах; положительный факт из недоступного содержания не извлекался')+'.','']
src += ['## Важные недоступные материалы и точный остаток','','Этот список выделяет документы, которые нельзя ошибочно назвать прочитанными оригиналами. Отказ одного транспорта не доказывает отсутствия документа.','']
unavailable=[
('Официальный 265-ФЗ','https://publication.pravo.gov.ru/document/0001202607260024','Оригинал не получен; полный текст ст.1–7 прочитан на Меганорм. Не называть открытым официальным оригиналом.','Q005'),
('Официальный приказ ФСТЭК 220','https://publication.pravo.gov.ru/document/0001202609080021','Web недоступен, requests SSL EOF; полный текст прочитан на rulaws.','Q005'),
('Актуальный перечень 360-р после1237-р','https://publication.pravo.gov.ru/document/0001202602260020','Официальный timeout; первоначальный текст прочитан на Меганорм, карточка изменения27.05.2026 прочитана; консолидированные строки не прочитаны.','Q006'),
('Официальные карточки H1/H&S/4.0','https://reestr.digital.gov.ru/reestr/8716301/ ; https://reestr.digital.gov.ru/reestr/373523/ ; https://reestr.digital.gov.ru/reestr/10836001/','Прямые карточки недоступны/timeout; АРПП открыта, поисковый индекс официального реестра прочитан; текущих выписок нет.','Q007'),
('GISP H/HPQ','https://gisp.gov.ru/goods/#/product/4767267 ; https://gisp.gov.ru/goods/#/product/4781119','Оболочка/JS403; product-ID локализованы, регистрационные номера точного комплекта не прочитаны.','Q007'),
('DSSL_price-15.10.2026.xlsx','https://www.dssl.ru/upload/medialibrary/724/tmh980ov7vkj0pid9s352ib3air808qu/DSSL_price-15.10.2026.xlsx','Файл/дата/размер37136914 видны; ни один путь не дал ячейки. Не выводить из него цену/НДС/срок.','Q009'),
('Россети32616289558','https://zakupki.gov.ru/223/purchase/public/purchase/info/common-info.html?regNumber=32616289558','ЕИС not accessible/SSL EOF, агрегаторные переходы требуют входа; ТЗ/протокол отмены/договор не прочитаны.','Q008'),
('СалаватстеклоB1903261413153','https://www.roseltorg.ru/procedure/B1903261413153','Первичный недоступен; DOCX из РосТендер Internal Error, requests403.','Q008'),
('РТ-Инжиниринг1201618','https://www.tender.pro/api/tender/1201618/view_public?tenderid=1201618','Web недоступен, requests503 Testing; только карточка Контур.','Q008'),
('Исходный XLSX Росстата2025','https://rosstat.gov.ru/storage/mediabank/pr_travm_2025.xlsx','Исходный бинарник не получен; PDF-конверсия4стр. через публичный viewer прочитана и сохранена.','Q014'),
('Октябрьская заявка и актуальный scoring','https://i.moscow/pilot ; https://i.moscow/pilot/grant','403; весенние приказы прочитаны, октябрьский отбор/обновление scoring не установлены.','Q011'),
('Поздний реестр площадок30.09.2026','https://base.garant.ru/415003232/','Только индекс; полное открытие403, первичный реестр не получен.','Q011'),
('Полный Science2012 и DOL CLEAR','https://www.hbs.edu/ris/download.aspx?name=LevineToffelJohnson_2012_Science.pdf ; https://clear.dol.gov/sites/default/files/OSHALevine2012.pdf','403; abstract/релиз HBS доступны, исследование инспекций не AI.','Q013'),
('IVA CV руководство — бинарный оригинал','https://ivacv.ru/wp-content/uploads/2026/05/Руководство_администратора_сайт.pdf','Web-текст титула/с.4–6 прочитан; requests SSL, бинарник не сохранён; не писать что PDF лежит в MATERIALS.','Q010'),
]
for title,url,status,q in unavailable:src += [f'- **{title}** — {url}. {status} Связь: {q}.']
src += ['','## Локальные артефакты','',
'[W2_A_MATERIALS/MANIFEST.json](_WORK/W2_A_MATERIALS/MANIFEST.json): первичные PDF ТЗ ШСУ (7стр.) и перечня НТЭК (55стр.; прочитаны шапка и строка257), PNG страниц, SHA256 и время. [W2_D_MATERIALS/MANIFEST.json](_WORK/W2_D_MATERIALS/MANIFEST.json): PDF-конверсия XLSX, полученный PDF538, исторический MET2018, PNG; [MODEL.py](_WORK/W2_D_MATERIALS/MODEL.py) и [MODEL_RESULTS.json](_WORK/W2_D_MATERIALS/MODEL_RESULTS.json). [W2_E_MATERIALS/MANIFEST.json](_WORK/W2_E_MATERIALS/MANIFEST.json): PDF базовых актов/приказов и PNG прочитанных страниц. Публичный viewer — транспорт, а не независимый источник содержания; хеш с недоступным origin не сравнивался. Выписки B/C/F — собственные заметки, не оригиналы внешних публикаций.']
write('SOURCES.md','\n'.join(src))

raw=['# RAW_FACTS — нормализованная доказательная база market_deployment','',
'Собрано 23.10.2026 из W1/W2 без новой сети, запуска продукта и аппаратных измерений. Все F-ID стабильны в пределах темы. S-ID раскрываются в [SOURCES.md](SOURCES.md), Q/E-ID — в [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). [ID_MAP](_WORK/ID_MAP.md) сохраняет происхождение. Ни версия документа, ни дата доступа не равны дате испытания.','',
'## Обязательные поправки после W2','',
'IVA CV/Cognitive Solutions прямо описывает LinQ TPU и демонстрационный ПАК ОТПБ19.06.2026: общая уникальность «СИЗ на LinQ» опровергнута, серийная поставка и benchmark не установлены. Российский ТЗ теперь n=1: ШСУ, проектирование2026,26 рабочих камер+4ЗИП, минимум9аналитических,32канальная ёмкость; это не30PPE-потоков и не исполненный контракт. Parsec относится к двери серверной. Московские прямые штатные условия отменены2474-ПП, апрельский ресурсный scoring существует отдельно; обновление после сентября и октябрьский набор неизвестны. Статистика2025 относится к своему обследуемому контуру, не всем занятым РФ. Денежные значения модели — assumptions, P/L неизвестны. Полные правовые тексты на нормативных зеркалах не становятся прочитанными официальными оригиналами.','',
'## Типы доказательства и порядок чтения','',
'CLAIM — заявление вендора/заказчика; DOC — конкретное положение документации/ТЗ; NORM-MIRROR — нормативный текст на вторичном хосте; STAT — официальная статистика со способом получения/охватом; STUDY — исследование с собственной областью; OBS — наблюдение чтения/доступа; INFER — наш вывод; ASSUME/CALC — предположение/расчёт; UNKNOWN — неизвестно. Исследовательская фиксация документа не равна нашему тесту продукта. Тип уточнён внутри каждой записи. Если ранняя и поздняя записи связаны, использовать поздний фактический статус; ранние ограничения чтения сохранены как история.','',
'## Каталог конкурентов — единая схема','',
section('W2-F','## Однородные карточки','## Матрица проверки отличий'),
'','## Индекс канонических фактов','']
UPDATES={
'W1-B-F11':'W2-D-F04/W2-D-F05',
'W1-C-F03':'W2-B-F01','W1-C-F04':'W2-B-F02','W1-C-F05':'W2-B-F03/W2-B-F04/W2-B-F05',
'W1-C-F08':'W2-B-F07','W1-C-F09':'W2-B-F08','W1-C-F11':'W2-B-F08','W1-C-F12':'W2-B-F10/W2-B-F11',
'W1-C-F13':'W2-B-F12','W1-C-F14':'W2-B-F13/W2-B-F14/W2-B-F16','W1-C-F15':'W2-B-F15',
'W1-C-F16':'W2-E-F02/W2-E-F03','W1-C-F17':'W2-E-F04/W2-E-F06/W2-E-F08/W2-E-F09',
'W1-C-F18':'W2-E-F03','W1-D-F08':'W2-C-F01/W2-C-F03/W2-C-F05/W2-C-F06/W2-C-F07',
'W1-D-F14':'W2-F-F05/W2-F-F06/W2-F-F07','W1-F-F20':'W2-F-F05/W2-F-F10',
}
for fid,locals_ in fgroups.items():
    if locals_[0].startswith('COL-'):continue
    raw += [f'### {fid}','']
    if len(locals_)>1:raw += ['Объединённые наблюдения одного предмета; повтор/перепечатка не является независимым подтверждением.','']
    for old in locals_:
        if old in UPDATES:raw += ['**Позднее уточнение после W2:** '+norm(UPDATES[old],facts[old]['prefix'])+'. Ранний статус чтения/неизвестности ниже — история первой волны; актуальное решение принимать по указанным поздним фактам.','']
    for local in locals_:
        rec=facts[local];p=rec['prefix'];body=norm(striprow(rec['raw'],local),p)
        raw += [f'**Происхождение {p}; контекст доступа 23.10.2026 {ACCESS[p]} UTC.** {body}',
                f'Локатор сохранённой выписки: [{FILES[p]}, строка {rec["line"]}](_WORK/{FILES[p]}).','']

raw += ['## Сравнительные регистры и подробные расчётные блоки','',
'Следующие F-ID нормализуют содержательные таблицы и процедуры волн, которым ранее не были назначены собственные F. Это аналитические/методические конструкции с явными исходными источниками; они не создают новые рыночные измерения.','']
for key,title,body in EXTRA:
    raw += [f'### {fmap[key]} — {title}','',body,'']
raw += ['## Дополнительные ценовые строки и границы рынка','',
section('W1-A','## Сопоставление публичных цен','## Что меняется'),
section('W1-F','## M14 — оценки рынка','## Реестр источников'),
'','## Связанные цепочки происхождения и неразрешённые противоречия','',
'1. Росэнергоатом: CNews-реклама, официальный Telegram и корпоративный Вестник описывают один класс системы/claims. Сумма ссылок не создаёт независимого причинного эффекта. 10раз — нарушения,98% — неопределённая регистрация, ноль травм в помещениях — редкий исход без экспозиции; это разные показатели. Q013.\n2. TelecomDaily→Seldon/SberPro — одна оценка; прогноз2025 не итог2025. Ivideon — другой состав/методика. Широкие CCTV/VA/HSE не складывать. Q018.\n3. HPS<1150Вт в презентации vs до1500Вт TDP в datasheet: режим/ревизия/граница мощности не согласованы; не усреднять. Q003.\n4. IVA CV: Linux≥6.0 PDF vs≥6.1 веб; версия сборки неизвестна. Презентация2025 без LinQ уступает новым прямым документам2026, но это не наш запуск. Q010.\n5. Macroscop overview CPU/GPU vs install Special/GPU: выбрать точные build/нейропакет, не универсальную удобную формулировку. Q009/Q010.\n6. Россети: «завершена»/«отменена» у агрегаторов не равны акту контракта или техническому провалу; исход и причины неизвестны. Q008.\n7. Приказ220 меняет235 с01.03.2027; текущий239 имеет отдельно прочитанныйп.31. Новость «оба с01.09.2026» не нормативное основание. Полные тексты прочитаны на зеркалах; актуальную применимость к объекту согласует заказчик. Q005/Q006.\n8. Роспатент, реестр Минцифры, промышленный реестр и нацрежим имеют разные предметы. H1№32778 — SDK,10990 — старыйH&S,33642 — отдельный4.0; product4767267/4781119 — ID каталога. Q007.\n9. Прямое требование5работников отменено2474-ПП; численность остаётся подкритерием прочитанного апрельского scoring. Это разные механизмы и даты, противоречие не снимается догадкой об автоматической отмене приказа. Q011.','',
'## Неидентифицированные положительные доказательства не создаются','',
'Размеры/выручка/штат большинства компаний, репрезентативные частоты требований российских ТЗ, московский локальный риск, контрактная цена полного PPE-пакета, независимое предотвращение травм, подтверждённый судебный промышленный PPE-провал, гарантированная постхакатонная покупка не установлены. Отсутствие доступного материала не означает отсутствие объекта. Остатки и предметные способы ответа перечислены в OPEN_QUESTIONS.']
write('RAW_FACTS.md','\n'.join(raw))

idmap=['# ID_MAP — стабильные идентификаторы market_deployment','',
'Назначены сборщиком23.10.2026 после двух волн. Один S объединяет чтение одного URL/документа; варианты хоста/редакции и независимость раскрыты в SOURCES. Один F может содержать позднее уточнение одного наблюдения; хронология сохранена. При копировании в соседнюю тему использовать префикс market_deployment.','',
'## Источники','', '| Локальный ID | Стабильный ID | Файл исходной записи |','|---|---|---|']
for local,sid in smap.items():idmap.append(f'| {local} | {sid} | {FILES[sources[local]["prefix"]]} |')
idmap+=['','## Факты','', '| Локальный ID/содержательный блок | Стабильный ID |','|---|---|']
for local,fid in fmap.items():idmap.append(f'| {local} | {fid} |')
idmap+=['','## Вопросы и эксперименты','', 'Локальные вопросы волн не имели единого Q/E-ID; назначены заново в OPEN_QUESTIONS.md. K001–K012 сохранены без перенумерации. E001–E008 — только предлагаемые процедуры, ни одна не представлена выполненным экспериментом.']
write('_WORK/ID_MAP.md','\n'.join(idmap))
write('_WORK/COLLECT_META.json',json.dumps({'sources':smap,'facts':fmap,'source_count':len(sgroups),'fact_count':len(fgroups),'source_defs':len(sources),'fact_defs':len(facts)},ensure_ascii=False,indent=2))
print(json.dumps({'source_count':len(sgroups),'fact_count':len(fgroups),'source_defs':len(sources),'fact_defs':len(facts),'files':[str(ROOT/n) for n in ['SOURCES.md','RAW_FACTS.md','_WORK/ID_MAP.md']]},ensure_ascii=False))
