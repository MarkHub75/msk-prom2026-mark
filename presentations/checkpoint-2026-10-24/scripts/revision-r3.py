"""Bounded requested revision: current UI, notes, sources; no product changes."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1]
repo=ROOT.parents[1]
def write(p,s): (ROOT/p).write_text(s,encoding='utf-8')
def js(p,v): write(p,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
heads={name:subprocess.check_output(['git','rev-parse','origin/'+name],cwd=repo,text=True).strip() for name in ['main','front/control-room','demo/checkpoint']}
out=ROOT/'research/revision-r3';out.mkdir(exist_ok=True)
snapshots=[]
for ref,path,name in [('main','progress.md','progress.md'),('main','src/safewatch/services.py','services.py'),('front/control-room','frontend/src/features/Operator.tsx','Operator.tsx'),('front/control-room','frontend/src/styles/pro-skin.css','pro-skin.css')]:
    data=subprocess.check_output(['git','show',heads[ref]+':'+path],cwd=repo)
    (out/name).write_bytes(data)
    snapshots.append(dict(ref=ref,commit=heads[ref],path=path,snapshot='research/revision-r3/'+name,sha256=hashlib.sha256(data).hexdigest()))
js('research/revision-r3/source-index.json',dict(verified_at=datetime.now(ZoneInfo('Europe/Moscow')).isoformat(),heads=heads,sources=snapshots))
notes=json.loads((ROOT/'speaker-notes.json').read_text())
for n in notes:
    n['notes']=n['notes'].replace('http://127.0.0.1:5317','http://localhost:5173').replace('localhost5317','localhost:5173').replace('localhost5317','localhost:5173').replace('REST4310,WS4311','REST4010,WS4011').replace('на4310/4311','на4010/4011').replace('REST4310,WS4311','REST4010,WS4011').replace('WS4311','WS4011')
    n['notes']=n['notes'].replace('8161719d','1b8822ef').replace('9f652236','053683da')
    n['sources']=[s.replace('front/control-room@8161719d','front/control-room@1b8822ef').replace('demo/checkpoint@9f652236','demo/checkpoint@053683da') for s in n['sources']]
notes[1]['notes']=notes[1]['notes'].replace('Показанный журнал работает на моке; real backend S12 ещё не реализован.','Показанный журнал работает на моке. В свежем main журнал уже реализован; интеграция текущего frontend проверяется здесь на моке.')
notes[4]['speech']='Проверенная основа backend и контракта включает S0–S11 с записанными долгами. Стабильность LinQ отдельно не доказана. Правила детекции проверялись на синтетике. На экране — новый снимок текущего control-room: тёмный Premiere-скин, быстрые действия прямо в панели, сводка смены и видимое отсутствие наблюдения. Путь оператора до мастера и журнал проверены на совместимом моке. Дополнительные модели и оставшиеся сценарии требуют дальнейшей проверки.'
notes[4]['notes']='Снимки заново получены с front/control-room@1b8822ef и tools/checkpoint-demo@053683da. Показ: http://localhost:5173, мок REST4010 и WS4011. Последовательность reset → next → next --force. В матрице указана запрошенная проверенная основа S0–S11; свежий main продвинулся дальше. Журнал и статистика backend уже реализованы по текущему коду, но демонстрация остаётся на stateful-моке. Камерные кадры синтетические, рамки ручные. Новых численных результатов CV эта правка не добавляет.'
notes[4]['sources']=['main@'+heads['main']+':progress.md','front/control-room@'+heads['front/control-room']+':frontend/src/features/Operator.tsx','research/frontend-evidence.md','research/revision-r3/source-index.json']
notes[6]['speech']='До защиты нужно стабилизировать интегрированный прогон LinQ, подключить свои модели в общий конвейер и измерить качество на размеченных видео. Отдельно оценить ложные тревоги на камеро-час и задержку до оповещения. Наше отличие — полный цикл тревоги до мастера, сводка смены, видимое отсутствие наблюдения и происхождение каждого события. Ближайший конкурент на LinQ в позиционировании команды — IVA CV.'
notes[6]['notes']='Приоритеты сохранены без новых чисел и сроков. Журнал backend уже реализован в свежем main. Формулировка «ближайший конкурент» — позиционирование команды, а не независимый рейтинг или сравнение качества. Официальная страница IVA CV https://ivacv.ru/platforma/ прямо перечисляет поддержку LinQ(TPU); https://ivacv.ru/iva-cv/ описывает видеоаналитику безопасности. Отличия SafeWatch перечисляют проверенный пользовательский путь и наблюдаемость, не утверждают отсутствие таких функций у IVA CV.'
notes[6]['sources']+=['https://ivacv.ru/platforma/','https://ivacv.ru/iva-cv/','research/revision-r3/source-index.json']
js('speaker-notes.json',notes)
update=f'''\n\n## Правка r3 по запросу владельца\n\nПроверено {datetime.now(ZoneInfo('Europe/Moscow')).isoformat()}. Текущие refs: main `{heads['main']}`, front/control-room `{heads['front/control-room']}`, demo `{heads['demo/checkpoint']}`. В слайде оставлена запрошенная основа S0–S11; свежий progress уже продвинулся дальше. Устаревшие заявления о неготовом журнале сняты. Новые численные метрики не добавлялись.\n\nIVA CV поддерживает LinQ(TPU) по официальной [странице платформы](https://ivacv.ru/platforma/). «Ближайший конкурент» — позиционирование команды из запроса владельца, не измеренный рейтинг. Перечень отличий не означает отсутствие аналогичных функций у конкурента.\n\nСнимки: текущий Premiere-скин, быстрые действия и сводка смены; frontend http://localhost:5173, мок4010/4011; reset → next → next --force. Источники новой готовности: [r3 source-index](research/revision-r3/source-index.json). Предыдущие разделы ниже/выше описывают историческую ревизию и не подменяют этот актуальный update.\n'''
for path in ['SOURCES.md','research/technical-evidence.md']:
    write(path,(ROOT/path).read_text()+update)
print('r3 notes and current source snapshots updated.')
