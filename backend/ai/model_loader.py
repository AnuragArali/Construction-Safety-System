import os
import logging
from pathlib import Path
from config import settings

logger = logging.getLogger("construction_safety.ai")

class ModelLoader:
    _instance = None
    _model = None
    _model_type = "UNINITIALIZED"

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls.load_model()
        return cls._model, cls._model_type

    @classmethod
    def load_model(cls):
        model_path = Path(settings.MODEL_PATH)
        custom_ppe_model = Path(settings.MODELS_DIR) / "construction_ppe_yolov8.pt"

        # Check for custom fine-tuned PPE model first
        if custom_ppe_model.exists():
            try:
                from ultralytics import YOLO
                logger.info(f"Loading custom fine-tuned Construction PPE model: {custom_ppe_model}")
                cls._model = YOLO(str(custom_ppe_model))
                cls._model_type = "CUSTOM_PPE_YOLO"
                return cls._model, cls._model_type
            except Exception as e:
                logger.warning(f"Failed to load custom PPE model: {e}. Falling back...")

        # Load standard YOLOv8 nano edge model
        try:
            from ultralytics import YOLO
            logger.info(f"Loading standard YOLO edge model: yolov8n.pt")
            cls._model = YOLO("yolov8n.pt")
            cls._model_type = "YOLOv8_EDGE_HYBRID"
            return cls._model, cls._model_type
        except Exception as e:
            logger.error(f"Could not load YOLO model: {e}. Falling back to heuristic edge detector.")
            cls._model = None
            cls._model_type = "HEURISTIC_EDGE_DETECTOR"
            return cls._model, cls._model_type
