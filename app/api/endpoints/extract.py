from fastapi import APIRouter, HTTPException

from app.schemas.request import ExtractRequest
from app.schemas.response import ExtractResponse
from app.services.analysis import run_analysis

router = APIRouter()


@router.post("/extracts", response_model=ExtractResponse)
def extract(data: ExtractRequest):
    result = run_analysis(data.request_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Image not found.")
    return ExtractResponse(**result)
