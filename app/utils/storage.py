import os
import uuid
import glob

import cv2
import numpy as np
from PIL import Image

from app.core.config import settings


class ImageStorage:
    def __init__(self):
        self.origin_dir = settings.ORIGIN_IMAGE_DIR
        self.crop_dir = settings.CROP_IMAGE_DIR
        os.makedirs(self.origin_dir, exist_ok=True)
        os.makedirs(self.crop_dir, exist_ok=True)

    def load_image(self, request_id: str) -> np.ndarray | None:
        pattern = os.path.join(self.origin_dir, f"{request_id}.*")
        matches = glob.glob(pattern)

        if not matches:
            return None

        img_pil = Image.open(matches[0])
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    def save_crop(self, crop: np.ndarray, request_id: str) -> str:
        target_dir = os.path.join(self.crop_dir, request_id)
        os.makedirs(target_dir, exist_ok=True)

        filename = f"{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join(target_dir, filename)
        cv2.imwrite(filepath, crop, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

        return filename
