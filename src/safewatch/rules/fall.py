"""Scenario `fall` (tech.md 8.3): a fall seen as upright → lying, or lying still too long."""

from safewatch import config as app_config
from safewatch import texts
from safewatch.rules.base import obs, param, why_common, zones_at
from safewatch.types import EpisodeDraft, FrameContext, Observation, ScenarioMeta, WhyItem

ID = "fall"


class FallPlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="fall",
        default_level="red",
        status="active",
        status_text="",
        required_classes=["person"],
        zone_kinds=["lying_allowed"],
        params=[
            param("transition_s", 0.0, 10.0),
            param("confirm_s", 0.0, 60.0),
            param("still_s", 0.0, 600.0),
            param("allowed_still_s", 0.0, 3600.0),
        ],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        min_px = app_config.get_settings().features.min_person_px
        out = []
        for p in ctx.persons:
            method = p.posture_method
            # A lying bbox is short by nature: the size of the person is H_ref.
            if p.posture == "unknown" or p.ref_height_px < min_px:
                out.append(obs(ID, p, "U", level="red", method=method))
                continue
            if p.posture == "upright" or p.lying_since_ms is None:
                out.append(obs(ID, p, "N", level="red", method=method))
                continue
            still_ms = ctx.ts_ms - (p.still_since_ms if p.still_since_ms is not None else ctx.ts_ms)
            still = {"still_s": still_ms / 1000}
            text = texts.LYING_STILL.format(n=still_ms // 1000)
            zones = zones_at(ctx, p.anchor, ("lying_allowed",))
            if zones:
                if still_ms >= params["allowed_still_s"] * 1000:
                    out.append(
                        obs(
                            ID,
                            p,
                            "P",
                            level="red",
                            reason_code="lying_still_allowed",
                            reason_text=text + texts.IN_REPAIR_ZONE,
                            method=method,
                            metrics=still,
                            zone_id=zones[0].id,
                        )  # fmt: skip
                    )
                else:
                    out.append(obs(ID, p, "N", level="red", method=method))
                continue
            up = p.last_upright_ms
            if up is not None and p.lying_since_ms - up <= params["transition_s"] * 1000:
                transition = {"transition_s": (p.lying_since_ms - up) / 1000}
                out.append(
                    obs(
                        ID,
                        p,
                        "P",
                        level="red",
                        hold_s=params["confirm_s"],
                        reason_code="fall",
                        reason_text=texts.FALL_SEEN,
                        method=method,
                        metrics=transition,
                    )  # fmt: skip
                )
            elif still_ms >= params["still_s"] * 1000:
                out.append(
                    obs(
                        ID,
                        p,
                        "P",
                        level="red",
                        reason_code="lying_still",
                        reason_text=text,
                        method=method,
                        metrics=still,
                    )  # fmt: skip
                )
            else:
                out.append(obs(ID, p, "N", level="red", method=method))
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        if episode.reason_code == "fall":
            t, s = texts.fmt_num(params["transition_s"]), texts.fmt_num(params["confirm_s"])
            rule = texts.WHY_FALL.format(t=t, s=s)
        else:
            key = "allowed_still_s" if episode.zone_id is not None else "still_s"
            rule = texts.WHY_LYING.format(s=texts.fmt_num(params[key]))
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
