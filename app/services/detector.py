import cv2
import numpy as np
import torch
from ultralytics import YOLO

from app.core.config import settings


class WasteDetector:
    def __init__(self):
        self.device = self._get_device()
        self.model = YOLO(settings.YOLO_MODEL_PATH).to(self.device)

    def _get_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def detect(self, image: np.ndarray) -> list[dict]:
        results = self.model.predict(
            source=image,
            conf=settings.YOLO_CONFIDENCE,
            verbose=False,
        )

        detected_items = []
        for result in results:
            for box in result.boxes:
                crop = self._get_padded_crop(image, box)
                if crop.size == 0:
                    continue

                category = self.model.names[int(box.cls[0])]
                confidence = round(float(box.conf[0]), 3)

                detected_items.append({
                    "category": category,
                    "confidence": confidence,
                    "crop": crop,
                })

        return detected_items

    def _get_padded_crop(self, img: np.ndarray, box) -> np.ndarray:
        h, w = img.shape[:2]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        pad_w, pad_h = int((x2 - x1) * 0.1), int((y2 - y1) * 0.1)
        x1 = max(0, x1 - pad_w)
        y1 = max(0, y1 - pad_h)
        x2 = min(w, x2 + pad_w)
        y2 = min(h, y2 + pad_h)
        return img[y1:y2, x1:x2]
