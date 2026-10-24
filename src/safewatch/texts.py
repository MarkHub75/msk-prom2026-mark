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
