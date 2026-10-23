# Передача fresh-context critic → W2

2026-10-23 07:33 Europe/Moscow (+03:00). Создан [CRITIC.md](../CRITIC.md). Оба входных промпта, PLAN и все шесть W1 прочитаны полностью; RUN_STATE и мнение оркестратора не читались; новой сети, запусков и агентов не было.

Рекомендации W1 в целом обоснованы: conditional LinQ adapter, MediaMTX/PyAV как кандидаты ingest, bounded scheduler, один владелец state/камера, модульный монолит, transactional outbox, encoded recording и processed JPEG+metadata view. Каталог8проектов и честный параметрический50/500 уже достаточны; не повторять их целиком.

Меняют решение прежде всего пять связей:

1. **K001:** local timeout не освобождает server job/credit; нужен persisted job ledger/reconcile после crash, иначе bounded local queue не ограничивает remote work.
2. **K002/K003:** decoder PTS/epoch ещё не сопоставлены с реальными recording segments; неизвестный/неограниченный queue delay несовместим с гарантированным finite pre-roll. Выбрать mapping и конечную acceptance/partial policy.
3. **K004:** atomic processed frame устраняет неправильные рамки, но не WS/TCP/browser decode backlog. Нужны per-viewer bounds/credit/disconnect.
4. **K005:** один inflight/камера имеет свой потолок1/L; tracker с frame-based dt/lost age не станет variable-FPS tracker от наличия timestamps в envelope.
5. **K010:** выбрать один минимальный vertical slice и gates/cuts45ч; GUI-only или job-only с неприемлемым turnaround не превращаются в live приложение простой заменой adapter.

Дополнения P1: K006 return tensors/downlink/NMS/viewer fanout/OS-resource terms; K007 coherent pinned prospective manifest и фактический reuse/license scope; K008 SQLite/WAL durable commit/backup/restore/DB–clips reconciliation. K009 camera tamper P2: ограниченный gap, не blocker и не повод строить новый detector.

## Группы W2

| Файл | Владение | Точный результат |
|---|---|---|
| `_WORK/W2_01.md` | A: K001 + return K006 | Remote-job state machine/ledger/unknown-terminal credit; один первичный job API аналог; response-size/downlink/postprocess contract |
| `_WORK/W2_02.md` | B: K002/K003 | Pinned MediaMTX recording/time/hooks/export path; event→segment manifest; finite ring/late result/ongoing pins/partial lifecycle |
| `_WORK/W2_03.md` | C: K004 | Один конкретный Python WS route с documented backpressure; bounded per-viewer render-credit protocol и frame lifetime |
| `_WORK/W2_04.md` | D: K005 | Один pinned lightweight tracker dt/gap/reset; per-camera service ceiling и sequential/reorder switch prerequisites |
| `_WORK/W2_05.md` | E: K007/K008 | Coherent provisional release/artifact/license manifest; SQLite/WAL/current caveats/backup/recovery и commit boundary |
| `_WORK/W2_06.md` | F: K006(view/resources)/K009/K010 | Недостающие50/500 topology terms; короткий camera-health scope; автору minimum45ч, owners/gates/cuts/per-mode symbolic budgets/E consolidation |

Полное задание каждого K-ID, точные затронутые W1 и local S/F/Q/E IDs находятся в CRITIC.md. Не передавать только заголовок группы: передать K-ID и исходный материал. Новую сеть получают Medium-исследователи. F может начать по W1, затем учесть выходы A–E; E согласует версии с B/C. Достаточно очередей с доступным лимитом слотов.

Не тратить W2 на повтор рекламных страниц LinQ, сравнение всех брокеров, расширение каталога ради названий, benchmark чужого GPU ради числа камер, универсальный JPEG Q, новый native WebRTC overlay если выбран atomic processed view, или CPU per-core capacity неизвестного компьютера. Такие unknown закрываются доступом, inventory, full case или учебным E.

Collector после W2 сохраняет исходную критику неизменной и дописывает статусы обработки K001–K010 с доказательствами. Отдельного финального аудита не создавать.
