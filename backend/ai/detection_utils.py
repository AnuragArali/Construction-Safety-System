def calculate_iou(box1: dict, box2: dict) -> float:
    """
    Computes Intersection over Union (IoU) between two bounding boxes.
    Boxes are in format: {"x1": float, "y1": float, "x2": float, "y2": float}
    """
    x_left = max(box1["x1"], box2["x1"])
    y_top = max(box1["y1"], box2["y1"])
    x_right = min(box1["x2"], box2["x2"])
    y_bottom = min(box1["y2"], box2["y2"])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    box1_area = (box1["x2"] - box1["x1"]) * (box1["y2"] - box1["y1"])
    box2_area = (box2["x2"] - box2["x1"]) * (box2["y2"] - box2["y1"])

    union_area = float(box1_area + box2_area - intersection_area)
    if union_area <= 0:
        return 0.0
    return intersection_area / union_area

def is_point_or_box_in_zone(box: dict, zone_normalized: dict, img_w: int, img_h: int) -> bool:
    """
    Checks if worker lower center (feet / standing position) or box centroid is within a restricted hazard zone.
    """
    zx1 = zone_normalized["x1"] * img_w
    zy1 = zone_normalized["y1"] * img_h
    zx2 = zone_normalized["x2"] * img_w
    zy2 = zone_normalized["y2"] * img_h

    # Worker feet anchor point (center x, bottom y)
    feet_x = (box["x1"] + box["x2"]) / 2.0
    feet_y = box["y2"]

    return (zx1 <= feet_x <= zx2) and (zy1 <= feet_y <= zy2)

def associate_ppe_to_workers(workers: list[dict], equipments: list[dict]) -> list[dict]:
    """
    Associates detected PPE (helmets, vests) to individual workers based on anatomical geometry:
    - Hard hat / helmet is located at worker's head region (top 30% of worker box).
    - High-visibility vest is located at worker's torso region (20% to 75% of worker box).
    """
    associated_workers = []

    for w in workers:
        w_box = w["box"]
        w_h = w_box["y2"] - w_box["y1"]
        w_w = w_box["x2"] - w_box["x1"]

        # Anatomical regions
        head_box = {
            "x1": w_box["x1"] - (w_w * 0.1),
            "y1": w_box["y1"] - (w_h * 0.1),
            "x2": w_box["x2"] + (w_w * 0.1),
            "y2": w_box["y1"] + (w_h * 0.35)
        }

        torso_box = {
            "x1": w_box["x1"] - (w_w * 0.05),
            "y1": w_box["y1"] + (w_h * 0.20),
            "x2": w_box["x2"] + (w_w * 0.05),
            "y2": w_box["y1"] + (w_h * 0.75)
        }

        has_helmet = False
        helmet_conf = 0.0
        has_vest = False
        vest_conf = 0.0

        for eq in equipments:
            eq_box = eq["box"]
            cls_name = eq.get("class_name", "").lower()

            if "helmet" in cls_name or "hardhat" in cls_name or "hat" in cls_name:
                # Check containment or overlap with head region
                eq_cx = (eq_box["x1"] + eq_box["x2"]) / 2.0
                eq_cy = (eq_box["y1"] + eq_box["y2"]) / 2.0
                if (head_box["x1"] <= eq_cx <= head_box["x2"]) and (head_box["y1"] <= eq_cy <= head_box["y2"]):
                    has_helmet = True
                    helmet_conf = max(helmet_conf, eq.get("confidence", 0.0))

            elif "vest" in cls_name or "jacket" in cls_name or "reflective" in cls_name:
                eq_cx = (eq_box["x1"] + eq_box["x2"]) / 2.0
                eq_cy = (eq_box["y1"] + eq_box["y2"]) / 2.0
                if (torso_box["x1"] <= eq_cx <= torso_box["x2"]) and (torso_box["y1"] <= eq_cy <= torso_box["y2"]):
                    has_vest = True
                    vest_conf = max(vest_conf, eq.get("confidence", 0.0))

        worker_entry = dict(w)
        worker_entry["has_helmet"] = has_helmet
        worker_entry["helmet_confidence"] = helmet_conf
        worker_entry["has_vest"] = has_vest
        worker_entry["vest_confidence"] = vest_conf
        associated_workers.append(worker_entry)

    return associated_workers
