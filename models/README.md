# AI Model Specifications & Edge Deployment Architecture

## 1. Required Detection Classes
For comprehensive construction workspace safety enforcement according to OSHA and EN 397 / EN ISO 20471:
- `worker` / `person` (Worker boundary)
- `safety_helmet` / `hard_hat` (Compliant head protection)
- `no_helmet` (Direct negative violation class)
- `safety_vest` (High-visibility reflective vest)
- `no_vest` (Direct negative violation class)
- `machinery` / `restricted_zone` (Hazardous equipment boundary)

## 2. Pretrained Model vs. Real Construction Constraints
- Standard generic models (e.g., standard COCO pretrained YOLOv8n) only contain `person` (class ID 0) among 80 generic consumer classes. **COCO does NOT natively recognize safety helmets or reflective vests.**
- In this project, we implement a **Dual-Mode Edge Architecture**:
  1. **Hybrid Edge Mode (Default Active)**:
     - Detects `person` coordinates with YOLOv8n.
     - Performs deterministic spatial chromaticity and geometric ROI verification on upper head zone (top 25%) and torso zone (25%-70%) using adaptive CLAHE + HSV color-space thresholding (fluorescent yellow, orange, white hard-hats, silver retro-reflective tape).
  2. **Custom Fine-Tuned PPE YOLOv8 Mode**:
     - When `models/construction_ppe_yolov8.pt` is present, the system directly switches to the fine-tuned 5-class detector without requiring heuristic spatial checks.

## 3. Dataset Requirements
To train the specialized PPE model, use established benchmark datasets:
- **SHWD (Safety Helmet Wearing Dataset)**: 7,581 annotated images with hard-hat and head annotations.
- **Pictor-v3 Construction Safety Dataset**: Multi-angle, varied lighting construction site worker poses.
- **Roboflow Construction Site Safety (CSS) Dataset**: 2,800+ annotated worksite images with `hard_hat`, `vest`, `mask`, `gloves`.

## 4. Annotation Format
YOLO standard format (`<class_id> <x_center> <y_center> <width> <height>` normalized 0.0 - 1.0):
```
0 0.485 0.520 0.210 0.640   # worker
1 0.482 0.225 0.120 0.110   # safety_helmet
2 0.488 0.410 0.190 0.320   # safety_vest
```

## 5. Model Export for Raspberry Pi Edge Hardware
- PyTorch `.pt` -> ONNX (`opset=12`)
- ONNX -> NCNN or TFLite INT8 Quantization
- Runs inference via OpenCV DNN (`cv2.dnn.readNetFromONNX`) with zero PyTorch overhead on Raspberry Pi OS 64-bit (Debian Bookworm).
