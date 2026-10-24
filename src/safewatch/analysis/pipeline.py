"""analyze() (tech.md 8.2): detections → tracks → features → observations → episodes, HUD."""

import itertools
from collections.abc import Callable
from pathlib import Path

from safewatch import config as app_config
from safewatch import rules
from safewatch.analysis import features, geometry, hud
from safewatch.analysis.episodes import EpisodeManager
from safewatch.analysis.tracking import Tracker
from safewatch.types import (
    AnalysisConfig,
    AnalysisResult,
    Detection,
    FrameContext,
    FrameDetections,
    HudFrame,
    ModelSpec,
    ObjectState,
    Observation,
    Point,
    ScenarioPlugin,
)

VEHICLES = ("car", "bus", "truck", "train")


def _plugins(config: AnalysisConfig) -> list[tuple[ScenarioPlugin, dict[str, float]]]:
    """Active scenarios the camera keeps on, with defaults + camera overrides (tech.md 8.3)."""
    out = []
    for meta in rules.scenario_metas(config.active_classes):
        rule = config.rules.get(meta.id)
        if meta.status != "active" or (rule is not None and not rule.enabled):
            continue
        params = rules.defaults(meta.id) | (
            rule.effective | rule.params if rule is not None else {}
        )
        out.append((rules.plugin(meta.id), params))
    return out


def _ground(config: AnalysisConfig) -> Callable[[Point], Point | None] | None:
    """Pixel point → floor meters, only inside the hull of the calibration points (8.11)."""
    cal = config.calibration
    h = None if cal is None else geometry.homography(cal.image_points, cal.world_points)
    if cal is None or h is None:
        return None
    hull = cal.image_points

    def to_floor(p: Point) -> Point | None:
        q = (p[0] / config.width, p[1] / config.height)
        return geometry.apply_h(h, q) if geometry.hull_contains(hull, q) else None

    return to_floor


def analyze(
    det: list[FrameDetections],
    pose: list[FrameDetections] | None,
    video_path: Path,  # read from slice 11 on (sample_luma)
    config: AnalysisConfig,
    pose_model: ModelSpec | None,
    det_model: ModelSpec,
    extra: list[tuple[ModelSpec, list[FrameDetections]]] | None = None,
) -> AnalysisResult:
    """`extra`: frames of the `pipeline.extra` models, their classes become untracked objects."""
    settings = app_config.get_settings()
    ids = itertools.count(1)
    people, machines = Tracker(settings.tracker, ids), Tracker(settings.tracker, ids)
    poses = {f.frame_idx: f.detections for f in pose or []}
    extras = [(m, {f.frame_idx: f.detections for f in frames}) for m, frames in extra or []]
    pose_names = pose_model.classes if pose_model is not None else {}
    history: features.History = {}
    vehicle_history: features.VehicleHistory = {}
    # The HUD speed tag follows the camera's running rule, not the config defaults.
    rule = config.rules.get("running")
    hud_running = rules.defaults("running") | (
        rule.effective | rule.params if rule is not None else {}
    )
    ground = _ground(config)
    plugins = _plugins(config)
    episodes = EpisodeManager(settings.episodes)
    frames: list[HudFrame] = []
    for frame in det:
        ts = round(frame.ts_ms)
        persons: list[Detection] = []
        vehicles: list[Detection] = []
        objects: list[ObjectState] = []
        for d in frame.detections:
            name = det_model.classes.get(d.cls)
            if name is None:
                continue
            if name == "person":
                if d.score >= settings.tracker.low_thresh:
                    persons.append(d)
            elif d.score >= config.class_conf.get(name, det_model.conf):
                if name in VEHICLES:
                    vehicles.append(d.model_copy(update={"name": name}))
                else:
                    objects.append(ObjectState(name=name, bbox=d.bbox_xyxy, score=d.score))
        for model, by_frame in extras:
            for d in by_frame.get(frame.frame_idx, []):
                name = model.classes.get(d.cls)
                if name is not None and d.score >= config.class_conf.get(name, model.conf):
                    objects.append(ObjectState(name=name, bbox=d.bbox_xyxy, score=d.score))
        tracked = people.update(ts, persons)
        frame_poses = [
            p for p in poses.get(frame.frame_idx, []) if pose_names.get(p.cls) == "person"
        ]
        by_index = features.attach_keypoints(
            [d.bbox_xyxy for _, d in tracked], frame_poses, settings.pose.match_iou
        )
        kpts = {tracked[i][0]: points for i, points in by_index.items()}
        ctx = FrameContext(
            frame_idx=frame.frame_idx,
            ts_ms=ts,
            width=config.width,
            height=config.height,
            persons=features.person_states(
                tracked,
                kpts,
                ts,
                config.height,
                history,
                settings.features,
                settings.pose.kpt_conf,
                ground,
            ),
            vehicles=features.vehicle_states(
                machines.update(ts, vehicles), ts, vehicle_history, settings.features, ground
            ),
            objects=objects,
            zones=config.zones,
            calibrated=config.calibration is not None,
        )
        observations: list[Observation] = []
        for plugin, params in plugins:
            observations += plugin.observe(ctx, params)
        episodes.update(frame.frame_idx, ts, observations)
        frames.append(hud.build_hud(ctx, hud_running, settings.features, observations))
    return AnalysisResult(
        hud=frames,
        episodes=episodes.finish(config.duration_ms),
        gaps=[],
        pose_used=pose is not None,
    )
