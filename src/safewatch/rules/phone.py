"""Scenario `phone` (tech.md 8.3): a phone held by a person; red in a danger zone."""

from safewatch import texts
from safewatch.rules.base import attach_objects, obs, param, why_common, zones_at
from safewatch.types import EpisodeDraft, FrameContext, Observation, ScenarioMeta, WhyItem

ID = "phone"
DANGER_KINDS = ("danger", "vehicle_path")


class PhonePlugin:
    meta = ScenarioMeta(
        id=ID,
        title=texts.SCENARIO_TITLES[ID],
        description=texts.SCENARIO_DESCRIPTIONS[ID],
        icon="phone",
        default_level="yellow",
        status="active",
        status_text="",
        required_classes=["person", "cell phone"],
        zone_kinds=list(DANGER_KINDS),
        params=[
            param("hold_s", 0.0, 60.0),
            param("danger_hold_s", 0.0, 60.0),
            param("min_person_px", 0.0, 2000.0),
            param("upper_frac", 0.0, 1.0),
            param("wrist_dist_bh", 0.0, 5.0),
        ],
    )

    def observe(self, ctx: FrameContext, params: dict[str, float]) -> list[Observation]:
        phones = attach_objects(ctx, "cell phone", params)
        out = []
        for p in ctx.persons:
            if p.height_px < params["min_person_px"]:
                out.append(obs(ID, p, "U", reason_code="too_small"))
                continue
            phone = phones.get(p.track_id)
            if phone == "ambiguous":
                out.append(obs(ID, p, "U", reason_code="owner_ambiguous"))
                continue
            if phone is None:
                out.append(obs(ID, p, "N"))
                continue
            zones = zones_at(ctx, p.anchor, DANGER_KINDS)
            o = obs(
                ID,
                p,
                "P",
                level="red" if zones else "yellow",
                hold_s=params["danger_hold_s" if zones else "hold_s"],
                reason_code="phone_zone" if zones else "phone",
                reason_text=texts.PHONE_HELD,
                metrics={"score": phone.score},
                zone_id=zones[0].id if zones else None,
            )
            out.append(o)
        return out

    def explain(self, episode: EpisodeDraft, params: dict[str, float]) -> list[WhyItem]:
        hold = params["danger_hold_s" if episode.level_initial == "red" else "hold_s"]
        rule = texts.WHY_HOLD.format(rule=texts.SCENARIO_TITLES[ID], s=texts.fmt_num(hold))
        return [WhyItem(label=texts.WHY_RULE, value=rule), *why_common(episode)]
