from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import api_router
from app.message.rabbitmq import init_rabbitmq, close_rabbitmq


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = await init_rabbitmq()
    yield
    await close_rabbitmq(connection)


app = FastAPI(title="Waste Detection API", version="1.0.0", lifespan=lifespan)
app.include_router(api_router)
