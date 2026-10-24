"""Slice 4: HUD frames of tech.md 8.2 item 8."""

from typing import Any

from safewatch.analysis.hud import build_hud
from safewatch.config import get_settings
from safewatch.types import FrameContext, ObjectState, PersonState, VehicleState

W, H = 640, 480
TS = 20_000


def _person(**over: Any) -> PersonState:
    base: dict[str, Any] = {
        "track_id": 1,
        "bbox": (-5.0, 100.0, 60.0, 500.0),  # sticks out of the frame on the left and bottom
        "score": 0.9,
        "foot": (27.5, 500.0),
        "anchor": (27.5, 500.0),
        "feet_visible": True,
        "ground": None,
        "height_px": 100.0,
        "ref_height_px": 100.0,
        "speed_bh_s": None,
        "speed_m_s": None,
        "posture": "upright",
        "posture_method": "bbox",
        "torso_deg": None,
        "last_upright_ms": TS,
        "lying_since_ms": None,
        "still_since_ms": TS,
        "prev_anchor": None,
        "prev_ts_ms": None,
        "kpts": [(700.0, 240.0, 0.9)] * 17,
    }
    return PersonState(**(base | over))


def _tags(p: PersonState) -> list[tuple[str, str, str | None]]:
    ctx = FrameContext(
        frame_idx=0, ts_ms=TS, width=W, height=H, persons=[p], vehicles=[], objects=[],
        zones=[], calibrated=False,
    )  # fmt: skip
    obj = build_hud(ctx, 1.5, get_settings().features, []).objects[0]
    return [(t.code, t.text, t.level) for t in obj.tags]


def test_tags_texts_russian_format() -> None:
    assert _tags(_person(speed_bh_s=2.44)) == [("speed", "бег 2,4 роста/с", "yellow")]
    assert _tags(_person(speed_bh_s=1.5)) == [("speed", "бег 1,5 роста/с", "yellow")]
    assert _tags(_person(speed_bh_s=1.0)) == [("speed", "1,0 роста/с", None)]
    lying = _person(posture="lying", lying_since_ms=TS - 12_400, still_since_ms=TS - 3000)
    assert _tags(lying) == [("lying", "лежит 12 с", None)]  # still exactly 3 s: not yet
    still = _person(still_since_ms=TS - 4100)
    assert _tags(still) == [("still", "неподвижен 4 с", None)]
    assert _tags(_person(feet_visible=False)) == [("feet_hidden", "ноги не видны", None)]
    assert _tags(_person(height_px=39.0)) == [("too_small", "слишком мелко", None)]
    assert _tags(_person(height_px=40.0)) == []

    ctx = FrameContext(
        frame_idx=4, ts_ms=TS, width=W, height=H, persons=[_person()],
        vehicles=[
            VehicleState(
                track_id=2, name="truck", bbox=(300.0, 0.0, 700.0, 480.0), score=0.8,
                footprint=None, height_px=480.0, speed_vh_s=None, speed_m_s=None,
            )
        ],
        objects=[ObjectState(name="cell phone", bbox=(10.0, 150.0, 20.0, 170.0), score=0.5)],
        zones=[], calibrated=False,
    )  # fmt: skip
    frame = build_hud(ctx, 1.5, get_settings().features, [])
    assert [(o.kind, o.label, o.track_id) for o in frame.objects] == [
        ("person", "человек", 1),
        ("vehicle", "грузовик", 2),
        ("phone", "телефон", None),
    ]
    for obj in frame.objects:
        assert all(0.0 <= v <= 1.0 for v in obj.bbox)
        assert all(0.0 <= v <= 1.0 for x, y, _ in obj.kpts or [] for v in (x, y))
    assert frame.objects[0].bbox == (0.0, 100 / H, 60 / W, 1.0)
