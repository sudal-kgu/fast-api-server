from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    YOLO_MODEL_PATH: str = "models/best.pt" # 아직 없음
    ORIGIN_IMAGE_DIR: str = "./images/inputs"
    CROP_IMAGE_DIR: str = "./images/outputs"
    YOLO_CONFIDENCE: float = 0.25

    class Config:
        env_file = ".env"


settings = Settings()
