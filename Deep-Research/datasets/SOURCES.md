# Источники datasets

Срез получения доказательств: 23.10.2026, Europe/Moscow (UTC+3), две завершённые волны. Сборщик работает только с сохранёнными материалами; новой сети нет. Дата публикации/версии ниже отделена от доступа: **все перечисленные источники исследователи открывали 23.10.2026**, если не сказано иначе. Когда точное время запроса не сохранено, указывается только дата. Первичные файлы остаются в `_WORK/MATERIALS/`; W1/W2 — журналы происхождения и границ проверок, а не независимые подтверждения одного автора. Поддерживаемые F-ID приведены в соответствующих карточках [RAW_FACTS.md](RAW_FACTS.md); обратный индекс добавлен в конце реестра.

`Документ` означает прочитанный текст; `metadata` — полученную схему/список; `payload` — реально полученные bytes; `наша проверка` — сохранённый локальный результат с указанным охватом. Наличие URL и manifest не означает получения всего media. Git commit фиксирует код/документ, но не immutable revision внешнего Drive ZIP.

## SH17

<a id="s001"></a>

### S001 — SH17, авторская публикация

Mughees Ahmad, Irfan Rahimi, *SH17: A Dataset for Human Safety and Personal Protective Equipment Detection in Manufacturing Industry*. [ar Xiv:2407.04590v1](https://arxiv.org/html/2407.04590v1), 05.07.2024. Тип: первичный документ, авторские измерения/описания. Локаторы: §III, Table II, Appendix A/Table VIII, Introduction/Conclusion. Снимки: [_WORK/MATERIALS/W1-02/paper.txt](_WORK/MATERIALS/W1-02/paper.txt), [_WORK/MATERIALS/W1-13/sh17.pdf](_WORK/MATERIALS/W1-13/sh17.pdf). Прочитаны источник фото, protocol, counts и size statements; все labels из статьи не проверялись. Таблицы между собой расходятся.

<a id="s002"></a>

### S002 — SH17 repository и class map

Ahmad et al., [SH17 dataset commit `2f832c289f9deea063367045ed8230b26e3e7ea9`](https://github.com/ahmadmughees/SH17dataset/tree/2f832c289f9deea063367045ed8230b26e3e7ea9). Дата commit в настоящей сборке не установлена; это не дата доступа. Локаторы: `sh17.yaml`, `list_of_all_urls.csv`, downloader, README License/Disclaimer. Сохранены в [_WORK/MATERIALS/W1-02/](_WORK/MATERIALS/W1-02/), README также W1-10. Фактически прочитаны YAML/CSV/код; downloader не запускался как массовый сборщик. README даёт NC-SA и Pexels layer.

<a id="s003"></a>

### S003 — SH17 Kaggle version 1

Автор Mughees Ahmad, [dataset](https://www.kaggle.com/datasets/mugheesahmad/sh17-dataset-for-ppe-detection), [view API](https://www.kaggle.com/api/v1/datasets/view/mugheesahmad/sh17-dataset-for-ppe-detection), [listing API](https://www.kaggle.com/api/v1/datasets/list/mugheesahmad/sh17-dataset-for-ppe-detection). Version 1, creation `2024-07-03T23:09:23.513Z`; id 5329058. Локаторы: `_WORK/MATERIALS/W2-12/kaggle_view.txt`, [_WORK/MATERIALS/W2-01/MANIFEST_PROGRESS.json](_WORK/MATERIALS/W2-01/MANIFEST_PROGRESS.json). Полная pagination завершена; 32,398 unique paths. Это metadata counts/bytes, не получение 14 GB фотографий.

<a id="s004"></a>

### S004 — SH17 released small files и paired image

Тот же автор/release S003. Прямой single-file маршрут: `https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName={path}`; реальные exact paths/ответы: [_WORK/MATERIALS/W2-01/RELEASE_REQUESTS.json](_WORK/MATERIALS/W2-01/RELEASE_REQUESTS.json), `PAIRED_RELEASE_REQUESTS.json`, `RELEASE_IMAGE_REQUEST.json`. Version 1; дата отдельного файла не установлена. Получены 13 YOLO, 2 VOC, 2 metadata JSON и один image ZIP. Результаты `PAIRED_COMPARISON.json`, `RELEASE_IMAGE_DECODE.json`, `RELEASE_COORDINATE_OVERLAY.jpg`. Полный released label audit не выполнен. Старые `released_*` ответы 404 не являются labels.

<a id="s005"></a>

### S005 — SH17 raw и ответ автора

Ahmad, [issue 4](https://github.com/ahmadmughees/SH17dataset/issues/4), комментарии 15.11.2024; [прямой raw ZIP](https://github.com/user-attachments/files/17777364/SH17-raw.zip). Тип: авторский текст/conversion example и payload. 5,835,796 bytes, SHA256 `ebac83a98d36b32c54d00efa9e8591279bb80232711fdd385d5dbac09cf462a9`. Локаторы: [_WORK/MATERIALS/W1-11/raw_audit.json](_WORK/MATERIALS/W1-11/raw_audit.json), `geometry_audit.json`, `sh17_issue4.txt`, `SH17-raw.zip`. Полностью parsed 8,102 XML; semantic completeness не проверена полностью.

<a id="s006"></a>

### S006 — SH17 targeted semantic audit

Исследователи W2, наша проверка 23.10.2026, не внешняя публикация. [_WORK/MATERIALS/W2-02/SAMPLE_SELECTION.json](_WORK/MATERIALS/W2-02/SAMPLE_SELECTION.json), `CONTACT0.jpg`–`CONTACT3.jpg`, 13 originals/XML/overlays; mapping comparison в S004. Источник изображений — exact Pexels URLs из selection; долговечный шаблон `https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg`. Выбор по классам/on-off/крупным boxes и crowded case; не случайная выборка. Current Pexels и released pixels различаются для 13376117; исправлен pairing, а не source bbox.

<a id="s007"></a>

### S007 — SH17 Zenodo alternative record

Ahmad et al., [Zenodo 12659325 API](https://zenodo.org/api/records/12659325), v1, 04.07.2024, API revision 4. Локатор: `_WORK/MATERIALS/W1-10/sh17_zenodo.json`, `_WORK/MATERIALS/W2-12/sh17_correct_zenodo.txt`; license CC BY-NC 4.0, restricted, files empty. API получен, файлы через этот record не получены. Посторонний record 12750834 исключён и не источник SH17.

<a id="s008"></a>

### S008 — Pexels terms/license

Pexels, [Terms of Service](https://www.pexels.com/terms-of-service/), §4–6, [License](https://www.pexels.com/license/), allowed/prohibited uses, [AUP](https://www.pexels.com/acceptable-use-policy/). Terms/AUP last updated 20.10.2026. Первичный legal text прочитан web исследователями W1/W2; сохранена запись [_WORK/MATERIALS/W2-12/PEXELS_ACCESS_NOTES.md](_WORK/MATERIALS/W2-12/PEXELS_ACCESS_NOTES.md), а не полный успешный HTML snapshot. Shell 403 challenge не источник legal wording. Историческая редакция условий каждого фото 2024 не установлена; это карта условий, не юридическое заключение.

## Каски, головы, одежда и заводское CCTV

<a id="s009"></a>

### S009 — SHWD repository / SCUT provenance

njvisionpower, [Safety-Helmet-Wearing-Dataset commit `c952631dfc352e0defdd54b4785a9be6576451ad`](https://github.com/njvisionpower/Safety-Helmet-Wearing-Dataset/tree/c952631dfc352e0defdd54b4785a9be6576451ad). README Introduction/Download, `train_yolo.py` class list, MIT LICENSE copyright 2019. Снимки `_WORK/MATERIALS/W1-03/Safety-Helmet-Wearing-Dataset/`, `shwd-train.py`, W1-10 `shwd_LICENSE`. Документ/код прочитаны; слово person требует проверки geometry в S010.

<a id="s010"></a>

### S010 — SHWD actual VOC2028.zip

Авторская [Drive ссылка](https://drive.google.com/file/d/1qWm7rrwvjAWs1slymbrLaCf7Q-wnGLEX/view), download `https://drive.usercontent.google.com/download?id=1qWm7rrwvjAWs1slymbrLaCf7Q-wnGLEX&export=download&confirm=t`. Дата публикации/immutable revision не установлены. Total 1,117,970,537 bytes по Content-Range. [_WORK/MATERIALS/W2-05/ARCHIVE_MANIFEST.json](_WORK/MATERIALS/W2-05/ARCHIVE_MANIFEST.json), `STRUCTURE_AUDIT.json`, `PAIRED_AUDIT.json`, `CONTACT.jpg`, `SELECTED_MEMBERS.json`. Получены directory, 4 split TXT, 20 XML, 8 JPEG; весь ZIP SHA256 не вычислен. Нет найденных README/LICENSE members.

<a id="s011"></a>

### S011 — SCUT-HEAD upstream condition

HCIILAB, [официальный SCUT-HEAD README](https://github.com/HCIILAB/SCUT-HEAD-Dataset-Release), §Remark; mutable master, commit не установлен. `_WORK/MATERIALS/W1-10/scut_readme.md`. Дата публикации в сборке неизвестна. Документ ограничивает использование academic research. Доля этого parent в SHWD не определена; условие нельзя заменить MIT software.

<a id="s012"></a>

### S012 — CHV publication/repository

Zijian Wang et al., [Sensors 2021, 21, 3478](https://doi.org/10.3390/s21103478), §2.3, Fig.5–6; [PPE_detection commit `907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d`](https://github.com/ZijianWang-ZW/PPE_detection/tree/907fafdbf13dde8e9fbfb9eeeda0bf3d037ed08d). Authors/source names сохранены в статье; дата здесь установлена до года/volume, точный день не нужен для выбора. `_WORK/MATERIALS/W1-03/chv-paper.pdf`, `.txt`; README W1-10. Документирует GDUT-HWD+SHWD, class map, random split и free-use statement без полной license specification.

<a id="s013"></a>

### S013 — CHV actual archive

Авторский [Drive CHV_dataset.zip](https://drive.google.com/file/d/1fdGn67W0B7ShpBDbbQpUF0ScPQa4DR0a/view); usercontent route с этим id/export=download/confirm=t. 439,733,771 bytes по Content-Range; дата/revision/full ZIP hash неизвестны. [_WORK/MATERIALS/W2-06/ARCHIVE_MANIFEST.json](_WORK/MATERIALS/W2-06/ARCHIVE_MANIFEST.json), [реальный README](_WORK/MATERIALS/W2-06/pairs/README.md), `STRUCTURE_AUDIT.json`, `PAIRED_AUDIT.json`, `SAMPLE_SELECTION.json`. Получены directory, splits/README, 27 YOLO labels и 4 JPEG. README — primary artifact protocol, pairing — наша проверка.

<a id="s014"></a>

### S014 — SHEL5K publication and parent

Otgonbold et al., [Sensors 2022, 22, 2315](https://doi.org/10.3390/s22062315), §2.1/§3/Fig.3, setup; [Moyo G/SHEL5K commit `d187230e09cb34216f56987b31462e86a78f38b3`](https://github.com/MoyoG/SHEL5K/tree/d187230e09cb34216f56987b31462e86a78f38b3). `_WORK/MATERIALS/W1-03/shel5k-paper.pdf`, `.txt`. Parent — [andrewmvd/hard-hat-detection](https://www.kaggle.com/datasets/andrewmvd/hard-hat-detection), здесь самостоятельный parent payload не исследован. Статья заявляет six classes/75,570 и random 4,000/1,000; это не supplied membership.

<a id="s015"></a>

### S015 — SHEL5K Mendeley v1

Munkhjargal Gochoo / authors, [Safety Helmet Wearing Dataset](https://data.mendeley.com/datasets/9rcv8mm682/1), DOI 10.17632/9 rcv 8 mm682.1, 23.04.2021, CC BY-NC 3.0. [Folders API](https://data.mendeley.com/public-api/datasets/9rcv8mm682/folders/1), files endpoint `https://data.mendeley.com/public-api/datasets/9rcv8mm682/files` с folder_id, version=1, $limit/$start. `_WORK/MATERIALS/W1-15/shel-Annotations-manifest.json`, `shel-Images-manifest.json`; 5,000+5,000 metadata, original download URL и SHA256 каждого файла. Root files [] не означает отсутствие вложенных файлов.

<a id="s016"></a>

### S016 — SHEL5K full XML and selected pixels

Наша выполненная проверка, 23.10.2026; originals по S015. [_WORK/MATERIALS/W2-07/XML_AUDIT.json](_WORK/MATERIALS/W2-07/XML_AUDIT.json), 5,000 originals в `XML/`, `DOWNLOAD_LOG.json`, `SAMPLE_DOWNLOADS.json`, `PAIRED_AUDIT.json`, `CONTACT.jpg`; `_WORK/SHEL_AUDIT.py`. Все XML SHA256 совпали с metadata; 4 новых PNG + 3 W1. 8 unexpected person objects имеют exact filenames/boxes, не назначенный автором seventh-class protocol.

<a id="s017"></a>

### S017 — SFCHD paper and pinned repository

Fusheng Yu, Jiang Li, Xiaoping Wang, Depeng Li, Xin Zhan, Shaojin Wu, Junjie Zhang. [ar Xiv:2306.02098](https://arxiv.org/abs/2306.02098): v1 03.06.2023, v2 10.08.2024; current Git Hub manuscript оформлен ACM MM 2025. [Commit `7bfabb4533613e6917461dc3758dcff5f304bd03`](https://github.com/lijfrank/SFCHD-SCALE/tree/7bfabb4533613e6917461dc3758dcff5f304bd03), `sfchd-scale.pdf`, README Dataset Acquisition. `_WORK/MATERIALS/W1-03/SFCHD-SCALE/sfchd-scale.txt`, §3.1–3.3 (примерно lines 605–653, 877–884). Источник domain/privacy/annotation claims и small<0.1% definition; не evidence perfect annotation.

<a id="s018"></a>

### S018 — SFCHD annotation/split payload

Тот же commit S017: [dataset_SFCHD](https://github.com/lijfrank/SFCHD-SCALE/tree/7bfabb4533613e6917461dc3758dcff5f304bd03/dataset_SFCHD), `classes.txt`, `annotations/all_data.json`, `val.json`, `labels.zip`, `new_split_yolo/{train,val,test}.txt`. Реально получены W1; complete local annotation audit [_WORK/MATERIALS/W2-03/AUDIT.json](_WORK/MATERIALS/W2-03/AUDIT.json), `SUPPLEMENT.json`, `GEOMETRY_OVER_0_001.json`. Full image decoding не выполнен; пустой test.json не пригоден как JSON annotation.

<a id="s019"></a>

### S019 — SFCHD media archive, selected pairs, groups

Авторский [Drive SFCHD.zip](https://drive.google.com/file/d/1-2z7r3J4sZdLvVt5mllvSEwAFO49Y-zj/view); download usercontent с этим id. Total 1,972,746,810 bytes; immutable revision/full ZIP hash не установлены. [_WORK/MATERIALS/W2-04/ARCHIVE_MANIFEST.json](_WORK/MATERIALS/W2-04/ARCHIVE_MANIFEST.json), `MEDIA_MEMBERSHIP.json`, `PAIRED_AUDIT.json`, `RUN_GROUPS.json`, `PREFIX_GROUPS.json`, `CONTACT.jpg`, range/member logs. Получены directory и 7 JPEG; 40 prefixes/231 runs — наши proxy, не author camera/session IDs. В S018 missing name нет JPEG и современного TXT; старый TXT извлечён в W2-03.

## Face protection, smoking and temporal data

<a id="s020"></a>

### S020 — CPPE-5 paper/current repo

Rishit Dagli, Ali Mustufa Shaikh, [ar Xiv:2112.09569](https://arxiv.org/abs/2112.09569), v1 15.12.2021, v2 18.02.2023 (PDF date 21.02.2023). [Repo commit `8d6701db6a25a3ce482f8a3d9766ebe318b1f1dc`](https://github.com/Rishit-dagli/CPPE-Dataset/tree/8d6701db6a25a3ce482f8a3d9766ebe318b1f1dc). `_WORK/MATERIALS/W1-04/cppe.pdf`, `cppe.txt`, README; §§3–5, Table 1–3. Domain/protocol/source metadata claims и 100 extra test description — авторские, не доказательство публичных 1,129 images.

<a id="s021"></a>

### S021 — CPPE-5 original release v0.1.0

Те же авторы, [release](https://github.com/Rishit-dagli/CPPE-Dataset/releases/tag/v0.1.0), published 14.12.2021 19:20:05 UTC, tag commit `c18d33dd33230c601c62f944df2626cd73412a79`; [asset dataset.tar.gz](https://github.com/Rishit-dagli/CPPE-Dataset/releases/download/v0.1.0/dataset.tar.gz) metadata 238,482,705 bytes. HTTP asset Last-Modified 15.04.2023 отдельно от release publication. W2 получил первые 8,388,608 bytes, полные `annotations/train.json`/`test.json` и 2 PNG; [_WORK/MATERIALS/W2-08/PARTIAL_TAR_MEMBERS.json](_WORK/MATERIALS/W2-08/PARTIAL_TAR_MEMBERS.json), `ORIGINAL_MEDIA_PAIRING.json`, `release_tree.json`, `RANGE_RESPONSE.json`. README MD5 `f4e043f983cff94ef82ef7d57a879212` всего tar не проверен. Partial tar listing не полный manifest.

<a id="s022"></a>

### S022 — CPPE annotations/code license clarification

Rishit Dagli, [issue 6 comment 1082077175](https://github.com/Rishit-dagli/CPPE-Dataset/issues/6#issuecomment-1082077175), created/updated 29.03.2022 16:11:44 UTC. Primary author statement; [_WORK/MATERIALS/W2-08/issue6comments.json](_WORK/MATERIALS/W2-08/issue6comments.json). Apache 2.0 назван для annotations и code; автор отделяет copyright фотографий/Flickr conditions. Конкретный metadata inventory этим комментарием не предоставлен.

<a id="s023"></a>

### S023 — CPPE Hugging Face representation

Авторская [rishitdagli/cppe-5 revision `66f6a5efd474e35bd7cb94bf15dea27d4c6ad3f8`](https://huggingface.co/datasets/rishitdagli/cppe-5/tree/66f6a5efd474e35bd7cb94bf15dea27d4c6ad3f8). Дата revision здесь неизвестна. `README`, dataset-server [test first rows](https://datasets-server.huggingface.co/first-rows?dataset=rishitdagli/cppe-5&config=default&split=test), response фиксирует revision. `_WORK/MATERIALS/W1-04/hf_first_rows.json`, `hf_test_1012.jpg`, `hf_test_1013.jpg`, `_WORK/MATERIALS/W2-08/HF_ORIGINAL_COMPARISON.json`. 29 rows/207 boxes и 2 JPEG; сравнение annotation lineage полностью для этих 29, pixel identity с PNG не установлена.

<a id="s024"></a>

### S024 — Masked Face-Net

Cabani, Hammoudi, Benhabiles, Melkemi, [official repo](https://github.com/cabani/MaskedFace-Net), README Dataset/Licenses, master accessed; commit API 403, pin не установлен. Paper DOI [10.1016/j.smhl.2020.100144](https://doi.org/10.1016/j.smhl.2020.100144), 2020. `_WORK/MATERIALS/W1-04/maskedface_readme.md`. Только документация: current 133,783 отличается от older abstract 137,016. Images не получены, FFHQ source rights неоднородны.

<a id="s025"></a>

### S025 — Smoker Detection Dataset v1 and original paper

Ali Khan et al., [Mendeley j45 dj8 bgfc/1](https://data.mendeley.com/datasets/j45dj8bgfc/1), DOI10.17632/j45 dj8 bgfc.1, 15.08.2022, CC BY 4.0; [Sensors 2022,22,892](https://doi.org/10.3390/s22030892), §5. `_WORK/MATERIALS/W1-06/smoker-paper.pdf`, `.txt`, card; `_WORK/MATERIALS/W1-15/j45dj8bgfc-files.json`. File-id `c386d8e9-2b49-4ade-ae3b-fb2f63815eaf`, `Smoker Detection.rar`, 65,575,997 bytes, SHA256 `2b0ef67ec714a507cff7248ef7f3d7bbdb4c4e00adc8e309cfac02cd2b6e5d18`, actual matched API. Search-derived photographs — source rights remain a different layer.

<a id="s026"></a>

### S026 — Smoker actual decode/visual observations

Наши проверки W1/W2 23.10.2026, [_WORK/MATERIALS/W1-06/SMOKER_ARCHIVE_MANIFEST.json](_WORK/MATERIALS/W1-06/SMOKER_ARCHIVE_MANIFEST.json), `SMOKER_COUNTS.json`, [_WORK/MATERIALS/W2-09/DECODE.json](_WORK/MATERIALS/W2-09/DECODE.json), `DECODE2.py`, `NOTSMOKING_CONTACT.jpg`. Full decode 1120; exact canonical RGB hash comparison. 40 initial negative thumbnails просмотрены; это не randomized confuser audit и не near-duplicate/subject independence test.

<a id="s027"></a>

### S027 — surveillance smoking/calling primary paper

J. Zhang, L. Wei, B. Chen, H. Chen, W. Xu, *Intelligent Recognition of Smoking and Calling Behaviors for Safety Surveillance*, Electronics 12,3225, 26.07.2023; [DOI](https://doi.org/10.3390/electronics12153225), [издательский PDF](https://mdpi-res.com/d_attachment/electronics/electronics-12-03225/article_deploy/electronics-12-03225.pdf). `_WORK/MATERIALS/W2-09/paper.pdf` 5,126,503 bytes, `.txt`; §3.1/Fig.2/Data Availability. PDF получен после HTML429. Документация описывает labels/counts, но data только upon reasonable request; payload/лицензия данных не получены, письма не отправлены.

<a id="s028"></a>

### S028 — HMDB51

Kuehne, Jhuang, Garrote, Serre, Poggio, ICCV2011; [Serre Lab official page](https://serre.lab.brown.edu/hmdb51.html), Download/Action classes/Meta-labels, текущая страница 6,849/51. Документ открыт W1-06, точный immutable media revision не известен; video payload не получен. Unstabilized/stabilized и три split sets — варианты протокола, не независимые источники.

<a id="s029"></a>

### S029 — SED/SED-FL wearable exclusion

Aristotle University, [Smoking Event Detection](https://mug.ee.auth.gr/smoking-event-detection/), page created 05.02.2021. W1-06 Description/Download: publicly delivered pickle 6 Do F smartwatch, не подтверждённый visual payload. Документ прочитан, исходное smartphone video использовали для GT, не доказана выдача видео.

<a id="s030"></a>

### S030 — Önal/Dandıl data and API

O. Önal, E. Dandıl, [Video Dataset for Safe and Unsafe Behaviours v1](https://data.mendeley.com/datasets/xjmtb22pff/1), DOI10.17632/xjmtb 22 pff.1, 11.06.2024, CC BY 4.0. [Folders](https://data.mendeley.com/public-api/datasets/xjmtb22pff/folders/1), files endpoint с version=1/folder_id. `_WORK/MATERIALS/W1-07/safe_unsafe.html`; [_WORK/MATERIALS/W2-10/MANIFEST.json](_WORK/MATERIALS/W2-10/MANIFEST.json), leaf JSON. Полный 691 MP4 metadata, не все MP4. 8 actual files и hashes/probes в `SAMPLE_OBSERVATIONS.json`.

<a id="s031"></a>

### S031 — Önal/Dandıl Data in Brief article

Те же авторы, [Data in Brief 56(2024)110791](https://doi.org/10.1016/j.dib.2024.110791), online 03.08.2024; [университетский PDF](https://acikkaynak.bilecik.edu.tr/server/api/core/bitstreams/dc6b0007-eb9b-4496-9d00-81ecb68fa9b4/content). `_WORK/MATERIALS/W1-07/safe_unsafe.pdf`, `.txt`, Tables 1–3/§4/Limitations. CC BY-NC 4.0 относится к статье, не автоматически к video. 4,000h — описанный raw source, не published volume.

<a id="s032"></a>

### S032 — SARD deposit/core/supplementary

Wu, Chengfeng, [Zenodo 19926448](https://zenodo.org/records/19926448), DOI10.5281/zenodo.19926448, v1 publication 30.04.2026, created/modified 13.05.2026, API revision 4. [API](https://zenodo.org/api/records/19926448), [CoreSet.zip content](https://zenodo.org/api/records/19926448/files/CoreSet.zip/content). `_WORK/MATERIALS/W1-07/sard.json`, ZIP manifests, `SARD_4.txt`; W2-11 `ZENODO.json`, `CORE_RETRIEVAL.json`, `CORE_SAMPLE.ffmpeg.txt`, `PARSER_AUDIT.json`, `ID_STRUCTURE.json`. Полные ZIP не скачаны; 1 supplementary label и 1 иной Core clip. Schema и supplied split не получены. ORCID works пуст, это не отсутствие любой статьи.

<a id="s033"></a>

### S033 — PhysicalAI pinned dataset

NVIDIA, [PhysicalAI-Event-Videos revision `7f79b39fcd1ef1dc39f23f227cd8a9480d6077db`](https://huggingface.co/datasets/nvidia/PhysicalAI-Event-Videos/tree/7f79b39fcd1ef1dc39f23f227cd8a9480d6077db), v1.0 creation 15.06.2026. `_WORK/MATERIALS/W1-06/PhysicalAI-Event-Videos/`: README,2026/provenance.json, stats.json, train/labels.json, video_manifest.csv, anomaly-category-mapping.json. Payload metadata получен; video/chunk ZIP не получены. [_WORK/MATERIALS/W2-15/EXACT_JOIN.json](_WORK/MATERIALS/W2-15/EXACT_JOIN.json), `JOIN_SUMMARY.json`, `AUDIT_JOIN.py` — наша deterministic selection, не author closed ontology.

<a id="s034"></a>

### S034 — NVIDIA Dataset License

NVIDIA, [Dataset License Agreement PDF](https://assets.ngc.nvidia.com/products/api-catalog/legal/Personas-Dataset-NVIDIA-Training-Dataset-License-Agreement-2025-11-26.pdf), text version 21.11.2025, URL filename 26.11.2025. `_WORK/MATERIALS/W2-15/LICENSE.pdf`293,509 bytes, `LICENSE.txt`, §§1–5,12.3. Прочитан полный текст; Trustworthy AI terms по отсылке отдельно не разобраны. Grant только AI training/development и запрет redistribution dataset whole/part; не blanket public asset permission.

<a id="s035"></a>

### S035 — Google additional generation terms

Google Cloud, [Service Specific Terms](https://cloud.google.com/terms/service-terms), §17a/b. Mutable page, version не установлена; доступ 23.10.2026. `_WORK/MATERIALS/W2-15/GOOGLE.html`1,053,191 bytes, `GOOGLE_EXTRACT.txt`. Дополнительное условие по card S033 для Veo output; per-video Veo/Cosmos assignment не известен, полный compliance review не выполнен.

## Дополнительные PPE, generic и доменные источники

<a id="s036"></a>

### S036 — Pictor publication/repository

Nath, Behzadan, Paal, *Deep Learning for Site Safety: Real-Time Detection of Personal Protective Equipment*, Automation in Construction 112,103085,2020, [DOI](https://doi.org/10.1016/j.autcon.2020.103085); [ciber-lab/pictor-ppe commit `8f41c9525bbd1f45245f593c7502a1934eef06fa`](https://github.com/ciber-lab/pictor-ppe/tree/8f41c9525bbd1f45245f593c7502a1934eef06fa). W1-05 README Dataset/Methods, tree. Публикация и README описывают 774+698 и три подхода; это не фактически полученные 1472 media.

<a id="s037"></a>

### S037 — Pictor actual crowd annotations

Авторские [Labels folder](https://drive.google.com/drive/folders/17VMS2-EQAuB6CsCVDK5ScmxjrP-B2cgW), [Images folder](https://drive.google.com/drive/folders/1zDdTd8GVOIGENYVEHGABEFLUqBjnCzeS). Drive file dates 09.09.2024 отдельно от paper 2020; immutable revision не установлен. 9 TXT реально получены `https://drive.google.com/uc?export=download&id=FILE_ID`; exact IDs в [_WORK/MATERIALS/W2-14/PICTOR_DOWNLOADS.json](_WORK/MATERIALS/W2-14/PICTOR_DOWNLOADS.json), counts/hash `PICTOR_AUDIT.json`; 1 JPEG/overlay. License notice в этих annotations не найден. Numeric worker-state map не установлен полностью.

<a id="s038"></a>

### S038 — Construction-PPE documentation/config

Mrunmayee Dalvi, Niyati Singh, Sahil Bhingarde, Ketaki Chalke (citation January 2025/v1.0.0), Ultralytics, [docs](https://docs.ultralytics.com/datasets/detect/construction-ppe/), [YAML main](https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/construction-ppe.yaml). Mutable main, commit не установлен; использованы W1-05 и exact internal config S039. Документация сама не доказывает все фото source rights/annotation completeness.

<a id="s039"></a>

### S039 — Construction-PPE actual ZIP/internal notice

Ultralytics [release asset](https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip), [release API](https://api.github.com/repos/ultralytics/assets/releases/tags/v0.0.0). Mutable tag v0.0.0; asset updated 07.09.2025 05:14:00 UTC. Полностью получен 178,415,813 bytes, SHA256 `bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`; `_WORK/MATERIALS/W2-14/construction-ppe.zip`, `ASSET.json`, `DIRECTORY.json`, `AUDIT.json`, `EXTRACTED/data.yaml`, `EXTRACTED/LICENSE`, `SEMANTIC_CONTACT.jpg`. Internal full AGPLv3 text dated 19.11.2007 — дата лицензии, не дата датасета. 4 semantic sample images, не полная visual validation.

<a id="s040"></a>

### S040 — Harness publication and actual XML/tree

Xu, Huang, Huang, [IET Image Processing 17(4),1071–1085,2023](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/ipr2.12696), §4.1.2/Data Availability; [Huangjiajing 96/Dataset commit `251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c`](https://github.com/Huangjiajing96/Dataset/tree/251f32e408d535f4ccc3e1d57a4ecb0f075bcd9c). W1-05 `harness_tree.txt`, `Dangerous0001.xml`, `SafetyHarness0001.xml`. Tree counts 3,300 XML/3,300 JPEG; 2 XML actual, images не декодировались. Chest/person geometry, неизвестные rights/split membership/upstream exact overlaps.

<a id="s041"></a>

### S041 — Site Object Detection SODA

Rui Duan, Hui Deng, Mao Tian, Yichuan Deng, Jiarui Lin, [ar Xiv:2202.09554v1](https://arxiv.org/abs/2202.09554),19.02.2022, §§3–5/Data Availability. `_WORK/MATERIALS/W1-01/soda.pdf`, `soda.txt`. [VOCv1.zip](https://scut-scet-academic.oss-cn-guangzhou.aliyuncs.com/SODA/2022.2/VOCv1.zip) Range запрос вернул 403 Aliyun OSS, media/XML не получены. Это конкретный failed route, не доказательство общей закрытости. Не SODA-D/A и не SODA10M. Числа и named categories только из paper, numeric IDs неизвестны.

<a id="s042"></a>

### S042 — COCO official schemas/terms

COCO consortium, [download](https://cocodataset.org/#download), [official site source](https://github.com/cocodataset/cocodataset.github.io), mutable master без закреплённого commit. `_WORK/MATERIALS/W1-08/download.htm`, `format-data.htm`, `termsofuse.htm`, `keypoints-2020.htm`. Download/format/keypoints/terms прочитаны; full annotations/images не получены. 2017 split переиспользует 2014 images; web site/annotations CC BY 4.0 отдельно от Flickr image rights.

<a id="s043"></a>

### S043 — Crowd Human official format/conditions

Shao et al.,2018, [official](https://www.crowdhuman.org/), [download](https://www.crowdhuman.org/download.html). `_WORK/MATERIALS/W1-08/crowdhuman.html`, `crowdhuman_download.html`; ODGT/Terms. Revision не указан, ODGT/media не скачаны. Full/visible/head boxes и ignore/unsure schema документированы; tag mask означает ignore person-like region, не PPE. Noncommercial research/education; image redistribution prohibited по странице.

<a id="s044"></a>

### S044 — MOT17 archive/actual labels

MOTChallenge, [MOT17](https://motchallenge.net/data/MOT17/), [MOT17Labels.zip](https://motchallenge.net/data/MOT17Labels.zip). Download state accessed 23.10.2026; results archive state 16.04.2026, не дата нового dataset release. `_WORK/MATERIALS/W1-08/MOT17Labels.zip`, manifest 10,107,022 bytes/105 entries; `_WORK/MATERIALS/W1-14/MOT17_GT_hash_groups.json`. Actual GT hash groups 21→7×3; image pixel comparison не выполнен. CC BY-NC-SA 3.0 + possible upstream conditions; instructions route 410, class filtering требует инструкции.

<a id="s045"></a>

### S045 — Construction Meta Action (CMA)

Yang et al., [Construction Action Recognition commit `06c11e0777f122e286752e2f39b45cfdd4191fd0`](https://github.com/S1mpleyang/ConstructionActionRecognition/tree/06c11e0777f122e286752e2f39b45cfdd4191fd0); papers 2023 [10.1016/j.autcon.2022.104703](https://doi.org/10.1016/j.autcon.2022.104703) и 2024 [10.1016/j.aei.2023.102294](https://doi.org/10.1016/j.aei.2023.102294). `_WORK/MATERIALS/W1-07/cma_readme.md`, W1-10 LICENSE. README1,595 clips/7 actions, Baidu code z7a2, research-only data; MIT repo отдельно. Full payload не получен, real 7 names/IDs не установлены.

<a id="s046"></a>

### S046 — Foundation Pit v2

Zhao et al., [Mendeley xjm 2 czccx 9/2](https://data.mendeley.com/datasets/xjm2czccx9/2),07.11.2025, CC BY 4.0 card. `_WORK/MATERIALS/W1-07/foundation.html`. Card заявляет добавление video sequences; count/FPS/GT не установлены. Один ошибочно предположенный API route 404 не доказывает недоступность всего dataset. Отложенная ветка, не ready event source.

<a id="s047"></a>

### S047 — Creative Commons primary texts

Creative Commons, [BY4.0](https://creativecommons.org/licenses/by/4.0/), [BY-NC-SA4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), [BY-NC3.0 legalcode](https://creativecommons.org/licenses/by-nc/3.0/legalcode), §§3–4. Прочитаны исследователем W1-10 23.10.2026; дата license version задана названием, дата страницы не установлена. Объясняют найденные условия, не доказывают полномочия конкретного uploader на все media. Сборка не разрешает общий спор о NC в призовом хакатоне или copy left на weights.

<a id="s048"></a>

### S048 — наш воспроизводимый annotation scale audit

Исследователь W2-A,23.10.2026; originals S005/S018/S023. [_WORK/MATERIALS/W2-13/SCALE_AUDIT.py](_WORK/MATERIALS/W2-13/SCALE_AUDIT.py), `SCALE_SUMMARY.json`, `QUANTILES.csv`, `BOXES.csv`. Executed 132 groups/202,781 rows с намеренно повторённым raw release-member subset. Точный transform и scopes в RAW_FACTS; не benchmark и не доказанный LinQ input.

## Правила использования реестра

S001–S048 имеют общий access date 23.10.2026; отсутствующее время или version явно не восполняются догадкой. Источники внутри одного author lineage не считаются независимыми. Сохранённые W1/W2 bundles заморожены: [_WORK/W1_BUNDLE_MANIFEST.json](_WORK/W1_BUNDLE_MANIFEST.json), [_WORK/W2_BUNDLE_MANIFEST.json](_WORK/W2_BUNDLE_MANIFEST.json). Прямой источник и конкретная локальная проверка должны читаться вместе. В [_WORK/ID_MAP.md](_WORK/ID_MAP.md) — переход от веточных S/F/Q/E-ID к общим; в [CRITIC.md](CRITIC.md) исходная критика и отдельное дополнение статусов.

## Обратный индекс поддерживаемых фактов

- **S001:** F002, F004, F005, F017, F019, F020, F022, F099, F100, F102
- **S002:** F005, F008, F009, F018, F022, F097, F101
- **S003:** F006, F009, F012, F018, F022
- **S004:** F003, F007, F008, F012, F013, F016
- **S005:** F010, F011, F012, F020, F098
- **S006:** F003, F014, F015, F016, F020, F098
- **S007:** F018
- **S008:** F018
- **S009:** F042, F044, F045, F099
- **S010:** F003, F043, F044, F045, F097, F100
- **S011:** F042, F045
- **S012:** F046, F047, F048, F049, F099
- **S013:** F003, F047, F048, F049, F097, F100
- **S014:** F002, F050, F051, F053, F055, F099
- **S015:** F050, F051, F053, F055, F101
- **S016:** F003, F050, F051, F052, F053, F054, F055, F097, F098, F100
- **S017:** F023, F026, F035, F039
- **S018:** F002, F003, F024, F025, F026, F028, F029, F030, F031, F097, F098, F100, F101, F102
- **S019:** F003, F026, F027, F032, F033, F034, F035, F100
- **S020:** F002, F056, F058, F059, F060, F062, F098, F099, F102
- **S021:** F003, F057, F058, F059, F060, F061, F062, F097, F100, F101
- **S022:** F060
- **S023:** F058, F059, F060, F061, F062, F097, F098, F099
- **S024:** F094
- **S025:** F063, F064
- **S026:** F003, F063, F064, F100
- **S027:** F002, F065, F066, F097
- **S028:** F095
- **S029:** F095
- **S030:** F003, F067, F068, F069, F070, F071, F097, F100, F102
- **S031:** F002, F067, F068, F070, F071
- **S032:** F002, F003, F072, F073, F074, F075, F097, F100
- **S033:** F003, F076, F077, F078, F079, F097, F099, F100, F101
- **S034:** F079
- **S035:** F079
- **S036:** F080, F081, F082, F099
- **S037:** F003, F081, F082, F097, F100, F101
- **S038:** F083, F086
- **S039:** F003, F083, F084, F085, F086, F097, F098, F100, F101
- **S040:** F087, F099
- **S041:** F088, F089
- **S042:** F090, F091, F093, F099
- **S043:** F091, F093
- **S044:** F003, F092, F093, F099
- **S045:** F095
- **S046:** F004, F096
- **S047:** Контекст/terms в связанных карточках, без отдельного значимого F.
- **S048:** F003, F019, F037, F038, F039, F040, F041, F062, F102
