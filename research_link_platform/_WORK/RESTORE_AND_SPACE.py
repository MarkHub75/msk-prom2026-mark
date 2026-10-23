from pathlib import Path
import runpy,re,json
R=Path(__file__).resolve().parent.parent;W=R/'_WORK'
p=R/'CRITIC.md';t=p.read_text(encoding='utf-8');t=t.split('## Фактические dispositions после завершения W2')[0].rstrip()+'\n';p.write_text(t,encoding='utf-8')
runpy.run_path(str(W/'ASSEMBLE_EVIDENCE.py'))
runpy.run_path(str(W/'FINALIZE_ASSEMBLY.py'))
runpy.run_path(str(W/'POLISH_ASSEMBLY.py'))

# Only deterministic spacing edits. Never segment Russian words algorithmically.
pairs='''devicegrant|device grant
useroutcomeunreported|user outcome unreported
currentrelease|current release
currentinstall|current install
actualrelease|actual release
actualartifact|actual artifact
actualregistrytag|actual registry tag
actualscalingunknown|actual scaling unknown
signupoutcome|signup outcome
customrunner|custom runner
customPPE|custom PPE
hoststages|host stages
compiletarget|compile target
Versionedbundle|Versioned bundle
wheelhouse|wheelhouse
matchedartifact|matched artifact
matchedbundle|matched bundle
missingdependency|missing dependency
ctypespairing|ctypes pairing
Cloudclaims|Cloud claims
workingcall|working call
servicegrant|service grant
sourcepre|source pre
negativegolden|negative golden
nooutputs|no outputs
maxpayload|max payload
sharedqueue|shared queue
modelAPI|model API
cameraadmission|camera admission
placementUI|placement UI
Issuedlimits|Issued limits
documentedterminalstates|documented terminal states
TensorAPI|Tensor API
nopersistence|no persistence
timeoutwithoutcancel|timeout without cancel
requestcompletion|request completion
acceptedwitness|accepted witness
vendorpin|vendor pin
accesscontract|access contract
publicguide|public guide
devicepermissions|device permissions
longrunning|long-running
boundedinflight|bounded in-flight
boundedqueue|bounded queue
hostboundariesconditional|host boundaries conditional
header/native|header/native
CPUcompileonlyfuture|CPU-only compile is a future check
Genlinkconflicts|Gen link conflicts
sourcechoice|source choice
inputpatch|input patch
compilecallopen|compile call remains open
NMSimportversion|NMS import version
outputname|output name
inplace|in place
viewbackingretained|view backing retained
exceptiondestroyomissionmockonly|exception destroy omission: mock only
unknownnamevalidation|unknown-name validation
Moderntext|Modern text
onlyunitsunresolved|only; units unresolved
newwrapperrates|new wrapper rates
purearith|pure arithmetic
oldasync|old async
butmoderncontractunknown|but modern contract unknown
noresetcommands|no reset commands
codeclocation|codec location
DirectONNXcurrent|Current direct ONNX
known-goodvendorfile|known-good vendor file
stageplacement|stage placement
rawoutputcontract|raw output contract
modelmanifest|model manifest
environmentmanifest|environment manifest
incidentpacket|incident packet
frameidentity|frame identity
frameassociation|frame association
eventassociation|event association
percamera|per camera
perrequest|per request
wholerequest|whole request
samepreparedinputs|same prepared inputs
sharedmodel|shared model
nativeerror|native error
historicalexception|historical exception
pre-submitapplication|pre-submit application
ordinaryexception|ordinary exception
terminalcompletion|terminal completion
posterror|post-error
same-sessionretry|same-session retry
newworker|new worker
rawheads|raw heads
ModelZoo|Model Zoo
Tinybinary|Tiny binary
vendorunknown|vendor unknown
strictnotexported|strict not exported
Percentilescope|Percentile scope
effectiveunknown|effective unknown
holdoutpercamera|holdout per camera
HardwareNetwork|HardwareNetwork
noTypeErrorretry|no TypeError retry
literalLinQ|literal LinQ
PPEmanifest|PPE manifest
NNboundary|NN boundary
documentedsource|documented source
opset13|opset13
capturedstream|captured stream
Oneclippreparedtensorsvsrealdecode|One clip: prepared tensors vs real decode
Onegraphpartitionmanifest|One graph partition manifest
OneDataManifestcamera|One DATA_MANIFEST: camera
ActualLinQallocation|Actual LinQ allocation
Actualsupportedtopology|Actual supported topology
Deviceabsenttopology|Device-absent topology
Capturefirsterror|Capture first error
normalbaseline|normal baseline
currentruntimecontract|current runtime contract
APIwall|API wall time
commonsteadywindow|common steady window
commonwindowcompletedrealimages|common window: completed real images
samepreparedtensor|same prepared tensor
Samepreparedtensor|Same prepared tensor
currentcoverage|current coverage
oldexamples|old examples
Currentlifetime|Current lifetime
type(return)|type(return)
source-only/helper|source-only/helper
невыдумывать|не выдумывать
невыполнялись|не выполнялись
неполучены|не получены
неполучен|не получен
невыданы|не выданы
неустановлены|не установлены
невизуально|не визуально
неподтвердилась|не подтвердилась
неперебирать|не перебирать
неприменим|не применим
необъявлять|не объявлять
неостанавливает|не останавливает
неизпубличного|не из публичного
невыводятсяизпубличногопредложения|не выводятся из публичного предложения
можетбытьдостаточен|может быть достаточен
проверитьдостаточность|проверить достаточность
безповторного|без повторного
вместоготового|вместо готового
по-прежнемуусловный|по-прежнему условный
неавтоматически|не автоматически
сохраняемыеартефакты|сохраняемые артефакты
пределдоказательства|предел доказательства
отдельнодоступные|отдельно доступные
покаждымслоям|по каждому слою
непутать|не путать
ненорма|не норма
непотолок|не потолок
двазвена|два звена
видеонепросмотрено|видео не просмотрено
проверитьcodec|проверить codec
сня тдля|снят для
снятдля|снят для
исходнойкритику|исходную критику
неединый|не единый
неодин|не один
неэквивалент|не эквивалент
поspec|по spec
ккамерам|к камерам
человеческийотчёт|человеческий отчёт
Счётчикнаконецсборки|Счётчик на конец сборки'''
mapping=[line.split('|',1) for line in pairs.splitlines() if '|' in line]
protect=re.compile(r'(\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://[^\s]+)')
def clean(t):
    parts=protect.split(t)
    for i in range(0,len(parts),2):
        c=parts[i]
        c=re.sub(r'([А-Яа-яЁё])([A-Za-z])',r'\1 \2',c)
        c=re.sub(r'([A-Za-z])([А-Яа-яЁё])',r'\1 \2',c)
        for a,b in mapping:c=c.replace(a,b)
        c=re.sub(r'([,;:])(?=[A-Za-zА-Яа-яЁё])',r'\1 ',c)
        c=c.replace('Type Error','TypeError').replace('Tpu Program','TpuProgram').replace('Batch Normalization','BatchNormalization')
        c=re.sub(' +→ +',' → ',c)
        parts[i]=c
    return ''.join(parts)
for p,marker in [(R/'OPEN_QUESTIONS.md',None),(W/'AUTHOR_HANDOFF.md',None),(R/'RAW_FACTS.md','## Сводные карточки сборщика'),(R/'CRITIC.md','## Фактические dispositions после завершения W2'),(W/'ID_MAP.md','## Cross-wave normalized fact additions')]:
    t=p.read_text(encoding='utf-8');at=t.index(marker) if marker else 0;p.write_text(t[:at]+clean(t[at:]),encoding='utf-8')

p=W/'AUTHOR_HANDOFF.md';t=p.read_text(encoding='utf-8');a=t.index('\n\n');b=t.index('## Быстрый')
t=t[:a]+'''

Сборщик использовал 15 результатов W1, 13 результатов W2, исходную критику и сохранённые первичные материалы и протоколы. Нового внешнего поиска, третьей волны, делегирования и отдельного аудита нет. Отчёты пишет следующий автор. Модель этой роли — gpt-6.1-sol/high. Позднее уточнение RUN_STATE: пользовательский screenshot показал GPT-6.1-Sol high у root; раннюю неопределённость настройки не повторять как постоянную. Все роли исследователей были явно назначены medium, аналитические роли — high.

'''+t[b:]
a=t.index('## Рекомендуемая логика');b=t.index('## Единые manifests')
t=t[:a]+'''## Рекомендуемая логика человеческого отчёта

Начать с результата: публичные документы и исходники позволяют восстановить путь модели и границы интеграции, но actual release и контракт доступа сильнее всего меняют архитектуру. Порядок объяснения: продукты и версии → путь артефакта → custom detector и контраст TinyYOLO3 → квантование и численные границы → runtime и доказательство исполнения → видео и условные маршруты → производительность → первые часы, эксперименты и вопросы. Источник и статус держать рядом с числами и командами.

Человеческий отчёт нужен на русском, подробный и связный. Машинный — на английском, с YAML-полями из section17 исходного prompt: questions/answers, entity_schema, актуальность, SDK access, actual tested_here и связанные файлы. В tested_here включить реальные публичные CPU ONNX-пробы, сравнение весов и helper/mock tests; явно отделить отсутствующие vendor compile/LinQ runs. Не объявлять known-good vendor artifact или TLM обязательными во всех маршрутах. Неизвестное не означает unsupported. Редактор улучшает текст, затем работает compressor; нового сетевого поиска и отдельного финального аудитора нет.

'''+t[b:]
t=re.sub(r'Счётчик на конец сборки:.*?(?=\n\n|\Z)','',t,flags=re.S)
p.write_text(t,encoding='utf-8')

# Exact operator literals from saved GRAPH.JSON, protected as code.
p=R/'RAW_FACTS.md';t=p.read_text(encoding='utf-8');a=t.index('<a id="f328"></a>');b=t.index('<a id="f329"></a>');chunk=t[a:b]
graph=json.loads((W/'W2_E/GRAPH.JSON').read_text(encoding='utf-8'))
counts='; '.join(f'`{k}`={v}' for k,v in graph['ops'].items())
chunk=re.sub(r'Exact original graph counts:.*?\. Это inventory',f'Exact original graph counts: {counts}. Это inventory',chunk,flags=re.S)
t=t[:a]+chunk+t[b:];p.write_text(t,encoding='utf-8')

names=['SOURCES.md','RAW_FACTS.md','OPEN_QUESTIONS.md','CRITIC.md','_WORK/AUTHOR_HANDOFF.md','_WORK/ID_MAP.md']
anchors={n:set(re.findall(r'<a id="([^"]+)"',(R/n).read_text(encoding='utf-8'))) for n in names};bad=[]
for n in names:
    for path,a in re.findall(r'\]\(([^)#]+)#([^ )]+)\)',(R/n).read_text(encoding='utf-8')):
        try:rel=((R/n).parent/path).resolve().relative_to(R).as_posix()
        except ValueError:continue
        if rel in anchors and a not in anchors[rel]:bad.append([n,path,a])
result={'anchors':{n:len(v) for n,v in anchors.items()},'bad_local_anchor_links':bad,'artifact_bytes':{n:(R/n).stat().st_size for n in names}}
(W/'ASSEMBLY_LINK_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
