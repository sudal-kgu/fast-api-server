import asyncio
import json
from aio_pika import Channel, Message
from aio_pika.abc import AbstractIncomingMessage

from app.message.producer import ResultMessageProducer
from app.services.analysis import run_analysis
from app.core.config import settings

MAX_RETRY_COUNT = 1


class RequestMessageConsumer:
    def __init__(self, producer: ResultMessageProducer):
        self.producer = producer
        self.channel: Channel | None = None

    async def start_consuming(self, channel: Channel):
        self.channel = channel
        await channel.set_qos(prefetch_count=4)
        queue = await channel.declare_queue(settings.RABBITMQ_REQUEST_QUEUE, durable=True)
        await queue.consume(self.consume)
        print(f"[MQ] Consumer started on queue: {settings.RABBITMQ_REQUEST_QUEUE}")

    async def consume(self, message: AbstractIncomingMessage):
        request_id = json.loads(message.body.decode("utf-8"))
        print(f"[MQ] Received request_id: {request_id}")

        retry_count = int(message.headers.get("x-retry-count", 0))

        try:
            result_data = await asyncio.to_thread(run_analysis, request_id)

            if result_data is None:
                print(f"[MQ] Image not found for request_id: {request_id}")
                await self.producer.publish_result({
                    "request_id": request_id,
                    "error": "IMAGE_NOT_FOUND",
                })
                await message.ack()
                return

            await self.producer.publish_result(result_data)
            await message.ack()

        except Exception as e:
            print(f"[MQ] Analysis failed for request_id: {request_id}, attempt: {retry_count + 1}, error: {e}")
            await message.ack()

            if retry_count < MAX_RETRY_COUNT:
                retry_message = Message(
                    body=message.body,
                    headers={"x-retry-count": retry_count + 1},
                )
                await self.channel.default_exchange.publish(
                    retry_message,
                    routing_key=settings.RABBITMQ_REQUEST_QUEUE,
                )
            else:
                print(f"[MQ] Max retries reached for request_id: {request_id}")
                await self.producer.publish_result({
                    "request_id": request_id,
                    "error": "ANALYSIS_FAILED",
                })
