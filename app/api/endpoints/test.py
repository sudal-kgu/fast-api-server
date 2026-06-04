from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2

from app.schemas.response import ExtractResponse, DetectedItem
from app.dependencies import detector, storage
from app.services.llm_fallback import classify_with_llm

router = APIRouter()

REQUEST_ID = "test"


@router.post("/test/detect", response_model=ExtractResponse)
def test_detect(file: UploadFile = File(...)):
    raw = np.frombuffer(file.file.read(), np.uint8)
    image = cv2.imdecode(raw, cv2.IMREAD_COLOR)

    results = detector.detect(image)

    if results:
        detected_items = []
        for item in results:
            filename = storage.save_crop(item["crop"], REQUEST_ID)
            detected_items.append(DetectedItem(
                category=item["category"],
                confidence=item["confidence"],
                filename=filename,
            ))
        return ExtractResponse(
            request_id=REQUEST_ID,
            count=len(detected_items),
            detected_items=detected_items,
            source="yolo",
        )

    category = classify_with_llm(image)
    if category is None:
        return ExtractResponse(
            request_id=REQUEST_ID,
            count=0,
            detected_items=[],
            source="llm",
        )

    filename = storage.save_crop(image, REQUEST_ID)
    return ExtractResponse(
        request_id=REQUEST_ID,
        count=1,
        detected_items=[DetectedItem(category=category, confidence=None, filename=filename)],
        source="llm",
    )