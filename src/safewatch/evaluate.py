"""Quality evaluation (tech.md 8.18): episodes against hand labels, pure logic."""

from typing import Literal

from safewatch import texts
from safewatch.types import EpisodeDraft, EvalReport, ExpectedEvent

OutcomeKind = Literal["tp", "fn", "fp", "duplicate", "late"]
Outcome = tuple[str, OutcomeKind, float | None]  # scenario, kind, delay_s of a tp


def _ms(seconds: float) -> int:
    # Episode times are integer ms: comparing in ms keeps `delay == deadline_s` exact.
    return round(seconds * 1000)


def match_episodes(
    expected: list[ExpectedEvent], episodes: list[EpisodeDraft], deadline_s: float
) -> list[Outcome]:
    """One video: a tp per matched pair, an fn per lone label, a kind per unmatched episode."""
    deadline = _ms(deadline_s)
    inside: list[list[int]] = [[] for _ in episodes]  # labels holding the confirm moment
    pairs: list[tuple[int, int, int]] = []  # (delay_ms, episode, label)
    for i, ep in enumerate(episodes):
        for j, label in enumerate(expected):
            start = _ms(label.start_s)
            if ep.scenario == label.scenario and start <= ep.confirm_ms < _ms(label.end_s):
                inside[i].append(j)
                if ep.confirm_ms - start <= deadline:
                    pairs.append((ep.confirm_ms - start, i, j))
    out: list[Outcome] = []
    matched_episodes: set[int] = set()
    matched_labels: set[int] = set()
    for delay, i, j in sorted(pairs):  # greedy by the smallest delay
        if i not in matched_episodes and j not in matched_labels:
            matched_episodes.add(i)
            matched_labels.add(j)
            out.append((expected[j].scenario, "tp", delay / 1000))
    for i, ep in enumerate(episodes):
        if i in matched_episodes:
            continue
        kind: OutcomeKind = "fp"
        if any(j in matched_labels for j in inside[i]):
            kind = "duplicate"
        elif inside[i]:
            kind = "late"
        out.append((ep.scenario, kind, None))
    out += [(e.scenario, "fn", None) for j, e in enumerate(expected) if j not in matched_labels]
    return out


def _number(x: float | None) -> str:
    return "—" if x is None else f"{x:.3f}"


def report_md(report: EvalReport) -> str:
    lines = [
        texts.EVAL_TITLE.format(labels=report.labels, hours=_number(report.hours)),
        "",
        "| " + " | ".join(texts.EVAL_COLUMNS) + " |",
        "|" + " --- |" * len(texts.EVAL_COLUMNS),
    ]
    for r in report.rows:
        cells = [r.scenario, r.expected, r.episodes, r.tp, r.fn, r.fp, r.duplicates, r.late]
        cells += [_number(x) for x in (r.precision, r.recall, r.f1, r.fp_per_hour)]
        cells += [_number(r.delay_s.p50), _number(r.delay_s.p95), r.delay_s.n]
        lines.append("| " + " | ".join(str(c) for c in cells) + " |")
    lines += ["", texts.EVAL_FOOTNOTE.format(deadline=report.deadline_s)]
    return "\n".join(lines) + "\n"
