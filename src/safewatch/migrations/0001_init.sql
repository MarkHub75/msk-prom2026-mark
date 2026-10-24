CREATE TABLE sectors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_demo INTEGER NOT NULL DEFAULT 0,          -- пишет: seed.seed_demo
    created_at TEXT NOT NULL
);

CREATE TABLE cameras (
    id INTEGER PRIMARY KEY,
    sector_id INTEGER NOT NULL REFERENCES sectors(id),
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    is_demo INTEGER NOT NULL DEFAULT 0,          -- пишет: seed.seed_demo
    created_at TEXT NOT NULL,
    deleted_at TEXT                              -- пишет: services.camera_delete; события ссылаются на удалённую камеру
);

CREATE TABLE videos (
    id INTEGER PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    filename TEXT NOT NULL,                      -- исходное имя файла
    sha256 TEXT NOT NULL,
    path TEXT NOT NULL,                          -- от data_dir: uploads/<sha256><ext>
    size_bytes INTEGER NOT NULL,
    width INTEGER NOT NULL,                      -- пишет: media.probe_video через services.video_upload
    height INTEGER NOT NULL,
    fps REAL NOT NULL,
    frame_count INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL,
    codec TEXT NOT NULL,                         -- FourCC в нижнем регистре
    browser_playable INTEGER NOT NULL,           -- codec из media.BROWSER_CODECS
    status TEXT NOT NULL CHECK (status IN ('uploaded', 'processing', 'ready', 'failed')),
    active_analysis_id INTEGER REFERENCES analyses(id),  -- пишет: services.run_next_job, последняя версия анализа
    created_at TEXT NOT NULL,
    UNIQUE (camera_id, sha256)
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('process', 'recompute')),
    video_id INTEGER NOT NULL REFERENCES videos(id),
    backend TEXT NOT NULL CHECK (backend IN ('linq', 'local')),
    fake INTEGER NOT NULL,                       -- Settings.fake на момент постановки
    status TEXT NOT NULL CHECK (status IN ('queued', 'running', 'retry_wait', 'done', 'failed')),
    stage TEXT NOT NULL CHECK (stage IN ('queued', 'inference_detect', 'inference_pose', 'analysis', 'evidence', 'done')),
    progress REAL NOT NULL DEFAULT 0,            -- 0..1 по всем стадиям (раздел 8.1)
    attempts INTEGER NOT NULL DEFAULT 0,
    next_attempt_at TEXT,                        -- пишет: services.run_next_job при retry_wait
    error_code TEXT,                             -- JobErrorCode
    error_text TEXT,                             -- до 500 символов, без секретов
    det_artifact_id INTEGER REFERENCES artifacts(id),   -- пишет: services.run_next_job
    pose_artifact_id INTEGER REFERENCES artifacts(id),  -- пишет: services.run_next_job; NULL, если pose выключен или упал
    analysis_id INTEGER REFERENCES analyses(id),        -- пишет: services.run_next_job (с слайса 4)
    analysis_ms INTEGER,                         -- пишет: services.run_next_job, время стадии анализа
    created_at TEXT NOT NULL,
    started_at TEXT,
    finished_at TEXT
);

CREATE TABLE artifacts (
    id INTEGER PRIMARY KEY,
    cache_key TEXT NOT NULL UNIQUE,              -- inference.artifacts.cache_key(...)
    video_sha256 TEXT NOT NULL,
    model_id TEXT NOT NULL,
    model_version TEXT NOT NULL,
    task TEXT NOT NULL CHECK (task IN ('detect', 'pose')),
    input_size INTEGER NOT NULL,
    step INTEGER NOT NULL,
    backend TEXT NOT NULL CHECK (backend IN ('linq', 'local')),
    fake INTEGER NOT NULL,                       -- 1: детекции синтетические (FakeRemoteShell)
    path TEXT NOT NULL,                          -- artifacts/<cache_key>.jsonl
    frames INTEGER NOT NULL,
    metrics_json TEXT NOT NULL,                  -- InferenceMetrics без поля cached
    created_at TEXT NOT NULL
);

CREATE TABLE analyses (
    id INTEGER PRIMARY KEY,
    video_id INTEGER NOT NULL REFERENCES videos(id),
    version INTEGER NOT NULL,
    det_artifact_id INTEGER NOT NULL REFERENCES artifacts(id),
    pose_artifact_id INTEGER REFERENCES artifacts(id),
    config_json TEXT NOT NULL,                   -- AnalysisConfig: снимок калибровки, зон и правил на момент анализа
    hud_path TEXT NOT NULL,                      -- analyses/<video_id>-v<version>/hud.jsonl
    gaps_json TEXT NOT NULL,                     -- list[ObservabilityGap]
    duration_ms INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE (video_id, version)
);

CREATE TABLE episodes (
    id INTEGER PRIMARY KEY,
    analysis_id INTEGER NOT NULL REFERENCES analyses(id),
    scenario TEXT NOT NULL,
    subject TEXT NOT NULL,                       -- "track:12" | "pair:12-7" | "zone:12-3" | "fire"
    zone_id INTEGER REFERENCES zones(id),
    level_initial TEXT NOT NULL CHECK (level_initial IN ('yellow', 'red')),
    level_max TEXT NOT NULL CHECK (level_max IN ('yellow', 'red')),
    start_ms INTEGER NOT NULL,                   -- первое позитивное наблюдение
    confirm_ms INTEGER NOT NULL,                 -- подтверждение: момент публикации в эфире
    escalate_ms INTEGER,                         -- жёлтое → красное внутри эпизода
    end_ms INTEGER NOT NULL,
    end_reason TEXT NOT NULL CHECK (end_reason IN ('observed_exit', 'track_lost_timeout', 'video_end')),
    reason_code TEXT NOT NULL,
    reason_text TEXT NOT NULL,                   -- короткий нейтральный текст причины, texts.py
    method TEXT NOT NULL,                        -- "pose" | "bbox" | "calibrated" | "relative" | "zone" | "model"
    confidence REAL NOT NULL,
    metrics_json TEXT NOT NULL,                  -- dict[str, float]: пики признаков за эпизод
    uncertain_ms INTEGER NOT NULL DEFAULT 0      -- сумма интервалов U внутри эпизода
);

CREATE TABLE evidence (
    id INTEGER PRIMARY KEY,
    episode_id INTEGER NOT NULL REFERENCES episodes(id),
    kind TEXT NOT NULL CHECK (kind IN ('confirm', 'escalate')),
    frame_idx INTEGER NOT NULL,
    ts_ms INTEGER NOT NULL,
    path TEXT NOT NULL,                          -- evidence/<episode_id>-<kind>.jpg
    sha256 TEXT NOT NULL,                        -- sha256 JPEG-файла
    objects_json TEXT NOT NULL,                  -- list[HudObject] этого кадра
    UNIQUE (episode_id, kind)
);

CREATE TABLE broadcasts (
    id INTEGER PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    video_id INTEGER NOT NULL REFERENCES videos(id),
    analysis_id INTEGER NOT NULL REFERENCES analyses(id),
    started_at TEXT NOT NULL,                    -- стеночное время позиции 0 цикла 0
    loop INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('playing', 'stopped', 'ended')),
    cycle INTEGER NOT NULL DEFAULT 0,            -- пишет: services.broadcast_tick
    position_ms INTEGER NOT NULL DEFAULT 0,      -- пишет: services.broadcast_tick, последняя обработанная позиция
    stopped_at TEXT                              -- пишет: services.broadcast_stop, broadcast_start, video_recompute, camera_delete
);
CREATE UNIQUE INDEX broadcasts_one_playing ON broadcasts (camera_id) WHERE status = 'playing';

CREATE TABLE zones (
    id INTEGER PRIMARY KEY,
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    kind TEXT NOT NULL,                          -- id из zone_kinds в config/default.yaml
    name TEXT NOT NULL,
    points_json TEXT NOT NULL,                   -- [[x, y]] нормированные 0..1; polygon 3..32 точек, line ровно 2
    created_at TEXT NOT NULL,
    deleted_at TEXT                              -- пишет: services.zone_delete
);

CREATE TABLE calibrations (
    camera_id INTEGER PRIMARY KEY REFERENCES cameras(id),
    image_points_json TEXT NOT NULL,             -- [[u, v]] нормированные 0..1, 4..8 точек
    world_points_json TEXT NOT NULL,             -- [[x, y]] метры на полу
    control_json TEXT NOT NULL,                  -- list[ControlPoint], 0..8
    homography_json TEXT NOT NULL,               -- 3×3: нормированное изображение → пол в метрах
    fit_rmse_m REAL NOT NULL,
    control_rmse_m REAL,                         -- NULL: контрольных точек нет
    updated_at TEXT NOT NULL
);

CREATE TABLE camera_rules (
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    scenario TEXT NOT NULL,
    enabled INTEGER NOT NULL,
    params_json TEXT NOT NULL,                   -- переопределения параметров сценария, dict[str, float]
    updated_at TEXT NOT NULL,
    PRIMARY KEY (camera_id, scenario)
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    pub_key TEXT NOT NULL UNIQUE,                -- "b<broadcast>:c<cycle>:e<episode>" | "demo:<n>"
    episode_id INTEGER REFERENCES episodes(id),  -- NULL у демо-событий
    broadcast_id INTEGER REFERENCES broadcasts(id),  -- NULL у демо-событий
    cycle INTEGER NOT NULL DEFAULT 0,
    video_id INTEGER REFERENCES videos(id),
    camera_id INTEGER NOT NULL REFERENCES cameras(id),
    sector_id INTEGER NOT NULL REFERENCES sectors(id),  -- сектор камеры на момент публикации
    zone_id INTEGER REFERENCES zones(id),
    scenario TEXT NOT NULL,
    title TEXT NOT NULL,                         -- название сценария на момент публикации
    reason_text TEXT NOT NULL,
    level TEXT NOT NULL CHECK (level IN ('yellow', 'red')),
    status TEXT NOT NULL CHECK (status IN ('new', 'viewed', 'confirmed', 'false_alarm', 'sent_to_master',
                                            'master_accepted', 'resolved', 'auto_finished', 'superseded')),
    operator_verdict TEXT NOT NULL DEFAULT 'none' CHECK (operator_verdict IN ('none', 'confirmed', 'false_alarm')),
    escalated_by_timeout INTEGER NOT NULL DEFAULT 0,
    started_at TEXT NOT NULL,                    -- стеночное время начала эпизода
    published_at TEXT NOT NULL,
    red_at TEXT,                                 -- пишет: services.broadcast_tick (публикация красным или эскалация)
    ended_at TEXT,                               -- пишет: services.broadcast_tick (конец эпизода в эфире)
    video_start_ms INTEGER,
    video_end_ms INTEGER,
    is_demo INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX events_published ON events (published_at);
CREATE INDEX events_status ON events (status);
CREATE INDEX events_camera ON events (camera_id);

CREATE TABLE event_actions (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    at TEXT NOT NULL,
    actor_role TEXT NOT NULL CHECK (actor_role IN ('operator', 'master', 'ohs', 'management', 'admin', 'system')),
    actor_name TEXT NOT NULL,                    -- заголовок X-Actor или texts.DEMO_ACTOR[role]; "система"
    action TEXT NOT NULL,                        -- LogAction
    from_status TEXT,
    to_status TEXT,
    comment TEXT NOT NULL DEFAULT ''
);
CREATE INDEX event_actions_event ON event_actions (event_id);
CREATE TRIGGER event_actions_no_update BEFORE UPDATE ON event_actions
BEGIN SELECT RAISE(ABORT, 'event_actions is append-only'); END;
CREATE TRIGGER event_actions_no_delete BEFORE DELETE ON event_actions
BEGIN SELECT RAISE(ABORT, 'event_actions is append-only'); END;

CREATE TABLE deliveries (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    channel TEXT NOT NULL,                       -- "webhook:<name>"
    kind TEXT NOT NULL CHECK (kind IN ('published', 'escalated', 'to_master')),
    status TEXT NOT NULL CHECK (status IN ('sent', 'failed')),
    http_status INTEGER,
    error TEXT NOT NULL DEFAULT '',
    at TEXT NOT NULL,
    UNIQUE (event_id, channel, kind)
);
