# W2_A search and access log

2026-10-23 Europe/Moscow, примерно06:10–06:19; часы подтверждены clock03:19:16UTC. Новые источники получал этот Medium-исследователь. Разметка инспектировалась, модели не запускались.

| Цепочка / запрос | Результат и предел |
|---|---|
| `SH17 dataset extended annotations on off PPE annotation GitHub`; `SH17 extended annotation download` | Авторский repo→paperTable2→Kaggle. Repo tree inspected/pinned, no separate annotation asset там. Не глобальный отрицательный поиск всех внешних архивов. |
| GitHub tree/branches/releases API | master SHA и kaggleSHA установлены. Повторный GitHub API запрос kaggle tree403, raw pinned YAML200. |
| Kaggle web→dataset view/list API | Web body0lines; оба API200. Version1/lastUpdated установлены. list pageSize1000 фактически дал200files, только partial inventory. Не объявлять полной инвентаризацией. |
| `/datasets/download/owner/slug/labels/path` |404: неверная форма URL. Исправлено на `?fileName=...`; real XML/TXT200. |
| Download twoVOC/twoTXT + firefighter image | XML/TXT прямой текст. JPG API фактически zip, сигнатураPK, извлечён единственный image; просмотрен. Annotation semantic cross-check выполнен. |
| `industrial respirator detection removed neck hand dataset annotation half face respirator`; `respirator neck detection dataset PPE`; `respirator removed dataset detection industrial`; `respirator not wearing neck detection`; `respirator on neck detection dataset` | Не получен industrial neck/hand/removal GT. FMR-DB institutional abstract открыт; IEEE DataPort недоступен. Найден R2PPE и исследован дальше. |
| `呼吸器 摘下 检测 数据集`; `防毒面具 佩戴 数据集 检测 摘下` | Сильная цепочка YOLOv8-LPE→издательPDF и predecessor FasterRCNN; патентCN117079082A. Не ограничивались повторением generic mask literature. |
| `YOLOv8-LPE 防毒面具`; `side_head_wear_wrong`; `YOLOv8-LPE github dataset`; `front_head_wear dataset github` | Новый полный 8pagePDF downloaded200 по прямому CDN, Table1/Fig2 visualverified. Небольшая реальная annotation поставка industrial не найдена. Predecessor restricted; searchsnippet не принят fulltext. |
| R2PPE PMC/Nature canonical | Ошибочные guessedNature DOI суффиксы8/4 недоступны и не использованы. Правильный DOI04355-0 установлен из official EuropePMC XML. Canonical Nature cookie redirect, PMC recaptcha. XML200: guide и metadata прочитаны. |
| R2PPE→Zenodo v1→annotations.zip |5.5MB archive200; combinedJSON parsed, categories/all annotation keys inspected; summary sample saved. Это новый реальный N95 state artifact, но другая healthcare область. |

Stop: семантика состояний/артефактов уже меняет выбор. Дальнейшее обещание industrial off-neck/hand benchmark потребует конкретного авторского архива либо целевых клипов; общие mask поиски этого разрыва не закрывают. Отсутствие найденного архива не означает его несуществования.
