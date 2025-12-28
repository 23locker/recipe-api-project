from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.api.v1 import admin, auth, category, ingredients, recipes, store
from app.db.mongodb import close_mongodb, init_mongodb
from app.db.tortoise_config import TORTOISE_ORM, close_tortoise, init_tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_tortoise()
    await init_mongodb()
    print("✅ Databases initialized")

    yield

    await close_tortoise()
    await close_mongodb()
    print("❌ Databases closed")


app = FastAPI(
    title="Recipe API",
    description="API для рецептов с пагинацией, заменами ингредиентов",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== ROUTES ======
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(recipes.router, prefix="/api/v1/recipes", tags=["recipes"])
app.include_router(
    ingredients.router, prefix="/api/v1/ingredients", tags=["ingredients"]
)
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(category.router, prefix="/api/v1/category", tags=["category"])
app.include_router(store.router, prefix="/api/v1/store", tags=["store"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
