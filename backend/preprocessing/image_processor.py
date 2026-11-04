import cv2
import numpy as np

class ImageProcessor:
    @staticmethod
    def enhance_contrast(image: np.ndarray) -> np.ndarray:
        """
        Enhance image contrast using Contrast Limited Adaptive Histogram Equalization (CLAHE).
        Supports robust detection across varying outdoor construction lighting conditions.
        """
        if image is None or image.size == 0:
            return image
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    @staticmethod
    def resize_for_inference(image: np.ndarray, target_size: int = 640) -> tuple[np.ndarray, float, tuple[int, int]]:
        """
        Resize image with aspect ratio preservation and letterboxing for YOLO inference.
        Returns: (processed_image, scale_factor, (pad_w, pad_h))
        """
        h, w = image.shape[:2]
        scale = min(target_size / h, target_size / w)
        nh, nw = int(h * scale), int(w * scale)
        resized = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_LINEAR)

        top = (target_size - nh) // 2
        bottom = target_size - nh - top
        left = (target_size - nw) // 2
        right = target_size - nw - left

        padded = cv2.copyMakeBorder(
            resized, top, bottom, left, right,
            cv2.BORDER_CONSTANT, value=(114, 114, 114)
        )
        return padded, scale, (left, top)

    @staticmethod
    def apply_privacy_face_blur(image: np.ndarray, worker_boxes: list[dict]) -> np.ndarray:
        """
        Privacy preserving safeguard: Blurs upper-face region of detected workers.
        Ensures worker identity is protected and no identifiable facial biometrics are exposed.
        """
        if image is None:
            return image
        output = image.copy()
        img_h, img_w = output.shape[:2]

        for w in worker_boxes:
            box = w.get("box", {})
            x1 = max(0, int(box.get("x1", 0)))
            y1 = max(0, int(box.get("y1", 0)))
            x2 = min(img_w, int(box.get("x2", 0)))
            y2 = min(img_h, int(box.get("y2", 0)))

            if x2 > x1 and y2 > y1:
                # Estimate facial / head region (top 25% of worker bounding box)
                head_y2 = y1 + int((y2 - y1) * 0.28)
                face_roi = output[y1:head_y2, x1:x2]
                if face_roi.size > 0:
                    ksize = max(15, (face_roi.shape[1] // 3) | 1)
                    blurred = cv2.GaussianBlur(face_roi, (ksize, ksize), 30)
                    output[y1:head_y2, x1:x2] = blurred

        return output

    @staticmethod
    def draw_safety_annotations(
        image: np.ndarray,
        workers: list[dict],
        equipment: list[dict],
        violations: list[dict],
        restricted_zones: list[dict]
    ) -> np.ndarray:
        """
        Draws professional industrial safety overlays:
        - Red zones for restricted hazards
        - Orange/Red bounding boxes for safety violations
        - Green bounding boxes for compliant workers
        """
        if image is None:
            return image
        canvas = image.copy()
        img_h, img_w = canvas.shape[:2]

        # 1. Overlay Restricted Zones
        for rz in restricted_zones:
            x1 = int(rz["x1"] * img_w)
            y1 = int(rz["y1"] * img_h)
            x2 = int(rz["x2"] * img_w)
            y2 = int(rz["y2"] * img_h)

            overlay = canvas.copy()
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 220), -1)
            cv2.addWeighted(overlay, 0.25, canvas, 0.75, 0, canvas)
            cv2.rectangle(canvas, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(
                canvas, f"HAZARD ZONE: {rz.get('name', 'Restricted')}",
                (x1 + 8, y1 + 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2
            )

        # 2. Draw Equipment (Helmets & Vests)
        for eq in equipment:
            box = eq.get("box", {})
            bx1, by1, bx2, by2 = int(box["x1"]), int(box["y1"]), int(box["x2"]), int(box["y2"])
            label = eq.get("class_name", "Equipment")
            conf = eq.get("confidence", 0.0)
            color = (0, 200, 100) if "helmet" in label.lower() else (255, 170, 0)
            cv2.rectangle(canvas, (bx1, by1), (bx2, by2), color, 2)
            cv2.putText(
                canvas, f"{label} {int(conf*100)}%",
                (bx1, max(15, by1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1
            )

        # 3. Draw Workers and Violation Tags
        for w in workers:
            box = w.get("box", {})
            bx1, by1, bx2, by2 = int(box["x1"]), int(box["y1"]), int(box["x2"]), int(box["y2"])
            w_id = w.get("worker_id", "Worker")
            w_violations = w.get("violations", [])

            if len(w_violations) > 0:
                color = (0, 0, 230) # Red violation
                status_txt = f"{w_id}: VIOLATION ({', '.join(w_violations)})"
            else:
                color = (0, 210, 0) # Green compliant
                status_txt = f"{w_id}: COMPLIANT"

            cv2.rectangle(canvas, (bx1, by1), (bx2, by2), color, 2)

            # Draw tag background
            (tw, th), _ = cv2.getTextSize(status_txt, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(canvas, (bx1, max(0, by1 - 25)), (bx1 + tw + 10, by1), color, -1)
            cv2.putText(
                canvas, status_txt,
                (bx1 + 5, max(15, by1 - 7)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
            )

        return canvas
