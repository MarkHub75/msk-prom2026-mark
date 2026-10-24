"""Every Russian text of the product (tech.md 4). The frontend gets them through the API."""

from safewatch.types import ActorRole, Level, NoObservationReason, Role

PRODUCT_TITLE = "SafeWatch"

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
HUD_LYING = "лежит {n} с"
HUD_STILL = "неподвижен {n} с"
HUD_FEET_HIDDEN = "ноги не видны"
HUD_TOO_SMALL = "слишком мелко"
OBJECT_LABELS = {
    "person": "человек",
    "car": "легковой автомобиль",
    "bus": "автобус",
    "truck": "грузовик",
    "train": "поезд",
    "cell phone": "телефон",
}
VIDEO_NOT_READY = "Анализ видео ещё не готов"
TRACKS_WINDOW_INVALID = "Окно: from_ms меньше to_ms, не длиннее {max} мс"

# Scenarios, reasons and "why" lines (tech.md 8.3), evidence and recompute (slice 5).
SCENARIO_DESCRIPTIONS = {
    "running": "Человек бежит; рядом с техникой или в опасной зоне — красное событие.",
    "fall": "Падение человека или долгая неподвижность лёжа.",
}
SCENARIO_ACTIVE = "Сценарий работает"
SCENARIO_MODEL_MISSING = "Нет модели с классами: {classes}"
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
}
RUN_BH = "Бег {v} роста/с"
RUN_M = "Бег {v} м/с"
IN_ZONE = " в зоне «{zone}»"
NEAR_VEHICLE = " рядом с техникой"
FALL_SEEN = "Зафиксировано падение"
LYING_STILL = "Человек лежит неподвижно {n} с"
IN_REPAIR_ZONE = " в зоне ремонта"
WHY_RULE = "Правило"
WHY_RUN_BH = "Бег: скорость выше {v} роста/с дольше {s} с"
WHY_RUN_M = "Бег: скорость выше {v} м/с дольше {s} с"
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
    "relative": "в ростах человека",
}
METRIC_TITLES = {
    "speed_bh_s": "Скорость, роста/с",
    "speed_m_s": "Скорость, м/с",
    "transition_s": "Переход стоя → лёжа, с",
    "still_s": "Неподвижность, с",
}
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


def notification_text(
    level: Level, sector_name: str, reason_text: str, escalated_by_timeout: bool
) -> str:
    """`<level> · <sector> · <reason>`; the sector is its name up to the first « · »."""
    text = f"{LEVEL_TITLES[level]} · {sector_name.split(' · ')[0]} · {reason_text}"
    return text + NOT_CONFIRMED_SUFFIX if escalated_by_timeout else text
