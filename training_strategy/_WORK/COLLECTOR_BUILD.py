
from pathlib import Path
import re,json
root=Path(__file__).resolve().parents[1]
docs={f'{p.parent.name}-{p.name[:2]}':{'p':p,'text':p.read_text(encoding='utf-8-sig'),'lines':p.read_text(encoding='utf-8-sig').splitlines()} for p in sorted(root.glob('_WORK/W[12]/*.md'))}
def definition(line,b,t):
    # Every explicit heading/bold/first table cell, never an inline citation.
    if not re.match(r'^(?:#{1,4}\s|\*\*|\|\s*)',line): return []
    m=re.match(r'^(?:#{1,4}\s+(?:\d+\.\s+)?|\*\*|\|\s*)'+re.escape(b)+r'-'+t+r'(\d{2})',line)
    if not m:
        if t=='F' and b=='W1-08' and re.match(r'^### '+b+r'-S\d{2} / '+b+r'-F\d{2}',line):
            return re.findall(b+r'-F\d{2}',line)
        return []
    ids=[b+'-'+t+m.group(1)]
    # Joint definition e.g. F08/F09.
    suffix=line[m.end():]
    mm=re.match(r'/(?:'+re.escape(b)+r'-)?'+t+r'(\d{2})',suffix)
    if mm: ids.append(b+'-'+t+mm.group(1))
    return ids
sources={};facts={};exps={};questions={};extras={}
for b,d in docs.items():
    ls=d['lines']; markers=[]
    for i,l in enumerate(ls):
        for t in 'SFE':
            ids=definition(l,b,t)
            if ids: markers.append((i,t,ids))
    for i,t,ids in markers:
        # sources represented as table row are only one line
        if t=='S' and ls[i].startswith('|'):
            end=i+1
        else:
            candidates=[j for j,tt,ii in markers if j>i]
            candidates += [j for j in range(i+1,len(ls)) if re.match(r'^#{1,2}\s',ls[j])]
            # source ends at next heading too; F/E allow nested h3 inside procedure
            if t=='S': candidates += [j for j in range(i+1,len(ls)) if re.match(r'^### ',ls[j])]
            end=min(candidates,default=len(ls))
        block='\n'.join(ls[i:end]).strip()
        if t=='S' and b=='W1-08':
            # metadata only; the remainder is retained in its fact entry
            paras=block.split('\n\n')
            block='\n\n'.join(paras[:2])
        for ident in ids:
            (sources if t=='S' else facts if t=='F' else exps)[ident]={'b':b,'start':i,'end':end,'body':block,'path':str(d['p'].relative_to(root)).replace('\\','/')}
    # unnumbered questions tables/bullets; exact per-question block
    qstarts=[(i,re.search(b+r'-Q\d{2}',l).group()) for i,l in enumerate(ls) if re.match(r'^(?:\|\s*|- \*\*|\*\*)'+b+r'-Q\d{2}',l)]
    for z,(i,qid) in enumerate(qstarts):
        end=i+1 if ls[i].startswith('|') else min([j for j in range(i+1,len(ls)) if re.match(r'^#{1,3}\s',ls[j])]+[jj for jj,qq in qstarts if jj>i],default=len(ls))
        questions[qid]={'b':b,'body':'\n'.join(ls[i:end]).strip(),'path':str(d['p'].relative_to(root)).replace('\\','/')}
    # W2-09 has bold headings with em dash rather than exact beginning? covered bold.
    used=set()
    for coll in (sources,facts,exps):
        for v in coll.values():
            if v['b']==b: used.update(range(v['start'],v['end']))
    secs=[]
    hs=[i for i,l in enumerate(ls) if re.match(r'^## ',l)]+[len(ls)]
    for hi,he in zip(hs,hs[1:]):
        title=ls[hi]
        if re.search(r'источник|вопрос|передач|доступ|остаточ|заверш|примечан|факт|процедур|E-проц|K\d+ outcome',title,re.I): continue
        remain='\n'.join(l for i,l in enumerate(ls[hi:he],hi) if i not in used).strip()
        if len(remain)>200: secs.append(remain)
    extras[b]=secs


from datetime import datetime
now=datetime.now().astimezone().isoformat(timespec='seconds')
fact_groups=[
['W1-02-F01','W1-03-F03'],['W1-02-F02','W1-03-F02','W1-15-F01'],
['W1-04-F10','W1-12-F08'],['W1-05-F06','W1-11-F14'],
['W1-14-F10','W1-15-F03'],['W1-13-F08','W1-13-F09'],['W2-01-F07','W2-11-F07']]
exp_groups=[
['W1-01-E03','W1-06-E01'],['W1-08-E02','W1-10-E01'],['W1-13-E01','W1-15-E04'],
['W1-03-E02','W2-02-E01'],['W1-09-E03','W2-03-E01'],['W1-08-E01','W2-04-E01'],
['W1-09-E01','W2-05-E01'],['W1-07-E02','W2-07-E01'],['W1-11-E02','W2-08-E01'],
['W1-12-E03','W2-11-E01'],['W1-10-E02','W2-01-E01']]
def grouped(coll,groups,prefix):
    lookup={k:g for g in groups for k in g}; result={}; m={};done=set()
    for k in coll:
        if k in done:continue
        group=[x for x in lookup.get(k,[k]) if x in coll]; ident=f'{prefix}{len(result)+1:03}'
        result[ident]=group
        for x in group:m[x]=ident;done.add(x)
    return m,result
fmap,fgroups=grouped(facts,fact_groups,'F');emap,egroups=grouped(exps,exp_groups,'E')
def urls(t): return [x.rstrip('.,;:') for x in re.findall(r'https?://[^\s<>\x60|)]+',t)]
def canon(url):
    url=url.split('#')[0].rstrip('/')
    return re.sub(r'https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.*)',r'https://github.com/\1/\2/blob/\3/\4',url)
def primary(v):
    us=urls(v['body']); valid=[u for u in us if 'api.github.com' not in u]
    return canon((valid or us or [v['path']])[0])
smap={};sgroups={'S001':['INPUT-CONTEXT']};keys={}
for k,v in sources.items():
    key=primary(v)
    if key not in keys:keys[key]=f'S{len(sgroups)+1:03}';sgroups[keys[key]]=[]
    gid=keys[key];smap[k]=gid;sgroups[gid].append(k)
q_assign={
'W1-01':[1,3,5,7,29,10],'W1-02':[5,4,6,14,7,14],'W1-03':[3,13,4,1,30,7],
'W1-04':[10,6,3,4,10,13,7],'W1-05':[1,6,17,10,29,19],'W1-06':[17,7,17,10,9,30],
'W1-07':[2,3,3,21,10,5,7],'W1-08':[4,1,16,12,16,6],'W1-09':[1,21,11,30,7,29],
'W1-10':[6,11,1,7,30,30,27],'W1-11':[1,19,4,19,20,29,7],
'W1-12':[6,3,10,27,17,31,14],'W1-13':[7,8,3,9,23,9],
'W1-14':[27,27,12,26,27,27,27],'W1-15':[10,4,25,26,29,31,27],
'W2-01':[5,11,7,6,30],'W2-02':[3,13,13,13],'W2-03':[21,21,2,11,7,21],
'W2-04':[6,2,16,16,7],'W2-05':[10,4,11,13],'W2-06':[5,15,30,2,7],
'W2-07':[22,22,22,2,22,7],'W2-08':[20,19,19,7],'W2-09':[23,8,4],
'W2-10':[24,24,7,24,24],'W2-11':[10,25,25,7],'W2-12':[10,6,7,27,28,27]}
qinfo=[
('P0','Ontology объектов, состояний и событий; visibility/unknown/ignore','Кейс/постановщик + annotation guideline','Примеры СИЗ, зон и курения не задают полный mandatory vocabulary. Object/носит/отсутствует/не видно не одно понятие.','Входы; W1-01/03/05/06/11; W2-02/05/06','Согласовать definitions с positive/negative/ambiguous примерами до разметки.'),
('P0','Разрешённое unlabelled exposure и независимый test','Кейс/постановщик + manifests','BN statistics, embeddings, backgrounds, pseudo mining и pretraining тоже exposure. Разрешение не получено.','W1-07-F10; W1-08-E01; W2-06/07/12','Получить правило кейса и роли каждого camera/time group; выбирает SSL/SFOD/pretraining и transfer claim.'),
('P0','Source×class coverage, verified negatives, sparse instances и ROI','Original annotations + ручной audit','TXT missing/empty дают zero rows; ordinary conversion теряет verified/crowd/coverage. Штатный U не partial-aware.','W1-03/04/12; W2-02','Получить originals/coverage до union; различить hidden class B и hidden instance C.'),
('P0','Независимые камеры/сессии/эпизоды и rare support','Данные + split/duplicate audit + полный GT','Boxes/frames не independent groups. N/A не ноль; target inventory отсутствует.','W1-03/07/15; W2-05','Grouped splits/counts objects/events/camera-hours/blind GT; выбирает claim и необходимость доразметки.'),
('P0','Фактические обучаемые checkpoints: provenance, classes, rights, unfused state','Artifact/manifest + loader smoke','Публичные links/metadata и wheel есть; выбранных target weights нет. URL не вес и не разрешение использования.','W1-02/03/07/10; W2-01/06/07','Получить bytes/hash/YAML/ancestry/class definitions/licence, transfer tensor inventory.'),
('P0','Выбранный package/dependency lock и trainer runtime','Artifact + inventory + bounded smoke','U8.4.184 исследован, wheel10файлов сверены. Это не installation test. Docs PyTorch2.14 не версия команды.','W1-02/05/08/12/14; W2-01/04/11','Pin OS/Python/torch/CUDA/driver/GPU/VRAM/dependencies, actual criterion/head и finite update/reload.'),
('P0','LinQ device/SDK build и accepted graph/input/export','SDK/доступ + compile/run','Vendor называет yolo5s/yolo8/yolo11,int8,Compiler/DNN Quant. Exact устройство/SDK/opset/shapes/postprocess не получены.','W1-13-S11/S12; W2-01/03/09/10','Получить versioned guide/sample/operator-shape matrix; выполнить selected artifact на LinQ.'),
('P0','Quant import/arithmetic: DNN Quant, QDQ/QOperator, ranges/axes/fusion','SDK/sample + numerical boundary tests','ORT/NVIDIA reference установлены; arithmetic match LinQ неизвестен. QAT graph может быть отвергнут/перекалиброван.','W1-13; W2-09-Q02','Signedness/range/rounding/zp/axes/accumulator/bias/requant, scale-sharing/fusion/exclusions и accepted sample.'),
('P0','Placement/fallback и model/end-to-end latency/memory','SDK profiler + target measurement','FLOPs/MACs/INT8/compiled file не execution или acceleration. Network/decode/queue/crops могут доминировать.','W1-06/13/14; W2-09/10/12','Placement/precision/fallback logs, fixed timing boundary, p50/p95/throughput/calls/exposure.'),
('P0','Constrained objective: critical recall/FP/margins/selection/tie/stop','Кейс + evaluation + baseline','AP-best=EMA AP50:95, не event/rare objective. Numerical margins/sample floors не установлены.','W1-04/15; W2-05/11/12','Primary/delta_min/epsilon/R_min/FP exposure/tie/candidate budget до tuning; решает promote/rollback.'),
('P0 перед unchecked/KD','Качество teacher и допуск pseudo labels по class×size×camera','Blind complete audit + independent confirmation','Calibration не восстанавливает no-detection misses; precision без retained recall/localization/support недостаточна.','W1-09/10; W2-01/03/05','Frozen score/IoU/matching/cutoff, P probability+D diagnostics отдельно, confirmation; выбирает assistance/review/unchecked/KD.'),
('P1','Полная human cost manual/preannotation/selection/QA','Randomized matched cost pilot','Images/objects/clicks не person-minutes. CVAT imported/interpolated/net counters не минуты/сцены.','W1-08/10/14; W2-04/05','Selection+draw/correct+miss search+review/adjudicate+export QA, annotator/order; выбирает teacher/AL/manual.'),
('P0 для partial','Coverage/ignore mechanism выбранного assignment/loss','Implementation artifact + A/B/C gradient gate','B U-objectness-free допускает custom class validity; C spatial policy, legacy objectness и обеE2E branches отдельно. MMDet defaults off/zero-GT limit.','W1-03-E02; W2-02','Metadata/transforms/assignment/unreduced losses/gradients, positive precedence и denominator; сравнить доразметку.'),
('P1','Target trainable mask, BN/freeze/full/staged optimum','Controlled comparison + buffer/update audit','TFA predictor-only не YOLO freeze. U freeze BN eval, manual mask может быть отменена; freeze разрешён resume, новый LR нет.','W1-02/12; W2-11','Один target init, actual masks/groups/stats; limited vs full, BN/staged только при причине.'),
('P1','Detector-specific tensors сверх одинакового backbone','Artifact + matched initialization trial','DetCo/DETReg transfer components различны; base stage/schedule/exposure confounds. Artifact не pretraining с нуля.','W2-06','Identical backbone/head state, только detector tensors отличаются, target/retention/compute.'),
('P1; raw P2','Minimal acquisition usefulness и raw/vector interfaces','Output smoke + equal-human-minutes trial','Results xyxy/conf/cls,probs=None. Low-confidence не entropy. No-box exploration входит proposed policy.','W1-08; W2-04','Records/caps/time/rank; одна arm vs stratified random. Raw/hooks/embeddings только по отдельной нужде.'),
('P0 при tiny failure','Визуальный сигнал/scale/crop/cascade и системная цена','Native→actual input audit + inference comparison','Resize не создаёт информацию; cascade recall≤usable-crop coverage. SAHI AP50 не AP50:95, recipe revisions различны.','W1-01/06; W2-12','Pixel/visibility audit, один большийinput либо predicted cascade с upstream misses; target shapes/calls/latency.'),
('P1','Польза и semantics аугментаций','Dataloader replay/survival + real ablation','Defaults не optimum; bbox-only CopyPaste no-op, erasing classification; Alb2.0.8 signatures не live.','W1-05/06','Before/after labels/relations/ROI/temporal/evidence; clean/real degraded, один intervention.'),
('P1','Synthetic assets/masks/relations/review и real transfer','Assets/ontology + semantic gate + real comparison','Prompt не GT; occlusion не no_PPE. Fully reviewed data-only route конкретен, benefit неизвестен.','W1-11; W2-08','Whole-frame review/train-only provenance; updates/real/synthetic draw ledger и independent real holdout.'),
('P1 conditional','Gen2Det author fork/config/schema и actual loss','Новый primary artifact; затем correctness test','После paper/author pages/GitHub exact search code не найден, это не отсутствие capability. p whole batches,tau_i0 synthetic bg RPN+head,lowdata иной.','W2-08 S01–S04/search log','Author fork+commit/filter/sample schema/empty/assignment/reduction/sampling/final graph; до этого reviewed route.'),
('P1 conditional','One-stage online SSOD loop/state/extraction exact family','Artifact lock + correctness/extraction smoke','UTv2 std остаётся eval field/teacher default. ET active YOLOv5, onlineEMA/secondary/best/export различны, raw decoder/domain heads.','W2-03','Один compatible route; geometry/empty/mixed/nohiddenGT/branch hashes/extraction/export, затем supervised comparison.'),
('P2','Source-free artifact и BN/eval/JSON/hook/selection','Compatible checkpoint + bounded smoke + labeled V','simple-SFOD code есть, local weights; eval-only меняет BN, manualJSON/sourcevalhook risk. Fixed-row selection gap.','W2-07','Exact source detector, frozen eval buffers, U-only AdaBN/explicitJSON/no sourceGT hooks; V selection/H.'),
('P1 conditional','Detector QAT lock/export artifact/architecture','Artifact lock/sample + parity smoke','YOLOv7 featureMSE/noGT route; historical YOLO/toolkit не pinned. Reference2.1.2 не installed author env.','W2-09','Container/package/source/weight/ONNX hashes, ranges/export outputs/SDK; supervisedport назвать новым.'),
('P2','Physical pruning old topology/recovery/usefulness','Custom artifact + conversion/reload/export smoke','TP1.6.1/U8.0.90/C2f_v2/patchedtrainer/fullobject; YAML+state_dict не topology; MACratio не latency, no rollback.','W2-10','Conversion parity/customimport/headclass/compile доrecovery; native smaller comparator, actual target timing.'),
('P0 training; exact P1','Immutable candidate saver/evaluator/resume/stages','Callback/evaluator + fresh-process smoke','on_model_save доstrip; prestrip EMA, online/RNG/loader/scheduler нет; booleanresume может стать warmstart.','W2-11','Copy/hash ledger/save/val/pathbasedeval; explicit prestripresume vs newstage resumeFalse; exactstate требует иного saver.'),
('P1','Paired/group uncertainty и repeat/sample/split design','Данные + evaluation estimator','Sample/optimizer/split/resampling seeds различны. Degenerate/zero support CI unavailable; seeds не новые scenes.','W1-15; W2-05/12','Hierarchy/estimand/paired groups/all repeats/cap; при нехватке independent support нужны новые группы.'),
('P0 scheduling','Resource costs/D_useful/ownership/critical path','Inventory + bounded profile/time + owner','RTX4070 не VRAM/минуты. DDP не объединяет память; setup/validation/save/export/review могут доминировать.','W1-14; W2-11/12','Stage timestamps/headroom/personminutes/GPUhours/queue; admit now+CP_remaining<=D_useful.'),
('P2; no proxy default','Early quality proxy для immutable full recipe','Full histories + dev rank-reversal analysis','Hyperband/ASHA не detector-ranking guarantee. ShortU меняет auto/warmup/schedule/mosaic, resume не exactprefix.','W2-12','Short runs correctness-only; proxy при самостоятельной нужде/историях/support/полном artifact deadline.'),
('P0 event error','Object/association/temporal attribution и trace interface','Кейс + stage logs/oracle substitution','BoxAP не wearing/zone/smoking event. Сохраняющаяся с oracle objects ошибка не основание detectortraining.','W1-01-E02; W1-06/07/15','A обычные→B правильныеobjects→C правильныеrelations при fixedrules; решает training vs logic/context.'),
('P1/P2 conditional','Recipe→checkpoint→published row lineage и contradictions','Авторский artifact/log/revision по нужде','SAHI abstract/table/config; SoftTeacher jitter/LR/README; FGDgamma; DETReg2023assets; SFODcutoff/selection differences сохранены.','W1-02/03/05/06/09/10/11; W2-06/07/08','Для буквальной replication exactconfig/hash/tablemap; иначе ограниченное evidence и собственный trial, без третьей волны.'),
('P0 promotion','Serialized selected artifact quality reload/export/quant/target','Artifacts + adjacent-stage paired inference/GT','Чтение code не execution. CPU/RTX/ORT не LinQ. Actual training/export/LinQ не выполнены.','W1-13-E01/W1-15-E04; W2-01/09/10/11','Canonical tensors/preprocess/decoder/NMS/rules; raw deviations+GT/support/hashes/placement, frozenbundle+rollback.')]
qmap={};qgroups={f'Q{i:03}':[] for i in range(1,len(qinfo)+1)}
for k,v in questions.items():
    gid=f'Q{q_assign[v["b"]][int(k[-2:])-1]:03}';qmap[k]=gid;qgroups[gid].append(k)
allmap={**smap,**fmap,**emap,**qmap}
def norm(t,b):
    def rel(m):
        label,target=m.group(1),m.group(2)
        if re.match(r'https?://|#',target):return m.group(0)
        if '.md' in target:
            path,sep,anchor=target.partition('#')
            try:r=(docs[b]['p'].parent/path).resolve().relative_to(root).as_posix()
            except ValueError:return m.group(0)
            return '['+label+']('+r+(sep+anchor if sep else '')+')'
        return m.group(0)
    t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',rel,t)
    t=re.sub(r'(W[12]-\d{2})-([SFEQ])(\d{2})[–-](?:\2)?(\d{2})(?!\d)',lambda m:', '.join(m.group(1)+'-'+m.group(2)+f'{n:02}' for n in range(int(m.group(3)),int(m.group(4))+1)),t)
    t=re.sub(r'(?<![\w-])([SFEQ])(\d{2})[–-](?:\1)?(\d{2})(?!\d)',lambda m:', '.join(m.group(1)+f'{n:02}' for n in range(int(m.group(2)),int(m.group(3))+1)),t)
    t=re.sub(r'W[12]-\d{2}-[SFEQ]\d{2}',lambda m:allmap.get(m.group(),m.group()),t)
    return re.sub(r'(?<![\w-])([SFEQ])(\d{2})(?!\d)',lambda m:allmap.get(b+'-'+m.group(1)+m.group(2),m.group()),t)
def refs(t,b,typ):
    t=re.sub(r'(?<![\w-])([SFEQ])(\d{2})[–-](?:\1)?(\d{2})(?!\d)',lambda m:' '.join(m.group(1)+f'{n:02}' for n in range(int(m.group(2)),int(m.group(3))+1)),t)
    return {b+'-'+typ+m.group(1) for m in re.finditer(r'(?<![\w-])'+typ+r'(\d{2})(?!\d)',t)}
f_sources={}
for fid,group in fgroups.items():
    deps=set()
    for k in group:
        v=facts[k];b=v['b'];deps.update(smap[x] for x in refs(v['body'],b,'S') if x in smap)
        prev=[(sv['start'],sid) for sid,sv in sources.items() if sv['b']==b and sv['start']<v['start'] and not sv['body'].startswith('|')]
        if prev:
            parent_i,parent_id=max(prev)
            if not any(re.match(r'^#{1,2} ',line) for line in docs[b]['lines'][parent_i+1:v['start']]):
                deps.add(smap[parent_id])
        for sid,sv in sources.items():
            if sv['b']==b and k in refs(sv['body'],b,'F'):deps.add(smap[sid])
    f_sources[fid]=sorted(deps)
s_facts={s:[] for s in sgroups}
for f,ss in f_sources.items():
    for s in ss:s_facts[s].append(f)
# Durable extraction checkpoint; source content lives in original branches.
(root/'_WORK/ID_MAP.md').write_text('# ID_MAP — сборка в работе\n\nВсе27веток и входы прочитаны. Следующий запуск COLLECTOR_BUILD.py повторяет детерминированную сборку без сети.\n\n'+'\n'.join(f'{k} → {v}' for k,v in allmap.items()),encoding='utf-8')
print('EXTRACTED',len(sgroups),len(fgroups),len(egroups),len(qgroups),'locals',len(sources),len(facts),len(exps),len(questions))


out=[f"""# SOURCES — training_strategy

Сборка: {now}, Europe/Moscow. Доступ исследователей: 23.10.2026; публикация/версия отдельно в карточках. Сборщик новой сети не получал. Все15 W1 и12 W2 прочитаны полностью, первичные read/run статусы восстановлены из журналов. Повтор одного pin не независимое подтверждение.

Канонический источник объединяет чтения одного primary artifact URL/revision. Дополнительные versions/URLs/locators и фактические ограничения сохранены по каждому чтению; разные версии не объявляются побайтно одинаковыми. Исследовательские парафразы не являются полными копиями внешних документов. Тип материала и фактическое получение/исполнение — отдельные поля. Полезность на target и LinQ execution не установлены.

"""]
for s,group in sgroups.items():
    if s=='S001':
        out += ["""<a id="s001"></a>\n\n## S001 — Входная постановка mosprom-research-v1

- **Автор/организация:** пользователь.
- **URL/путь:** [Context-prompt.md](Context-prompt.md), [prompt-training-strategy.md](prompt-training-strategy.md).
- **Тип:** пользовательский контекст/задание, не новая проверка регламента.
- **Публикация/версия:** mosprom-research-v1, дата редакции не установлена.
- **Доступ:** 23.10.2026, оба файла полностью прочитаны.
- **Локатор:** общий контекст §§2–4,15–17; тема §§2–5,8–14.
- **F-связи:** контекст всех F/E/Q; исходные данные/SDK отсутствуют как входы.

"""];continue
    vals=[sources[x] for x in group];raw=vals[0]['body'];joined=' '.join(v['body'] for v in vals)
    us=[]
    for v in vals:
        for u in urls(v['body']):
            if u not in us:us.append(u)
    title=raw.splitlines()[0]
    if title.startswith('|'):title=title.strip('|').split('|')[1].strip()
    title=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',title)
    title=re.sub(r'https?://\S+','',title)
    title=re.sub(r'W[12]-\d{2}-S\d{2}','',title).strip('# |—')
    title=re.sub(r'\s+',' ',title)[:170] or 'Первичный материал и локатор'
    if any(x in joined for x in ['ultralytics/ultralytics','Ultralytics']):author='Ultralytics'
    elif 'NVIDIA' in joined:author='NVIDIA; дополнительные авторы указаны в деталях'
    elif 'Torch-Pruning' in joined:author='VainF/Torch-Pruning, Fang et al.; автор example — в деталях'
    elif 'docs.pytorch' in joined or 'pytorch.org' in joined:author='PyTorch Contributors / авторы конкретного материала в деталях'
    elif 'onnxruntime' in joined:author='Microsoft/ONNX Runtime contributors'
    elif 'cvat' in joined.lower():author='CVAT.ai contributors'
    elif 'OpenMMLab' in joined:author='OpenMMLab'
    else:
        meta=raw
        if raw.startswith('#'):meta='\n'.join(raw.splitlines()[1:]).strip()
        elif raw.startswith('|'):meta=raw.strip('|').split('|')[1].strip()
        prefix=meta.split('[')[0].strip(' *.,;')
        if len(prefix)<4:
            gh=next((re.search(r'github.com/([^/]+)',u) for u in us if re.search(r'github.com/([^/]+)',u)),None)
            author=gh.group(1)+' / авторы материала ниже' if gh else 'Авторы/организация — в первичной библиографической записи ниже; если не названы, не установлены'
        else:author=re.sub(r'\s+',' ',prefix)[:180]
    kind='Первичная публикация/статья и/или связанный авторский artifact' if re.search(r'arxiv|proceedings|CVPR|ICCV|JMLR|ECCV|AAAI',joined) else 'Первичная документация/исходный код/metadata — по деталям'
    status='Получены текст/указанные функции согласно журналу; код модели не исполнен. Индивидуальные ограничения ниже имеют приоритет.'
    if 'W2-10-S01' in group:status='Открыты metadata/abstract; полный paper PDF не читался, numerical results не извлекались.'
    if 'W2-01-S04' in group:status='PyPI JSON и wheel ZIP реально получены, SHA и10файлов bytes сверены; sdist только metadata; install/import/forward не выполнены.'
    if any(x in group for x in ['W2-12-S03','W2-12-S04']):
        kind='Внутренняя передача сохранённых W1/W2, не независимый primary source'
        status='Прочитаны локальные ветки, не новое HTTP подтверждение их источников.'
    out += [f'<a id="{s.lower()}"></a>\n\n## {s} — {title}\n\n',f'- **Автор/организация:** {author}.\n- **Тип материала:** {kind}.\n- **Actual read/run status:** {status}\n',
        '- **Дата доступа:** 2026-10-23, время при наличии — в ветке.\n',
        '- **Публикация/версия — литералы:** '+', '.join(dict.fromkeys(re.findall(r'\b[a-f0-9]{40}\b|\b(?:v)?\d+\.\d+\.\d+\b|\b\d{4}-\d{2}-\d{2}(?:T[0-9:]+Z)?\b|\b\d{2}\.\d{2}\.\d{4}\b',joined)))+'. Тип даты определяется записью ниже; неустановленная дата/редакция отмечена явно, доступ не публикация.\n',
        '- **Прямой URL / состав artifact:** '+('; '.join(f'[материал {i+1}]({u})' for i,u in enumerate(us)) if us else 'внутренние пути в деталях')+'.\n',
        '- **F-связи:** '+(', '.join(f'[{x}](RAW_FACTS.md#{x.lower()})' for x in s_facts[s]) or 'provenance/negative search/implementation context; область и связи в деталях')+'.\n\n']
    seen=set()
    for k,v in zip(group,vals):
        body=norm(v['body'],v['b'])
        if body.startswith('#'):body=re.sub(r'^#{1,4} .*\n', '', body, count=1).strip()
        if body in seen:continue
        seen.add(body)
        out += [f'**Версия, библиография, locator и actual доступ — {k}**, [ветка]({v["path"]}):\n\n',body+'\n\n']
out += ['## Недоступные и непрочитанные материалы; metadata-only artifacts\n\nЭто ограничения доступа/использования, не доказательство отсутствия capability. Указанные ниже альтернативные первичные пути учитываются по фактическому статусу; URL, download link и прочитанный binary различаются.\n\n']
for b,d in docs.items():
    selected=[]
    for l in d['lines']:
        if not l.startswith('|') and re.search(r'403|404|502|не (?:скач|получ|прочит)|Coming [Ss]oon|только.*(?:ссыл|abstract)',l):
            if len(l)>90 and re.search(r'403|404|502|[Дд]оступ|[Вв]еса|[Ww]eight|Coming|PDF|[Ss]dist|model zoo|release|repo',l):selected.append(l)
    if selected:out += [f'### {b}: access/public gaps\n\n',norm('\n\n'.join(selected),b)+'\n\n']
(root/'SOURCES.md').write_text(''.join(out),encoding='utf-8')
raw=[f"""# RAW_FACTS — training_strategy

Сборка: {now}, Europe/Moscow. Полностью прочитаны оба входа, PLAN/RUN_STATE, исходная CRITIC и все27 W1/W2. Нового сетевого получения сборщик не делал. Подробная база сохраняет численные результаты с единицами, версии, протоколы, negative results, implementation contracts, противоречия и проекты проверок.

**Actual checks:** research search/open и read-only metadata/text; W2-01 дополнительно wheel ZIP/bytes/SHA comparison в памяти. Это не установка/модельный запуск. Training, annotation audit, dataset generation, model inference/backward, export, physical surgery, model profiling и LinQ execution не выполнены. Полный кейс, target data, выбранные weights, фактическая GPU/VRAM конфигурация и SDK не предоставлены. Target usefulness всех методов не установлен.

**Основание отдельно от проверки:** DOC/CLAIM — документация/заявление; CODE/REP — исходник; PAPER/PUB/MEASUREMENT — опубликованное авторами описание/измерение; LOCAL/META/BYTES — служебное наблюдение; INFERENCE/INF — наш вывод; PROPOSED/PROP — предлагаемое действие; UNKNOWN — неизвестно. Исходные метки/локаторы в каждом F сохранены. Чтение кода не выполнение, published measurement не наш тест.

**Источники и повторы:** [SOURCES.md](SOURCES.md) хранит версии/access/locators; [_WORK/ID_MAP.md](_WORK/ID_MAP.md) — branch→global. Общий U=e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8/8.4.184 — одна evidence chain, не независимые confirmations и не обязательный стек. Одинаковое наблюдение сведено под один F с сохранением дополнительных условий/версий; новая определённость W2 остаётся отдельным фактом. Это парафразы исследования, не полные копии внешних источников.

**Несопоставимые единицы:** COCO box AP50:95, SAHI AP50, LVIS mask AP, novel AP, pedestrian miss-rate/FPPI, event recall/false-alarms-hour и robot cm не объединяются. Images/instances/episodes/cameras/person-minutes/GPU-hours различаются. Missing support/N/A/невалидный CI не становятся нулём.

## Обязательные gates и условный банк

G0 task/decision; G1 data/observation; G2 correctness только при выбранном training; G3 comparison/selection; G4 deploy/rollback — переиспользуемые допуски. AL/SSL/KD/synthetic/initialization/scale/QAT/pruning/repeats — альтернативы, не mandatory grid. Сначала earliest unknown gate, затем одно различающее сравнение. Gates переиспользуются только для того же task/class/data/split/code/dependency/head/input/preprocess/save/export/SDK contract key. Ранний LinQ feasibility и финальное actual execution различны; обязательный platform outcome сейчас не выполнен.

Очередь всех восьми сценариев, дорогих альтернатив и исходного банка E сохранена в синтезе W2-12 ниже. Caps W1 — illustrative proposed diagnostics, не общие бюджеты. Deadline useful artifact задаёт integration owner: now+CP_remaining<=D_useful с измеренными costs, без выдуманных минут RTX4070.

## Критические уточнения и противоречия

1. Native KD существует: wheel8.4.184/10files bytes verified, U — следующий docs commit после release R. YOLO11n←target-trainedYOLO11s doc/code-supported; installation/runtime/benefit/target нет.
2. Teacher сохраняет свои classes; max-class weighting допускает другое nc технически, semantic competence проверяется отдельно. EMA checkpoint уже teacher-free, projectors до final unwrap.
3. Hidden class B и hidden instance C различны. U dense BCE без objectness, legacyv5 objectness и обе activeE2ELoss branches требуют своих validity. MMDet ignore defaults off/zero-regular-GT исключение.
4. UTv2 std auxiliary остаётся Python eval и defaultteacher; EfficientTeacher rawstudent/onlineEMA/secondarybest/export разные, domain heads удаляются явно, rawlevels нужен decoder.
5. Results scalarconf/cls,probs=None; low-confidence heuristic не entropy. No-box/error records+exploration обязательны для предложенной policy; superiority неизвестна.
6. Teacher audit ищет всеGT/no-detection misses; probability P и targeted D отдельно без выдуманных inclusion weights; calibration не восстанавливает recall.
7. Pretraining — состав tensors/ancestry. DETReg base/no-base schedules/unlabelled exposure confound;2023assets/results не ранний2021release.
8. Source-free eval-only меняет BN; source-val hooks/manual JSON могут раскрыть source/hiddenGT. No-grad не frozenstate.
9. Gen2Det author code не найден после primary traces. Paper p whole batches, tau_i0 synthbg RPN+head, lowdata безfilter/ignore; foldermerge не reproduction.
10. NVIDIA detectorQAT — featureMSE reconstruction/noGT, historical lock неполон; QDQ/TensorRT не LinQ arithmetic match.
11. Physical pruning TP1.6.1+oldU8.0.90/C2f_v2/patchedtrain/fullobject; YAML/state_dict не topology; speed_up MACratio, no rejected-stage rollback.
12. Freeze разрешён resume, новыйLR/optimizer/epochs нет. Даже prestrip без online/RNG/loader/scheduler exactstate; on_model_save позволяет immutable serialized EMA candidates.

"""]
corrections={'W1-10-F06': 'F193: saved EMA wrapper уже teacher-free; projectors до unwrap. F274: pre-strip не exact online/RNG/loader/scheduler continuation.', 'W1-12-F05': 'F272/F273/F274/F275/F276/F277: точный lifecycle. Pre-strip EMA вместо online, scheduler/RNG/loader не сохраняются; boolean resume stripped может стать new training.', 'W1-12-F07': 'F276: freeze входит в resume whitelist; новый LR/optimizer/epochs нет. Новая stage2 с новым recipe — resume=False, unfreeze в прежнем run технически разрешён.', 'W1-15-F08': 'F272/F273/F274/F277: immutable candidates через on_model_save до strip; AP-best/custom objective раздельны, pre-strip не exact continuation.', 'W1-13-F05': 'F256: найден reconstruction QAT без detector GT loss. Labels нужны quality measurement, но не каждому QAT objective; supervised QAT — другой contract.', 'W1-09-F12': 'F206–F212: UTv2 code теперь прочитан; std остаётся Python eval, default teacher, обычный export не доказан. F213–F219 — legacy YOLOv5 EfficientTeacher route.', 'W1-03-F13': 'F194–F205: U loader/assignment/BCE/regression/E2E trace. Hidden class B и hidden instance C различны; MMDet default/zero-GT ограничения.', 'W1-11-F10': 'F248–F254: Gen2Det paper RPN+head ignore не inspected trainer. Author artifact gap Q020 открыт; reviewed data-only route отличается.', 'W1-11-F11': 'F249/F250/F251: whole-batch exposure, low-data без filtering/ignore, Table2/Table5 provenance; naive-mix negative result сохранён.', 'W1-07-F07': 'F241–F246: simple-SFOD author route найден, local weights/manual JSON/eval BN/source hooks/selection gap не ready target package.', 'W1-02-F09': 'F191: class-row transfer — student; KD teacher target nc/names не получает. Different nc не обязательно shape failure для max-class weighting.'}
last_b=None
for f,group in fgroups.items():
    v0=facts[group[0]];b=v0['b']
    if b!=last_b:raw += [f'\n## {b} — {docs[b]["lines"][0].lstrip("# ")}\n\n'];last_b=b
    title=re.sub(r'^#{1,4}\s*|^\*\*|\*\*$','',v0['body'].splitlines()[0])
    title=re.sub(r'W[12]-\d{2}-F\d{2}','',title).strip(' /—|')
    title=norm(title,b).replace('*','')
    if len(title)>165:title=title[:165].rsplit(' ',1)[0]+'…'
    raw += [f'<a id="{f.lower()}"></a>\n\n### {f} — {title}\n\n',
        '**Тип основания:** исходная метка в наблюдении ниже. **Actual статус:** '+('служебная metadata/wheel/bytes проверка выполнена; install/runtime нет.' if 'W2-01-F01' in group else 'получен/прочитан текст или проанализированы сохранённые основания; model run/target benefit не проверены.')+'\n\n',
        '**S/locator:** '+(', '.join(f'[{x}](SOURCES.md#{x.lower()})' for x in f_sources[f]) or 'S001 и указанные F/branch основания; это вывод/проект/статус, не самостоятельное измерение')+'. **Исходные IDs:** '+', '.join(group)+'.\n\n']
    for oldid in group:
        if oldid in corrections:raw += ['**Уточнение W2 к исходному утверждению:** '+corrections[oldid]+'\n\n']
    seen=set()
    for k in group:
        v=facts[k];body=norm(v['body'],v['b'])
        if body.startswith('#'):body=re.sub(r'^#{1,4} .*\n', '', body, count=1).strip()
        if body in seen:continue
        seen.add(body)
        raw += [f'**{k}: условия/наблюдение** ([ветка]({v["path"]})):\n\n',body+'\n\n']
    raw += ['**Предел:** version/model/data/split/metric и оговорки выше — часть факта. CODE≠RUN; published number не наш результат. Target решение требует соответствующей E/Q.\n\n']
raw += ['## Дополнительные карты решений, metadata contracts и восемь сценариев\n\nНиже — явно предложенные схемы/синтез веток, не новые измерения. Содержательные матрицы сохранены, чтобы F-база не теряла operational contracts между отдельными наблюдениями.\n\n']
for b,secs in extras.items():
    if secs:
        raw += [f'### {b}: решение и контракты\n\n']
        for sec in secs:
            raw += [re.sub(r'^## ','#### ',norm(sec,b),flags=re.M)+'\n\n']
raw += ["""## E-процедуры следующей практической волны

**Общий contract C-E.** Все E — PROPOSED/не выполнены. До запуска exact model/task/repo/package/dependency/checkpoint hash получает model_stack либо фиксирует отсутствие как Q005/Q006; выдуманных CLI/weights нет. Data/ontology/coverage/roles/group independence фиксируются версиями Q001–Q004; lockbox не debugging/training/acquisition/calibration pool. OS/torch/CUDA/driver/GPU/VRAM — inventory; SDK/device обязателен для target части Q007–Q009. Если локальная E не задаёт numerical cap/margin, это незаполненный вход Q010/Q027 до trial по фактическому pilot, не неограниченный sweep.

Контроль сохраняет init/class rows/data/split/preprocess/postprocess/rules и заявленный estimand update/exposure/human-time; различия явно записываются. Artifacts: hashes data/config/dependencies/weights/input, отдельные sample/optimization/split/resampling seeds, raw outputs/logs, actual exposures/updates/time, immutable serialized selected checkpoint+reason. Outcomes: promote/kill/inconclusive/rollback, не обещанное улучшение. Любой successful gate ограничен этой реализацией/материалом; unseen cameras/rare events/event safety/LinQ без actual test не подтверждает. Точные дополнительные fields и stop/limit каждой процедуры ниже имеют приоритет. E W2 amendments объединены с исходной процедурой и не добавляют обязательный quality trial.

"""]
for e,group in egroups.items():
    v0=exps[group[0]];title=re.sub(r'^#{1,4}\s*(?:\d+\.\s*)?','',v0['body'].splitlines()[0])
    title=re.sub(r'W[12]-\d{2}-E\d{2}','',title).strip(' —')
    raw += [f'<a id="{e.lower()}"></a>\n\n### {e} — {title}\n\n',
        '**Статус/очередь:** PROPOSED, не выполнено; gate либо условная альтернатива W2-12. **Общие входы/checkpoint/environment/контроль/artifacts/stop/limit:** C-E; unresolved exact interfaces Q005/Q006/Q007/Q010/Q027. Локальные детали ниже обязательны в scope выбранной ветки.\n\n',
        '**Состав:** '+', '.join(group)+'.\n\n']
    for k in group:
        v=exps[k];body=norm(v['body'],v['b'])
        body=re.sub(r'^#{1,4}\s*(?:\d+\.\s*)?.*\n','',body,count=1)
        body=re.sub(r'^#{1,3} ','#### ',body,flags=re.M)
        raw += [f'**{k}: '+('исходная процедура' if k==group[0] else 'W2 операционная поправка/дополнение')+f'** ([ветка]({v["path"]})):\n\n',body+'\n\n']
(root/'RAW_FACTS.md').write_text(''.join(raw),encoding='utf-8')
print('SAVED SOURCES/RAW',len(''.join(out)),len(''.join(raw)))


qo=[f"""# OPEN_QUESTIONS — training_strategy

Сборка: {now}, Europe/Moscow. Нового поиска после27 веток нет. Вопрос не означает отсутствия capability. Public contracts отделены от missing artifact, неизвестного target benefit и невыполненного SDK/experiment. Исходные154 локальные формулировки сведены в31 decision object с сохранением условий/истории. W2 уточняет ранние W1 вопросы; закрытый public trace не запрашивается повторно как общий обзор.

Короткая P0 группа: Q001 ontology; Q002 exposure permission; Q003 coverage; Q004 independent support; Q005/Q006 actual artifacts/environment; Q007–Q009 LinQ/quant/placement; Q010 acceptance. Перед unchecked labels нужны Q011/Q013; перед long training Q025. Actual LinQ execution — обязательный outcome, сейчас не выполнен. Q020 — локализованный public author-code gap; Q022–Q024 — условные artifact/implementation ветки, не третья волна.

"""]
for i,(priority,title,mode,known,history,decision) in enumerate(qinfo,1):
    q=f'Q{i:03}';group=qgroups[q];relatedF=set();relatedE=set()
    branches=sorted({questions[k]['b'] for k in group})
    for local in group:
        v=questions[local];b=v['b']
        relatedF.update(fmap[x] for x in refs(v['body'],b,'F') if x in fmap)
        relatedE.update(emap[x] for x in refs(v['body'],b,'E') if x in emap)
    if not relatedF:
        for b in branches:
            relatedF.update([gid for gid,g in fgroups.items() if any(x.startswith(b+'-') for x in g)][:2])
    if not relatedE:
        for b in branches:
            relatedE.update([gid for gid,g in egroups.items() if any(x.startswith(b+'-') for x in g)][:1])
    kk=8 if i==20 else 11 if i==25 else 12 if i in [27,28] else 5 if i==11 else 2 if i==13 else 9 if i in [8,23] else 10 if i==24 else 7 if i==22 else 3 if i==21 else 6 if i==15 else 4 if i==16 else 1 if i==5 else 12
    qo += [f'<a id="{q.lower()}"></a>\n\n## {q} — {title}\n\n',f'- **Приоритет:** {priority}.\n- **Mode to close:** {mode}.\n- **Что известно:** {known}\n',
        f'- **Где искали/что прочитали:** {history}; полный history/locators в '+', '.join(f'[{b}]({docs[b]["p"].relative_to(root).as_posix()})' for b in branches)+'. Сборщик новых HTTP не получал.\n',
        f'- **Почему остаётся неизвестным:** нужный actual case/artifact/данные/исполнение отсутствует; известный public contract не устанавливает его target результат. Точная граница в scoped уточнениях ниже.\n',
        f'- **Недостающее звено / решение / способ закрытия:** {decision}\n',
        '- **Related IDs:** '+', '.join(f'[{x}](RAW_FACTS.md#{x.lower()})' for x in sorted(relatedF)+sorted(relatedE))+f'; K{kk:03}.\n\n',
        '**Сведённые условия и происхождение** (если ранний public вопрос W1 закрыт W2, текущий остаток — actual artifact/experiment, не повторный общий поиск):\n\n']
    if not group:qo+=['Сборщик выделил вопрос из фактов/контрактов, отдельного branch Q не было.\n\n']
    for local in group:
        v=questions[local];body=norm(v['body'],v['b']).strip(' |')
        qo += [f'- **{local}** ([ветка]({v["path"]})): '+body+'\n\n']
(root/'OPEN_QUESTIONS.md').write_text(''.join(qo),encoding='utf-8')
mp=[f"""# ID_MAP — training_strategy

Сборка: {now}, Europe/Moscow. Полностью прочитаны входы, критика, PLAN/RUN_STATE и27W1/W2; усечения дочитаны диапазонами. Нового получения сети нет. Служебный воспроизводимый скрипт: [COLLECTOR_BUILD.py](COLLECTOR_BUILD.py); он читает исходные ветки, не получает сеть и не исполняет модели.

Канонический S объединяет primary artifact URL/revision; дополнительные versions/bibliography/read limits сохранены внутри. Повтор F объединён с сохранением условий, W2 new contracts не независимые confirmations. W2 E amendments сосредоточены с исходной процедурой, не добавляют mandatory quality trials. Q сведены по решению, все154 исходных формулировки сохранены в OPEN_QUESTIONS.

**Реальные counts:** {len(sgroups)} S, {len(fgroups)} F, {len(egroups)} E, {len(qgroups)} Q. Исходные definitions: {len(sources)} S, {len(facts)} F, {len(exps)} E, {len(questions)} Q. S001 — пользовательский контекст. Branch shorthand после merge может образовать немонотонный range; для точной связи использовать эту карту, не арифметический global range.

"""]
for b in docs:
    mp += [f'## {b} — [{docs[b]["p"].name}]({docs[b]["p"].relative_to(root/"_WORK").as_posix()})\n\n','| Branch ID | Global ID | Тип |\n|---|---|---|\n']
    for typ,mm in [('S',smap),('F',fmap),('E',emap),('Q',qmap)]:
        for k,v in mm.items():
            if k.startswith(b+'-'):mp.append(f'| {k} | {v} | {typ} |\n')
    mp.append('\n')
mp += ['## Слияния\n\n']
for groups in [fgroups,egroups,sgroups]:
    for gid,g in groups.items():
        if len(g)>1:mp.append(f'- {gid}: '+', '.join(g)+'.\n')
(root/'_WORK/ID_MAP.md').write_text(''.join(mp),encoding='utf-8')
print('SAVED Q/ID',len(''.join(qo)),len(''.join(mp)))

# Outcomes append preserves the complete original criticism byte-for-text; rerun replaces only collector append.
critic_path=root/'CRITIC.md'
critic=critic_path.read_text(encoding='utf-8-sig')
marker='\n<!-- COLLECTOR_W2_OUTCOMES -->\n'
original=critic.split(marker)[0]
outcome=[
('K001','уточнена область','01_NATIVE_KD_CONTRACT.md','S078, S137, S138, S139, S080, S140, S012, S011','F187, F188, F189, F190, F191, F192, F193','E027, E028','Q005, Q006, Q007, Q011, Q025, Q030',
'Установлена package provenance: release R не U, wheel8.4.184 действительно получен, SHA и10нужныхfiles byte-equal U. Конкретизирован documented same-family/code-supported YOLO11n←target-trainedYOLO11s: grids/channels/strides/raw scores и native student extraction.',
'Разное nc технически допустимо max-class feature weighting; teacher сохраняет свой class contract. Это не semantic transfer и не quality admission. EMA уже без teacher, wrapper/projectors до unwrap. KD теперь конкретная опция при готовом полезном teacher, без обязательного обучения нескольких families.',
'Installation, actual checkpoint compatibility/BN/gradients/VRAM, teacher competence, controlled student gain/export/LinQ не выполнены.'),
('K002','закрыто','02_PARTIAL_ASSIGNMENT.md','S025, S141, S026, S012, S142, S143, S144, S145, S146','F194, F195, F196, F197, F198, F199, F200, F201, F202, F203, F204, F205','E007','Q003, Q006, Q013, Q007',
'Закрыт именно публичный static loader→assignment→loss gap: hidden GT не создаёт targets, U dense BCE отрицательна по zero-target entries, regression только known foreground, две active E2ELoss branches. Legacyv5 отдельно objectness.',
'B unknown class допускает custom image×class validity при exhaustive остальных; C hidden instance не решается той же полной class mask. Нужны positive precedence/reduction/geometry и transformed coverage. MMDet known crowd route class-agnostic, thresholds defaultoff, zero regularGT всё background. Unsafe union не готов по одному ignore flag.',
'Практические gradients/mask correctness/actual coverage/target gain не проверены. Default conditional альтернатива — fully checked subset либо separate exhaustive own tasks; это не claim always-best.'),
('K003','уточнена область','03_ONESTAGE_SSL.md','S147, S148, S149, S150, S151, S152, S153, S154, S155, S156, S157, S158','F206, F207, F208, F209, F210, F211, F212, F213, F214, F215, F216, F217, F218, F219','E026','Q002, Q004, Q011, Q021, Q007',
'Найдены и прочитаны concrete UTv2 FCOS и отдельный EfficientTeacher legacy YOLOv5 route, с head/loader/geometry/pseudo losses/state/extraction boundaries.',
'UTv2 std branch остаётся Python eval, teacher default. ET rawstudent/onlineEMA/secondarybest/export различны, --da снимает domain heads, export raw levels требует decode. Нельзя назвать generic modernYOLO feature; один compatible route — альтернатива corrected-supervised.',
'Weights/lock/runtime/empty/mixed gradients/clean extraction/export parity и actual target benefit/LinQ открыты.'),
('K004','закрыто','04_ACQUISITION_INTERFACE.md','S159, S160, S161, S162, S163, S164, S165, S166, S167, S168','F220, F221, F222, F223, F224, F225, F226','E022','Q006, Q012, Q016, Q002',
'Публичный U Results interface закрыт: original xyxy, scalar conf/cls, detect probs=None. Full logits/vectors/features находятся до filtering и требуют другого interface.',
'Минимальный proposed route low-confidence retained scores + metadata exploration не требует extra forwards поверх уже выполненного pool inference. Это не entropy/calibrated uncertainty. No-box/error/cap rows и exploration обязательны; scan/human QA могут быть дорогими.',
'Actual checkpoint interface/cost/ranking usefulness против stratified random при equal total human minutes не измерены.'),
('K005','закрыто','05_TEACHER_AUDIT.md','S169, S170, S171, S172, S173, S174','F227, F228, F229, F230, F231, F232, F233','E024, E023','Q004, Q010, Q011, Q012, Q013',
'Закрыт public-methodical admission gap: detection calibration определяется class+IoU criterion и не может калибровать recall пропусков без scores; netcal получает matched per prediction.',
'Blind completeGT/no-detection audit, probability P против diagnostics D, известные inclusion probabilities/weighted ratios и group uncertainty сохранены. Cutoff chosen audit не independent confirmation; insufficient support/N/A — отказ от unchecked claim. Fully reviewed assistance не требует calibrator.',
'Ни один actual teacher/class не допущен: нет target support, numerical acceptance, audit/cost/confirmation.'),
('K006','закрыто','06_DETECTION_PRETRAINING.md','S175, S176, S177, S178, S179, S180, S181, S182, S183','F234, F235, F236, F237, F238, F239, F240','E048, E004','Q005, Q015, Q002, Q030, Q007',
'Публичное различение initialization восстановлено: DetCo representation versus DETReg localization/transformer/query components сверх SwAV backbone versus supervised source detector/base stage.',
'Source/base stage schedules/exposure/normalization/head confound исключают простое causal ranking. DETReg2023few-shot/assets/latepaper и filename scratch не no-pretraining. Предложена одна identical-backbone/head tensor ablation; готовый artifact отличается от pretraining с нуля.',
'Actual weight key/hash lineage, exact author checkpoint-selection, лучший target init/retention и SDK совместимость не установлены.'),
('K007','уточнена область','07_SOURCEFREE_ROUTE.md','S055, S184, S185, S186, S187, S188, S189, S190','F241, F242, F243, F244, F245, F246','E020','Q002, Q005, Q022, Q007',
'Найден author-linked simple-SFOD AdaBN→fixed pseudoJSON→FasterR-CNN, то есть public implementation больше не только название.',
'Runnable artifact/selection частично открыты: weights local, JSON ручной и может остаться GT; eval-only реально меняет BN, source ValLossHook/state exposure нарушает строгий source-free. No-grad не frozen evaluation. Fixed ordinary loss не лечит omissions.',
'Исходный SFOD2021 repo не установлен; exact fixed-row selection/cutoff, compatible source detector/lock, runtime/audit/benefit/retention/LinQ требуют artifact/experiment. P2 conditional, без proxy quality claim.'),
('K008','открыто','08_SYNTHETIC_SUPERVISION.md','S099, S191, S192, S193','F247, F248, F249, F250, F251, F252, F253, F254','E030, E031, E007','Q019, Q020, Q003, Q007',
'Author Gen2Det trainer/fork/config/schema не найден после paper→author pages→GitHub exact-name/author tracing. Это локализованный public gap, не отсутствие кода/capability.',
'Уточнён paper scope: background-ignore RPN+detector head, tau_i0 все synthetic bg, p0.2 whole batches, poolratio/drawfraction/schedule различны. Low-data COCO без filtering/ignore; LVIS ablations и COCO borrowedXPaste provenance ограничивают causal reading. Negative naive-mix сохранён.',
'До нового primary artifact special-loss route не concrete recipe. Доступная future альтернатива — fully reviewed whole synthetic frames + ordinary supervised detector с real holdout/exposure controls; польза target неизвестна.'),
('K009','уточнена область','09_DETECTOR_QAT.md','S194, S195, S196, S197, S198, S199, S200, S201, S202, S203, S204','F255, F256, F257, F258, F259, F260, F261','E049, E038, E037','Q008, Q023, Q004, Q007',
'Concrete detector QAT→export code найден: NVIDIA YOLOv7 fuse→quant/rules→calibration→feature reconstruction→ONNXQDQopset13→TensorRT.',
'Actual finetune loss featureMSE/no detectorGT; это не supervised newclass adaptation. Historical detector/toolkit lock неполон, reference2.1.2 не установленная авторская версия. MMrazor detector config оказался PTQ. Нельзя переносить route на modernYOLO/LinQ по имени.',
'Dependency/container/weights/ONNX hashes, arithmetic/fusion/import matchSDK, FP continuation/reconstruction controls и actual exported/target quality открыты. QAT только после PTQ diagnostics.'),
('K010','уточнена область','10_PHYSICAL_PRUNING.md','S205, S206, S207, S208, S209, S210, S211, S212, S213, S214, S215','F262, F263, F264, F265, F266, F267, F268, F269, F270, F271','E050, E037','Q024, Q007, Q009',
'Положительный detector-aware graph surgery route найден в author-hosted TP example: dependency groups физически уменьшают Conv/BN/dense dimensions, защищают head outputs.',
'Ограничение старое: TP1.6.1+U8.0.90/C2f_v2/patched train/save/fullobject, custom import при reload; originalYAML+state_dict topology не восстановит. Conversion-only parity/export/compile доrecovery. Speed_up — MAC ratio, demo break экспортирует current rejected stage без rollback.',
'Actual pinned execution, conversion/reload/export correctness, recovery useful quality и LinQ latency/memory не измерены. P2 резерв после меньшего native student, не запрет и не mandatory trial.'),
('K011','закрыто','11_CHECKPOINT_CONTROL.md','S011, S081, S164, S216, S217, S105, S012, S104','F272, F273, F274, F275, F276, F277, F193','E035, E046, E037','Q025, Q010, Q007',
'Публичная lifecycle/operational часть закрыта exact save/val/callback/strip/override trace. on_model_save после write доstrip даёт immutable EMA candidates и внешний constrained winner без замены APfitness.',
'Существенные уточнения ранних формулировок: freeze разрешён resume; LR/optimizer/epochs нет. Prestrip уже EMA вместо online и без scheduler/RNG/loader/accumulation state; strip не единственная причина отсутствия exact continuation. Booleanresume stripped может тихо стать новым training. Новая stage2 с новым recipe явно resumeFalse.',
'Actual copy/evaluator/reload/stage-transition test, target objective/support/acceptance и finalSDK execution отсутствуют. Exact trajectory требует иного reviewed saver; не обещать восстановление задним числом.'),
('K012','закрыто','12_TRIAL_QUEUE.md','S218, S219, S220','F278, F279, F280, F281, F282, F283, F284','E051; все E001–E050 как reused gates/alternatives','Q027, Q028, Q001, Q010, Q007',
'Методическая queue часть закрыта: все исходные E размещены в reused G0–G4 или conditional alternatives;8сценариев имеют первое наблюдение, один discriminating next trial, kill/promote/rollback/useful artifact.',
'Hyperband/ASHA не дают detector rank-preservation guarantee. ShortU может менять autooptimizer/warmup/schedule/close_mosaic, resume не exactprefix; correctness smoke не ранний quality ranking. Admission по wholeCP/D_useful, reviewer/SDK/annotation dependencies, не GPU utilization.',
'Actual times, workload, resource configuration, independent support, useful deadline и scheduler benefit остаются case/experiment; numerical timetable/optimal scheduler не заявлены.')
]
append=[marker,f'\n## Сборщик: outcomes K001–K012 после второй волны\n\nДата сборки: {now}, Europe/Moscow. Исходный текст выше сохранён. Новые основания —12 самостоятельных W2 результатов; сборщик прочитал их вместе со всеми15W1. Ни один outcome не означает выполненное обучение/экспорт/target inference. Закрытие относится к указанному public/methodical вопросу, остаток вынесен в OPEN_QUESTIONS.\n\n']
for k,status,file,ss,fs,es,qs,found,decision,left in outcome:
    append += [f'### {k}: {status}\n\n',f'- **Результат:** [_WORK/W2/{file}](_WORK/W2/{file}).\n- **Новые/уточняющие источники:** {ss}.\n- **Глобальные факты:** {fs}; [RAW_FACTS.md](RAW_FACTS.md).\n- **E/Q:** {es}; {qs}.\n',
        f'- **Что найдено:** {found}\n- **Как изменилось решение:** {decision}\n- **Остаток case/SDK/artifact/experiment:** {left}\n\n']
append += ['Статусы: закрыто — K002/K004/K005/K006/K011/K012 (6); уточнена область — K001/K003/K007/K009/K010 (5); открыто — K008 (1). Противоречащие старые/новые ограничения не скрыты: поправки стоят также у затронутых F в RAW_FACTS. Отдельной финальной проверки отчётов этот файл не содержит.\n']
critic_path.write_text(original+''.join(append),encoding='utf-8')
print('CRITIC OUTCOMES APPENDED',len(outcome))


handoff='# AUTHOR_HANDOFF — training_strategy\n\nСборщик прочитал оба входа, общие правила и роль COLLECTOR, PLAN/RUN_STATE, исходную критику, все 15 W1 и 12 W2. Усечённые ответы дочитаны диапазонами. Новой сети, обучения, генерации данных, модельного инференса, экспорта, pruning surgery и LinQ execution не было. W2-01 выполнил только служебное получение wheel ZIP, сравнение bytes и SHA.\n\nГотовы [SOURCES.md](../SOURCES.md), [RAW_FACTS.md](../RAW_FACTS.md), [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md), outcomes в [CRITIC.md](../CRITIC.md). Реальные counts: 220 канонических S, 284 F, 51 E, 31 Q. S001 — пользовательская постановка. Сведены исходные 251 S / 292 F / 62 E / 154 Q; отличающиеся условия и версии сохранены. [ID_MAP.md](ID_MAP.md) даёт все branch→global связи; [COLLECTOR_BUILD.py](COLLECTOR_BUILD.py) воспроизводит служебную сборку без сети.\n\n## Доказательная картина\n\nНужен связный рассказ о выборе следующего действия. Начало цепочки — воспроизводимая baseline и контракт наблюдения: смысл классов и событий, фактическое изображение после preprocessing, полнота annotations, независимые группы оценки, способ сохранения и ранняя feasibility LinQ. Наблюдаемая ошибка затем превращается в гипотезу и одно различающее сравнение. Методы не образуют обязательный набор; отказ или inconclusive результат тоже меняет решение, если сохранены причины и рабочий bundle.\n\nСодержательный риск — неверное supervision или selection. Источник никогда не размечал класс, пропущен второй instance уже размечаемого класса, изображение полностью unlabeled и проверен настоящий negative — разные случаи. TXT/conversion может стереть различие ещё до loss. Небольшой полностью проверенный subset — конкретная условная альтернатива сложному trainer, но его превосходство и человеческая стоимость на наших данных не измерены. Тысячи соседних кадров не заменяют независимые эпизоды, камеры или отсутствующий визуальный сигнал.\n\nБольшой teacher может дать предразметку с коррекцией, поиск примеров, noisy labels, online EMA supervision или feature KD. Это разные вмешательства. Их стоимость и окончательная inference branch различаются; teacher AP нельзя сообщать как student AP. Confidence не подтверждает правильный class+box+wearing/event, а калибровка не восстанавливает объекты без detections.\n\nВторая волна дала положительные implementation contracts, а не только ограничения: опубликованный native KD package, конкретную YOLO11 пару, trace hidden-label negatives, авторские one-stage SSOD и source-free routes, detector QAT и физический pruning. Они остаются условными вариантами с точными prerequisites, доступными артефактами и локализованными gaps. Полезность на target не установлена.\n\nОбязательный platform outcome — фактический инференс выбранного artifact на LinQ — не выполнен. Публичные заявления yolo5s/yolo8/yolo11, int8, Compiler и DNN Quant не определяют exact SDK/device/operator/quant contract. CPU/RTX/ORT дают reference и отладку; каждый selected student/graph должен пройти реальную цепочку reload→export→quant/compiler→target.\n\n## Навигация для выборочного чтения\n\nУ F/E имеются стабильные anchors: ../RAW_FACTS.md#f001 и #e001; источники — ../SOURCES.md#s001, вопросы — ../OPEN_QUESTIONS.md#q001. В F сохранены тип основания, source/locator, actual read/run status, числа и условия. Важные W2 поправки стоят и у затронутых ранних F. Source blocks содержат bibliography/access, а не случайно захваченные fact/experiment blocks.\n\n| Решение | F | E | Q |\n|---|---|---|---|\n| Baseline, причина ошибки, object против event | F001–F007, F080–F082, F186 | E001 baseline, E002 oracle stages, E003 visibility | Q001/Q004/Q010/Q017/Q029 |\n| Малая разметка, limited/full, BN, class transfer | F008–F032, F234–F240 | E004 depth, E005 BN, E006 sample variance, E048 initialization | Q005/Q014/Q015/Q026 |\n| Hidden class B, hidden instance C, assignment/ignore | F023–F031, F040–F042, F194–F205 | E007 A/B/C + W2 supplement; E008 sparse inference | Q003/Q013 |\n| Rare exposure, RFS, weights, hard negatives | F033–F049 | E009 counts, E010 один balancing trial, E011 negatives vs diverse annotation | Q003/Q004/Q010 |\n| Augmentation semantics и small-label survival | F050–F071 | E012 gate, E013 ablation, E014 tiny survival, E015 real degradation | Q001/Q017/Q018/Q019 |\n| Resolution/tiles/cascade и полная цена | F072–F082 | E003, E016 input/tiles, E017 predicted crops, E018 scale training | Q007/Q009/Q017 |\n| Domain mixing, retention, new session/camera | F083–F092, F241–F246 | E019 mixing, E020 source-free, E021 camera/rules | Q002/Q003/Q004/Q022 |\n| AL, ручная разметка, CVAT, output scores | F093–F101, F220–F226 | E022 output/cost + equal minutes, E023 assistance | Q006/Q012/Q016 |\n| Teacher admission, pseudo и online SSOD | F102–F114, F206–F219, F227–F233 | E024 audit, E025 corrected supervised, E026 online gate | Q011/Q013/Q021 |\n| Native/heterogeneous KD, final student | F115–F129, F187–F193 | E027 native smoke+quality, E028 extraction, E029 FGD/LD | Q005/Q007/Q011/Q025/Q030 |\n| Synthetic и Gen2Det gap | F130–F147, F247–F254 | E030 labels, E031 real transfer/exposure, E032 shortcuts | Q019/Q020 |\n| Optimization, реальные updates, EMA/state | F148–F154, F272–F277, F193 | E033 loader, E034 update, E035 tiny/reload/save/stages, E036 optimizer | Q006/Q014/Q025 |\n| PTQ/QAT/pruning/target | F155–F167, F255–F271 | E037 parity+lockbox, E038 calibration, E039 umbrella, E049 QAT, E050 pruning | Q007–Q009/Q023/Q024/Q031 |\n| GPU/DDP/cost/queue | F168–F179, F278–F284 | E040 profile, E041 loader/cache, E042 DDP, E043 annotation, E044 dispatch, E051 queue | Q012/Q027/Q028 |\n| Selection, independence, uncertainty, rollback | F177, F180–F186, F272–F277 | E045 partitions, E046 weights vs rules, E047 repeats, E037 frozen bundle | Q004/Q010/Q025/Q026/Q031 |\n\nGlobal ranges здесь действительно последовательны; точные branch ranges после слияния раскрыты в базе и ID_MAP. 51 E — банк альтернатив и переиспользуемых gates, не 51 обязательный запуск. Исходные caps W1, например diagnostic tiny run до 300 updates или 15 минут, сохраняют статус предложений конкретного smoke test.\n\n## Поправки W2, которые нельзя потерять\n\n**Native KD — F187–F193.** Wheel 8.4.184 действительно получен; SHA256 d04c80f27d335fe27a057dcf00f91c843b11f99d21e7b3017616959a523bfc8a, десять contract files byte-equal U. U=e6d5fc5918f57d4d39fadb43fc5b2a1aea132ac8 — следующий docs commit после release R=f7dd275e5853801674ca78ef51896617bb5362ba, не release tag. YOLO11n←target-trained YOLO11s имеет documented family support и code-supported стандартные grids/channels/strides. Runtime/quality/export/LinQ не проверены. Teacher сохраняет собственный task/nc/names; max-class weighting допускает другое nc технически, но не создаёт semantic knowledge нового класса. EMA payload уже teacher-free; wrapper/projectors остаются до final unwrap. Строка distill_model в final train_args не доказывает inference dependency.\n\n**Partial labels — F194–F205.** В objectness-free U случай B допускает custom BCE column validity без безусловного изменения bbox loss, если остальные классы exhaustive. C требует другой spatial/negative policy; ignore не создаёт missing localization. Legacy YOLOv5 требует отдельного objectness handling. В active E2ELoss надо проверять обе assignments/loss branches; displayed logs только one-to-one. MMDetection crowd route class-agnostic, thresholds default -1, zero regular GT назначает всё background. Это static trace, не измеренный gradient test.\n\n**One-stage SSOD — F206–F219.** UTv2 FCOS std branch остаётся Python eval field, стандартный cls_n_ctr ranking её не использует; удаление/export — proposed инженерная работа. Default evaluation teacher. EfficientTeacher active path — legacy YOLOv5, не generic current Ultralytics. Raw student, online pseudo teacher EMA и secondary best/export EMA различны. Domain heads вычисляются даже при нулевом loss, снимаются явно через --da. Export raw levels требует собственного sigmoid/grid/anchor decoder и parity.\n\n**Acquisition и teacher audit — F220–F233.** Detect Results содержит original xyxy, scalar conf/cls; probs=None, boxes.data уже postprocessing. Low-confidence retained ranking не entropy. Нулевое число дополнительных forwards относится к score поверх уже выполненного pool inference, а не к полной стоимости acquisition. No-box/error/cap records и exploration входят в предложенную policy. Probability P и targeted D audit нельзя сливать в population rate без известного design. Calibration не восстанавливает recall пропусков. GT класса 0 → recall N/A; accepted 0 при GT>0 → precision N/A, recall 0. Degenerate CI unavailable. Никакая страта teacher пока не допущена к unchecked labels.\n\n**Initialization — F234–F240.** DetCo representation не обученная detector head. DETReg передаёт localization/transformer/query компоненты, но pretrain loader удаляет class_embed; SwAV/FrozenBN ancestry существенна. Base/no-base сравнение меняет ещё и schedules, не чистый effect source-stage. Filename scratch означает no supervised base stage, а не отсутствие pretraining. Results/assets обновлены в 2023 при release label 2021; label не tensor hash. Готовый artifact и pretraining с нуля имеют разную цену.\n\n**Source-free — F241–F246.** Simple-SFOD eval-only вызывает model.train/no_grad и AdaBN, до 1401 forward; frozen baseline так не получают. Активный путь не вызывает reset helper. JSON registration может оставаться target GT, подмена manual. Source ValLossHook создаёт source-label/state exposure, ordinary loss не чинит omissions. Repo найден; compatible source weights, lock, fixed-row selection и target usefulness не установлены.\n\n**Synthetic — F247–F254.** Gen2Det author trainer/fork/config/schema не найден после primary paper/author/GitHub tracing. Это public artifact gap, не отсутствие capability. Paper p=0.2 — whole-batch probability; tau_i=0 — все synthetic background regions в RPN+head. Low-data COCO не применяет filtering/background-ignore. LVIS ablations немонотонны, COCO/XPaste comparison имеет отдельное происхождение. Fully reviewed whole synthetic images + ordinary supervised detector — наш data-only route, не reproduction Gen2Det. Equal updates при replacement не означает equal real exposure; draw ledger обязателен.\n\n**QAT — F255–F261.** NVIDIA YOLOv7 finetune использует feature reconstruction MSE без detector GT loss. Это не supervised обучение новых PPE classes; labels нужны для оценки. Добавление detection loss — новый port с matched controls. Reference toolkit 2.1.2 не доказанная historical author environment. QDQ signedness/axes/fusion/rules/opset13 не LinQ arithmetic match. README 640 и script 672, mixed head precision ограничивают перенос AP/FPS. Найденный MMrazor RetinaNet config — PTQ.\n\n**Physical pruning — F262–F271.** TP 1.6.1 + old Ultralytics 8.0.90, C2f_v2, patched trainer/save и full-object serialization. Не current U 8.4.184 или YOLO11. Conversion-only parity нужна отдельно от surgery; original YAML + plain state_dict не восстанавливают topology, clean process должен импортировать custom class. Toy coco128 override опасен custom ontology. Speed_up в script — MAC ratio. Demo break не откатывает последний rejected stage перед export. Smoke/reload/FP export/compiler acceptance новых dense shapes нужны до recovery. Меньший штатный student — comparator, LinQ speed неизвестна.\n\n**Checkpoint — F272–F277/F193.** on_model_save после validation/write до strip позволяет immutable serialized EMA candidates и внешний constrained winner. on_train_epoch_end рано для текущей val; on_train_end поздно; on_fit_epoch_end имеет дополнительный final call. Pre-strip содержит EMA FP16 вместо online weights; scheduler/RNG/loader/gradients отсутствуют. Exact continuation не обеспечивается и до strip. Freeze разрешён при resume, LR/optimizer/epochs нет. Новая stage2 с новым recipe — resume=False, новые optimizer/EMA/warmup; supervised явно distill_model=None. Boolean resume stripped может стать warm start. Учитель/projectors нужны interrupted KD resume, а не final inference.\n\n**Queue/fidelity — F278–F284.** Short epoch budget может менять auto optimizer, warmup, scheduler и close_mosaic; это другой recipe, не автоматически prefix. Hyperband/ASHA не гарантируют detector early ranking. Correctness smoke не позволяет kill по низкому early AP без представленного critical support. Admission зависит от полного critical path до useful artifact, annotation/review/SDK owners и D_useful; GPU utilization не цель.\n\n## Публикационные числа: сохранять исходный вопрос сравнения\n\nВ F008/F009 TFA shot — instance/class, не frame или independent scene; sample-set variance не optimizer seed. F011 различает pretraining gain и convergence cost, сохраняя внутреннее 3.4/3.5 расхождение scratch. F033–F035 LVIS — mask AP и long-tail ablation, не PPE box/event forecast. F072–F079 SAHI — aerial AP50, с negative large-object effect, abstract/table deltas и current config differences. F102–F111 SoftTeacher/UTv1 — разные paper/README/teacher/student/threshold contracts; uniform/Gaussian jitter и LR 110k/120k не смешиваются.\n\nF130–F140/F251 содержат полезные negative synthetic mixes, context/contour/mask/GT ограничения; robot cm не detection AP. F121–F126 FGD/LD дают detection-specific evidence при своих grids/GT/bins, не готовый loss любой YOLO. RAW_FACTS хранит все значимые численные строки и протоколы: основной текст может выбирать примеры, но не превращать headline gain в обещание target результата.\n\n## Восемь сценариев и очередь\n\n| Входы | Одно следующее различающее действие |\n|---|---|\n| Open data и weights | E001 zero-update, actual input, target diagnostic GT и ранний G4 |\n| Немного полных target labels | E004 limited vs full; E048 заменяет эту пару только если initialization главный вопрос |\n| Target video без labels | Один assistance-vs-manual cost/admission pilot E023/E024; затем corrected labels E025 либо manual |\n| Разные камеры | E021 object против camera rules; при detector error E019 target-only vs один replay mix |\n| Partial labels | E007 A/B/C metadata→assignment→loss gate до union training |\n| Rare/new/tiny | E009/E003 причина; затем один input E016, balancing E010 или независимая annotation addition E043 |\n| Working model misses/FP | E002 oracle objects/association; потом один targeted data/augmentation trial |\n| Хорошая FP модель дорога или портится после conversion | E037 adjacent-stage parity либо native smaller detector comparator при proven compute bottleneck |\n\nПолная таблица восьми сценариев с artifact/kill/promote/rollback и readiness дорогих routes сохранена в RAW_FACTS, блок W2-12. Сначала earliest failed/unknown gate. E001–E050 — reused gates и условные альтернативы под E051, не mandatory grid. Передавать текущий working bundle сразу с честным статусом; новая ветка допускается, если now + CP_remaining <= D_useful. При отсутствии target execution FP candidate имеет статус target-unverified. Previous accepted bundle не перезаписывается; rollback включает weights, preprocessing, class map, postprocessing и rules.\n\n## Передача соседним topics и границы автора\n\nmodel_stack нужны Q005/Q006/Q013/Q021–Q025: actual loaders, heads, masks/BN, branches, saver/extraction и hashes/locks. datasets нужны Q001–Q004/Q011/Q019: original coverage, lineage, groups, no-box complete review, unknown states, train-only assets и calibration roles. evaluation нужны Q004/Q010/Q011/Q026/Q031: constrained selection, support/exposure, grouped paired uncertainty, thresholds/rules отдельно weights, serialized candidate evaluator.\n\nviolation_methods получает Q001/Q017/Q029: visibility, relations и temporal context, oracle attribution до training. linq_platform/video_architecture получают Q007–Q009/Q031: фактический device/SDK/quant/operator/shape/sample/placement, canonical inputs, decoder/NMS и target timing. operator_product/hackathon_strategy получают Q010/Q012/Q027: измеренный human effort, useful deadline/owner, supported scope и target status. Соседние отчёты не предполагаются существующими; внешних сообщений не было.\n\nK002/K004/K005/K006/K011/K012 закрыты в public/methodical scope; K001/K003/K007/K009/K010 уточнены; K008 author-artifact gap открыт. Следующий этап — большой самостоятельный русский черновик по ROLE_PROMPTS, затем редактор и machine compressor. Автор не получает новую сеть, не заполняет gaps из памяти и не превращает unknown в обещание. Дополнительный финальный аудитор запрещён.\n\n'
(root/'_WORK/AUTHOR_HANDOFF.md').write_text(handoff,encoding='utf-8')
print('AUTHOR_HANDOFF SAVED',len(handoff))


(root/'_WORK/ID_MAP.md').write_text((root/'_WORK/ID_MAP.md').read_text(encoding='utf-8')+'\n\n## Контроль самой сборки внутри роли COLLECTOR\n\nОпределены 220 S, 284 F, 51 E, 31 Q; дополнены все12 K outcomes. Проверены UTF-8 без replacement characters, существование внутренних файлов/числовых anchors и определённость global S/F/E/Q references в шести выходах роли. Ошибок не обнаружено. Источники выделяются в metadata blocks (максимальный исходный source block1138символов), fact/experiment blocks в реестр не захвачены. Короткие branch ranges раскрыты перед merge; W2 поправки стоят у затронутых ранних facts. Это контроль нормализации текущей роли, не отдельная финальная проверка будущих отчётов. Новых сетевых/модельных действий нет.\n',encoding='utf-8')
