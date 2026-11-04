"""
Export YOLOv8 model to ONNX / OpenVINO / NCNN for Raspberry Pi Edge Inference.
"""

import argparse
from ultralytics import YOLO

def export_edge(model_path: str = "yolov8n.pt", format_name: str = "onnx"):
    print(f"Loading {model_path} for edge export...")
    model = YOLO(model_path)

    # Export model with static shape 640x640 suitable for OpenCV DNN
    exported_path = model.export(
        format=format_name,
        imgsz=640,
        dynamic=False,
        simplify=True
    )
    print(f"Exported successfully to: {exported_path}")
    print("This model can be loaded directly on Raspberry Pi using cv2.dnn.readNetFromONNX()")
    return exported_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export YOLO for Edge Hardware")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Model weights path")
    parser.add_argument("--format", type=str, default="onnx", choices=["onnx", "tflite", "openvino", "ncnn"])
    args = parser.parse_args()
    export_edge(args.model, args.format)
