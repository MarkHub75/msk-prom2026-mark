"""Editorial cleanup of this researcher's individual outputs only."""
from pathlib import Path
root=Path('_WORK')
root.joinpath('W2-10.md').write_text('''# W2-10 — Önal/Dandıl: manifest и реальное заводское replay

K010; W2-C. Доступ 23.10.2026; продолжение зафиксировано clock в 03:40:57 UTC / 06:40:57 Europe/Moscow. **K010 — область уточнена:** реальные replay inputs доступны, но interval/polygon/track/camera-session GT и длительные непрерывные safe periods остаются открытыми.

## Источники и происхождение

| ID | Первичный источник / версия | Полученное и locator |
|---|---|---|
| W2-10-S01 | Önal, O.; Dandıl, E., *Video Dataset for Safe and Unsafe Behaviours*, Mendeley v1, 11.06.2024, DOI10.17632/xjmtb22pff.1 https://data.mendeley.com/datasets/xjmtb22pff/1 | Карточка и статья сохранены W1-07; dataset CC BY4.0. W2 анализирует тот же v1, а не независимый источник. |
| W2-10-S02 | https://data.mendeley.com/public-api/datasets/xjmtb22pff/folders/1 ; files endpoint `https://data.mendeley.com/public-api/datasets/xjmtb22pff/files` | Параметры folder_id, version=1, $start=0, $limit=1000. Реально сохранены folders19entries, rootfiles и каждый leaf response; `FETCH.py`, `MANIFEST.json`, `files-*.json`. Полные metadata, не весь media payload. |
| W2-10-S03 | Восемь MP4 по download_url/UUID из S02 | `MATERIALS/W2-10/SAMPLES.py`, `SAMPLE_OBSERVATIONS.json`, MP4, `.ffmpeg.txt`, extracted JPEG и `CONTACT.jpg`. UUID, bytes и SHA256 каждого файла сохранены в JSON. Доступ23.10.2026. |

## Факты

**W2-10-F01 — выполненный inventory S02.** 691 file entries, все MP4; advertised total 9,999,951,582 bytes. В16leaf class/split folders train566/test125; counts совпали с таблицей W1-07. Rootfiles пуст; annotation sidecar, README, licence file в manifest нет. ClassID_tr/teN и folder дают clip class; отдельные multi-label records, intervals, polygons и tracks не получены. Это ограничение опубликованной структуры, а не доказательство отсутствия unpublished GT. Открытые691clips — около10GB, не4000h raw video.

**W2-10-F02 — выполненное получение S03.** Выбор целенаправленный: safe/unsafe walkway (class0/4), оба official splits, разные размеры и визуальные framing. Получены8samples; полного decode691clips не было.

| Clip | Bytes | Duration s / start s | Displayed fps / tbn |
|---|---:|---|---|
| 0_te23.mp4 | 6391494 | 10.48 /0 | 23 /19672 |
| 0_te9.mp4 | 33474374 | 17.02 /0 | 24.80 /15872 |
| 4_te5.mp4 | 4217183 | 10.44 /0 | 25.10 /19672 |
| 4_te19.mp4 | 28558205 | 15.06 /0 | 24.83 /19864 |
| 0_tr128.mp4 | 3021735 | 10.45 /0 | 25.08 /19672 |
| 0_tr16.mp4 | 34584860 | 16.98 /0.040008 | 24.80 /15872 |
| 4_tr13.mp4 | 3240413 | 10.41 /0 | 25.06 /19672 |
| 4_tr6.mp4 | 42290441 | 20.84 /0 | 25.05 /16032 |

**W2-10-F03 — measured container metadata S03.** Все8H2641920×1080, yuv420p или yuvj420p. Фактические rates/timebases различаются, поэтому авторские24FPS нельзя считать жёстким constant-rate контрактом. 4_tr6 длится20.84s, encoder Bandicut Joiner; другие samples Cutter. `At least one output file must be specified` в ffmpeg-i log ожидаемо при probe без output, это не decode failure; JPEG extraction выполнена отдельно. Для timing нужны stream timestamps, clip start не GT onset.

**W2-10-F04 — выборочный просмотр extracted frames S03.** Видны зелёная полоса с жёлтой границей, оборудование и люди. Framing0_te23/0_tr128 и4_te5/4_tr13/4_tr6 сходен;0_te9/0_tr16 и4_te19 отличаются crop/angle. Это proxy `inferred_view_A/B`, не supplied camera IDs. Оба observed framing есть в train и test; camera independence не установлена. Некоторые клипы начинаются с уже присутствующим человеком; достаточный lead-in не гарантирован. В4_tr6 человек в selected frames находится вне зелёной полосы при clip class Safe Walkway. Возможны несколько действий, разные люди или clip-level convention; это не автоматически label error, но запрещает трактовать folder class как exhaustive per-person state. Статья W1 допускает несколько behaviors в клипе.

**W2-10-F05 — scope и условия S01/S02.** Dataset card CC BY4.0 и article CC BY-NC4.0 относятся к разным artifacts. Сохранить авторов, DOI и attribution; дополнительных внутренних textual notices в manifest не найдено. Continuous-recording URL, manifest и исходные timestamps не установлены. Указанные авторами4000h описывают raw source, а не полученный denominator. Всеобщая commercial/privacy гарантия не выводится.

## Готовые inputs, следующий эксперимент и Q

W2-10-E01: восемь локальных MP4 с checksums и native timing — готовые1080p replay inputs для video_architecture/linq_platform. Throughput LinQ здесь не измерен.

W2-10-E02 — предложено, не выполнено: просмотреть полные clips, задать policy и ground-plane footpoint, polygon, person tracks, visibility/occlusion/uncertain intervals, onset/end, cut-start/end flags и multiple-person relations. Если человек уже outside на первом кадре, onset left-censored. Такой manual example нельзя называть author GT. Даже успешная разметка8curated clips не даёт representative false alerts/h из длительной эксплуатации.

W2-10-Q01: доступны ли continuous safe periods/raw recordings, supplied camera/session IDs и event protocol? Следующий путь — адресный вопрос авторам/постановщику; письмо не отправлялось. → evaluation: clip labels и framing overlap ограничивают оценку; → violation_methods: authorization/overload требуют контекста; → rights collector: сохранить отдельные dataset/article licence layers.
''',encoding='utf8')
root.joinpath('W2-11.md').write_text('''# W2-11 — SARD: bounded media acquisition и неизвестная schema

K011; W2-C. Доступ23.10.2026; продолжение clock03:40:57UTC/06:40:57Europe/Moscow. **K011 — область уточнена; schema, identity protocol и splits открыты.** Приоритет снижен до дополнительного construction-action donor. Сейчас не выбирать главным temporal/PPE-event источником. Полученный Core clip не paired с supplementary4.txt; его FPS нельзя переносить на4.mp4.

## Источники

| ID | Первичный источник / версия | Доступ / locator |
|---|---|---|
| W2-11-S01 | Wu, Chengfeng, *SARD: A Comprehensive Dataset for Construction Site Activity Recognition*, Zenodo v1, DOI10.5281/zenodo.19926448, publication30.04.2026, created/modified13.05.2026, revision4 https://zenodo.org/api/records/19926448 | `MATERIALS/W2-11/ZENODO.json`, прочитан23.10.2026. W1 API/ZIP directories — тот же deposit. |
| W2-11-S02 | https://zenodo.org/api/records/19926448/files/CoreSet.zip/content ; archive MD5 0302eb8d2af0722a9aa02f578cd03f89 | HTTP Range, member `CoreSet/Mix concrete/27115_29941.mp4` полностью извлечён, CRC проверен zipfile. `CHECK.py`, `CORE_SAMPLE.mp4`, `CORE_RETRIEVAL.json`, `CORE_SAMPLE.ffmpeg.txt`. Полный ZIP не скачан. |
| W2-11-S03 | Author ORCID https://pub.orcid.org/v3.0/0009-0008-2232-3560/works | Реально получен `ORCID.json`, group пуст. Это не доказательство отсутствия любой статьи автора. |
| W2-11-S04 | Ранее извлечённый `ComplementarySet.zip/ComplementarySet/4.txt` | Original в W1-07/SARD_4.txt. Новый локальный анализ: `ID_STRUCTURE.json`, `PARSE.py`, `PARSER_AUDIT.json`. Это новый анализ того же payload, не независимый источник. |

## Факты

**W2-11-F01 — прочитанная API metadata S01.** Нет related_identifiers на paper/schema/repository; creator имеет только ORCID, affiliationnull. Description обещает definitions/splits/source metadata, однако полные ZIP directories W1 содержат class directories/media и9txt/9mp4, без отдельных documents/manifests. Bounded exact-name поиск `SARD Chengfeng dataset` и `SARD 67,098` дал Zenodo и нерелевантные результаты; новая первичная schema не найдена. Это не доказательство её несуществования.

**W2-11-F02 — performed acquisition S02.** Выбран минимальный compressed media member;81,218decoded member bytes,172,585network bytes включая directory/headers. ffmpeg распознал H264480×270, duration2.84s, start0, displayed23.96fps, tbn19168. Это real container probe, не visual action validation и не измерение supplementary media. Core папка Mix concrete задаёт video-level class; original URL по filename не установлен.

**W2-11-F03 — выполненный label audit S04.** В160,824строках raw_id_1 имеет43,951уникальных значений; raw_id_2 —2180уникальных (диапазон1..4495 не равен count). ID2=1 повторяется по последовательным ID1 с person/Unknow и плавно меняющимися координатами. Это поддерживает гипотезу frame/object IDs, но **340значений raw_id_2 встречаются с разными source classes**: например48=person/vest,174=helmet/hook/person/vest. Поэтому raw_id_2 нельзя считать глобально class-consistent object track ID. Возможны resets, class changes или иная schema; механизм не установлен. Parser audit сохраняет все cross-class случаи, примеры первого/среднего/последнего появления. Нулевые nonpositive rectangles при условной xyxy интерпретации не доказывают coordinate convention.

**W2-11-F04 — implemented safe parser S04.** `PARSE.py` отделяет первые2integers, source_class, последние4integer coords и средний raw_action. Поля называются raw_id_1/raw_id_2/raw_box; `Unknow` и пустой action сохраняются, переменная длина строк допустима. Execution artifact существует. Настоящий paired overlay/frame-index test на4.mp4 **не выполнен**: Core sample другая sequence,35GB supplementary ради одного sample не загружался. Не объявлять parser implementation валидированной tracking schema.

**W2-11-F05 — documentary counts/rights S01.** Core748clips/11activities/27HOI и supplementary9clips/67,098annotated frames/1,018,232person boxes — авторские числа, не W2 full count. Zenodo CC BY4.0 относится к deposit; upstream rights каждого web/video source неизвестны. Activity label не равен нарушению, wear mask не industrial respirator GT, raw IDs не validated MOT tracks.

## Q и решение

W2-11-Q01: author column definitions,27HOI map, supplied splits/source grouping и upstream notices. Это адресный вопрос, внешнего письма нет. Core допустим как conditional action/video-plumbing donor, supplementary отложить до schema gate.

W2-11-E01 — предложено: получить короткий author-provided4.mp4 excerpt с исходным frame offset/FPS; наложить labels в начале/середине/конце и около occlusion; проверить0/1-based indexing, xyxy/xywh, inclusive bounds, lifecycle/reset IDs и action ontology. Несколько frames не валидируют все9sequences. → evaluation: splits/source groups открыты; → violation_methods: нет zone/policy/onset GT; → training_strategy: partial labels и raw IDs требуют gate.
''',encoding='utf8')
