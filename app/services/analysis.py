from app.dependencies import detector, storage


def _build_detected_items(results: list, request_id: str) -> list:
    detected_items = []
    for item in results:
        filename = storage.save_crop(item["crop"], request_id)
        detected_items.append({
            "category": item["category"],
            "confidence": item["confidence"],
            "filename": filename,
        })
    return detected_items


def run_analysis(request_id: str) -> dict | None:
    image = storage.load_image(request_id)
    if image is None:
        return None

    results = detector.detect(image)
    detected_items = _build_detected_items(results, request_id)

    return {
        "request_id": request_id,
        "count": len(detected_items),
        "detected_items": detected_items,
    }
