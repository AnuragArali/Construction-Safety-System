import time
import math
import cv2
import numpy as np
import logging

logger = logging.getLogger("construction_safety.camera")

class FrameCapture:
    def __init__(self, source=0):
        self.source = source
        self.cap = None
        self.is_synthetic = False
        self._frame_count = 0
        self._init_source()

    def _init_source(self):
        source_str = str(self.source).strip().lower()
        if source_str in ("synthetic", "sim", "demo", "mock"):
            self.is_synthetic = True
            self.cap = None
            logger.info("Initialized Synthetic Construction Workspace Simulator.")
            return

        if isinstance(self.source, int) or (isinstance(self.source, str) and self.source.isdigit()):
            cam_idx = int(self.source)
            try:
                # Use CAP_DSHOW for rapid device check on Windows
                cap_backend = cv2.CAP_DSHOW if hasattr(cv2, "CAP_DSHOW") else cv2.CAP_ANY
                self.cap = cv2.VideoCapture(cam_idx, cap_backend)
                if not self.cap.isOpened():
                    logger.info(f"Hardware camera {cam_idx} not openable. Using synthetic workspace simulator.")
                    self.is_synthetic = True
                    self.cap = None
                else:
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    ret, test_frame = self.cap.read()
                    if not ret or test_frame is None:
                        logger.info(f"Hardware camera {cam_idx} returned blank frame. Using synthetic workspace simulator.")
                        self.is_synthetic = True
                        self.cap.release()
                        self.cap = None
                    else:
                        logger.info(f"Hardware camera {cam_idx} online and capturing.")
            except Exception as e:
                logger.warning(f"Error accessing hardware camera {cam_idx}: {e}. Falling back to synthetic.")
                self.is_synthetic = True
                self.cap = None

        elif isinstance(self.source, str) and (self.source.endswith(('.mp4', '.avi', '.mov', '.mkv'))):
            self.cap = cv2.VideoCapture(self.source)
            if not self.cap.isOpened():
                logger.warning(f"Video file {self.source} cannot be opened. Using synthetic simulator.")
                self.is_synthetic = True
                self.cap = None
            else:
                logger.info(f"Loaded video clip: {self.source}")
        else:
            self.is_synthetic = True
            self.cap = None

    def read_frame(self) -> tuple[bool, np.ndarray]:
        self._frame_count += 1
        if not self.is_synthetic and self.cap is not None:
            ret, frame = self.cap.read()
            if ret and frame is not None:
                return True, frame
            # If video reached end, loop back
            if isinstance(self.source, str) and not self.source.isdigit():
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    return True, frame

        # Synthetic Construction Workspace or Mock Doorway Checkpoint Generator
        if str(self.source).strip().lower() in ("doorway", "checkpoint", "entrance", "mock_doorway"):
            return True, self._generate_synthetic_doorway_frame()
        return True, self._generate_synthetic_construction_frame()

    def _generate_synthetic_doorway_frame(self) -> np.ndarray:
        """
        Synthesizes a realistic mock work area doorway / turnstile entry checkpoint:
        - Structural doorway portal with electronic turnstile barrier
        - Biometric scanner kiosk (Fingerprint scanner pad & Face camera)
        - Animated worker stepping up to the doorway scanner
        """
        w, h = 640, 480
        frame = np.full((h, w, 3), (220, 225, 230), dtype=np.uint8)

        # Draw indoor/entryway walls & floor
        cv2.rectangle(frame, (0, 0), (w, int(h * 0.65)), (190, 195, 205), -1) # Wall
        cv2.rectangle(frame, (0, int(h * 0.65)), (w, h), (100, 105, 115), -1) # Tiled entry floor

        # Concrete doorway frame / portal
        door_x1, door_x2 = 200, 440
        door_top = 70
        door_bottom = int(h * 0.65) + 120
        # Pillars
        cv2.rectangle(frame, (door_x1 - 35, door_top), (door_x1, door_bottom), (60, 65, 75), -1)
        cv2.rectangle(frame, (door_x2, door_top), (door_x2 + 35, door_bottom), (60, 65, 75), -1)
        # Lintel / Overhead beam
        cv2.rectangle(frame, (door_x1 - 45, door_top - 35), (door_x2 + 45, door_top), (40, 45, 55), -1)
        # Overhead doorway sign
        cv2.rectangle(frame, (door_x1 - 20, door_top - 30), (door_x2 + 20, door_top - 5), (15, 20, 30), -1)
        cv2.putText(frame, "DOORWAY CHECKPOINT - MOCK WORK AREA", (door_x1 - 10, door_top - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 220, 255), 1)

        # Entrance interior beyond doorway (construction site backdrop visible inside)
        cv2.rectangle(frame, (door_x1, door_top), (door_x2, int(h * 0.65)), (160, 175, 190), -1)
        # Distant scaffolding inside doorway
        cv2.line(frame, (door_x1 + 40, 130), (door_x1 + 40, int(h * 0.65)), (110, 115, 125), 2)
        cv2.line(frame, (door_x2 - 40, 130), (door_x2 - 40, int(h * 0.65)), (110, 115, 125), 2)
        cv2.line(frame, (door_x1 + 20, 180), (door_x2 - 20, 180), (110, 115, 125), 2)

        # Electronic Turnstile Barrier
        barrier_y = int(h * 0.65) + 20
        cv2.rectangle(frame, (door_x1 + 10, barrier_y - 25), (door_x1 + 45, barrier_y + 45), (50, 50, 60), -1)
        cv2.rectangle(frame, (door_x2 - 45, barrier_y - 25), (door_x2 - 10, barrier_y + 45), (50, 50, 60), -1)
        # Turnstile arms
        cv2.line(frame, (door_x1 + 45, barrier_y), (door_x1 + 115, barrier_y - 15), (180, 180, 190), 4)
        cv2.line(frame, (door_x2 - 45, barrier_y), (door_x2 - 115, barrier_y - 15), (180, 180, 190), 4)

        # Biometric Scanner Kiosk (Left side of doorway)
        kiosk_x = 110
        kiosk_y = 230
        cv2.rectangle(frame, (kiosk_x, kiosk_y), (kiosk_x + 35, kiosk_y + 160), (35, 40, 50), -1) # Pedestal
        cv2.rectangle(frame, (kiosk_x - 8, kiosk_y - 30), (kiosk_x + 43, kiosk_y), (25, 30, 40), -1) # Reader head
        # Fingerprint Scanner Pad (Glowing cyan)
        cv2.circle(frame, (kiosk_x + 10, kiosk_y - 15), 7, (230, 180, 0), -1)
        # Mini camera lens
        cv2.circle(frame, (kiosk_x + 28, kiosk_y - 15), 5, (20, 20, 20), -1)
        cv2.putText(frame, "BIOMETRIC", (kiosk_x - 14, kiosk_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (200, 200, 200), 1)
        cv2.putText(frame, "STATION", (kiosk_x - 10, kiosk_y + 32), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (200, 200, 200), 1)

        # Animated Worker approaching the doorway
        t = self._frame_count * 0.04
        worker_x = int(320 + 20 * math.sin(t * 0.8))
        worker_y = 210

        # Body with High-Vis Safety Vest
        cv2.rectangle(frame, (worker_x - 22, worker_y + 40), (worker_x + 22, worker_y + 110), (30, 220, 210), -1)
        cv2.rectangle(frame, (worker_x - 16, worker_y + 60), (worker_x + 16, worker_y + 90), (200, 200, 200), 2)
        # Legs
        cv2.rectangle(frame, (worker_x - 18, worker_y + 110), (worker_x - 5, worker_y + 165), (55, 60, 70), -1)
        cv2.rectangle(frame, (worker_x + 5, worker_y + 110), (worker_x + 18, worker_y + 165), (55, 60, 70), -1)
        # Head & Yellow Helmet
        cv2.circle(frame, (worker_x, worker_y + 20), 16, (140, 170, 210), -1) # Head skin
        cv2.ellipse(frame, (worker_x, worker_y + 14), (18, 12), 0, 180, 360, (0, 220, 255), -1) # Yellow Hard hat
        cv2.rectangle(frame, (worker_x - 20, worker_y + 12), (worker_x + 20, worker_y + 16), (0, 200, 240), -1)

        # Status text overlay
        cv2.putText(frame, "CAM-02 [DOORWAY CHECKPOINT - RASPBERRY PI EDGE]", (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 2)
        cv2.putText(frame, "ACCESS CONTROL: FINGERPRINT + FACE + YOLO11 PPE VERIFICATION", (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 120, 0), 1)

        return frame

    def _generate_synthetic_construction_frame(self) -> np.ndarray:
        """
        Synthesizes a realistic construction site scene:
        - Worksite background with scaffolding and safety barriers
        - Multiple animated workers walking through zones:
          - Worker 1: Safe worker with yellow hard hat and high-vis vest
          - Worker 2: Safe worker with white helmet and orange vest
          - Worker 3: Unsafe worker with missing helmet and missing vest
        """
        w, h = 640, 480
        frame = np.full((h, w, 3), (210, 215, 220), dtype=np.uint8)

        # Draw construction sky / ground
        cv2.rectangle(frame, (0, 0), (w, int(h * 0.4)), (220, 200, 180), -1) # Sky/Distance
        cv2.rectangle(frame, (0, int(h * 0.4)), (w, h), (130, 140, 150), -1) # Concrete ground

        # Construction scaffold structure
        for x in range(40, w, 90):
            cv2.line(frame, (x, 80), (x, int(h * 0.7)), (80, 80, 90), 3)
        cv2.line(frame, (30, 140), (w - 30, 140), (80, 80, 90), 3)
        cv2.line(frame, (30, 210), (w - 30, 210), (80, 80, 90), 3)

        # Scaffold diagonal braces
        for x in range(40, w - 90, 90):
            cv2.line(frame, (x, 140), (x + 90, 210), (90, 90, 100), 2)
            cv2.line(frame, (x + 90, 140), (x, 210), (90, 90, 100), 2)

        # Oscillating worker positions based on frame count
        t = self._frame_count * 0.04

        # Worker 1: COMPLIANT WORKER (Has yellow helmet & high-vis green vest)
        w1_x = int(120 + 25 * math.sin(t))
        w1_y = 220
        # Body
        cv2.rectangle(frame, (w1_x - 20, w1_y + 40), (w1_x + 20, w1_y + 110), (30, 215, 200), -1) # High-vis lime vest
        cv2.rectangle(frame, (w1_x - 14, w1_y + 60), (w1_x + 14, w1_y + 90), (190, 190, 190), 2) # Silver reflective stripe
        # Legs
        cv2.rectangle(frame, (w1_x - 16, w1_y + 110), (w1_x - 4, w1_y + 160), (60, 60, 70), -1)
        cv2.rectangle(frame, (w1_x + 4, w1_y + 110), (w1_x + 16, w1_y + 160), (60, 60, 70), -1)
        # Head & Yellow Helmet
        cv2.circle(frame, (w1_x, w1_y + 20), 16, (140, 170, 210), -1) # Head skin
        cv2.ellipse(frame, (w1_x, w1_y + 14), (18, 12), 0, 180, 360, (0, 220, 255), -1) # Yellow Hard hat
        cv2.rectangle(frame, (w1_x - 20, w1_y + 12), (w1_x + 20, w1_y + 16), (0, 200, 240), -1) # Helmet brim

        # Worker 2: COMPLIANT WORKER (Has white helmet & orange vest)
        w2_x = int(240 + 30 * math.sin(t * 0.7))
        w2_y = 210
        # Body
        cv2.rectangle(frame, (w2_x - 20, w2_y + 40), (w2_x + 20, w2_y + 110), (20, 140, 240), -1) # Orange vest
        cv2.rectangle(frame, (w2_x - 14, w2_y + 60), (w2_x + 14, w2_y + 90), (190, 190, 190), 2)
        # Legs
        cv2.rectangle(frame, (w2_x - 16, w2_y + 110), (w2_x - 4, w2_y + 160), (50, 50, 60), -1)
        cv2.rectangle(frame, (w2_x + 4, w2_y + 110), (w2_x + 16, w2_y + 160), (50, 50, 60), -1)
        # White Helmet
        cv2.circle(frame, (w2_x, w2_y + 20), 16, (140, 170, 210), -1)
        cv2.ellipse(frame, (w2_x, w2_y + 14), (18, 12), 0, 180, 360, (245, 245, 245), -1)

        # Worker 3: VIOLATION WORKER (Missing helmet - dark hair; Missing vest - plain dark blue shirt)
        w3_x = int(380 + 35 * math.cos(t * 0.8))
        w3_y = 200
        # Plain Blue Shirt (NO VEST)
        cv2.rectangle(frame, (w3_x - 22, w3_y + 42), (w3_x + 22, w3_y + 115), (140, 60, 40), -1)
        # Legs
        cv2.rectangle(frame, (w3_x - 18, w3_y + 115), (w3_x - 4, w3_y + 165), (50, 50, 60), -1)
        cv2.rectangle(frame, (w3_x + 4, w3_y + 115), (w3_x + 18, w3_y + 165), (50, 50, 60), -1)
        # Head with dark hair (NO HELMET)
        cv2.circle(frame, (w3_x, w3_y + 20), 16, (140, 170, 210), -1)
        cv2.ellipse(frame, (w3_x, w3_y + 12), (16, 10), 0, 180, 360, (20, 20, 25), -1) # Dark hair

        # Add timestamp & camera overlay
        cv2.putText(frame, "CAM-01 [AR/VR WORKSPACE EDGE]", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2)
        cv2.putText(frame, "LIVE LOCAL EDGE INFERENCE - NO CLOUD VIDEO TRANSMISSION", (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 120, 0), 1)

        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
