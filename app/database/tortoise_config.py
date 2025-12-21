from tortoise import Tortoise

from app.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.tortoise.user",
                "app.models.tortoise.category",
                "app.models.tortoise.ingredient",
                "app.models.tortoise.substitute",
            ],
            "default_connection": "default",
        }
    },
}


async def init_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_tortoise():
    await Tortoise.close_connections()
