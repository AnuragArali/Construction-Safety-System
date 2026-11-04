import time
from ai.detection_utils import is_point_or_box_in_zone
from safety.recommendations import RecommendationEngine
from config import settings

class ViolationAnalyzer:
    def __init__(self):
        # Debounce state: { (worker_id, violation_type): last_alert_time }
        self._last_alert_timestamps: dict[tuple[str, str], float] = {}

    def analyze(
        self,
        workers: list[dict],
        restricted_zones: list[dict],
        frame_width: int,
        frame_height: int,
        language: str = "en",
        cooldown_seconds: float = None
    ) -> tuple[list[dict], list[dict]]:
        """
        Evaluates detection results against safety rules.
        Returns:
            - updated_workers: list of worker dicts with 'violations' list added
            - active_violations: list of violations detected in this frame,
                                 flagged with 'trigger_alert' based on debounce cooldown.
        """
        cooldown = cooldown_seconds or settings.ALERT_COOLDOWN_SECONDS
        current_time = time.time()
        active_violations = []
        updated_workers = []

        for worker in workers:
            w_dict = dict(worker)
            w_violations = []
            w_id = worker.get("worker_id", "Worker-Anonymous")
            w_box = worker.get("box", {})

            # 1. Check Missing Helmet Violation
            if not worker.get("has_helmet", False):
                v_type = "MISSING_HELMET"
                w_violations.append("NO_HELMET")
                rec_info = RecommendationEngine.get_recommendation(v_type, language)

                deb_key = (w_id, v_type)
                last_time = self._last_alert_timestamps.get(deb_key, 0.0)
                should_alert = (current_time - last_time) >= cooldown
                if should_alert:
                    self._last_alert_timestamps[deb_key] = current_time

                active_violations.append({
                    "violation_type": v_type,
                    "category": "PPE",
                    "severity": "HIGH",
                    "confidence": worker.get("confidence", 0.85),
                    "worker_tag": w_id,
                    "recommendation": rec_info["recommendation"],
                    "alert_title": rec_info["alert"],
                    "voice_text": rec_info["voice"],
                    "language": language,
                    "trigger_alert": should_alert,
                    "zone_name": "General Workspace"
                })

            # 2. Check Missing High-Visibility Vest Violation
            if not worker.get("has_vest", False):
                v_type = "MISSING_VEST"
                w_violations.append("NO_VEST")
                rec_info = RecommendationEngine.get_recommendation(v_type, language)

                deb_key = (w_id, v_type)
                last_time = self._last_alert_timestamps.get(deb_key, 0.0)
                should_alert = (current_time - last_time) >= cooldown
                if should_alert:
                    self._last_alert_timestamps[deb_key] = current_time

                active_violations.append({
                    "violation_type": v_type,
                    "category": "PPE",
                    "severity": "MEDIUM",
                    "confidence": worker.get("confidence", 0.80),
                    "worker_tag": w_id,
                    "recommendation": rec_info["recommendation"],
                    "alert_title": rec_info["alert"],
                    "voice_text": rec_info["voice"],
                    "language": language,
                    "trigger_alert": should_alert,
                    "zone_name": "General Workspace"
                })

            # 3. Check Restricted Zone Intrusion
            for zone in restricted_zones:
                if is_point_or_box_in_zone(w_box, zone, frame_width, frame_height):
                    v_type = "RESTRICTED_ZONE_INTRUSION"
                    w_violations.append("ZONE_INTRUSION")
                    rec_info = RecommendationEngine.get_recommendation(v_type, language)

                    deb_key = (w_id, f"{v_type}_{zone.get('name')}")
                    last_time = self._last_alert_timestamps.get(deb_key, 0.0)
                    should_alert = (current_time - last_time) >= cooldown
                    if should_alert:
                        self._last_alert_timestamps[deb_key] = current_time

                    active_violations.append({
                        "violation_type": v_type,
                        "category": "ZONE_BOUNDARY",
                        "severity": "CRITICAL",
                        "confidence": 0.95,
                        "worker_tag": w_id,
                        "recommendation": rec_info["recommendation"],
                        "alert_title": rec_info["alert"],
                        "voice_text": rec_info["voice"],
                        "language": language,
                        "trigger_alert": should_alert,
                        "zone_name": zone.get("name", "Hazardous Zone")
                    })

            w_dict["violations"] = w_violations
            updated_workers.append(w_dict)

        return updated_workers, active_violations
