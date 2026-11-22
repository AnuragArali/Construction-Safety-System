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


class Worker(Base):
    """
    Enrolled construction personnel directory.
    Stores biometric feature hashes and local embeddings for edge matching.
    Raw biometrics are never uploaded to any cloud server.
    """
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_id = Column(String(50), unique=True, index=True, nullable=False) # e.g. W-101
    name = Column(String(100), nullable=False)
    role = Column(String(100), default="Technician")
    department = Column(String(100), default="Construction & Framing")
    
    # Fingerprint Biometrics
    fingerprint_id = Column(Integer, unique=True, nullable=True) # Slot index 1-300 on AS608/R503 sensor
    fingerprint_enrolled = Column(Boolean, default=False)
    fingerprint_hash = Column(String(128), nullable=True) # SHA-256 hash of minutiae template
    
    # Face Recognition Biometrics (Lightweight 128-D spatial LBP / SFace embedding vector)
    face_enrolled = Column(Boolean, default=False)
    face_features = Column(Text, nullable=True) # JSON array of normalized float embedding
    photo_thumbnail = Column(Text, nullable=True) # Base64 thumbnail or URI for profile badge

    authorized_zones = Column(String(255), default="General Worksite,Doorway-North")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def to_dict(self, include_features=False):
        d = {
            "id": self.id,
            "worker_id": self.worker_id,
            "name": self.name,
            "role": self.role,
            "department": self.department,
            "fingerprint_id": self.fingerprint_id,
            "fingerprint_enrolled": self.fingerprint_enrolled,
            "face_enrolled": self.face_enrolled,
            "authorized_zones": self.authorized_zones.split(",") if self.authorized_zones else [],
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_features:
            d["face_features"] = self.face_features
            d["fingerprint_hash"] = self.fingerprint_hash
        return d


class CheckpointAccessLog(Base):
    """
    Audit log of worker authentication and PPE safety verification at mock work area / doorway.
    """
    __tablename__ = "checkpoint_access_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    checkpoint_name = Column(String(100), default="Doorway-North")
    worker_id = Column(String(50), nullable=True)
    worker_name = Column(String(100), nullable=True)
    auth_method = Column(String(50), default="FINGERPRINT+FACE") # FINGERPRINT, FACE, FINGERPRINT+FACE, MANUAL
    fingerprint_verified = Column(Boolean, default=False)
    face_verified = Column(Boolean, default=False)
    has_helmet = Column(Boolean, default=False)
    has_vest = Column(Boolean, default=False)
    access_decision = Column(String(40), nullable=False) # GRANTED, DENIED_PPE_VIOLATION, DENIED_UNAUTHORIZED, DENIED_BIOMETRIC_FAIL
    reason = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.0)
    voice_announcement = Column(String(255), nullable=True)
    gpio_pulse_sent = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "checkpoint_name": self.checkpoint_name,
            "worker_id": self.worker_id,
            "worker_name": self.worker_name,
            "auth_method": self.auth_method,
            "fingerprint_verified": self.fingerprint_verified,
            "face_verified": self.face_verified,
            "has_helmet": self.has_helmet,
            "has_vest": self.has_vest,
            "access_decision": self.access_decision,
            "reason": self.reason,
            "confidence_score": round(self.confidence_score, 3) if self.confidence_score else 0.0,
            "voice_announcement": self.voice_announcement,
            "gpio_pulse_sent": self.gpio_pulse_sent,
        }
