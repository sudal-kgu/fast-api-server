import json
from aio_pika import Channel, Message
from aio_pika.abc import AbstractExchange

from app.core.config import settings


class ResultMessageProducer:
    def __init__(self, channel: Channel):
        self.channel = channel
        self.exchange: AbstractExchange | None = None

    async def initialize(self):
        self.exchange = await self.channel.get_exchange(settings.RABBITMQ_EXCHANGE)

    async def publish_result(self, result_data: dict):
        message = Message(
            body=json.dumps(result_data).encode("utf-8"),
            content_type="application/json",
        )

        await self.exchange.publish(message, routing_key=settings.RABBITMQ_RESULT_ROUTING_KEY)
        print(f"[MQ] Sent result for request_id: {result_data.get('request_id')}")
