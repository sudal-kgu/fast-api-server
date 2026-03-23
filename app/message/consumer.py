import asyncio
import json
from aio_pika import Channel
from aio_pika.abc import AbstractIncomingMessage

from app.message.producer import ResultMessageProducer
from app.services.analysis import run_analysis
from app.core.config import settings


class RequestMessageConsumer:
    def __init__(self, producer: ResultMessageProducer):
        self.producer = producer

    async def start_consuming(self, channel: Channel):
        await channel.set_qos(prefetch_count=4)
        queue = await channel.declare_queue(settings.RABBITMQ_REQUEST_QUEUE, durable=True)
        await queue.consume(self.consume)
        print(f"[MQ] Consumer started on queue: {settings.RABBITMQ_REQUEST_QUEUE}")

    async def consume(self, message: AbstractIncomingMessage):
        async with message.process():
            request_id = json.loads(message.body.decode("utf-8"))
            print(f"[MQ] Received request_id: {request_id}")

            result_data = await asyncio.to_thread(run_analysis, request_id)

            if result_data is None:
                result_data = {
                    "request_id": request_id,
                    "count": 0,
                    "detected_items": [],
                    "error": "Image not found.",
                }

            await self.producer.publish_result(result_data)
