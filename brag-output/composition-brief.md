# Hyperframes Composition Brief: АРГУС

## Objective
Промо-ролик АРГУС для начала защиты, ≤ 30,0 с, два монтажа (динамичный и «кино") из одних и тех же живых кадров.

## Output
- Composition directory: `brag-output-2026-10-25-034949/composition/` (`index.html` — динамичный, `index-kino.html` — кино, `index-vertical.html` — 1080×1920 при наличии времени)
- Rendered video: `ARGUS_promo30_dynamic.mp4`, `ARGUS_promo30_kino.mp4` (+ `brag.mp4` = лучший)
- Format: landscape — 1920×1080, 30 fps, H.264
- Duration: 30,0 с

## Source Material
- Project root: `C:\Users\User\Documents\argus-promo` (worktree origin/front/to-main 9b8b9a33), бэкенд `safewatch serve --seed` без SAFEWATCH_FAKE на :8030, демо-пакет `data/demo/argus-real`
- Primary files read: frontend/src/brand.ts, styles/ds.css, styles/targeted-visual.css, features/MasterEvent.tsx, components/Media.tsx, data/demo/argus-real/manifest.json + ATTRIBUTION.txt
- Product name: АРГУС
- Key UI moments: красный захват «Критическое событие / #241», «Подтвердить», телефон мастера «Принял, иду» / «Решено», журнал #241
- Copy that must appear verbatim: «1,17 пострадавших на 1000 работников в год», «Мастер не может видеть всё», «Росстат, 2025», «Точность там, где что-то происходит», «АРГУС», «под надзором», «Видео: Onal, Dandil, Mendeley Data, CC BY 4.0»
- Measured numbers only: детектор 10,6 кадр/с, задержка p50 308 мс (LinQ на argus-real)

## Captured material (capture/)
- `flow/*.png` — живой сайт, один чистый проход (событие #241, единственное событие пакета): desktop 3840×2160 (DPR 2), phone 1170×2532 (390 pt, DPR 3)
- `tracks-v1.json` — HUD-кадры анализа LinQ из `/api/videos/1/tracks`; рисуем только `kind=person` (пресс, ошибочно подписанный «грузовик», не рисуется и не попадает в кадр)
- Footage: `argus-real/videos/ppe-industrial4tr6.mp4` (1920×1080, 25 к/с, 20,8 с), зона 8 «Проезд погрузчиков» [0,6–0,82]×[0,45–0,9]

## Creative Direction
См. brag-plan.md. Avoid: generic SaaS language, abstract filler, неон, английский текст, синтетика.

## Visual Identity
- Background #111214, panels #18191c/#1e1f23, text #eceef1/#a1a7b0/#747b86, red #d64545, amber #c99a3a, blue accent #3d84f0
- Display: Source Sans Pro (assets/fonts, OFL), mono: Source Code Pro (bundled)

## Audio
- Music: vol-12 (ende.app, CC BY 4.0), media-start 4,0 s, бед тихий; итог ≈ −18 LUFS
- SFX: impact на тревоге, click на «Подтвердить», 2 тапа телефона, мягкий drop на журнале, impactBell_heavy на «АРГУС»
- Audio-reactive: subtle, свет за «АРГУС»

## Hyperframes Instructions
Composition contract per hyperframes skill; `check` is the gate; render locally.
