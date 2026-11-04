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
    MODEL_PATH: str = str(_MODELS_DIR / "yolov8n.pt")
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

settings = Settings()
