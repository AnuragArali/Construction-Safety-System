import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import pytest
import cv2
import numpy as np
from fastapi.testclient import TestClient

from main import app
from database.db import init_db, SessionLocal
from database.event_repository import EventRepository
from safety.recommendations import RecommendationEngine
from safety.violation_analyzer import ViolationAnalyzer
from privacy.privacy_manager import PrivacyManager
from preprocessing.image_processor import ImageProcessor
from camera.frame_capture import FrameCapture
from ai.detector import SafetyDetector

client = TestClient(app)

def test_system_startup_and_status():
    init_db()
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "system_name" in data
    assert data["privacy"]["status"] == "COMPLIANT"

def test_privacy_compliance_verification():
    compliance = PrivacyManager.verify_privacy_compliance()
    assert compliance["status"] == "COMPLIANT"
    assert compliance["continuous_video_upload_blocked"] is True
    assert compliance["raw_video_storage_disabled"] is True
    assert compliance["worker_facial_blur_active"] is True

def test_recommendation_engine_multilingual():
    for lang in ["en", "hi", "kn", "es"]:
        rec = RecommendationEngine.get_recommendation("MISSING_HELMET", lang)
        assert "alert" in rec
        assert "recommendation" in rec
        assert "voice" in rec
        assert len(rec["recommendation"]) > 5

def test_image_preprocessing():
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    enhanced = ImageProcessor.enhance_contrast(dummy)
    assert enhanced.shape == (480, 640, 3)

    padded, scale, (pad_w, pad_h) = ImageProcessor.resize_for_inference(dummy, 640)
    assert padded.shape == (640, 640, 3)

def test_synthetic_camera_capture():
    cap = FrameCapture(source="synthetic")
    ret, frame = cap.read_frame()
    assert ret is True
    assert frame is not None
    assert frame.shape == (480, 640, 3)
    cap.release()

def test_violation_analyzer_and_debounce():
    analyzer = ViolationAnalyzer()
    dummy_workers = [{
        "worker_id": "Worker-1",
        "box": {"x1": 100, "y1": 100, "x2": 200, "y2": 300},
        "has_helmet": False,
        "has_vest": False,
        "confidence": 0.90
    }]
    zones = []

    # First call: triggers alerts
    w_updated, violations = analyzer.analyze(dummy_workers, zones, 640, 480, "en", cooldown_seconds=5.0)
    assert len(violations) >= 2
    assert any(v["violation_type"] == "MISSING_HELMET" and v["trigger_alert"] for v in violations)

    # Immediate second call: alert should be debounced (trigger_alert == False)
    w_updated2, violations2 = analyzer.analyze(dummy_workers, zones, 640, 480, "en", cooldown_seconds=5.0)
    helmet_v2 = next(v for v in violations2 if v["violation_type"] == "MISSING_HELMET")
    assert helmet_v2["trigger_alert"] is False

def test_database_events_and_stats():
    db = SessionLocal()
    try:
        ev = EventRepository.create_safety_event(db, {
            "violation_type": "MISSING_HELMET",
            "category": "PPE",
            "severity": "HIGH",
            "confidence": 0.92,
            "recommendation": "Put on hard hat",
            "voice_alert_generated": True,
            "alert_delivered": True,
            "worker_tag": "Worker-Test"
        })
        assert ev.id is not None

        stats = EventRepository.get_statistics(db)
        assert stats["total_events"] >= 1
        assert "MISSING_HELMET" in stats["by_type"]
    finally:
        db.close()

def test_api_endpoints():
    # Test rules
    res = client.get("/api/rules")
    assert res.status_code == 200
    assert len(res.json()) >= 2

    # Test recommendations
    res = client.get("/api/recommendations?language=en")
    assert res.status_code == 200
    assert "ppe_requirements" in res.json()

    # Test events list
    res = client.get("/api/events?limit=5")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # Test statistics
    res = client.get("/api/events/statistics")
    assert res.status_code == 200
    assert "compliance_rate" in res.json()

def test_yolo11_model_loading_and_detection():
    detector = SafetyDetector()
    assert detector.model is not None
    assert "YOLO11" in detector.model_type or "YOLO" in detector.model_type

    # Test detection on synthetic blank frame
    dummy = np.zeros((480, 640, 3), dtype=np.uint8)
    res = detector.detect(dummy)
    assert "workers" in res
    assert "equipment" in res
    assert "inference_time_ms" in res
    assert res["frame_width"] == 640
    assert res["frame_height"] == 480

def test_fingerprint_biometrics():
    from biometrics.fingerprint_manager import FingerprintManager
    fprint_mgr = FingerprintManager.get_instance()
    status = fprint_mgr.get_status()
    assert "operating_mode" in status
    assert "enrolled_fingerprints" in status
    assert status["max_capacity"] >= 300

    # Test verification via simulated scan of enrolled worker W-101
    scan = fprint_mgr.verify_fingerprint(simulated_worker_id="W-101")
    assert scan["matched"] is True
    assert scan["worker_id"] == "W-101"
    assert scan["confidence"] >= 0.70

    # Test API endpoint
    res = client.get("/api/biometrics/status")
    assert res.status_code == 200
    assert "fingerprint" in res.json()
    assert "doorway_checkpoint" in res.json()

def test_face_recognition_embedding():
    from biometrics.face_recognizer import FaceRecognizer
    recognizer = FaceRecognizer.get_instance()
    
    # Create synthetic test face image
    dummy_face = np.full((120, 100, 3), 180, dtype=np.uint8)
    # Draw simple facial features (eyes, mouth)
    cv2.circle(dummy_face, (35, 45), 6, (40, 40, 40), -1)
    cv2.circle(dummy_face, (65, 45), 6, (40, 40, 40), -1)
    cv2.ellipse(dummy_face, (50, 80), (18, 8), 0, 0, 180, (50, 50, 50), 2)

    emb = recognizer.compute_embedding(dummy_face)
    assert len(emb) == 128
    # Embedding must be unit normalized
    norm = np.linalg.norm(np.array(emb, dtype=np.float32))
    assert abs(norm - 1.0) < 0.05

def test_doorway_checkpoint_evaluation():
    from biometrics.doorway_controller import DoorwayController
    controller = DoorwayController.get_instance()

    # Scenario 1: Compliant worker (W-101 Rajesh Kumar) -> Access Granted
    res_granted = controller.run_demo_scenario("compliant_worker")
    assert res_granted["access_decision"] == "GRANTED"
    assert res_granted["turnstile_unlocked"] is True
    assert res_granted["ppe_check"]["compliant"] is True

    # Scenario 2: Non-compliant worker (W-102 Amit Sharma - Missing Helmet) -> Access Denied PPE Violation
    res_denied_ppe = controller.run_demo_scenario("non_compliant_worker")
    assert res_denied_ppe["access_decision"] == "DENIED"
    assert res_denied_ppe["status_code"] == "DENIED_PPE_VIOLATION"
    assert res_denied_ppe["turnstile_unlocked"] is False
    assert res_denied_ppe["ppe_check"]["compliant"] is False

    # Scenario 3: Unknown worker -> Biometric Fail
    res_denied_bio = controller.run_demo_scenario("unregistered_worker")
    assert res_denied_bio["access_decision"] == "DENIED"
    assert res_denied_bio["status_code"] == "DENIED_BIOMETRIC_FAIL"
    assert res_denied_bio["turnstile_unlocked"] is False

    # Test Checkpoint REST APIs
    api_verify = client.post("/api/checkpoint/verify", json={"scenario_key": "compliant_worker"})
    assert api_verify.status_code == 200
    assert api_verify.json()["access_decision"] == "GRANTED"

    api_logs = client.get("/api/checkpoint/logs")
    assert api_logs.status_code == 200
    assert len(api_logs.json()) >= 1

    api_stats = client.get("/api/checkpoint/stats")
    assert api_stats.status_code == 200
    assert "total_checkpoints_logged" in api_stats.json()
