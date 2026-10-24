"""Slice 12: CSV export of the journal (tech.md 2 «Допущения», 16)."""

import csv
import io

import httpx
import pytest
from test_jobs import _tune
from test_journal import world

from safewatch import store
from safewatch.config import Settings

COLUMNS = [
    "id", "опубликовано (МСК)", "начало", "сектор", "камера", "зона", "сценарий", "уровень",
    "статус", "вердикт", "эскалация по таймауту", "причина", "длительность (с)", "демо",
    "sha256 кадра", "история", "ФИО", "Должность", "Бригада",
]  # fmt: skip


def rows(body: bytes) -> list[list[str]]:
    return list(csv.reader(io.StringIO(body.decode("utf-8-sig")), delimiter=";"))


async def test_csv_columns_and_history(
    client: httpx.AsyncClient, core: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    w = world()
    fall = w["fall"]
    with store.tx():
        for at, role, action, comment in [
            ("2026-10-24T09:00:05.000Z", "operator", "confirmed", ""),
            ("2026-10-24T09:03:00.000Z", "master", "resolved", "Помог подняться"),
        ]:
            store.insert("event_actions", {
                "event_id": fall, "at": at, "actor_role": role, "actor_name": "Иван",
                "action": action, "comment": comment,
            })  # fmt: skip
        store.event_update(
            fall, {"operator_verdict": "confirmed", "ended_at": "2026-10-24T09:00:12.500Z"}
        )
    r = await client.get("/api/events/export.csv", params={"camera_id": w["north"]})
    assert r.status_code == 200
    assert r.headers["content-type"] == "text/csv; charset=utf-8"
    assert r.content.startswith(b"\xef\xbb\xbf")
    table = rows(r.content)
    assert table[0] == COLUMNS
    assert sorted(int(row[0]) for row in table[1:]) == sorted(
        [w["run"], w["fall"], w["demo"], w["odd"]]
    )
    (row,) = [row for row in table[1:] if row[0] == str(fall)]
    record = dict(zip(COLUMNS, row, strict=True))
    assert record["начало"] == "2026-10-24 12:00:00"  # 09:00 UTC in Moscow
    assert record["сектор"] == "Сектор 1 · Цех" and record["зона"] == "Проход"
    assert record["уровень"] == "Красная опасность" and record["статус"] == "Решено"
    assert record["вердикт"] == "подтверждено" and record["эскалация по таймауту"] == "нет"
    assert record["длительность (с)"] == "12,5" and record["демо"] == "нет"
    assert record["история"] == (
        "2026-10-24 11:00:00 система: опубликовано; "
        "2026-10-24 12:00:05 Оператор: подтверждено; "
        "2026-10-24 12:03:00 Мастер смены: решено (Помог подняться)"
    )
    _tune(monkeypatch, core, journal={"export_max_rows": 2})
    r = await client.get("/api/events/export.csv")
    assert len(rows(r.content)) == 1 + 2


async def test_csv_has_identity_columns(client: httpx.AsyncClient) -> None:
    w = world()
    body = {"person_name": "Сидоров Пётр", "person_position": "стропальщик", "crew": "3"}
    r = await client.patch(
        f"/api/events/{w['fall']}/identity", json=body, headers={"X-Role": "ohs"}
    )
    assert r.status_code == 200, r.text
    r = await client.get("/api/events/export.csv", params={"camera_id": w["north"]})
    table = rows(r.content)
    assert table[0][-3:] == ["ФИО", "Должность", "Бригада"]
    found = {row[0]: row for row in table[1:]}
    assert found[str(w["fall"])][-3:] == ["Сидоров Пётр", "стропальщик", "3"]
    assert found[str(w["run"])][-3:] == ["", "", ""]
    assert found[str(w["fall"])][-4].endswith(
        "идентификация (ФИО: Сидоров Пётр; должность: стропальщик; бригада: 3)"
    )
