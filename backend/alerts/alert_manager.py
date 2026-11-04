import datetime
from collections import deque
from database.db import SessionLocal
from database.event_repository import EventRepository
from alerts.voice_alert import VoiceAlertService

class AlertManager:
    _instance = None

    def __init__(self):
        self.recent_alerts = deque(maxlen=30)
        self.voice_service = VoiceAlertService.get_instance()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AlertManager()
        return cls._instance

    def process_violations(self, violations: list[dict], language: str = "en") -> list[dict]:
        """
        Receives violations from the violation analyzer.
        For active violations flagged for alert triggering:
          1. Spawns native language voice warning
          2. Creates minimal database event record in SQLite
          3. Appends to live alerts buffer for worker app display
        """
        dispatched_alerts = []

        for v in violations:
            if v.get("trigger_alert", False):
                voice_text = v.get("voice_text", v.get("recommendation", ""))
                # 1. Trigger voice alert
                self.voice_service.speak(voice_text, language)

                # 2. Persist minimal event to local SQLite
                db = SessionLocal()
                try:
                    event_data = {
                        "violation_type": v["violation_type"],
                        "category": v["category"],
                        "severity": v["severity"],
                        "confidence": v["confidence"],
                        "recommendation": v["recommendation"],
                        "voice_alert_generated": True,
                        "alert_delivered": True,
                        "language": language,
                        "worker_tag": v["worker_tag"],
                        "zone_name": v.get("zone_name", "General Workspace"),
                    }
                    db_event = EventRepository.create_safety_event(db, event_data)
                    event_dict = db_event.to_dict()
                finally:
                    db.close()

                # 3. Add to live memory buffer
                self.recent_alerts.appendleft(event_dict)
                dispatched_alerts.append(event_dict)

        return dispatched_alerts

    def get_recent_alerts(self, limit: int = 10) -> list[dict]:
        return list(self.recent_alerts)[:limit]
