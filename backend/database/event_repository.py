import uuid
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database.models import SafetyEvent, SafetyRule, SystemConfig, PrivacyAuditLog, Worker, CheckpointAccessLog

class EventRepository:
    @staticmethod
    def create_safety_event(db: Session, data: dict) -> SafetyEvent:
        event = SafetyEvent(
            event_uuid=data.get("event_uuid", str(uuid.uuid4())),
            timestamp=data.get("timestamp", datetime.datetime.utcnow()),
            violation_type=data.get("violation_type", "Unknown Violation"),
            category=data.get("category", "PPE"),
            severity=data.get("severity", "MEDIUM"),
            confidence=data.get("confidence", 0.0),
            recommendation=data.get("recommendation", "Please follow safety guidelines."),
            voice_alert_generated=data.get("voice_alert_generated", False),
            alert_delivered=data.get("alert_delivered", False),
            language=data.get("language", "en"),
            worker_tag=data.get("worker_tag", "Worker-Anonymous"),
            zone_name=data.get("zone_name", "General Worksite"),
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def get_events(
        db: Session,
        limit: int = 50,
        offset: int = 0,
        violation_type: str | None = None,
        severity: str | None = None,
        category: str | None = None
    ) -> list[SafetyEvent]:
        query = db.query(SafetyEvent)
        if violation_type:
            query = query.filter(SafetyEvent.violation_type.ilike(f"%{violation_type}%"))
        if severity:
            query = query.filter(SafetyEvent.severity == severity.upper())
        if category:
            query = query.filter(SafetyEvent.category == category.upper())
        return query.order_by(desc(SafetyEvent.timestamp)).offset(offset).limit(limit).all()

    @staticmethod
    def get_latest_alerts(db: Session, limit: int = 6) -> list[SafetyEvent]:
        return db.query(SafetyEvent).order_by(desc(SafetyEvent.timestamp)).limit(limit).all()

    @staticmethod
    def get_statistics(db: Session) -> dict:
        total_events = db.query(SafetyEvent).count()
        today = datetime.datetime.utcnow().date()
        today_start = datetime.datetime.combine(today, datetime.time.min)
        today_events = db.query(SafetyEvent).filter(SafetyEvent.timestamp >= today_start).count()

        # Group by violation type
        by_type_rows = db.query(
            SafetyEvent.violation_type, func.count(SafetyEvent.id)
        ).group_by(SafetyEvent.violation_type).all()
        by_type = {row[0]: row[1] for row in by_type_rows}

        # Group by severity
        by_severity_rows = db.query(
            SafetyEvent.severity, func.count(SafetyEvent.id)
        ).group_by(SafetyEvent.severity).all()
        by_severity = {row[0]: row[1] for row in by_severity_rows}

        # Compliance score: 100 - min(100, today_events * 3.5)
        compliance_rate = max(0, min(100, 100 - (today_events * 4)))

        # Daily breakdown for last 7 days
        daily_trends = []
        for i in range(6, -1, -1):
            day_dt = today - datetime.timedelta(days=i)
            day_s = datetime.datetime.combine(day_dt, datetime.time.min)
            day_e = datetime.datetime.combine(day_dt, datetime.time.max)
            cnt = db.query(SafetyEvent).filter(SafetyEvent.timestamp >= day_s, SafetyEvent.timestamp <= day_e).count()
            daily_trends.append({
                "date": day_dt.strftime("%b %d"),
                "violations": cnt
            })

        return {
            "total_events": total_events,
            "today_violations": today_events,
            "compliance_rate": compliance_rate,
            "by_type": by_type,
            "by_severity": by_severity,
            "daily_trends": daily_trends
        }

    @staticmethod
    def get_rules(db: Session) -> list[SafetyRule]:
        return db.query(SafetyRule).all()

    @staticmethod
    def toggle_rule(db: Session, rule_code: str, enabled: bool) -> SafetyRule | None:
        rule = db.query(SafetyRule).filter(SafetyRule.rule_code == rule_code).first()
        if rule:
            rule.is_enabled = enabled
            db.commit()
            db.refresh(rule)
        return rule

    @staticmethod
    def purge_expired_records(db: Session, retention_days: int) -> int:
        cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=retention_days)
        deleted = db.query(SafetyEvent).filter(SafetyEvent.timestamp < cutoff).delete()
        db.commit()
        # Log to privacy audit
        audit = PrivacyAuditLog(
            action="DATA_RETENTION_PURGE",
            details=f"Purged {deleted} records older than {retention_days} days."
        )
        db.add(audit)
        db.commit()
        return deleted

    @staticmethod
    def get_audit_logs(db: Session, limit: int = 20) -> list[PrivacyAuditLog]:
        return db.query(PrivacyAuditLog).order_by(desc(PrivacyAuditLog.timestamp)).limit(limit).all()

    # --- Worker Biometrics & Directory Repository Methods ---
    @staticmethod
    def get_workers(db: Session, is_active: bool = True) -> list[Worker]:
        query = db.query(Worker)
        if is_active is not None:
            query = query.filter(Worker.is_active == is_active)
        return query.order_by(Worker.worker_id).all()

    @staticmethod
    def get_worker_by_id(db: Session, worker_id: str) -> Worker | None:
        return db.query(Worker).filter(Worker.worker_id == worker_id).first()

    @staticmethod
    def get_worker_by_fingerprint_id(db: Session, fingerprint_id: int) -> Worker | None:
        return db.query(Worker).filter(Worker.fingerprint_id == fingerprint_id).first()

    @staticmethod
    def create_worker(db: Session, data: dict) -> Worker:
        worker = Worker(
            worker_id=data["worker_id"],
            name=data["name"],
            role=data.get("role", "Technician"),
            department=data.get("department", "Construction & Framing"),
            fingerprint_id=data.get("fingerprint_id"),
            fingerprint_enrolled=data.get("fingerprint_enrolled", False),
            fingerprint_hash=data.get("fingerprint_hash"),
            face_enrolled=data.get("face_enrolled", False),
            face_features=data.get("face_features"),
            photo_thumbnail=data.get("photo_thumbnail"),
            authorized_zones=",".join(data.get("authorized_zones", ["General Worksite", "Doorway-North"]))
            if isinstance(data.get("authorized_zones"), list)
            else data.get("authorized_zones", "General Worksite,Doorway-North"),
            is_active=data.get("is_active", True)
        )
        db.add(worker)
        db.commit()
        db.refresh(worker)
        return worker

    @staticmethod
    def update_worker(db: Session, worker_id: str, updates: dict) -> Worker | None:
        worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
        if not worker:
            return None
        for key, val in updates.items():
            if hasattr(worker, key):
                if key == "authorized_zones" and isinstance(val, list):
                    val = ",".join(val)
                setattr(worker, key, val)
        worker.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(worker)
        return worker

    @staticmethod
    def delete_worker(db: Session, worker_id: str) -> bool:
        worker = db.query(Worker).filter(Worker.worker_id == worker_id).first()
        if not worker:
            return False
        db.delete(worker)
        db.commit()
        return True

    # --- Checkpoint Access Logs Repository Methods ---
    @staticmethod
    def create_checkpoint_log(db: Session, data: dict) -> CheckpointAccessLog:
        log = CheckpointAccessLog(
            checkpoint_name=data.get("checkpoint_name", "Doorway-North"),
            worker_id=data.get("worker_id"),
            worker_name=data.get("worker_name"),
            auth_method=data.get("auth_method", "FINGERPRINT+FACE"),
            fingerprint_verified=data.get("fingerprint_verified", False),
            face_verified=data.get("face_verified", False),
            has_helmet=data.get("has_helmet", False),
            has_vest=data.get("has_vest", False),
            access_decision=data.get("access_decision", "DENIED"),
            reason=data.get("reason", ""),
            confidence_score=data.get("confidence_score", 0.0),
            voice_announcement=data.get("voice_announcement"),
            gpio_pulse_sent=data.get("gpio_pulse_sent", False)
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_checkpoint_logs(db: Session, limit: int = 50, offset: int = 0) -> list[CheckpointAccessLog]:
        return db.query(CheckpointAccessLog).order_by(desc(CheckpointAccessLog.timestamp)).offset(offset).limit(limit).all()

    @staticmethod
    def get_checkpoint_statistics(db: Session) -> dict:
        total = db.query(CheckpointAccessLog).count()
        granted = db.query(CheckpointAccessLog).filter(CheckpointAccessLog.access_decision == "GRANTED").count()
        denied_ppe = db.query(CheckpointAccessLog).filter(CheckpointAccessLog.access_decision == "DENIED_PPE_VIOLATION").count()
        denied_auth = db.query(CheckpointAccessLog).filter(CheckpointAccessLog.access_decision.in_(["DENIED_BIOMETRIC_FAIL", "DENIED_UNAUTHORIZED"])).count()
        
        compliance_pct = round((granted / total * 100), 1) if total > 0 else 100.0
        return {
            "total_checkpoints_logged": total,
            "granted_count": granted,
            "denied_ppe_count": denied_ppe,
            "denied_auth_count": denied_auth,
            "doorway_compliance_rate": compliance_pct
        }
