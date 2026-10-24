"""Slice 6: notification texts and sounds of tech.md 8.8, audience of the WS messages."""

from conftest import FakeClock
from test_broadcast import at, drain, playing, started

from safewatch import services, texts
from safewatch.config import Settings
from safewatch.hub import hub

FALL = {"scenario": "fall", "level_initial": "red", "level_max": "red", "confirm_ms": 6000,
        "reason_code": "lying_still", "reason_text": "Человек лежит неподвижно 15 с"}  # fmt: skip


def test_notification_texts_and_sounds(core: Settings, fake_clock: FakeClock) -> None:
    yellow = texts.notification_text("yellow", "Сектор 5 · Склад", "Бег 2,4 роста/с", False)
    assert yellow == "Жёлтая опасность · Сектор 5 · Бег 2,4 роста/с"
    red = texts.notification_text("red", "Сектор 7 · Ремонт", FALL["reason_text"], False)
    assert red == "Красная опасность · Сектор 7 · Человек лежит неподвижно 15 с"
    late = texts.notification_text("red", "Сектор 7", "Падение", True)
    assert late == "Красная опасность · Сектор 7 · Падение · Не подтверждено оператором"

    b = playing([{}, FALL])
    operator, master = hub.connect("operator"), hub.connect("master")
    at(fake_clock, started(b), 6000)
    services.broadcast_tick()
    notes = [d for k, d in drain(operator) if k == "notification"]
    found = [(n["text"], n["sound"], n["takeover"], n["level"]) for n in notes]
    assert found == [
        ("Жёлтая опасность · Сектор 5 · Бег 2,4 роста/с", "chime", False, "yellow"),
        ("Красная опасность · Сектор 5 · Человек лежит неподвижно 15 с", "siren", True, "red"),
    ]
    assert [k for k, _ in drain(master) if k == "notification"] == []
