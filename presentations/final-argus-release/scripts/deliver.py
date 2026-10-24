from pathlib import Path
import json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
exp=read('evidence/exports-13/report.json');craft=read('evidence/craft-13/report.json');qa=read('evidence/browser-quick/report.json')
assert exp['status']=='PASS' and exp['slides']==13 and exp['powerPointOpenRenderExport']=='PASS'
assert craft['status']=='CAPTURED' and craft['sourceStable'] and len(craft['screenshots'])==52 and not craft['runtimeErrors']
assert qa['status']=='PASS' and not qa['errors'] and qa['humanReview']['checkedVerdicts']==0
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
text='''# Проверено перед сдачей

13слайдов1920×1080,готовые PPTX/PDF и единое превью. Все слайды просмотрены в720p; проверены глифы,границы и пересечения текста. Реальный LinQкадр на9слайде сохранён целиком,без обрезки подписей; речь пользователя вставлена дословно.

Microsoft PowerPoint16 открыл и экспортировал все13слайдов. Встроенные PNG побайтно совпадают с исходниками; заметки совпали вXML иPowerPoint. Максимальная средняя разница каналов нативного растра менее0.3/255. PDF отрендерен обратно: все13страниц попиксельно идентичны исходникам; attribution приложен текстовым вложением.

Presentation Craft:52захвата (13сцен×2разрешения×2motion),источники стабильны,ошибок загрузки нет.52missing-assertion — ограничениеDOM для текста внутриPNG;13craft-review и1rubric-unknown сохранены. HRE renderer1.1/contract1.0:13items,86артефактов; валидатор и браузер проверили ресурсы,варианты иинспектор. Решений человека не выбирали.

69тестов frontend наa5e43aff прошли заново,код не менялся.352backend — по отчётуmain.45с — настройка;18FPSCPU и45.2с не подтверждены ине используются. LinQ результаты — сохранённые реальные ответы и отдельныйbaseline; новых TPUзапросов не делали,промышленное качество не объявляем измеренным.

Полный тихий300секундный прогон остановлен/опущен по прямому приоритету пользователя успеть до18:00. Это не влияет на выполненные проверки всех изображений,PowerPoint,PDF иHRE. Озвученная репетиция и проекция в зале не проверялись. Human acceptance остаётся PENDING. Более ранние12-слайдовые проверки и неуспешная HREревизия с неверными метаданными исходногоJPEG сохранены как история. Файл пользователя с расширениемPNG фактическиJPEG; вфинальном HRE MIME и размеры определены декодером,байты не менялись.
'''
(ROOT/'VERIFICATION.md').write_text(text+'\nЗавершено: '+stamp+'\n',encoding='utf-8')
paths=['exports/ARGUS_Final.pptx','exports/ARGUS_Final.pdf','exports/ATTRIBUTION.txt','preview/ALL_13_SLIDES.png','SPEAKER_SCRIPT.md','SOURCES.md','VERIFICATION.md','research/source-index.json','research/linq-proof-index.json','evidence/exports-13/report.json','evidence/craft-13/report.json','evidence/browser-quick/report.json','review-final/manifest.json']+[f'slides/slide-{n:02}.png' for n in range(1,14)]
data=dict(status='READY_FOR_DELIVERY',checked_at=stamp,slides=13,human_acceptance='PENDING',branch='codex/argus-final-presentation',sources=read('research/source-index.json')['heads'],artifacts=[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=sha(p)) for p in paths])
(ROOT/'DELIVERY.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p}\n' for p in paths),encoding='utf-8')
print('READY:13slides,PPTX,PDF,preview; native and projection QA passed; long hold sequence omitted by user deadline.')
