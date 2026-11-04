import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SafetyEvent(Base):
    """
    Stores minimal necessary event information per synopsis privacy specification.
    No raw video footage is ever stored here.
    """
    __tablename__ = "safety_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_uuid = Column(String(64), unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    violation_type = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False) # e.g., "PPE", "RESTRICTED_ZONE", "EQUIPMENT"
    severity = Column(String(20), nullable=False, default="MEDIUM") # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    confidence = Column(Float, nullable=False)
    recommendation = Column(Text, nullable=False)
    voice_alert_generated = Column(Boolean, default=False)
    alert_delivered = Column(Boolean, default=False)
    language = Column(String(10), default="en")
    worker_tag = Column(String(50), default="Worker-Anonymous") # Anonymized tag (no biometric/PII)
    zone_name = Column(String(100), default="General Worksite")

    def to_dict(self):
        return {
            "id": self.id,
            "event_uuid": self.event_uuid,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "violation_type": self.violation_type,
            "category": self.category,
            "severity": self.severity,
            "confidence": round(self.confidence, 3),
            "recommendation": self.recommendation,
            "voice_alert_generated": self.voice_alert_generated,
            "alert_delivered": self.alert_delivered,
            "language": self.language,
            "worker_tag": self.worker_tag,
            "zone_name": self.zone_name,
        }

class SafetyRule(Base):
    __tablename__ = "safety_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_code = Column(String(50), unique=True, index=True)
    rule_name = Column(String(120), nullable=False)
    category = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False, default="HIGH")
    is_enabled = Column(Boolean, default=True)
    description = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "rule_code": self.rule_code,
            "rule_name": self.rule_name,
            "category": self.category,
            "severity": self.severity,
            "is_enabled": self.is_enabled,
            "description": self.description,
        }

class SystemConfig(Base):
    __tablename__ = "system_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(80), unique=True, index=True)
    config_value = Column(String(255), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class PrivacyAuditLog(Base):
    """
    Audit log tracking local data management and ensuring zero raw video leak.
    """
    __tablename__ = "privacy_audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    status = Column(String(20), default="COMPLIANT")
