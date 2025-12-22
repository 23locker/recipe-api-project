from tortoise import Tortoise

from app.config import settings

TORTOISE_ORM = {
    "connection": {"default": settings.DATABASE_URL},
    "apps": {
        "models": [
            "app.models.tortoise.user",
            "app.models.tortoise.category",
            "app.models.tortoise.ingredient",
            "app.models.tortoise.substitute",
        ],
        "default_connection": "default",
    },
}


async def init_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print(f"✅ Tortoise ORM работает")


async def close_tortoise():
    await Tortoise.close_connections()
    print("❌ Tortoise ORM выключился")
