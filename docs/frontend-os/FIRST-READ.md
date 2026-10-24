# SafeWatch — текущий рабочий frontend

Утверждённый «Сигнальный пост» сохранён. Точечные исправления после HUMAN_PRODUCT_REVIEW KEEP выполнены. Внешний stateful mock E2E **PASS 8/8**, frontend gate **PASS 19/19**. OS достигла следующего обязательного checkpoint **HUMAN_FINAL_PRODUCT_REVIEW**; финальной приёмки исправлений ещё нет.

## Открыть

- [Приложение с внешним stateful-моком](http://127.0.0.1:5185/operator?review=real). Мир после проверки сброшен; сценарий публикуется через CLI мока.
- [Новый настоящий HRE исправленных экранов](http://127.0.0.1:8197/human_review/renderer/v1.1/index.html?manifest=../../../runs/safewatch-20261024-working-r3/human-review/hre-signal-post-integrated-v1-b1-r0/attempt-1-fa4a4eac/manifest.json).
- [Portable HRE working-v2.zip](/mnt/d/templates/frontend-hackathon-os/production/runs/safewatch-20261024-working-r3/review-delivery/working-v2.zip): копия канонического пакета, неизменённый approved renderer, исходники и раздельные QA-доказательства.
- [Текущий FRONTEND_STATUS](FRONTEND_STATUS.md), [проверки и ограничения v2](INTEGRATION_REVIEW_v2.md), [скриншоты внешнего мока](review-v2/README.md).

HRE использует renderer 1.1.0, manifest/decision schemas 1.0.0. Новый пакет содержит **12 состояний, 48 PNG на 1440×900 и 390×844 в normal/reduced motion, 4 настоящие записи сценария мастера**, 3 документа происхождения. Никаких новых концепций или самостоятельного редизайна. Проверки 1280×800 и 25 captures внешнего мока приложены отдельно.

## Исправленный продукт

App Shell и пять ролей; `/operator`, `/operator/sectors/:sectorId`, `/operator/cameras/:cameraId`, `/events/:eventId`, `/master`, `/master/events/:eventId`, `/master/shift`, `/ohs/journal`.

Активная очередь отделена от завершённой истории по серверным metadata; normal показывает 0 / 4. У синтетического падения удалены неподходящие кадр и видео. Явное имя запрашивается перед первым действием, фиктивного X-Actor нет. Оба блока сравнения Incident видны на первом экране 1440×900. HUD использует точные objects/bbox кадра и контрастную подпись. Журнал работает с реальными filters/facets/cursor API. Исправлены stale actions после reset/404 и повторная загрузка evidence по тому же URL.

## Повторить внешний сценарий

Текущий отдельный mock worktree: `/mnt/d/templates/msk-promhack/safewatch-checkpoint-mock`, detached `f7520320`; новый `93ad427f` меняет только журнал наблюдения и его артефакты, runtime-код тот же. Он получен из `origin/demo/checkpoint`, не скопирован в frontend и не изменён. REST4010, WS4011.

Если серверы остановлены, в отдельных терминалах:

```bash
cd /mnt/d/templates/msk-promhack/safewatch-checkpoint-mock/tools/checkpoint-demo
npm ci
npm run mock
```

```bash
cd /mnt/d/templates/msk-promhack/safewatch-os-first-pass/frontend
npm ci
npm run dev:mock -- --host 127.0.0.1 --port 5185
```

Из каталога mock: `node bin/demo.mjs reset`, затем `node bin/demo.mjs next` публикует жёлтое. Подтвердить его через UI с явным именем; следующий `next` публикует красное. Дальше takeover → Incident → подтвердить/передать → роль «Мастер» → принять → обязательные меры → завершить → журнал. `node bin/demo.mjs ws-drop` проверяет восстановление канала. Smoke сбрасывает мир, поэтому не запускается одновременно с ручным сценарием.

`review=real` явно отключает сохранённые локальные fixtures. Мок и его изображения синтетические, видео/эфира у него нет. Против настоящего backend запускать обычный `npm run dev`: Vite proxy `/api` и `/ws` →8000, без cross-origin API base.

## OS, человеческие решения и повторное открытие HRE

Run `/mnt/d/templates/frontend-hackathon-os/production/runs/safewatch-20261024-working-r3`, ID `1b7496bc17f942cb9e483483e329ca2b`. Реальный режим OS4 — interactive Codex + controller; автономный worker не заявляется. `drive` не создаёт продукт сам.

Концепция `signal-post` и механизмы `response-route`, `sector-atlas`, `evidence-desk`, `shift-ribbon`, `video-switchboard` зарегистрированы через настоящий `human-feedback`. Позднейший KEEP рабочих экранов зарегистрирован через `single-product-completion`, base **signal-post-command**; это actual chat feedback, не выдуманный HRE export. Далее штатные `review-spec` → `creative-receipt final-product` автоматически создали новый пакет. Код OS не менялся. Новых исследований и изображений не генерировалось.

Из корня OS:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=production python3 -B -m hackathon_os.cli --run production/runs/safewatch-20261024-working-r3 next
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=production python3 -u -B -m hackathon_os.cli --run production/runs/safewatch-20261024-working-r3 review-serve --review hre-signal-post-integrated-v1-b1-r0 --port 8197
```

Новый completion product ID требуется контроллером; прежняя утверждённая база сохранена. Автоматической cross-candidate baseline нет, HRE честно показывает NO BASELINE. [Предыдущее утверждённое рабочее ревью](http://127.0.0.1:8198/human_review/renderer/v1.1/index.html?manifest=../../../runs/safewatch-20261024-working-r3/human-review/hre-signal-post-command-b1-r0/attempt-2-eeb37be0/manifest.json) остаётся доступным. Сохранены шесть прежних концепций, все исходные run/ошибочные attempts и архив working-v1; recovery описан в run/evidence/working-review-recovery.json. Процесс не начинался заново.

## Git и интеграционные границы

Ветка **codex/safewatch-frontend-v1**, изолированный worktree `/mnt/d/templates/msk-promhack/safewatch-os-first-pass`; вся история предыдущей `codex/safewatch-os-first-pass` сохранена. Проверенные этапы коммитятся и пушатся только в собственную ветку. Main, backend, mock, DTO, CLAUDE.md и progress.md не изменялись.

REST-типы из настоящего OpenAPI1.0.0, WS по настоящим schema/examples; последние upstream contracts не изменились. Текущий S0 backend: health200/WShello, business501. Свежая попытка S5 в доступном runtime остановилась на отсутствующем cv2; последний R5 runtime не проверен. Полная интеграция с настоящим backend **не объявляется завершённой**. Детали, известные P2 и следующие зависимости — в FRONTEND_STATUS и INTEGRATION_REVIEW_v2.
