import numpy as np

from app.dependencies import detector, storage
from app.services.llm_fallback import classify_with_llm


def _build_yolo_response(results: list, request_id: str) -> dict:
    detected_items = []
    for item in results:
        filename = storage.save_crop(item["crop"], request_id)
        detected_items.append({
            "category": item["category"],
            "confidence": item["confidence"],
            "filename": filename,
        })
    return {
        "request_id": request_id,
        "count": len(detected_items),
        "detected_items": detected_items,
        "source": "yolo",
    }


def _build_llm_response(image: np.ndarray, request_id: str) -> dict:
    category = classify_with_llm(image)
    if category is None:
        return {
            "request_id": request_id,
            "count": 0,
            "detected_items": [],
            "source": "llm",
        }
    filename = storage.save_crop(image, request_id)
    return {
        "request_id": request_id,
        "count": 1,
        "detected_items": [{"category": category, "confidence": None, "filename": filename}],
        "source": "llm",
    }


def run_analysis(request_id: str) -> dict | None:
    image = storage.load_image(request_id)
    if image is None:
        return None

    results = detector.detect(image)
    if results:
        return _build_yolo_response(results, request_id)
    return _build_llm_response(image, request_id)
