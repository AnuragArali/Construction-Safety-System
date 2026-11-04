import os
import shutil
import time
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session

from database.db import get_db
from database.event_repository import EventRepository
from camera.video_processor import VideoProcessor
from alerts.alert_manager import AlertManager
from safety.recommendations import RecommendationEngine
from privacy.privacy_manager import PrivacyManager
from config import settings
from api.schemas import (
    MonitoringControlRequest, MonitoringControlResponse,
    SafetyEventResponse, SafetyStatisticsResponse,
    RuleResponse, RuleToggleRequest, LanguageConfigRequest,
    SettingsUpdateRequest, PrivacyComplianceResponse
)

router = APIRouter(prefix="/api")

@router.get("/status")
def get_system_status():
    processor = VideoProcessor.get_instance()
    status_info = processor.get_status()
    privacy_info = PrivacyManager.verify_privacy_compliance()

    return {
        "system_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "is_edge_device": settings.IS_EDGE_DEVICE,
        "monitoring": status_info,
        "privacy": privacy_info,
        "supported_languages": settings.SUPPORTED_LANGUAGES,
        "current_language": processor.language,
        "timestamp": time.time()
    }

@router.post("/monitoring/start", response_model=MonitoringControlResponse)
def start_monitoring(payload: MonitoringControlRequest):
    processor = VideoProcessor.get_instance()
    source_val = payload.source if payload.source is not None else settings.DEFAULT_CAMERA_INDEX
    # If source is numeric string, convert to int
    if isinstance(source_val, str) and source_val.isdigit():
        source_val = int(source_val)

    res = processor.start_monitoring(source=source_val, language=payload.language or "en")
    return res

@router.post("/monitoring/stop", response_model=MonitoringControlResponse)
def stop_monitoring():
    processor = VideoProcessor.get_instance()
    res = processor.stop_monitoring()
    return res

@router.get("/monitoring/detections")
def get_latest_detections():
    processor = VideoProcessor.get_instance()
    with processor._lock:
        return processor._latest_detection_results

@router.get("/monitoring/stream")
def video_stream():
    """
    MJPEG streaming endpoint for live preview with safety overlays.
    Direct edge device to browser socket; no cloud server hop.
    """
    processor = VideoProcessor.get_instance()

    def frame_generator():
        while True:
            frame_bytes = processor.get_latest_frame_bytes()
            if frame_bytes is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(1.0 / settings.TARGET_FPS)

    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@router.post("/upload/video")
async def upload_sample_video(file: UploadFile = File(...)):
    """
    Allows uploading test construction clips to benchmark edge detection.
    """
    allowed_exts = {".mp4", ".avi", ".mov", ".mkv"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail=f"Invalid video extension. Allowed: {allowed_exts}")

    dest_path = settings.UPLOADS_DIR / f"test_{int(time.time())}_{file.filename}"
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": str(dest_path),
        "message": "Video uploaded successfully. You can now select it for monitoring."
    }

@router.get("/alerts/latest", response_model=list[SafetyEventResponse])
def get_latest_alerts(limit: int = 8, db: Session = Depends(get_db)):
    events = EventRepository.get_latest_alerts(db, limit=limit)
    return [e.to_dict() for e in events]

@router.get("/events", response_model=list[SafetyEventResponse])
def get_safety_events(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    violation_type: str | None = None,
    severity: str | None = None,
    category: str | None = None,
    db: Session = Depends(get_db)
):
    events = EventRepository.get_events(
        db, limit=limit, offset=offset,
        violation_type=violation_type, severity=severity, category=category
    )
    return [e.to_dict() for e in events]

@router.get("/events/statistics", response_model=SafetyStatisticsResponse)
def get_safety_statistics(db: Session = Depends(get_db)):
    stats = EventRepository.get_statistics(db)
    return stats

@router.get("/rules", response_model=list[RuleResponse])
def get_safety_rules(db: Session = Depends(get_db)):
    rules = EventRepository.get_rules(db)
    return [r.to_dict() for r in rules]

@router.post("/rules/toggle", response_model=RuleResponse)
def toggle_safety_rule(payload: RuleToggleRequest, db: Session = Depends(get_db)):
    updated = EventRepository.toggle_rule(db, payload.rule_code, payload.is_enabled)
    if not updated:
        raise HTTPException(status_code=404, detail="Safety rule not found")
    return updated.to_dict()

@router.get("/recommendations")
def get_recommendations(language: str = "en"):
    lang = language if language in settings.SUPPORTED_LANGUAGES else "en"
    guidelines = {
        "ppe_requirements": [
            {
                "equipment": "Hard Hat / Safety Helmet",
                "standard": "ANSI/ISEA Z89.1 / EN 397",
                "purpose": "Shields against falling tools, overhead collisions, and electrical hazards.",
                "mandatory_areas": "All active construction zones and scaffolding perimeters."
            },
            {
                "equipment": "High-Visibility Reflective Vest",
                "standard": "ANSI/ISEA 107 Class 2/3 / EN ISO 20471",
                "purpose": "Provides 360-degree high-contrast optical conspicuity for machine operators.",
                "mandatory_areas": "Roadwork, crane swing radiuses, and transport corridors."
            },
            {
                "equipment": "Hazard Exclusion Perimeter",
                "standard": "OSHA 1926 Heavy Equipment Boundaries",
                "purpose": "Prohibits unauthorized personnel inside active heavy equipment operation zones.",
                "mandatory_areas": "Excavator radiuses, suspended loads, and trench margins."
            }
        ],
        "corrective_actions": {
            "MISSING_HELMET": RecommendationEngine.get_recommendation("MISSING_HELMET", lang),
            "MISSING_VEST": RecommendationEngine.get_recommendation("MISSING_VEST", lang),
            "RESTRICTED_ZONE_INTRUSION": RecommendationEngine.get_recommendation("RESTRICTED_ZONE_INTRUSION", lang),
        }
    }
    return guidelines

@router.get("/privacy/compliance", response_model=PrivacyComplianceResponse)
def get_privacy_compliance():
    return PrivacyManager.verify_privacy_compliance()

@router.post("/privacy/purge")
def purge_expired_records(days: int = Query(None), db: Session = Depends(get_db)):
    purged_count = PrivacyManager.enforce_retention_policy(days)
    return {"status": "purged", "records_removed": purged_count}

@router.get("/settings")
def get_settings():
    processor = VideoProcessor.get_instance()
    return {
        "voice_enabled": settings.VOICE_ENABLED,
        "language": processor.language,
        "supported_languages": settings.SUPPORTED_LANGUAGES,
        "alert_cooldown": settings.ALERT_COOLDOWN_SECONDS,
        "retention_days": settings.DATA_RETENTION_DAYS,
        "target_fps": settings.TARGET_FPS,
        "detection_confidence": settings.DETECTION_CONFIDENCE,
        "preserve_privacy": settings.PRESERVE_PRIVACY,
        "blur_faces": settings.BLUR_FACES_IN_EVENTS,
        "is_edge_device": settings.IS_EDGE_DEVICE
    }

@router.post("/settings")
def update_settings(payload: SettingsUpdateRequest):
    processor = VideoProcessor.get_instance()
    if payload.voice_enabled is not None:
        settings.VOICE_ENABLED = payload.voice_enabled
    if payload.language is not None and payload.language in settings.SUPPORTED_LANGUAGES:
        settings.DEFAULT_LANGUAGE = payload.language
        processor.language = payload.language
    if payload.alert_cooldown is not None:
        settings.ALERT_COOLDOWN_SECONDS = payload.alert_cooldown
    if payload.retention_days is not None:
        settings.DATA_RETENTION_DAYS = payload.retention_days
    if payload.target_fps is not None:
        settings.TARGET_FPS = payload.target_fps

    return {"status": "updated", "message": "Settings saved successfully."}
