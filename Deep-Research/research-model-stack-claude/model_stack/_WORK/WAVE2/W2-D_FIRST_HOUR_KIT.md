# W2-D FIRST_HOUR_KIT — набор первого часа с SDK LinQ

(черновик, пишется по ходу работы; финальные разделы дописываются ниже)

## Шапка

- ID ячейки: W2-D (вторая волна). Закрывает K003, K004, K005, K012, K024, K025.
- Запрошено: Claude Sonnet 5.5, effort high.
- Фактическая модель (из системного окружения агента): **Sonnet 5.5, model ID `claude-sonnet-5-5`**. Effort: заявлен оркестратором «high»; сам параметр в окружении агента не виден (unknown).
- Начало: 2026-10-23 ~05:30 MSK (UTC+3; `date` в среде показывает «RTZ 2»). Конец: см. конец файла.
- ROOT = `C:\Users\User\Documents\mosprom2026-hack\research-model-stack-claude\model_stack`
- Каталог артефактов (небольшие файлы, в ROOT): `_WORK\WAVE2\W2-D_files\kit\`. Большие .onnx/.npy: `<SCRATCH>\kit-W2-D\` (манифест sha256 и команда воспроизведения — ниже).

## FLASH

### FLASH-1 (записан первым, 05:3x MSK). Номенклатура графов W2-D (для W2-C и W2-E)

Идентификатор графа: `<M>.<head>.op<N>[.<in>]`, файл `<SCRATCH>\kit-W2-D\graphs\<M>\<M>.<head>.op<N>[.<in>].onnx`. Все варианты одной модели и одного opset получены **из одного и того же официального экспорта `full`** (Ultralytics 8.4.184, `format="onnx"`, `opset=N`, `imgsz=640`, `batch=1`, `dynamic=False`, `simplify` по умолчанию), срезом `onnx.utils.extract_model` до выходов финальных Conv головы и доклейкой простых узлов (Sigmoid/Reshape/Concat). Следовательно backbone/neck/веса/opset у `full` и `raw*` совпадают по построению (закрывает «смешение opset» из K004).

| `<M>` | модель (вес) |
|---|---|
| `v8n`, `v11n`, `v26n` | `yolov8n.pt`, `yolo11n.pt`, `yolo26n.pt` (nc=80) |
| `v5s7` | yolov5s v7.0 (репозиторий yolov5 tag v7.0, `yolov5s.pt`; anchor-based, nc=80) |
| `v8n-pose`, `v11n-pose`, `v26n-pose` | `yolov8n-pose.pt`, `yolo11n-pose.pt`, `yolo26n-pose.pt` (nc=1, kpt_shape [17,3]) |
| `mnv2` | torchvision `mobilenet_v2` (классификатор, 1000 логитов) |

| `<head>` | что выходит | выходы (имена `output_names`) |
|---|---|---|
| `full` | штатный экспорт с `nms=None` (по умолчанию); v8/v11/v5u: `[1,4+nc,A]` xywh px + sigmoid-вероятности; YOLO26: one2many `[1,4+nc,A]` (внешний NMS) | `output0` |
| `e2e` | только YOLO26 (и v26n-pose): `nms=False` → `[1,300,6]` (pose: `[1,300,57]`), NMS-free one2one | `output0` |
| `raw6-logit` | 6 выходов = выходы финальных Conv: `box_s8/16/32` `[1,4*reg_max,H,W]` (v8/v11: 64; v26: 4), `cls_s8/16/32` `[1,nc,H,W]` **логиты, без Sigmoid** | `box_s8,box_s16,box_s32,cls_s8,cls_s16,cls_s32` |
| `raw6-sig` | как `raw6-logit`, но на cls добавлен `Sigmoid` (определение W1-10) | те же имена |
| `raw2-logit` | 2 выхода: `box` `[1,4*reg_max,A]` и `cls` `[1,nc,A]` (flatten H·W, Concat по уровням в порядке s8,s16,s32, логиты) | `box,cls` |
| `raw9-logit` (pose) | 9 выходов: `box_s*`, `cls_s*` (логиты), `kpt_s*` `[1,51,H,W]` (сырые Conv-выходы перед `kpts_decode`) | `box_s*,cls_s*,kpt_s*` |
| `raw3-logit` (pose) | 3 выхода: `box` `[1,64|4,A]`, `cls` `[1,1,A]`, `kpt` `[1,51,A]` | `box,cls,kpt` |
| `raw3-logit` (`v5s7`) | 3 выхода Conv `[1,255,H,W]` (3 якоря × 85, **логиты**) — срез `/model.24/m.{0,1,2}/Conv` | `p3,p4,p5` |
| `logits` (`mnv2`) | `[1,1000]` без softmax | `output0` |

Opset: **{11, 13, 18}** для всех (18 = умолчание 8.4.184; 17 проверен точечно, см. тело). Варианты входа (K025), суффикс `<in>`: *нет* — базовый `images` float32 NCHW 0..1; `.nhwc_u8` — вход `images` **uint8 [1,H,W,3]** → `Cast(float)` → `Transpose(0,3,1,2)` → `Div(255)` внутри графа; `.fold255` — вход float32 NCHW **0..255**, `/255` вшит в веса первого Conv (для mnv2 — ещё и mean/std ImageNet); подробности и инвентарь добавленных операторов — в теле.

Контракты порядка: уровни всегда s8, s16, s32; якоря в `raw2-*` идут строка-за-строкой (y, затем x) по уровням s8→s16→s32 — идентично порядку якорей `full`. Раскладка выходов — NCHW (в `raw6`) независимо от варианта входа.

Эталонные тензоры (K024): `<SCRATCH>\kit-W2-D\refs\` — `in_ref_u8.npy [N,640,640,3]` (после letterbox, RGB), `in_ref_nchw_f32.npy [N,3,640,640]` (/255), `in_ref_nhwc_f32.npy`, `meta.json`; сырые выходы PT/ORT на каждый граф — `refs\raw_<runtime>_<graphID>_<out>.npy` (подробности в теле, появятся ниже).

(Конец FLASH-1. Дальнейшие FLASH ниже по мере появления.)

