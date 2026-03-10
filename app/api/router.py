from fastapi import APIRouter

from app.api.endpoints import extract, test

api_router = APIRouter()
api_router.include_router(extract.router, tags=["extract"])
api_router.include_router(test.router, tags=["test"])
