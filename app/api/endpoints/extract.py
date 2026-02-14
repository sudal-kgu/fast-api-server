from fastapi import APIRouter, HTTPException

from app.schemas.request import ExtractRequest
from app.schemas.response import ExtractResponse, DetectedItem
from app.services.detector import WasteDetector
from app.utils.storage import ImageStorage

router = APIRouter()
detector = WasteDetector()
storage = ImageStorage()


@router.post("/extracts", response_model=ExtractResponse)
def extract(data: ExtractRequest):
    image = storage.load_image(data.request_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found.")

    results = detector.detect(image)

    detected_items = []
    for item in results:
        filename = storage.save_crop(item["crop"], data.request_id)
        detected_items.append(DetectedItem(
            category=item["category"],
            confidence=item["confidence"],
            filename=filename,
        ))

    return ExtractResponse(
        request_id=data.request_id,
        count=len(detected_items),
        detected_items=detected_items,
    )
