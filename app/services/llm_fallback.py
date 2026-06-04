import logging

import cv2
import numpy as np
from PIL import Image as PILImage

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.50

VALID_CLASSES = {
    "공통(가구류)", "고철(고철류)", "비철금속(고철류)", "주전자(고철류)", "프라이팬(고철류)",
    "도마(나무)", "액자(나무)", "장식품(나무)", "주걱(나무)", "주방용품(나무)",
    "그릇류(도기류)", "뚝배기(도기류)", "병(도기류)", "컵(도기류)", "항아리(도기류)", "화분(도기류)",
    "식품봉지(비닐)", "리필용기(비닐)", "봉투(비닐)", "에어캡(비닐)", "포장재(비닐)",
    "네모트레이(스티로폼류)", "보호재(스티로폼류)", "일반스티로폼(스티로폼류)", "포장용기(스티로폼류)",
    "기타술병(유리병)", "맥주병(유리병)", "박카스병(유리병)", "소주병(유리병)", "음료병(유리병)",
    "상의(의류)", "원피스(의류)", "하의(의류)",
    "두발자전거(자전거)",
    "TV(전자제품)", "가습기(전자제품)", "냉장고(전자제품)", "세탁기(전자제품)", "컴퓨터(전자제품)",
    "노트(종이)", "상자류(종이)", "신문지(종이)", "음료수곽(종이)", "포장상자(종이)",
    "음료(캔류)", "통조림(캔류)",
    "일회용컵(페트병류)", "일반페트병(페트병류)",
    "대용량통(플라스틱)", "밀폐용기(플라스틱)", "바구니(플라스틱)", "욕실용품(플라스틱)", "장난감(플라스틱)",
    "공통(형광등)",
}

_PROMPT = """이 이미지에 있는 쓰레기를 아래 카테고리 중 하나로 분류해줘.
반드시 아래 목록 중 정확히 하나만 골라서 카테고리 이름만 답해줘. 다른 말은 하지 마.

카테고리 목록:
공통(가구류), 고철(고철류), 비철금속(고철류), 주전자(고철류), 프라이팬(고철류),
도마(나무), 액자(나무), 장식품(나무), 주걱(나무), 주방용품(나무),
그릇류(도기류), 뚝배기(도기류), 병(도기류), 컵(도기류), 항아리(도기류), 화분(도기류),
식품봉지(비닐), 리필용기(비닐), 봉투(비닐), 에어캡(비닐), 포장재(비닐),
네모트레이(스티로폼류), 보호재(스티로폼류), 일반스티로폼(스티로폼류), 포장용기(스티로폼류),
기타술병(유리병), 맥주병(유리병), 박카스병(유리병), 소주병(유리병), 음료병(유리병),
상의(의류), 원피스(의류), 하의(의류),
두발자전거(자전거),
TV(전자제품), 가습기(전자제품), 냉장고(전자제품), 세탁기(전자제품), 컴퓨터(전자제품),
노트(종이), 상자류(종이), 신문지(종이), 음료수곽(종이), 포장상자(종이),
음료(캔류), 통조림(캔류),
일회용컵(페트병류), 일반페트병(페트병류),
대용량통(플라스틱), 밀폐용기(플라스틱), 바구니(플라스틱), 욕실용품(플라스틱), 장난감(플라스틱),
공통(형광등)"""


def _to_pil(image: np.ndarray) -> PILImage.Image:
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return PILImage.fromarray(rgb)


def _call_gemini(image: np.ndarray) -> str:
    from google import genai
    from app.core.config import settings

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[_PROMPT, _to_pil(image)],
    )
    return response.text.strip()


def _validate_category(text: str) -> str | None:
    if text not in VALID_CLASSES:
        logger.warning("LLM returned invalid category: %r", text)
        return None
    return text


def classify_with_llm(image: np.ndarray) -> str | None:
    from app.core.config import settings

    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set, skipping LLM fallback")
        return None

    try:
        return _validate_category(_call_gemini(image))
    except Exception as e:
        logger.error("LLM fallback failed: %s", e)
        return None
