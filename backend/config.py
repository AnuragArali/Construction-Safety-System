import os
from pathlib import Path
from pydantic import BaseModel

_BASE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _BASE_DIR.parent
_DATA_DIR = _PROJECT_ROOT / "data"
_MODELS_DIR = _PROJECT_ROOT / "models"
_UPLOADS_DIR = _BASE_DIR / "uploads"

# Ensure directories exist
_DATA_DIR.mkdir(parents=True, exist_ok=True)
_MODELS_DIR.mkdir(parents=True, exist_ok=True)
_UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    # App & Hardware
    APP_NAME: str = "Edge-Enabled Construction Safety Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    IS_EDGE_DEVICE: bool = os.uname().sysname == "Linux" and os.path.exists("/proc/device-tree/model") if hasattr(os, "uname") else False

    # Directories
    BASE_DIR: str = str(_BASE_DIR)
    DATA_DIR: str = str(_DATA_DIR)
    MODELS_DIR: str = str(_MODELS_DIR)
    UPLOADS_DIR: str = str(_UPLOADS_DIR)

    # Server Network
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "*"]

    # Database
    DATABASE_URL: str = f"sqlite:///{_DATA_DIR / 'construction_safety.db'}"

    # AI Detection
    MODEL_PATH: str = str(_MODELS_DIR / "yolo11n.pt")
    DETECTION_CONFIDENCE: float = 0.40
    IOU_THRESHOLD: float = 0.45
    INPUT_IMAGE_SIZE: int = 640
    TARGET_FPS: int = 15

    # Camera & Video Stream
    DEFAULT_CAMERA_INDEX: int = 0
    FALLBACK_SAMPLE_VIDEO: str = str(_UPLOADS_DIR / "sample_construction.mp4")

    # Safety Rules & Debounce
    ALERT_COOLDOWN_SECONDS: float = 6.0
    RESTRICTED_ZONE_COORDS: list[dict] = [
        {"x1": 0.0, "y1": 0.65, "x2": 0.45, "y2": 1.0, "name": "Heavy Machinery Excavation Zone"}
    ]

    # Voice Alerting
    VOICE_ENABLED: bool = True
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: list[str] = ["en", "hi", "kn", "es"]
    VOICE_RATE: int = 160
    VOICE_VOLUME: float = 0.9

    # Privacy Preserving Controls
    PRESERVE_PRIVACY: bool = True
    STORE_RAW_VIDEO: bool = False  # Strictly forbidden per synopsis privacy requirement
    BLUR_FACES_IN_EVENTS: bool = True
    DATA_RETENTION_DAYS: int = 14
    ALLOW_CLOUD_STREAMING: bool = False  # Local edge only

    # Biometric Worker Authentication & Edge Fingerprint Sensor
    BIOMETRICS_ENABLED: bool = True
    FINGERPRINT_PORT: str = "/dev/serial0" if (hasattr(os, "uname") and os.uname().sysname == "Linux") else "COM3"
    FINGERPRINT_BAUDRATE: int = 57600
    FINGERPRINT_TIMEOUT: float = 1.0
    FINGERPRINT_SIMULATION_MODE: bool = False  # Auto-falls back to simulation if hardware not connected
    
    # Face Recognition (Raspberry Pi Edge Local Embeddings)
    FACE_RECOGNITION_ENABLED: bool = True
    FACE_MATCH_THRESHOLD: float = 0.70  # Cosine similarity threshold for worker verification
    FACE_ROI_SCALE: float = 0.28        # Top portion of worker bounding box containing face

    # Doorway / Mock Work Area Checkpoint Controller
    CHECKPOINT_NAME: str = "Doorway-North"
    DOORWAY_RELAY_GPIO_PIN: int = 17   # Raspberry Pi BCM Pin 17 for electronic turnstile / door latch
    DOORWAY_STATUS_LED_GREEN: int = 27 # BCM Pin 27 for Access Granted LED
    DOORWAY_STATUS_LED_RED: int = 22   # BCM Pin 22 for Access Denied LED / buzzer
    DOORWAY_UNLOCK_SECONDS: float = 4.0 # Latch hold duration
    REQUIRE_BIOMETRIC_AUTH: bool = True
    REQUIRE_PPE_FOR_ACCESS: bool = True

settings = Settings()
