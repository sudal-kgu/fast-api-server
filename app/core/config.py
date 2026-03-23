from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    YOLO_MODEL_PATH: str = "models/best.pt" # 아직 없음
    ORIGIN_IMAGE_DIR: str = "./images/inputs"
    CROP_IMAGE_DIR: str = "./images/outputs"
    YOLO_CONFIDENCE: float = 0.25

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USERNAME: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_EXCHANGE: str = "analysis.exchange"
    RABBITMQ_REQUEST_QUEUE: str = "analysis.request.queue"
    RABBITMQ_RESULT_ROUTING_KEY: str = "analysis.result"

    class Config:
        env_file = ".env"


settings = Settings()
