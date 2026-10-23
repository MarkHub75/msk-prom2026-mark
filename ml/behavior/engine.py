"""Conservative pose/helmet episode engine with per-camera ownership.

The geometric thresholds are configurable camera policy, not validated universal
fall thresholds. Missing observations never count towards confirmation.
"""
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import hypot, isfinite
from uuid import uuid4

from ml.contracts import validate_observation

DEFAULTS = {
    "confirm_helmet_ms": 2000, "confirm_lying_ms": 3000,
    "confirm_fall_ms": 1000, "transition_ms": 1500,
    "max_gap_ms": 750, "track_exit_ms": 2000,
    "min_score": 0.5, "keypoint_score": 0.5,
    "min_torso_px": 10, "orientation_ratio": 1.3,
    "lying_bbox_ratio": 1.15, "upright_bbox_ratio": 0.85,
    "match_distance": 0.75, "match_ambiguity": 0.08,
    "allow_bbox_head_association": False, "zone_id": None,
    "rule_version": "behavior-v1", "floor_polygon": None,
    "confirm_immobility_ms": 3000, "immobility_min_points": 6,
    "immobility_max_speed": 0.04,
}


def _center(box):
    a,b,c,d = box
    return ((a+c)/2, (b+d)/2)


def _inside(p, box):
    return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]


def _iou(a,b):
    area = max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    union = (a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-area
    return area/union if union else 0


def _polygon_contains(p, poly):
    inside = False
    x,y = p
    for i in range(len(poly)):
        a,b = poly[i-1],poly[i]
        if (a[1]>y) != (b[1]>y) and x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
            inside = not inside
    return inside


@dataclass
class Track:
    id: int
    box: list
    last_seen: float
    candidates: dict = field(default_factory=dict)
    sent: set = field(default_factory=set)
    active: dict = field(default_factory=dict)
    last_upright: float | None = None
    fall_candidate: bool = False
    motion_previous: dict | None = None
    still_since: float | None = None


@dataclass
class Camera:
    epoch: str
    generation: int = 1
    last_time: float | None = None
    last_frame: int | None = None
    next_id: int = 1
    tracks: dict = field(default_factory=dict)


class BehaviorEngine:
    """update(batch)->event mutations; on_gap(gap)->interrupted mutations.

    One ordered writer must own each camera. A local track id is not identity
    across occlusion, exit, reconnect, restart, or ambiguous crossing.
    """
    def __init__(self, config=None):
        self.config = {**DEFAULTS, **(config or {})}
        for k in ("confirm_helmet_ms", "confirm_lying_ms", "confirm_fall_ms", "transition_ms", "max_gap_ms", "track_exit_ms", "confirm_immobility_ms"):
            if self.config[k] < 0:
                raise ValueError(f"{k} must be nonnegative")
        if not 1 <= self.config["immobility_min_points"] <= 12:
            raise ValueError("immobility_min_points must be between 1 and 12")
        if self.config["immobility_max_speed"] < 0:
            raise ValueError("immobility_max_speed must be nonnegative")
        if "retain_upright_during_unknown" in self.config and type(self.config["retain_upright_during_unknown"]) is not bool:
            raise ValueError("retain_upright_during_unknown must be boolean")
        self.cameras = {}

    def _posture(self, person):
        k = person.get("keypoints")
        if not k or len(k) != 17:
            return "unknown"
        indices = (5,6,11,12)
        if any(len(k[i]) != 3 or k[i][2] < self.config["keypoint_score"] for i in indices):
            return "unknown"
        shoulder = tuple((k[5][j]+k[6][j])/2 for j in (0,1))
        hip = tuple((k[11][j]+k[12][j])/2 for j in (0,1))
        dx,dy = abs(hip[0]-shoulder[0]),abs(hip[1]-shoulder[1])
        if hypot(dx,dy) < self.config["min_torso_px"]:
            return "unknown"
        box = person["bbox_xyxy"]
        ratio = (box[2]-box[0])/max(1,box[3]-box[1])
        if dx > self.config["orientation_ratio"]*dy and ratio >= self.config["lying_bbox_ratio"]:
            poly = self.config["floor_polygon"]
            if poly and not _polygon_contains(_center(box), poly):
                return "unknown"
            return "lying"
        if dy > self.config["orientation_ratio"]*dx and ratio <= self.config["upright_bbox_ratio"]:
            return "upright"
        return "unknown"

    def _head_candidate(self, person, item):
        box = item["bbox_xyxy"]
        pbox = person["bbox_xyxy"]
        if not _inside(_center(box), pbox):
            return False
        k = person.get("keypoints")
        if k and len(k) == 17:
            points = [v for v in k[:5] if len(v)==3 and v[2] >= self.config["keypoint_score"]]
            if points:
                # Positive item must cover at least one visible anatomical head point.
                return any(_inside(v[:2],box) for v in points)
        if self.config["allow_bbox_head_association"]:
            return (pbox[2]-pbox[0])/max(1,pbox[3]-pbox[1]) < self.config["upright_bbox_ratio"] and _center(box)[1] <= pbox[1]+0.3*(pbox[3]-pbox[1])
        return False

    def _helmet_states(self, people, items):
        owners = {i:[] for i in range(len(people))}
        ambiguous = set()
        for item in items:
            possible = [i for i,p in enumerate(people) if self._head_candidate(p,item)]
            if len(possible) == 1:
                owners[possible[0]].append(item["class_name"])
            elif len(possible)>1:
                ambiguous.update(possible)
        result = {}
        for i in owners:
            names=owners[i]
            if i in ambiguous or len(names) != 1:
                result[i]="unknown"
            else:
                result[i]="violation" if names[0]=="bare_head" else "safe"
        return result

    def _mutation(self, event, state, reason, batch):
        event.update(revision=event["revision"]+1,state=state,close_reason=reason,
                     end_media_ms=batch["media_time_ms"],emitted_at=datetime.now(timezone.utc).isoformat())
        return deepcopy(event)

    def _interrupt(self, camera, batch, reason):
        events=[]
        for track in camera.tracks.values():
            for event in track.active.values():
                events.append(self._mutation(event,"interrupted",reason,batch))
        camera.tracks.clear()
        camera.generation += 1
        return events

    def on_gap(self, gap):
        """Explicit gaps break all pending evidence; active incidents interrupted.

        Required gap keys: camera_id, media_time_ms. Optional stream_epoch,
        reason. A late gap cannot interrupt newer accepted observations.
        """
        camera=self.cameras.get(gap["camera_id"])
        if not camera or gap.get("stream_epoch",camera.epoch) != camera.epoch:
            return []
        t=gap["media_time_ms"]
        if camera.last_time is not None and (t < camera.last_time or
                t == camera.last_time and camera.last_frame is None):
            # The last accepted item was already this gap. Replaying a durable
            # gap must not allocate a new tracker generation. A first EOF gap
            # at the last observed frame time may still interrupt an incident.
            return []
        events=self._interrupt(camera,gap,gap.get("reason","observation_gap"))
        camera.last_time=t
        camera.last_frame=None
        return events

    def _open(self, camera_id, camera, track, kind, start, batch):
        hazard="posture" if kind in ("suspected_fall","prolonged_lying") else kind
        if hazard in track.sent:
            return None
        event={"schema_version":"1.0","event_id":str(uuid4()),"revision":1,
               "camera_id":camera_id,"stream_epoch":camera.epoch,
               "zone_id":self.config["zone_id"],
               "track_key":f"{camera_id}/{camera.epoch}/{camera.generation}/{track.id}",
               "type":kind,"severity":"warning" if kind=="missing_helmet" else "critical",
               "state":"open","start_media_ms":start,"confirmed_media_ms":batch["media_time_ms"],
               "emitted_at":datetime.now(timezone.utc).isoformat(),
               "rule_version":self.config["rule_version"],
               "model_ids":batch.get("model_ids",[batch.get("model_id","unknown")]),
               "execution_backend":batch.get("backend","unknown"),
               "execution_records":deepcopy(batch.get("execution_records",[])),
               "evidence":{"frame_id":batch["frame_id"],"snapshot_ref":None,"clip_ref":None,"status":"pending"}}
        track.sent.add(hazard)
        track.active[hazard]=event
        return deepcopy(event)

    def _reset_motion(self, track):
        track.motion_previous=None
        track.still_since=None

    def _immobility(self, track, person, batch):
        """Bounded visible-keypoint low-motion evidence, never consciousness."""
        k=person.get("keypoints") or []
        points={str(i):list(v[:2]) for i,v in enumerate(k) if i>=5 and len(v)==3
                and all(isfinite(x) for x in v)
                and v[2]>=self.config["keypoint_score"]}
        t=batch["media_time_ms"]
        if len(points)<self.config["immobility_min_points"]:
            self._reset_motion(track)
            return []
        # _posture has already established four observed torso points.
        shoulders=[(k[5][j]+k[6][j])/2 for j in (0,1)]
        hips=[(k[11][j]+k[12][j])/2 for j in (0,1)]
        scale=max(self.config["min_torso_px"],hypot(hips[0]-shoulders[0],hips[1]-shoulders[1]))
        previous=track.motion_previous
        track.motion_previous={"time":t,"points":points,"scale":scale}
        if previous is None:
            track.still_since=None
            return []
        common=set(points)&set(previous["points"])
        elapsed=t-previous["time"]
        if len(common)<self.config["immobility_min_points"] or not 0<elapsed<=self.config["max_gap_ms"]:
            track.still_since=None
            return []
        # Maximum, rather than median, keeps one moving limb observable.
        speed=max(hypot(points[i][0]-previous["points"][i][0],
                        points[i][1]-previous["points"][i][1]) for i in common)
        speed/=max(scale,previous["scale"])*(elapsed/1000)
        if speed>self.config["immobility_max_speed"]:
            track.still_since=None
            return []
        if track.still_since is None:
            track.still_since=t
        event=track.active.get("posture")
        if (event is None or event.get("attributes",{}).get("immobility_observed")
                or t-track.still_since<self.config["confirm_immobility_ms"]):
            return []
        event.setdefault("attributes",{}).update(
            immobility_observed=True, immobility_since_media_ms=track.still_since,
            immobility_confirmed_media_ms=t,
            immobility_min_points=self.config["immobility_min_points"],
            immobility_max_speed=self.config["immobility_max_speed"])
        event["revision"]+=1
        event["emitted_at"]=datetime.now(timezone.utc).isoformat()
        event["update_reason"]="visible_keypoint_immobility"
        return [deepcopy(event)]

    def _observe(self, camera_id, camera, track, person, helmet, batch):
        t=batch["media_time_ms"]
        events=[]
        if helmet=="violation":
            start=track.candidates.setdefault("helmet",t)
            if t-start >= self.config["confirm_helmet_ms"]:
                event=self._open(camera_id,camera,track,"missing_helmet",start,batch)
                if event:events.append(event)
        else:
            track.candidates.pop("helmet",None)
            if helmet=="safe" and "missing_helmet" in track.active:
                events.append(self._mutation(track.active.pop("missing_helmet"),"closed","observed_compliance",batch))
        posture=self._posture(person)
        if posture=="upright":
            self._reset_motion(track)
            track.last_upright=t
            track.candidates.pop("lying",None)
            track.fall_candidate=False
            if "posture" in track.active:
                events.append(self._mutation(track.active.pop("posture"),"closed","observed_upright",batch))
        elif posture=="lying":
            if "lying" not in track.candidates:
                track.candidates["lying"]=t
                track.fall_candidate=track.last_upright is not None and t-track.last_upright<=self.config["transition_ms"]
            kind="suspected_fall" if track.fall_candidate else "prolonged_lying"
            duration=self.config["confirm_fall_ms"] if track.fall_candidate else self.config["confirm_lying_ms"]
            start=track.candidates["lying"]
            if t-start>=duration:
                event=self._open(camera_id,camera,track,kind,start,batch)
                if event:events.append(event)
        else:
            self._reset_motion(track)
            track.candidates.pop("lying",None)
            # Experimental H-FALL-02 only: an observed but undecidable posture
            # does not become lying evidence. Keep the last *observed upright*
            # timestamp only within the existing finite transition window.
            if (not self.config.get("retain_upright_during_unknown",False) or
                    track.last_upright is not None and t-track.last_upright>self.config["transition_ms"]):
                track.last_upright=None
            track.fall_candidate=False
        if posture=="lying":
            events.extend(self._immobility(track,person,batch))
        return events

    def update(self, batch):
        validate_observation(batch)
        if batch["status"] != "ok":
            return self.on_gap(batch)
        cid,epoch,t,fid=(batch[k] for k in ("camera_id","stream_epoch","media_time_ms","frame_id"))
        camera=self.cameras.get(cid)
        events=[]
        if camera and epoch != camera.epoch:
            # Retired epoch results must not reset the current stream.
            retired=getattr(camera,"retired_epochs",set())
            if epoch in retired:return []
            old=camera.epoch
            # New stream media time has a different origin. Close the retired
            # epoch at its last observed timestamp, never at new-epoch zero.
            retired_batch = {**batch, "media_time_ms": camera.last_time if camera.last_time is not None else t}
            events.extend(self._interrupt(camera,retired_batch,"stream_reset"))
            camera.epoch=epoch
            camera.last_time=camera.last_frame=None
            camera.retired_epochs=retired|{old}
        if camera is None:
            camera=Camera(epoch)
            self.cameras[cid]=camera
        if camera.last_time is not None:
            if t<=camera.last_time or camera.last_frame is not None and fid<=camera.last_frame:
                return []
            if t-camera.last_time>self.config["max_gap_ms"]:
                events.extend(self._interrupt(camera,batch,"observation_gap"))
        camera.last_time,camera.last_frame=t,fid
        for tid,track in list(camera.tracks.items()):
            if t-track.last_seen>self.config["track_exit_ms"]:
                for event in track.active.values():
                    events.append(self._mutation(event,"closed","track_exit",batch))
                del camera.tracks[tid]
        ds=[d for d in batch["detections"] if d["score"]>=self.config["min_score"]]
        people=[d for d in ds if d["class_name"]=="person"]
        helmets=self._helmet_states(people,[d for d in ds if d["class_name"] in ("helmet","bare_head")])
        pairs=[]
        for i,p in enumerate(people):
            for tid,tr in camera.tracks.items():
                a,b=_center(p["bbox_xyxy"]),_center(tr.box)
                scale=max(1,hypot(tr.box[2]-tr.box[0],tr.box[3]-tr.box[1]))
                distance=hypot(a[0]-b[0],a[1]-b[1])/scale
                overlap=_iou(p["bbox_xyxy"],tr.box)
                if overlap>=0.05 or distance<=self.config["match_distance"]:
                    pairs.append((overlap+max(0,1-distance),i,tid))
        # Ambiguous crossings do not borrow another person's accumulated evidence.
        ambiguous_people=set(); ambiguous_tracks=set()
        for score,i,tid in pairs:
            if any((i==j or tid==tj) and (i,tid)!=(j,tj) and abs(score-s)<self.config["match_ambiguity"] for s,j,tj in pairs):
                ambiguous_people.add(i);ambiguous_tracks.add(tid)
        matched={};used=set()
        for score,i,tid in sorted(pairs,reverse=True):
            if i not in matched and tid not in used and i not in ambiguous_people and tid not in ambiguous_tracks:
                matched[i]=tid;used.add(tid)
        for tid,tr in camera.tracks.items():
            if tid not in used:
                tr.candidates.clear();tr.last_upright=None;tr.fall_candidate=False
                self._reset_motion(tr)
        for i,p in enumerate(people):
            if i in ambiguous_people:continue
            tid=matched.get(i)
            if tid is None:
                tid=camera.next_id;camera.next_id+=1
                camera.tracks[tid]=Track(tid,p["bbox_xyxy"],t)
            tr=camera.tracks[tid]
            if t-tr.last_seen>self.config["max_gap_ms"]:
                tr.candidates.clear();tr.last_upright=None;tr.fall_candidate=False
                self._reset_motion(tr)
            tr.box=p["bbox_xyxy"];tr.last_seen=t
            events.extend(self._observe(cid,camera,tr,p,helmets[i],batch))
        return events

    def export_state(self):
        """JSON checkpoint; commit atomically with event mutations/outbox.

        Restoring the checkpoint keeps sent suppression and event UUIDs. Camera
        identities and source timestamps must also survive pipeline restart.
        """
        cameras={}
        for cid,c in self.cameras.items():
            tracks=[]
            for tr in c.tracks.values():
                tracks.append({"id":tr.id,"box":tr.box,"last_seen":tr.last_seen,
                               "candidates":tr.candidates,"sent":sorted(tr.sent),
                               "active":tr.active,"last_upright":tr.last_upright,
                               "fall_candidate":tr.fall_candidate,
                               "motion_previous":tr.motion_previous,"still_since":tr.still_since})
            cameras[cid]={"epoch":c.epoch,"generation":c.generation,
                          "last_time":c.last_time,"last_frame":c.last_frame,
                          "next_id":c.next_id,"tracks":tracks,
                          "retired_epochs":sorted(getattr(c,"retired_epochs",set()))}
        return deepcopy({"version":1,"config":self.config,"cameras":cameras})

    def restore_state(self, state):
        """Restore a previously committed checkpoint; reject policy changes."""
        if state.get("version") != 1 or state.get("config") != self.config:
            raise ValueError("incompatible behavior checkpoint or rule config")
        restored={}
        for cid,v in deepcopy(state["cameras"]).items():
            c=Camera(v["epoch"],v["generation"],v["last_time"],v["last_frame"],v["next_id"])
            c.retired_epochs=set(v.get("retired_epochs",[]))
            for item in v["tracks"]:
                item["sent"]=set(item["sent"])
                tr=Track(**item)
                c.tracks[tr.id]=tr
            restored[cid]=c
        self.cameras=restored
