import time
import threading
import cv2
import numpy as np
import logging

from camera.frame_capture import FrameCapture
from preprocessing.image_processor import ImageProcessor
from ai.detector import SafetyDetector
from safety.violation_analyzer import ViolationAnalyzer
from alerts.alert_manager import AlertManager
from config import settings

logger = logging.getLogger("construction_safety.pipeline")

class VideoProcessor:
    _instance = None

    def __init__(self):
        self.is_monitoring = False
        self.source = settings.DEFAULT_CAMERA_INDEX
        self.language = settings.DEFAULT_LANGUAGE
        self.camera = None
        self.detector = SafetyDetector()
        self.analyzer = ViolationAnalyzer()
        self.alert_manager = AlertManager.get_instance()

        self._thread = None
        self._lock = threading.Lock()
        self._current_frame_bytes = None
        self._latest_detection_results = {
            "workers": [],
            "equipment": [],
            "violations": [],
            "inference_time_ms": 0.0,
            "fps": 0.0,
            "camera_connected": False,
            "monitoring_active": False,
            "is_synthetic": True
        }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = VideoProcessor()
        return cls._instance

    def start_monitoring(self, source=None, language="en"):
        with self._lock:
            if self.is_monitoring:
                return {"status": "already_running", "message": "Monitoring is already active."}

            if source is not None:
                self.source = source
            self.language = language or self.language
            self.camera = FrameCapture(source=self.source)
            self.is_monitoring = True
            self._thread = threading.Thread(target=self._processing_loop, daemon=True)
            self._thread.start()
            logger.info("Local Edge Safety Monitoring started.")
            return {"status": "started", "source": str(self.source), "language": self.language}

    def stop_monitoring(self):
        with self._lock:
            if not self.is_monitoring:
                return {"status": "stopped", "message": "Monitoring is not running."}
            self.is_monitoring = False

        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

        if self.camera:
            self.camera.release()
            self.camera = None

        logger.info("Local Edge Safety Monitoring stopped.")
        return {"status": "stopped"}

    def get_status(self) -> dict:
        with self._lock:
            return {
                "monitoring_active": self.is_monitoring,
                "camera_connected": self.camera is not None,
                "source": str(self.source),
                "language": self.language,
                "is_synthetic": self.camera.is_synthetic if self.camera else True,
                "latest_stats": self._latest_detection_results
            }

    def get_latest_frame_bytes(self) -> bytes | None:
        with self._lock:
            return self._current_frame_bytes

    def _processing_loop(self):
        """
        Core Edge Processing Loop as specified in Flowchart (Figure 2):
        Capture -> Preprocess -> AI Analysis -> Violation Check -> Alerts/Recommendations/Voice -> Annotate
        """
        prev_time = time.time()

        while self.is_monitoring:
            loop_start = time.time()
            success, raw_frame = self.camera.read_frame()
            if not success or raw_frame is None:
                time.sleep(0.05)
                continue

            # 1. Image Preprocessing (Contrast enhancement for outdoor lighting)
            enhanced = ImageProcessor.enhance_contrast(raw_frame)

            # 2. AI-Based Analysis (Worker and PPE Detection)
            detection_res = self.detector.detect(enhanced)
            workers = detection_res["workers"]
            equipment = detection_res["equipment"]
            fw, fh = detection_res["frame_width"], detection_res["frame_height"]

            # 3. Safety Violation Analysis
            updated_workers, violations = self.analyzer.analyze(
                workers=workers,
                restricted_zones=settings.RESTRICTED_ZONE_COORDS,
                frame_width=fw,
                frame_height=fh,
                language=self.language
            )

            # 4. Process Violations (Voice Alert + DB Record + Alert Queue)
            dispatched = self.alert_manager.process_violations(violations, language=self.language)

            # 5. Privacy Safeguard: Mask worker faces before visualization
            if settings.BLUR_FACES_IN_EVENTS:
                viz_frame = ImageProcessor.apply_privacy_face_blur(enhanced, updated_workers)
            else:
                viz_frame = enhanced

            # 6. Safety Annotations Overlay
            annotated = ImageProcessor.draw_safety_annotations(
                viz_frame,
                workers=updated_workers,
                equipment=equipment,
                violations=violations,
                restricted_zones=settings.RESTRICTED_ZONE_COORDS
            )

            # 7. Calculate FPS
            now = time.time()
            fps = 1.0 / max(0.001, (now - prev_time))
            prev_time = now

            cv2.putText(
                annotated, f"FPS: {fps:.1f} | Latency: {detection_res['inference_time_ms']:.1f}ms",
                (fw - 260, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2
            )

            # 8. Encode JPEG for browser streaming
            ret, jpeg = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                with self._lock:
                    self._current_frame_bytes = jpeg.tobytes()
                    self._latest_detection_results = {
                        "workers": updated_workers,
                        "equipment": equipment,
                        "violations": violations,
                        "dispatched_alerts": dispatched,
                        "inference_time_ms": detection_res["inference_time_ms"],
                        "fps": round(fps, 1),
                        "camera_connected": True,
                        "monitoring_active": True,
                        "is_synthetic": self.camera.is_synthetic if self.camera else True
                    }

            # Target ~15 FPS edge processing pacing
            elapsed = time.time() - loop_start
            sleep_time = max(0.01, (1.0 / settings.TARGET_FPS) - elapsed)
            time.sleep(sleep_time)
