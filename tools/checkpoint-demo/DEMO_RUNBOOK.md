# DEMO_RUNBOOK: SafeWatch на чекпойнте

Папка: `tools/checkpoint-demo/` (ветка `demo/checkpoint`). Нужен Node 22+ (на машине 24). Команды для PowerShell или cmd. В Git Bash вместо `.\mock.cmd` пишите `node src/server.mjs`, вместо `.\demo.cmd` — `node bin/demo.mjs`.

## 1. Мок (вместо бэкенда)

```powershell
cd tools\checkpoint-demo
.\mock.cmd                    # REST http://127.0.0.1:4010, WS ws://127.0.0.1:4011/ws
.\mock.cmd --escalation       # с автоэскалацией красного через 45 с (8.7), по умолчанию выкл
```

**Не запускать вместе с `npm run mock` из `frontend/`**: порты те же (4010/4011). Мок скажет «Порт 4010 занят» и выйдет с кодом 2. Остановка: Ctrl+C в окне мока.

## 2. Фронт

| Против чего | Команда в `frontend/` | Адреса |
| --- | --- | --- |
| мок | `npm run dev:mock` | `.env.mock` уже смотрит на 4010/4011, CORS открыт для 5173 |
| бэкенд | `npm run dev` | прокси Vite `/api` и `/ws` → 127.0.0.1:8000; `VITE_API_BASE` пустой (у бэкенда нет CORS) |

Бэкенд для показа: `SAFEWATCH_FAKE=1` и `uv run safewatch serve --seed` (порт 8000). Фейковые детекции, не LinQ.

## 3. Режиссёр (темп задаёт ведущий)

```powershell
.\demo.cmd status            # что опубликовано и в каких статусах
.\demo.cmd next              # 1-й раз: ЖЁЛТОЕ «Бег 2,4 роста/с», Сектор 1, Камера 1.1 · Пресс №2
                             # оператор: «Подтверждаю» → confirmed
.\demo.cmd next              # 2-й раз: КРАСНОЕ «Зафиксировано падение», сирена, захват экрана
                             # оператор: «Подтверждаю» → мастеру; мастер: «Принял, иду» → «Решено» + комментарий
.\demo.cmd reset             # мир как после запуска; рвёт WS, фронт перечитает экран сам
.\demo.cmd ws-drop           # проверить переподключение фронта
.\demo.cmd fault evidence-404   # кадр отвечает 404; fault 500 — все /api/* отвечают 500; fault off — снять
```

Красное не публикуется, пока жёлтое ждёт оператора (на бэкенде оно завершилось бы само). Нужно сразу — `.\demo.cmd next --force`.

## 4. Smoke

```powershell
.\smoke.cmd --target mock    # мок должен быть запущен; ждём: PASS 30 · FAIL 0 · SKIP 0, код 0
.\smoke.cmd --target real    # бэкенд на 8000 с SAFEWATCH_FAKE=1 и --seed
```

Коды: `0` — сценарий прошёл, можно показывать; `1` — есть FAIL; `3` — FAIL нет, но шаги SKIP (слайс бэкенда не готов, 501). Smoke мока в конце делает `reset`. Smoke бэкенда грузит в «Камеру 1.1» синтетический ролик `synthetic_demo_<время>.mp4` (20 с, ffmpeg) и запускает эфир. При `fake=false` на LinQ он ничего не грузит.

## 5. На показе упало

| Что | Действие (до минуты) |
| --- | --- |
| WS отвалился, лента не обновляется | фронт переподключается сам (1, 2, 4, 8 с). Не помогло — F5 |
| бэкенд упал или отвечает 5xx | 1) Ctrl+C у `npm run dev`; 2) `.\mock.cmd` в `tools\checkpoint-demo`; 3) в `frontend\`: `npm run dev:mock`; 4) F5, роль «Оператор»; 5) `.\demo.cmd next` с нужного шага |
| мок завис | Ctrl+C, `.\mock.cmd`, `.\demo.cmd reset`, F5 |
| кадр не грузится | `.\demo.cmd fault off`; проверить, что `evidence\yellow.jpg` и `red.jpg` на месте |

Мок держите запущенным заранее во втором окне: порты 4010/4011 бэкенду не мешают.

## 6. Свои кадры

1. Положите `evidence\yellow.jpg` и `evidence\red.jpg` (16:9) с теми же именами.
2. В `evidence\evidence.json` поправьте `bbox` (`x1, y1, x2, y2` в долях кадра 0..1).
3. `.\demo.cmd reset`. Код не меняется.

Рамка на кадре — ручная разметка. Не называйте её детекцией модели. Заглушки перерисовывает `py -3.12 evidence\make_placeholders.py`.

## 7. Свой стек проверок (не мешает 4010/4011/5173 и 8000)

- `node bin/local-checks.mjs`: мок 4110/4111 (поднимет сам), smoke mock ×20, e2e на фикстуре и на фронте `C:\Users\User\Documents\mosprom2026-hack\frontend` (Vite 5174 со своим конфигом и кэшем во %TEMP%; файлы фронта не меняются, `npm install` там не делается).
- `node e2e/run.mjs [--fixture | --front DIR] [--no-bugs]`: один прогон e2e, скриншоты в `e2e/screens/` (фикстура в `e2e/screens/fixture/`), провалы фронта в `e2e/FRONT_BUGS.md`.
- Режиссёр для своего мока: `SW_MOCK_URL=http://127.0.0.1:4110 node bin/demo.mjs status` (`reset --keep-ws` — без разрыва WS).
- `node bin/watch.mjs` (цикл, раз в 30 мин): main на 8000 + `local-checks`, строка в `WATCH_LOG.md`.
