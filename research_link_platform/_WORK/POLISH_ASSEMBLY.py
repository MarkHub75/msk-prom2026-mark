from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parent.parent;W=R/'_WORK'
data=json.loads((W/'ASSEMBLY_DATA.json').read_text(encoding='utf-8'))
FM=data['fact_alias']
local_sources=[
('S172','W2-D shape/schema helper protocol','W2_D/SCHEMA_PROBE_RESULT.json','W2_D/SCHEMA_PROBE.py',['F239','F333'],'2026-10-23; exact timestamp not asserted','Python-only shape object + AST-extracted pinned normalizer; no NumPy/model/NMS/SDK/device. Printed arithmetic counterexample is source-derived, not torch NMS execution.'),
('S173','W1-10 contract helper and formula protocol','W1_10/CONTRACT_PROBES_RESULT.json','W1_10/CONTRACT_PROBES.py',[FM['W1-10-F02'],FM['W1-10-F04'],FM['W1-10-F06'],'F333'],'2026-10-23; exact timestamp not asserted','NumPy2.4.2 helper dtype/argparse and geometry formulas. No OpenCV pixel interpolation or neural/device execution.'),
('S174','W1-15 isolated historical listing-expression probe','W1_15/STATIC_SOURCE_CHECK.json','W1_15/STATIC_SOURCE_CHECK.py',[FM['W1-15-F05']],'2026-10-23; exact timestamp not asserted','Mock directory names and actual source expression; no native library, device enumeration protocol or hardware inference.')]
sources=(R/'SOURCES.md').read_text(encoding='utf-8')
sources+='\n## Дополнительные прямые локаторы выполненных host probes\n\nЭти записи уточняют происхождение actual_check и не являются новыми внешними источниками.\n'
for sid,title,protocol,script,facts,date,scope in local_sources:
    p=W/protocol;sha=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else 'not found; locator retained from branch'
    # Do not fabricate script presence/name when result file used a different name.
    script_info=f'[_WORK/{script}](_WORK/{script})' if (W/script).exists() else 'Script locator is recorded in the originating RESULT; no existence claim for a guessed filename.'
    sources+=f'\n<a id="{sid.lower()}"></a>\n## {sid} — {title}\n\n- Title/author: {title}; researcher of the indicated branch.\n- Direct local evidence: [_WORK/{protocol}](_WORK/{protocol}); SHA256 `{sha}`. {script_info}\n- Publication/check date: {date}; assembly only read saved evidence.\n- Product/configuration/check scope: {scope}\n- Evidence type: local_observation / isolated helper protocol, not an independent vendor experiment. Availability: actual saved result file read.\n- Facts: '+', '.join(f'[{f}](RAW_FACTS.md#{f.lower()})' for f in facts)+'.\n'
(R/'SOURCES.md').write_text(sources,encoding='utf-8')
raw=(R/'RAW_FACTS.md').read_text(encoding='utf-8')
for sid,title,protocol,script,facts,date,scope in local_sources:
    for fid in facts:
        at=raw.index(f'<a id="{fid.lower()}"></a>')
        m=re.search(r'(?m)^- Sources:.*$',raw[at:])
        if m:
            end=at+m.end();raw=raw[:end]+f'; [{sid}](SOURCES.md#{sid.lower()})'+raw[end:]
# Clarify latest saved rerun without erasing earlier branch timestamp.
at=raw.index('<a id="f247"></a>');pos=raw.index('\n\n',raw.index('- actual_check:',at))
raw=raw[:pos]+'\n- Protocol clarification: latest saved HOST_PROBE_RESULT.JSON timestamp is2026-10-23T02:02:11.352325Z; HOST_PROCESS_RESULT returncode0. Earlier time in branch narrative may refer to an earlier run. b2 remains a recorded Squeeze failure; see [F333](RAW_FACTS.md#f333).'+raw[pos:]
raw=raw.replace('[F093](RAW_FACTS.md#f093)', '[F093](RAW_FACTS.md#f093)')
(R/'RAW_FACTS.md').write_text(raw,encoding='utf-8')
q=(R/'OPEN_QUESTIONS.md').read_text(encoding='utf-8')
start=q.index('<a id="q030"></a>');end=q.index('<a id="q031"></a>')
part=q[start:end].replace('[F093](RAW_FACTS.md#f093)',f'[{FM["W1-07-F07"]}](RAW_FACTS.md#{FM["W1-07-F07"].lower()})')
q=q[:start]+part+q[end:];(R/'OPEN_QUESTIONS.md').write_text(q,encoding='utf-8')

# Prose spacing for the assembler's own shorthand only; never edit original wave
# result text, source code, URLs, or the critic's pre-W2 observations.
dictionary='''actual access allocation accepted activation activations adapter admission after aggregate all allowed anchors annotation api application approved archive artifact artifacts association async author authoritative average backend baseline batch before benign binary bit boundary bounded box boxes buffer buffers budget bytes calibration callback camera cameras candidate canonical capture captured case catalog cell chain check checkpoint chip class classes classic cleanup clear client clip clock close clone code codec color combined common compile compiler completion compute config configuration conflict constant container contract control converter copy correct count coverage cpu current custom data dataset deadline decode decoded decoder default delivery dependency descriptors detect detection device devices diagnostics digest directory distinct documented domain done driver drop dtype effective encoder end environment error errors evaluation event exception execute execution experiment export exporter external factor fail failure false file finite first fixed flag float format frame freeze frontend full generic golden good graph guarantee half hardware hash head helper historical holdout host identity image immutable import importer independent inference info init input inputs inspection internal interval inventory job json kernel label late layer legal library license lifecycle line lineage limit lin link linux load local log logs manifest map mapping mask matching max mean measured measurement memory metadata method minimal missing mixed mock mode model modern monotonic named native network new next no node non normal normalized np nms numerical objects offline onnx only open operations optional ordinary original output outputs owned owner ownership package padding parallel parity participant path payload per percentile physical pinned pixel placement policy post pre precision prepared primary print process profiler program proof protocol public published python quality quant quantization quantized quantizer queue quotas range raw read reader real receive reconnect record recovery reference register registered release remote render replica replicas report request reset resolution response result retained reuse revision rights role round roundtrip route rss rules run runtime safe same sample schema scope score script sdk second separate sequential serial server service session settings shape shared shortcut sigmoid single size skip slot small smoke source split stable stage standard static status stop storage stream strict subtree submit success sufficient supplied supported surviving synthetic target task team tensor terminal test text thread time timestamp tolerance tool topology trace tracking transfer transforms transpose trusted type unchanged unknown unsupported update upload user valid validation value vendor version video view visual wall warm wave weight weights window with without worker workflow whole wrong yaml yes source only namespace no fallback title possible before after mutation lifetime matrix case camera factor exact image model''' .split()
known=set(dictionary)
# Preserve established words in ordinary source prose when they are already
# separated. Restrict size/frequency so accidental long joined tokens do not
# become dictionary entries.
counts={}
for f in sorted(W.glob('W1_*_RESULT.md')):
    for token in re.findall(r'(?<![\w./-])[a-z]{3,15}(?![\w./-])',f.read_text(encoding='utf-8-sig')):
        counts[token]=counts.get(token,0)+1
known.update(t for t,c in counts.items() if c>=3)
known.update(['tpu','tlm','ort','onnx','nms','dfll','df l','qps','pts','nn','os','ram','rtt','rgb','bgr','dtype','nc','abi','bdf','ddr','isa','sku','cpu','gpu','ap','fps','ui','vram','epoch','inflight','outstanding','unavailable','met adata','readonly','preprocess','postprocess','rawheads','userraw','tiny','darknet','pytorch','torch','numpy','tensorflow','ultralytics','default','staging','objectness','bitwise','singlegraph','multichip','multipart','tuple','copy','stats','finite','benign','heldout','quantreference','schema','mean','independent','reproducibility'])

def splitword(token):
    if len(token)<10 or token.lower() in known:return token
    low=token.lower();n=len(low);dp={0:(0,[])}
    for i in range(n):
        if i not in dp:continue
        for j in range(i+2,n+1):
            word=low[i:j]
            if word not in known:continue
            cost=dp[i][0]+1
            if j not in dp or cost<dp[j][0]:dp[j]=(cost,dp[i][1]+[(i,j)])
    if n not in dp or dp[n][0]>6:return token
    return ' '.join(token[a:b] for a,b in dp[n][1])

protect=re.compile(r'(\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://[^\s]+|\b[\w.-]*[_/][\w./:-]*\b|\b[А-ЯЁA-Z0-9_.:-]*\d[А-ЯЁA-Z0-9_.:-]*\b)')
def prose_space(t):
    chunks=protect.split(t)
    for i in range(0,len(chunks),2):
        c=chunks[i]
        c=re.sub(r'([А-Яа-яЁё])([A-Za-z])',r'\1 \2',c)
        c=re.sub(r'([A-Za-z])([А-Яа-яЁё])',r'\1 \2',c)
        c=re.sub(r'([а-яё])([0-9])',r'\1 \2',c)
        c=re.sub(r'([0-9])([а-яё])',r'\1 \2',c)
        c=re.sub(r'([,;:])(?=[A-Za-zА-Яа-яЁё])',r'\1 ',c)
        c=re.sub(r'[A-Za-z]{10,}',lambda m:splitword(m.group(0)),c)
        c=c.replace('→',' → ').replace('≠',' ≠ ')
        chunks[i]=c
    return ''.join(chunks)

for p,marker in [(R/'OPEN_QUESTIONS.md',None),(W/'AUTHOR_HANDOFF.md',None),(R/'RAW_FACTS.md','## Сводные карточки сборщика'),(R/'CRITIC.md','## Фактические dispositions после завершения W2'),(W/'ID_MAP.md','## Cross-wave normalized fact additions')]:
    t=p.read_text(encoding='utf-8');at=t.index(marker) if marker else 0
    prefix=t[:at];own=prose_space(t[at:])
    own=own.replace('171S locatorrecords (166externalURLrecords+5localprotocol/derivedrecords)','174 S locator records (166 external URL records + 8 local protocol/derived records)')
    own=own.replace('171 S locator records (166 external URL records+5 local protocol/derived records)','174 S locator records (166 external URL records + 8 local protocol/derived records)')
    p.write_text(prefix+own,encoding='utf-8')

# Explicit count and artifact boundary in readable prose supersede shorthand.
p=W/'AUTHOR_HANDOFF.md';t=p.read_text(encoding='utf-8')
t+='''

## Финальный паспорт сборки

Сохранены 174 S-карточки: 166 нормализованных внешних URL и 8 локальных протоколов или производных выписок. Это число локаторов, а не независимых источников или экспериментов. База содержит 333 F-карточки: 306 исходных факт-записей веток, 20 подробных матриц веток и 7 сводных карточек сборщика. Повторные наблюдения одного исходника намеренно сохраняют историю и не повышают силу доказательства. Дополнительно: 35 Q, 20 E, 8 R и 20 K-dispositions.

Есть реальные публичные CPU-проверки ONNX Runtime 1.31.0, сравнение весов и изолированные Python helper/mock-пробы. Никакая установка proprietary SDK, vendor conversion/calibration/compile/TLM или inference на LinQ не выполнены. Пользователь не сообщил исход регистрации. Автор должен сохранить эти границы в начале обоих отчётов и рядом с техническими результатами.

Дополнительные прямые S локальных probes: S172 — W2-D shape/schema; S173 — W1-10 dtype/geometry/argparse; S174 — W1-15 listing-expression. Их bytes прочитаны, новые проверки модели не запускались. Сводный источник actual checks — F333.
'''
p.write_text(t,encoding='utf-8')
p=W/'ID_MAP.md';t=p.read_text(encoding='utf-8');t+='\n\n## Additional local protocol sources\n\n| Local protocol | Global |\n|---|---|\n'
for sid,title,protocol,*_ in local_sources:t+=f'| _WORK/{protocol} | {sid} |\n'
p.write_text(t,encoding='utf-8')
print('Polished own prose; added S172-S174. Stable total:174S/333F/35Q/20E/8R/20K.')
