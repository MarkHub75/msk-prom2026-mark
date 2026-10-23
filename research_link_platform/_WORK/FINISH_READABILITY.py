from pathlib import Path
import re,json
R=Path(__file__).resolve().parent.parent;W=R/'_WORK'
ru={};en={}
for p in W.glob('W1_*_RESULT.md'):
    t=p.read_text(encoding='utf-8-sig')
    for v in re.findall(r'(?<!\w)[А-Яа-яЁё]{2,24}(?!\w)',t):ru[v.lower()]=ru.get(v.lower(),0)+1
    for v in re.findall(r'(?<!\w)[A-Za-z]{2,18}(?!\w)',t):en[v.lower()]=en.get(v.lower(),0)+1
ru=set(v for v,c in ru.items() if c>=2)|set('и в с к о у а не ни но по до на при без из после для либо это как что один одной свои только также отдельно достаточно фактически неизвестно неизвестны получил получен получили поставка поставки потребляет передаёт сохраняемые артефакты источником статусом роль роли этой этойролью узкий'.split())
en=set(v for v,c in en.items() if c>=2)|set('actual access device grant user outcome unreported scope only current modern source choice patch raw decoded old new class nc vs pipeline already exists here no accepted vendor public synthetic metadata checked host native library test protocol result bytes input output final source strict not exported valid unknown release mismatches callback thread evidence limit life cycle shape mode inference graph copy backing retained exception destroy omission mock validation first frame small object size quality in place update ready accepted proof before after post pre outstanding input family direct prior claim party hardware whole correct request correlation instance line axis compile weight kernel record ids last avg max returned data stream worker immutable detected hash same state child role permanent setting index rule tracking tool chain manifest environment timing field elapsed missing dependency false alarm sdk words docs stage encoder root'.split())
def split(t,words,minimum):
    if len(t)<minimum or t.lower() in words:return t
    low=t.lower();n=len(t);dp={0:(0,[])}
    for i in range(n):
        if i not in dp:continue
        for j in range(i+1,n+1):
            if low[i:j] not in words:continue
            cost=dp[i][0]+1
            if j not in dp or cost<dp[j][0]:dp[j]=(cost,dp[i][1]+[(i,j)])
    if n not in dp or dp[n][0]>8:return t
    return ' '.join(t[a:b] for a,b in dp[n][1])

protected=re.compile(r'(\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://[^\s]+)')
def clean(t):
    parts=protected.split(t)
    for i in range(0,len(parts),2):
        c=parts[i]
        c=re.sub(r'([А-Яа-яЁё])([A-Za-z])',r'\1 \2',c)
        c=re.sub(r'([A-Za-z])([А-Яа-яЁё])',r'\1 \2',c)
        c=re.sub(r'[А-Яа-яЁё]{5,}',lambda m:split(m.group(0),ru,5),c)
        c=re.sub(r'[A-Za-z]{9,}',lambda m:split(m.group(0),en,9),c)
        c=re.sub(r'([,;:])(?=[A-Za-zА-Яа-яЁё])',r'\1 ',c)
        c=re.sub(r'(?<=[A-Za-zА-Яа-яЁё])(?=\[F\d{3}\])',' ',c)
        c=c.replace('Type Error','TypeError').replace('Tpu Program','TpuProgram').replace('Regular Model','RegularModel').replace('Quantized Model','QuantizedModel').replace('Tensor Description','TensorDescription')
        c=re.sub(' +→ +',' → ',c)
        parts[i]=c
    return ''.join(parts)
for p,mark in [(R/'OPEN_QUESTIONS.md',None),(W/'AUTHOR_HANDOFF.md',None),(R/'RAW_FACTS.md','## Сводные карточки сборщика'),(R/'CRITIC.md','## Фактические dispositions после завершения W2'),(W/'ID_MAP.md','## Cross-wave normalized fact additions')]:
    t=p.read_text(encoding='utf-8');at=t.index(mark) if mark else 0;p.write_text(t[:at]+clean(t[at:]),encoding='utf-8')

# Replace the author's entry prose with plain text; detailed matrices remain.
p=W/'AUTHOR_HANDOFF.md';t=p.read_text(encoding='utf-8');a=t.index('\n\n');b=t.index('## Быстрый')
t=t[:a]+'''

Сборщик использовал 15 результатов W1, 13 результатов W2, исходную критику и сохранённые первичные материалы и протоколы. Нового внешнего поиска, третьей волны, делегирования и отдельного аудита нет. Отчёты пишет следующий автор. Модель этой роли — gpt-6.1-sol/high. Позднее уточнение RUN_STATE: пользовательский screenshot показал GPT-6.1-Sol high у root; раннюю неопределённость настройки не повторять как постоянную. Все роли исследователей были явно назначены medium, аналитические роли — high.

'''+t[b:]
a=t.index('## Рекомендуемая логика');b=t.index('## Единые manifests')
t=t[:a]+'''## Рекомендуемая логика человеческого отчёта

Начать с результата: публичные документы и исходники позволяют восстановить путь модели и границы интеграции, но actual release и контракт доступа сильнее всего меняют архитектуру. Порядок объяснения: продукты и версии → путь артефакта → custom detector и контраст TinyYOLO3 → квантование и численные границы → runtime и доказательство исполнения → видео и условные маршруты → производительность → первые часы, эксперименты и вопросы. Источник и статус держать рядом с числами и командами.

Человеческий отчёт нужен на русском, подробный и связный. Машинный — на английском, с YAML-полями из section17 исходного prompt: вопросы answers, entity_schema, актуальность, SDK access, actual tested_here и связанные файлы. В tested_here включить реальные публичные CPU ONNX-пробы, сравнение весов и helper/mock tests; явно отделить отсутствующие vendor compile/LinQ runs. Не объявлять known-good vendor artifact или TLM обязательными во всех маршрутах. Неизвестное не означает unsupported. Редактор улучшает текст, затем работает compressor; нового сетевого поиска и отдельного финального аудитора нет.

'''+t[b:]
# Remove stale shorthand count paragraph now superseded by final passport.
t=re.sub(r'Счётчикнаконецсборки:.*?(?=\n\n|\Z)','',t,flags=re.S)
t=t.replace('Счётчик на конец сборки:171','Счётчик на конец сборки:174')
p.write_text(t,encoding='utf-8')

# Assembly consistency checks: local anchors only, no new evidence or role.
names=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md','_WORK/AUTHOR_HANDOFF.md','_WORK/ID_MAP.md']
anchors={n:set(re.findall(r'<a id="([^"]+)"',(R/n).read_text(encoding='utf-8'))) for n in names}
bad=[]
for n in names:
    t=(R/n).read_text(encoding='utf-8')
    for path,a in re.findall(r'\]\(([^)#]+)#([^ )]+)\)',t):
        dest=((R/n).parent/path).resolve()
        try:rel=dest.relative_to(R).as_posix()
        except ValueError:continue
        if rel in anchors and a not in anchors[rel]:bad.append([n,path,a])
result={'anchors':{n:len(a) for n,a in anchors.items()},'bad_local_anchor_links':bad,'artifact_bytes':{n:(R/n).stat().st_size for n in names}}
(W/'ASSEMBLY_LINK_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
