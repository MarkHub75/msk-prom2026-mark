# W2_A — новые доказательства по K001/K003

Доступ проверен 2026-10-23, до 06:19 Europe/Moscow (+03:00), часы инструмента 03:19:16 UTC. Публикационные даты ниже не заменены датой доступа. Модели, benchmark и приложение не запускались. Файлы разметки прочитаны; собственные выводы отделены. Полные чужие статьи не сохраняются.

## W2-A-S01 — официальная поставка SH17 и её два реальных примера

Авторы: Hafiz Mughees Ahmad, Afshin Rahimi; владелец Kaggle mugheesahmad.

- [Репозиторий](https://github.com/ahmadmughees/SH17dataset), master `2f832c289f9deea063367045ed8230b26e3e7ea9`; [дерево](https://api.github.com/repos/ahmadmughees/SH17dataset/git/trees/master?recursive=1). Собственная сохранённая запись `sh17-tree.json` содержит `truncated=false`. GitHub release assets просмотрены: веса, отдельный extended annotation artifact не найден.
- [Kaggle](https://www.kaggle.com/datasets/mugheesahmad/sh17-dataset-for-ppe-detection); [metadata API](https://www.kaggle.com/api/v1/datasets/view/mugheesahmad/sh17-dataset-for-ppe-detection): dataset ID5329058, version1, lastUpdated `2024-07-03T23:09:23.513Z`. API metadata получены локально, web body пустой.
- [Конкретный VOC](https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName=voc_labels%2Fcareer-firefighter-relaxing-job-162540.xml), [YOLO](https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName=labels%2Fcareer-firefighter-relaxing-job-162540.txt), [исходное изображение](https://www.kaggle.com/api/v1/datasets/download/mugheesahmad/sh17-dataset-for-ppe-detection?fileName=images%2Fcareer-firefighter-relaxing-job-162540.jpeg). Сохранены `voc_labels-career-firefighter-relaxing-job-162540.xml`, `labels-career-firefighter-relaxing-job-162540.txt`, `firefighter.jpeg`.
- Второй basename `building-construction-building-site-constructing`: `sh17-sample-voc-download`, `labels-building-construction-building-site-constructing.txt`; те же URL с заменой basename и расширения.

**W2-A-F01 [artifact inspection].** В проверенных XML: filename/size, object name/pose/truncated/difficult/bndbox; wearer ID, on/off и relation отсутствуют. В TXT пять колонок. Firefighter helmet: YOLO class10, bbox `[.536750,.393375,.249833,.274750]`; XML `[2471,1024,3970,2123]` при6000×4000. Класс9 второго примера — gloves.

**W2-A-F02 [local visual observation].** В firefighter фото каска лежит на снятой куртке; голова сидящего человека вне кадра. Разметка сохраняет helmet как предмет, но не сообщает off или отсутствие защиты головы. Это конкретный контрпример `object_present => worn` и `off-body => uncovered`.

**W2-A-F03 [scope/unknown].** Инспектированы два примера, не все8099. Официальный отдельный extended export не получен. Нельзя утверждать, что tags нигде не существуют; нельзя обещать wearer relation в скачиваемой YOLO/VOC поставке.

## W2-A-S02 — SH17, публикация и class mapping

Ahmad/Rahimi, Journal of Safety Science and Resilience,2024; [DOI](https://doi.org/10.1016/j.jnlssr.2024.09.002), §3.3 Table2/Note; текст открыт через издателя/индекс. [YAML master](https://raw.githubusercontent.com/ahmadmughees/SH17dataset/2f832c289f9deea063367045ed8230b26e3e7ea9/sh17.yaml) прочитан и сохранён `sh17.yaml`; [Kaggle branch YAML](https://raw.githubusercontent.com/ahmadmughees/SH17dataset/c8bcd13b3f1b9ef42f856f4ec5d194d29df25ed0/sh17_kaggle.yaml) сохранён `sh17_kaggle.yaml`.

**W2-A-F04 [primary documentation].** Статья утверждает extended tags on/off у нескольких СИЗ, включая medical mask. Off означает предмет в сцене вне ношения. Отдельного wearer ID Table2 не описывает. Medical mask не заявлен промышленной cartridge полумаской. Порядок17 категорий Table2 не равен YOLO indices: фактические `helmet=10`, `hands=11`, `head=12`, `face-mask=5`. Проверенные VOC/TXT согласуются с YAML, а не с порядком таблицы.

Предел: статья о выпуске tags и реально прочитанные примеры базового экспорта — разные основания; ни одно не является industrial off-face benchmark.

## W2-A-S03 — industrial 3M head-state, полный текст

Zhu Yi, Wang Bangrong, Wang Jun, Xu Xiaofeng, *YOLOv8-LPE—a gas mask wearing detection method for industrial scenarios*, Journal of Qingdao University of Technology46(6),149–156,2025; received2024-04-28 — не дата выпуска. [Страница PDF издателя](https://cjournal.hep.com.cn/1673-4602/CN/PDF/1217769465963126793), [прямой PDF](https://jf2.hep.com.cn/aac09e01e03546ab91293b47895a116a.pdf). Web redirect failed; HTTP download200,6,520,852bytes,8pages, PyMuPDF text прочитан; p151 отрисована и визуально осмотрена. Сохранён только locator screenshot `gasmask-table-page.png`, не полная статья.

**W2-A-F05 [primary annotation semantics].** §1 pp150–151/Table1/Fig1–2: industrial3M cartridge head-state. Front/side wear_mask, no_wear, wear_wrong; седьмой back_head. Wrong включает обычную медицинскую маску вместо промышленной. Реальные+симулированные сцены,7992images,6058train/1934test. Neck/hand и removal-transition классов нет; unknown не отдельный PPE-class, back_head — observable orientation, который наша политика должна отобразить в unknown face coverage.

**W2-A-F06 [published measurement caveat].** §3.1p153: input1280², stated Nvidia GTX3090. §3.2 неверно описывает AP IoU threshold как confidence threshold; Table2 также содержит несогласованный F1. Эти ошибки ограничивают доверие интерпретации метрик. Не используем aggregate mAP для обещания событий, LinQ или transfer. Код/annotation artifact по этой работе не получены.

## W2-A-S04 — исходная Faster R-CNN цепочка, ограниченный доступ

Bangrong Wang, Jun Wang, Xiaofeng Xu, Xianglin Bao; *Gas mask wearing detection based on Faster R-CNN*, [DOI](https://doi.org/10.3233/AIS-220460). First online17.08.2023, issue16(1):57–71,14.03.2024. [Издатель](https://journals.sagepub.com/doi/abs/10.3233/AIS-220460).

**W2-A-F07 [access status].** PDF URL редиректит на restricted abstract; epdf/full/старый IOS URL не открылись. Поисковый индекс показывает Table1/6134images/15scenes, но этот body не получен: не выдаём его за прочитанный fulltext и не объединяем с7992images S03. Новый S03 даёт самостоятельное прочитанное основание семантики.

## W2-A-S05 — R2PPE: N95/adherence и ambiguous omission

Wanzhao Yang, Mary S. Kim, Genevieve J. Sippel, Aaron H. Mun, Kathleen H. McCarthy, Beomseok Park, Aleksandra Sarcevic, Marius George Linguraru, Ivan Marsic, Randall S. Burd. *An image dataset for surveillance of personal protective equipment adherence in healthcare*, Scientific Data12,96,17.01.2025. [DOI](https://doi.org/10.1038/s41597-024-04355-0); [официальный fulltext XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11742010/fullTextXML) получен; Methods/Dataset Annotation, Table1, Data Records прочитаны. PMC web давал recaptcha, XML независимым HTTP доступен.

**W2-A-F08 [primary annotation guide].** Mask absent = не надет либо открыты нос и рот; incomplete = нос открыт, рот закрыт. N95 complete выделен из regular mask. Неразрешимую для разметчика неоднозначность пропускали, а не помечали absent. Поэтому отсутствие annotation не отрицательное доказательство. Клинические simulations и их цвета/формы не промышленная переносимость; fit/seal и cartridge off-neck/hand не доказаны.

## W2-A-S06 — фактическая R2PPE разметка

Те же создатели. [Zenodo record](https://zenodo.org/records/13851664), publication27.09.2024,v1, modified29.09.2024; [annotations.zip](https://zenodo.org/records/13851664/files/annotations.zip?download=1),md5 record `c190615219de9b9b389c705c95d0c7f0`. Архив получен и JSON прочитан в памяти; изображения34.5GB/видео6GB не скачивались. Собственная небольшая выборка+schema summary: `r2ppe-annotation-inspection.json`.

**W2-A-F09 [artifact inspection].** `annotations/combined.json`:10034images,123751annotations,18categories. Реальны IDs7 Mask_Absent_ma,8 Mask_Incomplete_mi,9 N95_complete_nc,10 N95_Strap_s,17 PAPR_pr,18 Head. Union annotation keys: area,bbox,category_id,id,image_id,iscrowd,segmentation. Нет wearer_id/track_id/relation keys. Это state labels+bbox; N95_Strap не факт seal. No neck/hand/remove labels. Source2 actual schema подтверждена, но healthcare не industrial cartridge.

## W2-A-S07 — FMR-DB и патентный контрпример

Antonio Costantino Marceddu, Bartolomeo Montrucchio,2020. [Институциональная запись FMR-DB](https://iris.polito.it/handle/11583/2856883), DOI10.21227/wg71-v415. Реально прочитан abstract/metadata: half/full-face, disposable valved/unvalved и occlusion negatives; файлов в записи нет. IEEE DataPort через web недоступен. **W2-A-F10 [scope]:** полезная таксономическая зацепка, не полученная neck/hand annotation поставка.

CN117079082A, Nanjing Aokan Information Technology; 熊秀芳,何欣,肖伟,尹科才,董文杰; filing16.10.2023,publication17.11.2023. [Текст](https://patents.google.com/patent/CN117079082A/zh), description S201–206 прочитаны. **W2-A-F11 [patent disclosure, not measured deployment]:** lithium-cell dismantling, front/diagonal multiple4MPcameras; заднюю ориентацию предлагается разрешать другим видом. Mask/Unmask пример опирается на цвет лица/маски. Это контрпример generic «correct wearing»: camera/context-specific shortcut, без публичного neck/hand/unknown benchmark. Численные обещания качества не заимствуются.
