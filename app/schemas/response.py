from pydantic import BaseModel


class DetectedItem(BaseModel):
    category: str
    confidence: float
    filename: str


class ExtractResponse(BaseModel):
    request_id: str
    count: int
    detected_items: list[DetectedItem]
