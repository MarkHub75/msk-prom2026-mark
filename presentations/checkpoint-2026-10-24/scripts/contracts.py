"""Bind final image slides to the permanent OS Craft source/story contract."""
from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p,obj): (ROOT/p).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
notes=read('speaker-notes.json')
sourceindex=read('research/source-snapshots/source-index.json')
sources=[]
for i,entry in enumerate(sourceindex['sources'],1):
    p='research/source-snapshots/'+entry['snapshot']
    sources.append(dict(id=f'src{i:02}',path=p,sha256=sha(p),kind='product',
        locator=f"{entry['commit']}:{entry['path']}; original lines {entry['original_line_ranges'] or 'whole blob'}; snapshot index records Git blob and hashes"))
extras=[('smoke','research/smoke-mock-fresh.json','fixture','Fresh isolated stateful mock smoke 24.10.2026:30 PASS/0 FAIL/0 SKIP'),
        ('frontend','research/frontend-evidence.md','research','New front/control-room runtime capture and interactions 08:28–08:29 MSK'),
        ('audit','research/technical-evidence.md','research','Semantic audit, history reconciliation and explicit limitations'),
        ('composition','evidence/composition.json','research','Exact slide text and ink bounds; UI crop provenance'),
        ('sources','SOURCES.md','research','Claim/source index after fetch')]
for ident,p,kind,locator in extras:
    sources.append(dict(id=ident,path=p,sha256=sha(p),kind=kind,locator=locator))
def find(path,ref=None):
    return [f'src{i:02}' for i,e in enumerate(sourceindex['sources'],1) if e['path']==path and (ref is None or e['ref_at_verification']==ref)]
tech=find('tech.md');progress=find('progress.md');linq=find('docs/linq/LINQ_CONTRACT.md')
ml=find('ml/EVAL_REPORT.md')+find('ml/RELEASE_MANIFEST.json')+find('ml/reports/pose-linq-ur01-parity.json')
assertions=['Промышленная безопасность','Видео → событие → действие','LinQ: реальное исполнение на TPU',
    'Собственные модели дошли до TPU','Готовность по слоям','Проверяем путь реакции',
    'До финальной защиты','Вопросы экспертам LinQ']
claims=[
    [('roles','Оператор проверяет событие; мастер реагирует; охрана труда анализирует журнал.',tech,'Целевой процесс; наличие пяти ролей не равно готовности пяти рабочих мест.')],
    [('architecture','Видео → Jupyter → TPU → JSONL → CPU → эпизоды → эмуляция → WS → оператор → мастер → журнал.',tech,'Целевой конвейер архива/эмуляции; стабильная интеграция TPU и настоящий журнал ещё открыты.')],
    [('baseline','400 кадров1280×720;19.09с;20.95FPS;31с с загрузкой.',linq+find('results/linq_smoke/synthetic_coco_40x1s_mosprom_det640_cut_ap9999_b1_o1_h1m_s1.summary.json'),'Detector test video-run inflight8; не общий detector+pose pipeline и не alert latency.'),
     ('timeout','Поздний интегрированный backend получил TPU timeout.',progress,'Не отменяет ранний успешный отдельный baseline smoke.')],
    [('own-hardware','Helmet и Split-Pose имеют correlated status0 TPU captures.',ml,'По свежим сохранённым отчётам ветки; raw hardware captures вне Git; здесь не rerun.'),
     ('software','335 software tests PASS.',ml,'Программные проверки по отчёту ветки, не335 измерений качества CV.'),
     ('fall','URfall01: аппаратные ответы получены, одно падение пропущено.',ml,'Один development clip; Fall quality NOT_ACCEPTED; independent final test NOT_RUN.')],
    [('main-readiness','В main закрыты S0–S10 с долгами; журнал S12 ещё в работе.',progress+['audit'],'Статус документов и кода, не повторный product gate в этой сессии.'),
     ('mock-smoke','Свежая проверка stateful-мока:30/30.', ['smoke'],'Это mock backend, не real backend и не LinQ.'),
     ('ui','Текущая диспетчерская и действия работают на совместимом моке.', ['frontend'],'Синтетические still previews; видео/эфир501; не реальные подключённые камеры.')],
    [('demo','Оператор → красная передача → мастер → меры → журнал пройдены в браузере.', ['frontend'],'Демонстрационные данные. Кадры синтетические. Рамки размечены вручную.')],
    [('remaining','Интеграция, независимые метрики и оставшиеся сценарии ещё открыты.',progress+ml,'Без обещаний сроков и чисел.')],
    [('questions','Время непосредственно на TPU и стабильность интегрированной очереди остаются открыты.',linq+progress,'Вопросы экспертам, без предположения о критериях жюри.')]
]
scenes=[]
for i,note in enumerate(notes):
    scenes.append(dict(id=f'{i+1:02}',audienceTakeaway=assertions[i],assertion=assertions[i],
        evidence=note['sources'],protagonist=['Опасное событие и роли','Цепь от видео к реакции','Измеренный baseline video-run','Цепь доказательств собственных моделей','Матрица готовности и актуальный frontend','Три состояния реального пользовательского пути','Приоритеты до защиты','Открытые вопросы экспертам'][i],
        readingOrder=['assertion','evidence','qualification'],
        composition=['Industrial image and role chain','Three connected processing lanes','Monumental throughput with measured times','Model proof ladder plus negative quality result','Status ledger beside current screenshot','Three captured interaction steps','Priorities against illustrative industrial camera','Four expert questions with calm visual hierarchy'][i],
        groups=[dict(id='assertion',role='assertion',description=assertions[i],essential=True),
                dict(id='evidence',role='evidence',description='Exact source-backed final PNG including graphic evidence',essential=True),
                dict(id='qualification',role='qualification',description='Visible limitations; additional detail in native notes',essential=True)],
        attentionRationale='One assertion and a dominant evidence region. Technical diagrams may contain more nodes; reading order is causal.',
        motion=dict(rationale='Static image slide; presenter advances manually in PowerPoint.',continuity='Order preserves product → architecture → evidence → readiness → demo → gaps → questions.',holds=['Entire final slide'],reducedMotion='Identical static pixels, no motion.'),
        speakingNotes=note['speech']+'\n\n'+note['notes'],
        claims=[dict(id=a,text=b,kind='factual',sourceIds=c,qualification=d) for a,b,c,d in claims[i]],rubricIds=[]))
story=dict(version='1.0.0',id='safewatch-checkpoint-20261024',audience='Технические эксперты Моспром2026 и LinQ',
    scope='Восемь image-based PowerPoint слайдов технического чекпойнта; продуктовый код не меняется.',
    sequenceRationale='Показать продуктовую задачу, архитектуру, подтверждённые hardware результаты, ограничения качества, текущие UI действия и приоритеты.',
    rubric=dict(status='unknown',source=None,criteria=[]),sources=sources,scenes=scenes)
write('craft/story.json',story)
inputs=['scripts/compose.py','speaker-notes.json','evidence/composition.json','craft/capture.html','craft/story.json']+[f'slides/slide-{n:02}.png' for n in range(1,9)]
adapter=dict(version='1.0.0',root='..',story='story.json',fixture='safewatch-checkpoint-20261024',runtime='dom',baseUrl='http://127.0.0.1:8724/',
    browserPluginReason='Browser plugin not available; existing OS Playwright/Chromium. Raster text is outside DOM probe coverage; missing-assertion findings retained and typography checked separately.',
    sourceFiles=inputs,probe=dict(stage='#stage',safeMargin=.05,minimumTextPx=24),
    holds=[dict(id=f'{i+1:02}',scene=f'{i+1:02}',url=f'craft/capture.html?slide={i+1}',
        probe=dict(assertion=dict(selector='#slide',text=assertions[i]),groups=[dict(id='evidence',selector='#slide',essential=True,
            safeException='Intentional full-bleed raster. Exact text glyph coverage and safe ink bounds checked in composition.json; manual 720p review required.')])) for i in range(8)])
write('craft/adapter.json',adapter)
script=['# SafeWatch — сценарий технического чекпойнта','',
    'План: 280 секунд (4:40), включая короткую демонстрацию. Это бюджет времени, не замер речи. Дополнительные технические пояснения находятся в заметках PowerPoint.','']
for i,n in enumerate(notes,1):
    script += [f"## {i}. {n['title']} · {n['duration']} с",'',n['speech'],'']
(ROOT/'SPEAKER_SCRIPT.md').write_text('\n'.join(script),encoding='utf-8')
print('Story, source hashes, adapter and280s speaker script written; no human decision generated.')
