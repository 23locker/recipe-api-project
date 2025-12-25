from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_admin_user
from app.models.tortoise.user import User

router = APIRouter()


@router.post("/parse-stores")
async def parse_stores(current_user: User = Depends(get_admin_user)):
    """
    Запустить парсер магазина Пятерочка (только админ)

    Временно - заглушка. Позже подключим реальный парсер.
    """
    return {
        "status": "success",
        "message": "Parser started in background",
        "timestamp": None,  # Пока не реализовано
    }


@router.get("/stats")
async def get_stats(current_user: User = Depends(get_admin_user)):
    """Получить статистику (только админ)"""
    return {"status": "success", "message": "Stats will be here soon"}
