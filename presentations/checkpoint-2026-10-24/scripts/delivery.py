"""Finalize the delivery index only after all real checks have completed."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
browser=read('evidence/browser-r2/report.json')
craft=read('evidence/craft-r2/report.json')
exports=read('evidence/exports/report.json')
pdf=read('evidence/pdf-report.json')
content=read('evidence/content-report.json')
index=read('research/source-snapshots/source-index.json')
manifest=read('review-r2/manifest.json')
assert browser['status']=='PASS' and browser['sourceStable'] and not browser['errors']
assert browser['humanReview']['checkedVerdicts']==0 and browser['humanReview']['items']==8
assert browser['sequence']['status']=='PASS' and browser['sequence']['plannedHoldSeconds']==280
assert craft['status']=='CAPTURED' and craft['sourceStable'] and len(craft['screenshots'])==32
assert all(source['status']=='MATCH' for source in craft['sources'])
assert exports['status']==pdf['status']==content['status']=='PASS'
assert exports['powerPointOpenRenderExport']=='PASS' and exports['slides']==8
assert manifest['review']['revision']==2 and len(manifest['items'])==8
assert sha('review-r2/manifest.json')==(ROOT/'review-r2/manifest.sha256').read_text().strip()
assert sha('exports/SafeWatch_Checkpoint_2026-10-24.pptx')==exports['pptx']['sha256']
now=datetime.now(ZoneInfo('Europe/Moscow')).isoformat()
mae=max(c['powerPointRasterMeanAbsoluteChannelError'] for c in exports['checks'])
elapsed=browser['sequence']['elapsedSeconds']
report=f'''# SafeWatch — проверка готовой презентации

Проверка завершена {now}. Техническое состояние: **готово к Human Review**. Человеческое визуальное принятие не заявлено.

| Проверка | Результат и доказательство |
|---|---|
| PowerPoint | PASS: установленный Microsoft PowerPoint {exports['powerPointVersion']} открыл файл, экспортировал все 8 слайдов, прочитал основные и дополнительные заметки. [Native receipt](evidence/powerpoint/report.json) |
| PPTX | PASS: 8 слайдов 16:9; по одному полноразмерному PNG; встроенные байты совпадают с исходниками; заметки совпадают в XML и PowerPoint. [Receipt](evidence/exports/report.json) |
| Обратный рендер | PASS: максимальная средняя абсолютная разница каналов {mae:.6f} из 255 на слайд. Небольшая интерполяция PowerPoint; встроенные PNG точны. |
| PDF | PASS: 8 страниц, повторный рендер 1920×1080 совпал с PNG пиксель в пиксель. [Receipt](evidence/pdf-report.json) |
| Projection matrix | PASS: 8 × 2 размера × 2 motion-настройки = 32 captures; 0 runtime errors; стабильные источники и совпавшие SHA. [Craft r2](evidence/craft-r2/report.json) |
| Русская типографика | PASS: все символы есть в Golos Text, текстовые границы внутри безопасной зоны, числовые утверждения сверены с первичными JSON. [Receipt](evidence/content-report.json) |
| Визуальный осмотр | Все 8 финальных PNG осмотрены на 1280×720 независимым reviewer; P1 не осталось. [Review](research/independent-visual-review.md) |
| Human Review Engine | PASS: неизменённый renderer v1.1, ревизия 2, 8 items, 0 broken assets, 0 выбранных verdicts; проверены normal/reduced и оба разрешения; inspector открывается. [Browser receipt](evidence/browser-r2/report.json) |
| Полная последовательность | PASS: 280 с запланированных выдержек; фактически {elapsed:.1f} с с переходами и записью. [Видео](evidence/browser-r2/complete-280s-sequence.webm) — без речи, служебная QA-последовательность. |
| Stateful-мок | Заново PASS 30 / FAIL 0 / SKIP 0; 26 REST-ответов и 32 WS-сообщения. [Raw](research/smoke-mock-fresh.json) |
| Настоящий frontend | Повторно пройден оператор → мастер → меры → журнал на front/control-room@8161719d и совместимом моке. [Происхождение снимков](research/frontend-evidence.md) |

Граница проверки: DOM critic не читает текст внутри PNG; его 32 `missing-assertion` сохранены. Восемь craft-advisory и неизвестный официальный rubric также не превращены в автоматический PASS. Отдельная точная типографика и ручной осмотр дополняют этот пробел. Микротекст UI-снимков — визуальное доказательство экрана; ключевые подписи вынесены крупно.

Две индустриальные иллюстрации созданы встроенным image_gen; версия модели инструментом не раскрыта. Все реальные UI-снимки получены с запущенного приложения. Камерные кадры в demo синтетические, рамки ручные, видео/эфир отсутствует; ожидаемый camera/view 501 документирован. Это не качество нейросети и не подключение камер завода.

Новых TPU-запусков и повторного запуска ML/backend-тестов не было. Результат 335 программных проверок взят из отчёта ветки Матвея. Hardware execution и качество разграничены; отрицательный результат Fall сохранён. Стабильный общий LinQ-прогон, независимое качество, ложные тревоги/камера-час и alert latency ещё открыты. Источники и время заморозки — [SOURCES.md](SOURCES.md).

Человеческий checkpoint: **HUMAN_SAFEWATCH_CHECKPOINT_PRODUCTION_REVIEW**. [Финальный пакет](review-r2/). Ни одно решение человека не выбрано, не импортировано и не отправлено. Реальная проекция в зале, устная репетиция и персональная скорость выступления не проверены.

Ревизия 2 исправляет только хронологическую формулировку в заметках слайда 8. Все восемь PNG byte-identical между ревизиями. Нативный экспорт, Craft captures, HRE и полная последовательность повторно проверены после исправления. Первая ревизия сохранена как техническая история.
'''
(ROOT/'VERIFICATION.md').write_text(report,encoding='utf-8')
files=['exports/SafeWatch_Checkpoint_2026-10-24.pptx','exports/SafeWatch_Checkpoint_2026-10-24.pdf',
       'preview/SafeWatch_8_slides.png','speaker-notes.json','SPEAKER_SCRIPT.md','SOURCES.md',
       'VERIFICATION.md','craft/story.json','craft/adapter.json','review-r2/manifest.json']+[f'slides/slide-{n:02}.png' for n in range(1,9)]
delivery=dict(status='READY_FOR_HUMAN_REVIEW',verified_at=now,slides=8,
    human_acceptance='NOT_ASSERTED',checkpoint='HUMAN_SAFEWATCH_CHECKPOINT_PRODUCTION_REVIEW',
    branch='codex/safewatch-checkpoint-pptx',source_index_verified_at=index['verified_at_utc'],
    sources=index.get('frozen_heads',{}),files=[dict(path=p,sha256=sha(p),bytes=(ROOT/p).stat().st_size) for p in files],
    checks=dict(powerPointOpenRender='PASS',projectionCaptures=32,sourceRecordsMatched=32,
                nativeMaxMeanChannelError=mae,pdfPixels='IDENTICAL',humanReviewVerdicts=0,
                browserErrors=0,sequenceSeconds=elapsed,freshMock='30/30'))
(ROOT/'DELIVERY.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'SHA256SUMS.txt').write_text(''.join(f"{sha(p)}  {p}\n" for p in files),encoding='utf-8')
assetfiles=[p for p in (ROOT/'assets').rglob('*') if p.is_file() and p.name!='manifest.json']
assets=dict(generation=dict(route='built-in image_gen.imagegen',count=2,model_version='NOT_EXPOSED',prompts='prompts/industrial-artwork.md'),
    screenshots=dict(frontend='8161719d687083c7a3578b0f5de8bc2043a95ce1',mock='9f652236589698857ba05eabbcf361b4ab3779b2',provenance='research/frontend-evidence.md'),
    files=[dict(path=str(p.relative_to(ROOT)),sha256=sha(str(p.relative_to(ROOT))),bytes=p.stat().st_size) for p in sorted(assetfiles)])
(ROOT/'assets/manifest.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':delivery['status'],'slides':8,'human_acceptance':'NOT_ASSERTED','report':'VERIFICATION.md'}))
