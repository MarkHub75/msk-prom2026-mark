# Дизайн-система

Токены и стили: `src/styles/ds.css` (подключён последним в `main.tsx`). Компоненты: `src/components/ui.tsx`, бейджи: `src/components/Badges.tsx`.
Старые имена переменных (`--surface`, `--line`, `--text`, `--muted`, `--accent`, `--red`, `--amber`, `--timecode`) остаются и указывают на новые токены.

## Токены

| Группа | Переменные |
|---|---|
| Поверхности | `--ds-bg-0` фон/зазоры, `--ds-bg-1` тело панели, `--ds-bg-2` шапки и панели инструментов, `--ds-bg-3` поля и hover, `--ds-bg-4` нажатое, `--ds-well` колодец видео |
| Линии | `--ds-line-dark` (между панелями), `--ds-line` (внутри), `--ds-line-strong` (контролы) |
| Текст | `--ds-text`, `--ds-text-2` (подписи), `--ds-text-3` (третичный) |
| Акцент | `--ds-accent`, `--ds-accent-hover`, `--ds-accent-bg` (выбор), `--ds-timecode` (время, таймкоды) |
| Семантика | `--ds-red(-bg,-line)` тревога, `--ds-amber(-bg,-line)` внимание, `--ds-green(-bg)` норма, `--ds-grey(-bg)` нет наблюдения |
| Отступы | `--s1` 4 … `--s8` 32 (шаг 4px) |
| Радиусы, тени | `--r1` 2, `--r2` 3, `--r3` 4; `--shadow-pop`, `--shadow-modal`; `--focus` (фокус-кольцо) |
| Оболочка | `--ds-top-h` 44, `--ds-status-h` 26, `--ds-rail-w`, `--ds-panel-head` 30 |

Правило цвета: красный и янтарный только там, где тревога/внимание; синий только для выбора, фокуса и времени. Уровень и состояние всегда текст + иконка.

## Компоненты (`import { ... } from "../components/ui"`)

| Имя | Пропсы | Пример |
|---|---|---|
| `Icon` | `name: IconName`, `size=16` | `<Icon name="camera" />` — lucide, stroke 1.75. Имена: `arrow back camera camera-off play pause grid list sound mute check chevron chevron-down cross eye eye-off monitor bell journal rules chart settings user users pin alert critical info ok no-observation clock refresh search filter download external more file server cpu wifi wifi-off activity shield inbox spinner` |
| `Panel` | `title`, или `tabs[{id,label}]` + `active` + `onTab`; `tools`, `flush`, `className` | `<Panel title="Камеры" tools={<IconButton icon="refresh" label="Обновить" size="sm" />}>…</Panel>` |
| `[data-panel]` | атрибут на любом блоке | `<section data-panel="Очередь тревог">` — та же шапка-таб из CSS |
| `Button` | `variant: primary\|secondary\|ghost\|danger`, `size: sm\|md`, `icon`, `iconRight`, `busy` | `<Button variant="primary" icon="check">Подтвердить</Button>` |
| `buttonClass(variant, size)` | — | `<Link className={buttonClass("ghost","sm")} to="…">` |
| `IconButton` | `icon`, `label` (aria-label + тултип), `size`, `variant`, `pressed` | `<IconButton icon="eye" label="HUD" pressed={hud} />` |
| `Segmented` | `options[{id,label,icon?,count?}]`, `value`, `onChange`, `label`, `size` | `<Segmented label="Уровень" value={f} onChange={setF} options={[{id:"all",label:"Все"}]} />` |
| `Field` | `label`, `hint`, `error`, children — контрол | `<Field label="Поиск"><TextInput icon="search" /></Field>` |
| `TextInput` | input-пропсы + `icon` | |
| `Select` | select-пропсы, `<option>` в children | |
| `Checkbox` | `label` + input-пропсы | |
| `Switch` | `label`, `checked`, `onChange(next)` | |
| `Badge` | `tone: neutral\|accent\|red\|amber\|green\|grey`, `icon`, `solid` | `<Badge tone="green" icon="ok">Норма</Badge>` |
| `LevelBadge`, `StatusBadge`, `StateBadge` (Badges.tsx) | `level` / `status` / `state` (+`text`, `solid`) | `<StateBadge state="no_observation" />` — серый пунктир, не зелёный |
| `Level`, `Status` | как раньше | |
| `Kpi` | `label`, `value`, `unit`, `delta`, `deltaTone`, `hint`, `spark`, `tone` | `<Kpi label="Событий" value={57} spark={<Sparkline values={byDay} />} />` |
| `Sparkline` | `values: number[]`, `tone`, `label` | только значения из API |
| `Tooltip` | `content`, `side: top\|bottom\|right` | `<Tooltip content="Время сервера"><span>…</span></Tooltip>` |
| `Empty` / `EmptyState` | `title`, `text`, `icon`, children | |
| `Loading`, `Skeleton` | `text` / `lines`, `height` | `<Skeleton lines={4} />` |
| `ErrorNotice` | `error`, `retry`, `compact` | как раньше |
| `ConfirmDialog` | `open`, `title`, `text`, `confirmLabel`, `cancelLabel`, `tone: primary\|danger`, `busy`, `onConfirm`, `onCancel` | Esc и клик по фону отменяют |
| `useToast()` | `toast({ title, text?, tone?: neutral\|green\|amber\|red })` | провайдер уже в `AppShell` |
| `Kbd`, `Timecode` | children; `Timecode tone="accent"` | `<Timecode tone="accent">00:14</Timecode>` |
| `PageHeading`, `PanelHeading`, `Breadcrumb` | как раньше; выглядят как полоса инструментов / шапка панели | |

## CSS-классы без компонента

- Таблица: `<table className="ds-table">`, строка `tr.is-selected` или `aria-selected`, ячейки `td.num` (моно, вправо) и `td.mono`. Шапка липкая внутри прокручиваемого `.shell-main`.
- Кнопки старого вида `.button`, `.button-primary`, `.button-danger`, `.button-small` нарисованы теми же стилями, что `Button`.
- Анимации: `ds-row-in` (появление строки), `ds-alarm-pulse` (пульс красной рамки), `ds-fade`. Всё гасится `prefers-reduced-motion`.

## Оболочка

Верхняя панель (продукт из `brand.ts`, вкладки ролей, источник детекций `data-testid="backend"`, канал событий, звук тревог, сотрудник, часы МСК), левый рейл разделов, нижний статус-бар (сервер по `/api/health`, канал событий, инференс из `/api/meta` и WS `backend.status`, демо-данные, время сервера из WS `hello`, версия контракта). Рабочая область `.shell-main` занимает остаток экрана и прокручивается сама; диспетчерская помещается в один экран.
