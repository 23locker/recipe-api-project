import asyncio
import os

import pytest
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from tortoise import Tortoise

os.environ["ENV"] = "test"
os.environ["DATABASE_URL"] = (
    "postgres://recipe_user_test:recipe_password_test@localhost:5434/recipe_db_test"
)
os.environ["MONGODB_URL"] = "mongodb://localhost:27017"
os.environ["MONGODB_DB"] = "recipe_db_test"
os.environ["REDIS_URL"] = "redis://localhost:6381/0"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    await Tortoise.init(
        db_url=os.environ["DATABASE_URL"],
        modules={
            "models": [
                "app.models.tortoise.user",
                "app.models.tortoise.category",
                "app.models.tortoise.ingredient",
                "app.models.tortoise.substitute",
            ]
        },
    )
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()
    yield


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def admin_client():
    from app.models.tortoise.user import User
    from app.utils.security import create_access_token, hash_password

    admin = await User.create(
        username="admin_test",
        email="admin_test@example.com",
        password_hash=hash_password("adminpass"),
        role="admin",
    )

    token = create_access_token({"user_id": admin.id})
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        ac.headers.update({"Authorization": f"Bearer {token}"})
        yield ac


@pytest.fixture
async def user_client():
    from app.models.tortoise.user import User
    from app.utils.security import create_access_token, hash_password

    user = await User.create(
        username="user_test",
        email="user_test@example.com",
        password_hash=hash_password("userpass"),
        role="user",
    )

    token = create_access_token({"user_id": user.id})
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        ac.headers.update({"Authorization": f"Bearer {token}"})
        yield ac


@pytest.fixture(autouse=True)
async def db_cleanup(client):
    from app.models.tortoise.category import Category
    from app.models.tortoise.ingredient import Ingredient
    from app.models.tortoise.substitute import Substitute
    from app.models.tortoise.user import User

    try:
        await User.all().delete()
        await Category.all().delete()
        await Ingredient.all().delete()
        await Substitute.all().delete()
    except Exception as e:
        pass

    try:
        m_client = AsyncIOMotorClient(os.environ["MONGODB_URL"])
        db = m_client[os.environ["MONGODB_DB"]]
        collections = await db.list_collection_names()
        for col in collections:
            await db[col].delete_many({})
        m_client.close()
    except Exception as e:
        pass

    yield
