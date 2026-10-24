"""analyze() (tech.md 8.2): detections → tracks → features → HUD; episodes come in slice 5."""

import itertools
from pathlib import Path

from safewatch import config as app_config
from safewatch.analysis import features, hud
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
    VehicleState,
)

VEHICLES = ("car", "bus", "truck", "train")


def analyze(
    det: list[FrameDetections],
    pose: list[FrameDetections] | None,
    video_path: Path,  # read from slice 11 on (sample_luma)
    config: AnalysisConfig,
    pose_model: ModelSpec | None,
    det_model: ModelSpec,
) -> AnalysisResult:
    settings = app_config.get_settings()
    ids = itertools.count(1)
    people, machines = Tracker(settings.tracker, ids), Tracker(settings.tracker, ids)
    poses = {f.frame_idx: f.detections for f in pose or []}
    pose_names = pose_model.classes if pose_model is not None else {}
    history: features.History = {}
    run_bh_s = settings.scenarios.running["speed_bh_s"]
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
                tracked, kpts, ts, config.height, history, settings.features, settings.pose.kpt_conf
            ),
            vehicles=[
                VehicleState(
                    track_id=track_id,
                    name=d.name,
                    bbox=d.bbox_xyxy,
                    score=d.score,
                    footprint=None,  # slice 9: calibration
                    height_px=d.bbox_xyxy[3] - d.bbox_xyxy[1],
                    speed_vh_s=None,  # slice 10: features.vehicle_states
                    speed_m_s=None,
                )
                for track_id, d in machines.update(ts, vehicles)
            ],
            objects=objects,
            zones=config.zones,
            calibrated=config.calibration is not None,
        )
        frames.append(hud.build_hud(ctx, run_bh_s, settings.features))
    return AnalysisResult(hud=frames, episodes=[], gaps=[], pose_used=pose is not None)
