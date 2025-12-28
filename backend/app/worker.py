import asyncio
import json

import aio_pika
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import settings
from app.db.mongodb import close_mongodb, get_mongodb, init_mongodb


async def process_task(message: aio_pika.IncomingMessage):
    async with message.process():
        body = json.loads(message.body.decode())
        task_type = body.get("type")
        data = body.get("data")

        print(f" [v] Processing task: {task_type}")

        if task_type == "sync_store_prices":
            # Имитация обновления цен из магазина
            db = await get_mongodb()
            collection = db.store_products

            # В реальности нужно будет доделать парсинг
            result = await collection.update_many(
                {}, {"$set": {"updated_at": "2025-10-27T12:00:00"}}
            )
            print(f" [x] Updated {result.modified_count} prices")

        await asyncio.sleep(2)
        print(f" [x] Task {task_type} completed")


async def main():
    await init_mongodb()

    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue("recipe_tasks", durable=True)

    print(" [*] Waiting for tasks. To exit press CTRL+C")

    await queue.consume(process_task)

    try:
        await asyncio.Future()
    finally:
        await connection.close()
        await close_mongodb()


if __name__ == "__main__":
    asyncio.run(main())
