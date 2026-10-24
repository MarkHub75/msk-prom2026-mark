"""Every Russian text of the product (tech.md 4). The frontend gets them through the API."""

from safewatch import clock
from safewatch.types import (
    ActorRole,
    CalcTier,
    Job,
    JobErrorCode,
    Level,
    LogAction,
    NoObservationReason,
    Role,
    Verdict,
)

LEVEL_TITLES: dict[Level, str] = {
    "yellow": "Жёлтая опасность",
    "red": "Красная опасность",
}

STATUS_TITLES = {  # EventStatus -> title; the trace of tech.md 6.7 needs this line as is
    "new": "Новое",
    "viewed": "Просмотрено",
    "confirmed": "Подтверждено",
    "false_alarm": "Ложное срабатывание",
    "sent_to_master": "Передано мастеру",
    "master_accepted": "Мастер принял",
    "resolved": "Решено",
    "auto_finished": "Завершилось само",
    "superseded": "Пересчитано",
}

ROLE_TITLES: dict[Role, str] = {
    "operator": "Оператор",
    "master": "Мастер смены",
    "ohs": "Охрана труда",
    "management": "Менеджмент",
    "admin": "Администратор",
}

# actor_name of an action without the X-Actor header.
DEMO_ACTOR: dict[ActorRole, str] = {
    "operator": "Оператор смены",
    "master": "Мастер смены",
    "ohs": "Специалист по охране труда",
    "management": "Руководитель",
    "admin": "Администратор",
    "system": "система",
}

NO_OBSERVATION_TEXTS: dict[NoObservationReason, str] = {
    "no_source": "Нет источника видео",
    "processing": "Видео обрабатывается",
    "failed": "Обработка не удалась",
    "ended": "Запись закончилась",
    "stale": "Данные анализа устарели",
    "dark": "Слишком темно",
    "obstructed": "Камера закрыта или не в фокусе",
}

# Scenario titles (tech.md 8.3); the plugins of slices 5 and 10 take them from here.
SCENARIO_TITLES: dict[str, str] = {
    "running": "Бег и резкие перемещения",
    "proximity": "Опасное сближение с техникой",
    "phone": "Телефон при работе",
    "fall": "Падение и неподвижность",
    "fence_crossing": "Перелезание через ограждение",
    "restricted_under": "Проход под конвейером или грузом",
    "fire_smoking": "Курение и открытый огонь",
    "no_harness": "Высота без страховочной привязи",
    "suspended_load": "Под подвешенным грузом",
    "load_carrying": "Переноска груза с нарушением",
    "no_helmet": "Без каски в зоне обязательной каски",
    "no_respirator": "Без респиратора в зоне обязательного респиратора",
}

# API errors.
REQUEST_INVALID = "Неверные данные запроса"
ROLE_REQUIRED = "Выберите роль"
ACTOR_INVALID = "Имя: до 60 символов"
NOT_IMPLEMENTED = "Функция появится в слайсе {slice}"
VIDEOS_DIR_MISSING = "Папка с видео не найдена: {path}"
FORBIDDEN_ROLE = "Действие недоступно для этой роли"

# Sectors and cameras (tech.md 9).
NAME_INVALID = "Название: от 1 до 80 символов"
DESCRIPTION_INVALID = "Описание: до 300 символов"
SECTOR_NOT_FOUND = "Сектор не найден"
CAMERA_NOT_FOUND = "Камера не найдена"
SECTOR_NAME_TAKEN = "Сектор с таким названием уже есть"
SECTOR_NOT_EMPTY = "В секторе есть камеры: сначала удалите или перенесите их"
SECTOR_HAS_HISTORY = "Сектор хранит историю удалённых камер и событий: его нельзя удалить"

# Videos and jobs (tech.md 8.1).
VIDEO_EXTENSION = "Формат не поддерживается, нужен один из: {extensions}"
VIDEO_UNREADABLE = "Видео не читается"
VIDEO_TOO_LARGE = "Файл больше {mb} МБ"
VIDEO_NOT_FOUND = "Видео не найдено"
FILE_NOT_FOUND = "Файл не найден: {path}"
JOB_NOT_FOUND = "Задача не найдена"
LIMIT_INVALID = "limit: от 1 до {max}"
JOB_NOT_FAILED = "Повторить можно только упавшую задачу"

# Backend state (tech.md 6.1, slice 3).
BACKEND_UNCHECKED = "Не проверено"
BACKEND_FAKE = "Фейк: детекции синтетические. {text}"
LINQ_OK = "LinQ доступен, {present} из {total} программ"
LINQ_UNREACHABLE = "LinQ недоступен: туннель или VPN"
LINQ_MODELS_MISSING = "Нет программ: {names}"
LINQ_BAD_ANSWER = "Неожиданный ответ Jupyter"
LOCAL_OK = "CPU (local), не LinQ: {present} из {total} моделей"
LOCAL_MODELS_MISSING = "Нет файлов моделей: {names}"

# Demo world (tech.md 8.16).
DEMO_SECTORS = [
    "Сектор 1 · Прессовый участок",
    "Сектор 2 · Склад и погрузка",
    "Сектор 3 · Сборочный цех",
    "Сектор 4 · Ремонтная зона",
]
DEMO_CAMERAS = [
    ("Камера 1.1 · Пресс №2", "Обзор пресса и рабочего места"),
    ("Камера 1.2 · Проход у прессов", "Проход между прессами"),
    ("Камера 2.1 · Погрузочная рампа", "Рампа и зона работы погрузчиков"),
    ("Камера 2.2 · Стеллажи", "Проезд между стеллажами"),
    ("Камера 3.1 · Конвейер", "Сборочный конвейер"),
    ("Камера 3.2 · Ограждение линии", "Ограждение роботизированной линии"),
    ("Камера 4.1 · Ремонтная яма", "Ремонт под вагоном"),
    ("Камера 4.2 · Верстаки", "Верстаки и сварочный пост"),
]
DEMO_ZONE_NAMES = {
    "danger": "Пресс",
    "fence": "Забор у линии",
    "under_load": "Под конвейером",
    "lying_allowed": "Ремонтная яма",
    "vehicle_path": "Проезд погрузчика",
}
DEMO_REASONS: dict[str, list[str]] = {
    "running": ["Бег 2,4 роста/с", "Бег 3,1 м/с", "Бег 2,0 роста/с рядом с техникой"],
    "proximity": ["Сближение с погрузчиком: 0,8 м", "Сближение с грузовиком: 0,4 роста"],
    "phone": ["Телефон в руке 12 с", "Телефон в руке 25 с"],
    "fall": ["Зафиксировано падение", "Человек лежит неподвижно 15 с"],
    "fence_crossing": ["Пересечение ограждения «Забор у линии»"],
    "restricted_under": ["Человек в зоне «Под конвейером»"],
}
DEMO_RESOLVE_COMMENTS = [
    "Провёл инструктаж на месте",
    "Работник отстранён до повторного инструктажа",
    "Пострадавших нет, рабочее место осмотрено",
    "Установлено дополнительное ограждение",
]


def fmt_num(x: float) -> str:
    """One decimal with a comma: 3.14 → "3,1"."""
    return f"{x:.1f}".replace(".", ",")


# HUD tags and object labels (tech.md 8.2 item 8).
HUD_SPEED_BH = "{v} роста/с"
HUD_RUN_BH = "бег {v} роста/с"
HUD_SPEED_M = "{v} м/с (калибровка)"
HUD_RUN_M = "бег {v} м/с (калибровка)"
HUD_SPEED_M_AUTO = "≈{v} м/с (авто)"
HUD_RUN_M_AUTO = "бег ≈{v} м/с (авто)"
HUD_LYING = "лежит {n} с"
HUD_STILL = "неподвижен {n} с"
HUD_FEET_HIDDEN = "ноги не видны"
HUD_TOO_SMALL = "слишком мелко"
HUD_LOAD_PROJECTION = "зона под грузом"
OBJECT_LABELS = {
    "person": "человек",
    "car": "легковой автомобиль",
    "bus": "автобус",
    "truck": "грузовик",
    "train": "поезд",
    "cell phone": "телефон",
    "fire": "огонь",
    "smoke": "дым",
    "cigarette": "сигарета",
    "no_harness": "без привязи",
    "suspended_load": "подвешенный груз",
}
VIDEO_NOT_READY = "Анализ видео ещё не готов"
TRACKS_WINDOW_INVALID = "Окно: from_ms меньше to_ms, не длиннее {max} мс"

# Scenarios, reasons and "why" lines (tech.md 8.3), evidence and recompute (slice 5).
SCENARIO_DESCRIPTIONS = {
    "running": "Человек бежит; рядом с техникой или в опасной зоне — красное событие.",
    "fall": "Падение человека или долгая неподвижность лёжа.",
    "proximity": "Человек рядом с движущейся техникой или в опасной зоне.",
    "phone": "Человек держит телефон; в опасной зоне — красное событие.",
    "fence_crossing": "Человек пересёк линию ограждения.",
    "restricted_under": "Человек в зоне под конвейером или грузом.",
    "fire_smoking": "Огонь или дым вне разрешённой зоны, курение.",
    "no_harness": "Человек в зоне работы на высоте без страховочной привязи.",
    "suspended_load": "Человек под подвешенным грузом.",
    "load_carrying": "Переноска груза с нарушением правил.",
    "no_helmet": "Человек без каски в зоне, где каска обязательна.",
    "no_respirator": "Человек без респиратора в зоне, где респиратор обязателен.",
}
SCENARIO_ACTIVE = "Сценарий работает"
SCENARIO_MODEL_MISSING = "Модель не подключена: нужны классы {classes}"
SCENARIO_SKELETON = "Сценарий уточняется: правила переноски не определены"
PARAM_TITLES = {  # key of scenarios.<id> → (title, unit)
    "speed_bh_s": ("Порог скорости без калибровки", "роста/с"),
    "speed_m_s": ("Порог скорости с калибровкой", "м/с"),
    "hold_s": ("Удержание жёлтого", "с"),
    "red_hold_s": ("Удержание красного", "с"),
    "near_vehicle_bh": ("Рядом с техникой без калибровки", "роста"),
    "near_vehicle_m": ("Рядом с техникой с калибровкой", "м"),
    "transition_s": ("Переход стоя → лёжа не дольше", "с"),
    "confirm_s": ("Удержание падения", "с"),
    "still_s": ("Неподвижность лёжа", "с"),
    "allowed_still_s": ("Неподвижность в зоне «лежать допустимо»", "с"),
    "yellow_bh": ("Жёлтая дистанция без калибровки", "роста"),
    "red_bh": ("Красная дистанция без калибровки", "роста"),
    "yellow_m": ("Жёлтая дистанция с калибровкой", "м"),
    "red_m": ("Красная дистанция с калибровкой", "м"),
    "moving_vh_s": ("Техника движется без калибровки", "высот/с"),
    "moving_m_s": ("Техника движется с калибровкой", "м/с"),
    "driver_ioa": ("Доля рамки водителя внутри техники", ""),
    "danger_hold_s": ("Удержание в опасной зоне", "с"),
    "min_person_px": ("Минимальный рост человека", "px"),
    "upper_frac": ("Верхняя доля рамки человека", ""),
    "wrist_dist_bh": ("Расстояние до запястья", "роста"),
    "max_gap_s": ("Наибольший разрыв наблюдения", "с"),
    "under_hold_s": ("Удержание под грузом", "с"),
    "fire_hold_s": ("Удержание огня", "с"),
    "smoking_hold_s": ("Удержание курения", "с"),
    "harness_hold_s": ("Удержание без привязи", "с"),
    "load_hold_s": ("Удержание под грузом", "с"),
    "head_frac": ("Верхняя доля рамки человека (голова)", ""),
}
RUN_BH = "Бег {v} роста/с"
RUN_M = "Бег {v} м/с"
IN_ZONE = " в зоне «{zone}»"
NEAR_VEHICLE = " рядом с техникой"
FALL_SEEN = "Зафиксировано падение"
LYING_STILL = "Человек лежит неподвижно {n} с"
IN_REPAIR_ZONE = " в зоне ремонта"
VEHICLE_WITH = {"car": "автомобилем", "bus": "автобусом", "truck": "грузовиком", "train": "поездом"}
PROXIMITY_BH = "Сближение с {vehicle}: {v} роста"
PROXIMITY_M = "Сближение с {vehicle}: {v} м"
PERSON_IN_ZONE = "Человек в зоне «{zone}»"
PHONE_HELD = "Телефон в руке {duration_s} с"
FENCE_CROSSED = "Пересечение ограждения «{zone}»"
FENCE_UNSEEN = ": момент не виден"
FIRE_OUTSIDE = "Открытый огонь вне разрешённой зоны"
SMOKING = "Курение"
NO_HARNESS = "Работа на высоте без привязи"
NO_HELMET = "Без каски в зоне «{zone}»"
NO_RESPIRATOR = "Без респиратора в зоне «{zone}»"
UNDER_LOAD = "Человек под подвешенным грузом"
WHY_PROXIMITY_BH = (
    "Сближение: техника движется, дистанция до {red} роста — красный, до {yellow} — жёлтый"
)
WHY_PROXIMITY_M = (
    "Сближение: техника движется, дистанция до {red} м — красный, до {yellow} м — жёлтый"
)
WHY_HOLD = "{rule} дольше {s} с"
WHY_RULE = "Правило"
WHY_RUN_BH = "Бег: скорость выше {v} роста/с дольше {s} с"
WHY_RUN_M = "Бег: скорость выше {v} м/с дольше {s} с"
WHY_SPEED = "Скорость"
WHY_SPEED_AUTO = "автокалибровка по росту людей ({n} замеров, точность около ±20 %)"
WHY_SPEED_CALIBRATION = "по калибровке камеры"
WHY_FALL = "Падение: переход стоя → лёжа не дольше {t} с, лежит дольше {s} с"
WHY_LYING = "Неподвижность: лежит без движения дольше {s} с"
WHY_METHOD = "Метод"
WHY_CONFIDENCE = "Уверенность детекции"
WHY_UNCERTAIN = "Потеря видимости"
WHY_SECONDS = "{n} с"
METHOD_TITLES = {
    "pose": "поза",
    "bbox": "рамка",
    "calibrated": "калибровка",
    "auto": "автокалибровка",
    "relative": "в ростах человека",
}
METRIC_TITLES = {
    "speed_bh_s": "Скорость, роста/с",
    "speed_m_s": "Скорость, м/с",
    "transition_s": "Переход стоя → лёжа, с",
    "still_s": "Неподвижность, с",
    "distance_bh": "Дистанция до техники, роста",
    "distance_m": "Дистанция до техники, м",
    "score": "Уверенность объекта",
}
AUTOCAL_FEW = "Мало стоящих людей в кадре: {n} из {need}"
AUTOCAL_PERSPECTIVE = "Рост людей не согласуется с перспективой"
AUTOCAL_ONE_ROW = "Все люди стоят в одном ряду кадра: перспективу не оценить"
EVIDENCE_NOT_FOUND = "Кадр не найден"
ARTIFACTS_MISSING = "Нет результатов инференса этого видео: загрузите его заново"

# Broadcast, states, notifications (tech.md 8.5, 8.8, 8.9; slice 6).
STATE_NORMAL = "Норма"
SECTOR_NO_OBSERVATION = "Нет наблюдения: {n} из {total} камер"
SECTOR_EMPTY = "В секторе нет камер"
NO_READY_VIDEO = "У камеры нет готового видео"
PREVIEW_NOT_FOUND = "Нет кадра: у камеры нет готового видео"
NOT_CONFIRMED_SUFFIX = " · Не подтверждено оператором"

# Event screen and operator decisions (tech.md 8.6, 9; slice 7).
EVENT_NOT_FOUND = "Событие не найдено"
INVALID_TRANSITION = "Действие недоступно в текущем статусе события"
COMMENT_REQUIRED = "Опишите принятые меры"
COMMENT_TOO_LONG = "Комментарий: до 500 символов"
WHY_REASON = "Причина"

# Calibration, zones, camera rules, recompute (tech.md 8.11, 8.12, 9; slice 9).
CAL_POINTS_COUNT = "Нужно от 4 до 8 точек"
CAL_POINTS_MISMATCH = "Число точек кадра и пола должно совпадать"
CAL_CONTROL_MAX = "Контрольных точек: до 8"
CAL_COLLINEAR = "Три точки на одной прямой"
POINTS_OUTSIDE = "Точки вне кадра"
ZONE_KIND_UNKNOWN = "Неизвестный тип зоны"
ZONE_NAME_INVALID = "Название зоны: от 1 до 60 символов"
ZONE_LINE_POINTS = "Линия — ровно 2 точки"
ZONE_POLYGON_POINTS = "Полигон: от 3 до 32 точек"
ZONE_DEGENERATE = "Полигон без площади: точки на одной прямой"
ZONE_NOT_FOUND = "Зона не найдена"
SCENARIO_NOT_FOUND = "Сценарий не найден"
PARAM_UNKNOWN = "Неизвестный параметр {key}"
PARAM_RANGE = "Параметр {key}: от {lo} до {hi}"
RECOMPUTE_COMMENT = "Пересчёт: версия анализа {n}"


# Journal and CSV export (tech.md 9, 16; slice 12).
FILTER_INVALID = "Неверный фильтр: {field}"
ACTION_TITLES: dict[LogAction, str] = {
    "published": "опубликовано",
    "viewed": "просмотрено",
    "confirmed": "подтверждено",
    "false_alarm": "ложное срабатывание",
    "sent_to_master": "передано мастеру",
    "level_escalated": "повышено до красного",
    "timeout_escalated": "эскалация по таймауту",
    "master_accepted": "мастер принял",
    "resolved": "решено",
    "auto_finished": "завершилось само",
    "superseded": "пересчитано",
    "identified": "идентификация",
}
VERDICT_TITLES: dict[Verdict, str] = {
    "none": "нет",
    "confirmed": "подтверждено",
    "false_alarm": "ложное",
}
YES, NO = "да", "нет"
CSV_COLUMNS = [
    "id",
    "опубликовано (МСК)",
    "начало",
    "сектор",
    "камера",
    "зона",
    "сценарий",
    "уровень",
    "статус",
    "вердикт",
    "эскалация по таймауту",
    "причина",
    "длительность (с)",
    "демо",
    "sha256 кадра",
    "история",
    "ФИО",
    "Должность",
    "Бригада",
]


# Statistics (tech.md 8.13, 9; slice 13).
PERIOD_INVALID = "Неверный период"
TREND_CAVEAT = "Сравнение до и после не доказывает причину."
TREND_LESS = "Жёлтых нарушений стало меньше на {pct} % ({span}). " + TREND_CAVEAT
TREND_MORE = "Жёлтых нарушений стало больше на {pct} % ({span}). " + TREND_CAVEAT
TREND_SAME = "Жёлтых нарушений без изменений ({span}). " + TREND_CAVEAT
TREND_NO_DATA = "Недостаточно данных для сравнения"

# Quality evaluation (tech.md 8.18, 9; slice 14).
EVAL_LABELS_INVALID = "Разметка: неверное поле {field}"
EVAL_INTERVAL_INVALID = "Разметка: start_s должно быть меньше end_s ({field})"
EVAL_TITLE = "# Оценка качества: {labels}, видео {hours} ч"
EVAL_COLUMNS = [
    "сценарий",
    "эталонов",
    "эпизодов",
    "TP",
    "FN",
    "FP",
    "дубли",
    "поздние",
    "precision",
    "recall",
    "F1",
    "FP в час",
    "задержка p50, с",
    "задержка p95, с",
    "n",
]
EVAL_FOOTNOTE = (
    "Дедлайн подтверждения {deadline} с. Сноска: recall валиден только при полной разметке видео."
)


# Delivery to outside systems (slice 15): `deliveries.error` of a failed attempt.
DELIVERY_TIMEOUT = "таймаут"
DELIVERY_HTTP = "ответ HTTP {status}"
DELIVERY_UNREACHABLE = "нет связи ({error})"

# Call to the master (slice 23, tech.md 8.24): `Delivery.status_text` of a `call:<name>` row and
# `Channel.target` of a call channel without a number.
CALL_SENT = "Звонок отправлен"
CALL_DELIVERED_STUB = "Звонок доставлен (заглушка)"
CALL_NO_NUMBER = "заглушка"

# Payback and scale calculator (slice 24, tech.md 8.25): tier titles, breakdown lines, sources
# and titles of the measured numbers.
CALC_INVALID = "Неверное значение: {field}"
CALC_TIER_TITLES: dict[CalcTier, str] = {
    "base": "Базовый",
    "extended": "Расширенный",
    "max": "Максимальный",
}
CALC_ACCELERATORS = "Ускорители LinQ"
CALC_SERVERS = "Серверы под ускорители"
CALC_INTEGRATION = "Пусконаладка и подключение камер"
CALC_LIGHT_SOUND = "Световой и звуковой сигнал у зон"
CALC_SPEAKERS = "Громкоговорители в цеха"
CALC_NEW_CAMERAS = "Новые IP-камеры с монтажом"
CALC_PAYBACK = "Окупаемость"
CALC_PAYBACK_MONTHS = "{n} мес."
CALC_NOT_PROFITABLE = "Не окупается при этих допущениях"
CALC_OVERRIDDEN = "задано в расчёте"
CALC_CAPACITY = "Пропускная способность одного ускорителя LinQ по замеру"
CALC_RTT = "Время ответа TPU, p50 последних задач LinQ"
CALC_EVENTS = "Событий эфира на камеру в день"
CALC_EVENTS_SOURCE = "журнал: события эфира за {days} дн. на камеру с событиями"


def fmt_rub(x: float) -> str:
    """Whole rubles with space groups: 500000 → "500 000 ₽"."""
    return f"{round(x):,} ₽".replace(",", " ")


def measured_jobs(n: int) -> str:
    """«замер приложения: 2 задачи»: the source of a number measured on LinQ."""
    one, few = n % 10 == 1 and n % 100 != 11, 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14
    return f"замер приложения: {n} {'задача' if one else 'задачи' if few else 'задач'}"


def weeks_span(n: int) -> str:
    """«4 недели к 4 неделям»: the Russian plural after a number, then the dative."""
    one, few = n % 10 == 1 and n % 100 != 11, 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14
    word = "неделя" if one else "недели" if few else "недель"
    return f"{n} {word} к {n} {'неделе' if one else 'неделям'}"


def notification_text(
    level: Level, sector_name: str, reason_text: str, escalated_by_timeout: bool
) -> str:
    """`<level> · <sector> · <reason>`; the sector is its name up to the first « · »."""
    text = f"{LEVEL_TITLES[level]} · {sector_name.split(' · ')[0]} · {reason_text}"
    return text + NOT_CONFIRMED_SUFFIX if escalated_by_timeout else text


# Demo pack and job texts (tech.md 8.19; slice 17).
DEMO_FAKE_REFUSED = "Демо-пакет на фейке: добавьте --allow-fake"
DEMO_OUT_NOT_EMPTY = "Папка пакета не пуста: {path}"
DEMO_LAYOUT_INVALID = "Раскладка демо-пакета: неверное поле {field}"
DEMO_MANIFEST_INVALID = "manifest.json: неверное поле {field}"
DEMO_MODEL_UNKNOWN = "Модели {model} нет в config/models.yaml"
DEMO_SHA_MISMATCH = "sha256 видео {file} не совпадает с manifest.json"
ARTIFACT_INVALID = "Артефакт {file} не читается: {error}"
JOB_QUEUED = "В очереди"
JOB_RUNNING_LINQ = "Обработка на LinQ"
JOB_RUNNING_LOCAL = "Обработка на CPU (local)"
JOB_RETRY_UNAVAILABLE = "LinQ недоступен, повтор в {time}"
JOB_RETRY_TIMEOUT = "LinQ не ответил вовремя, повтор в {time}"
JOB_RETRY = "Повтор в {time}"
JOB_DONE = "Готово"
JOB_FAILED_TEXTS: dict[JobErrorCode, str] = {
    "linq_unavailable": "LinQ недоступен: попробуйте позже",
    "timeout": "LinQ не ответил вовремя: попробуйте позже",
    "remote_error": "Неожиданный ответ LinQ",
    "bad_output": "Неожиданный ответ LinQ",
    "model_missing": "Нет программы модели на LinQ",
    "video_unreadable": "Видео не читается",
    "artifacts_missing": ARTIFACTS_MISSING,
    "internal": "Внутренняя ошибка",
}


def job_status_text(job: Job, tz: str) -> str:
    """`Job.status_text` (tech.md 8.19); times in the product time zone `tz`."""
    if job.status == "queued":
        return JOB_QUEUED
    if job.status == "running":
        return JOB_RUNNING_LINQ if job.backend == "linq" else JOB_RUNNING_LOCAL
    if job.status == "done":
        return JOB_DONE
    if job.status == "failed":
        return JOB_FAILED_TEXTS[job.error_code or "internal"]
    at = job.next_attempt_at
    time = "" if at is None else clock.local(at, tz).strftime("%H:%M")
    if job.error_code == "linq_unavailable":
        return JOB_RETRY_UNAVAILABLE.format(time=time)
    if job.error_code == "timeout":
        return JOB_RETRY_TIMEOUT.format(time=time)
    return JOB_RETRY.format(time=time)


# Manual identification of the violator (tech.md 8.27; slice 26).
IDENTITY_TOO_LONG = "Поле: до 80 символов"
IDENTITY_CLEARED = "Идентификация очищена"
IDENTITY_EMPTY = "—"


def identity_comment(person_name: str, person_position: str, crew: str) -> str:
    """The comment of an `identified` row; an empty field shows as a dash."""
    if not (person_name or person_position or crew):
        return IDENTITY_CLEARED
    name, position, team = (v or IDENTITY_EMPTY for v in (person_name, person_position, crew))
    return f"ФИО: {name}; должность: {position}; бригада: {team}"
