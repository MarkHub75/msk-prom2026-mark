import os
import time
from collections import deque

import cv2
import numpy as np
from ultralytics import YOLO

from event_logger import SmokingEventLogger
from pose_detector import ActionPoseDetector

DEBUG = True

VIDEO_SOURCE = "test_video.mp4"

SAVE_ANNOTATED_OUTPUT = True
OUTPUT_PATH = "test_video_annotated.mp4"

PERSON_MODEL_PATH = "yolov8n.pt"
PERSON_CONFIDENCE, PERSON_IOU = 0.30, 0.45
MIN_PERSON_WIDTH, MIN_PERSON_HEIGHT, MIN_PERSON_AREA = 35, 60, 2000
POSE_REQUIRED_FRAMES = 30
PERSON_DETECT_INTERVAL, POSE_INTERVAL, LANDMARK_INTERVAL = 2, 2, 3
TRACK_MAX_MISSING, TRACK_MAX_CENTER_DISTANCE = 45, 0.70
HAND_MOUTH_THRESHOLD = 0.16
ACTION_SMOOTHING, HAND_HISTORY = 6, 12
SMOKE_CONFIRM_FRAMES, SMOKE_RESET_FRAMES = 5, 10
SMOKE_MIN_PROBABILITY = 0.65
SKELETON_CONNECTIONS = (
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (5, 11), (6, 12), (11, 12), (11, 13), (13, 15),
    (12, 14), (14, 16), (0, 1), (0, 2), (1, 3), (2, 4),
    (0, 5), (0, 6),
)


def box_iou(a, b):
    ax1, ay1, ax2, ay2 = a; bx1, by1, bx2, by2 = b
    intersection = max(0, min(ax2, bx2) - max(ax1, bx1)) * max(0, min(ay2, by2) - max(ay1, by1))
    union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - intersection
    return intersection / union if union > 0 else 0.0


def center_distance(a, b):
    ac = np.asarray(((a[0] + a[2]) / 2, (a[1] + a[3]) / 2))
    bc = np.asarray(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
    return float(np.linalg.norm(ac - bc) / max(1.0, np.hypot(a[2] - a[0], a[3] - a[1])))


class PersonState:
    """No state in this class is shared by another detected person."""
    def __init__(self, track_id, bbox):
        self.track_id, self.bbox = track_id, bbox
        self.pose_sequence = deque(maxlen=POSE_REQUIRED_FRAMES)
        self.action_history = deque(maxlen=ACTION_SMOOTHING)
        self.posture_history = deque(maxlen=ACTION_SMOOTHING)
        self.posture = "UNKNOWN"
        self.hand_history = deque(maxlen=HAND_HISTORY)
        self.action = self.raw_action = "ANALYZING"
        self.action_confidence = self.smoke_probability = 0.0
        self.hand_mouth_score = self.hand_mouth_detected = None
        self.confirmed_smoking = False
        self.confirm_streak = self.reset_streak = self.missing_frames = 0
        self.last_seen = time.time()
        self.smoking_started_at = None

    @property
    def pose_ready(self):
        return len(self.pose_sequence) == POSE_REQUIRED_FRAMES


class SmokingDetectionSystem:
    def __init__(self):
        print("Loading person detector...")
        self.person_model = YOLO(PERSON_MODEL_PATH)
        print("Loading pose detector...")
        self.pose_detector = ActionPoseDetector()
        print("Loading action model...")
                                                                            
                                                                  
        from action_predictor import ActionPredictor
        self.action_predictor = ActionPredictor()
        print("Loading hand/face detector...")
        from hand_face_detector import HandFaceDetector
                                                                                 
        self.hand_face_detector = HandFaceDetector(HAND_MOUTH_THRESHOLD)
        self.event_logger = SmokingEventLogger()
        self.tracks, self.next_track_id = {}, 1
        self.frame_number, self.fps, self.last_time = 0, 0.0, time.time()
        print("SYSTEM READY")

    def debug(self, text):
        if DEBUG:
            print(text)

    def detect_people(self, frame):
        try:
            results = self.person_model.predict(frame, imgsz=640, conf=PERSON_CONFIDENCE, iou=PERSON_IOU,
                                                classes=[0], max_det=20, verbose=False)
        except Exception as error:
            print(f"[TRACK] person inference error: {error}")
            return []
        detections = []
        for result in results:
            if result.boxes is None:
                continue
            for box in result.boxes.xyxy.cpu().numpy():
                x1, y1, x2, y2 = map(int, box)
                if x2-x1 >= MIN_PERSON_WIDTH and y2-y1 >= MIN_PERSON_HEIGHT and (x2-x1)*(y2-y1) >= MIN_PERSON_AREA:
                    detections.append((x1, y1, x2, y2))
        return detections

    def update_tracks(self, detections):
        for state in self.tracks.values():
            state.missing_frames += 1
        pairs = []
        for detection_index, box in enumerate(detections):
            for track_id, state in self.tracks.items():
                overlap, distance = box_iou(state.bbox, box), center_distance(state.bbox, box)
                                                                            
                                                                            
                                                                     
                if overlap >= 0.05 or distance <= TRACK_MAX_CENTER_DISTANCE:
                    pairs.append((-(0.75 * overlap + 0.25 * max(0.0, 1.0-distance)), track_id, detection_index))
        used_tracks, used_detections = set(), set()
        for _, track_id, detection_index in sorted(pairs):
            if track_id in used_tracks or detection_index in used_detections:
                continue
            state = self.tracks[track_id]
            state.bbox, state.last_seen, state.missing_frames = detections[detection_index], time.time(), 0
            used_tracks.add(track_id); used_detections.add(detection_index)
            self.debug(f"[TRACK] ID={track_id} matched")
        for index, box in enumerate(detections):
            if index not in used_detections:
                self.tracks[self.next_track_id] = PersonState(self.next_track_id, box)
                self.debug(f"[TRACK] ID={self.next_track_id} created")
                self.next_track_id += 1
        for track_id in [key for key, value in self.tracks.items() if value.missing_frames > TRACK_MAX_MISSING]:
            state = self.tracks.pop(track_id)
            if state.confirmed_smoking and state.smoking_started_at is not None:
                self.event_logger.log_event(track_id, state.smoking_started_at, time.time())
            self.debug(f"[TRACK] ID={track_id} expired")

    def update_action(self, state, pose):
        if pose is None:
            self.debug(f"[POSE] ID={state.track_id} detected=False sequence={len(state.pose_sequence)}/30")
            return
        pose = np.asarray(pose, dtype=np.float32)
        if pose.shape != (34,):
            print(f"[POSE] ID={state.track_id} invalid shape={pose.shape}")
            return
        state.pose_sequence.append(pose)
        self.debug(f"[POSE] ID={state.track_id} detected=True sequence={len(state.pose_sequence)}/30")
        if not state.pose_ready:
            state.action = state.raw_action = "ANALYZING"; state.action_confidence = state.smoke_probability = 0.0
            return
        try:
            result = self.action_predictor.predict(list(state.pose_sequence))
        except Exception as error:
            print(f"[ACTION] ID={state.track_id} error: {error}")
            return
        state.raw_action = str(result["action"]).upper()
        state.action_confidence = float(result["confidence"])
        labels = self.action_predictor.labels
        smoke_index = labels.index("smoke") if isinstance(labels, list) and "smoke" in labels else None
        probabilities = np.asarray(result["probabilities"], dtype=float)
        state.smoke_probability = float(probabilities[smoke_index]) if smoke_index is not None else 0.0
        state.action_history.append(state.raw_action)
        state.action = max(set(state.action_history), key=state.action_history.count)
        self.debug(f"[ACTION] ID={state.track_id} raw={state.raw_action} conf={state.action_confidence:.2f} smoke={state.smoke_probability:.2f}")

    def update_posture(self, state, keypoints):
        """Classify body posture independently from the smoking class.

        YOLO's 17 body keypoints provide the stable standing/sitting signal;
        the temporal model's smoke label is deliberately not used here.
        """
        if keypoints is None or np.asarray(keypoints).shape != (17, 2):
            return
        points = np.asarray(keypoints, dtype=np.float32)
        x1, y1, x2, y2 = state.bbox
        height = max(1.0, y2 - y1)
        hips = points[[11, 12]]
        knees = points[[13, 14]]
        ankles = points[[15, 16]]
        
        if np.any(hips <= 0) or np.any(knees <= 0):
            return
        hip_y, knee_y = float(np.mean(hips[:, 1])), float(np.mean(knees[:, 1]))
        hip_to_knee = (knee_y - hip_y) / height
        ankles_valid = np.all(ankles > 0)
        hip_to_ankle = ((float(np.mean(ankles[:, 1])) - hip_y) / height
                         if ankles_valid else 0.0)

        if state.raw_action == "WALK":
            posture = "WALKING"
        elif hip_to_knee < 0.18 or (ankles_valid and hip_to_ankle < 0.35):
            posture = "SITTING"
        elif hip_to_knee >= 0.18 and (not ankles_valid or hip_to_ankle >= 0.35):
            posture = "STANDING"
        else:
            posture = "UNKNOWN"
        state.posture_history.append(posture)
        state.posture = max(set(state.posture_history), key=state.posture_history.count)
        self.debug(f"[POSTURE] ID={state.track_id} pose={state.posture} hip-knee={hip_to_knee:.2f}")

    def update_hand_mouth(self, frame, state):
        x1, y1, x2, y2 = state.bbox
        crop = frame[max(0,y1):max(y1+1,y2), max(0,x1):max(x1+1,x2)]
        detected, distance = self.hand_face_detector.detect(crop)
        state.hand_mouth_score = distance
        state.hand_mouth_detected = bool(detected) if distance is not None else None
        if distance is not None:
            state.hand_history.append(bool(detected))
        value = "N/A" if distance is None else f"{bool(detected)} ({distance:.3f})"
        self.debug(f"[HAND] [MOUTH] ID={state.track_id} {value}")

    def update_smoking(self, state):
        if not state.pose_ready:
            state.confirmed_smoking = False
            return
        hand_hits = sum(state.hand_history)
        
        evidence = state.smoke_probability >= SMOKE_MIN_PROBABILITY and hand_hits >= 2 and state.hand_mouth_detected is not None
        if evidence:
            state.confirm_streak += 1; state.reset_streak = 0
        else:
            state.confirm_streak = 0; state.reset_streak += 1
        was_smoking = state.confirmed_smoking
        if state.confirm_streak >= SMOKE_CONFIRM_FRAMES:
            state.confirmed_smoking = True
        elif state.reset_streak >= SMOKE_RESET_FRAMES:
            state.confirmed_smoking = False
        now = time.time()
        if state.confirmed_smoking and not was_smoking:
            state.smoking_started_at = now
        elif was_smoking and not state.confirmed_smoking and state.smoking_started_at is not None:
            self.event_logger.log_event(state.track_id, state.smoking_started_at, now); state.smoking_started_at = None
        self.debug(f"[SMOKING] ID={state.track_id} p={state.smoke_probability:.2f} hands={hand_hits} confirmed={state.confirmed_smoking}")

    def process_frame(self, frame):
        self.frame_number += 1
        if self.frame_number % PERSON_DETECT_INTERVAL == 1:
            self.update_tracks(self.detect_people(frame))
        active = {track_id: state.bbox for track_id, state in self.tracks.items() if state.missing_frames == 0}
        if self.frame_number % POSE_INTERVAL == 1:
            poses = self.pose_detector.detect_for_tracks(frame, active)
            for track_id, pose in poses.items():
                self.update_action(self.tracks[track_id], pose)
                self.update_posture(self.tracks[track_id], self.pose_detector.last_keypoints_by_track.get(track_id))
        if self.frame_number % LANDMARK_INTERVAL == 1:
            for track_id in active:
                self.update_hand_mouth(frame, self.tracks[track_id])
        smoking = not_smoking = analyzing = 0
        for track_id in active:
            state = self.tracks[track_id]; self.update_smoking(state)
            smoking += state.confirmed_smoking; not_smoking += state.pose_ready and not state.confirmed_smoking; analyzing += not state.pose_ready
            self.draw_skeleton(frame, self.pose_detector.last_keypoints_by_track.get(track_id))
            self.draw_person(frame, state)
        self.draw_panel(frame, len(active), smoking, not_smoking, analyzing)
        return frame

    @staticmethod
    def draw_skeleton(frame, keypoints):
        """Draw the actual 17-point YOLO pose assigned to this track."""
        if keypoints is None or np.asarray(keypoints).shape != (17, 2):
            return
        points = np.asarray(keypoints, dtype=np.int32)
        for start, end in SKELETON_CONNECTIONS:
            a, b = points[start], points[end]
            if np.all(a > 0) and np.all(b > 0):
                cv2.line(frame, tuple(a), tuple(b), (255, 0, 255), 2, cv2.LINE_AA)
        for point in points:
            if np.all(point > 0):
                cv2.circle(frame, tuple(point), 3, (0, 255, 255), -1, cv2.LINE_AA)

    def draw_person(self, frame, state):
        x1, y1, x2, y2 = state.bbox
        status = "SMOKING" if state.confirmed_smoking else ("NOT SMOKING" if state.pose_ready else "ANALYZING")
        color = (0,0,255) if state.confirmed_smoking else ((0,255,0) if state.pose_ready else (0,255,255))
        hand = "N/A" if state.hand_mouth_detected is None else ("YES" if state.hand_mouth_detected else "NO")
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        lines = [f"Person {state.track_id}: {status}", f"Pose: {state.posture}",
                 f"Action: {state.action} ({state.action_confidence*100:.0f}%)",
                 f"Pose frames: {len(state.pose_sequence)}/30", f"Hand-Mouth: {hand}",
                 f"Smoke probability: {state.smoke_probability*100:.0f}%"]
        for index, text in enumerate(lines):
            cv2.putText(frame, text, (x1, max(22, y1-8+index*20)), cv2.FONT_HERSHEY_SIMPLEX, .52,
                        color if index == 0 else (255,255,255), 2, cv2.LINE_AA)

    @staticmethod
    def draw_panel(frame, people, smoking, not_smoking, analyzing):
        overlay = frame.copy(); cv2.rectangle(overlay, (15,15), (355,155), (20,20,20), -1); cv2.addWeighted(overlay,.82,frame,.18,0,frame)
        entries = [(f"People: {people}",(255,255,255)), (f"Smoking: {smoking}",(0,0,255)), (f"Not Smoking: {not_smoking}",(0,255,0)), (f"Analyzing: {analyzing}",(0,255,255))]
        for index, (text, color) in enumerate(entries):
            cv2.putText(frame, text, (30,45+index*30), cv2.FONT_HERSHEY_SIMPLEX, .65, color, 2, cv2.LINE_AA)

    def run(self):
        is_file_source = isinstance(VIDEO_SOURCE, str)

        if is_file_source and not os.path.exists(VIDEO_SOURCE):
            raise FileNotFoundError(
                f"Video file not found: {VIDEO_SOURCE}\n"
                f"Place it next to main.py, or update VIDEO_SOURCE at the "
                f"top of this file to the correct path."
            )

        cap = cv2.VideoCapture(VIDEO_SOURCE)

        if not is_file_source:
            
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not cap.isOpened():
            raise RuntimeError(f"Could not open video source: {VIDEO_SOURCE}")

        writer = None

        if is_file_source and SAVE_ANNOTATED_OUTPUT:
            source_fps = cap.get(cv2.CAP_PROP_FPS)
            if not source_fps or source_fps <= 1:
                source_fps = 25.0  

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, source_fps, (frame_width, frame_height))

            if not writer.isOpened():
                print(f"WARNING: could not open output writer for {OUTPUT_PATH}; annotated output will not be saved.")
                writer = None
            else:
                print(f"Saving annotated output to: {OUTPUT_PATH}")

        print("Video started. Press Q to quit." if is_file_source else "Camera started. Press Q to quit.")

        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    if is_file_source:
                        print("End of video reached.")
                    else:
                        print("Camera frame read failed.")
                    break

                now = time.time(); elapsed = now-self.last_time; self.last_time = now
                if elapsed > 0: self.fps = .9*self.fps + .1/elapsed
                frame = self.process_frame(frame)
                cv2.putText(frame, f"FPS: {self.fps:.1f}", (frame.shape[1]-150,35), cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2,cv2.LINE_AA)

                if writer is not None:
                    writer.write(frame)

                cv2.imshow("Smoking Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"): break
        finally:
            cap.release()
            if writer is not None:
                writer.release()
            cv2.destroyAllWindows(); self.close()

    def close(self):
        self.hand_face_detector.close()


if __name__ == "__main__":
    SmokingDetectionSystem().run()