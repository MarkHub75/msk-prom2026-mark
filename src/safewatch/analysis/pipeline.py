"""analyze() (tech.md 8.2): detections → tracks → features → observations → episodes, HUD."""

import itertools
from collections.abc import Callable
from pathlib import Path

from safewatch import config as app_config
from safewatch import media, rules
from safewatch.analysis import autocal, features, geometry, hud, observability
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
    video_path: Path,  # only for sample_luma
    config: AnalysisConfig,
    pose_model: ModelSpec | None,
    det_model: ModelSpec,
    extra: list[tuple[ModelSpec, list[FrameDetections]]] | None = None,
) -> AnalysisResult:
    """`extra`: frames of the `pipeline.extra` models; their classes become untracked objects,
    a class of `pipeline.vehicle_classes` becomes tracked machinery (tech.md 8.30 item 3)."""
    settings = app_config.get_settings()
    vehicle_names = set(settings.pipeline.vehicle_classes)
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
    # Fitted anew on every analysis and recompute; the manual calibration wins (tech.md 8.21).
    person_cls = {cls for cls, name in det_model.classes.items() if name == "person"}
    cal = autocal.fit(
        det, person_cls, config.width, config.height, settings.autocal,
        settings.features.upright_hw, settings.tracker.high_thresh,
    )  # fmt: skip
    plugins = _plugins(config)
    episodes = EpisodeManager(settings.episodes)
    frames: list[HudFrame] = []
    obs = settings.observability
    luma = media.sample_luma(video_path, obs.sample_s)
    gaps = observability.find_gaps([round(f.ts_ms) for f in det], luma, config.duration_ms, obs)
    # A stale gap has no frames: the episode manager counts its time as unseen by itself.
    blind = [g for g in gaps if g.reason != "stale"]
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
                if name in vehicle_names:
                    vehicles.append(d.model_copy(update={"name": name}))
                else:
                    objects.append(ObjectState(name=name, bbox=d.bbox_xyxy, score=d.score))
        for model, by_frame in extras:
            for d in by_frame.get(frame.frame_idx, []):
                name = model.classes.get(d.cls)
                if name is None or d.score < config.class_conf.get(name, model.conf):
                    continue
                if name in vehicle_names:
                    vehicles.append(d.model_copy(update={"name": name}))
                else:
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
                cal,
            ),
            vehicles=features.vehicle_states(
                machines.update(ts, vehicles), ts, vehicle_history, settings.features, ground, cal
            ),
            objects=objects,
            zones=config.zones,
            calibrated=config.calibration is not None,
            auto_calibration=cal,
        )
        observations: list[Observation] = []
        for plugin, params in plugins:
            observations += plugin.observe(ctx, params)
        if any(g.start_ms <= ts < g.end_ms for g in blind):
            observations = []  # a dark or covered frame says nothing: U for every subject
        episodes.update(frame.frame_idx, ts, observations)
        frames.append(hud.build_hud(ctx, hud_running, settings.features, observations))
    return AnalysisResult(
        hud=frames,
        episodes=episodes.finish(config.duration_ms),
        gaps=gaps,
        pose_used=pose is not None,
        auto_calibration=cal,
    )
