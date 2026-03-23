from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection

from app.core.config import settings
from app.message.producer import ResultMessageProducer
from app.message.consumer import RequestMessageConsumer


async def init_rabbitmq() -> AbstractRobustConnection | None:
    try:
        url = f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/"
        connection = await connect_robust(url)
        channel = await connection.channel()

        producer = ResultMessageProducer(channel)
        await producer.initialize()
        consumer = RequestMessageConsumer(producer)
        await consumer.start_consuming(channel)

        print(f"[MQ] Connected to RabbitMQ ({settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT})")
        return connection

    except Exception as e:
        print(f"[MQ] Failed to connect: {e}")
        return None


async def close_rabbitmq(connection: AbstractRobustConnection | None):
    if connection:
        await connection.close()
        print("[MQ] Connection closed.")