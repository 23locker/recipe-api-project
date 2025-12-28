from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_admin_user
from app.models.tortoise.user import User
from app.services.task_service import task_service

router = APIRouter()


@router.post("/parse-stores")
async def parse_stores(current_user: User = Depends(get_admin_user)):
    """
    Запустить парсер магазина Пятерочка (только админ)
    """
    await task_service.publish_task("sync_store_prices", {})
    return {
        "status": "success",
        "message": "Parser started in background",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/stats")
async def get_stats(current_user: User = Depends(get_admin_user)):
    """Получить статистику (только админ)"""
    return {"status": "success", "message": "Stats will be here soon"}
