"""
Model Evaluation and Benchmark Script
Measures:
- Precision: TP / (TP + FP)
- Recall: TP / (TP + FN)
- F1-Score: 2PR / (P + R)
- Inference Latency (ms)
- Edge Hardware Viability
"""

import time
import json
import argparse
from pathlib import Path
import numpy as np
from ultralytics import YOLO

def evaluate(model_path: str, data_yaml: str):
    print(f"Evaluating model: {model_path} against dataset: {data_yaml}")
    model = YOLO(model_path)

    start_time = time.time()
    metrics = model.val(data=data_yaml, split="val", imgsz=640)
    eval_duration = time.time() - start_time

    precision = float(metrics.box.mp)
    recall = float(metrics.box.mr)
    f1 = float(2 * (precision * recall) / max(1e-6, precision + recall))
    map50 = float(metrics.box.map50)
    map50_95 = float(metrics.box.map)

    # Measure raw single-frame inference latency over 20 repeated trials
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    latencies = []
    for _ in range(20):
        t0 = time.time()
        _ = model.predict(dummy_img, verbose=False)
        latencies.append((time.time() - t0) * 1000.0)

    avg_latency = float(np.mean(latencies))
    p95_latency = float(np.percentile(latencies, 95))

    report = {
        "model": model_path,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "mAP_50": round(map50, 4),
        "mAP_50_95": round(map50_95, 4),
        "avg_inference_latency_ms": round(avg_latency, 2),
        "p95_latency_ms": round(p95_latency, 2),
        "classes": list(metrics.names.values())
    }

    report_path = Path("evaluation_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print("\n--- Model Evaluation Summary ---")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1-Score:  {f1:.3f}")
    print(f"mAP@50:    {map50:.3f}")
    print(f"Avg Inference Latency: {avg_latency:.2f} ms")
    print(f"Report saved to: {report_path.resolve()}")
    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Construction PPE YOLO Model")
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="Path to model weights")
    parser.add_argument("--data", type=str, default="coco8.yaml", help="Path to dataset yaml")
    args = parser.parse_args()
    evaluate(args.model, args.data)
