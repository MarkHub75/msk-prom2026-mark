from pathlib import Path
import re,json
R=Path.cwd(); W=R/'_WORK'
cells=[f'W1_{i:02}' for i in range(1,16)]+[f'W2_{i:02}' for i in range(1,5)]
texts={c:(W/f'{c}.md').read_text(encoding='utf-8-sig') for c in cells}
prefix=lambda c:c.replace('_','-')
# One source identity can have several retrieval records and locator scopes.
merge={'W1-12-S01':'W1-11-S04','W2-01-S01':'W1-15-S06','W2-01-S02':'W1-15-S05','W2-01-S03':'W1-15-S03','W2-01-S04':'W1-15-S04','W2-03-S02':'W1-14-S08','W2-04-S04':'W1-05-S04'}
smap={}; canon={}; src_cells={}
for c,t in texts.items():
 for n in sorted(set(re.findall(prefix(c)+r'-S(\d{2})',t))):
  old=prefix(c)+'-S'+n; key=merge.get(old,old)
  if key not in canon:canon[key]=f'S{len(canon)+1:03}'
  smap[old]=canon[key];src_cells.setdefault(canon[key],[]).append(c)
# Explicit Q aliases consolidate by decision owner rather than appearance.
qgroups={
'Q001':['W1-01-Q01','W1-07-Q01','W2-02-Q01','W2-04-Q01'],
'Q002':['W1-01-Q02','W1-03-Q01','W1-14-Q01','W2-03-Q01'],
'Q003':['W1-01-Q03'], 'Q004':['W1-01-Q04'],
'Q005':['W1-07-Q02'], 'Q006':['W1-07-Q03'], 'Q007':['W1-07-Q04'],
'Q008':['W1-07-Q05','W1-12-Q02'],
'Q009':['W2-01-Q01','W1-12-Q03'], 'Q010':['W2-01-Q02'],
'Q011':['W2-01-Q03','W1-14-Q03'], 'Q012':['W2-01-Q04'],
'Q013':['W1-12-Q01','W2-02-Q02','W2-04-Q03','W1-14-Q04'],
'Q014':['W1-12-Q04','W2-02-Q03','W2-03-Q02','W2-04-Q02'],
'Q015':['W2-03-Q03','W1-14-Q06'], 'Q016':['W2-04-Q04'],
'Q017':['W1-14-Q02'], 'Q018':['W1-14-Q05']}
qmap={x:q for q,xs in qgroups.items() for x in xs}
# Separate source register sections from substantive records.
sections={};ssections={};preambles={}
for c,t in texts.items():
 chunks=re.split(r'(?m)^## ',t);preambles[c]=chunks[0].strip();sections[c]=[];ssections[c]=[]
 for chunk in chunks[1:]:
  title,_,body=chunk.partition('\n')
  is_src=bool(re.match(r'Sources(?: and|,)|Source (?:register|registry)|Идентичность и воспроизводимость источника|Provenance and sources',title))
  (ssections[c] if is_src else sections[c]).append((title,body.strip()))
# Source definition metadata parser; retain multiple retrievals for merged sources.
metas={s:[] for s in canon.values()}
for c,secs in ssections.items():
 for title,body in secs:
  lines=body.splitlines(); starts=[]
  for i,l in enumerate(lines):
   if re.match(r'(?:\| |[-*] \*\*|[-*] S|### |\*\*)'+re.escape(prefix(c))+r'-S\d',l):starts.append(i)
  # W1_03 S06/07 are intentionally one shared source paragraph; individual identities retained.
  for k,i in enumerate(starts):
   end=starts[k+1] if k+1<len(starts) else len(lines)
   if lines[i].startswith('| '): end=i+1
   block='\n'.join(lines[i:end]).strip()
   ids=list(dict.fromkeys(re.findall(prefix(c)+r'-S\d{2}',block.split('\n\n')[0])))
   # W2_01 puts S03 and S04 on one paragraph; preserve both locator records.
   if c=='W1_03' and 'W1-03-S06' in ids: ids=['W1-03-S06','W1-03-S07']
   for old in ids:
    if old in smap:metas[smap[old]].append((c,title,block))
# W1_01 sources table source records detected; source-meta fallback preserves provenance without fabrication.
for old,s in smap.items():
 c=old[:5].replace('-','_')
 if not any(prefix(c) in block for cc,title,block in metas[s]):
  for title,body in ssections[c]:
   if old in body:metas[s].append((c,title,body))
# W2_03 provenance includes the primary table and applied questions in a combined section.
ssections['W2_03']=[(title,body) for title,body in sections['W2_03'] if title.startswith('Provenance, scope')]
for title,body in ssections['W2_03']:
 for line in body.splitlines():
  if line.startswith('| W2-03-S'):
   old=re.search(r'W2-03-S\d{2}',line).group()
   metas[smap[old]].append(('W2_03',title,line))
# Resolve compact cross-branch references before local shorthand (e.g. W2-02-P01/P02).
def expand_cross(t):
 pat=r'(W[12]-\d{2}-)([SFPDXCEQ])(\d{2})((?:/[SFPDXCEQ]?\d{2})+)'
 def repl(m):
  base,typ,num,tail=m.groups()
  return base+typ+num+''.join('/'+base+(z[0] if z[0].isalpha() else typ)+(z[1:] if z[0].isalpha() else z) for z in tail.split('/')[1:])
 t=re.sub(pat,repl,t)
 def underscore(m):
  base=m.group(1)+'-'+m.group(2)+'-'; return '/'.join(base+z for z in m.group(3).split('/'))
 return re.sub(r'\b(W[12])_(\d{2})\s+([SFPDXCEQ]\d{2}(?:/[SFPDXCEQ]\d{2})*)',underscore,t)
# Fine-grained records: section boundaries, numbered subprotocols, and explicitly labeled observations.
records=[];fmap={};section_map={}
for c,secs in sections.items():
 for title,body in secs:
  # Q/handoff-only sections go to the questions registry; preserve detailed evidence elsewhere.
  if re.match(r'(?:Handoff and localized|Open questions and handoff|Remaining unknowns / handoff|Open requirements and handoff|Remaining inputs and K dispositions|Адресная передача|K-ID|Remaining owner/artifact|Open questions and addressable)',title):continue
  lines=body.splitlines(); cuts=[0]
  for i,l in enumerate(lines):
   if i and (re.match(r'### ',l) or re.match(r'(?:[-*] )?\*\*'+re.escape(prefix(c))+r'-(?:F|D|X|E)\d',l) or (c=='W2_03' and re.match(r'\*\*F0[5-8]:',l))):cuts.append(i)
  cuts=sorted(set(cuts))
  for j,i in enumerate(cuts):
   b='\n'.join(lines[i:cuts[j+1] if j+1<len(cuts) else len(lines)]).strip()
   if len(re.sub(r'\s','',b))<50:continue
   f=f'F{len(records)+7:03}'; label=title
   if b.startswith('### '):label=b.splitlines()[0][4:]; b='\n'.join(b.splitlines()[1:]).strip()
   elif re.match(r'(?:[-*] )?\*\*'+re.escape(prefix(c))+r'-',b):label=b.splitlines()[0].split('**',2)[1]
   rec={'id':f,'cell':c,'section':title,'title':label,'body':b}
   records.append(rec);section_map.setdefault(c,[]).append(f)
   # First actual appearance maps an old identifier to its containing normalized record.
   for old in re.findall(r'W[12]-\d{2}-(?:F|P|D|X|C|E)\d{2}',title+'\n'+b):fmap.setdefault(old,f)
   # Expand shortened ranges and section-local references.
   if c=='W2_03' and re.match(r'\*\*F0[5-8]:',b):
    fmap[prefix(c)+'-'+re.match(r'\*\*(F0[5-8]):',b).group(1)]=f
   for code in re.findall(r'^(?:P|C|X)\d{2}\b',title):fmap[prefix(c)+'-'+code]=f
   if label!=title:
    for code in re.findall(r'^(?:P|C|X)\d{2}\b',label):fmap[prefix(c)+'-'+code]=f
for n in range(1,9):fmap[f'W1-08-C{n:02}']='F116'
fmap['W1-08-C09']='F118'
fmap['W1-13-E01']='F185'
# Records with source register-only local observation E01 refer to metadata/checking, not future experiments.
# W1_13 E01 is executed maths detailed in the small examples sections.
for old,s in smap.items():pass
# Resolve local links to portable topic-root paths.
def paths(t):
 t=re.sub(r'\]\((W[12]_\d{2}_SOURCES/[^)]*)\)',r'](_WORK/\1)',t)
 return t

def norm(t,c,where='raw'):
 t=expand_cross(paths(t))
 def explicit(m):
  x=m.group();
  if x in smap:return f'[{smap[x]}](SOURCES.md#{smap[x].lower()})'
  if x in qmap:return f'[{qmap[x]}](OPEN_QUESTIONS.md#{qmap[x].lower()})'
  if x in fmap:
   f=fmap[x];return f'[{f}]({"#" if where=="raw" else "RAW_FACTS.md#"}{f.lower()})'
  return x
 t=re.sub(r'W[12]-\d{2}-(?:S|F|P|D|X|C|E|Q)\d{2}',explicit,t)
 # Local shorthand Sxx / Pxx etc still resolves in the branch's scope.
 def local(m):
  typ,num=m.group(1),m.group(2); x=prefix(c)+'-'+typ+num
  if x not in smap and x not in fmap and x not in qmap:return m.group()
  return explicit(type('M',(),{'group':lambda self:x})())
 t=re.sub(r'(?<![\w.-])([SFPDXCEQ])(\d{2})(?!\d)',local,t)
 return t
# Source associations are references, not a claim that all proposals are source-prescribed.
sfacts={s:set() for s in canon.values()}
for rec in records:
 c=rec['cell'];b=expand_cross(rec['body']+'\n'+rec['title'])
 for old in re.findall(r'W[12]-\d{2}-S\d{2}',b):
  if old in smap:sfacts[smap[old]].add(rec['id'])
 for n in re.findall(r'(?<![\w.-])S(\d{2})\b',b):
  old=prefix(c)+'-S'+n
  if old in smap:sfacts[smap[old]].add(rec['id'])
 # Expand compact S01–S03 ranges.
 for a,z in re.findall(r'(?<![\w.-])S(\d{2})[–-]S?(\d{2})',b):
  for n in range(int(a),int(z)+1):
   old=prefix(c)+f'-S{n:02}'
   if old in smap:sfacts[smap[old]].add(rec['id'])
# Add explicit source-to-synthesis links (proposals remain labeled as ours).
for source_id,fs in {'S124':['F002'],'S121':['F002'],'S122':['F002'],'S123':['F002'],'S127':['F003'],'S128':['F003'],'S129':['F003'],'S131':['F004'],'S117':['F004'],'S132':['F004'],'S133':['F005'],'S134':['F005'],'S135':['F005'],'S029':['F005']}.items():
 if source_id in sfacts:sfacts[source_id].update(fs)
source_urls={
'S026':'https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/eval_detection.py',
'S027':'https://github.com/activitynet/ActivityNet/blob/82304fa9f4a7219421df13dae6347a445c4cf5bc/Evaluation/utils.py',
'S028':'https://github.com/TUT-ARG/sed_eval/blob/0cb1b6d11ceec4fe500cc9b31079c9d8666ed6eb/sed_eval/sound_event.py',
'S030':'https://github.com/TUT-ARG/sed_eval/blob/0cb1b6d11ceec4fe500cc9b31079c9d8666ed6eb/sed_eval/metric.py',
'S031':'https://tut-arg.github.io/sed_eval/generated/sed_eval.sound_event.EventBasedMetrics.html',
'S032':'https://dcase.community/challenge2017/download',
'S033':'https://dcase.community/challenge2020/task-sound-event-detection-and-separation-in-domestic-environments',
'S034':'https://arxiv.org/html/2010.13648v1'}
# Initial authoritative normalized notes, with later section links generated below.
intro='''# RAW_FACTS — evaluation

Собрано по завершённым 15 W1 и четырём W2; новые источники после W2 не получались. Дата исследования — 23 октября 2026, Europe/Moscow (UTC+03:00); точные моменты доступа относятся к соответствующим S-записям. Это подробная фактическая база, а не измерение системы. [Реестр источников](SOURCES.md), [вопросы и будущие эксперименты](OPEN_QUESTIONS.md), [исходная критика и dispositions](CRITIC.md).

У каждого F сохранены исходный контекст, определения, параметры, граничные случаи и фактический статус проверки. DOC — первичная документация; CODE — прочитанный исходник; PUB/PAPER — опубликованный результат/метод авторов; LOCAL/LOCAL MATH — фактически выполненная маленькая синтетическая проверка/арифметика; INFERENCE/DERIVATION — наш вывод/вывод формулы; PROPOSAL/PROPOSED — предложенный договор; UNKNOWN — недостающий вход. Тип основания и выполнение различаются: прочитанный код не считается запущенным. Групповые F-записи сохраняют исходные метки каждого наблюдения внутри, не превращая всё содержимое в один измеренный факт.

## F001 — Фактический уровень выполненной работы
<a id="f001"></a>

**Основание: локальное состояние и выполненные исследователями действия.** Существуют 19 завершённых branch-результатов и сохранённые первичные snapshots/locators. Исполнены только явно названные source-level/synthetic mathematical fixtures (COCO matching/accumulation, извлечённые sed_eval validators, TrackEval metrics на supplied similarity, статистическая арифметика, ActEV extracted function, конечная sampling enumeration и tiny matcher oracle). Ни один не является измерением модели, промышленного видео, LinQ, event recall, FPS или эксплуатационной безопасности. Нет полученного SDK, endpoint/device access, actual model/weights, organizer data/evaluator или соседних готовых отчётов. Для будущих прогонов используются E-карточки в OPEN_QUESTIONS.

## F002 — LinQ: публичный blocking path установлен; actual execution неизвестен
<a id="f002"></a>

**DOC/CODE/INFERENCE; чтение, без исполнения.** Руководство IVA H1 2025 RU.РМДВ.04.06.014-03 34 01 описывает list/open/load/inference и blocking `inference.sync(...)` с returned output mapping. Оно не было установлено/исполнено. TLM `execution_time_us` — estimate, µs, не hardware samples. Устаревшая широкая формулировка W1 о неизвестном completion API ниже читается только как неизвестная actual package/remote applicability. Python3.11 versus3.8, signature/default and sample-fragment расхождения сохранены. Wheel/build, working example, allocated hardware, remote job semantics, placement/fallback и physical timer требуют артефакта/доступа ([Q009](OPEN_QUESTIONS.md#q009)–[Q012](OPEN_QUESTIONS.md#q012)); [K001](CRITIC.md#k001).

## F003 — Экспозиция и достаточность review зависят от estimand
<a id="f003"></a>

**PROPOSAL/INFERENCE, W2 уточняет W1.** Complete destination-delivery census + adjudication всех record assertions с достаточным context может установить semantic false records / fixed logged source camera-hours без полной разметки каждого non-alert кадра. Это не recall, не verified-normal exposure и не false-active duration. Strict useful one-to-one precision дополнительно требует закрытого matching neighborhood. Для recall нужна независимая discovery всех GT onsets либо корректный probability-sampled core audit. Поэтому W1 formulations «fully reviewed hours» ниже сохраняются только для соответствующего более строгого endpoint. Source burden использует immutable latest-consumed-input evidence anchor при first logical alert creation; wall-hour workload — actual visible records в receiver interval. У record exactly one source owner, поздний retry не меняет owner. Finite close C именует delivered-by-C snapshot, не eventual total; все pending/late/drain/carry-in/out остаются в ledger. Source-alert precision и onset-GT recall не имеют автоматически общего TP/F1. См. [Q013](OPEN_QUESTIONS.md#q013), [Q014](OPEN_QUESTIONS.md#q014), [K002/K003](CRITIC.md).

## F004 — Randomized finite-corpus review: unbiased totals, generally biased ratio
<a id="f004"></a>

**PROPOSAL/DERIVATION + LOCAL MATH.** Disjoint exhaustive half-open cores, known positive inclusion π, independent full-core reference review, onset ownership и достаточный adjoining context позволяют design-unbiased HT totals Σy/π для fixed recorded corpus. Это randomization inference: iid camera contents/events не требуются. Future-camera inference требует отдельного population/sample model. Recall That/Ehat — generally biased ratio, даже если оба total estimates unbiased; tiny exact enumeration mean ratio .5625 против истинных .3. Контекст не становится дополнительным selected unit. Global one-to-one outcomes требуют closure всего competing component; произвольный margin не гарантирует closure. Неответ/нечитаемый selected core нельзя заменить/заполнить нулём. Нулевой Ehat даёт NA recall; n_h=1 noncertainty stratum не даёт указанной variance estimate. [Q014](OPEN_QUESTIONS.md#q014), [Q015](OPEN_QUESTIONS.md#q015), [K004](CRITIC.md).

## F005 — Предложенный lex-offline-v1 — tiny exact oracle
<a id="f005"></a>

**PROPOSAL + выполненные LOCAL MATH fixtures.** Objective lexicographically minimizes (-pair count, summed nonnegative exact cost, sorted stable pair list), invalid edges absent, unmatched explicit. Costs Fraction/ticks; no epsilon/big-M. Выполнены 13 named graphs/permutations, все512 labeled3×3 graphs cardinality versus SciPy1.17.1 и independent partial-injection oracle для всех трёх priorities. Reference exponential, годится для tiny conformance; scalable production implementation не проверена. Sum delay не min max/p95: fixed selected subsets имеют permutation-invariant sum(d)-sum(s). Это отдельный supplemental protocol, не замена COCO/ActivityNet/sed_eval/official scoring. [Q016](OPEN_QUESTIONS.md#q016), [K006](CRITIC.md).

## F006 — Interval truth, censoring и граница K005
<a id="f006"></a>

**PROPOSAL/DERIVATION + tiny LOCAL MATH.** Exact point endpoint требует известной truth/identity/clock и полного opportunity follow-up. Unknown onset support не probability distribution. Definite-edge graph и possible-edge union дают только outer matching count bounds при fixed known roster; possible union maximum не обязательно attainable: linked onsets s1=θ,s2=θ+1 допускают individually possible2, jointly max1. Общего solver по jointly feasible truth worlds не создано и не заявлено. Unknown roster/identity меняет знаменатель и требует quarantine/конкретных совместных truth cases. Primary complete-component endpoint исключает весь incomplete stratum/component, включая successes, с counts/exposure; это narrow conditional endpoint, не unbiased whole-population recall. Known short episodes с завершившейся opportunity остаются полными; processing outage при известном GT/log — operational miss, missing logs/follow-up — unresolved. [Q014](OPEN_QUESTIONS.md#q014), [K005](CRITIC.md).

'''
intro=intro.replace('## F003', 'Основание: [S124](SOURCES.md#s124), [F217](#f217)–[F223](#f223); manual printed pp5–10,17,19–25, сохранённый numbered text L0–L650.\n\n## F003',1)
intro=intro.replace('## F004', 'Основание: [F224](#f224)–[F234](#f234), source-derived distinctions [S127](SOURCES.md#s127), [S128](SOURCES.md#s128), [S129](SOURCES.md#s129); ownership/close rules являются нашими proposals.\n\n## F004',1)
intro=intro.replace('## F005', 'Основание: [F235](#f235)–[F249](#f249), [S131](SOURCES.md#s131), [S117](SOURCES.md#s117), [S132](SOURCES.md#s132); exact invented-population outputs сохранены в [fixtures.json](_WORK/W2_03_SOURCES/fixtures.json).\n\n## F005',1)
intro=intro.replace('## F006', 'Основание: [F251](#f251), [F252](#f252), [F256](#f256)–[F261](#f261); solver semantics [S133](SOURCES.md#s133), [S134](SOURCES.md#s134); our [reference/results](_WORK/W2_04_SOURCES/results.json).\n\n## F006',1)
intro += '\nОснование F006: [F253](#f253), [F254](#f254), [F262](#f262)–[F265](#f265); [joint-onset/censor fixtures](_WORK/W2_04_SOURCES/results.json). Joint-world general solver не является полученным источником или выполненной реализацией.\n'
raw=[intro];index=[]
for c in cells:
 raw.append(f'\n# {c} — сохранённые подробные наблюдения\n\nПроисхождение: [{c}](_WORK/{c}.md); [snapshots и локальные fixtures](_WORK/{c}_SOURCES/). Контекст доступа и выполнения: '+paths(preambles[c].split('\n',1)[-1]).replace('\n',' ')+'\n')
 if c in ['W1_06','W1_07','W1_08','W1_12','W1_13','W1_14','W1_15']:raw.append('\n**Уточнение сборки:** единый W2 metric-specific/source-close договор [F003](#f003) имеет приоритет над broad «reviewed H_eval» wording; это сохраняет соответствующие более узкие определения как диагностические, а не универсальные.\n')
 if c=='W1_11':raw.append('\n**Уточнение сборки:** публичный blocking sync найден и сохранён; blanket unknown уточнён [F002](#f002). Actual environment остаётся unknown.\n')
 if c=='W1_05':raw.append('\n**Уточнение сборки:** точные eligibility/assignment/censoring уточнены [F005](#f005), [F006](#f006). Common-TP formulas применяются лишь в shared closed universe; boundary source/onset cohorts см. [F003](#f003).\n')
 for rec in [x for x in records if x['cell']==c]:
  f=rec['id']; title=norm(rec['title'],c)
  title=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',title)
  title=re.sub(r'^F\d{3}(?:[–-]F\d{3})?\s*(?:[—/:–-]\s*)?', '',title)
  title=re.sub(r'\s*[—–]\s*F\d{3}$','',title)
  if not title.strip():title='VOC/COCO: interpolation, matching, coordinates and difficult/crowd differences'
  if rec['cell']=='W2_03' and re.match(r'\*\*F0[5-8]:',rec['body']):title=rec['body'].split('**',2)[1]
  raw.append(f'\n## {f} — {title}\n<a id="{f.lower()}"></a>\n\n'+norm(rec['body'],c)+'\n')
  index.append((f,c,title))
(R/'RAW_FACTS.md').write_text('\n'.join(raw),encoding='utf-8')
# Detailed source registry: original metadata retained, duplicate source identities reconciled.
sout=['''# SOURCES — evaluation

Реестр первичных оснований из завершённых 15 W1 и 4 W2. Сборщик новых материалов не получал. Дата доступа — 2026-10-23, с фактическим часовым поясом в каждой записи/локальном manifest; дата публикации/commit/version указана отдельно или честно unknown. Это не подтверждение установленной у команды версии. Один S может объединять повторные чтения того же документа/commit; разные implementation versions остаются разными S. Код, текст документа, metadata и фактическое исполнение не смешиваются.

Ссылки F ниже ведут к извлечённым наблюдениям и явно помеченным выводам/предложениям, которые используют источник. Они не означают, что источник предписывает наш промышленный deadline, matcher или policy. Локальная source directory содержит retrieval/hash records; успешное web-only чтение при failed native download отмечено в метаданных. Недоступный lead не становится доказательством и не означает отсутствия capability. Повторные retrieval records сохраняют ограничения маршрута инструмента.

''']
for s in canon.values():
 aliases=[old for old,v in smap.items() if v==s]
 sout.append(f'## {s}\n<a id="{s.lower()}"></a>\n\nИдентичность/исходные locator IDs: '+', '.join('`'+x+'`' for x in aliases)+'.\n')
 if s in source_urls:sout.append('Прямой URL первичного основания: '+source_urls[s]+'\n')
 fs=sorted(sfacts[s]);
 if fs:sout.append('Поддерживаемые наблюдения/применения: '+', '.join(f'[{f}](RAW_FACTS.md#{f.lower()})' for f in fs)+'.\n')
 else:sout.append('Статус: вспомогательное первичное основание или retrieval-only lead; конкретная использованная область и ограничение ниже. Самостоятельный измеренный результат не утверждается.\n')
 seen=set()
 for c,title,b in metas[s]:
  if b in seen:continue
  seen.add(b)
  # Render table metadata as compact paragraphs so column headings cannot be lost.
  if b.startswith('| '): b=' — '.join(x.strip() for x in b.strip('| ').split('|'))
  sout.append(f'Контекст доступа и actual verification из branch: '+paths(preambles[c].split('\n',1)[-1]).replace('\n',' ')+'\n')
  sout.append(f'Происхождение записи: [{c}](_WORK/{c}.md), [source artifacts](_WORK/{c}_SOURCES/).\n\n'+norm(b,c,'source')+'\n')
 if not metas[s]:sout.append('См. точный исходный branch register: '+', '.join(f'[{c}](_WORK/{c}.md)' for c in src_cells[s])+'. Извлечённые метаданные отсутствуют; это не утверждение о недоступности источника.\n')
(R/'SOURCES.md').write_text('\n'.join(sout),encoding='utf-8')
# Save normalized maps incrementally before questions/cards and dispositions.
mapout=['# ID_MAP — evaluation\n\nStable IDs assigned by collector; branch files remain untouched. Several original observations can share a normalized detailed protocol record when their definitions and edge cases belong together. Repeated primary source identity/commit merges retain all retrieval records. Future E001+ cards are separate from executed local branch examples.\n','## Sources\n\n| Branch ID | Normalized |\n|---|---|']
mapout += [f'| `{old}` | [{s}](../SOURCES.md#{s.lower()}) |' for old,s in smap.items()]
mapout += ['\n## Facts, proposals and local examples\n\n| Branch ID | Normalized detail record |\n|---|---|']
mapout += [f'| `{old}` | [{f}](../RAW_FACTS.md#{f.lower()}) |' for old,f in sorted(fmap.items())]
mapout += ['\n## Questions\n\n| Branch ID | Consolidated actionable question |\n|---|---|']
mapout += [f'| `{old}` | [{q}](../OPEN_QUESTIONS.md#{q.lower()}) |' for old,q in sorted(qmap.items())]
mapout += ['\n## Detailed normalized record index\n\n| F-ID | Provenance | Topic |\n|---|---|---|']
mapout += [f'| [{f}](../RAW_FACTS.md#{f.lower()}) | {c} | {title.replace("|","/")} |' for f,c,title in index]
(W/'ID_MAP.md').write_text('\n'.join(mapout)+'\n',encoding='utf-8')
(W/'COLLECTOR_MAP.json').write_text(json.dumps({'sources':smap,'facts':fmap,'questions':qmap,'index':index,'source_facts':{s:sorted(fs) for s,fs in sfacts.items()}},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'source_identities':len(canon),'source_aliases':len(smap),'detail_records':len(records)+6,'fact_aliases':len(fmap),'source_metadata_records':sum(len(x) for x in metas.values()),'missing_source_metadata':[s for s,x in metas.items() if not x]},ensure_ascii=False))
