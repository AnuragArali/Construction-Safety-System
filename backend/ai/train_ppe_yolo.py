"""
Construction PPE Detection Model Training Script
Trains a custom YOLOv8 model for construction site PPE compliance.
"""

import os
import argparse
from pathlib import Path
import yaml
from ultralytics import YOLO

def setup_dataset_yaml(dataset_dir: str) -> str:
    yaml_path = Path(dataset_dir) / "construction_ppe.yaml"
    data_config = {
        "path": str(Path(dataset_dir).resolve()),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": {
            0: "worker",
            1: "safety_helmet",
            2: "no_helmet",
            3: "safety_vest",
            4: "no_vest"
        }
    }
    with open(yaml_path, "w") as f:
        yaml.dump(data_config, f, default_flow_style=False)
    return str(yaml_path)

def train(dataset_dir: str, epochs: int = 50, batch_size: int = 16, imgsz: int = 640):
    yaml_config = setup_dataset_yaml(dataset_dir)
    print(f"Dataset config written to {yaml_config}")

    # Initialize pretrained YOLOv8 nano edge backbone
    model = YOLO("yolov8n.pt")

    print("Beginning fine-tuning on construction PPE dataset...")
    results = model.train(
        data=yaml_config,
        epochs=epochs,
        batch=batch_size,
        imgsz=imgsz,
        patience=10,
        device="cpu", # Change to 0 for CUDA GPU
        save=True,
        project="runs/construction_ppe",
        name="edge_model_v1"
    )
    print("Training complete. Best model weights saved at: runs/construction_ppe/edge_model_v1/weights/best.pt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Construction PPE YOLO Model")
    parser.add_argument("--data", type=str, default="data/ppe_dataset", help="Path to PPE dataset folder")
    parser.add_argument("--epochs", type=int, default=30, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=8, help="Batch size")
    args = parser.parse_args()
    train(args.data, args.epochs, args.batch)
