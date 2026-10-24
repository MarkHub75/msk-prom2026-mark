-- v5 (tech.md 6.11.1): additive only, rows of 0001 keep working.
ALTER TABLE videos ADD COLUMN web_path TEXT;           -- пишет: services.video_upload, video_import (S18); uploads/<sha256>.web.mp4, NULL — исходник играет в браузере
ALTER TABLE analyses ADD COLUMN autocal_json TEXT;     -- пишет: services.run_next_job (S19); AutoCalibration или NULL (анализ до v5)
ALTER TABLE events ADD COLUMN person_name TEXT NOT NULL DEFAULT '';      -- пишет: services.event_identify (S26)
ALTER TABLE events ADD COLUMN person_position TEXT NOT NULL DEFAULT '';  -- пишет: services.event_identify (S26)
ALTER TABLE events ADD COLUMN crew TEXT NOT NULL DEFAULT '';             -- пишет: services.event_identify (S26)
ALTER TABLE deliveries ADD COLUMN delivered_at TEXT;   -- пишет: services.deliveries_flush (S23), канал call

CREATE TABLE delivery_queue (                          -- пишет: services.broadcast_tick, event_action, escalation_tick; читает и чистит deliveries_flush (S23)
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id),
    kind TEXT NOT NULL CHECK (kind IN ('published', 'escalated', 'to_master')),
    level TEXT NOT NULL CHECK (level IN ('yellow', 'red')),  -- уровень на момент постановки
    created_at TEXT NOT NULL,
    UNIQUE (event_id, kind)
);

CREATE TABLE dataset_items (                           -- пишет: services.datasets_flush (S25)
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL UNIQUE REFERENCES events(id),
    scenario TEXT NOT NULL,
    label TEXT NOT NULL CHECK (label IN ('false_alarm')),
    path TEXT NOT NULL,                                -- datasets/false_alarms/<event_id>/ от data_dir
    frames INTEGER NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE demo_packs (                              -- пишет: services.demo_import (S17)
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL,                              -- sha256 файла manifest.json
    backend TEXT NOT NULL CHECK (backend IN ('linq', 'local')),  -- бэкенд артефактов пакета
    fake INTEGER NOT NULL,                             -- 1: хоть один артефакт синтетический
    cameras INTEGER NOT NULL,
    videos INTEGER NOT NULL,
    imported_at TEXT NOT NULL
);
