from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class MonitoringControlRequest(BaseModel):
    source: Optional[str] = Field("0", description="Camera index or uploaded video path")
    language: Optional[str] = Field("en", description="Voice alert language (en, hi, kn, es)")

class MonitoringControlResponse(BaseModel):
    status: str
    message: Optional[str] = None
    source: Optional[str] = None
    language: Optional[str] = None

class SafetyEventResponse(BaseModel):
    id: int
    event_uuid: str
    timestamp: Optional[str]
    violation_type: str
    category: str
    severity: str
    confidence: float
    recommendation: str
    voice_alert_generated: bool
    alert_delivered: bool
    language: str
    worker_tag: str
    zone_name: str

class SafetyStatisticsResponse(BaseModel):
    total_events: int
    today_violations: int
    compliance_rate: float
    by_type: Dict[str, int]
    by_severity: Dict[str, int]
    daily_trends: List[Dict[str, Any]]

class RuleResponse(BaseModel):
    id: int
    rule_code: str
    rule_name: str
    category: str
    severity: str
    is_enabled: bool
    description: Optional[str]

class RuleToggleRequest(BaseModel):
    rule_code: str
    is_enabled: bool

class LanguageConfigRequest(BaseModel):
    language: str

class SettingsUpdateRequest(BaseModel):
    voice_enabled: Optional[bool] = None
    language: Optional[str] = None
    alert_cooldown: Optional[float] = None
    retention_days: Optional[int] = None
    target_fps: Optional[int] = None

class PrivacyComplianceResponse(BaseModel):
    status: str
    local_first_processing: bool
    continuous_video_upload_blocked: bool
    raw_video_storage_disabled: bool
    worker_facial_blur_active: bool
    data_retention_days: int
    database_type: str
    compliance_score: int
    issues: List[str]
