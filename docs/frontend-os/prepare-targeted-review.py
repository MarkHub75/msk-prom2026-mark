"""Author a supported HRE capture recipe for the approved targeted corrections."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
if args.output.exists():
    raise SystemExit('Use a new recipe version.')

def expect(selector, value):
    return dict(action='expect', selector=selector, value=value)

def click(selector):
    return dict(action='click', selector=selector)

def fill(selector, value):
    return dict(action='fill', selector=selector, value=value)

wait = dict(action='wait', ms=1000)
identity = [expect('.actor-dialog[open]', 'Представьтесь для действия'), fill('.actor-dialog input', 'Проверка интерфейса'), click('.actor-dialog button[type="submit"]'), wait]
states = []

def state(name, label, route, setup, recording=None):
    value = dict(id=name, label=label, route=route, setup=setup + [wait], fixture_id='safewatch-targeted-contract-v1', equivalence='signal-post-targeted-' + name,
                 description=label + '. Реальный браузер, исправленный продукт. Явные детерминированные fixtures UI; не LinQ/CCTV. Полный внешний mock E2E и проверки настоящего backend приложены отдельно.')
    if recording:
        value['recording'] = recording
    states.append(value)

state('dispatch-critical', 'Пульт · активная очередь отдельно от истории', '/operator/?review=critical&reset=1', [expect('[data-testid="active-event-count"]', '3'), expect('[data-testid="closed-event-count"]', '1')])
state('dispatch-normal', 'Пульт · активных 0, завершённых 4', '/operator/?review=normal&reset=1', [expect('[data-testid="active-event-count"]', '0'), expect('[data-testid="closed-event-count"]', '4'), click('.closed-event-history summary'), expect('.closed-event-history', 'Недавно завершено')])
state('incident-compare', 'Incident Focus · доказательство и последующий кадр', '/events/41/?review=critical&reset=1', [expect('[data-testid="incident-focus"]', 'Вход в опасную зону'), expect('.observation-panel', 'Последующее наблюдение')])
state('actor-required', 'Явное имя перед первым действием', '/events/41/?review=critical&reset=1', [expect('button[data-action="confirm"]', 'Подтвердить'), click('button[data-action="confirm"]'), expect('.actor-dialog[open]', 'Представьтесь для действия')])
state('red-takeover', 'Красная тревога · исходная композиция сохранена', '/events/41/?review=critical&reset=1&takeover=1', [expect('.takeover', '#41')])
master_recording = dict(steps=[click('button[data-action="accept"]')] + identity + [expect('[data-testid="event-status"]', 'Принято мастером'), fill('textarea[data-testid="measures"]', 'Участок проверен. Оборудование остановлено, проход освобождён.'), click('button[data-action="resolve"]'), wait, expect('[data-testid="event-status"]', 'Решено')], hold_ms=1500)
state('master-task', 'Мастер · поручение и полный сценарий отчёта', '/master/events/43/?review=critical&reset=1', [expect('button[data-action="accept"]', 'Прин')], master_recording)
state('master-report', 'Мастер · обязательные меры перед завершением', '/master/events/43/?review=critical&reset=1', [expect('button[data-action="accept"]', 'Прин'), click('button[data-action="accept"]')] + identity + [expect('[data-testid="event-status"]', 'Принято мастером'), fill('textarea[data-testid="measures"]', 'Участок ограждён. Оборудование остановлено, выполнен осмотр.'), expect('button[data-action="resolve"]', 'Отправить')])
state('evidence-unavailable', 'Падение · честное отсутствие подходящего материала', '/events/43/?review=critical&reset=1', [expect('[data-testid="incident-focus"]', 'Падение и неподвижность'), expect('.evidence-panel', 'Доказательство отсутствует')])
state('journal-resolved', 'Журнал · серверные фильтры и история решения', '/ohs/journal/?review=critical&reset=1&status=resolved&level=yellow', [expect('[data-testid="journal-view"]', 'Журнал событий'), expect('tr[data-event-id="44"]', 'Решено')])
state('camera-hud', 'Камера · уточнённые подписи существующего HUD', '/operator/cameras/1/?review=critical&reset=1', [expect('[data-testid="camera-view"]', 'Камера')])
state('incident-gone', 'Удалённое событие · 404 без старых действий', '/events/41/?review=empty&reset=1', [expect('[role="alert"]', 'Событие не найдено')])
state('ws-disconnected', 'Потеря канала · явный статус и текущая очередь', '/operator/?review=disconnected&reset=1', [expect('.connection', 'Канал событий отключён'), expect('[data-testid="active-event-count"]', '3')])

recipe = dict(version=1, product_id='signal-post-integrated-v1', launch=dict(kind='static'), motions=['normal', 'reduced'],
              viewports=[dict(id='desktop', label='Desktop', width=1440, height=900, device_scale_factor=1), dict(id='mobile', label='Mobile', width=390, height=844, device_scale_factor=1)], states=states)
args.output.write_text(json.dumps(recipe, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(dict(states=len(states), images=len(states) * 4, recordings=4)))
