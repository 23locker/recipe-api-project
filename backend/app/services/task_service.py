import json
import aio_pika
from app.config import settings

class TaskService:
    def __init__(self):
        self.connection = None
        self.channel = None

    async def get_channel(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        if self.channel is None or self.channel.is_closed:
            self.channel = await self.connection.channel()
            await self.channel.declare_queue("recipe_tasks", durable=True)
        return self.channel

    async def publish_task(self, task_type: str, data: dict):
        channel = await self.get_channel()
        message_body = json.dumps({"type": task_type, "data": data})
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key="recipe_tasks"
        )
        print(f" [x] Sent task: {task_type}")

    async def close(self):
        if self.connection:
            await self.connection.close()

task_service = TaskService()
