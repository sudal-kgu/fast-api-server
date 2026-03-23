from app.dependencies import detector, storage


def run_analysis(request_id: str) -> dict | None:
    image = storage.load_image(request_id)
    if image is None:
        return None

    results = detector.detect(image)
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
    }
