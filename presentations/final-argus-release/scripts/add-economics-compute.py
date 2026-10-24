"""Idempotent additions to the original thirteen-scene narrative and export tooling.

Run after story.py (also invoked there), before exports.mjs. Operating settings
come from the user's brief; they are not a newly measured hardware benchmark.
"""
from pathlib import Path
import copy, hashlib, json, re
ROOT = Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def write(p, data): (ROOT/p).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
compute = dict(title='Как Argus экономит вычисления',
    speech='Сначала все камеры проходят дешёвую проверку движения на CPU. При движении включается детектор людей на LinQ, а поза и СИЗ проверяются только на вырезке человека; между кадрами детектора работает CPU-трекер. Пустые кадры не доходят до нейросети, полная частота и все модели нужны только в момент события. Поэтому ускорители считаются по пиковой одновременной активности, а не по числу камер.',
    notes='Частоты и пороги на схеме — заданные пользователем режимы архитектуры, не новые замеры этой сессии: движение 5 проверок/с, <1 мс на кадр; детектор людей до 10 кадров/с; контрольный кадр раз в 3–5 с. Вне смены — только движение и тревога охране. Пропускная способность, число камер на ускоритель и процент экономии не заявляются.',
    question='Сколько камер выдержит один ускоритель?',
    answer='Это зависит от пиковой одновременной активности и состава каскада; ёмкость нужно измерить на целевых видео и профиле нагрузки.',
    sources=['compute-user'], duration=30)
economics = dict(title='Экономика',
    speech='По Росстату за 2025 год в обрабатывающей промышленности — 1,17 пострадавшего на тысячу работников в год. КоАП предусматривает для юрлица штраф до 150 тысяч рублей за необеспечение СИЗ второго класса риска, при повторном аналогичном нарушении возможно приостановление деятельности до 90 суток. Во внешнем кейсе АлЭС зарегистрированных нарушений стало меньше на 69 процентов — это данные заказчика за 2026 год, а не снижение травматизма и не результат Argus. Наш эффект — снижение рисков и повторных нарушений, ускорение реакции и меньше ручного контроля; точную окупаемость считаем после пилота, а калькулятор в продукте показывает точку безубыточности при заданных допущениях.',
    notes='Основание: front/final@87f8a2c47d9621c8b7620d20c3c0548c0ebb128a:docs/ECONOMICS_SOURCES.md; точный снимок сохранён в research. Росстат: форма 7-травматизм, данные 2025, опубликованы в 2026. КоАП 5.27.1 ч. 4 и 5, редакция 2026: до 150 тыс. ₽ — за необеспечение СИЗ 2-го класса риска; при повторном аналогичном нарушении для юрлица штраф или приостановление до 90 суток, не оба наказания одновременно. АлЭС: Самрук-Энерго, 2026, данные заказчика о зарегистрированных нарушениях; причинный эффект и переносимость на Argus не доказаны. Срок окупаемости и доля предотвращённых травм не обещаются. Калькулятор показывает условную точку безубыточности; итог требует пилота и реальной сметы.',
    question='Когда окупится Argus?',
    answer='Точную окупаемость считаем после пилота. Калькулятор в продукте показывает точку безубыточности при заданных допущениях; заранее срок не обещаем.',
    sources=['economics-2026'], duration=35)
for item in (compute, economics):
    item['notes'] += '\n\nВОЗМОЖНЫЙ ВОПРОС ЭКСПЕРТА: '+item['question']+'\nКОРОТКИЙ ЧЕСТНЫЙ ОТВЕТ: '+item['answer']
additions = [compute['title'], economics['title']]
notes = [s for s in read('speaker-notes.json') if s['title'] not in additions]
assert len(notes) == 13
notes.insert(8, compute)
notes.insert(12, economics)
for i, item in enumerate(notes, 1): item['id'] = f'{i:02}'
write('speaker-notes.json', notes)
script=['# Сценарий финальной презентации', '', f'15 слайдов. Бюджет речи: {sum(s["duration"] for s in notes)} с — план, не измеренная репетиция.', '']
for item in notes:
    script += [f'## {item["id"]}. {item["title"]}', '', item['speech'], '', item['notes'], '', 'Источники: '+', '.join(item['sources']), '']
(ROOT/'SPEAKER_SCRIPT.md').write_text('\n'.join(script), encoding='utf-8')
story = read('craft/story.json')
scenes = [s for s in story['scenes'] if s['audienceTakeaway'] not in additions]
assert len(scenes) == 13
for position, item, composition in [(8, compute, 'Слева сужающаяся четырёхступенчатая воронка, рядом режим ожидания; справа три крупных тезиса. Графит, приглушённый синий.'), (12, economics, 'Три опорных факта с источниками и годами, ниже эффект и условная точка безубыточности. Графит, приглушённый синий.')]:
    scene=copy.deepcopy(scenes[0])
    scene.update(audienceTakeaway=item['title'], assertion=item['title'], evidence=item['sources'], protagonist=item['title'], composition=composition, speakingNotes=item['speech']+'\n\n'+item['notes'],
        groups=[dict(id='assertion',role='assertion',description=item['title'],essential=True),dict(id='evidence',role='evidence',description=composition,essential=True)],
        claims=[dict(id=item['sources'][0],text=item['speech'],kind='conceptual' if item is compute else 'factual',sourceIds=item['sources'],qualification=item['notes'])])
    scenes.insert(position, scene)
for i, scene in enumerate(scenes, 1): scene['id']=f'{i:02}'
story.update(id='argus-final-release-15', scenes=scenes, scope='15 растровых слайдов; событийные вычисления после архитектуры, экономика после плана пилота.')
source_path='research/front-final__docs__ECONOMICS_SOURCES.md'
brief_path='research/COMPUTE_BRIEF.md'
(ROOT/brief_path).write_text('# Источник схемы вычислений\n\nПользовательский запрос от 24.10.2026. Режимы: все камеры — 5 проверок/с, движение на CPU <1 мс/кадр; движение → LinQ, люди до 10 кадров/с; человек → поза и СИЗ на вырезке; между кадрами — CPU-трекер. Пусто → контрольный кадр раз в 3–5 с; вне смены только движение и тревога охране. Это режимы предложенной архитектуры, не свежие замеры. Число камер на ускоритель и процент экономии не заданы.\n',encoding='utf-8')
for ident, path, locator in [('compute-user',brief_path,'Пользовательский запрос 24.10.2026; режимы архитектуры, без нового бенчмарка'),('economics-2026',source_path,'front/final@87f8a2c47d9621c8b7620d20c3c0548c0ebb128a:docs/ECONOMICS_SOURCES.md')]:
    story['sources']=[s for s in story['sources'] if s['id']!=ident]
    story['sources'].append(dict(id=ident,path=path,sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),kind='research',locator=locator))
write('craft/story.json',story)
adapter=read('craft/adapter.json');adapter['fixture']='argus-final-release-15'
template=copy.deepcopy(adapter['holds'][0]);adapter['holds']=[]
for i, item in enumerate(notes,1):
    hold=copy.deepcopy(template);hold.update(id=f'{i:02}',scene=f'{i:02}',url=f'craft/capture.html?slide={i}')
    hold['probe']['assertion']['text']=item['title']
    for group in hold['probe'].get('groups',[]):group['safeException']='Full-slide PNG; typography checked in composition.json; real LinQ proof is slide 10.'
    adapter['holds'].append(hold)
adapter['sourceFiles']=[s for s in adapter['sourceFiles'] if not s.startswith('slides/')]+[f'slides/slide-{i:02}.png' for i in range(1,16)]
write('craft/adapter.json',adapter)
# Original story.py also regenerates the legacy exporters. Upgrade their fixed count.
for name in ['exports.mjs','pdf-preview.py','verify-exports.py','powerpoint-check.ps1']:
    p=ROOT/'scripts'/name;s=p.read_text(encoding='utf-8')
    s=re.sub(r'(?<![\d.])13(?![\d.])', '15', s)
    s=s.replace('ARGUS_Final.pptx','ARGUS_Final_15.pptx').replace('range(1,14)','range(1,16)').replace('thirteen','fifteen').replace('Thirteen','Fifteen').replace('Тринадцать','Пятнадцать')
    p.write_text(s,encoding='utf-8')
p=ROOT/'craft/capture.html';p.write_text(p.read_text().replace('n>13','n>15').replace('1…13','1…15'),encoding='utf-8')
print('15-scene notes, source ledger and exporters updated.')
